# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,71 +1,24 @@
-function init()
-	local mode = 1 --mode(1 - scout, 0 - anti-human)  
-	
-	RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
-	SetBool("game.tool.odm.enabled", true)
-
-	HookSnd = {LoadSound("MOD/HookSnd1.ogg"), LoadSound("MOD/HookSnd2.ogg")}
-	GasSnd = {LoadSound("gas-s0.ogg")}
-	ShotgunShotSnd = {}
-	for i = 0, 6 do
-		ShotgunShotSnd[i+1] = LoadSound("tools/shotgun"..i..".ogg")
-	end
-	RocketShotSnd = {}
-	for i = 1, 5 do
-		RocketShotSnd[i] = LoadSound("tools/launcher"..i..".ogg")
-	end
-	
-	grapplepower = 0.5
-	lastuse = 0
-	power = 100
-	grapplepower_a = 0.5
-
-	lgp, lgb = nil, nil
-	gp, gb = nil, nil
-	cable_left, cable_right = nil, nil
-
-	SetInt("game.tool.odm.ammo", 100)
-
-	if mode == 0 then
-		Shot = function()
-			local ct = GetCameraTransform()
-			local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
-			PlaySound(RocketShotSnd[math.random(1, #RocketShotSnd)])
-    		Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "rocket", 1.5, 300)
-		end
-	else
-		Shot = function()
-			local ct = GetCameraTransform()
-    		local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
-    		PlaySound(ShotgunShotSnd[math.random(1, #ShotgunShotSnd)])
-			Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "shotgun", 1, 150)
-		end
-	end
-end
-
-
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
 
-
 function Stab()
-	if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity()[2] < 0 then
-		local playerPos = GetPlayerPos()
-		local vel = GetPlayerVelocity()
+	if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity(playerId)[2] < 0 then
+		local playerPos = GetPlayerPos(playerId)
+		local vel = GetPlayerVelocity(playerId)
 		local dirs = {Vec(1,0,0), Vec(0,0,1), Vec(-1,0,0), Vec(0,0,-1)}
 		
 		for _, dir in ipairs(dirs) do
 			local hit = QueryRaycast(playerPos, dir, 0.3, 0.2, false)
 			if hit then
-				SetPlayerVelocity(Vec(vel[1], 0, vel[3]))
+				SetPlayerVelocity(playerId, Vec(vel[1], 0, vel[3]))
 				break
 			end
 		end
 	end
 end
-
 
 function Move(dt, direction, powerCost)
 	if IsPlayerGrounded() == false then
@@ -76,10 +29,10 @@
 		else
 			ToDir = VecNormalize(VecCross(Vec(0, 1, 0), Forward))
 		end
-		SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(ToDir, 0.15)))
+		SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(ToDir, 0.15)))
 		PlaySound(GasSnd[math.random(1, #GasSnd)], 1)
 		for n = 1, 4 do
-			SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
+			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
 		end
 		lastuse = 0
 		power = math.max(0, power - dt * powerCost)
@@ -87,21 +40,20 @@
 end
 
 function MovingRight(dt) Move(dt, "right", 125) end
+
 function MovingLeft(dt) Move(dt, "left", 105) end
 
-
 function GasAcceleration(dt)
-	if not QueryRaycast(GetPlayerPos(), Vec(0,-1,0), 1.0, 0.2, false) then
+	if not QueryRaycast(GetPlayerPos(playerId), Vec(0,-1,0), 1.0, 0.2, false) then
 		for n = 1, 11 do
-			SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-		end
-		SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(), Vec(0,0,-1))), 1.3)))
+			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+		end
+		SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(), Vec(0,0,-1))), 1.3)))
 		PlaySound(GasSnd[math.random(1, #GasSnd)], 1)
 		lastuse = 0
 		power = math.max(0, power - dt * 105)
 	end
 end
-
 
 function update_cable(dt, cable_data, is_right, button_down)
 	if not cable_data or not button_down then return nil end
@@ -127,7 +79,6 @@
 	end
 end
 
-
 function draw_flying_cable(cable_data)
 	local start_pos = cable_data.start_pos
 	local end_pos = cable_data.end_pos
@@ -162,14 +113,12 @@
 	end
 end
 
-
 function draw_hooked_cable(cable_data)
 	local start_pos = cable_data.start_pos
 	local end_pos = cable_data.hit_pos or cable_data.end_pos
 	DrawLine(start_pos, end_pos, 0.0, 0.0, 0.0)
 	DrawLine(start_pos, end_pos, 0.2, 0.2, 0.2, 0.3)
 end
-
 
 function HandleGrapple(dt, is_right)
 	local button = is_right and "rmb" or "lmb"
@@ -239,15 +188,15 @@
 	
 	if point and down then
 		local ct = GetCameraTransform()
-		local playerPos = GetPlayerPos()
+		local playerPos = GetPlayerPos(playerId)
 		local grapplePoint = body and TransformToParentPoint(GetBodyTransform(body), point) or point
 		
 		local offset = VecSub(grapplePoint, playerPos)
 		if body then
-			SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(VecNormalize(offset), grapplepower_a * 0.75)))
+			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(VecNormalize(offset), grapplepower_a * 0.75)))
 			ApplyBodyImpulse(body, grapplePoint, VecScale(VecNormalize(offset), grapplepower_a * -250))
 		else
-			SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(VecNormalize(offset), grapplepower_a)))
+			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(VecNormalize(offset), grapplepower_a)))
 		end
 	elseif not down then
 		if is_right then
@@ -258,10 +207,9 @@
 	end
 end
 
-
 function RightString(dt) HandleGrapple(dt, true) end
+
 function LeftString(dt) HandleGrapple(dt, false) end
-
 
 function Power(dt)
 	if power == nil then
@@ -273,7 +221,7 @@
 	else
 		power = 100.0 
 	end
-end	
+end
 
 function validateVariables()
 	if grapplepower == nil then 
@@ -292,87 +240,6 @@
 		grapplepower_a = 0.5 
 	end
 end
-
-
-function tick(dt)
-	SetBool("game.player.show", true)
-	
-	if lastuse == nil then
-		lastuse = 0 
-	elseif lastuse < 0 then
-		lastuse = 0
-	elseif lastuse < 1 then
-		lastuse = lastuse + dt
-	else 
-		Power(dt)	
-	end	 
-	
-	validateVariables()
-	
-	local speed = VecLength(GetPlayerVelocity())
-	if speed > 25 then MakeHole(GetPlayerPos(), 1, 0.5, 0.125) end
-	if speed > 50 then MakeHole(GetPlayerPos(), 1.5, 0.75, 0.25) end
-	if speed > 100 then MakeHole(GetPlayerPos(), 2, 1.0, 0.5) end
-
-	if GetString("game.player.tool") == "odm" then
-		grapplepower_a = InputDown("space") and grapplepower or 0
-		
-		if InputPressed("uparrow") then grapplepower = grapplepower + 0.1 end
-		if InputPressed("downarrow") then grapplepower = grapplepower - 0.1 end
-		
-		if InputPressed("shift") and not IsPlayerGrounded() then Shot() end
-		
-		Stab()
-		
-		if InputDown("ctrl") and power > 0 then GasAcceleration(dt) end
-		
-		LeftString(dt)
-		RightString(dt)
-		
-		if InputDown("a") and power > 0 then MovingLeft(dt) end
-		if InputDown("d") and power > 0 then MovingRight(dt) end
-		
-		local t = Transform()
-		t.pos = Vec(0, -0.6, -0.3)
-		SetToolTransform(t)
-	end
-end
-
-
-function draw()
-	if GetString("game.player.tool") == "odm" then
-		UiPush()
-		
-		local spower = math.floor(math.max(power, 0) + 0.5) .. "%"
-		UiTranslate(UiCenter(), 1030)
-		UiAlign("center middle")
-		UiFont("bold.ttf", 40)
-		
-		for _, offset in ipairs({{0,0.5}, {0,-1}, {0.5,0.5}, {-1,0}, {0.5,0}}) do
-			UiColor(0,0,0)
-			UiTranslate(offset[1], offset[2])
-			UiText(spower)
-			UiTranslate(-offset[1], -offset[2])
-		end
-		
-		UiColor(1,1,1)
-		UiText(spower)
-		UiPop()
-		
-		UiPush()
-		UiTranslate(300, 100)
-		UiAlign("left top")
-		UiFont("bold.ttf", 40)
-		UiColor(0,0,0)
-		UiTranslate(3, 3)
-		UiText("Odm power: " .. tostring(grapplepower))
-		UiTranslate(-1, -1)
-		UiColor(1,1,1)
-		UiText("Odm power: " .. tostring(grapplepower))
-		UiPop()
-	end
-end
-
 
 function getRaycastBody()
 	local direction = TransformToParentVec(GetCameraTransform(), Vec(0, 0, -100))
