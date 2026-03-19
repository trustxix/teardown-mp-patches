"""JSON file-based task storage with Windows file locking."""

import json
import msvcrt
from datetime import datetime, timezone
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"
LOCK_FILE = Path(__file__).parent / "tasks.lock"


def _with_lock(fn):
    """Execute fn(data) -> result with exclusive file lock.

    Uses a separate lock file so the lock byte count stays constant
    even as tasks.json grows/shrinks during writes.
    Retries up to 10 times with 0.2s delay if lock is held.
    Falls back to unlocked read if lock fails completely.
    """
    import time

    # Ensure files exist
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text(json.dumps({"tasks": [], "next_id": 1}, indent=2))
    LOCK_FILE.touch()

    max_retries = 10
    for attempt in range(max_retries):
        try:
            with open(LOCK_FILE, "r+") as lf:
                # Non-blocking lock attempt
                msvcrt.locking(lf.fileno(), msvcrt.LK_NBLCK, 1)
                try:
                    content = TASKS_FILE.read_text(encoding="utf-8").strip()
                    data = json.loads(content) if content else {"tasks": [], "next_id": 1}
                    result = fn(data)
                    TASKS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
                    return result
                finally:
                    lf.seek(0)
                    msvcrt.locking(lf.fileno(), msvcrt.LK_UNLCK, 1)
        except IOError:
            if attempt < max_retries - 1:
                time.sleep(0.2)
            else:
                # Fallback: read without lock (safe for reads, risky for writes)
                content = TASKS_FILE.read_text(encoding="utf-8").strip()
                data = json.loads(content) if content else {"tasks": [], "next_id": 1}
                result = fn(data)
                try:
                    TASKS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
                except:
                    pass
                return result


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


STALE_TIMEOUT_BY_PRIORITY = {
    "critical": 5,
    "high": 15,
    "medium": 30,
    "low": 45,
}
STALE_TIMEOUT_DEFAULT = 30


def _recover_stale(data):
    """Auto-recover tasks stuck IN_PROGRESS based on priority-specific timeouts.

    critical: 5min, high: 15min, medium: 30min, low: 45min.
    """
    now = datetime.now(timezone.utc)
    recovered = 0
    for t in data["tasks"]:
        if t["status"] == "in_progress" and t.get("started_at"):
            try:
                started = datetime.fromisoformat(t["started_at"])
                elapsed = (now - started).total_seconds() / 60
                timeout = STALE_TIMEOUT_BY_PRIORITY.get(
                    t.get("priority", "medium"), STALE_TIMEOUT_DEFAULT
                )
                if elapsed > timeout:
                    t["status"] = "open"
                    t["assigned_to"] = None
                    t["started_at"] = None
                    recovered += 1
            except (ValueError, TypeError):
                pass
    return recovered


def get_next_task(role: str) -> dict | None:
    """Get next OPEN task for role, mark it IN_PROGRESS. Auto-recovers stale tasks."""
    def _op(data):
        # Auto-recover stuck tasks first
        _recover_stale(data)

        # Priority order: critical > high > medium > low
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        # Maintainer picks up tasks for all 3 specialist roles it replaces
        match_roles = {role}
        if role == "maintainer":
            match_roles |= {"api_surgeon", "mod_converter", "docs_keeper"}
        candidates = [
            t for t in data["tasks"]
            if t["role"] in match_roles and t["status"] == "open"
        ]
        candidates.sort(key=lambda t: priority_order.get(t.get("priority", "medium"), 2))
        if not candidates:
            return None
        task = candidates[0]
        task["status"] = "in_progress"
        task["assigned_to"] = role
        task["started_at"] = _now()
        return dict(task)
    return _with_lock(_op)


def complete_task(task_id: str, summary: str) -> bool:
    """Mark task DONE with completion summary."""
    def _op(data):
        for t in data["tasks"]:
            if t["id"] == task_id:
                t["status"] = "done"
                t["completed_at"] = _now()
                t["completion_summary"] = summary
                # Flag for QA review if task involved mod code
                if t.get("mods"):
                    t["review_status"] = "pending"
                return True
        return False
    return _with_lock(_op)


def create_task(title: str, role: str, priority: str, description: str, mods: list[str] | None = None) -> str:
    """Create a new task, return its ID."""
    def _op(data):
        task_id = f"T{data['next_id']}"
        data["next_id"] += 1
        task = {
            "id": task_id,
            "title": title,
            "role": role,
            "priority": priority,
            "status": "open",
            "description": description,
            "mods": mods or [],
            "created_by": "mcp",
            "created_at": _now(),
            "assigned_to": None,
            "started_at": None,
            "completed_at": None,
            "completion_summary": None,
            "review_status": None,
            "review_notes": None,
        }
        data["tasks"].append(task)
        return task_id
    return _with_lock(_op)


def review_task(task_id: str, approved: bool, notes: str) -> bool:
    """QA review of a completed task. Reopens if not approved."""
    def _op(data):
        for t in data["tasks"]:
            if t["id"] == task_id:
                if approved:
                    t["review_status"] = "approved"
                    t["review_notes"] = notes
                else:
                    # Reopen with notes
                    t["status"] = "open"
                    t["review_status"] = "rejected"
                    t["review_notes"] = notes
                    t["assigned_to"] = None
                    t["completed_at"] = None
                    t["completion_summary"] = None
                return True
        return False
    return _with_lock(_op)


def get_all_tasks() -> dict:
    """Return full status summary."""
    def _op(data):
        tasks = data["tasks"]
        by_status = {"open": [], "in_progress": [], "done": []}
        by_role = {}
        for t in tasks:
            status = t["status"]
            by_status.setdefault(status, []).append(t)
            role = t["role"]
            by_role.setdefault(role, {"open": 0, "in_progress": 0, "done": 0})
            by_role[role][status] = by_role[role].get(status, 0) + 1

        return {
            "total": len(tasks),
            "counts": {s: len(v) for s, v in by_status.items()},
            "by_role": by_role,
            "active": [t for t in tasks if t["status"] == "in_progress"],
            "recently_completed": sorted(
                [t for t in tasks if t["status"] == "done"],
                key=lambda t: t.get("completed_at") or "",
                reverse=True,
            )[:10],
            "pending_review": [t for t in tasks if t.get("review_status") == "pending"],
            "open_tasks": by_status.get("open", []),
        }
    return _with_lock(_op)
