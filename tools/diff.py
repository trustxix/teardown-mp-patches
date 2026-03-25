"""Compare patched mods against workshop originals.

Shows exactly what changed between the Steam Workshop version and your local copy.

Usage:
    python -m tools.diff                    # Diff all mods
    python -m tools.diff --mod "AC130"      # Diff one mod
    python -m tools.diff --summary          # Just show which mods differ
"""
import os
import sys
import difflib
from pathlib import Path
from tools.common import LIVE_MODS_DIR

WORKSHOP_DIR = Path("C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630")


def find_workshop_original(mod_dir: Path) -> Path | None:
    """Find the workshop original for a local mod by reading id.txt."""
    id_path = mod_dir / "id.txt"
    if not id_path.exists():
        return None
    workshop_id = id_path.read_text(errors="ignore").strip().split("\n")[0]
    workshop_path = WORKSHOP_DIR / workshop_id
    if workshop_path.exists():
        return workshop_path
    return None


def diff_file(local_path: Path, workshop_path: Path) -> list[str]:
    """Generate unified diff between two files."""
    try:
        local_lines = local_path.read_text(errors="ignore").splitlines(keepends=True)
        workshop_lines = workshop_path.read_text(errors="ignore").splitlines(keepends=True)
    except Exception:
        return []

    diff = list(difflib.unified_diff(
        workshop_lines, local_lines,
        fromfile=f"workshop/{workshop_path.parent.name}/{workshop_path.name}",
        tofile=f"local/{local_path.parent.name}/{local_path.name}",
        n=3,
    ))
    return diff


def diff_mod(mod_dir: Path, summary_only: bool = False) -> dict:
    """Diff a single mod against its workshop original."""
    result = {"name": mod_dir.name, "status": "unknown", "files_changed": [], "diff_lines": 0}

    workshop_dir = find_workshop_original(mod_dir)
    if workshop_dir is None:
        result["status"] = "no-workshop"
        return result

    # Compare all .lua files
    changed_files = []
    total_diff_lines = 0

    for lua_file in sorted(mod_dir.rglob("*.lua")):
        rel_path = lua_file.relative_to(mod_dir)
        workshop_file = workshop_dir / rel_path

        if not workshop_file.exists():
            changed_files.append({"file": str(rel_path), "status": "added"})
            continue

        diff = diff_file(lua_file, workshop_file)
        if diff:
            additions = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
            deletions = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
            changed_files.append({
                "file": str(rel_path),
                "status": "modified",
                "additions": additions,
                "deletions": deletions,
                "diff": diff if not summary_only else [],
            })
            total_diff_lines += additions + deletions

    # Check for files in workshop but not local
    if workshop_dir.exists():
        for lua_file in sorted(workshop_dir.rglob("*.lua")):
            rel_path = lua_file.relative_to(workshop_dir)
            if not (mod_dir / rel_path).exists():
                changed_files.append({"file": str(rel_path), "status": "removed"})

    if changed_files:
        result["status"] = "modified"
        result["files_changed"] = changed_files
        result["diff_lines"] = total_diff_lines
    else:
        result["status"] = "identical"

    return result


def main():
    summary_only = "--summary" in sys.argv
    mod_filter = None
    if "--mod" in sys.argv:
        idx = sys.argv.index("--mod")
        if idx + 1 < len(sys.argv):
            mod_filter = sys.argv[idx + 1]

    from tools.classify import BUILTIN_MODS

    results = []
    for d in sorted(LIVE_MODS_DIR.iterdir()):
        if not d.is_dir() or d.name.lower() in BUILTIN_MODS or d.name.startswith("__"):
            continue
        if mod_filter and mod_filter.lower() not in d.name.lower():
            continue
        results.append(diff_mod(d, summary_only))

    # Print results
    modified_count = 0
    identical_count = 0
    no_workshop_count = 0

    for r in results:
        if r["status"] == "identical":
            identical_count += 1
            if not summary_only:
                continue
        elif r["status"] == "no-workshop":
            no_workshop_count += 1
        elif r["status"] == "modified":
            modified_count += 1

        if summary_only:
            status_icon = {"identical": "=", "modified": "*", "no-workshop": "?"}
            print(f"  {status_icon.get(r['status'], '?')} {r['name']:<40} {r['status']:<12} +{r.get('diff_lines', 0)} lines")
        else:
            if r["status"] == "modified":
                print(f"\n{'='*70}")
                print(f"  {r['name']} -- {len(r['files_changed'])} files changed, {r['diff_lines']} diff lines")
                print(f"{'='*70}")
                for f in r["files_changed"]:
                    if f["status"] == "modified":
                        print(f"  M {f['file']} (+{f['additions']}/-{f['deletions']})")
                        if not summary_only:
                            for line in f.get("diff", []):
                                print(f"    {line}", end="")
                    elif f["status"] == "added":
                        print(f"  A {f['file']}")
                    elif f["status"] == "removed":
                        print(f"  D {f['file']}")

    print(f"\n{len(results)} mods: {modified_count} modified, {identical_count} identical, {no_workshop_count} no workshop original")


if __name__ == "__main__":
    main()
