# Team Infrastructure Improvements — Design Spec

**Date:** 2026-03-19
**Revision:** 2 (post spec-review)
**Scope:** 17 improvements across 4 phases to the Teardown MP Patcher multi-agent team system
**Delivery:** Phased rollout (P0 → P1 → P2 → P3), team validates each phase before next begins

---

## Context

The Teardown MP Patcher uses a 4-terminal autonomous Claude Code team (QA Lead, API Surgeon, Mod Converter, Docs Keeper) with a 2-terminal maintenance mode variant. Terminals coordinate via a unified MCP server, file-based inbox/outbox messaging, a web dashboard, and a Python tooling suite.

The project reached feature-complete status: 177 mods converted, 0 lint findings, 523 tests. During analysis of the team infrastructure, 17 issues were identified ranging from critical bugs (broken cross-terminal file locks) to process improvements (session retrospectives).

### Two-Server Architecture (Important Context)

The project has two MCP server codebases:
- **`mcp_unified_server/server.py`** — the ACTIVE server (per `.mcp.json`). All terminals connect to this. Contains: task CRUD, inbox/outbox, file locks, change tracker, template engine, mod registry.
- **`mcp_task_server/server.py`** — an OLDER, MORE COMPLETE server that is NOT connected. Contains tools that were never wired into the unified server: `heartbeat()`, `auto_commit()`, `generate_tasks_from_lint()`, `check_terminal_health()`, `team_log()`, `spawn_terminal()` (more complete version).

**Strategy for this spec:** Import and expose existing `mcp_task_server` implementations through the unified server (same pattern already used for `task_store`). Do NOT rewrite tools that already exist.

### Key Constraint

The autonomous team validates Phases 1-3. **Phase 0 is validated by the human running pytest directly**, because P0 modifies the lock system that the team's own task tools depend on — self-referential validation is unreliable.

---

## Phase 0: Critical Bug Fixes

### 0A. File Locks → Shared File-Based Locks

**Problem:** `_locks` in `mcp_unified_server/server.py:27` is an in-memory dict. Each terminal spawns its own MCP server process (stdio transport), so locks are never shared. The file lock system prevents self-conflicts only — cross-terminal conflicts are undetected.

**Fix:** Replace the in-memory dict with file-based storage. Use a separate sentinel file `locks.lock` (following the same pattern as `task_store.py` which uses `tasks.lock`) — do NOT lock `locks.json` directly, as its size changes on write and `msvcrt.locking` is byte-count-sensitive.

**File layout:**
- `mcp_task_server/locks.json` — data file (lock state)
- `mcp_task_server/locks.lock` — sentinel file (1 byte, locked during reads/writes)

**Data format:**
```json
{
  "locks": {
    "c:/users/trust/documents/teardown/mods/awp/main.lua": {
      "role": "api_surgeon",
      "locked_at": "2026-03-19T15:46:35+00:00"
    }
  }
}
```

**Lock expiry:** 5 minutes (unchanged). Expired locks cleaned on every read.

**Modified files:**
- `mcp_unified_server/server.py` — rewrite `lock_file`, `unlock_file`, `list_locks`, `force_unlock` to use file-based storage with sentinel lock pattern
- Remove `_locks` dict and `_expire_locks()` function

### 0B. Lock Fallback → Fail Safely

**Problem:** `task_store.py:46-53` falls back to unlocked read/write after 10 failed lock attempts. Two terminals hitting this simultaneously corrupt `tasks.json`. The bare `except:` at line 52 swallows all errors.

**Fix:**
- Increase retry count from 10 to 20 (4 seconds total instead of 2)
- Add exponential backoff: 100ms, 150ms, 225ms, ... instead of fixed 200ms
- After exhausting retries: raise `RuntimeError("Could not acquire task store lock after 20 attempts")` instead of writing unlocked
- Remove the bare `except:` block
- MCP tool wrappers in the unified server catch the exception and return `{"error": "Task store busy, try again"}` to the terminal — terminals retry on next loop iteration rather than crashing

### 0C. Add `maintainer` to VALID_ROLES

