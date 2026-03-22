"""Add shared table sync for simple gun mods that only use unlimitedammo/realisticdamage.

For each mod:
1. In server.init/server.tick PlayersAdded: init shared.toolSettings
2. Where SetBool("savegame.mod.X") is called: also set shared.toolSettings.X
3. In client.draw: read from shared.toolSettings instead of savegame.mod
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

def process_simple_mod(mod_name, settings_keys):
    """Process a mod with simple bool settings."""
    filepath = os.path.join(MODS_DIR, mod_name, "main.lua")
    if not os.path.isfile(filepath):
        print(f"  SKIP {mod_name}: not found")
        return False

    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    original = content
    changes = []

    # 1. Add shared.toolSettings init in server.init or first PlayersAdded
    if "shared.toolSettings" not in content:
        # Find server.init or server.tick with PlayersAdded
        init_pattern = re.search(r'(function server\.init\(\)[^\n]*\n)', content)
        if init_pattern:
            init_line = init_pattern.group(0)
            init_code = init_line
            for key in settings_keys:
                short = key.replace("savegame.mod.", "")
                getter = "GetBool" if "ammo" in key or "damage" in key or "recoil" in key or "fire" in key or "debris" in key else "GetBool"
                init_code += f'\tshared.toolSettings = shared.toolSettings or {{}}\n'
                init_code += f'\tshared.toolSettings["{short}"] = {getter}("{key}")\n'
                break  # Only need the init once
            for key in settings_keys:
                short = key.replace("savegame.mod.", "")
                if f'shared.toolSettings["{short}"]' not in init_code:
                    init_code += f'\tshared.toolSettings["{short}"] = GetBool("{key}")\n'
            content = content.replace(init_line, init_code)
            changes.append("added shared.toolSettings init")

    # 2. After each SetBool("savegame.mod.X", value), add shared sync
    for key in settings_keys:
        short = key.replace("savegame.mod.", "")
        # Pattern: SetBool("savegame.mod.X", not X) or SetBool("savegame.mod.X", value)
        set_pattern = f'SetBool("{key}",'
        if set_pattern in content and f'shared.toolSettings["{short}"]' not in content.split(set_pattern, 1)[1][:200]:
            # Add shared sync after each SetBool
            content = content.replace(
                set_pattern,
                set_pattern
            )
            # More targeted: find lines with SetBool and add shared sync after
            lines = content.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if set_pattern in line and "shared.toolSettings" not in line:
                    indent = line[:len(line) - len(line.lstrip())]
                    # Extract the value being set
                    m = re.search(rf'SetBool\("{re.escape(key)}",\s*(.+?)\)', line)
                    if m:
                        val = m.group(1).strip()
                        new_lines.append(f'{indent}shared.toolSettings["{short}"] = {val}')
                        changes.append(f"sync {short}")
            content = "\n".join(new_lines)

    # 3. In client.draw, replace GetBool("savegame.mod.X") with shared reads
    for key in settings_keys:
        short = key.replace("savegame.mod.", "")
        # Only replace in draw context — look for GetBool after client.draw or draw function
        # Simple approach: replace all GetBool("savegame.mod.X") with shared read
        # But we need to keep the server reads using savegame.mod (they're authoritative)
        # So only replace in lines that are clearly in draw/display context
        # Safest: replace the local variable assignment in draw
        draw_pattern = f'GetBool("{key}")'
        shared_read = f'(shared.toolSettings and shared.toolSettings["{short}"] or GetBool("{key}"))'

        # Find the client.draw function and replace within it
        draw_match = re.search(r'function (?:client\.)?draw\(\)', content)
        if draw_match:
            draw_start = draw_match.start()
            # Replace GetBool only after the draw function starts
            before_draw = content[:draw_start]
            after_draw = content[draw_start:]
            after_draw = after_draw.replace(draw_pattern, shared_read)
            content = before_draw + after_draw
            if content != original:
                changes.append(f"client reads shared.{short}")

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        unique_changes = list(dict.fromkeys(changes))
        print(f"  FIXED {mod_name}: {', '.join(unique_changes)}")
        return True
    else:
        print(f"  NO CHANGE {mod_name}")
        return False

# Simple mods with just unlimitedammo
simple_unlimited = [
    "AWP", "Airstrike_Arsenal", "Asteroid_Strike", "Attack_Drone",
    "Charge_Shotgun", "Desert_Eagle", "Dragonslayer", "Dual_Berettas",
    "HADOUKEN", "Lightkatana", "Lightsaber", "M249",
    "M2A1_Flamethrower", "M4A1", "MEGAGUN", "Multi_Grenade_Launcher",
    "Nova_Shotgun", "P90", "Remote_Explosives", "Rods_from_Gods", "SCAR-20",
]

# Mods with unlimitedammo + realisticdamage
unlimited_realistic = [
    "AK-47", "M1_Garand",
]

# Mods with norecoil
norecoil_mods = [
    "Dual_Miniguns", "Minigun",
]

# Mods with custom bool settings
custom_bool_mods = {
    "Gasoline_Flamethrower": ["savegame.mod.unlimitedfire"],
    "Multiple_Grenade_Launcher": ["savegame.mod.unlimitedammo", "savegame.mod.norecoil", "savegame.mod.noreticle"],
    "Lava_Gun": ["savegame.mod.fireamount"],
    "Lightning_Gun": ["savegame.mod.nodebris", "savegame.mod.nofire"],
    "AC130_Airstrike_MP": ["savegame.mod.nocd"],
    "Jackhammer": ["savegame.mod.jackhammer.nodamage"],
    "Magic_Bag": ["savegame.mod.magicbag.extendedreach"],
    "Swap_Button": ["savegame.mod.swapbutton.noselfswap"],
}

print("=" * 50)
print("Syncing tool settings to shared table")
print("=" * 50)

print("\n--- Unlimited ammo only ---")
for mod in simple_unlimited:
    process_simple_mod(mod, ["savegame.mod.unlimitedammo"])

print("\n--- Unlimited + realistic ---")
for mod in unlimited_realistic:
    process_simple_mod(mod, ["savegame.mod.unlimitedammo", "savegame.mod.realisticdamage"])

print("\n--- Norecoil ---")
for mod in norecoil_mods:
    process_simple_mod(mod, ["savegame.mod.norecoil"])

print("\n--- Custom bool settings ---")
for mod, keys in custom_bool_mods.items():
    process_simple_mod(mod, keys)
