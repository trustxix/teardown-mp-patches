"""Mod feature matrix audit tool for Teardown MP Patcher."""

import re
from pathlib import Path

import click

from tools.common import discover_mods, read_lua_files

# ── Feature detection ────────────────────────────────────────────────────────

_SHOOT_RE = re.compile(r"\bShoot\s*\(|\bQueryShot\s*\(")
_AIM_INFO_RE = re.compile(r"\bGetPlayerAimInfo\s*\(")
_AMMO_PICKUP_RE = re.compile(r"\bSetToolAmmoPickupAmount\s*\(")
_OPTIONS_OPEN_RE = re.compile(r"optionsOpen|optionsopen|settingsOpen", re.IGNORECASE)
_UI_INTERACTIVE_RE = re.compile(r"\bUiMakeInteractive\s*\(")
_KEYBIND_REMAP_RE = re.compile(r'savegame\.mod\.keys')
_AMMO_DISPLAY_RE = re.compile(r'SetString\s*\(\s*"game\.tool\.\w+\.ammo\.display"')
_MAKEHOLE_RE = re.compile(r"\bMakeHole\s*\(")
_GUN_KEYWORDS_RE = re.compile(r"\b(bullet|ammo|magazine|reload)\b", re.IGNORECASE)
_UITEXT_RE = re.compile(r"\bUiText\s*\(")

# Key-like word inside a quoted string - letters, digits, underscore, 1-12 chars
_KEY_LIKE_RE = re.compile(r'"([a-zA-Z][a-zA-Z0-9_]{0,11})"')
_INPUT_PRESSED_RE = re.compile(r'\bInputPressed\s*\(')

# options guard: optionsOpen on same line as InputPressed/InputDown("usetool"),
# OR on an adjacent line within ±1
_USETOOL_LINE_RE = re.compile(r'Input(?:Pressed|Down)\s*\(\s*"usetool"')


def _options_guard(source: str) -> bool:
    """Return True if optionsOpen appears near a usetool InputPressed/Down call."""
    if not _OPTIONS_OPEN_RE.search(source):
        return False
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if _USETOOL_LINE_RE.search(line):
            # Check the line itself and ±1 neighbours
            window = lines[max(0, i - 1): i + 2]
            if any(_OPTIONS_OPEN_RE.search(l) for l in window):
                return True
    return False


def _keybind_hints(source: str, has_options_menu: bool) -> bool:
    """Heuristic: options menu present + UiText calls + InputPressed with key-like strings."""
    if not has_options_menu:
        return False
    if not _UITEXT_RE.search(source):
        return False
    if not _INPUT_PRESSED_RE.search(source):
        return False
    # Check that at least one InputPressed call uses a key-like (non-action) string
    for m in re.finditer(r'\bInputPressed\s*\(\s*"([^"]+)"', source):
        key = m.group(1).lower()
        # Action names that are NOT raw keys
        action_names = {"usetool", "interact", "flashlight", "jump", "crouch"}
        if key not in action_names:
            return True
    return False


def detect_features(source: str) -> dict[str, bool]:
    """Detect mod features from Lua source text.

    Returns a dict with keys:
      has_shoot, has_aim_info, has_ammo_pickup, has_options_menu,
      has_options_guard, has_keybind_hints, has_keybind_remap,
      has_ammo_display_hidden, is_gun_mod
    """
    has_shoot = bool(_SHOOT_RE.search(source))
    has_aim_info = bool(_AIM_INFO_RE.search(source))
    has_ammo_pickup = bool(_AMMO_PICKUP_RE.search(source))
    has_options_menu = (
        bool(_OPTIONS_OPEN_RE.search(source)) and bool(_UI_INTERACTIVE_RE.search(source))
    )
    has_options_guard = _options_guard(source)
    has_keybind_remap = bool(_KEYBIND_REMAP_RE.search(source))
    has_ammo_display_hidden = bool(_AMMO_DISPLAY_RE.search(source))

    has_makehole = bool(_MAKEHOLE_RE.search(source))
    is_gun_mod = has_shoot or (has_makehole and bool(_GUN_KEYWORDS_RE.search(source)))

    has_keybind_hints = _keybind_hints(source, has_options_menu)

    return {
        "has_shoot": has_shoot,
        "has_aim_info": has_aim_info,
        "has_ammo_pickup": has_ammo_pickup,
        "has_options_menu": has_options_menu,
        "has_options_guard": has_options_guard,
        "has_keybind_hints": has_keybind_hints,
        "has_keybind_remap": has_keybind_remap,
        "has_ammo_display_hidden": has_ammo_display_hidden,
        "is_gun_mod": is_gun_mod,
    }


