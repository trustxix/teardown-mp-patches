-- Attack Drone by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

players = {}

local pSpeed = 7

function createPlayerData()
	return {
		attackdroneenabled = false,
		flycamenabled = false,
		firing = false,
		magnet = false,
		lockCam = false,
		hideSight = false,

		gravity = Vec(),
		velocity = 1,
		shotDelay = 0.08,
		shoottimer = 0,

		droneVel = Vec(),
		angle = 0.0,
		distanceToGround = 0,
		droneHeight = 10,
		averageSurroundingHeight = 0,
		droneSpeed = 15,
		hoverAngle = 0,

		maxDist = 25,
		maxMass = 5000,
		gravStrength = 0.5,

		lightTimer = 0,
		equipTimer = 0,

		drone = {
			pos = Vec(),
			rot = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0)),
			barrel = {
				pos = Vec(),
				rot = Quat(),
			},
		},
		droneTargetPos = Vec(),
		droneTargetRot = Quat(),
		aimpos = Vec(),

		body = nil,
		droneshape = nil,
		controlshape = nil,
		dronetransformation = nil,
		controltransformation = nil,

		projectileHandler = {
			shellNum = 1,
			shells = {},
			defaultShell = {active = false},
		},
	}
end

function deepcopy(orig)
	local orig_type = type(orig)
	local copy
	if orig_type == 'table' then
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

function clamp(value, mi, ma)
	if value < mi then value = mi end
	if value > ma then value = ma end
	return value
end

function aorb(a, b, d)
	return (a and d or 0) - (b and d or 0)
end

function orientation(transform, sign)
	local fwd = VecNormalize(VecSub(TransformToParentPoint(transform, Vec(0, 0, -5)), transform.pos))
	local dir = Vec(0, 1 * sign, 0)
	local orientationFactor = clamp(VecDot(dir, fwd) * 0.7 + 0.3, 0.0, 1.0)
	return orientationFactor
end

function GetAimPos(p)
	local ct = GetPlayerEyeTransform(p)
	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -150))
	local direction = VecSub(forwardPos, ct.pos)
	local distance = VecLength(direction)
	direction = VecNormalize(direction)
	local hit, hitDistance = QueryRaycast(ct.pos, direction, distance)
	if hit then
		forwardPos = TransformToParentPoint(ct, Vec(0, 0, -hitDistance))
		distance = hitDistance
	end
	return forwardPos, hit, distance
end

function GetCamLookPos(data)
	local forwardPos = TransformToParentPoint(data.drone.barrel, Vec(0, 0, -150))
	local direction = VecSub(forwardPos, data.drone.barrel.pos)
	local distance = VecLength(direction)
	direction = VecNormalize(direction)
	local hit, hitDistance = QueryRaycast(data.drone.barrel.pos, direction, distance)
	if hit then
		forwardPos = TransformToParentPoint(data.drone.barrel, Vec(0, 0, -hitDistance))
		distance = hitDistance
	end
	return forwardPos, hit, distance
end

function GetShootDistance(data)
	local direction = VecSub(data.aimpos, data.drone.barrel.pos)
	local distance = VecLength(direction)
	direction = VecNormalize(direction)
	local hit, hitDistance = QueryRaycast(data.drone.barrel.pos, direction, distance)
	if hit then
		distance = hitDistance
	end
	return distance
end

function ProjectileOperations(projectile, dt)
	local gravity = Vec()
	projectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity, VecScale(gravity, dt))
	local point2 = VecAdd(projectile.pos, VecScale(projectile.predictedBulletVelocity, dt))
	local pointsDist = VecSub(point2, projectile.pos)
	local hit, dist = QueryRaycast(projectile.pos, VecNormalize(pointsDist), VecLength(pointsDist))
	if hit then
		local hitPos = VecAdd(projectile.pos, VecScale(VecNormalize(pointsDist), dist))
		projectile.active = false
		MakeHole(hitPos, 1, 0.85, 0.7)
		SpawnParticle("smoke", hitPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.6, 1)
		return
	else
		DrawLine(projectile.pos, point2)
	end
	projectile.pos = point2
end