@@ -380,7 +247,6 @@
 	return hit and shape and GetShapeBody(shape) or false
 end
 
-
 function getRaycast()
 	local direction = TransformToParentVec(GetCameraTransform(), Vec(0, 0, -100))
 	local dir_norm = VecNormalize(direction)
@@ -395,4 +261,125 @@
 		end
 	end
 	return false
-end+end
+
+function server.init()
+    local mode = 1 --mode(1 - scout, 0 - anti-human)  
+    RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
+    SetBool("game.tool.odm.enabled", true, true)
+    ShotgunShotSnd = {}
+    RocketShotSnd = {}
+    grapplepower = 0.5
+    lastuse = 0
+    power = 100
+    grapplepower_a = 0.5
+    lgp, lgb = nil, nil
+    gp, gb = nil, nil
+    cable_left, cable_right = nil, nil
+    SetInt("game.tool.odm.ammo", 100, true)
+    else
+    	Shot = function()
+    		local ct = GetCameraTransform()
+       		local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
+    		Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "shotgun", 1, 150)
+    	end
+    end
+end
+
+function server.tick(dt)
+    SetBool("game.player.show", true, true)
+    if lastuse == nil then
+    	lastuse = 0 
+    elseif lastuse < 0 then
+    	lastuse = 0
+    elseif lastuse < 1 then
+    	lastuse = lastuse + dt
+    else 
+    	Power(dt)	
+    end	 
+    validateVariables()
+    local speed = VecLength(GetPlayerVelocity(playerId))
+end
+
+function client.init()
+    HookSnd = {LoadSound("MOD/HookSnd1.ogg"), LoadSound("MOD/HookSnd2.ogg")}
+    GasSnd = {LoadSound("gas-s0.ogg")}
+    for i = 0, 6 do
+    	ShotgunShotSnd[i+1] = LoadSound("tools/shotgun"..i..".ogg")
+    end
+    for i = 1, 5 do
+    	RocketShotSnd[i] = LoadSound("tools/launcher"..i..".ogg")
+    end
+    if mode == 0 then
+    	Shot = function()
+    		local ct = GetCameraTransform()
+    		local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
+    		PlaySound(RocketShotSnd[math.random(1, #RocketShotSnd)])
+       		Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "rocket", 1.5, 300)
+    	end
+       		PlaySound(ShotgunShotSnd[math.random(1, #ShotgunShotSnd)])
+end
+
+function client.tick(dt)
+    if speed > 25 then MakeHole(GetPlayerPos(playerId), 1, 0.5, 0.125) end
+    if speed > 50 then MakeHole(GetPlayerPos(playerId), 1.5, 0.75, 0.25) end
+    if speed > 100 then MakeHole(GetPlayerPos(playerId), 2, 1.0, 0.5) end
+
+    if GetString("game.player.tool") == "odm" then
+    	grapplepower_a = InputDown("space") and grapplepower or 0
+
+    	if InputPressed("uparrow") then grapplepower = grapplepower + 0.1 end
+    	if InputPressed("downarrow") then grapplepower = grapplepower - 0.1 end
+
+    	if InputPressed("shift") and not IsPlayerGrounded() then Shot() end
+
+    	Stab()
+
+    	if InputDown("ctrl") and power ~= 0 then GasAcceleration(dt) end
+
+    	LeftString(dt)
+    	RightString(dt)
+
+    	if InputDown("a") and power ~= 0 then MovingLeft(dt) end
+    	if InputDown("d") and power ~= 0 then MovingRight(dt) end
+
+    	local t = Transform()
+    	t.pos = Vec(0, -0.6, -0.3)
+    	SetToolTransform(t)
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "odm" then
+    	UiPush()
+
+    	local spower = math.floor(math.max(power, 0) + 0.5) .. "%"
+    	UiTranslate(UiCenter(), 1030)
+    	UiAlign("center middle")
+    	UiFont("bold.ttf", 40)
+
+    	for _, offset in ipairs({{0,0.5}, {0,-1}, {0.5,0.5}, {-1,0}, {0.5,0}}) do
+    		UiColor(0,0,0)
+    		UiTranslate(offset[1], offset[2])
+    		UiText(spower)
+    		UiTranslate(-offset[1], -offset[2])
+    	end
+
+    	UiColor(1,1,1)
+    	UiText(spower)
+    	UiPop()
+
+    	UiPush()
+    	UiTranslate(300, 100)
+    	UiAlign("left top")
+    	UiFont("bold.ttf", 40)
+    	UiColor(0,0,0)
+    	UiTranslate(3, 3)
+    	UiText("Odm power: " .. tostring(grapplepower))
+    	UiTranslate(-1, -1)
+    	UiColor(1,1,1)
+    	UiText("Odm power: " .. tostring(grapplepower))
+    	UiPop()
+    end
+end
+

```

---

# Migration Report: Reservs\Reserve (2).lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Reservs\Reserve (2).lua
+++ patched/Reservs\Reserve (2).lua
@@ -1,253 +1,7 @@
-dofile("mode0")
-dofile("mode1")
-
-function init()
-	--Register tool and enable it
-	RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
-	SetBool("game.tool.odm.enabled", true)
-
-	HookSnd = {LoadSound("MOD/HookSnd1.ogg"),LoadSound("MOD/HoodSnd2.ogg")}
-	GasSnd = {LoadSound("gas-s0.ogg"),LoadSound("gas-s1.ogg")}
-    RocketShot = {LoadSound("tools/launcher1.ogg"),LoadSound("tools/launcher2.ogg"),LoadSound("tools/launcher3.ogg"),LoadSound("tools/launcher4.ogg"),LoadSound("tools/launcher5.ogg"),}
-	ShotgunShot = {LoadSound("tools/shotgun0.ogg"),LoadSound("tools/shotgun1.ogg"),LoadSound("tools/shotgun2.ogg"),LoadSound("tools/shotgun3.ogg"),LoadSound("tools/shotgun4.ogg"),LoadSound("tools/shotgun5.ogg"),LoadSound("tools/shotgun6.ogg")}
-
-	local file = io.open("config.txt", "r")
-	if file then
-		local skip = file:read()
-		mode = file:read("*number")
-    	file:close()
-	end
-
-	grapplepower = 0.5
-	lastuse = 0
-	power = 100
-	graplepower_a = 0.5
-
-	SetInt("game.tool.odm.ammo", 100)
-end
-
---Return a random vector of desired length
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
-end
-
-function tick(dt) --main function
-	SetBool("game.player.show", true)
-	if power < 0.0 then --power can not go negative
-		power = 0.0
-	end
-	if lastuse < 1 then
-		lastuse = lastuse + dt
-	else
-		if power < 100.0 then
-			power = power+dt*100.0
-		else
-			power = 100.0
-		end
-	end
-
-	local speed = VecLength(GetPlayerVelocity())--making holes when speeding
-	if speed > 25 then
-		MakeHole(GetPlayerPos(),1,0.5,0.125)
-	end
-	if speed > 50 then
-		MakeHole(GetPlayerPos(),1.5,0.75,0.25)
-	end
-	if speed > 100 then
-		MakeHole(GetPlayerPos(),2,1.0,0.5)
-	end
-
-
-	if GetString("game.player.tool") == "odm" then --if tool is selected than
-		if InputDown("space") then
-        	grapplepower_a = grapplepower
-		else
-			grapplepower_a =0
-		end	
-
-		if InputPressed("uparrow") then
-        	grapplepower = grapplepower + 0.1
-    	end
-
-		if InputPressed("downarrow") then
-        	grapplepower = grapplepower - 0.1
-    	end
-
-		if mode then 
-			RocketShot()
-		else
-			ShotgunShot()
-		end		
-
-		if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity()[2] < 0 then 
-			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(1,0,0), 0.3, 0.2, false)
-			if hit then
-				SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-			else
-				hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,0,1), 0.3, 0.2, false)
-				if hit then
-					SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-				else
-					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(-1,0,0), 0.3, 0.2, false)
-					if hit then
-						SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-					else
-						hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,0,-1), 0.3, 0.2, false)
-						if hit then
-							SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-						else
-							
-						end
-					end
-				end
-			end
-		end
-
-		if InputDown("ctrl") and power > 0.0 then --The smoke acceleration part
-			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,-1,0), 1.0, 0.2, false)
-			if not hit then
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				--SetPlayerVelocity(VecScale(VecNormalize(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1))), VecLength(GetPlayerVelocity())+1.0))
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1.3)))
-				PlaySound(GasSnd[math.random(1, #GasSnd)], 1)
-				lastuse = 0
-				power = power-dt*100.0
-			end
-		end
-
-		--Check if firing
-		if GetBool("game.player.canusetool") and InputPressed("rmb") then
-			PlaySound(HookSnd[math.random(1, #HookSnd)])
-			local ct = GetCameraTransform()
-			local p = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
-			if getRaycast() then
-				gp = getRaycast()
-				if IsBodyDynamic(getRaycastBody()) then
-					gb = getRaycastBody()
-					gp = TransformToLocalPoint(GetBodyTransform(gb),gp)
-					MakeHole(TransformToParentPoint(GetBodyTransform(gb),gp),0.3,0.2,0.1,false)
-				else
-					gb = false
-					MakeHole(gp,0.3,0.2,0.1,false)
-				end
-				SpawnParticle("smoke", gp, rndVec(0.3), 0.4, 0.9)
-				SpawnParticle("smoke", gp, rndVec(0.3), 0.5, 1.0)
-				SpawnParticle("smoke", gp, rndVec(0.3), 0.6, 1.1)
-			else
-				gp = false
-			end
-
-			SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
-		end
-
-
-		if GetBool("game.player.canusetool") and InputPressed("lmb") then--left string
-			PlaySound(HookSnd[math.random(1, #HookSnd)])
-			local ct = GetCameraTransform()
-			local p = TransformToParentPoint(ct, Vec(-0.55, -0.85, -1.2))
-			if getRaycast() then
-				lgp = getRaycast()
-				if IsBodyDynamic(getRaycastBody()) then--checkng if object can move(body)
-					lgb = getRaycastBody()
-					lgp = TransformToLocalPoint(GetBodyTransform(lgb),lgp)
-					MakeHole(TransformToParentPoint(GetBodyTransform(lgb),lgp),0.3,0.2,0.1,false)
-				else
-					lgb = false
-					MakeHole(lgp,0.3,0.2,0.1,false)
-				end
-				SpawnParticle("smoke", lgp, rndVec(0.3), 0.4, 0.9)
-				SpawnParticle("smoke", lgp, rndVec(0.3), 0.5, 1.0)
-				SpawnParticle("smoke", lgp, rndVec(0.3), 0.6, 1.1)
-			else
-				lgp = false
-			end
-
-			SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
-		end
-
-		if gp and GetBool("game.player.canusetool") and InputDown("rmb") then --right string
-
-			offset = VecSub(gp,GetPlayerPos())
-			if gb then
-				offset = VecSub(TransformToParentPoint(GetBodyTransform(gb),gp),GetPlayerPos())
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower_a*0.75)))
-				ApplyBodyImpulse(gb,TransformToParentPoint(GetBodyTransform(gb),gp),VecScale(VecNormalize(offset),grapplepower_a*-250))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(gb),gp), 0.2,0.2,0.2)
-			else
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower_a)))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), gp, 0.2,0.2,0.2)
-			end
-		end
-
-		if lgp and GetBool("game.player.canusetool") and InputDown("lmb") then
-
-			offset = VecSub(lgp,GetPlayerPos())
-			if lgb then
-				offset = VecSub(TransformToParentPoint(GetBodyTransform(lgb),lgp),GetPlayerPos())
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower_a*0.75)))
-				ApplyBodyImpulse(lgb,TransformToParentPoint(GetBodyTransform(lgb),lgp),VecScale(VecNormalize(offset),grapplepower_a*-250))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(lgb),lgp), 0.2,0.2,0.2)
-			else
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower_a)))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), lgp, 0.2,0.2,0.2)
-			end
-		end
-
-		
-		--Move tool a bit to the right and recoil
-		local t = Transform()
-		t.pos = Vec(0, -0.6, -0.3)
-		SetToolTransform(t)
-	end
-end
-
-function draw()-- output of %of gas
-	if GetString("game.player.tool") == "odm" then
-		UiPush()
-
-		spower = math.floor(math.max(power,0)+0.5).."%"
-		UiTranslate(UiCenter(), 1030)
-		UiAlign("center middle")
-		UiFont("bold.ttf", 40)
-		UiColor(0,0,0)
-		UiTranslate(0, 0.5)
-		UiText(spower)
-		UiTranslate(0, -1)
-		UiText(spower)
-		UiTranslate(0.5, 0.5)
-		UiText(spower)
-		UiTranslate(-1, 0)
-		UiText(spower)
-		UiTranslate(0.5, 0)
-		UiColor(1,1,1)
-		UiText(spower)
-
-		UiPop()
-
-		UiPush()
-
-		UiTranslate(300, 100)
-		UiAlign("left top")
-		UiFont("bold.ttf", 40)
-		UiColor(0, 0, 0)
-        UiTranslate(3, 3)
-        UiText("Odm power: " .. tostring(grapplepower))
-        UiTranslate(-1, -1)
-        UiColor(1, 1, 1)
-        UiText("Odm power: " .. tostring(grapplepower))		
-	end
 end
 
 function getRaycastBody() --searching for a body
@@ -274,4 +28,244 @@
         return point
     end
     return false
-end+end
+
+function server.init()
+    RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
+    SetBool("game.tool.odm.enabled", true, true)
+    local file = io.open("config.txt", "r")
+    if file then
+    	local skip = file:read()
+    	mode = file:read("*number")
+       	file:close()
+    end
+    grapplepower = 0.5
+    lastuse = 0
+    power = 100
+    graplepower_a = 0.5
+    SetInt("game.tool.odm.ammo", 100, true)
+end
+
+function server.tick(dt)
+    SetBool("game.player.show", true, true)
+    if power < 0.0 then --power can not go negative
+    	power = 0.0
+    end
+    if lastuse < 1 then
+    	lastuse = lastuse + dt
+    else
+    	if power < 100.0 then
+    		power = power+dt*100.0
+    	else
+    		power = 100.0
+    	end
+    end
+    local speed = VecLength(GetPlayerVelocity(playerId))--making holes when speeding
+    if speed > 25 then
+    	MakeHole(GetPlayerPos(playerId),1,0.5,0.125)
+    end
+    if speed > 50 then
+    	MakeHole(GetPlayerPos(playerId),1.5,0.75,0.25)
+    end
+    if speed > 100 then
+    	MakeHole(GetPlayerPos(playerId),2,1.0,0.5)
+    end
+end
+
+function client.init()
+    HookSnd = {LoadSound("MOD/HookSnd1.ogg"),LoadSound("MOD/HoodSnd2.ogg")}
+    GasSnd = {LoadSound("gas-s0.ogg"),LoadSound("gas-s1.ogg")}
+       RocketShot = {LoadSound("tools/launcher1.ogg"),LoadSound("tools/launcher2.ogg"),LoadSound("tools/launcher3.ogg"),LoadSound("tools/launcher4.ogg"),LoadSound("tools/launcher5.ogg"),}
+    ShotgunShot = {LoadSound("tools/shotgun0.ogg"),LoadSound("tools/shotgun1.ogg"),LoadSound("tools/shotgun2.ogg"),LoadSound("tools/shotgun3.ogg"),LoadSound("tools/shotgun4.ogg"),LoadSound("tools/shotgun5.ogg"),LoadSound("tools/shotgun6.ogg")}
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "odm" then --if tool is selected than
+    	if InputDown("space") then
+           	grapplepower_a = grapplepower
+    	else
+    		grapplepower_a =0
+    	end	
+
+    	if InputPressed("uparrow") then
+           	grapplepower = grapplepower + 0.1
+       	end
+
+    	if InputPressed("downarrow") then
+           	grapplepower = grapplepower - 0.1
+       	end
+
+    	if mode then 
+    		RocketShot()
+    	else
+    		ShotgunShot()
+    	end		
+
+    	if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity(playerId)[2] < 0 then 
+    		hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(1,0,0), 0.3, 0.2, false)
+    		if hit then
+    			SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    		else
+    			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,0,1), 0.3, 0.2, false)
+    			if hit then
+    				SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    			else
+    				hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(-1,0,0), 0.3, 0.2, false)
+    				if hit then
+    					SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    				else
+    					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,0,-1), 0.3, 0.2, false)
+    					if hit then
+    						SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    					else
+
+    					end
+    				end
+    			end
+    		end
+    	end
+
+    	if InputDown("ctrl") and power > 0.0 then --The smoke acceleration part
+    		hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,-1,0), 1.0, 0.2, false)
+    		if not hit then
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			--SetPlayerVelocity(playerId, VecScale(VecNormalize(VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1))), VecLength(GetPlayerVelocity(playerId))+1.0))
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1.3)))
+    			PlaySound(GasSnd[math.random(1, #GasSnd)], 1)
+    			lastuse = 0
+    			power = power-dt*100.0
+    		end
+    	end
+
+    	--Check if firing
+    	if GetBool("game.player.canusetool") and InputPressed("rmb") then
+    		PlaySound(HookSnd[math.random(1, #HookSnd)])
+    		local ct = GetCameraTransform()
+    		local p = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
+    		if getRaycast() then
+    			gp = getRaycast()
+    			if IsBodyDynamic(getRaycastBody()) then
+    				gb = getRaycastBody()
+    				gp = TransformToLocalPoint(GetBodyTransform(gb),gp)
+    				MakeHole(TransformToParentPoint(GetBodyTransform(gb),gp),0.3,0.2,0.1,false)
+    			else
+    				gb = false
+    				MakeHole(gp,0.3,0.2,0.1,false)
+    			end
+    			SpawnParticle("smoke", gp, rndVec(0.3), 0.4, 0.9)
+    			SpawnParticle("smoke", gp, rndVec(0.3), 0.5, 1.0)
+    			SpawnParticle("smoke", gp, rndVec(0.3), 0.6, 1.1)
+    		else
+    			gp = false
+    		end
+
+    		SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
+    	end
+
+    	if GetBool("game.player.canusetool") and InputPressed("lmb") then--left string
+    		PlaySound(HookSnd[math.random(1, #HookSnd)])
+    		local ct = GetCameraTransform()
+    		local p = TransformToParentPoint(ct, Vec(-0.55, -0.85, -1.2))
+    		if getRaycast() then
+    			lgp = getRaycast()
+    			if IsBodyDynamic(getRaycastBody()) then--checkng if object can move(body)
+    				lgb = getRaycastBody()
+    				lgp = TransformToLocalPoint(GetBodyTransform(lgb),lgp)
+    				MakeHole(TransformToParentPoint(GetBodyTransform(lgb),lgp),0.3,0.2,0.1,false)
+    			else
+    				lgb = false
+    				MakeHole(lgp,0.3,0.2,0.1,false)
+    			end
+    			SpawnParticle("smoke", lgp, rndVec(0.3), 0.4, 0.9)
+    			SpawnParticle("smoke", lgp, rndVec(0.3), 0.5, 1.0)
+    			SpawnParticle("smoke", lgp, rndVec(0.3), 0.6, 1.1)
+    		else
+    			lgp = false
+    		end
+
+    		SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
+    	end
+
+    	if gp and GetBool("game.player.canusetool") and InputDown("rmb") then --right string
+
+    		offset = VecSub(gp,GetPlayerPos(playerId))
+    		if gb then
+    			offset = VecSub(TransformToParentPoint(GetBodyTransform(gb),gp),GetPlayerPos(playerId))
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower_a*0.75)))
+    			ApplyBodyImpulse(gb,TransformToParentPoint(GetBodyTransform(gb),gp),VecScale(VecNormalize(offset),grapplepower_a*-250))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(gb),gp), 0.2,0.2,0.2)
+    		else
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower_a)))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), gp, 0.2,0.2,0.2)
+    		end
+    	end
+
+    	if lgp and GetBool("game.player.canusetool") and InputDown("lmb") then
+
+    		offset = VecSub(lgp,GetPlayerPos(playerId))
+    		if lgb then
+    			offset = VecSub(TransformToParentPoint(GetBodyTransform(lgb),lgp),GetPlayerPos(playerId))
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower_a*0.75)))
+    			ApplyBodyImpulse(lgb,TransformToParentPoint(GetBodyTransform(lgb),lgp),VecScale(VecNormalize(offset),grapplepower_a*-250))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(lgb),lgp), 0.2,0.2,0.2)
+    		else
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower_a)))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), lgp, 0.2,0.2,0.2)
+    		end
+    	end
+
+    	--Move tool a bit to the right and recoil
+    	local t = Transform()
+    	t.pos = Vec(0, -0.6, -0.3)
+    	SetToolTransform(t)
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "odm" then
+    	UiPush()
+
+    	spower = math.floor(math.max(power,0)+0.5).."%"
+    	UiTranslate(UiCenter(), 1030)
+    	UiAlign("center middle")
+    	UiFont("bold.ttf", 40)
+    	UiColor(0,0,0)
+    	UiTranslate(0, 0.5)
+    	UiText(spower)
+    	UiTranslate(0, -1)
+    	UiText(spower)
+    	UiTranslate(0.5, 0.5)
+    	UiText(spower)
+    	UiTranslate(-1, 0)
+    	UiText(spower)
+    	UiTranslate(0.5, 0)
+    	UiColor(1,1,1)
+    	UiText(spower)
+
+    	UiPop()
+
+    	UiPush()
+
+    	UiTranslate(300, 100)
+    	UiAlign("left top")
+    	UiFont("bold.ttf", 40)
+    	UiColor(0, 0, 0)
+           UiTranslate(3, 3)
+           UiText("Odm power: " .. tostring(grapplepower))
+           UiTranslate(-1, -1)
+           UiColor(1, 1, 1)
+           UiText("Odm power: " .. tostring(grapplepower))		
+    end
+end
+

```

---

# Migration Report: Reservs\Reserve.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Reservs\Reserve.lua
+++ patched/Reservs\Reserve.lua
@@ -1,208 +1,7 @@
-function init()
-	--Register tool and enable it
-	RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
-	SetBool("game.tool.odm.enabled", true)
-
-	shootSnd = {}
-	for i=0, 7 do
-		shootSnd[i] = LoadSound("tools/gun"..i..".ogg")
-	end
-	grapplepower = 0.5
-	lastuse = 0
-	power = 100
-	
-	SetInt("game.tool.odm.ammo", 100)
-end
-
---Return a random vector of desired length
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
-end
-
-function tick(dt)
-	if power < 0.0 then
-		power = 0.0
-	end
-	if lastuse < 1 then
-		lastuse = lastuse + dt
-	else
-		if power < 100.0 then
-			power = power+dt*100.0
-		else
-			power = 100.0
-		end
-	end
-	local speed = VecLength(GetPlayerVelocity())
-	if speed > 10 then
-		MakeHole(GetPlayerPos(),1,0.5,0.125)
-	end
-	if speed > 25 then
-		MakeHole(GetPlayerPos(),1.5,0.75,0.25)
-	end
-	if speed > 50 then
-		MakeHole(GetPlayerPos(),2,1.0,0.5)
-	end
-
-	if GetString("game.player.tool") == "odm" then
-
-		if InputDown("ctrl") then	
-			grapplepower = 0.1
-		else
-			grapplepower = 0.5
-		end
-		if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity()[2] < 0 then
-			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(1,0,0), 0.3, 0.2, false)
-			if hit then
-				SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-			else
-				hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,0,1), 0.3, 0.2, false)
-				if hit then
-					SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-				else
-					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(-1,0,0), 0.3, 0.2, false)
-					if hit then
-						SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-					else
-						hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,0,-1), 0.3, 0.2, false)
-						if hit then
-							SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
-						else
-							
-						end
-					end
-				end
-			end
-		end
-
-		if InputDown("space") and power > 0.0 then
-			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,-1,0), 1.0, 0.2, false)
-			if not hit then
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-				
-				--SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),2.0)))
-				SetPlayerVelocity(VecScale(VecNormalize(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1))), VecLength(GetPlayerVelocity())+1.0))
-				lastuse = 0
-				power = power-dt*200.0
-			end
-		end
-
-		--Check if firing
-		if GetBool("game.player.canusetool") and InputPressed("rmb") then
-			local ct = GetCameraTransform()
-			local p = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
-			if getRaycast() then
-				gp = getRaycast()
-				if IsBodyDynamic(getRaycastBody()) then
-					gb = getRaycastBody()
-					gp = TransformToLocalPoint(GetBodyTransform(gb),gp)
-					MakeHole(TransformToParentPoint(GetBodyTransform(gb),gp),0.3,0.2,0.1,false)
-				else
-					gb = false
-					MakeHole(gp,0.3,0.2,0.1,false)
-				end
-				SpawnParticle("smoke", gp, rndVec(0.3), 0.4, 0.9)
-				SpawnParticle("smoke", gp, rndVec(0.3), 0.5, 1.0)
-				SpawnParticle("smoke", gp, rndVec(0.3), 0.6, 1.1)
-			else
-				gp = false
-			end
-
-			SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
-			PlaySound(shootSnd[math.random(0,#shootSnd)])
-		end
-
-
-		if GetBool("game.player.canusetool") and InputPressed("lmb") then
-
-			local ct = GetCameraTransform()
-			local p = TransformToParentPoint(ct, Vec(-0.55, -0.85, -1.2))
-			if getRaycast() then
-				lgp = getRaycast()
-				if IsBodyDynamic(getRaycastBody()) then
-					lgb = getRaycastBody()
-					lgp = TransformToLocalPoint(GetBodyTransform(lgb),lgp)
-					MakeHole(TransformToParentPoint(GetBodyTransform(lgb),lgp),0.3,0.2,0.1,false)
-				else
-					lgb = false
-					MakeHole(lgp,0.3,0.2,0.1,false)
-				end
-				SpawnParticle("smoke", lgp, rndVec(0.3), 0.4, 0.9)
-				SpawnParticle("smoke", lgp, rndVec(0.3), 0.5, 1.0)
-				SpawnParticle("smoke", lgp, rndVec(0.3), 0.6, 1.1)
-			else
-				lgp = false
-			end
-
-			SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
-			PlaySound(shootSnd[math.random(0,#shootSnd)])
-		end
-
-		if gp and GetBool("game.player.canusetool") and InputDown("rmb") then
-
-			offset = VecSub(gp,GetPlayerPos())
-			if gb then
-				offset = VecSub(TransformToParentPoint(GetBodyTransform(gb),gp),GetPlayerPos())
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower*0.75)))
-				ApplyBodyImpulse(gb,TransformToParentPoint(GetBodyTransform(gb),gp),VecScale(VecNormalize(offset),grapplepower*-250))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(gb),gp), 0.2,0.2,0.2)
-			else
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower)))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), gp, 0.2,0.2,0.2)
-			end
-		end
-		if lgp and GetBool("game.player.canusetool") and InputDown("lmb") then
-
-			offset = VecSub(lgp,GetPlayerPos())
-			if lgb then
-				offset = VecSub(TransformToParentPoint(GetBodyTransform(lgb),lgp),GetPlayerPos())
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower*0.75)))
-				ApplyBodyImpulse(lgb,TransformToParentPoint(GetBodyTransform(lgb),lgp),VecScale(VecNormalize(offset),grapplepower*-250))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(lgb),lgp), 0.2,0.2,0.2)
-			else
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower)))
-				DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), lgp, 0.2,0.2,0.2)
-			end
-		end
-
-		
-		--Move tool a bit to the right and recoil
-		local t = Transform()
-		t.pos = Vec(0, -0.6, -0.3)
-		SetToolTransform(t)
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "odm" then
-		spower = math.floor(math.max(power,0)+0.5).."%"
-		UiTranslate(UiCenter(), 1030)
-		UiAlign("center middle")
-		UiFont("bold.ttf", 40)
-		UiColor(0,0,0)
-		UiTranslate(0, 0.5)
-		UiText(spower)
-		UiTranslate(0, -1)
-		UiText(spower)
-		UiTranslate(0.5, 0.5)
-		UiText(spower)
-		UiTranslate(-1, 0)
-		UiText(spower)
-		UiTranslate(0.5, 0)
-		UiColor(1,1,1)
-		UiText(spower)
-	end
 end
 
 function getRaycastBody()
