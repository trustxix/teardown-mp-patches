import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from mcp_task_server import metrics


def _make_tasks(tmp_path, tasks_data):
    f = tmp_path / "tasks.json"
    f.write_text(json.dumps(tasks_data, indent=2))
    return f


def test_throughput_calculation(tmp_path):
    """Throughput = completed tasks per hour."""
    now = datetime.now(timezone.utc)
    tasks = {
        "tasks": [
            {"id": "T1", "status": "done", "role": "api_surgeon",
             "started_at": (now - timedelta(hours=1)).isoformat(),
             "completed_at": (now - timedelta(minutes=30)).isoformat()},
            {"id": "T2", "status": "done", "role": "api_surgeon",
             "started_at": (now - timedelta(minutes=30)).isoformat(),
             "completed_at": now.isoformat()},
        ],
        "next_id": 3,
    }
    f = _make_tasks(tmp_path, tasks)
    result = metrics.compute(tasks_file=f)
    assert result["throughput_per_hour"] > 0
    assert "avg_time_minutes" in result


def test_empty_tasks(tmp_path):
    """Empty task file returns zero metrics."""
    f = _make_tasks(tmp_path, {"tasks": [], "next_id": 1})
    result = metrics.compute(tasks_file=f)
    assert result["throughput_per_hour"] == 0
