"""Mod feature matrix audit tool for Teardown MP Patcher."""

import re
from pathlib import Path

import click

from tools.common import discover_mods, read_lua_files

# ── Feature detection ────────────────────────────────────────────────────────

_SHOOT_RE = re.compile(r"\bShoot\s*\(|\bQueryShot\s*\(")
_AIM_INFO_RE = re.compile(r"\bGetPlayerAimInfo\s*\(")
_AMMO_PICKUP_RE = re.compile(r"\bSetToolAmmoPickupAmount\s*\(")
_OPTIONS_OPEN_RE = re.compile(r"optionsOpen|optionsopen|settingsOpen|showOptions|showSettings", re.IGNORECASE)
_UI_INTERACTIVE_RE = re.compile(r"\bUiMakeInteractive\s*\(")
_MENU_FRAMEWORK_RE = re.compile(r"\bmenu_draw\s*\(|\bmenu_init\s*\(|\bisMenuOpen\s*\(")
_KEYBIND_REMAP_RE = re.compile(r'savegame\.mod\.keys')
_AMMO_DISPLAY_RE = re.compile(r'SetString\s*\(.*ammo\.display')
_MAKEHOLE_RE = re.compile(r"\bMakeHole\s*\(")
_GUN_KEYWORDS_RE = re.compile(r"\b(bullet|ammo|magazine|reload)\b", re.IGNORECASE)
_UITEXT_RE = re.compile(r"\bUiText\s*\(")

# Key-like word inside a quoted string - letters, digits, underscore, 1-12 chars
_KEY_LIKE_RE = re.compile(r'"([a-zA-Z][a-zA-Z0-9_]{0,11})"')
_INPUT_PRESSED_RE = re.compile(r'\bInputPressed\s*\(')

# options guard: optionsOpen on same line as InputPressed/InputDown("usetool"),
# OR on an adjacent line within ±1
_USETOOL_LINE_RE = re.compile(r'Input(?:Pressed|Down)\s*\(\s*"usetool"')
_ANY_INPUT_LINE_RE = re.compile(r'Input(?:Pressed|Down|Released)\s*\(')

_EARLY_RETURN_GUARD_RE = re.compile(
    r'if\s+.*optionsOpen\s+then\s+return', re.IGNORECASE
)

_BLOCK_GUARD_RE = re.compile(
    r'if\s+not\s+\w+\.optionsOpen\s+then', re.IGNORECASE
)


def _options_guard(source: str) -> bool:
    """Return True if optionsOpen guards input handling.

    Detects six patterns:
    1. optionsOpen on same line or ±1 of usetool InputPressed/Down
    2. Early-return guard: ``if data.optionsOpen then return end`` before usetool
    3. ``not data.optionsOpen`` in a condition with usetool on same line
    4. Early-return or block guard before ANY input line (for mods using lmb/rmb)
    5. optionsOpen + early-return/block guard anywhere (guards engine-handled tool use)
    6. Menu framework: ``isMenuOpen()`` call indicates external menu system with guards
    """
    # Pattern 6: menu framework handles its own guarding
    if _MENU_FRAMEWORK_RE.search(source):
        return True
    if not _OPTIONS_OPEN_RE.search(source):
        return False
    lines = source.splitlines()
    has_early_return = False
    has_block_guard = False
    for i, line in enumerate(lines):
        if _EARLY_RETURN_GUARD_RE.search(line):
            has_early_return = True
        if _BLOCK_GUARD_RE.search(line):
            has_block_guard = True
        if _USETOOL_LINE_RE.search(line):
            if has_early_return or has_block_guard:
                return True
            # Pattern 1: ±1 neighbour check
            window = lines[max(0, i - 1): i + 2]
            if any(_OPTIONS_OPEN_RE.search(l) for l in window):
                return True
        # Pattern 4: early-return/block guard before any input call
        if _ANY_INPUT_LINE_RE.search(line) and not _USETOOL_LINE_RE.search(line):
            if has_early_return or has_block_guard:
                return True
    # Pattern 5: optionsOpen exists + guard exists = guards engine-handled tool use
    if has_early_return or has_block_guard:
        return True
    return False


