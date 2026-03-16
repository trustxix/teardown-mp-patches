# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,25 +1,4 @@
-function init()
-	RegisterTool("guided", "Guided Missile", "MOD/vox/stinger.vox", 4)
-	SetBool("game.tool.guided.enabled", true)
-	SetString("game.tool.guided.ammo.display","")
-	SetFloat("game.tool.guided.ammo", 101)
-
-	guidedexplosionSound = LoadSound("MOD/snd/explosion.ogg")
-	guidedflyingSound = LoadLoop("MOD/snd/rocket_loop.ogg")
-	guidedfireSound = LoadSound("tools/launcher0.ogg")
-	guidedboosterSound = LoadLoop("MOD/snd/booster.ogg")
-	guidedmissileSprite = LoadSprite("MOD/img/missile.png")
-	guidedmissileStrength = 20
-	guidedmissileSpeed = 20
-	guidedmissile = {}
-	guidedcamdist = 2
-	
-	guidedflying = false
-	guideddetached = false
-	guidedprimed = false
-	piercing = false
-end
-
+#version 2
 function GuidedExplode()
 	PlaySound(guidedexplosionSound, guidedmissile.pos, 8, false)
 	Explosion(guidedmissiletip, guidedmissileStrength/10)
@@ -46,109 +25,132 @@
 	end
 end
 
-function tick()
-	if GetString("game.player.tool") == "guided" and GetPlayerVehicle() == 0 then
-		if InputPressed("lmb") then
-			if not guidedflying and not guideddetached then
-				guidedflying = true
-				PlaySound(guidedfireSound)
-				rocketProjectile = Spawn("MOD/vox/rocket.xml", rocketTrans)
-			end
+function server.init()
+    RegisterTool("guided", "Guided Missile", "MOD/vox/stinger.vox", 4)
+    SetBool("game.tool.guided.enabled", true, true)
+    SetString("game.tool.guided.ammo.display","", true)
+    SetFloat("game.tool.guided.ammo", 101, true)
+    guidedflyingSound = LoadLoop("MOD/snd/rocket_loop.ogg")
+    guidedboosterSound = LoadLoop("MOD/snd/booster.ogg")
+    guidedmissileSprite = LoadSprite("MOD/img/missile.png")
+    guidedmissileStrength = 20
+    guidedmissileSpeed = 20
+    guidedmissile = {}
+    guidedcamdist = 2
+    guidedflying = false
+    guideddetached = false
+    guidedprimed = false
+    piercing = false
+end
 
-			if guidedprimed and guidedflying or guideddetached then
-				GuidedExplode()
-			end
-		end
+function client.init()
+    guidedexplosionSound = LoadSound("MOD/snd/explosion.ogg")
+    guidedfireSound = LoadSound("tools/launcher0.ogg")
+end
 
-		if InputPressed("rmb") then
-			if guidedflying then
-				guidedflying = false
-				guideddetached = true
-			end
-		end
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "guided" and GetPlayerVehicle(playerId) == 0 then
+    	if InputPressed("lmb") then
+    		if not guidedflying and not guideddetached then
+    			guidedflying = true
+    			PlaySound(guidedfireSound)
+    			rocketProjectile = Spawn("MOD/vox/rocket.xml", rocketTrans)
+    		end
 
-		if InputPressed("R") then 
-			piercing = not piercing
-			SetString("hud.notification", "Piercing rocket "..(piercing and "on" or "off"))
-		end
+    		if guidedprimed and guidedflying or guideddetached then
+    			GuidedExplode()
+    		end
+    	end
 
-		local b = GetToolBody()
-		if b ~= 0 then
-			if body ~= b then
-				body = b
-				local shapes = GetBodyShapes(b)
-				rocket = shapes[2]
-				rocketTrans = GetShapeLocalTransform(rocket)
-			end
-		end
-	end
+    	if InputPressed("rmb") then
+    		if guidedflying then
+    			guidedflying = false
+    			guideddetached = true
+    		end
+    	end
 
