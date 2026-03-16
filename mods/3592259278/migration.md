# Migration Report: custom_explosion.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/custom_explosion.lua
+++ patched/custom_explosion.lua
@@ -1,24 +1,74 @@
-QueryRequire("physical")
-
+#version 2
+local MATERIAL_RESISTANCE = {
+    glass=0.5, dirt=0.6, wood=1.0, plastic=1.0, plaster=1.2,
+    concrete=2.0, brick=2.2, ["weak metal"]=2.4, ["hard masonry"]=3.2,
+    ["hard metal"]=3.7, ["heavy metal"]=9999, rock=9999
+}
+local HOLE_SCORCH_BASE_CHANCE     = 0.55
+local HOLE_SCORCH_SMALL_UPSCALE   = 1.0
+local HOLE_SCORCH_SMALL_THRESH    = 0.060
+local HOLE_SCORCH_MIN_RAD_SCALE   = 0.65
+local HOLE_SCORCH_MAX_RAD_SCALE   = 1.35
+local HOLE_SCORCH_STEPS_MIN       = 1
+local HOLE_SCORCH_STEPS_MAX       = 3
+cal HOLES_PER_FRAME        = 60  
+cal HOLE_JOBS_PER_FRAME    = 20  
+cal HOLE_SILENT            = true  
+cal holeJobs = {}  
+cal holesProcessedThisFrame = 0
+l
+cal holeJobsProcessedThisFrame = 0
+
+cal SHRAPNEL_YMIN      = -0.35  
+cal SHRAPNEL_YMAX      =  0.80  
+cal SHRAPNEL_FLAT      =  0.00  
+cal SHRAPNEL_DOWN_TILT =  0.06  
+cal SHRAPNEL_MIX_FASTCALC         = 0.85  
+cal SHRAPNEL_SEGMENTS_PER_FRAME   = 360  
+cal SHRAPNEL_HOLE_PROB_NEAR       = 0.99  
+cal SHRAPNEL_HOLE_PROB_FAR        = 0.00  
+cal SHRAPNEL_FAR_NOHOLE_DIST      = 70.0  
+l SHRAPNEL_MAX_ACTIVE_FRAGMENTS = 280    
+l SHRAPNEL_MAX_STEPS_PER_FRAG   = 180    
+l SHRAPNEL_FASTCALC_LEN         =  math.min( maxDist or 80, 70 )  --
+l SHRAPNEL_STEP_DIST            = 0.20    
+l SHRAPNEL_AIR_LOSS_PER_METER   = 0.025
+
+lo
+l shrapnelTasks = {}    
+l shrapnelSegmentBudget = 0    
+HitsPlayer
+local applySh
+apnelHPDamage
+
+-- Budgeted
+_DELAY   = 0.30     -- never 
+KETS     = 8        -- num
+KET_DT   = PUFF_MAX_DELAY / PUFF_BUCKETS
+local PUFF_FR
+G_SPEED  = 300.0    -- m/s-ish
+ets = {}
+for i = 1, PU
+etCursor = 1
+local puffBuc
+etAcc    = 0.0
+
+-- Ready lis
+y = {}
+
+-- For a rou
+apnelPuff
+
+-- === Cente
+  -- entries: {t=delay, p
 
 function rnd(mi, ma)
     return math.random(1000)/1000*(ma-mi) + mi
 end
 
-
 function rndVec(t)
 	return Vec(rnd(-t, t), rnd(-t, t), rnd(-t, t))
 end
-
-explosionPos = Vec()
-
-trails = {}
-debugRays = {} ---------
-
--- === Blast debug drawing ===
-enableBlastDebug      = false     -- master toggle for LOS rays
-blastDebugLife        = 8.0      -- seconds to persist
-blastDebugMaxSegments = 600      -- history cap (avoid runaway lists)
 
 local function AddDebugRay(from, to, color, life)
 	if not enableBlastDebug then return end
@@ -34,27 +84,6 @@
 	end
 end
 
-
-
-
--- Hoisted so it's shared everywhere
-local MATERIAL_RESISTANCE = {
-    glass=0.5, dirt=0.6, wood=1.0, plastic=1.0, plaster=1.2,
-    concrete=2.0, brick=2.2, ["weak metal"]=2.4, ["hard masonry"]=3.2,
-    ["hard metal"]=3.7, ["heavy metal"]=9999, rock=9999
-}
-
-
-
--- === Scorch helper around holes (cheap + biased to small holes) ===
-local HOLE_SCORCH_BASE_CHANCE     = 0.55   -- default chance to paint around a hole
-local HOLE_SCORCH_SMALL_UPSCALE   = 1.0   -- extra chance added for really small holes
-local HOLE_SCORCH_SMALL_THRESH    = 0.060  -- ~1-voxel-ish base (meters)
-local HOLE_SCORCH_MIN_RAD_SCALE   = 0.65   -- scorch radius ~ base*bias
-local HOLE_SCORCH_MAX_RAD_SCALE   = 1.35
-local HOLE_SCORCH_STEPS_MIN       = 1
-local HOLE_SCORCH_STEPS_MAX       = 3
-
 local function ScorchAroundHole(hitPos, nrm, baseR)
     if not baseR or baseR <= 0 then return end
     local chance = HOLE_SCORCH_BASE_CHANCE
@@ -87,17 +116,7 @@
     end
 end
 
-
--- === Hole planner (varied shapes, budgeted) ===
-local HOLES_PER_FRAME        = 60     -- hard cap of how many MakeHole() we do per frame
-local HOLE_JOBS_PER_FRAME    = 20      -- how many *recipes* (which may do multiple holes) we run per frame
-local HOLE_SILENT            = true   -- no break sounds from micro shrapnel
-
-local holeJobs = {}     -- queue of {pos, n, mat, base, style}
-local holesProcessedThisFrame = 0
-local holeJobsProcessedThisFrame = 0
-
-local function QueueHole(pos, nrm, mat, baseR, style)
+cal function QueueHole(pos, nrm, mat, baseR, style)
     holeJobs[#holeJobs+1] = {
         pos  = VecCopy(pos),
         nrm  = VecNormalize(nrm or Vec(0,1,0)),
@@ -107,14 +126,13 @@
     }
 end
 
-local function _doMakeHole(p, r0, r1, r2)
+cal function _doMakeHole(p, r0, r1, r2)
     if holesProcessedThisFrame >= HOLES_PER_FRAME then return end
     MakeHole(p, r0, r1 or 0, r2 or 0, HOLE_SILENT)
     holesProcessedThisFrame = holesProcessedThisFrame + 1
 end
 
--- 4 light-weight styles; each style limits itself to a handful of MakeHole() calls
-local function _runHoleRecipe(job)
+cal function _runHoleRecipe(job)
     local p   = job.pos
     local n   = job.nrm
     local b   = job.base * math.random(80,125) * 0.01  -- small random overall scale
@@ -124,7 +142,6 @@
     local t = VecNormalize(VecCross(n, Vec(0,1,0)))
     if VecLength(t) < 0.01 then t = VecNormalize(VecCross(n, Vec(1,0,0))) end
     local bt = VecNormalize(VecCross(n, t))
-
 
 	if sty == "ragged" then
 		_doMakeHole(p, b*1.0, b*0.85, b*0.5)
@@ -167,7 +184,7 @@
 	end
 end
 
-function UpdateHoles(dt)
+nction UpdateHoles(dt)
     holesProcessedThisFrame = 0
     holeJobsProcessedThisFrame = 0
     -- run at most X recipes per frame
@@ -180,29 +197,7 @@
     end
 end
 
--- shrapnel more bias towards ground 
-local SHRAPNEL_YMIN      = -0.35   -- was -0.2
-local SHRAPNEL_YMAX      =  0.80   -- was 0.7
-local SHRAPNEL_FLAT      =  0.00   -- 0..1 scales vertical component  good now.
-local SHRAPNEL_DOWN_TILT =  0.06   -- tiny extra downward bias
-
-
--- === Shrapnel scheduler ===
-local SHRAPNEL_MIX_FASTCALC         = 0.85      -- was 0.7 (more cheap hits = more puffs/marks)
-local SHRAPNEL_SEGMENTS_PER_FRAME   = 360       -- was 220
-local SHRAPNEL_HOLE_PROB_NEAR       = 0.99      -- was 0.70
-local SHRAPNEL_HOLE_PROB_FAR        = 0.00    -- far hits never cut holes
-local SHRAPNEL_FAR_NOHOLE_DIST      = 70.0      -- was 35.0 (don’t ban holes too aggressively)
-local SHRAPNEL_MAX_ACTIVE_FRAGMENTS = 280       -- was 180
-local SHRAPNEL_MAX_STEPS_PER_FRAG   = 180       -- was 120
-local SHRAPNEL_FASTCALC_LEN         =  math.min( maxDist or 80, 70 )  -- was 8.0
-local SHRAPNEL_STEP_DIST            = 0.20    -- keep step length
-local SHRAPNEL_AIR_LOSS_PER_METER   = 0.025
-
-local shrapnelTasks = {}           -- queue of marching fragments to simulate over time
-local shrapnelSegmentBudget = 0    -- refilled each frame in UpdateExplosionEffects
-
-local function _enqueueShrapnel(origin, dir, maxDist, power, maxPower)
+l function _enqueueShrapnel(origin, dir, maxDist, power, maxPower)
     if #shrapnelTasks >= SHRAPNEL_MAX_ACTIVE_FRAGMENTS then return end
     shrapnelTasks[#shrapnelTasks+1] = {
         pos = VecCopy(origin),
@@ -216,9 +211,9 @@
     }
 end
 
--- Fast, short ray that can pass thin walls once.
--- NEW: Dynamic/vehicle hits make holes immediately (MakeHole), statics keep queued recipes.
-local function _fastcalcShrapnel(origin, dir, materialResistance, farNoHoleDist, maxDist)
+--
+
+l function _fastcalcShrapnel(origin, dir, materialResistance, farNoHoleDist, maxDist)
     local len   = math.min(SHRAPNEL_FASTCALC_LEN, maxDist)
     local o     = origin
     local left  = len
@@ -269,7 +264,6 @@
 			ScorchAroundHole(hitPos, nrm, base)
 		end
 	end
-
 
     while hits < 2 and left > 0 do
         local hit, dist, nrm, shp = QueryRaycast(o, dir, left)
@@ -317,15 +311,9 @@
     end
 end
 
-
--- Put these near the top, BEFORE _advanceShrapnelFragments is defined
-local shrapnelHitsPlayer
-local applyShrapnelHPDamage
-
-
--- Budgeted marcher over multiple frames.
--- NEW: Dynamic/vehicle hits get immediate holes; statics keep queued recipes.
-local function _advanceShrapnelFragments(explosionOrigin, materialResistance)
+-- Put thes
+
+ _advanceShrapnelFragments(explosionOrigin, materialResistance)
     local processedSegments = 0
 
 	local function makeImmediateHole(hitPos, nrm)
@@ -373,7 +361,6 @@
 		end
 	end
 
-
     for i = #shrapnelTasks, 1, -1 do
         local f = shrapnelTasks[i]
         while processedSegments < shrapnelSegmentBudget do
@@ -400,7 +387,7 @@
             if not f.didPlayer then
                 local a = f.pos
                 local b = hit and VecAdd(f.pos, VecScale(f.dir, dist)) or VecAdd(f.pos, VecScale(f.dir, step))
-                local crosses, tOnSeg = shrapnelHitsPlayer(a, b, GetPlayerTransform().pos)
+                local crosses, tOnSeg = shrapnelHitsPlayer(a, b, GetPlayerTransform(playerId).pos)
                 if crosses then
                     local pt = VecLerp(a, b, tOnSeg)
                     applyShrapnelHPDamage(explosionOrigin, pt, f.traveled + (dist or step) * tOnSeg, f.power, f.maxPower)
@@ -461,45 +448,17 @@
     end
 end
 
-
-
--- === Shrapnel impact puffs ===
-enableShrapnelPuffs = true
-shrapnelPuffQueue = {}
-SHRAPNEL_PUFFS_PER_FRAME = 300   
-SHRAPNEL_PUFFS_INSTANT_BUDGET = 240  
-SHRAPNEL_PUFF_HARD_LIMIT = 2000   
-
-puffLoad = 0
-
-shrapnelPuffsProcessedThisFrame = 0
-
--- === Staggered shrapnel puff scheduler ===
-local PUFF_MAX_DELAY   = 0.30     -- never more than 0.2 s total staggering
-local PUFF_BUCKETS     = 8        -- number of time buckets inside the window
-local PUFF_BUCKET_DT   = PUFF_MAX_DELAY / PUFF_BUCKETS
-local PUFF_FRAG_SPEED  = 300.0    -- m/s-ish for artillery fragments (tune!)
-
-local puffBuckets = {}
-for i = 1, PUFF_BUCKETS do puffBuckets[i] = {} end
-local puffBucketCursor = 1
-local puffBucketAcc    = 0.0
-
--- Ready list we actually spawn from this frame
-local puffReady = {}
-
--- For a rough global cap across buckets
-local function totalQueuedPuffs()
+-- === Shr
+
+ totalQueuedPuffs()
     local c = #puffReady
     for i = 1, PUFF_BUCKETS do c = c + #puffBuckets[i] end
     return c
 end
 
-
-local SpawnShrapnelPuff
-
--- === Center "dustball" VFX burst (purely visual) ===
-local function EmitDustballBurst(origin, count)
+local Spawn
+
+ EmitDustballBurst(origin, count)
     count = count or 18
 
     for i = 1, count do
@@ -538,11 +497,10 @@
     end
 end
 
-
-
-function QueueShrapnelPuff(pos, normal, mat, strength)
+function Que
+
+rapnelPuff(pos, normal, mat, strength)
 	if not enableShrapnelPuffs then return end
-
 
 	if shrapnelPuffsProcessedThisFrame < SHRAPNEL_PUFFS_INSTANT_BUDGET then
 		SpawnShrapnelPuff(pos, VecNormalize(normal), mat or "plaster", strength or 1)
@@ -551,7 +509,6 @@
 		return
 	end
 
-
 	if #shrapnelPuffQueue >= SHRAPNEL_PUFF_HARD_LIMIT then
 
 		table.remove(shrapnelPuffQueue, 1)
@@ -572,7 +529,7 @@
     if totalQueuedPuffs() >= SHRAPNEL_PUFF_HARD_LIMIT then
         -- Drop oldest from the current cursor bucket to keep moving
         local b = puffBuckets[puffBucketCursor]
-        if #b > 0 then table.remove(b, 1) end
+        if #b ~= 0 then table.remove(b, 1) end
     end
 
     local b = puffBuckets[idx]
@@ -584,16 +541,15 @@
     }
 end
 
