# Project Consolidation v2 — Cleanup, Streamline, Automate

> **For agentic workers:** Execute tasks in order. Steps use checkbox syntax for tracking.

**Goal:** Clean up organizational debt, remove stale content, consolidate redundant docs, and wire tools/hooks into an automated workflow.

**Architecture:** Archive stale files, consolidate overlapping docs, update references to match reality, add automation hooks.

---

## Task 1: Archive 19 stale root scripts

- [ ] Create `archive/batch_scripts/` directory
- [ ] Move all 19 root .py scripts there (NOT activate_all_local_mods.py or launch_teardown.vbs -- those are active)
- [ ] Scripts to move: add_client_tracers.py, add_toolconfig.py, apply_ui_standards.py, convert_guns_arm.py, copy_new_mods.py, fix_recoil_float.py, fix_tool_grab.py, fix_tool_groups.py, gate_options_host.py, generate_watchdog_config.py, scan_desync_patterns.py, scan_ungated_keys.py, scan_ungated_options.py, sync_complex_settings.py, sync_mods.py, sync_remaining_settings.py, sync_settings.py, sync_simple_settings.py
- [ ] Create archive/batch_scripts/README.md: "One-time batch processors from March 2026. Superseded by tools/. Historical reference only."

## Task 2: Archive stale root docs

- [ ] Create `archive/old_docs/` directory
- [ ] Move: BUILD_ADDITIONAL_SERVERS.md, BUILD_MCP_TASK_SERVER.md, QA_MENU.md, TASK_QUEUE.md
- [ ] These describe planned/completed infrastructure -- no longer actionable

## Task 3: Slim down ROLE files

Each ROLE file repeats the same loop structure. Consolidate to role-specific content only.

- [ ] Read all 5 ROLE_*.md files
- [ ] For each, strip the repeated "work loop" boilerplate (check inbox, get task, etc.) -- that's in CLAUDE.md
- [ ] Keep ONLY role-specific authority, decision examples, and expertise area
- [ ] Target: each ROLE file should be ~30-50 lines, not 100-300
- [ ] ROLE_MAINTAINER.md -- check if still needed or archive

## Task 4: Clean stale comms

- [ ] Delete all files in .comms/*/outbox/ and .comms/*/archive/ (old messages from previous sessions)
- [ ] Reset .comms/heartbeats.json to empty: {}
- [ ] Keep FOCUS.md (already updated), PROTOCOL.md, TRIGGERS.md, TEAMWORK.md

## Task 5: Update CLAUDE.md -- final pass

Key updates needed:
- [ ] Remove hardcoded mod counts -- replace with "run tools.status"
- [ ] Add new lessons to "Known Subagent Bugs" section:
  - #19: No local at file scope in v2 (preprocessor splits chunks)
  - #20: mousedx/mousedy valid for SetCameraTransform cameras (camerax/cameray returns 0)
  - #21: Surgical fixes over rewrites (test incrementally, one change at a time)
  - #22: GetAddedPlayers() (engine built-in) vs PlayersAdded() (requires player.lua include)
  - #23: Camera sensitivity pattern: GetInt("options.input.sensitivity") / 1000 * (zoomlevel / defaultZoom)
- [ ] Update "Do NOT Use Agents/Subagents" -- this rule was from bad experiences; add nuance about when agents are OK (research, independent file reads) vs not OK (code edits)
- [ ] Verify the mod directory table matches current reality
- [ ] Add "File Integrity" section: all players need identical mod files for MP

## Task 6: Update MASTER_MOD_LIST.md

- [ ] Add "Current State (2026-03-23)" section at top with 49 mods
- [ ] List mods by category: 4 working tools, 14 fixed tools, 13 v1 disabled, 16 content/maps
- [ ] Mark old batch history as "Archive" section (don't delete)

## Task 7: Update README.md and QUICKSTART.md

- [ ] Read both files
- [ ] Remove hardcoded mod counts
- [ ] Update paths from Documents/ to game install dir
- [ ] Simplify QUICKSTART to match current workflow

## Task 8: Update ISSUES_AND_FIXES.md

- [ ] Add header note: "Project reset 2026-03-23: path changed to game install dir, 49 mods"
- [ ] Add new issues discovered today:
  - #74: VecCopy doesn't exist in Teardown Lua
  - #75: local at file scope invisible across v2 chunks
  - #76: camerax/cameray returns 0 when SetCameraTransform active
  - #77: PlayersAdded() requires player.lua include
  - #78: File integrity check -- all players need identical mod files
  - #79: AC-130 500-element shared table sync bomb (fixed: pool 500->30, cached sounds)

## Task 9: Verify all tools work end-to-end

- [ ] `python -m tools.status` -- shows 89 mods (49 ours + 40 built-in)
- [ ] `python -m tools.sync --status` -- compares correctly
- [ ] `python -m tools.deploy_framework --fix-lua` -- fixes lua files in game install dir
- [ ] `python -m tools.lint --mod "Tripmine"` -- finds a known-good mod
- [ ] `python -m tools.logparse` -- parses game log correctly
- [ ] Grep for any remaining Documents/ references in code: `grep -rn "Documents/Teardown/mods" --include="*.py"`

---

## Execution Order

1. Tasks 1-2: Archive stale files (clean up clutter)
2. Tasks 3-4: Slim docs and clean comms (reduce noise)
3. Tasks 5-8: Update content (accuracy)
4. Task 9: Validate everything works
