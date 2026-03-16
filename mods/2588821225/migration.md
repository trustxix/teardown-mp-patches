# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,330 +1,4 @@
-ak47projectileHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false}
-}
-
-ak47grenadeHandler = {
-	shellNum = 1,
-	shells = {},
-	defaultShell = {active = false}
-}
-
-function init()
-	RegisterTool("g36k", "G36K", "MOD/vox/g36k.vox", 3)
-	SetBool("game.tool.g36k.enabled", true)
-	SetFloat("game.tool.g36k.ammo", 101)
-
-
-	------INITIALISE OPTIONS MENU------
-	damageoption = GetInt("savegame.mod.damageoption")
-	if damageoption < 50 then
-		damageoption = 100
-		SetInt("savegame.mod.damageoption", 100)
-	end
-	slots = {}
-	for i = 1,8 do
-		slots[i] = {}
-		for j = 1,2 do
-			slots[i][j] = {"", {0, 0}, 1, 1}
-		end
-	end
-	grabbed = {{"", {0, 0}, 1, 1}, 0, 0}
-	magtable = {}
-
-	totalmags = GetInt("savegame.mod.totalmags")
-
-	magplace = 1
-	if GetBool("level.optionstriggered") then
-	for i = 1,#slots do
-		for j = 1,#slots[i] do
-			if slots[i][j][2][1] == 0 and magplace < totalmags+1 then
-				local w, h = 1, 1
-				local mag = GetString("savegame.mod.mslot"..magplace)
-				if mag == "mag0" then
-					w, h = 1, 2
-				elseif mag == "mag1" then
-					w, h = 1, 2
-				elseif mag == "mag2" then
-					w, h = 2, 2
-				elseif mag == "mag3" then
-					w, h = 3, 2
-				else
-					w, h = 1, 2
-				end
-				placeItem({{mag, {0, 0}, w, h}, 0, 0}, i, j)
-				magplace = magplace + 1
-				DebugPrint("true")
-				DebugPrint(mag)
-			else
-				DebugPrint("false")
-			end
-		end
-	end
-	end
-
-
-	------INITIALISE WEAPON FUNCTIONS------
-	damage = 0.125 * GetInt("savegame.mod.damage")/100
-	if damage == 0 then
-		damage = 0.125
-	end
-	gravity = Vec(0, -10, 0)
-	hidePos = Vec(0, -200, 0)
-	hideTrans = Transform(hidePos,QuatEuler())
-	velocity = 950
-	drag = 1.7
-	maxMomentum = 3
-	tracer = false
-
-	recoilVertical = 1
-	recoilHorizontal = 6
-	recoilWander = 6
-
-	--armor pen
-	lvl5armor = 0.1
-	lvl4armor = 0.3
-	lvl3armor = 0.6
-	lvl2armor = 0.9
-	lvl1armor = 1
-
-	inside = {}
-	for i = 1,50 do
-		inside[i] = {0,0,0,0}
-	end
-	hoverindex = 0
-
-	--magazine and attachments system
-	gunsound = LoadSound("MOD/snd/ak0.ogg")
-	suppressedgunsound = LoadSound("MOD/snd/aksuppressed.ogg")
-	grenadelaunchersound = LoadSound("MOD/snd/grenadelauncher.ogg")
-	toprail = GetString("savegame.mod.toprail")
-	muzzle = GetString("savegame.mod.muzzle")
-	stock = GetString("savegame.mod.stock")
-	foldstock = GetString("savegame.mod.foldstock")
-	realistic = GetBool("savegame.mod.realistic")
-
-	--magazine system
-	mslot1 = GetString("savegame.mod.mslot1")
-	mslot2 = GetString("savegame.mod.mslot2")
-	mslot3 = GetString("savegame.mod.mslot3")
-	mslot4 = GetString("savegame.mod.mslot4")
-	mslot5 = GetString("savegame.mod.mslot5")
-	mslot6 = GetString("savegame.mod.mslot6")
-	mslot7 = GetString("savegame.mod.mslot7")
-	mslot8 = GetString("savegame.mod.mslot8")
-	if totalmags == 0 then
-		mslot1, mslot2 = "mag0", "mag0"
-		SetString("savegame.mod.mslot1", "mag0")
-		SetString("savegame.mod.mslot2", "mag0")
-	totalmags = 2
-	end
-magtable2 = {{mslot1,0,0},{mslot2,0,0},{mslot3,0,0},{mslot4,0,0},{mslot5,0,0},{mslot6,0,0},{mslot7,0,0},{mslot8,0,0}}
-	for i=1,8 do
-		local magslottype = GetString("savegame.mod.mslot"..i)
-		if magslottype == "mag0" then
-			magtable2[i][2] = 30
-			magtable2[i][3] = 30
-		elseif magslottype == "mag1" then
-			magtable2[i][2] = 40
-			magtable2[i][3] = 40
-		elseif magslottype == "mag2" then
-			magtable2[i][2] = 50
-			magtable2[i][3] = 50
-		elseif magslottype == "mag3" then
-			magtable2[i][2] = 100
-			magtable2[i][3] = 100
-		else
-			magtable2[i][2] = 20
-			magtable2[i][3] = 20
-		end
-	end
-	curmagslot = 1
-	nextmagslot = 1
-	if realistic then
-		sightadjust = -0.005
-		mag = mslot1
-		reloadFactor = 1
-	else
-		sightadjust = 0
-		mag = GetString("savegame.mod.mag")
-		reloadFactor = 1
-	end
-	grip = GetString("savegame.mod.grip")
-	barrel = GetString("savegame.mod.barrel")
-	side = GetString("savegame.mod.side")
-	guard = GetString("savegame.mod.guard")
-	magnifier = GetString("savegame.mod.magnifier")
-	magnified = false
-	magnifierFactor = 1
-	cocksound = LoadSound("MOD/snd/guncock.ogg")
-	reloadsound = LoadSound("MOD/snd/reload.ogg")
-	reloadsound2 = LoadSound("MOD/snd/reload2.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-	selectsound = LoadSound("MOD/snd/selectorswitch.ogg")
-	casingsound = LoadSound("MOD/snd/casingsound.ogg")
-	interactsound1 = LoadSound("MOD/snd/interact1.ogg")
-	interactsound2 = LoadSound("MOD/snd/interact2.ogg")
-	uiselect = LoadSound("MOD/snd/uiselect.ogg")
-
-	reloadTime = 2.2
-	shotDelay = 0.08
-	burstammo = 2
-	spreadTimer = 1.25
-	spreadFactor = 1.5
-	accuracyFactor = 1
-	bipodFactor = 1
-	if not realistic then
-		if mag == "" then
-			magsize = 30
-			reloadFactor = 1.1
-		elseif mag == "mag1" then
-			magsize = 40
-			reloadFactor = 1.3
-		elseif mag == "mag2" then
-			magsize = 50
-			reloadFactor = 1.5
-		elseif mag == "mag3" then
-			magsize = 100
-			reloadFactor = 1.6
-		else
-			magsize = 20
-			reloadFactor = 1
-		end
-		ammo = magsize
-	else
-		ammo = magtable2[curmagslot][2]
-	end
-	barrellength = 0
-	guardlength = 0
-	barrelFactorx = 0.8
-	barrelFactory = 1
-	barrelFactordamage = 1.15
-	grenadelauncherammo = 1
-	reloading = false
-	ironsight = false
-	ADSx = 0
-	ADSy = 0
-	ADSz = 0
-	ADSrotx = 0
-	ADSroty = 0
-	ADSrotz = 0
-	ADSx0 = 0
-	ADSy0 = 0
-	ADSz0 = 0
-	ADSrotx0 = 0
-	ADSroty0 = 0
-	ADSrotz0 = 0
-	ADSdelta = {0,0,0,0,0,0}
-	ADSfov = 0
-	RELx = 0
-	RELy = 0
-	RELz = 0
-	RELrotx = 0
-	RELroty = 0
-	RELrotz = 0
-	SELx = 0
-	SELy = 0
-	SELz = 0
-	SELrotx = 0
-	SELroty = 0
-	SELrotz = 0
-	INSx = 0
-	INSy = 0
-	INSz = 0
-	INSrotx = 0
-	INSroty = 0
-	INSrotz = 0
-	RECx = 0
-	RECy = 0
-	RECz = 0
-	RECrotx = 0
-	RECroty = 0
-	RECrotz = 0
-	RECx0 = 0
-	RECy0 = 0
-	RECz0 = 0
-	RECrotx0 = 0
-	RECroty0 = 0
-	RECrotz0 = 0
-	RECdelta = {0,0,0,0,0,0}
-	crouchoffset = 0
-	sideattachment = false
-	range = 0
-	grenadelauncher = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	spentcasingsoption = GetBool("savegame.mod.spentcasingsoption")
-
-	for i=1, 200 do
-		ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
-	end
-	for i=1, 10 do
-		ak47grenadeHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
-	end
-
-	shootTimer = 0
-	reloadTimer = 0
-	recoilTimer = 0
-	recoilAngle = 0
-	recoilFactor = 0
-	stockFactor = 0
-	muzzleFactor = 0
-	muzzlelength = 0
-	gripfactorx = 0
-	gripfactory = 0
-	lightFactor = 1
-	recoilMax = 0
-	rnd1, rnd2, rnd3, rnd4, rnd5, rnd6 = 0, 0, 0, 0, 0, 0
-	lightTimer = 0
-	clickedmag = false
-	animationTimers = {0, 0, 0, 0, 0}
-	fovTimer = 0
-	animation1Timer = 0
-	optionsrotx = -50
-	optionsroty = 0
-	optionszoom = 0
-	optionsx = 0
-
-	magoutTimer = 0
-	maginTimer = 0
-	meleeTimer = 0
-	magcheckTimer = 0
-	selecttextTimer = 0
-	cocksoundplaying = false
-	reloadsound2playing = true
-	selectsoundplaying = false
-	selectattachments = false
-	selectmag = false
-	jammed = false
-	jamclearTimer = 0
-	selectattachmentsTimer = 0
-	selectattachmentsTimer = 0
-	inspectTimer = 0
-	heldrTimer = 0
-	scopeTimer = 0
-
-	e = false
-	q = false
-	altaim = false
-	switchsights = false
-	selectfire = 1
-	selectfire0 = 0
-	selectfireTimer = 0
-	selectfireText = "Semi"
-
-	sin1 = 0
-	cos1 = 1
-	sin2 = 0
-	cos2 = 1
-	swayx = 0
-	swayy = 0
-	swingx = 0
-	swingy = 0
-	swingx2 = 0
-	swingy2 = 0
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -396,13 +70,13 @@
 	loadedShell.predictedBulletVelocity = VecAdd(loadedShell.predictedBulletVelocity, Vec((math.random()-0.5)*accuracyFactor*2, (math.random()-0.5)*accuracyFactor*2, (math.random()-0.5)*accuracyFactor*2))
 
 	local barrelend = barrellength + muzzlelength
-	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 2), GetPlayerVelocity()), 0.2, 0.3)
+	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 2), GetPlayerVelocity(playerId)), 0.2, 0.3)
 	ParticleType("plain")
 	ParticleTile(5)
 	ParticleColor(1, 0.6, 0.4, 1, 0.3, 0.2)
 	ParticleRadius(0.2)
 	ParticleEmissive(5, 1)
-	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 4), GetPlayerVelocity()), shotDelay/2, 0.3)
+	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 4), GetPlayerVelocity(playerId)), shotDelay/2, 0.3)
 	ParticleReset()
 	ParticleType("plain")
 	ParticleTile(6)
@@ -414,14 +88,14 @@
 	ParticleGravity(-10)
 	ParticleCollide(0)
 	for i = 1, math.random(8, 16) do
-		SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecAdd(VecScale(dir, 25), GetPlayerVelocity()), Vec((math.random(-100,100)/100)*4,(math.random(-100,100)/100)*4, (math.random(-100,100)/100)*4)), shotDelay)
+		SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecAdd(VecScale(dir, 25), GetPlayerVelocity(playerId)), Vec((math.random(-100,100)/100)*4,(math.random(-100,100)/100)*4, (math.random(-100,100)/100)*4)), shotDelay)
 	end
 	if muzzle == "muzzle1" then
-		PlaySound(suppressedgunsound, GetPlayerTransform().pos, 0.75, false)
+		PlaySound(suppressedgunsound, GetPlayerTransform(playerId).pos, 0.75, false)
 	elseif muzzle == "muzzle2" then
-		PlaySound(gunsound, GetPlayerTransform().pos, 0.65, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.65, false)
 	else
-		PlaySound(gunsound, GetPlayerTransform().pos, 0.55, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.55, false)
 	end
 
 	if not unlimitedammo then
@@ -446,22 +120,23 @@
 		SpentCasing()
 	end
 	local jamrate = 1/400
-	if realistic and math.random() < jamrate and ammo > 0 then
+	if realistic and math.random() < jamrate and ammo ~= 0 then
 		jammed = true
-		PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
+		PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
 	end
 	
-	local pvel = GetPlayerVelocity()
-	local prot = QuatToEuler(GetPlayerTransform(true).rot)
-	local ppos = GetPlayerTransform().pos
-	local camrot = QuatToEuler(GetPlayerCameraTransform().rot)
+	local pvel = GetPlayerVelocity(playerId)
+	local prot = QuatToEuler(GetPlayerTransform(playerId, true).rot)
+	local ppos = GetPlayerTransform(playerId).pos
+	local camrot = QuatToEuler(GetPlayerCameraTransform(playerId).rot)
 	local ppos2 = Transform()
 	ppos2.rot = QuatEuler(prot[1], camrot[2], camrot[3])
 	ppos2.rot = QuatRotateQuat(ppos2.rot, QuatEuler(recoilFactor*muzzleFactor*gripfactory*barrelFactory/2-rnd4/16, -rnd5/16, 0))
 	ppos2.pos = ppos
-	--SetPlayerTransform(ppos2, true)
-	--SetPlayerVelocity(pvel)
+	--SetPlayerTransform(playerId, ppos2, true)
+	--SetPlayerVelocity(playerId, pvel)
 end
+
 function QuatToEuler(quat)
 	local euler={}
 	local x,y,z=GetQuatEuler(quat)
@@ -495,7 +170,7 @@
 	ak47grenadeHandler.shellNum = (ak47grenadeHandler.shellNum%#ak47grenadeHandler.shells) + 1
 
 	SpawnParticle("fire", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(grenadelaunchersound, GetPlayerTransform().pos, 0.75, false)
+	PlaySound(grenadelaunchersound, GetPlayerTransform(playerId).pos, 0.75, false)
 
 	if not unlimitedammo then
 		grenadelauncherammo = grenadelauncherammo - 1
@@ -591,7 +266,7 @@
 
 			local factor = barrelFactordamage
 
-			if projectile.momentum > 0 then
+			if projectile.momentum ~= 0 then
 				MakeHole(hitPos, damage*factor, damage*0.85*factor, damage*0.7*factor)
 			end
 		end
@@ -651,7 +326,7 @@
 			curmagslot = nextmagslot
 		end
 		magoutTimer = 0.6
-		PlaySound(reloadsound, GetPlayerTransform().pos, 0.5, false)
+		PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.5, false)
 	end
 end
 
@@ -681,7 +356,7 @@
 		end
 	elseif bool and animationTimer > animationTime then
 		animationTimer = animationTimer*0.9 - dt/20
-	elseif not bool and fovTimer > 0 then
+	elseif not bool and fovTimer ~= 0 then
 		animationTimer = animationTimer*0.9 - dt/20
 		if animationTimer < 0 then
 			animationTimer = 0
@@ -710,7 +385,7 @@
 	local gt = GetBodyTransform(GetToolBody())
 	local casingpos = TransformToParentPoint(gt, Vec(0.65, -0.6, -1.15))
 	local fwdpos = TransformToParentPoint(gt, Vec(6+math.random()*4, 0.5+math.random()*4, -0.65+math.random()*4))
-	local direction = VecAdd(GetPlayerVelocity(), VecSub(fwdpos, casingpos))
+	local direction = VecAdd(GetPlayerVelocity(playerId), VecSub(fwdpos, casingpos))
 	casing = Spawn("MOD/vox/casing.xml", Transform(casingpos, QuatEuler(math.random(0, 90), math.random(0, 90), math.random(0, 90))))
 	SetBodyVelocity(casing[1], direction)
 end
@@ -765,17 +440,17 @@
 		UiImageBox("ui/common/box-outline-6.png",ww,wh,6,6)
 		if UiImageButton("MOD/icon/"..itemID..".png")then
 			clicked=true
-			PlaySound(uiselect, GetPlayerTransform().pos, 1)
+			PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
 			if item == itemID then
-				SetString("savegame.mod."..itemType, "")
+				SetString("savegame.mod."..itemType, "", true)
 			else
-				SetString("savegame.mod."..itemType, itemID)
+				SetString("savegame.mod."..itemType, itemID, true)
 			end
 		end
 		if wantHint then
 			hoverindex=hoverindex+1
 			local hover,x,y=hovering(ww,wh,hoverindex)
-			if hover > 0 then
+			if hover ~= 0 then
 				hint=true
 				info={location[1],location[2],ww,wh,hover,x,y,Description}
 			else
@@ -804,13 +479,13 @@
 		UiImageBox("ui/common/box-outline-6.png",ww,wh,6,6)
 		if UiImageButton("MOD/icon/"..curmagslot0..".png")then
 			clicked=true
-			PlaySound(uiselect, GetPlayerTransform().pos, 1)
+			PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
 			nextmagslot = itemID
 		end
 		if wantHint then
 			hoverindex=hoverindex+1
 			local hover,x,y=hovering(ww,wh,hoverindex)
-			if hover > 0 then
+			if hover ~= 0 then
 				hint=true
 				info={location[1],location[2],ww,wh,hover,x,y,Description}
 			else
@@ -845,7 +520,7 @@
 		end
 		UiImageBox("ui/common/box-solid-shadow-50.png",120,120,6,6)
 
-		local ppos=GetPlayerTransform(GetToolBody())
+		local ppos=GetPlayerTransform(playerId, GetToolBody())
 		order = 1-order
 		location2 = TransformToParentPoint(ppos, Vec(optionsx*3+math.sin(order*math.pi*1.5-math.pi*1.66)*3, 1-math.cos(order*math.pi*1.5-math.pi*1.66)*2, -5))
 		DebugLine(location, location2, 1, 1, 1, 1)
@@ -856,11 +531,11 @@
 		UiImageBox("ui/common/box-outline-6.png",ww,wh,6,6)
 		if UiImageButton("MOD/icon/"..itemSelected..".png",ww,wh)then
 			clicked=true
-			PlaySound(uiselect, GetPlayerTransform().pos, 1)
+			PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
 			if item == itemID then
-				SetString("savegame.mod."..itemType, "")
+				SetString("savegame.mod."..itemType, "", true)
 			else
-				SetString("savegame.mod."..itemType, itemID)
+				SetString("savegame.mod."..itemType, itemID, true)
 			end
 		end
 	UiPop()
@@ -981,6 +656,7 @@
 			laserFactor = 1
 		end
 end
+
 function Flashlight(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.275, -0.5, -1.9))
@@ -999,6 +675,7 @@
 			SetShapeEmissiveScale(side2, 0)
 		end
 end
+
 function Rangefinder(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.175, -0.625, -1.9))
@@ -1075,27 +752,27 @@
 	-- 	elseif ADSy < 0.2 then
 	-- 		ADSy = ADSy + dt*math.abs((ADSy-0.2)) + ADSdelta[2]*0.7
 	-- 	end
-	-- 	if ADSz > 0 then 
+	-- 	if ADSz ~= 0 then 
 	-- 		ADSz = ADSz - dt*math.abs((ADSz-0)) + ADSdelta[3]*0.7
 	-- 	elseif ADSz < 0 then
 	-- 		ADSz = ADSz + dt*math.abs((ADSz-0)) + ADSdelta[3]*0.7
 	-- 	end
-	-- 	if ADSrotx > 0 then 
+	-- 	if ADSrotx ~= 0 then 
 	-- 		ADSrotx = ADSrotx - dt*math.abs((ADSrotx-0)) + ADSdelta[4]*0.7
 	-- 	elseif ADSrotx < 0 then
 	-- 		ADSrotx = ADSrotx + dt*math.abs((ADSrotx-0)) + ADSdelta[4]*0.7
 	-- 	end
-	-- 	if ADSroty > 0 then 
+	-- 	if ADSroty ~= 0 then 
 	-- 		ADSroty = ADSroty - dt*math.abs((ADSroty-0)) + ADSdelta[5]*0.7
 	-- 	elseif ADSroty < 0 then
 	-- 		ADSroty = ADSroty + dt*math.abs((ADSroty-0)) + ADSdelta[5]*0.7
 	-- 	end
-	-- 	if ADSrotz > 0 then 
+	-- 	if ADSrotz ~= 0 then 
 	-- 		ADSrotz = ADSrotz - dt*math.abs((ADSrotz-0)) + ADSdelta[6]*0.7
 	-- 	elseif ADSrotz < 0 then
 	-- 		ADSrotz = ADSrotz + dt*math.abs((ADSrotz-0)) + ADSdelta[6]*0.7
 	-- 	end
-	-- 	if ADSfov > 0 then 
+	-- 	if ADSfov ~= 0 then 
 	-- 		ADSfov = ADSfov - dt*math.abs((ADSfov-0))
 	-- 	elseif ADSz < 0 then
 	-- 		ADSfov = ADSfov + dt*math.abs((ADSfov-0))
@@ -1159,32 +836,32 @@
 	end
 
 	if not bool then
-		if RELx > 0 then 
+		if RELx ~= 0 then 
 			RELx = RELx - dt*math.abs((RELx-0))
 		elseif RELx < 0 then
 			RELx = RELx + dt*math.abs((RELx-0))
 		end
-		if RELy > 0 then 
+		if RELy ~= 0 then 
 			RELy = RELy - dt*math.abs((RELy-0))
 		elseif RELy < 0 then
 			RELy = RELy + dt*math.abs((RELy-0))
 		end
-		if RELz > 0 then 
+		if RELz ~= 0 then 
 			RELz = RELz - dt*math.abs((RELz-0))
 		elseif RELz < 0 then
 			RELz = RELz + dt*math.abs((RELz-0))
 		end
-		if RELrotx > 0 then 
+		if RELrotx ~= 0 then 
 			RELrotx = RELrotx - dt*math.abs((RELrotx-0))
 		elseif RELrotx < 0 then
 			RELrotx = RELrotx + dt*math.abs((RELrotx-0))
 		end
-		if RELroty > 0 then 
+		if RELroty ~= 0 then 
 			RELroty = RELroty - dt*math.abs((RELroty-0))
 		elseif RELroty < 0 then
 			RELroty = RELroty + dt*math.abs((RELroty-0))
 		end
