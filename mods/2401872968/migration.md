# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,27 +1,4 @@
-hadoukenHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false, strength = 2.5, maxDist = 7.5, maxMass = 1500},
-}
-
-function init()
-	RegisterTool("hadouken", "Hadouken", "MOD/vox/hadouken.vox")
-	SetBool("game.tool.hadouken.enabled", true)
-	SetFloat("game.tool.hadouken.ammo", 101)
-
-	ballgravity = Vec(0, 0, 0)
-	hadoukendamage = 1.5
-	velocity = 0.2
-	swingTimer = 0
-
-	for i=1, 100 do
-		hadoukenHandler.shells[i] = deepcopy(hadoukenHandler.defaultShell)
-	end
-
-	hadoukensound = LoadSound("MOD/snd/hadouken.ogg")
-	hadoukenSprite = LoadSprite("MOD/img/hadouken.png")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -64,7 +41,7 @@
 	loadedShell.predictedBulletVelocity = VecScale(direction, velocity)
 	hadoukenHandler.shellNum = (hadoukenHandler.shellNum%#hadoukenHandler.shells) +1
 
-	PlaySound(hadoukensound, GetPlayerTransform().pos, 0.45, false)
+	PlaySound(hadoukensound, GetPlayerTransform(playerId).pos, 0.45, false)
 	swingTimer = 0.3
 end
 
@@ -99,39 +76,6 @@
 
 	projectile.counter = projectile.counter + 1
     projectile.pos = point2
-end
-
-function tick(dt)
-	if GetString("game.player.tool") == "hadouken" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			Shoot()
-		end
-
-		if InputPressed("rmb") then
-			Boom()
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(10, 0, 0))
-			SetToolTransform(offset)
-
-			if swingTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, -swingTimer*3)
-				t.rot = QuatEuler(swingTimer*20, 0, 0)
-				SetToolTransform(t)
-
-				swingTimer = swingTimer - dt
-			end
-		end
-	end
-
-	for key, shell in ipairs(hadoukenHandler.shells) do
-		if shell.active then
-			HadoukenOperations(shell)
-		end
-	end
 end
 
 function HadoukenBlast(projectile)
@@ -171,4 +115,61 @@
 			SetBodyVelocity(b, vel)
 		end
 	end
-end+end
+
+function server.init()
+    RegisterTool("hadouken", "Hadouken", "MOD/vox/hadouken.vox")
+    SetBool("game.tool.hadouken.enabled", true, true)
+    SetFloat("game.tool.hadouken.ammo", 101, true)
+    ballgravity = Vec(0, 0, 0)
+    hadoukendamage = 1.5
+    velocity = 0.2
+    swingTimer = 0
+    for i=1, 100 do
+    	hadoukenHandler.shells[i] = deepcopy(hadoukenHandler.defaultShell)
+    end
+    hadoukenSprite = LoadSprite("MOD/img/hadouken.png")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(hadoukenHandler.shells) do
+        	if shell.active then
+        		HadoukenOperations(shell)
+        	end
+        end
+    end
+end
+
+function client.init()
+    hadoukensound = LoadSound("MOD/snd/hadouken.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "hadouken" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		Shoot()
+    	end
+
+    	if InputPressed("rmb") then
+    		Boom()
+    	end
+
+    	local b = GetToolBody()
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
+    	end
+    end
+end
+

```
