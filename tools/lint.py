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

    do_count = len(_DO_RE.findall(line))
    do_count -= len(_FOR_RE.findall(line))
    do_count -= len(_WHILE_RE.findall(line))
    if do_count > 0:
        count += do_count

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
_OPTIONS_OPEN_RE = re.compile(r"\boptionsOpen\b")


def check_missing_options_guard(source: str) -> list[dict]:
    """Warn if usetool input is used without nearby optionsOpen guard.

    Without the guard, the tool fires while the options menu is open.
    The guard should appear within 3 lines before the usetool check,
    or on the same line.
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

_SERVER_SET_OPTIONS_RE = re.compile(r"\bserver\.setOptionsOpen\b")


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

_HANDLE_GT_ZERO_RE = re.compile(r"\w+\s*>\s*0\s+then\b")


def check_handle_gt_zero(source: str) -> list[dict]:
    """Warn on handle > 0 comparisons - v2 client handles can be negative.

    Entity handles in v2 multiplayer can be negative, so `handle > 0` may
    incorrectly treat valid handles as invalid. Use `handle ~= 0` instead.
    """
    findings = []
    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        if _HANDLE_GT_ZERO_RE.search(stripped):
            findings.append(_finding(
                "HANDLE-GT-ZERO",
                lineno,
                "handle > 0 comparison - v2 client handles can be negative; use ~= 0 instead",
                severity="warn",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check T2-7: Manual aim via QueryRaycast without GetPlayerAimInfo
# ---------------------------------------------------------------------------

_QUERY_RAYCAST_RE = re.compile(r"\bQueryRaycast\s*\(")
_GET_PLAYER_AIM_INFO_RE = re.compile(r"\bGetPlayerAimInfo\s*\(")


def check_manual_aim(source: str) -> list[dict]:
    """Warn if QueryRaycast is used without GetPlayerAimInfo.

    GetPlayerAimInfo is the preferred API in v2; manual QueryRaycast
    from client eye transform can desync in multiplayer.
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
                "use GetPlayerAimInfo(muzzlePos, maxDist, p) for multiplayer-safe aiming. "
                "See docs/RESEARCH.md Finding #1",
                severity="warn",
            )]
    return []


# ---------------------------------------------------------------------------
# Check T2-8: MakeHole usage (informational)
# ---------------------------------------------------------------------------

_MAKEHOLE_RE = re.compile(r"\bMakeHole\s*\(")


def check_makehole_damage(source: str) -> list[dict]:
    """Info finding if MakeHole is used.

    MakeHole cannot damage players; guns should use Shoot() instead.
    Many mods use MakeHole legitimately, so this is informational only.
    """
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
# Check T2-9: Missing keybind hints in HUD
# ---------------------------------------------------------------------------

_RAW_SINGLE_KEY_RE = re.compile(r'InputPressed\s*\(\s*"([a-z])"')
_UI_KEYBIND_HINT_RE = re.compile(r'UiText\s*\(.*(?:LMB|RMB|key|bind|press)', re.IGNORECASE)


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
]

TIER2_CHECKS = [
    check_missing_ammo_display,
    check_missing_tool_ammo,
    check_missing_ammo_pickup,
    check_missing_options_guard,
    check_missing_options_sync,
    check_handle_gt_zero,
    check_manual_aim,
    check_makehole_damage,
    check_missing_keybind_hints,
]


def lint_source(source: str, filename: str, tier: str = "all") -> list[dict]:
    """Run lint checks on a single Lua source string.

    Args:
        source:   Lua source code.
        filename: File path for filling the 'file' field in findings.
        tier:     "all" (default), "1" (tier-1 only), or "2" (tier-2 only).
                  Any other value is treated as "all" for backward compatibility.

    Returns a list of finding dicts, each with:
      check, line, severity, file, detail
    """
    checks = []
    if tier in ("all", "1"):
        checks.extend(TIER1_CHECKS)
    if tier in ("all", "2"):
        checks.extend(TIER2_CHECKS)
    if not checks:
        # Backward-compat: unknown tier string → run everything
        checks = TIER1_CHECKS + TIER2_CHECKS

    results = []
    for check_fn in checks:
        findings = check_fn(source)
        for f in findings:
            f["file"] = filename
        results.extend(findings)
    return results


# ===========================================================================
# Click CLI
# ===========================================================================

import click
from tools.common import discover_mods, read_lua_files


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
        for rel_path, source in read_lua_files(mod_dir):
            if rel_path == "options.lua":
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
