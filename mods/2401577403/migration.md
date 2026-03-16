# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,32 +1,4 @@
-function init()
-	RegisterTool("scorpion", "Scorpion", "MOD/vox/scorpion.vox")
-	SetBool("game.tool.scorpion.enabled", true)
-	SetFloat("game.tool.scorpion.ammo", 101)
-
-	STATE_READY = 0
-	STATE_THROWN = 1
-	STATE_HOOKED = 2
-	STATE_PULLING = 3
-	state = STATE_READY
-
-	punchpower = GetFloat("savegame.mod.punchpower")
-	pullpower = GetFloat("savegame.mod.pullpower")
-	if punchpower == 0 then punchpower = 100 end
-	if pullpower == 0 then pullpower = 100 end
-	velocity = 0.75
-	gravity = Vec(0, 0, 0)
-	swingTimer = 0
-	pullTimer = 0
-
-	line = {}
-	line.active = false
-
-	comeheresound = LoadSound("MOD/snd/comehere0.ogg")
-	hitsound = LoadSound("MOD/snd/punch0.ogg")
-	swingsound = LoadSound("MOD/snd/swing0.ogg")
-	hooksound = LoadSound("MOD/snd/switch1.ogg")
-end
-
+#version 2
 function GetAimPos()
 	local ct = GetCameraTransform()
 	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
@@ -44,11 +16,11 @@
 function Punch()
 	local forwardPos = TransformToParentPoint(GetCameraTransform(), Vec(0, 0, -1))
 	local direction = VecSub(forwardPos, GetCameraTransform().pos)
-	PlaySound(swingsound, GetPlayerTransform().pos, 0.6, false)
+	PlaySound(swingsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	QueryRequire("physical")
 	local hit, dist, normal, shape = QueryRaycast(GetCameraTransform().pos, direction, 3)
 	if hit then
-		PlaySound(hitsound, GetPlayerTransform().pos, 0.75, false)
+		PlaySound(hitsound, GetPlayerTransform(playerId).pos, 0.75, false)
 		local body = GetShapeBody(shape)
 		if IsBodyDynamic(body) then
 			local mass = GetBodyMass(body)
@@ -65,7 +37,7 @@
 	local aimpos, dist = GetAimPos()
 	local startPos = TransformToParentPoint(GetCameraTransform(), Vec(0.45, -0.15, -1))
 	local direction = VecSub(aimpos, startPos)
-	PlaySound(swingsound, GetPlayerTransform().pos, 0.75, false)
+	PlaySound(swingsound, GetPlayerTransform(playerId).pos, 0.75, false)
 
 	line.gravity = gravity
 	line.pos = VecCopy(startPos)
@@ -73,7 +45,7 @@
 end
 
 function Pull()
-	PlaySound(comeheresound, GetPlayerTransform().pos, 0.5, false)
+	PlaySound(comeheresound, GetPlayerTransform(playerId).pos, 0.5, false)
 	local s = InputDown("s")
 	pullTimer = 0.45
 
@@ -107,7 +79,7 @@
 		
 		movedir = VecScale(movedir, scale*dirscale)
 		movedir = VecScale(movedir, pullpower)
-		SetPlayerVelocity(movedir)
+		SetPlayerVelocity(playerId, movedir)
 	end
 end
 
@@ -119,7 +91,7 @@
 	local hit, dist, normal, shape = QueryRaycast(line.pos, dir, VecLength(VecSub(point2, line.pos)))
 	
 	if hit then
-		PlaySound(hooksound, GetPlayerTransform().pos, 0.75, false)
+		PlaySound(hooksound, GetPlayerTransform(playerId).pos, 0.75, false)
 		hitPos = VecAdd(line.pos, VecScale(VecNormalize(VecSub(point2, line.pos)), dist))
 		hookbody = GetShapeBody(shape)
 		localhookpos = TransformToLocalPoint(GetBodyTransform(hookbody), hitPos)
@@ -131,61 +103,93 @@
 	line.pos = point2
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "scorpion" and GetPlayerVehicle() == 0 then
-		SetPlayerHealth(1)
-		if InputPressed("lmb") then
-			Punch()
-		end
-	
-		if InputPressed("rmb") then
-			if state == STATE_READY then
-				line.active = true
-				Hook()
-				state = STATE_THROWN
-			elseif state == STATE_HOOKED then
-				Pull()
-				state = STATE_READY
-				line.active = false
-			elseif state == STATE_THROWN then
-				state = STATE_READY
-				line.active = false
-			end
-		end
+function server.init()
+    RegisterTool("scorpion", "Scorpion", "MOD/vox/scorpion.vox")
+    SetBool("game.tool.scorpion.enabled", true, true)
+    SetFloat("game.tool.scorpion.ammo", 101, true)
+    STATE_READY = 0
+    STATE_THROWN = 1
+    STATE_HOOKED = 2
+    STATE_PULLING = 3
+    state = STATE_READY
+    punchpower = GetFloat("savegame.mod.punchpower")
+    pullpower = GetFloat("savegame.mod.pullpower")
+end
 
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(10, 0, 0))
-			SetToolTransform(offset)
+function client.init()
+    if punchpower == 0 then punchpower = 100 end
+    if pullpower == 0 then pullpower = 100 end
+    velocity = 0.75
+    gravity = Vec(0, 0, 0)
+    swingTimer = 0
+    pullTimer = 0
 
