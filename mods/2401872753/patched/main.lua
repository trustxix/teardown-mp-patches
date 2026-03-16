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
		missileStrength = 20,
		camDist = 2,
		missile = {},
		missileTip = Vec(0, 0, 0),
		smokePos = Vec(0, 0, 0),
		rocketBody = nil,
		rocketTrans = nil,
		body = nil,
	}
end

----------------------------------------------------------------------
-- SERVER
----------------------------------------------------------------------

function server.init()
	RegisterTool("guided", "Guided Missile", "MOD/vox/stinger.vox", 4)
end

function server.tick(dt)
	-- Phase 1: PlayersAdded
	for _, p in ipairs(PlayersAdded()) do
		players[p] = createPlayerData()
		SetToolEnabled(p, "guided", true)
	end

	-- Phase 2: PlayersRemoved
	for _, p in ipairs(PlayersRemoved()) do
		local pd = players[p]
		if pd and pd.rocketBody then
			Delete(pd.rocketBody)
		end
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

	if GetPlayerTool(p) == "guided" and GetPlayerVehicle(p) == 0 then
		-- LMB: launch or detonate
		if InputPressed("usetool", p) then
			if not pd.flying and not pd.detached then
				pd.flying = true
				-- Get rocket shape transform from tool body for spawn position
				local b = GetToolBody(p)
				if b ~= 0 then
					if pd.body ~= b then
						pd.body = b
						local shapes = GetBodyShapes(b)
						if #shapes >= 2 then
							pd.rocketTrans = GetShapeLocalTransform(shapes[2])
						end
					end
				end
				local spawnT = pd.rocketTrans or GetPlayerEyeTransform(p)
				local spawned = Spawn("MOD/vox/rocket.xml", spawnT)
				pd.rocketBody = spawned[1]
			elseif pd.primed and (pd.flying or pd.detached) then
				-- Explode
				serverExplode(p)
			end
		end

		-- RMB: detach
		if InputPressed("alttool", p) then
			if pd.flying then
				pd.flying = false
				pd.detached = true
			end
		end

		-- R: toggle piercing
		if InputPressed("r", p) then
			pd.piercing = not pd.piercing
		end

		-- Cache tool body
		local b = GetToolBody(p)
		if b ~= 0 then
			if pd.body ~= b then
				pd.body = b
				local shapes = GetBodyShapes(b)
				if #shapes >= 2 then
					pd.rocketTrans = GetShapeLocalTransform(shapes[2])
				end
			end
		end
	end

	-- Mousewheel detach
	if pd.flying and InputValue("mousewheel", p) ~= 0 then
		pd.flying = false
		pd.detached = true
	end

	-- Guided flight (server: physics + damage)
	if pd.flying then
		local ct = GetPlayerEyeTransform(p)
		if not pd.missile.pos then pd.missile.pos = ct.pos end
		if not pd.missile.rot then pd.missile.rot = ct.rot end

		local mx = InputValue("mousedx", p)
		local my = InputValue("mousedy", p)
		local s = InputDown("space", p)

		if s then
			pd.missileSpeed = 40
			mx = mx * 0.75
			my = my * 0.75
		else
			pd.missileSpeed = 20
		end

		local forwPos = TransformToParentPoint(pd.missile, Vec(0, 0, -5))
		pd.missile.pos = TransformToParentPoint(pd.missile, Vec(0, 0, -(pd.missileSpeed / 100)))
		pd.missile.rot = QuatLookAt(pd.missile.pos, forwPos)
		pd.missile.rot = QuatRotateQuat(pd.missile.rot, QuatEuler(-my / 10, -mx / 10, 0))
		pd.missileTip = TransformToParentPoint(pd.missile, Vec(0, 0, -1.1))
		pd.smokePos = TransformToParentPoint(pd.missile, Vec(0, 0, 0.9))

		-- Set body transform
		if pd.rocketBody then
			local spritepos = TransformToParentPoint(pd.missile, Vec(0, 0, -0.75))
			local rot = QuatLookAt(pd.missile.pos, pd.missileTip)
			SetBodyTransform(pd.rocketBody, Transform(spritepos, rot))
		end

		pd.primed = true
		serverCheckHit(p)
	end

	-- Detached flight (server: physics + damage)
	if pd.detached then
		if not pd.missile.pos then return end

		pd.missile.pos = TransformToParentPoint(pd.missile, Vec(0, 0, -(pd.missileSpeed / 100)))
		pd.missileTip = TransformToParentPoint(pd.missile, Vec(0, 0, -1.1))
		pd.smokePos = TransformToParentPoint(pd.missile, Vec(0, 0, 1))

		if pd.rocketBody then
			local rot = QuatLookAt(pd.missile.pos, pd.missileTip)
			SetBodyTransform(pd.rocketBody, Transform(pd.missile.pos, rot))
		end

		pd.primed = true
		serverCheckHit(p)
	end
