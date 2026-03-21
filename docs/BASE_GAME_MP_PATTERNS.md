# Base Game MP Sync Patterns — Research Analysis

> **Source:** Official Teardown scripts from `data/script/`, `data/script/mpcampaign/`, `dlcs/wildwestheist/script/tools/`, `data/built-in/script/vehicle/`
>
> **Purpose:** Document how the base game achieves rock-solid MP sync so we can apply the same patterns to our mods.

---

## Executive Summary

The base game uses **5 core sync mechanisms**, prioritized in this order:

1. **Engine-native functions** — `Shoot()`, `Explosion()`, `Spawn()`, `SetToolAmmo()`, etc. are automatically synced by the engine when called on the server. No RPC needed.
2. **Registry broadcast** — `SetInt/SetFloat/SetBool/SetString(key, value, true)` with the `true` flag broadcasts to all clients instantly.
3. **`shared.*` tables** — Server writes, all clients read. Automatic sync every frame.
4. **`ClientCall(0, ...)`** — Server → all clients for one-time events (death, pickup notifications, UI updates).
5. **`ServerCall(...)`** — Client → server for player actions (team join, unstuck, play button).

**The base game almost NEVER uses per-tick RPC.** State is synced via registry or shared tables. RPC is reserved for discrete events.

---

## Pattern 1: Server Owns All Game Logic

Every base game weapon/tool follows the same rule: **the server handles input, physics, damage, and spawning. The client only handles visuals and animation.**

### Snowball (Projectile Weapon)
```lua
-- SERVER: spawns projectile, tracks physics, detects collision
function server.tick(dt)
    for i in Players() do
        if GetPlayerTool(i) == "snowball" then
            SetToolAmmo("snowball", 9999, i)
            if InputPressed("usetool", i) and GetPlayerCanUseTool(i) then
                local t = GetPlayerEyeTransform(i)
                local fwd = TransformToParentVec(t, Vec(0,0,-1))
                local pos = TransformToParentPoint(t, Vec(0.3, -0.3, -0.5))
                local vel = VecAdd(VecScale(fwd, 16), Vec(0, 4, 0))
                local entities = Spawn("<body dynamic='true'><vox file='snowball.vox'/></body>", Transform(pos))
                local body = entities[1]
                SetBodyVelocity(body, vel)
                balls[#balls+1] = { body = body, player = i }
                PlaySound(throw, pos)
            end
        end
    end
end

-- CLIENT: only handles ToolAnimator for all players
function client.tick(dt)
    for p in PlayersAdded() do
        toolAnimators[p] = ToolAnimator()
    end
    for p in PlayersRemoved() do
        toolAnimators[p] = nil
    end
    for p in Players() do
        if GetPlayerTool(p) == "snowball" then
            tickToolAnimator(toolAnimators[p], dt, nil, p)
        end
    end
end
```

**Lesson:** Spawned physics bodies are automatically replicated to all clients. No need for ClientCall to sync projectile positions.

### Tank (Vehicle Weapon)
```lua
-- SERVER: per-player input check + explosion
function server.tick(dt)
    for j in Players() do
        if InputDown("vehicleraise", j) then
            -- fire projectile, track it, on impact:
            Explosion(impactPoint, explosionSize)
            -- sync ammo to all clients:
            for p in Players() do
                ClientCall(p, "client.setAmmo", ammo)
            end
        end
    end
end

-- CLIENT: only haptic feedback + ammo display
function client.tick(dt)
    if InputDown("vehicleraise") then
        PlayHapticEffect(...)  -- local feedback only
    end
end

function client.setAmmo(a)
    ammo = a  -- received from server
end
```

**Lesson:** `Explosion()` on the server auto-syncs to all clients. Ammo display is synced via a simple ClientCall, not per-tick polling.

---

## Pattern 2: Registry Broadcast for Tool State

The base game manages ALL tool state through registry keys with the broadcast flag:

```lua
-- Enable tool for a player (broadcasts to all)
SetBool("game.tool."..toolId..".enabled", true, true)

-- Set ammo (broadcasts to all)
SetInt("game.tool."..toolId..".ammo", value, true)
SetInt("game.tool."..toolId..".ammo.max", value, true)

-- Set upgrade properties (broadcasts to all)
SetInt("game.tool."..toolId.."."..prop, value, true)

-- Level-wide settings
SetBool("level.sandbox", false, true)
SetFloat("level.health", healthValue, true)
```

