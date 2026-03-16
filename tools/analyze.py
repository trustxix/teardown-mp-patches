"""Phase 2: Static analysis of Teardown mod Lua scripts using tree-sitter."""

import json
import re
from pathlib import Path

import tree_sitter_lua as tslua
from tree_sitter import Language, Parser

from tools.ingest import parse_info_txt

API_DB_PATH = Path(__file__).parent / "api_database.json"

_api_db = None


def _get_api_db() -> dict:
    global _api_db
    if _api_db is None:
        with open(API_DB_PATH) as f:
            _api_db = json.load(f)
    return _api_db


def _get_parser() -> Parser:
    parser = Parser(Language(tslua.language()))
    return parser


def extract_callbacks(source: str) -> list[str]:
    """Extract top-level function names that match Teardown callback patterns."""
    parser = _get_parser()
    # Strip #version directive before parsing (not valid Lua)
    clean_source = re.sub(r"^#version\s+\d+\s*\n?", "", source)
    tree = parser.parse(clean_source.encode())
    callbacks = []

    for node in tree.root_node.children:
        if node.type == "function_declaration":
            name_node = node.child_by_field_name("name")
            if name_node:
                name = clean_source[name_node.start_byte:name_node.end_byte]
                callbacks.append(name)

    return callbacks


def extract_api_calls(source: str) -> list[dict]:
    """Extract all function calls and classify against API database."""
    db = _get_api_db()
    parser = _get_parser()
    clean_source = re.sub(r"^#version\s+\d+\s*\n?", "", source)
    tree = parser.parse(clean_source.encode())
    calls = []

    def visit(node):
        if node.type == "function_call":
            # The first child is the function identifier or method access
            name_text = None
            first_child = node.children[0] if node.children else None
            if first_child:
                name_text = clean_source[first_child.start_byte:first_child.end_byte]

            if name_text:
                # Handle dotted names like "math.floor" - check both full and base name
                base_name = name_text.split(".")[-1] if "." in name_text else name_text
                line = node.start_point[0] + 1

                entry = db.get(name_text) or db.get(base_name)
                if entry:
                    calls.append({
                        "function": name_text if name_text in db else base_name,
                        "line": line,
                        "domain": entry["domain"],
                        "needs_player_id": entry["needs_player_id"],
                        "restricted_to": entry.get("restricted_to"),
                        "deprecated": entry.get("deprecated"),
                    })

        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return calls


def _detect_handle_checks(source: str) -> list[dict]:
    """Detect entity handle > 0 patterns that break with negative handles."""
    issues = []
    for i, line in enumerate(source.splitlines(), 1):
        if re.search(r"\w+\s*>\s*0", line) and not re.match(r"\s*--", line):
            issues.append({"line": i, "content": line.strip()})
    return issues


def analyze_script(source: str, filename: str) -> dict:
    """Analyze a single Lua script file."""
    callbacks = extract_callbacks(source)
    api_calls = extract_api_calls(source)
    lines = len(source.splitlines())

    server_calls = sum(1 for c in api_calls if c["domain"] == "server")
    client_calls = sum(1 for c in api_calls if c["domain"] == "client")
    ambiguous_calls = sum(1 for c in api_calls if c["domain"] == "both")

    deprecated_calls = [c for c in api_calls if c.get("deprecated")]
    handle_checks = _detect_handle_checks(source)

    registry_fns = {"SetInt", "GetInt", "SetFloat", "GetFloat", "SetBool", "GetBool", "SetString", "GetString"}
    registry_usage = [c for c in api_calls if c["function"] in registry_fns]

    return {
        "file": filename,
        "lines": lines,
        "callbacks_found": callbacks,
        "api_calls": api_calls,
        "server_calls": server_calls,
        "client_calls": client_calls,
        "ambiguous_calls": ambiguous_calls,
        "deprecated_calls": deprecated_calls,
        "entity_handle_checks": handle_checks,
        "registry_usage": registry_usage,
    }


def classify_complexity(scripts: list[dict]) -> str:
    """Score mod complexity as simple, medium, or complex."""
    total_lines = sum(s["lines"] for s in scripts)
    num_scripts = len(scripts)
    max_lines = max(s["lines"] for s in scripts) if scripts else 0

    if num_scripts > 2 or max_lines > 500 or total_lines > 800:
        return "complex"
    elif num_scripts > 1 or max_lines > 300 or total_lines > 400:
        return "medium"
    return "simple"


def analyze_mod(mod_dir: Path) -> dict:
    """Analyze an entire mod directory."""
    info = parse_info_txt(mod_dir / "info.txt")
    current_version = int(info.get("version", "1"))

    scripts = []
    for lua_file in sorted(mod_dir.rglob("*.lua")):
        source = lua_file.read_text(encoding="utf-8")
        rel_path = str(lua_file.relative_to(mod_dir))
        script_analysis = analyze_script(source, rel_path)
        scripts.append(script_analysis)

    complexity = classify_complexity(scripts)

    tags = info.get("tags", "").lower()
    all_calls = [c["function"] for s in scripts for c in s["api_calls"]]
    vehicle_fns = {"GetPlayerVehicle", "SetPlayerVehicle", "DriveVehicle", "GetVehicleBody", "GetVehicleTransform"}
    tool_fns = {"RegisterTool"}

    if "vehicle" in tags or vehicle_fns.intersection(all_calls):
        mod_type = "vehicle"
    elif tool_fns.intersection(all_calls):
        mod_type = "tool"
    else:
        mod_type = "gameplay"

    issues = []
    for s in scripts:
        for d in s["deprecated_calls"]:
            issues.append(f"Deprecated: {d['function']} at {s['file']}:{d['line']} → use {d['deprecated']}")
        for h in s["entity_handle_checks"]:
            issues.append(f"Handle check at {s['file']}:{h['line']}: {h['content']}")

    return {
        "mod_name": info.get("name", "Unknown"),
        "mod_type": mod_type,
        "current_version": current_version,
        "scripts": scripts,
        "complexity": complexity,
        "estimated_approach": "template" if complexity in ("simple", "medium") else "ai",
        "issues": issues,
    }
