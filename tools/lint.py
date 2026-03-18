"""Tier-1 and tier-2 lint checks for Teardown v2 multiplayer mod compatibility.

Each check function takes a Lua source string and returns a list of finding
dicts with keys: check, line, severity, file, detail.
The 'file' field is left as "" and filled in by the caller (lint_source).
"""

from __future__ import annotations

import re

from tools.common import RAW_KEYS


# ---------------------------------------------------------------------------
# Comment-stripping helper (replicated from validate.py approach)
# ---------------------------------------------------------------------------

def _strip_comment(line: str) -> str:
    """Remove Lua line comment (--) from a line, respecting string literals."""
    in_single = False
    in_double = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif c == '-' and not in_single and not in_double:
            if i + 1 < len(line) and line[i + 1] == '-':
                return line[:i]
        i += 1
    return line


# ---------------------------------------------------------------------------
# Block-depth helpers (for context-aware checks)
# ---------------------------------------------------------------------------

_FUNC_KEYWORD_RE = re.compile(r"\bfunction\b")
_IF_RE = re.compile(r"\bif\b")
_FOR_RE = re.compile(r"\bfor\b")
_WHILE_RE = re.compile(r"\bwhile\b")
_REPEAT_RE = re.compile(r"\brepeat\b")
_DO_RE = re.compile(r"\bdo\b")
_END_RE = re.compile(r"\bend\b")
_UNTIL_RE = re.compile(r"\buntil\b")
_FUNC_DEF_RE = re.compile(r"^\s*function\s+([\w.]+)\s*\(")


def _count_opens(line: str) -> int:
    count = 0
    count += len(_FUNC_KEYWORD_RE.findall(line))
    count += len(_IF_RE.findall(line))
    count += len(_FOR_RE.findall(line))
    count += len(_WHILE_RE.findall(line))
    count += len(_REPEAT_RE.findall(line))
    # Note: standalone `do` is NOT counted. In `for/while ... do`, the
    # for/while already counts the nesting level. Counting `do` separately
    # breaks when `for` and `do` span different lines (e.g. multi-line
    # for loops), causing a permanent depth imbalance.
    return count


def _count_ends(line: str) -> int:
    return len(_END_RE.findall(line)) + len(_UNTIL_RE.findall(line))


# ---------------------------------------------------------------------------
# Finding builder
# ---------------------------------------------------------------------------

