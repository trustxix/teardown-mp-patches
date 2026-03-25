"""Convert regular gun mods to ARM-style with ToolAnimator + Shoot()."""
import os

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

GUNS = {
    "AK-47": {
        "tool_id": "ak47", "name": "AK-47", "vox": "MOD/vox/ak47.vox",
        "muzzle": "Vec(0.275, -0.6, -2.6)", "damage": "0.6", "rate": "0.085",
        "mag": "30", "reload": "1.7", "mags": "7", "auto": True,
        "sounds": {
            "gunsound": "MOD/snd/ak0.ogg", "cocksound": "MOD/snd/guncock.ogg",
            "reloadsound": "MOD/snd/reload.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
    "AWP": {
        "tool_id": "awp", "name": "AWP", "vox": "MOD/vox/AWP.vox",
        "muzzle": "Vec(0.35, -0.55, -3.5)", "damage": "1.3", "rate": "1.0",
        "mag": "10", "reload": "2.4", "mags": "4", "auto": False,
        "sounds": {
            "gunsound": "MOD/snd/awp_shot.ogg", "cocksound": "MOD/snd/awp_cock.ogg",
            "reloadsound": "MOD/snd/awp_reload.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
    "Desert_Eagle": {
        "tool_id": "deagle", "name": "Desert Eagle", "vox": "MOD/vox/deagle.vox",
        "muzzle": "Vec(0.3, -0.45, -2.4)", "damage": "1.0", "rate": "0.2",
        "mag": "7", "reload": "0.9", "mags": "6", "auto": False,
        "sounds": {
            "gunsound": "MOD/snd/deagle_shot.ogg", "cocksound": "MOD/snd/pistolcock.ogg",
            "reloadsound": "MOD/snd/deagle_reload.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
    "M1_Garand": {
        "tool_id": "cresta-m1garand", "name": "M1 Garand", "vox": "MOD/vox/m1garand.vox",
        "muzzle": "Vec(0.35, -0.6, -2.6)", "damage": "1.1", "rate": "0.3",
        "mag": "8", "reload": "1.5", "mags": "10", "auto": False,
        "sounds": {
            "gunsound": "MOD/snd/garandshot.ogg", "cocksound": "MOD/snd/garandcock.ogg",
            "reloadsound": "MOD/snd/garandmag.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
    "M249": {
        "tool_id": "m249", "name": "M249", "vox": "MOD/vox/M249.vox",
        "muzzle": "Vec(0.425, -0.625, -2.75)", "damage": "0.5", "rate": "0.09",
        "mag": "200", "reload": "3.2", "mags": "3", "auto": True,
        "sounds": {
            "gunsound": "MOD/snd/m249_0.ogg", "cocksound": "MOD/snd/m249_cock.ogg",
            "reloadsound": "MOD/snd/m249_reload.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
    "M4A1": {
        "tool_id": "m4a1", "name": "M4A1", "vox": "MOD/vox/m4a1.vox",
        "muzzle": "Vec(0.35, -0.6, -2.35)", "damage": "0.5", "rate": "0.075",
        "mag": "30", "reload": "1.6", "mags": "8", "auto": True,
        "sounds": {
            "gunsound": "MOD/snd/m4.ogg", "cocksound": "MOD/snd/guncock.ogg",
            "reloadsound": "MOD/snd/reload.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
    "Nova_Shotgun": {
        "tool_id": "novashotgun", "name": "Nova Shotgun", "vox": "MOD/vox/novashotgun.vox",
        "muzzle": "Vec(0.35, -0.55, -2.4)", "damage": "0.35", "rate": "0.6",
        "mag": "8", "reload": "0.5", "mags": "41", "auto": False,
        "sounds": {
            "gunsound": "MOD/snd/nova_shot.ogg", "cocksound": "MOD/snd/nova_cock.ogg",
            "reloadsound": "MOD/snd/nova_load.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
    "SCAR-20": {
        "tool_id": "scar20", "name": "SCAR-20", "vox": "MOD/vox/scar20.vox",
        "muzzle": "Vec(0.4, -0.6, -2.45)", "damage": "1.1", "rate": "0.2",
        "mag": "20", "reload": "2.4", "mags": "5", "auto": True,
        "sounds": {
            "gunsound": "MOD/snd/scar0.ogg", "cocksound": "MOD/snd/awp_cock.ogg",
            "reloadsound": "MOD/snd/awp_reload.ogg", "dryfiresound": "MOD/snd/dryfire.ogg",
            "refillsound": "MOD/snd/refill.ogg",
        },
    },
}

TEMPLATE = '''-- {name} - v2 Multiplayer Patch (ARM-style with ToolAnimator + Shoot)

#version 2

#include "script/include/player.lua"
#include "script/toolanimation.lua"

players = {{}}

local TOOL_ID = "{tool_id}"
local MUZZLE_OFFSET = {muzzle}
local MAX_DIST = 100
local MAG_SIZE = {mag}
local FIRE_RATE = {rate}
local DAMAGE = {damage}
local RELOAD_TIME = {reload}
local MAX_MAGS = {mags}

local Aiming = {{
\tpos = Vec(0, 0.15, 0.3),
\trot = QuatEuler(0, 0, 0),
}}

function createPlayerData()
\treturn {{
\t\tammo = MAG_SIZE,
\t\tmags = MAX_MAGS,
\t\treloading = false,
\t\tshootTimer = 0,
\t\treloadTimer = 0,
\t\tlightTimer = 0,
\t\tspreadTimer = 0,
\t\toptionsOpen = false,
\t\taim = false,
\t\ttoolAnimator = ToolAnimator(),
\t\trecoilPos = 0,
\t\trecoilVel = 0,
\t\trecoilRot = 0,
\t\trecoilRotVel = 0,
\t\taimPos = Vec(0, 0, 0),
\t\taimVel = Vec(0, 0, 0),
\t}}
end

---------- SERVER ----------

function server.init()
\tshared.toolSettings = shared.toolSettings or {{}}
\tshared.toolSettings["unlimitedammo"] = GetBool("savegame.mod.unlimitedammo")
\tRegisterTool(TOOL_ID, "{name}", "{vox}", 3)
\tSetToolAmmoPickupAmount(TOOL_ID, MAG_SIZE)
\tSetBool("game.tool." .. TOOL_ID .. ".enabled", true)
\tSetString("game.tool." .. TOOL_ID .. ".ammo.display", "")
end

function server.setOptionsOpen(p, open)
\tlocal data = players[p]
\tif data then data.optionsOpen = open end
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tplayers[p] = createPlayerData()
\t\tSetToolEnabled(TOOL_ID, true, p)
\t\tSetToolAmmo(TOOL_ID, 101, p)
\tend
\tfor p in PlayersRemoved() do
\t\tplayers[p] = nil
\tend
\tfor p in Players() do
\t\tserver.tickPlayer(p, dt)
\tend
end

function server.tickPlayer(p, dt)
\tif GetPlayerTool(p) ~= TOOL_ID then return end
\tif GetPlayerVehicle(p) ~= 0 then return end

\tlocal data = players[p]
\tif not data then return end
\tlocal unlimitedammo = GetBool("savegame.mod.unlimitedammo")

\tif {input_check} and data.ammo > 0 and not data.reloading and not data.optionsOpen then
\t\tif data.shootTimer <= 0 then
\t\t\tlocal b = GetToolBody(p)
\t\t\tlocal muzzlePos = (b ~= 0) and TransformToParentPoint(GetBodyTransform(b), MUZZLE_OFFSET) or GetPlayerEyeTransform(p).pos
\t\t\tlocal _, startPos, endPos, aimDir = GetPlayerAimInfo(muzzlePos, MAX_DIST, p)
\t\t\tlocal dir = VecCopy(aimDir)
\t\t\tlocal spread = math.min(data.spreadTimer, 4) / 100
\t\t\tdir[1] = dir[1] + (math.random() - 0.5) * 2 * spread
\t\t\tdir[2] = dir[2] + (math.random() - 0.5) * 2 * spread
\t\t\tdir[3] = dir[3] + (math.random() - 0.5) * 2 * spread
\t\t\tdir = VecNormalize(dir)

\t\t\tShoot(muzzlePos, dir, "bullet", DAMAGE, MAX_DIST, p, TOOL_ID)

\t\t\tif not unlimitedammo then
\t\t\t\tdata.ammo = data.ammo - 1
\t\t\tend
\t\t\tdata.shootTimer = FIRE_RATE
\t\t\tdata.spreadTimer = data.spreadTimer + 1.25
\t\tend
\tend

\tif not {input_hold} then
\t\tdata.spreadTimer = math.max(0, data.spreadTimer - dt * 10)
\tend

\tif not unlimitedammo then
\t\tif data.reloading then
\t\t\tdata.reloadTimer = data.reloadTimer - dt
\t\t\tif data.reloadTimer < 0 then
\t\t\t\tdata.ammo = MAG_SIZE
\t\t\t\tdata.reloadTimer = 0
\t\t\t\tdata.reloading = false
\t\t\tend
\t\tend
\tend

\tif data.shootTimer > 0 then
\t\tdata.shootTimer = data.shootTimer - dt
\tend
end

function server.reload(p)
\tlocal data = players[p]
\tif not data then return end
\tif data.ammo < MAG_SIZE and data.mags > 0 and not data.reloading then
\t\tdata.reloading = true
\t\tdata.reloadTimer = RELOAD_TIME
\t\tdata.mags = data.mags - 1
\tend
end

---------- CLIENT ----------

local gunsound, cocksound, reloadsound, dryfiresound, refillsound

function client.init()
{sound_loads}
end

function client.tick(dt)
\tfor p in PlayersAdded() do
\t\tif not players[p] then players[p] = createPlayerData() end
\tend
\tfor p in PlayersRemoved() do
\t\tplayers[p] = nil
\tend
\tfor p in Players() do
\t\tclient.tickPlayer(p, dt)
\tend
end

function client.tickPlayer(p, dt)
\tif GetPlayerTool(p) ~= TOOL_ID then return end
\tif GetPlayerVehicle(p) ~= 0 then return end

\tlocal data = players[p]
\tif not data then return end
\tlocal pt = GetPlayerTransform(p)
\tlocal isLocal = IsPlayerLocal(p)
\tlocal unlimitedammo = GetBool("savegame.mod.unlimitedammo")

\t-- Tool Config
\tif IsPlayerHost() and GetString("toolconfig.request") == TOOL_ID then
\t\tdata.optionsOpen = true
\t\tSetString("toolconfig.request", "")
\tend

\tif isLocal and IsPlayerHost() and InputPressed("o") then
\t\tdata.optionsOpen = not data.optionsOpen
\t\tServerCall("server.setOptionsOpen", p, data.optionsOpen)
\tend

\tif data.optionsOpen then return end

\t-- ADS hold
\tif isLocal then
\t\tdata.aim = InputDown("rmb")
\tend

\t-- Shoot sound + muzzle flash + recoil kick
\tif {input_check} and data.ammo > 0 and not data.reloading then
\t\tif data.shootTimer <= 0 then
\t\t\tPlaySound(gunsound, pt.pos, 1)
\t\t\tlocal b = GetToolBody(p)
\t\t\tif b ~= 0 then
\t\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\t\tlocal toolPos = TransformToParentPoint(toolTrans, MUZZLE_OFFSET)
\t\t\t\tSpawnParticle("fire", toolPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.3, 0.1)
\t\t\tend
\t\t\tdata.recoilVel = data.recoilVel + {recoil_pos}
\t\t\tdata.recoilRotVel = data.recoilRotVel + {recoil_rot}
\t\t\tif not unlimitedammo then
\t\t\t\tdata.ammo = data.ammo - 1
\t\t\tend
\t\t\tdata.shootTimer = FIRE_RATE
\t\t\tdata.lightTimer = FIRE_RATE / 2
\t\t\tdata.spreadTimer = data.spreadTimer + 1.25
\t\tend
\tend

\tif InputPressed("usetool", p) and not data.reloading then
\t\tdata.spreadTimer = 0
\t\tif data.ammo == 0 then
\t\t\tPlaySound(dryfiresound, pt.pos, 1)
\t\tend
\tend

\tif not {input_hold} then
\t\tdata.spreadTimer = math.max(0, data.spreadTimer - dt * 10)
\tend

\t-- Reload
\tif not unlimitedammo then
\t\tif isLocal and data.ammo < MAG_SIZE and data.mags > 1 and InputPressed("r") then
\t\t\tif not data.reloading then
\t\t\t\tdata.reloading = true
\t\t\t\tPlaySound(reloadsound, pt.pos, 0.6)
\t\t\t\tdata.reloadTimer = RELOAD_TIME
\t\t\t\tdata.mags = data.mags - 1
\t\t\t\tServerCall("server.reload", p)
\t\t\tend
\t\tend

\t\tif GetBool("ammobox.refill") then
\t\t\tSetBool("ammobox.refill", false)
\t\t\tdata.mags = data.mags + 1
\t\t\tPlaySound(refillsound, pt.pos, 1)
\t\tend

\t\tif data.reloading then
\t\t\tdata.reloadTimer = data.reloadTimer - dt
\t\t\tif data.reloadTimer < 0 then
\t\t\t\tdata.ammo = MAG_SIZE
\t\t\t\tdata.reloadTimer = 0
\t\t\t\tPlaySound(cocksound, pt.pos, 0.85)
\t\t\t\tdata.reloading = false
\t\t\tend
\t\tend
\tend

\t-- Spring recoil
\tlocal stiffness = 200
\tlocal damping = 15
\tdata.recoilVel = data.recoilVel - data.recoilPos * stiffness * dt
\tdata.recoilVel = data.recoilVel - data.recoilVel * damping * dt
\tdata.recoilPos = data.recoilPos + data.recoilVel * dt

\tdata.recoilRotVel = data.recoilRotVel - data.recoilRot * stiffness * dt
\tdata.recoilRotVel = data.recoilRotVel - data.recoilRotVel * damping * dt
\tdata.recoilRot = data.recoilRot + data.recoilRotVel * dt

\t-- ADS interpolation
\tlocal aimTarget = data.aim and Aiming.pos or Vec(0, 0, 0)
\tlocal aimSpeed = 10
\tdata.aimPos[1] = data.aimPos[1] + (aimTarget[1] - data.aimPos[1]) * aimSpeed * dt
\tdata.aimPos[2] = data.aimPos[2] + (aimTarget[2] - data.aimPos[2]) * aimSpeed * dt
\tdata.aimPos[3] = data.aimPos[3] + (aimTarget[3] - data.aimPos[3]) * aimSpeed * dt

\tdata.toolAnimator.offsetTransform = Transform(
\t\tVecAdd(data.aimPos, Vec(0, 0, data.recoilPos)),
\t\tQuatEuler(-data.recoilRot, 0, 0)
\t)

\ttickToolAnimator(data.toolAnimator, dt, nil, p)

\t-- Muzzle light
\tif data.lightTimer > 0 then
\t\tlocal b = GetToolBody(p)
\t\tif b ~= 0 then
\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\tlocal toolPos = TransformToParentPoint(toolTrans, MUZZLE_OFFSET)
\t\t\tPointLight(toolPos, 1, 1, 1, 0.5)
\t\tend
\t\tdata.lightTimer = data.lightTimer - dt
\tend

\tif data.shootTimer > 0 then
\t\tdata.shootTimer = data.shootTimer - dt
\tend
end

function client.draw()
\tlocal p = GetLocalPlayer()
\tif not p then return end
\tlocal data = players[p]
\tif not data then return end
\tif GetPlayerTool(p) ~= TOOL_ID or GetPlayerVehicle(p) ~= 0 then return end

\tlocal unlimitedammo = (shared.toolSettings and shared.toolSettings["unlimitedammo"] or GetBool("savegame.mod.unlimitedammo"))

\tif not data.optionsOpen then
\t\tlocal hints = {{"LMB - Fire", "RMB - Aim", "R - Reload"}}
\t\tUiPush()
\t\tUiAlign("left bottom")
\t\tUiFont("bold.ttf", 16)
\t\tUiTextOutline(0, 0, 0, 1, 0.1)
\t\tUiColor(1, 1, 1, 0.6)
\t\tUiTranslate(10, UiHeight() - 30)
\t\tfor i = #hints, 1, -1 do
\t\t\tUiText(hints[i])
\t\t\tUiTranslate(0, -20)
\t\tend
\t\tUiPop()
\tend

\tif data.optionsOpen then
\t\tUiMakeInteractive()
\t\tUiPush()
\t\tUiTranslate(UiCenter(), UiHeight() / 2 - 80)
\t\tUiAlign("center middle")
\t\tUiColor(0, 0, 0, 0.85)
\t\tUiRect(320, 220)
\t\tUiColor(1, 1, 1)
\t\tUiFont("bold.ttf", 32)
\t\tUiTranslate(0, -60)
\t\tUiText("{name} Options")
\t\tUiFont("regular.ttf", 24)
\t\tUiTranslate(0, 60)
\t\tUiText("Unlimited Ammo: " .. (unlimitedammo and "ON" or "OFF"))
\t\tUiTranslate(0, 40)
\t\tUiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
\t\tif UiTextButton(unlimitedammo and "Disable" or "Enable", 120, 30) then
\t\t\tSetBool("savegame.mod.unlimitedammo", not unlimitedammo)
\t\t\tshared.toolSettings["unlimitedammo"] = not unlimitedammo
\t\tend
\t\tUiTranslate(0, 50)
\t\tif UiTextButton("Close [O]", 100, 30) then
\t\t\tdata.optionsOpen = false
\t\t\tServerCall("server.setOptionsOpen", p, false)
\t\tend
\t\tUiPop()
\t\treturn
\tend

\tUiPush()
\tUiAlign("center")
\tUiTranslate(UiWidth() / 2, UiHeight() - 60)
\tUiFont("bold.ttf", 18)
\tUiTextOutline(0, 0, 0, 1, 0.1)
\tUiColor(1, 1, 1, 0.9)
\tif not unlimitedammo then
\t\tif data.reloading then
\t\t\tUiColor(1, 0.8, 0, 0.9)
\t\t\tUiText("RELOADING...")
\t\telse
\t\t\tUiText(data.ammo .. "/" .. MAG_SIZE * math.max(0, data.mags - 1))
\t\tend
\tend
\tUiPop()
end
'''

for mod, cfg in sorted(GUNS.items()):
    # Input check based on auto/semi
    if cfg["auto"]:
        input_check = 'InputDown("usetool", p)'
        input_hold = 'InputDown("usetool", p)'
    else:
        input_check = 'InputPressed("usetool", p)'
        input_hold = 'InputDown("usetool", p)'

    # Recoil strength based on damage/type
    dmg = float(cfg["damage"])
    if dmg >= 1.0:
        recoil_pos = "0.5"
        recoil_rot = "5"
    elif dmg >= 0.5:
        recoil_pos = "0.3"
        recoil_rot = "3"
    else:
        recoil_pos = "0.2"
        recoil_rot = "2"

    # Sound loads
    sound_lines = []
    for var, path in sorted(cfg["sounds"].items()):
        sound_lines.append(f'\t{var} = LoadSound("{path}")')
    sound_loads = "\n".join(sound_lines)

    content = TEMPLATE.format(
        name=cfg["name"],
        tool_id=cfg["tool_id"],
        vox=cfg["vox"],
        muzzle=cfg["muzzle"],
        damage=cfg["damage"],
        rate=cfg["rate"],
        mag=cfg["mag"],
        reload=cfg["reload"],
        mags=cfg["mags"],
        input_check=input_check,
        input_hold=input_hold,
        recoil_pos=recoil_pos,
        recoil_rot=recoil_rot,
        sound_loads=sound_loads,
    )

    filepath = os.path.join(MODS_DIR, mod, "main.lua")
    with open(filepath, "w") as f:
        f.write(content)
    print(f"  CONVERTED {mod}")

print(f"\nConverted {len(GUNS)} guns")
