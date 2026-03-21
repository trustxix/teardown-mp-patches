"""Batch auto-fixer for Teardown MP mod compatibility issues.

Each fixer is a pure function: fix_X(source: str) -> str.
Returns the input unchanged if no fix is needed.

apply_fixes(source, only=None) -> (fixed_source, list[change_descriptions])
"""

from __future__ import annotations

import re
from pathlib import Path

import click

from tools.common import RAW_KEYS, discover_mods, read_lua_files


# ---------------------------------------------------------------------------
# Fixer 1: ipairs() on Players() iterators
# ---------------------------------------------------------------------------

_IPAIRS_ITER_RE = re.compile(
    r"for\s+_\s*,\s*(\w+)\s+in\s+ipairs\s*\(\s*(Players|PlayersAdded|PlayersRemoved)\s*\(\s*\)\s*\)\s+do"
)


def fix_ipairs_iterator(source: str) -> str:
    """Remove ipairs wrapper from Player iterator loops.

    ``for _, p in ipairs(Players()) do`` → ``for p in Players() do``
    """
    return _IPAIRS_ITER_RE.sub(r"for \1 in \2() do", source)


# ---------------------------------------------------------------------------
# Fixer 2: mousedx / mousedy → camerax / cameray
# ---------------------------------------------------------------------------

_MOUSEDX_RE = re.compile(r'InputValue\s*\(\s*"mousedx"(?:\s*,\s*[^)]+)?\s*\)')
_MOUSEDY_RE = re.compile(r'InputValue\s*\(\s*"mousedy"(?:\s*,\s*[^)]+)?\s*\)')


def fix_mousedx(source: str) -> str:
    """Replace deprecated mouse delta inputs with camera axis equivalents.

    ``InputValue("mousedx")`` → ``InputValue("camerax") * 180 / math.pi``
    ``InputValue("mousedy")`` → ``InputValue("cameray") * 180 / math.pi``
    """
    result = _MOUSEDX_RE.sub('InputValue("camerax") * 180 / math.pi', source)
    result = _MOUSEDY_RE.sub('InputValue("cameray") * 180 / math.pi', result)
    return result


# ---------------------------------------------------------------------------
# Fixer 3: "alttool" → "rmb"
# ---------------------------------------------------------------------------

_ALTTOOL_RE = re.compile(r'"alttool"')


def fix_alttool(source: str) -> str:
    """Replace wrong key name "alttool" with correct "rmb"."""
    return _ALTTOOL_RE.sub('"rmb"', source)


# ---------------------------------------------------------------------------
# Fixer 3b: Raw key + player param → remove player param
# ---------------------------------------------------------------------------

_RAW_KEY_PLAYER_RE = re.compile(
    r"(\b(?:InputPressed|InputReleased|InputDown|InputValue)"
    r"\s*\(\s*\"([^\"]+)\")\s*,\s*[^)]+\)"
)


def fix_raw_key_player(source: str) -> str:
    """Remove player param from raw key input calls.

    ``InputPressed("rmb", p)`` → ``InputPressed("rmb")``

    Raw keys silently fail with a player parameter in v2 MP. Removing the
    param makes them work for the local player only (the correct behavior).
    Action keys (usetool, interact, etc.) are left unchanged.
    """
    def _replace(m: re.Match) -> str:
        key_name = m.group(2)
        if key_name in RAW_KEYS:
            return m.group(1) + ")"
        return m.group(0)  # Not a raw key — leave unchanged

    return _RAW_KEY_PLAYER_RE.sub(_replace, source)


# ---------------------------------------------------------------------------
# Fixer 4: function draw( → function client.draw( at top level
# ---------------------------------------------------------------------------

# Matches bare `function draw(` at the start of a line (not `function foo.draw(`)
_BARE_DRAW_RE = re.compile(r"^(\s*)function\s+draw\s*(\()", re.MULTILINE)

# Block depth tracking patterns (reuse logic from validate.py)
_FUNC_KW_RE = re.compile(r"\bfunction\b")
_IF_KW_RE = re.compile(r"\bif\b")
_FOR_KW_RE = re.compile(r"\bfor\b")
_WHILE_KW_RE = re.compile(r"\bwhile\b")
_REPEAT_KW_RE = re.compile(r"\brepeat\b")
_DO_KW_RE = re.compile(r"\bdo\b")
_END_KW_RE = re.compile(r"\bend\b")
_UNTIL_KW_RE = re.compile(r"\buntil\b")


