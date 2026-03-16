# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,109 +1,15 @@
---rmwakm custom tool example
-
-#include "script/toolanimation.lua"
+#version 2
 local tool_initialized = false
-body = nil
-barrel = nil
-barrelTransform = nil
-toolAnimator = ToolAnimator()
-
-	reloadsound1 = LoadSound("MOD/snd/reloadingsounds1.ogg")
-	reloadsound2 = LoadSound("MOD/snd/reloadingsounds2.ogg")
-	fireselector = LoadSound("MOD/snd/fireselector.ogg")
-	silencedshoot = LoadSound("MOD/snd/silenced.ogg")
-	
-	reticlesprite = LoadSprite("MOD/sprites/reticlesprite2.png")
-	donoutreticlesprite = LoadSprite("MOD/sprites/donoutreticlesprite.png")
-	muzzleflash = LoadSprite("MOD/sprites/muzzleflash.png")
-	
-	-- ========= Recoil config (drop-in) =========
--- Pitch/Yaw state (persist between frames)
-recoilPitch = recoilPitch or 0.0
-recoilYaw   = recoilYaw   or 0.0
-
--- Tunables (per-weapon feel)
-RECOIL_BASE_HIP   = 1.2  -- per-shot pitch in hip
-RECOIL_BASE_ADS   = 1  -- per-shot pitch in ADS
-RECOIL_YAW_RANGE  = 0.62   -- +/- horizontal drift per shot (random)
-RECOVER_HIP       = 7.5    -- deg/sec pitch/yaw return in hip
-RECOVER_ADS       = 7.5   -- deg/sec pitch/yaw return in ADS
-
--- How much the GUN model moves vs the CAMERA
---   (gun should kick more than view; camera stays readable)
-VISUAL_SCALE_HIP  = 1.8   -- viewmodel tilt multiplier (hip)
-VISUAL_SCALE_ADS  = 1.4   -- viewmodel tilt multiplier (ADS)
-CAMERA_SCALE_HIP  = 0.75   -- camera tilt multiplier (hip)
-CAMERA_SCALE_ADS  = 0.65   -- camera tilt multiplier (ADS)
-
--- Attachments influence (optional)
-GRIP_MULT         = 0.85   -- if grips==1 or 2
-SUPPRESSOR_MULT   = 0.95   -- if muzzlec==1
--- ========= /Recoil config =========
 
 function SpentCasing()
 	local gt = GetBodyTransform(GetToolBody())
 	local casingpos = TransformToParentPoint(gt, Vec(0.18, 0.09, -0.3))
 	local fwdpos = TransformToParentPoint(gt, Vec(6+math.random()*4, 0.5+math.random()*4, -0.65+math.random()*4))
-	local direction = VecAdd(GetPlayerVelocity(), VecSub(fwdpos, casingpos))
+	local direction = VecAdd(GetPlayerVelocity(playerId), VecSub(fwdpos, casingpos))
 	casing = Spawn("MOD/vox/casing.xml", Transform(casingpos, QuatEuler(math.random(0, 90), math.random(0, 90), math.random(0, 90))))
 	SetBodyVelocity(casing[1], direction)
 end
 
-function init()
-	--Register tool and enable it
-	RegisterTool("rmwakm", "AKM", "MOD/prefab/minigun.xml")
-	SetBool("game.tool.rmwakm.enabled", true)
-	
-	 SetToolTransform(Transform(Vec(0, 0, 0)), 0) 
-    tool_initialized = false
-
-	angle = 0
-	angVel = 0
-	coolDown = 0
-	smoke = 0
-	magazine = 31
-	aiming = false
-	fireswitch = false
-	reloading = false
-	reloadtimer = 0
-	nocasings = GetBool("savegame.mod.nocasings")
-	optics = 0
-	grips = 0
-	muzzlec = 0
-	rails = 0
-	attachmentmenu = false
-	recoilshake = 0.48
-	zoomfov = 55
-    charginghandletime = 0
-	stocks = 1
-	autospread = 0.01
-	spread = 0.002
-	low = false
-	semi = 0
-	hands = 1
-	
-	-- recoil init
-	recoilPitch = 0.0
-	recoilYaw   = 0.0
-	
-	local offset = Transform(Vec(0.5, 0, 0))
-	SetToolTransform(offset, 0)
-	
-	shootSnd = {}
-	for i=0, 7 do
-		shootSnd[i] = LoadSound("MOD/snd/rifle.ogg")
-	end
-	
-	shootHaptic = LoadHaptic("MOD/haptic/gun_fire.xml")
-	local toolHaptic = LoadHaptic("MOD/haptic/background.xml")
-	SetToolHaptic("rmwakm", toolHaptic);
-
-	
-	oldPipePos = Vec()
-	particleTimer = 0
-end
-
---Return a random vector of desired length
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -113,16 +19,15 @@
 	return math.random(1000)/1000*(ma-mi) + mi
 end
 
--- Small helpers
 local function approach(current, target, maxDelta)
     if current < target then return math.min(current + maxDelta, target) end
     return math.max(current - maxDelta, target)
 end
+
 local function rndRange(mi, ma)
     return math.random(1000)/1000*(ma-mi) + mi
 end
 
--- Add recoil when a shot happens
 function AddRecoil(aiming, grips, muzzlec)
     local base = aiming and RECOIL_BASE_ADS or RECOIL_BASE_HIP
     if grips == 1 or grips == 2 then base = base * GRIP_MULT end
@@ -133,7 +38,6 @@
     recoilYaw   = recoilYaw   + yawKick
 end
 
--- Per-tick: apply camera recoil (small) & recover
 function ApplyRecoilTick(dt, aiming, reloading, attachmentmenu)
     local camScale = aiming and CAMERA_SCALE_ADS or CAMERA_SCALE_HIP
 
@@ -151,18 +55,16 @@
     recoilYaw   = approach(recoilYaw,   0.0, recover * dt)
 end
 
--- Per-tick: push viewmodel (gun) more than camera for the “hand kick” feel
-function ApplyVisualGunRecoil(dt, aiming)
+tion ApplyVisualGunRecoil(dt, aiming)
     local scale = aiming and VISUAL_SCALE_ADS or VISUAL_SCALE_HIP
     local vis = Transform(Vec(0,0,0), QuatEuler(recoilPitch*scale, recoilYaw*scale, 0))
     toolAnimator.offsetTransform = TransformToParentTransform(toolAnimator.offsetTransform, vis)
     tickToolAnimator(toolAnimator, dt)
 end
 
--- Fire ray that respects recoil and TPS/FPS differences:
---  - TPS: fire from muzzle (bullets follow the muzzle you see)
---  - FPS: fire from camera direction + (recoilPitch/Yaw)
-function ComputeFireRay(spreadValue, muzzleTransform)
+--
+
+tion ComputeFireRay(spreadValue, muzzleTransform)
     if GetBool("game.thirdperson") then
         local p = muzzleTransform.pos
         local d = TransformToParentVec(muzzleTransform, Vec(0,0,-1))
@@ -175,7 +77,9 @@
     end
 end
 
-function tick(dt)
+fu
+
+tion tick(dt)
 
   -- Check if the tool is available
     local tool_transform = GetToolLocationWorldTransform()
@@ -205,7 +109,7 @@
 		local d = GetToolBody()
 		local railings = GetBodyShapes(d)
 		
