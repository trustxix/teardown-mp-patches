# Teardown MP Patcher - Issues and Fixes Log

All resolved bugs and the rules derived from them. Consult before making changes. Append after fixing new issues.

## Key Rules (condensed from all 73 issues)

1. NEVER use `goto` or `::label::` (Lua 5.1 only)
2. NEVER use raw key names with player parameter - use ServerCall pattern
3. Camera input depends on context: normal gameplay camera = `camerax`/`cameray`; custom camera via SetCameraTransform = `mousedx`/`mousedy` (camerax returns 0 when script-controlled)
4. ALWAYS use `GetPlayerEyeTransform(p)` for camera position
5. Every mod with keybinds must show them on-screen
6. Always include group number in RegisterTool
7. Send ALL aim geometry from same client frame - never mix client aim with server eye transform
8. ~~options.lua stays UNCHANGED~~ **OUTDATED** — options.lua MUST be converted to v2 with `#version 2` + `client.init()`/`client.draw()` callbacks (Issue #71, all 9 converted 2026-03-20)
9. SetPlayerTransform is SERVER-ONLY
10. SetToolAmmo is REQUIRED in PlayersAdded
11. Use `ClientCall` to sync server state that client needs for HUD/input gating
12. Use `getOptions()` savegame reads for options - never cache in `data.*` on server
13. Gate tool input with `not data.optionsOpen` on BOTH server AND client
14. Sync `optionsOpen` to server via `server.setOptionsOpen` ServerCall
15. ALWAYS call `UiMakeInteractive()` before `UiPush()` in options menus
16. ALWAYS edit files in `C:/Users/trust/Documents/Teardown/mods/` - NEVER the patches repo
17. When freezing player position (scope/flycam), ALWAYS preserve rotation
18. Melee/projectile weapons MUST use `QueryShot()` + `ApplyPlayerDamage()` — `MakeHole()` is voxel-only
19. Never have two mods registering the same tool ID — remove v1 when v2 rewrite exists
20. `SetPlayerHealth(health, player)` — health FIRST, player SECOND (reverse silently affects wrong player)
21. Gate client projectile physics with `IsPlayerLocal(p)` — never simulate for remote players
22. Use registry sync for continuous state, `ServerCall`/`ClientCall` for events only
23. Throttle `FindShapes()`/`QueryAabb()` to ≤4Hz — never per-tick per-player
24. `SpawnParticle()`/`PointLight()`/`SetShapeEmissiveScale()` are CLIENT-ONLY — never call on server. **EXCEPTION: `PlaySound()` works on server and auto-syncs to all clients** (see BASE_GAME_MP_PATTERNS.md Pattern 10)
25. `QueryShot()` + `ApplyPlayerDamage()` on SERVER — client uses `QueryRaycast()` for visuals
26. Always guard `ApplyPlayerDamage()` with `player ~= 0` after `QueryShot()` — player 0 = host. `if player then` is WRONG (Lua 0 is truthy)
27. Always use 4-param `ApplyPlayerDamage(target, damage, toolId, attacker)` — for environmental hazards, pass `0` as attacker
28. `ServerCall("server.fn", p, ...)` — player ID is REQUIRED, NOT auto-injected by engine
29. `Explosion()` does NOT damage players — add explicit `ApplyPlayerDamage()` with distance falloff + tool ID for kill attribution
30. `ClientCall(0, ...)` for world-space effects (sounds, particles at positions). `ClientCall(p, ...)` only for personal feedback (camera shake, recoil, HUD sync)
31. All asset paths MUST use `MOD/` prefix in v2: `LoadSound("MOD/snd/fire.ogg")`. Without it, assets silently fail to load (v1 resolved relative paths automatically)
32. NEVER copy preview.jpg/preview.png from workshop into Documents/Teardown/mods/ — strncpy buffer overflow. Monitor active mod count: warn at 150+, engine crashes ~178
33. V2 scripts MUST define at least one callback (`server.init()`, `client.init()`, etc.) — empty stubs with only `#version 2` + includes cause "Error compiling"
34. Entity scripts on XML entities MUST have `#version 2` + v2 callbacks — without it, they are silently disabled in MP (no error, just missing features)
35. `#version 2` can appear on any line — preprocessor scans the whole file. Do NOT enforce line-1 placement. Ensure LF-only line endings (CRLF breaks preprocessor)
36. Shared `players[p]` on host causes double-processing — use separate fields for server-authoritative state vs client visual-only state (e.g., `data.bulletsInAir` vs `data.clientTracers`)
37. `options.lua` needs independent `#version 2` + v2 callbacks — same as entity scripts (Issue #68). Converting only `main.lua` does NOT fix options.lua

> **Note:** Issues #1-19 were resolved in earlier sessions. Their rules are captured above. Detailed entries for #1-19 are no longer available but all patterns are encoded in the lint tool (`python -m tools.lint`).

---

## Issue #20: Options menus missing cursor and wrong position

**Symptom:** Custom options menus for Mjölner, Scorpion, Hook Shotgun, M1 Garand, Exploding Star, Laser Cutter don't show a cursor and appear centered on screen instead of on the left side like the Black Hole menu.

**Root cause:** The subagent that created the menus used `UiRect` instead of `UiImageBox` and positioned them centered. Most critically, some were missing `UiMakeInteractive()` which enables the cursor.

**Fix:** All options menus must follow the Black Hole pattern exactly:
```lua
if data.optionsOpen then
    UiMakeInteractive()  -- REQUIRED for cursor
    UiPush()
    UiTranslate(20, UiMiddle() - HEIGHT/2)  -- LEFT side
    UiAlign("top left")
    UiColor(0, 0, 0, 0.75)
    UiImageBox("ui/common/box-solid-6.png", 650, HEIGHT, 6, 6)  -- proper box
    -- ... content with UiFont("regular.ttf", 26) ...
    UiPop()
end
```

**RULE: All options menus must use the Black Hole layout pattern. Always test that cursor appears.**

**Date fixed:** 2026-03-17

---

## Issue #21: Black Hole detonation visual too subtle

**Symptom:** Detonated black holes are invisible — just dark smoke that's hard to see. User expected a visible vortex effect.

**Root cause:** Original v1 only used `SpawnParticle("darksmoke")` which is inherently dark and hard to see. No sprites or distinctive visual markers.

**Fix:** Enhanced visual with multi-layered effect:
- Bright purple PointLight glow (scales with size)
- Orbiting dark smoke particles pulling toward center (3 particles per frame)
- Inner dark core particle
- Purple DrawLine ring segments rotating around the black hole
- Much more visible even from a distance

**Date fixed:** 2026-03-17

---

## Issue #22: AWP scope can only look left/right + sway + wrong reload math

**Symptom:** While scoped, player can only look horizontally. Scope sways side to side. Reload takes full 10 rounds from reserve instead of only what's needed.

**Root cause:**
1. Server froze BOTH position AND rotation during zoom (should only freeze position)
2. Camera offset of 0.5 units caused visible sway as player rotated
3. Reload logic set ammo=10 and deducted one full mag, instead of calculating rounds needed

**Fix:**
1. `SetPlayerTransform(Transform(frozenPos, GetPlayerTransform(p).rot), p)` — always keep current rotation
2. Use `SetCameraTransform(eyeT, fov)` directly without offset, hide tool with `SetToolTransform(Vec(0,-10,0))`
3. Calculate rounds needed: `toLoad = min(10 - currentAmmo, availableReserve)`

**RULE: When freezing player during scope/flycam, ALWAYS preserve rotation. Only freeze position.**

**Date fixed:** 2026-03-17

---

## Issue #23: Engine "101" ammo display showing on 7 mods

**Symptom:** C4, Lightsaber, Black Hole, Attack Drone, Bee Gun, Guided Missile, Holy Grenade all show "101" from the engine's ammo display.

**Root cause:** These mods were missing `SetString("game.tool.TOOLID.ammo.display", "")` in server.init.

**Fix:** Added `SetString("game.tool.TOOLID.ammo.display", "")` to all 7 mods.

**Date fixed:** 2026-03-17

---

## Issue #24: Options menus have overlapping text and oversized font

**Symptom:** The options menu text overlaps and font is too large. Layout not matching Black Hole properly.

**Fix:** Reduced option label font from 26→22, title from 26→24, button font from 18→20 (with larger 90x30 buttons), increased gap between buttons and options from 30→40px, reduced option spacing from 60→50px. Adjusted box heights. Also increased toggle button hit areas from 20x20→30x25. Applied to all 6 mods: Mjölner, Scorpion, Hook Shotgun, M1 Garand, Exploding Star, Laser Cutter.

**Date fixed:** 2026-03-17

---

## Issue #25: Hook Shotgun grapple still fires into ground

**Symptom:** Despite fix #17 (sending aim from client), the hook still goes to the wrong spot.

**Root cause:** Two bugs:
1. `server.throwHook` computed `startPos` from the SERVER's `GetPlayerEyeTransform(p)` but used the CLIENT's aim position. Any latency mismatch between server/client eye transforms skewed the direction vector downward.
2. Client never mirrored hook projectile physics — `data.line.pos` stayed at `Vec(0,0,0)` so the hook rope visual was wrong, and `data.hookbody`/`data.localhookpos` were only set server-side so the HOOKED state visual couldn't work.

**Fix:**
1. Client now sends both `startPos` and `aimpos` to `server.throwHook(p, sx,sy,sz, ax,ay,az)` so the geometry is self-consistent.
2. Client mirrors the hook projectile physics (raycast each tick, detect hit, set hookbody/localhookpos) for visual rendering.
3. Client initializes `data.line.pos` and `data.line.predictedBulletVelocity` locally when throwing.

**RULE: When sending aim data from client to server, always send ALL geometry from the same frame on the client. Never mix client aim with server eye transform.**

**Date fixed:** 2026-03-17

---

## Issue #26: Guided Missile missing keybind hints and ammo HUD

**Symptom:** No keybind hints or status display.

**Fix:** Added bottom-left keybind hints (LMB launch/detonate, RMB detach, Scroll detach, Space boost, R toggle piercing). Added bottom-center status indicator (READY/GUIDING/DETACHED with color coding). Kept PIERCING mode indicator.

**Date fixed:** 2026-03-17

---

## Issue #27: Holy Grenade HUD layout needs reorganization

**Symptom:** Fuse info and keybinds are where ammo count should be. Need to move fuse info to left side and add proper ammo counter.

**Fix:** Moved keybind hints (LMB throw, X increase fuse, Z decrease fuse) to bottom-left matching standard layout. Fuse timer displayed bottom-center in yellow with larger font.

**Date fixed:** 2026-03-17

---

## Issue #28: Bee Gun needs damage, less smoke, time limit, ammo count

**Symptom:** Bees bounce but do no damage. Too much smoke. Bees never despawn. No ammo counter (infinite).

**Root cause:**
1. `MakeHole` only called in `holeMode` — normal bees did zero damage.
2. `SpawnParticle("smoke")` called every frame per bee with `smokeTime=2` seconds — massive smoke buildup.
3. `shell.freeTimer = 0` reset on EVERY bounce — since bees bounce constantly, they never reached the 20s timeout.
4. No ammo system — completely infinite.

**Fix:**
1. Normal bees now do small damage on impact (`MakeHole(0.1, 0.1, 0.1)`), hungry mode does larger (`MakeHole(0.2, 0.2, 0.2)`).
2. Smoke throttled: only spawns every 0.3s per bee (uses smokeTime as countdown timer), particle lifetime reduced to 0.3s.
3. `freeTimer` no longer resets on bounce — accumulates continuously. Lifetime reduced from 20s to 10s.
4. Heat/cooldown system: each shot adds 12 heat (max 100), heat decays at 25/s when idle. At 100 heat gun overheats, can't fire until cooling to 30. HUD shows heat bar (green→yellow→red), active bee count, OVERHEATED warning, and mode indicator.

**Date fixed:** 2026-03-17

---

## Issue #29: Keybind remapping in options menus

**Symptom:** Players can't change mod keybinds — all keys are hardcoded.

**Fix:** Implemented a reusable keybind remapping system. Each mod stores bindings in `savegame.mod.keys.ACTIONID`. The O-key options menu shows each action's current key with a [Rebind] button. Clicking Rebind enters capture mode — next keypress (from `BINDABLE_KEYS` list) saves the new binding. ESC cancels. [Defaults] resets all.

**Architecture changes:**
- Moved raw key input from server (`InputPressed("key", p)` — broken per Issue #7) to client-only (`InputPressed(key)` without player param) — the correct v2 pattern
- Added `ServerCall` handler functions for each action (e.g., `server.toggleHungry`, `server.fuseUp`)
- Input suppressed during rebind mode (`not rebindingAction` guard)
- Keybind hints on HUD now show actual bindings via `keyDisplayName()`

**Mods implemented (5):**
1. Bee Gun (2425682439) — R/E/C → hungry mode, kamikaze, kill all
2. Black Hole (2401574819) — C → push/detonate
3. Guided Missile (2401872753) — R/RMB → piercing, detach
4. Holy Grenade (2401873154) — X/Z → fuse up/down
5. Mjölner (2401593417) — RMB/Space → heavy strike, boost jump

**Remaining mods:** 81 mods have custom keybinds (mostly just R for reload). The pattern is established and can be applied to additional mods as needed. Priority candidates: Attack Drone (M/N/R), AWP (C/R), Multi Grenade Launcher (C/R/X/Z).

**Date fixed:** 2026-03-17

---

## Issue #30: Magic Bag picks up objects but can't throw — ammo stays at 0

**Symptom:** LMB picks up objects (they disappear), but RMB charge/throw never works and the HUD counter stays at 0.

**Root cause:** Server/client count desync. `PickItem()` runs on the server and increments `data.count`, but the client's `data.count` was never updated. The client checks `data.count >= 2` before allowing RMB throw — always fails.

**Fix:** Server calls `ClientCall(p, "client.syncCount", data.count)` after every pickup and throw. Client has a `client.syncCount(count)` handler that updates the local count.

**RULE: When the server modifies state that the client needs for input gating or HUD, use `ClientCall` to sync it.**

**Date fixed:** 2026-03-17

---

## Issue #31: Options menu sliders don't affect gameplay

**Symptom:** Changing slider values has no effect on tool behavior (e.g., Exploding Star fuse time).

**Root cause:** Sliders write to `savegame.mod.*` and set client `data.*`, but the server's `data.*` was only loaded once during `PlayersAdded`. Server never sees updated values.

**Fix:** Adopted Black Hole's `getOptions()` pattern — reads fresh from savegame each tick. Applied to: Exploding Star, Mjölner, Scorpion, Hook Shotgun, M1 Garand, Laser Cutter.

**RULE: For options affecting server-side gameplay, use `getOptions()` savegame reads — never cache in `data.*` on the server.**

**Date fixed:** 2026-03-17

---

## Issue #32: Tool fires while options menu is open

**Symptom:** LMB clicks in the options menu also fire the tool. Even after client-side guard was added, the server still processed the input and fired invisible projectiles.

**Root cause:** `UiMakeInteractive()` enables cursor but doesn't suppress game input. Both server AND client independently check `InputPressed("usetool", p)`. Guarding only the client stops visuals/sounds but the server still fires, creates projectiles, does damage.

**Fix (two-part):**
1. Added `not data.optionsOpen` guard to ALL `usetool`/`InputDown("usetool")` checks — both client AND server side
2. Added `server.setOptionsOpen(p, open)` handler to every mod. Client calls `ServerCall("server.setOptionsOpen", GetLocalPlayer(), data.optionsOpen)` when O is pressed, syncing the menu state to the server.

**Applied to:** All 10 mods with options menus (Black Hole, Bee Gun, Guided Missile, Holy Grenade, Mjölner, Scorpion, Hook Shotgun, M1 Garand, Exploding Star, Laser Cutter).

**RULE: Options menu state MUST be synced to server via `server.setOptionsOpen` ServerCall. Guard `usetool` on BOTH server and client with `not data.optionsOpen`. Client-only guards are insufficient — the server processes input independently.**

**Date fixed:** 2026-03-17

---

## Issue #33: 12 unlimitedammo mods had no options menu UI

**Symptom:** Mods reading `savegame.mod.unlimitedammo` had no in-game UI to toggle the setting — players had to edit savegame files manually.

**Root cause:** Options menus were only added to 10 mods with complex settings (Black Hole, Bee Gun, etc). Simple gun mods with just an `unlimitedammo` toggle were skipped.

**Fix:** Added O-key options menu to 12 mods following the Black Hole pattern:
1. `optionsOpen = false` in `createPlayerData()`
2. `server.setOptionsOpen()` for server sync
3. `and not data.optionsOpen` on all `usetool` checks (server + client)
4. O-key toggle in `client.tickPlayer` (local player only)
5. Options UI in `client.draw()` with toggle button and `[O] Options` hint

**Applied to:** P90, 500_Magnum, AWP, AK-47 (+realisticdamage toggle), Desert_Eagle, Dual_Berettas, M249, M4A1, Multi_Grenade_Launcher, Nova_Shotgun, SCAR-20, SG553.

**Skipped:** .500_Magnum (still v1 structure, needs full rewrite first).

**RULE: Every mod with `savegame.mod.*` keys must have an O-key options menu so players can configure settings in-game. Follow the 5-point integration pattern above.**

**Date fixed:** 2026-03-17

---

## Issue #34: 7 rich-settings mods missing or incomplete options menus

**Symptom:** Mods with multiple savegame settings (sliders, toggles, modes) either had no options menu, had menus without server sync, or were missing OptionsGuard on usetool.

**Root cause:** These mods were more complex than the simple unlimitedammo toggles — each needed a custom menu layout with setting-specific UI.

**Fix:** Added or completed options menus for all 7:
- **C4:** Added O-key menu with explosion size +/- buttons and timer delay cycle. Moved timer cycling from O key into menu. Added savegame persistence for both settings.
- **AC130_Airstrike_MP:** Added O-key menu with No Cooldown toggle.
- **Lava_Gun:** Added O-key menu with Big/Small fire mode toggle. Server sync already present.
- **Multiple_Grenade_Launcher:** Added O-key menu with 3 toggles (unlimitedammo, norecoil, noreticle). Server sync already present.
- **High_Tech_Drone:** Already had full settings panel on E key. Added `server.setSettingsOpen()` for sync, added `not data.settingsOpen` guards on all usetool checks, added ServerCall on close button.
- **Vacuum_Cleaner:** Already had slider UI on R key. Added `server.setOptionsOpen()` for sync, changed R→O key for consistency, added `not pd.optionsopen` guards on usetool/rmb checks.
- **Revengeance_Katana:** Already had menu. Added missing `not data.optionsOpen` guard on client usetool check.

**Also fixed:** MISSING-OPTIONS-SYNC on 5 mods (Lava_Gun, Lightning_Gun, M2A1_Flamethrower, Welding_Tool, Winch) — all were missing `server.setOptionsOpen()` function, causing server to process usetool while client showed menu.

**RULE: Mods with existing settings panels must ALSO have server sync (`server.setOptionsOpen` or `server.setSettingsOpen`) and usetool guards on BOTH server and client. A menu without sync is worse than no menu — it gives false confidence that actions are blocked.**

**Date fixed:** 2026-03-17

## Issue #35: 16 mods with non-clickable options menus (missing UiMakeInteractive)

**Symptom:** Options menu panels render visually when pressing O, but all buttons (Enable/Disable, Close) cannot be clicked. The menu appears but is completely non-functional.

**Root cause:** `UiMakeInteractive()` was never called before drawing interactive UI elements. Without this call, `UiTextButton()` and `UiSlider()` draw visually but ignore mouse input. This was a systematic omission in the v2 conversion template.

**Fix:** Added `UiMakeInteractive()` as the first call inside each `if data.optionsOpen then` block, before `UiPush()`. Applied to 16 mods: 500_Magnum, AC130_Airstrike_MP, AK-47, AWP, C4, Desert_Eagle, Dual_Berettas, Lava_Gun, M249, M4A1, Multi_Grenade_Launcher, Multiple_Grenade_Launcher, Nova_Shotgun, P90, SCAR-20, SG553.

**RULE: Any in-game menu with clickable elements (UiTextButton, UiSlider, etc.) MUST call `UiMakeInteractive()` before any `UiPush()`. Without it, buttons render but don't respond to clicks.**

**Date fixed:** 2026-03-17

---

## Issue #36: 4 melee/projectile mods couldn't damage players in multiplayer

**Symptom:** Dragonslayer, HADOUKEN, Revengeance_Katana, and Scorpion could destroy voxels but never damaged other players in PvP.

**Root cause:** All 4 mods used `MakeHole()` for damage. `MakeHole()` only affects voxels — it cannot damage players. The v2 API requires `QueryShot()` + `ApplyPlayerDamage()` (or `Shoot()`) to register player hits.

**Fix:** Added `QueryShot()` + `ApplyPlayerDamage()` to each mod's attack path:
- **Dragonslayer:** QueryShot on swing path, radius 1.0
- **HADOUKEN:** QueryShot on energy ball projectile movement path, radius 0.5
- **Revengeance_Katana:** QueryShot on both slash arms with per-slash hit tracking
- **Scorpion:** QueryShot on both punch hit and hook projectile

MakeHole retained alongside QueryShot for voxel destruction.

**RULE: Melee/projectile weapons that need to damage players MUST use `QueryShot()` + `ApplyPlayerDamage()`. `MakeHole()` is voxel-only and cannot hurt players.**

**Date fixed:** 2026-03-17

---

## Issue #37: 3 gun mods missing options menus (Lightning_Gun, M2A1_Flamethrower, Minigun)

**Symptom:** Lightning_Gun, M2A1_Flamethrower, and Minigun had configurable settings but no in-game UI to change them.

**Root cause:** These mods were missed during the earlier options menu rollout (Issues #33-34).

**Fix:** Added O-key options menus following the standard pattern:
- **Lightning_Gun:** 2 toggles — Disable Fires (skips SpawnFire), Disable Debris Clear (skips debris deletion)
- **M2A1_Flamethrower:** Unlimited Ammo toggle
- **Minigun:** No Recoil toggle

All include: `optionsOpen` in `createPlayerData()`, `server.setOptionsOpen()` for server sync, `not data.optionsOpen` guards on usetool (server + client), `UiMakeInteractive()`, close button, `[O] Options` keybind hint.

**Date fixed:** 2026-03-17

---

## Milestone: Zero X Flags — Full Feature Compliance (2026-03-17)

**Achievement:** All 50 mods pass audit with zero X (wrong-pattern) flags. Tier 1 lint: 0 findings across all 50 mods.

**What was resolved to reach this point:**
- 14 MANUAL-AIM flags triaged: 4 migrated to GetPlayerAimInfo (Airstrike_Arsenal, Lava_Gun, Lightning_Gun, HADOUKEN, M2A1_Flamethrower), 11 suppressed as valid non-aim QueryRaycast uses via `@audit-ok`
- 1 MISSING-SHOOT flag resolved (Acid_Gun — particle physics, not standard gun pattern)
- OptionsMenu + OptionsGuard added to 30+ mods across Issues #33-35, #37
- 2 audit tool bugs fixed (AmmoDisplay regex for hyphenated IDs, OptionsGuard early-return detection)

**Remaining polish (no X flags, all optional):**
- OptionsMenu for utility mods without savegame settings (Swap_Button, Thruster_Tool, Asteroid_Strike, Magic_Bag)
- KeybindRemap in 45/50 mods (only 5 have it — low priority)
- fix.py handle_gt false positive (T23)

---

## Issue #38: .500_Magnum and 500_Magnum tool ID conflict

**Symptom:** Both `.500_Magnum/main.lua` and `500_Magnum/main.lua` register tool ID `"500magnum"`. This causes undefined behavior — the engine may load either mod's tool depending on order, or one may shadow the other.

**Root cause:** `.500_Magnum` is the original v1-style mod (global state, no `players` table, no MP support). `500_Magnum` is the proper v2 rewrite with full MP features. Both coexist in the mods directory.

**Fix:** Remove `.500_Magnum` directory. The v2 `500_Magnum` is the correct version with all features (OptionsMenu, OptionsGuard, AmmoPickup, AimInfo, Shoot, KeybindHints, AmmoDisplay).

**Status:** AWAITING USER APPROVAL — do not delete without confirmation.

**RULE: Never have two mods registering the same tool ID. When a v2 rewrite replaces a v1 mod, remove the v1 directory.**

**Date found:** 2026-03-17

---

## Issue #39: SetPlayerHealth swapped argument order

**Symptom:** `SetPlayerHealth(p, 1)` silently sets the wrong player to the wrong health. In MP, this could heal/kill arbitrary players.

**Root cause:** The correct signature is `SetPlayerHealth(health, player)` — health first, player second. The intuitive `(player, value)` order is wrong. Dragonslayer and Lightkatana both had this bug.

**Fix:** Swapped to `SetPlayerHealth(1, p)`. Added new Tier 1 lint rule `HEALTH-ARG-ORDER` to detect `SetPlayerHealth(p, number)` pattern.

**RULE: `SetPlayerHealth(health, player)` — health value FIRST, player ID SECOND. The reverse silently works but affects the wrong player.**

**Date fixed:** 2026-03-17

---

## Issue #40: Acid_Gun couldn't damage players

**Symptom:** Acid particles destroyed voxels but never damaged other players in multiplayer.

**Root cause:** Acid_Gun used only MakeHole for corrosion damage, which is voxel-only. Originally rejected as "particle physics, not applicable" (T20), but api_surgeon found a viable approach.

**Fix:** Added QueryShot + ApplyPlayerDamage to the corrosion loop. Acid particles now damage players within 0.4m radius, throttled to ~1/sec. Damage: 0.15 * corrosionPower * hitFactor.

**Date fixed:** 2026-03-17

---

## Issue #41: M249 and M4A1 Lua compile errors (extra `end`)

**Symptom:** Game log shows compile errors for M249 and M4A1 mods.

**Root cause:** Extra dangling `end` in client.draw() after the options menu early-return block. No matching block opener.

**Fix:** Removed extra `end`, fixed indentation. Both mods now lint clean.

**Date fixed:** 2026-03-17

---

## Issue #42: V2 API reference had wrong argument order for SetPlayer* functions

**Symptom:** Documentation showed `SetPlayerTransform(playerId, transform)` but actual API is `SetPlayerTransform(transform, playerId)`.

**Root cause:** 5 SetPlayer* functions in TEARDOWN_V2_API_REFERENCE.md had swapped argument order: SetPlayerTransform, SetPlayerTransformWithPitch, SetPlayerVelocity, SetPlayerGroundVelocity, SetPlayerHealth.

**Fix:** Corrected all 5 function signatures. The v2 API consistently puts player param last.

**RULE: In v2 API, player param is ALWAYS the last argument for SetPlayer* functions (e.g., `SetPlayerHealth(health, player)`, `SetPlayerTransform(transform, player)`).**

**Date fixed:** 2026-03-17

---

## Issue #43: Multiplayer desync and performance — 6 root causes

**Symptom:** User testing in multiplayer revealed massive desync — projectiles flying in wrong directions, actions only working for host, lag spikes with multiple players.

**Root causes identified (6 patterns across 30+ mods):**
1. Client-side projectile physics running for ALL players (should be local only)
2. Per-tick ServerCall/ClientCall with position data (should use registry sync)
3. FindShapes/QueryAabb every frame per player (should throttle to ≤4Hz)
4. Server-side ~~PlaySound~~/SpawnParticle (wasted CPU, effects are client-only) **[CORRECTED 2026-03-21: PlaySound on server actually auto-syncs — see BASE_GAME_MP_PATTERNS.md Pattern 10. Only SpawnParticle/PointLight/SetShapeEmissiveScale are truly client-only.]**
5. Raw key InputPressed in server code (fails silently for non-host players)
6. Client-side QueryShot for damage (should be server-side for authoritative hit detection)

**Fix:** Full audit of all 63 mods against all 6 patterns. See `docs/MP_DESYNC_PATTERNS.md` for detailed fix patterns and code examples.

**Already fixed (before sprint):** Ion_Cannon_Beacon (full rewrite), Laser_Cutter, Object_Possession, Airstrike_Arsenal, Remote_Explosives, 14 mods with dual projectile guards.

**Sprint results (2026-03-18):**
- API Surgeon: Attack_Drone isLocal guard on client projectile loop (RC1). 14 hitscan guns audited — 6 had server-side SpawnParticle removed (RC4): 500_Magnum, AK-47, AWP, Desert_Eagle, Dual_Berettas, Dual_Miniguns. 8 already clean.
- Mod Converter: 16 melee/utility/special mods audited. 1 fix: Guided_Missile client physics gated with isLocal (RC1) + camerax player param removed. 15 already clean.
- QA Lead: Fixed Ion_Cannon_Beacon (full rewrite), Laser_Cutter, Object_Possession before sprint.

**RULES:**
- Gate client projectile physics with `IsPlayerLocal(p)` (CLAUDE.md Rule 26)
- Use registry sync for continuous state, RPC for events only (Rule 27)
- Throttle FindShapes/QueryAabb to ≤4Hz (Rule 28)
- ~~PlaySound~~/SpawnParticle are client-only (Rule 29) **[CORRECTED: PlaySound on server auto-syncs — only SpawnParticle/PointLight/SetShapeEmissiveScale are client-only]**
- QueryShot + ApplyPlayerDamage must run on server (Rule 30)

**Date found:** 2026-03-18

---

## Issue #44: QueryAabb per-tick in 3 mods (RC3)

**Symptom:** FPS drops with multiple players using Vacuum_Cleaner, Black_Hole, or HADOUKEN.

**Root cause:** `QueryAabbBodies`/`QueryAabbShapes` called every frame in `server.tickPlayer` for physics push effects. O(n*m) per player per tick.

**Fix:** Added 0.25s throttle timer (≤4Hz) with cached results. Forces applied every frame from cache. `IsHandleValid()` guard on cached handles prevents stale-handle crashes.

**RULE: #28 — Throttle FindShapes/QueryAabb to ≤4Hz. Cache results, apply forces from cache, guard with IsHandleValid().**

**Date fixed:** 2026-03-18

---

## Issue #45: Server-side PlaySound/SpawnParticle in AC130_Airstrike_MP (RC4)

**Symptom:** Wasted CPU on server, effects only visible to host player.

**Root cause:** `server.handleProjectileHit` called `PlaySound`/`SpawnParticle` directly (9+1 calls). `server.updateProjectile` had water collision effects on server.

**Fix:** Added `hitPos`/`hitDir` to shared projectile table for client impact detection. Added `client.handleImpactEffects()` — detects projectile deactivation, plays correct sounds+particles per ammo type. Server handles only authoritative effects (MakeHole, Explosion, SpawnFire).

**RULE: #29 — ~~PlaySound~~/SpawnParticle are CLIENT-ONLY. Use shared state or ClientCall to trigger effects from server events.** **[CORRECTED 2026-03-21: PlaySound() on server auto-syncs to all clients (BASE_GAME_MP_PATTERNS.md Pattern 10). Only SpawnParticle/PointLight/SetShapeEmissiveScale are truly client-only. The AC130 fix was not wrong (client-side PlaySound also works) but was unnecessary for PlaySound specifically.]**

**Date fixed:** 2026-03-18

---

## Issue #46: gun_v2_generator.py produced non-compliant code

**Symptom:** Generated code had no player damage, wrong aim pattern, duplicate ammo decrement.

**Root cause:** Manual `QueryRaycast` aim (not `GetPlayerAimInfo`), no `QueryShot`+`ApplyPlayerDamage` (no player damage), duplicate ammo decrement on client+server, missing default keybind hints, `InputPressed("r", p)` on server for reload.

**Fix:** Replaced `GetAimPos` with `GetPlayerAimInfo`, added `QueryShot`+`ApplyPlayerDamage` to `ProjectileOperations`, removed client ammo decrement, added default keybind hints, reload via ServerCall, added OptionsMenu/OptionsGuard/AmmoPickup.

**RULES: #11 (GetPlayerAimInfo), #13/#30 (QueryShot on server), #8/#9 (server/client split), #10 (no raw keys with player param)**

**Date fixed:** 2026-03-18

---

## Issue #47: QueryShot player=0 causes phantom host damage

**Symptom:** Tripmine beam hitting debris/terrain caused the host player to take damage from anywhere on the map, even when no player was near the beam.

**Root cause:** `QueryShot()` returns `player=0` when it hits a non-player object (shape, terrain, debris). On the server, player ID 0 maps to the host. Calling `ApplyPlayerDamage(0, damage, ...)` therefore silently damages the host regardless of position.

**Fix:** Guard all `ApplyPlayerDamage` calls with `player ~= 0` check:
```lua
local hit, dist, shape, player, hitFactor, normal = QueryShot(pos, dir, len, radius, p)
if hit and player ~= 0 then
    ApplyPlayerDamage(player, damage, "toolid", p)
end
```

**Applied to:** Tripmine (original fix), then 34 more mods via QA Lead systemic sweep (2026-03-18): 7 manual fixes (Sith_Saber, Final_Flash, Dual_Miniguns, Dual_Berettas, Guided_Missile, Hook_Shotgun, Exploding_Star), then 27 auto-fixed via `python -m tools.fix --only queryshot-guard` (500_Magnum, AC130_Airstrike_MP, AK-47, AWP, Acid_Gun, Attack_Drone, Bee_Gun, Charge_Shotgun, Desert_Eagle, Dragonslayer, HADOUKEN, Laser_Cutter, Lava_Gun, Lightning_Gun, M1_Garand, M249, M2A1_Flamethrower, M4A1, MEGAGUN, Minigun, Nova_Shotgun, P90, RMW_RPG7, RMW_SMAW, SCAR-20, SG553, Scorpion). **Additional fixes (2026-03-19):** DAM_Helis (2x in rpg_projectile.lua `if shotPlayer then` → `~= 0`), Armour_Framework_MP (4x in TankMain.lua `if shotPlayer/fragPlayer then` → `~= 0`).

**Tooling added:** Lint rule `QUERYSHOT-PLAYER-GUARD` (Tier 1, tools/lint.py) detects the pattern. Auto-fix `queryshot-guard` (tools/fix.py) patches it deterministically.

**Investigation (API Surgeon):** The 5-param form `QueryShot(pos, dir, dist, radius, attacker_p)` — used by all weapon mods — excludes the attacker and returns `nil` for non-player hits. However, `if player then` is WRONG because Lua treats `0` as truthy. Must use `if player ~= 0 then`. The 3-param form `QueryShot(origin, dir, dist)` — used only by Tripmine — has no attacker exclusion and can return `player=0`. Both forms require `~= 0` guard.

**Tooling fix (2026-03-19):** gun_v2_generator.py also had this bug — generated code used `if qplayer then` instead of `if qplayer ~= 0 then`. Any future generated mod would have phantom host damage. Fixed + 14 regression tests added (tests/test_generator.py).

**RULE: ALWAYS use `player ~= 0` after QueryShot, regardless of param count. `if player then` is WRONG — Lua 0 is truthy. The 5-param form may return nil or 0; the 3-param form returns 0 for non-player hits. `player ~= 0` is universally safe.**

**Date fixed:** 2026-03-18

---

## Issue #48: Tripmine ApplyPlayerDamage missing attacker param

**Symptom:** `ApplyPlayerDamage(player, 1, "loc@DAMAGE_CAUSE_EXPLOSION")` in Tripmine used only 3 params. Missing 4th param (attackerPlayer) means kill feed shows no attacker for tripmine kills.

**Root cause:** The correct signature is `ApplyPlayerDamage(targetPlayer, damage, toolId, attackerPlayer)`. Tripmine is an environmental hazard with no tracked placer, so attacker was simply omitted.

**Fix:** Added `0` as the 4th param (no attacker / environment kill):
```lua
ApplyPlayerDamage(player, 1, "loc@DAMAGE_CAUSE_EXPLOSION", 0)
```

**Applied to:** Tripmine (`script/tripmine.lua:46`)

**RULE: Always use the full 4-param `ApplyPlayerDamage(target, damage, toolId, attacker)`. For environmental hazards without a tracked placer, pass `0` as attacker.**

**Date fixed:** 2026-03-18

---

## Issue #49: Remote_Explosives FindShapes per-frame spam

**Symptom:** Remote_Explosives called `FindShapes()` twice in `server.tick()` every frame (~120 calls/sec), causing unnecessary server load and potential network overhead in multiplayer.

**Root cause:** Shape lookups for explosive proximity detection ran every tick instead of being cached and throttled.

**Fix:** Throttled FindShapes calls to ≤4Hz with a 0.25s shape cache. Cache refreshes periodically; invalidates on detonation. Added `IsHandleValid` checks for stale handles.

**Applied to:** Remote_Explosives

**RULE: Throttle `FindShapes()`/`QueryAabb()` to ≤4Hz — cache results and refresh periodically. See CLAUDE.md rule 28.**

**Date fixed:** 2026-03-18

---

## Issue #50: Minigun invisible impact smoke in multiplayer

**Symptom:** Minigun bullet impacts produced no visible smoke/particle effects for other players. Impact was invisible despite hitting surfaces.

**Root cause:** `SpawnParticle` was called on the server for impact effects. `SpawnParticle` is CLIENT-ONLY — server calls are silently ignored, so only the host saw effects.

**Fix:** Replaced server-side `SpawnParticle` with `ClientCall` to `client.onProjectileHit`, which spawns the particle effect on all clients. Also removed dead `DrawLine` tracer code.

**Applied to:** Minigun, Hook_Shotgun, M1_Garand, M249, M4A1, Nova_Shotgun, P90, SCAR-20, SG553 (9 mods total)

**RULE: SpawnParticle/~~PlaySound~~ are CLIENT-ONLY (rule 29). For multiplayer-visible effects triggered by server events, use `ClientCall(0, "client.effectFunc", ...)` to broadcast to all clients.** **[CORRECTED 2026-03-21: PlaySound() on server auto-syncs. Only SpawnParticle is truly client-only here. The ClientCall pattern for SpawnParticle is correct; for PlaySound, direct server-side call is simpler.]**

**Date fixed:** 2026-03-18

---

## Issue #51: ServerCall does NOT auto-inject player ID

**Symptom:** Artillery_Barrage_RELOADED server functions received `nil` for player ID, causing errors when trying to use player-specific state.

**Root cause:** The Teardown engine passes ServerCall parameters exactly as given. Server functions receive `(p, ...)` where `p` must be explicitly sent by the client — it is NOT auto-injected by the engine. The client must always pass the player ID as the first parameter.

**Fix:** Always pass player ID as first param: `ServerCall("server.fn", p, arg1, arg2)`. Fixed 5 call sites in Artillery_Barrage_RELOADED.

**Verified:** Official minigun mod confirms the pattern: `ServerCall("server.setOptionsOpen", p, data.optionsOpen)`.

**Expanded scope (systemic sweep — COMPLETE):** Mod Converter swept all 122 mods. Fixed setOptionsOpen across ALL mods (batch sed fix), 9 framework gun clones (onShootSemi, onReload, onSelectFire, onMelee, onShootGrenade), Telekinesis (onInputUpdate + 9 onAction calls), Portal_Gun (onShootOrange, onResetPortals), Magnetizer_V2, Spells. Verified ~10 remaining no-p ServerCalls are legitimate (server funcs don't take p: DeleteAllBullets, createStormCloudGroupAbove, collapseShape, etc.). Result: 122 mods, 0 tier 1 findings. All ServerCall patterns now match official minigun reference.

**RULE: `ServerCall("server.fn", p, ...)` — player ID `p` is REQUIRED as the first param. The engine does NOT auto-inject it. Server functions receive exactly what the client sends.**

**Date fixed:** 2026-03-18

---

## Issue #52: Hurricanes_and_Blizzards raw key bugs (community v2 mod)

**Symptom:** Hurricanes_and_Blizzards (workshop 3669298473, author: Riv) was already v2 from workshop but had 6 FAIL-level raw key bugs causing silent input failures in multiplayer.

**Root cause:** UI textbox code used `InputDown("shift", 0)`, `InputPressed("lmb", 0)`, `InputPressed("rmb", 0)` — raw keys with player param. Raw key names do NOT accept a player parameter; the extra `0` is silently ignored, causing the input to fail for non-host players.

**Fix:** Removed the player parameter from all 6 raw key calls. Also annotated 2 false-positive PER-TICK-RPC and 1 false-positive HANDLE-GT-ZERO. 4 remaining INFO findings are weather raycasts (not weapons), acceptable.

**Applied to:** Hurricanes_and_Blizzards (mod #123)

**RULE: Raw key names ("rmb", "lmb", "shift", etc.) NEVER take a player parameter. Use `InputPressed("rmb")` with `isLocal` check + ServerCall. (Existing CLAUDE.md Rule 10)**

**Date fixed:** 2026-03-18

---

## Issue #53: SetShapeEmissiveScale server-only = host-only visual

**Symptom:** C4 explosive glow animation (SetShapeEmissiveScale pulsing) only visible to host player, invisible to other clients.

**Root cause:** `SetShapeEmissiveScale` was called in `server.tick`. Like `PlaySound`/`SpawnParticle`, shape visual functions only affect the local machine. Server-side calls only render for the host — other clients never see the effect.

**Fix:** Move `SetShapeEmissiveScale` calls from `server.tick` to `client.tick` so all players see the glow animation.

**Applied to:** Remote_Explosives (SetShapeEmissiveScale moved from server.tick to client.tick, also removed unused server shape cache, throttled IsShapeBroken to 4Hz). Originally found in Multiplayer_C4 (duplicate — see Issue #54). **Additional (2026-03-19):** Gwel_Mall (3 entity scripts: substation.lua, sampleCtrl1.lua, firesystem.lua — exit sign lighting, gate buttons, power-cut effects), PPAN_Vehicle_Pack (popupHeadlight_MP.lua — detached headlights), The_Office_US (lamp.lua — lamp shade glow).

**RULE: `SetShapeEmissiveScale` is effectively CLIENT-ONLY for visual effects. Expand Rule 29: ~~PlaySound~~/SpawnParticle/SetShapeEmissiveScale are client-only — never call on server for visual effects.** **[CORRECTED 2026-03-21: PlaySound() on server auto-syncs — it is NOT client-only. Corrected Rule 29 = SpawnParticle/PointLight/SetShapeEmissiveScale are client-only. PlaySound on server is the CORRECT base game pattern.]**

**Date fixed:** 2026-03-18

---

## Issue #54: Multiplayer_C4 and Remote_Explosives tool ID conflict

**Symptom:** Two mod directories (`Multiplayer_C4/` and `Remote_Explosives/`) both register tool ID `"slippy_remote_explosive"`. Identical info.txt (author: Slippy, workshop 3621598329). Same Issue #38 pattern.

**Root cause:** `Remote_Explosives` is our Batch 4 v2 conversion of this workshop mod. `Multiplayer_C4` was freshly installed from the same workshop item under its actual name. Two copies of the same mod coexist.

**Fix:** Delete `Multiplayer_C4/` — `Remote_Explosives` is the superior version (0 lint findings vs 4, more thorough polishing including FindShapes throttling). Mod count returns to 123.

**RULE: Before installing a workshop mod, verify its workshop ID isn't already in MASTER_MOD_LIST.md. (Reaffirms Issue #38 rule)**

**Status:** RESOLVED — QA Lead deleted Multiplayer_C4. Remote_Explosives retained. 123 mods.

**Date fixed:** 2026-03-18

---

## Issue #55: Tripmine GetPlayerHealth(player ~= 0) boolean-as-player-ID

**Symptom:** Tripmine tripwire laser health checks could malfunction — `GetPlayerHealth(player ~= 0)` was passing boolean `true` instead of the actual player ID, potentially returning incorrect health values.

**Root cause:** At `tripmine.lua:45`, the expression `GetPlayerHealth(player ~= 0)` evaluates the comparison first, producing `true` (since `player` is nonzero), then passes `true` to `GetPlayerHealth`. The `player ~= 0` guard was already correct on the outer `if` at line 44, so the inner call just needed the raw variable.

**Fix:** Changed `GetPlayerHealth(player ~= 0)` to `GetPlayerHealth(player)`. The `~= 0` guard is on the enclosing `if` block, not inside the function call.

**Applied to:** Tripmine (`script/tripmine.lua:45`)

**RULE: Never embed comparison expressions inside function calls as arguments. `fn(var ~= 0)` passes a boolean, not the variable. Use the guard in an `if` block, then pass the variable directly: `if var ~= 0 then fn(var) end`.**

**Date fixed:** 2026-03-18

---

## Issue #56: Explosion() does NOT damage players in v2 MP

**Symptom:** Explosive weapons (C4, grenades, missiles, orbital strikes) create spectacular explosions that destroy terrain and push objects but deal ZERO health damage to other players in multiplayer. Weapons appear to work (terrain destruction, physics impulse) but opponents are unharmed.

**Root cause:** `Explosion(pos, radius)` is auto-replicated deterministic destruction — it destroys voxels and applies physics impulse to bodies, but does NOT call player health damage. This parallels `MakeHole()` (Issue #4). Player health damage requires explicit `ApplyPlayerDamage()` or `Shoot()` calls. In singleplayer, explosion proximity damage was handled by the engine differently; in v2 MP, it must be explicit.

**Fix pattern:** After every `Explosion()` call in a weapon context, add distance-based player damage:
```lua
Explosion(pos, radius)
local damageRadius = radius * 3
for target in Players() do
    if target ~= attacker then
        local dist = VecLength(VecSub(pos, GetPlayerPos(target)))
        if dist < damageRadius then
            ApplyPlayerDamage(target, 1.0 * (1.0 - dist / damageRadius), "toolId", attacker)
        end
    end
end
```

**Applied to (23 mods):** Predator_Missile_MP, C4, Holy_Grenade, Mjolner, Multi_Grenade_Launcher, Multiple_Grenade_Launcher (4 Explosion() calls: HE, Cluster initial+continuation, Frag — added applyExplosionDamage helper with "Launcher" toolId), Asteroid_Strike, Ion_Cannon_Beacon, Spells (lightning spell), AK105, AK12, AK74, Dragunov_SVU, G17, G36K, Kriss_Vector, M4A1, SCAR, Saiga12 (all underslung grenade launcher), Airstrike_Arsenal (MOAB + World Buster modes), Bunker_Buster_MP (entity script owner propagation), Bombard (environmental damage), Explosive_Pack (C4 + Landmine — added applyExplosionDamage helper with distance falloff)

**Fixed (2026-03-19 — previously deferred):** Bunker_Buster_MP (owner player ID propagated through shared.spawnHandleTargets/spawnTargets into warhead.lua + cluster.lua, full kill attribution with toolId "bunkerbustermissile"), Bombard (environmental damage attacker=0 on cannonball Explosion in ball.lua — map hazard, not direct weapon)

**Not applicable (3 — non-weapon tools):** CnC_Weather_Machine, Drivable_Plane, Object_Possession

**Remaining (not fixable as focused API swaps):** 8 vehicle entity scripts in 4 mods (Armour_Framework_MP, Legacy_Tank_MP, Dumb_Stupid_Fast_Cars, MrRandoms_Vehicles) use hybrid v1/v2 callbacks — needs dedicated restructuring. Also: Koenigsegg_Agera_MP flying car (visual effect), Minecraft_Building_Tool firecharge (minor). 8 other files confirmed disabled in MP (no #version 2 header): DAM_Helis aircraft weapons, Multiplayer_Spawnable_Pack bombs, Spawnable_Missiles_MP fuel/cookoff scripts — no fix needed.

**RULE: `Explosion()` destroys terrain and pushes objects but does NOT damage players. Any weapon that relies on Explosion for damage MUST add explicit `ApplyPlayerDamage()` with distance falloff and kill attribution (`toolId` + `attacker`).**

**Date fixed:** 2026-03-19

---

## Issue #57: goto/::label:: not supported in Lua 5.1

**Bug:** Infinity_Technique v2 conversion used `goto continuec` / `::continuec::` as a `continue` statement in a `for p in Players()` loop. Lua 5.1 (Teardown's runtime) does not support `goto` or labels — these were added in Lua 5.2. The mod would crash at runtime on the `goto` line.

**Root cause:** The converter used a modern Lua pattern (`goto` as `continue`) that isn't available in Teardown's embedded Lua 5.1 interpreter.

**Fix:** Convert `if not data then goto continuec end ... ::continuec::` to `if data then ... end` — wrap the loop body in a conditional instead of using goto to skip it.

**Affected mod:** Infinity_Technique (2 occurrences, both in `client.tick` player loop)

**RULE: Never use `goto` or `::label::` in Teardown mods. Lua 5.1 does not support them. Use `if-then-end` wrapping instead of `goto` as `continue`. The GOTO-LABEL lint rule (Tier 1 FAIL) catches this.**

**Date fixed:** 2026-03-19

---

## Issue #58: ClientCall(p, ...) sends positional effects only to acting player

**Bug:** Three mods used `ClientCall(p, "client.onEffect", ...)` to send sound/visual effects at world positions, but targeted only the acting player (`p`) instead of broadcasting to all clients (`0`). Other players couldn't hear shots, magnet placement sounds, or see landmine explosion effects.

**Root cause:** Confusion between `ClientCall(p, ...)` (sends to one player — correct for personal HUD/recoil feedback) and `ClientCall(0, ...)` (broadcasts to all — correct for world-space positional effects like sounds and particles).

**Fix:** Changed `ClientCall(p, ...)` to `ClientCall(0, ...)` for all world-space effect callbacks.

**Affected mods (batch 1, 2026-03-19):**
- Omni_Gun: `client.onShootFX` (shoot sound + muzzle particles) — 1 fix
- Magnets: `client.onPlaceFX`, `client.onRemoveFX`, `client.onPolarityFX` — 3 fixes
- Explosive_Pack: `client.onExplosion` for landmine auto-trigger — 1 fix (manual detonation already used `ClientCall(0, ...)`)

**Affected mods (batch 2, 2026-03-20 — 10 framework mods):**
Earlier listed as "NOT affected" — re-investigation found all 10 used `ClientCall(p, "client.onShoot", ...)` with 0 ClientCall(0,...) broadcasts. Other players couldn't hear gunfire, reload sounds, or dry fire clicks.
- AK105_Framework, AK12_Framework, AK74_Framework, G17_Framework, G36K_Framework, M4A1_Framework, Kriss_Vector, Dragunov_SVU, SCAR_Framework, Saiga12_Framework
- Fix: split into `ClientCall(0, ...)` for world-space sounds + `ClientCall(p, ...)` for personal camera shake/recoil

**NOT affected (verified correct):**
- Predator_Missile_MP, Light_Katana_MP: Already broadcast via `for-loop over GetAllPlayers()`.
- Portal_Gun, ODM_Gear, Telekinesis, Magnetizer_V2: Personal action feedback, correctly targeted.

**RULE: Use `ClientCall(0, ...)` for world-space sound/visual effects (explosions, gunfire, placement sounds). Use `ClientCall(p, ...)` only for personal feedback (camera shake, recoil, HUD sync). Not lint-checkable — requires understanding handler semantics.**

**Date fixed:** 2026-03-19 (batch 1), 2026-03-20 (batch 2 — 10 framework mods)

---

## Issue #59: Deep analysis false positives masking real issues

**Bug:** The deepcheck.py static analysis tool reported 57 FAIL mods, but many were false positives caused by 5 distinct bugs in the analysis tool itself. This masked real issues and made batch results unreliable for quality assessment.

**Root causes (5 bugs fixed):**

1. **ServerCall param counter couldn't handle nested parentheses.** `ServerCall("server.fn", p, GetLocalPlayer())` was miscounted because the inner `()` confused the parameter parser. Fix: Proper paren depth tracking.

2. **HUD tool guard detector only checked `==` patterns.** Mods using `~=` patterns (e.g., `if GetPlayerTool(p) ~= "toolid"`) were flagged as missing guards. Fix: Accept both `==` and `~=` comparisons.

3. **Effect chain warned for engine-replicated functions.** `Shoot()` and `Explosion()` are auto-replicated by the Teardown engine to all clients — they don't need explicit `ClientCall` for effects. Fix: Exclude engine-replicated functions from effect chain analysis.

4. **Asset validator didn't recognize `.tde` encrypted files.** Teardown stores some assets as `file.ogg.tde` (encrypted). Code references `file.ogg` and the engine finds `.ogg.tde` transparently. Deepcheck only checked for exact filename match. Fix: Check for both `filename` and `filename.tde`.

5. **Optional ServerCall params flagged as missing.** Some ServerCall patterns have optional trailing params. Fix: Added optional param detection.

**Impact (phase 1):** FAIL count dropped 57→35 (22 false positives eliminated).

**Phase 2 fixes (same session, by api_surgeon):** 3 additional deepcheck.py improvements eliminated 7 more false positives (35→28 FAIL):

6. **API regex matched custom functions with same name.** `server.Shoot()` / `client.Shoot()` (custom user functions) matched the regex for Teardown's `Shoot()` API. Fix: `(?<!\.)` negative lookbehind — only match bare `Shoot()`, not `obj.Shoot()`. Fixed 4 ARM mods + others.

7. **Shadowed API names not detected.** Mods defining custom global `function Shoot()` or `function QueryShot()` were still flagged for missing server-side calls. Fix: Track custom global function definitions and exclude their call sites from API analysis. Fixed Attack_Drone.

8. **Lua optional param idiom not recognized.** `function foo(param) param = param or default ...end` — the `param or default` pattern means the param is optional, but deepcheck counted it as required. Fix: Detect Lua optional param idiom. Fixed Shape_Collapsor.

**Phase 2 impact:** FAIL count 28→12 (16 more false positives eliminated, 5 additional deepcheck fixes):

9. **Firing chain didn't trace function calls.** `usetool → ServerCall("server.fire") → fire() → Shoot()` was missed because the validator only looked for `Shoot()` directly in ServerCall target functions, not in functions they call. Fix: Recursive function-call tracing through the call graph.

10. **ServerCall alias detection.** `server.syncSelection = server.onSelect` and similar Lua aliases meant the declared function had a different name from the ServerCall target. Fix: Alias detection for `a = b` patterns.

11. **@lint-ok not respected in damage detection.** `-- @lint-ok EFFECT-CHAIN` suppressed lint but deepcheck still flagged the same code. Fix: Respect @lint-ok annotations in deepcheck validators.

12. **@deepcheck-ok annotation support.** Entity scripts that are intentionally server-side (vehicle turrets, weapon systems) need suppression. Fix: New `@deepcheck-ok` annotation for intentional patterns that don't need fixing.

13. **Entity script awareness.** Entity scripts run in their own context but deepcheck analyzed them as if they were in the main script's server/client split. Fix: Entity script detection and adjusted analysis.

**Also fixed (code):** American_High_School: added missing `server.syncSelection()` function (ServerCall target didn't exist). MrRandoms_Vehicles: `@deepcheck-ok` for entity scripts.

**Final impact:** FAIL count 57→12 (45 false positives eliminated across 13 fixes). Remaining 12 FAILs: 8 missing assets (T98/T99), 4 server-side effects in entity scripts (T96).

**Test count:** 458→523 tests (65 new tests covering all fixes).

**Affected tools:** `tools/deepcheck.py` (asset validator, firing chain, HUD validator, ServerCall checker, effect chain, API regex matching, function-call tracing, alias detection)

**RULE: When deepcheck reports a FAIL, verify the finding manually before creating fix tasks. False positives in analysis tools waste more time than they save — always add regression tests for fixed false positives.**

**Date fixed:** 2026-03-19

---

## Issue #60: v1-style SetBool tool setup — tools invisible to joining players

**Bug:** AC130_Airstrike_MP and Bunker_Buster_MP used v1-style `SetBool("game.tool.X.enabled", true)` + `SetFloat("game.tool.X.ammo", 101)` in `server.init()` instead of per-player `SetToolEnabled("toolid", true, p)` + `SetToolAmmo("toolid", 101, p)` in a `PlayersAdded()` loop. The v1 registry calls only affect the host — joining players never get the tool enabled, so it's invisible in their toolbar.

**Root cause:** These mods were converted to v2 but the tool setup was left in the v1 pattern. The `RegisterTool()` call was correctly present, but without `SetToolEnabled` per-player, joining players can't use the tool.

**Fix:** Removed v1 `SetBool`/`SetFloat`/`SetString` from `server.init()`. Added `PlayersAdded()` loop in `server.tick()` with `SetToolEnabled(id, true, p)` + `SetToolAmmo(id, 101, p)`.

**Mods fixed:** AC130_Airstrike_MP, Bunker_Buster_MP

**Note:** 40+ other mods still have v1 `SetBool` calls in `server.init()`, but they ALSO have correct v2 `SetToolEnabled` per-player setup — the v1 calls are harmless legacy cruft, not bugs.

**RULE:** Always use `SetToolEnabled("id", true, p)` + `SetToolAmmo("id", N, p)` in `PlayersAdded()`. Never rely on `SetBool("game.tool.X.enabled", true)` — it only works for the host.

**Date fixed:** 2026-03-19

---

## Issue #61: Deep analysis HUD guard false positives from options.lua

**Bug:** 16 mods showed false "client.draw() has no GetPlayerTool guard" WARN because deepcheck combined source from all .lua files. When a mod has both `main.lua` and `options.lua` defining `client.draw()`, the extractor could pick up the options.lua version (which has no tool guard because it's the settings page UI).

**Root cause:** `check_hud()` read all .lua files including `options.lua`. In Teardown, `options.lua` runs in a different context (mod settings page) and its `client.draw()` is separate from the gameplay HUD.

**Fix:** Skip `options.lua` in `check_hud()`. Also added `@deepcheck-ok HUD` suppression (file-level and line-level) for launcher/controller mods that intentionally draw HUD across all tools (AC130, Bunker_Buster, Predator_Missile, Bomb_Attack, CnC_Weather_Machine).

**Impact:** 16 false positive WARNs eliminated. 5 genuine HUD WARNs suppressed with annotations. Batch results improved 101→43 WARN.

**RULE:** Deepcheck must skip `options.lua` when analyzing gameplay code. Use `@deepcheck-ok HUD` for mods with intentional cross-tool HUD.

**Date fixed:** 2026-03-19

---

## Issue #62: Deepcheck auxiliary target false positives + hit effect broadcasting

**Bug:** deepcheck.py's firing chain and effect chain validators generated WARNs for auxiliary ServerCall/ClientCall targets (setOptionsOpen, reload, setMode, cancelStrike, UI counters, state sync) even when the server already had a complete damage chain. Additionally, `_extract_functions()` used dict assignment which caused options.lua `client.draw()` to overwrite main.lua's version, losing the tool guard.

**Root causes (4 categories):**

1. **options.lua shadow** (check_hud, Issue #61): `_extract_functions()` dict key collision — options.lua `client.draw()` overwrote main.lua's. Fix: concatenate duplicate function bodies.
2. **Auxiliary ServerCall targets** (check_firing_chain): ServerCall targets like `setOptionsOpen`, `reload`, `setMode` were flagged even when server already had Shoot/QueryShot/Explosion in other targets. Fix: expanded `any_target_has_damage` to include `Explosion()` and `server_damage_apis`.
3. **Auxiliary ClientCall targets** (check_effect_chain): ClientCall targets for UI/state sync were flagged even when other targets had PlaySound/SpawnParticle or when `Shoot()`/`Explosion()` auto-replicates effects. Fix: auxiliary target suppression when effects exist elsewhere.
4. **Target dedup**: `servercall_targets` and `clientcall_targets` now use sets to prevent duplicate findings from aliases.

**Also this session:** API Surgeon added ClientCall hit effect broadcasting to 9 standard-pattern mods (500_Magnum, AK-47, AWP, Desert_Eagle, Dual_Berettas, Attack_Drone, Charge_Shotgun, Exploding_Star, Guided_Missile) — adding `client.onProjectileHit` with PlaySound + SpawnParticle so other players can hear/see bullet impacts.

**Impact:** Batch deep analysis improved 77 PASS / 101 WARN / 12 FAIL → 162 PASS / 16 WARN / 0 FAIL. Test count: 523 → 548 (25 new tests across all fixes).

**RULE:** When deepcheck reports a WARN for auxiliary ServerCall/ClientCall targets, check if the server already has damage APIs in other targets before treating it as actionable.

**Date fixed:** 2026-03-19

---

## Issue #63: Missing MOD/ prefix on asset paths causes silent load failure in v2

**Bug:** 7 mods had asset paths like `LoadSound("snd/fire.ogg")` or `LoadSprite("img/crosshair.png")` without the `MOD/` prefix. In v1, the engine resolved relative paths from the mod folder. In v2, the engine requires explicit `MOD/snd/fire.ogg` — without it, `LoadSound`/`LoadSprite`/`UiImage` silently return nil/0 with no error. Assets appear missing at runtime (no sound, no sprite) but the mod doesn't crash.

**Root cause:** v1→v2 conversions preserved original asset paths without adding the `MOD/` prefix required in v2.

**Fix:** Added `MOD/` prefix to all relative asset paths.

**Mods fixed (7):**
- Lava_Gun: UiImage crosshair
- BHL-X42: LoadSprite
- CnC_Weather_Machine: LoadSound (4 paths) + LoadSprite
- Hurricanes_and_Blizzards: 8 paths across 4 files
- Ion_Cannon_Beacon: 8 paths
- Jetpack: 1 path
- M2A1_Flamethrower: asset copy

**RULE: All asset paths in v2 MUST use `MOD/` prefix: `LoadSound("MOD/snd/file.ogg")`, `LoadSprite("MOD/img/sprite.png")`, `UiImage("MOD/ui/image.png")`. Without it, assets silently fail to load.**

**Date fixed:** 2026-03-19

**Auto-fix available (2026-03-21):** `python -m tools.fix --only missing-mod-prefix` adds `MOD/` prefix to `LoadSound`/`LoadLoop`/`LoadSprite`/`LoadImage`/`UiImage` paths missing it. Use `--dry-run` to preview. 382 findings fixable across all mods.

---

## Issue #64: Orphaned `end` from incomplete raw-key block removal

**Bug:** ARM_M4A4 and ARM_NOVA had compile errors ("Error compiling" in game log). When the `InputPressed("mmb", p)` block was refactored to use the ServerCall pattern (raw key fix), the `if` block was deleted but its closing `end` and `sharedData.CurrentFireMode = ...` assignment were left behind. The orphaned `end` caused Lua to see an unmatched block terminator — compile error.

**Root cause:** Incomplete block deletion during raw-key refactoring. The fire mode toggle code was moved to `server.onChangeMode()` RPC handler, but the old in-line code wasn't fully cleaned up.

**Fix:** Removed the 3 orphaned lines (assignment + blank line + `end`) from both mods.

**Mods fixed (2):** ARM_M4A4, ARM_NOVA

**RULE: When moving code from an `if` block to an RPC handler, delete the ENTIRE block including its `end`. Verify the `end` count matches the control structure count after editing.**

**Date fixed:** 2026-03-19

---

## Issue #65: Lint annotation placed between function name and arguments

**Bug:** Hurricanes_and_Blizzards had compile errors from lint annotations inserted between `ClientCall` and its `(` arguments: `ClientCall -- @lint-ok PER-TICK-RPC: ...(id, "banner_send", ...)`. Since `--` comments extend to end of line, the `(id, ...)` was commented out. Lua then saw bare `ClientCall` followed by `end` — not a valid statement.

**Root cause:** The `@lint-ok` annotation was placed mid-expression instead of at end of line. Our lint tool matched and annotated the line but the annotation split the function call syntax.

**Fix:** Moved annotations to end of line: `ClientCall(id, ...) -- @lint-ok PER-TICK-RPC: ...`

**Mods fixed (1):** Hurricanes_and_Blizzards (2 lines)

**RULE: `@lint-ok` annotations MUST go at the END of the line, AFTER the closing `)`. NEVER between a function name and its arguments. Pattern to avoid: `Func -- comment(args)`. Correct: `Func(args) -- comment`.**

**Date fixed:** 2026-03-19

---

## Issue #66: Game crash from mod enumeration — strncpy buffer overflow

**Bug:** Game crashed during startup with a strncpy buffer overflow in C++ engine code (empty Lua callstack). Crash occurred during mod directory enumeration, not during script compilation. The crash was NOT caused by any specific Lua code change — it was triggered by one of 53 installed mods (39 RMW weapon pack mods + 14 others) causing the engine to overflow a fixed-size buffer while reading mod metadata/directories.

**Root cause:** Teardown's engine enumerates all mod directories at startup and copies mod metadata (preview images, info.txt, directory names) into fixed-size C string buffers using `strncpy`. With ~178 active mods, one or more mods pushed the buffer past its limit. The exact culprit mod was not isolated — binary search by disabling groups failed because the problematic mod wasn't in either test group.

**Fix:** User unsubscribed from 53 Steam Workshop mods (all 39 RMW weapons + 14 others), reducing active mods from 178 to 125. Crash resolved. Safe engine limit appears to be ~125-150 active mods (see also: shadow volume integer overflow at ~178 mods).

**Related rules:**
- **NEVER copy preview.jpg/preview.png** from workshop originals into Documents/Teardown/mods/ — this was initially suspected as the cause (strncpy on image path processing) and remains dangerous.
- **Active Mod Count Ceiling:** Warn when approaching 150 mods. Engine crashes above ~178.
- **No Mass Changes:** Changing 30+ mods simultaneously makes crash isolation impossible.

**RULE: Monitor active mod count. Warn user at 150+. Engine has hard crash limits around 178 mods (strncpy overflow, shadow volume overflow, audio memory ~760MB). When installing new mods, track total and advise which to keep disabled.**

**Date fixed:** 2026-03-19

---

## Issue #67: V2 script stubs with no callbacks cause "Error compiling"

**Symptom:** Jetskis and Service_Vehicles_MP showed "Error compiling" in the game log despite having valid `#version 2` headers and passing lint. Both are content/vehicle mods with minimal script stubs (4-5 lines) that had `#version 2` + `#include` but no callback function definitions.

**Root cause:** Teardown's v2 script engine expects at least one callback function (`server.init()`, `client.init()`, `server.tick()`, etc.) to be defined. A `#version 2` file with only directives, includes, and comments — but zero callbacks — fails the engine's compilation pass. This affects content mods (maps, vehicle packs) that need `#version 2` for MP compatibility but have no script logic (vehicles spawn via `spawn.txt`, entity scripts handle behavior).

**Fix:** Added empty `server.init()` callback to both mods:
```lua
#version 2
#include "script/include/player.lua"
-- Jetskis -- Content/Vehicle mod (no script logic needed)

function server.init()
    -- Required: v2 scripts must define at least one callback
end
```

**Applied to:** Jetskis (content mod, 5→7 lines), Service_Vehicles_MP (vehicle pack, 4→7 lines). Solid_Sphere_Summoner's compile error was stale (file modified after game log timestamp).

**RULE: All `#version 2` scripts MUST define at least one callback function. Content mods with no script logic should add an empty `server.init()`. Without it, the engine fails to compile the script.**

**Date fixed:** 2026-03-19

---

## Tooling: PER-TICK-RPC destruction event guard (2026-03-19)

**Improvement:** Added a 4th guard pattern to the PER-TICK-RPC lint rule. RPC calls (ServerCall/ClientCall) inside tick/update are now auto-suppressed if `MakeHole()` or `Explosion()` appears within ±10 lines — indicating the RPC is part of a destruction impact event, not continuous per-tick spam.

**Impact:** 11 `@lint-ok PER-TICK-RPC` annotations became stale and were removed from: Armour_Framework_MP, Explosive_Pack, Legacy_Tank_MP, Sith_Saber. PER-TICK-RPC suppressions reduced 134 → 123.

---

## Issue #68: V1 entity scripts silently disabled in multiplayer

**Symptom:** Vehicle physics, interactive objects (doors, steering wheels, sirens, lights), and environmental effects (flames, elevators, cranes) don't work in multiplayer — but produce no error or warning. The game runs fine, these features are just silently missing.

**Root cause:** Entity scripts using v1-style callbacks (`function init()`, `function tick()`, `function update()`, `function draw()`) without a `#version 2` header are silently skipped by the MP engine. Unlike main.lua scripts (which are forced to v2 via `info.txt version = 2`), entity scripts attached to XML entities via `tags="script=foo.lua"` each run in their own script context and must independently declare `#version 2`.

**Detection:** New lint rule V1-ENTITY-SCRIPT (T2-20) scans for files with global-scope v1 callbacks but no `#version 2` header. Severity: WARN (quality/missing functionality, not crash risk).

**Scale:** 81+ findings across 11 mods:
- Armored_Vehicles_MP, Armour_Framework_MP, DAM_Helis, GYM_Ragdoll, Gwel_Mall
- Haul_Truck_MP, Legacy_Tank_MP, Multiplayer_Spawnable_Pack, PPAN_Vehicle_Pack, Vehicle_Pack_Remastered_MP
- SVERLOVSK_TOWN_2_Multiplayer (EVF.lua + Immersive_Tank.lua — discovered 2026-03-21)

**Fix pattern:** Convert each entity script to v2 server/client pattern:
```lua
-- BEFORE (v1 — silently disabled in MP):
function init()
    snd = LoadSound("MOD/snd/engine.ogg")
end
function tick(dt)
    PlaySound(snd, GetBodyTransform(body).pos, 1)
end

-- AFTER (v2 — works in MP):
#version 2
#include "script/include/player.lua"
function server.init()
    -- server-side state init
end
function client.tick(dt)
    -- client-side effects
    local snd = LoadSound("MOD/snd/engine.ogg")
    PlaySound(snd, GetBodyTransform(GetSelf()).pos, 1)
end
```

**See also:** RESEARCH.md Finding #43 (entity script conversion patterns), Issue #67 (v2 stubs need at least one callback).

**RULE: Entity scripts attached to XML entities MUST have `#version 2` and use v2 callbacks (`server.init()`/`client.tick()`/etc.). Without it, they are silently disabled in multiplayer — no error, no warning, just missing functionality.**

**Progress:** Originally 79 scripts across 10 mods, expanded to 81 across 11 mods (SVERLOVSK added 2026-03-21). **ALL 81 CONVERTED (100%)** as of 2026-03-21. Key conversion sessions:
- 2026-03-19: 65 scripts converted/suppressed across Service_Vehicles_MP, Toyota_Supra_MP, Vehicle_Pack_Remastered_MP, Legacy_Tank_MP, Gwel_Mall, PPAN_Vehicle_Pack, others
- 2026-03-20: 14 more — Legacy_Tank_MP/tank.lua (full v1→v2 split with shared table sync), 7 DAM_Helis scripts (engineprops, ground, bigass_bomb, MultiEngine, Rocket, Bomb, Missile), DAM_Helis/GunnerAI.lua (T142, 1381-line AI gunner — final entity script), Gwel_Mall mission scripts, MrRandoms_Vehicles turret scripts, Armour_Framework_MP/tank.lua, Dumb_Stupid_Fast_Cars/recoil.lua, Multiplayer_Spawnable_Pack/bounce.lua x2 (V2-DEAD-CALLBACK: renamed init/tick/update → server.init/server.update + client.init for sound, converted player APIs for MP, added bounce cooldown)
- 2026-03-21: 2 more — SVERLOVSK_TOWN_2_Multiplayer (EVF.lua vehicle door/siren script, Immersive_Tank.lua T-34 tank script)

**Date discovered:** 2026-03-19

---

## Tooling: V1-ENTITY-SCRIPT lint rule + misc improvements (2026-03-19)

**New lint rule:** V1-ENTITY-SCRIPT (T2-20, severity: WARN) — detects v1 entity scripts silently disabled in MP. Found 81 issues across 10 mods. See Issue #68.

**Also improved:** Audit KeybindRemap regex broadened to detect `BINDABLE_KEYS`/`rebindingAction` patterns (+5 mods detected). MCP `generate_tasks_from_lint` timeout 60→180s.

**Tests:** 6 new tests for PER-TICK-RPC destruction event guard (432 → 438): MakeHole nearby clean, Explosion nearby clean, commented MakeHole still flags, far-away MakeHole still flags, input guard clean, one-time event clean. Plus V1-ENTITY-SCRIPT test suite (7 tests). Total: 571.

---

## Milestone: Workshop Exhausted — 161 Mods (2026-03-19)

**Achievement:** 161 mods installed, 438 tests, LINT ZERO (0 findings across 161 mods), 0 missing features (0/117 Shoot, 0/117 AimInfo, 0/134 AmmoPickup). Workshop fully exhausted.

**This session (3 new mods):**
- Infinity_Technique (#159) — first Very High conversion, 3505→~950 lines, full v2 rewrite with 12 abilities
- ARM_AK47 (#160) — workshop v2 install, auto-fixed 7→0 findings, keybind hints added
- GYM_Ragdoll (#161) — second Very High conversion, 294→320 lines v2, 9 backup files removed

**Tooling improvements:**
- MISSING-OPTIONS-GUARD: function-level early return + multi-line if detection → 12 @lint-ok suppressions removed
- gun_v2_generator.py: Issue #47 bug fixed (QueryShot guard), 14 regression tests added
- Cross-mod duplicate tool ID detection added to audit tool
- check_missing_interactive: comment stripping fix (false negatives eliminated)
- FPV_Drone_Tool: 3 server PlaySound→ClientCall pattern fix
- HANDLE-GT-ZERO: expanded suffix list (Sum, Value, Total)

**Remaining convertible (2 — both HIGH/DEFERRED):** GLARE (LnL framework), Lockonauts Toolbox (custom UI). 16 UMF-blocked.

---

## Milestone: Deep Analysis Zero FAIL — 178 Mods (2026-03-19)

**Achievement:** 178 mods installed. 546 tests. LINT ZERO (0 findings, 30 rules). 0 missing features (0/123 Shoot, 0/123 AimInfo, 0/145 AmmoPickup). Deep analysis: **0 FAIL** out of 178 tested (was 57→28→12→0).

**Tasks completed this pass:**
- T96 (api_surgeon): Fixed server-side PlaySound/SpawnParticle/PointLight in 8 mods → moved to client with `ClientCall(0, ...)`
- T97 (api_surgeon): Fixed Bee_Gun missing server.setOptionsOpen function
- T98 (mod_converter): Fixed 22 mods with missing assets — deepcheck.py now skips commented-out refs, supports @deepcheck-ok ASSET
- T99 (mod_converter): Copied missing assets from workshop originals for 5 mods
- Telekinesis: Fixed asset typo (liquidifying→liquifying)
- Koenigsegg_Agera_MP: 15 upstream-missing assets annotated with @deepcheck-ok
- 6 mods annotated as having upstream-missing assets (never in workshop original): American_High_School, Hide_and_Seek, Jetskis, Koenigsegg_Agera_MP, Multiplayer_Spawnable_Pack, PPAN_Vehicle_Pack

**deepcheck.py improvements (Phase 3):** @lint-ok-file SERVER-EFFECT support, commented-out asset skip, @deepcheck-ok ASSET annotation (file-level in first 5 lines, or per-line)

**deepcheck.py improvements (Phase 4 — changes #126-#128):**
- `_extract_functions()` was overwriting duplicate function bodies (dict key collision). Options.lua `client.draw()` shadowed main.lua's, causing false WARNs in HUD, firing chain, effect chain, and ID cross-ref validators. Fix: concatenate bodies instead of overwrite. Impact: 50+ false positives eliminated.
- Firing chain: auxiliary ServerCall targets (setOptionsOpen, setMode, cancelStrike, etc.) generated WARNs even when server already had damage APIs. Fix: expanded `any_target_has_damage` to include `Explosion()` and `server_damage_apis`.
- Regression test added: `test_options_lua_does_not_shadow_main_tool_guard`. Test count: 545→546.

**Remaining WARNs (43 mods — polish, not blocking):**
- 31x QueryShot bullet weapons without ClientCall — these should migrate to `Shoot()` for automatic cross-player effects
- 11x QueryShot beam/melee without ClientCall — need manual effect broadcasting via `ClientCall(0, ...)`
- 1x empty onExplosion callback

**Final deep analysis:** 135 PASS, 43 WARN, 0 FAIL out of 178 tested. deepcheck.py false-positive reduction: 101→43 WARNs (58 eliminated across 8 fixes in 4 phases).

---

## Milestone: UMF Bypass — 164 Mods (2026-03-19)

**Achievement:** 164 mods installed. 438 tests. LINT ZERO. 0 missing features. First 3 UMF-blocked mods converted via bypass strategy.

**UMF bypass conversions (3 mods, Batch 13):**
- Omni_Gun (#162) — 370 lines standalone v2 (replaces ~11K UMF framework). Physics projectile spawner.
- Magnets (#163) — ~330 lines standalone v2. N/S polarity magnet physics simulation.
- Ultimate_Jetpack (#164) — ~310 lines standalone v2. Omnidirectional jetpack, zero per-tick RPC.

**Key resource:** `docs/UMF_TRANSLATION_GUIDE.md` — all UMF API→v2 equivalents (237 lines). 14 UMF-blocked mods remaining, next targets: Shards Summoner (LOW-MEDIUM), Poltergeists (MEDIUM).

---

## Milestone: UMF Bypass Complete — 171 Mods (2026-03-19)

**Achievement:** 171 mods installed. 458 tests. LINT ZERO (0 findings across 171 mods, all tiers). 0 missing features (0/120 Shoot, 0/120 AimInfo, 0/142 AmmoPickup). UMF bypass sprint complete — 10 UMF-blocked mods converted in Batch 13.

**UMF bypass conversions (mods #165–#171, completing Batch 13):**
- Poltergeists (#165) — 580 lines. Possessed objects attack players.
- Melt (#166) — 350 lines. Voxel-by-voxel melt tool, 3 modes.
- Bouncepad (#167) — 500 lines. Trampolines/bouncepads/jumppads.
- Corrupted_Crystal (#168) — 400 lines. Auto-growing crystals.
- Singularity (#169) — 530 lines. 10 singularity physics effects.
- Solid_Sphere_Summoner (#170) — 460 lines. Sphere summoning/launching.
- Control (#171) — 430 lines. Telekinetic powers (grab/throw/jump/slam/dash/hover).

**Bug fixes this session:**
- Issue #58: ClientCall targeting — 5 fixes across 3 mods (world-space effects → `ClientCall(0, ...)`)
- Issue #47: 6 additional QueryShot player guards (DAM_Helis 2x, Armour_Framework_MP 4x)
- T80: 10 DAMAGE-NO-ATTACKER fixes across 5 mods (kill attribution restored)
- EXPLOSION-NO-DAMAGE lint rule refined (Shoot no longer suppresses)

**Tooling:**
- 2 new lint rules: DAMAGE-NO-ATTACKER, SETPLAYER-ARG-ORDER (30 total)
- CLIENT-SERVER-FUNC expanded: +QueryShot, +Spawn
- 20 new tests (438→458)
- 9 auto-fixers

**Post-session update (2026-03-19):** 4 additional mods converted: Adjustable_Fire (#174), Enchanter (#175, UMF bypass), Always_Up (#176, UMF bypass), Hungry_Slimes (#177, UMF bypass). **177 mods total**. Workshop fully exhausted. 523 tests (deepcheck.py false-positive fixes: C4, Light_Katana_MP now PASS).

**Deferred (11):** GLARE (LnL framework), Lockonauts Toolbox (custom UI), Chaos_Mod (8,100 lines), Player_Scaler (MP-incompatible physics), Ascended Sword Master (4,577 lines, 14 stances), Shards Summoner (2,677 lines), AI Trainer, Blight Gun, Thermite Cannon (1,691 lines), Tameable Dragon (5,037 lines AI), Synthetic Swarm (DO NOT CONVERT).

---

## Milestone: Sprint Complete — 123 Mods (2026-03-18)

**Achievement:** 123 mods installed. 0 FAIL, 0 WARN across all lint tiers. 342 tests passing. Sprint exceeded target of 120 by 3.

**Session totals:** 21 new conversions (102→123), 59+ bug fixes (39 QueryShot guard + 20 handle fixes), 2 new lint rules (QUERYSHOT-PLAYER-GUARD, PER-TICK-SPATIAL), 1 new auto-fix (queryshot-guard), 20 new tests (318→338). Issues documented: #47 expanded (39 mods), #50 (invisible smoke), #51 (ServerCall param sweep complete), #52 (community v2 raw key bugs).

**Remaining convertible (3 — all require dedicated sessions):** GLARE (6100+ lines, LnL framework), Infinity Technique (4004 lines, messy), Lockonauts Toolbox (8412 lines, multi-tool). 16 mods UMF-blocked.

---

## Milestone: Zero Warnings — All Tiers Clean (2026-03-18)

**Achievement:** 102 mods installed. 0 FAIL, 0 WARN across all lint tiers (25 checks). 0 X flags in audit. 86 gun mods fully compliant. 318 tests passing.

**What was resolved to reach this point (from 65→102 mods, 88 warnings→0):**
- PER-TICK-RPC sprint: 85 warnings triaged. QA Lead improved lint (state-change guard detection, 8-line window, user-defined func exclusion) → eliminated 50 false positives. API Surgeon (T40) converted real per-tick ServerCall/ClientCall to registry sync in 7 mods. Mod Converter (T41) applied @lint-ok suppressions on verified false positives.
- CLIENT-SERVER-FUNC: 3 warnings eliminated by QA Lead lint fix (user-defined Shoot() functions excluded).
- SERVER-EFFECT: lint boundary detection fixed (Asteroid_Strike false positives eliminated). Rods_from_Gods + Molotov @lint-ok suppressed (spawned entity scripts / server-only projectile positions).
- RMW weapon pack: 39 mods converted (2 rocket launchers + 5 hitscan exemplars + 32 mass batch). All lint clean, all audit compliant.
- New docs: OFFICIAL_DEVELOPER_DOCS.md (ground truth API), PER_TICK_RPC_FIX_GUIDE.md, MPLIB_INTERNALS.md, TEAM_PLUGINS.md

---

## Tooling: VERSION2-NOT-LINE1 lint rule reverted (2026-03-19)

**What happened:** A lint rule was added requiring `#version 2` to appear on line 1 of scripts. This caused 60 false positives across working mods — the Teardown preprocessor finds `#version 2` on ANY line, not just line 1. Many mods have it after comment headers.

**Root cause of Solid_Sphere_Summoner compile error:** Originally misdiagnosed as `#version 2` not being on line 1. Actual cause was CRLF line endings interfering with the preprocessor. Fix: reposition the `#version 2` line and normalize line endings.

**RULE: `#version 2` can appear on any line in a script — the preprocessor scans the whole file. Do not enforce line-1 placement. CRLF line endings can cause compile errors — ensure LF-only in Lua scripts.**

**Date:** 2026-03-19

---

## Milestone: Entity Script Conversion Sprint — 82% Complete (2026-03-19)

**Achievement:** 65 of 79 v1 entity scripts converted or suppressed (82% done). 5 mods fully cleared of V1-ENTITY-SCRIPT warnings. 14 scripts remaining across 4 mods.

**Fully cleared mods (5):**
- **Gwel_Mall** — ALL 38 scripts converted (dealership_spin ×6, speed ×2, discolights ×2, technoloop ×2, tagsmanager ×4, AutoGate ×9, doors ×3, radio ×2, discosmoke ×2, car ×2, shapesprite, betteralarmlights, voxscripts ×2)
- **Multiplayer_Spawnable_Pack** — ALL 18 scripts converted (physics: spin ×2, floating, blackhole, whitehole, trampoline, sharp, sensor/timed bombs. Effects: balloon, rocket, napalm/gas bombs, asteroid, particle spawner, ferris, rc. Dead: maze)
- **Armored_Vehicles_MP** — bulldozer.lua full v2, ground.lua voxscript suppressed
- **Haul_Truck_MP** — ground.lua voxscript suppressed
- **Legacy_Tank_MP** — ALL entity scripts now v2: RepairKit.lua + cookoff.lua (T120), tank.lua 500+ line full server/client split (T125, completed 2026-03-20). Referenced by 8 XML prefabs

**Partially cleared:**
- **PPAN_Vehicle_Pack** — 6 of 8 done (steer, breakgroup, cleaner, InitLightsShut, bike, popupHeadlight). 2 crane scripts remaining (WASD_CRANE is 152 lines with rope physics)

**Remaining (14 scripts, all complex):**
- PPAN_Vehicle_Pack: 2 crane scripts (rope physics + local server={} shadowing)
- DAM_Helis: 8 scripts (flight model, weapons, CRJ-200 engine)
- Vehicle_Pack_Remastered_MP: 1 aircraft flight model
- GYM_Ragdoll: 1 debug spawner

**Also fixed this session:**
- T126: Solid_Sphere_Summoner compile error (#version 2 + CRLF), Jetskis preview.jpg removed
- T127: Armored_Vehicles_MP bulldozer.lua full v2 server/client split
- MrRandoms_Vehicles: 4 entity scripts rewritten (policelights ×2, firetruck, elevator) — had 3 bugs each beyond SERVER-EFFECT (IsPlayerLocal on server, PlayLoop on server, raw key input on server)
- VERSION2-NOT-LINE1 lint rule reverted (60 false positives — see tooling entry above)

**All converted mods:** lint tier-1 clean, deepcheck PASS.

**Date:** 2026-03-19

---

## Tooling: V2-DEAD-CALLBACK lint rule (2026-03-19)

**New lint rule:** V2-DEAD-CALLBACK (check_v2_dead_callbacks) — detects scripts with `#version 2` that contain v1-style callbacks (`init()`, `tick()`, `update()`, `draw()`).

**Two severity levels:**
- **WARN** — script has `#version 2` but ONLY dead v1 callbacks. The entire script is non-functional in MP (all callbacks silently ignored). 5 found: Koenigsegg_Agera_MP (4 scripts), GYM_Ragdoll (1 script).
- **INFO** — script has `#version 2` with working v2 callbacks AND leftover dead v1 callbacks. Script works but has dead code. 10 found across 5 mods.

**Distinction from V1-ENTITY-SCRIPT:** V1-ENTITY-SCRIPT catches scripts missing `#version 2` entirely. V2-DEAD-CALLBACK catches scripts that HAVE `#version 2` but still use v1 callback names.

**Note:** This rule currently has NO test coverage in test_lint.py. Tests needed.

**Date added:** 2026-03-19 (documented 2026-03-20)

---

## Issue #69: MEGAGUN double bullet movement on host (shared players[p])

**Symptom:** On the host, MEGAGUN bullets fly at 2x speed. On remote clients, no bullet tracers visible.

**Root cause:** Host runs both server and client code. `server.tick` creates `players[p]`; `client.tick`'s `if not players[p]` skips on host → same data object shared. Server moves bullets in `data.bulletsInAir`, then client moves them again → 2x speed. Remote clients have empty `bulletsInAir` → no tracers.

**Fix:** Separated `data.bulletsInAir` (server auth) from `data.clientTracers` (client visual). Server broadcasts `ClientCall(0, "client.onMegagunFire", p, numBullets, bulletSpeed)`. Client creates approximate tracers from `GetPlayerEyeTransform(p)`.

**RULE: Separate server-owned and client-owned data into distinct fields when both contexts process the same arrays.**

**Date fixed:** 2026-03-20

---

## Issue #70: M2A1_Flamethrower double napalm on host (same pattern as #69)

**Symptom:** Host napalm at 2x rate/speed. Remote clients see no fire stream.

**Root cause:** Same shared `players[p]` pattern. Both contexts create napalm in `data.projectiles` and run physics.

**Fix:** Client uses `data.clientProjectiles`/`data.clientProjCounter`. No ClientCall needed — client uses `InputDown("usetool", p)` + `GetPlayerAimInfo` for all players. Server remains authoritative (SpawnFire, ApplyPlayerDamage).

**Date fixed:** 2026-03-20

---

## Issue #71: V1 options.lua silently disabled in multiplayer

**Symptom:** Mod options menus don't appear in multiplayer. Players can't change settings. The options button exists but the menu is non-functional.

**Root cause:** Same as Issue #68 — `options.lua` files are separate script contexts from `main.lua`. Without `#version 2` and v2 callbacks, they are silently disabled in MP. The engine loads them but skips execution of v1-style `init()`/`draw()` callbacks.

**Fix:** Add `#version 2` header and convert callbacks:
- `init()` → `client.init()` (options.lua runs client-side only)
- `draw()` → `client.draw()`
- No server callbacks needed — options UI is always client-local

**Scope:** 25 mods have options.lua. 16 already had `#version 2`. 9 were v1 (silently disabled in MP).
**Converted (9/9 — 100% complete):** Desert_Eagle, GYM_Ragdoll, Multiple_Grenade_Launcher, TABS_Effect, Airstrike_Arsenal, Ion_Cannon_Beacon, Artillery_Barrage_RELOADED, Minecraft_Building_Tool, Molotov_Cocktail

**RULE: options.lua follows the same v2 rules as entity scripts (Issue #68) — each script context needs independent `#version 2` + v2 callbacks. Converting only main.lua does NOT fix options.lua.**

**Date identified:** 2026-03-20

---

## Issue #72: Host double-processing of scalar fields in shared players[p] (extends #69/#70)

**Symptom:** On the host, mods exhibit 2x ammo drain, 2x timer speed, 2x reload speed, 2x recoil. Remote clients unaffected. Subtle — less visible than the array-based double-processing in Issues #69/#70.

**Root cause:** Same shared `players[p]` pattern as #69/#70, but affecting scalar fields instead of arrays. In v2, the host runs both `server.tickPlayer` and `client.tickPlayer` on the same `data` object. When both contexts modify the same scalar fields (ammo counters, cooldown timers, reload timers, recoil values), the host processes them twice per frame. Remote clients only run `client.tickPlayer`, so they see normal 1x behavior.

**Fix pattern:** Gate client-side continuous state writes with an `isHostClient` check, or use separate server-owned vs client-owned field names for state that both contexts modify:
```lua
-- Option A: Skip client scalar updates on host
function client.tickPlayer(p, dt)
    local data = players[p]
    if not IsPlayerLocal(p) then return end
    -- Only local player updates client-side scalars
    data.clientRecoil = math.max(0, data.clientRecoil - dt * 5)
end

-- Option B: Separate fields (same as #69/#70 pattern)
-- Server uses: data.ammo, data.reloadTimer, data.cooldown
-- Client uses: data.clientAmmo, data.clientRecoil, data.clientCooldown
```

**Affected mods:** 38 identified (extends beyond MEGAGUN and M2A1_Flamethrower which were fixed in #69/#70). Full list TBD — api_surgeon investigating.
**Fixed so far:** M2A1_Flamethrower (T163), MEGAGUN (T164)

**RULE: On host, both server.tickPlayer and client.tickPlayer share the same `players[p]` data object. Any scalar field modified in both contexts (ammo, timers, cooldowns, recoil) will be processed 2x on host. Gate client writes with `IsPlayerLocal(p)` or use separate field names.**

**Date identified:** 2026-03-20

---

## Issue #73: Dynamic keybind variables with player param — lint-invisible RAW-KEY-PLAYER

**Symptom:** Thruster_Tool_Multiplayer thrusters completely non-functional for non-host players. No lint warning.

**Root cause:** `InputPressed(rocket.keybind, p)` and `InputDown(rocket.keybind, p)` use a **variable** for the key name instead of a string literal. Lint rule RAW-KEY-PLAYER only matches string patterns like `InputPressed("rmb", p)`. When the key name is a variable, lint can't detect the raw key + player param combination, so the bug goes undetected.

**Fix:** Move all raw key input to client-side with `IsPlayerLocal(p)` check, use `ServerCall` to bridge to server logic. Same pattern as all other RAW-KEY-PLAYER fixes, just harder to find.

```lua
-- BROKEN (invisible to lint):
if InputPressed(rocket.keybind, p) then ... end

-- FIXED:
-- client.tick:
if IsPlayerLocal(p) and InputPressed(rocket.keybind) then
    ServerCall("server.activateRocket", p, rocketIndex)
end
```

**Applied to:** Thruster_Tool_Multiplayer (2 hidden bugs found and fixed, T166)

**RULE: After lint reports 0 findings, manually check for `InputPressed/InputDown/InputReleased` calls where the first argument is a variable (not a string literal). These bypass RAW-KEY-PLAYER detection. Consider adding lint support for this pattern.**

**Date identified:** 2026-03-21

---

## Project Reset Note (2026-03-23)

Path changed from Documents/Teardown/mods/ to C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/ (game install dir). 102 mods reduced to 49 after workshop cleanup. All tools updated.

---

## Issue #74: VecCopy doesn't exist in Teardown Lua

**Symptom:** Projectiles fail to spawn silently.
**Root cause:** `VecCopy(vec)` is not a Teardown API function. Using it causes nil assignment. `Vec(x, y, z)` takes 3 numbers, not another Vec.
**Fix:** Use direct assignment (ServerCall/ClientCall params are already copies) or `Vec(v[1], v[2], v[3])` when explicit copy needed.
**Rule:** Never assume Lua helper functions exist. Check Teardown API docs first.
**Date:** 2026-03-23

## Issue #75: local at file scope invisible across v2 chunks

**Symptom:** Server functions can't access file-scope local variables. Variables are nil.
**Root cause:** v2 preprocessor compiles server.* and client.* into separate Lua chunks. local at file scope becomes an upvalue in one chunk only.
**Fix:** Use globals for file-scope state in v2 scripts. local inside functions is fine.
**Rule:** NEVER use local at file scope in #version 2 scripts.
**Date:** 2026-03-23

## Issue #76: camerax/cameray returns 0 when SetCameraTransform active

**Symptom:** Custom camera (AC-130 fly cam, FPV drone, lightsabers) stops responding to mouse.
**Root cause:** Engine suppresses camerax/cameray when script controls camera via SetCameraTransform. mousedx/mousedy give raw delta that always works.
**Fix:** Keep mousedx/mousedy for mods with SetCameraTransform. Only use camerax/cameray for normal gameplay camera.
**Rule:** Check for SetCameraTransform before changing mouse input code.
**Date:** 2026-03-23

## Issue #77: PlayersAdded() requires player.lua include

**Symptom:** server.tick crashes silently. All subsequent tick processing stops.
**Root cause:** PlayersAdded()/PlayersRemoved()/Players() are defined in script/include/player.lua. Without the include, calling them errors. AC-130 had no include but we added PlayersAdded().
**Fix:** Use GetAddedPlayers()/GetRemovedPlayers()/GetAllPlayers() (engine built-ins, no include needed) OR add the include.
**Rule:** Check for #include "script/include/player.lua" before using iterator functions.
**Date:** 2026-03-23

## Issue #78: File integrity check -- all players need identical mod files

**Symptom:** Friends get "Connection Lost. Mod files differ from host" when joining.
**Root cause:** Teardown compares mod file hashes between host and clients. Patched files differ from original workshop versions.
**Fix:** Publish patched mods to Workshop so all players get identical files via Steam, or distribute via ModSync.
**Rule:** Every patched mod must be distributed to all players. Workshop publishing is the most reliable method.
**Date:** 2026-03-23

## Issue #79: AC-130 500-element shared table sync bomb

**Symptom:** Extreme lag when AC-130 is used in MP. Game becomes unplayable for all players.
**Root cause:** shared.projectiles had 500 entries synced to ALL clients every frame (~3500 values/frame). LoadSound() called per-hit instead of cached.
**Fix:** Reduced pool from 500 to 30 (94% reduction). Cached snd_explosion/snd_splash/snd_fire in server.init(). Original projectile logic preserved unchanged.
**Rule:** Keep shared.* tables small. Cache LoadSound in init, never call per-hit. When fixing performance, apply surgical changes to working code -- never rewrite.
**Date:** 2026-03-23

## Issue #80: v2 preprocessor breaks closures across server/client function definitions

**Symptom:** Framework callbacks (server.init, server.tick, etc.) defined INSIDE a function call (like `DEF.Tool()`) silently fail. Functions appear defined but local variables from the enclosing scope are nil at runtime.
**Root cause:** The v2 preprocessor extracts `function server.*()` and `function client.*()` into separate Lua chunks regardless of nesting depth. Local variables in the enclosing function become upvalues tied to one chunk, invisible to the other.
**Fix:** Define all server/client callbacks at the TOP LEVEL of the file. Store state in global tables (like `DEF._tools`). Never use closures across server/client boundaries.
**Rule:** NEVER define `function server.*()` or `function client.*()` inside another function. They must be at file scope. Reference globals only.
**Date:** 2026-03-25

## Issue #81: PlayersAdded/PlayersRemoved/Players iterators consumed after one pass

**Symptom:** In a multi-tool framework, only the first registered tool gets PlayersAdded events.
**Root cause:** These return Lua iterators. Once iterated, they're exhausted. Second call in same tick returns nothing.
**Fix:** Collect results into a table once at the top of tick, then iterate the table for each tool.
**Rule:** NEVER call PlayersAdded/PlayersRemoved/Players more than once per tick. Collect into table first if multiple consumers need results.
**Date:** 2026-03-25

## Issue #82: goto/::label:: is Lua 5.2+ — Teardown uses Lua 5.1

**Symptom:** Syntax error or compile failure.
**Root cause:** Teardown's Lua is 5.1. No goto support.
**Fix:** Use if/end guards or function extraction.
**Rule:** NEVER use goto or ::label::. Use if/end.
**Date:** 2026-03-25

## Issue #83: SpawnParticle/PointLight/SetShapeEmissiveScale called on server

**Symptom:** No visual effect. Silent failure.
**Root cause:** Client-only rendering functions. Server has no renderer. Exception: PlaySound on server DOES auto-sync.
**Fix:** Move visual calls to client.tick. Sync via registry or ClientCall if triggered by server events.
**Rule:** SpawnParticle, PointLight, DrawLine, DrawSprite, SetShapeEmissiveScale = CLIENT-ONLY. PlaySound = server OK.
**Date:** 2026-03-25

## Issue #84: Server-owned timer not synced to client for visual feedback

**Symptom:** Recoil/cooldown animation never shows. Timer always 0 on client.
**Root cause:** DEF uses separate state tables (_serverPlayers/_clientPlayers) to prevent double-processing. Server timer value doesn't reach client data.
**Fix:** Use registry broadcast: `tool:SyncToClient("timer", value, p)` on server, `tool:ReadSync("timer", p, 0)` on client.
**Rule:** Separate state tables prevent double-processing but also prevent sharing. Explicitly sync any server value the client needs for visuals.
**Date:** 2026-03-25

## Issue #85: LoadLoop() at file scope — client-only function in shared context

**Symptom:** Crash or nil handle when server processes file-scope LoadLoop call.
**Root cause:** LoadLoop is client-only. File-scope code runs in shared context.
**Fix:** Load via `tool:ClientInit(function() snd = LoadLoop("path") end)`.
**Rule:** LoadLoop = client-only. Use ClientInit hook, never file scope. LoadSound works in both contexts.
**Date:** 2026-03-25

## Issue #86: Projectile distance check uses absolute position, not travel distance

**Symptom:** Projectiles die early when player is far from world origin.
**Root cause:** `VecLength(proj.pos) > 500` checks distance from (0,0,0), not from muzzle.
**Fix:** Store `origin` per projectile. Check `VecLength(VecSub(pos, origin)) > maxDist`.
**Rule:** Distance checks must use travel distance from spawn, not absolute world position.
**Date:** 2026-03-25

## Issue #87: Inactive projectiles accumulate — memory leak

**Symptom:** Projectile table grows. pairs() iteration slows over time.
**Root cause:** `proj.active = false` leaves entry in table. pairs() still iterates it.
**Fix:** Set `data.projectiles[idx] = nil`. Lua GC handles the rest.
**Rule:** Remove table entries with nil assignment, not flag fields. pairs() skips nil keys.
**Date:** 2026-03-25

## Issue #88: GetPlayerCanUseTool(p) — phantom API

**Symptom:** Unknown. Function may not exist.
**Root cause:** Vanilla mods (minigun, lasergun) never use it. Engine gates usetool internally.
**Fix:** Removed from DEF. Use InputPressed("usetool", p) alone.
**Rule:** Do not call unverified APIs. If vanilla mods don't use it, verify before adding.
**Date:** 2026-03-25
