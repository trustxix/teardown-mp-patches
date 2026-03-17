#version 2
#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		swingTimer = 0,
		fuseTime = 5,
		shellNum = 1,
		shells = createShellPool(),
		optionsOpen = false,
	}
end

function createShellPool()
	local pool = {}
	for i = 1, 250 do
		pool[i] = {
			active = false,
			grenadeTimer = 0,
			boomTimer = 0,
			bounces = 0,
			grenadepos = Vec(0, 0, 0),
			predictedBulletVelocity = Vec(0, 0, 0),
			gravity = Vec(0, -160, 0),
		}
	end
	return pool
end

function deepcopy(orig)
	local orig_type = type(orig)
	local copy
	if orig_type == "table" then
		copy = {}
		for orig_key, orig_value in next, orig, nil do
			copy[deepcopy(orig_key)] = deepcopy(orig_value)
		end
		setmetatable(copy, deepcopy(getmetatable(orig)))
	else
		copy = orig
	end
	return copy
end

---------- KEYBIND SYSTEM ----------

local KEYBIND_DEFS = {
	{ id = "fuseup", label = "Increase Fuse", default = "x" },
	{ id = "fusedown", label = "Decrease Fuse", default = "z" },
}

local BINDABLE_KEYS = {
	"a","b","c","d","e","f","g","h","i","j","k","l","m","n",
	"p","q","r","s","t","u","v","w","x","y","z",
	"1","2","3","4","5","6","7","8","9","0",
	"rmb","mmb","space","shift","ctrl","alt",
	"backspace","delete","return",
	"f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12",
}

local KEY_DISPLAY = {
	rmb="RMB", mmb="MMB", lmb="LMB", space="SPACE", shift="SHIFT",
	ctrl="CTRL", alt="ALT", backspace="BKSP", delete="DEL", ["return"]="ENTER",
}

local keybinds = {}
local keybindsLoaded = false
local rebindingAction = nil

function keyDisplayName(key)
	return KEY_DISPLAY[key] or string.upper(key)
end

function loadKeybinds()
	for _, def in ipairs(KEYBIND_DEFS) do
		local skey = "savegame.mod.keys." .. def.id
		if HasKey(skey) then
			keybinds[def.id] = GetString(skey)
		else
			keybinds[def.id] = def.default
		end
	end
	keybindsLoaded = true
end

function resetKeybinds()
	for _, def in ipairs(KEYBIND_DEFS) do
		keybinds[def.id] = def.default
		SetString("savegame.mod.keys." .. def.id, def.default)
	end
end

---------- SHARED PROJECTILE PHYSICS ----------

function ShellPhysicsStep(shell, dt, bounceSoundFunc)
	shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(shell.gravity, dt / 4))
	local point2 = VecAdd(shell.grenadepos, VecScale(shell.predictedBulletVelocity, dt / 4))
	local dir = VecNormalize(VecSub(point2, shell.grenadepos))
	local distance = VecLength(VecSub(point2, shell.grenadepos))
	local hit, dist, normal = QueryRaycast(shell.grenadepos, dir, distance)
	if hit then
		if shell.bounces == 30 then
			shell.gravity = Vec(0, 0, 0)
			shell.predictedBulletVelocity = Vec(0, 0, 0)
		else
			if shell.bounces < 10 and bounceSoundFunc then
				bounceSoundFunc(shell.grenadepos)
			end
			local dot = VecDot(normal, shell.predictedBulletVelocity)
			shell.predictedBulletVelocity = VecSub(shell.predictedBulletVelocity, VecScale(normal, dot * 1.4))
			shell.bounces = shell.bounces + 1
		end
	else
		shell.grenadepos = point2
	end
end

