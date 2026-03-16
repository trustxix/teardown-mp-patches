# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,113 +1,24 @@
-Projectile_Body = {"ProjXml"}
-XmlLight = {"LightXml"}
-
-function init()
-	RegisterTool("fFlash", "Final Flash", "MOD/vox/InvisHand.vox")
-	SetBool("game.tool.fFlash.enabled", true)
-	SetFloat("game.tool.fFlash.ammo", 101)
-	
-	ExplFlash = 0
-	ExplFlash1 = 0
-	ToolReady = 0
-	coolDown = 0
-	Flashtimer = 0
-	expltimer = 0
-	ProjParti = 0
-	ProjPart = false
-	explactive = false
-	toolactive = false
-	kamefiresound = false
-	pvell = false
-	lesslaggymode = false
-	explosiontesthappened = false
-	explosiontesthappened1 = false
-	explosiontesthappened2 = false
-	timer = 0
-	Power = 1
-	Power1 = 0
-	mhT = 0
-	inuse = 0
-	uirng = 0
-	uirng1 = 0
-	beamparticl = 0
-	strength = 10
-	maxDist = 50
-	maxMass = 200000
-	distancetest = 0
-	pushtimer = 0
-	explosiontest = -2000000
-	hitcount = 0
-	SCc = 0
-	kameChargee = 0
-	uiheight = -1
-	uitexttimer = 0
-	playsndrng = 0
-	playsndrng1 = 0
-	fFlashactive = false
-	HandAnim = false
-	rHandT = 0
-	LightFlash = 0
-	EnergyBallFlicker = 0
-	LightningFlicker = 0
-	DImpact = true
-	EnvBack = false
-	FFlashFLoopStart = false
-	FFlashLT = 0
-	FFlashwasactive = false
-	FFlashwasactiveT = 0
-	mousex = 0
-	mousey = 0
-	mousex2 = 0
-	mousey2 = 0
-	HandSmokeT = 0
-	HandSmoke = false
-	SRndSize = 0
-	
-	KameLaunch = LoadLoop("snd/KameLaunchLatest.ogg")
-	KameFire = LoadSound("snd/KameFire.ogg")
-	KameFire1 = LoadSound("snd/KameFire1.ogg")
-	KameExplo = LoadSound("snd/KameExplo.ogg")
-	KameCharge = LoadSound("snd/KameCharge.ogg")
-	KameCharge1 = LoadSound("snd/KameCharge1.ogg")
-	ChargePower = LoadLoop("snd/ChargeSFX.ogg")
-	fFlashExplosion = LoadSound("snd/FFlashExplosion.ogg", 500)
-	fFlashExplosion2 = LoadSound("snd/FFlashExplosion2.ogg", 500)
-	fFlashLightExpl = LoadSound("snd/FFlashLightExpl.ogg")
-	FFlashStartUp = LoadLoop("snd/FFlashStartUp.ogg", 500)
-	FinalFlashFire = LoadLoop("snd/FinalFlashFire.ogg")
-	Earthquake = LoadLoop("snd/Earthquake.ogg", 500)
-	RockDestruction = LoadSound("snd/RockDestruction.ogg")
-	RockDestruction2 = LoadSound("snd/RockDestruction2.ogg")
-	RockDestruction3 = LoadSound("snd/RockDestruction3.ogg")
-	FinalThunder = LoadSound("snd/FinalThunder.ogg")
-	FinalThunder2 = LoadSound("snd/FinalThunder2.ogg")
-	FinalFlashChargeLightning = LoadSound("snd/FinalFlashChargeLightning.ogg")
-		
-		
-		FadeLightTest = LoadSprite("img/FadeLightTest.png")
-		FadeLightTest2 = LoadSprite("img/FadeLightTest2.png")
-		FadeLightTest3 = LoadSprite("img/FadeLightTest3.png")
-		SquareGlow = LoadSprite("img/SquareGlow.png")
-		Square = LoadSprite("img/Square.png")
-	lightningsprite = LoadSprite("img/Lightning_Bolt.png")
-	Glow = LoadSprite("img/Glow.png") 
-	GlowTexture2 = LoadSprite("img/GlowTexture2.png")
-	GlowTexture = LoadSprite("img/GlowTexture.png") 
-	OuterGlow = LoadSprite("img/OuterGlow.png") 
-	WhiteLine = LoadSprite("img/WhiteLine.png")
-	ConvergingRing = LoadSprite("img/ConvergingRing.png")
-	ConvergingRing2 = LoadSprite("img/ConvergingRing2.png")
-	ConvergingRingGlow = LoadSprite("img/ConvergingRingGlow.png")
-	ConvergingRingGlow2 = LoadSprite("img/ConvergingRingGlow2.png")
-	ConvergingRingTextureTest = LoadSprite("img/ConvergingRingTextureTest.png")
-	CrownFlare2 = LoadSprite("img/CrownFlare2.png")
-	Glow2 = LoadSprite("img/Glow2.png")
-	HoriFlare = LoadSprite("img/HoriFlareThin.png")
-
-end
+#version 2
+local Auras = {}
+local FireGusts = {}
+local Lightnings = {}
+local projHits = {}
+local projectiles = {}
+local shortestLifetime = math.huge
+local shortestLifetimeProjectileInfo = nil
+local detectedBodies = {}
+local Transition = 0
+local grabT = false
+local repulsionStrength = 4
+local minDistance = 2
+local gravity = Vec(0, -9.81, 0)
+local wallPushRadius = 2
+local wallPushForce = 1000
+local isolationRange = 1
+local heatStrength = 0
 
 function canShoot()
-	local vehicle = GetPlayerVehicle()
+	local vehicle = GetPlayerVehicle(playerId)
 	if vehicle ~= 0 then
 		local driverPos = GetVehicleDriverPos(vehicle)
 		local t = GetVehicleTransform(vehicle)
@@ -200,7 +111,6 @@
     return a*(1-f)+b*f
 end
 
-distortions = {}
 function SpawnDistortion(pos, vel, lifetime, DistortionSize, layerC, timeScale, debugMode) --layerC is layercount, so how many UiWindows u need per point
 	table.insert(distortions, {
 		pos = VecCopy(pos),
@@ -215,121 +125,6 @@
 	})
 end
 
-function draw(dt)
-	for i = #distortions, 1, -1 do
-		local p = distortions[i]
-		-- update position
-		
-		local camPos = GetCameraTransform().pos
-		local dirToCam = VecNormalize(VecSub(camPos, p.pos))  -- from projectile to camera
-		local distToCam = VecLength(VecSub(camPos, p.pos))
-
-		local hit2, dist2, normal2, shape2 = QueryRaycast(p.pos, dirToCam, distToCam)
-		if hit2 then
-			p.isVisible = 0
-		elseif not hit2 then
-			p.isVisible = 1
-		end
-
-		if p.time > p.lifetime then
-			table.remove(distortions, i)
-		else
-			-- project world position to screen
-			local x, y, dist = UiWorldToPixel(p.pos)
-			if dist > 0 then
-				local newtime = p.time * 1
-				local timeFactor = 1 - (newtime / p.lifetime)  -- shrink over time
-				local blurStrength = timeFactor
-				local camPos = GetCameraTransform().pos
-				local distToPlayer = VecLength(VecSub(p.pos, camPos))
-
-				local scaleComp = 1 / math.max(1, dist*4)
-
-				local baseSize = math.max(0.1, math.min(2825, p.DistortionSize * 25 - distToCam*5)) -- this limits the base size so u gotta increase it if u want larger distortions
-				
-				local layers = math.ceil(math.max(0, (p.layerC) * (1 - (p.time / p.lifetime))))
-
-				if p.debugMode then
-					DebugCross(p.pos, 1)
-				end
-
-				for j = 1, layers do
-					local layerProgress = (j - 1) / (layers - 1)
-					local growthFactor = 1 + layerProgress * 3
-					local size = baseSize * growthFactor * timeFactor -- maybe boolean for size time factor
-					if p.timeScale then
-						size = baseSize * growthFactor * timeFactor
-					else
-						size = baseSize * growthFactor
-					end
-					local falloff = 1 - layerProgress
-					local layerBlur = blurStrength * falloff
-					local layerAlpha = 0.02 * blurStrength * falloff
-
-					local scaledSize = math.max(1, size * scaleComp) -- center it
-					local halfSize = scaledSize / 2
-
-					UiPush()
-						UiTranslate(x - halfSize, y - halfSize)
-						UiWindow(scaledSize, scaledSize, true, false)
-						UiPush()
-							if p.isVisible == 1 then
-								UiBlur(layerBlur / 100)
-								UiColor(1, 0, 0, 1)
-								if p.debugMode then
-									UiRectOutline(scaledSize, scaledSize, 2)
-								end
-							end
-						UiPop()
-					UiPop()
-				end
-			end
-		end
-	end
-    if GetString("game.player.tool") == "fFlash" and GetPlayerVehicle() == 0 then
-		
-		if InputDown("lmb") then
-			local uiposx = 900 + math.random(Power/25*0.1, Power/50*2)
-			 UiPush()
-				local uiposx1 = uiposx + math.random(Power/50+1, Power/50+2)
-				UiTranslate(UiCenter()+uiposx, UiMiddle())
-				UiAlign("center middle")
-				bluecolor = Power/100
-				bluecolor1 = bluecolor-math.random(-100, 75)/1000
-				local val = math.random(0, Power)/100
-				UiColor(1,1,0, 10)
-				UiImageBox("ui/common/gradient.png", UiWidth()-2000,uiheight*1.1, 0, 0)
-			UiPop()
-			local uiposx = 900 + math.random(Power/50*0.1, Power/50*2)
-			UiPush()
-				UiTranslate(UiCenter()+uiposx, UiMiddle())
-				UiAlign("center middle")
-				bluecolor = Power/100
-				bluecolor1 = bluecolor-math.random(-100, 75)/1000
-				local val = math.random(0, Power)/100
-				UiColor(1,1,val, 10)
-				UiImageBox("ui/common/gradient.png", UiWidth()-1990,uiheight, 0, 0)
-			UiPop()
-			UiPush()
-				UiTranslate(UiCenter()+uiposx, UiMiddle())
-				UiAlign("center middle")
-				local val = math.random(0, Power)/100
-				UiColor(1,1,val, 10)
-				UiFont("bold.ttf", 42+val*4)
-				UiTextOutline(0,0,0,5,0.5)
-				UiText(math.ceil(Power))
-			UiPop()
-		end
-
-		if toolactive == true and InputDown("lmb") and GetString("game.player.tool") == "fFlash" and GetPlayerVehicle() == 0 then
-		--UiBlur(uirng)
-		end
-	
-	end
-end
-
-local Auras = {}
-
 function spawnAura(startPos, controlPos, endPos)
 	local Aura = {
 		startPos = startPos,
@@ -341,8 +136,6 @@
 	}
     table.insert(Auras, Aura)
 end
-
-local FireGusts = {}
 
 function spawnFireGust(startPos, velocity, maxDistance)
     local FireGust = {
@@ -362,8 +155,6 @@
     }
     table.insert(FireGusts, FireGust)
 end
-
-local Lightnings = {}
 
 function spawnLightningPoint(pos, dir, distance, color)
     local Lightning = {
@@ -385,8 +176,6 @@
     }
     return Lightning
 end
-
-local projHits = {}
 
 function spawnProjHit(startPos, velocity, maxDistance, Trans)
     local projHit = {
@@ -413,13 +202,11 @@
     table.insert(projHits, projHit)
 end
 
-local projectiles = {}
-
 function spawnProjectile(startPos, velocity, maxDistance)
     local projectile = {
         startPos = startPos,
         velocity = velocity,
-		--ProjBod = Spawn("MOD/" .. Projectile_Body[#Projectile_Body] .. ".xml", Transform(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5)), GetPlayerTransform(true).rot))[1],
+		--ProjBod = Spawn("MOD/" .. Projectile_Body[#Projectile_Body] .. ".xml", Transform(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5)), GetPlayerTransform(playerId, true).rot))[1],
         maxDistance = maxDistance,
         traveledDistance = 0,
         hit = false,
@@ -430,11 +217,6 @@
     }
     table.insert(projectiles, projectile)
 end
-
-hitPos = Vec()
-
-local shortestLifetime = math.huge  
-local shortestLifetimeProjectileInfo = nil
 
 function CastHeatCone(camTr, heatMult, maxAngle, centralRayDist, rayDist, pointsTable, voxelGridTable)
 	local origin = camTr.pos
@@ -512,408 +294,6 @@
 
 	return centralRayDist, heatHitPos
 end
-
-function update(dt)
-	updateFlames(dt)
-	
-	for i = #projHits, 1, -1 do
-        local projHit = projHits[i]
-		projHit.lightT = projHit.lightT - dt*2
-		projHit.lightT = math.max(0, projHit.lightT)
-		projHit.DirT = projHit.DirT - dt*4
-		projHit.DirT = math.max(0, projHit.DirT)
-        --local projHit.randomDir = math.random(1, 4)
-        --local projHit.explosionDir = nil
-		if projHit.DirT <= 0 then
-			projHit.FireBall = projHit.FireBall + dt*2
-			math.min(1, projHit.FireBall)
-			projHit.FireBallBack = projHit.FireBallBack - dt*2
-			math.max(0, projHit.FireBallBack)
-			if projHit.FireBall <= 0.1 then
-				for x=1, 50 do
-					ParticleReset()
-					ParticleRadius(Power/200, Power/100)
-					ParticleColor(1,0.2,0)
-					ParticleType("smoke")
-					ParticleAlpha(1, 0)
-					ParticleEmissive(5, 0)
-					ParticleTile(5)
-					ParticleCollide(1)
-					ParticleDrag(0.25)
-					SpawnParticle(projHit.startPos, rndVec(Power/3), math.random(50, 50)/100)
-				end
-				for x=1, 25 do
-					ParticleReset()
-					ParticleRadius(math.max(0.05, Power/1000), 0)
-					ParticleColor(1,0.3,0.2)
-					ParticleAlpha(1)
-					ParticleEmissive(5)
-					ParticleTile(6)
-					ParticleCollide(1)
-					ParticleGravity(-16)
-					ParticleDrag(0)
-					ParticleStretch(0)
-					SpawnParticle(projHit.startPos, rndVec(Power/3), math.random(250, 350)/100)
-				end
-			end
-			if projHit.FireBall >= 0.1 and projHit.FireBall <= 0.2 then
-				for x=1, Power*1.5 do
-					ParticleReset()
-					ParticleRadius(Power/200, Power/100)
-					ParticleType("smoke")
-					ParticleAlpha(0.4, 0, "easein")
-					ParticleEmissive(5, 0, "easeout")
-					ParticleTile(0)
-					ParticleColor(0,0,0, 0.01,0.01,0.01, "easeout")
-					ParticleCollide(1)
-					ParticleDrag(x/150/2)
-					SpawnParticle(projHit.startPos, rndVec(x/1.5), math.random(220, 340)/100)
-				end
-			end
-			if projHit.FireBall <= 0.1 then
-				for x=1, 20 do
-					local rnd = rndVec(10)
-					local pos = VecAdd(projHit.startPos, rnd)
-					--SpawnDistortion(pos, VecScale(rnd, 16), 0.5, 200, 15, false, false)
-				end
-			end
-			
-			if projHit.FireBallBack >= 0 then
-
-			end
-		end
-		
-		--PointLight(projHit.startPos, 1,1,0.25, projHit.lightT*0)
-		projHit.timer = projHit.timer + dt
-		if projHit.timer >= 5 then
-			table.remove(projHits, i)
-		end
-
-		if projHit.Hbool then
-		projHit.Hbool = false
-		local distance = VecLength(VecSub(GetPlayerTransform(true).pos, projHit.startPos)) 
-		
-		local hitPos = projHit.startPos
-		SCc = 0.009*Power
-		ShakeCamera(SCc/2)
-				
-		playsndrng = playsndrng + 1
-		playsndrng1 = playsndrng1 + 1
-		if playsndrng > 3 then
-			if distance < 50 then
-				if Power < 40 then
-					PlaySound(fFlashLightExpl, hitPos, Power/60*3)
-				end
-			end
-			playsndrng = 0
-		end
-
-		if playsndrng1 > 2 then
-			if distance <= 50 then
-				if Power > 40 then
-					PlaySound(fFlashExplosion, hitPos, Power/175*10, Power/175*10, math.random(1000, 1000)/1000)
-				end
-			elseif distance > 50 then
-				if Power > 40 then
-					PlaySound(fFlashExplosion, hitPos, Power/40*5, Power/40*5, math.random(1000, 1000)/1000)
-				end
-			end
-			playsndrng1 = 0
-		end		
-		
-			local particleVel2 = 35*Power/75
-			if particleVel2 < 0.3 then
-			particleVel2 = 0.3
-			end
-			ParticleAmount = Power
-			if ParticleAmount <= 30 then
-				ParticleAmount = 6
-			end
-			if ParticleAmount > 30 and ParticleAmount <= 60 then
-				ParticleAmount = 13
-			end
-			if ParticleAmount > 60 then
-				ParticleAmount = 20
-			end
-			for i=1, ParticleAmount do
-				ParticleReset()
-				--ParticleType("smoke")
-				ParticleGravity(0)
-				local SwaveVal = Power*2
-				if SwaveVal < 50 then SwaveVal = 50 end
-				local v = rndVec(Power/10)
-				ParticleAlpha(0.25, 0)
-				local particlradioos = 2*Power/100
-				if particlradioos < 0.15 then
-					particlradioos = 0.15
-				end
-				if particlradioos > 1.15 then
-					particlradioos = 1.15
-				end
-				ParticleRadius(particlradioos*1, particlradioos*2)
-				ParticleEmissive(5, 5, "easeout")
-				ParticleColor(1, 1, 0.25)
-				ParticleTile(0)
-				ParticleCollide(0)
-				ParticleDrag(0)
-				--SpawnParticle(hitPos, v, math.random(550, 1050)/1000)
-			end
-			for z=1, math.random(-1, 1) do
-				local ParticleAmount2 = Power
-				if ParticleAmount2 <= 30 then
-					ParticleAmount2 = 6
-				end
-				if ParticleAmount2 > 30 and ParticleAmount2 <= 60 then
-					ParticleAmount2 = 13
-				end
-				if ParticleAmount2 > 60 then
-					ParticleAmount2 = 20
-				end
-				for i=1, ParticleAmount2 do
-					ParticleReset()
-					--ParticleType("smoke")
-					ParticleGravity(-20)
-					local SwaveVal = Power*2
-					if SwaveVal < 50 then SwaveVal = 50 end
-					local v = rndVec(Power/1.5)
-					ParticleAlpha(1)
-					local particlradioos = 2*Power/100
-					if particlradioos < 0.15 then
-						particlradioos = 0.15
-					end
-					if particlradioos > 1.15 then
-						particlradioos = 1.15
-					end
-					ParticleRadius(particlradioos*0.4, 0)
-					ParticleEmissive(5, 5, "easeout")
-					ParticleColor(1, 1, 0.25)
-					ParticleTile(4)
-					ParticleStretch(0)
-					ParticleCollide(1)
-					ParticleDrag(0)
-					--SpawnParticle(hitPos, v, math.random(400, 1450)/1000)
-				end
-			end
-			for z=1, math.random(1, 1) do
-				local ParticleAmount2 = Power*4
-				if ParticleAmount2 <= 30 then
-					ParticleAmount2 = 6
-				end
-				if ParticleAmount2 > 30 and ParticleAmount2 <= 60 then
-					ParticleAmount2 = 13
-				end
-				if ParticleAmount2 > 60 then
-					ParticleAmount2 = 20
-				end
-				for i=1, ParticleAmount2 do
-					ParticleReset()
-					--ParticleType("smoke")
-					ParticleGravity(-20)
-					local SwaveVal = Power*2
-					if SwaveVal < 50 then SwaveVal = 50 end
-					local v = rndVec(Power*1)
-					ParticleAlpha(1)
-					local particlradioos = 2*Power/100
-					if particlradioos < 0.15 then
-						particlradioos = 0.15
-					end
-					if particlradioos > 1.15 then
-						particlradioos = 1.15
-					end
-					ParticleRadius(particlradioos*0.15, 0)
-					ParticleEmissive(5, 5, "easeout")
-					ParticleColor(1, 0.3, 0.25)
-					ParticleTile(4)
-					ParticleStretch(0)
-					ParticleCollide(1)
-					ParticleDrag(0)
-					--SpawnParticle(hitPos, v, math.random(1400, 2450)/1000)
-				end
-			end
-		end
-    end
-
-	for i = #distortions, 1, -1 do
-		local p = distortions[i]
-		p.pos = VecAdd(p.pos, VecScale(p.vel, dt))
-
-		p.time = p.time + dt
-	end
-	
-	for i = #Auras, 1, - 1 do
-		Aura = Auras[i]
-		Aura.t = Aura.t + dt / 4
-		if Aura.t > 1 then
-			Aura.t = 1 
-		end
-		
-		--Aura.endPos = Vec(10, 31 + math.sin(GetTime()*24.0)*3, 0)
-		
-		local direction = calculateBezierTangent(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
-		local normalizedDirection = VecScale(VecNormalize(direction), 50)
-		
-		local newPos = calculateBezierPoint(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
-		--SpawnParticle(newPos, VecAdd(normalizedDirection, rndVec(25)), 0.25)
-
-		--PointLight(newPos, 0,0,1, 3)
-
-		if Aura.t >= 1 then
-			table.remove(Auras, i)
-		end
-	end
-	
---LOOPEDSOUNDS
-	local FFLASHLOOP = GetSoundLoopProgress(FinalFlashFire)
-	if FFLASHLOOP >= 5.5 then
-		FFlashFLoopStart = false
-		SetSoundLoopProgress(FinalFlashFire, 5.5)
-	end 
-	
-		
-	for i = #FireGusts, 1, - 1 do
-		local FireGust = FireGusts[i]
-		FireGust.startPos = VecAdd(FireGust.startPos, VecScale(FireGust.velocity, 0.014))
-	end
-	
-	for i = 1, #Lightnings - 1 do
-		Lightnings[i].position = VecAdd(Lightnings[i].position, VecAdd(VecScale(GetPlayerVelocity(), 0.015), rndVec(0.025)))
-	end
-
-    table.sort(projectiles, function(a, b)
-        return (a.lifespan - a.timer) < (b.lifespan - b.timer)
-    end)
-
-    for i = #projectiles, 1, -1 do
-        local projectile = projectiles[i]
-
-        if not projectile.hit then
-
-            local displacement = VecScale(projectile.velocity, EaseInQuad(projectile.timer))
-            local newPos = VecAdd(projectile.startPos, displacement)
-
-			QueryRejectBody(GetToolBody())
-			QueryRequire("visible")
-            local hit, dist, normal, shape = QueryRaycast(projectile.startPos, VecNormalize(displacement), VecLength(displacement))
-
-            if hit then
-                local hitPoint = VecAdd(projectile.startPos, VecScale(VecNormalize(displacement), dist))
-                hitPos = hitPoint
-				spawnProjHit(projectile.startPos, Vec(), 10, GetPlayerTransform())
-
-				projectile.hit = true
-            else
-                projectile.startPos = newPos
-                projectile.traveledDistance = projectile.traveledDistance + VecLength(displacement)
-                hitPos = projectile.startPos
-                if projectile.traveledDistance >= projectile.maxDistance then
-                    projectile.hit = true
-                end
-            end
-			
-			if projectile.timer >= 5 or projectile.traveledDistance >= projectile.maxDistance then 
-				if projectile.timer < shortestLifetime then
-					shortestLifetime = projectile.timer
-					shortestLifetimeProjectileInfo = {
-						startPos = projectile.startPos,
-						velocity = projectile.velocity,
-						timer = projectile.timer
-					}
-					PointLight(shortestLifetimeProjectileInfo.startPos, 1, 1, 1, 250)
-				end
-			end
-			for x=1, math.random(-10, 1) do
-				ParticleReset()
-				ParticleType("smoke")
-				ParticleRadius(Power/30)
-				ParticleColor(0,0,1)
-				ParticleAlpha(0)
-				ParticleTile(4)
-				SpawnParticle(projectile.startPos, VecScale(VecNormalize(displacement), 150), 0.5)
-			end
-			
-			if projectile.hit and projectile.Hbool then
-				local paints = 2.4*Power/25
-				if paints < 0.8 then
-					paints = 0.8
-				end
-				if Power < 60 then
-					local makeh = 1.8*Power/30
-					local makeh1 = 1.8*Power/30
-					if makeh < 1 then
-						makeh = 1
-					end
-					if makeh1 < 0.6 then
-						makeh1 = 0.6
-					end
-					local pos = VecAdd(hitPos, rndVec(Power/40))
-					Paint(pos, paints, "explosion")
-					MakeHole(pos, makeh1/1, makeh1/1.55, makeh1/1.60)
-				elseif Power > 60 then
-					local pos = VecAdd(hitPos, rndVec(Power/40))
-					local makeh1 = 1.8*Power/30
-					Paint(pos, paints, "explosion")
-					MakeHole(pos, makeh1/1, makeh1/1.05, makeh1*Power/20/1.1)
-				end
-				local fd = 20
-				for i =1, 20 do
-					SpawnFire(VecAdd(hitPos, Vec(math.random(-1000,1000)*Power/fd/1000, math.random(-1000,1000)*Power/fd/1000, math.random(-1000,1000)*Power/fd/1000)))
-				end
-				
-				QueryRejectBody(GetToolBody())
-				max = 4*Power/20
-				local objectbodies = QueryAabbBodies( VecAdd(hitPos, Vec(-max, -max, -max)), VecAdd(hitPos, Vec(max, max, max)))
-				for i = 1, #objectbodies do
-					local objectbodies2 = objectbodies[i]
-					if IsBodyDynamic(objectbodies2) then
-					  local bb, bbba = GetBodyBounds(objectbodies2)
-					  local direction = VecSub(VecLerp(bb, bbba, 0.5), hitPos)
-					  local distance = VecLength(direction)
-					  local mass = GetBodyMass(objectbodies2)
-					  local angV = GetBodyAngularVelocity(objectbodies2)
-					  local angVel = Vec(math.random(5, 15), math.random(-15, -5), 0)
-					  direction = VecScale(direction, 1 / distance)
-					  if distance < max and mass < 500 then --max * 100
-					   local distScale = 1 - math.min(distance / max, 0.9)
-					  local vel = GetBodyVelocity(objectbodies2)
-						vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 7.5*Power/105 * distScale)) --50
-						SetBodyVelocity(objectbodies2, vel)
-						SetBodyAngularVelocity(objectbodies2, angVel)
-						elseif distance < max and mass > 500 then
-						local distScale = 1 - math.min(distance / max, 0.9)
-						local vel = GetBodyVelocity(objectbodies2)
-						vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 5*Power/105 * distScale)) --50
-						SetBodyVelocity(objectbodies2, vel)
-						end
-					  end
-				   end
-			end
-        end
-
-        projectile.timer = projectile.timer + dt*2
-        if projectile.timer >= projectile.lifespan or projectile.hit or projectile.traveledDistance >= projectile.maxDistance then
-			--hitPos = projectile.startPos
-			--detectBodies(projectile.startPos)
-            table.remove(projectiles, i)
-        end
-    end
-		if fFlashactive == true then
-			local t2 = GetCameraTransform()
-			local pos2 = t2.pos	
-			local dir2 = TransformToParentVec(t2, Vec(0, 0, -1))	
-			local hit2, dist2, shape2 = QueryRaycast(pos2, dir2, 200)
-			local hitpoint = VecAdd(pos2, VecScale(dir2, dist2))
-	
-			local t = GetCameraTransform()
-			local fwd = TransformToParentVec(t, Vec(-0.0075/dist2, 0.0075/dist2, -1))
-			local maxDist = 300
-			local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist)
-			if not hit then
-				dist = maxDist
-			end
-		end
-end
-
-local detectedBodies = {}
 
 function isBodyDetected(shape)
     for _, bodyInfo in ipairs(detectedBodies) do
@@ -1017,7 +397,7 @@
 					SpawnParticle(VecAdd(hitPos, rndVec(EnergyT/20)), VecScale(rnddir, math.random(0, 1000)/1000), 0.6 + bodyInfo.ExplosionSphere/2)
 				end]]
 		--FIRE VISUALS BELOW
