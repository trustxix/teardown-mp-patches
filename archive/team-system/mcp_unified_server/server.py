"""Unified MCP Server — all tools in a single process.

Instead of 5 separate MCP servers (20 Python processes across 4 terminals),
this runs everything in 1 process per terminal (4 total).
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server import FastMCP
from mcp_task_server import task_store
from mcp_task_server.server import (
    heartbeat as _heartbeat,
    get_heartbeats as _get_heartbeats,
    check_terminal_health as _check_health,
    auto_commit as _auto_commit,
    generate_tasks_from_lint as _gen_tasks_lint,
    team_log as _team_log,
)

mcp = FastMCP(
    name="teardown-team",
    instructions="Unified server for Teardown MP Patches. All team tools in one server.",
)

COMMS_DIR = PROJECT_ROOT / ".comms"


def _load_roles() -> set[str]:
    """Discover roles from ROLE_*.md files and .comms/ inbox directories."""
    roles = set()
    for f in PROJECT_ROOT.glob("ROLE_*.md"):
        roles.add(f.stem.replace("ROLE_", "").lower())
    if COMMS_DIR.exists():
        for d in COMMS_DIR.iterdir():
            if d.is_dir() and (d / "inbox").is_dir() and d.name != "__pycache__":
                roles.add(d.name)
    return roles


VALID_ROLES = _load_roles()


def _write_roles_json():
    """Write roles.json for other systems to read."""
    data = {"roles": sorted(VALID_ROLES), "last_scanned": datetime.now(timezone.utc).isoformat()}
    (PROJECT_ROOT / "roles.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


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
def create_task(title: str, role: str, priority: str, description: str,
                mods: list[str] | None = None, deduplicate: bool = False) -> dict:
    """Create a new task. Set deduplicate=True to avoid creating duplicates."""
    tid = task_store.create_task(title, role, priority, description, mods, deduplicate=deduplicate)
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
    """Read inbox messages. Auto-archives messages older than 60 minutes (except critical priority)."""
    inbox = COMMS_DIR / role / "inbox"
    if not inbox.exists():
        return "Inbox empty"
    archive = COMMS_DIR / role / "archive"
    now = datetime.now(timezone.utc)
    msgs = []
    for f in sorted(inbox.glob("*.md")):
        # Parse age from filename: YYYYMMDD_HHMMSS_...
        try:
            ts_str = f.name[:15]  # "20260319_154635"
            file_time = datetime.strptime(ts_str, "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc)
            age_minutes = (now - file_time).total_seconds() / 60
        except (ValueError, IndexError):
            age_minutes = 0

        content = f.read_text(encoding="utf-8", errors="replace")

        # Archive stale non-critical messages
        if age_minutes > 60 and "priority: critical" not in content[:500].lower():
            archive.mkdir(parents=True, exist_ok=True)
            f.rename(archive / f.name)
            continue

        msgs.append({"filename": f.name, "content": content})
    return msgs if msgs else "Inbox empty"


@mcp.tool()
def archive_stale_messages(role: str, max_age_minutes: int = 60) -> dict:
    """Manually archive messages older than max_age_minutes. Critical-priority messages are exempt."""
    inbox = COMMS_DIR / role / "inbox"
    if not inbox.exists():
        return {"archived": 0}
    archive = COMMS_DIR / role / "archive"
    now = datetime.now(timezone.utc)
    count = 0
    for f in inbox.glob("*.md"):
        try:
            ts_str = f.name[:15]
            file_time = datetime.strptime(ts_str, "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc)
            if (now - file_time).total_seconds() / 60 > max_age_minutes:
                content = f.read_text(encoding="utf-8", errors="replace")
                if "priority: critical" in content[:500].lower():
                    continue  # Never archive critical messages
                archive.mkdir(parents=True, exist_ok=True)
                f.rename(archive / f.name)
                count += 1
        except (ValueError, IndexError):
            pass
    return {"archived": count}


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
        _write_roles_json()
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


# ── ROLE MANAGEMENT ───────────────────────────────────

@mcp.tool()
def refresh_roles() -> dict:
    """Re-scan for roles and update roles.json."""
    global VALID_ROLES
    VALID_ROLES = _load_roles()
    _write_roles_json()
    return {"roles": sorted(VALID_ROLES)}


# ── TASK SERVER TOOLS (delegated) ─────────────────────

@mcp.tool()
def heartbeat(role: str, status: str = "working") -> dict:
    """Report alive status for terminal health tracking."""
    return _heartbeat(role, status)


@mcp.tool()
def get_heartbeats() -> dict:
    """Get heartbeat status for all terminals."""
    return _get_heartbeats()


@mcp.tool()
def check_terminal_health() -> dict:
    """Check health of all terminals. Returns stale/dead terminals and orphaned tasks."""
    return _check_health()


@mcp.tool()
def auto_commit(message: str | None = None) -> dict:
    """Auto-commit project state. Backs up state files first. QA Lead only."""
    backup_state("pre-commit")
    return _auto_commit(message)


@mcp.tool()
def generate_tasks_from_lint(role: str = "api_surgeon", priority: str = "medium") -> dict:
    """Generate tasks from lint findings. Groups by mod, skips mods with existing tasks."""
    return _gen_tasks_lint(role, priority)


@mcp.tool()
def team_log(role: str, event: str, detail: str) -> dict:
    """Append structured entry to team.log."""
    return _team_log(role, event, detail)


# ── METRICS ───────────────────────────────────────────

from mcp_task_server import metrics as _metrics


@mcp.tool()
def get_metrics() -> dict:
    """Get team performance metrics (throughput, avg task time, by role)."""
    return _metrics.compute()


# ── HANDOFF TOOLS ─────────────────────────────────────

@mcp.tool()
def save_handoff(role: str, current_task_id: str, notes: str) -> dict:
    """Save handoff note for graceful context overflow recovery."""
    handoff = COMMS_DIR / role / "handoff.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    content = f"---\ntask_id: {current_task_id}\nsaved_at: {datetime.now(timezone.utc).isoformat()}\n---\n\n{notes}"
    handoff.write_text(content, encoding="utf-8")
    return {"success": True, "path": str(handoff)}


@mcp.tool()
def check_handoff(role: str) -> dict | str:
    """Check for handoff note from a previous session. Deletes it after reading."""
    handoff = COMMS_DIR / role / "handoff.md"
    if not handoff.exists():
        return "No handoff note found."
    content = handoff.read_text(encoding="utf-8", errors="replace")
    handoff.unlink()
    return {"found": True, "content": content}


# ── SESSION RETROSPECTIVE ─────────────────────────────

@mcp.tool()
def save_retro(what_worked: str, what_stalled: str, improvements: str, role_changes: str) -> dict:
    """Save a session retrospective. QA Lead calls this before killswitch."""
    retro_dir = PROJECT_ROOT / "docs" / "retros"
    retro_dir.mkdir(parents=True, exist_ok=True)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    retro_file = retro_dir / f"{date}-retro.md"
    content = f"""# Session Retrospective — {date}