-
-
-local function materialDustParams(mat)
+local functi
+
+aterialDustParams(mat)
 
 	local start = {0.60, 0.58, 0.56}
 	local finish = {0.40, 0.38, 0.36}
 	local size = 0.35
 	local drag = 1.4
 	local grav = -2.0
-
 
 	if mat == "brick" then mat = "concrete" end
 	if mat == "weak metal" or mat == "hard metal" or mat == "heavy metal" then mat = "metal" end
@@ -610,17 +566,14 @@
 	elseif mat == "metal" then
 		start, finish, size, drag, grav = {0.70,0.70,0.70}, {0.48,0.48,0.48}, 0.30, 1.2, -3.6
 
-
 	end
 
 	return start, finish, size, drag, grav
 end
 
-
-
-
-
-function SpawnShrapnelPuff(pos, n, mat, s)
+function S
+
+rapnelPuff(pos, n, mat, s)
     -- Material-driven color/size/physics
     local c0, c1, rBase, drag, grav = materialDustParams(mat)  -- already defined above
     -- Strength multiplier (s ~ impact intensity)
@@ -680,9 +633,9 @@
     end
 end
 
-
-
-function UpdateShrapnelPuffs(dt)
+function UpdateShrapne
+
+fs(dt)
     if not enableShrapnelPuffs then return end
 
     -- advance the time wheel
@@ -691,7 +644,7 @@
         puffBucketAcc = puffBucketAcc - PUFF_BUCKET_DT
         -- move current bucket to ready
         local b = puffBuckets[puffBucketCursor]
-        if #b > 0 then
+        if #b ~= 0 then
             for i = 1, #b do puffReady[#puffReady+1] = b[i] end
             puffBuckets[puffBucketCursor] = {}
         end
@@ -717,17 +670,16 @@
     puffLoad = math.max(0.0, puffLoad - dt * 0.5)
 end
 
-
 -------------------
--- === Two-stage blast queue ===
-local postBlastQueue = {}   -- entries: {t=delay, pos=Vec(), r=number, p=number}
-
-function QueuePostBlast(pos, radius, power, delay)
+-- 
+
+s, radius, power, delay)
     postBlastQueue[#postBlastQueue+1] = { t = delay or 0.03, pos = VecCopy(pos), r = radius, p = power }
 end
 
--- Call this once per tick(dt) from your update/tick
-function UpdatePostBlasts(dt)
+-- Call this once per ti
+
+dt)
     for i = #postBlastQueue, 1, -1 do
         local job = postBlastQueue[i]
         job.t = job.t - dt
@@ -738,7 +690,9 @@
     end
 end
 
-function ApplyBlastImpulse(pos, radius, power)
+function ApplyBlastImpul
+
+(pos, radius, power)
     local bodies = QueryAabbBodies(VecAdd(pos, Vec(-radius,-radius,-radius)), VecAdd(pos, Vec(radius,radius,radius)))
     for i = 1, #bodies do
         local b = bodies[i]
@@ -770,9 +724,9 @@
     end
 end
 
-
-
-function trailsAdd(pos, vel, life, size, damp, gravity)
+function trailsAdd(pos, vel,
+
+e, size, damp, gravity)
 	t = {}
 	t.pos = VecCopy(pos)
 	t.vel = VecAdd(Vec(0, vel*.85, 0), rndVec(vel))
@@ -786,7 +740,9 @@
 end
 
 function trailsUpdate(dt)
-	for i=#trails,1,-1 do
+	for
+
+=#trails,1,-1 do
 		local t = trails[i]
 		t.vel[2] = t.vel[2] + t.gravity*dt
 		t.vel = VecScale(t.vel, t.damp)
@@ -816,17 +772,11 @@
 	end
 end
 
-
 smoke = {}
 smoke.age = 0
-smoke.size = 1
-smoke.life = 1.6
-smoke.next = 0
-smoke.vel = 0
-smoke.gravity = 0
-smoke.amount = 2.5
-function smokeUpdate(pos, dt)
-	smoke.age = smoke.age + dt
+smok
+
+moke.age = smoke.age + dt
 	if smoke.age < smoke.life then
 		local q = 1.0 - smoke.age / smoke.life
 		for i=1, smoke.amount*q do
@@ -848,27 +798,19 @@
 end
 
 dustKickup = {}
-dustKickup.age = 0
-dustKickup.size = 3.2           
-dustKickup.life = 4.5           
-dustKickup.next = 0
-dustKickup.vel = 5.5            
-dustKickup.gravity = -2.5       
-dustKickup.amount = 20          
-
-function dustKickupUpdate(pos, dt)
+dustKickup.age
+
+t)
 	dustKickup.age = dustKickup.age + dt
 	if dustKickup.age < dustKickup.life then
 		local q = 1.0 - dustKickup.age / dustKickup.life
 		for i = 1, dustKickup.amount * q do
 			local r = dustKickup.size * (0.5 + 0.5 * q)
 
-
 			local angle = rnd(0, math.pi * 2)
 			local distance = rnd(0.5, 2.0) * q 
 			local dir = Vec(math.cos(angle), 0, math.sin(angle)) 
 			local spreadVel = VecScale(dir, rnd(1.5, 3.5)) 
-
 
 			spreadVel[2] = rnd(0.1, 0.5)
 
@@ -887,17 +829,8 @@
 		end
 	end
 end
-----------------------------------------------------------------------------------------------------------------------------------------
-redSmoke = {}
-redSmoke.age = 0
-redSmoke.size = 1
-redSmoke.life = 1.6
-redSmoke.next = 0
-redSmoke.vel = 0
-redSmoke.gravity = 0
-redSmoke.amount = 2.5
-
-function redSmokeUpdate(pos, dt)
+-------------------------------
+
 	redSmoke.age = redSmoke.age + dt
 	if redSmoke.age < redSmoke.life then
 		local q = 1.0 - redSmoke.age / redSmoke.life
@@ -923,13 +856,9 @@
 	end
 end
 
-----------------------------------------------------------------------------------------------------------------
-fire = {}
-fire.age = 0
-fire.life = 5
-fire.size = 1
-function fireUpdate(pos, dt)
-	fire.age = fire.age + dt
+------------------------------
+
+re.age = fire.age + dt
 	if fire.age < fire.life then
 		local q = 1.0 - fire.age / fire.life
 		for i=1, 16 do
@@ -950,14 +879,11 @@
 	end
 end
 
