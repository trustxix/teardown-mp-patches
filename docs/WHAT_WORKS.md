# What Works

Proven fixes and patterns that successfully solve problems. Consult before attempting a fix.

---

## Fix: Hardcode tool gates instead of using savegame options
**Problem:** Control mod's super jump (V), dash (C), slam (F), hover (Space) fired globally regardless of equipped tool.
**Root cause:** Gate was `not getBool("control.toolOnly") or toolActive` — savegame cached the old `false` default, so changing `initBool` default had no effect.
**Fix:** Replace option-based gate with hardcoded `toolActive` check. Changed both `client.tick` (line 274) and `client.draw` (line 383).
**Why it works:** `initBool` only sets a value if the key doesn't exist in the savegame. Once a player has saved `false`, changing the default in code does nothing. Hardcoding bypasses the savegame entirely.
**Rule:** When a gate must always be on, hardcode it. Don't rely on savegame booleans for safety-critical behavior.

---

## Pattern: Tool gating in client.tick
**Correct pattern:**
```lua
local toolActive = GetPlayerTool(p) == TOOL_ID
if not toolActive then return end
-- all key bindings and abilities below this line
```
**Why:** Prevents mod abilities from firing when another tool is equipped. Every mod should gate ALL gameplay inputs (not just `usetool`) behind a tool check.

---

## Fix: Early return with remote player rendering preservation
**Problem:** Bunker_Buster_MP's `r` key (mode cycling) fired with any tool equipped.
**Root cause:** `client.tick` checked `currentTool ~= "bunkerbustermissile"` but only reset state — no `return`. All key inputs below ran unconditionally.
**Fix:** Added `return` after the wrong-tool cleanup, BUT moved the remote player tool rendering ABOVE the return so other players' bunker busters still display correctly.
**Rule:** When adding early returns to `client.tick`, check if there's remote player rendering (SetToolTransform for other players) that must run regardless of local tool. Move it before the gate.

---

## Scan result: Most mods ARE properly gated (2026-03-20)
**What we checked:** All 125 installed mods scanned for ungated raw key inputs.
**Result:** Only 2 mods needed fixes (Control, Bunker_Buster_MP). All others use valid gate patterns.
**Common gate patterns found in the wild:**
1. `if GetPlayerTool(p) ~= "toolid" then return end` (Framework mods, most common)
2. `local hasTool = (GetPlayerTool(p) == "toolid") ... if hasTool then` (Thruster_Tool)
3. `if GetPlayerTool() == "toolid" then` (Light_Katana_MP — no `p` param, works in client context)
4. Compound: `if data and IsPlayerLocal(p) and GetPlayerTool(p) == TOOL_ID then` (Melt)

---

## Fix: Move tool check ABOVE options toggle, not below
**Problem:** GYM_Ragdoll and Fire_Locator had tool checks AFTER the O key handler — options opened with any tool.
**Fix:** Move the `GetPlayerTool(p)` check and early return above the `InputPressed("o")` line.
**Rule:** Tool gates must be the FIRST logic in any input handler. Check tool → check options open → process keys.

---

## Fix: Bunker Buster MP desync improvements (5 fixes, 2026-03-20)
**Status: VERIFIED in single-player (2026-03-20). MP test on hold.**

### Fix 1: shared.spawnTargets cleanup
**Problem:** Every strike appended to `shared.spawnTargets` but entries were never removed. Over a long session, the shared table grows unbounded → engine syncs larger payloads to all clients every frame → lag.
**Fix:** Added cleanup in `server.tick` — removes entries older than 60 seconds.

### Fix 2: shared.spawnHandleTargets cleanup
**Problem:** Same issue — handle→target mappings accumulated forever even after missiles were destroyed.
**Fix:** Added cleanup in `server.tick` — removes entries where `IsHandleValid(h)` returns false (missile entity destroyed).

### Fix 3: Move aim raycast from client.update to client.tick
**Problem:** `client.update` runs at fixed 60Hz (0-2 times per frame). `client.tick` runs every frame. If game runs >60fps, clicking in `tick` reads stale aim data from the last `update` — strike could land at a slightly wrong position.
**Fix:** Moved the full aim raycast computation (QueryRaycast, muzzle calculation) into `client.tick` right before input handling. Removed the duplicate from `client.update`.

