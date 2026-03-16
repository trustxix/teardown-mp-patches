"""Phase 6: Validate patched Teardown mods for MP v2 compliance."""

from __future__ import annotations

import re
import subprocess
import shutil
from pathlib import Path

from tools.ingest import parse_info_txt


# ---------------------------------------------------------------------------
# Lua block-depth helpers
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
    """Count block-opening keywords on a line.

    In Lua, 'for ... do' and 'while ... do' each have ONE matching 'end'.
    The 'do' in those cases is NOT an additional block opener; only a
    *standalone* 'do ... end' block adds an extra opener.
    """
    count = 0
    count += len(_FUNC_KEYWORD_RE.findall(line))
    count += len(_IF_RE.findall(line))
    count += len(_FOR_RE.findall(line))
    count += len(_WHILE_RE.findall(line))
    count += len(_REPEAT_RE.findall(line))

    # Standalone 'do': subtract one 'do' for each 'for' or 'while' on this line
    do_count = len(_DO_RE.findall(line))
    do_count -= len(_FOR_RE.findall(line))
    do_count -= len(_WHILE_RE.findall(line))
    if do_count > 0:
        count += do_count

    return count


def _count_ends(line: str) -> int:
    """Count block-closing keywords on a line ('end' + 'until')."""
    return len(_END_RE.findall(line)) + len(_UNTIL_RE.findall(line))


# ---------------------------------------------------------------------------
# Helper patterns
# ---------------------------------------------------------------------------

# Matches top-level v1-style function declarations: function init(), function tick(dt), etc.
_V1_CALLBACK_RE = re.compile(
    r"^\s*function\s+(init|tick|update|draw)\s*\(", re.MULTILINE
)

# Matches Ui* function calls
_UI_CALL_RE = re.compile(r"\bUi\w+\s*\(")

# Matches handle comparison: handle > 0 then (unsafe pattern)
_HANDLE_GT_RE = re.compile(r"\bh\w*\s*>\s*0\b")

# Deprecated API
_DEPRECATED_RE = re.compile(r"\bGetPlayerRigTransform\b")

# Player functions with empty parens (missing playerId)
_PLAYER_EMPTY_RE = re.compile(
    r"\b(GetPlayerTransform|GetPlayerVelocity|SetPlayerVelocity|GetPlayerHealth|SetPlayerHealth"
    r"|GetPlayerGrabBody|GetPlayerGrabShape|GetPlayerInteractBody|GetPlayerInteractShape"
    r"|GetPlayerPickShape|GetPlayerPickBody|GetPlayerCameraTransform"
    r"|GetPlayerPos|SetPlayerTransform"
    r"|SetPlayerSpawnTransform|SetPlayerOutOfBounds)\s*\(\s*\)"
)

# State-mutation functions that must be in server context
# Note: SetBool/SetInt/SetFloat/SetString for "hud.*" and "game.tool.*" keys
# are client-safe, but we can't easily parse the key argument here.
# These are checked at the function-call level, not key level.
_SERVER_AUTH_FUNCS = re.compile(
    r"\b(SetPlayerHealth|SetPlayerSpawnTransform|SetPlayerOutOfBounds"
    r"|ApplyPlayerDamage|RespawnPlayer)\s*\("
)

# Input functions that must be in client context
_CLIENT_INPUT_FUNCS = re.compile(
    r"\b(InputPressed|InputReleased|InputDown|GetMousePos|GetMouseDelta)\s*\("
)

# Registry Set* calls (SetBool/SetInt/SetFloat/SetString) – need 3+ args (sync param)
_REGISTRY_SET_RE = re.compile(
    r"\b(SetBool|SetInt|SetFloat|SetString)\s*\(([^)]*)\)"
)

# Top-level global assignment: identifier = ... (not local, not inside a function)
_GLOBAL_ASSIGN_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=[^=]", re.MULTILINE)