-
-
 flash = {}
 flash.age = 0
-flash.life = 1.25
-flash.intensity = 20
-function flashUpdate(pos, dt)
-	flash.age = flash.age + dt
+fla
+
+lash.age = flash.age + dt
 	if flash.age < flash.life then
 		local q = 1.0 - flash.age / flash.life
 		PointLight(pos, 1.0, 0.85, 0.75, flash.intensity*q)
@@ -965,13 +891,11 @@
 	end
 end
 
-
 light = {}
 light.age = 0
-light.life = 1.15
-light.intensity = 50
-function lightUpdate(pos, dt)
-	light.age = light.age + dt
+ligh
+
+ight.age = light.age + dt
 	if light.age < light.life then
 		local q = 1.0 - light.age / light.life
 		local l = q * q
@@ -981,9 +905,9 @@
 	end
 end
 
-
-
-function explosionEmbers(count, vel)
+function explosionEmbers(cou
+
+vel)
     local origin = explosionPos
 
     -- base scales
@@ -999,20 +923,16 @@
         local t  = math.random() ^ 0.7
         local h  = hMin + t * (hMax - hMin)
 
-
         local phi = rnd(0, math.pi * 2)
         local rScale = 0.35 + 0.65 * ((h - hMin) / math.max(0.001, (hMax - hMin)))
         local r  = math.sqrt(math.random()) * rMax * rScale
 
-
         local spawn = VecAdd(origin, Vec(r * math.cos(phi), h + rnd(-0.2, 0.2), r * math.sin(phi)))
-
 
         local phi2    = rnd(0, math.pi * 2)
         local lateral = rnd(0.15, 0.6)
         local down    = rnd(0.15, 0.45)
         local v = VecAdd(Vec(lateral * math.cos(phi2), -down, lateral * math.sin(phi2)), wind)
-
 
         local life = (rnd(0.7, 1.0)^2) * 14
 
@@ -1029,13 +949,9 @@
     end
 end
 
-
-
-
-
-
-
-function explosionSparks(count, vel, opt)
+function explosionSparks
+
+vel, opt)
     opt = opt or {}
 	local rnd = function(mi, ma) return math.random()*(ma-mi)+mi end
     local flat       = opt.flat       or 0.15      -- keep some vertical variety
@@ -1080,7 +996,7 @@
         end
 
         -- Flatten a bit, then small downward nudge
-        if flat > 0 then
+        if flat ~= 0 then
             localDir[2] = localDir[2] * (1.0 - flat)
         end
         localDir[2] = localDir[2] - downBias
@@ -1116,11 +1032,9 @@
     end
 end
 
-
-
-
 function explosionSlag(count, vel)
-    for i = 1, count do
+
+or i = 1, count do
 
         local dir = VecNormalize(rndVec(1))
         dir[2] = dir[2] * 0.35  
@@ -1146,10 +1060,9 @@
     end
 end
 
-
-
 function explosionDebris(count, vel)
-	for i=1, count do
+
+r i=1, count do
 		local r = rnd(0, 1)
 		life = 10 + r*r*r*3
 		r = (0.4 + 0.6*r*r*r)
@@ -1169,9 +1082,9 @@
 	end
 end
 
-
 function explosionRubble(count, vel)
-	for i=1, count do
+
+r i=1, count do
 		local r = rnd(0, 1)
 		life = 5 + r*r*r*3
 		r = (0.4 + 0.6*r*r*r)
@@ -1190,9 +1103,10 @@
 	end
 end
 
-
 function explosionMedium(pos) 
-	explosionPos = pos
+	explo
+
+nPos = pos
 	PressureDamage(pos, 4.0, 3.0, 2.0)
 	DoShrapnelExplosion(pos, 400, 80)	
 	ApplyBlastVelocity(pos, 30.0, 22.0)
@@ -1202,7 +1116,6 @@
 	ShakeFromExplosion(pos, 100.0, 2.0) 
 	ScorchExplosionWithArms(pos, 3.0, 6, 20) 
 	ApplyBlastDamage(pos)
-
 
 	
 	explosionEmbers(200, 12)  
@@ -1246,7 +1159,9 @@
 end
 
 function smokeShell(pos)
-	explosionPos = pos
+	explosionPos
+
+ pos
 
 	
 	PressureDamage(pos, 1.0, 0.5, 0.3) 
@@ -1255,15 +1170,12 @@
 	ShakeFromExplosion(pos, 10.0, 1.0)
 	ScorchExplosionWithArms(pos, 3.0, 6, 20) 
 
-
-
 	explosionEmbers(50, 12) 
 	explosionSlag(50, 32)
 	explosionSparks(50, 26)
 	explosionDebris(150, 30)
 	explosionRubble(10, 22)
 
-
 	flash.age = 0
 	flash.life = 0.2 
 	flash.intensity = 1500
@@ -1275,7 +1187,6 @@
 	fire.age = 0
 	fire.life = 1.0
 	fire.size = 1.0
-
 
 	redSmoke.age = 0
 	redSmoke.size = 1
@@ -1294,18 +1205,9 @@
 	
 end
 
-
--- Upgraded DoShrapnelExplosion tuned for ~80 m:
--- - Air drag starts after 10 m
--- - Distance falloff uses ABSOLUTE meters (not tied to maxDist)
--- - Far-range “graze” hits (scorch only) beyond ~70 m
--- DoShrapnelExplosion tuned for ~80 m, lighter falloff, no grazes
-
-
--- Squared distance between two segments p1->q1 and p2->q2 (returns d2, plus the
--- parametric t in [0..1] along the first segment for the closest point).
-local function segSegDist2(p1, q1, p2, q2)
-	local u = VecSub(q1, p1)
+-- Upgraded DoShrapnelExplosion tuned
+
+local u = VecSub(q1, p1)
 	local v = VecSub(q2, p2)
 	local w = VecSub(p1, p2)
 
@@ -1369,9 +1271,9 @@
 	return VecDot(dP, dP), sc
 end
 
-
-function shrapnelHitsPlayer(stepA, stepB, playerPos)
-
+function shrapnelHitsPlayer(stepA, stepB, pl
+
+rPos)
 
 	local a = VecAdd(playerPos, Vec(0, -0.30, 0))     
 	local b = VecAdd(playerPos, Vec(0,  0.80, 0))     -- upper torso/head               :contentReference[oaicite:1]{index=1}
@@ -1384,9 +1286,9 @@
 	return false, 0.0
 end
 
-
--- Apply HP damage once for a fragment when a step crosses the player
-function applyShrapnelHPDamage(explosionOrigin, hitPoint, totalDist, power, maxPower)
+-- Apply HP damage once for a fragment when 
+
+ hitPoint, totalDist, power, maxPower)
 	
 	local falloffStartMeters = 10.0
 	local falloffEndMeters   = 70.0
@@ -1399,31 +1301,28 @@
 	end
 	local distScale = (1.0 - t) + t * farMinDamageScale
 
-
 	local powerScale = math.max(0.0, power / math.max(0.001, maxPower))
 
-
 	local baseDmg = 50.0
 
 	local dmg = baseDmg * distScale * powerScale
 
-
-	if GetPlayerVehicle() ~= 0 then
+	if GetPlayerVehicle(playerId) ~= 0 then
 		dmg = dmg * 0.35
 	end
 
 	if dmg > 0 and not GetBool("savegame.mod.barragere.disablePlayerDamage", false) then
-		local hp = GetPlayerHealth()
+		local hp = GetPlayerHealth(playerId)
 		
-		SetPlayerHealth(math.max(0.0, hp - dmg / 100.0))
+		SetPlayerHealth(playerId, math.max(0.0, hp - dmg / 100.0))
 		local newHp = math.max(0.0, hp - dmg / 100.0)
 
 	end
 end
 
-
--- === MIXED shrapnel spawner (no big frame spike) ===
-function DoShrapnelExplosion(origin, rayCount, maxDist)
+-- === MIXED shrapnel spawner (no big frame 
+
+maxDist)
     -- keep your smart lift
     local offset = 0
     local hitD = select(2, QueryRaycast(origin, Vec(0, -1, 0), 1.0))
@@ -1466,12 +1365,8 @@
 	EmitDustballBurst(raisedOrigin, 18)
 end
 
-
-
-
-
-
-function ApplyBlastVelocity(pos, radius, power)
+function ApplyBlastVelocity(pos, radius,
+
     local bodies = QueryAabbBodies(VecAdd(pos, Vec(-radius,-radius,-radius)), VecAdd(pos, Vec(radius,radius,radius)))
     local M_REF = 800.0         -- reference mass ~ a person/door
     local V_CAP_LIGHT = 22.0    -- cap for very light props
@@ -1505,9 +1400,9 @@
     end
 end
 
-
-
-function AddExplosionHeat(origin, rayCount, maxDist, maxHeat)
+function AddExplosionHeat(origin, rayCount, max
+
+, maxHeat)
 	for i = 1, rayCount do
 		local dir = VecNormalize(rndVec(1))
 		local hit, dist, normal, shape = QueryRaycast(origin, dir, maxDist)
@@ -1523,8 +1418,10 @@
 	end
 end
 
-function ShakeFromExplosion(explosionPos, maxDist, maxShake)
-	local playerPos = GetPlayerTransform().pos
+function ShakeFromExplosion(explosionPos, maxDist
+
+maxShake)
+	local playerPos = GetPlayerTransform(playerId).pos
 	local dist = VecLength(VecSub(playerPos, explosionPos))
 
 	if dist < maxDist then
@@ -1535,18 +1432,22 @@
 end
 
 function PressureDamage(pos, r0, r1, r2)
-	MakeHole(pos, r0, r1, r2, true)  --true is silent
-
-end
-
-function math.clamp(val, min, max)  --For the scrotch explosion arms
+	MakeHol
+
+pos, r0, r1, r2, true)  --true is silent
+
+end
+
+function math.clamp(val, min, max)  --For the scr
+
+ch explosion arms
 	if min > max then min, max = max, min end
 	return math.max(min, math.min(max, val))
 end
 
-
-
-function ScorchExplosionWithArms(pos, radius, minArms, maxArms) 
+function ScorchExplosionWithArms(pos, radius, m
+
+ms, maxArms) 
 	Paint(pos, math.min(radius, 5.0), "explosion", 1.0)
 
 	local numArms = math.random(minArms, maxArms)
@@ -1572,9 +1473,9 @@
 	end
 end
 
