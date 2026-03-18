# mplib Internals — How Loot, Drops, and Crates Actually Work

> Extracted from `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/mpclassics/mplib/tools.lua`
> This is the engine that powers ammo crates, loot spawning, and weapon drops in all official MP game modes.
> **Understanding this is essential for making our modded tools integrate correctly.**

---

## Why This Matters for Our Mods

When we call `SetToolAmmoPickupAmount("toolid", amount)` in `server.init()`, we're telling this exact system how to handle our tool. Without it, mplib can't spawn our tools in crates or let players pick them up. With it, our tools automatically appear in loot tables alongside official weapons.

---

## Custom Tool Detection

mplib finds our modded tools by checking a flag the engine sets automatically when `RegisterTool()` is called:

```lua
local tools = ListKeys("game.tool")
for i = 1, #tools do
    local toolId = tools[i]
    if GetBool("game.tool."..toolId..".custom") then
        -- This tool is from a mod — add to loot table
    end
end
```

**The `.custom` flag is set automatically by the engine** when `RegisterTool()` is called. We don't need to set it manually.

---

## Loot Table Structure

Each loot entry is a table with:
```lua
{
    name = "tool_id_string",    -- Tool ID to spawn
    weight = 10,                -- Probability weight (higher = more likely)
    amount = 20                 -- Ammo count when spawned in crate
}
```

**Selection algorithm:** Sums all weights, picks random float in `[0, weightSum]`, iterates entries accumulating weights until exceeded. Higher weight = higher spawn probability.

### How Game Modes Use Loot Tables

From official deathmatch:
```lua
lootTables[1] = {{name="steroid", weight=10, amount=4}}              -- low tier (gray crates)
lootTables[2] = {{name="shotgun", weight=7}, {name="gun", weight=7}} -- mid tier (blue crates)
lootTables[3] = {{name="rifle", weight=9}, {name="rocket", weight=10}} -- high tier (red crates)

-- This is where our mods get added automatically:
toolsAddModToolsToLootTable(lootTables[2], 3)   -- adds ALL custom mod tools to mid tier
toolsAddModToolsToLootTable(lootTables[3], 3)   -- AND to high tier
```

**Default weight for mod tools:** 3 (lower than built-in weapons). The `amount` comes from `GetToolAmmoPickupAmount(toolId)`, defaulting to 20 if not set.

---

## Loot Tier System

Tiers map to level markup:
- **Tier 1** → `ammospawn rarity=low` (gray crates)
- **Tier 2** → `ammospawn rarity=medium` (blue crates)
- **Tier 3** → `ammospawn rarity=high` (red crates)

Each tier has independent spawn points with their own timers.

### Configuration Defaults

```lua
respawnTime = 10.0     -- Seconds until loot respawns after pickup
despawnTime = 30.0     -- Seconds until unplayed crates disappear
despawnRange = 30.0    -- Distance from ALL players before despawn counter starts
```

- `toolsSetRespawnTime(seconds)` — changes respawn timer
- Despawn only happens when ALL players are beyond `despawnRange` from the crate

---

## Tool Drops on Death

When a player dies, mplib drops all their tools as physical pickups:

### Process
1. Listens for `GetEventCount("playerdied")` / `GetEvent("playerdied", i)` events
2. For each death, iterates all tools checking `IsToolEnabled(toolId, victim)`
3. Drops any tool with `GetToolAmmo(toolId, victim) > 0`
4. Spawns physical tool model via `SpawnTool(toolId, transform, false, scale)`
5. Clears the tool from the dead player: `SetToolEnabled(toolId, false, victim)` + `SetToolAmmo(toolId, 0, victim)`

### Drop Location
- Base position: 1 unit above player death position
- Random offset: random direction vector scaled by 0.5 units
- Creates a small sphere of drop positions around the death location

### Non-Droppable Tools
Hardcoded: `"sledge"`, `"spraycan"`, `"extinguisher"`
Plus any tool registered via `toolsPreventToolDrop(toolId)` (used for CTF flags, etc.)

