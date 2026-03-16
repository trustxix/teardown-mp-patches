#version 2
#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		charging = false,
		bullets = 0,
		recoilTimer = 0,
		shellNum = 1,
		shells = {},
		toolPos = Vec(0, 0, 0),
		toolTrans = Transform(),
	}
end

function initShells(pd)
	for i = 1, 900 do
		pd.shells[i] = {
			active = false,
			pos = Vec(0, 0, 0),
			damage = 0,
			predictedBulletVelocity = Vec(0, 0, 0),
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

function rnd(mi, ma)
	local v = math.random(0, 1000) / 1000
	return mi + (ma - mi) * v
end

function getPerpendicular(dir)
	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
	return perp
end

local GRAVITY = Vec(0, 0, 0)
local VELOCITY = 50

----------------------------------------------------------------------
-- SERVER
----------------------------------------------------------------------

function server.init()
	RegisterTool("cresta-chargeshotgun", "Charge Shotgun", "MOD/vox/chargeshotgun.vox")
end

function server.tick(dt)
	-- Phase 1: PlayersAdded
	for _, p in ipairs(PlayersAdded()) do
		players[p] = createPlayerData()
		initShells(players[p])
		SetToolEnabled(p, "cresta-chargeshotgun", true)
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
	if GetPlayerTool(p) ~= "cresta-chargeshotgun" then
		pd.charging = false
		return
	end

	-- Charge accumulation
	if InputDown("usetool", p) then
		pd.charging = true
		pd.bullets = math.min(pd.bullets + (dt * 500), 900)
	end

	-- Fire on release
	if pd.charging and not InputDown("usetool", p) then
		-- Recoil
		local ct = GetPlayerEyeTransform(p)
		local recoildir = TransformToParentVec(ct, Vec(0, 0, pd.bullets / 30))
		local vel = GetPlayerVelocity(p)
		vel = VecAdd(vel, recoildir)
		SetPlayerVelocity(vel, p)
		pd.recoilTimer = math.max(0.10, pd.bullets / 1800)

		-- Spawn projectiles (server authoritative)
		local b = GetToolBody(p)
		if b ~= 0 then
			local toolTrans = GetBodyTransform(b)
			local toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -2))
			local fwdpos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -3))

			for i = 1, math.floor(pd.bullets) do
				local dir = VecSub(fwdpos, toolPos)
				local wspread = 0.15
				if pd.bullets < 200 then wspread = 0.05 end
				if pd.bullets > 600 then wspread = 0.20 end

				local perp = getPerpendicular(dir)
				local spread = wspread * rnd(0.0, 1.0)
				dir = VecNormalize(VecAdd(dir, VecScale(perp, spread)))

				local damage = rnd(2.5, 5)

				pd.shells[pd.shellNum] = {
					active = true,
					pos = VecCopy(toolPos),
					damage = damage / 10,
					predictedBulletVelocity = VecScale(dir, VELOCITY),
				}
				pd.shellNum = (pd.shellNum % 900) + 1
			end
		end

		pd.bullets = 0
		pd.charging = false
	end

	-- Update projectiles (server: damage)
	for _, shell in ipairs(pd.shells) do
		if shell.active then
			shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(GRAVITY, dt))
			local point2 = VecAdd(shell.pos, VecScale(shell.predictedBulletVelocity, dt))
			local dir = VecNormalize(VecSub(point2, shell.pos))
			local dist_to_next = VecLength(VecSub(point2, shell.pos))
			local hit, dist = QueryRaycast(shell.pos, dir, dist_to_next)

			if hit then
				local hitPos = VecAdd(shell.pos, VecScale(dir, dist))
				shell.active = false
				MakeHole(hitPos, shell.damage, shell.damage * 0.75, shell.damage * 0.5)
			end

			shell.pos = point2
		end
	end
end

----------------------------------------------------------------------
-- CLIENT
----------------------------------------------------------------------

local gunsound
local chargesound