-		if RELrotz > 0 then 
+		if RELrotz ~= 0 then 
 			RELrotz = RELrotz - dt*math.abs((RELrotz-0))
 		elseif RELrotz < 0 then
 			RELrotz = RELrotz + dt*math.abs((RELrotz-0))
@@ -1236,32 +913,32 @@
 	end
 
 	if not bool then
-		if SELx > 0 then 
+		if SELx ~= 0 then 
 			SELx = SELx - dt*math.abs((SELx-0))
 		elseif SELx < 0 then
 			SELx = SELx + dt*math.abs((SELx-0))
 		end
-		if SELy > 0 then 
+		if SELy ~= 0 then 
 			SELy = SELy - dt*math.abs((SELy-0))
 		elseif SELy < 0 then
 			SELy = SELy + dt*math.abs((SELy-0))
 		end
-		if SELz > 0 then 
+		if SELz ~= 0 then 
 			SELz = SELz - dt*math.abs((SELz-0))
 		elseif SELz < 0 then
 			SELz = SELz + dt*math.abs((SELz-0))
 		end
-		if SELrotx > 0 then 
+		if SELrotx ~= 0 then 
 			SELrotx = SELrotx - dt*math.abs((SELrotx-0))
 		elseif SELrotx < 0 then
 			SELrotx = SELrotx + dt*math.abs((SELrotx-0))
 		end
-		if SELroty > 0 then 
+		if SELroty ~= 0 then 
 			SELroty = SELroty - dt*math.abs((SELroty-0))
 		elseif SELroty < 0 then
 			SELroty = SELroty + dt*math.abs((SELroty-0))
 		end
-		if SELrotz > 0 then 
+		if SELrotz ~= 0 then 
 			SELrotz = SELrotz - dt*math.abs((SELrotz-0))
 		elseif SELrotz < 0 then
 			SELrotz = SELrotz + dt*math.abs((SELrotz-0))
@@ -1313,32 +990,32 @@
 	-- end
 
 	-- if not bool then
-	-- 	if INSx > 0 then 
+	-- 	if INSx ~= 0 then 
 	-- 		INSx = INSx - dt*math.abs((INSx-0))
 	-- 	elseif INSx < 0 then
 	-- 		INSx = INSx + dt*math.abs((INSx-0))
 	-- 	end
-	-- 	if INSy > 0 then 
+	-- 	if INSy ~= 0 then 
 	-- 		INSy = INSy - dt*math.abs((INSy-0))
 	-- 	elseif INSy < 0 then
 	-- 		INSy = INSy + dt*math.abs((INSy-0))
 	-- 	end
-	-- 	if INSz > 0 then 
+	-- 	if INSz ~= 0 then 
 	-- 		INSz = INSz - dt*math.abs((INSz-0))
 	-- 	elseif INSz < 0 then
 	-- 		INSz = INSz + dt*math.abs((INSz-0))
 	-- 	end
-	-- 	if INSrotx > 0 then 
+	-- 	if INSrotx ~= 0 then 
 	-- 		INSrotx = INSrotx - dt*math.abs((INSrotx-0))
 	-- 	elseif INSrotx < 0 then
 	-- 		INSrotx = INSrotx + dt*math.abs((INSrotx-0))
 	-- 	end
-	-- 	if INSroty > 0 then 
+	-- 	if INSroty ~= 0 then 
 	-- 		INSroty = INSroty - dt*math.abs((INSroty-0))
 	-- 	elseif INSroty < 0 then
 	-- 		INSroty = INSroty + dt*math.abs((INSroty-0))
 	-- 	end
-	-- 	if INSrotz > 0 then 
+	-- 	if INSrotz ~= 0 then 
 	-- 		INSrotz = INSrotz - dt*math.abs((INSrotz-0))
 	-- 	elseif INSrotz < 0 then
 	-- 		INSrotz = INSrotz + dt*math.abs((INSrotz-0))
@@ -1390,32 +1067,32 @@
 	-- end
 
 	-- if not bool then
-	-- 	if RECx > 0 then 
+	-- 	if RECx ~= 0 then 
 	-- 		RECx = RECx - dt*math.abs((RECx-0))/16
 	-- 	elseif RECx < 0 then
 	-- 		RECx = RECx + dt*math.abs((RECx-0))/16
 	-- 	end
-	-- 	if RECy > 0 then 
+	-- 	if RECy ~= 0 then 
 	-- 		RECy = RECy - dt*math.abs((RECy-0))/16
 	-- 	elseif RECy < 0 then
 	-- 		RECy = RECy + dt*math.abs((RECy-0))/16
 	-- 	end
-	-- 	if RECz > 0 then 
+	-- 	if RECz ~= 0 then 
 	-- 		RECz = RECz - dt*math.abs((RECz-0))/16
 	-- 	elseif RECz < 0 then
 	-- 		RECz = RECz + dt*math.abs((RECz-0))/16
 	-- 	end
-	-- 	if RECrotx > 0 then 
+	-- 	if RECrotx ~= 0 then 
 	-- 		RECrotx = RECrotx - dt*math.abs((RECrotx-0))/16
 	-- 	elseif RECrotx < 0 then
 	-- 		RECrotx = RECrotx + dt*math.abs((RECrotx-0))/16
 	-- 	end
-	-- 	if RECroty > 0 then 
+	-- 	if RECroty ~= 0 then 
 	-- 		RECroty = RECroty - dt*math.abs((RECroty-0))/16
 	-- 	elseif RECroty < 0 then
 	-- 		RECroty = RECroty + dt*math.abs((RECroty-0))/16
 	-- 	end
-	-- 	if RECrotz > 0 then 
+	-- 	if RECrotz ~= 0 then 
 	-- 		RECrotz = RECrotz - dt*math.abs((RECrotz-0))/16
 	-- 	elseif RECrotz < 0 then
 	-- 		RECrotz = RECrotz + dt*math.abs((RECrotz-0))/16
@@ -1454,1889 +1131,12 @@
 		checkammotext = "Just Over Half Full"
 	elseif percentage > 0.25 then
 		checkammotext = "Just Under Half Full"
-	elseif percentage > 0 then
+	elseif percentage ~= 0 then
 		checkammotext = "Nearly Empty"
 	else
 		checkammotext = "Empty"
 	end
 	return checkammotext
