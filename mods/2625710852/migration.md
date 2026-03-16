# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,54 +1,4 @@
-function init()
-	RegisterTool("cresta-vacuumcleaner", "Vacuum Cleaner", "MOD/vox/vacuumcleaner.vox")
-	SetBool("game.tool.cresta-vacuumcleaner.enabled", true)
-	SetString("game.tool.cresta-vacuumcleaner.ammo.display","")
-	SetFloat("game.tool.cresta-vacuumcleaner.ammo", 101)
-
-	items = {}
-	count = 1
-	velocity = 0.5
-	spitspeed = 0
-	suckspeed = 0
-	vacuumpower = GetFloat("savegame.mod.vacuumpower")
-	spitpower = GetFloat("savegame.mod.spitpower")
-	if vacuumpower <= 0 then vacuumpower = 50 end
-	if spitpower <= 0 then spitpower = 50 end
-	tooltop = Vec()
-	affectradius = 1
-	deletestuff = false
-	started = false
-	optionsopen = false
-	startDelay = 0.35
-
-	STATE_READY = 1
-	STATE_SUCKSTART = 2
-	STATE_SUCK = 3
-	STATE_SUCKEND = 4
-	state = STATE_READY
-
-	maxmass = 640
-	maxdist = 1
-	strength = 0.4
-
-	ang = 0
-	angVel = 0
-	roll = 0
-	rollVel = 0
-	rollK = 1
-
-	vacuumloop = LoadLoop("MOD/snd/vacuumloop.ogg")
-	vacuumloopfast = LoadLoop("MOD/snd/vacuumloopf.ogg")
-	vacuumloopslow = LoadLoop("MOD/snd/vacuumloops.ogg")
-	vacuumstart = LoadSound("MOD/snd/vacuumstart.ogg")
-	vacuumstartfast = LoadSound("MOD/snd/vacuumstartf.ogg")
-	vacuumstartslow = LoadSound("MOD/snd/vacuumstarts.ogg")
-	vacuumend = LoadSound("MOD/snd/vacuumend.ogg")
-	vacuumendfast = LoadSound("MOD/snd/vacuumendf.ogg")
-	vacuumendslow = LoadSound("MOD/snd/vacuumends.ogg")
-	vacuumsuck = LoadSound("MOD/snd/vacuumsuck.ogg")
-	vacuumspit = LoadSound("MOD/snd/vacuumspit.ogg")
-end
-
+#version 2
 function GetAimPos()
 	local ct = GetCameraTransform()
 	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
@@ -63,7 +13,7 @@
 end
 
 function Suction(shape)
-	if suckspeed > 0 then return end
+	if suckspeed ~= 0 then return end
 	local ct = GetCameraTransform()
 	local body = GetShapeBody(shape)
 	local vehicle = GetBodyVehicle(body)
@@ -178,7 +128,7 @@
 end
 
 function Spition()
-	if count < 2 or spitspeed > 0 then return end
+	if count < 2 or spitspeed ~= 0 then return end
 
 	local ct = GetCameraTransform()
 	local startpos = TransformToParentPoint(ct, Vec(0, 0, -3))
@@ -214,170 +164,6 @@
 		spitspeed = 0.3
 	end
 	spitspeed = spitspeed / math.max(1, (spitpower/25))