def _block_opens(line: str) -> int:
    count = (
        len(_FUNC_KW_RE.findall(line))
        + len(_IF_KW_RE.findall(line))
        + len(_FOR_KW_RE.findall(line))
        + len(_WHILE_KW_RE.findall(line))
        + len(_REPEAT_KW_RE.findall(line))
    )
    # Standalone `do` blocks only
    do_count = len(_DO_KW_RE.findall(line)) - len(_FOR_KW_RE.findall(line)) - len(_WHILE_KW_RE.findall(line))
    if do_count > 0:
        count += do_count
    return count


def _block_ends(line: str) -> int:
    return len(_END_KW_RE.findall(line)) + len(_UNTIL_KW_RE.findall(line))


# Matches the top-level `function draw(` pattern we want to replace
_TOP_DRAW_LINE_RE = re.compile(r"^(\s*)function\s+draw\s*(\(.*)")


def fix_draw_func(source: str) -> str:
    """Fix top-level ``function draw(`` → ``function client.draw(``.

    Only replaces bare ``draw`` at block depth 0, not ``someObj.draw``.
    """
    lines = source.splitlines(keepends=True)
    depth = 0
    result = []
    changed = False

    for line in lines:
        stripped = line.rstrip("\n\r")
        # Check if this line is a bare `function draw(` at depth 0
        # Also accept non-indented draw() at any depth (depth tracker can lose sync)
        m = _TOP_DRAW_LINE_RE.match(stripped)
        if m and (depth == 0 or not m.group(1)):
            if True:
                indent = m.group(1)
                rest = m.group(2)  # "(..." portion
                new_line = f"{indent}function client.draw{rest}"
                # Preserve original line ending
                ending = line[len(stripped):]
                result.append(new_line + ending)
                changed = True
                # Update depth for this line (function keyword opens a block)
                opens = _block_opens(stripped)
                ends = _block_ends(stripped)
                depth = 1 + (opens - 1) - ends
                continue

        # Track depth
        opens = _block_opens(stripped)
        ends = _block_ends(stripped)

        if depth == 0:
            # Not inside a function; this line may open one
            func_match = re.match(r"^\s*function\s+", stripped)
            if func_match:
                depth = 1 + (opens - 1) - ends
            # else depth stays 0
        else:
            depth += opens - ends
            if depth < 0:
                depth = 0

        result.append(line)

    return "".join(result) if changed else source


# ---------------------------------------------------------------------------
# Fixer 5: entity handle comparison handle > 0 → handle ~= 0
# ---------------------------------------------------------------------------

# Matches: <word> > 0 then  (entity handle check pattern)
# Include optional # prefix to detect length checks (#table > 0)
_HANDLE_GT_RE = re.compile(r"(\#?\w+)\s*>\s*0\s+then")

# Import non-handle detection from lint.py
from tools.lint import _is_non_handle_name


_LINT_OK_HANDLE_RE = re.compile(r"@lint-ok\b.*\bHANDLE-GT-ZERO\b")


def fix_handle_gt(source: str) -> str:
    """Fix entity handle comparison: ``handle > 0 then`` → ``handle ~= 0 then``.

    In Teardown v2, client-side entity handles can be negative, so ``> 0``
    incorrectly treats valid negative handles as nil/invalid.
    Skips variables that are clearly not entity handles (dist, count, etc.).
    Skips lines with ``@lint-ok HANDLE-GT-ZERO`` annotations.
    """
    lines = source.split("\n")
    for i, line in enumerate(lines):
        if _LINT_OK_HANDLE_RE.search(line):
            continue  # respect @lint-ok annotation
        def _replace(m):
            if _is_non_handle_name(m.group(1)):
                return m.group(0)
            return m.group(1) + " ~= 0 then"
        lines[i] = _HANDLE_GT_RE.sub(_replace, line)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Fixer 6: inject missing ammo display hide after RegisterTool
# ---------------------------------------------------------------------------

