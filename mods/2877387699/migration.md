# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,44 +1,4 @@
--- Airstrike Arsenal script by Cyber
--- Based on minigun script by Tuxedo Labs
-
-function init()
-	RegisterTool("BarrageStrike", "Airstrike designator", "MOD/vox/BarrageStrike.vox")
-	SetBool("game.tool.BarrageStrike.enabled", true)
-	SetFloat("game.tool.BarrageStrike.ammo", 5)
-	nosmoke = GetBool("savegame.mod.nosmoke")
-	nosound = GetBool("savegame.mod.nosound")
-	noshock = GetBool("savegame.mod.noshock")
-	bevery =  GetBool("savegame.mod.bevery")
-	
-	mode = 0
-	coolDown = 0
-	smoke = 0
-	AirstikeEffectstime = -1
-	ModeWait = 0
-	AirstrikeLoc = 0
-	AirstikeEffectscount = 0
-	canfire = 1
-	lighttime = 0
-	MoabTime = 0
-	playsnd = 0
-	shockwave = 0
-	closetomoab = 0
-	light = 330
-	rocketsound = LoadSound("MOD/snd/rocketfire.ogg")
-	bunkersound = LoadSound("MOD/snd/bunkerfire.ogg")
-	moabapp = LoadSound("MOD/snd/moabapp.ogg")
-	moabsnd = LoadSound("MOD/snd/moabsnd.ogg")
-	moabsndapp = LoadSound("MOD/snd/moabsndapp.ogg")
-	moabsndboom = LoadSound("MOD/snd/moabsndboom.ogg")
-	plbustsnd = LoadSound("MOD/snd/plbustsnd.ogg")
-	radiosnd = LoadSound("MOD/snd/engtrgt.ogg")
-	minisnd = LoadSound("MOD/snd/minisnd.ogg")
-	
-	oldPipePos = Vec()
-	particleTimer = 0
-		
-end
-
+#version 2
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -46,80 +6,6 @@
 
 function rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
-end
-
-function tick(dt)
-
-    AirstikeEffectstime = AirstikeEffectstime - dt
-	ModeWait = ModeWait - dt
-	lighttime = lighttime - dt
-	MoabTime = MoabTime - dt
-	lighton()
-	AirstikeEffects()
-	ChangeMode()
-	moabdrop()
-
-	if GetString("game.player.tool") == "BarrageStrike" then
-			
-		local ct = GetCameraTransform()
-		
-		if canfire == 0 then
-			local b = GetToolBody()
-				local shapes = GetBodyShapes(b)
-		
-				if b ~= body then
-					body = b
-					t0 = GetShapeLocalTransform(shapes[2])
-				end
-
-				t = TransformCopy(t0)
-				t.pos = VecAdd(t.pos, Vec(0,0,3))
-				SetShapeLocalTransform(shapes[2], t)
-		else
-			local b = GetToolBody()
-			local shapes = GetBodyShapes(b)
-			if b ~= body then
-				body = b
-				    t0 = GetShapeLocalTransform(shapes[2])
-			end
-
-			t = TransformCopy(t0)
-			t.pos = VecAdd(t.pos, Vec(0,0,0))
-			SetShapeLocalTransform(shapes[2], t)
-		end
-        		
-		if GetBool("game.player.canusetool") and InputDown("usetool") and canfire == 1 and lighttime < 0 then
-		        
-			if coolDown < 0 then
-				local t = GetCameraTransform()
-				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
-				local maxDist = 10000
-				local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist)
-				if not hit then
-					dist = maxDist
-				end
-				
-				local e = VecAdd(t.pos, VecScale(fwd, dist))
-	           				
-				if hit then				
-					AirstrikeLoc = e
-					AirstikeEffectstime = 4
-					AirstikeEffectscount = 1
-					canfire = 0
-					if not nosound then
-						PlaySound(radiosnd)	
-					end
-				end
-
-				smoke = math.min(1.0, smoke + .5)
-				coolDown = 1
-
-			end			
-	    end
-					
-		coolDown = coolDown - dt
-		
-	end		
 end
 
 function lighton()
@@ -217,12 +103,12 @@
 			ParticleSticky(0)
 		end		
 	end	
-end 
+end
 
 function ChangeMode()
 
