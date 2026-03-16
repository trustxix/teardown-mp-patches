# Migration Report: hrafn\hrafn.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafn.lua
+++ patched/hrafn\hrafn.lua
@@ -1,337 +1,325 @@
-#include "script/common.lua"
-#include "hrafnscripts/bodyscripts.lua"
-#include "hrafnscripts/aiscripts.lua"
-#include "hrafnscripts/flightscripts.lua"
-#include "hrafnscripts/weaponscripts.lua"
-#include "hrafnscripts/utilities.lua"
-
---gfx
-customGlare = LoadSprite("gfx/glare.png")
-cGRadius = 10
-cGMaxDist = 75
-cGMidPoint = 40
---no weapons yet I'm just testing squad/swarm ai
---flyerfp is my standardized tag for various utilities
-function init()
-	getAllChoppers() --base game heli bodies, for rejection
-	
-	--settings locations
-	aiSettings = FindLocation("aisettings")
-	attackSettings = FindLocation("attacksettings") --to spare space in ai settings
-	squadSettings = FindLocation("squadsettings")
-	healthSettings = FindLocation("healthsettings")
-
-	--sounds
-	thrusterHumLoop = LoadLoop("MOD/snd/jet.ogg", 40.0)
-	heardSound = LoadSound("robot/alert.ogg")
-	heardSound = LoadSound("snd/alertclicking.ogg")
-	shieldBreakSound = LoadSound("alarm3-loop.ogg")
-	shieldBreakSound2 = LoadSound("alarm1.ogg")
-	shieldPop = LoadSound("light/spark2.ogg")
-	dieSound = LoadSound("robot/disable0.ogg")
-	--weaponChargeSound = LoadSound("MOD/snd/plasma.ogg", 20.0)
-
-	--load body and searchlight
-	initBodies()
-	--shields 
-	core = FindShape("core") --the weakspot, breakable after shields down
-	corebody = GetShapeBody(core)
-	
-	shieldsEnabled = HasTag(healthSettings,"shields") or false --enable entire shielding routine in lua
-	if shieldsEnabled then initShields(); SetTag(core,"unbreakable") end
-	
-	--searchlight colors
-	initSearchLightColors()
-	
-	--ai flight params
-	targetPos= GetPlayerPos() --where thing is targeting
-	lookPos = GetPlayerPos()
-	hoverPos = GetPlayerPos() --where to hover at relative to targetpos
-	hrafnVel = Vec() --for actual velocity
-	hrafnSpeed = 6
-	height = math.random(8,15)	--height above ground, i originally wanted 6, TODO: editor-set height
-	toHeight = 0 --after accounting for ground
-	averageSurroundingHeight = 0 
-	
-	--ai awareness parameters
-	timeSinceLastSeen = 0
-	timeSinceChoosePatrol = 0
-	maxPatrolTime = tonumber(GetTagValue(aiSettings, "patroltime")) or 10
-	minPatrolRadius = tonumber(GetTagValue(aiSettings, "minpatroldist")) or 7
-	maxPatrolRadius = tonumber(GetTagValue(aiSettings, "maxpatroldist")) or 45
-	
-	timeSinceDistraction = 0
-	distractionThreshold = tonumber(GetTagValue(aiSettings, "distracttime")) or 3
-	timeToReposition = 0 --how long to spend moving to a hoverPos before switching
-	repositionTime = tonumber(GetTagValue(aiSettings, "repotime")) or 2.8
-	minHoverDist = tonumber(GetTagValue(aisettings,"minhoverdist")) or 20
-	maxHoverDist = tonumber(GetTagValue(aisettings,"maxhoverdist")) or 26
-	
-	playerSeen = false --player sighted
-	playerTracked = false --preparations for attack
-	playerSeeMeter = 0 --from 0 to 1
-	maxHearDist = tonumber(GetTagValue(aiSettings, "maxhear")) or 50 --maximum hearing distance
-	
-	--ai attack parameters
-	closeInStyle = HasTag(attackSettings,"closein") or false --whether to continue circling around or to get in close on playertracking
-	closeInMaxDist = tonumber(GetTagValue(attackSettings,"closemax")) or 40
-	closeInMinDist = tonumber(GetTagValue(attackSettings,"closemin")) or 20
-	blindFireable = HasTag(attackSettings,"blindfire") or false --blindfire enabled? most apparent in squad context
-	weaponActive = false
-	activeWeaponCount = 0
-	attackCount = 0 --how many attacks so far
-	
-	--weapons
-	
-	--autocannon
-	initAutoCannon()
-	initLaser() --laser
-	initRockets()
-	
-	--ai squad parameters and registries
-	--IMPORTANT: a squad masterscript (such as flyerfpsquad) is required to make a registry for the squad, this script WILL break
-	--if you force squadup to true without a squad registered
-	squad = GetTagValue(squadSettings,"squad") or "nil" --get squad name from the ai settings or nah, don't use nil in the squad script
-	squadreg = "level.flyerfp.squad."..squad
-	squadup = HasKey(squadreg) --if there is a squad then yes
-	noSwarm = HasTag(squadSettings, "noswarm") --disable swarm ai and resume normal flight activity but with shared target data
-	--DebugPrint(squadup)
-	squadSightLink = HasTag(squadSettings,"sightlink") --if true then it receives sighting information from other units
-	regTargetChange = squadreg..".targetchange" --squad alternative to choosePatrolTarget
-	regHeard = squadreg..".detect" --report sightings or sounds to this bool
-	regSighted = squadreg..".sighted" --report sightings to this bool
-	regSightLink = squadreg..".sightlink" --for communication with squad script
-	regDetectPos = squadreg..".detectpos" --report the location of the sighting or sound to this string registry
-	regDetectLink = squadreg..".detectlink" --respond to sounds others heard
-	regAttackCount = squadreg..".attackcount"
-	
-	active = true
-end
-
-function tick(dt)
-	if not active then return end
-	local selflist = FindBodies("flyerfp")
-	--ai sight
-	playerSeen = false
-	playerTracked = false
-	lightR,lightG,lightB = idleLightR,idleLightG,idleLightB
-	SetLightColor(lightSpot,lightR,lightG,lightB)
-	
-	sightMeter(dt)
-	isPlayerSeen()
-	
-	playerTracking()
-	if squadup then squadSight() end
-	
-	--ai hearing
-	hearSound()
-	
-	--navigation
-	newPatrolPoint()
-	
-	--DebugLine(targetPos,VecAdd(targetPos,Vec(0,1,0)))
-	
-	--movement
-	hoverMovement(dt)
-	
-	--aBOIDance (crude)
-	rejectSelf()
-	local hit, p, n, s = QueryClosestPoint(hrafnTargetPos,4)
-	local p2 = hrafnTargetPos[2] - p[2]
-	if HasTag(GetShapeBody(s),"flyerfp") then --yay for my trademarked tag
-		if hit and p2 < 1 and p2 > -1 then
-			local dir = VecSub(hrafnTransform.pos,p)
-			--DebugLine(hrafnTransform.pos,p)
-			--dir[2] = 0
-			dir = VecNormalize(dir)
-			hrafnTargetPos = VecAdd(hrafnTargetPos,VecScale(dir,7))
-		end
-	end
-	
-	--closeInStyle movement
-	if closeInStyle then
-		closeInMovement(dt)
-	end
-	--timers
-	timeSince(dt)
-	
-	--repositioning hoverPos
-	hoverReposition()
-	
-	--height control
-	computeSurroundingHeight(7)
-	computeSurroundingHeight(7,height)
-	computeSurroundingHeight(13,0,hrafnTransform.pos)
-	computeSurroundingHeight(13,0,hrafnTransform.pos)
-	computeSurroundingHeight(3.8,height)
-	computeSurroundingHeight(3.8,height,hrafnTransform.pos)
-	
-	heightControl()
-	
-	--rotate body
-	hrafnTargetRot = QuatLookAt(hrafnTransform.pos,lookPos)
-	local coreEulerX, coreEulerY, coreEulerZ = GetQuatEuler(hrafnTargetRot) --break quat into euler
-	coreEulerX = clamp(coreEulerX,-10,10) --limit pitch
-	hrafnTargetRot = QuatEuler(coreEulerX,coreEulerY,coreEulerZ) --rebuild quat with modified pitch
-	
-	--searchlight control 
-	local aimPos = VecCopy(lookPos)
-	local radius = clamp(timeSinceLastSeen,0,7)
-	if not lookaimAngle then lookaimAngle = 0; lookaimAngleY= 0 end --sorry for needing two aimangles cause i don't want leaks later
-	lookaimAngle = lookaimAngle%360 + dt
-	lookaimAngleY = lookaimAngleY%360 + dt*1.7 --one day I can make the look pattern more easily modifiable element
-	local x = math.cos(lookaimAngle) * radius
-	local z = math.sin(lookaimAngleY) * radius
-	aimPos = VecAdd(aimPos, Vec(x, 0, z))
-	--DebugCross(aimPos)
-	
-	local lightTransform = TransformToParentTransform(hrafnTransform,searchLightLocalTransform)
-	searchLightTargetRot = QuatLookAt(lightTransform.pos,aimPos)
-	lightTransform.rot = searchLightRot
-	
-	--set transforms
-	SetBodyTransform(hrafn,hrafnTransform)
-	SetBodyTransform(searchLight,lightTransform)
-	
-	forceStatic()
-	
-	--render custom glare
-	rejectSelf()
-	local glareTrans = Transform(GetBodyTransform(searchLight).pos,GetCameraTransform().rot)
-	local glaredir = VecSub(GetCameraTransform().pos,GetBodyTransform(searchLight).pos)
-	local glaredist = VecLength(glaredir)
-	glaredir = VecNormalize(glaredir)
-	local glareBlocked = QueryRaycast(GetBodyTransform(searchLight).pos,glaredir,math.min(glaredist,cGMaxDist))
-	if not glareBlocked and glaredist < cGMaxDist then
-		local radi = 1-clamp(glaredist-cGMidPoint,0,cGMaxDist-cGMidPoint)/(cGMaxDist-cGMidPoint)
-		radi = radi*cGRadius
-		DrawSprite(customGlare,glareTrans,radi,radi,lightR,lightG,lightB,1,false,true)
-		DrawSprite(customGlare,glareTrans,radi,radi,1,1,1,0.25,false,true)
-	end
-	
-	--weapon system tick
-	activeWeaponCount = 0
-	if not weaponActive and not playerDead() then --which weapons to use for the attack unless you died
-		local shouldFire = false
-		if squadup then
-			if squadSightLink and GetBool(regSightLink) then
-				if blindFireable or not blindFireable and canSeePlayer() then
-					shouldFire = true
-				end
-			end
-		end
-		if playerTracked then shouldFire = true end
-		if shouldFire and getDistanceToPlayer() < 41 then
-			local activated = false
-			if hasAutoCannon and math.random() < .5 then
-				autoCannonReady = true
-				autoCannonFireDelay = 1 +(math.random()-0.5)*0.5
-				autoCannonShotCount = math.random(autoCannonShotCounter[1],autoCannonShotCounter[2])
-				--PlaySound(weaponChargeSound,hrafnTransform.pos,3,false)
-				activated = true
-			end
-			if hasLaser and math.random() <0.5 then
-				laserTimer = laserTime 
-				laserDelay = 1 +(math.random()-0.5)*0.5
-				laserReady = true
-				--PlaySound(weaponChargeSound,hrafnTransform.pos,2,false)
-				activated = true
-			end
-			if activated then attackCount = attackCount + 1 end
-			if squadup and activated then
-				SetFloat(regAttackCount, GetFloat(regAttackCount)+1)
-				attackCount = GetFloat(regAttackCount)
-			end
-		end
-	end
-	if hasAutoCannon then tickAutoCannon(dt) end
-	if hasLaser then tickLaser(dt) end
-	if activeWeaponCount > 0 then weaponActive = true else weaponActive = false end
-	if hasRocket then
-		if playerTracked or squadup and squadSightLink and GetBool(regSightLink) then considerRocket() end
-		if not playerTracked or squadup and squadSightLink and not GetBool(regSightLink) then
-			if rocketTimer > 0 then
-				rocketTimer = math.max(0,rocketTimer - dt)
-				if rocketTimer <= 0 then
-					rocketLaunch()
-					considerRocketReload()
-				end
-			end
-		end
-	end
-
-	--shield status
-	if shieldsEnabled then--run shield routine here if has shields
-		tickShields(dt)
-	end
-	
-	if IsShapeBroken(core) or GetShapeBody(core) ~= corebody then --ded
-		active = false
-		local self = selflist --thanks convenient tag i made
-		for s, p in ipairs(self) do
-			--remove unbreakability from all shapes
-			local shapes = GetBodyShapes(p)
-			for s, shp in ipairs(shapes) do
-				RemoveTag(shp,"unbreakable")
-			end
-		
-			SetBodyDynamic(p, true)
-			RemoveTag(p,"flyerfp") --cause its dead n all
-			SetBodyVelocity(p,hrafnVel)
-		end
-		--PlaySound(dieSound, hrafnTransform.pos, 13,false)
-		MakeHole(GetBodyTransform(searchLight).pos,0.1,0.1,0.1)
-	end
-
-	for key, shell in ipairs(autoCannonShellHandler.shells) do --operation of autocannon shots in tickspace
-		if shell.active then 
-			autoCannonShellOperation(shell)
-		end
-	end
-	for key, rocket in ipairs(rocketHandler.rockets) do --operation of autocannon shots in tickspace
-		if rocket.active then 
-			rocketOperation(rocket)
-		end
-	end	
-	
-end
-
+#version 2
 function rnd(mi, ma)
         return math.random(0, 100)/100*(ma-mi)+mi
 end
 
