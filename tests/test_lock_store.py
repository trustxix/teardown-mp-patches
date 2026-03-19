import json
from pathlib import Path
from mcp_task_server import lock_store


def test_acquire_lock(tmp_path):
    """A role can acquire a lock on a file."""
    lock_store.LOCKS_FILE = tmp_path / "locks.json"
    lock_store.LOCK_FILE = tmp_path / "locks.lock"
    result = lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    assert result["success"] is True
    # Verify it's persisted
    data = json.loads(lock_store.LOCKS_FILE.read_text())
    assert "c:/mods/awp/main.lua" in data["locks"]


def test_lock_conflict(tmp_path):
    """A second role cannot acquire a lock held by another."""
    lock_store.LOCKS_FILE = tmp_path / "locks.json"
    lock_store.LOCK_FILE = tmp_path / "locks.lock"
    lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    result = lock_store.acquire("mod_converter", "c:/mods/awp/main.lua")
    assert result["success"] is False
    assert result["held_by"] == "api_surgeon"


def test_release_lock(tmp_path):
    """Releasing a lock allows another role to acquire it."""
    lock_store.LOCKS_FILE = tmp_path / "locks.json"
    lock_store.LOCK_FILE = tmp_path / "locks.lock"
    lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    lock_store.release("api_surgeon", "c:/mods/awp/main.lua")
    result = lock_store.acquire("mod_converter", "c:/mods/awp/main.lua")
    assert result["success"] is True


def test_lock_refresh(tmp_path):
    """Same role re-acquiring refreshes the timestamp."""
    lock_store.LOCKS_FILE = tmp_path / "locks.json"
    lock_store.LOCK_FILE = tmp_path / "locks.lock"
    lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    result = lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    assert result["success"] is True
    assert result.get("refreshed") is True


def test_lock_expiry(tmp_path):
    """Locks older than expiry_seconds are cleaned up."""
    lock_store.LOCKS_FILE = tmp_path / "locks.json"
    lock_store.LOCK_FILE = tmp_path / "locks.lock"
    lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    # Manually backdate the lock
    data = json.loads(lock_store.LOCKS_FILE.read_text())
    data["locks"]["c:/mods/awp/main.lua"]["locked_at"] = "2020-01-01T00:00:00+00:00"
    lock_store.LOCKS_FILE.write_text(json.dumps(data))
    # Now another role should be able to acquire (expired lock cleaned)
    result = lock_store.acquire("mod_converter", "c:/mods/awp/main.lua")
    assert result["success"] is True


def test_list_locks(tmp_path):
    """List returns all active locks with age."""
    lock_store.LOCKS_FILE = tmp_path / "locks.json"
    lock_store.LOCK_FILE = tmp_path / "locks.lock"
    lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    lock_store.acquire("mod_converter", "c:/mods/m4/main.lua")
    locks = lock_store.list_all()
    assert len(locks) == 2
    assert any(l["role"] == "api_surgeon" for l in locks)


def test_force_unlock(tmp_path):
    """Force unlock removes any lock regardless of holder."""
    lock_store.LOCKS_FILE = tmp_path / "locks.json"
    lock_store.LOCK_FILE = tmp_path / "locks.lock"
    lock_store.acquire("api_surgeon", "c:/mods/awp/main.lua")
    lock_store.force_release("c:/mods/awp/main.lua")
    result = lock_store.acquire("mod_converter", "c:/mods/awp/main.lua")
    assert result["success"] is True
