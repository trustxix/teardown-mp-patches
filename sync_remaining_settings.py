"""Sync remaining complex tool settings."""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

def detect_type(key, content):
    if f'GetBool("{key}")' in content: return "Bool"
    if f'GetFloat("{key}")' in content: return "Float"
    if f'GetInt("{key}")' in content: return "Int"
    if f'SetBool("{key}"' in content: return "Bool"
    if f'SetFloat("{key}"' in content: return "Float"
    if f'SetInt("{key}"' in content: return "Int"
    return None

def process_mod(mod_name):
    filepath = os.path.join(MODS_DIR, mod_name, "main.lua")
    if not os.path.isfile(filepath):
        print(f"  SKIP {mod_name}")
        return False

    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    # Auto-detect all savegame.mod.* settings and their types
    all_keys = set()
    for m in re.finditer(r'(?:Get|Set)(Bool|Float|Int)\("(savegame\.mod\.[^"]+)"', content):
        stype = m.group(1)
        key = m.group(2)
        all_keys.add((key, stype))

    # Filter out keys that are just version/init markers
    settings = [(k, t) for k, t in sorted(all_keys)
                if not any(skip in k for skip in ['Version', 'version', 'verison', 'initialized'])]

    if not settings:
        print(f"  SKIP {mod_name}: no settings found")
        return False

    original = content

    # 1. Init shared.toolSettings in server.init
    if "shared.toolSettings" not in content:
        init_match = re.search(r'(function server\.init\(\)[^\n]*\n)', content)
        if init_match:
            init_block = init_match.group(0)
            init_code = init_block + '\tshared.toolSettings = shared.toolSettings or {}\n'
            for key, stype in settings:
                short = key.replace("savegame.mod.", "")
                init_code += f'\tshared.toolSettings["{short}"] = Get{stype}("{key}")\n'
            content = content.replace(init_block, init_code)

    # 2. After each Set*(key, value), add shared sync
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line)
        for key, stype in settings:
            short = key.replace("savegame.mod.", "")
            set_call = f'Set{stype}("{key}",'
            if set_call in line and "shared.toolSettings" not in line:
                indent = line[:len(line) - len(line.lstrip())]
                m = re.search(rf'Set{stype}\("{re.escape(key)}",\s*(.+?)\)', line)
                if m:
                    val = m.group(1).strip()
                    new_lines.append(f'{indent}shared.toolSettings["{short}"] = {val}')
    content = "\n".join(new_lines)

    # 3. In client.draw, replace Get* with shared reads
    draw_match = re.search(r'function (?:client\.)?draw\(\)', content)
    if draw_match:
        draw_start = draw_match.start()
        before = content[:draw_start]
        after = content[draw_start:]
        for key, stype in settings:
            short = key.replace("savegame.mod.", "")
            old = f'Get{stype}("{key}")'
            new = f'(shared.toolSettings and shared.toolSettings["{short}"] or Get{stype}("{key}"))'
            after = after.replace(old, new)
        content = before + after

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  FIXED {mod_name}: {len(settings)} settings synced")
        return True
    print(f"  NO CHANGE {mod_name}")
    return False

# Remaining mods not yet handled
remaining = [
    "Black_Hole", "Bomb_Attack", "Bouncepad", "Corrupted_Crystal",
    "Dual_Miniguns", "Final_Flash", "High_Tech_Drone",
    "Hungry_Slimes", "Melt", "Omni_Gun",
    "Vacuum_Cleaner", "Vortexes_and_Tornadoes",
    "Control", "Bee_Gun", "Bombard", "Dragonslayer",
    "Fire_Locator", "Guided_Missile", "Holy_Grenade",
    "Welding_Tool", "ODM_Gear",
]

print("=" * 50)
print("Syncing remaining tool settings")
print("=" * 50)
print()

fixed = 0
for mod in remaining:
    if process_mod(mod):
        fixed += 1

print(f"\nFixed: {fixed}/{len(remaining)}")
