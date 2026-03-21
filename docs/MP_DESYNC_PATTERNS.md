# Multiplayer Desync & Performance Patterns

> Created 2026-03-18 during MP Desync Fix Sprint. These patterns cause desync, lag, or silent failures in multiplayer.
>
> **Status (2026-03-21):** 7 root causes documented. RC1-6 resolved across 112 mods (mod set changed 2026-03-21: user removed some, installed ~34 new from workshop backlog). RC7 (host double-processing of shared players[p]) — MEGAGUN + M2A1_Flamethrower fixed (Issues #69-70). 10 framework mods fixed for silent gunfire (Issue #58 batch 2). PlaySound reclassified: works on server, auto-syncs (see RC4 correction below).

## Root Cause #1: Client-Side Projectile Physics for Remote Players

**Symptom:** Projectiles appear doubled, fly in wrong directions for remote players, or cause physics conflicts.

**Problem:** Client runs projectile physics (velocity, gravity, raycasts) for ALL players. In MP, each client computes slightly different results due to `dt` drift, `math.random()` seeds, and floating-point accumulation. Two clients simulating the same projectile diverge within frames.

**Fix:** Gate all projectile physics with `IsPlayerLocal(p)`:

```lua
function client.tickPlayer(p, dt)
    local data = players[p]
    if not IsPlayerLocal(p) then return end  -- remote players: skip projectile sim

    -- Only local player runs projectile physics
    for i, proj in ipairs(data.projectiles) do
        proj.pos = VecAdd(proj.pos, VecScale(proj.vel, dt))
        proj.vel[2] = proj.vel[2] - 9.81 * dt  -- gravity
        -- ... raycast, collision, damage ...
    end
end
```

**Server handles:** Damage (via `Shoot()` or `QueryShot` + `ApplyPlayerDamage`), destruction (`MakeHole`, `Explosion`).
**Client handles (local only):** Visual projectile trail, muzzle flash, camera shake, sound.

---

## Root Cause #2: Per-Tick ServerCall/ClientCall with Large Data

**Symptom:** Lag spikes, network saturation, input delay increases with player count.

**Problem:** RPC calls (`ServerCall`/`ClientCall`) are meant for one-shot events, not continuous state sync. Calling them every tick with position/rotation data floods the reliable network channel.

**Fix:** Use registry sync (`SetFloat`/`SetBool` with `sync=true`) for continuous state:

```lua
-- WRONG: RPC every tick
function server.tickPlayer(p, dt)
    ClientCall(0, "client.updateProjectile", data.pos[1], data.pos[2], data.pos[3])
end

-- RIGHT: Registry sync (engine-managed, batched, prioritized)
function server.tickPlayer(p, dt)
    SetFloat("mod."..p..".px", data.pos[1], true)
    SetFloat("mod."..p..".py", data.pos[2], true)
    SetFloat("mod."..p..".pz", data.pos[3], true)
end
```

**When to use RPC:** Fire events, mode changes, one-time actions (reload, throw, detonate).
**When to use registry:** Positions, rotations, timers, ammo counts, any value that changes every frame.

---

## Root Cause #3: FindShapes/QueryAabb Every Frame

**Symptom:** FPS drops sharply with more players or more objects. Server tick time grows linearly.

**Problem:** `FindShapes()`, `QueryAabb()`, and `FindBodies()` are spatial queries that scan the entire scene. Running them every tick per player is O(n*m) where n=players and m=objects.

**Fix:** Throttle to every N frames or cache results:

```lua
function server.tickPlayer(p, dt)
    local data = players[p]
    data.searchTimer = (data.searchTimer or 0) + dt

    -- Only search every 0.25 seconds (4 Hz instead of 60 Hz)
    if data.searchTimer >= 0.25 then
        data.searchTimer = 0
        data.nearbyShapes = FindShapes("", true)  -- cache result
    end

    -- Use cached data between searches
    for _, shape in ipairs(data.nearbyShapes or {}) do
        -- ... process shapes ...
    end
end
```

**Important:** Cached handles can go stale if objects are destroyed during the cache window. Always guard with `IsHandleValid()`:

```lua
    for _, shape in ipairs(data.nearbyShapes or {}) do
        if IsHandleValid(shape) then
            -- ... process shape ...
        end
    end
```

**Note:** `FindShapes("tagname", true)` with a tag filter is a hash lookup, NOT a spatial scan — it's cheap and doesn't need throttling. Only throttle unfiltered spatial queries (`QueryAabbBodies`, `QueryAabbShapes`, `FindBodies`).

**Alternative:** Use `QueryClosestPoint()` for single-target queries instead of full scene scans.

---

## Root Cause #4: Server-Side Visual Effects (SpawnParticle/PointLight/SetShapeEmissiveScale)

**Symptom:** Visual effects only visible to host, not to other players.

**Problem:** `SpawnParticle()`, `PointLight()`, and `SetShapeEmissiveScale()` are CLIENT-ONLY effects. Calling them on the server only renders for the host — other clients never see them.

**CORRECTION (2026-03-21):** `PlaySound()` is the EXCEPTION. The base game calls `PlaySound()` directly on the server (confirmed in official snowball.lua, tank.lua, mpcampaign/tools.lua) and it auto-syncs to all clients with positional audio. **Do NOT wrap PlaySound in ClientCall — call it directly on the server.** See `docs/BASE_GAME_MP_PATTERNS.md` Pattern 10.

**Fix:** Move VISUAL effects to client code. Keep PlaySound on server:

```lua
-- RIGHT: PlaySound on server auto-syncs to all clients
function server.tickPlayer(p, dt)
    if firing then
        PlaySound(gunsound, pos)  -- engine replicates to all clients
        Shoot(pos, dir, "bullet", 1, 100, p, "toolid")  -- synced
    end
end

-- RIGHT: Visual effects on client, triggered by state
function client.tickPlayer(p, dt)
    local data = players[p]
    if data.firing and not data.wasFiring then
        SpawnParticle(muzzleFlash, pos)  -- visual only, client-side
        PointLight(pos, 1, 0.8, 0.3, 2)  -- visual only, client-side
    end
    data.wasFiring = data.firing
end
```

**Server does:** `MakeHole`, `Explosion`, `Shoot`, `ApplyPlayerDamage`, `Spawn`, `Delete`, `SetBodyVelocity`, `SpawnFire`, **`PlaySound`**.
**Client does:** `SpawnParticle`, `DrawLine`, `DrawSprite`, `PointLight`, `SetToolTransform`, `SetShapeEmissiveScale`.

> **Note:** `SetShapeEmissiveScale()` is also effectively client-only for visual effects. Server calls only render for the host — other clients never see the emissive glow. Move to client code. (Issue #53)

---

## Root Cause #5: Raw Key Input in Server Code

**Symptom:** Actions only work for the host player. Other players' key presses are silently ignored.

**Problem:** `InputPressed("r", p)` and similar raw key checks with player parameter **fail silently** in v2 MP. They always return `false` for non-host players. Only virtual inputs like `"usetool"` work with the player parameter.

**Fix:** All raw key input must be client-only with `IsPlayerLocal` check + `ServerCall`:

```lua
-- WRONG: Raw key on server (only works for host)
function server.tickPlayer(p, dt)
    if InputPressed("r", p) then  -- SILENT FAIL for non-host
        reload(p)
    end
end

-- RIGHT: Client detects, server executes
function client.tickPlayer(p, dt)
    if not IsPlayerLocal(p) then return end
    if InputPressed("r") then  -- no player param, local only
        ServerCall("server.reload", p)
    end
end

function server.reload(p)
    local data = players[p]
    -- ... do reload ...
end
```

**Virtual inputs that DO work with player param:** `"usetool"`, `"grab"`, `"interact"`, `"jump"`, `"crouch"`, `"up"`, `"down"`, `"left"`, `"right"`.

---

## Root Cause #6: Client-Side QueryShot

**Symptom:** Hit detection inconsistent between players, phantom damage, or no damage at all.

**Problem:** `QueryShot()` detects player hits — but running it on the client means each client computes different hit results based on their local view of player positions (which have network latency). The server is the authority on player positions.

**Fix:** `QueryShot()` + `ApplyPlayerDamage()` should run on the SERVER. Client should use `QueryRaycast()` for visual effects (beam endpoints, impact sparks):

```lua
-- SERVER: Authoritative damage
function server.tickPlayer(p, dt)
    if data.firing then
        local hit, dist, shape, player, hitFactor = QueryShot(startPos, dir, range, radius, p)
        if player ~= 0 then  -- NOT "if player then" (Lua 0 is truthy)
            ApplyPlayerDamage(player, damage * hitFactor, "toolid", p)
        end
        if shape then
            MakeHole(hitPos, r, r, r, true)
        end
    end
end

-- CLIENT: Visual effects only (local player)
function client.tickPlayer(p, dt)
    if not IsPlayerLocal(p) then return end
    if data.firing then
        local hit, dist = QueryRaycast(startPos, dir, range)  -- for visuals
        local endPos = hit and VecAdd(startPos, VecScale(dir, dist)) or VecAdd(startPos, VecScale(dir, range))
        DrawLine(startPos, endPos, 1, 0.5, 0)  -- beam visual
        SpawnParticle(endPos, Vec(0, 0, 0), 0.2)  -- impact spark
    end
end
```

---

## Root Cause #7: Host Double-Processing Shared players[p] Data

**Symptom:** Host player experiences 2x ammo drain, 2x timer speed, 2x reload speed, 2x recoil. Remote clients behave normally. Arrays cause 2x physics (projectiles fly at 2x speed on host).

**Problem:** In v2, `PlayersAdded` in `server.tick` creates `players[p] = createPlayerData()`. On the host, `client.tick`'s guard `if not players[p]` evaluates to true (data already exists from server), so it skips creation. Both `server.tickPlayer(p, dt)` and `client.tickPlayer(p, dt)` then operate on the **same** `data` object. Any field modified in both contexts is processed twice per frame on host.

**Fix:** Gate client-side continuous state writes with `IsPlayerLocal(p)`, or use separate field names for server-owned vs client-owned state:

```lua
-- BROKEN (host gets 2x ammo drain):
function server.tickPlayer(p, dt)
    local data = players[p]
    if data.firing then data.ammo = data.ammo - 1 end
end
function client.tickPlayer(p, dt)
    local data = players[p]
    if data.firing then data.ammo = data.ammo - 1 end  -- ALSO runs on host
end

-- FIX A: Gate client writes
function client.tickPlayer(p, dt)
    local data = players[p]
    if not IsPlayerLocal(p) then return end
    -- Only local player runs client-side updates
    data.clientRecoil = math.max(0, data.clientRecoil - dt * 5)
end

-- FIX B: Separate fields (for arrays like projectiles)
-- Server: data.bulletsInAir (authoritative physics, damage)
-- Client: data.clientTracers (visual-only, local player)
```

**Scope:** 38+ mods affected (extends beyond MEGAGUN and M2A1_Flamethrower from Issues #69/#70). (Issue #72)

---

## Quick Reference: Server vs Client Responsibilities

| Operation | Where | Why |
|-----------|-------|-----|
| `Shoot()` | Server | Authoritative damage + destruction |
| `QueryShot()` + `ApplyPlayerDamage()` | Server | Hit detection must use server positions |
| `MakeHole()`, `Explosion()` | Server | Deterministic destruction, auto-replicated |
| `SetBodyVelocity()`, `ApplyBodyImpulse()` | Server | Physics authority |
| `Spawn()`, `Delete()` | Server | Entity management |
| `SpawnFire()` | Server | Fire propagation |
| `PlaySound()` | **Server** | **Auto-syncs to all clients** (see BASE_GAME_MP_PATTERNS.md Pattern 10) |
| `SpawnParticle()` | Client | Local visual |
| `SetShapeEmissiveScale()` | Client | Visual glow (Issue #53) |
| `DrawLine()`, `DrawSprite()` | Client | Local rendering |
| `PointLight()` | Client | Local lighting |
| `SetToolTransform()` | Client | Local tool position |
| Projectile physics | Client (local only) | Visual only, server does damage |
| `FindShapes()`, `QueryAabb()` | Server (throttled) | Expensive, use sparingly |
| `InputPressed("raw_key")` | Client (local only) | Raw keys fail with player param |
| `InputPressed("usetool", p)` | Server OK | Virtual inputs work with player param |
