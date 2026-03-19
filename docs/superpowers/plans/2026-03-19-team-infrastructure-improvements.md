# Team Infrastructure Improvements — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix critical bugs in the multi-agent team coordination system (broken file locks, data corruption risk) and add reliability/workflow improvements (watchdog, metrics, interactive dashboard).

**Architecture:** 4 phases of changes to the unified MCP server, task store, dashboard, and launch scripts. Existing `mcp_task_server` tools are imported/exposed through the unified server (same delegation pattern already used for change_tracker, template_engine, registry). New shared state uses file-based storage with sentinel locks (proven pattern from task_store.py).

**Tech Stack:** Python 3.10+, FastMCP, msvcrt (Windows file locking), PowerShell 7 (watchdog), HTTP server (dashboard), pytest

**Spec:** `docs/superpowers/specs/2026-03-19-team-infrastructure-improvements-design.md`

---

## File Map

| File | Responsibility | Phase |
|------|---------------|-------|
| `mcp_task_server/task_store.py` | Task storage with file locking — fix fallback, add deduplication | P0, P1 |
| `mcp_task_server/lock_store.py` | **NEW** — File-based lock storage (mirrors task_store.py pattern) | P0 |
| `mcp_unified_server/server.py` | Unified MCP server — replace in-memory locks, expose task_server tools, add new tools | P0, P1, P2, P3 |
| `dashboard/server.py` | Dashboard HTTP server — add POST endpoints, error indicator | P2, P3 |
| `dashboard/index.html` | Dashboard UI — add interactive controls, metrics, errors | P2, P3 |
| `mcp_task_server/metrics.py` | **NEW** — Metrics computation from existing data | P2 |
| `watchdog.ps1` | **NEW** — Terminal health monitor + auto-restart | P1 |
| `launch_team.bat` (Desktop/Team/) | Launch script — add watchdog, pre-launch validation | P1, P2 |
| `launch_team_maintenance.bat` (Desktop/Team/) | Maintenance launch — same additions | P1, P2 |
| `ROLE_QA_LEAD.md` | QA Lead role — add handoff, retro, error reporting | P1, P3 |
| `ROLE_API_SURGEON.md` | API Surgeon role — add handoff check | P1 |
| `ROLE_MOD_CONVERTER.md` | Mod Converter role — add handoff check | P1 |
| `ROLE_DOCS_KEEPER.md` | Docs Keeper role — add handoff check | P1 |
| `ROLE_MAINTAINER.md` | Maintainer role — add handoff check | P1 |
| `tests/test_lock_store.py` | **NEW** — Tests for file-based locks | P0 |
| `tests/test_task_store_locking.py` | **NEW** — Tests for task store lock safety | P0 |
| `tests/test_unified_server.py` | **NEW** — Tests for unified server tool wrappers | P1 |
| `tests/test_metrics.py` | **NEW** — Tests for metrics computation | P2 |

---

## Phase 0: Critical Bug Fixes

> **IMPORTANT:** After Phase 0, the human runs `python -m pytest tests/ -q` directly. Do NOT launch the team until all tests pass.

### Task 1: Create file-based lock store

**Files:**
- Create: `mcp_task_server/lock_store.py`
- Create: `tests/test_lock_store.py`

- [ ] **Step 1: Write the failing test for lock acquire/release**

```python
# tests/test_lock_store.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_lock_store.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'mcp_task_server.lock_store'`

- [ ] **Step 3: Implement lock_store.py**

```python
# mcp_task_server/lock_store.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_lock_store.py -v`
Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_task_server/lock_store.py tests/test_lock_store.py
git commit -m "feat: add file-based lock store with sentinel locking pattern"
```

---

### Task 2: Wire file-based locks into unified server

**Files:**
- Modify: `mcp_unified_server/server.py:26-27` (remove `_locks` dict), `server.py:36-40` (remove `_expire_locks`), `server.py:244-283` (replace lock tools)

- [ ] **Step 1: Replace in-memory lock tools with file-based lock_store calls**

In `mcp_unified_server/server.py`:

Remove these lines:
```python
_locks: dict[str, dict] = {}
```

```python
def _expire_locks():
    now = time.time()
    for fp in [k for k, v in _locks.items() if now - v["locked_at"] > 300]:
        del _locks[fp]
```

Replace the entire `# ── FILE LOCK ──` section (lines 244-283) with:

```python
# ── FILE LOCK ──────────────────────────────────────────

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
```

- [ ] **Step 2: Verify the import doesn't break the server**

Run: `cd C:\Users\trust\teardown-mp-patches && python -c "from mcp_unified_server import server; print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py
git commit -m "fix: replace in-memory file locks with shared file-based lock_store"
```

---

### Task 3: Fix task store lock fallback

**Files:**
- Modify: `mcp_task_server/task_store.py:27-54`
- Create: `tests/test_task_store_locking.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_task_store_locking.py
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
```