### Fix 4: Cache GetString("game.player.tool")
**Problem:** Called 8+ times per frame in `client.tick` — each call is a registry lookup.
**Fix:** `currentTool` variable already existed at top of `client.tick`. Replaced all downstream occurrences with `currentTool`. Left `getFirstPersonAim()` and `client.draw()` untouched (different scope).

### Fix 5: Remove fallback for id = 1, 32 loop
**Problem:** `client.tick` had a v1 fallback that iterated player IDs 1-32 with pcall when `Players()` wasn't available. In v2, `Players()` is always available.
**Fix:** Removed the `type(Players)` check and the fallback loop. Just uses `for id in Players()` directly.

---

## Fix: Clean up shared.playerData on disconnect (All_In_One_Utilities)
**Problem:** `shared.playerData[playerID]` was never cleaned up when players left. New player inheriting the same ID slot got the previous player's fly/noclip/godmode state.
**Root cause:** Mod uses `GetAllPlayers()` instead of `PlayersRemoved()` (no `player.lua` include). No disconnect cleanup existed.
**Fix:** Added a cleanup pass at the top of `server.tick` — builds a set of active player IDs, then removes any `shared.playerData` entries not in the set.
**Rule:** Any mod storing per-player state in `shared` tables must clean up on disconnect, even if it doesn't use `PlayersRemoved()`.

---

## Fix: PauseMenuButton must be in tick(), not draw()
**Problem:** PauseMenuButtons added in `client.draw()` / `draw()` didn't appear in the pause menu.
**Root cause:** `PauseMenuButton()` only registers buttons when called from `tick()` / `client.tick()`. Calling it in `draw()` has no effect.
**Fix:** Move all `PauseMenuButton()` calls to the `tick()` function. Keep UI rendering (UiMakeInteractive, options panels, HUD) in `draw()`.
**Verified working:** Hurricanes, Bunker Buster, Adjustable Fire all use PauseMenuButton in tick.

---

## Fix: Remove recoil position offset from SetToolTransform (prevents tool floating)
**Problem:** After shooting, the weapon model floats away from the player's hands in zero gravity. Affects 21+ gun mods.
**Root cause:** SetToolTransform called with recoilTimer-based Z position offset (`Vec(0, 0.2, recoilTimer)`) causes the tool body to clip into the player's physics body. The engine collision pushes the tool away. Between shots it drifts; on the next shot, SetToolTransform snaps it back briefly.
**What the v1 original did:** Same recoil pattern but v1 has no server/client physics split — the single context kept the body stable.
**Fix:** Remove ALL recoilTimer/swingTimer position offsets from SetToolTransform. Use a static base position only. Keep timer decrements (clamped to 0) for other logic that depends on them.
**Rule:** Never modify SetToolTransform position based on a timer. Static positions only. Also never use SetShapeLocalTransform with position offsets for recoil — this causes the same floating. Only rotation-only shape transforms are safe. Visual recoil should use ToolAnimator (like the ARM mods do) which handles positioning without physics interference.
**Applied to:** 21 mods (P90, AK-47, AWP, M1_Garand, M249, M4A1, Desert_Eagle, Nova_Shotgun, SCAR-20, Minigun, Multi_Grenade_Launcher, Multiple_Grenade_Launcher, Charge_Shotgun, Hook_Shotgun, Bee_Gun, Exploding_Star, HADOUKEN, Holy_Grenade, Magic_Bag, Dual_Berettas confirmed not needed).

---

## Fix: Hide XML prefab tools from Tool Menu (Q)
**Problem:** 4 tools (ARM M4A4, ARM AK-47, ARM Glock, Light Saber GP) appear invisible/broken when switched to via Tool Menu. They all use XML prefab files for registration instead of .vox files.
**Root cause:** `SetString("game.player.tool")` and `SetPlayerTool()` can't properly initialize XML prefab tool bodies — only the engine's toolbar handler does this.
**Fix:** Filter XML prefab tools out of the Tool Menu using case-insensitive matching: `id:lower():find("arm-")` for ARM mods, exact match for `lsaber2`. Use toolbar (1-6 keys) for these tools.
**Rule:** When filtering tool IDs from `ListKeys('game.tool')`, always use case-insensitive comparison — the engine may return IDs in different case than `RegisterTool` specified.

