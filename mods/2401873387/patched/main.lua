#version 2
#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		smashTimer = 0,
		soundtimer = 0,
		spinsmash = false,
	}
end

---------- SERVER ----------

function server.init()
	RegisterTool("lightkatana", "Lightkatana", "MOD/vox/lightkatana.vox")
end

function server.tick(dt)
	for _, p in ipairs(PlayersAdded()) do
		players[p] = createPlayerData()
		SetToolEnabled(p, "lightkatana", true)
	end
	for _, p in ipairs(PlayersRemoved()) do
		players[p] = nil
	end
	for _, p in ipairs(Players()) do
		server.tickPlayer(p, dt)
	end
end

function server.tickPlayer(p, dt)
	local d = players[p]
	if not d then return end
	if GetPlayerTool(p) ~= "lightkatana" or GetPlayerVehicle(p) ~= 0 then return end

	SetPlayerHealth(p, 1)

	if InputPressed("jump", p) then
		local pt = GetPlayerTransform(p)
		local dir = TransformToParentVec(pt, Vec(0, 7.5, -2.5))
		local vel = GetPlayerVelocity(p)
		vel[2] = 0
		vel = VecAdd(vel, dir)
		SetPlayerVelocity(vel, p)
	end

	if InputPressed("usetool", p) then
		if d.smashTimer == 0 then d.smashTimer = 0.1 end
	end

	if InputPressed("alttool", p) then
		d.spinsmash = true
		if d.smashTimer == 0 then d.smashTimer = 0.1 end
	end

	-- Blade tip MakeHole (constant while equipped)
	local b = GetToolBody(p)
	if b ~= 0 then
		local tipPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.05, -0.05, -2.7))
		MakeHole(tipPos, 0.2, 0.2, 0.2)
	end

	-- Slash MakeHole on timer expiry
	if d.smashTimer > 0 then
		d.smashTimer = d.smashTimer - dt
		if d.smashTimer < 0.0001 then
			local eye = GetPlayerEyeTransform(p)
			local holeposes = {}
			local hitcount = 0
			for i = 1, 16 do
				local inc = 0.2 * i
				local meleedist = 3.6
				if i < 6 or i > 10 then meleedist = meleedist * 0.95 end
				if i < 5 or i > 11 then meleedist = meleedist * 0.95 end
				if i < 4 or i > 12 then meleedist = meleedist * 0.95 end
				if i < 3 or i > 13 then meleedist = meleedist * 0.95 end
				if i < 2 or i > 14 then meleedist = meleedist * 0.95 end
				local vec = d.spinsmash and Vec(-1.5 + inc, 0, -meleedist) or Vec(0, -1.3 + inc, -meleedist)

				local fwdpos = TransformToParentPoint(eye, vec)
				local direction = VecSub(fwdpos, eye.pos)
				local distance = VecLength(direction)
				direction = VecNormalize(direction)
				local hit, hitDistance = QueryRaycast(eye.pos, direction, distance)

				if hit then
					hitcount = hitcount + 1
					local vec2 = d.spinsmash and Vec(-1.5 + inc, 0, -hitDistance) or Vec(0, -1.3 + inc, -hitDistance)
					vec2 = VecScale(vec2, 1.03)
					if i < 6 or i > 10 then vec2 = VecScale(vec2, 0.95) end
					if i < 4 or i > 12 then vec2 = VecScale(vec2, 0.95) end
					if i < 2 or i > 14 then vec2 = VecScale(vec2, 0.95) end
					holeposes[hitcount] = TransformToParentPoint(eye, vec2)
				end
			end
			for i = 1, #holeposes do
				MakeHole(holeposes[i], 0.3, 0.3, 0.3)
			end
			d.smashTimer = 0
			d.spinsmash = false
		end
	end
end

---------- CLIENT ----------

function client.init()
	swingsound = LoadSound("MOD/snd/swing0.ogg")
	hitsound = LoadLoop("MOD/snd/hitloop.ogg")
	saberonsound = LoadSound("MOD/snd/saberon.ogg")
end

function client.tick(dt)
	for _, p in ipairs(PlayersAdded()) do
		players[p] = createPlayerData()
	end
	for _, p in ipairs(PlayersRemoved()) do
		players[p] = nil
	end
	for _, p in ipairs(Players()) do
		client.tickPlayer(p, dt)
	end
end

function client.tickPlayer(p, dt)
	local d = players[p]
	if not d then return end
	if GetPlayerTool(p) ~= "lightkatana" or GetPlayerVehicle(p) ~= 0 then return end

	if InputPressed("usetool", p) then
		if d.smashTimer == 0 then d.smashTimer = 0.1 end
	end

	if InputPressed("alttool", p) then
		d.spinsmash = true
		if d.smashTimer == 0 then d.smashTimer = 0.1 end
	end

	-- Tool animation and blade tip light
	local b = GetToolBody(p)
	if b ~= 0 then
		local offset = Transform(Vec(0.3, -0.7, -0.8), QuatEuler(60, -5, 0))
		SetToolTransform(offset, 1.0, p)

		local tipPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.05, -0.05, -2.7))
		PointLight(tipPos, 1, 0.1, 0.1, 0.5)

		if d.smashTimer > 0 then
			if d.spinsmash then
				local t = Transform()
				t.pos = Vec(0.3, -0.6, -0.85 + d.smashTimer * 2)
				t.rot = QuatEuler(0, 60, -90)
				SetToolTransform(t, 1.0, p)
			else
				local t = Transform()
				t.pos = Vec(0.3, -0.6, -0.85 + d.smashTimer * 2)
				t.rot = QuatEuler(-d.smashTimer * 400, d.smashTimer * 150, 0)
				SetToolTransform(t, 1.0, p)
			end
		end

		if InputDown("usetool", p) and d.smashTimer == 0 then
			local t = Transform()
			t.pos = Vec(0.3, -0.6, -0.95)
			t.rot = QuatEuler(5, 5, 0)
			SetToolTransform(t, 1.0, p)
		end
	end

	-- Spin camera effect (local player only)
	if InputDown("alttool", p) and p == GetLocalPlayer() then
		local ct = GetPlayerEyeTransform(p)
		local pt = GetPlayerTransform(p)
		pt.pos[2] = pt.pos[2] + 1.8
		ct.pos = pt.pos
		ct.rot = QuatRotateQuat(ct.rot, QuatEuler(0, 10, 0))
		SetCameraTransform(ct)
	end

	-- Sound on slash completion
	if d.smashTimer > 0 then
		d.smashTimer = d.smashTimer - dt
		if d.smashTimer < 0.0001 then
			PlaySound(swingsound, GetPlayerTransform(p).pos, 0.6)
			d.smashTimer = 0
			d.spinsmash = false
		end
	end
end

---------- HUD ----------

function draw()
	local p = GetLocalPlayer()
	if not p or not players[p] then return end
end