function Shoot(p, data)
	if data.shoottimer > 0 then return end

	local distance = GetShootDistance(data)
	local dir = VecSub(data.aimpos, data.drone.barrel.pos)

	local handler = data.projectileHandler
	handler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
	local loadedShell = handler.shells[handler.shellNum]
	loadedShell.active = true
	loadedShell.pos = VecCopy(data.drone.barrel.pos)
	loadedShell.predictedBulletVelocity = VecScale(dir, data.velocity * (100 / distance))
	handler.shellNum = (handler.shellNum % #handler.shells) + 1

	data.shoottimer = data.shotDelay
	data.lightTimer = 0.05
end

function Magnet(data)
	local mi = VecAdd(data.drone.barrel.pos, Vec(-data.maxDist / 2, -data.maxDist / 2, -data.maxDist / 2))
	local ma = VecAdd(data.drone.barrel.pos, Vec(data.maxDist / 2, data.maxDist / 2, data.maxDist / 2))
	QueryRequire("physical dynamic")
	local bodies = QueryAabbBodies(mi, ma)

	for i = 1, #bodies do
		local b = bodies[i]
		local bmi, bma = GetBodyBounds(b)
		local bc = VecLerp(bmi, bma, 0.5)
		local dir = VecSub(data.drone.barrel.pos, bc)
		local dist = VecLength(dir)
		dir = VecScale(dir, 1.0 / dist)

		local mass = GetBodyMass(b)
		if dist < data.maxDist and mass < data.maxMass then
			local massScale = 1 - math.min(mass / data.maxMass, 1.0)
			local distScale = 1 - math.min(dist / data.maxDist, 1.0)
			local add = VecScale(dir, data.gravStrength * massScale * distScale)
			local vel = GetBodyVelocity(b)
			vel = VecAdd(vel, add)
			SetBodyVelocity(b, vel)
		end
	end
end

function computeSurroundingHeight(data)
	local probe = VecCopy(data.droneTargetPos)
	probe[1] = probe[1] + math.random(-10, 10)
	probe[2] = 100
	probe[3] = probe[3] + math.random(-10, 10)
	local hit, dist = QueryRaycast(probe, Vec(0, -1, 0), 100, 2.0)
	local hitHeight = 0
	if hit then
		hitHeight = 100 - dist
	end
	data.averageSurroundingHeight = math.max(hitHeight, data.averageSurroundingHeight - GetTimeStep() * 2)
end

function droneMovement(p, data, dt)
	data.angle = data.angle + 0.6
	local targetPos = GetPlayerPos(p)

	local hoverPos = VecCopy(targetPos)
	local radius = 10
	data.hoverAngle = data.hoverAngle + dt * 0.25
	local x = math.cos(data.hoverAngle) * radius
	local z = math.sin(data.hoverAngle) * radius
	hoverPos = VecAdd(hoverPos, Vec(x, 0, z))

	local toPlayer = VecSub(hoverPos, data.droneTargetPos)
	toPlayer[2] = 0
	local l = VecLength(toPlayer)
	local minDist = 1.0
	if l > minDist then
		local speed = (l - minDist)
		if speed > pSpeed then
			speed = pSpeed
		end
		toPlayer = VecNormalize(toPlayer)
		data.droneTargetPos = VecAdd(data.droneTargetPos, VecScale(toPlayer, speed * dt))
	end

	if not data.flycamenabled then
		if not data.magnet then
			computeSurroundingHeight(data)
			local currentHeight = data.droneHeight
			local probe = VecCopy(data.droneTargetPos)
			probe[2] = 100
			local hit, dist = QueryRaycast(probe, Vec(0, -1, 0), 100, 2.0)
			if hit then
				currentHeight = currentHeight + (100 - dist)
			end
			currentHeight = math.max(currentHeight, data.averageSurroundingHeight)
			data.droneTargetPos[2] = currentHeight + math.sin(GetTime() * 0.7) * 5
		else
			data.droneTargetPos[2] = data.droneHeight
		end
	end

	local toTarget = VecNormalize(VecSub(targetPos, data.droneTargetPos))
	toTarget[2] = clamp(toTarget[2], -0.1, 0.1)
	local lookPoint = VecAdd(data.droneTargetPos, toTarget)
	lookPoint[2] = data.droneTargetPos[2]
	local rot = QuatLookAt(data.droneTargetPos, lookPoint)
	rot = QuatRotateQuat(rot, QuatEuler(math.sin(data.angle * 0.053) * 10, math.sin(data.angle * 0.04) * 10, 0))
	rot = QuatRotateQuat(rot, QuatEuler(-90, -90, 0))
	data.droneTargetRot = rot
end

function FlyCam(p, data)
	local mx, my = InputValue("mousedx"), -InputValue("mousedy")
	local w = InputDown("w", p)
	local a = InputDown("a", p)
	local s = InputDown("s", p)
	local d = InputDown("d", p)
	local ctrl = InputDown("ctrl", p)
	local space = InputDown("jump", p)
	data.droneSpeed = InputDown("shift", p) and 50 or 25

	local upAngle = orientation(Transform(data.drone.barrel.pos, data.drone.barrel.rot), 1)
	local downAngle = orientation(Transform(data.drone.barrel.pos, data.drone.barrel.rot), -1)
	if (upAngle > 0.98 and my > 0) or (downAngle > 0.98 and my < 0) then
		my = 0
	end

	local forwPos = TransformToParentPoint(data.drone.barrel, Vec(0, 0, -5))
	if data.lockCam then
		data.drone.barrel.rot = QuatLookAt(data.drone.barrel.pos, data.aimpos)
	else
		data.drone.barrel.rot = QuatLookAt(data.drone.barrel.pos, forwPos)
	end

	local rotdiv = 20
	data.drone.barrel.rot = QuatRotateQuat(data.drone.barrel.rot, QuatEuler(my / rotdiv, -mx / rotdiv, 0))
	local newT = Transform(data.drone.barrel.pos, data.drone.barrel.rot)
	SetCameraTransform(newT)
	SetPlayerTransform(GetPlayerTransform(p), p)

	if a or d or w or s or ctrl or space then
		data.droneTargetPos = TransformToParentPoint(newT, Vec(aorb(a, d, -data.droneSpeed), aorb(ctrl, space, -data.droneSpeed), aorb(w, s, -data.droneSpeed)))
	else
		data.droneTargetPos = VecCopy(data.drone.pos)
	end
end

function dronePhysicsStep(data, dt)
	local acc = VecSub(data.droneTargetPos, data.drone.pos)
	data.droneVel = VecAdd(data.droneVel, VecScale(acc, dt))
	data.droneVel = VecScale(data.droneVel, 0.98)
	data.drone.pos = VecAdd(data.drone.pos, VecScale(data.droneVel, dt))
	data.drone.rot = QuatSlerp(data.drone.rot, data.droneTargetRot, 0.02)
end

---------- SERVER ----------

function server.init()
	RegisterTool("attackdrone", "Attack Drone", "MOD/vox/attackdrone.vox")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("attackdrone", true, p)
		local data = players[p]
		for i = 1, 100 do
			data.projectileHandler.shells[i] = deepcopy(data.projectileHandler.defaultShell)
		end
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

	if GetPlayerTool(p) ~= "attackdrone" or GetPlayerVehicle(p) ~= 0 then
		data.attackdroneenabled = false
		data.flycamenabled = false
		return
	end

	-- Initialize drone on equip
	if not data.attackdroneenabled then
		data.attackdroneenabled = true
		data.droneTargetPos = GetPlayerTransform(p).pos
		data.drone.pos = TransformToParentPoint(GetPlayerTransform(p), Vec(0, 0, -3))
		data.drone.rot = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0))
	end

	-- Toggle controls
	if InputPressed("m", p) then
		data.magnet = not data.magnet
	end

	if InputPressed("r", p) then
		data.lockCam = not data.lockCam
	end

	-- Aim pos
	if data.flycamenabled then
		data.aimpos = GetCamLookPos(data)
	else
		data.aimpos = GetAimPos(p)
	end

	-- Firing (server authoritative: MakeHole)
	data.firing = InputDown("usetool", p)
	if data.firing then
		Shoot(p, data)
	end

	-- Magnet (server authoritative: SetBodyVelocity)
	if data.magnet then
		Magnet(data)
	end

	-- Projectile processing
	for key, shell in ipairs(data.projectileHandler.shells) do
		if shell.active then
			ProjectileOperations(shell, dt)
		end
	end

	-- Drone movement
	if not data.flycamenabled then
		droneMovement(p, data, dt)
	end

	-- Drone barrel position
	data.drone.barrel.pos = TransformToParentPoint(data.drone, Vec(0.5, 0.25, -0.2))

	-- Drone physics
	dronePhysicsStep(data, dt)

	if data.shoottimer > 0 then
		data.shoottimer = data.shoottimer - dt
	end
