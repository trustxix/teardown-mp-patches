"""Add tool config registry check to all mods with options menus.

For each mod:
1. Gate InputPressed("o") behind IsPlayerHost()
2. Add registry key check to open options from centralized panel
3. Add "O - Options" to keybind hints for host only
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

# Map of mod folder -> tool ID (from RegisterTool or GetPlayerTool checks)
# We'll auto-detect these
def find_tool_id(mod_path):
    """Find the tool ID for a mod."""
    main = os.path.join(mod_path, "main.lua")
    if not os.path.isfile(main):
        return None
    with open(main, "r", errors="ignore") as f:
        content = f.read()
    # Check RegisterTool
    m = re.search(r'RegisterTool\("([^"]+)"', content)
    if m:
        return m.group(1)
    # Check TOOL_ID or WeaponName
    m = re.search(r'(?:TOOL_ID|WeaponName)\s*=\s*"([^"]+)"', content)
    if m:
        return m.group(1)
    # Check GetPlayerTool comparison
    m = re.search(r'GetPlayerTool\(\w+\)\s*[~=]=\s*"([^"]+)"', content)
    if m:
        return m.group(1)
    m = re.search(r'GetString\("game\.player\.tool"\)\s*==\s*"([^"]+)"', content)
    if m:
        return m.group(1)
    return None

def find_tool_name(mod_path):
    """Find display name from info.txt."""
    info = os.path.join(mod_path, "info.txt")
    if not os.path.isfile(info):
        return None
    with open(info, "r", errors="ignore") as f:
        for line in f:
            m = re.match(r'^name\s*=\s*(.+)', line.strip())
            if m:
                return m.group(1).strip()
    return None

# Find all mods with InputPressed("o") for options
results = []
for mod in sorted(os.listdir(MODS_DIR)):
    main = os.path.join(MODS_DIR, mod, "main.lua")
    if not os.path.isfile(main):
        continue
    with open(main, "r", errors="ignore") as f:
        content = f.read()
    if 'InputPressed("o")' not in content:
        continue
    if 'optionsOpen' not in content and 'Options' not in content:
        continue

    tool_id = find_tool_id(os.path.join(MODS_DIR, mod))
    tool_name = find_tool_name(os.path.join(MODS_DIR, mod))

    if tool_id:
        results.append((mod, tool_id, tool_name or mod))

print(f"Found {len(results)} configurable tools:\n")
for mod, tid, name in results:
    print(f'  {{id="{tid}", name="{name}", folder="{mod}"}},')