# ── Mod-level audit ──────────────────────────────────────────────────────────

def audit_mod(mod_dir: Path) -> dict:
    """Audit all .lua files in a mod directory and merge features (OR across files)."""
    merged: dict[str, bool] = {
        "has_shoot": False,
        "has_aim_info": False,
        "has_ammo_pickup": False,
        "has_options_menu": False,
        "has_options_guard": False,
        "has_keybind_hints": False,
        "has_keybind_remap": False,
        "has_ammo_display_hidden": False,
        "is_gun_mod": False,
    }
    for _rel, source in read_lua_files(mod_dir):
        file_features = detect_features(source)
        for key, val in file_features.items():
            merged[key] = merged[key] or val

    return {"name": mod_dir.name, "features": merged}


# ── Report generation ────────────────────────────────────────────────────────

_COLUMNS = [
    ("has_shoot",             "Shoot"),
    ("has_aim_info",          "AimInfo"),
    ("has_ammo_pickup",       "AmmoPickup"),
    ("has_options_menu",      "OptionsMenu"),
    ("has_options_guard",     "OptionsGuard"),
    ("has_keybind_hints",     "KeybindHints"),
    ("has_keybind_remap",     "KeybindRemap"),
    ("has_ammo_display_hidden", "AmmoDisplay"),
    ("is_gun_mod",            "IsGun"),
]


def generate_report(audit_results: list[dict]) -> str:
    """Generate a markdown table from audit results.

    For is_gun_mod mods that are missing has_shoot or has_aim_info, the
    respective cell is marked ✗ (should have it, but doesn't).
    """
    if not audit_results:
        return "_No mods found._"

    # Header
    col_keys = [c[0] for c in _COLUMNS]
    col_headers = [c[1] for c in _COLUMNS]

    header = "| Mod | " + " | ".join(col_headers) + " |"
    separator = "| --- | " + " | ".join(["---"] * len(_COLUMNS)) + " |"

    rows = [header, separator]

    for result in audit_results:
        name = result["name"]
        feats = result["features"]
        is_gun = feats.get("is_gun_mod", False)
        cells = []
        for key in col_keys:
            val = feats.get(key, False)
            if val:
                cells.append("Y")
            elif is_gun and key in ("has_shoot", "has_aim_info"):
                # Gun mod missing these - flag as should-have
                cells.append("X")
            else:
                cells.append("")
        rows.append("| " + name + " | " + " | ".join(cells) + " |")

    return "\n".join(rows)


# ── CLI ───────────────────────────────────────────────────────────────────────

@click.command("audit")
@click.option("--mod", "mod_name", default=None, help="Single mod")
@click.option("--output", "output_path", default=None, help="Write report to file")
def audit_cli(mod_name, output_path):
    """Generate mod feature compliance matrix."""
    mods = discover_mods(mod_name=mod_name)
    results = [audit_mod(m) for m in mods]
    report = generate_report(results)
    click.echo(report)
    if output_path:
        Path(output_path).write_text(report, encoding="utf-8")
        click.echo(f"\nReport written to {output_path}")


if __name__ == "__main__":
    audit_cli()
