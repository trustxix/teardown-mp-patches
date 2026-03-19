#version 2
#include "script/include/player.lua"

local toolId = ""
local selectTimer = 0

function server.init()
    toolId = GetString("savegame.mod.test.toolid")
end

function server.tick(dt)
    for p in PlayersAdded() do
        selectTimer = 2.0
    end
    if selectTimer > 0 then
        selectTimer = selectTimer - dt
        if selectTimer <= 0 and toolId ~= "" then
            for p in Players() do
                SetPlayerTool(toolId, p)
            end
        end
    end
end