_REGISTER_TOOL_RE = re.compile(
    r'^([ \t]*)RegisterTool\s*\(\s*"([^"]+)"[^\n]*\)',
    re.MULTILINE,
)


def fix_ammo_display(source: str) -> str:
    """Inject ``SetString("game.tool.<id>.ammo.display", "")`` after RegisterTool.

    Only injects when the line is absent from the file for that tool ID.
    """
    result_parts: list[str] = []
    last_end = 0
    changed = False

    for m in _REGISTER_TOOL_RE.finditer(source):
        indent = m.group(1)
        tool_id = m.group(2)
        ammo_key = f'game.tool.{tool_id}.ammo.display'
        inject_line = f'{indent}SetString("{ammo_key}", "")'

        # Check if the display key is already anywhere in the source
        if ammo_key in source:
            result_parts.append(source[last_end:m.end()])
            last_end = m.end()
            continue

        # Append everything up to and including the RegisterTool line
        result_parts.append(source[last_end:m.end()])

        # Find the end of the current line (include the newline char if present)
        pos = m.end()
        newline = ""
        if pos < len(source) and source[pos] == "\n":
            newline = "\n"
            pos += 1
        elif pos + 1 < len(source) and source[pos:pos + 2] == "\r\n":
            newline = "\r\n"
            pos += 2

        result_parts.append(newline + inject_line)
        last_end = m.end() + len(newline)
        changed = True

    if not changed:
        return source

    result_parts.append(source[last_end:])
    return "".join(result_parts)


# ---------------------------------------------------------------------------
# Fixer 7: QueryShot player=0 truthy guard (Issue #47)
# ---------------------------------------------------------------------------

_APD_RE = re.compile(r"\bApplyPlayerDamage\s*\(\s*(\w+)")


def fix_queryshot_player_guard(source: str) -> str:
    """Fix ``if player then`` → ``if player ~= 0 then`` near ApplyPlayerDamage.

    QueryShot returns player=0 for non-player hits. Lua 0 is truthy, so
    ``if player then`` passes and damages the host. See Issue #47.
    """
    lines = source.splitlines(keepends=True)
    changed = False

    for i, line in enumerate(lines):
        m = _APD_RE.search(line)
        if not m:
            continue
        var = m.group(1)
        # Look back up to 3 lines for truthy guard
        already_safe = False
        for j in range(max(0, i - 3), i + 1):
            # Find `if ... then` containing the variable
            if_then = re.search(r"\bif\b(.+?)\bthen\b", lines[j])
            if not if_then:
                continue
            condition = if_then.group(1)
            # Check if var appears in condition without proper guard
            var_re = re.compile(r"\b" + re.escape(var) + r"\b")
            if not var_re.search(condition):
                continue
            safe_re = re.compile(r"\b" + re.escape(var) + r"\s*~=\s*0|\b" + re.escape(var) + r"\s*>\s*0")
            if safe_re.search(condition):
                already_safe = True
                break  # found a proper guard — no fix needed
            # Insert `~= 0` after the variable in the condition
            # Replace first bare `var` with `var ~= 0` (not already guarded)
            fix_re = re.compile(r"\b" + re.escape(var) + r"\b(?!\s*~=)(?!\s*>)")
            new_line = fix_re.sub(var + " ~= 0", lines[j], count=1)
            if new_line != lines[j]:
                lines[j] = new_line
                changed = True
                break  # fixed one — done for this ApplyPlayerDamage

    return "".join(lines) if changed else source


# ---------------------------------------------------------------------------
# Fixer 8: Add missing #version 2 header
# ---------------------------------------------------------------------------

_VERSION2_HEADER_RE = re.compile(r"^\s*#version\s+2\b", re.MULTILINE)
_V2_PATTERN_RE = re.compile(
    r"\bfunction\s+(server|client)\.\w+\s*\(|\bRegisterTool\s*\("
)


def fix_missing_version2(source: str) -> str:
    """Add ``#version 2`` header to scripts that use v2 patterns but lack it.

    Without #version 2, scripts are silently disabled in multiplayer.
    Only adds the header if the file has server.*/client.*/RegisterTool patterns.
    """
    if _VERSION2_HEADER_RE.search(source):
        return source  # Already has #version 2
    if not _V2_PATTERN_RE.search(source):
        return source  # Not a v2 script
    # Skip include/library files (define Players() iterator)
    if re.search(r"^\s*function\s+Players\s*\(", source, re.MULTILINE):
        return source
    return "#version 2\n" + source