--- === PLAYER BLAST DAMAGE SYSTEM (multi-ray LOS) ===
-
-local function SampleBlastOrigins(center, radius, count, hemisphereUp)
+-- === PLAYER BLAST DAMAGE SYSTEM (multi-ray LOS)
+
+ount, hemisphereUp)
 	local outs = {}
 	for i = 1, count do
 		local a = rnd(0, math.pi * 2)
@@ -1590,18 +1491,20 @@
 end
 
 local function isVehicleBody(body)
-	return body ~= 0 and GetBodyVehicle(body) ~= 0
-end
-
+	return body ~=
+
+ and GetBodyVehicle(body) ~= 0
+end
 
 local function _rayBlocked(origin, target)
-	-- returns: bodyOrFalse, hitDistFromOrigin
+	-- re
+
+ns: bodyOrFalse, hitDistFromOrigin
 	local to   = VecSub(target, origin)
 	local dist = VecLength(to)
 	if dist <= 0.05 then return false, dist end
 	local dir  = VecNormalize(to)
 
-
 	local startEps = 0.06
 	local o2 = VecAdd(origin, VecScale(dir, startEps))
 
@@ -1620,9 +1523,10 @@
 	return GetShapeBody(hShape), (startEps + hDist)
 end
 
-
 function ApplyBlastDamage(explosionPos)
-	-- === Tunables
+	-- === T
+
+bles
 	local maxBlastRadius = 30.0
 	local innerRadius    = 3.0
 	local baseDamage     = 140.0
@@ -1647,9 +1551,8 @@
 		if #debugRays > 1200 then table.remove(debugRays, 1) end
 	end
 
-
 	-- Positions
-	local playerTr  = GetPlayerTransform()
+	local playerTr  = GetPlayerTransform(playerId)
 	local playerPos = playerTr.pos
 	local camPos    = GetCameraTransform().pos
 
@@ -1673,7 +1576,6 @@
 		VecAdd(playerPos, Vec(0, 0.30, 0)),    -- mid
 		VecAdd(playerPos, Vec(0, -0.30, 0)),   -- hips/knees
 	}
-
 
 	local jitter  = 0.18
 	local samples = {}
@@ -1719,12 +1621,10 @@
 		end
 	end
 
-
 	if openCount == 0 and dynBlockCount == 0 then return end
 
 	-- Visibility fraction = “how much of the silhouette is exposed”
 	local vis = (totalRays > 0) and (openCount / totalRays) or 0
-
 
 	local visEff = vis
 	if distCenter <= closeVisClampR then
@@ -1743,35 +1643,30 @@
 	local dmg = baseDamage * (1.0 - math.pow(t, falloffPower)) * visEff
 
 	-- Dynamic/vehicle blocker leakage: shave more off if most rays hit dynamics
-	if dynBlockCount > 0 then
+	if dynBlockCount ~= 0 then
 		local dynFrac = dynBlockCount / math.max(1, totalRays)
 		dmg = dmg * (1.0 - 0.60 * dynFrac)
 	end
 
-
-	if GetPlayerVehicle() ~= 0 then
+	if GetPlayerVehicle(playerId) ~= 0 then
 		dmg = dmg * 0.35
 	end
-
 
 	if distCenter <= lethalRadius and (openCount > 0 or dynBlockCount > 0) then
 		dmg = 200.0
 	end
 
-
 	if dmg > 0 and not GetBool("savegame.mod.barragere.disablePlayerDamage") then
-		local hp = GetPlayerHealth()
-		SetPlayerHealth(math.max(0.0, hp - dmg / 100.0))
-	end
-
-end
-
-
-
-
+		local hp = GetPlayerHealth(playerId)
+		SetPlayerHealth(playerId, math.max(0.0, hp - dmg / 100.0))
+	end
+
+end
 
 function UpdateExplosionEffects(dt)
-	shrapnelPuffsProcessedThisFrame = 0
+	shrapnelPuffsProce
+
+isFrame = 0
 	    -- refill segment budget proportionally to dt to keep frame time stable
     shrapnelSegmentBudget = math.floor(SHRAPNEL_SEGMENTS_PER_FRAME * math.max(0.001, dt) / (1/60))
 
@@ -1806,5 +1701,3 @@
 	end
 end
 
-
-

