#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7 } end
function server.init()
    RegisterTool("wside", "Wrong", "MOD/vox/gun.vox", 5)
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("wside", true, p)
        SetToolAmmo("wside", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
end
function client.tick(dt)
    for p in PlayersAdded() do players[p] = createPlayerData() end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        if IsPlayerLocal(p) and GetPlayerTool(p) == "wside" then
            if InputPressed("usetool", p) then
                local eye = GetPlayerEyeTransform(p)
                local dir = TransformToParentVec(eye, Vec(0, 0, -1))
                Shoot(eye.pos, dir, "bullet", 1.0, 100, p, "wside")
            end
        end
    end
end
