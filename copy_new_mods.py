"""Copy new workshop mods into local mods folder.
- Only copies mods not already present locally
- Never overwrites existing local mods
- Creates id.txt with workshop ID
- Names folder from info.txt name (sanitized)
"""
import os
import re
import shutil

WORKSHOP = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1167630"
LOCAL = r"C:\Users\trust\Documents\Teardown\mods"

def read_info_name(path):
    info = os.path.join(path, "info.txt")
    if not os.path.isfile(info):
        return None
    with open(info, "r", errors="ignore") as f:
        for line in f:
            m = re.match(r'^name\s*=\s*(.+)', line.strip())
            if m:
                return m.group(1).strip()
    return None

def sanitize_folder_name(name):
    """Convert mod name to safe folder name"""
    # Replace special chars with underscores
    s = re.sub(r'[<>:"/\\|?*\[\]()]', '', name)
    s = re.sub(r'\s+', '_', s.strip())
    s = re.sub(r'_+', '_', s)
    s = s.strip('_.')
    return s

# Build set of workshop IDs already in local
local_wids = set()
for folder in os.listdir(LOCAL):
    id_file = os.path.join(LOCAL, folder, "id.txt")
    if os.path.isfile(id_file):
        with open(id_file) as f:
            wid = f.readline().strip()
            if wid:
                local_wids.add(wid)

# Also build set of local folder names (lowercase) to avoid collisions
local_folders = set(f.lower() for f in os.listdir(LOCAL))

copied = []
skipped = []
errors = []

for wid in sorted(os.listdir(WORKSHOP)):
    wpath = os.path.join(WORKSHOP, wid)
    if not os.path.isdir(wpath):
        continue
    if wid in local_wids:
        continue  # Already have this mod locally

    name = read_info_name(wpath) or f"mod_{wid}"
    folder_name = sanitize_folder_name(name)

    # Handle name collision
    if folder_name.lower() in local_folders:
        folder_name = f"{folder_name}_{wid}"

    dest = os.path.join(LOCAL, folder_name)
    if os.path.exists(dest):
        skipped.append((wid, name, "destination exists"))
        continue

    try:
        shutil.copytree(wpath, dest)
        # Create/update id.txt
        id_file = os.path.join(dest, "id.txt")
        with open(id_file, "w") as f:
            f.write(f"{wid}\n")
        copied.append((wid, name, folder_name))
        local_folders.add(folder_name.lower())
    except Exception as e:
        errors.append((wid, name, str(e)))

print(f"Copied: {len(copied)}")
print(f"Skipped: {len(skipped)}")
print(f"Errors: {len(errors)}")
print()

if copied:
    print("=== COPIED ===")
    for wid, name, folder in copied:
        print(f"  {wid} -> {folder} ({name})")
    print()

if skipped:
    print("=== SKIPPED ===")
    for wid, name, reason in skipped:
        print(f"  {wid}: {name} ({reason})")
    print()

if errors:
    print("=== ERRORS ===")
    for wid, name, err in errors:
        print(f"  {wid}: {name} -> {err}")
