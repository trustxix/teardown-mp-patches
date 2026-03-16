# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,387 +1,4 @@
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
-	conversion = GetString("savegame.mod.conversion")
-	if conversion == "" then
-		conversion = "Semi"
-	end
-	gunname = "Glock 17"
-	if conversion == Full then
-		gunname = "Glock 18"
-	end
-
-	RegisterTool("g17", "Glock 17", "MOD/vox/g17.vox", 3)
-	SetBool("game.tool.g17.enabled", true)
-	SetFloat("game.tool.g17.ammo", 101)
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
-	damage = 0.11 * GetInt("savegame.mod.damage")/100
-	if damage == 0 then
-		damage = 0.11
-	end
-	gravity = Vec(0, -10, 0)
-	hidePos = Vec(0, -200, 0)
-	hideTrans = Transform(hidePos,QuatEuler())
-	velocity = 320
-	drag = 2
-	maxMomentum = 1.5
-	tracer = false
-
-	recoilVertical = 0.8
-	recoilHorizontal = 0.7
-	recoilWander = 3.5
-
-	lvl5armor = 0
-	lvl4armor = 0.05
-	lvl3armor = 0.15
-	lvl2armor = 0.5
-	lvl1armor = 0.7
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
-	realistic = GetBool("savegame.mod.realistic")
-	--realistic = true
-	--inventoryenabled = true
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
-	if inventoryenabled then
-		magtable2 = {}
-		local guninfo = Split(GetString("inventory.guns2"), "_")
-		magtable2[1] = {guninfo[3], tonumber(guninfo[5]), tonumber(guninfo[6]), {1,1}}
-		for i = 1, 8 do
-			for j = 1, 15 do
-				if GetString("inventory.backpack"..i.."_"..j) ~= "" then
-					local maginfo = Split(GetString("inventory.backpack"..i.."_"..j), "_")
-					local magtype, magammo, magammomax = maginfo[1], maginfo[3], maginfo[4]
-					if string.sub(magtype, 1, 3) == "mag" and string.sub(magtype, 6, 11) == "glock-9x19" then
-						table.insert(magtable2, {magtype,tonumber(magammo),tonumber(magammomax),{i,j}})
-					end
-				end
-			end
-		end
-		totalmags = #magtable2
-	else
-		if totalmags == 0 then
-			mslot1, mslot2 = "mag0", "mag0"
-			SetString("savegame.mod.mslot1", "mag0")
-			SetString("savegame.mod.mslot2", "mag0")
-		totalmags = 2
-		end
-		magtable2 = {{mslot1,0,0},{mslot2,0,0},{mslot3,0,0},{mslot4,0,0},{mslot5,0,0},{mslot6,0,0},{mslot7,0,0},{mslot8,0,0}}
-		for i=1,8 do
-			local magslottype = GetString("savegame.mod.mslot"..i)
-			if magslottype == "mag0" then
-				magtable2[i][2] = 30
-				magtable2[i][3] = 30
-			elseif magslottype == "mag1" then
-				magtable2[i][2] = 40
-				magtable2[i][3] = 40
-			elseif magslottype == "mag2" then
-				magtable2[i][2] = 60
-				magtable2[i][3] = 60
-			elseif magslottype == "mag3" then
-				magtable2[i][2] = 100
-				magtable2[i][3] = 100
-			else
-				magtable2[i][2] = 20
-				magtable2[i][3] = 20
-			end
-		end
-	end
-	curmagslot = 1
-	nextmagslot = 2
-	if inventoryenabled then
-		local guninfo = Split(GetString("inventory.guns2"), "_")
-		mag = guninfo[3]
-		reloadFactor = 1
-	elseif realistic then
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
-
-	if inventoryenabled then
-		item = GetString("inventory.guns2")
-		guninfo = Split(item, "_")
-		if #guninfo == 8 then
-			attachmentinfo = Split(guninfo[8], "-")
-			toprail = attachmentinfo[1]
-			canted = attachmentinfo[2]
-			muzzle = attachmentinfo[3]
-			stock = attachmentinfo[4]
-			grip = attachmentinfo[5]
-			barrel = attachmentinfo[6]
-			side = attachmentinfo[7]
-			guard = attachmentinfo[8]
-			magnifier = attachmentinfo[9]
-		else
-			toprail = ""
-			canted = ""
-			muzzle = ""
-			stock = ""
-			grip = ""
-			barrel = ""
-			side = ""
-			guard = ""
-			magnifier = ""
-		end
-	end
-
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
-	shotDelay = 0.05
-	spreadTimer = 1.25
-	spreadFactor = 1.5
-	accuracyFactor = 1
-	
-	if not realistic then
-		if mag == "" or mag == "mag0-glock-9x19" then
-			magsize = 17
-			reloadFactor = 1
-		elseif mag == "mag1-glock-9x19" then
-			magsize = 33
-			reloadFactor = 1.15
-		elseif mag == "mag2-glock-9x19" then
-			magsize = 50
-			reloadFactor = 1.35
-		else
-			magsize = 17
-			reloadFactor = 1
-		end
-		ammo = magsize
-	else
-		if not inventoryenabled then
-			ammo = magtable2[curmagslot][2]
-		else
-			ammo = magtable2[1][2]
-		end
-	end
-	if inventoryenabled then
-		initammo = false
-	end
-	ammoleft = 0
-	maxammoleft = 0
-	nextammo = 0
-	reloadFactor = 1
-	barrellength = 0
-	guardlength = 0
-	barrelFactorx = 0.8
-	barrelFactory = 1
-	barrelFactordamage = 1.25
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
-
-	e = false
-	q = false
-	selectfire = 1
-	selectfire0 = 0
-	selectfireTimer = 0
-	selectfireText = conversion
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
@@ -453,19 +70,19 @@
 	loadedShell.predictedBulletVelocity = VecAdd(loadedShell.predictedBulletVelocity, Vec((math.random()-0.5)*accuracyFactor*2, (math.random()-0.5)*accuracyFactor*2, (math.random()-0.5)*accuracyFactor*2))
 
 	local barrelend = barrellength + muzzlelength
-	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -1.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.02), GetPlayerVelocity()), 0.3, 0.3)
+	SpawnParticle("smoke", TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -1.4-barrelend*4/3)), VecAdd(VecScale(dir, 0.02), GetPlayerVelocity(playerId)), 0.3, 0.3)
 	ParticleType("plain")
 	ParticleTile(5)
 	ParticleColor(1, 0.6, 0.4, 1, 0.3, 0.2)
 	ParticleRadius(0.1)
 	ParticleEmissive(5, 1)
-	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -1.3-barrelend*4/3)), VecAdd(VecScale(dir, 0.04), GetPlayerVelocity()), 0.2, 0.3)
+	SpawnParticle(TransformToParentPoint(GetBodyTransform(GetToolBody()), Vec(0.25, -0.6, -1.3-barrelend*4/3)), VecAdd(VecScale(dir, 0.04), GetPlayerVelocity(playerId)), 0.2, 0.3)
 	if muzzle == "muzzle1" then
-		PlaySound(suppressedgunsound, GetPlayerTransform().pos, 0.75, false)
+		PlaySound(suppressedgunsound, GetPlayerTransform(playerId).pos, 0.75, false)
 	elseif muzzle == "muzzle2" then
-		PlaySound(gunsound, GetPlayerTransform().pos, 0.7, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.7, false)
 	else
-		PlaySound(gunsound, GetPlayerTransform().pos, 0.6, false)
+		PlaySound(gunsound, GetPlayerTransform(playerId).pos, 0.6, false)
 	end
 
 	if not unlimitedammo then
@@ -483,11 +100,11 @@
 				end
 				local guninfo = Split(GetString("inventory.guns2"), "_")
 				if #guninfo == 8 then
-					SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19_"..guninfo[8])
+					SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19_"..guninfo[8], true)
 				else
-					SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19")
+					SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19", true)
 				end
-				SetBool("inventory.update", true)
+				SetBool("inventory.update", true, true)
 			end
 		end
 	end
@@ -530,7 +147,7 @@
 	ak47grenadeHandler.shellNum = (ak47grenadeHandler.shellNum%#ak47grenadeHandler.shells) + 1
 
 	SpawnParticle("fire", gunpos, Vec(0, 1.0+math.random(1,10)*0.1, 0), 0.3, 0.1)
-	PlaySound(grenadelaunchersound, GetPlayerTransform().pos, 0.75, false)
+	PlaySound(grenadelaunchersound, GetPlayerTransform(playerId).pos, 0.75, false)
 
 	if not unlimitedammo then
 		grenadelauncherammo = grenadelauncherammo - 1
@@ -626,7 +243,7 @@
 
 			local factor = barrelFactordamage
 
-			if projectile.momentum > 0 then
+			if projectile.momentum ~= 0 then
 				MakeHole(hitPos, damage*factor, damage*0.85*factor, damage*0.7*factor)
 			end
 		end
@@ -678,7 +295,7 @@
 		else
 			reloadTimer = reloadTime - 0.7
 		end
-		if realistic and totalmags > 0 then
+		if realistic and totalmags ~= 0 then
 			if not inventoryenabled then
 			if ammo == 0 then
 				magtable2[curmagslot][2] = ammo
@@ -697,9 +314,9 @@
 		end
 		magoutTimer = 0.6
 		if mag == "none" and inventoryenabled then
-			PlaySound(interactsound1, GetPlayerTransform().pos, 0.5, false)
+			PlaySound(interactsound1, GetPlayerTransform(playerId).pos, 0.5, false)
 		else
-			PlaySound(reloadsound, GetPlayerTransform().pos, 0.5, false)
+			PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.5, false)
 		end
 	end
 end
