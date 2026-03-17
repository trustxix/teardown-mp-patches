-- Guided Missile by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		flying = false,
		detached = false,
		primed = false,
		piercing = false,
		missileSpeed = 20,
		missile = { pos = nil, rot = nil },
		missileTip = Vec(),
		smokePos = Vec(),
		rocketBody = nil,
		rocketTrans = nil,
		body = nil,
		rocket = nil,
		optionsOpen = false,
	}
end

---------- KEYBIND SYSTEM ----------

local KEYBIND_DEFS = {
	{ id = "piercing", label = "Toggle Piercing", default = "r" },
	{ id = "detach", label = "Detach Missile", default = "rmb" },
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

---------- SERVER ----------

function server.init()
	RegisterTool("guided", "Guided Missile", "MOD/vox/stinger.vox", 4)
	SetBool("game.tool.guided.enabled", true)
	SetString("game.tool.guided.ammo.display", "")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("guided", true, p)
	end
	for p in PlayersRemoved() do
		players[p] = nil
	end
	for p in Players() do
		server.tickPlayer(p, dt)
	end
end

function server.tickPlayer(p, dt)
	local data = players[p]
	if not data then return end
	if GetPlayerTool(p) ~= "guided" or GetPlayerVehicle(p) ~= 0 then return end

	-- Get rocket shape transform from tool body
	local b = GetToolBody(p)
	if b ~= 0 then
		if data.body ~= b then
			data.body = b
			local shapes = GetBodyShapes(b)
			if #shapes >= 2 then
				data.rocket = shapes[2]
				data.rocketTrans = GetShapeLocalTransform(data.rocket)
			end
		end
	end

	-- Launch
	if InputPressed("usetool", p) then
		if not data.flying and not data.detached then
			data.flying = true
			if data.rocketTrans then
				local spawnT = TransformToParentTransform(GetBodyTransform(GetToolBody(p)), data.rocketTrans)
				local spawned = Spawn("MOD/vox/rocket.xml", spawnT)
				if spawned and #spawned > 0 then
					data.rocketBody = spawned[1]
				end
			end
			local ct = GetPlayerEyeTransform(p)
			data.missile.pos = ct.pos
			data.missile.rot = ct.rot
		elseif data.primed and (data.flying or data.detached) then
			server.explode(p, data)
		end
	end

	-- Scroll wheel detach
	if data.flying and InputValue("mousewheel", p) ~= 0 then
		data.flying = false
		data.detached = true
	end

	-- Flying (guided)
	if data.flying and data.missile.pos then
		local mx = InputValue("mousedx", p)
		local my = InputValue("mousedy", p)
		local boosting = InputDown("space", p)

		if boosting then
			data.missileSpeed = 40
			mx = mx * 0.75
			my = my * 0.75
		else
			data.missileSpeed = 20
		end

		local forwPos = TransformToParentPoint(data.missile, Vec(0, 0, -5))
		data.missile.pos = TransformToParentPoint(data.missile, Vec(0, 0, -(data.missileSpeed / 100)))
		data.missile.rot = QuatLookAt(data.missile.pos, forwPos)
		data.missile.rot = QuatRotateQuat(data.missile.rot, QuatEuler(-my / 10, -mx / 10, 0))

		data.missileTip = TransformToParentPoint(data.missile, Vec(0, 0, -1.1))
		data.smokePos = TransformToParentPoint(data.missile, Vec(0, 0, 0.9))

		if data.rocketBody then
			local spritepos = TransformToParentPoint(data.missile, Vec(0, 0, -0.75))
			local rot = QuatLookAt(data.missile.pos, data.missileTip)
			SetBodyTransform(data.rocketBody, Transform(spritepos, rot))
		end

		data.primed = true
		server.checkHit(p, data)
	end

	-- Detached (straight flight)
	if data.detached and data.missile.pos then
		data.missile.pos = TransformToParentPoint(data.missile, Vec(0, 0, -(data.missileSpeed / 100)))
		data.missileTip = TransformToParentPoint(data.missile, Vec(0, 0, -1.1))
		data.smokePos = TransformToParentPoint(data.missile, Vec(0, 0, 1))

		if data.rocketBody then
			local rot = QuatLookAt(data.missile.pos, data.missileTip)
			SetBodyTransform(data.rocketBody, Transform(data.missile.pos, rot))
		end

		data.primed = true
		server.checkHit(p, data)
	end
end

function server.checkHit(p, data)
	if not data.missile.pos or not data.rocketBody then return end
	local fwdpos = TransformToParentPoint(data.missile, Vec(0, 0, -1.1))
	local dir = VecNormalize(VecSub(fwdpos, data.missileTip))
	QueryRejectBody(data.rocketBody)
	local hit, dist = QueryRaycast(data.missileTip, dir, VecLength(VecSub(fwdpos, data.missileTip)), 0.1)
	if hit then
		if data.piercing then
			MakeHole(data.missileTip, 0.3, 0.3, 0.3)
		else
			server.explode(p, data)
		end
	end
end

function server.explode(p, data)
	if data.missile.pos then
		Explosion(data.missileTip, 2)
	end
	if data.rocketBody then
		Delete(data.rocketBody)
		data.rocketBody = nil
	end
	data.missile.pos = nil
	data.missile.rot = nil
	data.primed = false
	data.flying = false
	data.detached = false
end

function server.togglePiercing(p)
	local data = players[p]
	if not data then return end
	data.piercing = not data.piercing
	SetString("hud.notification", "Piercing rocket " .. (data.piercing and "on" or "off"), true)
end

function server.detachMissile(p)
	local data = players[p]
	if not data then return end
	if data.flying then
		data.flying = false
		data.detached = true
	end
end

---------- CLIENT ----------

function client.init()
	explosionSound = LoadSound("MOD/snd/explosion.ogg")
	flyingSound = LoadLoop("MOD/snd/rocket_loop.ogg")
	fireSound = LoadSound("tools/launcher0.ogg")
	boosterSound = LoadLoop("MOD/snd/booster.ogg")
	missileSprite = LoadSprite("MOD/img/missile.png")
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
	local data = players[p]
	if not data then return end
	if GetPlayerTool(p) ~= "guided" or GetPlayerVehicle(p) ~= 0 then return end
	local isLocal = (p == GetLocalPlayer())

	-- Get tool body reference
	local b = GetToolBody(p)
	if b ~= 0 then
		if data.body ~= b then
			data.body = b
			local shapes = GetBodyShapes(b)
			if #shapes >= 2 then
				data.rocket = shapes[2]
				data.rocketTrans = GetShapeLocalTransform(data.rocket)
			end
		end
	end

	-- Launch sound + mirror state
	if InputPressed("usetool", p) then
		if not data.flying and not data.detached then
			data.flying = true
			PlaySound(fireSound, GetPlayerTransform(p).pos, 0.8)
			local ct = GetPlayerEyeTransform(p)
			data.missile.pos = ct.pos
			data.missile.rot = ct.rot
			-- Spawn rocket body on client too
			if data.rocketTrans then
				local spawnT = TransformToParentTransform(GetBodyTransform(GetToolBody(p)), data.rocketTrans)
				local spawned = Spawn("MOD/vox/rocket.xml", spawnT)
				if spawned and #spawned > 0 then
					data.rocketBody = spawned[1]
				end
			end
		elseif data.primed and (data.flying or data.detached) then
			if data.missileTip then
				PlaySound(explosionSound, data.missileTip, 8)
			end
			if data.rocketBody then
				Delete(data.rocketBody)
				data.rocketBody = nil
			end
			data.missile.pos = nil
			data.missile.rot = nil
			data.primed = false
			data.flying = false
			data.detached = false
		end
	end

	-- Options toggle + keybind loading (local only)
	if isLocal then
		if not keybindsLoaded then loadKeybinds() end
		if InputPressed("o") then data.optionsOpen = not data.optionsOpen end
	end

	-- Detach mirror (local: keybind + ServerCall; remote: engine "rmb")
	if isLocal and not rebindingAction then
		if InputPressed(keybinds["detach"] or "rmb") then
			if data.flying then
				data.flying = false
				data.detached = true
				ServerCall("server.detachMissile", GetLocalPlayer())
			end
		end
	else
		if InputPressed("rmb", p) then
			if data.flying then
				data.flying = false
				data.detached = true
			end
		end
	end
	if data.flying and InputValue("mousewheel", p) ~= 0 then
		data.flying = false
		data.detached = true
	end

	-- Piercing mirror (local: keybind + ServerCall; remote: engine "r")
	if isLocal and not rebindingAction then
		if InputPressed(keybinds["piercing"] or "r") then
			data.piercing = not data.piercing
			ServerCall("server.togglePiercing", GetLocalPlayer())
		end
	else
		if InputPressed("r", p) then
			data.piercing = not data.piercing
		end
	end

	-- Flying: mirror missile movement + camera + effects
	if data.flying and data.missile.pos then
		local mx = InputValue("mousedx", p)
		local my = InputValue("mousedy", p)
		local boosting = InputDown("space", p)

		if boosting then
			data.missileSpeed = 40
			mx = mx * 0.75
			my = my * 0.75
		else
			data.missileSpeed = 20
		end

		local forwPos = TransformToParentPoint(data.missile, Vec(0, 0, -5))
		data.missile.pos = TransformToParentPoint(data.missile, Vec(0, 0, -(data.missileSpeed / 100)))
		data.missile.rot = QuatLookAt(data.missile.pos, forwPos)
		data.missile.rot = QuatRotateQuat(data.missile.rot, QuatEuler(-my / 10, -mx / 10, 0))

		data.missileTip = TransformToParentPoint(data.missile, Vec(0, 0, -1.1))
		data.smokePos = TransformToParentPoint(data.missile, Vec(0, 0, 0.9))

		-- Move rocket body on client
		if data.rocketBody then
			local spritepos = TransformToParentPoint(data.missile, Vec(0, 0, -0.75))
			local rot = QuatLookAt(data.missile.pos, data.missileTip)
			SetBodyTransform(data.rocketBody, Transform(spritepos, rot))
		end

		-- Guided fly camera (LOCAL PLAYER ONLY)
		if isLocal then
			local camdist = 2
			local camPos = TransformToParentPoint(data.missile, Vec(0, camdist / 3, camdist))
			local camRot = QuatCopy(data.missile.rot)
			SetCameraTransform(Transform(camPos, camRot))
		end

		-- Effects
		PlayLoop(flyingSound, data.missile.pos, 0.2)
		SpawnParticle("fire", data.smokePos, Vec(0, 0, 0), 0.75, 0.25)
		SpawnParticle("smoke", data.smokePos, Vec(0, 0, 0), 1, 2)
		if boosting then
			PlayLoop(boosterSound, data.missile.pos, 0.6)
		end

		data.primed = true
	end

	-- Detached: mirror + effects (no camera)
	if data.detached and data.missile.pos then
		data.missile.pos = TransformToParentPoint(data.missile, Vec(0, 0, -(data.missileSpeed / 100)))
		data.missileTip = TransformToParentPoint(data.missile, Vec(0, 0, -1.1))
		data.smokePos = TransformToParentPoint(data.missile, Vec(0, 0, 1))

		if data.rocketBody then
			local rot = QuatLookAt(data.missile.pos, data.missileTip)
			SetBodyTransform(data.rocketBody, Transform(data.missile.pos, rot))
		end

		PlayLoop(flyingSound, data.missile.pos, 0.2)
		SpawnParticle("fire", data.smokePos, Vec(0, 0, 0), 0.75, 0.25)
		SpawnParticle("smoke", data.smokePos, Vec(0, 0, 0), 1, 2)
		data.primed = true
	end
end

function client.draw()
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end
	if GetPlayerTool(p) ~= "guided" or GetPlayerVehicle(p) ~= 0 then return end

	-- Keybind hints (bottom-left)
	if not keybindsLoaded then loadKeybinds() end
	local detachKey = keyDisplayName(keybinds["detach"] or "rmb")
	local piercingKey = keyDisplayName(keybinds["piercing"] or "r")
	UiPush()
	UiTranslate(10, UiHeight() - 160)
	UiAlign("left bottom")
	UiColor(1, 1, 1, 0.8)
	UiFont("bold.ttf", 20)
	UiTextOutline(0, 0, 0, 1, 0.1)
	UiText("LMB - Launch / Detonate\n" .. detachKey .. " - Detach (fly straight)\nScroll - Detach\nSpace - Boost\n" .. piercingKey .. " - Toggle Piercing\nO - Options")
	UiPop()

	-- Status indicator (bottom-center)
	UiPush()
	UiTranslate(UiCenter(), UiHeight() - 60)
	UiAlign("center middle")
	UiFont("bold.ttf", 24)
	UiTextOutline(0, 0, 0, 1, 0.1)
	if data.flying then
		UiColor(0.3, 1, 0.3)
		UiText("GUIDING")
	elseif data.detached then
		UiColor(1, 0.8, 0.2)
		UiText("DETACHED")
	else
		UiColor(1, 1, 1, 0.5)
		UiText("READY")
	end
	UiPop()

	-- Piercing mode indicator
	if data.piercing then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 90)
		UiAlign("center middle")
		UiColor(1, 0.5, 0.5)
		UiFont("bold.ttf", 20)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText("PIERCING")
		UiPop()
	end

	-- Options menu
	if not data.optionsOpen then return end

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
	UiText("Guided Missile Keybinds")

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
		data.optionsOpen = false
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