-end
-
-function tick(dt)
-	if GetString("game.player.tool") == "cresta-vacuumcleaner" and GetBool("game.player.canusetool") then
-		local lmbdown, lmbup, rmbdown, rmbup = InputDown("lmb"), InputReleased("lmb"), InputDown("rmb"), InputReleased("rmb")
-		
-		if lmbdown and (state == STATE_READY or state == STATE_SUCKEND) then
-			state = STATE_SUCKSTART
-			roll = 10
-			rollK = 1
-			if vacuumpower > 67 then
-				PlaySound(vacuumstartfast, GetPlayerTransform().pos, 0.4)
-			elseif vacuumpower < 33 then
-				PlaySound(vacuumstartslow, GetPlayerTransform().pos, 0.4)
-			else
-				PlaySound(vacuumstart, GetPlayerTransform().pos, 0.4)
-			end
-		end
-
-		if rmbdown and (state == STATE_READY or state == STATE_SUCKEND) then
-			state = STATE_SUCKSTART
-			roll = 10
-			rollK = 1
-			if spitpower > 67 then
-				PlaySound(vacuumstartfast, GetPlayerTransform().pos, 0.4)
-			elseif spitpower < 33 then
-				PlaySound(vacuumstartslow, GetPlayerTransform().pos, 0.4)
-			else
-				PlaySound(vacuumstart, GetPlayerTransform().pos, 0.4)
-			end
-		end
-
-		if lmbup and (state == STATE_SUCK or state == STATE_SPIT or state == STATE_SUCKSTART) then
-			state = STATE_SUCKEND
-			roll = 10
-			rollK = 1
-			if vacuumpower > 67 then
-				PlaySound(vacuumendfast, GetPlayerTransform().pos, 0.4)
-			elseif vacuumpower < 33 then
-				PlaySound(vacuumendslow, GetPlayerTransform().pos, 0.4)
-			else
-				PlaySound(vacuumend, GetPlayerTransform().pos, 0.4)
-			end
-		end
-
-		if rmbup and (state == STATE_SUCK or state == STATE_SPIT or state == STATE_SUCKSTART) then
-			state = STATE_SUCKEND
-			roll = 10
-			rollK = 1
-			if spitpower > 67 then
-				PlaySound(vacuumendfast, GetPlayerTransform().pos, 0.4)
-			elseif spitpower < 33 then
-				PlaySound(vacuumendslow, GetPlayerTransform().pos, 0.4)
-			else
-				PlaySound(vacuumend, GetPlayerTransform().pos, 0.4)
-			end
-		end
-
-		if state == STATE_SUCKSTART then
-			startDelay = startDelay - dt
-			if startDelay <= 0 then
-				if lmbdown then
-					state = STATE_SUCK
-				elseif rmbdown then
-					state = STATE_SPIT
-				end
-			end
-		end
-
-		if state == STATE_SUCKEND then
-			startDelay = startDelay + dt
-			if startDelay > 0.35 then
-				state = STATE_SUCKEND
-				startDelay = 0.35
-			end
-		end
-
-		if state == STATE_SUCK then
-			Vacuum()
-			if vacuumpower > 67 then
-				PlayLoop(vacuumloopfast, GetPlayerTransform().pos, 0.4)
-			elseif vacuumpower < 33 then
-				PlayLoop(vacuumloopslow, GetPlayerTransform().pos, 0.4)
-			else
-				PlayLoop(vacuumloop, GetPlayerTransform().pos, 0.4)
-			end
-		end
-
-		if state == STATE_SPIT then
-			Spition()
-			Blower()
-			if spitpower > 67 then
-				PlayLoop(vacuumloopfast, GetPlayerTransform().pos, 0.4)
-			elseif spitpower < 33 then
-				PlayLoop(vacuumloopslow, GetPlayerTransform().pos, 0.4)
-			else
-				PlayLoop(vacuumloop, GetPlayerTransform().pos, 0.4)
-			end
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			tooltop = TransformToParentPoint(toolTrans, Vec(0.355, -0.425, -2))
-
-			local framerate = dt*60
-			angVel = angVel * math.pow(0.8, framerate) - 0.02 * ang
-            ang = ang + angVel * framerate
-			rollK = rollK + 0.01 * -rollK
-            rollVel = rollVel * math.pow(rollK, framerate) - 0.2 * roll
-            roll = roll + rollVel * framerate
-
-			local offsetTransform = Transform(Vec(0, 0, 0), QuatEuler(ang * 3, ang * 3, roll))
-			SetToolTransform(offsetTransform)
-
-			if spitspeed > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, -spitspeed)
-				t.rot = QuatEuler(spitspeed*20, 0, 0)
-				SetToolTransform(t)
-
-				spitspeed = spitspeed - dt
-			end
-
-			if suckspeed > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, suckspeed)
-				t.rot = QuatEuler(suckspeed*20, 0, 0)
-				SetToolTransform(t)
-
-				suckspeed = suckspeed - dt
-			end
-		end
-		if spitspeed > 0 then
-			spitspeed = spitspeed - dt
-		end
-		if suckspeed > 0 then
-			suckspeed = suckspeed - dt
-		end
-	else
-		state = STATE_READY
-		startDelay = 0.35
-	end
-	if GetString("game.player.tool") == "cresta-vacuumcleaner" then
-		if InputPressed("R") then optionsopen = not optionsopen end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "cresta-vacuumcleaner" and GetBool("game.player.canusetool") then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(count-1)
-		UiPop()
-	end
-	if GetString("game.player.tool") == "cresta-vacuumcleaner" and optionsopen then
-		drawoptions()
-	end
 end
 
 function drawoptions()
@@ -411,7 +197,7 @@
 				UiAlign("right")
                 UiTranslate(0, 25)
 				vacuumpower = optionsSlider(vacuumpower, 1, 100)
