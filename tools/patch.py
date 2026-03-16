"""Main CLI entry point for the Teardown MP Mod Patcher."""

import json
import shutil
import time as _time
from pathlib import Path

import click

from tools.ingest import ingest_mod, ingest_batch
from tools.analyze import analyze_mod
from tools.rewrite_template import rewrite_script, update_info_txt
from tools.rewrite_ai import rewrite_script_ai
from tools.validate import validate_mod
from tools.package import package_mod
from tools.dashboard import generate_dashboard
from tools.release import release_mod, release_all


OUTPUT_DIR = Path("mods")


@click.group()
def cli():
    """Teardown MP Mod Patcher - Patch v1 mods for multiplayer."""
    pass


@cli.command()
@click.option("--mod", "mod_path", type=click.Path(exists=True), help="Path to a single mod folder")
@click.option("--batch", "batch_path", type=click.Path(exists=True), help="Path to Workshop content folder")
@click.option("--analyze-only", is_flag=True, help="Only analyze, don't rewrite")
@click.option("--force", is_flag=True, help="Re-process even if already done")
def patch(mod_path, batch_path, analyze_only, force):
    """Run the full patching pipeline on one or more mods."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    if mod_path:
        mod_path = Path(mod_path)
        workshop_id = mod_path.name
        _process_mod(mod_path, workshop_id, analyze_only, force)
    elif batch_path:
        batch_path = Path(batch_path)
        for i, sub in enumerate(sorted(batch_path.iterdir())):
            if sub.is_dir() and (sub / "info.txt").exists():
                _process_mod(sub, sub.name, analyze_only, force)
                if i > 0:
                    _time.sleep(2)
    else:
        click.echo("Provide --mod or --batch")


def _process_mod(mod_path: Path, workshop_id: str, analyze_only: bool, force: bool):
    """Process a single mod through the pipeline."""
    mod_output = OUTPUT_DIR / workshop_id
    meta_path = mod_output / "metadata.json"

    # Check idempotency
    if meta_path.exists() and not force:
        meta = json.loads(meta_path.read_text())
        if meta.get("manual_edits"):
            click.echo(f"  Skipping {workshop_id} (manual edits, use --force)")
            return
        if meta.get("status") in ("patched", "packaged", "released"):
            click.echo(f"  Skipping {workshop_id} (already {meta['status']})")
            return

    # Phase 1: Ingest
    click.echo(f"[1/6] Ingesting {workshop_id}...")
    result = ingest_mod(mod_path, OUTPUT_DIR, workshop_id)
    if result is None:
        click.echo(f"  Skipped (already v2)")
        return

    # Phase 2: Analyze
    click.echo(f"[2/6] Analyzing {result['name']}...")
    original_dir = mod_output / "original"
    analysis = analyze_mod(original_dir)
    (mod_output / "analysis.json").write_text(json.dumps(analysis, indent=2))
    click.echo(f"  Type: {analysis['mod_type']}, Complexity: {analysis['complexity']}, Approach: {analysis['estimated_approach']}")

    if analyze_only:
        meta = json.loads(meta_path.read_text())
        meta["status"] = "analyzed"
        meta_path.write_text(json.dumps(meta, indent=2))
        click.echo(f"  Analysis saved. Stopping (--analyze-only)")
        return

    # Phase 3: Rewrite
    click.echo(f"[3/6] Rewriting ({analysis['estimated_approach']})...")
    patched_dir = mod_output / "patched"
    if patched_dir.exists():
        shutil.rmtree(patched_dir)
    shutil.copytree(original_dir, patched_dir)

    rewrite_failed = False
    for script in analysis["scripts"]:
        lua_path = patched_dir / script["file"]
        source = lua_path.read_text(encoding="utf-8")

        try:
            if analysis["estimated_approach"] == "template":
                rewritten = rewrite_script(source, script, mod_type=analysis["mod_type"])
            else:
                cache_dir = mod_output / ".ai_cache"
                rewritten = rewrite_script_ai(source, script, cache_dir=cache_dir)

            lua_path.write_text(rewritten, encoding="utf-8")
            click.echo(f"  Rewrote {script['file']}")
        except Exception as e:
            click.echo(f"  FAILED {script['file']}: {e}")
            if analysis["estimated_approach"] == "template":
                click.echo(f"  Falling back to AI rewrite...")
                try:
                    cache_dir = mod_output / ".ai_cache"
                    rewritten = rewrite_script_ai(source, script, cache_dir=cache_dir)
                    lua_path.write_text(rewritten, encoding="utf-8")
                    click.echo(f"  AI rewrite succeeded for {script['file']}")
                except Exception as e2:
                    click.echo(f"  AI fallback also failed: {e2}")
                    rewrite_failed = True
            else:
                rewrite_failed = True

    # Update info.txt
    update_info_txt(patched_dir / "info.txt")

    if rewrite_failed:
        meta = json.loads(meta_path.read_text())
        meta["status"] = "rewrite_failed"
        meta_path.write_text(json.dumps(meta, indent=2))
        click.echo(f"  Status: rewrite_failed")
        return

    # Phase 4: Validate
    click.echo(f"[4/6] Validating...")
    val_result = validate_mod(patched_dir, original_dir=original_dir)

    # Count passes/total across all file checks + info + file_complete
    total = 0
    passed_count = 0
    if val_result.get("info_check"):
        total += 1
        if val_result["info_check"]["passed"]:
            passed_count += 1
    if val_result.get("file_complete"):
        total += 1
        if val_result["file_complete"]["passed"]:
            passed_count += 1
    for f in val_result.get("files", []):
        for c in f.get("checks", []):
            total += 1
            if c["passed"]:
                passed_count += 1
    click.echo(f"  Checks: {passed_count}/{total} passed")

    meta = json.loads(meta_path.read_text())
    if not val_result["all_passed"]:
        meta["status"] = "validation_failed"
        meta_path.write_text(json.dumps(meta, indent=2))
        if val_result.get("info_check") and not val_result["info_check"]["passed"]:
            click.echo(f"  FAIL: {val_result['info_check']['check']} - {val_result['info_check'].get('detail', '')}")
        if val_result.get("file_complete") and not val_result["file_complete"]["passed"]:
            click.echo(f"  FAIL: {val_result['file_complete']['check']} - {val_result['file_complete'].get('detail', '')}")
        for f in val_result.get("files", []):
            for c in f.get("checks", []):
                if not c["passed"]:
                    click.echo(f"  FAIL: {c['check']} ({f['file']}) - {c.get('detail', '')}")
        return
    else:
        meta["status"] = "patched"
        meta_path.write_text(json.dumps(meta, indent=2))

    # Phase 5: Package
    click.echo(f"[5/6] Packaging...")
    pkg = package_mod(mod_output)
    click.echo(f"  Created: {pkg['zip_path'].name}")

    click.echo(f"[6/6] Done! Ready for release.")


@cli.command()
@click.option("--mod", "mod_path", type=click.Path(exists=True))
def validate(mod_path):
    """Validate a patched mod."""
    from tools.validate import validate_mod as vm
    result = vm(Path(mod_path))
    total = 0
    passed_count = 0
    if result.get("info_check"):
        total += 1
        status = "PASS" if result["info_check"]["passed"] else "FAIL"
        if result["info_check"]["passed"]:
            passed_count += 1
        click.echo(f"  [{status}] {result['info_check']['check']}: {result['info_check'].get('detail', 'OK')}")
    for f in result.get("files", []):
        for c in f.get("checks", []):
            total += 1
            status = "PASS" if c["passed"] else "FAIL"
            if c["passed"]:
                passed_count += 1
            click.echo(f"  [{status}] {c['check']} ({f['file']}): {c.get('detail', 'OK')}")
    click.echo(f"\n{passed_count}/{total} checks passed")


@cli.command()
def dashboard():
    """Regenerate README dashboard."""
    readme = generate_dashboard(OUTPUT_DIR)
    Path("README.md").write_text(readme, encoding="utf-8")
    click.echo("README.md updated")


@cli.command()
@click.option("--all", "release_all_flag", is_flag=True)
@click.option("--mod", "workshop_id")
def release(release_all_flag, workshop_id):
    """Create GitHub releases."""
    if release_all_flag:
        results = release_all(OUTPUT_DIR)
        for r in results:
            if "error" in r:
                click.echo(f"  FAIL {r['workshop_id']}: {r['error']}")
            else:
                click.echo(f"  Released {r['workshop_id']}: {r['url']}")
    elif workshop_id:
        result = release_mod(OUTPUT_DIR / workshop_id)
        if "error" in result:
            click.echo(f"FAIL: {result['error']}")
        else:
            click.echo(f"Released: {result['url']}")


if __name__ == "__main__":
    cli()