-			if swingTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, -swingTimer*3)
-				t.rot = QuatEuler(swingTimer*20, 0, 0)
-				SetToolTransform(t)
+    line = {}
+    line.active = false
 
-				swingTimer = swingTimer - dt
-			end
+    comeheresound = LoadSound("MOD/snd/comehere0.ogg")
+    hitsound = LoadSound("MOD/snd/punch0.ogg")
+    swingsound = LoadSound("MOD/snd/swing0.ogg")
+    hooksound = LoadSound("MOD/snd/switch1.ogg")
+end
 
-			if pullTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, pullTimer*2)
-				t.rot = QuatEuler(pullTimer*50, 0, 0)
-				SetToolTransform(t)
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "scorpion" and GetPlayerVehicle(playerId) == 0 then
+    	SetPlayerHealth(playerId, 1)
+    	if InputPressed("lmb") then
+    		Punch()
+    	end
 
-				pullTimer = pullTimer - dt
-			end
-		end
+    	if InputPressed("rmb") then
+    		if state == STATE_READY then
+    			line.active = true
+    			Hook()
+    			state = STATE_THROWN
+    		elseif state == STATE_HOOKED then
+    			Pull()
+    			state = STATE_READY
+    			line.active = false
+    		elseif state == STATE_THROWN then
+    			state = STATE_READY
+    			line.active = false
+    		end
+    	end
 
-		if line.active then
-			handPos = TransformToParentPoint(GetCameraTransform(), Vec(0.35, -0.4, -2))
-			if state == STATE_THROWN then
-				HookOperations(line)
-			elseif state == STATE_HOOKED then
-				hookpos = TransformToParentPoint(GetBodyTransform(hookbody), localhookpos)
-				DrawLine(handPos, hookpos, 0, 0, 0)
-				DrawBodyOutline(GetShapeBody(hookbody), 0.5)
-			end
-		end
-	end
-end+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0, 0, 0), QuatEuler(10, 0, 0))
+    		SetToolTransform(offset)
+
+    		if swingTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, -swingTimer*3)
+    			t.rot = QuatEuler(swingTimer*20, 0, 0)
+    			SetToolTransform(t)
+
+    			swingTimer = swingTimer - dt
+    		end
+
+    		if pullTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, pullTimer*2)
+    			t.rot = QuatEuler(pullTimer*50, 0, 0)
+    			SetToolTransform(t)
+
+    			pullTimer = pullTimer - dt
+    		end
+    	end
+
+    	if line.active then
+    		handPos = TransformToParentPoint(GetCameraTransform(), Vec(0.35, -0.4, -2))
+    		if state == STATE_THROWN then
+    			HookOperations(line)
+    		elseif state == STATE_HOOKED then
+    			hookpos = TransformToParentPoint(GetBodyTransform(hookbody), localhookpos)
+    			DrawLine(handPos, hookpos, 0, 0, 0)
+    			DrawBodyOutline(GetShapeBody(hookbody), 0.5)
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: options.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/options.lua
+++ patched/options.lua
@@ -1,50 +1,4 @@
-function init()
-	punchPower = GetFloat("savegame.mod.punchpower")
-	if punchPower == 0 then punchPower = 100 end
-	pullPower = GetFloat("savegame.mod.pullpower")
-	if pullPower == 0 then pullPower = 100 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Mortal Kombat Scorpion")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 40)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Punch Power")
-		UiAlign("right")
-		UiTranslate(95, 40)
-		punchPower = optionsSlider(punchPower, 30, 300)
-		UiTranslate(-75, 20)
-		UiColor(0.2, 0.6, 1)
-		UiText(punchPower)
-		SetFloat("savegame.mod.punchpower", punchPower)
-	UiPop()
-
-	UiTranslate(0, 110)
-	UiPush()
-		UiText("Hook Pull Power")
-		UiAlign("right")
-		UiTranslate(95, 40)
-		pullPower = optionsSlider(pullPower, 30, 300)
-		UiTranslate(-75, 20)
-		UiColor(0.2, 0.6, 1)
-		UiText(pullPower)
-		SetFloat("savegame.mod.pullpower", pullPower)
-	UiPop()
-
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -63,4 +17,52 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    punchPower = GetFloat("savegame.mod.punchpower")
+    if punchPower == 0 then punchPower = 100 end
+    pullPower = GetFloat("savegame.mod.pullpower")
+    if pullPower == 0 then pullPower = 100 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Mortal Kombat Scorpion")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 40)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Punch Power")
+    	UiAlign("right")
+    	UiTranslate(95, 40)
+    	punchPower = optionsSlider(punchPower, 30, 300)
+    	UiTranslate(-75, 20)
+    	UiColor(0.2, 0.6, 1)
+    	UiText(punchPower)
+    	SetFloat("savegame.mod.punchpower", punchPower, true)
+    UiPop()
+
+    UiTranslate(0, 110)
+    UiPush()
+    	UiText("Hook Pull Power")
+    	UiAlign("right")
+    	UiTranslate(95, 40)
+    	pullPower = optionsSlider(pullPower, 30, 300)
+    	UiTranslate(-75, 20)
+    	UiColor(0.2, 0.6, 1)
+    	UiText(pullPower)
+    	SetFloat("savegame.mod.pullpower", pullPower, true)
+    UiPop()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```