_AUDIT_OK_RE = re.compile(r'--\s*@audit-ok\s+(\w+)')


def _audit_suppressions(source: str) -> set[str]:
    """Extract @audit-ok suppression tags from source comments.

    Usage in Lua: ``-- @audit-ok AimInfo`` suppresses AimInfo=X in the report.
    """
    return {m.group(1).lower() for m in _AUDIT_OK_RE.finditer(source)}


_KEYBIND_HINT_TEXT_RE = re.compile(
    r'UiText\s*\(.*(?:LMB|RMB|MMB|Fire|Reload|Options|Press|Hold|Click)', re.IGNORECASE
)


def _keybind_hints(source: str, has_options_menu: bool) -> bool:
    """Heuristic: detect keybind hint UiText in client.draw().

    Looks for UiText calls with keybind-like content (LMB, RMB, Fire, Reload, etc.)
    regardless of whether an options menu exists.
    """
    if _KEYBIND_HINT_TEXT_RE.search(source):
        return True
    # Fallback: options menu + InputPressed with raw key + UiText
    if has_options_menu and _UITEXT_RE.search(source) and _INPUT_PRESSED_RE.search(source):
        for m in re.finditer(r'\bInputPressed\s*\(\s*"([^"]+)"', source):
            key = m.group(1).lower()
            action_names = {"usetool", "interact", "flashlight", "jump", "crouch"}
            if key not in action_names:
                return True
    return False


_LUA_COMMENT_RE = re.compile(r'--(?!\s*@audit-ok).*$', re.MULTILINE)


def _strip_lua_comments(source: str) -> str:
    """Strip Lua single-line comments, preserving @audit-ok directives."""
    return _LUA_COMMENT_RE.sub('', source)


def detect_features(source: str) -> dict[str, bool]:
    """Detect mod features from Lua source text.

    Returns a dict with keys:
      has_shoot, has_aim_info, has_ammo_pickup, has_options_menu,
      has_options_guard, has_keybind_hints, has_keybind_remap,
      has_ammo_display_hidden, is_gun_mod
    """
    # Strip comments to avoid false positives from commented-out code
    code = _strip_lua_comments(source)
    has_shoot = bool(_SHOOT_RE.search(code))
    has_aim_info = bool(_AIM_INFO_RE.search(code))
    has_ammo_pickup = bool(_AMMO_PICKUP_RE.search(code))
    has_options_menu = (
        (bool(_OPTIONS_OPEN_RE.search(code)) and bool(_UI_INTERACTIVE_RE.search(code)))
        or bool(_MENU_FRAMEWORK_RE.search(code))
    )
    has_options_guard = _options_guard(code)
    has_keybind_remap = bool(_KEYBIND_REMAP_RE.search(code))
    has_ammo_display_hidden = bool(_AMMO_DISPLAY_RE.search(code))

    has_makehole = bool(_MAKEHOLE_RE.search(code))
    is_gun_mod = has_shoot or (has_makehole and bool(_GUN_KEYWORDS_RE.search(code)))

    has_keybind_hints = _keybind_hints(code, has_options_menu)

    suppressions = _audit_suppressions(source)

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
        "suppressions": suppressions,
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
    all_suppressions: set[str] = set()
    for _rel, source in read_lua_files(mod_dir):
        file_features = detect_features(source)
        for key, val in file_features.items():
            if key == "suppressions":
                all_suppressions |= val
            else:
                merged[key] = merged[key] or val
    merged["suppressions"] = all_suppressions

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

    # Map feature keys to suppression tag names
    _suppress_map = {"has_shoot": "shoot", "has_aim_info": "aiminfo"}

    for result in audit_results:
        name = result["name"]
        feats = result["features"]
        is_gun = feats.get("is_gun_mod", False)
        suppressions = feats.get("suppressions", set())
        cells = []
        for key in col_keys:
            val = feats.get(key, False)
            if val:
                cells.append("Y")
            elif is_gun and key in ("has_shoot", "has_aim_info"):
                # Check if suppressed via @audit-ok
                tag = _suppress_map.get(key, "")
                if tag and tag in suppressions:
                    cells.append("")  # Suppressed — not flagged
                else:
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
