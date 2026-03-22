# MP Reference — Consolidated Technical Guide

> Merged from RESEARCH.md, V2_SYNC_PATTERNS.md, MP_DESYNC_PATTERNS.md, PER_TICK_RPC_FIX_GUIDE.md.
> For the gold-standard patterns from vanilla code, see **BASE_GAME_MP_PATTERNS.md** first.

---

## Key Function Signatures

### Shoot()
```lua
Shoot(origin, direction, type, strength, maxDist, playerId, toolId)
```
- `type`: `"bullet"` (default), `"rocket"`, `"gun"`, `"shotgun"`
- `strength`: damage scaling (1.0 = standard)
- `maxDist`: max range (100.0 = standard)
- `playerId`: attacker for kill attribution
- `toolId`: tool name for kill feed (7th arg, confirmed working despite script_defs showing 6)
- Does NOT play sound — call `PlaySound()` separately on server

### QueryShot()
```lua
hit, dist, shape, playerId, damageFactor, normal = QueryShot(origin, direction, maxDist, radius, playerId)
```
- `radius`: hit radius (0 = precise raycast)
- `playerId` (5th arg): firing player (excluded from self-hit)
- Returns `playerId=0` when no player hit — guard with `~= 0` (Lua 0 is truthy)

### ApplyPlayerDamage()
```lua
ApplyPlayerDamage(targetPlayer, damage, cause, instigatingPlayer)
```
- `cause`: tool ID for kill feed
- `instigatingPlayer`: who caused it (0 for environmental)

### GetPlayerAimInfo()
```lua
hit, startPos, endPos, direction, normal, hitDist, hitEntity, hitMaterial = GetPlayerAimInfo(muzzlePos, maxDist, playerId)
```
- Handles MP aim compensation automatically
- Also has simple form: `GetPlayerAimInfo(playerId)` (returns basic aim data)

### Explosion()
```lua
Explosion(pos, size)  -- size: 0.5 to 4.0
```
- Auto-syncs to all clients
- Does NOT damage players — add explicit `ApplyPlayerDamage()` with distance falloff

---

## Server vs Client Function Split

### Server-only (crash or silently fail on client):
`Explosion`, `MakeHole`, `SpawnFire`, `Shoot`, `ApplyPlayerDamage`, `SetPlayerTransform`, `SetPlayerVelocity`, `SetBodyVelocity`, `SetBodyTransform`, `ApplyBodyImpulse`, `Delete`, `SetProperty`, `Paint`, `PaintRGBA`, `DisablePlayer`, `DisablePlayerInput`, `DisablePlayerDamage`, `RespawnPlayer`, `SetPlayerHealth`, `SetPlayerTool`, `Constrain*`

### Client-only (crash or silently fail on server):
`SetCamera*`, `Draw*`, `Highlight*`, `Ui*` (only in client.draw), `InputClear`, `PlayHaptic`, `SetToolHaptic`, `Music*`, post-processing

### Server but effectively client-only (only renders for host):
`SpawnParticle`, `PointLight`, `SetShapeEmissiveScale` — always call in `client.*`

**Exception:** `PlaySound()` on server auto-syncs to all clients (confirmed in vanilla snowball, tank, tools)

### Both contexts (safe anywhere):
All `Get*` queries, Vec/Quat/Transform math, `Find*`, `Query*`, registry `Get*`

---

## Sync Mechanisms (in priority order)

### 1. Engine-Native Functions
`Shoot`, `Explosion`, `Spawn`, `Delete`, `MakeHole`, `SpawnFire`, `SetBodyVelocity`, `PlaySound`, `SetToolAmmo`, `SetToolEnabled`, `SetPlayerTool`, `SetPlayerHealth`, `RespawnPlayer`, `SetPlayerTransform`, `SetPlayerColor` — all auto-sync when called on server.

### 2. Registry Broadcast
```lua
SetFloat("mymod.score", 42, true)  -- 3rd arg = broadcast to all clients
local score = GetFloat("mymod.score")  -- client reads
```
Best for: simple values, per-player state. Per-player key pattern: `"mod."..p..".fieldName"`

### 3. shared.* Tables
```lua
-- Server writes:
shared.scores = { [1] = 10, [2] = 5 }
-- Client reads (auto-synced, read-only on client):
local myScore = shared.scores[GetLocalPlayer()]
```
Best for: complex structured state, game mode data.

### 4. ClientCall / ServerCall (events only)
```lua
ServerCall("server.fn", p, ...)      -- client → server (p is REQUIRED, not auto-injected)
ClientCall(0, "client.fn", ...)      -- server → ALL clients (world events)
ClientCall(p, "client.fn", ...)      -- server → one client (personal feedback)
```
Best for: discrete one-time events. NEVER use per-tick.

---

## The Dual-Simulation Problem

Server and client run separate Lua contexts. Both simulate independently but WILL drift because `dt` differs, `math.random()` seeds differ, and floats accumulate errors.

