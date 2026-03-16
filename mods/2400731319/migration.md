# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,29 +1,4 @@
-chargeshotgunprojectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false},
-}
-
-function init()
-	RegisterTool("cresta-chargeshotgun", "Charge Shotgun", "MOD/vox/chargeshotgun.vox")
-	SetBool("game.tool.cresta-chargeshotgun.enabled", true)
-	SetString("game.tool.cresta-chargeshotgun.ammo.display","")
-	SetFloat("game.tool.cresta-chargeshotgun.ammo", 101)
-
-	gravity = Vec(0, 0, 0)
-	velocity = 50
-	charging = false
-	bullets = 0
-	recoilTimer = 0
-
-	for i=1, 900 do
-		chargeshotgunprojectileHandler.shells[i] = deepcopy(chargeshotgunprojectileHandler.defaultShell)
-	end
-
-	gunsound = LoadSound("MOD/snd/blast.ogg")
-	chargesound = LoadLoop("MOD/snd/chargeloop.ogg")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -69,9 +44,9 @@
 	aimpos, hit, distance = GetAimPos()
 	
 	local recoildir = TransformToParentVec(ct, Vec(0, 0, bullets/30))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	vel = VecAdd(vel, recoildir)
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
 	recoilTimer = math.max(0.10, bullets/1800)
 	
 	local fwdpos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -3))
@@ -118,73 +93,94 @@
 	projectile.pos = point2
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "cresta-chargeshotgun" and GetBool("game.player.canusetool") then
-		if InputDown("lmb") then
-			charging = true
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.05, 0.1, 0))
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -2))
-
-			local shapes = GetBodyShapes(b)
-			for i=1, #shapes do
-				if InputDown("lmb") then
-					SetShapeEmissiveScale(shapes[i], 5)
-				else
-					SetShapeEmissiveScale(shapes[i], 0)
-				end
-			end
-
-			if charging and  InputReleased("lmb") then
-				PointLight(toolPos, 1, 0.4, 1, 1)
-			end
-
-			if recoilTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0.2, recoilTimer/2)
-				t.rot = QuatEuler(recoilTimer*70, 0, 0)
-				SetToolTransform(t)
-
-				recoilTimer = recoilTimer - dt
-			end
-		end
-
-		if charging and InputReleased("lmb") then
-			Shoot()
-			PlaySound(gunsound, GetPlayerTransform().pos, 0.5)
-			bullets = 0
-			charging = false
-		end
-
-		for key, shell in ipairs(chargeshotgunprojectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
-			end
-		end
-
-		if charging then
-			PlayLoop(chargesound, GetPlayerTransform().pos, 0.4)
-			bullets = math.min(bullets + (GetTimeStep()*500), 900)
-		end
-	else
-		charging = false
-	end
+function server.init()
+    RegisterTool("cresta-chargeshotgun", "Charge Shotgun", "MOD/vox/chargeshotgun.vox")
+    SetBool("game.tool.cresta-chargeshotgun.enabled", true, true)
+    SetString("game.tool.cresta-chargeshotgun.ammo.display","", true)
+    SetFloat("game.tool.cresta-chargeshotgun.ammo", 101, true)
+    gravity = Vec(0, 0, 0)
+    velocity = 50
+    charging = false
+    bullets = 0
+    recoilTimer = 0
+    for i=1, 900 do
+    	chargeshotgunprojectileHandler.shells[i] = deepcopy(chargeshotgunprojectileHandler.defaultShell)
+    end
+    chargesound = LoadLoop("MOD/snd/chargeloop.ogg")
 end
 
-function draw()
-	if GetString("game.player.tool") == "cresta-chargeshotgun" and GetBool("game.player.canusetool") then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(math.floor(bullets))
-		UiPop()
-	end
-end+function client.init()
+    gunsound = LoadSound("MOD/snd/blast.ogg")
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "cresta-chargeshotgun" and GetBool("game.player.canusetool") then
+    	if InputDown("lmb") then
+    		charging = true
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.05, 0.1, 0))
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.3, -0.5, -2))
+
+    		local shapes = GetBodyShapes(b)
+    		for i=1, #shapes do
+    			if InputDown("lmb") then
+    				SetShapeEmissiveScale(shapes[i], 5)
+    			else
+    				SetShapeEmissiveScale(shapes[i], 0)
+    			end
+    		end
+
+    		if charging and  InputReleased("lmb") then
+    			PointLight(toolPos, 1, 0.4, 1, 1)
+    		end
+
+    		if recoilTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0.2, recoilTimer/2)
+    			t.rot = QuatEuler(recoilTimer*70, 0, 0)
+    			SetToolTransform(t)
+
+    			recoilTimer = recoilTimer - dt
+    		end
+    	end
+
+    	if charging and InputReleased("lmb") then
+    		Shoot()
+    		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.5)
+    		bullets = 0
+    		charging = false
+    	end
+
+    	for key, shell in ipairs(chargeshotgunprojectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		end
+    	end
+
+    	if charging then
+    		PlayLoop(chargesound, GetPlayerTransform(playerId).pos, 0.4)
+    		bullets = math.min(bullets + (GetTimeStep()*500), 900)
+    	end
+    else
+    	charging = false
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "cresta-chargeshotgun" and GetBool("game.player.canusetool") then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText(math.floor(bullets))
+    	UiPop()
+    end
+end
+

```
