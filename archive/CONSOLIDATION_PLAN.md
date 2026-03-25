# Project Consolidation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Update all project tooling, docs, and paths to reflect the current state: 49 mods in game install directory, not Documents/.

**Architecture:** Surgical updates to existing files. No rewrites. Change paths, update counts, remove stale content. Keep all proven patterns and knowledge intact.

**Tech Stack:** Python (tools), Markdown (docs), VBScript (launcher)

---

## File Map

### Files to UPDATE (path + state changes):
- `CLAUDE.md` -- paths partially updated, state/counts stale
- `tools/sync.py` -- targets Documents/ path
- `tools/deploy_framework.py` -- targets Documents/ path
- `tools/status.py` -- reads from Documents/ path
- `tools/common.py` -- likely defines the base path constant
- `activate_all_local_mods.py` -- targets Documents/ path + old modlists
- `launch_teardown.vbs` -- runs old activator
- `MASTER_MOD_LIST.md` -- references old 102-mod batches
- `.comms/FOCUS.md` -- stale focus area
- `QUICKSTART.md` -- setup instructions with old paths
- `README.md` -- project overview with old paths
- `ISSUES_AND_FIXES.md` -- still valid but needs state update note
- `hooks/post_edit_lint.py` -- path reference
- `hooks/pre_edit_guard.py` -- path reference

### Files that are STILL CORRECT (no changes needed):
- `docs/BASE_GAME_MP_PATTERNS.md` -- patterns are timeless
- `docs/MP_REFERENCE.md` -- API reference, still correct
- `docs/WHAT_WORKS.md` -- patterns still valid
- `docs/WHAT_DOESNT_WORK.md` -- updated today
- `docs/MPLIB_INTERNALS.md` -- mplib hasn't changed
- `docs/UI_STANDARDS.md` -- layout standards unchanged
- `docs/UMF_TRANSLATION_GUIDE.md` -- UMF patterns unchanged
- `docs/BALLISTICS_FRAMEWORK.md` -- framework docs unchanged

### Files to CONSIDER REMOVING (stale, no longer used):
- 19 root `.py` scripts (scan_ungated_keys.py, fix_recoil_float.py, etc.) -- one-off scripts from old batches
- `BUILD_ADDITIONAL_SERVERS.md`, `BUILD_MCP_TASK_SERVER.md` -- MCP build docs (server already built)
- `QA_MENU.md` -- old QA menu
- `TASK_QUEUE.md` -- old task queue (replaced by MCP)
- `.comms/heartbeats.json` -- stale team heartbeats
- `.comms/*/outbox/` and `.comms/*/archive/` -- old messages

---

## Task 1: Update the base path constant in tools

**Files:**
- Modify: `tools/common.py`

- [ ] Read `tools/common.py`, find the `MODS_DIR` or equivalent path constant
- [ ] Change from `Documents/Teardown/mods` to `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods`
- [ ] Check if there's a `WORKSHOP_DIR` constant -- should stay unchanged
- [ ] Run `python -m pytest tests/ -q` to see what breaks
- [ ] Fix any test failures caused by path change

---

## Task 2: Update tools/sync.py

**Files:**
- Modify: `tools/sync.py`

- [ ] Read `tools/sync.py`
- [ ] Update target directory from Documents/ to game install dir
- [ ] Update removed-mods backup path if needed
- [ ] Verify dry-run works: `python -m tools.sync`
- [ ] Test: `python -m tools.sync --status`

---

## Task 3: Update tools/deploy_framework.py

**Files:**
- Modify: `tools/deploy_framework.py`

- [ ] Read the file, find path references
- [ ] Update `--fix-lua` target from Documents/ to game install dir
- [ ] Update framework deployment target path
- [ ] Test: `python -m tools.deploy_framework --fix-lua` (dry run)

---

## Task 4: Update tools/status.py

**Files:**
- Modify: `tools/status.py`

- [ ] Read the file, find where it counts installed mods
- [ ] Update path to game install dir
- [ ] Test: `python -m tools.status`
- [ ] Verify mod count shows 49 (not 0)

---

## Task 5: Update activate_all_local_mods.py

**Files:**
- Modify: `activate_all_local_mods.py`

- [ ] Read the file
- [ ] Update scan directory from Documents/ to game install dir
- [ ] Update mod ID prefix if needed (was `local-`, might need `builtin-` for game install dir)
- [ ] Test: `python activate_all_local_mods.py` (preview mode)

---

## Task 6: Update launch_teardown.vbs

**Files:**
- Modify: `launch_teardown.vbs`

- [ ] Read the file
- [ ] Verify it calls activate_all_local_mods.py (which we just updated)
- [ ] No path changes needed if it delegates to the Python script
- [ ] If it has hardcoded paths, update them

---

## Task 7: Update hooks

