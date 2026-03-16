# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,78 +1,4 @@
-allMegagunSounds = {}
-bulletsInAir = {}
-bulletTypesArr = {"7.62 mm", "20 mm", "Mini nuke"}
-bulletTypes = {
-	["7.62 mm"] = {
-		["damage"] = 1,
-		["spread_radius"] = 6,
-		["time_to_hit_target"] = 1 / 30,
-		["cooldown"] = 0,
-		["barrel_speed"] = 85
-	},
-	["20 mm"] = {
-		["damage"] = 3,
-		["spread_radius"] = 6,
-		["time_to_hit_target"] = 1 / 20,
-		["cooldown"] = 3 / 60,
-		["barrel_speed"] = 100
-	},
-	["Mini nuke"] = {
-		["damage"] = 2.2,
-		["spread_radius"] = 4,
-		["constant_velocity"] = 100,
-		["cooldown"] = 1 / 5,
-		["explodes"] = true,
-		["barrel_speed"] = 70
-	}
-}
-ammoReserves = {
-	["7.62 mm"] = {
-		["numBelts"] = 100,
-		["bulletsPerBelt"] = 3600,
-	},
-	["20 mm"] = {
-		["numBelts"] = 80,
-		["bulletsPerBelt"] = 1500
-	},
-	["Mini nuke"] = {
-		["numBelts"] = 50,
-		["bulletsPerBelt"] = 300
-	}
-}
-activeAmmo = "7.62 mm"
-gunMode = 0
-
--- 0 = inactive
--- 1 = winding up
--- 2 = winding down
--- 3 = actively firing
-GUN_INACTIVE = 0
-GUN_WINDING_UP = 1
-GUN_WINDING_DOWN = 2
-GUN_FIRING = 3
-
-BULLET_FIRE_LOCATIONS = {
-	Vec(17.3, 90, -13.5),
-	Vec(17.3, 90, -29.5),
-	Vec(24.6, 90, -25.6),
-	Vec(10.5, 90, -25.6),
-	Vec(24.6, 90, -17.6),
-	Vec(10.5, 90, -17.6)
-}
-
-reloadTimer = 0
-cooldownTimer = 0
-recoilTimer = 0
-
-bulletFireLocations = nil
-barrelRotateVelocity = 0
-barrelRotateAcceleration = 0
-
-recoilStrength = nil
-maxRecoil = nil
-timeInterval = nil
-recoilAmplitude = nil
-recoilAmplitudeCoefficient = nil
+#version 2
 function ResetRecoil()
 	recoilStrength = 0
 	maxRecoil = 0.2
@@ -140,13 +66,13 @@
 end
 
 function PlayReloadSound()
-	PlaySound(allMegagunSounds["reload"], GetPlayerTransform().pos, 1.0)
+	PlaySound(allMegagunSounds["reload"], GetPlayerTransform(playerId).pos, 1.0)
 	reloadTimer = 0.95
 end
 
 function CalculateRecoil(direction, dt)
 	recoilStrength = (maxRecoil - recoilAmplitude) + ((recoilAmplitude / 2) * ((direction * math.sin(((math.pi / timeInterval) * recoilTimer) - (math.pi / 2))) + 1))
-	if direction > 0 then
+	if direction ~= 0 then
 		recoilStrength = (maxRecoil - recoilAmplitude) + ((recoilAmplitude / 2) * ((direction * math.sin(((math.pi / timeInterval) * recoilTimer) - (math.pi / 2))) + 1))
 	else
 		recoilStrength = 1.125 * recoilAmplitude * (math.cos((math.pi / timeInterval) * recoilTimer) - (1 / 9))
@@ -253,231 +179,225 @@
 	bullet.pos = newPosition
 end
 