@@ -216,6 +15,7 @@
     end
     return false
 end
+
 function getRaycast()
     local direction = TransformToParentVec(GetCameraTransform(), Vec(0, 0, -100))
     local dist = VecLength(direction)
@@ -230,4 +30,204 @@
     return false
 end
 
-
+function server.init()
+    RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
+    SetBool("game.tool.odm.enabled", true, true)
+    shootSnd = {}
+    grapplepower = 0.5
+    lastuse = 0
+    power = 100
+    SetInt("game.tool.odm.ammo", 100, true)
+end
+
+function server.tick(dt)
+    if power < 0.0 then
+    	power = 0.0
+    end
+    if lastuse < 1 then
+    	lastuse = lastuse + dt
+    else
+    	if power < 100.0 then
+    		power = power+dt*100.0
+    	else
+    		power = 100.0
+    	end
+    end
+    local speed = VecLength(GetPlayerVelocity(playerId))
+    if speed > 10 then
+    	MakeHole(GetPlayerPos(playerId),1,0.5,0.125)
+    end
+    if speed > 25 then
+    	MakeHole(GetPlayerPos(playerId),1.5,0.75,0.25)
+    end
+    if speed > 50 then
+    	MakeHole(GetPlayerPos(playerId),2,1.0,0.5)
+    end
+end
+
+function client.init()
+    for i=0, 7 do
+    	shootSnd[i] = LoadSound("tools/gun"..i..".ogg")
+    end
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "odm" then
+
+    	if InputDown("ctrl") then	
+    		grapplepower = 0.1
+    	else
+    		grapplepower = 0.5
+    	end
+    	if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity(playerId)[2] < 0 then
+    		hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(1,0,0), 0.3, 0.2, false)
+    		if hit then
+    			SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    		else
+    			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,0,1), 0.3, 0.2, false)
+    			if hit then
+    				SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    			else
+    				hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(-1,0,0), 0.3, 0.2, false)
+    				if hit then
+    					SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    				else
+    					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,0,-1), 0.3, 0.2, false)
+    					if hit then
+    						SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
+    					else
+
+    					end
+    				end
+    			end
+    		end
+    	end
+
+    	if InputDown("space") and power > 0.0 then
+    		hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,-1,0), 1.0, 0.2, false)
+    		if not hit then
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+    			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+
+    			--SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),2.0)))
+    			SetPlayerVelocity(playerId, VecScale(VecNormalize(VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1))), VecLength(GetPlayerVelocity(playerId))+1.0))
+    			lastuse = 0
+    			power = power-dt*200.0
+    		end
+    	end
+
+    	--Check if firing
+    	if GetBool("game.player.canusetool") and InputPressed("rmb") then
+    		local ct = GetCameraTransform()
+    		local p = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
+    		if getRaycast() then
+    			gp = getRaycast()
+    			if IsBodyDynamic(getRaycastBody()) then
+    				gb = getRaycastBody()
+    				gp = TransformToLocalPoint(GetBodyTransform(gb),gp)
+    				MakeHole(TransformToParentPoint(GetBodyTransform(gb),gp),0.3,0.2,0.1,false)
+    			else
+    				gb = false
+    				MakeHole(gp,0.3,0.2,0.1,false)
+    			end
+    			SpawnParticle("smoke", gp, rndVec(0.3), 0.4, 0.9)
+    			SpawnParticle("smoke", gp, rndVec(0.3), 0.5, 1.0)
+    			SpawnParticle("smoke", gp, rndVec(0.3), 0.6, 1.1)
+    		else
+    			gp = false
+    		end
+
+    		SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
+    		PlaySound(shootSnd[math.random(0,#shootSnd)])
+    	end
+
+    	if GetBool("game.player.canusetool") and InputPressed("lmb") then
+
+    		local ct = GetCameraTransform()
+    		local p = TransformToParentPoint(ct, Vec(-0.55, -0.85, -1.2))
+    		if getRaycast() then
+    			lgp = getRaycast()
+    			if IsBodyDynamic(getRaycastBody()) then
+    				lgb = getRaycastBody()
+    				lgp = TransformToLocalPoint(GetBodyTransform(lgb),lgp)
+    				MakeHole(TransformToParentPoint(GetBodyTransform(lgb),lgp),0.3,0.2,0.1,false)
+    			else
+    				lgb = false
+    				MakeHole(lgp,0.3,0.2,0.1,false)
+    			end
+    			SpawnParticle("smoke", lgp, rndVec(0.3), 0.4, 0.9)
+    			SpawnParticle("smoke", lgp, rndVec(0.3), 0.5, 1.0)
+    			SpawnParticle("smoke", lgp, rndVec(0.3), 0.6, 1.1)
+    		else
+    			lgp = false
+    		end
+
+    		SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
+    		PlaySound(shootSnd[math.random(0,#shootSnd)])
+    	end
+
+    	if gp and GetBool("game.player.canusetool") and InputDown("rmb") then
+
+    		offset = VecSub(gp,GetPlayerPos(playerId))
+    		if gb then
+    			offset = VecSub(TransformToParentPoint(GetBodyTransform(gb),gp),GetPlayerPos(playerId))
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower*0.75)))
+    			ApplyBodyImpulse(gb,TransformToParentPoint(GetBodyTransform(gb),gp),VecScale(VecNormalize(offset),grapplepower*-250))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(gb),gp), 0.2,0.2,0.2)
+    		else
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower)))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -1.2)), gp, 0.2,0.2,0.2)
+    		end
+    	end
+    	if lgp and GetBool("game.player.canusetool") and InputDown("lmb") then
+
+    		offset = VecSub(lgp,GetPlayerPos(playerId))
+    		if lgb then
+    			offset = VecSub(TransformToParentPoint(GetBodyTransform(lgb),lgp),GetPlayerPos(playerId))
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower*0.75)))
+    			ApplyBodyImpulse(lgb,TransformToParentPoint(GetBodyTransform(lgb),lgp),VecScale(VecNormalize(offset),grapplepower*-250))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), TransformToParentPoint(GetBodyTransform(lgb),lgp), 0.2,0.2,0.2)
+    		else
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower)))
+    			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(-0.55, -0.85, -1.2)), lgp, 0.2,0.2,0.2)
+    		end
+    	end
+
+    	--Move tool a bit to the right and recoil
+    	local t = Transform()
+    	t.pos = Vec(0, -0.6, -0.3)
+    	SetToolTransform(t)
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "odm" then
+    	spower = math.floor(math.max(power,0)+0.5).."%"
+    	UiTranslate(UiCenter(), 1030)
+    	UiAlign("center middle")
+    	UiFont("bold.ttf", 40)
+    	UiColor(0,0,0)
+    	UiTranslate(0, 0.5)
+    	UiText(spower)
+    	UiTranslate(0, -1)
+    	UiText(spower)
+    	UiTranslate(0.5, 0.5)
+    	UiText(spower)
+    	UiTranslate(-1, 0)
+    	UiText(spower)
+    	UiTranslate(0.5, 0)
+    	UiColor(1,1,1)
+    	UiText(spower)
+    end
+end
+

