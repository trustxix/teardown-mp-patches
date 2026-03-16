-- Dual Miniguns by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

local STATE_READY = 0
local STATE_FIRING = 1
local STATE_WINDING = 2
local STATE_UNWINDING = 3

players = {}

function createPlayerData()
	return {
		gun1 = {
			state = STATE_READY,
			startDelay = 0.6,
			spreadTimer = 0,
			smokeTimer = -1,
			simulBullets = 0,
			angle = 0,
			angVel = 0,
		},
		gun2 = {
			state = STATE_READY,
			startDelay = 0.6,
			spreadTimer = 0,
			smokeTimer = -1,
			simulBullets = 0,
			angle = 0,
			angVel = 0,
		},
		bulletsFired = 0,
		maxVel = 6.5,
		leftPos = Vec(),
		rightPos = Vec(),
		body = nil,
		barrel1 = nil,
		barrel2 = nil,
		barrelTransform1 = nil,
		barrelTransform2 = nil,
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

function GetAimPos(p)
	local ct = GetPlayerEyeTransform(p)
	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
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

function ShootGun(p, data, gun, muzzlePos)
	local velocity = 1.5
	local ct = GetPlayerEyeTransform(p)
	local aimpos, hit, distance = GetAimPos(p)
	if not distance or distance <= 0 then return end

	-- Recoil
	local recoildir = TransformToParentVec(ct, Vec(0, 0, 0.25))
	local vel = GetPlayerVelocity(p)
	local oldvel = VecCopy(vel)
	vel = VecAdd(vel, recoildir)
	if VecLength(vel) > data.maxVel then vel = oldvel end
	SetPlayerVelocity(vel, p)

	local dir = VecSub(aimpos, muzzlePos)
	local maxSpread = InputDown("ctrl", p) and 2.5 or 5
	local spread = math.min(gun.spreadTimer, maxSpread) * distance / 100
	local dmg = math.random(5, 9)
	dir[1] = dir[1] + (math.random() - 0.5) * 2 * spread
	dir[2] = dir[2] + (math.random() - 0.5) * 2 * spread
	dir[3] = dir[3] + (math.random() - 0.5) * 2 * spread

	local handler = data.projectileHandler
	handler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
	local loadedShell = handler.shells[handler.shellNum]
	loadedShell.active = true
	loadedShell.pos = VecCopy(muzzlePos)
	loadedShell.damage = dmg / 10
	loadedShell.predictedBulletVelocity = VecScale(dir, velocity * (100 / distance))
	handler.shellNum = (handler.shellNum % #handler.shells) + 1

	gun.spreadTimer = gun.spreadTimer + 0.25
	data.bulletsFired = data.bulletsFired + 1
	gun.simulBullets = gun.simulBullets + 1
end

function ProjectileOperations(projectile)
	local gravity = Vec(0, 0, 0)
	projectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity, VecScale(gravity, GetTimeStep()))
	local point2 = VecAdd(projectile.pos, VecScale(projectile.predictedBulletVelocity, GetTimeStep()))
	local dir = VecNormalize(VecSub(point2, projectile.pos))
	local hit, dist = QueryRaycast(projectile.pos, dir, VecLength(VecSub(point2, projectile.pos)))

	if hit then
		local hitPos = VecAdd(projectile.pos, VecScale(VecNormalize(VecSub(point2, projectile.pos)), dist))
		projectile.active = false
		MakeHole(hitPos, projectile.damage, projectile.damage * 0.75, projectile.damage * 0.5)
		SpawnParticle("smoke", hitPos, Vec(0, 1.0 + math.random(1, 5) * 0.1, 0), projectile.damage, 1)
	else
		DrawLine(projectile.pos, point2)
	end

	projectile.pos = point2
end

function tickGunState(gun, dt, inputDown, inputReleased)
	if inputDown then
		gun.angVel = math.min(500, gun.angVel + dt * 1000)
		if gun.state == STATE_READY or gun.state == STATE_UNWINDING then
			gun.state = STATE_WINDING
		end
	else
		gun.angVel = math.max(0, gun.angVel - dt * 250)
	end

	if inputReleased then
		if gun.state == STATE_FIRING or gun.state == STATE_WINDING then
			gun.state = STATE_UNWINDING
			gun.spreadTimer = 0
			gun.simulBullets = 0
		end
	end

	if gun.state == STATE_WINDING then
		gun.startDelay = gun.startDelay - dt
		if gun.startDelay <= 0 then
			gun.state = STATE_FIRING
		end
	end

	if gun.state == STATE_UNWINDING then
		gun.startDelay = gun.startDelay + dt
		if gun.startDelay > 0.6 then
			gun.state = STATE_READY
			gun.startDelay = 0.6
		end
	end
end

---------- SERVER ----------

function server.init()
	RegisterTool("dualminiguns", "Dual Miniguns", "MOD/vox/dualminiguns.vox")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("dualminiguns", true, p)
		local data = players[p]
		for i = 1, 300 do
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
	if GetPlayerTool(p) ~= "dualminiguns" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	if not data then return end

	-- Process projectiles (server authoritative)
	for key, shell in ipairs(data.projectileHandler.shells) do
		if shell.active then
			ProjectileOperations(shell)
		end
	end

	-- Dual fire maxVel
	if InputDown("usetool", p) and InputDown("alttool", p) then
		data.maxVel = 9
	else
		data.maxVel = 6.5
	end

	-- Gun 1 state (LMB = usetool fires left barrel)
	local g1down = InputDown("usetool", p)
	local g1released = InputReleased("usetool", p)
	tickGunState(data.gun1, dt, g1down, g1released)

	-- Gun 2 state (RMB = alttool fires right barrel)
	local g2down = InputDown("alttool", p)
	local g2released = InputReleased("alttool", p)
	tickGunState(data.gun2, dt, g2down, g2released)

	-- Compute muzzle positions from tool body
	local b = GetToolBody(p)
	if b ~= 0 then
		local toolTrans = GetBodyTransform(b)
		data.leftPos = TransformToParentPoint(toolTrans, Vec(-0.55, -0.7, -2))
		data.rightPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.7, -2))
	end

	-- Gun1 (LMB) fires from left muzzle
	if data.gun1.state == STATE_FIRING then
		ShootGun(p, data, data.gun1, data.leftPos)
	end

	-- Gun2 (RMB) fires from right muzzle
	if data.gun2.state == STATE_FIRING then
		ShootGun(p, data, data.gun2, data.rightPos)
	end