# ---------------------------------------------------------------------------
# Fixer 10: missing PlayersRemoved cleanup loop
# ---------------------------------------------------------------------------

_PLAYERS_ADDED_BLOCK_RE = re.compile(
    r"([ \t]*)(for\s+\w+\s+in\s+PlayersAdded\s*\(\s*\)\s+do\b.*?end)",
    re.DOTALL,
)
_PLAYERS_REMOVED_RE = re.compile(r"PlayersRemoved\s*\(\s*\)")


def fix_missing_players_removed(source: str) -> str:
    """Insert an empty PlayersRemoved() loop after PlayersAdded() blocks.

    Only runs if the file has PlayersAdded() but no PlayersRemoved().
    The inserted loop is a skeleton — manual cleanup code must be added.
    """
    if _PLAYERS_REMOVED_RE.search(source):
        return source  # Already has PlayersRemoved
    if not re.search(r"PlayersAdded\s*\(\s*\)", source):
        return source  # No PlayersAdded to pair with

    # Find the variable name used in the PlayersAdded loop
    m = re.search(r"for\s+(\w+)\s+in\s+PlayersAdded\s*\(\s*\)", source)
    if not m:
        return source
    var = m.group(1)

    # Insert a PlayersRemoved loop after the first PlayersAdded block
    def insert_removed(match):
        indent = match.group(1)
        block = match.group(2)
        removed_loop = (
            f"\n{indent}for {var} in PlayersRemoved() do\n"
            f"{indent}    -- TODO: clean up per-player state for {var}\n"
            f"{indent}end"
        )
        return block + removed_loop

    return _PLAYERS_ADDED_BLOCK_RE.sub(insert_removed, source, count=1)


# ---------------------------------------------------------------------------
# Fixer 11: Add MOD/ prefix to asset paths missing it (Issue #63)
# ---------------------------------------------------------------------------

# Matches LoadSound/LoadLoop/LoadSprite/LoadImage("path/file.ext")
_ASSET_LOAD_FIX_RE = re.compile(
    r'(\bLoadSound|\bLoadLoop|\bLoadSprite|\bLoadImage)'
    r'(\s*\(\s*)"([^"]+)"'
)
_UI_IMAGE_FIX_RE = re.compile(
    r'(\bUiImage)(\s*\(\s*)"([^"]+)"'
)

# Engine built-in prefixes that don't need MOD/
_BUILTIN_PREFIXES = (
    "ui/", "explosion/", "script/", "LEVEL/", "RAW:", "MOD/",
    "gfx/", "font/", "menu/",
    "dirt/", "glass/", "wood/", "masonry/", "metal/", "plastic/", "ice/",
    "foliage/", "rock/", "heavy/", "impact/",
    "tools/", "snd/", "vehicle/",
    "data/", "timer/",
)


def fix_missing_mod_prefix(source: str) -> str:
    """Add MOD/ prefix to asset Load*/UiImage paths that are missing it."""
    if "#version 2" not in source:
        return source

    def _fix_load(m: re.Match) -> str:
        func, paren, path = m.group(1), m.group(2), m.group(3)
        if not path or "/" not in path:
            return m.group(0)  # bare filename = engine built-in
        if any(path.startswith(p) for p in _BUILTIN_PREFIXES):
            return m.group(0)
        if ".." in path:
            return m.group(0)  # dynamic concatenation
        return f'{func}{paren}"MOD/{path}"'

    def _fix_ui(m: re.Match) -> str:
        func, paren, path = m.group(1), m.group(2), m.group(3)
        if not path or "/" not in path:
            return m.group(0)
        if any(path.startswith(p) for p in _BUILTIN_PREFIXES):
            return m.group(0)
        if ".." in path:
            return m.group(0)
        return f'{func}{paren}"MOD/{path}"'

    result = source
    # Process line by line to skip comments
    lines = result.split('\n')
    fixed_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('--'):
            fixed_lines.append(line)
            continue
        if '@lint-ok' in line or '@deepcheck-ok' in line:
            fixed_lines.append(line)
            continue
        line = _ASSET_LOAD_FIX_RE.sub(_fix_load, line)
        line = _UI_IMAGE_FIX_RE.sub(_fix_ui, line)
        fixed_lines.append(line)
    return '\n'.join(fixed_lines)