- [ ] **Step 2: Run test to verify `test_lock_exhaustion_raises` fails**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_task_store_locking.py::test_lock_exhaustion_raises -v`
Expected: FAIL — RuntimeError not raised (current code falls back to unlocked write)

- [ ] **Step 3: Fix `_with_lock` in task_store.py**

Replace ONLY lines 27-54 of `mcp_task_server/task_store.py` (the retry loop and fallback). Keep lines 12-26 (function signature, docstring, file existence check, `LOCK_FILE.touch()`) unchanged. The new retry loop:

```python
    max_retries = 20
    delay = 0.1
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
                time.sleep(delay)
                delay = min(delay * 1.5, 1.0)  # exponential backoff, cap 1s
            else:
                raise RuntimeError(
                    f"Could not acquire task store lock after {max_retries} attempts"
                )
```

Also update the docstring (lines 13-18):
```python
    """Execute fn(data) -> result with exclusive file lock.

    Uses a separate lock file so the lock byte count stays constant
    even as tasks.json grows/shrinks during writes.
    Retries up to 20 times with exponential backoff.
    Raises RuntimeError if lock cannot be acquired.
    """
```

- [ ] **Step 4: Run both tests to verify they pass**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_task_store_locking.py -v`
Expected: Both tests PASS

- [ ] **Step 5: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_task_server/task_store.py tests/test_task_store_locking.py
git commit -m "fix: task store raises on lock exhaustion instead of writing unlocked"
```

---

### Task 4: Add `maintainer` to VALID_ROLES

**Files:**
- Modify: `mcp_unified_server/server.py:25`

- [ ] **Step 1: Add maintainer to the set**

In `mcp_unified_server/server.py` line 25, change:
```python
VALID_ROLES = {"api_surgeon", "mod_converter", "qa_lead", "docs_keeper"}
```
to:
```python
VALID_ROLES = {"api_surgeon", "mod_converter", "qa_lead", "docs_keeper", "maintainer"}
```

- [ ] **Step 2: Verify server still imports**

Run: `cd C:\Users\trust\teardown-mp-patches && python -c "from mcp_unified_server import server; print('maintainer' in server.VALID_ROLES)"`
Expected: `True`

- [ ] **Step 3: Run ALL existing tests to verify nothing broke in P0**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/ -q`
Expected: All tests pass (523+ existing + new lock/task tests)

- [ ] **Step 4: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py
git commit -m "fix: add maintainer to VALID_ROLES for 2-terminal mode"
```

> **HUMAN GATE:** After Task 4, the human runs `python -m pytest tests/ -q` and confirms all pass. Phase 0 is complete. Proceed to Phase 1 only after confirmation.

---

## Phase 1: Reliability

### Task 5: Add task deduplication to task_store

**Files:**
- Modify: `mcp_task_server/task_store.py` — add `find_duplicate()`, modify `create_task()`
- Modify: `tests/test_task_store_locking.py` — add dedup tests

> **Note:** This is 1D from the spec. Implemented before 1C so `generate_tasks_from_lint` benefits.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_task_store_locking.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_task_store_locking.py -v -k "duplicate or dedup"`
Expected: FAIL — `find_duplicate` not defined

- [ ] **Step 3: Implement find_duplicate and modify create_task**

Add to `mcp_task_server/task_store.py` after `_recover_stale`:

```python
def _find_duplicate_in_data(data: dict, mods: list[str], title_substring: str) -> str | None:
    """Find an open/in-progress task with overlapping mods and matching title. Called inside _with_lock."""
    search_mods = set(mods)
    sub = title_substring.lower()
    for t in data["tasks"]:
        if t["status"] not in ("open", "in_progress"):
            continue
        if sub not in t.get("title", "").lower():
            continue
        task_mods = set(t.get("mods", []))
        if search_mods & task_mods:  # any overlap
            return t["id"]
    return None


def find_duplicate(mods: list[str], title_substring: str) -> str | None:
    """Find an open/in-progress task with overlapping mods and matching title."""
    def _op(data):
        return _find_duplicate_in_data(data, mods, title_substring)
    return _with_lock(_op)
```

Replace the entire `create_task` function (lines 138-162) with this complete version. **IMPORTANT:** The dedup check is inside `_op` so it shares the same lock — this avoids a TOCTOU race where two terminals both check for duplicates and both create:

```python
def create_task(title: str, role: str, priority: str, description: str,
                mods: list[str] | None = None, deduplicate: bool = False) -> str:
    """Create a new task, return its ID. If deduplicate=True, returns existing task ID if found."""
    def _op(data):
        # Atomic dedup check inside the same lock as creation
        if deduplicate and mods:
            sub = title.split(":")[0] if ":" in title else title
            existing = _find_duplicate_in_data(data, mods, sub)
            if existing:
                return existing  # Return existing task ID, no new task created

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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_task_store_locking.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

- [ ] **Step 6: Update unified server's create_task wrapper**

In `mcp_unified_server/server.py`, modify the `create_task` tool (around line 74) to pass through the `deduplicate` parameter:

```python
@mcp.tool()
def create_task(title: str, role: str, priority: str, description: str,
                mods: list[str] | None = None, deduplicate: bool = False) -> dict:
    """Create a new task. Set deduplicate=True to avoid creating duplicates."""
    tid = task_store.create_task(title, role, priority, description, mods, deduplicate=deduplicate)
    return {"success": True, "task_id": tid}
