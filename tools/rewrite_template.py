"""Phase 3: Template-based v1 -> v2 Lua rewriter for Teardown mods.

Uses block-aware parsing and Jinja2 templates to split v1 callbacks into
server/client domains and generate valid v2 scripts.
"""

import json
import re
from pathlib import Path

import jinja2
import tree_sitter_lua as tslua
from tree_sitter import Language, Parser

API_DB_PATH = Path(__file__).parent / "api_database.json"
TEMPLATES_DIR = Path(__file__).parent / "templates"

_api_db = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_api_db() -> dict:
    global _api_db
    if _api_db is None:
        with open(API_DB_PATH) as f:
            _api_db = json.load(f)
    return _api_db


def _get_parser() -> Parser:
    return Parser(Language(tslua.language()))


# Sets of function names used for domain classification
_CLIENT_SIGNAL_PREFIXES = (
    "Input", "Ui", "PlaySound", "PlayLoop", "LoadSound", "StopSound",
    "StopLoop", "SpawnParticle", "Particle", "SpawnFire", "SpawnExplosion",
    "SetFireSpread", "SetCameraDof", "SetCameraTransform",
)

_SERVER_SIGNAL_NAMES = {
    "SetPlayerHealth", "GetPlayerHealth", "ApplyPlayerDamage",
    "RespawnPlayer", "RespawnPlayerAtTransform",
    "DisablePlayer", "DisablePlayerInput", "DisablePlayerDamage",
    "SetPlayerVehicle", "GetPlayerVehicle", "GetPlayerTool", "SetPlayerTool",
    "GetPlayerTransform", "SetPlayerTransform", "GetPlayerPos",
    "GetPlayerRigTransform", "GetPlayerRigWorldTransform",
    "RegisterTool", "GetToolTransform", "SetToolTransform",
    "MakeHole", "Shoot", "Paint",
}

_REGISTRY_SET_FUNCS = {"SetInt", "SetFloat", "SetBool", "SetString"}

# Functions that need a playerId argument prepended in MP
_PLAYER_ID_FUNCTIONS: set[str] = set()


def _build_player_id_set() -> set[str]:
    """Build the set of functions needing playerId from the API database."""
    global _PLAYER_ID_FUNCTIONS
    if _PLAYER_ID_FUNCTIONS:
        return _PLAYER_ID_FUNCTIONS
    db = _get_api_db()
    for name, entry in db.items():
        if entry.get("needs_player_id"):
            _PLAYER_ID_FUNCTIONS.add(name)
    return _PLAYER_ID_FUNCTIONS


# ---------------------------------------------------------------------------
# apply_fixups
# ---------------------------------------------------------------------------


def apply_fixups(source: str) -> str:
    """Apply automatic code fixups to source.

    - Add ``#version 2`` header
    - Replace ``GetPlayerRigTransform`` -> ``GetPlayerRigWorldTransform``
    - Replace ``handle > 0 then`` -> ``handle ~= 0 then``
    - Add ``sync=true`` to registry Set* calls that only have 2 args
    """
    # Strip any existing #version line
    source = re.sub(r"^#version\s+\d+\s*\n?", "", source)

    # Deprecated function renames
    source = source.replace("GetPlayerRigTransform", "GetPlayerRigWorldTransform")

    # Handle checks:  `word > 0 then`  ->  `word ~= 0 then`
    source = re.sub(r"(\w+)\s*>\s*0(\s+then)", r"\1 ~= 0\2", source)

    # Registry sync: SetInt("key", val) -> SetInt("key", val, true)
    # Uses paren-aware arg counting to avoid breaking nested expressions.
    lines = source.split('\n')
    for i, line in enumerate(lines):
        for fn in _REGISTRY_SET_FUNCS:
            if fn + '(' not in line:
                continue
            # Find the function call and count its args properly
            idx = line.find(fn + '(')
            if idx == -1:
                continue
            start = idx + len(fn)  # position of '('
            # Walk forward counting parens to find the matching ')'
            depth = 0
            comma_count = 0
            j = start
            while j < len(line):
                c = line[j]
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                    if depth == 0:
                        # Found the matching close paren
                        if comma_count == 1:  # exactly 2 args, needs sync
                            line = line[:j] + ', true' + line[j:]
                        break
                elif c == ',' and depth == 1:
                    comma_count += 1
                j += 1
        lines[i] = line
    source = '\n'.join(lines)

    # Prepend #version 2
    source = "#version 2\n" + source

    return source


