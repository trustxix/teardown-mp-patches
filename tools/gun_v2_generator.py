"""
Generates v2 multiplayer Lua rewrites for standard gun mods.
Takes a config dict and produces a complete v2 main.lua.

Applies ALL known rules from CLAUDE.md and ISSUES_AND_FIXES.md:
- #version 2 + player.lua include (Rule 1)
- Per-player state tables, Players/PlayersAdded/PlayersRemoved loops (Rule 4)
- SetToolAmmo + SetToolEnabled in PlayersAdded (Rule 6)
- RegisterTool with group number in server.init (Rule 5)
- SetString ammo.display to hide engine ammo (Rule 7)
- SetToolAmmoPickupAmount for ammo crate integration (Rule 14)
- GetPlayerAimInfo for weapon aim (Rule 11)
- QueryShot + ApplyPlayerDamage for player damage (Rule 13/30)
- No goto/labels (Lua 5.1) (Rule 16)
- No raw keys with player param — ServerCall for RMB/R (Rule 10)
- Gate usetool with not data.optionsOpen (Rule 17)
- UiMakeInteractive before options menu (Rule 20)
- server.setOptionsOpen sync + guard on both sides (Rule 24)
- client.draw() not draw() (Rule 19)
- Server handles: MakeHole, Explosion, ammo decrement (Rule 8)
- Client handles: PlaySound, SpawnParticle, PointLight (Rule 9/29)
- ClientCall(0) for projectile hit effects broadcast to all clients (Rule 37)
- Entity handles check ~= 0 not > 0 (Rule 15)
- Keybind hints always shown (KeybindHints feature)
- OptionsMenu with unlimited ammo toggle (OptionsMenu feature)
"""

