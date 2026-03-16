-- HADOUKEN! by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		swingTimer = 0,
		projectileHandler = {
			shellNum = 1,
			shells = {},
			defaultShell = {active = false, strength = 2.5, maxDist = 7.5, maxMass = 1500},
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

function HadoukenBlast(projectile)
	local mi = VecAdd(projectile.pos, Vec(-projectile.maxDist / 2, -projectile.maxDist / 2, -projectile.maxDist / 2))
	local ma = VecAdd(projectile.pos, Vec(projectile.maxDist / 2, projectile.maxDist / 2, projectile.maxDist / 2))
	QueryRequire("physical dynamic")
	local bodies = QueryAabbBodies(mi, ma)

	for i = 1, #bodies do
		local b = bodies[i]
		local bmi, bma = GetBodyBounds(b)
		local bc = VecLerp(bmi, bma, 0.5)
		local dir = VecSub(bc, projectile.pos)
		local dist = VecLength(dir)
		dir = VecScale(dir, 1.0 / dist)
		local mass = GetBodyMass(b)

		if dist < projectile.maxDist and mass < projectile.maxMass then
			dir[2] = 0
			dir = VecNormalize(dir)
			local massScale = 1 - math.min(mass / projectile.maxMass, 1.0)
			local distScale = 1 - math.min(dist / projectile.maxDist, 1.0)
			local add = VecScale(dir, projectile.strength * massScale * distScale)
			local vel = GetBodyVelocity(b)
			vel = VecAdd(vel, add)
			SetBodyVelocity(b, vel)
		end
	end
end

---------- SERVER ----------

local hadoukenSprite = nil

function server.init()
	RegisterTool("hadouken", "Hadouken", "MOD/vox/hadouken.vox")
	hadoukenSprite = LoadSprite("MOD/img/hadouken.png")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("hadouken", true, p)
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
	if GetPlayerTool(p) ~= "hadouken" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	local velocity = 0.2
	local hadoukendamage = 1.5

	-- Shoot
	if InputPressed("usetool", p) then
		local ct = GetPlayerEyeTransform(p)
		local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
		local gunpos = TransformToParentPoint(ct, Vec(0, 0, -2))
		local direction = VecSub(forwardPos, gunpos)

		local handler = data.projectileHandler
		handler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
		local loadedShell = handler.shells[handler.shellNum]
		loadedShell.active = true
		loadedShell.pos = gunpos
		loadedShell.counter = 1
		loadedShell.predictedBulletVelocity = VecScale(direction, velocity)
		handler.shellNum = (handler.shellNum % #handler.shells) + 1

		data.swingTimer = 0.3
	end

	-- Boom (detonate all)
	if InputPressed("rmb", p) then
		for key, shell in ipairs(data.projectileHandler.shells) do
			if shell.active then
				Explosion(shell.pos, 2)
				shell.active = false
			end
		end
	end

	-- Process projectiles
	for key, shell in ipairs(data.projectileHandler.shells) do
		if shell.active then
			local ballgravity = Vec(0, 0, 0)
			shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(ballgravity, GetTimeStep()))
			local point2 = VecAdd(shell.pos, VecScale(shell.predictedBulletVelocity, GetTimeStep()))

			local mi = VecAdd(shell.pos, Vec(-0.5, -0.5, -0.5))
			local ma = VecAdd(shell.pos, Vec(0.5, 0.5, 0.5))
			QueryRequire("physical")
			local shapes = QueryAabbShapes(mi, ma)

			if #shapes > 0 and shell.counter % 3 == 0 then
				MakeHole(shell.pos, hadoukendamage, hadoukendamage, hadoukendamage)
			end

			HadoukenBlast(shell)

			shell.counter = shell.counter + 1
			shell.pos = point2
		end
	end
end

---------- CLIENT ----------

function client.init()
	hadoukensound = LoadSound("MOD/snd/hadouken.ogg")
	hadoukenSprite = LoadSprite("MOD/img/hadouken.png")
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
	if GetPlayerTool(p) ~= "hadouken" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	if not data then return end
	local pt = GetPlayerTransform(p)
	local velocity = 0.2

	-- Shoot: mirror server projectile creation + play sound
	if InputPressed("usetool", p) then
		PlaySound(hadoukensound, pt.pos, 0.45)
		data.swingTimer = 0.3

		-- Create projectile on client too (for visual tracking)
		local ct = GetPlayerEyeTransform(p)
		local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
		local gunpos = TransformToParentPoint(ct, Vec(0, 0, -2))
		local direction = VecSub(forwardPos, gunpos)

		local handler = data.projectileHandler
		handler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
		local loadedShell = handler.shells[handler.shellNum]
		loadedShell.active = true
		loadedShell.pos = gunpos
		loadedShell.counter = 1
		loadedShell.predictedBulletVelocity = VecScale(direction, velocity)
		handler.shellNum = (handler.shellNum % #handler.shells) + 1
	end

	-- Boom: mirror server detonation
	if InputPressed("rmb", p) then
		for key, shell in ipairs(data.projectileHandler.shells) do
			if shell.active then
				shell.active = false
			end
		end
	end

	-- Mirror projectile movement on client (for sprite positions)
	for key, shell in ipairs(data.projectileHandler.shells) do
		if shell.active then
			local ballgravity = Vec(0, 0, 0)
			shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(ballgravity, GetTimeStep()))
			local point2 = VecAdd(shell.pos, VecScale(shell.predictedBulletVelocity, GetTimeStep()))

			-- Draw sprite at current position
			local rot = QuatLookAt(shell.pos, GetPlayerEyeTransform(p).pos)
			local transform = Transform(shell.pos, rot)
			DrawSprite(hadoukenSprite, transform, 2, 2, 0.5, 0.5, 0.5, 0.75, true, false)

			shell.counter = shell.counter + 1
			shell.pos = point2
		end
	end

	-- Tool animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local offset = Transform(Vec(0, 0, 0), QuatEuler(10, 0, 0))
		SetToolTransform(offset, 1.0, p)

		if data.swingTimer > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, -data.swingTimer * 3)
			t.rot = QuatEuler(data.swingTimer * 20, 0, 0)
			SetToolTransform(t, 1.0, p)
			data.swingTimer = data.swingTimer - dt
		end
	end
end
