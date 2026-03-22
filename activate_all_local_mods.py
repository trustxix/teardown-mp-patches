"""Activate all local mods in every Teardown modlist.

Features:
- Scans Documents/Teardown/mods/ and activates all local mods
- Updates ALL modlists (Default, Host, and any future custom ones from index.xml)
- Registers new mods in master mods.xml
- Cleans stale entries for mods whose folders were deleted
- Keeps max 3 backups, rotates oldest
- Skips if Teardown is running (avoids XML corruption)
- Silent mode (--silent) for Steam pre-launch — no window, no prompts
- Safe to run repeatedly — never duplicates, never removes existing entries
"""
import os
import re
import sys
import shutil
import subprocess
from datetime import datetime

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"
APPDATA = r"C:\Users\trust\AppData\Local\Teardown"
MODLISTS_DIR = os.path.join(APPDATA, "modlists")
MODS_XML = os.path.join(APPDATA, "mods.xml")
LOG_PATH = os.path.join(APPDATA, "mod_activator.log")
MAX_BACKUPS = 3

silent = "--silent" in sys.argv


def log(msg):
    if not silent:
        print(msg)


def write_log(msg):
    """Append to persistent log file."""
    try:
        with open(LOG_PATH, "a") as f:
            f.write(f"{datetime.now().isoformat()} {msg}\n")
    except Exception:
        pass


def is_teardown_running():
    """Check if teardown.exe is currently running."""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq teardown.exe", "/NH"],
            capture_output=True, text=True, timeout=5
        )
        return "teardown.exe" in result.stdout.lower()
    except Exception:
        return False


def get_local_mod_ids():
    """Scan local mods folder and generate Teardown mod IDs."""
    mod_ids = []
    for folder in sorted(os.listdir(MODS_DIR)):
        path = os.path.join(MODS_DIR, folder)
        if not os.path.isdir(path):
            continue
        if folder.startswith("__") or folder.startswith("."):
            continue
        mod_id = "local-" + folder.lower().replace("_", "-").replace(" ", "-")
        mod_id = re.sub(r'-+', '-', mod_id).strip('-')
        mod_ids.append((folder, mod_id))
    return mod_ids


def get_existing_folder_ids():
    """Build set of mod IDs for all existing local folders."""
    ids = set()
    for folder in os.listdir(MODS_DIR):
        if not os.path.isdir(os.path.join(MODS_DIR, folder)):
            continue
        mid = "local-" + folder.lower().replace("_", "-").replace(" ", "-")
        mid = re.sub(r'-+', '-', mid).strip('-')
        ids.add(mid)
    return ids


def rotate_backups():
    """Keep only MAX_BACKUPS backup folders, delete oldest."""
    backups = sorted([
        d for d in os.listdir(MODLISTS_DIR)
        if d.startswith("backup_") and os.path.isdir(os.path.join(MODLISTS_DIR, d))
    ])
    while len(backups) >= MAX_BACKUPS:
        oldest = backups.pop(0)
        shutil.rmtree(os.path.join(MODLISTS_DIR, oldest), ignore_errors=True)