@@ -722,7 +339,7 @@
 	local gt = GetBodyTransform(GetToolBody())
 	local casingpos = TransformToParentPoint(gt, Vec(0.325, -0.4, -0.65))
 	local fwdpos = TransformToParentPoint(gt, Vec(1+math.random()*4, 4+math.random()*4, -0.3+math.random()*4))
-	local direction = VecAdd(GetPlayerVelocity(), VecSub(fwdpos, casingpos))
+	local direction = VecAdd(GetPlayerVelocity(playerId), VecSub(fwdpos, casingpos))
 	casing = Spawn("MOD/vox/casing.xml", Transform(casingpos, QuatEuler(math.random(0, 90), math.random(0, 90), math.random(0, 90))))
 	SetBodyVelocity(casing[1], direction)
 end
@@ -767,17 +384,17 @@
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
@@ -809,13 +426,13 @@
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
@@ -867,6 +484,7 @@
 			laserFactor = 1
 		end
 end
+
 function Flashlight(active)
 		local gt = GetBodyTransform(GetToolBody())
 		local gunpos = TransformToParentPoint(gt, Vec(0.275, -0.5, -1.9))
@@ -949,27 +567,27 @@
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
@@ -1033,32 +651,32 @@
 	end
 
 	if not bool then
-		if RELx > 0 then 
+		if RELx ~= 0 then 
 			RELx = RELx - dt*math.abs((RELx-0))*3
 		elseif RELx < 0 then
 			RELx = RELx + dt*math.abs((RELx-0))*3
 		end
-		if RELy > 0 then 
+		if RELy ~= 0 then 
 			RELy = RELy - dt*math.abs((RELy-0))*3
 		elseif RELy < 0 then
 			RELy = RELy + dt*math.abs((RELy-0))*3
 		end
-		if RELz > 0 then 
+		if RELz ~= 0 then 
 			RELz = RELz - dt*math.abs((RELz-0))*3
 		elseif RELz < 0 then
 			RELz = RELz + dt*math.abs((RELz-0))*3
 		end
-		if RELrotx > 0 then 
+		if RELrotx ~= 0 then 
 			RELrotx = RELrotx - dt*math.abs((RELrotx-0))*3
 		elseif RELrotx < 0 then
 			RELrotx = RELrotx + dt*math.abs((RELrotx-0))*3
 		end
-		if RELroty > 0 then 
+		if RELroty ~= 0 then 
 			RELroty = RELroty - dt*math.abs((RELroty-0))*3
 		elseif RELroty < 0 then
 			RELroty = RELroty + dt*math.abs((RELroty-0))*3
 		end
-		if RELrotz > 0 then 
+		if RELrotz ~= 0 then 
 			RELrotz = RELrotz - dt*math.abs((RELrotz-0))*3
 		elseif RELrotz < 0 then
 			RELrotz = RELrotz + dt*math.abs((RELrotz-0))*3
