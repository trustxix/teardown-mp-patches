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


def test_find_duplicate_by_mod(tmp_path):
    """find_duplicate returns existing task ID when mod overlaps."""
    task_store.TASKS_FILE = tmp_path / "tasks.json"
    task_store.LOCK_FILE = tmp_path / "tasks.lock"
    task_store.TASKS_FILE.write_text(json.dumps({"tasks": [], "next_id": 1}))
    task_store.LOCK_FILE.touch()

    task_store.create_task("LINT-FIX: AWP (3 warnings)", "api_surgeon", "medium", "Fix lint", ["AWP"])
    dup = task_store.find_duplicate(["AWP"], "LINT-FIX")
    assert dup is not None


def test_find_duplicate_no_match(tmp_path):
    """find_duplicate returns None when no overlap."""
    task_store.TASKS_FILE = tmp_path / "tasks.json"
    task_store.LOCK_FILE = tmp_path / "tasks.lock"
    task_store.TASKS_FILE.write_text(json.dumps({"tasks": [], "next_id": 1}))
    task_store.LOCK_FILE.touch()

    task_store.create_task("LINT-FIX: AWP (3 warnings)", "api_surgeon", "medium", "Fix lint", ["AWP"])
    dup = task_store.find_duplicate(["M4A1"], "LINT-FIX")
    assert dup is None


def test_create_task_dedup(tmp_path):
    """create_task with deduplicate=True returns existing task instead of creating new."""
    task_store.TASKS_FILE = tmp_path / "tasks.json"
    task_store.LOCK_FILE = tmp_path / "tasks.lock"
    task_store.TASKS_FILE.write_text(json.dumps({"tasks": [], "next_id": 1}))
    task_store.LOCK_FILE.touch()

    id1 = task_store.create_task("LINT-FIX: AWP", "api_surgeon", "medium", "Fix", ["AWP"])
    id2 = task_store.create_task("LINT-FIX: AWP", "api_surgeon", "medium", "Fix again", ["AWP"], deduplicate=True)
    assert id1 == id2  # Same task returned, not a new one