---

## Fix: Tool Menu tool switching deferred to tick
**Problem:** Tool Menu's `SetString("game.player.tool")` was called inside `client.draw()` during UI rendering, causing incomplete tool initialization.
**Fix:** Defer the switch to `client.tick()` via `pending_tool_switch` variable. Also use `ServerCall("server.switchTool")` with `SetPlayerTool(toolId, p)` for proper v2 server-side switching. Tool enable/disable uses `ServerCall("server.setToolState")` with `SetToolEnabled` + `SetToolAmmo` for v2 per-player compatibility.

---

## Fix: Non-tool mods should use PauseMenuButton, not keybinds
**Problem:** Hurricanes_and_Blizzards opened its control panel on a configurable key (default "o") globally — no tool to gate behind.
**Fix:** Disabled the keybind shortcut, kept `PauseMenuButton("Hurricane")` in the ESC menu (already existed).
**Rule:** Mods without a tool should use `PauseMenuButton()` for settings access, not raw key bindings.

---

## Fix: Dynamic keybind variables bypass lint — manual review required (Issue #73)
**Problem:** Thruster_Tool_Multiplayer thrusters non-functional for non-host players. Lint showed 0 findings because `InputPressed(rocket.keybind, p)` uses a variable for the key name, not a string literal.
**Root cause:** RAW-KEY-PLAYER lint rule only matches string patterns like `InputPressed("rmb", p)`. Variable key names are invisible to the regex.
**Fix:** Same as all RAW-KEY-PLAYER fixes — move input to client with `IsPlayerLocal(p)`, bridge to server via `ServerCall`. The hard part is finding the bug.
**Rule:** After lint reports 0 findings, grep for `Input(Pressed|Down|Released)\([^"']` (first arg not a string) to catch dynamic keybind+player bugs.

---

## Fix: Entity script v2 conversion — minimal approach for map/vehicle scripts (Issue #68)
**Problem:** V1 entity scripts (attached to XML entities via `tags="script=foo.lua"`) are silently disabled in MP — no error, no warning, just missing features (vehicle physics, doors, sirens, lights).
**Root cause:** Entity scripts need independent `#version 2` + v2 callbacks. Converting only `main.lua` does NOT fix entity scripts.
**Fix pattern:**
1. Add `#version 2` at top of file
2. Rename `init()` → `server.init()`
3. Rename `tick()` → `server.tick(dt)`
4. Rename `update(dt)` → `server.update(dt)` (keep fixed 60Hz for visual effects)
5. Add empty `function client.init() end` at bottom (v2 compliance)
6. For vehicle input: find the driver via `GetAllPlayers()` + `GetPlayerVehicle(p)` loop, pass player param to `InputDown("action", driver)`

**Cosmetic tradeoffs:** `SpawnParticle()`/`PointLight()` in server callbacks only render for the host. Core gameplay (Explosion, SpawnFire, MakeHole, DriveVehicle, PlaySound) auto-syncs to all clients. Accept cosmetic particle loss for minimal-effort conversions.
**Rule:** Entity scripts with fundamental MP issues (no player iteration, host-only input, shared mutable state) should get `@deepcheck-ok ENTITY` annotations and be deferred to a future vehicle-entity-refactor pass.
**Applied to:** 140 entity scripts across 18 mods (100% complete as of 2026-03-22). Original 81 across 11 mods (2026-03-21), plus 59 new scripts in 7 mods added during workshop sync: Volkograd_Town_2_Remastered (5), Volkotomsk_Town (7), Russian_Town_5_MP (13), Russian_Town_5_Winter_MP (1), Chebyrmansk_Town_MP (29), DAM_MP_Optimized (3), AndRe's_BMW_E36 (1). Voxel_Plaza has 184 additional v1 entity scripts identified but deferred (map features, low priority).

---

> **Base game patterns** (PlaySound auto-sync, ToolAnimator for all players, shared tables, event-driven deaths, registry broadcast, ClientCall(0), PlayersRemoved cleanup) are documented in `docs/BASE_GAME_MP_PATTERNS.md` — not duplicated here.
