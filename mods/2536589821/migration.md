# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,362 +1,4 @@
---put horizontal recoil in an animation function to smooth it out like in tarkov
---update reload animations on this and other guns (mag out and in was changed)
-
-
-
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
-	--SetString("inventory.pickup", "ak105_AK-105_mag0-ak-545_6L23_30_30_5.45")
-
-	ammotype = GetString("savegame.mod.ammotype")
-	local ammotext = "5"
-	if ammotype == "556" then
-		ammotext = "2"
-	elseif ammotype == "762" then
-		ammotext = "4"
-	end
-
-	RegisterTool("ak105", "AK-10"..ammotext, "MOD/vox/ak105.vox", 3)
-	SetBool("game.tool.ak105.enabled", true)
-	SetFloat("game.tool.ak105.ammo", 101)
-
-
-	------INITIALISE OPTIONS MENU------
-	damageoption = GetInt("savegame.mod.damage")
-	if damageoption < 50 then
-		damageoption = 100
-		SetInt("savegame.mod.damage", 100)
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
-	magplaceslot = 1
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
-				placeItem({{mag, {0, 0}, w, h}, 0, 0}, magplaceslot, 2)
-				magplace = magplace + 1
-				magplaceslot = magplaceslot + w
-			else
-			end
-		end
-	end
-
-	local keybinds = {{"Reload","r"},{"Check-Mag","h"},{"Fire-Mode","v"},{"Lean-Left","q"},{"Lean-Right","e"},{"Attachments","t"},{"Melee","x"},{"Side-Attachment","b"},{"Grenade-Launcher","c"},{"Inspect-Weapon","y"},{"Clear-Jam","r"}}
-	for i = 1,#keybinds do
-		if GetString("savegame.mod."..keybinds[i][1]) == "" then
-			SetString("savegame.mod."..keybinds[i][1], keybinds[i][2])
-		end
-	end
-	reloadKey,magcheckKey,selectfireKey,leanleftKey,leanrightKey,attachmentsKey,meleeKey,sideKey,grenadeKey,inspectKey,clearjamKey=GetString("savegame.mod.Reload"),GetString("savegame.mod.Check-Mag"),GetString("savegame.mod.Fire-Mode"),GetString("savegame.mod.Lean-Left"),GetString("savegame.mod.Lean-Right"),GetString("savegame.mod.Attachments"),GetString("savegame.mod.Melee"),GetString("savegame.mod.Side-Attachment"),GetString("savegame.mod.Grenade-Launcher"),GetString("savegame.mod.Inspect-Weapon"),GetString("savegame.mod.Clear-Jam")
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
-	velocity = 850
-	drag = 1.5
-	maxMomentum = 2.5
-	tracer = false
-
-	recoilVertical = 0.8
-	recoilHorizontal = 6
-	recoilWander = 7
-
-	--armor pen
-	if ammotype == "545" then
-	lvl5armor = 0.05
-	lvl4armor = 0.2
-	lvl3armor = 0.5
-	lvl2armor = 0.9
-	lvl1armor = 1
-	elseif ammotype == "762" then
-	lvl5armor = 0
-	lvl4armor = 0.15
-	lvl3armor = 0.45
-	lvl2armor = 0.7
-	lvl1armor = 1
-	else
-	lvl5armor = 0.1
-	lvl4armor = 0.3
-	lvl3armor = 0.6
-	lvl2armor = 0.9
-	lvl1armor = 1
-	end
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
-	canted = GetString("savegame.mod.canted")
-	muzzle = GetString("savegame.mod.muzzle")
-	stock = GetString("savegame.mod.stock")
-	removestock = GetString("savegame.mod.removestock")
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
-	magtable2 = {{mslot1,0,0},{mslot2,0,0},{mslot3,0,0},{mslot4,0,0},{mslot5,0,0},{mslot6,0,0},{mslot7,0,0},{mslot8,0,0}}
-	for i=1,8 do
-		local magslottype = GetString("savegame.mod.mslot"..i)
-		if magslottype == "mag0" then
-			magtable2[i][2] = 30
-			magtable2[i][3] = 30
-		elseif magslottype == "mag1" then
-			magtable2[i][2] = 45
-			magtable2[i][3] = 45
-		elseif magslottype == "mag2" then
-			magtable2[i][2] = 77
-			magtable2[i][3] = 77
-		elseif magslottype == "mag3" then
-			magtable2[i][2] = 95
-			magtable2[i][3] = 95
-		end
-	end
-	curmagslot = 1
-	nextmagslot = 1
-	if realistic then
-		mag = mslot1
-		reloadFactor = 1
-	else
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
-	dustcover = GetString("savegame.mod.dustcover")
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
-	shotDelay = 0.09
-	spreadTimer = 1.25
-	spreadFactor = 1.5
-	accuracyFactor = 1
-	bipodFactor = 1
-	laserFactor = 1
-	if not realistic then
-		if mag == "" then
-			magsize = 30
-			reloadFactor = 1.2
-		elseif mag == "mag1" then
-			magsize = 45
-			reloadFactor = 1.4
-		elseif mag == "mag2" then
-			magsize = 77
-			reloadFactor = 1.55
-		else
-			magsize = 95
-			reloadFactor = 1.7
-		end
-		ammo = magsize
-	else
-		ammo = magtable2[curmagslot][2]
-	end
-	barrellength = 0
-	barrelFactorx = 0.8
-	barrelFactory = 1
-	barrelFactordamage = 1.25
-	ammoFactory = 1
-	ammoFactordamage = 1
-	ammoFactorvelocity = 1
-	grenadelauncherammo = 1
-	mags = 2
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
-	for i=1, 100 do
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
-	selectfireText = "Full"
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
@@ -428,13 +70,13 @@
 	loadedShell.predictedBulletVelocity = VecAdd(loadedShell.predictedBulletVelocity, Vec((math.random()-0.5)*accuracyFactor*2, (math.random()-0.5)*accuracyFactor*2, (math.random()-0.5)*accuracyFactor*2))
 
 	local barrelend = barrellength + muzzlelength
-	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 2), GetPlayerVelocity()), 0.2, 0.3)
+	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 2), GetPlayerVelocity(playerId)), 0.2, 0.3)
 	ParticleType("plain")
 	ParticleTile(5)
 	ParticleColor(1, 0.6, 0.4, 1, 0.3, 0.2)
 	ParticleRadius(0.2)
 	ParticleEmissive(5, 1)
-	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 4), GetPlayerVelocity()), shotDelay/2, 0.3)
+	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.55, -2.4-barrelend*4/3)), VecAdd(VecScale(dir, 4), GetPlayerVelocity(playerId)), shotDelay/2, 0.3)
 	ParticleReset()
 	ParticleType("plain")
 	ParticleTile(6)
@@ -446,14 +88,14 @@
 	ParticleGravity(-10)
 	ParticleCollide(0)
 	for i = 1, math.random(8, 16) do
-		SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecAdd(VecScale(dir, 25), GetPlayerVelocity()), Vec((math.random(-100,100)/100)*4,(math.random(-100,100)/100)*4, (math.random(-100,100)/100)*4)), shotDelay)
+		SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -2.4-barrelend*4/3)), VecAdd(VecAdd(VecScale(dir, 25), GetPlayerVelocity(playerId)), Vec((math.random(-100,100)/100)*4,(math.random(-100,100)/100)*4, (math.random(-100,100)/100)*4)), shotDelay)
 	end
 	if muzzle == "muzzle1" then
-		PlaySound(suppressedgunsound, GetPlayerTransform().pos, 1, false)
+		PlaySound(suppressedgunsound, GetPlayerTransform(playerId).pos, 1, false)
 	elseif muzzle == "muzzle2" then
-		PlaySound(gunsound, GetPlayerTransform().pos, 0.9, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.9, false)
 	else
-		PlaySound(gunsound, GetPlayerTransform().pos, 0.75, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.75, false)
 	end
 
 	if not unlimitedammo then
@@ -488,22 +130,23 @@
 	end
 
 	local jamrate = 1/800
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
 	ppos2.rot = QuatRotateQuat(ppos2.rot, QuatEuler(recoilFactor*muzzleFactor*gripfactory*barrelFactory*3-rnd4/4, -rnd5/4, -rnd6/4))
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
@@ -537,7 +180,7 @@
 	ak47grenadeHandler.shellNum = (ak47grenadeHandler.shellNum%#ak47grenadeHandler.shells) + 1
 
 	SpawnParticle("fire", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(grenadelaunchersound, GetPlayerTransform().pos, 0.75, false)
+	PlaySound(grenadelaunchersound, GetPlayerTransform(playerId).pos, 0.75, false)
 
 	if not unlimitedammo then
 		grenadelauncherammo = grenadelauncherammo - 1
@@ -633,7 +276,7 @@
 
 			local factor = barrelFactordamage*ammoFactordamage
 
-			if projectile.momentum > 0 then
+			if projectile.momentum ~= 0 then
 				MakeHole(hitPos, damage*factor, damage*0.85*factor, damage*0.7*factor)
 			end
 		end
@@ -693,7 +336,7 @@
 			curmagslot = nextmagslot
 		end
 		magoutTimer = 0.6
-		PlaySound(reloadsound, GetPlayerTransform().pos, 0.6, false)
+		PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	end
 end
 
@@ -715,7 +358,7 @@
 	local gt = GetBodyTransform(GetToolBody())
 	local casingpos = TransformToParentPoint(gt, Vec(0.55, -0.55, -1.15))
 	local fwdpos = TransformToParentPoint(gt, Vec(6+math.random()*4, 0.5+math.random()*4, -0.65+math.random()*4))
-	local direction = VecAdd(GetPlayerVelocity(), VecSub(fwdpos, casingpos))
+	local direction = VecAdd(GetPlayerVelocity(playerId), VecSub(fwdpos, casingpos))
 	casing = Spawn("MOD/vox/casing.xml", Transform(casingpos, QuatEuler(math.random(0, 90), math.random(0, 90), math.random(0, 90))))
 	SetBodyVelocity(casing[1], direction)
 end
@@ -770,17 +413,17 @@
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
@@ -815,7 +458,7 @@
 		end
 		UiImageBox("ui/common/box-solid-shadow-50.png",120,120,6,6)
 
-		local ppos=GetPlayerTransform(GetToolBody())
+		local ppos=GetPlayerTransform(playerId, GetToolBody())
 		order = 1-order
 		location2 = TransformToParentPoint(ppos, Vec(optionsx*3+math.sin(order*math.pi*1.5-math.pi*1.66)*3, 1-math.cos(order*math.pi*1.5-math.pi*1.66)*2, -5))
 		DebugLine(location, location2, 1, 1, 1, 1)
@@ -826,11 +469,11 @@
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
@@ -845,8 +488,8 @@
 			keys = {"q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m","[","]",";",",","."}
 			for i = 1,#keys do
 				if InputPressed(keys[i]) then
-					SetString("savegame.mod."..keybind, keys[i])
-					SetString("savegame.mod.currentkey", "")
+					SetString("savegame.mod."..keybind, keys[i], true)
+					SetString("savegame.mod.currentkey", "", true)
 				end
 			end
 		else
@@ -860,8 +503,8 @@
 		UiImageBox("ui/common/box-outline-6.png",ww,wh,6,6)
 		if UiTextButton(keybind..": "..string.upper(GetString("savegame.mod."..keybind)))then
 			clicked=true
-			PlaySound(uiselect, GetPlayerTransform().pos, 1)
-			SetString("savegame.mod.currentkey", keybind)
+			PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
+			SetString("savegame.mod.currentkey", keybind, true)
 		end
 	UiPop()
 	return clicked,ww,wh
@@ -885,13 +528,13 @@
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
@@ -1016,6 +659,7 @@
 			laserFactor = 1
 		end
 end
+
 function Flashlight(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.125, -0.625, -1.9))
@@ -1034,6 +678,7 @@
 			SetShapeEmissiveScale(side2, 0)
 		end
 end
+
 function Rangefinder(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.175, -0.625, -1.9))