-			local PtoHpos = VecLength(VecSub(GetPlayerTransform(true).pos, hitPos))
+			local PtoHpos = VecLength(VecSub(GetPlayerTransform(playerId, true).pos, hitPos))
 			if PtoHpos > 125 then
 				--PointLight(CMassPoint, 1, 0.5, 0, bodyInfo.Flash*100)
 			end
@@ -1236,12 +616,6 @@
     return a + (b - a) * t
 end
 
-local Transition = 0
-
-mousex3 = 0
-mousey3 = 0
-mousez3 = 0
-
 function getOutermostVoxels(shape)
     local xsize, ysize, zsize, scale = GetShapeSize(shape)
     local transform = GetShapeWorldTransform(shape)
@@ -1302,8 +676,6 @@
 		end
 	end
 end
-local grabT = false
-Flames = {}
 
 function spawnFlame(pos, lifetime)
 	local cam = GetCameraTransform()
@@ -1317,12 +689,7 @@
 		lifetime = lifetime or 2
 	})
 end
-	local repulsionStrength = 4
-	local minDistance = 2
-	local gravity = Vec(0, -9.81, 0)
-	local wallPushRadius = 2
-	local wallPushForce = 1000
-	local isolationRange = 1  -- range to check for nearby flames
+
 function updateFlames(dt)
 	for i = #Flames, 1, -1 do
 		local flame = Flames[i]
@@ -1391,6 +758,7 @@
 		end
 	end
 end
+
 function render(dt)
 		for i = #Flames, 1, -1 do
 			local flame = Flames[i]
@@ -1546,16 +914,16 @@
     --DrawSprite(frameIDs[currentFrame], Transform(Vec(0,25,0)), 12.2, 12.2, 1,1,1, 1, true, false)
 	
 	--[[if not InputDown("shift") then --testing camera stuff
-		PlayerTransform = GetPlayerTransform(true)
+		PlayerTransform = GetPlayerTransform(playerId, true)
 		mousex = mousex
 		mousey = mousey
 		mousex2 = mousex2
 		mousey2 = mousey2
 	elseif InputDown("shift") then
-		SetPlayerTransform(PlayerTransform, true)
+		SetPlayerTransform(playerId, PlayerTransform, true)
 		mousex3 = mousex3 + InputValue("camerax")*12
 		mousey3 = mousey3 + InputValue("cameray")*12
-		local lookat = QuatLookAt(GetPlayerTransform(true).pos, GetCameraTransform().pos)
+		local lookat = QuatLookAt(GetPlayerTransform(playerId, true).pos, GetCameraTransform().pos)
 		local tPosY = Transform(Vec(mousex3, mousey3), QuatRotateQuat(lookat, QuatEuler(-mousey3*18, -mousex3*18)))
 		SetCameraOffsetTransform(tPosY, true)
 	end]]
@@ -1622,7 +990,7 @@
 				local Srng = math.random(Power*1000, Power*2000)/1000/75*SRndSize*Power/100
 				if distance < 100 then
 					for j=1, Power/10 do
-						local DToP = VecLength(VecSub(projectiles[i].startPos, GetPlayerTransform(true).pos))
+						local DToP = VecLength(VecSub(projectiles[i].startPos, GetPlayerTransform(playerId, true).pos))
 						--if DToP >= 1 then DToP = 1 end
 						local newD = 50/DToP
 						if newD >= 3 then newD = 3 end
@@ -1730,19 +1098,12 @@
 end
 
 function getLastSpawnedProjectile()
-    if #projectiles > 0 then
+    if #projectiles ~= 0 then
         return projectiles[#projectiles] 
     else
         return nil 
     end
 end
-
-HandsoutL = 0
-HandsoutR = 0
-HandsRaised = 0 
-HandsForwards = 0
-FFlashEnded = false
-FFlashEndedT = 0
 
 function postUpdate(dt)
 --DebugPrint(FFlashEnded)
@@ -1773,8 +1134,8 @@
 		end
 
         local animator = GetPlayerAnimator()
-        local point_l = TransformToParentPoint(GetPlayerTransform(true), Vec(0,HandsRaised,HandsoutL))
-		local point_r = TransformToParentPoint(GetPlayerTransform(true), Vec(0,HandsRaised,-HandsoutR))
+        local point_l = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,HandsRaised,HandsoutL))
+		local point_r = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,HandsRaised,-HandsoutR))
 
         local pos_l = GetBoneWorldTransform(animator, "shoulder_l").pos
         local len_l = GetBoneChainLength(animator, "shoulder_l", "hand_l")
@@ -1789,1171 +1150,1785 @@
 	end
 end
 
