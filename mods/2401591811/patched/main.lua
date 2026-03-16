#version 2
#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		smashTimer = 0,
		soundtimer = 0,
		swingTimer = 0,
		spinsmash = false,
		playsound = false,
	}
end

---------- HELPERS ----------

function Boost(p)
	local pt = GetPlayerTransform(p)
	local d = TransformToParentVec(pt, Vec(0, 7.5, -2.5))
	local vel = GetPlayerVelocity(p)
	vel[2] = 0
	vel = VecAdd(vel, d)
	SetPlayerVelocity(vel, p)
end

---------- SERVER ----------

function server.init()
	RegisterTool("dragonslayer", "Dragonslayer", "MOD/vox/dragonslayer.vox")
end

function server.tick(dt)
	for _, p in ipairs(PlayersAdded()) do
		players[p] = createPlayerData()
		SetToolEnabled(p, "dragonslayer", true)
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
	if GetPlayerTool(p) ~= "dragonslayer" or GetPlayerVehicle(p) ~= 0 then return end

	SetPlayerHealth(p, 1)

	if InputPressed("usetool", p) then
		if d.smashTimer == 0 then d.smashTimer = 0.1 end
	end

	if InputPressed("jump", p) then
		Boost(p)
	end

	if InputDown("alttool", p) then
		if d.smashTimer == 0 then d.smashTimer = 0.05 end
		if d.soundtimer == 0 then d.soundtimer = 0.05 end
		d.spinsmash = true
	else
		d.spinsmash = false
	end

	if d.smashTimer > 0 then
		d.smashTimer = d.smashTimer - dt
		if d.smashTimer < 0.0001 then
			d.playsound = false
			local eye = GetPlayerEyeTransform(p)
			for i = 1, 3 do
				local inc = 1.5 * i
				local holepos = TransformToParentPoint(eye, Vec(0, 0, -inc))
				MakeHole(holepos, 2, 1.75, 1.5)
				local hit = QueryClosestPoint(holepos, 1.75)
				if hit then
					d.playsound = true
				end
			end

			if not d.spinsmash then
				local holepos4 = TransformToParentPoint(eye, Vec(0, 1.5, -1.5))
				local holepos5 = TransformToParentPoint(eye, Vec(0, 1, -2.5))
				MakeHole(holepos4, 2, 1.75, 1.5)
				MakeHole(holepos5, 2, 1.75, 1.5)
			end
			d.smashTimer = 0

			if d.spinsmash and d.soundtimer > 0 then
				d.soundtimer = d.soundtimer - dt
				if d.soundtimer < 0.0001 then
					d.soundtimer = 0
				end
			end
		end
	end
end

---------- CLIENT ----------

function client.init()
	clangsound = LoadSound("MOD/snd/clang.ogg")
	spinsound = LoadLoop("MOD/snd/spinloop.ogg")
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
	if GetPlayerTool(p) ~= "dragonslayer" or GetPlayerVehicle(p) ~= 0 then return end

	if InputPressed("usetool", p) then
		if d.smashTimer == 0 then d.smashTimer = 0.1 end
	end

	if InputDown("alttool", p) then
		-- Spin camera effect (local player only)
		if p == GetLocalPlayer() then
			local ct = GetPlayerEyeTransform(p)
			local pt = GetPlayerTransform(p)
			pt.pos[2] = pt.pos[2] + 1.8
			ct.pos = pt.pos
			ct.rot = QuatRotateQuat(ct.rot, QuatEuler(0, 10, 0))
			SetCameraTransform(ct)
		end

		if d.smashTimer == 0 then d.smashTimer = 0.05 end
		if d.soundtimer == 0 then d.soundtimer = 0.05 end
		PlayLoop(spinsound)
		d.spinsmash = true
	else
		d.spinsmash = false
	end

	-- Tool animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local offset = Transform(Vec(0.05, -0.55, 0), QuatEuler(80, -15, 0))
		SetToolTransform(offset, 1.0, p)

		if d.smashTimer > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, -d.smashTimer * 3)
			t.rot = QuatEuler(-d.smashTimer * 50, d.smashTimer * 100, 0)
			SetToolTransform(t, 1.0, p)
		end
	end

	if d.smashTimer > 0 then
		d.smashTimer = d.smashTimer - dt
		if d.smashTimer < 0.0001 then
			d.playsound = false
			local eye = GetPlayerEyeTransform(p)
			for i = 1, 3 do
				local inc = 1.5 * i
				local holepos = TransformToParentPoint(eye, Vec(0, 0, -inc))
				local hit = QueryClosestPoint(holepos, 1.75)
				if hit then
					d.playsound = true
				end
			end
			local soundpos = TransformToParentPoint(eye, Vec(0, 0, -3))

			if not d.spinsmash then
				if d.playsound then PlaySound(clangsound, soundpos, 0.65) end
			end
			d.smashTimer = 0

			if d.spinsmash and d.soundtimer > 0 then
				d.soundtimer = d.soundtimer - dt
				if d.soundtimer < 0.0001 then
					if d.playsound then PlaySound(clangsound, soundpos, 0.65) end
					d.soundtimer = 0
				end
			end
		end
	end
end

---------- HUD ----------

function draw()
	local p = GetLocalPlayer()
	if not p or not players[p] then return end
end