**Files:**
- Modify: `hooks/post_edit_lint.py`
- Modify: `hooks/pre_edit_guard.py`

- [ ] Read both files
- [ ] Update any Documents/ path references to game install dir
- [ ] These hooks guard against editing wrong directories -- make sure the guard now protects the game install dir

---

## Task 8: Update CLAUDE.md -- state and counts

**Files:**
- Modify: `CLAUDE.md`

The paths section was partially updated. Now update:
- [ ] Mod count: 102 -> 49 everywhere
- [ ] The "Active Mod Count Ceiling" section -- 49 is well under 150 limit
- [ ] The batch system references -- update to reflect current 49 mods, not 102
- [ ] The "Do NOT Use Agents/Subagents" rule -- keep or revise based on user preference
- [ ] The "Known Subagent Bugs" section -- add the new lessons (no local at file scope, mousedx for script cameras, surgical fixes over rewrites)
- [ ] Verify all tool commands still reference correct paths

---

## Task 9: Update MASTER_MOD_LIST.md

**Files:**
- Modify: `MASTER_MOD_LIST.md`

- [ ] Add a "Current State (2026-03-23)" section at the top
- [ ] List all 49 mods with their status (4 working tools, 14 fixed tools, 13 v1 disabled, 6 maps, 12 content)
- [ ] Mark old batch history as archived (don't delete -- it's useful history)
- [ ] Note the path change from Documents/ to game install dir

---

## Task 10: Update .comms/FOCUS.md

**Files:**
- Modify: `.comms/FOCUS.md`

- [ ] Update to reflect current state: 49 mods, fixes applied, pending MP playtest
- [ ] Clear old priorities (compile errors, deepcheck WARNs for mods we no longer have)
- [ ] New priority: MP playtest with friends, Workshop publishing

---

## Task 11: Update QUICKSTART.md and README.md

**Files:**
- Modify: `QUICKSTART.md`
- Modify: `README.md`

- [ ] Read both files
- [ ] Update all Documents/ path references to game install dir
- [ ] Update mod counts
- [ ] Update setup instructions to reflect new workflow

---

## Task 12: Clean up stale root scripts

**Files:**
- Review: 19 root `.py` scripts

- [ ] List all root .py scripts
- [ ] Identify which are one-off batch scripts no longer needed (fix_recoil_float.py, scan_ungated_keys.py, etc.)
- [ ] Move stale scripts to a `scripts_archive/` folder (don't delete -- might have useful patterns)
- [ ] Keep any scripts that are still actively used (activate_all_local_mods.py, launch_teardown.vbs)

---

## Task 13: Clean up stale comms

**Files:**
- Clean: `.comms/*/outbox/`, `.comms/*/archive/`

- [ ] Clear old outbox messages (these are from previous sessions)
- [ ] Clear archive folders
- [ ] Keep PROTOCOL.md, TRIGGERS.md, TEAMWORK.md (still valid for future team use)
- [ ] Reset heartbeats.json

---

## Task 14: Update ISSUES_AND_FIXES.md

**Files:**
- Modify: `ISSUES_AND_FIXES.md`

- [ ] Add a header note: "Project reset 2026-03-23: 102 mods -> 49 mods, path changed to game install dir"
- [ ] Add new issues from today's session: AC-130 rewrite failures (#74-78), file integrity discovery
- [ ] Keep all existing issues -- they document patterns that apply to future mods

---

## Task 15: Update project memory files

**Files:**
- Modify: `~/.claude/projects/C--Users-trust/memory/project_teardown_mp_patcher.md`
- Modify: `~/.claude/projects/C--Users-trust/memory/feedback_deploy_to_local_mods.md`
- Modify: `~/.claude/projects/C--Users-trust/memory/project_teardown_session_state.md`

- [ ] Update project_teardown_mp_patcher.md with final current state
- [ ] Update feedback_deploy_to_local_mods.md -- this is NOW WRONG, mark as superseded by feedback_mp_lobby_mod_location.md
- [ ] Update project_teardown_session_state.md -- 48 mods patched is stale, now 49 mods with 14 fixed

---

## Task 16: Run full validation

- [ ] `python -m tools.status` -- verify it reads from correct path and shows 49 mods
- [ ] `python -m tools.sync --status` -- verify it compares against correct dirs
- [ ] `python -m pytest tests/ -q` -- verify no tests broke from path changes
- [ ] Grep entire project for any remaining Documents/Teardown/mods references: `grep -r "Documents/Teardown/mods" --include="*.py" --include="*.md"`
- [ ] Fix any remaining references

---

## Execution Order

Tasks 1-7 are the critical path (tools + paths). Do these first and validate.
Tasks 8-14 are documentation updates. Do these second.
Task 15-16 are cleanup and final validation.

**Estimated scope:** Tasks 1-7 are small code changes. Tasks 8-14 are text edits. No new features, no rewrites -- just updating existing content to match reality.
