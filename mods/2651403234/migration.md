# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,207 +1,4 @@
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
-	RegisterTool("saiga12", "Saiga-12", "MOD/vox/saiga12.vox", 3)
-	SetBool("game.tool.saiga12.enabled", true)
-	SetFloat("game.tool.saiga12.ammo", 101)
-
-	damage = 0.1 * GetInt("savegame.mod.damage")/100
-	if damage == 0 then
-		damage = 0.1
-	end
-	gravity = Vec(0, -10, 0)
-	hidePos = Vec(0, -200, 0)
-	hideTrans = Transform(hidePos,QuatEuler())
-	velocity = 400
-	drag = 2
-	maxMomentum = 1
-	tracer = false
-	pelletSpread = 1
-	pelletAmount = 8
-	pelletDamage = damage
-
-	recoilVertical = 2.5
-	recoilHorizontal = 9
-	recoilWander = 8
-
-	--armor pen
-	lvl5armor = 0
-	lvl4armor = 0
-	lvl3armor = 0
-	lvl2armor = 0.4
-	lvl1armor = 1
-
-	inside = {}
-	for i = 1,50 do
-		inside[i] = {0,0,0,0}
-	end
-	hoverindex = 0
-
-	gunsound = LoadSound("MOD/snd/ak0.ogg")
-	suppressedgunsound = LoadSound("MOD/snd/aksuppressed.ogg")
-	grenadelaunchersound = LoadSound("MOD/snd/grenadelauncher.ogg")
-	toprail = GetString("savegame.mod.toprail")
-	muzzle = GetString("savegame.mod.muzzle")
-	stock = GetString("savegame.mod.stock")
-	mag = GetString("savegame.mod.mag")
-	grip = GetString("savegame.mod.grip")
-	barrel = GetString("savegame.mod.barrel")
-	side = GetString("savegame.mod.side")
-	cocksound = LoadSound("MOD/snd/guncock.ogg")
-	reloadsound = LoadSound("MOD/snd/reload.ogg")
-	reloadsound2 = LoadSound("MOD/snd/reload2.ogg")
-	dryfiresound = LoadSound("MOD/snd/dryfire.ogg")
-	refillsound = LoadSound("MOD/snd/refill.ogg")
-	selectsound = LoadSound("MOD/snd/selectorswitch.ogg")
-	casingsound = LoadSound("MOD/snd/casingsound.ogg")
-	interactsound1 = LoadSound("MOD/snd/interact1.ogg")
-	interactsound2 = LoadSound("MOD/snd/interact2.ogg")
-	interactsound3 = LoadSound("MOD/snd/interact3.ogg")
-	uiselect = LoadSound("MOD/snd/uiselect.ogg")
-
-	reloadTime = 2.4
-	shotDelay = 0.125
-	spreadTimer = 1.25
-	spreadFactor = 1.5
-	accuracyFactor = 1
-	if mag == "" then
-		magsize = 5
-		reloadFactor = 1
-	elseif mag == "mag1" then
-		magsize = 10
-		reloadFactor = 1.15
-	elseif mag == "mag2" then
-		magsize = 20
-		reloadFactor = 1.35
-	else
-		magsize = 95
-		reloadFactor = 1.5
-	end
-	barrellength = 0
-	barrelFactorx = 0.8
-	barrelFactory = 1.5
-	barrelFactordamage = 1.25
-	ammo = magsize
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
-	recoilTimer2 = 0
-	recoilAngle = 0
-	recoilFactor = 0
-	stockFactor = 0
-	muzzleFactor = 0
-	muzzlelength = 0
-	gripfactorx = 0
-	gripfactory = 0
-	recoilMax = 0
-	rnd1, rnd2, rnd3, rnd4, rnd5, rnd6 = 0, 0, 0, 0, 0, 0
-	lightTimer = 0
-	clickedmag = false
-	animationTimers = {0, 0, 0, 0, 0}
-	fovTimer = 0
-	animation1Timer = 0
-
-	magoutTimer = 0
-	maginTimer = 0
-	meleeTimer = 0
-	cocksoundplaying = false
-	reloadsound2playing = true
-	selectsoundplaying = false
-	selectattachments = false
-	selectattachmentsTimer = 0
-	inspectTimer = 0
-
-	e = false
-	q = false
-	selectfire = 2
-	selectfire0 = 1
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
@@ -274,21 +71,20 @@
 	loadedShell.predictedBulletVelocity = VecAdd(loadedShell.predictedBulletVelocity, Vec((math.random()-0.5)*pelletSpread*barrelFactorspread, (math.random()-0.5)*pelletSpread*barrelFactorspread, (math.random()-0.5)*pelletSpread*barrelFactorspread))
 	end
 
-
 	local barrelend = barrellength + muzzlelength
-	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.02), GetPlayerVelocity()), 0.3, 0.3)
+	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.02), GetPlayerVelocity(playerId)), 0.3, 0.3)
 	ParticleType("plain")
 	ParticleTile(5)
 	ParticleColor(1, 0.6, 0.4, 1, 0.3, 0.2)
 	ParticleRadius(0.1)
 	ParticleEmissive(5, 1)
-	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.04), GetPlayerVelocity()), 0.2, 0.3)
+	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.04), GetPlayerVelocity(playerId)), 0.2, 0.3)
 	if muzzle == "muzzle1" then
-		PlaySound(suppressedgunsound, GetPlayerTransform().pos, 1, false)
+		PlaySound(suppressedgunsound, GetPlayerTransform(playerId).pos, 1, false)
 	elseif muzzle == "muzzle2" then
-		PlaySound(gunsound, GetPlayerTransform().pos, 1, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 1, false)
 	else
-		PlaySound(gunsound, GetPlayerTransform().pos, 0.75, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.75, false)
 	end
 
 	if not unlimitedammo then
@@ -330,7 +126,7 @@
 	ak47grenadeHandler.shellNum = (ak47grenadeHandler.shellNum%#ak47grenadeHandler.shells) + 1
 
 	SpawnParticle("fire", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(grenadelaunchersound, GetPlayerTransform().pos, 0.75, false)
+	PlaySound(grenadelaunchersound, GetPlayerTransform(playerId).pos, 0.75, false)
 
 	if not unlimitedammo then
 		grenadelauncherammo = grenadelauncherammo - 1
@@ -426,7 +222,7 @@
 
 			local factor = barrelFactordamage
 
-			if projectile.momentum > 0 then
+			if projectile.momentum ~= 0 then
 				MakeHole(hitPos, damage*factor, damage*0.85*factor, damage*0.7*factor)
 			end
 		end
@@ -468,7 +264,7 @@
 	end
 	reloading = true
 	if not grenadelauncher then
-		PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+		PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	end
 	if grenadelauncher then
 		if grenadelauncherammo == 0 then
@@ -503,7 +299,7 @@
 	local gt = GetBodyTransform(GetToolBody())
 	local casingpos = TransformToParentPoint(gt, Vec(0.55, -0.6, -1.15))
 	local fwdpos = TransformToParentPoint(gt, Vec(6+math.random()*4, 0.5+math.random()*4, -0.65+math.random()*4))
-	local direction = VecAdd(GetPlayerVelocity(), VecSub(fwdpos, casingpos))
+	local direction = VecAdd(GetPlayerVelocity(playerId), VecSub(fwdpos, casingpos))
 	casing = Spawn("MOD/vox/casing.xml", Transform(casingpos, QuatEuler(math.random(0, 90), math.random(0, 90), math.random(0, 90))))
 	SetBodyVelocity(casing[1], direction)
 end
@@ -548,17 +344,17 @@
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
@@ -610,6 +406,7 @@
 			laserFactor = 1
 		end
 end
+
 function Flashlight(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.175, -0.625, -1.9))
@@ -628,6 +425,7 @@
 			SetShapeEmissiveScale(side2, 0)
 		end
 end
+
 function Rangefinder(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.175, -0.625, -1.9))
@@ -704,27 +502,27 @@
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
@@ -788,32 +586,32 @@
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
@@ -865,32 +663,32 @@
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
@@ -942,32 +740,32 @@
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
@@ -1019,32 +817,32 @@
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
@@ -1071,1281 +869,1465 @@
 	return offset
 end
 