**Problem:** `mcp_unified_server/server.py:26` hardcodes 4 roles but omits `maintainer`, used in 2-terminal mode.

**Fix:** Add `"maintainer"` to the `VALID_ROLES` set. This is a stopgap — Phase 3B replaces the hardcoded set with dynamic role loading. Dashboard dynamic scanning is deferred to 3B to avoid doing the same work twice.

### Phase 0 Verification

**Human-run (not team-run) because P0 modifies the tools the team depends on:**
1. New pytest tests: file-based lock acquire/release, mutual exclusion simulation, lock expiry
2. New pytest test: task store raises `RuntimeError` on lock exhaustion (no silent fallback)
3. New pytest test: `maintainer` role accepted by unified server tools
4. Human runs `python -m pytest tests/ -q` and confirms all pass before launching the team

---

## Phase 1: Reliability

### 1A. Terminal Watchdog + Auto-Restart

**Problem:** Crashed terminals (context overflow, MCP error, Python exception) are undetected. No mechanism to restart them.

**Existing code:** `mcp_task_server/server.py` already has `heartbeat()` (lines 400-419) and `check_terminal_health()` (lines 488-553) with full heartbeat JSON file read/write, stale detection, and orphaned task identification. These just aren't exposed through the unified server.

**Changes:**

1. **Expose existing tools via unified server:** Import `heartbeat`, `get_heartbeats`, `check_terminal_health` from `mcp_task_server/server.py` and register them as `@mcp.tool()` wrappers in `mcp_unified_server/server.py`.

2. **New file: `watchdog.ps1`** (project root)
   - Runs as a background PowerShell job, started by `launch_team.bat` before terminal launch
   - Every 30 seconds: reads `.comms/heartbeats.json`, checks each terminal's last heartbeat
   - If any terminal's heartbeat is >5 minutes stale: logs to `logs/watchdog.log`, relaunches that terminal
   - **Restart command mapping:** Reads a `watchdog_config.json` file that maps role → launch command (generated by `launch_team.bat` at startup). This avoids parsing the .bat file.
   - **Restart limit:** Max 3 restarts per terminal per session. After 3 restarts, logs `RESTART_LIMIT_REACHED` and stops retrying that terminal (prevents restart loops from persistent errors).
   - **Restarted terminals:** Start fresh — they read their role file, run `tools.status`, check for handoff notes (1B), then enter normal work loop. In-progress tasks are auto-recovered by the existing stale task recovery in `task_store.py`.
   - Respects killswitch: if `.comms/STOP` exists, does not restart anything
   - Writes its own PID to `logs/watchdog.pid` for management
   - **No watchdog-of-the-watchdog:** If the watchdog dies, the dashboard still shows stale heartbeats. The user can restart it manually. Over-engineering this adds complexity without proportional value.

**Modified files:**
- `mcp_unified_server/server.py` — add wrapper tools for heartbeat/health
- `launch_team.bat` — generate `watchdog_config.json`, start watchdog before terminals
- `launch_team_maintenance.bat` — same

### 1B. Context Overflow Graceful Handoff

**Problem:** Long-running terminals hit context limits, lose accumulated state, become disoriented. No handoff mechanism.

**Honest limitation:** Claude Code terminals cannot reliably detect their own context usage. This feature is **best-effort** — the tools exist for terminals to use voluntarily, and the watchdog (1A) provides the safety net when they don't.

**New MCP tools (in unified server):**
- `save_handoff(role, current_task_id, notes)` — writes `.comms/{role}/handoff.md`
- `check_handoff(role)` — reads and deletes handoff.md if it exists, returns contents or null

**Handoff file format:**
```markdown
---
task_id: T42
saved_at: 2026-03-19T16:00:00+00:00
---

Working on: Lint fixes for AWP mod
Progress: Fixed 3 of 5 findings
Next steps: Apply PER_TICK_RPC_FIX_GUIDE pattern #2, then add ammo display
```

**Startup behavior change:** Each role's work loop gets a new step 0: `check_handoff(your_role)`. If found, read notes and resume from where it left off before entering normal inbox/task loop.