```

---

# Migration Report: Reservs\Reserve3.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Reservs\Reserve3.lua
+++ patched/Reservs\Reserve3.lua
@@ -1,123 +1,74 @@
-function init()
-	local mode = 1 --mode(1 - scout, 0 - anti-human)  
-	
-	--Register tool and enable it
-	RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
-	SetBool("game.tool.odm.enabled", true)
-
-	HookSnd = {LoadSound("MOD/HookSnd1.ogg"),LoadSound("MOD/HookSnd2.ogg")}
-	GasSnd = {LoadSound("gas-s0.ogg"),LoadSound("gas-s1.ogg")}
-	ShotgunShotSnd = {LoadSound("tools/shotgun0.ogg"),LoadSound("tools/shotgun1.ogg"),LoadSound("tools/shotgun2.ogg"),LoadSound("tools/shotgun3.ogg"),LoadSound("tools/shotgun4.ogg"),LoadSound("tools/shotgun5.ogg"),LoadSound("tools/shotgun6.ogg")}
-	RocketShotSnd = {LoadSound("tools/launcher1.ogg"),LoadSound("tools/launcher2.ogg"),LoadSound("tools/launcher3.ogg"),LoadSound("tools/launcher4.ogg"),LoadSound("tools/launcher5.ogg"),}
-	
-	grapplepower = 0.5
-	lastuse = 0
-	power = 100
-	grapplepower_a = 0.5
-
-	lgp = nil
-	lgb = nil
-	gp = nil
-	gb = nil
-
-	SetInt("game.tool.odm.ammo", 100)
-
-	local mode = 1
-
-	if mode == 0 then
-		function Shot()
-			local ct = GetCameraTransform()
-			local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
-			PlaySound(RocketShotSnd[math.random(1, #RocketShotSnd)])
-    		Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "rocket", 1.5, 300 )
-		end	
-	else
-		function Shot()
-			local ct = GetCameraTransform()
-    		local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
-    		PlaySound(ShotgunShotSnd[math.random(1, #ShotgunShotSnd)])
-			Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "shotgun", 1, 150 )
-		end
-	end
-end
-
-
---Return a random vector of desired length
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
 
-
 function Stab()
-	if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity()[2] < 0 then 
-		hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(1,0,0), 0.3, 0.2, false)
+	if (not InputDown("rmb")) and (not InputDown("lmb")) and GetPlayerVelocity(playerId)[2] < 0 then 
+		hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(1,0,0), 0.3, 0.2, false)
 		if hit then
-				SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
+				SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
 		else
-			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,0,1), 0.3, 0.2, false)
+			hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,0,1), 0.3, 0.2, false)
 			if hit then
-					SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
+					SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
 			else
-					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(-1,0,0), 0.3, 0.2, false)
+					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(-1,0,0), 0.3, 0.2, false)
 				if hit then
-						SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
+						SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
 				else
-					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,0,-1), 0.3, 0.2, false)
+					hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,0,-1), 0.3, 0.2, false)
 					if hit then
-						SetPlayerVelocity(Vec(GetPlayerVelocity()[1],0,GetPlayerVelocity()[3]))
+						SetPlayerVelocity(playerId, Vec(GetPlayerVelocity(playerId)[1],0,GetPlayerVelocity(playerId)[3]))
 					end
 				end
 			end
 		end
 	end
 end
-
 
 function MovingRight(dt)
 	if IsPlayerGrounded() == false then
 		local Forward = VecNormalize(TransformToParentVec(GetCameraTransform(), Vec(0, 0, -1)))
 		local ToRight = VecNormalize(VecCross(Forward ,Vec(0, 1, 0)))
-		SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(ToRight,  0.15 )))
+		SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(ToRight,  0.15 )))
 		PlaySound(GasSnd[math.random(1, #GasSnd)], 1)
 		for n = 0 , 3 do
-			SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
+			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
 		end
 		lastuse = 0
 		power = math.max(0, power - dt * 125)
 	end
-end	
-
+end
 
 function MovingLeft(dt)
 	if IsPlayerGrounded() == false then
 		local Forward = VecNormalize(TransformToParentVec(GetCameraTransform(), Vec(0, 0, -1)))
 		local ToLeft = VecNormalize(VecCross(Vec(0, 1, 0) , Forward))
-		SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(ToLeft,  0.15 )))
+		SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(ToLeft,  0.15 )))
 		PlaySound(GasSnd[math.random(1, #GasSnd)], 1)
 		for n = 0 , 3 do
-			SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
+			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
 		end
 		lastuse = 0
 		power = math.max(0, power - dt * 105)
 	end
-end	
-
+end
 
 function GasAcceleration(dt)--The smoke acceleration part
-	hit, dist, normal, shape = QueryRaycast(GetPlayerPos(), Vec(0,-1,0), 1.0, 0.2, false)
+	hit, dist, normal, shape = QueryRaycast(GetPlayerPos(playerId), Vec(0,-1,0), 1.0, 0.2, false)
 	if not hit then
 		for n = 0 , 10 do
-			SpawnParticle("smoke", GetPlayerPos(), rndVec(0.5), 0.5, 3)
-		end
-		--SetPlayerVelocity(VecScale(VecNormalize(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1))), VecLength(GetPlayerVelocity())+1.0))
-		SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1.3)))
+			SpawnParticle("smoke", GetPlayerPos(playerId), rndVec(0.5), 0.5, 3)
+		end
+		--SetPlayerVelocity(playerId, VecScale(VecNormalize(VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1))), VecLength(GetPlayerVelocity(playerId))+1.0))
+		SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(TransformToParentVec(GetCameraTransform(),Vec(0,0,-1))),1.3)))
 		PlaySound(GasSnd[math.random(1, #GasSnd)], 1)
 		lastuse = 0
 		power = math.max(0, power - dt * 105)
 	end
-end	
-
+end
 
 function RightString()
 	if GetBool("game.player.canusetool") and InputPressed("rmb") then
@@ -142,21 +93,21 @@
 		end
 		SpawnParticle("fire", p, rndVec(0.1), 0.5, 0.9)
 
-		local offset = VecSub(gp,GetPlayerPos())
+		local offset = VecSub(gp,GetPlayerPos(playerId))
 		if gb then
-			offset = VecSub(TransformToParentPoint(GetBodyTransform(gb),gp),GetPlayerPos())
-			SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower_a*0.75)))
+			offset = VecSub(TransformToParentPoint(GetBodyTransform(gb),gp),GetPlayerPos(playerId))
+			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower_a*0.75)))
 			ApplyBodyImpulse(gb,TransformToParentPoint(GetBodyTransform(gb),gp),VecScale(VecNormalize(offset),grapplepower_a*-250))
 			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -0.4)), TransformToParentPoint(GetBodyTransform(gb),gp), 0.2,0.2,0.2)
 		else
-			SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(VecNormalize(offset),grapplepower_a)))
+			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(VecNormalize(offset),grapplepower_a)))
 			DrawLine(TransformToParentPoint(GetCameraTransform(), Vec(0.55, -0.85, -0.4)), gp, 0.2,0.2,0.2)
 		end
 	end
 
 	if gp and InputDown("rmb") then
     	local ct = GetCameraTransform()
-    	local playerPos = GetPlayerPos()
+    	local playerPos = GetPlayerPos(playerId)
     	local grapplePoint
         
     	if gb then
@@ -168,14 +119,13 @@
 		
 		local offset = VecSub(grapplePoint, playerPos)
         if gb then
-            SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(VecNormalize(offset), grapplepower_a * 0.75)))
+            SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(VecNormalize(offset), grapplepower_a * 0.75)))
             ApplyBodyImpulse(gb, grapplePoint, VecScale(VecNormalize(offset), grapplepower_a * -250))
         else
-            SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(VecNormalize(offset), grapplepower_a)))
+            SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(VecNormalize(offset), grapplepower_a)))
         end
 	end	
-end	
-
+end
 
 function LeftString()
 	if GetBool("game.player.canusetool") and InputPressed("lmb") then--left string
@@ -202,7 +152,7 @@
 	
 	if lgp and InputDown("lmb") then
     	local ct = GetCameraTransform()
-    	local playerPos = GetPlayerPos()
+    	local playerPos = GetPlayerPos(playerId)
     	local grapplePoint
         
     	if lgb then
@@ -214,14 +164,13 @@
 		
 		local offset = VecSub(grapplePoint, playerPos)
         if lgb then
-            SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(VecNormalize(offset), grapplepower_a * 0.75)))
+            SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(VecNormalize(offset), grapplepower_a * 0.75)))
             ApplyBodyImpulse(lgb, grapplePoint, VecScale(VecNormalize(offset), grapplepower_a * -250))
         else
-            SetPlayerVelocity(VecAdd(GetPlayerVelocity(), VecScale(VecNormalize(offset), grapplepower_a)))
+            SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId), VecScale(VecNormalize(offset), grapplepower_a)))
         end
 	end	
-end	
-
+end
 
 function Power(dt)
 	if power == nil then
@@ -233,8 +182,7 @@
 	else
 		power = 100.0 
 	end
-end	
-
+end
 
 function validateVariables()
     if grapplepower == nil then
@@ -256,114 +204,6 @@
         grapplepower_a = 0.5
         print("Fixed: grapplepower_a was nil")
     end
-end
-
-
-function tick(dt)
-	SetBool("game.player.show", true)
-	if lastuse == nil then
-		lastuse = 0 
-	elseif lastuse < 0 then
-		lastuse = 0
-	elseif lastuse < 1 then
-		lastuse = lastuse + dt
-	else 
-		Power(dt)	
-	end	 	
-	
-	validateVariables()
-	
-	local speed = VecLength(GetPlayerVelocity())--making holes when speeding
-	if speed > 25 then
-		MakeHole(GetPlayerPos(),1,0.5,0.125)
-	end
-	if speed > 50 then
-		MakeHole(GetPlayerPos(),1.5,0.75,0.25)
-	end
-	if speed > 100 then
-		MakeHole(GetPlayerPos(),2,1.0,0.5)
-	end
-
-
-	if GetString("game.player.tool") == "odm" then --if tool is selected than
-		if InputDown("space") then
-        	grapplepower_a = grapplepower
-		else
-			grapplepower_a =0
-		end	
-
-		if InputPressed("uparrow") then
-        	grapplepower = grapplepower + 0.1
-    	end
-
-		if InputPressed("downarrow") then
-        	grapplepower = grapplepower - 0.1
-    	end
-		
-		if InputPressed("shift") and IsPlayerGrounded() == false then
-			Shot()
-		end
-
-		Stab()
-
-		if InputDown("ctrl") and power > 0.0 then
-			GasAcceleration(dt)
-		end
-
-		LeftString()
-
-		RightString()
-
-		if InputDown("a") and power > 0.0 then
-			MovingLeft(dt)
-		end
-
-		if InputDown("d") and power > 0.0 then
-			MovingRight(dt)
-		end	
-
-		--Move tool and recoil
-		local t = Transform()
-		t.pos = Vec(0, -0.6, -0.3)
-		SetToolTransform(t)
-	end
-end
-
-function draw()-- output of % of gas
-	if GetString("game.player.tool") == "odm" then
-		UiPush()
-
-		spower = math.floor(math.max(power,0)+0.5).."%"
-		UiTranslate(UiCenter(), 1030)
-		UiAlign("center middle")
-		UiFont("bold.ttf", 40)
-		UiColor(0,0,0)
-		UiTranslate(0, 0.5)
-		UiText(spower)
-		UiTranslate(0, -1)
-		UiText(spower)
-		UiTranslate(0.5, 0.5)
-		UiText(spower)
-		UiTranslate(-1, 0)
-		UiText(spower)
-		UiTranslate(0.5, 0)
-		UiColor(1,1,1)
-		UiText(spower)
-
-		UiPop()
-
-		UiPush()
-
-		UiTranslate(300, 100)
-		UiAlign("left top")
-		UiFont("bold.ttf", 40)
-		UiColor(0, 0, 0)
-        UiTranslate(3, 3)
-        UiText("Odm power: " .. tostring(grapplepower))
-        UiTranslate(-1, -1)
-        UiColor(1, 1, 1)
-        UiText("Odm power: " .. tostring(grapplepower))		
-	end
 end
 
 function getRaycastBody() --searching for a body
@@ -390,4 +230,150 @@
         return point
     end
     return false
-end+end
+
+function server.init()
+    local mode = 1 --mode(1 - scout, 0 - anti-human)  
+    --Register tool and enable it
+    RegisterTool("odm", "ODM Gear", "MOD/vox/odm.vox")
+    SetBool("game.tool.odm.enabled", true, true)
+    grapplepower = 0.5
+    lastuse = 0
+    power = 100
+    grapplepower_a = 0.5
+    lgp = nil
+    lgb = nil
+    gp = nil
+    gb = nil
+    SetInt("game.tool.odm.ammo", 100, true)
+    local mode = 1
+    else
+    	function Shot()
+    		local ct = GetCameraTransform()
+       		local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
+    		Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "shotgun", 1, 150 )
+    	end
+    end
+end
+
+function server.tick(dt)
+    SetBool("game.player.show", true, true)
+    if lastuse == nil then
+    	lastuse = 0 
+    elseif lastuse < 0 then
+    	lastuse = 0
+    elseif lastuse < 1 then
+    	lastuse = lastuse + dt
+    else 
+    	Power(dt)	
+    end	 	
+    validateVariables()
+    local speed = VecLength(GetPlayerVelocity(playerId))--making holes when speeding
+    if speed > 25 then
+    	MakeHole(GetPlayerPos(playerId),1,0.5,0.125)
+    end
+    if speed > 50 then
+    	MakeHole(GetPlayerPos(playerId),1.5,0.75,0.25)
+    end
+    if speed > 100 then
+    	MakeHole(GetPlayerPos(playerId),2,1.0,0.5)
+    end
+end
+
+function client.init()
+    HookSnd = {LoadSound("MOD/HookSnd1.ogg"),LoadSound("MOD/HookSnd2.ogg")}
+    GasSnd = {LoadSound("gas-s0.ogg"),LoadSound("gas-s1.ogg")}
+    ShotgunShotSnd = {LoadSound("tools/shotgun0.ogg"),LoadSound("tools/shotgun1.ogg"),LoadSound("tools/shotgun2.ogg"),LoadSound("tools/shotgun3.ogg"),LoadSound("tools/shotgun4.ogg"),LoadSound("tools/shotgun5.ogg"),LoadSound("tools/shotgun6.ogg")}
+    RocketShotSnd = {LoadSound("tools/launcher1.ogg"),LoadSound("tools/launcher2.ogg"),LoadSound("tools/launcher3.ogg"),LoadSound("tools/launcher4.ogg"),LoadSound("tools/launcher5.ogg"),}
+    if mode == 0 then
+    	function Shot()
+    		local ct = GetCameraTransform()
+    		local shootpos = TransformToParentPoint(ct, Vec(0.55, -0.85, -1.2))
+    		PlaySound(RocketShotSnd[math.random(1, #RocketShotSnd)])
+       		Shoot(shootpos, TransformToParentVec(ct, Vec(0, 0, -1)), "rocket", 1.5, 300 )
+    	end	
+       		PlaySound(ShotgunShotSnd[math.random(1, #ShotgunShotSnd)])
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "odm" then --if tool is selected than
+    	if InputDown("space") then
+           	grapplepower_a = grapplepower
+    	else
+    		grapplepower_a =0
+    	end	
+
+    	if InputPressed("uparrow") then
+           	grapplepower = grapplepower + 0.1
+       	end
+
+    	if InputPressed("downarrow") then
+           	grapplepower = grapplepower - 0.1
+       	end
+
+    	if InputPressed("shift") and IsPlayerGrounded() == false then
+    		Shot()
+    	end
+
+    	Stab()
+
+    	if InputDown("ctrl") and power > 0.0 then
+    		GasAcceleration(dt)
+    	end
+
+    	LeftString()
+
+    	RightString()
+
+    	if InputDown("a") and power > 0.0 then
+    		MovingLeft(dt)
+    	end
+
+    	if InputDown("d") and power > 0.0 then
+    		MovingRight(dt)
+    	end	
+
+    	--Move tool and recoil
+    	local t = Transform()
+    	t.pos = Vec(0, -0.6, -0.3)
+    	SetToolTransform(t)
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "odm" then
+    	UiPush()
+
+    	spower = math.floor(math.max(power,0)+0.5).."%"
+    	UiTranslate(UiCenter(), 1030)
+    	UiAlign("center middle")
+    	UiFont("bold.ttf", 40)
+    	UiColor(0,0,0)
+    	UiTranslate(0, 0.5)
+    	UiText(spower)
+    	UiTranslate(0, -1)
+    	UiText(spower)
+    	UiTranslate(0.5, 0.5)
+    	UiText(spower)
+    	UiTranslate(-1, 0)
+    	UiText(spower)
+    	UiTranslate(0.5, 0)
+    	UiColor(1,1,1)
+    	UiText(spower)
+
+    	UiPop()
+
+    	UiPush()
+
+    	UiTranslate(300, 100)
+    	UiAlign("left top")
+    	UiFont("bold.ttf", 40)
+    	UiColor(0, 0, 0)
+           UiTranslate(3, 3)
+           UiText("Odm power: " .. tostring(grapplepower))
+           UiTranslate(-1, -1)
+           UiColor(1, 1, 1)
+           UiText("Odm power: " .. tostring(grapplepower))		
+    end
+end
+

```
