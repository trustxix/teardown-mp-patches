"""Unified MCP Server — all tools in a single process.

Instead of 5 separate MCP servers (20 Python processes across 4 terminals),
this runs everything in 1 process per terminal (4 total).
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server import FastMCP
from mcp_task_server import task_store

mcp = FastMCP(
    name="teardown-team",
    instructions="Unified server for Teardown MP Patches. All team tools in one server.",
)

COMMS_DIR = PROJECT_ROOT / ".comms"
VALID_ROLES = {"api_surgeon", "mod_converter", "qa_lead", "docs_keeper", "maintainer"}


def _ts():
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


# ── TASK TOOLS ─────────────────────────────────────────

@mcp.tool()
def get_task(role: str) -> dict | str:
    """Get next open task for role. Auto-broadcasts start."""
    if role not in VALID_ROLES:
        return f"Invalid role. Must be: {', '.join(sorted(VALID_ROLES))}"
    task = task_store.get_next_task(role)
    if not task:
        return f"No open tasks for {role}"
    mods = ", ".join(task.get("mods", [])[:5]) or "general"
    broadcast(role, "info", "low", f"STARTING: [{task['id']}] {task['title']} — mods: {mods}")
    return task


@mcp.tool()
def complete_task(task_id: str, summary: str) -> dict:
    """Mark task DONE. Auto-broadcasts completion."""
    all_t = task_store.get_all_tasks()
    role = title = None
    for t in all_t.get("tasks", []):
        if t["id"] == task_id:
            role = t.get("assigned_to") or t.get("role")
            title = t.get("title", "")
    success = task_store.complete_task(task_id, summary)
    if success and role:
        broadcast(role, "info", "low", f"FINISHED: [{task_id}] {title}\n{summary}")
    return {"success": success, "task_id": task_id}


@mcp.tool()
def create_task(title: str, role: str, priority: str, description: str, mods: list[str] | None = None) -> dict:
    """Create a new task."""
    tid = task_store.create_task(title, role, priority, description, mods)
    return {"success": True, "task_id": tid}


@mcp.tool()
def review_task(task_id: str, approved: bool, notes: str) -> dict:
    """QA review of a completed task."""
    return {"success": task_store.review_task(task_id, approved, notes)}


@mcp.tool()
def get_status() -> dict:
    """Full queue status."""
    return task_store.get_all_tasks()


@mcp.tool()
def get_lint_summary() -> dict:
    """Run linter, return summary."""
    try:
        r = subprocess.run([sys.executable, "-m", "tools.lint"], capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=60)
        out = r.stdout + r.stderr
        c = {"FAIL": out.count("[FAIL]"), "WARN": out.count("[WARN]"), "INFO": out.count("[INFO]")}
        return {"counts": c, "total": sum(c.values())}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_audit_summary() -> dict:
    """Run audit, return feature matrix."""
    try:
        r = subprocess.run([sys.executable, "-m", "tools.audit"], capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=60)
        return {"report": (r.stdout + r.stderr).strip()}
    except Exception as e:
        return {"error": str(e)}


# ── DASHBOARD ──────────────────────────────────────────

@mcp.tool()
def team_dashboard() -> dict:
    """One-command team overview."""
    inboxes = {}
    for role in VALID_ROLES:
        inbox = COMMS_DIR / role / "inbox"
        msgs = list(inbox.glob("*.md")) if inbox.exists() else []
        inboxes[role] = {"count": len(msgs), "urgent": sum(1 for m in msgs if "critical" in m.read_text(encoding="utf-8", errors="replace")[:200].lower())}
    at = task_store.get_all_tasks()
    return {
        "inboxes": inboxes,
        "tasks": {"open": at["counts"].get("open", 0), "in_progress": at["counts"].get("in_progress", 0), "done": at["counts"].get("done", 0)},
        "killswitch": (COMMS_DIR / "STOP").exists(),
    }


# ── KILLSWITCH ─────────────────────────────────────────

@mcp.tool()
def killswitch() -> dict:
    """Activate killswitch. Broadcasts STOP to all."""
    (COMMS_DIR / "STOP").write_text("STOP", encoding="utf-8")
    for role in VALID_ROLES:
        inbox = COMMS_DIR / role / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        (inbox / f"{_ts()}_qa_lead_stop.md").write_text(f"---\nfrom: qa_lead\nto: {role}\ntype: info\npriority: critical\n---\n\nSTOP ORDER: Finish current task, then HALT.", encoding="utf-8")
    return {"success": True}


@mcp.tool()
def check_killswitch() -> dict:
    """Check if killswitch is active."""
    return {"active": (COMMS_DIR / "STOP").exists()}


@mcp.tool()
def clear_killswitch() -> dict:
    """Deactivate killswitch. Broadcasts RESUME."""
    s = COMMS_DIR / "STOP"
    if s.exists():
        s.unlink()
    for role in VALID_ROLES:
        inbox = COMMS_DIR / role / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        (inbox / f"{_ts()}_qa_lead_resume.md").write_text(f"---\nfrom: qa_lead\nto: {role}\ntype: info\npriority: critical\n---\n\nRESUME ORDER: Killswitch cleared. Resume work.", encoding="utf-8")
    return {"success": True}


# ── INBOX ──────────────────────────────────────────────

@mcp.tool()
def has_mail(role: str) -> dict:
    """Quick check for unread messages."""
    inbox = COMMS_DIR / role / "inbox"
    msgs = list(inbox.glob("*.md")) if inbox.exists() else []
    return {"has_mail": len(msgs) > 0, "count": len(msgs)}


@mcp.tool()
def get_focus() -> str:
    """Read current team focus area."""
    fp = COMMS_DIR / "FOCUS.md"
    return fp.read_text(encoding="utf-8", errors="replace") if fp.exists() else "No focus set."


@mcp.tool()
def check_inbox(role: str) -> list[dict] | str:
    """Read all inbox messages."""
    inbox = COMMS_DIR / role / "inbox"
    if not inbox.exists():
        return "Inbox empty"
    msgs = [{"filename": f.name, "content": f.read_text(encoding="utf-8", errors="replace")} for f in sorted(inbox.glob("*.md"))]
    return msgs if msgs else "Inbox empty"


@mcp.tool()
def send_message(from_role: str, to_role: str, msg_type: str, priority: str, content: str) -> dict:
    """Send a message to another terminal."""
    ts = _ts()
    fn = f"{ts}_{from_role}_{msg_type}.md"
    full = f"---\nfrom: {from_role}\nto: {to_role}\ntype: {msg_type}\npriority: {priority}\n---\n\n{content}"
    inbox = COMMS_DIR / to_role / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / fn).write_text(full, encoding="utf-8")
    outbox = COMMS_DIR / from_role / "outbox"
    outbox.mkdir(parents=True, exist_ok=True)
    (outbox / fn).write_text(full, encoding="utf-8")
    return {"success": True, "filename": fn}


@mcp.tool()
def broadcast(from_role: str, msg_type: str, priority: str, content: str) -> dict:
    """Broadcast to all other terminals."""
    for role in VALID_ROLES:
        if role != from_role:
            send_message(from_role, role, msg_type, priority, content)
    return {"success": True}


@mcp.tool()
def clear_message(role: str, filename: str) -> dict:
    """Delete a processed inbox message."""
    p = COMMS_DIR / role / "inbox" / filename
    if p.exists():
        p.unlink()
    return {"success": True}


# ── SPAWN TERMINAL ─────────────────────────────────────

@mcp.tool()
def spawn_terminal(role_name: str, display_name: str, role_file_content: str) -> dict:
    """Create a new team member with role file, inbox, and desktop launcher."""
    try:
        rf = f"ROLE_{role_name.upper()}.md"
        (PROJECT_ROOT / rf).write_text(role_file_content, encoding="utf-8")
        (COMMS_DIR / role_name / "inbox").mkdir(parents=True, exist_ok=True)
        (COMMS_DIR / role_name / "outbox").mkdir(parents=True, exist_ok=True)
        VALID_ROLES.add(role_name)
        prompt = f"Read {rf} and start your autonomous work loop. You are {role_name}. Run tools.status first, then get_focus, check_inbox, and get_task. Keep working forever."
        bat = f'@echo off\nstart "{display_name}" "C:\\Program Files\\PowerShell\\7\\pwsh.exe" -NoExit -Command "cd C:\\Users\\trust\\teardown-mp-patches; claude --dangerously-skip-permissions \'{prompt}\'"\n'
        lp = Path(f"C:/Users/trust/Desktop/launch_{role_name}.bat")
        lp.write_text(bat, encoding="utf-8")
        return {"success": True, "role_file": rf, "launcher": str(lp)}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── FILE LOCK (shared across terminals via file) ─────

from mcp_task_server import lock_store


@mcp.tool()
def lock_file(role: str, filepath: str) -> dict:
    """Acquire exclusive lock on a file (shared across all terminals)."""
    return lock_store.acquire(role, filepath)


@mcp.tool()
def unlock_file(role: str, filepath: str) -> dict:
    """Release a file lock."""
    return lock_store.release(role, filepath)


@mcp.tool()
def list_locks() -> list[dict]:
    """List all active file locks."""
    return lock_store.list_all()


@mcp.tool()
def force_unlock(role: str, filepath: str) -> dict:
    """Force-unlock a file. QA Lead only."""
    if role != "qa_lead":
        return {"success": False, "message": "Only qa_lead can force unlock"}
    return lock_store.force_release(filepath)


# ── CHANGE TRACKER ─────────────────────────────────────

from mcp_change_tracker.server import (
    record_change as _rc, get_changes as _gc, get_changes_by_mod as _gcm,
    get_undocumented_changes as _guc, mark_documented as _md,
    mark_all_documented as _mad, get_change_summary as _gcs,
)


@mcp.tool()
def record_change(role: str, mod_name: str, change_type: str, description: str) -> dict:
    """Record a project change for doc tracking."""
    return _rc(role, mod_name, change_type, description)


@mcp.tool()
def get_recent_changes(since_minutes: int = 60) -> list[dict] | str:
    """Get changes from last N minutes."""
    return _gc(since_minutes)


@mcp.tool()
def get_mod_changes(mod_name: str) -> list[dict] | str:
    """Get all changes for a mod."""
    return _gcm(mod_name)


@mcp.tool()
def get_undocumented() -> list[dict] | str:
    """Get changes not yet documented."""
    return _guc()


@mcp.tool()
def mark_change_documented(change_id: int) -> dict:
    """Mark a change as documented."""
    return _md(change_id)


@mcp.tool()
def mark_all_changes_documented(change_ids: list[int]) -> dict:
    """Batch mark changes as documented."""
    return _mad(change_ids)


@mcp.tool()
def change_summary() -> dict:
    """Dashboard of change activity."""
    return _gcs()


# ── TEMPLATE ENGINE ────────────────────────────────────

from mcp_template_server.server import (
    generate_options_menu as _gom, generate_keybind_hints as _gkh,
    generate_player_data as _gpd, generate_server_init as _gsi,
    generate_server_tick as _gst, generate_client_tick as _gct,
    generate_ammo_display as _gad,
)


@mcp.tool()
def gen_options_menu(tool_id: str, display_name: str, settings: list[dict]) -> dict:
    """Generate O-key options menu Lua code."""
    return _gom(tool_id, display_name, settings)


@mcp.tool()
def gen_keybind_hints(keybinds: list[dict], position: str = "bottom_left") -> str:
    """Generate keybind hints Lua code."""
    return _gkh(keybinds, position)


@mcp.tool()
def gen_player_data(fields: list[dict]) -> str:
    """Generate createPlayerData() Lua code."""
    return _gpd(fields)


@mcp.tool()
def gen_server_init(tool_id: str, display_name: str, vox_path: str, group: int, ammo_pickup: int = 0) -> str:
    """Generate server.init() Lua code."""
    return _gsi(tool_id, display_name, vox_path, group, ammo_pickup)


@mcp.tool()
def gen_server_tick(tool_id: str, ammo_amount: int = 101, extra_init_lines: str = "") -> str:
    """Generate server.tick() Lua code."""
    return _gst(tool_id, ammo_amount, extra_init_lines)


@mcp.tool()
def gen_client_tick() -> str:
    """Generate client.tick() Lua code."""
    return _gct()


@mcp.tool()
def gen_ammo_display(mag_size: int, show_reload: bool = True) -> str:
    """Generate ammo HUD Lua code."""
    return _gad(mag_size, show_reload)


# ── MOD REGISTRY ──────────────────────────────────────

from mcp_registry_server.server import (
    query_mod as _qm, query_mods as _qms,
    refresh_registry as _rr, get_mod_diff as _gmd,
)


@mcp.tool()
def query_mod(mod_name: str) -> dict | str:
    """Get full metadata for a mod."""
    return _qm(mod_name)


@mcp.tool()
def query_mods_by_filter(filter: str) -> list[dict] | str:
    """Filter mods by feature: missing_shoot, missing_options, is_gun, etc."""
    return _qms(filter)


@mcp.tool()
def refresh_mod_registry() -> dict:
    """Re-scan all mods."""
    return _rr()


@mcp.tool()
def get_mod_registry_diff(mod_name: str) -> dict | str:
    """Get changes for a specific mod since last scan."""
    return _gmd(mod_name)


if __name__ == "__main__":
    mcp.run(transport="stdio")