**Modified files:**
- `mcp_unified_server/server.py` — add `save_handoff()` and `check_handoff()` tools
- All `ROLE_*.md` files — add handoff check to work loop, add note: "If you've been working for a very long time, consider calling `save_handoff()` to preserve state"

### 1C. Expose Existing MCP Tools

**Problem:** QA Lead role references `auto_commit()` and `generate_tasks_from_lint()` — these already exist in `mcp_task_server/server.py` but aren't exposed through the unified server that terminals connect to.

**Existing implementations (no rewrite needed):**
- `auto_commit(message)` — `mcp_task_server/server.py:562-611`. Uses `git add -u` (tracked files only) + selective `git add` for safe directories (`docs/`, `tests/`, `.comms/`). Safer than `git add -A`. Returns commit hash.
- `generate_tasks_from_lint(role, priority)` — `mcp_task_server/server.py:330-390`. Already has deduplication (checks existing open tasks). Groups by mod, references PER_TICK_RPC_FIX_GUIDE for relevant findings.
- `team_log(role, event, detail)` — `mcp_task_server/server.py:621-632`. Structured append to `team.log`.

**Fix:** Import these from `mcp_task_server.server` and register as `@mcp.tool()` wrappers in the unified server. Same delegation pattern already used for `task_store`, change tracker, template engine, and registry.

**Note on ordering:** 1D (task deduplication) should be implemented BEFORE 1C, so `generate_tasks_from_lint` benefits from the improved deduplication in `create_task()`.

**Modified file:** `mcp_unified_server/server.py`

### 1D. Task Deduplication

**Problem:** Multiple terminals detecting the same lint finding can create duplicate tasks. The existing `generate_tasks_from_lint` has basic deduplication (checks mod names), but `create_task()` itself does not.

**Implementation order:** 1D before 1C, so the improved `create_task()` is available when `generate_tasks_from_lint` is wired in.

**New function in `task_store.py`:** `find_duplicate(mods, title_substring)`
- Searches open/in-progress tasks
- If any task has overlapping mods AND title contains the substring, returns that task's ID
- Otherwise returns None

**Modified `create_task()`:** New parameter `deduplicate: bool = True`. When true, calls `find_duplicate()` first. If duplicate found, returns existing task ID with a `"duplicate": True` flag instead of creating a new task.

### Phase 1 Verification

- Pytest tests for: heartbeat wrapper, handoff save/load, auto_commit wrapper (mocked git), deduplication logic
- Team runs a session with a specific **watchdog kill test:** QA Lead's first task is to verify heartbeats.json is populated. Then the human manually kills one terminal process. Within 60 seconds, the watchdog should detect the stale heartbeat, log a restart, and relaunch the terminal. QA Lead verifies this by checking `logs/watchdog.log`.
- Team also verifies `auto_commit` and `generate_tasks_from_lint` work by running them

---

## Phase 2: Workflow Improvements

### 2A. Interactive Dashboard

**Problem:** Dashboard is read-only. All actions require CLI.

**New POST endpoints in `dashboard/server.py`:**
- `POST /api/task` — create task (imports `task_store.create_task`)
- `POST /api/killswitch` — body `{"action": "activate"|"deactivate"}` (imports killswitch logic)
- `POST /api/focus` — body `{"content": "..."}` (writes to `.comms/FOCUS.md`)
- `POST /api/message` — body `{"from": "user", "to": "role", "type": "...", "priority": "...", "content": "..."}` (writes to inbox)

**Security note:** This is a localhost-only development tool. No auth is added, but the killswitch endpoint requires a confirmation field (`"confirm": true`) in the POST body to prevent accidental triggers. This is adequate for a single-user local tool.

**Dashboard UI additions in `index.html`:**
- "Create Task" collapsible form panel
- Red killswitch toggle button with confirmation dialog ("Are you sure? This stops all terminals.")
- Editable focus area textarea with "Save" button
- "Send Message" dropdown per terminal

### 2B. Metrics & Analytics

**New file:** `mcp_task_server/metrics.py`