**Lesson:** Our mods should use `SetInt/SetFloat/SetBool` with `true` for any state that clients need to read. This replaces per-tick ServerCall/ClientCall for continuous state.

---

## Pattern 3: Explosion Propagation via Registry

The base game uses a registry-based fire-and-forget pattern for explosion visuals:

```lua
-- SERVER: calls Explosion() which auto-sets registry keys
Explosion(pos, strength)
-- Engine internally sets: game.explosion.x, game.explosion.y, game.explosion.z, game.explosion.strength

-- CLIENT (explosionclient.lua): polls registry each tick
function client.tick(dt)
    if HasKey("game.explosion") then
        local strength = GetFloat("game.explosion.strength")
        local pos = Vec(GetFloat("game.explosion.x"), GetFloat("game.explosion.y"), GetFloat("game.explosion.z"))
        if strength >= 2 then
            explosionLarge(pos)
        elseif strength >= 1 then
            explosionMedium(pos)
        else
            explosionSmall(pos)
        end
        ClearKey("game.explosion")  -- Clear after reading to prevent re-processing
    end
end
```

**Lesson:** For custom explosion effects in our mods, we can use this same HasKey/ClearKey pattern to propagate one-time events through the registry without RPC.

---

## Pattern 4: shared.* Tables for Real-Time State

The mpcampaign scripts use `shared.*` extensively for state that the client needs to display:

```lua
-- SERVER writes:
shared.respawnTimeLeft = {}
shared._statsState = {}      -- { [playerId] = {kills=N, deaths=N} }
shared._teamState = { teams={}, state=_WAITING }
shared._hud = { useDamageIndicators=true, gameIsSetup=false }

-- CLIENT reads (every frame, automatically synced):
function client.draw()
    local timeLeft = shared.respawnTimeLeft[GetLocalPlayer()]
    local kills = shared._statsState[p] and shared._statsState[p].kills or 0
end
```

**Lesson:** For mod state that needs to be visible to all clients (ammo counts in HUD, settings states, tool configurations), `shared.*` is the cleanest approach. No polling, no RPC — just write on server, read on client.

---

## Pattern 5: Event-Driven Death/Damage Processing

The base game NEVER polls for deaths. It uses the event queue:

```lua
-- Process deaths exactly once per tick
local c = GetEventCount("playerdied")
for i = 1, c do
    local victim, attacker, _, _, _, _, _ = GetEvent("playerdied", i)
    -- Drop tools, update stats, notify clients
end

-- Process damage exactly once per tick
local c = GetEventCount("playerhurt")
for i = 1, c do
    local victim, before, after, attacker, point, impulse = GetEvent("playerhurt", i)
    -- Damage indicators, hit feedback
end
```

**Lesson:** Our mods should use `GetEventCount`/`GetEvent` for death/damage handling instead of polling `GetPlayerHealth()` each tick.

---

## Pattern 6: ToolAnimator for ALL Players

The base game calls `tickToolAnimator` for EVERY player, not just the local player:

```lua
function client.tick(dt)
    for p in PlayersAdded() do
        toolAnimators[p] = ToolAnimator()
        toolAnimators[p].armPitchScale = 0.2
        toolAnimators[p].toolPitchScale = 0.1
    end
    for p in PlayersRemoved() do
        toolAnimators[p] = nil
    end
    for p in Players() do
        if GetPlayerTool(p) == "snowball" then
            tickToolAnimator(toolAnimators[p], dt, nil, p)
        end
    end
end
```

The ToolAnimator internally handles FP vs TP:
```lua
function tickToolAnimator(toolAnimator, dt, defaultPoseTransform, playerId)
    local thirdPerson = (playerId and playerId > 0 and not IsPlayerLocal(playerId))
                        or GetBool("game.thirdperson")
    local prefix = thirdPerson and "tp_" or "fp_"
    -- Uses prefix to select correct pose transforms from tool prefab
end
```

**Lesson:** Our mods must call `tickToolAnimator` for ALL players in the `client.tick` loop, not just the local player. The function auto-selects FP/TP poses. This is why remote players see proper tool animations in the base game.

---

## Pattern 7: Tool Pickup via Tagged Bodies

The mplib tool system uses body tags for pickup detection:

```lua
-- Dropped tool bodies have these tags:
-- "mp-builtin-ammo" (marker tag)
-- "tool" = toolId (which tool)
-- "amount" = ammoCount (how much ammo)

-- Server pickup loop:
for p in Players() do
    if GetPlayerHealth(p) > 0 and InputPressed("interact", p) then
        local interactBody = GetPlayerInteractBody(p)
        if HasTag(interactBody, "mp-builtin-ammo") then
            local tool = GetTagValue(interactBody, "tool")
            local amount = GetTagValue(interactBody, "amount")
            if IsToolEnabled(tool, p) then
                SetToolAmmo(tool, GetToolAmmo(tool, p) + tonumber(amount), p)
            else
                SetToolEnabled(tool, true, p)
                SetToolAmmo(tool, tonumber(amount), p)
                SetPlayerTool(tool, p)
            end
            Delete(interactBody)
            PlaySound(refillSound, GetBodyTransform(interactBody).pos)
        end
    end
end
```

**Lesson:** Our mods using `SetToolAmmoPickupAmount()` integrate with this system. Without it, mplib doesn't know how to spawn ammo crates for custom tools.

---

## Pattern 8: Per-Player State Tables

Every base game system indexes state by player ID:

```lua
_hud.healthBarData[p] = { damage=0, decay=-1.0, alpha=0.0, health=GetPlayerHealth(p) }
_spawnState.deadTime[p] = 0.0
shared._statsState[p] = { kills=0, deaths=0 }
characters[p] = { entities={}, shapes={}, animator=0 }
toolAnimators[p] = ToolAnimator()
```

Cleanup always happens in `PlayersRemoved()`:
```lua
for p in PlayersRemoved() do
    toolAnimators[p] = nil
    characters[p] = nil  -- after deleting entities
    _spawnState.deadTime[p] = nil
end
```

**Lesson:** Our `createPlayerData()` pattern matches this exactly. The key addition: always clean up in `PlayersRemoved()`.

---

## Pattern 9: ClientCall(0, ...) for World Events

The base game uses `ClientCall(0, ...)` (player 0 = all clients) for events visible to everyone:

```lua
-- Server detects death → tells all clients to show ragdoll
ClientCall(0, "client.character_die", victim)

-- Server detects respawn → tells all clients to show character
ClientCall(0, "client.character_live", victim)

-- Server detects hit on dead body → tells all clients to show impact
ClientCall(0, "client.character_hit", victim, point, impulse)
```

**Lesson:** Use `ClientCall(0, ...)` for world-visible events. Use `ClientCall(p, ...)` only for personal feedback (camera shake, HUD updates for one player). This matches our Issue #58 rule.

---

## Pattern 10: Sound Placement Rules

| Context | Function | Synced? |
|---------|----------|---------|
| Server game event | `PlaySound(snd, pos)` | Yes — engine syncs to all clients |
| Client UI feedback | `UiSound("path.ogg")` | No — local only |
| Client haptic | `PlayHapticEffect(...)` | No — local only |

**Lesson:** `PlaySound()` on the server is automatically heard by all clients. Our mods should NOT use `ClientCall(0, "client.playSound", ...)` for game sounds — just call `PlaySound()` on the server directly.

---

## Pattern 11: Tools Settings via XML (Not Lua)

Tool physics properties are defined in `tools_settings.xml`, NOT in Lua:

```xml
<tool name="gun">
    <path value="prefab/tool/gun.xml"/>
    <tool_recoil value="0.2"/>
    <body_recoil value="0.2"/>
    <cooldown value="0.2"/>
    <group value="3"/>
    <target_zoom value="1.2"/>
    <hold_as_repeat value="false"/>
</tool>
```

**Lesson:** Workshop mods can't modify engine-level tool settings like recoil and cooldown — these are hardcoded in XML. Custom recoil in mods must be done via ToolAnimator pose manipulation, not engine settings.

---

## Pattern 12: DLC Weapons are Single-Player Only

**Critical finding:** The Wild West DLC weapons (revolver, rifle, pickaxe, dynamite, TNT, powder) are ALL v1 single-player scripts. They have:
- No `#version 2`
- No `server.*`/`client.*` callbacks
- No player iteration
- `Shoot()` called without player/tool ID (no kill attribution)

This means:
1. DLC weapons don't work in MP out of the box
2. Only the base game tools (sledge, gun, shotgun, etc.) and the mpcampaign scripts are MP-ready
3. The tank vehicle IS v2 MP-ready (has full server/client split)

---

## Actionable Improvements for Our Mods

### High Impact (Apply to all mods)