-function tick(dt)
-	if GetString("game.player.tool") == "saiga12" and GetPlayerVehicle() == 0 then
-		SetBool("hud.aimdot", false)
-		
-		if InputDown("lmb") and not reloading and selectfire == 1 and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-			end
-		elseif InputPressed("lmb") and not reloading and selectfire == 2 and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-				shootTimer = 0.11
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
-		end
-
-		
-		if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and GetPlayerGrabShape() == 0 and not InputDown("shift") then
-			if InputPressed("rmb") then
-				PlaySound(interactsound1, GetPlayerTransform().pos, 1)
-			end
-			ironsight = true
-			inspectTimer = 0
-		end
-		if not InputDown("rmb") then
-			ironsight = false
-		end
-		if selectfire == 0 then
-			ironsight = false
-		end
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
-		if InputPressed("x") and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") then
-			meleeTimer = 0.8
-		end
-
-		if InputPressed("v") and not reloading and not selectattachments then
-			SelectFire()
-			inspectTimer = 0
-		end
-
-		if InputDown("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") then
-			if InputPressed("t") then
-				PlaySound(interactsound2, GetPlayerTransform().pos, 1)
-				selectattachmentsTimer = 0.5
-			end
-			UiMakeInteractive()
-			selectattachments = true
-			ironsight = false
-			inspectTimer = 0
-		end
-		if InputReleased("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") then
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
-		if selectfire == 1 then
-			selectfireText = "Full"
-		elseif selectfire == 2 then
-			selectfireText = "Semi"
-		else
-			selectfireText = "Safe"
-		end
-
-		if shootTimer <= 0 then
-			recoverySpeed = 0.1
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
-			recoilFactor = recoilVertical*stockFactor
-		else
-			recoilFactor = recoilVertical*stockFactor*1.75
-		end
-
-		if ironsight then
-			recoilMax = 30*muzzleFactor*gripfactory*barrelFactory*stockFactor
-		else
-			recoilMax = 50*muzzleFactor*gripfactory*barrelFactory*stockFactor
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
-		if maginTimer > 0 then
-			mag = GetString("savegame.mod.mag")
-		end
-		grip = GetString("savegame.mod.grip")
-		barrel = GetString("savegame.mod.barrel")
-		side = GetString("savegame.mod.side")
-		ammotype = GetString("savegame.mod.ammotype")
-		if ammotype == "" then
-			SetString("savegame.mod.ammotype", "Buckshot")
-			maxMomentum = 1.1
-			pelletSpread = 12
-			pelletAmount = 8
-			pelletDamage = damage
-		elseif ammotype == "Birdshot" then
-			maxMomentum = 0.6
-			pelletSpread = 24
-			pelletAmount = 16
-			pelletDamage = damage*0.8
-		elseif ammotype == "Slugs" then
-			maxMomentum = 1
-			pelletSpread = 1
-			pelletAmount = 1
-			pelletDamage = damage*2
-		else
-			maxMomentum = 1.1
-			pelletSpread = 12
-			pelletAmount = 8
-			pelletDamage = damage
-		end
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local magoffset = Vec(0, 0, 0)
-			local grenadeoffset = Vec(-0.025, 0.025, 0)
-			local boltoffset = Vec(0, 0, 0)
-			local selectoroffset = Transform()
-			local suppressoroffset = Transform()
-			local scopeoffset = Transform()
-			local holooffset = Transform()
-			local holooffset2 = Transform()
-			local railoffset = Transform()
-			local magtimer = magoutTimer + maginTimer
-			offset = Transform(Vec(0, heightOffset, 0))
-			local x, y, z, rot = 0.275, 0, 0, 0
-			local adsFOV, adsTime = 0, 0
-			local defaultTrans = Transform(Vec(0.25, 0.15, 0.25), QuatEuler(0, 0, 0))
-
-			x,y,z,rotx,roty,rotz = -0.1,0.2,0.2,0,0,0
-			if ironsight then
-			if grenadelauncher then
-				x = 0
-				y = 0.45
-				z = 0.2
-				rotz = 0
-			elseif q then
-				x = 0.8
-				y = 0.15
-				z = 0.4
-				rotz = 30
-			elseif e then
-				x = -0.3
-				y = 0.4
-				z = 0.3
-				rotz = -15
-			else
-				if toprail == "holo" then
-					x = 0.275
-					y = 0.2625
-					z = 0.2
-					rotz = 0
-				elseif toprail == "" then
-					x = 0.275
-					y = 0.325
-					z = 0.2
-					rotz = 0
-				elseif toprail == "scope" then
-					x = 0.275
-					y = 0.25
-					z = 0.4
-					rotz = 0
-				end
-			end
-
-			if reloading then
-				adsFOV, adsTime = 0, 0.15
-			elseif not (q or e or grenadelauncher) then
-				if toprail == "" then
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
-			-- offset = ADS(ironsight, adsFOV, adsTime, -x, y, z, rotz)
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
-				if toprail == "holo" and not (q or e) then
-					local gt = GetBodyTransform(GetToolBody())
-					local sightcenter = Vec(0.275, -0.1875, -1.5)
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
-						DrawSprite(reticle1, holotrans, 0.025, 0.025, 1, 1, 1, 1, true)
-					end
-				end
-				if toprail == "scope" then
-					scopepoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.252, -1.45), QuatEuler(0, 180, 0)))
-					reticle2 = LoadSprite("MOD/img/reticle2.png")
-					DrawSprite(reticle2, scopepoint, 0.05, 0.05, 1, 1, 1, 1, true)
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
-						if GetShapeMaterialAtPosition(shape, stockPos) == "glass" and math.random() > 0.8 then
-							MakeHole(stockPos, 1)
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
-			if recoilTimer2 > 0 then
-				recoilTimer2 = recoilTimer2 - dt*recoilTimer2*4
-				-- offset.pos = VecAdd(offset.pos, Vec(0, -recoilTimer2/4, recoilTimer2))
-				-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer2-0.02)*16, 0, 0))
-			end
-			if recoilTimer > 0 then
-				recoilTimer = recoilTimer - dt
-				boltoffset = Vec(-0.001, -0.001, recoilTimer*4)
-			end
-			if recoilTimer < 0 then
-				recoilTimer = 0
-			end
-			if recoilTimer2 < 0 then
-				recoilTimer2 = 0
-			end
-			local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/200, (recoilAngle/-200)-(rnd1+rnd4)/200-recoilTimer2/4, recoilAngle/75+(rnd3+rnd6)/200+recoilTimer2/1.5+recoilTimer2/4, recoilAngle+(rnd1+rnd4)/4+(recoilTimer2-0.02)*4+(recoilTimer2-0.02)*8, (rnd2+rnd5)/4, (rnd3+rnd6)/4
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
-				PlaySound(interactsound3, GetPlayerTransform().pos, 0.5, false)
-			end
-			if maginTimer < 0.3 and not reloadsound2playing then
-					PlaySound(reloadsound2, GetPlayerTransform().pos, 0.6, false)
-					reloadsound2playing = true
-			end
-			if maginTimer < 0 then
-				maginTimer = 0
-				if grenadelauncher then
-					PlaySound(uiselect, GetPlayerTransform().pos, 1)
-				end
-			end
-			if magoutTimer > 0 then
-				if grenadelauncher then
-					grenadeoffset = Vec(-0.025, -magoutTimer*3+0.025, -0.6)
-				else
-					if magoutTimer >= 0.3 then
-						magoffset = Vec(0, 0, -(0.6-magoutTimer)*1.5)
-					elseif magoutTimer < 0.3 then
-						magoffset = Vec(0, -(0.3-magoutTimer)*6, -0.45)
-					
-					end
-				end
-				magoutTimer = magoutTimer - dt/reloadFactor
-			end
-			if maginTimer > 0 then
-				if grenadelauncher then
-					grenadeoffset = Vec(-0.025, 0.025, -maginTimer)
-				else
-					if maginTimer >= 0.2 then
-						magoffset = Vec(0, -(maginTimer-0.2)*4, -0.45)
-					elseif maginTimer < 0.2 then
-						magoffset = Vec(0, 0, -(maginTimer)*2.25)
-					end
-				end
-				maginTimer = maginTimer - dt/reloadFactor
-			end
-			if not grenadelauncher or (grenadelauncherammo == 0 and not reloading) then
-				grenadeoffset = hidePos
-			end
-
-			local x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 0, 0, 0
-			if reloading then
-			if grenadelauncher then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 5, -10
-			elseif ironsight then
-				if q then
-					if magoutTimer > 0.4 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.075, 0.1, 0, 0, 0, -10
-					elseif magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 0, -10
-					elseif maginTimer > 0 or reloadTimer > 0.8 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 10, -5
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.25, 0.25, -0.2, -10, 5, -40
-					end
-				elseif e then
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.1, 0, 5, -10, -10
-					elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, -0.1, -5, 15, 0
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = -1, -1.3, -0.4, 50, -50, 80
-					end
-				else
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.3, -0.05, 0, 0, 0, -20
-					elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) or (reloadTimer > 1 and ammo == 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.4, 0.05, 0, 0, 0, -25
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.35, 0.2, -0.2, -10, 5, -40
-					else
-						x1, y1, z1, rotx1, roty1, rotz1 = -0.05, 0, 0, 0, 0, 0
-					end
-				end
-			else
-				if magoutTimer > 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.15, -0.05, 0, 5, -5, -20
-				elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.35, -0.05, 0.1, 10, 10, -25
-				elseif reloadTimer < 0.8 and ammo == 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = -0.8, -0.9, -0.4, 40, -40, 55
-				end
-			end
-			end
-
-			-- RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
-			-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
-
-			if reloadTimer < 0.5 and reloadTimer > 0.2 and reloading and ammo == 0 then
-				boltoffset = Vec(-0.01, 0, (0.5-reloadTimer)*0.75)
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
-			end
-
-			-- INSoffset = INS(inspectTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
-			-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
-
-			local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0.4, 0.4, -0.2, -20, 60, 0
-			elseif ironsight and q and selectfireTimer > 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			elseif ironsight and selectfireTimer > 0  then
-				x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, 0, 0, 5, 30
-			elseif selectfireTimer > 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = -0.4, -0.3, 0.25, 0, 5, 50
-			else
-				x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			end
-
-			-- SELoffset = SEL((selectfireTimer > 0 or selectfire == 0 or InputDown("shift")) and not reloading, x3, y3, z3, rotx3, roty3, rotz3)
-			-- offset.pos = VecAdd(offset.pos, SELoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, SELoffset.rot)
-
-			offset = ADS(true, adsFOV, adsTime, -x+x1+x2+x3+ATToffset[1]-swingx2/100, y+y1+y2+y3+ATToffset[2]+swingy2/100, z+z1+z2+z3+ATToffset[3], rotx+rotx1+rotx2+rotx3+swingy-swingy2+swayy*speed+ATToffset[4], roty+roty1+roty2+roty3+swingx-swingx2+swayx*speed+ATToffset[5], rotz+rotz1+rotz2+rotz3+ATToffset[6])
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
-			for i = 30, 41 do
-				SetShapeLocalTransform(bs[i], hideTrans)
-			end
-			if clothingtype == "camo" then
-				hand1 = bs[33]
-				arm1 = bs[35]
-				hand2 = bs[34]
-			elseif clothingtype == "swat" then
-				hand1 = bs[36]
-				arm1 = bs[38]
-				hand2 = bs[37]
-			elseif clothingtype == "camo2" then
-				hand1 = bs[39]
-				arm1 = bs[41]
-				hand2 = bs[40]
-			else
-				hand1 = bs[30]
-				arm1 = bs[32]
-				hand2 = bs[31]
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
-				selector = shapes[4]
-				suppressor = shapes[5]
-				scope = shapes[6]
-				holo = shapes[7]
-				holo2 = shapes[8]
-				rail = shapes[9]
-				stock1 = shapes[10]
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
-				magTrans = GetShapeLocalTransform(mag0)
-				boltTrans = GetShapeLocalTransform(bolt)
-				selectorTrans = GetShapeLocalTransform(selector)
-				suppressorTrans = GetShapeLocalTransform(suppressor)
-				scopeTrans = GetShapeLocalTransform(scope)
-				holoTrans = GetShapeLocalTransform(holo)
-				holoTrans2 = GetShapeLocalTransform(holo2)
-				railTrans = GetShapeLocalTransform(rail)
-				stock1Trans = GetShapeLocalTransform(stock1)
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
-			end
-
-			mt = TransformCopy(magTrans)
-			mt.pos = VecAdd(mt.pos, magoffset)
-
-			bt = TransformCopy(boltTrans)
-			bt.pos = VecAdd(bt.pos, boltoffset)
-
-			st = TransformCopy(selectorTrans)
-			st.pos = VecAdd(st.pos, selectoroffset)
-
-			spt = TransformCopy(suppressorTrans)
-			spt.pos = VecAdd(spt.pos, suppressoroffset)
-
-			sct = TransformCopy(scopeTrans)
-			sct.pos = VecAdd(sct.pos, scopeoffset)
-
-			ht = TransformCopy(holoTrans)
-			ht.pos = VecAdd(ht.pos, holooffset)
-			ht2 = TransformCopy(holoTrans2)
-			ht2.pos = VecAdd(ht.pos, holooffset)
-
-			rt = TransformCopy(railTrans)
-			rt.pos = VecAdd(rt.pos, railoffset)
-
-			stt = TransformCopy(stock1Trans)
-			stt.pos = VecAdd(stt.pos, stock1offset)
-
-			mbt = TransformCopy(muzzlebreakTrans)
-			mbt.pos = VecAdd(mbt.pos, muzzlebreakoffset)
-			mbt2 = TransformCopy(muzzlebreakTrans2)
-			mbt2.pos = VecAdd(mbt2.pos, muzzlebreakoffset2)
-
-			gt1 = TransformCopy(gripTrans)
-			gt1.pos = VecAdd(gt1.pos, gripoffset)
-			gt1_2 = TransformCopy(gripTrans)
-			gt1_2.pos = VecAdd(gt1_2.pos, gripoffset)
-
-			gt2 = TransformCopy(gripTrans)
-			gt2.pos = VecAdd(gt2.pos, gripoffset)
-
-			gt3 = TransformCopy(gripTrans)
-			gt3.pos = VecAdd(gt3.pos, gripoffset)
-			gt3_1 = TransformCopy(gripTrans)
-			gt3_1.pos = VecAdd(gt3_1.pos, gripoffset)
-			gt3_2 = TransformCopy(gripTrans)
-			gt3_2.pos = VecAdd(gt3_2.pos, gripoffset)
-
-			glt = TransformCopy(gripTrans)
-			glt.pos = VecAdd(glt.pos, gripoffset)
-
-			bt0 = TransformCopy(barrelTrans0)
-			bt0.pos = VecAdd(bt0.pos, barreloffset)
-
-			bt1 = TransformCopy(barrelTrans1)
-			bt1.pos = VecAdd(bt1.pos, barreloffset)
-
-			bt2 = TransformCopy(barrelTrans2)
-			bt2.pos = VecAdd(bt2.pos, barreloffset)
-
-			sdt1 = TransformCopy(sideTrans1)
-			sdt1.pos = VecAdd(sdt1.pos, sideoffset)
-			sdt2 = TransformCopy(sideTrans2)
-			sdt2.pos = VecAdd(sdt2.pos, sideoffset)
-			sdt3 = TransformCopy(sideTrans3)
-			sdt3.pos = VecAdd(sdt3.pos, sideoffset)
-
-			grt = TransformCopy(grenadeTrans)
-			grt.pos = VecAdd(grt.pos, grenadeoffset)
-
-			if not grenadelauncher then
-				if magoutTimer > 0 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler((0.6-magoutTimer)*120, 0, 0))
-				elseif maginTimer >= 0.2 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(30, 0, 0))
-				elseif maginTimer > 0 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(maginTimer*180, 0, 0))
-				end
-			end
-
-			if selectfireTimer < 0.4 then
-				if selectfire == 1 then
-					st.rot = QuatEuler(-90, 0, 0)
-				elseif selectfire == 2 then
-					st.rot = QuatEuler(-100, 0, 0)
-				else
-					st.rot = QuatEuler(-70, 0, 0)
-				end
-			elseif selectfireTimer > 0 then
-				if selectfire0 == 1 then
-					st.rot = QuatEuler(-90, 0, 0)
-				elseif selectfire0 == 2 then
-					st.rot = QuatEuler(-105, 0, 0)
-				else
-					st.rot = QuatEuler(-70, 0, 0)
-				end
-			end
-
-			muzzlelength = 0
-			if muzzle == "muzzle1" then
-				spt.pos = VecAdd(spt.pos, Vec(0.075, 0, -barrellength))
-				spt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 0.4
-				muzzlelength = 0.6
-			else
-				spt.pos = hidePos
-				spt.rot = QuatEuler(0, 0, 0)
-				lightFactor = 2
-				muzzleFactor = 1
-			end
-			if muzzle == "muzzle2" then
-				mbt.pos = VecAdd(mbt.pos, Vec(0.075, 0, -barrellength))
-				mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0.05, -barrellength))
-				mbt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 3
-				muzzleFactor = 0.75
-				muzzlelength = 0.2
-			else
-				mbt.pos = hidePos
-				mbt2.pos = hidePos
-				mbt.rot = QuatEuler(0, 0, 0)
-				lightFactor = 2
-				muzzleFactor = 1
-			end
-			if toprail == "scope" then
-				sct.pos = Vec(0.2, -0.425, -1.375)
-			else
-				sct.pos = hidePos
-			end
-			if toprail == "holo" then
-				ht.pos = Vec(0.175, -0.425, -1.375)
-				ht2.pos = Vec(0.225, -0.35, -1.375)
-			else
-				ht.pos = hidePos
-				ht2.pos = hidePos
-			end
-			if stock == "removed" then
-				stt.pos = Vec(0.2, -0.95, -1.3)
-				stt.rot = QuatEuler(-90, 180, 0)
-				stockFactor = 2.5
-			else
-				stt.pos = Vec(0.2, -0.95, 0.2)
-				stt.rot = QuatEuler(-90, 0, 0)
-				stockFactor = 1
-			end
-			rt.pos = Vec(0.175, -0.725, -0.625)
-
-			if mag == "" then
-				magsize = 5
-				reloadFactor = 1.1
-				SetShapeLocalTransform(mag0, mt)
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-				SetShapeLocalTransform(mag3, hideTrans)
-			elseif mag == "mag1" then
-				magsize = 10
-				reloadFactor = 1.35
-				SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(0, -0.3, 0)), mt.rot))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-				SetShapeLocalTransform(mag3, hideTrans)
-			elseif mag == "mag2" then
-				magsize = 20
-				reloadFactor = 1.8
-				SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.175, -0.2, -0.2)), QuatRotateQuat(mt.rot, QuatEuler(20, 0, 0))))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag3, hideTrans)
-			elseif mag == "mag3" then
-				magsize = 95
-				reloadFactor = 2.25
-				SetShapeLocalTransform(mag3, Transform(VecAdd(mt.pos, Vec(-0.45, 0.15, 0)), mt.rot))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-			end
-
-			if grip == "grip1" then
-				gripfactorx = 0.85
-				gripfactory = 0.6
-				gt1.pos = Vec(0.2, -0.85, -1.575)
-				gt1_2.pos = Vec(0.225, -0.95, -1.6)
-			else
-				gt1.pos = hidePos
-				gt1_2.pos = hidePos
-			end
-			if grip == "grip2" then
-				gripfactorx = 0.6
-				gripfactory = 0.85
-				gt2.pos = Vec(0.25, -0.9, -1.5)
-			else
-				gt2.pos = hidePos
-			end
-			if grip == "grip3" then
-				local querypos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2-barrellength*4/3))
-				local hit, dist = QueryRaycast(querypos, Vec(0, -2, 0), 5, 0.2)
-				local bipodded = (InputDown("ctrl") or dist < 0.4) and selectfire > 0
-				if bipodded then
-					gripfactorx = 0.4
-					gripfactory = 0.4
-					gt3_1.pos = Vec(0.4, -1.35, -2.05-barrellength*4/3)
-					gt3_2.pos = Vec(0.05, -1.325, -2.05-barrellength*4/3)
-					gt3_1.rot = QuatEuler(0, 0, 10)
-					gt3_2.rot = QuatEuler(0, 0, -10)
-				else
-					gripfactorx = 1
-					gripfactory = 1
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
-				gt3.pos = Vec(0.225, -0.725, -1.95-barrellength)
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
-				accuracyFactor = 0.9
-				barrelFactorspread = 1
-				barrellength = 0.25
-				bt1.pos = bt1.pos
-			else
-				bt1.pos = hidePos
-			end
-			if barrel == "barrel1" then
-				barrelFactorx = 1.2
-				barrelFactory = 0.8
-				barrelFactordamage = 1
-				accuracyFactor = 1.1
-				barrelFactorspread = 1.3
-				barrellength = 0
-				bt0.pos = bt0.pos
-			else
-				bt0.pos = hidePos
-			end
-			if barrel == "barrel2" then
-				barrelFactorx = 0.8
-				barrelFactory = 1.3
-				barrelFactordamage = 1.2
-				accuracyFactor = 0.7
-				barrelFactorspread = 0.8
-				barrellength = 0.75
-				bt2.pos = bt2.pos
-			else
-				bt2.pos = hidePos
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
-			if mag == "mag2" or mag == "mag3" then
-				SetString("savegame.mod.stock", "")
-			end
-
-			SetShapeLocalTransform(bolt, bt)
-			SetShapeLocalTransform(selector, st)
-			SetShapeLocalTransform(suppressor, spt)
-			SetShapeLocalTransform(scope, sct)
-			SetShapeLocalTransform(holo, ht)
-			SetShapeLocalTransform(holo2, ht2)
-			SetShapeLocalTransform(rail, rt)
-			SetShapeLocalTransform(stock1, stt)
-			SetShapeLocalTransform(muzzlebreak, mbt)
-			SetShapeLocalTransform(muzzlebreak2, mbt2)
-			SetShapeLocalTransform(grip1, gt1)
-			SetShapeLocalTransform(grip1_2, gt1_2)
-			SetShapeLocalTransform(grip2, gt2)
-			SetShapeLocalTransform(grip3, gt3)
-			SetShapeLocalTransform(grip3_1, gt3_1)
-			SetShapeLocalTransform(grip3_2, gt3_2)
-			SetShapeLocalTransform(grip4, glt)
-			SetShapeLocalTransform(barrel0, bt0)
-			SetShapeLocalTransform(barrel1, bt1)
-			SetShapeLocalTransform(barrel2, bt2)
-			SetShapeLocalTransform(side1, sdt1)
-			SetShapeLocalTransform(side2, sdt2)
-			SetShapeLocalTransform(side3, sdt3)
-			SetShapeLocalTransform(grenade, grt)
-		end
-
-		if selectattachments then
-			clickedmag = clickedmag1 or clickedmag2 or clickedmag3
-			if clickedmag and selectattachments and not InputPressed("t") then
-				Reload()
-			end
-		end
-		if reloading and not clickedmag and selectattachments then
-			selectattachments = false
-			selectattachmentsTimer = 0.25
-		end
-
-		if not selectattachments then
-			if (InputPressed("R") or clickedmag) and selectfireTimer == 0 then
-				if (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) then
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
-				if reloadTimer > 0.5 then
-					reloadTimer = reloadTimer - dt/reloadFactor
-				elseif reloadTimer > 0 then
-					reloadTimer = reloadTimer - dt
-				end
-				if reloadTimer < 0.6 and not cocksoundplaying and ammo == 0 then
-					cocksoundplaying = true
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.85)
-				end
-				if reloadTimer < 0 then
-					cocksoundplaying = false
-					if grenadelauncher then
-						grenadelauncherammo = 1
-					else
-						if ammo == 0 then
-							ammo = magsize
-						else
-							ammo = magsize + 1
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
-		local x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.8, -1.9, 0, 0, 0
-		if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.2 then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0.3, -0.6, -0.3+bt.pos[3], 0, 0, 0
-		elseif reloading then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0+mt.pos[1], 0.15+mt.pos[2], -0.1+mt.pos[3], 0, 0, 0
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
-		sightattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.15, -1))
-		muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.35, -2.5))
-		stockattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.4, -0.6))
-		sideattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.45, -1.65))
-		magattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.65, -1))
-		gripattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.85, -1.4))
-		barrelattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.65, -1.6))
-		ammoattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.8, -0.75))
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
+function math.clamp(n, low, high) return math.min(math.max(n, low), high) end
+
+function server.init()
+    RegisterTool("saiga12", "Saiga-12", "MOD/vox/saiga12.vox", 3)
+    SetBool("game.tool.saiga12.enabled", true, true)
+    SetFloat("game.tool.saiga12.ammo", 101, true)
+    damage = 0.1 * GetInt("savegame.mod.damage")/100
+    if damage == 0 then
+    	damage = 0.1
+    end
+    gravity = Vec(0, -10, 0)
+    hidePos = Vec(0, -200, 0)
+    hideTrans = Transform(hidePos,QuatEuler())
+    velocity = 400
+    drag = 2
+    maxMomentum = 1
+    tracer = false
+    pelletSpread = 1
+    pelletAmount = 8
+    pelletDamage = damage
+    recoilVertical = 2.5
+    recoilHorizontal = 9
+    recoilWander = 8
+    --armor pen
+    lvl5armor = 0
+    lvl4armor = 0
+    lvl3armor = 0
+    lvl2armor = 0.4
+    lvl1armor = 1
+    inside = {}
+    for i = 1,50 do
+    	inside[i] = {0,0,0,0}
+    end
+    hoverindex = 0
+    toprail = GetString("savegame.mod.toprail")
+    muzzle = GetString("savegame.mod.muzzle")
+    stock = GetString("savegame.mod.stock")
+    mag = GetString("savegame.mod.mag")
+    grip = GetString("savegame.mod.grip")
+    barrel = GetString("savegame.mod.barrel")
+    side = GetString("savegame.mod.side")
+    reloadTime = 2.4
+    shotDelay = 0.125
+    spreadTimer = 1.25
+    spreadFactor = 1.5
+    accuracyFactor = 1
+    if mag == "" then
+    	magsize = 5
+    	reloadFactor = 1
+    elseif mag == "mag1" then
+    	magsize = 10
+    	reloadFactor = 1.15
+    elseif mag == "mag2" then
+    	magsize = 20
+    	reloadFactor = 1.35
+    else
+    	magsize = 95
+    	reloadFactor = 1.5
+    end
+    barrellength = 0
+    barrelFactorx = 0.8
+    barrelFactory = 1.5
+    barrelFactordamage = 1.25
+    ammo = magsize
+    grenadelauncherammo = 1
+    reloading = false
+    ironsight = false
+    ADSx = 0
+    ADSy = 0
+    ADSz = 0
+    ADSrotx = 0
+    ADSroty = 0
+    ADSrotz = 0
+    ADSx0 = 0
+    ADSy0 = 0
+    ADSz0 = 0
+    ADSrotx0 = 0
+    ADSroty0 = 0
+    ADSrotz0 = 0
+    ADSdelta = {0,0,0,0,0,0}
+    ADSfov = 0
+    RELx = 0
+    RELy = 0
+    RELz = 0
+    RELrotx = 0
+    RELroty = 0
+    RELrotz = 0
+    SELx = 0
+    SELy = 0
+    SELz = 0
+    SELrotx = 0
+    SELroty = 0
+    SELrotz = 0
+    INSx = 0
+    INSy = 0
+    INSz = 0
+    INSrotx = 0
+    INSroty = 0
+    INSrotz = 0
+    RECx = 0
+    RECy = 0
+    RECz = 0
+    RECrotx = 0
+    RECroty = 0
+    RECrotz = 0
+    RECx0 = 0
+    RECy0 = 0
+    RECz0 = 0
+    RECrotx0 = 0
+    RECroty0 = 0
+    RECrotz0 = 0
+    RECdelta = {0,0,0,0,0,0}
+    crouchoffset = 0
+    sideattachment = false
+    range = 0
+    grenadelauncher = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    spentcasingsoption = GetBool("savegame.mod.spentcasingsoption")
+    for i=1, 200 do
+    	ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    end
+    for i=1, 10 do
+    	ak47grenadeHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    recoilTimer2 = 0
+    recoilAngle = 0
+    recoilFactor = 0
+    stockFactor = 0
+    muzzleFactor = 0
+    muzzlelength = 0
+    gripfactorx = 0
+    gripfactory = 0
+    recoilMax = 0
+    rnd1, rnd2, rnd3, rnd4, rnd5, rnd6 = 0, 0, 0, 0, 0, 0
+    lightTimer = 0
+    clickedmag = false
+    animationTimers = {0, 0, 0, 0, 0}
+    fovTimer = 0
+    animation1Timer = 0
+    magoutTimer = 0
+    maginTimer = 0
+    meleeTimer = 0
+    cocksoundplaying = false
+    reloadsound2playing = true
+    selectsoundplaying = false
+    selectattachments = false
+    selectattachmentsTimer = 0
+    inspectTimer = 0
+    e = false
+    q = false
+    selectfire = 2
+    selectfire0 = 1
+    selectfireTimer = 0
+    selectfireText = "Semi"
+    sin1 = 0
+    cos1 = 1
+    sin2 = 0
+    cos2 = 1
+    swayx = 0
+    swayy = 0
+    swingx = 0
+    swingy = 0
+    swingx2 = 0
+    swingy2 = 0
 end
 
