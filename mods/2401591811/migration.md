# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,29 +1,16 @@
-function init()
-	RegisterTool("dragonslayer", "Dragonslayer", "MOD/vox/dragonslayer.vox")
-	SetBool("game.tool.dragonslayer.enabled", true)
-	SetFloat("game.tool.dragonslayer.ammo", 101)
-
-	smashTimer = 0
-	soundtimer = 0
-	swingTimer = 0
-	spinsmash = false
-
-	clangsound = LoadSound("MOD/snd/clang.ogg")
-	spinsound = LoadLoop("MOD/snd/spinloop.ogg")
-end
-
+#version 2
 function Boost()
-	local pt = GetPlayerTransform()
+	local pt = GetPlayerTransform(playerId)
 	local d = TransformToParentVec(pt, Vec(0, 7.5, -2.5))
-	local vel = GetPlayerVelocity()
+	local vel = GetPlayerVelocity(playerId)
 	vel[2] = 0
 	vel = VecAdd(vel, d)
-	SetPlayerVelocity(vel)
+	SetPlayerVelocity(playerId, vel)
 end
 
 function Spin()
 	local ct = GetCameraTransform()
-	local pt = GetPlayerTransform()
+	local pt = GetPlayerTransform(playerId)
 
 	pt.pos[2] = pt.pos[2] + 1.8
 	ct.pos = pt.pos
@@ -34,69 +21,86 @@
 	if soundtimer == 0 then soundtimer = 0.05 end
 end
 
-function tick()
-	if GetString("game.player.tool") == "dragonslayer" and GetPlayerVehicle() == 0 then
-		SetPlayerHealth(1)
+function server.init()
+    RegisterTool("dragonslayer", "Dragonslayer", "MOD/vox/dragonslayer.vox")
+    SetBool("game.tool.dragonslayer.enabled", true, true)
+    SetFloat("game.tool.dragonslayer.ammo", 101, true)
+    smashTimer = 0
+    soundtimer = 0
+    swingTimer = 0
+    spinsmash = false
+    spinsound = LoadLoop("MOD/snd/spinloop.ogg")
+end
 
-		if InputPressed("lmb") then
-			if smashTimer == 0 then smashTimer = 0.1 end
-		end
+function client.init()
+    clangsound = LoadSound("MOD/snd/clang.ogg")
+end
 
-		if InputPressed("space") then Boost() end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "dragonslayer" and GetPlayerVehicle(playerId) == 0 then
+    	SetPlayerHealth(playerId, 1)
 
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.05, -0.55, 0), QuatEuler(80, -15, 0))
-			SetToolTransform(offset)
+    	if InputPressed("lmb") then
+    		if smashTimer == 0 then smashTimer = 0.1 end
+    	end
 
-			if smashTimer > 0 then
-				local t = Transform()
-				t.pos = Vec(0, 0, -smashTimer*3)
-				t.rot = QuatEuler(-smashTimer*50, smashTimer*100, 0)
-				SetToolTransform(t)
-			end
-		end
+    	if InputPressed("space") then Boost() end
 
-		if smashTimer > 0 then
-			smashTimer = smashTimer - GetTimeStep()
-			if smashTimer < 0.0001 then
-				playsound = false
-				for i=1, 3 do
-					local inc = 1.5*i
-					local holepos = TransformToParentPoint(GetCameraTransform(), Vec(0, 0, -inc))
-					MakeHole(holepos, 2, 1.75, 1.5)
-					local hit, point, normal, shape = QueryClosestPoint(holepos, 1.75)
-					if hit then
-						playsound = true
-					end
-				end
-				local soundpos = TransformToParentPoint(GetCameraTransform(), Vec(0, 0, -3))
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.05, -0.55, 0), QuatEuler(80, -15, 0))
+    		SetToolTransform(offset)
 
-				if not spinsmash then
-					local holepos4 = TransformToParentPoint(GetCameraTransform(), Vec(0, 1.5, -1.5))
-					local holepos5 = TransformToParentPoint(GetCameraTransform(), Vec(0, 1, -2.5))
-					MakeHole(holepos4, 2, 1.75, 1.5)
-					MakeHole(holepos5, 2, 1.75, 1.5)
-					if playsound then PlaySound(clangsound, soundpos, 0.65) end
-				end
-				smashTimer = 0
+    		if smashTimer ~= 0 then
+    			local t = Transform()
+    			t.pos = Vec(0, 0, -smashTimer*3)
+    			t.rot = QuatEuler(-smashTimer*50, smashTimer*100, 0)
+    			SetToolTransform(t)
+    		end
+    	end
 
-				if spinsmash and soundtimer > 0 then
-					soundtimer = soundtimer - GetTimeStep()
-					if soundtimer < 0.0001 then
-						if playsound then PlaySound(clangsound, soundpos, 0.65) end
-						soundtimer = 0
-					end
-				end
-			end
-		end
+    	if smashTimer ~= 0 then
+    		smashTimer = smashTimer - GetTimeStep()
+    		if smashTimer < 0.0001 then
+    			playsound = false
+    			for i=1, 3 do
+    				local inc = 1.5*i
+    				local holepos = TransformToParentPoint(GetCameraTransform(), Vec(0, 0, -inc))
+    				MakeHole(holepos, 2, 1.75, 1.5)
+    				local hit, point, normal, shape = QueryClosestPoint(holepos, 1.75)
+    				if hit then
+    					playsound = true
+    				end
+    			end
+    			local soundpos = TransformToParentPoint(GetCameraTransform(), Vec(0, 0, -3))
 
-		if InputDown("rmb") then
-			Spin()
-			PlayLoop(spinsound)
-			spinsmash = true
-		else
-			spinsmash = false
-		end
-	end
-end+    			if not spinsmash then
+    				local holepos4 = TransformToParentPoint(GetCameraTransform(), Vec(0, 1.5, -1.5))
+    				local holepos5 = TransformToParentPoint(GetCameraTransform(), Vec(0, 1, -2.5))
+    				MakeHole(holepos4, 2, 1.75, 1.5)
+    				MakeHole(holepos5, 2, 1.75, 1.5)
+    				if playsound then PlaySound(clangsound, soundpos, 0.65) end
+    			end
+    			smashTimer = 0
+
+    			if spinsmash and soundtimer ~= 0 then
+    				soundtimer = soundtimer - GetTimeStep()
+    				if soundtimer < 0.0001 then
+    					if playsound then PlaySound(clangsound, soundpos, 0.65) end
+    					soundtimer = 0
+    				end
+    			end
+    		end
+    	end
+
+    	if InputDown("rmb") then
+    		Spin()
+    		PlayLoop(spinsound)
+    		spinsmash = true
+    	else
+    		spinsmash = false
+    	end
+    end
+end
+

```
