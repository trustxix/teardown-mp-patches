#version 2
#include "script/include/player.lua"
players = {}
function createPlayerData() return { ammo = 7, coolDown = 0 } end
function server.init()
    RegisterTool("pistol", "Pistol", "MOD/vox/pistol.vox", 5)
    SetString("game.tool.pistol.ammo.display", "")
    SetToolAmmoPickupAmount("pistol", 7)
end
function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("pistol", true, p)
        SetToolAmmo("pistol", 101, p)
    end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        local data = players[p]
        if not data then return end
        data.coolDown = math.max(0, data.coolDown - dt)
    end
end
function server.shoot(p, pos, dir)
    local data = players[p]
    if not data or data.ammo <= 0 or data.coolDown > 0 then return end
    Shoot(pos, dir, "bullet", 1.0, 100, p, "pistol")
    data.ammo = data.ammo - 1
    data.coolDown = 0.15
    ClientCall(0, "client.onShoot", pos, dir)
    ClientCall(p, "client.onRecoil")
end
function client.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
    end
    for p in PlayersRemoved() do players[p] = nil end
    for p in Players() do
        if IsPlayerLocal(p) and GetPlayerTool(p) == "pistol" then
            if InputPressed("usetool", p) then
                local hit, dist, normal, shape = GetPlayerAimInfo(p)
                local eye = GetPlayerEyeTransform(p)
                local dir = TransformToParentVec(eye, Vec(0, 0, -1))
                ServerCall("server.shoot", p, eye.pos, dir)
            end
        end
    end
end
function client.onShoot(pos, dir)
    PlaySound(LoadSound("MOD/snd/shoot.ogg"), pos)
    SpawnParticle("smoke", pos, Vec(0, 0.5, 0), 0.5, 1)
end
function client.onRecoil()
    ShakeCamera(0.2)
end
function client.draw()
    local p = GetLocalPlayer()
    if not p then return end
    local data = players[p]
    if not data then return end
    if GetPlayerTool(p) == "pistol" then
        UiAlign("right")
        UiTranslate(UiWidth() - 50, UiHeight() - 80)
        UiText(data.ammo)
    end
end