# ---------------------------------------------------------------------------
# wrap_player_calls_for_mp
# ---------------------------------------------------------------------------


def wrap_player_calls_for_mp(source: str) -> str:
    """Replace ``PlayerFunc()`` with ``PlayerFunc(playerId)`` and
    ``PlayerFunc(args)`` with ``PlayerFunc(playerId, args)`` for functions
    that need a player ID in multiplayer.
    """
    player_fns = _build_player_id_set()
    for fn in player_fns:
        # Case 1: FuncName() -- no args -> FuncName(playerId)
        source = re.sub(
            rf'\b{re.escape(fn)}\(\s*\)',
            f'{fn}(playerId)',
            source,
        )
        # Case 2: FuncName(args) -- has args -> FuncName(playerId, args)
        # But skip if already has playerId as first arg
        source = re.sub(
            rf'\b{re.escape(fn)}\((?!playerId\b)(\s*\S)',
            rf'{fn}(playerId, \1',
            source,
        )
    return source


# ---------------------------------------------------------------------------
# update_info_txt
# ---------------------------------------------------------------------------


def update_info_txt(path: Path) -> None:
    """Add or update ``version = 2`` in an info.txt file."""
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith("version"):
            lines[i] = "version = 2"
            found = True
            break

    if not found:
        lines.append("version = 2")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Block-aware splitting
# ---------------------------------------------------------------------------

# Keywords that open a block (must be matched by a corresponding ``end``)
_BLOCK_OPENERS = {"if", "for", "while", "repeat"}


def _classify_line_domain(line: str) -> str | None:
    """Classify a single line as 'client', 'server', or None (ambiguous).

    Uses function-call names present on the line to decide.
    """
    stripped = line.strip()
    if stripped.startswith("--"):
        return None

    db = _get_api_db()

    # Extract all potential function calls from the line
    calls = re.findall(r'\b([A-Z]\w+)\s*\(', line)
    domains: set[str] = set()
    for call in calls:
        entry = db.get(call)
        if entry:
            d = entry["domain"]
            restricted = entry.get("restricted_to")
            if restricted and "client" in restricted:
                domains.add("client")
            elif d == "client":
                domains.add("client")
            elif d == "server":
                domains.add("server")
            # 'both' doesn't give a signal

    if not domains:
        return None
    if domains == {"client"}:
        return "client"
    if domains == {"server"}:
        return "server"
    # Mixed -> client (safer default, the task spec says so)
    return "client"


def _parse_top_level_blocks(body_lines: list[str]) -> list[dict]:
    """Parse body_lines into a list of top-level blocks.

    Each block is a dict with:
      - ``lines``: list of source lines
      - ``type``: 'block' (if/for/while/repeat...end) or 'single'
    """
    blocks: list[dict] = []
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        stripped = line.strip()

        # Check if this line starts a block construct
        is_block_opener = False
        for kw in _BLOCK_OPENERS:
            # Match: if ... then, for ... do, while ... do, repeat
            if kw == "if" and re.match(r'\s*if\b', stripped) and "then" in stripped:
                is_block_opener = True
                break
            elif kw == "for" and re.match(r'\s*for\b', stripped) and "do" in stripped:
                is_block_opener = True
                break
            elif kw == "while" and re.match(r'\s*while\b', stripped) and "do" in stripped:
                is_block_opener = True
                break
            elif kw == "repeat" and re.match(r'\s*repeat\b', stripped):
                is_block_opener = True
                break

        if is_block_opener:
            # Collect lines until matching end
            depth = 1
            block_lines = [line]
            j = i + 1
            while j < len(body_lines) and depth > 0:
                inner = body_lines[j].strip()
                # Count openers
                for kw in _BLOCK_OPENERS:
                    if kw == "if" and re.match(r'\s*if\b', inner) and "then" in inner:
                        depth += 1
                    elif kw == "for" and re.match(r'\s*for\b', inner) and "do" in inner:
                        depth += 1
                    elif kw == "while" and re.match(r'\s*while\b', inner) and "do" in inner:
                        depth += 1
                    elif kw == "repeat" and re.match(r'\s*repeat\b', inner):
                        depth += 1
                # Count closers
                if re.match(r'\s*end\b', inner):
                    depth -= 1
                elif re.match(r'\s*until\b', inner):
                    depth -= 1
                block_lines.append(body_lines[j])
                j += 1
            blocks.append({"lines": block_lines, "type": "block"})
            i = j
        else:
            # Single line
            if stripped:  # skip blank lines at this stage
                blocks.append({"lines": [line], "type": "single"})
            i += 1

    return blocks