-local heatStrength = 0
-
-points = {}
-
-function tick(dt)
-
-	for i = #projHits, 1, -1 do
-		local projHit = projHits[i]
-		if projHit.FireBall <= 2 then
-			local intensity = math.max(0, 1 - (projHit.FireBall / 1.75))
-			PointLight(projHit.startPos, 1, 0.2, 0, intensity*Power)
-		end
-	end
-	
-	SRndSize = math.random(0, 3)
-	
-	if GetString("game.player.tool") ~= "fFlash" then
-		HandsoutL = 0
-		HandsoutR = 0
-		HandsRaised = 0 
-		HandsForwards = 0
-		FFlashEnded = true
-		FFlashEndedT = 0
-		
-		kameChargee = 0
-		Power = 0
-		FFlashwasactive = false
-		FFlashwasactiveT = 1
-		fFlashactive = false
-		LightningFlicker = 0
-		EnergyBallFlicker = 0
-		
-		FFlashFLoopStart = false
-		SetSoundLoopProgress(FinalFlashFire, 0)
-		rHandT = 0
-		hitcount = 0
-		inuse = 0
-		toolactive = false
-		fFlashactive = false
-		LightFlash = Power
-		HandAnim = false
-		FFlashEnded = false
-		HandSmoke = false
-		HandSmokeT = 0
-	end
-	
-	if GetString("game.player.tool") == "fFlash" then --camerachange
-		if not fFlashactive and InputDown("lmb") and not FFlashwasactive then
-			mousex = mousex + InputValue("camerax")*12
-			if mousex >= 10 then mousex = 10 end
-			if mousex <= -10 then mousex = -10 end
-			mousey = mousey + InputValue("cameray")*12
-			if mousey >= 8 then mousey = 8 end
-			if mousey <= 2 then mousey = 2 end
-			Transition = 0 --Transition = Transition - dt
-			if not GetBool("game.paused") then
-				CamShake = math.random(Power*1000/100, Power*1000/75)/1000
-				CamShake2 = math.random(Power*1000/100, Power*1000/75)/1000
-				CamShake3 = math.random(Power*1000/100, Power*1000/75)/1000
-			elseif GetBool("game.paused") then
-				CamShake = 0
-				CamShake2 = 0
-				CamShake3 = 0
-			end
-			xVal = CamShake + -mousex
-			yVal = mousey/2 + Power/60 - 0.5 + CamShake2
-			zVal = mousey*1 + CamShake3 + Power/12 - 0.83
-			local tPosY = Transform(Vec(CamShake + -mousex - 0.2, mousey/2 + Power/60 - 1.25 + CamShake2, mousey*1 - 2 + CamShake3 + Power/12 - 0.83), QuatAxisAngle(Vec(0, 0, 0)))
-			SetCameraOffsetTransform(tPosY, true)
-		elseif fFlashactive or FFlashwasactive then
-			mousex2 = mousex2 + InputValue("camerax")*12
-			if mousex2 >= 10 then mousex2 = 10 end
-			if mousex2 <= -10 then mousex2 = -10 end
-			mousey2 = mousey2 + InputValue("cameray")*12
-			if mousey2 >= 8 then mousey2 = 8 end
-			if mousey2 <= 2 then mousey2 = 2 end
-			Transition = Transition + dt*2
-			if Transition >= 1 then Transition = 1 end
-				if not GetBool("game.paused") then
-					CamShake1 = math.random(Power*1000/100, Power*1000/75)/1000
-					CamShake12 = math.random(Power*1000/100, Power*1000/75)/1000
-					CamShake13 = math.random(Power*1000/100, Power*1000/75)/1000
-				elseif GetBool("game.paused") then
-					CamShake1 = 0
-					CamShake12 = 0
-					CamShake13 = 0
-				end
-			xVal2 = lerp(xVal, xVal*1.25 + -mousex2, Transition) + CamShake1
-			yVal2 = lerp(yVal, yVal*1.25 + mousey/2, Transition) + CamShake12
-			zVal2 = lerp(zVal, zVal*1.25 + mousey*1, Transition) + CamShake13
-			local tPosY = Transform(Vec(lerp(xVal, xVal*1.25 + -mousex2, Transition) + CamShake1, lerp(yVal, yVal*1.25 + mousey/2, Transition) + CamShake12, lerp(zVal, zVal*1.25 + mousey*1, Transition) + CamShake13), QuatAxisAngle(Vec(0, 0, 0)))
-			SetCameraOffsetTransform(tPosY, true)
-		end
-		if FFlashwasactive and not fFlashactive then 
-		
-			local Default = Transform(Vec(lerp(xVal2, 0, FFlashwasactiveT), lerp(yVal2, 0, FFlashwasactiveT), lerp(zVal2, 0, FFlashwasactiveT)), QuatAxisAngle(Vec(0, 0, 0)))
-			SetCameraOffsetTransform(Default, true)
-		end
-		--SetCameraOffsetTransform(tPosX, true)
-	end
-	
-	--[[if InputPressed("b") then
-		SetEnvironmentProperty("exposure", 0.2/10, 20)
-		SetEnvironmentProperty("skyboxtint", 0.1, 0.1, 0.1)
-		SetEnvironmentProperty("constant", 0.001, 0.001, 0.001)
-		SetPostProcessingProperty("bloom", 4)
-		SetPostProcessingProperty("saturation", 1)
-		SetPostProcessingProperty("colorbalance", 1, 1, 1)
-		SetEnvironmentProperty("fogParams", 200, 450, 0.15, 100)--SetEnvironmentProperty("fogParams", 50, 210, 0.9, 8)
-		SetEnvironmentProperty("sunSpread", 0.001)
-		SetEnvironmentProperty("fogColor", 0.1, 0.45, 1)
-	end]]
-	
-	if HandSmoke then
-		HandSmokeT = HandSmokeT + dt
-	end
-	
-	if HandSmokeT > 0.6 and HandSmokeT <= 5 then
-		local animator = GetPlayerAnimator()
-		ParticleReset()
-		ParticleTile(0)
-		ParticleColor(0.7,0.7,0.7)
-		ParticleEmissive(0)
-		ParticleRadius(0, 0.1)
-		ParticleGravity(0.9)
-		ParticleAlpha(0.6, 0)
-		ParticleCollide(0)
-		SpawnParticle(GetBoneWorldTransform(animator, "hand_l").pos, rndVec(math.random(0, 25)/100), 1)
-		ParticleReset()
-		ParticleTile(0)
-		ParticleColor(0.7,0.7,0.7)
-		ParticleEmissive(0)
-		ParticleRadius(0, 0.1)
-		ParticleGravity(0.9)
-		ParticleAlpha(0.6, 0)
-		ParticleCollide(0)
-		SpawnParticle(GetBoneWorldTransform(animator, "hand_r").pos, rndVec(math.random(0, 25)/100), 1)
-	end
-
-	if HandSmokeT >= 5 then
-		HandSmokeT = 0
-		HandSmoke = false
-	end
-
-	for i = #Auras, 1, - 1 do
-		Aura = Auras[i]
-		
-		local direction = calculateBezierTangent(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
-		local normalizedDirection = VecScale(VecNormalize(direction), 25)
-		
-		local newPos = calculateBezierPoint(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
-		
-			for i=1, 20 do
-				local RndV = rndVec(0)
-				local Pos = VecAdd(newPos, RndV)
-				local Rot = QuatLookAt(newPos, GetCameraTransform().pos)--QuatLookAt(newPos, Pos)
-				local T = Transform(Pos, QuatRotateQuat(Rot, QuatEuler(math.random(0, 0), Aura.SpriteRnd, math.random(0, 0))))
-				local toCam = QuatLookAt(newPos, GetCameraTransform().pos)
-				local T2 = Transform(newPos, QuatRotateQuat(toCam, QuatEuler(0,0,0)))
-				local AuraSize = 0.01/Aura.t
-				if AuraSize >= 1 then AuraSize = 1 end
-				local sizeRnd = math.random(-i*1000/60, i*1000/60)/1000
-				--DrawSprite(Glow, T, i/4+ math.sin(GetTime()*math.random(500, 2500)/1000)*3, i/48, 1.0, 1, 0.4, 1, true, false) --50000
-				--DrawSprite(HoriFlare, T, i/50+sizeRnd, i/50+sizeRnd, 1.0, 1, 0.4, i/5000, true, false)
-				--DrawSprite(Glow, T2, i/4+sizeRnd, i/4+sizeRnd, 1.0, 1, 0.5, i/2500000, true, false)
-				--DrawSprite(Glow, T2, i/7+sizeRnd, i/7+sizeRnd, 1.0, 1, 0.5, i/1500000, true, false)
-				--DrawSprite(Glow, T2, i/13+sizeRnd, i/13+sizeRnd, 1.0, 1, 0.5, i/500000, true, false)
-			end
-		--PointLight(newPos, 1,1,0, 3)
-
-	end
-		
-	editBodies(dt)
-	
-	
-	for i = #FireGusts, 1, -1 do
-		local FireGust = FireGusts[i]
-		FireGust.ColorT = FireGust.ColorT - dt*1.5
-		if FireGust.ColorT <= 0 then FireGust.ColorT = 0 end
-		if FireGust.ColorT >= 1 then FireGust.ColorT = 1 end
-		FireGust.FireGT = FireGust.FireGT - dt*2
-		if FireGust.FireGT <= 0 then FireGust.FireGT = 0 end
-		if FireGust.FireGT >= 1 then FireGust.FireGT = 1 end
-		FireGust.FireGTB = FireGust.FireGTB - dt*4
-		if FireGust.FireGTB <= 0 then FireGust.FireGTB = 0 end
-		if FireGust.FireGTB >= 1 then FireGust.FireGTB = 1 end
-		local FireGTB = FireGust.FireGTB
-		if FireGTB <= 0 then FireGTB = 0 end
-		if FireGTB >= 1 then FireGTB = 1 end
-		FireGust.FireGBackF = FireGust.FireGBackF - dt*4
-		if FireGust.FireGBackF <= 0 then FireGust.FireGBackF = 0 end
-		if FireGust.FireGBackF >= 1 then FireGust.FireGBackF = 1 end
-		FireGust.Light = FireGust.Light - dt*2
-		if FireGust.Light <= 0 then FireGust.Light = 0 end
-		if FireGust.Light >= 1 then FireGust.Light = 1 end
-		PointLight(FireGust.startPos, FireGust.ColorT , math.random(FireGust.ColorT*1000/4, FireGust.ColorT*1000/3)/1000, 0, FireGust.Light*15)
-		for z=1, 20 do
-			ParticleReset()
-			ParticleRadius(math.random(FireGust.FireGT*2050, FireGust.FireGT*4050)/1000*0.45, 0, "easeout")
-			ParticleSticky(0)
-			ParticleEmissive(FireGust.FireGBackF*10, 0)
-			ParticleTile(0)
-			ParticleAlpha(FireGust.FireGT, 0, "easein")
-			ParticleDrag(0.25)
-			if FireGust.FireGBackF <= 0.05 then
-				Prngsmoke = 0
-			elseif FireGust.FireGBackF > 0.05 then
-				Prngsmoke = 0
-			end
-			ParticleColor(FireGust.ColorT + Prngsmoke, math.random(FireGust.ColorT*1000/3, FireGust.ColorT*1000/2)/1000 + Prngsmoke, 0 + Prngsmoke, 0,0,0)
-			ParticleCollide(0)
-			ParticleGravity(0)
-			ParticleStretch(6, 0)
-			local GustLifetime = 0.1/FireGust.ColorT
-			if GustLifetime > 0.5 then GustLifetime = 0.5 end
-			SpawnParticle(VecAdd(FireGust.startPos, rndVec(FireGTB/20)), VecAdd(VecScale(FireGust.velocity, math.random(0, 200)/1000), rndVec(GustLifetime*15)), 0.5 + GustLifetime)
-		end
-			FireGust.timer = FireGust.timer + dt
-			if FireGust.timer >= 1 then
-				table.remove(FireGusts, i)
-			end
-	end
-	
-	if GetString("game.player.tool") == "fFlash" and canShoot() and InputPressed("lmb") and not fFlashactive then
-		PTF = GetPlayerTransform(true)
-		DImpact = true
-	end	
-	if GetString("game.player.tool") == "fFlash" and canShoot() and InputDown("lmb") and not fFlashactive then
-		local ParticlePos = TransformToParentPoint(GetPlayerTransform(true), Vec(0,0,0))
-		QueryRejectBody(GetToolBody())
-		local hit, d = QueryRaycast(ParticlePos, Vec(0, -1, 0), 5)
-		local PlayerT = GetPlayerTransform(true)
-		if hit or not hit then --change to if hit then somebool active or don't use a raycast at all
-			SetPlayerVelocity(Vec(0,0,0))
-			PlayerT.pos = VecAdd(PTF.pos, Vec(0,lerp(0, Power/25, Power/100),0))
-			SetPlayerTransform(PlayerT, true)
-			
-				LightningFlicker = LightningFlicker + dt/4
-				if LightningFlicker >= 1 then LightningFlicker = 1 end
-				EnergyBallFlicker = EnergyBallFlicker + dt*LightningFlicker
-				if EnergyBallFlicker >= 0.1 then EnergyBallFlicker = 0 end
-				local Flicker = math.abs(EnergyBallFlicker - 0.05)
-				local p = TransformToParentPoint(GetPlayerTransform(true), Vec(0, 1, -1.5 + -Power/35))
-				
-				PlayLoop(Earthquake, p, 10, 10, math.random(1000, 1250)/1000)
-				PlayLoop(FFlashStartUp, p, 20)
-				local raritynum = 3
-				local rarity = math.random(1, raritynum)
-				if LightningFlicker < 0.75 and EnergyBallFlicker >= 0 then
-					local p = TransformToParentPoint(GetPlayerTransform(true), Vec(0, 1, -1.5 + -Power/35))
-					PointLight(VecAdd(p, rndVec(Power/30)), 1.0, 1, 0.2+math.sin(GetTime()*18.0)*0.3, math.random(Power*1000/8, Power*1000/5)/1000)
-					local Lpos2 = VecAdd(GetPlayerTransform(true).pos, Vec(math.random(-8000, 8000)/1000,math.random(-0, 8000)/1000,math.random(-8000, 8000)/1000)) --maybe math.sin Gettime()?
-					--createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 10, math.random(0, 3500)/1000)
-					for x=1, 8 do
-						local dir =  rndVec(1 + Power/75)
-						local pos = VecAdd(p, dir)
-						SpawnDistortion(pos, VecScale(dir, 16), 0.5, Power/2, 10, false, false)
-					end
-					for i=1, Power*2 do
-						local RndV = rndVec(Power/200)
-						local Pos = VecAdd(p, RndV)
-						local Rot = QuatLookAt(p, Pos)
-						local T = Transform(Pos, Rot)
-						local toCam = QuatLookAt(p, GetCameraTransform().pos)
-						local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
-						local sizeRnd = math.random(i*1000/120, i*1000/120)/1000 - math.random(Power*1000/100*0.25, Power*1000/100*1)/1000
-						DrawSprite(Glow, T, i/200+sizeRnd, i/200+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/100, true, false) --beamstart
-						DrawSprite(Glow, T, i/100+sizeRnd, i/100+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/100000, true, false)
-						--DrawSprite(Glow, T, i/15+sizeRnd, i/15+sizeRnd, 1.0, 1, 0.2+math.sin(GetTime()*18.0)*0.1, i/200000, true, false)
-					end
-					for i=10, Power/4 do
-						ParticleReset()
-						ParticleTile(5)
-						ParticleCollide(0)
-						ParticleEmissive(5, 0)
-						ParticleRadius(0.25 + Power/300, 0, "easeout")
-						ParticleGravity(-5)
-						ParticleAlpha(1, 0)
-						ParticleColor(1,1,0.25)
-						ParticleStretch(10)
-						local rndV = rndVec(15)
-						local rndpos = VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndV)
-						local pPos = TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35))
-						local changerndpos = VecAdd(VecAdd(rndpos, VecScale(VecNormalize(VecSub(pPos, rndpos)), Power/math.random(6,8))), math.cos(math.sin(GetTime()*10.0)*90))
-						local dir = VecNormalize(VecSub(pPos, changerndpos))
-						local dist = VecLength(VecSub(pPos, changerndpos))
-						--SpawnParticle(changerndpos, VecScale(dir, dist*14), Power/100/12)
-						for z=1, math.random(-7, 1) do
-							--SpawnParticle(changerndpos, VecScale(dir, dist*28), Power/100/12)
-						end
-					end
-					for z=1, math.random(-15, 1) do
-						PlaySound(FinalFlashChargeLightning, GetPlayerTransform().pos, Power/100, Power/100, math.random(800, 1200)/1000)
-						ShakeCamera(Power/1000*6)
-						for c=1, 3 do
-							local Lpos2 = VecAdd(GetPlayerTransform(true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 6500)/1000, Vec(1,1,0.4))
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 6500)/1000, Vec(1,1,0.4))
-							for x=1, 25 do
-								local dir =  rndVec(5 + Power/50)
-								local pos = VecAdd(p, dir)
-								SpawnDistortion(pos, VecScale(dir, 8), 1, Power*2, 15, false, false)
-							end
-						end
-						for x=1, 50 do
-							PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
-						end
-						for i=1, Power/13 do
-							ParticleReset()
-							ParticleTile(4)
-							ParticleCollide(0)
-							ParticleEmissive(5)
-							ParticleRadius(0.25 + Power/500, 0)
-							ParticleGravity(0)
-							ParticleStretch(8)
-							ParticleAlpha(1)
-							ParticleColor(1,1,0.25)
-							SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(Power*1600, Power*1600)/1000), Power/100/11)
-						end
-					end
-					for z=1, math.random(-12, 1) do
-						PlaySound(FinalFlashChargeLightning, GetPlayerTransform().pos, Power/200, Power/200, math.random(800, 1200)/1000)
-						for c=1, 3 do
-							local Lpos2 = VecAdd(GetPlayerTransform(true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
-						end
-						for x=1, 25 do
-							PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
-						end
-						for i=1, Power/13 do
-							ParticleReset()
-							ParticleTile(4)
-							ParticleCollide(0)
-							ParticleEmissive(5)
-							ParticleRadius(0.2 + Power/750, 0)
-							ParticleGravity(0)
-							ParticleStretch(4.5)
-							ParticleAlpha(1)
-							ParticleColor(1,1,0.2)
-							SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(Power*1100, Power*1100)/1000), Power/100/12)
-						end
-					end
-				elseif LightningFlicker >= 0.75 and EnergyBallFlicker >= 0 then
-					local p = TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35))
-					PointLight(VecAdd(p, rndVec(Power/30)), 1.0, 1, 0.2+math.sin(GetTime()*18.0)*0.3, math.random(Power*1000/8, Power*1000/5)/1000)
-					PlayLoop(Earthquake, p, 10, 10, math.random(1000, 1250)/1000)
-					PlayLoop(FFlashStartUp, p, 20, 20, 1)
-					for i=1, Power*2 do
-						local RndV = rndVec(Power/200)
-						local Pos = VecAdd(p, RndV)
-						local Rot = QuatLookAt(p, Pos)
-						local T = Transform(Pos, Rot)
-						local toCam = QuatLookAt(p, GetCameraTransform().pos)
-						local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
-						local sizeRnd = math.random(-i*1000/120, i*1000/120)/1000
-						DrawSprite(Glow, T, i/200+sizeRnd, i/200+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/100, true, false) --beamstart
-						DrawSprite(Glow, T, i/50+sizeRnd, i/50+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.1, i/100000, true, false)
-					end
-					--OUTER SPHERE
-					for i=10, Power/4 do
-						ParticleReset()
-						ParticleTile(5)
-						ParticleCollide(0)
-						ParticleRadius(0.25 + Power/300, 0, "easeout")
-						ParticleGravity(-5)
-						ParticleAlpha(1, 0)
-							ParticleEmissive(5, 0)
-							ParticleColor(1,1,0.25)
-						ParticleStretch(10)
-						local rndV = rndVec(15)
-						local rndpos = VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndV)
-						local pPos = TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35))
-						local changerndpos = VecAdd(VecAdd(rndpos, VecScale(VecNormalize(VecSub(pPos, rndpos)), Power/math.random(6,8))), math.cos(math.sin(GetTime()*10.0)*90))
-						local dir = VecNormalize(VecSub(pPos, changerndpos))
-						local dist = VecLength(VecSub(pPos, changerndpos))
-						SpawnParticle(changerndpos, VecScale(dir, dist*7), Power/100/12)
-						for z=1, math.random(-7, 1) do
-							SpawnParticle(changerndpos, VecScale(dir, dist*20), Power/100/12)
-						end
-					end
-				
-					for i=1, Power/5 do
-						ParticleReset()
-						ParticleTile(5)
-						ParticleCollide(0)
-						ParticleEmissive(5, 0)
-						ParticleRadius(0.25 + Power/100, 0)
-						ParticleGravity(-5)
-						ParticleAlpha(0.3, 0)
-						ParticleColor(1,1,0)
-						--SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(0, Power*2400)/1000), Power/100/15)
-					end
-					for x=1, 8 do
-						local dir =  rndVec(1 + Power/75)
-						local pos = VecAdd(p, dir)
-						SpawnDistortion(pos, VecScale(dir, 16), 0.5, Power/2, 10, false, false)
-					end
-					for z=1, math.random(-11, 1) do
-						for i=1, Power*3 do
-							local RndV = rndVec(math.random(Power*1000/25, Power*1000/20)/1000)
-							local Pos = VecAdd(p, RndV)
-							local Rot = QuatLookAt(p, Pos)
-							local T = Transform(Pos, Rot)
-							local toCam = QuatLookAt(p, GetCameraTransform().pos)
-							local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
-							local sizeRnd = math.random(-i*1000/60, i*1000/60)/1000
-							DrawSprite(Glow, T, i/50+sizeRnd, i/50+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/5000, true, false) --beamstart
-							DrawSprite(Glow, T, i/25+sizeRnd, i/25+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.1, i/30000, true, false)
-						end
-						PlaySound(FinalFlashChargeLightning, GetPlayerTransform().pos, 1, 1, math.random(800, 1200)/1000)
-						ShakeCamera(0.6)
-						for c=1, 3 do
-							local Lpos2 = VecAdd(GetPlayerTransform(true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 7500)/1000, Vec(1,1,0.4))
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 7500)/1000, Vec(1,1,0.4))
-							for x=1, 25 do
-								local dir =  rndVec(5 + Power/50)
-								local pos = VecAdd(p, dir)
-								SpawnDistortion(pos, VecScale(dir, 8), 1, Power*2, 15, false, false)
-							end
-						end
-						for x=1, 75 do
-							--PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
-						end
-						for i=1, Power/13 do
-							ParticleReset()
-							ParticleTile(4)
-							ParticleCollide(0)
-							ParticleRadius(0.25 + Power/500, 0)
-							ParticleGravity(0)
-							ParticleStretch(8)
-							ParticleAlpha(1)
-								ParticleEmissive(5, 0)
-								ParticleColor(1,1,0.25)
-							local rndpos2 = rndVec(5.5)
-							local spawnpos = VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndpos2)
-							local rndpos = VecAdd(spawnpos, VecScale(rndpos2, 2))
-							local directiontoSpos = VecNormalize(VecSub(rndpos, spawnpos))
-							SpawnParticle(spawnpos, VecScale(directiontoSpos, 100), Power/100/11)
-						end
-					end
-					for z=1, math.random(-9, 1) do
-						PlaySound(FinalFlashChargeLightning, GetPlayerTransform().pos, 0.5, 0.5, math.random(800, 1200)/1000)
-						for c=1, 3 do
-							local Lpos2 = VecAdd(GetPlayerTransform(true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
-							createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
-						end
-						for x=1, 25 do
-							PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
-						end
-						for i=1, Power/13 do
-							ParticleReset()
-							ParticleTile(4)
-							ParticleCollide(0)
-							ParticleRadius(0.2 + Power/750, 0)
-							ParticleGravity(0)
-							ParticleStretch(4.5)
-							ParticleAlpha(1)
-								ParticleEmissive(5, 0)
-								ParticleColor(1,1,0.2)
-							SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(Power*1100, Power*1100)/1000), Power/100/12)
-						end
-					end
-				end
-			
-			local center = PlayerT.pos  
-			local radius = math.random(Power*1000/40, Power*1000/20)/1000  
-			local numParticles = Power
-			
-			local angleIncrement = 2 * math.pi / numParticles 
-
-			for i = 1, numParticles do
-
-				local angle = i * angleIncrement
-
-				local x = center[1] + radius * math.cos(angle)
-				local z = center[3] + radius * math.sin(angle)
-
-				local y = center[2]
-
-				local particlePosition = Vec(x, y, z)
-				local Pdir = Vec(0, -1, 0)
-				local hitP, dP = QueryRaycast(particlePosition, Pdir, 6)
-				if hitP then
-					local hitPosition = VecAdd(particlePosition, VecScale(Pdir, dP))
-					ParticleReset()
-					ParticleTile(0)
-					ParticleRadius(0.25 + Power/150)
-					ParticleGravity(-5)
-					ParticleAlpha(0.3, 0)
-					ParticleColor(0.7,0.7,0.7)
-					SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform().pos)), math.random(0, Power*800)/1000), 0.5)
-					for i=1, math.random(-5, 1) do
-						ParticleReset()
-						ParticleTile(6)
-						ParticleRadius(math.random(50 + Power*1000/1750, 150 + Power*1000/1650)/1000, 0)
-						ParticleGravity(-45)
-						ParticleAlpha(1)
-						ParticleSticky(0.2)
-						local DebrisC = math.random(225, 650)/1000
-						ParticleColor(DebrisC,DebrisC,DebrisC)
-						SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform().pos)), math.random(0, Power*1200)/1000), 4.5)
-					end
-				end
-			end
-		end
-	elseif GetString("game.player.tool") == "fFlash" and canShoot() and fFlashactive then
-		local ParticlePos = TransformToParentPoint(GetPlayerTransform(true), Vec(0,0,0))
-		QueryRejectBody(GetToolBody())
-		local hit, d = QueryRaycast(ParticlePos, Vec(0, -1, 0), 5)
-		local PlayerT = GetPlayerTransform(true)
-		if hit or not hit then
-			SetPlayerVelocity(Vec(0,0,0))
-			--PlayerT.pos = VecAdd(PTF.pos, Vec(0,5,0))
-			--SetPlayerTransform(PlayerT, true)
-			
-			--local Lpos2 = VecAdd(GetPlayerTransform(true).pos, Vec(math.random(-8000, 8000)/1000,math.random(-0, 8000)/1000,math.random(-8000, 8000)/1000)) --maybe math.sin Gettime()?
-			--createLightningPath(TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5)), TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5)), 10, math.random(0, 3500)/1000)
-			
-			local center = PlayerT.pos
-			local radius = math.random(Power*1000/40, Power*1000/8)/1000
-			local numParticles = Power*2
-			
-			local angleIncrement = 2 * math.pi / numParticles 
-
-			for i = 1, numParticles do
-				local angle = i * angleIncrement
-
-				local x = center[1] + radius * math.cos(angle)
-				local z = center[3] + radius * math.sin(angle)
-
-				local y = center[2]
-
-				local particlePosition = Vec(x, y, z)
-				local Pdir = Vec(0, -1, 0)
-				local hitP, dP = QueryRaycast(particlePosition, Pdir, 6)
-				if hitP then
-					local newDir = VecScale(TransformToParentVec(PlayerT, Vec(0,0,-1)), Power/1.6)
-					local hitPosition = VecAdd(particlePosition, VecScale(Pdir, dP))
-					ParticleReset()
-					ParticleTile(0)
-					ParticleRadius(0.25 + Power/150)
-					ParticleGravity(-5)
-					ParticleAlpha(0.3, 0)
-					ParticleColor(0.7,0.7,0.7)
-					SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecAdd(VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform().pos)), math.random(0, Power*800)/1000), newDir), 0.5)
-					for i=1, math.random(-5, 1) do
-						ParticleReset()
-						ParticleTile(6)
-						ParticleRadius(math.random(50 + Power*1000/1750, 150 + Power*1000/1650)/1000, 0)
-						ParticleGravity(-45)
-						ParticleAlpha(1)
-						ParticleSticky(0.2)
-						local DebrisC = math.random(225, 650)/1000
-						ParticleColor(DebrisC,DebrisC,DebrisC)
-						SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecAdd(VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform().pos)), math.random(0, Power*800)/1000), newDir), 4.5)
-					end
-				end
-			end
-		end
-	end
-	
-			for i = 1, #Lightnings - 1 do
-				local distance = calculateDistance(Lightnings[i].position, Lightnings[i + 1].position)
-				local direction = VecNormalize(VecSub(Lightnings[i].position, Lightnings[i + 1].position))
-				--DebugPrint(distance)
-				Lightnings[i].t = Lightnings[i].t + dt
-				local Lightning = Lightnings[i]
-				--Lightnings[i].position = VecAdd(Lightnings[i].position, VecScale(GetPlayerVelocity(), 0.02))
-				local LightningLine = LoadSprite("img/WhiteLineGlow.png")
-				--local LightningLine = LoadSprite("img/Glow.png")
-				local origin = Lightnings[i].position
-				local Lchance = math.random(1, 20)
-				if Lchance == 1 then
-					--SetEnvironmentProperty("ambient", 1/Lightnings[i].t + dt)
-					PointLight(origin, Lightning.color[1], Lightning.color[2], Lightning.color[3]+math.sin(GetTime()*18.0)*0.6, math.random(6000, 12000)/1000)
-				end
-					PointLight(origin, 1, 1,  0.4+math.sin(GetTime()*18.0)*0.45, math.random(600, 1200)/1000)
-				local dir = direction
-				local length = -distance
-				local hitPoint = VecAdd(origin, VecScale(dir, length))
-				local t = Transform(VecLerp(origin, hitPoint, 0.5))
-				local xAxis = VecNormalize(VecSub(hitPoint, origin))
-				local zAxis = VecNormalize(VecSub(origin, GetCameraTransform().pos))
-				t.rot = QuatAlignXZ(xAxis, zAxis)
-				local direction2 = VecNormalize(VecSub(GetCameraTransform().pos, origin))
-				local origin2 = VecAdd(origin, VecScale(direction2, 0.001))
-				local t2 = Transform(VecLerp(origin2, hitPoint, 0.5))
-				local xAxis2 = VecNormalize(VecSub(hitPoint, origin2))
-				local zAxis2 = VecNormalize(VecSub(origin2, GetCameraTransform().pos))
-				t2.rot = QuatAlignXZ(xAxis2, zAxis2)
-				
-				if not fFlashactive then
-					if distance < 8 then
-						for z=1, 10 do
-							local Cchance = math.random(1, 20)
-								local iVal = math.random(z*250, z*1750)/1000
-								local rndP = math.random(Power*1000/60, Power*1000/40)/1000
-									DrawSprite(LightningLine, t, length*1.24, iVal/12*rndP, Lightning.color[1], Lightning.color[2], Lightning.color[3]+math.sin(GetTime()*18.0)*0.6, z/100, true, false)
-									DrawSprite(Glow, t, length*2.54, iVal/6*rndP, Lightning.color[1], Lightning.color[2], Lightning.color[3], z/8800, true, false)
-									DrawSprite(Glow, t, length*3.04, iVal/1.25*rndP, Lightning.color[1], Lightning.color[2], Lightning.color[3], z/10800, true, false)
-							--DrawSprite(LightningLine, t, length*1.175, iVal/50, 1, 1, 0, z/75, true, false)
-							--DrawSprite(Glow, t, length*1.75, iVal/40, 1, 1, 0, z/800, true, false)
-							--DrawSprite(Glow, t, length*1.75, iVal/30, 1, 1, 0, z/1200, true, false)
-							--DrawSprite(Glow, t, length*1.25, iVal/20, 1, 1, 0, z/2000, true, false)
-						end
-					end
-				elseif fFlashactive then
-					if distance < 28 then
-						for z=1, 10 do
-							local Cchance = math.random(1, 20)
-								local iVal = math.random(z*250, z*1750)/1000
-								DrawSprite(LightningLine, t, length*1.24, iVal/12, Lightning.color[1], Lightning.color[2], Lightning.color[3]+math.sin(GetTime()*18.0)*0.6, z/100, true, false)
-								DrawSprite(Glow, t, length*2.54, iVal/6, Lightning.color[3], Lightning.color[2], Lightning.color[1], z/8800, true, false)
-								DrawSprite(Glow, t, length*3.04, iVal/1.25, Lightning.color[3], Lightning.color[2], Lightning.color[1], z/10800, true, false)
-							--DrawSprite(LightningLine, t, length*1.175, iVal/50, 1, 1, 0, z/75, true, false)
-							--DrawSprite(Glow, t, length*1.75, iVal/40, 1, 1, 0, z/800, true, false)
-							--DrawSprite(Glow, t, length*1.75, iVal/30, 1, 1, 0, z/1200, true, false)
-							--DrawSprite(Glow, t, length*1.25, iVal/20, 1, 1, 0, z/2000, true, false)
-						end
-					end
-				end
-				if Lightnings[i].t >= 0.1 then
-					--table.remove(Lightnings, i)
-				end
-			end
-	
-	    for i, Lightning in ipairs(Lightnings) do
-        if Lightning.active then
-			Lightning.light = Lightning.light - dt*4
-			if Lightning.light <= 0 then Lightning.light = 0 end
-			Lightning.sprite = Lightning.sprite - dt*8
-			if Lightning.sprite <= 0 then Lightning.sprite = 0 end
-			if Lightning.soundState == true then
-				--if projectile.soundT > math.random(0, 1350)/1000 then
-					--PlayLoop(windWhoosh, projectile.position, projectile.soundT*2)
-					Lightning.soundState = false
-					--local body = Spawn("MOD/" .. bodyPoints[#bodyPoints] .. ".xml", Transform(VecAdd(projectile.position, Vec(0,-0,0)), GetCameraTransform().rot))[1]
-					--projectile.position = GetBodyTransform(body).pos
-				--end
-			end
-			--projectile.position = GetBodyTransform(projectile.distB).pos
-			local body = Lightning.distB
-			local bodyPos = GetBodyTransform(Lightning.distB).pos
-			--local smth = Spawn("MOD/" .. bodyPoints[#bodyPoints] .. ".xml", Transform(projectile.position, projectile.direction))[1]
-			--projectile.position = projectile.position
-			local Cchance = math.random(1, 2)
-			if Cchance == 1 then
-				PointLight(Lightning.position, Color, Color2, Color3, math.random(15, 25))
-			elseif Cchance == 2 then
-				PointLight(Lightning.position,Color4, Color5, Color6, math.random(15, 25))
-			end
-			
-            if Lightning.t >= math.random(60, 60)/1000 then
-				--Delete(Lightning.distB)
-                Lightning.active = false
-				table.remove(Lightnings, i)
-				--table.remove(Lightning, i)
+function server.init()
+    RegisterTool("fFlash", "Final Flash", "MOD/vox/InvisHand.vox")
+    SetBool("game.tool.fFlash.enabled", true, true)
+    SetFloat("game.tool.fFlash.ammo", 101, true)
+    ExplFlash = 0
+    ExplFlash1 = 0
+    ToolReady = 0
+    coolDown = 0
+    Flashtimer = 0
+    expltimer = 0
+    ProjParti = 0
+    ProjPart = false
+    explactive = false
+    toolactive = false
+    kamefiresound = false
+    pvell = false
+    lesslaggymode = false
+    explosiontesthappened = false
+    explosiontesthappened1 = false
+    explosiontesthappened2 = false
+    timer = 0
+    Power = 1
+    Power1 = 0
+    mhT = 0
+    inuse = 0
+    uirng = 0
+    uirng1 = 0
+    beamparticl = 0
+    strength = 10
+    maxDist = 50
+    maxMass = 200000
+    distancetest = 0
+    pushtimer = 0
+    explosiontest = -2000000
+    hitcount = 0
+    SCc = 0
+    kameChargee = 0
+    uiheight = -1
+    uitexttimer = 0
+    playsndrng = 0
+    playsndrng1 = 0
+    fFlashactive = false
+    HandAnim = false
+    rHandT = 0
+    LightFlash = 0
+    EnergyBallFlicker = 0
+    LightningFlicker = 0
+    DImpact = true
+    EnvBack = false
+    FFlashFLoopStart = false
+    FFlashLT = 0
+    FFlashwasactive = false
+    FFlashwasactiveT = 0
+    mousex = 0
+    mousey = 0
+    mousex2 = 0
+    mousey2 = 0
+    HandSmokeT = 0
+    HandSmoke = false
+    SRndSize = 0
+    KameLaunch = LoadLoop("snd/KameLaunchLatest.ogg")
+    ChargePower = LoadLoop("snd/ChargeSFX.ogg")
+    FFlashStartUp = LoadLoop("snd/FFlashStartUp.ogg", 500)
+    FinalFlashFire = LoadLoop("snd/FinalFlashFire.ogg")
+    Earthquake = LoadLoop("snd/Earthquake.ogg", 500)
+    	FadeLightTest = LoadSprite("img/FadeLightTest.png")
+    	FadeLightTest2 = LoadSprite("img/FadeLightTest2.png")
+    	FadeLightTest3 = LoadSprite("img/FadeLightTest3.png")
+    	SquareGlow = LoadSprite("img/SquareGlow.png")
+    	Square = LoadSprite("img/Square.png")
+    lightningsprite = LoadSprite("img/Lightning_Bolt.png")
+    Glow = LoadSprite("img/Glow.png") 
+    GlowTexture2 = LoadSprite("img/GlowTexture2.png")
+    GlowTexture = LoadSprite("img/GlowTexture.png") 
+    OuterGlow = LoadSprite("img/OuterGlow.png") 
+    WhiteLine = LoadSprite("img/WhiteLine.png")
+    ConvergingRing = LoadSprite("img/ConvergingRing.png")
+    ConvergingRing2 = LoadSprite("img/ConvergingRing2.png")
+    ConvergingRingGlow = LoadSprite("img/ConvergingRingGlow.png")
+    ConvergingRingGlow2 = LoadSprite("img/ConvergingRingGlow2.png")
+    ConvergingRingTextureTest = LoadSprite("img/ConvergingRingTextureTest.png")
+    CrownFlare2 = LoadSprite("img/CrownFlare2.png")
+    Glow2 = LoadSprite("img/Glow2.png")
+    HoriFlare = LoadSprite("img/HoriFlareThin.png")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for i = #projHits, 1, -1 do
+        	local projHit = projHits[i]
+        	if projHit.FireBall <= 2 then
+        		local intensity = math.max(0, 1 - (projHit.FireBall / 1.75))
+        		PointLight(projHit.startPos, 1, 0.2, 0, intensity*Power)
+        	end
+        end
+        SRndSize = math.random(0, 3)
+        if GetString("game.player.tool") ~= "fFlash" then
+        	HandsoutL = 0
+        	HandsoutR = 0
+        	HandsRaised = 0 
+        	HandsForwards = 0
+        	FFlashEnded = true
+        	FFlashEndedT = 0
+
+        	kameChargee = 0
+        	Power = 0
+        	FFlashwasactive = false
+        	FFlashwasactiveT = 1
+        	fFlashactive = false
+        	LightningFlicker = 0
+        	EnergyBallFlicker = 0
+
+        	FFlashFLoopStart = false
+        	SetSoundLoopProgress(FinalFlashFire, 0)
+        	rHandT = 0
+        	hitcount = 0
+        	inuse = 0
+        	toolactive = false
+        	fFlashactive = false
+        	LightFlash = Power
+        	HandAnim = false
+        	FFlashEnded = false
+        	HandSmoke = false
+        	HandSmokeT = 0
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        updateFlames(dt)
+    end
+end
+
+function client.init()
+    KameFire = LoadSound("snd/KameFire.ogg")
+    KameFire1 = LoadSound("snd/KameFire1.ogg")
+    KameExplo = LoadSound("snd/KameExplo.ogg")
+    KameCharge = LoadSound("snd/KameCharge.ogg")
+    KameCharge1 = LoadSound("snd/KameCharge1.ogg")
+    fFlashExplosion = LoadSound("snd/FFlashExplosion.ogg", 500)
+    fFlashExplosion2 = LoadSound("snd/FFlashExplosion2.ogg", 500)
+    fFlashLightExpl = LoadSound("snd/FFlashLightExpl.ogg")
+    RockDestruction = LoadSound("snd/RockDestruction.ogg")
+    RockDestruction2 = LoadSound("snd/RockDestruction2.ogg")
+    RockDestruction3 = LoadSound("snd/RockDestruction3.ogg")
+    FinalThunder = LoadSound("snd/FinalThunder.ogg")
+    FinalThunder2 = LoadSound("snd/FinalThunder2.ogg")
+    FinalFlashChargeLightning = LoadSound("snd/FinalFlashChargeLightning.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    	if GetString("game.player.tool") == "fFlash" then --camerachange
+    		if not fFlashactive and InputDown("lmb") and not FFlashwasactive then
+    			mousex = mousex + InputValue("camerax")*12
+    			if mousex >= 10 then mousex = 10 end
+    			if mousex <= -10 then mousex = -10 end
+    			mousey = mousey + InputValue("cameray")*12
+    			if mousey >= 8 then mousey = 8 end
+    			if mousey <= 2 then mousey = 2 end
+    			Transition = 0 --Transition = Transition - dt
+    			if not GetBool("game.paused") then
+    				CamShake = math.random(Power*1000/100, Power*1000/75)/1000
+    				CamShake2 = math.random(Power*1000/100, Power*1000/75)/1000
+    				CamShake3 = math.random(Power*1000/100, Power*1000/75)/1000
+    			elseif GetBool("game.paused") then
+    				CamShake = 0
+    				CamShake2 = 0
+    				CamShake3 = 0
+    			end
+    			xVal = CamShake + -mousex
+    			yVal = mousey/2 + Power/60 - 0.5 + CamShake2
+    			zVal = mousey*1 + CamShake3 + Power/12 - 0.83
+    			local tPosY = Transform(Vec(CamShake + -mousex - 0.2, mousey/2 + Power/60 - 1.25 + CamShake2, mousey*1 - 2 + CamShake3 + Power/12 - 0.83), QuatAxisAngle(Vec(0, 0, 0)))
+    			SetCameraOffsetTransform(tPosY, true)
+    		elseif fFlashactive or FFlashwasactive then
+    			mousex2 = mousex2 + InputValue("camerax")*12
+    			if mousex2 >= 10 then mousex2 = 10 end
+    			if mousex2 <= -10 then mousex2 = -10 end
+    			mousey2 = mousey2 + InputValue("cameray")*12
+    			if mousey2 >= 8 then mousey2 = 8 end
+    			if mousey2 <= 2 then mousey2 = 2 end
+    			Transition = Transition + dt*2
+    			if Transition >= 1 then Transition = 1 end
+    				if not GetBool("game.paused") then
+    					CamShake1 = math.random(Power*1000/100, Power*1000/75)/1000
+    					CamShake12 = math.random(Power*1000/100, Power*1000/75)/1000
+    					CamShake13 = math.random(Power*1000/100, Power*1000/75)/1000
+    				elseif GetBool("game.paused") then
+    					CamShake1 = 0
+    					CamShake12 = 0
+    					CamShake13 = 0
+    				end
+    			xVal2 = lerp(xVal, xVal*1.25 + -mousex2, Transition) + CamShake1
+    			yVal2 = lerp(yVal, yVal*1.25 + mousey/2, Transition) + CamShake12
+    			zVal2 = lerp(zVal, zVal*1.25 + mousey*1, Transition) + CamShake13
+    			local tPosY = Transform(Vec(lerp(xVal, xVal*1.25 + -mousex2, Transition) + CamShake1, lerp(yVal, yVal*1.25 + mousey/2, Transition) + CamShake12, lerp(zVal, zVal*1.25 + mousey*1, Transition) + CamShake13), QuatAxisAngle(Vec(0, 0, 0)))
+    			SetCameraOffsetTransform(tPosY, true)
+    		end
+    		if FFlashwasactive and not fFlashactive then 
+
+    			local Default = Transform(Vec(lerp(xVal2, 0, FFlashwasactiveT), lerp(yVal2, 0, FFlashwasactiveT), lerp(zVal2, 0, FFlashwasactiveT)), QuatAxisAngle(Vec(0, 0, 0)))
+    			SetCameraOffsetTransform(Default, true)
+    		end
+    		--SetCameraOffsetTransform(tPosX, true)
+    	end
+
+    	--[[if InputPressed("b") then
+    		SetEnvironmentProperty("exposure", 0.2/10, 20)
+    		SetEnvironmentProperty("skyboxtint", 0.1, 0.1, 0.1)
+    		SetEnvironmentProperty("constant", 0.001, 0.001, 0.001)
+    		SetPostProcessingProperty("bloom", 4)
+    		SetPostProcessingProperty("saturation", 1)
+    		SetPostProcessingProperty("colorbalance", 1, 1, 1)
+    		SetEnvironmentProperty("fogParams", 200, 450, 0.15, 100)--SetEnvironmentProperty("fogParams", 50, 210, 0.9, 8)
+    		SetEnvironmentProperty("sunSpread", 0.001)
+    		SetEnvironmentProperty("fogColor", 0.1, 0.45, 1)
+    	end]]
+
+    	if HandSmoke then
+    		HandSmokeT = HandSmokeT + dt
+    	end
+
+    	if HandSmokeT > 0.6 and HandSmokeT <= 5 then
+    		local animator = GetPlayerAnimator()
+    		ParticleReset()
+    		ParticleTile(0)
+    		ParticleColor(0.7,0.7,0.7)
+    		ParticleEmissive(0)
+    		ParticleRadius(0, 0.1)
+    		ParticleGravity(0.9)
+    		ParticleAlpha(0.6, 0)
+    		ParticleCollide(0)
+    		SpawnParticle(GetBoneWorldTransform(animator, "hand_l").pos, rndVec(math.random(0, 25)/100), 1)
+    		ParticleReset()
+    		ParticleTile(0)
+    		ParticleColor(0.7,0.7,0.7)
+    		ParticleEmissive(0)
+    		ParticleRadius(0, 0.1)
+    		ParticleGravity(0.9)
+    		ParticleAlpha(0.6, 0)
+    		ParticleCollide(0)
+    		SpawnParticle(GetBoneWorldTransform(animator, "hand_r").pos, rndVec(math.random(0, 25)/100), 1)
+    	end
+
+    	if HandSmokeT >= 5 then
+    		HandSmokeT = 0
+    		HandSmoke = false
+    	end
+
+    	for i = #Auras, 1, - 1 do
+    		Aura = Auras[i]
+
+    		local direction = calculateBezierTangent(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
+    		local normalizedDirection = VecScale(VecNormalize(direction), 25)
+
+    		local newPos = calculateBezierPoint(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
+
+    			for i=1, 20 do
+    				local RndV = rndVec(0)
+    				local Pos = VecAdd(newPos, RndV)
+    				local Rot = QuatLookAt(newPos, GetCameraTransform().pos)--QuatLookAt(newPos, Pos)
+    				local T = Transform(Pos, QuatRotateQuat(Rot, QuatEuler(math.random(0, 0), Aura.SpriteRnd, math.random(0, 0))))
+    				local toCam = QuatLookAt(newPos, GetCameraTransform().pos)
+    				local T2 = Transform(newPos, QuatRotateQuat(toCam, QuatEuler(0,0,0)))
+    				local AuraSize = 0.01/Aura.t
+    				if AuraSize >= 1 then AuraSize = 1 end
+    				local sizeRnd = math.random(-i*1000/60, i*1000/60)/1000
+    				--DrawSprite(Glow, T, i/4+ math.sin(GetTime()*math.random(500, 2500)/1000)*3, i/48, 1.0, 1, 0.4, 1, true, false) --50000
+    				--DrawSprite(HoriFlare, T, i/50+sizeRnd, i/50+sizeRnd, 1.0, 1, 0.4, i/5000, true, false)
+    				--DrawSprite(Glow, T2, i/4+sizeRnd, i/4+sizeRnd, 1.0, 1, 0.5, i/2500000, true, false)
+    				--DrawSprite(Glow, T2, i/7+sizeRnd, i/7+sizeRnd, 1.0, 1, 0.5, i/1500000, true, false)
+    				--DrawSprite(Glow, T2, i/13+sizeRnd, i/13+sizeRnd, 1.0, 1, 0.5, i/500000, true, false)
+    			end
+    		--PointLight(newPos, 1,1,0, 3)
+
+    	end
+
+    	editBodies(dt)
+
+    	for i = #FireGusts, 1, -1 do
+    		local FireGust = FireGusts[i]
+    		FireGust.ColorT = FireGust.ColorT - dt*1.5
+    		if FireGust.ColorT <= 0 then FireGust.ColorT = 0 end
+    		if FireGust.ColorT >= 1 then FireGust.ColorT = 1 end
+    		FireGust.FireGT = FireGust.FireGT - dt*2
+    		if FireGust.FireGT <= 0 then FireGust.FireGT = 0 end
+    		if FireGust.FireGT >= 1 then FireGust.FireGT = 1 end
+    		FireGust.FireGTB = FireGust.FireGTB - dt*4
+    		if FireGust.FireGTB <= 0 then FireGust.FireGTB = 0 end
+    		if FireGust.FireGTB >= 1 then FireGust.FireGTB = 1 end
+    		local FireGTB = FireGust.FireGTB
+    		if FireGTB <= 0 then FireGTB = 0 end
+    		if FireGTB >= 1 then FireGTB = 1 end
+    		FireGust.FireGBackF = FireGust.FireGBackF - dt*4
+    		if FireGust.FireGBackF <= 0 then FireGust.FireGBackF = 0 end
+    		if FireGust.FireGBackF >= 1 then FireGust.FireGBackF = 1 end
+    		FireGust.Light = FireGust.Light - dt*2
+    		if FireGust.Light <= 0 then FireGust.Light = 0 end
+    		if FireGust.Light >= 1 then FireGust.Light = 1 end
+    		PointLight(FireGust.startPos, FireGust.ColorT , math.random(FireGust.ColorT*1000/4, FireGust.ColorT*1000/3)/1000, 0, FireGust.Light*15)
+    		for z=1, 20 do
+    			ParticleReset()
+    			ParticleRadius(math.random(FireGust.FireGT*2050, FireGust.FireGT*4050)/1000*0.45, 0, "easeout")
+    			ParticleSticky(0)
+    			ParticleEmissive(FireGust.FireGBackF*10, 0)
+    			ParticleTile(0)
+    			ParticleAlpha(FireGust.FireGT, 0, "easein")
+    			ParticleDrag(0.25)
+    			if FireGust.FireGBackF <= 0.05 then
+    				Prngsmoke = 0
+    			elseif FireGust.FireGBackF > 0.05 then
+    				Prngsmoke = 0
+    			end
+    			ParticleColor(FireGust.ColorT + Prngsmoke, math.random(FireGust.ColorT*1000/3, FireGust.ColorT*1000/2)/1000 + Prngsmoke, 0 + Prngsmoke, 0,0,0)
+    			ParticleCollide(0)
+    			ParticleGravity(0)
+    			ParticleStretch(6, 0)
+    			local GustLifetime = 0.1/FireGust.ColorT
+    			if GustLifetime > 0.5 then GustLifetime = 0.5 end
+    			SpawnParticle(VecAdd(FireGust.startPos, rndVec(FireGTB/20)), VecAdd(VecScale(FireGust.velocity, math.random(0, 200)/1000), rndVec(GustLifetime*15)), 0.5 + GustLifetime)
+    		end
+    			FireGust.timer = FireGust.timer + dt
+    			if FireGust.timer >= 1 then
+    				table.remove(FireGusts, i)
+    			end
+    	end
+
+    	if GetString("game.player.tool") == "fFlash" and canShoot() and InputPressed("lmb") and not fFlashactive then
+    		PTF = GetPlayerTransform(playerId, true)
+    		DImpact = true
+    	end	
+    	if GetString("game.player.tool") == "fFlash" and canShoot() and InputDown("lmb") and not fFlashactive then
+    		local ParticlePos = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,0,0))
+    		QueryRejectBody(GetToolBody())
+    		local hit, d = QueryRaycast(ParticlePos, Vec(0, -1, 0), 5)
+    		local PlayerT = GetPlayerTransform(playerId, true)
+    		if hit or not hit then --change to if hit then somebool active or don't use a raycast at all
+    			SetPlayerVelocity(playerId, Vec(0,0,0))
+    			PlayerT.pos = VecAdd(PTF.pos, Vec(0,lerp(0, Power/25, Power/100),0))
+    			SetPlayerTransform(playerId, PlayerT, true)
+
+    				LightningFlicker = LightningFlicker + dt/4
+    				if LightningFlicker >= 1 then LightningFlicker = 1 end
+    				EnergyBallFlicker = EnergyBallFlicker + dt*LightningFlicker
+    				if EnergyBallFlicker >= 0.1 then EnergyBallFlicker = 0 end
+    				local Flicker = math.abs(EnergyBallFlicker - 0.05)
+    				local p = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0, 1, -1.5 + -Power/35))
+
+    				PlayLoop(Earthquake, p, 10, 10, math.random(1000, 1250)/1000)
+    				PlayLoop(FFlashStartUp, p, 20)
+    				local raritynum = 3
+    				local rarity = math.random(1, raritynum)
+    				if LightningFlicker < 0.75 and EnergyBallFlicker >= 0 then
+    					local p = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0, 1, -1.5 + -Power/35))
+    					PointLight(VecAdd(p, rndVec(Power/30)), 1.0, 1, 0.2+math.sin(GetTime()*18.0)*0.3, math.random(Power*1000/8, Power*1000/5)/1000)
+    					local Lpos2 = VecAdd(GetPlayerTransform(playerId, true).pos, Vec(math.random(-8000, 8000)/1000,math.random(-0, 8000)/1000,math.random(-8000, 8000)/1000)) --maybe math.sin Gettime()?
+    					--createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 10, math.random(0, 3500)/1000)
+    					for x=1, 8 do
+    						local dir =  rndVec(1 + Power/75)
+    						local pos = VecAdd(p, dir)
+    						SpawnDistortion(pos, VecScale(dir, 16), 0.5, Power/2, 10, false, false)
+    					end
+    					for i=1, Power*2 do
+    						local RndV = rndVec(Power/200)
+    						local Pos = VecAdd(p, RndV)
+    						local Rot = QuatLookAt(p, Pos)
+    						local T = Transform(Pos, Rot)
+    						local toCam = QuatLookAt(p, GetCameraTransform().pos)
+    						local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
+    						local sizeRnd = math.random(i*1000/120, i*1000/120)/1000 - math.random(Power*1000/100*0.25, Power*1000/100*1)/1000
+    						DrawSprite(Glow, T, i/200+sizeRnd, i/200+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/100, true, false) --beamstart
+    						DrawSprite(Glow, T, i/100+sizeRnd, i/100+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/100000, true, false)
+    						--DrawSprite(Glow, T, i/15+sizeRnd, i/15+sizeRnd, 1.0, 1, 0.2+math.sin(GetTime()*18.0)*0.1, i/200000, true, false)
+    					end
+    					for i=10, Power/4 do
+    						ParticleReset()
+    						ParticleTile(5)
+    						ParticleCollide(0)
+    						ParticleEmissive(5, 0)
+    						ParticleRadius(0.25 + Power/300, 0, "easeout")
+    						ParticleGravity(-5)
+    						ParticleAlpha(1, 0)
+    						ParticleColor(1,1,0.25)
+    						ParticleStretch(10)
+    						local rndV = rndVec(15)
+    						local rndpos = VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndV)
+    						local pPos = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35))
+    						local changerndpos = VecAdd(VecAdd(rndpos, VecScale(VecNormalize(VecSub(pPos, rndpos)), Power/math.random(6,8))), math.cos(math.sin(GetTime()*10.0)*90))
+    						local dir = VecNormalize(VecSub(pPos, changerndpos))
+    						local dist = VecLength(VecSub(pPos, changerndpos))
+    						--SpawnParticle(changerndpos, VecScale(dir, dist*14), Power/100/12)
+    						for z=1, math.random(-7, 1) do
+    							--SpawnParticle(changerndpos, VecScale(dir, dist*28), Power/100/12)
+    						end
+    					end
+    					for z=1, math.random(-15, 1) do
+    						PlaySound(FinalFlashChargeLightning, GetPlayerTransform(playerId).pos, Power/100, Power/100, math.random(800, 1200)/1000)
+    						ShakeCamera(Power/1000*6)
+    						for c=1, 3 do
+    							local Lpos2 = VecAdd(GetPlayerTransform(playerId, true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 6500)/1000, Vec(1,1,0.4))
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 6500)/1000, Vec(1,1,0.4))
+    							for x=1, 25 do
+    								local dir =  rndVec(5 + Power/50)
+    								local pos = VecAdd(p, dir)
+    								SpawnDistortion(pos, VecScale(dir, 8), 1, Power*2, 15, false, false)
+    							end
+    						end
+    						for x=1, 50 do
+    							PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
+    						end
+    						for i=1, Power/13 do
+    							ParticleReset()
+    							ParticleTile(4)
+    							ParticleCollide(0)
+    							ParticleEmissive(5)
+    							ParticleRadius(0.25 + Power/500, 0)
+    							ParticleGravity(0)
+    							ParticleStretch(8)
+    							ParticleAlpha(1)
+    							ParticleColor(1,1,0.25)
+    							SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(Power*1600, Power*1600)/1000), Power/100/11)
+    						end
+    					end
+    					for z=1, math.random(-12, 1) do
+    						PlaySound(FinalFlashChargeLightning, GetPlayerTransform(playerId).pos, Power/200, Power/200, math.random(800, 1200)/1000)
+    						for c=1, 3 do
+    							local Lpos2 = VecAdd(GetPlayerTransform(playerId, true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
+    						end
+    						for x=1, 25 do
+    							PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
+    						end
+    						for i=1, Power/13 do
+    							ParticleReset()
+    							ParticleTile(4)
+    							ParticleCollide(0)
+    							ParticleEmissive(5)
+    							ParticleRadius(0.2 + Power/750, 0)
+    							ParticleGravity(0)
+    							ParticleStretch(4.5)
+    							ParticleAlpha(1)
+    							ParticleColor(1,1,0.2)
+    							SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(Power*1100, Power*1100)/1000), Power/100/12)
+    						end
+    					end
+    				elseif LightningFlicker >= 0.75 and EnergyBallFlicker >= 0 then
+    					local p = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35))
+    					PointLight(VecAdd(p, rndVec(Power/30)), 1.0, 1, 0.2+math.sin(GetTime()*18.0)*0.3, math.random(Power*1000/8, Power*1000/5)/1000)
+    					PlayLoop(Earthquake, p, 10, 10, math.random(1000, 1250)/1000)
+    					PlayLoop(FFlashStartUp, p, 20, 20, 1)
+    					for i=1, Power*2 do
+    						local RndV = rndVec(Power/200)
+    						local Pos = VecAdd(p, RndV)
+    						local Rot = QuatLookAt(p, Pos)
+    						local T = Transform(Pos, Rot)
+    						local toCam = QuatLookAt(p, GetCameraTransform().pos)
+    						local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
+    						local sizeRnd = math.random(-i*1000/120, i*1000/120)/1000
+    						DrawSprite(Glow, T, i/200+sizeRnd, i/200+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/100, true, false) --beamstart
+    						DrawSprite(Glow, T, i/50+sizeRnd, i/50+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.1, i/100000, true, false)
+    					end
+    					--OUTER SPHERE
+    					for i=10, Power/4 do
+    						ParticleReset()
+    						ParticleTile(5)
+    						ParticleCollide(0)
+    						ParticleRadius(0.25 + Power/300, 0, "easeout")
+    						ParticleGravity(-5)
+    						ParticleAlpha(1, 0)
+    							ParticleEmissive(5, 0)
+    							ParticleColor(1,1,0.25)
+    						ParticleStretch(10)
+    						local rndV = rndVec(15)
+    						local rndpos = VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndV)
+    						local pPos = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35))
+    						local changerndpos = VecAdd(VecAdd(rndpos, VecScale(VecNormalize(VecSub(pPos, rndpos)), Power/math.random(6,8))), math.cos(math.sin(GetTime()*10.0)*90))
+    						local dir = VecNormalize(VecSub(pPos, changerndpos))
+    						local dist = VecLength(VecSub(pPos, changerndpos))
+    						SpawnParticle(changerndpos, VecScale(dir, dist*7), Power/100/12)
+    						for z=1, math.random(-7, 1) do
+    							SpawnParticle(changerndpos, VecScale(dir, dist*20), Power/100/12)
+    						end
+    					end
+
+    					for i=1, Power/5 do
+    						ParticleReset()
+    						ParticleTile(5)
+    						ParticleCollide(0)
+    						ParticleEmissive(5, 0)
+    						ParticleRadius(0.25 + Power/100, 0)
+    						ParticleGravity(-5)
+    						ParticleAlpha(0.3, 0)
+    						ParticleColor(1,1,0)
+    						--SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(0, Power*2400)/1000), Power/100/15)
+    					end
+    					for x=1, 8 do
+    						local dir =  rndVec(1 + Power/75)
+    						local pos = VecAdd(p, dir)
+    						SpawnDistortion(pos, VecScale(dir, 16), 0.5, Power/2, 10, false, false)
+    					end
+    					for z=1, math.random(-11, 1) do
+    						for i=1, Power*3 do
+    							local RndV = rndVec(math.random(Power*1000/25, Power*1000/20)/1000)
+    							local Pos = VecAdd(p, RndV)
+    							local Rot = QuatLookAt(p, Pos)
+    							local T = Transform(Pos, Rot)
+    							local toCam = QuatLookAt(p, GetCameraTransform().pos)
+    							local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
+    							local sizeRnd = math.random(-i*1000/60, i*1000/60)/1000
+    							DrawSprite(Glow, T, i/50+sizeRnd, i/50+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.3, i/5000, true, false) --beamstart
+    							DrawSprite(Glow, T, i/25+sizeRnd, i/25+sizeRnd, 1.0, 1, 0.75+math.sin(GetTime()*18.0)*0.1, i/30000, true, false)
+    						end
+    						PlaySound(FinalFlashChargeLightning, GetPlayerTransform(playerId).pos, 1, 1, math.random(800, 1200)/1000)
+    						ShakeCamera(0.6)
+    						for c=1, 3 do
+    							local Lpos2 = VecAdd(GetPlayerTransform(playerId, true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 7500)/1000, Vec(1,1,0.4))
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 15, math.random(0, 7500)/1000, Vec(1,1,0.4))
+    							for x=1, 25 do
+    								local dir =  rndVec(5 + Power/50)
+    								local pos = VecAdd(p, dir)
+    								SpawnDistortion(pos, VecScale(dir, 8), 1, Power*2, 15, false, false)
+    							end
+    						end
+    						for x=1, 75 do
+    							--PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
+    						end
+    						for i=1, Power/13 do
+    							ParticleReset()
+    							ParticleTile(4)
+    							ParticleCollide(0)
+    							ParticleRadius(0.25 + Power/500, 0)
+    							ParticleGravity(0)
+    							ParticleStretch(8)
+    							ParticleAlpha(1)
+    								ParticleEmissive(5, 0)
+    								ParticleColor(1,1,0.25)
+    							local rndpos2 = rndVec(5.5)
+    							local spawnpos = VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndpos2)
+    							local rndpos = VecAdd(spawnpos, VecScale(rndpos2, 2))
+    							local directiontoSpos = VecNormalize(VecSub(rndpos, spawnpos))
+    							SpawnParticle(spawnpos, VecScale(directiontoSpos, 100), Power/100/11)
+    						end
+    					end
+    					for z=1, math.random(-9, 1) do
+    						PlaySound(FinalFlashChargeLightning, GetPlayerTransform(playerId).pos, 0.5, 0.5, math.random(800, 1200)/1000)
+    						for c=1, 3 do
+    							local Lpos2 = VecAdd(GetPlayerTransform(playerId, true).pos, Vec(math.random(-20000, 20000)/1000,math.random(-0, 20000)/1000,math.random(-20000, 20000)/1000)) --maybe math.sin Gettime()?
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
+    							createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35)), 12, math.random(0, 5500)/1000, Vec(1,1,0.4))
+    						end
+    						for x=1, 25 do
+    							PointLight(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), 1,1,0.25, x/2)
+    						end
+    						for i=1, Power/13 do
+    							ParticleReset()
+    							ParticleTile(4)
+    							ParticleCollide(0)
+    							ParticleRadius(0.2 + Power/750, 0)
+    							ParticleGravity(0)
+    							ParticleStretch(4.5)
+    							ParticleAlpha(1)
+    								ParticleEmissive(5, 0)
+    								ParticleColor(1,1,0.2)
+    							SpawnParticle(VecAdd(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,1, -1.5 + -Power/35)), rndVec(0.5)), rndVec(math.random(Power*1100, Power*1100)/1000), Power/100/12)
+    						end
+    					end
+    				end
+
+    			local center = PlayerT.pos  
+    			local radius = math.random(Power*1000/40, Power*1000/20)/1000  
+    			local numParticles = Power
+
+    			local angleIncrement = 2 * math.pi / numParticles 
+
+    			for i = 1, numParticles do
+
+    				local angle = i * angleIncrement
+
+    				local x = center[1] + radius * math.cos(angle)
+    				local z = center[3] + radius * math.sin(angle)
+
+    				local y = center[2]
+
+    				local particlePosition = Vec(x, y, z)
+    				local Pdir = Vec(0, -1, 0)
+    				local hitP, dP = QueryRaycast(particlePosition, Pdir, 6)
+    				if hitP then
+    					local hitPosition = VecAdd(particlePosition, VecScale(Pdir, dP))
+    					ParticleReset()
+    					ParticleTile(0)
+    					ParticleRadius(0.25 + Power/150)
+    					ParticleGravity(-5)
+    					ParticleAlpha(0.3, 0)
+    					ParticleColor(0.7,0.7,0.7)
+    					SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform(playerId).pos)), math.random(0, Power*800)/1000), 0.5)
+    					for i=1, math.random(-5, 1) do
+    						ParticleReset()
+    						ParticleTile(6)
+    						ParticleRadius(math.random(50 + Power*1000/1750, 150 + Power*1000/1650)/1000, 0)
+    						ParticleGravity(-45)
+    						ParticleAlpha(1)
+    						ParticleSticky(0.2)
+    						local DebrisC = math.random(225, 650)/1000
+    						ParticleColor(DebrisC,DebrisC,DebrisC)
+    						SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform(playerId).pos)), math.random(0, Power*1200)/1000), 4.5)
+    					end
+    				end
+    			end
+    		end
+    	elseif GetString("game.player.tool") == "fFlash" and canShoot() and fFlashactive then
+    		local ParticlePos = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(0,0,0))
+    		QueryRejectBody(GetToolBody())
+    		local hit, d = QueryRaycast(ParticlePos, Vec(0, -1, 0), 5)
+    		local PlayerT = GetPlayerTransform(playerId, true)
+    		if hit or not hit then
+    			SetPlayerVelocity(playerId, Vec(0,0,0))
+    			--PlayerT.pos = VecAdd(PTF.pos, Vec(0,5,0))
+    			--SetPlayerTransform(playerId, PlayerT, true)
+
+    			--local Lpos2 = VecAdd(GetPlayerTransform(playerId, true).pos, Vec(math.random(-8000, 8000)/1000,math.random(-0, 8000)/1000,math.random(-8000, 8000)/1000)) --maybe math.sin Gettime()?
+    			--createLightningPath(TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5)), TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5)), 10, math.random(0, 3500)/1000)
+
+    			local center = PlayerT.pos
+    			local radius = math.random(Power*1000/40, Power*1000/8)/1000
+    			local numParticles = Power*2
+
+    			local angleIncrement = 2 * math.pi / numParticles 
+
+    			for i = 1, numParticles do
+    				local angle = i * angleIncrement
+
+    				local x = center[1] + radius * math.cos(angle)
+    				local z = center[3] + radius * math.sin(angle)
+
+    				local y = center[2]
+
+    				local particlePosition = Vec(x, y, z)
+    				local Pdir = Vec(0, -1, 0)
+    				local hitP, dP = QueryRaycast(particlePosition, Pdir, 6)
+    				if hitP then
+    					local newDir = VecScale(TransformToParentVec(PlayerT, Vec(0,0,-1)), Power/1.6)
+    					local hitPosition = VecAdd(particlePosition, VecScale(Pdir, dP))
+    					ParticleReset()
+    					ParticleTile(0)
+    					ParticleRadius(0.25 + Power/150)
+    					ParticleGravity(-5)
+    					ParticleAlpha(0.3, 0)
+    					ParticleColor(0.7,0.7,0.7)
+    					SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecAdd(VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform(playerId).pos)), math.random(0, Power*800)/1000), newDir), 0.5)
+    					for i=1, math.random(-5, 1) do
+    						ParticleReset()
+    						ParticleTile(6)
+    						ParticleRadius(math.random(50 + Power*1000/1750, 150 + Power*1000/1650)/1000, 0)
+    						ParticleGravity(-45)
+    						ParticleAlpha(1)
+    						ParticleSticky(0.2)
+    						local DebrisC = math.random(225, 650)/1000
+    						ParticleColor(DebrisC,DebrisC,DebrisC)
+    						SpawnParticle(VecAdd(hitPosition, rndVec(0.5)), VecAdd(VecScale(VecNormalize(VecSub(particlePosition, GetPlayerTransform(playerId).pos)), math.random(0, Power*800)/1000), newDir), 4.5)
+    					end
+    				end
+    			end
+    		end
+    	end
+
+    			for i = 1, #Lightnings - 1 do
+    				local distance = calculateDistance(Lightnings[i].position, Lightnings[i + 1].position)
+    				local direction = VecNormalize(VecSub(Lightnings[i].position, Lightnings[i + 1].position))
+    				--DebugPrint(distance)
+    				Lightnings[i].t = Lightnings[i].t + dt
+    				local Lightning = Lightnings[i]
+    				--Lightnings[i].position = VecAdd(Lightnings[i].position, VecScale(GetPlayerVelocity(playerId), 0.02))
+    				local LightningLine = LoadSprite("img/WhiteLineGlow.png")
+    				--local LightningLine = LoadSprite("img/Glow.png")
+    				local origin = Lightnings[i].position
+    				local Lchance = math.random(1, 20)
+    				if Lchance == 1 then
+    					--SetEnvironmentProperty("ambient", 1/Lightnings[i].t + dt)
+    					PointLight(origin, Lightning.color[1], Lightning.color[2], Lightning.color[3]+math.sin(GetTime()*18.0)*0.6, math.random(6000, 12000)/1000)
+    				end
+    					PointLight(origin, 1, 1,  0.4+math.sin(GetTime()*18.0)*0.45, math.random(600, 1200)/1000)
+    				local dir = direction
+    				local length = -distance
+    				local hitPoint = VecAdd(origin, VecScale(dir, length))
+    				local t = Transform(VecLerp(origin, hitPoint, 0.5))
+    				local xAxis = VecNormalize(VecSub(hitPoint, origin))
+    				local zAxis = VecNormalize(VecSub(origin, GetCameraTransform().pos))
+    				t.rot = QuatAlignXZ(xAxis, zAxis)
+    				local direction2 = VecNormalize(VecSub(GetCameraTransform().pos, origin))
+    				local origin2 = VecAdd(origin, VecScale(direction2, 0.001))
+    				local t2 = Transform(VecLerp(origin2, hitPoint, 0.5))
+    				local xAxis2 = VecNormalize(VecSub(hitPoint, origin2))
+    				local zAxis2 = VecNormalize(VecSub(origin2, GetCameraTransform().pos))
+    				t2.rot = QuatAlignXZ(xAxis2, zAxis2)
+
+    				if not fFlashactive then
+    					if distance < 8 then
+    						for z=1, 10 do
+    							local Cchance = math.random(1, 20)
+    								local iVal = math.random(z*250, z*1750)/1000
+    								local rndP = math.random(Power*1000/60, Power*1000/40)/1000
+    									DrawSprite(LightningLine, t, length*1.24, iVal/12*rndP, Lightning.color[1], Lightning.color[2], Lightning.color[3]+math.sin(GetTime()*18.0)*0.6, z/100, true, false)
+    									DrawSprite(Glow, t, length*2.54, iVal/6*rndP, Lightning.color[1], Lightning.color[2], Lightning.color[3], z/8800, true, false)
+    									DrawSprite(Glow, t, length*3.04, iVal/1.25*rndP, Lightning.color[1], Lightning.color[2], Lightning.color[3], z/10800, true, false)
+    							--DrawSprite(LightningLine, t, length*1.175, iVal/50, 1, 1, 0, z/75, true, false)
+    							--DrawSprite(Glow, t, length*1.75, iVal/40, 1, 1, 0, z/800, true, false)
+    							--DrawSprite(Glow, t, length*1.75, iVal/30, 1, 1, 0, z/1200, true, false)
+    							--DrawSprite(Glow, t, length*1.25, iVal/20, 1, 1, 0, z/2000, true, false)
+    						end
+    					end
+    				elseif fFlashactive then
+    					if distance < 28 then
+    						for z=1, 10 do
+    							local Cchance = math.random(1, 20)
+    								local iVal = math.random(z*250, z*1750)/1000
+    								DrawSprite(LightningLine, t, length*1.24, iVal/12, Lightning.color[1], Lightning.color[2], Lightning.color[3]+math.sin(GetTime()*18.0)*0.6, z/100, true, false)
+    								DrawSprite(Glow, t, length*2.54, iVal/6, Lightning.color[3], Lightning.color[2], Lightning.color[1], z/8800, true, false)
+    								DrawSprite(Glow, t, length*3.04, iVal/1.25, Lightning.color[3], Lightning.color[2], Lightning.color[1], z/10800, true, false)
+    							--DrawSprite(LightningLine, t, length*1.175, iVal/50, 1, 1, 0, z/75, true, false)
+    							--DrawSprite(Glow, t, length*1.75, iVal/40, 1, 1, 0, z/800, true, false)
+    							--DrawSprite(Glow, t, length*1.75, iVal/30, 1, 1, 0, z/1200, true, false)
+    							--DrawSprite(Glow, t, length*1.25, iVal/20, 1, 1, 0, z/2000, true, false)
+    						end
+    					end
+    				end
+    				if Lightnings[i].t >= 0.1 then
+    					--table.remove(Lightnings, i)
+    				end
+    			end
+
+    	    for i, Lightning in ipairs(Lightnings) do
+            if Lightning.active then
+    			Lightning.light = Lightning.light - dt*4
+    			if Lightning.light <= 0 then Lightning.light = 0 end
+    			Lightning.sprite = Lightning.sprite - dt*8
+    			if Lightning.sprite <= 0 then Lightning.sprite = 0 end
+    			if Lightning.soundState == true then
+    				--if projectile.soundT > math.random(0, 1350)/1000 then
+    					--PlayLoop(windWhoosh, projectile.position, projectile.soundT*2)
+    					Lightning.soundState = false
+    					--local body = Spawn("MOD/" .. bodyPoints[#bodyPoints] .. ".xml", Transform(VecAdd(projectile.position, Vec(0,-0,0)), GetCameraTransform().rot))[1]
+    					--projectile.position = GetBodyTransform(body).pos
+    				--end
+    			end
+    			--projectile.position = GetBodyTransform(projectile.distB).pos
+    			local body = Lightning.distB
+    			local bodyPos = GetBodyTransform(Lightning.distB).pos
+    			--local smth = Spawn("MOD/" .. bodyPoints[#bodyPoints] .. ".xml", Transform(projectile.position, projectile.direction))[1]
+    			--projectile.position = projectile.position
+    			local Cchance = math.random(1, 2)
+    			if Cchance == 1 then
+    				PointLight(Lightning.position, Color, Color2, Color3, math.random(15, 25))
+    			elseif Cchance == 2 then
+    				PointLight(Lightning.position,Color4, Color5, Color6, math.random(15, 25))
+    			end
+
+                if Lightning.t >= math.random(60, 60)/1000 then
+    				--Delete(Lightning.distB)
+                    Lightning.active = false
+    				table.remove(Lightnings, i)
+    				--table.remove(Lightning, i)
+                end
             end
         end
+
+    	if #projectiles ~= 0 then
+            local shortestLifespanProjectile = projectiles[1]
+    		if shortestLifespanProjectile.hit == false then
+    			local hit, p, n, s = QueryClosestPoint(shortestLifespanProjectile.startPos, Power/30)
+    			if not hit then
+    				PointLight(shortestLifespanProjectile.startPos, 1,1,0.5, Power*4.5)
+    			end
+    		end
+        end
+
+    		if ExplFlash ~= 0 then
+    		    local a = VecAdd (hitPos2andhalf, Vec(0, 0.1, 0))
+    			local b = math.random(10, 20)
+    			ExplFlash = ExplFlash - dt*b
+    		end
+    		if ExplFlash1 ~= 0 then
+    		    local a = VecAdd (hitPos2andhalf, Vec(0, 0, 0))
+    			local b1 = math.random(55, 65)
+
+    			ExplFlash1 = ExplFlash1 - dt*b1
+    		end
+    	--end
+
+    	--[[if GetString("game.player.tool") == "fFlash" and canShoot() and HandAnim then
+    		rHandT = rHandT + dt
+    		local rHandA = EaseInExpo(rHandT)
+    		local right, left = GetToolHandPoseWorldTransform()
+    		PointLight(TransformToParentPoint(right, Vec(0,0,-3)), 1,1,1, 2)
+    		SetToolHandPoseLocalTransform(Transform(Vec(-0.2 + rHandA, 0, -0.5)), Transform(Vec(-0.6, 0, -0.5), QuatEuler(0, 180, 0)))
+    	end]]
+
+    if GetString("game.player.tool") == "fFlash" and canShoot() then
+    	if ProjParti > 0.001 then
+    		ProjPart = false
+    	end
+
+    			beamparticl = 0
+
+    			if explactive == true then
+    			if pushtimer > 0 and pushtimer < 0.04 then
+    			--push(blastpoint1)
+    			explactive = false
+    			end
+    			end
+
+    			local b = GetToolBody()
+
+    			if b ~= 0 then
+    			local offset = Transform(Vec(0.4, -1, -0.3))
+    			SetToolTransform(offset)
+    			SetToolTransformOverride(offset)
+    			toolTrans = GetBodyTransform(b)
+    			toolPos = TransformToParentPoint(toolTrans, Vec(0.12, 0.2, -0.8))
+    			end
+    			if InputDown("lmb") then
+    			--local transform = TransformToParentTransform(GetPlayerCameraTransform(playerId), Transform(Vec(0, 5, 0), QuatAxisAngle(Vec(0, 1, 0), 45)))
+    			--SetCameraTransform(transform)
+    			end
+
+    			a1 = 1
+
+    			if InputDown("lmb") then
+    			PlayLoop(ChargePower, GetPlayerTransform(playerId).pos, Power/150)
+    			uiheight = uiheight - 2
+    			if uiheight < -200 then
+    			uiheight = -200
+    			end
+    			Power = Power + dt*75
+    			if Power >= 100 then
+    			Power = 100
+    			end
+    			end
+    			if Power < 20 then
+    				Power = 20
+    			end
+    			if not fFlashactive and not InputDown("lmb") and Power > 10 then
+    				Power = Power - dt*80
+    			end
+    			if InputDown("q") then
+    			PlayLoop(ChargePower, GetPlayerTransform(playerId).pos, Power/150)
+    			uiheight = uiheight + 2
+    			if uiheight > -1 then
+    			uiheight = -1
+    			end
+    			--Power = Power -1
+    			--if Power < 1 then
+    			--Power = 1
+    			--end
+    			end
+    			if InputDown("lmb") then
+    			Power1 = Power1 + dt*0.5
+    			if Power1 > 1 then
+    			Power1 = 1
+    			end
+    			end
+    			--if InputDown("q") then
+    			--Power1 = Power1 -0.02
+    			--if Power1 < 0 then
+    			--Power1 = 0
+    			--end
+    			--end
+
+    			if InputDown("lmb") and InputPressed ("esc") then
+    				toolactive = false
+    			end
+
+    			if InputPressed("lmb") and not fFlashactive then
+    				HandAnim = true
+    				rHandT = 0
+    				Power = 0
+    				local vel = GetPlayerVelocity(playerId)
+    				local t = GetCameraTransform()
+    				local localBack = Vec(0, 0, 7.6*Power/10970)
+    				local back = TransformToParentVec(t, localBack)
+    				local back1 = VecAdd(vel, back)
+    				if toolactive == true then
+    					--SetPlayerVelocity(playerId, back1)
+    					pvell = true
+    				end
+
+    				kamefiresound = true
+
+    				local d = 0.3*Power/50
+    				if d < 0.3 then
+    				d = 0.3
+    				end
+    				local soundrngg = math.random(1, 2)
+    				if soundrngg == 1 then
+    				PlaySound(KameCharge1, GetPlayerTransform(playerId).pos, d)
+    				elseif soundrngg == 2 then
+    				PlaySound(KameCharge1, GetPlayerTransform(playerId).pos, d)
+    				end
+    			end
+    		if FFlashFLoopStart then
+    			PlayLoop(FinalFlashFire, TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5)), 10, 10, 1) --playwpitch
+    		end
+    		if GetString("game.player.tool") == "fFlash" then
+    			if InputPressed("lmb") and not fFlashactive then
+    				mousex = 0
+    				mousex2 = 0
+    				mousey = 0
+    				mousey2 = 0
+    			end
+    			if InputReleased("lmb") and not fFlashactive then
+
+    			end
+    		end
+    		if InputReleased("rmb") and not fFlashactive then
+    			HandAnim = false
+    			FFlashEnded = false
+    		end
+    		if InputReleased("lmb") and kameChargee == 0 and not fFlashactive then
+    			HandSmoke = true
+    			if DImpact then
+    				EnvBack = true
+    				DImpact = false
+    				--SetEnvironmentProperty("exposure", 0.2/10, 25)
+    				--SetEnvironmentProperty("skyboxtint", 0.0, 0, 0.0)
+    				--SetEnvironmentProperty("constant", 0.00, 0.00, 0.00)
+    				--SetPostProcessingProperty("bloom", 10)
+    				--SetPostProcessingProperty("saturation", 0)
+    				--SetPostProcessingProperty("colorbalance", 1, 1, 1)
+    				--SetEnvironmentProperty("fogParams", 0, 0, 0, 0)
+    			end
+    			--HandAnim = false
+    			FFlashFLoopStart = true
+    			SetSoundLoopProgress(FinalFlashFire, 0)
+    			rHandT = 0
+    			hitcount = 0
+    			inuse = 0
+    			toolactive = true
+    			fFlashactive = true
+    			LightFlash = Power
+    		end
+
+    		if EnvBack == true and kameChargee > 0.015 then
+    			EnvBack = false
+    			--SetPostProcessingProperty("colorbalance", cBW1*15, cBW2*15, cBW3*15)
+    		end
+
+    		if kameChargee > 0.033 and kameChargee < 0.07 then
+    			--SetEnvironmentProperty("exposure", eBW, eBW2)
+    			--SetEnvironmentProperty("skyboxtint", sbW, sbW2, sbW3)
+    			--SetEnvironmentProperty("constant", c1, c2, c3)
+    			--SetPostProcessingProperty("bloom", bloomBW)
+    			--SetPostProcessingProperty("saturation", sBWs)
+    			--SetPostProcessingProperty("colorbalance", cBW1, cBW2, cBW3)
+    			--SetEnvironmentProperty("fogParams", fbW, fbW2, fbW3, fbW4)
+    		end
+
+    		if InputDown("lmb") and InputDown("w") then
+    			local vel1 = GetPlayerVelocity(playerId)
+    			local t1 = GetCameraTransform()
+    			local localBack1 = Vec(0, 0, -0.65*Power/2900)
+    			local back1 = TransformToParentVec(t1, localBack1)
+    			local back11 = VecAdd(vel1, back1)
+    			SetPlayerVelocity(playerId, back11)
+    		end
+
+    		--local b = GetToolBody()
+    		--if b ~= 0 then
+    		--local offset = Transform(Vec(0.4, -0.5, -0.48))
+    		--SetToolTransform(offset)
+    		--toolTrans = GetBodyTransform(b)
+    		--local toolPos = TransformToParentPoint(toolTrans, Vec(0.12, 0.2, -0.8))
+    		--local t5 = toolPos
+    		--local pos5 = t5
+    		--local dir5 = TransformToParentVec(t5, Vec(0, 0, -5))
+    		--local hit, dist, normal, shape = QueryRaycast(pos5, dir5, 30, .15)
+    		abcde = toolPos
+    		abcdef = aimpos
+    		DebugLine(pos5, dir5)
+    		--end
+
+    		if fFlashactive == true then
+    			kameChargee = kameChargee + dt/1.5
+    		end
+
+            if InputDown("lmb") then
+    			if toolactive == false then
+    				local rot = QuatLookAt(VecAdd(toolPos, Vec(math.random(-1, 1), math.random(-1, 1), math.random(-1, 1))), GetCameraTransform().pos)
+    				local transform = Transform(toolPos, Vec(math.random(-600, 600)/1000, math.random(-600, 600)/1000, math.random(-600, 600)/1000), rot)
+    				local v = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
+    				local v1 = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
+    				local life = rnd(0.75, 0.85)
+    				local t = GetBodyTransform(GetToolBody())
+    				local p = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35))
+    			end
+    		end
+
+    		if fFlashactive then
+    			LightFlash = LightFlash - dt*150
+    			if LightFlash <= 0 then LightFlash = 0 end
+    			local p = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35))
+    			PointLight(p, 1,1,1, LightFlash*5)
+    			PointLight(p, 1,1,0, Power/3)
+    				ParticleReset()
+    				ParticleStretch(5)
+    				ParticleAlpha(1)
+    				ParticleEmissive(3, 1, "easeout")
+    				ParticleGravity(0)
+    				local spherepradius = 1*Power/25
+    				local spherepradiusstart = 0.15
+    				if spherepradius > 5 then
+    					spherepradius = 5
+    				end
+    				if spherepradius < 0.35 then
+    					spherepradius = 0.35
+    				end
+    				ParticleRadius(spherepradiusstart, spherepradius)
+    				ParticleColor(1,1,0)
+    				ParticleTile(4)
+    				ParticleCollide(0)
+    				for i=1, 25 do
+    					--SpawnParticle(p, v, 0.1)
+    					local spherepradius1 = 1*Power/125
+    					local spherepradiusstart1 = 0.15
+    					if spherepradius1 > 3 then
+    						spherepradius1 = 3
+    					end
+    					if spherepradius1 < 0.25 then
+    						spherepradius1 = 0.25
+    					end
+    					ParticleRadius(spherepradiusstart1, spherepradius1)
+    					ParticleColor(1,1,1)
+    					ParticleAlpha(0, 1)
+    					ParticleCollide(0)
+    					--SpawnParticle(VecAdd(p, rndVec(Power/150)), v1, 0.1)
+    				end
+    				for i=1, 2 do
+    					ParticleReset()
+    					local spherepradiusstart2 = 1*Power/365
+    					local spherepradiusstart2 = 1
+    					if spherepradiusstart2 > 3 then
+    						spherepradiusstart2 = 3
+    					end
+    					if spherepradiusstart2 < 0.1 then
+    						spherepradiusstart2 = 0.1
+    					end
+    					ParticleTile(4)
+    					ParticleRadius(spherepradiusstart2, 0, "easeout")
+    					ParticleStretch(10)
+    					ParticleColor(1,1,0.125, 1,1,0.125, "easeout")
+    					ParticleEmissive(5)
+    					ParticleAlpha(1)
+    					ParticleCollide(0)
+    					--SpawnParticle(VecAdd(p, rndVec(Power/900)), rndVec(math.random(Power*800, Power*800)/1000), 0.1)
+    				end
+    				for i=1, Power*2 do
+    					local RndV = rndVec(Power/100)
+    					local Pos = VecAdd(p, RndV)
+    					local Rot = QuatLookAt(p, Pos)
+    					local T = Transform(Pos, Rot)
+    					local toCam = QuatLookAt(p, GetCameraTransform().pos)
+    					local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
+    					local sizeRnd = math.random(-i*1000/30, i*1000/30)/1000
+    					DrawSprite(Glow, T, i/100+sizeRnd, i/100+sizeRnd, 1.0, 1, 0.55, i/100, true, false) --beamstart
+    					DrawSprite(Glow, T2, i/16+sizeRnd, i/16+sizeRnd, 1.0, 1, 0.55, i/25000, true, false)
+    					DrawSprite(Glow, T2, i/26+sizeRnd, i/26+sizeRnd, 1.0, 1, 0.45, i/15000, true, false)
+    					DrawSprite(Glow, T2, i/52+sizeRnd, i/52+sizeRnd, 1.0, 1, 0.65, i/5000, true, false)
+    				end
+    		end
+
+    			if kameChargee > 0 and kameChargee < 1 then
+    			--toolactive = true
+    		if toolactive == true and fFlashactive == true then
+
+    				CF = Power*0.01 
+    				fov = GetInt("options.gfx.fov")
+    				fov2 = fov*1.23
+    				ff = NumberLerp(fov,fov2,CF)
+    				--SetCameraFov(ff)
+
+    			local vel = GetPlayerVelocity(playerId)
+    			local t = GetCameraTransform()
+    			local localBack = Vec(0, 0, 7.6*Power/140)
+    			local back = TransformToParentVec(t, localBack)
+    			local back1 = VecAdd(vel, back)
+
+    			if pvell == true then
+    				SetPlayerVelocity(playerId, back1)
+    				pvell = false
+    			end 
+    			uirng = math.random(50, 100)/1000*Power/130	
+    			hitcount = hitcount + 1
+    			if hitcount == 1 then
+    				--ShakeCamera(SCc*1.25)
+    			end
+
+    		local v = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
+    		local v1 = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
+    		local life = rnd(0.75, 0.85)
+    		local t = GetBodyTransform(GetToolBody())
+    		local p = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35))
+    		life = life*life * 0.15
+    		ParticleReset()
+    		ParticleAlpha(0.4, 0.4)
+    		ParticleEmissive(4.5, 0.5, "easeout")
+    		ParticleGravity(0)
+    		local spherepradius = 1*Power/40
+    		local spherepradiusstart = 0.15
+    		if spherepradius > 2.75 then
+    		spherepradius = 2.75
+    		end
+    		if spherepradius < 1.25 then
+    		spherepradius = 1.25
+    		end
+    		--if spherepradiusstart > 1 then
+    		--spherepradiusstart = 1
+    		--end
+    		ParticleRadius(spherepradiusstart, spherepradius)
+    		ParticleColor(1,1,0)
+    		ParticleTile(4)
+    		ParticleCollide(0)
+    		for i=1, 25 do
+    		--SpawnParticle(p, v, 0.1)
+    		local spherepradius1 = 1*Power/55
+    		local spherepradiusstart1 = 0.15
+    		if spherepradius1 > 1.25 then
+    		spherepradius1 = 1.25
+    		end
+    		if spherepradius1 < 0.5 then
+    		spherepradius1 = 0.5
+    		end
+    		--if spherepradiusstart1 > 1 then
+    		--spherepradiusstart1 = 1
+    		--end
+    		ParticleRadius(spherepradiusstart1, spherepradius1)
+    		ParticleColor(1, 1, 1)
+    		ParticleAlpha(0, 1)
+    		ParticleCollide(0)
+    		--SpawnParticle(p, v1, 0.1)
+    		--PointLight(p, 1, 1, 0, 0.25*Power/20)
+
+    		end
+
+    		if GetString("game.player.tool") == "fFlash" and GetPlayerVehicle(playerId) == 0 then
+    			local t = GetBodyTransform(GetToolBody())
+    			--local t = toolPos
+    			local tpos = VecAdd(t.pos, Vec(0, 25, 0))
+    			local trot = t.rot
+    			local pos = t
+    			local pos2 = TransformToParentPoint(t, Vec(1, -.6, 5))
+    			local dir1 = TransformToParentVec(t, Vec(0, 0, -1))
+
+    			local dx = -0.025
+    			local dx1 = dx/distancetest*23
+    			local dy = .02
+    			local dy1 = dy/distancetest*23
+    			local d = TransformToParentVec(t, Vec(dx1, dy1, -1))
+    			local p = TransformToParentPoint(t, Vec(.75, .1, 8.75))
+    			local v = GetPlayerVelocity(playerId)
+    			local p1 = VecSub(p,v)
+    			v = VecAdd(v, VecScale(dir1, -.1))
+    			local pvel = VecScale(v, .7)
+
+    			local vel1 = GetPlayerVelocity(playerId)
+    			local t1 = GetCameraTransform()
+    			local localBack1 = Vec(0, -0.35, 0.65*Power/105)
+    			local back1 = TransformToParentVec(t1, localBack1)
+    			local back11 = VecAdd(vel1, back1)
+    			local roll,yaw,pitch = GetQuatEuler(GetPlayerCameraTransform(playerId).rot)
+    				if roll > -30 then
+    					SetPlayerVelocity(playerId, back11)
+    				end
+    				volume = 1*Power/140
+    				if volume < 0.4 then
+    				volume = 0.4
+    				end
+    				local makeh = 0.8*Power/25
+    				local makeh1 = 0.8*Power/25
+    				if makeh < 0.6 then
+    				makeh = 0.6
+    				end
+    				if makeh1 < 0.6 then
+    				makeh1 = 0.6
+    				end
+    				if explactive == true then
+
+    				end
+
+    				PlayLoop(KameLaunch, GetPlayerTransform(playerId).pos, volume)
+    				--PlayLoop(KameLaunch1, toolPos, volume)
+
+    				timer = timer+dt
+
+    			if coolDown < 0 then
+    				local dir1 = TransformToParentVec(GetCameraTransform(), Vec(0, 0, -1))
+    				--local p = TransformToParentPoint(GetCameraTransform(), Vec(0,0,-1))
+    				--local dir2 = VecNormalize(VecSub(p, GetCameraTransform().pos))
+    				QueryRejectBody(GetToolBody())
+    				local maxDist = 500
+    				QueryRequire("visible")
+    				local hit, dist, normal, shape = QueryRaycast(GetCameraTransform().pos, dir1, maxDist)
+    				if hit then
+    					local hitpointt = VecAdd(GetCameraTransform().pos, VecScale(dir1, dist))
+    					local spawnPos = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35))
+    					local dir3 = VecNormalize(VecSub(hitpointt, spawnPos))
+    					spawnProjectile(spawnPos, VecScale(dir3, 155), 300)
+    					coolDown = 0.045*Power/120
+    				elseif not hit then
+    					local hitpointt = VecAdd(GetCameraTransform().pos, VecScale(dir1, dist))
+    					local spawnPos = TransformToParentPoint(GetPlayerTransform(playerId, true), Vec(-0.2, 1.2, -1.5 + -Power/35))
+    					local dir3 = VecNormalize(VecSub(hitpointt, spawnPos))
+    					spawnProjectile(spawnPos, VecScale(dir3, 155), 300)
+    					coolDown = 0.045*Power/120
+    				end
+    			end
+    		end
     end
