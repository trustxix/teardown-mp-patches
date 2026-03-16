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
	}
end

---------- SERVER ----------

function server.init()
	RegisterTool("guided", "Guided Missile", "MOD/vox/stinger.vox", 4)
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

	-- Detach
	if InputPressed("rmb", p) then
		if data.flying then
			data.flying = false
			data.detached = true
		end
	end

	-- Scroll wheel detach
	if data.flying and InputValue("mousewheel", p) ~= 0 then
		data.flying = false
		data.detached = true
	end

	-- Toggle piercing
	if InputPressed("r", p) then
		data.piercing = not data.piercing
		SetString("hud.notification", "Piercing rocket " .. (data.piercing and "on" or "off"), true)
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

	-- Detach mirror
	if InputPressed("rmb", p) then
		if data.flying then
			data.flying = false
			data.detached = true
		end
	end
	if data.flying and InputValue("mousewheel", p) ~= 0 then
		data.flying = false
		data.detached = true
	end

	-- Piercing mirror
	if InputPressed("r", p) then
		data.piercing = not data.piercing
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

function draw()
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end

	if GetPlayerTool(p) == "guided" and data.piercing then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 60)
		UiAlign("center middle")
		UiColor(1, 0.5, 0.5)
		UiFont("bold.ttf", 24)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText("PIERCING")
		UiPop()
	end
end