end

function serverCheckHit(p)
	local pd = players[p]
	if not pd then return end

	local fwdpos = TransformToParentPoint(pd.missile, Vec(0, 0, -1.1))
	local dir = VecNormalize(VecSub(fwdpos, pd.missileTip))
	if pd.rocketBody then
		QueryRejectBody(pd.rocketBody)
	end
	local hit, dist = QueryRaycast(pd.missileTip, dir, VecLength(VecSub(fwdpos, pd.missileTip)), 0.1)

	if hit then
		if pd.piercing then
			MakeHole(pd.missileTip, 0.3, 0.3, 0.3)
		else
			serverExplode(p)
		end
	end
end

function serverExplode(p)
	local pd = players[p]
	if not pd then return end

	Explosion(pd.missileTip, pd.missileStrength / 10)
	if pd.rocketBody then
		Delete(pd.rocketBody)
		pd.rocketBody = nil
	end
	pd.missile.pos = nil
	pd.missile.rot = nil
	pd.primed = false
	pd.flying = false
	pd.detached = false
end

----------------------------------------------------------------------
-- CLIENT
----------------------------------------------------------------------

local explosionSound
local flyingSound
local fireSound
local boosterSound
local missileSprite

function client.init()
	explosionSound = LoadSound("MOD/snd/explosion.ogg")
	flyingSound = LoadLoop("MOD/snd/rocket_loop.ogg")
	fireSound = LoadSound("tools/launcher0.ogg")
	boosterSound = LoadLoop("MOD/snd/booster.ogg")
	missileSprite = LoadSprite("MOD/img/missile.png")
end

