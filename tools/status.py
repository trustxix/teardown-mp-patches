"""Session boot script — single-command project status report."""

import subprocess
from pathlib import Path

import click

from tools.common import LIVE_MODS_DIR, LOG_PATH, discover_mods, read_lua_files


def build_status_report(mods_dir: Path | None = None, skip_git: bool = False, skip_log: bool = False) -> str:
    if mods_dir is None:
        mods_dir = LIVE_MODS_DIR

    lines = []
    lines.append("TEARDOWN MP PATCHER -- Status")
    lines.append("=" * 50)

    # Mod count
    mods = discover_mods(mods_dir)
    lines.append(f"Mods installed:   {len(mods)}")

    # Git
    if skip_git:
        lines.append("Last commit:      N/A")
    else:
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--oneline"],
                capture_output=True, text=True, timeout=5,
                cwd=str(Path(__file__).parent.parent)
            )
            commit = result.stdout.strip() if result.returncode == 0 else "N/A"
            lines.append(f"Last commit:      {commit}")
        except Exception:
            lines.append("Last commit:      N/A")

    # Game log
    if skip_log:
        lines.append("Game log:         N/A")
    else:
        try:
            log_path = LOG_PATH
            if log_path.exists():
                from tools.logparse import parse_log
                content = log_path.read_text(encoding="utf-8", errors="replace")
                log_result = parse_log(content)
                total_errors = sum(len(errs) for errs in log_result["mods"].values())
                mod_count = len(log_result["mods"])
                if total_errors == 0:
                    lines.append(f"Game log:         Teardown {log_result['version']} - 0 errors")
                else:
                    lines.append(f"Game log:         {mod_count} mod(s) with errors, {total_errors} total")
                    for mod_name, errors in sorted(log_result["mods"].items())[:3]:
                        err = errors[0]
                        if err["type"] == "runtime":
                            lines.append(f"  - {mod_name} line {err['line']}: {err['message'][:60]}")
                        else:
                            lines.append(f"  - {mod_name}: {err['type']}")
            else:
                lines.append("Game log:         not found")
        except Exception:
            lines.append("Game log:         N/A")

    # Lint tier-1
    try:
        from tools.lint import lint_source
        tier1_errors = []
        for mod_dir in mods:
            for rel_path, source in read_lua_files(mod_dir):
                if rel_path == "options.lua":
                    continue
                findings = lint_source(source, rel_path, tier="1")
                for f in findings:
                    f["mod"] = mod_dir.name
                    tier1_errors.append(f)

        lines.append("")
        if not tier1_errors:
            lines.append(f"Lint (Tier 1):    0 hard errors across {len(mods)} mods [OK]")
        else:
            lines.append(f"Lint (Tier 1):    {len(tier1_errors)} hard errors")
            for e in tier1_errors[:5]:
                lines.append(f"  - {e['mod']}/{e['file']}:{e['line']} {e['check']}")
    except Exception:
        lines.append("\nLint (Tier 1):    N/A")

    # Missing features summary
    try:
        from tools.audit import detect_features
        missing_shoot = 0
        missing_aim = 0
        missing_pickup = 0
        gun_count = 0
        tool_count = 0

        for mod_dir in mods:
            combined: dict[str, bool] = {}
            all_suppressions: set[str] = set()
            for rel_path, source in read_lua_files(mod_dir):
                features = detect_features(source)
                for k, v in features.items():
                    if k == "suppressions":
                        all_suppressions |= v
                    else:
                        combined[k] = combined.get(k, False) or v

            if combined.get("is_gun_mod"):
                gun_count += 1
                if not combined.get("has_shoot") and "shoot" not in all_suppressions:
                    missing_shoot += 1
                if not combined.get("has_aim_info") and "aiminfo" not in all_suppressions:
                    missing_aim += 1
            if combined.get("has_register_tool"):
                tool_count += 1
                if not combined.get("has_ammo_pickup"):
                    missing_pickup += 1

        lines.append(f"Missing features: {missing_shoot}/{gun_count} gun mods need Shoot(), "
                     f"{missing_aim}/{gun_count} need AimInfo, "
                     f"{missing_pickup}/{tool_count} tool mods need AmmoPickup")
    except Exception:
        lines.append("Missing features: N/A")

    # Deep analysis test results
    try:
        from tools.common import TEST_RESULTS_DIR
        from datetime import datetime, timedelta
        if TEST_RESULTS_DIR.exists():
            tested = set()
            failed = []
            warned = 0
            newest_ts = None
            for mod_result_dir in sorted(TEST_RESULTS_DIR.iterdir()):
                if mod_result_dir.is_dir():
                    if mod_result_dir.name.startswith("__"):
                        continue  # skip test harness and internal mods
                    tested.add(mod_result_dir.name)
                    # Read most recent report
                    runs = sorted(mod_result_dir.iterdir())
                    if runs:
                        report_file = runs[-1] / "report.txt"
                        if report_file.exists():
                            text = report_file.read_text(encoding="utf-8", errors="replace")
                            if "RESULT: FAIL" in text:
                                failed.append(mod_result_dir.name)
                            elif "RESULT: WARN" in text:
                                warned += 1
                            # Track newest result timestamp from dir name (YYYY-MM-DD_HH-MM-SS)
                            try:
                                ts = datetime.strptime(runs[-1].name, "%Y-%m-%d_%H-%M-%S")
                                if newest_ts is None or ts > newest_ts:
                                    newest_ts = ts
                            except ValueError:
                                pass
            if tested:
                untested = len(mods) - len(tested)
                stale_tag = ""
                if newest_ts and (datetime.now() - newest_ts) > timedelta(hours=4):
                    age_hours = (datetime.now() - newest_ts).total_seconds() / 3600
                    stale_tag = f" (results {age_hours:.0f}h old — re-run: python -m tools.test --batch all --static)"
                if failed:
                    lines.append(f"Deep analysis:    {len(tested)} tested, {len(failed)} FAIL, {warned} WARN, {untested} untested{stale_tag}")
                    for m in failed[:3]:
                        lines.append(f"  - {m}: FAIL (run: python -m tools.test --mod \"{m}\" --static)")
                else:
                    lines.append(f"Deep analysis:    {len(tested)} tested, 0 FAIL, {warned} WARN, {untested} untested [OK]{stale_tag}")
    except Exception:
        pass

    # Task queue
    try:
        queue_path = Path(__file__).parent.parent / "TASK_QUEUE.md"
        if queue_path.exists():
            queue = queue_path.read_text(encoding="utf-8")
            open_count = queue.count("**Status:** OPEN")
            progress_count = queue.count("**Status:** IN PROGRESS")
            if open_count + progress_count > 0:
                lines.append(f"Task queue:       {open_count} open, {progress_count} in progress — run: cat TASK_QUEUE.md")
            else:
                lines.append("Task queue:       all tasks complete")
    except Exception:
        pass

    # Recommended reading based on current state
    lines.append("")
    lines.append("Recommended reading for this session:")
    docs_to_read = []

    # Always relevant
    docs_to_read.append("  CLAUDE.md - rules, tools, workflow (always)")
    docs_to_read.append("  docs/OFFICIAL_DEVELOPER_DOCS.md - GROUND TRUTH from teardowngame.com (API, MP architecture, gotchas)")

    # If there are tier-1 errors, they need the issues log for patterns
    try:
        if tier1_errors:
            docs_to_read.append("  ISSUES_AND_FIXES.md - known bug patterns and fixes")
    except NameError:
        pass

    # If gun mods need Shoot/AimInfo, they need RESEARCH.md
    try:
        if missing_shoot > 0 or missing_aim > 0:
            docs_to_read.append("  docs/RESEARCH.md - Shoot(), GetPlayerAimInfo(), QueryShot() patterns")
    except NameError:
        pass

    # If there are mods with custom entities or complex state, recommend sync patterns
    try:
        has_custom_entities = False
        for mod_dir in mods:
            for rel_path, source in read_lua_files(mod_dir):
                if any(kw in source for kw in ["SetFloat(", "ClientCall(", "ServerCall(", "shared.", "VecLerp("]):
                    has_custom_entities = True
                    break
            if has_custom_entities:
                break
        if has_custom_entities:
            docs_to_read.append("  docs/V2_SYNC_PATTERNS.md - registry sync, RPC, interpolation")
    except Exception:
        pass

    # If there are game log errors, they may need the API reference
    try:
        if log_result and log_result.get("mods"):
            docs_to_read.append("  C:/Users/trust/Documents/Teardown/TEARDOWN_V2_API_REFERENCE.md - API signatures")
    except NameError:
        pass

    # Audit report for planning
    docs_to_read.append("  docs/AUDIT_REPORT.md - feature matrix (regenerate: python -m tools.audit --output docs/AUDIT_REPORT.md)")

    for d in docs_to_read:
        lines.append(d)

    return "\n".join(lines)


@click.command("status")
def status_cli():
    """Show project status report."""
    click.echo(build_status_report())


if __name__ == "__main__":
    status_cli()
