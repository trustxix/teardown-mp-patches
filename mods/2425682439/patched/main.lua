#version 2
#include "script/include/player.lua"

players = {}

local GRAVITY = Vec(0, 0, 0)
local VELOCITY = 50
local MAX_BEES = 50
local HEAT_PER_SHOT = 12
local HEAT_DECAY = 25
local OVERHEAT_MAX = 100
local COOLDOWN_THRESHOLD = 30
local BEE_LIFETIME = 10

function createPlayerData()
	return {
		shells = {},
		shellNum = 1,
		activeBees = 0,
		recoilTimer = 0,
		lightTimer = 0,
		holeMode = false,
		heat = 0,
		overheated = false,
		angle = 0,
		angVel = 0,
		toolPos = Vec(0, 0, 0),
		toolTrans = Transform(),
		body = nil,
		hive = nil,
		hiveTransform = nil,
		beeShapes = {},
		beeTransforms = {},
		optionsOpen = false,
	}
end

function initShells(pd)
	for i = 1, MAX_BEES do
		pd.shells[i] = {
			active = false,
			smokeTime = 2,
			freeTimer = 0,
			bounces = 0,
			explosive = false,
			pos = Vec(0, 0, 0),
			predictedBulletVelocity = Vec(0, 0, 0),
			gravity = Vec(0, 0, 0),
		}
	end
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

----------------------------------------------------------------------
-- KEYBIND SYSTEM
----------------------------------------------------------------------