-    local body = GetPlayerGrabBody()
-	local shape = GetPlayerGrabShape()
+    local body = GetPlayerGrabBody(playerId)
+	local shape = GetPlayerGrabShape(playerId)
 
     if GetString("game.player.tool") == "BarrageStrike" and InputDown("rmb") and canfire == 1 and shape == 0 and body == 0 then
 	    if mode <= 5 and ModeWait < 0 then
@@ -244,40 +130,9 @@
 	end
 end
 
-function draw()
-	if GetString("game.player.tool") == "BarrageStrike" and GetPlayerVehicle() == 0 then
-		UiPush()
-			UiTranslate(UiCenter(), UiHeight()-60)
-			UiAlign("center middle")
-			UiColor(1, 1, 1)
-			UiFont("bold.ttf", 32)
-			UiTextOutline(0,0,0,1,0.1)
-			if canfire == 1 and lighttime < 0 then
-			    if mode == 0 then
-			    UiText("Standard Barrage")
-				elseif mode == 1 then
-				UiText("Heavy Barrage")
-				elseif mode == 2 then
-				UiText("Bunker Buster")
-				elseif mode == 3 then
-				UiText("Wide Heavy Barrage")
-				elseif mode == 4 then
-				UiText("Minigun Fire")
-				elseif mode == 5 then
-				UiText("World Buster")
-				elseif mode == 6 then
-				UiText("M.O.A.B")
-				end
-			else
-			    UiText("RELOADING")
-			end 
-		UiPop()
-	end
-end
-
 function AirstikeEffects()
 
-	if AirstikeEffectstime > 0 then
+	if AirstikeEffectstime ~= 0 then
 		PointLight(AirstrikeLoc, 8, 0, 0, 1)
 	end 
 
@@ -360,13 +215,13 @@
 				end	
 			elseif mode == 5 then	-- world buster	
 				
-				local p = GetPlayerPos()
+				local p = GetPlayerPos(playerId)
 				local a = AirstrikeLoc
 				local x = VecSub(p, a)
 				local px = VecLength(x)
 				
 				if px < 500 then
-				    SetPlayerHealth(0.2) 	
+				    SetPlayerHealth(playerId, 0.2) 	
 				end
 				if not nosound then
 					PlaySound(plbustsnd)
@@ -408,13 +263,13 @@
 			
 				lighttime = 1.79
 				
-			    local p = GetPlayerPos()
+			    local p = GetPlayerPos(playerId)
 				local a = AirstrikeLoc
 				local x = VecSub(p, a)
 				local px = VecLength(x)
 				
 				if px < 55 then
-				    SetPlayerHealth(0.0) 
+				    SetPlayerHealth(playerId, 0.0) 
 					closetomoab = 1
 				end	
 				if not nosound and closetomoab == 0 then
@@ -514,4 +369,152 @@
 			AirstikeEffectscount = 0
 		end 
     end						