-	if guidedflying and InputValue("mousewheel") ~= 0 then
-		guidedflying = false
-		guideddetached = true
-	end
+    	if InputPressed("R") then 
+    		piercing = not piercing
+    		SetString("hud.notification", "Piercing rocket "..(piercing and "on" or "off"), true)
+    	end
 
-	if guidedflying then
-		local mx, my, s = InputValue("mousedx"), InputValue("mousedy"), InputDown("space")
-	
-		local guidedct = GetCameraTransform()
-		if not guidedmissile.pos then guidedmissile.pos = guidedct.pos end
-		if not guidedmissile.rot then guidedmissile.rot = guidedct.rot end
-		if s then 
-			guidedmissileSpeed = 40
-			PlayLoop(guidedboosterSound, guidedmissile.pos, 0.6, false)
-			mx = mx * 0.75
-			my = my * 0.75
-		else 
-			guidedmissileSpeed = 20
-		end
+    	local b = GetToolBody()
+    	if b ~= 0 then
+    		if body ~= b then
+    			body = b
+    			local shapes = GetBodyShapes(b)
+    			rocket = shapes[2]
+    			rocketTrans = GetShapeLocalTransform(rocket)
+    		end
+    	end
+    end
+    if guidedflying and InputValue("mousewheel") ~= 0 then
+    	guidedflying = false
+    	guideddetached = true
+    end
+    if guidedflying then
+    	local mx, my, s = InputValue("mousedx"), InputValue("mousedy"), InputDown("space")
 
-		local forwPos = TransformToParentPoint(guidedmissile, Vec(0, 0, -5))
-		guidedmissile.pos = TransformToParentPoint(guidedmissile, Vec(0, 0, -(guidedmissileSpeed/100)))
-		guidedmissile.rot = QuatLookAt(guidedmissile.pos, forwPos)
-		guidedmissile.rot = QuatRotateQuat(guidedmissile.rot, QuatEuler(-my/10, -mx/10, 0))
-		guidedmissiletip = TransformToParentPoint(guidedmissile, Vec(0, 0, -1.1))
-		guidedsmokepos = TransformToParentPoint(guidedmissile, Vec(0, 0, 0.9))
+    	local guidedct = GetCameraTransform()
+    	if not guidedmissile.pos then guidedmissile.pos = guidedct.pos end
+    	if not guidedmissile.rot then guidedmissile.rot = guidedct.rot end
+    	if s then 
+    		guidedmissileSpeed = 40
+    		PlayLoop(guidedboosterSound, guidedmissile.pos, 0.6, false)
+    		mx = mx * 0.75
+    		my = my * 0.75
+    	else 
+    		guidedmissileSpeed = 20
+    	end
 
-		guidedflycam = {}
-		guidedflycam.pos = TransformToParentPoint(guidedmissile, Vec(0, guidedcamdist/3, guidedcamdist))
-		guidedflycam.rot = QuatCopy(guidedmissile.rot)
+    	local forwPos = TransformToParentPoint(guidedmissile, Vec(0, 0, -5))
+    	guidedmissile.pos = TransformToParentPoint(guidedmissile, Vec(0, 0, -(guidedmissileSpeed/100)))
+    	guidedmissile.rot = QuatLookAt(guidedmissile.pos, forwPos)
+    	guidedmissile.rot = QuatRotateQuat(guidedmissile.rot, QuatEuler(-my/10, -mx/10, 0))
+    	guidedmissiletip = TransformToParentPoint(guidedmissile, Vec(0, 0, -1.1))
+    	guidedsmokepos = TransformToParentPoint(guidedmissile, Vec(0, 0, 0.9))
 
-		SetCameraTransform(guidedflycam)
+    	guidedflycam = {}
+    	guidedflycam.pos = TransformToParentPoint(guidedmissile, Vec(0, guidedcamdist/3, guidedcamdist))
+    	guidedflycam.rot = QuatCopy(guidedmissile.rot)
 
