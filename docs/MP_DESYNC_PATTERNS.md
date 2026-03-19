# Multiplayer Desync & Performance Patterns

> Created 2026-03-18 during MP Desync Fix Sprint. These patterns cause desync, lag, or silent failures in multiplayer.

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

## Root Cause #4: Server-Side PlaySound/SpawnParticle

**Symptom:** Wasted CPU on server, sounds may not play correctly for clients.

**Problem:** `PlaySound()` and `SpawnParticle()` are CLIENT-ONLY effects. Calling them on the server wastes processing and may behave unexpectedly. The server should only handle authoritative state — damage, destruction, spawning.

**Fix:** Move all visual/audio effects to client code:

```lua
-- WRONG: Server playing sounds
function server.tickPlayer(p, dt)
    if firing then
        PlaySound(gunsound, pos)  -- wasted on server
    end
end

-- RIGHT: Client handles effects, triggered by state
function client.tickPlayer(p, dt)
    local data = players[p]
    if data.firing and not data.wasFiring then
        PlaySound(gunsound, pos)
        SpawnParticle(muzzleFlash, pos)
    end
    data.wasFiring = data.firing
end
```

**Server does:** `MakeHole`, `Explosion`, `Shoot`, `ApplyPlayerDamage`, `Spawn`, `Delete`, `SetBodyVelocity`, `SpawnFire`.
**Client does:** `PlaySound`, `SpawnParticle`, `DrawLine`, `DrawSprite`, `PointLight`, `SetToolTransform`, `SetShapeEmissiveScale`.

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

## Quick Reference: Server vs Client Responsibilities

| Operation | Where | Why |
|-----------|-------|-----|
| `Shoot()` | Server | Authoritative damage + destruction |
| `QueryShot()` + `ApplyPlayerDamage()` | Server | Hit detection must use server positions |
| `MakeHole()`, `Explosion()` | Server | Deterministic destruction, auto-replicated |
| `SetBodyVelocity()`, `ApplyBodyImpulse()` | Server | Physics authority |
| `Spawn()`, `Delete()` | Server | Entity management |
| `SpawnFire()` | Server | Fire propagation |
| `PlaySound()` | Client | Local audio |
| `SpawnParticle()` | Client | Local visual |
| `SetShapeEmissiveScale()` | Client | Visual glow (Issue #53) |
| `DrawLine()`, `DrawSprite()` | Client | Local rendering |
| `PointLight()` | Client | Local lighting |
| `SetToolTransform()` | Client | Local tool position |
| Projectile physics | Client (local only) | Visual only, server does damage |
| `FindShapes()`, `QueryAabb()` | Server (throttled) | Expensive, use sparingly |
| `InputPressed("raw_key")` | Client (local only) | Raw keys fail with player param |
| `InputPressed("usetool", p)` | Server OK | Virtual inputs work with player param |