-function draw()
-	if GetString("game.player.tool") == "saiga12" and GetPlayerVehicle() == 0 then
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
-					UiText("Infinite")
-				end
-			UiPop()
-		end
-	end
-	if GetString("game.player.tool") == "saiga12" and grenadelauncher and not selectattachments then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle")
-			UiImage("ui/hud/crosshair-launcher.png")
-		UiPop()
-	end
-	if GetString("game.player.tool") == "saiga12" and sideattachment and side == "side3" then
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
-	if selectattachments then
-	if hint then drawHint(info) end
-	hoverindex=0
-		UiPush()
-			local x,y,dist=UiWorldToPixel(sightattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedholo = AttachmentButton("toprail","holo",true,{curx,cury},{"Holographic Sight","1x magnification sight for close range combat."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(muzzleattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedmuzzle1 = AttachmentButton("muzzle","muzzle1",true,{curx,cury},{"Suppressor","Suppresses gun noise for sneaky combat."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Muzzle Break","Reduces recoil, but turns your barrel into a flashbang."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(stockattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					if mag == "" or mag == "mag1" then
-						UiAlign("center middle")
-						clickedstockremoved = AttachmentButton("stock","removed",true,{curx,cury},{"Stock","Foldable for badasses only."})
-						UiTranslate(-70,0)
-					end
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(sideattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
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
-		UiPush()
-			local x,y,dist=UiWorldToPixel(magattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedmag1 = AttachmentButton("mag","mag1",true,{curx,cury},{"10rnd Mag","Pew Pew Pew"})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmag2 = AttachmentButton("mag","mag2",true,{curx,cury},{"20rnd Drum","Pew Pew Pew Pew Pew Pew"})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(gripattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedgrip1 = AttachmentButton("grip","grip1",true,{curx,cury},{"Vertical Grip","Decreased vertical recoil."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedgrip2 = AttachmentButton("grip","grip2",true,{curx,cury},{"Angled Grip","Decreased horizontal recoil."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(barrelattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedbarrel1 = AttachmentButton("barrel","barrel1",true,{curx,cury},{"Short Barrel","Increased spread but less vertical recoil."})
-					UiTranslate(-140,0)
-					curx,cury=curx-70,cury
-					clickedbarrel2 = AttachmentButton("barrel","barrel2",true,{curx,cury},{"Long Barrel","Increased accuracy and damage but more vertical recoil."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(ammoattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedammo1 = AttachmentButton("ammotype","Buckshot",true,{curx,cury},{"Buckshot","8 Pellets. Medium damage."})
-					UiTranslate(-100,0)
-					curx,cury=curx-70,cury
-					clickedammo2 = AttachmentButton("ammotype","Birdshot",true,{curx,cury},{"Birdshot","16 Pellets. Low damage."})
-					UiTranslate(-100,0)
-					curx,cury=curx-70,cury
-					clickedammo1 = AttachmentButton("ammotype","Slugs",true,{curx,cury},{"Slugs","1 Pellet. Pakcs a big punch"})
-					UiTranslate(-100,0)
-					curx,cury=curx-70,cury
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-	end
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
+    interactsound3 = LoadSound("MOD/snd/interact3.ogg")
+    uiselect = LoadSound("MOD/snd/uiselect.ogg")
 end
 
-function math.clamp(n, low, high) return math.min(math.max(n, low), high) end+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "saiga12" and GetPlayerVehicle(playerId) == 0 then
+    	SetBool("hud.aimdot", false, true)
+
+    	if InputDown("lmb") and not reloading and selectfire == 1 and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    		end
+    	elseif InputPressed("lmb") and not reloading and selectfire == 2 and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    			shootTimer = 0.11
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
+    	end
+
+    	if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") then
+    		if InputPressed("rmb") then
+    			PlaySound(interactsound1, GetPlayerTransform(playerId).pos, 1)
+    		end
+    		ironsight = true
+    		inspectTimer = 0
+    	end
+    	if not InputDown("rmb") then
+    		ironsight = false
+    	end
+    	if selectfire == 0 then
+    		ironsight = false
+    	end
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
+    	if InputPressed("x") and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") then
+    		meleeTimer = 0.8
+    	end
+
+    	if InputPressed("v") and not reloading and not selectattachments then
+    		SelectFire()
+    		inspectTimer = 0
+    	end
+
+    	if InputDown("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") then
+    		if InputPressed("t") then
+    			PlaySound(interactsound2, GetPlayerTransform(playerId).pos, 1)
+    			selectattachmentsTimer = 0.5
+    		end
+    		UiMakeInteractive()
+    		selectattachments = true
+    		ironsight = false
+    		inspectTimer = 0
+    	end
+    	if InputReleased("t") and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") then
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
+    	if selectfire == 1 then
+    		selectfireText = "Full"
+    	elseif selectfire == 2 then
+    		selectfireText = "Semi"
+    	else
+    		selectfireText = "Safe"
+    	end
+
+    	if shootTimer <= 0 then
+    		recoverySpeed = 0.1
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
+    		recoilFactor = recoilVertical*stockFactor
+    	else
+    		recoilFactor = recoilVertical*stockFactor*1.75
+    	end
+
+    	if ironsight then
+    		recoilMax = 30*muzzleFactor*gripfactory*barrelFactory*stockFactor
+    	else
+    		recoilMax = 50*muzzleFactor*gripfactory*barrelFactory*stockFactor
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
+    	if maginTimer ~= 0 then
+    		mag = GetString("savegame.mod.mag")
+    	end
+    	grip = GetString("savegame.mod.grip")
+    	barrel = GetString("savegame.mod.barrel")
+    	side = GetString("savegame.mod.side")
+    	ammotype = GetString("savegame.mod.ammotype")
+    	if ammotype == "" then
+    		SetString("savegame.mod.ammotype", "Buckshot", true)
+    		maxMomentum = 1.1
+    		pelletSpread = 12
+    		pelletAmount = 8
+    		pelletDamage = damage
+    	elseif ammotype == "Birdshot" then
+    		maxMomentum = 0.6
+    		pelletSpread = 24
+    		pelletAmount = 16
+    		pelletDamage = damage*0.8
+    	elseif ammotype == "Slugs" then
+    		maxMomentum = 1
+    		pelletSpread = 1
+    		pelletAmount = 1
+    		pelletDamage = damage*2
+    	else
+    		maxMomentum = 1.1
+    		pelletSpread = 12
+    		pelletAmount = 8
+    		pelletDamage = damage
+    	end
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local magoffset = Vec(0, 0, 0)
+    		local grenadeoffset = Vec(-0.025, 0.025, 0)
+    		local boltoffset = Vec(0, 0, 0)
+    		local selectoroffset = Transform()
+    		local suppressoroffset = Transform()
+    		local scopeoffset = Transform()
+    		local holooffset = Transform()
+    		local holooffset2 = Transform()
+    		local railoffset = Transform()
+    		local magtimer = magoutTimer + maginTimer
+    		offset = Transform(Vec(0, heightOffset, 0))
+    		local x, y, z, rot = 0.275, 0, 0, 0
+    		local adsFOV, adsTime = 0, 0
+    		local defaultTrans = Transform(Vec(0.25, 0.15, 0.25), QuatEuler(0, 0, 0))
+
+    		x,y,z,rotx,roty,rotz = -0.1,0.2,0.2,0,0,0
+    		if ironsight then
+    		if grenadelauncher then
+    			x = 0
+    			y = 0.45
+    			z = 0.2
+    			rotz = 0
+    		elseif q then
+    			x = 0.8
+    			y = 0.15
+    			z = 0.4
+    			rotz = 30
+    		elseif e then
+    			x = -0.3
+    			y = 0.4
+    			z = 0.3
+    			rotz = -15
+    		else
+    			if toprail == "holo" then
+    				x = 0.275
+    				y = 0.2625
+    				z = 0.2
+    				rotz = 0
+    			elseif toprail == "" then
+    				x = 0.275
+    				y = 0.325
+    				z = 0.2
+    				rotz = 0
+    			elseif toprail == "scope" then
+    				x = 0.275
+    				y = 0.25
+    				z = 0.4
+    				rotz = 0
+    			end
+    		end
+
+    		if reloading then
+    			adsFOV, adsTime = 0, 0.15
+    		elseif not (q or e or grenadelauncher) then
+    			if toprail == "" then
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
+    		-- offset = ADS(ironsight, adsFOV, adsTime, -x, y, z, rotz)
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
+    			if toprail == "holo" and not (q or e) then
+    				local gt = GetBodyTransform(GetToolBody())
+    				local sightcenter = Vec(0.275, -0.1875, -1.5)
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
+    					DrawSprite(reticle1, holotrans, 0.025, 0.025, 1, 1, 1, 1, true)
+    				end
+    			end
+    			if toprail == "scope" then
+    				scopepoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.252, -1.45), QuatEuler(0, 180, 0)))
+    				reticle2 = LoadSprite("MOD/img/reticle2.png")
+    				DrawSprite(reticle2, scopepoint, 0.05, 0.05, 1, 1, 1, 1, true)
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
+    					if GetShapeMaterialAtPosition(shape, stockPos) == "glass" and math.random() > 0.8 then
+    						MakeHole(stockPos, 1)
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
+    		if recoilTimer2 ~= 0 then
+    			recoilTimer2 = recoilTimer2 - dt*recoilTimer2*4
+    			-- offset.pos = VecAdd(offset.pos, Vec(0, -recoilTimer2/4, recoilTimer2))
+    			-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer2-0.02)*16, 0, 0))
+    		end
+    		if recoilTimer ~= 0 then
+    			recoilTimer = recoilTimer - dt
+    			boltoffset = Vec(-0.001, -0.001, recoilTimer*4)
+    		end
+    		if recoilTimer < 0 then
+    			recoilTimer = 0
+    		end
+    		if recoilTimer2 < 0 then
+    			recoilTimer2 = 0
+    		end
+    		local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/200, (recoilAngle/-200)-(rnd1+rnd4)/200-recoilTimer2/4, recoilAngle/75+(rnd3+rnd6)/200+recoilTimer2/1.5+recoilTimer2/4, recoilAngle+(rnd1+rnd4)/4+(recoilTimer2-0.02)*4+(recoilTimer2-0.02)*8, (rnd2+rnd5)/4, (rnd3+rnd6)/4
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
+    			PlaySound(interactsound3, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    		if maginTimer < 0.3 and not reloadsound2playing then
+    				PlaySound(reloadsound2, GetPlayerTransform(playerId).pos, 0.6, false)
+    				reloadsound2playing = true
+    		end
+    		if maginTimer < 0 then
+    			maginTimer = 0
+    			if grenadelauncher then
+    				PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
+    			end
+    		end
+    		if magoutTimer ~= 0 then
+    			if grenadelauncher then
+    				grenadeoffset = Vec(-0.025, -magoutTimer*3+0.025, -0.6)
+    			else
+    				if magoutTimer >= 0.3 then
+    					magoffset = Vec(0, 0, -(0.6-magoutTimer)*1.5)
+    				elseif magoutTimer < 0.3 then
+    					magoffset = Vec(0, -(0.3-magoutTimer)*6, -0.45)
+
+    				end
+    			end
+    			magoutTimer = magoutTimer - dt/reloadFactor
+    		end
+    		if maginTimer ~= 0 then
+    			if grenadelauncher then
+    				grenadeoffset = Vec(-0.025, 0.025, -maginTimer)
+    			else
+    				if maginTimer >= 0.2 then
+    					magoffset = Vec(0, -(maginTimer-0.2)*4, -0.45)
+    				elseif maginTimer < 0.2 then
+    					magoffset = Vec(0, 0, -(maginTimer)*2.25)
+    				end
+    			end
+    			maginTimer = maginTimer - dt/reloadFactor
+    		end
+    		if not grenadelauncher or (grenadelauncherammo == 0 and not reloading) then
+    			grenadeoffset = hidePos
+    		end
+
+    		local x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 0, 0, 0
+    		if reloading then
+    		if grenadelauncher then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 5, -10
+    		elseif ironsight then
+    			if q then
+    				if magoutTimer > 0.4 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.075, 0.1, 0, 0, 0, -10
+    				elseif magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 0, -10
+    				elseif maginTimer > 0 or reloadTimer > 0.8 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 10, -5
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.25, 0.25, -0.2, -10, 5, -40
+    				end
+    			elseif e then
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.1, 0, 5, -10, -10
+    				elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, -0.1, -5, 15, 0
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = -1, -1.3, -0.4, 50, -50, 80
+    				end
+    			else
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.3, -0.05, 0, 0, 0, -20
+    				elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) or (reloadTimer > 1 and ammo == 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.4, 0.05, 0, 0, 0, -25
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.35, 0.2, -0.2, -10, 5, -40
+    				else
+    					x1, y1, z1, rotx1, roty1, rotz1 = -0.05, 0, 0, 0, 0, 0
+    				end
+    			end
+    		else
+    			if magoutTimer ~= 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.15, -0.05, 0, 5, -5, -20
+    			elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.35, -0.05, 0.1, 10, 10, -25
+    			elseif reloadTimer < 0.8 and ammo == 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = -0.8, -0.9, -0.4, 40, -40, 55
+    			end
+    		end
+    		end
+
+    		-- RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
+    		-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
+
+    		if reloadTimer < 0.5 and reloadTimer > 0.2 and reloading and ammo == 0 then
+    			boltoffset = Vec(-0.01, 0, (0.5-reloadTimer)*0.75)
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
+    		end
+
+    		-- INSoffset = INS(inspectTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
+    		-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
+
+    		local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0.4, 0.4, -0.2, -20, 60, 0
+    		elseif ironsight and q and selectfireTimer ~= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		elseif ironsight and selectfireTimer ~= 0  then
+    			x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, 0, 0, 5, 30
+    		elseif selectfireTimer ~= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = -0.4, -0.3, 0.25, 0, 5, 50
+    		else
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		end
+
+    		-- SELoffset = SEL((selectfireTimer > 0 or selectfire == 0 or InputDown("shift")) and not reloading, x3, y3, z3, rotx3, roty3, rotz3)
+    		-- offset.pos = VecAdd(offset.pos, SELoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, SELoffset.rot)
+
+    		offset = ADS(true, adsFOV, adsTime, -x+x1+x2+x3+ATToffset[1]-swingx2/100, y+y1+y2+y3+ATToffset[2]+swingy2/100, z+z1+z2+z3+ATToffset[3], rotx+rotx1+rotx2+rotx3+swingy-swingy2+swayy*speed+ATToffset[4], roty+roty1+roty2+roty3+swingx-swingx2+swayx*speed+ATToffset[5], rotz+rotz1+rotz2+rotz3+ATToffset[6])
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
+    		for i = 30, 41 do
+    			SetShapeLocalTransform(bs[i], hideTrans)
+    		end
+    		if clothingtype == "camo" then
+    			hand1 = bs[33]
+    			arm1 = bs[35]
+    			hand2 = bs[34]
+    		elseif clothingtype == "swat" then
+    			hand1 = bs[36]
+    			arm1 = bs[38]
+    			hand2 = bs[37]
+    		elseif clothingtype == "camo2" then
+    			hand1 = bs[39]
+    			arm1 = bs[41]
+    			hand2 = bs[40]
+    		else
+    			hand1 = bs[30]
+    			arm1 = bs[32]
+    			hand2 = bs[31]
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
+    			selector = shapes[4]
+    			suppressor = shapes[5]
+    			scope = shapes[6]
+    			holo = shapes[7]
+    			holo2 = shapes[8]
+    			rail = shapes[9]
+    			stock1 = shapes[10]
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
+    			magTrans = GetShapeLocalTransform(mag0)
+    			boltTrans = GetShapeLocalTransform(bolt)
+    			selectorTrans = GetShapeLocalTransform(selector)
+    			suppressorTrans = GetShapeLocalTransform(suppressor)
+    			scopeTrans = GetShapeLocalTransform(scope)
+    			holoTrans = GetShapeLocalTransform(holo)
+    			holoTrans2 = GetShapeLocalTransform(holo2)
+    			railTrans = GetShapeLocalTransform(rail)
+    			stock1Trans = GetShapeLocalTransform(stock1)
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
+    		end
+
+    		mt = TransformCopy(magTrans)
+    		mt.pos = VecAdd(mt.pos, magoffset)
+
+    		bt = TransformCopy(boltTrans)
+    		bt.pos = VecAdd(bt.pos, boltoffset)
+
+    		st = TransformCopy(selectorTrans)
+    		st.pos = VecAdd(st.pos, selectoroffset)
+
+    		spt = TransformCopy(suppressorTrans)
+    		spt.pos = VecAdd(spt.pos, suppressoroffset)
+
+    		sct = TransformCopy(scopeTrans)
+    		sct.pos = VecAdd(sct.pos, scopeoffset)
+
+    		ht = TransformCopy(holoTrans)
+    		ht.pos = VecAdd(ht.pos, holooffset)
+    		ht2 = TransformCopy(holoTrans2)
+    		ht2.pos = VecAdd(ht.pos, holooffset)
+
+    		rt = TransformCopy(railTrans)
+    		rt.pos = VecAdd(rt.pos, railoffset)
+
+    		stt = TransformCopy(stock1Trans)
+    		stt.pos = VecAdd(stt.pos, stock1offset)
+
+    		mbt = TransformCopy(muzzlebreakTrans)
+    		mbt.pos = VecAdd(mbt.pos, muzzlebreakoffset)
+    		mbt2 = TransformCopy(muzzlebreakTrans2)
+    		mbt2.pos = VecAdd(mbt2.pos, muzzlebreakoffset2)
+
+    		gt1 = TransformCopy(gripTrans)
+    		gt1.pos = VecAdd(gt1.pos, gripoffset)
+    		gt1_2 = TransformCopy(gripTrans)
+    		gt1_2.pos = VecAdd(gt1_2.pos, gripoffset)
+
+    		gt2 = TransformCopy(gripTrans)
+    		gt2.pos = VecAdd(gt2.pos, gripoffset)
+
+    		gt3 = TransformCopy(gripTrans)
+    		gt3.pos = VecAdd(gt3.pos, gripoffset)
+    		gt3_1 = TransformCopy(gripTrans)
+    		gt3_1.pos = VecAdd(gt3_1.pos, gripoffset)
+    		gt3_2 = TransformCopy(gripTrans)
+    		gt3_2.pos = VecAdd(gt3_2.pos, gripoffset)
+
+    		glt = TransformCopy(gripTrans)
+    		glt.pos = VecAdd(glt.pos, gripoffset)
+
+    		bt0 = TransformCopy(barrelTrans0)
+    		bt0.pos = VecAdd(bt0.pos, barreloffset)
+
+    		bt1 = TransformCopy(barrelTrans1)
+    		bt1.pos = VecAdd(bt1.pos, barreloffset)
+
+    		bt2 = TransformCopy(barrelTrans2)
+    		bt2.pos = VecAdd(bt2.pos, barreloffset)
+
+    		sdt1 = TransformCopy(sideTrans1)
+    		sdt1.pos = VecAdd(sdt1.pos, sideoffset)
+    		sdt2 = TransformCopy(sideTrans2)
+    		sdt2.pos = VecAdd(sdt2.pos, sideoffset)
+    		sdt3 = TransformCopy(sideTrans3)
+    		sdt3.pos = VecAdd(sdt3.pos, sideoffset)
+
+    		grt = TransformCopy(grenadeTrans)
+    		grt.pos = VecAdd(grt.pos, grenadeoffset)
+
+    		if not grenadelauncher then
+    			if magoutTimer ~= 0 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler((0.6-magoutTimer)*120, 0, 0))
+    			elseif maginTimer >= 0.2 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(30, 0, 0))
+    			elseif maginTimer ~= 0 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(maginTimer*180, 0, 0))
+    			end
+    		end
+
+    		if selectfireTimer < 0.4 then
+    			if selectfire == 1 then
+    				st.rot = QuatEuler(-90, 0, 0)
+    			elseif selectfire == 2 then
+    				st.rot = QuatEuler(-100, 0, 0)
+    			else
+    				st.rot = QuatEuler(-70, 0, 0)
+    			end
+    		elseif selectfireTimer ~= 0 then
+    			if selectfire0 == 1 then
+    				st.rot = QuatEuler(-90, 0, 0)
+    			elseif selectfire0 == 2 then
+    				st.rot = QuatEuler(-105, 0, 0)
+    			else
+    				st.rot = QuatEuler(-70, 0, 0)
+    			end
+    		end
+
+    		muzzlelength = 0
+    		if muzzle == "muzzle1" then
+    			spt.pos = VecAdd(spt.pos, Vec(0.075, 0, -barrellength))
+    			spt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 0.4
+    			muzzlelength = 0.6
+    		else
+    			spt.pos = hidePos
+    			spt.rot = QuatEuler(0, 0, 0)
+    			lightFactor = 2
+    			muzzleFactor = 1
+    		end
+    		if muzzle == "muzzle2" then
+    			mbt.pos = VecAdd(mbt.pos, Vec(0.075, 0, -barrellength))
+    			mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0.05, -barrellength))
+    			mbt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 3
+    			muzzleFactor = 0.75
+    			muzzlelength = 0.2
+    		else
+    			mbt.pos = hidePos
+    			mbt2.pos = hidePos
+    			mbt.rot = QuatEuler(0, 0, 0)
+    			lightFactor = 2
+    			muzzleFactor = 1
+    		end
+    		if toprail == "scope" then
+    			sct.pos = Vec(0.2, -0.425, -1.375)
+    		else
+    			sct.pos = hidePos
+    		end
+    		if toprail == "holo" then
+    			ht.pos = Vec(0.175, -0.425, -1.375)
+    			ht2.pos = Vec(0.225, -0.35, -1.375)
+    		else
+    			ht.pos = hidePos
+    			ht2.pos = hidePos
+    		end
+    		if stock == "removed" then
+    			stt.pos = Vec(0.2, -0.95, -1.3)
+    			stt.rot = QuatEuler(-90, 180, 0)
+    			stockFactor = 2.5
+    		else
+    			stt.pos = Vec(0.2, -0.95, 0.2)
+    			stt.rot = QuatEuler(-90, 0, 0)
+    			stockFactor = 1
+    		end
+    		rt.pos = Vec(0.175, -0.725, -0.625)
+
+    		if mag == "" then
+    			magsize = 5
+    			reloadFactor = 1.1
+    			SetShapeLocalTransform(mag0, mt)
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    			SetShapeLocalTransform(mag3, hideTrans)
+    		elseif mag == "mag1" then
+    			magsize = 10
+    			reloadFactor = 1.35
+    			SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(0, -0.3, 0)), mt.rot))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    			SetShapeLocalTransform(mag3, hideTrans)
+    		elseif mag == "mag2" then
+    			magsize = 20
+    			reloadFactor = 1.8
+    			SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.175, -0.2, -0.2)), QuatRotateQuat(mt.rot, QuatEuler(20, 0, 0))))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag3, hideTrans)
+    		elseif mag == "mag3" then
+    			magsize = 95
+    			reloadFactor = 2.25
+    			SetShapeLocalTransform(mag3, Transform(VecAdd(mt.pos, Vec(-0.45, 0.15, 0)), mt.rot))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    		end
+
+    		if grip == "grip1" then
+    			gripfactorx = 0.85
+    			gripfactory = 0.6
+    			gt1.pos = Vec(0.2, -0.85, -1.575)
+    			gt1_2.pos = Vec(0.225, -0.95, -1.6)
+    		else
+    			gt1.pos = hidePos
+    			gt1_2.pos = hidePos
+    		end
+    		if grip == "grip2" then
+    			gripfactorx = 0.6
+    			gripfactory = 0.85
+    			gt2.pos = Vec(0.25, -0.9, -1.5)
+    		else
+    			gt2.pos = hidePos
+    		end
+    		if grip == "grip3" then
+    			local querypos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2-barrellength*4/3))
+    			local hit, dist = QueryRaycast(querypos, Vec(0, -2, 0), 5, 0.2)
+    			local bipodded = (InputDown("ctrl") or dist < 0.4) and selectfire > 0
+    			if bipodded then
+    				gripfactorx = 0.4
+    				gripfactory = 0.4
+    				gt3_1.pos = Vec(0.4, -1.35, -2.05-barrellength*4/3)
+    				gt3_2.pos = Vec(0.05, -1.325, -2.05-barrellength*4/3)
+    				gt3_1.rot = QuatEuler(0, 0, 10)
+    				gt3_2.rot = QuatEuler(0, 0, -10)
+    			else
+    				gripfactorx = 1
+    				gripfactory = 1
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
+    			gt3.pos = Vec(0.225, -0.725, -1.95-barrellength)
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
+    			accuracyFactor = 0.9
+    			barrelFactorspread = 1
+    			barrellength = 0.25
+    			bt1.pos = bt1.pos
+    		else
+    			bt1.pos = hidePos
+    		end
+    		if barrel == "barrel1" then
+    			barrelFactorx = 1.2
+    			barrelFactory = 0.8
+    			barrelFactordamage = 1
+    			accuracyFactor = 1.1
+    			barrelFactorspread = 1.3
+    			barrellength = 0
+    			bt0.pos = bt0.pos
+    		else
+    			bt0.pos = hidePos
+    		end
+    		if barrel == "barrel2" then
+    			barrelFactorx = 0.8
+    			barrelFactory = 1.3
+    			barrelFactordamage = 1.2
+    			accuracyFactor = 0.7
+    			barrelFactorspread = 0.8
+    			barrellength = 0.75
+    			bt2.pos = bt2.pos
+    		else
+    			bt2.pos = hidePos
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
+    		if mag == "mag2" or mag == "mag3" then
+    			SetString("savegame.mod.stock", "", true)
+    		end
+
+    		SetShapeLocalTransform(bolt, bt)
+    		SetShapeLocalTransform(selector, st)
+    		SetShapeLocalTransform(suppressor, spt)
+    		SetShapeLocalTransform(scope, sct)
+    		SetShapeLocalTransform(holo, ht)
+    		SetShapeLocalTransform(holo2, ht2)
+    		SetShapeLocalTransform(rail, rt)
+    		SetShapeLocalTransform(stock1, stt)
+    		SetShapeLocalTransform(muzzlebreak, mbt)
+    		SetShapeLocalTransform(muzzlebreak2, mbt2)
+    		SetShapeLocalTransform(grip1, gt1)
+    		SetShapeLocalTransform(grip1_2, gt1_2)
+    		SetShapeLocalTransform(grip2, gt2)
+    		SetShapeLocalTransform(grip3, gt3)
+    		SetShapeLocalTransform(grip3_1, gt3_1)
+    		SetShapeLocalTransform(grip3_2, gt3_2)
+    		SetShapeLocalTransform(grip4, glt)
+    		SetShapeLocalTransform(barrel0, bt0)
+    		SetShapeLocalTransform(barrel1, bt1)
+    		SetShapeLocalTransform(barrel2, bt2)
+    		SetShapeLocalTransform(side1, sdt1)
+    		SetShapeLocalTransform(side2, sdt2)
+    		SetShapeLocalTransform(side3, sdt3)
+    		SetShapeLocalTransform(grenade, grt)
+    	end
+
+    	if selectattachments then
+    		clickedmag = clickedmag1 or clickedmag2 or clickedmag3
+    		if clickedmag and selectattachments and not InputPressed("t") then
+    			Reload()
+    		end
+    	end
+    	if reloading and not clickedmag and selectattachments then
+    		selectattachments = false
+    		selectattachmentsTimer = 0.25
+    	end
+
+    	if not selectattachments then
+    		if (InputPressed("R") or clickedmag) and selectfireTimer == 0 then
+    			if (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) then
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
+    			if reloadTimer > 0.5 then
+    				reloadTimer = reloadTimer - dt/reloadFactor
+    			elseif reloadTimer ~= 0 then
+    				reloadTimer = reloadTimer - dt
+    			end
+    			if reloadTimer < 0.6 and not cocksoundplaying and ammo == 0 then
+    				cocksoundplaying = true
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.85)
+    			end
+    			if reloadTimer < 0 then
+    				cocksoundplaying = false
+    				if grenadelauncher then
+    					grenadelauncherammo = 1
+    				else
+    					if ammo == 0 then
+    						ammo = magsize
+    					else
+    						ammo = magsize + 1
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
+    	local x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.8, -1.9, 0, 0, 0
+    	if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.2 then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0.3, -0.6, -0.3+bt.pos[3], 0, 0, 0
+    	elseif reloading then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0+mt.pos[1], 0.15+mt.pos[2], -0.1+mt.pos[3], 0, 0, 0
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
+    	sightattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.15, -1))
+    	muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.35, -2.5))
+    	stockattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.4, -0.6))
+    	sideattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.45, -1.65))
+    	magattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.65, -1))
+    	gripattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.85, -1.4))
+    	barrelattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.65, -1.6))
+    	ammoattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.8, -0.75))
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
+    if GetString("game.player.tool") == "saiga12" and GetPlayerVehicle(playerId) == 0 then
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
+    				UiText("Infinite")
+    			end
+    		UiPop()
+    	end
+    end
+    if GetString("game.player.tool") == "saiga12" and grenadelauncher and not selectattachments then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle")
+    		UiImage("ui/hud/crosshair-launcher.png")
+    	UiPop()
+    end
+    if GetString("game.player.tool") == "saiga12" and sideattachment and side == "side3" then
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
+    if selectattachments then
+    if hint then drawHint(info) end
+    hoverindex=0
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(sightattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedholo = AttachmentButton("toprail","holo",true,{curx,cury},{"Holographic Sight","1x magnification sight for close range combat."})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(muzzleattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedmuzzle1 = AttachmentButton("muzzle","muzzle1",true,{curx,cury},{"Suppressor","Suppresses gun noise for sneaky combat."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Muzzle Break","Reduces recoil, but turns your barrel into a flashbang."})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(stockattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				if mag == "" or mag == "mag1" then
+    					UiAlign("center middle")
+    					clickedstockremoved = AttachmentButton("stock","removed",true,{curx,cury},{"Stock","Foldable for badasses only."})
+    					UiTranslate(-70,0)
+    				end
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(sideattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
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
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(magattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedmag1 = AttachmentButton("mag","mag1",true,{curx,cury},{"10rnd Mag","Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmag2 = AttachmentButton("mag","mag2",true,{curx,cury},{"20rnd Drum","Pew Pew Pew Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(gripattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedgrip1 = AttachmentButton("grip","grip1",true,{curx,cury},{"Vertical Grip","Decreased vertical recoil."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedgrip2 = AttachmentButton("grip","grip2",true,{curx,cury},{"Angled Grip","Decreased horizontal recoil."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(barrelattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedbarrel1 = AttachmentButton("barrel","barrel1",true,{curx,cury},{"Short Barrel","Increased spread but less vertical recoil."})
+    				UiTranslate(-140,0)
+    				curx,cury=curx-70,cury
+    				clickedbarrel2 = AttachmentButton("barrel","barrel2",true,{curx,cury},{"Long Barrel","Increased accuracy and damage but more vertical recoil."})
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(ammoattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedammo1 = AttachmentButton("ammotype","Buckshot",true,{curx,cury},{"Buckshot","8 Pellets. Medium damage."})
+    				UiTranslate(-100,0)
+    				curx,cury=curx-70,cury
+    				clickedammo2 = AttachmentButton("ammotype","Birdshot",true,{curx,cury},{"Birdshot","16 Pellets. Low damage."})
+    				UiTranslate(-100,0)
+    				curx,cury=curx-70,cury
+    				clickedammo1 = AttachmentButton("ammotype","Slugs",true,{curx,cury},{"Slugs","1 Pellet. Pakcs a big punch"})
+    				UiTranslate(-100,0)
+    				curx,cury=curx-70,cury
+    				UiTranslate(-70,0)
+    			UiPop()
+    		end
+    	UiPop()
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
@@ -1,75 +1,4 @@
-function init()
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	SetBool("savegame.mod.unlimitedammo", false)
-	spentcasingsoption = GetBool("savegame.mod.spentcasingsoption")
-	if unlimitedammo == 0 then unlimitedammo = 0.15 end
-	damage = GetInt("savegame.mod.damage")
-	if damage < 50 then
-		damage = 100
-		SetInt("savegame.mod.damage", 100)
-	end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Saiga-12")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Unlimited Ammo")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(0.5, 0.8, 1)
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
-		UiText("Damage: "..damage.."%")
-		UiTranslate(-50, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		damage = optionsSlider(damage, 50, 1000, 10)
-		SetInt("savegame.mod.damage", damage)
-	UiPop()
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(current, min, max, incri)
     UiPush()
         UiTranslate(0, -8)
@@ -89,4 +18,77 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    SetBool("savegame.mod.unlimitedammo", false, true)
+    spentcasingsoption = GetBool("savegame.mod.spentcasingsoption")
+    if unlimitedammo == 0 then unlimitedammo = 0.15 end
+    damage = GetInt("savegame.mod.damage")
+    if damage < 50 then
+    	damage = 100
+    	SetInt("savegame.mod.damage", 100, true)
+    end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Saiga-12")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Unlimited Ammo")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(0.5, 0.8, 1)
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
+    	UiText("Damage: "..damage.."%")
+    	UiTranslate(-50, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	damage = optionsSlider(damage, 50, 1000, 10)
+    	SetInt("savegame.mod.damage", damage, true)
+    UiPop()
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```
