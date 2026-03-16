# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,168 +1,4 @@
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
-casing = {
-	amount = 1,
-	shells = {},
-	defaultShell = {
-		active = false,
-		grenadeTimer = 0,
-		boomTimer = 0,
-		bounces = 0,
-		pos = Vec(0,0,0),
-		type = "casing",
-		crot = 0
-	}
-}
-
-function init()
-	RegisterTool("svu", "Dragunov SVU", "MOD/vox/svu.vox", 3)
-	SetBool("game.tool.svu.enabled", true)
-	SetFloat("game.tool.svu.ammo", 101)
-
-	damage = 0.15 * GetInt("savegame.mod.damage")/100
-	if damage == 0 then
-		damage = 0.15
-	end
-	gravity = Vec(0, -40, 0)
-	velocity = 5
-	maxMomentum = 12
-
-	inside = {}
-	for i = 1,50 do
-		inside[i] = {0,0,0,0}
-	end
-	hoverindex = 0
-
-	gunsound = LoadSound("MOD/snd/DragSVU.ogg")
-	gunsound308 = LoadSound("MOD/snd/ak308.ogg")
-	suppressedgunsound = LoadSound("MOD/snd/DraguSupressed.ogg")
-	grenadelaunchersound = LoadSound("MOD/snd/grenadelauncher.ogg")
-	toprail = GetString("savegame.mod.toprail")
-	muzzle = GetString("savegame.mod.muzzle")
-	stock = GetString("savegame.mod.stock")
-	grip = GetString("savegame.mod.grip")
-	barrel = GetString("savegame.mod.barrel")
-	side = GetString("savegame.mod.side")
-	guard = GetString("savegame.mod.guard")
-	magnifier = GetString("savegame.mod.magnifier")
-	magnified = false
-	magnifierFactor = 1
-	conversion = GetString("savegame.mod.conversion")
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
-	reloadTime = 2.4
-	shotDelay = 0.1
-	burstammo = 2
-	spreadTimer = 1.25
-	spreadFactor = 1.5
-	accuracyFactor = 1
-	mag = ""
-	magsize = 10
-	reloadFactor = 1.4
-	barrellength = 0
-	barrelFactorx = 0.8
-	barrelFactory = 1.5
-	barrelFactordamage = 1.25
-	ammo = magsize
-	grenadelauncherammo = 1
-	mags = 2
-	reloading = false
-	ironsight = false
-	ADSx = 0
-	ADSy = 0
-	ADSz = 0
-	ADSrot = 0
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
-	sideattachment = false
-	range = 0
-	grenadelauncher = false
-	unlimitedammo = GetBool("savegame.mod.unlimitedammo")
-	spentcasingsoption = GetBool("savegame.mod.spentcasingsoption")
-
-	for i=1, ammo do
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
-	recoilMax = 0
-	rnd1, rnd2, rnd3 = 0, 0, 0
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
-	selectfire = 0
-	selectfire0 = 1
-	selectfireTimer = 0
-	selectfireText = "Safe"
-
-	despawnTime = 20
-	casingGravity = Vec(0, -150, 0)
-	throwVel = 50
-end
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -234,26 +70,26 @@
 	ak47projectileHandler.shellNum = (ak47projectileHandler.shellNum%#ak47projectileHandler.shells) + 1
 
 	local barrelend = barrellength + muzzlelength
-	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.02), GetPlayerVelocity()), 0.3, 0.3)
+	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.02), GetPlayerVelocity(playerId)), 0.3, 0.3)
 	ParticleType("plain")
 	ParticleTile(5)
 	ParticleColor(1, 0.6, 0.4, 1, 0.3, 0.2)
 	ParticleRadius(0.1)
 	ParticleEmissive(5, 1)
-	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.04), GetPlayerVelocity()), 0.2, 0.3)
+	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.04), GetPlayerVelocity(playerId)), 0.2, 0.3)
 	if muzzle == "muzzle1" then
-		PlaySound(suppressedgunsound, GetPlayerTransform().pos, 1, false)
+		PlaySound(suppressedgunsound, GetPlayerTransform(playerId).pos, 1, false)
 	elseif muzzle == "muzzle2" then
 		if ammotype == "308" then
-			PlaySound(gunsound308, GetPlayerTransform().pos, 0.85, false)
+			PlaySound(gunsound308, GetPlayerTransform(playerId).pos, 0.85, false)
 		else
-			PlaySound(gunsound, GetPlayerTransform().pos, 0.9, false)
+			PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.9, false)
 		end
 	else
 		if ammotype == "308" then
-			PlaySound(gunsound308, GetPlayerTransform().pos, 0.7, false)
+			PlaySound(gunsound308, GetPlayerTransform(playerId).pos, 0.7, false)
 		else
-			PlaySound(gunsound, GetPlayerTransform().pos, 0.75, false)
+			PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.75, false)
 		end
 	end
 
@@ -310,7 +146,7 @@
 	ak47grenadeHandler.shellNum = (ak47grenadeHandler.shellNum%#ak47grenadeHandler.shells) + 1
 
 	SpawnParticle("fire", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(grenadelaunchersound, GetPlayerTransform().pos, 0.75, false)
+	PlaySound(grenadelaunchersound, GetPlayerTransform(playerId).pos, 0.75, false)
 
 	if not unlimitedammo then
 		grenadelauncherammo = grenadelauncherammo - 1
@@ -389,7 +225,7 @@
 
 			local factor = barrelFactordamage
 
-			if projectile.momentum > 0 then
+			if projectile.momentum ~= 0 then
 				MakeHole(hitPos, damage*factor, damage*0.85*factor, damage*0.7*factor)
 			end
 		end
@@ -432,7 +268,7 @@
 	local distance = VecLength(VecSub(point2, projectile.pos))
 	local hit, dist, normal = QueryRaycast(projectile.pos, dir, distance)
 	if hit then
-		PlaySound(casingsound, GetPlayerTransform().pos, 0.5/(projectile.bounces+1), false)
+		PlaySound(casingsound, GetPlayerTransform(playerId).pos, 0.5/(projectile.bounces+1), false)
 		if projectile.bounces == 6 then
 			projectile.gravity = Vec(0, 0, 0)
 			projectile.predictedBulletVelocity = Vec(0, 0, 0)
@@ -452,7 +288,7 @@
 	end
 	reloading = true
 	if not grenadelauncher then
-		PlaySound(reloadsound, GetPlayerTransform().pos, 0.5, false)
+		PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.5, false)
 	end
 	if grenadelauncher then
 		if grenadelauncherammo == 0 then
@@ -496,7 +332,7 @@
 		end
 	elseif bool and animationTimer > animationTime then
 		animationTimer = animationTimer*0.9 - dt/20
-	elseif not bool and fovTimer > 0 then
+	elseif not bool and fovTimer ~= 0 then
 		animationTimer = animationTimer*0.9 - dt/20
 		if animationTimer < 0 then
 			animationTimer = 0
@@ -584,17 +420,17 @@
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
@@ -646,6 +482,7 @@
 			laserFactor = 1
 		end
 end
+
 function Flashlight(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.175, -0.525, -2))
@@ -664,6 +501,7 @@
 			SetShapeEmissiveScale(side2, 0)
 		end
 end
+
 function Rangefinder(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.175, -0.525, -2))
@@ -734,7 +572,7 @@
 		elseif ADSz < -0.1 then
 			ADSz = ADSz + dt*math.abs((ADSz+0.1))
 		end
-		if ADSrot > 0 then 
+		if ADSrot ~= 0 then 
 			ADSrot = ADSrot - dt*math.abs((ADSrot-0))
 		elseif ADSrot < 0 then
 			ADSrot = ADSrot + dt*math.abs((ADSrot-0))
@@ -792,32 +630,32 @@
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
@@ -869,32 +707,32 @@
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
@@ -946,32 +784,32 @@
 	end
 
 	if not bool then
-		if INSx > 0 then 
+		if INSx ~= 0 then 
 			INSx = INSx - dt*math.abs((INSx-0))
 		elseif INSx < 0 then
 			INSx = INSx + dt*math.abs((INSx-0))
 		end
-		if INSy > 0 then 
+		if INSy ~= 0 then 
 			INSy = INSy - dt*math.abs((INSy-0))
 		elseif INSy < 0 then
 			INSy = INSy + dt*math.abs((INSy-0))
 		end
-		if INSz > 0 then 
+		if INSz ~= 0 then 
 			INSz = INSz - dt*math.abs((INSz-0))
 		elseif INSz < 0 then
 			INSz = INSz + dt*math.abs((INSz-0))
 		end
-		if INSrotx > 0 then 
+		if INSrotx ~= 0 then 
 			INSrotx = INSrotx - dt*math.abs((INSrotx-0))
 		elseif INSrotx < 0 then
 			INSrotx = INSrotx + dt*math.abs((INSrotx-0))
 		end
