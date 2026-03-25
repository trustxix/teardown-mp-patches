"""MCP Change Tracker Server — records all changes for documentation tracking.

Every terminal calls record_change() after meaningful edits.
Docs keeper polls get_undocumented_changes() to find work that needs logging.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from mcp.server import FastMCP

CHANGES_FILE = Path(__file__).parent / "changes.json"
LOCK_FILE = Path(__file__).parent / "changes.lock"

mcp = FastMCP(
    name="change-tracker",
    instructions="Records all project changes for documentation tracking. Terminals call record_change after edits. Docs keeper calls get_undocumented_changes to find work.",
)


def _load() -> dict:
    if CHANGES_FILE.exists():
        content = CHANGES_FILE.read_text(encoding="utf-8").strip()
        if content:
            return json.loads(content)
    return {"changes": [], "next_id": 1}


def _save(data: dict):
    CHANGES_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


VALID_TYPES = {"bug_fix", "feature_add", "api_migration", "polish", "conversion", "tool_update", "rule_add", "server_build", "doc_update"}


@mcp.tool(description="Record a change made to the project. Call this after every meaningful edit so docs keeper can track it.")
def record_change(role: str, mod_name: str, change_type: str, description: str) -> dict:
    """Record a change.

    role: who made it (api_surgeon, mod_converter, qa_lead, docs_keeper)
    mod_name: which mod or 'project' for non-mod changes
    change_type: bug_fix, feature_add, api_migration, polish, conversion, tool_update, rule_add, server_build, doc_update
    description: what was done
    """
    if change_type not in VALID_TYPES:
        return {"success": False, "message": f"Invalid change_type. Must be one of: {', '.join(sorted(VALID_TYPES))}"}

    data = _load()
    change_id = data["next_id"]
    change = {
        "id": change_id,
        "role": role,
        "mod": mod_name,
        "type": change_type,
        "description": description,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "documented": False,
    }
    data["changes"].append(change)
    data["next_id"] = change_id + 1
    _save(data)

    return {"success": True, "change_id": change_id}


@mcp.tool(description="Get all changes, optionally filtered by time window. Returns newest first.")
def get_changes(since_minutes: int = 60) -> list[dict]:
    """Get changes from the last N minutes."""
    data = _load()
    now = datetime.now(timezone.utc)
    cutoff = now.timestamp() - (since_minutes * 60)

    results = []
    for c in reversed(data["changes"]):
        try:
            ts = datetime.fromisoformat(c["timestamp"]).timestamp()
            if ts >= cutoff:
                results.append(c)
        except (ValueError, KeyError):
            results.append(c)

    return results if results else "No changes in the last {} minutes".format(since_minutes)


@mcp.tool(description="Get all changes for a specific mod. Returns newest first.")
def get_changes_by_mod(mod_name: str) -> list[dict]:
    """Get all changes for a specific mod."""
    data = _load()
    results = [c for c in reversed(data["changes"]) if c["mod"].lower() == mod_name.lower()]
    return results if results else f"No changes recorded for {mod_name}"


@mcp.tool(description="Get all changes not yet marked as documented. This is the docs keeper's main work-finding tool.")
def get_undocumented_changes() -> list[dict]:
    """Get changes that haven't been logged in docs yet."""
    data = _load()
    results = [c for c in data["changes"] if not c.get("documented", False)]
    return results if results else "All changes documented"


@mcp.tool(description="Mark a change as documented. Docs keeper calls this after updating ISSUES_AND_FIXES.md or other docs.")
def mark_documented(change_id: int) -> dict:
    """Mark a change as documented."""
    data = _load()
    for c in data["changes"]:
        if c["id"] == change_id:
            c["documented"] = True
            _save(data)
            return {"success": True, "change_id": change_id}
    return {"success": False, "message": f"Change {change_id} not found"}


@mcp.tool(description="Mark multiple changes as documented at once.")
def mark_all_documented(change_ids: list[int]) -> dict:
    """Batch mark changes as documented."""
    data = _load()
    marked = 0
    for c in data["changes"]:
        if c["id"] in change_ids:
            c["documented"] = True
            marked += 1
    _save(data)
    return {"success": True, "marked": marked, "total_requested": len(change_ids)}


@mcp.tool(description="Get a summary of change activity: counts by type, by role, documented vs undocumented.")
def get_change_summary() -> dict:
    """Dashboard view of all change activity."""
    data = _load()
    changes = data["changes"]

    by_type = {}
    by_role = {}
    by_mod = {}
    undocumented = 0

    for c in changes:
        t = c.get("type", "unknown")
        r = c.get("role", "unknown")
        m = c.get("mod", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
        by_role[r] = by_role.get(r, 0) + 1
        by_mod[m] = by_mod.get(m, 0) + 1
        if not c.get("documented", False):
            undocumented += 1

    return {
        "total_changes": len(changes),
        "undocumented": undocumented,
        "documented": len(changes) - undocumented,
        "by_type": by_type,
        "by_role": by_role,
        "most_changed_mods": dict(sorted(by_mod.items(), key=lambda x: -x[1])[:10]),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