-	
-	if #projectiles > 0 then
-        local shortestLifespanProjectile = projectiles[1]
-		if shortestLifespanProjectile.hit == false then
-			local hit, p, n, s = QueryClosestPoint(shortestLifespanProjectile.startPos, Power/30)
-			if not hit then
-				PointLight(shortestLifespanProjectile.startPos, 1,1,0.5, Power*4.5)
-			end
-		end
+
+    	end
+    	if coolDown >= 0.05 then coolDown = 0.05 end
+    	if kameChargee > 1 then
+    		FFlashEnded = true
+    		FFlashEndedT = 0
+    		kameChargee = 0
+    		Power1 = 0
+    		FFlashwasactive = true
+    		FFlashwasactiveT = 1
+    		fFlashactive = false
+    		LightningFlicker = 0
+    		EnergyBallFlicker = 0
+    		toolactive = false
+    	end
+
+    	if FFlashEnded then
+    		FFlashEndedT = FFlashEndedT + dt
+    	end
+
+    	if FFlashEndedT >= 1.5 then
+    		FFlashEndedT = 0
+    		FFlashEnded = false
+    		HandAnim = false
+    	end
+
+    	if FFlashwasactive then
+    		FFlashwasactiveT = FFlashwasactiveT + dt
+    	end
+
+    	if FFlashwasactiveT <= 0 then
+    		FFlashwasactive = false
+    		FFlashwasactiveT = 0
+    	end
+
+    	if FFlashwasactiveT >= 2 then
+    		FFlashwasactive = false
+    		FFlashwasactiveT = 0
+    	end
+
+    	end
+    	coolDown = coolDown - dt
+    	Flashtimer = Flashtimer + dt
+    	expltimer = expltimer + dt
+    	ProjParti = ProjParti + dt
+    	mhT = mhT + dt
+    	pushtimer = pushtimer + dt
+    	explosiontest = explosiontest + dt
+    	uitexttimer = uitexttimer + dt
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    	for i = #projHits, 1, -1 do
+            local projHit = projHits[i]
+    		projHit.lightT = projHit.lightT - dt*2
+    		projHit.lightT = math.max(0, projHit.lightT)
+    		projHit.DirT = projHit.DirT - dt*4
+    		projHit.DirT = math.max(0, projHit.DirT)
+            --local projHit.randomDir = math.random(1, 4)
+            --local projHit.explosionDir = nil
+    		if projHit.DirT <= 0 then
+    			projHit.FireBall = projHit.FireBall + dt*2
+    			math.min(1, projHit.FireBall)
+    			projHit.FireBallBack = projHit.FireBallBack - dt*2
+    			math.max(0, projHit.FireBallBack)
+    			if projHit.FireBall <= 0.1 then
+    				for x=1, 50 do
+    					ParticleReset()
+    					ParticleRadius(Power/200, Power/100)
+    					ParticleColor(1,0.2,0)
+    					ParticleType("smoke")
+    					ParticleAlpha(1, 0)
+    					ParticleEmissive(5, 0)
+    					ParticleTile(5)
+    					ParticleCollide(1)
+    					ParticleDrag(0.25)
+    					SpawnParticle(projHit.startPos, rndVec(Power/3), math.random(50, 50)/100)
+    				end
+    				for x=1, 25 do
+    					ParticleReset()
+    					ParticleRadius(math.max(0.05, Power/1000), 0)
+    					ParticleColor(1,0.3,0.2)
+    					ParticleAlpha(1)
+    					ParticleEmissive(5)
+    					ParticleTile(6)
+    					ParticleCollide(1)
+    					ParticleGravity(-16)
+    					ParticleDrag(0)
+    					ParticleStretch(0)
+    					SpawnParticle(projHit.startPos, rndVec(Power/3), math.random(250, 350)/100)
+    				end
+    			end
+    			if projHit.FireBall >= 0.1 and projHit.FireBall <= 0.2 then
+    				for x=1, Power*1.5 do
+    					ParticleReset()
+    					ParticleRadius(Power/200, Power/100)
+    					ParticleType("smoke")
+    					ParticleAlpha(0.4, 0, "easein")
+    					ParticleEmissive(5, 0, "easeout")
+    					ParticleTile(0)
+    					ParticleColor(0,0,0, 0.01,0.01,0.01, "easeout")
+    					ParticleCollide(1)
+    					ParticleDrag(x/150/2)
+    					SpawnParticle(projHit.startPos, rndVec(x/1.5), math.random(220, 340)/100)
+    				end
+    			end
+    			if projHit.FireBall <= 0.1 then
+    				for x=1, 20 do
+    					local rnd = rndVec(10)
+    					local pos = VecAdd(projHit.startPos, rnd)
+    					--SpawnDistortion(pos, VecScale(rnd, 16), 0.5, 200, 15, false, false)
+    				end
+    			end
+
+    			if projHit.FireBallBack >= 0 then
+
+    			end
+    		end
+
+    		--PointLight(projHit.startPos, 1,1,0.25, projHit.lightT*0)
+    		projHit.timer = projHit.timer + dt
+    		if projHit.timer >= 5 then
+    			table.remove(projHits, i)
+    		end
+
+    		if projHit.Hbool then
+    		projHit.Hbool = false
+    		local distance = VecLength(VecSub(GetPlayerTransform(playerId, true).pos, projHit.startPos)) 
+
+    		local hitPos = projHit.startPos
+    		SCc = 0.009*Power
+    		ShakeCamera(SCc/2)
+
+    		playsndrng = playsndrng + 1
+    		playsndrng1 = playsndrng1 + 1
+    		if playsndrng > 3 then
+    			if distance < 50 then
+    				if Power < 40 then
+    					PlaySound(fFlashLightExpl, hitPos, Power/60*3)
+    				end
+    			end
+    			playsndrng = 0
+    		end
+
+    		if playsndrng1 > 2 then
+    			if distance <= 50 then
+    				if Power > 40 then
+    					PlaySound(fFlashExplosion, hitPos, Power/175*10, Power/175*10, math.random(1000, 1000)/1000)
+    				end
+    			elseif distance > 50 then
+    				if Power > 40 then
+    					PlaySound(fFlashExplosion, hitPos, Power/40*5, Power/40*5, math.random(1000, 1000)/1000)
+    				end
+    			end
+    			playsndrng1 = 0
+    		end		
+
+    			local particleVel2 = 35*Power/75
+    			if particleVel2 < 0.3 then
+    			particleVel2 = 0.3
+    			end
+    			ParticleAmount = Power
+    			if ParticleAmount <= 30 then
+    				ParticleAmount = 6
+    			end
+    			if ParticleAmount > 30 and ParticleAmount <= 60 then
+    				ParticleAmount = 13
+    			end
+    			if ParticleAmount > 60 then
+    				ParticleAmount = 20
+    			end
+    			for i=1, ParticleAmount do
+    				ParticleReset()
+    				--ParticleType("smoke")
+    				ParticleGravity(0)
+    				local SwaveVal = Power*2
+    				if SwaveVal < 50 then SwaveVal = 50 end
+    				local v = rndVec(Power/10)
+    				ParticleAlpha(0.25, 0)
+    				local particlradioos = 2*Power/100
+    				if particlradioos < 0.15 then
+    					particlradioos = 0.15
+    				end
+    				if particlradioos > 1.15 then
+    					particlradioos = 1.15
+    				end
+    				ParticleRadius(particlradioos*1, particlradioos*2)
+    				ParticleEmissive(5, 5, "easeout")
+    				ParticleColor(1, 1, 0.25)
+    				ParticleTile(0)
+    				ParticleCollide(0)
+    				ParticleDrag(0)
+    				--SpawnParticle(hitPos, v, math.random(550, 1050)/1000)
+    			end
+    			for z=1, math.random(-1, 1) do
+    				local ParticleAmount2 = Power
+    				if ParticleAmount2 <= 30 then
+    					ParticleAmount2 = 6
+    				end
+    				if ParticleAmount2 > 30 and ParticleAmount2 <= 60 then
+    					ParticleAmount2 = 13
+    				end
+    				if ParticleAmount2 > 60 then
+    					ParticleAmount2 = 20
+    				end
+    				for i=1, ParticleAmount2 do
+    					ParticleReset()
+    					--ParticleType("smoke")
+    					ParticleGravity(-20)
+    					local SwaveVal = Power*2
+    					if SwaveVal < 50 then SwaveVal = 50 end
+    					local v = rndVec(Power/1.5)
+    					ParticleAlpha(1)
+    					local particlradioos = 2*Power/100
+    					if particlradioos < 0.15 then
+    						particlradioos = 0.15
+    					end
+    					if particlradioos > 1.15 then
+    						particlradioos = 1.15
+    					end
+    					ParticleRadius(particlradioos*0.4, 0)
+    					ParticleEmissive(5, 5, "easeout")
+    					ParticleColor(1, 1, 0.25)
+    					ParticleTile(4)
+    					ParticleStretch(0)
+    					ParticleCollide(1)
+    					ParticleDrag(0)
+    					--SpawnParticle(hitPos, v, math.random(400, 1450)/1000)
+    				end
+    			end
+    			for z=1, math.random(1, 1) do
+    				local ParticleAmount2 = Power*4
+    				if ParticleAmount2 <= 30 then
+    					ParticleAmount2 = 6
+    				end
+    				if ParticleAmount2 > 30 and ParticleAmount2 <= 60 then
+    					ParticleAmount2 = 13
+    				end
+    				if ParticleAmount2 > 60 then
+    					ParticleAmount2 = 20
+    				end
+    				for i=1, ParticleAmount2 do
+    					ParticleReset()
+    					--ParticleType("smoke")
+    					ParticleGravity(-20)
+    					local SwaveVal = Power*2
+    					if SwaveVal < 50 then SwaveVal = 50 end
+    					local v = rndVec(Power*1)
+    					ParticleAlpha(1)
+    					local particlradioos = 2*Power/100
+    					if particlradioos < 0.15 then
+    						particlradioos = 0.15
+    					end
+    					if particlradioos > 1.15 then
+    						particlradioos = 1.15
+    					end
+    					ParticleRadius(particlradioos*0.15, 0)
+    					ParticleEmissive(5, 5, "easeout")
+    					ParticleColor(1, 0.3, 0.25)
+    					ParticleTile(4)
+    					ParticleStretch(0)
+    					ParticleCollide(1)
+    					ParticleDrag(0)
+    					--SpawnParticle(hitPos, v, math.random(1400, 2450)/1000)
+    				end
+    			end
+    		end
+        end
+
+    	for i = #distortions, 1, -1 do
+    		local p = distortions[i]
+    		p.pos = VecAdd(p.pos, VecScale(p.vel, dt))
+
+    		p.time = p.time + dt
+    	end
+
+    	for i = #Auras, 1, - 1 do
+    		Aura = Auras[i]
+    		Aura.t = Aura.t + dt / 4
+    		if Aura.t > 1 then
+    			Aura.t = 1 
+    		end
+
+    		--Aura.endPos = Vec(10, 31 + math.sin(GetTime()*24.0)*3, 0)
+
+    		local direction = calculateBezierTangent(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
+    		local normalizedDirection = VecScale(VecNormalize(direction), 50)
+
+    		local newPos = calculateBezierPoint(Aura.t, Aura.startPos, Aura.controlPos, Aura.endPos)
+    		--SpawnParticle(newPos, VecAdd(normalizedDirection, rndVec(25)), 0.25)
+
+    		--PointLight(newPos, 0,0,1, 3)
+
+    		if Aura.t >= 1 then
+    			table.remove(Auras, i)
+    		end
+    	end
+
+    --LOOPEDSOUNDS
+    	local FFLASHLOOP = GetSoundLoopProgress(FinalFlashFire)
+    	if FFLASHLOOP >= 5.5 then
+    		FFlashFLoopStart = false
+    		SetSoundLoopProgress(FinalFlashFire, 5.5)
+    	end 
+
+    	for i = #FireGusts, 1, - 1 do
+    		local FireGust = FireGusts[i]
+    		FireGust.startPos = VecAdd(FireGust.startPos, VecScale(FireGust.velocity, 0.014))
+    	end
+
+    	for i = 1, #Lightnings - 1 do
+    		Lightnings[i].position = VecAdd(Lightnings[i].position, VecAdd(VecScale(GetPlayerVelocity(playerId), 0.015), rndVec(0.025)))
+    	end
+
+        table.sort(projectiles, function(a, b)
+            return (a.lifespan - a.timer) < (b.lifespan - b.timer)
+        end)
+
+        for i = #projectiles, 1, -1 do
+            local projectile = projectiles[i]
+
+            if not projectile.hit then
+
+                local displacement = VecScale(projectile.velocity, EaseInQuad(projectile.timer))
+                local newPos = VecAdd(projectile.startPos, displacement)
+
+    			QueryRejectBody(GetToolBody())
+    			QueryRequire("visible")
+                local hit, dist, normal, shape = QueryRaycast(projectile.startPos, VecNormalize(displacement), VecLength(displacement))
+
+                if hit then
+                    local hitPoint = VecAdd(projectile.startPos, VecScale(VecNormalize(displacement), dist))
+                    hitPos = hitPoint
+    				spawnProjHit(projectile.startPos, Vec(), 10, GetPlayerTransform(playerId))
+
+    				projectile.hit = true
+                else
+                    projectile.startPos = newPos
+                    projectile.traveledDistance = projectile.traveledDistance + VecLength(displacement)
+                    hitPos = projectile.startPos
+                    if projectile.traveledDistance >= projectile.maxDistance then
+                        projectile.hit = true
+                    end
+                end
+
+    			if projectile.timer >= 5 or projectile.traveledDistance >= projectile.maxDistance then 
+    				if projectile.timer < shortestLifetime then
+    					shortestLifetime = projectile.timer
+    					shortestLifetimeProjectileInfo = {
+    						startPos = projectile.startPos,
+    						velocity = projectile.velocity,
+    						timer = projectile.timer
+    					}
+    					PointLight(shortestLifetimeProjectileInfo.startPos, 1, 1, 1, 250)
+    				end
+    			end
+    			for x=1, math.random(-10, 1) do
+    				ParticleReset()
+    				ParticleType("smoke")
+    				ParticleRadius(Power/30)
+    				ParticleColor(0,0,1)
+    				ParticleAlpha(0)
+    				ParticleTile(4)
+    				SpawnParticle(projectile.startPos, VecScale(VecNormalize(displacement), 150), 0.5)
+    			end
+
+    			if projectile.hit and projectile.Hbool then
+    				local paints = 2.4*Power/25
+    				if paints < 0.8 then
+    					paints = 0.8
+    				end
+    				if Power < 60 then
+    					local makeh = 1.8*Power/30
+    					local makeh1 = 1.8*Power/30
+    					if makeh < 1 then
+    						makeh = 1
+    					end
+    					if makeh1 < 0.6 then
+    						makeh1 = 0.6
+    					end
+    					local pos = VecAdd(hitPos, rndVec(Power/40))
+    					Paint(pos, paints, "explosion")
+    					MakeHole(pos, makeh1/1, makeh1/1.55, makeh1/1.60)
+    				elseif Power > 60 then
+    					local pos = VecAdd(hitPos, rndVec(Power/40))
+    					local makeh1 = 1.8*Power/30
+    					Paint(pos, paints, "explosion")
+    					MakeHole(pos, makeh1/1, makeh1/1.05, makeh1*Power/20/1.1)
+    				end
+    				local fd = 20
+    				for i =1, 20 do
+    					SpawnFire(VecAdd(hitPos, Vec(math.random(-1000,1000)*Power/fd/1000, math.random(-1000,1000)*Power/fd/1000, math.random(-1000,1000)*Power/fd/1000)))
+    				end
+
+    				QueryRejectBody(GetToolBody())
+    				max = 4*Power/20
+    				local objectbodies = QueryAabbBodies( VecAdd(hitPos, Vec(-max, -max, -max)), VecAdd(hitPos, Vec(max, max, max)))
+    				for i = 1, #objectbodies do
+    					local objectbodies2 = objectbodies[i]
+    					if IsBodyDynamic(objectbodies2) then
+    					  local bb, bbba = GetBodyBounds(objectbodies2)
+    					  local direction = VecSub(VecLerp(bb, bbba, 0.5), hitPos)
+    					  local distance = VecLength(direction)
+    					  local mass = GetBodyMass(objectbodies2)
+    					  local angV = GetBodyAngularVelocity(objectbodies2)
+    					  local angVel = Vec(math.random(5, 15), math.random(-15, -5), 0)
+    					  direction = VecScale(direction, 1 / distance)
+    					  if distance < max and mass < 500 then --max * 100
+    					   local distScale = 1 - math.min(distance / max, 0.9)
+    					  local vel = GetBodyVelocity(objectbodies2)
+    						vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 7.5*Power/105 * distScale)) --50
+    						SetBodyVelocity(objectbodies2, vel)
+    						SetBodyAngularVelocity(objectbodies2, angVel)
+    						elseif distance < max and mass > 500 then
+    						local distScale = 1 - math.min(distance / max, 0.9)
+    						local vel = GetBodyVelocity(objectbodies2)
+    						vel = VecAdd(GetBodyVelocity(objectbodies2), VecScale(direction, 5*Power/105 * distScale)) --50
+    						SetBodyVelocity(objectbodies2, vel)
+    						end
+    					  end
+    				   end
+    			end
+            end
+
+            projectile.timer = projectile.timer + dt*2
+            if projectile.timer >= projectile.lifespan or projectile.hit or projectile.traveledDistance >= projectile.maxDistance then
+    			--hitPos = projectile.startPos
+    			--detectBodies(projectile.startPos)
+                table.remove(projectiles, i)
+            end
+        end
+    		if fFlashactive == true then
+    			local t2 = GetCameraTransform()
+    			local pos2 = t2.pos	
+    			local dir2 = TransformToParentVec(t2, Vec(0, 0, -1))	
+    			local hit2, dist2, shape2 = QueryRaycast(pos2, dir2, 200)
+    			local hitpoint = VecAdd(pos2, VecScale(dir2, dist2))
+
+    			local t = GetCameraTransform()
+    			local fwd = TransformToParentVec(t, Vec(-0.0075/dist2, 0.0075/dist2, -1))
+    			local maxDist = 300
+    			local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist)
+    			if not hit then
+    				dist = maxDist
+    			end
+    		end
+end
+
+function client.draw()
+    for i = #distortions, 1, -1 do
+    	local p = distortions[i]
+    	-- update position
+
+    	local camPos = GetCameraTransform().pos
+    	local dirToCam = VecNormalize(VecSub(camPos, p.pos))  -- from projectile to camera
+    	local distToCam = VecLength(VecSub(camPos, p.pos))
+
+    	local hit2, dist2, normal2, shape2 = QueryRaycast(p.pos, dirToCam, distToCam)
+    	if hit2 then
+    		p.isVisible = 0
+    	elseif not hit2 then
+    		p.isVisible = 1
+    	end
+
+    	if p.time > p.lifetime then
+    		table.remove(distortions, i)
+    	else
+    		-- project world position to screen
+    		local x, y, dist = UiWorldToPixel(p.pos)
+    		if dist ~= 0 then
+    			local newtime = p.time * 1
+    			local timeFactor = 1 - (newtime / p.lifetime)  -- shrink over time
+    			local blurStrength = timeFactor
+    			local camPos = GetCameraTransform().pos
+    			local distToPlayer = VecLength(VecSub(p.pos, camPos))
+
+    			local scaleComp = 1 / math.max(1, dist*4)
+
+    			local baseSize = math.max(0.1, math.min(2825, p.DistortionSize * 25 - distToCam*5)) -- this limits the base size so u gotta increase it if u want larger distortions
+
+    			local layers = math.ceil(math.max(0, (p.layerC) * (1 - (p.time / p.lifetime))))
+
+    			if p.debugMode then
+    				DebugCross(p.pos, 1)
+    			end
+
+    			for j = 1, layers do
+    				local layerProgress = (j - 1) / (layers - 1)
+    				local growthFactor = 1 + layerProgress * 3
+    				local size = baseSize * growthFactor * timeFactor -- maybe boolean for size time factor
+    				if p.timeScale then
+    					size = baseSize * growthFactor * timeFactor
+    				else
+    					size = baseSize * growthFactor
+    				end
+    				local falloff = 1 - layerProgress
+    				local layerBlur = blurStrength * falloff
+    				local layerAlpha = 0.02 * blurStrength * falloff
+
+    				local scaledSize = math.max(1, size * scaleComp) -- center it
+    				local halfSize = scaledSize / 2
+
+    				UiPush()
+    					UiTranslate(x - halfSize, y - halfSize)
+    					UiWindow(scaledSize, scaledSize, true, false)
+    					UiPush()
+    						if p.isVisible == 1 then
+    							UiBlur(layerBlur / 100)
+    							UiColor(1, 0, 0, 1)
+    							if p.debugMode then
+    								UiRectOutline(scaledSize, scaledSize, 2)
+    							end
+    						end
+    					UiPop()
+    				UiPop()
+    			end
+    		end
+    	end
     end