```

- [ ] **Step 7: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_task_server/task_store.py mcp_unified_server/server.py tests/test_task_store_locking.py
git commit -m "feat: add task deduplication to create_task (atomic check inside lock)"
```

---

### Task 6: Expose existing task_server tools via unified server

**Files:**
- Modify: `mcp_unified_server/server.py` — add imports + wrapper tools

> **Note:** This is 1C from the spec. These tools already exist in `mcp_task_server/server.py` — we only need thin wrappers.
>
> **Import coupling note:** Importing from `mcp_task_server.server` will execute that module, creating a second `FastMCP` instance in memory. This is harmless — the instance is never `run()`. The imported functions use their own module's `COMMS_DIR` and `PROJECT_ROOT`, which resolve to the same paths as the unified server's. Internal calls (e.g., `auto_commit` calling `team_log`) route through the task_server module, which is correct.

- [ ] **Step 1: Add the import block**

After the existing `from mcp_task_server import task_store` line (line 17) in `mcp_unified_server/server.py`, add:

```python
from mcp_task_server.server import (
    heartbeat as _heartbeat,
    get_heartbeats as _get_heartbeats,
    check_terminal_health as _check_health,
    auto_commit as _auto_commit,
    generate_tasks_from_lint as _gen_tasks_lint,
    team_log as _team_log,
)
```

- [ ] **Step 2: Add the wrapper tools**

Add a new section before `if __name__` at the end of the file:

```python
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
    """Auto-commit project state. QA Lead only. Uses git add -u (safe)."""
    return _auto_commit(message)


@mcp.tool()
def generate_tasks_from_lint(role: str = "api_surgeon", priority: str = "medium") -> dict:
    """Generate tasks from lint findings. Groups by mod, skips mods with existing tasks."""
    return _gen_tasks_lint(role, priority)


@mcp.tool()
def team_log(role: str, event: str, detail: str) -> dict:
    """Append structured entry to team.log."""
    return _team_log(role, event, detail)
```

- [ ] **Step 3: Verify the import chain works**

Run: `cd C:\Users\trust\teardown-mp-patches && python -c "from mcp_unified_server import server; print('heartbeat' in dir(server))"`
Expected: `True`

- [ ] **Step 4: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py
git commit -m "feat: expose heartbeat, auto_commit, generate_tasks_from_lint via unified server"
```

---

### Task 7: Add handoff tools

**Files:**
- Modify: `mcp_unified_server/server.py` — add `save_handoff()` and `check_handoff()`

- [ ] **Step 1: Add handoff tools to unified server**

Add to the new `# ── TASK SERVER TOOLS` section:

```python
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
```

- [ ] **Step 2: Verify it works**

Run: `cd C:\Users\trust\teardown-mp-patches && python -c "from mcp_unified_server import server; print('save_handoff' in dir(server))"`
Expected: `True`

- [ ] **Step 3: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py
git commit -m "feat: add save_handoff/check_handoff tools for context overflow recovery"
```

---

### Task 8: Update role files with handoff check

**Files:**
- Modify: `ROLE_QA_LEAD.md`, `ROLE_API_SURGEON.md`, `ROLE_MOD_CONVERTER.md`, `ROLE_DOCS_KEEPER.md`, `ROLE_MAINTAINER.md`

- [ ] **Step 1: Add handoff check to each role's work loop**

In each `ROLE_*.md` file, add as the FIRST step of the work loop (before killswitch check):

```markdown
0. `check_handoff(your_role)` — if a handoff note exists from a previous session, read it and resume that work before entering the normal loop
```

And add to the bottom of each role file under Rules or a new "Context Management" section:

```markdown
### Context Management
- If you've been working for an extended period and notice degraded performance (repeating yourself, forgetting recent context), call `save_handoff(your_role, current_task_id, notes)` describing your current progress and next steps. The watchdog will restart you and you'll pick up from the handoff note.
- Call `report_error(your_role, "context_limit", "approaching context limit")` if you believe you're near the context window boundary.
```

- [ ] **Step 2: Verify the role files are consistent**

Run: `cd C:\Users\trust\teardown-mp-patches && grep -l "check_handoff" ROLE_*.md | wc -l`
Expected: `5` (all 5 role files)

- [ ] **Step 3: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add ROLE_*.md
git commit -m "docs: add handoff check and context management to all role files"
```

---

### Task 9: Create watchdog script

**Files:**
- Create: `watchdog.ps1`

- [ ] **Step 1: Write the watchdog**

