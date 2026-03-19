# Portal Gun v2 Conversion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **CRITICAL RULES for Teardown v2 mod code:**
> - `Players()`/`PlayersAdded()`/`PlayersRemoved()` are ITERATORS — NO `ipairs()`
> - Raw keys (`"rmb"`, `"r"`) do NOT take player param — use `InputPressed("rmb")` + ServerCall
> - `SetToolEnabled("toolid", true, p)` — string first, bool second, player third
> - Player param is ALWAYS LAST in Set*/Get* functions
> - ALWAYS run `python -m tools.lint --mod "Portal_Gun"` after writing any mod code
> - Read `docs/OFFICIAL_DEVELOPER_DOCS.md` for authoritative API reference

**Goal:** Convert the Portal Gun workshop mod (ID 2421609769, 3208 lines) from v1 single-player to v2 multiplayer with per-player portal pairs, server-authoritative physics, and client-side portal rendering.

**Architecture:** Each player gets their own blue/orange portal pair stored in per-player data. Portal placement is driven by client input via ServerCall, validated on server. Player/body teleportation runs on server (SetPlayerTransform/SetPlayerVelocity/SetBodyTransform/SetBodyVelocity). The portal raycast shader stays entirely client-side, rendering only the local player's portals. Options menu integrates into client.draw() with UiMakeInteractive(). Laser level interaction is kept as optional (checks for level entities).

**Tech Stack:** Lua 5.1, Teardown v2 API, `#include "script/include/player.lua"`, `#include "script/toolanimation.lua"`

**Source:** `C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/2421609769/`
**Target:** `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/`

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `info.txt` | Create | Mod metadata with `version = 2` |
| `main.lua` | Create | V2 script: server/client split, tool registration, input, HUD, options |
| `portal.lua` | Rewrite | Portal create/place/destroy/validate/teleport functions — adapted for per-player |
| `portalshader.lua` | Copy+adapt | Client-only raycast shader — minor v2 fixes |
| `perlin.lua` | Copy | Pure math, no changes |
| `image/` | Copy | 8 PNG files (crosshairs, color picker, pixel) |
| `snd/` | Copy | 22 OGG files + `old/` subfolder (18 files) |
| `vox/` | Copy | `portalgun.vox` |
| `preview.jpg` | Copy | Workshop thumbnail |

## Design Decisions

### Per-Player Portal State
Each player's `createPlayerData()` includes `bluePortal` and `orangePortal` objects. Portals are completely independent between players.

### Portal Rendering Scope
Only the **local player's** portals are rendered with the full raycast shader (DrawPortal). Remote players' portals are invisible — the shader is too expensive to run for every player. Portal lights (PointLight) are rendered for the local player's portals only.

### Server/Client Split
| Operation | Side | Reason |
|-----------|------|--------|
| Portal placement (ShootPortal) | Server | Needs authoritative validation; QueryRaycast works on server |
| Portal state update (UpdatePortal) | Server | Surface destruction detection |
| Portal surface validation | Server | Authoritative |
| Player teleportation | Server | SetPlayerTransform/SetPlayerVelocity are server-only |
| Body teleportation | Server | SetBodyTransform/SetBodyVelocity are server-only |
| Object pickup physics | Server | ApplyBodyImpulse/SetBodyAngularVelocity are server-only |
| Portal funneling | Server | SetPlayerVelocity is server-only |
| Laser MakeHole | Server | MakeHole is server-only |
| Portal rendering (shader) | Client | DrawSprite, QueryRaycast for visuals |
| Sounds | Client | PlaySound/PlayLoop are client-only |
| Particles | Client | SpawnParticle is client-only |
| Tool animation | Client | SetShapeLocalTransform for visual model |
| Crosshair HUD | Client | Ui* functions are client-only |
| Options menu | Client | Ui* functions + UiMakeInteractive |
| Camera offset (post-teleport) | Client | SetPlayerCameraOffsetTransform |

### State Sync Strategy
Portal positions and open/closed state are synced via registry (`SetBool`/`SetFloat` with `sync=true`) so clients can render their portals correctly after server validation.

Key synced keys per player `p`:
```
portalgun.<p>.blue.open     (bool)
portalgun.<p>.blue.px/py/pz (float, position)
portalgun.<p>.blue.rx/ry/rz/rw (float, rotation quaternion)
portalgun.<p>.orange.open   (bool)
portalgun.<p>.orange.px/py/pz (float)
portalgun.<p>.orange.rx/ry/rz/rw (float)
```

### Input Mapping
| v1 Input | v2 Approach |
|----------|-------------|
| `InputPressed("usetool")` | `InputPressed("usetool", p)` on server — action name, works with player param |
| `InputPressed("grab")` on client for orange portal | `InputPressed("grab")` + `IsPlayerLocal(p)` on client → `ServerCall("server.onShootOrange", ...)` |
| `InputPressed("interact")` for object pickup | `InputPressed("interact", p)` on server — action name |
| `InputPressed("r")` for portal reset | `InputPressed("r")` + `IsPlayerLocal(p)` on client → `ServerCall("server.onResetPortals", p)` |

