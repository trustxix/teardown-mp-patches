# Teardown MP Patcher - Issues and Fixes Log

All resolved bugs and the rules derived from them. Consult before making changes. Append after fixing new issues.

## Key Rules (condensed from all 58 issues)

1. NEVER use `goto` or `::label::` (Lua 5.1 only)
2. NEVER use raw key names with player parameter - use ServerCall pattern
3. ALWAYS use `camerax`/`cameray` for camera input (not mousedx/mousedy)
4. ALWAYS use `GetPlayerEyeTransform(p)` for camera position
5. Every mod with keybinds must show them on-screen
6. Always include group number in RegisterTool
7. Send ALL aim geometry from same client frame - never mix client aim with server eye transform
8. options.lua stays UNCHANGED - uses special callbacks
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
24. `PlaySound()`/`SpawnParticle()` are CLIENT-ONLY — never call on server
25. `QueryShot()` + `ApplyPlayerDamage()` on SERVER — client uses `QueryRaycast()` for visuals
26. Always guard `ApplyPlayerDamage()` with `player ~= 0` after `QueryShot()` — player 0 = host. `if player then` is WRONG (Lua 0 is truthy)
27. Always use 4-param `ApplyPlayerDamage(target, damage, toolId, attacker)` — for environmental hazards, pass `0` as attacker
28. `ServerCall("server.fn", p, ...)` — player ID is REQUIRED, NOT auto-injected by engine
29. `Explosion()` does NOT damage players — add explicit `ApplyPlayerDamage()` with distance falloff + tool ID for kill attribution
30. `ClientCall(0, ...)` for world-space effects (sounds, particles at positions). `ClientCall(p, ...)` only for personal feedback (camera shake, recoil, HUD sync)

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
4. Server-side PlaySound/SpawnParticle (wasted CPU, effects are client-only)
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
- PlaySound/SpawnParticle are client-only (Rule 29)
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

**RULE: #29 — PlaySound/SpawnParticle are CLIENT-ONLY. Use shared state or ClientCall to trigger effects from server events.**

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

**RULE: SpawnParticle/PlaySound are CLIENT-ONLY (rule 29). For multiplayer-visible effects triggered by server events, use `ClientCall(0, "client.effectFunc", ...)` to broadcast to all clients.**

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

**Applied to:** Remote_Explosives (SetShapeEmissiveScale moved from server.tick to client.tick, also removed unused server shape cache, throttled IsShapeBroken to 4Hz). Originally found in Multiplayer_C4 (duplicate — see Issue #54).

**RULE: `SetShapeEmissiveScale` is effectively CLIENT-ONLY for visual effects. Expand Rule 29: PlaySound/SpawnParticle/SetShapeEmissiveScale are client-only — never call on server for visual effects.**

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

**Affected mods:**
- Omni_Gun: `client.onShootFX` (shoot sound + muzzle particles) — 1 fix
- Magnets: `client.onPlaceFX`, `client.onRemoveFX`, `client.onPolarityFX` — 3 fixes
- Explosive_Pack: `client.onExplosion` for landmine auto-trigger — 1 fix (manual detonation already used `ClientCall(0, ...)`)

**NOT affected (verified correct):**
- Framework gun mods (G17, AK series, SCAR, etc.): handlers use `GetLocalPlayer()` for camera shake + recoil — personal feedback. `Shoot()` handles deterministic effects for all clients via engine pipeline.
- Predator_Missile_MP, Light_Katana_MP: Already broadcast via `for-loop over GetAllPlayers()`.
- Portal_Gun, ODM_Gear, Telekinesis, Magnetizer_V2: Personal action feedback, correctly targeted.

**RULE: Use `ClientCall(0, ...)` for world-space sound/visual effects (explosions, gunfire, placement sounds). Use `ClientCall(p, ...)` only for personal feedback (camera shake, recoil, HUD sync). Not lint-checkable — requires understanding handler semantics.**

**Date fixed:** 2026-03-19

---

## Tooling: PER-TICK-RPC destruction event guard (2026-03-19)

**Improvement:** Added a 4th guard pattern to the PER-TICK-RPC lint rule. RPC calls (ServerCall/ClientCall) inside tick/update are now auto-suppressed if `MakeHole()` or `Explosion()` appears within ±10 lines — indicating the RPC is part of a destruction impact event, not continuous per-tick spam.

**Impact:** 11 `@lint-ok PER-TICK-RPC` annotations became stale and were removed from: Armour_Framework_MP, Explosive_Pack, Legacy_Tank_MP, Sith_Saber. PER-TICK-RPC suppressions reduced 134 → 123.

**Also improved:** Audit KeybindRemap regex broadened to detect `BINDABLE_KEYS`/`rebindingAction` patterns (+5 mods detected). MCP `generate_tasks_from_lint` timeout 60→180s.

**Tests:** 6 new tests added (432 → 438): MakeHole nearby clean, Explosion nearby clean, commented MakeHole still flags, far-away MakeHole still flags, input guard clean, one-time event clean.

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

**Remaining convertible (2 — both HIGH/DEFERRED):** GLARE (LnL framework), Lockonauts Toolbox (custom UI). ProBallistics closed (17,447 lines — DO NOT CONVERT). 16 UMF-blocked.

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

**Remaining unconverted:** GLARE (LnL framework), Lockonauts Toolbox (custom UI), 7 UMF-blocked (BHL-X42, Hungry Slimes, Blight Gun, Thermite Cannon, Ascended Sword Master, Enchanter, AI Trainer) + Shards Summoner (DEFERRED). Tameable Dragon deferred (5037 lines AI). ProBallistics/Synthetic Swarm permanently deferred. Note: Hungry Slimes (2695893023) and Poltergeists (2744169679) are DIFFERENT mods by same author.

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
