# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,20 +1,4 @@
-function init()
-	RegisterTool("magicbag", "Magic Bag", "MOD/vox/magicbag.vox")
-	SetBool("game.tool.magicbag.enabled", true)
-	SetFloat("game.tool.magicbag.ammo", 101)
-
-	items = {}
-	count = 1
-	velocity = 0.5
-	rottimer = 0
-	swingTimer = 0
-	pickTimer = 0
-	charging = false
-
-	throwsound = LoadSound("MOD/snd/throw.ogg")
-	picksound = LoadSound("tool_pickup.ogg")
-end
-
+#version 2
 function GetAimPos()
 	local ct = GetCameraTransform()
 	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
@@ -88,99 +72,119 @@
 	rottimer = 0.15
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "magicbag" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			PickItem()
-			pickTimer = 0.1
-		end
-
-		if InputDown("rmb") then
-			if count < 2 or rottimer > 0 then return end
-			charging = true
-		end
-
-		if InputReleased("rmb") then
-			if count < 2 or rottimer > 0 then return end
-			ThrowItem()
-			charging = false
-			velocity = 1
-			PlaySound(throwsound)
-			swingTimer = 0.2
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
-			SetToolTransform(offset)
-
-			if swingTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, -swingTimer*2)
-				t.rot = QuatEuler(swingTimer*30, 0, 0)
-				SetToolTransform(t)
-
-				swingTimer = swingTimer - dt
-			end
-
-			if pickTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, pickTimer)
-				t.rot = QuatEuler(pickTimer*20, 0, 0)
-				SetToolTransform(t)
-
-				pickTimer = pickTimer - dt
-			end
-		end
-
-		if charging then
-			velocity = math.min(velocity + (dt*50), 50)
-		end
-
-		if rottimer > 0 then
-			rottimer = rottimer - dt
-			local mx, my = InputValue("mousedx"), InputValue("mousedy")
-		
-			local rotvel = Vec(0, mx/40, -my/40)
-			local angvel = GetBodyAngularVelocity(items[count].body)
-			local newvel = VecAdd(rotvel, angvel)
-			SetBodyAngularVelocity(items[count].body, newvel)
-			
-			if rottimer <= 0 then
-				rottimer = 0
-			end
-		end
-	end
+function server.init()
+    RegisterTool("magicbag", "Magic Bag", "MOD/vox/magicbag.vox")
+    SetBool("game.tool.magicbag.enabled", true, true)
+    SetFloat("game.tool.magicbag.ammo", 101, true)
+    items = {}
+    count = 1
+    velocity = 0.5
+    rottimer = 0
+    swingTimer = 0
+    pickTimer = 0
+    charging = false
 end
 
-function draw()
-	if GetString("game.player.tool") == "magicbag" and GetPlayerVehicle() == 0 then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(count-1)
-		UiPop()
+function client.init()
+    throwsound = LoadSound("MOD/snd/throw.ogg")
+    picksound = LoadSound("tool_pickup.ogg")
+end
 
-		UiPush()
-			UiTranslate(UiCenter()-30, UiHeight()-110)
-			UiColor(1, 1, 1)
-			UiFont("regular.ttf", 24)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText("POWER")
-			
-			UiTranslate(-45, 10)
-			UiColor(0, 0, 0, 0.5)
-			local width = 150
-			UiImageBox("ui/common/box-solid-10.png", width, 20, 6, 6)
-			if velocity > 1 then
-				UiTranslate(2, 2)
-				width = (width-4)*(velocity/50)
-				UiColor(0.5, 1, 0.5)
-				UiImageBox("ui/common/box-solid-6.png", width, 16, 6, 6)
-			end
-		UiPop()
-	end
-end+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "magicbag" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		PickItem()
+    		pickTimer = 0.1
+    	end
+
+    	if InputDown("rmb") then
+    		if count < 2 or rottimer ~= 0 then return end
+    		charging = true
+    	end
+
+    	if InputReleased("rmb") then
+    		if count < 2 or rottimer ~= 0 then return end
+    		ThrowItem()
+    		charging = false
+    		velocity = 1
+    		PlaySound(throwsound)
+    		swingTimer = 0.2
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
+    		SetToolTransform(offset)
+
+    		if swingTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, -swingTimer*2)
+    			t.rot = QuatEuler(swingTimer*30, 0, 0)
+    			SetToolTransform(t)
+
+    			swingTimer = swingTimer - dt
+    		end
+
+    		if pickTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, pickTimer)
+    			t.rot = QuatEuler(pickTimer*20, 0, 0)
+    			SetToolTransform(t)
+
+    			pickTimer = pickTimer - dt
+    		end
+    	end
+
+    	if charging then
+    		velocity = math.min(velocity + (dt*50), 50)
+    	end
+
+    	if rottimer ~= 0 then
+    		rottimer = rottimer - dt
+    		local mx, my = InputValue("mousedx"), InputValue("mousedy")
+
+    		local rotvel = Vec(0, mx/40, -my/40)
+    		local angvel = GetBodyAngularVelocity(items[count].body)
+    		local newvel = VecAdd(rotvel, angvel)
+    		SetBodyAngularVelocity(items[count].body, newvel)
+
+    		if rottimer <= 0 then
+    			rottimer = 0
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "magicbag" and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText(count-1)
+    	UiPop()
+
+    	UiPush()
+    		UiTranslate(UiCenter()-30, UiHeight()-110)
+    		UiColor(1, 1, 1)
+    		UiFont("regular.ttf", 24)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText("POWER")
+
+    		UiTranslate(-45, 10)
+    		UiColor(0, 0, 0, 0.5)
+    		local width = 150
+    		UiImageBox("ui/common/box-solid-10.png", width, 20, 6, 6)
+    		if velocity > 1 then
+    			UiTranslate(2, 2)
+    			width = (width-4)*(velocity/50)
+    			UiColor(0.5, 1, 0.5)
+    			UiImageBox("ui/common/box-solid-6.png", width, 16, 6, 6)
+    		end
+    	UiPop()
+    end
+end
+

```
