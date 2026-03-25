"""Compute team metrics from existing task/heartbeat data."""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"


def compute(tasks_file: Path | None = None, hours_window: int = 24) -> dict:
    """Compute metrics from tasks.json over the given time window."""
    tf = tasks_file or TASKS_FILE
    if not tf.exists():
        return {"throughput_per_hour": 0, "avg_time_minutes": 0,
                "by_role": {}, "completed_in_window": 0}

    try:
        data = json.loads(tf.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"throughput_per_hour": 0, "avg_time_minutes": 0,
                "by_role": {}, "completed_in_window": 0}

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=hours_window)
    tasks = data.get("tasks", [])

    # Completed tasks in window
    completed = []
    for t in tasks:
        if t.get("status") != "done" or not t.get("completed_at"):
            continue
        try:
            completed_at = datetime.fromisoformat(t["completed_at"])
            if completed_at >= cutoff:
                completed.append(t)
        except (ValueError, TypeError):
            pass

    # Throughput
    throughput = len(completed) / hours_window if hours_window > 0 else 0

    # Avg time per task
    durations = []
    by_role = {}
    for t in completed:
        role = t.get("role", "unknown")
        by_role.setdefault(role, {"completed": 0, "total_minutes": 0})
        by_role[role]["completed"] += 1
        if t.get("started_at") and t.get("completed_at"):
            try:
                started = datetime.fromisoformat(t["started_at"])
                finished = datetime.fromisoformat(t["completed_at"])
                mins = (finished - started).total_seconds() / 60
                durations.append(mins)
                by_role[role]["total_minutes"] += mins
            except (ValueError, TypeError):
                pass

    for role_data in by_role.values():
        if role_data["completed"] > 0:
            role_data["avg_minutes"] = round(role_data["total_minutes"] / role_data["completed"], 1)

    avg_time = round(sum(durations) / len(durations), 1) if durations else 0

    return {
        "throughput_per_hour": round(throughput, 2),
        "avg_time_minutes": avg_time,
        "completed_in_window": len(completed),
        "by_role": by_role,
        "window_hours": hours_window,
    }
