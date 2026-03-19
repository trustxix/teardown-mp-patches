#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7 } end
function server.init()
    RegisterTool("mygun", "My Gun", "MOD/vox/gun.vox", 5)
    SetString("game.tool.mygun.ammo.display", "")
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("MyGun", true, p)
        SetToolAmmo("my_gun", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
end
function client.draw()
    local p = GetLocalPlayer()
    if not p then return end
    if GetPlayerTool(p) == "MYGUN" then
        UiText("ammo: 7")
    end
end