-				SetFloat("savegame.mod.vacuumpower", vacuumpower)
+				SetFloat("savegame.mod.vacuumpower", vacuumpower, true)
 				UiTranslate(0, -25)
 				UiText(vacuumpower)
             UiPop()
@@ -423,7 +209,7 @@
 				UiAlign("right")
 				UiTranslate(0, 25)
 				spitpower = optionsSlider(spitpower, 1, 100)
-				SetFloat("savegame.mod.spitpower", spitpower)
+				SetFloat("savegame.mod.spitpower", spitpower, true)
 				UiTranslate(0, -25)
 				UiText(spitpower)
 			UiPop()
@@ -449,4 +235,222 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    RegisterTool("cresta-vacuumcleaner", "Vacuum Cleaner", "MOD/vox/vacuumcleaner.vox")
+    SetBool("game.tool.cresta-vacuumcleaner.enabled", true, true)
+    SetString("game.tool.cresta-vacuumcleaner.ammo.display","", true)
+    SetFloat("game.tool.cresta-vacuumcleaner.ammo", 101, true)
+    items = {}
+    count = 1
+    velocity = 0.5
+    spitspeed = 0
+    suckspeed = 0
+    vacuumpower = GetFloat("savegame.mod.vacuumpower")
+    spitpower = GetFloat("savegame.mod.spitpower")
+end
+
+function client.init()
+    if vacuumpower <= 0 then vacuumpower = 50 end
+    if spitpower <= 0 then spitpower = 50 end
+    tooltop = Vec()
+    affectradius = 1
+    deletestuff = false
+    started = false
+    optionsopen = false
+    startDelay = 0.35
+
+    STATE_READY = 1
+    STATE_SUCKSTART = 2
+    STATE_SUCK = 3
+    STATE_SUCKEND = 4
+    state = STATE_READY
+
+    maxmass = 640
+    maxdist = 1
+    strength = 0.4
+
+    ang = 0
+    angVel = 0
+    roll = 0
+    rollVel = 0
+    rollK = 1
+
+    vacuumloop = LoadLoop("MOD/snd/vacuumloop.ogg")
+    vacuumloopfast = LoadLoop("MOD/snd/vacuumloopf.ogg")
+    vacuumloopslow = LoadLoop("MOD/snd/vacuumloops.ogg")
+    vacuumstart = LoadSound("MOD/snd/vacuumstart.ogg")
+    vacuumstartfast = LoadSound("MOD/snd/vacuumstartf.ogg")
+    vacuumstartslow = LoadSound("MOD/snd/vacuumstarts.ogg")
+    vacuumend = LoadSound("MOD/snd/vacuumend.ogg")
+    vacuumendfast = LoadSound("MOD/snd/vacuumendf.ogg")
+    vacuumendslow = LoadSound("MOD/snd/vacuumends.ogg")
+    vacuumsuck = LoadSound("MOD/snd/vacuumsuck.ogg")
+    vacuumspit = LoadSound("MOD/snd/vacuumspit.ogg")
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "cresta-vacuumcleaner" and GetBool("game.player.canusetool") then
+    	local lmbdown, lmbup, rmbdown, rmbup = InputDown("lmb"), InputReleased("lmb"), InputDown("rmb"), InputReleased("rmb")
+
+    	if lmbdown and (state == STATE_READY or state == STATE_SUCKEND) then
+    		state = STATE_SUCKSTART
+    		roll = 10
+    		rollK = 1
+    		if vacuumpower > 67 then
+    			PlaySound(vacuumstartfast, GetPlayerTransform(playerId).pos, 0.4)
+    		elseif vacuumpower < 33 then
+    			PlaySound(vacuumstartslow, GetPlayerTransform(playerId).pos, 0.4)
+    		else
+    			PlaySound(vacuumstart, GetPlayerTransform(playerId).pos, 0.4)
+    		end
+    	end
+
+    	if rmbdown and (state == STATE_READY or state == STATE_SUCKEND) then
+    		state = STATE_SUCKSTART
+    		roll = 10
+    		rollK = 1
+    		if spitpower > 67 then
+    			PlaySound(vacuumstartfast, GetPlayerTransform(playerId).pos, 0.4)
+    		elseif spitpower < 33 then
+    			PlaySound(vacuumstartslow, GetPlayerTransform(playerId).pos, 0.4)
+    		else
+    			PlaySound(vacuumstart, GetPlayerTransform(playerId).pos, 0.4)
+    		end
+    	end
+
+    	if lmbup and (state == STATE_SUCK or state == STATE_SPIT or state == STATE_SUCKSTART) then
+    		state = STATE_SUCKEND
+    		roll = 10
+    		rollK = 1
+    		if vacuumpower > 67 then
+    			PlaySound(vacuumendfast, GetPlayerTransform(playerId).pos, 0.4)
+    		elseif vacuumpower < 33 then
+    			PlaySound(vacuumendslow, GetPlayerTransform(playerId).pos, 0.4)
+    		else
+    			PlaySound(vacuumend, GetPlayerTransform(playerId).pos, 0.4)
+    		end
+    	end
+
+    	if rmbup and (state == STATE_SUCK or state == STATE_SPIT or state == STATE_SUCKSTART) then
+    		state = STATE_SUCKEND
+    		roll = 10
+    		rollK = 1
+    		if spitpower > 67 then
+    			PlaySound(vacuumendfast, GetPlayerTransform(playerId).pos, 0.4)
+    		elseif spitpower < 33 then
+    			PlaySound(vacuumendslow, GetPlayerTransform(playerId).pos, 0.4)
+    		else
+    			PlaySound(vacuumend, GetPlayerTransform(playerId).pos, 0.4)
+    		end
+    	end
+
+    	if state == STATE_SUCKSTART then
+    		startDelay = startDelay - dt
+    		if startDelay <= 0 then
+    			if lmbdown then
+    				state = STATE_SUCK
+    			elseif rmbdown then
+    				state = STATE_SPIT
+    			end
+    		end
+    	end
+
+    	if state == STATE_SUCKEND then
+    		startDelay = startDelay + dt
+    		if startDelay > 0.35 then
+    			state = STATE_SUCKEND
+    			startDelay = 0.35
+    		end
+    	end
+
+    	if state == STATE_SUCK then
+    		Vacuum()
+    		if vacuumpower > 67 then
+    			PlayLoop(vacuumloopfast, GetPlayerTransform(playerId).pos, 0.4)
+    		elseif vacuumpower < 33 then
+    			PlayLoop(vacuumloopslow, GetPlayerTransform(playerId).pos, 0.4)
+    		else
+    			PlayLoop(vacuumloop, GetPlayerTransform(playerId).pos, 0.4)
+    		end
+    	end
+
+    	if state == STATE_SPIT then
+    		Spition()
+    		Blower()
+    		if spitpower > 67 then
+    			PlayLoop(vacuumloopfast, GetPlayerTransform(playerId).pos, 0.4)
+    		elseif spitpower < 33 then
+    			PlayLoop(vacuumloopslow, GetPlayerTransform(playerId).pos, 0.4)
+    		else
+    			PlayLoop(vacuumloop, GetPlayerTransform(playerId).pos, 0.4)
+    		end
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		tooltop = TransformToParentPoint(toolTrans, Vec(0.355, -0.425, -2))
+
+    		local framerate = dt*60
+    		angVel = angVel * math.pow(0.8, framerate) - 0.02 * ang
+               ang = ang + angVel * framerate
+    		rollK = rollK + 0.01 * -rollK
+               rollVel = rollVel * math.pow(rollK, framerate) - 0.2 * roll
+               roll = roll + rollVel * framerate
+
+    		local offsetTransform = Transform(Vec(0, 0, 0), QuatEuler(ang * 3, ang * 3, roll))
+    		SetToolTransform(offsetTransform)
+
+    		if spitspeed ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, -spitspeed)
+    			t.rot = QuatEuler(spitspeed*20, 0, 0)
+    			SetToolTransform(t)
+
+    			spitspeed = spitspeed - dt
+    		end
+
+    		if suckspeed ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, suckspeed)
+    			t.rot = QuatEuler(suckspeed*20, 0, 0)
+    			SetToolTransform(t)
+
+    			suckspeed = suckspeed - dt
+    		end
+    	end
+    	if spitspeed ~= 0 then
+    		spitspeed = spitspeed - dt
+    	end
+    	if suckspeed ~= 0 then
+    		suckspeed = suckspeed - dt
+    	end
+    else
+    	state = STATE_READY
+    	startDelay = 0.35
+    end
+    if GetString("game.player.tool") == "cresta-vacuumcleaner" then
+    	if InputPressed("R") then optionsopen = not optionsopen end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "cresta-vacuumcleaner" and GetBool("game.player.canusetool") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText(count-1)
+    	UiPop()
+    end
+    if GetString("game.player.tool") == "cresta-vacuumcleaner" and optionsopen then
+    	drawoptions()
+    end
+end
+

```