```powershell
# watchdog.ps1 — Terminal health monitor for Teardown MP Patcher team
# Started by launch_team.bat. Monitors heartbeats, restarts dead terminals.
#
# Usage: pwsh -File watchdog.ps1 -ConfigFile watchdog_config.json

param(
    [string]$ConfigFile = "watchdog_config.json",
    [int]$CheckIntervalSeconds = 30,
    [int]$StaleMinutes = 5,
    [int]$MaxRestarts = 3
)

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$HeartbeatFile = Join-Path $ProjectRoot ".comms\heartbeats.json"
$StopFile = Join-Path $ProjectRoot ".comms\STOP"
$LogFile = Join-Path $ProjectRoot "logs\watchdog.log"
$PidFile = Join-Path $ProjectRoot "logs\watchdog.pid"
$ConfigPath = Join-Path $ProjectRoot $ConfigFile

# Write PID
$PID | Out-File -FilePath $PidFile -NoNewline

# Track restarts per terminal
$restartCounts = @{}

function Write-Log {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$ts] $Message"
    Add-Content -Path $LogFile -Value $entry
    Write-Host $entry
}

function Get-Config {
    if (-not (Test-Path $ConfigPath)) {
        Write-Log "ERROR: Config file not found: $ConfigPath"
        return $null
    }
    return Get-Content $ConfigPath -Raw | ConvertFrom-Json
}

function Get-Heartbeats {
    if (-not (Test-Path $HeartbeatFile)) { return $null }
    try {
        return Get-Content $HeartbeatFile -Raw | ConvertFrom-Json
    } catch {
        return $null
    }
}

function Restart-Terminal {
    param([string]$Role, [string]$Command, [string]$Title)

    if (-not $restartCounts.ContainsKey($Role)) {
        $restartCounts[$Role] = 0
    }

    if ($restartCounts[$Role] -ge $MaxRestarts) {
        Write-Log "RESTART_LIMIT_REACHED: $Role has been restarted $MaxRestarts times. Skipping."
        return
    }

    Write-Log "RESTARTING: $Role (restart #$($restartCounts[$Role] + 1)/$MaxRestarts)"
    $restartCounts[$Role]++

    try {
        Start-Process -FilePath "C:\Program Files\PowerShell\7\pwsh.exe" `
            -ArgumentList "-NoExit", "-Command", $Command `
            -WindowStyle Normal
        Write-Log "RESTARTED: $Role successfully"
    } catch {
        Write-Log "RESTART_FAILED: $Role — $_"
    }
}

# Main loop
Write-Log "Watchdog started. Check interval: ${CheckIntervalSeconds}s, Stale threshold: ${StaleMinutes}m, Max restarts: $MaxRestarts"

while ($true) {
    Start-Sleep -Seconds $CheckIntervalSeconds

    # Respect killswitch
    if (Test-Path $StopFile) {
        Write-Log "Killswitch active — skipping health check"
        continue
    }

    $config = Get-Config
    if ($null -eq $config) { continue }

    $heartbeats = Get-Heartbeats
    $now = [DateTimeOffset]::UtcNow

    foreach ($terminal in $config.terminals) {
        $role = $terminal.role
        $hb = $null
        if ($null -ne $heartbeats) {
            $hb = $heartbeats.$role
        }

        if ($null -eq $hb -or $null -eq $hb.timestamp) {
            # Never seen — might still be starting up. Skip for first 2 minutes.
            continue
        }

        try {
            $lastSeen = [DateTimeOffset]::Parse($hb.timestamp)
            $elapsed = ($now - $lastSeen).TotalMinutes

            if ($elapsed -gt $StaleMinutes) {
                Write-Log "STALE: $role — last seen ${elapsed:F1}m ago"
                Restart-Terminal -Role $role -Command $terminal.command -Title $terminal.title
            }
        } catch {
            Write-Log "PARSE_ERROR: $role heartbeat timestamp: $_"
        }
    }
}
```

- [ ] **Step 2: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add watchdog.ps1
git commit -m "feat: add PowerShell watchdog for terminal health monitoring and auto-restart"
```

---

### Task 10: Update launch scripts for watchdog + config generation

**Files:**
- Modify: `C:\Users\trust\Desktop\Team\launch_team.bat`
- Modify: `C:\Users\trust\Desktop\Team\launch_team_maintenance.bat`

- [ ] **Step 1: Add watchdog config generation and launch to `launch_team.bat`**

After the `:: ── Create log directory ──` section and BEFORE `:: ── Start Dashboard ──`, insert:

```batch
:: ── Generate watchdog config ───────────────────
echo [PRE] Generating watchdog config...
python -c "import json; roles=[('qa_lead','QA Lead','ROLE_QA_LEAD.md'),('api_surgeon','API Surgeon','ROLE_API_SURGEON.md'),('mod_converter','Mod Converter','ROLE_MOD_CONVERTER.md'),('docs_keeper','Docs Keeper','ROLE_DOCS_KEEPER.md')]; config={'terminals':[{'role':r,'title':t,'command':'cd %PROJECT%; claude --dangerously-skip-permissions \"Read '+f+' and start your autonomous work loop. You are '+r+'. Run tools.status first, then read docs/OFFICIAL_DEVELOPER_DOCS.md. Then get_focus, check_inbox, and get_task. Keep working forever.\"'} for r,t,f in roles]}; open('%PROJECT%/watchdog_config.json','w').write(json.dumps(config,indent=2))"
echo   [OK] watchdog_config.json