function ShootGrenade(p, d)
	local eye = GetPlayerEyeTransform(p)
	local fwdpos = TransformToParentPoint(eye, Vec(0, 0, -2))
	local gunpos = TransformToParentPoint(eye, Vec(0, 0, -1))
	local direction = VecSub(fwdpos, gunpos)
	d.swingTimer = 0.125

	local shell = d.shells[d.shellNum]
	shell.active = true
	shell.grenadepos = deepcopy(gunpos)
	shell.predictedBulletVelocity = VecScale(direction, 100)
	shell.grenadeTimer = d.fuseTime
	shell.boomTimer = 0
	shell.bounces = 0
	shell.gravity = Vec(0, -160, 0)

	d.shellNum = (d.shellNum % #d.shells) + 1
end

---------- SERVER ----------

function server.init()
	RegisterTool("holygrenade", "Holy Grenade", "MOD/vox/holygrenade.vox", 4)
	SetBool("game.tool.holygrenade.enabled", true)
	SetString("game.tool.holygrenade.ammo.display", "")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("holygrenade", true, p)
	end
	for p in PlayersRemoved() do
		players[p] = nil
	end
	for p in Players() do
		server.tickPlayer(p, dt)
	end
end

function server.fuseUp(p)
	local d = players[p]
	if not d then return end
	d.fuseTime = math.min(20, d.fuseTime + 1)
end

function server.fuseDown(p)
	local d = players[p]
	if not d then return end
	d.fuseTime = math.max(1, d.fuseTime - 1)
end

function server.tickPlayer(p, dt)
	local d = players[p]
	if not d then return end

	if GetPlayerTool(p) == "holygrenade" and GetPlayerVehicle(p) == 0 then
		if InputPressed("usetool", p) then
			ShootGrenade(p, d)
		end
	end

	-- Process all shells (grenade physics, fuse, explosion)
	for _, shell in ipairs(d.shells) do
		if shell.grenadeTimer > 0 then
			shell.grenadeTimer = shell.grenadeTimer - dt
			if shell.grenadeTimer < 0.1 then
				shell.grenadeTimer = 0
				shell.boomTimer = 1.4
			end
		end

		if shell.boomTimer > 0 then
			shell.boomTimer = shell.boomTimer - dt
			if shell.boomTimer < 0.1 then
				shell.boomTimer = 0
				shell.active = false
				Explosion(shell.grenadepos, 10)
			end
		end

		if shell.active then
			ShellPhysicsStep(shell, dt, nil)
		end
	end
end

---------- CLIENT ----------

function client.init()
	holygrenadethrowsound = LoadSound("MOD/snd/throw.ogg")
	holygrenadebouncesound = LoadSound("MOD/snd/holybounce.ogg")
	holygrenadehallesound = LoadSound("MOD/snd/hallelujah.ogg")
	holygrenadeboomsound = LoadSound("MOD/snd/holyboom.ogg")
	holygrenadesprite = LoadSprite("MOD/img/holygren.png")
end

function client.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
	end
	for p in PlayersRemoved() do
		players[p] = nil
	end
	for p in Players() do
		client.tickPlayer(p, dt)
	end
end

function client.tickPlayer(p, dt)
	local d = players[p]
	if not d then return end

	local isLocal = (p == GetLocalPlayer())

	if isLocal and not keybindsLoaded then
		loadKeybinds()
	end

	if GetPlayerTool(p) == "holygrenade" and GetPlayerVehicle(p) == 0 then
		if InputPressed("usetool", p) then
			ShootGrenade(p, d)
			PlaySound(holygrenadethrowsound, GetPlayerEyeTransform(p).pos, 1, false)
		end

		if isLocal and not rebindingAction then
			if InputPressed("o") then
				d.optionsOpen = not d.optionsOpen
			end
			if InputPressed(keybinds["fuseup"] or "x") then
				d.fuseTime = math.min(20, d.fuseTime + 1)
				ServerCall("server.fuseUp", GetLocalPlayer())
			end
			if InputPressed(keybinds["fusedown"] or "z") then
				d.fuseTime = math.max(1, d.fuseTime - 1)
				ServerCall("server.fuseDown", GetLocalPlayer())
			end
		end

		-- Tool throw animation
		local b = GetToolBody(p)
		if b ~= 0 then
			local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
			SetToolTransform(offset, 1.0, p)

			if d.swingTimer > 0 then
				local t = Transform()
				t.pos = Vec(0, 0, d.swingTimer * 2)
				t.rot = QuatEuler(d.swingTimer * 50, 0, 0)
				SetToolTransform(t, 1.0, p)
				d.swingTimer = d.swingTimer - dt
			end
		end
	end

	-- Process all shells (mirrored physics, sounds, visuals)
	for _, shell in ipairs(d.shells) do
		if shell.grenadeTimer > 0 then
			shell.grenadeTimer = shell.grenadeTimer - dt
			if shell.grenadeTimer < 0.1 then
				shell.grenadeTimer = 0
				PlaySound(holygrenadehallesound, shell.grenadepos, 1, false)
				shell.boomTimer = 1.4
			end
		end

		if shell.boomTimer > 0 then
			shell.boomTimer = shell.boomTimer - dt
			if shell.boomTimer < 0.1 then
				shell.boomTimer = 0
				shell.active = false
				PlaySound(holygrenadeboomsound, shell.grenadepos, 1)
			end
		end

		if shell.active then
			ShellPhysicsStep(shell, dt, function(pos)
				PlaySound(holygrenadebouncesound, pos, 1, false)
			end)

			local camPos = GetPlayerEyeTransform(p).pos
			local rot = QuatLookAt(shell.grenadepos, camPos)
			local transform = Transform(shell.grenadepos, rot)
			DrawSprite(holygrenadesprite, transform, 0.4, 0.4, 0.5, 0.5, 0.5, 1, true, false)
		end
	end
end

---------- HUD ----------

function client.draw()
	local p = GetLocalPlayer()
	if not p or not players[p] then return end
	local d = players[p]
	if GetPlayerTool(p) ~= "holygrenade" or GetPlayerVehicle(p) ~= 0 then return end

	-- Keybind hints + fuse info (bottom-left)
	UiPush()
	UiTranslate(10, UiHeight() - 120)
	UiAlign("left bottom")
	UiColor(1, 1, 1, 0.8)
	UiFont("bold.ttf", 20)
	UiTextOutline(0, 0, 0, 1, 0.1)
	UiText("LMB - Throw Grenade\n" ..
		keyDisplayName(keybinds["fuseup"] or "x") .. " - Increase Fuse\n" ..
		keyDisplayName(keybinds["fusedown"] or "z") .. " - Decrease Fuse\n" ..
		"O - Options")
	UiPop()

	-- Fuse timer display (bottom-center)
	UiPush()
	UiTranslate(UiCenter(), UiHeight() - 60)
	UiAlign("center middle")
	UiFont("bold.ttf", 28)
	UiTextOutline(0, 0, 0, 1, 0.1)
	UiColor(1, 0.9, 0.3)
	UiText("Fuse: " .. d.fuseTime .. "s")
	UiPop()

	-- Options menu
	if not d.optionsOpen then return end

	UiMakeInteractive()
	UiPush()
	UiTranslate(20, UiMiddle() - 240/2)
	UiAlign("top left")
	UiColor(0, 0, 0, 0.75)
	UiImageBox("ui/common/box-solid-6.png", 650, 240, 6, 6)
	UiTranslate(300, 40)
	UiColor(1, 1, 1)
	UiFont("regular.ttf", 24)
	UiAlign("center middle")
	UiText("Holy Grenade Keybinds")

	UiTranslate(0, 10)
	UiFont("regular.ttf", 20)
	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
	UiPush()
	UiTranslate(-100, 0)
	UiColor(0.5, 0.8, 1)
	if UiTextButton("Defaults", 90, 30) then
		resetKeybinds()
		rebindingAction = nil
	end
	UiPop()
	UiPush()
	UiTranslate(100, 0)
	UiColor(1, 0.4, 0.4)
	if UiTextButton("Close", 90, 30) then
		d.optionsOpen = false
		rebindingAction = nil
	end
	UiPop()

	UiTranslate(-200, 40)
	UiFont("regular.ttf", 22)
	UiAlign("left")

	-- Rebind capture
	if rebindingAction then
		if InputPressed("esc") then
			rebindingAction = nil
		else
			for _, key in ipairs(BINDABLE_KEYS) do
				if InputPressed(key) then
					keybinds[rebindingAction] = key
					SetString("savegame.mod.keys." .. rebindingAction, key)
					rebindingAction = nil
					break
				end
			end
		end
	end

	for _, def in ipairs(KEYBIND_DEFS) do
		UiPush()
		UiColor(1, 1, 1)
		UiText(def.label)
		UiTranslate(250, 0)
		if rebindingAction == def.id then
			UiColor(1, 1, 0.3)
			UiText("[Press key...]")
			UiTranslate(130, 0)
			UiColor(1, 0.4, 0.4)
			UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
			if UiTextButton("Cancel", 70, 25) then rebindingAction = nil end
		else
			UiColor(0.2, 0.6, 1)
			UiFont("bold.ttf", 22)
			UiText("[" .. keyDisplayName(keybinds[def.id] or def.default) .. "]")
			UiFont("regular.ttf", 22)
			UiTranslate(130, 0)
			UiColor(0.5, 0.8, 1)
			UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
			if UiTextButton("Rebind", 70, 25) then rebindingAction = def.id end
		end
		UiPop()
		UiTranslate(0, 50)
	end

	UiPop()
end