**Computed from existing data** (no new event recording needed):
- Task throughput: completed tasks per hour (from `tasks.json` timestamps)
- Avg time-per-task by role (from started_at → completed_at)
- Terminal uptime: percentage of time with fresh heartbeats (from `heartbeats.json`)
- Lint trend: current count vs last recorded count

**New MCP tool (exposed via unified server):** `get_metrics()` — returns the above as a dict.

**Dashboard:** New "Metrics" section with text stats. No charting library.

### 2C. Message TTL / Stale Cleanup

**Problem:** Stale messages from crashed terminals get reprocessed on restart, causing duplicate work.

**Modified `check_inbox()` in unified server:**
- Parse message age from the filename timestamp (format: `YYYYMMDD_HHMMSS_*`). Filename is authoritative because it's set at write time and doesn't change.
- Messages older than 60 minutes are moved to `.comms/{role}/archive/` instead of returned
- **Exception:** Messages with `priority: critical` are never auto-archived (killswitch, stop orders should persist)
- Archive directory created automatically

**New MCP tool:** `archive_stale_messages(max_age_minutes=60)` — manual trigger for QA Lead to force-archive or adjust threshold.

### 2D. Pre-Launch Validation

**Modified files:** `launch_team.bat`, `launch_team_maintenance.bat`

**New validation block after existing prerequisite checks:**
```batch
:: Validate project state
echo [PRE] Validating project state...
python -c "import json; json.load(open('mcp_task_server/tasks.json'))" 2>nul
if errorlevel 1 echo   [WARN] tasks.json is invalid or missing — task queue will be empty
curl -s -o nul http://localhost:8420 2>nul && echo   [WARN] Port 8420 already in use — dashboard may conflict
if not exist "C:\Users\trust\Documents\Teardown\mods" (
    echo   [FAIL] Mods directory missing
    pause
    exit /b 1
)
echo   [OK] Project state
```

Only mods directory missing is fatal. Others are warnings.

### Phase 2 Verification

- Team runs a full launch cycle
- QA Lead: creates a task from dashboard, sends a message to maintainer, checks metrics endpoint
- Docs Keeper: verifies old test messages got archived (not critical-priority ones)
- Pytest covers new POST endpoints, metrics computation, and message TTL logic

---

## Phase 3: Polish & Process

### 3A. Session Retrospective Template

**New MCP tool (unified server):** `save_retro(what_worked, what_stalled, improvements, role_changes)`
- Writes to `docs/retros/YYYY-MM-DD-retro.md` with structured sections
- Creates `docs/retros/` if missing

**Modified:** QA Lead role file — add to killswitch flow: "Before calling `killswitch()`, call `save_retro()`"

### 3B. Dynamic Role Loading

**Replace hardcoded `VALID_ROLES`** in unified server with:
```python
def _load_roles():
    roles = set()
    for f in PROJECT_ROOT.glob("ROLE_*.md"):
        roles.add(f.stem.replace("ROLE_", "").lower())
    for d in COMMS_DIR.iterdir():
        if d.is_dir() and (d / "inbox").is_dir():
            roles.add(d.name)
    return roles

VALID_ROLES = _load_roles()
```

**New MCP tool:** `refresh_roles()` — re-scans, updates `VALID_ROLES`, and writes `roles.json` to project root. Also called by `spawn_terminal()` after creating a new role, so other terminals pick it up on their next `refresh_roles()` call.

**`spawn_terminal()` fix:** The existing implementation in `mcp_task_server/server.py:644` does `ROLES_MAP[role_name] = role_name` (in-memory only, invisible to other terminals). After wiring this into the unified server, add a `_load_roles()` refresh + `roles.json` write so newly spawned roles are visible across terminals.

### 3C. Backup Strategy

**New MCP tool (unified server):** `backup_state(label)`
- Copies `tasks.json`, `changes.json`, `heartbeats.json`, `locks.json` to `backups/{timestamp}_{label}/`
- Keeps last 3 backups, deletes older ones
- Returns list of files backed up

**Integration:** `auto_commit()` calls `backup_state()` automatically before committing.

### 3D. Deduplicate Launch Scripts

