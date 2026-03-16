# Migration Report: main backup.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main backup.lua
+++ patched/main backup.lua
@@ -1,62 +1,4 @@
-magma = {
-    shellNum = 1,
-    shells = {},
-    defaultShell = {
-        lifetime = 0
-    },
-}
-
-MKQue = {}
-
-laserSprite = LoadSprite("gfx/laser.png")
-muzzleflash = LoadSprite("gfx/glare.png")
-
-function init()
-    RegisterTool("magmatool", "Lava Gun", "MOD/vox/lavagun.vox")
-    SetBool("game.tool.magmatool.enabled", true)
-    SetFloat("game.tool.magmatool.ammo", 9999)
-
-    gravity = Vec(0, -5, 0)
-    velocity = 0
-
-   recoilTimer = 0
-   driftH = 0
-   driftV = 0
-  
-    shakex = 0
-    shakey = 0
-    shakez = 0
-
-    damage = 1.8
-    fps = 60
-    
-    lmbdown = true
-    fireamount = GetBool("savegame.mod.fireamount")
-    
-    BurnSound = LoadLoop("MOD/snd/sizzle.ogg")
-    BeamSound = LoadLoop("MOD/snd/loop.ogg")
-    PewSound = LoadSound("MOD/snd/pew.ogg")
-    FinallySound = LoadSound("MOD/snd/finish.ogg")
-    EndSound = LoadSound("MOD/snd/end.ogg")
-    SmokeSound = LoadSound("MOD/snd/smoke.ogg")
-
-    if fireamount then
-		big = true
-    end
-
-    if big then
-    for i=1, 150 do
-        magma.shells[i] = deepcopy(magma.defaultShell)
-    end
-end
-
-    if not big then
-    for i=1, 250 do
-        magma.shells[i] = deepcopy(magma.defaultShell)
-    end
-end
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -161,7 +103,6 @@
         ParticleEmissive(0)
 SpawnParticle("smoke", at, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.5)
 end
-
 
 function createMagmaParticle(at)
     local val = math.random()
@@ -307,7 +248,7 @@
 
 function randomVec(t)
 	return Vec(random(-t, t), random(-t, t), random(-t, t))
-end 
+end
 
 function lookpos()
   local t = GetCameraTransform()
@@ -319,7 +260,7 @@
     else
       return false
     end
-end  
+end
 
 function shooting2()
   if lookpos() then
@@ -343,81 +284,6 @@
 	end
 end
 
-function tick(dt)
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputPressed("lmb") then
-           PlaySound(PewSound,GetCameraTransform().pos, 1.5)
-        end
-    end
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputDown("lmb") then
-        lmbdown = true
-    else
-        lmbdown = false
-    end
-end
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputDown("lmb") then
-            Shoot()
-            laserBeam()
-            shooting2()
-       end
-    end
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputReleased("lmb") then
-           PlaySound(EndSound, GetCameraTransform().pos, 0.4, false)           
-           end
-    end
-
-
-if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-    if InputPressed("rmb") then
-    clearAllFires()
-end
-end
-
-if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-    if InputPressed("rmb") then
-        for key, shell in ipairs(magma.shells) do
-        if shell.lifetime > 0 then
-        shell.lifetime = shell.lifetime - dt
-            shell.lifetime = 0
-            createSmokeParticle(shell.magmapos)
-            PlaySound(SmokeSound,GetCameraTransform().pos, 1.5)
-end
-end
-end
-end
-
-    for key, shell in ipairs(magma.shells) do
-        if shell.lifetime > 0 then
-            shell.lifetime = shell.lifetime - dt
-            MagmaOperations(shell)
-            local rot = QuatLookAt(shell.magmapos, GetCameraTransform().pos)
-            local transform = Transform(shell.magmapos, rot)
-            createMagmaParticle(shell.magmapos)
-        end
-    end
-
-	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-
-                if InputDown("lmb") then
-                shakex = math.random(-5, 5)/350
-                shakey = math.random(-5, 5)/350
-                shakez = math.random(-5, 5)/350
-                end
-				
-		local t = Transform()
-		t.pos = Vec(0.3+shakex, -1.0+shakey, -0.40+shakez) --change the last three values to change vhere bullets originate left/right, up/down, forward,back
-		t.rot = QuatEuler(-3, 0, 0)
-                SetToolTransform(t)
-end
-end
-
 function destructiblerobots(pos,damage,hitcounter) --thanks dima
     local hit, point, n, shape = QueryClosestPoint(pos, 0.3)
 	if HasTag(shape, "shapeHealth") then
