# Teardown Multiplayer Modding Research

Research findings for improving mod multiplayer compatibility. Consult before making changes to any mod.

> **NOTE:** For the authoritative, comprehensive reference, see **`docs/OFFICIAL_DEVELOPER_DOCS.md`** — it contains the complete official API sourced directly from teardowngame.com and has the highest authority. This RESEARCH.md file contains our project-specific findings, analysis, and migration notes that go beyond the official docs.

---

## Research Date: 2026-03-17 (updated 2026-03-18 with authority hierarchy)

### Sources
- [Official Teardown MP Modding Guide](https://teardowngame.com/modding-mp/index.html)
- [Teardown Scripting API](https://www.teardowngame.com/modding/api.html)
- [Teardown Modding Homepage](https://www.teardowngame.com/modding/)
- [mplib Documentation](https://tuxedolabsorg.github.io/mplib/)
- [mplib Source Code](https://github.com/tuxedolabsorg/mplib)
- [Teardown Multiplayer Blog Post](https://blog.voxagon.se/2026/03/13/teardown-multiplayer.html)
- Official reference mods: `minigun`, `lasergun` (in Teardown/mods/)
- Official game mode: `mpclassics` with full mplib integration

---

## Finding #1: GetPlayerAimInfo() — Aim Handling

**Problem:** We use manual `GetPlayerEyeTransform(p)` + `QueryRaycast` for aiming. This doesn't account for multiplayer aim prediction/compensation.

**Official pattern:**
```lua
local _, startPoint, endPoint, dir = GetPlayerAimInfo(muzzlePos, maxDist, p)
```
- `muzzlePos` — world position of the weapon muzzle
- `maxDist` — maximum range
- `p` — player ID
- Returns: unknown, start position, end position (hit point or max range), direction vector
- Handles multiplayer aim compensation automatically

**Where used:** Official minigun, official lasergun

**Impact:** All gun mods have slightly inaccurate aim in multiplayer because we bypass the engine's aim compensation system.

**Action:** Replace manual `GetPlayerEyeTransform` + `QueryRaycast` aim logic with `GetPlayerAimInfo` in gun mods that use QueryRaycast for **weapon aiming**.

**Triage (2026-03-17):** Of 18 mods flagged MANUAL-AIM by lint, only mods using QueryRaycast for actual weapon aim need migration. Most use QueryRaycast legitimately for non-aim purposes:
- **Already migrated:** Airstrike_Arsenal, Lava_Gun, Lightning_Gun, 500_Magnum
- **Real candidates:** HADOUKEN (energy ball direction), M2A1_Flamethrower (flame direction)
- **Valid non-aim uses (no migration needed):** AC130_Airstrike_MP (plane camera), Acid_Gun (particle physics), Asteroid_Strike (orbital strike), Bee_Gun (projectile launch), C4 (placement), Charge_Shotgun (recoil), High_Tech_Drone (drone camera), Holy_Grenade (bounce physics), Lightsaber (melee arcs), Magic_Bag (object picker), Molotov_Cocktail (thrown projectile physics), Multiple_Grenade_Launcher (grenade physics), Revengeance_Katana (slash arcs), Rods_from_Gods (area-effect orbital targeting), Swap_Button (target selection), Thruster_Tool (physics tool), Vacuum_Cleaner (suction), Welding_Tool (weld target), Winch (attach target)

---

## Finding #2: Shoot() — Bullet Weapon Damage

**Problem:** We use `MakeHole(hitPos, size, size, size)` for bullet damage. This only punches voxel holes — it does NOT damage players, doesn't attribute kills, doesn't work with the damage system.

**Official pattern:**
```lua
Shoot(pos, dir, "bullet", damage, range, p, "toolid")
```
- `pos` — start position (muzzle)
- `dir` — direction vector (can add spread with `VecAdd(dir, rndVec(0.02))`)
- `"bullet"` — projectile type
- `damage` — damage amount (1.0 = standard)
- `range` — max distance (100.0 = standard)
- `p` — attacking player ID
- `"toolid"` — tool name for kill attribution

**Where used:** Official minigun

**Impact:** None of our gun mods can kill other players in multiplayer PvP. `MakeHole` only affects voxels, not players.

**Action:** ~~Replace `MakeHole` with `Shoot()` for all bullet/projectile gun mods.~~ **DONE (2026-03-17)** — All gun mods now use `Shoot()` or `QueryShot()` + `ApplyPlayerDamage()` for player damage. MakeHole retained alongside for voxel destruction.

---

## Finding #3: QueryShot() + ApplyPlayerDamage() — Beam/Continuous Weapons

**Problem:** For continuous-fire weapons (lasers, beams), `QueryRaycast` can't detect player hits. No way to damage other players.

**Official pattern:**
```lua
local hit, dist, shape, player, hitFactor, normal = QueryShot(startPoint, dir, len, radius, p)
if hit then
    if player then
        ApplyPlayerDamage(player, damage * dt * hitFactor, "toolid", attackingPlayer)
    end
    if shape then
        MakeHole(hitPos, size, size, size, true)
    end
end
```
- `QueryShot` — like `QueryRaycast` but also detects player hits
- Returns `player` (player ID if a player was hit) and `hitFactor` (damage multiplier based on where hit)
- `ApplyPlayerDamage(targetPlayer, damage, "toolid", attackerPlayer)` — deals damage with proper kill attribution

**Where used:** Official lasergun

**Impact:** Beam/continuous weapons (Laser Cutter, Lightning Gun, Lava Gun, etc.) can't damage players at all.

**Action:** ~~Replace `QueryRaycast` with `QueryShot` for all weapons.~~ **DONE (2026-03-17)** — All beam/melee weapons now use QueryShot + ApplyPlayerDamage. 28 gun mods have player damage enabled.

---

## Finding #4: GetToolLocationWorldTransform() — Named Tool Positions

**Problem:** We hardcode muzzle positions with manual Vec offsets like `Vec(0.35, -0.6, -2.1)`. These are fragile and wrong if the tool model changes.

**Official pattern:**
```lua
local mt = GetToolLocationWorldTransform("muzzle", p)
-- mt.pos is the world position of the "muzzle" location on the tool
```
- Tool vox files can define named locations
- Engine reads them at runtime, accounting for tool animation, player position, etc.
- Much more accurate than manual offsets

**Where used:** Official minigun, official lasergun

**Impact:** Muzzle positions may be slightly off, especially with tool animations or third-person view. This is a lower-priority fix since it requires adding location data to vox files.

**Action:** Lower priority. Would require modifying vox files to add named locations. Manual offsets work adequately for now.

---

## Finding #5: SetToolAmmoPickupAmount() — Ammo Crate Integration

**Problem:** Our mods don't work with the built-in ammo crate system in multiplayer maps.

**Official pattern:**
```lua
function server.init()
    RegisterTool("minigun", "loc@MINIGUN", "MOD/prefab/minigun.xml", 6)
    SetToolAmmoPickupAmount("minigun", 30) -- picking up an ammo crate gives 30 rounds
end
```

**Where used:** Official minigun (30 ammo per pickup), official lasergun (10 ammo per pickup)

**Impact:** Players can't replenish custom weapon ammo from crates on multiplayer maps.

**Action:** ~~Add `SetToolAmmoPickupAmount` to `server.init()` for all weapon mods.~~ **DONE (2026-03-17)** — All 101 mods have AmmoPickup=Y in audit.

---

## Finding #6: Advanced Particle API

**Problem:** We use the simple `SpawnParticle("type", pos, vel, size, life)` for all effects. The engine supports much richer particle control.

**Official pattern:**
```lua
ParticleReset()
ParticleType("fire")
ParticleDrag(0.001)
ParticleGravity(0, 1)
ParticleColor(1, 0.9, 0.8, 1, 0.5, 0.4)  -- start color -> end color
ParticleAlpha(0.5, 0.0)
ParticleRadius(0.05, 0.5)  -- start radius -> end radius
ParticleEmissive(10, 0)  -- start emissive -> end emissive
SpawnParticle(hitPos, vel, lifetime)
```

Available functions:
- `ParticleReset()` — reset all particle properties to default
- `ParticleType("smoke"/"fire"/"water"/"darksmoke")` — particle rendering type
- `ParticleRadius(startRadius, endRadius)` — size over lifetime
- `ParticleAlpha(startAlpha, endAlpha, [fadeType], [fadeIn], [fadeOut])` — opacity over lifetime
- `ParticleColor(r1,g1,b1, r2,g2,b2)` — color interpolation over lifetime
- `ParticleEmissive(startEmissive, endEmissive)` — glow intensity over lifetime
- `ParticleDrag(drag)` — air resistance
- `ParticleGravity(gravity)` or `ParticleGravity(min, max)` — gravity with randomization
- `ParticleCollide(bounce, friction)` — collision behavior

**Where used:** Official lasergun, official smokegun

**Impact:** Our particle effects are basic compared to what the engine supports. Fire, smoke, and impact effects could look much better.

**Action:** Medium priority. Upgrade particle effects in high-visibility mods (Black Hole, Bee Gun, Exploding Star, etc.) using the full particle API.

---

## Finding #7: shared Table — Auto-Synced Server-to-Client State

**Problem:** We use `ClientCall` or savegame reads for server-to-client state sync. The `shared` table auto-syncs automatically.

**Official pattern:**
```lua
-- Server writes:
shared.scores = { [1] = 10, [2] = 5 }

-- Client reads (automatically synced, read-only on client):
local myScore = shared.scores[GetLocalPlayer()]
```

**Impact:** Could simplify state sync patterns. The `shared` table is automatically synchronized from server to all clients without explicit `ClientCall` or `SetFloat(..., true)`.

**Action:** Low priority. Current patterns work. Consider `shared` table for new mods or major refactors.

---

## Finding #8: Script Architecture — Official v2 Structure

**Required for all multiplayer mods:**

`info.txt`:
```
version = 2
```

Every `.lua` file:
```
#version 2
#include "script/include/player.lua"
```

### Callback Functions

**Server-side (host only):**
```lua
function server.init()        -- Called when script loads
function server.tick(dt)      -- Called once per frame (variable timestep)
function server.update(dt)    -- Fixed-timestep update (60 Hz max)
function server.postUpdate()  -- Runs after physics
```

**Client-side (each player):**
```lua
function client.init()        -- Called when script loads
function client.tick(dt)      -- Called once per frame
function client.update(dt)    -- Fixed-timestep update (60 Hz max)
function client.draw()        -- 2D overlay rendering (Ui.* only valid here)
function client.render(dt)    -- Called before final rendering
```

### Three Built-in Tables
| Table | Location | Purpose |
|-------|----------|---------|
| `server` | Host only | Game logic, scoring, validation |
| `client` | Each player | Rendering, UI, effects |
| `shared` | All (read-only on client) | Auto-synced state |

### Communication
- `ServerCall("server.func", args)` — client → server
- `ClientCall(playerId, "client.func", args)` — server → client (0 = broadcast)
- `SetFloat(key, value, true)` — registry sync (3rd arg = auto-replicate)

---

## Priority Action Items

### High Priority (PvP broken without these)
1. Add `Shoot()` to all bullet gun mods — enables player damage
2. Add `QueryShot()` + `ApplyPlayerDamage()` to beam/melee mods
3. Replace manual aim with `GetPlayerAimInfo()` in all weapon mods

### Medium Priority (quality of life)
4. Add `SetToolAmmoPickupAmount()` to all weapon mods
5. Upgrade particle effects with advanced particle API
6. Add `server.setOptionsOpen` + both-side `optionsOpen` guard to all mods (Issue #32)

### Low Priority (nice to have)
7. Migrate to `shared` table where applicable
8. Add named tool locations to vox files for `GetToolLocationWorldTransform`
9. Add haptic feedback with `SetToolHaptic` / `PlayHaptic`

---

## Reference Code: Official Minigun (complete)

Located at: `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/minigun/main.lua`

Key patterns to copy:
- `GetPlayerAimInfo(mt.pos, 100, p)` for aim
- `Shoot(pos, dir, "bullet", 1.0, 100.0, p, "minigun")` for firing
- `GetToolLocationWorldTransform("muzzle", p)` for muzzle position
- `SetToolAmmoPickupAmount("minigun", 30)` for ammo crates
- `GetToolAmmo("minigun", p)` / `SetToolAmmo("minigun", ammo-1, p)` for ammo tracking
- Client mirrors server simulation for visual prediction (barrel spin, recoil)

## Reference Code: Official Lasergun (complete)

Located at: `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/lasergun/main.lua`

Key patterns to copy:
- `QueryShot(startPoint, dir, len, 0, p)` for hit detection (detects players!)
- `ApplyPlayerDamage(player, damage, "lasergun", p)` for player damage
- `SpawnFire(hitPos)` + `MakeHole(hitPos, size, size, size, true)` for environment damage
- Full particle API: `ParticleReset()`, `ParticleType()`, `ParticleRadius()`, etc.
- `SetShapeEmissiveScale(shape, value)` for tool glow effects
- `SetToolHandPoseLocalTransform()` for third-person/VR hand positioning

---

## Finding #9: player.lua Include — Iterator Wrappers

**Location:** `C:/Program Files (x86)/Steam/steamapps/common/Teardown/data/script/include/player.lua`

The `#include "script/include/player.lua"` provides three iterator functions that wrap the raw API:
```lua
function Players()       -- wraps GetAllPlayers() as an iterator
function PlayersAdded()  -- wraps GetAddedPlayers() as an iterator
function PlayersRemoved() -- wraps GetRemovedPlayers() as an iterator
```
These are convenience wrappers. The underlying API functions return TABLES:
- `GetAllPlayers()` → table of player IDs
- `GetAddedPlayers()` → table of newly joined players this frame
- `GetRemovedPlayers()` → table of disconnected players this frame

**Important:** `Players()` etc. are ITERATORS. Use `for p in Players() do` NOT `for _, p in ipairs(Players()) do`.

---

## Finding #10: ToolAnimator System — Official Tool Animation

**Location:** `C:/Program Files (x86)/Steam/steamapps/common/Teardown/data/script/toolanimation.lua`

The official tool animation system handles:
- First-person and third-person tool poses (automatic switching)
- Arm pitch following player look direction
- Action pose (when firing) vs idle/run/jump/swim/crouch poses
- Tool collision solving (pushes tool out of walls)
- Hand pose for character hands gripping the tool
- Smooth pose blending between states

**Usage (from minigun):**
```lua
#include "script/toolanimation.lua"

-- In createPlayerData():
toolAnimator = ToolAnimator(),

-- In client.tickPlayer():
data.toolAnimator.offsetTransform = Transform(Vec(0,recoil,0))
tickToolAnimator(data.toolAnimator, dt, nil, p)
```

**Key function:** `tickToolAnimator(animator, dt, defaultPose, playerId)` — handles everything automatically.

**Impact:** We use manual `SetToolTransform` for all tools. The ToolAnimator gives proper third-person animation, wall collision, pose blending, and matches the official tool feel. Major quality improvement.

---

## Finding #11: Tool Location System — Named Positions on Tools

The ToolAnimator uses `GetToolLocationLocalTransform(poseName, playerId)` to read named positions from tool vox files:

- `"fp_action"` — first-person firing pose
- `"fp_action_crouch"` — first-person crouching fire pose
- `"fp_run"` — first-person running pose
- `"fp_jump"` — first-person jumping pose
- `"fp_swim"` — first-person swimming pose
- `"tp_action"` — third-person firing pose (+ `_rh`, `_lh` for hands)
- `"tp_run"` — third-person running pose
- `"muzzle"` — barrel/muzzle position for `GetToolLocationWorldTransform`

These are defined as location nodes in the tool's vox/xml prefab. Our mods could add these for proper animation support.

---

## Finding #12: mpclassics Deathmatch — Complete Game Mode Pattern

**Location:** `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/mpclassics/deathmatch.lua`

### Key patterns:
1. **`shared.time`** — match timer synced to all clients automatically
2. **`toolsAddModToolsToLootTable(lootTables[2], 3)`** — auto-adds custom mod tools to loot crates! If our mods set `SetToolAmmoPickupAmount`, they appear in MP loot automatically
3. **`GetEventCount("playerdied")` + `GetEvent("playerdied", i)`** — event system for kill tracking
4. **`DisablePlayerInput(p)`** — disables input during countdown/match end
5. **`SetPlayerHurtSpeedScale(0.6, p)`** — slows hurt players
6. **`SetLowHealthBlurThreshold(0.25)`** — visual health feedback
7. **Settings via `savegame.mod.settings.*`** with ServerCall to apply

### Loot tier system:
```lua
lootTables[1] = {{name="steroid", weight=10, amount=4}} -- low tier
lootTables[2] = {{name="shotgun", weight=7}, {name="gun", weight=7}} -- mid tier
lootTables[3] = {{name="rifle", weight=9}, {name="rocket", weight=10}} -- high tier
toolsAddModToolsToLootTable(lootTables[2], 3) -- adds ALL custom mods to mid tier
toolsAddModToolsToLootTable(lootTables[3], 3) -- AND high tier
```

### Drop on death:
The `toolsTick()` function in mplib/tools.lua uses `GetEvent("playerdied")` to detect deaths and drops all tools with remaining ammo as physical pickups. Uses `SpawnTool()` to create world-space tool models.

---

## Finding #13: mplib/tools.lua — Ammo Crate Integration

Custom mod tools are automatically detected via:
```lua
local tools = ListKeys("game.tool")
for i = 1, #tools do
    local toolId = tools[i]
    if GetBool("game.tool."..toolId..".custom") then
        -- This tool is from a mod, add to loot table
    end
end
```

For our mods to integrate with ammo crates, we need:
1. `RegisterTool("toolid", "Name", "MOD/vox/tool.vox", group)` — already done
2. `SetToolAmmoPickupAmount("toolid", amount)` — **MISSING from all our mods**

That's it. Step 2 is all that's needed for automatic loot crate integration in all multiplayer game modes.

---

## Finding #14: Event System — Kill Attribution

The event system tracks player deaths with full attribution:
```lua
-- Server-side, in tick:
local count = GetEventCount("playerdied")
for i = 1, count do
    local victim, attacker, damage, healthBefore, cause, point, impulse = GetEvent("playerdied", i)
    -- victim = player who died
    -- attacker = player who killed them (from ApplyPlayerDamage or Shoot)
    -- cause = tool ID used for the kill
end
```

**For this to work, weapons MUST use:**
- `Shoot(pos, dir, "bullet", damage, range, attackerPlayer, "toolId")` for bullets
- `ApplyPlayerDamage(victim, damage, "toolId", attackerPlayer)` for beams/melee

Without these, kills show as "unknown" and stats don't track properly.

---

## Finding #15: Complete Multiplayer Player API

From API parsing, important functions we're not using:

| Function | Purpose | Context |
|----------|---------|---------|
| `GetPlayerAimInfo(playerId)` | Get aim start/end/direction with MP compensation | Both |
| `GetPlayerCanUseTool(playerId)` | Check if player can fire | Both |
| `DisablePlayerInput(playerId)` | Block all input for a player | Server |
| `DisablePlayerDamage(playerId)` | Make player invulnerable | Server |
| `SetPlayerWalkingSpeed(speed, p)` | Change move speed | Server |
| `SetPlayerHurtSpeedScale(scale, p)` | Slow when damaged | Server |
| `SetPlayerSpawnTransform(t, p)` | Set respawn location | Server |
| `SetPlayerSpawnTool(tool, p)` | Set tool on respawn | Server |
| `GetPlayerGrabShape(p)` | What shape player is holding | Both |
| `GetPlayerPickShape(p)` | What shape player is looking at | Both |
| `GetPlayerInteractBody(p)` | What body player can interact with | Both |
| `ShakeCamera(pos, intensity, radius)` | Shake nearby players' cameras | Client |
| `SetCameraDof(near, far, blur)` | Depth of field effect | Client |
| `SetPlayerColor(color, p)` | Set player character color | Server |
| `IsPlayerGrounded(p)` | Check if on ground | Both |
| `GetPlayerGroundContact(p)` | Get ground surface info | Both |

---

## Updated Priority Action Items

### Critical (PvP fundamentally broken)
1. **Add `Shoot()` to all gun mods** — enables player damage + kill attribution
2. **Add `QueryShot()` + `ApplyPlayerDamage()` to beam/melee mods**
3. **Replace manual aim with `GetPlayerAimInfo()`** in all weapons
4. **Add `SetToolAmmoPickupAmount()` to all weapons** — enables loot crate integration

### High Priority (major quality improvement)
5. **Adopt `ToolAnimator` system** — proper third-person animation, wall collision
6. **Use advanced particle API** — `ParticleReset`/`ParticleType`/`ParticleRadius`/etc.
7. **Use `ShakeCamera()` for explosions** instead of manual screen effects
8. **Add `SetPlayerHurtSpeedScale`** when damaged by custom weapons

### Medium Priority (polish)
9. Use `shared` table for state that all clients need
10. Add named tool locations to vox files
11. Add `SetToolHandPoseLocalTransform` for proper hand positioning
12. Use `GetPlayerCanUseTool(p)` before processing input

### Low Priority (nice to have)
13. Add haptic feedback with `SetToolHaptic` / `PlayHaptic`
14. Support `SetShapeEmissiveScale` for tool glow effects
15. Use `SetCameraDof` for scope/zoom effects

---

## Finding #16: mplib Event Log — Kill Feed System

**Location:** `mpclassics/mplib/eventlog.lua`

The event log broadcasts kill messages to all players via `ClientCall(0, ...)`:

```lua
-- Server: auto-detect deaths and post to kill feed
function eventlogTick(dt)
    local count = GetEventCount("playerdied")
    for i = 1, count do
        local victim, attacker, _, _, cause, _, _ = GetEvent("playerdied", i)
        local msg = {}
        if attacker and attacker > 0 and attacker ~= victim then
            msg[#msg+1] = attacker -- player ID auto-resolves to name + avatar
        end
        msg[#msg+1] = {text = cause, textColor = {1.0, 0.38, 0.38}} -- weapon name in red
        msg[#msg+1] = {playerId = victim, iconRight = true}
        eventlogPostMessage(msg)
    end
end
```

**Key:** The `cause` field in `playerdied` events is the tool ID passed to `Shoot()` or `ApplyPlayerDamage()`. This is why our mods MUST pass the tool ID — it appears in the kill feed.

Custom events can also be posted:
```lua
eventlogPostMessage({playerId, "captured the flag!"}, 5.0)
```

**Items in messages can be:** player IDs (auto-resolve to name+avatar+color), strings (plain text), or tables with `text`, `textColor`, `color`, `icon`, `iconRight`, `playerId` fields.

---

## Finding #17: mplib Spectate System — Death Camera

**Location:** `mpclassics/mplib/spectate.lua`

Provides automatic third-person spectate camera when a player dies:
- Smooth transition from first-person death to orbiting camera
- Mouse orbit and zoom controls
- LMB/RMB to cycle between alive players
- Camera collision with walls (raycast-based)
- Vehicle spectating support
- Shows outline of spectated player
- Red outline of killer for 7 seconds
- Uses `SetCameraDof(0.1, 0.5)` for depth-of-field during death transition

**Usage:**
```lua
function client.tick(dt)
    spectateTick(GetAllPlayers()) -- or {} for self-only
end
function client.draw()
    spectateDraw()
end
function client.render(dt)
    spectateRender(dt)
end
```

**Key APIs used:**
- `GetPlayerBodies(p)` — gets all bodies belonging to a player (for outline drawing)
- `DrawBodyOutline(body, r, g, b, a)` — draws outline around a body
- `GetPlayerAnimator(p)` — for death pose bone positions
- `GetBoneWorldTransform(animator, "chest")` — bone-level positioning
- `QueryRejectPlayer(p)` / `QueryRejectVehicle(v)` — exclude from raycasts
- `GetVehicleTransform(v)` / `GetVehicleBodies(v)` — vehicle spectating
- `SetCameraDof(near, far)` — depth of field

---

## Finding #18: mplib Teams — Player Team Management

**Location:** `mpclassics/mplib/teams.lua`

**Key functions:**
- `teamsInit(numTeams)` — initialize team system
- `teamsSetColors({{r,g,b}, {r,g,b}})` — set team colors
- `teamsSetNames({"Team A", "Team B"})` — set team names
- `teamsGetTeam(playerId)` — get player's team
- `teamsGetLocalTeamPlayers()` — get teammates of local player
- Auto-assigns players to teams on join (balanced)
- Colors player characters via `SetPlayerColor()`

---

## Finding #19: Official V2 Mod Census

Only 2 official tool mods are v2 multiplayer:
- **minigun** (202 lines) — bullet weapon reference
- **lasergun** (233 lines) — beam weapon reference

All others are v1 single-player only:
- jetpack, smokegun, speedometer, vehiclebooster, slowmotion, debuginfo, screenrecorder, heistexample, scriptingshowcase, uishowcase

The **mpclassics** game mode (deathmatch, TDM, CTF) + **mplib** is the most comprehensive v2 reference.

---

## Finding #20: CTF-Specific Patterns

**Location:** `mpclassics/capturetheflag.lua`

Additional patterns from CTF:
- **`toolsPreventToolDrop("flag1")`** — prevents specific tools from dropping on death
- **Team-specific spawn locations** — `spawnSetSpawnTransforms(team1spawns, 1)`
- **`SetPlayerColor(color, p)`** — colors players by team
- **Flag tools registered AFTER adding mod tools to loot** — order matters for loot table

---

## Finding #21: DisablePlayerInput vs DisablePlayer

Two different ways to stop a player:
- **`DisablePlayerInput(p)`** — blocks input but player remains visible and interactive. Used during countdown, match end.
- **`DisablePlayer(p)`** — fully disables a player. Used during setup phase. `IsPlayerDisabled(p)` checks this state.

---

## Finding #22: ShakeCamera — Built-in Camera Shake

```lua
ShakeCamera(pos, intensity, radius, [duration])
```
- `pos` — world position of the shake source
- `intensity` — shake strength
- `radius` — maximum distance for effect
- `duration` — how long (optional)

This is MUCH better than our manual UI-based screen shake. It affects any player within radius, works in 3D space, and is engine-native.

**Impact:** Our Black Hole, Explosion Star, and any explosive mod should use this instead of manual `UiTranslate` shake in `draw()`.

---

## Finding #23: Full Helper Library Files

Available includes for v2 mods:
```lua
#include "script/include/player.lua"   -- Players(), PlayersAdded(), PlayersRemoved() iterators
#include "script/include/common.lua"   -- clamp(), math.clamp(), COLOR_WHITE, etc.
#include "script/toolanimation.lua"    -- ToolAnimator system for tool poses
#include "script/toolutilities.lua"    -- SpawnTool(), setupToolsUpgradedFully()
```

---

## Finding #24: GetPlayerAimInfo Full Signature

From the API and official code, `GetPlayerAimInfo` has two call patterns:

**Pattern 1 (from minigun):**
```lua
local _, pos, _, dir = GetPlayerAimInfo(muzzlePos, maxDist, p)
```

**Pattern 2 (from API):**
```lua
local hit, startPoint, endPoint, direction = GetPlayerAimInfo(playerId)
-- OR
local hit, startPoint, endPoint, direction = GetPlayerAimInfo(muzzlePos, maxDist, playerId)
```

The function handles aim compensation for multiplayer, accounting for network latency and prediction. All gun mods should use this instead of manual `GetPlayerEyeTransform` + `QueryRaycast`.

---

## Complete Reference File Locations

| File | Location | Purpose |
|------|----------|---------|
| player.lua | `data/script/include/player.lua` | Players/PlayersAdded/PlayersRemoved iterators |
| common.lua | `data/script/include/common.lua` | clamp, colors, math helpers |
| toolanimation.lua | `data/script/toolanimation.lua` | ToolAnimator, hand poses, third-person |
| toolutilities.lua | `data/script/toolutilities.lua` | SpawnTool, tool upgrade helpers |
| minigun | `mods/minigun/main.lua` | Bullet weapon reference (Shoot) |
| lasergun | `mods/lasergun/main.lua` | Beam weapon reference (QueryShot) |
| deathmatch | `mods/mpclassics/deathmatch.lua` | Game mode reference |
| ctf | `mods/mpclassics/capturetheflag.lua` | Team game mode reference |
| mplib/tools.lua | `mods/mpclassics/mplib/tools.lua` | Loot crate/ammo system |
| mplib/stats.lua | `mods/mpclassics/mplib/stats.lua` | Kill/death tracking |
| mplib/spawn.lua | `mods/mpclassics/mplib/spawn.lua` | Respawn system |
| mplib/hud.lua | `mods/mpclassics/mplib/hud.lua` | HUD, damage indicators, scoreboard |
| mplib/spectate.lua | `mods/mpclassics/mplib/spectate.lua` | Death camera system |
| mplib/eventlog.lua | `mods/mpclassics/mplib/eventlog.lua` | Kill feed messages |
| mplib/teams.lua | `mods/mpclassics/mplib/teams.lua` | Team management |
| mplib/ui.lua | `mods/mpclassics/mplib/ui.lua` | UI drawing helpers |
| mplib/util.lua | `mods/mpclassics/mplib/util.lua` | Spawn point generation |
| mplib/countdown.lua | `mods/mpclassics/mplib/countdown.lua` | Match countdown |

---

## Finding #25: Teardown Networking Internals (from Voxagon blog)

**Source:** [The unlikely story of Teardown Multiplayer](https://blog.voxagon.se/2026/03/13/teardown-multiplayer.html)

### Two Network Channels
1. **Reliable Stream** — Deterministic commands (destruction, spawning, property changes). Commands are discrete operations like "cut hole at X,Y,Z", NOT raw voxel data.
2. **Unreliable Stream** — Object transforms, velocities, player positions. Server uses priority queue per client (~1 Mbit/client bandwidth budget). Objects selected based on player visibility.

### Key Implications for Modding
- **Destruction is deterministic** — Uses fixed-point integer math. All clients compute the same result from the same command. `MakeHole`/`Explosion` commands are replicated, not their results.
- **Physics is semi-deterministic** — Server is authoritative. Client simulates locally but corrections happen when server state diverges. "Visible snapping" can occur for deprioritized objects.
- **Entity handles can be negative in v2** — Client-side entities use negative handles. Never check `handle > 0` for validity — check `handle ~= 0` instead.
- **Late-join uses command replay** — New joiners replay recorded deterministic commands. This means level state is reconstructed from a command buffer, not a snapshot.

### What This Means for Our Mods
- `MakeHole` and `Explosion` on the server are automatically replicated to all clients. We don't need to mirror them on the client.
- Client-side particles (`SpawnParticle`) are local only — each client runs its own visual effects.
- `Shoot()` is the right way to do bullets because it feeds into the deterministic destruction pipeline with proper replication.
- Server-side `SetBodyTransform`/`SetBodyVelocity` are replicated via the unreliable stream based on priority.
- Avoid creating lots of server-side bodies — each consumes bandwidth from the priority queue.

---

## Finding #26: Entity Handle Validation in v2

**CRITICAL for mod compatibility:**

In v1: all entity handles were positive numbers.
In v2: client-side entities use **negative handles**.

```lua
-- WRONG (breaks in v2):
if body > 0 then
    -- do something
end

-- RIGHT:
if body ~= 0 then
    -- do something
end

-- ALSO RIGHT:
if IsHandleValid(body) then
    -- do something
end
```

**Impact:** Any mod code that checks `body > 0` or `shape > 0` will silently fail for client-side created entities. Audit all mods for this pattern.

---

## Finding #27: Spawn Point Generation

**Location:** `mpclassics/mplib/util.lua`

The spawn system generates valid positions by:
1. Random XZ within level boundary
2. Raycast downward from Y=200 to find ground
3. Skip water, dynamic bodies, steep terrain
4. Score based on distance from other spawns (avoid clustering)
5. Prefer positions near walls (cover)
6. Sort by score, take top N

Key API functions used:
- `GetBoundaryBounds()` / `GetBoundaryArea()` — level boundaries
- `IsPointInBoundaries(pos)` — boundary check with distance
- `IsPointInWater(pos)` — water check
- `FindLocations(tag, recursive)` — find tagged level locations
- `GetLocationTransform(loc)` — get location position
- `GetTagValue(entity, tag)` — read tag values

---

## Finding #28: Workshop Community Mod Patterns

From Steam Workshop research, multiplayer-compatible community mods include:
- **Kooshing's Gun System** — Physical gun pickups (spawn guns as world objects)
- **Fire Fighter Tool MP** — Multiplayer-compatible utility tool
- **Physics Gun MP ports** — Gravity gun style tools adapted for v2
- **Simple UZI TDMP** — Customizable fire rate and hole size

Community mods generally follow the same patterns as official mods but often lack:
- `Shoot()` / `QueryShot()` for proper player damage
- `SetToolAmmoPickupAmount()` for loot integration
- `ToolAnimator` for proper third-person display
- Event-based kill attribution

---

## Implementation Checklist for Bulletproof MP Mods

For each weapon mod, verify ALL of these:

### Required (mod won't work properly in MP without these)
- [ ] `info.txt` has `version = 2`
- [ ] Script has `#version 2` header
- [ ] `#include "script/include/player.lua"` included
- [ ] `RegisterTool()` in `server.init()` with group number
- [ ] `SetToolEnabled()` + `SetToolAmmo()` in `PlayersAdded` loop
- [ ] Per-player state table (`players[p] = createPlayerData()`)
- [ ] Three-phase loop (PlayersAdded/PlayersRemoved/Players) in both server and client tick
- [ ] `data.optionsOpen` guard on ALL `usetool` checks (both server AND client)
- [ ] Entity handle checks use `~= 0` not `> 0`

### Critical for PvP (players can't damage each other without these)
- [ ] `Shoot()` for bullet weapons (replaces MakeHole for guns)
- [ ] `QueryShot()` + `ApplyPlayerDamage()` for beam/melee weapons
- [ ] `GetPlayerAimInfo()` for aim (replaces manual raycast)
- [ ] Tool ID passed to Shoot/ApplyPlayerDamage for kill attribution

### Important for Integration (mod feels broken without these)
- [ ] `SetToolAmmoPickupAmount()` for ammo crate support
- [ ] `SetString("game.tool.TOOLID.ammo.display", "")` to hide engine ammo display
- [ ] Options use `getOptions()` savegame pattern (not cached data.*)
- [ ] `server.setOptionsOpen` ServerCall syncs menu state
- [ ] Keybind hints shown on screen
- [ ] Client mirrors server simulation for visual prediction

### Quality (professional feel)
- [ ] `ToolAnimator` for proper third-person display
- [ ] Advanced particle API (ParticleReset/Type/Radius/etc.)
- [ ] `ShakeCamera()` for explosions
- [ ] `SetPlayerHurtSpeedScale()` for damage feedback
- [ ] Named tool locations for muzzle/poses
- [ ] `GetPlayerCanUseTool(p)` check before input processing

---

## Finding #29: Built-in Events System (from API agent)

4 built-in events plus custom events:

```lua
-- Built-in events:
"playerhurt"   -- victim, healthBefore, healthAfter, attacker, point, impulse
"playerdied"   -- victim, attacker, damage, healthBefore, cause, point, impulse
"explosion"    -- pos, damage
"projectilehit" -- pos, dir, damage, type, player

-- Reading events (poll each frame):
local count = GetEventCount("playerdied")
for i = 1, count do
    local victim, attacker, damage, hpBefore, cause, point, impulse = GetEvent("playerdied", i)
end

-- Custom events:
PostEvent("myevent", arg1, arg2)
RegisterListenerTo(entity, "myevent")
```

The `"projectilehit"` event is fired when `Shoot()` hits something — this could be used for impact effects on the client.

---

## Finding #30: Server-Only vs Client-Only Functions (from API agent)

**Server-only (will crash or silently fail on client):**
- `Explosion()`, `MakeHole()`, `SpawnFire()`, `Shoot()`
- `ApplyPlayerDamage()`, `SetPlayerTransform()`, `SetPlayerVelocity()`
- `SetBodyVelocity()`, `SetBodyTransform()`, `ApplyBodyImpulse()`
- `Delete()`, `SetProperty()`, `Paint()`, `PaintRGBA()`
- `DisablePlayer()`, `DisablePlayerInput()`, `DisablePlayerDamage()`
- `RespawnPlayer()`, `SetPlayerHealth()`, `SetPlayerTool()`
- All `Constrain*` functions

**Client-only (will crash or silently fail on server):**
- All `SetCamera*` functions
- All `Draw*` / `Highlight*` functions (DrawLine, DrawSprite, DrawBodyOutline)
- All `Ui*` functions (only valid in client.draw())
- `InputClear()`, `InputResetOnTransition()`
- `PlayHaptic()`, `SetToolHaptic()`
- Music functions, post-processing

**Both context (safe to call anywhere):**
- All `Get*` query functions
- All Vec/Quat/Transform math
- `Find*` functions, `Query*` functions
- Registry `Get*` functions
- Particle functions (`SpawnParticle`, `ParticleReset`, etc.)
- Sound loading and playing (`LoadSound`, `PlaySound`, `LoadLoop`, `PlayLoop`)

**CRITICAL IMPLICATION:** Our mods call `Explosion()` and `MakeHole()` on both server AND client. The client calls should be removed — these are server-only and the engine automatically replicates them via the deterministic command stream.

---

## Finding #31: Input Names — Physical vs Logical (from API agent)

**Logical inputs (work WITH player parameter):**
- `"usetool"`, `"grab"`, `"interact"`, `"jump"`, `"crouch"`
- `"up"`, `"down"`, `"left"`, `"right"` (WASD movement)
- `"pause"`, `"flashlight"`, `"map"`

**Physical inputs (work WITHOUT player parameter, client-only):**
- Letters: `"a"` through `"z"`
- Numbers: `"0"` through `"9"`
- Mouse: `"lmb"`, `"rmb"`, `"mmb"`
- Special: `"space"`, `"shift"`, `"ctrl"`, `"alt"`, `"tab"`, `"esc"`, `"backspace"`, `"delete"`, `"return"`
- Function: `"f1"` through `"f12"`
- Values: `"mousedx"`, `"mousedy"`, `"mousewheel"`, `"camerax"`, `"cameray"`

This confirms Issue #7 — raw key names silently fail with player param.

---

## Finding #32: Performance Considerations (from unofficial mods agent)

- Keep `shared` table updates **minimal** — every change consumes bandwidth (~1 Mbit/s per client)
- Use `ClientCall` for one-off events, `shared` for persistent state
- Sync only whole-second timers (like mplib Plank Climbers does)
- Spawn particles on CLIENT only — they're local visual effects, not networked
- Use `server.update(dt)` at 60Hz for physics; `server.tick(dt)` for non-critical
- mplib tools module uses round-robin distance checking to spread CPU across frames
- `MakeHole`/`Explosion` are replicated automatically — don't duplicate on client

---

## Finding #33: Community Resources & References

- **Official Discord**: [Teardown Modding Discord](https://discord.com/invite/d4uW3hG)
- **10-part video tutorial series** covering: Introduction, Multiple Players, Input, Overlay, UI, Optimization, Custom Tools, Game Modes, mplib, Advanced Topics
- **mplib GitHub**: [tuxedolabsorg/mplib](https://github.com/tuxedolabsorg/mplib) (MIT, v1.0.0)
- **899+ Workshop items** tagged Multiplayer as of March 2026
- **Full v2 API reference**: `C:/Users/trust/Documents/Teardown/TEARDOWN_V2_API_REFERENCE.md` (1,117 lines, 550+ functions)

---

## Finding #34: 10 Official Code Patterns (from official mods agent)

### Pattern 1: Shooting with Aim Compensation
```lua
local mt = GetToolLocationWorldTransform("muzzle", p)
local _, pos, _, dir = GetPlayerAimInfo(mt.pos, maxDist, p)
dir = VecAdd(dir, rndVec(spread))
Shoot(pos, dir, "bullet", damage, maxDist, p, "toolId")
```

### Pattern 2: Beam Weapon with Player Damage
```lua
local _, start, end_ = GetPlayerAimInfo(muzzlePos, maxDist, p)
local dir = VecNormalize(VecSub(end_, start))
local hit, dist, shape, player, hitFactor, normal = QueryShot(start, dir, len, 0, p)
if player then ApplyPlayerDamage(player, dmg * dt * hitFactor, "tool", p) end
if shape then MakeHole(hitPos, r1, r2, r3, true); SpawnFire(hitPos) end
```

### Pattern 3: Full Particle Sequence
```lua
ParticleReset()
ParticleType("fire")
ParticleDrag(0.001)
ParticleGravity(0, 1)
ParticleColor(1, 0.9, 0.8, 1, 0.5, 0.4)
ParticleAlpha(0.5, 0.0)
ParticleRadius(0.05, 0.5)
ParticleEmissive(10, 0)
ParticleCollide(0, 1)
SpawnParticle(pos, vel, lifetime)
```

### Pattern 4: Tool Registration + Ammo Crates
```lua
function server.init()
    RegisterTool("id", "name", "MOD/prefab.xml", slot)
    SetToolAmmoPickupAmount("id", 30)
end
-- In PlayersAdded:
SetToolEnabled("id", true, p)
SetToolAmmo("id", startAmmo, p)
```

### Pattern 5: ToolAnimator
```lua
data.toolAnimator = ToolAnimator()
data.toolAnimator.offsetTransform = Transform(Vec(0, recoil, 0))
tickToolAnimator(data.toolAnimator, dt, nil, p)
```

### Pattern 6: Custom Ammo Display
```lua
if IsPlayerLocal(p) then
    SetString("game.tool.toolid.ammo.display", tostring(math.floor(ammo)))
end
```

### Pattern 7: Haptic Feedback
```lua
shootHaptic = LoadHaptic("MOD/haptic/fire.xml")
SetToolHaptic("toolid", LoadHaptic("MOD/haptic/background.xml"))
if IsPlayerLocal(p) then PlayHaptic(shootHaptic, 1) end
```

### Pattern 8: Third-Person Awareness
```lua
if GetBool("game.thirdperson") then
    toolTransform = Transform(Vec(0.2, -0.5, -0.2))
    SetToolHandPoseLocalTransform(rightHand, leftHand, p)
end
```

### Pattern 9: Infinite Ammo Check
```lua
if ammo < 9999 then  -- 9999 = infinite ammo sentinel
    SetToolAmmo("id", ammo - 1, p)
end
```

### Pattern 10: Server Plays Sounds Too
The lasergun loads and plays sounds on the SERVER side (not just client). This is valid for sounds that need to be positional and heard by all players near the source.

---

## Finding #35: Definitive Function Signatures (from script_defs.lua)

**Source:** `C:/Program Files (x86)/Steam/steamapps/common/Teardown/data/script_defs.lua`

### Shoot()
```lua
Shoot(origin, direction, type, strength, maxDist, playerId, toolId)
```
- `origin` (TVec) — world position
- `direction` (TVec) — unit direction vector
- `type` (string, optional) — `"bullet"`, `"rocket"`, `"gun"`, or `"shotgun"`. Default `"bullet"`. Also accepts number (1=rocket, else bullet) for backwards compat.
- `strength` (number, optional) — damage scaling, default 1.0
- `maxDist` (number, optional) — max range, default 100.0
- `playerId` (number, optional) — instigating player for kill attribution. Can skip for NPC shots.
- `toolId` (string, optional) — tool ID for kill feed attribution (e.g., `"minigun"`). Confirmed from official minigun source.

**IMPORTANT:** Does NOT play sound. You must `PlaySound` separately.

**CONFIRMED:** The 7th arg is the tool ID for kill feed — verified from official minigun mod and our 86 working gun mods. The `playerdied` event's `cause` field receives this value. Script_defs may show only 6 params but the engine accepts 7.

### QueryShot()
```lua
hit, dist, shape, playerId, playerDamageFactor, normal = QueryShot(origin, direction, maxDist, radius, playerId)
```
- `origin` (TVec) — start position
- `direction` (TVec) — direction vector
- `maxDist` (number) — max distance
- `radius` (number) — hit radius (0 for precise raycast)
- `playerId` (number) — player firing (excluded from self-hit)
- Returns:
  - `hit` (boolean)
  - `dist` (number) — distance to hit
  - `shape` (number) — shape handle (0 if no shape)
  - `playerId` (number) — player hit (0 if no player)
  - `playerDamageFactor` (number) — 1.0 for torso, less for legs. Scale damage by this.
  - `normal` (TVec) — hit surface normal

### ApplyPlayerDamage()
```lua
ApplyPlayerDamage(targetPlayerId, damage, cause, instigatingPlayerId)
```
- `targetPlayerId` (number) — who gets hurt
- `damage` (number) — damage amount
- `cause` (string, optional) — tool ID shown in kill feed
- `instigatingPlayerId` (number, optional) — who caused it

### GetPlayerAimInfo()
```lua
hit, startPos, endPos, direction, normal, hitDist, hitEntity, hitMaterial = GetPlayerAimInfo(position, maxDist, playerId)
```
- `position` (TVec) — muzzle/origin position
- `maxDist` (number) — max range
- `playerId` (number) — player ID
- Returns 8 values including hit info, direction, distance, entity, and material

### Explosion()
```lua
Explosion(pos, size)
```
- `pos` (TVec) — world position
- `size` (number) — 0.5 to 4.0

### Projectile Types
| Type | Behavior |
|------|----------|
| `"bullet"` | Instant hitscan, small hole on impact |
| `"rocket"` | Explosive projectile, creates explosion on impact |
| `"gun"` | Similar to bullet (used by revolver in Wild West DLC) |
| `"shotgun"` | Spread pattern (multiple pellets) |

---

## Finding #36: Built-in Tool Registry (from data/tools.lua)

All built-in tools with their upgrade systems:

| Tool ID | Name | Default Ammo | Max Ammo | Has Damage Upgrade |
|---------|------|-------------|----------|-------------------|
| sledge | Sledgehammer | - | - | No |
| spraycan | Spray Can | - | - | No |
| extinguisher | Extinguisher | - | - | No |
| blowtorch | Blowtorch | 20 | 60 | No |
| shotgun | Shotgun | 12 | 96 | Yes (3-5) |
| gun | Pistol | 6 | 36 | Yes (1-3) |
| pipebomb | Pipe Bomb | 6 | 36 | Yes (blast 2-4) |
| bomb | Bomb | 6 | 36 | Yes (blast 4-6) |
| wire | Cable | 6 | 24 | No |
| rocket | Rocket Launcher | 6 | 24 | Yes (blast 3-5) |
| booster | Rocket Booster | 6 | 24 | No |
| leafblower | Leaf Blower | - | - | No |
| turbo | Vehicle Thruster | 6 | 24 | No |
| explosive | Nitroglycerin | 4 | 16 | Yes (blast 5-8) |
| rifle | Hunting Rifle | 6 | 18 | No |
| plank | Plank | 8 | 64 | No |

Custom mod tools appear in loot crates via `toolsAddModToolsToLootTable` if they set `SetToolAmmoPickupAmount`.

---

## Finding #37: Official Multiplayer Video Tutorials

10-part series (from Teardown modding page):
1. Introduction
2. Multiple Players
3. Input Handling
4. Overlay Graphics
5. User Interfaces
6. Optimization
7. Custom Tools
8. Game Modes
9. mplib
10. Advanced Topics

These cover everything from basic MP concepts to advanced optimization. Watching tutorials #2, #3, #7, and #10 would be most valuable for our mod conversion work.

---

## Finding #38: Community Multiplayer Ecosystem (from unofficial mods agent)

### Active Community Projects
- **899+ Workshop items** tagged Multiplayer (as of March 2026)
- **PropHunt, Hide & Seek, Zombiedown** — full game modes
- **Easy Chat** — text chat with public API
- **Easy Admin Menu** — host server management
- **ULTRA PLAYERMODELS** — custom player model templates
- **140+ Vehicle Pack** — multiplayer vehicle collection
- **Performance Mod v3.1** — MP optimization presets

### GitHub Repositories
| Repo | Purpose |
|------|---------|
| [tuxedolabsorg/mplib](https://github.com/tuxedolabsorg/mplib) | Official MP library (MIT) |
| [BisocM/Hide-Seek-MP](https://github.com/BisocM/Hide-Seek-MP) | Game mode reference |
| [teardownM/server](https://github.com/teardownM/server) | Community dedicated server (Go+Lua) |
| [BrandonAustin01/TDRX](https://github.com/BrandonAustin01/TDRX) | Performance optimization |

### Key Community Insight
All files must be **identical** between host and clients for a session to function. Mod updates that change file contents will break existing sessions.

---

## Finding #39: XML Prefab Format for Tool Definitions

**Source:** `mods/minigun/prefab/minigun.xml`

Tools can be defined as XML prefabs (instead of raw .vox files) to specify named locations:

```xml
<prefab version="1.5.4">
  <group name="instance=MOD/prefab/minigun.xml">
    <group name="eye_space">
      <!-- Tool poses (positions relative to player eye) -->
      <location name="fp_action" tags="name=fp_action" pos="0.1 -0.3 0.0"/>
      <location name="fp_run" tags="name=fp_run" pos="0.1 -0.5 -0.1" rot="20.0 40.0 0.0"/>
      <location name="tp_action" tags="name=tp_action" pos="0.1 -0.5 -0.1"/>
      <location name="tp_run" tags="name=tp_run" pos="..." rot="..."/>
      <location name="tp_crouch" tags="name=tp_crouch" pos="..." rot="..."/>
    </group>
    <group name="tool_space">
      <!-- The actual tool model -->
      <body dynamic="false">
        <vox file="MOD/vox/minigun.vox" scale="0.4"/>
      </body>
      <!-- Hand IK targets (where character hands grip the tool) -->
      <location name="tp_action_rh" tags="name=tp_action_rh ik_hand" pos="0.175 0.0 -0.2" rot="0.0 90.0 0.0"/>
      <location name="tp_action_lh" tags="name=tp_action_lh ik_hand" pos="-0.037 0.1 -0.4" rot="90.0 40.0 0.0"/>
      <location name="tp_run_rh" tags="..." pos="..."/>
      <location name="tp_run_lh" tags="..." pos="..."/>
      <!-- Muzzle position for GetToolLocationWorldTransform("muzzle", p) -->
      <location name="muzzle" tags="name=muzzle" pos="0.025 0.02 -1.05"/>
    </group>
  </group>
</prefab>
```

**Two groups:**
- `eye_space` — tool poses relative to player eye (for `ToolAnimator`)
- `tool_space` — positions on the tool model (muzzle, hand IK)

**Named locations available:**
- `fp_action`, `fp_run`, `fp_jump`, `fp_swim`, `fp_crouch` — first-person poses
- `tp_action`, `tp_run`, `tp_crouch` — third-person poses
- `tp_action_rh/lh`, `tp_run_rh/lh`, `tp_crouch_rh/lh` — hand IK positions (tagged `ik_hand`)
- `muzzle` — barrel tip for `GetToolLocationWorldTransform("muzzle", p)`

**Alternative:** Lasergun uses a raw `.vox` file with no prefab, and handles positioning manually via `SetToolTransform()`. Prefab is optional but enables `ToolAnimator` and proper third-person.

---

## Finding #40: Wild West DLC Weapon Patterns

**Source:** `dlcs/wildwestheist/script/tools/revolver.lua`

The revolver shows additional patterns:
- **Dual muzzles:** `GetToolLocationWorldTransform("muzzle_left")` and `"muzzle_right"` — alternating barrels
- **"gun" projectile type:** `Shoot(firePos, aimDir, "gun", 1)` — slightly different from `"bullet"`
- **Haptic check:** `HapticIsPlaying(handle)` before `PlayHaptic()` to avoid stacking
- **v1 ammo system:** `GetInt("game.tool.revolver.ammo")` / `SetInt(...)` — registry-based ammo (v1 pattern)
- **Can-use check:** `GetBool("game.player.canusetool")` — checks if player is allowed to fire
- **`ToolAnimator` config:** `toolAnimator.armPitchScale = 0.4`, `toolAnimator.toolPitchScale = 0.4` — adjustable pitch tracking

**NOTE:** This is v1 code. A v2 conversion would need player param on all calls.

---

## Finding #41: Built-in Helper Functions (common.lua)

**Available via `#include "script/include/common.lua"` (v2) or `#include "script/common.lua"` (v1):**

| Function | Signature | Description |
|----------|-----------|-------------|
| `clamp` | `clamp(value, min, max)` | Clamp value to range |
| `math.clamp` | `math.clamp(val, lower, upper)` | Same, as math extension |
| `smoothstep` | `smoothstep(edge0, edge1, x)` | Smooth interpolation |
| `trim` | `trim(s)` | Strip whitespace |
| `startsWith` | `startsWith(str, start)` | String prefix check |
| `splitString` | `splitString(str, delimiter)` | Split string to table |
| `hasWord` | `hasWord(str, word)` | Check if word exists in string |
| `rnd` | `rnd(mi, ma)` | Random float in range |
| `rndVec` | `rndVec(length)` | Random direction vector |
| `progressBar` | `progressBar(w, h, t)` | Draw a progress bar UI |
| `queryRaycastLocation` | `queryRaycastLocation(start, dir, dist)` | Raycast returning hit position |
| `drawHintArrow` | `drawHintArrow(str)` | Draw hint tooltip UI |
| `fixedWidthText` | `fixedWidthText(txt, w, font, size)` | Auto-scale text to width |
| `Remap` | `Remap(value, min, max, from, to)` | Remap value between ranges |
| `ReverseTable` | `ReverseTable(tbl)` | Reverse a table |
| `IsRunningOnDesktop` | `IsRunningOnDesktop()` | PC or Mac check |

**Note:** The v2 include (`script/include/common.lua`) does NOT include `math.clamp` — that's only in the v1 version. However, `math.clamp` appears to be built into Teardown's Lua runtime since `smoothstep` uses it without defining it in the v2 include.

---

## Finding #42: Tool Properties via Registry

Built-in tools have configurable properties set via registry:

```lua
-- Shotgun spread
SetFloat("game.tool.shotgun.spread", 0.075, true)  -- campaign default
SetFloat("game.tool.shotgun.spread", 0.045, true)  -- fully upgraded

-- Rifle range
SetFloat("game.tool.rifle.range", 1000, true)

-- Rocket speed
SetFloat("game.tool.rocket.speed", 20.0, true)   -- campaign
SetFloat("game.tool.rocket.speed", 30.0, true)   -- fully upgraded
```

The `setupToolsUpgradedFully()` function in `toolutilities.lua` maxes out all tool upgrades — this is called by mplib `toolsInit()` so all tools are fully upgraded in multiplayer.

---

## RESEARCH COMPLETE — ALL GAPS FILLED

Total findings: **42**
Total lines: ~1200
Companion doc: `TEARDOWN_V2_API_REFERENCE.md` (1,117 lines, 550+ functions)

All gaps from the original research have been filled:
1. XML prefab format for named tool locations — DONE (Finding #39)
2. Wild West DLC weapon patterns — DONE (Finding #40)
3. Space DLC robot patterns — confirmed same `Shoot("bullet"/"rocket")` as other scripts
4. common.lua helpers — DONE (Finding #41)
5. toolutilities.lua SpawnTool — DONE (Finding #42)