def _finding(check_id: str, lineno: int, detail: str, severity: str = "error") -> dict:
    return {
        "check": check_id,
        "line": lineno,
        "severity": severity,
        "file": "",
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# Check 1: ipairs on Players() iterators
# ---------------------------------------------------------------------------

_IPAIRS_ITER_RE = re.compile(
    r"ipairs\s*\(\s*(Players|PlayersAdded|PlayersRemoved)\s*\("
)


def check_ipairs_iterator(source: str) -> list[dict]:
    """Catch ipairs(Players()), ipairs(PlayersAdded()), ipairs(PlayersRemoved()).

    These are iterators in Teardown v2, not tables. Using ipairs on them crashes.
    """
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        m = _IPAIRS_ITER_RE.search(stripped)
        if m:
            findings.append(_finding(
                "IPAIRS-ITERATOR",
                lineno,
                f"ipairs() on iterator {m.group(1)}() - use 'for p in {m.group(1)}() do' instead",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check 2: Raw keys with player parameter
# ---------------------------------------------------------------------------

_INPUT_FUNC_RE = re.compile(
    r"\b(InputPressed|InputReleased|InputDown)\s*\(\s*\"([^\"]+)\"\s*,"
)


def check_raw_key_player(source: str) -> list[dict]:
    """Catch InputPressed/InputReleased/InputDown with raw key + player parameter.

    Raw keys don't work with a player parameter in Teardown v2; they silently fail.
    Use action keys (usetool, interact, jump, etc.) instead.
    """
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        for m in _INPUT_FUNC_RE.finditer(stripped):
            func_name = m.group(1)
            key_name = m.group(2)
            if key_name in RAW_KEYS:
                findings.append(_finding(
                    "RAW-KEY-PLAYER",
                    lineno,
                    f"{func_name}(\"{key_name}\", p) - raw key with player arg silently fails; "
                    f"use action key or InputPressed(\"{key_name}\") with isLocal check",
                ))
    return findings


# ---------------------------------------------------------------------------
# Check 3: SetToolEnabled wrong argument order
# ---------------------------------------------------------------------------

_SET_TOOL_ENABLED_RE = re.compile(r"SetToolEnabled\s*\(\s*([^\s,)]+)")


def check_tool_enabled_order(source: str) -> list[dict]:
    """Catch SetToolEnabled(p, 'id', true) - wrong argument order.

    Correct form: SetToolEnabled("toolid", true, p) - first arg must be a string literal.
    """
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        for m in _SET_TOOL_ENABLED_RE.finditer(stripped):
            first_arg = m.group(1).strip()
            if not first_arg.startswith('"'):
                findings.append(_finding(
                    "TOOL-ENABLED-ORDER",
                    lineno,
                    f"SetToolEnabled() first arg is not a string literal ({first_arg!r}); "
                    f"correct order is SetToolEnabled(\"toolid\", true, p)",
                ))
    return findings


# ---------------------------------------------------------------------------
# Check 4: "alttool" string literal
# ---------------------------------------------------------------------------

_ALTTOOL_RE = re.compile(r'"alttool"')


def check_alttool(source: str) -> list[dict]:
    """Catch "alttool" anywhere in source - should be "rmb" instead."""
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _ALTTOOL_RE.search(stripped):
            findings.append(_finding(
                "ALTTOOL",
                lineno,
                '"alttool" key does not exist in v2; use "rmb" instead',
            ))
    return findings


# ---------------------------------------------------------------------------
# Check 5: goto / label syntax (Lua 5.1 doesn't support goto)
# ---------------------------------------------------------------------------

_GOTO_RE = re.compile(r"\bgoto\s+\w+")
_LABEL_RE = re.compile(r"::\w+::")


def check_goto_label(source: str) -> list[dict]:
    """Catch goto statements and ::label:: syntax.

    Teardown uses Lua 5.1 which does not support goto or labels.
    """
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _GOTO_RE.search(stripped):
            findings.append(_finding(
                "GOTO-LABEL",
                lineno,
                "goto is not supported in Lua 5.1 (Teardown runtime)",
            ))
        elif _LABEL_RE.search(stripped):
            findings.append(_finding(
                "GOTO-LABEL",
                lineno,
                "::label:: syntax is not supported in Lua 5.1 (Teardown runtime)",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check 6: mousedx / mousedy
# ---------------------------------------------------------------------------

_MOUSEDX_RE = re.compile(r'"mousedx"|"mousedy"')


def check_mousedx(source: str) -> list[dict]:
    """Catch "mousedx" and "mousedy" key names - use "camerax"/"cameray" instead."""
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        m = _MOUSEDX_RE.search(stripped)
        if m:
            key = m.group(0).strip('"')
            replacement = "camerax" if key == "mousedx" else "cameray"
            findings.append(_finding(
                "MOUSEDX",
                lineno,
                f'"{key}" does not work in v2; use "{replacement}" instead',
            ))
    return findings


# ---------------------------------------------------------------------------
# Check 7: SetPlayerTransform inside client.* functions
# ---------------------------------------------------------------------------

_SET_PLAYER_TRANSFORM_RE = re.compile(r"\bSetPlayerTransform\s*\(")


def check_set_player_transform_client(source: str) -> list[dict]:
    """Catch SetPlayerTransform inside client.* functions.

    SetPlayerTransform is server-only in Teardown v2; calling it from a
    client.* function will silently do nothing or cause desyncs.
    """
    findings = []
    current_func: str | None = None
    depth = 0

    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        func_match = _FUNC_DEF_RE.match(stripped)
        opens = _count_opens(stripped)
        ends = _count_ends(stripped)

        if func_match and depth == 0:
            current_func = func_match.group(1)
            depth = 1 + (opens - 1) - ends
        elif depth > 0:
            depth += opens - ends

        if depth < 0:
            depth = 0

        if _SET_PLAYER_TRANSFORM_RE.search(stripped):
            if current_func is not None and current_func.startswith("client."):
                findings.append(_finding(
                    "SPT-CLIENT",
                    lineno,
                    f"SetPlayerTransform() is server-only; found inside {current_func!r}",
                ))

        if depth == 0:
            current_func = None

    return findings


# ---------------------------------------------------------------------------
# Check 8: top-level function draw() without client. prefix
# ---------------------------------------------------------------------------

_BARE_DRAW_RE = re.compile(r"^\s*function\s+draw\s*\(")


def check_draw_not_client(source: str) -> list[dict]:
    """Catch bare function draw() at top level - must be client.draw() in v2."""
    findings = []
    depth = 0

    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        opens = _count_opens(stripped)
        ends = _count_ends(stripped)

        # Only flag top-level bare draw()
        if depth == 0 and _BARE_DRAW_RE.match(stripped):
            findings.append(_finding(
                "DRAW-NOT-CLIENT",
                lineno,
                "function draw() must be function client.draw() in v2",
            ))

        # Update depth after checking (so the function itself is depth 0 when detected)
        func_match = _FUNC_DEF_RE.match(stripped)
        if func_match and depth == 0:
            depth = 1 + (opens - 1) - ends
        elif depth > 0:
            depth += opens - ends

        if depth < 0:
            depth = 0

    return findings


# ===========================================================================
# Tier-2 checks - missing features / best practices
# ===========================================================================

# ---------------------------------------------------------------------------
# Check T2-1: Missing ammo display string
# ---------------------------------------------------------------------------

_REGISTER_TOOL_ID_RE = re.compile(r'RegisterTool\s*\(\s*"([^"]+)"')
_SET_AMMO_DISPLAY_RE = re.compile(r'SetString\s*\(\s*"game\.tool\.([^"]+)\.ammo\.display"')


def check_missing_ammo_display(source: str) -> list[dict]:
    """Warn if RegisterTool exists but matching ammo display SetString is absent.

    Without SetString("game.tool.ID.ammo.display", ""), the engine renders
    a default ammo counter that looks wrong in multiplayer mods.
    """
    findings = []
    tool_ids = _REGISTER_TOOL_ID_RE.findall(source)
    if not tool_ids:
        return findings
    display_ids = set(_SET_AMMO_DISPLAY_RE.findall(source))
    lines = source.splitlines()
    for tool_id in tool_ids:
        if tool_id not in display_ids:
            # Find the line of the RegisterTool call for this id
            for lineno, raw_line in enumerate(lines, 1):
                stripped = _strip_comment(raw_line)
                m = _REGISTER_TOOL_ID_RE.search(stripped)
                if m and m.group(1) == tool_id:
                    findings.append(_finding(
                        "MISSING-AMMO-DISPLAY",
                        lineno,
                        f'RegisterTool("{tool_id}") has no SetString("game.tool.{tool_id}.ammo.display", "") - '
                        f"engine ammo counter will show by default",
                        severity="warn",
                    ))
                    break
    return findings


# ---------------------------------------------------------------------------
# Check T2-2: Missing SetToolAmmo
# ---------------------------------------------------------------------------

_SET_TOOL_ENABLED_PRESENT_RE = re.compile(r"\bSetToolEnabled\s*\(")
_SET_TOOL_AMMO_PRESENT_RE = re.compile(r"\bSetToolAmmo\s*\(")


def check_missing_tool_ammo(source: str) -> list[dict]:
    """Warn if SetToolEnabled is used but SetToolAmmo is absent.

    Mods that enable tools should also set initial ammo to avoid showing 0.
    """
    if not _SET_TOOL_ENABLED_PRESENT_RE.search(source):
        return []
    if _SET_TOOL_AMMO_PRESENT_RE.search(source):
        return []
    # Find first SetToolEnabled line for the finding
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _SET_TOOL_ENABLED_PRESENT_RE.search(stripped):
            return [_finding(
                "MISSING-TOOL-AMMO",
                lineno,
                "SetToolEnabled() present but no SetToolAmmo() found - "
                "players may see 0 ammo on first equip",
                severity="warn",
            )]
    return []


# ---------------------------------------------------------------------------
# Check T2-3: Missing SetToolAmmoPickupAmount
# ---------------------------------------------------------------------------

_REGISTER_TOOL_RE = re.compile(r"\bRegisterTool\s*\(")
_AMMO_PICKUP_AMOUNT_RE = re.compile(r"\bSetToolAmmoPickupAmount\s*\(")


def check_missing_ammo_pickup(source: str) -> list[dict]:
    """Warn if RegisterTool exists but SetToolAmmoPickupAmount is absent.

    Mods without SetToolAmmoPickupAmount won't integrate with ammo crates.
    """
    if not _REGISTER_TOOL_RE.search(source):
        return []
    if _AMMO_PICKUP_AMOUNT_RE.search(source):
        return []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _REGISTER_TOOL_RE.search(stripped):
            return [_finding(
                "MISSING-AMMO-PICKUP",
                lineno,
                "RegisterTool() present but no SetToolAmmoPickupAmount() - "
                "ammo crates won't refill this tool. "
                "See docs/RESEARCH.md Finding #5",
                severity="warn",
            )]
    return []


# ---------------------------------------------------------------------------
# Check T2-4: Missing optionsOpen guard on usetool input
# ---------------------------------------------------------------------------

_USETOOL_INPUT_RE = re.compile(r'Input(?:Pressed|Down)\s*\(\s*"usetool"')
_NEGATED_USETOOL_RE = re.compile(r'not\s+Input(?:Pressed|Down)\s*\(\s*"usetool"')
_OPTIONS_OPEN_RE = re.compile(r"\b(?:optionsOpen|optionsopen|settingsOpen|showOptions|showSettings)\b")


def check_missing_options_guard(source: str) -> list[dict]:
    """Warn if usetool input is used without nearby optionsOpen guard.

    Without the guard, the tool fires while the options menu is open.
    The guard should appear within 3 lines before the usetool check,
    or on the same line. Negated patterns (not InputDown("usetool"))
    are excluded — they run when NOT pressing trigger (e.g. spread decay).
    """
    if not _OPTIONS_OPEN_RE.search(source):
        # No optionsOpen concept at all - heuristic: skip if optionsOpen never used
        return []

    findings = []
    lines = source.splitlines()
    for lineno, raw_line in enumerate(lines, 1):
        stripped = _strip_comment(raw_line)
        if not _USETOOL_INPUT_RE.search(stripped):
            continue
        # Skip negated patterns: "not InputDown("usetool")" — these are
        # spread-decay or idle checks that correctly run regardless of menu state
        if _NEGATED_USETOOL_RE.search(stripped):
            continue
        # Check this line and up to 3 lines before for optionsOpen
        window_start = max(0, lineno - 4)  # lineno is 1-based; lines[lineno-1] is current
        window = lines[window_start:lineno]
        has_guard = any(
            _OPTIONS_OPEN_RE.search(_strip_comment(l)) for l in window
        )
        if not has_guard:
            findings.append(_finding(
                "MISSING-OPTIONS-GUARD",
                lineno,
                'InputPressed/Down("usetool") without nearby optionsOpen guard - '
                "tool fires while options menu is open. "
                "See ISSUES_AND_FIXES.md Issue #32",
                severity="warn",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check T2-5: Missing server.setOptionsOpen function
# ---------------------------------------------------------------------------

_SERVER_SET_OPTIONS_RE = re.compile(r"\bserver\.set(?:Options|Settings)Open\b")


def check_missing_options_sync(source: str) -> list[dict]:
    """Warn if optionsOpen is used but no server.setOptionsOpen function defined.

    The standard pattern requires a server function to sync the options state.
    """
    if not _OPTIONS_OPEN_RE.search(source):
        return []
    if _SERVER_SET_OPTIONS_RE.search(source):
        return []
    # Report on the first optionsOpen line
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _OPTIONS_OPEN_RE.search(stripped):
            return [_finding(
                "MISSING-OPTIONS-SYNC",
                lineno,
                "optionsOpen used but no server.setOptionsOpen function found - "
                "options state may not sync across clients. "
                "See ISSUES_AND_FIXES.md Issue #32",
                severity="warn",
            )]
    return []


# ---------------------------------------------------------------------------
# Check T2-6: Handle > 0 comparisons (should use ~= 0)
# ---------------------------------------------------------------------------

_HANDLE_GT_ZERO_RE = re.compile(r"(\#?\w+)\s*>\s*0\s+then\b")

# Variable names that are clearly NOT entity handles — skip these
_NON_HANDLE_NAMES = {
    "dist", "distance", "depth", "count", "size", "amount", "time", "dt",
    "hp", "health", "damage", "ammo", "mags", "speed", "velocity", "angle",
    "alpha", "scale", "width", "height", "radius", "length", "weight",
    "mass", "force", "power", "level", "index", "num", "total", "max",
    "min", "timer", "cooldown", "delay", "duration", "progress", "ratio",
    "x", "y", "z", "direction", "strength", "volume", "intensity",
    "temperature", "frequency", "lifetime",
    "scroll", "ymovement", "offset",
}
# Suffixes that indicate non-handle numeric variables
_NON_HANDLE_SUFFIXES = (
    "Timer", "Count", "Speed", "Power", "Strength", "Offset", "Size",
    "Delay", "Duration", "Amount", "Distance", "Angle", "Scale",
    "Height", "Width", "Length", "Radius", "Weight", "Mass", "Force",
    "Level", "Index", "Velocity", "Progress", "Ratio", "Lifetime",
    "Pos", "Belts", "Clouds", "Binds", "Values",
)


def _is_non_handle_name(var_name: str) -> bool:
    """Return True if var_name is clearly not an entity handle."""
    if var_name.startswith("#"):
        return True  # #table is length, not a handle
    lower = var_name.lower()
    if lower in _NON_HANDLE_NAMES:
        return True
    for suffix in _NON_HANDLE_SUFFIXES:
        if lower.endswith(suffix.lower()):
            return True
    return False


def check_handle_gt_zero(source: str) -> list[dict]:
    """Warn on handle > 0 comparisons - v2 client handles can be negative.

    Entity handles in v2 multiplayer can be negative, so `handle > 0` may
    incorrectly treat valid handles as invalid. Use `handle ~= 0` instead.
    Excludes variables with names that are clearly not handles (dist, count, etc.).
    """
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        m = _HANDLE_GT_ZERO_RE.search(stripped)
        if m:
            var_name = m.group(1)
            if var_name.startswith("#"):
                continue  # #table > 0 is a length check, not handle
            if _is_non_handle_name(var_name):
                continue
            findings.append(_finding(
                "HANDLE-GT-ZERO",
                lineno,
                f"{var_name} > 0 comparison - v2 client handles can be negative; use ~= 0 instead",
                severity="warn",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check T2-7: Manual aim via QueryRaycast without GetPlayerAimInfo
# ---------------------------------------------------------------------------

_QUERY_RAYCAST_RE = re.compile(r"\bQueryRaycast\s*\(")
_GET_PLAYER_AIM_INFO_RE = re.compile(r"\bGetPlayerAimInfo\s*\(")


def check_manual_aim(source: str) -> list[dict]:
    """Info if QueryRaycast is used without GetPlayerAimInfo.

    GetPlayerAimInfo is the preferred API in v2 for weapon aim; manual
    QueryRaycast from client eye transform can desync in multiplayer.
    However, many mods use QueryRaycast for non-aim purposes (collision,
    particles, utility tools needing shape/body/normal returns) where
    GetPlayerAimInfo is not a suitable replacement.
    """
    if not _QUERY_RAYCAST_RE.search(source):
        return []
    if _GET_PLAYER_AIM_INFO_RE.search(source):
        return []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _QUERY_RAYCAST_RE.search(stripped):
            return [_finding(
                "MANUAL-AIM",
                lineno,
                "QueryRaycast() used without GetPlayerAimInfo() - "
                "consider GetPlayerAimInfo(muzzlePos, maxDist, p) for weapon aim. "
                "Note: QueryRaycast is valid for non-aim uses (collision, shape lookup). "
                "See docs/RESEARCH.md Finding #1",
                severity="info",
            )]
    return []


# ---------------------------------------------------------------------------
# Check T2-8: MakeHole usage (informational)
# ---------------------------------------------------------------------------

_MAKEHOLE_RE = re.compile(r"\bMakeHole\s*\(")


def check_makehole_damage(source: str) -> list[dict]:
    """Info finding if MakeHole is used WITHOUT QueryShot/ApplyPlayerDamage.

    MakeHole cannot damage players; guns should use Shoot() instead.
    If the file already has QueryShot or ApplyPlayerDamage, MakeHole is
    presumably used for terrain damage alongside the player damage system
    — suppress to reduce noise.
    """
    has_player_damage = bool(re.search(r"\b(QueryShot|ApplyPlayerDamage)\s*\(", source))
    if has_player_damage:
        return []
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _MAKEHOLE_RE.search(stripped):
            findings.append(_finding(
                "MAKEHOLE-DAMAGE",
                lineno,
                "MakeHole() cannot damage players in v2 - "
                "use Shoot() for weapons that should damage players. "
                "See docs/RESEARCH.md Finding #2",
                severity="info",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check T2-9: Server-side client-only effects (RC4 desync)
# ---------------------------------------------------------------------------

_BLOCK_COMMENT_RE = re.compile(r'--\[\[.*?\]\](?:--)?', re.DOTALL)


def _strip_block_comments(source: str) -> str:
    """Replace Lua --[[ ... ]] block comments with empty lines to preserve line numbers."""
    def _replace_with_newlines(match):
        return '\n' * match.group(0).count('\n')
    return _BLOCK_COMMENT_RE.sub(_replace_with_newlines, source)


_CLIENT_EFFECT_RE = re.compile(
    r"\b(SpawnParticle|PlaySound|PlayLoop|PointLight)\s*\("
)


def check_server_side_effects(source: str) -> list[dict]:
    """Warn if PlaySound/SpawnParticle/PlayLoop/PointLight inside server.* functions.

    These APIs are client-only in v2 multiplayer. When called on the server,
    they either silently fail or only execute for the host player.
    Use ClientCall() to notify clients to play effects instead.
    See docs/MP_DESYNC_PATTERNS.md RC4.
    """
    findings = []
    current_func: str | None = None
    depth = 0

    cleaned = _strip_block_comments(source)

    for lineno, raw_line in enumerate(cleaned.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        func_match = _FUNC_DEF_RE.match(stripped)
        opens = _count_opens(stripped)
        ends = _count_ends(stripped)

        if func_match and depth == 0:
            current_func = func_match.group(1)
            depth = 1 + (opens - 1) - ends
        elif depth > 0:
            depth += opens - ends

        if depth < 0:
            depth = 0

        m = _CLIENT_EFFECT_RE.search(stripped)
        if m and current_func is not None and current_func.startswith("server."):
            findings.append(_finding(
                "SERVER-EFFECT",
                lineno,
                f"{m.group(1)}() is client-only; found inside {current_func!r} — "
                f"use ClientCall() to play effects on all clients. "
                f"See docs/MP_DESYNC_PATTERNS.md RC4",
                severity="warn",
            ))

        if depth == 0:
            current_func = None

    return findings


# ---------------------------------------------------------------------------
# Check T2-10: Missing keybind hints in HUD
# ---------------------------------------------------------------------------

_RAW_SINGLE_KEY_RE = re.compile(r'InputPressed\s*\(\s*"([a-z])"')
_UI_KEYBIND_HINT_RE = re.compile(r'UiText\s*\(.*(?:LMB|RMB|MMB|Fire|Reload|Options|Press|Hold|Click|key|bind)', re.IGNORECASE)


def check_missing_interactive(source: str) -> list[dict]:
    """Warn if optionsOpen UI block has UiTextButton but no UiMakeInteractive.

    Without UiMakeInteractive(), buttons render but cannot be clicked.
    """
    if not _OPTIONS_OPEN_RE.search(source):
        return []

    ui_interactive_re = re.compile(r"\bUiMakeInteractive\s*\(")
    ui_button_re = re.compile(r"\bUiTextButton\s*\(")

    if not ui_button_re.search(source):
        return []

    if ui_interactive_re.search(source):
        return []

    # Has optionsOpen + UiTextButton but no UiMakeInteractive
    # Find the first UiTextButton line for reporting
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if ui_button_re.search(stripped):
            return [_finding(
                "MISSING-INTERACTIVE",
                lineno,
                "UiTextButton() found but no UiMakeInteractive() call - "
                "buttons render but cannot be clicked. Add UiMakeInteractive() "
                "before UiPush() in options menu. See ISSUES_AND_FIXES.md Issue #35",
                severity="warn",
            )]
    return []


def check_missing_keybind_hints(source: str) -> list[dict]:
    """Warn if 2+ single-letter raw key inputs exist but no keybind hint UiText.

    Mods that bind single-letter keys should display keybind hints so players
    know which keys to press.
    """
    raw_key_lines = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _RAW_SINGLE_KEY_RE.search(stripped):
            raw_key_lines.append(lineno)

    if len(raw_key_lines) < 2:
        return []

    if _UI_KEYBIND_HINT_RE.search(source):
        return []

    return [_finding(
        "MISSING-KEYBIND-HINTS",
        raw_key_lines[0],
        f"{len(raw_key_lines)} single-letter InputPressed() calls found but no keybind hint UiText - "
        "consider displaying keybind hints to players",
        severity="warn",
    )]


# ---------------------------------------------------------------------------
# Check 18: SetPlayerHealth swapped arguments
# ---------------------------------------------------------------------------

_SET_PLAYER_HEALTH_RE = re.compile(
    r"SetPlayerHealth\s*\(\s*([^,)]+)\s*,\s*([^,)]+)"
)


def check_set_player_health_order(source: str) -> list[dict]:
    """Catch SetPlayerHealth(p, 1) — swapped argument order.

    Correct form: SetPlayerHealth(health, player).
    If the first argument looks like a variable (not a number literal)
    and the second looks like a number literal, the args are swapped.
    """
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        m = _SET_PLAYER_HEALTH_RE.search(stripped)
        if not m:
            continue
        first_arg = m.group(1).strip()
        second_arg = m.group(2).strip()
        # First arg is variable (not number), second arg is number literal
        first_is_number = re.match(r'^-?\d+\.?\d*$', first_arg) is not None
        second_is_number = re.match(r'^-?\d+\.?\d*$', second_arg) is not None
        if not first_is_number and second_is_number:
            findings.append(_finding(
                "HEALTH-ARG-ORDER",
                lineno,
                f"SetPlayerHealth() first arg is {first_arg!r} (variable), second is {second_arg!r} (number); "
                f"correct order is SetPlayerHealth(health, player) — value first, player last",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check 19: Server-only functions in client code (generalized)
# ---------------------------------------------------------------------------

_SERVER_ONLY_FUNCS_RE = re.compile(
    r"\b(Shoot|MakeHole|Explosion|DisablePlayerInput|DisablePlayer|"
    r"SetPlayerVelocity|SetPlayerWalkingSpeed|SetPlayerHurtSpeedScale|"
    r"ApplyBodyImpulse|SetBodyVelocity|SpawnFire|Delete)\s*\("
)


_USER_FUNC_DEF_RE = re.compile(r"^\s*function\s+(\w+)\s*\(")


def check_server_only_in_client(source: str) -> list[dict]:
    """Catch server-only functions (Shoot, MakeHole, Explosion, etc.) in client.* functions.

    These functions are server-only in v2 multiplayer. Calling them from
    client code either silently fails or causes desyncs.
    Excludes user-defined functions with the same name (e.g. custom Shoot()).
    See docs/OFFICIAL_DEVELOPER_DOCS.md § Critical Gotchas #5.
    """
    # Pre-scan: collect user-defined function names to exclude
    user_defined = set()
    for line in source.splitlines():
        m = _USER_FUNC_DEF_RE.match(_strip_comment(line))
        if m:
            user_defined.add(m.group(1))

    findings = []
    current_func: str | None = None
    depth = 0

    cleaned = _strip_block_comments(source)

    for lineno, raw_line in enumerate(cleaned.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        func_match = _FUNC_DEF_RE.match(stripped)
        opens = _count_opens(stripped)
        ends = _count_ends(stripped)

        if func_match and depth == 0:
            current_func = func_match.group(1)
            depth = 1 + (opens - 1) - ends
        elif depth > 0:
            depth += opens - ends

        if depth < 0:
            depth = 0

        m = _SERVER_ONLY_FUNCS_RE.search(stripped)
        if m and current_func is not None and current_func.startswith("client."):
            # Skip SetPlayerTransform — already has its own dedicated check
            if m.group(1) == "SetPlayerTransform":
                continue
            # Skip user-defined functions with same name (not the engine API)
            if m.group(1) in user_defined:
                continue
            findings.append(_finding(
                "CLIENT-SERVER-FUNC",
                lineno,
                f"{m.group(1)}() is server-only; found inside {current_func!r} — "
                f"move to server.* function or use ServerCall(). "
                f"See docs/OFFICIAL_DEVELOPER_DOCS.md § Critical Gotchas #5",
                severity="warn",
            ))

        if depth == 0:
            current_func = None

    return findings


# ---------------------------------------------------------------------------
# Check 20: Per-tick RPC calls (network flooding)
# ---------------------------------------------------------------------------

_SERVER_CALL_RE = re.compile(r"\b(ServerCall|ClientCall)\s*\(")

_TICK_FUNC_NAMES = {
    "server.tick", "server.update", "server.tickPlayer",
    "client.tick", "client.update", "client.tickPlayer",
}


_INPUT_GUARD_RE = re.compile(
    r"\bInput(?:Pressed|Down|Released)\s*\("
)


def check_per_tick_rpc(source: str) -> list[dict]:
    """Warn if ServerCall/ClientCall appear inside tick/update without guards.

    RPC calls in tick/update flood the reliable network channel, causing
    lag spikes and input delay. Use registry sync (SetFloat with sync=true)
    for continuous state instead.

    Skips RPC calls guarded by:
    - InputPressed/InputDown/InputReleased within previous 5 lines (event-driven)
    - State-change patterns (~= was/old/last/prev) within previous 3 lines (transition-only)
    See docs/OFFICIAL_DEVELOPER_DOCS.md § Critical Gotchas #8.
    """
    findings = []
    current_func: str | None = None
    depth = 0

    cleaned = _strip_block_comments(source)
    lines = cleaned.splitlines()

    state_change_re = re.compile(r"~=\s*(was|old|last|prev)\w*", re.IGNORECASE)

    for lineno, raw_line in enumerate(lines, 1):
        stripped = _strip_comment(raw_line)
        func_match = _FUNC_DEF_RE.match(stripped)
        opens = _count_opens(stripped)
        ends = _count_ends(stripped)

        if func_match and depth == 0:
            current_func = func_match.group(1)
            depth = 1 + (opens - 1) - ends
        elif depth > 0:
            depth += opens - ends

        if depth < 0:
            depth = 0

        m = _SERVER_CALL_RE.search(stripped)
        if m and current_func is not None and current_func in _TICK_FUNC_NAMES:
            # Check if guarded by InputPressed/InputDown within 8 lines
            window_start = max(0, lineno - 9)
            window = lines[window_start:lineno]
            has_input_guard = any(
                _INPUT_GUARD_RE.search(_strip_comment(l)) for l in window
            )
            # Check if guarded by state-change pattern within 3 lines
            sc_window = lines[max(0, lineno - 4):lineno]
            has_state_change_guard = any(
                state_change_re.search(_strip_comment(l)) for l in sc_window
            )
            if not has_input_guard and not has_state_change_guard:
                findings.append(_finding(
                    "PER-TICK-RPC",
                    lineno,
                    f"{m.group(1)}() inside {current_func!r} without input guard — "
                    f"RPC every tick floods the network. "
                    f"Use SetFloat/SetBool with sync=true for continuous state. "
                    f"See docs/PER_TICK_RPC_FIX_GUIDE.md for fix patterns",
                    severity="warn",
                ))

        if depth == 0:
            current_func = None

    return findings


# ---------------------------------------------------------------------------
# Check 21: Missing #version 2 header
# ---------------------------------------------------------------------------

_VERSION2_RE = re.compile(r"^\s*#version\s+2\b", re.MULTILINE)


def check_missing_version2(source: str) -> list[dict]:
    """Warn if a script has RegisterTool/server./client. but no #version 2 header.

    Without #version 2, scripts are silently disabled in multiplayer sessions.
    Excludes include/library files that define (not use) v2 functions.
    See docs/OFFICIAL_DEVELOPER_DOCS.md § V2 Multiplayer Architecture.
    """
    if _VERSION2_RE.search(source):
        return []

    # Skip files that are include/library files (they define functions, not use them)
    if re.search(r"^\s*function\s+Players\s*\(", source, re.MULTILINE):
        return []  # This is the player.lua include itself

    # Only flag if the file looks like it's trying to be a v2 mod
    # Match function calls (with parens) not function definitions
    has_v2_patterns = bool(re.search(
        r"\bfunction\s+(server|client)\.\w+\s*\(|"
        r"\bRegisterTool\s*\(",
        source
    ))
    if not has_v2_patterns:
        return []

    return [_finding(
        "MISSING-VERSION2",
        1,
        "Script uses v2 patterns (server.*/client.*/RegisterTool) but has no "
        "'#version 2' header — script will be SILENTLY DISABLED in multiplayer. "
        "See docs/OFFICIAL_DEVELOPER_DOCS.md § V2 Multiplayer Architecture",
    )]


# ---------------------------------------------------------------------------
# Check 22: Shoot() missing playerId/toolId (no kill attribution)
# ---------------------------------------------------------------------------

_ENGINE_SHOOT_RE = re.compile(r"(?<!\.)\bShoot\s*\(")


def _count_top_level_commas(s: str) -> int:
    """Count commas NOT inside nested parentheses."""
    depth = 0
    count = 0
    in_string = False
    escape = False
    for ch in s:
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            count += 1
    return count


def check_shoot_missing_attribution(source: str) -> list[dict]:
    """Flag Shoot() calls with fewer than 7 args (missing playerId/toolId).

    Full signature: Shoot(pos, dir, type, damage, range, playerId, toolId)
    Without playerId and toolId, kills show as 'unknown' in the kill feed.
    Skips user-defined Shoot functions.
    See docs/OFFICIAL_DEVELOPER_DOCS.md § Weapon & Combat API.
    """
    # Pre-scan: skip if user defines their own Shoot function
    user_defined = set()
    for line in source.splitlines():
        m = _USER_FUNC_DEF_RE.match(_strip_comment(line))
        if m:
            user_defined.add(m.group(1))
    if "Shoot" in user_defined:
        return []

    findings = []
    cleaned = _strip_block_comments(source)
    lines = cleaned.splitlines()

    for lineno, raw_line in enumerate(lines, 1):
        stripped = _strip_comment(raw_line)
        if not _ENGINE_SHOOT_RE.search(stripped):
            continue

        # Extract args: everything after "Shoot(" up to matching ")"
        idx = stripped.find("Shoot(")
        if idx < 0:
            continue
        after = stripped[idx + 6:]  # after "Shoot("
        # Find matching close paren
        depth = 1
        end = -1
        for i, ch in enumerate(after):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            continue  # multi-line call, skip

        args_str = after[:end]
        num_commas = _count_top_level_commas(args_str)
        # 7 args = 6 commas; fewer means missing params
        if num_commas < 6:
            findings.append(_finding(
                "SHOOT-NO-ATTRIB",
                lineno,
                f"Shoot() has {num_commas + 1} args (expected 7) — missing "
                f"playerId and/or toolId for kill attribution. "
                f"See docs/OFFICIAL_DEVELOPER_DOCS.md § Weapon & Combat API",
                severity="info",
            ))

    return findings


# ===========================================================================
# Aggregation
# ===========================================================================

TIER1_CHECKS = [
    check_ipairs_iterator,
    check_raw_key_player,
    check_tool_enabled_order,
    check_alttool,
    check_goto_label,
    check_mousedx,
    check_set_player_transform_client,
    check_draw_not_client,
    check_set_player_health_order,
    check_missing_version2,
]

TIER2_CHECKS = [
    check_missing_ammo_display,
    check_missing_tool_ammo,
    check_missing_ammo_pickup,
    check_missing_options_guard,
    check_missing_options_sync,
    check_missing_interactive,
    check_handle_gt_zero,
    check_manual_aim,
    check_makehole_damage,
    check_server_side_effects,
    check_missing_keybind_hints,
    check_server_only_in_client,
    check_per_tick_rpc,
    check_shoot_missing_attribution,
]


_LINT_OK_RE = re.compile(r'--\s*@lint-ok\s+([\w-]+(?:\s*,\s*[\w-]+)*)')


def _lint_suppressions(source: str) -> dict[int, set[str]]:
    """Extract @lint-ok suppression tags per line.

    Usage in Lua: ``-- @lint-ok SERVER-EFFECT`` on same line suppresses that check.
    Multiple checks: ``-- @lint-ok SERVER-EFFECT, MANUAL-AIM``
    """
    suppressions: dict[int, set[str]] = {}
    for lineno, line in enumerate(source.splitlines(), 1):
        m = _LINT_OK_RE.search(line)
        if m:
            checks = {c.strip().upper() for c in m.group(1).split(",")}
            suppressions[lineno] = checks
    return suppressions


def lint_source(source: str, filename: str, tier: str = "all") -> list[dict]:
    """Run lint checks on a single Lua source string.

    Args:
        source:   Lua source code.
        filename: File path for filling the 'file' field in findings.
        tier:     "all" (default), "1" (tier-1 only), or "2" (tier-2 only).
                  Any other value is treated as "all" for backward compatibility.

    Returns a list of finding dicts, each with:
      check, line, severity, file, detail

    Supports ``-- @lint-ok CHECK-ID`` comments to suppress specific checks per line.
    """
    checks = []
    if tier in ("all", "1"):
        checks.extend(TIER1_CHECKS)
    if tier in ("all", "2"):
        checks.extend(TIER2_CHECKS)
    if not checks:
        # Backward-compat: unknown tier string → run everything
        checks = TIER1_CHECKS + TIER2_CHECKS

    suppressions = _lint_suppressions(source)

    results = []
    for check_fn in checks:
        findings = check_fn(source)
        for f in findings:
            f["file"] = filename
            # Filter suppressed findings
            line_sups = suppressions.get(f["line"], set())
            if f["check"].upper() not in line_sups:
                results.append(f)
    return results


# ===========================================================================
# Click CLI
# ===========================================================================

import click
from tools.common import discover_mods, read_lua_files


def check_info_txt(mod_dir) -> list[dict]:
    """Check info.txt for required multiplayer fields.

    Returns findings for missing version=2 or missing required fields.
    """
    info_path = mod_dir / "info.txt"
    if not info_path.exists():
        return [_finding("MISSING-INFO-TXT", 1, "No info.txt found in mod folder", severity="error")]

    try:
        content = info_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    findings = []
    lines = content.splitlines()
    has_version2 = False
    has_name = False

    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if re.match(r"version\s*=\s*2\b", stripped):
            has_version2 = True
        if re.match(r"name\s*=\s*.+", stripped):
            has_name = True

    if not has_name:
        findings.append({
            "check": "INFO-MISSING-NAME",
            "line": 1,
            "severity": "warn",
            "file": "info.txt",
            "detail": "info.txt missing 'name = ...' field",
        })

    if not has_version2:
        # Check if any lua file uses v2 patterns (to avoid flagging v1 mods)
        has_v2_lua = False
        for lua_file in mod_dir.rglob("*.lua"):
            try:
                src = lua_file.read_text(encoding="utf-8", errors="replace")
                if re.search(r"#version\s+2\b", src):
                    has_v2_lua = True
                    break
            except Exception:
                pass

        if has_v2_lua:
            findings.append({
                "check": "INFO-MISSING-VERSION2",
                "line": 1,
                "severity": "error",
                "file": "info.txt",
                "detail": "Lua scripts have #version 2 but info.txt lacks 'version = 2' — "
                          "mod will NOT be recognized as multiplayer-compatible. "
                          "See docs/OFFICIAL_DEVELOPER_DOCS.md § info.txt Format",
            })

    return findings


@click.command("lint")
@click.option("--mod", "mod_name", default=None, help="Single mod folder name")
@click.option("--tier", type=click.Choice(["1", "2", "all"]), default="all")
@click.option("--json-output", "json_out", is_flag=True, help="JSON output")
def lint_cli(mod_name, tier, json_out):
    """Scan mods for known bugs and missing features."""
    mods = discover_mods(mod_name=mod_name)
    if not mods:
        click.echo(f"No mods found{f' matching {mod_name!r}' if mod_name else ''}")
        raise SystemExit(1)

    all_results = {}
    has_errors = False

    for mod_dir in mods:
        mod_results = []

        # Check info.txt (tier 1)
        if tier in ("all", "1"):
            info_findings = check_info_txt(mod_dir)
            mod_results.extend(info_findings)
            if any(r["severity"] == "error" for r in info_findings):
                has_errors = True

        for rel_path, source in read_lua_files(mod_dir):
            if rel_path == "options.lua":
                continue
            # Skip disabled options files and engine include copies
            if rel_path.startswith("options") or "/include/" in rel_path or "\\include\\" in rel_path:
                continue
            file_results = lint_source(source, rel_path, tier=tier)
            mod_results.extend(file_results)
            if any(r["severity"] == "error" for r in file_results):
                has_errors = True
        all_results[mod_dir.name] = mod_results

    if json_out:
        import json
        click.echo(json.dumps(all_results, indent=2))
    else:
        _print_results(all_results)

    raise SystemExit(1 if has_errors else 0)


def _print_results(all_results):
    total = 0
    for mod_name, results in sorted(all_results.items()):
        if not results:
            continue
        for r in results:
            total += 1
            tag = {"error": "FAIL", "warn": "WARN", "info": "INFO"}[r["severity"]]
            click.echo(f"  [{tag}] {mod_name}/{r['file']}:{r['line']}  {r['check']}  {r['detail']}")

    pass_count = sum(1 for r in all_results.values() if not r)
    fail_count = len(all_results) - pass_count
    click.echo(f"\n{len(all_results)} mods scanned: {pass_count} clean, {fail_count} with findings, {total} total findings")


if __name__ == "__main__":
    lint_cli()
