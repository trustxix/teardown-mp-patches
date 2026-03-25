# Fix Plan: 16 Broken MP Tool Mods

> **For agentic workers:** Work through mods one at a time, tier by tier. After each fix: run `python -m tools.lint --mod "ModName"` and `python -m tools.deploy_framework --fix-lua`. Steps use checkbox syntax for tracking.

**Goal:** Fix all 16 tool mods that desync, lag, or fail in multiplayer so they work for ALL players with zero desync.

**Architecture:** Every fix follows the same 5 principles from BASE_GAME_MP_PATTERNS.md:
1. Server owns all game logic (input, damage, spawning, timers, cooldowns)
2. Client owns all visuals (particles, sprites, ToolAnimator, HUD)
3. No per-tick RPC — use `shared.*` or registry broadcast for continuous state
4. `ClientCall(0,...)` only for discrete one-time events
5. Every `PlayersAdded` has a matching `PlayersRemoved`

**Mod location:** `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/`

**Validation after EVERY mod fix:**
```
python -m tools.deploy_framework --fix-lua   # LF + ASCII enforcement
python -m tools.lint --mod "ModName"
python -m tools.test --mod "ModName" --static
```

---

## Bug Pattern Reference

These are the 5 root causes across all 16 mods. Every fix below applies one or more of these patterns.

### Pattern A: Raw Key + Player Param (silent failure)
```lua
-- BROKEN (silently fails for non-host):
InputPressed("lmb", p)  -- in server context

-- FIXED:
-- CLIENT: detect input locally, send to server
function client.tick(dt)
    for p in Players() do
        if IsPlayerLocal(p) and GetPlayerTool(p) == TOOL_ID then
            if InputPressed("lmb") then
                ServerCall("server.onFire", p)
            end
        end
    end
end
-- SERVER: handle the action
function server.onFire(p)
    -- do the thing
end
```

### Pattern B: Shared Table Sync Bomb
```lua
-- BROKEN (syncs 500 objects every frame):
shared.projectiles = {}
for i = 1, 500 do shared.projectiles[i] = {...} end

-- FIXED: server owns state locally, syncs via discrete events
local projectiles = {}  -- server-local, NOT shared
function server.onHit(projId, hitPos, hitType)
    ClientCall(0, "client.showImpact", hitPos, hitType)  -- one-time event
end
```

### Pattern C: Double-Processing on Host
```lua
-- BROKEN (host runs both, timer decrements 2x):
function server.tick(dt) data.timer = data.timer - dt end
function client.tick(dt) data.timer = data.timer - dt end

-- FIXED: server owns timer, client reads via shared
function server.tick(dt)
    data.timer = data.timer - dt
    shared.timerState[p] = data.timer  -- sync to client for HUD
end
function client.tick(dt)
    local displayTimer = shared.timerState[p]  -- read-only
end
```

### Pattern D: Per-Tick ClientCall Spam
```lua
-- BROKEN (fires 60+ RPCs/sec per player):
function server.tick(dt)
    ClientCall(0, "client.updateMotor", p, motorPower)  -- EVERY tick
end

-- FIXED: use shared.* for continuous state
function server.tick(dt)
    shared.motorPower[p] = motorPower  -- auto-syncs, zero RPC
end
-- Client reads shared.motorPower[p] directly
```

### Pattern E: mousedx/mousedy vs camerax/cameray
```lua
-- For mods using NORMAL gameplay camera (no SetCameraTransform override):
local mx = InputValue("camerax")
local my = InputValue("cameray")

-- For mods using SetCameraTransform (custom camera — AC-130, FPV Drone, etc.):
-- camerax/cameray return 0 when camera is script-controlled!
local mx = InputValue("mousedx")
local my = InputValue("mousedy")
-- Check which applies BEFORE changing any camera input code.
```

---

## Tier 1: Quick Fixes (1 root cause each, <400 lines)

### Task 1: Molotov_Cocktail
**Bug:** Pattern A — `InputPressed("lmb", id)` in `server.toolLogic` (line 297)
**Also:** Particles on server (`SpawnParticle` in server context), no `PlayersRemoved`

**Files:** `Molotov_Cocktail/main.lua` (367 lines)

