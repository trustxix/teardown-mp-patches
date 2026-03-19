#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7 } end
function server.init()
    RegisterTool("bchain", "Broken", "MOD/vox/gun.vox", 5)
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("bchain", true, p)
        SetToolAmmo("bchain", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
end
function server.fire(p, pos, dir)
    Shoot(pos, dir, "bullet", 1.0, 100, p, "bchain")
end
function client.tick(dt)
    for p in PlayersAdded() do players[p] = createPlayerData() end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        if IsPlayerLocal(p) and GetPlayerTool(p) == "bchain" then
            if InputPressed("usetool", p) then
                local eye = GetPlayerEyeTransform(p)
                local dir = TransformToParentVec(eye, Vec(0, 0, -1))
                ServerCall("server.shoot", p, eye.pos, dir)
            end
        end
    end
end