| # | Current Pattern | Base Game Pattern | Action |
|---|----------------|-------------------|--------|
| 1 | `ServerCall` every tick for ammo sync | Registry `SetInt(..., true)` | Replace per-tick ammo RPCs with registry broadcast |
| 2 | Manual `ClientCall` for sounds | `PlaySound()` on server | Remove sound ClientCalls, call PlaySound on server directly |
| 3 | ToolAnimator only for local player | ToolAnimator for ALL players | Add `for p in Players()` loop around tickToolAnimator |
| 4 | Polling `GetPlayerHealth()` for deaths | `GetEventCount("playerdied")` | Switch to event-driven death detection |
| 5 | Missing `PlayersRemoved()` cleanup | Always clean up per-player state | Add cleanup loop to all mods |

### Medium Impact (Apply where relevant)

| # | Pattern | Action |
|---|---------|--------|
| 6 | Custom settings sync via ServerCall | Use `shared.*` tables for settings state |
| 7 | Missing SetToolAmmoPickupAmount | Add to all weapon mods for mplib crate integration |
| 8 | `ClientCall(p, ...)` for world-visible effects | Use `ClientCall(0, ...)` instead |
| 9 | Manual explosion visual sync | Use registry HasKey/ClearKey pattern |

### Low Impact (Nice-to-have)

| # | Pattern | Action |
|---|---------|--------|
| 10 | Hardcoded spawn positions | Use `FindLocations("playerspawn")` pattern |
| 11 | No tool drop on death | Implement mplib-compatible drop system |
| 12 | No loadout system | Add default loadout on respawn |

---

## Reference: Key Engine Functions That Auto-Sync

These functions, when called on the server, are automatically replicated to all clients by the engine. **No RPC needed:**

| Function | What It Syncs |
|----------|---------------|
| `Shoot(pos, dir, type, dmg, range, p, toolId)` | Bullet trace + damage + kill feed |
| `Explosion(pos, strength)` | Physics + terrain destruction + visual |
| `Spawn(xml, transform)` | New entity visible to all |
| `Delete(handle)` | Entity removal on all clients |
| `SetBodyVelocity(body, vel)` | Physics state |
| `ApplyBodyImpulse(body, pos, impulse)` | Physics impulse |
| `MakeHole(pos, r1, r2, r3)` | Terrain destruction |
| `SpawnFire(pos)` | Fire propagation |
| `SetToolAmmo(id, amount, p)` | Ammo count for player |
| `SetToolEnabled(id, bool, p)` | Tool availability |
| `SetPlayerTool(id, p)` | Currently equipped tool |
| `SetPlayerHealth(health, p)` | Player health |
| `RespawnPlayer(p)` | Full respawn |
| `SetPlayerTransform(t, p)` | Player position |
| `SetPlayerColor(r, g, b, p)` | Player color |
| `PlaySound(snd, pos)` | Positional audio |

---

## Compliance Status (auto-detected by lint)

Three lint rules now enforce base game patterns. Run `python -m tools.lint` to check.

| Rule | What it catches | Auto-fix? |
|------|----------------|-----------|
| `CLIENTCALL-SOUND` | ClientCall wrapping PlaySound instead of server-side PlaySound | No — requires manual refactor |
| `TOOLANIM-LOCAL-ONLY` | tickToolAnimator gated behind IsPlayerLocal | No — requires restructuring |
| `MISSING-PLAYERS-REMOVED` | PlayersAdded without matching PlayersRemoved cleanup | **Yes** — `python -m tools.fix --only missing-players-removed` |

### Current Violations (as of 2026-03-21)

| Pattern | Mods Affected | Findings | Priority |
|---------|--------------|----------|----------|
| CLIENTCALL-SOUND | 8 mods | 30 | Medium — works but adds unnecessary RPC overhead |
| MISSING-PLAYERS-REMOVED | 10 mods | 11 | High — causes state leaks on player disconnect |
| TOOLANIM-LOCAL-ONLY | 0 mods | 0 | N/A — all mods compliant |

**Mods needing CLIENTCALL-SOUND fixes:** CnC_Weather_Machine, FPV_Drone_Tool, Hurricanes_and_Blizzards, Koenigsegg_Agera_MP, Magnetizer_V2, Multiplayer_Spawnable_Pack, Service_Vehicles_MP, Toyota_Supra_MP

**Mods needing MISSING-PLAYERS-REMOVED fixes:** AC130_Airstrike_MP, Advanced_Tornado, Bomb_Attack, Bunker_Buster_MP, CnC_Weather_Machine, Drivable_Plane, Molotov_Cocktail, Object_Possession, Predator_Missile_MP, Thruster_Tool_Multiplayer
