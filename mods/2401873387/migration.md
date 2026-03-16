# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,33 +1,20 @@
-function init()
-	RegisterTool("lightkatana", "Lightkatana", "MOD/vox/lightkatana.vox")
-	SetBool("game.tool.lightkatana.enabled", true)
-	SetFloat("game.tool.lightkatana.ammo", 101)
-
-	smashTimer = 0
-	soundtimer = 0
-	spinsmash = false
-
-	swingsound = LoadSound("MOD/snd/swing0.ogg")
-	hitsound = LoadLoop("MOD/snd/hitloop.ogg")
-	saberonsound = LoadSound("MOD/snd/saberon.ogg")
-end
-
+#version 2
 function Smash()
 	if smashTimer == 0 then smashTimer = 0.1 end
 end
 
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
@@ -38,93 +25,110 @@
 	if soundtimer == 0 then soundtimer = 0.05 end
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "lightkatana" and GetPlayerVehicle() == 0 then
-		SetPlayerHealth(1)
+function server.init()
+    RegisterTool("lightkatana", "Lightkatana", "MOD/vox/lightkatana.vox")
+    SetBool("game.tool.lightkatana.enabled", true, true)
+    SetFloat("game.tool.lightkatana.ammo", 101, true)
+    smashTimer = 0
+    soundtimer = 0
+    spinsmash = false
+    hitsound = LoadLoop("MOD/snd/hitloop.ogg")
+end
 
-		if InputPressed("space") then Boost() end
+function client.init()
+    swingsound = LoadSound("MOD/snd/swing0.ogg")
+    saberonsound = LoadSound("MOD/snd/saberon.ogg")
+end
 
-		if InputPressed("lmb") then
-			Smash()
-		end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "lightkatana" and GetPlayerVehicle(playerId) == 0 then
+    	SetPlayerHealth(playerId, 1)
 
-		if InputPressed("rmb") then
-			spinsmash = true
-			Smash()
-		end
+    	if InputPressed("space") then Boost() end
 
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.3, -0.7, -0.8), QuatEuler(60, -5, 0))
-			SetToolTransform(offset)
-			
-			tipPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.05, -0.05, -2.7))
-			PointLight(tipPos, 1, 0.1, 0.1, 0.5)
-			MakeHole(tipPos, 0.2, 0.2, 0.2)
+    	if InputPressed("lmb") then
+    		Smash()
+    	end
 
-			if smashTimer > 0 then
-				if spinsmash then
-					local t = Transform()
-					t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
-					t.rot = QuatEuler(0, 60, -90)
-					SetToolTransform(t)
-				else
-					local t = Transform()
-					t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
-					t.rot = QuatEuler(-smashTimer*400, smashTimer*150, 0)
-					SetToolTransform(t)
-				end
-			end
+    	if InputPressed("rmb") then
+    		spinsmash = true
+    		Smash()
+    	end
 
-			if InputDown("lmb") and smashTimer == 0 then
-				local t = Transform()
-				t.pos = Vec(0.3, -0.6, -0.95)
-				t.rot = QuatEuler(5, 5, 0)
-				SetToolTransform(t)
-			end
-		end
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.3, -0.7, -0.8), QuatEuler(60, -5, 0))
+    		SetToolTransform(offset)
 
-		if smashTimer > 0 then
-			smashTimer = smashTimer - dt
-			if smashTimer < 0.0001 then
-				PlaySound(swingsound, GetPlayerTransform().pos, 0.6)
-				local holeposes = {}
-				local hitcount = 0
-				for i=1, 16 do
-					local inc = 0.2*i
+    		tipPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.05, -0.05, -2.7))
+    		PointLight(tipPos, 1, 0.1, 0.1, 0.5)
+    		MakeHole(tipPos, 0.2, 0.2, 0.2)
 