function client.init()
	gunsound = LoadSound("MOD/snd/blast.ogg")
	chargesound = LoadLoop("MOD/snd/chargeloop.ogg")
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
	if GetPlayerTool(p) ~= "cresta-chargeshotgun" then
		pd.charging = false
		return
	end

	local b = GetToolBody(p)
	if b ~= 0 then
		local offset = Transform(Vec(0.05, 0.1, 0))
		SetToolTransform(offset, 1.0, p)
		pd.toolTrans = GetBodyTransform(b)
		pd.toolPos = TransformToParentPoint(pd.toolTrans, Vec(0.3, -0.5, -2))

		-- Emissive glow while charging
		local shapes = GetBodyShapes(b)
		for i = 1, #shapes do
			if InputDown("usetool", p) then
				SetShapeEmissiveScale(shapes[i], 5)
			else
				SetShapeEmissiveScale(shapes[i], 0)
			end
		end

		-- Recoil animation
		if pd.recoilTimer > 0 then
			local t = Transform()
			t.pos = Vec(0, 0.2, pd.recoilTimer / 2)
			t.rot = QuatEuler(pd.recoilTimer * 70, 0, 0)
			SetToolTransform(t, 1.0, p)
			pd.recoilTimer = pd.recoilTimer - dt
		end
	end

	-- Charge accumulation (client mirrors for HUD)
	if InputDown("usetool", p) then
		pd.charging = true
		pd.bullets = math.min(pd.bullets + (dt * 500), 900)
		PlayLoop(chargesound, GetPlayerTransform(p).pos, 0.4)
	end

	-- Fire on release
	if pd.charging and not InputDown("usetool", p) then
		if b ~= 0 then
			PointLight(pd.toolPos, 1, 0.4, 1, 1)
		end
		PlaySound(gunsound, GetPlayerTransform(p).pos, 0.5)

		-- Client mirrors projectiles for visuals
		local toolPos = pd.toolPos
		local fwdpos = TransformToParentPoint(pd.toolTrans, Vec(0.3, -0.5, -3))

		for i = 1, math.floor(pd.bullets) do
			local dir = VecSub(fwdpos, toolPos)
			local wspread = 0.15
			if pd.bullets < 200 then wspread = 0.05 end
			if pd.bullets > 600 then wspread = 0.20 end

			local perp = getPerpendicular(dir)
			local spread = wspread * rnd(0.0, 1.0)
			dir = VecNormalize(VecAdd(dir, VecScale(perp, spread)))

			local damage = rnd(2.5, 5)

			pd.shells[pd.shellNum] = {
				active = true,
				pos = VecCopy(toolPos),
				damage = damage / 10,
				predictedBulletVelocity = VecScale(dir, VELOCITY),
			}
			pd.shellNum = (pd.shellNum % 900) + 1
		end

		pd.recoilTimer = math.max(0.10, pd.bullets / 1800)
		pd.bullets = 0
		pd.charging = false
	end

	-- Update projectiles (client: visuals only)
	for _, shell in ipairs(pd.shells) do
		if shell.active then
			shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(GRAVITY, dt))
			local point2 = VecAdd(shell.pos, VecScale(shell.predictedBulletVelocity, dt))
			local dir = VecNormalize(VecSub(point2, shell.pos))
			local dist_to_next = VecLength(VecSub(point2, shell.pos))
			local hit, dist = QueryRaycast(shell.pos, dir, dist_to_next)

			if hit then
				local hitPos = VecAdd(shell.pos, VecScale(dir, dist))
				shell.active = false
				SpawnParticle("smoke", hitPos, Vec(0, 1.0 + math.random(1, 5) * 0.1, 0), shell.damage, 1)
			else
				DrawLine(shell.pos, point2, 1, 0.4, 1)
			end

			shell.pos = point2
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
	if GetPlayerTool(p) ~= "cresta-chargeshotgun" then return end

	UiPush()
		UiTranslate(UiCenter(), UiHeight() - 60)
		UiAlign("center middle")
		UiColor(1, 1, 1)
		UiFont("bold.ttf", 32)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText(math.floor(pd.bullets))
	UiPop()
end
