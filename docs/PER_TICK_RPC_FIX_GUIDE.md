# PER-TICK-RPC Fix Guide

> **Problem:** 69 mods had `ServerCall`/`ClientCall` inside tick/update functions without input guards.
> This floods the reliable network channel every frame, causing lag spikes and input delay.
> The lint rule `PER-TICK-RPC` flags these.
>
> **Status (2026-03-19):** All 69 findings resolved. 0 PER-TICK-RPC findings across 178 mods. Guide kept for reference.

---

## Decision Tree

When you see a PER-TICK-RPC finding, read the surrounding code and ask:

```
Is this RPC triggered by player input?
├── YES → Wrap in InputPressed/InputDown guard
│         (Already correct pattern, just needs the guard)
│
└── NO → Is it syncing continuous state (position, rotation, timer)?
    ├── YES → Convert to registry sync (SetFloat/SetBool with sync=true)
    │
    └── NO → Is it a one-time event that happens to be in tick?
        ├── YES → Move to a flag-based trigger (only call once when condition changes)
        │
        └── NO → Evaluate if the RPC is actually needed every tick
            └── Usually it isn't — find the semantic trigger
```

---

## Fix Pattern 1: Add Input Guard

**When:** The RPC is clearly triggered by a player action (fire, reload, mode switch).

```lua
-- BEFORE (flagged by lint):
function client.tickPlayer(p, dt)
    local data = players[p]
    if data.firing then
        ServerCall("server.fire", data.aimX, data.aimY, data.aimZ)
    end
end

-- AFTER (clean):
function client.tickPlayer(p, dt)
    local data = players[p]
    if InputDown("usetool") and not data.optionsOpen then
        ServerCall("server.fire", data.aimX, data.aimY, data.aimZ)
    end
end
```

**Why this works:** `InputDown("usetool")` only fires when the player is holding the trigger. The RPC only sends during active input, not every frame.

**Note:** If the ServerCall is already inside an `InputPressed`/`InputDown` block but the lint can't see it (block is >3 lines above), add `-- @lint-ok PER-TICK-RPC` to suppress.

---

## Fix Pattern 2: Convert to Registry Sync

**When:** The RPC syncs continuous state (position, rotation, speed, angle) that changes smoothly over time.

```lua
-- BEFORE (flagged — sends RPC every tick):
function client.tickPlayer(p, dt)
    local data = players[p]
    ServerCall("server.updateDronePos", data.droneX, data.droneY, data.droneZ)
end

-- AFTER (clean — uses engine-managed sync):
function server.tickPlayer(p, dt)
    local data = players[p]
    SetFloat("mod."..p..".droneX", data.droneX, true)
    SetFloat("mod."..p..".droneY", data.droneY, true)
    SetFloat("mod."..p..".droneZ", data.droneZ, true)
end

function client.tickPlayer(p, dt)
    -- Read synced values (engine handles batching and prioritization)
    local x = GetFloat("mod."..p..".droneX")
    local y = GetFloat("mod."..p..".droneY")
    local z = GetFloat("mod."..p..".droneZ")
end
```

**Why this works:** Registry sync with `sync=true` uses the engine's unreliable channel (batched, prioritized, ~1 Mbit/client). RPC uses the reliable channel which queues up and causes lag.

---

## Fix Pattern 3: Flag-Based Trigger

**When:** The RPC should only fire once when a condition changes, but the code calls it every tick the condition is true.

```lua
-- BEFORE (flagged — sends every tick while scope is active):
function client.tickPlayer(p, dt)
    local data = players[p]
    if data.scopeActive then
        ServerCall("server.setScope", true)
    end
end

-- AFTER (clean — only sends on state change):
function client.tickPlayer(p, dt)
    local data = players[p]
    local scopeNow = InputDown("rmb")
    if scopeNow ~= data.lastScopeState then
        data.lastScopeState = scopeNow
        ServerCall("server.setScope", scopeNow)
    end
end
```

**Why this works:** The RPC only fires on the frame the state transitions, not every frame it's active.

---

## Fix Pattern 4: Legitimate Per-Tick — Suppress

**When:** After careful analysis, the RPC truly needs to run every tick (rare — usually for guided projectiles where server needs continuous input).

```lua
-- Suppress with lint comment:
function client.tickPlayer(p, dt)
    local data = players[p]
    if data.guidedMissileActive and IsPlayerLocal(p) then
        local aim = GetPlayerAimInfo(p)
        ServerCall("server.guideMissile", aim[1], aim[2], aim[3]) -- @lint-ok PER-TICK-RPC
    end
end
```

**Before suppressing, verify:**
1. Can this use registry sync instead? (Usually yes)
2. Is it gated by a condition that limits how often it fires? (Should be)
3. Does it include `IsPlayerLocal(p)` to avoid running for remote players?

---

## Common PER-TICK-RPC Patterns in Our Mods

| Pattern | Frequency | Recommended Fix |
|---------|-----------|-----------------|
| Continuous fire (auto weapons) | High | Should already have InputDown guard — add if missing |
| Scope/zoom state sync | Medium | Flag-based trigger (Pattern 3) |
| Projectile guidance (missiles, drones) | Medium | Registry sync (Pattern 2) or suppress with IsPlayerLocal gate |
| Position sync (attached objects, grapple points) | Low | Registry sync (Pattern 2) |
| Animation state sync | Low | Registry sync (Pattern 2) |

---

## Quick Checklist for Each Finding

- [ ] Read the surrounding 10 lines of code
- [ ] Identify the semantic purpose of the RPC
- [ ] Choose fix pattern (1-4) based on the decision tree
- [ ] Apply fix
- [ ] Run `python -m tools.lint --mod "ModName"` to verify
- [ ] Test in-game if the mod's behavior is affected