-					local meleedist = 3.6
-					if i < 6 or i > 10 then meleedist = meleedist * 0.95 end
-					if i < 5 or i > 11 then meleedist = meleedist * 0.95 end
-					if i < 4 or i > 12 then meleedist = meleedist * 0.95 end
-					if i < 3 or i > 13 then meleedist = meleedist * 0.95 end
-					if i < 2 or i > 14 then meleedist = meleedist * 0.95 end
-					local vec = spinsmash and Vec(-1.5+inc, 0, -meleedist) or Vec(0, -1.3+inc, -meleedist)
+    		if smashTimer ~= 0 then
+    			if spinsmash then
+    				local t = Transform()
+    				t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
+    				t.rot = QuatEuler(0, 60, -90)
+    				SetToolTransform(t)
+    			else
+    				local t = Transform()
+    				t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
+    				t.rot = QuatEuler(-smashTimer*400, smashTimer*150, 0)
+    				SetToolTransform(t)
+    			end
+    		end
 
-					local ct = GetCameraTransform()
-					local fwdpos = TransformToParentPoint(GetCameraTransform(), vec)
-					local direction = VecSub(fwdpos, ct.pos)
-					local distance = VecLength(direction)
-					local direction = VecNormalize(direction)
-					local hit, hitDistance = QueryRaycast(ct.pos, direction, distance)
-					
-					if hit then
-						hitcount = hitcount + 1
-						local vec2 = spinsmash and Vec(-1.5+inc, 0, -hitDistance) or Vec(0, -1.3+inc, -hitDistance)
+    		if InputDown("lmb") and smashTimer == 0 then
+    			local t = Transform()
+    			t.pos = Vec(0.3, -0.6, -0.95)
+    			t.rot = QuatEuler(5, 5, 0)
+    			SetToolTransform(t)
+    		end
+    	end
 
-						vec2 = VecScale(vec2, 1.03)
-						if i < 6 or i > 10 then vec2 = VecScale(vec2, 0.95) end
-						if i < 4 or i > 12 then vec2 = VecScale(vec2, 0.95) end
-						if i < 2 or i > 14 then vec2 = VecScale(vec2, 0.95) end
-						holeposes[hitcount] = TransformToParentPoint(GetCameraTransform(), vec2)
-					end
-				end
-				for i=1, #holeposes do
-					MakeHole(holeposes[i], 0.3, 0.3, 0.3)
-				end
-				smashTimer = 0
-				spinsmash = false
-			end
-		end
-	end
-end+    	if smashTimer ~= 0 then
+    		smashTimer = smashTimer - dt
+    		if smashTimer < 0.0001 then
+    			PlaySound(swingsound, GetPlayerTransform(playerId).pos, 0.6)
+    			local holeposes = {}
+    			local hitcount = 0
+    			for i=1, 16 do
+    				local inc = 0.2*i
+
+    				local meleedist = 3.6
+    				if i < 6 or i > 10 then meleedist = meleedist * 0.95 end
+    				if i < 5 or i > 11 then meleedist = meleedist * 0.95 end
+    				if i < 4 or i > 12 then meleedist = meleedist * 0.95 end
+    				if i < 3 or i > 13 then meleedist = meleedist * 0.95 end
+    				if i < 2 or i > 14 then meleedist = meleedist * 0.95 end
+    				local vec = spinsmash and Vec(-1.5+inc, 0, -meleedist) or Vec(0, -1.3+inc, -meleedist)
+
+    				local ct = GetCameraTransform()
+    				local fwdpos = TransformToParentPoint(GetCameraTransform(), vec)
+    				local direction = VecSub(fwdpos, ct.pos)
+    				local distance = VecLength(direction)
+    				local direction = VecNormalize(direction)
+    				local hit, hitDistance = QueryRaycast(ct.pos, direction, distance)
+
+    				if hit then
+    					hitcount = hitcount + 1
+    					local vec2 = spinsmash and Vec(-1.5+inc, 0, -hitDistance) or Vec(0, -1.3+inc, -hitDistance)
+
+    					vec2 = VecScale(vec2, 1.03)
+    					if i < 6 or i > 10 then vec2 = VecScale(vec2, 0.95) end
+    					if i < 4 or i > 12 then vec2 = VecScale(vec2, 0.95) end
+    					if i < 2 or i > 14 then vec2 = VecScale(vec2, 0.95) end
+    					holeposes[hitcount] = TransformToParentPoint(GetCameraTransform(), vec2)
+    				end
+    			end
+    			for i=1, #holeposes do
+    				MakeHole(holeposes[i], 0.3, 0.3, 0.3)
+    			end
+    			smashTimer = 0
+    			spinsmash = false
+    		end
+    	end
+    end
+end
+

```
