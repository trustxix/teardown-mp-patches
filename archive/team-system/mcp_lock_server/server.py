"""MCP File Lock Server for Teardown MP Patches.

Prevents concurrent edits to the same file by multiple terminals.
Locks auto-expire after 5 minutes to prevent stale locks from crashed terminals.
"""

import time

from mcp.server import FastMCP

LOCK_EXPIRY_SECONDS = 300  # 5 minutes

mcp = FastMCP(
    name="file-lock",
    instructions=(
        "File locking server for Teardown MP Patches. "
        "Terminals must call lock_file before editing mod files "
        "and unlock_file when done."
    ),
)

# In-memory lock store: filepath -> {"role": str, "locked_at": float}
_locks: dict[str, dict] = {}

VALID_ROLES = {"api_surgeon", "mod_converter", "qa_lead", "docs_keeper"}


def _normalize_path(filepath: str) -> str:
    """Normalize path separators for consistent lock keys."""
    return filepath.replace("\\", "/").lower()


def _expire_stale_locks() -> None:
    """Remove locks older than LOCK_EXPIRY_SECONDS."""
    now = time.time()
    expired = [fp for fp, info in _locks.items() if now - info["locked_at"] > LOCK_EXPIRY_SECONDS]
    for fp in expired:
        del _locks[fp]


@mcp.tool(description="Acquire an exclusive lock on a file. Returns success/fail and who holds it if locked.")
def lock_file(role: str, filepath: str) -> dict:
    """Lock a file for exclusive editing."""
    if role not in VALID_ROLES:
        return {"success": False, "error": f"Invalid role '{role}'. Must be one of: {', '.join(sorted(VALID_ROLES))}"}

    _expire_stale_locks()
    key = _normalize_path(filepath)

    if key in _locks:
        holder = _locks[key]
        if holder["role"] == role:
            # Same role re-locking — refresh the timestamp
            holder["locked_at"] = time.time()
            return {"success": True, "message": f"Lock refreshed on {filepath}"}
        else:
            age = int(time.time() - holder["locked_at"])
            return {
                "success": False,
                "held_by": holder["role"],
                "locked_seconds_ago": age,
                "message": f"File locked by {holder['role']} ({age}s ago). Send them a message to coordinate.",
            }

    _locks[key] = {"role": role, "locked_at": time.time()}
    return {"success": True, "message": f"Lock acquired on {filepath}"}


@mcp.tool(description="Release a lock on a file. Only the lock holder can unlock.")
def unlock_file(role: str, filepath: str) -> dict:
    """Unlock a file after editing is complete."""
    if role not in VALID_ROLES:
        return {"success": False, "error": f"Invalid role '{role}'."}

    _expire_stale_locks()
    key = _normalize_path(filepath)

    if key not in _locks:
        return {"success": True, "message": "File was not locked."}

    holder = _locks[key]
    if holder["role"] != role:
        return {
            "success": False,
            "error": f"Lock held by {holder['role']}, not {role}. Use force_unlock if stuck.",
        }

    del _locks[key]
    return {"success": True, "message": f"Lock released on {filepath}"}


@mcp.tool(description="List all active locks and who holds them.")
def list_locks() -> dict:
    """Show all active file locks."""
    _expire_stale_locks()
    now = time.time()
    locks = []
    for fp, info in sorted(_locks.items()):
        locks.append({
            "filepath": fp,
            "held_by": info["role"],
            "locked_seconds_ago": int(now - info["locked_at"]),
        })
    return {"count": len(locks), "locks": locks}


@mcp.tool(description="Force-unlock a file. QA Lead only — use when a lock is stuck from a crashed terminal.")
def force_unlock(role: str, filepath: str) -> dict:
    """Break a stuck lock. Restricted to QA Lead."""
    if role != "qa_lead":
        return {"success": False, "error": "Only qa_lead can force-unlock files."}

    _expire_stale_locks()
    key = _normalize_path(filepath)

    if key not in _locks:
        return {"success": True, "message": "File was not locked."}

    holder = _locks[key]["role"]
    del _locks[key]
    return {"success": True, "message": f"Force-unlocked {filepath} (was held by {holder})."}


if __name__ == "__main__":
    mcp.run(transport="stdio")
