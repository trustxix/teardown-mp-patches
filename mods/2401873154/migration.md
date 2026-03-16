# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,36 +1,4 @@
-holygrenade = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {
-		active = false, 
-		grenadeTimer = 0,
-		boomTimer = 0,
-		bounces = 0,
-	},
-}
-
-function init()
-	RegisterTool("holygrenade", "Holy Grenade", "MOD/vox/holygrenade.vox")
-	SetBool("game.tool.holygrenade.enabled", true)
-	SetFloat("game.tool.holygrenade.ammo", 101)
-
-	holygrenadegravity = Vec(0, -160, 0)
-	holygrenadevelocity = 100
-	holygrenadefuseTime = 5
-	swingTimer = 0
-
-	for i=1, 250 do
-		holygrenade.shells[i] = deepcopy(holygrenade.defaultShell)
-	end
-
-	holygrenadethrowsound = LoadSound("MOD/snd/throw.ogg")
-	holygrenadebouncesound = LoadSound("MOD/snd/holybounce.ogg")
-	holygrenadehallesound = LoadSound("MOD/snd/hallelujah.ogg")
-	holygrenadeboomsound = LoadSound("MOD/snd/holyboom.ogg")
-
-	holygrenadesprite = LoadSprite("MOD/img/holygren.png")
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -89,59 +57,81 @@
 	end
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "holygrenade" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			Shoot()
-		end
+function server.init()
+    RegisterTool("holygrenade", "Holy Grenade", "MOD/vox/holygrenade.vox")
+    SetBool("game.tool.holygrenade.enabled", true, true)
+    SetFloat("game.tool.holygrenade.ammo", 101, true)
+    holygrenadegravity = Vec(0, -160, 0)
+    holygrenadevelocity = 100
+    holygrenadefuseTime = 5
+    swingTimer = 0
+    for i=1, 250 do
+    	holygrenade.shells[i] = deepcopy(holygrenade.defaultShell)
+    end
+    holygrenadesprite = LoadSprite("MOD/img/holygren.png")
+end
 
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
-			SetToolTransform(offset)
+function client.init()
+    holygrenadethrowsound = LoadSound("MOD/snd/throw.ogg")
+    holygrenadebouncesound = LoadSound("MOD/snd/holybounce.ogg")
+    holygrenadehallesound = LoadSound("MOD/snd/hallelujah.ogg")
+    holygrenadeboomsound = LoadSound("MOD/snd/holyboom.ogg")
+end
 
-			if swingTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, swingTimer*2)
-				t.rot = QuatEuler(swingTimer*50, 0, 0)
-				SetToolTransform(t)
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "holygrenade" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		Shoot()
+    	end
 
-				swingTimer = swingTimer - dt
-			end
-		end
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0, 0, 0), QuatEuler(0, 0, 0))
+    		SetToolTransform(offset)
 
-		if InputPressed("X") then
-			holygrenadefuseTime = math.min(20, holygrenadefuseTime + 1)
-		elseif InputPressed("Z") then
-			holygrenadefuseTime = math.max(1, holygrenadefuseTime - 1)
-		end
-	end
+    		if swingTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, swingTimer*2)
+    			t.rot = QuatEuler(swingTimer*50, 0, 0)
+    			SetToolTransform(t)
 
-	for key, shell in ipairs(holygrenade.shells) do
-		if shell.grenadeTimer > 0 then
-			shell.grenadeTimer = shell.grenadeTimer - GetTimeStep()
-			if shell.grenadeTimer < 0.1 then
-				shell.grenadeTimer = 0
-				PlaySound(holygrenadehallesound, shell.grenadepos, 1, false)
-				shell.boomTimer = 1.4
-			end
-		end
+    			swingTimer = swingTimer - dt
+    		end
+    	end
 
-		if shell.boomTimer > 0 then
-			shell.boomTimer = shell.boomTimer - GetTimeStep()
-			if shell.boomTimer < 0.1 then
-				shell.boomTimer = 0
-				shell.active = false
-				Explosion(shell.grenadepos, 10)
-				PlaySound(holygrenadeboomsound, shell.grenadepos, 1)
-			end
-		end
+    	if InputPressed("X") then
+    		holygrenadefuseTime = math.min(20, holygrenadefuseTime + 1)
+    	elseif InputPressed("Z") then
+    		holygrenadefuseTime = math.max(1, holygrenadefuseTime - 1)
+    	end
+    end
+    for key, shell in ipairs(holygrenade.shells) do
+    	if shell.grenadeTimer ~= 0 then
+    		shell.grenadeTimer = shell.grenadeTimer - GetTimeStep()
+    		if shell.grenadeTimer < 0.1 then
+    			shell.grenadeTimer = 0
+    			PlaySound(holygrenadehallesound, shell.grenadepos, 1, false)
+    			shell.boomTimer = 1.4
+    		end
+    	end
 
-		if shell.active then
-			HolyGrenadeOperations(shell)
-			local rot = QuatLookAt(shell.grenadepos, GetCameraTransform().pos)
-			local transform = Transform(shell.grenadepos, rot)
-			DrawSprite(holygrenadesprite, transform, 0.4, 0.4, 0.5, 0.5, 0.5, 1, true, false)
-		end
-	end
-end+    	if shell.boomTimer ~= 0 then
+    		shell.boomTimer = shell.boomTimer - GetTimeStep()
+    		if shell.boomTimer < 0.1 then
+    			shell.boomTimer = 0
+    			shell.active = false
+    			Explosion(shell.grenadepos, 10)
+    			PlaySound(holygrenadeboomsound, shell.grenadepos, 1)
+    		end
+    	end
+
+    	if shell.active then
+    		HolyGrenadeOperations(shell)
+    		local rot = QuatLookAt(shell.grenadepos, GetCameraTransform().pos)
+    		local transform = Transform(shell.grenadepos, rot)
+    		DrawSprite(holygrenadesprite, transform, 0.4, 0.4, 0.5, 0.5, 0.5, 1, true, false)
+    	end
+    end
+end
+

```
