"""Apply UI standards to all gun mods with the common HUD template.

Pattern to find and replace:
1. Keybind hints block: UiTranslate(10, UiHeight()-N) with bold 20, multiline UiText
   → Stacked table, bold 16, 0.6 opacity, anchor H-30
2. Ammo block: UiTranslate(UiCenter(), UiHeight()-60) with bold 32
   → bold 18, UiWidth()/2, yellow RELOADING
3. "[O] Options" hint below ammo → removed
4. DrawCrosshair() calls → removed
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

def process_mod(mod_name, main_file="main.lua"):
    filepath = os.path.join(MODS_DIR, mod_name, main_file)
    if not os.path.isfile(filepath):
        print(f"  SKIP {mod_name}: {main_file} not found")
        return False

    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    original = content
    changes = []

    # 1. Remove DrawCrosshair() calls
    if "DrawCrosshair()" in content:
        # Remove the line and any blank line after
        content = re.sub(r'\s*DrawCrosshair\(\)\s*\n', '\n', content)
        changes.append("removed DrawCrosshair()")

    # 2. Fix keybind hints: multiline UiText with \n → stacked table
    # Pattern: UiTranslate(10, UiHeight() - N) ... UiFont("bold.ttf", 20) ... UiText("X\nY\nZ\n...")
    def fix_keybind_block(m):
        full = m.group(0)
        # Extract the hint text
        text_match = re.search(r'UiText\("([^"]+)"\)', full)
        if not text_match:
            return full
        hints_raw = text_match.group(1)
        # Filter out "O - Options" hints
        hints = [h.strip() for h in hints_raw.split("\\n") if h.strip() and "Options" not in h and "[O]" not in h]
        if not hints:
            return full

        # Build replacement
        hints_lua = ", ".join([f'"{h}"' for h in hints])
        indent = "\t" if "\t" in full else "    "
        replacement = f"""{indent}{indent}local hints = {{{hints_lua}}}
{indent}{indent}UiPush()
{indent}{indent}UiAlign("left bottom")
{indent}{indent}UiFont("bold.ttf", 16)
{indent}{indent}UiTextOutline(0, 0, 0, 1, 0.1)
{indent}{indent}UiColor(1, 1, 1, 0.6)
{indent}{indent}UiTranslate(10, UiHeight() - 30)
{indent}{indent}for i = #hints, 1, -1 do
{indent}{indent}{indent}UiText(hints[i])
{indent}{indent}{indent}UiTranslate(0, -20)
{indent}{indent}end
{indent}{indent}UiPop()"""
        return replacement

    # Match keybind blocks
    pattern_keybind = re.compile(
        r'UiPush\(\)\s*\n'
        r'\s*UiTranslate\(10,\s*UiHeight\(\)\s*-\s*\d+\)\s*\n'
        r'\s*UiAlign\("left bottom"\)\s*\n'
        r'\s*UiColor\(1,\s*1,\s*1,\s*0\.8\)\s*\n'
        r'\s*UiFont\("bold\.ttf",\s*20\)\s*\n'
        r'\s*UiTextOutline\([^)]+\)\s*\n'
        r'\s*UiText\("[^"]+"\)\s*\n'
        r'\s*UiPop\(\)',
        re.MULTILINE
    )

    new_content = pattern_keybind.sub(fix_keybind_block, content)
    if new_content != content:
        content = new_content
        changes.append("fixed keybind hints")

    # 3. Fix ammo display: bold 32 → bold 18, center middle → center
    # Replace font size in ammo blocks
    # Pattern: UiFont("bold.ttf", 32) near ammo display
    ammo_pattern = re.compile(
        r'(UiTranslate\(UiCenter\(\),\s*UiHeight\(\)\s*-\s*60\)\s*\n'
        r'\s*UiAlign\("center middle"\)\s*\n'
        r'\s*UiColor\(1,\s*1,\s*1\)\s*\n'
        r'\s*UiFont\("bold\.ttf",\s*)32(\))',
        re.MULTILINE
    )
    if ammo_pattern.search(content):
        # Replace the whole ammo block more carefully
        pass  # Will handle case by case below

    # Simple font size replacement in ammo context
    # Find UiFont("bold.ttf", 32) that's near ammo/reloading text
    content_new = content
    # Replace bold 32 → bold 18 (only in draw/client.draw context)
    content_new = re.sub(
        r'(UiTranslate\(UiCenter\(\),\s*UiHeight\(\)\s*-\s*60\)\s*\n\s*UiAlign\("center middle"\)\s*\n\s*UiColor\(1,\s*1,\s*1\)\s*\n\s*UiFont\("bold\.ttf",\s*)32',
        r'\g<1>18',
        content_new
    )
    # Also fix alignment from "center middle" to "center"
    # And add proper positioning
    if content_new != content:
        content = content_new
        changes.append("reduced ammo font 32 to 18")

    # 4. Remove "[O] Options" hint below ammo
    content_new = re.sub(
        r'\s*UiTranslate\(0,\s*30\)\s*\n\s*UiFont\("regular\.ttf",\s*18\)\s*\n\s*UiText\("\[O\] Options"\)',
        '',
        content
    )
    if content_new != content:
        content = content_new
        changes.append("removed [O] Options hint")

    # 5. Fix "Reloading" text to "RELOADING..."
    content = content.replace('UiText("Reloading")', 'UiColor(1, 0.8, 0, 0.9)\n\t\t\tUiText("RELOADING...")')

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  FIXED {mod_name}: {', '.join(changes)}")
        return True
    else:
        print(f"  NO CHANGE {mod_name}")
        return False

# Standard gun mods with the common template
standard_guns = [
    "Desert_Eagle",
    "M249",
    "M4A1",
    "Nova_Shotgun",
    "P90",
    "SCAR-20",
    "Charge_Shotgun",
    "AWP",
    "Dual_Berettas",
    "Dual_Miniguns",
    "Minigun",
    "M1_Garand",
]

# Other mods with keybind hints that need the same treatment
other_mods_with_hints = [
    "Gasoline_Flamethrower",
    "Jackhammer",
    "Lightning_Gun",
    "Laser_Cutter",
    "Lava_Gun",
    "Lightsaber",
    "Sith_Saber",
    "Welding_Tool",
    "Winch",
    "C4",
    "Explosive_Pack",
    "Magic_Bag",
    "Asteroid_Strike",
    "Multi_Grenade_Launcher",
    "Multiple_Grenade_Launcher",
    "Attack_Drone",
]

# Mods with keybinds at center that need moving to bottom-left
center_hint_mods = [
    "Airstrike_Arsenal",
    "Remote_Explosives",
    "Tripmine",
    "Rods_from_Gods",
    "Magnetizer_V2",
]

print("=" * 50)
print("Applying UI standards")
print("=" * 50)

print("\n--- Standard gun mods ---")
for mod in standard_guns:
    process_mod(mod)

print("\n--- Other mods with hints ---")
for mod in other_mods_with_hints:
    process_mod(mod)

print("\n--- Center hint mods ---")
for mod in center_hint_mods:
    process_mod(mod)