-end+end
+
+function server.init()
+    RegisterTool("BarrageStrike", "Airstrike designator", "MOD/vox/BarrageStrike.vox")
+    SetBool("game.tool.BarrageStrike.enabled", true, true)
+    SetFloat("game.tool.BarrageStrike.ammo", 5, true)
+    nosmoke = GetBool("savegame.mod.nosmoke")
+    nosound = GetBool("savegame.mod.nosound")
+    noshock = GetBool("savegame.mod.noshock")
+    bevery =  GetBool("savegame.mod.bevery")
+    mode = 0
+    coolDown = 0
+    smoke = 0
+    AirstikeEffectstime = -1
+    ModeWait = 0
+    AirstrikeLoc = 0
+    AirstikeEffectscount = 0
+    canfire = 1
+    lighttime = 0
+    MoabTime = 0
+    playsnd = 0
+    shockwave = 0
+    closetomoab = 0
+    light = 330
+    oldPipePos = Vec()
+    particleTimer = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+           AirstikeEffectstime = AirstikeEffectstime - dt
+        ModeWait = ModeWait - dt
+        lighttime = lighttime - dt
+        MoabTime = MoabTime - dt
+        lighton()
+        AirstikeEffects()
+        ChangeMode()
+        moabdrop()
+    end
+end
+
+function client.init()
+    rocketsound = LoadSound("MOD/snd/rocketfire.ogg")
+    bunkersound = LoadSound("MOD/snd/bunkerfire.ogg")
+    moabapp = LoadSound("MOD/snd/moabapp.ogg")
+    moabsnd = LoadSound("MOD/snd/moabsnd.ogg")
+    moabsndapp = LoadSound("MOD/snd/moabsndapp.ogg")
+    moabsndboom = LoadSound("MOD/snd/moabsndboom.ogg")
+    plbustsnd = LoadSound("MOD/snd/plbustsnd.ogg")
+    radiosnd = LoadSound("MOD/snd/engtrgt.ogg")
+    minisnd = LoadSound("MOD/snd/minisnd.ogg")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if GetString("game.player.tool") == "BarrageStrike" then
+
+    	local ct = GetCameraTransform()
+
+    	if canfire == 0 then
+    		local b = GetToolBody()
+    			local shapes = GetBodyShapes(b)
+
+    			if b ~= body then
+    				body = b
+    				t0 = GetShapeLocalTransform(shapes[2])
+    			end
+
+    			t = TransformCopy(t0)
+    			t.pos = VecAdd(t.pos, Vec(0,0,3))
+    			SetShapeLocalTransform(shapes[2], t)
+    	else
+    		local b = GetToolBody()
+    		local shapes = GetBodyShapes(b)
+    		if b ~= body then
+    			body = b
+    			    t0 = GetShapeLocalTransform(shapes[2])
+    		end
+
+    		t = TransformCopy(t0)
+    		t.pos = VecAdd(t.pos, Vec(0,0,0))
+    		SetShapeLocalTransform(shapes[2], t)
+    	end
+
+    	if GetBool("game.player.canusetool") and InputDown("usetool") and canfire == 1 and lighttime < 0 then
+
+    		if coolDown < 0 then
+    			local t = GetCameraTransform()
+    			local fwd = TransformToParentVec(t, Vec(0, 0, -1))
+    			local maxDist = 10000
+    			local hit, dist, normal, shape = QueryRaycast(t.pos, fwd, maxDist)
+    			if not hit then
+    				dist = maxDist
+    			end
+
+    			local e = VecAdd(t.pos, VecScale(fwd, dist))
+
+    			if hit then				
+    				AirstrikeLoc = e
+    				AirstikeEffectstime = 4
+    				AirstikeEffectscount = 1
+    				canfire = 0
+    				if not nosound then
+    					PlaySound(radiosnd)	
+    				end
+    			end
+
+    			smoke = math.min(1.0, smoke + .5)
+    			coolDown = 1
+
+    		end			
+        end
+
+    	coolDown = coolDown - dt
+
+    end		
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "BarrageStrike" and GetPlayerVehicle(playerId) == 0 then
+    	UiPush()
+    		UiTranslate(UiCenter(), UiHeight()-60)
+    		UiAlign("center middle")
+    		UiColor(1, 1, 1)
+    		UiFont("bold.ttf", 32)
+    		UiTextOutline(0,0,0,1,0.1)
+    		if canfire == 1 and lighttime < 0 then
+    		    if mode == 0 then
+    		    UiText("Standard Barrage")
+    			elseif mode == 1 then
+    			UiText("Heavy Barrage")
+    			elseif mode == 2 then
+    			UiText("Bunker Buster")
+    			elseif mode == 3 then
+    			UiText("Wide Heavy Barrage")
+    			elseif mode == 4 then
+    			UiText("Minigun Fire")
+    			elseif mode == 5 then
+    			UiText("World Buster")
+    			elseif mode == 6 then
+    			UiText("M.O.A.B")
+    			end
+    		else
+    		    UiText("RELOADING")
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
-	nosmoke = GetBool("savegame.mod.nosmoke")
-	if nosmoke == 0 then nosmoke = 0.15 end
-	nosound = GetBool("savegame.mod.nosound")
-	if nosound == 0 then nosound = 0.15 end
-	noshock = GetBool("savegame.mod.noshock")
-	if noshock == 0 then noshock = 0.15 end
-	bevery = GetBool("savegame.mod.bevery")
-	if bevery == 0 then bevery = 0.15 end
-end
-
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
-
-	UiFont("bold.ttf", 48)
-	UiText("Airstrike Arsenal")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("No smoke or light effects")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(1, 1, 1)
-		if nosmoke then
-		   	if UiTextButton("Yes", 20, 20) then
-				nosmoke = false
-				SetBool("savegame.mod.nosmoke", nosmoke)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				nosmoke = true
-				SetBool("savegame.mod.nosmoke", nosmoke)
-			end
-		end
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("No sound effects")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(1, 1, 1)
-		if nosound then
-		    if UiTextButton("Yes", 20, 20) then
-		        nosound = false
-			    SetBool("savegame.mod.nosound", nosound)
-			end
-		else
-		    if UiTextButton("No", 20, 20) then
-			    nosound = true
-			    SetBool("savegame.mod.nosound", nosound)
-			end
-		end
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("No M.O.A.B shockwave effect")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(1, 1, 1)
-		if noshock then
-		    if UiTextButton("Yes", 20, 20) then
-		        noshock = false
-			    SetBool("savegame.mod.noshock", noshock)
-			end
-		else
-		    if UiTextButton("No", 20, 20) then
-			    noshock = true
-			    SetBool("savegame.mod.noshock", noshock)
-			end
-		end	
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("World buster removes everything")
-		UiTranslate(0, 40)
-		UiAlign("center")
-		UiColor(1, 1, 1)
-		if bevery then
-		    if UiTextButton("Yes", 20, 20) then
-		        bevery = false
-			    SetBool("savegame.mod.bevery", bevery)
-			end
-		else
-		    if UiTextButton("No", 20, 20) then
-			    bevery = true
-			    SetBool("savegame.mod.bevery", bevery)
-			end
-		end	
-
-end
-
+#version 2
 function optionsSlider(val, min, max)
 	UiColor(0.2, 0.6, 1)
 	UiPush()