---

## Custom Tool Crate Spawning

When mplib spawns our custom tool in a crate, it:

1. **Precomputes tool dimensions** at init (spawns the tool once, measures it, deletes it)
2. **Creates an ammo crate** using `prop/toolcrate_open.vox` as the container
3. **Places our tool model inside** the crate, scaled and rotated based on its longest axis:
   - Axis 1 (X longest): 80° rotation around Z, pointing upward
   - Axis 2 (Y longest): 20° rotation around Z
   - Axis 3 (Z longest): 80° rotation around X
   - Plus 10° Y rotation for visual variation
4. **Tags the entity** with: `mp-builtin-ammo`, `tool=TOOLID`, `amount=N`, `interact=loc@PICK_UP`

### Pickup Mechanics

When a player interacts with a tagged crate:
```lua
if HasTag(interactBody, "mp-builtin-ammo") then
    local amount = GetTagValue(interactBody, "amount")
    local tool = GetTagValue(interactBody, "tool")

    if IsToolEnabled(tool, p) then
        -- Player already has tool: add ammo
        SetToolAmmo(tool, GetToolAmmo(tool, p) + amount, p)
    else
        -- New tool: enable and equip
        SetToolEnabled(tool, true, p)
        SetPlayerTool(tool, p)
        SetToolAmmo(tool, amount, p)
    end

    Delete(interactBody)  -- Remove crate
end
```

---

## Public API Summary

| Function | Purpose | Called By |
|----------|---------|----------|
| `toolsInit()` | Reset loot system | Game mode init |
| `toolsSetRespawnTime(seconds)` | Change crate respawn timer | Game mode init |
| `toolsSetDropToolsOnDeath(bool)` | Enable/disable death drops | Game mode init |
| `toolsPreventToolDrop(toolId)` | Block specific tool from dropping | Game mode init (CTF flags) |
| `toolsAddModToolsToLootTable(table, weight)` | Auto-add all custom mod tools | Game mode init |
| `toolsAddLootTier(transforms, lootTable)` | Create a loot tier with spawn points | Game mode init |
| `toolsCleanup()` | Delete all spawned entities | Game mode destroy |
| `toolsTick(dt)` | Main loop (respawn, pickup, despawn) | server.tick |

---

## What Our Mods Need (Minimum)

For full integration with official MP game modes:

```lua
function server.init()
    RegisterTool("toolid", "Tool Name", "MOD/prefab/tool.xml", 6)
    SetToolAmmoPickupAmount("toolid", 20)  -- THIS enables loot crate integration
end
```

That's it. With those two lines, mplib will:
1. Detect our tool via the `.custom` flag
2. Add it to mid and high tier loot tables (weight=3)
3. Spawn it in ammo crates on the map
4. Let players pick it up with proper ammo
5. Drop it on death with remaining ammo
6. Track kills via the event system (if we use `Shoot()` or `ApplyPlayerDamage()`)

---

## All mplib Modules

| Module | Size | Purpose |
|--------|------|---------|
| `tools.lua` | 18,826 bytes | Loot, crates, drops (documented above) |
| `hud.lua` | Large | Damage indicators, timer, scoreboard, respawn, settings UI |
| `spawn.lua` | Medium | Player spawn/respawn at location nodes |
| `spectate.lua` | Medium | Third-person death camera, player cycling |
| `eventlog.lua` | Medium | Kill feed messages (top-right corner) |
| `stats.lua` | Small | Kill/death counts per player |
| `teams.lua` | Medium | Dynamic team assignment, player coloring, team UI |
| `ui.lua` | Medium | Standardized UI helpers (text, panels, buttons) |
| `util.lua` | Small | Spawn point extraction from level tags |
| `countdown.lua` | Small | Pre-round countdown timer |
| `mp.lua` | 389 bytes | Core multiplayer entry point |

**Location:** `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/mpclassics/mplib/`