GUN_TEMPLATE = '''-- {display_name} - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

players = {{}}

function createPlayerData()
\treturn {{
\t\tdamage = {damage},
\t\tvelocity = {velocity},
\t\treloadTime = {reload_time},
\t\tshotDelay = {shot_delay},
\t\tammo = {ammo},
\t\tmags = {mags},
\t\treloading = false,
\t\toptionsOpen = false,{extra_state}
\t\tshootTimer = 0,
\t\treloadTimer = 0,
\t\trecoilTimer = 0,
\t\tlightTimer = 0,{extra_timers}
\t\tspreadTimer = 0,
\t\ttoolPos = Vec(),{extra_body_state}
\t\tprojectileHandler = {{
\t\t\tshellNum = 1,
\t\t\tshells = {{}},
\t\t\tdefaultShell = {{active = false}},
\t\t}},
\t}}
end

function deepcopy(orig)
\tlocal orig_type = type(orig)
\tlocal copy
\tif orig_type == 'table' then
\t\tcopy = {{}}
\t\tfor orig_key, orig_value in next, orig, nil do
\t\t\tcopy[deepcopy(orig_key)] = deepcopy(orig_value)
\t\tend
\t\tsetmetatable(copy, deepcopy(getmetatable(orig)))
\telse
\t\tcopy = orig
\tend
\treturn copy
end

function GetAimPos(p)
\tlocal b = GetToolBody(p)
\tlocal muzzlePos = (b ~= 0) and TransformToParentPoint(GetBodyTransform(b), {muzzle_offset}) or GetPlayerEyeTransform(p).pos
\tlocal _, startPos, endPos, dir = GetPlayerAimInfo(muzzlePos, 100, p)
\tlocal distance = VecLength(VecSub(endPos, muzzlePos))
\treturn endPos, distance
end

function ProjectileOperations(projectile, data, p)
\tlocal gravity = Vec(0, {gravity_y}, 0)
\tprojectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity, VecScale(gravity, GetTimeStep()))
\tlocal point2 = VecAdd(projectile.pos, VecScale(projectile.predictedBulletVelocity, GetTimeStep()))
\tlocal dir = VecNormalize(VecSub(point2, projectile.pos))
\tlocal moveDist = VecLength(VecSub(point2, projectile.pos))

\t-- Player damage via QueryShot (server authoritative)
\tlocal qhit, qdist, qshape, qplayer, qhitFactor = QueryShot(projectile.pos, dir, moveDist, 0, p)
\tif qplayer ~= 0 then  -- Issue #47: Lua 0 is truthy, must use ~= 0
\t\tApplyPlayerDamage(qplayer, data.damage * qhitFactor, "{tool_id}", p)
\tend

\tlocal hit, dist = QueryRaycast(projectile.pos, dir, moveDist)
\tif hit then
\t\tlocal hitPos = VecAdd(projectile.pos, VecScale(dir, dist))
\t\tprojectile.active = false{proj_hit_logic}
\tend
\tprojectile.pos = point2
end

---------- SERVER ----------

function server.init()
\tRegisterTool("{tool_id}", "{display_name}", "{vox_path}", {group})
\tSetToolAmmoPickupAmount("{tool_id}", {ammo_pickup})
\tSetBool("game.tool.{tool_id}.enabled", true)
\tSetString("game.tool.{tool_id}.ammo.display", "")
end

function server.setOptionsOpen(p, open)
\tlocal data = players[p]
\tif data then data.optionsOpen = open end
end

function server.requestReload(p)
\tlocal data = players[p]
\tif not data then return end
\tif data.optionsOpen then return end
\tlocal unlimitedammo = GetBool("savegame.mod.unlimitedammo")
\tif unlimitedammo then return end
\tif data.ammo < {ammo} and data.mags > 1 and not data.reloading then
\t\tdata.reloading = true
\t\tdata.reloadTimer = data.reloadTime
\t\tdata.mags = data.mags - 1
\tend
end

function server.tick(dt)
\tfor p in PlayersAdded() do
\t\tplayers[p] = createPlayerData()
\t\tSetToolEnabled("{tool_id}", true, p)
\t\tSetToolAmmo("{tool_id}", 101, p)
\t\tlocal data = players[p]{server_init_extra}
\t\tfor i = 1, {pool_size} do
\t\t\tdata.projectileHandler.shells[i] = deepcopy(data.projectileHandler.defaultShell)
\t\tend
\tend

\tfor p in PlayersRemoved() do
\t\tplayers[p] = nil
\tend

\tfor p in Players() do
\t\tserver.tickPlayer(p, dt)
\tend
end

function server.tickPlayer(p, dt)
\tif GetPlayerTool(p) ~= "{tool_id}" then return end
\tif GetPlayerVehicle(p) ~= 0 then return end

\tlocal data = players[p]
\tif not data then return end
\tlocal unlimitedammo = GetBool("savegame.mod.unlimitedammo")

\tfor key, shell in ipairs(data.projectileHandler.shells) do
\t\tif shell.active then
\t\t\tProjectileOperations(shell, data, p)
\t\tend
\tend

{server_shoot_logic}

\tif not InputDown("usetool", p) then
\t\tdata.spreadTimer = math.max(0, data.spreadTimer - dt * 10)
\tend

{server_reload_logic}

\tif data.shootTimer > 0 then
\t\tdata.shootTimer = data.shootTimer - dt
\tend
end

---------- CLIENT ----------

function client.init()
{client_sound_loads}
end

-- Called via ClientCall(0, ...) when a projectile hits — broadcasts to ALL clients
function client.onProjectileHit(x, y, z)
\tlocal pos = Vec(x, y, z)
\tSpawnParticle("smoke", pos, Vec(0, 1, 0), 0.5, 0.3)
end

function client.tick(dt)
\tfor p in PlayersAdded() do
\t\tif not players[p] then
\t\t\tplayers[p] = createPlayerData()
\t\tend
\tend

\tfor p in PlayersRemoved() do
\t\tplayers[p] = nil
\tend

\tfor p in Players() do
\t\tclient.tickPlayer(p, dt)
\tend
end

function client.tickPlayer(p, dt)
\tif GetPlayerTool(p) ~= "{tool_id}" then return end
\tif GetPlayerVehicle(p) ~= 0 then return end

\tlocal data = players[p]
\tif not data then return end
\tlocal pt = GetPlayerTransform(p)
\tlocal unlimitedammo = GetBool("savegame.mod.unlimitedammo")
\tlocal isLocal = IsPlayerLocal(p)

{client_extra_input}

{client_shoot_effects}

\tif not InputDown("usetool", p) then
\t\tdata.spreadTimer = math.max(0, data.spreadTimer - dt * 10)
\tend

{client_reload_logic}

{client_tool_transform}

\tif data.shootTimer > 0 then
\t\tdata.shootTimer = data.shootTimer - dt
\tend
end

---------- HUD ----------

function client.draw()
\tlocal unlimitedammo = GetBool("savegame.mod.unlimitedammo")
\tlocal p = GetLocalPlayer()
\tif not p then return end
\tlocal data = players[p]
\tif not data then return end

\tif GetPlayerTool(p) ~= "{tool_id}" or GetPlayerVehicle(p) ~= 0 then return end

{client_draw_extra}

\tif not unlimitedammo then
\t\tUiPush()
\t\tUiTranslate(UiCenter(), UiHeight() - 60)
\t\tUiAlign("center middle")
\t\tUiColor(1, 1, 1)
\t\tUiFont("bold.ttf", 32)
\t\tUiTextOutline(0, 0, 0, 1, 0.1)
\t\tif data.reloading then
\t\t\tUiText("Reloading")
\t\telse
\t\t\tUiText(data.ammo .. "/" .. {ammo} * math.max(0, data.mags - 1){draw_extra_text})
\t\tend
\t\tUiPop()
\tend

{client_keybind_hints}
end
'''


