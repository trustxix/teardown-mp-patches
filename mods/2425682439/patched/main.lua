#version 2
#include "script/include/player.lua"

players = {}

local GRAVITY = Vec(0, 0, 0)
local VELOCITY = 50
local MAX_BEES = 50

function createPlayerData()
	return {
		shells = {},
		shellNum = 1,
		activeBees = 0,
		recoilTimer = 0,
		lightTimer = 0,
		holeMode = false,
		angle = 0,
		angVel = 0,
		toolPos = Vec(0, 0, 0),
		toolTrans = Transform(),
		body = nil,
		hive = nil,
		hiveTransform = nil,
		beeShapes = {},
		beeTransforms = {},
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
-- SERVER
----------------------------------------------------------------------

function server.init()
	RegisterTool("beegun", "Bee Gun", "MOD/vox/beegun.vox")
end

function server.tick(dt)
	-- Phase 1: PlayersAdded
	for _, p in ipairs(PlayersAdded()) do
		players[p] = createPlayerData()
		initShells(players[p])
		SetToolEnabled(p, "beegun", true)
	end

	-- Phase 2: PlayersRemoved
	for _, p in ipairs(PlayersRemoved()) do
		players[p] = nil
	end

	-- Phase 3: Active players
	for _, p in ipairs(Players()) do
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
		-- LMB: shoot
		if InputPressed("usetool", p) then
			local ct = GetPlayerEyeTransform(p)
			local fwdpos = TransformToParentPoint(ct, Vec(0.3, -0.45, -3.2))
			local gunpos = TransformToParentPoint(ct, Vec(0.3, -0.45, -2.2))
			local direction = VecSub(fwdpos, gunpos)

			pd.shells[pd.shellNum] = {
				active = true,
				smokeTime = 2,
				freeTimer = 0,
				bounces = 0,
				explosive = false,
				pos = VecCopy(gunpos),
				predictedBulletVelocity = VecScale(direction, VELOCITY),
				gravity = VecCopy(GRAVITY),
			}
			pd.shellNum = (pd.shellNum % MAX_BEES) + 1
		end

		-- R: toggle hungry mode
		if InputPressed("r", p) then
			pd.holeMode = not pd.holeMode
		end

		-- E: kamikaze single bee
		if InputPressed("e", p) then
			for _, shell in ipairs(pd.shells) do
				if shell.active and not shell.explosive then
					shell.explosive = true
					break
				end
			end
		end

		-- C: kill all bees
		if InputPressed("c", p) then
			for _, shell in ipairs(pd.shells) do
				if shell.active then
					if shell.explosive then
						Explosion(shell.pos, 0.5)
					end
					shell.active = false
				end
			end
		end
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
					if pd.holeMode then
						MakeHole(hitPos, 0.2, 0.2, 0.2)
					end
					-- Bounce
					local dot = VecDot(normal, shell.predictedBulletVelocity)
					shell.predictedBulletVelocity = VecSub(shell.predictedBulletVelocity, VecScale(normal, dot * 2))
					shell.bounces = shell.bounces + 1
					shell.freeTimer = 0
				end
			else
				shell.pos = point2
			end

			-- Lifetime
			shell.freeTimer = shell.freeTimer + dt
			if shell.freeTimer > 20 then
				if shell.explosive then
					Explosion(shell.pos, 0.5)
				end
				shell.active = false
			end
		end
	end
	pd.activeBees = bees
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
	for _, p in ipairs(PlayersAdded()) do
		if not players[p] then
			players[p] = createPlayerData()
			initShells(players[p])
		end
	end

	-- Phase 2: PlayersRemoved
	for _, p in ipairs(PlayersRemoved()) do
		players[p] = nil
	end

	-- Phase 3: Active players
	for _, p in ipairs(Players()) do
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

	if GetPlayerTool(p) == "beegun" and GetPlayerVehicle(p) == 0 then
		-- LMB: shoot (client mirrors for visuals)
		if InputPressed("usetool", p) then
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
				smokeTime = 2,
				freeTimer = 0,
				bounces = 0,
				explosive = false,
				pos = VecCopy(gunpos),
				predictedBulletVelocity = VecScale(direction, VELOCITY),
				gravity = VecCopy(GRAVITY),
			}
			pd.shellNum = (pd.shellNum % MAX_BEES) + 1
		else
			pd.angVel = math.max(0, pd.angVel - dt * 175)
		end

		-- R: toggle hungry mode
		if InputPressed("r", p) then
			pd.holeMode = not pd.holeMode
			if isLocal then
				SetString("hud.notification", "Hungry Bees " .. (pd.holeMode and "on" or "off"))
			end
		end

		-- E: kamikaze single bee
		if InputPressed("e", p) then
			for _, shell in ipairs(pd.shells) do
				if shell.active and not shell.explosive then
					shell.explosive = true
					PlaySound(kamisound, shell.pos, 1, false)
					if isLocal then
						SetString("hud.notification", "Kamikaze Bees enabled!!!")
					end
					break
				end
			end
		end

		-- C: kill all bees
		if InputPressed("c", p) then
			for _, shell in ipairs(pd.shells) do
				if shell.active then
					shell.active = false
					PlaySound(ripsound, shell.pos, 1, false)
				end
			end
			if isLocal then
				SetString("hud.notification", "All bees dead!!!")
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
					-- Bounce
					local dot = VecDot(normal, shell.predictedBulletVelocity)
					shell.predictedBulletVelocity = VecSub(shell.predictedBulletVelocity, VecScale(normal, dot * 2))
					shell.bounces = shell.bounces + 1
					shell.freeTimer = 0
				end
			else
				DrawLine(shell.pos, point2, 1, 1, 0.2)
				PlayLoop(beeloop, shell.pos, 0.6)
				SpawnParticle("smoke", shell.pos, Vec(0, 0.15, 0), 0.15, shell.smokeTime)
				shell.pos = point2
			end

			shell.freeTimer = shell.freeTimer + dt
			if shell.freeTimer > 20 then
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

function draw()
	local p = GetLocalPlayer()
	if not p then return end
	local pd = players[p]
	if not pd then return end
	if GetPlayerTool(p) ~= "beegun" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	UiPush()
		UiTranslate(UiCenter(), UiHeight() - 60)
		UiAlign("center middle")
		UiColor(1, 1, 1)
		UiFont("bold.ttf", 32)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText(pd.activeBees)
	UiPop()
end