-		if INSroty > 0 then 
+		if INSroty ~= 0 then 
 			INSroty = INSroty - dt*math.abs((INSroty-0))
 		elseif INSroty < 0 then
 			INSroty = INSroty + dt*math.abs((INSroty-0))
 		end
-		if INSrotz > 0 then 
+		if INSrotz ~= 0 then 
 			INSrotz = INSrotz - dt*math.abs((INSrotz-0))
 		elseif INSrotz < 0 then
 			INSrotz = INSrotz + dt*math.abs((INSrotz-0))
@@ -984,1170 +822,6 @@
 	offset.pos = VecAdd(offset.pos, INSvec)
 
 	return offset
-end
-
-function tick(dt)
-	if GetString("game.player.tool") == "svu" and GetPlayerVehicle() == 0 then
-		conversion = GetString("savegame.mod.conversion")
-		if conversion == "" then
-			conversion = "Semi"
-		end
-
-		if InputDown("lmb") and not reloading and selectfire == 1 and conversion == "Full" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-			end
-		elseif InputPressed("lmb") and not reloading and selectfire == 1 and conversion == "Semi" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 then
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
-			burstammo = 2
-		end
-
-		if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and (toprail == "sight4" or toprail == "scope") and not (q or e) and not reloading then
-			ThermalScope()
-		end
-
-		if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and GetPlayerGrabShape() == 0 and not InputDown("shift") then
-			if InputPressed("rmb") then
-				PlaySound(interactsound1, GetPlayerTransform().pos, 1)
-			end
-			ironsight = true
-			inspectTimer = 0
-		end
-		if InputReleased("rmb") then
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
-		if InputPressed("x") and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") and not selectattachments then
-			meleeTimer = 0.8
-		end
-
-		if InputPressed("v") and not reloading and not selectattachments and not InputDown("shift") then
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
-		if InputPressed("g") and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire > 0 and not selectattachments then
-			if inspectTimer <= 0 then
-				inspectTimer = 6
-				ironsight = false
-			else
-				inspectTimer = 0
-			end
-		end
-
-		if InputPressed("z") and magnifier == "g33" then
-			magnified = not magnified
-			PlaySound(uiselect, GetPlayerTransform().pos, 1)
-		elseif magnifier == "" then
-			magnified = false
-		end
-		if magnified then
-			magnifierFactor = 3
-		else
-			magnifierFactor = 1
-		end
-
-		if selectfire == 1 then
-			selectfireText = conversion
-		else
-			selectfireText = "Safe"
-		end
-
-		if shootTimer <= 0 then
-			if recoilAngle > 0 then
-				recoilAngle = recoilAngle - 0.1*recoilAngle - 0.1
-			elseif recoilAngle < 0 then
-				recoilAngle = 0
-
-			end
-			if rnd1 > 0 then
-				rnd1 = rnd1 - 0.1*rnd1 - 0.1
-			elseif rnd1 <= 0 then
-				rnd1 = 0
-			end
-			if rnd2 > 0 then
-				rnd2 = rnd2 - 0.1*rnd2 - 0.1
-			elseif rnd2 <= 0 then
-				rnd2 = 0
-			end
-			if rnd3 > 0 then
-				rnd3 = rnd3 - 0.1*rnd3 - 0.1
-			elseif rnd3 <= 0 then
-				rnd3 = 0
-			end
-		end
-
-		if ironsight then
-			recoilFactor = 2*stockFactor
-		else
-			recoilFactor = 4*stockFactor
-		end
-
-		if ironsight then
-			recoilMax = 20*muzzleFactor*gripfactory*barrelFactory*stockFactor
-		else
-			recoilMax = 30*muzzleFactor*gripfactory*barrelFactory*stockFactor
-		end
-
-		if toprail == "scope" and not (q or e) then
-			spreadFactor = 1.25
-		elseif toprail == "holo" and not (q or e) then
-			spreadFactor = 1.75
-		elseif toprail == "sight3" and not (q or e) then
-			spreadFactor = 1.75
-		elseif toprail == "sight4" and not (q or e) then
-			spreadFactor = 1
-		else
-			spreadFactor = 2
-		end
-
-		toprail = GetString("savegame.mod.toprail")
-		muzzle = GetString("savegame.mod.muzzle")
-		stock = GetString("savegame.mod.stock")
-		grip = GetString("savegame.mod.grip")
-		barrel = GetString("savegame.mod.barrel")
-		side = GetString("savegame.mod.side")
-		guard = GetString("savegame.mod.guard")
-		magnifier = GetString("savegame.mod.magnifier")
-
-		for key, shell in ipairs(casing.shells) do
-			if shell.active then
-				Bouncing(shell)
-				local rot = QuatEuler(90, shell[6], 0)
-				local transform = Transform(shell.pos, rot)
-				DrawSprite(spentcasing.sprite, transform, 0.4, 0.4, 0.35, 0.35, 0.35, 1, true, false)
-			end
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
-			if grenadelauncher then
-				x = 0
-				y = 0.45
-				z = -0.2
-				rot = 0
-			elseif q then
-				x = 0.8
-				y = -0.05
-				z = -0.2
-				rot = 30
-			elseif e then
-				x = -0.4
-				y = 0.25
-				z = -0.2
-				rot = -15
-			else
-				if toprail == "holo" then
-					x = 0.275
-					y = 0.2375
-					z = -0.2
-					rot = 0
-				elseif toprail == "" then
-					x = 0.275
-					y = 0.265
-					z = -0.2
-					rot = 0
-				elseif toprail == "scope" then
-					x = 0.275
-					y = 0.3
-					z = -0.2
-					rot = 0
-				elseif toprail == "sight3" then
-					x = 0.275
-					y = 0.2875
-					z = -0.2
-					rot = 0
-				elseif toprail == "sight4" then
-					x = 0.275
-					y = 0.275
-					z = 0.2
-					rot = 0
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
-				elseif toprail == "sight3" then
-					adsFOV, adsTime = 10, 0.1
-				elseif toprail == "sight4" then
-					adsFOV, adsTime = 100, 0.3
-				end
-			elseif grenadelauncher then
-				adsFOV, adsTime = 10, 0.15
-			else
-				adsFOV, adsTime = 0, 0.15
-			end
-
-			offset = ADS(ironsight, adsFOV*magnifierFactor, adsTime, -x, y, z, rot)
-
-			if ironsight then
-				btrans = GetBodyTransform(b)
-				if toprail == "holo" then
-					holopoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.2375, -0.7), QuatEuler(0, 180, 0)))
-					reticle1 = LoadSprite("MOD/img/reticle1.png")
-					DrawSprite(reticle1, holopoint, 0.025, 0.025, 1, 0, 0, 1, true)
-				end
-				if toprail == "scope" then
-					scopepoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.302, -1.1), QuatEuler(0, 180, 0)))
-					reticle2 = LoadSprite("MOD/img/reticle2.png")
-					DrawSprite(reticle2, scopepoint, 0.075, 0.075, 1, 1, 1, 1, true)
-				end
-				if toprail == "sight4" then
-					scopepoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.275, -0.8), QuatEuler(0, 0, 0)))
-					reticle3 = LoadSprite("MOD/img/reticle4.png")
-					DrawSprite(reticle3, scopepoint, 0.105, 0.06, 1, 1, 1, 1, true)
-				end
-			end
-
-			local speed = VecLength(GetPlayerVelocity())
-			if speed > 1 then
-				swayy = math.sin(GetTime()*20*speed/7)
-				swayx = math.sin(GetTime()/reloadFactor*speed)
-				offset.rot = QuatRotateQuat(offset.rot, QuatEuler(swayy*speed/10, swayx*speed/12, 0))
-			end
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
-			if recoilTimer > 0 then
-				offset.pos = VecAdd(offset.pos, Vec(0, 0, recoilTimer*1.3))
-				offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer-0.02)*30, 0, 0))
-				
-				recoilTimer = recoilTimer - dt
-				boltoffset = Vec(-0.01, 0, recoilTimer*4)
-			end
-			offset.pos = VecAdd(offset.pos, Vec(0, (recoilAngle/-100), 0))
-			offset.rot = QuatRotateQuat(offset.rot, QuatEuler(recoilAngle + rnd1/2, rnd2/2, rnd3/2))
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 0.75, 0.25, (lightTimer/shotDelay)*lightFactor)
-				lightTimer = lightTimer - dt
-			end
-
-			if magoutTimer < 0 then
-				maginTimer = 0.6
-				magoutTimer = 0
-				if not grenadelauncher then
-					reloadsound2playing = false
-				end
-			end
-			if maginTimer < 0.1 and not reloadsound2playing and not grenadelauncher then
-					PlaySound(reloadsound2, GetPlayerTransform().pos, 0.5, false)
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
-						magoffset = Vec(0, 0, -(0.6-magoutTimer)*0.375)
-					elseif magoutTimer < 0.3 then
-						magoffset = Vec(0, -(0.3-magoutTimer)*6, -0.125)
-					
-					end
-				end
-				magoutTimer = magoutTimer - dt/reloadFactor
-			end
-			if maginTimer > 0 then
-				if grenadelauncher then
-					grenadeoffset = Vec(-0.025, 0.025, -maginTimer)
-				else
-					if maginTimer >= 0.1 then
-						magoffset = Vec(0, -(maginTimer-0.1)*4, -0.125)
-					elseif maginTimer < 0.1 then
-						magoffset = Vec(0, 0, -(maginTimer)*1.25)
-					end
-				end
-				maginTimer = maginTimer - dt/reloadFactor
-			end
-			if not grenadelauncher or (grenadelauncherammo == 0 and not reloading) then
-				grenadeoffset = Vec(0, 0, 1000)
-			end
-
-			local x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 0, 0, 0
-			if grenadelauncher then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 5, -10
-			elseif ironsight then
-				if q then
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, -0.4, 10, 10, -10
-					elseif maginTimer > 0 or reloadTimer > 0.8 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, -0.3, -0.3, 10, 0
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.25, -0.1, -0.2, 20, -20, -20
-					end
-				elseif e then
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, -0.05, -0.4, 10, -10, 10
-					elseif maginTimer > 0 or (reloadTimer > 0.8 and ammo > 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, -0.4, 5, -5, 0
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = -0.75, -0.45, -0.5, 10, 0, 50
-					end
-				else
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.3, -0.1, -0.5, 0, 0, -20
-					elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) or (reloadTimer > 1 and ammo == 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.4, -0.05, -0.5, 0, 0, -25
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = -0.3, -0.1, -0.6, -10, -5, 10
-					else
-						x1, y1, z1, rotx1, roty1, rotz1 = -0.05, -0.1, -0.5, 0, 0, 0
-					end
-				end
-			else
-				if magoutTimer > 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0, 0.05, -0.4, 10, -50, -10
-				elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0, -0.3, 5, 0, -20
-				elseif reloadTimer < 0.8 and ammo == 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = -0.75, -0.4, -0.5, 10, 0, 50
-				end
-			end
-
-			RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
-			offset.pos = VecAdd(offset.pos, RELoffset.pos)
-			offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
-
-			if reloadTimer < 0.5 and reloadTimer > 0.2 and reloading and ammo == 0 then
-				boltoffset = Vec(-0.01, 0, (0.5-reloadTimer)*1.25)
-			end
-
-			if selectattachmentsTimer > 0 and selectattachments then
-				local t1 = (0.5 - selectattachmentsTimer)/0.5
-				offset.pos = VecAdd(offset.pos, Vec(1*t1, 0, -0.8*t1*180/GetInt("options.gfx.fov")))
-				offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t1, 75*t1, -10*t1))
-			elseif selectattachmentsTimer > 0 and not selectattachments then
-				local t2 = selectattachmentsTimer/0.25
-				offset.pos = VecAdd(offset.pos, Vec(1*t2, 0, -0.8*t2*180/GetInt("options.gfx.fov")))
-				offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t2, 75*t2, -10*t2))
-			elseif selectattachments then
-				offset.pos = VecAdd(offset.pos, Vec(1, 0, -0.8*180/GetInt("options.gfx.fov")))
-				offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10, 75, -10))
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
-			INSoffset = INS(inspectTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
-			offset.pos = VecAdd(offset.pos, INSoffset.pos)
-			offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
-
-			local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0, 0.2, -0.2, -20, 60, 0
-			elseif ironsight and q and selectfireTimer > 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			elseif ironsight and selectfireTimer > 0  then
-				x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, -0.2, 0, 5, 30
-			elseif selectfireTimer > 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = -0.7, -0.5, -0.2, 0, 5, 50
-			else
-				x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			end
-
-			SELoffset = SEL(selectfireTimer > 0 or selectfire == 0 or InputDown("shift"), x3, y3, z3, rotx3, roty3, rotz3)
-			offset.pos = VecAdd(offset.pos, SELoffset.pos)
-			offset.rot = QuatRotateQuat(offset.rot, SELoffset.rot)
-
-			SetToolTransform(offset)
-			toolTrans = GetBodyTransform(b)
-			toolPos = TransformToParentPoint(toolTrans, Vec(0.275, -0.6, -2.6))
-
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				mag0 = shapes[2]
-				mag0_762 = shapes[31]
-				mag0_308 = shapes[38]
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
-				mag1_762 = shapes[43]
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
-				barrel3 = shapes[30]
-				side1 = shapes[26]
-				side2 = shapes[27]
-				side3 = shapes[28]
-				grenade = shapes[29]
-				guard0 = shapes[39]
-				guard0_2 = shapes[40]
-				guard1 = shapes[41]
-				guard1_2 = shapes[42]
-				g33 = shapes[32]
-				g33_2 = shapes[33]
-				reddot = shapes[35]
-				reddot2 = shapes[34]
-				scope2 = shapes[36]
-				scope2_2 = shapes[37]
-				magTrans = GetShapeLocalTransform(mag0)
-				boltTrans = GetShapeLocalTransform(bolt)
-				selectorTrans = GetShapeLocalTransform(selector)
-				suppressorTrans = GetShapeLocalTransform(suppressor)
-				scopeTrans = GetShapeLocalTransform(scope)
-				holoTrans = GetShapeLocalTransform(holo)
-				holoTrans2 = GetShapeLocalTransform(holo2)
-				reddotTrans = GetShapeLocalTransform(reddot)
-				scopeTrans2 = GetShapeLocalTransform(scope2)
-				g33Trans = GetShapeLocalTransform(g33)
-				railTrans = GetShapeLocalTransform(rail)
-				stock1Trans = GetShapeLocalTransform(stock1)
-				muzzlebreakTrans = GetShapeLocalTransform(muzzlebreak)
-				muzzlebreakTrans2 = GetShapeLocalTransform(muzzlebreak2)
-				gripTrans = GetShapeLocalTransform(grip1)
-				barrelTrans0 = GetShapeLocalTransform(barrel0)
-				barrelTrans1 = GetShapeLocalTransform(barrel1)
-				barrelTrans2 = GetShapeLocalTransform(barrel2)
-				barrelTrans3 = GetShapeLocalTransform(barrel3)
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
-			rdt = TransformCopy(reddotTrans)
-			rdt2 = TransformCopy(reddotTrans)
-
-			sct2 = TransformCopy(scopeTrans2)
-			sct2_2 = TransformCopy(scopeTrans2)
-
-			g33t = TransformCopy(g33Trans)
-			g33t2 = TransformCopy(g33Trans)
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
-			bt3 = TransformCopy(barrelTrans3)
-			bt3.pos = VecAdd(bt3.pos, barreloffset)
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
-			gdt0 = TransformCopy(guardTrans0)
-			gdt0.pos = VecAdd(gdt0.pos, guardoffset)
-			gdt0_2 = TransformCopy(guardTrans0)
-			gdt0_2.pos = VecAdd(gdt0.pos, guardoffset)
-			gdt1 = TransformCopy(guardTrans0)
-			gdt1.pos = VecAdd(gdt0.pos, guardoffset)
-			gdt1_2 = TransformCopy(guardTrans0)
-			gdt1_2.pos = VecAdd(gdt0.pos, guardoffset)
-
-			if not grenadelauncher then
-				if magoutTimer > 0 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler((0.6-magoutTimer)*22.5, 0, 0))
-				elseif maginTimer > 0.1 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(22.5*0.6, 0, 0))
-				elseif maginTimer > 0 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(maginTimer*60, 0, 0))
-				end
-			end
-
-			if selectfireTimer < 0.4 then
-				if selectfire == 1 then
-					st.rot = QuatEuler(-85, 0, 0)
-				elseif selectfire == 2 then
-					st.rot = QuatEuler(-92, 0, 0)
-				elseif selectfire == 3 then
-					st.rot = QuatEuler(-100, 0, 0)
-				else
-					st.rot = QuatEuler(-70, 0, 0)
-				end
-			elseif selectfireTimer > 0 then
-				if selectfire0 == 1 then
-					st.rot = QuatEuler(-85, 0, 0)
-				elseif selectfire0 == 2 then
-					st.rot = QuatEuler(-92, 0, 0)
-				elseif selectfire0 == 3 then
-					st.rot = QuatEuler(-100, 0, 0)
-				else
-					st.rot = QuatEuler(-70, 0, 0)
-				end
-			end
-
-			muzzlelength = 0
-			if muzzle == "muzzle1" then
-				spt.pos = VecAdd(spt.pos, Vec(0.125, -0.075, 0))
-				spt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 0.4
-				muzzlelength = 0.6
-			else
-				spt.pos = Vec(0, 0, 1000)
-				spt.rot = QuatEuler(0, 0, 0)
-				lightFactor = 2
-				muzzleFactor = 1
-			end
-			if muzzle == "muzzle2" then
-				mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, 0))
-				mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0, 0))
-				mbt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 3
-				muzzleFactor = 0.8
-				muzzlelength = 0.2
-			else
-				mbt.pos = Vec(0, 0, 1000)
-				mbt2.pos = Vec(0, 0, 1000)
-				mbt.rot = QuatEuler(0, 0, 0)
-				lightFactor = 2
-				muzzleFactor = 1
-			end
-			if toprail == "scope" then
-				sct.pos = Vec(0.2, -0.575, -0.525)
-			else
-				sct.pos = Vec(0, 0, 1000)
-			end
-			if toprail == "holo" then
-				ht.pos = Vec(0.175, -0.6, -0.575)
-				ht2.pos = Vec(0.225, -0.325, -0.575)
-			else
-				ht.pos = Vec(0, 0, 1000)
-				ht2.pos = Vec(0, 0, 1000)
-			end
-			if toprail == "sight3" then
-				rdt.pos = Vec(0.175, -0.6, -0.575)
-				rdt2.pos = Vec(0.2, -0.475, -0.625)
-			else
-				rdt.pos = Vec(0, 0, 1000)
-				rdt2.pos = Vec(0, 0, 1000)
-			end
-			if toprail == "sight4" then
-				sct2.pos = Vec(0.175, -0.575, -0.425)
-				sct2_2.pos = Vec(0.2, -0.35, -0.425)
-			else
-				sct2.pos = Vec(0, 0, 1000)
-				sct2_2.pos = Vec(0, 0, 1000)
-			end
-			if magnifier == "g33" then
-				g33t.pos = Vec(0.175, -0.475, -0.425)
-				if magnified then
-					g33t2.pos = Vec(0.2, -0.3375, -0.425)
-				else
-					g33t2.pos = Vec(0.35, -0.1875, -0.425)
-					g33t2.rot = QuatRotateQuat(g33t2.rot, QuatEuler(0, 90, 0))
-				end
-			else
-				g33t.pos = Vec(0, 0, 1000)
-				g33t2.pos = Vec(0, 0, 1000)
-			end
-
-			stt.pos = Vec(0, 0, 1000)
-			stt.rot = QuatEuler(-90, 0, 0)
-			stockFactor = 1
-
-			rt.pos = Vec(0.175, -0.925, 0.375)
-
-			magsize = 10
-			reloadFactor = 1.4
-			SetShapeLocalTransform(mag0_308, Transform(VecAdd(mt.pos, Vec(0, 0.1, 0)), mt.rot))
-			SetShapeLocalTransform(mag0, Transform(Vec(0, 0, 1000)))
-			SetShapeLocalTransform(mag0_762, Transform(Vec(0, 0, 1000)))
-			SetShapeLocalTransform(mag1, Transform(Vec(0, 0, 1000)))
-			SetShapeLocalTransform(mag1_762, Transform(Vec(0, 0, 1000)))
-			SetShapeLocalTransform(mag2, Transform(Vec(0, 0, 1000)))
-			SetShapeLocalTransform(mag3, Transform(Vec(0, 0, 1000)))
-
-			if grip == "grip1" then
-				gripfactorx = 0.9
-				gripfactory = 0.8
-				gt1.pos = Vec(0.25, -0.875, -1.45)
-				gt1_2.pos = Vec(0.225, -1.025, -1.375)
-			else
-				gt1.pos = Vec(0, 0, 1000)
-				gt1_2.pos = Vec(0, 0, 1000)
-			end
-			if grip == "grip2" then
-				gripfactorx = 0.7
-				gripfactory = 0.9
-				gt2.pos = Vec(0.25, -0.95, -1.2)
-			else
-				gt2.pos = Vec(0, 0, 1000)
-			end
-			if grip == "grip3" then
-				local querypos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -1.9))
-				local hit, dist = QueryRaycast(querypos, Vec(0, -2, 0), 5, 0.2)
-				local bipodded = (InputDown("ctrl") or dist < 0.4) and selectfire > 0
-				if bipodded then
-					gripfactorx = 0.3
-					gripfactory = 0.3
-					gt3_1.pos = Vec(0.4, -1.575, -1.75)
-					gt3_2.pos = Vec(0.05, -1.55, -1.75)
-					gt3_1.rot = QuatEuler(0, 0, 10)
-					gt3_2.rot = QuatEuler(0, 0, -10)
-				else
-					gripfactorx = 1
-					gripfactory = 1
-					gt3_1.pos = Vec(0.3, -0.875, -1)
-					gt3_2.pos = Vec(0.15, -0.875, -1)
-					gt3_1.rot = QuatEuler(-90, 0, 0)
-					gt3_2.rot = QuatEuler(-90, 0, 0)
-				end
-				gt3.pos = Vec(0.25, -0.875, -1)
-				
-			else
-				gt3.pos = Vec(0, 0, 1000)
-				gt3_1.pos = Vec(0, 0, 1000)
-				gt3_2.pos = Vec(0, 0, 1000)
-			end
-			if grip == "grenade_launcher" then
-				gripfactorx = 1.1
-				gripfactory = 1.1
-				glt.pos = Vec(0.2, -0.9, -1.4)
-			else
-				glt.pos = Vec(0, 0, 1000)
-			end
-			if grip == "" then
-				gripfactorx = 1
-				gripfactory = 1
-			end
-
-			barrelFactorx = 0.8
-			barrelFactory = 1.2
-			barrelFactordamage = 1
-			accuracyFactor = 0.2
-			barrellength = 0.4
-			bt1.pos = bt1.pos
-			bt0.pos = Vec(0, 0, 1000)
-			bt2.pos = Vec(0, 0, 1000)
-			bt3.pos = Vec(0, 0, 1000)
-
-			if side == "side1" then
-				sdt1.pos = sdt1.pos
-			else
-				sdt1.pos = Vec(0, 0, 1000)
-			end
-			if side == "side2" then
-				sdt2.pos = sdt2.pos
-			else
-				sdt2.pos = Vec(0, 0, 1000)
-			end
-			if side == "side3" then
-				sdt3.pos = sdt3.pos
-			else
-				sdt3.pos = Vec(0, 0, 1000)
-			end
-
-			if mag == "mag2" or mag == "mag3" then
-				SetString("savegame.mod.stock", "")
-			end
-			if toprail ~= "holo" then
-				SetString("savegame.mod.magnifier", "")
-			end
-			if guard == "guard2" and grip == "grenade_launcher" or ammotype == "308" and grip == "grenade_launcher"  then
-				SetString("savegame.mod.grip", "")
-				grip = ""
-			end
-
-			gdt0.pos = Vec(0, 0, 1000)
-			gdt0_2.pos = Vec(0, 0, 1000)
-			gdt1.pos = Vec(0, 0, 1000)
-			gdt1_2.pos = Vec(0, 0, 1000)
-			guardlength = 0
-
-			SetShapeLocalTransform(bolt, bt)
-			SetShapeLocalTransform(selector, st)
-			SetShapeLocalTransform(suppressor, spt)
-			SetShapeLocalTransform(scope, sct)
-			SetShapeLocalTransform(holo, ht)
-			SetShapeLocalTransform(holo2, ht2)
-			SetShapeLocalTransform(reddot, rdt)
-			SetShapeLocalTransform(reddot2, rdt2)
-			SetShapeLocalTransform(scope2, sct2)
-			SetShapeLocalTransform(scope2_2, sct2_2)
-			SetShapeLocalTransform(g33, g33t)
-			SetShapeLocalTransform(g33_2, g33t2)
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
-			SetShapeLocalTransform(barrel3, bt3)
-			SetShapeLocalTransform(side1, sdt1)
-			SetShapeLocalTransform(side2, sdt2)
-			SetShapeLocalTransform(side3, sdt3)
-			SetShapeLocalTransform(grenade, grt)
-			SetShapeLocalTransform(guard0, gdt0)
-			SetShapeLocalTransform(guard0_2, gdt0_2)
-			SetShapeLocalTransform(guard1, gdt1)
-			SetShapeLocalTransform(guard1_2, gdt1_2)
-		end
-
-		if selectattachments then
-			clickedmag = clickedmag1 or clickedmag2 or clickedmag3
-			if clickedmag  and selectattachments and not InputPressed("t") then
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
-				if reloadTimer < 0.5 and not cocksoundplaying and ammo == 0 then
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
-		sightattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.15, -1))
-		muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.35, -2.5))
-		stockattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.4, -0.6))
-		sideattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.45, -1.65))
-		magattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.65, -1))
-		gripattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.85, -1.4))
-		barrelattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.65, -1.6))
-		guardattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.5, -1.4))
-		ammoattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.8, -0.75))
-		magnifierattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.25, -0.7))
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
-	if GetString("game.player.tool") == "svu" and GetPlayerVehicle() == 0 then
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
-					UiText(ammo.."/"..magsize*math.max(0, mags-1).." - "..selectfireText)
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
-	if GetString("game.player.tool") == "svu" and grenadelauncher and not selectattachments then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle")
-			UiImage("ui/hud/crosshair-launcher.png")
-		UiPop()
-	end
-	if GetString("game.player.tool") == "svu" and sideattachment and side == "side3" then
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
-					UiAlign("center middle")
-					clickedscope = AttachmentButton("toprail","sight3",true,{curx,cury},{"Scope","1x magnification sight for close range combat."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedholo = AttachmentButton("toprail","sight4",true,{curx,cury},{"Precision Scope","8x magnification sight for long range combat."})
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
-						--clickedstockremoved = AttachmentButton("stock","removed",true,{curx,cury},{"Stock","Foldable for badasses only."})
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
-					clickedgrip3 = AttachmentButton("grip","grip3",true,{curx,cury},{"Bipod","Increased accuracy while crouching or resting the gun on a ledge."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedgrip4 = AttachmentButton("grip","grenade_launcher",true,{curx,cury},{"GP-25","Grenade launcher for increased collateral damage."})
-					UiTranslate(-70,0)
-				UiPop()
-			end
-		UiPop()
-	end
-	--if ironsight and not (q or e) and toprail == "holo" and fovTimer > 0.1 then
-		--UiPush()
-			--local gt = GetBodyTransform(GetToolBody())
-			--local gunpos = TransformToParentPoint(gt, Vec(0.175, -0.525, -1.9))
-			--local fwdpos = TransformToParentVec(gt, Vec(0, 0, -1))
-			--local hit, dist = QueryRaycast(gunpos, fwdpos, 500)
-			--local hitpoint = VecAdd(gunpos, VecScale(fwdpos, dist))
-			--local imgx, imgy, dist = UiWorldToPixel(hitpoint)
-			--UiTranslate(imgx, imgy)
-			--UiAlign("center middle")
-			--UiImage("MOD/icon/reticle1.png")
-		--UiPop()
-	--end
 end
 
 function ThermalScope()
@@ -2193,4 +867,1290 @@
 		DrawBodyHighlight(Torso, 1)
 		DrawBodyOutline(Torso, 0, 1, 1, 0)
 	end
-end+end
+
+function server.init()
+    RegisterTool("svu", "Dragunov SVU", "MOD/vox/svu.vox", 3)
+    SetBool("game.tool.svu.enabled", true, true)
+    SetFloat("game.tool.svu.ammo", 101, true)
+    damage = 0.15 * GetInt("savegame.mod.damage")/100
+    if damage == 0 then
+    	damage = 0.15
+    end
+    gravity = Vec(0, -40, 0)
+    velocity = 5
+    maxMomentum = 12
+    inside = {}
+    for i = 1,50 do
+    	inside[i] = {0,0,0,0}
+    end
+    hoverindex = 0
+    toprail = GetString("savegame.mod.toprail")
+    muzzle = GetString("savegame.mod.muzzle")
+    stock = GetString("savegame.mod.stock")
+    grip = GetString("savegame.mod.grip")
+    barrel = GetString("savegame.mod.barrel")
+    side = GetString("savegame.mod.side")
+    guard = GetString("savegame.mod.guard")
+    magnifier = GetString("savegame.mod.magnifier")
+    magnified = false
+    magnifierFactor = 1
+    conversion = GetString("savegame.mod.conversion")
+    reloadTime = 2.4
+    shotDelay = 0.1
+    burstammo = 2
+    spreadTimer = 1.25
+    spreadFactor = 1.5
+    accuracyFactor = 1
+    mag = ""
+    magsize = 10
+    reloadFactor = 1.4
+    barrellength = 0
+    barrelFactorx = 0.8
+    barrelFactory = 1.5
+    barrelFactordamage = 1.25
+    ammo = magsize
+    grenadelauncherammo = 1
+    mags = 2
+    reloading = false
+    ironsight = false
+    ADSx = 0
+    ADSy = 0
+    ADSz = 0
+    ADSrot = 0
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
+    sideattachment = false
+    range = 0
+    grenadelauncher = false
+    unlimitedammo = GetBool("savegame.mod.unlimitedammo")
+    spentcasingsoption = GetBool("savegame.mod.spentcasingsoption")
+    for i=1, ammo do
+    	ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    end
+    for i=1, 10 do
+    	ak47grenadeHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    end
+    shootTimer = 0
+    reloadTimer = 0
+    recoilTimer = 0
+    recoilAngle = 0
+    recoilFactor = 0
+    stockFactor = 0
+    muzzleFactor = 0
+    muzzlelength = 0
+    gripfactorx = 0
+    gripfactory = 0
+    recoilMax = 0
+    rnd1, rnd2, rnd3 = 0, 0, 0
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
+    selectfire = 0
+    selectfire0 = 1
+    selectfireTimer = 0
+    selectfireText = "Safe"
+    despawnTime = 20
+    casingGravity = Vec(0, -150, 0)
+    throwVel = 50
+end
+
+function client.init()
+    gunsound = LoadSound("MOD/snd/DragSVU.ogg")
+    gunsound308 = LoadSound("MOD/snd/ak308.ogg")
+    suppressedgunsound = LoadSound("MOD/snd/DraguSupressed.ogg")
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
+    if GetString("game.player.tool") == "svu" and GetPlayerVehicle(playerId) == 0 then
+    	conversion = GetString("savegame.mod.conversion")
+    	if conversion == "" then
+    		conversion = "Semi"
+    	end
+
+    	if InputDown("lmb") and not reloading and selectfire == 1 and conversion == "Full" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    		end
+    	elseif InputPressed("lmb") and not reloading and selectfire == 1 and conversion == "Semi" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 then
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
+    		burstammo = 2
+    	end
+
+    	if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and (toprail == "sight4" or toprail == "scope") and not (q or e) and not reloading then
+    		ThermalScope()
+    	end
+
+    	if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") then
+    		if InputPressed("rmb") then
+    			PlaySound(interactsound1, GetPlayerTransform(playerId).pos, 1)
+    		end
+    		ironsight = true
+    		inspectTimer = 0
+    	end
+    	if InputReleased("rmb") then
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
+    	if InputPressed("x") and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") and not selectattachments then
+    		meleeTimer = 0.8
+    	end
+
+    	if InputPressed("v") and not reloading and not selectattachments and not InputDown("shift") then
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
+    	if InputPressed("g") and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire > 0 and not selectattachments then
+    		if inspectTimer <= 0 then
+    			inspectTimer = 6
+    			ironsight = false
+    		else
+    			inspectTimer = 0
+    		end
+    	end
+
+    	if InputPressed("z") and magnifier == "g33" then
+    		magnified = not magnified
+    		PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
+    	elseif magnifier == "" then
+    		magnified = false
+    	end
+    	if magnified then
+    		magnifierFactor = 3
+    	else
+    		magnifierFactor = 1
+    	end
+
+    	if selectfire == 1 then
+    		selectfireText = conversion
+    	else
+    		selectfireText = "Safe"
+    	end
+
+    	if shootTimer <= 0 then
+    		if recoilAngle ~= 0 then
+    			recoilAngle = recoilAngle - 0.1*recoilAngle - 0.1
+    		elseif recoilAngle < 0 then
+    			recoilAngle = 0
+
+    		end
+    		if rnd1 ~= 0 then
+    			rnd1 = rnd1 - 0.1*rnd1 - 0.1
+    		elseif rnd1 <= 0 then
+    			rnd1 = 0
+    		end
+    		if rnd2 ~= 0 then
+    			rnd2 = rnd2 - 0.1*rnd2 - 0.1
+    		elseif rnd2 <= 0 then
+    			rnd2 = 0
+    		end
+    		if rnd3 ~= 0 then
+    			rnd3 = rnd3 - 0.1*rnd3 - 0.1
+    		elseif rnd3 <= 0 then
+    			rnd3 = 0
+    		end
+    	end
+
+    	if ironsight then
+    		recoilFactor = 2*stockFactor
+    	else
+    		recoilFactor = 4*stockFactor
+    	end
+
+    	if ironsight then
+    		recoilMax = 20*muzzleFactor*gripfactory*barrelFactory*stockFactor
+    	else
+    		recoilMax = 30*muzzleFactor*gripfactory*barrelFactory*stockFactor
+    	end
+
+    	if toprail == "scope" and not (q or e) then
+    		spreadFactor = 1.25
+    	elseif toprail == "holo" and not (q or e) then
+    		spreadFactor = 1.75
+    	elseif toprail == "sight3" and not (q or e) then
+    		spreadFactor = 1.75
+    	elseif toprail == "sight4" and not (q or e) then
+    		spreadFactor = 1
+    	else
+    		spreadFactor = 2
+    	end
+
+    	toprail = GetString("savegame.mod.toprail")
+    	muzzle = GetString("savegame.mod.muzzle")
+    	stock = GetString("savegame.mod.stock")
+    	grip = GetString("savegame.mod.grip")
+    	barrel = GetString("savegame.mod.barrel")
+    	side = GetString("savegame.mod.side")
+    	guard = GetString("savegame.mod.guard")
+    	magnifier = GetString("savegame.mod.magnifier")
+
+    	for key, shell in ipairs(casing.shells) do
+    		if shell.active then
+    			Bouncing(shell)
+    			local rot = QuatEuler(90, shell[6], 0)
+    			local transform = Transform(shell.pos, rot)
+    			DrawSprite(spentcasing.sprite, transform, 0.4, 0.4, 0.35, 0.35, 0.35, 1, true, false)
+    		end
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
+    		if grenadelauncher then
+    			x = 0
+    			y = 0.45
+    			z = -0.2
+    			rot = 0
+    		elseif q then
+    			x = 0.8
+    			y = -0.05
+    			z = -0.2
+    			rot = 30
+    		elseif e then
+    			x = -0.4
+    			y = 0.25
+    			z = -0.2
+    			rot = -15
+    		else
+    			if toprail == "holo" then
+    				x = 0.275
+    				y = 0.2375
+    				z = -0.2
+    				rot = 0
+    			elseif toprail == "" then
+    				x = 0.275
+    				y = 0.265
+    				z = -0.2
+    				rot = 0
+    			elseif toprail == "scope" then
+    				x = 0.275
+    				y = 0.3
+    				z = -0.2
+    				rot = 0
+    			elseif toprail == "sight3" then
+    				x = 0.275
+    				y = 0.2875
+    				z = -0.2
+    				rot = 0
+    			elseif toprail == "sight4" then
+    				x = 0.275
+    				y = 0.275
+    				z = 0.2
+    				rot = 0
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
+    			elseif toprail == "sight3" then
+    				adsFOV, adsTime = 10, 0.1
+    			elseif toprail == "sight4" then
+    				adsFOV, adsTime = 100, 0.3
+    			end
+    		elseif grenadelauncher then
+    			adsFOV, adsTime = 10, 0.15
+    		else
+    			adsFOV, adsTime = 0, 0.15
+    		end
+
+    		offset = ADS(ironsight, adsFOV*magnifierFactor, adsTime, -x, y, z, rot)
+
+    		if ironsight then
+    			btrans = GetBodyTransform(b)
+    			if toprail == "holo" then
+    				holopoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.2375, -0.7), QuatEuler(0, 180, 0)))
+    				reticle1 = LoadSprite("MOD/img/reticle1.png")
+    				DrawSprite(reticle1, holopoint, 0.025, 0.025, 1, 0, 0, 1, true)
+    			end
+    			if toprail == "scope" then
+    				scopepoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.302, -1.1), QuatEuler(0, 180, 0)))
+    				reticle2 = LoadSprite("MOD/img/reticle2.png")
+    				DrawSprite(reticle2, scopepoint, 0.075, 0.075, 1, 1, 1, 1, true)
+    			end
+    			if toprail == "sight4" then
+    				scopepoint = TransformToParentTransform(btrans, Transform(Vec(0.275, -0.275, -0.8), QuatEuler(0, 0, 0)))
+    				reticle3 = LoadSprite("MOD/img/reticle4.png")
+    				DrawSprite(reticle3, scopepoint, 0.105, 0.06, 1, 1, 1, 1, true)
+    			end
+    		end
+
+    		local speed = VecLength(GetPlayerVelocity(playerId))
+    		if speed > 1 then
+    			swayy = math.sin(GetTime()*20*speed/7)
+    			swayx = math.sin(GetTime()/reloadFactor*speed)
+    			offset.rot = QuatRotateQuat(offset.rot, QuatEuler(swayy*speed/10, swayx*speed/12, 0))
+    		end
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
+    		if recoilTimer ~= 0 then
+    			offset.pos = VecAdd(offset.pos, Vec(0, 0, recoilTimer*1.3))
+    			offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer-0.02)*30, 0, 0))
+
+    			recoilTimer = recoilTimer - dt
+    			boltoffset = Vec(-0.01, 0, recoilTimer*4)
+    		end
+    		offset.pos = VecAdd(offset.pos, Vec(0, (recoilAngle/-100), 0))
+    		offset.rot = QuatRotateQuat(offset.rot, QuatEuler(recoilAngle + rnd1/2, rnd2/2, rnd3/2))
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 0.75, 0.25, (lightTimer/shotDelay)*lightFactor)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if magoutTimer < 0 then
+    			maginTimer = 0.6
+    			magoutTimer = 0
+    			if not grenadelauncher then
+    				reloadsound2playing = false
+    			end
+    		end
+    		if maginTimer < 0.1 and not reloadsound2playing and not grenadelauncher then
+    				PlaySound(reloadsound2, GetPlayerTransform(playerId).pos, 0.5, false)
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
+    					magoffset = Vec(0, 0, -(0.6-magoutTimer)*0.375)
+    				elseif magoutTimer < 0.3 then
+    					magoffset = Vec(0, -(0.3-magoutTimer)*6, -0.125)
+
+    				end
+    			end
+    			magoutTimer = magoutTimer - dt/reloadFactor
+    		end
+    		if maginTimer ~= 0 then
+    			if grenadelauncher then
+    				grenadeoffset = Vec(-0.025, 0.025, -maginTimer)
+    			else
+    				if maginTimer >= 0.1 then
+    					magoffset = Vec(0, -(maginTimer-0.1)*4, -0.125)
+    				elseif maginTimer < 0.1 then
+    					magoffset = Vec(0, 0, -(maginTimer)*1.25)
+    				end
+    			end
+    			maginTimer = maginTimer - dt/reloadFactor
+    		end
+    		if not grenadelauncher or (grenadelauncherammo == 0 and not reloading) then
+    			grenadeoffset = Vec(0, 0, 1000)
+    		end
+
+    		local x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 0, 0, 0
+    		if grenadelauncher then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.2, 0, 10, 5, -10
+    		elseif ironsight then
+    			if q then
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, -0.4, 10, 10, -10
+    				elseif maginTimer > 0 or reloadTimer > 0.8 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, -0.3, -0.3, 10, 0
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.25, -0.1, -0.2, 20, -20, -20
+    				end
+    			elseif e then
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, -0.05, -0.4, 10, -10, 10
+    				elseif maginTimer > 0 or (reloadTimer > 0.8 and ammo > 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, -0.4, 5, -5, 0
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = -0.75, -0.45, -0.5, 10, 0, 50
+    				end
+    			else
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.3, -0.1, -0.5, 0, 0, -20
+    				elseif maginTimer > 0 or (reloadTimer > 0.4 and ammo > 0) or (reloadTimer > 1 and ammo == 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.4, -0.05, -0.5, 0, 0, -25
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = -0.3, -0.1, -0.6, -10, -5, 10
+    				else
+    					x1, y1, z1, rotx1, roty1, rotz1 = -0.05, -0.1, -0.5, 0, 0, 0
+    				end
+    			end
+    		else
+    			if magoutTimer ~= 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0, 0.05, -0.4, 10, -50, -10
+    			elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0, -0.3, 5, 0, -20
+    			elseif reloadTimer < 0.8 and ammo == 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = -0.75, -0.4, -0.5, 10, 0, 50
+    			end
+    		end
+
+    		RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
+    		offset.pos = VecAdd(offset.pos, RELoffset.pos)
+    		offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
+
+    		if reloadTimer < 0.5 and reloadTimer > 0.2 and reloading and ammo == 0 then
+    			boltoffset = Vec(-0.01, 0, (0.5-reloadTimer)*1.25)
+    		end
+
+    		if selectattachmentsTimer > 0 and selectattachments then
+    			local t1 = (0.5 - selectattachmentsTimer)/0.5
+    			offset.pos = VecAdd(offset.pos, Vec(1*t1, 0, -0.8*t1*180/GetInt("options.gfx.fov")))
+    			offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t1, 75*t1, -10*t1))
+    		elseif selectattachmentsTimer > 0 and not selectattachments then
+    			local t2 = selectattachmentsTimer/0.25
+    			offset.pos = VecAdd(offset.pos, Vec(1*t2, 0, -0.8*t2*180/GetInt("options.gfx.fov")))
+    			offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t2, 75*t2, -10*t2))
+    		elseif selectattachments then
+    			offset.pos = VecAdd(offset.pos, Vec(1, 0, -0.8*180/GetInt("options.gfx.fov")))
+    			offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10, 75, -10))
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
+    		INSoffset = INS(inspectTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
+    		offset.pos = VecAdd(offset.pos, INSoffset.pos)
+    		offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
+
+    		local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0, 0.2, -0.2, -20, 60, 0
+    		elseif ironsight and q and selectfireTimer ~= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		elseif ironsight and selectfireTimer ~= 0  then
+    			x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, -0.2, 0, 5, 30
+    		elseif selectfireTimer ~= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = -0.7, -0.5, -0.2, 0, 5, 50
+    		else
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		end
+
+    		SELoffset = SEL(selectfireTimer > 0 or selectfire == 0 or InputDown("shift"), x3, y3, z3, rotx3, roty3, rotz3)
+    		offset.pos = VecAdd(offset.pos, SELoffset.pos)
+    		offset.rot = QuatRotateQuat(offset.rot, SELoffset.rot)
+
+    		SetToolTransform(offset)
+    		toolTrans = GetBodyTransform(b)
+    		toolPos = TransformToParentPoint(toolTrans, Vec(0.275, -0.6, -2.6))
+
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			mag0 = shapes[2]
+    			mag0_762 = shapes[31]
+    			mag0_308 = shapes[38]
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
+    			mag1_762 = shapes[43]
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
+    			barrel3 = shapes[30]
+    			side1 = shapes[26]
+    			side2 = shapes[27]
+    			side3 = shapes[28]
+    			grenade = shapes[29]
+    			guard0 = shapes[39]
+    			guard0_2 = shapes[40]
+    			guard1 = shapes[41]
+    			guard1_2 = shapes[42]
+    			g33 = shapes[32]
+    			g33_2 = shapes[33]
+    			reddot = shapes[35]
+    			reddot2 = shapes[34]
+    			scope2 = shapes[36]
+    			scope2_2 = shapes[37]
+    			magTrans = GetShapeLocalTransform(mag0)
+    			boltTrans = GetShapeLocalTransform(bolt)
+    			selectorTrans = GetShapeLocalTransform(selector)
+    			suppressorTrans = GetShapeLocalTransform(suppressor)
+    			scopeTrans = GetShapeLocalTransform(scope)
+    			holoTrans = GetShapeLocalTransform(holo)
+    			holoTrans2 = GetShapeLocalTransform(holo2)
+    			reddotTrans = GetShapeLocalTransform(reddot)
+    			scopeTrans2 = GetShapeLocalTransform(scope2)
+    			g33Trans = GetShapeLocalTransform(g33)
+    			railTrans = GetShapeLocalTransform(rail)
+    			stock1Trans = GetShapeLocalTransform(stock1)
+    			muzzlebreakTrans = GetShapeLocalTransform(muzzlebreak)
+    			muzzlebreakTrans2 = GetShapeLocalTransform(muzzlebreak2)
+    			gripTrans = GetShapeLocalTransform(grip1)
+    			barrelTrans0 = GetShapeLocalTransform(barrel0)
+    			barrelTrans1 = GetShapeLocalTransform(barrel1)
+    			barrelTrans2 = GetShapeLocalTransform(barrel2)
+    			barrelTrans3 = GetShapeLocalTransform(barrel3)
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
+    		rdt = TransformCopy(reddotTrans)
+    		rdt2 = TransformCopy(reddotTrans)
+
+    		sct2 = TransformCopy(scopeTrans2)
+    		sct2_2 = TransformCopy(scopeTrans2)
+
+    		g33t = TransformCopy(g33Trans)
+    		g33t2 = TransformCopy(g33Trans)
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
+    		bt3 = TransformCopy(barrelTrans3)
+    		bt3.pos = VecAdd(bt3.pos, barreloffset)
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
+    		gdt0 = TransformCopy(guardTrans0)
+    		gdt0.pos = VecAdd(gdt0.pos, guardoffset)
+    		gdt0_2 = TransformCopy(guardTrans0)
+    		gdt0_2.pos = VecAdd(gdt0.pos, guardoffset)
+    		gdt1 = TransformCopy(guardTrans0)
+    		gdt1.pos = VecAdd(gdt0.pos, guardoffset)
+    		gdt1_2 = TransformCopy(guardTrans0)
+    		gdt1_2.pos = VecAdd(gdt0.pos, guardoffset)
+
+    		if not grenadelauncher then
+    			if magoutTimer ~= 0 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler((0.6-magoutTimer)*22.5, 0, 0))
+    			elseif maginTimer > 0.1 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(22.5*0.6, 0, 0))
+    			elseif maginTimer ~= 0 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(maginTimer*60, 0, 0))
+    			end
+    		end
+
+    		if selectfireTimer < 0.4 then
+    			if selectfire == 1 then
+    				st.rot = QuatEuler(-85, 0, 0)
+    			elseif selectfire == 2 then
+    				st.rot = QuatEuler(-92, 0, 0)
+    			elseif selectfire == 3 then
+    				st.rot = QuatEuler(-100, 0, 0)
+    			else
+    				st.rot = QuatEuler(-70, 0, 0)
+    			end
+    		elseif selectfireTimer ~= 0 then
+    			if selectfire0 == 1 then
+    				st.rot = QuatEuler(-85, 0, 0)
+    			elseif selectfire0 == 2 then
+    				st.rot = QuatEuler(-92, 0, 0)
+    			elseif selectfire0 == 3 then
+    				st.rot = QuatEuler(-100, 0, 0)
+    			else
+    				st.rot = QuatEuler(-70, 0, 0)
+    			end
+    		end
+
+    		muzzlelength = 0
+    		if muzzle == "muzzle1" then
+    			spt.pos = VecAdd(spt.pos, Vec(0.125, -0.075, 0))
+    			spt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 0.4
+    			muzzlelength = 0.6
+    		else
+    			spt.pos = Vec(0, 0, 1000)
+    			spt.rot = QuatEuler(0, 0, 0)
+    			lightFactor = 2
+    			muzzleFactor = 1
+    		end
+    		if muzzle == "muzzle2" then
+    			mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, 0))
+    			mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0, 0))
+    			mbt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 3
+    			muzzleFactor = 0.8
+    			muzzlelength = 0.2
+    		else
+    			mbt.pos = Vec(0, 0, 1000)
+    			mbt2.pos = Vec(0, 0, 1000)
+    			mbt.rot = QuatEuler(0, 0, 0)
+    			lightFactor = 2
+    			muzzleFactor = 1
+    		end
+    		if toprail == "scope" then
+    			sct.pos = Vec(0.2, -0.575, -0.525)
+    		else
+    			sct.pos = Vec(0, 0, 1000)
+    		end
+    		if toprail == "holo" then
+    			ht.pos = Vec(0.175, -0.6, -0.575)
+    			ht2.pos = Vec(0.225, -0.325, -0.575)
+    		else
+    			ht.pos = Vec(0, 0, 1000)
+    			ht2.pos = Vec(0, 0, 1000)
+    		end
+    		if toprail == "sight3" then
+    			rdt.pos = Vec(0.175, -0.6, -0.575)
+    			rdt2.pos = Vec(0.2, -0.475, -0.625)
+    		else
+    			rdt.pos = Vec(0, 0, 1000)
+    			rdt2.pos = Vec(0, 0, 1000)
+    		end
+    		if toprail == "sight4" then
+    			sct2.pos = Vec(0.175, -0.575, -0.425)
+    			sct2_2.pos = Vec(0.2, -0.35, -0.425)
+    		else
+    			sct2.pos = Vec(0, 0, 1000)
+    			sct2_2.pos = Vec(0, 0, 1000)
+    		end
+    		if magnifier == "g33" then
+    			g33t.pos = Vec(0.175, -0.475, -0.425)
+    			if magnified then
+    				g33t2.pos = Vec(0.2, -0.3375, -0.425)
+    			else
+    				g33t2.pos = Vec(0.35, -0.1875, -0.425)
+    				g33t2.rot = QuatRotateQuat(g33t2.rot, QuatEuler(0, 90, 0))
+    			end
+    		else
+    			g33t.pos = Vec(0, 0, 1000)
+    			g33t2.pos = Vec(0, 0, 1000)
+    		end
+
+    		stt.pos = Vec(0, 0, 1000)
+    		stt.rot = QuatEuler(-90, 0, 0)
+    		stockFactor = 1
+
+    		rt.pos = Vec(0.175, -0.925, 0.375)
+
+    		magsize = 10
+    		reloadFactor = 1.4
+    		SetShapeLocalTransform(mag0_308, Transform(VecAdd(mt.pos, Vec(0, 0.1, 0)), mt.rot))
+    		SetShapeLocalTransform(mag0, Transform(Vec(0, 0, 1000)))
+    		SetShapeLocalTransform(mag0_762, Transform(Vec(0, 0, 1000)))
+    		SetShapeLocalTransform(mag1, Transform(Vec(0, 0, 1000)))
+    		SetShapeLocalTransform(mag1_762, Transform(Vec(0, 0, 1000)))
+    		SetShapeLocalTransform(mag2, Transform(Vec(0, 0, 1000)))
+    		SetShapeLocalTransform(mag3, Transform(Vec(0, 0, 1000)))
+
+    		if grip == "grip1" then
+    			gripfactorx = 0.9
+    			gripfactory = 0.8
+    			gt1.pos = Vec(0.25, -0.875, -1.45)
+    			gt1_2.pos = Vec(0.225, -1.025, -1.375)
+    		else
+    			gt1.pos = Vec(0, 0, 1000)
+    			gt1_2.pos = Vec(0, 0, 1000)
+    		end
+    		if grip == "grip2" then
+    			gripfactorx = 0.7
+    			gripfactory = 0.9
+    			gt2.pos = Vec(0.25, -0.95, -1.2)
+    		else
+    			gt2.pos = Vec(0, 0, 1000)
+    		end
+    		if grip == "grip3" then
+    			local querypos = TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -1.9))
+    			local hit, dist = QueryRaycast(querypos, Vec(0, -2, 0), 5, 0.2)
+    			local bipodded = (InputDown("ctrl") or dist < 0.4) and selectfire > 0
+    			if bipodded then
+    				gripfactorx = 0.3
+    				gripfactory = 0.3
+    				gt3_1.pos = Vec(0.4, -1.575, -1.75)
+    				gt3_2.pos = Vec(0.05, -1.55, -1.75)
+    				gt3_1.rot = QuatEuler(0, 0, 10)
+    				gt3_2.rot = QuatEuler(0, 0, -10)
+    			else
+    				gripfactorx = 1
+    				gripfactory = 1
+    				gt3_1.pos = Vec(0.3, -0.875, -1)
+    				gt3_2.pos = Vec(0.15, -0.875, -1)
+    				gt3_1.rot = QuatEuler(-90, 0, 0)
+    				gt3_2.rot = QuatEuler(-90, 0, 0)
+    			end
+    			gt3.pos = Vec(0.25, -0.875, -1)
+
+    		else
+    			gt3.pos = Vec(0, 0, 1000)
+    			gt3_1.pos = Vec(0, 0, 1000)
+    			gt3_2.pos = Vec(0, 0, 1000)
+    		end
+    		if grip == "grenade_launcher" then
+    			gripfactorx = 1.1
+    			gripfactory = 1.1
+    			glt.pos = Vec(0.2, -0.9, -1.4)
+    		else
+    			glt.pos = Vec(0, 0, 1000)
+    		end
+    		if grip == "" then
+    			gripfactorx = 1
+    			gripfactory = 1
+    		end
+
+    		barrelFactorx = 0.8
+    		barrelFactory = 1.2
+    		barrelFactordamage = 1
+    		accuracyFactor = 0.2
+    		barrellength = 0.4
+    		bt1.pos = bt1.pos
+    		bt0.pos = Vec(0, 0, 1000)
+    		bt2.pos = Vec(0, 0, 1000)
+    		bt3.pos = Vec(0, 0, 1000)
+
+    		if side == "side1" then
+    			sdt1.pos = sdt1.pos
+    		else
+    			sdt1.pos = Vec(0, 0, 1000)
+    		end
+    		if side == "side2" then
+    			sdt2.pos = sdt2.pos
+    		else
+    			sdt2.pos = Vec(0, 0, 1000)
+    		end
+    		if side == "side3" then
+    			sdt3.pos = sdt3.pos
+    		else
+    			sdt3.pos = Vec(0, 0, 1000)
+    		end
+
+    		if mag == "mag2" or mag == "mag3" then
+    			SetString("savegame.mod.stock", "", true)
+    		end
+    		if toprail ~= "holo" then
+    			SetString("savegame.mod.magnifier", "", true)
+    		end
+    		if guard == "guard2" and grip == "grenade_launcher" or ammotype == "308" and grip == "grenade_launcher"  then
+    			SetString("savegame.mod.grip", "", true)
+    			grip = ""
+    		end
+
+    		gdt0.pos = Vec(0, 0, 1000)
+    		gdt0_2.pos = Vec(0, 0, 1000)
+    		gdt1.pos = Vec(0, 0, 1000)
+    		gdt1_2.pos = Vec(0, 0, 1000)
+    		guardlength = 0
+
+    		SetShapeLocalTransform(bolt, bt)
+    		SetShapeLocalTransform(selector, st)
+    		SetShapeLocalTransform(suppressor, spt)
+    		SetShapeLocalTransform(scope, sct)
+    		SetShapeLocalTransform(holo, ht)
+    		SetShapeLocalTransform(holo2, ht2)
+    		SetShapeLocalTransform(reddot, rdt)
+    		SetShapeLocalTransform(reddot2, rdt2)
+    		SetShapeLocalTransform(scope2, sct2)
+    		SetShapeLocalTransform(scope2_2, sct2_2)
+    		SetShapeLocalTransform(g33, g33t)
+    		SetShapeLocalTransform(g33_2, g33t2)
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
+    		SetShapeLocalTransform(barrel3, bt3)
+    		SetShapeLocalTransform(side1, sdt1)
+    		SetShapeLocalTransform(side2, sdt2)
+    		SetShapeLocalTransform(side3, sdt3)
+    		SetShapeLocalTransform(grenade, grt)
+    		SetShapeLocalTransform(guard0, gdt0)
+    		SetShapeLocalTransform(guard0_2, gdt0_2)
+    		SetShapeLocalTransform(guard1, gdt1)
+    		SetShapeLocalTransform(guard1_2, gdt1_2)
+    	end
+
+    	if selectattachments then
+    		clickedmag = clickedmag1 or clickedmag2 or clickedmag3
+    		if clickedmag  and selectattachments and not InputPressed("t") then
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
+    			if reloadTimer < 0.5 and not cocksoundplaying and ammo == 0 then
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
+    	sightattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.15, -1))
+    	muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.35, -2.5))
+    	stockattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.4, -0.6))
+    	sideattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.45, -1.65))
+    	magattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.65, -1))
+    	gripattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.85, -1.4))
+    	barrelattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.65, -1.6))
+    	guardattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.5, -1.4))
+    	ammoattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.8, -0.75))
+    	magnifierattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.25, -0.7))
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
+    if GetString("game.player.tool") == "svu" and GetPlayerVehicle(playerId) == 0 then
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
+    				UiText(ammo.."/"..magsize*math.max(0, mags-1).." - "..selectfireText)
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
+    if GetString("game.player.tool") == "svu" and grenadelauncher and not selectattachments then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle")
+    		UiImage("ui/hud/crosshair-launcher.png")
+    	UiPop()
+    end
+    if GetString("game.player.tool") == "svu" and sideattachment and side == "side3" then
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
+    				UiAlign("center middle")
+    				clickedscope = AttachmentButton("toprail","sight3",true,{curx,cury},{"Scope","1x magnification sight for close range combat."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedholo = AttachmentButton("toprail","sight4",true,{curx,cury},{"Precision Scope","8x magnification sight for long range combat."})
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
+    					--clickedstockremoved = AttachmentButton("stock","removed",true,{curx,cury},{"Stock","Foldable for badasses only."})
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
+    				clickedgrip3 = AttachmentButton("grip","grip3",true,{curx,cury},{"Bipod","Increased accuracy while crouching or resting the gun on a ledge."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedgrip4 = AttachmentButton("grip","grenade_launcher",true,{curx,cury},{"GP-25","Grenade launcher for increased collateral damage."})
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
@@ -1,92 +1,4 @@
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
-	inside = {}
-	for i = 1,50 do
-		inside[i] = {0,0,0,0}
-	end
-	hoverindex = 0
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Dragunov SVU")
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
-	UiTranslate(0, 140)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-	hoverindex=0
-	UiPush()
-		local curx,cury=UiGetRelativePos()
-		UiAlign("center middle")
-		UiTranslate(50,-60)
-		clickedammo1 = AttachmentButton("conversion","Semi",true,{curx,cury},{"Semi","Default factory trigger group that allows the weapon to fire semi automatically."})
-		UiTranslate(-100,0)
-		clickedammo2 = AttachmentButton("conversion","Full",true,{curx,cury},{"Auto","Modified trigger group that allows the weapon to fire fully automatically."})
-	UiPop()
-	if GetString("savegame.mod.conversion") == "" then
-		SetString("savegame.mod.conversion", "Semi")
-	end
-end
-
+#version 2
 function optionsSlider(current, min, max, incri)
     UiPush()
         UiTranslate(0, -8)
@@ -148,17 +60,17 @@
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
@@ -191,4 +103,94 @@
 		inside[index][2]=math.max(0,inside[index][2]-dt*4)
 	end
 	return inside[index][2],inside[index][3],inside[index][4]
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
+    inside = {}
+    for i = 1,50 do
+    	inside[i] = {0,0,0,0}
+    end
+    hoverindex = 0
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Dragunov SVU")
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
+    UiTranslate(0, 140)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+    hoverindex=0
+    UiPush()
+    	local curx,cury=UiGetRelativePos()
+    	UiAlign("center middle")
+    	UiTranslate(50,-60)
+    	clickedammo1 = AttachmentButton("conversion","Semi",true,{curx,cury},{"Semi","Default factory trigger group that allows the weapon to fire semi automatically."})
+    	UiTranslate(-100,0)
+    	clickedammo2 = AttachmentButton("conversion","Full",true,{curx,cury},{"Auto","Modified trigger group that allows the weapon to fire fully automatically."})
+    UiPop()
+    if GetString("savegame.mod.conversion") == "" then
+    	SetString("savegame.mod.conversion", "Semi", true)
+    end
+end
+

```