-			SetBool("hud.aimdot", false)
+			SetBool("hud.aimdot", false, true)
 		
         if optics > 3 then optics = 0 
 		end
@@ -271,7 +175,7 @@
 			if GetString("game.player.tool") == "rmwakm" then --- When Zero then its empty
 			
 			local optic = opticssight[9]
-                if charginghandletime > 0 then ---Charginghandle
+                if charginghandletime ~= 0 then ---Charginghandle
 					SetShapeLocalTransform(optic, Transform(Vec(0.01, 0.125, -0.1), QuatEuler(-90, 0, 0)))
 				else
 					SetShapeLocalTransform(optic, Transform(Vec(0.01, 0.125, -0.2), QuatEuler(-90, 0, 0)))
@@ -402,7 +306,7 @@
             end
               for i = 1, #railings do
                 local rail = railings[7] ---Laser
-                if rails > 0 then 
+                if rails ~= 0 then 
                     RemoveTag(rail, "invisible")
 					
 				else
@@ -508,7 +412,7 @@
 					smoke = math.min(1.0, smoke + 0.1)
 					coolDown = 0.08
 					charginghandletime = 0.07
-					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1)
+					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1, true)
 				end
 			end
 			PlayHaptic(shootHaptic, 1)
@@ -547,7 +451,7 @@
 					smoke = math.min(1.0, smoke + 0.1)
 					coolDown = 0.08
 					charginghandletime = 0.07
-					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1)
+					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1, true)
 				end
 			end
 			PlayHaptic(shootHaptic, 1)
@@ -556,8 +460,8 @@
 		end
 	
 		--Emit smoke from the pipe, but not when firing
-		if InputDown("usetool") and magazine > 0 then
-			if smoke > 0 then
+		if InputDown("usetool") and magazine ~= 0 then
+			if smoke ~= 0 then
 				if particleTimer < 0.0 then
 					particleTimer = dt + (1.0-smoke)*0.05
 					local forward = TransformToParentVec(bt, Vec(0, 0, 0))
@@ -668,7 +572,9 @@
 	smoke = math.max(0.0, smoke - dt/0)
 end
 
-function GetAimPos() --where your crosshair is
+fu
+
+tion GetAimPos() --where your crosshair is
 	local ct = GetCameraTransform()
 	local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -100))
     local direction = VecSub(forwardPos, ct.pos)
@@ -682,7 +588,9 @@
 	return forwardPos, hit, distance
 end
 
-function draw()
+fu
+
+tion draw()
 
 if GetString("game.player.tool") == "rmwakm" and not reloading and not attachmentmenu and GetBool("game.thirdperson") and not low then
         local crossX, crossY = UiWorldToPixel(pointpos)
@@ -746,5 +654,52 @@
 			
 			end
 			