- [ ] Read full main.lua, identify all server-side input calls
- [ ] Move `InputPressed("lmb")` to client.tick with `IsPlayerLocal(p)` guard
- [ ] Add `ServerCall("server.onThrow", p, aimPos)` — send aim position WITH the call
- [ ] Create `server.onThrow(p, aimPos)` containing the throw logic from `server.Shoot`
- [ ] Move any `SpawnParticle`/`ParticleReset` from server functions to client via `ClientCall(0,...)`
- [ ] Add `PlayersRemoved` cleanup
- [ ] Run lint + fix-lua

### Task 2: CnC_Weather_Machine
**Bug:** `InputPressed("usetool", 0)` — player 0 invalid in MP

**Files:** `CnC_Weather_Machine/main.lua` (400 lines) + 8 weather scripts

- [ ] Read main.lua, find all `InputPressed` calls with player 0 or no player
- [ ] Replace `InputPressed("usetool", 0)` with proper `for p in Players()` + `InputPressed("usetool", p)` loop
- [ ] Check if weather scripts have their own input handling — fix same pattern
- [ ] Add `PlayersRemoved` cleanup
- [ ] Run lint + fix-lua

### Task 3: Rods_from_Gods
**Bug:** `GetLocalPlayer()==1` hardcoded on line 128

**Files:** `Rods_from_Gods/main.lua` (195 lines)

- [ ] Read main.lua
- [ ] Remove the `==1` check: change `GetLocalPlayer()==1` to just allowing any local player
- [ ] The `InputPressed("usetool")` on client without player param is correct — only fires for local player
- [ ] Verify `ServerCall("server.strike", ...)` properly passes `GetLocalPlayer()` as owner
- [ ] Run lint + fix-lua

### Task 4: Predator_Missile_MP
**Bug:** No `PlayersRemoved`, `QueryAabb` per tick

**Files:** `Predator_Missile_MP/main.lua` (1247 lines)

- [ ] Read main.lua
- [ ] Add `PlayersRemoved` cleanup matching every `PlayersAdded`
- [ ] Find `QueryAabb`/`FindBodies` calls in tick functions
- [ ] Throttle to run at most every 0.25s (4Hz) using a timer
- [ ] Run lint + fix-lua

---

## Tier 2: Medium Fixes (input bridges, RPC reduction)

### Task 5: Fire_Fighter_MP
**Bug:** Pattern C — `data.power`, `data.shoottimer`, `data.shells` modified in BOTH server.tick and client.tick

**Files:** `Fire_Fighter_MP/main.lua` (215 lines)

- [ ] Read main.lua
- [ ] **Server owns:** `data.power`, `data.shoottimer`, `data.shellNum`, `data.shells` (for `ExtinguishFireAt`)
- [ ] **Client gets SEPARATE fields:** `data.clientPower`, `data.clientShootTimer`, `data.clientShellNum`, `data.clientShells` (for water particles only)
- [ ] Server syncs power to client: `shared.firePower = shared.firePower or {}` then `shared.firePower[p] = data.power`
- [ ] Client reads `shared.firePower[p]` for visual shell spawning intensity
- [ ] Remove ALL gameplay state modifications from `client.tick` — only visual particle spawning
- [ ] Client shell simulation is visual-only: `SpawnWaterParticles` based on shared power level
- [ ] Run lint + fix-lua

### Task 6: Thruster_Tool_Multiplayer
**Bug:** Pattern A — `InputPressed(rocket.keybind, id)` variable raw keys + player param in server

**Files:** `Thruster_Tool_Multiplayer/main.lua` (310 lines)

- [ ] Read main.lua, map all input calls with context (server vs client, key name, player param)
- [ ] Move ALL input handling to `client.tick`:
  - `InputPressed(rocket.keybind)` with `IsPlayerLocal(p)` → `ServerCall("server.toggleRocket", p, rocketIndex)`
  - `InputDown(rocket.keybind)` → `ServerCall("server.activateRocket", p, rocketIndex, true/false)`
  - `InputPressed("lmb"/"rmb"/"C"/"g"/"f1")` → respective ServerCalls with player ID
- [ ] Create server handler functions for each action
- [ ] Add `PlayersRemoved` cleanup
- [ ] Run lint + fix-lua

### Task 7: Jackhammer
**Bug:** Pattern D — 4-5 `ClientCall(0,...)` per player per tick

