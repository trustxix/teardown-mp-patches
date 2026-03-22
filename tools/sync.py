"""Mod sync tool — keeps local mods in sync with Steam Workshop subscriptions.

Source of truth: Steam Workshop folder (what the user is subscribed to).
Target: Documents/Teardown/mods/ (where the game loads mods from).

Usage:
    python -m tools.sync              # dry-run: show what would change
    python -m tools.sync --apply      # actually sync
    python -m tools.sync --status     # just show counts, no details
"""
import argparse
import os
import re
import shutil
import sys

WORKSHOP_DIR = "C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630"
LOCAL_MODS_DIR = "C:/Users/trust/Documents/Teardown/mods"
REMOVED_DIR = "C:/Users/trust/Documents/Teardown/mods_REMOVED"
# Files that must NEVER be copied (cause engine crashes)
SKIP_FILES = {"preview.jpg", "preview.png", "preview.jpeg"}


def sanitize_mod_name(name: str) -> str:
    """Convert info.txt name to a safe directory name."""
    # Replace spaces and problematic chars with underscores
    name = re.sub(r"[^\w\s\-']", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    # Collapse multiple underscores
    name = re.sub(r"_+", "_", name)
    return name or "Unknown_Mod"


def read_info_txt(path: str) -> dict:
    """Parse info.txt key=value pairs."""
    info = {}
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, _, val = line.partition("=")
                    info[key.strip()] = val.strip()
    except FileNotFoundError:
        pass
    return info


def get_workshop_mods() -> dict:
    """Return {workshop_id: folder_path} for all subscribed mods."""
    mods = {}
    if not os.path.isdir(WORKSHOP_DIR):
        return mods
    for entry in os.listdir(WORKSHOP_DIR):
        full = os.path.join(WORKSHOP_DIR, entry)
        if os.path.isdir(full) and entry.isdigit():
            mods[entry] = full
    return mods


def get_local_mods() -> dict:
    """Return {workshop_id: (mod_name, folder_path)} for all local mods with id.txt."""
    mods = {}
    if not os.path.isdir(LOCAL_MODS_DIR):
        return mods
    for entry in os.listdir(LOCAL_MODS_DIR):
        full = os.path.join(LOCAL_MODS_DIR, entry)
        id_file = os.path.join(full, "id.txt")
        if os.path.isdir(full) and os.path.isfile(id_file):
            try:
                with open(id_file, "r") as f:
                    workshop_id = f.readline().strip()
                if workshop_id.isdigit():
                    mods[workshop_id] = (entry, full)
            except (IOError, OSError):
                pass
    return mods


def copy_mod(workshop_id: str, workshop_path: str) -> str:
    """Copy a workshop mod to local mods directory. Returns the new folder name."""
    # Read mod name from info.txt
    info = read_info_txt(os.path.join(workshop_path, "info.txt"))
    raw_name = info.get("name", f"Mod_{workshop_id}")
    mod_name = sanitize_mod_name(raw_name)

    # Ensure unique name
    dest = os.path.join(LOCAL_MODS_DIR, mod_name)
    if os.path.exists(dest):
        mod_name = f"{mod_name}_{workshop_id}"
        dest = os.path.join(LOCAL_MODS_DIR, mod_name)

    # Copy everything except preview images
    os.makedirs(dest, exist_ok=True)
    for item in os.listdir(workshop_path):
        if item.lower() in SKIP_FILES:
            continue
        src = os.path.join(workshop_path, item)
        dst = os.path.join(dest, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    # Ensure id.txt exists with workshop ID
    id_file = os.path.join(dest, "id.txt")
    if not os.path.isfile(id_file):
        with open(id_file, "w") as f:
            f.write(workshop_id + "\n")

    return mod_name


def remove_mod(mod_name: str, mod_path: str, workshop_id: str):
    """Move a local mod to mods_REMOVED/ (safety net)."""
    os.makedirs(REMOVED_DIR, exist_ok=True)
    dest = os.path.join(REMOVED_DIR, mod_name)
    # If already exists in removed dir, add ID suffix
    if os.path.exists(dest):
        dest = f"{dest}_{workshop_id}"
    shutil.move(mod_path, dest)


def update_master_mod_list(removed_names: list):
    """Remove entries from MASTER_MOD_LIST.md for removed mods."""
    list_path = os.path.join(os.path.dirname(__file__), "..", "MASTER_MOD_LIST.md")
    list_path = os.path.normpath(list_path)
    if not os.path.isfile(list_path):
        return
    try:
        with open(list_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            # Skip lines that mention removed mod names
            if any(name in line for name in removed_names):
                continue
            new_lines.append(line)
        with open(list_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except (IOError, OSError):
        pass


def main():
    parser = argparse.ArgumentParser(description="Sync local mods with Steam Workshop subscriptions")
    parser.add_argument("--apply", action="store_true", help="Actually perform sync (default is dry-run)")
    parser.add_argument("--status", action="store_true", help="Just show sync status counts")
    args = parser.parse_args()

    workshop = get_workshop_mods()
    local = get_local_mods()

    workshop_ids = set(workshop.keys())
    local_ids = set(local.keys())

    new_ids = sorted(workshop_ids - local_ids)
    removed_ids = sorted(local_ids - workshop_ids)
    in_sync = sorted(workshop_ids & local_ids)

    # Gather info for display
    new_mods = []
    for wid in new_ids:
        info = read_info_txt(os.path.join(workshop[wid], "info.txt"))
        name = info.get("name", f"Unknown ({wid})")
        new_mods.append((wid, name))

    removed_mods = []
    for wid in removed_ids:
        mod_name, mod_path = local[wid]
        removed_mods.append((wid, mod_name, mod_path))

    # --- Status mode ---
    if args.status:
        print(f"Workshop: {len(workshop_ids)} subscribed")
        print(f"Local:    {len(local_ids)} installed (with id.txt)")
        print(f"In sync:  {len(in_sync)}")
        if new_mods:
            print(f"NEW:      {len(new_mods)} (in workshop, not local)")
        if removed_mods:
            print(f"REMOVED:  {len(removed_mods)} (in local, not workshop)")
        if not new_mods and not removed_mods:
            print("Status:   ALL SYNCED")
        sys.exit(0 if not new_mods and not removed_mods else 1)

    # --- Dry-run / apply mode ---
    dry_run = not args.apply

    if not new_mods and not removed_mods:
        print(f"All synced. {len(in_sync)} mods in both workshop and local.")
        sys.exit(0)

    print("MOD SYNC" + (" (DRY RUN)" if dry_run else ""))
    print("=" * 50)

    if new_mods:
        print(f"\n  NEW — {len(new_mods)} mods to install:")
        for wid, name in new_mods:
            print(f"    + {name} ({wid})")
            if not dry_run:
                folder = copy_mod(wid, workshop[wid])
                print(f"      → Copied to {folder}/")

    if removed_mods:
        print(f"\n  REMOVED — {len(removed_mods)} mods to uninstall:")
        for wid, mod_name, mod_path in removed_mods:
            print(f"    - {mod_name} ({wid})")
            if not dry_run:
                remove_mod(mod_name, mod_path, wid)
                print(f"      → Moved to mods_REMOVED/{mod_name}")

        if not dry_run:
            removed_names = [m[1] for m in removed_mods]
            update_master_mod_list(removed_names)
            if removed_names:
                print(f"\n  Updated MASTER_MOD_LIST.md (removed {len(removed_names)} entries)")

    print(f"\n  Summary: {len(in_sync)} synced, {len(new_mods)} new, {len(removed_mods)} removed")

    if dry_run:
        print("\n  Run with --apply to execute these changes.")


if __name__ == "__main__":
    main()