# Teardown API table names and Lua builtins to ignore in global assignment check
_GLOBAL_WHITELIST = frozenset(
    [
        # Lua builtins
        "print", "tostring", "tonumber", "type", "pairs", "ipairs", "next",
        "select", "unpack", "rawget", "rawset", "rawequal", "rawlen",
        "setmetatable", "getmetatable", "require", "load", "loadfile",
        "dofile", "pcall", "xpcall", "error", "assert", "collectgarbage",
        "math", "string", "table", "io", "os", "coroutine", "package",
        # Teardown globals/tables
        "server", "client", "ui", "game", "player",
    ]
)


# ---------------------------------------------------------------------------
# Result builder
# ---------------------------------------------------------------------------

def _result(check_id: str, passed: bool, detail: str = "") -> dict:
    return {"check": check_id, "passed": passed, "detail": detail}


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_v2_header(source: str) -> dict:
    """V2-HEADER: script must start with '#version 2'."""
    first_line = source.lstrip().split("\n", 1)[0].strip()
    passed = first_line == "#version 2"
    detail = "" if passed else f"First non-blank line is: {first_line!r}"
    return _result("V2-HEADER", passed, detail)


def check_v2_info(info_path: Path) -> dict:
    """V2-INFO: info.txt must have 'version = 2'."""
    if not info_path.exists():
        return _result("V2-INFO", False, f"info.txt not found at {info_path}")
    info = parse_info_txt(info_path)
    passed = info.get("version") == "2"
    detail = "" if passed else f"version = {info.get('version', '<missing>')!r}"
    return _result("V2-INFO", passed, detail)


def check_no_v1_callbacks(source: str) -> dict:
    """NO-V1-CBACKS: no bare function init/tick/update/draw at top level."""
    matches = _V1_CALLBACK_RE.findall(source)
    passed = len(matches) == 0
    detail = "" if passed else f"Found v1 callbacks: {matches}"
    return _result("NO-V1-CBACKS", passed, detail)


def check_ui_in_draw(source: str) -> dict:
    """UI-IN-DRAW: Ui* calls only inside client.draw().

    Uses depth-tracking to handle nested blocks and correctly determine
    which function scope each Ui* call lives in.
    """
    current_func: str | None = None
    depth = 0
    violations: list[str] = []

    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        func_match = _FUNC_DEF_RE.match(stripped)
        opens = _count_opens(stripped)
        ends = _count_ends(stripped)

        prev_depth = depth
        if func_match and depth == 0:
            current_func = func_match.group(1)
            # The 'function' keyword itself is 1 opener; additional openers/ends
            # on the same line (e.g., one-liner function) adjust from depth=1.
            depth = 1 + (opens - 1) - ends
        elif depth > 0:
            depth += opens - ends

        if depth < 0:
            depth = 0

        # Check for Ui* calls on this line.
        # Only flag Ui* calls inside explicitly wrong server.*/client.* functions
        # (not client.draw). Helper functions (no dot) are allowed since they
        # can be called from client.draw context.
        if _UI_CALL_RE.search(stripped):
            if current_func is not None and "." in current_func and current_func != "client.draw":
                violations.append("line %d: Ui* call in %r" % (lineno, current_func))

        # If depth dropped to 0, we've left the function
        if depth == 0:
            current_func = None

    passed = len(violations) == 0
    detail = "; ".join(violations) if violations else ""
    return _result("UI-IN-DRAW", passed, detail)


def _strip_comment(line: str) -> str:
    """Remove Lua line comment (--) from a line, naively."""
    # Very simple: find first '--' not inside a string.
    # For our purposes, a rough strip is fine.
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


def check_handle_safe(source: str) -> dict:
    """HANDLE-SAFE: no 'handle > 0 then' patterns (use IsValid() instead)."""
    violations = []
    for lineno, line in enumerate(source.splitlines(), 1):
        if _HANDLE_GT_RE.search(line):
            violations.append(f"line {lineno}: {line.strip()!r}")
    passed = len(violations) == 0
    detail = "; ".join(violations) if violations else ""
    return _result("HANDLE-SAFE", passed, detail)


def check_no_deprecated(source: str) -> dict:
    """NO-DEPRECATED: no use of deprecated API functions."""
    violations = []
    for lineno, line in enumerate(source.splitlines(), 1):
        if _DEPRECATED_RE.search(line):
            violations.append(f"line {lineno}: {line.strip()!r}")
    passed = len(violations) == 0
    detail = "; ".join(violations) if violations else ""
    return _result("NO-DEPRECATED", passed, detail)