-		local width = 0.5
-		local length = 1.5
-		local spritepos = TransformToParentPoint(guidedmissile, Vec(0, 0, -0.75))
-		local rot = QuatLookAt(guidedmissile.pos, guidedmissiletip)
-		rocketWorldtransform = Transform(spritepos, rot)
+    	SetCameraTransform(guidedflycam)
 
-		SetBodyTransform(rocketProjectile[1], rocketWorldtransform)
+    	local width = 0.5
+    	local length = 1.5
+    	local spritepos = TransformToParentPoint(guidedmissile, Vec(0, 0, -0.75))
+    	local rot = QuatLookAt(guidedmissile.pos, guidedmissiletip)
+    	rocketWorldtransform = Transform(spritepos, rot)
 
-		PlayLoop(guidedflyingSound, guidedmissile.pos, 0.2, false)
-		SpawnParticle("fire", guidedsmokepos, Vec(0, 0, 0), 0.75, 0.25)
-		SpawnParticle("smoke", guidedsmokepos, Vec(0, 0, 0), 1, 2)
-		guidedprimed = true
-		GuidedCheckHit()
-	end
+    	SetBodyTransform(rocketProjectile[1], rocketWorldtransform)
 
-	if guideddetached then
-		local guidedct = GetCameraTransform()
-		if not guidedmissile.pos then guidedmissile.pos = guidedct.pos end
-		if not guidedmissile.rot then guidedmissile.rot = guidedct.rot end
+    	PlayLoop(guidedflyingSound, guidedmissile.pos, 0.2, false)
+    	SpawnParticle("fire", guidedsmokepos, Vec(0, 0, 0), 0.75, 0.25)
+    	SpawnParticle("smoke", guidedsmokepos, Vec(0, 0, 0), 1, 2)
+    	guidedprimed = true
+    	GuidedCheckHit()
+    end
 
-		guidedmissile.pos = TransformToParentPoint(guidedmissile, Vec(0, 0, -(guidedmissileSpeed/100)))
-		guidedmissiletip = TransformToParentPoint(guidedmissile, Vec(0, 0, -1.1))
-		guidedsmokepos = TransformToParentPoint(guidedmissile, Vec(0, 0, 1))
+    if guideddetached then
+    	local guidedct = GetCameraTransform()
+    	if not guidedmissile.pos then guidedmissile.pos = guidedct.pos end
+    	if not guidedmissile.rot then guidedmissile.rot = guidedct.rot end
 
-		local size = 0.5
-		local rot = QuatLookAt(guidedmissile.pos, guidedmissiletip)
-		rocketWorldtransform = Transform(guidedmissile.pos, rot)
+    	guidedmissile.pos = TransformToParentPoint(guidedmissile, Vec(0, 0, -(guidedmissileSpeed/100)))
+    	guidedmissiletip = TransformToParentPoint(guidedmissile, Vec(0, 0, -1.1))
+    	guidedsmokepos = TransformToParentPoint(guidedmissile, Vec(0, 0, 1))
 
-		SetBodyTransform(rocketProjectile[1], rocketWorldtransform)
-		PlayLoop(guidedflyingSound, guidedmissile.pos, 0.2, false)
-		SpawnParticle("fire", guidedsmokepos, Vec(0, 0, 0), 0.75, 0.25)
-		SpawnParticle("smoke", guidedsmokepos, Vec(0, 0, 0), 1, 2)
-		guidedprimed = true
-		GuidedCheckHit()
-	end
-end+    	local size = 0.5
+    	local rot = QuatLookAt(guidedmissile.pos, guidedmissiletip)
+    	rocketWorldtransform = Transform(guidedmissile.pos, rot)
+
+    	SetBodyTransform(rocketProjectile[1], rocketWorldtransform)
+    	PlayLoop(guidedflyingSound, guidedmissile.pos, 0.2, false)
+    	SpawnParticle("fire", guidedsmokepos, Vec(0, 0, 0), 0.75, 0.25)
+    	SpawnParticle("smoke", guidedsmokepos, Vec(0, 0, 0), 1, 2)
+    	guidedprimed = true
+    	GuidedCheckHit()
+    end
+end
+

```