@@ -1110,27 +755,27 @@
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
@@ -1194,32 +839,32 @@
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
@@ -1271,32 +916,32 @@
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
@@ -1348,32 +993,32 @@
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
@@ -1425,32 +1070,32 @@
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
@@ -1489,2337 +1134,12 @@
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
-	if GetString("game.player.tool") == "ak105" and GetPlayerVehicle() == 0 then
-		SetBool("hud.aimdot", false)
-
-
-		------CONTROLS------
-		if InputDown("lmb") and not reloading and selectfire == 1 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-			end
-		elseif InputPressed("lmb") and not reloading and selectfire == 2 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
-			if grenadelauncherammo > 0 and grenadelauncher then
-				ShootGrenade()
-			elseif not grenadelauncher and ammo > 0 then
-				Shoot()
-				shootTimer = 0.11
-			end
-		end
-
-		if InputPressed("lmb") and not reloading and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and jamclearTimer == 0 then
-			spreadTimer = 1.25
-			if (ammo == 0 or selectfire == 0 or jammed) and not selectattachments and not selectmag then
-				PlaySound(dryfiresound, GetPlayerTransform().pos, 1, false)
-			end
-		end
-
-		if InputReleased("lmb") and not reloading and selectfire > 0 then
-			shootTimer = 0
-		end
-
-		if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and not selectmag and GetPlayerGrabShape() == 0 and magcheckTimer == 0 and jamclearTimer == 0 and magcheckTimer == 0 and jamclearTimer == 0 then
-			if InputPressed("rmb") then
-				PlaySound(interactsound1, GetPlayerTransform().pos, 1)
-			end
-			ironsight = true
-			inspectTimer = 0
-			if scopeTimer < 0.5 and not reloading and not (q or e) and selectfireTimer == 0 then
-				scopeTimer = scopeTimer + dt
-			end
-		end
-		if not InputDown("rmb") then
-			ironsight = false
-		end
-		if selectfire == 0 and selectfireTimer <= 0 then
-			ironsight = false
-		end
-		if (not InputDown("rmb") or reloading or q or e or selectfireTimer > 0) and scopeTimer > 0 then scopeTimer = scopeTimer - dt end
-
-		if InputPressed(leanrightKey) then
-			e = not e
-			q = false
-		end
-
-		if InputPressed(leanleftKey) then
-			q = not q
-			e = false
-		end
-
-		if InputDown("alt") and InputPressed("rmb") or InputDown("rmb") and InputPressed("alt") then
-			altaim = not altaim
-			if toprail == "scope3" or toprail == "scope4" then
-				PlaySound(selectsound, GetPlayerTransform().pos, 0.85)
-			end
-		end
-		if toprail ~= "scope2" and toprail ~= "scope3" and toprail ~= "scope4" then
-			altaim = false
-		end
-		if InputPressed("c") then
-			switchsights = not switchsights
-		end
-		if canted == "" then
-			switchsights = false
-		end
-
-		if InputPressed(meleeKey) and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") and not selectattachments then
-			meleeTimer = 0.8
-		end
-
-		if InputPressed(selectfireKey) and not reloading and not selectattachments and not selectmag and magcheckTimer == 0 and jamclearTimer == 0 then
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
-		if InputDown(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 or GetBool("level.optionstriggered") then
-			if InputPressed(attachmentsKey) and not GetBool("level.optionstriggered") then
-				PlaySound(interactsound2, GetPlayerTransform().pos, 1)
-				selectattachmentsTimer = 0.5
-			end
-			UiMakeInteractive()
-			selectattachments = true
-			ironsight = false
-			inspectTimer = 0
-		end
-		if InputReleased(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") then
-			selectattachments = false
-			selectattachmentsTimer = 0.25
-		end
-
-		if InputPressed(sideKey) and side ~= "" then
-			sideattachment = not sideattachment
-			PlaySound(uiselect, GetPlayerTransform().pos, 0.75)
-		end
-		Laser(sideattachment and side == "side1")
-		Flashlight(sideattachment and side == "side2")
-		Rangefinder(sideattachment and side == "side3")
-
-		if InputPressed(magcheckKey) and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 then
-			magcheckTimer = 3
-			PlaySound(reloadsound, GetPlayerTransform().pos, 0.6)
-			inspectTimer = 0
-		end
-		if magcheckTimer > 0 then
-			magcheckTimer = magcheckTimer - dt
-			ironsight = false
-		end
-		if magcheckTimer < 0 then
-			magcheckTimer = 0
-			reloadsound2playing = false
-		end
-
-		if InputDown(reloadKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then heldrTimer = heldrTimer + dt end
-		if InputDown(reloadKey) and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 and heldrTimer > 0.2 then
-			UiMakeInteractive()
-			selectmag = true
-			ironsight = false
-		else
-			selectmag = false
-		end
-		if InputReleased(reloadKey) and heldrTimer <= 0.2 and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
-			if totalmags > 0 then
-			for i = 1, totalmags do
-				if magtable2[i][2] > magtable2[nextmagslot][2] and i ~= curmagslot then
-					nextmagslot = i
-				end
-			end
-			end
-			inspectTimer = 0
-			Reload()
-		end
-		if InputReleased(reloadKey) then heldrTimer = 0 end
-
-		if InputPressed(clearjamKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jammed and jamclearTimer == 0 then
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
-
-		if InputDown("shift") then
-			ironsight = false
-			selectattachments = false
-			inspectTimer = 0
-		end
-
-		if grip == "grenade_launcher" then
-			if InputPressed(grenadeKey) and not reloading then
-				grenadelauncher = not grenadelauncher
-			end
-		else
-			grenadelauncher = false
-		end
-
-		if InputPressed(inspectKey) and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire > 0 and not selectattachments and magcheckTimer == 0 and jamclearTimer == 0 then
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
-
-		------WEAPON FUNCTIONS AND ANIMATIONS------
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
-			recoilFactor = recoilVertical*stockFactor*ammoFactory
-		else
-			recoilFactor = recoilVertical*stockFactor*ammoFactory*1.75
-		end
-
-		if ironsight then
-			recoilMax = 10*muzzleFactor*gripfactory*barrelFactory
-		else
-			recoilMax = 20*muzzleFactor*gripfactory*barrelFactory
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
-		removestock = GetString("savegame.mod.removestock")
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
-		dustcover = GetString("savegame.mod.dustcover")
-		ammotype = GetString("savegame.mod.ammotype")
-		if ammotype == "" then
-			SetString("savegame.mod.ammotype", "545")
-			maxMomentum = 2.5
-			ammoFactory = 1
-			ammoFactordamage = 1
-			ammoFactorvelocity = 1
-		elseif ammotype == "762" then
-			maxMomentum = 3
-			ammoFactory = 1.25
-			ammoFactordamage = 1.1
-			ammoFactorvelocity = 0.85
-		elseif ammotype == "556" then
-			maxMomentum = 3
-			ammoFactory = 1.2
-			ammoFactordamage = 1.2
-			ammoFactorvelocity = 1.2
-		else
-			maxMomentum = 2.5
-			ammoFactory = 1
-			ammoFactordamage = 1
-			ammoFactorvelocity = 1
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
-			local adsFOV, adsTime = 0, 0
-			local defaultTrans = Transform(Vec(0.25, 0.15, 0.25), QuatEuler(0, 0, 0))
-
-			x,y,z,rotx,roty,rotz = -0.1,0.2,0,0,0,0
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
-					y = 0.3075
-					z = 0.2
-					rotz = 0
-				elseif toprail == "kobra" then
-					x = 0.275
-					y = 0.35
-					z = 0.2
-					rotz = 0
-				elseif toprail == "sight3" then
-					x = 0.275
-					y = 0.2625
-					z = 0.2
-					rotz = 0
-				elseif toprail == "" then
-					x = 0.275
-					y = 0.39
-					z = 0.2
-					rotz = 0
-				elseif toprail == "scope" then
-					x = 0.275
-					y = 0.3
-					z = 0.2
-					rotz = 0
-				elseif toprail == "scope3" then
-					x = 0.275
-					y = 0.25
-					z = 0.2
-					rotz = 0.1
-				elseif toprail == "scope2" then
-					if altaim then
-						x = 0.275
-						y = 0.1625
-						z = 0.2
-					else
-						x = 0.275
-						y = 0.3
-						z = 0.2
-					end
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
-				elseif toprail == "scope2" then
-					if altaim then
-						adsFOV, adsTime = 10, 0.15
-					else
-						adsFOV, adsTime = 80, 0.25
-					end
-				elseif toprail == "holo" then
-					adsFOV, adsTime = 20, 0.1
-				elseif toprail == "kobra" then
-					adsFOV, adsTime = 10, 0.1
-				elseif toprail == "sight3" then
-					adsFOV, adsTime = 10, 0.1
-				elseif toprail == "scope3" then
-					if altaim then
-						adsFOV = 80
-					else
-						adsFOV = 10
-					end
-					if ironsight and scopeTimer >= 0.5 then
-						adsTime = 0
-					else
-						adsTime = 0.15
-					end
-				end
-			elseif grenadelauncher then
-				adsFOV, adsTime = 10, 0.15
-			else
-				adsFOV, adsTime = 0, 0.15
-			end
-			end
-
-			--offset = ADS(ironsight, adsFOV, adsTime, -x, y, z, rotz)
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
-					local sightcenter = Vec(0.275, -0.3, -1)
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
-						reticle1 = LoadSprite("MOD/img/reticle1.png")
-						DrawSprite(reticle1, holotrans, 0.025, 0.025, 1, 1, 1, 1, true)
-					end
-				end
-				if toprail == "scope2" and altaim then
-					local gt = GetBodyTransform(GetToolBody())
-					local sightcenter = Vec(0.275, -0.1625, -1.2)
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
-						reticle4 = LoadSprite("MOD/img/reticle5.png")
-						DrawSprite(reticle4, holotrans, 0.2, 0.15, 1, 1, 1, 1, true)
-					end
-				end
-				if toprail == "kobra" then
-					local gt = GetBodyTransform(GetToolBody())
-					local sightcenter = Vec(0.275, -0.35, -1)
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
-					if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.05 then
-						reticle4 = LoadSprite("MOD/img/reticle4_ak.png")
-						DrawSprite(reticle4, holotrans, 0.1, 0.1, 1, 1, 1, 1, true)
-					end
-				end
-				if toprail == "sight3" then
-					local gt = GetBodyTransform(GetToolBody())
-					local sightcenter = Vec(0.275, -0.2625, -1)
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
-					if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.05 then
-						reticle4 = LoadSprite("MOD/img/reticle4.png")
-						DrawSprite(reticle4, holotrans, 0.1, 0.1, 1, 1, 1, 1, true)
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
-				recoilTimer2 = recoilTimer2 - (recoilTimer2*0.1+dt)
-				offset.pos = VecAdd(offset.pos, Vec(0, 0, recoilTimer2/8))
-				offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer2)*3, 0, 0))
-			end
-			if recoilTimer > 0 then
-				recoilTimer = recoilTimer - dt
-				boltoffset = Vec(-0.001, -0.001, recoilTimer*3.5)
-			end
-			if recoilTimer < 0 then
-				recoilTimer = 0
-			end
-			if recoilTimer2 < 0 then
-				recoilTimer2 = 0
-			end
-			local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/400, (recoilAngle/-150)-(rnd1+rnd4)/400-recoilTimer2/8, recoilAngle/75+(rnd3+rnd6)/200+recoilTimer2/1.5+recoilTimer2/32, (recoilTimer2)*3+recoilAngle+(rnd1+rnd4)/4+(recoilTimer2-0.02)*2, (rnd2+rnd5)/4, (rnd3+rnd6)/4
-			-- RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
-			-- offset.pos = VecAdd(offset.pos, RECoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, RECoffset.rot)
-
-			if jammed and jamclearTimer < 1 and jamclearTimer > 0.7 then
-				boltoffset = Vec(-0.001, -0.001, 1-jamclearTimer)
-				if not cocksoundplaying then
-					cocksoundplaying = true
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.85)
-				end
-			end
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
-				PlaySound(interactsound3, GetPlayerTransform().pos, 0.5, false)
-			end
-			if maginTimer < 0.4 and not reloadsound2playing and not grenadelauncher then
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
-			if magcheckTimer > 2.7 then
-				magoffset = Vec(0, 0, -(3-magcheckTimer)*1.5)
-			elseif magcheckTimer > 2.4 and magcheckTimer < 3.7 then
-				magoffset = Vec(0, -(2.7-magcheckTimer), -0.45)
-			elseif magcheckTimer > 1.8 then
-				magoffset = Vec(-(2.4-magcheckTimer)*0.5, (2.4-magcheckTimer)/2-0.3, -0.45)
-			elseif magcheckTimer > 0.7 then
-				magoffset = Vec(-0.3, 0, -0.45)
-				if not reloadsound2playing then
-					PlaySound(reloadsound2, GetPlayerTransform().pos, 0.6)
-					reloadsound2playing = true
-				end
-			elseif magcheckTimer > 0.4 then
-				magoffset = Vec(-magcheckTimer+0.4, magcheckTimer-0.7, -0.45)
-			elseif magcheckTimer > 0.2 then
-				magoffset = Vec(0, -magcheckTimer*2/3, -(magcheckTimer)*2.25/2)
-			elseif magcheckTimer > 0 then
-				magoffset = Vec(0, 0, -(magcheckTimer)*2.25/2)
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
-					elseif magoutTimer > 0 or magcheckTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 0, -10
-					elseif maginTimer > 0 or reloadTimer > 0.8 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 10, -5
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.25, 0.25, -0.2, -10, 5, -40
-					end
-				elseif e then
-					if magoutTimer > 0 or magcheckTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.1, 0, 5, -10, -10
-					elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, -0.1, -5, 15, 0
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = -1, -1.3, -0.4, 50, -50, 80
-					end
-				else
-					if magoutTimer > 0 or magcheckTimer > 0 then
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
-				if magoutTimer > 0 or magcheckTimer > 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.15, -0.05, 0, 5, -5, -20
-				elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.35, -0.05, 0.1, 10, 10, -25
-				elseif reloadTimer < 0.8 and ammo == 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = -0.8, -0.9, -0.4, 40, -40, 55
-				end
-			end
-			end
-
-			-- RELoffset = REL(reloading or magcheckTimer > 0, x1, y1, z1, rotx1, roty1, rotz1)
-			-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
-
-			if reloadTimer < 0.5 and reloadTimer > 0.2 and reloading and ammo == 0 then
-				boltoffset = Vec(-0.001, -0.001, (0.5-reloadTimer)*0.75)
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
-				x2, y2, z2, rotx2, roty2, rotz2 = -0.75, -0.5, 0, 10, 0, 50
-			elseif jamclearTimer > 0 then
-				x2, y2, z2, rotx2, roty2, rotz2 = -0.75, -0.5, 0, 10, 0, 50
-			end
-
-			-- INSoffset = INS(inspectTimer > 0 or jamclearTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
-			-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
-
-			local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = 0.4, 0.2, -0.2, -20, 60, 0
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
-			for i = 55, 66 do
-				SetShapeLocalTransform(bs[i], hideTrans)
-			end
-			if clothingtype == "camo" then
-				hand1 = bs[58]
-				arm1 = bs[60]
-				hand2 = bs[59]
-			elseif clothingtype == "swat" then
-				hand1 = bs[61]
-				arm1 = bs[63]
-				hand2 = bs[62]
-			elseif clothingtype == "camo2" then
-				hand1 = bs[64]
-				arm1 = bs[66]
-				hand2 = bs[65]
-			else
-				hand1 = bs[55]
-				arm1 = bs[57]
-				hand2 = bs[56]
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
-				mag0_762 = shapes[30]
-				mag0_556 = shapes[32]
-				bolt = shapes[3]
-				selector = shapes[4]
-				suppressor = shapes[5]
-				scope = shapes[6]
-				holo = shapes[7]
-				holo2 = shapes[8]
-				kobra = shapes[67]
-				leupold = shapes[46]
-				leupold_2 = shapes[47]
-				reddot = shapes[50]
-				reddot2 = shapes[51]
-				rail = shapes[9]
-				rail2 = shapes[42]
-				rail3 = shapes[43]
-				stock0 = shapes[10]
-				muzzlebreak = shapes[11]
-				muzzlebreak2 = shapes[12]
-				mag1 = shapes[13]
-				mag1_762 = shapes[31]
-				mag1_556 = shapes[33]
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
-				guard0 = shapes[34]
-				guard0_2 = shapes[35]
-				guard2 = shapes[36]
-				guard2_2 = shapes[37]
-				guard1 = shapes[38]
-				guard1_2 = shapes[39]
-				guard3 = shapes[40]
-				guard3_2 = shapes[41]
-				stock1 = shapes[44]
-				stock1_2 = shapes[45]
-				stock2 = shapes[54]
-				scope3 = shapes[52]
-				scope3_2 = shapes[53]
-				g33 = shapes[48]
-				g33_2 = shapes[49]
-				magTrans = GetShapeLocalTransform(mag0)
-				boltTrans = GetShapeLocalTransform(bolt)
-				selectorTrans = GetShapeLocalTransform(selector)
-				suppressorTrans = GetShapeLocalTransform(suppressor)
-				scopeTrans = GetShapeLocalTransform(scope)
-				holoTrans = GetShapeLocalTransform(holo)
-				holoTrans2 = GetShapeLocalTransform(holo2)
-				kobraTrans = GetShapeLocalTransform(kobra)
-				g33Trans = GetShapeLocalTransform(g33)
-				leupoldTrans = GetShapeLocalTransform(leupold)
-				leupoldTrans2 = GetShapeLocalTransform(leupold_2)
-				reddotTrans = GetShapeLocalTransform(reddot)
-				railTrans = GetShapeLocalTransform(rail)
-				railTrans2 = GetShapeLocalTransform(rail2)
-				railTrans3 = GetShapeLocalTransform(rail3)
-				stock0Trans = GetShapeLocalTransform(stock0)
-				stock1Trans = GetShapeLocalTransform(stock1)
-				stock1_2Trans = GetShapeLocalTransform(stock1_2)
-				stock2Trans = GetShapeLocalTransform(stock2)
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
-				scopeTrans3 = GetShapeLocalTransform(scope3)
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
-
-			ht = TransformCopy(holoTrans)
-			ht2 = TransformCopy(holoTrans2)
-
-			kbt = TransformCopy(kobraTrans)
-
-			lpt = TransformCopy(leupoldTrans)
-			lpt2 = TransformCopy(leupoldTrans2)
-
-			g33t = TransformCopy(g33Trans)
-			g33t2 = TransformCopy(g33Trans)
-
-			rdt = TransformCopy(reddotTrans)
-			rdt2 = TransformCopy(reddotTrans)
-
-			sct3 = TransformCopy(scopeTrans3)
-			sct3_2 = TransformCopy(scopeTrans3)
-
-			rt = TransformCopy(railTrans)
-			rt2 = TransformCopy(railTrans2)
-			rt3 = TransformCopy(railTrans3)
-
-			stt0 = TransformCopy(stock0Trans)
-			stt1 = TransformCopy(stock1Trans)
-			stt1_2 = TransformCopy(stock1_2Trans)
-			stt2 = TransformCopy(stock2Trans)
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
-			gdt0 = TransformCopy(guardTrans0)
-			gdt0_2 = TransformCopy(guardTrans0)
-			gdt1 = TransformCopy(guardTrans0)
-			gdt1_2 = TransformCopy(guardTrans0)
-			gdt2 = TransformCopy(guardTrans0)
-			gdt2_2 = TransformCopy(guardTrans0)
-			gdt3 = TransformCopy(guardTrans0)
-			gdt3_2 = TransformCopy(guardTrans0)
-
-			if not grenadelauncher then
-				if magoutTimer > 0 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler((0.6-magoutTimer)*120, 0, 0))
-				elseif maginTimer >= 0.2 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(30, 0, 0))
-				elseif maginTimer > 0 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(maginTimer*180, 0, 0))
-				end
-				if magcheckTimer > 2.7 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler((3-magcheckTimer)*120, 0, 0))
-				elseif magcheckTimer >= 0.6 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(30, 0, 0))
-				elseif magcheckTimer > 0 then
-					mt.rot = QuatRotateQuat(mt.rot, QuatEuler(magcheckTimer*60, 0, 0))
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
-					st.rot = QuatEuler(-100, 0, 0)
-				else
-					st.rot = QuatEuler(-70, 0, 0)
-				end
-			end
-
-			muzzlelength = 0
-			if muzzle == "muzzle1" then
-				spt.pos = VecAdd(spt.pos, Vec(0.075, -0.05, -barrellength))
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
-				mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, -barrellength))
-				mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0, -barrellength))
-				mbt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 3
-				muzzleFactor = 0.75
-			else
-				mbt.pos = hidePos
-				mbt2.pos = hidePos
-				mbt.rot = QuatEuler(0, 0, 0)
-				lightFactor = 2
-				muzzleFactor = 1
-				muzzlelength = 0.2
-			end
-			if toprail == "scope" and (not ironsight or reloading or scopeTimer < 0.5 or q or e) then
-				sct.pos = Vec(0.15, -0.675, -0.625)
-			else
-				sct.pos = hidePos
-			end
-			if toprail == "holo" then
-				ht.pos = Vec(0.175, -0.475, -0.875)
-				ht2.pos = Vec(0.2, -0.45, -0.885)
-			else
-				ht.pos = hidePos
-				ht2.pos = hidePos
-			end
-			if toprail == "kobra" then
-				kbt.pos = Vec(0.15, -0.725, -0.65)
-			else
-				kbt.pos = hidePos
-			end
-			if toprail == "scope2" and ((not ironsight or reloading or scopeTimer < 0.5 or q or e) or altaim) then
-				lpt.pos = Vec(0.2, -0.475, -0.725)
-				lpt2.pos = Vec(0.175, -0.4, -0.75)
-			else
-				lpt.pos = hidePos
-				lpt2.pos = hidePos
-			end
-			if toprail == "sight3" then
-				rdt.pos = Vec(0.175, -0.425, -0.975)
-				rdt2.pos = Vec(0.2, -0.45, -1.025)
-			else
-				rdt.pos = hidePos
-				rdt2.pos = hidePos
-			end
-			if toprail == "scope3" and ((not ironsight or reloading or scopeTimer < 0.5 or q or e) or (canted == "sight5" and switchsights)) then
-				sct3.pos = Vec(0.175, -0.445, -0.525)
-				sct3_2.pos = Vec(0.15, -0.42, -0.675)
-			else
-				sct3.pos = hidePos
-				sct3_2.pos = hidePos
-			end
-			if magnifier == "g33" then
-				g33t.pos = Vec(0.175, -0.425-0.045, -0.725+0.05)
-				if magnified then
-					g33t2.pos = Vec(0.2, -0.3375-0.045, -0.475+0.05)
-				else
-					g33t2.pos = Vec(0.35, -0.1875-0.045, -0.475+0.05)
-					g33t2.rot = QuatRotateQuat(g33t2.rot, QuatEuler(0, 90, 0))
-				end
-			else
-				g33t.pos = hidePos
-				g33t2.pos = hidePos
-			end
-			if removestock == "removed" then
-				stt0.pos = Vec(0.2, -0.95, -1.35)
-				stt0.rot = QuatEuler(-90, 180, 0)
-				stt1.pos = Vec(0.55, -0.95, -1.2)
-				stt1.rot = QuatEuler(-90, -180, 0)
-				stt2.pos = Vec(0.2, -0.95, -1.35)
-				stt2.rot = QuatEuler(-90, 180, 0)
-				stockFactor = 3
-			end
-			if stock == "stock1" then
-				stt0.pos = hidePos
-				stt2.pos = hidePos
-				stockFactor = 0.9
-			elseif stock == "stock2" then
-				stt0.pos = hidePos
-				stt1.pos = hidePos
-				stt1_2.pos = hidePos
-				stockFactor = 1.1
-			elseif stock == "" then
-				stt1.pos = hidePos
-				stt1_2.pos = hidePos
-				stt2.pos = hidePos
-				stockFactor = 1
-			end
-			if stock == "removed" then
-				stt0.pos = hidePos
-				stt1.pos = hidePos
-				stt1_2.pos = hidePos
-				stt2.pos = hidePos
-				stockFactor = 3
-			end
-			if removestock == "removed" then
-				stockFactor = 3
-			end
-
-			rt.pos = hidePos
-			rt2.pos = hidePos
-			rt3.pos = hidePos
-			if dustcover == "" then
-				rt.pos = Vec(0.225, -0.575, -0.625)
-			elseif dustcover == "cover2" then
-				rt2.pos = Vec(0.225, -0.575, -0.625)
-				rt3.pos = Vec(0.25, -0.5, -0.75)
-			end
-
-			SetShapeLocalTransform(mag0, hideTrans)
-			SetShapeLocalTransform(mag1, hideTrans)
-			SetShapeLocalTransform(mag2, hideTrans)
-			SetShapeLocalTransform(mag3, hideTrans)
-			SetShapeLocalTransform(mag0_762, hideTrans)
-			SetShapeLocalTransform(mag1_762, hideTrans)
-			SetShapeLocalTransform(mag0_556, hideTrans)
-			SetShapeLocalTransform(mag1_556, hideTrans)
-			if mag == "" or mag == "mag0" then
-				magsize = 30
-				reloadFactor = 1.2
-				if ammotype == "762" then
-					SetShapeLocalTransform(mag0_762, Transform(VecAdd(mt.pos, Vec(0, -0.05, 0)), mt.rot))
-				elseif ammotype == "556" then
-					SetShapeLocalTransform(mag0_556, mt)
-				else
-					SetShapeLocalTransform(mag0, mt)
-				end
-			elseif mag == "mag1" then
-				magsize = 45
-				reloadFactor = 1.4
-				if ammotype == "762" then
-					SetShapeLocalTransform(mag1_762, Transform(VecAdd(mt.pos, Vec(0, -0.1, 0)), mt.rot))
-				elseif ammotype == "556" then
-					SetShapeLocalTransform(mag1_556, Transform(VecAdd(mt.pos, Vec(0, -0.15, 0)), mt.rot))
-				else
-					SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(0, -0.1, 0)), mt.rot))
-				end
-			elseif mag == "mag2" then
-				magsize = 77
-				reloadFactor = 1.75
-				SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.15, 0.05, 0)), mt.rot))
-			elseif mag == "mag3" then
-				magsize = 95
-				reloadFactor = 2.25
-				SetShapeLocalTransform(mag3, Transform(VecAdd(mt.pos, Vec(-0.45, 0.1, 0)), mt.rot))
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
-						gt3_1.pos = Vec(0.3, -0.725, -1.35-barrellength)
-						gt3_2.pos = Vec(0.15, -0.725, -1.35-barrellength)
-					else
-						gt3_1.pos = Vec(0.3, -0.675, -2.8-barrellength)
-						gt3_2.pos = Vec(0.15, -0.675, -2.8-barrellength)
-						gt3_1.rot = QuatEuler(90, 0, 0)
-						gt3_2.rot = QuatEuler(90, 0, 0)
-					end
-					
-				end
-				gt3.pos = Vec(0.225, -0.725, -2-barrellength)
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
-				accuracyFactor = 1*bipodFactor
-				barrellength = 0
-				bt0.pos = bt0.pos
-			else
-				bt0.pos = hidePos
-			end
-			if barrel == "barrel1" then
-				barrelFactorx = 0.8
-				barrelFactory = 1.05
-				barrelFactordamage = 1
-				accuracyFactor = 0.8*bipodFactor
-				barrellength = 0.35
-				bt1.pos = bt1.pos
-			else
-				bt1.pos = hidePos
-			end
-			if barrel == "barrel2" then
-				barrelFactorx = 0.8
-				barrelFactory = 1.1
-				barrelFactordamage = 1.25
-				accuracyFactor = 0.6*bipodFactor
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
-			if toprail ~= "holo" then
-				SetString("savegame.mod.magnifier", "")
-			end
-
-			if mag == "mag2" or mag == "mag3" or toprail == "scope" or toprail == "kobra" then
-				SetString("savegame.mod.removestock", "")
-			end
-			if guard == "" and grip ~= "grenade_launcher" and grip ~= "grip3" then
-				SetString("savegame.mod.grip", "")
-			end
-			if guard ~= "" and grip == "grenade_launcher" then
-				SetString("savegame.mod.grip", "")
-			end
-			if guard == "guard2" and barrel == "" and grip == "grip3" then
-				SetString("savegame.mod.grip", "")
-			end
-			if dustcover == "" and toprail ~= "scope" and toprail ~= "kobra" then
-				SetString("savegame.mod.toprail", "")
-			end
-			if dustcover ~= "" and toprail == "kobra" then
-				SetString("savegame.mod.toprail", "")
-			end
-			if guard == "" or guard == "guard3" then
-				SetString("savegame.mod.side", "")
-			end
-
-			if guard == "" then
-				gdt0.pos = VecAdd(gdt0.pos, Vec(0, 0, 0))
-				gdt0_2.pos = VecAdd(gdt0_2.pos, Vec(0.025, 0.025, 0))
-				guardlength = 0
-			else
-				gdt0.pos = hidePos
-				gdt0_2.pos = hidePos
-			end
-			if guard == "guard1" then
-				gdt1.pos = VecAdd(gdt1.pos, Vec(0, 0, 0))
-				gdt1_2.pos = VecAdd(gdt1_2.pos, Vec(-0.025, 0.025, 0))
-				guardlength = -0.15
-			else
-				gdt1.pos = hidePos
-				gdt1_2.pos = hidePos
-			end
-			if guard == "guard2" then
-				gdt2.pos = VecAdd(gdt2.pos, Vec(0, 0.05, 0))
-				gdt2_2.pos = VecAdd(gdt2_2.pos, Vec(-0.025, 0.025, -0.05))
-				guardlength = 0
-			else
-				gdt2.pos = hidePos
-				gdt2_2.pos = hidePos
-			end
-			if guard == "guard3" then
-				gdt3.pos = VecAdd(gdt3.pos, Vec(0, 0, 0))
-				gdt3_2.pos = VecAdd(gdt3_2.pos, Vec(-0.025, 0.025, -0.001))
-				guardlength = -0.15
-			else
-				gdt3.pos = hidePos
-				gdt3_2.pos = hidePos
-			end
-
-			SetShapeLocalTransform(bolt, bt)
-			SetShapeLocalTransform(selector, st)
-			SetShapeLocalTransform(suppressor, spt)
-			SetShapeLocalTransform(scope, sct)
-			SetShapeLocalTransform(holo, ht)
-			SetShapeLocalTransform(holo2, ht2)
-			SetShapeLocalTransform(kobra, kbt)
-			SetShapeLocalTransform(leupold, lpt)
-			SetShapeLocalTransform(leupold_2, lpt2)
-			SetShapeLocalTransform(reddot, rdt)
-			SetShapeLocalTransform(reddot2, rdt2)
-			SetShapeLocalTransform(scope3, sct3)
-			SetShapeLocalTransform(scope3_2, sct3_2)
-			SetShapeLocalTransform(g33, g33t)
-			SetShapeLocalTransform(g33_2, g33t2)
-			SetShapeLocalTransform(rail, rt)
-			SetShapeLocalTransform(rail2, rt2)
-			SetShapeLocalTransform(rail3, rt3)
-			SetShapeLocalTransform(stock0, stt0)
-			SetShapeLocalTransform(stock1, stt1)
-			SetShapeLocalTransform(stock1_2, stt1_2)
-			SetShapeLocalTransform(stock2, stt2)
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
-			SetShapeLocalTransform(guard0, gdt0)
-			SetShapeLocalTransform(guard0_2, gdt0_2)
-			SetShapeLocalTransform(guard1, gdt1)
-			SetShapeLocalTransform(guard1_2, gdt1_2)
-			SetShapeLocalTransform(guard2, gdt2)
-			SetShapeLocalTransform(guard2_2, gdt2_2)
-			SetShapeLocalTransform(guard3, gdt3)
-			SetShapeLocalTransform(guard3_2, gdt3_2)
-		end
-
-		if selectattachments then
-			clickedmag = clickedmag1 or clickedmag2 or clickedmag3
-			if clickedmag and selectattachments and not InputPressed(attachmentsKey) and not GetBool("level.optionstriggered") then
-				Reload()
-			end
-		end
-		if reloading and not clickedmag and selectattachments then
-			selectattachments = false
-			selectattachmentsTimer = 0.25
-		end
-
-		if not selectattachments then
-			if (InputPressed(reloadKey) or clickedmag) and selectfireTimer == 0 then
-				if not realistic and (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) then
-					Reload()
-					inspectTimer = 0
-				end
-			end
-
-			if (InputReleased(reloadKey) or clickedmag) and selectfireTimer == 0 then
-				if realistic and curmagslot ~= nextmagslot and magcheckTimer == 0 then
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
-				if reloadTimer < 0.7 and not cocksoundplaying and ammo == 0 then
-					cocksoundplaying = true
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.85)
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
-		local x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.8, -1.9, 0, 0, 0
-		if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.2 then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0.3, -0.6, -0.3+bt.pos[3], 0, 0, 0
-		elseif reloading then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0+mt.pos[1], 0.35+mt.pos[2], 0+mt.pos[3], 0, 0, 0
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
-		sightattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.4, -1))
-		muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.55, -2.5-barrellength))
-		stockattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.65, -0.6))
-		removestockattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.7, -0.5))
-		sideattachpoint = TransformToParentPoint(btrans, Vec(0.175, -0.65, -1.8))
-		magattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1.15))
-		gripattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1.7))
-		barrelattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.65, -1.6))
-		guardattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.55, -1.5))
-		dustcoverattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.5, -0.7))
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
-	if GetString("game.player.tool") == "ak105" and GetPlayerVehicle() == 0 then
-
-
-		------SCOPE RETICLE------
-		if toprail == "scope" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
-			local gt = GetBodyTransform(GetToolBody())
-			local sightcenter = Vec(0.275, -0.2875, -1.8)
-			local sightrear = Vec(0.275, -0.2875, -1.4)
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
-		elseif toprail == "scope2" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) and not altaim then
-			local gt = GetBodyTransform(GetToolBody())
-			local sightcenter = Vec(0.275, -0.3, -1.8)
-			local sightrear = Vec(0.275, -0.3, -1.4)
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
-				local w, h = UiGetImageSize("MOD/img/reticle6.png")
-				local x, y = UiWorldToPixel(holopoint)
-				UiTranslate(x-w/2, y-h/2)
-				UiImage("MOD/img/reticle6.png")
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
-			UiPop()
-		elseif toprail == "sight4" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
-			UiPush()
-				w, h = UiGetImageSize("MOD/img/reticle3.png")
-				UiTranslate((UiWidth()-w)/2, (UiHeight()-h)/2)
-				UiTranslate(RECroty*-100, RECrotx*-100-recoilAngle*40-recoilTimer2*400)
-				if realistic then
-					UiTranslate(-math.sin(1.3*GetTime())*6*bipodFactor^4, -math.sin(2.1*GetTime())*4*bipodFactor^4)
-				end
-				local speed =VecLength(GetPlayerVelocity())
-				if speed > 1 then
-					UiTranslate(-swayx*speed*120, -swayy*speed*80)
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
-		elseif toprail == "scope3" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
-			local gt = GetBodyTransform(GetToolBody())
-			local sightcenter = Vec(0.275, -0.25, -1.8)
-			local sightrear = Vec(0.275, -0.25, -1.1)
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
-				local w, h = UiGetImageSize("MOD/img/reticle7.png")
-				local x, y = UiWorldToPixel(holopoint)
-				UiTranslate(x-w/2, y-h/2)
-				if altaim then
-					UiImage("MOD/img/reticle3.png")
-				else
-					UiImage("MOD/img/reticle7.png")
-				end
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
-					UiText("Infinite")
-				end
-			UiPop()
-		end
-		end
-		if realistic then
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
-	if GetString("game.player.tool") == "ak105" and grenadelauncher and not selectattachments then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle")
-			UiImage("ui/hud/crosshair-launcher.png")
-		UiPop()
-	end
-	if GetString("game.player.tool") == "ak105" and sideattachment and side == "side3" then
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
-	if realistic and selectmag and GetString("game.player.tool") == "ak105" then
-		hoverindex=0
-		UiPush()
-			local x,y,dist=UiWorldToPixel(magattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					if totalmags > 0 then
-					for i = 1, totalmags do
-					clickedslot = MagButton(nextmagslot,i,true,{curx,cury},{"Ammo: ", CheckAmmo(i)},60,60)
-					UiTranslate(60,0)
-					curx,cury=curx+60,cury
-					end
-					end
-				UiPop()
-			end
-		UiPop()
-	end
-
-
-	------ATTACHMENTS MENU------
-	if not realistic or GetBool("level.optionstriggered") then
-	if selectattachments and GetString("game.player.tool") == "ak105" and GetPlayerVehicle() == 0 then
-
-	local total = 9
-	gripattachpoint2 = AttachmentGroup("attachmentgroup","grip",gripattachpoint,Description,1/total,60,60)
-	barrelattachpoint2 = AttachmentGroup("attachmentgroup","barrel",barrelattachpoint,Description,2/total,60,60)
-	muzzleattachpoint2 = AttachmentGroup("attachmentgroup","muzzle",muzzleattachpoint,Description,3/total,60,60)
-	if guard ~= "" and guard ~= "guard3" then
-	sideattachpoint2 = AttachmentGroup("attachmentgroup","side",sideattachpoint,Description,4/total,60,60)
-	else
-		SetString("savegame.mod.side", "")
-	end
-	guardattachpoint2 = AttachmentGroup("attachmentgroup","guard",guardattachpoint,Description,5/total,60,60)
-	sightattachpoint2 = AttachmentGroup("attachmentgroup","toprail",sightattachpoint,Description,6/total,60,60)
-	dustcoverattachpoint2 = AttachmentGroup("attachmentgroup","dustcover",dustcoverattachpoint,Description,7/total,60,60)
-	stockattachpoint2 = AttachmentGroup("attachmentgroup","stock",stockattachpoint,Description,8/total,60,60)
-	if not realistic then
-	magattachpoint2 = AttachmentGroup("attachmentgroup","mag",magattachpoint,Description,9/total,60,60)
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
-					if dustcover ~= "" then
-						clickedscope = AttachmentButton("toprail","sight3",true,{curx,cury},{"Red Dot","1x magnification sight for close range combat."})
-						UiTranslate(-70,0)
-						curx,cury=curx-70,cury
-						clickedholo = AttachmentButton("toprail","holo",true,{curx,cury},{"Holographic Sight","1x magnification sight for close range combat."})
-						UiTranslate(70,70)
-						curx,cury=curx+70,cury+70
-						clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
-						UiTranslate(-70,0)
-						curx,cury=curx-70,cury
-						clickedholo = AttachmentButton("toprail","scope2",true,{curx,cury},{"Leupold Scope with Delta Sight","3x magnification scope with a 1x delta sight on top for close range combat."})
-						UiTranslate(-70,0)
-						curx,cury=curx-70,cury
-						clickedholo = AttachmentButton("toprail","scope3",true,{curx,cury},{"Eotech Vudu Scope","1x / 6x magnification scope."})
-						UiTranslate(-100,0)
-						curx,cury=curx-70,cury
-						--clickedholo = AttachmentButton("toprail","sight4",true,{curx,cury},{"Precision Scope","8x magnification sight for long range combat."})
-						UiTranslate(-100,0)
-						curx,cury=curx-70,cury
-						--clickedholo = AttachmentButton("toprail","scope4",true,{curx,cury},{"FLIR Scope","1x / 6x magnification sight with infrared sensor that detects heat signatures."})
-						UiTranslate(340,70)
-						curx,cury=curx+340,cury+70
-						clickedholo = AttachmentButton("canted","sight5",true,{curx,cury},{"Cented Delta Sight","1x magnification canted sight for close range combat."})
-						UiTranslate(-70,0)
-						curx,cury=curx-70,cury
-						if toprail == "holo" then
-							clickedmagnifier1 = AttachmentButton("magnifier","g33",true,{curx,cury},{"Thermal Magnifier","Foldable 3x magnifier for close range optics that shows heat signatures. Press 'Z' to fold/unfold."})
-						end
-					else
-						clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
-						UiTranslate(-70,0)
-						curx,cury=curx-70,cury
-						clickedscope = AttachmentButton("toprail","kobra",true,{curx,cury},{"Red Dot Sight","1x magnification sight for close range combat."})
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
-					clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Muzzle Break","Reduces recoil, but turns your barrel into a flashbang."})
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
-					if guard == "guard1" or guard == "guard2" then
-					clickedside1 = AttachmentButton("side","side1",true,{curx,cury},{"Laser","A laser that points where you shoot."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedside2 = AttachmentButton("side","side2",true,{curx,cury},{"Flashlight","Lights up the area in front of you."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedside3 = AttachmentButton("side","side3",true,{curx,cury},{"Rangefinder","Displays the range to your target."})
-					UiTranslate(-70,0)
-					end
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
-					clickedmag1 = AttachmentButton("mag","mag1",true,{curx,cury},{"45rnd Mag","Pew Pew Pew"})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmag2 = AttachmentButton("mag","mag2",true,{curx,cury},{"77rnd Drum","Pew Pew Pew Pew Pew Pew"})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmag3 = AttachmentButton("mag","mag3",true,{curx,cury},{"95rnd Double Drum","Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew"})
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
-					if guard ~= "" then
-					clickedgrip1 = AttachmentButton("grip","grip1",true,{curx,cury},{"Vertical Grip","Decreased vertical recoil."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedgrip2 = AttachmentButton("grip","grip2",true,{curx,cury},{"Angled Grip","Decreased horizontal recoil."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					end
-					if not (guard == "guard2" and barrel == "") then
-					clickedgrip3 = AttachmentButton("grip","grip3",true,{curx,cury},{"Bipod","Increased accuracy while crouching or resting the gun on a ledge."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					end
-					if guard == "" then
-					clickedgrip4 = AttachmentButton("grip","grenade_launcher",true,{curx,cury},{"GP-25","Grenade launcher for increased collateral damage."})
-					end
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
-					clickedbarrel1 = AttachmentButton("barrel","barrel1",true,{curx,cury},{"AK-74 Barrel","Increased accuracy but more vertical recoil."})
-					UiTranslate(-100,0)
-					curx,cury=curx-100,cury
-					clickedbarrel2 = AttachmentButton("barrel","barrel2",true,{curx,cury},{"RPK-74 Barrel","Increased accuracy and damage but more vertical recoil."})
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
-					clickedguard1 = AttachmentButton("guard","guard1",true,{curx,cury},{"Modernised Handguard","Allows for attachments such as grips and lasers."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedguard2 = AttachmentButton("guard","guard3",true,{curx,cury},{"Modernised Handguard","Allows for attachments such as grips and lasers."})
-					UiTranslate(-100,0)
-					curx,cury=curx-100,cury
-					clickedguard2 = AttachmentButton("guard","guard2",true,{curx,cury},{"Modernised Handguard","Allows for attachments such as grips and lasers."})
-				UiPop()
-			end
-		UiPop()
-		UiPush()
-			local x,y,dist=UiWorldToPixel(dustcoverattachpoint2)
-			if GetString("savegame.mod.attachmentgroup") == "dustcover" and dist > 0 then
-				UiTranslate(x,y+70)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
-					clickedmoderncover = AttachmentButton("dustcover","cover2",true,{curx,cury},{"Modernised Dust Cover","Allows for attachments of optics."})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					--clickedcoverremoved = AttachmentButton("dustcover","cover3",true,{curx,cury},{"Remove Dust Cover","Removes dust cover for that scav look."})
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
-					clickedstock1 = AttachmentButton("stock","stock1",true,{curx,cury},{"Sidefolder","Side folding light metal stock."})
-					UiTranslate(70,0)
-					curx,cury=curx+70,cury
-					clickedstock2 = AttachmentButton("stock","stock2",true,{curx,cury},{"Light Stock","Light stock."})
-					UiTranslate(70,0)
-					curx,cury=curx+70,cury
-					clickedstock3 = AttachmentButton("stock","removed",true,{curx,cury},{"Remove Stock","Removes stock entirely."})
-				UiPop()
-			end
-		UiPop()
-	end
-	end
-	if selectattachments and GetString("game.player.tool") == "ak105" and GetPlayerVehicle() == 0 or GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
-	hoverindex=0
-	UiPush()
-		local x,y,dist=UiWorldToPixel(removestockattachpoint)
-			if GetString("savegame.mod.attachmentgroup") and dist > 0 then
-				UiTranslate(x,y)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-				UiAlign("center middle")
-				if not InputDown("shift") and mag ~= "mag2" and mag ~= "mag3" and toprail ~= "scope" and toprail ~= "kobra" then
-					clickedstockremoved = AttachmentButton("removestock","removed",true,{curx,cury},{"Fold Stock","Folds stock for a smaller profile weapon."})
-				end
-			UiPop()
-		end
-	UiPop()
-	end
-	if hint and (selectattachments or InputDown(reloadKey) and heldrTimer > 0.2) then drawHint(info) end
-
-
-	------OPTIONS UI------
-	if GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
-	UiPush()
-		UiAlign("center middle")
-		UiTranslate(UiCenter(), 70)
-		UiFont("bold.ttf", 60)
-		UiText("WEAPON MODDING")
-	UiPop()
-	end
-	
-	if GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
-
-	UiAlign("center middle")
-	UiTranslate(300, 250)
-	UiFont("bold.ttf", 48)
-	local ammotext = "5"
-	if ammotype == "556" then
-		ammotext = "2"
-	elseif ammotype == "762" then
-		ammotext = "4"
-	end
-	UiText("AK-10"..ammotext)
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
-	UiTranslate(0, 100)
-	UiPush()
-		local curx,cury=120,635
-		UiAlign("center middle")
-		UiTranslate(100, 0)
-		curx,cury=curx+100,cury
-		clickedammo1 = AttachmentButton("ammotype","545",true,{curx,cury},{"5.45x39","Smaller, higher velocity round that does less damage to target."})
-		UiTranslate(-100,0)
-		curx,cury=curx-100,cury
-		clickedammo2 = AttachmentButton("ammotype","762",true,{curx,cury},{"7.62x39","Larger, lower velocity round that does more damage to target."})
-		UiTranslate(-100,0)
-		curx,cury=curx-100,cury
-		clickedammo3 = AttachmentButton("ammotype","556",true,{curx,cury},{"7.62x51","Larger, higher velocity round that does more damage to target."})
-	UiPop()
-	if GetString("savegame.mod.ammotype") == "" then
-		SetString("savegame.mod.ammotype", "545")
-	end
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
-
-	if not realistic then
-		UiTranslate(0, 240)
-	end
-
-	UiPush()
-		UiTranslate(800+optionsx*100, -80)
-		UiFont("bold.ttf", 26)
-		UiTranslate(-120, 70)
-		UiText("Horizontal Recoil: "..round(recoilHorizontal*stockFactor*laserFactor*muzzleFactor*gripfactorx*barrelFactorx*ammoFactory, 2))
-		UiTranslate(260, 0)
-		UiText("Vertical Recoil: "..round(recoilFactor*muzzleFactor*gripfactory*barrelFactory*ammoFactory, 2))
-		UiTranslate(200, 0)
-		UiText("Accuracy: "..round(1/accuracyFactor, 2))
-	UiPop()
-
-	UiPush()
-		UiTranslate(-200, 50)
-		UiPush()
-			UiAlign("center middle")
-			KeybindButton("Reload")
-			UiTranslate(124, 0)
-			KeybindButton("Check-Mag")
-			UiTranslate(140, 0)
-			KeybindButton("Fire-Mode")
-			UiTranslate(132, 0)
-			KeybindButton("Lean-Left")
-			UiTranslate(132, 0)
-			KeybindButton("Lean-Right")
-			UiTranslate(152, 0)
-			KeybindButton("Attachments")
-			UiTranslate(132, 0)
-			KeybindButton("Melee")
-			UiTranslate(148, 0)
-			KeybindButton("Side-Attachment")
-			UiTranslate(204, 0)
-			KeybindButton("Grenade-Launcher")
-			UiTranslate(204, 0)
-			KeybindButton("Inspect-Weapon")
-			UiTranslate(164, 0)
-			KeybindButton("Clear-Jam")
-		UiPop()
-	UiPop()
-	end
 end
 
 function optionsSlider(current, min, max, incri)
@@ -3843,4 +1163,2647 @@
     return math.floor(number * power) / power
 end
 
-function math.clamp(n, low, high) return math.min(math.max(n, low), high) end+function math.clamp(n, low, high) return math.min(math.max(n, low), high) end
+
+function server.init()
+    ammotype = GetString("savegame.mod.ammotype")
+    local ammotext = "5"
+    if ammotype == "556" then
+    	ammotext = "2"
+    elseif ammotype == "762" then
+    	ammotext = "4"
+    end
+    RegisterTool("ak105", "AK-10"..ammotext, "MOD/vox/ak105.vox", 3)
+    SetBool("game.tool.ak105.enabled", true, true)
+    SetFloat("game.tool.ak105.ammo", 101, true)
+    ------INITIALISE OPTIONS MENU------
+    damageoption = GetInt("savegame.mod.damage")
+    if damageoption < 50 then
+    	damageoption = 100
+    	SetInt("savegame.mod.damage", 100, true)
+    end
+    slots = {}
+    for i = 1,8 do
+    	slots[i] = {}
+    	for j = 1,2 do
+    		slots[i][j] = {"", {0, 0}, 1, 1}
+    	end
+    end
+    grabbed = {{"", {0, 0}, 1, 1}, 0, 0}
+    magtable = {}
+    totalmags = GetInt("savegame.mod.totalmags")
+    magplace = 1
+    magplaceslot = 1
+    for i = 1,#slots do
+    	for j = 1,#slots[i] do
+    		if slots[i][j][2][1] == 0 and magplace < totalmags+1 then
+    			local w, h = 1, 1
+    			local mag = GetString("savegame.mod.mslot"..magplace)
+    			if mag == "mag0" then
+    				w, h = 1, 2
+    			elseif mag == "mag1" then
+    				w, h = 1, 2
+    			elseif mag == "mag2" then
+    				w, h = 2, 2
+    			elseif mag == "mag3" then
+    				w, h = 3, 2
+    			else
+    				w, h = 1, 2
+    			end
+    			placeItem({{mag, {0, 0}, w, h}, 0, 0}, magplaceslot, 2)
+    			magplace = magplace + 1
+    			magplaceslot = magplaceslot + w
+    		else
+    		end
+    	end
+    end
+    local keybinds = {{"Reload","r"},{"Check-Mag","h"},{"Fire-Mode","v"},{"Lean-Left","q"},{"Lean-Right","e"},{"Attachments","t"},{"Melee","x"},{"Side-Attachment","b"},{"Grenade-Launcher","c"},{"Inspect-Weapon","y"},{"Clear-Jam","r"}}
+    for i = 1,#keybinds do
+    	if GetString("savegame.mod."..keybinds[i][1]) == "" then
+    		SetString("savegame.mod."..keybinds[i][1], keybinds[i][2], true)
+    	end
+    end
+    reloadKey,magcheckKey,selectfireKey,leanleftKey,leanrightKey,attachmentsKey,meleeKey,sideKey,grenadeKey,inspectKey,clearjamKey=GetString("savegame.mod.Reload"),GetString("savegame.mod.Check-Mag"),GetString("savegame.mod.Fire-Mode"),GetString("savegame.mod.Lean-Left"),GetString("savegame.mod.Lean-Right"),GetString("savegame.mod.Attachments"),GetString("savegame.mod.Melee"),GetString("savegame.mod.Side-Attachment"),GetString("savegame.mod.Grenade-Launcher"),GetString("savegame.mod.Inspect-Weapon"),GetString("savegame.mod.Clear-Jam")
+    ------INITIALISE WEAPON FUNCTIONS------
+    damage = 0.125 * GetInt("savegame.mod.damage")/100
+    if damage == 0 then
+    	damage = 0.125
+    end
+    gravity = Vec(0, -10, 0)
+    hidePos = Vec(0, -200, 0)
+    hideTrans = Transform(hidePos,QuatEuler())
+    velocity = 850
+    drag = 1.5
+    maxMomentum = 2.5
+    tracer = false
+    recoilVertical = 0.8
+    recoilHorizontal = 6
+    recoilWander = 7
+    --armor pen
+    if ammotype == "545" then
+    lvl5armor = 0.05
+    lvl4armor = 0.2
+    lvl3armor = 0.5
+    lvl2armor = 0.9
+    lvl1armor = 1
+    elseif ammotype == "762" then
+    lvl5armor = 0
+    lvl4armor = 0.15
+    lvl3armor = 0.45
+    lvl2armor = 0.7
+    lvl1armor = 1
+    else
+    lvl5armor = 0.1
+    lvl4armor = 0.3
+    lvl3armor = 0.6
+    lvl2armor = 0.9
+    lvl1armor = 1
+    end
+    inside = {}
+    for i = 1,50 do
+    	inside[i] = {0,0,0,0}
+    end
+    hoverindex = 0
+    --magazine and attachments system
+    toprail = GetString("savegame.mod.toprail")
+    canted = GetString("savegame.mod.canted")
+    muzzle = GetString("savegame.mod.muzzle")
+    stock = GetString("savegame.mod.stock")
+    removestock = GetString("savegame.mod.removestock")
+    realistic = GetBool("savegame.mod.realistic")
+    --magazine system
+    mslot1 = GetString("savegame.mod.mslot1")
+    mslot2 = GetString("savegame.mod.mslot2")
+    mslot3 = GetString("savegame.mod.mslot3")
+    mslot4 = GetString("savegame.mod.mslot4")
+    mslot5 = GetString("savegame.mod.mslot5")
+    mslot6 = GetString("savegame.mod.mslot6")
+    mslot7 = GetString("savegame.mod.mslot7")
+    mslot8 = GetString("savegame.mod.mslot8")
+    if totalmags == 0 then
+    	mslot1, mslot2 = "mag0", "mag0"
+    	SetString("savegame.mod.mslot1", "mag0", true)
+    	SetString("savegame.mod.mslot2", "mag0", true)
+    totalmags = 2
+    end
+    magtable2 = {{mslot1,0,0},{mslot2,0,0},{mslot3,0,0},{mslot4,0,0},{mslot5,0,0},{mslot6,0,0},{mslot7,0,0},{mslot8,0,0}}
+    for i=1,8 do
+    	local magslottype = GetString("savegame.mod.mslot"..i)
+    	if magslottype == "mag0" then
+    		magtable2[i][2] = 30
+    		magtable2[i][3] = 30
+    	elseif magslottype == "mag1" then
+    		magtable2[i][2] = 45
+    		magtable2[i][3] = 45
+    	elseif magslottype == "mag2" then
+    		magtable2[i][2] = 77
+    		magtable2[i][3] = 77
+    	elseif magslottype == "mag3" then
+    		magtable2[i][2] = 95
+    		magtable2[i][3] = 95
+    	end
+    end
+    curmagslot = 1
+    nextmagslot = 1
+    if realistic then
+    	mag = mslot1
+    	reloadFactor = 1
+    else
+    	mag = GetString("savegame.mod.mag")
+    	reloadFactor = 1
+    end
+    grip = GetString("savegame.mod.grip")
+    barrel = GetString("savegame.mod.barrel")
+    side = GetString("savegame.mod.side")
+    guard = GetString("savegame.mod.guard")
+    magnifier = GetString("savegame.mod.magnifier")
+    magnified = false
+    magnifierFactor = 1
+    dustcover = GetString("savegame.mod.dustcover")
+    reloadTime = 2.4
+    shotDelay = 0.09
+    spreadTimer = 1.25
+    spreadFactor = 1.5
+    accuracyFactor = 1
+    bipodFactor = 1
+    laserFactor = 1
+    if not realistic then
+    	if mag == "" then
+    		magsize = 30
+    		reloadFactor = 1.2
+    	elseif mag == "mag1" then
+    		magsize = 45
+    		reloadFactor = 1.4
+    	elseif mag == "mag2" then
+    		magsize = 77
+    		reloadFactor = 1.55
+    	else
+    		magsize = 95
+    		reloadFactor = 1.7
+    	end
+    	ammo = magsize
+    else
+    	ammo = magtable2[curmagslot][2]
+    end
+    barrellength = 0
+    barrelFactorx = 0.8
+    barrelFactory = 1
+    barrelFactordamage = 1.25
+    ammoFactory = 1
+    ammoFactordamage = 1
+    ammoFactorvelocity = 1
+    grenadelauncherammo = 1
+    mags = 2
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
+    for i=1, 100 do
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
+    lightFactor = 1
+    recoilMax = 0
+    rnd1, rnd2, rnd3, rnd4, rnd5, rnd6 = 0, 0, 0, 0, 0, 0
+    lightTimer = 0
+    clickedmag = false
+    animationTimers = {0, 0, 0, 0, 0}
+    fovTimer = 0
+    animation1Timer = 0
+    optionsrotx = -50
+    optionsroty = 0
+    optionszoom = 0
+    optionsx = 0
+    magoutTimer = 0
+    maginTimer = 0
+    meleeTimer = 0
+    magcheckTimer = 0
+    selecttextTimer = 0
+    cocksoundplaying = false
+    reloadsound2playing = true
+    selectsoundplaying = false
+    selectattachments = false
+    selectmag = false
+    jammed = false
+    jamclearTimer = 0
+    selectattachmentsTimer = 0
+    inspectTimer = 0
+    heldrTimer = 0
+    scopeTimer = 0
+    e = false
+    q = false
+    altaim = false
+    switchsights = false
+    selectfire = 1
+    selectfire0 = 0
+    selectfireTimer = 0
+    selectfireText = "Full"
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
+    interactsound3 = LoadSound("MOD/snd/interact3.ogg")
+    uiselect = LoadSound("MOD/snd/uiselect.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "ak105" and GetPlayerVehicle(playerId) == 0 then
+    	SetBool("hud.aimdot", false, true)
+
+    	------CONTROLS------
+    	if InputDown("lmb") and not reloading and selectfire == 1 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    		end
+    	elseif InputPressed("lmb") and not reloading and selectfire == 2 and not selectattachments and not selectmag and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
+    		if grenadelauncherammo > 0 and grenadelauncher then
+    			ShootGrenade()
+    		elseif not grenadelauncher and ammo ~= 0 then
+    			Shoot()
+    			shootTimer = 0.11
+    		end
+    	end
+
+    	if InputPressed("lmb") and not reloading and not InputDown("shift") and inspectTimer <= 0 and magcheckTimer == 0 and jamclearTimer == 0 then
+    		spreadTimer = 1.25
+    		if (ammo == 0 or selectfire == 0 or jammed) and not selectattachments and not selectmag then
+    			PlaySound(dryfiresound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+    	end
+
+    	if InputReleased("lmb") and not reloading and selectfire ~= 0 then
+    		shootTimer = 0
+    	end
+
+    	if InputDown("rmb") and selectfire > 0 and selectfireTimer == 0 and not selectattachments and not selectmag and GetPlayerGrabShape(playerId) == 0 and magcheckTimer == 0 and jamclearTimer == 0 and magcheckTimer == 0 and jamclearTimer == 0 then
+    		if InputPressed("rmb") then
+    			PlaySound(interactsound1, GetPlayerTransform(playerId).pos, 1)
+    		end
+    		ironsight = true
+    		inspectTimer = 0
+    		if scopeTimer < 0.5 and not reloading and not (q or e) and selectfireTimer == 0 then
+    			scopeTimer = scopeTimer + dt
+    		end
+    	end
+    	if not InputDown("rmb") then
+    		ironsight = false
+    	end
+    	if selectfire == 0 and selectfireTimer <= 0 then
+    		ironsight = false
+    	end
+    	if (not InputDown("rmb") or reloading or q or e or selectfireTimer > 0) and scopeTimer ~= 0 then scopeTimer = scopeTimer - dt end
+
+    	if InputPressed(leanrightKey) then
+    		e = not e
+    		q = false
+    	end
+
+    	if InputPressed(leanleftKey) then
+    		q = not q
+    		e = false
+    	end
+
+    	if InputDown("alt") and InputPressed("rmb") or InputDown("rmb") and InputPressed("alt") then
+    		altaim = not altaim
+    		if toprail == "scope3" or toprail == "scope4" then
+    			PlaySound(selectsound, GetPlayerTransform(playerId).pos, 0.85)
+    		end
+    	end
+    	if toprail ~= "scope2" and toprail ~= "scope3" and toprail ~= "scope4" then
+    		altaim = false
+    	end
+    	if InputPressed("c") then
+    		switchsights = not switchsights
+    	end
+    	if canted == "" then
+    		switchsights = false
+    	end
+
+    	if InputPressed(meleeKey) and not reloading and not ironsight and shootTimer <= 0 and selectfire > 0 and stock ~= "removed" and not InputDown("shift") and not selectattachments then
+    		meleeTimer = 0.8
+    	end
+
+    	if InputPressed(selectfireKey) and not reloading and not selectattachments and not selectmag and magcheckTimer == 0 and jamclearTimer == 0 then
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
+    	if InputDown(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 or GetBool("level.optionstriggered") then
+    		if InputPressed(attachmentsKey) and not GetBool("level.optionstriggered") then
+    			PlaySound(interactsound2, GetPlayerTransform(playerId).pos, 1)
+    			selectattachmentsTimer = 0.5
+    		end
+    		UiMakeInteractive()
+    		selectattachments = true
+    		ironsight = false
+    		inspectTimer = 0
+    	end
+    	if InputReleased(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") then
+    		selectattachments = false
+    		selectattachmentsTimer = 0.25
+    	end
+
+    	if InputPressed(sideKey) and side ~= "" then
+    		sideattachment = not sideattachment
+    		PlaySound(uiselect, GetPlayerTransform(playerId).pos, 0.75)
+    	end
+    	Laser(sideattachment and side == "side1")
+    	Flashlight(sideattachment and side == "side2")
+    	Rangefinder(sideattachment and side == "side3")
+
+    	if InputPressed(magcheckKey) and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 then
+    		magcheckTimer = 3
+    		PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.6)
+    		inspectTimer = 0
+    	end
+    	if magcheckTimer ~= 0 then
+    		magcheckTimer = magcheckTimer - dt
+    		ironsight = false
+    	end
+    	if magcheckTimer < 0 then
+    		magcheckTimer = 0
+    		reloadsound2playing = false
+    	end
+
+    	if InputDown(reloadKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then heldrTimer = heldrTimer + dt end
+    	if InputDown(reloadKey) and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and not jammed and jamclearTimer == 0 and heldrTimer > 0.2 then
+    		UiMakeInteractive()
+    		selectmag = true
+    		ironsight = false
+    	else
+    		selectmag = false
+    	end
+    	if InputReleased(reloadKey) and heldrTimer <= 0.2 and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and magcheckTimer == 0 and not jammed and jamclearTimer == 0 then
+    		if totalmags ~= 0 then
+    		for i = 1, totalmags do
+    			if magtable2[i][2] > magtable2[nextmagslot][2] and i ~= curmagslot then
+    				nextmagslot = i
+    			end
+    		end
+    		end
+    		inspectTimer = 0
+    		Reload()
+    	end
+    	if InputReleased(reloadKey) then heldrTimer = 0 end
+
+    	if InputPressed(clearjamKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jammed and jamclearTimer == 0 then
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
+
+    	if InputDown("shift") then
+    		ironsight = false
+    		selectattachments = false
+    		inspectTimer = 0
+    	end
+
+    	if grip == "grenade_launcher" then
+    		if InputPressed(grenadeKey) and not reloading then
+    			grenadelauncher = not grenadelauncher
+    		end
+    	else
+    		grenadelauncher = false
+    	end
+
+    	if InputPressed(inspectKey) and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire > 0 and not selectattachments and magcheckTimer == 0 and jamclearTimer == 0 then
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
+    	------WEAPON FUNCTIONS AND ANIMATIONS------
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
+    		recoilFactor = recoilVertical*stockFactor*ammoFactory
+    	else
+    		recoilFactor = recoilVertical*stockFactor*ammoFactory*1.75
+    	end
+
+    	if ironsight then
+    		recoilMax = 10*muzzleFactor*gripfactory*barrelFactory
+    	else
+    		recoilMax = 20*muzzleFactor*gripfactory*barrelFactory
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
+    	removestock = GetString("savegame.mod.removestock")
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
+    	dustcover = GetString("savegame.mod.dustcover")
+    	ammotype = GetString("savegame.mod.ammotype")
+    	if ammotype == "" then
+    		SetString("savegame.mod.ammotype", "545", true)
+    		maxMomentum = 2.5
+    		ammoFactory = 1
+    		ammoFactordamage = 1
+    		ammoFactorvelocity = 1
+    	elseif ammotype == "762" then
+    		maxMomentum = 3
+    		ammoFactory = 1.25
+    		ammoFactordamage = 1.1
+    		ammoFactorvelocity = 0.85
+    	elseif ammotype == "556" then
+    		maxMomentum = 3
+    		ammoFactory = 1.2
+    		ammoFactordamage = 1.2
+    		ammoFactorvelocity = 1.2
+    	else
+    		maxMomentum = 2.5
+    		ammoFactory = 1
+    		ammoFactordamage = 1
+    		ammoFactorvelocity = 1
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
+    		local adsFOV, adsTime = 0, 0
+    		local defaultTrans = Transform(Vec(0.25, 0.15, 0.25), QuatEuler(0, 0, 0))
+
+    		x,y,z,rotx,roty,rotz = -0.1,0.2,0,0,0,0
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
+    				y = 0.3075
+    				z = 0.2
+    				rotz = 0
+    			elseif toprail == "kobra" then
+    				x = 0.275
+    				y = 0.35
+    				z = 0.2
+    				rotz = 0
+    			elseif toprail == "sight3" then
+    				x = 0.275
+    				y = 0.2625
+    				z = 0.2
+    				rotz = 0
+    			elseif toprail == "" then
+    				x = 0.275
+    				y = 0.39
+    				z = 0.2
+    				rotz = 0
+    			elseif toprail == "scope" then
+    				x = 0.275
+    				y = 0.3
+    				z = 0.2
+    				rotz = 0
+    			elseif toprail == "scope3" then
+    				x = 0.275
+    				y = 0.25
+    				z = 0.2
+    				rotz = 0.1
+    			elseif toprail == "scope2" then
+    				if altaim then
+    					x = 0.275
+    					y = 0.1625
+    					z = 0.2
+    				else
+    					x = 0.275
+    					y = 0.3
+    					z = 0.2
+    				end
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
+    			elseif toprail == "scope2" then
+    				if altaim then
+    					adsFOV, adsTime = 10, 0.15
+    				else
+    					adsFOV, adsTime = 80, 0.25
+    				end
+    			elseif toprail == "holo" then
+    				adsFOV, adsTime = 20, 0.1
+    			elseif toprail == "kobra" then
+    				adsFOV, adsTime = 10, 0.1
+    			elseif toprail == "sight3" then
+    				adsFOV, adsTime = 10, 0.1
+    			elseif toprail == "scope3" then
+    				if altaim then
+    					adsFOV = 80
+    				else
+    					adsFOV = 10
+    				end
+    				if ironsight and scopeTimer >= 0.5 then
+    					adsTime = 0
+    				else
+    					adsTime = 0.15
+    				end
+    			end
+    		elseif grenadelauncher then
+    			adsFOV, adsTime = 10, 0.15
+    		else
+    			adsFOV, adsTime = 0, 0.15
+    		end
+    		end
+
+    		--offset = ADS(ironsight, adsFOV, adsTime, -x, y, z, rotz)
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
+    				local sightcenter = Vec(0.275, -0.3, -1)
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
+    					reticle1 = LoadSprite("MOD/img/reticle1.png")
+    					DrawSprite(reticle1, holotrans, 0.025, 0.025, 1, 1, 1, 1, true)
+    				end
+    			end
+    			if toprail == "scope2" and altaim then
+    				local gt = GetBodyTransform(GetToolBody())
+    				local sightcenter = Vec(0.275, -0.1625, -1.2)
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
+    					reticle4 = LoadSprite("MOD/img/reticle5.png")
+    					DrawSprite(reticle4, holotrans, 0.2, 0.15, 1, 1, 1, 1, true)
+    				end
+    			end
+    			if toprail == "kobra" then
+    				local gt = GetBodyTransform(GetToolBody())
+    				local sightcenter = Vec(0.275, -0.35, -1)
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
+    				if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.05 then
+    					reticle4 = LoadSprite("MOD/img/reticle4_ak.png")
+    					DrawSprite(reticle4, holotrans, 0.1, 0.1, 1, 1, 1, 1, true)
+    				end
+    			end
+    			if toprail == "sight3" then
+    				local gt = GetBodyTransform(GetToolBody())
+    				local sightcenter = Vec(0.275, -0.2625, -1)
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
+    				if VecLength(VecSub(TransformToParentPoint(gt, sightcenter), holopoint)) < 0.05 then
+    					reticle4 = LoadSprite("MOD/img/reticle4.png")
+    					DrawSprite(reticle4, holotrans, 0.1, 0.1, 1, 1, 1, 1, true)
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
+    			recoilTimer2 = recoilTimer2 - (recoilTimer2*0.1+dt)
+    			offset.pos = VecAdd(offset.pos, Vec(0, 0, recoilTimer2/8))
+    			offset.rot = QuatRotateQuat(offset.rot, QuatEuler((recoilTimer2)*3, 0, 0))
+    		end
+    		if recoilTimer ~= 0 then
+    			recoilTimer = recoilTimer - dt
+    			boltoffset = Vec(-0.001, -0.001, recoilTimer*3.5)
+    		end
+    		if recoilTimer < 0 then
+    			recoilTimer = 0
+    		end
+    		if recoilTimer2 < 0 then
+    			recoilTimer2 = 0
+    		end
+    		local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/400, (recoilAngle/-150)-(rnd1+rnd4)/400-recoilTimer2/8, recoilAngle/75+(rnd3+rnd6)/200+recoilTimer2/1.5+recoilTimer2/32, (recoilTimer2)*3+recoilAngle+(rnd1+rnd4)/4+(recoilTimer2-0.02)*2, (rnd2+rnd5)/4, (rnd3+rnd6)/4
+    		-- RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
+    		-- offset.pos = VecAdd(offset.pos, RECoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, RECoffset.rot)
+
+    		if jammed and jamclearTimer < 1 and jamclearTimer > 0.7 then
+    			boltoffset = Vec(-0.001, -0.001, 1-jamclearTimer)
+    			if not cocksoundplaying then
+    				cocksoundplaying = true
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.85)
+    			end
+    		end
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
+    			PlaySound(interactsound3, GetPlayerTransform(playerId).pos, 0.5, false)
+    		end
+    		if maginTimer < 0.4 and not reloadsound2playing and not grenadelauncher then
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
+    		if magcheckTimer > 2.7 then
+    			magoffset = Vec(0, 0, -(3-magcheckTimer)*1.5)
+    		elseif magcheckTimer > 2.4 and magcheckTimer < 3.7 then
+    			magoffset = Vec(0, -(2.7-magcheckTimer), -0.45)
+    		elseif magcheckTimer > 1.8 then
+    			magoffset = Vec(-(2.4-magcheckTimer)*0.5, (2.4-magcheckTimer)/2-0.3, -0.45)
+    		elseif magcheckTimer > 0.7 then
+    			magoffset = Vec(-0.3, 0, -0.45)
+    			if not reloadsound2playing then
+    				PlaySound(reloadsound2, GetPlayerTransform(playerId).pos, 0.6)
+    				reloadsound2playing = true
+    			end
+    		elseif magcheckTimer > 0.4 then
+    			magoffset = Vec(-magcheckTimer+0.4, magcheckTimer-0.7, -0.45)
+    		elseif magcheckTimer > 0.2 then
+    			magoffset = Vec(0, -magcheckTimer*2/3, -(magcheckTimer)*2.25/2)
+    		elseif magcheckTimer ~= 0 then
+    			magoffset = Vec(0, 0, -(magcheckTimer)*2.25/2)
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
+    				elseif magoutTimer > 0 or magcheckTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 0, -10
+    				elseif maginTimer > 0 or reloadTimer > 0.8 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.2, 0, -5, 10, -5
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.25, 0.25, -0.2, -10, 5, -40
+    				end
+    			elseif e then
+    				if magoutTimer > 0 or magcheckTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, -0.1, 0, 5, -10, -10
+    				elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, -0.1, -5, 15, 0
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = -1, -1.3, -0.4, 50, -50, 80
+    				end
+    			else
+    				if magoutTimer > 0 or magcheckTimer ~= 0 then
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
+    			if magoutTimer > 0 or magcheckTimer ~= 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.15, -0.05, 0, 5, -5, -20
+    			elseif maginTimer > 0 or (reloadTimer > 0.6 and ammo > 0) then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.35, -0.05, 0.1, 10, 10, -25
+    			elseif reloadTimer < 0.8 and ammo == 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = -0.8, -0.9, -0.4, 40, -40, 55
+    			end
+    		end
+    		end
+
+    		-- RELoffset = REL(reloading or magcheckTimer > 0, x1, y1, z1, rotx1, roty1, rotz1)
+    		-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
+
+    		if reloadTimer < 0.5 and reloadTimer > 0.2 and reloading and ammo == 0 then
+    			boltoffset = Vec(-0.001, -0.001, (0.5-reloadTimer)*0.75)
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
+    			x2, y2, z2, rotx2, roty2, rotz2 = -0.75, -0.5, 0, 10, 0, 50
+    		elseif jamclearTimer ~= 0 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = -0.75, -0.5, 0, 10, 0, 50
+    		end
+
+    		-- INSoffset = INS(inspectTimer > 0 or jamclearTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
+    		-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
+
+    		local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		if (selectfire == 0 or InputDown("shift")) and selectfireTimer <= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = 0.4, 0.2, -0.2, -20, 60, 0
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
+    		for i = 55, 66 do
+    			SetShapeLocalTransform(bs[i], hideTrans)
+    		end
+    		if clothingtype == "camo" then
+    			hand1 = bs[58]
+    			arm1 = bs[60]
+    			hand2 = bs[59]
+    		elseif clothingtype == "swat" then
+    			hand1 = bs[61]
+    			arm1 = bs[63]
+    			hand2 = bs[62]
+    		elseif clothingtype == "camo2" then
+    			hand1 = bs[64]
+    			arm1 = bs[66]
+    			hand2 = bs[65]
+    		else
+    			hand1 = bs[55]
+    			arm1 = bs[57]
+    			hand2 = bs[56]
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
+    			mag0_762 = shapes[30]
+    			mag0_556 = shapes[32]
+    			bolt = shapes[3]
+    			selector = shapes[4]
+    			suppressor = shapes[5]
+    			scope = shapes[6]
+    			holo = shapes[7]
+    			holo2 = shapes[8]
+    			kobra = shapes[67]
+    			leupold = shapes[46]
+    			leupold_2 = shapes[47]
+    			reddot = shapes[50]
+    			reddot2 = shapes[51]
+    			rail = shapes[9]
+    			rail2 = shapes[42]
+    			rail3 = shapes[43]
+    			stock0 = shapes[10]
+    			muzzlebreak = shapes[11]
+    			muzzlebreak2 = shapes[12]
+    			mag1 = shapes[13]
+    			mag1_762 = shapes[31]
+    			mag1_556 = shapes[33]
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
+    			guard0 = shapes[34]
+    			guard0_2 = shapes[35]
+    			guard2 = shapes[36]
+    			guard2_2 = shapes[37]
+    			guard1 = shapes[38]
+    			guard1_2 = shapes[39]
+    			guard3 = shapes[40]
+    			guard3_2 = shapes[41]
+    			stock1 = shapes[44]
+    			stock1_2 = shapes[45]
+    			stock2 = shapes[54]
+    			scope3 = shapes[52]
+    			scope3_2 = shapes[53]
+    			g33 = shapes[48]
+    			g33_2 = shapes[49]
+    			magTrans = GetShapeLocalTransform(mag0)
+    			boltTrans = GetShapeLocalTransform(bolt)
+    			selectorTrans = GetShapeLocalTransform(selector)
+    			suppressorTrans = GetShapeLocalTransform(suppressor)
+    			scopeTrans = GetShapeLocalTransform(scope)
+    			holoTrans = GetShapeLocalTransform(holo)
+    			holoTrans2 = GetShapeLocalTransform(holo2)
+    			kobraTrans = GetShapeLocalTransform(kobra)
+    			g33Trans = GetShapeLocalTransform(g33)
+    			leupoldTrans = GetShapeLocalTransform(leupold)
+    			leupoldTrans2 = GetShapeLocalTransform(leupold_2)
+    			reddotTrans = GetShapeLocalTransform(reddot)
+    			railTrans = GetShapeLocalTransform(rail)
+    			railTrans2 = GetShapeLocalTransform(rail2)
+    			railTrans3 = GetShapeLocalTransform(rail3)
+    			stock0Trans = GetShapeLocalTransform(stock0)
+    			stock1Trans = GetShapeLocalTransform(stock1)
+    			stock1_2Trans = GetShapeLocalTransform(stock1_2)
+    			stock2Trans = GetShapeLocalTransform(stock2)
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
+    			scopeTrans3 = GetShapeLocalTransform(scope3)
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
+
+    		ht = TransformCopy(holoTrans)
+    		ht2 = TransformCopy(holoTrans2)
+
+    		kbt = TransformCopy(kobraTrans)
+
+    		lpt = TransformCopy(leupoldTrans)
+    		lpt2 = TransformCopy(leupoldTrans2)
+
+    		g33t = TransformCopy(g33Trans)
+    		g33t2 = TransformCopy(g33Trans)
+
+    		rdt = TransformCopy(reddotTrans)
+    		rdt2 = TransformCopy(reddotTrans)
+
+    		sct3 = TransformCopy(scopeTrans3)
+    		sct3_2 = TransformCopy(scopeTrans3)
+
+    		rt = TransformCopy(railTrans)
+    		rt2 = TransformCopy(railTrans2)
+    		rt3 = TransformCopy(railTrans3)
+
+    		stt0 = TransformCopy(stock0Trans)
+    		stt1 = TransformCopy(stock1Trans)
+    		stt1_2 = TransformCopy(stock1_2Trans)
+    		stt2 = TransformCopy(stock2Trans)
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
+    		gdt0 = TransformCopy(guardTrans0)
+    		gdt0_2 = TransformCopy(guardTrans0)
+    		gdt1 = TransformCopy(guardTrans0)
+    		gdt1_2 = TransformCopy(guardTrans0)
+    		gdt2 = TransformCopy(guardTrans0)
+    		gdt2_2 = TransformCopy(guardTrans0)
+    		gdt3 = TransformCopy(guardTrans0)
+    		gdt3_2 = TransformCopy(guardTrans0)
+
+    		if not grenadelauncher then
+    			if magoutTimer ~= 0 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler((0.6-magoutTimer)*120, 0, 0))
+    			elseif maginTimer >= 0.2 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(30, 0, 0))
+    			elseif maginTimer ~= 0 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(maginTimer*180, 0, 0))
+    			end
+    			if magcheckTimer > 2.7 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler((3-magcheckTimer)*120, 0, 0))
+    			elseif magcheckTimer >= 0.6 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(30, 0, 0))
+    			elseif magcheckTimer ~= 0 then
+    				mt.rot = QuatRotateQuat(mt.rot, QuatEuler(magcheckTimer*60, 0, 0))
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
+    				st.rot = QuatEuler(-100, 0, 0)
+    			else
+    				st.rot = QuatEuler(-70, 0, 0)
+    			end
+    		end
+
+    		muzzlelength = 0
+    		if muzzle == "muzzle1" then
+    			spt.pos = VecAdd(spt.pos, Vec(0.075, -0.05, -barrellength))
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
+    			mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, -barrellength))
+    			mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0, -barrellength))
+    			mbt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 3
+    			muzzleFactor = 0.75
+    		else
+    			mbt.pos = hidePos
+    			mbt2.pos = hidePos
+    			mbt.rot = QuatEuler(0, 0, 0)
+    			lightFactor = 2
+    			muzzleFactor = 1
+    			muzzlelength = 0.2
+    		end
+    		if toprail == "scope" and (not ironsight or reloading or scopeTimer < 0.5 or q or e) then
+    			sct.pos = Vec(0.15, -0.675, -0.625)
+    		else
+    			sct.pos = hidePos
+    		end
+    		if toprail == "holo" then
+    			ht.pos = Vec(0.175, -0.475, -0.875)
+    			ht2.pos = Vec(0.2, -0.45, -0.885)
+    		else
+    			ht.pos = hidePos
+    			ht2.pos = hidePos
+    		end
+    		if toprail == "kobra" then
+    			kbt.pos = Vec(0.15, -0.725, -0.65)
+    		else
+    			kbt.pos = hidePos
+    		end
+    		if toprail == "scope2" and ((not ironsight or reloading or scopeTimer < 0.5 or q or e) or altaim) then
+    			lpt.pos = Vec(0.2, -0.475, -0.725)
+    			lpt2.pos = Vec(0.175, -0.4, -0.75)
+    		else
+    			lpt.pos = hidePos
+    			lpt2.pos = hidePos
+    		end
+    		if toprail == "sight3" then
+    			rdt.pos = Vec(0.175, -0.425, -0.975)
+    			rdt2.pos = Vec(0.2, -0.45, -1.025)
+    		else
+    			rdt.pos = hidePos
+    			rdt2.pos = hidePos
+    		end
+    		if toprail == "scope3" and ((not ironsight or reloading or scopeTimer < 0.5 or q or e) or (canted == "sight5" and switchsights)) then
+    			sct3.pos = Vec(0.175, -0.445, -0.525)
+    			sct3_2.pos = Vec(0.15, -0.42, -0.675)
+    		else
+    			sct3.pos = hidePos
+    			sct3_2.pos = hidePos
+    		end
+    		if magnifier == "g33" then
+    			g33t.pos = Vec(0.175, -0.425-0.045, -0.725+0.05)
+    			if magnified then
+    				g33t2.pos = Vec(0.2, -0.3375-0.045, -0.475+0.05)
+    			else
+    				g33t2.pos = Vec(0.35, -0.1875-0.045, -0.475+0.05)
+    				g33t2.rot = QuatRotateQuat(g33t2.rot, QuatEuler(0, 90, 0))
+    			end
+    		else
+    			g33t.pos = hidePos
+    			g33t2.pos = hidePos
+    		end
+    		if removestock == "removed" then
+    			stt0.pos = Vec(0.2, -0.95, -1.35)
+    			stt0.rot = QuatEuler(-90, 180, 0)
+    			stt1.pos = Vec(0.55, -0.95, -1.2)
+    			stt1.rot = QuatEuler(-90, -180, 0)
+    			stt2.pos = Vec(0.2, -0.95, -1.35)
+    			stt2.rot = QuatEuler(-90, 180, 0)
+    			stockFactor = 3
+    		end
+    		if stock == "stock1" then
+    			stt0.pos = hidePos
+    			stt2.pos = hidePos
+    			stockFactor = 0.9
+    		elseif stock == "stock2" then
+    			stt0.pos = hidePos
+    			stt1.pos = hidePos
+    			stt1_2.pos = hidePos
+    			stockFactor = 1.1
+    		elseif stock == "" then
+    			stt1.pos = hidePos
+    			stt1_2.pos = hidePos
+    			stt2.pos = hidePos
+    			stockFactor = 1
+    		end
+    		if stock == "removed" then
+    			stt0.pos = hidePos
+    			stt1.pos = hidePos
+    			stt1_2.pos = hidePos
+    			stt2.pos = hidePos
+    			stockFactor = 3
+    		end
+    		if removestock == "removed" then
+    			stockFactor = 3
+    		end
+
+    		rt.pos = hidePos
+    		rt2.pos = hidePos
+    		rt3.pos = hidePos
+    		if dustcover == "" then
+    			rt.pos = Vec(0.225, -0.575, -0.625)
+    		elseif dustcover == "cover2" then
+    			rt2.pos = Vec(0.225, -0.575, -0.625)
+    			rt3.pos = Vec(0.25, -0.5, -0.75)
+    		end
+
+    		SetShapeLocalTransform(mag0, hideTrans)
+    		SetShapeLocalTransform(mag1, hideTrans)
+    		SetShapeLocalTransform(mag2, hideTrans)
+    		SetShapeLocalTransform(mag3, hideTrans)
+    		SetShapeLocalTransform(mag0_762, hideTrans)
+    		SetShapeLocalTransform(mag1_762, hideTrans)
+    		SetShapeLocalTransform(mag0_556, hideTrans)
+    		SetShapeLocalTransform(mag1_556, hideTrans)
+    		if mag == "" or mag == "mag0" then
+    			magsize = 30
+    			reloadFactor = 1.2
+    			if ammotype == "762" then
+    				SetShapeLocalTransform(mag0_762, Transform(VecAdd(mt.pos, Vec(0, -0.05, 0)), mt.rot))
+    			elseif ammotype == "556" then
+    				SetShapeLocalTransform(mag0_556, mt)
+    			else
+    				SetShapeLocalTransform(mag0, mt)
+    			end
+    		elseif mag == "mag1" then
+    			magsize = 45
+    			reloadFactor = 1.4
+    			if ammotype == "762" then
+    				SetShapeLocalTransform(mag1_762, Transform(VecAdd(mt.pos, Vec(0, -0.1, 0)), mt.rot))
+    			elseif ammotype == "556" then
+    				SetShapeLocalTransform(mag1_556, Transform(VecAdd(mt.pos, Vec(0, -0.15, 0)), mt.rot))
+    			else
+    				SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(0, -0.1, 0)), mt.rot))
+    			end
+    		elseif mag == "mag2" then
+    			magsize = 77
+    			reloadFactor = 1.75
+    			SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.15, 0.05, 0)), mt.rot))
+    		elseif mag == "mag3" then
+    			magsize = 95
+    			reloadFactor = 2.25
+    			SetShapeLocalTransform(mag3, Transform(VecAdd(mt.pos, Vec(-0.45, 0.1, 0)), mt.rot))
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
+    					gt3_1.pos = Vec(0.3, -0.725, -1.35-barrellength)
+    					gt3_2.pos = Vec(0.15, -0.725, -1.35-barrellength)
+    				else
+    					gt3_1.pos = Vec(0.3, -0.675, -2.8-barrellength)
+    					gt3_2.pos = Vec(0.15, -0.675, -2.8-barrellength)
+    					gt3_1.rot = QuatEuler(90, 0, 0)
+    					gt3_2.rot = QuatEuler(90, 0, 0)
+    				end
+
+    			end
+    			gt3.pos = Vec(0.225, -0.725, -2-barrellength)
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
+    			accuracyFactor = 1*bipodFactor
+    			barrellength = 0
+    			bt0.pos = bt0.pos
+    		else
+    			bt0.pos = hidePos
+    		end
+    		if barrel == "barrel1" then
+    			barrelFactorx = 0.8
+    			barrelFactory = 1.05
+    			barrelFactordamage = 1
+    			accuracyFactor = 0.8*bipodFactor
+    			barrellength = 0.35
+    			bt1.pos = bt1.pos
+    		else
+    			bt1.pos = hidePos
+    		end
+    		if barrel == "barrel2" then
+    			barrelFactorx = 0.8
+    			barrelFactory = 1.1
+    			barrelFactordamage = 1.25
+    			accuracyFactor = 0.6*bipodFactor
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
+    		if toprail ~= "holo" then
+    			SetString("savegame.mod.magnifier", "", true)
+    		end
+
+    		if mag == "mag2" or mag == "mag3" or toprail == "scope" or toprail == "kobra" then
+    			SetString("savegame.mod.removestock", "", true)
+    		end
+    		if guard == "" and grip ~= "grenade_launcher" and grip ~= "grip3" then
+    			SetString("savegame.mod.grip", "", true)
+    		end
+    		if guard ~= "" and grip == "grenade_launcher" then
+    			SetString("savegame.mod.grip", "", true)
+    		end
+    		if guard == "guard2" and barrel == "" and grip == "grip3" then
+    			SetString("savegame.mod.grip", "", true)
+    		end
+    		if dustcover == "" and toprail ~= "scope" and toprail ~= "kobra" then
+    			SetString("savegame.mod.toprail", "", true)
+    		end
+    		if dustcover ~= "" and toprail == "kobra" then
+    			SetString("savegame.mod.toprail", "", true)
+    		end
+    		if guard == "" or guard == "guard3" then
+    			SetString("savegame.mod.side", "", true)
+    		end
+
+    		if guard == "" then
+    			gdt0.pos = VecAdd(gdt0.pos, Vec(0, 0, 0))
+    			gdt0_2.pos = VecAdd(gdt0_2.pos, Vec(0.025, 0.025, 0))
+    			guardlength = 0
+    		else
+    			gdt0.pos = hidePos
+    			gdt0_2.pos = hidePos
+    		end
+    		if guard == "guard1" then
+    			gdt1.pos = VecAdd(gdt1.pos, Vec(0, 0, 0))
+    			gdt1_2.pos = VecAdd(gdt1_2.pos, Vec(-0.025, 0.025, 0))
+    			guardlength = -0.15
+    		else
+    			gdt1.pos = hidePos
+    			gdt1_2.pos = hidePos
+    		end
+    		if guard == "guard2" then
+    			gdt2.pos = VecAdd(gdt2.pos, Vec(0, 0.05, 0))
+    			gdt2_2.pos = VecAdd(gdt2_2.pos, Vec(-0.025, 0.025, -0.05))
+    			guardlength = 0
+    		else
+    			gdt2.pos = hidePos
+    			gdt2_2.pos = hidePos
+    		end
+    		if guard == "guard3" then
+    			gdt3.pos = VecAdd(gdt3.pos, Vec(0, 0, 0))
+    			gdt3_2.pos = VecAdd(gdt3_2.pos, Vec(-0.025, 0.025, -0.001))
+    			guardlength = -0.15
+    		else
+    			gdt3.pos = hidePos
+    			gdt3_2.pos = hidePos
+    		end
+
+    		SetShapeLocalTransform(bolt, bt)
+    		SetShapeLocalTransform(selector, st)
+    		SetShapeLocalTransform(suppressor, spt)
+    		SetShapeLocalTransform(scope, sct)
+    		SetShapeLocalTransform(holo, ht)
+    		SetShapeLocalTransform(holo2, ht2)
+    		SetShapeLocalTransform(kobra, kbt)
+    		SetShapeLocalTransform(leupold, lpt)
+    		SetShapeLocalTransform(leupold_2, lpt2)
+    		SetShapeLocalTransform(reddot, rdt)
+    		SetShapeLocalTransform(reddot2, rdt2)
+    		SetShapeLocalTransform(scope3, sct3)
+    		SetShapeLocalTransform(scope3_2, sct3_2)
+    		SetShapeLocalTransform(g33, g33t)
+    		SetShapeLocalTransform(g33_2, g33t2)
+    		SetShapeLocalTransform(rail, rt)
+    		SetShapeLocalTransform(rail2, rt2)
+    		SetShapeLocalTransform(rail3, rt3)
+    		SetShapeLocalTransform(stock0, stt0)
+    		SetShapeLocalTransform(stock1, stt1)
+    		SetShapeLocalTransform(stock1_2, stt1_2)
+    		SetShapeLocalTransform(stock2, stt2)
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
+    		SetShapeLocalTransform(guard0, gdt0)
+    		SetShapeLocalTransform(guard0_2, gdt0_2)
+    		SetShapeLocalTransform(guard1, gdt1)
+    		SetShapeLocalTransform(guard1_2, gdt1_2)
+    		SetShapeLocalTransform(guard2, gdt2)
+    		SetShapeLocalTransform(guard2_2, gdt2_2)
+    		SetShapeLocalTransform(guard3, gdt3)
+    		SetShapeLocalTransform(guard3_2, gdt3_2)
+    	end
+
+    	if selectattachments then
+    		clickedmag = clickedmag1 or clickedmag2 or clickedmag3
+    		if clickedmag and selectattachments and not InputPressed(attachmentsKey) and not GetBool("level.optionstriggered") then
+    			Reload()
+    		end
+    	end
+    	if reloading and not clickedmag and selectattachments then
+    		selectattachments = false
+    		selectattachmentsTimer = 0.25
+    	end
+
+    	if not selectattachments then
+    		if (InputPressed(reloadKey) or clickedmag) and selectfireTimer == 0 then
+    			if not realistic and (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) then
+    				Reload()
+    				inspectTimer = 0
+    			end
+    		end
+
+    		if (InputReleased(reloadKey) or clickedmag) and selectfireTimer == 0 then
+    			if realistic and curmagslot ~= nextmagslot and magcheckTimer == 0 then
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
+    			if reloadTimer < 0.7 and not cocksoundplaying and ammo == 0 then
+    				cocksoundplaying = true
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.85)
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
+    	local x2, y2, z2, rotx2, roty2, rotz2 = 0.175, -0.8, -1.9, 0, 0, 0
+    	if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.2 then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0.3, -0.6, -0.3+bt.pos[3], 0, 0, 0
+    	elseif reloading then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0+mt.pos[1], 0.35+mt.pos[2], 0+mt.pos[3], 0, 0, 0
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
+    	sightattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.4, -1))
+    	muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.55, -2.5-barrellength))
+    	stockattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.65, -0.6))
+    	removestockattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.7, -0.5))
+    	sideattachpoint = TransformToParentPoint(btrans, Vec(0.175, -0.65, -1.8))
+    	magattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1.15))
+    	gripattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.75, -1.7))
+    	barrelattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.65, -1.6))
+    	guardattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.55, -1.5))
+    	dustcoverattachpoint = TransformToParentPoint(btrans, Vec(0.275, -0.5, -0.7))
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
+    if GetString("game.player.tool") == "ak105" and GetPlayerVehicle(playerId) == 0 then
+
+    	------SCOPE RETICLE------
+    	if toprail == "scope" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
+    		local gt = GetBodyTransform(GetToolBody())
+    		local sightcenter = Vec(0.275, -0.2875, -1.8)
+    		local sightrear = Vec(0.275, -0.2875, -1.4)
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
+    	elseif toprail == "scope2" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) and not altaim then
+    		local gt = GetBodyTransform(GetToolBody())
+    		local sightcenter = Vec(0.275, -0.3, -1.8)
+    		local sightrear = Vec(0.275, -0.3, -1.4)
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
+    			local w, h = UiGetImageSize("MOD/img/reticle6.png")
+    			local x, y = UiWorldToPixel(holopoint)
+    			UiTranslate(x-w/2, y-h/2)
+    			UiImage("MOD/img/reticle6.png")
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
+    		UiPop()
+    	elseif toprail == "sight4" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
+    		UiPush()
+    			w, h = UiGetImageSize("MOD/img/reticle3.png")
+    			UiTranslate((UiWidth()-w)/2, (UiHeight()-h)/2)
+    			UiTranslate(RECroty*-100, RECrotx*-100-recoilAngle*40-recoilTimer2*400)
+    			if realistic then
+    				UiTranslate(-math.sin(1.3*GetTime())*6*bipodFactor^4, -math.sin(2.1*GetTime())*4*bipodFactor^4)
+    			end
+    			local speed =VecLength(GetPlayerVelocity(playerId))
+    			if speed > 1 then
+    				UiTranslate(-swayx*speed*120, -swayy*speed*80)
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
+    	elseif toprail == "scope3" and ironsight and not reloading and scopeTimer >= 0.5 and not (q or e) then
+    		local gt = GetBodyTransform(GetToolBody())
+    		local sightcenter = Vec(0.275, -0.25, -1.8)
+    		local sightrear = Vec(0.275, -0.25, -1.1)
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
+    			local w, h = UiGetImageSize("MOD/img/reticle7.png")
+    			local x, y = UiWorldToPixel(holopoint)
+    			UiTranslate(x-w/2, y-h/2)
+    			if altaim then
+    				UiImage("MOD/img/reticle3.png")
+    			else
+    				UiImage("MOD/img/reticle7.png")
+    			end
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
+    				UiText("Infinite")
+    			end
+    		UiPop()
+    	end
+    	end
+    	if realistic then
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
+    if GetString("game.player.tool") == "ak105" and grenadelauncher and not selectattachments then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle")
+    		UiImage("ui/hud/crosshair-launcher.png")
+    	UiPop()
+    end
+    if GetString("game.player.tool") == "ak105" and sideattachment and side == "side3" then
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
+    if realistic and selectmag and GetString("game.player.tool") == "ak105" then
+    	hoverindex=0
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(magattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				if totalmags ~= 0 then
+    				for i = 1, totalmags do
+    				clickedslot = MagButton(nextmagslot,i,true,{curx,cury},{"Ammo: ", CheckAmmo(i)},60,60)
+    				UiTranslate(60,0)
+    				curx,cury=curx+60,cury
+    				end
+    				end
+    			UiPop()
+    		end
+    	UiPop()
+    end
+
+    ------ATTACHMENTS MENU------
+    if not realistic or GetBool("level.optionstriggered") then
+    if selectattachments and GetString("game.player.tool") == "ak105" and GetPlayerVehicle(playerId) == 0 then
+
+    local total = 9
+    gripattachpoint2 = AttachmentGroup("attachmentgroup","grip",gripattachpoint,Description,1/total,60,60)
+    barrelattachpoint2 = AttachmentGroup("attachmentgroup","barrel",barrelattachpoint,Description,2/total,60,60)
+    muzzleattachpoint2 = AttachmentGroup("attachmentgroup","muzzle",muzzleattachpoint,Description,3/total,60,60)
+    if guard ~= "" and guard ~= "guard3" then
+    sideattachpoint2 = AttachmentGroup("attachmentgroup","side",sideattachpoint,Description,4/total,60,60)
+    else
+    	SetString("savegame.mod.side", "", true)
+    end
+    guardattachpoint2 = AttachmentGroup("attachmentgroup","guard",guardattachpoint,Description,5/total,60,60)
+    sightattachpoint2 = AttachmentGroup("attachmentgroup","toprail",sightattachpoint,Description,6/total,60,60)
+    dustcoverattachpoint2 = AttachmentGroup("attachmentgroup","dustcover",dustcoverattachpoint,Description,7/total,60,60)
+    stockattachpoint2 = AttachmentGroup("attachmentgroup","stock",stockattachpoint,Description,8/total,60,60)
+    if not realistic then
+    magattachpoint2 = AttachmentGroup("attachmentgroup","mag",magattachpoint,Description,9/total,60,60)
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
+    				if dustcover ~= "" then
+    					clickedscope = AttachmentButton("toprail","sight3",true,{curx,cury},{"Red Dot","1x magnification sight for close range combat."})
+    					UiTranslate(-70,0)
+    					curx,cury=curx-70,cury
+    					clickedholo = AttachmentButton("toprail","holo",true,{curx,cury},{"Holographic Sight","1x magnification sight for close range combat."})
+    					UiTranslate(70,70)
+    					curx,cury=curx+70,cury+70
+    					clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
+    					UiTranslate(-70,0)
+    					curx,cury=curx-70,cury
+    					clickedholo = AttachmentButton("toprail","scope2",true,{curx,cury},{"Leupold Scope with Delta Sight","3x magnification scope with a 1x delta sight on top for close range combat."})
+    					UiTranslate(-70,0)
+    					curx,cury=curx-70,cury
+    					clickedholo = AttachmentButton("toprail","scope3",true,{curx,cury},{"Eotech Vudu Scope","1x / 6x magnification scope."})
+    					UiTranslate(-100,0)
+    					curx,cury=curx-70,cury
+    					--clickedholo = AttachmentButton("toprail","sight4",true,{curx,cury},{"Precision Scope","8x magnification sight for long range combat."})
+    					UiTranslate(-100,0)
+    					curx,cury=curx-70,cury
+    					--clickedholo = AttachmentButton("toprail","scope4",true,{curx,cury},{"FLIR Scope","1x / 6x magnification sight with infrared sensor that detects heat signatures."})
+    					UiTranslate(340,70)
+    					curx,cury=curx+340,cury+70
+    					clickedholo = AttachmentButton("canted","sight5",true,{curx,cury},{"Cented Delta Sight","1x magnification canted sight for close range combat."})
+    					UiTranslate(-70,0)
+    					curx,cury=curx-70,cury
+    					if toprail == "holo" then
+    						clickedmagnifier1 = AttachmentButton("magnifier","g33",true,{curx,cury},{"Thermal Magnifier","Foldable 3x magnifier for close range optics that shows heat signatures. Press 'Z' to fold/unfold."})
+    					end
+    				else
+    					clickedscope = AttachmentButton("toprail","scope",true,{curx,cury},{"Scope","3x magnification sight for medium range combat."})
+    					UiTranslate(-70,0)
+    					curx,cury=curx-70,cury
+    					clickedscope = AttachmentButton("toprail","kobra",true,{curx,cury},{"Red Dot Sight","1x magnification sight for close range combat."})
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
+    				clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Muzzle Break","Reduces recoil, but turns your barrel into a flashbang."})
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
+    				if guard == "guard1" or guard == "guard2" then
+    				clickedside1 = AttachmentButton("side","side1",true,{curx,cury},{"Laser","A laser that points where you shoot."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedside2 = AttachmentButton("side","side2",true,{curx,cury},{"Flashlight","Lights up the area in front of you."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedside3 = AttachmentButton("side","side3",true,{curx,cury},{"Rangefinder","Displays the range to your target."})
+    				UiTranslate(-70,0)
+    				end
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
+    				clickedmag1 = AttachmentButton("mag","mag1",true,{curx,cury},{"45rnd Mag","Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmag2 = AttachmentButton("mag","mag2",true,{curx,cury},{"77rnd Drum","Pew Pew Pew Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmag3 = AttachmentButton("mag","mag3",true,{curx,cury},{"95rnd Double Drum","Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew Pew"})
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
+    				if guard ~= "" then
+    				clickedgrip1 = AttachmentButton("grip","grip1",true,{curx,cury},{"Vertical Grip","Decreased vertical recoil."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedgrip2 = AttachmentButton("grip","grip2",true,{curx,cury},{"Angled Grip","Decreased horizontal recoil."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				end
+    				if not (guard == "guard2" and barrel == "") then
+    				clickedgrip3 = AttachmentButton("grip","grip3",true,{curx,cury},{"Bipod","Increased accuracy while crouching or resting the gun on a ledge."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				end
+    				if guard == "" then
+    				clickedgrip4 = AttachmentButton("grip","grenade_launcher",true,{curx,cury},{"GP-25","Grenade launcher for increased collateral damage."})
+    				end
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
+    				clickedbarrel1 = AttachmentButton("barrel","barrel1",true,{curx,cury},{"AK-74 Barrel","Increased accuracy but more vertical recoil."})
+    				UiTranslate(-100,0)
+    				curx,cury=curx-100,cury
+    				clickedbarrel2 = AttachmentButton("barrel","barrel2",true,{curx,cury},{"RPK-74 Barrel","Increased accuracy and damage but more vertical recoil."})
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
+    				clickedguard1 = AttachmentButton("guard","guard1",true,{curx,cury},{"Modernised Handguard","Allows for attachments such as grips and lasers."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedguard2 = AttachmentButton("guard","guard3",true,{curx,cury},{"Modernised Handguard","Allows for attachments such as grips and lasers."})
+    				UiTranslate(-100,0)
+    				curx,cury=curx-100,cury
+    				clickedguard2 = AttachmentButton("guard","guard2",true,{curx,cury},{"Modernised Handguard","Allows for attachments such as grips and lasers."})
+    			UiPop()
+    		end
+    	UiPop()
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(dustcoverattachpoint2)
+    		if GetString("savegame.mod.attachmentgroup") == "dustcover" and dist ~= 0 then
+    			UiTranslate(x,y+70)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
+    				clickedmoderncover = AttachmentButton("dustcover","cover2",true,{curx,cury},{"Modernised Dust Cover","Allows for attachments of optics."})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				--clickedcoverremoved = AttachmentButton("dustcover","cover3",true,{curx,cury},{"Remove Dust Cover","Removes dust cover for that scav look."})
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
+    				clickedstock1 = AttachmentButton("stock","stock1",true,{curx,cury},{"Sidefolder","Side folding light metal stock."})
+    				UiTranslate(70,0)
+    				curx,cury=curx+70,cury
+    				clickedstock2 = AttachmentButton("stock","stock2",true,{curx,cury},{"Light Stock","Light stock."})
+    				UiTranslate(70,0)
+    				curx,cury=curx+70,cury
+    				clickedstock3 = AttachmentButton("stock","removed",true,{curx,cury},{"Remove Stock","Removes stock entirely."})
+    			UiPop()
+    		end
+    	UiPop()
+    end
+    end
+    if selectattachments and GetString("game.player.tool") == "ak105" and GetPlayerVehicle(playerId) == 0 or GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
+    hoverindex=0
+    UiPush()
+    	local x,y,dist=UiWorldToPixel(removestockattachpoint)
+    		if GetString("savegame.mod.attachmentgroup") and dist ~= 0 then
+    			UiTranslate(x,y)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    			UiAlign("center middle")
+    			if not InputDown("shift") and mag ~= "mag2" and mag ~= "mag3" and toprail ~= "scope" and toprail ~= "kobra" then
+    				clickedstockremoved = AttachmentButton("removestock","removed",true,{curx,cury},{"Fold Stock","Folds stock for a smaller profile weapon."})
+    			end
+    		UiPop()
+    	end
+    UiPop()
+    end
+    if hint and (selectattachments or InputDown(reloadKey) and heldrTimer > 0.2) then drawHint(info) end
+
+    ------OPTIONS UI------
+    if GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
+    UiPush()
+    	UiAlign("center middle")
+    	UiTranslate(UiCenter(), 70)
+    	UiFont("bold.ttf", 60)
+    	UiText("WEAPON MODDING")
+    UiPop()
+    end
+
+    if GetBool("level.optionstriggered") and GetString("game.player.tool") == "ak105" then
+
+    UiAlign("center middle")
+    UiTranslate(300, 250)
+    UiFont("bold.ttf", 48)
+    local ammotext = "5"
+    if ammotype == "556" then
+    	ammotext = "2"
+    elseif ammotype == "762" then
+    	ammotext = "4"
+    end
+    UiText("AK-10"..ammotext)
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
+    UiTranslate(0, 100)
+    UiPush()
+    	local curx,cury=120,635
+    	UiAlign("center middle")
+    	UiTranslate(100, 0)
+    	curx,cury=curx+100,cury
+    	clickedammo1 = AttachmentButton("ammotype","545",true,{curx,cury},{"5.45x39","Smaller, higher velocity round that does less damage to target."})
+    	UiTranslate(-100,0)
+    	curx,cury=curx-100,cury
+    	clickedammo2 = AttachmentButton("ammotype","762",true,{curx,cury},{"7.62x39","Larger, lower velocity round that does more damage to target."})
+    	UiTranslate(-100,0)
+    	curx,cury=curx-100,cury
+    	clickedammo3 = AttachmentButton("ammotype","556",true,{curx,cury},{"7.62x51","Larger, higher velocity round that does more damage to target."})
+    UiPop()
+    if GetString("savegame.mod.ammotype") == "" then
+    	SetString("savegame.mod.ammotype", "545", true)
+    end
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
+
+    if not realistic then
+    	UiTranslate(0, 240)
+    end
+
+    UiPush()
+    	UiTranslate(800+optionsx*100, -80)
+    	UiFont("bold.ttf", 26)
+    	UiTranslate(-120, 70)
+    	UiText("Horizontal Recoil: "..round(recoilHorizontal*stockFactor*laserFactor*muzzleFactor*gripfactorx*barrelFactorx*ammoFactory, 2))
+    	UiTranslate(260, 0)
+    	UiText("Vertical Recoil: "..round(recoilFactor*muzzleFactor*gripfactory*barrelFactory*ammoFactory, 2))
+    	UiTranslate(200, 0)
+    	UiText("Accuracy: "..round(1/accuracyFactor, 2))
+    UiPop()
+
+    UiPush()
+    	UiTranslate(-200, 50)
+    	UiPush()
+    		UiAlign("center middle")
+    		KeybindButton("Reload")
+    		UiTranslate(124, 0)
+    		KeybindButton("Check-Mag")
+    		UiTranslate(140, 0)
+    		KeybindButton("Fire-Mode")
+    		UiTranslate(132, 0)
+    		KeybindButton("Lean-Left")
+    		UiTranslate(132, 0)
+    		KeybindButton("Lean-Right")
+    		UiTranslate(152, 0)
+    		KeybindButton("Attachments")
+    		UiTranslate(132, 0)
+    		KeybindButton("Melee")
+    		UiTranslate(148, 0)
+    		KeybindButton("Side-Attachment")
+    		UiTranslate(204, 0)
+    		KeybindButton("Grenade-Launcher")
+    		UiTranslate(204, 0)
+    		KeybindButton("Inspect-Weapon")
+    		UiTranslate(164, 0)
+    		KeybindButton("Clear-Jam")
+    	UiPop()
+    UiPop()
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
-	SetString("game.player.tool","ak105")
-	SetBool("level.optionstriggered",true)
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetString("game.player.tool","ak105", true)
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
