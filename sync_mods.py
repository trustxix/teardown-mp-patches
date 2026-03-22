"""Compare workshop mods vs local mods using layered matching.

Layer 1: id.txt workshop ID match
Layer 2: info.txt name match (exact)
Layer 3: info.txt name fuzzy match (lowercase, strip suffixes like [MP], (Multiplayer))
Layer 4: Folder name similarity

Reports:
- Local mods with NO workshop match (candidates for removal)
- Workshop mods with NO local match (candidates for copying)
"""
import os
import re

WORKSHOP = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1167630"
LOCAL = r"C:\Users\trust\Documents\Teardown\mods"

def read_info_name(path):
    """Read mod name from info.txt"""
    info = os.path.join(path, "info.txt")
    if not os.path.isfile(info):
        return None
    with open(info, "r", errors="ignore") as f:
        for line in f:
            m = re.match(r'^name\s*=\s*(.+)', line.strip())
            if m:
                return m.group(1).strip()
    return None

def normalize_name(name):
    """Normalize mod name for fuzzy matching"""
    if not name:
        return ""
    n = name.lower()
    # Strip common MP suffixes
    n = re.sub(r'\s*\[mp\]', '', n)
    n = re.sub(r'\s*\(multiplayer\)', '', n)
    n = re.sub(r'\s*\[multiplayer\]', '', n)
    n = re.sub(r'\s*- multiplayer', '', n)
    n = re.sub(r'\s*mp$', '', n)
    # Strip special chars
    n = re.sub(r'[^a-z0-9 ]', '', n)
    n = n.strip()
    return n

# ── Build workshop index ──
print("Scanning workshop folder...")
workshop_mods = {}  # wid -> {name, norm_name, path}
for wid in os.listdir(WORKSHOP):
    wpath = os.path.join(WORKSHOP, wid)
    if not os.path.isdir(wpath):
        continue
    name = read_info_name(wpath)
    workshop_mods[wid] = {
        "name": name or f"(unnamed:{wid})",
        "norm": normalize_name(name),
        "path": wpath,
    }

# ── Build local index ──
print("Scanning local mods folder...")
local_mods = {}  # folder_name -> {wid_from_id_txt, name, norm_name, path}
for folder in os.listdir(LOCAL):
    lpath = os.path.join(LOCAL, folder)
    if not os.path.isdir(lpath):
        continue
    if folder == "__test_harness.disabled":
        continue

    # Read id.txt
    wid = None
    id_file = os.path.join(lpath, "id.txt")
    if os.path.isfile(id_file):
        with open(id_file, "r") as f:
            wid = f.readline().strip()

    name = read_info_name(lpath)
    local_mods[folder] = {
        "wid": wid,
        "name": name or folder,
        "norm": normalize_name(name or folder),
        "path": lpath,
    }

# ── Multi-layer matching ──
print(f"\nMatching {len(local_mods)} local mods against {len(workshop_mods)} workshop mods...\n")

# Track which workshop mods are matched
matched_workshop = {}  # wid -> local_folder
matched_local = {}     # folder -> (wid, method)

# Layer 1: id.txt exact match
for folder, lmod in local_mods.items():
    if lmod["wid"] and lmod["wid"] in workshop_mods:
        matched_local[folder] = (lmod["wid"], "L1:id.txt")
        matched_workshop[lmod["wid"]] = folder

# Layer 2: info.txt name exact match
for folder, lmod in local_mods.items():
    if folder in matched_local:
        continue
    for wid, wmod in workshop_mods.items():
        if wid in matched_workshop:
            continue
        if lmod["name"] and wmod["name"] and lmod["name"] == wmod["name"]:
            matched_local[folder] = (wid, "L2:exact_name")
            matched_workshop[wid] = folder
            break

# Layer 3: normalized name match
for folder, lmod in local_mods.items():
    if folder in matched_local:
        continue
    if not lmod["norm"]:
        continue
    for wid, wmod in workshop_mods.items():
        if wid in matched_workshop:
            continue
        if lmod["norm"] and wmod["norm"] and lmod["norm"] == wmod["norm"]:
            matched_local[folder] = (wid, "L3:fuzzy_name")
            matched_workshop[wid] = folder
            break

# Layer 4: folder name matches workshop info.txt name (normalized)
for folder, lmod in local_mods.items():
    if folder in matched_local:
        continue
    folder_norm = normalize_name(folder.replace("_", " "))
    for wid, wmod in workshop_mods.items():
        if wid in matched_workshop:
            continue
        if folder_norm and wmod["norm"] and folder_norm == wmod["norm"]:
            matched_local[folder] = (wid, "L4:folder_to_name")
            matched_workshop[wid] = folder
            break

# ── Report ──
print("=" * 70)
print("SYNC ANALYSIS")
print("=" * 70)

# Unmatched local mods (removal candidates)
unmatched_local = [f for f in local_mods if f not in matched_local]
print(f"\n### LOCAL MODS NOT IN WORKSHOP — candidates for REMOVAL ({len(unmatched_local)}):\n")
if unmatched_local:
    for folder in sorted(unmatched_local):
        lmod = local_mods[folder]
        print(f"  {folder}")
        print(f"    Name: {lmod['name']}")
        print(f"    id.txt: {lmod['wid'] or 'missing'}")
        print()
else:
    print("  None — all local mods matched a workshop entry.\n")

# Unmatched workshop mods (copy candidates)
unmatched_workshop = [w for w in workshop_mods if w not in matched_workshop]
print(f"### WORKSHOP MODS NOT IN LOCAL — candidates for COPY ({len(unmatched_workshop)}):\n")
if unmatched_workshop:
    for wid in sorted(unmatched_workshop):
        wmod = workshop_mods[wid]
        print(f"  {wid}: {wmod['name']}")
else:
    print("  None — all workshop mods already have a local copy.\n")

# Matched with wrong id.txt (should update)
print(f"\n### ID.TXT CORRECTIONS NEEDED:\n")
corrections = 0
for folder, (wid, method) in sorted(matched_local.items()):
    lmod = local_mods[folder]
    if method != "L1:id.txt" and lmod["wid"] != wid:
        print(f"  {folder}: id.txt says {lmod['wid'] or 'missing'}, should be {wid} (matched via {method}: {workshop_mods[wid]['name']})")
        corrections += 1
if corrections == 0:
    print("  None needed.\n")

# Summary
print(f"\n### MATCH SUMMARY:\n")
for method in ["L1:id.txt", "L2:exact_name", "L3:fuzzy_name", "L4:folder_to_name"]:
    count = sum(1 for _, (_, m) in matched_local.items() if m == method)
    if count:
        print(f"  {method}: {count} mods")
print(f"  Unmatched local: {len(unmatched_local)}")
print(f"  Unmatched workshop: {len(unmatched_workshop)}")
print(f"  Total local: {len(local_mods)}, Total workshop: {len(workshop_mods)}")
