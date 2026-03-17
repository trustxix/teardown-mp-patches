-- Minigun by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

local STATE_READY = 0
local STATE_FIRING = 1
local STATE_WINDING = 2
local STATE_UNWINDING = 3

players = {}

function createPlayerData()
	return {
		state = STATE_READY,
		angle = 0,
		angVel = 0,
		shotDelay = 0.00001,
		startDelay = 0.6,
		bulletsFired = 0,
		simulBullets = 0,
		shootTimer = 0,
		spreadTimer = 0,
		smokeTimer = -1,
		recoilTimer = 0,
		toolPos = Vec(),
		body = nil,
		barrel = nil,
		barrelTransform = nil,
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

---------- SERVER ----------

function server.init()
	RegisterTool("crestaminigun", "Minigun", "MOD/vox/crestaminigun.vox", 3)
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("crestaminigun", true, p)
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
	if GetPlayerTool(p) ~= "crestaminigun" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	local velocity = 1.5

	-- Process projectiles (server authoritative)
	for key, shell in ipairs(data.projectileHandler.shells) do
		if shell.active then
			ProjectileOperations(shell)
		end
	end

	-- Winding state machine
	if InputDown("usetool", p) then
		data.angVel = math.min(500, data.angVel + dt * 1000)
		if data.state == STATE_READY or data.state == STATE_UNWINDING then
			data.state = STATE_WINDING
		end
	else
		data.angVel = math.max(0, data.angVel - dt * 250)
	end

	if InputReleased("usetool", p) then
		if data.state == STATE_FIRING or data.state == STATE_WINDING then
			data.state = STATE_UNWINDING
			data.spreadTimer = 0
			data.simulBullets = 0
		end
	end

	if data.state == STATE_WINDING then
		data.startDelay = data.startDelay - dt
		if data.startDelay <= 0 then
			data.state = STATE_FIRING
		end
	end

	if data.state == STATE_UNWINDING then
		data.startDelay = data.startDelay + dt
		if data.startDelay > 0.6 then
			data.state = STATE_READY
			data.startDelay = 0.6
		end
	end

	-- Firing (server authoritative: recoil, projectiles)
	if data.state == STATE_FIRING then
		if data.shootTimer <= 0 then
			local aimpos, hit, distance = GetAimPos(p)
			if distance and distance > 0 then
				-- Recoil
				local ct = GetPlayerEyeTransform(p)
				local recoildir = TransformToParentVec(ct, Vec(0, 0, 0.25))
				local vel = GetPlayerVelocity(p)
				local oldvel = VecCopy(vel)
				vel = VecAdd(vel, recoildir)
				if VecLength(vel) > 6.5 then vel = oldvel end
				SetPlayerVelocity(vel, p)

				-- Get tool muzzle position
				local b = GetToolBody(p)
				if b ~= 0 then
					local toolTrans = GetBodyTransform(b)
					data.toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.75, -2.1))

					local dir = VecSub(aimpos, data.toolPos)
					local maxSpread = InputDown("ctrl", p) and 2.5 or 5
					local spread = math.min(data.spreadTimer, maxSpread) * distance / 100
					local dmg = math.random(5, 9)
					dir[1] = dir[1] + (math.random() - 0.5) * 2 * spread
					dir[2] = dir[2] + (math.random() - 0.5) * 2 * spread
					dir[3] = dir[3] + (math.random() - 0.5) * 2 * spread

					local handler = data.projectileHandler
					handler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
					local loadedShell = handler.shells[handler.shellNum]
					loadedShell.active = true
					loadedShell.pos = data.toolPos
					loadedShell.damage = dmg / 10
					loadedShell.predictedBulletVelocity = VecScale(dir, velocity * (100 / distance))
					handler.shellNum = (handler.shellNum % #handler.shells) + 1
				end

				data.shootTimer = data.shotDelay
				data.recoilTimer = data.shotDelay
				data.spreadTimer = data.spreadTimer + 0.25
				data.bulletsFired = data.bulletsFired + 1
				data.simulBullets = data.simulBullets + 1
			end
		end
	end

	if data.shootTimer > 0 then
		data.shootTimer = data.shootTimer - dt
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
	end

	for p in PlayersRemoved() do
		players[p] = nil
	end

	for p in Players() do
		client.tickPlayer(p, dt)
	end
end

function client.tickPlayer(p, dt)
	if GetPlayerTool(p) ~= "crestaminigun" then return end
	if GetPlayerVehicle(p) ~= 0 then
		local data = players[p]
		if data then
			data.state = STATE_READY
			data.startDelay = 0.6
		end
		return
	end

	local data = players[p]
	if not data then return end
	local pt = GetPlayerTransform(p)

	-- Mirror server state machine for smooth animations
	if InputDown("usetool", p) then
		data.angVel = math.min(500, data.angVel + dt * 1000)
		if data.state == STATE_READY or data.state == STATE_UNWINDING then
			data.state = STATE_WINDING
			PlaySound(windupsound, pt.pos, 0.5)
		end
	else
		data.angVel = math.max(0, data.angVel - dt * 250)
	end

	if InputReleased("usetool", p) then
		if data.state == STATE_FIRING or data.state == STATE_WINDING then
			data.state = STATE_UNWINDING
			data.spreadTimer = 0
			local b = GetToolBody(p)
			if b ~= 0 then
				local toolTrans = GetBodyTransform(b)
				local toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.75, -2.1))
				if data.simulBullets > 3 then
					SpawnParticle("darksmoke", toolPos, Vec(0, 1.0 + math.random(1, 5) * 0.1, 0), 0.5, 2.5)
					SpawnParticle("smoke", toolPos, Vec(0, 1.0 + math.random(1, 3) * 0.1, 0), 1, 2)
				end
			end
			if data.simulBullets > 100 then
				data.smokeTimer = 1
			end
			data.simulBullets = 0
			PlaySound(winddownsound, pt.pos, 0.5)
		end
	end

	if data.state == STATE_WINDING then
		data.startDelay = data.startDelay - dt
		if data.startDelay <= 0 then
			data.state = STATE_FIRING
		end
	end

	if data.state == STATE_UNWINDING then
		data.startDelay = data.startDelay + dt
		if data.startDelay > 0.6 then
			data.state = STATE_READY
			data.startDelay = 0.6
		end
	end

	-- Firing visual/audio effects
	if data.state == STATE_FIRING then
		PlayLoop(gunsound, pt.pos, 0.6)
		local b = GetToolBody(p)
		if b ~= 0 then
			local toolTrans = GetBodyTransform(b)
			local toolPos = TransformToParentPoint(toolTrans, Vec(0.35, -0.75, -2.1))
			SpawnParticle("fire", toolPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.3, 0.15)
			PointLight(toolPos, 1, 1, 1, 0.5)
		end
		data.bulletsFired = data.bulletsFired + 1
	end

	-- Tool transform and barrel animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local heightOffset = InputDown("ctrl", p) and 0.3 or 0.2
		local offset = Transform(Vec(0.1, heightOffset, 0))
		SetToolTransform(offset, 1.0, p)

		if data.recoilTimer > 0 then
			local t = Transform()
			t.pos = Vec(0.1, heightOffset, 0.01)
			t.rot = QuatEuler(1, 0, 0)
			SetToolTransform(t, 1.0, p)
			data.recoilTimer = data.recoilTimer - dt
		end

		data.angle = data.angle + data.angVel * dt * 5
		local voxSize = 0.1
		local attach = Transform(Vec(2.8 * voxSize, -7.3 * voxSize, 0))
		if data.body ~= b then
			data.body = b
			local shapes = GetBodyShapes(b)
			data.barrel = shapes[1]
			data.barrelTransform = TransformToLocalTransform(attach, GetShapeLocalTransform(data.barrel))
		end

		if data.barrel then
			attach.rot = QuatEuler(0, 0, -data.angle)
			local t = TransformToParentTransform(attach, data.barrelTransform)
			SetShapeLocalTransform(data.barrel, t)
		end
	end

	-- Smoke after sustained fire
	if data.smokeTimer >= 0 then
		local smokepos = TransformToParentPoint(GetPlayerEyeTransform(p), Vec(0.55, -0.65, -1))
		SpawnParticle("smoke", smokepos, Vec(0, 0.5, 0), 0.5, 1.5)
		data.smokeTimer = data.smokeTimer - dt
	end
end

function client.draw()
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end

	if GetPlayerTool(p) == "crestaminigun" and GetPlayerVehicle(p) == 0 then
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
