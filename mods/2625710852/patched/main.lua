-- Vacuum Cleaner by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

local STATE_READY = 1
local STATE_SUCKSTART = 2
local STATE_SUCK = 3
local STATE_SPIT = 4
local STATE_SUCKEND = 5

players = {}

function createPlayerData()
	return {
		items = {},
		count = 1,
		velocity = 0.5,
		spitspeed = 0,
		suckspeed = 0,
		vacuumpower = 50,
		spitpower = 50,
		tooltop = Vec(),
		affectradius = 1,
		deletestuff = false,
		started = false,
		optionsopen = false,
		startDelay = 0.35,
		state = STATE_READY,

		maxmass = 640,
		maxdist = 1,
		strength = 0.4,

		ang = 0,
		angVel = 0,
		roll = 0,
		rollVel = 0,
		rollK = 1,
	}
end

function GetAimPos(p)
	local ct = GetPlayerEyeTransform(p)
	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
	local direction = VecSub(forwardPos, ct.pos)
	local distance = VecLength(direction)
	direction = VecNormalize(direction)
	local hit, hitDistance, normal, shape = QueryRaycast(ct.pos, direction, distance)
	if hit then
		forwardPos = TransformToParentPoint(ct, Vec(0, 0, -hitDistance))
	end
	return hit, shape
end

