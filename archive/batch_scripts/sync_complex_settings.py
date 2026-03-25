"""Sync complex tool settings (floats, ints, mixed types) to shared table."""
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
    return "Bool"

def process_mod(mod_name, settings):
    """settings = list of (savegame_key, type) tuples"""
    filepath = os.path.join(MODS_DIR, mod_name, "main.lua")
    if not os.path.isfile(filepath):
        print(f"  SKIP {mod_name}")
        return False

    with open(filepath, "r", errors="ignore") as f:
        content = f.read()
    original = content

    # 1. Add shared.toolSettings init in server.init
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
        print(f"  FIXED {mod_name}")
        return True
    print(f"  NO CHANGE {mod_name}")
    return False

# Complex mods with their settings
complex_mods = {
    "C4": [
        ("savegame.mod.explosionSize", "Float"),
        ("savegame.mod.explosionTimer", "Int"),
    ],
    "Exploding_Star": [
        ("savegame.mod.boomsize", "Float"),
        ("savegame.mod.fusetime", "Float"),
    ],
    "Explosive_Pack": [
        ("savegame.mod.explosivepack.claymore", "Bool"),
        ("savegame.mod.explosivepack.safety", "Int"),
    ],
    "Hook_Shotgun": [
        ("savegame.mod.kickbackpower", "Float"),
        ("savegame.mod.pelletdamage", "Float"),
        ("savegame.mod.pellets", "Float"),
        ("savegame.mod.pullpower", "Float"),
    ],
    "Ion_Cannon_Beacon": [
        ("savegame.mod.IonCannonBeaconDowngradeExplosion", "Bool"),
        ("savegame.mod.IonCannonBeaconEffectVolume", "Float"),
        ("savegame.mod.IonCannonBeaconEvaVolume", "Float"),
        ("savegame.mod.IonCannonBeaconQuickTrigger", "Bool"),
    ],
    "Laser_Cutter": [
        ("savegame.mod.holesize", "Float"),
        ("savegame.mod.range", "Float"),
        ("savegame.mod.startfire", "Bool"),
    ],
    "Scorpion": [
        ("savegame.mod.pullpower", "Float"),
        ("savegame.mod.punchpower", "Float"),
    ],
    "Sith_Saber": [
        ("savegame.mod.sound", "Int"),
        ("savegame.mod.vox", "Int"),
    ],
    "Spells": [
        ("savegame.mod.power", "Float"),
        ("savegame.mod.shake", "Float"),
        ("savegame.mod.volume", "Float"),
    ],
    "Winch": [
        ("savegame.mod.winch.slot", "Int"),
        ("savegame.mod.winch.speed", "Float"),
        ("savegame.mod.winch.strength", "Float"),
    ],
    "Revengeance_Katana": [
        ("savegame.mod.revengeance.slashDistance", "Int"),
        ("savegame.mod.revengeance.slashDrawParticles", "Bool"),
        ("savegame.mod.revengeance.slashForce", "Int"),
        ("savegame.mod.revengeance.slashOptimization", "Bool"),
        ("savegame.mod.revengeance.slashRadius", "Float"),
        ("savegame.mod.revengeance.slashSpawnFire", "Bool"),
    ],
    "Molotov_Cocktail": [
        ("savegame.mod.molotovBreakGlass", "Bool"),
        ("savegame.mod.molotovEmberCount", "Int"),
        ("savegame.mod.molotovEmberfire", "Bool"),
        ("savegame.mod.molotovMaxMolotovCount", "Int"),
        ("savegame.mod.molotovMaxWorldEmbers", "Int"),
        ("savegame.mod.molotovSilencedMolotov", "Bool"),
        ("savegame.mod.molotovUnlimitedAmmo", "Bool"),
    ],
    "Artillery_Barrage_RELOADED": [
        ("savegame.mod.barragere.barrageIntensity", "Float"),
        ("savegame.mod.barragere.baseReload", "Float"),
        ("savegame.mod.barragere.disablePlayerDamage", "Bool"),
        ("savegame.mod.barragere.disableReloadCooldown", "Bool"),
        ("savegame.mod.barragere.howitzers", "Int"),
        ("savegame.mod.barragere.shellsPerHowitzer", "Int"),
    ],
    "Mjolner": [
        ("savegame.mod.explosion", "Float"),
    ],
    "Magnetizer_V2": [
        ("savegame.mod.lightning", "Bool"),
    ],
    "Tripmine": [
        ("savegame.mod.tripmine.unlimitedammo", "Bool"),
    ],
}

print("=" * 50)
print("Syncing complex tool settings")
print("=" * 50)
print()

fixed = 0
for mod, settings in complex_mods.items():
    if process_mod(mod, settings):
        fixed += 1

print(f"\nFixed: {fixed}/{len(complex_mods)}")