:: ── Start Watchdog ─────────────────────────────
echo [0/4] Starting Watchdog...
start "Watchdog" "%PWSH%" -WindowStyle Minimized -File "%PROJECT%\watchdog.ps1"
echo [%DATE% %TIME%] Watchdog started >> "%LOGFILE%"
```

Do the same for `launch_team_maintenance.bat` but with only `qa_lead` and `maintainer` terminals in the config.

- [ ] **Step 2: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add "C:\Users\trust\Desktop\Team\launch_team.bat" "C:\Users\trust\Desktop\Team\launch_team_maintenance.bat"
git commit -m "feat: launch scripts generate watchdog config and start watchdog process"
```

---

### Task 10.5: Write tests for unified server wrappers and new tools

**Files:**
- Create: `tests/test_unified_server.py`

> **Note:** The file map listed this but no task created it. Covers: handoff save/load, message archival with critical exemption, heartbeat wrapper.

- [ ] **Step 1: Write the tests**

```python
# tests/test_unified_server.py
"""Tests for unified server tools that don't go through MCP transport."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta


def test_handoff_save_and_load(tmp_path):
    """save_handoff writes file, check_handoff reads and deletes it."""
    from mcp_unified_server import server
    old_comms = server.COMMS_DIR
    server.COMMS_DIR = tmp_path
    try:
        (tmp_path / "qa_lead" / "inbox").mkdir(parents=True)
        result = server.save_handoff("qa_lead", "T42", "Working on AWP lint fixes")
        assert result["success"] is True
        assert (tmp_path / "qa_lead" / "handoff.md").exists()

        loaded = server.check_handoff("qa_lead")
        assert loaded["found"] is True
        assert "T42" in loaded["content"]
        assert not (tmp_path / "qa_lead" / "handoff.md").exists()  # deleted after read
    finally:
        server.COMMS_DIR = old_comms


def test_check_handoff_no_file(tmp_path):
    """check_handoff returns string when no handoff exists."""
    from mcp_unified_server import server
    old_comms = server.COMMS_DIR
    server.COMMS_DIR = tmp_path
    try:
        (tmp_path / "qa_lead" / "inbox").mkdir(parents=True)
        result = server.check_handoff("qa_lead")
        assert isinstance(result, str)
        assert "no handoff" in result.lower()
    finally:
        server.COMMS_DIR = old_comms


def test_message_archival_preserves_critical(tmp_path):
    """check_inbox auto-archives old messages but keeps critical ones."""
    from mcp_unified_server import server
    old_comms = server.COMMS_DIR
    server.COMMS_DIR = tmp_path
    try:
        inbox = tmp_path / "qa_lead" / "inbox"
        inbox.mkdir(parents=True)
        # Old non-critical message (2 hours old timestamp in filename)
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=2)).strftime("%Y%m%d_%H%M%S")
        (inbox / f"{old_ts}_api_surgeon_info.md").write_text(
            "---\npriority: low\n---\nOld message", encoding="utf-8"
        )
        # Old critical message (same age)
        (inbox / f"{old_ts}_qa_lead_stop.md").write_text(
            "---\npriority: critical\n---\nSTOP ORDER", encoding="utf-8"
        )
        # Recent message
        now_ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        (inbox / f"{now_ts}_mod_converter_info.md").write_text(
            "---\npriority: low\n---\nRecent message", encoding="utf-8"
        )

        msgs = server.check_inbox("qa_lead")
        # Should return 2: the critical (preserved despite age) + the recent one
        assert isinstance(msgs, list)
        assert len(msgs) == 2
        # Old non-critical should be archived
        archive = tmp_path / "qa_lead" / "archive"
        assert archive.exists()
        assert len(list(archive.glob("*.md"))) == 1
    finally:
        server.COMMS_DIR = old_comms
```

- [ ] **Step 2: Run tests**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_unified_server.py -v`
Expected: All 3 tests PASS

- [ ] **Step 3: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add tests/test_unified_server.py
git commit -m "test: add tests for unified server handoff and message TTL tools"
```

> **TEAM GATE:** Launch the team. QA Lead's first verification task: confirm `heartbeats.json` is populated, `logs/watchdog.log` exists and shows startup. Then the human kills one terminal process — within 60s the watchdog should detect and restart it (check `logs/watchdog.log`).

---

## Phase 2: Workflow Improvements

### Task 11: Add pre-launch validation to launch scripts

**Files:**
- Modify: `C:\Users\trust\Desktop\Team\launch_team.bat`
- Modify: `C:\Users\trust\Desktop\Team\launch_team_maintenance.bat`