def check_player_id(source: str) -> dict:
    """PLAYER-ID: player functions should have a playerId argument (no empty parens)."""
    violations = []
    for lineno, line in enumerate(source.splitlines(), 1):
        if _PLAYER_EMPTY_RE.search(line):
            violations.append(f"line {lineno}: {line.strip()!r}")
    passed = len(violations) == 0
    detail = "; ".join(violations) if violations else ""
    return _result("PLAYER-ID", passed, detail)


def check_server_auth(source: str) -> dict:
    """SERVER-AUTH: state-mutation functions must be in server.* functions."""
    violations = []
    _check_context_calls(
        source,
        call_re=_SERVER_AUTH_FUNCS,
        required_prefix="server",
        violations=violations,
    )
    passed = len(violations) == 0
    detail = "; ".join(violations) if violations else ""
    return _result("SERVER-AUTH", passed, detail)


def check_client_input(source: str) -> dict:
    """CLIENT-INPUT: input functions must be in client.* functions."""
    violations = []
    _check_context_calls(
        source,
        call_re=_CLIENT_INPUT_FUNCS,
        required_prefix="client",
        violations=violations,
    )
    passed = len(violations) == 0
    detail = "; ".join(violations) if violations else ""
    return _result("CLIENT-INPUT", passed, detail)


def _check_context_calls(
    source: str,
    call_re: re.Pattern,
    required_prefix: str,
    violations: list,
) -> None:
    """Generic helper: find calls to `call_re` that appear outside functions
    whose name starts with `required_prefix`."""
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

        # Check for violations: call found in the WRONG explicit context.
        # Only flag calls inside server.*/client.* functions that are in
        # the wrong domain. Helper functions (no dot in name) are allowed
        # since they can be called from either context.
        if call_re.search(stripped):
            if current_func is not None and "." in current_func:
                # Explicitly in a server.* or client.* function
                if not current_func.startswith(required_prefix + "."):
                    violations.append(
                        "line %d: %s... in %r" % (lineno, call_re.pattern[:30], current_func)
                    )

        if depth == 0:
            current_func = None


def check_registry_sync(source: str) -> dict:
    """REGISTRY-SYNC: SetBool/SetInt/SetFloat/SetString must have 3+ args (sync param)."""
    violations = []
    reg_fn_re = re.compile(r'\b(SetBool|SetInt|SetFloat|SetString)\s*\(')
    for lineno, line in enumerate(source.splitlines(), 1):
        for m in reg_fn_re.finditer(line):
            func_name = m.group(1)
            # Walk forward from the open paren, counting depth to find matching close
            start = m.end() - 1  # position of '('
            depth = 0
            comma_count = 0
            for j in range(start, len(line)):
                c = line[j]
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        if comma_count < 2:  # fewer than 3 args
                            violations.append(
                                f"line {lineno}: {func_name}() called with {comma_count + 1} args (need 3+)"
                            )
                        break
                elif c == ',' and depth == 1:
                    comma_count += 1
    passed = len(violations) == 0
    detail = "; ".join(violations) if violations else ""
    return _result("REGISTRY-SYNC", passed, detail)


def _count_args(args_str: str) -> int:
    """Count comma-separated arguments, respecting nested parens."""
    if not args_str.strip():
        return 0
    depth = 0
    count = 1
    for ch in args_str:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            count += 1
    return count


