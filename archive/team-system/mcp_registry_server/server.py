"""MCP Mod Registry Server for Teardown MP Patches.

Indexes all mod metadata on startup and serves fast queries.
Avoids repeated file reads by caching everything in memory.
"""

import re
import sys
from pathlib import Path
from datetime import datetime, timezone

from mcp.server import FastMCP

# Add project root so we can import tools
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.common import discover_mods, read_lua_files
from tools.audit import detect_features

# ── Metadata extraction regexes ──────────────────────────────────────────────

_REGISTER_TOOL_RE = re.compile(
    r'RegisterTool\s*\(\s*"([^"]+)"\s*,\s*"([^"]+)"'
)
_SAVEGAME_KEY_RE = re.compile(
    r'(?:GetBool|SetBool|GetInt|SetInt|GetFloat|SetFloat|GetString|SetString|HasKey)'
    r'\s*\(\s*"(savegame\.mod\.[^"]+)"'
)

# ── Registry ─────────────────────────────────────────────────────────────────

_registry: dict[str, dict] = {}
_last_scan: str | None = None


def _scan_mod(mod_dir: Path) -> dict:
    """Extract all metadata from a single mod directory."""
    lua_files = read_lua_files(mod_dir)
    all_source = "\n".join(src for _, src in lua_files)

    # Tool ID and display name from RegisterTool
    tool_id = ""
    display_name = ""
    m = _REGISTER_TOOL_RE.search(all_source)
    if m:
        tool_id = m.group(1)
        display_name = m.group(2)

    # Savegame keys
    savegame_keys = sorted(set(_SAVEGAME_KEY_RE.findall(all_source)))

    # Feature flags (reuse audit.py logic)
    features = detect_features(all_source)

    # File and line counts
    file_count = len(lua_files)
    line_count = sum(src.count("\n") + 1 for _, src in lua_files)

    # info.txt metadata
    info_path = mod_dir / "info.txt"
    author = ""
    description = ""
    if info_path.exists():
        info_text = info_path.read_text(encoding="utf-8", errors="replace")
        for line in info_text.splitlines():
            if line.startswith("author"):
                author = line.split("=", 1)[-1].strip()
            elif line.startswith("description"):
                description = line.split("=", 1)[-1].strip()

    return {
        "mod_name": mod_dir.name,
        "tool_id": tool_id,
        "display_name": display_name,
        "author": author,
        "description": description,
        "savegame_keys": savegame_keys,
        "features": features,
        "file_count": file_count,
        "line_count": line_count,
    }


def _full_scan() -> dict[str, dict]:
    """Scan all mods and return the registry dict."""
    global _last_scan
    registry = {}
    for mod_dir in discover_mods():
        entry = _scan_mod(mod_dir)
        registry[mod_dir.name] = entry
    _last_scan = datetime.now(timezone.utc).isoformat()
    return registry


# ── FastMCP server ───────────────────────────────────────────────────────────

mcp = FastMCP(
    name="mod-registry",
    instructions=(
        "Mod metadata registry for Teardown MP Patches. "
        "Indexes all mods on startup for fast queries. "
        "Use query_mod for single mod info, query_mods to filter by feature."
    ),
)


@mcp.tool(description="Get metadata for a single mod. Returns tool_id, display_name, features, savegame_keys, file/line counts.")
def query_mod(mod_name: str) -> dict | str:
    """Query metadata for a specific mod by folder name."""
    if mod_name not in _registry:
        # Try case-insensitive match
        for key in _registry:
            if key.lower() == mod_name.lower():
                return _registry[key]
        return f"Mod '{mod_name}' not found. Use query_mods() to list all mods."
    return _registry[mod_name]