def backup():
    """Create a timestamped backup of modlist XMLs."""
    rotate_backups()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(MODLISTS_DIR, f"backup_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    for f in os.listdir(MODLISTS_DIR):
        src = os.path.join(MODLISTS_DIR, f)
        if os.path.isfile(src) and f.endswith(".xml"):
            shutil.copy2(src, os.path.join(backup_dir, f))
    if os.path.isfile(MODS_XML):
        shutil.copy2(MODS_XML, os.path.join(backup_dir, "mods.xml"))
    return backup_dir


def discover_modlists():
    """Find all modlist XML files from index.xml + fallback scan."""
    modlist_files = []
    seen_paths = set()

    # Read index.xml for named modlists
    index_path = os.path.join(MODLISTS_DIR, "index.xml")
    if os.path.isfile(index_path):
        with open(index_path, "r", errors="ignore") as f:
            index_content = f.read()
        for m in re.finditer(r'<modlist id="(\d+)">\s*<name>([^<]+)</name>', index_content):
            ml_id = m.group(1)
            ml_name = m.group(2)
            ml_path = os.path.join(MODLISTS_DIR, f"{ml_id}.xml")
            if os.path.isfile(ml_path):
                modlist_files.append((ml_path, ml_name))
                seen_paths.add(ml_path)

    # Fallback: catch any numbered XML files not in index
    for f in os.listdir(MODLISTS_DIR):
        if re.match(r'^\d+\.xml$', f):
            fpath = os.path.join(MODLISTS_DIR, f)
            if fpath not in seen_paths:
                modlist_files.append((fpath, f"Unknown ({f})"))

    return modlist_files


def update_modlist(filepath, mod_ids_to_add):
    """Add missing local mod IDs to a modlist XML file."""
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    existing = set(re.findall(r'<mod id="([^"]+)"', content))
    to_add = [(folder, mid) for folder, mid in mod_ids_to_add if mid not in existing]

    if not to_add:
        return 0

    new_entries = "\n".join(f'\t\t<mod id="{mid}"/>' for _, mid in to_add)
    content = content.replace("</mods>", new_entries + "\n\t</mods>")

    with open(filepath, "w") as f:
        f.write(content)
    return len(to_add)


def update_mods_xml(mod_ids_to_add):
    """Ensure all local mods are registered in master mods.xml."""
    if not os.path.isfile(MODS_XML):
        return 0

    with open(MODS_XML, "r", errors="ignore") as f:
        content = f.read()

    existing = set(re.findall(r'<mod id="([^"]+)"', content))
    to_add = [(folder, mid) for folder, mid in mod_ids_to_add if mid not in existing]

    if not to_add:
        return 0

    new_entries = "\n".join(f'\t<mod id="{mid}" shown="false"/>' for _, mid in to_add)
    content = content.replace("</mods>", new_entries + "\n</mods>")

    with open(MODS_XML, "w") as f:
        f.write(content)
    return len(to_add)


def remove_stale_entries():
    """Remove modlist entries for local mods whose folders no longer exist."""
    existing_ids = get_existing_folder_ids()
    total_removed = 0

    # Clean each modlist
    for ml_file in os.listdir(MODLISTS_DIR):
        if not ml_file.endswith(".xml") or ml_file == "index.xml":
            continue
        filepath = os.path.join(MODLISTS_DIR, ml_file)
        with open(filepath, "r", errors="ignore") as f:
            lines = f.readlines()

        new_lines = []
        removed_here = 0
        for line in lines:
            m = re.search(r'<mod id="(local-[^"]+)"', line)
            if m and m.group(1) not in existing_ids:
                removed_here += 1
            else:
                new_lines.append(line)

        if removed_here > 0:
            with open(filepath, "w") as f:
                f.writelines(new_lines)
            total_removed += removed_here

    # Clean mods.xml
    if os.path.isfile(MODS_XML):
        with open(MODS_XML, "r", errors="ignore") as f:
            lines = f.readlines()

        new_lines = []
        removed_here = 0
        for line in lines:
            m = re.search(r'<mod id="(local-[^"]+)"', line)
            if m and m.group(1) not in existing_ids:
                removed_here += 1
            else:
                new_lines.append(line)

        if removed_here > 0:
            with open(MODS_XML, "w") as f:
                f.writelines(new_lines)
            total_removed += removed_here

    return total_removed


def main():
    # Check if Teardown is running
    if is_teardown_running():
        msg = "Teardown is running — skipping mod activation to avoid XML corruption"
        log(f"  {msg}")
        write_log(f"SKIPPED: {msg}")
        return

    if not silent:
        print("=" * 50)
        print("  Teardown — Activate All Local Mods")
        print("=" * 50)
        print()

    # Backup
    backup_dir = backup()
    log(f"  Backup: {backup_dir}")

    # Get all local mod IDs
    mod_ids = get_local_mod_ids()
    log(f"  Found {len(mod_ids)} local mods")

    # Remove stale entries for deleted mods
    removed = remove_stale_entries()
    if removed:
        log(f"  Cleaned {removed} stale entries")

    # Discover and update all modlists
    modlist_files = discover_modlists()
    total_added = 0
    for filepath, name in modlist_files:
        added = update_modlist(filepath, mod_ids)
        total_added += added
        log(f"  {name}: +{added} mods")

    # Update master mods.xml
    registered = update_mods_xml(mod_ids)
    log(f"  mods.xml: +{registered} registered")

    if not silent:
        print()
        print(f"  Total: {total_added} activations, {registered} registrations")
        print("  Done! Launch Teardown.")

    # Always log when changes were made
    if total_added > 0 or registered > 0 or removed > 0:
        write_log(f"activated={total_added} registered={registered} removed={removed} mods={len(mod_ids)}")


if __name__ == "__main__":
    main()