def generate_standard_auto_rifle(config):
    """Generate v2 code for a standard auto-fire rifle (like AK-47, M4A1, P90, M249)"""

    c = config
    has_ironsight = c.get('has_ironsight', False)
    has_mag_anim = c.get('has_mag_anim', False)
    has_penetration = c.get('has_penetration', False)
    has_pellets = c.get('has_pellets', False)
    is_semi = c.get('is_semi', False)
    penetration = c.get('penetration', 1)
    pellets = c.get('pellets', 1)

    # Extra state fields
    extra_state = ""
    if has_ironsight:
        extra_state += "\n\t\tironsight = false,"
    if has_penetration:
        extra_state += f"\n\t\tpenetration = {penetration},"

    extra_timers = ""
    if has_mag_anim:
        extra_timers += "\n\t\tmagoutTimer = 0,\n\t\tmaginTimer = 0,"

    extra_body_state = ""
    if has_mag_anim:
        extra_body_state += "\n\t\tbody = nil,\n\t\tmag = nil,\n\t\tmagTrans = nil,"

    # Projectile hit logic (+ ClientCall to broadcast impact effects to all clients)
    if has_penetration:
        proj_hit_logic = '''
\t\tif projectile.index < projectile.penetration then
\t\t\tMakeHole(hitPos, 0.2, 0.2, 0.2)
\t\telse
\t\t\tMakeHole(hitPos, data.damage, data.damage * 0.7, data.damage * 0.4)
\t\tend
\t\tClientCall(0, "client.onProjectileHit", hitPos[1], hitPos[2], hitPos[3])'''
    else:
        proj_hit_logic = '''
\t\tMakeHole(hitPos, data.damage, data.damage * 0.85, data.damage * 0.7)
\t\tClientCall(0, "client.onProjectileHit", hitPos[1], hitPos[2], hitPos[3])'''

    # Server shoot logic
    input_fn = "InputPressed" if is_semi else "InputDown"
    muzzle = c.get('muzzle_offset', 'Vec(0.3, -0.5, -2.0)')

    if has_penetration:
        server_shoot = f'''\t-- {"Semi-auto" if is_semi else "Auto"} fire
\tif {input_fn}("usetool", p) and data.ammo > 0 and not data.reloading and not data.optionsOpen then
\t\tif data.shootTimer <= 0 then
\t\t\tlocal aimpos, distance = GetAimPos(p)
\t\t\tif distance and distance > 0 then
\t\t\t\tlocal b = GetToolBody(p)
\t\t\t\tif b ~= 0 then
\t\t\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\t\t\tdata.toolPos = TransformToParentPoint(toolTrans, {muzzle})
\t\t\t\t\tlocal ct = GetPlayerEyeTransform(p)

\t\t\t\t\tfor i = 1, data.penetration do
\t\t\t\t\t\tlocal direction
\t\t\t\t\t\tif i == 1 then
\t\t\t\t\t\t\tdirection = VecSub(aimpos, data.toolPos)
\t\t\t\t\t\telse
\t\t\t\t\t\t\tdirection = VecSub(aimpos, ct.pos)
\t\t\t\t\t\tend
\t\t\t\t\t\tlocal handler = data.projectileHandler
\t\t\t\t\t\thandler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
\t\t\t\t\t\tlocal loadedShell = handler.shells[handler.shellNum]
\t\t\t\t\t\tloadedShell.active = true
\t\t\t\t\t\tloadedShell.penetration = data.penetration
\t\t\t\t\t\tloadedShell.index = i
\t\t\t\t\t\tif i == 1 then
\t\t\t\t\t\t\tloadedShell.pos = VecCopy(data.toolPos)
\t\t\t\t\t\t\tloadedShell.predictedBulletVelocity = VecScale(direction, data.velocity * (100 / distance))
\t\t\t\t\t\telse
\t\t\t\t\t\t\tloadedShell.pos = VecCopy(ct.pos)
\t\t\t\t\t\t\tloadedShell.predictedBulletVelocity = VecScale(direction, 0.8 * (data.velocity * (100 / distance)))
\t\t\t\t\t\tend
\t\t\t\t\t\thandler.shellNum = (handler.shellNum % #handler.shells) + 1
\t\t\t\t\tend

\t\t\t\t\tif not unlimitedammo then
\t\t\t\t\t\tdata.ammo = data.ammo - 1
\t\t\t\t\tend
\t\t\t\t\tdata.shootTimer = data.shotDelay
\t\t\t\t\tdata.spreadTimer = data.spreadTimer + {c.get("spread_inc", 1.25)}
\t\t\t\tend
\t\t\tend
\t\tend
\tend'''
    elif has_pellets:
        server_shoot = f'''\t-- Shotgun fire ({pellets} pellets)
\tif {input_fn}("usetool", p) and data.ammo > 0 and not data.reloading and not data.optionsOpen then
\t\tif data.shootTimer <= 0 then
\t\t\tlocal aimpos, distance = GetAimPos(p)
\t\t\tif distance and distance > 0 then
\t\t\t\tlocal b = GetToolBody(p)
\t\t\t\tif b ~= 0 then
\t\t\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\t\t\tdata.toolPos = TransformToParentPoint(toolTrans, {muzzle})

\t\t\t\t\tfor i = 1, {pellets} do
\t\t\t\t\t\tlocal direction = VecSub(aimpos, data.toolPos)
\t\t\t\t\t\tlocal spread = {c.get("pellet_spread", 5)}
\t\t\t\t\t\tdirection[1] = direction[1] + (math.random() - 0.5) * 2 * spread
\t\t\t\t\t\tdirection[2] = direction[2] + (math.random() - 0.5) * 2 * spread
\t\t\t\t\t\tdirection[3] = direction[3] + (math.random() - 0.5) * 2 * spread

\t\t\t\t\t\tlocal handler = data.projectileHandler
\t\t\t\t\t\thandler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
\t\t\t\t\t\tlocal loadedShell = handler.shells[handler.shellNum]
\t\t\t\t\t\tloadedShell.active = true
\t\t\t\t\t\tloadedShell.pos = VecCopy(data.toolPos)
\t\t\t\t\t\tloadedShell.predictedBulletVelocity = VecScale(direction, data.velocity * (100 / distance))
\t\t\t\t\t\thandler.shellNum = (handler.shellNum % #handler.shells) + 1
\t\t\t\t\tend

\t\t\t\t\tif not unlimitedammo then
\t\t\t\t\t\tdata.ammo = data.ammo - 1
\t\t\t\t\tend
\t\t\t\t\tdata.shootTimer = data.shotDelay
\t\t\t\tend
\t\t\tend
\t\tend
\tend'''
    else:
        server_shoot = f'''\t-- {"Semi-auto" if is_semi else "Auto"} fire
\tif {input_fn}("usetool", p) and data.ammo > 0 and not data.reloading and not data.optionsOpen then
\t\tif data.shootTimer <= 0 then
\t\t\tlocal aimpos, distance = GetAimPos(p)
\t\t\tif distance and distance > 0 then
\t\t\t\tlocal b = GetToolBody(p)
\t\t\t\tif b ~= 0 then
\t\t\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\t\t\tdata.toolPos = TransformToParentPoint(toolTrans, {muzzle})

\t\t\t\t\tlocal direction = VecSub(aimpos, data.toolPos)
\t\t\t\t\tlocal spread = math.min(data.spreadTimer, {c.get("max_spread", 2)}) * distance / 100
\t\t\t\t\tdirection[1] = direction[1] + (math.random() - 0.5) * 2 * spread
\t\t\t\t\tdirection[2] = direction[2] + (math.random() - 0.5) * 2 * spread
\t\t\t\t\tdirection[3] = direction[3] + (math.random() - 0.5) * 2 * spread

\t\t\t\t\tlocal handler = data.projectileHandler
\t\t\t\t\thandler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
\t\t\t\t\tlocal loadedShell = handler.shells[handler.shellNum]
\t\t\t\t\tloadedShell.active = true
\t\t\t\t\tloadedShell.pos = VecCopy(data.toolPos)
\t\t\t\t\tloadedShell.predictedBulletVelocity = VecScale(direction, data.velocity * (100 / distance))
\t\t\t\t\thandler.shellNum = (handler.shellNum % #handler.shells) + 1

\t\t\t\t\tif not unlimitedammo then
\t\t\t\t\t\tdata.ammo = data.ammo - 1
\t\t\t\t\tend
\t\t\t\t\tdata.shootTimer = data.shotDelay
\t\t\t\t\tdata.spreadTimer = data.spreadTimer + {c.get("spread_inc", 1.25)}
\t\t\t\tend
\t\t\tend
\t\tend
\tend'''

    # Server reload
    # Server reload — reload is triggered via ServerCall from client (raw key "r" can't take player param)
    incremental_reload = c.get('incremental_reload', False)
    if incremental_reload:
        server_reload = f'''\tif data.reloading then
\t\tdata.reloadTimer = data.reloadTimer - dt
\t\tif data.reloadTimer < 0 then
\t\t\tdata.ammo = data.ammo + 1
\t\t\tdata.mags = data.mags - 1
\t\t\tdata.reloadTimer = data.reloadTime
\t\t\tif data.ammo >= {c["ammo"]} or data.mags <= 0 then
\t\t\t\tdata.reloading = false
\t\t\t\tdata.reloadTimer = 0
\t\t\tend
\t\tend
\tend'''
    else:
        server_reload = f'''\tif data.reloading then
\t\tdata.reloadTimer = data.reloadTimer - dt
\t\tif data.reloadTimer < 0 then
\t\t\tdata.ammo = {c["ammo"]}
\t\t\tdata.reloadTimer = 0
\t\t\tdata.reloading = false
\t\tend
\tend'''

    # Server init extra
    server_init_extra = ""
    if c.get('has_realistic_damage', False):
        server_init_extra = f'''
\t\tlocal realisticdamage = GetBool("savegame.mod.realisticdamage")
\t\tdata.damage = realisticdamage and {c.get("realistic_damage", 0.25)} or {c["damage"]}'''

    # Client sound loads
    sounds = c.get('sounds', {})
    client_sounds = ""
    for var, path in sounds.items():
        client_sounds += f'\t{var} = LoadSound("{path}")\n'

    # Client extra input (iron sight via RMB)
    client_extra_input = ""
    if has_ironsight:
        client_extra_input = '''\tif isLocal and InputPressed("rmb") and not data.optionsOpen then
\t\tdata.ironsight = not data.ironsight
\tend\n'''
    # Options toggle (always added)
    client_extra_input += '''\tif isLocal and InputPressed("o") then
\t\tdata.optionsOpen = not data.optionsOpen
\t\tServerCall("server.setOptionsOpen", p, data.optionsOpen)
\tend
\tif data.optionsOpen then return end\n'''

    # Client shoot effects
    client_shoot = f'''\tif {input_fn}("usetool", p) and data.ammo > 0 and not data.reloading and not data.optionsOpen then
\t\tif data.shootTimer <= 0 then
\t\t\tPlaySound(gunsound, pt.pos, {c.get("gun_volume", 1)})
\t\t\tlocal b = GetToolBody(p)
\t\t\tif b ~= 0 then
\t\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\t\tlocal toolPos = TransformToParentPoint(toolTrans, {muzzle})
\t\t\t\tSpawnParticle("fire", toolPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.3, 0.1)
\t\t\tend
\t\t\t-- ammo decrement is server-authoritative (server.tickPlayer handles it)
\t\t\tdata.shootTimer = data.shotDelay
\t\t\tdata.recoilTimer = data.shotDelay
\t\t\tdata.lightTimer = data.shotDelay / 2
\t\t\tdata.spreadTimer = data.spreadTimer + {c.get("spread_inc", 1.25)}
\t\tend
\tend

\tif InputPressed("usetool", p) and not data.reloading and not data.optionsOpen then
\t\tdata.spreadTimer = 0
\t\tif data.ammo == 0 then
\t\t\tPlaySound(dryfiresound, pt.pos, 1)
\t\tend
\tend'''

    # Client reload
    # Client reload — "r" is a raw key, use isLocal check + ServerCall
    if incremental_reload:
        client_reload = f'''\tif isLocal and not unlimitedammo and InputPressed("r") and not data.optionsOpen then
\t\tif not data.reloading then
\t\t\tServerCall("server.requestReload", p)
\t\t\tdata.reloading = true
\t\t\tPlaySound(reloadsound, pt.pos, 0.6)
\t\tend
\tend

\tif data.reloading then
\t\tdata.reloadTimer = data.reloadTimer - dt
\t\tif data.reloadTimer < 0 then
\t\t\tdata.ammo = data.ammo + 1
\t\t\tdata.mags = data.mags - 1
\t\t\tPlaySound(loadsound, pt.pos, 0.6)
\t\t\tdata.reloadTimer = data.reloadTime
\t\t\tif data.ammo >= {c["ammo"]} or data.mags <= 0 then
\t\t\t\tdata.reloading = false
\t\t\t\tdata.reloadTimer = 0
\t\t\t\tPlaySound(cocksound, pt.pos, 0.85)
\t\t\tend
\t\tend
\tend'''
    else:
        ironsight_reset = ""
        if has_ironsight:
            ironsight_reset = "\n\t\tdata.ironsight = false"
        mag_anim_reset = ""
        if has_mag_anim:
            mag_anim_reset = "\n\t\tdata.magoutTimer = 0.6"
        client_reload = f'''\tif isLocal and not unlimitedammo and InputPressed("r") and not data.optionsOpen then
\t\tif not data.reloading then
\t\t\tServerCall("server.requestReload", p)
\t\t\tdata.reloading = true{ironsight_reset}
\t\t\tPlaySound(reloadsound, pt.pos, 0.6){mag_anim_reset}
\t\tend
\tend

\tif data.reloading then
\t\tdata.reloadTimer = data.reloadTimer - dt
\t\tif data.reloadTimer < 0 then
\t\t\tdata.ammo = {c["ammo"]}
\t\t\tdata.reloadTimer = 0
\t\t\tPlaySound(cocksound, pt.pos, 0.85)
\t\t\tdata.reloading = false
\t\tend
\tend'''

    # Client tool transform
    if has_ironsight and has_mag_anim:
        client_tool = f'''\tlocal b = GetToolBody(p)
\tif b ~= 0 then
\t\tlocal magoffset = Vec(0, 0, 0)
\t\tlocal magtimer = data.magoutTimer + data.maginTimer
\t\tlocal x, y, z, rot = 0, 0.2, 0, 0

\t\tif data.ironsight then
\t\t\tx = {c.get("iron_x", 0.275)}
\t\t\ty = {c.get("iron_y", 0.45)}
\t\t\tz = {c.get("iron_z", 1)}
\t\t\trot = {c.get("iron_rot", 2.5)}
\t\tend

\t\tlocal offset = Transform(Vec(-x, y, z), QuatEuler(-rot, 0, 0))
\t\tif magtimer > 0 then
\t\t\toffset.rot = QuatEuler(10, 0, -10)
\t\t\toffset.pos = VecAdd(offset.pos, Vec(0.2, 0.2, 0))
\t\t\tmagoffset = Vec(-0.6, -0.6, 0.6)
\t\tend
\t\tSetToolTransform(offset, data.ironsight and 0 or 0.5, p)

\t\tif data.recoilTimer > 0 then
\t\t\tlocal t = Transform()
\t\t\tt.pos = Vec(-x, y, data.recoilTimer + z)
\t\t\tlocal ironrot = data.ironsight and rot or -data.recoilTimer * 50 - rot
\t\t\tt.rot = QuatEuler(-ironrot, 0, 0)
\t\t\tSetToolTransform(t, data.ironsight and 0 or 0.5, p)
\t\t\tdata.recoilTimer = data.recoilTimer - dt
\t\tend

\t\tif data.lightTimer > 0 then
\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\tlocal toolPos = TransformToParentPoint(toolTrans, {muzzle})
\t\t\tPointLight(toolPos, 1, 1, 1, 0.5)
\t\t\tdata.lightTimer = data.lightTimer - dt
\t\tend

\t\tif data.magoutTimer > 0 then
\t\t\tmagoffset = Vec(-0.3 + data.magoutTimer / 2, -0.6 + data.magoutTimer, 0.9 - data.magoutTimer * 1.5)
\t\t\tdata.magoutTimer = data.magoutTimer - dt
\t\t\tif data.magoutTimer < 0 then data.maginTimer = 0.6 end
\t\tend
\t\tif data.maginTimer > 0 then
\t\t\tmagoffset = Vec(-data.maginTimer / 2, -data.maginTimer, data.maginTimer * 1.5)
\t\t\tdata.maginTimer = data.maginTimer - dt
\t\tend

\t\tif data.body ~= b then
\t\t\tdata.body = b
\t\t\tlocal shapes = GetBodyShapes(b)
\t\t\tif shapes[2] then
\t\t\t\tdata.mag = shapes[2]
\t\t\t\tdata.magTrans = GetShapeLocalTransform(data.mag)
\t\t\tend
\t\tend
\t\tif data.mag and data.magTrans then
\t\t\tlocal mt = TransformCopy(data.magTrans)
\t\t\tmt.pos = VecAdd(mt.pos, magoffset)
\t\t\tmt.rot = QuatRotateQuat(mt.rot, QuatEuler(-magtimer * 30, magtimer * 30, 0))
\t\t\tSetShapeLocalTransform(data.mag, mt)
\t\tend
\tend'''
    else:
        client_tool = f'''\tlocal b = GetToolBody(p)
\tif b ~= 0 then
\t\tlocal offset = Transform(Vec(0, 0.2, 0))
\t\tSetToolTransform(offset, 0.5, p)

\t\tif data.recoilTimer > 0 then
\t\t\tlocal t = Transform()
\t\t\tt.pos = Vec(0, 0.2, data.recoilTimer)
\t\t\tt.rot = QuatEuler(-data.recoilTimer * 50, 0, 0)
\t\t\tSetToolTransform(t, 0.5, p)
\t\t\tdata.recoilTimer = data.recoilTimer - dt
\t\tend

\t\tif data.lightTimer > 0 then
\t\t\tlocal toolTrans = GetBodyTransform(b)
\t\t\tlocal toolPos = TransformToParentPoint(toolTrans, {muzzle})
\t\t\tPointLight(toolPos, 1, 1, 1, 0.5)
\t\t\tdata.lightTimer = data.lightTimer - dt
\t\tend
\tend'''

    # Client draw extra — options menu
    client_draw_extra = f'''\tif data.optionsOpen then
\t\tUiMakeInteractive()
\t\tUiPush()
\t\t\tUiTranslate(UiCenter(), UiHeight() / 2 - 80)
\t\t\tUiAlign("center middle")
\t\t\tUiColor(0, 0, 0, 0.85)
\t\t\tUiRect(320, 180)
\t\t\tUiColor(1, 1, 1)
\t\t\tUiFont("bold.ttf", 32)
\t\t\tUiTranslate(0, -40)
\t\t\tUiText("{c['display_name']} Options")
\t\t\tUiFont("regular.ttf", 24)
\t\t\tUiTranslate(0, 60)
\t\t\tUiText("Unlimited Ammo: " .. (unlimitedammo and "ON" or "OFF"))
\t\t\tUiTranslate(0, 40)
\t\t\tUiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
\t\t\tif UiTextButton(unlimitedammo and "Disable" or "Enable", 120, 30) then
\t\t\t\tSetBool("savegame.mod.unlimitedammo", not unlimitedammo)
\t\t\tend
\t\t\tUiTranslate(0, 50)
\t\t\tif UiTextButton("Close [O]", 100, 30) then
\t\t\t\tdata.optionsOpen = false
\t\t\t\tServerCall("server.setOptionsOpen", p, false)
\t\t\tend
\t\tUiPop()
\t\treturn
\tend'''
    draw_extra_text = ""

    # Keybind hints — always show at minimum LMB/R/O
    default_hints = "LMB - Fire\\nR - Reload\\nO - Options"
    if has_ironsight:
        default_hints = "LMB - Fire\\nRMB - Iron Sight\\nR - Reload\\nO - Options"
    hints = c.get('keybind_hints', default_hints)
    client_keybind_hints = f'''\tUiPush()
\tUiTranslate(10, UiHeight() - 120)
\tUiAlign("left bottom")
\tUiColor(1, 1, 1, 0.8)
\tUiFont("bold.ttf", 20)
\tUiTextOutline(0, 0, 0, 1, 0.1)
\tUiText("{hints}")
\tUiPop()'''

    return GUN_TEMPLATE.format(
        display_name=c['display_name'],
        tool_id=c['tool_id'],
        vox_path=c['vox_path'],
        group=c.get('group', 3),
        damage=c['damage'],
        velocity=c['velocity'],
        reload_time=c['reload_time'],
        shot_delay=c['shot_delay'],
        ammo=c['ammo'],
        mags=c['mags'],
        ammo_pickup=c.get('ammo_pickup', 10),
        muzzle_offset=c.get('muzzle_offset', 'Vec(0.3, -0.5, -2.0)'),
        gravity_y=c.get('gravity_y', -1),
        pool_size=c.get('pool_size', c['ammo']),
        extra_state=extra_state,
        extra_timers=extra_timers,
        extra_body_state=extra_body_state,
        proj_hit_logic=proj_hit_logic,
        server_init_extra=server_init_extra,
        server_shoot_logic=server_shoot,
        server_reload_logic=server_reload,
        client_sound_loads=client_sounds,
        client_extra_input=client_extra_input,
        client_shoot_effects=client_shoot,
        client_reload_logic=client_reload,
        client_tool_transform=client_tool,
        client_draw_extra=client_draw_extra,
        draw_extra_text=draw_extra_text,
        client_keybind_hints=client_keybind_hints,
    )