- Delete `C:\Users\trust\teardown-mp-patches\launch_team.bat` (the project root copy — a simpler 3-terminal launcher from an earlier era)
- Canonical launchers: `C:\Users\trust\Desktop\Team\` only
- Verify no scripts or documentation reference the deleted file before removing

### 3E. Error Reporting Pipeline

**New MCP tool (unified server):** `report_error(role, error_type, details, task_id=None)`
- Appends to `logs/errors.json` (array of error objects with timestamps)
- Keeps last 100 errors, rotates older ones

**Dashboard:** Red error indicator in header showing count of errors in last hour. Expandable to show details.

**Role file addition (all roles):** "When you encounter an error you cannot resolve (including lock failures, MCP errors, or tool crashes), call `report_error()` before retrying or halting."

### 3F. Centralized `roles.json`

Generated by `refresh_roles()` (3B). Written to project root.
```json
{
  "roles": ["qa_lead", "api_surgeon", "mod_converter", "docs_keeper", "maintainer"],
  "last_scanned": "2026-03-19T16:00:00+00:00"
}
```

Dashboard reads from this file as a fast-path before falling back to directory scanning.

### Phase 3 Verification

- Team runs a full session
- QA Lead: tests retrospective generation, verifies backup created after auto-commit, tests error reporting, confirms `roles.json` is accurate
- At session end: QA Lead saves retro, confirms the file was written correctly

---

## Files Changed Summary

| Phase | New Files | Modified Files | Data Files Created |
|-------|-----------|----------------|-------------------|
| P0 | 0 | `mcp_unified_server/server.py`, `mcp_task_server/task_store.py`, `dashboard/server.py` | `locks.json`, `locks.lock` |
| P1 | 1 (`watchdog.ps1`) | `mcp_unified_server/server.py`, `launch_team.bat`, `launch_team_maintenance.bat`, all `ROLE_*.md` | `watchdog_config.json` |
| P2 | 1 (`mcp_task_server/metrics.py`) | `dashboard/server.py`, `dashboard/index.html`, `mcp_unified_server/server.py`, `launch_team.bat`, `launch_team_maintenance.bat` | `metrics.json` |
| P3 | 0 | `mcp_unified_server/server.py`, `ROLE_QA_LEAD.md`, all `ROLE_*.md` | `roles.json`, `backups/`, `logs/errors.json`, `docs/retros/` |

**Also:** Delete `C:\Users\trust\teardown-mp-patches\launch_team.bat` (project root copy) in P3.

---

## Implementation Order Within Phases

- **P0:** 0A → 0B → 0C (sequential, each builds on previous)
- **P1:** 1D → 1C → 1A → 1B (deduplication first so exposed tools benefit; watchdog before handoff since watchdog is the real safety net)
- **P2:** 2D → 2A → 2B → 2C (launch validation first since it's needed for team testing; dashboard before metrics since metrics adds a dashboard section)
- **P3:** 3B → 3F → 3A → 3C → 3E → 3D (dynamic roles first since other items depend on it; launch script cleanup last)

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| P0 lock rewrite breaks task operations | Human runs pytest before team launch; P0 is never team-validated |
| Watchdog restart loop on persistent error | 3-restart limit per terminal per session |
| `auto_commit` stages unwanted files | Use existing implementation with `git add -u` + selective safe dirs (not `git add -A`) |
| Message TTL archives in-progress task notifications | Critical-priority messages exempt from auto-archival |
| `spawn_terminal` role invisible to other terminals | `refresh_roles()` + `roles.json` write after spawn |
| Dashboard POST endpoints triggered by external scripts | Killswitch POST requires `confirm: true` field |

---

## Out of Scope

- Git branch strategy (team works on main, this is a modding project not a production service)
- New dashboard charting libraries (text stats are sufficient)
- New testing frameworks (existing pytest suite is adequate)
- Changes to the mod tooling itself (lint, fix, audit, test)
- Consolidating `mcp_task_server/server.py` into `mcp_unified_server/server.py` (would be valuable but is a larger refactor outside this spec's scope — we import/delegate instead)