@@ -427,28 +293,139 @@
 	end
 
     if hit then 
-        SetFloat('level.destructible-bot.hitCounter',hitcounter)
-        SetInt('level.destructible-bot.hitShape',shape)
-        SetString('level.destructible-bot.weapon',"weapon-name")
-        SetFloat('level.destructible-bot.damage',damage)
+        SetFloat('level.destructible-bot.hitCounter',hitcounter, true)
+        SetInt('level.destructible-bot.hitShape',shape, true)
+        SetString('level.destructible-bot.weapon',"weapon-name", true)
+        SetFloat('level.destructible-bot.damage',damage, true)
     end 
 end
 
-
-function draw()
-
-	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-	UiPush()
-    	UiAlign("center middle")
-    	UiTranslate(UiCenter(), UiMiddle());
-    	UiImage("circle/crosshair-dot.png")
-  	UiPop()
-end
-
-	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        UiAlign("center")
-        UiTranslate(UiCenter(),UiHeight()-60)
-        UiFont("regular.ttf", 30)
-        UiText("LMB - Fire, RMB - Extinguish")
-    end
-end+function server.init()
+        RegisterTool("magmatool", "Lava Gun", "MOD/vox/lavagun.vox")
+        SetBool("game.tool.magmatool.enabled", true, true)
+        SetFloat("game.tool.magmatool.ammo", 9999, true)
+        gravity = Vec(0, -5, 0)
+        velocity = 0
+       recoilTimer = 0
+       driftH = 0
+       driftV = 0
+        shakex = 0
+        shakey = 0
+        shakez = 0
+        damage = 1.8
+        fps = 60
+        lmbdown = true
+        fireamount = GetBool("savegame.mod.fireamount")
+        BurnSound = LoadLoop("MOD/snd/sizzle.ogg")
+        BeamSound = LoadLoop("MOD/snd/loop.ogg")
+        if fireamount then
+    		big = true
+        end
+        if big then
+        for i=1, 150 do
+            magma.shells[i] = deepcopy(magma.defaultShell)
+        end
+    end
+        if not big then
+        for i=1, 250 do
+            magma.shells[i] = deepcopy(magma.defaultShell)
+        end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(magma.shells) do
+            if shell.lifetime ~= 0 then
+                shell.lifetime = shell.lifetime - dt
+                MagmaOperations(shell)
+                local rot = QuatLookAt(shell.magmapos, GetCameraTransform().pos)
+                local transform = Transform(shell.magmapos, rot)
+                createMagmaParticle(shell.magmapos)
+            end
+        end
+    end
+end
+
+function client.init()
+    PewSound = LoadSound("MOD/snd/pew.ogg")
+    FinallySound = LoadSound("MOD/snd/finish.ogg")
+    EndSound = LoadSound("MOD/snd/end.ogg")
+    SmokeSound = LoadSound("MOD/snd/smoke.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputPressed("lmb") then
+               PlaySound(PewSound,GetCameraTransform().pos, 1.5)
+            end
+        end
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputDown("lmb") then
+            lmbdown = true
+        else
+            lmbdown = false
+        end
+    end
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputDown("lmb") then
+                Shoot()
+                laserBeam()
+                shooting2()
+           end
+        end
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputReleased("lmb") then
+               PlaySound(EndSound, GetCameraTransform().pos, 0.4, false)           
+               end
+        end
+    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+        if InputPressed("rmb") then
+        clearAllFires()
+    end
+    end
+    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+        if InputPressed("rmb") then
+            for key, shell in ipairs(magma.shells) do
+            if shell.lifetime ~= 0 then
+            shell.lifetime = shell.lifetime - dt
+                shell.lifetime = 0
+                createSmokeParticle(shell.magmapos)
+                PlaySound(SmokeSound,GetCameraTransform().pos, 1.5)
+    end
+    end
+    end
+    end
+    	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+
+                    if InputDown("lmb") then
+                    shakex = math.random(-5, 5)/350
+                    shakey = math.random(-5, 5)/350
+                    shakez = math.random(-5, 5)/350
+                    end
+
+    		local t = Transform()
+    		t.pos = Vec(0.3+shakex, -1.0+shakey, -0.40+shakez) --change the last three values to change vhere bullets originate left/right, up/down, forward,back
+    		t.rot = QuatEuler(-3, 0, 0)
+                    SetToolTransform(t)
+    end
+end
+
+function client.draw()
+    	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+        	UiAlign("center middle")
+        	UiTranslate(UiCenter(), UiMiddle());
+        	UiImage("circle/crosshair-dot.png")
+      	UiPop()
+    end
+
+    	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            UiAlign("center")
+            UiTranslate(UiCenter(),UiHeight()-60)
+            UiFont("regular.ttf", 30)
+            UiText("LMB - Fire, RMB - Extinguish")
+        end
+end
+

```

---

# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,62 +1,4 @@
-magma = {
-    shellNum = 1,
-    shells = {},
-    defaultShell = {
-        lifetime = 0
-    },
-}
-
-MKQue = {}
-
-laserSprite = LoadSprite("gfx/laser.png")
-muzzleflash = LoadSprite("gfx/glare.png")
-
-function init()
-    RegisterTool("magmatool", "Lava Gun", "MOD/vox/lavagun.vox")
-    SetBool("game.tool.magmatool.enabled", true)
-    SetFloat("game.tool.magmatool.ammo", 9999)
-
-    gravity = Vec(0, -5, 0)
-    velocity = 0
-
-   recoilTimer = 0
-   driftH = 0
-   driftV = 0
-  
-    shakex = 0
-    shakey = 0
-    shakez = 0
-
-    damage = 1.8
-    fps = 60
-    
-    lmbdown = true
-    fireamount = GetBool("savegame.mod.fireamount")
-    
-    BurnSound = LoadLoop("MOD/snd/sizzle.ogg")
-    BeamSound = LoadLoop("MOD/snd/loop.ogg")
-    PewSound = LoadSound("MOD/snd/pew.ogg")
-    FinallySound = LoadSound("MOD/snd/finish.ogg")
-    EndSound = LoadSound("MOD/snd/end.ogg")
-    SmokeSound = LoadSound("MOD/snd/smoke.ogg")
-
-    if fireamount then
-		big = true
-    end
-
-    if big then
-    for i=1, 150 do
-        magma.shells[i] = deepcopy(magma.defaultShell)
-    end
-end
-
-    if not big then
-    for i=1, 250 do
-        magma.shells[i] = deepcopy(magma.defaultShell)
-    end
-end
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -161,7 +103,6 @@
         ParticleEmissive(0)
 SpawnParticle("smoke", at, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.5, 0.5)
 end
-
 
 function createMagmaParticle(at)
     local val = math.random()
@@ -307,7 +248,7 @@
 
 function randomVec(t)
 	return Vec(random(-t, t), random(-t, t), random(-t, t))
-end 
+end
 
 function lookpos()
   local t = GetCameraTransform()
@@ -319,7 +260,7 @@
     else
       return false
     end
-end  
+end
 
 function shooting2()
   if lookpos() then
@@ -343,81 +284,6 @@
 	end
 end
 
-function tick(dt)
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputPressed("lmb") then
-           PlaySound(PewSound,GetCameraTransform().pos, 1.5)
-        end
-    end
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputDown("lmb") then
-        lmbdown = true
-    else
-        lmbdown = false
-    end
-end
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputDown("lmb") then
-            Shoot()
-            laserBeam()
-            shooting2()
-       end
-    end
-
-    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        if InputReleased("lmb") then
-           PlaySound(EndSound, GetCameraTransform().pos, 0.4, false)           
-           end
-    end
-
-
-if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-    if InputPressed("rmb") then
-    clearAllFires()
-end
-end
-
-if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-    if InputPressed("rmb") then
-        for key, shell in ipairs(magma.shells) do
-        if shell.lifetime > 0 then
-        shell.lifetime = shell.lifetime - dt
-            shell.lifetime = 0
-            createSmokeParticle(shell.magmapos)
-            PlaySound(SmokeSound,GetCameraTransform().pos, 1.5)
-end
-end
-end
-end
-
-    for key, shell in ipairs(magma.shells) do
-        if shell.lifetime > 0 then
-            shell.lifetime = shell.lifetime - dt
-            MagmaOperations(shell)
-            local rot = QuatLookAt(shell.magmapos, GetCameraTransform().pos)
-            local transform = Transform(shell.magmapos, rot)
-            createMagmaParticle(shell.magmapos)
-        end
-    end
-
-	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-
-                if InputDown("lmb") then
-                shakex = math.random(-5, 5)/350
-                shakey = math.random(-5, 5)/350
-                shakez = math.random(-5, 5)/350
-                end
-				
-		local t = Transform()
-		t.pos = Vec(0.3+shakex, -1.0+shakey, -0.40+shakez) --change the last three values to change vhere bullets originate left/right, up/down, forward,back
-		t.rot = QuatEuler(-3, 0, 0)
-                SetToolTransform(t)
-end
-end
-
 function destructiblerobots(pos,damage,hitcounter) --thanks dima
     local hit, point, n, shape = QueryClosestPoint(pos, 0.3)
 	if HasTag(shape, "shapeHealth") then
@@ -427,28 +293,139 @@
 	end
 
     if hit then 
-        SetFloat('level.destructible-bot.hitCounter',hitcounter)
-        SetInt('level.destructible-bot.hitShape',shape)
-        SetString('level.destructible-bot.weapon',"weapon-name")
-        SetFloat('level.destructible-bot.damage',damage)
+        SetFloat('level.destructible-bot.hitCounter',hitcounter, true)
+        SetInt('level.destructible-bot.hitShape',shape, true)
+        SetString('level.destructible-bot.weapon',"weapon-name", true)
+        SetFloat('level.destructible-bot.damage',damage, true)
     end 
 end
 
-
-function draw()
-
-	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-	UiPush()
-    	UiAlign("center middle")
-    	UiTranslate(UiCenter(), UiMiddle());
-    	UiImage("circle/crosshair-dot.png")
-  	UiPop()
-end
-
-	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle() == 0 then
-        UiAlign("center")
-        UiTranslate(UiCenter(),UiHeight()-60)
-        UiFont("regular.ttf", 30)
-        UiText("LMB - Fire, RMB - Extinguish")
-    end
-end+function server.init()
+        RegisterTool("magmatool", "Lava Gun", "MOD/vox/lavagun.vox")
+        SetBool("game.tool.magmatool.enabled", true, true)
+        SetFloat("game.tool.magmatool.ammo", 9999, true)
+        gravity = Vec(0, -5, 0)
+        velocity = 0
+       recoilTimer = 0
+       driftH = 0
+       driftV = 0
+        shakex = 0
+        shakey = 0
+        shakez = 0
+        damage = 1.8
+        fps = 60
+        lmbdown = true
+        fireamount = GetBool("savegame.mod.fireamount")
+        BurnSound = LoadLoop("MOD/snd/sizzle.ogg")
+        BeamSound = LoadLoop("MOD/snd/loop.ogg")
+        if fireamount then
+    		big = true
+        end
+        if big then
+        for i=1, 150 do
+            magma.shells[i] = deepcopy(magma.defaultShell)
+        end
+    end
+        if not big then
+        for i=1, 250 do
+            magma.shells[i] = deepcopy(magma.defaultShell)
+        end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(magma.shells) do
+            if shell.lifetime ~= 0 then
+                shell.lifetime = shell.lifetime - dt
+                MagmaOperations(shell)
+                local rot = QuatLookAt(shell.magmapos, GetCameraTransform().pos)
+                local transform = Transform(shell.magmapos, rot)
+                createMagmaParticle(shell.magmapos)
+            end
+        end
+    end
+end
+
+function client.init()
+    PewSound = LoadSound("MOD/snd/pew.ogg")
+    FinallySound = LoadSound("MOD/snd/finish.ogg")
+    EndSound = LoadSound("MOD/snd/end.ogg")
+    SmokeSound = LoadSound("MOD/snd/smoke.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputPressed("lmb") then
+               PlaySound(PewSound,GetCameraTransform().pos, 1.5)
+            end
+        end
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputDown("lmb") then
+            lmbdown = true
+        else
+            lmbdown = false
+        end
+    end
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputDown("lmb") then
+                Shoot()
+                laserBeam()
+                shooting2()
+           end
+        end
+        if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            if InputReleased("lmb") then
+               PlaySound(EndSound, GetCameraTransform().pos, 0.4, false)           
+               end
+        end
+    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+        if InputPressed("rmb") then
+        clearAllFires()
+    end
+    end
+    if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+        if InputPressed("rmb") then
+            for key, shell in ipairs(magma.shells) do
+            if shell.lifetime ~= 0 then
+            shell.lifetime = shell.lifetime - dt
+                shell.lifetime = 0
+                createSmokeParticle(shell.magmapos)
+                PlaySound(SmokeSound,GetCameraTransform().pos, 1.5)
+    end
+    end
+    end
+    end
+    	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+
+                    if InputDown("lmb") then
+                    shakex = math.random(-5, 5)/350
+                    shakey = math.random(-5, 5)/350
+                    shakez = math.random(-5, 5)/350
+                    end
+
+    		local t = Transform()
+    		t.pos = Vec(0.3+shakex, -1.0+shakey, -0.40+shakez) --change the last three values to change vhere bullets originate left/right, up/down, forward,back
+    		t.rot = QuatEuler(-3, 0, 0)
+                    SetToolTransform(t)
+    end
+end
+
+function client.draw()
+    	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+        	UiAlign("center middle")
+        	UiTranslate(UiCenter(), UiMiddle());
+        	UiImage("circle/crosshair-dot.png")
+      	UiPop()
+    end
+
+    	if GetString("game.player.tool") == "magmatool" and GetPlayerVehicle(playerId) == 0 then
+            UiAlign("center")
+            UiTranslate(UiCenter(),UiHeight()-60)
+            UiFont("regular.ttf", 30)
+            UiText("LMB - Fire, RMB - Extinguish")
+        end
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
@@ -1,38 +1,40 @@
-function init()
-	fireamount = GetBool("savegame.mod.fireamount")
-	if fireamount == 0 then fireamount = 0.15 end
+#version 2
+function server.init()
+    fireamount = GetBool("savegame.mod.fireamount")
+    if fireamount == 0 then fireamount = 0.15 end
 end
 
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
 
-	UiFont("bold.ttf", 48)
-	UiText("Lava Gun Customization Service")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Weapon Settings")
-		UiTranslate(0, 40)
-		UiAlign("center middle")
-		UiColor(0.5, 0.8, 1)
-		if fireamount then
-			if UiTextButton("More Fire", 0, 20) then
-				fireamount = false
-				SetBool("savegame.mod.fireamount", fireamount)
-			end
-		else
-			if UiTextButton("More Lava", 0, 20) then
-				fireamount = true
-				SetBool("savegame.mod.fireamount", fireamount)
-			end
-		end
-	UiPop()
+    UiFont("bold.ttf", 48)
+    UiText("Lava Gun Customization Service")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Weapon Settings")
+    	UiTranslate(0, 40)
+    	UiAlign("center middle")
+    	UiColor(0.5, 0.8, 1)
+    	if fireamount then
+    		if UiTextButton("More Fire", 0, 20) then
+    			fireamount = false
+    			SetBool("savegame.mod.fireamount", fireamount, true)
+    		end
+    	else
+    		if UiTextButton("More Lava", 0, 20) then
+    			fireamount = true
+    			SetBool("savegame.mod.fireamount", fireamount, true)
+    		end
+    	end
+    UiPop()
 
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-		
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)		
-	end	
-end+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)		
+    end	
+end
+

```
