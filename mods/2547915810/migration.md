# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,34 +1,20 @@
-function init()
-	RegisterTool("lightsaber", "Lightsaber", "MOD/vox/lightsaber.vox")
-	SetBool("game.tool.lightsaber.enabled", true)
-	SetFloat("game.tool.lightsaber.ammo", 101)
-
-	smashTimer = 0
-	soundtimer = 0
-	spinsmash = false
-
-        hitwallsound = LoadSound("MOD/snd/hitwall0.ogg")
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
@@ -39,168 +25,185 @@
 	if soundtimer == 0 then soundtimer = 0.05 end
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "lightsaber" and GetPlayerVehicle() == 0 then
-		SetPlayerHealth(1)
-
-		if InputPressed("lmb") then
-			Smash()
-		end
-
-		if InputPressed("rmb") then
-			spinsmash = true
-			Smash()
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local offset = Transform(Vec(0.4, -0.9, -0.9), QuatEuler(56, -5, 0))
-			SetToolTransform(offset)
-
-			tipPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.05, -0.05, -2.7))
-			PointLight(tipPos, 0.1, 0.47, 1, 1.5)
-
-			if smashTimer > 0 then
-				if spinsmash then
-					local t = Transform()
-					t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
-					t.rot = QuatEuler(90, 170, -90)
-					SetToolTransform(t)
-                                        SpawnFire(tipPos)
-                                        MakeHole(tipPos, 0.4, 0.4, 0.4)
-				else
-					local t = Transform()
-					t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
-					t.rot = QuatEuler(-smashTimer*500, smashTimer*350, 0)
-					SetToolTransform(t)
-                                        SpawnFire(tipPos)
-                                        MakeHole(tipPos, 0.4, 0.4, 0.4)
-				end
-			end
-
-			if InputDown("lmb") and smashTimer == 0 then
-				local t = Transform()
-				t.pos = Vec(0.3, -0.6, -0.95)
-				t.rot = QuatEuler(5, 5, 0)
-				SetToolTransform(t)
-                                SpawnFire(tipPos)
-                                MakeHole(tipPos, 0.4, 0.4, 0.4)
-                                
-			end
-		end
-
-		if smashTimer > 0 then
-			smashTimer = smashTimer - dt
-			if smashTimer < 0.0001 then
-				PlaySound(swingsound, GetPlayerTransform().pos, 0.6)
-				local holeposes = {}
-				local hitcount = 0
-				for i=1, 16 do
-					local inc = 0.2*i
-
-					local meleedist = 3.6
-					if i < 6 or i > 10 then meleedist = meleedist * 0.95 end
-					if i < 5 or i > 11 then meleedist = meleedist * 0.95 end
-					if i < 4 or i > 12 then meleedist = meleedist * 0.95 end
-					if i < 3 or i > 13 then meleedist = meleedist * 0.95 end
-					if i < 2 or i > 14 then meleedist = meleedist * 0.95 end
-					local vec = spinsmash and Vec(-1.5+inc, 0, -meleedist) or Vec(0, -1.3+inc, -meleedist)
-
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
-                                                SpawnParticle("smoke", tipPos, Vec(0, 0.1+math.random(1,10)*0.1, 0), 0.3, 3)
-                                                PlaySound(hitwallsound, GetPlayerTransform().pos, 0.3)
-                                                PointLight(tipPos, 1, 0.2, 0, 2)
-
-                                                ParticleReset()
-			ParticleGravity(-7)
-			ParticleRadius(0.05)
-			ParticleColor(0.6, 0.6, 0.6)
-			ParticleTile(6)
-			ParticleDrag(0, 0.7)
-			ParticleCollide(0, 1, "easeout")
-		        ParticleRotation(3, 0)
-		        ParticleAlpha(1)
-			SpawnParticle(tipPos, Vec(-0.5+math.random(-5,10)*0.1, 0.1+math.random(1,10)*0.1, -0.5+math.random(-5,10)*0.1), 15)
-
-                                                ParticleReset()
-			ParticleGravity(-6)
-			ParticleRadius(0.15, 0.0, "smooth")
-			ParticleColor(0.8, 0.8, 0.8)
-			ParticleTile(3)
-			ParticleDrag(0, 0.7)
-		        ParticleRotation(4, 1)
-                        ParticleStretch(200.0)
-                        ParticleAlpha(0.8, 0.0)
-                        ParticleCollide(1, 1, "constant", 0.05)
-			SpawnParticle(tipPos, Vec(-0.5+math.random(-5,10)*0.1, 0.2+math.random(2,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
-
-                                                ParticleReset()
-			ParticleGravity(-5)
-			ParticleRadius(0.03)
-			ParticleColor(0.6, 0.6, 0.6)
-			ParticleTile(6)
-			ParticleDrag(0, 0.7)
-                        ParticleRotation(-5, 0)
-                        ParticleCollide(1, 1, "constant", 0.05)
-		        ParticleAlpha(1)
-			SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.2+math.random(2,10)*0.1, -0.5+math.random(-5,10)*0.1), 15)
-
-                                                ParticleReset()
-			ParticleEmissive(1, 0, "easein")
-			ParticleGravity(-4)
-			ParticleRadius(0.3, 0.0, "smooth")
-			ParticleColor(1,0.7,0.5, 1,.1,0)
-			ParticleTile(8)
-			ParticleDrag(0, 0.7)
-                        ParticleStretch(100.0)
-                        ParticleCollide(1, 1, "constant", 0.05)
-			SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.3+math.random(3,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
-
-                                                ParticleReset()
-			ParticleEmissive(2, 0, "easein")
-			ParticleGravity(-3)
-			ParticleRadius(0.02, 0.0, "smooth")
-			ParticleColor(1,0.8,0.6, 1,.0,0)
-			ParticleTile(4)
-			ParticleDrag(0, 0.7)
-                        ParticleStretch(1.5)
-                        ParticleCollide(1, 1, "constant", 0.05)
-			SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.3+math.random(3,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
-
-                                                ParticleReset()
-			ParticleEmissive(2, 0, "easein")
-			ParticleGravity(-4)
-			ParticleRadius(0.02, 0.0, "smooth")
-			ParticleColor(1,0.6,0.6, 1,.0,0)
-			ParticleTile(4)
-			ParticleDrag(0, 0.7)
-                        ParticleStretch(1.5)
-                        ParticleCollide(1, 1, "constant", 0.05)
-			SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.3+math.random(3,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
-
-
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
-end+function server.init()
+    RegisterTool("lightsaber", "Lightsaber", "MOD/vox/lightsaber.vox")
+    SetBool("game.tool.lightsaber.enabled", true, true)
+    SetFloat("game.tool.lightsaber.ammo", 101, true)
+    smashTimer = 0
+    soundtimer = 0
+    spinsmash = false
+    hitsound = LoadLoop("MOD/snd/hitloop.ogg")
+end
+
+function client.init()
+           hitwallsound = LoadSound("MOD/snd/hitwall0.ogg")
+    swingsound = LoadSound("MOD/snd/swing0.ogg")
+    saberonsound = LoadSound("MOD/snd/saberon.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "lightsaber" and GetPlayerVehicle(playerId) == 0 then
+    	SetPlayerHealth(playerId, 1)
+
+    	if InputPressed("lmb") then
+    		Smash()
+    	end
+
+    	if InputPressed("rmb") then
+    		spinsmash = true
+    		Smash()
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local offset = Transform(Vec(0.4, -0.9, -0.9), QuatEuler(56, -5, 0))
+    		SetToolTransform(offset)
+
+    		tipPos = TransformToParentPoint(GetBodyTransform(b), Vec(0.05, -0.05, -2.7))
+    		PointLight(tipPos, 0.1, 0.47, 1, 1.5)
+
+    		if smashTimer ~= 0 then
+    			if spinsmash then
+    				local t = Transform()
+    				t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
+    				t.rot = QuatEuler(90, 170, -90)
+    				SetToolTransform(t)
+                                           SpawnFire(tipPos)
+                                           MakeHole(tipPos, 0.4, 0.4, 0.4)
+    			else
+    				local t = Transform()
+    				t.pos = Vec(0.3, -0.6, -0.85+smashTimer*2)
+    				t.rot = QuatEuler(-smashTimer*500, smashTimer*350, 0)
+    				SetToolTransform(t)
+                                           SpawnFire(tipPos)
+                                           MakeHole(tipPos, 0.4, 0.4, 0.4)
+    			end
+    		end
+
+    		if InputDown("lmb") and smashTimer == 0 then
+    			local t = Transform()
+    			t.pos = Vec(0.3, -0.6, -0.95)
+    			t.rot = QuatEuler(5, 5, 0)
+    			SetToolTransform(t)
+                                   SpawnFire(tipPos)
+                                   MakeHole(tipPos, 0.4, 0.4, 0.4)
+
+    		end
+    	end
+
+    	if smashTimer ~= 0 then
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
+                                                   SpawnParticle("smoke", tipPos, Vec(0, 0.1+math.random(1,10)*0.1, 0), 0.3, 3)
+                                                   PlaySound(hitwallsound, GetPlayerTransform(playerId).pos, 0.3)
+                                                   PointLight(tipPos, 1, 0.2, 0, 2)
+
+                                                   ParticleReset()
+    		ParticleGravity(-7)
+    		ParticleRadius(0.05)
+    		ParticleColor(0.6, 0.6, 0.6)
+    		ParticleTile(6)
+    		ParticleDrag(0, 0.7)
+    		ParticleCollide(0, 1, "easeout")
+    	        ParticleRotation(3, 0)
+    	        ParticleAlpha(1)
+    		SpawnParticle(tipPos, Vec(-0.5+math.random(-5,10)*0.1, 0.1+math.random(1,10)*0.1, -0.5+math.random(-5,10)*0.1), 15)
+
+                                                   ParticleReset()
+    		ParticleGravity(-6)
+    		ParticleRadius(0.15, 0.0, "smooth")
+    		ParticleColor(0.8, 0.8, 0.8)
+    		ParticleTile(3)
+    		ParticleDrag(0, 0.7)
+    	        ParticleRotation(4, 1)
+                           ParticleStretch(200.0)
+                           ParticleAlpha(0.8, 0.0)
+                           ParticleCollide(1, 1, "constant", 0.05)
+    		SpawnParticle(tipPos, Vec(-0.5+math.random(-5,10)*0.1, 0.2+math.random(2,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
+
+                                                   ParticleReset()
+    		ParticleGravity(-5)
+    		ParticleRadius(0.03)
+    		ParticleColor(0.6, 0.6, 0.6)
+    		ParticleTile(6)
+    		ParticleDrag(0, 0.7)
+                           ParticleRotation(-5, 0)
+                           ParticleCollide(1, 1, "constant", 0.05)
+    	        ParticleAlpha(1)
+    		SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.2+math.random(2,10)*0.1, -0.5+math.random(-5,10)*0.1), 15)
+
+                                                   ParticleReset()
+    		ParticleEmissive(1, 0, "easein")
+    		ParticleGravity(-4)
+    		ParticleRadius(0.3, 0.0, "smooth")
+    		ParticleColor(1,0.7,0.5, 1,.1,0)
+    		ParticleTile(8)
+    		ParticleDrag(0, 0.7)
+                           ParticleStretch(100.0)
+                           ParticleCollide(1, 1, "constant", 0.05)
+    		SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.3+math.random(3,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
+
+                                                   ParticleReset()
+    		ParticleEmissive(2, 0, "easein")
+    		ParticleGravity(-3)
+    		ParticleRadius(0.02, 0.0, "smooth")
+    		ParticleColor(1,0.8,0.6, 1,.0,0)
+    		ParticleTile(4)
+    		ParticleDrag(0, 0.7)
+                           ParticleStretch(1.5)
+                           ParticleCollide(1, 1, "constant", 0.05)
+    		SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.3+math.random(3,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
+
+                                                   ParticleReset()
+    		ParticleEmissive(2, 0, "easein")
+    		ParticleGravity(-4)
+    		ParticleRadius(0.02, 0.0, "smooth")
+    		ParticleColor(1,0.6,0.6, 1,.0,0)
+    		ParticleTile(4)
+    		ParticleDrag(0, 0.7)
+                           ParticleStretch(1.5)
+                           ParticleCollide(1, 1, "constant", 0.05)
+    		SpawnParticle(tipPos, Vec(-0.4+math.random(-4,10)*0.1, 0.3+math.random(3,10)*0.1, -0.4+math.random(-4,10)*0.1), 7)
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