- [ ] **Step 1: Add validation block after prerequisite checks**

After the `echo   [OK] Python` line in both launch scripts, add:

```batch
:: ── Validate project state ─────────────────────
echo [PRE] Validating project state...
python -c "import json; json.load(open('%PROJECT%/mcp_task_server/tasks.json'))" 2>nul
if errorlevel 1 echo   [WARN] tasks.json invalid or missing — task queue empty
curl -s -o nul http://localhost:8420 2>nul
if not errorlevel 1 echo   [WARN] Port 8420 already in use
if not exist "C:\Users\trust\Documents\Teardown\mods" (
    echo [FAIL] Mods directory not found
    pause
    exit /b 1
)
python -c "import mcp_unified_server.server" 2>nul
if errorlevel 1 (
    echo [FAIL] MCP server has import errors
    pause
    exit /b 1
)
echo   [OK] Project state
```

- [ ] **Step 2: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add "C:\Users\trust\Desktop\Team\launch_team.bat" "C:\Users\trust\Desktop\Team\launch_team_maintenance.bat"
git commit -m "feat: add pre-launch validation for tasks.json, port, mods dir, MCP imports"
```

---

### Task 12: Create metrics module

**Files:**
- Create: `mcp_task_server/metrics.py`
- Create: `tests/test_metrics.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_metrics.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_metrics.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement metrics.py**

```python
# mcp_task_server/metrics.py
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
```

- [ ] **Step 4: Run tests**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/test_metrics.py -v`
Expected: PASS

- [ ] **Step 5: Expose via unified server**

Add to `mcp_unified_server/server.py`:

```python
from mcp_task_server import metrics as _metrics

@mcp.tool()
def get_metrics() -> dict:
    """Get team performance metrics (throughput, avg task time, by role)."""
    return _metrics.compute()
```

- [ ] **Step 6: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_task_server/metrics.py tests/test_metrics.py mcp_unified_server/server.py
git commit -m "feat: add metrics module with throughput and per-role task timing"
```

---

### Task 13: Add interactive dashboard POST endpoints

**Files:**
- Modify: `dashboard/server.py` — add `do_POST` handler
- Modify: `dashboard/index.html` — add interactive controls

- [ ] **Step 1: Add POST handler to dashboard/server.py**

Add this method to the `DashboardHandler` class after `do_GET`:

```python
    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}

        if parsed.path == "/api/task":
            try:
                from mcp_task_server import task_store
                tid = task_store.create_task(
                    body["title"], body["role"], body.get("priority", "medium"),
                    body.get("description", ""), body.get("mods", []),
                )
                self._json_response(200, {"success": True, "task_id": tid})
            except Exception as e:
                self._json_response(400, {"error": str(e)})

        elif parsed.path == "/api/killswitch":
            if not body.get("confirm"):
                self._json_response(400, {"error": "Must include confirm: true"})
                return
            stop_file = COMMS / "STOP"
            if body.get("action") == "activate":
                stop_file.write_text("STOP", encoding="utf-8")
                self._json_response(200, {"success": True, "active": True})
            elif body.get("action") == "deactivate":
                if stop_file.exists():
                    stop_file.unlink()
                self._json_response(200, {"success": True, "active": False})
            else:
                self._json_response(400, {"error": "action must be activate or deactivate"})

        elif parsed.path == "/api/focus":
            focus_file = COMMS / "FOCUS.md"
            focus_file.write_text(body.get("content", ""), encoding="utf-8")
            self._json_response(200, {"success": True})

        elif parsed.path == "/api/message":
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            to_role = body.get("to", "")
            msg_type = body.get("type", "info")
            priority = body.get("priority", "medium")
            content = body.get("content", "")
            fn = f"{ts}_user_{msg_type}.md"
            full = f"---\nfrom: user\nto: {to_role}\ntype: {msg_type}\npriority: {priority}\n---\n\n{content}"
            inbox = COMMS / to_role / "inbox"
            inbox.mkdir(parents=True, exist_ok=True)
            (inbox / fn).write_text(full, encoding="utf-8")
            self._json_response(200, {"success": True, "filename": fn})

        else:
            self._json_response(404, {"error": "not found"})

    def _json_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
```

- [ ] **Step 2: Add metrics to the GET /api/status response**

In `build_api_response()`, add:

```python
from mcp_task_server import metrics
# ... inside the function:
"metrics": metrics.compute(),
```

- [ ] **Step 3: Update index.html with interactive controls**

Add to `dashboard/index.html` — a "Create Task" form, killswitch button with confirmation, editable focus field, and per-terminal message forms. This is a large HTML change — the implementer should add:
- A collapsible "Actions" panel with forms for each POST endpoint
- The killswitch button should be red with a `confirm()` dialog
- Forms should use `fetch()` to POST to the API and show success/failure
- A "Metrics" section displaying throughput and per-role stats from the API response

- [ ] **Step 4: Test manually** — start dashboard with `python dashboard/server.py`, verify POST endpoints work via curl:

