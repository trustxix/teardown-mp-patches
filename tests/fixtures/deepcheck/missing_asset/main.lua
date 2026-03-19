#version 2
#include "script/include/player.lua"

players = {}
function createPlayerData() return { ammo = 7 } end

function server.init()
    RegisterTool("missingtool", "Missing Tool", "MOD/vox/tool.vox", 5)
end

function client.tick(dt)
    for p in Players() do
        if GetPlayerTool(p) == "missingtool" then
            PlaySound(LoadSound("MOD/snd/shoot.ogg"), GetPlayerEyeTransform(p).pos)
        end
    end
end
