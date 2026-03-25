"""File-based lock storage with Windows file locking.

Mirrors task_store.py pattern: separate sentinel file (locks.lock)
for msvcrt.locking, data in locks.json.
"""

import json
import msvcrt
import time
from datetime import datetime, timezone
from pathlib import Path

LOCKS_FILE = Path(__file__).parent / "locks.json"
LOCK_FILE = Path(__file__).parent / "locks.lock"
EXPIRY_SECONDS = 300  # 5 minutes


def _with_lock(fn):
    """Execute fn(data) -> result with exclusive file lock."""
    if not LOCKS_FILE.exists():
        LOCKS_FILE.write_text(json.dumps({"locks": {}}, indent=2))
    LOCK_FILE.touch()

    max_retries = 20
    delay = 0.1
    for attempt in range(max_retries):
        try:
            with open(LOCK_FILE, "r+") as lf:
                msvcrt.locking(lf.fileno(), msvcrt.LK_NBLCK, 1)
                try:
                    content = LOCKS_FILE.read_text(encoding="utf-8").strip()
                    data = json.loads(content) if content else {"locks": {}}
                    result = fn(data)
                    LOCKS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
                    return result
                finally:
                    lf.seek(0)
                    msvcrt.locking(lf.fileno(), msvcrt.LK_UNLCK, 1)
        except IOError:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay = min(delay * 1.5, 1.0)  # exponential backoff, cap 1s
            else:
                raise RuntimeError("Could not acquire lock store lock after 20 attempts")


def _norm(fp: str) -> str:
    return fp.replace("\\", "/").lower()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _expire(data: dict) -> int:
    """Remove expired locks. Returns count removed."""
    now = datetime.now(timezone.utc)
    expired = []
    for fp, info in data["locks"].items():
        try:
            locked_at = datetime.fromisoformat(info["locked_at"])
            if (now - locked_at).total_seconds() > EXPIRY_SECONDS:
                expired.append(fp)
        except (ValueError, KeyError):
            expired.append(fp)
    for fp in expired:
        del data["locks"][fp]
    return len(expired)


def acquire(role: str, filepath: str) -> dict:
    """Acquire exclusive lock on a file."""
    key = _norm(filepath)

    def _op(data):
        _expire(data)
        if key in data["locks"]:
            holder = data["locks"][key]
            if holder["role"] == role:
                holder["locked_at"] = _now()
                return {"success": True, "refreshed": True}
            return {"success": False, "held_by": holder["role"]}
        data["locks"][key] = {"role": role, "locked_at": _now()}
        return {"success": True}

    return _with_lock(_op)


def release(role: str, filepath: str) -> dict:
    """Release a file lock."""
    key = _norm(filepath)

    def _op(data):
        if key in data["locks"] and data["locks"][key]["role"] == role:
            del data["locks"][key]
        return {"success": True}

    return _with_lock(_op)


def list_all() -> list[dict]:
    """List all active locks with age in seconds."""
    def _op(data):
        _expire(data)
        now = datetime.now(timezone.utc)
        result = []
        for fp, info in data["locks"].items():
            try:
                locked_at = datetime.fromisoformat(info["locked_at"])
                age = int((now - locked_at).total_seconds())
            except (ValueError, KeyError):
                age = -1
            result.append({"filepath": fp, "role": info["role"], "age": age})
        return result

    return _with_lock(_op)


def force_release(filepath: str) -> dict:
    """Force-unlock a file regardless of holder."""
    key = _norm(filepath)

    def _op(data):
        data["locks"].pop(key, None)
        return {"success": True}

    return _with_lock(_op)