-	
-		if ExplFlash > 0 then
-		    local a = VecAdd (hitPos2andhalf, Vec(0, 0.1, 0))
-			local b = math.random(10, 20)
-			ExplFlash = ExplFlash - dt*b
-		end
-		if ExplFlash1 > 0 then
-		    local a = VecAdd (hitPos2andhalf, Vec(0, 0, 0))
-			local b1 = math.random(55, 65)
-
-			ExplFlash1 = ExplFlash1 - dt*b1
-		end
-	--end
-	
-	
-	--[[if GetString("game.player.tool") == "fFlash" and canShoot() and HandAnim then
-		rHandT = rHandT + dt
-		local rHandA = EaseInExpo(rHandT)
-		local right, left = GetToolHandPoseWorldTransform()
-		PointLight(TransformToParentPoint(right, Vec(0,0,-3)), 1,1,1, 2)
-		SetToolHandPoseLocalTransform(Transform(Vec(-0.2 + rHandA, 0, -0.5)), Transform(Vec(-0.6, 0, -0.5), QuatEuler(0, 180, 0)))
-	end]]
-	
-if GetString("game.player.tool") == "fFlash" and canShoot() then
-	if ProjParti > 0.001 then
-		ProjPart = false
-	end
-			
-			beamparticl = 0
-			
-			if explactive == true then
-			if pushtimer > 0 and pushtimer < 0.04 then
-			--push(blastpoint1)
-			explactive = false
-			end
-			end
-
-			local b = GetToolBody()
-
-			if b ~= 0 then
-			local offset = Transform(Vec(0.4, -1, -0.3))
-			SetToolTransform(offset)
-			SetToolTransformOverride(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.12, 0.2, -0.8))
-			end
-			if InputDown("lmb") then
-			--local transform = TransformToParentTransform(GetPlayerCameraTransform(), Transform(Vec(0, 5, 0), QuatAxisAngle(Vec(0, 1, 0), 45)))
-			--SetCameraTransform(transform)
-			end
-			
-			a1 = 1
-			
-			if InputDown("lmb") then
-			PlayLoop(ChargePower, GetPlayerTransform().pos, Power/150)
-			uiheight = uiheight - 2
-			if uiheight < -200 then
-			uiheight = -200
-			end
-			Power = Power + dt*75
-			if Power >= 100 then
-			Power = 100
-			end
-			end
-			if Power < 20 then
-				Power = 20
-			end
-			if not fFlashactive and not InputDown("lmb") and Power > 10 then
-				Power = Power - dt*80
-			end
-			if InputDown("q") then
-			PlayLoop(ChargePower, GetPlayerTransform().pos, Power/150)
-			uiheight = uiheight + 2
-			if uiheight > -1 then
-			uiheight = -1
-			end
-			--Power = Power -1
-			--if Power < 1 then
-			--Power = 1
-			--end
-			end
-			if InputDown("lmb") then
-			Power1 = Power1 + dt*0.5
-			if Power1 > 1 then
-			Power1 = 1
-			end
-			end
-			--if InputDown("q") then
-			--Power1 = Power1 -0.02
-			--if Power1 < 0 then
-			--Power1 = 0
-			--end
-			--end
-			
-			if InputDown("lmb") and InputPressed ("esc") then
-				toolactive = false
-			end
-			
-			
-			if InputPressed("lmb") and not fFlashactive then
-				HandAnim = true
-				rHandT = 0
-				Power = 0
-				local vel = GetPlayerVelocity()
-				local t = GetCameraTransform()
-				local localBack = Vec(0, 0, 7.6*Power/10970)
-				local back = TransformToParentVec(t, localBack)
-				local back1 = VecAdd(vel, back)
-				if toolactive == true then
-					--SetPlayerVelocity(back1)
-					pvell = true
-				end
-				
-				kamefiresound = true
-				
-				local d = 0.3*Power/50
-				if d < 0.3 then
-				d = 0.3
-				end
-				local soundrngg = math.random(1, 2)
-				if soundrngg == 1 then
-				PlaySound(KameCharge1, GetPlayerTransform().pos, d)
-				elseif soundrngg == 2 then
-				PlaySound(KameCharge1, GetPlayerTransform().pos, d)
-				end
-			end
-		if FFlashFLoopStart then
-			PlayLoop(FinalFlashFire, TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5)), 10, 10, 1) --playwpitch
-		end
-		if GetString("game.player.tool") == "fFlash" then
-			if InputPressed("lmb") and not fFlashactive then
-				mousex = 0
-				mousex2 = 0
-				mousey = 0
-				mousey2 = 0
-			end
-			if InputReleased("lmb") and not fFlashactive then
-
-			end
-		end
-		if InputReleased("rmb") and not fFlashactive then
-			HandAnim = false
-			FFlashEnded = false
-		end
-		if InputReleased("lmb") and kameChargee == 0 and not fFlashactive then
-			HandSmoke = true
-			if DImpact then
-				EnvBack = true
-				DImpact = false
-				--SetEnvironmentProperty("exposure", 0.2/10, 25)
-				--SetEnvironmentProperty("skyboxtint", 0.0, 0, 0.0)
-				--SetEnvironmentProperty("constant", 0.00, 0.00, 0.00)
-				--SetPostProcessingProperty("bloom", 10)
-				--SetPostProcessingProperty("saturation", 0)
-				--SetPostProcessingProperty("colorbalance", 1, 1, 1)
-				--SetEnvironmentProperty("fogParams", 0, 0, 0, 0)
-			end
-			--HandAnim = false
-			FFlashFLoopStart = true
-			SetSoundLoopProgress(FinalFlashFire, 0)
-			rHandT = 0
-			hitcount = 0
-			inuse = 0
-			toolactive = true
-			fFlashactive = true
-			LightFlash = Power
-		end
-				
-		if EnvBack == true and kameChargee > 0.015 then
-			EnvBack = false
-			--SetPostProcessingProperty("colorbalance", cBW1*15, cBW2*15, cBW3*15)
-		end
-
-		if kameChargee > 0.033 and kameChargee < 0.07 then
-			--SetEnvironmentProperty("exposure", eBW, eBW2)
-			--SetEnvironmentProperty("skyboxtint", sbW, sbW2, sbW3)
-			--SetEnvironmentProperty("constant", c1, c2, c3)
-			--SetPostProcessingProperty("bloom", bloomBW)
-			--SetPostProcessingProperty("saturation", sBWs)
-			--SetPostProcessingProperty("colorbalance", cBW1, cBW2, cBW3)
-			--SetEnvironmentProperty("fogParams", fbW, fbW2, fbW3, fbW4)
-		end
-		
-		if InputDown("lmb") and InputDown("w") then
-			local vel1 = GetPlayerVelocity()
-			local t1 = GetCameraTransform()
-			local localBack1 = Vec(0, 0, -0.65*Power/2900)
-			local back1 = TransformToParentVec(t1, localBack1)
-			local back11 = VecAdd(vel1, back1)
-			SetPlayerVelocity(back11)
-		end
-			
-		--local b = GetToolBody()
-		--if b ~= 0 then
-		--local offset = Transform(Vec(0.4, -0.5, -0.48))
-		--SetToolTransform(offset)
-		--toolTrans = GetBodyTransform(b)
-		--local toolPos = TransformToParentPoint(toolTrans, Vec(0.12, 0.2, -0.8))
-		--local t5 = toolPos
-		--local pos5 = t5
-		--local dir5 = TransformToParentVec(t5, Vec(0, 0, -5))
-		--local hit, dist, normal, shape = QueryRaycast(pos5, dir5, 30, .15)
-		abcde = toolPos
-		abcdef = aimpos
-		DebugLine(pos5, dir5)
-		--end
-		
-		if fFlashactive == true then
-			kameChargee = kameChargee + dt/1.5
-		end
-
-        if InputDown("lmb") then
-			if toolactive == false then
-				local rot = QuatLookAt(VecAdd(toolPos, Vec(math.random(-1, 1), math.random(-1, 1), math.random(-1, 1))), GetCameraTransform().pos)
-				local transform = Transform(toolPos, Vec(math.random(-600, 600)/1000, math.random(-600, 600)/1000, math.random(-600, 600)/1000), rot)
-				local v = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
-				local v1 = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
-				local life = rnd(0.75, 0.85)
-				local t = GetBodyTransform(GetToolBody())
-				local p = TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35))
-			end
-		end
-		
-		if fFlashactive then
-			LightFlash = LightFlash - dt*150
-			if LightFlash <= 0 then LightFlash = 0 end
-			local p = TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35))
-			PointLight(p, 1,1,1, LightFlash*5)
-			PointLight(p, 1,1,0, Power/3)
-				ParticleReset()
-				ParticleStretch(5)
-				ParticleAlpha(1)
-				ParticleEmissive(3, 1, "easeout")
-				ParticleGravity(0)
-				local spherepradius = 1*Power/25
-				local spherepradiusstart = 0.15
-				if spherepradius > 5 then
-					spherepradius = 5
-				end
-				if spherepradius < 0.35 then
-					spherepradius = 0.35
-				end
-				ParticleRadius(spherepradiusstart, spherepradius)
-				ParticleColor(1,1,0)
-				ParticleTile(4)
-				ParticleCollide(0)
-				for i=1, 25 do
-					--SpawnParticle(p, v, 0.1)
-					local spherepradius1 = 1*Power/125
-					local spherepradiusstart1 = 0.15
-					if spherepradius1 > 3 then
-						spherepradius1 = 3
-					end
-					if spherepradius1 < 0.25 then
-						spherepradius1 = 0.25
-					end
-					ParticleRadius(spherepradiusstart1, spherepradius1)
-					ParticleColor(1,1,1)
-					ParticleAlpha(0, 1)
-					ParticleCollide(0)
-					--SpawnParticle(VecAdd(p, rndVec(Power/150)), v1, 0.1)
-				end
-				for i=1, 2 do
-					ParticleReset()
-					local spherepradiusstart2 = 1*Power/365
-					local spherepradiusstart2 = 1
-					if spherepradiusstart2 > 3 then
-						spherepradiusstart2 = 3
-					end
-					if spherepradiusstart2 < 0.1 then
-						spherepradiusstart2 = 0.1
-					end
-					ParticleTile(4)
-					ParticleRadius(spherepradiusstart2, 0, "easeout")
-					ParticleStretch(10)
-					ParticleColor(1,1,0.125, 1,1,0.125, "easeout")
-					ParticleEmissive(5)
-					ParticleAlpha(1)
-					ParticleCollide(0)
-					--SpawnParticle(VecAdd(p, rndVec(Power/900)), rndVec(math.random(Power*800, Power*800)/1000), 0.1)
-				end
-				for i=1, Power*2 do
-					local RndV = rndVec(Power/100)
-					local Pos = VecAdd(p, RndV)
-					local Rot = QuatLookAt(p, Pos)
-					local T = Transform(Pos, Rot)
-					local toCam = QuatLookAt(p, GetCameraTransform().pos)
-					local T2 = Transform(p, QuatRotateQuat(toCam, QuatEuler(0,0,math.sin(GetTime()*3)*3000)))
-					local sizeRnd = math.random(-i*1000/30, i*1000/30)/1000
-					DrawSprite(Glow, T, i/100+sizeRnd, i/100+sizeRnd, 1.0, 1, 0.55, i/100, true, false) --beamstart
-					DrawSprite(Glow, T2, i/16+sizeRnd, i/16+sizeRnd, 1.0, 1, 0.55, i/25000, true, false)
-					DrawSprite(Glow, T2, i/26+sizeRnd, i/26+sizeRnd, 1.0, 1, 0.45, i/15000, true, false)
-					DrawSprite(Glow, T2, i/52+sizeRnd, i/52+sizeRnd, 1.0, 1, 0.65, i/5000, true, false)
-				end
-		end
-
-			if kameChargee > 0 and kameChargee < 1 then
-			--toolactive = true
-		if toolactive == true and fFlashactive == true then
-		
-				CF = Power*0.01 
-				fov = GetInt("options.gfx.fov")
-				fov2 = fov*1.23
-				ff = NumberLerp(fov,fov2,CF)
-				--SetCameraFov(ff)
-		
-			local vel = GetPlayerVelocity()
-			local t = GetCameraTransform()
-			local localBack = Vec(0, 0, 7.6*Power/140)
-			local back = TransformToParentVec(t, localBack)
-			local back1 = VecAdd(vel, back)
-
-			
-			if pvell == true then
-				SetPlayerVelocity(back1)
-				pvell = false
-			end 
-			uirng = math.random(50, 100)/1000*Power/130	
-			hitcount = hitcount + 1
-			if hitcount == 1 then
-				--ShakeCamera(SCc*1.25)
-			end
-			
-			
-		local v = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
-		local v1 = VecAdd(Vec(1, 1, 1), rndVec(rnd(1*0.5, 1*1.5))) --VecAdd(Vec(0, 15, 0 ), rndVec(rnd(15*0.5, 15*1.5)))
-		local life = rnd(0.75, 0.85)
-		local t = GetBodyTransform(GetToolBody())
-		local p = TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35))
-		life = life*life * 0.15
-		ParticleReset()
-		ParticleAlpha(0.4, 0.4)
-		ParticleEmissive(4.5, 0.5, "easeout")
-		ParticleGravity(0)
-		local spherepradius = 1*Power/40
-		local spherepradiusstart = 0.15
-		if spherepradius > 2.75 then
-		spherepradius = 2.75
-		end
-		if spherepradius < 1.25 then
-		spherepradius = 1.25
-		end
-		--if spherepradiusstart > 1 then
-		--spherepradiusstart = 1
-		--end
-		ParticleRadius(spherepradiusstart, spherepradius)
-		ParticleColor(1,1,0)
-		ParticleTile(4)
-		ParticleCollide(0)
-		for i=1, 25 do
-		--SpawnParticle(p, v, 0.1)
-		local spherepradius1 = 1*Power/55
-		local spherepradiusstart1 = 0.15
-		if spherepradius1 > 1.25 then
-		spherepradius1 = 1.25
-		end
-		if spherepradius1 < 0.5 then
-		spherepradius1 = 0.5
-		end
-		--if spherepradiusstart1 > 1 then
-		--spherepradiusstart1 = 1
-		--end
-		ParticleRadius(spherepradiusstart1, spherepradius1)
-		ParticleColor(1, 1, 1)
-		ParticleAlpha(0, 1)
-		ParticleCollide(0)
-		--SpawnParticle(p, v1, 0.1)
-		--PointLight(p, 1, 1, 0, 0.25*Power/20)
-		
-		end
-			
-		if GetString("game.player.tool") == "fFlash" and GetPlayerVehicle() == 0 then
-			local t = GetBodyTransform(GetToolBody())
-			--local t = toolPos
-			local tpos = VecAdd(t.pos, Vec(0, 25, 0))
-			local trot = t.rot
-			local pos = t
-			local pos2 = TransformToParentPoint(t, Vec(1, -.6, 5))
-			local dir1 = TransformToParentVec(t, Vec(0, 0, -1))
-			
-			local dx = -0.025
-			local dx1 = dx/distancetest*23
-			local dy = .02
-			local dy1 = dy/distancetest*23
-			local d = TransformToParentVec(t, Vec(dx1, dy1, -1))
-			local p = TransformToParentPoint(t, Vec(.75, .1, 8.75))
-			local v = GetPlayerVelocity()
-			local p1 = VecSub(p,v)
-			v = VecAdd(v, VecScale(dir1, -.1))
-			local pvel = VecScale(v, .7)
-				
-			local vel1 = GetPlayerVelocity()
-			local t1 = GetCameraTransform()
-			local localBack1 = Vec(0, -0.35, 0.65*Power/105)
-			local back1 = TransformToParentVec(t1, localBack1)
-			local back11 = VecAdd(vel1, back1)
-			local roll,yaw,pitch = GetQuatEuler(GetPlayerCameraTransform().rot)
-				if roll > -30 then
-					SetPlayerVelocity(back11)
-				end
-				volume = 1*Power/140
-				if volume < 0.4 then
-				volume = 0.4
-				end
-				local makeh = 0.8*Power/25
-				local makeh1 = 0.8*Power/25
-				if makeh < 0.6 then
-				makeh = 0.6
-				end
-				if makeh1 < 0.6 then
-				makeh1 = 0.6
-				end
-				if explactive == true then
-
-				end
-				
-				PlayLoop(KameLaunch, GetPlayerTransform().pos, volume)
-				--PlayLoop(KameLaunch1, toolPos, volume)
-
-				timer = timer+dt
-
-			if coolDown < 0 then
-				local dir1 = TransformToParentVec(GetCameraTransform(), Vec(0, 0, -1))
-				--local p = TransformToParentPoint(GetCameraTransform(), Vec(0,0,-1))
-				--local dir2 = VecNormalize(VecSub(p, GetCameraTransform().pos))
-				QueryRejectBody(GetToolBody())
-				local maxDist = 500
-				QueryRequire("visible")
-				local hit, dist, normal, shape = QueryRaycast(GetCameraTransform().pos, dir1, maxDist)
-				if hit then
-					local hitpointt = VecAdd(GetCameraTransform().pos, VecScale(dir1, dist))
-					local spawnPos = TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35))
-					local dir3 = VecNormalize(VecSub(hitpointt, spawnPos))
-					spawnProjectile(spawnPos, VecScale(dir3, 155), 300)
-					coolDown = 0.045*Power/120
-				elseif not hit then
-					local hitpointt = VecAdd(GetCameraTransform().pos, VecScale(dir1, dist))
-					local spawnPos = TransformToParentPoint(GetPlayerTransform(true), Vec(-0.2, 1.2, -1.5 + -Power/35))
-					local dir3 = VecNormalize(VecSub(hitpointt, spawnPos))
-					spawnProjectile(spawnPos, VecScale(dir3, 155), 300)
-					coolDown = 0.045*Power/120
-				end
-			end
-		end
-end
-
-	end
-	if coolDown >= 0.05 then coolDown = 0.05 end
-	if kameChargee > 1 then
-		FFlashEnded = true
-		FFlashEndedT = 0
-		kameChargee = 0
-		Power1 = 0
-		FFlashwasactive = true
-		FFlashwasactiveT = 1
-		fFlashactive = false
-		LightningFlicker = 0
-		EnergyBallFlicker = 0
-		toolactive = false
-	end
-	
-	if FFlashEnded then
-		FFlashEndedT = FFlashEndedT + dt
-	end
-	
-	if FFlashEndedT >= 1.5 then
-		FFlashEndedT = 0
-		FFlashEnded = false
-		HandAnim = false
-	end
-	
-	if FFlashwasactive then
-		FFlashwasactiveT = FFlashwasactiveT + dt
-	end
-	
-	if FFlashwasactiveT <= 0 then
-		FFlashwasactive = false
-		FFlashwasactiveT = 0
-	end
-	
-	if FFlashwasactiveT >= 2 then
-		FFlashwasactive = false
-		FFlashwasactiveT = 0
-	end
-	
-	end
-	coolDown = coolDown - dt
-	Flashtimer = Flashtimer + dt
-	expltimer = expltimer + dt
-	ProjParti = ProjParti + dt
-	mhT = mhT + dt
-	pushtimer = pushtimer + dt
-	explosiontest = explosiontest + dt
-	uitexttimer = uitexttimer + dt
-end+       if GetString("game.player.tool") == "fFlash" and GetPlayerVehicle(playerId) == 0 then
+
+    	if InputDown("lmb") then
+    		local uiposx = 900 + math.random(Power/25*0.1, Power/50*2)
+    		 UiPush()
+    			local uiposx1 = uiposx + math.random(Power/50+1, Power/50+2)
+    			UiTranslate(UiCenter()+uiposx, UiMiddle())
+    			UiAlign("center middle")
+    			bluecolor = Power/100
+    			bluecolor1 = bluecolor-math.random(-100, 75)/1000
+    			local val = math.random(0, Power)/100
+    			UiColor(1,1,0, 10)
+    			UiImageBox("ui/common/gradient.png", UiWidth()-2000,uiheight*1.1, 0, 0)
+    		UiPop()
+    		local uiposx = 900 + math.random(Power/50*0.1, Power/50*2)
+    		UiPush()
+    			UiTranslate(UiCenter()+uiposx, UiMiddle())
+    			UiAlign("center middle")
+    			bluecolor = Power/100
+    			bluecolor1 = bluecolor-math.random(-100, 75)/1000
+    			local val = math.random(0, Power)/100
+    			UiColor(1,1,val, 10)
+    			UiImageBox("ui/common/gradient.png", UiWidth()-1990,uiheight, 0, 0)
+    		UiPop()
+    		UiPush()
+    			UiTranslate(UiCenter()+uiposx, UiMiddle())
+    			UiAlign("center middle")
+    			local val = math.random(0, Power)/100
+    			UiColor(1,1,val, 10)
+    			UiFont("bold.ttf", 42+val*4)
+    			UiTextOutline(0,0,0,5,0.5)
+    			UiText(math.ceil(Power))
+    		UiPop()
+    	end
+
+    	if toolactive == true and InputDown("lmb") and GetString("game.player.tool") == "fFlash" and GetPlayerVehicle(playerId) == 0 then
+    	--UiBlur(uirng)
+    	end
+
+    end
+end
+

```
