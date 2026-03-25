"""Sync tool settings via shared table.

For each mod:
1. Find all SetBool/SetFloat/SetInt("savegame.mod.X", value) calls in options panels
2. Add shared sync: when writing to savegame.mod.*, also write to shared.settings.*
3. In server.init, initialize shared.settings from savegame.mod.*
4. In client.draw, read from shared.settings.* instead of savegame.mod.*
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

def find_settings(filepath):
    """Find all savegame.mod.* keys used in a mod."""
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    # Find all savegame.mod.* key patterns
    settings = set()
    for m in re.finditer(r'(?:Get|Set)(?:Bool|Float|Int|String)\("(savegame\.mod\.[^"]+)"', content):
        settings.add(m.group(1))
    return sorted(settings)

def find_tool_id(filepath):
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()
    m = re.search(r'RegisterTool\("([^"]+)"', content)
    if m: return m.group(1)
    m = re.search(r'(?:TOOL_ID|WeaponName)\s*=\s*"([^"]+)"', content)
    if m: return m.group(1)
    return None

# Scan all mods
print("=== Settings per mod ===\n")
for mod in sorted(os.listdir(MODS_DIR)):
    main = os.path.join(MODS_DIR, mod, "main.lua")
    if not os.path.isfile(main):
        continue
    settings = find_settings(main)
    if not settings:
        continue
    tool_id = find_tool_id(main)
    print(f"{mod} (tool={tool_id}):")
    for s in settings:
        # Determine type
        with open(main, "r", errors="ignore") as f:
            content = f.read()
        if f'GetBool("{s}")' in content:
            stype = "bool"
        elif f'GetFloat("{s}")' in content:
            stype = "float"
        elif f'GetInt("{s}")' in content:
            stype = "int"
        else:
            stype = "?"
        short = s.replace("savegame.mod.", "")
        print(f"  {short} ({stype})")
    print()