```bash
curl -X POST http://localhost:8420/api/task -H "Content-Type: application/json" -d '{"title":"Test task","role":"qa_lead","priority":"low","description":"test"}'
```

- [ ] **Step 5: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add dashboard/server.py dashboard/index.html
git commit -m "feat: add interactive dashboard with POST endpoints for tasks, killswitch, focus, messages"
```

---

### Task 14: Add message TTL / stale cleanup

**Files:**
- Modify: `mcp_unified_server/server.py` — modify `check_inbox()`, add `archive_stale_messages()`

- [ ] **Step 1: Modify check_inbox to filter stale messages**

Replace the `check_inbox` function in `mcp_unified_server/server.py`:

```python
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
```

- [ ] **Step 2: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py
git commit -m "feat: add message TTL — auto-archive stale inbox messages (60min, critical exempt)"
```

> **TEAM GATE:** Launch the team. QA Lead verifies: dashboard POST endpoints work, metrics appear, old messages are archived. Run all tests: `python -m pytest tests/ -q`.

---

## Phase 3: Polish & Process

### Task 15: Add dynamic role loading

**Files:**
- Modify: `mcp_unified_server/server.py` — replace hardcoded `VALID_ROLES`

- [ ] **Step 1: Replace VALID_ROLES with dynamic loading**

In `mcp_unified_server/server.py`, replace:
```python
VALID_ROLES = {"api_surgeon", "mod_converter", "qa_lead", "docs_keeper", "maintainer"}
```

with:

```python
def _load_roles() -> set[str]:
    """Discover roles from ROLE_*.md files and .comms/ inbox directories."""
    roles = set()
    for f in PROJECT_ROOT.glob("ROLE_*.md"):
        roles.add(f.stem.replace("ROLE_", "").lower())
    for d in COMMS_DIR.iterdir():
        if d.is_dir() and (d / "inbox").is_dir() and d.name != "__pycache__":
            roles.add(d.name)
    return roles


VALID_ROLES = _load_roles()


def _write_roles_json():
    """Write roles.json for other systems to read."""
    data = {"roles": sorted(VALID_ROLES), "last_scanned": datetime.now(timezone.utc).isoformat()}
    (PROJECT_ROOT / "roles.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
```

Add the refresh tool:
```python
@mcp.tool()
def refresh_roles() -> dict:
    """Re-scan for roles and update roles.json."""
    global VALID_ROLES
    VALID_ROLES = _load_roles()
    _write_roles_json()
    return {"roles": sorted(VALID_ROLES)}
```

Add `import json` to the imports if not already present.

Call `_write_roles_json()` at the bottom of the file (before `if __name__`) so it generates on startup.

- [ ] **Step 2: Update spawn_terminal to write roles.json**

The existing `spawn_terminal` in the unified server (line ~227) does `VALID_ROLES.add(role_name)` which is in-memory only. After it, add a call to persist the new role:

```python
# Inside spawn_terminal, after VALID_ROLES.add(role_name):
_write_roles_json()
```

- [ ] **Step 3: Update dashboard to read roles.json as fast-path**

In `dashboard/server.py`, modify `get_inboxes()` to try `roles.json` first:

```python
def get_inboxes():
    """Get inbox/outbox counts for each role."""
    # Try roles.json first (fast-path), fall back to directory scan
    roles_file = PROJECT / "roles.json"
    if roles_file.exists():
        try:
            roles = json.loads(roles_file.read_text(encoding="utf-8")).get("roles", [])
        except (json.JSONDecodeError, OSError):
            roles = ["qa_lead", "api_surgeon", "mod_converter", "docs_keeper"]
    else:
        roles = ["qa_lead", "api_surgeon", "mod_converter", "docs_keeper"]
    # Also scan for any additional roles in .comms/
    if COMMS.exists():
        for d in COMMS.iterdir():
            if d.is_dir() and (d / "inbox").is_dir() and d.name not in roles and d.name != "__pycache__":
                roles.append(d.name)
    # ... rest of function unchanged
```

- [ ] **Step 4: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py dashboard/server.py
git commit -m "feat: dynamic role loading, roles.json persistence, dashboard reads roles.json"
```

---

### Task 16: Add session retrospective tool

**Files:**
- Modify: `mcp_unified_server/server.py` — add `save_retro()`
- Modify: `ROLE_QA_LEAD.md` — add retro to killswitch flow

- [ ] **Step 1: Add save_retro tool**

```python
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
```

- [ ] **Step 2: Update QA Lead role — add retro to killswitch flow**

In `ROLE_QA_LEAD.md`, in the Killswitch section, add before step 1:

```markdown
0. Call `save_retro(what_worked, what_stalled, improvements, role_changes)` — capture session learnings before halting
```

- [ ] **Step 3: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py ROLE_QA_LEAD.md
git commit -m "feat: add save_retro tool and wire into QA Lead killswitch flow"
```

---

### Task 17: Add backup strategy

**Files:**
- Modify: `mcp_unified_server/server.py` — add `backup_state()`

