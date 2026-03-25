"""Push mod changes from Documents to game install dir.

Documents is the edit/publish source. Game install is where MP loads from.
This copies changed files from Documents -> game install to keep them in sync.

Usage:
    python -m tools.push                    # Push all changed mods
    python -m tools.push --mod "AC130"      # Push one mod
    python -m tools.push --all              # Force push all mods
"""
import os
import sys
import shutil
import filecmp
from pathlib import Path

DOCS_MODS = Path("C:/Users/trust/Documents/Teardown/mods")
GAME_MODS = Path("C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods")

SKIP_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def push_mod(mod_name, force=False):
    src = DOCS_MODS / mod_name
    dst = GAME_MODS / mod_name

    if not src.exists():
        print(f"  {mod_name}: not in Documents, skipping")
        return 0

    copied = 0
    for src_file in src.rglob("*"):
        if src_file.is_dir():
            continue
        if src_file.suffix.lower() in SKIP_EXTENSIONS:
            continue

        rel = src_file.relative_to(src)
        dst_file = dst / rel

        if not force and dst_file.exists():
            if filecmp.cmp(str(src_file), str(dst_file), shallow=False):
                continue

        os.makedirs(dst_file.parent, exist_ok=True)
        shutil.copy2(src_file, dst_file)
        copied += 1

    return copied


def main():
    mod_filter = None
    force_all = "--all" in sys.argv

    if "--mod" in sys.argv:
        idx = sys.argv.index("--mod")
        if idx + 1 < len(sys.argv):
            mod_filter = sys.argv[idx + 1]

    total_copied = 0
    mods_changed = 0

    for d in sorted(DOCS_MODS.iterdir()):
        if not d.is_dir():
            continue
        if mod_filter and mod_filter.lower() not in d.name.lower():
            continue

        copied = push_mod(d.name, force=force_all)
        if copied > 0:
            print(f"  {d.name}: {copied} files pushed", flush=True)
            total_copied += copied
            mods_changed += 1

    if total_copied == 0:
        print("Everything in sync.")
    else:
        print(f"\nPushed {total_copied} files across {mods_changed} mods")


if __name__ == "__main__":
    main()
