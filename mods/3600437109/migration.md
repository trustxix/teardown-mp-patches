# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,5 +1,4 @@
--- Nade Launcher script by Cyber
-
+#version 2
 local projectiles = {}
 local empty = true
 local semi = false
@@ -23,373 +22,8 @@
 local expand = 1
 local intensity = 600
 
-function init()
-	RegisterTool("Launcher", "Grenade Launcher", "MOD/vox/Launcher.vox")
-	SetBool("game.tool.Launcher.enabled", true)
-	SetFloat("game.tool.Launcher.ammo", 7)
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	norecoil = GetBool("savegame.mod.norecoil")
-	noreticle = GetBool("savegame.mod.noreticle")
-		
-	gunSnd = LoadSound("MOD/snd/gunsnd.ogg")
-	gunRev = LoadSound("MOD/snd/gunreverb.ogg")
-	gunRel = LoadSound("MOD/snd/reload.ogg")
-	gunLock = LoadSound("MOD/snd/lock.ogg")
-	gasSnd = LoadSound("MOD/snd/gasSnd.ogg")
-	imploSnd = LoadSound ("MOD/snd/imploSnd.ogg")
-	
-end
-
-function tick(dt)
-
-	delay = delay - dt
-	reltime = reltime - dt
-	recoiltime = recoiltime - dt
-	coolDown = coolDown - dt
-	implotime = implotime -dt
-	clustime = clustime -dt
-	cluster()
-	implode()
-		
-	if next(projectiles) == nil then
-		empty = true
-	else
-		empty = false
-	end
-	
-	if GetString("game.player.tool") == "Launcher" then	
-
-
-		if GetBool("game.thirdperson") then
-			local offset = Transform(Vec(0, -500, 0))
-			SetToolTransform(offset)
-			SetToolHandPoseLocalTransform(nil, nil)
-		else
-		--reload
-		if reltime > 1.25 then
-			if rerotate > -15 then
-				rerotate = rerotate - 0.5
-			end
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(rerotate, 0, 0))
-			SetToolTransform(offset)
-		elseif reltime > 0 and reltime < 1.25 then
-			if rerotate < 0 then
-				rerotate = rerotate + 0.5
-			end
-			local offset = Transform(Vec(0, 0, 0), QuatEuler(rerotate, 0, 0))
-			SetToolTransform(offset)
-		end
-			
-		end
-		if recoiltime > 0 then
-			local curpitch = GetPlayerPitch()
-			local nextpitch = curpitch + 5
-			SetPlayerPitch(nextpitch)
-			ShakeCamera(0.5)
-		end	
-		if delay > 0.22 then
-			recoilrotate = recoilrotate + 2
-			recoilrotateH = recoilrotate/12
-			local offset = Transform(Vec(0, 0, recoilrotateH), QuatEuler(recoilrotate, 0, 0))
-			SetToolTransform(offset)
-			--elseif reltime > 0 and reltime < 1.25 then
-			--if recoilrotate < 0 then
-				--recoilrotate = recoilrotate + 0.5
-			--end
-			--local offset = Transform(Vec(0, 0, 0), QuatEuler(recoilrotate, 0, 0))
-			--SetToolTransform(offset)
-		else
-			recoilrotate = 0
-		end
-		
-		if not rotime then
-			local b = GetToolBody()
-			local shapes = GetBodyShapes(b)
-
-			if b ~= body then
-				body = b
-				t0 = GetShapeLocalTransform(shapes[1])
-			end
-
-			t = TransformCopy(t0)
-			t.rot = QuatRotateQuat(QuatEuler(0, 0, 45), t.rot)
-			t.pos = VecAdd(t.pos, Vec(0.225,-0.12,0))
-			SetShapeLocalTransform(shapes[1], t)
-		elseif rotime then
-			local b = GetToolBody()
-			local shapes = GetBodyShapes(b)
-
-			if b ~= body then
-				body = b
-				t0 = GetShapeLocalTransform(shapes[1])
-			end
-
-			t = TransformCopy(t0)
-			t.rot = QuatRotateQuat(QuatEuler(0, 0, 0), t.rot)
-			t.pos = VecAdd(t.pos, Vec(0,0,0))
-			SetShapeLocalTransform(shapes[1], t)
-		end	
-		--
-	
-		if GetBool("game.player.canusetool") and InputDown("lmb") and semi == false and delay < 0 and ammo > 0 and not reloading then
-			if not unlimitedammo then
-				ammo = ammo - 1
-			end
-			delay = 0.3
-			semi = true
-			if not norecoil then
-				recoiltime = 0.05
-			end
-			if rotime == true then
-				rotime = false
-			else
-				rotime =  true
-			end
-					
-			local numbers = {-0.02, 0, 0.02}
-			local randomIndex = math.random(1, #numbers)
-			local r = numbers[randomIndex]
-			local cam_tr = GetCameraTransform()
-			local fwd = QuatRotateVec(cam_tr.rot, Vec(r, -0.2, -1.9)) 
-			local up  = QuatRotateVec(cam_tr.rot, Vec(0, 1, 0))   
-			local right = VecNormalize(VecCross(fwd, up))        
-
-			local forward_offset = VecScale(fwd, 1.0)
-			local right_offset   = VecScale(right, 0.4)  -- change 0.5 to move left/right
-			local start_pos = VecAdd(cam_tr.pos, VecAdd(forward_offset, right_offset))
-			
-			ParticleGravity(4)
-			ParticleRotation(.2)
-			ParticleRadius(0.3)
-			ParticleType("smoke")
-			ParticleCollide(0)
-			ParticleDrag(1)
-			ParticleColor(.5,.5,.6)
-			SpawnParticle(start_pos, VecAdd(0,0,0), 5.0)
-			
-			if ammoselect == 2 then
-					Shoot(start_pos, fwd, "shotgun")
-				PlaySound(gunLock)
-			end
-			
-			if ammoselect ~= 2 then
-				PlaySound(gunSnd)
-				local speed = 40.0
-				local vel = VecScale(fwd, speed)
-				
-				-- Add new projectile to the list
-				table.insert(projectiles, {
-					pos = VecCopy(start_pos),
-					prev_pos = VecCopy(start_pos),
-					vel = vel,
-					time = 0.0,  -- For timeout
-					max_time = 3.5  -- Max flight time in seconds before despawn
-				})
-			end
-		end	
-
-		if not InputDown("lmb") then
-			semi = false
-		end 
-		
-		if reltime > 0 then
-		reloading = true
-		ammo = 6
-		else
-			reloading = false
-		end
-		
-		if InputDown("r") and reltime < 0 and ammo < 6 then
-			reltime = 2.5
-			PlaySound(gunRel)
-		end
-		
-		if InputDown ("mmb") and not ammostop and empty then
-			ammostop = true
-			if ammoselect > 0 then
-				ammoselect = ammoselect - 1
-			else
-				ammoselect = 5
-			end
-		elseif not InputDown ("mmb") then
-			ammostop = false
-		end
-		if InputDown ("rmb") and not ammostopdown and empty then
-			ammostopdown = true
-			if ammoselect < 5 then
-				ammoselect = ammoselect + 1
-			else
-				ammoselect = 0
-			end
-		elseif not InputDown ("rmb") then
-			ammostopdown = false
-		end
-	end
-	
-	for i = #projectiles, 1, -1 do
-        local p = projectiles[i]
-        
-        p.time = p.time + dt
-        
-        -- Timeout check
-        if p.time > p.max_time then
-            table.remove(projectiles, i)
-        end
-		
-		--gravity
-		p.vel = VecAdd(p.vel, Vec(0, -9.81 * dt, 0))
-        
-        -- Update position
-        p.prev_pos = VecCopy(p.pos)
-        p.pos = VecAdd(p.pos, VecScale(p.vel, dt))
-        
-        -- Calculate movement vector this frame
-        local move_vec = VecSub(p.pos, p.prev_pos)
-        local move_len = VecLength(move_vec)
-        
-        if move_len > 0 then
-            local dir = VecScale(move_vec, 1 / move_len)
-            
-            -- Raycast to check for collision
-            local hit, dist, normal, shape = QueryRaycast(p.prev_pos, dir, move_len)
-            
-            if hit then
-                -- Calculate hit position
-                hit_pos = VecAdd(p.prev_pos, VecScale(dir, dist))
-                
-                -- Hit Effects
-				if ammoselect == 0 then -- HE
-					Explosion(hit_pos, 1.0) 
-				elseif ammoselect == 1 then  -- CLUSTER
-					Explosion(hit_pos, 0.7) 
-					clustime = 1.5
-				elseif ammoselect == 2 then  -- HORNETS
-					--Explosion(hit_pos, 0.5) 
-				elseif ammoselect == 3 then	-- FRAG
-					Explosion(hit_pos, 1.0) 
-					local cam = GetCameraTransform()          -- player view direction
-					local forward = QuatRotateVec(cam.rot, Vec(0,0,-1))
-					local up      = QuatRotateVec(cam.rot, Vec(0,1,0))
-
-					-- build a local right vector (forward × up)
-					local right = VecNormalize(VecCross(forward, up))
-
-					local spreadAngle = 80         -- max cone angle in degrees
-					local rad = math.rad(spreadAngle)
-
-					for i = 0, 15 do
-						local golden = 0.618033988749895  
-						local theta  = 2 * math.pi * (i * golden) % (2 * math.pi)
-
-						-- vertical offset inside the cone
-						local r = math.sqrt( (i + 0.5) / 16 )   
-						local pitch = math.asin(r) * rad
-
-						local sinPitch = math.sin(pitch)
-						local cosPitch = math.cos(pitch)
-
-						local dirX = math.cos(theta) * sinPitch * right[1] +
-									 math.sin(theta) * sinPitch * up[1] +
-									 cosPitch * forward[1]
-
-						local dirY = math.cos(theta) * sinPitch * right[2] +
-									 math.sin(theta) * sinPitch * up[2] +
-									 cosPitch * forward[2]
-
-						local dirZ = math.cos(theta) * sinPitch * right[3] +
-									 math.sin(theta) * sinPitch * up[3] +
-									 cosPitch * forward[3]
-
-						local dir = Vec(dirX, dirY, dirZ)
-					
-						Shoot(hit_pos, dir, "bullet")
-						Shoot(hit_pos, dir, "shotgun")
-					end	
-				elseif ammoselect == 4 then --CAUSTIC
-					local p = GetPlayerPos()
-					local a = hit_pos
-					local x = VecSub(p, a)
-					local px = VecLength(x)
-					
-					if px < 5 then
-							SetPlayerHealth(0.0)
-					end	
-					PlaySound(gasSnd, hit_pos, 1.0)
-					r = VecAdd (hit_pos, Vec(2, 0, 0))
-					MakeHole(r, 11.0, 10.0, 9.0)
-					MakeHole(r, 10.0, 9.0, 8.0)
-					MakeHole(r, 9.0, 8.0, 7.0)
-					Paint(r, 5.0, "spraycan", 1.0)
-					SpawnFire(r)
-					ParticleGravity(4)
-					ParticleRotation(.2)
-					ParticleRadius(4.0)
-					ParticleType("plain")
-					ParticleCollide(0)
-					ParticleDrag(1)
-					ParticleColor(1,1,0)
-					ParticleAlpha(5.0 , 0.0, smooth, .05)
-					r = VecAdd (hit_pos, Vec(4, 0, 0))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					r = VecAdd (hit_pos, Vec(0, 0, 4))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					ParticleRotation(-.2)
-					r = VecAdd (hit_pos, Vec(-4, 0, 0))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					r = VecAdd (hit_pos, Vec(0, 0, -4))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					r = VecAdd (hit_pos, Vec(0, 0, 0))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-				elseif ammoselect == 5 then -- IMPLOSION
-					r = VecAdd (hit_pos, Vec(2, 0, 0))
-					MakeHole(r, 11.0, 10.0, 9.0)
-					MakeHole(r, 10.0, 9.0, 8.0)
-					PlaySound(imploSnd, hit_pos, 5.0)
-					implotime = 1.0
-					intensity = 600
-					implode(hit_pos)
-					ParticleGravity(-4)
-					ParticleRotation(.2)
-					ParticleRadius(4.0)
-					ParticleType("plain")
-					ParticleCollide(0)
-					ParticleDrag(1)
-					ParticleColor(.5,.5,.6)
-					r = VecAdd (hit_pos, Vec(5, 0, 0))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					r = VecAdd (hit_pos, Vec(0, 0, 5))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					ParticleRotation(-.2)
-					r = VecAdd (hit_pos, Vec(-5, 0, 0))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					r = VecAdd (hit_pos, Vec(0, 0, -5))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					r = VecAdd (hit_pos, Vec(0, 0, 0))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-					ParticleRadius(1.0, 100.0)
-					r = VecAdd (hit_pos, Vec(0, 5, 0))
-					SpawnParticle(r, VecAdd(0,0,0), 5.0)
-				end	
-                
-                table.remove(projectiles, i)
-            else
-				ParticleRadius(0.2)
-				ParticleTile(9)
-				ParticleType("plain")
-				ParticleCollide(0)
-				ParticleDrag(1)
-				ParticleColor(.5,.5,.5)
-                if ammoselect == 5 then
-					PointLight(p.pos, 0, 0, 1, 10)
-				end
-				SpawnParticle(p.pos, VecAdd(0,0,0), 0.5)
-            end
-        end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "Launcher" and GetPlayerVehicle() == 0 then
+unction draw()
+	if GetString("game.player.tool") == "Launcher" and GetPlayerVehicle(playerId) == 0 then
 		UiPush()
 			UiTranslate(UiCenter(), UiHeight()-60)
 			UiAlign("center middle")
@@ -436,7 +70,7 @@
 	end
 end
 
-function cluster()
+unction cluster()
 	if clustime > 0.5 and clustime < 1.3 and hit_pos ~= 0 then
 		local rx = math.random(-expand, expand)
 		local ry = math.random(-expand, expand)
@@ -451,11 +85,11 @@
 	end
 end
 
-function implode()
+unction implode()
 	if implotime > 0 and hit_pos ~= 0 then
 		local hitv = hit_pos
 		local r = VecAdd (hitv, Vec(0, 5, 0))
-		if intensity > 0 then
+		if intensity ~= 0 then
 			intensity = intensity - 15
 		end	
 		PointLight(r, 0, 0, 1, intensity)
@@ -480,4 +114,369 @@
 			end
 		end
 	end
-end+end
+
+function server.init()
+    RegisterTool("Launcher", "Grenade Launcher", "MOD/vox/Launcher.vox")
+    SetBool("game.tool.Launcher.enabled", true, true)
+    SetFloat("game.tool.Launcher.ammo", 7, true)
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    norecoil = GetBool("savegame.mod.norecoil")
+    noreticle = GetBool("savegame.mod.noreticle")
+end
+
+function server.tick(dt)
+    delay = delay - dt
+    reltime = reltime - dt
+    recoiltime = recoiltime - dt
+    coolDown = coolDown - dt
+    implotime = implotime -dt
+    clustime = clustime -dt
+    cluster()
+    implode()
+    if next(projectiles) == nil then
+    	empty = true
+    else
+    	empty = false
+    end
+end
+
+function client.init()
+    gunSnd = LoadSound("MOD/snd/gunsnd.ogg")
+    gunRev = LoadSound("MOD/snd/gunreverb.ogg")
+    gunRel = LoadSound("MOD/snd/reload.ogg")
+    gunLock = LoadSound("MOD/snd/lock.ogg")
+    gasSnd = LoadSound("MOD/snd/gasSnd.ogg")
+    imploSnd = LoadSound ("MOD/snd/imploSnd.ogg")
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "Launcher" then	
+
+    	if GetBool("game.thirdperson") then
+    		local offset = Transform(Vec(0, -500, 0))
+    		SetToolTransform(offset)
+    		SetToolHandPoseLocalTransform(nil, nil)
+    	else
+    	--reload
+    	if reltime > 1.25 then
+    		if rerotate > -15 then
+    			rerotate = rerotate - 0.5
+    		end
+    		local offset = Transform(Vec(0, 0, 0), QuatEuler(rerotate, 0, 0))
+    		SetToolTransform(offset)
+    	elseif reltime > 0 and reltime < 1.25 then
+    		if rerotate < 0 then
+    			rerotate = rerotate + 0.5
+    		end
+    		local offset = Transform(Vec(0, 0, 0), QuatEuler(rerotate, 0, 0))
+    		SetToolTransform(offset)
+    	end
+
+    	end
+    	if recoiltime ~= 0 then
+    		local curpitch = GetPlayerPitch()
+    		local nextpitch = curpitch + 5
+    		SetPlayerPitch(nextpitch)
+    		ShakeCamera(0.5)
+    	end	
+    	if delay > 0.22 then
+    		recoilrotate = recoilrotate + 2
+    		recoilrotateH = recoilrotate/12
+    		local offset = Transform(Vec(0, 0, recoilrotateH), QuatEuler(recoilrotate, 0, 0))
+    		SetToolTransform(offset)
+    		--elseif reltime > 0 and reltime < 1.25 then
+    		--if recoilrotate < 0 then
+    			--recoilrotate = recoilrotate + 0.5
+    		--end
+    		--local offset = Transform(Vec(0, 0, 0), QuatEuler(recoilrotate, 0, 0))
+    		--SetToolTransform(offset)
+    	else
+    		recoilrotate = 0
+    	end
+
+    	if not rotime then
+    		local b = GetToolBody()
+    		local shapes = GetBodyShapes(b)
+
+    		if b ~= body then
+    			body = b
+    			t0 = GetShapeLocalTransform(shapes[1])
+    		end
+
+    		t = TransformCopy(t0)
+    		t.rot = QuatRotateQuat(QuatEuler(0, 0, 45), t.rot)
+    		t.pos = VecAdd(t.pos, Vec(0.225,-0.12,0))
+    		SetShapeLocalTransform(shapes[1], t)
+    	elseif rotime then
+    		local b = GetToolBody()
+    		local shapes = GetBodyShapes(b)
+
+    		if b ~= body then
+    			body = b
+    			t0 = GetShapeLocalTransform(shapes[1])
+    		end
+
+    		t = TransformCopy(t0)
+    		t.rot = QuatRotateQuat(QuatEuler(0, 0, 0), t.rot)
+    		t.pos = VecAdd(t.pos, Vec(0,0,0))
+    		SetShapeLocalTransform(shapes[1], t)
+    	end	
+    	--
+
+    	if GetBool("game.player.canusetool") and InputDown("lmb") and semi == false and delay < 0 and ammo > 0 and not reloading then
+    		if not unlimitedammo then
+    			ammo = ammo - 1
+    		end
+    		delay = 0.3
+    		semi = true
+    		if not norecoil then
+    			recoiltime = 0.05
+    		end
+    		if rotime == true then
+    			rotime = false
+    		else
+    			rotime =  true
+    		end
+
+    		local numbers = {-0.02, 0, 0.02}
+    		local randomIndex = math.random(1, #numbers)
+    		local r = numbers[randomIndex]
+    		local cam_tr = GetCameraTransform()
+    		local fwd = QuatRotateVec(cam_tr.rot, Vec(r, -0.2, -1.9)) 
+    		local up  = QuatRotateVec(cam_tr.rot, Vec(0, 1, 0))   
+    		local right = VecNormalize(VecCross(fwd, up))        
+
+    		local forward_offset = VecScale(fwd, 1.0)
+    		local right_offset   = VecScale(right, 0.4)  -- change 0.5 to move left/right
+    		local start_pos = VecAdd(cam_tr.pos, VecAdd(forward_offset, right_offset))
+
+    		ParticleGravity(4)
+    		ParticleRotation(.2)
+    		ParticleRadius(0.3)
+    		ParticleType("smoke")
+    		ParticleCollide(0)
+    		ParticleDrag(1)
+    		ParticleColor(.5,.5,.6)
+    		SpawnParticle(start_pos, VecAdd(0,0,0), 5.0)
+
+    		if ammoselect == 2 then
+    				Shoot(start_pos, fwd, "shotgun")
+    			PlaySound(gunLock)
+    		end
+
+    		if ammoselect ~= 2 then
+    			PlaySound(gunSnd)
+    			local speed = 40.0
+    			local vel = VecScale(fwd, speed)
+
+    			-- Add new projectile to the list
+    			table.insert(projectiles, {
+    				pos = VecCopy(start_pos),
+    				prev_pos = VecCopy(start_pos),
+    				vel = vel,
+    				time = 0.0,  -- For timeout
+    				max_time = 3.5  -- Max flight time in seconds before despawn
+    			})
+    		end
+    	end	
+
+    	if not InputDown("lmb") then
+    		semi = false
+    	end 
+
+    	if reltime ~= 0 then
+    	reloading = true
+    	ammo = 6
+    	else
+    		reloading = false
+    	end
+
+    	if InputDown("r") and reltime < 0 and ammo < 6 then
+    		reltime = 2.5
+    		PlaySound(gunRel)
+    	end
+
+    	if InputDown ("mmb") and not ammostop and empty then
+    		ammostop = true
+    		if ammoselect ~= 0 then
+    			ammoselect = ammoselect - 1
+    		else
+    			ammoselect = 5
+    		end
+    	elseif not InputDown ("mmb") then
+    		ammostop = false
+    	end
+    	if InputDown ("rmb") and not ammostopdown and empty then
+    		ammostopdown = true
+    		if ammoselect < 5 then
+    			ammoselect = ammoselect + 1
+    		else
+    			ammoselect = 0
+    		end
+    	elseif not InputDown ("rmb") then
+    		ammostopdown = false
+    	end
+    end
+    for i = #projectiles, 1, -1 do
+           local p = projectiles[i]
+
+           p.time = p.time + dt
+
+           -- Timeout check
+           if p.time > p.max_time then
+               table.remove(projectiles, i)
+           end
+
+    	--gravity
+    	p.vel = VecAdd(p.vel, Vec(0, -9.81 * dt, 0))
+
+           -- Update position
+           p.prev_pos = VecCopy(p.pos)
+           p.pos = VecAdd(p.pos, VecScale(p.vel, dt))
+
+           -- Calculate movement vector this frame
+           local move_vec = VecSub(p.pos, p.prev_pos)
+           local move_len = VecLength(move_vec)
+
+           if move_len ~= 0 then
+               local dir = VecScale(move_vec, 1 / move_len)
+
+               -- Raycast to check for collision
+               local hit, dist, normal, shape = QueryRaycast(p.prev_pos, dir, move_len)
+
+               if hit then
+                   -- Calculate hit position
+                   hit_pos = VecAdd(p.prev_pos, VecScale(dir, dist))
+
+                   -- Hit Effects
+    			if ammoselect == 0 then -- HE
+    				Explosion(hit_pos, 1.0) 
+    			elseif ammoselect == 1 then  -- CLUSTER
+    				Explosion(hit_pos, 0.7) 
+    				clustime = 1.5
+    			elseif ammoselect == 2 then  -- HORNETS
+    				--Explosion(hit_pos, 0.5) 
+    			elseif ammoselect == 3 then	-- FRAG
+    				Explosion(hit_pos, 1.0) 
+    				local cam = GetCameraTransform()          -- player view direction
+    				local forward = QuatRotateVec(cam.rot, Vec(0,0,-1))
+    				local up      = QuatRotateVec(cam.rot, Vec(0,1,0))
+
+    				-- build a local right vector (forward × up)
+    				local right = VecNormalize(VecCross(forward, up))
+
+    				local spreadAngle = 80         -- max cone angle in degrees
+    				local rad = math.rad(spreadAngle)
+
+    				for i = 0, 15 do
+    					local golden = 0.618033988749895  
+    					local theta  = 2 * math.pi * (i * golden) % (2 * math.pi)
+
+    					-- vertical offset inside the cone
+    					local r = math.sqrt( (i + 0.5) / 16 )   
+    					local pitch = math.asin(r) * rad
+
+    					local sinPitch = math.sin(pitch)
+    					local cosPitch = math.cos(pitch)
+
+    					local dirX = math.cos(theta) * sinPitch * right[1] +
+    								 math.sin(theta) * sinPitch * up[1] +
+    								 cosPitch * forward[1]
+
+    					local dirY = math.cos(theta) * sinPitch * right[2] +
+    								 math.sin(theta) * sinPitch * up[2] +
+    								 cosPitch * forward[2]
+
+    					local dirZ = math.cos(theta) * sinPitch * right[3] +
+    								 math.sin(theta) * sinPitch * up[3] +
+    								 cosPitch * forward[3]
+
+    					local dir = Vec(dirX, dirY, dirZ)
+
+    					Shoot(hit_pos, dir, "bullet")
+    					Shoot(hit_pos, dir, "shotgun")
+    				end	
+    			elseif ammoselect == 4 then --CAUSTIC
+    				local p = GetPlayerPos(playerId)
+    				local a = hit_pos
+    				local x = VecSub(p, a)
+    				local px = VecLength(x)
+
+    				if px < 5 then
+    						SetPlayerHealth(playerId, 0.0)
+    				end	
+    				PlaySound(gasSnd, hit_pos, 1.0)
+    				r = VecAdd (hit_pos, Vec(2, 0, 0))
+    				MakeHole(r, 11.0, 10.0, 9.0)
+    				MakeHole(r, 10.0, 9.0, 8.0)
+    				MakeHole(r, 9.0, 8.0, 7.0)
+    				Paint(r, 5.0, "spraycan", 1.0)
+    				SpawnFire(r)
+    				ParticleGravity(4)
+    				ParticleRotation(.2)
+    				ParticleRadius(4.0)
+    				ParticleType("plain")
+    				ParticleCollide(0)
+    				ParticleDrag(1)
+    				ParticleColor(1,1,0)
+    				ParticleAlpha(5.0 , 0.0, smooth, .05)
+    				r = VecAdd (hit_pos, Vec(4, 0, 0))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				r = VecAdd (hit_pos, Vec(0, 0, 4))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				ParticleRotation(-.2)
+    				r = VecAdd (hit_pos, Vec(-4, 0, 0))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				r = VecAdd (hit_pos, Vec(0, 0, -4))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				r = VecAdd (hit_pos, Vec(0, 0, 0))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    			elseif ammoselect == 5 then -- IMPLOSION
+    				r = VecAdd (hit_pos, Vec(2, 0, 0))
+    				MakeHole(r, 11.0, 10.0, 9.0)
+    				MakeHole(r, 10.0, 9.0, 8.0)
+    				PlaySound(imploSnd, hit_pos, 5.0)
+    				implotime = 1.0
+    				intensity = 600
+    				implode(hit_pos)
+    				ParticleGravity(-4)
+    				ParticleRotation(.2)
+    				ParticleRadius(4.0)
+    				ParticleType("plain")
+    				ParticleCollide(0)
+    				ParticleDrag(1)
+    				ParticleColor(.5,.5,.6)
+    				r = VecAdd (hit_pos, Vec(5, 0, 0))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				r = VecAdd (hit_pos, Vec(0, 0, 5))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				ParticleRotation(-.2)
+    				r = VecAdd (hit_pos, Vec(-5, 0, 0))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				r = VecAdd (hit_pos, Vec(0, 0, -5))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				r = VecAdd (hit_pos, Vec(0, 0, 0))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    				ParticleRadius(1.0, 100.0)
+    				r = VecAdd (hit_pos, Vec(0, 5, 0))
+    				SpawnParticle(r, VecAdd(0,0,0), 5.0)
+    			end	
+
+                   table.remove(projectiles, i)
+               else
+    			ParticleRadius(0.2)
+    			ParticleTile(9)
+    			ParticleType("plain")
+    			ParticleCollide(0)
+    			ParticleDrag(1)
+    			ParticleColor(.5,.5,.5)
+                   if ammoselect == 5 then
+    				PointLight(p.pos, 0, 0, 1, 10)
+    			end
+    			SpawnParticle(p.pos, VecAdd(0,0,0), 0.5)
+               end
+           end
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
@@ -1,80 +1,4 @@
-function init()
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	if unlimitedammo == 0 then unlimitedammo = 0.15 end
-	norecoil = GetBool("savegame.mod.norecoil")
-	if norecoil == 0 then norecoil = 0.15 end
-	noreticle = GetBool("savegame.mod.noreticle")
-	if noreticle == 0 then noreticle = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Grenade Launcher Options")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Unlimited Ammo")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(1, 1, 1)
-		if unlimitedammo then
-		   	if UiTextButton("Yes", 20, 20) then
-				unlimitedammo = false
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				unlimitedammo = true
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		end
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("No Recoil")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(1, 1, 1)
-		if norecoil then
-		    if UiTextButton("Yes", 20, 20) then
-		        norecoil = false
-			    SetBool("savegame.mod.norecoil", norecoil)
-			end
-		else
-		    if UiTextButton("No", 20, 20) then
-			    norecoil = true
-			    SetBool("savegame.mod.norecoil", norecoil)
-			end
-		end
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("No Reticle")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(1, 1, 1)
-		if noreticle then
-		    if UiTextButton("Yes", 20, 20) then
-		        noreticle = false
-			    SetBool("savegame.mod.noreticle", noreticle)
-			end
-		else
-		    if UiTextButton("No", 20, 20) then
-			    noreticle = true
-			    SetBool("savegame.mod.noreticle", noreticle)
-			end
-		end	
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
@@ -93,4 +17,82 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    if unlimitedammo == 0 then unlimitedammo = 0.15 end
+    norecoil = GetBool("savegame.mod.norecoil")
+    if norecoil == 0 then norecoil = 0.15 end
+    noreticle = GetBool("savegame.mod.noreticle")
+    if noreticle == 0 then noreticle = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Grenade Launcher Options")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Unlimited Ammo")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(1, 1, 1)
+    	if unlimitedammo then
+    	   	if UiTextButton("Yes", 20, 20) then
+    			unlimitedammo = false
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			unlimitedammo = true
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	end
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("No Recoil")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(1, 1, 1)
+    	if norecoil then
+    	    if UiTextButton("Yes", 20, 20) then
+    	        norecoil = false
+    		    SetBool("savegame.mod.norecoil", norecoil, true)
+    		end
+    	else
+    	    if UiTextButton("No", 20, 20) then
+    		    norecoil = true
+    		    SetBool("savegame.mod.norecoil", norecoil, true)
+    		end
+    	end
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("No Reticle")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(1, 1, 1)
+    	if noreticle then
+    	    if UiTextButton("Yes", 20, 20) then
+    	        noreticle = false
+    		    SetBool("savegame.mod.noreticle", noreticle, true)
+    		end
+    	else
+    	    if UiTextButton("No", 20, 20) then
+    		    noreticle = true
+    		    SetBool("savegame.mod.noreticle", noreticle, true)
+    		end
+    	end	
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
