"""For each tool mod with InputPressed("o") options:
1. Gate behind IsPlayerHost() so only host can open options
2. Add registry check for toolconfig.request to open options from central panel
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

# Patterns for the O key options toggle
# Most mods use one of these patterns:
# Pattern A: if isLocal and InputPressed("o") then
# Pattern B: if InputPressed("o") then
# Pattern C: if IsPlayerLocal(p) and InputPressed("o") then
# Pattern D: if toolActive and InputPressed("o") then

def find_tool_id(filepath):
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()
    m = re.search(r'RegisterTool\("([^"]+)"', content)
    if m: return m.group(1)
    m = re.search(r'(?:TOOL_ID|WeaponName)\s*=\s*"([^"]+)"', content)
    if m: return m.group(1)
    m = re.search(r'GetPlayerTool\(\w+\)\s*~=\s*"([^"]+)"', content)
    if m: return m.group(1)
    m = re.search(r'GetString\("game\.player\.tool"\)\s*==\s*"([^"]+)"', content)
    if m: return m.group(1)
    return None

def process_mod(mod_name):
    filepath = os.path.join(MODS_DIR, mod_name, "main.lua")
    if not os.path.isfile(filepath):
        return False

    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    if 'InputPressed("o")' not in content:
        return False

    tool_id = find_tool_id(filepath)
    if not tool_id:
        print(f"  SKIP {mod_name}: no tool ID found")
        return False

    original = content
    changes = []

    # Gate the O key behind IsPlayerHost
    # Handle various patterns

    # Pattern: if isLocal and InputPressed("o") then
    content = re.sub(
        r'if isLocal and InputPressed\("o"\) then',
        'if isLocal and IsPlayerHost() and InputPressed("o") then',
        content
    )

    # Pattern: if InputPressed("o") then (standalone, for options)
    # Be careful not to match ones already gated
    # Only replace if not already preceded by IsPlayerHost
    lines = content.split("\n")
    new_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == 'if InputPressed("o") then' or stripped.startswith('if InputPressed("o") then'):
            # Check if this is about options (look for optionsOpen nearby)
            context = "\n".join(lines[max(0,i-2):min(len(lines),i+5)])
            if "optionsOpen" in context or "Options" in context:
                # Check previous line doesn't already have IsPlayerHost
                prev = lines[i-1].strip() if i > 0 else ""
                if "IsPlayerHost" not in line and "IsPlayerHost" not in prev:
                    line = line.replace('if InputPressed("o") then', 'if IsPlayerHost() and InputPressed("o") then')
                    changes.append("gated O key")
        new_lines.append(line)
    content = "\n".join(new_lines)

    # Pattern: if IsPlayerLocal(p) and InputPressed("o") then
    content = re.sub(
        r'if IsPlayerLocal\(p\) and InputPressed\("o"\) then',
        'if IsPlayerLocal(p) and IsPlayerHost() and InputPressed("o") then',
        content
    )

    # Pattern: if toolActive and InputPressed("o") then
    content = re.sub(
        r'if toolActive and InputPressed\("o"\) then',
        'if toolActive and IsPlayerHost() and InputPressed("o") then',
        content
    )

    # Now add the registry check for toolconfig.request
    # Find the options toggle line and add the registry check before it
    # We need to add it somewhere that runs every tick, inside the tool gate
    # Best place: right after the tool gate check, before other input handling

    # Add registry check for opening options from central panel
    config_check = f'''
    -- Tool Config: open options from centralized panel (host only)
    if IsPlayerHost() and GetString("toolconfig.request") == "{tool_id}" then
        data.optionsOpen = true
        SetString("toolconfig.request", "")
    end
'''

    # Try to insert after common patterns
    # Look for the first occurrence of optionsOpen being set
    if "toolconfig.request" not in content:
        # Find a good insertion point — right before the O key handler
        # Try various option patterns
        for pattern in [
            'if isLocal and IsPlayerHost() and InputPressed("o") then',
            'if IsPlayerHost() and InputPressed("o") then',
            'if IsPlayerLocal(p) and IsPlayerHost() and InputPressed("o") then',
            'if toolActive and IsPlayerHost() and InputPressed("o") then',
        ]:
            if pattern in content:
                content = content.replace(pattern, config_check.rstrip() + "\n\n\t" + pattern)
                changes.append("added toolconfig check")
                break

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        if not changes:
            changes.append("gated O key")
        print(f"  FIXED {mod_name} ({tool_id}): {', '.join(changes)}")
        return True
    else:
        print(f"  NO CHANGE {mod_name}")
        return False

# All mods with options
mods_with_options = [
    "AC130_Airstrike_MP", "AK-47", "AWP", "Airstrike_Arsenal",
    "Artillery_Barrage_RELOADED", "Asteroid_Strike", "Attack_Drone",
    "Bee_Gun", "Black_Hole", "Bombard", "Bouncepad", "C4",
    "Charge_Shotgun", "Control", "Corrupted_Crystal", "Desert_Eagle",
    "Dragonslayer", "Dual_Berettas", "Dual_Miniguns", "Exploding_Star",
    "Explosive_Pack", "Final_Flash", "Fire_Locator", "Gasoline_Flamethrower",
    "Guided_Missile", "HADOUKEN", "Holy_Grenade", "Hook_Shotgun",
    "Hungry_Slimes", "Infinity_Technique", "Ion_Cannon_Beacon",
    "Jackhammer", "Laser_Cutter", "Lava_Gun", "Lightkatana",
    "Lightning_Gun", "Lightsaber", "M1_Garand", "M249",
    "M2A1_Flamethrower", "M4A1", "MEGAGUN", "Magic_Bag", "Magnets",
    "Melt", "Minigun", "Mjolner", "Molotov_Cocktail",
    "Multi_Grenade_Launcher", "Multiple_Grenade_Launcher",
    "Nova_Shotgun", "ODM_Gear", "Omni_Gun", "P90",
    "Remote_Explosives", "Revengeance_Katana", "Rods_from_Gods",
    "SCAR-20", "Scorpion", "Sith_Saber", "Spells", "Swap_Button",
    "Telekinesis", "Tripmine", "Vacuum_Cleaner",
    "Vortexes_and_Tornadoes", "Welding_Tool", "Winch",
    "GYM_Ragdoll",
]

print("=" * 50)
print("Gating options behind host + adding config check")
print("=" * 50)
print()

fixed = 0
for mod in mods_with_options:
    if process_mod(mod):
        fixed += 1

print(f"\nFixed: {fixed}/{len(mods_with_options)}")
