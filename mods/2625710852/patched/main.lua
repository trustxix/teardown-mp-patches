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

function Suction(p, pd, shape)
	if pd.suckspeed > 0 then return end
	local body = GetShapeBody(shape)
	if not body then return end
	local vehicle = GetBodyVehicle(body)

	local vacuummass = pd.maxmass * pd.vacuumpower
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

	local hidevec = Vec(0, -150 - (#pd.items * 5), 0)
	local hidepos = TransformToParentVec(Transform(Vec(0, 0, 0), Quat()), hidevec)
	local bodyrot = GetBodyTransform(body).rot

	SetBodyTransform(body, Transform(hidepos, bodyrot))
	SetTag(body, "unbreakable")
	pd.items[pd.count] = {}
	pd.items[pd.count].shape = shape
	pd.items[pd.count].body = body
	pd.items[pd.count].rot = bodyrot
	pd.count = pd.count + 1
	if mass < 100 then
		pd.suckspeed = 0.1
	elseif mass < 200 then
		pd.suckspeed = 0.15
	else
		pd.suckspeed = 0.2
	end
	pd.suckspeed = pd.suckspeed / math.max(1, (pd.vacuumpower / 25))
end

function Vacuum(p, pd)
	local vacuumdist = pd.maxdist * pd.vacuumpower
	local vacuummass = pd.maxmass * pd.vacuumpower
	local mi = VecAdd(pd.tooltop, Vec(-vacuumdist / 2, -vacuumdist / 2, -vacuumdist / 2))
	local ma = VecAdd(pd.tooltop, Vec(vacuumdist / 2, vacuumdist / 2, vacuumdist / 2))
	QueryRequire("physical dynamic")
	local shapes = QueryAabbShapes(mi, ma)

	for i = 1, #shapes do
		local shape = shapes[i]
		local bmi, bma = GetShapeBounds(shape)
		local bc = VecLerp(bmi, bma, 0.5)
		local dir = VecSub(pd.tooltop, bc)
		local dist = VecLength(dir)
		dir = VecScale(dir, 1.0 / dist)

		local body = GetShapeBody(shape)
		local mass = GetBodyMass(body)

		if dist < pd.affectradius then
			if pd.deletestuff then Delete(shape) else Suction(p, pd, shape) end
		end

		if dist < vacuumdist and mass < vacuummass then
			local massScale = 1 - math.min(mass / vacuummass, 1.0)
			local distScale = 1 - math.min(dist / vacuumdist, 1.0)
			local add = VecScale(dir, pd.strength * massScale * distScale)
			local vel = GetBodyVelocity(body)
			vel = VecAdd(vel, add)
			SetBodyVelocity(body, vel)
		end
	end
end

function Blower(p, pd)
	local vacuumdist = pd.maxdist * pd.spitpower / 1.5
	local vacuummass = pd.maxmass * pd.spitpower / 1.5
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
		local dir = VecSub(bc, pd.tooltop)
		local dist = VecLength(dir)
		dir = VecScale(dir, 1.0 / dist)

		local body = GetShapeBody(shape)
		local mass = GetBodyMass(body)

		if dist < vacuumdist and mass < vacuummass then
			local massScale = 1 - math.min(mass / vacuummass, 1.0)
			local distScale = 1 - math.min(dist / vacuumdist, 1.0)
			local add = VecScale(dir, pd.strength * massScale * distScale)
			local vel = GetBodyVelocity(body)
			vel = VecAdd(vel, add)
			SetBodyVelocity(body, vel)
		end
	end
end

function Spition(p, pd)
	if pd.count < 2 or pd.spitspeed > 0 then return end

	local ct = GetPlayerEyeTransform(p)
	local startpos = TransformToParentPoint(ct, Vec(0, 0, -3))
	local fwdpos = TransformToParentPoint(ct, Vec(0, 0, -10))
	local direction = VecSub(fwdpos, startpos)
	direction[1] = direction[1] + (math.random() - 0.5)
	direction[2] = direction[2] + (math.random() - 0.5)
	direction[3] = direction[3] + (math.random() - 0.5)
	local spitvelocity = pd.velocity * pd.spitpower / 5
	direction = VecScale(direction, spitvelocity)

	local body = pd.items[pd.count - 1].body
	local shape = pd.items[pd.count - 1].shape
	local mass = GetBodyMass(body)
	local vehicle = GetBodyVehicle(body)

	if vehicle == 0 then
		local transform = Transform(Vec(), Quat())
		SetShapeLocalTransform(shape, transform)
	end

	SetBodyTransform(body, Transform(startpos, pd.items[pd.count - 1].rot))
	RemoveTag(body, "unbreakable")
	SetBodyDynamic(body, true)
	SetBodyVelocity(body, direction)
	pd.count = pd.count - 1
	if mass < 100 then
		pd.spitspeed = 0.2
	elseif mass < 200 then
		pd.spitspeed = 0.25
	else
		pd.spitspeed = 0.3
	end
	pd.spitspeed = pd.spitspeed / math.max(1, (pd.spitpower / 25))
end

----------------------------------------------------------------------
-- SERVER
----------------------------------------------------------------------

function server.init()
	RegisterTool("cresta-vacuumcleaner", "Vacuum Cleaner", "MOD/vox/vacuumcleaner.vox")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("cresta-vacuumcleaner", true, p)
		local pd = players[p]
		local vp = GetFloat("savegame.mod.vacuumpower")
		local sp = GetFloat("savegame.mod.spitpower")
		if vp > 0 then pd.vacuumpower = vp end
		if sp > 0 then pd.spitpower = sp end
	end

	for p in PlayersRemoved() do
		players[p] = nil
	end

	for p in Players() do
		local pd = players[p]
		if pd then
			server.tickPlayer(p, pd, dt)
		end
	end
end

function server.tickPlayer(p, pd, dt)
	if GetPlayerTool(p) ~= "cresta-vacuumcleaner" then
		pd.state = STATE_READY
		pd.startDelay = 0.35
		return
	end

	local lmbdown = InputDown("usetool", p)
	local lmbup = InputReleased("usetool", p)
	local rmbdown = InputDown("rmb", p)
	local rmbup = InputReleased("rmb", p)

	-- LMB start
	if lmbdown and (pd.state == STATE_READY or pd.state == STATE_SUCKEND) then
		pd.state = STATE_SUCKSTART
		pd.roll = 10
		pd.rollK = 1
	end

	-- RMB start
	if rmbdown and (pd.state == STATE_READY or pd.state == STATE_SUCKEND) then
		pd.state = STATE_SUCKSTART
		pd.roll = 10
		pd.rollK = 1
	end

	-- LMB release
	if lmbup and (pd.state == STATE_SUCK or pd.state == STATE_SPIT or pd.state == STATE_SUCKSTART) then
		pd.state = STATE_SUCKEND
		pd.roll = 10
		pd.rollK = 1
	end

	-- RMB release
	if rmbup and (pd.state == STATE_SUCK or pd.state == STATE_SPIT or pd.state == STATE_SUCKSTART) then
		pd.state = STATE_SUCKEND
		pd.roll = 10
		pd.rollK = 1
	end

	-- Startup delay countdown
	if pd.state == STATE_SUCKSTART then
		pd.startDelay = pd.startDelay - dt
		if pd.startDelay <= 0 then
			if lmbdown then
				pd.state = STATE_SUCK
			elseif rmbdown then
				pd.state = STATE_SPIT
			end
		end
	end

	-- Wind-down
	if pd.state == STATE_SUCKEND then
		pd.startDelay = pd.startDelay + dt
		if pd.startDelay > 0.35 then
			pd.state = STATE_SUCKEND
			pd.startDelay = 0.35
		end
	end

	-- Compute tooltop from tool body
	local b = GetToolBody(p)
	if b ~= 0 then
		local toolTrans = GetBodyTransform(b)
		pd.tooltop = TransformToParentPoint(toolTrans, Vec(0.355, -0.425, -2))
	end

	-- Vacuum (server authoritative: SetBodyVelocity, Delete, SetBodyTransform)
	if pd.state == STATE_SUCK then
		Vacuum(p, pd)
	end

	-- Spit (server authoritative: SetBodyVelocity, SetBodyTransform)
	if pd.state == STATE_SPIT then
		Spition(p, pd)
		Blower(p, pd)
	end

	-- Decay speed timers
	if pd.spitspeed > 0 then
		pd.spitspeed = pd.spitspeed - dt
	end
	if pd.suckspeed > 0 then
		pd.suckspeed = pd.suckspeed - dt
	end
end

----------------------------------------------------------------------
-- CLIENT
----------------------------------------------------------------------

local vacuumloop
local vacuumloopfast
local vacuumloopslow
local vacuumstart
local vacuumstartfast
local vacuumstartslow
local vacuumend
local vacuumendfast
local vacuumendslow
local vacuumsuck
local vacuumspit

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
		if not players[p] then
			players[p] = createPlayerData()
		end
		local pd = players[p]
		local vp = GetFloat("savegame.mod.vacuumpower")
		local sp = GetFloat("savegame.mod.spitpower")
		if vp > 0 then pd.vacuumpower = vp end
		if sp > 0 then pd.spitpower = sp end
	end

	for p in PlayersRemoved() do
		players[p] = nil
	end

	for p in Players() do
		local pd = players[p]
		if pd then
			client.tickPlayer(p, pd, dt)
		end
	end
end

function client.tickPlayer(p, pd, dt)
	if GetPlayerTool(p) ~= "cresta-vacuumcleaner" then
		pd.state = STATE_READY
		pd.startDelay = 0.35
		return
	end

	local pt = GetPlayerTransform(p)

	local lmbdown = InputDown("usetool", p)
	local lmbup = InputReleased("usetool", p)
	local rmbdown = InputDown("rmb", p)
	local rmbup = InputReleased("rmb", p)

	-- LMB start: play start sound
	if lmbdown and (pd.state == STATE_READY or pd.state == STATE_SUCKEND) then
		pd.state = STATE_SUCKSTART
		pd.roll = 10
		pd.rollK = 1
		if pd.vacuumpower > 67 then
			PlaySound(vacuumstartfast, pt.pos, 0.4)
		elseif pd.vacuumpower < 33 then
			PlaySound(vacuumstartslow, pt.pos, 0.4)
		else
			PlaySound(vacuumstart, pt.pos, 0.4)
		end
	end

	-- RMB start: play start sound
	if rmbdown and (pd.state == STATE_READY or pd.state == STATE_SUCKEND) then
		pd.state = STATE_SUCKSTART
		pd.roll = 10
		pd.rollK = 1
		if pd.spitpower > 67 then
			PlaySound(vacuumstartfast, pt.pos, 0.4)
		elseif pd.spitpower < 33 then
			PlaySound(vacuumstartslow, pt.pos, 0.4)
		else
			PlaySound(vacuumstart, pt.pos, 0.4)
		end
	end

	-- LMB release: play end sound
	if lmbup and (pd.state == STATE_SUCK or pd.state == STATE_SPIT or pd.state == STATE_SUCKSTART) then
		pd.state = STATE_SUCKEND
		pd.roll = 10
		pd.rollK = 1
		if pd.vacuumpower > 67 then
			PlaySound(vacuumendfast, pt.pos, 0.4)
		elseif pd.vacuumpower < 33 then
			PlaySound(vacuumendslow, pt.pos, 0.4)
		else
			PlaySound(vacuumend, pt.pos, 0.4)
		end
	end

	-- RMB release: play end sound
	if rmbup and (pd.state == STATE_SUCK or pd.state == STATE_SPIT or pd.state == STATE_SUCKSTART) then
		pd.state = STATE_SUCKEND
		pd.roll = 10
		pd.rollK = 1
		if pd.spitpower > 67 then
			PlaySound(vacuumendfast, pt.pos, 0.4)
		elseif pd.spitpower < 33 then
			PlaySound(vacuumendslow, pt.pos, 0.4)
		else
			PlaySound(vacuumend, pt.pos, 0.4)
		end
	end

	-- Startup delay countdown (mirror server logic)
	if pd.state == STATE_SUCKSTART then
		pd.startDelay = pd.startDelay - dt
		if pd.startDelay <= 0 then
			if lmbdown then
				pd.state = STATE_SUCK
			elseif rmbdown then
				pd.state = STATE_SPIT
			end
		end
	end

	-- Wind-down (mirror server logic)
	if pd.state == STATE_SUCKEND then
		pd.startDelay = pd.startDelay + dt
		if pd.startDelay > 0.35 then
			pd.state = STATE_SUCKEND
			pd.startDelay = 0.35
		end
	end

	-- Vacuum loop sounds
	if pd.state == STATE_SUCK then
		if pd.vacuumpower > 67 then
			PlayLoop(vacuumloopfast, pt.pos, 0.4)
		elseif pd.vacuumpower < 33 then
			PlayLoop(vacuumloopslow, pt.pos, 0.4)
		else
			PlayLoop(vacuumloop, pt.pos, 0.4)
		end
	end

	-- Spit loop sounds
	if pd.state == STATE_SPIT then
		if pd.spitpower > 67 then
			PlayLoop(vacuumloopfast, pt.pos, 0.4)
		elseif pd.spitpower < 33 then
			PlayLoop(vacuumloopslow, pt.pos, 0.4)
		else
			PlayLoop(vacuumloop, pt.pos, 0.4)
		end
	end

	-- Tool transform and animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local toolTrans = GetBodyTransform(b)
		pd.tooltop = TransformToParentPoint(toolTrans, Vec(0.355, -0.425, -2))

		local framerate = dt * 60
		pd.angVel = pd.angVel * math.pow(0.8, framerate) - 0.02 * pd.ang
		pd.ang = pd.ang + pd.angVel * framerate
		pd.rollK = pd.rollK + 0.01 * -pd.rollK
		pd.rollVel = pd.rollVel * math.pow(pd.rollK, framerate) - 0.2 * pd.roll
		pd.roll = pd.roll + pd.rollVel * framerate

		local offsetTransform = Transform(Vec(0, 0, 0), QuatEuler(pd.ang * 3, pd.ang * 3, pd.roll))
		SetToolTransform(offsetTransform, 1.0, p)

		if pd.spitspeed > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, -pd.spitspeed)
			t.rot = QuatEuler(pd.spitspeed * 20, 0, 0)
			SetToolTransform(t, 1.0, p)
		end

		if pd.suckspeed > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, pd.suckspeed)
			t.rot = QuatEuler(pd.suckspeed * 20, 0, 0)
			SetToolTransform(t, 1.0, p)
		end
	end

	-- Decay speed timers (client mirrors for animation)
	if pd.spitspeed > 0 then
		pd.spitspeed = pd.spitspeed - dt
	end
	if pd.suckspeed > 0 then
		pd.suckspeed = pd.suckspeed - dt
	end

	-- Options toggle (local player only)
	if p == GetLocalPlayer() then
		if InputPressed("r", p) then
			pd.optionsopen = not pd.optionsopen
		end
	end
