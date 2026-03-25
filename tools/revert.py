"""Revert a mod to its original Steam Workshop version.

When a fix breaks a mod, one command restores the working original.
Backs up the current version before reverting.

Usage:
    python -m tools.revert --mod "AC130_Airstrike_MP"      # Revert one mod
    python -m tools.revert --mod "AC130_Airstrike_MP" --no-backup  # Skip backup
    python -m tools.revert --mod "AC130_Airstrike_MP" --dry-run    # Preview only
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from tools.common import LIVE_MODS_DIR

WORKSHOP_DIR = Path("C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630")
BACKUP_DIR = LIVE_MODS_DIR.parent / "mods_revert_backups"


def find_workshop_id(mod_dir: Path) -> str | None:
    id_path = mod_dir / "id.txt"
    if id_path.exists():
        return id_path.read_text(errors="ignore").strip().split("\n")[0]
    return None


def revert_mod(mod_name: str, dry_run: bool = False, no_backup: bool = False) -> bool:
    # Find the mod
    mod_dir = LIVE_MODS_DIR / mod_name
    if not mod_dir.exists():
        # Try case-insensitive match
        for d in LIVE_MODS_DIR.iterdir():
            if d.name.lower() == mod_name.lower():
                mod_dir = d
                mod_name = d.name
                break
        else:
            print(f"Mod not found: {mod_name}")
            return False

    # Find workshop original
    workshop_id = find_workshop_id(mod_dir)
    if not workshop_id:
        print(f"No id.txt in {mod_name} -- can't find workshop original")
        return False

    workshop_dir = WORKSHOP_DIR / workshop_id
    if not workshop_dir.exists():
        print(f"Workshop original not found: {workshop_id}")
        return False

    if dry_run:
        print(f"Would revert {mod_name} from workshop ID {workshop_id}")
        # Show what files differ
        for lua in mod_dir.rglob("*.lua"):
            rel = lua.relative_to(mod_dir)
            ws_file = workshop_dir / rel
            if ws_file.exists():
                local_data = lua.read_bytes()
                ws_data = ws_file.read_bytes()
                if local_data != ws_data:
                    print(f"  DIFFERS: {rel}")
            else:
                print(f"  LOCAL ONLY: {rel}")
        return True

    # Backup current version
    if not no_backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"{mod_name}_{timestamp}"
        os.makedirs(backup_path, exist_ok=True)
        for lua in mod_dir.rglob("*.lua"):
            rel = lua.relative_to(mod_dir)
            dest = backup_path / rel
            os.makedirs(dest.parent, exist_ok=True)
            shutil.copy2(lua, dest)
        print(f"Backed up to: {backup_path}")

    # Copy workshop files over local (only .lua and .txt, skip preview images)
    reverted = 0
    skip_extensions = {".jpg", ".jpeg", ".png"}
    for ws_file in workshop_dir.rglob("*"):
        if ws_file.is_dir():
            continue
        if ws_file.suffix.lower() in skip_extensions:
            continue
        rel = ws_file.relative_to(workshop_dir)
        dest = mod_dir / rel
        os.makedirs(dest.parent, exist_ok=True)
        shutil.copy2(ws_file, dest)
        reverted += 1

    # Re-create id.txt (workshop copy doesn't have it)
    (mod_dir / "id.txt").write_text(workshop_id + "\n")

    # Fix line endings
    for lua in mod_dir.rglob("*.lua"):
        data = lua.read_bytes()
        fixed = data.replace(b"\r\n", b"\n")
        if fixed != data:
            lua.write_bytes(fixed)

    print(f"Reverted {mod_name} to workshop original ({reverted} files)")
    return True


def main():
    mod_name = None
    dry_run = "--dry-run" in sys.argv
    no_backup = "--no-backup" in sys.argv

    if "--mod" in sys.argv:
        idx = sys.argv.index("--mod")
        if idx + 1 < len(sys.argv):
            mod_name = sys.argv[idx + 1]

    if not mod_name:
        print("Usage: python -m tools.revert --mod \"ModName\" [--dry-run] [--no-backup]")
        sys.exit(1)

    success = revert_mod(mod_name, dry_run=dry_run, no_backup=no_backup)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