-function init()
-	RegisterTool("megagun", "MEGAGUN", "MOD/vox/MEGAGUN.vox")
-	SetBool("game.tool.megagun.enabled", true)
-
-	ResetRecoil()
-
-	-- Set default bullet number
-	for k, v in pairs(ammoReserves) do
-		ammoReserves[k]["currentBelt"] = ammoReserves[k]["bulletsPerBelt"]
-	end
-
-	allMegagunSounds["ambient"] = LoadLoop("MOD/snd/MEGAGUN_Firing_Ambient.ogg")
-	allMegagunSounds["reload"] = LoadSound("MOD/snd/MEGAGUN_Reload.ogg")
-	allMegagunSounds["winddown"] = LoadSound("MOD/snd/MEGAGUN_Spin_Down_Sound.ogg")
-	allMegagunSounds["windup"] = LoadSound("MOD/snd/MEGAGUN_Wind_Up_Sound.ogg")
-
-	allMegagunSounds["fire"] = {}
-	for i = 1, 3 do
-		allMegagunSounds["fire"][i] = LoadSound("MOD/snd/MEGAGUN_Firing_Sound_" .. i .. ".ogg")
-	end
-end
-
--- Updates once per frame
-function tick(dt)
-	-- Tick active bullets
-	local cleaningUpBullets = {}
-
-	for i = 1, #bulletsInAir do
-		local thisBullet = bulletsInAir[i]
-		if thisBullet == nil or thisBullet.isDead then
-			cleaningUpBullets[#cleaningUpBullets + 1] = i
-		elseif thisBullet.isInMotion then
-			ProjectileOperations(thisBullet)
-		end
-	end
-
-	cleanedBulletsInAir = {}
-	for i = 1, #cleaningUpBullets do
-		bulletsInAir[cleaningUpBullets[i]] = nil
-	end
-	for i = 1, #bulletsInAir do
-		if bulletsInAir[i] ~= nil then cleanedBulletsInAir[#cleanedBulletsInAir + 1] = bulletsInAir[i] end
-	end
-	bulletsInAir = cleanedBulletsInAir
-
-	if GetBool("level.unlimitedammo") then
-		ammoReserves[activeAmmo]["currentBelt"] = 99999
-		ammoReserves[activeAmmo]["numBelts"] = 99999
-	end
-
-	SetInt("game.tool.megagun.ammo", ammoReserves[activeAmmo]["numBelts"])
-
-	if GetString("game.player.tool") == "megagun" and GetBool("game.player.canusetool") and GetFloat("game.player.health") ~= 0 then
-		-- Switch ammo type
-		if InputPressed("c") and gunMode == GUN_INACTIVE then
-			for i = 1, #bulletTypesArr do
-				local k = bulletTypesArr[i]
-				if k == activeAmmo then
-					local newBulletIndex = i + 1
-					if newBulletIndex > #bulletTypesArr then newBulletIndex = 1 end
-					activeAmmo = bulletTypesArr[newBulletIndex]
-					PlayReloadSound()
-					break
-				end
-			end
-		end
-		
-		-- Reload
-		if InputPressed("r") and ammoReserves[activeAmmo]["currentBelt"] < ammoReserves[activeAmmo]["bulletsPerBelt"] then
-			LoadBeltIfNecessary(true)
-		end
-
-		-- Time to wind up
-		if ammoReserves[activeAmmo]["currentBelt"] > 0 and InputDown("usetool") and (gunMode == GUN_INACTIVE or gunMode == GUN_WINDING_DOWN) then
-			PlaySound(allMegagunSounds["windup"], GetPlayerTransform().pos, 0.6)
-			gunMode = GUN_WINDING_UP
-		end
-
-		-- Time to wind down
-		if gunMode == GUN_WINDING_UP or gunMode == GUN_FIRING then
-			if ammoReserves[activeAmmo]["currentBelt"] <= 0 or InputReleased("usetool") then
-				PlaySound(allMegagunSounds["winddown"], GetPlayerTransform().pos, 0.6)
-				gunMode = GUN_WINDING_DOWN
-			end	
-		end
-
-		-- Recoil
-		local toolBody = GetToolBody()
-		if toolBody ~= 0 then
-			SetToolTransform(Transform(Vec(0, 0, recoilStrength)))
-		end
-	else
-		barrelRotateVelocity = 0
-		barrelRotateAcceleration = 0
-		gunMode = GUN_INACTIVE
-	end
-end
-
--- Updates always 60 times per second
-undoingRecoil = false
-function update(dt)
-	if reloadTimer > 0 then
-		reloadTimer = reloadTimer - dt
-	end
-	if cooldownTimer > 0 then
-		cooldownTimer = cooldownTimer - dt
-	end
-
-	-- Undo recoil
-	if gunMode == GUN_FIRING then
-		if undoingRecoil then
-			undoingRecoil = false
-			ResetRecoil()
-		end
-		recoilTimer = recoilTimer + dt
-	else
-		if undoingRecoil or recoilStrength > 0 then
-			if not undoingRecoil then
-				undoingRecoil = true
-				local initialStoppingRecoil = recoilStrength
-				ResetRecoil()
-				maxRecoil = initialStoppingRecoil
-				recoilAmplitude = maxRecoil
-				recoilAmplitudeCoefficient = 1/16
-			end
-
-			recoilTimer = recoilTimer + dt
-			CalculateRecoil(-1, dt)
-		end
-
-		if undoingRecoil and recoilTimer >= 2.5 then
-			undoingRecoil = false
-			ResetRecoil()
-		end
-	end
-
-	-- Winding up animation
-	if gunMode == GUN_WINDING_UP then
-		if barrelRotateAcceleration <= 0 then
-			barrelRotateAcceleration = (bulletTypes[activeAmmo]["barrel_speed"] - barrelRotateVelocity) / 1.38
-		end
-
-		barrelRotateVelocity = barrelRotateVelocity + (barrelRotateAcceleration * dt)
-		if barrelRotateVelocity >= bulletTypes[activeAmmo]["barrel_speed"] then
-			barrelRotateVelocity = bulletTypes[activeAmmo]["barrel_speed"]
-			barrelRotateAcceleration = 0
-			gunMode = GUN_FIRING
-		end
-	end
-
-	-- Winding down animation
-	if gunMode == GUN_WINDING_DOWN then
-		if barrelRotateAcceleration >= 0 then
-			barrelRotateAcceleration = (0 - barrelRotateVelocity) / 1.39
-		end
-
-		barrelRotateVelocity = barrelRotateVelocity + (barrelRotateAcceleration * dt)
-		if barrelRotateVelocity <= 0 then
-			barrelRotateVelocity = 0
-			barrelRotateAcceleration = 0
-			gunMode = GUN_INACTIVE
-		end	
-	end
-
-	local toolBody = GetToolBody()
-	if GetString("game.player.tool") == "megagun" and toolBody ~= 0 then
-		-- Get some relative positions based off of the tool body
-		local toolTrans = GetBodyTransform(toolBody)
-		bulletFireLocations = {}
-		for i = 1, #BULLET_FIRE_LOCATIONS do
-			bulletFireLocations[#bulletFireLocations + 1] = TransformToParentPoint(toolTrans, MagicaVoxelPointToLocalPoint(BULLET_FIRE_LOCATIONS[i]))
-		end
-
-		-- Physically rotate the barrel
-		local megagunShapes = GetBodyShapes(GetToolBody())
-		local barrelShape = megagunShapes[2]
-		local attachmentPoint = Transform(MagicaVoxelPointToLocalPoint(Vec(17.5, 0, -21.2)))
-		local barrelTrans = TransformToLocalTransform(attachmentPoint, GetShapeLocalTransform(barrelShape))
-		attachmentPoint.rot = QuatEuler(0, 0, barrelRotateVelocity)
-		SetShapeLocalTransform(barrelShape, TransformToParentTransform(attachmentPoint, barrelTrans))
-
-		-- Firing effects
-		if gunMode == GUN_FIRING then
-			PlayLoop(allMegagunSounds["ambient"], GetPlayerTransform().pos, 0.8, false)
-			CalculateRecoil(1, dt)
-		end
-
-		-- Firing bullets
-		if gunMode == GUN_FIRING and reloadTimer <= 0 and cooldownTimer <= 0 then
-			ShootMegagun()
-		end
-	end
-end
-
-
--- Configuration UI
-function draw()
-	if GetString("game.player.tool") == "megagun" and GetBool("game.player.interactive") then
-		-- Ammo indicator
-		if not GetBool("level.unlimitedammo") then
-			UiPush()
-				UiTranslate(UiCenter(), UiHeight()-90)
-				UiAlign("center middle")
-				UiColor(1, 1, 1)
-				UiFont("bold.ttf", 24)
-				UiTextOutline(0, 0, 0, 1, 0.1)
-				UiText(string.format("%.0f", ammoReserves[activeAmmo]["currentBelt"]) .. " / " .. string.format("%.0f", ammoReserves[activeAmmo]["bulletsPerBelt"]))
-			UiPop()
-		end
-
-		-- Ammo type
-		UiPush()
-			UiTranslate(70, UiHeight() - (30 * #bulletTypesArr + 20 + 80))
-			UiAlign("bottom left")
-			UiColor(1, 1, 1)
-			UiFont("regular.ttf", 24)
-			UiTextOutline(0, 0, 0, 1, 0.1)
-			UiText("Press C to switch ammo type")
-			UiTranslate(0, 20)
-			for i = 1, #bulletTypesArr do
-				UiColor(0.5, 0.5, 0.5)
-				if activeAmmo == bulletTypesArr[i] then UiColor(1, 1, 1) end
-				UiTranslate(0, 30)
-				UiText(bulletTypesArr[i])
-			end
-		UiPop()
-	end
-end
+function server.init()
+    RegisterTool("megagun", "MEGAGUN", "MOD/vox/MEGAGUN.vox")
+    SetBool("game.tool.megagun.enabled", true, true)
+    ResetRecoil()
+    -- Set default bullet number
+    for k, v in pairs(ammoReserves) do
+    	ammoReserves[k]["currentBelt"] = ammoReserves[k]["bulletsPerBelt"]
+    end
+    allMegagunSounds["ambient"] = LoadLoop("MOD/snd/MEGAGUN_Firing_Ambient.ogg")
+    allMegagunSounds["fire"] = {}
+end
+
+function server.tick(dt)
+    local cleaningUpBullets = {}
+    for i = 1, #bulletsInAir do
+    	local thisBullet = bulletsInAir[i]
+    	if thisBullet == nil or thisBullet.isDead then
+    		cleaningUpBullets[#cleaningUpBullets + 1] = i
+    	elseif thisBullet.isInMotion then
+    		ProjectileOperations(thisBullet)
+    	end
+    end
+    cleanedBulletsInAir = {}
+    for i = 1, #cleaningUpBullets do
+    	bulletsInAir[cleaningUpBullets[i]] = nil
+    end
+end
+
+function server.update(dt)
+    if reloadTimer ~= 0 then
+    	reloadTimer = reloadTimer - dt
+    end
+    if cooldownTimer ~= 0 then
+    	cooldownTimer = cooldownTimer - dt
+    end
+    -- Undo recoil
+    if gunMode == GUN_FIRING then
+    	if undoingRecoil then
+    		undoingRecoil = false
+    		ResetRecoil()
+    	end
+    	recoilTimer = recoilTimer + dt
+    else
+    	if undoingRecoil or recoilStrength ~= 0 then
+    		if not undoingRecoil then
+    			undoingRecoil = true
+    			local initialStoppingRecoil = recoilStrength
+    			ResetRecoil()
+    			maxRecoil = initialStoppingRecoil
+    			recoilAmplitude = maxRecoil
+    			recoilAmplitudeCoefficient = 1/16
+    		end
+
+    		recoilTimer = recoilTimer + dt
+    		CalculateRecoil(-1, dt)
+    	end
+
+    	if undoingRecoil and recoilTimer >= 2.5 then
+    		undoingRecoil = false
+    		ResetRecoil()
+    	end
+    end
+    -- Winding up animation
+    if gunMode == GUN_WINDING_UP then
+    	if barrelRotateAcceleration <= 0 then
+    		barrelRotateAcceleration = (bulletTypes[activeAmmo]["barrel_speed"] - barrelRotateVelocity) / 1.38
+    	end
+
+    	barrelRotateVelocity = barrelRotateVelocity + (barrelRotateAcceleration * dt)
+    	if barrelRotateVelocity >= bulletTypes[activeAmmo]["barrel_speed"] then
+    		barrelRotateVelocity = bulletTypes[activeAmmo]["barrel_speed"]
+    		barrelRotateAcceleration = 0
+    		gunMode = GUN_FIRING
+    	end
+    end
+    -- Winding down animation
+    if gunMode == GUN_WINDING_DOWN then
+    	if barrelRotateAcceleration >= 0 then
+    		barrelRotateAcceleration = (0 - barrelRotateVelocity) / 1.39
+    	end
+
+    	barrelRotateVelocity = barrelRotateVelocity + (barrelRotateAcceleration * dt)
+    	if barrelRotateVelocity <= 0 then
+    		barrelRotateVelocity = 0
+    		barrelRotateAcceleration = 0
+    		gunMode = GUN_INACTIVE
+    	end	
+    end
+    local toolBody = GetToolBody()
+end
+
+function client.init()
+    allMegagunSounds["reload"] = LoadSound("MOD/snd/MEGAGUN_Reload.ogg")
+    allMegagunSounds["winddown"] = LoadSound("MOD/snd/MEGAGUN_Spin_Down_Sound.ogg")
+    allMegagunSounds["windup"] = LoadSound("MOD/snd/MEGAGUN_Wind_Up_Sound.ogg")
+    for i = 1, 3 do
+    	allMegagunSounds["fire"][i] = LoadSound("MOD/snd/MEGAGUN_Firing_Sound_" .. i .. ".ogg")
+    end
+end
+
+function client.tick(dt)
+    for i = 1, #bulletsInAir do
+    	if bulletsInAir[i] ~= nil then cleanedBulletsInAir[#cleanedBulletsInAir + 1] = bulletsInAir[i] end
+    end
+    bulletsInAir = cleanedBulletsInAir
+
+    if GetBool("level.unlimitedammo") then
+    	ammoReserves[activeAmmo]["currentBelt"] = 99999
+    	ammoReserves[activeAmmo]["numBelts"] = 99999
+    end
+
+    SetInt("game.tool.megagun.ammo", ammoReserves[activeAmmo]["numBelts"], true)
+
+    if GetString("game.player.tool") == "megagun" and GetBool("game.player.canusetool") and GetFloat("game.player.health") ~= 0 then
+    	-- Switch ammo type
+    	if InputPressed("c") and gunMode == GUN_INACTIVE then
+    		for i = 1, #bulletTypesArr do
+    			local k = bulletTypesArr[i]
+    			if k == activeAmmo then
+    				local newBulletIndex = i + 1
+    				if newBulletIndex > #bulletTypesArr then newBulletIndex = 1 end
+    				activeAmmo = bulletTypesArr[newBulletIndex]
+    				PlayReloadSound()
+    				break
+    			end
+    		end
+    	end
+
+    	-- Reload
+    	if InputPressed("r") and ammoReserves[activeAmmo]["currentBelt"] < ammoReserves[activeAmmo]["bulletsPerBelt"] then
+    		LoadBeltIfNecessary(true)
+    	end
+
+    	-- Time to wind up
+    	if ammoReserves[activeAmmo]["currentBelt"] > 0 and InputDown("usetool") and (gunMode == GUN_INACTIVE or gunMode == GUN_WINDING_DOWN) then
+    		PlaySound(allMegagunSounds["windup"], GetPlayerTransform(playerId).pos, 0.6)
+    		gunMode = GUN_WINDING_UP
+    	end
+
+    	-- Time to wind down
+    	if gunMode == GUN_WINDING_UP or gunMode == GUN_FIRING then
+    		if ammoReserves[activeAmmo]["currentBelt"] <= 0 or InputReleased("usetool") then
+    			PlaySound(allMegagunSounds["winddown"], GetPlayerTransform(playerId).pos, 0.6)
+    			gunMode = GUN_WINDING_DOWN
+    		end	
+    	end
+
+    	-- Recoil
+    	local toolBody = GetToolBody()
+    	if toolBody ~= 0 then
+    		SetToolTransform(Transform(Vec(0, 0, recoilStrength)))
+    	end
+    else
+    	barrelRotateVelocity = 0
+    	barrelRotateAcceleration = 0
+    	gunMode = GUN_INACTIVE
+    end
+end
+
+function client.update(dt)
+    if GetString("game.player.tool") == "megagun" and toolBody ~= 0 then
+    	-- Get some relative positions based off of the tool body
+    	local toolTrans = GetBodyTransform(toolBody)
+    	bulletFireLocations = {}
+    	for i = 1, #BULLET_FIRE_LOCATIONS do
+    		bulletFireLocations[#bulletFireLocations + 1] = TransformToParentPoint(toolTrans, MagicaVoxelPointToLocalPoint(BULLET_FIRE_LOCATIONS[i]))
+    	end
+
+    	-- Physically rotate the barrel
+    	local megagunShapes = GetBodyShapes(GetToolBody())
+    	local barrelShape = megagunShapes[2]
+    	local attachmentPoint = Transform(MagicaVoxelPointToLocalPoint(Vec(17.5, 0, -21.2)))
+    	local barrelTrans = TransformToLocalTransform(attachmentPoint, GetShapeLocalTransform(barrelShape))
+    	attachmentPoint.rot = QuatEuler(0, 0, barrelRotateVelocity)
+    	SetShapeLocalTransform(barrelShape, TransformToParentTransform(attachmentPoint, barrelTrans))
+
+    	-- Firing effects
+    	if gunMode == GUN_FIRING then
+    		PlayLoop(allMegagunSounds["ambient"], GetPlayerTransform(playerId).pos, 0.8, false)
+    		CalculateRecoil(1, dt)
+    	end
+
+    	-- Firing bullets
+    	if gunMode == GUN_FIRING and reloadTimer <= 0 and cooldownTimer <= 0 then
+    		ShootMegagun()
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "megagun" and GetBool("game.player.interactive") then
+    	-- Ammo indicator
+    	if not GetBool("level.unlimitedammo") then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-90)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 24)
+    			UiTextOutline(0, 0, 0, 1, 0.1)
+    			UiText(string.format("%.0f", ammoReserves[activeAmmo]["currentBelt"]) .. " / " .. string.format("%.0f", ammoReserves[activeAmmo]["bulletsPerBelt"]))
+    		UiPop()
+    	end
+
+    	-- Ammo type
+    	UiPush()
+    		UiTranslate(70, UiHeight() - (30 * #bulletTypesArr + 20 + 80))
+    		UiAlign("bottom left")
+    		UiColor(1, 1, 1)
+    		UiFont("regular.ttf", 24)
+    		UiTextOutline(0, 0, 0, 1, 0.1)
+    		UiText("Press C to switch ammo type")
+    		UiTranslate(0, 20)
+    		for i = 1, #bulletTypesArr do
+    			UiColor(0.5, 0.5, 0.5)
+    			if activeAmmo == bulletTypesArr[i] then UiColor(1, 1, 1) end
+    			UiTranslate(0, 30)
+    			UiText(bulletTypesArr[i])
+    		end
+    	UiPop()
+    end
+end
+

```