-end
-
-function tick(dt)
-	if GetString("game.player.tool") == "g36k" and GetPlayerVehicle() == 0 then
-		SetBool("hud.aimdot", false)
-
-
-		------CONTROLS------
-		if InputDown("lmb") and not reloading and selectfire == 3 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-			end
-		elseif InputPressed("lmb") and not reloading and selectfire == 1 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-				shootTimer = 0.11
-			end
-		elseif InputDown("lmb") and not reloading and selectfire == 2 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 and burstammo > 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-			end
-		end
-
-		if InputPressed("lmb") and not reloading and not InputDown("shift") and inspectTimer <= 0 then
-			spreadTimer = 1.25
-			if (ammo == 0 or selectfire == 0) and not selectattachments then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			end
-		end
-
-		if InputReleased("lmb") and not reloading and selectfire > 0 then
-			shootTimer = 0
-			burstammo = 2
-		end
-
-		
-		if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and GetPlayerGrabShape() == 0 and not InputDown("shift") then
-			if InputPressed("rmb") then
-				PlaySound(interactsound1, GetPlayerTransform().pos, 1)
-			end
-			ironsight = true
-			inspectTimer = 0
-			if scopeTimer < 0.5 and not reloading and not (q or e) and selectfireTimer == 0 and not (altaim and toprail == "scope2") and not switchsights and not InputDown("shift") then
-				scopeTimer = scopeTimer + dt
-			end
-		end
-		if not InputDown("rmb") then
-			ironsight = false
-		end
-		if selectfire == 0  and selectfireTimer <= 0 then
-			ironsight = false
-		end
-		if (not InputDown("rmb") or reloading or q or e or selectfireTimer > 0 or (altaim and toprail == "scope2") or switchsights or InputDown("shift")) and scopeTimer > 0 then scopeTimer = scopeTimer - dt end
-
-
-		if InputPressed("e") then
-			e = not e
-			q = false
-		end
-
-		if InputPressed("q") then
-			q = not q
-			e = false
-		end
-
-		if InputPressed("c") then
-			switchsights = not switchsights
-		end
-		-- if canted == "" then
-		-- 	switchsights = false
-		-- end
-
-		if InputPressed("x") and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") then
-			meleeTimer = 0.8
-			inspectTimer = 0
-		end
-
-		if InputPressed("v") and not reloading and not selectattachments and not selectmag and magcheckTimer == 0 and jamclearTimer == 0 then
-			SelectFire()
-			inspectTimer = 0
-			selecttextTimer = 3
-		end
-		if selecttextTimer > 0 then
-			selecttextTimer = selecttextTimer - dt
-		end
-		if selecttextTimer < 0 then
-			selecttextTimer = 0
-		end
-
-		if InputDown("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 and not realistic or GetBool("level.optionstriggered") then
-			if InputPressed("t") and not GetBool("level.optionstriggered") then
-				PlaySound(interactsound2, GetPlayerTransform().pos, 1)
-				selectattachmentsTimer = 0.5
-			end
-			UiMakeInteractive()
-			selectattachments = true
-			ironsight = false
-			inspectTimer = 0
-		end
-		if InputReleased("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and not realistic then
-			selectattachments = false
-			selectattachmentsTimer = 0.25
-		end
-
-		if InputPressed("b") and side ~= "" then
-			sideattachment = not sideattachment
-			PlaySound(uiselect, GetPlayerTransform().pos, 0.75)
-		end
-		Laser(sideattachment and side == "side1")
-		Flashlight(sideattachment and side == "side2")
-		Rangefinder(sideattachment and side == "side3")
-
-		if InputPressed("h") and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 then
-			magcheckTimer = 4
-			PlaySound(reloadsound, GetPlayerTransform().pos, 0.5)
-			inspectTimer = 0
-		end
-		if magcheckTimer > 0 then
-			magcheckTimer = magcheckTimer - dt
-			ironsight = false
-		end
-		if magcheckTimer < 0 then
-			magcheckTimer = 0
-			PlaySound(reloadsound2, GetPlayerTransform().pos, 0.5)
-		end
-
-		if InputDown("r") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then heldrTimer = heldrTimer + dt end
-		if InputDown("r") and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 and heldrTimer > 0.2 then
-			UiMakeInteractive()
-			selectmag = true
-			ironsight = false
-		else
-			selectmag = false
-		end
-		if InputReleased("r") and heldrTimer <= 0.2 and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
-			for i = 1, totalmags do
-				if magtable2[i][2]/magtable2[i][3] > 0.4 and i ~= curmagslot and curmagslot == nextmagslot then
-					nextmagslot = i
-				end
-			end
-			inspectTimer = 0
-			Reload()
-		end
-		if InputReleased("r") then heldrTimer = 0 end
-
-		if InputPressed("r") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jammed and jamclearTimer == 0 then
-			jamclearTimer = 2
-		end
-		if jamclearTimer > 0 then
-			jamclearTimer = jamclearTimer - dt
-			ironsight = false
-		end
-		if jamclearTimer < 0 then
-			jamclearTimer = 0
-			jammed = false
-			cocksoundplaying = false
-		end
-		if InputDown("shift") then
-			ironsight = false
-			selectattachments = false
-			inspectTimer = 0
-		end
-
-		if grip == "grenade_launcher" then
-			if InputPressed("c") and not reloading then
-				grenadelauncher = not grenadelauncher
-			end
-		else
-			grenadelauncher = false
-		end
-
-		if InputPressed("y") and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire > 0 and not selectattachments then
-			if inspectTimer <= 0 then
-				inspectTimer = 6
-				ironsight = false
-			else
-				inspectTimer = 0
-			end
-		end
-
-		if InputPressed("alt") and magnifier == "g33" then
-			magnified = not magnified
-			PlaySound(uiselect, GetPlayerTransform().pos, 1)
-		elseif magnifier == "" then
-			magnified = false
-		end
-		if magnified and not switchsights then
-			magnifierFactor = 3
-		else
-			magnifierFactor = 1
-		end
-
-		if selectfire == 3 then
-			selectfireText = "Full"
-		elseif selectfire == 1 then
-			selectfireText = "Semi"
-		elseif selectfire == 2 then
-			selectfireText = "Burst"
-		else
-			selectfireText = "Safe"
-		end
-
-		if shootTimer <= 0 then
-			recoverySpeed = 0.085
-			if recoilAngle > 0 then
-				recoilAngle = recoilAngle - (recoilAngle-0.25)*recoverySpeed
-			elseif recoilAngle < 0 then
-				recoilAngle = 0
-			end
-			if math.abs(rnd1) < 0.05 then
-				rnd1 = 0
-			elseif rnd1 > 0 then
-				rnd1 = rnd1 - (rnd1+0.25)*recoverySpeed
-			elseif rnd1 < 0 then
-				rnd1 = rnd1 - (rnd1-0.25)*recoverySpeed
-			end
-			if math.abs(rnd2) < 0.05 then
-				rnd2 = 0
-			elseif rnd2 > 0 then
-				rnd2 = rnd2 - (rnd2+0.25)*recoverySpeed
-			elseif rnd2 < 0 then
-				rnd2 = rnd2 - (rnd2-0.25)*recoverySpeed
-			end
-			if math.abs(rnd3) < 0.05 then
-				rnd3 = 0
-			elseif rnd3 > 0 then
-				rnd3 = rnd3 - (rnd3+0.25)*recoverySpeed
-			elseif rnd3 < 0 then
-				rnd3 = rnd3 - (rnd3-0.25)*recoverySpeed
-			end
-			if math.abs(rnd4) < 0.05 then
-				rnd4 = 0
-			elseif rnd4 > 0 then
-				rnd4 = rnd4 - (rnd4+0.25)*recoverySpeed
-			elseif rnd4 < 0 then
-				rnd4 = rnd4 - (rnd4-0.25)*recoverySpeed
-			end
-			if math.abs(rnd5) < 0.05 then
-				rnd5 = 0
-			elseif rnd5 > 0 then
-				rnd5 = rnd5 - (rnd5+0.25)*recoverySpeed
-			elseif rnd5 < 0 then
-				rnd5 = rnd5 - (rnd5-0.25)*recoverySpeed
-			end
-			if math.abs(rnd6) < 0.05 then
-				rnd6 = 0
-			elseif rnd6 > 0 then
-				rnd6 = rnd6 - (rnd6+0.25)*recoverySpeed
-			elseif rnd6 < 0 then
-				rnd6 = rnd6 - (rnd6-0.25)*recoverySpeed
-			end
-		end
-
-		if ironsight then
-			recoilFactor = 0.8*stockFactor
-		else
-			recoilFactor = 1.6*stockFactor
-		end
-
-		if ironsight then
-			recoilMax = 12*muzzleFactor*gripfactory*barrelFactory*stockFactor
-		else
-			recoilMax = 25*muzzleFactor*gripfactory*barrelFactory*stockFactor
-		end
-
-		if toprail == "scope" and not (q or e) then
-			spreadFactor = 1
-		elseif toprail == "holo" and not (q or e) then
-			spreadFactor = 1.75
-		else
-			spreadFactor = 2
-		end
-
-		toprail = GetString("savegame.mod.toprail")
-		muzzle = GetString("savegame.mod.muzzle")
-		stock = GetString("savegame.mod.stock")
-		foldstock = GetString("savegame.mod.foldstock")
-		if realistic then
-			if maginTimer > 0 then
-				mag = magtable2[curmagslot][1]
-			end
-		else
-			if maginTimer > 0 then
-				mag = GetString("savegame.mod.mag")
-			end
-		end
-		if GetBool("level.optionstriggered") then
-			if realistic then
-				mag = magtable[1] or ""
-			else
-				mag = GetString("savegame.mod.mag")
-			end
-		end
-		grip = GetString("savegame.mod.grip")
-		barrel = GetString("savegame.mod.barrel")
-		side = GetString("savegame.mod.side")
-		guard = GetString("savegame.mod.guard")
-		magnifier = GetString("savegame.mod.magnifier")
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local magoffset = Vec(0, 0, 0)
-			local grenadeoffset = Vec(-0.025, 0.025, 0)
-			local boltoffset = Vec(-0.025, 0, 0)
-			local selectoroffset = Transform()
-			local suppressoroffset = Transform()
-			local scopeoffset = Transform()
-			local holooffset = Transform()
-			local holooffset2 = Transform()
-			local railoffset = Transform()
-			local magtimer = magoutTimer + maginTimer
-			offset = Transform(Vec(0, heightOffset, 0))
-			local adsFOV, adsTime = 0, 0
-			local defaultTrans = Transform(Vec(0.25, 0.15, 0.25), QuatEuler(0, 0, 0))
-
-			x,y,z,rotx,roty,rotz = -0.1,0.2,0,0,0,0
-			if ironsight then
-			if grenadelauncher then
-				x = 0
-				y = 0.45
-				z = 0.25
-				rotz = 0
-			elseif q then
-				x = 0.9
-				y = 0.1
-				z = 0.3
-				rotz = 30
-			elseif e then
-				x = -0.3
-				y = 0.3
-				z = 0.1
-				rotz = -15
-			else
-				--if canted == "sight5" and switchsights then
-				if switchsights and not reloading then
-					x = 0.55
-					y = 0.05
-					z = 0.2
-					rotz = 20
-				elseif toprail == "holo" then
-					x = 0.275
-					y = 0.2125
-					z = 0.15
-					rotz = 0
-				elseif toprail == "" then
-					x = 0.275
-					y = 0.3
-					z = 0.15
-					rotz = 0
-				elseif toprail == "scope" then
-					x = 0.275
-					y = 0.175
-					z = 0.15
-					rotz = 0
-				elseif toprail == "sight3" then
-					x = 0.275
-					y = 0.1625
-					z = 0.2
-					rotz = 0.1
-				end
-			end
-
-			if reloading then
-				adsFOV, adsTime = 0, 0.15
-			elseif not (q or e or grenadelauncher) then
-				if switchsights then
-					adsFOV, adsTime = 10, 0.15
-				elseif toprail == "" then
-					adsFOV, adsTime = 10, 0.15
-				elseif toprail == "scope" then
-					adsFOV, adsTime = 80, 0.25
-				elseif toprail == "holo" then
-					adsFOV, adsTime = 20, 0.1
-				end
-			elseif grenadelauncher then
-				adsFOV, adsTime = 10, 0.15
-			else
-				adsFOV, adsTime = 0, 0.15
-			end
-			end
-
-			--offset = ADS(ironsight, adsFOV*magnifierFactor, adsTime, -x, y, z, rotz)
-
-			local limit = 10
-			if ironsight then limit = 45 end
-			-- if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and ironsight then swingx2 = math.clamp(swingx2 - InputValue("mousedx")/10, -limit, limit) end
-			if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and not ironsight then swingx2 = math.clamp(swingx2 + InputValue("mousedx")/40, -limit, limit) end
-			if swingx2 > 0 and ironsight then
-				swingx2 = swingx2 - swingx2*0.32
-			elseif swingx2 < 0 and ironsight then
-				swingx2 = swingx2 - swingx2*0.32
-			end
-			-- if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and ironsight then swingy2 = math.clamp(swingy2 - InputValue("mousedy")/10, -limit, limit) end
-			if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and not ironsight then swingy2 = math.clamp(swingy2 + InputValue("mousedy")/40, -limit, limit) end
-			if swingy2 > 0 and ironsight then
-				swingy2 = swingy2 - swingy2*0.32
-			elseif swingy2 < 0 and ironsight then
-				swingy2 = swingy2 - swingy2*0.32
-			end
-
-			if ironsight then
-				btrans = GetBodyTransform(b)
-				if toprail == "holo" then
-					local gt = GetBodyTransform(GetToolBody())
-					local sightcenter = Vec(0.275, -0.2125, -1.15)
-					local gunpos = TransformToParentPoint(gt, sightcenter)
-					local fwdpos = TransformToParentVec(gt, Vec(0, 0, -1))
-					local hit, dist = QueryRaycast(gunpos, fwdpos, 500, 0, true)
-					local hitpoint = VecAdd(gunpos, VecScale(fwdpos, dist))
-
-					local camtrans = GetPlayerCameraTransform()
-					local sightdist = VecLength(VecSub(camtrans.pos, gunpos))
-
-					local holopoint = VecAdd(camtrans.pos, VecScale(VecNormalize(VecSub(camtrans.pos, hitpoint)), -sightdist))
-
-					local holotrans = Transform(holopoint, QuatLookAt(camtrans.pos, hitpoint))
-
-					if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.08 then
-						reticle1 = LoadSprite("MOD/img/reticle1.png")
-						DrawSprite(reticle1, Transform(VecAdd(holotrans.pos, VecScale(GetPlayerVelocity(), 0.045)), holotrans.rot), 0.025, 0.025, 1, 1, 1, 1, true)
-					end
-				end
-				if toprail == "sight3" then
-					local gt = GetBodyTransform(GetToolBody())
-					local sightcenter = Vec(0.275, -0.2125+0.05, -1.2+0.05)
-					local gunpos = TransformToParentPoint(gt, sightcenter)
-					local fwdpos = TransformToParentVec(gt, Vec(0, 0, -1))
-					local hit, dist = QueryRaycast(gunpos, fwdpos, 500, 0, true)
-					local hitpoint = VecAdd(gunpos, VecScale(fwdpos, dist))
-
-					local camtrans = GetPlayerCameraTransform()
-					local sightdist = VecLength(VecSub(camtrans.pos, gunpos))
-
-					local holopoint = VecAdd(camtrans.pos, VecScale(VecNormalize(VecSub(camtrans.pos, hitpoint)), -sightdist))
-
-					local holotrans = Transform(holopoint, QuatLookAt(camtrans.pos, hitpoint))
-
-					if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.1 then
-						reticle4 = LoadSprite("MOD/img/reticle4.png")
-						DrawSprite(reticle4, holotrans, 0.2, 0.15, 1, 1, 1, 1, true)
-					end
-				end
-			end
-
-			local speed = math.clamp(VecLength(GetPlayerVelocity()), 0, 10)
-			sin1 = math.clamp(sin1 + cos1*dt*speed*2.8, -1.2, 1.2)
-			cos1 = math.clamp(cos1 - sin1*dt*speed*2.8, -1.2, 1.2)
-			sin2 = math.clamp(sin2 + cos2*dt*speed*0.7, -1.2, 1.2)
-			cos2 = math.clamp(cos2 - sin2*dt*speed*0.7, -1.2, 1.2)
-			swayy = sin1/3
-			swayx = sin2/2
-			-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(swayy*speed, swayx*speed, 0))
-			-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(math.sin(2.1*GetTime())/9*bipodFactor^4,  math.sin(1.3*GetTime())/6*bipodFactor^4, 0))
-			-- offset.pos = VecAdd(offset.pos, Vec(math.sin(1.1*GetTime())/360*bipodFactor^4,  math.sin(0.7*GetTime())/240*bipodFactor^4, 0))
-
-			if meleeTimer > 0 then
-				if meleeTimer > 0.6 then
-					offset.rot = QuatEuler(0, (0.8-meleeTimer)*800, (0.8-meleeTimer)*50)
-					offset.pos = VecAdd(offset.pos, Vec((0.8-meleeTimer)*1, (0.8-meleeTimer)*-1, (0.8-meleeTimer)*-7.5))
-				elseif meleeTimer > 0.4 then
-					offset.rot = QuatEuler(0, 160, 0)
-					offset.pos = VecAdd(offset.pos, Vec(0.4+(meleeTimer-0.4)*1.5, 0, -2.5+(meleeTimer-0.4)*-1.5))
-					stockPos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0, -0.5, -0.65))
-					if meleeTimer > 0.55 then
-						if GetShapeMaterialAtPosition(shape, stockPos) == "glass" then
-							MakeHole(stockPos, 2)
-						else
-							MakeHole(stockPos, 0.3)
-						end
-					end
-				else
-					offset.rot = QuatEuler(0, meleeTimer*400, meleeTimer*100)
-					offset.pos = VecAdd(offset.pos, Vec(0, 0, meleeTimer*-5))
-				end
-
-				meleeTimer = meleeTimer - dt
-			end
-
-			if selectfireTimer > 0 then
-				selectfireTimer = selectfireTimer - dt
-			end
-
-			if inspectTimer > 0 then
-				inspectTimer = inspectTimer - dt
-			end
-
-			if recoilTimer > 0 then
-				-- offset.pos = VecAdd(offset.pos, Vec(0, 0, recoilTimer/2))
-				-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer)*10, 0, 0))
-				
-				recoilTimer = recoilTimer - dt
-				boltoffset = Vec(-0.025, 0, recoilTimer*6)
-			end
-			local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/400, (recoilAngle/-200)-(rnd1+rnd4)/400-recoilTimer/2, recoilAngle/125+recoilTimer, recoilAngle+(rnd1+rnd4)/4+recoilTimer*16, (rnd2+rnd5)/4, (rnd3+rnd6)/4
-			-- RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
-			-- offset.pos = VecAdd(offset.pos, RECoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, RECoffset.rot)
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 0.75, 0.25, (lightTimer/shotDelay)*lightFactor)
-				lightTimer = lightTimer - dt
-			end
-
-			if magoutTimer < 0 then
-				maginTimer = 0.6
-				magoutTimer = 0
-				reloadsound2playing = false
-				PlaySound(interactsound1, GetPlayerTransform().pos, 1, false)
-			end
-			if maginTimer < 0 then
-				maginTimer = 0
-				if grenadelauncher then
-					PlaySound(uiselect, GetPlayerTransform().pos, 1)
-				end
-			end
-			if maginTimer < 0.25 and not reloadsound2playing and not grenadelauncher then
-					PlaySound(reloadsound2, GetPlayerTransform().pos, 0.6, false)
-					reloadsound2playing = true
-			end
-			if magoutTimer > 0 then
-				if grenadelauncher then
-					grenadeoffset = Vec(-0.025, -magoutTimer*3+0.025, -0.6)
-				else
-					magoffset = Vec(0, -(0.6-magoutTimer)*4, 0)
-				end
-				magoutTimer = magoutTimer - dt/reloadFactor
-			end
-			if maginTimer > 0 then
-				if grenadelauncher then
-					grenadeoffset = Vec(-0.025, 0.025, -maginTimer)
-				else
-					magoffset = Vec(0, -maginTimer*4, 0)
-				end
-				maginTimer = maginTimer - dt/reloadFactor
-			end
-			if not grenadelauncher or (grenadelauncherammo == 0 and not reloading) then
-				grenadeoffset = Vec(0, 0, 1000)
-			end
-
-			local x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 0, 0, 0
-			if reloading then
-			if grenadelauncher then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 5, -10
-			elseif ironsight then
-				if q then
-					if magoutTimer > 0 or magcheckTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.1, 0, -5, 10, -10
-					elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, 0.05, 0, -5, 10, 0
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = -0.1, -0.05, 0, 5, -15, -5
-					end
-				elseif e then
-					if magoutTimer > 0 or magcheckTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 10, -10
-					elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.075, -0.125, 0.05, 5, 5, -5
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = -0.4, -0.15, 0.05, 10, 0, 10
-					end
-				else
-					if magoutTimer > 0 or magcheckTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.35, -0.025, -0.1, 0, 0, -25
-					elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) or (reloadTimer > 0.8 and ammo == 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.35, 0.025, -0.1, 0, 10, -15
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.1, -0.05, -10, 5, 5
-					end
-				end
-			else
-				if magoutTimer > 0.5 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.05, 0, 0, -5, 5, -5
-				elseif magoutTimer > 0 or magcheckTimer > 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.3, 0, 0.1, 5, 20, -15
-				elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) or (reloadTimer > 0.8 and ammo == 0) then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.15, 0.1, 15, 10, -10
-				elseif reloadTimer < 0.8 and ammo == 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, 0.05, 10, 15, -10
-				end
-			end
-			end
-
-			-- RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
-			-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
-
-			if reloadTimer > 0.2 and reloading and ammo == 0 then
-				boltoffset = Vec(-0.025, 0, 0.34)
-			elseif ammo == 0 and not reloading then
-				boltoffset = Vec(-0.025, 0, 0.34)
-			end
-
-			ATToffset = {0,0,0,0,0,0}
-			if not GetBool("level.optionstriggered") then
-			-- if selectattachmentsTimer > 0 and selectattachments then
-			-- 	local t1 = (0.5 - selectattachmentsTimer)/0.5
-			-- 	ATToffset = VecAdd(offset.pos, Vec(1*t1, 0, -0.8*t1*180/GetInt("options.gfx.fov")))
-			-- 	ATToffset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t1, 75*t1, -10*t1))
-			-- elseif selectattachmentsTimer > 0 and not selectattachments then
-			-- 	local t2 = selectattachmentsTimer/0.25
-			-- 	ATToffset.pos = VecAdd(offset.pos, Vec(1*t2, 0, -0.8*t2*180/GetInt("options.gfx.fov")))
-			-- 	ATToffset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t2, 75*t2, -10*t2))
-			-- elseif selectattachments then
-			-- 	ATToffset.pos = VecAdd(offset.pos, Vec(1, 0, -0.8*180/GetInt("options.gfx.fov")))
-			-- 	ATToffset.rot = QuatRotateQuat(offset.rot, QuatEuler(10, 75, -10))
-			-- end
-			if selectattachments then ATToffset = {1,0,-0.8*180/GetInt("options.gfx.fov"),10,75,-10} end
-			end
-			if GetBool("level.optionstriggered") then
-				offset.pos = VecAdd(offset.pos, Vec(optionsx+0.2+math.cos(math.pi*optionsrotx/180), 0.2, -1.5-math.sin(math.pi*optionsrotx/180)+optionszoom))
-				offset.rot = QuatRotateQuat(offset.rot, QuatEuler(0, 100+optionsrotx, optionsroty))
-				
-				if InputValue("mousewheel") > 0 and optionszoom < 1 then
-					optionszoom = optionszoom + 0.05
-				elseif InputValue("mousewheel") < 0 and optionszoom > -2 then
-					optionszoom = optionszoom - 0.05
-				end
-				if InputDown("rmb") and grabbed[1][1] == "" then
-					optionsrotx = optionsrotx + InputValue("mousedx")/2
-				end
-				if InputDown("rmb") and grabbed[1][1] == "" then
-					optionsroty = optionsroty + InputValue("mousedy")/20
-				end
-				if optionsroty > 0.1 then optionsroty = optionsroty - optionsroty*0.05 - 0.05 end
-				if optionsroty < 0.1 then optionsroty = optionsroty - optionsroty*0.05 + 0.05 end
-				if InputDown("lmb") and grabbed[1][1] == "" then
-					optionsx = optionsx + InputValue("mousedx")/400
-				end
-			end
-
-			if selectattachmentsTimer > 0 then
-				selectattachmentsTimer = selectattachmentsTimer*0.9 - dt/20
-			elseif selectattachmentsTimer < 0 then
-				selectattachmentsTimer = 0
-			end
-
-			local x2, y2, z2, rotx2, roty2, rotz2 = 0, 0, 0, 0, 0, 0
-			if inspectTimer > 4 then
-				x2, y2, z2, rotx2, roty2, rotz2 = 1, 0, -0.75, 10, 75, -10
-			elseif inspectTimer > 3 then
-				x2, y2, z2, rotx2, roty2, rotz2 = 1, 0, -0.75, 10, 75, -20
-			elseif inspectTimer > 1.25 then
-				x2, y2, z2, rotx2, roty2, rotz2 = 0.25, -1, 0, 20, 30, 120
-			elseif inspectTimer > 0 then
-				x2, y2, z2, rotx2, roty2, rotz2 = 0.25, -0.25, 0.25, 20, 30, 0
-			elseif jamclearTimer > 0 then
-				x2, y2, z2, rotx2, roty2, rotz2 = 0.2, -0.1, 0.1, 10, 10, -10
-			end
-
-			-- INSoffset = INS(inspectTimer > 0 or jamclearTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
-			-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
-
-			local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 and not reloading then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0.2, 0.2, -0.2, -20, 60, 0
-			elseif ironsight and q and selectfireTimer > 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			elseif ironsight and selectfireTimer > 0  then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0.15, 0, 0, 0, 5, -10
-			elseif selectfireTimer > 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0.4, 0, -0.25, 0, 5, -20
-			else
-				x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			end
-
-			-- if not GetBool("level.optionstriggered") then SELoffset = SEL((selectfireTimer > 0 or selectfire == 0 or InputDown("shift")) and not reloading, x3, y3, z3, rotx3, roty3, rotz3)
-			-- offset.pos = VecAdd(offset.pos, SELoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, SELoffset.rot) end
-
-			offset = ADS(true, adsFOV*magnifierFactor, adsTime, -x+x1+x2+x3+ATToffset[1]-swingx2/100, y+y1+y2+y3+ATToffset[2]+swingy2/100, z+z1+z2+z3+ATToffset[3], rotx+rotx1+rotx2+rotx3+swingy-swingy2+swayy*speed+ATToffset[4], roty+roty1+roty2+roty3+swingx-swingx2+swayx*speed+ATToffset[5], rotz+rotz1+rotz2+rotz3+ATToffset[6])
-
-			RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
-			offset.pos = VecAdd(offset.pos, RECoffset.pos)
-			offset.rot = QuatRotateQuat(offset.rot, RECoffset.rot)
-
-			if InputPressed("mmb") then
-				if clothingtype == "camo" then
-					clothingtype = "swat"
-				elseif clothingtype == "swat" then
-					clothingtype = "camo2"
-				elseif clothingtype == "camo2" then
-					clothingtype = ""
-				else
-					clothingtype = "camo"
-				end
-			end
-			local bs = GetBodyShapes(GetToolBody())
-			for i = 43, 54 do
-				SetShapeLocalTransform(bs[i], hideTrans)
-			end
-			if clothingtype == "camo" then
-				hand1 = bs[46]
-				arm1 = bs[48]
-				hand2 = bs[47]
-			elseif clothingtype == "swat" then
-				hand1 = bs[49]
-				arm1 = bs[51]
-				hand2 = bs[50]
-			elseif clothingtype == "camo2" then
-				hand1 = bs[52]
-				arm1 = bs[54]
-				hand2 = bs[53]
-			else
-				hand1 = bs[43]
-				arm1 = bs[45]
-				hand2 = bs[44]
-			end
-
-			SetToolTransform(offset, 0.2)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.275, -0.6, -2.6))
-
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				mag0 = shapes[2]
-				bolt = shapes[3]
-				bolt2 = shapes[30]
-				selector = shapes[4]
-				suppressor = shapes[5]
-				scope = shapes[6]
-				scope_2 = shapes[42]
-				holo = shapes[7]
-				holo2 = shapes[8]
-				reddot = shapes[40]
-				reddot2 = shapes[41]
-				rail = shapes[9]
-				stock0 = shapes[10]
-				stock1 = shapes[37]
-				muzzlebreak = shapes[11]
-				muzzlebreak2 = shapes[12]
-				mag1 = shapes[13]
-				mag2 = shapes[14]
-				mag3 = shapes[15]
-				grip1 = shapes[16]
-				grip1_2 = shapes[17]
-				grip2 = shapes[18]
-				grip3 = shapes[22]
-				grip3_1 = shapes[23]
-				grip3_2 = shapes[24]
-				grip4 = shapes[25]
-				barrel0 = shapes[19]
-				barrel1 = shapes[20]
-				barrel2 = shapes[21]
-				side1 = shapes[26]
-				side2 = shapes[27]
-				side3 = shapes[28]
-				grenade = shapes[29]
-				guard0 = shapes[31]
-				guard0_2 = shapes[32]
-				guard1 = shapes[33]
-				guard1_2 = shapes[34]
-				guard2 = shapes[35]
-				guard2_2 = shapes[36]
-				g33 = shapes[38]
-				g33_2 = shapes[39]
-				magTrans = GetShapeLocalTransform(mag0)
-				boltTrans = GetShapeLocalTransform(bolt)
-				boltTrans2 = GetShapeLocalTransform(bolt2)
-				selectorTrans = GetShapeLocalTransform(selector)
-				suppressorTrans = GetShapeLocalTransform(suppressor)
-				scopeTrans = GetShapeLocalTransform(scope)
-				holoTrans = GetShapeLocalTransform(holo)
-				holoTrans2 = GetShapeLocalTransform(holo2)
-				reddotTrans = GetShapeLocalTransform(reddot)
-				g33Trans = GetShapeLocalTransform(g33)
-				railTrans = GetShapeLocalTransform(rail)
-				stock0Trans = GetShapeLocalTransform(stock0)
-				muzzlebreakTrans = GetShapeLocalTransform(muzzlebreak)
-				muzzlebreakTrans2 = GetShapeLocalTransform(muzzlebreak2)
-				gripTrans = GetShapeLocalTransform(grip1)
-				barrelTrans0 = GetShapeLocalTransform(barrel0)
-				barrelTrans1 = GetShapeLocalTransform(barrel1)
-				barrelTrans2 = GetShapeLocalTransform(barrel2)
-				sideTrans1 = GetShapeLocalTransform(side1)
-				sideTrans2 = GetShapeLocalTransform(side2)
-				sideTrans3 = GetShapeLocalTransform(side3)
-				grenadeTrans = GetShapeLocalTransform(grenade)
-				guardTrans0 = GetShapeLocalTransform(guard0)
-			end
-
-			mt = TransformCopy(magTrans)
-			mt.pos = VecAdd(mt.pos, magoffset)
-
-			bt = TransformCopy(boltTrans)
-			bt.pos = VecAdd(bt.pos, boltoffset)
-			bt2 = TransformCopy(boltTrans2)
-			bt2.pos = VecAdd(bt2.pos, boltoffset)
-
-			st = TransformCopy(selectorTrans)
-
-			spt = TransformCopy(suppressorTrans)
-
-			sct = TransformCopy(scopeTrans)
-			sct_2 = TransformCopy(scopeTrans)
-
-			ht = TransformCopy(holoTrans)
-			ht2 = TransformCopy(holoTrans2)
-
-			rdt = TransformCopy(reddotTrans)
-			rdt2 = TransformCopy(reddotTrans)
-
-			g33t = TransformCopy(g33Trans)
-			g33t2 = TransformCopy(g33Trans)
-
-			rt = TransformCopy(railTrans)
-
-			stt0 = TransformCopy(stock0Trans)
-			stt1 = TransformCopy(stock0Trans)
-
-			mbt = TransformCopy(muzzlebreakTrans)
-			mbt2 = TransformCopy(muzzlebreakTrans2)
-
-			gt1 = TransformCopy(gripTrans)
-			gt1_2 = TransformCopy(gripTrans)
-
-			gt2 = TransformCopy(gripTrans)
-
-			gt3 = TransformCopy(gripTrans)
-			gt3_1 = TransformCopy(gripTrans)
-			gt3_2 = TransformCopy(gripTrans)
-
-			glt = TransformCopy(gripTrans)
-
-			brt0 = TransformCopy(barrelTrans0)
-
-			brt1 = TransformCopy(barrelTrans1)
-
-			brt2 = TransformCopy(barrelTrans2)
-
-			sdt1 = TransformCopy(sideTrans1)
-			sdt2 = TransformCopy(sideTrans2)
-			sdt3 = TransformCopy(sideTrans3)
-
-			grt = TransformCopy(grenadeTrans)
-			grt.pos = VecAdd(grt.pos, grenadeoffset)
-
-			gdt0 = TransformCopy(guardTrans0)
-			gdt0_2 = TransformCopy(guardTrans0)
-			gdt1 = TransformCopy(guardTrans0)
-			gdt1_2 = TransformCopy(guardTrans0)
-			gdt2 = TransformCopy(guardTrans0)
-			gdt2_2 = TransformCopy(guardTrans0)
-
-			if reloading and ammo == 0 then
-				-- if q and ironsight then
-				-- 	if reloadTimer < 0.4 and reloadTimer > 0.2 then
-				-- 		bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(0.4-reloadTimer)/0.2))
-				-- 	elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
-				-- 		bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(reloadTimer-0.15)/0.05))
-				-- 	end
-				-- else
-					if reloadTimer < 0.4 and reloadTimer > 0.2 then
-						bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(0.4-reloadTimer)/0.2))
-					elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
-						bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(reloadTimer-0.15)/0.05))
-					end
-				-- end
-			end
-
-			if selectfireTimer < 0.4 then
-				if selectfire == 1 then
-					st.rot = QuatEuler(-65, 0, 0)
-					st.pos = VecAdd(st.pos, Vec(-0.025, -0.01, -0.015))
-				elseif selectfire == 2 then
-					st.rot = QuatEuler(-10, 0, 0)
-					st.pos = VecAdd(st.pos, Vec(-0.025, -0.005, -0.045))
-				else
-					st.rot = QuatEuler(45, 0, 0)
-					st.pos = VecAdd(st.pos, Vec(-0.025, 0.025, -0.0625))
-				end
-			elseif selectfireTimer > 0 then
-				if selectfire0 == 1 then
-					st.rot = QuatEuler(-65, 0, 0)
-					st.pos = VecAdd(st.pos, Vec(-0.025, -0.01, -0.015))
-				elseif selectfire0 == 2 then
-					st.rot = QuatEuler(-10, 0, 0)
-					st.pos = VecAdd(st.pos, Vec(-0.025, -0.005, -0.045))
-				else
-					st.rot = QuatEuler(45, 0, 0)
-					st.pos = VecAdd(st.pos, Vec(-0.025, 0.025, -0.0625))
-				end
-			end
-
-			muzzlelength = 0
-			lightFactor = 2
-			if muzzle == "muzzle1" then
-				spt.pos = VecAdd(spt.pos, Vec(0.075, -0.05, -barrellength))
-				spt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 0.2
-				muzzlelength = 0.6
-			else
-				spt.pos = hidePos
-				spt.rot = QuatEuler(0, 0, 0)
-				muzzleFactor = 1
-			end
-			if muzzle == "muzzle2" then
-				mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, -barrellength))
-				mbt2.pos = VecAdd(mbt2.pos, Vec(0.025, -0.025, -barrellength))
-				mbt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 3
-				muzzleFactor = 0.75
-				muzzlelength = 0.2
-			else
-				mbt.pos = hidePos
-				mbt2.pos = hidePos
-				mbt.rot = QuatEuler(0, 0, 0)
-				muzzleFactor = 1
-			end
-			if toprail == "scope" and (not ironsight or reloading or scopeTimer < 0.5 or q or e) then
-				sct.pos = Vec(0.2, -0.35, -0.85)
-				sct_2.pos = Vec(0.175, -0.275, -1.149)
-			else
-				sct.pos = hidePos
-				sct_2.pos = hidePos
-			end
-			if toprail == "holo" then
-				ht.pos = Vec(0.175, -0.375, -1.1)
-				ht2.pos = Vec(0.225, -0.3, -1.1)
-			else
-				ht.pos = hidePos
-				ht2.pos = hidePos
-			end
-			if toprail == "sight3" then
-				rdt.pos = Vec(0.175, -0.375+0.05, -0.95+0.05)
-				rdt2.pos = Vec(0.2, -0.4+0.05, -1+0.05)
-			else
-				rdt.pos = hidePos
-				rdt2.pos = hidePos
-			end
-			if magnifier == "g33" then
-				g33t.pos = Vec(0.175, -0.425+0.05, -0.9)
-				if magnified then
-					g33t2.pos = Vec(0.2, -0.3375+0.05, -0.7)
-				else
-					g33t2.pos = Vec(0.35, -0.1875+0.05, -0.7)
-					g33t2.rot = QuatRotateQuat(g33t2.rot, QuatEuler(0, 90, 0))
-				end
-			else
-				g33t.pos = hidePos
-				g33t2.pos = hidePos
-			end
-			if foldstock == "removed" then
-				stt0.pos = Vec(0.2, -1, 0.45)
-				stt0.rot = QuatEuler(-90, 0, 0)
-				stt1.pos = Vec(0.2, -1, 0.45)
-				stt1.rot = QuatEuler(-90, 0, 0)
-				stockFactor = 5
-			end
-			if stock == "stock1" then
-				stt0.pos = hidePos
-				stockFactor = 0.9
-			elseif stock == "" then
-				stt1.pos = hidePos
-				stockFactor = 1
-			end
-			if stock == "removed" then
-				stt0.pos = hidePos
-				stt1.pos = hidePos
-				stockFactor = 5
-			end
-			if foldstock == "removed" then
-				stockFactor = 5
-			end
-			rt.pos = Vec(0.175, -0.725, -0.85)
-
-			if mag == "" or mag == "mag0" then
-				magsize = 30
-				reloadFactor = 1.3
-				SetShapeLocalTransform(mag0, Transform(VecAdd(mt.pos, Vec(-0.025, 0.05, -0.025)), mt.rot))
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-				SetShapeLocalTransform(mag3, hideTrans)
-			elseif mag == "mag1" then
-				magsize = 40
-				reloadFactor = 1.5
-				SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(-0.025, -0.05, -0.025)), mt.rot))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-				SetShapeLocalTransform(mag3, hideTrans)
-			elseif mag == "mag2" then
-				magsize = 50
-				reloadFactor = 1.7
-				SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.175, 0.05, 0.025)), mt.rot))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag3, hideTrans)
-			elseif mag == "mag3" then
-				magsize = 100
-				reloadFactor = 2.3
-				SetShapeLocalTransform(mag3, Transform(VecAdd(mt.pos, Vec(-0.475, 0.05, -0.025)), QuatRotateQuat(mt.rot, QuatEuler(10, 0, 0))))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-			end
-
-			if grip == "grip1" then
-				gripfactorx = 0.85
-				gripfactory = 0.6
-				gt1.pos = Vec(0.2, -0.85, -1.775-guardlength)
-				gt1_2.pos = Vec(0.225, -1.05, -1.8-guardlength)
-			else
-				gt1.pos = hidePos
-				gt1_2.pos = hidePos
-			end
-			if grip == "grip2" then
-				gripfactorx = 0.6
-				gripfactory = 0.85
-				gt2.pos = Vec(0.225, -0.9, -1.8-guardlength)
-			else
-				gt2.pos = hidePos
-			end
-			if grip == "grip3" then
-				local querypos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2-barrellength*4/3))
-				local hit, dist = QueryRaycast(querypos, Vec(0, -2, 0), 5, 0.2)
-				local bipodded = (InputDown("ctrl") or dist < 0.4) and selectfire > 0 and VecLength(GetPlayerVelocity()) < 0.1
-				if bipodded then
-					gripfactorx = 0.4
-					gripfactory = 0.4
-					bipodFactor = 0.5
-					gt3_1.pos = Vec(0.4, -1.35, -2.05-barrellength*4/3)
-					gt3_2.pos = Vec(0.05, -1.325, -2.05-barrellength*4/3)
-					gt3_1.rot = QuatEuler(0, 0, 10)
-					gt3_2.rot = QuatEuler(0, 0, -10)
-				else
-					gripfactorx = 1
-					gripfactory = 1
-					bipodFactor = 1
-					if barrel == "barrel2" then
-						gt3_1.pos = Vec(0.3, -0.725, -1.3-barrellength)
-						gt3_2.pos = Vec(0.15, -0.725, -1.3-barrellength)
-					else
-						gt3_1.pos = Vec(0.3, -0.675, -2.75-barrellength)
-						gt3_2.pos = Vec(0.15, -0.675, -2.75-barrellength)
-						gt3_1.rot = QuatEuler(90, 0, 0)
-						gt3_2.rot = QuatEuler(90, 0, 0)
-					end
-					
-				end
-				gt3.pos = Vec(0.225, -0.725, -1.95-guardlength)
-				
-			else
-				gt3.pos = hidePos
-				gt3_1.pos = hidePos
-				gt3_2.pos = hidePos
-			end
-			if grip == "grenade_launcher" then
-				gripfactorx = 1.1
-				gripfactory = 1.1
-				glt.pos = Vec(0.2, -0.9, -1.4)
-			else
-				glt.pos = hidePos
-			end
-			if grip == "" then
-				gripfactorx = 1
-				gripfactory = 1
-			end
-
-			if barrel == "" then
-				barrelFactorx = 1
-				barrelFactory = 1
-				barrelFactordamage = 1
-				accuracyFactor = 0.7*bipodFactor
-				barrellength = 0.075
-				brt0.pos = brt0.pos
-				if guard == "guard2" then
-					SetString("savegame.mod.guard", "")
-				end
-			else
-				brt0.pos = hidePos
-			end
-			if barrel == "barrel1" then
-				barrelFactorx = 1.2
-				barrelFactory = 0.95
-				barrelFactordamage = 1
-				accuracyFactor = 0.9*bipodFactor
-				barrellength = -0.125
-				brt1.pos = brt1.pos
-				if guard == "" or guard == "guard2" then
-					SetString("savegame.mod.guard", "guard1")
-				end
-			else
-				brt1.pos = hidePos
-			end
-			if barrel == "barrel2" then
-				barrelFactorx = 0.8
-				barrelFactory = 1.05
-				barrelFactordamage = 1.15
-				accuracyFactor = 0.5*bipodFactor
-				barrellength = 0.375
-				brt2.pos = brt2.pos
-			else
-				brt2.pos = hidePos
-			end
-
-			if side == "side1" then
-				sdt1.pos = sdt1.pos
-			else
-				sdt1.pos = hidePos
-			end
-			if side == "side2" then
-				sdt2.pos = sdt2.pos
-			else
-				sdt2.pos = hidePos
-			end
-			if side == "side3" then
-				sdt3.pos = sdt3.pos
-			else
-				sdt3.pos = hidePos
-			end
-
-			if toprail ~= "holo" then
-				SetString("savegame.mod.magnifier", "")
-			end
-
-			if mag == "mag3" then
-				SetString("savegame.mod.foldstock", "")
-			end
-
-			if guard == "" then
-				gdt0.pos = Vec(0.225, -0.625, -1.8)
-				gdt0_2.pos = Vec(0.2, -0.7, -1.8)
-				guardlength = 0
-			else
-				gdt0.pos = hidePos
-				gdt0_2.pos = hidePos
-			end
-			if guard == "guard1" then
-				gdt1.pos = Vec(0.225, -0.625, -1.8)
-				gdt1_2.pos = Vec(0.2, -0.7, -1.8)
-				guardlength = -0.2
-			else
-				gdt1.pos = hidePos
-				gdt1_2.pos = hidePos
-			end
-			if guard == "guard2" then
-				gdt2.pos = Vec(0.225, -0.725, -1.8)
-				gdt2_2.pos = Vec(0.2, -0.7, -1.8)
-				guardlength = 0.3
-			else
-				gdt2.pos = hidePos
-				gdt2_2.pos = hidePos
-			end
-
-			SetShapeLocalTransform(bolt, bt)
-			SetShapeLocalTransform(bolt2, bt2)
-			SetShapeLocalTransform(selector, st)
-			SetShapeLocalTransform(suppressor, spt)
-			SetShapeLocalTransform(scope, sct)
-			SetShapeLocalTransform(scope_2, sct_2)
-			SetShapeLocalTransform(holo, ht)
-			SetShapeLocalTransform(holo2, ht2)
-			SetShapeLocalTransform(reddot, rdt)
-			SetShapeLocalTransform(reddot2, rdt2)
-			SetShapeLocalTransform(g33, g33t)
-			SetShapeLocalTransform(g33_2, g33t2)
-			SetShapeLocalTransform(rail, rt)
-			SetShapeLocalTransform(stock0, stt0)
-			SetShapeLocalTransform(stock1, stt1)
-			SetShapeLocalTransform(muzzlebreak, mbt)
-			SetShapeLocalTransform(muzzlebreak2, mbt2)
-			SetShapeLocalTransform(grip1, gt1)
-			SetShapeLocalTransform(grip1_2, gt1_2)
-			SetShapeLocalTransform(grip2, gt2)
-			SetShapeLocalTransform(grip3, gt3)
-			SetShapeLocalTransform(grip3_1, gt3_1)
-			SetShapeLocalTransform(grip3_2, gt3_2)
-			SetShapeLocalTransform(grip4, glt)
-			SetShapeLocalTransform(barrel0, brt0)
-			SetShapeLocalTransform(barrel1, brt1)
-			SetShapeLocalTransform(barrel2, brt2)
-			SetShapeLocalTransform(side1, sdt1)
-			SetShapeLocalTransform(side2, sdt2)
-			SetShapeLocalTransform(side3, sdt3)
-			SetShapeLocalTransform(grenade, grt)
-			SetShapeLocalTransform(guard0, gdt0)
-			SetShapeLocalTransform(guard0_2, gdt0_2)
-			SetShapeLocalTransform(guard1, gdt1)
-			SetShapeLocalTransform(guard1_2, gdt1_2)
-			SetShapeLocalTransform(guard2, gdt2)
-			SetShapeLocalTransform(guard2_2, gdt2_2)
-		end
-
-		if selectattachments then
-			clickedmag = clickedmag1 or clickedmag2 or clickedmag3 or clickedmag4
-			if clickedmag and selectattachments and not InputPressed("t") and not GetBool("level.optionstriggered") then
-				Reload()
-			end
-		end
-		if reloading and not clickedmag and selectattachments then
-			selectattachments = false
-			selectattachmentsTimer = 0.25
-		end
-
-		if not selectattachments then
-			if (InputPressed("r") or clickedmag) and selectfireTimer == 0 then
-				if not realistic and (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) then
-					Reload()
-					inspectTimer = 0
-				end
-			end
-
-			if (InputReleased("r") or clickedmag) and selectfireTimer == 0 then
-				if realistic and curmagslot ~= nextmagslot then
-					Reload()
-					inspectTimer = 0
-				end
-			end
-			
-			if GetBool("ammobox.refill") then
-				SetBool("ammobox.refill", false)
-				mags = mags + 1
-				PlaySound(refillsound, GetPlayerTransform().pos, 1, false)
-			end
-
-			if reloading then
-				if reloadTimer > 0.4 then
-					reloadTimer = reloadTimer - dt/reloadFactor
-				elseif reloadTimer > 0 then
-					reloadTimer = reloadTimer - dt
-				end
-				if reloadTimer < 0.5 and not cocksoundplaying and ammo == 0 then
-					cocksoundplaying = true
-					PlaySound(cocksound, GetPlayerTransform().pos, 1)
-				end
-				if reloadTimer < 0 then
-					cocksoundplaying = false
-					if grenadelauncher then
-						grenadelauncherammo = 1
-					else
-						if realistic then
-							if ammo == 0 then
-								ammo = magtable2[curmagslot][2]
-							else
-								ammo = magtable2[curmagslot][2] + 1
-							end
-						else
-							if ammo == 0 then
-								ammo = magsize
-							else
-								ammo = magsize + 1
-							end
-						end
-					end
-					reloadTimer = 0
-					reloading = false
-				end
-			end
-
-			if selectfireTimer < 0.55 and selectfireTimer > 0 and not selectsoundplaying then
-				selectsoundplaying = true
-				PlaySound(selectsound, GetPlayerTransform().pos, 0.85)
-			end
-			if selectfireTimer < 0 then
-				selectsoundplaying = false
-				selectfireTimer = 0
-			end
-			
-		end
-
-		btrans = GetBodyTransform(b)
-
-		if InputDown("crouch") then
-			crouchoffset = math.min(crouchoffset + dt*3, 0.8)
-		else
-			crouchoffset = math.max(crouchoffset - dt*3, 0)
-		end
-		local x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.8, -2-guardlength, 0, 0, 0
-		if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.4 then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0.125, -0.5, -1.4, 0, 0, 0
-		elseif reloading and ammo == 0 and reloadTimer < 0.5 and reloadTimer > 0.2 then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0.15-(reloadTimer-0.2)*1.5, -0.5, -1.5+(0.6-reloadTimer)*0.75, 0, 0, 0
-		elseif (reloading and ammo > 0) or (reloading and ammo == 0 and reloadTimer > 0.2) then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0+mt.pos[1], 0.4+mt.pos[2], -0.2+mt.pos[3], 0, 0, 0
-		elseif selectfireTimer > 0 then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.825, -0.9, 0, 0, 0
-		end
-
-		h1p1l = INS(true, x2, y2, z2, rotx2, roty2, rotz2).pos
-
-		-- h1p1l = Vec(0.225, -0.85, -1.9)
-		h1p2l = TransformToLocalPoint(btrans, TransformToParentPoint(GetPlayerTransform(), Vec(-0.6, 0.7-crouchoffset, 0.2)))
-		hnd1 = Transform(h1p1l, QuatRotateQuat(QuatLookAt(h1p2l, h1p1l), QuatEuler(0,90,90)))
-		a1p1l = VecAdd(h1p1l, TransformToParentVec(hnd1, Vec(0, 1, 0)))
-		a1p2l = TransformToLocalPoint(btrans, TransformToParentPoint(GetPlayerTransform(), Vec(-0.45, 1.5-crouchoffset, 0.5)))
-		amt1 = Transform(a1p1l, QuatRotateQuat(QuatLookAt(a1p2l, a1p1l), QuatEuler(0,90,90)))
-		SetShapeLocalTransform(hand1, hnd1)
-		SetShapeLocalTransform(arm1, amt1)
-
-		h2p1l = Vec(0.275, -0.95, -0.85)
-		h2p2l = TransformToLocalPoint(btrans, TransformToParentPoint(GetPlayerTransform(), Vec(0.55, 1.1-crouchoffset, 0.9)))
-		hnd2 = Transform(h2p1l, QuatRotateQuat(QuatLookAt(h2p2l, h2p1l), QuatEuler(0,90,90)))
-		SetShapeLocalTransform(hand2, hnd2)
-
-
-		sightattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.3, -1.2))
-		muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.575, -2.4-barrellength))
-		stockattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.55, -0.5))
-		sideattachpoint = TransformToParentPoint(btrans, Vec(0.2, -0.6, -1.95))
-		magattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1))
-		gripattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1.9-guardlength))
-		barrelattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.6, -1.6))
-		guardattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.5, -1.8))
-
-		for key, shell in ipairs(ak47projectileHandler.shells) do
-			if shell.active then
-				ProjectileOperations(shell)
-			end
-		end
-		for key, shell in ipairs(ak47grenadeHandler.shells) do
-			if shell.active then
-				GrenadeOperations(shell)
-			end
-		end
-	
-		if shootTimer > 0 or ammo == 0 then
-			shootTimer = shootTimer - dt
-		end
-	end
-end
-
-function draw()
-	if GetString("game.player.tool") == "g36k" and GetPlayerVehicle() == 0 then
-
-
-		------SCOPE RETICLE------
-		if toprail == "scope" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
-			local gt = GetBodyTransform(GetToolBody())
-			local sightcenter = Vec(0.275, -0.175, -1.8)
-			local sightrear = Vec(0.275, -0.175, -1.4)
-			local gunpos = TransformToParentPoint(gt, sightcenter)
-			local rearpos = TransformToParentPoint(gt, sightrear)
-			local fwdpos = TransformToParentVec(gt, Vec(0, 0, -1))
-			local hit, dist = QueryRaycast(gunpos, fwdpos, 500, 0, true)
-			local hitpoint = VecAdd(gunpos, VecScale(fwdpos, dist))
-
-			local camtrans = GetPlayerCameraTransform()
-			local sightdist = VecLength(VecSub(camtrans.pos, gunpos))
-
-			local holopoint = VecAdd(camtrans.pos, VecScale(VecNormalize(VecSub(camtrans.pos, hitpoint)), -sightdist))
-			UiPush()
-				local w, h = UiGetImageSize("MOD/img/reticle2.png")
-				local x, y = UiWorldToPixel(holopoint)
-				UiTranslate(x-w/2, y-h/2)
-				UiImage("MOD/img/reticle2.png")
-			UiPop()
-			UiPush()
-				local w, h = UiGetImageSize("MOD/img/reticleoutline.png")
-				local x, y = UiWorldToPixel(rearpos)
-				UiTranslate(x-w/2, y-h/2)
-				UiImage("MOD/img/reticleoutline.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-			UiPop()
-		elseif toprail == "sight4" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
-			UiPush()
-				w, h = UiGetImageSize("MOD/img/reticle3.png")
-				UiTranslate((UiWidth()-w)/2, (UiHeight()-h)/2-sightadjust*20000)
-				UiTranslate(-rnd2*50, -(rnd1*50+recoilAngle*150)-recoilTimer*200)
-				if realistic then
-					UiTranslate(-math.sin(1.3*GetTime())*6*bipodFactor^4, -math.sin(2.1*GetTime())*4*bipodFactor^4)
-				end
-				local speed = math.floor(VecLength(GetPlayerVelocity())+0.1)
-				if speed > 1 then
-					swayy = math.sin(GetTime()*20*speed/7)
-					swayx = math.sin(GetTime()/reloadFactor*speed)
-					UiTranslate(-swayx*speed*6, -swayy*speed*4)
-				end
-				UiImage("MOD/img/reticle3.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-				UiTranslate(0, h)
-				UiImage("MOD/img/black.png")
-			UiPop()
-		end
-		
-			
-		------IN-GAME UI------
-		if not realistic and not GetBool("level.optionstriggered") then
-		if not unlimitedammo then
-			UiPush()
-				UiTranslate(UiCenter(), UiHeight()-60)
-				UiAlign("center middle")
-				UiColor(1, 1, 1)
-				UiFont("bold.ttf", 32)
-				UiTextOutline(0,0,0,1,0.1)
-				if reloading then
-					UiText("Reloading")
-				elseif grenadelauncher then
-					UiText(grenadelauncherammo.."/1 - Grenade")
-				else
-					UiText(ammo.."/"..magsize.." - "..selectfireText)
-				end
-			UiPop()
-		else
-			UiPush()
-				UiTranslate(UiCenter(), UiHeight()-60)
-				UiAlign("center middle")
-				UiColor(1, 1, 1)
-				UiFont("bold.ttf", 32)
-				UiTextOutline(0,0,0,1,0.1)
-				if reloading then
-					UiText("Reloading")
-				elseif grenadelauncher then
-					UiText(grenadelauncherammo.."/1 - Grenade")
-				else
-					UiText("Infinite".." - "..selectfireText)
-				end
-			UiPop()
-		end
-		end
-		if realistic and not GetBool("level.optionstriggered") then
-		if magcheckTimer > 0 and magcheckTimer < 2 then
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiAlign("center middle")
-			UiColor(1, 1, 1, magcheckTimer)
-			UiFont("bold.ttf", 32)
-			local checkammo = CheckAmmo(curmagslot)
-			UiText(checkammo)
-		end
-		if selecttextTimer > 0 then
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiAlign("center middle")
-			UiColor(1, 1, 1, selecttextTimer)
-			UiFont("bold.ttf", 32)
-			UiText(selectfireText)
-		end
-		if jammed and jamclearTimer == 0 then
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiAlign("center middle")
-			UiColor(1, 1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiText("Jammed")
-		elseif jamclearTimer > 0 then
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiAlign("center middle")
-			UiColor(1, 1, 1, jamclearTimer)
-			UiFont("bold.ttf", 32)
-			UiText("Jammed")
-		end
-		end
-	end
-	if GetString("game.player.tool") == "g36k" and grenadelauncher and not selectattachments then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle")
-			UiImage("ui/hud/crosshair-launcher.png")
-		UiPop()
-	end
-	if GetString("game.player.tool") == "g36k" and sideattachment and side == "side3" then
-		UiPush()
-			local x,y,dist = UiWorldToPixel(sideattachpoint)
-			UiTranslate(x, y)
-			UiAlign("center middle")
-			UiColor(1, 0.1, 0.1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(math.floor(range))
-		UiPop()
-	end
-
-	if realistic and selectmag and GetString("game.player.tool") == "g36k" then
-		hoverindex=0
-		UiPush()
-			local x,y,dist=UiWorldToPixel(magattachpoint2)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					for i = 1, totalmags do
-					clickedslot = MagButton(nextmagslot,i,true,{curx,cury},{"Ammo: ", CheckAmmo(i)},60,60)
-					UiTranslate(60,0)
-					curx,cury=curx+60,cury
-					end
-				UiPop()
-			end
-		UiPop()
-	end
-
-
-	------ATTACHMENTS MENU------
-	if not realistic or GetBool("level.optionstriggered") then
-	if selectattachments and GetString("game.player.tool") == "g36k" and GetPlayerVehicle() == 0 then
-
-	local total = 8
-	gripattachpoint2 = AttachmentGroup("attachmentgroup","grip",gripattachpoint,Description,1/total,60,60)
-	barrelattachpoint2 = AttachmentGroup("attachmentgroup","barrel",barrelattachpoint,Description,2/total,60,60)
-	muzzleattachpoint2 = AttachmentGroup("attachmentgroup","muzzle",muzzleattachpoint,Description,3/total,60,60)
-	sideattachpoint2 = AttachmentGroup("attachmentgroup","side",sideattachpoint,Description,4/total,60,60)
-	guardattachpoint2 = AttachmentGroup("attachmentgroup","guard",guardattachpoint,Description,5/total,60,60)
-	sightattachpoint2 = AttachmentGroup("attachmentgroup","toprail",sightattachpoint,Description,6/total,60,60)
-	stockattachpoint2 = AttachmentGroup("attachmentgroup","stock",stockattachpoint,Description,7/total,60,60)
-	if not realistic then
-	magattachpoint2 = AttachmentGroup("attachmentgroup","mag",magattachpoint,Description,8/total,60,60)
-	end
-
-
-	hoverindex=0
-		UiPush()
-			local x,y,dist=UiWorldToPixel(sightattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "toprail" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedscope = AttachmentButton("toprail","sight3",true,{curx,cury},{"Red Dot","1x magnification sight for close range combat."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedholo = AttachmentButton("toprail","holo",true,{curx,cury},{"Holographic Sight","1x magnification sight for close range combat."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					if toprail == "holo" then
-						clickedmagnifier1 = AttachmentButton("magnifier","g33",true,{curx,cury},{"Thermal Magnifier","Foldable 3x magnifier for close range optics that shows heat signatures. Press 'Z' to fold/unfold."})
-					end
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(muzzleattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "muzzle" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedmuzzle1 = AttachmentButton("muzzle","muzzle1",true,{curx,cury},{"Suppressor","Suppresses gun noise for sneaky combat."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Compensator","Reduces horizontal recoil, but turns your barrel into a flashbang."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(stockattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "stock" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedstockremoved = AttachmentButton("stock","removed",true,{curx,cury},{"Stock","Removeable, but decreases overall performance."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedstockremoved = AttachmentButton("stock","stock1",true,{curx,cury},{"Stock","Removeable, but decreases overall performance."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(sideattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "side" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedside1 = AttachmentButton("side","side1",true,{curx,cury},{"Laser","A laser that points where you shoot."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedside2 = AttachmentButton("side","side2",true,{curx,cury},{"Flashlight","Lights up the area in front of you."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedside3 = AttachmentButton("side","side3",true,{curx,cury},{"Rangefinder","Displays the range to your target."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		if not realistic then
-		UiPush()
-			local x,y,dist=UiWorldToPixel(magattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "mag" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedmag1 = AttachmentButton("mag","mag1",true,{curx,cury},{"40rnd Mag","Pew Pew Pew"})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmag2 = AttachmentButton("mag","mag2",true,{curx,cury},{"50rnd Drum","Pew Pew Pew Pew Pew Pew"})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmag3 = AttachmentButton("mag","mag3",true,{curx,cury},{"100rnd Double Drum","Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew"})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		end
-		UiPush()
-			local x,y,dist=UiWorldToPixel(gripattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "grip" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedgrip1 = AttachmentButton("grip","grip1",true,{curx,cury},{"Vertical Grip","Decreased vertical recoil."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedgrip2 = AttachmentButton("grip","grip2",true,{curx,cury},{"Angled Grip","Decreased horizontal recoil."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedgrip3 = AttachmentButton("grip","grip3",true,{curx,cury},{"Bipod","Increased accuracy while crouching or resting the gun on a ledge."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedgrip4 = AttachmentButton("grip","grenade_launcher",true,{curx,cury},{"GP-25","Grenade launcher for increased collateral damage."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(barrelattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "barrel" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedbarrel1 = AttachmentButton("barrel","barrel1",true,{curx,cury},{"Carbine Barrel","Decreased accuracy but less vertical recoil."})
-					UiTranslate(-100,0)
-					curx,cury=curx-70,cury
-					clickedbarrel2 = AttachmentButton("barrel","barrel2",true,{curx,cury},{"Heavy Barrel","Increased accuracy and damage but more vertical recoil."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(guardattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "guard" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedguard1 = AttachmentButton("guard","guard1",true,{curx,cury},{"Short Guard","For carbine barrel."})
-					UiTranslate(-100,0)
-					curx,cury=curx-70,cury
-					if barrel == "barrel2" then
-						clickedguard2 = AttachmentButton("guard","guard2",true,{curx,cury},{"Long Guard","For extended barrel."})
-					end
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-	end
-	end
-	if selectattachments and GetString("game.player.tool") == "g36k" and GetPlayerVehicle() == 0 or GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
-	hoverindex=0
-	UiPush()
-		local x,y,dist=UiWorldToPixel(stockattachpoint)
-			if dist > 0 then
-				UiTranslate(x-70,y)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-				UiAlign("center middle")
-				if not InputDown("shift") and mag ~= "mag3" then
-					clickedstockremoved = AttachmentButton("foldstock","removed",true,{curx,cury},{"Fold Stock","Folds stock for a smaller profile weapon."})
-				end
-			UiPop()
-		end
-	UiPop()
-	end
-	if hint and (selectattachments or InputDown("r") and heldrTimer > 0.2) then drawHint(info) end
-
-
-	------OPTIONS UI------
-	if GetBool("level.optionstriggered") and GetString("game.player.tool") == "g36k" then
-	UiPush()
-		UiAlign("center middle")
-		UiTranslate(UiCenter(), 70)
-		UiFont("bold.ttf", 60)
-		UiText("WEAPON MODDING")
-	UiPop()
-	end
-	
-	if GetBool("level.optionstriggered") and GetString("game.player.tool") == "g36k" then
-
-	UiAlign("center middle")
-	UiTranslate(300, 300)
-	UiFont("bold.ttf", 48)
-	UiText("G36K")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Unlimited Ammo")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(0.5, 0.8, 1)
-		if realistic then
-			UiText("Unvavailable")
-		else
-		if unlimitedammo then
-			if UiTextButton("Yes", 20, 20) then
-				unlimitedammo = false
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				unlimitedammo = true
-				SetBool("savegame.mod.unlimitedammo", unlimitedammo)
-			end
-		end
-		end
-	UiPop()
-	UiTranslate(0, 80)
-	UiPush()
-		UiText("Spent Casings")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if spentcasingsoption then
-			if UiTextButton("Yes", 20, 20) then
-				spentcasingsoption = false
-				SetBool("savegame.mod.spentcasingsoption", spentcasingsoption)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				spentcasingsoption = true
-				SetBool("savegame.mod.spentcasingsoption", spentcasingsoption)
-			end
-		end
-	UiPop()
-	UiTranslate(0, 80)
-	UiPush()
-		UiText("Damage: "..damageoption.."%")
-		UiTranslate(-50, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		damageoption = optionsSlider(damageoption, 50, 1000, 10)
-		SetInt("savegame.mod.damage", damageoption)
-	UiPop()
-
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Realistic Mode")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(0.5, 0.8, 1)
-		if realistic then
-			if UiTextButton("Yes", 20, 20) then
-				realistic = false
-				SetBool("savegame.mod.realistic", realistic)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				realistic = true
-				SetBool("savegame.mod.realistic", realistic)
-				SetBool("savegame.mod.unlimitedammo", false)
-			end
-		end
-	UiPop()
-
-	UiTranslate(0, 100)
-	hoverindex=0
-	if realistic then
-	magtable = {}
-
-	UiPush()
-		UiTranslate(-180, 150)
-		MagButton2("mag0", 1, 2, "30rnd Mag")
-		UiTranslate(60, 0)
-		MagButton2("mag1", 1, 2, "40rnd Mag")
-		UiTranslate(90, 0)
-		MagButton2("mag2", 2, 2, "50rnd Drum")
-		UiTranslate(150, 0)
-		MagButton2("mag3", 3, 2, "100rnd Double Drum")
-	UiPop()
-
-	UiPush()
-		UiAlign("center middle")
-		UiTranslate(-30*(#slots-1), 20+30*(#slots[1]-1))
-		for i = 1,#slots do
-			for j = 1,#slots[i] do
-				local w, h = slots[i][j][3], slots[i][j][4]
-				UiTranslate(30*(w-1), 30*(h-1))
-				local inside2 = UiIsMouseInRect(60*w-1, 60*h-1)
-				UiTranslate(-30*(w-1), -30*(h-1))
-				if inside2 then
-					UiTranslate(30*(w-1), 30*(h-1))
-					UiImageBox("ui/common/box-solid-6.png", 60*w, 60*h, 6, 6)
-					UiTranslate(-30*(w-1), -30*(h-1))
-				elseif slots[i][j][2][1] == i or slots[i][j][2][2] == j or slots[i][j][2][1] == 0 then
-					UiTranslate(30*(w-1), 30*(h-1))
-					UiColor(0.1, 0.2, 0.1)
-					UiImageBox("ui/common/box-solid-6.png", 60*w, 60*h, 6, 6)
-					UiColor(1, 1, 1)
-					UiImageBox("ui/common/box-outline-6.png", 60*w, 60*h, 6, 6)
-					UiTranslate(-30*(w-1), -30*(h-1))
-				end
-				UiTranslate(0, -60)
-			end
-			UiTranslate(60, 60*#slots[i])
-		end
-		UiTranslate(-60*#slots, 0)
-		for i = 1,#slots do
-			for j = 1,#slots[i] do
-				local item, w, h = slots[i][j][1], slots[i][j][3], slots[i][j][4]
-				UiTranslate(30*(w-1), 30*(h-1))
-				if slots[i][j][1] ~= "" then
-					UiImageBox("MOD/icon/"..item..".png", 60*w, 60*h, 0, 0)
-					table.insert(magtable, item)
-				end
-				UiTranslate(-30*(w-1), -30*(h-1))
-				if not InputDown("lmb") and UiIsMouseInRect(59, 59) and grabbed[1][1] ~= "" then
-					placeItem(grabbed, i, j)
-					grabbed = {{"", {0, 0}, 1, 1}, 0, 0}
-				end
-				if InputPressed("lmb") and UiIsMouseInRect(60, 60) then
-					if slots[i][j][1] ~= "" then
-						local w, h = slots[i][j][3], slots[i][j][4]
-						grabbed = {slots[i][j], i, j}
-						slots[i][j] = {"", {0, 0}, w, h}
-					elseif slots[i][j][2][1] ~= 0 then
-						local a = slots[i][j][2][1][1]
-						local b = slots[i][j][2][1][2]
-						local w, h = slots[a][b][3], slots[a][b][4]
-						grabbed = {slots[a][b], a, b}
-						slots[a][b] = {"", {0, 0}, w, h}
-					end
-				end
-				UiTranslate(0, -60)
-			end
-			UiTranslate(60, 60*#slots[i])
-		end
-		if grabbed[1][1] ~= "" then
-			local item, w, h = grabbed[1][1], grabbed[1][3], grabbed[1][4]
-			local x, y = UiGetMousePos()
-			UiTranslate(x+30*(w-1), y+30*(h-1))
-			UiImageBox("MOD/icon/"..item..".png", 60*w, 60*h, 0, 0)
-		end
-		if not InputDown("lmb") and grabbed[1][1] ~= "" then
-			clearItem(grabbed)
-			grabbed = {{"", {0, 0}, 1, 1}, 0, 0}
-		end
-	UiPop()
-
-	SetInt("savegame.mod.totalmags", #magtable)
-	for i = 1, #magtable do
-		SetString("savegame.mod.mslot"..i, magtable[i])
-	end
-	end
-
-	if realistic then
-		UiTranslate(0, 240)
-	end
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-	end
 end
 
 function optionsSlider(current, min, max, incri)
@@ -3360,4 +1160,2175 @@
     return math.floor(number * power) / power
 end
 
-function math.clamp(n, low, high) return math.min(math.max(n, low), high) end+function math.clamp(n, low, high) return math.min(math.max(n, low), high) end
+
+function server.init()
+    	RegisterTool("g36k", "G36K", "MOD/vox/g36k.vox", 3)
+    	SetBool("game.tool.g36k.enabled", true, true)
+    	SetFloat("game.tool.g36k.ammo", 101, true)
+    	------INITIALISE OPTIONS MENU------
+    	damageoption = GetInt("savegame.mod.damageoption")
+    	if damageoption < 50 then
+    		damageoption = 100
+    		SetInt("savegame.mod.damageoption", 100, true)
+    	end
+    	slots = {}
+    	for i = 1,8 do
+    		slots[i] = {}
+    		for j = 1,2 do
+    			slots[i][j] = {"", {0, 0}, 1, 1}
+    		end
+    	end
+    	grabbed = {{"", {0, 0}, 1, 1}, 0, 0}
+    	magtable = {}
+    	totalmags = GetInt("savegame.mod.totalmags")
+    	magplace = 1
+    	if GetBool("level.optionstriggered") then
+    	for i = 1,#slots do
+    		for j = 1,#slots[i] do
+    			if slots[i][j][2][1] == 0 and magplace < totalmags+1 then
+    				local w, h = 1, 1
+    				local mag = GetString("savegame.mod.mslot"..magplace)
+    				if mag == "mag0" then
+    					w, h = 1, 2
+    				elseif mag == "mag1" then
+    					w, h = 1, 2
+    				elseif mag == "mag2" then
+    					w, h = 2, 2
+    				elseif mag == "mag3" then
+    					w, h = 3, 2
+    				else
+    					w, h = 1, 2
+    				end
+    				placeItem({{mag, {0, 0}, w, h}, 0, 0}, i, j)
+    				magplace = magplace + 1
+    				DebugPrint("true")
+    				DebugPrint(mag)
+    			else
+    				DebugPrint("false")
+    			end
+    		end
+    	end
+    	end
+    	------INITIALISE WEAPON FUNCTIONS------
+    	damage = 0.125 * GetInt("savegame.mod.damage")/100
+    	if damage == 0 then
+    		damage = 0.125
+    	end
+    	gravity = Vec(0, -10, 0)
+    	hidePos = Vec(0, -200, 0)
+    	hideTrans = Transform(hidePos,QuatEuler())
+    	velocity = 950
+    	drag = 1.7
+    	maxMomentum = 3
+    	tracer = false
+    	recoilVertical = 1
+    	recoilHorizontal = 6
+    	recoilWander = 6
+    	--armor pen
+    	lvl5armor = 0.1
+    	lvl4armor = 0.3
+    	lvl3armor = 0.6
+    	lvl2armor = 0.9
+    	lvl1armor = 1
+    	inside = {}
+    	for i = 1,50 do
+    		inside[i] = {0,0,0,0}
+    	end
+    	hoverindex = 0
+    	--magazine and attachments system
+    	toprail = GetString("savegame.mod.toprail")
+    	muzzle = GetString("savegame.mod.muzzle")
+    	stock = GetString("savegame.mod.stock")
+    	foldstock = GetString("savegame.mod.foldstock")
+    	realistic = GetBool("savegame.mod.realistic")
+    	--magazine system
+    	mslot1 = GetString("savegame.mod.mslot1")
+    	mslot2 = GetString("savegame.mod.mslot2")
+    	mslot3 = GetString("savegame.mod.mslot3")
+    	mslot4 = GetString("savegame.mod.mslot4")
+    	mslot5 = GetString("savegame.mod.mslot5")
+    	mslot6 = GetString("savegame.mod.mslot6")
+    	mslot7 = GetString("savegame.mod.mslot7")
+    	mslot8 = GetString("savegame.mod.mslot8")
+    	if totalmags == 0 then
+    		mslot1, mslot2 = "mag0", "mag0"
+    		SetString("savegame.mod.mslot1", "mag0", true)
+    		SetString("savegame.mod.mslot2", "mag0", true)
+    	totalmags = 2
+    	end
+    magtable2 = {{mslot1,0,0},{mslot2,0,0},{mslot3,0,0},{mslot4,0,0},{mslot5,0,0},{mslot6,0,0},{mslot7,0,0},{mslot8,0,0}}
+    	for i=1,8 do
+    		local magslottype = GetString("savegame.mod.mslot"..i)
+    		if magslottype == "mag0" then
+    			magtable2[i][2] = 30
+    			magtable2[i][3] = 30
+    		elseif magslottype == "mag1" then
+    			magtable2[i][2] = 40
+    			magtable2[i][3] = 40
+    		elseif magslottype == "mag2" then
+    			magtable2[i][2] = 50
+    			magtable2[i][3] = 50
+    		elseif magslottype == "mag3" then
+    			magtable2[i][2] = 100
+    			magtable2[i][3] = 100
+    		else
+    			magtable2[i][2] = 20
+    			magtable2[i][3] = 20
+    		end
+    	end
+    	curmagslot = 1
+    	nextmagslot = 1
+    	if realistic then
+    		sightadjust = -0.005
+    		mag = mslot1
+    		reloadFactor = 1
+    	else
+    		sightadjust = 0
+    		mag = GetString("savegame.mod.mag")
+    		reloadFactor = 1
+    	end
+    	grip = GetString("savegame.mod.grip")
+    	barrel = GetString("savegame.mod.barrel")
+    	side = GetString("savegame.mod.side")
+    	guard = GetString("savegame.mod.guard")
+    	magnifier = GetString("savegame.mod.magnifier")
+    	magnified = false
+    	magnifierFactor = 1
+    	reloadTime = 2.2
+    	shotDelay = 0.08
+    	burstammo = 2
+    	spreadTimer = 1.25
+    	spreadFactor = 1.5
+    	accuracyFactor = 1
+    	bipodFactor = 1
+    	if not realistic then
+    		if mag == "" then
+    			magsize = 30
+    			reloadFactor = 1.1
+    		elseif mag == "mag1" then
+    			magsize = 40
+    			reloadFactor = 1.3
+    		elseif mag == "mag2" then
+    			magsize = 50
+    			reloadFactor = 1.5
+    		elseif mag == "mag3" then
+    			magsize = 100
+    			reloadFactor = 1.6
+    		else
+    			magsize = 20
+    			reloadFactor = 1
+    		end
+    		ammo = magsize
+    	else
+    		ammo = magtable2[curmagslot][2]
+    	end
+    	barrellength = 0
+    	guardlength = 0
+    	barrelFactorx = 0.8
+    	barrelFactory = 1
+    	barrelFactordamage = 1.15
+    	grenadelauncherammo = 1
+    	reloading = false
+    	ironsight = false
+    	ADSx = 0
+    	ADSy = 0
+    	ADSz = 0
+    	ADSrotx = 0
+    	ADSroty = 0
+    	ADSrotz = 0
+    	ADSx0 = 0
+    	ADSy0 = 0
+    	ADSz0 = 0
+    	ADSrotx0 = 0
+    	ADSroty0 = 0
+    	ADSrotz0 = 0
+    	ADSdelta = {0,0,0,0,0,0}
+    	ADSfov = 0
+    	RELx = 0
+    	RELy = 0
+    	RELz = 0
+    	RELrotx = 0
+    	RELroty = 0
+    	RELrotz = 0
+    	SELx = 0
+    	SELy = 0
+    	SELz = 0
+    	SELrotx = 0
+    	SELroty = 0
+    	SELrotz = 0
+    	INSx = 0
+    	INSy = 0
+    	INSz = 0
+    	INSrotx = 0
+    	INSroty = 0
+    	INSrotz = 0
+    	RECx = 0
+    	RECy = 0
+    	RECz = 0
+    	RECrotx = 0
+    	RECroty = 0
+    	RECrotz = 0
+    	RECx0 = 0
+    	RECy0 = 0
+    	RECz0 = 0
+    	RECrotx0 = 0
+    	RECroty0 = 0
+    	RECrotz0 = 0
+    	RECdelta = {0,0,0,0,0,0}
+    	crouchoffset = 0
+    	sideattachment = false
+    	range = 0
+    	grenadelauncher = false
+    	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    	spentcasingsoption = GetBool("savegame.mod.spentcasingsoption")
+    	for i=1, 200 do
+    		ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    	end
+    	for i=1, 10 do
+    		ak47grenadeHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    	end
+    	shootTimer = 0
+    	reloadTimer = 0
+    	recoilTimer = 0
+    	recoilAngle = 0
+    	recoilFactor = 0
+    	stockFactor = 0
+    	muzzleFactor = 0
+    	muzzlelength = 0
+    	gripfactorx = 0
+    	gripfactory = 0
+    	lightFactor = 1
+    	recoilMax = 0
+    	rnd1, rnd2, rnd3, rnd4, rnd5, rnd6 = 0, 0, 0, 0, 0, 0
+    	lightTimer = 0
+    	clickedmag = false
+    	animationTimers = {0, 0, 0, 0, 0}
+    	fovTimer = 0
+    	animation1Timer = 0
+    	optionsrotx = -50
+    	optionsroty = 0
+    	optionszoom = 0
+    	optionsx = 0
+    	magoutTimer = 0
+    	maginTimer = 0
+    	meleeTimer = 0
+    	magcheckTimer = 0
+    	selecttextTimer = 0
+    	cocksoundplaying = false
+    	reloadsound2playing = true
+    	selectsoundplaying = false
+    	selectattachments = false
+    	selectmag = false
+    	jammed = false
+    	jamclearTimer = 0
+    	selectattachmentsTimer = 0
+    	selectattachmentsTimer = 0
+    	inspectTimer = 0
+    	heldrTimer = 0
+    	scopeTimer = 0
+    	e = false
+    	q = false
+    	altaim = false
+    	switchsights = false
+    	selectfire = 1
+    	selectfire0 = 0
+    	selectfireTimer = 0
+    	selectfireText = "Semi"
+    	sin1 = 0
+    	cos1 = 1
+    	sin2 = 0
+    	cos2 = 1
+    	swayx = 0
+    	swayy = 0
+    	swingx = 0
+    	swingy = 0
+    	swingx2 = 0
+    	swingy2 = 0
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/ak0.ogg")
+    suppressedgunsound = LoadSound("MOD/snd/aksuppressed.ogg")
+    grenadelaunchersound = LoadSound("MOD/snd/grenadelauncher.ogg")
+    cocksound = LoadSound("MOD/snd/guncock.ogg")
+    reloadsound = LoadSound("MOD/snd/reload.ogg")
+    reloadsound2 = LoadSound("MOD/snd/reload2.ogg")
+    dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
+    refillsound = LoadSound("MOD/snd/refill.ogg")
+    selectsound = LoadSound("MOD/snd/selectorswitch.ogg")
+    casingsound = LoadSound("MOD/snd/casingsound.ogg")
+    interactsound1 = LoadSound("MOD/snd/interact1.ogg")
+    interactsound2 = LoadSound("MOD/snd/interact2.ogg")
+    uiselect = LoadSound("MOD/snd/uiselect.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "g36k" and GetPlayerVehicle(playerId) == 0 then
+    	SetBool("hud.aimdot", false, true)
+
+    	------CONTROLS------
+    	if InputDown("lmb") and not reloading and selectfire == 3 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    		end
+    	elseif InputPressed("lmb") and not reloading and selectfire == 1 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    			shootTimer = 0.11
+    		end
+    	elseif InputDown("lmb") and not reloading and selectfire == 2 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 and burstammo > 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    		end
+    	end
+
+    	if InputPressed("lmb") and not reloading and not InputDown("shift") and inspectTimer <= 0 then
+    		spreadTimer = 1.25
+    		if (ammo == 0 or selectfire == 0) and not selectattachments then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    	end
+
+    	if InputReleased("lmb") and not reloading and selectfire ~= 0 then
+    		shootTimer = 0
+    		burstammo = 2
+    	end
+
+    	if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") then
+    		if InputPressed("rmb") then
+    			PlaySound(interactsound1, GetPlayerTransform(playerId).pos, 1)
+    		end
+    		ironsight = true
+    		inspectTimer = 0
+    		if scopeTimer < 0.5 and not reloading and not (q or e) and selectfireTimer == 0 and not (altaim and toprail == "scope2") and not switchsights and not InputDown("shift") then
+    			scopeTimer = scopeTimer + dt
+    		end
+    	end
+    	if not InputDown("rmb") then
+    		ironsight = false
+    	end
+    	if selectfire == 0  and selectfireTimer <= 0 then
+    		ironsight = false
+    	end
+    	if (not InputDown("rmb") or reloading or q or e or selectfireTimer > 0 or (altaim and toprail == "scope2") or switchsights or InputDown("shift")) and scopeTimer ~= 0 then scopeTimer = scopeTimer - dt end
+
+    	if InputPressed("e") then
+    		e = not e
+    		q = false
+    	end
+
+    	if InputPressed("q") then
+    		q = not q
+    		e = false
+    	end
+
+    	if InputPressed("c") then
+    		switchsights = not switchsights
+    	end
+    	-- if canted == "" then
+    	-- 	switchsights = false
+    	-- end
+
+    	if InputPressed("x") and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") then
+    		meleeTimer = 0.8
+    		inspectTimer = 0
+    	end
+
+    	if InputPressed("v") and not reloading and not selectattachments and not selectmag and magcheckTimer == 0 and jamclearTimer == 0 then
+    		SelectFire()
+    		inspectTimer = 0
+    		selecttextTimer = 3
+    	end
+    	if selecttextTimer ~= 0 then
+    		selecttextTimer = selecttextTimer - dt
+    	end
+    	if selecttextTimer < 0 then
+    		selecttextTimer = 0
+    	end
+
+    	if InputDown("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 and not realistic or GetBool("level.optionstriggered") then
+    		if InputPressed("t") and not GetBool("level.optionstriggered") then
+    			PlaySound(interactsound2, GetPlayerTransform(playerId).pos, 1)
+    			selectattachmentsTimer = 0.5
+    		end
+    		UiMakeInteractive()
+    		selectattachments = true
+    		ironsight = false
+    		inspectTimer = 0
+    	end
+    	if InputReleased("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and not realistic then
+    		selectattachments = false
+    		selectattachmentsTimer = 0.25
+    	end
+
+    	if InputPressed("b") and side ~= "" then
+    		sideattachment = not sideattachment
+    		PlaySound(uiselect, GetPlayerTransform(playerId).pos, 0.75)
+    	end
+    	Laser(sideattachment and side == "side1")
+    	Flashlight(sideattachment and side == "side2")
+    	Rangefinder(sideattachment and side == "side3")
+
+    	if InputPressed("h") and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 then
+    		magcheckTimer = 4
+    		PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.5)
+    		inspectTimer = 0
+    	end
+    	if magcheckTimer ~= 0 then
+    		magcheckTimer = magcheckTimer - dt
+    		ironsight = false
+    	end
+    	if magcheckTimer < 0 then
+    		magcheckTimer = 0
+    		PlaySound(reloadsound2, GetPlayerTransform(playerId).pos, 0.5)
+    	end
+
+    	if InputDown("r") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then heldrTimer = heldrTimer + dt end
+    	if InputDown("r") and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 and heldrTimer > 0.2 then
+    		UiMakeInteractive()
+    		selectmag = true
+    		ironsight = false
+    	else
+    		selectmag = false
+    	end
+    	if InputReleased("r") and heldrTimer <= 0.2 and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
+    		for i = 1, totalmags do
+    			if magtable2[i][2]/magtable2[i][3] > 0.4 and i ~= curmagslot and curmagslot == nextmagslot then
+    				nextmagslot = i
+    			end
+    		end
+    		inspectTimer = 0
+    		Reload()
+    	end
+    	if InputReleased("r") then heldrTimer = 0 end
+
+    	if InputPressed("r") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jammed and jamclearTimer == 0 then
+    		jamclearTimer = 2
+    	end
+    	if jamclearTimer ~= 0 then
+    		jamclearTimer = jamclearTimer - dt
+    		ironsight = false
+    	end
+    	if jamclearTimer < 0 then
+    		jamclearTimer = 0
+    		jammed = false
+    		cocksoundplaying = false
+    	end
+    	if InputDown("shift") then
+    		ironsight = false
+    		selectattachments = false
+    		inspectTimer = 0
+    	end
+
+    	if grip == "grenade_launcher" then
+    		if InputPressed("c") and not reloading then
+    			grenadelauncher = not grenadelauncher
+    		end
+    	else
+    		grenadelauncher = false
+    	end
+
+    	if InputPressed("y") and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire > 0 and not selectattachments then
+    		if inspectTimer <= 0 then
+    			inspectTimer = 6
+    			ironsight = false
+    		else
+    			inspectTimer = 0
+    		end
+    	end
+
+    	if InputPressed("alt") and magnifier == "g33" then
+    		magnified = not magnified
+    		PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
+    	elseif magnifier == "" then
+    		magnified = false
+    	end
+    	if magnified and not switchsights then
+    		magnifierFactor = 3
+    	else
+    		magnifierFactor = 1
+    	end
+
+    	if selectfire == 3 then
+    		selectfireText = "Full"
+    	elseif selectfire == 1 then
+    		selectfireText = "Semi"
+    	elseif selectfire == 2 then
+    		selectfireText = "Burst"
+    	else
+    		selectfireText = "Safe"
+    	end
+
+    	if shootTimer <= 0 then
+    		recoverySpeed = 0.085
+    		if recoilAngle ~= 0 then
+    			recoilAngle = recoilAngle - (recoilAngle-0.25)*recoverySpeed
+    		elseif recoilAngle < 0 then
+    			recoilAngle = 0
+    		end
+    		if math.abs(rnd1) < 0.05 then
+    			rnd1 = 0
+    		elseif rnd1 ~= 0 then
+    			rnd1 = rnd1 - (rnd1+0.25)*recoverySpeed
+    		elseif rnd1 < 0 then
+    			rnd1 = rnd1 - (rnd1-0.25)*recoverySpeed
+    		end
+    		if math.abs(rnd2) < 0.05 then
+    			rnd2 = 0
+    		elseif rnd2 ~= 0 then
+    			rnd2 = rnd2 - (rnd2+0.25)*recoverySpeed
+    		elseif rnd2 < 0 then
+    			rnd2 = rnd2 - (rnd2-0.25)*recoverySpeed
+    		end
+    		if math.abs(rnd3) < 0.05 then
+    			rnd3 = 0
+    		elseif rnd3 ~= 0 then
+    			rnd3 = rnd3 - (rnd3+0.25)*recoverySpeed
+    		elseif rnd3 < 0 then
+    			rnd3 = rnd3 - (rnd3-0.25)*recoverySpeed
+    		end
+    		if math.abs(rnd4) < 0.05 then
+    			rnd4 = 0
+    		elseif rnd4 ~= 0 then
+    			rnd4 = rnd4 - (rnd4+0.25)*recoverySpeed
+    		elseif rnd4 < 0 then
+    			rnd4 = rnd4 - (rnd4-0.25)*recoverySpeed
+    		end
+    		if math.abs(rnd5) < 0.05 then
+    			rnd5 = 0
+    		elseif rnd5 ~= 0 then
+    			rnd5 = rnd5 - (rnd5+0.25)*recoverySpeed
+    		elseif rnd5 < 0 then
+    			rnd5 = rnd5 - (rnd5-0.25)*recoverySpeed
+    		end
+    		if math.abs(rnd6) < 0.05 then
+    			rnd6 = 0
+    		elseif rnd6 ~= 0 then
+    			rnd6 = rnd6 - (rnd6+0.25)*recoverySpeed
+    		elseif rnd6 < 0 then
+    			rnd6 = rnd6 - (rnd6-0.25)*recoverySpeed
+    		end
+    	end
+
+    	if ironsight then
+    		recoilFactor = 0.8*stockFactor
+    	else
+    		recoilFactor = 1.6*stockFactor
+    	end
+
+    	if ironsight then
+    		recoilMax = 12*muzzleFactor*gripfactory*barrelFactory*stockFactor
+    	else
+    		recoilMax = 25*muzzleFactor*gripfactory*barrelFactory*stockFactor
+    	end
+
+    	if toprail == "scope" and not (q or e) then
+    		spreadFactor = 1
+    	elseif toprail == "holo" and not (q or e) then
+    		spreadFactor = 1.75
+    	else
+    		spreadFactor = 2
+    	end
+
+    	toprail = GetString("savegame.mod.toprail")
+    	muzzle = GetString("savegame.mod.muzzle")
+    	stock = GetString("savegame.mod.stock")
+    	foldstock = GetString("savegame.mod.foldstock")
+    	if realistic then
+    		if maginTimer ~= 0 then
+    			mag = magtable2[curmagslot][1]
+    		end
+    	else
+    		if maginTimer ~= 0 then
+    			mag = GetString("savegame.mod.mag")
+    		end
+    	end
+    	if GetBool("level.optionstriggered") then
+    		if realistic then
+    			mag = magtable[1] or ""
+    		else
+    			mag = GetString("savegame.mod.mag")
+    		end
+    	end
+    	grip = GetString("savegame.mod.grip")
+    	barrel = GetString("savegame.mod.barrel")
+    	side = GetString("savegame.mod.side")
+    	guard = GetString("savegame.mod.guard")
+    	magnifier = GetString("savegame.mod.magnifier")
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local magoffset = Vec(0, 0, 0)
+    		local grenadeoffset = Vec(-0.025, 0.025, 0)
+    		local boltoffset = Vec(-0.025, 0, 0)
+    		local selectoroffset = Transform()
+    		local suppressoroffset = Transform()
+    		local scopeoffset = Transform()
+    		local holooffset = Transform()
+    		local holooffset2 = Transform()
+    		local railoffset = Transform()
+    		local magtimer = magoutTimer + maginTimer
+    		offset = Transform(Vec(0, heightOffset, 0))
+    		local adsFOV, adsTime = 0, 0
+    		local defaultTrans = Transform(Vec(0.25, 0.15, 0.25), QuatEuler(0, 0, 0))
+
+    		x,y,z,rotx,roty,rotz = -0.1,0.2,0,0,0,0
+    		if ironsight then
+    		if grenadelauncher then
+    			x = 0
+    			y = 0.45
+    			z = 0.25
+    			rotz = 0
+    		elseif q then
+    			x = 0.9
+    			y = 0.1
+    			z = 0.3
+    			rotz = 30
+    		elseif e then
+    			x = -0.3
+    			y = 0.3
+    			z = 0.1
+    			rotz = -15
+    		else
+    			--if canted == "sight5" and switchsights then
+    			if switchsights and not reloading then
+    				x = 0.55
+    				y = 0.05
+    				z = 0.2
+    				rotz = 20
+    			elseif toprail == "holo" then
+    				x = 0.275
+    				y = 0.2125
+    				z = 0.15
+    				rotz = 0
+    			elseif toprail == "" then
+    				x = 0.275
+    				y = 0.3
+    				z = 0.15
+    				rotz = 0
+    			elseif toprail == "scope" then
+    				x = 0.275
+    				y = 0.175
+    				z = 0.15
+    				rotz = 0
+    			elseif toprail == "sight3" then
+    				x = 0.275
+    				y = 0.1625
+    				z = 0.2
+    				rotz = 0.1
+    			end
+    		end
+
+    		if reloading then
+    			adsFOV, adsTime = 0, 0.15
+    		elseif not (q or e or grenadelauncher) then
+    			if switchsights then
+    				adsFOV, adsTime = 10, 0.15
+    			elseif toprail == "" then
+    				adsFOV, adsTime = 10, 0.15
+    			elseif toprail == "scope" then
+    				adsFOV, adsTime = 80, 0.25
+    			elseif toprail == "holo" then
+    				adsFOV, adsTime = 20, 0.1
+    			end
+    		elseif grenadelauncher then
+    			adsFOV, adsTime = 10, 0.15
+    		else
+    			adsFOV, adsTime = 0, 0.15
+    		end
+    		end
+
+    		--offset = ADS(ironsight, adsFOV*magnifierFactor, adsTime, -x, y, z, rotz)
+
+    		local limit = 10
+    		if ironsight then limit = 45 end
+    		-- if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and ironsight then swingx2 = math.clamp(swingx2 - InputValue("mousedx")/10, -limit, limit) end
+    		if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and not ironsight then swingx2 = math.clamp(swingx2 + InputValue("mousedx")/40, -limit, limit) end
+    		if swingx2 > 0 and ironsight then
+    			swingx2 = swingx2 - swingx2*0.32
+    		elseif swingx2 < 0 and ironsight then
+    			swingx2 = swingx2 - swingx2*0.32
+    		end
+    		-- if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and ironsight then swingy2 = math.clamp(swingy2 - InputValue("mousedy")/10, -limit, limit) end
+    		if not (selectattachments or GetBool("level.optionstriggered") or selectmag) and not ironsight then swingy2 = math.clamp(swingy2 + InputValue("mousedy")/40, -limit, limit) end
+    		if swingy2 > 0 and ironsight then
+    			swingy2 = swingy2 - swingy2*0.32
+    		elseif swingy2 < 0 and ironsight then
+    			swingy2 = swingy2 - swingy2*0.32
+    		end
+
+    		if ironsight then
+    			btrans = GetBodyTransform(b)
+    			if toprail == "holo" then
+    				local gt = GetBodyTransform(GetToolBody())
+    				local sightcenter = Vec(0.275, -0.2125, -1.15)
+    				local gunpos = TransformToParentPoint(gt, sightcenter)
+    				local fwdpos = TransformToParentVec(gt, Vec(0, 0, -1))
+    				local hit, dist = QueryRaycast(gunpos, fwdpos, 500, 0, true)
+    				local hitpoint = VecAdd(gunpos, VecScale(fwdpos, dist))
+
+    				local camtrans = GetPlayerCameraTransform(playerId)
+    				local sightdist = VecLength(VecSub(camtrans.pos, gunpos))
+
+    				local holopoint = VecAdd(camtrans.pos, VecScale(VecNormalize(VecSub(camtrans.pos, hitpoint)), -sightdist))
+
+    				local holotrans = Transform(holopoint, QuatLookAt(camtrans.pos, hitpoint))
+
+    				if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.08 then
+    					reticle1 = LoadSprite("MOD/img/reticle1.png")
+    					DrawSprite(reticle1, Transform(VecAdd(holotrans.pos, VecScale(GetPlayerVelocity(playerId), 0.045)), holotrans.rot), 0.025, 0.025, 1, 1, 1, 1, true)
+    				end
+    			end
+    			if toprail == "sight3" then
+    				local gt = GetBodyTransform(GetToolBody())
+    				local sightcenter = Vec(0.275, -0.2125+0.05, -1.2+0.05)
+    				local gunpos = TransformToParentPoint(gt, sightcenter)
+    				local fwdpos = TransformToParentVec(gt, Vec(0, 0, -1))
+    				local hit, dist = QueryRaycast(gunpos, fwdpos, 500, 0, true)
+    				local hitpoint = VecAdd(gunpos, VecScale(fwdpos, dist))
+
+    				local camtrans = GetPlayerCameraTransform(playerId)
+    				local sightdist = VecLength(VecSub(camtrans.pos, gunpos))
+
+    				local holopoint = VecAdd(camtrans.pos, VecScale(VecNormalize(VecSub(camtrans.pos, hitpoint)), -sightdist))
+
+    				local holotrans = Transform(holopoint, QuatLookAt(camtrans.pos, hitpoint))
+
+    				if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.1 then
+    					reticle4 = LoadSprite("MOD/img/reticle4.png")
+    					DrawSprite(reticle4, holotrans, 0.2, 0.15, 1, 1, 1, 1, true)
+    				end
+    			end
+    		end
+
+    		local speed = math.clamp(VecLength(GetPlayerVelocity(playerId)), 0, 10)
+    		sin1 = math.clamp(sin1 + cos1*dt*speed*2.8, -1.2, 1.2)
+    		cos1 = math.clamp(cos1 - sin1*dt*speed*2.8, -1.2, 1.2)
+    		sin2 = math.clamp(sin2 + cos2*dt*speed*0.7, -1.2, 1.2)
+    		cos2 = math.clamp(cos2 - sin2*dt*speed*0.7, -1.2, 1.2)
+    		swayy = sin1/3
+    		swayx = sin2/2
+    		-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(swayy*speed, swayx*speed, 0))
+    		-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(math.sin(2.1*GetTime())/9*bipodFactor^4,  math.sin(1.3*GetTime())/6*bipodFactor^4, 0))
+    		-- offset.pos = VecAdd(offset.pos, Vec(math.sin(1.1*GetTime())/360*bipodFactor^4,  math.sin(0.7*GetTime())/240*bipodFactor^4, 0))
+
+    		if meleeTimer ~= 0 then
+    			if meleeTimer > 0.6 then
+    				offset.rot = QuatEuler(0, (0.8-meleeTimer)*800, (0.8-meleeTimer)*50)
+    				offset.pos = VecAdd(offset.pos, Vec((0.8-meleeTimer)*1, (0.8-meleeTimer)*-1, (0.8-meleeTimer)*-7.5))
+    			elseif meleeTimer > 0.4 then
+    				offset.rot = QuatEuler(0, 160, 0)
+    				offset.pos = VecAdd(offset.pos, Vec(0.4+(meleeTimer-0.4)*1.5, 0, -2.5+(meleeTimer-0.4)*-1.5))
+    				stockPos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0, -0.5, -0.65))
+    				if meleeTimer > 0.55 then
+    					if GetShapeMaterialAtPosition(shape, stockPos) == "glass" then
+    						MakeHole(stockPos, 2)
+    					else
+    						MakeHole(stockPos, 0.3)
+    					end
+    				end
+    			else
+    				offset.rot = QuatEuler(0, meleeTimer*400, meleeTimer*100)
+    				offset.pos = VecAdd(offset.pos, Vec(0, 0, meleeTimer*-5))
+    			end
+
+    			meleeTimer = meleeTimer - dt
+    		end
+
+    		if selectfireTimer ~= 0 then
+    			selectfireTimer = selectfireTimer - dt
+    		end
+
+    		if inspectTimer ~= 0 then
+    			inspectTimer = inspectTimer - dt
+    		end
+
+    		if recoilTimer ~= 0 then
+    			-- offset.pos = VecAdd(offset.pos, Vec(0, 0, recoilTimer/2))
+    			-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer)*10, 0, 0))
+
+    			recoilTimer = recoilTimer - dt
+    			boltoffset = Vec(-0.025, 0, recoilTimer*6)
+    		end
+    		local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/400, (recoilAngle/-200)-(rnd1+rnd4)/400-recoilTimer/2, recoilAngle/125+recoilTimer, recoilAngle+(rnd1+rnd4)/4+recoilTimer*16, (rnd2+rnd5)/4, (rnd3+rnd6)/4
+    		-- RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
+    		-- offset.pos = VecAdd(offset.pos, RECoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, RECoffset.rot)
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 0.75, 0.25, (lightTimer/shotDelay)*lightFactor)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if magoutTimer < 0 then
+    			maginTimer = 0.6
+    			magoutTimer = 0
+    			reloadsound2playing = false
+    			PlaySound(interactsound1, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    		if maginTimer < 0 then
+    			maginTimer = 0
+    			if grenadelauncher then
+    				PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
+    			end
+    		end
+    		if maginTimer < 0.25 and not reloadsound2playing and not grenadelauncher then
+    				PlaySound(reloadsound2, GetPlayerTransform(playerId).pos, 0.6, false)
+    				reloadsound2playing = true
+    		end
+    		if magoutTimer ~= 0 then
+    			if grenadelauncher then
+    				grenadeoffset = Vec(-0.025, -magoutTimer*3+0.025, -0.6)
+    			else
+    				magoffset = Vec(0, -(0.6-magoutTimer)*4, 0)
+    			end
+    			magoutTimer = magoutTimer - dt/reloadFactor
+    		end
+    		if maginTimer ~= 0 then
+    			if grenadelauncher then
+    				grenadeoffset = Vec(-0.025, 0.025, -maginTimer)
+    			else
+    				magoffset = Vec(0, -maginTimer*4, 0)
+    			end
+    			maginTimer = maginTimer - dt/reloadFactor
+    		end
+    		if not grenadelauncher or (grenadelauncherammo == 0 and not reloading) then
+    			grenadeoffset = Vec(0, 0, 1000)
+    		end
+
+    		local x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 0, 0, 0
+    		if reloading then
+    		if grenadelauncher then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 5, -10
+    		elseif ironsight then
+    			if q then
+    				if magoutTimer > 0 or magcheckTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.1, 0, -5, 10, -10
+    				elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, 0.05, 0, -5, 10, 0
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = -0.1, -0.05, 0, 5, -15, -5
+    				end
+    			elseif e then
+    				if magoutTimer > 0 or magcheckTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 10, -10
+    				elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.075, -0.125, 0.05, 5, 5, -5
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = -0.4, -0.15, 0.05, 10, 0, 10
+    				end
+    			else
+    				if magoutTimer > 0 or magcheckTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.35, -0.025, -0.1, 0, 0, -25
+    				elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) or (reloadTimer > 0.8 and ammo == 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.35, 0.025, -0.1, 0, 10, -15
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.1, -0.05, -10, 5, 5
+    				end
+    			end
+    		else
+    			if magoutTimer > 0.5 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.05, 0, 0, -5, 5, -5
+    			elseif magoutTimer > 0 or magcheckTimer ~= 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.3, 0, 0.1, 5, 20, -15
+    			elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) or (reloadTimer > 0.8 and ammo == 0) then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.15, 0.1, 15, 10, -10
+    			elseif reloadTimer < 0.8 and ammo == 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, 0.05, 10, 15, -10
+    			end
+    		end
+    		end
+
+    		-- RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
+    		-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
+
+    		if reloadTimer > 0.2 and reloading and ammo == 0 then
+    			boltoffset = Vec(-0.025, 0, 0.34)
+    		elseif ammo == 0 and not reloading then
+    			boltoffset = Vec(-0.025, 0, 0.34)
+    		end
+
+    		ATToffset = {0,0,0,0,0,0}
+    		if not GetBool("level.optionstriggered") then
+    		-- if selectattachmentsTimer > 0 and selectattachments then
+    		-- 	local t1 = (0.5 - selectattachmentsTimer)/0.5
+    		-- 	ATToffset = VecAdd(offset.pos, Vec(1*t1, 0, -0.8*t1*180/GetInt("options.gfx.fov")))
+    		-- 	ATToffset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t1, 75*t1, -10*t1))
+    		-- elseif selectattachmentsTimer > 0 and not selectattachments then
+    		-- 	local t2 = selectattachmentsTimer/0.25
+    		-- 	ATToffset.pos = VecAdd(offset.pos, Vec(1*t2, 0, -0.8*t2*180/GetInt("options.gfx.fov")))
+    		-- 	ATToffset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t2, 75*t2, -10*t2))
+    		-- elseif selectattachments then
+    		-- 	ATToffset.pos = VecAdd(offset.pos, Vec(1, 0, -0.8*180/GetInt("options.gfx.fov")))
+    		-- 	ATToffset.rot = QuatRotateQuat(offset.rot, QuatEuler(10, 75, -10))
+    		-- end
+    		if selectattachments then ATToffset = {1,0,-0.8*180/GetInt("options.gfx.fov"),10,75,-10} end
+    		end
+    		if GetBool("level.optionstriggered") then
+    			offset.pos = VecAdd(offset.pos, Vec(optionsx+0.2+math.cos(math.pi*optionsrotx/180), 0.2, -1.5-math.sin(math.pi*optionsrotx/180)+optionszoom))
+    			offset.rot = QuatRotateQuat(offset.rot, QuatEuler(0, 100+optionsrotx, optionsroty))
+
+    			if InputValue("mousewheel") > 0 and optionszoom < 1 then
+    				optionszoom = optionszoom + 0.05
+    			elseif InputValue("mousewheel") < 0 and optionszoom > -2 then
+    				optionszoom = optionszoom - 0.05
+    			end
+    			if InputDown("rmb") and grabbed[1][1] == "" then
+    				optionsrotx = optionsrotx + InputValue("mousedx")/2
+    			end
+    			if InputDown("rmb") and grabbed[1][1] == "" then
+    				optionsroty = optionsroty + InputValue("mousedy")/20
+    			end
+    			if optionsroty > 0.1 then optionsroty = optionsroty - optionsroty*0.05 - 0.05 end
+    			if optionsroty < 0.1 then optionsroty = optionsroty - optionsroty*0.05 + 0.05 end
+    			if InputDown("lmb") and grabbed[1][1] == "" then
+    				optionsx = optionsx + InputValue("mousedx")/400
+    			end
+    		end
+
+    		if selectattachmentsTimer ~= 0 then
+    			selectattachmentsTimer = selectattachmentsTimer*0.9 - dt/20
+    		elseif selectattachmentsTimer < 0 then
+    			selectattachmentsTimer = 0
+    		end
+
+    		local x2, y2, z2, rotx2, roty2, rotz2 = 0, 0, 0, 0, 0, 0
+    		if inspectTimer > 4 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = 1, 0, -0.75, 10, 75, -10
+    		elseif inspectTimer > 3 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = 1, 0, -0.75, 10, 75, -20
+    		elseif inspectTimer > 1.25 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = 0.25, -1, 0, 20, 30, 120
+    		elseif inspectTimer ~= 0 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = 0.25, -0.25, 0.25, 20, 30, 0
+    		elseif jamclearTimer ~= 0 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = 0.2, -0.1, 0.1, 10, 10, -10
+    		end
+
+    		-- INSoffset = INS(inspectTimer > 0 or jamclearTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
+    		-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
+
+    		local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 and not reloading then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0.2, 0.2, -0.2, -20, 60, 0
+    		elseif ironsight and q and selectfireTimer ~= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		elseif ironsight and selectfireTimer ~= 0  then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0.15, 0, 0, 0, 5, -10
+    		elseif selectfireTimer ~= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0.4, 0, -0.25, 0, 5, -20
+    		else
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		end
+
+    		-- if not GetBool("level.optionstriggered") then SELoffset = SEL((selectfireTimer > 0 or selectfire == 0 or InputDown("shift")) and not reloading, x3, y3, z3, rotx3, roty3, rotz3)
+    		-- offset.pos = VecAdd(offset.pos, SELoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, SELoffset.rot) end
+
+    		offset = ADS(true, adsFOV*magnifierFactor, adsTime, -x+x1+x2+x3+ATToffset[1]-swingx2/100, y+y1+y2+y3+ATToffset[2]+swingy2/100, z+z1+z2+z3+ATToffset[3], rotx+rotx1+rotx2+rotx3+swingy-swingy2+swayy*speed+ATToffset[4], roty+roty1+roty2+roty3+swingx-swingx2+swayx*speed+ATToffset[5], rotz+rotz1+rotz2+rotz3+ATToffset[6])
+
+    		RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
+    		offset.pos = VecAdd(offset.pos, RECoffset.pos)
+    		offset.rot = QuatRotateQuat(offset.rot, RECoffset.rot)
+
+    		if InputPressed("mmb") then
+    			if clothingtype == "camo" then
+    				clothingtype = "swat"
+    			elseif clothingtype == "swat" then
+    				clothingtype = "camo2"
+    			elseif clothingtype == "camo2" then
+    				clothingtype = ""
+    			else
+    				clothingtype = "camo"
+    			end
+    		end
+    		local bs = GetBodyShapes(GetToolBody())
+    		for i = 43, 54 do
+    			SetShapeLocalTransform(bs[i], hideTrans)
+    		end
+    		if clothingtype == "camo" then
+    			hand1 = bs[46]
+    			arm1 = bs[48]
+    			hand2 = bs[47]
+    		elseif clothingtype == "swat" then
+    			hand1 = bs[49]
+    			arm1 = bs[51]
+    			hand2 = bs[50]
+    		elseif clothingtype == "camo2" then
+    			hand1 = bs[52]
+    			arm1 = bs[54]
+    			hand2 = bs[53]
+    		else
+    			hand1 = bs[43]
+    			arm1 = bs[45]
+    			hand2 = bs[44]
+    		end
+
+    		SetToolTransform(offset, 0.2)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.275, -0.6, -2.6))
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			mag0 = shapes[2]
+    			bolt = shapes[3]
+    			bolt2 = shapes[30]
+    			selector = shapes[4]
+    			suppressor = shapes[5]
+    			scope = shapes[6]
+    			scope_2 = shapes[42]
+    			holo = shapes[7]
+    			holo2 = shapes[8]
+    			reddot = shapes[40]
+    			reddot2 = shapes[41]
+    			rail = shapes[9]
+    			stock0 = shapes[10]
+    			stock1 = shapes[37]
+    			muzzlebreak = shapes[11]
+    			muzzlebreak2 = shapes[12]
+    			mag1 = shapes[13]
+    			mag2 = shapes[14]
+    			mag3 = shapes[15]
+    			grip1 = shapes[16]
+    			grip1_2 = shapes[17]
+    			grip2 = shapes[18]
+    			grip3 = shapes[22]
+    			grip3_1 = shapes[23]
+    			grip3_2 = shapes[24]
+    			grip4 = shapes[25]
+    			barrel0 = shapes[19]
+    			barrel1 = shapes[20]
+    			barrel2 = shapes[21]
+    			side1 = shapes[26]
+    			side2 = shapes[27]
+    			side3 = shapes[28]
+    			grenade = shapes[29]
+    			guard0 = shapes[31]
+    			guard0_2 = shapes[32]
+    			guard1 = shapes[33]
+    			guard1_2 = shapes[34]
+    			guard2 = shapes[35]
+    			guard2_2 = shapes[36]
+    			g33 = shapes[38]
+    			g33_2 = shapes[39]
+    			magTrans = GetShapeLocalTransform(mag0)
+    			boltTrans = GetShapeLocalTransform(bolt)
+    			boltTrans2 = GetShapeLocalTransform(bolt2)
+    			selectorTrans = GetShapeLocalTransform(selector)
+    			suppressorTrans = GetShapeLocalTransform(suppressor)
+    			scopeTrans = GetShapeLocalTransform(scope)
+    			holoTrans = GetShapeLocalTransform(holo)
+    			holoTrans2 = GetShapeLocalTransform(holo2)
+    			reddotTrans = GetShapeLocalTransform(reddot)
+    			g33Trans = GetShapeLocalTransform(g33)
+    			railTrans = GetShapeLocalTransform(rail)
+    			stock0Trans = GetShapeLocalTransform(stock0)
+    			muzzlebreakTrans = GetShapeLocalTransform(muzzlebreak)
+    			muzzlebreakTrans2 = GetShapeLocalTransform(muzzlebreak2)
+    			gripTrans = GetShapeLocalTransform(grip1)
+    			barrelTrans0 = GetShapeLocalTransform(barrel0)
+    			barrelTrans1 = GetShapeLocalTransform(barrel1)
+    			barrelTrans2 = GetShapeLocalTransform(barrel2)
+    			sideTrans1 = GetShapeLocalTransform(side1)
+    			sideTrans2 = GetShapeLocalTransform(side2)
+    			sideTrans3 = GetShapeLocalTransform(side3)
+    			grenadeTrans = GetShapeLocalTransform(grenade)
+    			guardTrans0 = GetShapeLocalTransform(guard0)
+    		end
+
+    		mt = TransformCopy(magTrans)
+    		mt.pos = VecAdd(mt.pos, magoffset)
+
+    		bt = TransformCopy(boltTrans)
+    		bt.pos = VecAdd(bt.pos, boltoffset)
+    		bt2 = TransformCopy(boltTrans2)
+    		bt2.pos = VecAdd(bt2.pos, boltoffset)
+
+    		st = TransformCopy(selectorTrans)
+
+    		spt = TransformCopy(suppressorTrans)
+
+    		sct = TransformCopy(scopeTrans)
+    		sct_2 = TransformCopy(scopeTrans)
+
+    		ht = TransformCopy(holoTrans)
+    		ht2 = TransformCopy(holoTrans2)
+
+    		rdt = TransformCopy(reddotTrans)
+    		rdt2 = TransformCopy(reddotTrans)
+
+    		g33t = TransformCopy(g33Trans)
+    		g33t2 = TransformCopy(g33Trans)
+
+    		rt = TransformCopy(railTrans)
+
+    		stt0 = TransformCopy(stock0Trans)
+    		stt1 = TransformCopy(stock0Trans)
+
+    		mbt = TransformCopy(muzzlebreakTrans)
+    		mbt2 = TransformCopy(muzzlebreakTrans2)
+
+    		gt1 = TransformCopy(gripTrans)
+    		gt1_2 = TransformCopy(gripTrans)
+
+    		gt2 = TransformCopy(gripTrans)
+
+    		gt3 = TransformCopy(gripTrans)
+    		gt3_1 = TransformCopy(gripTrans)
+    		gt3_2 = TransformCopy(gripTrans)
+
+    		glt = TransformCopy(gripTrans)
+
+    		brt0 = TransformCopy(barrelTrans0)
+
+    		brt1 = TransformCopy(barrelTrans1)
+
+    		brt2 = TransformCopy(barrelTrans2)
+
+    		sdt1 = TransformCopy(sideTrans1)
+    		sdt2 = TransformCopy(sideTrans2)
+    		sdt3 = TransformCopy(sideTrans3)
+
+    		grt = TransformCopy(grenadeTrans)
+    		grt.pos = VecAdd(grt.pos, grenadeoffset)
+
+    		gdt0 = TransformCopy(guardTrans0)
+    		gdt0_2 = TransformCopy(guardTrans0)
+    		gdt1 = TransformCopy(guardTrans0)
+    		gdt1_2 = TransformCopy(guardTrans0)
+    		gdt2 = TransformCopy(guardTrans0)
+    		gdt2_2 = TransformCopy(guardTrans0)
+
+    		if reloading and ammo == 0 then
+    			-- if q and ironsight then
+    			-- 	if reloadTimer < 0.4 and reloadTimer > 0.2 then
+    			-- 		bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(0.4-reloadTimer)/0.2))
+    			-- 	elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
+    			-- 		bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(reloadTimer-0.15)/0.05))
+    			-- 	end
+    			-- else
+    				if reloadTimer < 0.4 and reloadTimer > 0.2 then
+    					bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(0.4-reloadTimer)/0.2))
+    				elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
+    					bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(reloadTimer-0.15)/0.05))
+    				end
+    			-- end
+    		end
+
+    		if selectfireTimer < 0.4 then
+    			if selectfire == 1 then
+    				st.rot = QuatEuler(-65, 0, 0)
+    				st.pos = VecAdd(st.pos, Vec(-0.025, -0.01, -0.015))
+    			elseif selectfire == 2 then
+    				st.rot = QuatEuler(-10, 0, 0)
+    				st.pos = VecAdd(st.pos, Vec(-0.025, -0.005, -0.045))
+    			else
+    				st.rot = QuatEuler(45, 0, 0)
+    				st.pos = VecAdd(st.pos, Vec(-0.025, 0.025, -0.0625))
+    			end
+    		elseif selectfireTimer ~= 0 then
+    			if selectfire0 == 1 then
+    				st.rot = QuatEuler(-65, 0, 0)
+    				st.pos = VecAdd(st.pos, Vec(-0.025, -0.01, -0.015))
+    			elseif selectfire0 == 2 then
+    				st.rot = QuatEuler(-10, 0, 0)
+    				st.pos = VecAdd(st.pos, Vec(-0.025, -0.005, -0.045))
+    			else
+    				st.rot = QuatEuler(45, 0, 0)
+    				st.pos = VecAdd(st.pos, Vec(-0.025, 0.025, -0.0625))
+    			end
+    		end
+
+    		muzzlelength = 0
+    		lightFactor = 2
+    		if muzzle == "muzzle1" then
+    			spt.pos = VecAdd(spt.pos, Vec(0.075, -0.05, -barrellength))
+    			spt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 0.2
+    			muzzlelength = 0.6
+    		else
+    			spt.pos = hidePos
+    			spt.rot = QuatEuler(0, 0, 0)
+    			muzzleFactor = 1
+    		end
+    		if muzzle == "muzzle2" then
+    			mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, -barrellength))
+    			mbt2.pos = VecAdd(mbt2.pos, Vec(0.025, -0.025, -barrellength))
+    			mbt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 3
+    			muzzleFactor = 0.75
+    			muzzlelength = 0.2
+    		else
+    			mbt.pos = hidePos
+    			mbt2.pos = hidePos
+    			mbt.rot = QuatEuler(0, 0, 0)
+    			muzzleFactor = 1
+    		end
+    		if toprail == "scope" and (not ironsight or reloading or scopeTimer < 0.5 or q or e) then
+    			sct.pos = Vec(0.2, -0.35, -0.85)
+    			sct_2.pos = Vec(0.175, -0.275, -1.149)
+    		else
+    			sct.pos = hidePos
+    			sct_2.pos = hidePos
+    		end
+    		if toprail == "holo" then
+    			ht.pos = Vec(0.175, -0.375, -1.1)
+    			ht2.pos = Vec(0.225, -0.3, -1.1)
+    		else
+    			ht.pos = hidePos
+    			ht2.pos = hidePos
+    		end
+    		if toprail == "sight3" then
+    			rdt.pos = Vec(0.175, -0.375+0.05, -0.95+0.05)
+    			rdt2.pos = Vec(0.2, -0.4+0.05, -1+0.05)
+    		else
+    			rdt.pos = hidePos
+    			rdt2.pos = hidePos
+    		end
+    		if magnifier == "g33" then
+    			g33t.pos = Vec(0.175, -0.425+0.05, -0.9)
+    			if magnified then
+    				g33t2.pos = Vec(0.2, -0.3375+0.05, -0.7)
+    			else
+    				g33t2.pos = Vec(0.35, -0.1875+0.05, -0.7)
+    				g33t2.rot = QuatRotateQuat(g33t2.rot, QuatEuler(0, 90, 0))
+    			end
+    		else
+    			g33t.pos = hidePos
+    			g33t2.pos = hidePos
+    		end
+    		if foldstock == "removed" then
+    			stt0.pos = Vec(0.2, -1, 0.45)
+    			stt0.rot = QuatEuler(-90, 0, 0)
+    			stt1.pos = Vec(0.2, -1, 0.45)
+    			stt1.rot = QuatEuler(-90, 0, 0)
+    			stockFactor = 5
+    		end
+    		if stock == "stock1" then
+    			stt0.pos = hidePos
+    			stockFactor = 0.9
+    		elseif stock == "" then
+    			stt1.pos = hidePos
+    			stockFactor = 1
+    		end
+    		if stock == "removed" then
+    			stt0.pos = hidePos
+    			stt1.pos = hidePos
+    			stockFactor = 5
+    		end
+    		if foldstock == "removed" then
+    			stockFactor = 5
+    		end
+    		rt.pos = Vec(0.175, -0.725, -0.85)
+
+    		if mag == "" or mag == "mag0" then
+    			magsize = 30
+    			reloadFactor = 1.3
+    			SetShapeLocalTransform(mag0, Transform(VecAdd(mt.pos, Vec(-0.025, 0.05, -0.025)), mt.rot))
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    			SetShapeLocalTransform(mag3, hideTrans)
+    		elseif mag == "mag1" then
+    			magsize = 40
+    			reloadFactor = 1.5
+    			SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(-0.025, -0.05, -0.025)), mt.rot))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    			SetShapeLocalTransform(mag3, hideTrans)
+    		elseif mag == "mag2" then
+    			magsize = 50
+    			reloadFactor = 1.7
+    			SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.175, 0.05, 0.025)), mt.rot))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag3, hideTrans)
+    		elseif mag == "mag3" then
+    			magsize = 100
+    			reloadFactor = 2.3
+    			SetShapeLocalTransform(mag3, Transform(VecAdd(mt.pos, Vec(-0.475, 0.05, -0.025)), QuatRotateQuat(mt.rot, QuatEuler(10, 0, 0))))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    		end
+
+    		if grip == "grip1" then
+    			gripfactorx = 0.85
+    			gripfactory = 0.6
+    			gt1.pos = Vec(0.2, -0.85, -1.775-guardlength)
+    			gt1_2.pos = Vec(0.225, -1.05, -1.8-guardlength)
+    		else
+    			gt1.pos = hidePos
+    			gt1_2.pos = hidePos
+    		end
+    		if grip == "grip2" then
+    			gripfactorx = 0.6
+    			gripfactory = 0.85
+    			gt2.pos = Vec(0.225, -0.9, -1.8-guardlength)
+    		else
+    			gt2.pos = hidePos
+    		end
+    		if grip == "grip3" then
+    			local querypos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2-barrellength*4/3))
+    			local hit, dist = QueryRaycast(querypos, Vec(0, -2, 0), 5, 0.2)
+    			local bipodded = (InputDown("ctrl") or dist < 0.4) and selectfire > 0 and VecLength(GetPlayerVelocity(playerId)) < 0.1
+    			if bipodded then
+    				gripfactorx = 0.4
+    				gripfactory = 0.4
+    				bipodFactor = 0.5
+    				gt3_1.pos = Vec(0.4, -1.35, -2.05-barrellength*4/3)
+    				gt3_2.pos = Vec(0.05, -1.325, -2.05-barrellength*4/3)
+    				gt3_1.rot = QuatEuler(0, 0, 10)
+    				gt3_2.rot = QuatEuler(0, 0, -10)
+    			else
+    				gripfactorx = 1
+    				gripfactory = 1
+    				bipodFactor = 1
+    				if barrel == "barrel2" then
+    					gt3_1.pos = Vec(0.3, -0.725, -1.3-barrellength)
+    					gt3_2.pos = Vec(0.15, -0.725, -1.3-barrellength)
+    				else
+    					gt3_1.pos = Vec(0.3, -0.675, -2.75-barrellength)
+    					gt3_2.pos = Vec(0.15, -0.675, -2.75-barrellength)
+    					gt3_1.rot = QuatEuler(90, 0, 0)
+    					gt3_2.rot = QuatEuler(90, 0, 0)
+    				end
+
+    			end
+    			gt3.pos = Vec(0.225, -0.725, -1.95-guardlength)
+
+    		else
+    			gt3.pos = hidePos
+    			gt3_1.pos = hidePos
+    			gt3_2.pos = hidePos
+    		end
+    		if grip == "grenade_launcher" then
+    			gripfactorx = 1.1
+    			gripfactory = 1.1
+    			glt.pos = Vec(0.2, -0.9, -1.4)
+    		else
+    			glt.pos = hidePos
+    		end
+    		if grip == "" then
+    			gripfactorx = 1
+    			gripfactory = 1
+    		end
+
+    		if barrel == "" then
+    			barrelFactorx = 1
+    			barrelFactory = 1
+    			barrelFactordamage = 1
+    			accuracyFactor = 0.7*bipodFactor
+    			barrellength = 0.075
+    			brt0.pos = brt0.pos
+    			if guard == "guard2" then
+    				SetString("savegame.mod.guard", "", true)
+    			end
+    		else
+    			brt0.pos = hidePos
+    		end
+    		if barrel == "barrel1" then
+    			barrelFactorx = 1.2
+    			barrelFactory = 0.95
+    			barrelFactordamage = 1
+    			accuracyFactor = 0.9*bipodFactor
+    			barrellength = -0.125
+    			brt1.pos = brt1.pos
+    			if guard == "" or guard == "guard2" then
+    				SetString("savegame.mod.guard", "guard1", true)
+    			end
+    		else
+    			brt1.pos = hidePos
+    		end
+    		if barrel == "barrel2" then
+    			barrelFactorx = 0.8
+    			barrelFactory = 1.05
+    			barrelFactordamage = 1.15
+    			accuracyFactor = 0.5*bipodFactor
+    			barrellength = 0.375
+    			brt2.pos = brt2.pos
+    		else
+    			brt2.pos = hidePos
+    		end
+
+    		if side == "side1" then
+    			sdt1.pos = sdt1.pos
+    		else
+    			sdt1.pos = hidePos
+    		end
+    		if side == "side2" then
+    			sdt2.pos = sdt2.pos
+    		else
+    			sdt2.pos = hidePos
+    		end
+    		if side == "side3" then
+    			sdt3.pos = sdt3.pos
+    		else
+    			sdt3.pos = hidePos
+    		end
+
+    		if toprail ~= "holo" then
+    			SetString("savegame.mod.magnifier", "", true)
+    		end
+
+    		if mag == "mag3" then
+    			SetString("savegame.mod.foldstock", "", true)
+    		end
+
+    		if guard == "" then
+    			gdt0.pos = Vec(0.225, -0.625, -1.8)
+    			gdt0_2.pos = Vec(0.2, -0.7, -1.8)
+    			guardlength = 0
+    		else
+    			gdt0.pos = hidePos
+    			gdt0_2.pos = hidePos
+    		end
+    		if guard == "guard1" then
+    			gdt1.pos = Vec(0.225, -0.625, -1.8)
+    			gdt1_2.pos = Vec(0.2, -0.7, -1.8)
+    			guardlength = -0.2
+    		else
+    			gdt1.pos = hidePos
+    			gdt1_2.pos = hidePos
+    		end
+    		if guard == "guard2" then
+    			gdt2.pos = Vec(0.225, -0.725, -1.8)
+    			gdt2_2.pos = Vec(0.2, -0.7, -1.8)
+    			guardlength = 0.3
+    		else
+    			gdt2.pos = hidePos
+    			gdt2_2.pos = hidePos
+    		end
+
+    		SetShapeLocalTransform(bolt, bt)
+    		SetShapeLocalTransform(bolt2, bt2)
+    		SetShapeLocalTransform(selector, st)
+    		SetShapeLocalTransform(suppressor, spt)
+    		SetShapeLocalTransform(scope, sct)
+    		SetShapeLocalTransform(scope_2, sct_2)
+    		SetShapeLocalTransform(holo, ht)
+    		SetShapeLocalTransform(holo2, ht2)
+    		SetShapeLocalTransform(reddot, rdt)
+    		SetShapeLocalTransform(reddot2, rdt2)
+    		SetShapeLocalTransform(g33, g33t)
+    		SetShapeLocalTransform(g33_2, g33t2)
+    		SetShapeLocalTransform(rail, rt)
+    		SetShapeLocalTransform(stock0, stt0)
+    		SetShapeLocalTransform(stock1, stt1)
+    		SetShapeLocalTransform(muzzlebreak, mbt)
+    		SetShapeLocalTransform(muzzlebreak2, mbt2)
+    		SetShapeLocalTransform(grip1, gt1)
+    		SetShapeLocalTransform(grip1_2, gt1_2)
+    		SetShapeLocalTransform(grip2, gt2)
+    		SetShapeLocalTransform(grip3, gt3)
+    		SetShapeLocalTransform(grip3_1, gt3_1)
+    		SetShapeLocalTransform(grip3_2, gt3_2)
+    		SetShapeLocalTransform(grip4, glt)
+    		SetShapeLocalTransform(barrel0, brt0)
+    		SetShapeLocalTransform(barrel1, brt1)
+    		SetShapeLocalTransform(barrel2, brt2)
+    		SetShapeLocalTransform(side1, sdt1)
+    		SetShapeLocalTransform(side2, sdt2)
+    		SetShapeLocalTransform(side3, sdt3)
+    		SetShapeLocalTransform(grenade, grt)
+    		SetShapeLocalTransform(guard0, gdt0)
+    		SetShapeLocalTransform(guard0_2, gdt0_2)
+    		SetShapeLocalTransform(guard1, gdt1)
+    		SetShapeLocalTransform(guard1_2, gdt1_2)
+    		SetShapeLocalTransform(guard2, gdt2)
+    		SetShapeLocalTransform(guard2_2, gdt2_2)
+    	end
+
+    	if selectattachments then
+    		clickedmag = clickedmag1 or clickedmag2 or clickedmag3 or clickedmag4
+    		if clickedmag and selectattachments and not InputPressed("t") and not GetBool("level.optionstriggered") then
+    			Reload()
+    		end
+    	end
+    	if reloading and not clickedmag and selectattachments then
+    		selectattachments = false
+    		selectattachmentsTimer = 0.25
+    	end
+
+    	if not selectattachments then
+    		if (InputPressed("r") or clickedmag) and selectfireTimer == 0 then
+    			if not realistic and (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) then
+    				Reload()
+    				inspectTimer = 0
+    			end
+    		end
+
+    		if (InputReleased("r") or clickedmag) and selectfireTimer == 0 then
+    			if realistic and curmagslot ~= nextmagslot then
+    				Reload()
+    				inspectTimer = 0
+    			end
+    		end
+
+    		if GetBool("ammobox.refill") then
+    			SetBool("ammobox.refill", false, true)
+    			mags = mags + 1
+    			PlaySound(refillsound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+
+    		if reloading then
+    			if reloadTimer > 0.4 then
+    				reloadTimer = reloadTimer - dt/reloadFactor
+    			elseif reloadTimer ~= 0 then
+    				reloadTimer = reloadTimer - dt
+    			end
+    			if reloadTimer < 0.5 and not cocksoundplaying and ammo == 0 then
+    				cocksoundplaying = true
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 1)
+    			end
+    			if reloadTimer < 0 then
+    				cocksoundplaying = false
+    				if grenadelauncher then
+    					grenadelauncherammo = 1
+    				else
+    					if realistic then
+    						if ammo == 0 then
+    							ammo = magtable2[curmagslot][2]
+    						else
+    							ammo = magtable2[curmagslot][2] + 1
+    						end
+    					else
+    						if ammo == 0 then
+    							ammo = magsize
+    						else
+    							ammo = magsize + 1
+    						end
+    					end
+    				end
+    				reloadTimer = 0
+    				reloading = false
+    			end
+    		end
+
+    		if selectfireTimer < 0.55 and selectfireTimer > 0 and not selectsoundplaying then
+    			selectsoundplaying = true
+    			PlaySound(selectsound, GetPlayerTransform(playerId).pos, 0.85)
+    		end
+    		if selectfireTimer < 0 then
+    			selectsoundplaying = false
+    			selectfireTimer = 0
+    		end
+
+    	end
+
+    	btrans = GetBodyTransform(b)
+
+    	if InputDown("crouch") then
+    		crouchoffset = math.min(crouchoffset + dt*3, 0.8)
+    	else
+    		crouchoffset = math.max(crouchoffset - dt*3, 0)
+    	end
+    	local x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.8, -2-guardlength, 0, 0, 0
+    	if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.4 then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0.125, -0.5, -1.4, 0, 0, 0
+    	elseif reloading and ammo == 0 and reloadTimer < 0.5 and reloadTimer > 0.2 then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0.15-(reloadTimer-0.2)*1.5, -0.5, -1.5+(0.6-reloadTimer)*0.75, 0, 0, 0
+    	elseif (reloading and ammo > 0) or (reloading and ammo == 0 and reloadTimer > 0.2) then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0+mt.pos[1], 0.4+mt.pos[2], -0.2+mt.pos[3], 0, 0, 0
+    	elseif selectfireTimer ~= 0 then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.825, -0.9, 0, 0, 0
+    	end
+
+    	h1p1l = INS(true, x2, y2, z2, rotx2, roty2, rotz2).pos
+
+    	-- h1p1l = Vec(0.225, -0.85, -1.9)
+    	h1p2l = TransformToLocalPoint(btrans, TransformToParentPoint(GetPlayerTransform(playerId), Vec(-0.6, 0.7-crouchoffset, 0.2)))
+    	hnd1 = Transform(h1p1l, QuatRotateQuat(QuatLookAt(h1p2l, h1p1l), QuatEuler(0,90,90)))
+    	a1p1l = VecAdd(h1p1l, TransformToParentVec(hnd1, Vec(0, 1, 0)))
+    	a1p2l = TransformToLocalPoint(btrans, TransformToParentPoint(GetPlayerTransform(playerId), Vec(-0.45, 1.5-crouchoffset, 0.5)))
+    	amt1 = Transform(a1p1l, QuatRotateQuat(QuatLookAt(a1p2l, a1p1l), QuatEuler(0,90,90)))
+    	SetShapeLocalTransform(hand1, hnd1)
+    	SetShapeLocalTransform(arm1, amt1)
+
+    	h2p1l = Vec(0.275, -0.95, -0.85)
+    	h2p2l = TransformToLocalPoint(btrans, TransformToParentPoint(GetPlayerTransform(playerId), Vec(0.55, 1.1-crouchoffset, 0.9)))
+    	hnd2 = Transform(h2p1l, QuatRotateQuat(QuatLookAt(h2p2l, h2p1l), QuatEuler(0,90,90)))
+    	SetShapeLocalTransform(hand2, hnd2)
+
+    	sightattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.3, -1.2))
+    	muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.575, -2.4-barrellength))
+    	stockattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.55, -0.5))
+    	sideattachpoint = TransformToParentPoint(btrans, Vec(0.2, -0.6, -1.95))
+    	magattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1))
+    	gripattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1.9-guardlength))
+    	barrelattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.6, -1.6))
+    	guardattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.5, -1.8))
+
+    	for key, shell in ipairs(ak47projectileHandler.shells) do
+    		if shell.active then
+    			ProjectileOperations(shell)
+    		end
+    	end
+    	for key, shell in ipairs(ak47grenadeHandler.shells) do
+    		if shell.active then
+    			GrenadeOperations(shell)
+    		end
+    	end
+
+    	if shootTimer > 0 or ammo == 0 then
+    		shootTimer = shootTimer - dt
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "g36k" and GetPlayerVehicle(playerId) == 0 then
+
+    	------SCOPE RETICLE------
+    	if toprail == "scope" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
+    		local gt = GetBodyTransform(GetToolBody())
+    		local sightcenter = Vec(0.275, -0.175, -1.8)
+    		local sightrear = Vec(0.275, -0.175, -1.4)
+    		local gunpos = TransformToParentPoint(gt, sightcenter)
+    		local rearpos = TransformToParentPoint(gt, sightrear)
+    		local fwdpos = TransformToParentVec(gt, Vec(0, 0, -1))
+    		local hit, dist = QueryRaycast(gunpos, fwdpos, 500, 0, true)
+    		local hitpoint = VecAdd(gunpos, VecScale(fwdpos, dist))
+
+    		local camtrans = GetPlayerCameraTransform(playerId)
+    		local sightdist = VecLength(VecSub(camtrans.pos, gunpos))
+
+    		local holopoint = VecAdd(camtrans.pos, VecScale(VecNormalize(VecSub(camtrans.pos, hitpoint)), -sightdist))
+    		UiPush()
+    			local w, h = UiGetImageSize("MOD/img/reticle2.png")
+    			local x, y = UiWorldToPixel(holopoint)
+    			UiTranslate(x-w/2, y-h/2)
+    			UiImage("MOD/img/reticle2.png")
+    		UiPop()
+    		UiPush()
+    			local w, h = UiGetImageSize("MOD/img/reticleoutline.png")
+    			local x, y = UiWorldToPixel(rearpos)
+    			UiTranslate(x-w/2, y-h/2)
+    			UiImage("MOD/img/reticleoutline.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    		UiPop()
+    	elseif toprail == "sight4" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
+    		UiPush()
+    			w, h = UiGetImageSize("MOD/img/reticle3.png")
+    			UiTranslate((UiWidth()-w)/2, (UiHeight()-h)/2-sightadjust*20000)
+    			UiTranslate(-rnd2*50, -(rnd1*50+recoilAngle*150)-recoilTimer*200)
+    			if realistic then
+    				UiTranslate(-math.sin(1.3*GetTime())*6*bipodFactor^4, -math.sin(2.1*GetTime())*4*bipodFactor^4)
+    			end
+    			local speed = math.floor(VecLength(GetPlayerVelocity(playerId))+0.1)
+    			if speed > 1 then
+    				swayy = math.sin(GetTime()*20*speed/7)
+    				swayx = math.sin(GetTime()/reloadFactor*speed)
+    				UiTranslate(-swayx*speed*6, -swayy*speed*4)
+    			end
+    			UiImage("MOD/img/reticle3.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    			UiTranslate(0, h)
+    			UiImage("MOD/img/black.png")
+    		UiPop()
+    	end
+
+    	------IN-GAME UI------
+    	if not realistic and not GetBool("level.optionstriggered") then
+    	if not unlimitedammo then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			if reloading then
+    				UiText("Reloading")
+    			elseif grenadelauncher then
+    				UiText(grenadelauncherammo.."/1 - Grenade")
+    			else
+    				UiText(ammo.."/"..magsize.." - "..selectfireText)
+    			end
+    		UiPop()
+    	else
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			if reloading then
+    				UiText("Reloading")
+    			elseif grenadelauncher then
+    				UiText(grenadelauncherammo.."/1 - Grenade")
+    			else
+    				UiText("Infinite".." - "..selectfireText)
+    			end
+    		UiPop()
+    	end
+    	end
+    	if realistic and not GetBool("level.optionstriggered") then
+    	if magcheckTimer > 0 and magcheckTimer < 2 then
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1, magcheckTimer)
+    		UiFont("bold.ttf", 32)
+    		local checkammo = CheckAmmo(curmagslot)
+    		UiText(checkammo)
+    	end
+    	if selecttextTimer ~= 0 then
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1, selecttextTimer)
+    		UiFont("bold.ttf", 32)
+    		UiText(selectfireText)
+    	end
+    	if jammed and jamclearTimer == 0 then
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiText("Jammed")
+    	elseif jamclearTimer ~= 0 then
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1, jamclearTimer)
+    		UiFont("bold.ttf", 32)
+    		UiText("Jammed")
+    	end
+    	end
+    end
+    if GetString("game.player.tool") == "g36k" and grenadelauncher and not selectattachments then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle")
+    		UiImage("ui/hud/crosshair-launcher.png")
+    	UiPop()
+    end
+    if GetString("game.player.tool") == "g36k" and sideattachment and side == "side3" then
+    	UiPush()
+    		local x,y,dist = UiWorldToPixel(sideattachpoint)
+    		UiTranslate(x, y)
+    		UiAlign("center middle")
+    		UiColor(1, 0.1, 0.1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		UiText(math.floor(range))
+    	UiPop()
+    end
+
+    if realistic and selectmag and GetString("game.player.tool") == "g36k" then
+    	hoverindex=0
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(magattachpoint2)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				for i = 1, totalmags do
+    				clickedslot = MagButton(nextmagslot,i,true,{curx,cury},{"Ammo: ", CheckAmmo(i)},60,60)
+    				UiTranslate(60,0)
+    				curx,cury=curx+60,cury
+    				end
+    			UiPop()
+    		end
+    	UiPop()
+    end
+
+    ------ATTACHMENTS MENU------
+    if not realistic or GetBool("level.optionstriggered") then
+    if selectattachments and GetString("game.player.tool") == "g36k" and GetPlayerVehicle(playerId) == 0 then
+
+    local total = 8
+    gripattachpoint2 = AttachmentGroup("attachmentgroup","grip",gripattachpoint,Description,1/total,60,60)
+    barrelattachpoint2 = AttachmentGroup("attachmentgroup","barrel",barrelattachpoint,Description,2/total,60,60)
+    muzzleattachpoint2 = AttachmentGroup("attachmentgroup","muzzle",muzzleattachpoint,Description,3/total,60,60)
+    sideattachpoint2 = AttachmentGroup("attachmentgroup","side",sideattachpoint,Description,4/total,60,60)
+    guardattachpoint2 = AttachmentGroup("attachmentgroup","guard",guardattachpoint,Description,5/total,60,60)
+    sightattachpoint2 = AttachmentGroup("attachmentgroup","toprail",sightattachpoint,Description,6/total,60,60)
+    stockattachpoint2 = AttachmentGroup("attachmentgroup","stock",stockattachpoint,Description,7/total,60,60)
+    if not realistic then
+    magattachpoint2 = AttachmentGroup("attachmentgroup","mag",magattachpoint,Description,8/total,60,60)
+    end
+
+    hoverindex=0
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(sightattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "toprail" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedscope = AttachmentButton("toprail","sight3",true,{curx,cury},{"Red Dot","1x magnification sight for close range combat."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedholo = AttachmentButton("toprail","holo",true,{curx,cury},{"Holographic Sight","1x magnification sight for close range combat."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				if toprail == "holo" then
+    					clickedmagnifier1 = AttachmentButton("magnifier","g33",true,{curx,cury},{"Thermal Magnifier","Foldable 3x magnifier for close range optics that shows heat signatures. Press 'Z' to fold/unfold."})
+    				end
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(muzzleattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "muzzle" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedmuzzle1 = AttachmentButton("muzzle","muzzle1",true,{curx,cury},{"Suppressor","Suppresses gun noise for sneaky combat."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Compensator","Reduces horizontal recoil, but turns your barrel into a flashbang."})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(stockattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "stock" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedstockremoved = AttachmentButton("stock","removed",true,{curx,cury},{"Stock","Removeable, but decreases overall performance."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedstockremoved = AttachmentButton("stock","stock1",true,{curx,cury},{"Stock","Removeable, but decreases overall performance."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(sideattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "side" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedside1 = AttachmentButton("side","side1",true,{curx,cury},{"Laser","A laser that points where you shoot."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedside2 = AttachmentButton("side","side2",true,{curx,cury},{"Flashlight","Lights up the area in front of you."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedside3 = AttachmentButton("side","side3",true,{curx,cury},{"Rangefinder","Displays the range to your target."})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	if not realistic then
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(magattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "mag" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedmag1 = AttachmentButton("mag","mag1",true,{curx,cury},{"40rnd Mag","Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmag2 = AttachmentButton("mag","mag2",true,{curx,cury},{"50rnd Drum","Pew Pew Pew Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmag3 = AttachmentButton("mag","mag3",true,{curx,cury},{"100rnd Double Drum","Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	end
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(gripattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "grip" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedgrip1 = AttachmentButton("grip","grip1",true,{curx,cury},{"Vertical Grip","Decreased vertical recoil."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedgrip2 = AttachmentButton("grip","grip2",true,{curx,cury},{"Angled Grip","Decreased horizontal recoil."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedgrip3 = AttachmentButton("grip","grip3",true,{curx,cury},{"Bipod","Increased accuracy while crouching or resting the gun on a ledge."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedgrip4 = AttachmentButton("grip","grenade_launcher",true,{curx,cury},{"GP-25","Grenade launcher for increased collateral damage."})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(barrelattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "barrel" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedbarrel1 = AttachmentButton("barrel","barrel1",true,{curx,cury},{"Carbine Barrel","Decreased accuracy but less vertical recoil."})
+    				UiTranslate(-100,0)
+    				curx,cury=curx-70,cury
+    				clickedbarrel2 = AttachmentButton("barrel","barrel2",true,{curx,cury},{"Heavy Barrel","Increased accuracy and damage but more vertical recoil."})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(guardattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "guard" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedguard1 = AttachmentButton("guard","guard1",true,{curx,cury},{"Short Guard","For carbine barrel."})
+    				UiTranslate(-100,0)
+    				curx,cury=curx-70,cury
+    				if barrel == "barrel2" then
+    					clickedguard2 = AttachmentButton("guard","guard2",true,{curx,cury},{"Long Guard","For extended barrel."})
+    				end
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    end
+    end
+    if selectattachments and GetString("game.player.tool") == "g36k" and GetPlayerVehicle(playerId) == 0 or GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
+    hoverindex=0
+    UiPush()
+    	local x,y,dist=UiWorldToPixel(stockattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-70,y)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    			UiAlign("center middle")
+    			if not InputDown("shift") and mag ~= "mag3" then
+    				clickedstockremoved = AttachmentButton("foldstock","removed",true,{curx,cury},{"Fold Stock","Folds stock for a smaller profile weapon."})
+    			end
+    		UiPop()
+    	end
+    UiPop()
+    end
+    if hint and (selectattachments or InputDown("r") and heldrTimer > 0.2) then drawHint(info) end
+
+    ------OPTIONS UI------
+    if GetBool("level.optionstriggered") and GetString("game.player.tool") == "g36k" then
+    UiPush()
+    	UiAlign("center middle")
+    	UiTranslate(UiCenter(), 70)
+    	UiFont("bold.ttf", 60)
+    	UiText("WEAPON MODDING")
+    UiPop()
+    end
+
+    if GetBool("level.optionstriggered") and GetString("game.player.tool") == "g36k" then
+
+    UiAlign("center middle")
+    UiTranslate(300, 300)
+    UiFont("bold.ttf", 48)
+    UiText("G36K")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Unlimited Ammo")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(0.5, 0.8, 1)
+    	if realistic then
+    		UiText("Unvavailable")
+    	else
+    	if unlimitedammo then
+    		if UiTextButton("Yes", 20, 20) then
+    			unlimitedammo = false
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			unlimitedammo = true
+    			SetBool("savegame.mod.unlimitedammo", unlimitedammo, true)
+    		end
+    	end
+    	end
+    UiPop()
+    UiTranslate(0, 80)
+    UiPush()
+    	UiText("Spent Casings")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if spentcasingsoption then
+    		if UiTextButton("Yes", 20, 20) then
+    			spentcasingsoption = false
+    			SetBool("savegame.mod.spentcasingsoption", spentcasingsoption, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			spentcasingsoption = true
+    			SetBool("savegame.mod.spentcasingsoption", spentcasingsoption, true)
+    		end
+    	end
+    UiPop()
+    UiTranslate(0, 80)
+    UiPush()
+    	UiText("Damage: "..damageoption.."%")
+    	UiTranslate(-50, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	damageoption = optionsSlider(damageoption, 50, 1000, 10)
+    	SetInt("savegame.mod.damage", damageoption, true)
+    UiPop()
+
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Realistic Mode")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(0.5, 0.8, 1)
+    	if realistic then
+    		if UiTextButton("Yes", 20, 20) then
+    			realistic = false
+    			SetBool("savegame.mod.realistic", realistic, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			realistic = true
+    			SetBool("savegame.mod.realistic", realistic, true)
+    			SetBool("savegame.mod.unlimitedammo", false, true)
+    		end
+    	end
+    UiPop()
+
+    UiTranslate(0, 100)
+    hoverindex=0
+    if realistic then
+    magtable = {}
+
+    UiPush()
+    	UiTranslate(-180, 150)
+    	MagButton2("mag0", 1, 2, "30rnd Mag")
+    	UiTranslate(60, 0)
+    	MagButton2("mag1", 1, 2, "40rnd Mag")
+    	UiTranslate(90, 0)
+    	MagButton2("mag2", 2, 2, "50rnd Drum")
+    	UiTranslate(150, 0)
+    	MagButton2("mag3", 3, 2, "100rnd Double Drum")
+    UiPop()
+
+    UiPush()
+    	UiAlign("center middle")
+    	UiTranslate(-30*(#slots-1), 20+30*(#slots[1]-1))
+    	for i = 1,#slots do
+    		for j = 1,#slots[i] do
+    			local w, h = slots[i][j][3], slots[i][j][4]
+    			UiTranslate(30*(w-1), 30*(h-1))
+    			local inside2 = UiIsMouseInRect(60*w-1, 60*h-1)
+    			UiTranslate(-30*(w-1), -30*(h-1))
+    			if inside2 then
+    				UiTranslate(30*(w-1), 30*(h-1))
+    				UiImageBox("ui/common/box-solid-6.png", 60*w, 60*h, 6, 6)
+    				UiTranslate(-30*(w-1), -30*(h-1))
+    			elseif slots[i][j][2][1] == i or slots[i][j][2][2] == j or slots[i][j][2][1] == 0 then
+    				UiTranslate(30*(w-1), 30*(h-1))
+    				UiColor(0.1, 0.2, 0.1)
+    				UiImageBox("ui/common/box-solid-6.png", 60*w, 60*h, 6, 6)
+    				UiColor(1, 1, 1)
+    				UiImageBox("ui/common/box-outline-6.png", 60*w, 60*h, 6, 6)
+    				UiTranslate(-30*(w-1), -30*(h-1))
+    			end
+    			UiTranslate(0, -60)
+    		end
+    		UiTranslate(60, 60*#slots[i])
+    	end
+    	UiTranslate(-60*#slots, 0)
+    	for i = 1,#slots do
+    		for j = 1,#slots[i] do
+    			local item, w, h = slots[i][j][1], slots[i][j][3], slots[i][j][4]
+    			UiTranslate(30*(w-1), 30*(h-1))
+    			if slots[i][j][1] ~= "" then
+    				UiImageBox("MOD/icon/"..item..".png", 60*w, 60*h, 0, 0)
+    				table.insert(magtable, item)
+    			end
+    			UiTranslate(-30*(w-1), -30*(h-1))
+    			if not InputDown("lmb") and UiIsMouseInRect(59, 59) and grabbed[1][1] ~= "" then
+    				placeItem(grabbed, i, j)
+    				grabbed = {{"", {0, 0}, 1, 1}, 0, 0}
+    			end
+    			if InputPressed("lmb") and UiIsMouseInRect(60, 60) then
+    				if slots[i][j][1] ~= "" then
+    					local w, h = slots[i][j][3], slots[i][j][4]
+    					grabbed = {slots[i][j], i, j}
+    					slots[i][j] = {"", {0, 0}, w, h}
+    				elseif slots[i][j][2][1] ~= 0 then
+    					local a = slots[i][j][2][1][1]
+    					local b = slots[i][j][2][1][2]
+    					local w, h = slots[a][b][3], slots[a][b][4]
+    					grabbed = {slots[a][b], a, b}
+    					slots[a][b] = {"", {0, 0}, w, h}
+    				end
+    			end
+    			UiTranslate(0, -60)
+    		end
+    		UiTranslate(60, 60*#slots[i])
+    	end
+    	if grabbed[1][1] ~= "" then
+    		local item, w, h = grabbed[1][1], grabbed[1][3], grabbed[1][4]
+    		local x, y = UiGetMousePos()
+    		UiTranslate(x+30*(w-1), y+30*(h-1))
+    		UiImageBox("MOD/icon/"..item..".png", 60*w, 60*h, 0, 0)
+    	end
+    	if not InputDown("lmb") and grabbed[1][1] ~= "" then
+    		clearItem(grabbed)
+    		grabbed = {{"", {0, 0}, 1, 1}, 0, 0}
+    	end
+    UiPop()
+
+    SetInt("savegame.mod.totalmags", #magtable, true)
+    for i = 1, #magtable do
+    	SetString("savegame.mod.mslot"..i, magtable[i], true)
+    end
+    end
+
+    if realistic then
+    	UiTranslate(0, 240)
+    end
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
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
@@ -1,7 +1,11 @@
-function init()
-	StartLevel("","MOD/room.xml")
+#version 2
+function server.init()
+    StartLevel("","MOD/room.xml")
 end
 
-function tick()
-	StartLevel("","MOD/room.xml")
-end+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        StartLevel("","MOD/room.xml")
+    end
+end
+

```

---

# Migration Report: options2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/options2.lua
+++ patched/options2.lua
@@ -1,9 +1,13 @@
-function tick(dt)
-	SetString("game.player.tool","g36k")
-	SetBool("level.optionstriggered",true)
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetString("game.player.tool","g36k", true)
+        SetBool("level.optionstriggered",true, true)
+    end
 end
 
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-end+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+end
+

```
