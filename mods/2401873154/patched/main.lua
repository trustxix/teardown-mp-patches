#version 2
#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		swingTimer = 0,
		fuseTime = 5,
		shellNum = 1,
		shells = createShellPool(),
	}
end

function createShellPool()
	local pool = {}
	for i = 1, 250 do
		pool[i] = {
			active = false,
			grenadeTimer = 0,
			boomTimer = 0,
			bounces = 0,
			grenadepos = Vec(0, 0, 0),
			predictedBulletVelocity = Vec(0, 0, 0),
			gravity = Vec(0, -160, 0),
		}
	end
	return pool
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

---------- SHARED PROJECTILE PHYSICS ----------

function ShellPhysicsStep(shell, dt, bounceSoundFunc)
	shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity, VecScale(shell.gravity, dt / 4))
	local point2 = VecAdd(shell.grenadepos, VecScale(shell.predictedBulletVelocity, dt / 4))
	local dir = VecNormalize(VecSub(point2, shell.grenadepos))
	local distance = VecLength(VecSub(point2, shell.grenadepos))
	local hit, dist, normal = QueryRaycast(shell.grenadepos, dir, distance)
	if hit then
		if shell.bounces == 30 then
			shell.gravity = Vec(0, 0, 0)
			shell.predictedBulletVelocity = Vec(0, 0, 0)
		else
			if shell.bounces < 10 and bounceSoundFunc then
				bounceSoundFunc(shell.grenadepos)
			end
			local dot = VecDot(normal, shell.predictedBulletVelocity)
			shell.predictedBulletVelocity = VecSub(shell.predictedBulletVelocity, VecScale(normal, dot * 1.4))
			shell.bounces = shell.bounces + 1
		end
	else
		shell.grenadepos = point2
	end
end

function ShootGrenade(p, d)
	local eye = GetPlayerEyeTransform(p)
	local fwdpos = TransformToParentPoint(eye, Vec(0, 0, -2))
	local gunpos = TransformToParentPoint(eye, Vec(0, 0, -1))
	local direction = VecSub(fwdpos, gunpos)
	d.swingTimer = 0.125

	local shell = d.shells[d.shellNum]
	shell.active = true
	shell.grenadepos = deepcopy(gunpos)
	shell.predictedBulletVelocity = VecScale(direction, 100)
	shell.grenadeTimer = d.fuseTime
	shell.boomTimer = 0
	shell.bounces = 0
	shell.gravity = Vec(0, -160, 0)

	d.shellNum = (d.shellNum % #d.shells) + 1
end

---------- SERVER ----------

function server.init()
	RegisterTool("holygrenade", "Holy Grenade", "MOD/vox/holygrenade.vox")
end

function server.tick(dt)
	for _, p in ipairs(PlayersAdded()) do
		players[p] = createPlayerData()
		SetToolEnabled(p, "holygrenade", true)
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

	if GetPlayerTool(p) == "holygrenade" and GetPlayerVehicle(p) == 0 then
		if InputPressed("usetool", p) then
			ShootGrenade(p, d)
		end

		if InputPressed("X", p) then
			d.fuseTime = math.min(20, d.fuseTime + 1)
		elseif InputPressed("Z", p) then
			d.fuseTime = math.max(1, d.fuseTime - 1)
		end
	end

	-- Process all shells (grenade physics, fuse, explosion)
	for _, shell in ipairs(d.shells) do
		if shell.grenadeTimer > 0 then
			shell.grenadeTimer = shell.grenadeTimer - dt
			if shell.grenadeTimer < 0.1 then
				shell.grenadeTimer = 0
				shell.boomTimer = 1.4
			end
		end

		if shell.boomTimer > 0 then
			shell.boomTimer = shell.boomTimer - dt
			if shell.boomTimer < 0.1 then
				shell.boomTimer = 0
				shell.active = false
				Explosion(shell.grenadepos, 10)
			end
		end

		if shell.active then
			ShellPhysicsStep(shell, dt, nil)
		end
	end
end

---------- CLIENT ----------

function client.init()
	holygrenadethrowsound = LoadSound("MOD/snd/throw.ogg")
	holygrenadebouncesound = LoadSound("MOD/snd/holybounce.ogg")
	holygrenadehallesound = LoadSound("MOD/snd/hallelujah.ogg")
	holygrenadeboomsound = LoadSound("MOD/snd/holyboom.ogg")
	holygrenadesprite = LoadSprite("MOD/img/holygren.png")
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

	if GetPlayerTool(p) == "holygrenade" and GetPlayerVehicle(p) == 0 then
		if InputPressed("usetool", p) then
			ShootGrenade(p, d)
			PlaySound(holygrenadethrowsound, GetPlayerEyeTransform(p).pos, 1, false)
		end

		if InputPressed("X", p) then
			d.fuseTime = math.min(20, d.fuseTime + 1)
		elseif InputPressed("Z", p) then
			d.fuseTime = math.max(1, d.fuseTime - 1)
		end

		-- Tool throw animation
		local b = GetToolBody(p)
		if b ~= 0 then
			local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
			SetToolTransform(offset, 1.0, p)

			if d.swingTimer > 0 then
				local t = Transform()
				t.pos = Vec(0, 0, d.swingTimer * 2)
				t.rot = QuatEuler(d.swingTimer * 50, 0, 0)
				SetToolTransform(t, 1.0, p)
				d.swingTimer = d.swingTimer - dt
			end
		end
	end

	-- Process all shells (mirrored physics, sounds, visuals)
	for _, shell in ipairs(d.shells) do
		if shell.grenadeTimer > 0 then
			shell.grenadeTimer = shell.grenadeTimer - dt
			if shell.grenadeTimer < 0.1 then
				shell.grenadeTimer = 0
				PlaySound(holygrenadehallesound, shell.grenadepos, 1, false)
				shell.boomTimer = 1.4
			end
		end

		if shell.boomTimer > 0 then
			shell.boomTimer = shell.boomTimer - dt
			if shell.boomTimer < 0.1 then
				shell.boomTimer = 0
				shell.active = false
				PlaySound(holygrenadeboomsound, shell.grenadepos, 1)
			end
		end

		if shell.active then
			ShellPhysicsStep(shell, dt, function(pos)
				PlaySound(holygrenadebouncesound, pos, 1, false)
			end)

			local camPos = GetPlayerEyeTransform(p).pos
			local rot = QuatLookAt(shell.grenadepos, camPos)
			local transform = Transform(shell.grenadepos, rot)
			DrawSprite(holygrenadesprite, transform, 0.4, 0.4, 0.5, 0.5, 0.5, 1, true, false)
		end
	end
end

---------- HUD ----------

function draw()
	local p = GetLocalPlayer()
	if not p or not players[p] then return end
	local d = players[p]
	UiAlign("center middle")
	UiTranslate(UiCenter(), UiHeight() - 80)
	UiColor(1, 1, 1, 0.8)
	UiFont("bold.ttf", 24)
	if GetPlayerTool(p) == "holygrenade" and GetPlayerVehicle(p) == 0 then
		UiText("Fuse: " .. d.fuseTime .. "s  [X]+  [Z]-")
	end
end