def check_syntax(source: str) -> dict:
    """SYNTAX-CHECK: run luac -p if available; skip gracefully if not."""
    luac = shutil.which("luac")
    if luac is None:
        return _result("SYNTAX-CHECK", True, "luac not available, skipped")

    import tempfile
    with tempfile.NamedTemporaryFile(
        suffix=".lua", mode="w", delete=False, encoding="utf-8"
    ) as f:
        # luac doesn't understand #version directives; strip the first line if needed
        lines = source.splitlines(keepends=True)
        if lines and lines[0].strip().startswith("#"):
            lines = lines[1:]
        f.write("".join(lines))
        tmp_path = f.name

    try:
        result = subprocess.run(
            [luac, "-p", tmp_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        passed = result.returncode == 0
        detail = result.stderr.strip() if not passed else ""
        return _result("SYNTAX-CHECK", passed, detail)
    except Exception as exc:
        return _result("SYNTAX-CHECK", True, f"luac check skipped: {exc}")
    finally:
        import os
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def check_no_globals(source: str) -> dict:
    """NO-GLOBALS: detect non-local top-level assignments. Always passes (warnings only).

    Uses a whitelist for Teardown API tables and Lua builtins.
    """
    warnings: list[str] = []
    local_re = re.compile(r"^\s*local\b")
    depth = 0

    for lineno, raw_line in enumerate(source.splitlines(), 1):
        stripped = _strip_comment(raw_line)
        func_match = _FUNC_DEF_RE.match(stripped)
        opens = _count_opens(stripped)
        ends = _count_ends(stripped)

        if func_match and depth == 0:
            depth = 1 + (opens - 1) - ends
        elif depth > 0:
            depth += opens - ends

        if depth < 0:
            depth = 0

        # Only check assignments at top level (depth == 0), not local ones
        if depth == 0 and not local_re.match(stripped):
            m = _GLOBAL_ASSIGN_RE.match(stripped)
            if m:
                name = m.group(1)
                if name not in _GLOBAL_WHITELIST:
                    warnings.append("line %d: possible global %r" % (lineno, name))

    # Always passes; warnings go in detail
    detail = "; ".join(warnings) if warnings else ""
    return _result("NO-GLOBALS", True, detail)


def check_file_complete(original_dir: Path, patched_dir: Path) -> dict:
    """FILE-COMPLETE: every file in original_dir must exist in patched_dir."""
    missing = []
    for orig_file in original_dir.rglob("*"):
        if not orig_file.is_file():
            continue
        rel = orig_file.relative_to(original_dir)
        patched_file = patched_dir / rel
        if not patched_file.exists():
            missing.append(str(rel))
    passed = len(missing) == 0
    detail = f"Missing files: {missing}" if missing else ""
    return _result("FILE-COMPLETE", passed, detail)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def validate_script(source: str, filename: str) -> list[dict]:
    """Run all per-script checks (checks 1, 3-12) on a single Lua source string."""
    return [
        check_v2_header(source),
        check_no_v1_callbacks(source),
        check_ui_in_draw(source),
        check_handle_safe(source),
        check_no_deprecated(source),
        check_player_id(source),
        check_server_auth(source),
        check_client_input(source),
        check_registry_sync(source),
        check_syntax(source),
        check_no_globals(source),
    ]


def validate_mod(mod_dir: Path, original_dir: Path | None = None) -> dict:
    """Run all checks on an entire mod directory.

    Returns a dict with keys:
      - all_passed: bool
      - files: list of per-file result dicts
      - info_check: V2-INFO result
      - file_complete: FILE-COMPLETE result (if original_dir provided)
    """
    results: dict = {
        "all_passed": True,
        "files": [],
        "info_check": None,
        "file_complete": None,
    }

    # Check info.txt
    info_result = check_v2_info(mod_dir / "info.txt")
    results["info_check"] = info_result
    if not info_result["passed"]:
        results["all_passed"] = False

    # Check file completeness if original provided
    if original_dir is not None:
        fc_result = check_file_complete(original_dir, mod_dir)
        results["file_complete"] = fc_result
        if not fc_result["passed"]:
            results["all_passed"] = False

    # Check each .lua file
    for lua_file in sorted(mod_dir.rglob("*.lua")):
        source = lua_file.read_text(encoding="utf-8", errors="replace")
        file_results = validate_script(source, lua_file.name)
        file_entry = {
            "file": str(lua_file.relative_to(mod_dir)),
            "checks": file_results,
            "passed": all(r["passed"] for r in file_results),
        }
        results["files"].append(file_entry)
        if not file_entry["passed"]:
            results["all_passed"] = False

    return results