- [ ] **Step 1: Add backup_state tool**

```python
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

    # Keep only last 3 backups
    backups_root = PROJECT_ROOT / "backups"
    all_backups = sorted(backups_root.iterdir(), reverse=True)
    for old in all_backups[3:]:
        if old.is_dir():
            shutil.rmtree(old)

    return {"success": True, "path": str(backup_dir), "files": backed_up}
```

- [ ] **Step 2: Wire into auto_commit**

The existing `auto_commit` in `mcp_task_server/server.py` should call backup first. But since we're wrapping it, add the backup call in the unified server's wrapper instead:

```python
@mcp.tool()
def auto_commit(message: str | None = None) -> dict:
    """Auto-commit project state. Backs up state files first. QA Lead only."""
    backup_state("pre-commit")
    return _auto_commit(message)
```

- [ ] **Step 3: Add `backups/` to .gitignore**

Append to `.gitignore`:
```
backups/
```

- [ ] **Step 4: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py .gitignore
git commit -m "feat: add backup_state tool with auto-backup before commits, 3-backup rotation"
```

---

### Task 18: Add error reporting pipeline

**Files:**
- Modify: `mcp_unified_server/server.py` — add `report_error()`
- Modify: `dashboard/server.py` — add error data to API
- Modify: `dashboard/index.html` — add error indicator
- Modify: All `ROLE_*.md` — add error reporting guidance

- [ ] **Step 1: Add report_error tool**

```python
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
```

- [ ] **Step 2: Add errors to dashboard API response**

In `dashboard/server.py`, add a `get_errors()` function:

```python
def get_errors():
    errors_file = PROJECT / "logs" / "errors.json"
    if not errors_file.exists():
        return {"total": 0, "recent": []}
    try:
        errors = json.loads(errors_file.read_text(encoding="utf-8"))
        now = datetime.now(timezone.utc)
        one_hour_ago = (now - timedelta(hours=1)).isoformat()
        recent = [e for e in errors if e.get("timestamp", "") >= one_hour_ago]
        return {"total": len(recent), "recent": recent[-5:]}
    except (json.JSONDecodeError, OSError):
        return {"total": 0, "recent": []}
```

Add `from datetime import timedelta` to imports. Add `"errors": get_errors()` to `build_api_response()`.

- [ ] **Step 3: Add error indicator to dashboard index.html**

Add a red badge in the header that shows error count from the last hour. Expandable to show details.

- [ ] **Step 4: Add error reporting guidance to all role files**

Append to each `ROLE_*.md` under the Context Management section:

```markdown
- When you encounter an error you cannot resolve (lock failures, MCP errors, tool crashes), call `report_error(your_role, "error_type", "details")` before retrying or halting. This makes errors visible on the dashboard.
```

- [ ] **Step 5: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add mcp_unified_server/server.py dashboard/server.py dashboard/index.html ROLE_*.md
git commit -m "feat: add error reporting pipeline with dashboard indicator"
```

---

### Task 19: Delete duplicate launch script

**Files:**
- Delete: `C:\Users\trust\teardown-mp-patches\launch_team.bat`

- [ ] **Step 1: Verify nothing references it**

Run: `cd C:\Users\trust\teardown-mp-patches && grep -r "launch_team.bat" --include="*.md" --include="*.py" --include="*.bat" --include="*.json" .`

Check the output — if only the Desktop copy references itself, safe to delete.

- [ ] **Step 2: Delete the project root copy**

```bash
rm C:\Users\trust\teardown-mp-patches\launch_team.bat
```

- [ ] **Step 3: Commit**

```bash
cd C:\Users\trust\teardown-mp-patches
git add -u
git commit -m "chore: remove duplicate launch_team.bat from project root (canonical copy is Desktop/Team/)"
```

---

### Task 20: Final full test run

- [ ] **Step 1: Run all pytest tests**

Run: `cd C:\Users\trust\teardown-mp-patches && python -m pytest tests/ -q`
Expected: All tests pass

- [ ] **Step 2: Verify unified server imports cleanly**

Run: `cd C:\Users\trust\teardown-mp-patches && python -c "from mcp_unified_server import server; tools = [x for x in dir(server) if not x.startswith('_')]; print(f'{len(tools)} tools/functions exposed'); print(sorted(tools))"`

- [ ] **Step 3: Launch team for final verification**

Team runs a full session. QA Lead tests all new tools: heartbeat, auto_commit, generate_tasks_from_lint, save_handoff, check_handoff, get_metrics, report_error, save_retro, backup_state, refresh_roles. Docs Keeper verifies roles.json and retro file. At session end, QA Lead saves retro.

- [ ] **Step 4: Final commit (if any uncommitted changes remain)**

```bash
cd C:\Users\trust\teardown-mp-patches
git add -u
git commit -m "chore: team infrastructure improvements complete — all 4 phases implemented"
```

Note: Use `git add -u` (tracked files only), not `git add -A`, to avoid staging secrets or untracked binaries.