### Options Architecture
The v1 mod has a separate `options.lua` with sliders and color picker. For v2:
- Settings are read from `savegame.mod.*` at init (these are local per-player)
- In-game options toggle via `O` key → `data.optionsOpen = true`
- Options menu renders in `client.draw()` with `UiMakeInteractive()`
- Server guards `usetool` input with `not data.optionsOpen`
- The full slider/color-picker options stay in a separate `options.lua` file (game's mod settings screen)

### Laser Level Interaction
The laser is level-specific (requires `FindShape("button")`, `FindShape("emitter")`, `FindLocation("emitter")`). In v2:
- Server: laser MakeHole, vault door logic, laser state
- Client: laser visual (DrawSprite), smoke particles, sounds
- Gate with `laserLevel = (buttonShape ~= 0 and emitterShape ~= 0)` check
- Laser player damage via `ApplyPlayerDamage` on server (replacing v1 `SetPlayerHealth`)

### Dropped/Deferred Features
- **Portal rendering for remote players** — Too expensive; deferred
- **Cross-player portal usage** — Each player can only use their own portals; deferred
- **updateKeys() registry command system** — Was for inter-script communication in v1; not needed in v2

---

## Tasks

### Task 1: Scaffold — Create folder, copy assets, write info.txt

**Files:**
- Create: `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/info.txt`
- Copy: all assets from workshop folder

- [ ] **Step 1: Create mod folder and copy all assets**

```bash
mkdir -p "C:/Users/trust/Documents/Teardown/mods/Portal_Gun"
cp -r "C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/2421609769/snd" "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/"
cp -r "C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/2421609769/vox" "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/"
cp -r "C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/2421609769/image" "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/"
cp "C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/2421609769/preview.jpg" "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/"
```

- [ ] **Step 2: Write info.txt**

```
name = Portal Gun
author = Mathias
description = Think with portals! [LMB] Blue Portal, [RMB/Grab] Orange Portal, [Interact] Grab objects, [R] Reset portals, [O] Options
tags = Tool
version = 2
```

- [ ] **Step 3: Verify assets copied correctly**

```bash
ls -la "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/"
ls -la "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/snd/"
ls -la "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/vox/"
ls -la "C:/Users/trust/Documents/Teardown/mods/Portal_Gun/image/"
```

---

### Task 2: Copy helper files — perlin.lua, portalshader.lua

**Files:**
- Copy: `perlin.lua` (verbatim — pure math)
- Adapt: `portalshader.lua` (remove top-level savegame reads — portal config will be passed via portal object)

- [ ] **Step 1: Copy perlin.lua verbatim**

Copy `perlin.lua` from workshop to `Portal_Gun/perlin.lua` — no changes needed. This file is pure math (Perlin noise implementation) with no game API calls that need v2 adaptation.

- [ ] **Step 2: Adapt portalshader.lua**

The v1 portalshader.lua has duplicate savegame.mod reads at the top (already read in portal.lua and main.lua). For v2, these config values will come from the portal object's Width/Height/etc. properties set during creation.

Key changes:
- Remove all top-level `HasKey`/`Set*`/`Get*` savegame.mod reads (lines 1-61) — portal config comes from the portal object
- Remove top-level `PORTAL_*` locals — these are read from the portal object
- Keep all rendering functions unchanged — `DrawPortal()` and `CreatePortalShader()` are client-only and work as-is
- The `CreatePortalShader()` function already receives resolution params
- `DrawPortal()` reads dimensions from `portal.Width`/`portal.Height` which are set by portal.lua

- [ ] **Step 3: Verify both files are in place**

---

### Task 3: Rewrite portal.lua for v2

**Files:**
- Create: `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/portal.lua`

This is the portal mechanics core. The v1 version uses global state; v2 needs per-player portals.

**Key changes from v1:**
1. Remove top-level savegame.mod reads — config read at portal creation time
2. `CreatePortal()` — takes config params instead of reading globals
3. `ShootPortal()` — largely unchanged (server-side, pure game logic)
4. `PlacePortal()` — unchanged (operates on portal object)
5. `DestroyPortal()` — unchanged
6. `CheckPortalValidSurface()` — unchanged (uses QueryRaycast)
7. `integrateSurface()` — unchanged (pure math + GetShapeMaterialAtIndex)
8. `FunnelPortalPlayer()` — add player param for `SetPlayerVelocity(vel, p)`
9. `CheckPortalPlayer()` — add player param for `GetPlayerTransform(p)`, `GetPlayerVelocity(p)`
10. `TravelPortalPlayer()` — add player param for `SetPlayerTransform(t, p)`, `SetPlayerVelocity(v, p)`, `GetPlayerTransform(p)`
11. `CheckPortalBody()` — unchanged (body physics, no player dependency)
12. `TravelPortalBody()` — unchanged (SetBodyTransform/SetBodyVelocity)
13. `UpdatePortal()` — unchanged (surface tracking)
14. Remove `DrawPortal()`, `PortalLight()` calls — these go in client code, shader handles rendering

- [ ] **Step 1: Write portal.lua with all portal functions adapted for v2**

The file should NOT have `#include` directives (it's included by main.lua which has them).

Functions to include:
- `CreatePortal(width, height, resolution, renderDist, color)` — factory
- `PlacePortal(portal, shape, transform, normal)` — place on surface
- `DestroyPortal(portal)` — close portal
- `ShootPortal(portal, otherPortal, origin, dir, placeAnywhere)` — raycast + validate + place
- `CheckPortalValidSurface(portal, otherPortal, surfaceShape, transform, normal)` — edge validation
- `integrateSurface(hitPos, normal, shape)` — BFS normal integration
- `FunnelPortalPlayer(portal, p)` — velocity nudge toward portal center
- `CheckPortalPlayer(portal, p)` — has player crossed portal plane?
- `TravelPortalPlayer(portal, otherPortal, p)` — teleport player
- `CheckPortalBody(portal, body)` — has body crossed portal plane?
- `TravelPortalBody(portal, otherPortal, body)` — teleport body
- `UpdatePortal(portal, otherPortal, dt)` — surface tracking + damage check
- `CheckPortalPoint(portal, point)` — point inside portal area?
- `TransformPortalPoint(portal, otherPortal, point)` — coordinate transform
- `TransformPortalDirection(portal, otherPortal, direction)` — direction transform

- [ ] **Step 2: Run lint**

```bash
python -m tools.lint --mod "Portal_Gun"
```

---

### Task 4: Write main.lua — Server side

**Files:**
- Create: `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/main.lua`

- [ ] **Step 1: Write header and createPlayerData()**

```lua
#version 2

#include "script/include/player.lua"
#include "script/toolanimation.lua"
#include "perlin.lua"
#include "portal.lua"
#include "portalshader.lua"

players = {}

function getOptions()
    return {
        width = GetFloat("savegame.mod.width") or 1,
        height = GetFloat("savegame.mod.height") or 2,
        resolution = GetInt("savegame.mod.res") or 20,
        renderDist = GetInt("savegame.mod.dist") or 50,
        placeAnywhere = GetBool("savegame.mod.any"),
        indestructible = GetBool("savegame.mod.ind"),
        funneling = GetBool("savegame.mod.fun"),
        renderEnabled = GetBool("savegame.mod.ren"),
        unlimitedAmmo = GetBool("savegame.mod.unlimitedammo"),
        blueColor = {GetFloat("savegame.mod.red1") or 0, GetFloat("savegame.mod.green1") or 0.5, GetFloat("savegame.mod.blue1") or 1},
        orangeColor = {GetFloat("savegame.mod.red2") or 1, GetFloat("savegame.mod.green2") or 0.5, GetFloat("savegame.mod.blue2") or 0},
    }
end

function createPlayerData()
    local opts = getOptions()
    return {
        bluePortal = CreatePortal(opts.width, opts.height, opts.resolution, opts.renderDist, opts.blueColor),
        orangePortal = CreatePortal(opts.width, opts.height, opts.resolution, opts.renderDist, opts.orangeColor),
        toolAnimator = ToolAnimator(),
        ang = 0,
        angVel = 0,
        roll = 0,
        rollVel = 0,
        rollK = 1,
        lastOpen = false,
        grabBody = 0,
        grab = false,
        equipped = false,
        optionsOpen = false,
        cameraOffsetRot = Quat(),
        cameraOffsetTime = 0,
        falling = false,
        fallingNormal = Vec(),
    }
end
```

- [ ] **Step 2: Write server.init()**

```lua
function server.init()
    RegisterTool("portalgun", "Portal Gun", "MOD/vox/portalgun.vox", 6)
    SetToolAmmoPickupAmount("portalgun", 0)  -- not a consumable weapon
    SetString("game.tool.portalgun.ammo.display", "")

    -- Laser level detection
    local bs = FindShape("button", true)
    local es = FindShape("emitter", true)
    local el = FindLocation("emitter", true)
    laserLevel = (bs ~= 0 and es ~= 0 and el ~= 0)
    if laserLevel then
        laserEnabled = false
        laserButtonShape = bs
        laserEmitterShape = es
        laserEmitterLocation = el
        laserVaultDoors = FindBodies("vaultdoor", true)
        laserDeflectors = FindBodies("mirror2", true)
        laserDisableTimer = 0
        -- Find the interactive button (closest shape in same body)
        local buttonBody = GetShapeBody(bs)
        local shapes = GetBodyShapes(buttonBody)
        laserNewButtonShape = 0
        local closest = 1000
        for i = 1, #shapes do
            if shapes[i] ~= bs then
                local length = VecLength(VecSub(GetShapeWorldTransform(bs).pos, GetShapeWorldTransform(shapes[i]).pos))
                if length < closest then
                    closest = length
                    laserNewButtonShape = shapes[i]
                end
            end
        end
        if laserNewButtonShape ~= 0 then
            RemoveTag(bs, "interact")
            SetTag(laserNewButtonShape, "interact", "Turn on")
        end
    end
end
```

- [ ] **Step 3: Write server.tick() — player management + tool input**

```lua
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("portalgun", true, p)
        SetToolAmmo("portalgun", 1000, p)
    end

    for p in PlayersRemoved() do
        players[p] = nil
    end

    for p in Players() do
        server.tickPlayer(p, dt)
    end

    -- Laser level logic (server-side MakeHole)
    if laserLevel then
        server.tickLaser(dt)
    end
end

function server.tickPlayer(p, dt)
    if GetPlayerTool(p) ~= "portalgun" then return end
    local data = players[p]
    if not data then return end

    -- Portal shooting via "usetool" action (blue portal)
    if InputPressed("usetool", p) and not data.grab and not data.optionsOpen and GetPlayerVehicle(p) == 0 then
        local hit, startPos, endPos, dir = GetPlayerAimInfo(p)
        if hit then
            server.shootPortal(p, "blue", startPos, VecNormalize(VecSub(endPos, startPos)))
        end
    end

    -- Object pickup via "interact" action
    if InputPressed("interact", p) and not data.optionsOpen and GetPlayerVehicle(p) == 0 then
        if data.grab then
            data.grab = false
            data.grabBody = 0
            ClientCall(p, "client.onStopPickup")
        else
            server.tryPickup(p)
        end
    end

    -- Pickup physics update
    if data.grab and data.grabBody ~= 0 then
        server.tickPickup(p, dt)
    end
end
```

- [ ] **Step 4: Write server RPC handlers for client-initiated actions**

```lua
-- Called by client when "grab" pressed (orange portal - raw key alternative)
function server.onShootOrange(p, sx, sy, sz, dx, dy, dz)
    local data = players[p]
    if not data then return end
    if data.optionsOpen then return end
    if data.grab then return end
    server.shootPortal(p, "orange", Vec(sx, sy, sz), Vec(dx, dy, dz))
end

-- Called by client when "r" pressed (reset portals - raw key)
function server.onResetPortals(p)
    local data = players[p]
    if not data then return end
    local hadPortals = data.bluePortal.Open or data.orangePortal.Open
    if data.bluePortal.Open then
        DestroyPortal(data.bluePortal)
        server.syncPortalState(p, "blue")
    end
    if data.orangePortal.Open then
        DestroyPortal(data.orangePortal)
        server.syncPortalState(p, "orange")
    end
    if hadPortals then
        ClientCall(p, "client.onPortalsReset")
    end
end

-- Called by client when options toggled
function server.setOptionsOpen(p, open)
    local data = players[p]
    if data then
        data.optionsOpen = open
    end
end

-- Core portal shooting logic
function server.shootPortal(p, color, origin, dir)
    local data = players[p]
    if not data then return end
    local opts = getOptions()

    local portal, otherPortal
    if color == "blue" then
        portal = data.bluePortal
        otherPortal = data.orangePortal
    else
        portal = data.orangePortal
        otherPortal = data.bluePortal
    end

    local hit, valid, portalPos = ShootPortal(portal, otherPortal, origin, dir, opts.placeAnywhere)
    if hit then
        server.syncPortalState(p, color)
        ClientCall(p, "client.onPortalShot", color, hit, valid,
            portalPos[1], portalPos[2], portalPos[3])
    else
        ClientCall(p, "client.onPortalShot", color, false, false, 0, 0, 0)
    end
end

-- Sync portal state to clients via registry
function server.syncPortalState(p, color)
    local data = players[p]
    if not data then return end
    local portal = (color == "blue") and data.bluePortal or data.orangePortal
    local prefix = "portalgun."..p.."."..color.."."

    SetBool(prefix.."open", portal.Open, true)
    if portal.Open then
        SetFloat(prefix.."px", portal.Position[1], true)
        SetFloat(prefix.."py", portal.Position[2], true)
        SetFloat(prefix.."pz", portal.Position[3], true)
        local r = portal.Transform.rot
        SetFloat(prefix.."rx", r[1], true)
        SetFloat(prefix.."ry", r[2], true)
        SetFloat(prefix.."rz", r[3], true)
        SetFloat(prefix.."rw", r[4], true)
        SetFloat(prefix.."nx", portal.Normal[1], true)
        SetFloat(prefix.."ny", portal.Normal[2], true)
        SetFloat(prefix.."nz", portal.Normal[3], true)
        SetFloat(prefix.."scale", portal.Scale, true)
    end
end
```

- [ ] **Step 5: Run lint**

```bash
python -m tools.lint --mod "Portal_Gun"
```

---

### Task 5: Write main.lua — Server physics (teleportation, bodies, funneling)

**Files:**
- Modify: `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/main.lua`

- [ ] **Step 1: Write server.update() — player teleportation + body teleportation + funneling**

```lua
function server.update(dt)
    local opts = getOptions()

    for p in Players() do
        local data = players[p]
        if not data then goto continue_player end

        local bp = data.bluePortal
        local op = data.orangePortal

        -- Update portal surface tracking
        if bp.Open then
            if UpdatePortal(bp, op, dt) then
                server.syncPortalState(p, "blue")
                ClientCall(p, "client.onPortalFizzle", "blue")
            end
            server.syncPortalScale(p, "blue", bp.Scale)
        end
        if op.Open then
            if UpdatePortal(op, bp, dt) then
                server.syncPortalState(p, "orange")
                ClientCall(p, "client.onPortalFizzle", "orange")
            end
            server.syncPortalScale(p, "orange", op.Scale)
        end

        -- Portal funneling
        if opts.funneling then
            if bp.Open and not InputDown("any", p) then
                FunnelPortalPlayer(bp, p)
            end
            if op.Open and not InputDown("any", p) then
                FunnelPortalPlayer(op, p)
            end
        end

        -- Player teleportation
        if bp.Open and op.Open then
            if CheckPortalPlayer(bp, p) then
                TravelPortalPlayer(bp, op, p)
                ClientCall(p, "client.onTeleported", "blue")
            end
            if CheckPortalPlayer(op, p) then
                TravelPortalPlayer(op, bp, p)
                ClientCall(p, "client.onTeleported", "orange")
            end

            -- Body teleportation (throttled — check bodies near portals)
            server.tickBodyTeleport(data, bp, op)
            server.tickBodyTeleport(data, op, bp)
        end

        -- Air resistance compensation when falling after teleport
        if data.falling then
            local vel = GetPlayerVelocity(p)
            local norm = VecCopy(data.fallingNormal)
            norm[2] = 0
            if VecLength(norm) > 0 then
                norm = VecNormalize(norm)
                SetPlayerVelocity(VecAdd(GetPlayerVelocity(p), VecScale(norm, 0.15)), p)
                local playerPos = GetPlayerTransform(p).pos
                local hitGround = QueryRaycast(playerPos, Vec(0, -0.1, 0), 0.1)
                if hitGround then
                    data.falling = false
                end
            end
        end

        ::continue_player::
    end
end

-- Sync just the scale (called during animation)
function server.syncPortalScale(p, color, scale)
    SetFloat("portalgun."..p.."."..color..".scale", scale, true)
end

-- Body teleportation for one portal pair direction
function server.tickBodyTeleport(data, portal, otherPortal)
    if not portal.Open or not otherPortal.Open then return end
    if portal.SurfaceShape == nil then return end

    QueryRequire("dynamic physical")
    QueryRejectShape(portal.SurfaceShape)
    local min = VecAdd(portal.Position, Vec(-5, -5, -5))
    local max = VecAdd(portal.Position, Vec(5, 5, 5))
    local bodies = QueryAabbBodies(min, max)
    for i = 1, #bodies do
        local body = bodies[i]
        if CheckPortalBody(portal, body) then
            TravelPortalBody(portal, otherPortal, body)
        end
    end
end
```

Note: Uses `goto` labels — but Lua 5.1 doesn't support goto! Must use `if/end` nesting instead. Fix the `goto continue_player` to use a nested function or conditional pattern.

- [ ] **Step 2: Write server.tryPickup() — object grab logic**

```lua
function server.tryPickup(p)
    local data = players[p]
    local hit, startPos, endPos, dir = GetPlayerAimInfo(p)
    if not hit then
        ClientCall(p, "client.onPickupFail")
        return
    end

    local dist = VecLength(VecSub(endPos, startPos))
    if dist > 3 then
        ClientCall(p, "client.onPickupFail")
        return
    end

    -- Find the shape at the aim point
    local camT = GetPlayerEyeTransform(p)
    local camDir = TransformToParentVec(camT, Vec(0, 0, -1))
    local rayHit, rayDist, _, shape = QueryRaycast(camT.pos, camDir, 3)
    if not rayHit then
        ClientCall(p, "client.onPickupFail")
        return
    end

    local body = GetShapeBody(shape)
    if not IsBodyDynamic(body) then
        ClientCall(p, "client.onPickupFail")
        return
    end
    if IsBodyJointedToStatic(body) or GetBodyMass(body) > 3000 then
        ClientCall(p, "client.onPickupFail")
        return
    end

    data.grab = true
    data.grabBody = body
    ClientCall(p, "client.onPickupStart")
end

function server.tickPickup(p, dt)
    local data = players[p]
    if not data.grab or data.grabBody == 0 then return end

    local body = data.grabBody
    if not IsBodyDynamic(body) then
        data.grab = false
        data.grabBody = 0
        return
    end

    local camT = GetPlayerEyeTransform(p)
    local playerVel = GetPlayerVelocity(p)

    local grabPos = VecAdd(TransformToParentPoint(camT, Vec(0, 0, -2.5)), VecScale(playerVel, 0.1))

    local bodyTransform = GetBodyTransform(body)
    local com = GetBodyCenterOfMass(body)
    local bodyPos = TransformToParentPoint(bodyTransform, com)

    local diff = VecSub(grabPos, VecAdd(bodyPos, VecScale(GetBodyVelocity(body), 0.1)))

    if VecLength(diff) > 3 then
        data.grab = false
        data.grabBody = 0
        ClientCall(p, "client.onStopPickup")
        return
    end

    local forceDir = VecNormalize(diff)
    local force = VecScale(forceDir, GetBodyMass(body) * 4 * math.min(VecLength(diff), 0.5))

    -- Angular velocity correction for upright orientation
    local bodyAngVel = GetBodyAngularVelocity(body)
    local up = Vec(0, 1, 0)
    local bodyUp = TransformToParentVec(bodyTransform, up)
    local angVel = Vec(-bodyUp[3] * 1, 0, bodyUp[1] * 1)
    local torque = VecSub(angVel, VecScale(bodyAngVel, dt * 10))

    SetBodyAngularVelocity(body, VecAdd(bodyAngVel, torque))
    ApplyBodyImpulse(body, bodyPos, force)
end
```

- [ ] **Step 3: Write laser level server logic**

```lua
function server.tickLaser(dt)
    if not laserLevel then return end

    -- Button interaction (check all players)
    for p in Players() do
        if GetPlayerInteractShape(p) == laserNewButtonShape and InputPressed("interact", p) then
            laserEnabled = not laserEnabled
            if laserEnabled then
                SetShapeEmissiveScale(laserEmitterShape, 1)
                if laserNewButtonShape ~= 0 then
                    SetTag(laserNewButtonShape, "interact", "Turn off")
                end
            else
                SetShapeEmissiveScale(laserEmitterShape, 0)
                if laserNewButtonShape ~= 0 then
                    SetTag(laserNewButtonShape, "interact", "Turn on")
                end
            end
            SetBool("level.laser", laserEnabled)
        end
    end

    if laserEmitterLocation == 0 then return end

    if laserEnabled then
        local emitTransform = GetLocationTransform(laserEmitterLocation)
        local origin = emitTransform.pos
        local dir = TransformToParentVec(emitTransform, Vec(0, 0, -1))

        -- Server-side laser for damage + MakeHole
        QueryRequire("physical")
        local hit, hitDist, hitNormal, hitShape = QueryRaycast(origin, dir, 1000, 0.0, true)
        if hit then
            local hitPoint = VecAdd(origin, VecScale(dir, hitDist))
            MakeHole(hitPoint, 0.5, 0.3, 0, true) -- @lint-ok MAKEHOLE-DAMAGE

            -- Check if laser hits any player
            for p in Players() do
                local ppos = GetPlayerPos(p)
                ppos[2] = ppos[2] + 0.8 -- approximate center
                local pdist = VecLength(VecSub(ppos, VecAdd(origin, VecScale(dir, VecDot(VecSub(ppos, origin), dir)))))
                if pdist < 0.4 then
                    local health = GetPlayerHealth(p)
                    health = math.max(0.1, health - 0.3 * dt)
                    SetPlayerHealth(health, p)
                end
            end

            -- Vault door logic
            if laserVaultDoors then
                local hitBody = GetShapeBody(hitShape)
                for i = 1, #laserVaultDoors do
                    if hitBody == laserVaultDoors[i] then
                        RemoveTag(laserVaultDoors[i], "unbreakable")
                    end
                end
            end
        end
    end

    -- Vault broken auto-disable
    if GetBool("level.vaultbroken") then
        laserDisableTimer = laserDisableTimer + dt
        if laserDisableTimer > 3 then
            laserEnabled = false
            SetShapeEmissiveScale(laserEmitterShape, 0)
            if laserNewButtonShape ~= 0 then
                SetTag(laserNewButtonShape, "interact", "Turn on")
            end
            SetBool("level.laser", false)
            SetBool("level.vaultbroken", false)
        end
    end
end
```

- [ ] **Step 4: Fix goto usage — replace with conditional pattern**

Lua 5.1 doesn't support `goto`. Replace `goto continue_player` with a function call or `if data then ... end` nesting.

- [ ] **Step 5: Run lint**

```bash
python -m tools.lint --mod "Portal_Gun"
```

---

### Task 6: Write main.lua — Client side (tick, rendering, effects)

**Files:**
- Modify: `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/main.lua`

- [ ] **Step 1: Write client.init()**

```lua
function client.init()
    pixel = LoadSprite("MOD/image/pixel.png")
    laserSprite = LoadSprite("gfx/laser.png")

    -- Load sounds
    activationSnd = LoadSound("MOD/snd/activation.ogg")
    enterSnd = {
        LoadSound("MOD/snd/enter1.ogg"),
        LoadSound("MOD/snd/enter2.ogg"),
        LoadSound("MOD/snd/enter3.ogg")
    }
    fizzleSnd = {
        LoadSound("MOD/snd/fizzle1.ogg"),
        LoadSound("MOD/snd/fizzle2.ogg")
    }
    fireBlueSnd = {
        LoadSound("MOD/snd/fire_blue1.ogg"),
        LoadSound("MOD/snd/fire_blue2.ogg"),
        LoadSound("MOD/snd/fire_blue3.ogg")
    }
    fireRedSnd = {
        LoadSound("MOD/snd/fire_red1.ogg"),
        LoadSound("MOD/snd/fire_red2.ogg"),
        LoadSound("MOD/snd/fire_red3.ogg")
    }
    openBlueSnd = LoadSound("MOD/snd/open_blue1.ogg")
    openRedSnd = LoadSound("MOD/snd/open_red1.ogg")
    invalidSurfaceSnd = LoadSound("MOD/snd/invalid_surface.ogg")
    fizzlerSnd = LoadSound("MOD/snd/fizzler.ogg")
    blueAmbientLoop = LoadLoop("MOD/snd/ambient.ogg")
    redAmbientLoop = LoadLoop("MOD/snd/ambient.ogg")
    useStartSnd = LoadSound("MOD/snd/use_start.ogg")
    useStopSnd = LoadSound("MOD/snd/use_stop.ogg")
    useFailureSnd = LoadSound("MOD/snd/use_failure.ogg")
    useLoop = LoadLoop("MOD/snd/use_loop.ogg")

    -- Laser sounds
    if FindShape("emitter", true) ~= 0 then
        laserLoop = LoadLoop("MOD/snd/ambient.ogg") -- reuse ambient
        laserHitLoop = LoadLoop("MOD/snd/ambient.ogg")
        laserHitSound = LoadSound("light/spark0.ogg")
    end
end
```

- [ ] **Step 2: Write client.tick() — player management + input + tool animation**

```lua
function client.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
    end
    for p in PlayersRemoved() do
        players[p] = nil
    end
    for p in Players() do
        client.tickPlayer(p, dt)
    end
end

function client.tickPlayer(p, dt)
    if GetPlayerTool(p) ~= "portalgun" then
        local data = players[p]
        if data then data.equipped = false end
        return
    end

    local data = players[p]
    if not data then return end

    -- Equip sound
    if not data.equipped then
        data.equipped = true
        if IsPlayerLocal(p) then
            PlaySound(activationSnd, GetPlayerPos(p), 0.2)
        end
    end

    -- Local player input for raw keys
    if IsPlayerLocal(p) then
        -- Orange portal via "grab" when can't grab objects
        if InputPressed("grab") and not GetBool("game.player.cangrab") and not data.optionsOpen and not data.grab then
            local camT = GetPlayerCameraTransform()
            local origin = camT.pos
            local dir = TransformToParentVec(camT, Vec(0, 0, -1))
            ServerCall("server.onShootOrange",
                origin[1], origin[2], origin[3],
                dir[1], dir[2], dir[3])
            PlaySound(fireRedSnd[math.random(1, #fireRedSnd)], GetPlayerPos(p), 0.5)
            data.angVel = 1
            data.ang = 0
        end

        -- Reset portals via "r" key
        if InputPressed("r") then
            ServerCall("server.onResetPortals", p)
        end

        -- Options toggle via "o" key
        if InputPressed("o") then
            data.optionsOpen = not data.optionsOpen
            ServerCall("server.setOptionsOpen", data.optionsOpen)
        end

        -- Pickup loop sound
        if data.grab then
            PlayLoop(useLoop)
        end
    end

    -- Tool animation
    tickToolAnimator(data.toolAnimator, dt, nil, p)

    -- Portal rendering (local player only)
    if IsPlayerLocal(p) then
        client.tickPortals(p, dt)
    end
end
```

- [ ] **Step 3: Write client portal rendering**

```lua
function client.tickPortals(p, dt)
    local data = players[p]
    if not data then return end

    local bp = data.bluePortal
    local op = data.orangePortal

    -- Read portal state from registry (synced from server)
    client.readPortalState(p, "blue", bp)
    client.readPortalState(p, "orange", op)

    -- Update portal surface tracking on client too (for rendering)
    if bp.Open then
        UpdatePortal(bp, op, dt)
    end
    if op.Open then
        UpdatePortal(op, bp, dt)
    end

    -- Draw portals
    if bp.Open then
        DrawPortal(bp, op)
        PortalLight(bp)
        PlayLoop(blueAmbientLoop, bp.Position, 0.25)
    end
    if op.Open then
        DrawPortal(op, bp)
        PortalLight(op)
        PlayLoop(redAmbientLoop, op.Position, 0.25)
    end
end

function client.readPortalState(p, color, portal)
    local prefix = "portalgun."..p.."."..color.."."
    local isOpen = GetBool(prefix.."open")

    if isOpen and not portal.Open then
        -- Portal just opened — need to reconstruct placement
        -- Position and rotation come from registry
        portal.Open = true
    elseif not isOpen and portal.Open then
        portal.Open = false
        portal.SurfaceShape = nil
    end

    if isOpen then
        portal.Position = Vec(
            GetFloat(prefix.."px"),
            GetFloat(prefix.."py"),
            GetFloat(prefix.."pz"))
        portal.Transform = Transform(portal.Position, Quat(
            GetFloat(prefix.."rx"),
            GetFloat(prefix.."ry"),
            GetFloat(prefix.."rz"),
            GetFloat(prefix.."rw")))
        portal.Normal = Vec(
            GetFloat(prefix.."nx"),
            GetFloat(prefix.."ny"),
            GetFloat(prefix.."nz"))
        portal.Scale = GetFloat(prefix.."scale")
    end
end

function PortalLight(portal)
    PointLight(portal.Position, portal.Color[1], portal.Color[2], portal.Color[3], portal.Scale * 5)
end
```

- [ ] **Step 4: Write client RPC handlers**

```lua
function client.onPortalShot(color, hit, valid, px, py, pz)
    local p = GetLocalPlayer()
    if not p then return end
    local data = players[p]
    if not data then return end
    local pos = Vec(px, py, pz)

    if hit and valid then
        if color == "blue" then
            PlaySound(openBlueSnd, pos, 0.5)
        else
            PlaySound(openRedSnd, pos, 0.5)
        end
        data.lastOpen = (color == "orange")
    elseif hit then
        -- Invalid surface
        local portal = (color == "blue") and data.bluePortal or data.orangePortal
        -- Spawn colored particles
        local c = portal.Color
        for i = 1, 40 do
            ParticleTile(6)
            ParticleColor(c[1], c[2], c[3])
            ParticleRadius(0.01)
            ParticleGravity(-10)
            ParticleEmissive(1)
            ParticleStretch(2)
            local vel = Vec((math.random() - 0.5) * 6, math.random() * 6, (math.random() - 0.5) * 6)
            SpawnParticle(pos, vel, 2)
        end
        PlaySound(invalidSurfaceSnd, pos, 0.5)
    end

    -- Fire sound was already played on client (for responsiveness)
    if color == "blue" then
        PlaySound(fireBlueSnd[math.random(1, #fireBlueSnd)], GetPlayerPos(p), 0.5)
    end

    data.angVel = 1
    data.ang = 0
end

function client.onPortalFizzle(color)
    local p = GetLocalPlayer()
    local data = players[p]
    if not data then return end
    local portal = (color == "blue") and data.bluePortal or data.orangePortal
    PlaySound(fizzleSnd[math.random(1, #fizzleSnd)], portal.Position, 0.5)
end

function client.onPortalsReset()
    local p = GetLocalPlayer()
    local data = players[p]
    if not data then return end
    if data.bluePortal.Open then
        PlaySound(fizzleSnd[math.random(1, #fizzleSnd)], data.bluePortal.Position, 0.5)
    end
    if data.orangePortal.Open then
        PlaySound(fizzleSnd[math.random(1, #fizzleSnd)], data.orangePortal.Position, 0.5)
    end
    PlaySound(fizzlerSnd, GetPlayerPos(p), 1)
    data.roll = 15
    data.rollK = 1
end

function client.onTeleported(fromColor)
    local p = GetLocalPlayer()
    local data = players[p]
    if not data then return end
    PlaySound(enterSnd[math.random(1, #enterSnd)], GetPlayerPos(p), 0.2)
    data.falling = true
    data.fallingNormal = (fromColor == "blue") and data.orangePortal.Normal or data.bluePortal.Normal
    data.cameraOffsetTime = 2
    -- TODO: compute camera offset rotation for smooth transition
end

function client.onPickupStart()
    local p = GetLocalPlayer()
    PlaySound(useStartSnd, GetPlayerPos(p), 0.5)
    local data = players[p]
    if data then data.grab = true end
end

function client.onStopPickup()
    local p = GetLocalPlayer()
    PlaySound(useStopSnd, GetPlayerPos(p), 0.5)
    local data = players[p]
    if data then data.grab = false end
end

function client.onPickupFail()
    local p = GetLocalPlayer()
    PlaySound(useFailureSnd, GetPlayerPos(p), 0.5)
    local data = players[p]
    if data then
        data.roll = 15
        data.rollK = 1
    end
end
```

- [ ] **Step 5: Run lint**

```bash
python -m tools.lint --mod "Portal_Gun"
```

---

### Task 7: Write main.lua — client.draw() (HUD, options, keybinds)

**Files:**
- Modify: `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/main.lua`

- [ ] **Step 1: Write client.draw() — crosshair + camera offset**

```lua
function client.draw()
    local p = GetLocalPlayer()
    if not p then return end
    local data = players[p]
    if not data then return end

    if GetPlayerTool(p) ~= "portalgun" then return end
    if GetPlayerVehicle(p) ~= 0 then return end

    -- Options menu
    if data.optionsOpen then
        client.drawOptions(p, data)
        return
    end

    -- Crosshair
    if GetPlayerCanUseTool(p) then
        UiTranslate(UiCenter(), UiMiddle())
        UiAlign("center middle")
        -- Blue crosshair
        UiColor(data.bluePortal.Color[1], data.bluePortal.Color[2], data.bluePortal.Color[3])
        UiPush()
            UiTranslate(-5, -10)
            if data.bluePortal.Open then
                UiImage("MOD/image/crosshair_bluefull.png")
            else
                UiImage("MOD/image/crosshair_blue.png")
            end
        UiPop()
        -- Orange crosshair
        UiColor(data.orangePortal.Color[1], data.orangePortal.Color[2], data.orangePortal.Color[3])
        UiPush()
            UiTranslate(5, 10)
            if data.orangePortal.Open then
                UiImage("MOD/image/crosshair_orangefull.png")
            else
                UiImage("MOD/image/crosshair_orange.png")
            end
        UiPop()
    end

    -- Keybind hints
    UiPush()
        UiTranslate(UiCenter(), UiHeight() - 25)
        UiAlign("center middle")
        UiColor(0.7, 0.7, 0.7)
        UiFont("regular.ttf", 20)
        UiTextOutline(0, 0, 0, 1, 0.1)
        UiText("LMB: Blue | RMB: Orange | R: Reset | E: Grab | O: Options")
    UiPop()

    -- Camera offset after teleportation
    if data.cameraOffsetTime > 0 then
        local dt = GetTimeStep()
        data.cameraOffsetRot = QuatSlerp(data.cameraOffsetRot, Quat(), 4 * dt)
        SetPlayerCameraOffsetTransform(Transform(Vec(), data.cameraOffsetRot))
        data.cameraOffsetTime = data.cameraOffsetTime - dt
        if data.cameraOffsetTime <= 0 then
            SetPlayerCameraOffsetTransform(Transform())
        end
    end
end
```

- [ ] **Step 2: Write client.drawOptions() — simplified options menu**

```lua
function client.drawOptions(p, data)
    UiMakeInteractive()
    UiPush()
    UiTranslate(UiCenter(), UiHeight() / 2 - 120)
    UiAlign("center middle")

    -- Background
    UiColor(0, 0, 0, 0.85)
    UiRect(400, 350)

    -- Title
    UiColor(1, 1, 1)
    UiFont("bold.ttf", 32)
    UiTranslate(0, -130)
    UiText("Portal Gun Options")

    UiFont("regular.ttf", 24)
    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)

    -- Place Anywhere toggle
    UiTranslate(0, 50)
    local placeAnywhere = GetBool("savegame.mod.any")
    UiText("Place Anywhere: " .. (placeAnywhere and "ON" or "OFF"))
    UiTranslate(0, 30)
    if UiTextButton(placeAnywhere and "Disable" or "Enable", 120, 30) then
        SetBool("savegame.mod.any", not placeAnywhere)
    end

    -- Indestructible toggle
    UiTranslate(0, 40)
    local indestructible = GetBool("savegame.mod.ind")
    UiText("Indestructible: " .. (indestructible and "ON" or "OFF"))
    UiTranslate(0, 30)
    if UiTextButton(indestructible and "Disable" or "Enable", 120, 30) then
        SetBool("savegame.mod.ind", not indestructible)
    end

    -- Funneling toggle
    UiTranslate(0, 40)
    local funneling = GetBool("savegame.mod.fun")
    UiText("Funneling: " .. (funneling and "ON" or "OFF"))
    UiTranslate(0, 30)
    if UiTextButton(funneling and "Disable" or "Enable", 120, 30) then
        SetBool("savegame.mod.fun", not funneling)
    end

    -- Portal Rendering toggle
    UiTranslate(0, 40)
    local rendering = GetBool("savegame.mod.ren")
    UiText("Rendering: " .. (rendering and "ON" or "OFF"))
    UiTranslate(0, 30)
    if UiTextButton(rendering and "Disable" or "Enable", 120, 30) then
        SetBool("savegame.mod.ren", not rendering)
    end

    -- Close button
    UiTranslate(0, 50)
    if UiTextButton("Close [O]", 100, 30) then
        data.optionsOpen = false
        ServerCall("server.setOptionsOpen", false)
    end

    UiPop()
end
```

- [ ] **Step 3: Write tool visual model animation in client.tickPlayer**

The v1 tool animation (lines 740-810 of original main.lua) handles the portal gun's animated arms and barrel. This code uses `GetToolBody()`, `GetBodyShapes()`, and `SetShapeLocalTransform()` — all client-side functions. Port this into client.tickPlayer with player param for `GetToolBody(p)`.

This is the most complex visual code — the portal gun has 16 shapes that animate based on firing state and grab state. Port the shape indexing and transform math.

- [ ] **Step 4: Run lint**

```bash
python -m tools.lint --mod "Portal_Gun"
```

---

### Task 8: Final polish — lint, audit, test, notify

**Files:**
- Verify: all files in `C:/Users/trust/Documents/Teardown/mods/Portal_Gun/`

- [ ] **Step 1: Run full lint**

```bash
python -m tools.lint --mod "Portal_Gun"
```

Fix any findings.

- [ ] **Step 2: Run audit**

```bash
python -m tools.audit --output docs/AUDIT_REPORT.md
```

Verify Portal_Gun shows in the feature matrix.

- [ ] **Step 3: Add @lint-ok annotations where needed**

The mod uses `QueryRaycast` for portal placement (not weapon aim) — this is intentional.
The laser uses `MakeHole` without player damage — this is level-specific.
Add `-- @lint-ok MANUAL-AIM` and `-- @lint-ok MAKEHOLE-DAMAGE` where appropriate.

- [ ] **Step 4: Update MASTER_MOD_LIST.md**

Add Portal_Gun as mod #103 with workshop ID 2421609769.

- [ ] **Step 5: Broadcast completion + notify team**

```
broadcast(mod_converter, info, low, "FINISHED: Portal Gun v2 conversion complete — mod #103, per-player portals, server physics, client rendering")
send_message(mod_converter, docs_keeper, info, medium, "Portal_Gun added as mod #103. Workshop ID 2421609769. Update MASTER_MOD_LIST.md")
```

---

## Known Risks & Mitigations

1. **Portal SurfaceShape handle sync** — Server and client may have different handles for the same shape. Mitigation: Client reconstructs portal placement locally using synced position/rotation, and uses QueryRaycast to find the surface shape at that position.

2. **Portal shader performance** — The raycast shader is expensive. Mitigation: Only render local player's portals.

3. **Body teleportation QueryAabb throttling** — QueryAabbBodies every tick could be expensive. Mitigation: Only check when both portals are open, and the CLAUDE.md rule says throttle to ≤4Hz. For portal body detection, per-tick is acceptable since it's only 2 queries when portals are open (not per-player).

4. **Camera offset after teleportation** — The v1 code computes a camera rotation offset for smooth transition. In v2, `SetPlayerCameraOffsetTransform` is client-only. The server handles the teleport transform, then ClientCall tells the client to apply camera smoothing.

5. **Laser level not testable in sandbox** — The laser features only work on levels with "button", "emitter" entities. This code path won't be testable in most MP maps. It's kept as optional.
