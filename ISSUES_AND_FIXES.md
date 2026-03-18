# Teardown MP Patcher - Issues and Fixes Log

All resolved bugs and the rules derived from them. Consult before making changes. Append after fixing new issues.

## Key Rules (condensed from all 46 issues)

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

## Milestone: Zero Warnings — All Tiers Clean (2026-03-18)

**Achievement:** 102 mods installed. 0 FAIL, 0 WARN across all lint tiers (25 checks). 0 X flags in audit. 86 gun mods fully compliant. 309 tests passing.

**What was resolved to reach this point (from 65→102 mods, 88 warnings→0):**
- PER-TICK-RPC sprint: 85 warnings triaged. QA Lead improved lint (state-change guard detection, 8-line window, user-defined func exclusion) → eliminated 50 false positives. API Surgeon (T40) converted real per-tick ServerCall/ClientCall to registry sync in 7 mods. Mod Converter (T41) applied @lint-ok suppressions on verified false positives.
- CLIENT-SERVER-FUNC: 3 warnings eliminated by QA Lead lint fix (user-defined Shoot() functions excluded).
- SERVER-EFFECT: lint boundary detection fixed (Asteroid_Strike false positives eliminated). Rods_from_Gods + Molotov @lint-ok suppressed (spawned entity scripts / server-only projectile positions).
- RMW weapon pack: 39 mods converted (2 rocket launchers + 5 hitscan exemplars + 32 mass batch). All lint clean, all audit compliant.
- New docs: OFFICIAL_DEVELOPER_DOCS.md (ground truth API), PER_TICK_RPC_FIX_GUIDE.md, MPLIB_INTERNALS.md, TEAM_PLUGINS.md
