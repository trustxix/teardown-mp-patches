"""Assign all tools to proper category groups (1-6)."""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

# Group assignments: mod_folder -> group number
GROUPS = {
    # Group 1: Pistols & SMGs
    "Desert_Eagle": 1, "P90": 1, "Dual_Berettas": 1, "ARM_Glock": 1,

    # Group 2: Rifles & Shotguns
    "AK-47": 2, "M4A1": 2, "AWP": 2, "M1_Garand": 2, "SCAR-20": 2,
    "M249": 2, "Nova_Shotgun": 2, "Charge_Shotgun": 2, "Hook_Shotgun": 2,
    "ARM_M4A4": 2, "ARM_AK47": 2,

    # Group 3: Heavy Weapons
    "Minigun": 3, "Dual_Miniguns": 3, "MEGAGUN": 3, "M2A1_Flamethrower": 3,
    "Lava_Gun": 3, "Acid_Gun": 3, "Lightning_Gun": 3, "Bee_Gun": 3,
    "Gasoline_Flamethrower": 3, "Laser_Cutter": 3,

    # Group 4: Explosives & Launchers
    "C4": 4, "Tripmine": 4, "Remote_Explosives": 4, "Multi_Grenade_Launcher": 4,
    "Multiple_Grenade_Launcher": 4, "Molotov_Cocktail": 4, "Holy_Grenade": 4,
    "Exploding_Star": 4, "Explosive_Pack": 4, "Bomb_Attack": 4, "HADOUKEN": 4,
    "Bombard": 4,

    # Group 5: Melee & Special
    "Lightsaber": 5, "Lightkatana": 5, "Light_Katana_MP": 5, "Dragonslayer": 5,
    "Revengeance_Katana": 5, "Mjolner": 5, "Scorpion": 5, "Sith_Saber": 5,
    "ODM_Gear": 5, "Light_Saber": 5, "Jackhammer": 5,

    # Group 6: Utilities & Gadgets
    "Telekinesis": 6, "Swap_Button": 6, "Vacuum_Cleaner": 6, "Fire_Locator": 6,
    "Welding_Tool": 6, "Magnets": 6, "Magnetizer_V2": 6, "Bouncepad": 6,
    "Winch": 6, "Thruster_Tool_Multiplayer": 6, "Portal_Gun_MP": 6,
    "Control": 6, "Black_Hole": 6, "Magic_Bag": 6, "Attack_Drone": 6,
    "High_Tech_Drone": 6, "FPV_Drone_Tool": 6, "Guided_Missile": 6,
    "Bunker_Buster_MP": 6, "AC130_Airstrike_MP": 6, "Airstrike_Arsenal": 6,
    "Rods_from_Gods": 6, "Asteroid_Strike": 6, "Ion_Cannon_Beacon": 6,
    "Artillery_Barrage_RELOADED": 6, "CnC_Weather_Machine": 6,
    "Vortexes_and_Tornadoes": 6, "Corrupted_Crystal": 6, "Melt": 6,
    "Omni_Gun": 6, "Spells": 6, "Hungry_Slimes": 6, "Enchanter": 6,
    "Minecraft_Building_Tool": 6, "Object_Possession": 6,
    "Infinity_Technique": 6, "Final_Flash": 6, "Predator_Missile_MP": 6,
    "Adjustable_Fire": 6,
}

fixed = 0
for mod, group in sorted(GROUPS.items()):
    # Check main.lua and all lua files for RegisterTool
    mod_dir = os.path.join(MODS_DIR, mod)
    if not os.path.isdir(mod_dir):
        continue

    for root, dirs, files in os.walk(mod_dir):
        for fname in files:
            if not fname.endswith(".lua"):
                continue
            filepath = os.path.join(root, fname)
            with open(filepath, "r", errors="ignore") as f:
                content = f.read()

            if "RegisterTool(" not in content:
                continue

            original = content
            # Pattern: RegisterTool("id", "name", "vox", N) or RegisterTool("id", "name", "vox")
            def replace_group(m):
                full = m.group(0)
                pre = m.group(1)
                old_group = m.group(2)
                if old_group:
                    return pre + str(group) + ")"
                else:
                    # No group param — add one
                    return full[:-1] + ", " + str(group) + ")"

            new_content = re.sub(
                r'(RegisterTool\(\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*)(\d+)\)',
                replace_group,
                content
            )

            # Handle case where no group param exists
            if new_content == content:
                new_content = re.sub(
                    r'(RegisterTool\(\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*"[^"]+"\s*)\)',
                    lambda m: m.group(1) + ", " + str(group) + ")",
                    content
                )

            if new_content != original:
                with open(filepath, "w") as f:
                    f.write(new_content)
                relpath = os.path.relpath(filepath, MODS_DIR)
                fixed += 1

print(f"Updated {fixed} files")