function client.tick(dt)
	-- Phase 1: PlayersAdded
	for _, p in ipairs(PlayersAdded()) do
		if not players[p] then
			players[p] = createPlayerData()
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

	if GetPlayerTool(p) == "guided" and GetPlayerVehicle(p) == 0 then
		-- LMB: launch or detonate
		if InputPressed("usetool", p) then
			if not pd.flying and not pd.detached then
				pd.flying = true
				PlaySound(fireSound, GetPlayerTransform(p).pos, 1)
				-- Client spawns rocket body for visuals
				local b = GetToolBody(p)
				if b ~= 0 then
					if pd.body ~= b then
						pd.body = b
						local shapes = GetBodyShapes(b)
						if #shapes >= 2 then
							pd.rocketTrans = GetShapeLocalTransform(shapes[2])
						end
					end
				end
				local spawnT = pd.rocketTrans or GetPlayerEyeTransform(p)
				local spawned = Spawn("MOD/vox/rocket.xml", spawnT)
				pd.rocketBody = spawned[1]
			elseif pd.primed and (pd.flying or pd.detached) then
				clientExplode(p)
			end
		end

		-- RMB: detach
		if InputPressed("alttool", p) then
			if pd.flying then
				pd.flying = false
				pd.detached = true
			end
		end

		-- R: toggle piercing
		if InputPressed("r", p) then
			pd.piercing = not pd.piercing
			if isLocal then
				SetString("hud.notification", "Piercing rocket " .. (pd.piercing and "on" or "off"))
			end
		end

		-- Cache tool body
		local b = GetToolBody(p)
		if b ~= 0 then
			if pd.body ~= b then
				pd.body = b
				local shapes = GetBodyShapes(b)
				if #shapes >= 2 then
					pd.rocketTrans = GetShapeLocalTransform(shapes[2])
				end
			end
		end
	end

	-- Mousewheel detach (local only)
	if isLocal and pd.flying and InputValue("mousewheel", p) ~= 0 then
		pd.flying = false
		pd.detached = true
	end

	-- Guided flight (client: visuals + camera)
	if pd.flying then
		local ct = GetPlayerEyeTransform(p)
		if not pd.missile.pos then pd.missile.pos = ct.pos end
		if not pd.missile.rot then pd.missile.rot = ct.rot end

		local mx = InputValue("mousedx", p)
		local my = InputValue("mousedy", p)
		local s = InputDown("space", p)

		if s then
			pd.missileSpeed = 40
			PlayLoop(boosterSound, pd.missile.pos, 0.6, false)
			mx = mx * 0.75
			my = my * 0.75
		else
			pd.missileSpeed = 20
		end

		local forwPos = TransformToParentPoint(pd.missile, Vec(0, 0, -5))
		pd.missile.pos = TransformToParentPoint(pd.missile, Vec(0, 0, -(pd.missileSpeed / 100)))
		pd.missile.rot = QuatLookAt(pd.missile.pos, forwPos)
		pd.missile.rot = QuatRotateQuat(pd.missile.rot, QuatEuler(-my / 10, -mx / 10, 0))
		pd.missileTip = TransformToParentPoint(pd.missile, Vec(0, 0, -1.1))
		pd.smokePos = TransformToParentPoint(pd.missile, Vec(0, 0, 0.9))

		-- Guided camera only for local player
		if isLocal then
			local flycam = {}
			flycam.pos = TransformToParentPoint(pd.missile, Vec(0, pd.camDist / 3, pd.camDist))
			flycam.rot = QuatCopy(pd.missile.rot)
			SetCameraTransform(flycam)
		end

		-- Set rocket body position
		if pd.rocketBody then
			local spritepos = TransformToParentPoint(pd.missile, Vec(0, 0, -0.75))
			local rot = QuatLookAt(pd.missile.pos, pd.missileTip)
			SetBodyTransform(pd.rocketBody, Transform(spritepos, rot))
		end

		-- Visuals
		PlayLoop(flyingSound, pd.missile.pos, 0.2, false)
		SpawnParticle("fire", pd.smokePos, Vec(0, 0, 0), 0.75, 0.25)
		SpawnParticle("smoke", pd.smokePos, Vec(0, 0, 0), 1, 2)
		pd.primed = true

		-- Client hit check for visual feedback (piercing sparks)
		clientCheckHit(p)
	end

	-- Detached flight (client: visuals)
	if pd.detached then
		if not pd.missile.pos then return end

		pd.missile.pos = TransformToParentPoint(pd.missile, Vec(0, 0, -(pd.missileSpeed / 100)))
		pd.missileTip = TransformToParentPoint(pd.missile, Vec(0, 0, -1.1))
		pd.smokePos = TransformToParentPoint(pd.missile, Vec(0, 0, 1))

		if pd.rocketBody then
			local rot = QuatLookAt(pd.missile.pos, pd.missileTip)
			SetBodyTransform(pd.rocketBody, Transform(pd.missile.pos, rot))
		end

		PlayLoop(flyingSound, pd.missile.pos, 0.2, false)
		SpawnParticle("fire", pd.smokePos, Vec(0, 0, 0), 0.75, 0.25)
		SpawnParticle("smoke", pd.smokePos, Vec(0, 0, 0), 1, 2)
		pd.primed = true

		clientCheckHit(p)
	end
end

function clientCheckHit(p)
	local pd = players[p]
	if not pd then return end

	local fwdpos = TransformToParentPoint(pd.missile, Vec(0, 0, -1.1))
	local dir = VecNormalize(VecSub(fwdpos, pd.missileTip))
	if pd.rocketBody then
		QueryRejectBody(pd.rocketBody)
	end
	local hit, dist = QueryRaycast(pd.missileTip, dir, VecLength(VecSub(fwdpos, pd.missileTip)), 0.1)

	if hit then
		if not pd.piercing then
			clientExplode(p)
		end
	end
end

function clientExplode(p)
	local pd = players[p]
	if not pd then return end

	PlaySound(explosionSound, pd.missile.pos, 8, false)
	if pd.rocketBody then
		Delete(pd.rocketBody)
		pd.rocketBody = nil
	end
	pd.missile.pos = nil
	pd.missile.rot = nil
	pd.primed = false
	pd.flying = false
	pd.detached = false
end

----------------------------------------------------------------------
-- DRAW (HUD)
----------------------------------------------------------------------

function draw()
	local p = GetLocalPlayer()
	if not p then return end
	local pd = players[p]
	if not pd then return end
	if GetPlayerTool(p) ~= "guided" then return end

	if pd.piercing then
		UiPush()
			UiTranslate(UiCenter(), UiHeight() - 60)
			UiAlign("center middle")
			UiColor(1, 0.4, 0.4)
			UiFont("bold.ttf", 24)
			UiTextOutline(0, 0, 0, 1, 0.1)
			UiText("PIERCING")
		UiPop()
	end
end