@@ -1110,32 +728,32 @@
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
@@ -1187,32 +805,32 @@
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
@@ -1264,32 +882,32 @@
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
@@ -1330,1297 +948,12 @@
 		checkammotext = "About Half Full"
 	elseif percentage > 0.2 then
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
-	if inventoryenabled and not reloading then
-		item = GetString("inventory.guns2")
-		if Split(item, "_")[1] == "g17" then
-			guninfo = Split(item, "_")
-			if GetBool("inventory.update_guns2") or not initammo then
-				ammo = tonumber(guninfo[5])
-				mag = guninfo[3]
-				SetBool("inventory.update_guns2", false)
-				initammo = true
-			end
-		end
-	end
-	
-	if inventoryenabled then
-		magtable2 = {}
-		local guninfo = Split(GetString("inventory.guns2"), "_")
-		magtable2[1] = {guninfo[3], tonumber(guninfo[5]), tonumber(guninfo[6]), {1,1}}
-		for i = 1, 8 do
-			for j = 1, 15 do
-				if GetString("inventory.backpack"..i.."_"..j) ~= "" then
-					local maginfo = Split(GetString("inventory.backpack"..i.."_"..j), "_")
-					local magtype, magammo, magammomax = maginfo[1], maginfo[3], maginfo[4]
-					if string.sub(magtype, 1, 3) == "mag" and string.sub(magtype, 6, 15) == "glock-9x19" then
-						table.insert(magtable2, {magtype,tonumber(magammo),tonumber(magammomax),{i,j}})
-					end
-				end
-			end
-		end
-		totalmags = #magtable2
-		if nextmagslot > totalmags then
-			nextmagslot = 1
-		end
-	end
-
-	if GetString("game.player.tool") == "g17" and GetPlayerVehicle() == 0 then
-		SetBool("hud.aimdot", false)
-
-
-		------CONTROLS------
-		if InputDown("lmb") and not reloading and selectfire == 1 and conversion == "Full" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 and not selectmag then
-			if ammo > 0 then
-				Shoot()
-			end
-		elseif InputPressed("lmb") and not reloading and selectfire == 1 and conversion == "Semi" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape() == 0 and not InputDown("shift") and inspectTimer <= 0 and not selectmag then
-			if ammo > 0 then
-				Shoot()
-				shootTimer = 0.05
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
-		if selectfire == 0  and selectfireTimer <= 0 then
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
-			inspectTimer = 0
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
-		if InputDown(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 and not realistic or GetBool("level.optionstriggered") then
-			if InputPressed(attachmentsKey) and not GetBool("level.optionstriggered") then
-				PlaySound(interactsound2, GetPlayerTransform().pos, 1)
-				selectattachmentsTimer = 0.5
-			end
-			UiMakeInteractive()
-			selectattachments = true
-			ironsight = false
-			inspectTimer = 0
-		end
-		if InputReleased(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and not realistic then
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
-
-		if InputPressed(magcheckKey) and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 then
-			magcheckTimer = 4
-			PlaySound(reloadsound, GetPlayerTransform().pos, 0.5)
-			inspectTimer = 0
-		end
-		if magcheckTimer > 0 then
-			magcheckTimer = magcheckTimer - dt*1.5
-			ironsight = false
-		end
-		if magcheckTimer < 0 then
-			magcheckTimer = 0
-			PlaySound(reloadsound2, GetPlayerTransform().pos, 0.5)
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
-			for i = 1, totalmags do
-				if magtable2[i][2] > magtable2[nextmagslot][2] and i ~= curmagslot then
-					nextmagslot = i
-				end
-			end
-			inspectTimer = 0
-			Reload()
-		end
-		if InputReleased(reloadKey) then heldrTimer = 0 end
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
-		if InputPressed("y") and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire > 0 then
-			if inspectTimer <= 0 then
-				inspectTimer = 6
-				ironsight = false
-			else
-				inspectTimer = 0
-			end
-		end
-
-		if selectfire == 1 then
-			selectfireText = conversion
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
-			recoilFactor = recoilVertical
-		else
-			recoilFactor = recoilVertical*1.75
-		end
-
-		if ironsight then
-			recoilMax = 8*muzzleFactor
-		else
-			recoilMax = 20*muzzleFactor
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
-		if realistic or inventoryenabled then
-			if maginTimer > 0 then
-				if totalmags == 0 then
-					mag = "none"
-					maginTimer = 0
-				elseif not inventoryenabled then
-					mag = magtable2[curmagslot][1]
-				end
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
-
-		local b = GetToolBody()
-		if b ~= 0 then
-			local magoffset = Vec(-0.025, 0, -0.0125)
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
-			x,y,z,rotx,roty,rotz = -0.2,0.35,-0.5,0,0,0
-			if ironsight then
-			if grenadelauncher then
-				x = 0
-				y = 0.45
-				z = -0.4
-				rotz = 0
-			elseif q then
-				x = 0.9
-				y = 0.1
-				z = -0.4
-				rotz = 30
-			elseif e then
-				x = -0.3
-				y = 0.4
-				z = -0.4
-				rotz = -15
-			else
-				if toprail == "holo" then
-					x = 0.275
-					y = 0.4375
-					z = -0.45
-					rotz = 0
-				elseif toprail == "" then
-					x = 0.275
-					y = 0.5
-					z = -0.45
-					rotz = 0
-				elseif toprail == "scope" then
-					x = 0.275
-					y = 0.4
-					z = 0.25
-					rotz = -0.25
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
-				if toprail == "holo" then
-					local gt = GetBodyTransform(GetToolBody())
-					local sightcenter = Vec(0.275, -0.4375, -0.7)
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
-			-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(math.sin(2.1*GetTime())/9,  math.sin(1.3*GetTime())/6, 0))
-			-- offset.pos = VecAdd(offset.pos, Vec(math.sin(1.1*GetTime())/360,  math.sin(0.7*GetTime())/240, 0))
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
-				recoilTimer = recoilTimer - dt
-				boltoffset = Vec(0, 0, recoilTimer*2.5)
-			end
-			if recoilTimer2 > 0 then
-				recoilTimer2 = recoilTimer2 - (recoilTimer2*0.1+dt)
-				-- offset.pos = VecAdd(offset.pos, Vec(0, -recoilTimer2/2, recoilTimer2))
-				-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(recoilTimer2*40, 0, 0))
-			end
-			local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/400, (recoilAngle/-100)-(rnd1+rnd4)/400-recoilTimer2/2, recoilTimer2, recoilAngle + (rnd1+rnd4)/4+recoilTimer2*40, (rnd2+rnd5)/4, (rnd3+rnd6)/4
-			-- RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
-			-- offset.pos = VecAdd(offset.pos, Vec((rnd2+rnd5)/400, (recoilAngle/-100)-(rnd1+rnd4)/400, 0))
-			-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(recoilAngle + (rnd1+rnd4)/4, (rnd2+rnd5)/4, (rnd3+rnd6)/4))
-
-			if lightTimer > 0 then
-				PointLight(toolPos, 1, 0.75, 0.25, (lightTimer/shotDelay)*lightFactor)
-				lightTimer = lightTimer - dt
-			end
-
-			if magoutTimer < 0 then
-				if inventoryenabled then
-					name = "mag0-glock-9x19"
-					maxammo = 17
-					id = mag
-					if id == "mag0-glock-9x19" then name, maxammo = "Glock", 17
-					elseif id == "mag1-glock-9x19" then name, maxammo = "Glock", 33
-					elseif id == "mag2-glock-9x19" then name, maxammo = "Glock", 50
-					elseif id == "mag3-glock-9x19" then name, maxammo = "Glock", 100
-					end
-					if mag ~= "none" then
-						SetString("inventory.pickup", mag.."_"..name.."_"..ammoleft.."_"..magtable2[1][3].."_9x19")
-					end
-					SetString("inventory.remove", magtable2[nextmagslot][4][1].."_"..magtable2[nextmagslot][4][2])
-					nextammo = magtable2[nextmagslot][2]
-					mag = magtable2[nextmagslot][1]
-				end
-
-				maginTimer = 0.6
-				magoutTimer = 0
-				reloadsound2playing = false
-			end
-			if maginTimer < 0 then
-				maginTimer = 0
-				if grenadelauncher then
-					PlaySound(uiselect, GetPlayerTransform().pos, 1)
-				end
-			end
-			if maginTimer < 0.3 and not reloadsound2playing and not grenadelauncher then
-					PlaySound(reloadsound2, GetPlayerTransform().pos, 0.7, false)
-					reloadsound2playing = true
-			end
-			if magoutTimer > 0 then
-				if grenadelauncher then
-					grenadeoffset = Vec(-0.025, -magoutTimer*3+0.025, -0.6)
-				else
-					magoffset = Vec(-0.025, -(0.6-magoutTimer)*4, -0.0125+(0.6-magoutTimer)*2)
-				end
-				magoutTimer = magoutTimer - dt/reloadFactor
-			end
-			if maginTimer > 0 then
-				if grenadelauncher then
-					grenadeoffset = Vec(-0.025, 0.025, -0.0125-maginTimer)
-				else
-					magoffset = Vec(-0.025, -maginTimer*4, -0.0125+maginTimer*2)
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
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.1, 0, -5, 10, -10
-					elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, -5, 10, 0
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.25, -0.1, 0, 20, -20, -20
-					end
-				elseif e then
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, -0.05, 0, 10, -10, 10
-					elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 5, -5, 0
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0, -0.05, 0, 10, -30, -5
-					end
-				else
-					if magoutTimer > 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.3, -0.05, 0, 0, 0, -20
-					elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) or (reloadTimer > 1 and ammo == 0) then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.5, 0.1, 0, 0, 0, -35
-					elseif reloadTimer < 0.8 and ammo == 0 then
-						x1, y1, z1, rotx1, roty1, rotz1 = 0.35, 0, 0.15, 10, 5, -10
-					end
-				end
-			else
-				if magoutTimer > 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.2, 0, 0.1, 10, -10, -20
-				elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, 0, 5, 10, -10
-				elseif reloadTimer < 0.8 and ammo == 0 then
-					x1, y1, z1, rotx1, roty1, rotz1 = 0.25, -0.05, 0, 10, 10, -5
-				end
-			end
-			end
-
-			-- RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
-			-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
-
-			if reloadTimer > 0.2 and reloading and ammo == 0 then
-				boltoffset = Vec(0, 0, 0.15)
-				holooffset = Vec(0, 0, 0.15)
-				holooffset2 = Vec(0, 0, 0)
-			elseif ammo == 0 and not reloading then
-				boltoffset = Vec(0, 0, 0.15)
-				holooffset = Vec(0, 0, 0.15)
-				holooffset2 = Vec(0, 0, 0)
-			end
-
-			ATToffset = {0,0,0,0,0,0}
-			if not GetBool("level.optionstriggered") then
-			-- if selectattachmentsTimer > 0 and selectattachments then
-			-- 	local t1 = (0.5 - selectattachmentsTimer)/0.5
-			-- 	offset.pos = VecAdd(offset.pos, Vec(1*t1, 0, -0.8*t1*180/GetInt("options.gfx.fov")))
-			-- 	offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t1, 75*t1, -10*t1))
-			-- elseif selectattachmentsTimer > 0 and not selectattachments then
-			-- 	local t2 = selectattachmentsTimer/0.25
-			-- 	offset.pos = VecAdd(offset.pos, Vec(1*t2, 0, -0.8*t2*180/GetInt("options.gfx.fov")))
-			-- 	offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t2, 75*t2, -10*t2))
-			-- elseif selectattachments then
-			-- 	offset.pos = VecAdd(offset.pos, Vec(1, 0, -0.8*180/GetInt("options.gfx.fov")))
-			-- 	offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10, 75, -10))
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
-			if inspectTimer > 4.5 then
-				x2, y2, z2, rotx2, roty2, rotz2 = -0.3, -0.4, 0.6, 40, 10, -10
-			elseif inspectTimer > 3 then
-				x2, y2, z2, rotx2, roty2, rotz2 = -0.65, -0.5, 0.65, 40, -10, 20
-			elseif inspectTimer > 1.25 then
-				x2, y2, z2, rotx2, roty2, rotz2 = 0.8, 0, -0.5, 10, 55, -10
-			elseif inspectTimer > 0 then
-				x2, y2, z2, rotx2, roty2, rotz2 = 0.25, -0.25, 0.25, 20, 30, 0
-			end
-
-			-- INSoffset = INS(inspectTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
-			-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
-			-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
-
-			local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
-			if selectfire == 0 and selectfireTimer <= 0 then
-				x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, -0.1, -20, 20, 10
-			elseif InputDown("shift") and selectfireTimer <= 0 and not reloading then
-				x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, -0.1, -20, 20, 10
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
-			for i = 15, 26 do
-				SetShapeLocalTransform(bs[i], hideTrans)
-			end
-			if clothingtype == "camo" then
-				hand1 = bs[18]
-				arm1 = bs[20]
-				hand2 = bs[19]
-			elseif clothingtype == "swat" then
-				hand1 = bs[21]
-				arm1 = bs[23]
-				hand2 = bs[22]
-			elseif clothingtype == "camo2" then
-				hand1 = bs[24]
-				arm1 = bs[26]
-				hand2 = bs[25]
-			else
-				hand1 = bs[15]
-				arm1 = bs[17]
-				hand2 = bs[16]
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
-				mag1 = shapes[13]
-				mag2 = shapes[14]
-				bolt = shapes[3]
-				selector = shapes[4]
-				suppressor = shapes[5]
-				holo = shapes[6]
-				holo2 = shapes[7]
-				muzzlebreak = shapes[8]
-				muzzlebreak2 = shapes[9]
-				side1 = shapes[11]
-				side2 = shapes[12]
-				barrel = shapes[10]
-
-				magTrans = GetShapeLocalTransform(mag0)
-				boltTrans = GetShapeLocalTransform(bolt)
-				selectorTrans = GetShapeLocalTransform(selector)
-				suppressorTrans = GetShapeLocalTransform(suppressor)
-				holoTrans = GetShapeLocalTransform(holo)
-				holoTrans2 = GetShapeLocalTransform(holo2)
-				muzzlebreakTrans = GetShapeLocalTransform(muzzlebreak)
-				muzzlebreakTrans2 = GetShapeLocalTransform(muzzlebreak2)
-				sideTrans1 = GetShapeLocalTransform(side1)
-				sideTrans2 = GetShapeLocalTransform(side2)
-				sideTrans3 = GetShapeLocalTransform(side3)
-				barrelTrans0 = GetShapeLocalTransform(barrel)
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
-			ht2.pos = VecAdd(ht.pos, holooffset2)
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
-			brt0 = TransformCopy(barrelTrans0)
-			brt0.pos = VecAdd(brt0.pos, barreloffset)
-
-			brt1 = TransformCopy(barrelTrans1)
-			brt1.pos = VecAdd(brt1.pos, barreloffset)
-
-			brt2 = TransformCopy(barrelTrans2)
-			brt2.pos = VecAdd(brt2.pos, barreloffset)
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
-			gdt2 = TransformCopy(guardTrans0)
-			gdt2.pos = VecAdd(gdt0.pos, guardoffset)
-			gdt2_2 = TransformCopy(guardTrans0)
-			gdt2_2.pos = VecAdd(gdt0.pos, guardoffset)
-
-			if reloading and ammo == 0 then
-				if q and ironsight then
-					if reloadTimer < 0.4 and reloadTimer > 0.2 then
-						bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(0.4-reloadTimer)/0.2))
-					elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
-						bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(reloadTimer-0.15)/0.05))
-					end
-				else
-					if reloadTimer < 0.4 and reloadTimer > 0.2 then
-						bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(0.4-reloadTimer)/0.2))
-					elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
-						bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(reloadTimer-0.15)/0.05))
-					end
-				end
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
-			if muzzle == "muzzle1" then
-				spt.pos = VecAdd(spt.pos, Vec(0.025, 0, 0))
-				lightFactor = 0.4
-				muzzlelength = 0.8
-			else
-				spt.pos = hidePos
-				spt.rot = QuatEuler(0, 0, 0)
-				lightFactor = 2
-				muzzleFactor = 1
-			end
-			if muzzle == "muzzle2" then
-				mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, 0))
-				mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0, 0))
-				mbt.rot = QuatEuler(-90, 0, 45)
-				lightFactor = 3
-				muzzleFactor = 0.85
-				muzzlelength = 0.2
-			else
-				mbt.pos = hidePos
-				mbt2.pos = hidePos
-				mbt.rot = QuatEuler(0, 0, 0)
-				lightFactor = 2
-				muzzleFactor = 1
-			end
-			if toprail == "scope" then
-				sct.pos = Vec(0.2, -0.375, -0.9)
-			else
-				sct.pos = hidePos
-			end
-			if toprail == "holo" then
-				if ammo > 0 then
-					ht.pos = VecAdd(ht.pos, Vec(0.025, 0, recoilTimer*2.5))
-					ht2.pos = VecAdd(ht2.pos, Vec(0.025, 0.075, -0.025+recoilTimer*2.5))
-				else
-					ht.pos = VecAdd(ht.pos, Vec(0.025, 0, 0))
-					ht2.pos = VecAdd(ht2.pos, Vec(0.025, 0.075, -0.025))
-				end
-			else
-				ht.pos = hidePos
-				ht2.pos = hidePos
-			end
-			if stock == "removed" then
-				stt.pos = Vec(0.5, -1, -1.5)
-				stt.rot = QuatEuler(-90, -180, 0)
-				stockFactor = 2.5
-			else
-				stt.pos = Vec(0.2, -1, 0.5)
-				stt.rot = QuatEuler(-90, 0, 0)
-				stockFactor = 1
-			end
-			rt.pos = Vec(0.175, -0.725, -0.85)
-
-			brt0.pos = VecAdd(brt0.pos, Vec(-0.025, -0.025, 0.005))
-
-			if mag == "" or mag == "mag0-glock-9x19" then
-				magsize = 17
-				reloadFactor = 1.25
-				SetShapeLocalTransform(mag0, Transform(VecAdd(mt.pos, Vec(0, 0, 0)), mt.rot))
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-			elseif mag == "mag1-glock-9x19" then
-				magsize = 33
-				reloadFactor = 1.5
-				SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(0, -0.25, 0.1)), mt.rot))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-			elseif mag == "mag2-glock-9x19" then
-				magsize = 50
-				reloadFactor = 1.7
-				SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.1, -0.35, -0.05)), mt.rot))
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag1, hideTrans)
-			elseif mag == "none" then
-				SetShapeLocalTransform(mag0, hideTrans)
-				SetShapeLocalTransform(mag1, hideTrans)
-				SetShapeLocalTransform(mag2, hideTrans)
-			end
-
-			if side == "side1" then
-				sdt1.pos = sdt1.pos
-			else
-				sdt1.pos = hidePos
-			end
-			if side == "side2" then
-				sdt2.pos = VecAdd(sdt2.pos, Vec(0.025, 0, 0))
-			else
-				sdt2.pos = hidePos
-			end
-			if side == "side3" then
-				sdt3.pos = sdt3.pos
-			else
-				sdt3.pos = hidePos
-			end
-
-			if mag == "mag2-glock-9x19" or mag == "mag3" then
-				SetString("savegame.mod.stock", "")
-			end
-
-			if guard == "" then
-				gdt0.pos = Vec(0.225, -0.625, -1.75)
-				gdt0_2.pos = Vec(0.2, -0.7, -1.75)
-				guardlength = 0
-			else
-				gdt0.pos = hidePos
-				gdt0_2.pos = hidePos
-			end
-			if guard == "guard1" then
-				gdt1.pos = Vec(0.225, -0.625, -1.75)
-				gdt1_2.pos = Vec(0.2, -0.7, -1.75)
-				guardlength = -0.2
-			else
-				gdt1.pos = hidePos
-				gdt1_2.pos = hidePos
-			end
-			if guard == "guard2" then
-				gdt2.pos = Vec(0.225, -0.725, -1.75)
-				gdt2_2.pos = Vec(0.2, -0.7, -1.75)
-				guardlength = 0.3
-			else
-				gdt2.pos = hidePos
-				gdt2_2.pos = hidePos
-			end
-			accuracyFactor = 1.5
-
-			SetShapeLocalTransform(barrel, brt0)
-			SetShapeLocalTransform(bolt, bt)
-			SetShapeLocalTransform(selector, st)
-			SetShapeLocalTransform(suppressor, spt)
-			SetShapeLocalTransform(holo, ht)
-			SetShapeLocalTransform(holo2, ht2)
-			SetShapeLocalTransform(muzzlebreak, mbt)
-			SetShapeLocalTransform(muzzlebreak2, mbt2)
-			SetShapeLocalTransform(side1, sdt1)
-			SetShapeLocalTransform(side2, sdt2)
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
-				if not realistic and (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) and not jammed then
-					Reload()
-					inspectTimer = 0
-				end
-			end
-
-			if (InputReleased(reloadKey) or clickedmag) and selectfireTimer == 0 and not jammed then
-				if realistic and curmagslot ~= nextmagslot and magcheckTimer == 0 then
-					Reload()
-					inspectTimer = 0
-				end
-			end
-			
-			if GetBool("ammobox.refill") then
-				SetBool("ammobox.refill", false)
-				PlaySound(refillsound, GetPlayerTransform().pos, 1, false)
-			end
-
-			if reloading then
-				if reloadTimer > 0.4 then
-					reloadTimer = reloadTimer - dt/reloadFactor*1.25
-				elseif reloadTimer > 0 then
-					reloadTimer = reloadTimer - dt
-				end
-				if reloadTimer < 0.4 and not cocksoundplaying and ammo == 0 then
-					cocksoundplaying = true
-					PlaySound(cocksound, GetPlayerTransform().pos, 0.45)
-				end
-				if reloadTimer < 0 then
-					cocksoundplaying = false
-					if grenadelauncher then
-						grenadelauncherammo = 1
-					else
-						if inventoryenabled then
-							if ammo == 0 then
-								ammo = nextammo
-							else
-								ammo = nextammo + 1
-							end
-							name = "mag0-glock-9x19"
-							maxammo = 17
-							id = mag
-							if id == "mag0-glock-9x19" then name, maxammo = "Glock", 17
-							elseif id == "mag1-glock-9x19" then name, maxammo = "Glock", 33
-							elseif id == "mag2-glock-9x19" then name, maxammo = "Glock", 50
-							elseif id == "mag3-glock-9x19" then name, maxammo = "Glock", 100
-							end
-							local guninfo = Split(GetString("inventory.guns2"), "_")
-							if #guninfo == 8 then
-								SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19_"..guninfo[8])
-							else
-								SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19")
-							end
-							SetBool("inventory.update", true)
-							curmagslot = 1
-						elseif realistic then
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
-		local x2, y2, z2, rotx2, roty2, rotz2 = 0.15, -0.95, -0.85, 0, 0, 0
-		if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.2 then
-			x2, y2, z2, rotx2, roty2, rotz2 = 0.1, -0.7, -0.2+bt.pos[3], 0, 0, 0
-		elseif reloading then
-			x2, y2, z2, rotx2, roty2, rotz2 = -0.1+mt.pos[1], 0.05+mt.pos[2], -0.2+mt.pos[3], 0, 0, 0
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
-		sightattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.15, -0.6))
-		muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.35, -1.6))
-		stockattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.4, -0.6))
-		sideattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.6, -1.25))
-		magattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.85, -0.5))
-		gripattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.85, -1.4-guardlength))
-		barrelattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.65, -1.6))
-		guardattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.25, -1.5))
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
-	if GetString("game.player.tool") == "g17" and GetPlayerVehicle() == 0 then
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
-	if GetString("game.player.tool") == "g17" and grenadelauncher and not selectattachments then
-		UiPush()
-			UiTranslate(UiCenter(), UiMiddle())
-			UiAlign("center middle")
-			UiImage("ui/hud/crosshair-launcher.png")
-		UiPop()
-	end
-	if GetString("game.player.tool") == "g17" and sideattachment and side == "side3" then
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
-	if realistic and selectmag and GetString("game.player.tool") == "g17" then
-		hoverindex=0
-		UiPush()
-			local x,y,dist=UiWorldToPixel(VecAdd(magattachpoint, Vec(0, 0.3, 0)))
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
-	if selectattachments and GetString("game.player.tool") == "g17" and GetPlayerVehicle() == 0 then
-	if hint then drawHint(info) end
-	hoverindex=0
-		UiPush()
-			local x,y,dist=UiWorldToPixel(sightattachpoint)
-			if dist > 0 then
-				UiTranslate(x-50,y+20)
-				local curx,cury=UiGetRelativePos()
-				UiPush()
-					UiAlign("center middle")
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
-					clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Compensator","Reduces horizontal recoil, but turns your barrel into a flashbang."})
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
-					clickedmag1 = AttachmentButton("mag","mag1-glock-9x19",true,{curx,cury},{"33rnd Mag","Pew Pew Pew"})
-					UiTranslate(-70,0)
-					curx,cury=curx-70,cury
-					clickedmag2 = AttachmentButton("mag","mag2-glock-9x19",true,{curx,cury},{"50rnd Drum","Pew Pew Pew Pew Pew Pew"})
-					UiTranslate(-70,0)
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
-				UiPop()
-			end
-		UiPop()
-	end
 end
 
 function round(number, decimals)