**Files:** `Jackhammer/main.lua` (714 lines)

- [ ] Read full main.lua
- [ ] Replace continuous-state ClientCalls with `shared.*`:
  - `shared.motorPower = shared.motorPower or {}`
  - `shared.animTime = shared.animTime or {}`
  - `shared.isHitting = shared.isHitting or {}`
  - Server writes these each tick, client reads directly
- [ ] Keep `ClientCall(0,...)` ONLY for discrete events:
  - `client.onHit(point, normal, sound, r, g, b, a)` — one-time per hit
  - `client.onDestroy(point, normal, r, g, b, a, hardness)` — one-time per break
  - `client.onPlayerDamage(victim, attackerPos, damage)` — one-time
- [ ] Client reads `shared.motorPower[p]` and `shared.animTime[p]` to drive motor sound loop and animation
- [ ] Add `PlayersRemoved` cleanup for `serverData` and `shared.*` tables
- [ ] Add tool ID to `ApplyPlayerDamage(victim, 0.25, "jackhammer", attacker)`
- [ ] Run lint + fix-lua

### Task 8: VectorRazor
**Bug:** Pattern A — variable raw keys for settings in server context

**Files:** `VectorRazor/main.lua` (1318 lines)

- [ ] Read main.lua, find `server.getPlayerBind` system and all `InputPressed(variable, playerId)`
- [ ] Move settings input to client.tick:
  - Client checks `InputPressed(keybind)` with `IsPlayerLocal(p)`
  - Sends `ServerCall("server.adjustSetting", p, settingName, direction)` for each setting change
- [ ] Create `server.adjustSetting(p, settingName, direction)` that modifies `config`
- [ ] Mine placement via `InputPressed("usetool", playerId)` in server is CORRECT — "usetool" is a game action, keep it
- [ ] Move any `SpawnParticle`/`PointLight` from server to client
- [ ] Run lint + fix-lua

---

## Tier 3: Major Fixes (shared table rewrites, complex mods)

### Task 9: AC130_Airstrike_MP
**Bug:** Pattern B — 500-element `shared.projectiles` synced every frame. Pattern E — mousedx.

**Files:** `AC130_Airstrike_MP/main.lua` (775 lines)

- [ ] Read full main.lua
- [ ] **Remove `shared.projectiles` entirely.** Replace with server-local `projectiles = {}`
- [ ] Server tracks projectile physics in its local table (same update logic)
- [ ] On projectile spawn: `ClientCall(0, "client.spawnTrail", projId, startPos, velocity, shellType)`
- [ ] Client maintains its own visual-only projectile copies for trail rendering (no physics, just interpolation)
- [ ] On projectile hit: `ClientCall(0, "client.showImpact", hitPos, shellType, normal)` — client spawns particles/sounds
- [ ] Move ALL particle functions (`SpawnFireParticles`, `SpawnAcidParticles`, `SpawnWaterParticles`) to client-only context
- [ ] Move `Shockwave()` (uses `QueryAabbBodies` + `SetBodyVelocity`) — keep on server (SetBodyVelocity auto-syncs)
- [ ] Cache ALL `LoadSound()` in `server.init()` and `client.init()` — remove from hit handlers
- [ ] Check camera type: if mod uses SetCameraTransform, KEEP mousedx/mousedy (camerax returns 0) in `client.flyCam()`
- [ ] Add `PlayersAdded`/`PlayersRemoved` for per-player airstrike state
- [ ] Cluster bomb (type 4): server spawns 20 child projectiles locally, each hit sends its own ClientCall — no more shared table explosion
- [ ] Run lint + fix-lua

### Task 10: FPV_Drone_Tool
**Bug:** Pattern B — 350+200-element shared tables. Pattern E — mousedx.

**Files:** `FPV_Drone_Tool/main.lua` (1421 lines) + 2 extra lua

- [ ] Read main.lua and extra lua files
- [ ] Identify what the shared tables store (drone positions? trail data? projectiles?)
- [ ] Apply same Pattern B fix as AC-130: server-local state + ClientCall for events
- [ ] Check camera type: if mod uses SetCameraTransform, KEEP mousedx/mousedy
- [ ] Add `PlayersAdded`/`PlayersRemoved`
- [ ] Run lint + fix-lua