def _classify_block_domain(block: dict) -> str:
    """Classify an entire block by scanning all its lines for domain signals.

    Returns 'client', 'server', or 'ambiguous'.
    """
    domains: set[str] = set()
    for line in block["lines"]:
        d = _classify_line_domain(line)
        if d:
            domains.add(d)

    if not domains:
        return "ambiguous"
    if domains == {"client"}:
        return "client"
    if domains == {"server"}:
        return "server"
    # Mixed -> client (task spec: mixed blocks default to client)
    return "client"


def split_callback_body(
    body_lines: list[str], callback_name: str
) -> tuple[list[str], list[str]]:
    """Split a callback body into (client_lines, server_lines) using
    block-aware parsing.

    - Input functions -> client
    - Player state mutations -> server
    - UI functions -> client
    - Sound/effects -> client
    - Registry writes -> server
    - Mixed blocks -> client
    - Ambiguous single lines default by callback:
        draw -> client, init -> server, tick/update -> server
    """
    blocks = _parse_top_level_blocks(body_lines)
    client_lines: list[str] = []
    server_lines: list[str] = []

    # Default domain for ambiguous lines depends on callback
    default_domain = "client" if callback_name == "draw" else "server"

    for block in blocks:
        domain = _classify_block_domain(block)
        if domain == "ambiguous":
            domain = default_domain

        if domain == "client":
            client_lines.extend(block["lines"])
        else:
            server_lines.extend(block["lines"])

    return client_lines, server_lines


# ---------------------------------------------------------------------------
# Tree-sitter function body extraction
# ---------------------------------------------------------------------------


def _extract_function_body(
    source: str, func_name: str
) -> tuple[list[str], int, int] | None:
    """Extract the body lines of a top-level function using tree-sitter.

    Returns (body_lines, start_line, end_line) or None if not found.
    Line numbers are 0-based.
    """
    parser = _get_parser()
    # Strip #version directive before parsing
    clean_source = re.sub(r"^#version\s+\d+\s*\n?", "", source)
    tree = parser.parse(clean_source.encode())

    for node in tree.root_node.children:
        if node.type == "function_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                name = clean_source[name_node.start_byte:name_node.end_byte]
                if name == func_name:
                    # The function body is between the parameter list and 'end'
                    # In tree-sitter-lua, the body is the `block` child
                    body_node = node.child_by_field_name("body")
                    if body_node is None:
                        # Fallback: find the block node
                        for child in node.children:
                            if child.type == "block":
                                body_node = child
                                break

                    if body_node is None:
                        return None

                    # Extract body lines from the source lines directly,
                    # using the block node's line range. This avoids the
                    # mid-line start issue from byte-based extraction.
                    source_lines = clean_source.splitlines()
                    start_row = body_node.start_point[0]
                    end_row = body_node.end_point[0]
                    body_lines = source_lines[start_row:end_row + 1]

                    # Remove leading/trailing empty lines
                    while body_lines and not body_lines[0].strip():
                        body_lines.pop(0)
                    while body_lines and not body_lines[-1].strip():
                        body_lines.pop()

                    return (
                        body_lines,
                        start_row,
                        end_row,
                    )

    return None


def _extract_helper_functions(source: str, callback_names: set[str]) -> str:
    """Extract all non-callback top-level functions as a string."""
    parser = _get_parser()
    clean_source = re.sub(r"^#version\s+\d+\s*\n?", "", source)
    tree = parser.parse(clean_source.encode())

    helpers = []
    for node in tree.root_node.children:
        if node.type == "function_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                name = clean_source[name_node.start_byte:name_node.end_byte]
                if name not in callback_names:
                    func_text = clean_source[node.start_byte:node.end_byte]
                    helpers.append(func_text)

    return "\n\n".join(helpers)


def _extract_module_locals(source: str) -> str:
    """Extract top-level local variable declarations (not inside functions)."""
    parser = _get_parser()
    clean_source = re.sub(r"^#version\s+\d+\s*\n?", "", source)
    tree = parser.parse(clean_source.encode())

    locals_lines = []
    for node in tree.root_node.children:
        if node.type == "variable_declaration":
            text = clean_source[node.start_byte:node.end_byte]
            locals_lines.append(text)

    return "\n".join(locals_lines)


