# Build Spec: MCP Task Coordination Server

## Purpose

A local MCP server that runs as a background process. All 3 Claude Code terminals connect to it. It manages a task queue so terminals automatically receive work, report progress, and coordinate without human involvement.

## Architecture

```
MCP Task Server (Python, localhost:3847)
    ├── Terminal 1 (API Surgeon) → calls get_task, complete_task
    ├── Terminal 2 (Mod Converter) → calls get_task, complete_task
    └── Terminal 3 (QA Lead) → calls create_task, get_task, complete_task, review_task, get_status
```

## MCP Tools to Implement

### `get_task(role: string) → task`
Returns the next OPEN task assigned to the given role ("api_surgeon", "mod_converter", "qa_lead"). Automatically marks it IN_PROGRESS. Returns null if no tasks available.

### `complete_task(task_id: string, summary: string) → bool`
Marks a task DONE with a completion summary. Triggers QA review if the task modified mod code.

### `create_task(title: string, role: string, priority: string, description: string, mods: list[string]) → task_id`
Creates a new task. Only QA Lead should call this, but don't enforce — any terminal can create tasks.

### `review_task(task_id: string, approved: bool, notes: string) → bool`
QA Lead reviews a completed task. If not approved, reopens it with notes.

### `get_status() → status`
Returns full queue status: open/in_progress/done counts per role, list of active tasks, recently completed tasks.

### `get_lint_summary() → summary`
Runs `python -m tools.lint` and returns the summary (FAIL/WARN/INFO counts). Any terminal can call this to find new work.

### `get_audit_summary() → summary`
Runs `python -m tools.audit` and returns the feature matrix. Terminals use this to identify gaps.

## Task Schema

```json
{
  "id": "Q3",
  "title": "Add keybind hints to 9 mods",
  "role": "mod_converter",
  "priority": "medium",
  "status": "open",
  "description": "Add keybind hint text in client.draw()...",
  "mods": ["500_Magnum", "AK-47", ...],
  "created_by": "qa_lead",
  "assigned_to": null,
  "completed_at": null,
  "completion_summary": null,
  "review_status": null,
  "review_notes": null
}
```

## File Structure

```
teardown-mp-patches/
  mcp_task_server/
    __init__.py
    server.py          # MCP server with all tools
    task_store.py       # JSON file-based task storage
    tasks.json          # Persistent task data
    start_server.sh     # Launch script
```

## Implementation Details

### server.py
- Use `mcp` Python SDK (install: `pip install mcp`)
- Use stdio transport (Claude Code connects via stdin/stdout)
- Import and call `tools.lint` and `tools.audit` directly for lint/audit tools
- Task store is a simple JSON file (tasks.json) with file locking for concurrent access

### task_store.py
- Read/write tasks.json with `fcntl` or `msvcrt` file locking (Windows)
- Methods: `get_next_task(role)`, `update_task(id, fields)`, `create_task(...)`, `get_all_tasks()`
- Auto-increment task IDs

### Integration — Each Terminal's MCP Config

After building, each terminal needs this in their Claude Code MCP settings:

```json
{
  "mcpServers": {
    "task-coordinator": {
      "command": "python",
      "args": ["C:/Users/trust/teardown-mp-patches/mcp_task_server/server.py"],
      "type": "stdio"
    }
  }
}
```

This can be set via Claude Code settings:
- Global: `C:\Users\trust\.claude\settings.json`
- Or project: `C:\Users\trust\teardown-mp-patches\.claude\settings.json`

### Seed Tasks

Pre-populate tasks.json with current remaining work from TASK_QUEUE.md:

1. **B1** (mod_converter): Add keybind hints to 9 mods — 500_Magnum, AK-47, C4, Desert_Eagle, M249, M4A1, Nova_Shotgun, SCAR-20, SG553, Thruster_Tool
2. **Q3** (qa_lead): Add options menus to 16 no-settings mods — needs settings designed first
3. **Q4** (qa_lead): Full lint review — verify all 48 mods pass lint with only INFO-level findings
4. **Q5** (qa_lead): Regenerate all docs after all work complete

### Auto-Work Loop

Each terminal's role file already has autonomous work instructions. With the MCP server, they replace file-based queue checking with MCP tool calls:

```
1. Call get_task(my_role)
2. If task returned → do the work → call complete_task(id, summary)
3. If no task → call get_lint_summary() → create tasks from findings → goto 1
4. If everything clean → call get_audit_summary() → create tasks from gaps → goto 1
5. If truly nothing left → report "all work complete" to user
```

## Current Project State (for context)

- 48 mods installed at `C:/Users/trust/Documents/Teardown/mods/`
- 0 Tier 1 lint errors
- All options menus added to mods with savegame settings
- Remaining work: keybind hints, options for 16 no-settings mods, Shoot() migration analysis
- Tools: `python -m tools.status`, `python -m tools.lint`, `python -m tools.audit`
- All edits go to `C:/Users/trust/Documents/Teardown/mods/` (NEVER the patches repo)
- CLAUDE.md in project root has all rules

## Build Order

1. `pip install mcp` (if not installed)
2. Create `mcp_task_server/` directory
3. Build `task_store.py` (JSON storage with locking)
4. Build `server.py` (MCP server with all 6 tools)
5. Seed `tasks.json` with current remaining work
6. Test: `python mcp_task_server/server.py` — verify it starts
7. Add MCP config to project `.claude/settings.json`
8. Create `start_server.sh` convenience script