local KEYBIND_DEFS = {
	{ id = "hungry", label = "Hungry Mode", default = "r" },
	{ id = "kamikaze", label = "Kamikaze Bee", default = "e" },
	{ id = "killall", label = "Kill All Bees", default = "c" },
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

----------------------------------------------------------------------
-- SERVER
----------------------------------------------------------------------

function server.init()
	RegisterTool("beegun", "Bee Gun", "MOD/vox/beegun.vox", 6)
	SetBool("game.tool.beegun.enabled", true)
	SetString("game.tool.beegun.ammo.display", "")
end

function server.tick(dt)
	-- Phase 1: PlayersAdded
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		initShells(players[p])
		SetToolEnabled("beegun", true, p)
	end

	-- Phase 2: PlayersRemoved
	for p in PlayersRemoved() do
		players[p] = nil
	end

	-- Phase 3: Active players
	for p in Players() do
		local pd = players[p]
		if pd then
			server.tickPlayer(p, dt)
		end
	end
end

function server.tickPlayer(p, dt)
	local pd = players[p]
	if not pd then return end

	if GetPlayerTool(p) == "beegun" and GetPlayerVehicle(p) == 0 then
		-- Heat decay
		if pd.heat > 0 then
			pd.heat = math.max(0, pd.heat - HEAT_DECAY * dt)
		end
		if pd.overheated and pd.heat <= COOLDOWN_THRESHOLD then
			pd.overheated = false
		end

		-- LMB: shoot (blocked when overheated)
		if InputPressed("usetool", p) and not pd.overheated then
			local ct = GetPlayerEyeTransform(p)
			local fwdpos = TransformToParentPoint(ct, Vec(0.3, -0.45, -3.2))
			local gunpos = TransformToParentPoint(ct, Vec(0.3, -0.45, -2.2))
			local direction = VecSub(fwdpos, gunpos)

			pd.shells[pd.shellNum] = {
				active = true,
				smokeTime = 0.3,
				freeTimer = 0,
				bounces = 0,
				explosive = false,
				pos = VecCopy(gunpos),
				predictedBulletVelocity = VecScale(direction, VELOCITY),
				gravity = VecCopy(GRAVITY),
			}
			pd.shellNum = (pd.shellNum % MAX_BEES) + 1

			pd.heat = math.min(OVERHEAT_MAX, pd.heat + HEAT_PER_SHOT)
			if pd.heat >= OVERHEAT_MAX then
				pd.overheated = true
			end
		end

		-- R/E/C actions handled via ServerCall from client (see server.toggleHungry etc.)
	end

	-- Update projectiles (server: damage/physics)
	local bees = 0
	for _, shell in ipairs(pd.shells) do
		if shell.active then
			bees = bees + 1

			-- Physics
			shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(shell.gravity, dt / 4))
			local point2 = VecAdd(shell.pos, VecScale(shell.predictedBulletVelocity, dt / 4))
			local dir = VecNormalize(VecSub(point2, shell.pos))
			local distance = VecLength(VecSub(point2, shell.pos))
			local hit, dist, normal = QueryRaycast(shell.pos, dir, distance)

			if hit then
				local hitPos = VecAdd(shell.pos, VecScale(dir, dist))
				if shell.explosive then
					Explosion(hitPos, 0.5)
					shell.active = false
				else
					-- Always do small damage on impact
					if pd.holeMode then
						MakeHole(hitPos, 0.2, 0.2, 0.2)
					else
						MakeHole(hitPos, 0.1, 0.1, 0.1)
					end
					-- Bounce (don't reset freeTimer — bees must despawn)
					local dot = VecDot(normal, shell.predictedBulletVelocity)
					shell.predictedBulletVelocity = VecSub(shell.predictedBulletVelocity, VecScale(normal, dot * 2))
					shell.bounces = shell.bounces + 1
				end
			else
				shell.pos = point2
			end

			-- Lifetime (accumulates regardless of bouncing)
			shell.freeTimer = shell.freeTimer + dt
			if shell.freeTimer > BEE_LIFETIME then
				if shell.explosive then
					Explosion(shell.pos, 0.5)
				end
				shell.active = false
			end
		end
	end
	pd.activeBees = bees
end

-- ServerCall handlers for keybind actions
function server.toggleHungry(p)
	local pd = players[p]
	if not pd then return end
	pd.holeMode = not pd.holeMode
end

function server.kamikazeBee(p)
	local pd = players[p]
	if not pd then return end
	for _, shell in ipairs(pd.shells) do
		if shell.active and not shell.explosive then
			shell.explosive = true
			break
		end
	end
end

function server.killAllBees(p)
	local pd = players[p]
	if not pd then return end
	for _, shell in ipairs(pd.shells) do
		if shell.active then
			if shell.explosive then
				Explosion(shell.pos, 0.5)
			end
			shell.active = false
		end
	end
end

----------------------------------------------------------------------
-- CLIENT
----------------------------------------------------------------------

local beeshotsound
local bouncesound
local chompsound
local kamisound
local ripsound
local beeloop
local beegunloop

function client.init()
	beeshotsound = LoadSound("MOD/snd/beeshot.ogg")
	bouncesound = LoadSound("MOD/snd/bounce.ogg")
	chompsound = LoadSound("MOD/snd/chomp0.ogg")
	kamisound = LoadSound("MOD/snd/beekami.ogg")
	ripsound = LoadSound("MOD/snd/beerip.ogg")
	beeloop = LoadLoop("MOD/snd/beeloop.ogg")
	beegunloop = LoadLoop("MOD/snd/beegunloop.ogg")
end

function client.tick(dt)
	-- Phase 1: PlayersAdded
	for p in PlayersAdded() do
		if not players[p] then
			players[p] = createPlayerData()
			initShells(players[p])
		end
	end

	-- Phase 2: PlayersRemoved
	for p in PlayersRemoved() do
		players[p] = nil
	end

	-- Phase 3: Active players
	for p in Players() do
		local pd = players[p]
		if pd then
			client.tickPlayer(p, dt)
		end
	end
end

function client.tickPlayer(p, dt)
	local pd = players[p]
	if not pd then return end
	local isLocal = IsPlayerLocal(p)

	-- Load keybinds once
	if isLocal and not keybindsLoaded then
		loadKeybinds()
	end

	if GetPlayerTool(p) == "beegun" and GetPlayerVehicle(p) == 0 then
		-- Heat decay (mirror server)
		if pd.heat > 0 then
			pd.heat = math.max(0, pd.heat - HEAT_DECAY * dt)
		end
		if pd.overheated and pd.heat <= COOLDOWN_THRESHOLD then
			pd.overheated = false
		end

		-- LMB: shoot (client mirrors for visuals, blocked when overheated)
		if InputPressed("usetool", p) and not pd.overheated then
			local ct = GetPlayerEyeTransform(p)
			local fwdpos = TransformToParentPoint(ct, Vec(0.3, -0.45, -3.2))
			local gunpos = TransformToParentPoint(ct, Vec(0.3, -0.45, -2.2))
			local direction = VecSub(fwdpos, gunpos)

			pd.recoilTimer = 0.2
			pd.lightTimer = pd.recoilTimer / 2
			pd.angVel = math.min(500, pd.angVel + dt * 9500)

			SpawnParticle("smoke", ct.pos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.3, 0.5)
			PlaySound(beeshotsound, ct.pos, 1, false)

			pd.shells[pd.shellNum] = {
				active = true,
				smokeTime = 0.3,
				freeTimer = 0,
				bounces = 0,
				explosive = false,
				pos = VecCopy(gunpos),
				predictedBulletVelocity = VecScale(direction, VELOCITY),
				gravity = VecCopy(GRAVITY),
			}
			pd.shellNum = (pd.shellNum % MAX_BEES) + 1

			pd.heat = math.min(OVERHEAT_MAX, pd.heat + HEAT_PER_SHOT)
			if pd.heat >= OVERHEAT_MAX then
				pd.overheated = true
			end
		else
			pd.angVel = math.max(0, pd.angVel - dt * 175)
		end

		-- Keybind actions (local player only, no player param — proper v2 pattern)
		if isLocal and not rebindingAction then
			-- O: toggle options
			if InputPressed("o") then
				pd.optionsOpen = not pd.optionsOpen
			end

			-- Hungry mode toggle
			if InputPressed(keybinds["hungry"] or "r") then
				pd.holeMode = not pd.holeMode
				ServerCall("server.toggleHungry", GetLocalPlayer())
				SetString("hud.notification", "Hungry Bees " .. (pd.holeMode and "on" or "off"))
			end

			-- Kamikaze bee
			if InputPressed(keybinds["kamikaze"] or "e") then
				ServerCall("server.kamikazeBee", GetLocalPlayer())
				for _, shell in ipairs(pd.shells) do
					if shell.active and not shell.explosive then
						shell.explosive = true
						PlaySound(kamisound, shell.pos, 1, false)
						SetString("hud.notification", "Kamikaze Bee!")
						break
					end
				end
			end

			-- Kill all bees
			if InputPressed(keybinds["killall"] or "c") then
				ServerCall("server.killAllBees", GetLocalPlayer())
				for _, shell in ipairs(pd.shells) do
					if shell.active then
						shell.active = false
						PlaySound(ripsound, shell.pos, 1, false)
					end
				end
				SetString("hud.notification", "All bees dead!")
			end
		end

		-- Animate tool
		clientAnimateTool(p, dt)
	end

	-- Update projectiles (client: visuals)
	local bees = 0
	for _, shell in ipairs(pd.shells) do
		if shell.active then
			bees = bees + 1

			shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(shell.gravity, dt / 4))
			local point2 = VecAdd(shell.pos, VecScale(shell.predictedBulletVelocity, dt / 4))
			local dir = VecNormalize(VecSub(point2, shell.pos))
			local distance = VecLength(VecSub(point2, shell.pos))
			local hit, dist, normal = QueryRaycast(shell.pos, dir, distance)

			if hit then
				if shell.explosive then
					shell.active = false
				else
					if pd.holeMode then
						PlaySound(chompsound, shell.pos, 1, false)
					else
						PlaySound(bouncesound, shell.pos, 1, false)
					end
					-- Bounce (don't reset freeTimer — bees must despawn)
					local dot = VecDot(normal, shell.predictedBulletVelocity)
					shell.predictedBulletVelocity = VecSub(shell.predictedBulletVelocity, VecScale(normal, dot * 2))
					shell.bounces = shell.bounces + 1
				end
			else
				DrawLine(shell.pos, point2, 1, 1, 0.2)
				PlayLoop(beeloop, shell.pos, 0.6)
				-- Throttled smoke: only spawn every 0.3s per bee
				shell.smokeTime = shell.smokeTime - dt
				if shell.smokeTime <= 0 then
					SpawnParticle("smoke", shell.pos, Vec(0, 0.15, 0), 0.1, 0.3)
					shell.smokeTime = 0.3
				end
				shell.pos = point2
			end

			-- Lifetime (accumulates regardless of bouncing)
			shell.freeTimer = shell.freeTimer + dt
			if shell.freeTimer > BEE_LIFETIME then
				shell.active = false
			end
		end
	end
	pd.activeBees = bees
end

function clientAnimateTool(p, dt)
	local pd = players[p]
	if not pd then return end

	local b = GetToolBody(p)
	if b == 0 then return end

	local offset = Transform(Vec(0.1, 0.1, 0))
	SetToolTransform(offset, 1.0, p)
	pd.toolTrans = GetBodyTransform(b)
	pd.toolPos = TransformToParentPoint(pd.toolTrans, Vec(0.3, -0.45, -2.2))
	PlayLoop(beegunloop, pd.toolPos)

	-- Recoil
	if pd.recoilTimer > 0 then
		local t = Transform()
		t.pos = Vec(0.1, 0.1, pd.recoilTimer)
		t.rot = QuatEuler(pd.recoilTimer * 50, 0, 0)
		SetToolTransform(t, 1.0, p)
		pd.recoilTimer = pd.recoilTimer - dt
	end

	-- Muzzle flash light
	if pd.lightTimer > 0 then
		PointLight(pd.toolPos, 1, 1, 1, 0.5)
		pd.lightTimer = pd.lightTimer - dt
	end

	-- Rotating barrel animation
	pd.angle = pd.angle + pd.angVel * dt * 5
	local voxSize = 0.1
	local attach = Transform(Vec(2.75 * voxSize, -0.3, -1.525))

	if pd.body ~= b then
		pd.body = b
		local shapes = GetBodyShapes(b)
		if #shapes >= 6 then
			pd.hive = shapes[6]
			pd.beeShapes = {}
			pd.beeTransforms = {}
			for i = 1, 4 do
				pd.beeShapes[i] = shapes[i + 1]
				pd.beeTransforms[i] = TransformToLocalTransform(attach, GetShapeLocalTransform(pd.beeShapes[i]))
			end
			pd.hiveTransform = TransformToLocalTransform(attach, GetShapeLocalTransform(pd.hive))
		end
	end

	if pd.hive and pd.hiveTransform then
		attach.rot = QuatEuler(0, -pd.angle, 0)
		local t = TransformToParentTransform(attach, pd.hiveTransform)
		SetShapeLocalTransform(pd.hive, t)

		for i = 1, 4 do
			if pd.beeShapes[i] and pd.beeTransforms[i] then
				local bt = TransformCopy(attach)
				local beeAngle = GetTime() * (100 * (i / 2))
				bt.rot = QuatEuler(beeAngle, -beeAngle, 0)
				local beet = TransformToParentTransform(bt, pd.beeTransforms[i])
				SetShapeLocalTransform(pd.beeShapes[i], beet)
			end
		end
	end
end

----------------------------------------------------------------------
-- DRAW (HUD)
----------------------------------------------------------------------

function client.draw()
	local p = GetLocalPlayer()
	if not p then return end
	local pd = players[p]
	if not pd then return end
	if GetPlayerTool(p) ~= "beegun" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	-- Keybind hints (bottom-left, uses actual bindings)
	if not pd.optionsOpen then
		UiPush()
		UiTranslate(10, UiHeight() - 140)
		UiAlign("left bottom")
		UiColor(1, 1, 1, 0.8)
		UiFont("bold.ttf", 20)
		UiTextOutline(0, 0, 0, 1, 0.1)
		local hk = keybindsLoaded and keybinds or {}
		UiText("LMB - Shoot Bee\n" ..
			keyDisplayName(hk["hungry"] or "r") .. " - Hungry Mode\n" ..
			keyDisplayName(hk["kamikaze"] or "e") .. " - Kamikaze Bee\n" ..
			keyDisplayName(hk["killall"] or "c") .. " - Kill All Bees\n" ..
			"O - Options")
		UiPop()
	end

	-- Active bees count (bottom-center)
	UiPush()
	UiTranslate(UiCenter(), UiHeight() - 80)
	UiAlign("center middle")
	UiColor(1, 1, 1)
	UiFont("bold.ttf", 28)
	UiTextOutline(0, 0, 0, 1, 0.1)
	UiText("Bees: " .. pd.activeBees)
	UiPop()

	-- Heat bar (bottom-center, below bee count)
	local barW = 160
	local barH = 8
	local heatFrac = pd.heat / OVERHEAT_MAX
	UiPush()
	UiTranslate(UiCenter() - barW/2, UiHeight() - 50)
	UiAlign("top left")
	UiColor(0.2, 0.2, 0.2, 0.6)
	UiRect(barW, barH)
	if heatFrac > 0.7 then
		UiColor(1, 0.2, 0.1)
	elseif heatFrac > 0.4 then
		UiColor(1, 0.8, 0.1)
	else
		UiColor(0.3, 1, 0.3)
	end
	UiRect(barW * heatFrac, barH)
	UiPop()

	-- Overheat warning
	if pd.overheated then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 30)
		UiAlign("center middle")
		UiColor(1, 0.2, 0.1)
		UiFont("bold.ttf", 20)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText("OVERHEATED")
		UiPop()
	end

	-- Mode indicator
	if pd.holeMode then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 105)
		UiAlign("center middle")
		UiColor(1, 0.5, 0.2)
		UiFont("bold.ttf", 20)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText("HUNGRY MODE")
		UiPop()
	end

	--------------------------------------------------------------
	-- OPTIONS MENU with keybind remapping
	--------------------------------------------------------------
	if not pd.optionsOpen then return end

	UiMakeInteractive()
	UiPush()
	UiTranslate(20, UiMiddle() - 260/2)
	UiAlign("top left")
	UiColor(0, 0, 0, 0.75)
	UiImageBox("ui/common/box-solid-6.png", 650, 260, 6, 6)
	UiTranslate(300, 40)
	UiColor(1, 1, 1)
	UiFont("regular.ttf", 24)
	UiAlign("center middle")
	UiText("Bee Gun Keybinds")

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
		pd.optionsOpen = false
		rebindingAction = nil
	end
	UiPop()

	UiTranslate(-200, 40)
	UiFont("regular.ttf", 22)
	UiAlign("left")

	-- Rebind key capture (check all bindable keys)
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

	-- Draw each keybind row
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
			if UiTextButton("Cancel", 70, 25) then
				rebindingAction = nil
			end
		else
			UiColor(0.2, 0.6, 1)
			UiFont("bold.ttf", 22)
			UiText("[" .. keyDisplayName(keybinds[def.id] or def.default) .. "]")
			UiFont("regular.ttf", 22)
			UiTranslate(130, 0)
			UiColor(0.5, 0.8, 1)
			UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
			if UiTextButton("Rebind", 70, 25) then
				rebindingAction = def.id
			end
		end
		UiPop()
		UiTranslate(0, 45)
	end

	UiPop()
end