end

----------------------------------------------------------------------
-- HUD
----------------------------------------------------------------------

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
	local pd = players[p]
	if not pd then return end

	if GetPlayerTool(p) == "cresta-vacuumcleaner" then
		UiPush()
			UiTranslate(UiCenter(), UiHeight() - 60)
			UiAlign("center middle")
			UiColor(1, 1, 1)
			UiFont("bold.ttf", 32)
			UiTextOutline(0, 0, 0, 1, 0.1)
			UiText(pd.count - 1)
		UiPop()
	end

	if GetPlayerTool(p) == "cresta-vacuumcleaner" and pd.optionsopen then
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
				if InputPressed("lmb") and not UiIsMouseInRect(225, 160) then pd.optionsopen = false end
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
					pd.vacuumpower = optionsSlider(pd.vacuumpower, 1, 100)
					SetFloat("savegame.mod.vacuumpower", pd.vacuumpower)
					UiTranslate(0, -25)
					UiText(pd.vacuumpower)
				UiPop()

				UiTranslate(0, 50)
				UiPush()
					UiText("Spit Power")
					UiTranslate(w, 0)
					UiAlign("right")
					UiTranslate(0, 25)
					pd.spitpower = optionsSlider(pd.spitpower, 1, 100)
					SetFloat("savegame.mod.spitpower", pd.spitpower)
					UiTranslate(0, -25)
					UiText(pd.spitpower)
				UiPop()
			UiPop()
		UiPop()
	end
end