function Suction(p, data, shape)
	if data.suckspeed > 0 then return end
	local ct = GetPlayerEyeTransform(p)
	local body = GetShapeBody(shape)
	local vehicle = GetBodyVehicle(body)

	if not body then return end

	local vacuummass = data.maxmass * data.vacuumpower
	local mass = GetBodyMass(body)
	if mass > vacuummass then return end
	if mass < 16 then
		Delete(shape)
		return
	end

	local joints = GetShapeJoints(shape)
	for i = 1, #joints do
		Delete(joints[i])
	end

	local hidevec = Vec(0, -150 - (#data.items * 5), 0)
	local hidepos = TransformToParentVec(Transform(Vec(0, 0, 0), Quat()), hidevec)
	local bodyrot = GetBodyTransform(body).rot

	SetBodyTransform(body, Transform(hidepos, bodyrot))
	SetTag(body, "unbreakable")
	data.items[data.count] = {}
	data.items[data.count].shape = shape
	data.items[data.count].body = body
	data.items[data.count].rot = bodyrot
	data.count = data.count + 1
	if mass < 100 then
		data.suckspeed = 0.1
	elseif mass < 200 then
		data.suckspeed = 0.15
	else
		data.suckspeed = 0.2
	end
	data.suckspeed = data.suckspeed / math.max(1, (data.vacuumpower / 25))
end

function Vacuum(p, data)
	local vacuumdist = data.maxdist * data.vacuumpower
	local vacuummass = data.maxmass * data.vacuumpower
	local mi = VecAdd(data.tooltop, Vec(-vacuumdist / 2, -vacuumdist / 2, -vacuumdist / 2))
	local ma = VecAdd(data.tooltop, Vec(vacuumdist / 2, vacuumdist / 2, vacuumdist / 2))
	QueryRequire("physical dynamic")
	local shapes = QueryAabbShapes(mi, ma)

	for i = 1, #shapes do
		local shape = shapes[i]
		local bmi, bma = GetShapeBounds(shape)
		local bc = VecLerp(bmi, bma, 0.5)
		local dir = VecSub(data.tooltop, bc)
		local dist = VecLength(dir)
		dir = VecScale(dir, 1.0 / dist)

		local body = GetShapeBody(shape)
		local mass = GetBodyMass(body)

		if dist < data.affectradius then
			if data.deletestuff then Delete(shape) else Suction(p, data, shape) end
		end

		if dist < vacuumdist and mass < vacuummass then
			local massScale = 1 - math.min(mass / vacuummass, 1.0)
			local distScale = 1 - math.min(dist / vacuumdist, 1.0)
			local add = VecScale(dir, data.strength * massScale * distScale)
			local vel = GetBodyVelocity(body)
			vel = VecAdd(vel, add)
			SetBodyVelocity(body, vel)
		end
	end
end

function Blower(p, data)
	local vacuumdist = data.maxdist * data.spitpower / 1.5
	local vacuummass = data.maxmass * data.spitpower / 1.5
	local t = GetPlayerEyeTransform(p)
	local c = TransformToParentPoint(t, Vec(0, 0, -vacuumdist / 2))
	local mi = VecAdd(c, Vec(-vacuumdist / 2, -vacuumdist / 2, -vacuumdist / 2))
	local ma = VecAdd(c, Vec(vacuumdist / 2, vacuumdist / 2, vacuumdist / 2))
	QueryRequire("physical dynamic")
	local shapes = QueryAabbShapes(mi, ma)

	for i = 1, #shapes do
		local shape = shapes[i]
		local bmi, bma = GetShapeBounds(shape)
		local bc = VecLerp(bmi, bma, 0.5)
		local dir = VecSub(bc, data.tooltop)
		local dist = VecLength(dir)
		dir = VecScale(dir, 1.0 / dist)

		local body = GetShapeBody(shape)
		local mass = GetBodyMass(body)

		if dist < vacuumdist and mass < vacuummass then
			local massScale = 1 - math.min(mass / vacuummass, 1.0)
			local distScale = 1 - math.min(dist / vacuumdist, 1.0)
			local add = VecScale(dir, data.strength * massScale * distScale)
			local vel = GetBodyVelocity(body)
			vel = VecAdd(vel, add)
			SetBodyVelocity(body, vel)
		end
	end
end

function Spition(p, data)
	if data.count < 2 or data.spitspeed > 0 then return end

	local ct = GetPlayerEyeTransform(p)
	local startpos = TransformToParentPoint(ct, Vec(0, 0, -3))
	local fwdpos = TransformToParentPoint(ct, Vec(0, 0, -10))
	local direction = VecSub(fwdpos, startpos)
	direction[1] = direction[1] + (math.random() - 0.5)
	direction[2] = direction[2] + (math.random() - 0.5)
	direction[3] = direction[3] + (math.random() - 0.5)
	local spitvelocity = data.velocity * data.spitpower / 5
	direction = VecScale(direction, spitvelocity)

	local body = data.items[data.count - 1].body
	local shape = data.items[data.count - 1].shape
	local mass = GetBodyMass(body)
	local vehicle = GetBodyVehicle(body)

	if vehicle == 0 then
		local transform = Transform(Vec(), Quat())
		SetShapeLocalTransform(shape, transform)
	end

	SetBodyTransform(body, Transform(startpos, data.items[data.count - 1].rot))
	RemoveTag(body, "unbreakable")
	SetBodyDynamic(body, true)
	SetBodyVelocity(body, direction)
	data.count = data.count - 1
	if mass < 100 then
		data.spitspeed = 0.2
	elseif mass < 200 then
		data.spitspeed = 0.25
	else
		data.spitspeed = 0.3
	end
	data.spitspeed = data.spitspeed / math.max(1, (data.spitpower / 25))
end

---------- SERVER ----------

function server.init()
	RegisterTool("cresta-vacuumcleaner", "Vacuum Cleaner", "MOD/vox/vacuumcleaner.vox")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("cresta-vacuumcleaner", true, p)
		-- Load saved settings
		local data = players[p]
		local vp = GetFloat("savegame.mod.vacuumpower")
		local sp = GetFloat("savegame.mod.spitpower")
		if vp > 0 then data.vacuumpower = vp end
		if sp > 0 then data.spitpower = sp end
	end

	for p in PlayersRemoved() do
		players[p] = nil
	end

	for p in Players() do
		server.tickPlayer(p, dt)
	end
end

function server.tickPlayer(p, dt)
	if GetPlayerTool(p) ~= "cresta-vacuumcleaner" then return end

	local data = players[p]
	if not data then return end

	local lmbdown = InputDown("usetool", p)
	local lmbup = InputReleased("usetool", p)
	local rmbdown = InputDown("rmb", p)
	local rmbup = InputReleased("rmb", p)

	-- State transitions
	if lmbdown and (data.state == STATE_READY or data.state == STATE_SUCKEND) then
		data.state = STATE_SUCKSTART
		data.roll = 10
		data.rollK = 1
	end

	if rmbdown and (data.state == STATE_READY or data.state == STATE_SUCKEND) then
		data.state = STATE_SUCKSTART
		data.roll = 10
		data.rollK = 1
	end

	if lmbup and (data.state == STATE_SUCK or data.state == STATE_SPIT or data.state == STATE_SUCKSTART) then
		data.state = STATE_SUCKEND
		data.roll = 10
		data.rollK = 1
	end

	if rmbup and (data.state == STATE_SUCK or data.state == STATE_SPIT or data.state == STATE_SUCKSTART) then
		data.state = STATE_SUCKEND
		data.roll = 10
		data.rollK = 1
	end

	if data.state == STATE_SUCKSTART then
		data.startDelay = data.startDelay - dt
		if data.startDelay <= 0 then
			if lmbdown then
				data.state = STATE_SUCK
			elseif rmbdown then
				data.state = STATE_SPIT
			end
		end
	end

	if data.state == STATE_SUCKEND then
		data.startDelay = data.startDelay + dt
		if data.startDelay > 0.35 then
			data.state = STATE_SUCKEND
			data.startDelay = 0.35
		end
	end

	-- Compute tooltop from tool body
	local b = GetToolBody(p)
	if b ~= 0 then
		local toolTrans = GetBodyTransform(b)
		data.tooltop = TransformToParentPoint(toolTrans, Vec(0.355, -0.425, -2))
	end

	-- Vacuum (server authoritative: SetBodyVelocity, Delete, SetBodyTransform)
	if data.state == STATE_SUCK then
		Vacuum(p, data)
	end

	-- Spit (server authoritative: SetBodyVelocity, SetBodyTransform)
	if data.state == STATE_SPIT then
		Spition(p, data)
		Blower(p, data)
	end

	if GetPlayerVehicle(p) ~= 0 then
		data.state = STATE_READY
		data.startDelay = 0.35
	end

	if data.spitspeed > 0 then
		data.spitspeed = data.spitspeed - dt
	end
	if data.suckspeed > 0 then
		data.suckspeed = data.suckspeed - dt
	end
end

---------- CLIENT ----------

function client.init()
	vacuumloop = LoadLoop("MOD/snd/vacuumloop.ogg")
	vacuumloopfast = LoadLoop("MOD/snd/vacuumloopf.ogg")
	vacuumloopslow = LoadLoop("MOD/snd/vacuumloops.ogg")
	vacuumstart = LoadSound("MOD/snd/vacuumstart.ogg")
	vacuumstartfast = LoadSound("MOD/snd/vacuumstartf.ogg")
	vacuumstartslow = LoadSound("MOD/snd/vacuumstarts.ogg")
	vacuumend = LoadSound("MOD/snd/vacuumend.ogg")
	vacuumendfast = LoadSound("MOD/snd/vacuumendf.ogg")
	vacuumendslow = LoadSound("MOD/snd/vacuumends.ogg")
	vacuumsuck = LoadSound("MOD/snd/vacuumsuck.ogg")
	vacuumspit = LoadSound("MOD/snd/vacuumspit.ogg")
end

function client.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		local data = players[p]
		local vp = GetFloat("savegame.mod.vacuumpower")
		local sp = GetFloat("savegame.mod.spitpower")
		if vp > 0 then data.vacuumpower = vp end
		if sp > 0 then data.spitpower = sp end
	end

	for p in PlayersRemoved() do
		players[p] = nil
	end

	for p in Players() do
		client.tickPlayer(p, dt)
	end
end

function client.tickPlayer(p, dt)
	if GetPlayerTool(p) ~= "cresta-vacuumcleaner" then return end

	local data = players[p]
	if not data then return end
	local pt = GetPlayerTransform(p)
	local isLocal = (p == GetLocalPlayer())

	local lmbdown = InputDown("usetool", p)
	local lmbup = InputReleased("usetool", p)
	local rmbdown = InputDown("rmb", p)
	local rmbup = InputReleased("rmb", p)

	-- State machine with sounds
	if lmbdown and (data.state == STATE_READY or data.state == STATE_SUCKEND) then
		data.state = STATE_SUCKSTART
		data.roll = 10
		data.rollK = 1
		if data.vacuumpower > 67 then
			PlaySound(vacuumstartfast, pt.pos, 0.4)
		elseif data.vacuumpower < 33 then
			PlaySound(vacuumstartslow, pt.pos, 0.4)
		else
			PlaySound(vacuumstart, pt.pos, 0.4)
		end
	end

	if rmbdown and (data.state == STATE_READY or data.state == STATE_SUCKEND) then
		data.state = STATE_SUCKSTART
		data.roll = 10
		data.rollK = 1
		if data.spitpower > 67 then
			PlaySound(vacuumstartfast, pt.pos, 0.4)
		elseif data.spitpower < 33 then
			PlaySound(vacuumstartslow, pt.pos, 0.4)
		else
			PlaySound(vacuumstart, pt.pos, 0.4)
		end
	end

	if lmbup and (data.state == STATE_SUCK or data.state == STATE_SPIT or data.state == STATE_SUCKSTART) then
		data.state = STATE_SUCKEND
		data.roll = 10
		data.rollK = 1
		if data.vacuumpower > 67 then
			PlaySound(vacuumendfast, pt.pos, 0.4)
		elseif data.vacuumpower < 33 then
			PlaySound(vacuumendslow, pt.pos, 0.4)
		else
			PlaySound(vacuumend, pt.pos, 0.4)
		end
	end

	if rmbup and (data.state == STATE_SUCK or data.state == STATE_SPIT or data.state == STATE_SUCKSTART) then
		data.state = STATE_SUCKEND
		data.roll = 10
		data.rollK = 1
		if data.spitpower > 67 then
			PlaySound(vacuumendfast, pt.pos, 0.4)
		elseif data.spitpower < 33 then
			PlaySound(vacuumendslow, pt.pos, 0.4)
		else
			PlaySound(vacuumend, pt.pos, 0.4)
		end
	end

	if data.state == STATE_SUCKSTART then
		data.startDelay = data.startDelay - dt
		if data.startDelay <= 0 then
			if lmbdown then
				data.state = STATE_SUCK
			elseif rmbdown then
				data.state = STATE_SPIT
			end
		end
	end

	if data.state == STATE_SUCKEND then
		data.startDelay = data.startDelay + dt
		if data.startDelay > 0.35 then
			data.state = STATE_SUCKEND
			data.startDelay = 0.35
		end
	end

	-- Vacuum/spit loop sounds
	if data.state == STATE_SUCK then
		if data.vacuumpower > 67 then
			PlayLoop(vacuumloopfast, pt.pos, 0.4)
		elseif data.vacuumpower < 33 then
			PlayLoop(vacuumloopslow, pt.pos, 0.4)
		else
			PlayLoop(vacuumloop, pt.pos, 0.4)
		end
		-- Suck sound on pickup
		if data.suckspeed > 0 then
			PlaySound(vacuumsuck, pt.pos, 0.4)
		end
	end

	if data.state == STATE_SPIT then
		if data.spitpower > 67 then
			PlayLoop(vacuumloopfast, pt.pos, 0.4)
		elseif data.spitpower < 33 then
			PlayLoop(vacuumloopslow, pt.pos, 0.4)
		else
			PlayLoop(vacuumloop, pt.pos, 0.4)
		end
		-- Spit sound on launch
		if data.spitspeed > 0 then
			PlaySound(vacuumspit, pt.pos, 0.4)
		end
	end

	-- Tool transform and animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local toolTrans = GetBodyTransform(b)
		data.tooltop = TransformToParentPoint(toolTrans, Vec(0.355, -0.425, -2))

		local framerate = dt * 60
		data.angVel = data.angVel * math.pow(0.8, framerate) - 0.02 * data.ang
		data.ang = data.ang + data.angVel * framerate
		data.rollK = data.rollK + 0.01 * -data.rollK
		data.rollVel = data.rollVel * math.pow(data.rollK, framerate) - 0.2 * data.roll
		data.roll = data.roll + data.rollVel * framerate

		local offsetTransform = Transform(Vec(0, 0, 0), QuatEuler(data.ang * 3, data.ang * 3, data.roll))
		SetToolTransform(offsetTransform, 1.0, p)

		if data.spitspeed > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, -data.spitspeed)
			t.rot = QuatEuler(data.spitspeed * 20, 0, 0)
			SetToolTransform(t, 1.0, p)
		end

		if data.suckspeed > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, data.suckspeed)
			t.rot = QuatEuler(data.suckspeed * 20, 0, 0)
			SetToolTransform(t, 1.0, p)
		end
	end

	if data.spitspeed > 0 then
		data.spitspeed = data.spitspeed - dt
	end
	if data.suckspeed > 0 then
		data.suckspeed = data.suckspeed - dt
	end

	if GetPlayerVehicle(p) ~= 0 then
		data.state = STATE_READY
		data.startDelay = 0.35
	end

	-- Options toggle (local player only)
	if isLocal then
		if InputPressed("r", p) then
			data.optionsopen = not data.optionsopen
		end
	end