-			
-
+
+function server.init()
+    RegisterTool("rmwakm", "AKM", "MOD/prefab/minigun.xml")
+    SetBool("game.tool.rmwakm.enabled", true, true)
+     SetToolTransform(Transform(Vec(0, 0, 0)), 0) 
+       tool_initialized = false
+    angle = 0
+    angVel = 0
+    coolDown = 0
+    smoke = 0
+    magazine = 31
+    aiming = false
+    fireswitch = false
+    reloading = false
+    reloadtimer = 0
+    nocasings = GetBool("savegame.mod.nocasings")
+    optics = 0
+    grips = 0
+    muzzlec = 0
+    rails = 0
+    attachmentmenu = false
+    recoilshake = 0.48
+    zoomfov = 55
+       charginghandletime = 0
+    stocks = 1
+    autospread = 0.01
+    spread = 0.002
+    low = false
+    semi = 0
+    hands = 1
+    -- recoil init
+    recoilPitch = 0.0
+    recoilYaw   = 0.0
+    local offset = Transform(Vec(0.5, 0, 0))
+    SetToolTransform(offset, 0)
+    shootSnd = {}
+    shootHaptic = LoadHaptic("MOD/haptic/gun_fire.xml")
+    local toolHaptic = LoadHaptic("MOD/haptic/background.xml")
+    SetToolHaptic("rmwakm", toolHaptic);
+    oldPipePos = Vec()
+    particleTimer = 0
+end
+
+function client.init()
+    for i=0, 7 do
+    	shootSnd[i] = LoadSound("MOD/snd/rifle.ogg")
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
@@ -1,42 +1,4 @@
-function init()
-	nocasings = GetBool("savegame.mod.nocasings")
-	if nocasings == 0 then nocasings = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("M4 Carbine")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("No Casings")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if nocasings then
-			if UiTextButton("Yes", 20, 20) then
-				nocasings = false
-				SetBool("savegame.mod.nocasings", nocasings)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				nocasings = true
-				SetBool("savegame.mod.nocasings", nocasings)
-			end
-		end
-	UiPop()
-
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -55,4 +17,44 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    nocasings = GetBool("savegame.mod.nocasings")
+    if nocasings == 0 then nocasings = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("M4 Carbine")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("No Casings")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if nocasings then
+    		if UiTextButton("Yes", 20, 20) then
+    			nocasings = false
+    			SetBool("savegame.mod.nocasings", nocasings, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			nocasings = true
+    			SetBool("savegame.mod.nocasings", nocasings, true)
+    		end
+    	end
+    UiPop()
+
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```

---

# Migration Report: safe.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/safe.lua
+++ patched/safe.lua
@@ -1,80 +1,15 @@
---rmwakm custom tool example
-
-#include "script/toolanimation.lua"
+#version 2
 local tool_initialized = false
-body = nil
-barrel = nil
-barrelTransform = nil
-toolAnimator = ToolAnimator()
-
-	reloadsound1 = LoadSound("MOD/snd/reloadingsounds1.ogg")
-	reloadsound2 = LoadSound("MOD/snd/reloadingsounds2.ogg")
-	fireselector = LoadSound("MOD/snd/fireselector.ogg")
-	silencedshoot = LoadSound("MOD/snd/silenced.ogg")
-	
-	reticlesprite = LoadSprite("MOD/sprites/reticlesprite2.png")
-	donoutreticlesprite = LoadSprite("MOD/sprites/donoutreticlesprite.png")
-	muzzleflash = LoadSprite("MOD/sprites/muzzleflash.png")
 
 function SpentCasing()
 	local gt = GetBodyTransform(GetToolBody())
 	local casingpos = TransformToParentPoint(gt, Vec(0.18, 0.09, -0.3))
 	local fwdpos = TransformToParentPoint(gt, Vec(6+math.random()*4, 0.5+math.random()*4, -0.65+math.random()*4))
-	local direction = VecAdd(GetPlayerVelocity(), VecSub(fwdpos, casingpos))
+	local direction = VecAdd(GetPlayerVelocity(playerId), VecSub(fwdpos, casingpos))
 	casing = Spawn("MOD/vox/casing.xml", Transform(casingpos, QuatEuler(math.random(0, 90), math.random(0, 90), math.random(0, 90))))
 	SetBodyVelocity(casing[1], direction)
 end
 
-function init()
-	--Register tool and enable it
-	RegisterTool("rmwakm", "AKM", "MOD/prefab/minigun.xml")
-	SetBool("game.tool.rmwakm.enabled", true)
-	
-	 SetToolTransform(Transform(Vec(0, 0, 0)), 0) 
-    tool_initialized = false
-
-	angle = 0
-	angVel = 0
-	coolDown = 0
-	smoke = 0
-	magazine = 31
-	aiming = false
-	fireswitch = false
-	reloading = false
-	reloadtimer = 0
-	nocasings = GetBool("savegame.mod.nocasings")
-	optics = 0
-	grips = 0
-	muzzlec = 0
-	rails = 0
-	attachmentmenu = false
-	recoilshake = 0.48
-	zoomfov = 55
-    charginghandletime = 0
-	stocks = 1
-	autospread = 0.01
-	spread = 0.002
-	low = false
-	semi = 0
-	hands = 1
-	local offset = Transform(Vec(0.5, 0, 0))
-	SetToolTransform(offset, 0)
-	
-	shootSnd = {}
-	for i=0, 7 do
-		shootSnd[i] = LoadSound("MOD/snd/rifle.ogg")
-	end
-	
-	shootHaptic = LoadHaptic("MOD/haptic/gun_fire.xml")
-	local toolHaptic = LoadHaptic("MOD/haptic/background.xml")
-	SetToolHaptic("rmwakm", toolHaptic);
-
-	
-	oldPipePos = Vec()
-	particleTimer = 0
-end
-
---Return a random vector of desired length
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -82,499 +17,6 @@
 
 function rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
-end
-
-function tick(dt)
-
-  -- Check if the tool is available
-    local tool_transform = GetToolLocationWorldTransform()
-    
-    -- If the tool is initialized, set the transform with no sway
-    if tool_transform then
-        if not tool_initialized then
-            print("Tool initialized, disabling sway.")
-            tool_initialized = true
-        end
-        SetToolTransform(tool_transform, 0)  -- Disable sway by setting to 0
-    else
-        -- If the tool is not initialized, keep trying until it's available
-        print("Tool transform not available yet.")
-    end
-	--Check if rmwakm is selected
-	if GetString("game.player.tool") == "rmwakm" then
-        local mt = GetToolLocationWorldTransform("muzzle")
-		local at = GetToolLocationWorldTransform("acog")
-		local ht = GetToolLocationWorldTransform("holo")
-		local a = GetToolBody()
-		local opticssight = GetBodyShapes(a)
-		local b = GetToolBody()
-		local foregrips = GetBodyShapes(b)
-		local c = GetToolBody()
-		local muzzles = GetBodyShapes(c)
-		local d = GetToolBody()
-		local railings = GetBodyShapes(d)
-		
-			SetBool("hud.aimdot", false)
-		
-        if optics > 3 then optics = 0 
-		end
-		if grips > 2 then grips = 0 
-		end
-		if stocks > 2 then stocks = 0 
-		end
-		if muzzlec > 1 then muzzlec = 0 
-		end
-		if rails > 3 then rails = 0 
-		end
-		if hands > 2 then hands = 0 
-		end
-if InputReleased("usetool") then semi = 0 
-		end
-		
-		
-		if semi > 1 then semi = 1 
-		end
-
-       if InputDown("t") and not reloading then attachmentmenu = true ---Turn on the attachment selection Menu
-			coolDown = 0.09
-			
-			aiming = false
-		else attachmentmenu = false
-			end
-			
-        
-		
-		if InputPressed("mmb") == true and fireswitch == false then fireswitch = true
-			coolDown = 0.09
-			PlaySound(fireselector)
-			end
-			
-			
-		if InputPressed("mmb") == true and fireswitch == true and coolDown < 0 then 
-			fireswitch = false
-			PlaySound(fireselector)
-			end
-			
-			if InputPressed("o") and attachmentmenu then 
-			optics = optics + 1
-			end
-			
-			if InputPressed("i") and attachmentmenu then 
-			stocks = stocks + 1
-			end
-			
-			if InputPressed("p") and attachmentmenu then 
-			grips = grips + 1
-			end
-			
-			if InputPressed("k") and attachmentmenu then 
-			muzzlec = muzzlec + 1
-			end
-			
-			if InputPressed("l") and attachmentmenu then 
-			rails = rails + 1
-			end
-			if InputPressed("h") and attachmentmenu then 
-			hands = hands + 1
-			end
-			if GetString("game.player.tool") == "rmwakm" then --- When Zero then its empty
-			
-			local optic = opticssight[9]
-                if charginghandletime > 0 then ---Charginghandle
-					SetShapeLocalTransform(optic, Transform(Vec(0.01, 0.125, -0.1), QuatEuler(-90, 0, 0)))
-				else
-					SetShapeLocalTransform(optic, Transform(Vec(0.01, 0.125, -0.2), QuatEuler(-90, 0, 0)))
-                end
-			
-			local optic = opticssight[8]
-                if reloadtimer > 1 then ---Magazine
-					SetTag(optic, "invisible")
-				else
-				RemoveTag(optic, "invisible")
-                end
-			
-			
-			 for i = 1, #opticssight do
-                local optic = opticssight[1]
-                if optics == 1 or optics == 2 or optics == 3 then ---Mount
-                    RemoveTag(optic, "invisible")
-					
-					SetShapeLocalTransform(optic, Transform(Vec(-0.05, 0.06, -0.1), QuatEuler(-90, 0, 0)))
-				else
-				SetTag(optic, "invisible")
-					
-                end
-				local optic = opticssight[2]
-                if optics == 2 then ---Acog
-                    RemoveTag(optic, "invisible")
-					
-					SetShapeLocalTransform(optic, Transform(Vec(-0.037, 0.19, -0.07), QuatEuler(-90, 0, 0)))
-				else
-				SetTag(optic, "invisible")
-					
-                end
-				
-				
-				local optic = opticssight[3]
-                if optics == 3 then ---Holo
-                    RemoveTag(optic, "invisible")
-					
-					SetShapeLocalTransform(optic, Transform(Vec(-0.025, 0.165, -0.15), QuatEuler(-90, 0, 0)))
-				else
-				SetTag(optic, "invisible")
-					
-                end
-				local stock = opticssight[10]
-                if stocks == 1 then ---Stock
-                    RemoveTag(stock, "invisible")
-					
-				else
-					SetTag(stock, "invisible")
-					
-                end
-				local stock = opticssight[11]
-                if stocks == 2 then ---Stock
-                    RemoveTag(stock, "invisible")
-					
-				else
-					SetTag(stock, "invisible")
-					
-                end
-                for i = 1, #foregrips do
-                local grip = foregrips[4] ---Vertical Grip
-                if grips == 1 then
-                    RemoveTag(grip, "invisible")
-					
-				else
-					SetTag(grip, "invisible")
-					
-                end
-				
-				
-				local grip = foregrips[5] ---Angled Grip
-                if grips == 2 then
-                    RemoveTag(grip, "invisible")
-					SetShapeLocalTransform(grip, Transform(Vec(-0.025, 0.013, -0.45), QuatEuler(-90, 0, 0)))
-				else
-					SetTag(grip, "invisible")
-					
-                end
-				
-				local hand1 = foregrips[12] ---lets try some hands... here we fucking go.
-                if not GetBool("game.thirdperson") and not reloading and not attachmentmenu and hands == 1 then
-                    RemoveTag(hand1, "invisible")
-					SetShapeLocalTransform(hand1, Transform(Vec(-0.25, -0.14, -0.21), QuatEuler(-90, 45, 20)))
-				else
-					SetTag(hand1, "invisible")
-					
-					
-                end
-				local hand2 = foregrips[13] ---lets try some hands... here we fucking go. take two.
-                if not GetBool("game.thirdperson") and hands == 1 then
-                    RemoveTag(hand2, "invisible")
-					SetShapeLocalTransform(hand2, Transform(Vec(0.0765, -0.05, 0.1), QuatEuler(-90, 20, 0)))
-				else
-					SetTag(hand2, "invisible")
-					
-					
-                end
-				local hand1 = foregrips[14] ---lets try some hands... here we fucking go.
-                if not GetBool("game.thirdperson") and not reloading and not attachmentmenu and hands == 2 then
-                    RemoveTag(hand1, "invisible")
-					SetShapeLocalTransform(hand1, Transform(Vec(-0.25, -0.14, -0.21), QuatEuler(-90, 45, 20)))
-				else
-					SetTag(hand1, "invisible")
-					
-					
-                end
-				local hand2 = foregrips[15] ---lets try some hands... here we fucking go. take two.
-                if not GetBool("game.thirdperson") and hands == 2 then
-                    RemoveTag(hand2, "invisible")
-					SetShapeLocalTransform(hand2, Transform(Vec(0.0765, -0.05, 0.1), QuatEuler(-90, 20, 0)))
-				else
-					SetTag(hand2, "invisible")
-					
-					
-                end
-                for i = 1, #muzzles do
-                local muzzle = muzzles[6] ---Silencer
-                if muzzlec == 1 then 
-                    RemoveTag(muzzle, "invisible")
-					
-				else
-					SetTag(muzzle, "invisible")
-					
-                end
-				for i = 1, #railings do
-                local rail = railings[7] ---Laser
-                if rails > 0 then 
-                    RemoveTag(rail, "invisible")
-					
-				else
-					SetTag(rail, "invisible")
-					
-                end
-				
-                
-            end
-                
-            end
-            end
-            end
-			end
-			
-		
-		
-		
-		if InputDown("rmb") and not reloading and not attachmentmenu then 
-		aiming = true
-		else aiming = false
-			end
-			
-		
-		
-			if aiming then
-			SetCameraFov(80)
-			spread = 0.002
-			autospread = 0.002
-			
-    
-			if optics == 2 then
-			SetCameraFov(30)
-			if not InputDown("a") and not InputDown("d") and not InputDown("shift") then
-			DrawSprite(reticlesprite, at, 0.04, 0.04, 1, 1, 1, 1)
-			end
-			end
-			if optics == 3 and not InputDown("a") and not InputDown("d") and not InputDown("shift") then
-			DrawSprite(donoutreticlesprite, ht, 0.01, 0.01, 1, 1, 1, 1)
-			end
-			else
-			spread = 0.002
-			autospread = 0.01
-			end
-			
-			if InputPressed("r") and magazine < 31 and not InputDown("usetool") and not reloading and not attachmentmenu then
-				reloadtimer = 2.3
-				PlaySound(reloadsound1)
-				aiming = false
-				reloading = true
-			end
-			
-			if reloadtimer < 0 and reloading == true then
-			magazine = 31
-			PlaySound(reloadsound2)
-			reloading = false
-			charginghandletime = 0.1
-			end
-			
-			if grips == 1 or grips == 2 then
-			recoilshake = 0.52
-			
-			end
-			
-			
-			if grips == 0 or grips == 3 then
-			recoilshake = 0.61
-			
-			end
-			
-			if stocks == 0 then
-			recoilshake = recoilshake + 0.12
-			else
-			recoilshake = recoilshake - 0.12
-			end
-			
-			
-			
-		if GetBool("game.player.canusetool") and InputDown("usetool") and not attachmentmenu and GetInt("game.tool.gun.ammo") > 0 and magazine > 0 and fireswitch and not low and not reloading and semi < 1 then
-			angVel = math.min(1000, angVel + dt*9000)	
-			if angVel == 1000 then
-				if coolDown < 0 then
-                    local _, p, _, d = GetPlayerAimInfo(mt.pos)
-                    d = VecAdd(d, rndVec(spread))
-					Shoot(p, d, "bullet", 0.15)
-					Shoot(p, d, "bullet", 0.15)
-					Shoot(p, d, "bullet", 0.15)
-					
-					magazine = magazine - 1
-					semi = semi + 1
-					ShakeCamera(recoilshake)
-					if muzzlec == 0 then
-					DrawSprite(muzzleflash, mt, 0.3, 0.3, 1, 1, 1, 1, true)
-					end
-					SetCameraOffsetTransform(Transform(Vec(x, y, 0.07), QuatEuler(x, y, 2)), true)
-					if not nocasings then
-					SpentCasing()
-					end
-
-					--Light, particles and sound
-					PointLight(mt.pos, 1, 0.7, 0.5, 3)
-					if muzzlec == 1 then
-					PlaySound(silencedshoot)
-					else
-					PlaySound(shootSnd[math.random(0,#shootSnd)])
-					end
-
-					smoke = math.min(1.0, smoke + 0.1)
-					coolDown = 0.08
-					charginghandletime = 0.07
-					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1)
-				end
-			end
-			PlayHaptic(shootHaptic, 1)
-		else
-			angVel = math.max(0, angVel - dt*1000)
-		end
-
-		--Check if firing
-		if GetBool("game.player.canusetool") and InputDown("usetool") and not attachmentmenu and not reloading and GetInt("game.tool.gun.ammo") > 0 and magazine > 0 and not low and not fireswitch then
-			angVel = math.min(1000, angVel + dt*9000)	
-			if angVel == 1000 then
-				if coolDown < 0 then
-                    local _, p, _, d = GetPlayerAimInfo(mt.pos)
-                    d = VecAdd(d, rndVec(autospread))
-					Shoot(p, d, "bullet", 0.15)
-					Shoot(p, d, "bullet", 0.15)
-					Shoot(p, d, "bullet", 0.15)
-					
-					magazine = magazine - 1
-					ShakeCamera(recoilshake)
-					if muzzlec == 0 then
-					DrawSprite(muzzleflash, mt, 0.3, 0.3, 1, 1, 1, 1, true)
-					end
-					SetCameraOffsetTransform(Transform(Vec(x, y, 0.07), QuatEuler(x, y, 2)), true)
-					if not nocasings then
-					SpentCasing()
-					end
-
-					--Light, particles and sound
-					PointLight(mt.pos, 1, 0.7, 0.5, 3)
-					if muzzlec == 1 then
-					PlaySound(silencedshoot)
-					else
-					PlaySound(shootSnd[math.random(0,#shootSnd)])
-					end
-
-					smoke = math.min(1.0, smoke + 0.1)
-					coolDown = 0.08
-					charginghandletime = 0.07
-					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1)
-				end
-			end
-			PlayHaptic(shootHaptic, 1)
-		else
-			angVel = math.max(0, angVel - dt*1000)
-		end
-	
-		--Emit smoke from the pipe, but not when firing
-		if InputDown("usetool") and magazine > 0 then
-			if smoke > 0 then
-				if particleTimer < 0.0 then
-					particleTimer = dt + (1.0-smoke)*0.05
-					local forward = TransformToParentVec(bt, Vec(0, 0, 0))
-					local vel = VecScale(forward, 0.5/ dt)
-					local startColour = math.random(20,55)/100
-					local endColour = math.random(1,10)/100
-					ParticleColor(startColour ,startColour ,startColour ,endColour ,endColour ,endColour )
-					vel = VecAdd(vel, Vec(0, rnd(0, 2), 0))
-					ParticleType("plain")
-					ParticleEmissive(1, 0.1,"easeout")
-					ParticleRadius(0.08, 0.15)
-					ParticleDrag(5)
-					ParticleAlpha(1, 0)
-					ParticleCollide(0)
-					SpawnParticle(mt.pos, VecAdd(vel, rndVec(0.1)), 2.0)
-				end
-			end
-		end
-		particleTimer = particleTimer - dt
-	
-		reloadtimer = reloadtimer - dt
-		coolDown = coolDown - dt
-		angle = angle + angVel*dt
-		charginghandletime = charginghandletime - dt
-		
-		--------------------------------------------
-		-----\/ WHERE THE LASER POINT NOW AT \/-----
-		--------------------------------------------
-		--\/ this line is stolen from line 393
-		local attachmentPoint = Transform(VecScale(Vec(0, 1.2, -12), 0.05))
-		--\/ this line defines the laserlightTransform in world vec, done by translating the local vec inside the tool body out of the tool body
-		local laserlightTransfrom=TransformToParentTransform(GetBodyTransform(GetToolBody()), attachmentPoint)
-		--\/ just in case its a nil, can remove this if statement if you want, its not needed
-		if laserlightTransfrom~=nil and rails == 1 then
-			laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
-			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
-			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
-			PointLight(pointpos, 1, 0.1, 0.07,.2)
-			DrawLine(pointpos,laserlightTransfrom.pos, 1, 0.1, 0.07, .15)
-		end
-		if laserlightTransfrom~=nil and rails == 2 then
-			laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
-			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
-			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
-			PointLight(pointpos, 0, 1, 0,.2)
-			DrawLine(pointpos,laserlightTransfrom.pos, 0, 1, 0, .15)
-		end
-		if laserlightTransfrom~=nil and rails == 3 then
-			laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
-			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
-			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
-			PointLight(pointpos, 1, 0, 0.5,.2)
-			DrawLine(pointpos,laserlightTransfrom.pos, 1, 0, 0.5, .15)
-		end
-		
-		--Move tool a bit to the right and recoil
-		local t = Transform()
-		local recoil = math.max(0, coolDown)
-		---toolAnimator.offsetTransform = Transform(Vec(0,0,recoil))
-		toolAnimator.offsetTransform = Transform(Vec(0,0,recoil/2), QuatEuler(recoil*math.random(20, 30), recoil*math.random(-10, 10), 0))
-		tickToolAnimator(toolAnimator, dt)
-		if InputDown("shift") and not aiming and not reloading and not attachmentmenu and not InputDown("usetools") then 
-		low = true
-		SetPlayerWalkingSpeed(10.0)
-		else
-		low = false
-		SetPlayerWalkingSpeed(7.0)
-		end
-		
-		if low then
-		toolAnimator.offsetTransform = (Transform(Vec(0, -0.01, 0), QuatEuler(-20, 40, 0)))
-		tickToolAnimator(toolAnimator, dt)
-		end
-		if aiming then
-		toolAnimator.offsetTransform = (Transform(Vec(-0.1085, 0.044, recoil/2), QuatEuler(0, 0, 0)))
-		tickToolAnimator(toolAnimator, dt)
-		if optics == 2 then
-		toolAnimator.offsetTransform = (Transform(Vec(-0.1085, 0.003, recoil/2), QuatEuler(0, 0, 0)))
-		tickToolAnimator(toolAnimator, dt)
-		end
-		if optics == 3 then
-		toolAnimator.offsetTransform = (Transform(Vec(-0.1085, 0.017, recoil/2), QuatEuler(0, 0, 0)))
-		tickToolAnimator(toolAnimator, dt)
-		end
-		if InputDown("shift") then
-		toolAnimator.offsetTransform = (Transform(Vec(-0.108, 0.005, recoil/2), QuatEuler(0, 0, 30)))
-		tickToolAnimator(toolAnimator, dt)
-		SetCameraFov(80)
-		end
-		end
-		
-		if reloading then
-		toolAnimator.offsetTransform = (Transform(Vec(0, -0.01, 0), QuatEuler(10, 20, -35)))
-		tickToolAnimator(toolAnimator, dt)
-		end
-		
-		if attachmentmenu then
-		toolAnimator.offsetTransform = (Transform(Vec(-0.105, -0.01, -0.2), QuatEuler(35, 20, -35)))
-		tickToolAnimator(toolAnimator, dt)
-		end
-
-		--Animate barrel around the attachment point
-		
-		
-	end
-	smoke = math.max(0.0, smoke - dt/0)
 end
 
 function GetAimPos() --where your crosshair is
@@ -591,69 +33,578 @@
 	return forwardPos, hit, distance
 end
 
-function draw()
-
-if GetString("game.player.tool") == "rmwakm" and not reloading and not attachmentmenu and GetBool("game.thirdperson") and not low then
-        local crossX, crossY = UiWorldToPixel(pointpos)
-		local attachmentPoint = Transform(VecScale(Vec(0, 1.2, -12), 0.05))
-		local laserlightTransfrom=TransformToParentTransform(GetBodyTransform(GetToolBody()), attachmentPoint)
-		laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
-			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
-			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
-        UiPush()
-            UiAlign("center middle")
-            UiTranslate(crossX, crossY)
-            UiImage("MOD/sprites/tpscrosshair.png")
-        UiPop()
+function server.init()
+    RegisterTool("rmwakm", "AKM", "MOD/prefab/minigun.xml")
+    SetBool("game.tool.rmwakm.enabled", true, true)
+     SetToolTransform(Transform(Vec(0, 0, 0)), 0) 
+       tool_initialized = false
+    angle = 0
+    angVel = 0
+    coolDown = 0
+    smoke = 0
+    magazine = 31
+    aiming = false
+    fireswitch = false
+    reloading = false
+    reloadtimer = 0
+    nocasings = GetBool("savegame.mod.nocasings")
+    optics = 0
+    grips = 0
+    muzzlec = 0
+    rails = 0
+    attachmentmenu = false
+    recoilshake = 0.48
+    zoomfov = 55
+       charginghandletime = 0
+    stocks = 1
+    autospread = 0.01
+    spread = 0.002
+    low = false
+    semi = 0
+    hands = 1
+    local offset = Transform(Vec(0.5, 0, 0))
+    SetToolTransform(offset, 0)
+    shootSnd = {}
+    shootHaptic = LoadHaptic("MOD/haptic/gun_fire.xml")
+    local toolHaptic = LoadHaptic("MOD/haptic/background.xml")
+    SetToolHaptic("rmwakm", toolHaptic);
+    oldPipePos = Vec()
+    particleTimer = 0
+end
+
+function server.tick(dt)
+       local tool_transform = GetToolLocationWorldTransform()
+       -- If the tool is initialized, set the transform with no sway
+       if tool_transform then
+           if not tool_initialized then
+               print("Tool initialized, disabling sway.")
+               tool_initialized = true
+           end
+           SetToolTransform(tool_transform, 0)  -- Disable sway by setting to 0
+       else
+           -- If the tool is not initialized, keep trying until it's available
+           print("Tool transform not available yet.")
+       end
+    --Check if rmwakm is selected
+    smoke = math.max(0.0, smoke - dt/0)
+end
+
+function client.init()
+    for i=0, 7 do
+    	shootSnd[i] = LoadSound("MOD/snd/rifle.ogg")
     end
-	
-if GetString("game.player.tool") == "rmwakm" and not fireswitch and not reloading and not attachmentmenu then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(magazine.." (7.62x39mm) Auto")
-				
-				
-			end
-
-if GetString("game.player.tool") == "rmwakm" and fireswitch and not reloading and not attachmentmenu then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(magazine.." (7.62x39mm) Semi")
-			
-			end
-			
-if GetString("game.player.tool") == "rmwakm" and reloading and not attachmentmenu then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText(" RELOADING...")
-				
-				
-			end
-if GetString("game.player.tool") == "rmwakm" and not reloading and attachmentmenu then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(0.8, 0.8, 0.8)
-			UiFont("bold.ttf", 31)
-			UiTextOutline(0,0,0,1,0.1)
-			UiText("Attachments: [O-Sights] [P-Underbarrel] [K-Muzzle] [L-Rails] [I-Stock] [H-Hands]")
-				
-			end
-			
-			
-			end
-			
-			
-
+end
+
+function client.tick(dt)
+    	if GetString("game.player.tool") == "rmwakm" then
+            local mt = GetToolLocationWorldTransform("muzzle")
+    		local at = GetToolLocationWorldTransform("acog")
+    		local ht = GetToolLocationWorldTransform("holo")
+    		local a = GetToolBody()
+    		local opticssight = GetBodyShapes(a)
+    		local b = GetToolBody()
+    		local foregrips = GetBodyShapes(b)
+    		local c = GetToolBody()
+    		local muzzles = GetBodyShapes(c)
+    		local d = GetToolBody()
+    		local railings = GetBodyShapes(d)
+
+    			SetBool("hud.aimdot", false, true)
+
+            if optics > 3 then optics = 0 
+    		end
+    		if grips > 2 then grips = 0 
+    		end
+    		if stocks > 2 then stocks = 0 
+    		end
+    		if muzzlec > 1 then muzzlec = 0 
+    		end
+    		if rails > 3 then rails = 0 
+    		end
+    		if hands > 2 then hands = 0 
+    		end
+    if InputReleased("usetool") then semi = 0 
+    		end
+
+    		if semi > 1 then semi = 1 
+    		end
+
+           if InputDown("t") and not reloading then attachmentmenu = true ---Turn on the attachment selection Menu
+    			coolDown = 0.09
+
+    			aiming = false
+    		else attachmentmenu = false
+    			end
+
+    		if InputPressed("mmb") == true and fireswitch == false then fireswitch = true
+    			coolDown = 0.09
+    			PlaySound(fireselector)
+    			end
+
+    		if InputPressed("mmb") == true and fireswitch == true and coolDown < 0 then 
+    			fireswitch = false
+    			PlaySound(fireselector)
+    			end
+
+    			if InputPressed("o") and attachmentmenu then 
+    			optics = optics + 1
+    			end
+
+    			if InputPressed("i") and attachmentmenu then 
+    			stocks = stocks + 1
+    			end
+
+    			if InputPressed("p") and attachmentmenu then 
+    			grips = grips + 1
+    			end
+
+    			if InputPressed("k") and attachmentmenu then 
+    			muzzlec = muzzlec + 1
+    			end
+
+    			if InputPressed("l") and attachmentmenu then 
+    			rails = rails + 1
+    			end
+    			if InputPressed("h") and attachmentmenu then 
+    			hands = hands + 1
+    			end
+    			if GetString("game.player.tool") == "rmwakm" then --- When Zero then its empty
+
+    			local optic = opticssight[9]
+                    if charginghandletime ~= 0 then ---Charginghandle
+    					SetShapeLocalTransform(optic, Transform(Vec(0.01, 0.125, -0.1), QuatEuler(-90, 0, 0)))
+    				else
+    					SetShapeLocalTransform(optic, Transform(Vec(0.01, 0.125, -0.2), QuatEuler(-90, 0, 0)))
+                    end
+
+    			local optic = opticssight[8]
+                    if reloadtimer > 1 then ---Magazine
+    					SetTag(optic, "invisible")
+    				else
+    				RemoveTag(optic, "invisible")
+                    end
+
+    			 for i = 1, #opticssight do
+                    local optic = opticssight[1]
+                    if optics == 1 or optics == 2 or optics == 3 then ---Mount
+                        RemoveTag(optic, "invisible")
+
+    					SetShapeLocalTransform(optic, Transform(Vec(-0.05, 0.06, -0.1), QuatEuler(-90, 0, 0)))
+    				else
+    				SetTag(optic, "invisible")
+
+                    end
+    				local optic = opticssight[2]
+                    if optics == 2 then ---Acog
+                        RemoveTag(optic, "invisible")
+
+    					SetShapeLocalTransform(optic, Transform(Vec(-0.037, 0.19, -0.07), QuatEuler(-90, 0, 0)))
+    				else
+    				SetTag(optic, "invisible")
+
+                    end
+
+    				local optic = opticssight[3]
+                    if optics == 3 then ---Holo
+                        RemoveTag(optic, "invisible")
+
+    					SetShapeLocalTransform(optic, Transform(Vec(-0.025, 0.165, -0.15), QuatEuler(-90, 0, 0)))
+    				else
+    				SetTag(optic, "invisible")
+
+                    end
+    				local stock = opticssight[10]
+                    if stocks == 1 then ---Stock
+                        RemoveTag(stock, "invisible")
+
+    				else
+    					SetTag(stock, "invisible")
+
+                    end
+    				local stock = opticssight[11]
+                    if stocks == 2 then ---Stock
+                        RemoveTag(stock, "invisible")
+
+    				else
+    					SetTag(stock, "invisible")
+
+                    end
+                    for i = 1, #foregrips do
+                    local grip = foregrips[4] ---Vertical Grip
+                    if grips == 1 then
+                        RemoveTag(grip, "invisible")
+
+    				else
+    					SetTag(grip, "invisible")
+
+                    end
+
+    				local grip = foregrips[5] ---Angled Grip
+                    if grips == 2 then
+                        RemoveTag(grip, "invisible")
+    					SetShapeLocalTransform(grip, Transform(Vec(-0.025, 0.013, -0.45), QuatEuler(-90, 0, 0)))
+    				else
+    					SetTag(grip, "invisible")
+
+                    end
+
+    				local hand1 = foregrips[12] ---lets try some hands... here we fucking go.
+                    if not GetBool("game.thirdperson") and not reloading and not attachmentmenu and hands == 1 then
+                        RemoveTag(hand1, "invisible")
+    					SetShapeLocalTransform(hand1, Transform(Vec(-0.25, -0.14, -0.21), QuatEuler(-90, 45, 20)))
+    				else
+    					SetTag(hand1, "invisible")
+
+                    end
+    				local hand2 = foregrips[13] ---lets try some hands... here we fucking go. take two.
+                    if not GetBool("game.thirdperson") and hands == 1 then
+                        RemoveTag(hand2, "invisible")
+    					SetShapeLocalTransform(hand2, Transform(Vec(0.0765, -0.05, 0.1), QuatEuler(-90, 20, 0)))
+    				else
+    					SetTag(hand2, "invisible")
+
+                    end
+    				local hand1 = foregrips[14] ---lets try some hands... here we fucking go.
+                    if not GetBool("game.thirdperson") and not reloading and not attachmentmenu and hands == 2 then
+                        RemoveTag(hand1, "invisible")
+    					SetShapeLocalTransform(hand1, Transform(Vec(-0.25, -0.14, -0.21), QuatEuler(-90, 45, 20)))
+    				else
+    					SetTag(hand1, "invisible")
+
+                    end
+    				local hand2 = foregrips[15] ---lets try some hands... here we fucking go. take two.
+                    if not GetBool("game.thirdperson") and hands == 2 then
+                        RemoveTag(hand2, "invisible")
+    					SetShapeLocalTransform(hand2, Transform(Vec(0.0765, -0.05, 0.1), QuatEuler(-90, 20, 0)))
+    				else
+    					SetTag(hand2, "invisible")
+
+                    end
+                    for i = 1, #muzzles do
+                    local muzzle = muzzles[6] ---Silencer
+                    if muzzlec == 1 then 
+                        RemoveTag(muzzle, "invisible")
+
+    				else
+    					SetTag(muzzle, "invisible")
+
+                    end
+    				for i = 1, #railings do
+                    local rail = railings[7] ---Laser
+                    if rails ~= 0 then 
+                        RemoveTag(rail, "invisible")
+
+    				else
+    					SetTag(rail, "invisible")
+
+                    end
+
+                end
+
+                end
+                end
+                end
+    			end
+
+    		if InputDown("rmb") and not reloading and not attachmentmenu then 
+    		aiming = true
+    		else aiming = false
+    			end
+
+    			if aiming then
+    			SetCameraFov(80)
+    			spread = 0.002
+    			autospread = 0.002
+
+    			if optics == 2 then
+    			SetCameraFov(30)
+    			if not InputDown("a") and not InputDown("d") and not InputDown("shift") then
+    			DrawSprite(reticlesprite, at, 0.04, 0.04, 1, 1, 1, 1)
+    			end
+    			end
+    			if optics == 3 and not InputDown("a") and not InputDown("d") and not InputDown("shift") then
+    			DrawSprite(donoutreticlesprite, ht, 0.01, 0.01, 1, 1, 1, 1)
+    			end
+    			else
+    			spread = 0.002
+    			autospread = 0.01
+    			end
+
+    			if InputPressed("r") and magazine < 31 and not InputDown("usetool") and not reloading and not attachmentmenu then
+    				reloadtimer = 2.3
+    				PlaySound(reloadsound1)
+    				aiming = false
+    				reloading = true
+    			end
+
+    			if reloadtimer < 0 and reloading == true then
+    			magazine = 31
+    			PlaySound(reloadsound2)
+    			reloading = false
+    			charginghandletime = 0.1
+    			end
+
+    			if grips == 1 or grips == 2 then
+    			recoilshake = 0.52
+
+    			end
+
+    			if grips == 0 or grips == 3 then
+    			recoilshake = 0.61
+
+    			end
+
+    			if stocks == 0 then
+    			recoilshake = recoilshake + 0.12
+    			else
+    			recoilshake = recoilshake - 0.12
+    			end
+
+    		if GetBool("game.player.canusetool") and InputDown("usetool") and not attachmentmenu and GetInt("game.tool.gun.ammo") > 0 and magazine > 0 and fireswitch and not low and not reloading and semi < 1 then
+    			angVel = math.min(1000, angVel + dt*9000)	
+    			if angVel == 1000 then
+    				if coolDown < 0 then
+                        local _, p, _, d = GetPlayerAimInfo(mt.pos)
+                        d = VecAdd(d, rndVec(spread))
+    					Shoot(p, d, "bullet", 0.15)
+    					Shoot(p, d, "bullet", 0.15)
+    					Shoot(p, d, "bullet", 0.15)
+
+    					magazine = magazine - 1
+    					semi = semi + 1
+    					ShakeCamera(recoilshake)
+    					if muzzlec == 0 then
+    					DrawSprite(muzzleflash, mt, 0.3, 0.3, 1, 1, 1, 1, true)
+    					end
+    					SetCameraOffsetTransform(Transform(Vec(x, y, 0.07), QuatEuler(x, y, 2)), true)
+    					if not nocasings then
+    					SpentCasing()
+    					end
+
+    					--Light, particles and sound
+    					PointLight(mt.pos, 1, 0.7, 0.5, 3)
+    					if muzzlec == 1 then
+    					PlaySound(silencedshoot)
+    					else
+    					PlaySound(shootSnd[math.random(0,#shootSnd)])
+    					end
+
+    					smoke = math.min(1.0, smoke + 0.1)
+    					coolDown = 0.08
+    					charginghandletime = 0.07
+    					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1, true)
+    				end
+    			end
+    			PlayHaptic(shootHaptic, 1)
+    		else
+    			angVel = math.max(0, angVel - dt*1000)
+    		end
+
+    		--Check if firing
+    		if GetBool("game.player.canusetool") and InputDown("usetool") and not attachmentmenu and not reloading and GetInt("game.tool.gun.ammo") > 0 and magazine > 0 and not low and not fireswitch then
+    			angVel = math.min(1000, angVel + dt*9000)	
+    			if angVel == 1000 then
+    				if coolDown < 0 then
+                        local _, p, _, d = GetPlayerAimInfo(mt.pos)
+                        d = VecAdd(d, rndVec(autospread))
+    					Shoot(p, d, "bullet", 0.15)
+    					Shoot(p, d, "bullet", 0.15)
+    					Shoot(p, d, "bullet", 0.15)
+
+    					magazine = magazine - 1
+    					ShakeCamera(recoilshake)
+    					if muzzlec == 0 then
+    					DrawSprite(muzzleflash, mt, 0.3, 0.3, 1, 1, 1, 1, true)
+    					end
+    					SetCameraOffsetTransform(Transform(Vec(x, y, 0.07), QuatEuler(x, y, 2)), true)
+    					if not nocasings then
+    					SpentCasing()
+    					end
+
+    					--Light, particles and sound
+    					PointLight(mt.pos, 1, 0.7, 0.5, 3)
+    					if muzzlec == 1 then
+    					PlaySound(silencedshoot)
+    					else
+    					PlaySound(shootSnd[math.random(0,#shootSnd)])
+    					end
+
+    					smoke = math.min(1.0, smoke + 0.1)
+    					coolDown = 0.08
+    					charginghandletime = 0.07
+    					SetInt("game.tool.gun.ammo", GetInt("game.tool.gun.ammo")-1, true)
+    				end
+    			end
+    			PlayHaptic(shootHaptic, 1)
+    		else
+    			angVel = math.max(0, angVel - dt*1000)
+    		end
+
+    		--Emit smoke from the pipe, but not when firing
+    		if InputDown("usetool") and magazine ~= 0 then
+    			if smoke ~= 0 then
+    				if particleTimer < 0.0 then
+    					particleTimer = dt + (1.0-smoke)*0.05
+    					local forward = TransformToParentVec(bt, Vec(0, 0, 0))
+    					local vel = VecScale(forward, 0.5/ dt)
+    					local startColour = math.random(20,55)/100
+    					local endColour = math.random(1,10)/100
+    					ParticleColor(startColour ,startColour ,startColour ,endColour ,endColour ,endColour )
+    					vel = VecAdd(vel, Vec(0, rnd(0, 2), 0))
+    					ParticleType("plain")
+    					ParticleEmissive(1, 0.1,"easeout")
+    					ParticleRadius(0.08, 0.15)
+    					ParticleDrag(5)
+    					ParticleAlpha(1, 0)
+    					ParticleCollide(0)
+    					SpawnParticle(mt.pos, VecAdd(vel, rndVec(0.1)), 2.0)
+    				end
+    			end
+    		end
+    		particleTimer = particleTimer - dt
+
+    		reloadtimer = reloadtimer - dt
+    		coolDown = coolDown - dt
+    		angle = angle + angVel*dt
+    		charginghandletime = charginghandletime - dt
+
+    		--------------------------------------------
+    		-----\/ WHERE THE LASER POINT NOW AT \/-----
+    		--------------------------------------------
+    		--\/ this line is stolen from line 393
+    		local attachmentPoint = Transform(VecScale(Vec(0, 1.2, -12), 0.05))
+    		--\/ this line defines the laserlightTransform in world vec, done by translating the local vec inside the tool body out of the tool body
+    		local laserlightTransfrom=TransformToParentTransform(GetBodyTransform(GetToolBody()), attachmentPoint)
+    		--\/ just in case its a nil, can remove this if statement if you want, its not needed
+    		if laserlightTransfrom~=nil and rails == 1 then
+    			laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
+    			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
+    			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
+    			PointLight(pointpos, 1, 0.1, 0.07,.2)
+    			DrawLine(pointpos,laserlightTransfrom.pos, 1, 0.1, 0.07, .15)
+    		end
+    		if laserlightTransfrom~=nil and rails == 2 then
+    			laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
+    			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
+    			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
+    			PointLight(pointpos, 0, 1, 0,.2)
+    			DrawLine(pointpos,laserlightTransfrom.pos, 0, 1, 0, .15)
+    		end
+    		if laserlightTransfrom~=nil and rails == 3 then
+    			laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
+    			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
+    			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
+    			PointLight(pointpos, 1, 0, 0.5,.2)
+    			DrawLine(pointpos,laserlightTransfrom.pos, 1, 0, 0.5, .15)
+    		end
+
+    		--Move tool a bit to the right and recoil
+    		local t = Transform()
+    		local recoil = math.max(0, coolDown)
+    		---toolAnimator.offsetTransform = Transform(Vec(0,0,recoil))
+    		toolAnimator.offsetTransform = Transform(Vec(0,0,recoil/2), QuatEuler(recoil*math.random(20, 30), recoil*math.random(-10, 10), 0))
+    		tickToolAnimator(toolAnimator, dt)
+    		if InputDown("shift") and not aiming and not reloading and not attachmentmenu and not InputDown("usetools") then 
+    		low = true
+    		SetPlayerWalkingSpeed(10.0)
+    		else
+    		low = false
+    		SetPlayerWalkingSpeed(7.0)
+    		end
+
+    		if low then
+    		toolAnimator.offsetTransform = (Transform(Vec(0, -0.01, 0), QuatEuler(-20, 40, 0)))
+    		tickToolAnimator(toolAnimator, dt)
+    		end
+    		if aiming then
+    		toolAnimator.offsetTransform = (Transform(Vec(-0.1085, 0.044, recoil/2), QuatEuler(0, 0, 0)))
+    		tickToolAnimator(toolAnimator, dt)
+    		if optics == 2 then
+    		toolAnimator.offsetTransform = (Transform(Vec(-0.1085, 0.003, recoil/2), QuatEuler(0, 0, 0)))
+    		tickToolAnimator(toolAnimator, dt)
+    		end
+    		if optics == 3 then
+    		toolAnimator.offsetTransform = (Transform(Vec(-0.1085, 0.017, recoil/2), QuatEuler(0, 0, 0)))
+    		tickToolAnimator(toolAnimator, dt)
+    		end
+    		if InputDown("shift") then
+    		toolAnimator.offsetTransform = (Transform(Vec(-0.108, 0.005, recoil/2), QuatEuler(0, 0, 30)))
+    		tickToolAnimator(toolAnimator, dt)
+    		SetCameraFov(80)
+    		end
+    		end
+
+    		if reloading then
+    		toolAnimator.offsetTransform = (Transform(Vec(0, -0.01, 0), QuatEuler(10, 20, -35)))
+    		tickToolAnimator(toolAnimator, dt)
+    		end
+
+    		if attachmentmenu then
+    		toolAnimator.offsetTransform = (Transform(Vec(-0.105, -0.01, -0.2), QuatEuler(35, 20, -35)))
+    		tickToolAnimator(toolAnimator, dt)
+    		end
+
+    		--Animate barrel around the attachment point
+
+    	end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "rmwakm" and not reloading and not attachmentmenu and GetBool("game.thirdperson") and not low then
+            local crossX, crossY = UiWorldToPixel(pointpos)
+    		local attachmentPoint = Transform(VecScale(Vec(0, 1.2, -12), 0.05))
+    		local laserlightTransfrom=TransformToParentTransform(GetBodyTransform(GetToolBody()), attachmentPoint)
+    		laserForwardTransform=TransformToParentVec(laserlightTransfrom,Vec(0,0,-1))
+    			hit,dist=QueryRaycast(laserlightTransfrom.pos,laserForwardTransform,500)
+    			pointpos=VecAdd(laserlightTransfrom.pos,VecScale(laserForwardTransform,dist))
+            UiPush()
+                UiAlign("center middle")
+                UiTranslate(crossX, crossY)
+                UiImage("MOD/sprites/tpscrosshair.png")
+            UiPop()
+        end
+
+    if GetString("game.player.tool") == "rmwakm" and not fireswitch and not reloading and not attachmentmenu then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			UiText(magazine.." (7.62x39mm) Auto")
+
+    			end
+
+    if GetString("game.player.tool") == "rmwakm" and fireswitch and not reloading and not attachmentmenu then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			UiText(magazine.." (7.62x39mm) Semi")
+
+    			end
+
+    if GetString("game.player.tool") == "rmwakm" and reloading and not attachmentmenu then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(1, 1, 1)
+    			UiFont("bold.ttf", 32)
+    			UiTextOutline(0,0,0,1,0.1)
+    			UiText(" RELOADING...")
+
+    			end
+    if GetString("game.player.tool") == "rmwakm" and not reloading and attachmentmenu then
+    		UiPush()
+    			UiTranslate(UiCenter(), UiHeight()-60)
+    			UiAlign("center middle")
+    			UiColor(0.8, 0.8, 0.8)
+    			UiFont("bold.ttf", 31)
+    			UiTextOutline(0,0,0,1,0.1)
+    			UiText("Attachments: [O-Sights] [P-Underbarrel] [K-Muzzle] [L-Rails] [I-Stock] [H-Hands]")
+
+    			end
+end
+

```
