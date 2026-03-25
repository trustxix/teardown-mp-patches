----------------------------------------------------------------
-- DEF CONVERSION GUIDE — Before/After Example
-- Shows exactly how to convert a v1 tool mod using DEF v1.2
--
-- BEFORE (v1 — silently disabled in MP):
--
--   function init()
--       RegisterTool("my-gun", "My Gun", "MOD/vox/gun.vox")
--       SetBool("game.tool.my-gun.enabled", true)
--       snd = LoadSound("MOD/snd/fire.ogg")
--       ammo = 30
--       cooldown = 0
--   end
--   function tick(dt)
--       cooldown = math.max(0, cooldown - dt)
--       if GetString("game.player.tool") == "my-gun" then
--           if InputPressed("lmb") and cooldown <= 0 and ammo > 0 then
--               local t = GetCameraTransform()
--               local dir = TransformToParentVec(t, Vec(0, 0, -1))
--               QueryRaycast(...)  -- manual hit detection
--               MakeHole(...)      -- manual terrain damage
--               PlaySound(snd, t.pos)
--               ammo = ammo - 1
--               cooldown = 0.2
--           end
--       end
--   end
--   function draw()
--       UiText("Ammo: " .. ammo)
--   end
--
-- PROBLEMS WITH V1 IN MP:
-- - No #version 2 → script silently disabled
-- - Global variables → no per-player state
-- - InputPressed("lmb") → raw key, no player param
-- - GetCameraTransform → wrong in MP, need GetPlayerEyeTransform(p)
-- - GetString("game.player.tool") → need GetPlayerTool(p)
-- - No PlayersAdded/Removed loops → state never initialized/cleaned
-- - No ToolAnimator → tool model frozen for other players
-- - QueryRaycast+MakeHole → should use Shoot() for proper MP sync
-- - Single draw() → need client.draw() with GetLocalPlayer()
--
-- AFTER (v2 + DEF — works in MP, zero desync):
----------------------------------------------------------------
#version 2
#include "script/include/player.lua"
#include "lib/def.lua"

-- 1. Register tool (DEF handles RegisterTool, SetToolEnabled,
--    SetToolAmmo, ammo display suppression, ToolAnimator)
tool = DEF.Tool("my-gun", {
    displayName = "My Gun",
    prefab = "MOD/vox/gun.vox",
    group = 6,
    ammoPickup = 15,
    ammo = 30,
})

-- 2. Load sounds (DEF reloads in both server.init + client.init)
snd_fire = tool:LoadSound("MOD/snd/fire.ogg")

-- 3. Per-player state (server and client get SEPARATE copies)
tool:PlayerData(function()
    return {
        cooldown = 0,
        magazine = 30,
    }
end)

-- 4. Server tick: ALL game logic (damage, ammo, physics)
tool:ServerTick(function(p, data, dt)
    tool:TickTimer(data, "cooldown", dt)

    if tool:InputPressed("usetool", p) and data.cooldown <= 0 and data.magazine > 0 then
        local aim = tool:GetAim(p)

        -- Shoot() handles: terrain, players, kill feed, bullet trace, MP sync
        tool:Fire(aim.pos, aim.dir, { damage = 20, range = 100 }, p)

        -- PlaySound on server auto-syncs to all clients
        tool:PlaySound(snd_fire, aim.pos)

        data.magazine = data.magazine - 1
        data.cooldown = 0.2

        -- Sync to client for HUD (separate state tables, so must be explicit)
        tool:SyncToClient("magazine", data.magazine, p)
    end
end)

-- 5. Client tick: ONLY visuals (particles, lights, etc.)
tool:ClientTick(function(p, data, dt)
    -- Add muzzle flash, recoil spring, etc. here
    -- ToolAnimator for all players is auto-wired by DEF
    -- SpawnParticle/PointLight/DrawLine are CLIENT-ONLY (never on server)
end)

-- 6. HUD: auto-gated to local player + tool equipped
tool:Draw(function(p, data)
    local mag = tool:ReadSync("magazine", p, 30)
    UiText("Ammo: " .. mag)
end)

-- 7. Client-only init (for LoadLoop or other client-only APIs)
-- tool:ClientInit(function()
--     snd_loop = LoadLoop("MOD/snd/loop.ogg")  -- LoadLoop is client-only
-- end)

----------------------------------------------------------------
-- WHAT DEF v1.2 HANDLES AUTOMATICALLY:
--
-- Registration:
--   RegisterTool + SetToolAmmoPickupAmount in server.init
--   SetToolEnabled + SetToolAmmo per player in PlayersAdded
--   SetString("game.tool.X.ammo.display", "") to hide engine HUD
--
-- Lifecycle:
--   PlayersAdded / PlayersRemoved / Players loops (server + client)
--   Iterator collection (called once per tick, shared across tools)
--   Per-player state cleanup on disconnect
--   ToolAnimator for ALL players (FP/TP handled internally)
--
-- Safety:
--   Separate _serverPlayers / _clientPlayers tables (no double-processing)
--   Safe input routing (raw keys → client-only, usetool → player-aware)
--   Top-level callbacks (survives v2 preprocessor chunk splitting)
--   Sound loading in both server + client init
--
-- ISSUES PREVENTED BY DESIGN:
--   #2   Raw key + player param         → tool:InputPressed routes safely
--   #42  Double-processing on host       → separate state tables
--   #51  Missing player ID              → tool:InputPressed includes context
--   #56  Explosion no damage            → tool:Fire uses Shoot()
--   #63  Missing MOD/ prefix            → config requires full paths
--   #67  No callback defined            → server.init auto-wired
--   #69  Shared players[p] 2x           → _serverPlayers vs _clientPlayers
--   #75  local at file scope            → framework uses globals
--   #80  Preprocessor breaks closures   → callbacks at top level
--   #81  Iterator consumed              → collected into tables once
--   #82  goto in Lua 5.1               → no goto used anywhere
--   #83  SpawnParticle on server        → ClientTick pattern enforced
--   #84  Timer not synced              → SyncToClient/ReadSync pattern
--   #85  LoadLoop at file scope         → ClientInit hook
--   #86  Distance from origin           → framework pattern uses origin
--   #87  Flag-based cleanup             → nil assignment pattern
--   #88  Phantom API                    → verified API only
----------------------------------------------------------------
