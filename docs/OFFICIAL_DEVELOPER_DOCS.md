# Official Teardown Developer Documentation

> **AUTHORITY:** This document is sourced directly from the Teardown developers at teardowngame.com.
> These are the GROUND TRUTH rules. When any other project doc contradicts this file, THIS FILE WINS.
>
> **Sources:**
> - https://teardowngame.com/#modding
> - https://teardowngame.com/modding-mp/index.html
> - https://www.teardowngame.com/modding/
> - https://www.teardowngame.com/modding/api.html
> - https://blog.voxagon.se/2026/03/13/teardown-multiplayer.html
> - https://github.com/tuxedolabsorg/mplib (MIT, v1.0.0, March 13 2026)
> - https://tuxedolabsorg.github.io/mplib/
>
> **Last updated:** 2026-03-18

---

## Table of Contents

1. [Mod Structure & Files](#mod-structure--files)
2. [info.txt Format](#infotxt-format)
3. [Mod Types](#mod-types)
4. [Scripting System](#scripting-system)
5. [V2 Multiplayer Architecture](#v2-multiplayer-architecture)
6. [Callback Functions](#callback-functions)
7. [Player Management API](#player-management-api)
8. [Player State & Transform API](#player-state--transform-api)
9. [Player Health & Damage API](#player-health--damage-api)
10. [Player Physics API](#player-physics-api)
11. [Tool System API](#tool-system-api)
12. [Weapon & Combat API](#weapon--combat-api)
13. [Input API (Multiplayer-Aware)](#input-api-multiplayer-aware)
14. [Network Communication](#network-communication)
15. [Registry Sync](#registry-sync)
16. [Shared Table](#shared-table)
17. [Game Modes](#game-modes)
18. [Level Markup for Multiplayer](#level-markup-for-multiplayer)
19. [Asset System](#asset-system)
20. [Event System](#event-system)
21. [Camera & Visual Effects](#camera--visual-effects)
22. [Player Interaction API](#player-interaction-api)
23. [Player Spawn & Respawn API](#player-spawn--respawn-api)
24. [Player Vehicles & Rigging API](#player-vehicles--rigging-api)
25. [Player Movement & Settings API](#player-movement--settings-api)
26. [Helper Includes](#helper-includes)
27. [mplib — Official Multiplayer Library](#mplib--official-multiplayer-library)
28. [Networking Internals](#networking-internals)
29. [Critical Gotchas & Rules](#critical-gotchas--rules)
30. [Official Reference Mods](#official-reference-mods)
31. [External Resources](#external-resources)

---

## Mod Structure & Files

Mods are folders in `Documents/Teardown/mods/`. Key files:

| File | Required | Purpose |
|------|----------|---------|
| `info.txt` | YES | Mod metadata |
| `main.lua` | YES | Script executed when mod is active |
| `main.xml` | Content mods only | Level data (created in Editor) |
| `options.lua` | No | Optional settings interface |
| `preview.jpg` | No | Steam Workshop thumbnail (max 1MB) |
| `spawn.txt` | No | Spawnable asset list |
| `gamemodes.txt` | No | Game mode definitions |

**Path keywords:**
- `MOD/` — references the mod's root folder
- `LEVEL/` — references the folder matching the current XML filename

---

## info.txt Format

```
name = My Mod Name
author = Author Name
description = Short description
tags = Tool, Gameplay
version = 2
preview = preview.png
```

**Fields:**
- `name` — Mod display name
- `author` — Author name
- `description` — Short description
- `tags` — Comma-separated: `Map`, `Gameplay`, `Asset`, `Vehicle`, `Tool`
- `version = 2` — **REQUIRED** for multiplayer compatibility
- `preview` — Preview image filename (512x292 px, PNG or JPG)

---

## Mod Types

| Type | Has main.xml | Behavior |
|------|-------------|----------|
| **Global** | No | Affects all gameplay when enabled (Campaign, Sandbox, other mods). Listed on loading screens. |
| **Content** | Yes | Standalone playable environment. Has Play button in Mod Manager. |

---

## Scripting System

- **Language:** Lua (engine-embedded interpreter, Lua 5.1 — no `goto`/labels)
- **No external installation needed**
- **Registry system** for inter-script communication (hierarchical key-value store)
- **`savegame.mod.*`** — persistent per-mod storage

---

## V2 Multiplayer Architecture

**Declaration:** `version = 2` in `info.txt` + `#version 2` at the top of every `.lua` file.

Without `#version 2`, scripts are **automatically disabled** in multiplayer sessions.

The same script file runs on both server and clients. Three built-in tables separate code:

| Table | Runs On | Purpose |
|-------|---------|---------|
| `server` | Host only | Game logic, scoring, validation, spawning, damage |
| `client` | Each client + host | Rendering, UI, effects, local predictions |
| `shared` | All (read-only on clients) | Synchronized state from server |

**CRITICAL:** The host runs BOTH `server` and `client` code simultaneously.

---

## Callback Functions

### Server-Side (host only)
```lua
function server.init()          -- Called once when script loads
function server.tick(dt)        -- Called every frame (variable timestep)
function server.update(dt)      -- Fixed 60 Hz timestep (0, 1, or 2 calls per frame)
function server.postUpdate()    -- After physics calculations
function server.destroy()       -- Called on script/game mode termination
```

### Client-Side (each client + host)
```lua
function client.init()          -- Called once when script loads
function client.tick(dt)        -- Called every frame (variable timestep)
function client.update(dt)      -- Fixed 60 Hz timestep
function client.postUpdate()    -- After physics; used by animators
function client.draw()          -- 2D overlay rendering (ONLY place for Ui* calls)
function client.render(dt)      -- Called before final rendering
function client.destroy()       -- Called on script/game mode termination
```

---

## Player Management API

```lua
GetAllPlayers()                 -- Returns table of all player handles
GetAddedPlayers()               -- Returns newly added players this frame
GetRemovedPlayers()             -- Returns players removed this frame
GetLocalPlayer()                -- Returns local player ID (client only)
IsPlayerLocal(playerId)         -- true if player is on this client
IsPlayerHost(playerId)          -- true if player is the host
IsPlayerValid(playerId)         -- true if player handle is valid
GetPlayerName(playerId)         -- Returns player display name
GetPlayerCount()                -- Returns number of active players
GetMaxPlayers()                 -- Returns max player count
```

### Iterator Wrappers (from player.lua include)

```lua
-- These wrap the raw API as iterators for use in for-loops
Players()                       -- wraps GetAllPlayers()
PlayersAdded()                  -- wraps GetAddedPlayers()
PlayersRemoved()                -- wraps GetRemovedPlayers()

-- CORRECT:
for p in Players() do ... end

-- WRONG (will crash):
for _, p in ipairs(Players()) do ... end
```

---

## Player State & Transform API

```lua
GetPlayerPos(playerId)                              -- Returns TVec position
GetPlayerTransform(playerId)                        -- Returns TTransform
GetPlayerTransformWithPitch(playerId)               -- Returns TTransform, pitch
SetPlayerTransform(transform, playerId)             -- Server only (player param LAST)
SetPlayerTransformWithPitch(transform, pitch, playerId)  -- Server only (player param LAST)
GetPlayerEyeTransform(playerId)                     -- Camera/eye transform
GetPlayerCameraTransform(playerId)                  -- Current camera transform
SetPlayerCameraOffsetTransform(transform, stackable, playerId) -- Offset camera (value FIRST, player LAST)
GetPlayerPitch(playerId)                            -- Returns pitch in degrees
GetPlayerYaw(playerId)                              -- Returns yaw in degrees
SetPlayerPitch(pitch, playerId)                     -- Set pitch (degrees) (value FIRST, player LAST)
GetPlayerCrouch(playerId)                           -- Returns crouch state
```

---

## Player Health & Damage API

```lua
GetPlayerHealth(playerId)                           -- Returns health (0.0-1.0)
SetPlayerHealth(health, playerId)                   -- Set health (SERVER ONLY) — health FIRST, player SECOND
ApplyPlayerDamage(targetPlayer, damage, toolId, attackerPlayer)
    -- targetPlayer: player to damage
    -- damage: number damage amount
    -- toolId: string tool ID for kill attribution
    -- attackerPlayer: player who caused the damage
    -- NOTE: API page shows (playerId, damage, healthBefore, cause, point, impulse)
    --   but official lasergun source uses this 4-param signature

GetPlayerAimInfo(playerId)                          -- Simple form
GetPlayerAimInfo(muzzlePos, maxDist, playerId)      -- Extended form
    -- Returns: hit, startPoint, endPoint, direction
    -- Handles MP aim compensation automatically
```

---

## Player Physics API

```lua
GetPlayerVelocity(playerId)                         -- Returns TVec
SetPlayerVelocity(velocity, playerId)               -- Server only (player param LAST)
SetPlayerGroundVelocity(velocity, playerId)         -- Server only (player param LAST)
IsPlayerGrounded(playerId)                          -- true if on ground
IsPlayerJumping(playerId)                           -- true if jumping
GetPlayerGroundContact(playerId)                    -- Ground surface info
```

---

## Tool System API

```lua
-- Registration (server.init only)
RegisterTool(name, label, file, [group])
    -- name: string ID (e.g., "minigun")
    -- label: string display name (e.g., "loc@MINIGUN" or "Minigun")
    -- file: string XML path (e.g., "MOD/prefab/minigun.xml")
    -- group: number for tool ordering (optional, from official minigun)

-- Enable/Disable (player param LAST — API page incorrectly shows playerId first)
SetToolEnabled(toolId, enabled, playerId)           -- Server only
IsToolEnabled(toolId, playerId)                     -- toolId FIRST, player LAST

-- Ammo (player param LAST — API page incorrectly shows playerId first)
SetToolAmmo(toolId, ammo, playerId)                 -- Server only
GetToolAmmo(toolId, playerId)                       -- toolId FIRST, player LAST
SetToolAmmoPickupAmount(toolId, amount)              -- Global pickup amount
GetToolAmmoPickupAmount(toolId)

-- Tool bodies and transforms (player param LAST throughout)
GetToolBody(playerId)                               -- Returns body handle (single param)
GetToolHandPoseLocalTransform(playerId)              -- Returns right, left transforms
GetToolHandPoseWorldTransform(playerId)              -- Returns right, left transforms
SetToolHandPoseLocalTransform(right, left, playerId) -- Set hand poses (values FIRST, player LAST)
GetToolLocationLocalTransform(name, playerId)        -- location name FIRST, player LAST
GetToolLocationWorldTransform(name, playerId)        -- location name FIRST, player LAST
    -- name: string location (e.g., "muzzle", "fp_action", "tp_action")
SetToolTransform(transform, sway, playerId)          -- Client only (values FIRST, player LAST)
SetToolAllowedZoom(zoom, _zoom)                      -- No player param in script_defs
SetToolTransformOverride(transform, playerId)        -- Client only (value FIRST, player LAST)
SetToolOffset(offset, playerId)                      -- Client only (value FIRST, player LAST)

-- Player tool state (player param LAST)
GetPlayerTool(playerId)                             -- Current tool name
SetPlayerTool(tool, playerId)                       -- Switch tool (tool FIRST, player LAST)
GetPlayerCanUseTool(playerId)                       -- Can fire?
```

---

## Weapon & Combat API

### Shoot (bullets — server only)
```lua
Shoot(position, direction, type, damage, range, playerId, toolId)
    -- position: TVec muzzle position
    -- direction: TVec fire direction
    -- type: string projectile type (e.g., "bullet")
    -- damage: number damage amount (1.0 = standard)
    -- range: number max distance
    -- playerId: attacker for kill attribution
    -- toolId: string tool ID for kill feed (e.g., "minigun")
    -- NOTE: API page shows (pos, dir, force, damage, [playerId], [blunt])
    --   but official minigun source uses this extended signature
```

### QueryShot (raycast that detects players — server only)
```lua
QueryShot(position, direction, length, radius, playerId)
    -- Returns raycast from projectile perspective
    -- DETECTS PLAYERS (unlike QueryRaycast)
    -- length: number max distance
    -- radius: number hit radius
    -- playerId: attacker (for self-hit exclusion — excludes this player from detection)
    -- Returns: hit, dist, shape, player, hitFactor, normal
    --   player = 0 or nil when no player hit (BOTH forms)
    --   ALWAYS guard with `if player ~= 0 then` (Lua 0 is truthy!)
    -- NOTE: API page shows (pos, dir, [maxDist]) but official lasergun
    --   uses this extended signature
    -- IMPORTANT: Always use the 5-param form for weapons. The 3-param form
    --   QueryShot(pos, dir, maxDist) has no attacker exclusion.
    --   See Issue #47 — 39 mods fixed for this bug pattern
```

### ApplyPlayerDamage (beam/melee damage — server only)
```lua
ApplyPlayerDamage(targetPlayer, damage, toolId, attackerPlayer)
    -- targetPlayer: player to damage
    -- damage: number damage amount
    -- toolId: string tool ID (appears in kill feed)
    -- attackerPlayer: player who caused the damage
    -- NOTE: API page shows (playerId, damage, healthBefore, cause, point, impulse)
    --   but official lasergun source uses this simplified signature
```

### MakeHole (terrain destruction — server only, auto-replicated)
```lua
MakeHole(position, radius)
    -- Voxel destruction only — does NOT damage players
    -- Automatically replicated to all clients via deterministic commands
```

### Explosion (server only, auto-replicated)
```lua
Explosion(position, radius, [impulse], [damage])
    -- Auto-replicated like MakeHole
    -- Does NOT damage players — only destroys terrain + applies physics impulse
    -- For player damage, add ApplyPlayerDamage() with distance falloff (Issue #56)
```

---

## Input API (Multiplayer-Aware)

```lua
InputPressed(input, [playerId])
InputReleased(input, [playerId])
InputDown(input, [playerId])
InputValue(input, [playerId])
InputLastPressedKey([playerId])
```

**playerId semantics:**
- On client: `0` or omitted = local player
- On server: `0` = host player

**CRITICAL:** Action names (`"usetool"`, `"jump"`, `"interact"`) work with player param. **Raw key names** (`"rmb"`, `"r"`, `"lmb"`) do **NOT** work with player param — they **fail silently**. Use raw keys only on client with `IsPlayerLocal(p)` check + `ServerCall` pattern.

---

## Network Communication

### ServerCall (client → server)
```lua
ServerCall(functionName, [param1, param2, ...])
    -- functionName: string name of server function (e.g., "server.onFire")
    -- Function must exist in the same script
    -- CRITICAL: Engine does NOT auto-inject caller's player ID.
    -- Client MUST pass player ID explicitly as first param:
    --   ServerCall("server.onFire", p, aimX, aimY, aimZ)
    -- Server function receives exactly what client sends:
    --   function server.onFire(p, ax, ay, az)
    -- Verified from official minigun source (Issue #51)
```

### ClientCall (server → client)
```lua
ClientCall(playerId, functionName, [param1, param2, ...])
    -- playerId: target player (0 = broadcast to ALL)
    -- functionName: string name of client function
```

**Best for:** One-time events (fire, reload, round start). **NOT** for continuous state sync (use registry sync instead).

---

## Registry Sync

```lua
-- Server writes with sync=true (3rd parameter)
SetInt(key, value, [sync])
SetFloat(key, value, [sync])
SetBool(key, value, [sync])
SetString(key, value, [sync])

-- Client reads
GetInt(key)
GetFloat(key)
GetBool(key)
GetString(key)
```

When `sync = true`, values are automatically replicated from server to all clients via the engine's network layer (batched, prioritized, efficient).

**Best for:** Continuous state (positions, scores, timers, per-player data).

**Per-player pattern:**
```lua
SetFloat("mymod."..p..".score", score, true)
```

---

## Shared Table

```lua
-- Server writes directly
shared.matchTime = 120
shared.roundNumber = 3

-- Client reads (READ-ONLY)
local time = shared.matchTime
```

Automatic server→client synchronization. Clients cannot write to `shared`.

---

## Game Modes

### Global Game Modes (in Global mods)
Played on current level. Defined in `gamemodes.txt`:
```
[My Game Mode]
description = "Description text"
path = mygamemode.lua
restart = true
preview = mode_thumb.jpg
```

### Content Game Modes (in Content mods)
Always start on `main.xml`. Use layers:
```
[My Game Mode]
description = "Description text"
layers = gamemodelayer1, alwaysActiveLayer
preview = mode_thumb.jpg
```

**Preview images:** 512x292 px, PNG or JPG.

**Rules:**
- Only one game mode active at a time
- Global modes use current level; Content modes load specified layers
- Pressing Restart keeps active mode
- Content mode level transitions preserve the active mode

---

## Level Markup for Multiplayer

Standardized Location Node tags (convention, not requirement):

| Tag | Purpose |
|-----|---------|
| `playerspawn` | Free-for-all spawn points |
| `teamspawn=1`, `teamspawn=2` | Team-specific spawn points |
| `ammospawn rarity=low` | Gray crates (low rarity) |
| `ammospawn rarity=medium` | Blue crates (medium rarity) |
| `ammospawn rarity=high` | Red crates (high rarity) |
| `pointofinterest=1` | Team 1 objectives (CTF bases, etc.) |
| `pointofinterest=2` | Team 2 objectives |

---

## Asset System

### Voxel Files (.vox)
- Created in **MagicaVoxel** (tested up to v0.99.6.4)
- Max size: 256x256x256 voxels (recommended 128x128x128)
- Voxels connect along sides, not edges/corners
- 14 material types with hardness levels
- Support named locations (muzzle, fp_action, etc.)

### Audio
- Format: `.ogg`
- Game loads `.ogg` before encrypted `.tde` — custom sounds override defaults

### Content Replacement
Replicate game data structure in mod folder to override defaults:
```
MOD/data/vox/pipebomb.vox  →  replaces default pipebomb
```

---

## Event System

```lua
-- Server-side event detection
local count = GetEventCount("playerdied")
for i = 1, count do
    local victim, attacker, damage, healthBefore, cause, point, impulse = GetEvent("playerdied", i)
    -- victim: player who died
    -- attacker: player who killed them
    -- cause: tool ID (from Shoot() or ApplyPlayerDamage())
end
```

**For kill attribution to work, weapons MUST pass tool ID to `Shoot()` or `ApplyPlayerDamage()`.** Without it, kills show as "unknown" in the kill feed and stats.

---

## Camera & Visual Effects

```lua
-- Camera shake (client, affects all nearby players)
ShakeCamera(pos, intensity, radius, [duration])

-- Depth of field (client)
SetCameraDof(near, far, [blur])

-- Low health blur (client)
SetLowHealthBlurThreshold(threshold)

-- Body outline drawing (client)
DrawBodyOutline(body, r, g, b, a)

-- Shape emissive glow (client)
SetShapeEmissiveScale(shape, value)
```

---

## Player Interaction API

```lua
GetPlayerGrabShape(playerId)          -- Shape player is holding
GetPlayerGrabBody(playerId)           -- Body player is holding
GetPlayerGrabPoint(playerId)          -- Grab point position
ReleasePlayerGrab(playerId)           -- Force release
GetPlayerPickShape(playerId)          -- Shape player is looking at
GetPlayerPickBody(playerId)           -- Body player is looking at
GetPlayerInteractShape(playerId)      -- Interactable shape
GetPlayerInteractBody(playerId)       -- Interactable body
```

---

## Player Spawn & Respawn API

```lua
SetPlayerSpawnTransform(transform, playerId)    -- Set spawn location (value FIRST, player LAST)
SetPlayerSpawnHealth(health, playerId)           -- Set health on respawn (value FIRST, player LAST)
SetPlayerSpawnTool(toolId, playerId)             -- Set tool on respawn (value FIRST, player LAST)
RespawnPlayer(playerId)                          -- Respawn at set location
RespawnPlayerAtTransform(transform, playerId)    -- Respawn at specific location (value FIRST, player LAST)
```

---

## Player Vehicles & Rigging API

```lua
GetPlayerVehicle(playerId)
SetPlayerVehicle(vehicle, playerId)              -- value FIRST, player LAST
IsPlayerVehicleDriver(handle, playerId)          -- vehicle handle FIRST, player LAST
IsPlayerVehiclePassenger(handle, playerId)        -- vehicle handle FIRST, player LAST
GetPlayerAnimator(playerId)
SetPlayerAnimator(animator, playerId)            -- value FIRST, player LAST
GetPlayerBodies(playerId)                        -- All bodies belonging to player
SetPlayerRig(rig, playerId)                      -- value FIRST, player LAST
GetPlayerRig(playerId)
GetPlayerRigWorldTransform(playerId)
SetPlayerRigTransform(rig_id, location, playerId) -- values FIRST, player LAST
ClearPlayerRig(playerId)
SetPlayerRigLocationLocalTransform(rig_id, name, location, playerId) -- values FIRST, player LAST
GetPlayerRigLocationWorldTransform(name, playerId) -- name FIRST, player LAST
GetPlayerRigHasTag(tag, playerId)                -- tag FIRST, player LAST
GetPlayerRigTagValue(tag, playerId)              -- tag FIRST, player LAST
SetPlayerRigTags(rig_id, tag, playerId)          -- values FIRST, player LAST
GetPlayerColor(playerId)                         -- Returns found, r, g, b
SetPlayerColor(r, g, b, playerId)                -- Server only (colors FIRST, player LAST)
```

---

## Player Movement & Settings API

```lua
GetPlayerWalkingSpeed(playerId)
SetPlayerWalkingSpeed(speed, playerId)           -- Server only (value FIRST, player LAST)
GetPlayerCrouchSpeedScale(playerId)
SetPlayerCrouchSpeedScale(speed, playerId)       -- Server only (value FIRST, player LAST)
GetPlayerHurtSpeedScale(playerId)
SetPlayerHurtSpeedScale(speed, playerId)         -- Server only (value FIRST, player LAST)
GetPlayerParam(parameter, player)                -- param FIRST, player LAST
SetPlayerParam(parameter, value, player)         -- param FIRST, value SECOND, player LAST
SetPlayerHidden(playerId)                        -- Server only (single param per script_defs)
DisablePlayerInput(player)                       -- Server only: block all input
DisablePlayer(playerId)                          -- Server only: fully disable
IsPlayerDisabled(playerId)
DisablePlayerDamage(playerId)                    -- Server only: invulnerable
SetPlayerScreen(handle, playerId)                -- handle FIRST, player LAST
GetPlayerScreen(playerId)
SetPlayerRegenerationState(state, player)        -- value FIRST, player LAST
SetPlayerOrientation(orientation, playerId)      -- value FIRST, player LAST
GetPlayerOrientation(playerId)
GetPlayerUp(playerId)
```

---

## Helper Includes

```lua
#include "script/include/player.lua"    -- Players(), PlayersAdded(), PlayersRemoved() iterators
#include "script/include/common.lua"    -- clamp(), math.clamp(), COLOR_WHITE, etc.
#include "script/toolanimation.lua"     -- ToolAnimator system for tool poses
#include "script/toolutilities.lua"     -- SpawnTool(), setupToolsUpgradedFully()
```

### ToolAnimator System
Handles first-person and third-person tool poses, arm pitch, action vs idle poses, wall collision, hand positioning, smooth blending:

```lua
#include "script/toolanimation.lua"

-- In createPlayerData():
toolAnimator = ToolAnimator(),

-- In client.tickPlayer():
data.toolAnimator.offsetTransform = Transform(Vec(0, recoil, 0))
tickToolAnimator(data.toolAnimator, dt, nil, p)
```

### Tool Location Names
Named positions defined in tool vox/xml prefab:
- `"muzzle"` — barrel/muzzle position
- `"fp_action"` — first-person firing pose
- `"fp_action_crouch"` — crouching fire pose
- `"fp_run"` / `"fp_jump"` / `"fp_swim"` — movement poses
- `"tp_action"` — third-person firing pose (+ `_rh`, `_lh` for hands)
- `"tp_run"` — third-person running pose

---

## mplib — Official Multiplayer Library

**Source:** https://github.com/tuxedolabsorg/mplib (MIT, v1.0.0)
**Docs:** https://tuxedolabsorg.github.io/mplib/

10 modules for multiplayer game modes:

| Module | Purpose |
|--------|---------|
| `countdown.lua` | Pre-round countdown, locks players during countdown |
| `eventlog.lua` | Kill feed / event messages in top-right corner |
| `hud.lua` | Damage feedback, timers, scoreboard, world markers, respawn timer, settings UI |
| `spawn.lua` | Player spawning and respawning |
| `spectate.lua` | Third-person death camera, player cycling, killer highlight |
| `stats.lua` | Kill/death counts per player |
| `teams.lua` | Dynamic team assignment, player coloring, team selection UI |
| `tools.lua` | Loot tables, tool spawning, dropped weapons, ammo crates |
| `ui.lua` | Standardized text, panel, button, and player-related UI helpers |
| `util.lua` | Spawn position extraction, tool spawn locations, points of interest |

### Integration
```lua
#include "mplib/countdown.lua"
#include "mplib/eventlog.lua"
#include "mplib/stats.lua"
#include "mplib/teams.lua"
#include "mplib/tools.lua"
#include "mplib/util.lua"
#include "mplib/spectate.lua"
#include "mplib/hud.lua"
```

### Key mplib Patterns

**Loot tables (from deathmatch):**
```lua
lootTables[1] = {{name="steroid", weight=10, amount=4}}        -- low tier
lootTables[2] = {{name="shotgun", weight=7}, {name="gun", weight=7}} -- mid tier
lootTables[3] = {{name="rifle", weight=9}, {name="rocket", weight=10}} -- high tier
toolsAddModToolsToLootTable(lootTables[2], 3)   -- auto-adds ALL custom mod tools
toolsAddModToolsToLootTable(lootTables[3], 3)
```

**Auto-detection of custom mod tools:**
```lua
local tools = ListKeys("game.tool")
for i = 1, #tools do
    if GetBool("game.tool."..tools[i]..".custom") then
        -- This tool is from a mod
    end
end
```

**For custom tools to appear in loot crates, you need:**
1. `RegisterTool("toolid", "Name", "MOD/vox/tool.xml", group)` — registers the tool
2. `SetToolAmmoPickupAmount("toolid", amount)` — enables ammo crate integration

That's it. Both are required for automatic loot crate integration in all multiplayer game modes.

**Teams:**
```lua
teamsInit(numTeams)
teamsSetColors({{r,g,b}, {r,g,b}})
teamsSetNames({"Team A", "Team B"})
teamsGetTeam(playerId)
teamsGetLocalTeamPlayers()
```

**Tool drop prevention:**
```lua
toolsPreventToolDrop("flag1")   -- prevents specific tools from dropping on death
```

---

## Networking Internals

> Source: https://blog.voxagon.se/2026/03/13/teardown-multiplayer.html

### Two Network Channels

1. **Reliable Stream** — Deterministic commands (destruction, spawning, property changes). Commands like `MakeHole`, `Explosion` are replicated as operations, NOT raw voxel data.
2. **Unreliable Stream** — Object transforms, velocities, player positions. Server uses priority queue (~1 Mbit/client). Objects selected by player visibility.

### Key Implications

- **Destruction is deterministic** — Fixed-point integer math ensures identical results across clients. `MakeHole`/`Explosion` commands are replicated, not their visual output.
- **Physics is semi-deterministic** — Server is authoritative. Client simulates locally but receives corrections. "Visible snapping" for deprioritized objects.
- **Entity handles can be NEGATIVE in v2** — Client-side entities use negative handles. **NEVER** check `handle > 0` — check `handle ~= 0` instead.
- **Late-join uses command replay** — New joiners replay the recorded command buffer to reconstruct level state.
- **`MakeHole`/`Explosion` on server are auto-replicated** — No need to mirror on client.
- **`SpawnParticle`/`PlaySound` are client-local only** — Each client runs its own visual effects.
- **`Shoot()` feeds into deterministic destruction pipeline** — Proper replication, damage, and kill attribution.
- **Avoid creating many server-side bodies** — Each consumes bandwidth from the priority queue.

---

## Critical Gotchas & Rules

### 1. Raw Keys + Player Param = SILENT FAILURE
```lua
-- BROKEN (fails silently, returns false always):
InputPressed("rmb", p)
InputPressed("r", p)
InputPressed("lmb", p)

-- CORRECT:
InputPressed("usetool")   -- action names work without player
-- OR on client with IsPlayerLocal check:
if IsPlayerLocal(p) and InputPressed("rmb") then
    ServerCall("server.onFire", ...)
end
```

### 2. Players/PlayersAdded/PlayersRemoved are ITERATORS
```lua
-- CORRECT:
for p in Players() do ... end
for p in PlayersAdded() do ... end

-- WRONG (CRASH):
for _, p in ipairs(Players()) do ... end
```

### 3. Entity Handles Can Be Negative
```lua
-- WRONG:
if handle > 0 then ... end

-- CORRECT:
if handle ~= 0 then ... end
```

### 4. MakeHole and Explosion Cannot Damage Players
`MakeHole()` and `Explosion()` destroy terrain and apply physics impulse, but do **NOT** reduce player health. Use `Shoot()` for bullets or `QueryShot()` + `ApplyPlayerDamage()` for beams/melee. For explosive weapons, add `ApplyPlayerDamage()` with distance falloff after `Explosion()`. (Issue #56)

### 5. Server-Only vs Client-Only Functions

**Server only:** `MakeHole`, `Explosion`, `Shoot`, `SetBodyVelocity`, `ApplyBodyImpulse`, `Spawn`, `Delete`, `SpawnFire`, `SetPlayerVelocity`, `SetPlayerTransform`, `ApplyPlayerDamage`, `SetPlayerHealth`, `SetToolEnabled`, `SetToolAmmo`, `DisablePlayerInput`, `SetPlayerColor`, `SetPlayerWalkingSpeed`

**Client only:** `PlaySound`, `SpawnParticle`, `DrawLine`, `DrawSprite`, `PointLight`, `SetToolTransform`, `SetCameraTransform`, all `Ui*` functions, `ShakeCamera`, `SetCameraDof`, `DrawBodyOutline`
**Effectively client-only (visual):** `SetShapeEmissiveScale` — server calls only render for host; use in client code for all players to see (Issue #53)

### 6. UiMakeInteractive Before UiPush
Options menus MUST call `UiMakeInteractive()` before `UiPush()`. Without it, buttons render but can't be clicked.

### 7. Player Param is ALWAYS LAST
```lua
SetPlayerHealth(health, playerId)       -- value FIRST, player LAST
SetPlayerWalkingSpeed(speed, playerId)  -- value FIRST, player LAST
SetPlayerColor(r, g, b, playerId)       -- values FIRST, player LAST
SetPlayerTool(tool, playerId)           -- value FIRST, player LAST
-- This pattern applies to ALL Set*/Get* functions with playerId.
-- The API page shows playerId FIRST — it is WRONG. See discrepancy table.
```

### 8. Per-Tick RPC Floods the Network
Never call `ServerCall`/`ClientCall` every tick with position data. Use registry sync (`SetFloat(key, val, true)`) for continuous state.

### 9. Client Projectile Physics Must Be Local-Only
Gate all projectile physics with `IsPlayerLocal(p)`. Remote player projectile simulation causes desync.

### 10. Lua 5.1 Restrictions
No `goto` statements, no labels. No `mousedx`/`mousedy` — use `camerax`/`cameray` instead.

---

## Official Reference Mods

| Mod | Lines | Type | Key Patterns |
|-----|-------|------|--------------|
| **minigun** | 202 | Bullet weapon | `Shoot()`, `GetPlayerAimInfo()`, `GetToolLocationWorldTransform("muzzle")`, `SetToolAmmoPickupAmount()`, `ToolAnimator` |
| **lasergun** | 233 | Beam weapon | `QueryShot()`, `ApplyPlayerDamage()`, advanced particle API, `SetShapeEmissiveScale()`, `SetToolHandPoseLocalTransform()` |
| **mpclassics** | Game modes | Deathmatch/TDM/CTF | `shared.time`, loot tables, event system, teams, spectate, full mplib integration |

**Locations:**
```
C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/minigun/main.lua
C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/lasergun/main.lua
C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/mpclassics/
```

---

## API Signature Notes

> The official API page (api.html) sometimes shows **simplified or differently-ordered signatures** compared to what actually works. The main sections above now use the **actual working signatures** verified from official reference mods (minigun/lasergun) and our 159 working mods. The table below documents the discrepancies for reference.

**API page vs actual signatures (main sections above already use the correct versions):**

| Function | API Page Shows | Actual Working Signature |
|----------|---------------|--------------------------------------|
| `RegisterTool` | `(name, label, file)` | `(name, label, file, group)` — group number for tool ordering |
| `Shoot` | `(pos, dir, force, damage, [playerId], [blunt])` | `(pos, dir, "bullet", damage, range, playerId, "toolId")` — from minigun |
| `ApplyPlayerDamage` | `(playerId, damage, healthBefore, cause, point, impulse)` | `(targetPlayer, damage, "toolId", attackerPlayer)` — from lasergun |
| `SetToolEnabled` | `(playerId, toolName, enabled)` | `(toolName, enabled, playerId)` — from 159 working mods |
| `SetToolAmmo` | `(playerId, toolName, ammo)` | `(toolName, ammo, playerId)` — matches SetToolEnabled pattern |
| `SetPlayerHealth` | `(playerId, health)` | `(health, playerId)` — health value FIRST |
| `SetPlayerTransform` | `(playerId, transform)` | `(transform, playerId)` — player param LAST |
| `SetPlayerTransformWithPitch` | `(playerId, transform, pitch)` | `(transform, pitch, playerId)` — player param LAST |
| `SetPlayerVelocity` | `(playerId, velocity)` | `(velocity, playerId)` — player param LAST |
| `SetPlayerGroundVelocity` | `(playerId, velocity)` | `(velocity, playerId)` — player param LAST |
| `GetPlayerAimInfo` | `(playerId)` | `(muzzlePos, maxDist, playerId)` — from minigun |
| `QueryShot` | `(pos, dir, [maxDist])` | `(pos, dir, len, radius, playerId)` — from lasergun |
| `SetPlayerSpawnTransform` | `(playerId, transform)` | `(transform, playerId)` — from script_defs.lua + hub/startpos.lua |
| `SetPlayerSpawnHealth` | `(playerId, health)` | `(health, playerId)` — from script_defs.lua |
| `SetPlayerSpawnTool` | `(playerId, tool)` | `(toolId, playerId)` — from script_defs.lua |
| `RespawnPlayerAtTransform` | `(playerId, transform)` | `(transform, playerId)` — from script_defs.lua + mpclassics/spawn.lua |
| `SetPlayerPitch` | `(playerId, pitch)` | `(pitch, playerId)` — from script_defs.lua |
| `SetPlayerCameraOffsetTransform` | `(playerId, transform)` | `(transform, stackable, playerId)` — from script_defs.lua (extra param) |
| `SetPlayerWalkingSpeed` | `(playerId, speed)` | `(speed, playerId)` — from script_defs.lua + mplib/countdown.lua |
| `SetPlayerCrouchSpeedScale` | `(playerId, scale)` | `(speed, playerId)` — from script_defs.lua |
| `SetPlayerHurtSpeedScale` | `(playerId, scale)` | `(speed, playerId)` — from script_defs.lua |
| `SetPlayerParam` | `(playerId, param, value)` | `(parameter, value, player)` — from script_defs.lua |
| `GetPlayerParam` | `(playerId, param)` | `(parameter, player)` — from script_defs.lua |
| `SetPlayerScreen` | `(playerId, screen)` | `(handle, playerId)` — from script_defs.lua |
| `SetPlayerRegenerationState` | `(playerId, state)` | `(state, player)` — from script_defs.lua |
| `SetPlayerOrientation` | `(playerId, orientation)` | `(orientation, playerId)` — from script_defs.lua |
| `SetPlayerTool` | `(playerId, tool)` | `(tool, playerId)` — from script_defs.lua + mpclassics |
| `SetPlayerVehicle` | `(playerId, vehicle)` | `(vehicle, playerId)` — from script_defs.lua |
| `SetPlayerAnimator` | `(playerId, animator)` | `(animator, playerId)` — from script_defs.lua |
| `SetPlayerRig` | `(playerId, rig)` | `(rig, playerId)` — from script_defs.lua |
| `SetPlayerColor` | `(playerId, r, g, b)` | `(r, g, b, playerId)` — from script_defs.lua + mplib/teams.lua |
| `SetPlayerHidden` | `(playerId, hidden)` | `(playerId)` — script_defs.lua shows single param |
| `IsToolEnabled` | `(playerId, toolName)` | `(toolId, playerId)` — from script_defs.lua |
| `GetToolAmmo` | `(playerId, toolName)` | `(toolId, playerId)` — from script_defs.lua |
| `GetToolBody` | `(playerId, toolName)` | `(playerId)` — script_defs.lua shows single param |
| `SetToolHandPoseLocalTransform` | `(playerId, transform)` | `(right, left, playerId)` — from script_defs.lua (two transforms) |
| `SetToolTransform` | `(playerId, transform)` | `(transform, sway, playerId)` — from script_defs.lua (extra sway param) |
| `SetToolTransformOverride` | `(playerId, transform)` | `(transform, playerId)` — from script_defs.lua |
| `SetToolOffset` | `(playerId, offset)` | `(offset, playerId)` — from script_defs.lua |
| `GetToolLocationLocalTransform` | `(playerId)` | `(name, playerId)` — from script_defs.lua (needs name param) |
| `GetToolLocationWorldTransform` | `(playerId, toolName, location)` | `(name, playerId)` — from script_defs.lua |
| `GetPlayerRigLocationWorldTransform` | `(playerId, location)` | `(name, playerId)` — from script_defs.lua |
| `GetPlayerRigHasTag` | `(playerId, tag)` | `(tag, playerId)` — from script_defs.lua |
| `GetPlayerRigTagValue` | `(playerId, tag)` | `(tag, playerId)` — from script_defs.lua |
| `IsPlayerVehicleDriver` | `(playerId)` | `(handle, playerId)` — from script_defs.lua (needs vehicle handle) |
| `IsPlayerVehiclePassenger` | `(playerId)` | `(handle, playerId)` — from script_defs.lua (needs vehicle handle) |

**Pattern:** The API page almost universally puts `playerId` FIRST. The actual engine puts `playerId` LAST (making it optional, defaulting to host/local). This applies to nearly every `Set*`/`Get*` function that takes a player parameter. Source: `script_defs.lua` (engine function definitions) + verified against official mod source code (mpclassics, minigun, lasergun, hub scripts).

**Rule:** When the API page contradicts official mod source code or script_defs.lua, follow the source code. The main sections above already reflect the correct signatures.

---

## External Resources

| Resource | URL |
|----------|-----|
| **Modding Homepage** | https://www.teardowngame.com/modding/ |
| **Lua API Reference** | https://www.teardowngame.com/modding/api.html |
| **API XML (machine-readable)** | https://www.teardowngame.com/modding/api.xml |
| **MP Modding Guide** | https://teardowngame.com/modding-mp/index.html |
| **mplib Documentation** | https://tuxedolabsorg.github.io/mplib/ |
| **mplib Source** | https://github.com/tuxedolabsorg/mplib |
| **Voxagon Blog (Networking)** | https://blog.voxagon.se/2026/03/13/teardown-multiplayer.html |
| **Steam Workshop** | https://steamcommunity.com/app/1167630/workshop/ |
| **Discord** | https://discord.gg/teardown |
| **Video Tutorials** | 10 MP tutorials + 12 modding basics on YouTube |