-function update(dt)
-	if not active then return end
-
-    tipPos = TransformToParentPoint(GetBodyTransform(corebody), Vec(6.3, -0.3, -1.2))
-    tipPos2 = TransformToParentPoint(GetBodyTransform(corebody), Vec(-6.3, -0.3, -1.2))	
-
-	--smooth movement
-	local acc = VecSub(hrafnTargetPos,hrafnTransform.pos)
-	hrafnVel = VecAdd(hrafnVel,VecScale(acc,dt*1.5))
-	hrafnVel = VecScale(hrafnVel,0.98) --drag factor, 0 for immobilize, 1 for NO DRAG
-	hrafnTransform.pos = VecAdd(hrafnTransform.pos,VecScale(hrafnVel,dt))
-	--smooth rotation
-	hrafnTransform.rot = QuatSlerp(hrafnTransform.rot,hrafnTargetRot,0.008)
-	
-	--searchlight control
-	searchLightRot = QuatSlerp(searchLightRot, searchLightTargetRot, 0.13)
-	
-	ParticleReset()
-	ParticleType("smoke")
-	ParticleTile(5)
-	ParticleColor(0.95, 0.9, 1)
-	ParticleRadius(0.7, 0)
-	ParticleStretch(2, 20)
-	ParticleAlpha(0.7, 0.0)
-	ParticleDrag(0)
-	ParticleCollide(0)
-	ParticleGravity(-400)
-	ParticleSticky(0.0, 0.0)
-
-    for i=1,5 do 					
-		 SpawnParticle(tipPos, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
-		 SpawnParticle(tipPos2, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
-	end	
-	
-end+function server.init()
+    getAllChoppers() --base game heli bodies, for rejection
+    --settings locations
+    aiSettings = FindLocation("aisettings")
+    attackSettings = FindLocation("attacksettings") --to spare space in ai settings
+    squadSettings = FindLocation("squadsettings")
+    healthSettings = FindLocation("healthsettings")
+    --sounds
+    thrusterHumLoop = LoadLoop("MOD/snd/jet.ogg", 40.0)
+    --weaponChargeSound = LoadSound("MOD/snd/plasma.ogg", 20.0)
+    --load body and searchlight
+    initBodies()
+    --shields 
+    core = FindShape("core") --the weakspot, breakable after shields down
+    corebody = GetShapeBody(core)
+    shieldsEnabled = HasTag(healthSettings,"shields") or false --enable entire shielding routine in lua
+    if shieldsEnabled then initShields(); SetTag(core,"unbreakable") end
+
+    --searchlight colors
+    initSearchLightColors()
+
+    --ai flight params
+    targetPos= GetPlayerPos(playerId) --where thing is targeting
+    lookPos = GetPlayerPos(playerId)
+    hoverPos = GetPlayerPos(playerId) --where to hover at relative to targetpos
+    hrafnVel = Vec() --for actual velocity
+    hrafnSpeed = 6
+    height = math.random(8,15)	--height above ground, i originally wanted 6, TODO: editor-set height
+    toHeight = 0 --after accounting for ground
+    averageSurroundingHeight = 0 
+
+    --ai awareness parameters
+    timeSinceLastSeen = 0
+    timeSinceChoosePatrol = 0
+    maxPatrolTime = tonumber(GetTagValue(aiSettings, "patroltime")) or 10
+    minPatrolRadius = tonumber(GetTagValue(aiSettings, "minpatroldist")) or 7
+    maxPatrolRadius = tonumber(GetTagValue(aiSettings, "maxpatroldist")) or 45
+
+    timeSinceDistraction = 0
+    distractionThreshold = tonumber(GetTagValue(aiSettings, "distracttime")) or 3
+    timeToReposition = 0 --how long to spend moving to a hoverPos before switching
+    repositionTime = tonumber(GetTagValue(aiSettings, "repotime")) or 2.8
+    minHoverDist = tonumber(GetTagValue(aisettings,"minhoverdist")) or 20
+    maxHoverDist = tonumber(GetTagValue(aisettings,"maxhoverdist")) or 26
+
+    playerSeen = false --player sighted
+    playerTracked = false --preparations for attack
+    playerSeeMeter = 0 --from 0 to 1
+    maxHearDist = tonumber(GetTagValue(aiSettings, "maxhear")) or 50 --maximum hearing distance
+
+    --ai attack parameters
+    closeInStyle = HasTag(attackSettings,"closein") or false --whether to continue circling around or to get in close on playertracking
+    closeInMaxDist = tonumber(GetTagValue(attackSettings,"closemax")) or 40
+    closeInMinDist = tonumber(GetTagValue(attackSettings,"closemin")) or 20
+    blindFireable = HasTag(attackSettings,"blindfire") or false --blindfire enabled? most apparent in squad context
+    weaponActive = false
+    activeWeaponCount = 0
+    attackCount = 0 --how many attacks so far
+
+    --weapons
+
+    --autocannon
+    initAutoCannon()
+    initLaser() --laser
+    initRockets()
+
+    --ai squad parameters and registries
+    --IMPORTANT: a squad masterscript (such as flyerfpsquad) is required to make a registry for the squad, this script WILL break
+    --if you force squadup to true without a squad registered
+    squad = GetTagValue(squadSettings,"squad") or "nil" --get squad name from the ai settings or nah, don't use nil in the squad script
+    squadreg = "level.flyerfp.squad."..squad
+    squadup = HasKey(squadreg) --if there is a squad then yes
+    noSwarm = HasTag(squadSettings, "noswarm") --disable swarm ai and resume normal flight activity but with shared target data
+    --DebugPrint(squadup)
+    squadSightLink = HasTag(squadSettings,"sightlink") --if true then it receives sighting information from other units
+    regTargetChange = squadreg..".targetchange" --squad alternative to choosePatrolTarget
+    regHeard = squadreg..".detect" --report sightings or sounds to this bool
+    regSighted = squadreg..".sighted" --report sightings to this bool
+    regSightLink = squadreg..".sightlink" --for communication with squad script
+    regDetectPos = squadreg..".detectpos" --report the location of the sighting or sound to this string registry
+    regDetectLink = squadreg..".detectlink" --respond to sounds others heard
+    regAttackCount = squadreg..".attackcount"
+
+    active = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not active then return end
+        local selflist = FindBodies("flyerfp")
+        --ai sight
+        playerSeen = false
+        playerTracked = false
+        lightR,lightG,lightB = idleLightR,idleLightG,idleLightB
+        SetLightColor(lightSpot,lightR,lightG,lightB)
+
+        sightMeter(dt)
+        isPlayerSeen()
+
+        playerTracking()
+        if squadup then squadSight() end
+
+        --ai hearing
+        hearSound()
+
+        --navigation
+        newPatrolPoint()
+
+        --DebugLine(targetPos,VecAdd(targetPos,Vec(0,1,0)))
+
+        --movement
+        hoverMovement(dt)
+
+        --aBOIDance (crude)
+        rejectSelf()
+        local hit, p, n, s = QueryClosestPoint(hrafnTargetPos,4)
+        local p2 = hrafnTargetPos[2] - p[2]
+        if HasTag(GetShapeBody(s),"flyerfp") then --yay for my trademarked tag
+        	if hit and p2 < 1 and p2 > -1 then
+        		local dir = VecSub(hrafnTransform.pos,p)
+        		--DebugLine(hrafnTransform.pos,p)
+        		--dir[2] = 0
+        		dir = VecNormalize(dir)
+        		hrafnTargetPos = VecAdd(hrafnTargetPos,VecScale(dir,7))
+        	end
+        end
+
+        --closeInStyle movement
+        if closeInStyle then
+        	closeInMovement(dt)
+        end
+        --timers
+        timeSince(dt)
+
+        --repositioning hoverPos
+        hoverReposition()
+
+        --height control
+        computeSurroundingHeight(7)
+        computeSurroundingHeight(7,height)
+        computeSurroundingHeight(13,0,hrafnTransform.pos)
+        computeSurroundingHeight(13,0,hrafnTransform.pos)
+        computeSurroundingHeight(3.8,height)
+        computeSurroundingHeight(3.8,height,hrafnTransform.pos)
+
+        heightControl()
+
+        --rotate body
+        hrafnTargetRot = QuatLookAt(hrafnTransform.pos,lookPos)
+        local coreEulerX, coreEulerY, coreEulerZ = GetQuatEuler(hrafnTargetRot) --break quat into euler
+        coreEulerX = clamp(coreEulerX,-10,10) --limit pitch
+        hrafnTargetRot = QuatEuler(coreEulerX,coreEulerY,coreEulerZ) --rebuild quat with modified pitch
+
+        --searchlight control 
+        local aimPos = VecCopy(lookPos)
+        local radius = clamp(timeSinceLastSeen,0,7)
+        if not lookaimAngle then lookaimAngle = 0; lookaimAngleY= 0 end --sorry for needing two aimangles cause i don't want leaks later
+        lookaimAngle = lookaimAngle%360 + dt
+        lookaimAngleY = lookaimAngleY%360 + dt*1.7 --one day I can make the look pattern more easily modifiable element
+        local x = math.cos(lookaimAngle) * radius
+        local z = math.sin(lookaimAngleY) * radius
+        aimPos = VecAdd(aimPos, Vec(x, 0, z))
+        --DebugCross(aimPos)
+
+        local lightTransform = TransformToParentTransform(hrafnTransform,searchLightLocalTransform)
+        searchLightTargetRot = QuatLookAt(lightTransform.pos,aimPos)
+        lightTransform.rot = searchLightRot
+
+        --set transforms
+        SetBodyTransform(hrafn,hrafnTransform)
+        SetBodyTransform(searchLight,lightTransform)
+
+        forceStatic()
+
+        --render custom glare
+        rejectSelf()
+        local glareTrans = Transform(GetBodyTransform(searchLight).pos,GetCameraTransform().rot)
+        local glaredir = VecSub(GetCameraTransform().pos,GetBodyTransform(searchLight).pos)
+        local glaredist = VecLength(glaredir)
+        glaredir = VecNormalize(glaredir)
+        local glareBlocked = QueryRaycast(GetBodyTransform(searchLight).pos,glaredir,math.min(glaredist,cGMaxDist))
+        if not glareBlocked and glaredist < cGMaxDist then
+        	local radi = 1-clamp(glaredist-cGMidPoint,0,cGMaxDist-cGMidPoint)/(cGMaxDist-cGMidPoint)
+        	radi = radi*cGRadius
+        	DrawSprite(customGlare,glareTrans,radi,radi,lightR,lightG,lightB,1,false,true)
+        	DrawSprite(customGlare,glareTrans,radi,radi,1,1,1,0.25,false,true)
+        end
+
+        --weapon system tick
+        activeWeaponCount = 0
+        if not weaponActive and not playerDead() then --which weapons to use for the attack unless you died
+        	local shouldFire = false
+        	if squadup then
+        		if squadSightLink and GetBool(regSightLink) then
+        			if blindFireable or not blindFireable and canSeePlayer() then
+        				shouldFire = true
+        			end
+        		end
+        	end
+        	if playerTracked then shouldFire = true end
+        	if shouldFire and getDistanceToPlayer() < 41 then
+        		local activated = false
+        		if hasAutoCannon and math.random() < .5 then
+        			autoCannonReady = true
+        			autoCannonFireDelay = 1 +(math.random()-0.5)*0.5
+        			autoCannonShotCount = math.random(autoCannonShotCounter[1],autoCannonShotCounter[2])
+        			--PlaySound(weaponChargeSound,hrafnTransform.pos,3,false)
+        			activated = true
+        		end
+        		if hasLaser and math.random() <0.5 then
+        			laserTimer = laserTime 
+        			laserDelay = 1 +(math.random()-0.5)*0.5
+        			laserReady = true
+        			--PlaySound(weaponChargeSound,hrafnTransform.pos,2,false)
+        			activated = true
+        		end
+        		if activated then attackCount = attackCount + 1 end
+        		if squadup and activated then
+        			SetFloat(regAttackCount, GetFloat(regAttackCount)+1, true)
+        			attackCount = GetFloat(regAttackCount)
+        		end
+        	end
+        end
+        if hasAutoCannon then tickAutoCannon(dt) end
+        if hasLaser then tickLaser(dt) end
+        if activeWeaponCount ~= 0 then weaponActive = true else weaponActive = false end
+        if hasRocket then
+        	if playerTracked or squadup and squadSightLink and GetBool(regSightLink) then considerRocket() end
+        	if not playerTracked or squadup and squadSightLink and not GetBool(regSightLink) then
+        		if rocketTimer ~= 0 then
+        			rocketTimer = math.max(0,rocketTimer - dt)
+        			if rocketTimer <= 0 then
+        				rocketLaunch()
+        				considerRocketReload()
+        			end
+        		end
+        	end
+        end
+
+        --shield status
+        if shieldsEnabled then--run shield routine here if has shields
+        	tickShields(dt)
+        end
+
+        if IsShapeBroken(core) or GetShapeBody(core) ~= corebody then --ded
+        	active = false
+        	local self = selflist --thanks convenient tag i made
+        	for s, p in ipairs(self) do
+        		--remove unbreakability from all shapes
+        		local shapes = GetBodyShapes(p)
+        		for s, shp in ipairs(shapes) do
+        			RemoveTag(shp,"unbreakable")
+        		end
+
+        		SetBodyDynamic(p, true)
+        		RemoveTag(p,"flyerfp") --cause its dead n all
+        		SetBodyVelocity(p,hrafnVel)
+        	end
+        	--PlaySound(dieSound, hrafnTransform.pos, 13,false)
+        	MakeHole(GetBodyTransform(searchLight).pos,0.1,0.1,0.1)
+        end
+
+        for key, shell in ipairs(autoCannonShellHandler.shells) do --operation of autocannon shots in tickspace
+        	if shell.active then 
+        		autoCannonShellOperation(shell)
+        	end
+        end
+        for key, rocket in ipairs(rocketHandler.rockets) do --operation of autocannon shots in tickspace
+        	if rocket.active then 
+        		rocketOperation(rocket)
+        	end
+        end	
+    end
+end
+
+function client.init()
+    heardSound = LoadSound("robot/alert.ogg")
+    heardSound = LoadSound("snd/alertclicking.ogg")
+    shieldBreakSound = LoadSound("alarm3-loop.ogg")
+    shieldBreakSound2 = LoadSound("alarm1.ogg")
+    shieldPop = LoadSound("light/spark2.ogg")
+    dieSound = LoadSound("robot/disable0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if not active then return end
+
+       tipPos = TransformToParentPoint(GetBodyTransform(corebody), Vec(6.3, -0.3, -1.2))
+       tipPos2 = TransformToParentPoint(GetBodyTransform(corebody), Vec(-6.3, -0.3, -1.2))	
+
+    --smooth movement
+    local acc = VecSub(hrafnTargetPos,hrafnTransform.pos)
+    hrafnVel = VecAdd(hrafnVel,VecScale(acc,dt*1.5))
+    hrafnVel = VecScale(hrafnVel,0.98) --drag factor, 0 for immobilize, 1 for NO DRAG
+    hrafnTransform.pos = VecAdd(hrafnTransform.pos,VecScale(hrafnVel,dt))
+    --smooth rotation
+    hrafnTransform.rot = QuatSlerp(hrafnTransform.rot,hrafnTargetRot,0.008)
+
+    --searchlight control
+    searchLightRot = QuatSlerp(searchLightRot, searchLightTargetRot, 0.13)
+
+    ParticleReset()
+    ParticleType("smoke")
+    ParticleTile(5)
+    ParticleColor(0.95, 0.9, 1)
+    ParticleRadius(0.7, 0)
+    ParticleStretch(2, 20)
+    ParticleAlpha(0.7, 0.0)
+    ParticleDrag(0)
+    ParticleCollide(0)
+    ParticleGravity(-400)
+    ParticleSticky(0.0, 0.0)
+
+       for i=1,5 do 					
+    	 SpawnParticle(tipPos, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
+    	 SpawnParticle(tipPos2, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
+    end	
+end
+

```

---

# Migration Report: hrafn\hrafnintro.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafnintro.lua
+++ patched/hrafn\hrafnintro.lua
@@ -1,337 +1,325 @@
-#include "script/common.lua"
-#include "hrafnscripts/bodyscripts.lua"
-#include "hrafnscripts/aiscripts.lua"
-#include "hrafnscripts/flightscripts.lua"
-#include "hrafnscripts/weaponscripts2.lua"
-#include "hrafnscripts/utilities.lua"
-
---gfx
-customGlare = LoadSprite("gfx/glare.png")
-cGRadius = 10
-cGMaxDist = 75
-cGMidPoint = 40
---no weapons yet I'm just testing squad/swarm ai
---flyerfp is my standardized tag for various utilities
-function init()
-	getAllChoppers() --base game heli bodies, for rejection
-	
-	--settings locations
-	aiSettings = FindLocation("aisettings")
-	attackSettings = FindLocation("attacksettings") --to spare space in ai settings
-	squadSettings = FindLocation("squadsettings")
-	healthSettings = FindLocation("healthsettings")
-
-	--sounds
-	thrusterHumLoop = LoadLoop("MOD/snd/jet.ogg", 60.0)
-	heardSound = LoadSound("robot/alert.ogg")
-	heardSound = LoadSound("snd/alertclicking.ogg")
-	shieldBreakSound = LoadSound("alarm3-loop.ogg")
-	shieldBreakSound2 = LoadSound("alarm1.ogg")
-	shieldPop = LoadSound("light/spark2.ogg")
-	dieSound = LoadSound("robot/disable0.ogg")
-	weaponChargeSound = LoadSound("MOD/snd/plasma.ogg", 20.0)
-
-	--load body and searchlight
-	initBodies()
-	--shields 
-	core = FindShape("core") --the weakspot, breakable after shields down
-	corebody = GetShapeBody(core)
-	
-	shieldsEnabled = HasTag(healthSettings,"shields") or false --enable entire shielding routine in lua
-	if shieldsEnabled then initShields(); SetTag(core,"unbreakable") end
-	
-	--searchlight colors
-	initSearchLightColors()
-	
-	--ai flight params
-	targetPos= GetPlayerPos() --where thing is targeting
-	lookPos = GetPlayerPos()
-	hoverPos = GetPlayerPos() --where to hover at relative to targetpos
-	hrafnVel = Vec() --for actual velocity
-	hrafnSpeed = 6
-	height = math.random(8,15)	--height above ground, i originally wanted 6, TODO: editor-set height
-	toHeight = 0 --after accounting for ground
-	averageSurroundingHeight = 0 
-	
-	--ai awareness parameters
-	timeSinceLastSeen = 0
-	timeSinceChoosePatrol = 0
-	maxPatrolTime = tonumber(GetTagValue(aiSettings, "patroltime")) or 10
-	minPatrolRadius = tonumber(GetTagValue(aiSettings, "minpatroldist")) or 7
-	maxPatrolRadius = tonumber(GetTagValue(aiSettings, "maxpatroldist")) or 45
-	
-	timeSinceDistraction = 0
-	distractionThreshold = tonumber(GetTagValue(aiSettings, "distracttime")) or 3
-	timeToReposition = 0 --how long to spend moving to a hoverPos before switching
-	repositionTime = tonumber(GetTagValue(aiSettings, "repotime")) or 2.8
-	minHoverDist = tonumber(GetTagValue(aisettings,"minhoverdist")) or 20
-	maxHoverDist = tonumber(GetTagValue(aisettings,"maxhoverdist")) or 26
-	
-	playerSeen = false --player sighted
-	playerTracked = false --preparations for attack
-	playerSeeMeter = 0 --from 0 to 1
-	maxHearDist = tonumber(GetTagValue(aiSettings, "maxhear")) or 50 --maximum hearing distance
-	
-	--ai attack parameters
-	closeInStyle = HasTag(attackSettings,"closein") or false --whether to continue circling around or to get in close on playertracking
-	closeInMaxDist = tonumber(GetTagValue(attackSettings,"closemax")) or 40
-	closeInMinDist = tonumber(GetTagValue(attackSettings,"closemin")) or 20
-	blindFireable = HasTag(attackSettings,"blindfire") or false --blindfire enabled? most apparent in squad context
-	weaponActive = false
-	activeWeaponCount = 0
-	attackCount = 0 --how many attacks so far
-	
-	--weapons
-	
-	--autocannon
-	initAutoCannon()
-	initLaser() --laser
-	initRockets()
-	
-	--ai squad parameters and registries
-	--IMPORTANT: a squad masterscript (such as flyerfpsquad) is required to make a registry for the squad, this script WILL break
-	--if you force squadup to true without a squad registered
-	squad = GetTagValue(squadSettings,"squad") or "nil" --get squad name from the ai settings or nah, don't use nil in the squad script
-	squadreg = "level.flyerfp.squad."..squad
-	squadup = HasKey(squadreg) --if there is a squad then yes
-	noSwarm = HasTag(squadSettings, "noswarm") --disable swarm ai and resume normal flight activity but with shared target data
-	--DebugPrint(squadup)
-	squadSightLink = HasTag(squadSettings,"sightlink") --if true then it receives sighting information from other units
-	regTargetChange = squadreg..".targetchange" --squad alternative to choosePatrolTarget
-	regHeard = squadreg..".detect" --report sightings or sounds to this bool
-	regSighted = squadreg..".sighted" --report sightings to this bool
-	regSightLink = squadreg..".sightlink" --for communication with squad script
-	regDetectPos = squadreg..".detectpos" --report the location of the sighting or sound to this string registry
-	regDetectLink = squadreg..".detectlink" --respond to sounds others heard
-	regAttackCount = squadreg..".attackcount"
-	
-	active = true
-end
-
-function tick(dt)
-	if not active then return end
-	local selflist = FindBodies("flyerfp")
-	--ai sight
-	playerSeen = false
-	playerTracked = false
-	lightR,lightG,lightB = idleLightR,idleLightG,idleLightB
-	SetLightColor(lightSpot,lightR,lightG,lightB)
-	
-	sightMeter(dt)
-	isPlayerSeen()
-	
-	playerTracking()
-	if squadup then squadSight() end
-	
-	--ai hearing
-	hearSound()
-	
-	--navigation
-	newPatrolPoint()
-	
-	--DebugLine(targetPos,VecAdd(targetPos,Vec(0,1,0)))
-	
-	--movement
-	hoverMovement(dt)
-	
-	--aBOIDance (crude)
-	rejectSelf()
-	local hit, p, n, s = QueryClosestPoint(hrafnTargetPos,4)
-	local p2 = hrafnTargetPos[2] - p[2]
-	if HasTag(GetShapeBody(s),"flyerfp") then --yay for my trademarked tag
-		if hit and p2 < 1 and p2 > -1 then
-			local dir = VecSub(hrafnTransform.pos,p)
-			--DebugLine(hrafnTransform.pos,p)
-			--dir[2] = 0
-			dir = VecNormalize(dir)
-			hrafnTargetPos = VecAdd(hrafnTargetPos,VecScale(dir,7))
-		end
-	end
-	
-	--closeInStyle movement
-	if closeInStyle then
-		closeInMovement(dt)
-	end
-	--timers
-	timeSince(dt)
-	
-	--repositioning hoverPos
-	hoverReposition()
-	
-	--height control
-	computeSurroundingHeight(7)
-	computeSurroundingHeight(7,height)
-	computeSurroundingHeight(13,0,hrafnTransform.pos)
-	computeSurroundingHeight(13,0,hrafnTransform.pos)
-	computeSurroundingHeight(3.8,height)
-	computeSurroundingHeight(3.8,height,hrafnTransform.pos)
-	
-	heightControl()
-	
-	--rotate body
-	hrafnTargetRot = QuatLookAt(hrafnTransform.pos,lookPos)
-	local coreEulerX, coreEulerY, coreEulerZ = GetQuatEuler(hrafnTargetRot) --break quat into euler
-	coreEulerX = clamp(coreEulerX,-10,10) --limit pitch
-	hrafnTargetRot = QuatEuler(coreEulerX,coreEulerY,coreEulerZ) --rebuild quat with modified pitch
-	
-	--searchlight control 
-	local aimPos = VecCopy(lookPos)
-	local radius = clamp(timeSinceLastSeen,0,7)
-	if not lookaimAngle then lookaimAngle = 0; lookaimAngleY= 0 end --sorry for needing two aimangles cause i don't want leaks later
-	lookaimAngle = lookaimAngle%360 + dt
-	lookaimAngleY = lookaimAngleY%360 + dt*1.7 --one day I can make the look pattern more easily modifiable element
-	local x = math.cos(lookaimAngle) * radius
-	local z = math.sin(lookaimAngleY) * radius
-	aimPos = VecAdd(aimPos, Vec(x, 0, z))
-	--DebugCross(aimPos)
-	
-	local lightTransform = TransformToParentTransform(hrafnTransform,searchLightLocalTransform)
-	searchLightTargetRot = QuatLookAt(lightTransform.pos,aimPos)
-	lightTransform.rot = searchLightRot
-	
-	--set transforms
-	SetBodyTransform(hrafn,hrafnTransform)
-	SetBodyTransform(searchLight,lightTransform)
-	
-	forceStatic()
-	
-	--render custom glare
-	rejectSelf()
-	local glareTrans = Transform(GetBodyTransform(searchLight).pos,GetCameraTransform().rot)
-	local glaredir = VecSub(GetCameraTransform().pos,GetBodyTransform(searchLight).pos)
-	local glaredist = VecLength(glaredir)
-	glaredir = VecNormalize(glaredir)
-	local glareBlocked = QueryRaycast(GetBodyTransform(searchLight).pos,glaredir,math.min(glaredist,cGMaxDist))
-	if not glareBlocked and glaredist < cGMaxDist then
-		local radi = 1-clamp(glaredist-cGMidPoint,0,cGMaxDist-cGMidPoint)/(cGMaxDist-cGMidPoint)
-		radi = radi*cGRadius
-		DrawSprite(customGlare,glareTrans,radi,radi,lightR,lightG,lightB,1,false,true)
-		DrawSprite(customGlare,glareTrans,radi,radi,1,1,1,0.25,false,true)
-	end
-	
-	--weapon system tick
-	activeWeaponCount = 0
-	if not weaponActive and not playerDead() then --which weapons to use for the attack unless you died
-		local shouldFire = false
-		if squadup then
-			if squadSightLink and GetBool(regSightLink) then
-				if blindFireable or not blindFireable and canSeePlayer() then
-					shouldFire = true
-				end
-			end
-		end
-		if playerTracked then shouldFire = true end
-		if shouldFire and getDistanceToPlayer() < 41 then
-			local activated = false
-			if hasAutoCannon and math.random() < .5 then
-				autoCannonReady = true
-				autoCannonFireDelay = 1 +(math.random()-0.5)*0.5
-				autoCannonShotCount = math.random(autoCannonShotCounter[1],autoCannonShotCounter[2])
-				--PlaySound(weaponChargeSound,hrafnTransform.pos,3,false)
-				activated = true
-			end
-			if hasLaser and math.random() <0.5 then
-				laserTimer = laserTime 
-				laserDelay = 1 +(math.random()-0.5)*0.5
-				laserReady = true
-				--PlaySound(weaponChargeSound,hrafnTransform.pos,2,false)
-				activated = true
-			end
-			if activated then attackCount = attackCount + 1 end
-			if squadup and activated then
-				SetFloat(regAttackCount, GetFloat(regAttackCount)+1)
-				attackCount = GetFloat(regAttackCount)
-			end
-		end
-	end
-	if hasAutoCannon then tickAutoCannon(dt) end
-	if hasLaser then tickLaser(dt) end
-	if activeWeaponCount > 0 then weaponActive = true else weaponActive = false end
-	if hasRocket then
-		if playerTracked or squadup and squadSightLink and GetBool(regSightLink) then considerRocket() end
-		if not playerTracked or squadup and squadSightLink and not GetBool(regSightLink) then
-			if rocketTimer > 0 then
-				rocketTimer = math.max(0,rocketTimer - dt)
-				if rocketTimer <= 0 then
-					rocketLaunch()
-					considerRocketReload()
-				end
-			end
-		end
-	end
-
-	--shield status
-	if shieldsEnabled then--run shield routine here if has shields
-		tickShields(dt)
-	end
-	
-	if IsShapeBroken(core) or GetShapeBody(core) ~= corebody then --ded
-		active = false
-		local self = selflist --thanks convenient tag i made
-		for s, p in ipairs(self) do
-			--remove unbreakability from all shapes
-			local shapes = GetBodyShapes(p)
-			for s, shp in ipairs(shapes) do
-				RemoveTag(shp,"unbreakable")
-			end
-		
-			SetBodyDynamic(p, true)
-			RemoveTag(p,"flyerfp") --cause its dead n all
-			SetBodyVelocity(p,hrafnVel)
-		end
-		--PlaySound(dieSound, hrafnTransform.pos, 13,false)
-		MakeHole(GetBodyTransform(searchLight).pos,0.1,0.1,0.1)
-	end
-
-	for key, shell in ipairs(autoCannonShellHandler.shells) do --operation of autocannon shots in tickspace
-		if shell.active then 
-			autoCannonShellOperation(shell)
-		end
-	end
-	for key, rocket in ipairs(rocketHandler.rockets) do --operation of autocannon shots in tickspace
-		if rocket.active then 
-			rocketOperation(rocket)
-		end
-	end	
-	
-end
-
+#version 2
 function rnd(mi, ma)
         return math.random(0, 100)/100*(ma-mi)+mi
 end
 
-function update(dt)
-	if not active then return end
-
-    tipPos = TransformToParentPoint(GetBodyTransform(corebody), Vec(6.3, -0.3, -1.2))
-    tipPos2 = TransformToParentPoint(GetBodyTransform(corebody), Vec(-6.3, -0.3, -1.2))	
-
-	--smooth movement
-	local acc = VecSub(hrafnTargetPos,hrafnTransform.pos)
-	hrafnVel = VecAdd(hrafnVel,VecScale(acc,dt*1.5))
-	hrafnVel = VecScale(hrafnVel,0.98) --drag factor, 0 for immobilize, 1 for NO DRAG
-	hrafnTransform.pos = VecAdd(hrafnTransform.pos,VecScale(hrafnVel,dt))
-	--smooth rotation
-	hrafnTransform.rot = QuatSlerp(hrafnTransform.rot,hrafnTargetRot,0.008)
-	
-	--searchlight control
-	searchLightRot = QuatSlerp(searchLightRot, searchLightTargetRot, 0.13)
-	
-	ParticleReset()
-	ParticleType("smoke")
-	ParticleTile(5)
-	ParticleColor(0.95, 0.9, 1)
-	ParticleRadius(0.7, 0)
-	ParticleStretch(2, 20)
-	ParticleAlpha(0.7, 0.0)
-	ParticleDrag(0)
-	ParticleCollide(0)
-	ParticleGravity(-400)
-	ParticleSticky(0.0, 0.0)
-
-    for i=1,5 do 					
-		 SpawnParticle(tipPos, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
-		 SpawnParticle(tipPos2, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
-	end	
-	
-end+function server.init()
+    getAllChoppers() --base game heli bodies, for rejection
+    --settings locations
+    aiSettings = FindLocation("aisettings")
+    attackSettings = FindLocation("attacksettings") --to spare space in ai settings
+    squadSettings = FindLocation("squadsettings")
+    healthSettings = FindLocation("healthsettings")
+    --sounds
+    thrusterHumLoop = LoadLoop("MOD/snd/jet.ogg", 60.0)
+    --load body and searchlight
+    initBodies()
+    --shields 
+    core = FindShape("core") --the weakspot, breakable after shields down
+    corebody = GetShapeBody(core)
+    shieldsEnabled = HasTag(healthSettings,"shields") or false --enable entire shielding routine in lua
+    if shieldsEnabled then initShields(); SetTag(core,"unbreakable") end
+
+    --searchlight colors
+    initSearchLightColors()
+
+    --ai flight params
+    targetPos= GetPlayerPos(playerId) --where thing is targeting
+    lookPos = GetPlayerPos(playerId)
+    hoverPos = GetPlayerPos(playerId) --where to hover at relative to targetpos
+    hrafnVel = Vec() --for actual velocity
+    hrafnSpeed = 6
+    height = math.random(8,15)	--height above ground, i originally wanted 6, TODO: editor-set height
+    toHeight = 0 --after accounting for ground
+    averageSurroundingHeight = 0 
+
+    --ai awareness parameters
+    timeSinceLastSeen = 0
+    timeSinceChoosePatrol = 0
+    maxPatrolTime = tonumber(GetTagValue(aiSettings, "patroltime")) or 10
+    minPatrolRadius = tonumber(GetTagValue(aiSettings, "minpatroldist")) or 7
+    maxPatrolRadius = tonumber(GetTagValue(aiSettings, "maxpatroldist")) or 45
+
+    timeSinceDistraction = 0
+    distractionThreshold = tonumber(GetTagValue(aiSettings, "distracttime")) or 3
+    timeToReposition = 0 --how long to spend moving to a hoverPos before switching
+    repositionTime = tonumber(GetTagValue(aiSettings, "repotime")) or 2.8
+    minHoverDist = tonumber(GetTagValue(aisettings,"minhoverdist")) or 20
+    maxHoverDist = tonumber(GetTagValue(aisettings,"maxhoverdist")) or 26
+
+    playerSeen = false --player sighted
+    playerTracked = false --preparations for attack
+    playerSeeMeter = 0 --from 0 to 1
+    maxHearDist = tonumber(GetTagValue(aiSettings, "maxhear")) or 50 --maximum hearing distance
+
+    --ai attack parameters
+    closeInStyle = HasTag(attackSettings,"closein") or false --whether to continue circling around or to get in close on playertracking
+    closeInMaxDist = tonumber(GetTagValue(attackSettings,"closemax")) or 40
+    closeInMinDist = tonumber(GetTagValue(attackSettings,"closemin")) or 20
+    blindFireable = HasTag(attackSettings,"blindfire") or false --blindfire enabled? most apparent in squad context
+    weaponActive = false
+    activeWeaponCount = 0
+    attackCount = 0 --how many attacks so far
+
+    --weapons
+
+    --autocannon
+    initAutoCannon()
+    initLaser() --laser
+    initRockets()
+
+    --ai squad parameters and registries
+    --IMPORTANT: a squad masterscript (such as flyerfpsquad) is required to make a registry for the squad, this script WILL break
+    --if you force squadup to true without a squad registered
+    squad = GetTagValue(squadSettings,"squad") or "nil" --get squad name from the ai settings or nah, don't use nil in the squad script
+    squadreg = "level.flyerfp.squad."..squad
+    squadup = HasKey(squadreg) --if there is a squad then yes
+    noSwarm = HasTag(squadSettings, "noswarm") --disable swarm ai and resume normal flight activity but with shared target data
+    --DebugPrint(squadup)
+    squadSightLink = HasTag(squadSettings,"sightlink") --if true then it receives sighting information from other units
+    regTargetChange = squadreg..".targetchange" --squad alternative to choosePatrolTarget
+    regHeard = squadreg..".detect" --report sightings or sounds to this bool
+    regSighted = squadreg..".sighted" --report sightings to this bool
+    regSightLink = squadreg..".sightlink" --for communication with squad script
+    regDetectPos = squadreg..".detectpos" --report the location of the sighting or sound to this string registry
+    regDetectLink = squadreg..".detectlink" --respond to sounds others heard
+    regAttackCount = squadreg..".attackcount"
+
+    active = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not active then return end
+        local selflist = FindBodies("flyerfp")
+        --ai sight
+        playerSeen = false
+        playerTracked = false
+        lightR,lightG,lightB = idleLightR,idleLightG,idleLightB
+        SetLightColor(lightSpot,lightR,lightG,lightB)
+
+        sightMeter(dt)
+        isPlayerSeen()
+
+        playerTracking()
+        if squadup then squadSight() end
+
+        --ai hearing
+        hearSound()
+
+        --navigation
+        newPatrolPoint()
+
+        --DebugLine(targetPos,VecAdd(targetPos,Vec(0,1,0)))
+
+        --movement
+        hoverMovement(dt)
+
+        --aBOIDance (crude)
+        rejectSelf()
+        local hit, p, n, s = QueryClosestPoint(hrafnTargetPos,4)
+        local p2 = hrafnTargetPos[2] - p[2]
+        if HasTag(GetShapeBody(s),"flyerfp") then --yay for my trademarked tag
+        	if hit and p2 < 1 and p2 > -1 then
+        		local dir = VecSub(hrafnTransform.pos,p)
+        		--DebugLine(hrafnTransform.pos,p)
+        		--dir[2] = 0
+        		dir = VecNormalize(dir)
+        		hrafnTargetPos = VecAdd(hrafnTargetPos,VecScale(dir,7))
+        	end
+        end
+
+        --closeInStyle movement
+        if closeInStyle then
+        	closeInMovement(dt)
+        end
+        --timers
+        timeSince(dt)
+
+        --repositioning hoverPos
+        hoverReposition()
+
+        --height control
+        computeSurroundingHeight(7)
+        computeSurroundingHeight(7,height)
+        computeSurroundingHeight(13,0,hrafnTransform.pos)
+        computeSurroundingHeight(13,0,hrafnTransform.pos)
+        computeSurroundingHeight(3.8,height)
+        computeSurroundingHeight(3.8,height,hrafnTransform.pos)
+
+        heightControl()
+
+        --rotate body
+        hrafnTargetRot = QuatLookAt(hrafnTransform.pos,lookPos)
+        local coreEulerX, coreEulerY, coreEulerZ = GetQuatEuler(hrafnTargetRot) --break quat into euler
+        coreEulerX = clamp(coreEulerX,-10,10) --limit pitch
+        hrafnTargetRot = QuatEuler(coreEulerX,coreEulerY,coreEulerZ) --rebuild quat with modified pitch
+
+        --searchlight control 
+        local aimPos = VecCopy(lookPos)
+        local radius = clamp(timeSinceLastSeen,0,7)
+        if not lookaimAngle then lookaimAngle = 0; lookaimAngleY= 0 end --sorry for needing two aimangles cause i don't want leaks later
+        lookaimAngle = lookaimAngle%360 + dt
+        lookaimAngleY = lookaimAngleY%360 + dt*1.7 --one day I can make the look pattern more easily modifiable element
+        local x = math.cos(lookaimAngle) * radius
+        local z = math.sin(lookaimAngleY) * radius
+        aimPos = VecAdd(aimPos, Vec(x, 0, z))
+        --DebugCross(aimPos)
+
+        local lightTransform = TransformToParentTransform(hrafnTransform,searchLightLocalTransform)
+        searchLightTargetRot = QuatLookAt(lightTransform.pos,aimPos)
+        lightTransform.rot = searchLightRot
+
+        --set transforms
+        SetBodyTransform(hrafn,hrafnTransform)
+        SetBodyTransform(searchLight,lightTransform)
+
+        forceStatic()
+
+        --render custom glare
+        rejectSelf()
+        local glareTrans = Transform(GetBodyTransform(searchLight).pos,GetCameraTransform().rot)
+        local glaredir = VecSub(GetCameraTransform().pos,GetBodyTransform(searchLight).pos)
+        local glaredist = VecLength(glaredir)
+        glaredir = VecNormalize(glaredir)
+        local glareBlocked = QueryRaycast(GetBodyTransform(searchLight).pos,glaredir,math.min(glaredist,cGMaxDist))
+        if not glareBlocked and glaredist < cGMaxDist then
+        	local radi = 1-clamp(glaredist-cGMidPoint,0,cGMaxDist-cGMidPoint)/(cGMaxDist-cGMidPoint)
+        	radi = radi*cGRadius
+        	DrawSprite(customGlare,glareTrans,radi,radi,lightR,lightG,lightB,1,false,true)
+        	DrawSprite(customGlare,glareTrans,radi,radi,1,1,1,0.25,false,true)
+        end
+
+        --weapon system tick
+        activeWeaponCount = 0
+        if not weaponActive and not playerDead() then --which weapons to use for the attack unless you died
+        	local shouldFire = false
+        	if squadup then
+        		if squadSightLink and GetBool(regSightLink) then
+        			if blindFireable or not blindFireable and canSeePlayer() then
+        				shouldFire = true
+        			end
+        		end
+        	end
+        	if playerTracked then shouldFire = true end
+        	if shouldFire and getDistanceToPlayer() < 41 then
+        		local activated = false
+        		if hasAutoCannon and math.random() < .5 then
+        			autoCannonReady = true
+        			autoCannonFireDelay = 1 +(math.random()-0.5)*0.5
+        			autoCannonShotCount = math.random(autoCannonShotCounter[1],autoCannonShotCounter[2])
+        			--PlaySound(weaponChargeSound,hrafnTransform.pos,3,false)
+        			activated = true
+        		end
+        		if hasLaser and math.random() <0.5 then
+        			laserTimer = laserTime 
+        			laserDelay = 1 +(math.random()-0.5)*0.5
+        			laserReady = true
+        			--PlaySound(weaponChargeSound,hrafnTransform.pos,2,false)
+        			activated = true
+        		end
+        		if activated then attackCount = attackCount + 1 end
+        		if squadup and activated then
+        			SetFloat(regAttackCount, GetFloat(regAttackCount)+1, true)
+        			attackCount = GetFloat(regAttackCount)
+        		end
+        	end
+        end
+        if hasAutoCannon then tickAutoCannon(dt) end
+        if hasLaser then tickLaser(dt) end
+        if activeWeaponCount ~= 0 then weaponActive = true else weaponActive = false end
+        if hasRocket then
+        	if playerTracked or squadup and squadSightLink and GetBool(regSightLink) then considerRocket() end
+        	if not playerTracked or squadup and squadSightLink and not GetBool(regSightLink) then
+        		if rocketTimer ~= 0 then
+        			rocketTimer = math.max(0,rocketTimer - dt)
+        			if rocketTimer <= 0 then
+        				rocketLaunch()
+        				considerRocketReload()
+        			end
+        		end
+        	end
+        end
+
+        --shield status
+        if shieldsEnabled then--run shield routine here if has shields
+        	tickShields(dt)
+        end
+
+        if IsShapeBroken(core) or GetShapeBody(core) ~= corebody then --ded
+        	active = false
+        	local self = selflist --thanks convenient tag i made
+        	for s, p in ipairs(self) do
+        		--remove unbreakability from all shapes
+        		local shapes = GetBodyShapes(p)
+        		for s, shp in ipairs(shapes) do
+        			RemoveTag(shp,"unbreakable")
+        		end
+
+        		SetBodyDynamic(p, true)
+        		RemoveTag(p,"flyerfp") --cause its dead n all
+        		SetBodyVelocity(p,hrafnVel)
+        	end
+        	--PlaySound(dieSound, hrafnTransform.pos, 13,false)
+        	MakeHole(GetBodyTransform(searchLight).pos,0.1,0.1,0.1)
+        end
+
+        for key, shell in ipairs(autoCannonShellHandler.shells) do --operation of autocannon shots in tickspace
+        	if shell.active then 
+        		autoCannonShellOperation(shell)
+        	end
+        end
+        for key, rocket in ipairs(rocketHandler.rockets) do --operation of autocannon shots in tickspace
+        	if rocket.active then 
+        		rocketOperation(rocket)
+        	end
+        end	
+    end
+end
+
+function client.init()
+    heardSound = LoadSound("robot/alert.ogg")
+    heardSound = LoadSound("snd/alertclicking.ogg")
+    shieldBreakSound = LoadSound("alarm3-loop.ogg")
+    shieldBreakSound2 = LoadSound("alarm1.ogg")
+    shieldPop = LoadSound("light/spark2.ogg")
+    dieSound = LoadSound("robot/disable0.ogg")
+    weaponChargeSound = LoadSound("MOD/snd/plasma.ogg", 20.0)
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if not active then return end
+
+       tipPos = TransformToParentPoint(GetBodyTransform(corebody), Vec(6.3, -0.3, -1.2))
+       tipPos2 = TransformToParentPoint(GetBodyTransform(corebody), Vec(-6.3, -0.3, -1.2))	
+
+    --smooth movement
+    local acc = VecSub(hrafnTargetPos,hrafnTransform.pos)
+    hrafnVel = VecAdd(hrafnVel,VecScale(acc,dt*1.5))
+    hrafnVel = VecScale(hrafnVel,0.98) --drag factor, 0 for immobilize, 1 for NO DRAG
+    hrafnTransform.pos = VecAdd(hrafnTransform.pos,VecScale(hrafnVel,dt))
+    --smooth rotation
+    hrafnTransform.rot = QuatSlerp(hrafnTransform.rot,hrafnTargetRot,0.008)
+
+    --searchlight control
+    searchLightRot = QuatSlerp(searchLightRot, searchLightTargetRot, 0.13)
+
+    ParticleReset()
+    ParticleType("smoke")
+    ParticleTile(5)
+    ParticleColor(0.95, 0.9, 1)
+    ParticleRadius(0.7, 0)
+    ParticleStretch(2, 20)
+    ParticleAlpha(0.7, 0.0)
+    ParticleDrag(0)
+    ParticleCollide(0)
+    ParticleGravity(-400)
+    ParticleSticky(0.0, 0.0)
+
+       for i=1,5 do 					
+    	 SpawnParticle(tipPos, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
+    	 SpawnParticle(tipPos2, Vec(rnd(-0,0), rnd(-0,0), rnd(-0,0)), 0.15)
+    end	
+end
+

```

---

# Migration Report: hrafn\hrafnscripts\aiscripts.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafnscripts\aiscripts.lua
+++ patched/hrafn\hrafnscripts\aiscripts.lua
@@ -1,4 +1,4 @@
---shields 
+#version 2
 function initShields()
 	shieldLights = FindShapes("shieldlight") --shield, for convenience i make them glow
 	for s, shap in ipairs(shieldLights) do
@@ -6,7 +6,7 @@
 		shieldLights[s].body = GetShapeBody(shap)
 	end
 	shieldBreakTime = 0
-	if #shieldLights > 0 then shielded = true; shieldBreakTime = 0.44 end
+	if #shieldLights ~= 0 then shielded = true; shieldBreakTime = 0.44 end
 end
 
 function initSearchLightColors()
@@ -31,7 +31,7 @@
 function choosePatrolTarget() --change targetPos
 	local dir = VecNormalize(Vec(rndFloat(-1,1), 0, rndFloat(-1,1)))
 	local r = math.random(minPatrolRadius,maxPatrolRadius)
-	targetPos = VecAdd(GetPlayerPos(), VecScale(dir, r))
+	targetPos = VecAdd(GetPlayerPos(playerId), VecScale(dir, r))
 end
 
 function computeSurroundingHeight(radius, exheight,controlpoint) --control radius, extra height to give, and where to base probe from
@@ -54,7 +54,7 @@
 end
 
 function canSeePlayer()
-	local playerPos = GetPlayerCameraTransform().pos
+	local playerPos = GetPlayerCameraTransform(playerId).pos
 	--direction to player
 	local lightPos = GetBodyTransform(searchLight).pos
 	local dir = VecSub (playerPos, lightPos)
@@ -62,21 +62,20 @@
 	dir = VecNormalize(dir)
 	
 	rejectSelf()
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	return not QueryRaycast(lightPos, dir, dist, 0, true)
 
 end
 
 function playerDead()
-	if GetPlayerHealth() <= 0 then
+	if GetPlayerHealth(playerId) <= 0 then
 		return true
 	end
 	return false
 end
 
---tickspace
 function sightMeter(dt) --playerSeeMeter
-	if canSeePlayer() and IsPointAffectedByLight(lightSpot,GetPlayerCameraTransform().pos) then --you are spotted by the spotlight
+	if canSeePlayer() and IsPointAffectedByLight(lightSpot,GetPlayerCameraTransform(playerId).pos) then --you are spotted by the spotlight
 		playerSeen = true
 		playerSeeMeter = math.min(2,playerSeeMeter+dt*2) --getting seen increases seen meter
 	else
@@ -95,20 +94,20 @@
 function isPlayerSeen()
 	if playerSeen then
 		timeSinceLastSeen = 0
-		lookPos = GetPlayerPos()
+		lookPos = GetPlayerPos(playerId)
 	elseif not playerSeen and timeSinceLastSeen < 1 then--emulate motion estimation
-		lookPos = GetPlayerPos()
+		lookPos = GetPlayerPos(playerId)
 		if playerTracked then 
-			targetPos = GetPlayerPos() 
+			targetPos = GetPlayerPos(playerId) 
 			if squadup then 
-				SetString(regDetectPos,string.format("%f,%f,%f",targetPos[1],targetPos[2],targetPos[3])) --write targetpos to registry
+				SetString(regDetectPos,string.format("%f,%f,%f",targetPos[1],targetPos[2],targetPos[3]), true) --write targetpos to registry
 			end
 		end
 	end	
 end
 
 function getDistanceToPlayer()
-	local playerPos = GetPlayerPos()
+	local playerPos = GetPlayerPos(playerId)
 	return VecDist(playerPos, hrafnTransform.pos)
 end
 
@@ -117,16 +116,17 @@
 		timeSinceChoosePatrol = 0
 		timeSinceDistraction =0
 		if closeInStyle then timeToReposition = 0 end --force reposition timer to 0 if tracking player in closein mode
-		if playerSeen then targetPos = GetPlayerPos() end
+		if playerSeen then targetPos = GetPlayerPos(playerId) end
 		
 		if squadup then
-			SetBool(regSighted,true)
+			SetBool(regSighted,true, true)
 			if playerSeen then 
-				SetString(regDetectPos,string.format("%f,%f,%f",targetPos[1],targetPos[2],targetPos[3])) --report player target pos to reg
-			end
-		end
-	end
-end
+				SetString(regDetectPos,string.format("%f,%f,%f",targetPos[1],targetPos[2],targetPos[3]), true) --report player target pos to reg
+			end
+		end
+	end
+end
+
 function timeSince(dt) --last seen, patrol change, reposition, etc
 	if not playerSeen then
 		timeSinceLastSeen = math.min(timeSinceLastSeen + dt,1000) --math.min to prevent overflow
@@ -164,8 +164,8 @@
 				lookPos = VecCopy(targetPos)
 				repositionPoint()
 				if squadup then 
-					SetBool(regHeard, true) 
-					SetString(regDetectPos,string.format("%f,%f,%f",pos[1],pos[2],pos[3]))
+					SetBool(regHeard, true, true) 
+					SetString(regDetectPos,string.format("%f,%f,%f",pos[1],pos[2],pos[3]), true)
 				end
 				timeSinceChoosePatrol = 0
 				timeSinceDistraction = 0
@@ -185,7 +185,6 @@
 	end
 end
 
---navigation tickspace
 function newPatrolPoint()
 	local exceedtime = timeSinceChoosePatrol > maxPatrolTime
 	if exceedtime and not squadup or exceedtime and squadup and noSwarm then --this statement if no squad or swarm flying is disabled
@@ -211,7 +210,6 @@
 	end
 end
 
-	--movement tickspace
 function hoverMovement(dt)	
 	local toHover = VecSub(hoverPos,hrafnTargetPos)
 	toHover[2] = 0
@@ -248,7 +246,7 @@
 function hoverReposition()
 	if timeToReposition > repositionTime then
 		repositionPoint()
-		targetPos[2] = GetPlayerPos()[2]
+		targetPos[2] = GetPlayerPos(playerId)[2]
 		
 		--choosing look point, dependant on squad or not
 		if not weaponActive then
@@ -269,7 +267,6 @@
 	end
 end
 
---shield tick
 function tickShields(dt)
 	for s,shield in ipairs(shieldLights) do
 		if IsShapeBroken(shield.shape) or not IsHandleValid(shield.shape) or GetShapeBody(shield.shape) ~= shield.body then 
@@ -301,4 +298,5 @@
 		PointLight(hrafnTransform.pos,1,0.66,0.1,(shieldBreakTime/0.44)*52) --AUGH SHIELDS ARE DOWN
 		shieldBreakTime = math.max(shieldBreakTime-dt,0)--how long the shield break light lasts
 	end
-end+end
+

```

---

# Migration Report: hrafn\hrafnscripts\bodyscripts.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafnscripts\bodyscripts.lua
+++ patched/hrafn\hrafnscripts\bodyscripts.lua
@@ -1,3 +1,4 @@
+#version 2
 function initBodies()
 	hrafn = FindBody("hrafn")
 	hrafnTransform = GetBodyTransform(hrafn)
@@ -12,4 +13,5 @@
 	searchLightLocalTransform = TransformToLocalTransform(hrafnTransform,searchLightTransform)
 	searchLightRot = QuatEuler()
 	searchLightTargetRot = QuatEuler()
-end+end
+

```

---

# Migration Report: hrafn\hrafnscripts\flightscripts.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafnscripts\flightscripts.lua
+++ patched/hrafn\hrafnscripts\flightscripts.lua
@@ -1,3 +1,4 @@
+#version 2
 function computeSurroundingHeight(radius, exheight,controlpoint) --control radius, extra height to give, and where to base probe from
 	radius = radius or 10
 	exheight = exheight or 0

```

---

# Migration Report: hrafn\hrafnscripts\utilities.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafnscripts\utilities.lua
+++ patched/hrafn\hrafnscripts\utilities.lua
@@ -1,3 +1,4 @@
+#version 2
 function rndFloat(mi, ma)
 	return mi + (ma-mi)*(math.random(0, 1000000)/1000000.0)
 end
@@ -12,7 +13,8 @@
 		value = tonumber(value)
 	end
 	return tag
-end 
+end
+
 function commasplit(inputstr) --splits a "x,x,x..." string into a table
 	local t = {}
 	for str in string.gmatch(inputstr,"([^,]+)") do
@@ -99,3 +101,4 @@
     local nearest = VecAdd(nearest, p0)
     return dist, nearest
 end
+

```

---

# Migration Report: hrafn\hrafnscripts\weaponscripts.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafnscripts\weaponscripts.lua
+++ patched/hrafn\hrafnscripts\weaponscripts.lua
@@ -1,15 +1,4 @@
-autoCannonShellHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false}
-} --for secondary autocannon
-
-rocketHandler = {
-	rocketNum = 1,
-	rockets = {},
-	defaultRocket = {active = false}
-} --for rockets
-
+#version 2
 function initAutoCannon()
 	autoCannonSettings = FindLocation("autocannonsettings")
 	autoCannonSound = LoadSound("MOD/snd/plasma.ogg", 20.0)
@@ -66,7 +55,6 @@
 	laserReady = false
 end
 
---autocannon
 function autoCannonFire()
 	local origin = TransformToParentTransform(hrafnTransform,autoCannonLocalMuzzle) --should be the unmoving muzzle of the drone
 	origin.rot = QuatLookAt(origin.pos,lookPos)
@@ -108,23 +96,23 @@
 	
 	--check player for damage
 	local hitPlayer = false --will it hit you?
-	local ppos = GetPlayerPos()
+	local ppos = GetPlayerPos(playerId)
 	ppos[2] = ppos[2]-0.5
 	local pdist,phit = getDistanceToLineSegment(ppos,shell.pos,ahead)
 	if pdist < 0.6 then
 		hitPlayer = true
 	end
-	ppos = GetPlayerCameraTransform().pos
+	ppos = GetPlayerCameraTransform(playerId).pos
 	ppos[2] = ppos[2] - 0.7 --now 1.2 m height
 	local pdist,phit = getDistanceToLineSegment(ppos,shell.pos,ahead)
 	if pdist < 0.6 then
 		hitPlayer = true
 	end
 	if hitPlayer then
-		local health = GetPlayerHealth()
+		local health = GetPlayerHealth(playerId)
 		health = health - 0.1
 		--health = math.max(0.1,health - 0.1)
-		SetPlayerHealth(health)
+		SetPlayerHealth(playerId, health)
 	end
 	
 	if squadup then rejectAll() else rejectSelf() end --disable friendly fire
@@ -270,6 +258,7 @@
 		shell.active = false
 	end
 end
+
 function tickAutoCannon(dt)
 	if autoCannonReady then activeWeaponCount = activeWeaponCount+1 end --weapon is operating
 	if playerDead() then
@@ -278,11 +267,11 @@
 		-- return 
 	end
 	if autoCannonReady then
-		if autoCannonFireDelay > 0 then
+		if autoCannonFireDelay ~= 0 then
 			autoCannonFireDelay = math.max(0,autoCannonFireDelay - dt) --stop function here if delayed
 			return
 		end
-		if autoCannonShotCount > 0 then
+		if autoCannonShotCount ~= 0 then
 			autoCannonFire()
 			autoCannonFireDelay = autoCannonFR+ math.random()*0.1
 			autoCannonShotCount = autoCannonShotCount - 1
@@ -292,7 +281,6 @@
 	end
 end
 
---laser 
 function laser()
 	local origin = TransformToParentTransform(hrafnTransform,laserPoint) --should be the unmoving muzzle of the drone
 	origin.rot = laserRot
@@ -322,27 +310,28 @@
 	PlayLoop(laserHitLoop,hitPos,6,false)
 	--check player for damage
 	local hitPlayer = false --will it hit you?
-	local ppos = GetPlayerPos()
+	local ppos = GetPlayerPos(playerId)
 	ppos[2] = ppos[2]-0.5
 	local pdist,phit = getDistanceToLineSegment(ppos,origin.pos,hitPos)
 	PlayLoop(laserLoop,phit,4,false)
 	if pdist < 0.7 then
 		hitPlayer = true
 	end
-	ppos = GetPlayerCameraTransform().pos
+	ppos = GetPlayerCameraTransform(playerId).pos
 	ppos[2] = ppos[2] - 0.7 --now 1.2 m height
 	local pdist,phit = getDistanceToLineSegment(ppos,origin.pos,hitPos)
 	if pdist < 0.7 then
 		hitPlayer = true
 	end
 	if hitPlayer then
-		PlaySound(laserHitPlayer,GetPlayerPos(),0.6,false)
-		local health = GetPlayerHealth()
+		PlaySound(laserHitPlayer,GetPlayerPos(playerId),0.6,false)
+		local health = GetPlayerHealth(playerId)
 		health = health - 0.005
 		--health = math.max(0.1,health - 0.1)
-		SetPlayerHealth(health)
-	end
-end
+		SetPlayerHealth(playerId, health)
+	end
+end
+
 function laserParticle()
 	ParticleReset()
 	ParticleTile(3)
@@ -351,6 +340,7 @@
 	ParticleCollide(0)
 	ParticleSticky(0)
 end
+
 function tickLaser(dt)
 	laserTargetRot = QuatLookAt(TransformToParentPoint(hrafnTransform,laserPoint.pos),lookPos)
 	laserRot = QuatSlerp(laserRot,laserTargetRot,0.33)
@@ -362,11 +352,11 @@
 		-- return 
 	end
 	if laserReady then
-		if laserDelay > 0 then
+		if laserDelay ~= 0 then
 			laserDelay = math.max(0,laserDelay - dt) --stop function here if delayed
 			return
 		end
-		if laserTimer > 0 then
+		if laserTimer ~= 0 then
 			laser()
 			laserTimer = math.max(0,laserTimer - dt)
 		else
@@ -382,6 +372,7 @@
 		rocketTimer = 0
 	end
 end
+
 function considerRocketReload()
 	if math.random() < 0.78 then
 		rocketTimer = 0.1 + math.random()*0.1
@@ -389,6 +380,7 @@
 		rocketTimer = 0
 	end
 end
+
 function rocketLaunch()
 	local origin = TransformToParentTransform(hrafnTransform,rocketLaunchLocalPoint)
 	origin.rot = QuatLookAt(origin.pos,targetPos)
@@ -406,6 +398,7 @@
 	
 	PlaySound(rocketSound, origin.pos, 5, false)
 end
+
 function rocketOperation(rocket)
 	local ahead = VecAdd(rocket.pos,VecScale(rocket.vel,GetTimeStep()))
 	local dir = VecNormalize(rocket.vel)
@@ -442,4 +435,5 @@
 		rocket.active = false
 		Explosion(rocket.pos,dmg)
 	end
-end+end
+

```

---

# Migration Report: hrafn\hrafnscripts\weaponscripts2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\hrafnscripts\weaponscripts2.lua
+++ patched/hrafn\hrafnscripts\weaponscripts2.lua
@@ -1,15 +1,4 @@
-autoCannonShellHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false}
-} --for secondary autocannon
-
-rocketHandler = {
-	rocketNum = 1,
-	rockets = {},
-	defaultRocket = {active = false}
-} --for rockets
-
+#version 2
 function initAutoCannon()
 	autoCannonSettings = FindLocation("autocannonsettings")
 	autoCannonSound = LoadSound("MOD/snd/plasma.ogg", 40.0)
@@ -66,7 +55,6 @@
 	laserReady = false
 end
 
---autocannon
 function autoCannonFire()
 	local origin = TransformToParentTransform(hrafnTransform,autoCannonLocalMuzzle) --should be the unmoving muzzle of the drone
 	origin.rot = QuatLookAt(origin.pos,lookPos)
@@ -108,23 +96,23 @@
 	
 	--check player for damage
 	local hitPlayer = false --will it hit you?
-	local ppos = GetPlayerPos()
+	local ppos = GetPlayerPos(playerId)
 	ppos[2] = ppos[2]-0.5
 	local pdist,phit = getDistanceToLineSegment(ppos,shell.pos,ahead)
 	if pdist < 0.6 then
 		hitPlayer = true
 	end
-	ppos = GetPlayerCameraTransform().pos
+	ppos = GetPlayerCameraTransform(playerId).pos
 	ppos[2] = ppos[2] - 0.7 --now 1.2 m height
 	local pdist,phit = getDistanceToLineSegment(ppos,shell.pos,ahead)
 	if pdist < 0.6 then
 		hitPlayer = true
 	end
 	if hitPlayer then
-		local health = GetPlayerHealth()
+		local health = GetPlayerHealth(playerId)
 		health = health - 0.1
 		--health = math.max(0.1,health - 0.1)
-		SetPlayerHealth(health)
+		SetPlayerHealth(playerId, health)
 	end
 	
 	if squadup then rejectAll() else rejectSelf() end --disable friendly fire
@@ -270,6 +258,7 @@
 		shell.active = false
 	end
 end
+
 function tickAutoCannon(dt)
 	if autoCannonReady then activeWeaponCount = activeWeaponCount+1 end --weapon is operating
 	if playerDead() then
@@ -278,11 +267,11 @@
 		-- return 
 	end
 	if autoCannonReady then
-		if autoCannonFireDelay > 0 then
+		if autoCannonFireDelay ~= 0 then
 			autoCannonFireDelay = math.max(0,autoCannonFireDelay - dt) --stop function here if delayed
 			return
 		end
-		if autoCannonShotCount > 0 then
+		if autoCannonShotCount ~= 0 then
 			autoCannonFire()
 			autoCannonFireDelay = autoCannonFR+ math.random()*0.1
 			autoCannonShotCount = autoCannonShotCount - 1
@@ -292,7 +281,6 @@
 	end
 end
 
---laser 
 function laser()
 	local origin = TransformToParentTransform(hrafnTransform,laserPoint) --should be the unmoving muzzle of the drone
 	origin.rot = laserRot
@@ -322,27 +310,28 @@
 	PlayLoop(laserHitLoop,hitPos,6,false)
 	--check player for damage
 	local hitPlayer = false --will it hit you?
-	local ppos = GetPlayerPos()
+	local ppos = GetPlayerPos(playerId)
 	ppos[2] = ppos[2]-0.5
 	local pdist,phit = getDistanceToLineSegment(ppos,origin.pos,hitPos)
 	PlayLoop(laserLoop,phit,4,false)
 	if pdist < 0.7 then
 		hitPlayer = true
 	end
-	ppos = GetPlayerCameraTransform().pos
+	ppos = GetPlayerCameraTransform(playerId).pos
 	ppos[2] = ppos[2] - 0.7 --now 1.2 m height
 	local pdist,phit = getDistanceToLineSegment(ppos,origin.pos,hitPos)
 	if pdist < 0.7 then
 		hitPlayer = true
 	end
 	if hitPlayer then
-		PlaySound(laserHitPlayer,GetPlayerPos(),0.6,false)
-		local health = GetPlayerHealth()
+		PlaySound(laserHitPlayer,GetPlayerPos(playerId),0.6,false)
+		local health = GetPlayerHealth(playerId)
 		health = health - 0.005
 		--health = math.max(0.1,health - 0.1)
-		SetPlayerHealth(health)
-	end
-end
+		SetPlayerHealth(playerId, health)
+	end
+end
+
 function laserParticle()
 	ParticleReset()
 	ParticleTile(3)
@@ -351,6 +340,7 @@
 	ParticleCollide(0)
 	ParticleSticky(0)
 end
+
 function tickLaser(dt)
 	laserTargetRot = QuatLookAt(TransformToParentPoint(hrafnTransform,laserPoint.pos),lookPos)
 	laserRot = QuatSlerp(laserRot,laserTargetRot,0.33)
@@ -362,11 +352,11 @@
 		-- return 
 	end
 	if laserReady then
-		if laserDelay > 0 then
+		if laserDelay ~= 0 then
 			laserDelay = math.max(0,laserDelay - dt) --stop function here if delayed
 			return
 		end
-		if laserTimer > 0 then
+		if laserTimer ~= 0 then
 			laser()
 			laserTimer = math.max(0,laserTimer - dt)
 		else
@@ -382,6 +372,7 @@
 		rocketTimer = 0
 	end
 end
+
 function considerRocketReload()
 	if math.random() < 0.78 then
 		rocketTimer = 0.1 + math.random()*0.1
@@ -389,6 +380,7 @@
 		rocketTimer = 0
 	end
 end
+
 function rocketLaunch()
 	local origin = TransformToParentTransform(hrafnTransform,rocketLaunchLocalPoint)
 	origin.rot = QuatLookAt(origin.pos,targetPos)
@@ -406,6 +398,7 @@
 	
 	PlaySound(rocketSound, origin.pos, 5, false)
 end
+
 function rocketOperation(rocket)
 	local ahead = VecAdd(rocket.pos,VecScale(rocket.vel,GetTimeStep()))
 	local dir = VecNormalize(rocket.vel)
@@ -442,4 +435,5 @@
 		rocket.active = false
 		Explosion(rocket.pos,dmg)
 	end
-end+end
+

```

---

# Migration Report: hrafn\laser.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/hrafn\laser.lua
+++ patched/hrafn\laser.lua
@@ -1,34 +1,11 @@
-MAX_DIST = 1000
-DONE_TIMER = 2.0
-BURN_TIME = 25
-PLAYER_HIT_RADIUS = 0.4
-
+#version 2
 function rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
 
 function rndVec(t)
 	return Vec(rnd(-t, t), rnd(-t, t), rnd(-t, t))
-end 
-
-function init()
-	buttonShape = FindShape("button")
-	emitterShape = FindShape("emitter")
-	emitterLocation = FindLocation("emitter")
-	vaultDoors = FindBodies("vaultdoor", true)
-	
-	laserLoop = LoadLoop("laser-loop.ogg")
-	laserHitLoop = LoadLoop("laser-hit-loop.ogg")
-	laserHitSound = LoadSound("light/spark0.ogg")
-	laserDist = 0
-	laserHitScale = 0
-	
-	laserSprite = LoadSprite("gfx/laser.png")
-
-	disableTimer = 0
-	setEnabled(false)
 end
-
 
 function setEnabled(e)
 	enabled = e
@@ -40,7 +17,6 @@
 		SetTag(buttonShape, "interact", "Turn on")
 	end
 end
-
 
 function emitSmoke(pos, amount)
 	ParticleReset()
@@ -62,7 +38,6 @@
 	SpawnParticle(pos, vel, rnd(1.0, 2.0))
 end
 
-
 function getDistanceToLineSegment(point, p0, p1)
     local line_vec = VecSub(p1, p0)
     local pnt_vec = VecSub(point, p0)
@@ -80,7 +55,6 @@
     local nearest = VecAdd(nearest, p0)
     return dist, nearest
 end
-
 
 function shootLaser(body, shape, origin, dir, currentLength)
 	--Raycast
@@ -106,14 +80,14 @@
 	DrawSprite(laserSprite, t, length, 0.5, 1.0, 0.3, 0.3, 1, true, true)
 
 	--Check if player if hit by laser
-	local ppos = GetPlayerCameraTransform().pos
+	local ppos = GetPlayerCameraTransform(playerId).pos
 	ppos[2] = ppos[2] - PLAYER_HIT_RADIUS*0.5
 	local pdist, phit = getDistanceToLineSegment(ppos, origin, hitPoint)
 	if pdist < PLAYER_HIT_RADIUS then
 		--Decrease health but don't kill
-		local health = GetPlayerHealth()
+		local health = GetPlayerHealth(playerId)
 		health = math.max(0.1, health - 0.3)
-		SetPlayerHealth(health)
+		SetPlayerHealth(playerId, health)
 		ReleasePlayerGrab()
 		
 		--Disance to player, without vertical component
@@ -122,10 +96,10 @@
 		pdir = VecNormalize(pdir)
 
 		--Move player and give a nudge
-		local pt = GetPlayerTransform(true)
+		local pt = GetPlayerTransform(playerId, true)
 		pt.pos = VecAdd(pt.pos, VecScale(pdir, PLAYER_HIT_RADIUS-pdist+0.1))
-		SetPlayerTransform(pt, true)
-		SetPlayerVelocity(VecScale(pdir, 10))
+		SetPlayerTransform(playerId, pt, true)
+		SetPlayerVelocity(playerId, VecScale(pdir, 10))
 
 		--Play hit sound
 		PlaySound(laserHitSound, ppos)
@@ -140,45 +114,67 @@
 	return currentLength + length, hitPoint, hitBody, hitShape
 end
 
-function tick(dt)
-	if GetPlayerInteractShape() == buttonShape and InputPressed("interact") then
-		setEnabled(not enabled)
-	end
-	
-	if enabled then
-		local emitTransform = GetLocationTransform(emitterLocation)
-		local origin = emitTransform.pos
-		PlayLoop(laserLoop, origin, 0.5)
-		local dir = TransformToParentVec(emitTransform, Vec(0, 0, -1))
-		local length, hitPoint, hitBody, hitShape = shootLaser(0, emitterShape, origin, dir, 0)
-		if length ~= laserDist then
-			laserHitScale = 1
-			laserDist = length
-		end
-		laserHitScale = math.max(0.0, laserHitScale - dt)
-		if laserHitScale > 0 then
-			PlayLoop(laserHitLoop, endPoint, laserHitScale)
-			PointLight(hitPoint, 1, 0.2, 0.2, rnd(2.0, 4.0)*laserHitScale)
-		end
-		PointLight(hitPoint, 1, 0.2, 0.2, rnd(0.5, 1.0))
+function server.init()
+    buttonShape = FindShape("button")
+    emitterShape = FindShape("emitter")
+    emitterLocation = FindLocation("emitter")
+    vaultDoors = FindBodies("vaultdoor", true)
+    laserLoop = LoadLoop("laser-loop.ogg")
+    laserHitLoop = LoadLoop("laser-hit-loop.ogg")
+    laserDist = 0
+    laserHitScale = 0
+    laserSprite = LoadSprite("gfx/laser.png")
+    disableTimer = 0
+    setEnabled(false)
+end
 
-		for i = 1, #vaultDoors do
-			if hitBody == vaultDoors[i] then
-				RemoveTag(vaultDoors[i], "unbreakable")
-			end
-		end
-	
-		emitSmoke(hitPoint, 1.0)
-		MakeHole(hitPoint, 0.5, 0.3, 0, true)
-	end
-	
-	SetBool("level.laser", enabled)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetBool("level.laser", enabled, true)
+        if GetBool("level.vaultbroken") then
+        	disableTimer = disableTimer + dt
+        	if disableTimer > 3 then
+        		setEnabled(false)
+        		SetBool("level.vaultbroken", false, true)
+        	end
+        end
+    end
+end
 
-	if GetBool("level.vaultbroken") then
-		disableTimer = disableTimer + dt
-		if disableTimer > 3 then
-			setEnabled(false)
-			SetBool("level.vaultbroken", false)
-		end
-	end
+function client.init()
+    laserHitSound = LoadSound("light/spark0.ogg")
 end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == buttonShape and InputPressed("interact") then
+    	setEnabled(not enabled)
+    end
+    if enabled then
+    	local emitTransform = GetLocationTransform(emitterLocation)
+    	local origin = emitTransform.pos
+    	PlayLoop(laserLoop, origin, 0.5)
+    	local dir = TransformToParentVec(emitTransform, Vec(0, 0, -1))
+    	local length, hitPoint, hitBody, hitShape = shootLaser(0, emitterShape, origin, dir, 0)
+    	if length ~= laserDist then
+    		laserHitScale = 1
+    		laserDist = length
+    	end
+    	laserHitScale = math.max(0.0, laserHitScale - dt)
+    	if laserHitScale ~= 0 then
+    		PlayLoop(laserHitLoop, endPoint, laserHitScale)
+    		PointLight(hitPoint, 1, 0.2, 0.2, rnd(2.0, 4.0)*laserHitScale)
+    	end
+    	PointLight(hitPoint, 1, 0.2, 0.2, rnd(0.5, 1.0))
+
+    	for i = 1, #vaultDoors do
+    		if hitBody == vaultDoors[i] then
+    			RemoveTag(vaultDoors[i], "unbreakable")
+    		end
+    	end
+
+    	emitSmoke(hitPoint, 1.0)
+    	MakeHole(hitPoint, 0.5, 0.3, 0, true)
+    end
+end
+

```

---

# Migration Report: script\chopper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\chopper.lua
+++ patched/script\chopper.lua
@@ -1,17 +1,4 @@
-GroundProximityDetection = true
-
-config = {
-	["ah_64"] = {},
-	["mh_60"] = {},
-	["mi_17"] = {},
-	["mi_24"] = {weaponLoc = Vec(-0.05, 0.95, -9), music = "MOD/katyusha.ogg"},
-	["uh_1"] = {weaponLoc = Vec(0.0, -0.9, -3.3), music = "MOD/fortunate_son.ogg"},
-	["ka_50"] = {weaponLoc = Vec(0.85, 1.1, -3.9), music = "MOD/soviet_anthem.ogg", rotors = "coaxial"},
-	["av_8"] = {weaponLoc = Vec(-0.55, 0.65, -2.5)},
-	["mh_60medic"] = {},
-	["delorean"] = {}
-}
-
+#version 2
 function EulerQuat(q, k)
 	local x, y, z, w = q[1], q[2], q[3], q[4]
 	local bank, heading, attitude
@@ -51,7 +38,7 @@
 function sign(x)
 	if x < 0 then
 		return -1
-	elseif x > 0 then
+	elseif x ~= 0 then
 		return 1
 	else
 		return 0
@@ -74,252 +61,235 @@
 	return yaw
 end
 
-function init()
-	chopper = {}
-	chopper.body = FindBody("chopper")
-	chopper.transform = GetBodyTransform(chopper.body)
-	
-    leg1 = FindShape("target1")
-    leg2 = FindShape("target2")
-    leg3 = FindShape("target3")
-    leg4 = FindShape("target4")	
-
-	chopper.mainRotor = FindBody("mainrotor")
-	chopper.mainRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.mainRotor))
-	
-	chopper.mainRotor2 = FindBody("mainrotor2")
-	chopper.mainRotor2LocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.mainRotor2))
-
-	chopper.tailRotor = FindBody("tailrotor")
-	chopper.tailRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.tailRotor))
-
-	chopper.angle = 0.0
-	chopper.mass = GetBodyMass(chopper.body)
-	chopper.sound = LoadLoop("MOD/snd/jet.ogg", 20.0)
-
-	shootSound = LoadSound("MOD/snd/plasma.ogg", 10.0)
-	rocketSound = LoadSound("tools/launcher0.ogg")	
-
-	pitch = 0
-	yaw = 0
-	roll = 0
-	collective = chopper.transform.pos[2] + 0.5 -- Starting altitude
-
-	cameraX = 0
-	cameraY = 0
-	zoom = 25
-
-	vehicleType = GetTagValue(chopper.body, "chopper")
-	if config[vehicleType].music then
-		music = config[vehicleType].music
-	end
-	if not HasTag(chopper.body, "avf") and config[vehicleType].weaponLoc then
-		weaponLoc = config[vehicleType].weaponLoc
-	end
-	if HasTag(chopper.body, "avf") then
-		isAVF = true
-	end
-	isCoaxial = false
-	if config[vehicleType].rotors then
-		isCoaxial = true
-	end
-
-	playing = true -- Default: false
-	aimMode = false
-	hover = false
-	dynamicRotor = true
-end
-
-
-function tick(dt)
-	local vehicle = GetPlayerVehicle()
-	if vehicle ~= FindVehicle("helicopter") then
-		if not dynamicRotor then -- Player leaves the chopper
-			dynamicRotor = true
-			SetBodyDynamic(chopper.mainRotor, true)
-			SetBodyDynamic(chopper.mainRotor2, true)
-			SetBodyAngularVelocity(chopper.body, Vec())
-			SetPlayerVehicle(0)
-			pitch = 0
-			roll = 0
-			cameraY = pitch
-			local playerSpawn = TransformToParentPoint(chopper.transform, Vec(2, 0, -4))
-			local playerRot = QuatEuler(pitch, yaw, roll)
-			SetPlayerTransform(Transform(playerSpawn, playerRot))
-		end
-		return
-	elseif GetBodyMass(chopper.body) < chopper.mass * 0.66 then
-		if not dynamicRotor then -- Helicopter is too damaged
-			dynamicRotor = true
-			SetBodyDynamic(chopper.mainRotor, true)
-			SetBodyDynamic(chopper.mainRotor2, true)
-		end
-		return
-	else
-		if dynamicRotor then -- Player enter the chopper
-			dynamicRotor = false
-			SetBodyDynamic(chopper.mainRotor, false)
-			SetBodyDynamic(chopper.mainRotor2, false)
-			chopper.transform.pos = GetBodyTransform(chopper.body).pos -- Update chopper position
-			local unused = 0
-			unused, yaw = EulerQuat(GetBodyTransform(chopper.body).rot) -- Update yaw rotation
-			cameraX = yaw
-			collective = chopper.transform.pos[2] + 0.5
-			Delete(leg1)
-			Delete(leg2)
-			Delete(leg3)
-			Delete(leg4)
-		end
-		if music and not playing then
-			playing = true
-			PlayMusic(music)
-		end
-	end
-
-	if InputDown("space") then
-		collective = collective + 0.1
-	end
-	if InputDown("ctrl") and collective > 0 then
-		collective = collective - 0.1
-	end
-
-	if InputDown("a") and roll < 30 then
-		roll = roll + 0.5
-	end
-	if InputDown("d") and roll > -30 then
-		roll = roll - 0.5
-	end
-
-	if weaponLoc then
-		local firePos = TransformToParentPoint(chopper.transform, weaponLoc)
-		local fireDir = TransformToParentVec(chopper.transform, Vec(0, 0, -1))
-		if vehicleType == "mh_60" then
-			fireDir = VecNormalize(TransformToParentVec(chopper.transform, Vec(-2, -1, 0)))
-			if InputDown("lmb") then
-				PlaySound(shootSound, chopper.transform.pos, 10)
-				--PointLight(pos, 0.9, 0.1, 0.4, 90)
-				Shoot(firePos, fireDir, 0)
-			end
-		else
-			if InputPressed("lmb") then
-				PlaySound(shootSound, chopper.transform.pos, 5)
-				PointLight(firePos, 0.9, 0.1, 0.4, 90)
-				Shoot(firePos, fireDir, 0)
-			end
-			if InputPressed("rmb") then
-				PlaySound(rocketSound, chopper.transform.pos, 5)
-				--PointLight(pos, 0.9, 0.1, 0.4, 90)
-				Shoot(firePos, fireDir, 1)
-			end
-		end
-	elseif isAVF then
-		if InputPressed("rmb") then
-			aimMode = not aimMode
-		end
-	end
-	if InputPressed("h") then
-		hover = not hover
-	end
-
-	local prevYaw = yaw
-
-	if not aimMode then
-		local x, y = EulerQuat(GetCameraTransform().rot)
-
-		if x < pitch and pitch > -45 then
-			pitch = pitch - 0.5
-		end
-		if x > pitch and pitch < 15 then
-			pitch = pitch + 0.5
-		end
-
-		if y < yaw and not (y < yaw - 180) then
-			yaw = YawRight(yaw)
-		elseif y < yaw - 180 then
-			yaw = YawLeft(yaw)
-		end
-
-		if y > yaw and not (y > yaw + 180) then
-			yaw = YawLeft(yaw)
-		elseif y > yaw + 180 then
-			yaw = YawRight(yaw)
-		end
-	else
-		local mouseX = -InputValue("mousedx")
-		local mouseY = -InputValue("mousedy")
-
-		if sign(mouseY) < 0 and pitch > -45 then
-			pitch = pitch - 0.5
-		elseif sign(mouseY) > 0 and pitch < 15 then
-			pitch = pitch + 0.5
-		end
-
-		if sign(mouseX) < 0 then
-			yaw = YawRight(yaw)
-		elseif sign(mouseX) > 0 then
-			yaw = YawLeft(yaw)
-		end
-	end
-
-	if hover then
-		if pitch ~= 0 then
-			pitch = pitch - sign(pitch)
-		end
-		yaw = prevYaw
-	end
-
-	local moveDir = Vec(0.01 * -roll, 0, 0.01 * pitch)
-	local pos = TransformToParentPoint(chopper.transform, moveDir)
-
-	if GroundProximityDetection then
-		pos[2] = pos[2] - 0.1
-		local dir = VecNormalize(VecSub(pos, chopper.transform.pos))
-		local maxDist = 0.5 + math.abs(pitch / 5) + math.abs(roll / 10)
-		QueryRejectBody(chopper.body)
-		QueryRequire("physical large")
-		local hit, dist = QueryRaycast(chopper.transform.pos, dir, maxDist)
-		--local posEnd = VecAdd(chopper.transform.pos, VecScale(dir, maxDist))
-		if hit then
-			collective = collective + (maxDist - dist) / (2 * maxDist)
-		end
-	end
-	pos[2] = collective
-
-	chopper.angle = chopper.angle + 0.6
-	local rot = QuatEuler(math.sin(chopper.angle*0.053)*5 + pitch, math.sin(chopper.angle*0.04)*5 + yaw, roll)
-
-	if aimMode then
-		rot = QuatEuler(pitch, yaw, roll)
-	end
-
-	chopper.transform.pos = pos
-	chopper.transform.rot = rot
-	SetBodyTransform(chopper.body, chopper.transform)
-
-	chopper.mainRotorLocalTransform.rot = QuatEuler(0, chopper.angle * 57, 0)
-	SetBodyTransform(chopper.mainRotor, TransformToParentTransform(chopper.transform, chopper.mainRotorLocalTransform))
-	
-	chopper.mainRotor2LocalTransform.rot = QuatEuler(0, chopper.angle * 57, 0)
-	SetBodyTransform(chopper.mainRotor2, TransformToParentTransform(chopper.transform, chopper.mainRotor2LocalTransform))	
-
-	if isCoaxial then
-		chopper.tailRotorLocalTransform.rot = QuatEuler(0, -chopper.angle * 57, 0)
-	else
-		chopper.tailRotorLocalTransform.rot = QuatEuler(chopper.angle * 57, 0)
-	end
-	SetBodyTransform(chopper.tailRotor, TransformToParentTransform(chopper.transform, chopper.tailRotorLocalTransform))
-
-	PlayLoop(chopper.sound, chopper.transform.pos, 0.5)
-
-	local mx, my = InputValue("mousedx"), InputValue("mousedy")
-	cameraX = cameraX - mx / 10
-	cameraY = cameraY - my / 10
-	cameraY = clamp(cameraY, -90, 90)
-	local cameraRot = QuatEuler(cameraY, cameraX, 0)
-	local cameraT = Transform(chopper.transform.pos, cameraRot)
-	zoom = zoom - InputValue("mousewheel")
-	zoom = clamp(zoom, -3, 30)
-	local cameraPos = TransformToParentPoint(cameraT, Vec(0, 6, zoom))
-	local camera = Transform(cameraPos, cameraRot)
-	SetCameraTransform(camera)
-end
+function server.init()
+    chopper = {}
+    chopper.body = FindBody("chopper")
+    chopper.transform = GetBodyTransform(chopper.body)
+       leg1 = FindShape("target1")
+       leg2 = FindShape("target2")
+       leg3 = FindShape("target3")
+       leg4 = FindShape("target4")	
+    chopper.mainRotor = FindBody("mainrotor")
+    chopper.mainRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.mainRotor))
+    chopper.mainRotor2 = FindBody("mainrotor2")
+    chopper.mainRotor2LocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.mainRotor2))
+    chopper.tailRotor = FindBody("tailrotor")
+    chopper.tailRotorLocalTransform = TransformToLocalTransform(chopper.transform, GetBodyTransform(chopper.tailRotor))
+    chopper.angle = 0.0
+    chopper.mass = GetBodyMass(chopper.body)
+    chopper.sound = LoadLoop("MOD/snd/jet.ogg", 20.0)
+    pitch = 0
+    yaw = 0
+    roll = 0
+    collective = chopper.transform.pos[2] + 0.5 -- Starting altitude
+    cameraX = 0
+    cameraY = 0
+    zoom = 25
+    vehicleType = GetTagValue(chopper.body, "chopper")
+    if config[vehicleType].music then
+    	music = config[vehicleType].music
+    end
+    if not HasTag(chopper.body, "avf") and config[vehicleType].weaponLoc then
+    	weaponLoc = config[vehicleType].weaponLoc
+    end
+    if HasTag(chopper.body, "avf") then
+    	isAVF = true
+    end
+    isCoaxial = false
+    if config[vehicleType].rotors then
+    	isCoaxial = true
+    end
+    playing = true -- Default: false
+    aimMode = false
+    hover = false
+    dynamicRotor = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local vehicle = GetPlayerVehicle(playerId)
+        if vehicle ~= FindVehicle("helicopter") then
+        	if not dynamicRotor then -- Player leaves the chopper
+        		dynamicRotor = true
+        		SetBodyDynamic(chopper.mainRotor, true)
+        		SetBodyDynamic(chopper.mainRotor2, true)
+        		SetBodyAngularVelocity(chopper.body, Vec())
+        		SetPlayerVehicle(playerId, 0)
+        		pitch = 0
+        		roll = 0
+        		cameraY = pitch
+        		local playerSpawn = TransformToParentPoint(chopper.transform, Vec(2, 0, -4))
+        		local playerRot = QuatEuler(pitch, yaw, roll)
+        		SetPlayerTransform(playerId, Transform(playerSpawn, playerRot))
+        	end
+        	return
+        elseif GetBodyMass(chopper.body) < chopper.mass * 0.66 then
+        	if not dynamicRotor then -- Helicopter is too damaged
+        		dynamicRotor = true
+        		SetBodyDynamic(chopper.mainRotor, true)
+        		SetBodyDynamic(chopper.mainRotor2, true)
+        	end
+        	return
+        else
+        	if dynamicRotor then -- Player enter the chopper
+        		dynamicRotor = false
+        		SetBodyDynamic(chopper.mainRotor, false)
+        		SetBodyDynamic(chopper.mainRotor2, false)
+        		chopper.transform.pos = GetBodyTransform(chopper.body).pos -- Update chopper position
+        		local unused = 0
+        		unused, yaw = EulerQuat(GetBodyTransform(chopper.body).rot) -- Update yaw rotation
+        		cameraX = yaw
+        		collective = chopper.transform.pos[2] + 0.5
+        		Delete(leg1)
+        		Delete(leg2)
+        		Delete(leg3)
+        		Delete(leg4)
+        	end
+        	if music and not playing then
+        		playing = true
+        		PlayMusic(music)
+        	end
+        end
+        local prevYaw = yaw
+        if hover then
+        	if pitch ~= 0 then
+        		pitch = pitch - sign(pitch)
+        	end
+        	yaw = prevYaw
+        end
+        local moveDir = Vec(0.01 * -roll, 0, 0.01 * pitch)
+        local pos = TransformToParentPoint(chopper.transform, moveDir)
+        if GroundProximityDetection then
+        	pos[2] = pos[2] - 0.1
+        	local dir = VecNormalize(VecSub(pos, chopper.transform.pos))
+        	local maxDist = 0.5 + math.abs(pitch / 5) + math.abs(roll / 10)
+        	QueryRejectBody(chopper.body)
+        	QueryRequire("physical large")
+        	local hit, dist = QueryRaycast(chopper.transform.pos, dir, maxDist)
+        	--local posEnd = VecAdd(chopper.transform.pos, VecScale(dir, maxDist))
+        	if hit then
+        		collective = collective + (maxDist - dist) / (2 * maxDist)
+        	end
+        end
+        pos[2] = collective
+        chopper.angle = chopper.angle + 0.6
+        local rot = QuatEuler(math.sin(chopper.angle*0.053)*5 + pitch, math.sin(chopper.angle*0.04)*5 + yaw, roll)
+        if aimMode then
+        	rot = QuatEuler(pitch, yaw, roll)
+        end
+        chopper.transform.pos = pos
+        chopper.transform.rot = rot
+        SetBodyTransform(chopper.body, chopper.transform)
+        chopper.mainRotorLocalTransform.rot = QuatEuler(0, chopper.angle * 57, 0)
+        SetBodyTransform(chopper.mainRotor, TransformToParentTransform(chopper.transform, chopper.mainRotorLocalTransform))
+        chopper.mainRotor2LocalTransform.rot = QuatEuler(0, chopper.angle * 57, 0)
+        SetBodyTransform(chopper.mainRotor2, TransformToParentTransform(chopper.transform, chopper.mainRotor2LocalTransform))	
+        if isCoaxial then
+        	chopper.tailRotorLocalTransform.rot = QuatEuler(0, -chopper.angle * 57, 0)
+        else
+        	chopper.tailRotorLocalTransform.rot = QuatEuler(chopper.angle * 57, 0)
+        end
+        SetBodyTransform(chopper.tailRotor, TransformToParentTransform(chopper.transform, chopper.tailRotorLocalTransform))
+        cameraX = cameraX - mx / 10
+        cameraY = cameraY - my / 10
+        cameraY = clamp(cameraY, -90, 90)
+        local cameraRot = QuatEuler(cameraY, cameraX, 0)
+        local cameraT = Transform(chopper.transform.pos, cameraRot)
+        zoom = clamp(zoom, -3, 30)
+        local cameraPos = TransformToParentPoint(cameraT, Vec(0, 6, zoom))
+        local camera = Transform(cameraPos, cameraRot)
+        SetCameraTransform(camera)
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("MOD/snd/plasma.ogg", 10.0)
+    rocketSound = LoadSound("tools/launcher0.ogg")	
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputDown("space") then
+    	collective = collective + 0.1
+    end
+    if InputDown("ctrl") and collective ~= 0 then
+    	collective = collective - 0.1
+    end
+    if InputDown("a") and roll < 30 then
+    	roll = roll + 0.5
+    end
+    if InputDown("d") and roll > -30 then
+    	roll = roll - 0.5
+    end
+    if weaponLoc then
+    	local firePos = TransformToParentPoint(chopper.transform, weaponLoc)
+    	local fireDir = TransformToParentVec(chopper.transform, Vec(0, 0, -1))
+    	if vehicleType == "mh_60" then
+    		fireDir = VecNormalize(TransformToParentVec(chopper.transform, Vec(-2, -1, 0)))
+    		if InputDown("lmb") then
+    			PlaySound(shootSound, chopper.transform.pos, 10)
+    			--PointLight(pos, 0.9, 0.1, 0.4, 90)
+    			Shoot(firePos, fireDir, 0)
+    		end
+    	else
+    		if InputPressed("lmb") then
+    			PlaySound(shootSound, chopper.transform.pos, 5)
+    			PointLight(firePos, 0.9, 0.1, 0.4, 90)
+    			Shoot(firePos, fireDir, 0)
+    		end
+    		if InputPressed("rmb") then
+    			PlaySound(rocketSound, chopper.transform.pos, 5)
+    			--PointLight(pos, 0.9, 0.1, 0.4, 90)
+    			Shoot(firePos, fireDir, 1)
+    		end
+    	end
+    elseif isAVF then
+    	if InputPressed("rmb") then
+    		aimMode = not aimMode
+    	end
+    end
+    if InputPressed("h") then
+    	hover = not hover
+    end
+    if not aimMode then
+    	local x, y = EulerQuat(GetCameraTransform().rot)
+
+    	if x < pitch and pitch > -45 then
+    		pitch = pitch - 0.5
+    	end
+    	if x > pitch and pitch < 15 then
+    		pitch = pitch + 0.5
+    	end
+
+    	if y < yaw and not (y < yaw - 180) then
+    		yaw = YawRight(yaw)
+    	elseif y < yaw - 180 then
+    		yaw = YawLeft(yaw)
+    	end
+
+    	if y > yaw and not (y > yaw + 180) then
+    		yaw = YawLeft(yaw)
+    	elseif y > yaw + 180 then
+    		yaw = YawRight(yaw)
+    	end
+    else
+    	local mouseX = -InputValue("mousedx")
+    	local mouseY = -InputValue("mousedy")
+
+    	if sign(mouseY) < 0 and pitch > -45 then
+    		pitch = pitch - 0.5
+    	elseif sign(mouseY) > 0 and pitch < 15 then
+    		pitch = pitch + 0.5
+    	end
+
+    	if sign(mouseX) < 0 then
+    		yaw = YawRight(yaw)
+    	elseif sign(mouseX) > 0 then
+    		yaw = YawLeft(yaw)
+    	end
+    end
+    PlayLoop(chopper.sound, chopper.transform.pos, 0.5)
+    local mx, my = InputValue("mousedx"), InputValue("mousedy")
+    zoom = zoom - InputValue("mousewheel")
+end
+

```

---

# Migration Report: script\endoskeleton.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\endoskeleton.lua
+++ patched/script\endoskeleton.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 2.0)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 50
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 40.0
-config.aggressive = true
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 450.0
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -181,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -198,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 100.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -248,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -279,22 +126,18 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
-
 
 function robotUpdate(dt)
 	robotSetAxes()
@@ -331,7 +174,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -361,7 +204,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -376,35 +219,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -424,9 +255,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -434,10 +264,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -456,7 +282,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -473,7 +298,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -486,7 +310,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -502,8 +325,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -566,7 +387,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -575,7 +396,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -586,15 +407,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -611,11 +423,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -624,12 +436,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -662,7 +468,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -690,9 +495,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -737,7 +541,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -779,13 +583,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -829,13 +626,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -862,7 +657,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -871,10 +665,9 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
 
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -885,7 +678,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -901,14 +694,14 @@
 		local toPlayer = VecSub(GetPlayerEyeTransform().pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 2.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.2 or distToPlayer < 0.1 then
 				rejectAllBodies(robot.allBodies)
 				SetJointMotor(saber, 0)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.2 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength)
 					--SetJointMotor(saber, -15)
 					SetBodyAngularVelocity(body1, Vec(0, -100, 0))
 				end
@@ -916,7 +709,6 @@
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -940,7 +732,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1005,15 +797,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1023,7 +807,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1048,22 +831,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1102,32 +873,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1151,7 +902,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1198,8 +949,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1228,26 +979,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1283,35 +1025,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1403,7 +1126,7 @@
 		end
 
 		local targetRadius = 0.2
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 4.0
 		end
 	
@@ -1434,9 +1157,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1446,7 +1168,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -0.1
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1509,12 +1231,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1563,7 +1279,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1572,8 +1288,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1589,7 +1303,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1604,7 +1317,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1612,7 +1324,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1623,7 +1334,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1642,449 +1352,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("MOD/snd/plasma.ogg", 4.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
-	huntSound = LoadSound("MOD/main/snd/power.ogg", 9.0)
-	idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-	insound = LoadSound("MOD/main/snd/in01.ogg", 9.0)
-	crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
-	swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
-    fdeath = LoadSound("MOD/main/snd/vdeath.ogg", 9.0)
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerEyeTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			Delete(lighsaber)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(fdeath, robot.bodyCenter, 9.0, false)
-		PlaySound(insound, robot.bodyCenter, 0.3, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 0.3, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 3.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			--PlaySound(huntSound, robot.bodyCenter, 50.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2093,64 +1360,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerEyeTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2177,15 +1386,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2210,29 +1417,15 @@
 	end
 end
 
-
-	if IsShapeBroken(target) then
-                        for i=1, #robot.allShapes do
-				if robot.allShapes[i] == shape then
-					robot.stunned = robot.stunned + 1000
-					return
-				end
-			end
-	end
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2250,8 +1443,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2278,16 +1469,477 @@
 	end
 end
 
-function tick(dt)
-	if GetPlayerHealth() <= 0 then
-		if not playing then
-			PlaySound(crush)
-			PlaySound(swing)
-			playing = true
-		end
-	elseif GetPlayerHealth() >= 0 then
-		if playing then
-			playing = false
-		end
-	end
-end
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerEyeTransform().pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerEyeTransform().pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 3.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        if state.id == "huntlost" then
+        	if not state.timer then
+        		state.timer = 6
+        		state.turnTimer = 1
+        	end
+        	state.timer = state.timer - dt
+        	head.dir = VecCopy(robot.dir)
+        	if state.timer < 0 then
+        		--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+        		stackPop()
+        	else
+        		state.turnTimer = state.turnTimer - dt
+        		if state.turnTimer < 0 then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turnTimer = rnd(0.5, 1.5)
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+        if state.id == "navigate" then
+        	if not state.initialized then
+        		if not state.timeout then state.timeout = 30 end
+        		navigationClear()
+        		navigationSetTarget(state.pos, state.timeout)
+        		state.initialized = true
+        	else
+        		head.dir = VecCopy(robot.dir)
+        		navigationUpdate(dt)
+        		if navigation.state == "done" or navigation.state == "fail" then
+        			stackPop()
+        		end
+        	end
+        end
+
+        --React to sound
+        if not stackHas("hunt") then
+        	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+        		stackClear()
+        		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+        		local s = stackPush("investigate")
+        		s.pos = hearing.lastSoundPos	
+        		hearingConsumeSound()
+        	end
+        end
+
+        --Seen player
+        if config.huntPlayer and not stackHas("hunt") then
+        	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+        		stackClear()
+        		--PlaySound(huntSound, robot.bodyCenter, 50.0, false)
+        		stackPush("hunt")
+        	end
+        end
+
+        --Seen player
+        if config.avoidPlayer and not stackHas("avoid") then
+        	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+        		stackClear()
+        		stackPush("avoid")
+        	end
+        end
+
+        --Get up
+        if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+        	stackPush("getup")
+        end
+
+        if IsShapeBroken(GetLightShape(head.eye)) then
+        	config.hasVision = false
+        	config.canSeePlayer = false
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("MOD/snd/plasma.ogg", 4.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
+    huntSound = LoadSound("MOD/main/snd/power.ogg", 9.0)
+    idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+    insound = LoadSound("MOD/main/snd/in01.ogg", 9.0)
+    crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
+    swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
+       fdeath = LoadSound("MOD/main/snd/vdeath.ogg", 9.0)
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		Delete(lighsaber)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(fdeath, robot.bodyCenter, 9.0, false)
+    	PlaySound(insound, robot.bodyCenter, 0.3, false)
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 0.3, false)
+    		stackPop()
+    	end	
+    end
+end
+

```

---

# Migration Report: script\endoskeletonintro.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\endoskeletonintro.lua
+++ patched/script\endoskeletonintro.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 2.0)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 50
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 40.0
-config.aggressive = true
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 450.0
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -181,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -198,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 100.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -248,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -279,28 +126,24 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -319,7 +162,7 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	local vel = GetBodyVelocity(robot.body)
@@ -331,7 +174,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -361,7 +204,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -376,35 +219,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -424,9 +255,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -434,10 +264,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -456,7 +282,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -473,7 +298,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -486,7 +310,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -502,8 +325,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -566,7 +387,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -575,7 +396,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -586,15 +407,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -611,11 +423,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -624,12 +436,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -662,7 +468,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -690,9 +495,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -737,7 +541,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -779,13 +583,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -829,13 +626,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -862,7 +657,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -871,10 +665,9 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
 
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -885,7 +678,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -898,17 +691,17 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 2.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.2 or distToPlayer < 0.1 then
 				rejectAllBodies(robot.allBodies)
 				SetJointMotor(saber, 0)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.2 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength)
 					--SetJointMotor(saber, -15)
 					SetBodyAngularVelocity(body1, Vec(0, -100, 0))
 				end
@@ -916,7 +709,6 @@
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -940,7 +732,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1005,15 +797,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1023,7 +807,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1048,22 +831,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1102,32 +873,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1151,7 +902,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1198,8 +949,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1228,26 +979,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1283,35 +1025,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1403,7 +1126,7 @@
 		end
 
 		local targetRadius = 0.2
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 4.0
 		end
 	
@@ -1434,9 +1157,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1446,7 +1168,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -0.1
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1509,12 +1231,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1563,7 +1279,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1572,8 +1288,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1589,7 +1303,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1604,7 +1317,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1612,7 +1324,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1623,7 +1334,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1642,449 +1352,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("MOD/snd/plasma2.ogg", 3.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
-	huntSound = LoadSound("MOD/main/snd/power.ogg", 9.0)
-	idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-	insound = LoadSound("MOD/main/snd/in01.ogg", 9.0)
-	crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
-	swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
-    fdeath = LoadSound("MOD/main/snd/vdeath.ogg", 9.0)
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			Delete(lighsaber)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(fdeath, robot.bodyCenter, 9.0, false)
-		PlaySound(insound, robot.bodyCenter, 0.3, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 0.3, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 3.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			--PlaySound(huntSound, robot.bodyCenter, 50.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2093,64 +1360,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2177,15 +1386,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2210,29 +1417,15 @@
 	end
 end
 
-
-	if IsShapeBroken(target) then
-                        for i=1, #robot.allShapes do
-				if robot.allShapes[i] == shape then
-					robot.stunned = robot.stunned + 1000
-					return
-				end
-			end
-	end
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2250,8 +1443,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2278,16 +1469,477 @@
 	end
 end
 
-function tick(dt)
-	if GetPlayerHealth() <= 0 then
-		if not playing then
-			PlaySound(crush)
-			PlaySound(swing)
-			playing = true
-		end
-	elseif GetPlayerHealth() >= 0 then
-		if playing then
-			playing = false
-		end
-	end
-end
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 3.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        if state.id == "huntlost" then
+        	if not state.timer then
+        		state.timer = 6
+        		state.turnTimer = 1
+        	end
+        	state.timer = state.timer - dt
+        	head.dir = VecCopy(robot.dir)
+        	if state.timer < 0 then
+        		--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+        		stackPop()
+        	else
+        		state.turnTimer = state.turnTimer - dt
+        		if state.turnTimer < 0 then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turnTimer = rnd(0.5, 1.5)
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+        if state.id == "navigate" then
+        	if not state.initialized then
+        		if not state.timeout then state.timeout = 30 end
+        		navigationClear()
+        		navigationSetTarget(state.pos, state.timeout)
+        		state.initialized = true
+        	else
+        		head.dir = VecCopy(robot.dir)
+        		navigationUpdate(dt)
+        		if navigation.state == "done" or navigation.state == "fail" then
+        			stackPop()
+        		end
+        	end
+        end
+
+        --React to sound
+        if not stackHas("hunt") then
+        	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+        		stackClear()
+        		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+        		local s = stackPush("investigate")
+        		s.pos = hearing.lastSoundPos	
+        		hearingConsumeSound()
+        	end
+        end
+
+        --Seen player
+        if config.huntPlayer and not stackHas("hunt") then
+        	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+        		stackClear()
+        		--PlaySound(huntSound, robot.bodyCenter, 50.0, false)
+        		stackPush("hunt")
+        	end
+        end
+
+        --Seen player
+        if config.avoidPlayer and not stackHas("avoid") then
+        	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+        		stackClear()
+        		stackPush("avoid")
+        	end
+        end
+
+        --Get up
+        if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+        	stackPush("getup")
+        end
+
+        if IsShapeBroken(GetLightShape(head.eye)) then
+        	config.hasVision = false
+        	config.canSeePlayer = false
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("MOD/snd/plasma2.ogg", 3.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
+    huntSound = LoadSound("MOD/main/snd/power.ogg", 9.0)
+    idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+    insound = LoadSound("MOD/main/snd/in01.ogg", 9.0)
+    crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
+    swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
+       fdeath = LoadSound("MOD/main/snd/vdeath.ogg", 9.0)
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		Delete(lighsaber)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(fdeath, robot.bodyCenter, 9.0, false)
+    	PlaySound(insound, robot.bodyCenter, 0.3, false)
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 0.3, false)
+    		stackPop()
+    	end	
+    end
+end
+

```

---

# Migration Report: script\flyover.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\flyover.lua
+++ patched/script\flyover.lua
@@ -1,48 +1,42 @@
+#version 2
 local startTime = 0
 
-function init()	
-	local l0 = FindLocation("start")
-	local l1 = FindLocation("end")
-	
-	t0 = GetLocationTransform(l0)
-	t1 = GetLocationTransform(l1)
-	
-	t = 0
-	
-	startTime = GetTime()	
-
+function server.init()
+    local l0 = FindLocation("start")
+    local l1 = FindLocation("end")
+    t0 = GetLocationTransform(l0)
+    t1 = GetLocationTransform(l1)
+    t = 0
+    startTime = GetTime()	
 end
 
-
-function tick(dt)
-
-    SetPlayerHealth(2)
-
-	t = t + dt
-	if t > 30.6 then
-	          StartLevel("main2","MOD/main2.xml","")
-	end
-	
-	if InputPressed("space") or InputPressed("lmb") then
-		StartLevel("main2","MOD/main2.xml","")
-	end
-
-	--Linear interpolation between t0 and t1
-	local q = t / 30.6
-	local pos = VecLerp(t0.pos, t1.pos, q)
-	local rot = QuatSlerp(t0.rot, t1.rot, q)
-	
-	--Set camera transform, this will override the default camera for this frame
-	SetCameraTransform(Transform(pos, rot))
-	SetCameraFov(100)
-	SetPlayerHealth(100)
-	SetPlayerHealth(100)
-
-
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           SetPlayerHealth(playerId, 2)
+        t = t + dt
+        if t > 30.6 then
+                  StartLevel("main2","MOD/main2.xml","")
+        end
+        --Linear interpolation between t0 and t1
+        local q = t / 30.6
+        local pos = VecLerp(t0.pos, t1.pos, q)
+        local rot = QuatSlerp(t0.rot, t1.rot, q)
+        --Set camera transform, this will override the default camera for this frame
+        SetCameraTransform(Transform(pos, rot))
+        SetCameraFov(100)
+        SetPlayerHealth(playerId, 100)
+        SetPlayerHealth(playerId, 100)
+    end
 end
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("space") or InputPressed("lmb") then
+    	StartLevel("main2","MOD/main2.xml","")
+    end
+end
 
-function draw()
+function client.draw()
     local elapsed = GetTime() - startTime
 
     local screenW = UiWidth()
@@ -66,7 +60,7 @@
         blackAlpha = 1
     end
 
-    if blackAlpha > 0 then
+    if blackAlpha ~= 0 then
         UiPush()
             UiTranslate(UiCenter(), UiMiddle())
             UiAlign("center middle")

```

---

# Migration Report: script\huntedchopper.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\huntedchopper.lua
+++ patched/script\huntedchopper.lua
@@ -1,98 +1,15 @@
--- Animate chopper to chase player
-
-
---TODO
---Difference in light/darkness, movement speed
-
-#include "script/common.lua"
-
-pSpeed = GetFloatParam("speed", 7)
-pActivationId = GetStringParam("id", "challenge.chopper1")
-
-
+#version 2
 function rndFloat(mi, ma)
 	return mi + (ma-mi)*(math.random(0, 1000)/1000.0)
 end
 
-function init()
-	SetBool("level."..pActivationId,false)
-	SetBodyDynamic(chopper, false)
-    SetBodyDynamic(mainrotor, false)
-    SetBodyDynamic(tailrotor, false)		
-
-	chopper = FindBody("chopper")
-	chopperTransform = GetBodyTransform(chopper)
-	
-	mainRotor = FindBody("mainrotor")
-	mainRotorLocalTransform = TransformToLocalTransform(chopperTransform, GetBodyTransform(mainRotor))
-
-	tailRotor = FindBody("tailrotor")
-	tailRotorLocalTransform = TransformToLocalTransform(chopperTransform, GetBodyTransform(tailRotor))
-
-	lightSource = FindLight("light")
-
-	searchLight = FindBody("light")
-	searchLightLocalTransform = TransformToLocalTransform(chopperTransform, GetBodyTransform(searchLight))
-	
-	chopperSound = LoadLoop("MOD/snd/jet.ogg", 15.0)
-	--chopperChargeSound = LoadSound("chopper-charge.ogg")
-	chopperShootSound = LoadSound("MOD/snd/plasma.ogg", 80.0)
-	chopperRocketSound = LoadSound("tools/launcher0.ogg")
-	
-	--chopperStartSound = LoadSound("chopper-start.ogg")
-	--chopperEndSound = LoadSound("chopper-end.ogg")
-	--chopperSoundSound = LoadSound("chopper-sound.ogg")
-	
-	angle = 0.0
-	targetPos = chopperTransform
-
-	chopperHeight = 15
-	chopperVel = Vec()
-	chopperTargetPos = VecAdd(chopperTransform.pos, Vec(0,0,0))
-	chopperTargetRot = QuatEuler()
-	searchLightTargetRot = QuatEuler()
-	searchLightRot = QuatEuler()
-	averageSurroundingHeight = 0
-
-	poiPos = Vec()
-	poiTimer = 0.0
-
-	playerSeen = false
-	timeSinceLastSeen = 0
-
-	shootMode = "search"
-	shootTimer = 0
-	shootCount = 0
-	rocketTimer = 10.0
-
-	lastPlayerPos = GetPlayerPos()
-	playerSpeed = 0
-
-	seenTime = 0
-
-	active = false
-	complete = false
-
-	shotsFired = 0
-
-	choppers = FindBodies("chopper",true)
-	tailrotors = FindBodies("tailrotor",true)
-	mainrotors = FindBodies("mainrotor",true)
-	lights = FindBodies("light",true)
-
-	hardmode = false
-	outlineAlpha = 0
-end
-
-
 function getDistanceToPlayer()
-	local playerPos = GetPlayerPos()
+	local playerPos = GetPlayerPos(playerId)
 	return VecLength(VecSub(playerPos, chopperTransform.pos))
 end
 
-
 function getTimeVisibleBeforeBeingSeen()
-	local playerPos = GetPlayerPos()
+	local playerPos = GetPlayerPos(playerId)
 	if IsPointAffectedByLight(lightSource, playerPos) then
 		return 0
 	end
@@ -103,7 +20,7 @@
 	end
 
 	--
-	if GetPlayerVehicle() ~= 0 then
+	if GetPlayerVehicle(playerId) ~= 0 then
 		nominalTime = 6
 		if hardmode then
 			nominalTime = 3
@@ -119,7 +36,7 @@
 	local distanceUpper = 100
 	local distanceFactor = 1.0 - clamp(d-distanceLower, 0, distanceUpper-distanceLower)/(distanceUpper-distanceLower)
 
-	local toPlayer = VecNormalize(VecSub(GetPlayerPos(), chopperTransform.pos))
+	local toPlayer = VecNormalize(VecSub(GetPlayerPos(playerId), chopperTransform.pos))
 	local forward = TransformToParentVec(chopperTransform, Vec(0, 0, -1))
 	local orientationFactor = clamp(VecDot(forward, toPlayer) * 0.7 + 0.3, 0.0, 1.0)
 		
@@ -136,29 +53,26 @@
 	return (1.0-visibility) * nominalTime
 end
 
-
 function choosePatrolTarget()
 	local dir = VecNormalize(Vec(rndFloat(-1,1), 0, rndFloat(-1,1)))
 	local r = rndFloat(15, 30)
-	targetPos = VecAdd(GetPlayerPos(), VecScale(dir, r))
+	targetPos = VecAdd(GetPlayerPos(playerId), VecScale(dir, r))
 	timeSinceLastSeen = 0
 end
 
-
 function canSeePlayer()
-	local playerPos = GetPlayerPos()
+	local playerPos = GetPlayerPos(playerId)
 
 	--Direction to player
 	local dir = VecSub(playerPos, chopperTransform.pos)
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	QueryRejectBody(chopper)
-	QueryRejectBody(GetPlayerGrabBody())
+	QueryRejectBody(GetPlayerGrabBody(playerId))
 	return not QueryRaycast(chopperTransform.pos, dir, dist, 0, true)
 end
-
 
 function getSoundVolume(pos)
 	local d = VecLength(VecSub(pos, chopperTransform.pos))
@@ -178,7 +92,6 @@
 	return blockedFactor * distanceFactor
 end
 
-
 function shoot()
 	PlaySound(chopperShootSound, chopperTransform.pos, 80, false)
 
@@ -186,7 +99,7 @@
 	local d = VecNormalize(VecSub(targetPos, p)) 
 	local spread = 0.03
 
-	if GetPlayerVehicle() ~= 0 then
+	if GetPlayerVehicle(playerId) ~= 0 then
 		spread = 0.1
 	end
 
@@ -200,7 +113,6 @@
 	shotsFired = shotsFired + 1
 end
 
-
 function rocket()
 	PlaySound(chopperRocketSound, chopperTransform.pos, 5, false)
 
@@ -208,7 +120,7 @@
 	local d = VecNormalize(VecSub(targetPos, p))
 	local spread = 0.03
 
-	if GetPlayerVehicle() ~= 0 then
+	if GetPlayerVehicle(playerId) ~= 0 then
 		spread = 0.1
 	end
 
@@ -220,13 +132,12 @@
 	Shoot(p, d, 1)
 end
 
-
 function tickShooting(dt)
 	if GetFloat("game.player.health") == 0.0 or GetString("level.state") ~= "" then
 		return
 	end
 
-	if shootTimer > 0 then
+	if shootTimer ~= 0 then
 		shootTimer = shootTimer - dt
 		return
 	end
@@ -245,7 +156,7 @@
 		end
 
 	elseif shootMode == "shoot" then
-		if shootCount > 0 then
+		if shootCount ~= 0 then
 			shootCount = shootCount - 1
 			shoot();
 			shootTimer = 0.2
@@ -261,7 +172,6 @@
 	end
 end
 
-
 function considerRocket()
 	if math.random() < 0.4 and shotsFired > 10 then
 		rocketTimer = 1 + math.random()*2
@@ -269,7 +179,6 @@
 		rocketTimer = 0
 	end
 end
-
 
 function computeSurroundingHeight()
 	rejectAllHelicopters() 
@@ -300,211 +209,255 @@
 	end
 end
 
-function tick(dt)
-	--if not active and GetBool("challenge."..pActivationId) then
-    if not active then--just spawn
-		PlaySound(chopperStartSound)
-		active = true
-		targetPos = GetPlayerPos()
-		chopperTransform.pos[2] = chopperHeight
-	end
-
-	if GetBool("challenge.hardmode") then
-		hardmode = true
-	end
-
-	if not active then
-		return
-	end
-
-	if not complete and GetFloat("game.player.health") == 0.0 then
-		complete = true
-		PlaySound(chopperEndSound)
-		return
-	end
-
-	angle = angle + 0.6
-
-	playerSpeed = VecLength(VecSub(GetPlayerPos(), lastPlayerPos)) / dt
-
-	playerSeen = false
-	if canSeePlayer() then
-		seenTime = seenTime + dt
-		local limit = getTimeVisibleBeforeBeingSeen()
-		if seenTime > limit then
-			targetPos = GetPlayerPos()
-			playerSeen = true
-			considerRocket()
-		end
-	else
-		seenTime = math.max(0.0, math.min(1.0, seenTime) - dt * 0.5)
-	end
-
-	if playerSeen then
-		timeSinceLastSeen = 0
-	else
-		timeSinceLastSeen = timeSinceLastSeen + dt
-	end
-	
-	--Let the chopper see player for two extra second if recently seen
-	if timeSinceLastSeen < 2.0 and seenTime > 0 then
-		playerSeen = true
-		targetPos = GetPlayerPos()
-	end	
-
-	if timeSinceLastSeen > 10 then
-		choosePatrolTarget()
-	end
-
-	if timeSinceLastSeen > 3 then
-		local volume, pos = GetLastSound();
-		if volume > 0.5 then
-	 		local v = getSoundVolume(pos) * volume
-			if v > 0.5 then
-				targetPos = pos
-				timeSinceLastSeen = 0
-				PlaySound(chopperSoundSound)
-			end
-		end
-	end
-
-	if not playerSeen and rocketTimer > 0 then
-		rocketTimer = rocketTimer - dt
-		if rocketTimer <= 0.0 then
-			rocket()
-			considerRocket()
-		end
-	end
-
-	tickShooting(dt)
-
-	--Hover around last seen point when searching
-	local hoverPos = VecCopy(targetPos)
-	if not playerSeen then
-		local radius = clamp(10 + timeSinceLastSeen, 10, 20)
-		if not hoverAngle then hoverAngle = 0 end
-		hoverAngle = hoverAngle + dt*0.25
-		local x = math.cos(hoverAngle) * radius
-		local z = math.sin(hoverAngle) * radius
-		hoverPos = VecAdd(hoverPos, Vec(x, 0, z))
-	end
-
-	local toPlayer = VecSub(hoverPos, chopperTargetPos)
-	toPlayer[2] = 0
-	local l = VecLength(toPlayer)
-	local minDist = 1.0
-	if l > minDist then
-		local speed = (l-minDist)
-		if speed > pSpeed then
-			speed = pSpeed
-		end
-		toPlayer = VecNormalize(toPlayer)
-		chopperTargetPos = VecAdd(chopperTargetPos, VecScale(toPlayer, speed*dt))
-	end
-
-	computeSurroundingHeight()
-
-	local currentHeight = chopperHeight
-	rejectAllHelicopters()
-	local probe = VecCopy(chopperTargetPos)
-	probe[2] = 100
-	local hit, dist = QueryRaycast(probe, Vec(0,-1,0), 100, 2.0)
-	if hit then
-		currentHeight = currentHeight + (100 - dist)
-	end
-	currentHeight = math.max(currentHeight, averageSurroundingHeight)
-	chopperTargetPos[2] = currentHeight + math.sin(GetTime()*0.7)*5
-
-	local toTarget = VecNormalize(VecSub(targetPos, chopperTargetPos))
-	toTarget[2] = clamp(toTarget[2], -0.1, 0.1);
-	local lookPoint = VecAdd(chopperTargetPos, toTarget);
-	lookPoint[2] = chopperTargetPos[2]
-	local rot = QuatLookAt(chopperTargetPos, lookPoint)
-	rot = QuatRotateQuat(rot, QuatEuler(math.sin(angle*0.053)*10, math.sin(angle*0.04)*10, 0))
-	chopperTargetRot = rot
-
-	SetBodyTransform(chopper, chopperTransform)
-	PlayLoop(chopperSound, chopperTransform.pos, 1, false)
-	
-	mainRotorLocalTransform.rot = QuatEuler(0, angle*50, 0)
-	SetBodyTransform(mainRotor, TransformToParentTransform(chopperTransform, mainRotorLocalTransform))
-
-	tailRotorLocalTransform.rot = QuatEuler(0, angle*50, 0)
-	SetBodyTransform(tailRotor, TransformToParentTransform(chopperTransform, tailRotorLocalTransform))
-
-	--Searchlight
-	local aimPos = VecCopy(targetPos)
-	local radius = clamp(timeSinceLastSeen, 0, 10)
-	if not aimAngle then aimAngle = 0 end
-	aimAngle = aimAngle + dt*1.0
-	local x = math.cos(aimAngle) * radius
-	local z = math.sin(aimAngle*1.7) * radius
-	aimPos = VecAdd(aimPos, Vec(x, 0, z))
-
-	if poiTimer > 0.0 then
-		poiTimer = poiTimer - dt
-		aimPos = poiPos
-	end
-
-	local lightTransform = TransformToParentTransform(chopperTransform, searchLightLocalTransform)
-	searchLightTargetRot = QuatLookAt(lightTransform.pos, aimPos)
-	lightTransform.rot = searchLightRot
-	SetBodyTransform(searchLight, lightTransform)
-
-
-	local alpha = 0.0
-	if timeSinceLastSeen > 0.0 then
-		alpha = clamp(1.0 - (getDistanceToPlayer()-50) / 50, 0.0, 0.5)
-		if alpha < 0.1 then
-			alpha = 0.0
-		end
-	end
-	outlineAlpha = outlineAlpha + clamp(alpha - outlineAlpha, -0.01, 0.01)
-	if outlineAlpha > 0.0 then
-		--DrawBodyOutline(chopper, outlineAlpha)
-		--DrawBodyOutline(mainRotor, outlineAlpha)
-		--DrawBodyOutline(tailRotor, outlineAlpha)
-	end
-
-	lastPlayerPos = GetPlayerPos()
-
-	-- avoid other helicopters
-	QueryRejectBody(chopper)
-	QueryRejectBody(tailRotor)
-	QueryRejectBody(mainRotor)
-	QueryRejectBody(searchLight)
-	QueryRequire("dynamic")
-	local hit, p, n, s = QueryClosestPoint(chopperTargetPos, 8)
-	if hit then
-		local dir = VecSub(chopperTransform.pos, p)
-		dir[2] = 0
-		dir = VecNormalize(dir)
-		chopperTargetPos = VecAdd(chopperTargetPos , VecScale(dir,8))
-	end
-	
-end
-
-function update(dt)
+function server.init()
+    SetBool("level."..pActivationId,false, true)
     SetBodyDynamic(chopper, false)
-    SetBodyDynamic(mainrotor, false)
-    SetBodyDynamic(tailrotor, false)	
-	if not active then
-		return
-	end
-	
-    SetBodyDynamic(chopper, false)
-    SetBodyDynamic(mainrotor, false)
-    SetBodyDynamic(tailrotor, false)	
-
-	--Move chopper towards target position smoothly
-	local acc = VecSub(chopperTargetPos, chopperTransform.pos)
-	chopperVel = VecAdd(chopperVel, VecScale(acc, dt))
-	chopperVel = VecScale(chopperVel, 0.98)
-	chopperTransform.pos = VecAdd(chopperTransform.pos, VecScale(chopperVel, dt))
-
-	--Rotate chopper smoothly towards target rotation
-	chopperTransform.rot = QuatSlerp(chopperTransform.rot, chopperTargetRot, 0.01)
-
-	--Rotate search light smoothly towards target rotation
-	searchLightRot = QuatSlerp(searchLightRot, searchLightTargetRot, 0.05)
-end
+       SetBodyDynamic(mainrotor, false)
+       SetBodyDynamic(tailrotor, false)		
+    chopper = FindBody("chopper")
+    chopperTransform = GetBodyTransform(chopper)
+    mainRotor = FindBody("mainrotor")
+    mainRotorLocalTransform = TransformToLocalTransform(chopperTransform, GetBodyTransform(mainRotor))
+    tailRotor = FindBody("tailrotor")
+    tailRotorLocalTransform = TransformToLocalTransform(chopperTransform, GetBodyTransform(tailRotor))
+    lightSource = FindLight("light")
+    searchLight = FindBody("light")
+    searchLightLocalTransform = TransformToLocalTransform(chopperTransform, GetBodyTransform(searchLight))
+    chopperSound = LoadLoop("MOD/snd/jet.ogg", 15.0)
+    --chopperChargeSound = LoadSound("chopper-charge.ogg")
+    --chopperStartSound = LoadSound("chopper-start.ogg")
+    --chopperEndSound = LoadSound("chopper-end.ogg")
+    --chopperSoundSound = LoadSound("chopper-sound.ogg")
+    angle = 0.0
+    targetPos = chopperTransform
+    chopperHeight = 15
+    chopperVel = Vec()
+    chopperTargetPos = VecAdd(chopperTransform.pos, Vec(0,0,0))
+    chopperTargetRot = QuatEuler()
+    searchLightTargetRot = QuatEuler()
+    searchLightRot = QuatEuler()
+    averageSurroundingHeight = 0
+    poiPos = Vec()
+    poiTimer = 0.0
+    playerSeen = false
+    timeSinceLastSeen = 0
+    shootMode = "search"
+    shootTimer = 0
+    shootCount = 0
+    rocketTimer = 10.0
+    lastPlayerPos = GetPlayerPos(playerId)
+    playerSpeed = 0
+    seenTime = 0
+    active = false
+    complete = false
+    shotsFired = 0
+    choppers = FindBodies("chopper",true)
+    tailrotors = FindBodies("tailrotor",true)
+    mainrotors = FindBodies("mainrotor",true)
+    lights = FindBodies("light",true)
+    hardmode = false
+    outlineAlpha = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetBool("challenge.hardmode") then
+        	hardmode = true
+        end
+        if not active then
+        	return
+        end
+        angle = angle + 0.6
+        playerSpeed = VecLength(VecSub(GetPlayerPos(playerId), lastPlayerPos)) / dt
+        playerSeen = false
+        if canSeePlayer() then
+        	seenTime = seenTime + dt
+        	local limit = getTimeVisibleBeforeBeingSeen()
+        	if seenTime > limit then
+        		targetPos = GetPlayerPos(playerId)
+        		playerSeen = true
+        		considerRocket()
+        	end
+        else
+        	seenTime = math.max(0.0, math.min(1.0, seenTime) - dt * 0.5)
+        end
+        if playerSeen then
+        	timeSinceLastSeen = 0
+        else
+        	timeSinceLastSeen = timeSinceLastSeen + dt
+        end
+        --Let the chopper see player for two extra second if recently seen
+        if timeSinceLastSeen < 2.0 and seenTime ~= 0 then
+        	playerSeen = true
+        	targetPos = GetPlayerPos(playerId)
+        end	
+        if timeSinceLastSeen > 10 then
+        	choosePatrolTarget()
+        end
+        if not playerSeen and rocketTimer ~= 0 then
+        	rocketTimer = rocketTimer - dt
+        	if rocketTimer <= 0.0 then
+        		rocket()
+        		considerRocket()
+        	end
+        end
+        tickShooting(dt)
+        --Hover around last seen point when searching
+        local hoverPos = VecCopy(targetPos)
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           SetBodyDynamic(chopper, false)
+           SetBodyDynamic(mainrotor, false)
+           SetBodyDynamic(tailrotor, false)	
+        if not active then
+        	return
+        end
+           SetBodyDynamic(chopper, false)
+           SetBodyDynamic(mainrotor, false)
+           SetBodyDynamic(tailrotor, false)	
+        --Move chopper towards target position smoothly
+        local acc = VecSub(chopperTargetPos, chopperTransform.pos)
+        chopperVel = VecAdd(chopperVel, VecScale(acc, dt))
+        chopperVel = VecScale(chopperVel, 0.98)
+        chopperTransform.pos = VecAdd(chopperTransform.pos, VecScale(chopperVel, dt))
+        --Rotate chopper smoothly towards target rotation
+        chopperTransform.rot = QuatSlerp(chopperTransform.rot, chopperTargetRot, 0.01)
+        --Rotate search light smoothly towards target rotation
+        searchLightRot = QuatSlerp(searchLightRot, searchLightTargetRot, 0.05)
+    end
+end
+
+function client.init()
+    chopperShootSound = LoadSound("MOD/snd/plasma.ogg", 80.0)
+    chopperRocketSound = LoadSound("tools/launcher0.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+       if not active then--just spawn
+    	PlaySound(chopperStartSound)
+    	active = true
+    	targetPos = GetPlayerPos(playerId)
+    	chopperTransform.pos[2] = chopperHeight
+    end
+    if not complete and GetFloat("game.player.health") == 0.0 then
+    	complete = true
+    	PlaySound(chopperEndSound)
+    	return
+    end
+    if timeSinceLastSeen > 3 then
+    	local volume, pos = GetLastSound();
+    	if volume > 0.5 then
+     		local v = getSoundVolume(pos) * volume
+    		if v > 0.5 then
+    			targetPos = pos
+    			timeSinceLastSeen = 0
+    			PlaySound(chopperSoundSound)
+    		end
+    	end
+    end
+    if not playerSeen then
+    	local radius = clamp(10 + timeSinceLastSeen, 10, 20)
+    	if not hoverAngle then hoverAngle = 0 end
+    	hoverAngle = hoverAngle + dt*0.25
+    	local x = math.cos(hoverAngle) * radius
+    	local z = math.sin(hoverAngle) * radius
+    	hoverPos = VecAdd(hoverPos, Vec(x, 0, z))
+    end
+
+    local toPlayer = VecSub(hoverPos, chopperTargetPos)
+    toPlayer[2] = 0
+    local l = VecLength(toPlayer)
+    local minDist = 1.0
+    if l > minDist then
+    	local speed = (l-minDist)
+    	if speed > pSpeed then
+    		speed = pSpeed
+    	end
+    	toPlayer = VecNormalize(toPlayer)
+    	chopperTargetPos = VecAdd(chopperTargetPos, VecScale(toPlayer, speed*dt))
+    end
+
+    computeSurroundingHeight()
+
+    local currentHeight = chopperHeight
+    rejectAllHelicopters()
+    local probe = VecCopy(chopperTargetPos)
+    probe[2] = 100
+    local hit, dist = QueryRaycast(probe, Vec(0,-1,0), 100, 2.0)
+    if hit then
+    	currentHeight = currentHeight + (100 - dist)
+    end
+    currentHeight = math.max(currentHeight, averageSurroundingHeight)
+    chopperTargetPos[2] = currentHeight + math.sin(GetTime()*0.7)*5
+
+    local toTarget = VecNormalize(VecSub(targetPos, chopperTargetPos))
+    toTarget[2] = clamp(toTarget[2], -0.1, 0.1);
+    local lookPoint = VecAdd(chopperTargetPos, toTarget);
+    lookPoint[2] = chopperTargetPos[2]
+    local rot = QuatLookAt(chopperTargetPos, lookPoint)
+    rot = QuatRotateQuat(rot, QuatEuler(math.sin(angle*0.053)*10, math.sin(angle*0.04)*10, 0))
+    chopperTargetRot = rot
+
+    SetBodyTransform(chopper, chopperTransform)
+    PlayLoop(chopperSound, chopperTransform.pos, 1, false)
+
+    mainRotorLocalTransform.rot = QuatEuler(0, angle*50, 0)
+    SetBodyTransform(mainRotor, TransformToParentTransform(chopperTransform, mainRotorLocalTransform))
+
+    tailRotorLocalTransform.rot = QuatEuler(0, angle*50, 0)
+    SetBodyTransform(tailRotor, TransformToParentTransform(chopperTransform, tailRotorLocalTransform))
+
+    --Searchlight
+    local aimPos = VecCopy(targetPos)
+    local radius = clamp(timeSinceLastSeen, 0, 10)
+    if not aimAngle then aimAngle = 0 end
+    aimAngle = aimAngle + dt*1.0
+    local x = math.cos(aimAngle) * radius
+    local z = math.sin(aimAngle*1.7) * radius
+    aimPos = VecAdd(aimPos, Vec(x, 0, z))
+
+    if poiTimer > 0.0 then
+    	poiTimer = poiTimer - dt
+    	aimPos = poiPos
+    end
+
+    local lightTransform = TransformToParentTransform(chopperTransform, searchLightLocalTransform)
+    searchLightTargetRot = QuatLookAt(lightTransform.pos, aimPos)
+    lightTransform.rot = searchLightRot
+    SetBodyTransform(searchLight, lightTransform)
+
+    local alpha = 0.0
+    if timeSinceLastSeen > 0.0 then
+    	alpha = clamp(1.0 - (getDistanceToPlayer()-50) / 50, 0.0, 0.5)
+    	if alpha < 0.1 then
+    		alpha = 0.0
+    	end
+    end
+    outlineAlpha = outlineAlpha + clamp(alpha - outlineAlpha, -0.01, 0.01)
+    if outlineAlpha > 0.0 then
+    	--DrawBodyOutline(chopper, outlineAlpha)
+    	--DrawBodyOutline(mainRotor, outlineAlpha)
+    	--DrawBodyOutline(tailRotor, outlineAlpha)
+    end
+
+    lastPlayerPos = GetPlayerPos(playerId)
+
+    -- avoid other helicopters
+    QueryRejectBody(chopper)
+    QueryRejectBody(tailRotor)
+    QueryRejectBody(mainRotor)
+    QueryRejectBody(searchLight)
+    QueryRequire("dynamic")
+    local hit, p, n, s = QueryClosestPoint(chopperTargetPos, 8)
+    if hit then
+    	local dir = VecSub(chopperTransform.pos, p)
+    	dir[2] = 0
+    	dir = VecNormalize(dir)
+    	chopperTargetPos = VecAdd(chopperTargetPos , VecScale(dir,8))
+    end
+end
+

```

---

# Migration Report: script\skyboxrotater.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\skyboxrotater.lua
+++ patched/script\skyboxrotater.lua
@@ -1,4 +1,8 @@
-function tick(dt)
-    local t = math.sin(GetTime()*0.04) * 1.5
-    SetEnvironmentProperty("skyboxrot", GetTime())
-end	
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local t = math.sin(GetTime()*0.04) * 1.5
+        SetEnvironmentProperty("skyboxrot", GetTime())
+    end
+end
+

```

---

# Migration Report: script\terminator.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\terminator.lua
+++ patched/script\terminator.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,36 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 2.0)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 50
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 40.0
-config.aggressive = true
-config.stepSound = "m"
-config.practice = false
-config.maxHealth = 450.0
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -181,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -198,49 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-robot.health = 100.0
-robot.headDamageScale = 3.0
-robot.torsoDamageScale = 1.4
-robot.torso = 0
-robot.head = 0
-robot.rightHand = 0
-robot.leftHand = 0
-robot.rightFoot = 0
-robot.leftFoot = 0
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -248,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 
@@ -279,22 +126,18 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
-
 
 function robotUpdate(dt)
 	robotSetAxes()
@@ -331,7 +174,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -361,7 +204,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -376,35 +219,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			--PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -424,9 +255,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -434,10 +264,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -456,7 +282,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -473,7 +298,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -486,7 +310,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -502,8 +325,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -566,7 +387,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -575,7 +396,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -586,15 +407,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -611,11 +423,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -624,12 +436,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -662,7 +468,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -690,9 +495,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -737,7 +541,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -779,13 +583,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -829,13 +626,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -862,7 +657,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -871,10 +665,9 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
 
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -885,7 +678,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -901,14 +694,14 @@
 		local toPlayer = VecSub(GetPlayerEyeTransform().pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 2.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.2 or distToPlayer < 0.1 then
 				rejectAllBodies(robot.allBodies)
 				SetJointMotor(saber, 0)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.2 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength)
 					--SetJointMotor(saber, -15)
 					SetBodyAngularVelocity(body1, Vec(0, -100, 0))
 				end
@@ -916,7 +709,6 @@
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -940,7 +732,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -1005,15 +797,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1023,7 +807,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1048,22 +831,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1102,32 +873,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 1	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1151,7 +902,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1198,8 +949,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				--PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1228,26 +979,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		--PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(10, -100, 10)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1283,35 +1025,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1403,7 +1126,7 @@
 		end
 
 		local targetRadius = 0.2
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 4.0
 		end
 	
@@ -1434,9 +1157,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1446,7 +1168,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -0.1
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1509,12 +1231,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1563,7 +1279,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1572,8 +1288,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1589,7 +1303,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1604,7 +1317,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1612,7 +1324,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1623,7 +1334,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1642,449 +1352,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
-	turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
-	huntSound = LoadSound("MOD/snd/talk0.ogg", 90.0)
-	idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-	insound = LoadSound("MOD/main/snd/in01.ogg", 9.0)
-	crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
-	swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
-    fdeath = LoadSound("MOD/main/snd/vdeath.ogg", 9.0)
-        mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
-
-
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerEyeTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if robot.health <= 0.0 then
-		for i = 1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-			Delete(lighsaber)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-		PlaySound(fdeath, robot.bodyCenter, 9.0, false)
-		PlaySound(insound, robot.bodyCenter, 0.3, false)
-	end
-	
-	if IsPointInWater(robot.bodyCenter) then
-		--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 0.3, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 3.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 400.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2093,64 +1360,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerEyeTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2177,15 +1386,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2210,29 +1417,15 @@
 	end
 end
 
-
-	if IsShapeBroken(target) then
-                        for i=1, #robot.allShapes do
-				if robot.allShapes[i] == shape then
-					robot.stunned = robot.stunned + 1000
-					return
-				end
-			end
-	end
-
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2250,8 +1443,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2278,16 +1469,477 @@
 	end
 end
 
-function tick(dt)
-	if GetPlayerHealth() <= 0 then
-		if not playing then
-			PlaySound(crush)
-			PlaySound(swing)
-			playing = true
-		end
-	elseif GetPlayerHealth() >= 0 then
-		if playing then
-			playing = false
-		end
-	end
-end
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerEyeTransform().pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerEyeTransform().pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        if IsPointInWater(robot.bodyCenter) then
+        	--PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+        	for i=1, #robot.allShapes do
+        		SetShapeEmissiveScale(robot.allShapes[i], 0)
+        	end
+        	SetTag(robot.body, "disabled")
+        	robot.enabled = false
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 1000.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 3.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        if state.id == "huntlost" then
+        	if not state.timer then
+        		state.timer = 6
+        		state.turnTimer = 1
+        	end
+        	state.timer = state.timer - dt
+        	head.dir = VecCopy(robot.dir)
+        	if state.timer < 0 then
+        		--PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+        		stackPop()
+        	else
+        		state.turnTimer = state.turnTimer - dt
+        		if state.turnTimer < 0 then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turnTimer = rnd(0.5, 1.5)
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("MOD/main/snd/villager/woman.ogg", 7.0)
+    turnLoop = LoadLoop("MOD/main/snd/villager/m3.ogg", 7.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadSound("MOD/main/snd/villager/midle2.ogg")
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("MOD/main/snd/villager/m1.ogg", 9.0)
+    huntSound = LoadSound("MOD/snd/talk0.ogg", 90.0)
+    idleSound = LoadSound("MOD/main/snd/villager/midle0.ogg")
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+    insound = LoadSound("MOD/main/snd/in01.ogg", 9.0)
+    crush = LoadSound("MOD/main/snd/clsh08.ogg", 9.0)
+    swing = LoadSound("MOD/main/snd/swng07.ogg", 9.0)
+       fdeath = LoadSound("MOD/main/snd/vdeath.ogg", 9.0)
+           mdeath = LoadSound("MOD/main/snd/villager/mdeath0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if robot.health <= 0.0 then
+    	for i = 1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    		Delete(lighsaber)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    	PlaySound(fdeath, robot.bodyCenter, 9.0, false)
+    	PlaySound(insound, robot.bodyCenter, 0.3, false)
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 0.3, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		--PlaySound(alertSound, robot.bodyCenter, 2.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 400.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: script\weaponscripts.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\weaponscripts.lua
+++ patched/script\weaponscripts.lua
@@ -1,15 +1,4 @@
-autoCannonShellHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false}
-} --for secondary autocannon
-
-rocketHandler = {
-	rocketNum = 1,
-	rockets = {},
-	defaultRocket = {active = false}
-} --for rockets
-
+#version 2
 function initAutoCannon()
 	autoCannonSettings = FindLocation("autocannonsettings")
 	autoCannonSound = LoadSound("MOD/snd/plasma.ogg", 20.0)
@@ -66,7 +55,6 @@
 	laserReady = false
 end
 
---autocannon
 function autoCannonFire()
 	local origin = TransformToParentTransform(hrafnTransform,autoCannonLocalMuzzle) --should be the unmoving muzzle of the drone
 	origin.rot = QuatLookAt(origin.pos,lookPos)
@@ -108,23 +96,23 @@
 	
 	--check player for damage
 	local hitPlayer = false --will it hit you?
-	local ppos = GetPlayerPos()
+	local ppos = GetPlayerPos(playerId)
 	ppos[2] = ppos[2]-0.5
 	local pdist,phit = getDistanceToLineSegment(ppos,shell.pos,ahead)
 	if pdist < 0.6 then
 		hitPlayer = true
 	end
-	ppos = GetPlayerCameraTransform().pos
+	ppos = GetPlayerCameraTransform(playerId).pos
 	ppos[2] = ppos[2] - 0.7 --now 1.2 m height
 	local pdist,phit = getDistanceToLineSegment(ppos,shell.pos,ahead)
 	if pdist < 0.6 then
 		hitPlayer = true
 	end
 	if hitPlayer then
-		local health = GetPlayerHealth()
+		local health = GetPlayerHealth(playerId)
 		health = health - 0.1
 		--health = math.max(0.1,health - 0.1)
-		SetPlayerHealth(health)
+		SetPlayerHealth(playerId, health)
 	end
 	
 	if squadup then rejectAll() else rejectSelf() end --disable friendly fire
@@ -270,6 +258,7 @@
 		shell.active = false
 	end
 end
+
 function tickAutoCannon(dt)
 	if autoCannonReady then activeWeaponCount = activeWeaponCount+1 end --weapon is operating
 	if playerDead() then
@@ -278,11 +267,11 @@
 		-- return 
 	end
 	if autoCannonReady then
-		if autoCannonFireDelay > 0 then
+		if autoCannonFireDelay ~= 0 then
 			autoCannonFireDelay = math.max(0,autoCannonFireDelay - dt) --stop function here if delayed
 			return
 		end
-		if autoCannonShotCount > 0 then
+		if autoCannonShotCount ~= 0 then
 			autoCannonFire()
 			autoCannonFireDelay = autoCannonFR+ math.random()*0.1
 			autoCannonShotCount = autoCannonShotCount - 1
@@ -292,7 +281,6 @@
 	end
 end
 
---laser 
 function laser()
 	local origin = TransformToParentTransform(hrafnTransform,laserPoint) --should be the unmoving muzzle of the drone
 	origin.rot = laserRot
@@ -322,27 +310,28 @@
 	PlayLoop(laserHitLoop,hitPos,6,false)
 	--check player for damage
 	local hitPlayer = false --will it hit you?
-	local ppos = GetPlayerPos()
+	local ppos = GetPlayerPos(playerId)
 	ppos[2] = ppos[2]-0.5
 	local pdist,phit = getDistanceToLineSegment(ppos,origin.pos,hitPos)
 	PlayLoop(laserLoop,phit,4,false)
 	if pdist < 0.7 then
 		hitPlayer = true
 	end
-	ppos = GetPlayerCameraTransform().pos
+	ppos = GetPlayerCameraTransform(playerId).pos
 	ppos[2] = ppos[2] - 0.7 --now 1.2 m height
 	local pdist,phit = getDistanceToLineSegment(ppos,origin.pos,hitPos)
 	if pdist < 0.7 then
 		hitPlayer = true
 	end
 	if hitPlayer then
-		PlaySound(laserHitPlayer,GetPlayerPos(),0.6,false)
-		local health = GetPlayerHealth()
+		PlaySound(laserHitPlayer,GetPlayerPos(playerId),0.6,false)
+		local health = GetPlayerHealth(playerId)
 		health = health - 0.005
 		--health = math.max(0.1,health - 0.1)
-		SetPlayerHealth(health)
-	end
-end
+		SetPlayerHealth(playerId, health)
+	end
+end
+
 function laserParticle()
 	ParticleReset()
 	ParticleTile(3)
@@ -351,6 +340,7 @@
 	ParticleCollide(0)
 	ParticleSticky(0)
 end
+
 function tickLaser(dt)
 	laserTargetRot = QuatLookAt(TransformToParentPoint(hrafnTransform,laserPoint.pos),lookPos)
 	laserRot = QuatSlerp(laserRot,laserTargetRot,0.33)
@@ -362,11 +352,11 @@
 		-- return 
 	end
 	if laserReady then
-		if laserDelay > 0 then
+		if laserDelay ~= 0 then
 			laserDelay = math.max(0,laserDelay - dt) --stop function here if delayed
 			return
 		end
-		if laserTimer > 0 then
+		if laserTimer ~= 0 then
 			laser()
 			laserTimer = math.max(0,laserTimer - dt)
 		else
@@ -382,6 +372,7 @@
 		rocketTimer = 0
 	end
 end
+
 function considerRocketReload()
 	if math.random() < 0.78 then
 		rocketTimer = 0.1 + math.random()*0.1
@@ -389,6 +380,7 @@
 		rocketTimer = 0
 	end
 end
+
 function rocketLaunch()
 	local origin = TransformToParentTransform(hrafnTransform,rocketLaunchLocalPoint)
 	origin.rot = QuatLookAt(origin.pos,targetPos)
@@ -406,6 +398,7 @@
 	
 	PlaySound(rocketSound, origin.pos, 5, false)
 end
+
 function rocketOperation(rocket)
 	local ahead = VecAdd(rocket.pos,VecScale(rocket.vel,GetTimeStep()))
 	local dir = VecNormalize(rocket.vel)
@@ -442,4 +435,5 @@
 		rocket.active = false
 		Explosion(rocket.pos,dmg)
 	end
-end+end
+

```

---

# Migration Report: script\winddust.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/script\winddust.lua
+++ patched/script\winddust.lua
@@ -1,20 +1,12 @@
-gLargeParticles = 2
-gSmallParticles = 1
-gSmokeParticles = 7
-gParticleColor = {0.27, 0.25, 0.22}
-gSmokeColor = {0.67, 0.65, 0.62}
-
-
+#version 2
 function rnd(mi, ma)
 	return math.random(100)/100*(ma-mi) + mi
 end
 
-
 function rndVec(t)
 	return Vec(rnd(-t, t), rnd(-t, t), rnd(-t, t))
 end
- 
- 
+
 function getParticlePos(rMin, rMax, life)
 	local camPos = GetCameraTransform().pos
 	local p = rndVec(1)
@@ -31,50 +23,48 @@
 	return p, d
 end
 
-
-function update(dt)
-	ParticleReset()
-	ParticleType("plain")
-	ParticleRadius(0.8)
-	ParticleColor(gParticleColor[1], gParticleColor[2], gParticleColor[3])
-	ParticleAlpha(1, 1, "constant", 0.5, 0.5)
-	ParticleCollide(0)
-	ParticleTile(8)
-	for i = 1, gLargeParticles do
-		local life = 1.0
-		local p, d = getParticlePos(8, 12, life);
-		local vel = GetWindVelocity(p);
-		SpawnParticle(p, vel, life)
-	end
-	
-	ParticleReset()
-	ParticleType("plain")
-	ParticleRadius(0.02)
-	ParticleGravity(-5)
-	ParticleColor(gParticleColor[1], gParticleColor[2], gParticleColor[3])
-	ParticleAlpha(1, 1, "constant", 0.5, 0.5)
-	ParticleCollide(1)
-	ParticleTile(4)
-	for i = 1, gSmallParticles do
-		local life = 1.0
-		local p, d = getParticlePos(6, 10, life);
-		local vel = GetWindVelocity(p);
-		SpawnParticle(p, vel, life)
-	end
-
-	ParticleReset()
-	ParticleType("plain")
-	ParticleGravity(-5)
-	ParticleColor(gSmokeColor[1], gSmokeColor[2], gSmokeColor[3])
-	ParticleAlpha(0.1, 0.1, "constant", 0.5, 0.5)
-	ParticleCollide(1)
-	ParticleTile(0)
-	for i = 1, gSmokeParticles do
-		local life = 1.0
-		local p, d = getParticlePos(8, 32, life);
-		local vel = GetWindVelocity(p);
-		ParticleRadius(d/10)
-		SpawnParticle(p, vel, life)
-	end
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    ParticleReset()
+    ParticleType("plain")
+    ParticleRadius(0.8)
+    ParticleColor(gParticleColor[1], gParticleColor[2], gParticleColor[3])
+    ParticleAlpha(1, 1, "constant", 0.5, 0.5)
+    ParticleCollide(0)
+    ParticleTile(8)
+    for i = 1, gLargeParticles do
+    	local life = 1.0
+    	local p, d = getParticlePos(8, 12, life);
+    	local vel = GetWindVelocity(p);
+    	SpawnParticle(p, vel, life)
+    end
+    ParticleReset()
+    ParticleType("plain")
+    ParticleRadius(0.02)
+    ParticleGravity(-5)
+    ParticleColor(gParticleColor[1], gParticleColor[2], gParticleColor[3])
+    ParticleAlpha(1, 1, "constant", 0.5, 0.5)
+    ParticleCollide(1)
+    ParticleTile(4)
+    for i = 1, gSmallParticles do
+    	local life = 1.0
+    	local p, d = getParticlePos(6, 10, life);
+    	local vel = GetWindVelocity(p);
+    	SpawnParticle(p, vel, life)
+    end
+    ParticleReset()
+    ParticleType("plain")
+    ParticleGravity(-5)
+    ParticleColor(gSmokeColor[1], gSmokeColor[2], gSmokeColor[3])
+    ParticleAlpha(0.1, 0.1, "constant", 0.5, 0.5)
+    ParticleCollide(1)
+    ParticleTile(0)
+    for i = 1, gSmokeParticles do
+    	local life = 1.0
+    	local p, d = getParticlePos(8, 32, life);
+    	local vel = GetWindVelocity(p);
+    	ParticleRadius(d/10)
+    	SpawnParticle(p, vel, life)
+    end
 end
 

```
