# Teardown V2 Multiplayer Sync Patterns

Reference for syncing custom state between server and clients in Teardown v2 mods.

## Available Sync Mechanisms

### 1. Registry Sync (`SetFloat`/`SetBool`/`SetInt`/`SetString` with `sync=true`)

The third parameter enables automatic server→client replication:

```lua
-- Server writes (in server.tick or server.update)
SetFloat("mymod.score", 42, true)        -- float
SetBool("mymod.active", true, true)      -- bool
SetInt("mymod.round", 3, true)           -- int
SetString("mymod.winner", "Alice", true) -- string

-- Client reads (in client.tick)
local score = GetFloat("mymod.score")
local active = GetBool("mymod.active")
```

**Best for:** Simple values, per-player state that needs to cross the server/client boundary.

**Key pattern for per-player state:**
```lua
-- Use player ID in the key to namespace per-player
SetFloat("mymod."..p..".posX", pos[1], true)
SetFloat("mymod."..p..".posY", pos[2], true)
SetFloat("mymod."..p..".posZ", pos[3], true)
```

### 2. RPC Calls (`ServerCall` / `ClientCall`)

For event-driven imperative actions:

```lua
-- Client → Server
ServerCall("server.onPlayerReady")

-- Server → One Client
ClientCall(playerId, "client.showEffect", x, y, z)

-- Server → All Clients (playerId = 0)
ClientCall(0, "client.roundStarted", roundNumber)
```

**Best for:** One-time events (scored, died, round started), camera animations, notifications.

### 3. `shared` Table

A special global Lua table that auto-syncs between server and client contexts:

```lua
shared = {}
shared.timer = 0
shared.scores = {0, 0}
```

**Best for:** Complex structured state, game mode data (scores, timers, flags).

## The Dual-Simulation Problem

In v2, server and client run in separate Lua contexts. Both can run the same logic independently, but they WILL drift because:
- `dt` differs slightly between server/client frames
- `math.random()` uses different seeds
- Accumulated floating-point differences compound via damping/physics
- Mouse/keyboard input is only meaningful for the local player

### Solution: Local Prediction + Server-Synced Remote

**Pattern:** For the local player, run the full simulation client-side for responsiveness. For remote players, read server-synced state and interpolate.

```lua
function client.tickPlayer(p, dt)
    local data = players[p]
    if not data then return end

    if not IsPlayerLocal(p) then
        client.tickRemotePlayer(p, data, dt)
        return
    end

    -- LOCAL: full simulation (responsive, no network latency)
    -- ... compute position, handle input, update state ...
end

function client.tickRemotePlayer(p, data, dt)
    -- REMOTE: read server-synced position, interpolate smoothly
    local syncPos = Vec(
        GetFloat("mymod."..p..".px"),
        GetFloat("mymod."..p..".py"),
        GetFloat("mymod."..p..".pz")
    )

    -- Snap on first encounter, lerp after
    if not data.initialized then
        data.initialized = true
        data.pos = VecCopy(syncPos)
    else
        data.pos = VecLerp(data.pos, syncPos, 0.3)
    end
end
```

### Server-Side Sync Writes

Place sync writes in `server.update()` (after physics) for position/rotation, and in `server.tick()` for input-derived state:

```lua
function server.update(dt)
    for p in Players() do
        local data = players[p]
        if data then
            -- Physics step (authoritative)
            updatePhysics(data, dt)

            -- Sync to clients
            SetFloat("mymod."..p..".px", data.pos[1], true)
            SetFloat("mymod."..p..".py", data.pos[2], true)
            SetFloat("mymod."..p..".pz", data.pos[3], true)
            SetBool("mymod."..p..".firing", data.firing, true)
        end
    end
end
```

## Syncing Quaternion Rotations

Teardown has no `Quat(x,y,z,w)` constructor. Build from components:

```lua
-- Server: write quaternion components
SetFloat("mymod."..p..".rx", data.rot[1], true)
SetFloat("mymod."..p..".ry", data.rot[2], true)
SetFloat("mymod."..p..".rz", data.rot[3], true)
SetFloat("mymod."..p..".rw", data.rot[4], true)

-- Client: reconstruct quaternion
local syncRot = Quat()
syncRot[1] = GetFloat("mymod."..p..".rx")
syncRot[2] = GetFloat("mymod."..p..".ry")
syncRot[3] = GetFloat("mymod."..p..".rz")
syncRot[4] = GetFloat("mymod."..p..".rw")

-- Interpolate
data.rot = QuatSlerp(data.rot, syncRot, 0.3)
```

## Interpolation Tuning

The lerp factor controls smoothness vs responsiveness:
- `0.1` — Very smooth, noticeable lag (good for slow-moving objects)
- `0.3` — Balanced (good default for drones, NPCs)
- `0.5` — Snappy, slight jitter possible (good for fast-moving objects)
- `1.0` — No interpolation, raw sync (jittery)

## Tool Registration Checklist (V2)

Every v2 tool mod MUST have:

```lua
function server.init()
    RegisterTool("toolid", "Tool Name", "MOD/vox/tool.vox")
    SetBool("game.tool.toolid.enabled", true)  -- global fallback
end

function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("toolid", true, p)      -- per-player enable
        SetToolAmmo("toolid", ammoCount, p)    -- per-player ammo (REQUIRED)
    end
    for p in PlayersRemoved() do
        players[p] = nil
    end
    for p in Players() do
        server.tickPlayer(p, dt)
    end
end
```

**Without `SetToolAmmo`, the tool will NOT appear in the toolbar.**

## What's Automatically Synced by the Engine

These do NOT need manual sync:
- Player position/rotation (`GetPlayerTransform(p)`, `GetPlayerPos(p)`)
- Player eye transform (`GetPlayerEyeTransform(p)`)
- Player virtual input (`InputDown("usetool", p)`) — **WARNING:** raw keys like `"rmb"` with player param FAIL SILENTLY (see CLAUDE.md Rule 10). Use `InputPressed("rmb")` on client with `isLocal` check + ServerCall instead.
- Tool body transforms (`GetToolBody(p)`)
- Environment destruction (`MakeHole`, `Explosion` results)
- Player velocity (`GetPlayerVelocity(p)`)

## What NEEDS Manual Sync

These require registry sync or RPC:
- Custom entity positions (drones, NPCs, projectiles)
- Custom state machines (firing modes, charge levels)
- Any accumulated counter (`hoverAngle`, `spinVelocity`)
- Anything derived from `math.random()`