@mcp.tool(description="Query mods by feature filter. Filters: 'all', 'missing_shoot', 'missing_aiminfo', 'missing_options', 'missing_hints', 'missing_ammo_display', 'has_savegame', 'is_gun', 'has_options'. Returns list of matching mod names with key metadata.")
def query_mods(filter: str = "all") -> dict:
    """Filter mods by feature. Returns summary list."""
    results = []
    for name, entry in sorted(_registry.items()):
        feats = entry["features"]
        match = False

        if filter == "all":
            match = True
        elif filter == "missing_shoot":
            match = feats["is_gun_mod"] and not feats["has_shoot"]
        elif filter == "missing_aiminfo":
            match = feats["is_gun_mod"] and not feats["has_aim_info"]
        elif filter == "missing_options":
            match = not feats["has_options_menu"]
        elif filter == "missing_hints":
            match = not feats["has_keybind_hints"]
        elif filter == "missing_ammo_display":
            match = not feats["has_ammo_display_hidden"]
        elif filter == "has_savegame":
            match = len(entry["savegame_keys"]) > 0
        elif filter == "is_gun":
            match = feats["is_gun_mod"]
        elif filter == "has_options":
            match = feats["has_options_menu"]
        else:
            return {"error": f"Unknown filter '{filter}'. Valid: all, missing_shoot, missing_aiminfo, missing_options, missing_hints, missing_ammo_display, has_savegame, is_gun, has_options"}

        if match:
            results.append({
                "mod_name": name,
                "tool_id": entry["tool_id"],
                "display_name": entry["display_name"],
                "line_count": entry["line_count"],
            })

    return {
        "filter": filter,
        "count": len(results),
        "total_mods": len(_registry),
        "last_scan": _last_scan,
        "mods": results,
    }


@mcp.tool(description="Re-scan all mods and return what changed since last scan. Call after batch edits.")
def refresh_registry() -> dict:
    """Re-scan all mods. Returns diff of changes."""
    global _registry
    old_registry = _registry.copy()
    _registry.update(_full_scan())

    # Compute diff
    added = [k for k in _registry if k not in old_registry]
    removed = [k for k in old_registry if k not in _registry]
    changed = []
    for k in _registry:
        if k in old_registry and _registry[k] != old_registry[k]:
            changed.append(k)

    # Remove mods that no longer exist
    for k in removed:
        _registry.pop(k, None)

    return {
        "total_mods": len(_registry),
        "last_scan": _last_scan,
        "added": added,
        "removed": removed,
        "changed": changed,
    }


@mcp.tool(description="Show what changed for a specific mod since last refresh. Useful for docs updates.")
def get_mod_diff(mod_name: str) -> dict | str:
    """Re-scan a single mod and diff against cached version."""
    if mod_name not in _registry:
        for key in _registry:
            if key.lower() == mod_name.lower():
                mod_name = key
                break
        else:
            return f"Mod '{mod_name}' not found in registry."

    old_entry = _registry[mod_name]

    # Find the mod dir and re-scan
    mods = discover_mods(mod_name=mod_name)
    if not mods:
        return f"Mod directory for '{mod_name}' no longer exists."

    new_entry = _scan_mod(mods[0])

    # Compare
    diffs = {}
    for key in new_entry:
        if key == "features":
            old_feats = old_entry.get("features", {})
            new_feats = new_entry["features"]
            feat_diffs = {}
            for fk in new_feats:
                if old_feats.get(fk) != new_feats[fk]:
                    feat_diffs[fk] = {"old": old_feats.get(fk), "new": new_feats[fk]}
            if feat_diffs:
                diffs["features"] = feat_diffs
        elif old_entry.get(key) != new_entry[key]:
            diffs[key] = {"old": old_entry.get(key), "new": new_entry[key]}

    # Update cache
    _registry[mod_name] = new_entry

    return {
        "mod_name": mod_name,
        "has_changes": len(diffs) > 0,
        "diffs": diffs,
    }


# ── Startup ──────────────────────────────────────────────────────────────────

# Scan all mods on import so the registry is ready when the server starts
_registry = _full_scan()

if __name__ == "__main__":
    mcp.run(transport="stdio")
