# Migration Report: gorescript\goreELITEterrorist.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/gorescript\goreELITEterrorist.lua
+++ patched/gorescript\goreELITEterrorist.lua
@@ -1,699 +1,4 @@
-function init()
-	Head = FindBody("Head")
-	HeadBloodCapacity = GetBodyMass(Head)
-	HeadBloodLevel = HeadBloodCapacity * 20
-	StartingBleed = HeadBloodCapacity
-	MaxBloodCapacity = GetBodyMass(Head)
-	bleed = true
-
-	Torso = FindBody("Torso")
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	TorsoBloodLevel = TorsoBloodCapacity * 20
-	StartingBleed1 = TorsoBloodCapacity
-	MaxBloodCapacity1 = GetBodyMass(Torso)
-	bleed1 = true
-
-	LARM = FindBody("LARM")
-	LARMBloodCapacity = GetBodyMass(LARM)
-	LARMBloodLevel = LARMBloodCapacity * 20
-	StartingBleed2 = LARMBloodCapacity
-	MaxBloodCapacity2 = GetBodyMass(LARM)
-
-	bleed2 = true
-
-	LLARM = FindBody("LLARM")
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	LLARMBloodLevel = LLARMBloodCapacity * 20
-	StartingBleed3 = LLARMBloodCapacity
-	MaxBloodCapacity3 = GetBodyMass(LLARM)
-	bleed3 = true
-
-	RARM = FindBody("RARM")
-	RARMBloodCapacity = GetBodyMass(RARM)
-	RARMBloodLevel = RARMBloodCapacity * 20
-	StartingBleed4 = RARMBloodCapacity
-	MaxBloodCapacity4 = GetBodyMass(RARM)
-	bleed4 = true
-
-	RRARM = FindBody("RRARM")
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	RRARMBloodLevel = RRARMBloodCapacity * 20
-	StartingBleed5 = RRARMBloodCapacity
-	MaxBloodCapacity5 = GetBodyMass(RRARM)
-	bleed5 = true
-
-	LLEG = FindBody("LLEG")
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	LLEGBloodLevel = LLEGBloodCapacity * 20
-	StartingBleed6 = LLEGBloodCapacity
-	MaxBloodCapacity6 = GetBodyMass(LLEG)
-	bleed6 = true
-
-	LLLEG = FindBody("LLLEG")
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	LLLEGBloodLevel = LLLEGBloodCapacity * 20
-	StartingBleed7 = LLLEGBloodCapacity
-	MaxBloodCapacity7 = GetBodyMass(LLLEG)
-	bleed7 = true
-
-	RLEG = FindBody("RLEG")
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	RLEGBloodLevel = RLEGBloodCapacity * 20
-	StartingBleed8 = RLEGBloodCapacity
-	MaxBloodCapacity8 = GetBodyMass(RLEG)
-	bleed8 = true
-
-	RRLEG = FindBody("RRLEG")
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	RRLEGBloodLevel = RRLEGBloodCapacity * 20
-	StartingBleed9 = RRLEGBloodCapacity
-	MaxBloodCapacity9 = GetBodyMass(RRLEG)
-	bleed9 = true
-
-	antibleed = 15 -- only affects smoke speed
-	extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
-	regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
-	limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
-	MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
-
-	LimbBleedSpeed = 0.1
-
-	bloodgrav = -20
-	blooddrag = 0
-	startupspeed = Vec(0,0.7,0)
-	upspeed = Vec(0,2,0)
-	downspeed = Vec(0,-0.7,0)
-	alive = true
-
-	akm = FindBody("AKM")
-	weight = 20
-	bias = Vec(0,0,0)
-	biasb = Vec(0,0,0)
-	weightb = -0.6
-	agrotimer = 0
-	forget = 10
-	KillTimer = 0
-	Eliminate = 1
-	shootim = 0
-	shots = 0
-	reload = 0
-	magsize = 95
-	firerate = 1.5
-	recoil = 2
-
-	flare = FindLight("flare")
-	flaretim = false
-	flaretimer = 0
-	SetLightEnabled(flare, false)
-	disarmed = false
-	spetsnaz = FindShape("spetsnaz",true)
-	GunShot = LoadSound("MOD/gorescript/akm.ogg")
-	enemyspotted = false
-		switched = true
-		enabled = true
-end
-
-
-function tick(dt)
-
-	if InputPressed("H") then
-		if switched then
-			enabled = false
-			switched = false
-		else if not switched then
-			enabled = true
-		switched = true
-		end
-	end
-end
-
-	if IsShapeBroken(spetsnaz) then
-		RemoveTag(spetsnaz,"spetsnaz")
-		agro = false
-		agrotimer = 0
-		spetsnaz = FindShape("spetsnaz",true)
-		enemyspotted = false
-		shoot = false
-	end
-
-	if PlayerHP == 0 then
-		shoot = false
-		agro = false
-		agrotimer = 0
-		enemyspotted = false
-	end
-	gunTrans = GetBodyTransform(Head)
-	gunPos = gunTrans.pos
-	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
-	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
-
-	drawtext = false
-
-	HeadBloodCapacity = GetBodyMass(Head)
-	Bleed = StartingBleed - HeadBloodCapacity
-	HeadPos = GetBodyTransform(Head)
-
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	Bleed1 = StartingBleed1 - TorsoBloodCapacity
-	TorsoPos = GetBodyTransform(Torso)
-
-	LARMBloodCapacity = GetBodyMass(LARM)
-	Bleed2 = StartingBleed2 - LARMBloodCapacity
-	LARMPos = GetBodyTransform(LARM)
-
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	Bleed3 = StartingBleed3 - LLARMBloodCapacity
-	LLARMPos = GetBodyTransform(LLARM)
-
-	RARMBloodCapacity = GetBodyMass(RARM)
-	Bleed4 = StartingBleed4 - RARMBloodCapacity
-	RARMPos = GetBodyTransform(RARM)
-
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	Bleed5 = StartingBleed5 - RRARMBloodCapacity
-	RRARMPos = GetBodyTransform(RRARM)
-
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	Bleed6 = StartingBleed6 - LLEGBloodCapacity
-	LLEGPos = GetBodyTransform(LLEG)
-
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
-	LLLEGPos = GetBodyTransform(LLLEG)
-
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	Bleed8 = StartingBleed8 - RLEGBloodCapacity
-	RLEGPos = GetBodyTransform(RLEG)
-
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
-	RRLEGPos = GetBodyTransform(RRLEG)
-
-	--AGRESSIVE BEHAVIOR
-
-	if IsBodyBroken(LLARM) then
-		disarmed = true
-	end
-
-	if canSeeSpetsnaz() then
-			agro = true
-		agrotimer = 0
-		KillTimer = KillTimer + dt
-		enemyspotted = true
-		shoot = true
-
-	end
-
-	if canSeePlayer() then
-		agro = true
-		agrotimer = 0
-		KillTimer = KillTimer + dt
-		enemyspotted = true
-		shoot = true
-		end
-		if agro then
-			agrotimer = agrotimer + dt
-		if agrotimer > forget then
-		agro = false
-		agrotimer = 0
-		KillTimer = 0
-	end
-end
-
-	--RELOAD
-	if shots > magsize then
-		reloading = true
-		if alive then
-		reload = reload + dt
-		if reload > 4 then
-			reloading = false
-			shots = 0
-			reload = 0
-		end
-	end
-	end
-
-
-	--ELIMINATE TARGET 
-	local barrel = FindShape("barrel")
-	local guntrans = GetShapeWorldTransform(barrel)
-	local terrorist = FindShape("terrorist")
-	terrorpos = GetShapeWorldTransform(terrorist)
-	--DebugPrint("guny:  "..guntrans.pos[2])
-	--DebugPrint("body:  "..terrorpos.pos[2])
-	if guntrans.pos[2] < terrorpos.pos[2] then
-		shoot = false
-	end
-    local gunpos = guntrans.pos
-	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
-    local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
-
-    if flaretim then
-    	flaretimer = flaretimer + dt
-    	if flaretimer > 0.1 then
-    		SetLightEnabled(flare, false)
-    		flaretimer = 0
-    	end
-    end
-    if shoot then
-	if KillTimer > Eliminate then
-		if not disarmed then
-		if not reloading then
-		shootim = shootim + dt * firerate
-		if shootim > 0.2 then
-		Shoot(shootpos, direction)
-		PlaySound(GunShot, shootpos,10)
-		SetLightEnabled(flare, true)
-		flaretim = true
-		for i=1,33 do
-		GunSmoke()
-	end
-		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
-		shootim = 0
-		shots = shots + 1
-	end
-end
-	end
-end
-end
-
-	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
-	if enemyspotted then
-	if not disarmed then
-	if alive then
-		if agro then
-	local ppos = GetPlayerCameraTransform()
-	ppos.pos[2] = ppos.pos[2] - 0.5
-	spetsnazpos = GetShapeWorldTransform(spetsnaz)
-	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
-	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
-
-
-
-	if distToPlayeraim > distToSpetsaim and canSeeSpetsnaz() then
-	enemy = spetsnazpos.pos
-else if distToPlayeraim > distToSpetsaim and not canSeeSpetsnaz() then
-	enemy = ppos.pos
-end
-end
-	if distToPlayeraim < distToSpetsaim and canSeePlayer() then
-	enemy = ppos.pos
-else if distToPlayeraim < distToSpetsaim and not canSeePlayer() then
-	enemy = spetsnazpos.pos
-end
-	end
-
-
-
-	local akmpos = GetBodyTransform(akm)
-
-	local aimangle = QuatLookAt(akmpos.pos, enemy)
-
-	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
-	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
-
-
---yaw
- gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
-  --pitch
- gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
-  --roll
- gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
- if agro then
-
- local bias = QuatEuler(gunyaw, gunpitch, gunroll)
-  SetBodyTransform(akm, Transform(akmpos.pos, bias))
-end
-end
-end
-
---b = GetBodyTransform(LLARM)
-  --for i=1,3 do
-        --if(ppos.pos[i]<b.pos[i]) then
-             --biasb[i] = -weightb
-        --elseif(ppos.pos[i]>b.pos[i]) then
-          --  biasb[i] = weightb
-        --else
-          --  biasb[i] = 0
-        --end
-    --end
-    --local currentVelocity = GetBodyVelocity(LLARM)
-    if alive then
-    	if agro then
-    local ppos = enemy
-    local bmi, bma = GetBodyBounds(LLARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(LLARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(LLARM, vel)
-local bmi, bma = GetBodyBounds(RRARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(RRARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(RRARM, vel)
-end
-end
-end
-end
-  --akmpos.rot = Rot
-  --SetBodyTransform(akm, akmpos)
-
---HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
-	if bleed then
-	if IsBodyBroken(Head) then
-
-		for i=1, 9 do
-		 	 thingz = FindJoints("eye")
-		 	 for i=1, #thingz do
-		 	 	thinz = thingz[i]
-		 	 	Delete(thinz)
-		 	 end
-		 end
-
-		for i=1,Bleed/2 do
-		smoke()
-	end
-end
-end
-
-if bleed then
-	
-		if HeadBloodCapacity < MaxBloodCapacity then
-		Bleed = Bleed * 6 
-		for i=1,Bleed/6 do
-		smoke()
-	end
-	end
-
-HeadBloodLevel = HeadBloodLevel - Bleed/2
-end
-
-	if HeadBloodLevel <= 0 then
-		bleed = false
-		HeadBloodLevel = 0
-	end
-
-	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
-
-	if bleed1 then
-	if IsBodyBroken(Torso) then
-		for i=1,Bleed1/regularantibleed do
-		smoke1()
-	end
-end
-end
-
-if bleed1 then
-
-		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
-		Bleed1 = Bleed1 * 6 
-		 for i=1, 9 do
-		 	 things = FindBodies("gut", true)
-		 	 for i=1, #things do
-		 	 	thing = things[i]
-		 	 	SetBodyDynamic(thing, true)
-		 	 end
-		 end
-		for i=1,Bleed1/extremeantibleed do
-		smoke1()
-	end
-	end
-
-TorsoBloodLevel = TorsoBloodLevel - Bleed1
-end
-
-	if TorsoBloodLevel <= 0 then
-		bleed1 = false
-		TorsoBloodLevel = 0
-	end
-
--- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
-
-if bleed2 then
-
-	if LARMBloodCapacity < MaxBloodCapacity2/3 then
-		Bleed2 = Bleed2 * 6 
-		for i=1,Bleed2/extremeantibleed do
-		smoke2()
-	end
-	end
-
-	if IsBodyBroken(LARM) then
-		for i=1,Bleed2/limbantibleed do
-		smoke2()
-	end
-end
-end
-
-if bleed2 then
-LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
-end
-
-	if LARMBloodLevel <= 0 then
-		bleed2 = false
-		LARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-if bleed3 then
-
-	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
-		Bleed3 = Bleed3 * 6 
-		for i=1,Bleed3/extremeantibleed do
-		smoke3()
-	end
-	end
-
-	if IsBodyBroken(LLARM) then
-		for i=1,Bleed3/limbantibleed do
-		smoke3()
-	end
-end
-end
-
-if bleed3 then
-LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
-end
-
-	if LLARMBloodLevel <= 0 then
-		bleed3 = false
-		LLARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed4 then
-
-		if RARMBloodCapacity < MaxBloodCapacity4/3 then
-		Bleed4 = Bleed4 * 6 
-		for i=1,Bleed4/extremeantibleed do
-		smoke4()
-	end
-	end
-
-	if IsBodyBroken(RARM) then
-		for i=1,Bleed4/limbantibleed do
-		smoke4()
-	end
-end
-end
-
-if bleed4 then
-RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
-end
-
-	if RARMBloodLevel <= 0 then
-		bleed4 = false
-		RARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed5 then
-
-		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
-		Bleed5 = Bleed5 * 6 
-		for i=1,Bleed5/extremeantibleed do
-		smoke5()
-	end
-	end
-
-	if IsBodyBroken(RRARM) then
-		for i=1,Bleed5/limbantibleed do
-		smoke5()
-	end
-end
-end
-
-if bleed5 then
-RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
-end
-
-	if RRARMBloodLevel <= 0 then
-		bleed5 = false
-		RRARMBloodLevel = 0
-	end
-
-	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
-
-	if bleed6 then
-
-		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
-		Bleed6 = Bleed6 * 6 
-		for i=1,Bleed6/extremeantibleed do
-		smoke6()
-	end
-	end
-
-	if IsBodyBroken(LLEG) then
-		for i=1,Bleed6/limbantibleed do
-		smoke6()
-	end
-end
-end
-
-if bleed6 then
-LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
-end
-
-	if LLEGBloodLevel <= 0 then
-		bleed6 = false
-	LLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed7 then
-
-		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
-		Bleed7 = Bleed7 * 6 
-		for i=1,Bleed7/extremeantibleed do
-		smoke7()
-	end
-	end
-
-	if IsBodyBroken(LLLEG) then
-		for i=1,Bleed7/limbantibleed do
-		smoke7()
-	end
-end
-end
-
-if bleed7 then
-LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
-end
-
-	if LLLEGBloodLevel <= 0 then
-		bleed7 = false
-	LLLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed8 then
-
-		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
-		Bleed8 = Bleed8 * 6 
-		for i=1,Bleed8/extremeantibleed do
-		smoke8()
-	end
-	end
-
-	if IsBodyBroken(RLEG) then
-		for i=1,Bleed8/limbantibleed do
-		smoke8()
-	end
-end
-end
-
-if bleed8 then
-RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
-end
-
-	if RLEGBloodLevel <= 0 then
-		bleed8 = false
-	RLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed9 then
-
-		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
-		Bleed9 = Bleed9 * 6 
-		for i=1,Bleed9/extremeantibleed do
-		smoke9()
-	end
-	end
-
-	if IsBodyBroken(RRLEG) then
-		for i=1,Bleed9/limbantibleed do
-		smoke9()
-	end
-end
-end
-
-if bleed9 then
-RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
-end
-
-	if RRLEGBloodLevel <= 0 then
-		bleed9 = false
-	RRLEGBloodLevel = 0
-	end
-
-	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
-	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
-
-	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
-		upspeed[2] = TotalLegBloodValue/10000
-
-	currentvel = GetBodyVelocity(Head)
-	currentvel1 = GetBodyVelocity(LLLEG)
-	currentvel2 = GetBodyVelocity(RRLEG)
-
-	if IsBodyBroken(Head) then
-		alive = false
-	end
-
-	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
-		alive = false
-	end
-
-	if TotalBloodValue < MinBloodValue then
-		alive = false
-	end
-	if alive then
-	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
-	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
-	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
-end
-
-a = GetPlayerTransform()
-
-	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
-
-	if distToPlayer < 3 then
-		inrange = true
-	else
-		inrange = false
-	end
-
-
-end
-
-
+#version 2
 function smoke()
     --spawn sparks
     ParticleType("smoke")
@@ -860,138 +165,8 @@
     SpawnParticle(shootpos.pos, Vec(math.random(-5, 5), math.random(-5, 5), math.random(-5, 5)),0.3)
 end
 
-
-function draw()
-if drawtext then
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("Head Blood Level:  "..HeadBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 220)
-      UiFont("bold.ttf", 30)
-      UiText("Torso Blood Level:  "..TorsoBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 240)
-      UiFont("bold.ttf", 30)
-      UiText("upper left arm Blood Level:  "..LARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 260)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 280)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 300)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 320)
-      UiFont("bold.ttf", 30)
-      UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 340)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 360)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 380)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 400)
-      UiFont("bold.ttf", 30)
-      UiText("total Blood Level:  "..TotalBloodValue)
-    UiPop()
-end
-if inrange then
-	if enabled then
-
-			UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 300)
-      UiColor(0,0,1)
-      UiFont("bold.ttf", 30)
-      UiText("To disable viewable ragdoll stats, press H ")
-    UiPop()
-
-	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 350)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 30)
-      UiText("Total Blood Volume:  "..TotalBloodValue)
-    UiPop()
-
-    if alive then
-    	  UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 60)
-      UiText("ALIVE")
-    UiPop()
-    if TotalBloodValue < 15000 then
-    	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 450)
-      UiColor(1,1,0)
-      UiFont("bold.ttf", 50)
-      UiText("CRITICAL CONDITION")
-    UiPop()
-    end
-end
-if not alive then
-	  UiPush()
-	  UiColor(1,0,0)
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiFont("bold.ttf", 60)
-      UiText("DECEASED")
-    UiPop()
-end
-end
-end
-end
-
 function canSeePlayer()
-    local camTrans = GetPlayerCameraTransform()
+    local camTrans = GetPlayerCameraTransform(playerId)
 	local playerPos = camTrans.pos
 
 	--Direction to player
@@ -999,7 +174,7 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	return not QueryRaycast(shootPos, dir, dist, 0, true)
 end
 
@@ -1013,6 +188,745 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	return not QueryRaycast(shootPos, dir, dist, 0, true)
-end+end
+
+function server.init()
+    Head = FindBody("Head")
+    HeadBloodCapacity = GetBodyMass(Head)
+    HeadBloodLevel = HeadBloodCapacity * 20
+    StartingBleed = HeadBloodCapacity
+    MaxBloodCapacity = GetBodyMass(Head)
+    bleed = true
+    Torso = FindBody("Torso")
+    TorsoBloodCapacity = GetBodyMass(Torso)
+    TorsoBloodLevel = TorsoBloodCapacity * 20
+    StartingBleed1 = TorsoBloodCapacity
+    MaxBloodCapacity1 = GetBodyMass(Torso)
+    bleed1 = true
+    LARM = FindBody("LARM")
+    LARMBloodCapacity = GetBodyMass(LARM)
+    LARMBloodLevel = LARMBloodCapacity * 20
+    StartingBleed2 = LARMBloodCapacity
+    MaxBloodCapacity2 = GetBodyMass(LARM)
+    bleed2 = true
+    LLARM = FindBody("LLARM")
+    LLARMBloodCapacity = GetBodyMass(LLARM)
+    LLARMBloodLevel = LLARMBloodCapacity * 20
+    StartingBleed3 = LLARMBloodCapacity
+    MaxBloodCapacity3 = GetBodyMass(LLARM)
+    bleed3 = true
+    RARM = FindBody("RARM")
+    RARMBloodCapacity = GetBodyMass(RARM)
+    RARMBloodLevel = RARMBloodCapacity * 20
+    StartingBleed4 = RARMBloodCapacity
+    MaxBloodCapacity4 = GetBodyMass(RARM)
+    bleed4 = true
+    RRARM = FindBody("RRARM")
+    RRARMBloodCapacity = GetBodyMass(RRARM)
+    RRARMBloodLevel = RRARMBloodCapacity * 20
+    StartingBleed5 = RRARMBloodCapacity
+    MaxBloodCapacity5 = GetBodyMass(RRARM)
+    bleed5 = true
+    LLEG = FindBody("LLEG")
+    LLEGBloodCapacity = GetBodyMass(LLEG)
+    LLEGBloodLevel = LLEGBloodCapacity * 20
+    StartingBleed6 = LLEGBloodCapacity
+    MaxBloodCapacity6 = GetBodyMass(LLEG)
+    bleed6 = true
+    LLLEG = FindBody("LLLEG")
+    LLLEGBloodCapacity = GetBodyMass(LLLEG)
+    LLLEGBloodLevel = LLLEGBloodCapacity * 20
+    StartingBleed7 = LLLEGBloodCapacity
+    MaxBloodCapacity7 = GetBodyMass(LLLEG)
+    bleed7 = true
+    RLEG = FindBody("RLEG")
+    RLEGBloodCapacity = GetBodyMass(RLEG)
+    RLEGBloodLevel = RLEGBloodCapacity * 20
+    StartingBleed8 = RLEGBloodCapacity
+    MaxBloodCapacity8 = GetBodyMass(RLEG)
+    bleed8 = true
+    RRLEG = FindBody("RRLEG")
+    RRLEGBloodCapacity = GetBodyMass(RRLEG)
+    RRLEGBloodLevel = RRLEGBloodCapacity * 20
+    StartingBleed9 = RRLEGBloodCapacity
+    MaxBloodCapacity9 = GetBodyMass(RRLEG)
+    bleed9 = true
+    antibleed = 15 -- only affects smoke speed
+    extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
+    regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
+    limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
+    MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
+    LimbBleedSpeed = 0.1
+    bloodgrav = -20
+    blooddrag = 0
+    startupspeed = Vec(0,0.7,0)
+    upspeed = Vec(0,2,0)
+    downspeed = Vec(0,-0.7,0)
+    alive = true
+    akm = FindBody("AKM")
+    weight = 20
+    bias = Vec(0,0,0)
+    biasb = Vec(0,0,0)
+    weightb = -0.6
+    agrotimer = 0
+    forget = 10
+    KillTimer = 0
+    Eliminate = 1
+    shootim = 0
+    shots = 0
+    reload = 0
+    magsize = 95
+    firerate = 1.5
+    recoil = 2
+    flare = FindLight("flare")
+    flaretim = false
+    flaretimer = 0
+    SetLightEnabled(flare, false)
+    disarmed = false
+    spetsnaz = FindShape("spetsnaz",true)
+    enemyspotted = false
+    	switched = true
+    	enabled = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        end
+        	if IsShapeBroken(spetsnaz) then
+        		RemoveTag(spetsnaz,"spetsnaz")
+        		agro = false
+        		agrotimer = 0
+        		spetsnaz = FindShape("spetsnaz",true)
+        		enemyspotted = false
+        		shoot = false
+        	end
+        	if PlayerHP == 0 then
+        		shoot = false
+        		agro = false
+        		agrotimer = 0
+        		enemyspotted = false
+        	end
+        	gunTrans = GetBodyTransform(Head)
+        	gunPos = gunTrans.pos
+        	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
+        	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
+        	drawtext = false
+        	HeadBloodCapacity = GetBodyMass(Head)
+        	Bleed = StartingBleed - HeadBloodCapacity
+        	HeadPos = GetBodyTransform(Head)
+        	TorsoBloodCapacity = GetBodyMass(Torso)
+        	Bleed1 = StartingBleed1 - TorsoBloodCapacity
+        	TorsoPos = GetBodyTransform(Torso)
+        	LARMBloodCapacity = GetBodyMass(LARM)
+        	Bleed2 = StartingBleed2 - LARMBloodCapacity
+        	LARMPos = GetBodyTransform(LARM)
+        	LLARMBloodCapacity = GetBodyMass(LLARM)
+        	Bleed3 = StartingBleed3 - LLARMBloodCapacity
+        	LLARMPos = GetBodyTransform(LLARM)
+        	RARMBloodCapacity = GetBodyMass(RARM)
+        	Bleed4 = StartingBleed4 - RARMBloodCapacity
+        	RARMPos = GetBodyTransform(RARM)
+        	RRARMBloodCapacity = GetBodyMass(RRARM)
+        	Bleed5 = StartingBleed5 - RRARMBloodCapacity
+        	RRARMPos = GetBodyTransform(RRARM)
+        	LLEGBloodCapacity = GetBodyMass(LLEG)
+        	Bleed6 = StartingBleed6 - LLEGBloodCapacity
+        	LLEGPos = GetBodyTransform(LLEG)
+        	LLLEGBloodCapacity = GetBodyMass(LLLEG)
+        	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
+        	LLLEGPos = GetBodyTransform(LLLEG)
+        	RLEGBloodCapacity = GetBodyMass(RLEG)
+        	Bleed8 = StartingBleed8 - RLEGBloodCapacity
+        	RLEGPos = GetBodyTransform(RLEG)
+        	RRLEGBloodCapacity = GetBodyMass(RRLEG)
+        	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
+        	RRLEGPos = GetBodyTransform(RRLEG)
+        	--AGRESSIVE BEHAVIOR
+        	if IsBodyBroken(LLARM) then
+        		disarmed = true
+        	end
+        	if canSeeSpetsnaz() then
+        			agro = true
+        		agrotimer = 0
+        		KillTimer = KillTimer + dt
+        		enemyspotted = true
+        		shoot = true
+
+        	end
+        	if canSeePlayer() then
+        		agro = true
+        		agrotimer = 0
+        		KillTimer = KillTimer + dt
+        		enemyspotted = true
+        		shoot = true
+        		end
+        		if agro then
+        			agrotimer = agrotimer + dt
+        		if agrotimer > forget then
+        		agro = false
+        		agrotimer = 0
+        		KillTimer = 0
+        	end
+        end
+        	--RELOAD
+        	if shots > magsize then
+        		reloading = true
+        		if alive then
+        		reload = reload + dt
+        		if reload > 4 then
+        			reloading = false
+        			shots = 0
+        			reload = 0
+        		end
+        	end
+        	end
+        	--ELIMINATE TARGET 
+        	local barrel = FindShape("barrel")
+        	local guntrans = GetShapeWorldTransform(barrel)
+        	local terrorist = FindShape("terrorist")
+        	terrorpos = GetShapeWorldTransform(terrorist)
+        	--DebugPrint("guny:  "..guntrans.pos[2])
+        	--DebugPrint("body:  "..terrorpos.pos[2])
+        	if guntrans.pos[2] < terrorpos.pos[2] then
+        		shoot = false
+        	end
+            local gunpos = guntrans.pos
+        	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
+            local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
+            if flaretim then
+            	flaretimer = flaretimer + dt
+            	if flaretimer > 0.1 then
+            		SetLightEnabled(flare, false)
+            		flaretimer = 0
+            	end
+            end
+        	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
+        	if enemyspotted then
+        	if not disarmed then
+        	if alive then
+        		if agro then
+        	local ppos = GetPlayerCameraTransform(playerId)
+        	ppos.pos[2] = ppos.pos[2] - 0.5
+        	spetsnazpos = GetShapeWorldTransform(spetsnaz)
+        	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
+        	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
+
+        	if distToPlayeraim > distToSpetsaim and canSeeSpetsnaz() then
+        	enemy = spetsnazpos.pos
+        else if distToPlayeraim > distToSpetsaim and not canSeeSpetsnaz() then
+        	enemy = ppos.pos
+        end
+        end
+        	if distToPlayeraim < distToSpetsaim and canSeePlayer() then
+        	enemy = ppos.pos
+        else if distToPlayeraim < distToSpetsaim and not canSeePlayer() then
+        	enemy = spetsnazpos.pos
+        end
+        	end
+
+        	local akmpos = GetBodyTransform(akm)
+
+        	local aimangle = QuatLookAt(akmpos.pos, enemy)
+
+        	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
+        	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
+
+        --yaw
+         gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
+          --pitch
+         gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
+          --roll
+         gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
+         if agro then
+
+         local bias = QuatEuler(gunyaw, gunpitch, gunroll)
+          SetBodyTransform(akm, Transform(akmpos.pos, bias))
+        end
+        end
+        end
+        --b = GetBodyTransform(LLARM)
+          --for i=1,3 do
+                --if(ppos.pos[i]<b.pos[i]) then
+                     --biasb[i] = -weightb
+                --elseif(ppos.pos[i]>b.pos[i]) then
+                  --  biasb[i] = weightb
+                --else
+                  --  biasb[i] = 0
+                --end
+            --end
+            --local currentVelocity = GetBodyVelocity(LLARM)
+            if alive then
+            	if agro then
+            local ppos = enemy
+            local bmi, bma = GetBodyBounds(LLARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(LLARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(LLARM, vel)
+        local bmi, bma = GetBodyBounds(RRARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(RRARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(RRARM, vel)
+        end
+        end
+        end
+        end
+          --akmpos.rot = Rot
+          --SetBodyTransform(akm, akmpos)
+        --HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
+        	if bleed then
+        	if IsBodyBroken(Head) then
+
+        		for i=1, 9 do
+        		 	 thingz = FindJoints("eye")
+        		 	 for i=1, #thingz do
+        		 	 	thinz = thingz[i]
+        		 	 	Delete(thinz)
+        		 	 end
+        		 end
+
+        		for i=1,Bleed/2 do
+        		smoke()
+        	end
+        end
+        end
+        if bleed then
+
+        		if HeadBloodCapacity < MaxBloodCapacity then
+        		Bleed = Bleed * 6 
+        		for i=1,Bleed/6 do
+        		smoke()
+        	end
+        	end
+
+        HeadBloodLevel = HeadBloodLevel - Bleed/2
+        end
+        	if HeadBloodLevel <= 0 then
+        		bleed = false
+        		HeadBloodLevel = 0
+        	end
+        	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
+        	if bleed1 then
+        	if IsBodyBroken(Torso) then
+        		for i=1,Bleed1/regularantibleed do
+        		smoke1()
+        	end
+        end
+        end
+        if bleed1 then
+
+        		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
+        		Bleed1 = Bleed1 * 6 
+        		 for i=1, 9 do
+        		 	 things = FindBodies("gut", true)
+        		 	 for i=1, #things do
+        		 	 	thing = things[i]
+        		 	 	SetBodyDynamic(thing, true)
+        		 	 end
+        		 end
+        		for i=1,Bleed1/extremeantibleed do
+        		smoke1()
+        	end
+        	end
+
+        TorsoBloodLevel = TorsoBloodLevel - Bleed1
+        end
+        	if TorsoBloodLevel <= 0 then
+        		bleed1 = false
+        		TorsoBloodLevel = 0
+        	end
+        -- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
+        if bleed2 then
+
+        	if LARMBloodCapacity < MaxBloodCapacity2/3 then
+        		Bleed2 = Bleed2 * 6 
+        		for i=1,Bleed2/extremeantibleed do
+        		smoke2()
+        	end
+        	end
+
+        	if IsBodyBroken(LARM) then
+        		for i=1,Bleed2/limbantibleed do
+        		smoke2()
+        	end
+        end
+        end
+        if bleed2 then
+        LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
+        end
+        	if LARMBloodLevel <= 0 then
+        		bleed2 = false
+        		LARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        if bleed3 then
+
+        	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
+        		Bleed3 = Bleed3 * 6 
+        		for i=1,Bleed3/extremeantibleed do
+        		smoke3()
+        	end
+        	end
+
+        	if IsBodyBroken(LLARM) then
+        		for i=1,Bleed3/limbantibleed do
+        		smoke3()
+        	end
+        end
+        end
+        if bleed3 then
+        LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
+        end
+        	if LLARMBloodLevel <= 0 then
+        		bleed3 = false
+        		LLARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed4 then
+
+        		if RARMBloodCapacity < MaxBloodCapacity4/3 then
+        		Bleed4 = Bleed4 * 6 
+        		for i=1,Bleed4/extremeantibleed do
+        		smoke4()
+        	end
+        	end
+
+        	if IsBodyBroken(RARM) then
+        		for i=1,Bleed4/limbantibleed do
+        		smoke4()
+        	end
+        end
+        end
+        if bleed4 then
+        RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
+        end
+        	if RARMBloodLevel <= 0 then
+        		bleed4 = false
+        		RARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed5 then
+
+        		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
+        		Bleed5 = Bleed5 * 6 
+        		for i=1,Bleed5/extremeantibleed do
+        		smoke5()
+        	end
+        	end
+
+        	if IsBodyBroken(RRARM) then
+        		for i=1,Bleed5/limbantibleed do
+        		smoke5()
+        	end
+        end
+        end
+        if bleed5 then
+        RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
+        end
+        	if RRARMBloodLevel <= 0 then
+        		bleed5 = false
+        		RRARMBloodLevel = 0
+        	end
+        	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
+        	if bleed6 then
+
+        		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
+        		Bleed6 = Bleed6 * 6 
+        		for i=1,Bleed6/extremeantibleed do
+        		smoke6()
+        	end
+        	end
+
+        	if IsBodyBroken(LLEG) then
+        		for i=1,Bleed6/limbantibleed do
+        		smoke6()
+        	end
+        end
+        end
+        if bleed6 then
+        LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
+        end
+        	if LLEGBloodLevel <= 0 then
+        		bleed6 = false
+        	LLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed7 then
+
+        		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
+        		Bleed7 = Bleed7 * 6 
+        		for i=1,Bleed7/extremeantibleed do
+        		smoke7()
+        	end
+        	end
+
+        	if IsBodyBroken(LLLEG) then
+        		for i=1,Bleed7/limbantibleed do
+        		smoke7()
+        	end
+        end
+        end
+        if bleed7 then
+        LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
+        end
+        	if LLLEGBloodLevel <= 0 then
+        		bleed7 = false
+        	LLLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed8 then
+
+        		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
+        		Bleed8 = Bleed8 * 6 
+        		for i=1,Bleed8/extremeantibleed do
+        		smoke8()
+        	end
+        	end
+
+        	if IsBodyBroken(RLEG) then
+        		for i=1,Bleed8/limbantibleed do
+        		smoke8()
+        	end
+        end
+        end
+        if bleed8 then
+        RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
+        end
+        	if RLEGBloodLevel <= 0 then
+        		bleed8 = false
+        	RLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed9 then
+
+        		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
+        		Bleed9 = Bleed9 * 6 
+        		for i=1,Bleed9/extremeantibleed do
+        		smoke9()
+        	end
+        	end
+
+        	if IsBodyBroken(RRLEG) then
+        		for i=1,Bleed9/limbantibleed do
+        		smoke9()
+        	end
+        end
+        end
+        if bleed9 then
+        RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
+        end
+        	if RRLEGBloodLevel <= 0 then
+        		bleed9 = false
+        	RRLEGBloodLevel = 0
+        	end
+        	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
+        	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
+        	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
+        		upspeed[2] = TotalLegBloodValue/10000
+        	currentvel = GetBodyVelocity(Head)
+        	currentvel1 = GetBodyVelocity(LLLEG)
+        	currentvel2 = GetBodyVelocity(RRLEG)
+        	if IsBodyBroken(Head) then
+        		alive = false
+        	end
+        	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
+        		alive = false
+        	end
+        	if TotalBloodValue < MinBloodValue then
+        		alive = false
+        	end
+        	if alive then
+        	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
+        	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
+        	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
+        end
+        a = GetPlayerTransform(playerId)
+        	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
+        	if distToPlayer < 3 then
+        		inrange = true
+        	else
+        		inrange = false
+        	end
+    end
+end
+
+function client.init()
+    GunShot = LoadSound("MOD/gorescript/akm.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    	if InputPressed("H") then
+    		if switched then
+    			enabled = false
+    			switched = false
+    		else if not switched then
+    			enabled = true
+    		switched = true
+    		end
+    	end
+        if shoot then
+    	if KillTimer > Eliminate then
+    		if not disarmed then
+    		if not reloading then
+    		shootim = shootim + dt * firerate
+    		if shootim > 0.2 then
+    		Shoot(shootpos, direction)
+    		PlaySound(GunShot, shootpos,10)
+    		SetLightEnabled(flare, true)
+    		flaretim = true
+    		for i=1,33 do
+    		GunSmoke()
+    	end
+    		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
+    		shootim = 0
+    		shots = shots + 1
+    	end
+    end
+    	end
+    end
+    end
+end
+
+function client.draw()
+    if drawtext then
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("Head Blood Level:  "..HeadBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 220)
+          UiFont("bold.ttf", 30)
+          UiText("Torso Blood Level:  "..TorsoBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 240)
+          UiFont("bold.ttf", 30)
+          UiText("upper left arm Blood Level:  "..LARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 260)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 280)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 300)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 320)
+          UiFont("bold.ttf", 30)
+          UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 340)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 360)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 380)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 400)
+          UiFont("bold.ttf", 30)
+          UiText("total Blood Level:  "..TotalBloodValue)
+        UiPop()
+    end
+    if inrange then
+    	if enabled then
+
+    			UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 300)
+          UiColor(0,0,1)
+          UiFont("bold.ttf", 30)
+          UiText("To disable viewable ragdoll stats, press H ")
+        UiPop()
+
+    	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 350)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 30)
+          UiText("Total Blood Volume:  "..TotalBloodValue)
+        UiPop()
+
+        if alive then
+        	  UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 60)
+          UiText("ALIVE")
+        UiPop()
+        if TotalBloodValue < 15000 then
+        	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 450)
+          UiColor(1,1,0)
+          UiFont("bold.ttf", 50)
+          UiText("CRITICAL CONDITION")
+        UiPop()
+        end
+    end
+    if not alive then
+    	  UiPush()
+    	  UiColor(1,0,0)
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiFont("bold.ttf", 60)
+          UiText("DECEASED")
+        UiPop()
+    end
+    end
+    end
+end
+

```

---

# Migration Report: gorescript\goremi7.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/gorescript\goremi7.lua
+++ patched/gorescript\goremi7.lua
@@ -1,672 +1,4 @@
-function init()
-	Head = FindBody("Head")
-	HeadBloodCapacity = GetBodyMass(Head)
-	HeadBloodLevel = HeadBloodCapacity * 20
-	StartingBleed = HeadBloodCapacity
-	MaxBloodCapacity = GetBodyMass(Head)
-	bleed = true
-
-	Torso = FindBody("Torso")
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	TorsoBloodLevel = TorsoBloodCapacity * 20
-	StartingBleed1 = TorsoBloodCapacity
-	MaxBloodCapacity1 = GetBodyMass(Torso)
-	bleed1 = true
-
-	LARM = FindBody("LARM")
-	LARMBloodCapacity = GetBodyMass(LARM)
-	LARMBloodLevel = LARMBloodCapacity * 20
-	StartingBleed2 = LARMBloodCapacity
-	MaxBloodCapacity2 = GetBodyMass(LARM)
-
-	bleed2 = true
-
-	LLARM = FindBody("LLARM")
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	LLARMBloodLevel = LLARMBloodCapacity * 20
-	StartingBleed3 = LLARMBloodCapacity
-	MaxBloodCapacity3 = GetBodyMass(LLARM)
-	bleed3 = true
-
-	RARM = FindBody("RARM")
-	RARMBloodCapacity = GetBodyMass(RARM)
-	RARMBloodLevel = RARMBloodCapacity * 20
-	StartingBleed4 = RARMBloodCapacity
-	MaxBloodCapacity4 = GetBodyMass(RARM)
-	bleed4 = true
-
-	RRARM = FindBody("RRARM")
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	RRARMBloodLevel = RRARMBloodCapacity * 20
-	StartingBleed5 = RRARMBloodCapacity
-	MaxBloodCapacity5 = GetBodyMass(RRARM)
-	bleed5 = true
-
-	LLEG = FindBody("LLEG")
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	LLEGBloodLevel = LLEGBloodCapacity * 20
-	StartingBleed6 = LLEGBloodCapacity
-	MaxBloodCapacity6 = GetBodyMass(LLEG)
-	bleed6 = true
-
-	LLLEG = FindBody("LLLEG")
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	LLLEGBloodLevel = LLLEGBloodCapacity * 20
-	StartingBleed7 = LLLEGBloodCapacity
-	MaxBloodCapacity7 = GetBodyMass(LLLEG)
-	bleed7 = true
-
-	RLEG = FindBody("RLEG")
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	RLEGBloodLevel = RLEGBloodCapacity * 20
-	StartingBleed8 = RLEGBloodCapacity
-	MaxBloodCapacity8 = GetBodyMass(RLEG)
-	bleed8 = true
-
-	RRLEG = FindBody("RRLEG")
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	RRLEGBloodLevel = RRLEGBloodCapacity * 20
-	StartingBleed9 = RRLEGBloodCapacity
-	MaxBloodCapacity9 = GetBodyMass(RRLEG)
-	bleed9 = true
-
-	antibleed = 15 -- only affects smoke speed
-	extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
-	regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
-	limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
-	MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
-
-	LimbBleedSpeed = 0.1
-
-	bloodgrav = -20
-	blooddrag = 0
-	startupspeed = Vec(0,0.7,0)
-	upspeed = Vec(0,0.5,0)
-	downspeed = Vec(0,-0.9,0)
-	alive = true
-
-	akm = FindBody("AKM")
-	weight = 2
-	bias = Vec(0,0,0)
-	biasb = Vec(0,0,0)
-	weightb = -0.4
-	agrotimer = 0
-	forget = 10
-	KillTimer = 0
-	Eliminate = 0
-	shootim = 0
-	shots = 0
-	reload = 0
-	recoil = 20
-	firerate = 1.3
-
-	flare = FindLight("flare")
-	flaretim = false
-	flaretimer = 0
-	SetLightEnabled(flare, false)
-	disarmed = false
-	spetsnaz = FindShape("terrorist",true)
-	GunShot = LoadSound("MOD/gorescript/mp7.ogg")
-	enemyspotted = false
-		switched = true
-		enabled = true
-end
-
-
-function tick(dt)
-
-	if InputPressed("H") then
-		if switched then
-			enabled = false
-			switched = false
-		else if not switched then
-			enabled = true
-		switched = true
-		end
-	end
-end
-
-	if IsShapeBroken(spetsnaz) then
-		RemoveTag(spetsnaz,"terrorist")
-		agro = false
-		agrotimer = 0
-		spetsnaz = FindShape("terrorist",true)
-		enemyspotted = false
-		shoot = false
-	end
-
-	if PlayerHP == 0 then
-		shoot = false
-		agro = false
-		agrotimer = 0
-		enemyspotted = false
-	end
-	gunTrans = GetBodyTransform(Head)
-	gunPos = gunTrans.pos
-	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
-	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
-
-	drawtext = false
-
-	HeadBloodCapacity = GetBodyMass(Head)
-	Bleed = StartingBleed - HeadBloodCapacity
-	HeadPos = GetBodyTransform(Head)
-
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	Bleed1 = StartingBleed1 - TorsoBloodCapacity
-	TorsoPos = GetBodyTransform(Torso)
-
-	LARMBloodCapacity = GetBodyMass(LARM)
-	Bleed2 = StartingBleed2 - LARMBloodCapacity
-	LARMPos = GetBodyTransform(LARM)
-
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	Bleed3 = StartingBleed3 - LLARMBloodCapacity
-	LLARMPos = GetBodyTransform(LLARM)
-
-	RARMBloodCapacity = GetBodyMass(RARM)
-	Bleed4 = StartingBleed4 - RARMBloodCapacity
-	RARMPos = GetBodyTransform(RARM)
-
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	Bleed5 = StartingBleed5 - RRARMBloodCapacity
-	RRARMPos = GetBodyTransform(RRARM)
-
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	Bleed6 = StartingBleed6 - LLEGBloodCapacity
-	LLEGPos = GetBodyTransform(LLEG)
-
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
-	LLLEGPos = GetBodyTransform(LLLEG)
-
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	Bleed8 = StartingBleed8 - RLEGBloodCapacity
-	RLEGPos = GetBodyTransform(RLEG)
-
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
-	RRLEGPos = GetBodyTransform(RRLEG)
-
-	--AGRESSIVE BEHAVIOR
-
-	if IsBodyBroken(LLARM) then
-		disarmed = true
-	end
-
-	if canSeeSpetsnaz() then
-			agro = true
-		agrotimer = 0
-		KillTimer = KillTimer + dt
-		enemyspotted = true
-		shoot = true
-	end
-
-	--RELOAD
-	if shots > 29 then
-		reloading = true
-		if alive then
-		reload = reload + dt
-		if reload > 4 then
-			reloading = false
-			shots = 0
-			reload = 0
-		end
-	end
-	end
-
-
-	--ELIMINATE TARGET 
-	local barrel = FindShape("barrel")
-	local guntrans = GetShapeWorldTransform(barrel)
-	local terrorist = FindShape("spetsnaz")
-	terrorpos = GetShapeWorldTransform(terrorist)
-	--DebugPrint("guny:  "..guntrans.pos[2])
-	--DebugPrint("body:  "..terrorpos.pos[2])
-	if guntrans.pos[2] < terrorpos.pos[2] then
-		shoot = false
-	end
-    local gunpos = guntrans.pos
-	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
-    local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
-
-    if flaretim then
-    	flaretimer = flaretimer + dt
-    	if flaretimer > 0.05 then
-    		SetLightEnabled(flare, false)
-    		flaretimer = 0
-    	end
-    end
-    if shoot then
-	if KillTimer > Eliminate then
-		if not disarmed then
-		if not reloading then
-		shootim = shootim + dt * firerate
-		if shootim > 0.1 then
-		Shoot(shootpos, direction)
-		PlaySound(GunShot, shootpos,10)
-		SetLightEnabled(flare, true)
-		flaretim = true
-		for i=1,33 do
-		GunSmoke()
-	end
-		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
-		shootim = 0
-		shots = shots + 1
-	end
-end
-	end
-end
-end
-
-	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
-	if enemyspotted then
-	if not disarmed then
-	if alive then
-		if agro then
-	local ppos = GetPlayerCameraTransform()
-	ppos.pos[2] = ppos.pos[2] - 0.5
-	spetsnazpos = GetShapeWorldTransform(spetsnaz)
-	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
-	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
-
-
-
-	if canSeeSpetsnaz() then
-		enemy = spetsnazpos.pos
-end
-
-
-
-	local akmpos = GetBodyTransform(akm)
-
-	local aimangle = QuatLookAt(akmpos.pos, enemy)
-
-	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
-	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
-
-
---yaw
- gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
-  --pitch
- gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
-  --roll
- gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
- if agro then
-
- local bias = QuatEuler(gunyaw, gunpitch, gunroll)
-  SetBodyTransform(akm, Transform(akmpos.pos, bias))
-end
-end
-end
-
---b = GetBodyTransform(LLARM)
-  --for i=1,3 do
-        --if(ppos.pos[i]<b.pos[i]) then
-             --biasb[i] = -weightb
-        --elseif(ppos.pos[i]>b.pos[i]) then
-          --  biasb[i] = weightb
-        --else
-          --  biasb[i] = 0
-        --end
-    --end
-    --local currentVelocity = GetBodyVelocity(LLARM)
-    if alive then
-    	if agro then
-    local ppos = enemy
-    local bmi, bma = GetBodyBounds(LLARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(LLARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(LLARM, vel)
-local bmi, bma = GetBodyBounds(RRARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(RRARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(RRARM, vel)
-end
-end
-end
-end
-  --akmpos.rot = Rot
-  --SetBodyTransform(akm, akmpos)
-
---HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
-	if bleed then
-	if IsBodyBroken(Head) then
-
-		for i=1, 9 do
-		 	 thingz = FindJoints("eye")
-		 	 for i=1, #thingz do
-		 	 	thinz = thingz[i]
-		 	 	Delete(thinz)
-		 	 end
-		 end
-
-		for i=1,Bleed/2 do
-		smoke()
-	end
-end
-end
-
-if bleed then
-	
-		if HeadBloodCapacity < MaxBloodCapacity then
-		Bleed = Bleed * 6 
-		for i=1,Bleed/6 do
-		smoke()
-	end
-	end
-
-HeadBloodLevel = HeadBloodLevel - Bleed/2
-end
-
-	if HeadBloodLevel <= 0 then
-		bleed = false
-		HeadBloodLevel = 0
-	end
-
-	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
-
-	if bleed1 then
-	if IsBodyBroken(Torso) then
-		for i=1,Bleed1/regularantibleed do
-		smoke1()
-	end
-end
-end
-
-if bleed1 then
-
-		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
-		Bleed1 = Bleed1 * 6 
-		 for i=1, 9 do
-		 	 things = FindBodies("gut", true)
-		 	 for i=1, #things do
-		 	 	thing = things[i]
-		 	 	SetBodyDynamic(thing, true)
-		 	 end
-		 end
-		for i=1,Bleed1/extremeantibleed do
-		smoke1()
-	end
-	end
-
-TorsoBloodLevel = TorsoBloodLevel - Bleed1
-end
-
-	if TorsoBloodLevel <= 0 then
-		bleed1 = false
-		TorsoBloodLevel = 0
-	end
-
--- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
-
-if bleed2 then
-
-	if LARMBloodCapacity < MaxBloodCapacity2/3 then
-		Bleed2 = Bleed2 * 6 
-		for i=1,Bleed2/extremeantibleed do
-		smoke2()
-	end
-	end
-
-	if IsBodyBroken(LARM) then
-		for i=1,Bleed2/limbantibleed do
-		smoke2()
-	end
-end
-end
-
-if bleed2 then
-LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
-end
-
-	if LARMBloodLevel <= 0 then
-		bleed2 = false
-		LARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-if bleed3 then
-
-	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
-		Bleed3 = Bleed3 * 6 
-		for i=1,Bleed3/extremeantibleed do
-		smoke3()
-	end
-	end
-
-	if IsBodyBroken(LLARM) then
-		for i=1,Bleed3/limbantibleed do
-		smoke3()
-	end
-end
-end
-
-if bleed3 then
-LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
-end
-
-	if LLARMBloodLevel <= 0 then
-		bleed3 = false
-		LLARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed4 then
-
-		if RARMBloodCapacity < MaxBloodCapacity4/3 then
-		Bleed4 = Bleed4 * 6 
-		for i=1,Bleed4/extremeantibleed do
-		smoke4()
-	end
-	end
-
-	if IsBodyBroken(RARM) then
-		for i=1,Bleed4/limbantibleed do
-		smoke4()
-	end
-end
-end
-
-if bleed4 then
-RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
-end
-
-	if RARMBloodLevel <= 0 then
-		bleed4 = false
-		RARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed5 then
-
-		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
-		Bleed5 = Bleed5 * 6 
-		for i=1,Bleed5/extremeantibleed do
-		smoke5()
-	end
-	end
-
-	if IsBodyBroken(RRARM) then
-		for i=1,Bleed5/limbantibleed do
-		smoke5()
-	end
-end
-end
-
-if bleed5 then
-RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
-end
-
-	if RRARMBloodLevel <= 0 then
-		bleed5 = false
-		RRARMBloodLevel = 0
-	end
-
-	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
-
-	if bleed6 then
-
-		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
-		Bleed6 = Bleed6 * 6 
-		for i=1,Bleed6/extremeantibleed do
-		smoke6()
-	end
-	end
-
-	if IsBodyBroken(LLEG) then
-		for i=1,Bleed6/limbantibleed do
-		smoke6()
-	end
-end
-end
-
-if bleed6 then
-LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
-end
-
-	if LLEGBloodLevel <= 0 then
-		bleed6 = false
-	LLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed7 then
-
-		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
-		Bleed7 = Bleed7 * 6 
-		for i=1,Bleed7/extremeantibleed do
-		smoke7()
-	end
-	end
-
-	if IsBodyBroken(LLLEG) then
-		for i=1,Bleed7/limbantibleed do
-		smoke7()
-	end
-end
-end
-
-if bleed7 then
-LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
-end
-
-	if LLLEGBloodLevel <= 0 then
-		bleed7 = false
-	LLLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed8 then
-
-		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
-		Bleed8 = Bleed8 * 6 
-		for i=1,Bleed8/extremeantibleed do
-		smoke8()
-	end
-	end
-
-	if IsBodyBroken(RLEG) then
-		for i=1,Bleed8/limbantibleed do
-		smoke8()
-	end
-end
-end
-
-if bleed8 then
-RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
-end
-
-	if RLEGBloodLevel <= 0 then
-		bleed8 = false
-	RLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed9 then
-
-		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
-		Bleed9 = Bleed9 * 6 
-		for i=1,Bleed9/extremeantibleed do
-		smoke9()
-	end
-	end
-
-	if IsBodyBroken(RRLEG) then
-		for i=1,Bleed9/limbantibleed do
-		smoke9()
-	end
-end
-end
-
-if bleed9 then
-RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
-end
-
-	if RRLEGBloodLevel <= 0 then
-		bleed9 = false
-	RRLEGBloodLevel = 0
-	end
-
-	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
-	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
-
-	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
-		upspeed[2] = TotalLegBloodValue/10000
-
-	currentvel = GetBodyVelocity(Head)
-	currentvel1 = GetBodyVelocity(LLLEG)
-	currentvel2 = GetBodyVelocity(RRLEG)
-
-	if IsBodyBroken(Head) then
-		alive = false
-	end
-
-	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
-		alive = false
-	end
-
-	if TotalBloodValue < MinBloodValue then
-		alive = false
-	end
-	if alive then
-	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
-	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
-	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
-end
-
-a = GetPlayerTransform()
-
-	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
-
-	if distToPlayer < 3 then
-		inrange = true
-	else
-		inrange = false
-	end
-
-
-end
-
-
+#version 2
 function smoke()
     --spawn sparks
     ParticleType("smoke")
@@ -833,149 +165,6 @@
     SpawnParticle(shootpos.pos, Vec(math.random(-5, 5), math.random(-5, 5), math.random(-5, 5)),0.3)
 end
 
-
-function draw()
-if drawtext then
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("Head Blood Level:  "..HeadBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 220)
-      UiFont("bold.ttf", 30)
-      UiText("Torso Blood Level:  "..TorsoBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 240)
-      UiFont("bold.ttf", 30)
-      UiText("upper left arm Blood Level:  "..LARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 260)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 280)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 300)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 320)
-      UiFont("bold.ttf", 30)
-      UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 340)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 360)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 380)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 400)
-      UiFont("bold.ttf", 30)
-      UiText("total Blood Level:  "..TotalBloodValue)
-    UiPop()
-end
-if inrange then
-	if enabled then
-
-			UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 300)
-      UiColor(0,0,1)
-      UiFont("bold.ttf", 30)
-      UiText("To disable viewable ragdoll stats, press H ")
-    UiPop()
-
-	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 350)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 30)
-      UiText("Total Blood Volume:  "..TotalBloodValue)
-    UiPop()
-
-    if alive then
-    	  UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 60)
-      UiText("ALIVE")
-    UiPop()
-    if TotalBloodValue < 15000 then
-    	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 450)
-      UiColor(1,1,0)
-      UiFont("bold.ttf", 50)
-      UiText("CRITICAL CONDITION")
-    UiPop()
-    end
-end
-if not alive then
-	  UiPush()
-	  UiColor(1,0,0)
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiFont("bold.ttf", 60)
-      UiText("DECEASED")
-    UiPop()
-end
-end
-end
-end
-
---function canSeePlayer()
-    --local camTrans = GetPlayerCameraTransform()
-	--local playerPos = camTrans.pos
-
-	--Direction to player
-	--local dir = VecSub(playerPos, shootPos)
-	--local dist = VecLength(dir)
-	--dir = VecNormalize(dir)
-
-	--QueryRejectVehicle(GetPlayerVehicle())
-	--return not QueryRaycast(shootPos, dir, dist, 0, true)
---end
-
 function canSeeSpetsnaz()
     local camTrans = GetShapeWorldTransform(spetsnaz)
     camTrans.pos[2] = camTrans.pos[2]
@@ -986,6 +175,720 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	return not QueryRaycast(shootPos, dir, dist, 0, true)
-end+end
+
+function server.init()
+    Head = FindBody("Head")
+    HeadBloodCapacity = GetBodyMass(Head)
+    HeadBloodLevel = HeadBloodCapacity * 20
+    StartingBleed = HeadBloodCapacity
+    MaxBloodCapacity = GetBodyMass(Head)
+    bleed = true
+    Torso = FindBody("Torso")
+    TorsoBloodCapacity = GetBodyMass(Torso)
+    TorsoBloodLevel = TorsoBloodCapacity * 20
+    StartingBleed1 = TorsoBloodCapacity
+    MaxBloodCapacity1 = GetBodyMass(Torso)
+    bleed1 = true
+    LARM = FindBody("LARM")
+    LARMBloodCapacity = GetBodyMass(LARM)
+    LARMBloodLevel = LARMBloodCapacity * 20
+    StartingBleed2 = LARMBloodCapacity
+    MaxBloodCapacity2 = GetBodyMass(LARM)
+    bleed2 = true
+    LLARM = FindBody("LLARM")
+    LLARMBloodCapacity = GetBodyMass(LLARM)
+    LLARMBloodLevel = LLARMBloodCapacity * 20
+    StartingBleed3 = LLARMBloodCapacity
+    MaxBloodCapacity3 = GetBodyMass(LLARM)
+    bleed3 = true
+    RARM = FindBody("RARM")
+    RARMBloodCapacity = GetBodyMass(RARM)
+    RARMBloodLevel = RARMBloodCapacity * 20
+    StartingBleed4 = RARMBloodCapacity
+    MaxBloodCapacity4 = GetBodyMass(RARM)
+    bleed4 = true
+    RRARM = FindBody("RRARM")
+    RRARMBloodCapacity = GetBodyMass(RRARM)
+    RRARMBloodLevel = RRARMBloodCapacity * 20
+    StartingBleed5 = RRARMBloodCapacity
+    MaxBloodCapacity5 = GetBodyMass(RRARM)
+    bleed5 = true
+    LLEG = FindBody("LLEG")
+    LLEGBloodCapacity = GetBodyMass(LLEG)
+    LLEGBloodLevel = LLEGBloodCapacity * 20
+    StartingBleed6 = LLEGBloodCapacity
+    MaxBloodCapacity6 = GetBodyMass(LLEG)
+    bleed6 = true
+    LLLEG = FindBody("LLLEG")
+    LLLEGBloodCapacity = GetBodyMass(LLLEG)
+    LLLEGBloodLevel = LLLEGBloodCapacity * 20
+    StartingBleed7 = LLLEGBloodCapacity
+    MaxBloodCapacity7 = GetBodyMass(LLLEG)
+    bleed7 = true
+    RLEG = FindBody("RLEG")
+    RLEGBloodCapacity = GetBodyMass(RLEG)
+    RLEGBloodLevel = RLEGBloodCapacity * 20
+    StartingBleed8 = RLEGBloodCapacity
+    MaxBloodCapacity8 = GetBodyMass(RLEG)
+    bleed8 = true
+    RRLEG = FindBody("RRLEG")
+    RRLEGBloodCapacity = GetBodyMass(RRLEG)
+    RRLEGBloodLevel = RRLEGBloodCapacity * 20
+    StartingBleed9 = RRLEGBloodCapacity
+    MaxBloodCapacity9 = GetBodyMass(RRLEG)
+    bleed9 = true
+    antibleed = 15 -- only affects smoke speed
+    extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
+    regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
+    limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
+    MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
+    LimbBleedSpeed = 0.1
+    bloodgrav = -20
+    blooddrag = 0
+    startupspeed = Vec(0,0.7,0)
+    upspeed = Vec(0,0.5,0)
+    downspeed = Vec(0,-0.9,0)
+    alive = true
+    akm = FindBody("AKM")
+    weight = 2
+    bias = Vec(0,0,0)
+    biasb = Vec(0,0,0)
+    weightb = -0.4
+    agrotimer = 0
+    forget = 10
+    KillTimer = 0
+    Eliminate = 0
+    shootim = 0
+    shots = 0
+    reload = 0
+    recoil = 20
+    firerate = 1.3
+    flare = FindLight("flare")
+    flaretim = false
+    flaretimer = 0
+    SetLightEnabled(flare, false)
+    disarmed = false
+    spetsnaz = FindShape("terrorist",true)
+    enemyspotted = false
+    	switched = true
+    	enabled = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        end
+        	if IsShapeBroken(spetsnaz) then
+        		RemoveTag(spetsnaz,"terrorist")
+        		agro = false
+        		agrotimer = 0
+        		spetsnaz = FindShape("terrorist",true)
+        		enemyspotted = false
+        		shoot = false
+        	end
+        	if PlayerHP == 0 then
+        		shoot = false
+        		agro = false
+        		agrotimer = 0
+        		enemyspotted = false
+        	end
+        	gunTrans = GetBodyTransform(Head)
+        	gunPos = gunTrans.pos
+        	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
+        	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
+        	drawtext = false
+        	HeadBloodCapacity = GetBodyMass(Head)
+        	Bleed = StartingBleed - HeadBloodCapacity
+        	HeadPos = GetBodyTransform(Head)
+        	TorsoBloodCapacity = GetBodyMass(Torso)
+        	Bleed1 = StartingBleed1 - TorsoBloodCapacity
+        	TorsoPos = GetBodyTransform(Torso)
+        	LARMBloodCapacity = GetBodyMass(LARM)
+        	Bleed2 = StartingBleed2 - LARMBloodCapacity
+        	LARMPos = GetBodyTransform(LARM)
+        	LLARMBloodCapacity = GetBodyMass(LLARM)
+        	Bleed3 = StartingBleed3 - LLARMBloodCapacity
+        	LLARMPos = GetBodyTransform(LLARM)
+        	RARMBloodCapacity = GetBodyMass(RARM)
+        	Bleed4 = StartingBleed4 - RARMBloodCapacity
+        	RARMPos = GetBodyTransform(RARM)
+        	RRARMBloodCapacity = GetBodyMass(RRARM)
+        	Bleed5 = StartingBleed5 - RRARMBloodCapacity
+        	RRARMPos = GetBodyTransform(RRARM)
+        	LLEGBloodCapacity = GetBodyMass(LLEG)
+        	Bleed6 = StartingBleed6 - LLEGBloodCapacity
+        	LLEGPos = GetBodyTransform(LLEG)
+        	LLLEGBloodCapacity = GetBodyMass(LLLEG)
+        	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
+        	LLLEGPos = GetBodyTransform(LLLEG)
+        	RLEGBloodCapacity = GetBodyMass(RLEG)
+        	Bleed8 = StartingBleed8 - RLEGBloodCapacity
+        	RLEGPos = GetBodyTransform(RLEG)
+        	RRLEGBloodCapacity = GetBodyMass(RRLEG)
+        	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
+        	RRLEGPos = GetBodyTransform(RRLEG)
+        	--AGRESSIVE BEHAVIOR
+        	if IsBodyBroken(LLARM) then
+        		disarmed = true
+        	end
+        	if canSeeSpetsnaz() then
+        			agro = true
+        		agrotimer = 0
+        		KillTimer = KillTimer + dt
+        		enemyspotted = true
+        		shoot = true
+        	end
+        	--RELOAD
+        	if shots > 29 then
+        		reloading = true
+        		if alive then
+        		reload = reload + dt
+        		if reload > 4 then
+        			reloading = false
+        			shots = 0
+        			reload = 0
+        		end
+        	end
+        	end
+        	--ELIMINATE TARGET 
+        	local barrel = FindShape("barrel")
+        	local guntrans = GetShapeWorldTransform(barrel)
+        	local terrorist = FindShape("spetsnaz")
+        	terrorpos = GetShapeWorldTransform(terrorist)
+        	--DebugPrint("guny:  "..guntrans.pos[2])
+        	--DebugPrint("body:  "..terrorpos.pos[2])
+        	if guntrans.pos[2] < terrorpos.pos[2] then
+        		shoot = false
+        	end
+            local gunpos = guntrans.pos
+        	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
+            local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
+            if flaretim then
+            	flaretimer = flaretimer + dt
+            	if flaretimer > 0.05 then
+            		SetLightEnabled(flare, false)
+            		flaretimer = 0
+            	end
+            end
+        	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
+        	if enemyspotted then
+        	if not disarmed then
+        	if alive then
+        		if agro then
+        	local ppos = GetPlayerCameraTransform(playerId)
+        	ppos.pos[2] = ppos.pos[2] - 0.5
+        	spetsnazpos = GetShapeWorldTransform(spetsnaz)
+        	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
+        	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
+
+        	if canSeeSpetsnaz() then
+        		enemy = spetsnazpos.pos
+        end
+
+        	local akmpos = GetBodyTransform(akm)
+
+        	local aimangle = QuatLookAt(akmpos.pos, enemy)
+
+        	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
+        	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
+
+        --yaw
+         gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
+          --pitch
+         gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
+          --roll
+         gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
+         if agro then
+
+         local bias = QuatEuler(gunyaw, gunpitch, gunroll)
+          SetBodyTransform(akm, Transform(akmpos.pos, bias))
+        end
+        end
+        end
+
+        --b = GetBodyTransform(LLARM)
+          --for i=1,3 do
+                --if(ppos.pos[i]<b.pos[i]) then
+                     --biasb[i] = -weightb
+                --elseif(ppos.pos[i]>b.pos[i]) then
+                  --  biasb[i] = weightb
+                --else
+                  --  biasb[i] = 0
+                --end
+            --end
+            --local currentVelocity = GetBodyVelocity(LLARM)
+            if alive then
+            	if agro then
+            local ppos = enemy
+            local bmi, bma = GetBodyBounds(LLARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(LLARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(LLARM, vel)
+        local bmi, bma = GetBodyBounds(RRARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(RRARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(RRARM, vel)
+        end
+        end
+        end
+        end
+          --akmpos.rot = Rot
+          --SetBodyTransform(akm, akmpos)
+        --HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
+        	if bleed then
+        	if IsBodyBroken(Head) then
+
+        		for i=1, 9 do
+        		 	 thingz = FindJoints("eye")
+        		 	 for i=1, #thingz do
+        		 	 	thinz = thingz[i]
+        		 	 	Delete(thinz)
+        		 	 end
+        		 end
+
+        		for i=1,Bleed/2 do
+        		smoke()
+        	end
+        end
+        end
+        if bleed then
+
+        		if HeadBloodCapacity < MaxBloodCapacity then
+        		Bleed = Bleed * 6 
+        		for i=1,Bleed/6 do
+        		smoke()
+        	end
+        	end
+
+        HeadBloodLevel = HeadBloodLevel - Bleed/2
+        end
+        	if HeadBloodLevel <= 0 then
+        		bleed = false
+        		HeadBloodLevel = 0
+        	end
+        	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
+        	if bleed1 then
+        	if IsBodyBroken(Torso) then
+        		for i=1,Bleed1/regularantibleed do
+        		smoke1()
+        	end
+        end
+        end
+        if bleed1 then
+
+        		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
+        		Bleed1 = Bleed1 * 6 
+        		 for i=1, 9 do
+        		 	 things = FindBodies("gut", true)
+        		 	 for i=1, #things do
+        		 	 	thing = things[i]
+        		 	 	SetBodyDynamic(thing, true)
+        		 	 end
+        		 end
+        		for i=1,Bleed1/extremeantibleed do
+        		smoke1()
+        	end
+        	end
+
+        TorsoBloodLevel = TorsoBloodLevel - Bleed1
+        end
+        	if TorsoBloodLevel <= 0 then
+        		bleed1 = false
+        		TorsoBloodLevel = 0
+        	end
+        -- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
+        if bleed2 then
+
+        	if LARMBloodCapacity < MaxBloodCapacity2/3 then
+        		Bleed2 = Bleed2 * 6 
+        		for i=1,Bleed2/extremeantibleed do
+        		smoke2()
+        	end
+        	end
+
+        	if IsBodyBroken(LARM) then
+        		for i=1,Bleed2/limbantibleed do
+        		smoke2()
+        	end
+        end
+        end
+        if bleed2 then
+        LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
+        end
+        	if LARMBloodLevel <= 0 then
+        		bleed2 = false
+        		LARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        if bleed3 then
+
+        	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
+        		Bleed3 = Bleed3 * 6 
+        		for i=1,Bleed3/extremeantibleed do
+        		smoke3()
+        	end
+        	end
+
+        	if IsBodyBroken(LLARM) then
+        		for i=1,Bleed3/limbantibleed do
+        		smoke3()
+        	end
+        end
+        end
+        if bleed3 then
+        LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
+        end
+        	if LLARMBloodLevel <= 0 then
+        		bleed3 = false
+        		LLARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed4 then
+
+        		if RARMBloodCapacity < MaxBloodCapacity4/3 then
+        		Bleed4 = Bleed4 * 6 
+        		for i=1,Bleed4/extremeantibleed do
+        		smoke4()
+        	end
+        	end
+
+        	if IsBodyBroken(RARM) then
+        		for i=1,Bleed4/limbantibleed do
+        		smoke4()
+        	end
+        end
+        end
+        if bleed4 then
+        RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
+        end
+        	if RARMBloodLevel <= 0 then
+        		bleed4 = false
+        		RARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed5 then
+
+        		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
+        		Bleed5 = Bleed5 * 6 
+        		for i=1,Bleed5/extremeantibleed do
+        		smoke5()
+        	end
+        	end
+
+        	if IsBodyBroken(RRARM) then
+        		for i=1,Bleed5/limbantibleed do
+        		smoke5()
+        	end
+        end
+        end
+        if bleed5 then
+        RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
+        end
+        	if RRARMBloodLevel <= 0 then
+        		bleed5 = false
+        		RRARMBloodLevel = 0
+        	end
+        	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
+        	if bleed6 then
+
+        		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
+        		Bleed6 = Bleed6 * 6 
+        		for i=1,Bleed6/extremeantibleed do
+        		smoke6()
+        	end
+        	end
+
+        	if IsBodyBroken(LLEG) then
+        		for i=1,Bleed6/limbantibleed do
+        		smoke6()
+        	end
+        end
+        end
+        if bleed6 then
+        LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
+        end
+        	if LLEGBloodLevel <= 0 then
+        		bleed6 = false
+        	LLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed7 then
+
+        		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
+        		Bleed7 = Bleed7 * 6 
+        		for i=1,Bleed7/extremeantibleed do
+        		smoke7()
+        	end
+        	end
+
+        	if IsBodyBroken(LLLEG) then
+        		for i=1,Bleed7/limbantibleed do
+        		smoke7()
+        	end
+        end
+        end
+        if bleed7 then
+        LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
+        end
+        	if LLLEGBloodLevel <= 0 then
+        		bleed7 = false
+        	LLLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed8 then
+
+        		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
+        		Bleed8 = Bleed8 * 6 
+        		for i=1,Bleed8/extremeantibleed do
+        		smoke8()
+        	end
+        	end
+
+        	if IsBodyBroken(RLEG) then
+        		for i=1,Bleed8/limbantibleed do
+        		smoke8()
+        	end
+        end
+        end
+        if bleed8 then
+        RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
+        end
+        	if RLEGBloodLevel <= 0 then
+        		bleed8 = false
+        	RLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed9 then
+
+        		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
+        		Bleed9 = Bleed9 * 6 
+        		for i=1,Bleed9/extremeantibleed do
+        		smoke9()
+        	end
+        	end
+
+        	if IsBodyBroken(RRLEG) then
+        		for i=1,Bleed9/limbantibleed do
+        		smoke9()
+        	end
+        end
+        end
+        if bleed9 then
+        RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
+        end
+        	if RRLEGBloodLevel <= 0 then
+        		bleed9 = false
+        	RRLEGBloodLevel = 0
+        	end
+        	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
+        	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
+        	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
+        		upspeed[2] = TotalLegBloodValue/10000
+        	currentvel = GetBodyVelocity(Head)
+        	currentvel1 = GetBodyVelocity(LLLEG)
+        	currentvel2 = GetBodyVelocity(RRLEG)
+        	if IsBodyBroken(Head) then
+        		alive = false
+        	end
+        	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
+        		alive = false
+        	end
+        	if TotalBloodValue < MinBloodValue then
+        		alive = false
+        	end
+        	if alive then
+        	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
+        	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
+        	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
+        end
+        a = GetPlayerTransform(playerId)
+        	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
+        	if distToPlayer < 3 then
+        		inrange = true
+        	else
+        		inrange = false
+        	end
+    end
+end
+
+function client.init()
+    GunShot = LoadSound("MOD/gorescript/mp7.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    	if InputPressed("H") then
+    		if switched then
+    			enabled = false
+    			switched = false
+    		else if not switched then
+    			enabled = true
+    		switched = true
+    		end
+    	end
+        if shoot then
+    	if KillTimer > Eliminate then
+    		if not disarmed then
+    		if not reloading then
+    		shootim = shootim + dt * firerate
+    		if shootim > 0.1 then
+    		Shoot(shootpos, direction)
+    		PlaySound(GunShot, shootpos,10)
+    		SetLightEnabled(flare, true)
+    		flaretim = true
+    		for i=1,33 do
+    		GunSmoke()
+    	end
+    		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
+    		shootim = 0
+    		shots = shots + 1
+    	end
+    end
+    	end
+    end
+    end
+end
+
+function client.draw()
+    if drawtext then
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("Head Blood Level:  "..HeadBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 220)
+          UiFont("bold.ttf", 30)
+          UiText("Torso Blood Level:  "..TorsoBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 240)
+          UiFont("bold.ttf", 30)
+          UiText("upper left arm Blood Level:  "..LARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 260)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 280)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 300)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 320)
+          UiFont("bold.ttf", 30)
+          UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 340)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 360)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 380)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 400)
+          UiFont("bold.ttf", 30)
+          UiText("total Blood Level:  "..TotalBloodValue)
+        UiPop()
+    end
+    if inrange then
+    	if enabled then
+
+    			UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 300)
+          UiColor(0,0,1)
+          UiFont("bold.ttf", 30)
+          UiText("To disable viewable ragdoll stats, press H ")
+        UiPop()
+
+    	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 350)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 30)
+          UiText("Total Blood Volume:  "..TotalBloodValue)
+        UiPop()
+
+        if alive then
+        	  UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 60)
+          UiText("ALIVE")
+        UiPop()
+        if TotalBloodValue < 15000 then
+        	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 450)
+          UiColor(1,1,0)
+          UiFont("bold.ttf", 50)
+          UiText("CRITICAL CONDITION")
+        UiPop()
+        end
+    end
+    if not alive then
+    	  UiPush()
+    	  UiColor(1,0,0)
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiFont("bold.ttf", 60)
+          UiText("DECEASED")
+        UiPop()
+    end
+    end
+    end
+end
+

```

---

# Migration Report: gorescript\gorenormman.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/gorescript\gorenormman.lua
+++ patched/gorescript\gorenormman.lua
@@ -1,492 +1,4 @@
-function init()
-	Head = FindBody("Head")
-	HeadBloodCapacity = GetBodyMass(Head)
-	HeadBloodLevel = HeadBloodCapacity * 20
-	StartingBleed = HeadBloodCapacity
-	MaxBloodCapacity = GetBodyMass(Head)
-	bleed = true
-
-	Torso = FindBody("Torso")
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	TorsoBloodLevel = TorsoBloodCapacity * 20
-	StartingBleed1 = TorsoBloodCapacity
-	MaxBloodCapacity1 = GetBodyMass(Torso)
-	bleed1 = true
-
-	LARM = FindBody("LARM")
-	LARMBloodCapacity = GetBodyMass(LARM)
-	LARMBloodLevel = LARMBloodCapacity * 20
-	StartingBleed2 = LARMBloodCapacity
-	MaxBloodCapacity2 = GetBodyMass(LARM)
-
-	bleed2 = true
-
-	LLARM = FindBody("LLARM")
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	LLARMBloodLevel = LLARMBloodCapacity * 20
-	StartingBleed3 = LLARMBloodCapacity
-	MaxBloodCapacity3 = GetBodyMass(LLARM)
-	bleed3 = true
-
-	RARM = FindBody("RARM")
-	RARMBloodCapacity = GetBodyMass(RARM)
-	RARMBloodLevel = RARMBloodCapacity * 20
-	StartingBleed4 = RARMBloodCapacity
-	MaxBloodCapacity4 = GetBodyMass(RARM)
-	bleed4 = true
-
-	RRARM = FindBody("RRARM")
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	RRARMBloodLevel = RRARMBloodCapacity * 20
-	StartingBleed5 = RRARMBloodCapacity
-	MaxBloodCapacity5 = GetBodyMass(RRARM)
-	bleed5 = true
-
-	LLEG = FindBody("LLEG")
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	LLEGBloodLevel = LLEGBloodCapacity * 20
-	StartingBleed6 = LLEGBloodCapacity
-	MaxBloodCapacity6 = GetBodyMass(LLEG)
-	bleed6 = true
-
-	LLLEG = FindBody("LLLEG")
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	LLLEGBloodLevel = LLLEGBloodCapacity * 20
-	StartingBleed7 = LLLEGBloodCapacity
-	MaxBloodCapacity7 = GetBodyMass(LLLEG)
-	bleed7 = true
-
-	RLEG = FindBody("RLEG")
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	RLEGBloodLevel = RLEGBloodCapacity * 20
-	StartingBleed8 = RLEGBloodCapacity
-	MaxBloodCapacity8 = GetBodyMass(RLEG)
-	bleed8 = true
-
-	RRLEG = FindBody("RRLEG")
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	RRLEGBloodLevel = RRLEGBloodCapacity * 20
-	StartingBleed9 = RRLEGBloodCapacity
-	MaxBloodCapacity9 = GetBodyMass(RRLEG)
-	bleed9 = true
-
-	antibleed = 15 -- only affects smoke speed
-	extremeantibleed = 500 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
-	regularantibleed = 30 -- affects cureable bleeds, reduce to have more blood in general
-	limbantibleed = 30 -- affects bleeding of limbs, decrease to have more blood from arms and legs
-	MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
-
-	LimbBleedSpeed = 0.1
-
-	bloodgrav = -20
-	blooddrag = 0
-	standup = 1
-	startupspeed = Vec(0,standup,0)
-	upspeed = Vec(0,standup,0)
-	downspeed = Vec(0,-standup,0)
-	alive = true
-	enabled = true
-	switched = true
-end
-
-
-function tick()
-
-	if IsBodyBroken(Head) then
-		alive = false
-	end
-
-	if InputPressed("H") then
-		if switched then
-			enabled = false
-			switched = false
-		else if not switched then
-			enabled = true
-		switched = true
-		end
-	end
-end
-
-	drawtext = false
-
-	HeadBloodCapacity = GetBodyMass(Head)
-	Bleed = StartingBleed - HeadBloodCapacity
-	HeadPos = GetBodyTransform(Head)
-
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	Bleed1 = StartingBleed1 - TorsoBloodCapacity
-	TorsoPos = GetBodyTransform(Torso)
-
-	LARMBloodCapacity = GetBodyMass(LARM)
-	Bleed2 = StartingBleed2 - LARMBloodCapacity
-	LARMPos = GetBodyTransform(LARM)
-
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	Bleed3 = StartingBleed3 - LLARMBloodCapacity
-	LLARMPos = GetBodyTransform(LLARM)
-
-	RARMBloodCapacity = GetBodyMass(RARM)
-	Bleed4 = StartingBleed4 - RARMBloodCapacity
-	RARMPos = GetBodyTransform(RARM)
-
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	Bleed5 = StartingBleed5 - RRARMBloodCapacity
-	RRARMPos = GetBodyTransform(RRARM)
-
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	Bleed6 = StartingBleed6 - LLEGBloodCapacity
-	LLEGPos = GetBodyTransform(LLEG)
-
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
-	LLLEGPos = GetBodyTransform(LLLEG)
-
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	Bleed8 = StartingBleed8 - RLEGBloodCapacity
-	RLEGPos = GetBodyTransform(RLEG)
-
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
-	RRLEGPos = GetBodyTransform(RRLEG)
-
---HEAD HEAD HEAD HEAD HEAD HEAD LLEGHEAD HEAD HEAD HEAD
-	if bleed then
-	if IsBodyBroken(Head) then
-
-		for i=1, 9 do
-		 	 thingz = FindJoints("eye")
-		 	 for i=1, #thingz do
-		 	 	thinz = thingz[i]
-		 	 	Delete(thinz)
-		 	 end
-		 end
-
-		for i=1,Bleed/2 do
-		smoke()
-	end
-end
-end
-
-if bleed then
-	
-		if HeadBloodCapacity < MaxBloodCapacity then
-		Bleed = Bleed * 6 
-
-		for i=1,Bleed/6 do
-		smoke()
-	end
-	end
-
-HeadBloodLevel = HeadBloodLevel - Bleed/2
-end
-
-	if HeadBloodLevel <= 0 then
-		bleed = false
-		HeadBloodLevel = 0
-	end
-
-	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
-
-	if bleed1 then
-	if IsBodyBroken(Torso) then
-		for i=1,Bleed1/regularantibleed do
-		smoke1()
-	end
-end
-end
-
-if bleed1 then
-
-		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
-		Bleed1 = Bleed1 * 6 
-
-		 for i=1, 9 do
-		 	 things = FindBodies("gut", true)
-		 	 for i=1, #things do
-		 	 	thing = things[i]
-		 	 	SetBodyDynamic(thing, true)
-		 	 end
-		 end
-		for i=1,Bleed1/extremeantibleed do
-		smoke1()
-	end
-	end
-
-TorsoBloodLevel = TorsoBloodLevel - Bleed1
-end
-
-	if TorsoBloodLevel <= 0 then
-		bleed1 = false
-		TorsoBloodLevel = 0
-	end
-
--- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
-
-if bleed2 then
-
-	if LARMBloodCapacity < MaxBloodCapacity2/3 then
-		Bleed2 = Bleed2 * 6 
-
-		for i=1,Bleed2/extremeantibleed do
-		smoke2()
-	end
-	end
-
-	if IsBodyBroken(LARM) then
-		for i=1,Bleed2/limbantibleed do
-		smoke2()
-	end
-end
-end
-
-if bleed2 then
-LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
-end
-
-	if LARMBloodLevel <= 0 then
-		bleed2 = false
-		LARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-if bleed3 then
-
-	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
-		Bleed3 = Bleed3 * 6 
-
-		for i=1,Bleed3/extremeantibleed do
-		smoke3()
-	end
-	end
-
-	if IsBodyBroken(LLARM) then
-		for i=1,Bleed3/limbantibleed do
-		smoke3()
-	end
-end
-end
-
-if bleed3 then
-LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
-end
-
-	if LLARMBloodLevel <= 0 then
-		bleed3 = false
-		LLARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed4 then
-
-		if RARMBloodCapacity < MaxBloodCapacity4/3 then
-		Bleed4 = Bleed4 * 6 
-
-		for i=1,Bleed4/extremeantibleed do
-		smoke4()
-	end
-	end
-
-	if IsBodyBroken(RARM) then
-		for i=1,Bleed4/limbantibleed do
-		smoke4()
-	end
-end
-end
-
-if bleed4 then
-RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
-end
-
-	if RARMBloodLevel <= 0 then
-		bleed4 = false
-		RARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed5 then
-
-		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
-		Bleed5 = Bleed5 * 6 
-
-		for i=1,Bleed5/extremeantibleed do
-		smoke5()
-	end
-	end
-
-	if IsBodyBroken(RRARM) then
-		for i=1,Bleed5/limbantibleed do
-		smoke5()
-	end
-end
-end
-
-if bleed5 then
-RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
-end
-
-	if RRARMBloodLevel <= 0 then
-		bleed5 = false
-		RRARMBloodLevel = 0
-	end
-
-	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
-
-	if bleed6 then
-
-		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
-		Bleed6 = Bleed6 * 6 
-
-		for i=1,Bleed6/extremeantibleed do
-		smoke6()
-	end
-	end
-
-	if IsBodyBroken(LLEG) then
-		for i=1,Bleed6/limbantibleed do
-		smoke6()
-	end
-end
-end
-
-if bleed6 then
-LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
-end
-
-	if LLEGBloodLevel <= 0 then
-		bleed6 = false
-	LLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed7 then
-
-		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
-		Bleed7 = Bleed7 * 6 
-
-		for i=1,Bleed7/extremeantibleed do
-		smoke7()
-	end
-	end
-
-	if IsBodyBroken(LLLEG) then
-		for i=1,Bleed7/limbantibleed do
-		smoke7()
-	end
-end
-end
-
-if bleed7 then
-LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
-end
-
-	if LLLEGBloodLevel <= 0 then
-		bleed7 = false
-	LLLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed8 then
-
-		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
-		Bleed8 = Bleed8 * 6 
-
-		for i=1,Bleed8/extremeantibleed do
-		smoke8()
-	end
-	end
-
-	if IsBodyBroken(RLEG) then
-		for i=1,Bleed8/limbantibleed do
-		smoke8()
-	end
-end
-end
-
-if bleed8 then
-RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
-end
-
-	if RLEGBloodLevel <= 0 then
-		bleed8 = false
-	RLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed9 then
-
-		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
-		Bleed9 = Bleed9 * 6 
-
-		for i=1,Bleed9/extremeantibleed do
-		smoke9()
-	end
-	end
-
-	if IsBodyBroken(RRLEG) then
-		for i=1,Bleed9/limbantibleed do
-		smoke9()
-	end
-end
-end
-
-if bleed9 then
-RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
-end
-
-	if RRLEGBloodLevel <= 0 then
-		bleed9 = false
-	RRLEGBloodLevel = 0
-	end
-
-	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
-	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
-
-	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
-		upspeed[2] = TotalLegBloodValue/10000
-
-
-
-	currentvel = GetBodyVelocity(Head)
-	currentvel1 = GetBodyVelocity(LLLEG)
-	currentvel2 = GetBodyVelocity(RRLEG)
-
-	if IsBodyBroken(Head) then
-		alive = false
-	end
-
-	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
-		alive = false
-	end
-
-	if TotalBloodValue < MinBloodValue then
-		alive = false
-	end
-	if alive then
-	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
-	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
-	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
-end
-
-a = GetPlayerTransform()
-
-	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
-
-	if distToPlayer < 3 then
-		inrange = true
-	else
-		inrange = false
-	end
-
-
-end
-
-
+#version 2
 function smoke()
     --spawn sparks
     ParticleType("smoke")
@@ -627,129 +139,545 @@
     SpawnParticle(RRLEGPos.pos, Vec(math.random(-Bleed3/antibleed, Bleed3/antibleed), math.random(-Bleed3/antibleed, Bleed3/antibleed), math.random(-Bleed3/antibleed, Bleed3/antibleed)),10)
 end
 
-function draw()
-if drawtext then
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("Head Blood Level:  "..HeadBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 220)
-      UiFont("bold.ttf", 30)
-      UiText("Torso Blood Level:  "..TorsoBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 240)
-      UiFont("bold.ttf", 30)
-      UiText("upper left arm Blood Level:  "..LARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 260)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 280)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 300)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 320)
-      UiFont("bold.ttf", 30)
-      UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 340)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 360)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 380)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 400)
-      UiFont("bold.ttf", 30)
-      UiText("total Blood Level:  "..TotalBloodValue)
-    UiPop()
-end
-if inrange then
-	if enabled then
-	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 300)
-      UiColor(0,0,1)
-     UiFont("bold.ttf", 30)
-      UiText("To disable viewable ragdoll stats, press H ")
-    UiPop()
-	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 350)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 30)
-      UiText("Total Blood Volume:  "..TotalBloodValue)
-    UiPop()
-
-    if alive then
+function server.init()
+    Head = FindBody("Head")
+    HeadBloodCapacity = GetBodyMass(Head)
+    HeadBloodLevel = HeadBloodCapacity * 20
+    StartingBleed = HeadBloodCapacity
+    MaxBloodCapacity = GetBodyMass(Head)
+    bleed = true
+    Torso = FindBody("Torso")
+    TorsoBloodCapacity = GetBodyMass(Torso)
+    TorsoBloodLevel = TorsoBloodCapacity * 20
+    StartingBleed1 = TorsoBloodCapacity
+    MaxBloodCapacity1 = GetBodyMass(Torso)
+    bleed1 = true
+    LARM = FindBody("LARM")
+    LARMBloodCapacity = GetBodyMass(LARM)
+    LARMBloodLevel = LARMBloodCapacity * 20
+    StartingBleed2 = LARMBloodCapacity
+    MaxBloodCapacity2 = GetBodyMass(LARM)
+    bleed2 = true
+    LLARM = FindBody("LLARM")
+    LLARMBloodCapacity = GetBodyMass(LLARM)
+    LLARMBloodLevel = LLARMBloodCapacity * 20
+    StartingBleed3 = LLARMBloodCapacity
+    MaxBloodCapacity3 = GetBodyMass(LLARM)
+    bleed3 = true
+    RARM = FindBody("RARM")
+    RARMBloodCapacity = GetBodyMass(RARM)
+    RARMBloodLevel = RARMBloodCapacity * 20
+    StartingBleed4 = RARMBloodCapacity
+    MaxBloodCapacity4 = GetBodyMass(RARM)
+    bleed4 = true
+    RRARM = FindBody("RRARM")
+    RRARMBloodCapacity = GetBodyMass(RRARM)
+    RRARMBloodLevel = RRARMBloodCapacity * 20
+    StartingBleed5 = RRARMBloodCapacity
+    MaxBloodCapacity5 = GetBodyMass(RRARM)
+    bleed5 = true
+    LLEG = FindBody("LLEG")
+    LLEGBloodCapacity = GetBodyMass(LLEG)
+    LLEGBloodLevel = LLEGBloodCapacity * 20
+    StartingBleed6 = LLEGBloodCapacity
+    MaxBloodCapacity6 = GetBodyMass(LLEG)
+    bleed6 = true
+    LLLEG = FindBody("LLLEG")
+    LLLEGBloodCapacity = GetBodyMass(LLLEG)
+    LLLEGBloodLevel = LLLEGBloodCapacity * 20
+    StartingBleed7 = LLLEGBloodCapacity
+    MaxBloodCapacity7 = GetBodyMass(LLLEG)
+    bleed7 = true
+    RLEG = FindBody("RLEG")
+    RLEGBloodCapacity = GetBodyMass(RLEG)
+    RLEGBloodLevel = RLEGBloodCapacity * 20
+    StartingBleed8 = RLEGBloodCapacity
+    MaxBloodCapacity8 = GetBodyMass(RLEG)
+    bleed8 = true
+    RRLEG = FindBody("RRLEG")
+    RRLEGBloodCapacity = GetBodyMass(RRLEG)
+    RRLEGBloodLevel = RRLEGBloodCapacity * 20
+    StartingBleed9 = RRLEGBloodCapacity
+    MaxBloodCapacity9 = GetBodyMass(RRLEG)
+    bleed9 = true
+    antibleed = 15 -- only affects smoke speed
+    extremeantibleed = 500 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
+    regularantibleed = 30 -- affects cureable bleeds, reduce to have more blood in general
+    limbantibleed = 30 -- affects bleeding of limbs, decrease to have more blood from arms and legs
+    MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
+    LimbBleedSpeed = 0.1
+    bloodgrav = -20
+    blooddrag = 0
+    standup = 1
+    startupspeed = Vec(0,standup,0)
+    upspeed = Vec(0,standup,0)
+    downspeed = Vec(0,-standup,0)
+    alive = true
+    enabled = true
+    switched = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        	if IsBodyBroken(Head) then
+        		alive = false
+        	end
+        end
+        	drawtext = false
+        	HeadBloodCapacity = GetBodyMass(Head)
+        	Bleed = StartingBleed - HeadBloodCapacity
+        	HeadPos = GetBodyTransform(Head)
+        	TorsoBloodCapacity = GetBodyMass(Torso)
+        	Bleed1 = StartingBleed1 - TorsoBloodCapacity
+        	TorsoPos = GetBodyTransform(Torso)
+        	LARMBloodCapacity = GetBodyMass(LARM)
+        	Bleed2 = StartingBleed2 - LARMBloodCapacity
+        	LARMPos = GetBodyTransform(LARM)
+        	LLARMBloodCapacity = GetBodyMass(LLARM)
+        	Bleed3 = StartingBleed3 - LLARMBloodCapacity
+        	LLARMPos = GetBodyTransform(LLARM)
+        	RARMBloodCapacity = GetBodyMass(RARM)
+        	Bleed4 = StartingBleed4 - RARMBloodCapacity
+        	RARMPos = GetBodyTransform(RARM)
+        	RRARMBloodCapacity = GetBodyMass(RRARM)
+        	Bleed5 = StartingBleed5 - RRARMBloodCapacity
+        	RRARMPos = GetBodyTransform(RRARM)
+        	LLEGBloodCapacity = GetBodyMass(LLEG)
+        	Bleed6 = StartingBleed6 - LLEGBloodCapacity
+        	LLEGPos = GetBodyTransform(LLEG)
+        	LLLEGBloodCapacity = GetBodyMass(LLLEG)
+        	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
+        	LLLEGPos = GetBodyTransform(LLLEG)
+        	RLEGBloodCapacity = GetBodyMass(RLEG)
+        	Bleed8 = StartingBleed8 - RLEGBloodCapacity
+        	RLEGPos = GetBodyTransform(RLEG)
+        	RRLEGBloodCapacity = GetBodyMass(RRLEG)
+        	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
+        	RRLEGPos = GetBodyTransform(RRLEG)
+        --HEAD HEAD HEAD HEAD HEAD HEAD LLEGHEAD HEAD HEAD HEAD
+        	if bleed then
+        	if IsBodyBroken(Head) then
+
+        		for i=1, 9 do
+        		 	 thingz = FindJoints("eye")
+        		 	 for i=1, #thingz do
+        		 	 	thinz = thingz[i]
+        		 	 	Delete(thinz)
+        		 	 end
+        		 end
+
+        		for i=1,Bleed/2 do
+        		smoke()
+        	end
+        end
+        end
+        if bleed then
+
+        		if HeadBloodCapacity < MaxBloodCapacity then
+        		Bleed = Bleed * 6 
+
+        		for i=1,Bleed/6 do
+        		smoke()
+        	end
+        	end
+
+        HeadBloodLevel = HeadBloodLevel - Bleed/2
+        end
+        	if HeadBloodLevel <= 0 then
+        		bleed = false
+        		HeadBloodLevel = 0
+        	end
+        	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
+        	if bleed1 then
+        	if IsBodyBroken(Torso) then
+        		for i=1,Bleed1/regularantibleed do
+        		smoke1()
+        	end
+        end
+        end
+        if bleed1 then
+
+        		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
+        		Bleed1 = Bleed1 * 6 
+
+        		 for i=1, 9 do
+        		 	 things = FindBodies("gut", true)
+        		 	 for i=1, #things do
+        		 	 	thing = things[i]
+        		 	 	SetBodyDynamic(thing, true)
+        		 	 end
+        		 end
+        		for i=1,Bleed1/extremeantibleed do
+        		smoke1()
+        	end
+        	end
+
+        TorsoBloodLevel = TorsoBloodLevel - Bleed1
+        end
+        	if TorsoBloodLevel <= 0 then
+        		bleed1 = false
+        		TorsoBloodLevel = 0
+        	end
+        -- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
+        if bleed2 then
+
+        	if LARMBloodCapacity < MaxBloodCapacity2/3 then
+        		Bleed2 = Bleed2 * 6 
+
+        		for i=1,Bleed2/extremeantibleed do
+        		smoke2()
+        	end
+        	end
+
+        	if IsBodyBroken(LARM) then
+        		for i=1,Bleed2/limbantibleed do
+        		smoke2()
+        	end
+        end
+        end
+        if bleed2 then
+        LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
+        end
+        	if LARMBloodLevel <= 0 then
+        		bleed2 = false
+        		LARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        if bleed3 then
+
+        	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
+        		Bleed3 = Bleed3 * 6 
+
+        		for i=1,Bleed3/extremeantibleed do
+        		smoke3()
+        	end
+        	end
+
+        	if IsBodyBroken(LLARM) then
+        		for i=1,Bleed3/limbantibleed do
+        		smoke3()
+        	end
+        end
+        end
+        if bleed3 then
+        LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
+        end
+        	if LLARMBloodLevel <= 0 then
+        		bleed3 = false
+        		LLARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed4 then
+
+        		if RARMBloodCapacity < MaxBloodCapacity4/3 then
+        		Bleed4 = Bleed4 * 6 
+
+        		for i=1,Bleed4/extremeantibleed do
+        		smoke4()
+        	end
+        	end
+
+        	if IsBodyBroken(RARM) then
+        		for i=1,Bleed4/limbantibleed do
+        		smoke4()
+        	end
+        end
+        end
+        if bleed4 then
+        RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
+        end
+        	if RARMBloodLevel <= 0 then
+        		bleed4 = false
+        		RARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed5 then
+
+        		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
+        		Bleed5 = Bleed5 * 6 
+
+        		for i=1,Bleed5/extremeantibleed do
+        		smoke5()
+        	end
+        	end
+
+        	if IsBodyBroken(RRARM) then
+        		for i=1,Bleed5/limbantibleed do
+        		smoke5()
+        	end
+        end
+        end
+        if bleed5 then
+        RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
+        end
+        	if RRARMBloodLevel <= 0 then
+        		bleed5 = false
+        		RRARMBloodLevel = 0
+        	end
+        	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
+        	if bleed6 then
+
+        		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
+        		Bleed6 = Bleed6 * 6 
+
+        		for i=1,Bleed6/extremeantibleed do
+        		smoke6()
+        	end
+        	end
+
+        	if IsBodyBroken(LLEG) then
+        		for i=1,Bleed6/limbantibleed do
+        		smoke6()
+        	end
+        end
+        end
+        if bleed6 then
+        LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
+        end
+        	if LLEGBloodLevel <= 0 then
+        		bleed6 = false
+        	LLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed7 then
+
+        		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
+        		Bleed7 = Bleed7 * 6 
+
+        		for i=1,Bleed7/extremeantibleed do
+        		smoke7()
+        	end
+        	end
+
+        	if IsBodyBroken(LLLEG) then
+        		for i=1,Bleed7/limbantibleed do
+        		smoke7()
+        	end
+        end
+        end
+        if bleed7 then
+        LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
+        end
+        	if LLLEGBloodLevel <= 0 then
+        		bleed7 = false
+        	LLLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed8 then
+
+        		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
+        		Bleed8 = Bleed8 * 6 
+
+        		for i=1,Bleed8/extremeantibleed do
+        		smoke8()
+        	end
+        	end
+
+        	if IsBodyBroken(RLEG) then
+        		for i=1,Bleed8/limbantibleed do
+        		smoke8()
+        	end
+        end
+        end
+        if bleed8 then
+        RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
+        end
+        	if RLEGBloodLevel <= 0 then
+        		bleed8 = false
+        	RLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed9 then
+
+        		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
+        		Bleed9 = Bleed9 * 6 
+
+        		for i=1,Bleed9/extremeantibleed do
+        		smoke9()
+        	end
+        	end
+
+        	if IsBodyBroken(RRLEG) then
+        		for i=1,Bleed9/limbantibleed do
+        		smoke9()
+        	end
+        end
+        end
+        if bleed9 then
+        RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
+        end
+        	if RRLEGBloodLevel <= 0 then
+        		bleed9 = false
+        	RRLEGBloodLevel = 0
+        	end
+        	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
+        	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
+        	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
+        		upspeed[2] = TotalLegBloodValue/10000
+        	currentvel = GetBodyVelocity(Head)
+        	currentvel1 = GetBodyVelocity(LLLEG)
+        	currentvel2 = GetBodyVelocity(RRLEG)
+        	if IsBodyBroken(Head) then
+        		alive = false
+        	end
+        	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
+        		alive = false
+        	end
+        	if TotalBloodValue < MinBloodValue then
+        		alive = false
+        	end
+        	if alive then
+        	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
+        	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
+        	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
+        end
+        a = GetPlayerTransform(playerId)
+        	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
+        	if distToPlayer < 3 then
+        		inrange = true
+        	else
+        		inrange = false
+        	end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("H") then
+    	if switched then
+    		enabled = false
+    		switched = false
+    	else if not switched then
+    		enabled = true
+    	switched = true
+    	end
+    end
+end
+
+function client.draw()
+    if drawtext then
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("Head Blood Level:  "..HeadBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 220)
+          UiFont("bold.ttf", 30)
+          UiText("Torso Blood Level:  "..TorsoBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 240)
+          UiFont("bold.ttf", 30)
+          UiText("upper left arm Blood Level:  "..LARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 260)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 280)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 300)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 320)
+          UiFont("bold.ttf", 30)
+          UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 340)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 360)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 380)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 400)
+          UiFont("bold.ttf", 30)
+          UiText("total Blood Level:  "..TotalBloodValue)
+        UiPop()
+    end
+    if inrange then
+    	if enabled then
+    	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 300)
+          UiColor(0,0,1)
+         UiFont("bold.ttf", 30)
+          UiText("To disable viewable ragdoll stats, press H ")
+        UiPop()
+    	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 350)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 30)
+          UiText("Total Blood Volume:  "..TotalBloodValue)
+        UiPop()
+
+        if alive then
+        	  UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 60)
+          UiText("ALIVE")
+        UiPop()
+        if TotalBloodValue < 15000 then
+        	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 450)
+          UiColor(1,1,0)
+          UiFont("bold.ttf", 50)
+          UiText("CRITICAL CONDITION")
+        UiPop()
+        end
+    end
+    if not alive then
     	  UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 60)
-      UiText("ALIVE")
-    UiPop()
-    if TotalBloodValue < 15000 then
-    	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 450)
-      UiColor(1,1,0)
-      UiFont("bold.ttf", 50)
-      UiText("CRITICAL CONDITION")
-    UiPop()
+    	  UiColor(1,0,0)
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiFont("bold.ttf", 60)
+          UiText("DECEASED")
+        UiPop()
     end
-end
-if not alive then
-	  UiPush()
-	  UiColor(1,0,0)
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiFont("bold.ttf", 60)
-      UiText("DECEASED")
-    UiPop()
-end
-end
-end
-end+    end
+    end
+end
+

```

---

# Migration Report: gorescript\gorespetsnaz.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/gorescript\gorespetsnaz.lua
+++ patched/gorescript\gorespetsnaz.lua
@@ -1,671 +1,4 @@
-function init()
-	Head = FindBody("Head")
-	HeadBloodCapacity = GetBodyMass(Head)
-	HeadBloodLevel = HeadBloodCapacity * 20
-	StartingBleed = HeadBloodCapacity
-	MaxBloodCapacity = GetBodyMass(Head)
-	bleed = true
-
-	Torso = FindBody("Torso")
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	TorsoBloodLevel = TorsoBloodCapacity * 20
-	StartingBleed1 = TorsoBloodCapacity
-	MaxBloodCapacity1 = GetBodyMass(Torso)
-	bleed1 = true
-
-	LARM = FindBody("LARM")
-	LARMBloodCapacity = GetBodyMass(LARM)
-	LARMBloodLevel = LARMBloodCapacity * 20
-	StartingBleed2 = LARMBloodCapacity
-	MaxBloodCapacity2 = GetBodyMass(LARM)
-
-	bleed2 = true
-
-	LLARM = FindBody("LLARM")
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	LLARMBloodLevel = LLARMBloodCapacity * 20
-	StartingBleed3 = LLARMBloodCapacity
-	MaxBloodCapacity3 = GetBodyMass(LLARM)
-	bleed3 = true
-
-	RARM = FindBody("RARM")
-	RARMBloodCapacity = GetBodyMass(RARM)
-	RARMBloodLevel = RARMBloodCapacity * 20
-	StartingBleed4 = RARMBloodCapacity
-	MaxBloodCapacity4 = GetBodyMass(RARM)
-	bleed4 = true
-
-	RRARM = FindBody("RRARM")
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	RRARMBloodLevel = RRARMBloodCapacity * 20
-	StartingBleed5 = RRARMBloodCapacity
-	MaxBloodCapacity5 = GetBodyMass(RRARM)
-	bleed5 = true
-
-	LLEG = FindBody("LLEG")
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	LLEGBloodLevel = LLEGBloodCapacity * 20
-	StartingBleed6 = LLEGBloodCapacity
-	MaxBloodCapacity6 = GetBodyMass(LLEG)
-	bleed6 = true
-
-	LLLEG = FindBody("LLLEG")
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	LLLEGBloodLevel = LLLEGBloodCapacity * 20
-	StartingBleed7 = LLLEGBloodCapacity
-	MaxBloodCapacity7 = GetBodyMass(LLLEG)
-	bleed7 = true
-
-	RLEG = FindBody("RLEG")
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	RLEGBloodLevel = RLEGBloodCapacity * 20
-	StartingBleed8 = RLEGBloodCapacity
-	MaxBloodCapacity8 = GetBodyMass(RLEG)
-	bleed8 = true
-
-	RRLEG = FindBody("RRLEG")
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	RRLEGBloodLevel = RRLEGBloodCapacity * 20
-	StartingBleed9 = RRLEGBloodCapacity
-	MaxBloodCapacity9 = GetBodyMass(RRLEG)
-	bleed9 = true
-
-	antibleed = 15 -- only affects smoke speed
-	extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
-	regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
-	limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
-	MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
-
-	LimbBleedSpeed = 0.1
-
-	bloodgrav = -20
-	blooddrag = 0
-	startupspeed = Vec(0,0.7,0)
-	upspeed = Vec(0,2,0)
-	downspeed = Vec(0,-1,0)
-	alive = true
-
-	akm = FindBody("AKM")
-	weight = 2
-	bias = Vec(0,0,0)
-	biasb = Vec(0,0,0)
-	weightb = -0.4
-	agrotimer = 0
-	forget = 10
-	KillTimer = 0
-	Eliminate = 1
-	shootim = 0
-	shots = 0
-	reload = 0
-	recoil = 2
-
-	flare = FindLight("flare")
-	flaretim = false
-	flaretimer = 0
-	SetLightEnabled(flare, false)
-	disarmed = false
-	spetsnaz = FindShape("terrorist",true)
-	GunShot = LoadSound("MOD/gorescript/m4.ogg")
-	enemyspotted = false
-	enabled = true
-	disabled = false
-	switched = true
-
-end
-
-
-function tick(dt)
-
-		if InputPressed("H") then
-		if switched then
-			enabled = false
-			switched = false
-		else if not switched then
-			enabled = true
-		switched = true
-		end
-	end
-end
-
-	if IsShapeBroken(spetsnaz) then
-		RemoveTag(spetsnaz,"terrorist")
-		agro = false
-		agrotimer = 0
-		spetsnaz = FindShape("terrorist",true)
-		enemyspotted = false
-		shoot = false
-	end
-
-	if PlayerHP == 0 then
-		shoot = false
-		agro = false
-		agrotimer = 0
-		enemyspotted = false
-	end
-	gunTrans = GetBodyTransform(Head)
-	gunPos = gunTrans.pos
-	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
-	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
-
-	drawtext = false
-
-	HeadBloodCapacity = GetBodyMass(Head)
-	Bleed = StartingBleed - HeadBloodCapacity
-	HeadPos = GetBodyTransform(Head)
-
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	Bleed1 = StartingBleed1 - TorsoBloodCapacity
-	TorsoPos = GetBodyTransform(Torso)
-
-	LARMBloodCapacity = GetBodyMass(LARM)
-	Bleed2 = StartingBleed2 - LARMBloodCapacity
-	LARMPos = GetBodyTransform(LARM)
-
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	Bleed3 = StartingBleed3 - LLARMBloodCapacity
-	LLARMPos = GetBodyTransform(LLARM)
-
-	RARMBloodCapacity = GetBodyMass(RARM)
-	Bleed4 = StartingBleed4 - RARMBloodCapacity
-	RARMPos = GetBodyTransform(RARM)
-
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	Bleed5 = StartingBleed5 - RRARMBloodCapacity
-	RRARMPos = GetBodyTransform(RRARM)
-
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	Bleed6 = StartingBleed6 - LLEGBloodCapacity
-	LLEGPos = GetBodyTransform(LLEG)
-
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
-	LLLEGPos = GetBodyTransform(LLLEG)
-
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	Bleed8 = StartingBleed8 - RLEGBloodCapacity
-	RLEGPos = GetBodyTransform(RLEG)
-
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
-	RRLEGPos = GetBodyTransform(RRLEG)
-
-	--AGRESSIVE BEHAVIOR
-
-	if IsBodyBroken(LLARM) then
-		disarmed = true
-	end
-
-	if canSeeSpetsnaz() then
-			agro = true
-		agrotimer = 0
-		KillTimer = KillTimer + dt
-		enemyspotted = true
-		shoot = true
-	end
-
-	--RELOAD
-	if shots > 29 then
-		reloading = true
-		if alive then
-		reload = reload + dt
-		if reload > 4 then
-			reloading = false
-			shots = 0
-			reload = 0
-		end
-	end
-	end
-
-
-	--ELIMINATE TARGET 
-	local barrel = FindShape("barrel")
-	local guntrans = GetShapeWorldTransform(barrel)
-	local terrorist = FindShape("spetsnaz")
-	terrorpos = GetShapeWorldTransform(terrorist)
-	if guntrans.pos[2] < terrorpos.pos[2] then
-		shoot = false
-	end
-    local gunpos = guntrans.pos
-	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
-    local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
-
-    if flaretim then
-    	flaretimer = flaretimer + dt
-    	if flaretimer > 0.05 then
-    		SetLightEnabled(flare, false)
-    		flaretimer = 0
-    	end
-    end
-    if shoot then
-	if KillTimer > Eliminate then
-		if not disarmed then
-		if not reloading then
-		shootim = shootim + dt
-		if shootim > 0.1 then
-		Shoot(shootpos, direction)
-		PlaySound(GunShot, shootpos,10)
-		SetLightEnabled(flare, true)
-		flaretim = true
-		for i=1,33 do
-		GunSmoke()
-	end
-		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
-		shootim = 0
-		shots = shots + 1
-	end
-end
-	end
-end
-end
-
-	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
-	if enemyspotted then
-	if not disarmed then
-	if alive then
-		if agro then
-	local ppos = GetPlayerCameraTransform()
-	ppos.pos[2] = ppos.pos[2] - 0.5
-	spetsnazpos = GetShapeWorldTransform(spetsnaz)
-	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
-	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
-
-
-
-	if canSeeSpetsnaz() then
-	enemy = spetsnazpos.pos
-end
-
-
-
-	local akmpos = GetBodyTransform(akm)
-
-	local aimangle = QuatLookAt(akmpos.pos, enemy)
-
-	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
-	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
-
-
---yaw
- gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
-  --pitch
- gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
-  --roll
- gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
- if agro then
-
- local bias = QuatEuler(gunyaw, gunpitch, gunroll)
-  SetBodyTransform(akm, Transform(akmpos.pos, bias))
-end
-end
-end
-
---b = GetBodyTransform(LLARM)
-  --for i=1,3 do
-        --if(ppos.pos[i]<b.pos[i]) then
-             --biasb[i] = -weightb
-        --elseif(ppos.pos[i]>b.pos[i]) then
-          --  biasb[i] = weightb
-        --else
-          --  biasb[i] = 0
-        --end
-    --end
-    --local currentVelocity = GetBodyVelocity(LLARM)
-    if alive then
-    	if agro then
-    local ppos = enemy
-    local bmi, bma = GetBodyBounds(LLARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(LLARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(LLARM, vel)
-local bmi, bma = GetBodyBounds(RRARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(RRARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(RRARM, vel)
-end
-end
-end
-end
-  --akmpos.rot = Rot
-  --SetBodyTransform(akm, akmpos)
-
---HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
-	if bleed then
-	if IsBodyBroken(Head) then
-
-		for i=1, 9 do
-		 	 thingz = FindJoints("eye")
-		 	 for i=1, #thingz do
-		 	 	thinz = thingz[i]
-		 	 	Delete(thinz)
-		 	 end
-		 end
-
-		for i=1,Bleed/2 do
-		smoke()
-	end
-end
-end
-
-if bleed then
-	
-		if HeadBloodCapacity < MaxBloodCapacity then
-		Bleed = Bleed * 6 
-		for i=1,Bleed/6 do
-		smoke()
-	end
-	end
-
-HeadBloodLevel = HeadBloodLevel - Bleed/2
-end
-
-	if HeadBloodLevel <= 0 then
-		bleed = false
-		HeadBloodLevel = 0
-	end
-
-	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
-
-	if bleed1 then
-	if IsBodyBroken(Torso) then
-		for i=1,Bleed1/regularantibleed do
-		smoke1()
-	end
-end
-end
-
-if bleed1 then
-
-		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
-		Bleed1 = Bleed1 * 6 
-		 for i=1, 9 do
-		 	 things = FindBodies("gut", true)
-		 	 for i=1, #things do
-		 	 	thing = things[i]
-		 	 	SetBodyDynamic(thing, true)
-		 	 end
-		 end
-		for i=1,Bleed1/extremeantibleed do
-		smoke1()
-	end
-	end
-
-TorsoBloodLevel = TorsoBloodLevel - Bleed1
-end
-
-	if TorsoBloodLevel <= 0 then
-		bleed1 = false
-		TorsoBloodLevel = 0
-	end
-
--- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
-
-if bleed2 then
-
-	if LARMBloodCapacity < MaxBloodCapacity2/3 then
-		Bleed2 = Bleed2 * 6 
-		for i=1,Bleed2/extremeantibleed do
-		smoke2()
-	end
-	end
-
-	if IsBodyBroken(LARM) then
-		for i=1,Bleed2/limbantibleed do
-		smoke2()
-	end
-end
-end
-
-if bleed2 then
-LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
-end
-
-	if LARMBloodLevel <= 0 then
-		bleed2 = false
-		LARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-if bleed3 then
-
-	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
-		Bleed3 = Bleed3 * 6 
-		for i=1,Bleed3/extremeantibleed do
-		smoke3()
-	end
-	end
-
-	if IsBodyBroken(LLARM) then
-		for i=1,Bleed3/limbantibleed do
-		smoke3()
-	end
-end
-end
-
-if bleed3 then
-LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
-end
-
-	if LLARMBloodLevel <= 0 then
-		bleed3 = false
-		LLARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed4 then
-
-		if RARMBloodCapacity < MaxBloodCapacity4/3 then
-		Bleed4 = Bleed4 * 6 
-		for i=1,Bleed4/extremeantibleed do
-		smoke4()
-	end
-	end
-
-	if IsBodyBroken(RARM) then
-		for i=1,Bleed4/limbantibleed do
-		smoke4()
-	end
-end
-end
-
-if bleed4 then
-RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
-end
-
-	if RARMBloodLevel <= 0 then
-		bleed4 = false
-		RARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed5 then
-
-		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
-		Bleed5 = Bleed5 * 6 
-		for i=1,Bleed5/extremeantibleed do
-		smoke5()
-	end
-	end
-
-	if IsBodyBroken(RRARM) then
-		for i=1,Bleed5/limbantibleed do
-		smoke5()
-	end
-end
-end
-
-if bleed5 then
-RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
-end
-
-	if RRARMBloodLevel <= 0 then
-		bleed5 = false
-		RRARMBloodLevel = 0
-	end
-
-	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
-
-	if bleed6 then
-
-		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
-		Bleed6 = Bleed6 * 6 
-		for i=1,Bleed6/extremeantibleed do
-		smoke6()
-	end
-	end
-
-	if IsBodyBroken(LLEG) then
-		for i=1,Bleed6/limbantibleed do
-		smoke6()
-	end
-end
-end
-
-if bleed6 then
-LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
-end
-
-	if LLEGBloodLevel <= 0 then
-		bleed6 = false
-	LLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed7 then
-
-		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
-		Bleed7 = Bleed7 * 6 
-		for i=1,Bleed7/extremeantibleed do
-		smoke7()
-	end
-	end
-
-	if IsBodyBroken(LLLEG) then
-		for i=1,Bleed7/limbantibleed do
-		smoke7()
-	end
-end
-end
-
-if bleed7 then
-LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
-end
-
-	if LLLEGBloodLevel <= 0 then
-		bleed7 = false
-	LLLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed8 then
-
-		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
-		Bleed8 = Bleed8 * 6 
-		for i=1,Bleed8/extremeantibleed do
-		smoke8()
-	end
-	end
-
-	if IsBodyBroken(RLEG) then
-		for i=1,Bleed8/limbantibleed do
-		smoke8()
-	end
-end
-end
-
-if bleed8 then
-RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
-end
-
-	if RLEGBloodLevel <= 0 then
-		bleed8 = false
-	RLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed9 then
-
-		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
-		Bleed9 = Bleed9 * 6 
-		for i=1,Bleed9/extremeantibleed do
-		smoke9()
-	end
-	end
-
-	if IsBodyBroken(RRLEG) then
-		for i=1,Bleed9/limbantibleed do
-		smoke9()
-	end
-end
-end
-
-if bleed9 then
-RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
-end
-
-	if RRLEGBloodLevel <= 0 then
-		bleed9 = false
-	RRLEGBloodLevel = 0
-	end
-
-	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
-	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
-
-	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
-		upspeed[2] = TotalLegBloodValue/10000
-
-	currentvel = GetBodyVelocity(Head)
-	currentvel1 = GetBodyVelocity(LLLEG)
-	currentvel2 = GetBodyVelocity(RRLEG)
-
-	if IsBodyBroken(Head) then
-		alive = false
-	end
-
-	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
-		alive = false
-	end
-
-	if TotalBloodValue < MinBloodValue then
-		alive = false
-	end
-	if alive then
-	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
-	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
-	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
-end
-
-a = GetPlayerTransform()
-
-	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
-
-	if distToPlayer < 3 then
-		inrange = true
-	else
-		inrange = false
-	end
-
-
-end
-
-
+#version 2
 function smoke()
     --spawn sparks
     ParticleType("smoke")
@@ -832,151 +165,6 @@
     SpawnParticle(shootpos.pos, Vec(math.random(-5, 5), math.random(-5, 5), math.random(-5, 5)),0.3)
 end
 
-
-function draw()
-if drawtext then
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("Head Blood Level:  "..HeadBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 220)
-      UiFont("bold.ttf", 30)
-      UiText("Torso Blood Level:  "..TorsoBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 240)
-      UiFont("bold.ttf", 30)
-      UiText("upper left arm Blood Level:  "..LARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 260)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 280)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 300)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 320)
-      UiFont("bold.ttf", 30)
-      UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 340)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 360)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 380)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 400)
-      UiFont("bold.ttf", 30)
-      UiText("total Blood Level:  "..TotalBloodValue)
-    UiPop()
-end
-if inrange then
-	if enabled then
-
-
-	
-		UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 300)
-      UiColor(0,0,1)
-      UiFont("bold.ttf", 30)
-      UiText("To disable viewable ragdoll stats, press H ")
-    UiPop()
-
-
-	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 350)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 30)
-      UiText("Total Blood Volume:  "..TotalBloodValue)
-    UiPop()
-
-    if alive then
-    	  UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 60)
-      UiText("ALIVE")
-    UiPop()
-    if TotalBloodValue < 15000 then
-    	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 450)
-      UiColor(1,1,0)
-      UiFont("bold.ttf", 50)
-      UiText("CRITICAL CONDITION")
-    UiPop()
-    end
-end
-if not alive then
-	  UiPush()
-	  UiColor(1,0,0)
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiFont("bold.ttf", 60)
-      UiText("DECEASED")
-    UiPop()
-end
-end
-end
-end
---function canSeePlayer()
-    --local camTrans = GetPlayerCameraTransform()
-	--local playerPos = camTrans.pos
-
-	--Direction to player
-	--local dir = VecSub(playerPos, shootPos)
-	--local dist = VecLength(dir)
-	--dir = VecNormalize(dir)
-
-	--QueryRejectVehicle(GetPlayerVehicle())
-	--return not QueryRaycast(shootPos, dir, dist, 0, true)
---end
-
 function canSeeSpetsnaz()
     local camTrans = GetShapeWorldTransform(spetsnaz)
     camTrans.pos[2] = camTrans.pos[2]
@@ -987,6 +175,718 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	return not QueryRaycast(shootPos, dir, dist, 0, true)
-end+end
+
+function server.init()
+    Head = FindBody("Head")
+    HeadBloodCapacity = GetBodyMass(Head)
+    HeadBloodLevel = HeadBloodCapacity * 20
+    StartingBleed = HeadBloodCapacity
+    MaxBloodCapacity = GetBodyMass(Head)
+    bleed = true
+    Torso = FindBody("Torso")
+    TorsoBloodCapacity = GetBodyMass(Torso)
+    TorsoBloodLevel = TorsoBloodCapacity * 20
+    StartingBleed1 = TorsoBloodCapacity
+    MaxBloodCapacity1 = GetBodyMass(Torso)
+    bleed1 = true
+    LARM = FindBody("LARM")
+    LARMBloodCapacity = GetBodyMass(LARM)
+    LARMBloodLevel = LARMBloodCapacity * 20
+    StartingBleed2 = LARMBloodCapacity
+    MaxBloodCapacity2 = GetBodyMass(LARM)
+    bleed2 = true
+    LLARM = FindBody("LLARM")
+    LLARMBloodCapacity = GetBodyMass(LLARM)
+    LLARMBloodLevel = LLARMBloodCapacity * 20
+    StartingBleed3 = LLARMBloodCapacity
+    MaxBloodCapacity3 = GetBodyMass(LLARM)
+    bleed3 = true
+    RARM = FindBody("RARM")
+    RARMBloodCapacity = GetBodyMass(RARM)
+    RARMBloodLevel = RARMBloodCapacity * 20
+    StartingBleed4 = RARMBloodCapacity
+    MaxBloodCapacity4 = GetBodyMass(RARM)
+    bleed4 = true
+    RRARM = FindBody("RRARM")
+    RRARMBloodCapacity = GetBodyMass(RRARM)
+    RRARMBloodLevel = RRARMBloodCapacity * 20
+    StartingBleed5 = RRARMBloodCapacity
+    MaxBloodCapacity5 = GetBodyMass(RRARM)
+    bleed5 = true
+    LLEG = FindBody("LLEG")
+    LLEGBloodCapacity = GetBodyMass(LLEG)
+    LLEGBloodLevel = LLEGBloodCapacity * 20
+    StartingBleed6 = LLEGBloodCapacity
+    MaxBloodCapacity6 = GetBodyMass(LLEG)
+    bleed6 = true
+    LLLEG = FindBody("LLLEG")
+    LLLEGBloodCapacity = GetBodyMass(LLLEG)
+    LLLEGBloodLevel = LLLEGBloodCapacity * 20
+    StartingBleed7 = LLLEGBloodCapacity
+    MaxBloodCapacity7 = GetBodyMass(LLLEG)
+    bleed7 = true
+    RLEG = FindBody("RLEG")
+    RLEGBloodCapacity = GetBodyMass(RLEG)
+    RLEGBloodLevel = RLEGBloodCapacity * 20
+    StartingBleed8 = RLEGBloodCapacity
+    MaxBloodCapacity8 = GetBodyMass(RLEG)
+    bleed8 = true
+    RRLEG = FindBody("RRLEG")
+    RRLEGBloodCapacity = GetBodyMass(RRLEG)
+    RRLEGBloodLevel = RRLEGBloodCapacity * 20
+    StartingBleed9 = RRLEGBloodCapacity
+    MaxBloodCapacity9 = GetBodyMass(RRLEG)
+    bleed9 = true
+    antibleed = 15 -- only affects smoke speed
+    extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
+    regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
+    limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
+    MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
+    LimbBleedSpeed = 0.1
+    bloodgrav = -20
+    blooddrag = 0
+    startupspeed = Vec(0,0.7,0)
+    upspeed = Vec(0,2,0)
+    downspeed = Vec(0,-1,0)
+    alive = true
+    akm = FindBody("AKM")
+    weight = 2
+    bias = Vec(0,0,0)
+    biasb = Vec(0,0,0)
+    weightb = -0.4
+    agrotimer = 0
+    forget = 10
+    KillTimer = 0
+    Eliminate = 1
+    shootim = 0
+    shots = 0
+    reload = 0
+    recoil = 2
+    flare = FindLight("flare")
+    flaretim = false
+    flaretimer = 0
+    SetLightEnabled(flare, false)
+    disarmed = false
+    spetsnaz = FindShape("terrorist",true)
+    enemyspotted = false
+    enabled = true
+    disabled = false
+    switched = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        end
+        	if IsShapeBroken(spetsnaz) then
+        		RemoveTag(spetsnaz,"terrorist")
+        		agro = false
+        		agrotimer = 0
+        		spetsnaz = FindShape("terrorist",true)
+        		enemyspotted = false
+        		shoot = false
+        	end
+        	if PlayerHP == 0 then
+        		shoot = false
+        		agro = false
+        		agrotimer = 0
+        		enemyspotted = false
+        	end
+        	gunTrans = GetBodyTransform(Head)
+        	gunPos = gunTrans.pos
+        	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
+        	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
+        	drawtext = false
+        	HeadBloodCapacity = GetBodyMass(Head)
+        	Bleed = StartingBleed - HeadBloodCapacity
+        	HeadPos = GetBodyTransform(Head)
+        	TorsoBloodCapacity = GetBodyMass(Torso)
+        	Bleed1 = StartingBleed1 - TorsoBloodCapacity
+        	TorsoPos = GetBodyTransform(Torso)
+        	LARMBloodCapacity = GetBodyMass(LARM)
+        	Bleed2 = StartingBleed2 - LARMBloodCapacity
+        	LARMPos = GetBodyTransform(LARM)
+        	LLARMBloodCapacity = GetBodyMass(LLARM)
+        	Bleed3 = StartingBleed3 - LLARMBloodCapacity
+        	LLARMPos = GetBodyTransform(LLARM)
+        	RARMBloodCapacity = GetBodyMass(RARM)
+        	Bleed4 = StartingBleed4 - RARMBloodCapacity
+        	RARMPos = GetBodyTransform(RARM)
+        	RRARMBloodCapacity = GetBodyMass(RRARM)
+        	Bleed5 = StartingBleed5 - RRARMBloodCapacity
+        	RRARMPos = GetBodyTransform(RRARM)
+        	LLEGBloodCapacity = GetBodyMass(LLEG)
+        	Bleed6 = StartingBleed6 - LLEGBloodCapacity
+        	LLEGPos = GetBodyTransform(LLEG)
+        	LLLEGBloodCapacity = GetBodyMass(LLLEG)
+        	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
+        	LLLEGPos = GetBodyTransform(LLLEG)
+        	RLEGBloodCapacity = GetBodyMass(RLEG)
+        	Bleed8 = StartingBleed8 - RLEGBloodCapacity
+        	RLEGPos = GetBodyTransform(RLEG)
+        	RRLEGBloodCapacity = GetBodyMass(RRLEG)
+        	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
+        	RRLEGPos = GetBodyTransform(RRLEG)
+        	--AGRESSIVE BEHAVIOR
+        	if IsBodyBroken(LLARM) then
+        		disarmed = true
+        	end
+        	if canSeeSpetsnaz() then
+        			agro = true
+        		agrotimer = 0
+        		KillTimer = KillTimer + dt
+        		enemyspotted = true
+        		shoot = true
+        	end
+        	--RELOAD
+        	if shots > 29 then
+        		reloading = true
+        		if alive then
+        		reload = reload + dt
+        		if reload > 4 then
+        			reloading = false
+        			shots = 0
+        			reload = 0
+        		end
+        	end
+        	end
+        	--ELIMINATE TARGET 
+        	local barrel = FindShape("barrel")
+        	local guntrans = GetShapeWorldTransform(barrel)
+        	local terrorist = FindShape("spetsnaz")
+        	terrorpos = GetShapeWorldTransform(terrorist)
+        	if guntrans.pos[2] < terrorpos.pos[2] then
+        		shoot = false
+        	end
+            local gunpos = guntrans.pos
+        	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
+            local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
+            if flaretim then
+            	flaretimer = flaretimer + dt
+            	if flaretimer > 0.05 then
+            		SetLightEnabled(flare, false)
+            		flaretimer = 0
+            	end
+            end
+        	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
+        	if enemyspotted then
+        	if not disarmed then
+        	if alive then
+        		if agro then
+        	local ppos = GetPlayerCameraTransform(playerId)
+        	ppos.pos[2] = ppos.pos[2] - 0.5
+        	spetsnazpos = GetShapeWorldTransform(spetsnaz)
+        	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
+        	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
+
+        	if canSeeSpetsnaz() then
+        	enemy = spetsnazpos.pos
+        end
+
+        	local akmpos = GetBodyTransform(akm)
+
+        	local aimangle = QuatLookAt(akmpos.pos, enemy)
+
+        	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
+        	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
+
+        --yaw
+         gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
+          --pitch
+         gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
+          --roll
+         gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
+         if agro then
+
+         local bias = QuatEuler(gunyaw, gunpitch, gunroll)
+          SetBodyTransform(akm, Transform(akmpos.pos, bias))
+        end
+        end
+        end
+
+        --b = GetBodyTransform(LLARM)
+          --for i=1,3 do
+                --if(ppos.pos[i]<b.pos[i]) then
+                     --biasb[i] = -weightb
+                --elseif(ppos.pos[i]>b.pos[i]) then
+                  --  biasb[i] = weightb
+                --else
+                  --  biasb[i] = 0
+                --end
+            --end
+            --local currentVelocity = GetBodyVelocity(LLARM)
+            if alive then
+            	if agro then
+            local ppos = enemy
+            local bmi, bma = GetBodyBounds(LLARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(LLARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(LLARM, vel)
+        local bmi, bma = GetBodyBounds(RRARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(RRARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(RRARM, vel)
+        end
+        end
+        end
+        end
+          --akmpos.rot = Rot
+          --SetBodyTransform(akm, akmpos)
+        --HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
+        	if bleed then
+        	if IsBodyBroken(Head) then
+
+        		for i=1, 9 do
+        		 	 thingz = FindJoints("eye")
+        		 	 for i=1, #thingz do
+        		 	 	thinz = thingz[i]
+        		 	 	Delete(thinz)
+        		 	 end
+        		 end
+
+        		for i=1,Bleed/2 do
+        		smoke()
+        	end
+        end
+        end
+        if bleed then
+
+        		if HeadBloodCapacity < MaxBloodCapacity then
+        		Bleed = Bleed * 6 
+        		for i=1,Bleed/6 do
+        		smoke()
+        	end
+        	end
+
+        HeadBloodLevel = HeadBloodLevel - Bleed/2
+        end
+        	if HeadBloodLevel <= 0 then
+        		bleed = false
+        		HeadBloodLevel = 0
+        	end
+        	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
+        	if bleed1 then
+        	if IsBodyBroken(Torso) then
+        		for i=1,Bleed1/regularantibleed do
+        		smoke1()
+        	end
+        end
+        end
+        if bleed1 then
+
+        		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
+        		Bleed1 = Bleed1 * 6 
+        		 for i=1, 9 do
+        		 	 things = FindBodies("gut", true)
+        		 	 for i=1, #things do
+        		 	 	thing = things[i]
+        		 	 	SetBodyDynamic(thing, true)
+        		 	 end
+        		 end
+        		for i=1,Bleed1/extremeantibleed do
+        		smoke1()
+        	end
+        	end
+
+        TorsoBloodLevel = TorsoBloodLevel - Bleed1
+        end
+        	if TorsoBloodLevel <= 0 then
+        		bleed1 = false
+        		TorsoBloodLevel = 0
+        	end
+        -- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
+        if bleed2 then
+
+        	if LARMBloodCapacity < MaxBloodCapacity2/3 then
+        		Bleed2 = Bleed2 * 6 
+        		for i=1,Bleed2/extremeantibleed do
+        		smoke2()
+        	end
+        	end
+
+        	if IsBodyBroken(LARM) then
+        		for i=1,Bleed2/limbantibleed do
+        		smoke2()
+        	end
+        end
+        end
+        if bleed2 then
+        LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
+        end
+        	if LARMBloodLevel <= 0 then
+        		bleed2 = false
+        		LARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        if bleed3 then
+
+        	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
+        		Bleed3 = Bleed3 * 6 
+        		for i=1,Bleed3/extremeantibleed do
+        		smoke3()
+        	end
+        	end
+
+        	if IsBodyBroken(LLARM) then
+        		for i=1,Bleed3/limbantibleed do
+        		smoke3()
+        	end
+        end
+        end
+        if bleed3 then
+        LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
+        end
+        	if LLARMBloodLevel <= 0 then
+        		bleed3 = false
+        		LLARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed4 then
+
+        		if RARMBloodCapacity < MaxBloodCapacity4/3 then
+        		Bleed4 = Bleed4 * 6 
+        		for i=1,Bleed4/extremeantibleed do
+        		smoke4()
+        	end
+        	end
+
+        	if IsBodyBroken(RARM) then
+        		for i=1,Bleed4/limbantibleed do
+        		smoke4()
+        	end
+        end
+        end
+        if bleed4 then
+        RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
+        end
+        	if RARMBloodLevel <= 0 then
+        		bleed4 = false
+        		RARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed5 then
+
+        		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
+        		Bleed5 = Bleed5 * 6 
+        		for i=1,Bleed5/extremeantibleed do
+        		smoke5()
+        	end
+        	end
+
+        	if IsBodyBroken(RRARM) then
+        		for i=1,Bleed5/limbantibleed do
+        		smoke5()
+        	end
+        end
+        end
+        if bleed5 then
+        RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
+        end
+        	if RRARMBloodLevel <= 0 then
+        		bleed5 = false
+        		RRARMBloodLevel = 0
+        	end
+        	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
+        	if bleed6 then
+
+        		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
+        		Bleed6 = Bleed6 * 6 
+        		for i=1,Bleed6/extremeantibleed do
+        		smoke6()
+        	end
+        	end
+
+        	if IsBodyBroken(LLEG) then
+        		for i=1,Bleed6/limbantibleed do
+        		smoke6()
+        	end
+        end
+        end
+        if bleed6 then
+        LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
+        end
+        	if LLEGBloodLevel <= 0 then
+        		bleed6 = false
+        	LLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed7 then
+
+        		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
+        		Bleed7 = Bleed7 * 6 
+        		for i=1,Bleed7/extremeantibleed do
+        		smoke7()
+        	end
+        	end
+
+        	if IsBodyBroken(LLLEG) then
+        		for i=1,Bleed7/limbantibleed do
+        		smoke7()
+        	end
+        end
+        end
+        if bleed7 then
+        LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
+        end
+        	if LLLEGBloodLevel <= 0 then
+        		bleed7 = false
+        	LLLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed8 then
+
+        		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
+        		Bleed8 = Bleed8 * 6 
+        		for i=1,Bleed8/extremeantibleed do
+        		smoke8()
+        	end
+        	end
+
+        	if IsBodyBroken(RLEG) then
+        		for i=1,Bleed8/limbantibleed do
+        		smoke8()
+        	end
+        end
+        end
+        if bleed8 then
+        RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
+        end
+        	if RLEGBloodLevel <= 0 then
+        		bleed8 = false
+        	RLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed9 then
+
+        		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
+        		Bleed9 = Bleed9 * 6 
+        		for i=1,Bleed9/extremeantibleed do
+        		smoke9()
+        	end
+        	end
+
+        	if IsBodyBroken(RRLEG) then
+        		for i=1,Bleed9/limbantibleed do
+        		smoke9()
+        	end
+        end
+        end
+        if bleed9 then
+        RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
+        end
+        	if RRLEGBloodLevel <= 0 then
+        		bleed9 = false
+        	RRLEGBloodLevel = 0
+        	end
+        	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
+        	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
+        	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
+        		upspeed[2] = TotalLegBloodValue/10000
+        	currentvel = GetBodyVelocity(Head)
+        	currentvel1 = GetBodyVelocity(LLLEG)
+        	currentvel2 = GetBodyVelocity(RRLEG)
+        	if IsBodyBroken(Head) then
+        		alive = false
+        	end
+        	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
+        		alive = false
+        	end
+        	if TotalBloodValue < MinBloodValue then
+        		alive = false
+        	end
+        	if alive then
+        	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
+        	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
+        	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
+        end
+        a = GetPlayerTransform(playerId)
+        	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
+        	if distToPlayer < 3 then
+        		inrange = true
+        	else
+        		inrange = false
+        	end
+    end
+end
+
+function client.init()
+    GunShot = LoadSound("MOD/gorescript/m4.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    		if InputPressed("H") then
+    		if switched then
+    			enabled = false
+    			switched = false
+    		else if not switched then
+    			enabled = true
+    		switched = true
+    		end
+    	end
+        if shoot then
+    	if KillTimer > Eliminate then
+    		if not disarmed then
+    		if not reloading then
+    		shootim = shootim + dt
+    		if shootim > 0.1 then
+    		Shoot(shootpos, direction)
+    		PlaySound(GunShot, shootpos,10)
+    		SetLightEnabled(flare, true)
+    		flaretim = true
+    		for i=1,33 do
+    		GunSmoke()
+    	end
+    		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
+    		shootim = 0
+    		shots = shots + 1
+    	end
+    end
+    	end
+    end
+    end
+end
+
+function client.draw()
+    if drawtext then
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("Head Blood Level:  "..HeadBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 220)
+          UiFont("bold.ttf", 30)
+          UiText("Torso Blood Level:  "..TorsoBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 240)
+          UiFont("bold.ttf", 30)
+          UiText("upper left arm Blood Level:  "..LARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 260)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 280)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 300)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 320)
+          UiFont("bold.ttf", 30)
+          UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 340)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 360)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 380)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 400)
+          UiFont("bold.ttf", 30)
+          UiText("total Blood Level:  "..TotalBloodValue)
+        UiPop()
+    end
+    if inrange then
+    	if enabled then
+
+    		UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 300)
+          UiColor(0,0,1)
+          UiFont("bold.ttf", 30)
+          UiText("To disable viewable ragdoll stats, press H ")
+        UiPop()
+
+    	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 350)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 30)
+          UiText("Total Blood Volume:  "..TotalBloodValue)
+        UiPop()
+
+        if alive then
+        	  UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 60)
+          UiText("ALIVE")
+        UiPop()
+        if TotalBloodValue < 15000 then
+        	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 450)
+          UiColor(1,1,0)
+          UiFont("bold.ttf", 50)
+          UiText("CRITICAL CONDITION")
+        UiPop()
+        end
+    end
+    if not alive then
+    	  UiPush()
+    	  UiColor(1,0,0)
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiFont("bold.ttf", 60)
+          UiText("DECEASED")
+        UiPop()
+    end
+    end
+    end
+end
+

```

---

# Migration Report: gorescript\goreterrorist.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/gorescript\goreterrorist.lua
+++ patched/gorescript\goreterrorist.lua
@@ -1,700 +1,4 @@
-function init()
-	Head = FindBody("Head")
-	HeadBloodCapacity = GetBodyMass(Head)
-	HeadBloodLevel = HeadBloodCapacity * 20
-	StartingBleed = HeadBloodCapacity
-	MaxBloodCapacity = GetBodyMass(Head)
-	bleed = true
-
-	Torso = FindBody("Torso")
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	TorsoBloodLevel = TorsoBloodCapacity * 20
-	StartingBleed1 = TorsoBloodCapacity
-	MaxBloodCapacity1 = GetBodyMass(Torso)
-	bleed1 = true
-
-	LARM = FindBody("LARM")
-	LARMBloodCapacity = GetBodyMass(LARM)
-	LARMBloodLevel = LARMBloodCapacity * 20
-	StartingBleed2 = LARMBloodCapacity
-	MaxBloodCapacity2 = GetBodyMass(LARM)
-
-	bleed2 = true
-
-	LLARM = FindBody("LLARM")
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	LLARMBloodLevel = LLARMBloodCapacity * 20
-	StartingBleed3 = LLARMBloodCapacity
-	MaxBloodCapacity3 = GetBodyMass(LLARM)
-	bleed3 = true
-
-	RARM = FindBody("RARM")
-	RARMBloodCapacity = GetBodyMass(RARM)
-	RARMBloodLevel = RARMBloodCapacity * 20
-	StartingBleed4 = RARMBloodCapacity
-	MaxBloodCapacity4 = GetBodyMass(RARM)
-	bleed4 = true
-
-	RRARM = FindBody("RRARM")
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	RRARMBloodLevel = RRARMBloodCapacity * 20
-	StartingBleed5 = RRARMBloodCapacity
-	MaxBloodCapacity5 = GetBodyMass(RRARM)
-	bleed5 = true
-
-	LLEG = FindBody("LLEG")
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	LLEGBloodLevel = LLEGBloodCapacity * 20
-	StartingBleed6 = LLEGBloodCapacity
-	MaxBloodCapacity6 = GetBodyMass(LLEG)
-	bleed6 = true
-
-	LLLEG = FindBody("LLLEG")
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	LLLEGBloodLevel = LLLEGBloodCapacity * 20
-	StartingBleed7 = LLLEGBloodCapacity
-	MaxBloodCapacity7 = GetBodyMass(LLLEG)
-	bleed7 = true
-
-	RLEG = FindBody("RLEG")
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	RLEGBloodLevel = RLEGBloodCapacity * 20
-	StartingBleed8 = RLEGBloodCapacity
-	MaxBloodCapacity8 = GetBodyMass(RLEG)
-	bleed8 = true
-
-	RRLEG = FindBody("RRLEG")
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	RRLEGBloodLevel = RRLEGBloodCapacity * 20
-	StartingBleed9 = RRLEGBloodCapacity
-	MaxBloodCapacity9 = GetBodyMass(RRLEG)
-	bleed9 = true
-
-	antibleed = 15 -- only affects smoke speed
-	extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
-	regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
-	limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
-	MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
-
-	LimbBleedSpeed = 0.1
-
-	bloodgrav = -20
-	blooddrag = 0
-	startupspeed = Vec(0,0.7,0)
-	upspeed = Vec(0,0.7,0)
-	downspeed = Vec(0,-0.7,0)
-	alive = true
-
-	akm = FindBody("AKM")
-	weight = 500
-	bias = Vec(0,0,0)
-	biasb = Vec(0,0,0)
-	weightb = -0.6
-	agrotimer = 0
-	forget = 10
-	KillTimer = 0
-	Eliminate = 1
-	shootim = 0
-	shots = 0
-	reload = 0
-	recoil = 40
-
-	flare = FindLight("flare")
-	flaretim = false
-	flaretimer = 0
-	SetLightEnabled(flare, false)
-	disarmed = false
-	spetsnaz = FindShape("spetsnaz",true)
-	GunShot = LoadSound("MOD/gorescript/akm.ogg")
-	enemyspotted = false
-		switched = true
-		enabled = true
-end
-
-
-function tick(dt)
-
-	if InputPressed("H") then
-		if switched then
-			enabled = false
-			switched = false
-		else if not switched then
-			enabled = true
-		switched = true
-		end
-	end
-end
-
-	if IsShapeBroken(spetsnaz) then
-		RemoveTag(spetsnaz,"spetsnaz")
-		agro = false
-		agrotimer = 0
-		spetsnaz = FindShape("spetsnaz",true)
-		enemyspotted = false
-		shoot = false
-	end
-
-	if PlayerHP == 0 then
-		shoot = false
-		agro = false
-		agrotimer = 0
-		enemyspotted = false
-	end
-	gunTrans = GetBodyTransform(Head)
-	gunPos = gunTrans.pos
-	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
-	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
-
-	drawtext = false
-
-	HeadBloodCapacity = GetBodyMass(Head)
-	Bleed = StartingBleed - HeadBloodCapacity
-	HeadPos = GetBodyTransform(Head)
-
-	TorsoBloodCapacity = GetBodyMass(Torso)
-	Bleed1 = StartingBleed1 - TorsoBloodCapacity
-	TorsoPos = GetBodyTransform(Torso)
-
-	LARMBloodCapacity = GetBodyMass(LARM)
-	Bleed2 = StartingBleed2 - LARMBloodCapacity
-	LARMPos = GetBodyTransform(LARM)
-
-	LLARMBloodCapacity = GetBodyMass(LLARM)
-	Bleed3 = StartingBleed3 - LLARMBloodCapacity
-	LLARMPos = GetBodyTransform(LLARM)
-
-	RARMBloodCapacity = GetBodyMass(RARM)
-	Bleed4 = StartingBleed4 - RARMBloodCapacity
-	RARMPos = GetBodyTransform(RARM)
-
-	RRARMBloodCapacity = GetBodyMass(RRARM)
-	Bleed5 = StartingBleed5 - RRARMBloodCapacity
-	RRARMPos = GetBodyTransform(RRARM)
-
-	LLEGBloodCapacity = GetBodyMass(LLEG)
-	Bleed6 = StartingBleed6 - LLEGBloodCapacity
-	LLEGPos = GetBodyTransform(LLEG)
-
-	LLLEGBloodCapacity = GetBodyMass(LLLEG)
-	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
-	LLLEGPos = GetBodyTransform(LLLEG)
-
-	RLEGBloodCapacity = GetBodyMass(RLEG)
-	Bleed8 = StartingBleed8 - RLEGBloodCapacity
-	RLEGPos = GetBodyTransform(RLEG)
-
-	RRLEGBloodCapacity = GetBodyMass(RRLEG)
-	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
-	RRLEGPos = GetBodyTransform(RRLEG)
-
-	--AGRESSIVE BEHAVIOR
-
-	if IsBodyBroken(LLARM) then
-		disarmed = true
-	end
-
-	if canSeeSpetsnaz() then
-			agro = true
-		agrotimer = 0
-		KillTimer = KillTimer + dt
-		enemyspotted = true
-		shoot = true
-
-	end
-
-	if canSeePlayer() then
-		agro = true
-		agrotimer = 0
-		KillTimer = KillTimer + dt
-		enemyspotted = true
-		shoot = true
-		end
-		if agro then
-			agrotimer = agrotimer + dt
-		if agrotimer > forget then
-		agro = false
-		agrotimer = 0
-		KillTimer = 0
-	end
-end
-
-	--RELOAD
-	if shots > 29 then
-		reloading = true
-		if alive then
-		reload = reload + dt
-		if reload > 4 then
-			reloading = false
-			shots = 0
-			reload = 0
-		end
-	end
-	end
-
-
-	--ELIMINATE TARGET 
-	local barrel = FindShape("barrel")
-	local guntrans = GetShapeWorldTransform(barrel)
-	local terrorist = FindShape("terrorist")
-	terrorpos = GetShapeWorldTransform(terrorist)
-	--DebugPrint("guny:  "..guntrans.pos[2])
-	--DebugPrint("body:  "..terrorpos.pos[2])
-	if guntrans.pos[2] < terrorpos.pos[2] then
-		shoot = false
-	end
-    local gunpos = guntrans.pos
-	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
-    local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
-
-    if flaretim then
-    	flaretimer = flaretimer + dt
-    	if flaretimer > 0.1 then
-    		SetLightEnabled(flare, false)
-    		flaretimer = 0
-    	end
-    end
-    if shoot then
-	if KillTimer > Eliminate then
-		if not disarmed then
-		if not reloading then
-			if not alive then
-				dt = dt * 4
-			end
-		shootim = shootim + dt
-		if shootim > 0.2 then
-		Shoot(shootpos, direction)
-		PlaySound(GunShot, shootpos,10)
-		SetLightEnabled(flare, true)
-		flaretim = true
-		for i=1,33 do
-		GunSmoke()
-	end
-		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
-		shootim = 0
-		shots = shots + 1
-	end
-end
-	end
-end
-end
-
-	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
-	if enemyspotted then
-	if not disarmed then
-	if alive then
-		if agro then
-	local ppos = GetPlayerCameraTransform()
-	ppos.pos[2] = ppos.pos[2] - 0.5
-	spetsnazpos = GetShapeWorldTransform(spetsnaz)
-	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
-	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
-
-
-
-	if distToPlayeraim > distToSpetsaim and canSeeSpetsnaz() then
-	enemy = spetsnazpos.pos
-else if distToPlayeraim > distToSpetsaim and not canSeeSpetsnaz() then
-	enemy = ppos.pos
-end
-end
-	if distToPlayeraim < distToSpetsaim and canSeePlayer() then
-	enemy = ppos.pos
-else if distToPlayeraim < distToSpetsaim and not canSeePlayer() then
-	enemy = spetsnazpos.pos
-end
-	end
-
-
-
-	local akmpos = GetBodyTransform(akm)
-
-	local aimangle = QuatLookAt(akmpos.pos, enemy)
-
-	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
-	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
-
-
---yaw
- gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
-  --pitch
- gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
-  --roll
- gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
- if agro then
-
- local bias = QuatEuler(gunyaw, gunpitch, gunroll)
-  SetBodyTransform(akm, Transform(akmpos.pos, bias))
-end
-end
-end
-
---b = GetBodyTransform(LLARM)
-  --for i=1,3 do
-        --if(ppos.pos[i]<b.pos[i]) then
-             --biasb[i] = -weightb
-        --elseif(ppos.pos[i]>b.pos[i]) then
-          --  biasb[i] = weightb
-        --else
-          --  biasb[i] = 0
-        --end
-    --end
-    --local currentVelocity = GetBodyVelocity(LLARM)
-    if alive then
-    	if agro then
-    local ppos = enemy
-    local bmi, bma = GetBodyBounds(LLARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(LLARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(LLARM, vel)
-local bmi, bma = GetBodyBounds(RRARM)
-		local bc = VecLerp(bmi, bma, 0.5)
-		local ppos = enemy
-		local dir = VecSub(bc, ppos)
-		local dist = VecLength(dir)
-		dir = VecScale(dir, 1.0/dist)
-    local add = VecScale(dir, weightb)
-	local vel = GetBodyVelocity(RRARM)
-	vel = VecAdd(vel, add)
-    SetBodyVelocity(RRARM, vel)
-end
-end
-end
-end
-  --akmpos.rot = Rot
-  --SetBodyTransform(akm, akmpos)
-
---HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
-	if bleed then
-	if IsBodyBroken(Head) then
-
-		for i=1, 9 do
-		 	 thingz = FindJoints("eye")
-		 	 for i=1, #thingz do
-		 	 	thinz = thingz[i]
-		 	 	Delete(thinz)
-		 	 end
-		 end
-
-		for i=1,Bleed/2 do
-		smoke()
-	end
-end
-end
-
-if bleed then
-	
-		if HeadBloodCapacity < MaxBloodCapacity then
-		Bleed = Bleed * 6 
-		for i=1,Bleed/6 do
-		smoke()
-	end
-	end
-
-HeadBloodLevel = HeadBloodLevel - Bleed/2
-end
-
-	if HeadBloodLevel <= 0 then
-		bleed = false
-		HeadBloodLevel = 0
-	end
-
-	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
-
-	if bleed1 then
-	if IsBodyBroken(Torso) then
-		for i=1,Bleed1/regularantibleed do
-		smoke1()
-	end
-end
-end
-
-if bleed1 then
-
-		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
-		Bleed1 = Bleed1 * 6 
-		 for i=1, 9 do
-		 	 things = FindBodies("gut", true)
-		 	 for i=1, #things do
-		 	 	thing = things[i]
-		 	 	SetBodyDynamic(thing, true)
-		 	 end
-		 end
-		for i=1,Bleed1/extremeantibleed do
-		smoke1()
-	end
-	end
-
-TorsoBloodLevel = TorsoBloodLevel - Bleed1
-end
-
-	if TorsoBloodLevel <= 0 then
-		bleed1 = false
-		TorsoBloodLevel = 0
-	end
-
--- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
-
-if bleed2 then
-
-	if LARMBloodCapacity < MaxBloodCapacity2/3 then
-		Bleed2 = Bleed2 * 6 
-		for i=1,Bleed2/extremeantibleed do
-		smoke2()
-	end
-	end
-
-	if IsBodyBroken(LARM) then
-		for i=1,Bleed2/limbantibleed do
-		smoke2()
-	end
-end
-end
-
-if bleed2 then
-LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
-end
-
-	if LARMBloodLevel <= 0 then
-		bleed2 = false
-		LARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-if bleed3 then
-
-	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
-		Bleed3 = Bleed3 * 6 
-		for i=1,Bleed3/extremeantibleed do
-		smoke3()
-	end
-	end
-
-	if IsBodyBroken(LLARM) then
-		for i=1,Bleed3/limbantibleed do
-		smoke3()
-	end
-end
-end
-
-if bleed3 then
-LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
-end
-
-	if LLARMBloodLevel <= 0 then
-		bleed3 = false
-		LLARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed4 then
-
-		if RARMBloodCapacity < MaxBloodCapacity4/3 then
-		Bleed4 = Bleed4 * 6 
-		for i=1,Bleed4/extremeantibleed do
-		smoke4()
-	end
-	end
-
-	if IsBodyBroken(RARM) then
-		for i=1,Bleed4/limbantibleed do
-		smoke4()
-	end
-end
-end
-
-if bleed4 then
-RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
-end
-
-	if RARMBloodLevel <= 0 then
-		bleed4 = false
-		RARMBloodLevel = 0
-	end
-
-	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
-
-	if bleed5 then
-
-		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
-		Bleed5 = Bleed5 * 6 
-		for i=1,Bleed5/extremeantibleed do
-		smoke5()
-	end
-	end
-
-	if IsBodyBroken(RRARM) then
-		for i=1,Bleed5/limbantibleed do
-		smoke5()
-	end
-end
-end
-
-if bleed5 then
-RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
-end
-
-	if RRARMBloodLevel <= 0 then
-		bleed5 = false
-		RRARMBloodLevel = 0
-	end
-
-	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
-
-	if bleed6 then
-
-		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
-		Bleed6 = Bleed6 * 6 
-		for i=1,Bleed6/extremeantibleed do
-		smoke6()
-	end
-	end
-
-	if IsBodyBroken(LLEG) then
-		for i=1,Bleed6/limbantibleed do
-		smoke6()
-	end
-end
-end
-
-if bleed6 then
-LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
-end
-
-	if LLEGBloodLevel <= 0 then
-		bleed6 = false
-	LLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed7 then
-
-		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
-		Bleed7 = Bleed7 * 6 
-		for i=1,Bleed7/extremeantibleed do
-		smoke7()
-	end
-	end
-
-	if IsBodyBroken(LLLEG) then
-		for i=1,Bleed7/limbantibleed do
-		smoke7()
-	end
-end
-end
-
-if bleed7 then
-LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
-end
-
-	if LLLEGBloodLevel <= 0 then
-		bleed7 = false
-	LLLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed8 then
-
-		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
-		Bleed8 = Bleed8 * 6 
-		for i=1,Bleed8/extremeantibleed do
-		smoke8()
-	end
-	end
-
-	if IsBodyBroken(RLEG) then
-		for i=1,Bleed8/limbantibleed do
-		smoke8()
-	end
-end
-end
-
-if bleed8 then
-RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
-end
-
-	if RLEGBloodLevel <= 0 then
-		bleed8 = false
-	RLEGBloodLevel = 0
-	end
-
-	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
-
-	if bleed9 then
-
-		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
-		Bleed9 = Bleed9 * 6 
-		for i=1,Bleed9/extremeantibleed do
-		smoke9()
-	end
-	end
-
-	if IsBodyBroken(RRLEG) then
-		for i=1,Bleed9/limbantibleed do
-		smoke9()
-	end
-end
-end
-
-if bleed9 then
-RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
-end
-
-	if RRLEGBloodLevel <= 0 then
-		bleed9 = false
-	RRLEGBloodLevel = 0
-	end
-
-	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
-	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
-
-	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
-		upspeed[2] = TotalLegBloodValue/10000
-
-	currentvel = GetBodyVelocity(Head)
-	currentvel1 = GetBodyVelocity(LLLEG)
-	currentvel2 = GetBodyVelocity(RRLEG)
-
-	if IsBodyBroken(Head) then
-		alive = false
-	end
-
-	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
-		alive = false
-	end
-
-	if TotalBloodValue < MinBloodValue then
-		alive = false
-	end
-	if alive then
-	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
-	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
-	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
-end
-
-a = GetPlayerTransform()
-
-	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
-
-	if distToPlayer < 3 then
-		inrange = true
-	else
-		inrange = false
-	end
-
-
-end
-
-
+#version 2
 function smoke()
     --spawn sparks
     ParticleType("smoke")
@@ -861,138 +165,8 @@
     SpawnParticle(shootpos.pos, Vec(math.random(-5, 5), math.random(-5, 5), math.random(-5, 5)),0.3)
 end
 
-
-function draw()
-if drawtext then
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("Head Blood Level:  "..HeadBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 220)
-      UiFont("bold.ttf", 30)
-      UiText("Torso Blood Level:  "..TorsoBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 240)
-      UiFont("bold.ttf", 30)
-      UiText("upper left arm Blood Level:  "..LARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 260)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 280)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 300)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 320)
-      UiFont("bold.ttf", 30)
-      UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 340)
-      UiFont("bold.ttf", 30)
-      UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 360)
-      UiFont("bold.ttf", 30)
-      UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
-    UiPop()
-
-     UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 380)
-      UiFont("bold.ttf", 30)
-      UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
-    UiPop()
-
-    UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 400)
-      UiFont("bold.ttf", 30)
-      UiText("total Blood Level:  "..TotalBloodValue)
-    UiPop()
-end
-if inrange then
-	if enabled then
-
-			UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 300)
-      UiColor(0,0,1)
-      UiFont("bold.ttf", 30)
-      UiText("To disable viewable ragdoll stats, press H ")
-    UiPop()
-
-	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 350)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 30)
-      UiText("Total Blood Volume:  "..TotalBloodValue)
-    UiPop()
-
-    if alive then
-    	  UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiColor(0,1,0)
-      UiFont("bold.ttf", 60)
-      UiText("ALIVE")
-    UiPop()
-    if TotalBloodValue < 15000 then
-    	UiPush()
-      UiAlign("center middle")
-      UiTranslate(900, 450)
-      UiColor(1,1,0)
-      UiFont("bold.ttf", 50)
-      UiText("CRITICAL CONDITION")
-    UiPop()
-    end
-end
-if not alive then
-	  UiPush()
-	  UiColor(1,0,0)
-      UiAlign("center middle")
-      UiTranslate(900, 400)
-      UiFont("bold.ttf", 60)
-      UiText("DECEASED")
-    UiPop()
-end
-end
-end
-end
-
 function canSeePlayer()
-    local camTrans = GetPlayerCameraTransform()
+    local camTrans = GetPlayerCameraTransform(playerId)
 	local playerPos = camTrans.pos
 
 	--Direction to player
@@ -1000,7 +174,7 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	return not QueryRaycast(shootPos, dir, dist, 0, true)
 end
 
@@ -1014,6 +188,746 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	return not QueryRaycast(shootPos, dir, dist, 0, true)
-end+end
+
+function server.init()
+    Head = FindBody("Head")
+    HeadBloodCapacity = GetBodyMass(Head)
+    HeadBloodLevel = HeadBloodCapacity * 20
+    StartingBleed = HeadBloodCapacity
+    MaxBloodCapacity = GetBodyMass(Head)
+    bleed = true
+    Torso = FindBody("Torso")
+    TorsoBloodCapacity = GetBodyMass(Torso)
+    TorsoBloodLevel = TorsoBloodCapacity * 20
+    StartingBleed1 = TorsoBloodCapacity
+    MaxBloodCapacity1 = GetBodyMass(Torso)
+    bleed1 = true
+    LARM = FindBody("LARM")
+    LARMBloodCapacity = GetBodyMass(LARM)
+    LARMBloodLevel = LARMBloodCapacity * 20
+    StartingBleed2 = LARMBloodCapacity
+    MaxBloodCapacity2 = GetBodyMass(LARM)
+    bleed2 = true
+    LLARM = FindBody("LLARM")
+    LLARMBloodCapacity = GetBodyMass(LLARM)
+    LLARMBloodLevel = LLARMBloodCapacity * 20
+    StartingBleed3 = LLARMBloodCapacity
+    MaxBloodCapacity3 = GetBodyMass(LLARM)
+    bleed3 = true
+    RARM = FindBody("RARM")
+    RARMBloodCapacity = GetBodyMass(RARM)
+    RARMBloodLevel = RARMBloodCapacity * 20
+    StartingBleed4 = RARMBloodCapacity
+    MaxBloodCapacity4 = GetBodyMass(RARM)
+    bleed4 = true
+    RRARM = FindBody("RRARM")
+    RRARMBloodCapacity = GetBodyMass(RRARM)
+    RRARMBloodLevel = RRARMBloodCapacity * 20
+    StartingBleed5 = RRARMBloodCapacity
+    MaxBloodCapacity5 = GetBodyMass(RRARM)
+    bleed5 = true
+    LLEG = FindBody("LLEG")
+    LLEGBloodCapacity = GetBodyMass(LLEG)
+    LLEGBloodLevel = LLEGBloodCapacity * 20
+    StartingBleed6 = LLEGBloodCapacity
+    MaxBloodCapacity6 = GetBodyMass(LLEG)
+    bleed6 = true
+    LLLEG = FindBody("LLLEG")
+    LLLEGBloodCapacity = GetBodyMass(LLLEG)
+    LLLEGBloodLevel = LLLEGBloodCapacity * 20
+    StartingBleed7 = LLLEGBloodCapacity
+    MaxBloodCapacity7 = GetBodyMass(LLLEG)
+    bleed7 = true
+    RLEG = FindBody("RLEG")
+    RLEGBloodCapacity = GetBodyMass(RLEG)
+    RLEGBloodLevel = RLEGBloodCapacity * 20
+    StartingBleed8 = RLEGBloodCapacity
+    MaxBloodCapacity8 = GetBodyMass(RLEG)
+    bleed8 = true
+    RRLEG = FindBody("RRLEG")
+    RRLEGBloodCapacity = GetBodyMass(RRLEG)
+    RRLEGBloodLevel = RRLEGBloodCapacity * 20
+    StartingBleed9 = RRLEGBloodCapacity
+    MaxBloodCapacity9 = GetBodyMass(RRLEG)
+    bleed9 = true
+    antibleed = 15 -- only affects smoke speed
+    extremeantibleed = 500000 -- affects extreme bleed which is caused by total organ failure, reduce for blood to explode more
+    regularantibleed = 30000 -- affects cureable bleeds, reduce to have more blood in general
+    limbantibleed = 30000 -- affects bleeding of limbs, decrease to have more blood from arms and legs
+    MinBloodValue = 10000 -- minimum allowed blood value for human to stay alive
+    LimbBleedSpeed = 0.1
+    bloodgrav = -20
+    blooddrag = 0
+    startupspeed = Vec(0,0.7,0)
+    upspeed = Vec(0,0.7,0)
+    downspeed = Vec(0,-0.7,0)
+    alive = true
+    akm = FindBody("AKM")
+    weight = 500
+    bias = Vec(0,0,0)
+    biasb = Vec(0,0,0)
+    weightb = -0.6
+    agrotimer = 0
+    forget = 10
+    KillTimer = 0
+    Eliminate = 1
+    shootim = 0
+    shots = 0
+    reload = 0
+    recoil = 40
+    flare = FindLight("flare")
+    flaretim = false
+    flaretimer = 0
+    SetLightEnabled(flare, false)
+    disarmed = false
+    spetsnaz = FindShape("spetsnaz",true)
+    enemyspotted = false
+    	switched = true
+    	enabled = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        end
+        	if IsShapeBroken(spetsnaz) then
+        		RemoveTag(spetsnaz,"spetsnaz")
+        		agro = false
+        		agrotimer = 0
+        		spetsnaz = FindShape("spetsnaz",true)
+        		enemyspotted = false
+        		shoot = false
+        	end
+        	if PlayerHP == 0 then
+        		shoot = false
+        		agro = false
+        		agrotimer = 0
+        		enemyspotted = false
+        	end
+        	gunTrans = GetBodyTransform(Head)
+        	gunPos = gunTrans.pos
+        	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
+        	 shootPos = VecAdd(gunPos, VecScale(direction,0.2))
+        	drawtext = false
+        	HeadBloodCapacity = GetBodyMass(Head)
+        	Bleed = StartingBleed - HeadBloodCapacity
+        	HeadPos = GetBodyTransform(Head)
+        	TorsoBloodCapacity = GetBodyMass(Torso)
+        	Bleed1 = StartingBleed1 - TorsoBloodCapacity
+        	TorsoPos = GetBodyTransform(Torso)
+        	LARMBloodCapacity = GetBodyMass(LARM)
+        	Bleed2 = StartingBleed2 - LARMBloodCapacity
+        	LARMPos = GetBodyTransform(LARM)
+        	LLARMBloodCapacity = GetBodyMass(LLARM)
+        	Bleed3 = StartingBleed3 - LLARMBloodCapacity
+        	LLARMPos = GetBodyTransform(LLARM)
+        	RARMBloodCapacity = GetBodyMass(RARM)
+        	Bleed4 = StartingBleed4 - RARMBloodCapacity
+        	RARMPos = GetBodyTransform(RARM)
+        	RRARMBloodCapacity = GetBodyMass(RRARM)
+        	Bleed5 = StartingBleed5 - RRARMBloodCapacity
+        	RRARMPos = GetBodyTransform(RRARM)
+        	LLEGBloodCapacity = GetBodyMass(LLEG)
+        	Bleed6 = StartingBleed6 - LLEGBloodCapacity
+        	LLEGPos = GetBodyTransform(LLEG)
+        	LLLEGBloodCapacity = GetBodyMass(LLLEG)
+        	Bleed7 = StartingBleed7 - LLLEGBloodCapacity
+        	LLLEGPos = GetBodyTransform(LLLEG)
+        	RLEGBloodCapacity = GetBodyMass(RLEG)
+        	Bleed8 = StartingBleed8 - RLEGBloodCapacity
+        	RLEGPos = GetBodyTransform(RLEG)
+        	RRLEGBloodCapacity = GetBodyMass(RRLEG)
+        	Bleed9 = StartingBleed9 - RRLEGBloodCapacity
+        	RRLEGPos = GetBodyTransform(RRLEG)
+        	--AGRESSIVE BEHAVIOR
+        	if IsBodyBroken(LLARM) then
+        		disarmed = true
+        	end
+        	if canSeeSpetsnaz() then
+        			agro = true
+        		agrotimer = 0
+        		KillTimer = KillTimer + dt
+        		enemyspotted = true
+        		shoot = true
+
+        	end
+        	if canSeePlayer() then
+        		agro = true
+        		agrotimer = 0
+        		KillTimer = KillTimer + dt
+        		enemyspotted = true
+        		shoot = true
+        		end
+        		if agro then
+        			agrotimer = agrotimer + dt
+        		if agrotimer > forget then
+        		agro = false
+        		agrotimer = 0
+        		KillTimer = 0
+        	end
+        end
+        	--RELOAD
+        	if shots > 29 then
+        		reloading = true
+        		if alive then
+        		reload = reload + dt
+        		if reload > 4 then
+        			reloading = false
+        			shots = 0
+        			reload = 0
+        		end
+        	end
+        	end
+        	--ELIMINATE TARGET 
+        	local barrel = FindShape("barrel")
+        	local guntrans = GetShapeWorldTransform(barrel)
+        	local terrorist = FindShape("terrorist")
+        	terrorpos = GetShapeWorldTransform(terrorist)
+        	--DebugPrint("guny:  "..guntrans.pos[2])
+        	--DebugPrint("body:  "..terrorpos.pos[2])
+        	if guntrans.pos[2] < terrorpos.pos[2] then
+        		shoot = false
+        	end
+            local gunpos = guntrans.pos
+        	local direction = TransformToParentVec(guntrans, Vec(0, -1, 0))
+            local shootpos = VecAdd(gunpos, VecScale(direction, 0.2))
+            if flaretim then
+            	flaretimer = flaretimer + dt
+            	if flaretimer > 0.1 then
+            		SetLightEnabled(flare, false)
+            		flaretimer = 0
+            	end
+            end
+        	--AIM AIM AIM AIM AIM AIM AIM AIM AIM
+        	if enemyspotted then
+        	if not disarmed then
+        	if alive then
+        		if agro then
+        	local ppos = GetPlayerCameraTransform(playerId)
+        	ppos.pos[2] = ppos.pos[2] - 0.5
+        	spetsnazpos = GetShapeWorldTransform(spetsnaz)
+        	distToPlayeraim = VecLength(VecSub(ppos.pos, TorsoPos.pos))
+        	distToSpetsaim = VecLength(VecSub(spetsnazpos.pos, TorsoPos.pos))
+
+        	if distToPlayeraim > distToSpetsaim and canSeeSpetsnaz() then
+        	enemy = spetsnazpos.pos
+        else if distToPlayeraim > distToSpetsaim and not canSeeSpetsnaz() then
+        	enemy = ppos.pos
+        end
+        end
+        	if distToPlayeraim < distToSpetsaim and canSeePlayer() then
+        	enemy = ppos.pos
+        else if distToPlayeraim < distToSpetsaim and not canSeePlayer() then
+        	enemy = spetsnazpos.pos
+        end
+        	end
+
+        	local akmpos = GetBodyTransform(akm)
+
+        	local aimangle = QuatLookAt(akmpos.pos, enemy)
+
+        	local gunyaw, gunpitch, gunroll = GetQuatEuler(akmpos.rot)
+        	local aimyaw, aimpitch, aimroll = GetQuatEuler(aimangle)
+
+        --yaw
+         gunyaw = gunyaw + math.min(math.max(aimyaw - gunyaw, -weight), weight)
+          --pitch
+         gunpitch = gunpitch + math.min(math.max(aimpitch - gunpitch, -weight), weight)
+          --roll
+         gunroll = gunroll + math.min(math.max(aimroll - gunroll, -weight), weight)
+         if agro then
+
+         local bias = QuatEuler(gunyaw, gunpitch, gunroll)
+          SetBodyTransform(akm, Transform(akmpos.pos, bias))
+        end
+        end
+        end
+        --b = GetBodyTransform(LLARM)
+          --for i=1,3 do
+                --if(ppos.pos[i]<b.pos[i]) then
+                     --biasb[i] = -weightb
+                --elseif(ppos.pos[i]>b.pos[i]) then
+                  --  biasb[i] = weightb
+                --else
+                  --  biasb[i] = 0
+                --end
+            --end
+            --local currentVelocity = GetBodyVelocity(LLARM)
+            if alive then
+            	if agro then
+            local ppos = enemy
+            local bmi, bma = GetBodyBounds(LLARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(LLARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(LLARM, vel)
+        local bmi, bma = GetBodyBounds(RRARM)
+        		local bc = VecLerp(bmi, bma, 0.5)
+        		local ppos = enemy
+        		local dir = VecSub(bc, ppos)
+        		local dist = VecLength(dir)
+        		dir = VecScale(dir, 1.0/dist)
+            local add = VecScale(dir, weightb)
+        	local vel = GetBodyVelocity(RRARM)
+        	vel = VecAdd(vel, add)
+            SetBodyVelocity(RRARM, vel)
+        end
+        end
+        end
+        end
+          --akmpos.rot = Rot
+          --SetBodyTransform(akm, akmpos)
+        --HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD HEAD
+        	if bleed then
+        	if IsBodyBroken(Head) then
+
+        		for i=1, 9 do
+        		 	 thingz = FindJoints("eye")
+        		 	 for i=1, #thingz do
+        		 	 	thinz = thingz[i]
+        		 	 	Delete(thinz)
+        		 	 end
+        		 end
+
+        		for i=1,Bleed/2 do
+        		smoke()
+        	end
+        end
+        end
+        if bleed then
+
+        		if HeadBloodCapacity < MaxBloodCapacity then
+        		Bleed = Bleed * 6 
+        		for i=1,Bleed/6 do
+        		smoke()
+        	end
+        	end
+
+        HeadBloodLevel = HeadBloodLevel - Bleed/2
+        end
+        	if HeadBloodLevel <= 0 then
+        		bleed = false
+        		HeadBloodLevel = 0
+        	end
+        	--TORSO TORSO TORSO TORSO TORSO TORSO TORSO
+        	if bleed1 then
+        	if IsBodyBroken(Torso) then
+        		for i=1,Bleed1/regularantibleed do
+        		smoke1()
+        	end
+        end
+        end
+        if bleed1 then
+
+        		if TorsoBloodCapacity < MaxBloodCapacity1/2 then
+        		Bleed1 = Bleed1 * 6 
+        		 for i=1, 9 do
+        		 	 things = FindBodies("gut", true)
+        		 	 for i=1, #things do
+        		 	 	thing = things[i]
+        		 	 	SetBodyDynamic(thing, true)
+        		 	 end
+        		 end
+        		for i=1,Bleed1/extremeantibleed do
+        		smoke1()
+        	end
+        	end
+
+        TorsoBloodLevel = TorsoBloodLevel - Bleed1
+        end
+        	if TorsoBloodLevel <= 0 then
+        		bleed1 = false
+        		TorsoBloodLevel = 0
+        	end
+        -- ARMARMARMARMAMRAMRMARMAMRAMRMARMAMRAMMARMAMAMRMARMMRMARMRMAMRMAR
+        if bleed2 then
+
+        	if LARMBloodCapacity < MaxBloodCapacity2/3 then
+        		Bleed2 = Bleed2 * 6 
+        		for i=1,Bleed2/extremeantibleed do
+        		smoke2()
+        	end
+        	end
+
+        	if IsBodyBroken(LARM) then
+        		for i=1,Bleed2/limbantibleed do
+        		smoke2()
+        	end
+        end
+        end
+        if bleed2 then
+        LARMBloodLevel = LARMBloodLevel - Bleed2*LimbBleedSpeed
+        end
+        	if LARMBloodLevel <= 0 then
+        		bleed2 = false
+        		LARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        if bleed3 then
+
+        	if LLARMBloodCapacity < MaxBloodCapacity3/3 then
+        		Bleed3 = Bleed3 * 6 
+        		for i=1,Bleed3/extremeantibleed do
+        		smoke3()
+        	end
+        	end
+
+        	if IsBodyBroken(LLARM) then
+        		for i=1,Bleed3/limbantibleed do
+        		smoke3()
+        	end
+        end
+        end
+        if bleed3 then
+        LLARMBloodLevel = LLARMBloodLevel - Bleed3*LimbBleedSpeed
+        end
+        	if LLARMBloodLevel <= 0 then
+        		bleed3 = false
+        		LLARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed4 then
+
+        		if RARMBloodCapacity < MaxBloodCapacity4/3 then
+        		Bleed4 = Bleed4 * 6 
+        		for i=1,Bleed4/extremeantibleed do
+        		smoke4()
+        	end
+        	end
+
+        	if IsBodyBroken(RARM) then
+        		for i=1,Bleed4/limbantibleed do
+        		smoke4()
+        	end
+        end
+        end
+        if bleed4 then
+        RARMBloodLevel = RARMBloodLevel - Bleed4*LimbBleedSpeed
+        end
+        	if RARMBloodLevel <= 0 then
+        		bleed4 = false
+        		RARMBloodLevel = 0
+        	end
+        	--aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
+        	if bleed5 then
+
+        		if RRARMBloodCapacity < MaxBloodCapacity5/3 then
+        		Bleed5 = Bleed5 * 6 
+        		for i=1,Bleed5/extremeantibleed do
+        		smoke5()
+        	end
+        	end
+
+        	if IsBodyBroken(RRARM) then
+        		for i=1,Bleed5/limbantibleed do
+        		smoke5()
+        	end
+        end
+        end
+        if bleed5 then
+        RRARMBloodLevel = RRARMBloodLevel - Bleed5*LimbBleedSpeed
+        end
+        	if RRARMBloodLevel <= 0 then
+        		bleed5 = false
+        		RRARMBloodLevel = 0
+        	end
+        	--LEGLEGLEGLELGLELGLGLELGLEGLLGLEGLELGLEGLELGLEGLEGLELGELLEGLEGLLEGLEGLGELGELGLEGLELGELGLEGLEGLLEGLEGLLEGLELGLEGLELGLEGLLEGLELGELGELG
+        	if bleed6 then
+
+        		if LLEGBloodCapacity < MaxBloodCapacity6/3 then
+        		Bleed6 = Bleed6 * 6 
+        		for i=1,Bleed6/extremeantibleed do
+        		smoke6()
+        	end
+        	end
+
+        	if IsBodyBroken(LLEG) then
+        		for i=1,Bleed6/limbantibleed do
+        		smoke6()
+        	end
+        end
+        end
+        if bleed6 then
+        LLEGBloodLevel = LLEGBloodLevel - Bleed6*LimbBleedSpeed
+        end
+        	if LLEGBloodLevel <= 0 then
+        		bleed6 = false
+        	LLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed7 then
+
+        		if LLLEGBloodCapacity < MaxBloodCapacity7/3 then
+        		Bleed7 = Bleed7 * 6 
+        		for i=1,Bleed7/extremeantibleed do
+        		smoke7()
+        	end
+        	end
+
+        	if IsBodyBroken(LLLEG) then
+        		for i=1,Bleed7/limbantibleed do
+        		smoke7()
+        	end
+        end
+        end
+        if bleed7 then
+        LLLEGBloodLevel = LLLEGBloodLevel - Bleed7*LimbBleedSpeed
+        end
+        	if LLLEGBloodLevel <= 0 then
+        		bleed7 = false
+        	LLLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed8 then
+
+        		if RLEGBloodCapacity < MaxBloodCapacity8/3 then
+        		Bleed8 = Bleed8 * 6 
+        		for i=1,Bleed8/extremeantibleed do
+        		smoke8()
+        	end
+        	end
+
+        	if IsBodyBroken(RLEG) then
+        		for i=1,Bleed8/limbantibleed do
+        		smoke8()
+        	end
+        end
+        end
+        if bleed8 then
+        RLEGBloodLevel = RLEGBloodLevel - Bleed8*LimbBleedSpeed
+        end
+        	if RLEGBloodLevel <= 0 then
+        		bleed8 = false
+        	RLEGBloodLevel = 0
+        	end
+        	--lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll
+        	if bleed9 then
+
+        		if RRLEGBloodCapacity < MaxBloodCapacity9/3 then
+        		Bleed9 = Bleed9 * 6 
+        		for i=1,Bleed9/extremeantibleed do
+        		smoke9()
+        	end
+        	end
+
+        	if IsBodyBroken(RRLEG) then
+        		for i=1,Bleed9/limbantibleed do
+        		smoke9()
+        	end
+        end
+        end
+        if bleed9 then
+        RRLEGBloodLevel = RRLEGBloodLevel - Bleed9*LimbBleedSpeed
+        end
+        	if RRLEGBloodLevel <= 0 then
+        		bleed9 = false
+        	RRLEGBloodLevel = 0
+        	end
+        	TotalLegBloodCapacity = MaxBloodCapacity6 + MaxBloodCapacity7 + MaxBloodCapacity8 + MaxBloodCapacity9
+        	TotalLegBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel
+        	TotalBloodValue = RRLEGBloodLevel + RLEGBloodLevel + LLLEGBloodLevel + LLEGBloodLevel + RRARMBloodLevel + RARMBloodLevel + LLARMBloodLevel + LARMBloodLevel + TorsoBloodLevel + HeadBloodLevel
+        		upspeed[2] = TotalLegBloodValue/10000
+        	currentvel = GetBodyVelocity(Head)
+        	currentvel1 = GetBodyVelocity(LLLEG)
+        	currentvel2 = GetBodyVelocity(RRLEG)
+        	if IsBodyBroken(Head) then
+        		alive = false
+        	end
+        	if TorsoBloodLevel < MaxBloodCapacity1/4 or TorsoBloodCapacity < MaxBloodCapacity1/3 then
+        		alive = false
+        	end
+        	if TotalBloodValue < MinBloodValue then
+        		alive = false
+        	end
+        	if alive then
+        	SetBodyVelocity(Head,VecAdd(currentvel,upspeed))
+        	SetBodyVelocity(LLLEG,VecAdd(currentvel1,downspeed))
+        	SetBodyVelocity(RRLEG,VecAdd(currentvel2,downspeed))
+        end
+        a = GetPlayerTransform(playerId)
+        	distToPlayer = VecLength(VecSub(a.pos, TorsoPos.pos))
+        	if distToPlayer < 3 then
+        		inrange = true
+        	else
+        		inrange = false
+        	end
+    end
+end
+
+function client.init()
+    GunShot = LoadSound("MOD/gorescript/akm.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    	if InputPressed("H") then
+    		if switched then
+    			enabled = false
+    			switched = false
+    		else if not switched then
+    			enabled = true
+    		switched = true
+    		end
+    	end
+        if shoot then
+    	if KillTimer > Eliminate then
+    		if not disarmed then
+    		if not reloading then
+    			if not alive then
+    				dt = dt * 4
+    			end
+    		shootim = shootim + dt
+    		if shootim > 0.2 then
+    		Shoot(shootpos, direction)
+    		PlaySound(GunShot, shootpos,10)
+    		SetLightEnabled(flare, true)
+    		flaretim = true
+    		for i=1,33 do
+    		GunSmoke()
+    	end
+    		ApplyBodyImpulse(LLARM, Vec(0,0,0), Vec(math.random(-recoil,recoil),recoil,math.random(-recoil,recoil)))
+    		shootim = 0
+    		shots = shots + 1
+    	end
+    end
+    	end
+    end
+    end
+end
+
+function client.draw()
+    if drawtext then
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("Head Blood Level:  "..HeadBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 220)
+          UiFont("bold.ttf", 30)
+          UiText("Torso Blood Level:  "..TorsoBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 240)
+          UiFont("bold.ttf", 30)
+          UiText("upper left arm Blood Level:  "..LARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 260)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left arm Blood Level:  "..LLARMBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 280)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right arm Blood Level:  "..RARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 300)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right arm Blood Level:  "..RRARMBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 320)
+          UiFont("bold.ttf", 30)
+          UiText("Upper left leg Blood Level:  "..LLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 340)
+          UiFont("bold.ttf", 30)
+          UiText("Lower left leg Blood Level:  "..LLLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 360)
+          UiFont("bold.ttf", 30)
+          UiText("Upper right leg Blood Level:  "..RLEGBloodLevel)
+        UiPop()
+
+         UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 380)
+          UiFont("bold.ttf", 30)
+          UiText("Lower right leg Blood Level:  "..RRLEGBloodLevel)
+        UiPop()
+
+        UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 400)
+          UiFont("bold.ttf", 30)
+          UiText("total Blood Level:  "..TotalBloodValue)
+        UiPop()
+    end
+    if inrange then
+    	if enabled then
+
+    			UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 300)
+          UiColor(0,0,1)
+          UiFont("bold.ttf", 30)
+          UiText("To disable viewable ragdoll stats, press H ")
+        UiPop()
+
+    	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 350)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 30)
+          UiText("Total Blood Volume:  "..TotalBloodValue)
+        UiPop()
+
+        if alive then
+        	  UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiColor(0,1,0)
+          UiFont("bold.ttf", 60)
+          UiText("ALIVE")
+        UiPop()
+        if TotalBloodValue < 15000 then
+        	UiPush()
+          UiAlign("center middle")
+          UiTranslate(900, 450)
+          UiColor(1,1,0)
+          UiFont("bold.ttf", 50)
+          UiText("CRITICAL CONDITION")
+        UiPop()
+        end
+    end
+    if not alive then
+    	  UiPush()
+    	  UiColor(1,0,0)
+          UiAlign("center middle")
+          UiTranslate(900, 400)
+          UiFont("bold.ttf", 60)
+          UiText("DECEASED")
+        UiPop()
+    end
+    end
+    end
+end
+

```

---

# Migration Report: main\Airport\airport.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Airport\airport.lua
+++ patched/main\Airport\airport.lua
@@ -1,157 +1,155 @@
-function init()
-	local announceList={"covid_announch_general","Flight_N2904A","Flight_N10042A","Flight_N10759A","keep_distance_for_workers","wear_your_mask"}
-	local secretList={"deffcolony_easteregg1_version_2","russianglitch","sheeeeesh"}
-	announcements = {}
-	for i=1, #announceList do
-		announcements[i] = LoadSound("MOD/main/Airport/snd/Announcements/"..announceList[i]..".ogg")
-	end
-	secrets = {}
-	for i=1, #secretList do
-		secrets[i] = LoadSound("MOD/main/Airport/snd/easter eggs/"..secretList[i]..".ogg")
-	end
-	
-	damageLV1 = LoadSound("MOD/main/Airport/snd/Announcements/Damaged airport/evac_normal.ogg")
-	damageLV2 = LoadSound("MOD/main/Airport/snd/Announcements/Damaged airport/EVAC_glitch1.ogg")
-	damageIntercom = LoadSound("MOD/main/Airport/snd/Announcements/Damaged airport/intercom_damanged3.ogg")
-	alertTimer = 0
-	alertActive = false
-	alert2active = false
-	
-	speakers = FindShapes("speaker",true)
-	announcementTimer = 8
-	
-	outsideSnd = LoadLoop("MOD/main/Airport/snd/EXT airport.ogg")
-	insideSnd = LoadLoop("MOD/main/Airport/snd/INT airport.ogg")
-	airportTrigger = FindTrigger("airportInside")
-	airportShapes = {}
-	airportVoxCount = 0
-	
-	local shapes=FindShapes(nil,true)
-	for i=1, #shapes do
-		shape = shapes[i]
-		if IsShapeInTrigger(airportTrigger,shape) then
-			table.insert(airportShapes,shape)
-			airportVoxCount = airportVoxCount + GetShapeVoxelCount(shape)
-		end
-	end
-	
-	cessna = FindBody("cessna")
-	cessnaSnd = LoadLoop("MOD/main/Airport/snd/Cessna_195_Flyby_Distant.ogg")
-	cessnaTerminated = LoadSound("MOD/main/Airport/snd/easter eggs/Easter_egg_tarmac.ogg")
-	cessnaDropped = false
-	flybyAngle = 0
-	flybyTimer = 2000
-	
-	Timer = 0
+#version 2
+function server.init()
+    local announceList={"covid_announch_general","Flight_N2904A","Flight_N10042A","Flight_N10759A","keep_distance_for_workers","wear_your_mask"}
+    local secretList={"deffcolony_easteregg1_version_2","russianglitch","sheeeeesh"}
+    announcements = {}
+    secrets = {}
+    alertTimer = 0
+    alertActive = false
+    alert2active = false
+    speakers = FindShapes("speaker",true)
+    announcementTimer = 8
+    outsideSnd = LoadLoop("MOD/main/Airport/snd/EXT airport.ogg")
+    insideSnd = LoadLoop("MOD/main/Airport/snd/INT airport.ogg")
+    airportTrigger = FindTrigger("airportInside")
+    airportShapes = {}
+    airportVoxCount = 0
+    local shapes=FindShapes(nil,true)
+    for i=1, #shapes do
+    	shape = shapes[i]
+    	if IsShapeInTrigger(airportTrigger,shape) then
+    		table.insert(airportShapes,shape)
+    		airportVoxCount = airportVoxCount + GetShapeVoxelCount(shape)
+    	end
+    end
+    cessna = FindBody("cessna")
+    cessnaSnd = LoadLoop("MOD/main/Airport/snd/Cessna_195_Flyby_Distant.ogg")
+    cessnaDropped = false
+    flybyAngle = 0
+    flybyTimer = 2000
+    Timer = 0
 end
 
-function tick(dt)
-	pTrans = GetPlayerTransform()
-	Timer = Timer + dt
-	announcementTimer = announcementTimer-dt
-	
-	flybyTimer = flybyTimer + (dt*40)
-	if flybyTimer > 1500 then
-		flybyTimer = -1500
-		flybyAngle = math.random(-180,180)
-		PlaySound(cessnaSnd,pTrans.pos,5)
-	end
-	
-	for i=1, #speakers do
-		if IsShapeBroken(speakers[i]) then
-			table.remove(speakers,i)
-		end
-	end
-	
-	if announcementTimer < 0 and not alertActive then
-		local announcement
-		if math.random(1,5) == 2 then
-			announcement = secrets[math.random(1,#secrets)]
-		else
-			announcement = announcements[math.random(1,#announcements)]
-		end
-		for i=1, #speakers do
-			
-			local pos = GetShapeWorldTransform(speakers[i]).pos
-			local dist = VecLength(VecSub(pTrans.pos,pos))
-			--DebugPrint(dist)
-			if dist<45 then
-				PlaySound(announcement,pos,50/dist)
-			end
-		end
-		announcementTimer = math.random(7,11)*6
-	end
-	if IsPointInTrigger(airportTrigger,pTrans.pos) then
-		PlayLoop(insideSnd,pTrans.pos,5)
-	else
-		PlayLoop(outsideSnd,pTrans.pos,5)
-	end
-	if not IsBodyDynamic(cessna) then
-		SetBodyTransform(cessna,TransformToParentTransform(Transform(Vec(0,0,0),QuatEuler(0,flybyAngle,0)),Transform(Vec(0,100,flybyTimer),Quat())))
-	end
-	if IsBodyBroken(cessna) and not cessnaDropped then
-		SetBodyDynamic(cessna,true)
-		SetBodyVelocity(cessna,TransformToParentVec(GetBodyTransform(cessna),Vec(0,0,40)))
-		cessnaDropped = true
-		
-		for i=1, #speakers do
-			
-			local pos = GetShapeWorldTransform(speakers[i]).pos
-			local dist = VecLength(VecSub(pTrans.pos,pos))
-			--DebugPrint(dist)
-			if dist<45 then
-				PlaySound(cessnaTerminated,pos,50/dist)
-			end
-		end
-	end
-	--DebugLine(Vec(0,0,0),GetBodyTransform(cessna).pos)
-	
-	local currentVoxCount = 0
-	for i=1, #airportShapes do
-		shape = airportShapes[i]
-		currentVoxCount = currentVoxCount + GetShapeVoxelCount(shape)
-	end
-	local percent = currentVoxCount/airportVoxCount
-	--DebugPrint(percent)
-	local alert=0
-	if percent <= 0.988 then
-		alert=damageLV1
-		alertActive=true
-	end
-	if percent <= 0.967 then
-		alert=damageLV2
-		alertActive=true
-	end
-	--DebugPrint(#speakers)
-	if #speakers < 2 then
-		alert=damageIntercom
-		alertActive=true
-		--DebugPrint("aaaa")
-		alert2active=true
-	end
-	
-	alertTimer = alertTimer - dt
-	if alert ~= 0 and alertTimer < 0 then
-		alertTimer = 25
-		for i=1, #speakers do
-			if IsShapeBroken(speakers[i]) then
-				table.remove(speakers,i)
-			else
-				local pos = GetShapeWorldTransform(speakers[i]).pos
-				local dist = VecLength(VecSub(pTrans.pos,pos))
-				--DebugPrint(dist)
-				if dist<45 then
-					PlaySound(alert,pos,50/dist)
-				end
-			end
-		end
-	end
-	
-	if alertActive then
-		SetBool('airport.gate_info.alert',true)
-	end
-	if alert2active then
-		SetBool('airport.gate_info.lost_signal',true)
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        pTrans = GetPlayerTransform(playerId)
+        Timer = Timer + dt
+        announcementTimer = announcementTimer-dt
+        flybyTimer = flybyTimer + (dt*40)
+        for i=1, #speakers do
+        	if IsShapeBroken(speakers[i]) then
+        		table.remove(speakers,i)
+        	end
+        end
+        if not IsBodyDynamic(cessna) then
+        	SetBodyTransform(cessna,TransformToParentTransform(Transform(Vec(0,0,0),QuatEuler(0,flybyAngle,0)),Transform(Vec(0,100,flybyTimer),Quat())))
+        end
+        --DebugLine(Vec(0,0,0),GetBodyTransform(cessna).pos)
+        local currentVoxCount = 0
+        for i=1, #airportShapes do
+        	shape = airportShapes[i]
+        	currentVoxCount = currentVoxCount + GetShapeVoxelCount(shape)
+        end
+        local percent = currentVoxCount/airportVoxCount
+        --DebugPrint(percent)
+        local alert=0
+        if percent <= 0.988 then
+        	alert=damageLV1
+        	alertActive=true
+        end
+        if percent <= 0.967 then
+        	alert=damageLV2
+        	alertActive=true
+        end
+        --DebugPrint(#speakers)
+        if #speakers < 2 then
+        	alert=damageIntercom
+        	alertActive=true
+        	--DebugPrint("aaaa")
+        	alert2active=true
+        end
+        alertTimer = alertTimer - dt
+        if alertActive then
+        	SetBool('airport.gate_info.alert',true, true)
+        end
+        if alert2active then
+        	SetBool('airport.gate_info.lost_signal',true, true)
+        end
+    end
 end
 
+function client.init()
+    for i=1, #announceList do
+    	announcements[i] = LoadSound("MOD/main/Airport/snd/Announcements/"..announceList[i]..".ogg")
+    end
+    for i=1, #secretList do
+    	secrets[i] = LoadSound("MOD/main/Airport/snd/easter eggs/"..secretList[i]..".ogg")
+    end
+    damageLV1 = LoadSound("MOD/main/Airport/snd/Announcements/Damaged airport/evac_normal.ogg")
+    damageLV2 = LoadSound("MOD/main/Airport/snd/Announcements/Damaged airport/EVAC_glitch1.ogg")
+    damageIntercom = LoadSound("MOD/main/Airport/snd/Announcements/Damaged airport/intercom_damanged3.ogg")
+    cessnaTerminated = LoadSound("MOD/main/Airport/snd/easter eggs/Easter_egg_tarmac.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if flybyTimer > 1500 then
+    	flybyTimer = -1500
+    	flybyAngle = math.random(-180,180)
+    	PlaySound(cessnaSnd,pTrans.pos,5)
+    end
+    if announcementTimer < 0 and not alertActive then
+    	local announcement
+    	if math.random(1,5) == 2 then
+    		announcement = secrets[math.random(1,#secrets)]
+    	else
+    		announcement = announcements[math.random(1,#announcements)]
+    	end
+    	for i=1, #speakers do
+
+    		local pos = GetShapeWorldTransform(speakers[i]).pos
+    		local dist = VecLength(VecSub(pTrans.pos,pos))
+    		--DebugPrint(dist)
+    		if dist<45 then
+    			PlaySound(announcement,pos,50/dist)
+    		end
+    	end
+    	announcementTimer = math.random(7,11)*6
+    end
+    if IsPointInTrigger(airportTrigger,pTrans.pos) then
+    	PlayLoop(insideSnd,pTrans.pos,5)
+    else
+    	PlayLoop(outsideSnd,pTrans.pos,5)
+    end
+    if IsBodyBroken(cessna) and not cessnaDropped then
+    	SetBodyDynamic(cessna,true)
+    	SetBodyVelocity(cessna,TransformToParentVec(GetBodyTransform(cessna),Vec(0,0,40)))
+    	cessnaDropped = true
+
+    	for i=1, #speakers do
+
+    		local pos = GetShapeWorldTransform(speakers[i]).pos
+    		local dist = VecLength(VecSub(pTrans.pos,pos))
+    		--DebugPrint(dist)
+    		if dist<45 then
+    			PlaySound(cessnaTerminated,pos,50/dist)
+    		end
+    	end
+    end
+    if alert ~= 0 and alertTimer < 0 then
+    	alertTimer = 25
+    	for i=1, #speakers do
+    		if IsShapeBroken(speakers[i]) then
+    			table.remove(speakers,i)
+    		else
+    			local pos = GetShapeWorldTransform(speakers[i]).pos
+    			local dist = VecLength(VecSub(pTrans.pos,pos))
+    			--DebugPrint(dist)
+    			if dist<45 then
+    				PlaySound(alert,pos,50/dist)
+    			end
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: main\Airport\screens\GateInfo.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Airport\screens\GateInfo.lua
+++ patched/main\Airport\screens\GateInfo.lua
@@ -1,7 +1,21 @@
--- Screen Res 400 900
--- Screen Script MOD/main/Airport/screens/GateInfo.lua
+#version 2
+function cR(r)
+    return r/255
+end
 
-function init()
+function cG(g)
+    return g/255
+end
+
+function cB(b)
+    return b/255
+end
+
+function cA(a)
+    return a/100
+end
+
+function server.init()
     Gate = "A-11"
     Text01 = "Lockelle flight"
     Flight = "N10759A"
@@ -14,43 +28,26 @@
     Text_departure_1 = "boarding in"
     Text_departure_2 = "41 minutes"
     Text_evac = "Please evacuate\nthe airport"
-
     -- Lost Signal
-
     full_alert_timer = 1
     full_alert_started = false
     full_alert_bool = false
-
     full_alert_timer_sec = 5
-
     -- Lost Signal
-
     lost_signal_timer = 1
     lost_signal_started = false
     lost_signal_bool = false
-
     lost_signal_timer_sec = 1
 end
-function cR(r)
-    return r/255
-end
-function cG(g)
-    return g/255
-end
-function cB(b)
-    return b/255
-end
-function cA(a)
-    return a/100
-end
-function draw()
+
+function client.draw()
     if full_alert_bool == false then 
         if GetBool('airport.gate_info.alert') then 
             if full_alert_started == false then 
                 full_alert_started = true 
                 SetValue('full_alert_timer',0,"linear",full_alert_timer_sec)
             elseif full_alert_started == true and full_alert_timer == 0 then
-                SetBool('airport.gate_info.full_alert',true)
+                SetBool('airport.gate_info.full_alert',true, true)
                 full_alert_bool = true
             end
         end
@@ -61,7 +58,7 @@
                 lost_signal_started = true
                 SetValue('lost_signal_timer',0,"linear",lost_signal_timer_sec)
             elseif lost_signal_started == true and lost_signal_timer == 0 then
-                SetBool('airport.gate_info.lost_signal_full',true)
+                SetBool('airport.gate_info.lost_signal_full',true, true)
                 lost_signal_bool = true
             end
         end
@@ -192,4 +189,5 @@
             UiPop()
         UiPop()
     end
-end+end
+

```

---

# Migration Report: main\Boeing 737\script\cabinsnd.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\cabinsnd.lua
+++ patched/main\Boeing 737\script\cabinsnd.lua
@@ -1,22 +1,22 @@
---this script will play distorted music if the sound option has been enabled from the menu (on by default), and the map's easter egg layer has been loaded.
-
-function init()
-	cabinLoop = LoadLoop("MOD/main/Boeing 737/snd/AMB_-_Airplane_Tone-737-Floor-01-01-D100")
-	decompressLoop = LoadLoop("MOD/main/Boeing 737/snd/plane_depressurized")
-	engineLoop = LoadLoop("MOD/main/Boeing 737/snd/depressurized_engines")
-	trigger = FindTrigger("cabinsnd", true)
+#version 2
+function server.init()
+    cabinLoop = LoadLoop("MOD/main/Boeing 737/snd/AMB_-_Airplane_Tone-737-Floor-01-01-D100")
+    decompressLoop = LoadLoop("MOD/main/Boeing 737/snd/plane_depressurized")
+    engineLoop = LoadLoop("MOD/main/Boeing 737/snd/depressurized_engines")
+    trigger = FindTrigger("cabinsnd", true)
 end
 
-function draw()	
-		if IsPointInTrigger(trigger, GetPlayerTransform().pos) then
-			if GetBool("level.depressurized") then
-				if GetInt("level.engines") > 0 then
-					PlayLoop(engineLoop, GetPlayerTransform().pos, 0.1)
-				else
-					PlayLoop(decompressLoop, GetPlayerTransform().pos, 2)
-				end
-			else
-				PlayLoop(cabinLoop, GetPlayerTransform().pos, 2)
-			end
-		end
-	end+function client.draw()
+    if IsPointInTrigger(trigger, GetPlayerTransform(playerId).pos) then
+    	if GetBool("level.depressurized") then
+    		if GetInt("level.engines") > 0 then
+    			PlayLoop(engineLoop, GetPlayerTransform(playerId).pos, 0.1)
+    		else
+    			PlayLoop(decompressLoop, GetPlayerTransform(playerId).pos, 2)
+    		end
+    	else
+    		PlayLoop(cabinLoop, GetPlayerTransform(playerId).pos, 2)
+    	end
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\cockpitsnd.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\cockpitsnd.lua
+++ patched/main\Boeing 737\script\cockpitsnd.lua
@@ -1,21 +1,21 @@
---this script will play distorted music if the sound option has been enabled from the menu (on by default), and the map's easter egg layer has been loaded.
-
-function init()
-	cockpitLoop = LoadLoop("MOD/main/Boeing 737/snd/AMB_-_inside_the_cockpit_FLYING_-_room_tone_-_loopable")
-	decompressLoop = LoadLoop("MOD/main/Boeing 737/snd/plane_depressurized")
-	engineLoop = LoadLoop("MOD/main/Boeing 737/snd/depressurized_engines_cockpit")
-	trigger = FindTrigger("cockpitsnd", true)
+#version 2
+function server.init()
+    cockpitLoop = LoadLoop("MOD/main/Boeing 737/snd/AMB_-_inside_the_cockpit_FLYING_-_room_tone_-_loopable")
+    decompressLoop = LoadLoop("MOD/main/Boeing 737/snd/plane_depressurized")
+    engineLoop = LoadLoop("MOD/main/Boeing 737/snd/depressurized_engines_cockpit")
+    trigger = FindTrigger("cockpitsnd", true)
 end
 
-function draw()	
-		if IsPointInTrigger(trigger, GetPlayerTransform().pos) then
-			if GetBool("level.depressurized") then
-				PlayLoop(decompressLoop, GetPlayerTransform().pos, 2)
-				if GetInt("level.engines") > 0 then
-					PlayLoop(engineLoop, GetPlayerTransform().pos, 1)
-				end
-			else
-				PlayLoop(cockpitLoop, GetPlayerTransform().pos, 0.2)
-			end
-		end
-	end+function client.draw()
+    if IsPointInTrigger(trigger, GetPlayerTransform(playerId).pos) then
+    	if GetBool("level.depressurized") then
+    		PlayLoop(decompressLoop, GetPlayerTransform(playerId).pos, 2)
+    		if GetInt("level.engines") > 0 then
+    			PlayLoop(engineLoop, GetPlayerTransform(playerId).pos, 1)
+    		end
+    	else
+    		PlayLoop(cockpitLoop, GetPlayerTransform(playerId).pos, 0.2)
+    	end
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\eDoorLeft.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\eDoorLeft.lua
+++ patched/main\Boeing 737\script\eDoorLeft.lua
@@ -1,25 +1,4 @@
-function init()
-	door = FindShape("door")
-	
-	loc = FindLocation("loc")
-	
-	pos = GetLocationTransform(loc)
-	
-	leverJoint = FindJoint("leverJoint")
-	--lmin, lmax = GetJointLimits(leverJoint)
-end
-
-function tick(dt)
-	local p = GetJointMovement(leverJoint)
-	SetJointMotorTarget(leverJoint, 0, 0.03)
-	
-	if p >= 0.1 then
-		doorBlast()
-	end
-	
-	--DebugPrint(p)
-end
-
+#version 2
 function doorBlast()
 	SetBodyVelocity(GetShapeBody(door), Vec(-3, 0, 0))
 	
@@ -36,4 +15,22 @@
 	ParticleGravity(0)
 	--particle spawn
 	SpawnParticle(pos.pos, Vec(-3,0,0), 3)
-end+end
+
+function server.init()
+    door = FindShape("door")
+    loc = FindLocation("loc")
+    pos = GetLocationTransform(loc)
+    leverJoint = FindJoint("leverJoint")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local p = GetJointMovement(leverJoint)
+        SetJointMotorTarget(leverJoint, 0, 0.03)
+        if p >= 0.1 then
+        	doorBlast()
+        end
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\eDoorRearLeft.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\eDoorRearLeft.lua
+++ patched/main\Boeing 737\script\eDoorRearLeft.lua
@@ -1,24 +1,4 @@
-function init()
-	door = FindShape("door")
-	
-	loc = FindLocation("loc")
-	
-	pos = GetLocationTransform(loc)
-	
-	leverJoint = FindJoint("leverJoint")
-	--lmin, lmax = GetJointLimits(leverJoint)
-end
-
-function tick(dt)
-	local p = GetJointMovement(leverJoint)
-	
-	if p >= 169 then
-		doorBlast()
-	end
-	
-	--DebugPrint(p)
-end
-
+#version 2
 function doorBlast()
 	SetBodyVelocity(GetShapeBody(door), Vec(-3, 0, 0))
 	
@@ -35,4 +15,21 @@
 	ParticleGravity(0)
 	--particle spawn
 	SpawnParticle(pos.pos, Vec(-3,0,0), 3)
-end+end
+
+function server.init()
+    door = FindShape("door")
+    loc = FindLocation("loc")
+    pos = GetLocationTransform(loc)
+    leverJoint = FindJoint("leverJoint")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local p = GetJointMovement(leverJoint)
+        if p >= 169 then
+        	doorBlast()
+        end
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\eDoorRearRight.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\eDoorRearRight.lua
+++ patched/main\Boeing 737\script\eDoorRearRight.lua
@@ -1,25 +1,4 @@
-function init()
-	door = FindShape("door")
-	
-	loc = FindLocation("loc")
-	
-	pos = GetLocationTransform(loc)
-	
-	leverJoint = FindJoint("leverJoint")
-	--lmin, lmax = GetJointLimits(leverJoint)
-end
-
-function tick(dt)
-	local p = GetJointMovement(leverJoint)
-	
-	if p <= -169 then
-		doorBlast()
-	end
-	
-	--DebugPrint(p)	
-
-end
-
+#version 2
 function doorBlast()
 	SetBodyVelocity(GetShapeBody(door), Vec(3, 0, 0))
 	
@@ -36,4 +15,21 @@
 	ParticleGravity(0)
 	--particle spawn
 	SpawnParticle(pos.pos, Vec(3,0,0), 3)
-end+end
+
+function server.init()
+    door = FindShape("door")
+    loc = FindLocation("loc")
+    pos = GetLocationTransform(loc)
+    leverJoint = FindJoint("leverJoint")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local p = GetJointMovement(leverJoint)
+        if p <= -169 then
+        	doorBlast()
+        end
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\eDoorRight.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\eDoorRight.lua
+++ patched/main\Boeing 737\script\eDoorRight.lua
@@ -1,25 +1,4 @@
-function init()
-	door = FindShape("door")
-	
-	loc = FindLocation("loc")
-	
-	pos = GetLocationTransform(loc)
-	
-	leverJoint = FindJoint("leverJoint")
-	--lmin, lmax = GetJointLimits(leverJoint)
-end
-
-function tick(dt)
-	local p = GetJointMovement(leverJoint)
-	SetJointMotorTarget(leverJoint, 0, 0.03)
-	
-	if p >= 0.1 then
-		doorBlast()
-	end
-	
-
-end
-
+#version 2
 function doorBlast()
 	SetBodyVelocity(GetShapeBody(door), Vec(3, 0, 0))
 	
@@ -36,4 +15,22 @@
 	ParticleGravity(0)
 	--particle spawn
 	SpawnParticle(pos.pos, Vec(3,0,0), 3)
-end+end
+
+function server.init()
+    door = FindShape("door")
+    loc = FindLocation("loc")
+    pos = GetLocationTransform(loc)
+    leverJoint = FindJoint("leverJoint")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local p = GetJointMovement(leverJoint)
+        SetJointMotorTarget(leverJoint, 0, 0.03)
+        if p >= 0.1 then
+        	doorBlast()
+        end
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\engineblades.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\engineblades.lua
+++ patched/main\Boeing 737\script\engineblades.lua
@@ -1,132 +1,4 @@
-function init()
-	joints = FindJoints("engine")
-	for j, joint in pairs(joints) do
-		SetJointMotor(joint, 20)
-	end
-	bodies = FindBodies() --gets all bodies under the script because those are all we need (the propellers)
-	enginepos = GetLocationTransform(FindLocation("emit")).pos
-	enginebreak = 0
-	flame = 100
-	SetInt("level.engines",2)
-	enginebroken = false
-	smallsound = {}
-	for i=0,5 do
-		smallsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_small/"..i)
-	end
-	bigsound = {}
-	for i=0,3 do
-		bigsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_big/"..i)
-	end
-end
-
-function tick(dt)
-	
-	local id = GetIntParam("id")
-	red = GetInt("level.engines."..id..".red")
-	
-	local ptrans = GetPlayerTransform()
-	for b, body in pairs(bodies) do
-		center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
-		voxels, broken, total = GetBodyVoxelCount(body)
-		local soundpos = VecLerp(ptrans.pos,center,0.1)
-		if voxels == 0 then --completely destroyed = no vfx
-			enginebreak = 2
-			flame = -150
-			if enginebroken == false then
-				PlaySound(bigsound[math.random(1,3)],enginepos,100)
-				SetInt("level.engines",GetInt("level.engines")-1)
-				enginebroken = true
-			end
-		end
-		if broken > 0 and enginebreak == 0 then
-			enginebreak = 1
-			PlaySound(smallsound[math.random(1,5)],soundpos,5)
-		elseif broken > 15 and enginebreak <= 1 then
-			enginebreak = 2
-			PlaySound(bigsound[math.random(1,3)],soundpos,100)
-			if enginebroken == false then
-				SetInt("level.engines",GetInt("level.engines")-1)
-				enginebroken = true
-			end
-		end
-		if center[2] < 165  and flame > 0 then --when an engine falls off it explodes
-			Explosion(center,4)
-			enginebreak = 2
-			flame = -150
-			PlaySound(bigsound[math.random(1,3)],enginepos,100)
-			if enginebroken == false then
-				SetInt("level.engines",GetInt("level.engines")-1)
-				enginebroken = true
-			end
-		end
-	end
-	if enginebreak == 2 then --very, very bad things are happening
-		if flame > 0 then
-			flame = flame - 1
-		end
-		--first spawn fire
-		ParticleReset()
-		ParticleColor(1,0.6,0.3,0.1,0.1,0.1,"linear",0,0.5)
-		ParticleEmissive(2,0,"linear",0,0.5)
-		ParticleRadius(2.75+(flame/400),5,"linear",0.2,1)
-		ParticleAlpha(1.0,0.0)
-		ParticleCollide(0)
-		ParticleGravity(0,-2)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),(flame/50)+1.5)
-		--next is smoke
-		ParticleReset()
-		ParticleColor(0.16,0.15,0.15)
-		ParticleRadius(3,5)
-		ParticleAlpha(0.8,0.0,"linear",0.03,0.9)
-		ParticleCollide(0)
-		ParticleGravity(0,-2)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),(flame/20)+3.5)
-	elseif enginebreak == 1 then --bad things are sort of happening
-		ParticleReset()
-		ParticleColor(0.5,0.4,0.4)
-		ParticleRadius(3,5)
-		ParticleAlpha(0.3,0.0,"linear",0.03,0.9)
-		ParticleCollide(0)
-		ParticleGravity(0,-2)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),7)
-	else --engine is nominal
-		ParticleReset()
-		ParticleColor(0.9,0.9,0.9)
-		ParticleRadius(3,10)
-		if red > 0 then
-			ParticleAlpha(0.1,0.0,"linear",0.03,0.9)
-		else
-			ParticleAlpha(0.3,0.0,"linear",0.03,0.9)
-		end
-		ParticleCollide(0)
-		ParticleGravity(0,-2)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),20)
-	end
-	
-	if red > 0 and enginebreak < 2 then --funny tomato juice in the engines
-		SetInt("level.engines."..id..".red",red-1)
-		
-		ParticleReset()
-		ParticleColor(0.4,0.2,0.2)
-		ParticleRadius(3.1,5)
-		ParticleAlpha(0.5,0.0,"linear",0.03,0.9)
-		ParticleCollide(0)
-		ParticleGravity(0,-2)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),7)
-	end
-	
-	if enginebreak < 2 then
-		sceneBodies = FindBodies(nil,true)
-		for b=1,#sceneBodies do
-			bTrans = GetBodyTransform(sceneBodies[b])
-			if VecLength(VecMult(VecSub(bTrans.pos,enginepos),Vec(1,1,0.4))) < 5 then
-				ApplyBodyImpulse(sceneBodies[b],bTrans.pos,Vec(0,0,100))
-				DrawBodyOutline(sceneBodies[b])
-			end
-		end
-	end
-end
-
+#version 2
 function GetBodyVoxelCount(body)
 	local broken = 0
 	local voxels = 0
@@ -143,3 +15,138 @@
 function VecMult(a,b)
 	return Vec(a[1]*b[1],a[2]*b[2],a[3]*b[3])
 end
+
+function server.init()
+    joints = FindJoints("engine")
+    for j, joint in pairs(joints) do
+    	SetJointMotor(joint, 20)
+    end
+    bodies = FindBodies() --gets all bodies under the script because those are all we need (the propellers)
+    enginepos = GetLocationTransform(FindLocation("emit")).pos
+    enginebreak = 0
+    flame = 100
+    SetInt("level.engines",2, true)
+    enginebroken = false
+    smallsound = {}
+    bigsound = {}
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local id = GetIntParam("id")
+        red = GetInt("level.engines."..id..".red")
+        local ptrans = GetPlayerTransform(playerId)
+        if enginebreak < 2 then
+        	sceneBodies = FindBodies(nil,true)
+        	for b=1,#sceneBodies do
+        		bTrans = GetBodyTransform(sceneBodies[b])
+        		if VecLength(VecMult(VecSub(bTrans.pos,enginepos),Vec(1,1,0.4))) < 5 then
+        			ApplyBodyImpulse(sceneBodies[b],bTrans.pos,Vec(0,0,100))
+        			DrawBodyOutline(sceneBodies[b])
+        		end
+        	end
+        end
+    end
+end
+
+function client.init()
+    for i=0,5 do
+    	smallsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_small/"..i)
+    end
+    for i=0,3 do
+    	bigsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_big/"..i)
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    for b, body in pairs(bodies) do
+    	center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
+    	voxels, broken, total = GetBodyVoxelCount(body)
+    	local soundpos = VecLerp(ptrans.pos,center,0.1)
+    	if voxels == 0 then --completely destroyed = no vfx
+    		enginebreak = 2
+    		flame = -150
+    		if enginebroken == false then
+    			PlaySound(bigsound[math.random(1,3)],enginepos,100)
+    			SetInt("level.engines",GetInt("level.engines")-1, true)
+    			enginebroken = true
+    		end
+    	end
+    	if broken > 0 and enginebreak == 0 then
+    		enginebreak = 1
+    		PlaySound(smallsound[math.random(1,5)],soundpos,5)
+    	elseif broken > 15 and enginebreak <= 1 then
+    		enginebreak = 2
+    		PlaySound(bigsound[math.random(1,3)],soundpos,100)
+    		if enginebroken == false then
+    			SetInt("level.engines",GetInt("level.engines")-1, true)
+    			enginebroken = true
+    		end
+    	end
+    	if center[2] < 165  and flame ~= 0 then --when an engine falls off it explodes
+    		Explosion(center,4)
+    		enginebreak = 2
+    		flame = -150
+    		PlaySound(bigsound[math.random(1,3)],enginepos,100)
+    		if enginebroken == false then
+    			SetInt("level.engines",GetInt("level.engines")-1, true)
+    			enginebroken = true
+    		end
+    	end
+    end
+    if enginebreak == 2 then --very, very bad things are happening
+    	if flame ~= 0 then
+    		flame = flame - 1
+    	end
+    	--first spawn fire
+    	ParticleReset()
+    	ParticleColor(1,0.6,0.3,0.1,0.1,0.1,"linear",0,0.5)
+    	ParticleEmissive(2,0,"linear",0,0.5)
+    	ParticleRadius(2.75+(flame/400),5,"linear",0.2,1)
+    	ParticleAlpha(1.0,0.0)
+    	ParticleCollide(0)
+    	ParticleGravity(0,-2)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),(flame/50)+1.5)
+    	--next is smoke
+    	ParticleReset()
+    	ParticleColor(0.16,0.15,0.15)
+    	ParticleRadius(3,5)
+    	ParticleAlpha(0.8,0.0,"linear",0.03,0.9)
+    	ParticleCollide(0)
+    	ParticleGravity(0,-2)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),(flame/20)+3.5)
+    elseif enginebreak == 1 then --bad things are sort of happening
+    	ParticleReset()
+    	ParticleColor(0.5,0.4,0.4)
+    	ParticleRadius(3,5)
+    	ParticleAlpha(0.3,0.0,"linear",0.03,0.9)
+    	ParticleCollide(0)
+    	ParticleGravity(0,-2)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),7)
+    else --engine is nominal
+    	ParticleReset()
+    	ParticleColor(0.9,0.9,0.9)
+    	ParticleRadius(3,10)
+    	if red ~= 0 then
+    		ParticleAlpha(0.1,0.0,"linear",0.03,0.9)
+    	else
+    		ParticleAlpha(0.3,0.0,"linear",0.03,0.9)
+    	end
+    	ParticleCollide(0)
+    	ParticleGravity(0,-2)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),20)
+    end
+    if red > 0 and enginebreak < 2 then --funny tomato juice in the engines
+    	SetInt("level.engines."..id..".red",red-1, true)
+
+    	ParticleReset()
+    	ParticleColor(0.4,0.2,0.2)
+    	ParticleRadius(3.1,5)
+    	ParticleAlpha(0.5,0.0,"linear",0.03,0.9)
+    	ParticleCollide(0)
+    	ParticleGravity(0,-2)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),7)
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\groundedEngine.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\groundedEngine.lua
+++ patched/main\Boeing 737\script\groundedEngine.lua
@@ -1,120 +1,4 @@
-function init()
-	joints = FindJoints("engine")
-	for j, joint in pairs(joints) do
-		SetJointMotor(joint, 20)
-	end
-	bodies = FindBodies() --gets all bodies under the script because those are all we need (the propellers)
-	enginepos = GetLocationTransform(FindLocation("emit")).pos
-	enginebreak = 0
-	enginebreakShape=FindShape("explosive")
-	localEnginepos = TransformToLocalPoint(GetBodyTransform(FindBody("boeing",true)),enginepos)
-	flame = 100
-	SetInt("level.engines",2)
-	enginebroken = false
-	smallsound = {}
-	for i=0,5 do
-		smallsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_small/"..i)
-	end
-	bigsound = {}
-	for i=0,3 do
-		bigsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_big/"..i)
-	end
-	engineLoop = LoadLoop("MOD/main/Boeing 737/snd/engine_exterior.ogg")
-end
-
-function tick(dt)
-	enginepos = TransformToParentPoint(GetBodyTransform(FindBody("boeing",true)),localEnginepos)
-	
-	local id = GetIntParam("id")
-	red = GetInt("level.engines."..id..".red")
-	
-	local ptrans = GetPlayerTransform()
-	for b, body in pairs(bodies) do
-		center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
-		voxels, broken, total = GetBodyVoxelCount(body)
-		local soundpos = VecLerp(ptrans.pos,center,0.1)
-		--DebugPrint(FindShape("explosive"))
-		if voxels == 0 or FindShape("explosive")==0 then --completely destroyed = no vfx
-			enginebreak = 2
-			flame = -150
-			if enginebroken == false then
-				PlaySound(bigsound[math.random(1,3)],enginepos,100)
-				SetInt("level.engines",GetInt("level.engines")-1)
-				enginebroken = true
-			end
-		end
-		if broken > 0 and enginebreak == 0 then
-			enginebreak = 1
-			PlaySound(smallsound[math.random(1,5)],soundpos,5)
-		elseif broken > 15 and enginebreak <= 1 then
-			enginebreak = 2
-			PlaySound(bigsound[math.random(1,3)],soundpos,100)
-			if enginebroken == false then
-				SetInt("level.engines",GetInt("level.engines")-1)
-				enginebroken = true
-			end
-		end
-		
-	end
-	if enginebreak == 2 then --very, very bad things are happening
-		if flame > 0 then
-			flame = flame - 1
-		end
-		--first spawn fire
-		ParticleReset()
-		ParticleColor(1,0.6,0.3,0.1,0.1,0.1,"linear",0,0.5)
-		ParticleEmissive(2,0,"linear",0,0.5)
-		ParticleRadius(3+(flame/400),5,"linear",0.2,1)
-		ParticleAlpha(1.0,0.0)
-		ParticleCollide(0)
-		ParticleGravity(4,9)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,4),(flame/50)+1.5)
-		--next is smoke
-		ParticleReset()
-		ParticleColor(0.16,0.15,0.15)
-		ParticleRadius(3,5)
-		ParticleAlpha(0.8,0.0,"linear",0.03,0.9)
-		ParticleCollide(0)
-		ParticleGravity(4,9)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,4),(flame/20)+3.5)
-	end
-	
-	if red > 0 and enginebreak < 2 then --funny tomato juice in the engines
-		SetInt("level.engines."..id..".red",red-1)
-		
-		ParticleReset()
-		ParticleColor(0.4,0.2,0.2)
-		ParticleRadius(2.1,4)
-		ParticleAlpha(0.2,0.0,"linear",0.03,0.9)
-		ParticleCollide(0)
-		ParticleGravity(0,-2)
-		SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,2),7)
-	end
-	
-	if enginebreak < 2 then
-		sceneBodies = FindBodies(nil,true)
-		for b=1,#sceneBodies do
-			bTrans = GetBodyTransform(sceneBodies[b])
-			if VecLength(VecMult(VecSub(bTrans.pos,enginepos),Vec(1,1,0.4))) < 5 then
-				ApplyBodyImpulse(sceneBodies[b],bTrans.pos,Vec(0,0,GetBodyMass(sceneBodies[b])))
-				--DrawBodyOutline(sceneBodies[b])
-			end
-		end
-		pTrans = GetPlayerTransform()
-		if VecLength(VecMult(VecSub(pTrans.pos,enginepos),Vec(1,1,0.4))) < 5 then
-			SetPlayerVelocity(VecAdd(GetPlayerVelocity(),Vec(0,0,1)))
-			if VecLength(VecSub(pTrans.pos,enginepos))<2.5 then
-				SetPlayerHealth(0)
-				SetPlayerVelocity(Vec(0,0,5))
-				pTrans.pos[3]= pTrans.pos[3]+3
-				SetPlayerTransform(pTrans)
-			end
-		end
-		--DebugPrint(engineLoop)
-		PlayLoop(engineLoop,enginepos,2/VecLength(VecSub(pTrans.pos,enginepos)))
-	end
-end
-
+#version 2
 function GetBodyVoxelCount(body)
 	local broken = 0
 	local voxels = 0
@@ -131,3 +15,126 @@
 function VecMult(a,b)
 	return Vec(a[1]*b[1],a[2]*b[2],a[3]*b[3])
 end
+
+function server.init()
+    joints = FindJoints("engine")
+    for j, joint in pairs(joints) do
+    	SetJointMotor(joint, 20)
+    end
+    bodies = FindBodies() --gets all bodies under the script because those are all we need (the propellers)
+    enginepos = GetLocationTransform(FindLocation("emit")).pos
+    enginebreak = 0
+    enginebreakShape=FindShape("explosive")
+    localEnginepos = TransformToLocalPoint(GetBodyTransform(FindBody("boeing",true)),enginepos)
+    flame = 100
+    SetInt("level.engines",2, true)
+    enginebroken = false
+    smallsound = {}
+    bigsound = {}
+    engineLoop = LoadLoop("MOD/main/Boeing 737/snd/engine_exterior.ogg")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        enginepos = TransformToParentPoint(GetBodyTransform(FindBody("boeing",true)),localEnginepos)
+        local id = GetIntParam("id")
+        red = GetInt("level.engines."..id..".red")
+        local ptrans = GetPlayerTransform(playerId)
+    end
+end
+
+function client.init()
+    for i=0,5 do
+    	smallsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_small/"..i)
+    end
+    for i=0,3 do
+    	bigsound[i] = LoadSound("MOD/main/Boeing 737/snd/fail_big/"..i)
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    for b, body in pairs(bodies) do
+    	center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
+    	voxels, broken, total = GetBodyVoxelCount(body)
+    	local soundpos = VecLerp(ptrans.pos,center,0.1)
+    	--DebugPrint(FindShape("explosive"))
+    	if voxels == 0 or FindShape("explosive")==0 then --completely destroyed = no vfx
+    		enginebreak = 2
+    		flame = -150
+    		if enginebroken == false then
+    			PlaySound(bigsound[math.random(1,3)],enginepos,100)
+    			SetInt("level.engines",GetInt("level.engines")-1, true)
+    			enginebroken = true
+    		end
+    	end
+    	if broken > 0 and enginebreak == 0 then
+    		enginebreak = 1
+    		PlaySound(smallsound[math.random(1,5)],soundpos,5)
+    	elseif broken > 15 and enginebreak <= 1 then
+    		enginebreak = 2
+    		PlaySound(bigsound[math.random(1,3)],soundpos,100)
+    		if enginebroken == false then
+    			SetInt("level.engines",GetInt("level.engines")-1, true)
+    			enginebroken = true
+    		end
+    	end
+
+    end
+    if enginebreak == 2 then --very, very bad things are happening
+    	if flame ~= 0 then
+    		flame = flame - 1
+    	end
+    	--first spawn fire
+    	ParticleReset()
+    	ParticleColor(1,0.6,0.3,0.1,0.1,0.1,"linear",0,0.5)
+    	ParticleEmissive(2,0,"linear",0,0.5)
+    	ParticleRadius(3+(flame/400),5,"linear",0.2,1)
+    	ParticleAlpha(1.0,0.0)
+    	ParticleCollide(0)
+    	ParticleGravity(4,9)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,4),(flame/50)+1.5)
+    	--next is smoke
+    	ParticleReset()
+    	ParticleColor(0.16,0.15,0.15)
+    	ParticleRadius(3,5)
+    	ParticleAlpha(0.8,0.0,"linear",0.03,0.9)
+    	ParticleCollide(0)
+    	ParticleGravity(4,9)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,4),(flame/20)+3.5)
+    end
+    if red > 0 and enginebreak < 2 then --funny tomato juice in the engines
+    	SetInt("level.engines."..id..".red",red-1, true)
+
+    	ParticleReset()
+    	ParticleColor(0.4,0.2,0.2)
+    	ParticleRadius(2.1,4)
+    	ParticleAlpha(0.2,0.0,"linear",0.03,0.9)
+    	ParticleCollide(0)
+    	ParticleGravity(0,-2)
+    	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,2),7)
+    end
+    if enginebreak < 2 then
+    	sceneBodies = FindBodies(nil,true)
+    	for b=1,#sceneBodies do
+    		bTrans = GetBodyTransform(sceneBodies[b])
+    		if VecLength(VecMult(VecSub(bTrans.pos,enginepos),Vec(1,1,0.4))) < 5 then
+    			ApplyBodyImpulse(sceneBodies[b],bTrans.pos,Vec(0,0,GetBodyMass(sceneBodies[b])))
+    			--DrawBodyOutline(sceneBodies[b])
+    		end
+    	end
+    	pTrans = GetPlayerTransform(playerId)
+    	if VecLength(VecMult(VecSub(pTrans.pos,enginepos),Vec(1,1,0.4))) < 5 then
+    		SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),Vec(0,0,1)))
+    		if VecLength(VecSub(pTrans.pos,enginepos))<2.5 then
+    			SetPlayerHealth(playerId, 0)
+    			SetPlayerVelocity(playerId, Vec(0,0,5))
+    			pTrans.pos[3]= pTrans.pos[3]+3
+    			SetPlayerTransform(playerId, pTrans)
+    		end
+    	end
+    	--DebugPrint(engineLoop)
+    	PlayLoop(engineLoop,enginepos,2/VecLength(VecSub(pTrans.pos,enginepos)))
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\landedAlarms.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\landedAlarms.lua
+++ patched/main\Boeing 737\script\landedAlarms.lua
@@ -1,59 +1,64 @@
-function init()
-	
-	alarm0 = LoadLoop("MOD/main/Boeing 737/snd/alarms/0.ogg")
-	alarm1 = LoadLoop("MOD/main/Boeing 737/snd/alarms/1.ogg")
-	firealarm = LoadLoop("MOD/main/Boeing 737/snd/alarms/737_fire_alarm.ogg")
-	firstalarms = FindShapes("alarm1",true)
-	secondalarms = FindShapes("alarm2",true)
-	alarmsActive = GetBoolParam("doAlarms",true)
-	timer = 0
-	local lightshapes = FindShapes("emergency",true)
-	for s, shape in pairs(lightshapes) do
-		SetShapeEmissiveScale(shape,0)
-	end
-	for s, shape in pairs(firstalarms) do
-		SetShapeEmissiveScale(shape,0)
-	end
-	for s, shape in pairs(secondalarms) do
-		SetShapeEmissiveScale(shape,0)
-	end
+#version 2
+function round(v)
+	return math.floor(v+0.5)
 end
 
-function tick(dt)
-	timer = timer + dt
-	--[[if alarmsActive then
-		PlayLoop(alarm0,GetShapeWorldTransform(firstalarms[1]).pos,0.2)
-		for s, shape in pairs(firstalarms) do
-			if IsShapeBroken(shape) then
-				alarmsActive = false
-			end
-			if math.sin(timer*30) > 0 then
-				SetShapeEmissiveScale(shape,1)
-			else
-				SetShapeEmissiveScale(shape,0)
-			end
-		end
-		
-	end --]]
-	if GetInt("level.engines") < 2 and alarmsActive then
-		PlayLoop(firealarm,GetShapeWorldTransform(secondalarms[1]).pos,0.6)
-		if IsShapeBroken(secondalarms[1]) then
-			alarmsActive = false
-		end
-	end
-	if GetInt("level.engines") < 1 and alarmsActive then
-		for s, shape in pairs(secondalarms) do
-			PlayLoop(alarm1,GetShapeWorldTransform(secondalarms[1]).pos,0.4)
-			SetShapeEmissiveScale(shape,(math.sin((timer+(s*0.2))*10)+0.7)*0.25)
-			
-			if IsShapeBroken(shape) then
-				alarmsActive = false
-			end
-		end
-	end
-
+function server.init()
+    alarm0 = LoadLoop("MOD/main/Boeing 737/snd/alarms/0.ogg")
+    alarm1 = LoadLoop("MOD/main/Boeing 737/snd/alarms/1.ogg")
+    firealarm = LoadLoop("MOD/main/Boeing 737/snd/alarms/737_fire_alarm.ogg")
+    firstalarms = FindShapes("alarm1",true)
+    secondalarms = FindShapes("alarm2",true)
+    alarmsActive = GetBoolParam("doAlarms",true)
+    timer = 0
+    local lightshapes = FindShapes("emergency",true)
+    for s, shape in pairs(lightshapes) do
+    	SetShapeEmissiveScale(shape,0)
+    end
+    for s, shape in pairs(firstalarms) do
+    	SetShapeEmissiveScale(shape,0)
+    end
+    for s, shape in pairs(secondalarms) do
+    	SetShapeEmissiveScale(shape,0)
+    end
 end
 
-function round(v)
-	return math.floor(v+0.5)
-end+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        timer = timer + dt
+        --[[if alarmsActive then
+        	for s, shape in pairs(firstalarms) do
+        		if IsShapeBroken(shape) then
+        			alarmsActive = false
+        		end
+        		if math.sin(timer*30) > 0 then
+        			SetShapeEmissiveScale(shape,1)
+        		else
+        			SetShapeEmissiveScale(shape,0)
+        		end
+        	end
+        end --]]
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    	PlayLoop(alarm0,GetShapeWorldTransform(firstalarms[1]).pos,0.2)
+    if GetInt("level.engines") < 2 and alarmsActive then
+    	PlayLoop(firealarm,GetShapeWorldTransform(secondalarms[1]).pos,0.6)
+    	if IsShapeBroken(secondalarms[1]) then
+    		alarmsActive = false
+    	end
+    end
+    if GetInt("level.engines") < 1 and alarmsActive then
+    	for s, shape in pairs(secondalarms) do
+    		PlayLoop(alarm1,GetShapeWorldTransform(secondalarms[1]).pos,0.4)
+    		SetShapeEmissiveScale(shape,(math.sin((timer+(s*0.2))*10)+0.7)*0.25)
+
+    		if IsShapeBroken(shape) then
+    			alarmsActive = false
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: main\Boeing 737\script\menuEngine.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\menuEngine.lua
+++ patched/main\Boeing 737\script\menuEngine.lua
@@ -1,23 +1,24 @@
-function init()
-	joints = FindJoints("engine")
-	for j, joint in pairs(joints) do
-		SetJointMotor(joint, 20)
-	end
-	enginepos = GetLocationTransform(FindLocation("emit")).pos
-end
-
-function tick(dt)
-	
-	ParticleReset()
-	ParticleColor(0.9,0.9,0.9)
-	ParticleRadius(3,10)
-	ParticleAlpha(0.3,0.0,"linear",0.03,0.9)
-	ParticleCollide(0)
-	ParticleGravity(0,-2)
-	SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),20)
-	
-end
-
+#version 2
 function VecMult(a,b)
 	return Vec(a[1]*b[1],a[2]*b[2],a[3]*b[3])
 end
+
+function server.init()
+    joints = FindJoints("engine")
+    for j, joint in pairs(joints) do
+    	SetJointMotor(joint, 20)
+    end
+    enginepos = GetLocationTransform(FindLocation("emit")).pos
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    ParticleReset()
+    ParticleColor(0.9,0.9,0.9)
+    ParticleRadius(3,10)
+    ParticleAlpha(0.3,0.0,"linear",0.03,0.9)
+    ParticleCollide(0)
+    ParticleGravity(0,-2)
+    SpawnParticle(enginepos,Vec(math.random()-0.5,math.random()-0.5,30),20)
+end
+

```

---

# Migration Report: main\Boeing 737\script\seating.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Boeing 737\script\seating.lua
+++ patched/main\Boeing 737\script\seating.lua
@@ -1,46 +1,10 @@
-function init()
-	ragdolls = FindShapes("ragdoll",true)
-	table.sort(ragdolls,ragdollSort)
-	
-	for i=1, #ragdolls do
-		if not GetBool("savegame.mod.plane_seat."..i) then
-			bodies = GetFullRagdoll(ragdolls[i])
-			for b=1,#bodies do
-				Delete(bodies[b])
-			end
-		end
-	end
-end
-
-function tick(dt)
-	local engines = FindLocations("emit",true) --engines can chop up ragdolls
-	for i=1, #ragdolls do
-		pos = GetShapeWorldTransform(ragdolls[i]).pos
-		for e=1, #engines do
-			eTrans = GetLocationTransform(engines[e])
-			if VecLength(VecSub(pos,eTrans.pos)) < 2.5 then
-				if eTrans.pos[1] > 0 then
-					SetInt("level.engines.1.red",100)
-				else
-					SetInt("level.engines.2.red",100)
-				end
-				
-				SetBodyTransform(GetShapeBody(ragdolls[i]),Transform(Vec(0,5,0),Quat()))
-				bodies = GetFullRagdoll(ragdolls[i])
-				for b=1,#bodies do
-					Delete(bodies[b])
-				end
-			end
-		end
-	end
-end
-
+#version 2
 function _draw()
 	UiFont("bold.ttf",24)
 	UiColor(1,0,0)
 	for i=1, #ragdolls do
 		local x, y, dist = UiWorldToPixel(GetShapeWorldTransform(ragdolls[i]).pos)
-		if dist > 0 then
+		if dist ~= 0 then
 			UiTranslate(x, y)
 			UiText(i)
 		end
@@ -91,3 +55,42 @@
 		return aPos[3] < bPos[3]
 	end
 end
+
+function server.init()
+    ragdolls = FindShapes("ragdoll",true)
+    table.sort(ragdolls,ragdollSort)
+    for i=1, #ragdolls do
+    	if not GetBool("savegame.mod.plane_seat."..i) then
+    		bodies = GetFullRagdoll(ragdolls[i])
+    		for b=1,#bodies do
+    			Delete(bodies[b])
+    		end
+    	end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local engines = FindLocations("emit",true) --engines can chop up ragdolls
+        for i=1, #ragdolls do
+        	pos = GetShapeWorldTransform(ragdolls[i]).pos
+        	for e=1, #engines do
+        		eTrans = GetLocationTransform(engines[e])
+        		if VecLength(VecSub(pos,eTrans.pos)) < 2.5 then
+        			if eTrans.pos[1] > 0 then
+        				SetInt("level.engines.1.red",100, true)
+        			else
+        				SetInt("level.engines.2.red",100, true)
+        			end
+
+        			SetBodyTransform(GetShapeBody(ragdolls[i]),Transform(Vec(0,5,0),Quat()))
+        			bodies = GetFullRagdoll(ragdolls[i])
+        			for b=1,#bodies do
+        				Delete(bodies[b])
+        			end
+        		end
+        	end
+        end
+    end
+end
+

```

---

# Migration Report: main\Cessna 172\scripts\engineprops.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172\scripts\engineprops.lua
+++ patched/main\Cessna 172\scripts\engineprops.lua
@@ -1,14 +1,13 @@
-function init()
+#version 2
+function server.init()
+    blades = FindJoints("engine", true)
+    if GetPlayerVehicle(playerId) ~= 0 then
 
-	blades = FindJoints("engine", true)
+    	for i = 1, #blades do
+    		local blade = blades[i]
+    		SetJointMotor(blade, 30)
+    	end
 
-	if GetPlayerVehicle() ~= 0 then
+    end
+end
 
-		for i = 1, #blades do
-			local blade = blades[i]
-			SetJointMotor(blade, 30)
-		end
-
-	end
-
-end
```

---

# Migration Report: main\Cessna 172\scripts\lights.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172\scripts\lights.lua
+++ patched/main\Cessna 172\scripts\lights.lua
@@ -1,87 +1,83 @@
-function init()
-	btn_navlight = FindShape("nl", true)
-	btn_cabinlight = FindShape("cl", true)
-	btn_instrumentlight = FindShape("ilb", true)
-	
-	light_instrument = FindLight("instrument", true)
-	light_beacon = FindLight("beacon", true)
-	light_cabin = FindLights("cabin", true)
-	light_nav = FindLights("navlight", true)
-	
-	SetTag(btn_navlight, "interact", "Navigation lights")
-	SetTag(btn_cabinlight, "interact", "Cabin lights")
-	SetTag(btn_instrumentlight, "interact", "Instrument light")
-	
-	for i=1,#light_cabin do
-		SetLightEnabled(light_cabin[i], false)
-	end
-	
-	for i=1,#light_nav do
-		SetLightEnabled(light_nav[i], false)
-	end
-	
-	SetLightEnabled(light_instrument, false)
-	SetLightEnabled(light_beacon, false)
-	
-	beacon = false
-	timer = 0
+#version 2
+function server.init()
+    btn_navlight = FindShape("nl", true)
+    btn_cabinlight = FindShape("cl", true)
+    btn_instrumentlight = FindShape("ilb", true)
+    light_instrument = FindLight("instrument", true)
+    light_beacon = FindLight("beacon", true)
+    light_cabin = FindLights("cabin", true)
+    light_nav = FindLights("navlight", true)
+    SetTag(btn_navlight, "interact", "Navigation lights")
+    SetTag(btn_cabinlight, "interact", "Cabin lights")
+    SetTag(btn_instrumentlight, "interact", "Instrument light")
+    for i=1,#light_cabin do
+    	SetLightEnabled(light_cabin[i], false)
+    end
+    for i=1,#light_nav do
+    	SetLightEnabled(light_nav[i], false)
+    end
+    SetLightEnabled(light_instrument, false)
+    SetLightEnabled(light_beacon, false)
+    beacon = false
+    timer = 0
 end
 
-function update(dt)
-	
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if beacon then
+        timer = timer + 1
+        	if timer == 80 then
+        		timer = timer * 0 + 1
+        	end
+        	if timer > 0 and timer < 10 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 10 and timer < 20 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        	if timer >= 20 and timer < 30 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 30 and timer < 80 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        end
+    end
+end
 
-	
-	if GetPlayerInteractShape() == btn_cabinlight and InputPressed("interact") then
-		for i=1,#light_cabin do
-			if IsLightActive(light_cabin[i]) == false then
-				SetLightEnabled(light_cabin[i], true)
-			else
-				SetLightEnabled(light_cabin[i], false)
-			end
-		end
-	end
-	
-	if GetPlayerInteractShape() == btn_navlight and InputPressed("interact") then
-		if not beacon then
-			beacon = true
-		else
-			beacon = false
-		end
-		
-		for i=1,#light_nav do
-			if IsLightActive(light_nav[i]) == false then
-				SetLightEnabled(light_nav[i], true)
-			else
-				SetLightEnabled(light_nav[i], false)
-			end
-		end
-		
-	end
-	
-	if GetPlayerInteractShape() == btn_instrumentlight and InputPressed("interact") then
-		if IsLightActive(light_instrument) == false then
-			SetLightEnabled(light_instrument, true)
-		else
-			SetLightEnabled(light_instrument, false)
-		end
-	end
-	
-	if beacon then
-	timer = timer + 1
-		if timer == 80 then
-			timer = timer * 0 + 1
-		end
-		if timer > 0 and timer < 10 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 10 and timer < 20 then
-			SetLightEnabled(light_beacon, false)
-		end
-		if timer >= 20 and timer < 30 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 30 and timer < 80 then
-			SetLightEnabled(light_beacon, false)
-		end
-	end
-end+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == btn_cabinlight and InputPressed("interact") then
+    	for i=1,#light_cabin do
+    		if IsLightActive(light_cabin[i]) == false then
+    			SetLightEnabled(light_cabin[i], true)
+    		else
+    			SetLightEnabled(light_cabin[i], false)
+    		end
+    	end
+    end
+    if GetPlayerInteractShape(playerId) == btn_navlight and InputPressed("interact") then
+    	if not beacon then
+    		beacon = true
+    	else
+    		beacon = false
+    	end
+
+    	for i=1,#light_nav do
+    		if IsLightActive(light_nav[i]) == false then
+    			SetLightEnabled(light_nav[i], true)
+    		else
+    			SetLightEnabled(light_nav[i], false)
+    		end
+    	end
+
+    end
+    if GetPlayerInteractShape(playerId) == btn_instrumentlight and InputPressed("interact") then
+    	if IsLightActive(light_instrument) == false then
+    		SetLightEnabled(light_instrument, true)
+    	else
+    		SetLightEnabled(light_instrument, false)
+    	end
+    end
+end
+

```

---

# Migration Report: main\CRJ-200\script\engineprops.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\CRJ-200\script\engineprops.lua
+++ patched/main\CRJ-200\script\engineprops.lua
@@ -1,14 +1,13 @@
-function init()
+#version 2
+function server.init()
+    blades = FindJoints("engine", true)
+    if GetPlayerVehicle(playerId) ~= 0 then
 
-	blades = FindJoints("engine", true)
+    	for i = 1, #blades do
+    		local blade = blades[i]
+    		SetJointMotor(blade, 30)
+    	end
 
-	if GetPlayerVehicle() ~= 0 then
+    end
+end
 
-		for i = 1, #blades do
-			local blade = blades[i]
-			SetJointMotor(blade, 30)
-		end
-
-	end
-
-end
```

---

# Migration Report: main\Decompression.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Decompression.lua
+++ patched/main\Decompression.lua
@@ -1,165 +1,172 @@
-function init()
-	probe = FindLocation("probe")
-	pos = GetLocationTransform(probe).pos
-	resolution = GetFloatParam("resolution",24)
-	pressure = 100
-	offset = 0
-	activePosList = {} --so that each hole can be saved and constantly checked
-	activeDirList = {}
-	activeTimeList = {}
-	activated = false --changes when everything activates
-	windloop = LoadLoop("/Boeing 737/snd/plane_wind.ogg")
-	alarm0 = LoadLoop("/Boeing 737/snd/alarms/0.ogg")
-	alarm1 = LoadLoop("/Boeing 737/snd/alarms/1.ogg")
-	firealarm = LoadLoop("/Boeing 737/snd/alarms/737_fire_alarm.ogg")
-	firstalarms = FindShapes("alarm1",true)
-	secondalarms = FindShapes("alarm2",true)
-	alarmsActive = GetBoolParam("doAlarms",true)
-	losePressure = not GetBool("savegame.mod.cabin.depressurize_inf",false)
-	doPressure = GetBool("savegame.mod.cabin.depressurize",true)
-	timer = 0
-	local lightshapes = FindShapes("emergency",true)
-	for s, shape in pairs(lightshapes) do
-		SetShapeEmissiveScale(shape,0)
-	end
-	for s, shape in pairs(firstalarms) do
-		SetShapeEmissiveScale(shape,0)
-	end
-	for s, shape in pairs(secondalarms) do
-		SetShapeEmissiveScale(shape,0)
-	end
+#version 2
+function round(v)
+	return math.floor(v+0.5)
 end
 
-function tick(dt)
-	timer = timer + dt
-	if activated and alarmsActive then
-		PlayLoop(alarm0,GetShapeWorldTransform(firstalarms[1]).pos,0.2)
-		for s, shape in pairs(firstalarms) do
-			if IsShapeBroken(shape) then
-				alarmsActive = false
-			end
-			if math.sin(timer*30) > 0 then
-				SetShapeEmissiveScale(shape,1)
-			else
-				SetShapeEmissiveScale(shape,0)
-			end
-		end
-		
-	end
-	if GetInt("level.engines") < 2 and alarmsActive then
-		PlayLoop(firealarm,GetShapeWorldTransform(secondalarms[1]).pos,0.6)
-		if IsShapeBroken(secondalarms[1]) then
-			alarmsActive = false
-		end
-	end
-	if GetInt("level.engines") < 1 and alarmsActive then
-		for s, shape in pairs(secondalarms) do
-			PlayLoop(alarm1,GetShapeWorldTransform(secondalarms[1]).pos,0.4)
-			SetShapeEmissiveScale(shape,(math.sin((timer+(s*0.2))*10)+0.7)*0.25)
-			
-			if IsShapeBroken(shape) then
-				alarmsActive = false
-			end
-		end
-	end
-	if pressure > 0 and doPressure then
-		i = 0 --raycast counter
-		offset = offset + 2
-		if offset > 84 then offset = 0 end
-		local checkpos = VecCopy(pos)
-		checkpos[3] = checkpos[3] - offset
-		for r=0,resolution do
-			local quat = QuatEuler(0,0,r*360/resolution)
-			local dir = TransformToParentPoint(Transform(Vec(0,0,0),quat),Vec(1,0,0))
-			
-			if activePosList[i] ~= checkpos and activeDirList[i] ~= dir then
-				--DebugLine(checkpos,VecAdd(checkpos,dir),0,0,1) --debug the current checked position
-				i = i + 1
-				hit, dist = QueryRaycast(checkpos,dir,10)
-				if not hit then
-					activePosList[i] = checkpos
-					activeDirList[i] = dir
-					activeTimeList[i] = 0
-				end
-			end
-		end
-		for p in pairs(activePosList) do
-			local pos = activePosList[p]
-			local dir = activeDirList[p]
-			--DebugLine(pos,VecAdd(pos,dir),1,0,0) --debug active holes
-			ParticleReset()
-			ParticleColor(0.9,0.9,0.9)
-			ParticleRadius(3)
-			ParticleAlpha(0.85,0.0)
-			ParticleCollide(0)
-			if math.random(1,10) > 8 then
-				local velocity = math.random(-6,6)
-				SpawnParticle(VecAdd(pos,Vec(0,0,math.random(-5,5))),Vec(0,0,velocity),4)
-			end
-			
-			pressure = pressure - 0.5
-			
-			local holepos = VecAdd(pos,VecScale(dir,7))
-			if holepos[3] < -44 then
-				holepos[3] = -50
-			end
-			PlayLoop(windloop,holepos,pressure/25)
-			bodies = QueryAabbBodies(VecSub(pos,Vec(6,6,20)),VecAdd(pos,Vec(6,6,20)))
-			for b, body in pairs(bodies) do
-				QueryRejectBody(body)
-				local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
-				if pressure > 99 then --first two frames are more violently forceful
-					ApplyBodyImpulse(body,center,VecScale(VecSub(holepos,center),25))
-				else
-					ApplyBodyImpulse(body,center,VecScale(VecSub(holepos,center),5))
-				end
-			end
-			local ptrans = GetPlayerTransform()
-			local vec = VecSub(holepos,ptrans.pos)
-			if VecLength(vec) < 20 then
-				if pressure > 99 then --first two frames are more violently forceful
-					SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(dir,2)))
-				else
-					SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(dir,0.5)))
-				end
-			end
-			hit, dist = QueryRaycast(pos,dir,10)
-			if hit then
-				activeTimeList[p] = activeTimeList[p] + dt
-				if activeTimeList[p] > 5 then
-					activePosList[p] = nil
-					activeDirList[p] = nil
-				end
-			end
-		end
-	end
-	if pressure < 100 then
-		SetBool("level.depressurized",true)
-		activated = true
-		if pressure > 80 then
-			local masks = FindShapes("mask",true)
-			for m, mask in pairs(masks) do
-				local body = GetShapeBody(mask)
-				local btrans = GetBodyTransform(body)
-				SetBodyVelocity(body,Vec(0,-1,0))
-			end
-		end
-		local lightshapes = FindShapes("pressurestop",true)
-		for s, shape in pairs(lightshapes) do
-			SetShapeEmissiveScale(shape,0)
-		end
-		lightshapes = FindShapes("emergency",true)
-		for s, shape in pairs(lightshapes) do
-			SetShapeEmissiveScale(shape,1)
-		end
-		if not losePressure and pressure < 50 then
-			pressure = 50
-		end
-	end
-	if pressure < 0 then pressure = 0 end
-
+function server.init()
+    probe = FindLocation("probe")
+    pos = GetLocationTransform(probe).pos
+    resolution = GetFloatParam("resolution",24)
+    pressure = 100
+    offset = 0
+    activePosList = {} --so that each hole can be saved and constantly checked
+    activeDirList = {}
+    activeTimeList = {}
+    activated = false --changes when everything activates
+    windloop = LoadLoop("/Boeing 737/snd/plane_wind.ogg")
+    alarm0 = LoadLoop("/Boeing 737/snd/alarms/0.ogg")
+    alarm1 = LoadLoop("/Boeing 737/snd/alarms/1.ogg")
+    firealarm = LoadLoop("/Boeing 737/snd/alarms/737_fire_alarm.ogg")
+    firstalarms = FindShapes("alarm1",true)
+    secondalarms = FindShapes("alarm2",true)
+    alarmsActive = GetBoolParam("doAlarms",true)
+    losePressure = not GetBool("savegame.mod.cabin.depressurize_inf",false)
+    doPressure = GetBool("savegame.mod.cabin.depressurize",true)
+    timer = 0
+    local lightshapes = FindShapes("emergency",true)
+    for s, shape in pairs(lightshapes) do
+    	SetShapeEmissiveScale(shape,0)
+    end
+    for s, shape in pairs(firstalarms) do
+    	SetShapeEmissiveScale(shape,0)
+    end
+    for s, shape in pairs(secondalarms) do
+    	SetShapeEmissiveScale(shape,0)
+    end
 end
 
-function round(v)
-	return math.floor(v+0.5)
-end+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        timer = timer + dt
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if activated and alarmsActive then
+    	PlayLoop(alarm0,GetShapeWorldTransform(firstalarms[1]).pos,0.2)
+    	for s, shape in pairs(firstalarms) do
+    		if IsShapeBroken(shape) then
+    			alarmsActive = false
+    		end
+    		if math.sin(timer*30) > 0 then
+    			SetShapeEmissiveScale(shape,1)
+    		else
+    			SetShapeEmissiveScale(shape,0)
+    		end
+    	end
+
+    end
+    if GetInt("level.engines") < 2 and alarmsActive then
+    	PlayLoop(firealarm,GetShapeWorldTransform(secondalarms[1]).pos,0.6)
+    	if IsShapeBroken(secondalarms[1]) then
+    		alarmsActive = false
+    	end
+    end
+    if GetInt("level.engines") < 1 and alarmsActive then
+    	for s, shape in pairs(secondalarms) do
+    		PlayLoop(alarm1,GetShapeWorldTransform(secondalarms[1]).pos,0.4)
+    		SetShapeEmissiveScale(shape,(math.sin((timer+(s*0.2))*10)+0.7)*0.25)
+
+    		if IsShapeBroken(shape) then
+    			alarmsActive = false
+    		end
+    	end
+    end
+    if pressure > 0 and doPressure then
+    	i = 0 --raycast counter
+    	offset = offset + 2
+    	if offset > 84 then offset = 0 end
+    	local checkpos = VecCopy(pos)
+    	checkpos[3] = checkpos[3] - offset
+    	for r=0,resolution do
+    		local quat = QuatEuler(0,0,r*360/resolution)
+    		local dir = TransformToParentPoint(Transform(Vec(0,0,0),quat),Vec(1,0,0))
+
+    		if activePosList[i] ~= checkpos and activeDirList[i] ~= dir then
+    			--DebugLine(checkpos,VecAdd(checkpos,dir),0,0,1) --debug the current checked position
+    			i = i + 1
+    			hit, dist = QueryRaycast(checkpos,dir,10)
+    			if not hit then
+    				activePosList[i] = checkpos
+    				activeDirList[i] = dir
+    				activeTimeList[i] = 0
+    			end
+    		end
+    	end
+    	for p in pairs(activePosList) do
+    		local pos = activePosList[p]
+    		local dir = activeDirList[p]
+    		--DebugLine(pos,VecAdd(pos,dir),1,0,0) --debug active holes
+    		ParticleReset()
+    		ParticleColor(0.9,0.9,0.9)
+    		ParticleRadius(3)
+    		ParticleAlpha(0.85,0.0)
+    		ParticleCollide(0)
+    		if math.random(1,10) > 8 then
+    			local velocity = math.random(-6,6)
+    			SpawnParticle(VecAdd(pos,Vec(0,0,math.random(-5,5))),Vec(0,0,velocity),4)
+    		end
+
+    		pressure = pressure - 0.5
+
+    		local holepos = VecAdd(pos,VecScale(dir,7))
+    		if holepos[3] < -44 then
+    			holepos[3] = -50
+    		end
+    		PlayLoop(windloop,holepos,pressure/25)
+    		bodies = QueryAabbBodies(VecSub(pos,Vec(6,6,20)),VecAdd(pos,Vec(6,6,20)))
+    		for b, body in pairs(bodies) do
+    			QueryRejectBody(body)
+    			local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
+    			if pressure > 99 then --first two frames are more violently forceful
+    				ApplyBodyImpulse(body,center,VecScale(VecSub(holepos,center),25))
+    			else
+    				ApplyBodyImpulse(body,center,VecScale(VecSub(holepos,center),5))
+    			end
+    		end
+    		local ptrans = GetPlayerTransform(playerId)
+    		local vec = VecSub(holepos,ptrans.pos)
+    		if VecLength(vec) < 20 then
+    			if pressure > 99 then --first two frames are more violently forceful
+    				SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(dir,2)))
+    			else
+    				SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(dir,0.5)))
+    			end
+    		end
+    		hit, dist = QueryRaycast(pos,dir,10)
+    		if hit then
+    			activeTimeList[p] = activeTimeList[p] + dt
+    			if activeTimeList[p] > 5 then
+    				activePosList[p] = nil
+    				activeDirList[p] = nil
+    			end
+    		end
+    	end
+    end
+    if pressure < 100 then
+    	SetBool("level.depressurized",true, true)
+    	activated = true
+    	if pressure > 80 then
+    		local masks = FindShapes("mask",true)
+    		for m, mask in pairs(masks) do
+    			local body = GetShapeBody(mask)
+    			local btrans = GetBodyTransform(body)
+    			SetBodyVelocity(body,Vec(0,-1,0))
+    		end
+    	end
+    	local lightshapes = FindShapes("pressurestop",true)
+    	for s, shape in pairs(lightshapes) do
+    		SetShapeEmissiveScale(shape,0)
+    	end
+    	lightshapes = FindShapes("emergency",true)
+    	for s, shape in pairs(lightshapes) do
+    		SetShapeEmissiveScale(shape,1)
+    	end
+    	if not losePressure and pressure < 50 then
+    		pressure = 50
+    	end
+    end
+    if pressure < 0 then pressure = 0 end
+end
+

```

---

# Migration Report: main\Decompression_Cargo.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Decompression_Cargo.lua
+++ patched/main\Decompression_Cargo.lua
@@ -1,149 +1,146 @@
-function init()
-	probe = FindLocation("probe")
-	pos = GetLocationTransform(probe).pos
-	resolution = GetFloatParam("resolution",24)
-	pressure = 100
-	offset = 0
-	activePosList = {} --so that each hole can be saved and constantly checked
-	activeDirList = {}
-	activeTimeList = {}
-	activated = false --changes when everything activates
-	windloop = LoadLoop("/Boeing 737/snd/plane_wind.ogg")
-	--alarm0 = LoadLoop("/Boeing 737/snd/alarms/0.ogg")
-	--alarm1 = LoadLoop("/Boeing 737/snd/alarms/1.ogg")
-	--firealarm = LoadLoop("/Boeing 737/snd/alarms/737_fire_alarm.ogg")
-	--firstalarms = FindShapes("alarm1",true)
-	--secondalarms = FindShapes("alarm2",true)
-	timer = 0
-	--local lightshapes = FindShapes("emergency",true)
-	--for s, shape in pairs(lightshapes) do
-	--	SetShapeEmissiveScale(shape,0)
-	--end
-	--for s, shape in pairs(firstalarms) do
-	--	SetShapeEmissiveScale(shape,0)
-	--end
-	--for s, shape in pairs(secondalarms) do
-	--	SetShapeEmissiveScale(shape,0)
-	--end
+#version 2
+function round(v)
+	return math.floor(v+0.5)
 end
 
-function tick(dt)
-	timer = timer + dt
-	--if activated then
-		--PlayLoop(alarm0,GetShapeWorldTransform(firstalarms[1]).pos,0.2)
-		--for s, shape in pairs(firstalarms) do
-		--	if math.sin(timer*30) > 0 then
-		--		SetShapeEmissiveScale(shape,1)
-		--	else
-		--		SetShapeEmissiveScale(shape,0)
-		--	end
-		--end
-		
-	--end
-	--if GetInt("level.engines") < 2 then
-	--	PlayLoop(firealarm,GetShapeWorldTransform(secondalarms[1]).pos,0.6)
-	--end
-	--if GetInt("level.engines") < 1 then
-	--	for s, shape in pairs(secondalarms) do
-	--		PlayLoop(alarm1,GetShapeWorldTransform(secondalarms[1]).pos,0.4)
-	--		SetShapeEmissiveScale(shape,(math.sin((timer+(s*0.2))*10)+0.7)*0.25)
-	--	end
-	--end
-	if pressure > 0 then
-		i = 0 --raycast counter
-		offset = offset + 0.2
-		if offset > 15.6 then offset = 0 end
-		local checkpos = VecCopy(pos)
-		checkpos[3] = checkpos[3] - offset
-		for r=0,resolution do
-			local quat = QuatEuler(0,0,(r*180/resolution)+180)
-			local dir = TransformToParentPoint(Transform(Vec(0,0,0),quat),Vec(1,0,0))
-			
-			if activePosList[i] ~= checkpos and activeDirList[i] ~= dir then
-				--DebugLine(checkpos,VecAdd(checkpos,dir),0,0,1) --debug the current checked position
-				ignore = FindShapes()
-				--DebugPrint(#ignore)
-				for s, shape in pairs(ignore) do
-					QueryRejectShape(shape)
-				end
-				i = i + 1
-				hit, dist = QueryRaycast(checkpos,dir,10)
-				if not hit then
-					activePosList[i] = checkpos
-					activeDirList[i] = dir
-					activeTimeList[i] = 0
-				end
-			end
-		end
-		for p in pairs(activePosList) do
-			local pos = activePosList[p]
-			local dir = activeDirList[p]
-			--DebugLine(pos,VecAdd(pos,dir),1,0,0) --debug active holes
-			ParticleReset()
-			ParticleColor(0.9,0.9,0.9)
-			ParticleRadius(2)
-			ParticleAlpha(0.7,0.0)
-			ParticleCollide(0)
-			if math.random(1,10) > 8 then
-				local velocity = math.random(-2,2)
-				SpawnParticle(VecAdd(pos,Vec(0,-0.5,0)),Vec(0,0,velocity),7)
-			end
-			pressure = pressure - 0.25
-			local holepos = VecAdd(pos,VecScale(dir,3))
-			if pressure >= 95 then
-				MakeHole(holepos,1,1,1)
-			end
-			PlayLoop(windloop,holepos,pressure/25)
-			bodies = QueryAabbBodies(VecSub(pos,Vec(3,1.5,5)),VecAdd(pos,Vec(3,0.1,10)))
-			for b, body in pairs(bodies) do
-				QueryRejectBody(body)
-				if not HasTag(body,"noSmallDepressurize") then
-					local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
-					ApplyBodyImpulse(body,center,VecScale(VecSub(holepos,center),300))
-				end
-			end
-			local ptrans = GetPlayerTransform()
-			local vec = VecSub(holepos,ptrans.pos)
-			if VecLength(vec) < 20 then
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),VecScale(dir,0.5)))
-			end
-			hit, dist = QueryRaycast(pos,dir,10)
-			if hit then
-				activeTimeList[p] = activeTimeList[p] + dt
-				if activeTimeList[p] > 5 then
-					activePosList[p] = nil
-					activeDirList[p] = nil
-				end
-			end
-		end
-	end
-	if pressure < 100 then
-		--SetBool("level.depressurized",true)
-		activated = true
-		--if pressure > 80 then
-		--	local masks = FindShapes("mask",true)
-		--	for m, mask in pairs(masks) do
-		--		local body = GetShapeBody(mask)
-		--		local btrans = GetBodyTransform(body)
-		--		SetBodyVelocity(body,Vec(0,-1,0))
-		--	end
-		--end
-		--local lightshapes = FindShapes("pressurestop",true)
-		--for s, shape in pairs(lightshapes) do
-		--	SetShapeEmissiveScale(shape,0)
-		--end
-		--lightshapes = FindShapes("emergency",true)
-		--for s, shape in pairs(lightshapes) do
-		--	SetShapeEmissiveScale(shape,1)
-		--end
-	end
-	if pressure < 0 then pressure = 0 end
-	--SetString("hud.notification",round(pressure).."% pressure")
-	if GetBool("level.depressurized") then
-		pressure = 0 --when the main cabin is depressurized, so is the cargo hold
-	end
+function server.init()
+    probe = FindLocation("probe")
+    pos = GetLocationTransform(probe).pos
+    resolution = GetFloatParam("resolution",24)
+    pressure = 100
+    offset = 0
+    activePosList = {} --so that each hole can be saved and constantly checked
+    activeDirList = {}
+    activeTimeList = {}
+    activated = false --changes when everything activates
+    windloop = LoadLoop("/Boeing 737/snd/plane_wind.ogg")
+    --alarm0 = LoadLoop("/Boeing 737/snd/alarms/0.ogg")
+    --alarm1 = LoadLoop("/Boeing 737/snd/alarms/1.ogg")
+    --firealarm = LoadLoop("/Boeing 737/snd/alarms/737_fire_alarm.ogg")
+    --firstalarms = FindShapes("alarm1",true)
+    --secondalarms = FindShapes("alarm2",true)
+    timer = 0
 end
 
-function round(v)
-	return math.floor(v+0.5)
-end+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        timer = timer + dt
+        --if activated then
+        	--PlayLoop(alarm0,GetShapeWorldTransform(firstalarms[1]).pos,0.2)
+        	--for s, shape in pairs(firstalarms) do
+        	--	if math.sin(timer*30) > 0 then
+        	--		SetShapeEmissiveScale(shape,1)
+        	--	else
+        	--		SetShapeEmissiveScale(shape,0)
+        	--	end
+        	--end
+        --end
+        --if GetInt("level.engines") < 2 then
+        --	PlayLoop(firealarm,GetShapeWorldTransform(secondalarms[1]).pos,0.6)
+        --end
+        --if GetInt("level.engines") < 1 then
+        --	for s, shape in pairs(secondalarms) do
+        --		PlayLoop(alarm1,GetShapeWorldTransform(secondalarms[1]).pos,0.4)
+        --		SetShapeEmissiveScale(shape,(math.sin((timer+(s*0.2))*10)+0.7)*0.25)
+        --	end
+        --end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if pressure ~= 0 then
+    	i = 0 --raycast counter
+    	offset = offset + 0.2
+    	if offset > 15.6 then offset = 0 end
+    	local checkpos = VecCopy(pos)
+    	checkpos[3] = checkpos[3] - offset
+    	for r=0,resolution do
+    		local quat = QuatEuler(0,0,(r*180/resolution)+180)
+    		local dir = TransformToParentPoint(Transform(Vec(0,0,0),quat),Vec(1,0,0))
+
+    		if activePosList[i] ~= checkpos and activeDirList[i] ~= dir then
+    			--DebugLine(checkpos,VecAdd(checkpos,dir),0,0,1) --debug the current checked position
+    			ignore = FindShapes()
+    			--DebugPrint(#ignore)
+    			for s, shape in pairs(ignore) do
+    				QueryRejectShape(shape)
+    			end
+    			i = i + 1
+    			hit, dist = QueryRaycast(checkpos,dir,10)
+    			if not hit then
+    				activePosList[i] = checkpos
+    				activeDirList[i] = dir
+    				activeTimeList[i] = 0
+    			end
+    		end
+    	end
+    	for p in pairs(activePosList) do
+    		local pos = activePosList[p]
+    		local dir = activeDirList[p]
+    		--DebugLine(pos,VecAdd(pos,dir),1,0,0) --debug active holes
+    		ParticleReset()
+    		ParticleColor(0.9,0.9,0.9)
+    		ParticleRadius(2)
+    		ParticleAlpha(0.7,0.0)
+    		ParticleCollide(0)
+    		if math.random(1,10) > 8 then
+    			local velocity = math.random(-2,2)
+    			SpawnParticle(VecAdd(pos,Vec(0,-0.5,0)),Vec(0,0,velocity),7)
+    		end
+    		pressure = pressure - 0.25
+    		local holepos = VecAdd(pos,VecScale(dir,3))
+    		if pressure >= 95 then
+    			MakeHole(holepos,1,1,1)
+    		end
+    		PlayLoop(windloop,holepos,pressure/25)
+    		bodies = QueryAabbBodies(VecSub(pos,Vec(3,1.5,5)),VecAdd(pos,Vec(3,0.1,10)))
+    		for b, body in pairs(bodies) do
+    			QueryRejectBody(body)
+    			if not HasTag(body,"noSmallDepressurize") then
+    				local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
+    				ApplyBodyImpulse(body,center,VecScale(VecSub(holepos,center),300))
+    			end
+    		end
+    		local ptrans = GetPlayerTransform(playerId)
+    		local vec = VecSub(holepos,ptrans.pos)
+    		if VecLength(vec) < 20 then
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),VecScale(dir,0.5)))
+    		end
+    		hit, dist = QueryRaycast(pos,dir,10)
+    		if hit then
+    			activeTimeList[p] = activeTimeList[p] + dt
+    			if activeTimeList[p] > 5 then
+    				activePosList[p] = nil
+    				activeDirList[p] = nil
+    			end
+    		end
+    	end
+    end
+    if pressure < 100 then
+    	--SetBool("level.depressurized",true, true)
+    	activated = true
+    	--if pressure > 80 then
+    	--	local masks = FindShapes("mask",true)
+    	--	for m, mask in pairs(masks) do
+    	--		local body = GetShapeBody(mask)
+    	--		local btrans = GetBodyTransform(body)
+    	--		SetBodyVelocity(body,Vec(0,-1,0))
+    	--	end
+    	--end
+    	--local lightshapes = FindShapes("pressurestop",true)
+    	--for s, shape in pairs(lightshapes) do
+    	--	SetShapeEmissiveScale(shape,0)
+    	--end
+    	--lightshapes = FindShapes("emergency",true)
+    	--for s, shape in pairs(lightshapes) do
+    	--	SetShapeEmissiveScale(shape,1)
+    	--end
+    end
+    if pressure < 0 then pressure = 0 end
+    --SetString("hud.notification",round(pressure).."% pressure", true)
+    if GetBool("level.depressurized") then
+    	pressure = 0 --when the main cabin is depressurized, so is the cargo hold
+    end
+end
+

```

---

# Migration Report: main\drag.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\drag.lua
+++ patched/main\drag.lua
@@ -1,77 +1,72 @@
-doDebug = GetBoolParam("Debug",false) --extensive debugging:
---outlined bodies are being affected by drag, they will have a debug line the length of the raycast
---bodies with a green debug line are not being affected by drag but are able to be
-ExplodeTime = 200
-bIndex = 0
-dragged = {}
-CPS = GetIntParam("ChecksPerFrame",30)
-dragsound= LoadLoop("MOD/main/Boeing 737/snd/drag.ogg")
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        bodies = FindBodies(nil,true)
+    end
+end
 
-function tick(dt)
-	bodies = FindBodies(nil,true)
-	for r=1, CPS do
-		bIndex = bIndex + 1
-		if bIndex > #bodies then bIndex = 1 end
-		
-		local body = bodies[bIndex]
-		if IsBodyDynamic(body) then
-			local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
-			local mass = GetBodyMass(body)
-			if (not HasTag(GetBodyShapes(body)[1],"nodrag")) and not (center[2]<20) then
-				QueryRejectBody(body)
-				local hit = QueryRaycast(center,Vec(0,0,-1),90)
-				if hit then
-					dragged[bIndex] = false
-				else
-					dragged[bIndex] = true
-				end
-			end
-		end
-	end
-	
-	if ExplodeTime > -25 then --cooldown system to keep large objects from causing lag
-		ExplodeTime = ExplodeTime - 5
-		--DebugPrint(ExplodeTime)
-	end
-	if doDebug then local dragged = 0 end
-	for i, body in pairs(bodies) do
-		local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
-		local mass = GetBodyMass(body)
-		if dragged[i] and center[2] > 20 then
-			ApplyBodyImpulse(body,center,Vec(0,0,mass))
-			if doDebug then
-				DrawBodyOutline(body,1,0,0,1)
-				DebugLine(center,VecAdd(center,Vec(0,0,-90)))
-			end
-		end
-		if center[2] < 5 and mass > 100 then
-			--DebugPrint(mass)
-			--Delete(body)
-			--if mass > ExplodeTime then
-			--	Explosion(center,4)
-			--	ExplodeTime = ExplodeTime + 25
-			--end
-			
-		end
-	end
-	local ptrans = GetPlayerTransform()
-	ptrans.pos = VecAdd(ptrans.pos,Vec(0,0.5,0))
-	local hit = QueryRaycast(ptrans.pos,Vec(0,0,-1),800)
-	local standing = QueryRaycast(ptrans.pos,Vec(0,-1,0),0.7)
-	if (not hit) and ptrans.pos[2] > 20 then
-		if ptrans.pos[2] > 20 then
-			PlayLoop(dragsound,ptrans.pos,1000)
-		end
-		pvel = GetPlayerVelocity()
-		if pvel[3] < 15 or ptrans.pos[2] > 100 then
-			SetPlayerVelocity(VecAdd(pvel,Vec(0,0,0.5)))
-		end
-		if standing then --blow the player off their feet if they're standing on something
-			SetPlayerVelocity(VecAdd(pvel,Vec(0,0.3,2)))
-		end
-	end
-	--if ptrans.pos[2] < 6 then
-	--	SetPlayerTransform(Transform(Vec(ptrans.pos[1],5.5,ptrans.pos[3]+15*dt),ptrans.rot), true)
-	--	SetPlayerHealth(0)
-	--end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    for r=1, CPS do
+    	bIndex = bIndex + 1
+    	if bIndex > #bodies then bIndex = 1 end
+
+    	local body = bodies[bIndex]
+    	if IsBodyDynamic(body) then
+    		local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
+    		local mass = GetBodyMass(body)
+    		if (not HasTag(GetBodyShapes(body)[1],"nodrag")) and not (center[2]<20) then
+    			QueryRejectBody(body)
+    			local hit = QueryRaycast(center,Vec(0,0,-1),90)
+    			if hit then
+    				dragged[bIndex] = false
+    			else
+    				dragged[bIndex] = true
+    			end
+    		end
+    	end
+    end
+
+    if ExplodeTime > -25 then --cooldown system to keep large objects from causing lag
+    	ExplodeTime = ExplodeTime - 5
+    	--DebugPrint(ExplodeTime)
+    end
+    if doDebug then local dragged = 0 end
+    for i, body in pairs(bodies) do
+    	local center = TransformToParentPoint(GetBodyTransform(body),GetBodyCenterOfMass(body))
+    	local mass = GetBodyMass(body)
+    	if dragged[i] and center[2] > 20 then
+    		ApplyBodyImpulse(body,center,Vec(0,0,mass))
+    		if doDebug then
+    			DrawBodyOutline(body,1,0,0,1)
+    			DebugLine(center,VecAdd(center,Vec(0,0,-90)))
+    		end
+    	end
+    	if center[2] < 5 and mass > 100 then
+    		--DebugPrint(mass)
+    		--Delete(body)
+    		--if mass > ExplodeTime then
+    		--	Explosion(center,4)
+    		--	ExplodeTime = ExplodeTime + 25
+    		--end
+
+    	end
+    end
+    local ptrans = GetPlayerTransform(playerId)
+    ptrans.pos = VecAdd(ptrans.pos,Vec(0,0.5,0))
+    local hit = QueryRaycast(ptrans.pos,Vec(0,0,-1),800)
+    local standing = QueryRaycast(ptrans.pos,Vec(0,-1,0),0.7)
+    if (not hit) and ptrans.pos[2] > 20 then
+    	if ptrans.pos[2] > 20 then
+    		PlayLoop(dragsound,ptrans.pos,1000)
+    	end
+    	pvel = GetPlayerVelocity(playerId)
+    	if pvel[3] < 15 or ptrans.pos[2] > 100 then
+    		SetPlayerVelocity(playerId, VecAdd(pvel,Vec(0,0,0.5)))
+    	end
+    	if standing then --blow the player off their feet if they're standing on something
+    		SetPlayerVelocity(playerId, VecAdd(pvel,Vec(0,0.3,2)))
+    	end
+    end
 end
+

```

---

# Migration Report: main\parallax.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\parallax.lua
+++ patched/main\parallax.lua
@@ -1,53 +1,53 @@
-function init()
-	bodies = FindBodies("section")
-	physFloor = FindBody("physBody1")
-	plane = FindBody("boeing",true)
-	velocity = GetIntParam("velocity", 15)
-	
-	paused=false
-	pauseTimer=0
+#version 2
+function server.init()
+    bodies = FindBodies("section")
+    physFloor = FindBody("physBody1")
+    plane = FindBody("boeing",true)
+    velocity = GetIntParam("velocity", 15)
+    paused=false
+    pauseTimer=0
 end
 
-function tick(dt)
-	
-	if IsBodyDynamic(plane) and pauseTimer < 5.3 then
-		SetBodyVelocity(plane,VecAdd(GetBodyVelocity(plane),Vec(0,8*dt,-0.5*dt)))
-	end
-	
-	if GetBodyTransform(plane).pos[2] < 20 and not paused then
-		pauseTimer = pauseTimer+dt
-		if pauseTimer > 5 then
-			paused=true
-			for i, body in pairs(FindBodies(nil,true)) do
-				SetBodyVelocity(body,VecAdd(GetBodyVelocity(body),Vec(0,0,-1*velocity)))
-			end
-			SetPlayerVelocity(VecAdd(GetPlayerVelocity,Vec(0,0,-1*velocity)))
-		end
-	end
-	
-	if paused then
-		SetBodyVelocity(physFloor,Vec(0,0,0))
-		for i in pairs(bodies) do
-			SetBodyVelocity(bodies[i],Vec(0,0,0))
-		end
-	else
-		for i in pairs(bodies) do
-			local amnt = GetTagValue(bodies[i],"section")
-			amnt = tonumber(amnt)
-			local diff = dt*velocity
-			amnt = amnt + diff
-			if amnt > 1200 then
-				amnt = amnt - 1400
-				diff = diff - 1400
-			end
-			SetTag(bodies[i],"section",amnt)
-			for s, shape in pairs(GetBodyShapes(bodies[i])) do
-				local strans = GetShapeLocalTransform(shape)
-				strans.pos[3] = strans.pos[3] + diff
-				strans.pos[2] = 50
-				SetShapeLocalTransform(shape,strans)
-			end
-		end
-		SetBodyVelocity(physFloor,Vec(0,0,velocity))
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if IsBodyDynamic(plane) and pauseTimer < 5.3 then
+        	SetBodyVelocity(plane,VecAdd(GetBodyVelocity(plane),Vec(0,8*dt,-0.5*dt)))
+        end
+        if GetBodyTransform(plane).pos[2] < 20 and not paused then
+        	pauseTimer = pauseTimer+dt
+        	if pauseTimer > 5 then
+        		paused=true
+        		for i, body in pairs(FindBodies(nil,true)) do
+        			SetBodyVelocity(body,VecAdd(GetBodyVelocity(body),Vec(0,0,-1*velocity)))
+        		end
+        		SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity,Vec(0,0,-1*velocity)))
+        	end
+        end
+        if paused then
+        	SetBodyVelocity(physFloor,Vec(0,0,0))
+        	for i in pairs(bodies) do
+        		SetBodyVelocity(bodies[i],Vec(0,0,0))
+        	end
+        else
+        	for i in pairs(bodies) do
+        		local amnt = GetTagValue(bodies[i],"section")
+        		amnt = tonumber(amnt)
+        		local diff = dt*velocity
+        		amnt = amnt + diff
+        		if amnt > 1200 then
+        			amnt = amnt - 1400
+        			diff = diff - 1400
+        		end
+        		SetTag(bodies[i],"section",amnt)
+        		for s, shape in pairs(GetBodyShapes(bodies[i])) do
+        			local strans = GetShapeLocalTransform(shape)
+        			strans.pos[3] = strans.pos[3] + diff
+        			strans.pos[2] = 50
+        			SetShapeLocalTransform(shape,strans)
+        		end
+        	end
+        	SetBodyVelocity(physFloor,Vec(0,0,velocity))
+        end
+    end
 end
+

```

---

# Migration Report: main\wing.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\wing.lua
+++ patched/main\wing.lua
@@ -1,101 +1,104 @@
-function init()
-	Xres = GetIntParam("Xres",20)
-	Yres = GetIntParam("Yres",50)
-	pos1 = GetLocationTransform(FindLocation("pos1")).pos --the wing has 4 corners
-	pos2 = GetLocationTransform(FindLocation("pos2")).pos
-	pos3 = GetLocationTransform(FindLocation("pos3")).pos
-	pos4 = GetLocationTransform(FindLocation("pos4")).pos
-	types = {} --used to store what types of leaks there are
-	lengths = {} --trails fade out
-	emitVel = GetFloatParam("trailSpeed",20)
-	disabled=false
+#version 2
+function server.init()
+    Xres = GetIntParam("Xres",20)
+    Yres = GetIntParam("Yres",50)
+    pos1 = GetLocationTransform(FindLocation("pos1")).pos --the wing has 4 corners
+    pos2 = GetLocationTransform(FindLocation("pos2")).pos
+    pos3 = GetLocationTransform(FindLocation("pos3")).pos
+    pos4 = GetLocationTransform(FindLocation("pos4")).pos
+    types = {} --used to store what types of leaks there are
+    lengths = {} --trails fade out
+    emitVel = GetFloatParam("trailSpeed",20)
+    disabled=false
 end
 
-function tick(dt)
-	if disabled then return end
-	local holecount = 0
-	local i = 0
-	local nearHoles = 0
-	for x=1, Xres do
-		for y=1, Yres do
-			i = i + 1
-			
-			local posnear = VecLerp(pos1,pos2,x/Xres)
-			local posfar = VecLerp(pos3,pos4,x/Xres)
-			local pos = VecLerp(posnear,posfar,y/Yres)
-			local hit, dist = QueryRaycast(pos,Vec(0,-1,0),3)
-			if not hit then
-				--DebugPrint(y)
-				--DebugLine(pos,VecSub(pos,Vec(0,dist,0)))
-				if y <= 2 then
-					nearHoles = nearHoles+1
-				end
-			--else
-				if holecount <= 3 then
-					holecount = holecount + 1
-					if not types[holecount] then
-						if i > 5 then
-							types[holecount] = math.random(1,3)
-							lengths[holecount] = math.random(75,200)
-						else
-							types[holecount] = 1
-							lengths[holecount] = 0
-						end
-					end
-					lengths[holecount] = lengths[holecount] - 0.6
-					--DebugPrint(lengths[holecount]*.1)
-					if types[holecount] == 1 then --white
-					--	DebugLine(pos,VecSub(pos,Vec(0,3,0)),1,0,0)
-						ParticleReset()
-						ParticleColor(0.9,0.9,0.9)
-						ParticleRadius(1,0)
-						ParticleAlpha(0.5,0.0,"linear",0.03,0.9)
-						if emitVel < 2 then
-							ParticleGravity(-7)
-							ParticleCollide(1)
-						else
-							ParticleGravity(0,-2)
-							ParticleCollide(0)
-						end
-						SpawnParticle(VecSub(pos,Vec(0,2,0)),Vec(math.random()-0.5,math.random()-0.5,emitVel),lengths[holecount]*.1)
-					elseif types[holecount] == 2 then --off white
-					--	DebugLine(pos,VecSub(pos,Vec(0,3,0)),1,0,0)
-						ParticleReset()
-						ParticleColor(0.75,0.75,0.95)
-						ParticleRadius(1,0)
-						ParticleAlpha(0.5,0.0,"linear",0.03,0.9)
-						if emitVel < 2 then
-							ParticleGravity(-7)
-							ParticleCollide(1)
-						else
-							ParticleGravity(0,-2)
-							ParticleCollide(0)
-						end
-						SpawnParticle(VecSub(pos,Vec(0,2,0)),Vec(math.random()-0.5,math.random()-0.5,emitVel),lengths[holecount]*.1)
-					elseif types[holecount] == 3 then --black
-					--	DebugLine(pos,VecSub(pos,Vec(0,3,0)),1,0,0)
-						ParticleReset()
-						ParticleColor(0.15,0.15,0.15)
-						ParticleRadius(1,0)
-						ParticleAlpha(0.7,0.0,"linear",0.03,0.9)
-						
-						if emitVel < 2 then
-							ParticleGravity(-7)
-							ParticleCollide(1)
-						else
-							ParticleGravity(0,-2)
-							ParticleCollide(0)
-						end
-						SpawnParticle(VecSub(pos,Vec(0,2,0)),Vec(math.random()-0.5,math.random()-0.5,emitVel),lengths[holecount]*.1)
-					end
-				end
-			end
-		end
-	end
-	
-	--DebugPrint(nearHoles)
-	if nearHoles > 6 and GetBool("savegame.mod.doFall") then
-		SetBodyDynamic(FindBody("boeing",true),true)
-		disabled = true
-	end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if disabled then return end
+    local holecount = 0
+    local i = 0
+    local nearHoles = 0
+    for x=1, Xres do
+    	for y=1, Yres do
+    		i = i + 1
+
+    		local posnear = VecLerp(pos1,pos2,x/Xres)
+    		local posfar = VecLerp(pos3,pos4,x/Xres)
+    		local pos = VecLerp(posnear,posfar,y/Yres)
+    		local hit, dist = QueryRaycast(pos,Vec(0,-1,0),3)
+    		if not hit then
+    			--DebugPrint(y)
+    			--DebugLine(pos,VecSub(pos,Vec(0,dist,0)))
+    			if y <= 2 then
+    				nearHoles = nearHoles+1
+    			end
+    		--else
+    			if holecount <= 3 then
+    				holecount = holecount + 1
+    				if not types[holecount] then
+    					if i > 5 then
+    						types[holecount] = math.random(1,3)
+    						lengths[holecount] = math.random(75,200)
+    					else
+    						types[holecount] = 1
+    						lengths[holecount] = 0
+    					end
+    				end
+    				lengths[holecount] = lengths[holecount] - 0.6
+    				--DebugPrint(lengths[holecount]*.1)
+    				if types[holecount] == 1 then --white
+    				--	DebugLine(pos,VecSub(pos,Vec(0,3,0)),1,0,0)
+    					ParticleReset()
+    					ParticleColor(0.9,0.9,0.9)
+    					ParticleRadius(1,0)
+    					ParticleAlpha(0.5,0.0,"linear",0.03,0.9)
+    					if emitVel < 2 then
+    						ParticleGravity(-7)
+    						ParticleCollide(1)
+    					else
+    						ParticleGravity(0,-2)
+    						ParticleCollide(0)
+    					end
+    					SpawnParticle(VecSub(pos,Vec(0,2,0)),Vec(math.random()-0.5,math.random()-0.5,emitVel),lengths[holecount]*.1)
+    				elseif types[holecount] == 2 then --off white
+    				--	DebugLine(pos,VecSub(pos,Vec(0,3,0)),1,0,0)
+    					ParticleReset()
+    					ParticleColor(0.75,0.75,0.95)
+    					ParticleRadius(1,0)
+    					ParticleAlpha(0.5,0.0,"linear",0.03,0.9)
+    					if emitVel < 2 then
+    						ParticleGravity(-7)
+    						ParticleCollide(1)
+    					else
+    						ParticleGravity(0,-2)
+    						ParticleCollide(0)
+    					end
+    					SpawnParticle(VecSub(pos,Vec(0,2,0)),Vec(math.random()-0.5,math.random()-0.5,emitVel),lengths[holecount]*.1)
+    				elseif types[holecount] == 3 then --black
+    				--	DebugLine(pos,VecSub(pos,Vec(0,3,0)),1,0,0)
+    					ParticleReset()
+    					ParticleColor(0.15,0.15,0.15)
+    					ParticleRadius(1,0)
+    					ParticleAlpha(0.7,0.0,"linear",0.03,0.9)
+
+    					if emitVel < 2 then
+    						ParticleGravity(-7)
+    						ParticleCollide(1)
+    					else
+    						ParticleGravity(0,-2)
+    						ParticleCollide(0)
+    					end
+    					SpawnParticle(VecSub(pos,Vec(0,2,0)),Vec(math.random()-0.5,math.random()-0.5,emitVel),lengths[holecount]*.1)
+    				end
+    			end
+    		end
+    	end
+    end
+
+    --DebugPrint(nearHoles)
+    if nearHoles > 6 and GetBool("savegame.mod.doFall") then
+    	SetBodyDynamic(FindBody("boeing",true),true)
+    	disabled = true
+    end
 end
+

```

---

# Migration Report: Main Menu\api.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\api.lua
+++ patched/Main Menu\api.lua
@@ -1,35 +1,31 @@
-function init()
-end
-
--- COLORS
-
+#version 2
 function cR(r)
     return r/255
 end
+
 function cG(g)
     return g/255
 end
+
 function cB(b)
     return b/255
 end
+
 function cA(a)
     return a/100
 end
 
--- FPS
-
 function Enable_FPS( ... )
 
 end
+
 function Enable_FPS( ... )
 
 end
-
--- PLANE
 
 function seat_button(seatid,key,w,h)
     -- if not HasKey(key.."."..seatid) then
-    --     SetBool(key.."."..seatid,false)
+    --     SetBool(key.."."..seatid,false, true)
     -- else
         -- if ClearKey(key..seatid) then
         --     DebugPrint('key clear: '..key..seatid)
@@ -62,10 +58,10 @@
             if GetBool(key.."."..seatid) == true then
                 -- DebugPrint("Seat Remove: "..seatid)
                 ClearKey(key.."."..seatid)
-                -- SetBool(key.."."..seatid,false) 
+                -- SetBool(key.."."..seatid,false, true) 
             else
                 -- DebugPrint("Seat Select: "..seatid)
-                SetBool(key.."."..seatid,true) 
+                SetBool(key.."."..seatid,true, true) 
             end
             AllSelectedPassengers(key,"savegame.mod.cabin.all_passemgers")
         end
@@ -78,13 +74,13 @@
         ClearKey(key.."."..i)
     end
 end
+
 function SelAPas(key)
     local maxSeats = 162
     for i = 1, maxSeats do
-        SetBool(key.."."..i,true)
-    end
-end
-
+        SetBool(key.."."..i,true, true)
+    end
+end
 
 function AllSelectedPassengers(key,boolKey,OneOrMore_selected)
     local maxSeats = 162
@@ -100,16 +96,17 @@
             selected = selected + 1
             if #keys == selected then
                 if maxSeats == selected then
-                    SetBool(boolKey,true)
+                    SetBool(boolKey,true, true)
                     return true
                 else
-                    SetBool(boolKey,false)
+                    SetBool(boolKey,false, true)
                     return false
                 end
             end
         end
     end
 end
+
 function RandomPassagers(key)
     local maxSeats = 162
     local randomnumber_seats = math.random(50,200)
@@ -118,10 +115,9 @@
     end
 
     for i = 1, randomnumber_seats do
-        SetBool(key.."."..math.random(1,162),true)
-    end
-end
--- GAMEMODES
+        SetBool(key.."."..math.random(1,162),true, true)
+    end
+end
 
 function GetAmmountModes( ... )
     local AmmountModes = 0
@@ -186,11 +182,6 @@
         return NoPreviewImage
     end
 end
-
-
-
-
--- UI
 
 function UiLineWidth(h)
     UiPush()
@@ -217,9 +208,9 @@
             UiButtonImageBox('path',image,borderWidth,borderHeight,r,g,b,a)
             if UiTextButton(" ",14,14) then
                 if GetBool(key) == true then
-                    SetBool(key,false)
+                    SetBool(key,false, true)
                 else
-                    SetBool(key,true)
+                    SetBool(key,true, true)
                 end
             end
         UiPop()
@@ -231,22 +222,18 @@
         UiFont('regular.ttf',26)
         if UiTextButton(Text,w) then
             if GetBool(key) == true then
-                SetBool(key,false)
+                SetBool(key,false, true)
             else
-                SetBool(key,true)
+                SetBool(key,true, true)
             end
         end
     UiPop()
 end
-
-
-SubItems = 0
-SubMenuOpenId = 0
 
 function CreateDropdownMenu(id,w,key,Values,keyValues,name)
     if not HasKey(key..".itemName") or not HasKey(key..".itemVal") then
-        SetString(key..".itemVal","Select")
-        SetString(key..".itemName","Select")
+        SetString(key..".itemVal","Select", true)
+        SetString(key..".itemName","Select", true)
     end
     ButtonHeight = 40
     UiPush()
@@ -304,21 +291,18 @@
                     -- UiColor(0,0,0,1)
                 -- end
                 if UiTextButton(Values[i],w,ButtonHeight) then
-                    SetString(key..".itemName",Values[i])
+                    SetString(key..".itemName",Values[i], true)
                 end
                 UiTranslate(0,ButtonHeight)
                 -- SubItems = #Values - 0
             end
-            SetString(key..".itemVal",keyValues[a_Selected])
+            SetString(key..".itemVal",keyValues[a_Selected], true)
         end
         UiPop()
     UiPop()
     return a_Selected
 end
 
--- MAIN UI
-
--- CenterPoingRight
 function CreateTabUi(Id, w, h, IsStart, IsEnd ,Text)
     UiPush()
         if not IsStart then
@@ -372,14 +356,6 @@
     UiPop()
     UiTranslate(w+5,0)
 end
-Settings_string = {
-    "savegame.mod.cabin.options.itemName",
-    "savegame.mod.time.itemName",
-    "savegame.mod.weather2.itemName",
-    "savegame.mod.GroundType.itemName",
-}
-currentkey = 1
-maxKeys = 1
 
 function IsSettingsSetup()
     local itemName_cabin        = GetString("savegame.mod.cabin.options.itemName")
@@ -412,53 +388,16 @@
     -- end
 end
 
-FPS_settings_keys_returns = {
-    ["wather"] = "",
-    -- [""]
-}
-
 function GetBool_FPS( ... )
     
 end
+
 function GetString_FPS( ... )
     
 end
 
 function GetBool_Settings(key,return_string)
     if GetBool(key) == true then return return_string else return "" end
-end
-
--- NOT IN DOCUMENTATION
-
-workshop_ids = {
-    "2490966482",
-    "2419552682",
-    "2429082431"
-}
-
-workshop_ids_warning = {
-    ["2490966482"] = {
-        ["ALERT"] = "Better flood", -- Item
-        ["MESSAGE"] = "Causes plane to explode", -- message
-    },
-    ["2419552682"] = {
-        ["ALERT"] = "Performance Mod", -- Item
-        ["MESSAGE"] = "Causes ragdolls to disappear", -- message
-    },
-    ["2429082431"] = {
-        ["ALERT"] = "HackerPhone",
-        ["MESSAGE"] = "Causes lights to break",
-    },
-}
-
-
-Conflicting = false
-ShowCredits = false
-
-for i = 1 , #workshop_ids do
-    if HasKey('mods.available.steam-'..workshop_ids[i]) == true and GetBool("mods.available.steam-"..workshop_ids[i]..".active") == true then
-        Conflicting = true
-    end
 end
 
 function Conflictingmods(get) 
@@ -533,7 +472,7 @@
                             --     UiColor(1, 1, 1, 1)
                             --     if UiTextButton("Workshop",181,42) then
                             --         -- Command("openurl", "https://steamcommunity.com/sharedfiles/filedetails/?id="..workshop_ids[i])
-                            --         -- SetBool("mods.available.steam-"..workshop_ids[i]..".active",false)
+                            --         -- SetBool("mods.available.steam-"..workshop_ids[i]..".active",false, true)
                             --     end
                             -- UiPop()
                             UiColor(1,0.4,0.4,1)
@@ -666,8 +605,6 @@
     end
 end
 
--- Custom functions
-
 function sa_CreateCheckBox(Id, w, key, TextCenter , Text)
     UiPush()
         UiAlign("left middle")
@@ -687,10 +624,10 @@
             UiButtonImageBox('path',image,borderWidth,borderHeight,r,g,b,a)
             if UiTextButton(" ",14,14) then
                 if GetBool(key) == true then
-                    SetBool(key,false)
+                    SetBool(key,false, true)
                     deSelAPas("savegame.mod.plane_seat")
                 else
-                    SetBool(key,true)
+                    SetBool(key,true, true)
                     SelAPas("savegame.mod.plane_seat")
                 end
             end
@@ -704,11 +641,12 @@
         if UiTextButton(Text,w) then
             if GetBool(key) == true then
                 deSelAPas("savegame.mod.plane_seat")
-                SetBool(key,false)
+                SetBool(key,false, true)
             else
                 SelAPas("savegame.mod.plane_seat")
-                SetBool(key,true)
+                SetBool(key,true, true)
             end
         end
     UiPop()
-end+end
+

```

---

# Migration Report: Main Menu\images\weather and time\screen.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\images\weather and time\screen.lua
+++ patched/Main Menu\images\weather and time\screen.lua
@@ -1,12 +1,10 @@
-function init( ... )
-    
-end
-
-function draw()
+#version 2
+function client.draw()
     UiPush()
         Wather = GetString('savegame.mod.weather2.itemVal')
         Time = GetString('savegame.mod.Time.itemVal')
 
         UiImageBox('./'..Time..Wather..".png",UiWidth(),UiHeight(),0,0)
     UiPop()
-end+end
+

```

---

# Migration Report: Main Menu\images\weather and time\temp_waether.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\images\weather and time\temp_waether.lua
+++ patched/Main Menu\images\weather and time\temp_waether.lua
@@ -1,7 +1,9 @@
-function init()
+#version 2
+function server.init()
     cam = GetLocationTransform(FindLocation('cam_weather',true))
 end
 
-function draw()
+function client.draw()
     SetCameraTransform(cam,90)
-end+end
+

```

---

# Migration Report: Main Menu\list_gamemodes.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\list_gamemodes.lua
+++ patched/Main Menu\list_gamemodes.lua
@@ -1,85 +1,89 @@
-function update()
-modes = {
-    [1] = {
-        [1] = {
-            ["map"] = "map.xml",
-            ["map Credits Text"] = "-",
-            ["name"] = "Sandbox",
-            ["image"] ="./gamemode_covers/737 sandbox.png",
-            ["Briefing"] = "You're finally awake, you have no clue where you are or how you got there. What will you do next?",
-            ["Objective"] = "- Do your thing",
-            ["can Play"] = true,
-            ["disabled Options"] = {
-                ["Cessna"] = false,
+#version 2
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        modes = {
+            [1] = {
+                [1] = {
+                    ["map"] = "map.xml",
+                    ["map Credits Text"] = "-",
+                    ["name"] = "Sandbox",
+                    ["image"] ="./gamemode_covers/737 sandbox.png",
+                    ["Briefing"] = "You're finally awake, you have no clue where you are or how you got there. What will you do next?",
+                    ["Objective"] = "- Do your thing",
+                    ["can Play"] = true,
+                    ["disabled Options"] = {
+                        ["Cessna"] = false,
+                    },
+                    ["Starting Layers"] = "".." "
+                        ..GetString('savegame.mod.weather2.itemVal').." "
+                        ..GetString('savegame.mod.time.itemVal').." "
+                        -- Cabin options
+                        ..GetBool_Settings('savegame.mod.cabin.Window_Shades',"Window_Shades").." "
+                        ..GetBool_Settings('savegame.mod.cabin.breathing_masks',"breathing_masks").." "
+                        ..GetBool_Settings('savegame.mod.cabin.luggage',"luggage").." "
+                        ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
+                        ..GetBool_Settings('savegame.mod.cabin.gore',"gore").." "
+                        -- other
+                        ..GetBool_Settings('savegame.mod.plane.wires',"options_other_wires").." "
+                        ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
+                        ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
+                        ..GetBool_Settings('savegame.mod.plane.cessna',"options_other_cesna").." "
+                        ..GetBool_Settings('savegame.mod.plane.wind_drag',"options_other_wind_drag").." "
+                        ..GetString('savegame.mod.GroundType.itemVal').." "
+                    ,
+                    ["FPS layers"] = "fps "
+                        ..GetString('savegame.mod.weather2.itemVal').." "
+                        ..GetString('savegame.mod.time.itemVal').." "
+                        ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
+                        ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
+                        ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
+                        ..GetBool_Settings('savegame.mod.plane.cessna',"options_other_cesna").." "
+                        ..GetString('savegame.mod.GroundType.itemVal').." "
+                    ,
+                },
+                [2] = {
+                    ["map"] = "map land.xml",
+                    ["map Credits Text"] = "Prop guy - Hellmark  props and some vehicles\nRand0mAccess - Jetway",
+                    ["name"] = "Grounded",
+                    ["image"] ="./gamemode_covers/grounded sandbox.png",
+                    ["Briefing"] = "Wake up, you'll be late to your flight! Remember your bags!",
+                    ["Objective"] = "- Wait for your plane",
+                    ["can Play"] = true,
+                    ["disabled Options"] = {
+                        ["Cessna"] = true,
+                        ["Depress"] = true,
+                    },
+                    ["Starting Layers"] = "".." "
+                        ..GetString('savegame.mod.weather2.itemVal').." "
+                        ..GetString('savegame.mod.time.itemVal').." "
+                        -- Cabin options
+                        ..GetBool_Settings('savegame.mod.cabin.Window_Shades',"Window_Shades").." "
+                        ..GetBool_Settings('savegame.mod.cabin.breathing_masks',"breathing_masks").." "
+                        ..GetBool_Settings('savegame.mod.cabin.luggage',"luggage").." "
+                        ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
+                        ..GetBool_Settings('savegame.mod.cabin.gore',"gore").." "
+                        -- other
+                        ..GetBool_Settings('savegame.mod.plane.wires',"options_other_wires").." "
+                        ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
+                        ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
+                    ,
+                    ["FPS layers"] = "fps "
+                        ..GetString('savegame.mod.weather2.itemVal').." "
+                        ..GetString('savegame.mod.time.itemVal').." "
+                        ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
+                        ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
+                        ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
+                        -- savegame.mod.plane.cessna
+                    ,
+                },
             },
-            ["Starting Layers"] = "".." "
-                ..GetString('savegame.mod.weather2.itemVal').." "
-                ..GetString('savegame.mod.time.itemVal').." "
-                -- Cabin options
-                ..GetBool_Settings('savegame.mod.cabin.Window_Shades',"Window_Shades").." "
-                ..GetBool_Settings('savegame.mod.cabin.breathing_masks',"breathing_masks").." "
-                ..GetBool_Settings('savegame.mod.cabin.luggage',"luggage").." "
-                ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
-                ..GetBool_Settings('savegame.mod.cabin.gore',"gore").." "
-                -- other
-                ..GetBool_Settings('savegame.mod.plane.wires',"options_other_wires").." "
-                ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
-                ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
-                ..GetBool_Settings('savegame.mod.plane.cessna',"options_other_cesna").." "
-                ..GetBool_Settings('savegame.mod.plane.wind_drag',"options_other_wind_drag").." "
-                ..GetString('savegame.mod.GroundType.itemVal').." "
-            ,
-            ["FPS layers"] = "fps "
-                ..GetString('savegame.mod.weather2.itemVal').." "
-                ..GetString('savegame.mod.time.itemVal').." "
-                ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
-                ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
-                ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
-                ..GetBool_Settings('savegame.mod.plane.cessna',"options_other_cesna").." "
-                ..GetString('savegame.mod.GroundType.itemVal').." "
-            ,
-        },
-        [2] = {
-            ["map"] = "map land.xml",
-            ["map Credits Text"] = "Prop guy - Hellmark  props and some vehicles\nRand0mAccess - Jetway",
-            ["name"] = "Grounded",
-            ["image"] ="./gamemode_covers/grounded sandbox.png",
-            ["Briefing"] = "Wake up, you'll be late to your flight! Remember your bags!",
-            ["Objective"] = "- Wait for your plane",
-            ["can Play"] = true,
-            ["disabled Options"] = {
-                ["Cessna"] = true,
-                ["Depress"] = true,
-            },
-            ["Starting Layers"] = "".." "
-                ..GetString('savegame.mod.weather2.itemVal').." "
-                ..GetString('savegame.mod.time.itemVal').." "
-                -- Cabin options
-                ..GetBool_Settings('savegame.mod.cabin.Window_Shades',"Window_Shades").." "
-                ..GetBool_Settings('savegame.mod.cabin.breathing_masks',"breathing_masks").." "
-                ..GetBool_Settings('savegame.mod.cabin.luggage',"luggage").." "
-                ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
-                ..GetBool_Settings('savegame.mod.cabin.gore',"gore").." "
-                -- other
-                ..GetBool_Settings('savegame.mod.plane.wires',"options_other_wires").." "
-                ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
-                ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
-            ,
-            ["FPS layers"] = "fps "
-                ..GetString('savegame.mod.weather2.itemVal').." "
-                ..GetString('savegame.mod.time.itemVal').." "
-                ..GetBool_Settings("savegame.mod.cabin.passengers","passengers").." "
-                ..GetBool_Settings('savegame.mod.plane.fuel',"options_other_fuel").." "
-                ..GetBool_Settings('savegame.mod.plane.cargo',"options_other_cargo").." "
-                -- savegame.mod.plane.cessna
-            ,
-        },
-    },
-    [2] = {
-        [1] = {
-            ["name"] = "Sandbox",
-            ["can Play"] = false,
+            [2] = {
+                [1] = {
+                    ["name"] = "Sandbox",
+                    ["can Play"] = false,
+                }
+            }
         }
-    }
-}
-end+    end
+end
+

```

---

# Migration Report: Main Menu\list_planes.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\list_planes.lua
+++ patched/Main Menu\list_planes.lua
@@ -1,339 +1 @@
--- #include "./scripts/uis/boeing_737_Ui_functions.lua"
-planes = {
-    [1] = {
-        ["name"] = "Boeing 737",
-        ["image"] ="./images/plane/plane_boeing_737.png",
-        ["logo"] ="./images/plane_titles/boeing737.png",
-        ["intro_logo"] ="./images/plane_titles/boeing737.png",
-        ["added"] = "First Aircraft Jul 27 2021",
-        ["can Use"] = true,
-        ["maps"] = {
-            [1] = "map.xml",
-        },
-        ["tabs_Button_layout"] = function( ... )
-            CreateTabUi(2,203,60,false,false,"Cabin options")
-            CreateTabUi(3,203,60,false,false,"Time & weather")
-            CreateTabUi(4,203,60,false,true ,"Other")
-        end,
-        ["tabs"] = {
-            [2] = {
-                ["tab_title"] = "Cabing Options",
-                ["ui_function"] = function()
-                    UiPush()
-                        if GetBool('savegame.mod.cabin.passengers') == true and GetBool('savegame.mod.firsttime.cabin_passengers.b_enabled') == false then
-                            SetBool('savegame.mod.firsttime.cabin_passengers.enabled',true)
-                            UiPush()
-                                local w_p_w,w_p_h = 24,16
-                                local T = "Try selecting seats for passengers"
-                                local w_w,w_h = UiGetTextSize(T)
-                                UiTranslate(1020,-80)
-                                UiColor(0,0,0,cA(86))
-                                UiImageBox('./images/tabs/full_15.png',w_w + w_p_w*2,w_h+w_p_h*2,15,15)   
-                                UiTranslate(w_p_w,w_p_h + 2)
-                                UiColor(1,1,1,1)
-                                UiText(T) 
-                            UiPop()    
-                            if AllSelectedPassengers("savegame.mod.plane_seat","savegame.mod.cabin.all_passemgers",true) then
-                                SetBool('savegame.mod.firsttime.cabin_passengers.b_enabled',true)
-                            end
-                        end
-                        -- savegame.mod.firsttime.cabin_passengers.enabled
-                        -- savegame.mod.firsttime.cabin_passengers.b_enabled
-                        UiPush()
-                            UiTranslate(32,32)
-                            UiPush()
-                                if GetBool("savegame.mod.fps") == true then
-                                    UiDisableInput()
-                                    UiColorFilter(1,1,1,0.5)
-                                end
-                                local padding = 32
-                                CreateCheckBox(3,150,"savegame.mod.cabin.Window_Shades",false,"Window Shades")
-                                UiTranslate(0,padding)
-                                CreateCheckBox(3,150,"savegame.mod.cabin.breathing_masks",false,"Breathing Masks")
-                                UiTranslate(0,padding)
-                                CreateCheckBox(3,150,"savegame.mod.cabin.luggage",false,"Luggage")
-                                UiTranslate(0,padding*4)
-                                CreateCheckBox(3,150,"savegame.mod.cabin.gore",false,"Gore")
-                            UiPop()    
-                            UiTranslate(0,padding*3)
-                            CreateCheckBox(3,150,"savegame.mod.cabin.passengers",false,"Passengers")
-                            UiTranslate(0,padding)
-                            UiPush()
-                                if (modes[currentPlaneMode][currentMode]["disabled Options"]["Depress"]) then
-                                    UiDisableInput()
-                                    UiColorFilter(1,1,1,0.5)
-                                else
-                                    
-                                end
-                                CreateCheckBox(3,150,"savegame.mod.cabin.depressurize",false,"Cabin Depress")
-                                UiTranslate(0,padding)
-                                UiPush()
-                                    if GetBool("savegame.mod.cabin.depressurize") == false and not modes[currentPlaneMode][currentMode]["disabled Options"]["Depress"] then
-                                        UiDisableInput()
-                                        UiColorFilter(1,1,1,0.5)
-                                    end
-                                    UiTranslate(24,0)
-                                    CreateCheckBox(3,150,"savegame.mod.cabin.depressurize_inf",false,"Infinite Depress")
-                                UiPop()    
-                            UiPop()    
-                        UiPop()    
-                        UiTranslate(250,16)
-                        if GetBool("savegame.mod.fps") == true then
-                            UiDisableInput()
-                            UiColorFilter(1,1,1,0.5)
-                        end
-                    UiPop()
-                    UiPush()
-                        UiAlign('right top')
-                        UiTranslate(UiWidth() - 16,16)
-                        if GetBool("savegame.mod.cabin.passengers") == false then
-                            UiDisableInput()
-                            UiColorFilter(1,1,1,0.5)
-                        end
-                        UiImage('./images/plane/plane.png')
-                        UiPush()
-                            UiTranslate(-648 - 212,265/2)
-                            UiAlign('center middle')
-                            sa_CreateCheckBox(3,150,"savegame.mod.cabin.all_passemgers",false,"Select All")
-                            UiTranslate(300,0)
-                            if UiTextButton('Randomize') then
-                                RandomPassagers("savegame.mod.plane_seat")
-                                AllSelectedPassengers("savegame.mod.plane_seat","savegame.mod.cabin.all_passemgers")
-                            end
-                        UiPop()
-                        UiPush()
-                            local first_class_seat_spacing = 33 + 3
-                            local normal_seat_spacing = 21 + 3
-                            local hlaway_width = 101
-                            UiAlign('left top')
-                            UiTranslate(-1372,174)
-                            UiColor(1,0,0,1)
-                            seatnumber = 0
-                            UiPush()
-                                UiTranslate(0,-173)
-                                seatnumber = seatnumber + 1
-                                UiTranslate(0,49+48)
-                                seat_button(2,"savegame.mod.plane_seat",20,20)
-                                seatnumber = seatnumber + 1
-                                UiTranslate(0,49)
-                                seat_button(1,"savegame.mod.plane_seat",20,20)
-                            UiPop()
-                            UiTranslate(284,0)
-                        -- 
-                            function first_class_seats(seatRow)
-                                UiPush()
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber,"savegame.mod.plane_seat",33,33)
-                                    UiTranslate(0,-first_class_seat_spacing)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber,"savegame.mod.plane_seat",33,33)
-                                    UiTranslate(0,-hlaway_width)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber,"savegame.mod.plane_seat",33,33)
-                                    UiTranslate(0,-first_class_seat_spacing)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber,"savegame.mod.plane_seat",33,33)
-                                UiPop()
-                            end
-                            function noraml_seats(seatRow)
-                                UiPush()
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber ,"savegame.mod.plane_seat",21,21)
-                                    UiTranslate(0,-normal_seat_spacing)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber ,"savegame.mod.plane_seat",21,21)
-                                    UiTranslate(0,-normal_seat_spacing)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber ,"savegame.mod.plane_seat",21,21)
-                                    UiTranslate(0,-hlaway_width + 12)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber ,"savegame.mod.plane_seat",21,21)
-                                    UiTranslate(0,-normal_seat_spacing)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber ,"savegame.mod.plane_seat",21,21)
-                                    UiTranslate(0,-normal_seat_spacing)
-                                    seatnumber = seatnumber + 1
-                                    seat_button(seatnumber ,"savegame.mod.plane_seat",21,21)
-                                UiPop()
-                            end
-                        -- 
-                            seatrow = 1
-                            UiPush()
-                                UiTranslate(0,29)
-                                for i=1,6 do
-                                    first_class_seats()
-                                    UiTranslate(39,0)
-                                end
-                                first_class_seats()
-                                UiTranslate(57,12)
-                                for i=1,3 do
-                                    noraml_seats()
-                                    UiTranslate(27,0)
-                                end
-                                noraml_seats()
-                                UiTranslate(27 + 7,0)
-                                noraml_seats()
-                                UiTranslate(27 + 7,0)
-                                for i=1,17 do
-                                    noraml_seats()
-                                    UiTranslate(27,0)
-                                end
-                            UiPop()
-                            -- UiRect(5,160)
-                        UiPop()
-                    UiPop()
-                end,
-            },
-            [3] = {
-                ["tab_title"] = "Time & weather",
-                ["ui_function"] = function()
-                    UiPush()
-                        UiTranslate(UiCenter() - 250,16)
-                        CreateDropdownMenu(2,200, "savegame.mod.time",
-                        {
-                            "Sunrise",
-                            "Sunny",
-                            "Sunset",
-                            "Night",
-                        }, {
-                            [1] = "sunrise",
-                            [2] = "sunny",
-                            [3] = "sunset",
-                            [4] = "night",
-                        },
-                        "Time")
-                        UiTranslate(300,0)
-                        CreateDropdownMenu(3,200, "savegame.mod.weather2",
-                        {
-                            "Clear",
-                            "Fog",
-                            "Rain",
-                            "Thunder",
-                        }, {
-                            [1] = "clear",
-                            [2] = "fog",
-                            [3] = "rain",
-                            [4] = "thunder",
-                        },
-                        "Weather")
-                    UiPop()
-                end
-            },
-            [4] = { 
-                ["tab_title"] = "Other",
-                ["ui_function"] = function()
-                    UiPush()
-                        UiDisableInput()
-                        -- UiPush()
-                        --     UiTranslate(UiCenter(),UiMiddle())
-                        --     UiAlign("center middle")
-                        --     UiImageBox('./images/comingsoon.png',436,80,0,0)
-                        -- UiPop()
-                        UiTranslate(UiCenter() - 100,16)
-                        UiPush()
-                            UiTranslate(- 150,0)
-                            UiPush()
-                                UiTranslate(- 40,0)
-                                UiFont('bold.ttf',32)
-                                UiText("Other Options")
-                            UiPop()
-                            UiTranslate(-32,50)
-                            UiPush()
-                                UiEnableInput()
-                                UiColorFilter(1,1,1,1)
-                                UiPush()
-                                    if GetBool("savegame.mod.fps") == true then
-                                        UiDisableInput()
-                                        UiColorFilter(1,1,1,0.5)
-                                    end
-                                    CreateCheckBox(2, 150, "savegame.mod.plane.wires", false , "Wires")
-                                UiPop()
-                                UiTranslate(0,30)
-                                CreateCheckBox(4, 150, "savegame.mod.plane.wind_drag", false , "Wind Drag")
-                                UiTranslate(0,30)
-                                CreateCheckBox(5, 150, "savegame.mod.doFall", false , "Airplane Falling")
-                                UiTranslate(0,30)
-                                CreateCheckBox(5, 150, "savegame.mod.plane.cargo", false , "Cargo")
-                                UiTranslate(0,30)
-                                CreateCheckBox(5, 150, "savegame.mod.plane.fuel", false , "Fuel")
-                                UiTranslate(0,30)
-                                UiPush()
-                                    if (modes[currentPlaneMode][currentMode]["disabled Options"]["Cessna"]) then
-                                        UiDisableInput()
-                                        UiColorFilter(1,1,1,0.5)
-                                    else
-                                        
-                                    end
-                                    -- ["disabled Options"] = {
-                                    --     ["Cessna"] = true,
-                                    -- },
-                                    CreateCheckBox(5, 150, "savegame.mod.plane.cessna", false , "Cessna")
-                                UiPop()
-                            UiPop()
-                            UiColorFilter(1,1,1,0.5)
-                            -- wires
-                            UiTranslate(0,30)
-                            -- Wind Drag
-                            UiTranslate(0,30)
-                            -- Airplane Falling
-                            UiTranslate(0,30)
-                            -- Cargo
-                            UiTranslate(0,30)
-                            -- Fuel
-                            UiTranslate(0,30)
-                            -- Cesna
-                        UiPop()
-                        UiPush()
-                            -- UiColorFilter(1,1,1,0.5)
-                            UiEnableInput()
-                            UiTranslate(150,0)
-                            CreateDropdownMenu(4,200, "savegame.mod.GroundType",
-                            {
-                                "Flat",
-                                "Ocean",
-                            },  {
-                                [1] = "ground",
-                                [2] = "o",
-                            },
-                            "Ground type")
-                        UiPop()
-                    UiPop()
-                end, 
-            },
-        },
-        ["windowSizes"] = function ()
-            if tab_selectedId == 1 then
-                SetCameraTransform(cam_1,90)
-                -- SetCameraTransform(GetLocationTransform(cams[1]))
-                -- SetCameraTransform(current_cam_transform,90,degrees)
-                menuoptions = "op1"
-                SetString("level.menuoptions", "op1")
-                -- elseif selectedId == 5 then
-                -- UiWindowSize = UiHeight()
-                preUiwindowsize = 580
-            elseif tab_selectedId == 2 then
-                preUiwindowsize = 300
-                SetCameraTransform(over_seats_cabin,80,degrees)
-                -- over_seats_cabin
-            elseif tab_selectedId == 3 then
-                SetBodyTransform(FindBody("TW_window",true),window_hide_loc)
-                preUiwindowsize = 300
-                SetCameraTransform(TW_seat_window_cam,90,degrees)
-                -- TW_seat_window_cam
-            elseif tab_selectedId == 4 then
-                SetBodyTransform(FindBody("TW_window",true),window_show_loc)
-                SetCameraTransform(outside_view,90,degrees)
-                preUiwindowsize = 300
-                -- outside_view
-            elseif tab_selectedId == "planes" then
-            else
-                SetCameraTransform(GetLocationTransform(FindLocation('camera_tab_no',true)),70,degrees)
-                UiWindowSize = 300
-            end
-            SetMenuHeight(580,1)
-            SetMenuHeight(300,2)
-            SetMenuHeight(300,3)
-            SetMenuHeight(300,4)
-        end
-    },
-}
+#version 2

```

---

# Migration Report: Main Menu\menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\menu.lua
+++ patched/Main Menu\menu.lua
@@ -1,140 +1,4 @@
---[[
-
-    RECREATED MENU BY AlexVeeBee
-
-]]
-#include "api.lua"
-#include "list_gamemodes.lua"
-#include "list_planes.lua"
-
-function init()
-    latetest_ver = "0.8.0"
-    test_current_ver = "0.7.0"
-    snd = LoadSound("./snd/click.ogg")
-
-    -- ClearKey('savegame.mod.plane.id')
-    
-    -- ClearKey('savegame.mod.firsttime.cabin_passengers.enabled')
-    -- ClearKey('savegame.mod.firsttime.cabin_passengers.b_enabled')
-
-    -- ClearKey("savegame.mod.cabin.Window_Shades")
-    -- ClearKey("savegame.mod.cabin.breathing_masks")
-    -- ClearKey("savegame.mod.cabin.luggage")
-    -- ClearKey("savegame.mod.cabin.gore")
-    -- ClearKey("savegame.mod.cabin.passengers")
-    -- ClearKey("savegame.mod.cabin.depressurize")
-    -- ClearKey("savegame.mod.cabin.f_depressurize")
-
-    -- ClearKey("savegame.mod.plane")
-
-
-    if not HasKey('savegame.mod.firsttime.cabin_passengers.enabled') then
-        SetBool('savegame.mod.firsttime.cabin_passengers.enabled',false)
-    end
-    if not HasKey('savegame.mod.firsttime.cabin_passengers.b_enabled') then
-        SetBool('savegame.mod.firsttime.cabin_passengers.b_enabled',false)
-    end
-    if not HasKey('savegame.mod.time.itemName') then
-        SetString('savegame.mod.time.itemName',"Sunrise")
-        SetString('savegame.mod.time.itemVal',"sunrise")
-    end
-    if not HasKey('savegame.mod.weather2.itemName') then
-        SetString('savegame.mod.weather2.itemName',"Clear")
-        SetString('savegame.mod.weather2.itemVal',"clear")
-    end
-    if not HasKey('savegame.mod.GroundType.itemName') then
-        SetString('savegame.mod.GroundType.itemName',"Flat")
-        SetString('savegame.mod.GroundType.itemVal',"f")
-    end
-
-    if not HasKey('savegame.mod.cabin.Window_Shades') then
-        SetBool('savegame.mod.cabin.Window_Shades',true)
-    end
-    if not HasKey('savegame.mod.cabin.breathing_masks') then
-        SetBool('savegame.mod.cabin.breathing_masks',true)
-    end
-    if not HasKey('savegame.mod.cabin.luggage') then
-        SetBool('savegame.mod.cabin.luggage',true)
-    end
-    if not HasKey('savegame.mod.cabin.gore') then
-        SetBool('savegame.mod.cabin.gore',true)
-    end
-    if not HasKey('savegame.mod.cabin.passengers') then
-        SetBool('savegame.mod.cabin.passengers',true)
-    end
-    if not HasKey('savegame.mod.cabin.depressurize') then
-        SetBool('savegame.mod.cabin.depressurize',true)
-    end
-
-    -- Plane Settings
-
-    if not HasKey('savegame.mod.plane.fuel') then
-        SetBool('savegame.mod.plane.fuel',true)
-    end
-    if not HasKey('savegame.mod.plane.wires') then
-        SetBool('savegame.mod.plane.wires',true)
-    end
-    if not HasKey('savegame.mod.plane.wind_drag') then
-        SetBool('savegame.mod.plane.wind_drag',true)
-    end
-    if not HasKey('savegame.mod.doFall') then
-        SetBool('savegame.mod.doFall',false)
-    end
-    if not HasKey("savegame.mod.plane.cargo") then
-        SetBool('savegame.mod.plane.cargo',true)
-    end
-    if not HasKey("savegame.mod.plane.cessna") then
-        SetBool('savegame.mod.plane.cessna',false)
-    end
-    -- savegame.mod.doFall
-
-    -- Planes
-
-    if not HasKey('savegame.mod.plane.id') then
-        SetInt('savegame.mod.plane.id',1)
-    end
-
-
-    round15px = "./images/borderradius/15px_rounded.png"
-
-    intro = 1080
-    introdelay = 3
-    SetValue('introdelay',0,"linear",1)
-    TW_seat_window_cam = GetLocationTransform(FindLocation('cam_w_t_SW',true))
-    over_seats_cabin = GetLocationTransform(FindLocation('main_menu_cam_2_cabin',true))
-    outside_view = GetLocationTransform(FindLocation('main_menu_other',true))
-    hanger_view = GetLocationTransform(FindLocation('main_menu_hanger',true))
-    -- main_menu_other
-    -- main_menu_cam_2_cabin
-
-	cameras = FindLocations("camera",true)
-	menuoptions = ""
-	SetString("level.menuoptions", "op1")
-
-    NoPreviewImage = "./gamemode_covers/no preview.png"
-
-    window_show_loc = GetLocationTransform(FindLocation('winshow',true))
-    window_hide_loc = GetLocationTransform(FindLocation('winHide',true))
-    SetBool("fading.Done",true)
-end
-tab_selectedId = 1
-pre_tab_selectedId = 1
-animation_tab_selectedId = 0
-pre_animation_tab_selectedId = 0
-
-UiWindowSize = 580
-
-currentMode = 1
-currentPlaneMode = 1
-PreCurrentPlaneMode = 1
-
-if HasKey("savegame.mod.plane.id") then
-    currentPlaneMode = GetInt("savegame.mod.plane.id")
-    PreCurrentPlaneMode = GetInt("savegame.mod.plane.id")
-end
-
--- Main ui
-
+#version 2
 function GetLayers()
     if GetBool('savegame.mod.fps') == true then
         -- FPS ENABLED  -----------------------------------------------------------------
@@ -144,28 +8,9 @@
         return GetCurrentModeJSON(currentPlaneMode,currentMode,"Starting Layers")
     end
 end
+
 function StartGame( ... )
     StartLevel("plane","MOD/"..GetCurrentModeJSON(currentPlaneMode,currentMode,"map"),GetLayers())
-end
-
-screenshots = {
-    "image1.png",
-    "image2.png",
-    "image3.png",
-    -- "chips_and_pepsi.jpg",
-}    
-
-current_screenshot              = 1
-next_current_screenshot         = 2
-current_screenshot_next         = 1
-next_current_screenshot_fade    = 1
-next_screenshot_fade_timer      = 1
-max_screenshots                 = 0
-SetValue('next_screenshot_fade_timer',0,"linear",5)
-
-
-for i=1,#screenshots do
-    max_screenshots = i
 end
 
 function fade_screenshot(changes_to)
@@ -179,7 +24,7 @@
     else
         next_current_screenshot = changes_to+1
     end
-    SetBool("fading.Done",false)
+    SetBool("fading.Done",false, true)
     if next_current_screenshot_fade == 1 then
         SetValue("next_current_screenshot_fade",0,"linear",1)
     end
@@ -189,7 +34,7 @@
     if next_current_screenshot_fade == 0 then
         current_screenshot = current_screenshot_next
         next_current_screenshot_fade = 1
-        SetBool("fading.Done",true)
+        SetBool("fading.Done",true, true)
     end
     if next_screenshot_fade_timer == 0 then
         next_screenshot_fade_timer = 1
@@ -251,27 +96,113 @@
     UiPop()
 end
 
--- Main Ui
-
-scrollTest = 0
-
-background_fade = 0
-menu_fade = 1
-
-fade_in_out = false
-
-timer_1 = 2
-timer_2 = 2
-timer_3 = 2
 function setup_fade()
 
 end
-function draw()
+
+function server.init()
+       latetest_ver = "0.8.0"
+       test_current_ver = "0.7.0"
+       -- ClearKey('savegame.mod.plane.id')
+       -- ClearKey('savegame.mod.firsttime.cabin_passengers.enabled')
+       -- ClearKey('savegame.mod.firsttime.cabin_passengers.b_enabled')
+       -- ClearKey("savegame.mod.cabin.Window_Shades")
+       -- ClearKey("savegame.mod.cabin.breathing_masks")
+       -- ClearKey("savegame.mod.cabin.luggage")
+       -- ClearKey("savegame.mod.cabin.gore")
+       -- ClearKey("savegame.mod.cabin.passengers")
+       -- ClearKey("savegame.mod.cabin.depressurize")
+       -- ClearKey("savegame.mod.cabin.f_depressurize")
+       -- ClearKey("savegame.mod.plane")
+       if not HasKey('savegame.mod.firsttime.cabin_passengers.enabled') then
+           SetBool('savegame.mod.firsttime.cabin_passengers.enabled',false, true)
+       end
+       if not HasKey('savegame.mod.firsttime.cabin_passengers.b_enabled') then
+           SetBool('savegame.mod.firsttime.cabin_passengers.b_enabled',false, true)
+       end
+       if not HasKey('savegame.mod.time.itemName') then
+           SetString('savegame.mod.time.itemName',"Sunrise", true)
+           SetString('savegame.mod.time.itemVal',"sunrise", true)
+       end
+       if not HasKey('savegame.mod.weather2.itemName') then
+           SetString('savegame.mod.weather2.itemName',"Clear", true)
+           SetString('savegame.mod.weather2.itemVal',"clear", true)
+       end
+       if not HasKey('savegame.mod.GroundType.itemName') then
+           SetString('savegame.mod.GroundType.itemName',"Flat", true)
+           SetString('savegame.mod.GroundType.itemVal',"f", true)
+       end
+       if not HasKey('savegame.mod.cabin.Window_Shades') then
+           SetBool('savegame.mod.cabin.Window_Shades',true, true)
+       end
+       if not HasKey('savegame.mod.cabin.breathing_masks') then
+           SetBool('savegame.mod.cabin.breathing_masks',true, true)
+       end
+       if not HasKey('savegame.mod.cabin.luggage') then
+           SetBool('savegame.mod.cabin.luggage',true, true)
+       end
+       if not HasKey('savegame.mod.cabin.gore') then
+           SetBool('savegame.mod.cabin.gore',true, true)
+       end
+       if not HasKey('savegame.mod.cabin.passengers') then
+           SetBool('savegame.mod.cabin.passengers',true, true)
+       end
+       if not HasKey('savegame.mod.cabin.depressurize') then
+           SetBool('savegame.mod.cabin.depressurize',true, true)
+       end
+       -- Plane Settings
+       if not HasKey('savegame.mod.plane.fuel') then
+           SetBool('savegame.mod.plane.fuel',true, true)
+       end
+       if not HasKey('savegame.mod.plane.wires') then
+           SetBool('savegame.mod.plane.wires',true, true)
+       end
+       if not HasKey('savegame.mod.plane.wind_drag') then
+           SetBool('savegame.mod.plane.wind_drag',true, true)
+       end
+       if not HasKey('savegame.mod.doFall') then
+           SetBool('savegame.mod.doFall',false, true)
+       end
+       if not HasKey("savegame.mod.plane.cargo") then
+           SetBool('savegame.mod.plane.cargo',true, true)
+       end
+       if not HasKey("savegame.mod.plane.cessna") then
+           SetBool('savegame.mod.plane.cessna',false, true)
+       end
+       -- savegame.mod.doFall
+       -- Planes
+       if not HasKey('savegame.mod.plane.id') then
+           SetInt('savegame.mod.plane.id',1, true)
+       end
+       round15px = "./images/borderradius/15px_rounded.png"
+       intro = 1080
+       introdelay = 3
+       SetValue('introdelay',0,"linear",1)
+       TW_seat_window_cam = GetLocationTransform(FindLocation('cam_w_t_SW',true))
+       over_seats_cabin = GetLocationTransform(FindLocation('main_menu_cam_2_cabin',true))
+       outside_view = GetLocationTransform(FindLocation('main_menu_other',true))
+       hanger_view = GetLocationTransform(FindLocation('main_menu_hanger',true))
+       -- main_menu_other
+       -- main_menu_cam_2_cabin
+    cameras = FindLocations("camera",true)
+    menuoptions = ""
+    SetString("level.menuoptions", "op1", true)
+       NoPreviewImage = "./gamemode_covers/no preview.png"
+       window_show_loc = GetLocationTransform(FindLocation('winshow',true))
+       window_hide_loc = GetLocationTransform(FindLocation('winHide',true))
+       SetBool("fading.Done",true, true)
+end
+
+function client.init()
+    snd = LoadSound("./snd/click.ogg")
+end
+
+function client.draw()
     if GetPlanesJSON(PreCurrentPlaneMode,"can Use") == false then
         currentPlaneMode = 1
         PreCurrentPlaneMode = 1
-        
-        SetInt('savegame.mod.plane.id',1)
+
+        SetInt('savegame.mod.plane.id',1, true)
     end
     -- UiColor(0,0,0,0.8)
     if fade_in_out then
@@ -305,8 +236,8 @@
         timer_1 = 1
     end
     function SetMenuHeight( height , Tab )
-        SetInt('tab.'..Tab..'.height',height)
-        SetInt('tab.'..Tab..'.Tab',Tab)
+        SetInt('tab.'..Tab..'.height',height, true)
+        SetInt('tab.'..Tab..'.Tab',Tab, true)
         -- DebugPrint("Tab: ".. Tab .. " | height: "..GetInt('tab.'..Tab..'.height'))
         -- DebugPrint('tab.'..Tab..'.heigh.',GetInt('tab.'..Tab..'.height'))
     end
@@ -420,7 +351,7 @@
                     UiWindow(UiWidth(),UiWindowSize,false)
                     UiTranslate(0,-UiWindowSize)
                 end
-                
+
                 UiAlign('left top')
                 -- UiText(selectedId)
                 if tab_selectedId == 1 then
@@ -488,7 +419,7 @@
                                     UiTranslate(Button_ChangeGameModesMargin,0)
                                     UiWindow(Button_ChangeGameModesWidth,300)
                                     -- UiRect(UiWidth(),UiHeight())
-                                    
+
                                     if currentMode > 1 then
                                         if UiTextButton(' ',UiWidth(),UiHeight()) then
                                             currentMode = currentMode - 1
@@ -517,7 +448,7 @@
                                     UiTranslate(UiWidth()-Button_ChangeGameModesMargin,0)
                                     UiWindow(Button_ChangeGameModesWidth,300)
                                     -- UiRect(UiWidth(),UiHeight())
-                                
+
                                     if GetAmmountModes() > currentMode then
                                         if UiTextButton(' ',60,300) then
                                             currentMode = currentMode + 1
@@ -611,7 +542,7 @@
                     UiPop()
                 else
                     if tab_selectedId == "planes" then
-                    
+
                     else
                         planes[currentPlaneMode]["tabs"][tab_selectedId]["ui_function"]()
                     end
@@ -633,9 +564,10 @@
 
         Conflictingmods() 
         CreditsPopout(false)
-    
+
     else
         UiMakeInteractive()
 
     end
-end+end
+

```

---

# Migration Report: Main Menu\scripts\activate.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\scripts\activate.lua
+++ patched/Main Menu\scripts\activate.lua
@@ -1,19 +1,4 @@
-function init()
-	objects = FindShapes("obj")
-	objects2 = FindShapes("obj2")
-end
-
-function tick()
-	local active = GetString("savegame.mod.options")
-	local menuoptions = GetString("level.menuoptions")
-	if active == "" and menuoptions =="op3" then
-		activate()
-	end
-	if active == " extra" and menuoptions =="op3" then
-		activate2()
-	end
-end
-
+#version 2
 function activate()
 	for i=1,#objects do
 		object = objects[i]
@@ -28,4 +13,23 @@
 		body2 = GetShapeBody(object2)
 		ApplyBodyImpulse(body2, Vec(0,0,0), Vec(0,0.0,0))
 	end
-end+end
+
+function server.init()
+    objects = FindShapes("obj")
+    objects2 = FindShapes("obj2")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local active = GetString("savegame.mod.options")
+        local menuoptions = GetString("level.menuoptions")
+        if active == "" and menuoptions =="op3" then
+        	activate()
+        end
+        if active == " extra" and menuoptions =="op3" then
+        	activate2()
+        end
+    end
+end
+

```

---

# Migration Report: Main Menu\scripts\display.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\scripts\display.lua
+++ patched/Main Menu\scripts\display.lua
@@ -1,16 +1,4 @@
-function draw()
-	local menuoptions = GetString("level.menuoptions")
-
-	if menuoptions =="op1" then
-		draw_gamemode()
-	end
-
-	if menuoptions =="op2" then
-		draw_timeweather()
-	end
-
-end
-
+#version 2
 function draw_timeweather()
 	lvl = GetString("savegame.mod.time")
 	lvl2 = GetString("savegame.mod.weather")
@@ -29,4 +17,17 @@
 		UiScale(UiWidth()/2210)
 		UiImage("MOD/option/"..lvl3..".png")
 	UiPop()
-end+end
+
+function client.draw()
+    local menuoptions = GetString("level.menuoptions")
+
+    if menuoptions =="op1" then
+    	draw_gamemode()
+    end
+
+    if menuoptions =="op2" then
+    	draw_timeweather()
+    end
+end
+

```

---

# Migration Report: Main Menu\scripts\uis\boeing_737_Ui_functions.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/Main Menu\scripts\uis\boeing_737_Ui_functions.lua
+++ patched/Main Menu\scripts\uis\boeing_737_Ui_functions.lua
@@ -1,12 +1,17 @@
+#version 2
 function map_737_tab_sizes( ... )
 
 end
+
 function map_737_cabin_options_tab()
 
 end
+
 function map_737_time_weather_tab()
 
 end
+
 function map_737_other_tab()
 
-end+end
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
@@ -1,23 +1,25 @@
-function init()
-	latetest_ver = "0.8.0"
-    -- current_ver = "0.7.0"
-    current_ver = GetString('game.version')
-	if current_ver < latetest_ver then
-		SetBool('map.version.outdated',true)
-	else
-		SetBool('map.version.outdated',false)
-	end	
+#version 2
+function server.init()
+    latetest_ver = "0.8.0"
+       -- current_ver = "0.7.0"
+       current_ver = GetString('game.version')
+    if current_ver < latetest_ver then
+    	SetBool('map.version.outdated',true, true)
+    else
+    	SetBool('map.version.outdated',false, true)
+    end	
 end
--- map.version.outdated
 
-function tick()
-	--Put a scripting menu button on the pause menu for all levels, except the main menu
-	if not string.find(GetString("game.levelpath"), "main.xml") then
-		if PauseMenuButton("Main menu") then
-			StartLevel("", "MOD/main.xml")
-		end
-        if GetBool("map.version.outdated") == true then
-			Menu()
-		end
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not string.find(GetString("game.levelpath"), "main.xml") then
+        	if PauseMenuButton("Main menu") then
+        		StartLevel("", "MOD/main.xml")
+        	end
+               if GetBool("map.version.outdated") == true then
+        		Menu()
+        	end
+        end
+    end
 end
+

```
