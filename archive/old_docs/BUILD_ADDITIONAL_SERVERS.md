# Additional MCP Servers — Build Specs

## 1. File Lock Server (HIGH PRIORITY)

**Problem:** Two terminals can edit the same mod file at the same time, causing overwrites and corruption.

**Solution:** A lock server that terminals must call before editing any file.

**Tools:**
- `lock_file(role, filepath)` → acquires exclusive lock, returns success/fail + who holds it
- `unlock_file(role, filepath)` → releases lock
- `list_locks()` → shows all active locks and who holds them
- `force_unlock(filepath)` → QA Lead only, breaks a stuck lock

**Behavior:**
- Locks auto-expire after 5 minutes (prevents stale locks from crashed terminals)
- If a terminal tries to lock a file held by another, it gets back who holds it so it can message them
- Store locks in memory (dict) — no persistence needed, locks reset on server restart

**Integration:** Add to `.mcp.json` alongside task-coordinator. All terminals should call `lock_file` before any Edit/Write on mod files.

**File:** `mcp_lock_server/server.py`

---

## 2. Mod Registry Server (HIGH PRIORITY)

**Problem:** Every terminal reads main.lua just to answer "what tool ID does this mod use?" or "does this mod have an options menu?" — wasteful and slow.

**Solution:** A registry that indexes all mod metadata once and serves queries instantly.

**Tools:**
- `query_mod(mod_name)` → returns: tool_id, display_name, has_options, has_keybinds, has_ammo, savegame_keys, file_count, line_count
- `query_mods(filter)` → filter by feature: "missing_options", "has_savegame", "is_gun", "missing_hints"
- `refresh_registry()` → re-scans all mods (call after batch of edits)
- `get_mod_diff(mod_name)` → what changed since last refresh (for docs_keeper)

**Behavior:**
- On startup, scans all `C:/Users/trust/Documents/Teardown/mods/*/main.lua`
- Extracts: RegisterTool ID, display name, savegame keys, feature flags (same as audit.py but cached)
- Stores in memory — fast queries, no file I/O per request
- `refresh_registry()` re-scans and returns a diff of what changed

**File:** `mcp_registry_server/server.py`

---

## 3. Change Tracker Server (MEDIUM PRIORITY)

**Problem:** Docs keeper has to manually scan outboxes and git log to find undocumented work. No single source of truth for "what changed."

**Solution:** A server that records every change as it happens and provides a changelog.

**Tools:**
- `record_change(role, mod_name, change_type, description)` → log a change
- `get_changes(since_minutes=30)` → all changes in last N minutes
- `get_changes_by_mod(mod_name)` → all changes to a specific mod
- `get_undocumented_changes()` → changes not yet marked as documented
- `mark_documented(change_id)` → docs keeper calls this after updating docs

**Change types:** `bug_fix`, `feature_add`, `api_migration`, `polish`, `conversion`, `tool_update`, `rule_add`

**Behavior:**
- Other terminals call `record_change()` after every meaningful edit (integrated into complete_task flow)
- Docs keeper polls `get_undocumented_changes()` to find work
- Persists to `mcp_change_tracker/changes.json`

**File:** `mcp_change_tracker/server.py`

---

## 4. Template Server (MEDIUM PRIORITY)

**Problem:** Every options menu, keybind hint block, and createPlayerData pattern is copy-pasted with manual substitution. Error-prone and slow.

**Solution:** A server that generates code from templates with parameters.

**Tools:**
- `generate_options_menu(tool_id, display_name, settings)` → returns complete Lua code for an O-key options menu
  - settings: `[{"name": "unlimitedammo", "type": "bool", "label": "Unlimited Ammo", "default": false}]`
- `generate_keybind_hints(keybinds)` → returns client.draw() hint block
  - keybinds: `[{"key": "LMB", "action": "Fire"}, {"key": "R", "action": "Reload"}]`
- `generate_player_data(fields)` → returns createPlayerData() with proper structure
- `generate_server_init(tool_id, display_name, vox_path, group, ammo_amount)` → returns server.init()

**Behavior:**
- Templates are Lua strings with `{placeholders}` filled by parameters
- Includes all required patterns: UiMakeInteractive, server.setOptionsOpen, optionsOpen guard, etc.
- Generated code is guaranteed lint-clean

**File:** `mcp_template_server/server.py`

---

## Build Order

1. **File Lock Server** — prevents data corruption, build first
2. **Mod Registry Server** — speeds up every terminal, high ROI
3. **Change Tracker** — unblocks docs_keeper automation
4. **Template Server** — eliminates copy-paste errors

## Integration

After building each, add to `.mcp.json`:
```json
{
  "mcpServers": {
    "task-coordinator": { ... },
    "file-lock": {
      "command": "python",
      "args": ["C:/Users/trust/teardown-mp-patches/mcp_lock_server/server.py"],
      "type": "stdio"
    },
    "mod-registry": {
      "command": "python",
      "args": ["C:/Users/trust/teardown-mp-patches/mcp_registry_server/server.py"],
      "type": "stdio"
    },
    "change-tracker": {
      "command": "python",
      "args": ["C:/Users/trust/teardown-mp-patches/mcp_change_tracker/server.py"],
      "type": "stdio"
    },
    "template-engine": {
      "command": "python",
      "args": ["C:/Users/trust/teardown-mp-patches/mcp_template_server/server.py"],
      "type": "stdio"
    }
  }
}
```
