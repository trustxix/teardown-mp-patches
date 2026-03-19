import json
from pathlib import Path
from unittest.mock import patch
from mcp_task_server import task_store


def test_lock_exhaustion_raises(tmp_path):
    """After exhausting retries, task store raises RuntimeError instead of writing unlocked."""
    task_store.TASKS_FILE = tmp_path / "tasks.json"
    task_store.LOCK_FILE = tmp_path / "tasks.lock"
    task_store.TASKS_FILE.write_text(json.dumps({"tasks": [], "next_id": 1}))
    task_store.LOCK_FILE.touch()

    # Mock msvcrt.locking to always fail
    import msvcrt
    with patch.object(msvcrt, "locking", side_effect=IOError("lock held")):
        try:
            task_store.get_all_tasks()
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "lock" in str(e).lower()


def test_normal_lock_still_works(tmp_path):
    """Normal operation (no contention) still works."""
    task_store.TASKS_FILE = tmp_path / "tasks.json"
    task_store.LOCK_FILE = tmp_path / "tasks.lock"
    task_store.TASKS_FILE.write_text(json.dumps({"tasks": [], "next_id": 1}))
    task_store.LOCK_FILE.touch()

    result = task_store.get_all_tasks()
    assert result["total"] == 0
    assert "counts" in result
