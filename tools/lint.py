"""Tier-1 lint checks for Teardown v2 multiplayer mod compatibility.

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

def _finding(check_id: str, lineno: int, detail: str) -> dict:
    return {
        "check": check_id,
        "line": lineno,
        "severity": "error",
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
                f"ipairs() on iterator {m.group(1)}() — use 'for p in {m.group(1)}() do' instead",
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
                    f"{func_name}(\"{key_name}\", p) — raw key with player arg silently fails; "
                    f"use action key or InputPressed(\"{key_name}\") with isLocal check",
                ))
    return findings


# ---------------------------------------------------------------------------
# Check 3: SetToolEnabled wrong argument order
# ---------------------------------------------------------------------------

_SET_TOOL_ENABLED_RE = re.compile(r"SetToolEnabled\s*\(\s*([^\s,)]+)")


def check_tool_enabled_order(source: str) -> list[dict]:
    """Catch SetToolEnabled(p, 'id', true) — wrong argument order.

    Correct form: SetToolEnabled("toolid", true, p) — first arg must be a string literal.
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
    """Catch "alttool" anywhere in source — should be "rmb" instead."""
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
    """Catch "mousedx" and "mousedy" key names — use "camerax"/"cameray" instead."""
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
    """Catch bare function draw() at top level — must be client.draw() in v2."""
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


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def lint_source(source: str, filename: str, tier: str = "all") -> list[dict]:
    """Run all tier-1 checks on a single Lua source string.

    Returns a list of finding dicts, each with:
      check, line, severity, file, detail
    """
    results = []
    checks = [
        check_ipairs_iterator,
        check_raw_key_player,
        check_tool_enabled_order,
        check_alttool,
        check_goto_label,
        check_mousedx,
        check_set_player_transform_client,
        check_draw_not_client,
    ]
    for check_fn in checks:
        findings = check_fn(source)
        for f in findings:
            f["file"] = filename
        results.extend(findings)
    return results