@@ -105,4 +17,93 @@
 function round(number, decimals)
     local power = 10^decimals
     return math.floor(number * power) / power
-end+end
+
+function server.init()
+    nosmoke = GetBool("savegame.mod.nosmoke")
+    if nosmoke == 0 then nosmoke = 0.15 end
+    nosound = GetBool("savegame.mod.nosound")
+    if nosound == 0 then nosound = 0.15 end
+    noshock = GetBool("savegame.mod.noshock")
+    if noshock == 0 then noshock = 0.15 end
+    bevery = GetBool("savegame.mod.bevery")
+    if bevery == 0 then bevery = 0.15 end
+end
+
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
+
+    UiFont("bold.ttf", 48)
+    UiText("Airstrike Arsenal")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("No smoke or light effects")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(1, 1, 1)
+    	if nosmoke then
+    	   	if UiTextButton("Yes", 20, 20) then
+    			nosmoke = false
+    			SetBool("savegame.mod.nosmoke", nosmoke, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			nosmoke = true
+    			SetBool("savegame.mod.nosmoke", nosmoke, true)
+    		end
+    	end
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("No sound effects")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(1, 1, 1)
+    	if nosound then
+    	    if UiTextButton("Yes", 20, 20) then
+    	        nosound = false
+    		    SetBool("savegame.mod.nosound", nosound, true)
+    		end
+    	else
+    	    if UiTextButton("No", 20, 20) then
+    		    nosound = true
+    		    SetBool("savegame.mod.nosound", nosound, true)
+    		end
+    	end
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("No M.O.A.B shockwave effect")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(1, 1, 1)
+    	if noshock then
+    	    if UiTextButton("Yes", 20, 20) then
+    	        noshock = false
+    		    SetBool("savegame.mod.noshock", noshock, true)
+    		end
+    	else
+    	    if UiTextButton("No", 20, 20) then
+    		    noshock = true
+    		    SetBool("savegame.mod.noshock", noshock, true)
+    		end
+    	end	
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("World buster removes everything")
+    	UiTranslate(0, 40)
+    	UiAlign("center")
+    	UiColor(1, 1, 1)
+    	if bevery then
+    	    if UiTextButton("Yes", 20, 20) then
+    	        bevery = false
+    		    SetBool("savegame.mod.bevery", bevery, true)
+    		end
+    	else
+    	    if UiTextButton("No", 20, 20) then
+    		    bevery = true
+    		    SetBool("savegame.mod.bevery", bevery, true)
+    		end
+    	end	
+end
+

```