end

---------- HUD ----------

function round(number, decimals)
	local power = 10 ^ decimals
	return math.floor(number * power) / power
end

function optionsSlider(val, min, max)
	UiColor(0.2, 0.6, 1)
	UiPush()
	UiTranslate(0, -8)
	val = (val - min) / (max - min)
	local w = 195
	UiRect(w, 3)
	UiAlign("center middle")
	UiTranslate(-195, 1)
	val = UiSlider("ui/common/dot.png", "x", val * w, 0, w) / w
	val = round((val * (max - min) + min), 2)
	UiPop()
	return val
end

function draw()
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end

	if GetPlayerTool(p) == "cresta-vacuumcleaner" and GetPlayerVehicle(p) == 0 then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 60)
		UiAlign("center middle")
		UiColor(1, 1, 1)
		UiFont("bold.ttf", 32)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText(data.count - 1)
		UiPop()
	end

	if GetPlayerTool(p) == "cresta-vacuumcleaner" and data.optionsopen then
		UiMakeInteractive()
		UiPush()
		UiTranslate(UiCenter(), UiMiddle())
		UiAlign("center middle")
		UiColor(0, 0, 0, 0.8)
		UiImageBox("common/box-solid-10.png", 225, 160, 5, 5)
		UiWindow(200, 160)

		UiTranslate(-10, 0)
		UiPush()
		UiAlign("top left")
		if InputPressed("lmb") and not UiIsMouseInRect(225, 160) then data.optionsopen = false end
		UiTranslate(10, 10)
		UiColor(1, 1, 1)
		UiFont("bold.ttf", 24)
		UiText("Vacuum Cleaner")

		local w = 195
		UiTranslate(3, 28)
		UiRect(w - 1, 2)
		UiFont("bold.ttf", 20)
		UiAlign("left")
		UiTranslate(0, 32)

		UiPush()
		UiText("Vacuum Power")
		UiTranslate(w, 0)
		UiAlign("right")
		UiTranslate(0, 25)
		data.vacuumpower = optionsSlider(data.vacuumpower, 1, 100)
		SetFloat("savegame.mod.vacuumpower", data.vacuumpower)
		UiTranslate(0, -25)
		UiText(data.vacuumpower)
		UiPop()

		UiTranslate(0, 50)
		UiPush()
		UiText("Spit Power")
		UiTranslate(w, 0)
		UiAlign("right")
		UiTranslate(0, 25)
		data.spitpower = optionsSlider(data.spitpower, 1, 100)
		SetFloat("savegame.mod.spitpower", data.spitpower)
		UiTranslate(0, -25)
		UiText(data.spitpower)
		UiPop()

		UiPop()
		UiPop()
	end
end