**Fix: Local Prediction + Server-Synced Remote**
```lua
function client.tickPlayer(p, dt)
    if not IsPlayerLocal(p) then
        -- REMOTE: read server-synced state, interpolate
        local syncPos = Vec(GetFloat("mod."..p..".px"), GetFloat("mod."..p..".py"), GetFloat("mod."..p..".pz"))
        data.pos = VecLerp(data.pos, syncPos, 0.3)
        return
    end
    -- LOCAL: full simulation (responsive, no latency)
end
```

**Interpolation tuning:** 0.1 = smooth/laggy, 0.3 = balanced (default), 0.5 = snappy/jittery, 1.0 = raw

**Quaternion sync:** Write 4 components via `SetFloat("mod."..p..".rx/ry/rz/rw", ..., true)`, reconstruct on client, use `QuatSlerp` for interpolation.

---

## 7 Desync Root Causes

### RC1: Client-Side Projectile Physics for Remote Players
Each client computes different results due to dt drift and random seeds.
**Fix:** Gate all projectile physics with `IsPlayerLocal(p)`. Server does damage via Shoot/QueryShot.

### RC2: Per-Tick ServerCall/ClientCall
Floods the reliable network channel causing lag.
**Fix:** Use registry sync for continuous state. See PER-TICK-RPC Decision Tree below.

### RC3: FindShapes/QueryAabb Every Frame
O(n*m) per tick. **Fix:** Throttle to ≤4Hz. Cache results, guard with `IsHandleValid()`.
Note: `FindShapes("tagname", true)` with tag filter is a hash lookup — doesn't need throttling.

### RC4: Server-Side Visual Effects
`SpawnParticle`, `PointLight`, `SetShapeEmissiveScale` only render for host.
**Fix:** Move to `client.*`. Exception: `PlaySound()` on server auto-syncs.

### RC5: Raw Key Input in Server Code
`InputPressed("r", p)` silently fails for non-host.
**Fix:** Client-only input with `IsPlayerLocal(p)` + `ServerCall`.
Virtual inputs that DO work with player param: `"usetool"`, `"grab"`, `"interact"`, `"jump"`, `"crouch"`, `"up"/"down"/"left"/"right"`.

### RC6: Client-Side QueryShot
Hit detection differs between clients due to latency.
**Fix:** `QueryShot` + `ApplyPlayerDamage` on SERVER. Client uses `QueryRaycast` for visuals only.

### RC7: Host Double-Processing Shared players[p]
Host runs both server.tickPlayer and client.tickPlayer on same `data` object.
**Fix:** Gate client writes with `IsPlayerLocal(p)` or use separate fields (`data.bulletsInAir` vs `data.clientTracers`).

---

## PER-TICK-RPC Decision Tree

```
Is this RPC triggered by player input?
├── YES → Add InputPressed/InputDown guard (Pattern 1)
└── NO → Is it syncing continuous state?
    ├── YES → Convert to registry sync (Pattern 2)
    └── NO → Is it a one-time event in tick?
        ├── YES → Flag-based trigger, only fire on state change (Pattern 3)
        └── NO → Evaluate if truly needed every tick (Pattern 4: suppress)
```

**Pattern 1 (input guard):** Wrap in `InputDown("usetool")` — RPC only fires during active input.
**Pattern 2 (registry sync):** Replace `ServerCall("server.updatePos", x, y, z)` with `SetFloat("mod."..p..".px", x, true)`.
**Pattern 3 (flag trigger):** Track `lastState`, only fire ServerCall when `currentState ~= lastState`.
**Pattern 4 (suppress):** `-- @lint-ok PER-TICK-RPC` after verifying it's gated by condition + `IsPlayerLocal(p)`.

---

## Input Names

**Logical (work WITH player param):** `"usetool"`, `"grab"`, `"interact"`, `"jump"`, `"crouch"`, `"up"`, `"down"`, `"left"`, `"right"`, `"pause"`, `"flashlight"`, `"map"`

**Physical (client-only, NO player param):** `"a"-"z"`, `"0"-"9"`, `"lmb"`, `"rmb"`, `"mmb"`, `"space"`, `"shift"`, `"ctrl"`, `"alt"`, `"tab"`, `"esc"`, `"return"`, `"f1"-"f12"`, `"mousedx"`, `"mousedy"`, `"mousewheel"`, `"camerax"`, `"cameray"`

---

## 10 Vanilla Code Patterns (from minigun/lasergun)

