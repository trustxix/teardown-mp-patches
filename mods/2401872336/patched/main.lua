-- Desert Eagle by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		damage = 1,
		velocity = 1.6,
		reloadTime = 0.9,
		shotDelay = 0.2,
		ammo = 7,
		mags = 6,
		reloading = false,
		shootTimer = 0,
		reloadTimer = 0,
		recoilTimer = 0,
		lightTimer = 0,
		toolPos = Vec(),
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

function ProjectileOperations(projectile, data)
	local gravity = Vec(0, 0, 0)
	projectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity, VecScale(gravity, GetTimeStep()))
	local point2 = VecAdd(projectile.pos, VecScale(projectile.predictedBulletVelocity, GetTimeStep()))
	local dir = VecNormalize(VecSub(point2, projectile.pos))
	local hit, dist = QueryRaycast(projectile.pos, dir, VecLength(VecSub(point2, projectile.pos)))

	if hit then
		local hitPos = VecAdd(projectile.pos, VecScale(VecNormalize(VecSub(point2, projectile.pos)), dist))
		projectile.active = false
		MakeHole(hitPos, data.damage, data.damage * 0.7, data.damage * 0.4)
		SpawnParticle("smoke", hitPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), data.damage, 1)
	else
		DrawLine(projectile.pos, point2)
	end
	projectile.pos = point2
end

---------- SERVER ----------

function server.init()
	RegisterTool("deagle", "Desert Eagle", "MOD/vox/deagle.vox", 3)
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("deagle", true, p)
		local data = players[p]
		for i = 1, 7 do
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
	if GetPlayerTool(p) ~= "deagle" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	local unlimitedammo = GetBool("savegame.mod.unlimitedammo")

	-- Process projectiles
	for key, shell in ipairs(data.projectileHandler.shells) do
		if shell.active then
			ProjectileOperations(shell, data)
		end
	end

	-- Shoot
	if InputPressed("usetool", p) then
		if not data.reloading then
			if data.shootTimer <= 0 and data.ammo > 0 then
				local aimpos, hit, distance = GetAimPos(p)
				if distance and distance > 0 then
					local b = GetToolBody(p)
					if b ~= 0 then
						local toolTrans = GetBodyTransform(b)
						data.toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.45, -2.4))

						local direction = VecSub(aimpos, data.toolPos)
						local handler = data.projectileHandler
						handler.shells[handler.shellNum] = deepcopy(handler.defaultShell)
						local loadedShell = handler.shells[handler.shellNum]
						loadedShell.active = true
						loadedShell.pos = data.toolPos
						loadedShell.predictedBulletVelocity = VecScale(direction, data.velocity * (100 / distance))
						handler.shellNum = (handler.shellNum % #handler.shells) + 1

						if not unlimitedammo then
							data.ammo = data.ammo - 1
						end
						data.shootTimer = data.shotDelay
						data.recoilTimer = data.shotDelay
						data.lightTimer = data.shotDelay / 4
					end
				end
			end
		end
	end

	-- Reload
	if not unlimitedammo then
		if data.ammo < 7 and data.mags > 1 and InputPressed("r", p) then
			if not data.reloading then
				data.reloading = true
				data.reloadTimer = data.reloadTime
				data.mags = data.mags - 1
			end
		end

		if data.reloading then
			data.reloadTimer = data.reloadTimer - dt
			if data.reloadTimer < 0 then
				data.ammo = 7
				data.reloadTimer = 0
				data.reloading = false
			end
		end
	end

	if data.shootTimer > 0 then
		data.shootTimer = data.shootTimer - dt
	end
end

---------- CLIENT ----------

function client.init()
	gunsound = LoadSound("MOD/snd/deagle_shot.ogg")
	cocksound = LoadSound("MOD/snd/pistolcock.ogg")
	reloadsound = LoadSound("MOD/snd/deagle_reload.ogg")
	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
	refillsound = LoadSound("MOD/snd/refill.ogg")
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
	if GetPlayerTool(p) ~= "deagle" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	if not data then return end
	local pt = GetPlayerTransform(p)
	local unlimitedammo = GetBool("savegame.mod.unlimitedammo")

	-- Shoot sound + effects
	if InputPressed("usetool", p) then
		if not data.reloading then
			if data.ammo > 0 and data.mags > 0 then
				PlaySound(gunsound, pt.pos, 0.9)
				local b = GetToolBody(p)
				if b ~= 0 then
					local toolTrans = GetBodyTransform(b)
					local toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.45, -2.4))
					SpawnParticle("fire", toolPos, Vec(0, 1.0 + math.random(1, 10) * 0.1, 0), 0.5, 0.1)
					SpawnParticle("darksmoke", toolPos, Vec(0, 1.0 + math.random(1, 5) * 0.1, 0), 0.4, 1.5)
				end
				if not unlimitedammo then
					data.ammo = data.ammo - 1
				end
				data.shootTimer = data.shotDelay
				data.recoilTimer = data.shotDelay
				data.lightTimer = data.shotDelay / 4
			else
				PlaySound(dryfiresound, pt.pos, 1)
			end
		end
	end

	-- Reload sound
	if not unlimitedammo then
		if data.ammo < 7 and data.mags > 1 and InputPressed("r", p) then
			if not data.reloading then
				data.reloading = true
				PlaySound(reloadsound, pt.pos, 0.6)
				data.reloadTimer = data.reloadTime
				data.mags = data.mags - 1
			end
		end

		if data.reloading then
			data.reloadTimer = data.reloadTimer - dt
			if data.reloadTimer < 0 then
				data.ammo = 7
				data.reloadTimer = 0
				PlaySound(cocksound, pt.pos)
				data.reloading = false
			end
		end
	end

	-- Tool transform and recoil animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local offset = Transform(Vec(0.1, 0.1, 0))
		SetToolTransform(offset, 1.0, p)

		if data.recoilTimer > 0 then
			local t = Transform()
			t.pos = Vec(0.1, 0.1, data.recoilTimer * 3)
			t.rot = QuatEuler(data.recoilTimer * 100, 0, 0)
			SetToolTransform(t, 1.0, p)
			data.recoilTimer = data.recoilTimer - dt
		end

		if data.lightTimer > 0 then
			local toolTrans = GetBodyTransform(b)
			local toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.45, -2.4))
			PointLight(toolPos, 1, 1, 1, 0.5)
			data.lightTimer = data.lightTimer - dt
		end
	end

	if data.shootTimer > 0 then
		data.shootTimer = data.shootTimer - dt
	end
end

function client.draw()
	local unlimitedammo = GetBool("savegame.mod.unlimitedammo")
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end

	if GetPlayerTool(p) == "deagle" and GetPlayerVehicle(p) == 0 and not unlimitedammo then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 60)
		UiAlign("center middle")
		UiColor(1, 1, 1)
		UiFont("bold.ttf", 32)
		UiTextOutline(0, 0, 0, 1, 0.1)
		if data.reloading then
			UiText("Reloading")
		else
			UiText(data.ammo .. "/" .. 7 * math.max(0, data.mags - 1))
		end
		UiPop()
	end
end
