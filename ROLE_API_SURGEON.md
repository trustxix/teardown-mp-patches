# Role: API Surgeon

You upgrade existing patched mods with the official multiplayer APIs discovered in RESEARCH.md.

## Your Task
Apply these 4 changes to every mod in `C:/Users/trust/Documents/Teardown/mods/`:

### 1. Replace MakeHole with Shoot() for gun mods
```lua
-- OLD (can't damage players):
MakeHole(hitPos, damage, damage * 0.7, damage * 0.4)

-- NEW (damages players + voxels, kill attribution):
Shoot(pos, dir, "bullet", damage, maxDist, p, "toolId")
```

### 2. Replace QueryRaycast with QueryShot + ApplyPlayerDamage for beam/melee mods
```lua
-- OLD:
local hit, dist, normal, shape = QueryRaycast(pos, dir, maxDist)

-- NEW:
local hit, dist, shape, player, hitFactor, normal = QueryShot(pos, dir, maxDist, 0, p)
if player then
    ApplyPlayerDamage(player, damage * dt * hitFactor, "toolId", p)
end
```

### 3. Replace manual aim with GetPlayerAimInfo()
```lua
-- OLD:
local ct = GetPlayerEyeTransform(p)
local fwd = TransformToParentVec(ct, Vec(0, 0, -1))
local hit, dist = QueryRaycast(ct.pos, fwd, 100)

-- NEW:
local b = GetToolBody(p)
local muzzlePos = (b ~= 0) and TransformToParentPoint(GetBodyTransform(b), muzzleOffset) or GetPlayerEyeTransform(p).pos
local _, pos, endPos, dir = GetPlayerAimInfo(muzzlePos, 100, p)
```

### 4. Add SetToolAmmoPickupAmount() to server.init()
```lua
function server.init()
    RegisterTool("toolId", "Name", "MOD/vox/tool.vox", group)
    SetToolAmmoPickupAmount("toolId", 30)  -- ADD THIS LINE
    -- ...
end
```

## Rules
- Work alphabetically through `C:/Users/trust/Documents/Teardown/mods/`
- Read each mod's main.lua before editing
- Keep MakeHole for NON-weapon effects (terrain destruction from explosions, environmental damage)
- Shoot() replaces MakeHole ONLY for bullet impacts that should damage players
- For infinite-ammo tools (Laser Cutter, Mjölner, etc.), set pickup amount to 0 or skip
- After each mod, verify: no `> 0` handle checks, no ipairs on iterators
- Do NOT restructure the mod — only swap the 4 API calls above
- Do NOT touch docs or create new mods