@@ -2636,4 +969,1644 @@
         table.insert(result, match);
     end
     return result;
-end+end
+
+function server.init()
+    conversion = GetString("savegame.mod.conversion")
+    if conversion == "" then
+    	conversion = "Semi"
+    end
+    gunname = "Glock 17"
+    if conversion == Full then
+    	gunname = "Glock 18"
+    end
+    RegisterTool("g17", "Glock 17", "MOD/vox/g17.vox", 3)
+    SetBool("game.tool.g17.enabled", true, true)
+    SetFloat("game.tool.g17.ammo", 101, true)
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
+    damage = 0.11 * GetInt("savegame.mod.damage")/100
+    if damage == 0 then
+    	damage = 0.11
+    end
+    gravity = Vec(0, -10, 0)
+    hidePos = Vec(0, -200, 0)
+    hideTrans = Transform(hidePos,QuatEuler())
+    velocity = 320
+    drag = 2
+    maxMomentum = 1.5
+    tracer = false
+    recoilVertical = 0.8
+    recoilHorizontal = 0.7
+    recoilWander = 3.5
+    lvl5armor = 0
+    lvl4armor = 0.05
+    lvl3armor = 0.15
+    lvl2armor = 0.5
+    lvl1armor = 0.7
+    inside = {}
+    for i = 1,50 do
+    	inside[i] = {0,0,0,0}
+    end
+    hoverindex = 0
+    toprail = GetString("savegame.mod.toprail")
+    muzzle = GetString("savegame.mod.muzzle")
+    stock = GetString("savegame.mod.stock")
+    realistic = GetBool("savegame.mod.realistic")
+    --realistic = true
+    --inventoryenabled = true
+    --magazine system
+    mslot1 = GetString("savegame.mod.mslot1")
+    mslot2 = GetString("savegame.mod.mslot2")
+    mslot3 = GetString("savegame.mod.mslot3")
+    mslot4 = GetString("savegame.mod.mslot4")
+    mslot5 = GetString("savegame.mod.mslot5")
+    mslot6 = GetString("savegame.mod.mslot6")
+    mslot7 = GetString("savegame.mod.mslot7")
+    mslot8 = GetString("savegame.mod.mslot8")
+    if inventoryenabled then
+    	magtable2 = {}
+    	local guninfo = Split(GetString("inventory.guns2"), "_")
+    	magtable2[1] = {guninfo[3], tonumber(guninfo[5]), tonumber(guninfo[6]), {1,1}}
+    	for i = 1, 8 do
+    		for j = 1, 15 do
+    			if GetString("inventory.backpack"..i.."_"..j) ~= "" then
+    				local maginfo = Split(GetString("inventory.backpack"..i.."_"..j), "_")
+    				local magtype, magammo, magammomax = maginfo[1], maginfo[3], maginfo[4]
+    				if string.sub(magtype, 1, 3) == "mag" and string.sub(magtype, 6, 11) == "glock-9x19" then
+    					table.insert(magtable2, {magtype,tonumber(magammo),tonumber(magammomax),{i,j}})
+    				end
+    			end
+    		end
+    	end
+    	totalmags = #magtable2
+    else
+    	if totalmags == 0 then
+    		mslot1, mslot2 = "mag0", "mag0"
+    		SetString("savegame.mod.mslot1", "mag0", true)
+    		SetString("savegame.mod.mslot2", "mag0", true)
+    	totalmags = 2
+    	end
+    	magtable2 = {{mslot1,0,0},{mslot2,0,0},{mslot3,0,0},{mslot4,0,0},{mslot5,0,0},{mslot6,0,0},{mslot7,0,0},{mslot8,0,0}}
+    	for i=1,8 do
+    		local magslottype = GetString("savegame.mod.mslot"..i)
+    		if magslottype == "mag0" then
+    			magtable2[i][2] = 30
+    			magtable2[i][3] = 30
+    		elseif magslottype == "mag1" then
+    			magtable2[i][2] = 40
+    			magtable2[i][3] = 40
+    		elseif magslottype == "mag2" then
+    			magtable2[i][2] = 60
+    			magtable2[i][3] = 60
+    		elseif magslottype == "mag3" then
+    			magtable2[i][2] = 100
+    			magtable2[i][3] = 100
+    		else
+    			magtable2[i][2] = 20
+    			magtable2[i][3] = 20
+    		end
+    	end
+    end
+    curmagslot = 1
+    nextmagslot = 2
+    if inventoryenabled then
+    	local guninfo = Split(GetString("inventory.guns2"), "_")
+    	mag = guninfo[3]
+    	reloadFactor = 1
+    elseif realistic then
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
+    if inventoryenabled then
+    	item = GetString("inventory.guns2")
+    	guninfo = Split(item, "_")
+    	if #guninfo == 8 then
+    		attachmentinfo = Split(guninfo[8], "-")
+    		toprail = attachmentinfo[1]
+    		canted = attachmentinfo[2]
+    		muzzle = attachmentinfo[3]
+    		stock = attachmentinfo[4]
+    		grip = attachmentinfo[5]
+    		barrel = attachmentinfo[6]
+    		side = attachmentinfo[7]
+    		guard = attachmentinfo[8]
+    		magnifier = attachmentinfo[9]
+    	else
+    		toprail = ""
+    		canted = ""
+    		muzzle = ""
+    		stock = ""
+    		grip = ""
+    		barrel = ""
+    		side = ""
+    		guard = ""
+    		magnifier = ""
+    	end
+    end
+    reloadTime = 2.4
+    shotDelay = 0.05
+    spreadTimer = 1.25
+    spreadFactor = 1.5
+    accuracyFactor = 1
+    if not realistic then
+    	if mag == "" or mag == "mag0-glock-9x19" then
+    		magsize = 17
+    		reloadFactor = 1
+    	elseif mag == "mag1-glock-9x19" then
+    		magsize = 33
+    		reloadFactor = 1.15
+    	elseif mag == "mag2-glock-9x19" then
+    		magsize = 50
+    		reloadFactor = 1.35
+    	else
+    		magsize = 17
+    		reloadFactor = 1
+    	end
+    	ammo = magsize
+    else
+    	if not inventoryenabled then
+    		ammo = magtable2[curmagslot][2]
+    	else
+    		ammo = magtable2[1][2]
+    	end
+    end
+    if inventoryenabled then
+    	initammo = false
+    end
+    ammoleft = 0
+    maxammoleft = 0
+    nextammo = 0
+    reloadFactor = 1
+    barrellength = 0
+    guardlength = 0
+    barrelFactorx = 0.8
+    barrelFactory = 1
+    barrelFactordamage = 1.25
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
+    e = false
+    q = false
+    selectfire = 1
+    selectfire0 = 0
+    selectfireTimer = 0
+    selectfireText = conversion
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
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if inventoryenabled and not reloading then
+        	item = GetString("inventory.guns2")
+        	if Split(item, "_")[1] == "g17" then
+        		guninfo = Split(item, "_")
+        		if GetBool("inventory.update_guns2") or not initammo then
+        			ammo = tonumber(guninfo[5])
+        			mag = guninfo[3]
+        			SetBool("inventory.update_guns2", false, true)
+        			initammo = true
+        		end
+        	end
+        end
+        if inventoryenabled then
+        	magtable2 = {}
+        	local guninfo = Split(GetString("inventory.guns2"), "_")
+        	magtable2[1] = {guninfo[3], tonumber(guninfo[5]), tonumber(guninfo[6]), {1,1}}
+        	for i = 1, 8 do
+        		for j = 1, 15 do
+        			if GetString("inventory.backpack"..i.."_"..j) ~= "" then
+        				local maginfo = Split(GetString("inventory.backpack"..i.."_"..j), "_")
+        				local magtype, magammo, magammomax = maginfo[1], maginfo[3], maginfo[4]
+        				if string.sub(magtype, 1, 3) == "mag" and string.sub(magtype, 6, 15) == "glock-9x19" then
+        					table.insert(magtable2, {magtype,tonumber(magammo),tonumber(magammomax),{i,j}})
+        				end
+        			end
+        		end
+        	end
+        	totalmags = #magtable2
+        	if nextmagslot > totalmags then
+        		nextmagslot = 1
+        	end
+        end
+    end
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
+    if GetString("game.player.tool") == "g17" and GetPlayerVehicle(playerId) == 0 then
+    	SetBool("hud.aimdot", false, true)
+
+    	------CONTROLS------
+    	if InputDown("lmb") and not reloading and selectfire == 1 and conversion == "Full" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 and not selectmag then
+    		if ammo ~= 0 then
+    			Shoot()
+    		end
+    	elseif InputPressed("lmb") and not reloading and selectfire == 1 and conversion == "Semi" and not selectattachments and selectfireTimer == 0 and GetPlayerGrabShape(playerId) == 0 and not InputDown("shift") and inspectTimer <= 0 and not selectmag then
+    		if ammo ~= 0 then
+    			Shoot()
+    			shootTimer = 0.05
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
+    	if selectfire == 0  and selectfireTimer <= 0 then
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
+    		inspectTimer = 0
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
+    	if InputDown(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 and not realistic or GetBool("level.optionstriggered") then
+    		if InputPressed(attachmentsKey) and not GetBool("level.optionstriggered") then
+    			PlaySound(interactsound2, GetPlayerTransform(playerId).pos, 1)
+    			selectattachmentsTimer = 0.5
+    		end
+    		UiMakeInteractive()
+    		selectattachments = true
+    		ironsight = false
+    		inspectTimer = 0
+    	end
+    	if InputReleased(attachmentsKey) and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and not realistic then
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
+
+    	if InputPressed(magcheckKey) and realistic and not reloading and selectfire > 0 and selectfireTimer <= 0 and not InputDown("shift") and magcheckTimer == 0 and jamclearTimer == 0 then
+    		magcheckTimer = 4
+    		PlaySound(reloadsound, GetPlayerTransform(playerId).pos, 0.5)
+    		inspectTimer = 0
+    	end
+    	if magcheckTimer ~= 0 then
+    		magcheckTimer = magcheckTimer - dt*1.5
+    		ironsight = false
+    	end
+    	if magcheckTimer < 0 then
+    		magcheckTimer = 0
+    		PlaySound(reloadsound2, GetPlayerTransform(playerId).pos, 0.5)
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
+    		for i = 1, totalmags do
+    			if magtable2[i][2] > magtable2[nextmagslot][2] and i ~= curmagslot then
+    				nextmagslot = i
+    			end
+    		end
+    		inspectTimer = 0
+    		Reload()
+    	end
+    	if InputReleased(reloadKey) then heldrTimer = 0 end
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
+    	if InputPressed("y") and not reloading and not InputDown("shift") and selectfireTimer <= 0 and not ironsight and selectfire ~= 0 then
+    		if inspectTimer <= 0 then
+    			inspectTimer = 6
+    			ironsight = false
+    		else
+    			inspectTimer = 0
+    		end
+    	end
+
+    	if selectfire == 1 then
+    		selectfireText = conversion
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
+    		recoilFactor = recoilVertical
+    	else
+    		recoilFactor = recoilVertical*1.75
+    	end
+
+    	if ironsight then
+    		recoilMax = 8*muzzleFactor
+    	else
+    		recoilMax = 20*muzzleFactor
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
+    	if realistic or inventoryenabled then
+    		if maginTimer ~= 0 then
+    			if totalmags == 0 then
+    				mag = "none"
+    				maginTimer = 0
+    			elseif not inventoryenabled then
+    				mag = magtable2[curmagslot][1]
+    			end
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
+
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		local magoffset = Vec(-0.025, 0, -0.0125)
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
+    		x,y,z,rotx,roty,rotz = -0.2,0.35,-0.5,0,0,0
+    		if ironsight then
+    		if grenadelauncher then
+    			x = 0
+    			y = 0.45
+    			z = -0.4
+    			rotz = 0
+    		elseif q then
+    			x = 0.9
+    			y = 0.1
+    			z = -0.4
+    			rotz = 30
+    		elseif e then
+    			x = -0.3
+    			y = 0.4
+    			z = -0.4
+    			rotz = -15
+    		else
+    			if toprail == "holo" then
+    				x = 0.275
+    				y = 0.4375
+    				z = -0.45
+    				rotz = 0
+    			elseif toprail == "" then
+    				x = 0.275
+    				y = 0.5
+    				z = -0.45
+    				rotz = 0
+    			elseif toprail == "scope" then
+    				x = 0.275
+    				y = 0.4
+    				z = 0.25
+    				rotz = -0.25
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
+    			if toprail == "holo" then
+    				local gt = GetBodyTransform(GetToolBody())
+    				local sightcenter = Vec(0.275, -0.4375, -0.7)
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
+    		-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(math.sin(2.1*GetTime())/9,  math.sin(1.3*GetTime())/6, 0))
+    		-- offset.pos = VecAdd(offset.pos, Vec(math.sin(1.1*GetTime())/360,  math.sin(0.7*GetTime())/240, 0))
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
+    			recoilTimer = recoilTimer - dt
+    			boltoffset = Vec(0, 0, recoilTimer*2.5)
+    		end
+    		if recoilTimer2 ~= 0 then
+    			recoilTimer2 = recoilTimer2 - (recoilTimer2*0.1+dt)
+    			-- offset.pos = VecAdd(offset.pos, Vec(0, -recoilTimer2/2, recoilTimer2))
+    			-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(recoilTimer2*40, 0, 0))
+    		end
+    		local rx, ry, rz, rr1, rr2, rr3 = (rnd2+rnd5)/400, (recoilAngle/-100)-(rnd1+rnd4)/400-recoilTimer2/2, recoilTimer2, recoilAngle + (rnd1+rnd4)/4+recoilTimer2*40, (rnd2+rnd5)/4, (rnd3+rnd6)/4
+    		-- RECoffset = REC(true, rx, ry, rz, rr1, rr2, rr3)
+    		-- offset.pos = VecAdd(offset.pos, Vec((rnd2+rnd5)/400, (recoilAngle/-100)-(rnd1+rnd4)/400, 0))
+    		-- offset.rot = QuatRotateQuat(offset.rot, QuatEuler(recoilAngle + (rnd1+rnd4)/4, (rnd2+rnd5)/4, (rnd3+rnd6)/4))
+
+    		if lightTimer ~= 0 then
+    			PointLight(toolPos, 1, 0.75, 0.25, (lightTimer/shotDelay)*lightFactor)
+    			lightTimer = lightTimer - dt
+    		end
+
+    		if magoutTimer < 0 then
+    			if inventoryenabled then
+    				name = "mag0-glock-9x19"
+    				maxammo = 17
+    				id = mag
+    				if id == "mag0-glock-9x19" then name, maxammo = "Glock", 17
+    				elseif id == "mag1-glock-9x19" then name, maxammo = "Glock", 33
+    				elseif id == "mag2-glock-9x19" then name, maxammo = "Glock", 50
+    				elseif id == "mag3-glock-9x19" then name, maxammo = "Glock", 100
+    				end
+    				if mag ~= "none" then
+    					SetString("inventory.pickup", mag.."_"..name.."_"..ammoleft.."_"..magtable2[1][3].."_9x19", true)
+    				end
+    				SetString("inventory.remove", magtable2[nextmagslot][4][1].."_"..magtable2[nextmagslot][4][2], true)
+    				nextammo = magtable2[nextmagslot][2]
+    				mag = magtable2[nextmagslot][1]
+    			end
+
+    			maginTimer = 0.6
+    			magoutTimer = 0
+    			reloadsound2playing = false
+    		end
+    		if maginTimer < 0 then
+    			maginTimer = 0
+    			if grenadelauncher then
+    				PlaySound(uiselect, GetPlayerTransform(playerId).pos, 1)
+    			end
+    		end
+    		if maginTimer < 0.3 and not reloadsound2playing and not grenadelauncher then
+    				PlaySound(reloadsound2, GetPlayerTransform(playerId).pos, 0.7, false)
+    				reloadsound2playing = true
+    		end
+    		if magoutTimer ~= 0 then
+    			if grenadelauncher then
+    				grenadeoffset = Vec(-0.025, -magoutTimer*3+0.025, -0.6)
+    			else
+    				magoffset = Vec(-0.025, -(0.6-magoutTimer)*4, -0.0125+(0.6-magoutTimer)*2)
+    			end
+    			magoutTimer = magoutTimer - dt/reloadFactor
+    		end
+    		if maginTimer ~= 0 then
+    			if grenadelauncher then
+    				grenadeoffset = Vec(-0.025, 0.025, -0.0125-maginTimer)
+    			else
+    				magoffset = Vec(-0.025, -maginTimer*4, -0.0125+maginTimer*2)
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
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.1, 0.1, 0, -5, 10, -10
+    				elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, -5, 10, 0
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.25, -0.1, 0, 20, -20, -20
+    				end
+    			elseif e then
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, -0.05, 0, 10, -10, 10
+    				elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, 0, 0, 5, -5, 0
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0, -0.05, 0, 10, -30, -5
+    				end
+    			else
+    				if magoutTimer ~= 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.3, -0.05, 0, 0, 0, -20
+    				elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) or (reloadTimer > 1 and ammo == 0) then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.5, 0.1, 0, 0, 0, -35
+    				elseif reloadTimer < 0.8 and ammo == 0 then
+    					x1, y1, z1, rotx1, roty1, rotz1 = 0.35, 0, 0.15, 10, 5, -10
+    				end
+    			end
+    		else
+    			if magoutTimer ~= 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.2, 0, 0.1, 10, -10, -20
+    			elseif maginTimer > 0 or (reloadTimer > 0 and ammo > 0) then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.15, 0, 0, 5, 10, -10
+    			elseif reloadTimer < 0.8 and ammo == 0 then
+    				x1, y1, z1, rotx1, roty1, rotz1 = 0.25, -0.05, 0, 10, 10, -5
+    			end
+    		end
+    		end
+
+    		-- RELoffset = REL(reloading, x1, y1, z1, rotx1, roty1, rotz1)
+    		-- offset.pos = VecAdd(offset.pos, RELoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, RELoffset.rot)
+
+    		if reloadTimer > 0.2 and reloading and ammo == 0 then
+    			boltoffset = Vec(0, 0, 0.15)
+    			holooffset = Vec(0, 0, 0.15)
+    			holooffset2 = Vec(0, 0, 0)
+    		elseif ammo == 0 and not reloading then
+    			boltoffset = Vec(0, 0, 0.15)
+    			holooffset = Vec(0, 0, 0.15)
+    			holooffset2 = Vec(0, 0, 0)
+    		end
+
+    		ATToffset = {0,0,0,0,0,0}
+    		if not GetBool("level.optionstriggered") then
+    		-- if selectattachmentsTimer > 0 and selectattachments then
+    		-- 	local t1 = (0.5 - selectattachmentsTimer)/0.5
+    		-- 	offset.pos = VecAdd(offset.pos, Vec(1*t1, 0, -0.8*t1*180/GetInt("options.gfx.fov")))
+    		-- 	offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t1, 75*t1, -10*t1))
+    		-- elseif selectattachmentsTimer > 0 and not selectattachments then
+    		-- 	local t2 = selectattachmentsTimer/0.25
+    		-- 	offset.pos = VecAdd(offset.pos, Vec(1*t2, 0, -0.8*t2*180/GetInt("options.gfx.fov")))
+    		-- 	offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10*t2, 75*t2, -10*t2))
+    		-- elseif selectattachments then
+    		-- 	offset.pos = VecAdd(offset.pos, Vec(1, 0, -0.8*180/GetInt("options.gfx.fov")))
+    		-- 	offset.rot = QuatRotateQuat(offset.rot, QuatEuler(10, 75, -10))
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
+    		if inspectTimer > 4.5 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = -0.3, -0.4, 0.6, 40, 10, -10
+    		elseif inspectTimer > 3 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = -0.65, -0.5, 0.65, 40, -10, 20
+    		elseif inspectTimer > 1.25 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = 0.8, 0, -0.5, 10, 55, -10
+    		elseif inspectTimer ~= 0 then
+    			x2, y2, z2, rotx2, roty2, rotz2 = 0.25, -0.25, 0.25, 20, 30, 0
+    		end
+
+    		-- INSoffset = INS(inspectTimer > 0, x2, y2, z2, rotx2, roty2, rotz2)
+    		-- offset.pos = VecAdd(offset.pos, INSoffset.pos)
+    		-- offset.rot = QuatRotateQuat(offset.rot, INSoffset.rot)
+
+    		local x3, y3, z3, rotx3, roty3, rotz3 = 0, 0, 0, 0, 0, 0
+    		if selectfire == 0 and selectfireTimer <= 0 then
+    			x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, -0.1, -20, 20, 10
+    		elseif InputDown("shift") and selectfireTimer <= 0 and not reloading then
+    			x3, y3, z3, rotx3, roty3, rotz3 = -0.25, -0.1, -0.1, -20, 20, 10
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
+    		for i = 15, 26 do
+    			SetShapeLocalTransform(bs[i], hideTrans)
+    		end
+    		if clothingtype == "camo" then
+    			hand1 = bs[18]
+    			arm1 = bs[20]
+    			hand2 = bs[19]
+    		elseif clothingtype == "swat" then
+    			hand1 = bs[21]
+    			arm1 = bs[23]
+    			hand2 = bs[22]
+    		elseif clothingtype == "camo2" then
+    			hand1 = bs[24]
+    			arm1 = bs[26]
+    			hand2 = bs[25]
+    		else
+    			hand1 = bs[15]
+    			arm1 = bs[17]
+    			hand2 = bs[16]
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
+    			mag1 = shapes[13]
+    			mag2 = shapes[14]
+    			bolt = shapes[3]
+    			selector = shapes[4]
+    			suppressor = shapes[5]
+    			holo = shapes[6]
+    			holo2 = shapes[7]
+    			muzzlebreak = shapes[8]
+    			muzzlebreak2 = shapes[9]
+    			side1 = shapes[11]
+    			side2 = shapes[12]
+    			barrel = shapes[10]
+
+    			magTrans = GetShapeLocalTransform(mag0)
+    			boltTrans = GetShapeLocalTransform(bolt)
+    			selectorTrans = GetShapeLocalTransform(selector)
+    			suppressorTrans = GetShapeLocalTransform(suppressor)
+    			holoTrans = GetShapeLocalTransform(holo)
+    			holoTrans2 = GetShapeLocalTransform(holo2)
+    			muzzlebreakTrans = GetShapeLocalTransform(muzzlebreak)
+    			muzzlebreakTrans2 = GetShapeLocalTransform(muzzlebreak2)
+    			sideTrans1 = GetShapeLocalTransform(side1)
+    			sideTrans2 = GetShapeLocalTransform(side2)
+    			sideTrans3 = GetShapeLocalTransform(side3)
+    			barrelTrans0 = GetShapeLocalTransform(barrel)
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
+    		ht2.pos = VecAdd(ht.pos, holooffset2)
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
+    		brt0 = TransformCopy(barrelTrans0)
+    		brt0.pos = VecAdd(brt0.pos, barreloffset)
+
+    		brt1 = TransformCopy(barrelTrans1)
+    		brt1.pos = VecAdd(brt1.pos, barreloffset)
+
+    		brt2 = TransformCopy(barrelTrans2)
+    		brt2.pos = VecAdd(brt2.pos, barreloffset)
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
+    		gdt2 = TransformCopy(guardTrans0)
+    		gdt2.pos = VecAdd(gdt0.pos, guardoffset)
+    		gdt2_2 = TransformCopy(guardTrans0)
+    		gdt2_2.pos = VecAdd(gdt0.pos, guardoffset)
+
+    		if reloading and ammo == 0 then
+    			if q and ironsight then
+    				if reloadTimer < 0.4 and reloadTimer > 0.2 then
+    					bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(0.4-reloadTimer)/0.2))
+    				elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
+    					bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, -90*(reloadTimer-0.15)/0.05))
+    				end
+    			else
+    				if reloadTimer < 0.4 and reloadTimer > 0.2 then
+    					bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(0.4-reloadTimer)/0.2))
+    				elseif reloadTimer < 0.2 and reloadTimer > 0.15 then
+    					bt2.rot = QuatRotateQuat(bt2.rot, QuatEuler(0, 0, 90*(reloadTimer-0.15)/0.05))
+    				end
+    			end
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
+    		if muzzle == "muzzle1" then
+    			spt.pos = VecAdd(spt.pos, Vec(0.025, 0, 0))
+    			lightFactor = 0.4
+    			muzzlelength = 0.8
+    		else
+    			spt.pos = hidePos
+    			spt.rot = QuatEuler(0, 0, 0)
+    			lightFactor = 2
+    			muzzleFactor = 1
+    		end
+    		if muzzle == "muzzle2" then
+    			mbt.pos = VecAdd(mbt.pos, Vec(0.075, -0.05, 0))
+    			mbt2.pos = VecAdd(mbt2.pos, Vec(0, 0, 0))
+    			mbt.rot = QuatEuler(-90, 0, 45)
+    			lightFactor = 3
+    			muzzleFactor = 0.85
+    			muzzlelength = 0.2
+    		else
+    			mbt.pos = hidePos
+    			mbt2.pos = hidePos
+    			mbt.rot = QuatEuler(0, 0, 0)
+    			lightFactor = 2
+    			muzzleFactor = 1
+    		end
+    		if toprail == "scope" then
+    			sct.pos = Vec(0.2, -0.375, -0.9)
+    		else
+    			sct.pos = hidePos
+    		end
+    		if toprail == "holo" then
+    			if ammo ~= 0 then
+    				ht.pos = VecAdd(ht.pos, Vec(0.025, 0, recoilTimer*2.5))
+    				ht2.pos = VecAdd(ht2.pos, Vec(0.025, 0.075, -0.025+recoilTimer*2.5))
+    			else
+    				ht.pos = VecAdd(ht.pos, Vec(0.025, 0, 0))
+    				ht2.pos = VecAdd(ht2.pos, Vec(0.025, 0.075, -0.025))
+    			end
+    		else
+    			ht.pos = hidePos
+    			ht2.pos = hidePos
+    		end
+    		if stock == "removed" then
+    			stt.pos = Vec(0.5, -1, -1.5)
+    			stt.rot = QuatEuler(-90, -180, 0)
+    			stockFactor = 2.5
+    		else
+    			stt.pos = Vec(0.2, -1, 0.5)
+    			stt.rot = QuatEuler(-90, 0, 0)
+    			stockFactor = 1
+    		end
+    		rt.pos = Vec(0.175, -0.725, -0.85)
+
+    		brt0.pos = VecAdd(brt0.pos, Vec(-0.025, -0.025, 0.005))
+
+    		if mag == "" or mag == "mag0-glock-9x19" then
+    			magsize = 17
+    			reloadFactor = 1.25
+    			SetShapeLocalTransform(mag0, Transform(VecAdd(mt.pos, Vec(0, 0, 0)), mt.rot))
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    		elseif mag == "mag1-glock-9x19" then
+    			magsize = 33
+    			reloadFactor = 1.5
+    			SetShapeLocalTransform(mag1, Transform(VecAdd(mt.pos, Vec(0, -0.25, 0.1)), mt.rot))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    		elseif mag == "mag2-glock-9x19" then
+    			magsize = 50
+    			reloadFactor = 1.7
+    			SetShapeLocalTransform(mag2, Transform(VecAdd(mt.pos, Vec(-0.1, -0.35, -0.05)), mt.rot))
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag1, hideTrans)
+    		elseif mag == "none" then
+    			SetShapeLocalTransform(mag0, hideTrans)
+    			SetShapeLocalTransform(mag1, hideTrans)
+    			SetShapeLocalTransform(mag2, hideTrans)
+    		end
+
+    		if side == "side1" then
+    			sdt1.pos = sdt1.pos
+    		else
+    			sdt1.pos = hidePos
+    		end
+    		if side == "side2" then
+    			sdt2.pos = VecAdd(sdt2.pos, Vec(0.025, 0, 0))
+    		else
+    			sdt2.pos = hidePos
+    		end
+    		if side == "side3" then
+    			sdt3.pos = sdt3.pos
+    		else
+    			sdt3.pos = hidePos
+    		end
+
+    		if mag == "mag2-glock-9x19" or mag == "mag3" then
+    			SetString("savegame.mod.stock", "", true)
+    		end
+
+    		if guard == "" then
+    			gdt0.pos = Vec(0.225, -0.625, -1.75)
+    			gdt0_2.pos = Vec(0.2, -0.7, -1.75)
+    			guardlength = 0
+    		else
+    			gdt0.pos = hidePos
+    			gdt0_2.pos = hidePos
+    		end
+    		if guard == "guard1" then
+    			gdt1.pos = Vec(0.225, -0.625, -1.75)
+    			gdt1_2.pos = Vec(0.2, -0.7, -1.75)
+    			guardlength = -0.2
+    		else
+    			gdt1.pos = hidePos
+    			gdt1_2.pos = hidePos
+    		end
+    		if guard == "guard2" then
+    			gdt2.pos = Vec(0.225, -0.725, -1.75)
+    			gdt2_2.pos = Vec(0.2, -0.7, -1.75)
+    			guardlength = 0.3
+    		else
+    			gdt2.pos = hidePos
+    			gdt2_2.pos = hidePos
+    		end
+    		accuracyFactor = 1.5
+
+    		SetShapeLocalTransform(barrel, brt0)
+    		SetShapeLocalTransform(bolt, bt)
+    		SetShapeLocalTransform(selector, st)
+    		SetShapeLocalTransform(suppressor, spt)
+    		SetShapeLocalTransform(holo, ht)
+    		SetShapeLocalTransform(holo2, ht2)
+    		SetShapeLocalTransform(muzzlebreak, mbt)
+    		SetShapeLocalTransform(muzzlebreak2, mbt2)
+    		SetShapeLocalTransform(side1, sdt1)
+    		SetShapeLocalTransform(side2, sdt2)
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
+    			if not realistic and (ammo ~= magsize + 1 and not grenadelauncher) or (grenadelauncherammo == 0 and grenadelauncher) and not jammed then
+    				Reload()
+    				inspectTimer = 0
+    			end
+    		end
+
+    		if (InputReleased(reloadKey) or clickedmag) and selectfireTimer == 0 and not jammed then
+    			if realistic and curmagslot ~= nextmagslot and magcheckTimer == 0 then
+    				Reload()
+    				inspectTimer = 0
+    			end
+    		end
+
+    		if GetBool("ammobox.refill") then
+    			SetBool("ammobox.refill", false, true)
+    			PlaySound(refillsound, GetPlayerTransform(playerId).pos, 1, false)
+    		end
+
+    		if reloading then
+    			if reloadTimer > 0.4 then
+    				reloadTimer = reloadTimer - dt/reloadFactor*1.25
+    			elseif reloadTimer ~= 0 then
+    				reloadTimer = reloadTimer - dt
+    			end
+    			if reloadTimer < 0.4 and not cocksoundplaying and ammo == 0 then
+    				cocksoundplaying = true
+    				PlaySound(cocksound, GetPlayerTransform(playerId).pos, 0.45)
+    			end
+    			if reloadTimer < 0 then
+    				cocksoundplaying = false
+    				if grenadelauncher then
+    					grenadelauncherammo = 1
+    				else
+    					if inventoryenabled then
+    						if ammo == 0 then
+    							ammo = nextammo
+    						else
+    							ammo = nextammo + 1
+    						end
+    						name = "mag0-glock-9x19"
+    						maxammo = 17
+    						id = mag
+    						if id == "mag0-glock-9x19" then name, maxammo = "Glock", 17
+    						elseif id == "mag1-glock-9x19" then name, maxammo = "Glock", 33
+    						elseif id == "mag2-glock-9x19" then name, maxammo = "Glock", 50
+    						elseif id == "mag3-glock-9x19" then name, maxammo = "Glock", 100
+    						end
+    						local guninfo = Split(GetString("inventory.guns2"), "_")
+    						if #guninfo == 8 then
+    							SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19_"..guninfo[8], true)
+    						else
+    							SetString("inventory.guns2", guninfo[1].."_"..guninfo[2].."_"..mag.."_"..name.."_"..ammo.."_"..maxammo.."_9x19", true)
+    						end
+    						SetBool("inventory.update", true, true)
+    						curmagslot = 1
+    					elseif realistic then
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
+    	local x2, y2, z2, rotx2, roty2, rotz2 = 0.15, -0.95, -0.85, 0, 0, 0
+    	if reloading and ammo == 0 and reloadTimer < 0.8 and reloadTimer > 0.2 then
+    		x2, y2, z2, rotx2, roty2, rotz2 = 0.1, -0.7, -0.2+bt.pos[3], 0, 0, 0
+    	elseif reloading then
+    		x2, y2, z2, rotx2, roty2, rotz2 = -0.1+mt.pos[1], 0.05+mt.pos[2], -0.2+mt.pos[3], 0, 0, 0
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
+    	sightattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.15, -0.6))
+    	muzzleattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.35, -1.6))
+    	stockattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.4, -0.6))
+    	sideattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.6, -1.25))
+    	magattachpoint = TransformToParentPoint(btrans, Vec(0.25, -0.85, -0.5))
+    	gripattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.85, -1.4-guardlength))
+    	barrelattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.65, -1.6))
+    	guardattachpoint = TransformToParentPoint(btrans, Vec(0.1, -0.25, -1.5))
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
+    if GetString("game.player.tool") == "g17" and GetPlayerVehicle(playerId) == 0 then
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
+    if GetString("game.player.tool") == "g17" and grenadelauncher and not selectattachments then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiMiddle())
+    		UiAlign("center middle")
+    		UiImage("ui/hud/crosshair-launcher.png")
+    	UiPop()
+    end
+    if GetString("game.player.tool") == "g17" and sideattachment and side == "side3" then
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
+    if realistic and selectmag and GetString("game.player.tool") == "g17" then
+    	hoverindex=0
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(VecAdd(magattachpoint, Vec(0, 0.3, 0)))
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
+    if selectattachments and GetString("game.player.tool") == "g17" and GetPlayerVehicle(playerId) == 0 then
+    if hint then drawHint(info) end
+    hoverindex=0
+    	UiPush()
+    		local x,y,dist=UiWorldToPixel(sightattachpoint)
+    		if dist ~= 0 then
+    			UiTranslate(x-50,y+20)
+    			local curx,cury=UiGetRelativePos()
+    			UiPush()
+    				UiAlign("center middle")
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
+    				clickedmuzzle2 = AttachmentButton("muzzle","muzzle2",true,{curx,cury},{"Compensator","Reduces horizontal recoil, but turns your barrel into a flashbang."})
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
+    				clickedmag1 = AttachmentButton("mag","mag1-glock-9x19",true,{curx,cury},{"33rnd Mag","Pew Pew Pew"})
+    				UiTranslate(-70,0)
+    				curx,cury=curx-70,cury
+    				clickedmag2 = AttachmentButton("mag","mag2-glock-9x19",true,{curx,cury},{"50rnd Drum","Pew Pew Pew Pew Pew Pew"})
+    				UiTranslate(-70,0)
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
-	UiText("G17")
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
+    UiText("G17")
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