# ---------------------------------------------------------------------------
# apply_fixes — orchestrator
# ---------------------------------------------------------------------------

# Registry of all fixers: (fix_id, fixer_fn, description_template)
_FIXERS: list[tuple[str, callable, str]] = [
    ("ipairs-iterator", fix_ipairs_iterator, "removed ipairs() wrapper from Player iterator"),
    ("mousedx",         fix_mousedx,         "replaced mousedx/mousedy with camerax/cameray"),
    ("alttool",         fix_alttool,         'replaced "alttool" with "rmb"'),
    ("raw-key-player",  fix_raw_key_player,  "removed player param from raw key input calls"),
    ("draw-func",       fix_draw_func,       "renamed top-level draw() to client.draw()"),
    ("handle-gt",       fix_handle_gt,       "replaced handle > 0 with handle ~= 0"),
    ("ammo-display",    fix_ammo_display,    "injected SetString ammo.display after RegisterTool"),
    ("queryshot-guard", fix_queryshot_player_guard, "fixed QueryShot player=0 truthy guard (Issue #47)"),
    ("missing-version2", fix_missing_version2, "added #version 2 header"),
    ("missing-players-removed", fix_missing_players_removed, "added PlayersRemoved() cleanup loop skeleton"),
    ("missing-mod-prefix", fix_missing_mod_prefix, "added MOD/ prefix to asset paths (Issue #63)"),
]


def apply_fixes(
    source: str,
    only: list[str] | None = None,
) -> tuple[str, list[str]]:
    """Run all (or a subset of) fixers on *source*.

    Parameters
    ----------
    source:
        Raw Lua source text.
    only:
        Optional list of fix IDs to run (e.g. ``["alttool", "mousedx"]``).
        When *None*, all fixers are run.

    Returns
    -------
    (fixed_source, changes)
        *changes* is a list of human-readable descriptions of what was changed.
        Empty list means no changes were made and *fixed_source* == *source*.
    """
    current = source
    changes: list[str] = []

    for fix_id, fixer_fn, description in _FIXERS:
        if only is not None and fix_id not in only:
            continue
        result = fixer_fn(current)
        if result != current:
            changes.append(description)
            current = result

    return current, changes


# ---------------------------------------------------------------------------
# Click CLI
# ---------------------------------------------------------------------------


@click.command("fix")
@click.option("--mod", "mod_name", default=None, help="Single mod folder name")
@click.option(
    "--only",
    "only_fixes",
    default=None,
    help=(
        "Comma-separated fix IDs: "
        "ipairs-iterator,mousedx,alttool,raw-key-player,draw-func,handle-gt,ammo-display,queryshot-guard,missing-version2,missing-mod-prefix"
    ),
)
@click.option("--dry-run", is_flag=True, help="Preview changes without writing")
def fix_cli(mod_name: str | None, only_fixes: str | None, dry_run: bool) -> None:
    """Apply safe auto-fixes to mods."""
    mods = discover_mods(mod_name=mod_name)
    if not mods:
        click.echo("No mods found")
        raise SystemExit(1)

    only = only_fixes.split(",") if only_fixes else None
    total_changes = 0

    for mod_dir in mods:
        for rel_path, source in read_lua_files(mod_dir):
            if rel_path == "options.lua":
                continue
            fixed, changes = apply_fixes(source, only=only)
            if changes:
                total_changes += len(changes)
                for c in changes:
                    tag = "WOULD FIX" if dry_run else "FIXED"
                    click.echo(f"  [{tag}] {mod_dir.name}/{rel_path}: {c}")
                if not dry_run:
                    lua_path = mod_dir / rel_path
                    # Backup
                    bak_path = lua_path.with_suffix(".lua.bak")
                    bak_path.write_text(source, encoding="utf-8")
                    # Write fixed
                    lua_path.write_text(fixed, encoding="utf-8")

    click.echo(f"\n{'Would fix' if dry_run else 'Fixed'}: {total_changes} issues")


if __name__ == "__main__":
    fix_cli()