# ---------------------------------------------------------------------------
# Template rendering
# ---------------------------------------------------------------------------


def _indent_body(lines: list[str], indent: int = 4) -> str:
    """Indent a list of body lines, preserving relative indentation.

    Finds the minimum indentation among non-blank lines, strips that common
    prefix, and re-indents everything by *indent* spaces.
    """
    # Determine minimum indentation (number of leading spaces) among non-blank lines
    min_indent = None
    for line in lines:
        if line.strip():
            leading = len(line) - len(line.lstrip())
            if min_indent is None or leading < min_indent:
                min_indent = leading
    if min_indent is None:
        min_indent = 0

    prefix = " " * indent
    result = []
    for line in lines:
        if line.strip():
            # Remove common leading indentation, then add target indent
            result.append(prefix + line[min_indent:])
        else:
            result.append("")
    return "\n".join(result)


def _render_template(mod_type: str, context: dict) -> str:
    """Render a Jinja2 template for the given mod type."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template_name = f"{mod_type}_mod.lua.j2"
    template = env.get_template(template_name)
    return template.render(**context)


# ---------------------------------------------------------------------------
# rewrite_script - main entry point
# ---------------------------------------------------------------------------

V1_CALLBACKS = {"init", "tick", "update", "draw"}


def rewrite_script(source: str, analysis: dict, mod_type: str = "tool") -> str:
    """Rewrite a v1 Lua script to v2 using template-based domain splitting.

    Args:
        source: Original v1 Lua source code.
        analysis: Output of ``analyze_script()``.
        mod_type: One of 'tool', 'vehicle', 'gameplay'.

    Returns:
        Rewritten v2 Lua source code.
    """
    callbacks_found = set(analysis.get("callbacks_found", []))

    # Extract module-level locals
    module_locals = _extract_module_locals(source)

    # Extract helper functions
    helper_functions = _extract_helper_functions(source, V1_CALLBACKS)

    # Process each callback
    server_init_body = ""
    client_init_body = ""
    server_tick_body = ""
    client_tick_body = ""
    server_update_body = ""
    client_update_body = ""
    client_draw_body = ""

    for cb_name in V1_CALLBACKS:
        if cb_name not in callbacks_found:
            continue

        extracted = _extract_function_body(source, cb_name)
        if extracted is None:
            continue

        body_lines, _, _ = extracted

        if cb_name == "draw":
            # draw -> always client.draw
            client_draw_body = _indent_body(body_lines)
        elif cb_name == "init":
            # Split init body
            client_lines, server_lines = split_callback_body(body_lines, "init")
            if server_lines:
                server_init_body = _indent_body(server_lines)
            if client_lines:
                client_init_body = _indent_body(client_lines)
        elif cb_name == "tick":
            client_lines, server_lines = split_callback_body(body_lines, "tick")
            if server_lines:
                server_tick_body = _indent_body(server_lines)
            if client_lines:
                client_tick_body = _indent_body(client_lines)
        elif cb_name == "update":
            client_lines, server_lines = split_callback_body(body_lines, "update")
            if server_lines:
                server_update_body = _indent_body(server_lines)
            if client_lines:
                client_update_body = _indent_body(client_lines)

    # Build template context
    context = {
        "module_locals": module_locals,
        "helper_functions": helper_functions,
        "server_init_body": server_init_body,
        "client_init_body": client_init_body,
        "server_tick_body": server_tick_body,
        "client_tick_body": client_tick_body,
        "server_update_body": server_update_body,
        "client_update_body": client_update_body,
        "client_draw_body": client_draw_body,
    }

    result = _render_template(mod_type, context)

    # Apply fixups (deprecated renames, handle checks, registry sync)
    # But skip adding #version 2 again since the template already has it
    result_no_version = re.sub(r"^#version\s+\d+\s*\n?", "", result)
    result_fixed = apply_fixups(result_no_version)

    # Wrap player calls for MP
    result_fixed = wrap_player_calls_for_mp(result_fixed)

    # Clean up excessive blank lines (3+ -> 2)
    result_fixed = re.sub(r"\n{3,}", "\n\n", result_fixed)

    # Ensure trailing newline
    if not result_fixed.endswith("\n"):
        result_fixed += "\n"

    return result_fixed