## What Worked Well
{what_worked}

## What Caused Stalls / Confusion
{what_stalled}

## Improvements Identified
{improvements}

## Role File Changes Needed
{role_changes}
"""
    retro_file.write_text(content, encoding="utf-8")
    return {"success": True, "path": str(retro_file)}


# ── BACKUP ────────────────────────────────────────────

import shutil


@mcp.tool()
def backup_state(label: str = "auto") -> dict:
    """Backup critical state files. Keeps last 3 backups."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_dir = PROJECT_ROOT / "backups" / f"{ts}_{label}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    files_to_backup = [
        PROJECT_ROOT / "mcp_task_server" / "tasks.json",
        PROJECT_ROOT / "mcp_change_tracker" / "changes.json",
        COMMS_DIR / "heartbeats.json",
        PROJECT_ROOT / "mcp_task_server" / "locks.json",
    ]
    backed_up = []
    for f in files_to_backup:
        if f.exists():
            shutil.copy2(f, backup_dir / f.name)
            backed_up.append(f.name)

    # Keep only last 3 backup directories
    backups_root = PROJECT_ROOT / "backups"
    all_backups = sorted(
        [d for d in backups_root.iterdir() if d.is_dir()],
        reverse=True,
    )
    for old in all_backups[3:]:
        shutil.rmtree(old)

    return {"success": True, "path": str(backup_dir), "files": backed_up}


# ── ERROR REPORTING ───────────────────────────────────

@mcp.tool()
def report_error(role: str, error_type: str, details: str, task_id: str | None = None) -> dict:
    """Report an error for dashboard visibility. All terminals should call this on unresolvable errors."""
    errors_file = PROJECT_ROOT / "logs" / "errors.json"
    errors_file.parent.mkdir(parents=True, exist_ok=True)

    errors = []
    if errors_file.exists():
        try:
            errors = json.loads(errors_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            errors = []

    errors.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "type": error_type,
        "details": details,
        "task_id": task_id,
    })

    # Keep last 100
    errors = errors[-100:]
    errors_file.write_text(json.dumps(errors, indent=2), encoding="utf-8")
    return {"success": True}


# Write roles.json on startup
_write_roles_json()

if __name__ == "__main__":
    mcp.run(transport="stdio")
