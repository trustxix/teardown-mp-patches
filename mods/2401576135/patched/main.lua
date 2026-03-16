-- Magic Bag by My Cresta - v2 Multiplayer Patch

#version 2

#include "script/include/player.lua"

players = {}

function createPlayerData()
	return {
		items = {},
		count = 1,
		velocity = 0.5,
		rottimer = 0,
		swingTimer = 0,
		pickTimer = 0,
		charging = false,
	}
end

function GetAimPos(p)
	local ct = GetPlayerEyeTransform(p)
	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
	local direction = VecSub(forwardPos, ct.pos)
	local distance = VecLength(direction)
	direction = VecNormalize(direction)
	local hit, hitDistance, normal, shape = QueryRaycast(ct.pos, direction, distance)
	if hit then
		forwardPos = TransformToParentPoint(ct, Vec(0, 0, -hitDistance))
	end
	return hit, shape
end

function PickItem(p, data)
	local ct = GetPlayerEyeTransform(p)
	local hit, shape = GetAimPos(p)

	if hit then
		local body = GetShapeBody(shape)
		local vehicle = GetBodyVehicle(body)

		if not body then return end

		local min, max = GetBodyBounds(body)
		local bounds = VecSub(max, min)
		local volume = math.abs(bounds[1] * bounds[2] * bounds[3])
		if volume > 64000 then return end

		local joints = GetShapeJoints(shape)
		for i = 1, #joints do
			Delete(joints[i])
		end

		local diff = (shape - body) ~= 1

		if diff and vehicle == 0 then
			local shaperot = GetShapeLocalTransform(shape).rot
			local transform = Transform(Vec(0, 0, 0), shaperot)
			SetShapeLocalTransform(shape, transform)
		end

		local hidevec = Vec(0, -200 - (#data.items * 5), 0)
		local hidepos = TransformToParentVec(ct, hidevec)
		local bodyrot = GetBodyTransform(body).rot

		SetBodyTransform(body, Transform(hidepos, Quat()))
		SetTag(body, "unbreakable")
		data.items[data.count] = {}
		data.items[data.count].body = body
		data.items[data.count].rot = bodyrot
		data.count = data.count + 1
	end
end

function ThrowItem(p, data)
	if data.count < 2 then return end

	local ct = GetPlayerEyeTransform(p)
	local startpos = TransformToParentPoint(ct, Vec(0, 0, -3))
	local fwdpos = TransformToParentPoint(ct, Vec(0, 0, -4))
	local direction = VecSub(fwdpos, startpos)
	direction = VecScale(direction, data.velocity)
	local body = data.items[data.count - 1].body

	SetBodyTransform(body, Transform(startpos, data.items[data.count - 1].rot))
	RemoveTag(body, "unbreakable")
	SetBodyDynamic(body, true)
	SetBodyVelocity(body, direction)
	data.count = data.count - 1
	data.rottimer = 0.15
end

---------- SERVER ----------

function server.init()
	RegisterTool("magicbag", "Magic Bag", "MOD/vox/magicbag.vox")
end

function server.tick(dt)
	for p in PlayersAdded() do
		players[p] = createPlayerData()
		SetToolEnabled("magicbag", true, p)
	end

	for p in PlayersRemoved() do
		players[p] = nil
	end

	for p in Players() do
		server.tickPlayer(p, dt)
	end
end

function server.tickPlayer(p, dt)
	if GetPlayerTool(p) ~= "magicbag" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	if not data then return end

	-- Pick item (server authoritative: SetBodyTransform, SetTag, Delete joints)
	if InputPressed("usetool", p) then
		PickItem(p, data)
		data.pickTimer = 0.1
	end

	-- Charge throw
	if InputDown("alttool", p) then
		if data.count < 2 or data.rottimer > 0 then return end
		data.charging = true
	end

	-- Release throw (server authoritative: SetBodyVelocity, SetBodyTransform)
	if InputReleased("alttool", p) then
		if data.count < 2 or data.rottimer > 0 then
			data.charging = false
			return
		end
		ThrowItem(p, data)
		data.charging = false
		data.velocity = 1
		data.swingTimer = 0.2
	end

	if data.charging then
		data.velocity = math.min(data.velocity + (dt * 50), 50)
	end

	-- Post-throw rotation control
	if data.rottimer > 0 then
		data.rottimer = data.rottimer - dt
		if data.rottimer <= 0 then
			data.rottimer = 0
		end
	end
end

---------- CLIENT ----------

function client.init()
	throwsound = LoadSound("MOD/snd/throw.ogg")
	picksound = LoadSound("tool_pickup.ogg")
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
	if GetPlayerTool(p) ~= "magicbag" then return end
	if GetPlayerVehicle(p) ~= 0 then return end

	local data = players[p]
	if not data then return end
	local pt = GetPlayerTransform(p)

	-- Mirror pick
	if InputPressed("usetool", p) then
		PlaySound(picksound, pt.pos, 0.5)
		data.pickTimer = 0.1
	end

	-- Mirror charge
	if InputDown("alttool", p) then
		if data.count >= 2 and data.rottimer <= 0 then
			data.charging = true
		end
	end

	-- Mirror throw release
	if InputReleased("alttool", p) then
		if data.charging and data.count >= 2 then
			PlaySound(throwsound, pt.pos, 0.5)
			data.swingTimer = 0.2
		end
		data.charging = false
		data.velocity = 1
	end

	if data.charging then
		data.velocity = math.min(data.velocity + (dt * 50), 50)
	end

	-- Tool animation
	local b = GetToolBody(p)
	if b ~= 0 then
		local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
		SetToolTransform(offset, 1.0, p)

		if data.swingTimer > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, -data.swingTimer * 2)
			t.rot = QuatEuler(data.swingTimer * 30, 0, 0)
			SetToolTransform(t, 1.0, p)
			data.swingTimer = data.swingTimer - dt
		end

		if data.pickTimer > 0 then
			local t = Transform()
			t.pos = Vec(0, 0, data.pickTimer)
			t.rot = QuatEuler(data.pickTimer * 20, 0, 0)
			SetToolTransform(t, 1.0, p)
			data.pickTimer = data.pickTimer - dt
		end
	end

	if data.rottimer > 0 then
		data.rottimer = data.rottimer - dt
		if data.rottimer <= 0 then
			data.rottimer = 0
		end
	end
end

---------- HUD ----------

function draw()
	local p = GetLocalPlayer()
	if not p then return end
	local data = players[p]
	if not data then return end

	if GetPlayerTool(p) == "magicbag" and GetPlayerVehicle(p) == 0 then
		UiPush()
		UiTranslate(UiCenter(), UiHeight() - 60)
		UiAlign("center middle")
		UiColor(1, 1, 1)
		UiFont("bold.ttf", 32)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText(data.count - 1)
		UiPop()

		UiPush()
		UiTranslate(UiCenter() - 30, UiHeight() - 110)
		UiColor(1, 1, 1)
		UiFont("regular.ttf", 24)
		UiTextOutline(0, 0, 0, 1, 0.1)
		UiText("POWER")

		UiTranslate(-45, 10)
		UiColor(0, 0, 0, 0.5)
		local width = 150
		UiImageBox("ui/common/box-solid-10.png", width, 20, 6, 6)
		if data.velocity > 1 then
			UiTranslate(2, 2)
			width = (width - 4) * (data.velocity / 50)
			UiColor(0.5, 1, 0.5)
			UiImageBox("ui/common/box-solid-6.png", width, 16, 6, 6)
		end
		UiPop()
	end
end