if __name__ == "__main__":
    import os, sys

    # Define all remaining My Cresta standard guns
    GUNS = [
        {
            'workshop_id': '2401591426',
            'tool_id': '500magnum',
            'display_name': '.500 Magnum',
            'vox_path': 'MOD/vox/magnum.vox',
            'group': 3,
            'damage': 1.2,
            'velocity': 1.7,
            'reload_time': 1.5,
            'shot_delay': 0.4,
            'ammo': 5,
            'mags': 10,
            'pool_size': 15,
            'gravity_y': 0,
            'is_semi': True,
            'has_penetration': True,
            'penetration': 4,
            'muzzle_offset': 'Vec(0.35, -0.65, -2.4)',
            'sounds': {
                'gunsound': 'MOD/snd/magnum0.ogg',
                'cocksound': 'MOD/snd/magnumcock.ogg',
                'reloadsound': 'MOD/snd/magnumreload.ogg',
                'dryfiresound': 'MOD/snd/dryfire.ogg',
                'refillsound': 'MOD/snd/refill.ogg',
            },
        },
        {
            'workshop_id': '2401871202',
            'tool_id': 'novashotgun',
            'display_name': 'Nova Shotgun',
            'vox_path': 'MOD/vox/novashotgun.vox',
            'group': 3,
            'damage': 0.35,
            'velocity': 1.5,
            'reload_time': 0.5,
            'shot_delay': 0.6,
            'ammo': 8,
            'mags': 41,
            'pool_size': 50,
            'gravity_y': 0,
            'is_semi': True,
            'has_pellets': True,
            'pellets': 25,
            'pellet_spread': 5,
            'incremental_reload': True,
            'muzzle_offset': 'Vec(0.35, -0.55, -2.4)',
            'sounds': {
                'gunsound': 'MOD/snd/nova_shot.ogg',
                'cocksound': 'MOD/snd/nova_cock.ogg',
                'reloadsound': 'MOD/snd/nova_load.ogg',
                'loadsound': 'MOD/snd/nova_load.ogg',
                'dryfiresound': 'MOD/snd/dryfire.ogg',
                'refillsound': 'MOD/snd/refill.ogg',
            },
        },
        {
            'workshop_id': '2401590057',
            'tool_id': 'scar20',
            'display_name': 'SCAR-20',
            'vox_path': 'MOD/vox/scar20.vox',
            'group': 3,
            'damage': 1.1,
            'velocity': 1.7,
            'reload_time': 2.4,
            'shot_delay': 0.2,
            'ammo': 20,
            'mags': 5,
            'pool_size': 15,
            'gravity_y': 0,
            'is_semi': True,
            'has_penetration': True,
            'penetration': 4,
            'muzzle_offset': 'Vec(0.4, -0.6, -2.45)',
            'sounds': {
                'gunsound': 'MOD/snd/scar0.ogg',
                'cocksound': 'MOD/snd/awp_cock.ogg',
                'reloadsound': 'MOD/snd/awp_reload.ogg',
                'dryfiresound': 'MOD/snd/dryfire.ogg',
                'refillsound': 'MOD/snd/refill.ogg',
            },
        },
        {
            'workshop_id': '2401591104',
            'tool_id': 'sg553',
            'display_name': 'SG-553',
            'vox_path': 'MOD/vox/sg553.vox',
            'group': 3,
            'damage': 0.65,
            'velocity': 1.5,
            'reload_time': 1.6,
            'shot_delay': 0.095,
            'ammo': 30,
            'mags': 6,
            'pool_size': 30,
            'gravity_y': -1,
            'max_spread': 1,
            'spread_inc': 1.25,
            'muzzle_offset': 'Vec(0.35, -0.55, -2.4)',
            'sounds': {
                'gunsound': 'MOD/snd/sg0.ogg',
                'cocksound': 'MOD/snd/guncock.ogg',
                'reloadsound': 'MOD/snd/reload.ogg',
                'dryfiresound': 'MOD/snd/dryfire.ogg',
                'refillsound': 'MOD/snd/refill.ogg',
            },
        },
        {
            'workshop_id': '2408922595',
            'tool_id': 'cresta-m1garand',
            'display_name': 'M1 Garand',
            'vox_path': 'MOD/vox/m1garand.vox',
            'group': 3,
            'damage': 1.1,
            'velocity': 1.7,
            'reload_time': 1.5,
            'shot_delay': 0.3,
            'ammo': 8,
            'mags': 10,
            'pool_size': 8,
            'gravity_y': 0,
            'is_semi': True,
            'has_penetration': True,
            'penetration': 2,
            'has_ironsight': True,
            'has_mag_anim': True,
            'has_realistic_damage': True,
            'realistic_damage': 0.35,
            'muzzle_offset': 'Vec(0.35, -0.6, -2.6)',
            'keybind_hints': 'RMB - Iron Sight\\nR - Reload',
            'sounds': {
                'gunsound': 'MOD/snd/garandshot.ogg',
                'cocksound': 'MOD/snd/garandcock.ogg',
                'reloadsound': 'MOD/snd/garandmag.ogg',
                'dryfiresound': 'MOD/snd/dryfire.ogg',
                'refillsound': 'MOD/snd/refill.ogg',
            },
        },
    ]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for gun in GUNS:
        wid = gun['workshop_id']
        out_path = os.path.join(base_dir, 'mods', wid, 'patched', 'main.lua')

        if not os.path.exists(os.path.dirname(out_path)):
            print(f"  SKIP {gun['display_name']} — no patched dir")
            continue

        lua_code = generate_standard_auto_rifle(gun)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(lua_code)
        print(f"  Generated: {gun['display_name']} ({wid})")

    print(f"\nDone. Generated {len(GUNS)} mods.")
