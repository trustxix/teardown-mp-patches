"""Session overview -- what changed since last commit, quick orientation.

Run at the start of every session to see what's been modified.

Usage:
    python -m tools.session                # Full overview
    python -m tools.session --changes      # Only show changed files
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from tools.common import LIVE_MODS_DIR
from tools.classify import BUILTIN_MODS


def get_git_changes(project_dir: str) -> dict:
    """Get git status and recent commits."""
    result = {"staged": [], "unstaged": [], "untracked": [], "recent_commits": []}

    try:
        # Staged changes
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=project_dir
        )
        result["staged"] = [l for l in out.stdout.strip().splitlines() if l]

        # Unstaged changes
        out = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True, cwd=project_dir
        )
        result["unstaged"] = [l for l in out.stdout.strip().splitlines() if l]

        # Untracked
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=project_dir
        )
        result["untracked"] = [l[3:] for l in out.stdout.strip().splitlines() if l.startswith("??")]

        # Recent commits
        out = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            capture_output=True, text=True, cwd=project_dir
        )
        result["recent_commits"] = out.stdout.strip().splitlines()

    except Exception:
        pass

    return result


def get_mod_changes() -> list[dict]:
    """Find mods that were modified more recently than their id.txt."""
    changed = []
    for d in sorted(LIVE_MODS_DIR.iterdir()):
        if not d.is_dir() or d.name.lower() in BUILTIN_MODS or d.name.startswith("__"):
            continue
        if not (d / "id.txt").exists():
            continue

        # Check if any .lua file is newer than id.txt
        id_mtime = (d / "id.txt").stat().st_mtime
        newest_lua = 0
        newest_file = ""
        for lua in d.rglob("*.lua"):
            mtime = lua.stat().st_mtime
            if mtime > newest_lua:
                newest_lua = mtime
                newest_file = str(lua.relative_to(d))

        if newest_lua > id_mtime:
            age_hours = (datetime.now().timestamp() - newest_lua) / 3600
            changed.append({
                "mod": d.name,
                "file": newest_file,
                "age_hours": age_hours,
            })

    return changed


def main():
    project_dir = str(Path(__file__).parent.parent)
    changes_only = "--changes" in sys.argv

    print("SESSION OVERVIEW")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Git status
    git = get_git_changes(project_dir)
    total_git = len(git["staged"]) + len(git["unstaged"]) + len(git["untracked"])

    if not changes_only:
        print("Recent commits:")
        for c in git["recent_commits"][:5]:
            print(f"  {c}")
        print()

    if total_git > 0:
        print(f"Git: {len(git['staged'])} staged, {len(git['unstaged'])} unstaged, {len(git['untracked'])} untracked")
        for f in git["staged"][:5]:
            print(f"  S {f}")
        for f in git["unstaged"][:5]:
            print(f"  M {f}")
        for f in git["untracked"][:5]:
            print(f"  ? {f}")
        if total_git > 15:
            print(f"  ... and {total_git - 15} more")
    else:
        print("Git: clean")
    print()

    # Modified mods
    mod_changes = get_mod_changes()
    if mod_changes:
        print(f"Recently modified mods ({len(mod_changes)}):")
        for mc in sorted(mod_changes, key=lambda x: x["age_hours"]):
            if mc["age_hours"] < 1:
                age_str = f"{int(mc['age_hours'] * 60)}m ago"
            elif mc["age_hours"] < 24:
                age_str = f"{mc['age_hours']:.1f}h ago"
            else:
                age_str = f"{mc['age_hours']/24:.1f}d ago"
            print(f"  {mc['mod']:<40} {mc['file']:<20} {age_str}")
    else:
        print("No recently modified mods")
    print()

    if not changes_only:
        print("Quick commands:")
        print("  python -m tools.status          # Full project status")
        print("  python -m tools.health          # Per-mod health dashboard")
        print("  python -m tools.classify        # Mod categories")
        print("  python -m tools.diff --summary  # Changes vs workshop")
        print("  python -m tools.pack            # Build mod pack for friends")
        print("  python -m tools.revert --mod X  # Revert mod to workshop original")


if __name__ == "__main__":
    main()