### Task 11: All_In_One_Utilities
**Bug:** 29 shared writes, no PlayersAdded/PlayersRemoved

**Files:** `All_In_One_Utilities/main.lua` (584 lines) + 21 extra lua files

- [ ] Read main.lua + scan key extra files for shared state patterns
- [ ] Add `PlayersAdded` in server.tick to initialize per-player state
- [ ] Add `PlayersRemoved` to clean `shared.playerData[p]` on disconnect
- [ ] Audit all 29 shared writes — ensure they're per-player keyed, not global
- [ ] Check that fly/noclip/godmode state is properly per-player and cleaned up
- [ ] Run lint + fix-lua

### Task 12: Bunker_Buster_MP
**Bug:** 49 shared writes, 14 ServerCalls, 44 ClientCalls — heavy sync load

**Files:** `Bunker_Buster_MP/main.lua` (2960 lines) + 2 extra lua

- [ ] Read main.lua (large — may need to read in sections)
- [ ] Categorize all 49 shared writes: which are continuous state vs. event-driven?
- [ ] Move continuous state to server-local tables
- [ ] Keep `shared.*` only for small HUD state clients need (ammo count, mode, cooldown display)
- [ ] Replace per-tick ClientCalls with shared.* reads on client
- [ ] Keep ClientCall only for discrete events (strike launched, impact, mode change notification)
- [ ] Audit ServerCalls — are any per-tick? Replace with registry broadcast or client-local-only
- [ ] Add `PlayersAdded`/`PlayersRemoved` if missing
- [ ] Run lint + fix-lua

---

## Tier 4: Complex Fixes (2500+ line mods)

### Task 13: Light_Katana_MP
**Bug:** 25 shared writes, QueryAabb per tick, mousedx/mousedy

**Files:** `Light_Katana_MP/main.lua` (2509 lines) + 2 extra lua

- [ ] Read main.lua in sections
- [ ] Check camera type: if mod uses SetCameraTransform, KEEP mousedx/mousedy
- [ ] Find all `QueryAabb`/`FindShapes` in tick functions — throttle to ≤4Hz with timer
- [ ] Audit 25 shared writes: categorize as continuous vs event-driven
- [ ] Move continuous state to server-local, keep shared for HUD-needed state
- [ ] Add `PlayersAdded`/`PlayersRemoved` if missing
- [ ] Run lint + fix-lua

### Task 14: Light_Saber
**Bug:** Same as Light_Katana — 25 shared writes, QueryAabb, mousedx

**Files:** `Light_Saber/main.lua` (3267 lines) + 2 extra lua

- [ ] Read main.lua in sections (largest mod)
- [ ] Apply same fixes as Light_Katana: check mousedx vs camerax (SetCameraTransform = keep mousedx), throttle QueryAabb, audit shared writes
- [ ] Add `PlayersAdded`/`PlayersRemoved` if missing
- [ ] Run lint + fix-lua

---

## Post-Fix Validation

### Task 15: Full Lint + Deepcheck Pass
- [ ] Run `python -m tools.lint` on all 16 fixed mods
- [ ] Run `python -m tools.test --batch all --static` for deep analysis
- [ ] Fix any new findings
- [ ] Run `python -m tools.deploy_framework --fix-lua` to ensure LF + ASCII

### Task 16: Update Project Docs
- [ ] Update CLAUDE.md: change live mods path to game install directory
- [ ] Update WHAT_WORKS.md with new patterns from this fix pass
- [ ] Update WHAT_DOESNT_WORK.md with any new failed approaches
- [ ] Update memory files to reflect new mod location

### Task 17: MP Playtest
- [ ] User tests each tier of fixes with friends in actual MP
- [ ] Run `python -m tools.logparse` after each session
- [ ] Document which mods pass/fail in real MP
- [ ] Create follow-up tasks for any mods that still desync

---

## Execution Order

**Recommended: Fix tier 1 first (4 quick wins), test in MP, then proceed tier by tier.**

Each tier builds confidence:
- Tier 1 proves the fix patterns work in real MP
- Tier 2 applies those patterns to more complex input bugs
- Tier 3 tackles the architectural rewrites (shared table removal)
- Tier 4 applies everything to the largest mods

**Do NOT fix all 16 at once.** Fix 2-3, test in MP, confirm fixes work, then continue. This is the batch system — small changes, verified between batches.