```lua
-- 1. Shooting with aim compensation
local mt = GetToolLocationWorldTransform("muzzle", p)
local _, pos, _, dir = GetPlayerAimInfo(mt.pos, maxDist, p)
Shoot(pos, VecAdd(dir, rndVec(spread)), "bullet", damage, maxDist, p, "toolId")

-- 2. Beam weapon with player damage
local hit, dist, shape, player, hitFactor = QueryShot(start, dir, len, 0, p)
if player ~= 0 then ApplyPlayerDamage(player, dmg * dt * hitFactor, "tool", p) end

-- 3. Full particle sequence
ParticleReset(); ParticleType("fire"); ParticleDrag(0.001); ParticleGravity(0, 1)
ParticleColor(1, 0.9, 0.8, 1, 0.5, 0.4); ParticleAlpha(0.5, 0.0)
ParticleRadius(0.05, 0.5); ParticleEmissive(10, 0); SpawnParticle(pos, vel, life)

-- 4. Tool registration + ammo crates
RegisterTool("id", "name", "MOD/prefab.xml", slot)
SetToolAmmoPickupAmount("id", 30)

-- 5. ToolAnimator (client, all players)
data.toolAnimator = ToolAnimator()
tickToolAnimator(data.toolAnimator, dt, nil, p)

-- 6. Custom ammo display (client, local only)
if IsPlayerLocal(p) then SetString("game.tool.id.ammo.display", tostring(ammo)) end

-- 7. Haptic feedback (client, local only)
if IsPlayerLocal(p) then PlayHaptic(shootHaptic, 1) end

-- 8. Infinite ammo sentinel
if ammo < 9999 then SetToolAmmo("id", ammo - 1, p) end

-- 9. ShakeCamera (client)
ShakeCamera(pos, intensity, radius)

-- 10. Server plays sounds (auto-syncs)
PlaySound(gunsound, pos)  -- called on server, heard by all clients
```

---

## Built-in Tools Reference

| Tool ID | Name | Default Ammo | Pickup Amount |
|---------|------|-------------|---------------|
| sledge | Sledgehammer | - | - |
| spraycan | Spray Can | - | - |
| extinguisher | Extinguisher | - | - |
| blowtorch | Blowtorch | 20 | - |
| shotgun | Shotgun | 12 | - |
| gun | Pistol | 6 | - |
| pipebomb | Pipe Bomb | 6 | - |
| bomb | Bomb | 6 | - |
| rocket | Rocket Launcher | 6 | - |
| rifle | Hunting Rifle | 6 | - |
| plank | Plank | 8 | - |

Non-droppable on death (hardcoded): `"sledge"`, `"spraycan"`, `"extinguisher"`

---

## Available Helper Includes

```lua
#include "script/include/player.lua"    -- Players(), PlayersAdded(), PlayersRemoved() iterators
#include "script/include/common.lua"    -- clamp(), rnd(), rndVec(), smoothstep(), splitString()
#include "script/toolanimation.lua"     -- ToolAnimator system
#include "script/toolutilities.lua"     -- SpawnTool(), setupToolsUpgradedFully()
```

## Vanilla Reference File Locations

| File | Purpose |
|------|---------|
| `mods/minigun/main.lua` | Bullet weapon reference (Shoot, AimInfo, ToolAnimator) |
| `mods/lasergun/main.lua` | Beam weapon reference (QueryShot, ApplyPlayerDamage, particles) |
| `mods/mpclassics/deathmatch.lua` | Game mode reference |
| `mods/mpclassics/mplib/tools.lua` | Loot crate/ammo/drop system |
| `mods/mpclassics/mplib/hud.lua` | HUD, damage indicators, scoreboard |
| `mods/mpclassics/mplib/stats.lua` | Kill/death tracking |
| `mods/mpclassics/mplib/eventlog.lua` | Kill feed messages |
| `mods/mpclassics/mplib/spectate.lua` | Death camera system |
| `mods/mpclassics/mplib/teams.lua` | Team management |
| `data/script/toolanimation.lua` | ToolAnimator internals |
| `data/script/include/player.lua` | Players/PlayersAdded/PlayersRemoved |
| `data/script/include/common.lua` | Utility functions |

All under `C:/Program Files (x86)/Steam/steamapps/common/Teardown/`

---

## Useful Player API Functions

| Function | Context | Purpose |
|----------|---------|---------|
| `GetPlayerCanUseTool(p)` | Both | Check if player can fire |
| `DisablePlayerInput(p)` | Server | Block all input |
| `DisablePlayerDamage(p)` | Server | Make invulnerable |
| `SetPlayerWalkingSpeed(speed, p)` | Server | Change move speed |
| `SetPlayerHurtSpeedScale(scale, p)` | Server | Slow when damaged |
| `SetPlayerSpawnTransform(t, p)` | Server | Set respawn location |
| `IsPlayerGrounded(p)` | Both | Check if on ground |
| `GetPlayerGrabShape(p)` | Both | What shape player holds |
| `GetPlayerInteractBody(p)` | Both | What body player can interact with |
| `ShakeCamera(pos, intensity, radius)` | Client | Engine-native camera shake |
| `SetCameraDof(near, far, blur)` | Client | Depth of field |

---

## Events System

```lua
-- 4 built-in events:
"playerhurt"    -- victim, healthBefore, healthAfter, attacker, point, impulse
"playerdied"    -- victim, attacker, damage, healthBefore, cause, point, impulse
"explosion"     -- pos, damage
"projectilehit" -- pos, dir, damage, type, player

-- Reading (poll each frame):
local c = GetEventCount("playerdied")
for i = 1, c do
    local victim, attacker, damage, hpBefore, cause = GetEvent("playerdied", i)
end

-- Custom events:
PostEvent("myevent", arg1, arg2)
```

The `cause` field in `playerdied` is the tool ID from `Shoot()` or `ApplyPlayerDamage()` — appears in kill feed.