```

---

# Migration Report: i18n.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/i18n.lua
+++ patched/i18n.lua
@@ -1,17 +1,5 @@
-
-I = I or {} 
-
+#version 2
 local LANG_KEY = "savegame.mod.barragere.lang"
-
-local function currentLang()
-    if not HasKey(LANG_KEY) then
-        SetString(LANG_KEY, "en")
-    end
-    local l = GetString(LANG_KEY)
-    return (l == "ru") and "ru" or "en"
-end
-
-
 local T = {
 	en = {
 		menu_title          = "Artillery Barrage Options",
@@ -128,7 +116,6 @@
 	}
 }
 
-
 function I.t(key, ...)
     local lang = currentLang()
     local pack = T[lang]
@@ -145,7 +132,14 @@
 
 function I.setLang(newLang)
     if newLang ~= "ru" then newLang = "en" end
-    SetString(LANG_KEY, newLang)
+    SetString(LANG_KEY, newLang, true)
 end
 
+local function currentLang()
+    if not HasKey(LANG_KEY) then
+        SetString(LANG_KEY, "en", true)
+    end
+    local l = GetString(LANG_KEY)
+    return (l == "ru") and "ru" or "en"
+end
 

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
@@ -1,119 +1,21 @@
-#include "custom_explosion.lua"
-#include "i18n.lua"
-
-barrageAccuracy = 20.0
-preExplosionSoundTime = 3.0
-circleOrigin = nil  -- will be used to clamp movement range
-strikeCancelledTime = nil
--- precise strike state
-strikeActive = false
-strikeCancelled = false
-incomingCloseLead = incomingCloseLead or 0.7    -- seconds before impact
--- Circle selection camera mode
-circleTopDown = circleTopDown or false   -- false = angled (default), true = top-down
--- Circle selection UI state
-circleControlsVisible = circleControlsVisible or false
-
---========================
--- DRONE VIEW (state)
---========================
-droneActive   = false
-droneCenter   = nil     -- Vec, center of called barrage (== barrageTarget)
-dronePos      = nil     -- Vec, current look-at point on ground plane
-droneZoom     = 1.0     -- 1 = same zoom-out as circle selection for chosen radius, 10 = close
-droneMaxMove  = 0.0     -- clamp radius for WASD (depends on selected barrage radius)
-droneBaseHoriz = 0.0    -- base camera horizontal offset derived from chosen radius
-droneBaseVert  = 0.0    -- base camera vertical   offset derived from chosen radius
-
-
--- =======================================
--- Drone view UI state
--- =======================================
-if not HasKey("savegame.mod.barragere.dronePanelVisible") then
-    SetBool("savegame.mod.barragere.dronePanelVisible", true)
-end
-dronePanelVisible = GetBool("savegame.mod.barragere.dronePanelVisible", true)
-
-
-
-showDistance = false  -- toggle on/off if needed --------------------------------------------------------------------------------------------
-
-cooldownActive = false
-
-incomingClose = {
-	LoadSound("MOD/sound/incoming_close.ogg"),
-	LoadSound("MOD/sound/incoming_close_2.ogg"),
-	LoadSound("MOD/sound/incoming_close_4.ogg"),
-	LoadSound("MOD/sound/incoming_close_5.ogg")
-}
-
-incomingSounds = {
-    LoadSound("MOD/sound/incoming_1.ogg"),
-    LoadSound("MOD/sound/incoming_2.ogg"),
-    LoadSound("MOD/sound/incoming_3.ogg"),
-    LoadSound("MOD/sound/incoming_4.ogg"),
-    LoadSound("MOD/sound/incoming_5.ogg"),
-    LoadSound("MOD/sound/incoming_6.ogg")
-}
-
-artillerySounds = {}
-for i = 1, 5 do
-    table.insert(artillerySounds, LoadSound("MOD/sound/artilery" .. i .. ".ogg"))
-end
-
--- ==== NEW: explosion banks (point-blank, mid, far, very-far) ====
-expPointBlank = {}    -- uses old exp_close1..8.ogg  (0–30 m)
-for i = 1, 8 do
-    table.insert(expPointBlank, LoadSound("MOD/sound/exp_close" .. i .. ".ogg"))
-end
-
-expMid = {}           -- uses old exp_mid1..8.ogg    (30–80 m)
-for i = 1, 8 do
-    table.insert(expMid, LoadSound("MOD/sound/exp_mid" .. i .. ".ogg"))
-end
-
-expFar = {}           -- uses old/new exp_far1..12.ogg (80–150 m)
-for i = 1, 12 do
-    table.insert(expFar, LoadSound("MOD/sound/exp_far" .. i .. ".ogg"))
-end
-
-expVeryFar = {}       -- NEW exp_veryfar1..12.ogg (170+ m)
-for i = 1, 12 do
-    table.insert(expVeryFar, LoadSound("MOD/sound/exp_veryfar" .. i .. ".ogg"))
-end
-
-
-radioSound = LoadSound("MOD/sound/radio.ogg")
-
-
--- ================= Sound (2D at player) =================
--- Explosions now use single-bank playback with a global distance falloff (no crossfades).
-SND_POS_TO_PLAYER_SCALE = SND_POS_TO_PLAYER_SCALE or 0.12  -- keep your global tweak
-
--- Whistle (incoming) envelope tuning
-WHISTLE_VOL       = WHISTLE_VOL or 0.7   -- overall whistle loudness knob
-WHISTLE_FAR_SCALE = 0.12                 -- how loud at the far edge (0.12 = 12% of point-blank)
-WHISTLE_URGENCY   = 0.20                 -- up to +20% gain in the final 0.8s
-CLOSE_WHISTLE_MIX = CLOSE_WHISTLE_MIX or 1.7   -- 1.0 = match exp_close loudness, tweak to taste
-
--- ==== NEW: range thresholds (meters) ====
-EXP_R0 = 30.0      -- 0–30      -> point blank
-EXP_R1 = 80.0      -- 30–80     -> mid
-EXP_R2 = 170.0     -- 80–150    -> far
-EXP_MAX = 400.0    -- beyond this we clamp falloff but still faintly audible
-
--- Falloff tuning: simple, smooth, monotonic
-EXP_MIN_VOL = 0.04   -- floor at max distance (~-28 dB)
-EXP_SHAPE   = 0.75   -- 0.5=gentler, 1.0=linear toward zero
-
-local function explosionFalloff(dist)
+#version 2
+FAKE_WHISTLE_DIST = 200.0   -- volume
+FAKE_EXP_BANK_DIST = 170.0  -- bank se
+FAKE_EXP_VOL_DIST  = 200.0  -- volume 
+eToolLock = false
+
+local func
+
+on explosionFalloff(dist)
     -- Normalize to [0..1] across EXP_MAX and shape the drop
     local t = math.max(0.0, math.min(1.0, dist / EXP_MAX))
     local v = (1.0 - t) ^ EXP_SHAPE
     return math.max(EXP_MIN_VOL, v)
 end
 
-local function pickExplosionBank(dist)
+local func
+
+on pickExplosionBank(dist)
     if dist < EXP_R0 then
         return expPointBlank
     elseif dist < EXP_R1 then
@@ -125,55 +27,51 @@
     end
 end
 
---drone button pulse
-local function pulseAlpha(speed, minA, maxA)
+--drone bu
+
+on pulseAlpha(speed, minA, maxA)
     local t = GetTime() * (speed or 4.0)
     local s = 0.5 + 0.5 * math.sin(t)
     return (minA or 0.45) + s * ((maxA or 1.0) - (minA or 0.45))
 end
 
--- ==========================================================
--- DRONE LISTENER ROUTING (revised)
--- ==========================================================
-local DRONE_FAKE_WHISTLE_DIST = 200.0   -- volume target for whistles
-local DRONE_FAKE_EXP_BANK_DIST = 170.0  -- bank selection target for explosions
-local DRONE_FAKE_EXP_VOL_DIST  = 200.0  -- volume target for explosions
-
-local function camPos()
+-- =======
+
+on camPos()
     return GetCameraTransform().pos
 end
 
--- Mid/far whistle volume as if 200 m from player
-local function droneWhistleGain200()
+-- Mid/far
+
+on droneWhistleGain200()
     return math.min(1.0, (WHISTLE_VOL or 1.0) * explosionFalloff(DRONE_FAKE_WHISTLE_DIST))
 end
 
--- Explosion bank/volume for drone view:
--- bank is chosen as if 150 m, volume as if 200 m (your spec)
-local function droneExplosionBank150Vol200()
+-- Explosi
+
+on droneExplosionBank150Vol200()
     local bank = pickExplosionBank(DRONE_FAKE_EXP_BANK_DIST)
     local vol  = explosionFalloff(DRONE_FAKE_EXP_VOL_DIST)
     return bank, vol
 end
 
-
-
--- === Vehicle lock state ===
-local vehicleToolLock = false
-
-local function IsPlayerInVehicle()
+-- === V
+
+on IsPlayerInVehicle()
     -- GetPlayerVehicle returns 0 if not in a vehicle
-    local v = GetPlayerVehicle and GetPlayerVehicle() or 0
+    local v = GetPlayerVehicle and GetPlayerVehicle(playerId) or 0
     return v ~= 0
 end
 
-local function UpdateVehicleToolLock()
+local func
+
+on UpdateVehicleToolLock()
     local inVeh = IsPlayerInVehicle()
 
     -- Hide/disable the barrage tool while seated so it can't be selected or used
     if inVeh and not vehicleToolLock then
         if GetBool("game.tool.barragere.enabled") then
-            SetBool("game.tool.barragere.enabled", false)
+            SetBool("game.tool.barragere.enabled", false, true)
         end
         vehicleToolLock = true
         -- If the circle UI was open when entering a vehicle, close it quietly
@@ -187,47 +85,46 @@
         end
     elseif (not inVeh) and vehicleToolLock then
         -- Re-enable tool once you exit the vehicle
-        SetBool("game.tool.barragere.enabled", true)
+        SetBool("game.tool.barragere.enabled", true, true)
         vehicleToolLock = false
     end
 
     return inVeh
 end
 
-
-
-
-function intensityLabelAndMax(intensity)
+functio
+
+ensityLabelAndMax(intensity)
 	if intensity == 1.0 then return I.t("intensity_high"), 5.0
 	elseif intensity == 2.0 then return I.t("intensity_med"), 20.0
 	else return I.t("intensity_low"), 60.0 end
 end
 
-
-function init()
+function 
+
+t()
     RegisterTool("barragere", "Artillery Support Radio", "vox/radio.vox")
-    SetBool("game.tool.barragere.enabled", true)
+    SetBool("game.tool.barragere.enabled", true, true)
 
     -- Ensure keys exist with safe defaults (so new subscribers get sane values immediately)
     if not HasKey("savegame.mod.barragere.howitzers") then
-        SetInt("savegame.mod.barragere.howitzers", 1)
+        SetInt("savegame.mod.barragere.howitzers", 1, true)
     end
     if not HasKey("savegame.mod.barragere.shellsPerHowitzer") then
-        SetInt("savegame.mod.barragere.shellsPerHowitzer", 1)
+        SetInt("savegame.mod.barragere.shellsPerHowitzer", 1, true)
     end
     if not HasKey("savegame.mod.barragere.barrageIntensity") then
-        SetFloat("savegame.mod.barragere.barrageIntensity", 1.0) -- High
+        SetFloat("savegame.mod.barragere.barrageIntensity", 1.0, true) -- High
     end
     if not HasKey("savegame.mod.barragere.baseReload") then
-        SetFloat("savegame.mod.barragere.baseReload", 10.0)
+        SetFloat("savegame.mod.barragere.baseReload", 10.0, true)
     end
     if not HasKey("savegame.mod.barragere.disableReloadCooldown") then
-        SetBool("savegame.mod.barragere.disableReloadCooldown", false)
+        SetBool("savegame.mod.barragere.disableReloadCooldown", false, true)
     end
 	if not HasKey("savegame.mod.barragere.disablePlayerDamage") then
-		SetBool("savegame.mod.barragere.disablePlayerDamage", false)  -- was true
-	end
-
+		SetBool("savegame.mod.barragere.disablePlayerDamage", false, true)  -- was true
+	end
 
     -- Read and CLAMP in case old bad values exist (e.g., 0 shells)
     barrageHowitzers = math.max(1, math.min(10, GetInt("savegame.mod.barragere.howitzers", 1)))
@@ -236,7 +133,7 @@
     local bi = GetFloat("savegame.mod.barragere.barrageIntensity", 1.0)
     if bi ~= 1.0 and bi ~= 2.0 and bi ~= 3.0 then
         bi = 1.0
-        SetFloat("savegame.mod.barragere.barrageIntensity", bi)
+        SetFloat("savegame.mod.barragere.barrageIntensity", bi, true)
     end
     barrageIntensity = bi
 
@@ -244,32 +141,20 @@
     disableReloadCooldown = GetBool("savegame.mod.barragere.disableReloadCooldown", false)
 
     -- If we clamped anything, write it back so the save is clean
-    SetInt("savegame.mod.barragere.howitzers", barrageHowitzers)
-    SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer)
-    SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity)
-    SetFloat("savegame.mod.barragere.baseReload", baseReload)
+    SetInt("savegame.mod.barragere.howitzers", barrageHowitzers, true)
+    SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer, true)
+    SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity, true)
+    SetFloat("savegame.mod.barragere.baseReload", baseReload, true)
 
     totalBarrageShots = barrageHowitzers * shellsPerHowitzer
 end
 
-
--- =======================================
--- Circle UI Global Variables (new)
--- =======================================
-circleUIActive = false
-circlePos = nil
-circleRadius = 5.0
-
--- We'll use this to slightly delay the radio sound,
--- so the camera can return to the player's actual position
-radioSoundDelay = -1.0
-radioPlayed = false
-
-function tick(dt)
+-- ======
+
+k(dt)
 
     local inVehicle = UpdateVehicleToolLock()
     local currentTime = GetTime()
-
 
     -- Fire logic for live howitzers
     if howitzerState then
@@ -277,7 +162,7 @@
             -- Play pre-boom sound
 			-- Play pre-boom (incoming) at player; STRONG distance falloff + gentle urgency
 			if not hw.soundPlayed and currentTime >= hw.nextFireTime - preExplosionSoundTime then
-				local playerPos = GetPlayerPos()
+				local playerPos = GetPlayerPos(playerId)
 
 				-- PLAN the exact impact for this upcoming shell (once), so whistles match the real hit
 				if not hw.nextImpactPos then
@@ -303,10 +188,8 @@
 					end
 				end
 
-
 				-- Battery thumps unchanged (constant)
 				PlaySound(artillerySounds[math.random(#artillerySounds)], droneActive and camPos() or playerPos, 0.4)
-
 
 				hw.soundPlayed = true
 			end
@@ -322,7 +205,7 @@
 					end
 
 					-- Only for players within "close" range, to avoid overlap with mid/far
-					local playerPos = GetPlayerPos()
+					local playerPos = GetPlayerPos(playerId)
 					local distNow = VecLength(VecSub(impactPos, playerPos))
 					if distNow < 85.0 then
 						local base = explosionFalloff(distNow)
@@ -342,7 +225,6 @@
 					hw.closeWhistlePlayed = true
 				end
 			end
-
 
 	
 			if hw.shellsLeft > 0 and currentTime >= hw.nextFireTime then
@@ -360,15 +242,15 @@
 				do
 					if droneActive then
 						local bank, vol = droneExplosionBank150Vol200()
-						if #bank > 0 then
+						if #bank ~= 0 then
 							PlaySound(bank[math.random(#bank)], camPos(), vol)
 						end
 					else
-						local playerPos = GetPlayerPos()
+						local playerPos = GetPlayerPos(playerId)
 						local dist = VecLength(VecSub(impactPos, playerPos))
 						local bank = pickExplosionBank(dist)
 						local vol  = explosionFalloff(dist)
-						if #bank > 0 then
+						if #bank ~= 0 then
 							PlaySound(bank[math.random(#bank)], playerPos, vol)
 						end
 					end
@@ -382,7 +264,7 @@
 				hw.lastImpactTime   = currentTime          -- when this shell hit
 				hw.impactTextUntil  = currentTime + 2.0    -- show IMPACT for 2s
 
-				if hw.shellsLeft > 0 then
+				if hw.shellsLeft ~= 0 then
 					if not strikeCancelled then
 						local extraDelay = getIntensityDelay(barrageIntensity)
 						hw.nextFireTime = currentTime + baseReload + extraDelay
@@ -400,7 +282,7 @@
 	if howitzerState then
 		local anyShellsLeft = false
 		for _, hw in ipairs(howitzerState) do
-			if hw.shellsLeft > 0 then
+			if hw.shellsLeft ~= 0 then
 				anyShellsLeft = true
 				break
 			end
@@ -421,7 +303,6 @@
 	end
 	
 
-
 	-- Tool activation / toggling
 	if GetString("game.player.tool") == "barragere" and not inVehicle then
 		SetToolTransform(Transform(Vec(0.4, -0.2, -0.7), QuatEuler(0, -15, 0)))
@@ -455,7 +336,7 @@
     -- Delayed radio sound
     if radioSoundDelay > 0 and currentTime >= radioSoundDelay then
         radioSoundDelay = -1
-        PlaySound(radioSound, GetPlayerPos(), 1.0)
+        PlaySound(radioSound, GetPlayerPos(playerId), 1.0)
     end
 	
 	-- Cancel only when the barrage tool is selected (MMB only)
@@ -476,16 +357,16 @@
 		end
 
 		-- Optional: exit on player death (keeps spec parity, separate from damage vignette)
-		if GetPlayerHealth and GetPlayerHealth() <= 0 then
+		if GetPlayerHealth and GetPlayerHealth(playerId) <= 0 then
 			exitDroneView()
 		end
 	end
 
-
-end
-
-
-function draw()
+end
+
+function 
+
+w()
 
 	if droneActive then
 		drawDroneView()
@@ -569,7 +450,9 @@
     end
 end
 
-function findExplosionSurface(pos)
+function f
+
+dExplosionSurface(pos)
     local skyStart = Vec(pos[1], pos[2] + 500, pos[3])
     local downDir = Vec(0, -1, 0)
     local hit, dist = QueryRaycast(skyStart, downDir, 1000)
@@ -580,9 +463,9 @@
     end
 end
 
-
-----------------------------------------------------------------------
-function startBarrage(targetPos, chosenRadius)
+---------
+
+rtBarrage(targetPos, chosenRadius)
     if not targetPos then return end
 
     -- Block starting if a strike is already running, just in case.
@@ -617,15 +500,18 @@
     end
 end
 
-
-function getCrosshairHit()
+function getC
+
+shairHit()
     local cam = GetCameraTransform()
     local origin, direction = cam.pos, TransformToParentVec(cam, Vec(0, 0, -1))
     local hit, dist = QueryRaycast(origin, direction, 5000)
     return hit, hit and VecAdd(origin, VecScale(direction, dist)) or nil
 end
 
-function apply3DAccuracyOffset(pos, radius)
+function apply
+
+AccuracyOffset(pos, radius)
     return VecAdd(pos, Vec(
         (math.random() * 2 - 1) * radius,
         (math.random() * 2 - 1) * radius * 0.75,
@@ -633,19 +519,21 @@
     ))
 end
 
-function exitDroneView()
+function exitD
+
+neView()
 	droneActive = false
 	droneCenter = nil
 	dronePos = nil
 end
 
-
--- Wrap the existing MMB cancel logic so we can call it from UI buttons too
-function cancelStrikeNow()
+-- Wrap the e
+
+trikeNow()
 	if howitzerState or cooldownActive then
 		if howitzerState then
 			for _, hw in ipairs(howitzerState) do
-				if hw.shellsLeft > 0 then
+				if hw.shellsLeft ~= 0 then
 					if hw.soundPlayed then
 						hw.shellsLeft = 1
 					else
@@ -659,12 +547,9 @@
 	end
 end
 
-
-
-----------------------------------------------------------------------
--- CIRCLE SELECTION UI CODE
-----------------------------------------------------------------------
-function initCircleSelection()
+------------
+
+cleSelection()
     local cam = GetCameraTransform()
     local dir = TransformToParentVec(cam, Vec(0, 0, -1))
     local hit, dist = QueryRaycast(cam.pos, dir, 1000)
@@ -676,7 +561,9 @@
     end
 end
 
-function updateCircleSelection(dt)
+function updat
+
+ircleSelection(dt)
     local scroll = InputValue("mousewheel")
     if scroll ~= 0 then
         local step = math.floor(scroll)
@@ -696,7 +583,6 @@
 			local camRot = QuatAlignXZ(Vec(1, 0, 0), Vec(0, 1, 0))
 
 			SetCameraTransform(Transform(camPos, camRot))
-
 
 		else
 			-- ANGLED: your original side/height offsets
@@ -729,7 +615,6 @@
 		if rl > 0.0001 then right   = VecScale(right,   1.0/rl) else right   = Vec(1,0, 0) end
 	end
 
-
 	-- Movement input
 	local moveDir = Vec(0, 0, 0)
 	if InputDown("w") then moveDir = VecAdd(moveDir, forward) end
@@ -754,7 +639,9 @@
 	end
 end
 
-function drawCircleSelection()
+function drawC
+
+cleSelection()
     if not circlePos then return end
     drawCircleLines(circlePos, circleRadius)
 
@@ -929,8 +816,6 @@
 		end
 	end
 
-
-
 		
 		
 
@@ -971,14 +856,14 @@
             if UiTextButton("-", BTN_W, BTN_H) then
                 barrageHowitzers = math.max(1, barrageHowitzers - 1)
                 totalBarrageShots = barrageHowitzers * shellsPerHowitzer
-                SetInt("savegame.mod.barragere.howitzers", barrageHowitzers)
+                SetInt("savegame.mod.barragere.howitzers", barrageHowitzers, true)
             end
             UiTranslate(BTN_W + BTN_GAP, 0)
             UiColor(0.2, 1, 0.2, 1)  -- plus
             if UiTextButton("+", BTN_W, BTN_H) then
                 barrageHowitzers = math.min(10, barrageHowitzers + 1)
                 totalBarrageShots = barrageHowitzers * shellsPerHowitzer
-                SetInt("savegame.mod.barragere.howitzers", barrageHowitzers)
+                SetInt("savegame.mod.barragere.howitzers", barrageHowitzers, true)
             end
         UiPop()
 
@@ -994,14 +879,14 @@
             if UiTextButton("-", BTN_W, BTN_H) then
                 shellsPerHowitzer = math.max(1, shellsPerHowitzer - 1)
                 totalBarrageShots = barrageHowitzers * shellsPerHowitzer
-                SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer)
+                SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer, true)
             end
             UiTranslate(BTN_W + BTN_GAP, 0)
             UiColor(0.2, 1, 0.2, 1)
             if UiTextButton("+", BTN_W, BTN_H) then
                 shellsPerHowitzer = math.min(20, shellsPerHowitzer + 1)
                 totalBarrageShots = barrageHowitzers * shellsPerHowitzer
-                SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer)
+                SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer, true)
             end
         UiPop()
 
@@ -1016,13 +901,13 @@
             UiColor(1, 0.2, 0.2, 1)
             if UiTextButton("-", BTN_W, BTN_H) then
                 baseReload = math.max(6, baseReload - 1)
-                SetFloat("savegame.mod.barragere.baseReload", baseReload)
+                SetFloat("savegame.mod.barragere.baseReload", baseReload, true)
             end
             UiTranslate(BTN_W + BTN_GAP, 0)
             UiColor(0.2, 1, 0.2, 1)
             if UiTextButton("+", BTN_W, BTN_H) then
                 baseReload = math.min(60, baseReload + 1)
-                SetFloat("savegame.mod.barragere.baseReload", baseReload)
+                SetFloat("savegame.mod.barragere.baseReload", baseReload, true)
             end
         UiPop()
 
@@ -1039,7 +924,7 @@
                 if active then UiColor(0.20, 0.95, 0.20, 1.0) else UiColor(0.65, 0.65, 0.65, 1.0) end
                 if UiTextButton(name, INT_W, INT_H) then
                     barrageIntensity = val
-                    SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity)
+                    SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity, true)
                 end
             end
             intensityBtn(I.t("intensity_low"),  3.0); UiTranslate(INT_W + INT_GAP, 0)
@@ -1070,7 +955,6 @@
 		local panelW, panelH = UiEndFrame()
 	UiPop()
 
-
     -- 2) Place panel flush to bottom-left with margin
     local bgW  = math.max(MIN_WIDTH, math.ceil(panelW))
     local bgH  = math.ceil(panelH)
@@ -1084,8 +968,6 @@
     -- 3) Draw actual content at the placed position
     drawSelectionSettingsPanelContent()
 UiPop()
-
-
 
 --================================================================================================================================---
 
@@ -1123,17 +1005,12 @@
         end
     UiPop()
 
-
-
     UiModalEnd()
 end
 
-
---==============================================================
--- DRONE VIEW
---==============================================================
-function initDroneView()
-    if not howitzerState or not barrageTarget or not barrageAccuracy then return end
+--=====================
+
+   if not howitzerState or not barrageTarget or not barrageAccuracy then return end
 
     droneActive  = true
     droneCenter  = VecCopy(barrageTarget)
@@ -1157,7 +1034,9 @@
     droneZoom = 1.0
 end
 
-function updateDroneView(dt)
+function updateDroneView
+
+t)
 	-- Zoom (same 1..10 envelope used by your selection overlay)
 	local scroll = InputValue("mousewheel")
 	if scroll ~= 0 then
@@ -1207,9 +1086,9 @@
 
 end
 
-
-
-local function countTotalShells()
+local function countTo
+
+hells()
 	local total = 0
 	if howitzerState then
 		for _, hw in ipairs(howitzerState) do
@@ -1219,7 +1098,9 @@
 	return total
 end
 
-local function drawBarragePanelContent(listLineH)
+local function drawBarra
+
+PanelContent(listLineH)
 	UiColor(1, 1, 1, 1)
 	UiTranslate(16, 16)
 
@@ -1249,7 +1130,6 @@
 	UiText(I.t("total_shells", countTotalShells()))
 
 	UiTranslate(0, 24)   -- clear space before first howitzer row
-
 
 	-- Howitzers list (with spacing and status rename)
 -- Howitzers list (row spacing + correctly aligned IMPACT)
@@ -1304,12 +1184,12 @@
 UiColor(0, 0, 0, 0)     -- invisible
 UiRect(1, PANEL_BOTTOM_PAD)
 
-
-end
-
+end
 
 function drawDroneView()
-	if not droneActive then return end
+	if not dro
+
+ctive then return end
 
 	UiMakeInteractive()
 	UiModalBegin()
@@ -1344,8 +1224,6 @@
 		UiText(zoomText)
 	UiPop()
 
-
-
 	-- right-side camera icon (reuse your art if present)
 	UiPush()
 	UiAlign("middle right")
@@ -1414,10 +1292,9 @@
 			UiFont("bold.ttf", 18)
 			if UiTextButton(I.t("hide_window"), BTN_W, BTN_H) then
 				dronePanelVisible = false
-				SetBool("savegame.mod.barragere.dronePanelVisible", false)
+				SetBool("savegame.mod.barragere.dronePanelVisible", false, true)
 			end
 		UiPop()
-
 
 		-- pass 2: draw contents
 		drawBarragePanelContent(22)
@@ -1439,13 +1316,12 @@
 		UiColor(1, 1, 1, 1)
 		if UiTextButton(label, tw, th) then
 			dronePanelVisible = true
-			SetBool("savegame.mod.barragere.dronePanelVisible", true)
+			SetBool("savegame.mod.barragere.dronePanelVisible", true, true)
 		end
 
 	end
 
 	UiPop()
-
 
 	-- Bottom‑center action row: Cancel / Quit Drone View
 	UiPush()
@@ -1472,11 +1348,9 @@
 	UiModalEnd()
 end
 
-
-
-
-function drawCircleLines(pos, radius)
-    local segments = 32
+function drawCircleLines(pos, radius
+
+ local segments = 32
     local up = Vec(0, 0.01, 0)
     for i = 1, segments do
         local angle1 = (i / segments) * math.pi * 2
@@ -1488,13 +1362,17 @@
 end
 
 function math.clamp(val, min, max)
-    if val < min then return min end
+    
+
+ val < min then return min end
     if val > max then return max end
     return val
 end
 
 function getIntensityDelay(intensity)
-    if intensity <= 1.0 then
+ 
+
+ if intensity <= 1.0 then
         return math.random() * 5.0       -- High intensity: fast repeat
     elseif intensity <= 2.0 then
         return math.random() * 20.0      -- Medium intensity

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
@@ -1,265 +1,247 @@
-#include "i18n.lua"
-
-
-function init()
-
-	if not HasKey("savegame.mod.barragere.baseReload") then
-		SetFloat("savegame.mod.barragere.baseReload", 10.0)
-	end
-	if not HasKey("savegame.mod.barragere.howitzers") then
-		SetInt("savegame.mod.barragere.howitzers", 1)
-	end
-	if not HasKey("savegame.mod.barragere.shellsPerHowitzer") then
-		SetInt("savegame.mod.barragere.shellsPerHowitzer", 1)
-	end
-	if not HasKey("savegame.mod.barragere.barrageIntensity") then
-		SetFloat("savegame.mod.barragere.barrageIntensity", 1.0)
-	end
-
-	if not HasKey("savegame.mod.barragere.disablePlayerDamage") then
-		SetBool("savegame.mod.barragere.disablePlayerDamage", false)  -- was true
-	end
-	local playerDamageEnabled = not GetBool("savegame.mod.barragere.disablePlayerDamage", false)
-
-
-	barrageHowitzers    = GetInt("savegame.mod.barragere.howitzers")
-	shellsPerHowitzer   = GetInt("savegame.mod.barragere.shellsPerHowitzer")
-	barrageIntensity    = GetFloat("savegame.mod.barragere.barrageIntensity")
-	baseReload          = GetFloat("savegame.mod.barragere.baseReload", 10.0)
-
-	if baseReload < 6.0 then
-		baseReload = 6.0
-		SetFloat("savegame.mod.barragere.baseReload", baseReload)
-	end
+#version 2
+function server.init()
+    if not HasKey("savegame.mod.barragere.baseReload") then
+    	SetFloat("savegame.mod.barragere.baseReload", 10.0, true)
+    end
+    if not HasKey("savegame.mod.barragere.howitzers") then
+    	SetInt("savegame.mod.barragere.howitzers", 1, true)
+    end
+    if not HasKey("savegame.mod.barragere.shellsPerHowitzer") then
+    	SetInt("savegame.mod.barragere.shellsPerHowitzer", 1, true)
+    end
+    if not HasKey("savegame.mod.barragere.barrageIntensity") then
+    	SetFloat("savegame.mod.barragere.barrageIntensity", 1.0, true)
+    end
+    if not HasKey("savegame.mod.barragere.disablePlayerDamage") then
+    	SetBool("savegame.mod.barragere.disablePlayerDamage", false, true)  -- was true
+    end
+    local playerDamageEnabled = not GetBool("savegame.mod.barragere.disablePlayerDamage", false)
+    barrageHowitzers    = GetInt("savegame.mod.barragere.howitzers")
+    shellsPerHowitzer   = GetInt("savegame.mod.barragere.shellsPerHowitzer")
+    barrageIntensity    = GetFloat("savegame.mod.barragere.barrageIntensity")
+    baseReload          = GetFloat("savegame.mod.barragere.baseReload", 10.0)
+    if baseReload < 6.0 then
+    	baseReload = 6.0
+    	SetFloat("savegame.mod.barragere.baseReload", baseReload, true)
+    end
 end
 
-function draw()
-	----------------------------------------------------------------
-	-- FULLSCREEN BACKGROUND (cover)
-	UiPush()
-		local cw, ch = UiWidth(), UiHeight()
-
-
-		UiPush()
-			UiColor(1,1,1,0)  
-			UiBeginFrame()
-				UiImage("MOD/UI/optionsbg.png")
-			local iw, ih = UiEndFrame()
-		UiPop()
-
-		if iw and ih and iw > 0 and ih > 0 then
-
-			local s = math.max(cw/iw, ch/ih)
-			UiPush()
-				UiTranslate(cw*0.5, ch*0.5)
-				UiAlign("center middle")
-				UiScale(s)
-				UiImage("MOD/UI/optionsbg.png")
-			UiPop()
-		else
-
-			UiImage("MOD/UI/optionsbg.png")
-		end
-	UiPop()
-	----------------------------------------------------------------
-
-	----------------------------------------------------------------
-	local x0, y0, x1, y1 = UiSafeMargins()  
-	UiPush()
-		UiTranslate(x0, y0)
-		UiWindow(x1 - x0, y1 - y0, true)     -- clip to safe area (important)
-		UiAlign("top left")
-
-		-- Layout constants
-		local leftPad   = 40
-		local topPad    = 36
-		local colW      = 900           -- width for each option card
-		local innerPadX = 22
-		local innerPadY = 16
-		local gapY      = 16
-
-		-- Typography
-		UiFont("bold.ttf", 26)
-		UiTextShadow(0,0,0,0.65, 2.0)   -- readable on any bg
-		UiWordWrap(colW - innerPadX*2)  -- wrap RU safely
-
-
-		local function Boxed(title, controlsDrawer, extraH)
-			-- constants
-			local wrapW    = colW - innerPadX*2
-			local titleGap = 22          -- spacing between title and controls
-			local controlH = 40          -- single-row controls height
-			extraH = extraH or 0         -- extra vertical height (e.g., for a second line)
-
-			-- measure TITLE invisibly (no shadow)
-			UiPush()
-				UiTextShadow(0,0,0,0, 0)
-				UiColor(1,1,1,0)
-				UiWordWrap(wrapW)
-				UiBeginFrame()
-					UiText(title)
-				local _, th = UiEndFrame()
-			UiPop()
-
-			local totalH = th + titleGap + controlH + extraH
-			local boxH   = totalH + innerPadY*2
-
-			-- background
-			UiPush()
-				UiColor(0,0,0,0.55)
-				UiRoundedRect(colW, boxH, 6)
-			UiPop()
-
-			-- content clipped to the box
-			UiTranslate(innerPadX, innerPadY)
-			UiPush()
-				UiClipRect(wrapW, totalH, true)
-
-				-- draw title with your normal style
-				UiWordWrap(wrapW)
-				UiText(title)
-				UiTranslate(0, titleGap)
-
-				-- draw controls (real draw)
-				controlsDrawer()
-			UiPop()
-
-			-- move cursor to after the box
-			UiTranslate(-innerPadX, boxH - innerPadY)
-		end
-
-
-
-		-- helper: +/- row (colored)
-		local function Stepper(getter, setter, step, minv, maxv)
-			step = step or 1
-			UiPush()
-				UiColor(1, 0.6, 0.6, 1)
-				if UiTextButton("-") then
-					local v = math.max(minv, getter() - step)
-					setter(v)
-				end
-				UiTranslate(64, 0)
-				UiColor(0.6, 1, 0.6, 1)
-				if UiTextButton("+") then
-					local v = math.min(maxv, getter() + step)
-					setter(v)
-				end
-				UiColor(1,1,1,1)
-			UiPop()
-		end
-
-		-- STATE setters used by the steppers
-		local function setHow(v) SetInt("savegame.mod.barragere.howitzers", v); barrageHowitzers = v end
-		local function getHow() return barrageHowitzers end
-		local function setSh(v) SetInt("savegame.mod.barragere.shellsPerHowitzer", v); shellsPerHowitzer = v end
-		local function getSh() return shellsPerHowitzer end
-		local function setRl(v) SetFloat("savegame.mod.barragere.baseReload", v); baseReload = v end
-		local function getRl() return baseReload end
-
-		-- start column
-		UiTranslate(leftPad, topPad)
-
-		-- Header (separate, with a translucent strip)
-		do
-			local barW, barH = colW, 40
-			UiPush()
-				UiColor(0,0,0,0.35)
-				UiRoundedRect(barW, barH, 6)
-			UiPop()
-			UiTranslate(12, 7)
-			UiFont("bold.ttf", 28)
-			UiText(I.t("menu_title"))
-			UiFont("bold.ttf", 26)
-			UiTranslate(-12, barH - 7 + 14)
-		end
-
-		-- Howitzers
-		Boxed(I.t("howitzers_label", barrageHowitzers), function()
-			Stepper(getHow, setHow, 1, 1, 10)
-		end)
-		UiTranslate(0, gapY)
-
-		-- Shells per Howitzer
-		Boxed(I.t("shells_label", shellsPerHowitzer), function()
-			Stepper(getSh, setSh, 1, 1, 20)
-		end)
-		UiTranslate(0, gapY)
-
-
-		Boxed(I.t("intensity_title"), function()
-			-- buttons row
-			local step = 200
-			if UiTextButton(I.t("intensity_low"))  then
-				barrageIntensity = 3.0
-				SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity)
-			end
-			UiTranslate(step, 0)
-			if UiTextButton(I.t("intensity_med"))  then
-				barrageIntensity = 2.0
-				SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity)
-			end
-			UiTranslate(step, 0)
-			if UiTextButton(I.t("intensity_high")) then
-				barrageIntensity = 1.0
-				SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity)
-			end
-
-
-			UiTranslate(-step*2, 36)
-			local sel = (barrageIntensity == 1.0 and I.t("intensity_high")
-					  or (barrageIntensity == 2.0 and I.t("intensity_med") or I.t("intensity_low")))
-			UiText(I.t("selected_label", sel))
-		end, 24 + 26)   -- extraH = gap(24) + approx one text line(~26)
-
-
-
-		Boxed(I.t("reload_label", baseReload), function()
-			Stepper(getRl, setRl, 1, 6, 60)
-		end)
-		UiTranslate(0, gapY)
-
-
-		Boxed(I.t("player_damage_title"), function()
-			local dmgDisabled = GetBool("savegame.mod.barragere.disablePlayerDamage")
-			local label = (not dmgDisabled) and I.t("enabled") or I.t("disabled")
-			if UiTextButton(label) then
-				SetBool("savegame.mod.barragere.disablePlayerDamage", not dmgDisabled)
-			end
-		end)
-		UiTranslate(0, gapY)
-
-		-- Language
-		Boxed(I.t("lang_title"), function()
-			local cur = I.getLang()
-			if cur == "en" then UiColor(0.8,1,0.8,1) else UiColor(1,1,1,1) end
-			if UiTextButton(I.t("lang_en")) then I.setLang("en") end
-			UiTranslate(200, 0)
-			UiColor(1,1,1,1)
-			if cur == "ru" then UiColor(0.8,1,0.8,1) else UiColor(1,1,1,1) end
-			if UiTextButton(I.t("lang_ru")) then I.setLang("ru") end
-			UiColor(1,1,1,1)
-		end)
-		UiTranslate(0, gapY)
-
-		-- Reset to Defaults
-		Boxed(I.t("reset_defaults"), function()
-			UiPush()
-				UiColor(1, 0.35, 0.35, 1)      -- red button
-				if UiTextButton(I.t("reset_defaults")) then
-					barrageHowitzers   = 1
-					shellsPerHowitzer  = 1
-					barrageIntensity   = 1.0
-					baseReload         = math.max(6.0, 10.0)
-					SetInt("savegame.mod.barragere.howitzers", barrageHowitzers)
-					SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer)
-					SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity)
-					SetFloat("savegame.mod.barragere.baseReload", baseReload)
-					SetBool("savegame.mod.barragere.disablePlayerDamage", false)
-				end
-			UiPop()
-		end)
-
-
-	UiPop()
+function client.draw()
+    UiPush()
+    	local cw, ch = UiWidth(), UiHeight()
+
+    	UiPush()
+    		UiColor(1,1,1,0)  
+    		UiBeginFrame()
+    			UiImage("MOD/UI/optionsbg.png")
+    		local iw, ih = UiEndFrame()
+    	UiPop()
+
+    	if iw and ih and iw > 0 and ih ~= 0 then
+
+    		local s = math.max(cw/iw, ch/ih)
+    		UiPush()
+    			UiTranslate(cw*0.5, ch*0.5)
+    			UiAlign("center middle")
+    			UiScale(s)
+    			UiImage("MOD/UI/optionsbg.png")
+    		UiPop()
+    	else
+
+    		UiImage("MOD/UI/optionsbg.png")
+    	end
+    UiPop()
+    ----------------------------------------------------------------
+
+    ----------------------------------------------------------------
+    local x0, y0, x1, y1 = UiSafeMargins()  
+    UiPush()
+    	UiTranslate(x0, y0)
+    	UiWindow(x1 - x0, y1 - y0, true)     -- clip to safe area (important)
+    	UiAlign("top left")
+
+    	-- Layout constants
+    	local leftPad   = 40
+    	local topPad    = 36
+    	local colW      = 900           -- width for each option card
+    	local innerPadX = 22
+    	local innerPadY = 16
+    	local gapY      = 16
+
+    	-- Typography
+    	UiFont("bold.ttf", 26)
+    	UiTextShadow(0,0,0,0.65, 2.0)   -- readable on any bg
+    	UiWordWrap(colW - innerPadX*2)  -- wrap RU safely
+
+    	local function Boxed(title, controlsDrawer, extraH)
+    		-- constants
+    		local wrapW    = colW - innerPadX*2
+    		local titleGap = 22          -- spacing between title and controls
+    		local controlH = 40          -- single-row controls height
+    		extraH = extraH or 0         -- extra vertical height (e.g., for a second line)
+
+    		-- measure TITLE invisibly (no shadow)
+    		UiPush()
+    			UiTextShadow(0,0,0,0, 0)
+    			UiColor(1,1,1,0)
+    			UiWordWrap(wrapW)
+    			UiBeginFrame()
+    				UiText(title)
+    			local _, th = UiEndFrame()
+    		UiPop()
+
+    		local totalH = th + titleGap + controlH + extraH
+    		local boxH   = totalH + innerPadY*2
+
+    		-- background
+    		UiPush()
+    			UiColor(0,0,0,0.55)
+    			UiRoundedRect(colW, boxH, 6)
+    		UiPop()
+
+    		-- content clipped to the box
+    		UiTranslate(innerPadX, innerPadY)
+    		UiPush()
+    			UiClipRect(wrapW, totalH, true)
+
+    			-- draw title with your normal style
+    			UiWordWrap(wrapW)
+    			UiText(title)
+    			UiTranslate(0, titleGap)
+
+    			-- draw controls (real draw)
+    			controlsDrawer()
+    		UiPop()
+
+    		-- move cursor to after the box
+    		UiTranslate(-innerPadX, boxH - innerPadY)
+    	end
+
+    	-- helper: +/- row (colored)
+    	local function Stepper(getter, setter, step, minv, maxv)
+    		step = step or 1
+    		UiPush()
+    			UiColor(1, 0.6, 0.6, 1)
+    			if UiTextButton("-") then
+    				local v = math.max(minv, getter() - step)
+    				setter(v)
+    			end
+    			UiTranslate(64, 0)
+    			UiColor(0.6, 1, 0.6, 1)
+    			if UiTextButton("+") then
+    				local v = math.min(maxv, getter() + step)
+    				setter(v)
+    			end
+    			UiColor(1,1,1,1)
+    		UiPop()
+    	end
+
+    	-- STATE setters used by the steppers
+    	local function setHow(v) SetInt("savegame.mod.barragere.howitzers", v, true); barrageHowitzers = v end
+    	local function getHow() return barrageHowitzers end
+    	local function setSh(v) SetInt("savegame.mod.barragere.shellsPerHowitzer", v, true); shellsPerHowitzer = v end
+    	local function getSh() return shellsPerHowitzer end
+    	local function setRl(v) SetFloat("savegame.mod.barragere.baseReload", v, true); baseReload = v end
+    	local function getRl() return baseReload end
+
+    	-- start column
+    	UiTranslate(leftPad, topPad)
+
+    	-- Header (separate, with a translucent strip)
+    	do
+    		local barW, barH = colW, 40
+    		UiPush()
+    			UiColor(0,0,0,0.35)
+    			UiRoundedRect(barW, barH, 6)
+    		UiPop()
+    		UiTranslate(12, 7)
+    		UiFont("bold.ttf", 28)
+    		UiText(I.t("menu_title"))
+    		UiFont("bold.ttf", 26)
+    		UiTranslate(-12, barH - 7 + 14)
+    	end
+
+    	-- Howitzers
+    	Boxed(I.t("howitzers_label", barrageHowitzers), function()
+    		Stepper(getHow, setHow, 1, 1, 10)
+    	end)
+    	UiTranslate(0, gapY)
+
+    	-- Shells per Howitzer
+    	Boxed(I.t("shells_label", shellsPerHowitzer), function()
+    		Stepper(getSh, setSh, 1, 1, 20)
+    	end)
+    	UiTranslate(0, gapY)
+
+    	Boxed(I.t("intensity_title"), function()
+    		-- buttons row
+    		local step = 200
+    		if UiTextButton(I.t("intensity_low"))  then
+    			barrageIntensity = 3.0
+    			SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity, true)
+    		end
+    		UiTranslate(step, 0)
+    		if UiTextButton(I.t("intensity_med"))  then
+    			barrageIntensity = 2.0
+    			SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity, true)
+    		end
+    		UiTranslate(step, 0)
+    		if UiTextButton(I.t("intensity_high")) then
+    			barrageIntensity = 1.0
+    			SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity, true)
+    		end
+
+    		UiTranslate(-step*2, 36)
+    		local sel = (barrageIntensity == 1.0 and I.t("intensity_high")
+    				  or (barrageIntensity == 2.0 and I.t("intensity_med") or I.t("intensity_low")))
+    		UiText(I.t("selected_label", sel))
+    	end, 24 + 26)   -- extraH = gap(24) + approx one text line(~26)
+
+    	Boxed(I.t("reload_label", baseReload), function()
+    		Stepper(getRl, setRl, 1, 6, 60)
+    	end)
+    	UiTranslate(0, gapY)
+
+    	Boxed(I.t("player_damage_title"), function()
+    		local dmgDisabled = GetBool("savegame.mod.barragere.disablePlayerDamage")
+    		local label = (not dmgDisabled) and I.t("enabled") or I.t("disabled")
+    		if UiTextButton(label) then
+    			SetBool("savegame.mod.barragere.disablePlayerDamage", not dmgDisabled, true)
+    		end
+    	end)
+    	UiTranslate(0, gapY)
+
+    	-- Language
+    	Boxed(I.t("lang_title"), function()
+    		local cur = I.getLang()
+    		if cur == "en" then UiColor(0.8,1,0.8,1) else UiColor(1,1,1,1) end
+    		if UiTextButton(I.t("lang_en")) then I.setLang("en") end
+    		UiTranslate(200, 0)
+    		UiColor(1,1,1,1)
+    		if cur == "ru" then UiColor(0.8,1,0.8,1) else UiColor(1,1,1,1) end
+    		if UiTextButton(I.t("lang_ru")) then I.setLang("ru") end
+    		UiColor(1,1,1,1)
+    	end)
+    	UiTranslate(0, gapY)
+
+    	-- Reset to Defaults
+    	Boxed(I.t("reset_defaults"), function()
+    		UiPush()
+    			UiColor(1, 0.35, 0.35, 1)      -- red button
+    			if UiTextButton(I.t("reset_defaults")) then
+    				barrageHowitzers   = 1
+    				shellsPerHowitzer  = 1
+    				barrageIntensity   = 1.0
+    				baseReload         = math.max(6.0, 10.0)
+    				SetInt("savegame.mod.barragere.howitzers", barrageHowitzers, true)
+    				SetInt("savegame.mod.barragere.shellsPerHowitzer", shellsPerHowitzer, true)
+    				SetFloat("savegame.mod.barragere.barrageIntensity", barrageIntensity, true)
+    				SetFloat("savegame.mod.barragere.baseReload", baseReload, true)
+    				SetBool("savegame.mod.barragere.disablePlayerDamage", false, true)
+    			end
+    		UiPop()
+    	end)
+
+    UiPop()
 end
+

```