end

---------- CLIENT ----------

function client.init()
	gunsound = LoadLoop("MOD/snd/gunloop.ogg")
	cocksound = LoadSound("MOD/snd/m249_cock.ogg")
	windupsound = LoadSound("MOD/snd/windup.ogg")
	winddownsound = LoadSound("MOD/snd/winddown.ogg")
end

function client.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		local data = players[p]
		for i = 1, 300 do
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
	if GetPlayerTool(p) ~= "dualminiguns" then return end
	if GetPlayerVehicle(p) ~= 0 then
		local data = players[p]
		if data then
			data.gun1.state = STATE_READY
			data.gun2.state = STATE_READY
			data.gun1.startDelay = 0.6
			data.gun2.startDelay = 0.6
		end
		return
	end

	local data = players[p]
	if not data then return end
	local pt = GetPlayerTransform(p)

	-- Mirror gun1 state (LMB = usetool)
	local g1down = InputDown("usetool", p)
	local g1released = InputReleased("usetool", p)

	if g1down then
		data.gun1.angVel = math.min(500, data.gun1.angVel + dt * 1000)
		if data.gun1.state == STATE_READY or data.gun1.state == STATE_UNWINDING then
			data.gun1.state = STATE_WINDING
			PlaySound(windupsound, pt.pos, 0.5)
		end
	else
		data.gun1.angVel = math.max(0, data.gun1.angVel - dt * 250)
	end

	if g1released then
		if data.gun1.state == STATE_FIRING or data.gun1.state == STATE_WINDING then
			data.gun1.state = STATE_UNWINDING
			data.gun1.spreadTimer = 0
			if data.gun1.simulBullets > 3 then
				SpawnParticle("darksmoke", data.leftPos, Vec(0, 1.0 + math.random(1, 5) * 0.1, 0), 0.5, 2.5)
				SpawnParticle("smoke", data.leftPos, Vec(0, 1.0 + math.random(1, 3) * 0.1, 0), 1, 2)
			end
			if data.gun1.simulBullets > 100 then
				data.gun1.smokeTimer = 1
			end
			data.gun1.simulBullets = 0
			PlaySound(winddownsound, pt.pos, 0.5)
		end
	end

	if data.gun1.state == STATE_WINDING then
		data.gun1.startDelay = data.gun1.startDelay - dt
		if data.gun1.startDelay <= 0 then
			data.gun1.state = STATE_FIRING
		end
	end
	if data.gun1.state == STATE_UNWINDING then
		data.gun1.startDelay = data.gun1.startDelay + dt
		if data.gun1.startDelay > 0.6 then
			data.gun1.state = STATE_READY
			data.gun1.startDelay = 0.6
		end
	end

	-- Mirror gun2 state (RMB = alttool)
	local g2down = InputDown("alttool", p)
	local g2released = InputReleased("alttool", p)

	if g2down then
		data.gun2.angVel = math.min(500, data.gun2.angVel + dt * 1000)
		if data.gun2.state == STATE_READY or data.gun2.state == STATE_UNWINDING then
			data.gun2.state = STATE_WINDING
			PlaySound(windupsound, pt.pos, 0.5)
		end
	else
		data.gun2.angVel = math.max(0, data.gun2.angVel - dt * 250)
	end

	if g2released then
		if data.gun2.state == STATE_FIRING or data.gun2.state == STATE_WINDING then
			data.gun2.state = STATE_UNWINDING
			data.gun2.spreadTimer = 0
			if data.gun2.simulBullets > 3 then
				SpawnParticle("darksmoke", data.rightPos, Vec(0, 1.0 + math.random(1, 5) * 0.1, 0), 0.5, 2.5)
				SpawnParticle("smoke", data.rightPos, Vec(0, 1.0 + math.random(1, 3) * 0.1, 0), 1, 2)
			end
			if data.gun2.simulBullets > 100 then
				data.gun2.smokeTimer = 1
			end
			data.gun2.simulBullets = 0
			PlaySound(winddownsound, pt.pos, 0.5)
		end
	end

	if data.gun2.state == STATE_WINDING then
		data.gun2.startDelay = data.gun2.startDelay - dt
		if data.gun2.startDelay <= 0 then
			data.gun2.state = STATE_FIRING
		end
	end
	if data.gun2.state == STATE_UNWINDING then
		data.gun2.startDelay = data.gun2.startDelay + dt
		if data.gun2.startDelay > 0.6 then
			data.gun2.state = STATE_READY
			data.gun2.startDelay = 0.6
		end
	end

	-- Firing visual/audio effects
	if data.gun1.state == STATE_FIRING then
		PlayLoop(gunsound, pt.pos, 0.6)
		SpawnParticle("fire", data.leftPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.3, 0.15)
		PointLight(data.leftPos, 1, 1, 1, 0.5)
	end

	if data.gun2.state == STATE_FIRING then
		PlayLoop(gunsound, pt.pos, 0.6)
		SpawnParticle("fire", data.rightPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.3, 0.15)
		PointLight(data.rightPos, 1, 1, 1, 0.5)
	end

	-- Tool transform and barrel animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local heightOffset = InputDown("ctrl", p) and 0.3 or 0.2
		local offset = Transform(Vec(0.1, heightOffset, 0))
		SetToolTransform(offset, 1.0, p)

		local toolTrans = GetBodyTransform(b)
		data.leftPos = TransformToParentPoint(toolTrans, Vec(-0.55, -0.7, -2))
		data.rightPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.7, -2))

		data.gun1.angle = data.gun1.angle + data.gun1.angVel * dt * 5
		data.gun2.angle = data.gun2.angle + data.gun2.angVel * dt * 5

		local voxSize = 0.1
		local attach1 = Transform(Vec(2.8 * voxSize, -7.3 * voxSize, 0))
		local attach2 = Transform(Vec(-5.3 * voxSize, -7.3 * voxSize, 0))

		if data.body ~= b then
			data.body = b
			local shapes = GetBodyShapes(b)
			data.barrel1 = shapes[1]
			data.barrel2 = shapes[3]
			data.barrelTransform1 = TransformToLocalTransform(attach1, GetShapeLocalTransform(data.barrel1))
			data.barrelTransform2 = TransformToLocalTransform(attach2, GetShapeLocalTransform(data.barrel2))
		end

		if data.barrel1 and data.barrelTransform1 then
			attach1.rot = QuatEuler(0, 0, -data.gun2.angle)
			local t = TransformToParentTransform(attach1, data.barrelTransform1)
			SetShapeLocalTransform(data.barrel1, t)
		end

		if data.barrel2 and data.barrelTransform2 then
			attach2.rot = QuatEuler(0, 0, -data.gun1.angle)
			local t2 = TransformToParentTransform(attach2, data.barrelTransform2)
			SetShapeLocalTransform(data.barrel2, t2)
		end
	end

	-- Smoke after sustained fire
	if data.gun1.smokeTimer >= 0 then
		local smokepos = TransformToParentPoint(GetPlayerEyeTransform(p), Vec(-0.55, -0.65, -1))
		SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), 0.5, 1.5)
		data.gun1.smokeTimer = data.gun1.smokeTimer - dt
	end
	if data.gun2.smokeTimer >= 0 then
		local smokepos = TransformToParentPoint(GetPlayerEyeTransform(p), Vec(0.55, -0.65, -1))
		SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), 0.5, 1.5)
		data.gun2.smokeTimer = data.gun2.smokeTimer - dt
	end
end

---------- HUD ----------

function draw()
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end

	if GetPlayerTool(p) == "dualminiguns" and GetPlayerVehicle(p) == 0 then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 60)
		UiAlign("center middle")
		UiColor(1, 1, 1)
		UiFont("bold.ttf", 32)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText(data.bulletsFired)
		UiPop()
	end
end