end

---------- CLIENT ----------

function client.init()
	gunsound = LoadSound("MOD/snd/gun0.ogg")
	dronesound = LoadLoop("MOD/snd/drone.ogg")
end

function client.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		local data = players[p]
		for i = 1, 100 do
			data.projectileHandler.shells[i] = deepcopy(data.projectileHandler.defaultShell)
		end
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

	if GetPlayerTool(p) ~= "attackdrone" or GetPlayerVehicle(p) ~= 0 then
		data.attackdroneenabled = false
		data.flycamenabled = false
		return
	end

	local isLocal = (p == GetLocalPlayer())

	-- Initialize drone on equip
	if not data.attackdroneenabled then
		data.attackdroneenabled = true
		data.droneTargetPos = GetPlayerTransform(p).pos
		data.drone.pos = TransformToParentPoint(GetPlayerTransform(p), Vec(0, 0, -3))
		data.drone.rot = QuatRotateQuat(Quat(), QuatEuler(-90, -90, 0))
	end

	-- Toggle controls
	if InputPressed("alttool", p) then
		data.flycamenabled = not data.flycamenabled
	end
	if isLocal and InputPressed("esc") then
		data.flycamenabled = false
	end

	if InputPressed("m", p) then
		data.magnet = not data.magnet
		if isLocal then
			SetString("hud.notification", "Magnet " .. (data.magnet and "on" or "off"))
		end
	end

	if InputPressed("n", p) then
		data.hideSight = not data.hideSight
		if isLocal then
			SetString("hud.notification", "Hide crosshair " .. (data.hideSight and "on" or "off"))
		end
	end

	if InputPressed("r", p) then
		data.lockCam = not data.lockCam
		if isLocal then
			SetString("hud.notification", "Lock cam " .. (data.lockCam and "on" or "off"))
		end
	end

	-- Aim pos
	if data.flycamenabled then
		data.aimpos = GetCamLookPos(data)
	else
		data.aimpos = GetAimPos(p)
	end

	-- Fly cam (local player only)
	if data.flycamenabled and isLocal then
		FlyCam(p, data)
	end

	-- Drone sound
	PlayLoop(dronesound, data.drone.pos, 0.6)

	-- Firing sounds and visuals
	data.firing = InputDown("usetool", p)
	if data.firing then
		if data.shoottimer <= 0 then
			local volume = data.flycamenabled and 0.4 or 0.5
			PlaySound(gunsound, data.drone.barrel.pos, volume)
			data.lightTimer = 0.05
			data.shoottimer = data.shotDelay
		end
	end

	-- Light flash
	if data.lightTimer > 0 then
		PointLight(data.drone.barrel.pos, 1, 1, 1, 1)
		data.lightTimer = data.lightTimer - dt
	end

	-- Tool body shape positioning
	local b = GetToolBody(p)
	if b ~= 0 then
		if data.body ~= b then
			data.body = b
			local shapes = GetBodyShapes(b)
			data.droneshape = shapes[1]
			data.controlshape = shapes[2]
			data.dronetransformation = GetShapeLocalTransform(data.droneshape)
			data.controltransformation = GetShapeLocalTransform(data.controlshape)
		end

		if data.controltransformation then
			local ct = TransformCopy(data.controltransformation)
			ct.rot = QuatRotateQuat(ct.rot, QuatEuler(-25, 0, 0))
			SetShapeLocalTransform(data.controlshape, ct)
		end

		if data.droneshape then
			SetShapeLocalTransform(data.droneshape, TransformToLocalTransform(GetBodyTransform(GetToolBody(p)), data.drone))
		end
	end

	-- Drone movement (client mirrors for smooth visuals)
	if not data.flycamenabled then
		droneMovement(p, data, dt)
	end

	data.drone.barrel.pos = TransformToParentPoint(data.drone, Vec(0.5, 0.25, -0.2))

	-- Drone physics step (mirror)
	dronePhysicsStep(data, dt)

	if data.shoottimer > 0 then
		data.shoottimer = data.shoottimer - dt
	end
end

---------- HUD ----------

function draw()
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end

	if GetPlayerTool(p) == "attackdrone" and GetPlayerVehicle(p) == 0 and data.flycamenabled and not data.hideSight then
		UiPush()
		UiTranslate(UiCenter(), UiMiddle())
		UiColor(1, 1, 1, 0.5)
		UiAlign("center middle")
		UiImage("MOD/img/crosshair.png")
		UiPop()
	end
end
