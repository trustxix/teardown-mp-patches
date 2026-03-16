# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,3246 +1,10 @@
---Because it's secretly malware. maybe. maybe not actually. just a joke function for those of you reading my code
+#version 2
 function hacker(Boolean)
 	if ModInstalled == true then
 	HackAndStealPersonalInformationOrWhatever(ThePersonReadingThisRightNow)
 	end
 end
 
-
-
-
-
---btw i swear in my code, just as a warning. if you don't want to read swear words, don't read my code, duh. not my fault.
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-function init()
-	RegisterTool("INFINITY", "Limitless technique", "untitled.vox")
-	SetBool("game.tool.INFINITY.enabled", true)
-	SetInt("game.tool.CLEAVER.ammo", 5000*500) --used to be shrine technique, made a copy and i'm also working on that >:) (it's laggy as fuck tho, even on my end. maybe check it out too? this one's way more optimized tho)
-	Feet = 0
-	cam = 0
-	Frames = 0
-	performance = true --actually the opposite, performance mode is now the worse one for performance, turning off makes it sprites, which is better for performance. press 8 in-game btw
-	BlueTrack = Vec(0,0,0)
-	BlueZone = Vec(0,0,0)
-	RedTrack = Vec(0,0,0)
-	RedTrackD = Vec(0,0,0) --Red track DICK, totally not direction
-	RVel = Vec(0,0,0)
-	BVel = Vec(0,0,0)
-	MVel = Vec(0,0,0) --merge velocity (unused)
-	particleTimer = 0
-	dcirc = {} --DICK circles, not direction at all
-	ctime = {} --COCK time, not circle at all
-	SBlue = false --can't make a dick and balls joke outta this one, sorry folks
-	smbt = {}
-	smbv = {}
-	smbtot = 0
-	ShotBlue = 0
-	ShotBlueTime = 0
-	BluesMerge = false
-	BTarget = 0
-	BTPos = Vec(0,0,0)
-	BROTIME = 0
-	SRed = false
-	PNuke = false --purple, not the nuke
-	NukeTime = 0 --this is the nuke timer, yes this is the nuke
-	NRelease = false --i have no fucking clue what this is
-	MTimer = 200 --red and blue merge timer, don't want it to be instant, lame as hell
-	--punch init
-	Str = 0.1 --strength of the technique and everything --POURPLE
-	BluStr = 0.1 --BLUE strength
-	RedStr = 0.1 --red string cheese
-	NTimer = 0 --NUKE timer
-	InfToggle = false
-	FlyToggle = false
-	--NTimer = 0
-	NMove = false
-	--void statistics (possibly)
-	DomActivate = 0
-	DomainToggle = false
-	DomainPos = 0
-	DPR = 0 --domain place rot
-	DPP = 0 --domain place pos
-	DPD = 0 --drection
-	BHolePos = 0 --Butthole position
-	DsTimer = 0 --Dick suck timer
-	--pvoid = CreateShape(0,0,0)
-	void = 0
-	voidb = 0
-	ovoid = 0
-	ovoidb = 0
-	DomainBreak = false
-	
-	--shade = CreateShape(0,0,0)
-	skybox = GetEnvironmentProperty("skybox")
-	sun = GetEnvironmentProperty("sunBrightness")
-	skybright = GetEnvironmentProperty("skyboxbrightness")
-	tintr,tintg,tintb = GetEnvironmentProperty("skyboxtint")
-	fogr,fogg,fogb = GetEnvironmentProperty("fogColor")
-	fogp1,fogp2,fogp3,fogp4 = GetEnvironmentProperty("fogParams")
-	amb = GetEnvironmentProperty("ambience")
-	rain = GetEnvironmentProperty("rain")
-
-	sat = GetPostProcessingProperty("saturation")
-	cb1,cb2,cb3 = GetPostProcessingProperty("colorbalance")
-	bright = GetPostProcessingProperty("brightness")
-	gamma = GetPostProcessingProperty("gamma")
-	freq = 0
-	--other things needed to work correctly
-	scrollPos = 0
-	Burnout = 0
-	LockToggle = false
-	HP = 1 --HOT PUSSY
-	RTime = 0
-	time = 1
-	pullBodies = QueryAabbBodies(0,0)
-	telek = false
-	SBlueStrScaleThingy = 0
-	tpStr = 0
-	tpvel = 0
-	--DebugPrint("This is the infinity mod creator, Idk how to make a ui so I put everything in DebugPrint")
-	--DebugPrint("Controls are in the Mod description thing, not typing all that out again")
-	--all sounds just already in teardown
-	BlueSound = LoadLoop("tornado.ogg")
-	RedSound = LoadLoop("fire-out-loop.ogg")
-	Water = LoadSound("splash-l1.ogg")
-	pShot = LoadSound("break-l4.ogg")
-	Boom = LoadSound("thunder2.ogg")
-	InfExisting = LoadLoop("float-loop.ogg")
-	Extra = LoadLoop("ambient.ogg")
-	Brown = LoadSound("Brown.ogg")
-	Explode = LoadSound("m0.ogg")
-	suck = LoadSound("suck.ogg")
-	--made some of these images
-	circle = LoadSprite("circle.png")
-	ripple = LoadSprite("ripple.png")
-	ripple2 = LoadSprite("ripple2.png")
-	ripple3 = LoadSprite("ripple3copyright.png")
-	star = LoadSprite("star.png")
-	--not this one
-	earth = LoadSprite("earth.png") --ripped straight from nasa
-
-	EntireAssFuckingCutsceneTypeAnimationTimer = 0 --also known as bich
-	RSplodeTime = 0
-	BSplodeTime = 0
-	pshart = false
-	ReleaseTheBeast = 0 --why did i call it that?
-	BDir = Vec(0,0,0)
-	honoredpos = 0
-	honoredrotata = 0
-	honored = false
-	PRtoggle = false
-	NoMoreRed = false --make sure you don't keep spawning them by holding grab
-	wheelless = false
-	--customizable shit, options
-	if not HasKey("savegame.mod.inf.wheelless") then
-		SetBool("savegame.mod.inf.wheelless", false)
-	else
-		if GetBool("savegame.mod.inf.wheelless") == true then
-			wheelless = true
-		end
-	end
-	if not HasKey("savegame.mod.inf.performancemode") then --remember, performance stat is the one WITH particles, i switched it in ONLY THE OPTIONS THING
-		SetBool("savegame.mod.inf.performancemode", true)
-		performance = true
-	end
-	if GetBool("savegame.mod.inf.performancemode") == false then
-		performance = false
-	end
-	controller = false
-	--keybinds, making sure there are some
-	if not HasKey("savegame.mod.inf.controller") then
-		SetBool("savegame.mod.inf.controller",false)
-	end
-
-	if GetBool("savegame.mod.inf.controller") then  --IF CONTROLLER OPTIONS THING IS GREEN/YES
-		--CONTROLLER KEYBINDS
-		controller = true
-		SetString("savegame.mod.inf.infkey","interact")
-	
-		SetString("savegame.mod.inf.sadd","z")
-
-	
-		SetString("savegame.mod.inf.ssub","x")
-
-	
-		SetString("savegame.mod.inf.time","scroll_down")
-
-	
-		SetString("savegame.mod.inf.warp","zoom")
-
-	
-		SetString("savegame.mod.inf.cutsc","flashlight")
-
-	
-		SetString("savegame.mod.inf.tel","tool_group_prev")
-
-	
-		SetString("savegame.mod.inf.dom","crouch")
-
-	
-		SetString("savegame.mod.inf.ptrack","n")
-
-	
-		SetString("savegame.mod.inf.flykey","jump")
-
-	
-		SetString("savegame.mod.inf.lock","tool_group_next")
-
-	
-		SetString("savegame.mod.inf.grab","scroll_up")
-	else 
-		--NORMAL KEYBOARD KEYBINDS
-		if not HasKey("savegame.mod.inf.infkey") then
-			SetString("savegame.mod.inf.infkey","e")
-		end
-		if not HasKey("savegame.mod.inf.sadd") then
-			SetString("savegame.mod.inf.sadd","z")
-		end
-		if not HasKey("savegame.mod.inf.ssub") then
-			SetString("savegame.mod.inf.ssub","x")
-		end
-		if not HasKey("savegame.mod.inf.time") then
-			SetString("savegame.mod.inf.time","r")
-		end
-		if not HasKey("savegame.mod.inf.warp") then
-			SetString("savegame.mod.inf.warp","t")
-		end
-		if not HasKey("savegame.mod.inf.cutsc") then
-			SetString("savegame.mod.inf.cutsc","v")
-		end
-		if not HasKey("savegame.mod.inf.tel") then
-			SetString("savegame.mod.inf.tel","b")
-		end
-		if not HasKey("savegame.mod.inf.dom") then
-			SetString("savegame.mod.inf.dom","m")
-		end
-		if not HasKey("savegame.mod.inf.ptrack") then
-			SetString("savegame.mod.inf.ptrack","n")
-		end
-		if not HasKey("savegame.mod.inf.flykey") then
-			SetString("savegame.mod.inf.flykey","alt")
-		end
-		if not HasKey("savegame.mod.inf.lock") then
-			SetString("savegame.mod.inf.lock","shift")
-		end
-		if not HasKey("savegame.mod.inf.grab") then
-			SetString("savegame.mod.inf.grab","q")
-		end
-		--reset keybinds after controller switched back to false
-		if GetString("savegame.mod.inf.infkey") == "interact" then
-			SetString("savegame.mod.inf.infkey","e")
-			SetString("savegame.mod.inf.sadd","z")
-			SetString("savegame.mod.inf.ssub","x")
-			SetString("savegame.mod.inf.time","r")
-			SetString("savegame.mod.inf.warp","t")
-			SetString("savegame.mod.inf.cutsc","v")
-			SetString("savegame.mod.inf.tel","b")
-			SetString("savegame.mod.inf.dom","m")
-			SetString("savegame.mod.inf.ptrack","n")
-			SetString("savegame.mod.inf.flykey","alt")
-			SetString("savegame.mod.inf.lock","shift")
-			SetString("savegame.mod.inf.grab","q")
-		end
-	end
-	--GetString("savegame.mod.inf.")
-end
-
-function tick(dt)
---warp screen effect with speed
-	--SetCameraFov((VecLength(pvel))/20+100)
---lock toggle
-	Frames = Frames + 1
-	--DebugPrint(dt*100)
-	--time = RTime
-	RTime = dt*100
-	if Frames == 10000 then
-		Frames = 0 --frames, unlimited frames, but no frames
-	end
-	if LockToggle == true then
-		if controller then
-			SetBool("game.player.caninteract", false)
-			SetBool("game.player.cangrab", false)
-			SetBool("game.player.flashlight.enabled", false)
-			SetBool("game.player.toolselect",false)
-			ReleasePlayerGrab()
-		end
-		if wheelless then
-			scrollPos = 10
-			if SBlue and SRed then
-				scrollPos = (BluStr+RedStr)/4+1
-			else
-				if SBlue then
-					scrollPos = (BluStr)/2+2
-				end
-				if SRed then
-					scrollPos = (RedStr)/2+2
-				end
-			end
-		else
-			scrollPos = scrollPos + InputValue("mousewheel")
-			--if InputDown(1) or scrollPos < 0 then
-			if InputDown("mmb") then
-				--if scrollPos <= 0.1 then
-					scrollPos = 0
-				--end
-			end
-		end
-		if InputPressed(2) then --not sure what to change to
-			Str = 0.1
-		end
-		--Strength scale
-		if InputDown (GetString("savegame.mod.inf.sadd")) then
-			Str = Str + 0.1*RTime
-			if SBlue then
-				BluStr = BluStr + 0.1*RTime
-			end
-			if SRed then
-				RedStr = RedStr + 0.1*RTime
-			end
-			--DebugPrint(Str)
-		end
-
-		if InputDown (GetString("savegame.mod.inf.ssub")) then
-			if Str > 0.1 then
-				Str = Str - 0.1*RTime
-			end
-			if SBlue then
-				BluStr = BluStr - 0.1*RTime
-			end
-			if SRed then
-				RedStr = RedStr - 0.1*RTime
-			end
-			--DebugPrint(Str)
-		end
-		if Str < 0.1 then
-			Str = 0.1
-		end
-		if BluStr < 0.1 then
-			BluStr = 0.1
-		end
-		if RedStr < 0.1 then
-			RedStr = 0.1
-		end
-	end
-	UScrollPos = scrollPos
-
-	--DebugPrint(scrollPos)
-	if Burnout > 0 then
-		Burnout = Burnout - 1
-	end
-	Feet = GetPlayerTransform(true)
-	cam = GetCameraTransform(true)
-	--DebugPrint(PlayerHeight)
-	pvel = GetPlayerVelocity()
-	if GetBool("game.thirdperson") == false then
-		origin = cam.pos
-		dir = TransformToParentVec(cam,Vec(0,0,-1))
-	else
-		origin = VecAdd(Feet.pos, Vec(0,1.7,0))
-		dir = TransformToParentVec(Feet,Vec(0,0,-1))
-	end
-	if tpStr > 1 then
-		--tpStr = tpStr - 1
-		if time == 1 then
-			--SetPlayerVelocity(VecAdd(pvel,VecScale(dir,scrollPos/RTime)))
-			--SetPlayerTransform(Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot),true)
-			SetCameraFov((-tpStr*10)+180)
-		else
-			SetPlayerTransformWithPitch(Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot))
-			SetCameraFov((-tpStr*10)+180)
-			tpStr = tpStr - 1
-		end
-	else
-		if tpStr > 0 then
-			--tpStr = 0
-		end
-	end
-	if tpStr == 1 then
-		SetCameraFov(360)
-		--SetPlayerVelocity(VecScale(dir,VecLength(tpvel)))
-		tpStr = 0
-	end
-	if GetString("game.player.tool") == "INFINITY" then
-		if InputPressed(GetString("savegame.mod.inf.cutsc")) and PNuke == false then
-			if EntireAssFuckingCutsceneTypeAnimationTimer == 0 then 
-				if InputDown(GetString("savegame.mod.inf.time")) then
-					PNuke = false
-					EntireAssFuckingCutsceneTypeAnimationTimer = 160
-					local f1,f2,f3 = GetQuatEuler(Feet.rot)
-					BVel = Vec(0,0,0)
-					RVel = Vec(0,0,0)
-					SetTimeScale(0.1)
-					honoredpos = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
-					--honoredrotata = TransformToParentVec(cam, Vec(1,0,0))
-					honoredrotata = TransformToParentVec(cam, Vec(0,-1,0))
-					honored = true
-					SetBool("game.flashlight.enabled", false)
-				else
-					PNuke = false
-					EntireAssFuckingCutsceneTypeAnimationTimer = 500
-					local f1,f2,f3 = GetQuatEuler(Feet.rot)
-					BVel = Vec(0,0,0)
-					RVel = Vec(0,0,0)
-					SetBool("game.flashlight.enabled", false)
-				end
-			end
-		end
-		if InputPressed(GetString("savegame.mod.inf.ptrack")) then
-			if PRtoggle == true then
-				PRtoggle = false
-			else
-				PRtoggle = true
-			end
-		end
-		if InputPressed("8") then
-			if performance == true then
-				performance = false
-			else
-				performance = true
-			end
-		end
-
-		--warp
-		if InputPressed(GetString("savegame.mod.inf.warp")) then
-			tpStr = 10
-			tpvel = pvel
-		end
-		
-
-		if InputDown(GetString("savegame.mod.inf.time")) then
-			--SetValue("time",0.03,"easeout",0)
-			if pshart == true then
-				if performance == true and (pshart and honored == false) then
-					time = 0.01
-				else
-					time = 0
-				end
-			else
-				time = 0.02
-			end
-			SetTimeScale(time)
-			--DebugPrint(pvel)
-		end
-		if not InputDown(GetString("savegame.mod.inf.time")) then
-			SetValue("time",1)
-			SetTimeScale(time)
-		end
-		if InputPressed(GetString("savegame.mod.inf.lock")) then
-			if LockToggle == true then
-				LockToggle = false
-				--DebugPrint("Lock is off")
-			else
-				LockToggle = true
-				--DebugPrint("Lock is on")
-			end
-		end
-
-		if LockToggle == true then
-			SetBool("game.input.locktool", true)
-		end
-		--infinity stuff
-		if InputPressed(GetString("savegame.mod.inf.infkey")) then
-			if InfToggle == true then
-				InfToggle = false
-			else
-				HP = GetPlayerHealth()
-				InfToggle = true
-			end
-		end
-	end
---REQUIRES LIMITLESS TECHNIQUE EQUIPPED
-	if GetString("game.player.tool") == "INFINITY" then
-		if InputPressed("3") then
-			Str = Str + 50
-		end
-		if InputPressed("9") then
-			SetPlayerTransform(Transform(Vec(0,0,0),QuatEuler(0,0,0)))
-		end
-		--SetToolTransform(Transform(Vec(0.2,-0.1,-0.5),QuatEuler(0,0,0)), 0)
-		if InputPressed(GetString("savegame.mod.inf.tel")) then
-			if telek == true then
-				telek = false
-				BTarget = 0
-				BVel = Vec(0,0,0)
-				if InputDown(GetString("savegame.mod.inf.grab")) and #smbt > 0 then
-					BluesMerge = true
-					--BlueTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,(BluStr+4)/6+0.1))
-					BlueTrack = smbt[1]
-					BVel = smbv[1]
-					table.remove(smbt,1)
-					table.remove(smbv,1)
-					BluStr = 5
-					smbtot = #smbt
-				else
-					SBlue = false
-					BluesMerge = false
-				end
-			else
-				telek = true
-				BluesMerge = false
-				if InputDown(GetString("savegame.mod.inf.grab")) and #smbt > 0 then
-					BluStr = BluStr + #smbt
-				end
-			end
-		end
-		--red
-		if InputPressed("grab") and PNuke == false then
-			if SRed == false and RSplodeTime <= 1 then
-				SRed = true
-				RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
-				RVel = VecScale(pvel,0.018)
-				RedStr = 0.1
-			else
-				if RSplodeTime <= 1 then
-					RSplodeTime = 1.5
-					SRed = false
-					MakeHole(RedTrack,RedStr,RedStr,RedStr)
-				end
-			end
-		end
-
-		if (SRed == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0) and PNuke == false then
-			--if InputDown("usetool") == false then
-			--RSplodeTime = 0
-			if Burnout == 0 then
-				if PNuke == false then
-					if InputDown("grab") then
-						--if VecLength(VecSub(origin,RedTrack)) <= 2 then
-							RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,5/6+0.1))
-							RVel = VecScale(pvel,0.01)
-						--end
-					end
-					if InputReleased("grab") then
-						if PNuke == false and not telek then
-							RVel = VecAdd(VecScale(pvel,0.01),VecScale(dir,scrollPos*0.05))
-						end
-						if telek then
-							RSplodeTime = 1.4
-						end
-					end
-				end
-			end
-		end
-		--blue	
-		if InputPressed("usetool") then
-			if PNuke == false then
-				if SBlue == false then
-					BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
-					BlueTrack = VecAdd(origin,dir)
-				end
-				BVel = VecScale(pvel,0.01)
-			end
-		end	
-		if InputPressed("usetool") and PNuke == false then
-		--and BSplodeTime <= 1
-			if SBlue == false then
-				SBlue = true
-				BlueTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
-				BVel = VecScale(pvel,0.01)
-				BluStr = 0.1
-			else
-				BluStr = 0
-				SBlue = false
-				--end
-			end
-		end
-		
-		if (SBlue == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0) and PNuke == false then
-			if Burnout == 0 then
-				if PNuke == false then
-					if InputDown("usetool") then
-						--if VecLength(VecSub(origin,RedTrack)) <= 2 then
-							BlueTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,(BluStr+4)/6+0.1))
-							BVel = VecScale(pvel,0.01)
-						--end
-					end
-					if InputReleased("usetool") then
-						if PNuke == false then
-							BVel = VecAdd(VecScale(pvel,0.01),VecScale(dir,scrollPos*0.05))
-						end
-					end
-				end
-			end
-		end
-		--infinite void (with rage so sigma i feel so sigma while listening to this song i'm trynna make this noticable so i can come back later thank you byeeeeee)
-		--DebugCross(DomainPos,1,0,0)
-		
-	end
---DOES NOT REQUIRE LIMITLESS TECHNIQUE EQUIPPED
-	--infinite void (with rage so sigma i feel so sigma while listening to this song i'm trynna make this noticable so i can come back later thank you byeeeeee)
-		--DebugCross(DomainPos,1,0,0)
-	if (InputPressed(GetString("savegame.mod.inf.dom")) and GetString("game.player.tool") == "INFINITY") or DomainBreak then
-		if DomainToggle == true then
-			--domain off/break
-			DomainToggle = false
-			--ClearShape(void)
-			Delete(voidb)
-			--DebugPrint(ovoid)
-			--ClearShape(ovoid)
-			Delete(ovoidb)
-			DomainBreak = false
-			for k = 1, 0 do --if wanted change the 0
-				for i = -1,1,0.3 do
-					for j = -1,1,0.3 do
-						local GDir = QuatRotateVec(DPR,VecNormalize(Vec(i,j,0)))
-						--local GDir = Vec(i,j,k)
-						--local hit, dis, gp = QueryRaycast(origin,GDir,10)
-						local what = ((rand(0,100))/10/math.pi)
-						--DebugPrint(math.sin(what))
-						local gspawn = VecAdd(VecAdd(DPP,VecScale(DPD,(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
-						--local gspawn = VecAdd(VecAdd(Feet.pos,VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
-						ParticleType("plain")
-						ParticleTile(3)
-						ParticleColor(1,1,1)
-						ParticleRadius(3)
-						ParticleAlpha(1)
-						ParticleGravity(-1)
-						ParticleDrag(0)
-						ParticleEmissive(1)
-						ParticleRotation(0)
-						ParticleCollide(0)
-						SpawnParticle(gspawn,VecScale(VecNormalize(GDir),10),0.8)
-						--PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
-					end
-				end
-			end
-			SetEnvironmentProperty("skybox", skybox)
-			SetEnvironmentProperty("skyboxbrightness", skybright)
-			SetEnvironmentProperty("skyboxtint",tintr,tintg,tintb)
-			SetEnvironmentProperty("sunBrightness",sun)
-			SetEnvironmentProperty("fogColor",fogr,fogg,fogb)
-			SetEnvironmentProperty("fogParams",fogp1,fogp2,fogp3,fogp4) 
-			SetEnvironmentProperty("ambience",amb)
-			SetEnvironmentProperty("rain",rain)
-
-			SetPostProcessingProperty("saturation", sat)
-			SetPostProcessingProperty("colorbalance",cb1,cb2,cb3)
-			SetPostProcessingProperty("brightness",bright)
-			SetPostProcessingProperty("gamma",gamma)
-			local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-20,-50)),VecAdd(DomainPos,Vec(50,50,50)))
-			for i = 1, #dbodies do
-				local dbody = dbodies[i]
-				if IsBodyDynamic(dbody) then
-					jbodies = GetJointedBodies(dbody)
-					for j = 1,#jbodies do
-						local jbody = jbodies[j]
-						local add = true
-						for k = 1, #dbodies do
-							if jbody == dbodies[k] then
-								add = false
-							end
-						end
-						if add then
-							dbodies[#dbodies+1] = jbody
-						end
-					end
-				end
-			end
-			for i = 1, #dbodies do
-				local dbody = dbodies[i]
-				if IsBodyDynamic(dbody) then
-					dtrans = GetBodyTransform(dbody)
-					--RemoveTag(dbody, "state.id","avoid")
-					SetBodyTransform(dbody,Transform(VecAdd(dtrans.pos,Vec(0,-9999.5,0)),dtrans.rot))
-				end
-			end
-			if VecLength(VecSub(Feet.pos,DomainPos)) < 100 then
-				SetPlayerTransform(Transform(VecAdd(Feet.pos,Vec(0,-9999.5,0)),Feet.rot))
-			end
-			SetPlayerParam("GodMode",false)
-			PlaySound(pShot,DomainPos,1,true,1)
-			PlaySound(pShot,DPP,10,true,0.8)
-		else
-			DomActivate = 100
-			DPP = Feet.pos
-			DPR = Feet.rot
-			DPD = dir
-			--PlaySound()
-		end
-	end
-	if DomActivate == 1 then
-		DomActivate = 0
-		if DomainToggle == false then
-			DomainToggle = true
-		--domain stuff you can walk on/break
-		--inside
-			DomainPos = VecAdd(VecAdd(DPP,Vec(0,10000,0)),Vec(0,0,0)) --change Vec(0,0,0) to offset later
-			local ins = Spawn("inside.xml", Transform(Vec(0,10000,0),QuatEuler(0,0,0)))
-			voidb = ins[1]
-			--DebugPrint(ins)
-			void = ins[2]
-		--outside
-			local out = Spawn("outside.xml", Transform(Vec(0,1000000,0),QuatEuler(0,0,0)))
-			ovoidb = out[1]
-			--DebugPrint(out)
-			ovoid = out[2]
-			
-			local dbodies = QueryAabbBodies(VecAdd(DPP,Vec(-8,-0.5,-8)),VecAdd(DPP,Vec(8,8,8)))
-			for i = 1, #dbodies do
-				local dbody = dbodies[i]
-				if IsBodyDynamic(dbody) then
-					local jbodies = GetJointedBodies(dbody)
-					for j = 1,#jbodies do
-						local jbody = jbodies[j]
-						local add = true
-						for k = 1, #dbodies do
-							if jbody == dbodies[k] then
-								add = false
-							end
-						end
-						if add then
-							dbodies[#dbodies+1] = jbody
-						end
-					end
-				end
-			end
-			for i = 1, #dbodies do
-				local dbody = dbodies[i]
-				if IsBodyDynamic(dbody) then
-					dtrans = GetBodyTransform(dbody)
-					--RemoveTag(dbody, "state.id","avoid")
-					SetBodyTransform(dbody,Transform(VecAdd(dtrans.pos,Vec(0,10000,0)),dtrans.rot))
-				end
-			end
-			SetPlayerTransform(Transform(VecAdd(Feet.pos,Vec(0,10000,0)),Feet.rot))
-			Feet = Transform(VecAdd(Feet.pos,Vec(0,10000,0)),Feet.rot)
-			SetEnvironmentProperty("skybox", nil)
-			SetEnvironmentProperty("skyboxbrightness", 0)
-			SetEnvironmentProperty("skyboxtint", 0,0,0)
-			SetEnvironmentProperty("sunBrightness",0)
-			SetEnvironmentProperty("fogColor",0,0,0)
-			SetEnvironmentProperty("fogParams",0,0,0,0)
-			SetEnvironmentProperty("ambience",nil)
-			SetEnvironmentProperty("rain",0)
-
-			SetPostProcessingProperty("saturation", 1)
-			SetPostProcessingProperty("colorbalance", 1,1,1)
-			SetPostProcessingProperty("brightness",0.8)
-			SetPostProcessingProperty("gamma",1)
-			DsTimer = 1
-			--local gdir = VecNormalize(VecAdd(RVec(),Vec(0,1,0)))
-
-			--local gscale = rand(50,100)
-			--BHolePos = VecAdd(DomainPos,VecScale(gdir,30))
-			BHolePos = VecAdd(DomainPos,Vec(0,10,-120))
-		end
-	end
-	if DomainToggle == true then
-		if GetShapeBody(ovoid) ~= ovoidb then
-			DomainBreak = true
-		end
-		if GetShapeBody(void) ~= voidb then
-			DomainBreak = true
-		end
-		if VecLength(VecSub(Feet.pos,DomainPos)) > 10 and VecLength(VecSub(Feet.pos,DomainPos)) < 100 then --and DsTimer == 0
-			SetPlayerTransform(Transform(DomainPos,Feet.rot),true)
-			SetPlayerVelocity(VecScale(VecNormalize(VecAdd(RVec(),Vec(0,2,0))),20))
-			DomainBreak = true
-		end
-		--DebugPrint(GetShapeBody(ovoid) ~= ovoidb)
-
-		if DsTimer >= 1 then 
-			for i = 1,DsTimer/200*30,1 do
-				for i = 1,DsTimer/200*5,1 do
-					local linepos = VecAdd(DomainPos,VecScale(VecNormalize(Vec(rand(-10,10),rand(-10,10),0)),rand(5,20)))
-					local ldir = Vec(0,0,-1)
-					lr = rand(0.6,1)
-					lg = rand(0.2,0.6)
-					lb = rand(0.6,1)
-
-					DrawLine(linepos,VecAdd(linepos,VecScale(ldir,50)),lr,lg,lb)
-					DrawLine(linepos,VecAdd(linepos,VecScale(VecScale(ldir,50),-1)),lr,lg,lb)
-					for j = 0,50,2 do
-						PointLight(VecAdd(linepos,VecScale(ldir,j)),lr-0.3,lg-0.3,lb-0.3,1)
-					end
-					for j = 0,50,2 do
-						PointLight(VecAdd(linepos,VecScale(ldir,-j)),lr-0.3,lg-0.3,lb-0.3,1)
-					end
-				end
-			end
-			SetCameraFov((VecLength(pvel))/20+100+DsTimer)
-			PlayLoop(BlueSound,DomainPos,1,false,0.2+(DsTimer/50))
-			--PlayLoop(InfExisting,DomainPos,2,false,0.2+(DsTimer/30))
-			--PlayLoop(RedSound,DomainPos,1,false,0.1+(DsTimer/60))
-			PlayLoop(Extra,DomainPos,0.1,false,0.2+(DsTimer/50))
-			if DsTimer == 200 then
-				PlaySound(Boom,DomainPos,2,false,1)
-			end
-		end
-		if DsTimer == 0 then
-			--SetEnvironmentProperty("fogColor",0.1,0.2,0.3)
-			rotarted = QuatLookAt(cam.pos,BHolePos)
-			DrawSprite(Circle,Transform(DomainPos,QuatLookAt(Vec(0,0,0),Vec(0,-1,0))),20,20,1,1,1,0.2,true,true)
-
-			DrawSprite(circle, Transform(BHolePos,rotarted), 30, 30, 0, 0, 0, 1,true,false)
-			DrawSprite(ripple, Transform(BHolePos,rotarted), 32, 32, 1, 1, 1, 1,true,true)
-			for i = 0, 100 do
-				DrawSprite(circle, Transform(BHolePos,QuatLookAt(Vec(0,0,0),VecNormalize(RVec()))), 30, 30, 0, 0, 0, 1,true,false)
-			end
-		end
-		local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-50,-50)),VecAdd(DomainPos,Vec(50,-8,50)))
-		for i = 1, #dbodies do
-			local dbody = dbodies[i]
-			if IsBodyDynamic(dbody) then
-				local jbodies = GetJointedBodies(dbody)
-				for j = 1,#jbodies do
-					local jbody = jbodies[j]
-					local add = true
-					for k = 1, #dbodies do
-						if jbody == dbodies[k] then
-							add = false
-						end
-					end
-					if add then
-						dbodies[#dbodies+1] = jbody
-					end
-				end
-			end
-		end
-		for i = 1, #dbodies do
-			local dbody = dbodies[i]
-			if IsBodyDynamic(dbody) then
-				dtrans = GetBodyTransform(dbody)
-				--RemoveTag(dbody, "state.id","avoid")
-				SetBodyTransform(dbody,Transform(VecAdd(dtrans.pos,Vec(0,-9995,0)),dtrans.rot))
-			end
-		end
-	end
-
---q
-	--quick pull thingy
-	if InputPressed(GetString("savegame.mod.inf.grab")) and GetString("game.player.tool") == "INFINITY" then
-		if (not SRed and not SBlue) and (not PNuke and EntireAssFuckingCutsceneTypeAnimationTimer <= 0) then
-			QueryRequire("dynamic")
-			local hit, dist, _, shape = QueryRaycast(origin,dir,1000)
-			if hit then
-				QueryRequire("dynamic")
-				local HitP = VecAdd(origin,VecScale(dir,dist))
-				local bodies = QueryAabbBodies(VecAdd(HitP,Vec(-2,-2,-2)),VecAdd(HitP,Vec(2,2,2)))
-				for i = 1, #bodies do
-					local body = bodies[i]
-					--local body = GetShapeBody(shape)
-					--DebugPrint(body)
-					--local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
-					local BlueZone = origin
-					local cent = GetBodyCenterOfMass(body)
-					local vel = GetBodyVelocity(body)
-					local worldPoint = TransformToParentPoint(GetBodyTransform(body), cent)
-					local idir = VecNormalize(VecSub(worldPoint,BlueZone))
-					local idist = VecLength(VecSub(worldPoint,BlueZone))
-					local Bigass = VecSub(BlueZone,worldPoint)
-					local min,max = GetBodyBounds(body)
-					local bigness = VecLength(VecSub(max,min))
-					--DebugCross(worldPoint)
-					local setvel = VecAdd(VecScale(vel,0.5),VecScale(VecNormalize(Bigass),50))
-					SetBodyVelocity(body,setvel)
-					for i = 1, 1 do
-						local gspawn = worldPoint
-						ParticleType("plain")
-						ParticleTile(4)
-						ParticleColor(0.7,0.8,1,0,0,1)
-						ParticleRadius(bigness)
-						ParticleAlpha(0.4,0)
-						ParticleGravity(0)
-						ParticleDrag(0)
-						ParticleEmissive(1)
-						ParticleRotation(rand(-10,10))
-						ParticleCollide(0)
-						SpawnParticle(gspawn,setvel,0.2)
-					end
-					table.remove(bodies,i)
-				end
-				PlaySound(suck,VecAdd(origin,dir),1,false,rand(2,3))
-				for i = 1, 1 do
-					local gspawn = VecAdd(origin,VecScale(dir,1))
-					ParticleType("plain")
-					ParticleTile(4)
-					ParticleColor(0.7,0.8,1,0,0,1)
-					ParticleRadius(0,1)
-					ParticleAlpha(0.4,0)
-					ParticleGravity(0)
-					ParticleDrag(0)
-					ParticleEmissive(1)
-					ParticleRotation(rand(-10,10))
-					ParticleCollide(0)
-					SpawnParticle(gspawn,Vec(0,0,0),0.2)
-				end
-				
-			end
-		end
-	end
-	if InputDown(GetString("savegame.mod.inf.grab")) and GetString("game.player.tool") == "INFINITY" then
-		UScrollPos = 0
-		--if InputDown("usetool") == false then
-		--red grab
-		if ((SRed and InputDown("grab") == false) and ((PNuke == false) and SBlue == false)) then
-			BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
-			local RDist = VecSub(RedTrack,BlueZone)
-			RVel = VecSub(VecScale(RVel,0.95),VecScale(RDist,1/((30*(RedStr+1))+1)))
-		end
-		--blue/blues grab
-		if ((SBlue and InputDown("usetool") == false) and ((PNuke == false) and SRed == false)) then
-			local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
-			if not telek then
-				local BDist = VecSub(BlueTrack,BlueZone)
-				BVel = VecSub(VecScale(BVel,0.95),VecScale(BDist,1/((30*(BluStr+5))+1)))
-			end
-		end
-		if (SBlue and telek) then
-			local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
-			local hit, dis,_,shape = QueryRaycast(origin, dir, scrollPos)
-			if hit then
-				BlueZone = VecAdd(origin,VecScale(dir,dis))
-			end
-			for j = 1, #smbt do
-				local BWANT = VecAdd(BlueZone,VecScale(QuatRotateVec(QuatEuler(j*(360/#smbt)+BROTIME,0,90),Vec(0,0,1)),#smbt/2))
-				local BDist = VecSub(smbt[j],BWANT)
-				
-				smbv[j] = VecSub(VecScale(smbv[j],0.95),VecScale(BDist,0.002))
-				if HasTag(BTarget,BluesTracking) then
-					RemoveTag(BTarget,BluesTracking)
-				end
-				BTarget = 0
-			end
-		end
-		--purple grab
-		if (PNuke == true and Str < 3) and VecLength(VecSub(origin,RedTrack)) <= Str/3+2 then
-			RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/6+1))
-			RVel = VecScale(pvel,0.018)
-		end	
-	else
-		if telek then
-			local BlueZone = Vec(0,0,0)
-			if InputReleased(GetString("savegame.mod.inf.grab")) then
-				local hit, dis,_,shape = QueryRaycast(origin, dir, 100)
-				if hit then
-					local p = VecAdd(origin,VecScale(dir,dis))
-					local t = GetShapeWorldTransform(shape)
-					pd = VecSub(p,t.pos)
-					BTarget = shape
-					BTP = TransformToLocalVec(t, pd)
-					SetTag(BTarget,BluesTracking)
-				else
-					BTarget = 0
-					--BTP = VecAdd(origin, VecScale(dir,scrollPos))
-				end
-			end
-			if not HasTag(BTarget,BluesTracking) then
-				BTarget = 0
-			end
-			if #smbt == 0 then
-				BTarget = 0
-				ShotBlue = 0
-				ShotBlueTime = 0
-			end
-			if BTarget ~= 0 then
-				BlueZone = TransformToParentPoint(GetShapeWorldTransform(BTarget),BTP)
-			else
-				if BTarget == -1 then
-					BlueZone = BTP
-				end
-			end
-			if BTarget ~= 0 or BTarget == -1 then
-				if ShotBlueTime <= 0 then
-					ShotBlue = 0
-				end
-				if ShotBlue == 0 then
-					ShotBlue = math.random(1,#smbt)
-					ShotBlueTime = 20
-				end
-				local j = ShotBlue
-				local BDist = VecSub(smbt[j],BlueZone)
-				
-				smbv[j] = VecSub(VecScale(smbv[j],0.99),VecScale(VecNormalize(BDist),0.08))
-				
-				for i=1, #smbv do
-					if i ~= ShotBlue then
-						local BWANT = VecAdd(BlueZone,VecScale(VecNormalize(VecSub(smbt[i],BlueZone)),20))
-						local BDist = VecSub(smbt[i],BWANT)
-						smbv[i] = VecSub(VecScale(smbv[i],0.98),VecScale(BDist,0.001))
-					end
-				end
-				DrawSprite(circle, Transform(BlueZone,cam.rot), 0.2, 0.2, 1, 1, 1, 0.3,false,false)
-			end
-		end
-	end
-
-	--Red existing
-	if (SRed == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0) and PNuke == false then
-		if Burnout == 0 then
-			if PNuke == false then
-				PlayLoop(RedSound,RedTrack,RedStr/10,true,1*((RedStr/10)+1))
-				--PlayLoop(InfExisting,RedTrack,RedStr/10,true,3*((RedStr/10)+1))
-				if telek == false and (InputDown("usetool") == false and SBlue == false) then
-					local point = 0
-					local hit, dist = QueryRaycast(RedTrack,RVel,VecLength(VecScale(RVel,RTime))*1.5)
-					if hit then
-						point = VecAdd(RedTrack,VecScale(VecNormalize(RVel),dist))
-					end
-					if not hit then
-						hit,point = QueryClosestPoint(RedTrack,1/3)
-						dist = VecLength(VecSub(RedTrack,point))
-					end
-					
-					if hit then
-						--RedTrack = VecAdd(RedTrack,VecScale(RVel,dist))
-						Shoot(point,VecNormalize(RVel),"shotgun",RedStr,0.1)
-						RSplodeTime = 1.4
-						SRed = false
-						--Burnout = 100
-						GDrag(VecAdd(RedTrack,VecScale(RVel,dist)),VecScale(RVel,1/0.018),0.01)
-					end
-				end
-			end
-		end
-		if PNuke == false then
-			RedTrack = VecAdd(RedTrack,VecScale(RVel,RTime))
-		end
-			
-		if PNuke == false then
-			if Burnout == 0 then
-				PointLight(RedTrack,0.6,0.1,0.1,RedStr*60)
-				if performance == false then
-					--VisChain(RedTrack,100,0.9,0.8,1,0.5,0,0,Str,Str,true,1,RVec(),cam,false)
-					if EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
-						--DrawSprite(circle, Transform(RedTrack,cam.rot), Str/10, Str/10, 1, 1, 1, 0.6,true,true)
-						--DrawSprite(circle, Transform(RedTrack,cam.rot), Str/5, Str/5, 1, 0, 0, 0.8,true,true)
-						--[[
-						for i = 0, 20, 1 do
-							DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), rand(0,RedStr/5), rand(0,RedStr/5), 1, 1, 1, 1,true,true)
-						end
-						for i = 0, 200, 1 do
-							DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), RedStr/5, RedStr/5, 1, 0, 0, 1,true,true)
-						end
-						]]
-						if SBlue then
-							for i = 1,360 do
-								DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames,0)), RedStr/5, RedStr/5, 1, 0, 0, 1,true,false)
-							end
-							for i = 1,360 do
-								DrawSprite(earth,Transform(RedTrack,QuatEuler(i+Frames,0,0)), RedStr/5, RedStr/5, 1, 0, 0, 1,true,false)
-							end
-						else
-							for i = 1,360 do
-								DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames,0)), 1/5, 1/5, 1, 0, 0, 1,true,false)
-							end
-							for i = 1,360 do
-								DrawSprite(earth,Transform(RedTrack,QuatEuler(i+Frames,0,0)), 1/5, 1/5, 1, 0, 0, 1,true,false)
-							end
-						end
-					end
-				end
-			end
-		end
-	end
-	if PNuke == true then
-		SRed = false
-		RedStr = 0.1
-	end
-	if RSplodeTime > 1 then
-		local Splstr = (RedStr)/RSplodeTime
-		local t = RSplodeTime
-		if RSplodeTime == 1.4 then
-			PlaySound(Explode,RedTrack,RedStr,false,1.5)
-			pvoid = CreateShape(GetWorldBody(),Transform(RedTrack,QuatEuler(0,0,0)),0)
-			ResizeShape(pvoid,-1,-1,-1,1,1,1)
-			SetBrush("sphere",1,"middle.vox")
-			DrawShapeBox(pvoid,0,0,0,2,2,2)
-			for i = 1,1,1 do
-				Shoot(RedTrack,VecNormalize(RVel),"shotgun",Splstr,0.001)
-			end
-			Delete(pvoid)
-		end
-		SRed = false
-		Gravity(RedTrack,-Splstr*10,Splstr*3)
-		PointLight(RedTrack,1,0,0,Splstr*160)
-		if performance == false then
-			for i = 0, 200, 1 do
-				DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2.6, Splstr/2.6, 1, 1, 1, 1,true,true)
-			end
-			for i = 0, 200, 1 do
-				DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2, Splstr/2, 1, 0, 0, 1,true,true)
-			end
-		else
-			for i = 1,800,1 do
-				local gdis = VecScale(VecNormalize(RVec()),Splstr/10)
-				local gspawn = VecAdd(RedTrack,gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(1,1,1,1,0,0)
-				ParticleRadius(Splstr/80)
-				ParticleAlpha(1,0)
-				ParticleGravity(0)
-				ParticleDrag(0.2)
-				ParticleEmissive(1)
-				ParticleRotation(rand(-10,10))
-				ParticleCollide(0)
-				local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-				local spidir = TransformToParentVec(look, Vec(0,0,rand(-Splstr,Splstr)))
-				SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,0),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-Splstr/0.5)),1)
-			end
-			if RSplodeTime < 1.5 then
-				for i = 1,0,1 do
-					local gdis = VecScale(VecNormalize(RVec()),Splstr/1.5)
-					local gspawn = VecAdd(RedTrack,gdis)
-					ParticleType("plain")
-					ParticleTile(5)
-					ParticleColor(1,1,1,1,0,0)
-					ParticleRadius(Splstr/50)
-					ParticleAlpha(1,0)
-					ParticleGravity(0)
-					ParticleDrag(0)
-					ParticleEmissive(1)
-					ParticleRotation(rand(-10,10))
-					ParticleCollide(0)
-					local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-					local spidir = TransformToParentVec(look, Vec(-1,0,0))
-					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-SplStr/3)),1)
-				end
-			end
-		end
-		--DebugPrint(RSplodeTime)
-		RSplodeTime = RSplodeTime-0.1
-		if RSplodeTime <= 1 then
-			--DebugPrint("splode")
-			RedTrack = origin
-			RVel = Vec(0,0,0)
-			SRed = false
-			RedStr = 0.1
-		end
-	end
-	--Blue existing
-	if SBlue == true then
-		--SBlueStrScaleThingy
-		BlueTrack = VecAdd(BlueTrack,VecScale(BVel,RTime))
-		if telek or BluesMerge then
-			if telek then
-				if InputPressed(GetString("savegame.mod.inf.tel")) then
-					for i = 0, BluStr, 1 do
-						smbt[i] = VecAdd(BlueTrack,VecScale(VecNormalize(RVec()),rand(0,BluStr/7)))
-						smbv[i] = VecAdd(BVel,VecScale(RVec(),0.1))
-					end
-				end
-				if #smbt < BluStr - 1 then
-					new = #smbt + 1
-					smbt[new] = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,(5)/6+0.1))
-					smbv[new] = VecAdd(VecScale(pvel,0.01),VecScale(VecNormalize(VecAdd(dir,VecScale(RVec(),0.2))),scrollPos*0.05))
-				end
-				if #smbt > BluStr + 1 then
-					for j = #smbt-2, #smbt, 1 do
-						table.remove(smbt,j)
-						table.remove(smbv,j)
-					end
-				end
-			end
-		--blues merging
-			if BluesMerge then
-				for i=1, #smbv do
-					local BWANT = BlueTrack
-					local BDist = VecSub(smbt[i],BWANT)
-					if BluStr < 80 then
-						smbv[i] = VecAdd(VecScale(smbv[i],0.99),VecScale(VecNormalize(BDist),-0.0006*BluStr))
-					else
-						smbv[i] = VecAdd(VecScale(smbv[i],0.99),VecScale(VecNormalize(BDist),-0.0006*80))
-					end
-					if VecLength(BDist) < 1.5 then
-						BluStr = BluStr + 1
-						table.remove(smbt,i)
-						table.remove(smbv,i)
-					end
-					--BVel = VecAdd(VecScale(BVel,1),VecScale(VecNormalize(BDist),0.001/BluStr))
-				end
-				if #smbt == 0 then
-					BluesMerge = false
-					smbtot = 0
-				end
-			end
-		--blues exist
-			for j = 1, #smbt do
-				smbt[j] = VecAdd(smbt[j],VecScale(smbv[j],RTime))
-				PlayLoop(BlueSound,smbt[j],5/20,true, 2.5)
-				PointLight(smbt[j],0.1,0.2,1,200)
-				if performance == false then
-					--for i = 1, 20, 1 do
-					--	DrawSprite(circle, Transform(smbt[j],QuatLookAt(Vec(0,0,0),RVec())), 1, 1, 0.2, 0.4, 1, 0.2,false,false)
-					--end
-					DrawSprite(earth, Transform(smbt[j],cam.rot), 1, 1, 0.2, 0.4, 1, 1,true,false)
-					--for i = 1, 20, 1 do
-					--	local r = rand(-0.5,0.5)
-					--	DrawSprite(ripple, Transform(VecAdd(smbt[j],Vec(0,r,0)),QuatEuler(90,0,0)), math.sin(2*r*math.pi), math.sin(2*r*math.pi), 1, 1, 1, 1,true,true)
-					--end
-				end
-			end
-			
-		end
-	--Normal blue
-		if not telek then
-			if BluStr < 80 then
-				PlayLoop(BlueSound,BlueTrack,BluStr/20,true, 6/((BluStr/10)+1))
-				PointLight(BlueTrack,0.1,0.2,1,BluStr*100)
-				if performance == false then
-					--for i = 1, 20, 1 do
-					--	DrawSprite(circle, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), BluStr/5, BluStr/5, 0.2, 0.4, 1, 0.2,false,false)
-					--end
-					for i = 1,360 do
-						DrawSprite(earth,Transform(BlueTrack,QuatEuler(0,i+Frames,0)), BluStr/5, BluStr/5, 0, 0.4, 1, 1,true,false)
-					end
-					for i = 1,360 do
-						DrawSprite(earth,Transform(BlueTrack,QuatEuler(i+Frames,0,0)), BluStr/5, BluStr/5, 0, 0.4, 1, 1,true,false)
-					end
-					--for i = 1, 20, 1 do
-					--	DrawSprite(ripple, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), rand(0,BluStr/5), rand(0,BluStr/5), 1, 1, 1, 1,true,true)
-					--end
-				end
-			else
-				DrawSprite(star, Transform(BlueTrack,cam.rot), 0.8,0.5, 0.3, rand(0.3,0.6), 1, 1,true,true)
-				for i = 1, 50, 1 do
-					DrawSprite(circle, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), 0.2, 0.2, 0, 0, 0, 1,true,false)
-				end
-			end
-		--Gravity(BlueTrack,Str,Str,_)
-			--nuke detection
-			if InputReleased("grab") then
-				NTimer = 100
-			end
-			--purple merge
-			if (SRed and InputDown("grab") == false) and GetString("game.player.tool") == "INFINITY" then
-				local Rdist = VecLength(VecSub(RedTrack,BlueTrack))
-				local Rdir = VecNormalize(VecSub(RedTrack,BlueTrack))
-				NTimer = NTimer - 1
-				if BluStr > RedStr then
-					Str = BluStr
-				else
-					Str = RedStr
-				end
-				if InputPressed("q") then
-					MTimer = 200
-				end
-				if InputDown(GetString("savegame.mod.inf.grab")) then
-					local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
-					local protata = TransformToParentVec(Feet, Vec(-1,0,0))
-					--if BluStr > RedStr * 1.5 then
-						local rZone = VecAdd(BlueZone,VecScale(protata,-(2*Str*MTimer/80)/(20)))
-						local RDist = VecSub(RedTrack,rZone)
-						RVel = VecSub(VecScale(RVel,0.3),VecScale(RDist,1/((10*(RedStr+1))+1)))
-				
-						local bZone = VecAdd(BlueZone,VecScale(protata,(2*Str*MTimer/80)/(20)))
-						local BDist = VecSub(BlueTrack,bZone)
-						BVel = VecSub(VecScale(BVel,0.3),VecScale(BDist,1/((10*(BluStr+1))+1)))
-
-					if MTimer > 0 then
-						--MTimer = MTimer - 1
-					end
-					if BluStr < RedStr then
-						BluStr = (RedStr-BluStr)/10+BluStr
-					end
-					if RedStr < BluStr then
-						RedStr = (BluStr-RedStr)/10+RedStr
-					end
-				else
-					RVel = VecSub(VecScale(RVel,0.99),VecScale(VecScale(Rdir,0.1*(1/(Rdist+5))),BluStr*0.018*RTime))
-					BVel = VecSub(VecScale(BVel,0.99),VecScale(VecScale(VecScale(Rdir,-1),0.1*(1/(Rdist+5))),RedStr*0.018*RTime))
-				end
-
-				if rand(0,10) > 8 and VecLength(VecSub(RedTrack,BlueTrack)) < Str*3 then
-					for i = 1, 2 do
-						s = VecAdd(RedTrack,VecScale(RVec(),rand(-RedStr/8,RedStr/8)))
-						local e = VecAdd(BlueTrack,VecScale(RVec(),rand(-BluStr/12,BluStr/12)))
-						--local s = RedTrack
-						--local e = BlueTrack
-						local last = s
-						for i=1, 10 do
-							local tt = i/10
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-					end
-					for i = 1, 2 do
-						s = VecAdd(BlueTrack,VecScale(RVec(),rand(-BluStr/8,BluStr/8)))
-						local e = VecAdd(RedTrack,VecScale(RVec(),rand(-RedStr/12,RedStr/12)))
-						local last = s
-						for i=1, 10 do
-							local tt = i/10
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-					end
-				end
-				if VecLength(VecSub(RedTrack,BlueTrack)) < Str/5 then
-					
-					--DrawLine(VecAdd(RedTrack,RVec()),VecSub(RedTrack,Rdir),1,1,1)
-					--DrawLine(VecAdd(BlueTrack,RVec()),VecSub(BlueTrack,VecScale(Rdir,-1)),1,1,1)
-					--VisChain()
-					--VisChain(RedTrack,Rdist/Str,1,1,1,0,0,0,true,Str,Rdir,0,true)
-					local c1, c2, c3 = GetQuatEuler(QuatLookAt(RedTrack,BlueTrack))
-					--DebugPrint(Vec(c1,c2,c3))
-					RVel = VecSub(VecScale(RVel,0),VecScale(VecScale(Rdir,0.2*(1/(6))),Str*0.05*RTime))
-					BVel = VecSub(VecScale(BVel,0),VecScale(VecScale(VecScale(Rdir,-1),0.2*(1/(6))),Str*0.05*RTime))
-					local middle = VecAdd(VecSub())
-					
-					if performance == false then
-						--if math.floor(GetTime()*10) % 4 == 1 then
-						--	VisChain(VecAdd(RedTrack,VecScale(RVec(),Str/10)),0.2/(Rdist+1),0.9,0.8,1,1,0.4,0.4,1,1,true,0.1,VecScale(Rdir,-1),cam,false)
-						--	VisChain(VecAdd(BlueTrack,VecScale(RVec(),Str/10)),0.2/(Rdist+1),0.9,0.8,1,0.4,0.8,1,1,1,true,0.1,VecScale(Rdir,1),cam,false)
-						--end
-					end
-					BLight = VecAdd(VecScale(VecSub(BlueTrack,RedTrack),0.5),RedTrack)
-					RLight = VecAdd(VecScale(VecSub(RedTrack,BlueTrack),0.5),BlueTrack)
-					local h1,h2,h3 = GetQuatEuler(cam.rot)
-					if performance == false then
-						for i = 0, 10 do
-							DrawSprite(ripple3,Transform(BLight,QuatEuler(0,h2,-Frames*5+55+i*2)), Str/5, Str/5, 1, 0, 0, 1,true,false)
-							DrawSprite(ripple3,Transform(BLight,QuatEuler(0,h2,-Frames*5+i*2)), Str/5, Str/5, 0, 0, 1, 1,true,false)
-						end
-					end
-					PointLight(BLight,0.1,0.2,1,Str*100/(Rdist+1))
-					PointLight(RLight,0.6,0.1,0.1,Str*80/(Rdist+1))
-					for i = 1, 2 do
-						s = VecAdd(BlueTrack,VecScale(RVec(),rand(-Str/8,Str/8)))
-						local e = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/12,Str/12)))
-						local last = s
-						for i=1, 10 do
-							local tt = i/10
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-						s = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/8,Str/8)))
-						local e = VecAdd(BlueTrack,VecScale(RVec(),rand(-Str/12,Str/12)))
-						local last = s
-						for i=1, 10 do
-							local tt = i/10
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-					end
-					--PointLight()
-				end
-				if NTimer <= 0 then
-					if VecLength(VecSub(RedTrack,BlueTrack)) < ((RedStr+BluStr)/2)/27 then
-						PNuke = true
-						NRelease = true
-						--RVel = VecAdd(BVel,RVel)
-						RVel = Vec(0,0,0)
-						RedTrack = BLight
-						for i = 0, 2000, 1 do
-							dcirc[#dcirc+1] = QuatEuler(rand(-180,180),rand(-180,180),rand(-180,180))
-							ctime[#ctime+1] = rand(-170,200)
-						end
-					end
-				end
-			end
-		end
-	end
-	if (not SBlue or (not telek and not BluesMerge)) and #smbt > 0 then
-		for j = 1, #smbt, 1 do
-			table.remove(smbt,j)
-			table.remove(smbv,j)
-		end
-	end
-	--[[
-	if BSplodeTime > 1 then
-		SBlue = false
-		local Splstr = (BluStr)/BSplodeTime
-		local t = BSplodeTime
-		--MakeHole(BlueTrack,Splstr/3,Splstr/3,Splstr/3)
-		--Shoot(BlueTrackD,VecNormalize(BVel),"shotgun",Splstr/2,0.1)
-		Gravity(BlueTrack,Splstr*50,Splstr*3)
-		PointLight(BlueTrack,0.1,0.2,0.6,Splstr*120)
-		if performance == false then
-			for i = 0, 200, 1 do
-				DrawSprite(circle, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2.6, Splstr/2.6, 1, 1, 1, 1,true,true)
-			end
-			for i = 0, 200, 1 do
-				DrawSprite(ripple, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2, Splstr/2, 0, 0, 1, 1,true,true)
-			end
-		else
-			for i = 1,800,1 do
-				local gdis = VecScale(VecNormalize(RVec()),Splstr*3)
-				local gspawn = VecAdd(BlueTrack,gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(1,1,1,0,0.2,1)
-				ParticleRadius(VecLength(gdis)/80)
-				ParticleAlpha(0,1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(1)
-				ParticleRotation(rand(-10,10))
-				ParticleCollide(0)
-				SpawnParticle(gspawn,VecScale(gdis,-5),0.2)
-			end
-		end
-		BSplodeTime = BSplodeTime-0.1
-		if BSplodeTime <= 1 then
-			--DebugPrint("nomosplode")
-			BlueTrack = origin
-			BVel = Vec(0,0,0)
-			SBlue = false
-			BluStr = 0.1
-		end
-	end
-	]]
---Purple
-	if PNuke == true then
-		SBlue = false
-		Burnout = 5
-		SetToolTransform(Transform(Vec(-0.025,-0.3,-0.6),QuatEuler(0,0,0)), 0)
-		
-		if PRtoggle == true then
-			local campos = VecAdd(RedTrack,VecScale(dir,-Str*1))
-			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,RedTrack))
-			local ccam = Transform(VecAdd(campos,Vec(0,0,0)),Feet.rot)
-			SetCameraTransform(ccam)
-		end
-		if NukeTime == 0 then
-			--DebugPrint((VecLength(RVel)/time))
-			
-			--damage
-			if Str<1 then
-				for i = -1, VecLength(VecScale(RVel,RTime)),0.02 do
-					RedTrackD = VecAdd(RedTrack,VecScale(RVel,i))
-					Destroy(RedTrackD,0.5*0.3,false,0,0,0.5*0.1)
-				end
-			else
-				for i = -1, VecLength(VecScale(RVel,RTime)),0.03*(Str)+0.02 do
-					RedTrackD = VecAdd(RedTrack,VecScale(RVel,i))
-					Destroy(RedTrackD,Str*0.2,false,0,0,Str*0.1)
-				end
-			end
-			PointLight(RedTrackD,0.4,0.1,0.8,Str*100)
-			--RedTrack = RedTrackD
-
-			
-
-			--DebugPrint(GetWindVelocity(RedTrack))
-			if Str > 2 then
-				--Gravity(RedTrack,Str*10*RTime,Str*0.3,nil)
-			end
-			local h1,h2,h3 = GetQuatEuler(cam.rot)
-			--VisChain(RedTrack,Str/9,1,1,1,1,1,1,true,Str,RVec(),cam,true)
-			PlayLoop(InfExisting,RedTrack,Str/20,true, 1/((Str/10)+1))
-
-			--visuals
-			if performance == false or time < 1 then
-				rotarted = QuatLookAt(Vec(0,0,0),TransformToParentVec(cam, Vec(0,0,-1)))
-				-- for safe keeping: QuatEuler(rand(-180,180),0,rand(-180,180))
-				--[[
-				for i = 1, 500, 1 do
-					--DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), Str/5, Str/5, 0.6, 0.2, 1, 1,true,true)
-					local gyat = rand(Str/4,Str/3)
-					DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), gyat, gyat, 0.2, 0, 1.0, 1,true,true)
-					DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), gyat, gyat, 0.1, 0, 1, 1,true,true)
-					--DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),VecNormalize(RVec()))), Str/5, Str/5, 0, 0, 1, 1,true,true)
-					--DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),VecNormalize(RVec()))), Str/5, Str/5, 0.6, 0, 1, 1,true,true)
-				end
-				]]
-					for i = 1,360 do
-						DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames,0)), Str/3.1, Str/3.1, 0.4, 0.2, 0.6, 1,true,true)
-					end
-					for i = 1,360 do
-						DrawSprite(earth,Transform(RedTrack,QuatEuler(i+Frames,0,0)), Str/3.1, Str/3.1, 0.4, 0.2, 0.6, 1,true,true)
-					end
-					for i = 1,360 do
-						DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames*5,0)), Str/3, Str/3, 0, 0, 0.6, 1,true,true)
-					end
-				--if #dcirc < 1000 then
-				--	for i = 1, 3, 1 do
-				--		dcirc[#dcirc+1] = QuatEuler(rand(-180,180),rand(-180,180),rand(-180,180))
-				--		ctime[#ctime+1] = 200
-				--	end
-				--end
-				for i = 1, #dcirc, 1 do
-					ctime[i] = ctime[i] - 0.5*RTime
-					c = ctime[i]
-					cspace = VecScale(QuatRotateVec(dcirc[i],Vec(math.cos(160/(c/10))*(c/120),0,math.sin(160/(c/10))*(c/120))),Str/11)
-					DrawSprite(circle, Transform(VecAdd(RedTrack,cspace),rotarted), (Str*0.01),(Str*0.01), 1, 1, 1, 1,true,true)
-					if ctime[i]<=-160 then
-						ctime[i] = 200
-					end
-				end
-				--VisChain(RedTrack,100,0.9,0.8,1,0.2,0,0.7,Str*1.5,Str*1.5,true,1,RVec(),cam,false)
-			end
-			if honored == true and NMove == false then
-				Str = 0.1
-				if GetString("game.player.tool") == "INFINITY" then
-					if InputDown(GetString("savegame.mod.inf.sadd")) then
-						StStr = StStr + 0.4
-						--DebugPrint(StStr)
-					end
-					if InputDown(GetString("savegame.mod.inf.ssub")) then
-						StStr = StStr - 0.2
-						--DebugPrint(StStr)
-					end
-				end
-				if StStr < 0 then
-					StStr = 0
-				end
-				DrawSprite(star, Transform(RedTrackD,cam.rot), rand(Str/1.2,Str/0.8), rand(Str/1.2,Str/0.8), 1, 0.5, 1, 1,true,true)
-				--lightning to nearby shapes
-				local bzzt = QueryAabbShapes(VecAdd(RedTrack,Vec(-5,-5,-5)),VecAdd(RedTrack,Vec(5,5,5)))
-				for i=1,#bzzt do
-					if rand(0,10) > 9.8 then
-						local hit, e = GetShapeClosestPoint(bzzt[i],RedTrack)
-						--e = GetShapeWorldTransform(bzzt[i]).pos
-						s = RedTrack
-						--Draw laser line in ten segments with random offset, stolen from teardown lazer gun built-in-mod cause I didn't know how to use veclerp
-						local last = s
-						for i=1, 10 do
-							local tt = i/10
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-					end
-				end
-				--lightning in the air
-				if rand(0,10) > 9 then
-					for j = 1, StStr do
-						s = VecAdd(origin,VecScale(RVec(),rand(-5,5)))
-						local e = VecAdd(RedTrack,VecScale(RVec(),rand(-5,5)))
-						local last = s
-						for i=1, 4 do
-							local tt = i/4
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.5*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-					end
-				end
-
-			end
-			if (pshart == true and DomainToggle == false) then
-				if NMove == false then
-					SetPostProcessingProperty("brightness",1.2)
-					SetPostProcessingProperty("saturation",0.8)
-					SetEnvironmentProperty("fogColor",0,0,0)
-					--SetEnvironmentProperty("fogParams",20,120,0.9,2)
-					SetEnvironmentProperty("skyboxbrightness", bright-0.8)
-					--SetEnvironmentProperty("skyboxtint",tintr-0.95,tintg-0.95,tintb-0.95)
-					SetEnvironmentProperty("sunBrightness",0)
-				end
-				if GetString("game.player.tool") == "INFINITY" then
-					if (InputReleased("grab") or InputReleased("usetool")) or (((InputReleased(GetString("savegame.mod.inf.time")) or (NMove and InputDown(GetString("savegame.mod.inf.time")) == false)) and honored == true) or (pshart and honored == false)) then
-						SetPostProcessingProperty("brightness",bright)
-						SetPostProcessingProperty("saturation",sat)
-						SetEnvironmentProperty("fogColor",fogr,fogg,fogb)
-						--SetEnvironmentProperty("fogParams",fogp1,fogp2,fogp3,fogp4)
-						SetEnvironmentProperty("skyboxbrightness", skybright)
-						--SetEnvironmentProperty("skyboxtint",tintr,tintg,tintb)
-						SetEnvironmentProperty("sunBrightness",sun)
-					end
-					if (InputReleased("grab") or InputReleased("usetool")) or (InputReleased(GetString("savegame.mod.inf.time")) and honored == true) then
-						pshart = false
-						PNuke = false
-						if (honored == true and InputReleased(GetString("savegame.mod.inf.time"))) and NMove == false then
-							PlaySound(pShot,RedTrack,1,false,10)
-							for i = -0.1, 100,0.05 do
-								RedTrackD = VecAdd(RedTrack,VecScale(dir,i))
-								if StStr > 0.5 then
-									Destroy(RedTrackD,StStr*0.1,false,0,0,StStr*0.15)
-								else
-									Destroy(RedTrackD,StStr*0.1,false,0,0,0.5*0.15)
-								end
-								if performance == true then
-									for i = 1,2,1 do
-										local gdis = VecScale(VecNormalize(RVec()),StStr/6)
-										local gspawn = VecAdd(RedTrackD,gdis)
-										ParticleType("plain")
-										ParticleTile(2)
-										ParticleColor(1,0.8,1,1,0,1)
-										ParticleRadius(StStr/70)
-										ParticleAlpha(1,0)
-										ParticleGravity(0)
-										ParticleDrag(0.5)
-										ParticleEmissive(5)
-										ParticleRotation(rand(-10,10))
-										ParticleCollide(0)
-										local look = Transform(RedTrackD,QuatLookAt(RedTrackD,gspawn))
-										local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
-										SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(dir,4),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-StStr/3)),0.5)
-									end
-								end
-							end
-							PointLight(RedTrack,0.6,0.2,1,StStr*1000)
-							PointLight(RedTrack,0.6,0.2,1,StStr*1000)
-						end
-						honored = false
-						NMove = false
-					end
-				end
-			end
-			--funky ass movement options
-			if GetString("game.player.tool") == "INFINITY" then
-				if InputDown(GetString("savegame.mod.inf.grab")) then
-					RVel = Vec(0,0,0)
-				end
-				if InputReleased(GetString("savegame.mod.inf.grab")) then
-					--RVel = VecScale(dir,(scrollPos/3)/Str)
-					if Str < 1 then
-						--Str = 1
-					end
-					RVel = VecScale(dir,0.5+(15/(Str*1)))
-					NRelease = false
-					PointLight(RedTrackD,0.8,0.4,1,Str*2000)
-					PointLight(RedTrackD,0.8,0.4,1,Str*2000)
-					DrawSprite(star, Transform(RedTrackD,cam.rot), rand(Str/1.2,Str/0.8), rand(Str/1.2,Str/0.8), 1, 1, 1, 1,true,true)
-					if pshart and honored then
-						NMove = true
-						--Str = StStr
-						--StStr = 0
-						RVel = VecScale(dir,8)
-					end
-					PlaySound(pShot,RedTrack,1,false,6)
-					PlaySound(Water,RedTrack,5,false,6)
-				end
-				if pshart and NMove then
-					--PointLight(RedTrackD,0.1,0.2,1,Str*2000)
-					--PointLight(RedTrackD,1,0.2,0.2,Str*2000)
-					PointLight(RedTrackD,0.6,0.2,1,Str*500)
-					PointLight(RedTrackD,0.6,0.2,1,Str*500)
-					if honored then
-					
-							if VecLength(VecSub(RedTrack,origin)) > ((StStr-Str)/2+Str)/5 then
-								Str = (StStr-Str)/4+Str
-							end
-							if Str > StStr - 0.1 then
-								Str = StStr
-							end
-						--DebugPrint(Str)
-					end
-				end
-				if (InputReleased("grab") or InputReleased("usetool")) then
-					if NRelease == true then
-						NukeTime = 1
-						Burnout = 20
-						PlaySound(Explode,RedTrack,Str,false,1)
-						PlaySound(Water,RedTrack,Str,false,2)
-					else
-						PNuke = false
-						Burnout = 20
-						RedTrack = origin
-					end
-					for i = 1, #dcirc, 1 do
-						dcirc[i] = nil
-						ctime[i] = nil
-					end
-				end
-			end
-			--velocity movement
-			if VecLength(RVel)/RTime > 5 then	
-			if pshart == false then
-				RVel = VecScale(VecNormalize(RVel),(5))
-			end
-			--DebugPrint((VecLength(RVel)))
-			end
-			if honored == false or InputDown(GetString("savegame.mod.inf.time")) == false then
-				RedTrack = VecAdd(RedTrack,VecScale(RVel,RTime))
-			else
-				RedTrack = VecAdd(RedTrack,VecScale(RVel,0.025))
-			end
-		end
-		
---NukeSplosion all over the place
-		if NukeTime > 0 then
-			NukeS = (Str/3)/NukeTime
-			--/NukeTime
-			PointLight(RedTrack,0.1,0.2,1,NukeS*200)
-			PointLight(RedTrack,1,0.1,0.1,NukeS*150)
-			if performance == false or time<1 then
-				local l1,l2,l3 = GetQuatEuler(cam.rot)
-				DrawSprite(circle, Transform(RedTrack,QuatEuler(l1,l2,l3)), NukeS, NukeS, 1, 0.6, 1, 1,true,true)
-				DrawSprite(circle, Transform(RedTrack,QuatEuler(l1,l2,l3)), NukeS/1.2, NukeS/1.2, 1, 1, 1, 1,true, true)
-				for i = 0, 200, 1 do
-					DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), NukeS, NukeS, 0.2, 0, 1.0, 0.65,true,true)
-					DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), NukeS, NukeS, 0, 0, 1, 1,true,true)
-					DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), NukeS/2, NukeS/2, 1, 1, 1, 1,true,true)
-				end
-				QuatLookAt(Vec(0,0,0),RVec())
-			end
-			--RVel = Vec(0,0,0)
-				
-			for i = 1, 10 do
-				s = VecAdd(RedTrack,VecScale(RVec(),rand(-NukeS/6,NukeS/6)))
-				local e = VecAdd(RedTrack,VecScale(RVec(),rand(Str/2,NukeS*2)))
-				local last = s
-				for i=1, 10 do
-					local tt = i/10
-					local p = VecLerp(s, e, tt)
-					p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
-					DrawLine(last, p, 1, 1, 1)
-					last = p
-				end
-			end
-			--local PPlayerD = VecLength(VecSub(RedTrack,origin))
-			--if VecLength(VecSub(RedTrack,origin)) < NukeS then
-				--DebugPrint(GetPlayerHealth()-(NukeS/PPlayerD)/10)
-				--SetPlayerHealth(((GetPlayerHealth()-(NukeS/PPlayerD)/100))*time)
-			--end
-		end
-	end
-	if GetString("game.player.tool") == "INFINITY" then
-		if InputPressed(GetString("savegame.mod.inf.flykey")) then
-			if FlyToggle then
-				FlyToggle = false
-			else
-				FlyToggle = true
-			end
-		end
-	end
-	if time < 1 then
-		if InfToggle == true then
-			if GetPlayerHealth() > HP then
-				HP = GetPlayerHealth()
-			end
-			SetPlayerHealth(HP)
-			SetPlayerParam("GodMode",true)
-		else
-			SetPlayerParam("GodMode",false)
-		end
-		if GetString("game.player.tool") == "INFINITY" then
-			--if InputDown(GetString("savegame.mod.inf.flykey")) then
-			if FlyToggle then
-				PlayerGravity(origin,pvel,BlueTrack,Str,dir,scrollPos)
-			end
-		end
-	end
-	if GetString("game.player.tool") == "INFINITY" then
-		if InputReleased(GetString("savegame.mod.inf.time")) and (pshart == true and honored == true) then
-			pshart = false
-			PNuke = false
-			honored = false
-		end
-	end
---WHOLE ASS FUCKING CUTSCENE BIIIITCH
-	if EntireAssFuckingCutsceneTypeAnimationTimer > 0 and honored == true then
-		if performance == true then
-			EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1*RTime/0.01
-		else
-			EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1
-		end
-		bich = EntireAssFuckingCutsceneTypeAnimationTimer
-		Str = 2
-		SetString("game.player.tool","INFINITY")
-		SBlue = false
-		--local middle = honoredpos
-		local middle = Vec(0,1000,0)
-
-		SetTimeScale(0.01)
-		time = 0.01
-		--middle = Vec(0,10000,0)
-		BVel = Vec(0,0,0)
-		RVel = Vec(0,0,0)
-		ubich = bich
-		--adderall = Vec(math.cos(60/(ubich/10))*(bich/120),0,math.sin(60/(ubich/10))*(bich/120))
-		adderall = VecScale(honoredrotata,math.sin((bich-100)/33)/1.5)
-		BlueTrack = VecAdd(middle,VecScale(adderall,-1))
-		RedTrack = VecAdd(middle,adderall)
-		rotata = VecNormalize(VecSub(RedTrack,BlueTrack))
-		--cadir = TransformToParentVec(cam.rot, Vec(1,0,0))
-		local campos = VecAdd(middle,VecScale(dir,-1))
-		local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,middle))
-		local ccam = Transform(VecAdd(campos,Vec(0,0.2,0)),Feet.rot)
-		SetCameraTransform(ccam)
-			SetPostProcessingProperty("brightness",1.2)
-			SetPostProcessingProperty("saturation",1)
-			SetEnvironmentProperty("fogColor",0,0,0)
-			--SetEnvironmentProperty("fogParams",20,120,0.9,2)
-			SetEnvironmentProperty("skyboxbrightness", bright-0.8)
-			--SetEnvironmentProperty("skyboxtint",tintr-0.95,tintg-0.95,tintb-0.95)
-			SetEnvironmentProperty("sunBrightness",0)
-		if bich < 92 and bich > 90 then
-			PlaySound(Water,middle,100,false,20)
-		end
-
-		if bich < 100 then
-			for i = 0, 1, 0.005 do
-
-				DrawSprite(ripple, Transform(middle,QuatLookAt(Vec(0,0,rand(-0.01,0.01)),honoredrotata)), (bich-100)*(i), (bich-100)*(i), 0.6, 0.2, 0.2, 0.1,true,true)
-				DrawSprite(ripple, Transform(middle,QuatLookAt(Vec(0,0,rand(-0.01,0.01)),honoredrotata)), (bich-100)*(i+0.0025), (bich-100)*(i+0.0025), 0.0, 0.0, 1.0, 0.1,true,true)
-			end
-		end
-		
-		--DebugPrint(bich)
-		for i = 10, 100, 1 do
-			if bich > 100 then
-				DrawSprite(ripple, Transform(VecAdd(middle,adderall),QuatLookAt(Vec(0,0,0),RVec())), 0.2, 0.2, 1, 0, 0, 1,true,true)
-				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1)),QuatLookAt(Vec(0,0,0),RVec())), 0.2, 0.2, 0, 0, 1, 1,true,true)
-			else
-				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,1/2)),QuatLookAt(Vec(0,0,0),RVec())), 0.1, 0.1, 1, 0, 0, 1,true,true)
-				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1/2)),QuatLookAt(Vec(0,0,0),RVec())), 0.1, 0.1, 0, 0, 1, 1,true,true)
-				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,1/3)),QuatLookAt(Vec(0,0,0),RVec())), 0.05, 0.05, 1, 0, 0, 1,true,true)
-				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1/3)),QuatLookAt(Vec(0,0,0),RVec())), 0.05, 0.05, 0, 0, 1, 1,true,true)
-				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,1/12)),QuatLookAt(Vec(0,0,0),RVec())), 0.15, 0.15, 1, 0, 0, 1,true,true)
-				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1/12)),QuatLookAt(Vec(0,0,0),RVec())), 0.15, 0.15, 0, 0, 1, 1,true,true)
-			end
-		end
-		if bich < 20 then
-			PointLight(middle,1,1,1,5/(bich/10))
-			PointLight(middle,0.1,0.2,1,5/(bich/10))
-			PointLight(middle,1,0.2,0.2,5/(bich/10))
-			DrawSprite(star, Transform(middle,cam.rot), rand(0.02/(bich/10),0.03/(bich/10)), rand(0.02/(bich/10),0.03/(bich/10)), 1, 1, 1, 1,true,true)
-		end
-		if bich <= 1 then
-			pshart = true
-			PNuke = true
-			RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4))
-			PointLight(RedTrack,1,1,1,10/(bich/100))
-			PointLight(RedTrack,0.1,0.2,1,10/(bich/100))
-			PointLight(RedTrack,1,0.2,0.2,10/(bich/100))
-			RVel = Vec(0,0,0)
-			if VecLength(VecSub(origin,RedTrack)) <= 2 then
-				RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
-			end
-			--SetPostProcessingProperty("colorbalance", cb1, cb2, cb3)
-			EntireAssFuckingCutsceneTypeAnimationTimer = 0
-			StStr = 3
-		end
-	end
---2nd animation
-	if EntireAssFuckingCutsceneTypeAnimationTimer > 0 and honored == false then
-		if performance == false then
-			--EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1
-		end
-
-		bich = EntireAssFuckingCutsceneTypeAnimationTimer
-		SetString("game.player.tool","INFINITY")
-		SBlue = false
-		SetPostProcessingProperty("brightness",1.2)
-		SetPostProcessingProperty("saturation",1)
-		SetEnvironmentProperty("fogColor",0,0,0)
-		--SetEnvironmentProperty("fogParams",20,120,0.9,2)
-		SetEnvironmentProperty("skyboxbrightness", bright-0.8)
-		--SetEnvironmentProperty("skyboxtint",tintr-0.95,tintg-0.95,tintb-0.95)
-		SetEnvironmentProperty("sunBrightness",0)
-		--local middle = honoredpos
-		honoredrotata = TransformToParentVec(cam, Vec(-1,0,0))
-		local middle = Vec(0,1000,0)
-		--local middle = VecAdd(origin,dir)
-		BVel = Vec(0,0,0)
-		RVel = Vec(0,0,0)
-		local borigin = VecAdd(origin,Vec(0,-0.5,0))
-		local mid2 = VecAdd(borigin,VecScale(Vec(dir[1],0,dir[3]),-3))
-		adderall = VecScale(honoredrotata,2)
-		if bich > 350 then
-			Str = 0
-			local campos = VecAdd(borigin,VecScale(dir,3))
-			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,borigin))
-			local ccam = Transform(VecAdd(campos,Vec(0,0.2,0)),QuatEuler(c1,c2,c3))
-			SetCameraTransform(ccam)
-			if bich <= 450 then
-				if bich < 450 and bich > 440 then
-					PointLight(VecAdd(mid2,VecScale(adderall,-1)),0.1,0.2,1,10000)
-				end
-				if bich < 400 and bich > 390 then
-					PointLight(VecAdd(mid2,VecScale(adderall,1)),1,0.2,0.2,10000)
-				end
-				for i = 1,100,1 do
-					--DrawSprite(ripple, Transform(VecAdd(mid2,VecScale(adderall,-1)),QuatLookAt(Vec(0,0,0),RVec())), 1, 1, 0, 0, 1, 1,false,false)
-				end
-				for i = 1,360 do
-					DrawSprite(earth, Transform(VecAdd(mid2,VecScale(adderall,-1)),QuatEuler(0,i,0)), 2, 2, 0, 0, 1, 1,true,false)
-				end
-				if bich <= 400 then
-					for i = 1, 100, 1 do
-						--DrawSprite(ripple, Transform(VecAdd(mid2,adderall),QuatLookAt(Vec(0,0,0),RVec())), 1, 1, 1, 0, 0, 1,false,false)
-					end
-					for i = 1,360 do
-						DrawSprite(earth, Transform(VecAdd(mid2,VecScale(adderall,1)),QuatEuler(0,i,0)), 2, 2, 1, 0, 0, 1,true,false)
-					end
-				--	DrawSprite(earth, Transform(VecAdd(mid2,VecScale(adderall,1)),QuatEuler(0,0,i)), 2, 2, 1, 0, 0, 1,true,false)
-				end
-
-			end
-		end
-		if bich <= 350 and bich > 200 then
-			--EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 0.5*(RTime/0.01)
-			--SetTimeScale(0.01)
-			Str = 0
-			local campos = VecAdd(middle,VecScale(Vec(0,-1,0),-2))
-			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,middle))
-			local ccam = Transform(VecAdd(campos,Vec(0,0,0)),QuatEuler(c1,c2,c3))
-			SetCameraTransform(ccam)
-			local add2 = VecScale(Vec(-1,0,0),bich/1000)
-			
-			--for i = 1, 20, 1 do
-				DrawSprite(earth, Transform(VecAdd(middle,VecScale(add2,-1)),QuatEuler(c1,c2,c3)), 1, 1, 0, 0, 1, 1,true,true)
-				DrawSprite(earth, Transform(VecAdd(middle,add2),QuatEuler(c1,c2,c3)), 1, 1, 1, 0, 0, 1,true,true)
-				--DrawSprite(circle,Transform(middle,QuatLookAt(Vec(0,0,0),RVec())),0.4,0.4,0,0,0,0.5,false,false)
-			--end
-			
-				DrawSprite(circle,Transform(VecAdd(middle,VecSub(middle,campos)),QuatEuler(c1,c2,c3)), 20, 20, 0, 0, 0, 1,true,false)
-				--DrawSprite(ripple,Transform(middle,QuatLookAt(Vec(0,0,0),RVec())), 0.8/(bich/150), 0.8/(bich/150), 0.8, 0.2, 1, 1,true,true)
-			--end
-			--PointLight(VecAdd(middle,VecScale(add2,-1)),0.1,0.2,1,100)
-			--PointLight(VecAdd(middle,VecScale(add2,1)),1,0.2,0.2,100)
-		end
-		if bich <= 200 and bich > 100 then
-			--if performance == true then
-			--	EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 0.3*(RTime/0.01)
-			--end
-			--SetTimeScale(0.01)
-			RedTrack = middle
-			local rotarted = QuatLookAt(Vec(0,0,0),TransformToParentVec(cam, Vec(0,0,-1)))
-			local campos = VecAdd(middle,Vec(0,5*math.sin((bich+42)/30)+8,0))
-			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,middle))
-			local ccam = Transform(VecAdd(campos,Vec(0,0.2,0)),QuatEuler(-90,0,0))
-			SetCameraTransform(ccam)
-			DrawSprite(circle,Transform(VecAdd(middle,VecScale(Vec(0,-3,0),1)),QuatEuler(-90,-180,0)), 100, 100, 0, 0, 0, 1,true,false)
-			--DrawSprite(ripple2,Transform(VecAdd(middle,Vec(0,10-bich/200,0)),QuatEuler(-90,-180,0)), 5, 5, 0.6, 0, 1, 1,false,false)
-			PointLight(campos,1,1,1,5)
-			if bich < 200 and bich > 190 then
-				for i = 1, 10 do
-					s = VecAdd(middle,VecScale(RVec(),rand(-Str/6,Str/6)))
-					local e = VecAdd(campos,VecScale(RVec(),rand(Str/2,Str)))
-					local last = s
-					for i=1, 10 do
-						local tt = i/10
-						local p = VecLerp(s, e, tt)
-						p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
-						DrawLine(last, p, 1, 1, 1)
-						last = p
-					end
-				end
-				for i = 0, 1000, 1 do
-					if #dcirc < 1000 then
-						dcirc[#dcirc+1] = QuatEuler(rand(-180,180),rand(-180,180),rand(-180,180))
-						ctime[#ctime+1] = rand(-160,200)
-					end
-				end
-				--if bich < 200 and bich > 190 then
-				
-				--end
-				--DrawSprite(circle,Transform(VecAdd(campos,Vec(0,-4,0)),QuatEuler(c1,c2,c3)),10,10,0,0,0,1,true,false)
-			end
-			
-			PNuke = false
-			Str = 16
-			if bich <= 150 then
-				RVel = Vec(0,0,0)
-				for i = 1, #dcirc, 1 do
-					ctime[i] = ctime[i] - 0.1*(RTime)
-					c = ctime[i]
-					cspace = VecScale(QuatRotateVec(dcirc[i],Vec(math.cos(160/(c/10))*(c/120),0,math.sin(160/(c/10))*(c/120))),Str/10)
-					DrawSprite(circle, Transform(VecAdd(RedTrack,cspace),rotarted), (0.1),(0.1), math.abs(ctime[i])/60+0.6, 0.6, math.abs(ctime[i])/60+0.6, 1,true,true)
-					if ctime[i]<= -160 then
-						ctime[i] = 200
-					end
-				end
-			end
-		end
-		QueryRequire("static")
-		local h,d,n = QueryRaycast(VecAdd(VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4)),VecScale(Vec(0,1,0),Str/12)),Vec(0,-1,0),Str/3)
-		if bich <= 100 then
-			--EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer + 0.5*RTime
-			--h = true
-			if h then
-				--RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4))
-				--RedTrack = VecAdd(VecAdd(VecAdd(VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4)),VecScale(Vec(0,1,0),Str/12)),VecScale(Vec(0,-VecSub(RedTrack,Feet.pos)[2]-1,0),1)),VecScale(Vec(0,1,0),Str/20))
-				RedTrack = VecAdd(VecSub(origin,Vec(0,0.2-Str/20,0)),VecScale(Vec(dir[1],0,dir[3]),Str/4))
-				RVel = VecScale(pvel,0.018)
-			else
-			RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4))
-			RVel = Vec(0,0,0)
-			end
-			PNuke = true
-			if bich < 100 and bich > 95 then
-				Str = 0
-				
-			end
-			if bich < 100 then
-				if performance == true then
-					Str = Str+0.4*(bich/100)*RTime
-				else
-					Str = Str+0.4*(bich/100)
-				end
-				if InputDown(GetString("savegame.mod.inf.sadd")) then
-					Str = Str + 1
-				end
-				if InputDown(GetString("savegame.mod.inf.ssub")) then
-					Str = Str - 1
-				end
-			end
-		end
-		--DebugPrint(bich)
-		if bich <= 5 then
-			PointLight(RedTrackD,0.8,0.4,1,Str*2000)
-			PointLight(RedTrackD,0.8,0.4,1,Str*2000)
-			DrawSprite(star, Transform(RedTrackD,cam.rot), rand(Str/1.2,Str/0.8), rand(Str/1.2,Str/0.8), 1, 1, 1, 1,false,false)
-		end
-		if bich <= 1 then
-			if h then
-				RVel = VecScale(Vec(dir[1],0,dir[3]),1)
-			else
-				RVel = VecScale(dir,1)
-			end
-			--DebugPrint("done")
-			pshart = true
-			PNuke = true
-			--bich = 0
-			EntireAssFuckingCutsceneTypeAnimationTimer = 0
-			PlaySound(pShot,RedTrack,1,false,10)
-		end
-	end
-	
-end
-
-function update(dt)
-	if GetString("game.player.tool") == "INFINITY" then
-		--Gravity stuffs at the red and blue (purple too)
-		BROTIME = BROTIME + 1
-		if BROTIME >= 360 then
-			BROTIME = 0
-		end
-		--Red
-		if SRed and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
-			if Burnout == 0 then
-				if PNuke == false then
-					if InputDown("grab") then
-						RedStr = RedStr + 0.1
-					end
-				end
-			end
-		end
-		if SBlue and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
-			if Burnout == 0 then
-				if PNuke == false then
-					if InputDown("usetool") then
-						BluStr = BluStr + 0.1
-					end
-				end
-			end
-		end
-	end
-		if SRed and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
-			if Burnout == 0 then
-				if PNuke == false then
-					RSP = VecLength(VecScale(RVel,1))
-					for i = 0, RSP,0.1 do
-						RedTrackD = VecAdd(RedTrack,VecScale(RVel,i))
-						if RedStr > 0.5 then
-							--Shoot(RedTrackD,VecNormalize(RVel),"shotgun",RedStr/4,0.1)
-							--if telek == true then
-							--	Shoot(RedTrackD,VecNormalize(RVel),"shotgun",RedStr/4,0.1)
-							--end
-						else
-							
-							--GDrag(RedTrackD,VecScale(RVel,1/0.018),1)
-						end
-					end
-					if not telek then
-						Gravity(RedTrackD,-RedStr,RedStr/2)
-					end
-					if performance == true then
-						if SBlue == true then
-							for i = 1,100,1 do
-								local gdis = VecScale(VecNormalize(RVec()),rand(RedStr/20,RedStr/9.5))
-								local gspawn = VecAdd(RedTrack,gdis)
-								ParticleType("plain")
-								ParticleTile(4)
-								ParticleColor(1,1,1,1,0,0)
-								ParticleRadius(RedStr/90)
-								ParticleAlpha(0.9,0)
-								ParticleGravity(0)
-								ParticleDrag(0)
-								ParticleEmissive(10)
-								ParticleRotation(rand(-10,10))
-								ParticleCollide(0)
-								local rotata = TransformToParentVec(cam, Vec(1,0,0))
-								local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-								local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
-								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-RedStr/3)),0.1)
-							end
-							for i = 1,500,1 do
-								local gdis = VecScale(VecNormalize(RVec()),rand(RedStr/8,RedStr/9))
-								local gspawn = VecAdd(RedTrack,gdis)
-								ParticleType("plain")
-								ParticleTile(5)
-								ParticleColor(1,0.3,0.3,1,0,0)
-								ParticleRadius(RedStr/80)
-								ParticleAlpha(0,0.9)
-								ParticleGravity(0)
-								ParticleDrag(0)
-								ParticleEmissive(1)
-								ParticleRotation(rand(-10,10))
-								ParticleCollide(0)
-								local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-								local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
-								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-RedStr/3)),0.1)
-							end
-							if telek == false and (RedStr < 80 and performance) then
-								for i = 0, 1, 1 do
-									local gspawn = RedTrack
-									ParticleType("plain")
-									ParticleTile(4)
-									ParticleColor(1,0.5,0.5,1,0,0)
-									ParticleRadius(RedStr/7)
-									ParticleAlpha(0.3,0)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(1)
-									ParticleRotation(100)
-									ParticleCollide(0)
-									SpawnParticle(gspawn,VecScale(RVel,1/0.01),0.15)
-								end
-							end
-						else
-							for i = 1,100,1 do
-								local gdis = VecScale(VecNormalize(RVec()),rand(1/20,1/6.5))
-								local gspawn = VecAdd(RedTrack,gdis)
-								ParticleType("plain")
-								ParticleTile(4)
-								ParticleColor(1,1,1,1,0,0)
-								ParticleRadius(1/90)
-								ParticleAlpha(0.9,0)
-								ParticleGravity(0)
-								ParticleDrag(0)
-								ParticleEmissive(10)
-								ParticleRotation(rand(-10,10))
-								ParticleCollide(0)
-								local rotata = TransformToParentVec(cam, Vec(1,0,0))
-								local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-								local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
-								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-1/3)),0.1)
-							end
-							for i = 1,500,1 do
-								local gdis = VecScale(VecNormalize(RVec()),rand(1/8,1/6))
-								local gspawn = VecAdd(RedTrack,gdis)
-								ParticleType("plain")
-								ParticleTile(5)
-								ParticleColor(1,0,0,1,0,0)
-								ParticleRadius(1/80)
-								ParticleAlpha(0,0.9)
-								ParticleGravity(0)
-								ParticleDrag(0)
-								ParticleEmissive(1)
-								ParticleRotation(rand(-10,10))
-								ParticleCollide(0)
-								local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-								local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
-								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-1/3)),0.1)
-							end
-							--[[
-							for i = 1,60,1 do
-								local gdis = VecScale(VecNormalize(RVec()),rand(1/8,1/6))
-								local gspawn = VecAdd(RedTrack,gdis)
-								ParticleType("plain")
-								ParticleTile(5)
-								ParticleColor(1,0.3,0.3,1,0,0)
-								ParticleRadius(1/80)
-								ParticleAlpha(0,0.9)
-								ParticleGravity(0)
-								ParticleDrag(0)
-								ParticleEmissive(1)
-								ParticleRotation(rand(-10,10))
-								ParticleCollide(0)
-								local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-								local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(0,0,-2))))
-								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-1/3)),0.1)
-							end
-							]]
-							if (RedStr < 80 and performance) then
-								for i = 0, 1, 1 do
-									local gspawn = RedTrack
-									ParticleType("plain")
-									ParticleTile(4)
-									ParticleColor(1,0.5,0.5,1,0,0)
-									ParticleRadius(1/7)
-									ParticleAlpha(0.3,0)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(RedStr)
-									ParticleRotation(100)
-									ParticleCollide(0)
-									SpawnParticle(gspawn,VecScale(RVel,1/0.01),0.15)
-								end
-							end
-						end
-					end
-				end
-			end
-		end
-		--Blue
-		if SBlue == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
-			if Burnout == 0 then
-				if PNuke == false then
-					if performance == true then
-						if BluStr < 80 and not telek then
-							if SRed == false then
-								for i = 1,100,1 do
-									local gdis = VecScale(VecNormalize(RVec()),rand(0.01,BluStr/15))
-									local gspawn = VecAdd(BlueTrack,gdis)
-									ParticleType("plain")
-									ParticleTile(4)
-									ParticleColor(1,1,1,0,0,1)
-									ParticleRadius(BluStr/400)
-									ParticleAlpha(0.9,0)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(10)
-									ParticleRotation(rand(-10,10))
-									ParticleCollide(0)
-									local rotata = TransformToParentVec(cam, Vec(1,0,0))
-									local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
-									local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0.5)))
-									SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-BluStr/3)),0.2)
-								end
-								for i = 1,100,1 do
-									local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/8,BluStr/5))
-									local gspawn = VecAdd(BlueTrack,gdis)
-									ParticleType("plain")
-									ParticleTile(5)
-									ParticleColor(0.2,1,0.8,0,0,1)
-									ParticleRadius(BluStr/50)
-									ParticleAlpha(0,0.5)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(1)
-									ParticleRotation(rand(-10,10))
-									ParticleCollide(0)
-									local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
-									local spidir = TransformToParentVec(look, Vec(-1,-1,0))
-									--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.018),VecScale(gdis,-3)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.25)
-									SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,-3)),VecScale(VecScale(spidir,BluStr/10/VecLength(gdis)),BluStr/2)),0.2)
-								end
-								for i = 1,100,1 do
-									local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/8,BluStr/5))
-									local gspawn = VecAdd(BlueTrack,gdis)
-									ParticleType("plain")
-									ParticleTile(5)
-									ParticleColor(0.2,1,0.8,0,0,1)
-									ParticleRadius(BluStr/50)
-									ParticleAlpha(0,0.5)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(1)
-									ParticleRotation(rand(-10,10))
-									ParticleCollide(0)
-									local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
-									local spidir = TransformToParentVec(look, Vec(1,1,0))
-									SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,-3)),VecScale(VecScale(spidir,BluStr/10/VecLength(gdis)),BluStr/2)),0.2)
-								end
-							else
-								for i = 1,100,1 do
-									local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/20,BluStr/9))
-									local gspawn = VecAdd(BlueTrack,gdis)
-									ParticleType("plain")
-									ParticleTile(4)
-									ParticleColor(1,1,1,0,0,1)
-									ParticleRadius(BluStr/90)
-									ParticleAlpha(0.9,0)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(10)
-									ParticleRotation(rand(-10,10))
-									ParticleCollide(0)
-									local rotata = TransformToParentVec(cam, Vec(1,0,0))
-									local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
-									local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
-									SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-BluStr/3)),0.1)
-								end
-								for i = 1,500,1 do
-									local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/8,BluStr/9))
-									local gspawn = VecAdd(BlueTrack,gdis)
-									ParticleType("plain")
-									ParticleTile(5)
-									ParticleColor(0.3,0.8,1,0,0,1)
-									ParticleRadius(BluStr/80)
-									ParticleAlpha(0,0.9)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(1)
-									ParticleRotation(rand(-10,10))
-									ParticleCollide(0)
-									local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
-									local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
-									SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-BluStr/3)),0.1)
-								end
-							end
-							for i = 1,50,1 do
-								local gdis = VecScale(VecNormalize(RVec()),rand(BluStr,BluStr*5))
-								local gspawn = VecAdd(BlueTrack,gdis)
-								ParticleType("plain")
-								ParticleTile(5)
-								ParticleColor(1,1,1)
-								ParticleRadius(BluStr/80)
-								ParticleAlpha(0,1)
-								ParticleGravity(0)
-								ParticleDrag(0)
-								ParticleEmissive(0)
-								ParticleRotation(rand(-10,10))
-								local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
-								local spidir = TransformToParentVec(look, Vec(-1,1,0))
-								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,-3)),VecScale(VecScale(spidir,BluStr/11/VecLength(gdis)),BluStr/3)),0.2)
-							end
-							if telek == false and (BluStr < 80 and performance) then
-								for i = 0, 1, 1 do
-									local gspawn = BlueTrack
-									ParticleType("plain")
-									ParticleTile(4)
-									ParticleColor(0.5,1,1,0,0,1)
-									ParticleRadius(BluStr/7)
-									ParticleAlpha(0.3,0)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(1)
-									ParticleRotation(100)
-									ParticleCollide(0)
-									SpawnParticle(gspawn,VecScale(BVel,1/0.01),0.15)
-								end
-							end
-						end
-						if telek or BluesMerge then
-							for j = 1, #smbt do
-								for i = 0,30,1 do
-									local gdis = VecScale(VecNormalize(RVec()),rand(5/20,5/9))
-									local gspawn = VecAdd(smbt[j],gdis)
-									ParticleType("plain")
-									ParticleTile(4)
-									ParticleColor(1,1,1,0,0,1)
-									ParticleRadius(5/90)
-									ParticleAlpha(0.9,0)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(10)
-									ParticleRotation(rand(-10,10))
-									ParticleCollide(0)
-									local rotata = TransformToParentVec(cam, Vec(1,0,0))
-									local look = Transform(smbt[j],QuatLookAt(smbt[j],gspawn))
-									local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
-									SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(smbv[j],1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-5/3)),0.1)
-								end
-								for i = 0, 1, 1 do
-									local gspawn = smbt[j]
-									ParticleType("plain")
-									ParticleTile(4)
-									ParticleColor(0.3,0.8,1,0,0,1)
-									ParticleRadius(5/6)
-									ParticleAlpha(0.9,0)
-									ParticleGravity(0)
-									ParticleDrag(0)
-									ParticleEmissive(1)
-									ParticleRotation(100)
-									ParticleCollide(0)
-									SpawnParticle(gspawn,VecScale(smbv[j],1/0.01),0.15)
-								end
-							end
-						end
-					end
-					--if InputDown("q") == false then
-					if telek == false then
-						QueryRequire("dynamic")
-						local shit = QueryClosestPoint(BlueTrack,BluStr)
-						if BluStr > 8 then
-							Shoot(BlueTrack,Vec(0,0,0),"shotgun",BluStr/2,0.005)
-						else
-							GDrag(BlueTrack,VecScale(BVel,1/0.015),0.001)
-						end
-						if shit == false then
-							for i = 0,VecLength(BVel),0.1 do
-								local BTS = VecAdd(BlueTrack,VecScale(BVel,i))
-								if BluStr > 8 then
-									MakeHole(BTS,BluStr/5,BluStr/5,BluStr/5)
-								end
-							end
-						end
-						Gravity(BlueTrack,BluStr,BluStr)
-					end
-					if telek or BluesMerge then
-						if not InputDown(GetString("savegame.mod.inf.grab")) and ShotBlueTime > 0 then
-							ShotBlueTime = ShotBlueTime - 1
-						end
-						for j = 1, #smbt do
-							for i = 0,VecLength(smbv[j]),0.2 do
-								local BTS = VecAdd(smbt[j],VecScale(smbv[j],i))
-								local shit = QueryClosestPoint(BTS,0.9)
-								if shit then
-									Shoot(BTS,Vec(0,0,0),"shotgun",5/2,0.005)
-									MakeHole(BTS,0.8,0.8,0.8)
-								end
-							end
-							Gravity(smbt[j],2,2)
-						end
-					end
-					--end
-				end
-			end
-		end
-		if (SRed and SBlue) then
-			if VecLength(VecSub(RedTrack,BlueTrack)) < Str/5 then
-				if performance == true then
-					Blight = VecAdd(VecScale(VecSub(BlueTrack,RedTrack),0.5),RedTrack)
-					for i = 1,50,1 do
-						local gdis = VecScale(VecNormalize(RVec()),Str/3)
-						local gspawn = VecAdd(Blight,gdis)
-						ParticleType("plain")
-						ParticleTile(5)
-						ParticleColor(1,0,0)
-						ParticleRadius(Str/80)
-						ParticleAlpha(0,1)
-						ParticleGravity(0)
-						ParticleDrag(0)
-						ParticleEmissive(1)
-						ParticleRotation(rand(-10,10))
-						local look = Transform(Blight,QuatLookAt(Blight,gspawn))
-						local spidir = TransformToParentVec(look, Vec(0,0,-1))
-						SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),1/0.01),VecScale(gdis,5)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.5)
-					end
-					for i = 1,50,1 do
-						local gdis = VecScale(VecNormalize(RVec()),Str/3)
-						local gspawn = VecAdd(Blight,gdis)
-						ParticleType("plain")
-						ParticleTile(5)
-						ParticleColor(0,0.4,1)
-						ParticleRadius(Str/80)
-						ParticleAlpha(0,1)
-						ParticleGravity(0)
-						ParticleDrag(0)
-						ParticleEmissive(1)
-						ParticleRotation(rand(-10,10))
-						local look = Transform(Blight,QuatLookAt(Blight,gspawn))
-						local spidir = TransformToParentVec(look, Vec(0,0,-1))
-						SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),1/0.01),VecScale(gdis,5)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.5)
-					end
-				end
-			end
-		end
-		--purple
-		if PNuke == true and (InputDown(GetString("savegame.mod.inf.time")) == false or honored == false) then
-			if NukeTime == 0 then
-				--DebugPrint((VecLength(RVel)/time))
-				local bzzt = QueryAabbShapes(VecAdd(RedTrack,Vec(-Str,-Str,-Str)),VecAdd(RedTrack,Vec(Str,Str,Str)))
-				for i=1,#bzzt do
-					if rand(0,10) > 9.9 then
-						local hit, e = GetShapeClosestPoint(bzzt[i],RedTrack)
-						--e = GetShapeWorldTransform(bzzt[i]).pos
-						s = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/6,Str/6)))
-						--Draw laser line in ten segments with random offset, stolen from teardown lazer gun built-in-mod
-						local last = s
-						for i=1, 15 do
-							local tt = i/15
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(1.2*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-					end
-				end
-				if rand(0,10) > 9.9 then
-					for i = 1, 2 do
-						s = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/6,Str/6)))
-						local e = VecAdd(RedTrack,VecScale(RVec(),rand(Str/2,Str)))
-						local last = s
-						for i=1, 10 do
-							local tt = i/10
-							local p = VecLerp(s, e, tt)
-							p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
-							DrawLine(last, p, 1, 1, 1)
-							last = p
-						end
-					end
-				end
-				if Str > 8 then
-					if honored == false and InputDown(GetString("savegame.mod.inf.time")) == false then
-						Gravity(RedTrack,Str*4,Str*0.3,_)
-					end
-					if performance == true then
-						for i = 1,50,1 do
-							local gdis = VecScale(VecNormalize(RVec()),rand(Str/7,Str*3))
-							local gspawn = VecAdd(RedTrack,gdis)
-							ParticleType("plain")
-							ParticleTile(5)
-							ParticleColor(1,1,1)
-							ParticleRadius(Str/40)
-							ParticleAlpha(0,1)
-							ParticleGravity(0)
-							ParticleDrag(0)
-							ParticleEmissive(1)
-							ParticleRotation(rand(-10,10))
-							local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-							local spidir = TransformToParentVec(look, Vec(0,0,-1))
-							SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,-3)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.25)
-						end
-					end
-				end
-				if performance == true then
-					for i = 1,100,1 do
-						local gdis = VecScale(VecNormalize(RVec()),rand(Str/20,Str/8))
-						local gspawn = VecAdd(RedTrack,gdis)
-						ParticleType("plain")
-						ParticleTile(4)
-						ParticleColor(1,1,1,0.5,0,1)
-						ParticleRadius(Str/90)
-						ParticleAlpha(0.9,0)
-						ParticleGravity(0)
-						ParticleDrag(0)
-						ParticleEmissive(1000)
-						ParticleRotation(rand(-10,10))
-						ParticleCollide(0)
-						local rotata = TransformToParentVec(cam, Vec(1,0,0))
-						local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-						local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),-0.5)))
-						SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-Str/3)),0.2)
-					end
-					for i = 1,500,1 do
-						local gdis = VecScale(VecNormalize(RVec()),rand(Str/8,Str/7))
-						local gspawn = VecAdd(RedTrack,gdis)
-						ParticleType("plain")
-						ParticleTile(5)
-						ParticleColor(1,0.8,1,0.8,0,1)
-						ParticleRadius(Str/80)
-						ParticleAlpha(0,0.9)
-						ParticleGravity(0)
-						ParticleDrag(0)
-						ParticleEmissive(1)
-						ParticleRotation(rand(-10,10))
-						ParticleCollide(0)
-						local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-						local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
-						SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-Str/3)),0.2)
-					end
-					--if (Str < 80 and performance) then
-						for i = 0, 1, 1 do
-							local gspawn = RedTrack
-							ParticleType("plain")
-							ParticleTile(4)
-							ParticleColor(1,0.8,1,0.8,0,1)
-							ParticleRadius(Str/7)
-							ParticleAlpha(0.3,0)
-							ParticleGravity(0)
-							ParticleDrag(0)
-							ParticleEmissive(10)
-							ParticleRotation(100)
-							ParticleCollide(0)
-							SpawnParticle(gspawn,VecScale(RVel,1/0.01),0.15)
-						end
-					--end
-				end
-			end
-			if NukeTime > 0 then
-				NukeS = (Str/3)/NukeTime
-
-				Gravity(RedTrack,-NukeS*60,NukeS,"dynamic")
-				Destroy(RedTrack,NukeS*0.5,true,0,0,NukeS*0.5)
-				Destroy(RedTrack,NukeS*0.5,true,0,0,NukeS*0.5)
-				if performance == true then
-					for i = 1,500,1 do
-						local gdis = VecScale(VecNormalize(RVec()),NukeS/1.5)
-						local gspawn = VecAdd(RedTrack,gdis)
-						ParticleType("plain")
-						ParticleTile(4)
-						ParticleColor(1,1,1,0.4,0,1)
-						ParticleRadius(NukeS/30)
-						ParticleAlpha(1,0)
-						ParticleGravity(0)
-						ParticleDrag(1)
-						ParticleEmissive(1)
-						ParticleRotation(rand(-10,10))
-						ParticleCollide(0)
-						local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-						local spidir = TransformToParentVec(look, Vec(-1,0,0))
-						SpawnParticle(gspawn,VecAdd(VecAdd(Vec(0,0,0),VecScale(gdis,5)),VecScale(VecScale(spidir,1),-Str/3)),0.1)
-					end
-					if NukeTime < 0.15 then
-						for i = 1,1000,1 do
-							local gdis = VecScale(VecNormalize(RVec()),NukeS/1.5)
-							local gspawn = VecAdd(RedTrack,gdis)
-							ParticleType("plain")
-							ParticleTile(5)
-							ParticleColor(1,1,1,0.4,0,1)
-							ParticleRadius(NukeS/40)
-							ParticleAlpha(1,0)
-							ParticleGravity(0)
-							ParticleDrag(0)
-							ParticleEmissive(1)
-							ParticleRotation(rand(-10,10))
-							ParticleCollide(0)
-							local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
-							local spidir = TransformToParentVec(look, Vec(-1,0,0))
-							SpawnParticle(gspawn,VecAdd(Vec(0,0,0),VecScale(VecScale(spidir,1),-Str/3)),1)
-						end
-					end
-				end
-
-				NukeTime = NukeTime -0.05
-				if NukeTime < 0.1 then
-					PNuke = false
-					NRelease = false
-					NukeTime = 0
-				end
-			end
-		end
-	--infinity stuff
-	if InfToggle then
-		--MakeHole(origin,rand(-50,Str),rand(-100,Str/2),rand(-100,Str/3))
-		Infinity(origin,5,pvel,true,false,false,false)
-		Infinity(Feet.pos,5,pvel,true,true,false,false)
-		if GetPlayerHealth() > HP then
-			HP = GetPlayerHealth()
-		end
-		SetPlayerHealth(HP)
-		SetPlayerParam("GodMode",true)
-	else
-		SetPlayerParam("GodMode",false)
-	end
---warp
-	if tpStr > 1 then
-		
-		if time == 1 then
-			SetPlayerVelocity(VecAdd(pvel,VecScale(dir,scrollPos)))
-			SetPlayerTransformWithPitch(Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot))
-			tpStr = tpStr - 1
-			--SetCameraFov((-tpStr*10)+180)
-		else
-			--SetPlayerTransform(Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot),true)
-			--SetCameraFov((-tpStr*10)+180)
-		end
-	else
-		if tpStr > 0 then
-			tpStr = 0
-		end
-	end
-	if tpStr == 1 then
-		--SetCameraFov(360)
-		SetPlayerVelocity(VecScale(dir,VecLength(tpvel)))
-		tpStr = 0
-	end
-	--if GetBool("savegame.mod.inf.toolless") == true or GetString("game.player.tool") == "INFINITY" then
-		--if InputDown(GetString("savegame.mod.inf.flykey")) then
-		if FlyToggle then
-			PlayerGravity(origin,pvel,BlueTrack,BluStr,dir,scrollPos)
-		end
-	--end
---DOMAIN STUFF
-	if DomActivate > 1 then
-			DomActivate = DomActivate - 1
-			--DebugPrint(DomActivate)
-			--local hit, dis, gp = QueryRaycast(origin,dir,10)
-	--balls
-			for i = -1,1,0.3 do
-				for j = -1,1,0.3 do
-			
-					local GDir = QuatRotateVec(DPR,VecNormalize(Vec(i,j,0)))
-					--local GDir = Vec(i,j,k)
-					--local hit, dis, gp = QueryRaycast(origin,GDir,10)
-					local what = ((DomActivate)/10/math.pi)
-					--DebugPrint(math.sin(what))
-					local gspawn = VecAdd(VecAdd(DPP,VecScale(DPD,(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
-					--local gspawn = VecAdd(VecAdd(Feet.pos,VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
-					ParticleType("plain")
-					ParticleTile(3)
-					ParticleColor(1,1,1)
-					ParticleRadius(3)
-					ParticleAlpha(1)
-					ParticleGravity(0)
-					ParticleDrag(0)
-					ParticleEmissive(1)
-					ParticleRotation(0)
-					ParticleCollide(0)
-					SpawnParticle(gspawn,Vec(0,0,0),3)
-					PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
-				end
-			end
-
-			for i = -1,1,0.3 do
-				for j = -1,1,0.3 do
-			
-					local GDir = VecNormalize(Vec(i,j,0))
-					--local GDir = Vec(i,j,k)
-					--local hit, dis, gp = QueryRaycast(origin,GDir,10)
-					local what = ((DomActivate)/10/math.pi)
-					--DebugPrint(math.sin(what))
-					--local gspawn = VecAdd(VecAdd(origin,VecScale(dir,(50-DomActivate)/10)),VecScale(GDir,20*math.sin(what)))
-					local gspawn = VecAdd(VecAdd(VecAdd(DPP,Vec(0,10000,0)),VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
-					ParticleType("plain")
-					ParticleTile(3)
-					ParticleColor(1,1,1)
-					ParticleRadius(3)
-					ParticleAlpha(1)
-					ParticleGravity(0)
-					ParticleDrag(0)
-					ParticleEmissive(1)
-					ParticleRotation(0)
-					ParticleCollide(0)
-					SpawnParticle(gspawn,Vec(0,0,0),1.5)
-					PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
-				end
-			end
-		end
-	--domain itself
-	if DomainToggle == true then
-		--SetShapeBody(ovoid,GetWorldBody(),Transform(VecAdd(DPP,Vec(-10,0,10)),QuatEuler(-90,0,0)))
-		SetBodyTransform(voidb,Transform(VecAdd(DomainPos,Vec(0,-1,0)),QuatEuler(0,0,0)))
-		SetBodyVelocity(voidb,Vec(0,0,0))
-		SetBodyAngularVelocity(voidb,Vec(0,0,0))
-		--DebugTransform(GetBodyTransform(voidb))
-		DrawBodyHighlight(voidb,1)
-
-		SetBodyTransform(ovoidb,Transform(VecAdd(DPP,Vec(0,-1,0)),QuatEuler(0,0,0)))
-		SetBodyVelocity(ovoidb,Vec(0,0,0))
-		SetBodyAngularVelocity(ovoidb,Vec(0,0,0))
-		DrawBodyHighlight(ovoidb,1)
-		--DebugCross(GetBodyTransform(ovoidb).pos)
-		SetPostProcessingProperty("brightness",2)
-		if GetPlayerHealth() > HP then
-			HP = GetPlayerHealth()
-		end
-		SetPlayerHealth(HP)
-		SetPlayerParam("GodMode",true)
-		QueryRejectBody(voidb)
-		local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-20,-50)),VecAdd(DomainPos,Vec(50,50,50)))
-		for i = 1, #dbodies do
-			local dbody = dbodies[i]
-			if IsBodyDynamic(dbody) then
-				jbodies = GetJointedBodies(dbody)
-				for j = 1,#jbodies do
-					local jbody = jbodies[j]
-					local add = true
-					for k = 1, #dbodies do
-						if jbody == dbodies[k] then
-							add = false
-						end
-					end
-					if add then
-						dbodies[#dbodies+1] = jbody
-					end
-				end
-			end
-		end
-		--makes everything in the domain stop thinking (only works with teardown robots as of now)
-		for i = 1, #dbodies do
-			local dbody = dbodies[i]
-			if not HasTag(dbody, "sleeping") then
-				SetTag(dbody, "sleeping")
-			end
-		end
-		-- my feeble attempts to temporarily lobotomize the AUTUMNATIC zombies, mostly just code ripped straight from that mod
-			
-		if DsTimer >= 1 then 
-			DsTimer = DsTimer + 1
-			for i = 1,5, 1 do
-				local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,rand(-200,200))),VecScale(VecNormalize(Vec(rand(-1,1),rand(-1,1),0)),40))
-				ParticleType("plain")
-				ParticleTile(1)
-				ParticleColor(1,1,1)
-				ParticleRadius(5)
-				ParticleAlpha(0,1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(1)
-				ParticleRotation(0)
-				--SpawnParticle(gspawn,VecScale(Vec(0,0,1),-20),2)
-			end
-		end
-		--when the wackass lines end
-		if DsTimer > 200 then
-			DsTimer = 0
-			--white shit on the screen
-			for i = 1,20,1 do
-				local gspawn = VecAdd(DomainPos,VecScale(VecNormalize(RVec()),rand(20,40)))
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(1,1,1)
-				ParticleRadius(7)
-				ParticleAlpha(1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(1)
-				ParticleRotation(0)
-
-				--SpawnParticle(gspawn,Vec(0,0,0),100)
-			end
-			fogtimer = 600
-		end
-		if DsTimer == 0 then
-			--local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-20,-50)),VecAdd(DomainPos,Vec(50,50,50)))
-			--for i = 1, #dbodies do
-			--	local dbody = dbodies[i]
-			--	if IsBodyDynamic(dbody) then
-					--SetTag(dbody, "inactive")
-					--dtran = GetBodyTransform(dbody)
-					--Shoot(dtran.pos,Vec(0,1,0),"shotgun",-1,0.01)
-					--DebugPrint(ListTags(dbody))
-			--	end
-			--end
-			local BHoleD = VecNormalize(VecSub(BHolePos,DomainPos))
-			local BHoleDP = VecAdd(BHolePos,VecScale(BHoleD,9))
-			--VisChain(BHoleDP,100,1,1,1,1,0.7,0.4,60,60,false,1,Vec(0,0,0),cam,false)
-			--VisChain(BHoleDP,100,1,1,1,1,1,1,60,60,false,1,Vec(-1,0,0),cam,false)
-			--PointLight(VecAdd(BHolePos,),1,1,1,1000)
-			
-			--complex ass fog (not really)
-			for i = 1,40,1 do
-				local gdis = VecScale(VecNormalize(Vec(rand(0,1),0,rand(-1,1))),130)
-				local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,10,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(rand(0.75,0.8),rand(0.85,0.9),1)
-				ParticleRadius(5,rand(10,30))
-				ParticleAlpha(1,0)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(0.5,0)
-				ParticleCollide(1)
-				ParticleRotation(0)
-				local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
-				local spidir = TransformToParentVec(look, Vec(-2,rand(-5,5),0))
-				--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),0.1)
-				SpawnParticle(gspawn,VecScale(spidir,2),2)
-			end
-			for i = 1,40,1 do
-				local gdis = VecScale(VecNormalize(Vec(rand(0,-1),0,rand(-1,1))),130)
-				local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,10,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(rand(0.75,0.8),rand(0.85,0.9),1)
-				ParticleRadius(5,rand(10,30))
-				ParticleAlpha(1,0)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(0.5,0)
-				ParticleCollide(1)
-				ParticleRotation(0)
-				local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
-				local spidir = TransformToParentVec(look, Vec(2,rand(-5,5),0))
-				--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),0.1)
-				SpawnParticle(gspawn,VecScale(spidir,2),2)
-			end
-			for i = 1,5,1 do
-				local gdis = VecScale(VecNormalize(Vec(rand(0,-1),rand(-1,1),0)),15)
-				local gspawn = VecAdd(VecAdd(BHolePos,Vec(0,0,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(1,1,1)
-				ParticleRadius(4)
-				ParticleAlpha(0,1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(1)
-				ParticleCollide(0)
-				ParticleRotation(0)
-				local look = Transform(BHolePos,QuatLookAt(BHolePos,gspawn))
-				local spidir = TransformToParentVec(look, Vec(0,2,0))
-				--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
-				SpawnParticle(gspawn,VecScale(spidir,1),1)
-			end
-			for i = 1,5,1 do
-				local gdis = VecScale(VecNormalize(Vec(rand(0,1),rand(-1,1),0)),15)
-				local gspawn = VecAdd(VecAdd(BHolePos,Vec(0,0,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(1,1,1)
-				ParticleRadius(4)
-				ParticleAlpha(0,1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(1)
-				ParticleCollide(0)
-				ParticleRotation(0)
-				local look = Transform(BHolePos,QuatLookAt(BHolePos,gspawn))
-				local spidir = TransformToParentVec(look, Vec(0,-2,0))
-				--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
-				SpawnParticle(gspawn,VecScale(spidir,1),1)
-			end
-			for i = 1,100,1 do
-				local gdis = VecScale(VecNormalize(Vec(rand(-1,1),rand(-1,1),0)),40)
-				local gspawn = VecAdd(VecAdd(BHolePos,Vec(0,0,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(4)
-				ParticleColor(1,1,0.5,0.5,1,0.5)
-				ParticleRadius(1,0)
-				ParticleAlpha(1,1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(rand(0.5,1),0.1)
-				ParticleCollide(0)
-				ParticleRotation(0)
-				local look = Transform(BHolePos,QuatLookAt(BHolePos,gspawn))
-				local spidir = TransformToParentVec(look, Vec(0,0,4))
-				--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
-				SpawnParticle(gspawn,VecScale(spidir,1),1)
-			end
-			for i = 1,50,1 do
-				local gdis = VecScale(VecNormalize(RVec()),200)
-				local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(0.4,rand(0.5,0.9),1)
-				ParticleRadius(rand(10,50),rand(1,50))
-				ParticleAlpha(0,0.1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(rand(0,8),0)
-				ParticleCollide(0)
-				ParticleRotation(0)
-				local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
-				local spidir = TransformToParentVec(look, Vec(0,0,3))
-				--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
-				SpawnParticle(gspawn,VecScale(spidir,1),4)
-			end
-			for i = 1,20,1 do
-				local gdis = VecScale(VecNormalize(RVec()),160)
-				local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				ParticleColor(0.1,0.1,0.1)
-				ParticleRadius(rand(1,50),rand(1,50))
-				ParticleAlpha(1,1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(0)
-				ParticleCollide(0)
-				ParticleRotation(0)
-				local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
-				local spidir = TransformToParentVec(look, Vec(0,0,-0))
-				--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
-				SpawnParticle(gspawn,VecScale(spidir,1),4)
-			end
-			for i = 1, 2,1 do
-				local gdis = VecScale(Vec(rand(-80,80),rand(-80,80),rand(-80,80)),1)
-				local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,0)),gdis)
-				ParticleType("plain")
-				ParticleTile(1)
-				ParticleColor(1,1,1)
-				ParticleRadius(2)
-				ParticleAlpha(0,1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(1)
-				ParticleCollide(0)
-				SpawnParticle(gspawn,VecScale(Vec(0,1,0),rand(0.1,1)),5)
-			end
-		end
-		--Back in the regular world
-		if false then --remove if wanted
-			for i = -1,1,0.3 do
-				for j = -1,1,0.3 do
-			
-					local GDir = QuatRotateVec(DPR,VecNormalize(Vec(i,j,0)))
-					--local GDir = Vec(i,j,k)
-					--local hit, dis, gp = QueryRaycast(origin,GDir,10)
-					local what = ((rand(0,100))/10/math.pi)
-					--DebugPrint(math.sin(what))
-					local gspawn = VecAdd(VecAdd(DPP,VecScale(DPD,(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
-					--local gspawn = VecAdd(VecAdd(Feet.pos,VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
-					ParticleType("plain")
-					ParticleTile(3)
-					ParticleColor(1,1,1)
-					ParticleRadius(3)
-					ParticleAlpha(1)
-					ParticleGravity(0)
-					ParticleDrag(0)
-					ParticleEmissive(1)
-					ParticleRotation(0)
-					ParticleCollide(0)
-					SpawnParticle(gspawn,Vec(0,0,0),0.8)
-					--PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
-				end
-			end
-		end
-	end
---Limitless particle shit
-	
-	if EntireAssFuckingCutsceneTypeAnimationTimer > 0 and honored == false then
-		--if performance == true then
-			EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1
-		--end
-		local middle = Vec(0,1000,0)
-		local borigin = VecAdd(origin,Vec(0,-0.5,0))
-		local mid2 = VecAdd(borigin,VecScale(Vec(dir[1],0,dir[3]),-3))
-		if bich > 350 then
-			if bich < 490 and bich > 470 then
-				
-				for i = 1,5,1 do
-					local gdis = VecScale(VecNormalize(RVec()),rand(1,1.2))
-					local gspawn = VecAdd(VecAdd(VecAdd(mid2,VecScale(adderall,-1))),gdis)
-					ParticleType("plain")
-					ParticleTile(2)
-					ParticleColor(1,1,1,0.8,0.8,1)
-					ParticleRadius(0.1,0.2)
-					ParticleAlpha(0,1)
-					ParticleGravity(0)
-					ParticleDrag(0)
-					ParticleEmissive(10)
-					ParticleRotation(rand(-10,10))
-					ParticleCollide(0)
-					local rotata = TransformToParentVec(cam, Vec(1,0,0))
-					local look = Transform(VecAdd(VecAdd(mid2,VecScale(adderall,-1))),QuatLookAt(VecAdd(VecAdd(mid2,VecScale(adderall,-1))),gspawn))
-					local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),1)))
-					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),0),VecScale(gdis,0)),VecScale(VecScale(spidir,2),1)),0.6)
-				end
-			end
-			if bich < 450 and bich > 420 then
-				for i = 1,5,1 do
-					local gdis = VecScale(VecNormalize(RVec()),rand(1,1.2))
-					local gspawn = VecAdd(VecAdd(VecAdd(mid2,VecScale(adderall,1))),gdis)
-					ParticleType("plain")
-					ParticleTile(2)
-					ParticleColor(1,1,1,1,0.8,0.8)
-					ParticleRadius(0.1,0.2)
-					ParticleAlpha(0,1)
-					ParticleGravity(0)
-					ParticleDrag(0)
-					ParticleEmissive(10)
-					ParticleRotation(rand(-10,10))
-					ParticleCollide(0)
-					local rotata = TransformToParentVec(cam, Vec(1,0,0))
-					local look = Transform(VecAdd(VecAdd(mid2,VecScale(adderall,1))),QuatLookAt(VecAdd(VecAdd(mid2,VecScale(adderall,1))),gspawn))
-					local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),1)))
-					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),0),VecScale(gdis,0)),VecScale(VecScale(spidir,2),1)),0.6)
-				end
-			end
-			if bich > 400 then
-				if bich <= 400 then
-					for i = 1, 0 do
-						local gdis = VecScale(RVec(),1.2)
-						local gspawn = VecAdd(VecAdd(mid2,VecScale(adderall,1)),gdis)
-						ParticleType("plain")
-						ParticleTile(5)
-						ParticleColor(1,0.5,0.5)
-						ParticleRadius(0.3)
-						ParticleAlpha(0.2,0.5)
-						ParticleGravity(0)
-						ParticleDrag(0)
-						ParticleEmissive(1)
-						ParticleCollide(1)
-					
-						SpawnParticle(gspawn,VecScale(adderall,1),1)
-					end
-				end
-			end
-		end
-		if bich <= 350 and bich > 200 then
-			local add2 = VecScale(Vec(-1,0,0),bich/1000)
-			for i = 1,30,1 do
-				local gdis = VecScale(VecNormalize(RVec()),rand(0.05,1))
-				local gspawn = VecAdd(middle,gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				local b = VecLength(VecSub(gdis,VecAdd(add2,VecNormalize(add2))))
-				local r = VecLength(VecSub(gdis,VecAdd(VecScale(add2,-1),VecNormalize(VecScale(add2,-1)))))
-				--DebugPrint(b)
-				ParticleColor(0,0,1)
-				ParticleRadius(0.1)
-				ParticleAlpha(1,0.2)
-				ParticleGravity(0)
-				ParticleDrag(0.2)
-				ParticleEmissive(1)
-				ParticleRotation(0)
-				ParticleCollide(0)
-				local look = Transform(middle,QuatLookAt(middle,gspawn))
-				local spidir = TransformToParentVec(look, Vec(1,0,0))
-				if VecLength(VecSub(gspawn,VecAdd(add2,middle))) < 0.5 and VecLength(VecSub(gspawn,VecAdd(VecScale(add2,-1),middle))) < 0.5 then
-					SpawnParticle(gspawn,VecAdd(VecScale(gdis,0),VecScale(VecScale(spidir,1/10/VecLength(gdis)),3/3)),0.5)
-				else
-					i = i - 1
-				end
-			end
-			for i = 1,30,1 do
-				local gdis = VecScale(VecNormalize(RVec()),rand(0.05,1))
-				local gspawn = VecAdd(middle,gdis)
-				ParticleType("plain")
-				ParticleTile(5)
-				local b = VecLength(VecSub(gdis,VecAdd(add2,VecNormalize(add2))))
-				local r = VecLength(VecSub(gdis,VecAdd(VecScale(add2,-1),VecNormalize(VecScale(add2,-1)))))
-				--DebugPrint(b)
-				ParticleColor(1,0,0)
-				ParticleRadius(0.1)
-				ParticleAlpha(1,0.2)
-				ParticleGravity(0)
-				ParticleDrag(0.2)
-				ParticleEmissive(1)
-				ParticleRotation(0)
-				ParticleCollide(0)
-				local look = Transform(middle,QuatLookAt(middle,gspawn))
-				local spidir = TransformToParentVec(look, Vec(1,0,0))
-				if VecLength(VecSub(gspawn,VecAdd(add2,middle))) < 0.5 and VecLength(VecSub(gspawn,VecAdd(VecScale(add2,-1),middle))) < 0.5 then
-					SpawnParticle(gspawn,VecAdd(VecScale(gdis,0),VecScale(VecScale(spidir,1/10/VecLength(gdis)),3/3)),0.5)
-				else
-					i = i-1
-				end
-			end
-		end
-		if bich < 200 and bich > 190 then
-			for i = 1,6,1 do
-				local gdis = VecScale(VecNormalize(RVec()),1)
-				local gspawn = VecAdd(middle,Vec(0,1,0))
-				ParticleType("plain")
-				ParticleTile(2)
-				ParticleColor(0.6,0.2,1)
-				ParticleRadius(2)
-				ParticleAlpha(1)
-				ParticleGravity(0)
-				ParticleDrag(0)
-				ParticleEmissive(2)
-				ParticleRotation(0)
-				ParticleCollide(0)
-				SpawnParticle(gspawn,VecScale(VecNormalize(VecAdd(RVec(),Vec(0,1,0))),10),5)
-				if bich == 199 then
-					SpawnParticle(gspawn,VecScale(VecNormalize(VecAdd(Vec(0,0,0),Vec(0,1,0))),10),5)
-				end
-			end
-		end
-	end
-end
-
-
-function draw(dt)
-	if GetString("game.player.tool") == "INFINITY" then
-		UiPush()
-			UiAlign("left")
-			UiWordWrap(5000000000000000) --5 million bajilion
-			UiFont("arial.ttf", 15)
-			UiTranslate(1700, 900)
-			if LockToggle then
-				UiColor(1,1,1)
-				UiText("Lock is: on")
-			else
-				UiColor(0,0,0)
-				UiText("Lock is: off")
-			end
-			UiColor(1,1,1)
-			UiTranslate(0, 20)
-				if wheelless then
-					UiText("Scrollwheelless: " .. tostring(math.floor(scrollPos)) .. "\n"
-					)
-				else
-					UiText("Scrollwheel: " .. tostring(math.floor(scrollPos)) .. "\n"
-					)
-				end
-			UiTranslate(0, 20)
-			if InfToggle then
-				UiColor(1,1,1)
-				UiText("Infinity is: on")
-			else
-				UiColor(0,0,0)
-				UiText("Infinity is: off")
-			end
-			UiTranslate(0, 20)
-			if FlyToggle then
-				UiColor(1,1,1)
-				UiText("Flight is: on")
-			else
-				UiColor(0,0,0)
-				UiText("Flight is: off")
-			end
-			UiTranslate(0, 20)
-			if telek then
-				UiColor(1,1,1)
-				UiText("Alt use is: on")
-			else
-				UiColor(0,0,0)
-				UiText("Alt use is: off")
-			end
-			UiTranslate(0, 20)
-			UiColor(0.2,0.6,1)
-			if SBlue then
-				UiText("Blue: " .. tostring(math.floor(BluStr)) .. "\n"
-				)
-			else
-				UiText("Blue: no")
-			end
-			UiTranslate(1, 20)
-			UiColor(1,0.2,0.2)
-			if SRed then
-				UiText("Red: " .. tostring(math.floor(RedStr)) .. "\n"
-				)
-			else
-				UiText("Red: no")
-			end
-			UiTranslate(0, 20)
-			UiColor(1,0.4,1)
-			if PNuke then
-				UiText("Purple: " .. tostring(math.floor(Str)) .. "\n"
-				)
-			else
-				UiText("Purple: no")
-			end
-
-			UiTranslate(0, 20)
-			local bitchasscolorrainbowheadassthingamabob = Vec(math.sin(Frames/10)+0.5,math.cos(Frames/10)+0.5,math.tan(Frames/10)+0.5) --worst fucking color generator ever
-			UiColor(bitchasscolorrainbowheadassthingamabob[1],bitchasscolorrainbowheadassthingamabob[2],bitchasscolorrainbowheadassthingamabob[3])
-			if DomainToggle then
-				UiText("DOMAIN EXPANSION: INFINITE VOID")
-			end
-		UiPop()
-	end
-end
-
-
 function rand(min,max)
 	return math.random(0,1000)/1000*(max-min)+min
 end
@@ -3249,7 +13,6 @@
 	r = VecNormalize(Vec(rand(-1,1),rand(-1,1),rand(-1,1)))
 	return VecNormalize(r)
 end
-
 
 function Gravity(Bpos,Str,leng,req1,req2)
 	if req1 ~= 0 then
@@ -3398,26 +161,26 @@
 			end 
 		end
 	end
-end	
+end
 
 function PlayerGravity(origin,pvel,BlueTrack,BluStr,dir, scrollPos)
 	--sigma player gravity flying n shit
-	--SetPlayerVelocity(VecAdd(pvel,Vec(0,0.15*time,0)))
-	SetPlayerVelocity(VecAdd(pvel,VecScale(GetGravity(),-0.016*time)))
+	--SetPlayerVelocity(playerId, VecAdd(pvel,Vec(0,0.15*time,0)))
+	SetPlayerVelocity(playerId, VecAdd(pvel,VecScale(GetGravity(),-0.016*time)))
 	if SBlue == true and InputDown("space") then
 		if PNuke == false then
 			local PBdir = VecNormalize(VecSub(origin,BlueTrack))
 			local PBdist = VecLength(VecSub(origin,BlueTrack))
 			--DebugPrint((-BluStr*0.5)/(PBdist+1))
 			--DebugPrint(PBdist+1)
-			SetPlayerVelocity(VecAdd(pvel,VecScale(PBdir,((-BluStr*0.5)-1)/(PBdist+1))))
+			SetPlayerVelocity(playerId, VecAdd(pvel,VecScale(PBdir,((-BluStr*0.5)-1)/(PBdist+1))))
 		end
 	end
 	
 	--regular flight
 		
 		if InputDown(GetString("savegame.mod.inf.time")) then
-			SetPlayerVelocity(Vec(0,0.016,0))
+			SetPlayerVelocity(playerId, Vec(0,0.016,0))
 			--SetCameraFov(100)
 			--SetPlayerCameraTransform(Vec(0,0,0))
 		end
@@ -3425,28 +188,28 @@
 		local mdir = Vec(0,0,0)
 		if InputDown("up") then
 			mdir = VecAdd(mdir,VecScale(dir,1))
-			SetPlayerVelocity(VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
+			SetPlayerVelocity(playerId, VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
 		end
 		if InputDown("down") then
 			mdir = VecAdd(mdir,VecScale(dir,-1))
-			SetPlayerVelocity(VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
+			SetPlayerVelocity(playerId, VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
 		end
 		
 		if InputDown("left") then
 			mdir = VecAdd(mdir,VecScale(rotata,-1))
-			SetPlayerVelocity(VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
+			SetPlayerVelocity(playerId, VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
 		end
 		if InputDown("right") then
 			mdir = VecAdd(mdir,VecScale(rotata,1))
-			SetPlayerVelocity(VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
+			SetPlayerVelocity(playerId, VecAdd(VecAdd(pvel,VecScale(mdir,scrollPos/15)),VecScale(VecScale(GetGravity(),1),-0.016*time)))
 		end
 		if InfToggle and (InputDown("jump") or InputDown("space")) then
-			SetPlayerVelocity(Vec(0,0.18,0))
+			SetPlayerVelocity(playerId, Vec(0,0.18,0))
 			--SetCameraFov(100)
 			--SetPlayerCameraTransform(Vec(0,0,0))
 		end
 end
---not used anymore, it kinda sucks now compared to the sprites
+
 function VisChain(endP,fo,r,g,b,r2,g2,b2,siz1,siz2,FFlash,Str, Pdir, Ptransform,DL,CDir)
 	if DL == false then
 		Ppos = VecCopy(Ptransform.pos)
@@ -3489,7 +252,7 @@
 			ParticleRadius(Str*0.05*siz1,0)
 				SpawnParticle(p, Vec(0,0,0), 0.1)
 			ParticleColor(r2,g2,b2)
-			if siz2 > 0 then
+			if siz2 ~= 0 then
 				ParticleRadius(Str*0.15*siz2,0.1)
 				SpawnParticle(pr, Vec(0,0,0), 0.1)
 			end
@@ -3503,4 +266,3151 @@
 			VisChain(endPoint,fo,r,g,b,r2,g2,b2,siz1,siz2,FFlash,Str-fo,Pdir, Ptransform,DL,CDir)
 		end
 	end
-end+end
+
+function server.init()
+    RegisterTool("INFINITY", "Limitless technique", "untitled.vox")
+    SetBool("game.tool.INFINITY.enabled", true, true)
+    SetInt("game.tool.CLEAVER.ammo", 5000*500, true) --used to be shrine technique, made a copy and i'm also working on that >:) (it's laggy as fuck tho, even on my end. maybe check it out too? this one's way more optimized tho)
+    Feet = 0
+    cam = 0
+    Frames = 0
+    performance = true --actually the opposite, performance mode is now the worse one for performance, turning off makes it sprites, which is better for performance. press 8 in-game btw
+    BlueTrack = Vec(0,0,0)
+    BlueZone = Vec(0,0,0)
+    RedTrack = Vec(0,0,0)
+    RedTrackD = Vec(0,0,0) --Red track DICK, totally not direction
+    RVel = Vec(0,0,0)
+    BVel = Vec(0,0,0)
+    MVel = Vec(0,0,0) --merge velocity (unused)
+    particleTimer = 0
+    dcirc = {} --DICK circles, not direction at all
+    ctime = {} --COCK time, not circle at all
+    SBlue = false --can't make a dick and balls joke outta this one, sorry folks
+    smbt = {}
+    smbv = {}
+    smbtot = 0
+    ShotBlue = 0
+    ShotBlueTime = 0
+    BluesMerge = false
+    BTarget = 0
+    BTPos = Vec(0,0,0)
+    BROTIME = 0
+    SRed = false
+    PNuke = false --purple, not the nuke
+    NukeTime = 0 --this is the nuke timer, yes this is the nuke
+    NRelease = false --i have no fucking clue what this is
+    MTimer = 200 --red and blue merge timer, don't want it to be instant, lame as hell
+    --punch init
+    Str = 0.1 --strength of the technique and everything --POURPLE
+    BluStr = 0.1 --BLUE strength
+    RedStr = 0.1 --red string cheese
+    NTimer = 0 --NUKE timer
+    InfToggle = false
+    FlyToggle = false
+    --NTimer = 0
+    NMove = false
+    --void statistics (possibly)
+    DomActivate = 0
+    DomainToggle = false
+    DomainPos = 0
+    DPR = 0 --domain place rot
+    DPP = 0 --domain place pos
+    DPD = 0 --drection
+    BHolePos = 0 --Butthole position
+    DsTimer = 0 --Dick suck timer
+    --pvoid = CreateShape(0,0,0)
+    void = 0
+    voidb = 0
+    ovoid = 0
+    ovoidb = 0
+    DomainBreak = false
+    --shade = CreateShape(0,0,0)
+    skybox = GetEnvironmentProperty("skybox")
+    sun = GetEnvironmentProperty("sunBrightness")
+    skybright = GetEnvironmentProperty("skyboxbrightness")
+    tintr,tintg,tintb = GetEnvironmentProperty("skyboxtint")
+    fogr,fogg,fogb = GetEnvironmentProperty("fogColor")
+    fogp1,fogp2,fogp3,fogp4 = GetEnvironmentProperty("fogParams")
+    amb = GetEnvironmentProperty("ambience")
+    rain = GetEnvironmentProperty("rain")
+    sat = GetPostProcessingProperty("saturation")
+    cb1,cb2,cb3 = GetPostProcessingProperty("colorbalance")
+    bright = GetPostProcessingProperty("brightness")
+    gamma = GetPostProcessingProperty("gamma")
+    freq = 0
+    --other things needed to work correctly
+    scrollPos = 0
+    Burnout = 0
+    LockToggle = false
+    HP = 1 --HOT PUSSY
+    RTime = 0
+    time = 1
+    pullBodies = QueryAabbBodies(0,0)
+    telek = false
+    SBlueStrScaleThingy = 0
+    tpStr = 0
+    tpvel = 0
+    --DebugPrint("This is the infinity mod creator, Idk how to make a ui so I put everything in DebugPrint")
+    --DebugPrint("Controls are in the Mod description thing, not typing all that out again")
+    --all sounds just already in teardown
+    BlueSound = LoadLoop("tornado.ogg")
+    RedSound = LoadLoop("fire-out-loop.ogg")
+    InfExisting = LoadLoop("float-loop.ogg")
+    Extra = LoadLoop("ambient.ogg")
+    --made some of these images
+    circle = LoadSprite("circle.png")
+    ripple = LoadSprite("ripple.png")
+    ripple2 = LoadSprite("ripple2.png")
+    ripple3 = LoadSprite("ripple3copyright.png")
+    star = LoadSprite("star.png")
+    --not this one
+    earth = LoadSprite("earth.png") --ripped straight from nasa
+    EntireAssFuckingCutsceneTypeAnimationTimer = 0 --also known as bich
+    RSplodeTime = 0
+    BSplodeTime = 0
+    pshart = false
+    ReleaseTheBeast = 0 --why did i call it that?
+    BDir = Vec(0,0,0)
+    honoredpos = 0
+    honoredrotata = 0
+    honored = false
+    PRtoggle = false
+    NoMoreRed = false --make sure you don't keep spawning them by holding grab
+    wheelless = false
+    --customizable shit, options
+    if not HasKey("savegame.mod.inf.wheelless") then
+    	SetBool("savegame.mod.inf.wheelless", false, true)
+    else
+    	if GetBool("savegame.mod.inf.wheelless") == true then
+    		wheelless = true
+    	end
+    end
+    if not HasKey("savegame.mod.inf.performancemode") then --remember, performance stat is the one WITH particles, i switched it in ONLY THE OPTIONS THING
+    	SetBool("savegame.mod.inf.performancemode", true, true)
+    	performance = true
+    end
+    if GetBool("savegame.mod.inf.performancemode") == false then
+    	performance = false
+    end
+    controller = false
+    --keybinds, making sure there are some
+    if not HasKey("savegame.mod.inf.controller") then
+    	SetBool("savegame.mod.inf.controller",false, true)
+    end
+    if GetBool("savegame.mod.inf.controller") then  --IF CONTROLLER OPTIONS THING IS GREEN/YES
+    	--CONTROLLER KEYBINDS
+    	controller = true
+    	SetString("savegame.mod.inf.infkey","interact", true)
+
+    	SetString("savegame.mod.inf.sadd","z", true)
+
+    	SetString("savegame.mod.inf.ssub","x", true)
+
+    	SetString("savegame.mod.inf.time","scroll_down", true)
+
+    	SetString("savegame.mod.inf.warp","zoom", true)
+
+    	SetString("savegame.mod.inf.cutsc","flashlight", true)
+
+    	SetString("savegame.mod.inf.tel","tool_group_prev", true)
+
+    	SetString("savegame.mod.inf.dom","crouch", true)
+
+    	SetString("savegame.mod.inf.ptrack","n", true)
+
+    	SetString("savegame.mod.inf.flykey","jump", true)
+
+    	SetString("savegame.mod.inf.lock","tool_group_next", true)
+
+    	SetString("savegame.mod.inf.grab","scroll_up", true)
+    else 
+    	--NORMAL KEYBOARD KEYBINDS
+    	if not HasKey("savegame.mod.inf.infkey") then
+    		SetString("savegame.mod.inf.infkey","e", true)
+    	end
+    	if not HasKey("savegame.mod.inf.sadd") then
+    		SetString("savegame.mod.inf.sadd","z", true)
+    	end
+    	if not HasKey("savegame.mod.inf.ssub") then
+    		SetString("savegame.mod.inf.ssub","x", true)
+    	end
+    	if not HasKey("savegame.mod.inf.time") then
+    		SetString("savegame.mod.inf.time","r", true)
+    	end
+    	if not HasKey("savegame.mod.inf.warp") then
+    		SetString("savegame.mod.inf.warp","t", true)
+    	end
+    	if not HasKey("savegame.mod.inf.cutsc") then
+    		SetString("savegame.mod.inf.cutsc","v", true)
+    	end
+    	if not HasKey("savegame.mod.inf.tel") then
+    		SetString("savegame.mod.inf.tel","b", true)
+    	end
+    	if not HasKey("savegame.mod.inf.dom") then
+    		SetString("savegame.mod.inf.dom","m", true)
+    	end
+    	if not HasKey("savegame.mod.inf.ptrack") then
+    		SetString("savegame.mod.inf.ptrack","n", true)
+    	end
+    	if not HasKey("savegame.mod.inf.flykey") then
+    		SetString("savegame.mod.inf.flykey","alt", true)
+    	end
+    	if not HasKey("savegame.mod.inf.lock") then
+    		SetString("savegame.mod.inf.lock","shift", true)
+    	end
+    	if not HasKey("savegame.mod.inf.grab") then
+    		SetString("savegame.mod.inf.grab","q", true)
+    	end
+    	--reset keybinds after controller switched back to false
+    	if GetString("savegame.mod.inf.infkey") == "interact" then
+    		SetString("savegame.mod.inf.infkey","e", true)
+    		SetString("savegame.mod.inf.sadd","z", true)
+    		SetString("savegame.mod.inf.ssub","x", true)
+    		SetString("savegame.mod.inf.time","r", true)
+    		SetString("savegame.mod.inf.warp","t", true)
+    		SetString("savegame.mod.inf.cutsc","v", true)
+    		SetString("savegame.mod.inf.tel","b", true)
+    		SetString("savegame.mod.inf.dom","m", true)
+    		SetString("savegame.mod.inf.ptrack","n", true)
+    		SetString("savegame.mod.inf.flykey","alt", true)
+    		SetString("savegame.mod.inf.lock","shift", true)
+    		SetString("savegame.mod.inf.grab","q", true)
+    	end
+    end
+end
+
+function server.tick(dt)
+    	Frames = Frames + 1
+    	--DebugPrint(dt*100)
+    	--time = RTime
+    	RTime = dt*100
+    	if Frames == 10000 then
+    		Frames = 0 --frames, unlimited frames, but no frames
+    	end
+    	UScrollPos = scrollPos
+    	--DebugPrint(scrollPos)
+    	if Burnout ~= 0 then
+    		Burnout = Burnout - 1
+    	end
+    	Feet = GetPlayerTransform(playerId, true)
+    	cam = GetCameraTransform(true)
+    	--DebugPrint(PlayerHeight)
+    	pvel = GetPlayerVelocity(playerId)
+    	if GetBool("game.thirdperson") == false then
+    		origin = cam.pos
+    		dir = TransformToParentVec(cam,Vec(0,0,-1))
+    	else
+    		origin = VecAdd(Feet.pos, Vec(0,1.7,0))
+    		dir = TransformToParentVec(Feet,Vec(0,0,-1))
+    	end
+    	if tpStr > 1 then
+    		--tpStr = tpStr - 1
+    		if time == 1 then
+    			--SetPlayerVelocity(playerId, VecAdd(pvel,VecScale(dir,scrollPos/RTime)))
+    			--SetPlayerTransform(playerId, Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot),true)
+    			SetCameraFov((-tpStr*10)+180)
+    		else
+    			SetPlayerTransformWithPitch(Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot))
+    			SetCameraFov((-tpStr*10)+180)
+    			tpStr = tpStr - 1
+    		end
+    	else
+    		if tpStr ~= 0 then
+    			--tpStr = 0
+    		end
+    	end
+    	if tpStr == 1 then
+    		SetCameraFov(360)
+    		--SetPlayerVelocity(playerId, VecScale(dir,VecLength(tpvel)))
+    		tpStr = 0
+    	end
+    --REQUIRES LIMITLESS TECHNIQUE EQUIPPED
+    --DOES NOT REQUIRE LIMITLESS TECHNIQUE EQUIPPED
+    	--infinite void (with rage so sigma i feel so sigma while listening to this song i'm trynna make this noticable so i can come back later thank you byeeeeee)
+    		--DebugCross(DomainPos,1,0,0)
+    	if DomActivate == 1 then
+    		DomActivate = 0
+    		if DomainToggle == false then
+    			DomainToggle = true
+    		--domain stuff you can walk on/break
+    		--inside
+    			DomainPos = VecAdd(VecAdd(DPP,Vec(0,10000,0)),Vec(0,0,0)) --change Vec(0,0,0) to offset later
+    			local ins = Spawn("inside.xml", Transform(Vec(0,10000,0),QuatEuler(0,0,0)))
+    			voidb = ins[1]
+    			--DebugPrint(ins)
+    			void = ins[2]
+    		--outside
+    			local out = Spawn("outside.xml", Transform(Vec(0,1000000,0),QuatEuler(0,0,0)))
+    			ovoidb = out[1]
+    			--DebugPrint(out)
+    			ovoid = out[2]
+
+    			local dbodies = QueryAabbBodies(VecAdd(DPP,Vec(-8,-0.5,-8)),VecAdd(DPP,Vec(8,8,8)))
+    			for i = 1, #dbodies do
+    				local dbody = dbodies[i]
+    				if IsBodyDynamic(dbody) then
+    					local jbodies = GetJointedBodies(dbody)
+    					for j = 1,#jbodies do
+    						local jbody = jbodies[j]
+    						local add = true
+    						for k = 1, #dbodies do
+    							if jbody == dbodies[k] then
+    								add = false
+    							end
+    						end
+    						if add then
+    							dbodies[#dbodies+1] = jbody
+    						end
+    					end
+    				end
+    			end
+    			for i = 1, #dbodies do
+    				local dbody = dbodies[i]
+    				if IsBodyDynamic(dbody) then
+    					dtrans = GetBodyTransform(dbody)
+    					--RemoveTag(dbody, "state.id","avoid")
+    					SetBodyTransform(dbody,Transform(VecAdd(dtrans.pos,Vec(0,10000,0)),dtrans.rot))
+    				end
+    			end
+    			SetPlayerTransform(playerId, Transform(VecAdd(Feet.pos,Vec(0,10000,0)),Feet.rot))
+    			Feet = Transform(VecAdd(Feet.pos,Vec(0,10000,0)),Feet.rot)
+    			SetEnvironmentProperty("skybox", nil)
+    			SetEnvironmentProperty("skyboxbrightness", 0)
+    			SetEnvironmentProperty("skyboxtint", 0,0,0)
+    			SetEnvironmentProperty("sunBrightness",0)
+    			SetEnvironmentProperty("fogColor",0,0,0)
+    			SetEnvironmentProperty("fogParams",0,0,0,0)
+    			SetEnvironmentProperty("ambience",nil)
+    			SetEnvironmentProperty("rain",0)
+
+    			SetPostProcessingProperty("saturation", 1)
+    			SetPostProcessingProperty("colorbalance", 1,1,1)
+    			SetPostProcessingProperty("brightness",0.8)
+    			SetPostProcessingProperty("gamma",1)
+    			DsTimer = 1
+    			--local gdir = VecNormalize(VecAdd(RVec(),Vec(0,1,0)))
+
+    			--local gscale = rand(50,100)
+    			--BHolePos = VecAdd(DomainPos,VecScale(gdir,30))
+    			BHolePos = VecAdd(DomainPos,Vec(0,10,-120))
+    		end
+    	end
+    --q
+    	--quick pull thingy
+    	--Red existing
+    	if PNuke == true then
+    		SRed = false
+    		RedStr = 0.1
+    	end
+    	--Blue existing
+    	if (not SBlue or (not telek and not BluesMerge)) and #smbt ~= 0 then
+    		for j = 1, #smbt, 1 do
+    			table.remove(smbt,j)
+    			table.remove(smbv,j)
+    		end
+    	end
+    	--[[
+    	]]
+    --Purple
+    	if time < 1 then
+    		if InfToggle == true then
+    			if GetPlayerHealth(playerId) > HP then
+    				HP = GetPlayerHealth(playerId)
+    			end
+    			SetPlayerHealth(playerId, HP)
+    			SetPlayerParam("GodMode",true)
+    		else
+    			SetPlayerParam("GodMode",false)
+    		end
+    		if GetString("game.player.tool") == "INFINITY" then
+    			--if InputDown(GetString("savegame.mod.inf.flykey")) then
+    			if FlyToggle then
+    				PlayerGravity(origin,pvel,BlueTrack,Str,dir,scrollPos)
+    			end
+    		end
+    	end
+    --WHOLE ASS FUCKING CUTSCENE BIIIITCH
+    --2nd animation
+end
+
+function server.update(dt)
+    		--Blue
+    		--purple
+    	--infinity stuff
+    	if InfToggle then
+    		--MakeHole(origin,rand(-50,Str),rand(-100,Str/2),rand(-100,Str/3))
+    		Infinity(origin,5,pvel,true,false,false,false)
+    		Infinity(Feet.pos,5,pvel,true,true,false,false)
+    		if GetPlayerHealth(playerId) > HP then
+    			HP = GetPlayerHealth(playerId)
+    		end
+    		SetPlayerHealth(playerId, HP)
+    		SetPlayerParam("GodMode",true)
+    	else
+    		SetPlayerParam("GodMode",false)
+    	end
+    --warp
+    	if tpStr > 1 then
+
+    		if time == 1 then
+    			SetPlayerVelocity(playerId, VecAdd(pvel,VecScale(dir,scrollPos)))
+    			SetPlayerTransformWithPitch(Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot))
+    			tpStr = tpStr - 1
+    			--SetCameraFov((-tpStr*10)+180)
+    		else
+    			--SetPlayerTransform(playerId, Transform(VecAdd(Feet.pos,VecScale(dir,scrollPos/10)),Feet.rot),true)
+    			--SetCameraFov((-tpStr*10)+180)
+    		end
+    	else
+    		if tpStr ~= 0 then
+    			tpStr = 0
+    		end
+    	end
+    	if tpStr == 1 then
+    		--SetCameraFov(360)
+    		SetPlayerVelocity(playerId, VecScale(dir,VecLength(tpvel)))
+    		tpStr = 0
+    	end
+    	--if GetBool("savegame.mod.inf.toolless") == true or GetString("game.player.tool") == "INFINITY" then
+    		--if InputDown(GetString("savegame.mod.inf.flykey")) then
+    		if FlyToggle then
+    			PlayerGravity(origin,pvel,BlueTrack,BluStr,dir,scrollPos)
+    		end
+    	--end
+    --DOMAIN STUFF
+    	--domain itself
+    --Limitless particle shit
+end
+
+function client.init()
+    Water = LoadSound("splash-l1.ogg")
+    pShot = LoadSound("break-l4.ogg")
+    Boom = LoadSound("thunder2.ogg")
+    Brown = LoadSound("Brown.ogg")
+    Explode = LoadSound("m0.ogg")
+    suck = LoadSound("suck.ogg")
+end
+
+function client.tick(dt)
+    	if LockToggle == true then
+    		if controller then
+    			SetBool("game.player.caninteract", false, true)
+    			SetBool("game.player.cangrab", false, true)
+    			SetBool("game.player.flashlight.enabled", false, true)
+    			SetBool("game.player.toolselect",false, true)
+    			ReleasePlayerGrab()
+    		end
+    		if wheelless then
+    			scrollPos = 10
+    			if SBlue and SRed then
+    				scrollPos = (BluStr+RedStr)/4+1
+    			else
+    				if SBlue then
+    					scrollPos = (BluStr)/2+2
+    				end
+    				if SRed then
+    					scrollPos = (RedStr)/2+2
+    				end
+    			end
+    		else
+    			scrollPos = scrollPos + InputValue("mousewheel")
+    			--if InputDown(1) or scrollPos < 0 then
+    			if InputDown("mmb") then
+    				--if scrollPos <= 0.1 then
+    					scrollPos = 0
+    				--end
+    			end
+    		end
+    		if InputPressed(2) then --not sure what to change to
+    			Str = 0.1
+    		end
+    		--Strength scale
+    		if InputDown (GetString("savegame.mod.inf.sadd")) then
+    			Str = Str + 0.1*RTime
+    			if SBlue then
+    				BluStr = BluStr + 0.1*RTime
+    			end
+    			if SRed then
+    				RedStr = RedStr + 0.1*RTime
+    			end
+    			--DebugPrint(Str)
+    		end
+
+    		if InputDown (GetString("savegame.mod.inf.ssub")) then
+    			if Str > 0.1 then
+    				Str = Str - 0.1*RTime
+    			end
+    			if SBlue then
+    				BluStr = BluStr - 0.1*RTime
+    			end
+    			if SRed then
+    				RedStr = RedStr - 0.1*RTime
+    			end
+    			--DebugPrint(Str)
+    		end
+    		if Str < 0.1 then
+    			Str = 0.1
+    		end
+    		if BluStr < 0.1 then
+    			BluStr = 0.1
+    		end
+    		if RedStr < 0.1 then
+    			RedStr = 0.1
+    		end
+    	end
+    	if GetString("game.player.tool") == "INFINITY" then
+    		if InputPressed(GetString("savegame.mod.inf.cutsc")) and PNuke == false then
+    			if EntireAssFuckingCutsceneTypeAnimationTimer == 0 then 
+    				if InputDown(GetString("savegame.mod.inf.time")) then
+    					PNuke = false
+    					EntireAssFuckingCutsceneTypeAnimationTimer = 160
+    					local f1,f2,f3 = GetQuatEuler(Feet.rot)
+    					BVel = Vec(0,0,0)
+    					RVel = Vec(0,0,0)
+    					SetTimeScale(0.1)
+    					honoredpos = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
+    					--honoredrotata = TransformToParentVec(cam, Vec(1,0,0))
+    					honoredrotata = TransformToParentVec(cam, Vec(0,-1,0))
+    					honored = true
+    					SetBool("game.flashlight.enabled", false, true)
+    				else
+    					PNuke = false
+    					EntireAssFuckingCutsceneTypeAnimationTimer = 500
+    					local f1,f2,f3 = GetQuatEuler(Feet.rot)
+    					BVel = Vec(0,0,0)
+    					RVel = Vec(0,0,0)
+    					SetBool("game.flashlight.enabled", false, true)
+    				end
+    			end
+    		end
+    		if InputPressed(GetString("savegame.mod.inf.ptrack")) then
+    			if PRtoggle == true then
+    				PRtoggle = false
+    			else
+    				PRtoggle = true
+    			end
+    		end
+    		if InputPressed("8") then
+    			if performance == true then
+    				performance = false
+    			else
+    				performance = true
+    			end
+    		end
+
+    		--warp
+    		if InputPressed(GetString("savegame.mod.inf.warp")) then
+    			tpStr = 10
+    			tpvel = pvel
+    		end
+
+    		if InputDown(GetString("savegame.mod.inf.time")) then
+    			--SetValue("time",0.03,"easeout",0)
+    			if pshart == true then
+    				if performance == true and (pshart and honored == false) then
+    					time = 0.01
+    				else
+    					time = 0
+    				end
+    			else
+    				time = 0.02
+    			end
+    			SetTimeScale(time)
+    			--DebugPrint(pvel)
+    		end
+    		if not InputDown(GetString("savegame.mod.inf.time")) then
+    			SetValue("time",1)
+    			SetTimeScale(time)
+    		end
+    		if InputPressed(GetString("savegame.mod.inf.lock")) then
+    			if LockToggle == true then
+    				LockToggle = false
+    				--DebugPrint("Lock is off")
+    			else
+    				LockToggle = true
+    				--DebugPrint("Lock is on")
+    			end
+    		end
+
+    		if LockToggle == true then
+    			SetBool("game.input.locktool", true, true)
+    		end
+    		--infinity stuff
+    		if InputPressed(GetString("savegame.mod.inf.infkey")) then
+    			if InfToggle == true then
+    				InfToggle = false
+    			else
+    				HP = GetPlayerHealth(playerId)
+    				InfToggle = true
+    			end
+    		end
+    	end
+    	if GetString("game.player.tool") == "INFINITY" then
+    		if InputPressed("3") then
+    			Str = Str + 50
+    		end
+    		if InputPressed("9") then
+    			SetPlayerTransform(playerId, Transform(Vec(0,0,0),QuatEuler(0,0,0)))
+    		end
+    		--SetToolTransform(Transform(Vec(0.2,-0.1,-0.5),QuatEuler(0,0,0)), 0)
+    		if InputPressed(GetString("savegame.mod.inf.tel")) then
+    			if telek == true then
+    				telek = false
+    				BTarget = 0
+    				BVel = Vec(0,0,0)
+    				if InputDown(GetString("savegame.mod.inf.grab")) and #smbt ~= 0 then
+    					BluesMerge = true
+    					--BlueTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,(BluStr+4)/6+0.1))
+    					BlueTrack = smbt[1]
+    					BVel = smbv[1]
+    					table.remove(smbt,1)
+    					table.remove(smbv,1)
+    					BluStr = 5
+    					smbtot = #smbt
+    				else
+    					SBlue = false
+    					BluesMerge = false
+    				end
+    			else
+    				telek = true
+    				BluesMerge = false
+    				if InputDown(GetString("savegame.mod.inf.grab")) and #smbt ~= 0 then
+    					BluStr = BluStr + #smbt
+    				end
+    			end
+    		end
+    		--red
+    		if InputPressed("grab") and PNuke == false then
+    			if SRed == false and RSplodeTime <= 1 then
+    				SRed = true
+    				RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
+    				RVel = VecScale(pvel,0.018)
+    				RedStr = 0.1
+    			else
+    				if RSplodeTime <= 1 then
+    					RSplodeTime = 1.5
+    					SRed = false
+    					MakeHole(RedTrack,RedStr,RedStr,RedStr)
+    				end
+    			end
+    		end
+
+    		if (SRed == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0) and PNuke == false then
+    			--if InputDown("usetool") == false then
+    			--RSplodeTime = 0
+    			if Burnout == 0 then
+    				if PNuke == false then
+    					if InputDown("grab") then
+    						--if VecLength(VecSub(origin,RedTrack)) <= 2 then
+    							RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,5/6+0.1))
+    							RVel = VecScale(pvel,0.01)
+    						--end
+    					end
+    					if InputReleased("grab") then
+    						if PNuke == false and not telek then
+    							RVel = VecAdd(VecScale(pvel,0.01),VecScale(dir,scrollPos*0.05))
+    						end
+    						if telek then
+    							RSplodeTime = 1.4
+    						end
+    					end
+    				end
+    			end
+    		end
+    		--blue	
+    		if InputPressed("usetool") then
+    			if PNuke == false then
+    				if SBlue == false then
+    					BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
+    					BlueTrack = VecAdd(origin,dir)
+    				end
+    				BVel = VecScale(pvel,0.01)
+    			end
+    		end	
+    		if InputPressed("usetool") and PNuke == false then
+    		--and BSplodeTime <= 1
+    			if SBlue == false then
+    				SBlue = true
+    				BlueTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
+    				BVel = VecScale(pvel,0.01)
+    				BluStr = 0.1
+    			else
+    				BluStr = 0
+    				SBlue = false
+    				--end
+    			end
+    		end
+
+    		if (SBlue == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0) and PNuke == false then
+    			if Burnout == 0 then
+    				if PNuke == false then
+    					if InputDown("usetool") then
+    						--if VecLength(VecSub(origin,RedTrack)) <= 2 then
+    							BlueTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,(BluStr+4)/6+0.1))
+    							BVel = VecScale(pvel,0.01)
+    						--end
+    					end
+    					if InputReleased("usetool") then
+    						if PNuke == false then
+    							BVel = VecAdd(VecScale(pvel,0.01),VecScale(dir,scrollPos*0.05))
+    						end
+    					end
+    				end
+    			end
+    		end
+    		--infinite void (with rage so sigma i feel so sigma while listening to this song i'm trynna make this noticable so i can come back later thank you byeeeeee)
+    		--DebugCross(DomainPos,1,0,0)
+
+    	end
+    	if (InputPressed(GetString("savegame.mod.inf.dom")) and GetString("game.player.tool") == "INFINITY") or DomainBreak then
+    		if DomainToggle == true then
+    			--domain off/break
+    			DomainToggle = false
+    			--ClearShape(void)
+    			Delete(voidb)
+    			--DebugPrint(ovoid)
+    			--ClearShape(ovoid)
+    			Delete(ovoidb)
+    			DomainBreak = false
+    			for k = 1, 0 do --if wanted change the 0
+    				for i = -1,1,0.3 do
+    					for j = -1,1,0.3 do
+    						local GDir = QuatRotateVec(DPR,VecNormalize(Vec(i,j,0)))
+    						--local GDir = Vec(i,j,k)
+    						--local hit, dis, gp = QueryRaycast(origin,GDir,10)
+    						local what = ((rand(0,100))/10/math.pi)
+    						--DebugPrint(math.sin(what))
+    						local gspawn = VecAdd(VecAdd(DPP,VecScale(DPD,(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
+    						--local gspawn = VecAdd(VecAdd(Feet.pos,VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
+    						ParticleType("plain")
+    						ParticleTile(3)
+    						ParticleColor(1,1,1)
+    						ParticleRadius(3)
+    						ParticleAlpha(1)
+    						ParticleGravity(-1)
+    						ParticleDrag(0)
+    						ParticleEmissive(1)
+    						ParticleRotation(0)
+    						ParticleCollide(0)
+    						SpawnParticle(gspawn,VecScale(VecNormalize(GDir),10),0.8)
+    						--PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
+    					end
+    				end
+    			end
+    			SetEnvironmentProperty("skybox", skybox)
+    			SetEnvironmentProperty("skyboxbrightness", skybright)
+    			SetEnvironmentProperty("skyboxtint",tintr,tintg,tintb)
+    			SetEnvironmentProperty("sunBrightness",sun)
+    			SetEnvironmentProperty("fogColor",fogr,fogg,fogb)
+    			SetEnvironmentProperty("fogParams",fogp1,fogp2,fogp3,fogp4) 
+    			SetEnvironmentProperty("ambience",amb)
+    			SetEnvironmentProperty("rain",rain)
+
+    			SetPostProcessingProperty("saturation", sat)
+    			SetPostProcessingProperty("colorbalance",cb1,cb2,cb3)
+    			SetPostProcessingProperty("brightness",bright)
+    			SetPostProcessingProperty("gamma",gamma)
+    			local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-20,-50)),VecAdd(DomainPos,Vec(50,50,50)))
+    			for i = 1, #dbodies do
+    				local dbody = dbodies[i]
+    				if IsBodyDynamic(dbody) then
+    					jbodies = GetJointedBodies(dbody)
+    					for j = 1,#jbodies do
+    						local jbody = jbodies[j]
+    						local add = true
+    						for k = 1, #dbodies do
+    							if jbody == dbodies[k] then
+    								add = false
+    							end
+    						end
+    						if add then
+    							dbodies[#dbodies+1] = jbody
+    						end
+    					end
+    				end
+    			end
+    			for i = 1, #dbodies do
+    				local dbody = dbodies[i]
+    				if IsBodyDynamic(dbody) then
+    					dtrans = GetBodyTransform(dbody)
+    					--RemoveTag(dbody, "state.id","avoid")
+    					SetBodyTransform(dbody,Transform(VecAdd(dtrans.pos,Vec(0,-9999.5,0)),dtrans.rot))
+    				end
+    			end
+    			if VecLength(VecSub(Feet.pos,DomainPos)) < 100 then
+    				SetPlayerTransform(playerId, Transform(VecAdd(Feet.pos,Vec(0,-9999.5,0)),Feet.rot))
+    			end
+    			SetPlayerParam("GodMode",false)
+    			PlaySound(pShot,DomainPos,1,true,1)
+    			PlaySound(pShot,DPP,10,true,0.8)
+    		else
+    			DomActivate = 100
+    			DPP = Feet.pos
+    			DPR = Feet.rot
+    			DPD = dir
+    			--PlaySound()
+    		end
+    	end
+    	if DomainToggle == true then
+    		if GetShapeBody(ovoid) ~= ovoidb then
+    			DomainBreak = true
+    		end
+    		if GetShapeBody(void) ~= voidb then
+    			DomainBreak = true
+    		end
+    		if VecLength(VecSub(Feet.pos,DomainPos)) > 10 and VecLength(VecSub(Feet.pos,DomainPos)) < 100 then --and DsTimer == 0
+    			SetPlayerTransform(playerId, Transform(DomainPos,Feet.rot),true)
+    			SetPlayerVelocity(playerId, VecScale(VecNormalize(VecAdd(RVec(),Vec(0,2,0))),20))
+    			DomainBreak = true
+    		end
+    		--DebugPrint(GetShapeBody(ovoid) ~= ovoidb)
+
+    		if DsTimer >= 1 then 
+    			for i = 1,DsTimer/200*30,1 do
+    				for i = 1,DsTimer/200*5,1 do
+    					local linepos = VecAdd(DomainPos,VecScale(VecNormalize(Vec(rand(-10,10),rand(-10,10),0)),rand(5,20)))
+    					local ldir = Vec(0,0,-1)
+    					lr = rand(0.6,1)
+    					lg = rand(0.2,0.6)
+    					lb = rand(0.6,1)
+
+    					DrawLine(linepos,VecAdd(linepos,VecScale(ldir,50)),lr,lg,lb)
+    					DrawLine(linepos,VecAdd(linepos,VecScale(VecScale(ldir,50),-1)),lr,lg,lb)
+    					for j = 0,50,2 do
+    						PointLight(VecAdd(linepos,VecScale(ldir,j)),lr-0.3,lg-0.3,lb-0.3,1)
+    					end
+    					for j = 0,50,2 do
+    						PointLight(VecAdd(linepos,VecScale(ldir,-j)),lr-0.3,lg-0.3,lb-0.3,1)
+    					end
+    				end
+    			end
+    			SetCameraFov((VecLength(pvel))/20+100+DsTimer)
+    			PlayLoop(BlueSound,DomainPos,1,false,0.2+(DsTimer/50))
+    			--PlayLoop(InfExisting,DomainPos,2,false,0.2+(DsTimer/30))
+    			--PlayLoop(RedSound,DomainPos,1,false,0.1+(DsTimer/60))
+    			PlayLoop(Extra,DomainPos,0.1,false,0.2+(DsTimer/50))
+    			if DsTimer == 200 then
+    				PlaySound(Boom,DomainPos,2,false,1)
+    			end
+    		end
+    		if DsTimer == 0 then
+    			--SetEnvironmentProperty("fogColor",0.1,0.2,0.3)
+    			rotarted = QuatLookAt(cam.pos,BHolePos)
+    			DrawSprite(Circle,Transform(DomainPos,QuatLookAt(Vec(0,0,0),Vec(0,-1,0))),20,20,1,1,1,0.2,true,true)
+
+    			DrawSprite(circle, Transform(BHolePos,rotarted), 30, 30, 0, 0, 0, 1,true,false)
+    			DrawSprite(ripple, Transform(BHolePos,rotarted), 32, 32, 1, 1, 1, 1,true,true)
+    			for i = 0, 100 do
+    				DrawSprite(circle, Transform(BHolePos,QuatLookAt(Vec(0,0,0),VecNormalize(RVec()))), 30, 30, 0, 0, 0, 1,true,false)
+    			end
+    		end
+    		local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-50,-50)),VecAdd(DomainPos,Vec(50,-8,50)))
+    		for i = 1, #dbodies do
+    			local dbody = dbodies[i]
+    			if IsBodyDynamic(dbody) then
+    				local jbodies = GetJointedBodies(dbody)
+    				for j = 1,#jbodies do
+    					local jbody = jbodies[j]
+    					local add = true
+    					for k = 1, #dbodies do
+    						if jbody == dbodies[k] then
+    							add = false
+    						end
+    					end
+    					if add then
+    						dbodies[#dbodies+1] = jbody
+    					end
+    				end
+    			end
+    		end
+    		for i = 1, #dbodies do
+    			local dbody = dbodies[i]
+    			if IsBodyDynamic(dbody) then
+    				dtrans = GetBodyTransform(dbody)
+    				--RemoveTag(dbody, "state.id","avoid")
+    				SetBodyTransform(dbody,Transform(VecAdd(dtrans.pos,Vec(0,-9995,0)),dtrans.rot))
+    			end
+    		end
+    	end
+    	if InputPressed(GetString("savegame.mod.inf.grab")) and GetString("game.player.tool") == "INFINITY" then
+    		if (not SRed and not SBlue) and (not PNuke and EntireAssFuckingCutsceneTypeAnimationTimer <= 0) then
+    			QueryRequire("dynamic")
+    			local hit, dist, _, shape = QueryRaycast(origin,dir,1000)
+    			if hit then
+    				QueryRequire("dynamic")
+    				local HitP = VecAdd(origin,VecScale(dir,dist))
+    				local bodies = QueryAabbBodies(VecAdd(HitP,Vec(-2,-2,-2)),VecAdd(HitP,Vec(2,2,2)))
+    				for i = 1, #bodies do
+    					local body = bodies[i]
+    					--local body = GetShapeBody(shape)
+    					--DebugPrint(body)
+    					--local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
+    					local BlueZone = origin
+    					local cent = GetBodyCenterOfMass(body)
+    					local vel = GetBodyVelocity(body)
+    					local worldPoint = TransformToParentPoint(GetBodyTransform(body), cent)
+    					local idir = VecNormalize(VecSub(worldPoint,BlueZone))
+    					local idist = VecLength(VecSub(worldPoint,BlueZone))
+    					local Bigass = VecSub(BlueZone,worldPoint)
+    					local min,max = GetBodyBounds(body)
+    					local bigness = VecLength(VecSub(max,min))
+    					--DebugCross(worldPoint)
+    					local setvel = VecAdd(VecScale(vel,0.5),VecScale(VecNormalize(Bigass),50))
+    					SetBodyVelocity(body,setvel)
+    					for i = 1, 1 do
+    						local gspawn = worldPoint
+    						ParticleType("plain")
+    						ParticleTile(4)
+    						ParticleColor(0.7,0.8,1,0,0,1)
+    						ParticleRadius(bigness)
+    						ParticleAlpha(0.4,0)
+    						ParticleGravity(0)
+    						ParticleDrag(0)
+    						ParticleEmissive(1)
+    						ParticleRotation(rand(-10,10))
+    						ParticleCollide(0)
+    						SpawnParticle(gspawn,setvel,0.2)
+    					end
+    					table.remove(bodies,i)
+    				end
+    				PlaySound(suck,VecAdd(origin,dir),1,false,rand(2,3))
+    				for i = 1, 1 do
+    					local gspawn = VecAdd(origin,VecScale(dir,1))
+    					ParticleType("plain")
+    					ParticleTile(4)
+    					ParticleColor(0.7,0.8,1,0,0,1)
+    					ParticleRadius(0,1)
+    					ParticleAlpha(0.4,0)
+    					ParticleGravity(0)
+    					ParticleDrag(0)
+    					ParticleEmissive(1)
+    					ParticleRotation(rand(-10,10))
+    					ParticleCollide(0)
+    					SpawnParticle(gspawn,Vec(0,0,0),0.2)
+    				end
+
+    			end
+    		end
+    	end
+    	if InputDown(GetString("savegame.mod.inf.grab")) and GetString("game.player.tool") == "INFINITY" then
+    		UScrollPos = 0
+    		--if InputDown("usetool") == false then
+    		--red grab
+    		if ((SRed and InputDown("grab") == false) and ((PNuke == false) and SBlue == false)) then
+    			BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
+    			local RDist = VecSub(RedTrack,BlueZone)
+    			RVel = VecSub(VecScale(RVel,0.95),VecScale(RDist,1/((30*(RedStr+1))+1)))
+    		end
+    		--blue/blues grab
+    		if ((SBlue and InputDown("usetool") == false) and ((PNuke == false) and SRed == false)) then
+    			local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
+    			if not telek then
+    				local BDist = VecSub(BlueTrack,BlueZone)
+    				BVel = VecSub(VecScale(BVel,0.95),VecScale(BDist,1/((30*(BluStr+5))+1)))
+    			end
+    		end
+    		if (SBlue and telek) then
+    			local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
+    			local hit, dis,_,shape = QueryRaycast(origin, dir, scrollPos)
+    			if hit then
+    				BlueZone = VecAdd(origin,VecScale(dir,dis))
+    			end
+    			for j = 1, #smbt do
+    				local BWANT = VecAdd(BlueZone,VecScale(QuatRotateVec(QuatEuler(j*(360/#smbt)+BROTIME,0,90),Vec(0,0,1)),#smbt/2))
+    				local BDist = VecSub(smbt[j],BWANT)
+
+    				smbv[j] = VecSub(VecScale(smbv[j],0.95),VecScale(BDist,0.002))
+    				if HasTag(BTarget,BluesTracking) then
+    					RemoveTag(BTarget,BluesTracking)
+    				end
+    				BTarget = 0
+    			end
+    		end
+    		--purple grab
+    		if (PNuke == true and Str < 3) and VecLength(VecSub(origin,RedTrack)) <= Str/3+2 then
+    			RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/6+1))
+    			RVel = VecScale(pvel,0.018)
+    		end	
+    	else
+    		if telek then
+    			local BlueZone = Vec(0,0,0)
+    			if InputReleased(GetString("savegame.mod.inf.grab")) then
+    				local hit, dis,_,shape = QueryRaycast(origin, dir, 100)
+    				if hit then
+    					local p = VecAdd(origin,VecScale(dir,dis))
+    					local t = GetShapeWorldTransform(shape)
+    					pd = VecSub(p,t.pos)
+    					BTarget = shape
+    					BTP = TransformToLocalVec(t, pd)
+    					SetTag(BTarget,BluesTracking)
+    				else
+    					BTarget = 0
+    					--BTP = VecAdd(origin, VecScale(dir,scrollPos))
+    				end
+    			end
+    			if not HasTag(BTarget,BluesTracking) then
+    				BTarget = 0
+    			end
+    			if #smbt == 0 then
+    				BTarget = 0
+    				ShotBlue = 0
+    				ShotBlueTime = 0
+    			end
+    			if BTarget ~= 0 then
+    				BlueZone = TransformToParentPoint(GetShapeWorldTransform(BTarget),BTP)
+    			else
+    				if BTarget == -1 then
+    					BlueZone = BTP
+    				end
+    			end
+    			if BTarget ~= 0 or BTarget == -1 then
+    				if ShotBlueTime <= 0 then
+    					ShotBlue = 0
+    				end
+    				if ShotBlue == 0 then
+    					ShotBlue = math.random(1,#smbt)
+    					ShotBlueTime = 20
+    				end
+    				local j = ShotBlue
+    				local BDist = VecSub(smbt[j],BlueZone)
+
+    				smbv[j] = VecSub(VecScale(smbv[j],0.99),VecScale(VecNormalize(BDist),0.08))
+
+    				for i=1, #smbv do
+    					if i ~= ShotBlue then
+    						local BWANT = VecAdd(BlueZone,VecScale(VecNormalize(VecSub(smbt[i],BlueZone)),20))
+    						local BDist = VecSub(smbt[i],BWANT)
+    						smbv[i] = VecSub(VecScale(smbv[i],0.98),VecScale(BDist,0.001))
+    					end
+    				end
+    				DrawSprite(circle, Transform(BlueZone,cam.rot), 0.2, 0.2, 1, 1, 1, 0.3,false,false)
+    			end
+    		end
+    	end
+    	if (SRed == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0) and PNuke == false then
+    		if Burnout == 0 then
+    			if PNuke == false then
+    				PlayLoop(RedSound,RedTrack,RedStr/10,true,1*((RedStr/10)+1))
+    				--PlayLoop(InfExisting,RedTrack,RedStr/10,true,3*((RedStr/10)+1))
+    				if telek == false and (InputDown("usetool") == false and SBlue == false) then
+    					local point = 0
+    					local hit, dist = QueryRaycast(RedTrack,RVel,VecLength(VecScale(RVel,RTime))*1.5)
+    					if hit then
+    						point = VecAdd(RedTrack,VecScale(VecNormalize(RVel),dist))
+    					end
+    					if not hit then
+    						hit,point = QueryClosestPoint(RedTrack,1/3)
+    						dist = VecLength(VecSub(RedTrack,point))
+    					end
+
+    					if hit then
+    						--RedTrack = VecAdd(RedTrack,VecScale(RVel,dist))
+    						Shoot(point,VecNormalize(RVel),"shotgun",RedStr,0.1)
+    						RSplodeTime = 1.4
+    						SRed = false
+    						--Burnout = 100
+    						GDrag(VecAdd(RedTrack,VecScale(RVel,dist)),VecScale(RVel,1/0.018),0.01)
+    					end
+    				end
+    			end
+    		end
+    		if PNuke == false then
+    			RedTrack = VecAdd(RedTrack,VecScale(RVel,RTime))
+    		end
+
+    		if PNuke == false then
+    			if Burnout == 0 then
+    				PointLight(RedTrack,0.6,0.1,0.1,RedStr*60)
+    				if performance == false then
+    					--VisChain(RedTrack,100,0.9,0.8,1,0.5,0,0,Str,Str,true,1,RVec(),cam,false)
+    					if EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
+    						--DrawSprite(circle, Transform(RedTrack,cam.rot), Str/10, Str/10, 1, 1, 1, 0.6,true,true)
+    						--DrawSprite(circle, Transform(RedTrack,cam.rot), Str/5, Str/5, 1, 0, 0, 0.8,true,true)
+    						--[[
+    						for i = 0, 20, 1 do
+    							DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), rand(0,RedStr/5), rand(0,RedStr/5), 1, 1, 1, 1,true,true)
+    						end
+    						for i = 0, 200, 1 do
+    							DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), RedStr/5, RedStr/5, 1, 0, 0, 1,true,true)
+    						end
+    						]]
+    						if SBlue then
+    							for i = 1,360 do
+    								DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames,0)), RedStr/5, RedStr/5, 1, 0, 0, 1,true,false)
+    							end
+    							for i = 1,360 do
+    								DrawSprite(earth,Transform(RedTrack,QuatEuler(i+Frames,0,0)), RedStr/5, RedStr/5, 1, 0, 0, 1,true,false)
+    							end
+    						else
+    							for i = 1,360 do
+    								DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames,0)), 1/5, 1/5, 1, 0, 0, 1,true,false)
+    							end
+    							for i = 1,360 do
+    								DrawSprite(earth,Transform(RedTrack,QuatEuler(i+Frames,0,0)), 1/5, 1/5, 1, 0, 0, 1,true,false)
+    							end
+    						end
+    					end
+    				end
+    			end
+    		end
+    	end
+    	if RSplodeTime > 1 then
+    		local Splstr = (RedStr)/RSplodeTime
+    		local t = RSplodeTime
+    		if RSplodeTime == 1.4 then
+    			PlaySound(Explode,RedTrack,RedStr,false,1.5)
+    			pvoid = CreateShape(GetWorldBody(),Transform(RedTrack,QuatEuler(0,0,0)),0)
+    			ResizeShape(pvoid,-1,-1,-1,1,1,1)
+    			SetBrush("sphere",1,"middle.vox")
+    			DrawShapeBox(pvoid,0,0,0,2,2,2)
+    			for i = 1,1,1 do
+    				Shoot(RedTrack,VecNormalize(RVel),"shotgun",Splstr,0.001)
+    			end
+    			Delete(pvoid)
+    		end
+    		SRed = false
+    		Gravity(RedTrack,-Splstr*10,Splstr*3)
+    		PointLight(RedTrack,1,0,0,Splstr*160)
+    		if performance == false then
+    			for i = 0, 200, 1 do
+    				DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2.6, Splstr/2.6, 1, 1, 1, 1,true,true)
+    			end
+    			for i = 0, 200, 1 do
+    				DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2, Splstr/2, 1, 0, 0, 1,true,true)
+    			end
+    		else
+    			for i = 1,800,1 do
+    				local gdis = VecScale(VecNormalize(RVec()),Splstr/10)
+    				local gspawn = VecAdd(RedTrack,gdis)
+    				ParticleType("plain")
+    				ParticleTile(5)
+    				ParticleColor(1,1,1,1,0,0)
+    				ParticleRadius(Splstr/80)
+    				ParticleAlpha(1,0)
+    				ParticleGravity(0)
+    				ParticleDrag(0.2)
+    				ParticleEmissive(1)
+    				ParticleRotation(rand(-10,10))
+    				ParticleCollide(0)
+    				local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    				local spidir = TransformToParentVec(look, Vec(0,0,rand(-Splstr,Splstr)))
+    				SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,0),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-Splstr/0.5)),1)
+    			end
+    			if RSplodeTime < 1.5 then
+    				for i = 1,0,1 do
+    					local gdis = VecScale(VecNormalize(RVec()),Splstr/1.5)
+    					local gspawn = VecAdd(RedTrack,gdis)
+    					ParticleType("plain")
+    					ParticleTile(5)
+    					ParticleColor(1,1,1,1,0,0)
+    					ParticleRadius(Splstr/50)
+    					ParticleAlpha(1,0)
+    					ParticleGravity(0)
+    					ParticleDrag(0)
+    					ParticleEmissive(1)
+    					ParticleRotation(rand(-10,10))
+    					ParticleCollide(0)
+    					local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    					local spidir = TransformToParentVec(look, Vec(-1,0,0))
+    					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-SplStr/3)),1)
+    				end
+    			end
+    		end
+    		--DebugPrint(RSplodeTime)
+    		RSplodeTime = RSplodeTime-0.1
+    		if RSplodeTime <= 1 then
+    			--DebugPrint("splode")
+    			RedTrack = origin
+    			RVel = Vec(0,0,0)
+    			SRed = false
+    			RedStr = 0.1
+    		end
+    	end
+    	if SBlue == true then
+    		--SBlueStrScaleThingy
+    		BlueTrack = VecAdd(BlueTrack,VecScale(BVel,RTime))
+    		if telek or BluesMerge then
+    			if telek then
+    				if InputPressed(GetString("savegame.mod.inf.tel")) then
+    					for i = 0, BluStr, 1 do
+    						smbt[i] = VecAdd(BlueTrack,VecScale(VecNormalize(RVec()),rand(0,BluStr/7)))
+    						smbv[i] = VecAdd(BVel,VecScale(RVec(),0.1))
+    					end
+    				end
+    				if #smbt < BluStr - 1 then
+    					new = #smbt + 1
+    					smbt[new] = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,(5)/6+0.1))
+    					smbv[new] = VecAdd(VecScale(pvel,0.01),VecScale(VecNormalize(VecAdd(dir,VecScale(RVec(),0.2))),scrollPos*0.05))
+    				end
+    				if #smbt > BluStr + 1 then
+    					for j = #smbt-2, #smbt, 1 do
+    						table.remove(smbt,j)
+    						table.remove(smbv,j)
+    					end
+    				end
+    			end
+    		--blues merging
+    			if BluesMerge then
+    				for i=1, #smbv do
+    					local BWANT = BlueTrack
+    					local BDist = VecSub(smbt[i],BWANT)
+    					if BluStr < 80 then
+    						smbv[i] = VecAdd(VecScale(smbv[i],0.99),VecScale(VecNormalize(BDist),-0.0006*BluStr))
+    					else
+    						smbv[i] = VecAdd(VecScale(smbv[i],0.99),VecScale(VecNormalize(BDist),-0.0006*80))
+    					end
+    					if VecLength(BDist) < 1.5 then
+    						BluStr = BluStr + 1
+    						table.remove(smbt,i)
+    						table.remove(smbv,i)
+    					end
+    					--BVel = VecAdd(VecScale(BVel,1),VecScale(VecNormalize(BDist),0.001/BluStr))
+    				end
+    				if #smbt == 0 then
+    					BluesMerge = false
+    					smbtot = 0
+    				end
+    			end
+    		--blues exist
+    			for j = 1, #smbt do
+    				smbt[j] = VecAdd(smbt[j],VecScale(smbv[j],RTime))
+    				PlayLoop(BlueSound,smbt[j],5/20,true, 2.5)
+    				PointLight(smbt[j],0.1,0.2,1,200)
+    				if performance == false then
+    					--for i = 1, 20, 1 do
+    					--	DrawSprite(circle, Transform(smbt[j],QuatLookAt(Vec(0,0,0),RVec())), 1, 1, 0.2, 0.4, 1, 0.2,false,false)
+    					--end
+    					DrawSprite(earth, Transform(smbt[j],cam.rot), 1, 1, 0.2, 0.4, 1, 1,true,false)
+    					--for i = 1, 20, 1 do
+    					--	local r = rand(-0.5,0.5)
+    					--	DrawSprite(ripple, Transform(VecAdd(smbt[j],Vec(0,r,0)),QuatEuler(90,0,0)), math.sin(2*r*math.pi), math.sin(2*r*math.pi), 1, 1, 1, 1,true,true)
+    					--end
+    				end
+    			end
+
+    		end
+    	--Normal blue
+    		if not telek then
+    			if BluStr < 80 then
+    				PlayLoop(BlueSound,BlueTrack,BluStr/20,true, 6/((BluStr/10)+1))
+    				PointLight(BlueTrack,0.1,0.2,1,BluStr*100)
+    				if performance == false then
+    					--for i = 1, 20, 1 do
+    					--	DrawSprite(circle, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), BluStr/5, BluStr/5, 0.2, 0.4, 1, 0.2,false,false)
+    					--end
+    					for i = 1,360 do
+    						DrawSprite(earth,Transform(BlueTrack,QuatEuler(0,i+Frames,0)), BluStr/5, BluStr/5, 0, 0.4, 1, 1,true,false)
+    					end
+    					for i = 1,360 do
+    						DrawSprite(earth,Transform(BlueTrack,QuatEuler(i+Frames,0,0)), BluStr/5, BluStr/5, 0, 0.4, 1, 1,true,false)
+    					end
+    					--for i = 1, 20, 1 do
+    					--	DrawSprite(ripple, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), rand(0,BluStr/5), rand(0,BluStr/5), 1, 1, 1, 1,true,true)
+    					--end
+    				end
+    			else
+    				DrawSprite(star, Transform(BlueTrack,cam.rot), 0.8,0.5, 0.3, rand(0.3,0.6), 1, 1,true,true)
+    				for i = 1, 50, 1 do
+    					DrawSprite(circle, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), 0.2, 0.2, 0, 0, 0, 1,true,false)
+    				end
+    			end
+    		--Gravity(BlueTrack,Str,Str,_)
+    			--nuke detection
+    			if InputReleased("grab") then
+    				NTimer = 100
+    			end
+    			--purple merge
+    			if (SRed and InputDown("grab") == false) and GetString("game.player.tool") == "INFINITY" then
+    				local Rdist = VecLength(VecSub(RedTrack,BlueTrack))
+    				local Rdir = VecNormalize(VecSub(RedTrack,BlueTrack))
+    				NTimer = NTimer - 1
+    				if BluStr > RedStr then
+    					Str = BluStr
+    				else
+    					Str = RedStr
+    				end
+    				if InputPressed("q") then
+    					MTimer = 200
+    				end
+    				if InputDown(GetString("savegame.mod.inf.grab")) then
+    					local BlueZone = VecAdd(origin, VecScale(dir,scrollPos))
+    					local protata = TransformToParentVec(Feet, Vec(-1,0,0))
+    					--if BluStr > RedStr * 1.5 then
+    						local rZone = VecAdd(BlueZone,VecScale(protata,-(2*Str*MTimer/80)/(20)))
+    						local RDist = VecSub(RedTrack,rZone)
+    						RVel = VecSub(VecScale(RVel,0.3),VecScale(RDist,1/((10*(RedStr+1))+1)))
+
+    						local bZone = VecAdd(BlueZone,VecScale(protata,(2*Str*MTimer/80)/(20)))
+    						local BDist = VecSub(BlueTrack,bZone)
+    						BVel = VecSub(VecScale(BVel,0.3),VecScale(BDist,1/((10*(BluStr+1))+1)))
+
+    					if MTimer ~= 0 then
+    						--MTimer = MTimer - 1
+    					end
+    					if BluStr < RedStr then
+    						BluStr = (RedStr-BluStr)/10+BluStr
+    					end
+    					if RedStr < BluStr then
+    						RedStr = (BluStr-RedStr)/10+RedStr
+    					end
+    				else
+    					RVel = VecSub(VecScale(RVel,0.99),VecScale(VecScale(Rdir,0.1*(1/(Rdist+5))),BluStr*0.018*RTime))
+    					BVel = VecSub(VecScale(BVel,0.99),VecScale(VecScale(VecScale(Rdir,-1),0.1*(1/(Rdist+5))),RedStr*0.018*RTime))
+    				end
+
+    				if rand(0,10) > 8 and VecLength(VecSub(RedTrack,BlueTrack)) < Str*3 then
+    					for i = 1, 2 do
+    						s = VecAdd(RedTrack,VecScale(RVec(),rand(-RedStr/8,RedStr/8)))
+    						local e = VecAdd(BlueTrack,VecScale(RVec(),rand(-BluStr/12,BluStr/12)))
+    						--local s = RedTrack
+    						--local e = BlueTrack
+    						local last = s
+    						for i=1, 10 do
+    							local tt = i/10
+    							local p = VecLerp(s, e, tt)
+    							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
+    							DrawLine(last, p, 1, 1, 1)
+    							last = p
+    						end
+    					end
+    					for i = 1, 2 do
+    						s = VecAdd(BlueTrack,VecScale(RVec(),rand(-BluStr/8,BluStr/8)))
+    						local e = VecAdd(RedTrack,VecScale(RVec(),rand(-RedStr/12,RedStr/12)))
+    						local last = s
+    						for i=1, 10 do
+    							local tt = i/10
+    							local p = VecLerp(s, e, tt)
+    							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
+    							DrawLine(last, p, 1, 1, 1)
+    							last = p
+    						end
+    					end
+    				end
+    				if VecLength(VecSub(RedTrack,BlueTrack)) < Str/5 then
+
+    					--DrawLine(VecAdd(RedTrack,RVec()),VecSub(RedTrack,Rdir),1,1,1)
+    					--DrawLine(VecAdd(BlueTrack,RVec()),VecSub(BlueTrack,VecScale(Rdir,-1)),1,1,1)
+    					--VisChain()
+    					--VisChain(RedTrack,Rdist/Str,1,1,1,0,0,0,true,Str,Rdir,0,true)
+    					local c1, c2, c3 = GetQuatEuler(QuatLookAt(RedTrack,BlueTrack))
+    					--DebugPrint(Vec(c1,c2,c3))
+    					RVel = VecSub(VecScale(RVel,0),VecScale(VecScale(Rdir,0.2*(1/(6))),Str*0.05*RTime))
+    					BVel = VecSub(VecScale(BVel,0),VecScale(VecScale(VecScale(Rdir,-1),0.2*(1/(6))),Str*0.05*RTime))
+    					local middle = VecAdd(VecSub())
+
+    					if performance == false then
+    						--if math.floor(GetTime()*10) % 4 == 1 then
+    						--	VisChain(VecAdd(RedTrack,VecScale(RVec(),Str/10)),0.2/(Rdist+1),0.9,0.8,1,1,0.4,0.4,1,1,true,0.1,VecScale(Rdir,-1),cam,false)
+    						--	VisChain(VecAdd(BlueTrack,VecScale(RVec(),Str/10)),0.2/(Rdist+1),0.9,0.8,1,0.4,0.8,1,1,1,true,0.1,VecScale(Rdir,1),cam,false)
+    						--end
+    					end
+    					BLight = VecAdd(VecScale(VecSub(BlueTrack,RedTrack),0.5),RedTrack)
+    					RLight = VecAdd(VecScale(VecSub(RedTrack,BlueTrack),0.5),BlueTrack)
+    					local h1,h2,h3 = GetQuatEuler(cam.rot)
+    					if performance == false then
+    						for i = 0, 10 do
+    							DrawSprite(ripple3,Transform(BLight,QuatEuler(0,h2,-Frames*5+55+i*2)), Str/5, Str/5, 1, 0, 0, 1,true,false)
+    							DrawSprite(ripple3,Transform(BLight,QuatEuler(0,h2,-Frames*5+i*2)), Str/5, Str/5, 0, 0, 1, 1,true,false)
+    						end
+    					end
+    					PointLight(BLight,0.1,0.2,1,Str*100/(Rdist+1))
+    					PointLight(RLight,0.6,0.1,0.1,Str*80/(Rdist+1))
+    					for i = 1, 2 do
+    						s = VecAdd(BlueTrack,VecScale(RVec(),rand(-Str/8,Str/8)))
+    						local e = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/12,Str/12)))
+    						local last = s
+    						for i=1, 10 do
+    							local tt = i/10
+    							local p = VecLerp(s, e, tt)
+    							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
+    							DrawLine(last, p, 1, 1, 1)
+    							last = p
+    						end
+    						s = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/8,Str/8)))
+    						local e = VecAdd(BlueTrack,VecScale(RVec(),rand(-Str/12,Str/12)))
+    						local last = s
+    						for i=1, 10 do
+    							local tt = i/10
+    							local p = VecLerp(s, e, tt)
+    							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.2*tt)))
+    							DrawLine(last, p, 1, 1, 1)
+    							last = p
+    						end
+    					end
+    					--PointLight()
+    				end
+    				if NTimer <= 0 then
+    					if VecLength(VecSub(RedTrack,BlueTrack)) < ((RedStr+BluStr)/2)/27 then
+    						PNuke = true
+    						NRelease = true
+    						--RVel = VecAdd(BVel,RVel)
+    						RVel = Vec(0,0,0)
+    						RedTrack = BLight
+    						for i = 0, 2000, 1 do
+    							dcirc[#dcirc+1] = QuatEuler(rand(-180,180),rand(-180,180),rand(-180,180))
+    							ctime[#ctime+1] = rand(-170,200)
+    						end
+    					end
+    				end
+    			end
+    		end
+    	end
+    	if BSplodeTime > 1 then
+    		SBlue = false
+    		local Splstr = (BluStr)/BSplodeTime
+    		local t = BSplodeTime
+    		--MakeHole(BlueTrack,Splstr/3,Splstr/3,Splstr/3)
+    		--Shoot(BlueTrackD,VecNormalize(BVel),"shotgun",Splstr/2,0.1)
+    		Gravity(BlueTrack,Splstr*50,Splstr*3)
+    		PointLight(BlueTrack,0.1,0.2,0.6,Splstr*120)
+    		if performance == false then
+    			for i = 0, 200, 1 do
+    				DrawSprite(circle, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2.6, Splstr/2.6, 1, 1, 1, 1,true,true)
+    			end
+    			for i = 0, 200, 1 do
+    				DrawSprite(ripple, Transform(BlueTrack,QuatLookAt(Vec(0,0,0),RVec())), Splstr/2, Splstr/2, 0, 0, 1, 1,true,true)
+    			end
+    		else
+    			for i = 1,800,1 do
+    				local gdis = VecScale(VecNormalize(RVec()),Splstr*3)
+    				local gspawn = VecAdd(BlueTrack,gdis)
+    				ParticleType("plain")
+    				ParticleTile(5)
+    				ParticleColor(1,1,1,0,0.2,1)
+    				ParticleRadius(VecLength(gdis)/80)
+    				ParticleAlpha(0,1)
+    				ParticleGravity(0)
+    				ParticleDrag(0)
+    				ParticleEmissive(1)
+    				ParticleRotation(rand(-10,10))
+    				ParticleCollide(0)
+    				SpawnParticle(gspawn,VecScale(gdis,-5),0.2)
+    			end
+    		end
+    		BSplodeTime = BSplodeTime-0.1
+    		if BSplodeTime <= 1 then
+    			--DebugPrint("nomosplode")
+    			BlueTrack = origin
+    			BVel = Vec(0,0,0)
+    			SBlue = false
+    			BluStr = 0.1
+    		end
+    	end
+    	if PNuke == true then
+    		SBlue = false
+    		Burnout = 5
+    		SetToolTransform(Transform(Vec(-0.025,-0.3,-0.6),QuatEuler(0,0,0)), 0)
+
+    		if PRtoggle == true then
+    			local campos = VecAdd(RedTrack,VecScale(dir,-Str*1))
+    			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,RedTrack))
+    			local ccam = Transform(VecAdd(campos,Vec(0,0,0)),Feet.rot)
+    			SetCameraTransform(ccam)
+    		end
+    		if NukeTime == 0 then
+    			--DebugPrint((VecLength(RVel)/time))
+
+    			--damage
+    			if Str<1 then
+    				for i = -1, VecLength(VecScale(RVel,RTime)),0.02 do
+    					RedTrackD = VecAdd(RedTrack,VecScale(RVel,i))
+    					Destroy(RedTrackD,0.5*0.3,false,0,0,0.5*0.1)
+    				end
+    			else
+    				for i = -1, VecLength(VecScale(RVel,RTime)),0.03*(Str)+0.02 do
+    					RedTrackD = VecAdd(RedTrack,VecScale(RVel,i))
+    					Destroy(RedTrackD,Str*0.2,false,0,0,Str*0.1)
+    				end
+    			end
+    			PointLight(RedTrackD,0.4,0.1,0.8,Str*100)
+    			--RedTrack = RedTrackD
+
+    			--DebugPrint(GetWindVelocity(RedTrack))
+    			if Str > 2 then
+    				--Gravity(RedTrack,Str*10*RTime,Str*0.3,nil)
+    			end
+    			local h1,h2,h3 = GetQuatEuler(cam.rot)
+    			--VisChain(RedTrack,Str/9,1,1,1,1,1,1,true,Str,RVec(),cam,true)
+    			PlayLoop(InfExisting,RedTrack,Str/20,true, 1/((Str/10)+1))
+
+    			--visuals
+    			if performance == false or time < 1 then
+    				rotarted = QuatLookAt(Vec(0,0,0),TransformToParentVec(cam, Vec(0,0,-1)))
+    				-- for safe keeping: QuatEuler(rand(-180,180),0,rand(-180,180))
+    				--[[
+    				for i = 1, 500, 1 do
+    					--DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), Str/5, Str/5, 0.6, 0.2, 1, 1,true,true)
+    					local gyat = rand(Str/4,Str/3)
+    					DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), gyat, gyat, 0.2, 0, 1.0, 1,true,true)
+    					DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), gyat, gyat, 0.1, 0, 1, 1,true,true)
+    					--DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),VecNormalize(RVec()))), Str/5, Str/5, 0, 0, 1, 1,true,true)
+    					--DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),VecNormalize(RVec()))), Str/5, Str/5, 0.6, 0, 1, 1,true,true)
+    				end
+    				]]
+    					for i = 1,360 do
+    						DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames,0)), Str/3.1, Str/3.1, 0.4, 0.2, 0.6, 1,true,true)
+    					end
+    					for i = 1,360 do
+    						DrawSprite(earth,Transform(RedTrack,QuatEuler(i+Frames,0,0)), Str/3.1, Str/3.1, 0.4, 0.2, 0.6, 1,true,true)
+    					end
+    					for i = 1,360 do
+    						DrawSprite(earth,Transform(RedTrack,QuatEuler(0,i+Frames*5,0)), Str/3, Str/3, 0, 0, 0.6, 1,true,true)
+    					end
+    				--if #dcirc < 1000 then
+    				--	for i = 1, 3, 1 do
+    				--		dcirc[#dcirc+1] = QuatEuler(rand(-180,180),rand(-180,180),rand(-180,180))
+    				--		ctime[#ctime+1] = 200
+    				--	end
+    				--end
+    				for i = 1, #dcirc, 1 do
+    					ctime[i] = ctime[i] - 0.5*RTime
+    					c = ctime[i]
+    					cspace = VecScale(QuatRotateVec(dcirc[i],Vec(math.cos(160/(c/10))*(c/120),0,math.sin(160/(c/10))*(c/120))),Str/11)
+    					DrawSprite(circle, Transform(VecAdd(RedTrack,cspace),rotarted), (Str*0.01),(Str*0.01), 1, 1, 1, 1,true,true)
+    					if ctime[i]<=-160 then
+    						ctime[i] = 200
+    					end
+    				end
+    				--VisChain(RedTrack,100,0.9,0.8,1,0.2,0,0.7,Str*1.5,Str*1.5,true,1,RVec(),cam,false)
+    			end
+    			if honored == true and NMove == false then
+    				Str = 0.1
+    				if GetString("game.player.tool") == "INFINITY" then
+    					if InputDown(GetString("savegame.mod.inf.sadd")) then
+    						StStr = StStr + 0.4
+    						--DebugPrint(StStr)
+    					end
+    					if InputDown(GetString("savegame.mod.inf.ssub")) then
+    						StStr = StStr - 0.2
+    						--DebugPrint(StStr)
+    					end
+    				end
+    				if StStr < 0 then
+    					StStr = 0
+    				end
+    				DrawSprite(star, Transform(RedTrackD,cam.rot), rand(Str/1.2,Str/0.8), rand(Str/1.2,Str/0.8), 1, 0.5, 1, 1,true,true)
+    				--lightning to nearby shapes
+    				local bzzt = QueryAabbShapes(VecAdd(RedTrack,Vec(-5,-5,-5)),VecAdd(RedTrack,Vec(5,5,5)))
+    				for i=1,#bzzt do
+    					if rand(0,10) > 9.8 then
+    						local hit, e = GetShapeClosestPoint(bzzt[i],RedTrack)
+    						--e = GetShapeWorldTransform(bzzt[i]).pos
+    						s = RedTrack
+    						--Draw laser line in ten segments with random offset, stolen from teardown lazer gun built-in-mod cause I didn't know how to use veclerp
+    						local last = s
+    						for i=1, 10 do
+    							local tt = i/10
+    							local p = VecLerp(s, e, tt)
+    							p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
+    							DrawLine(last, p, 1, 1, 1)
+    							last = p
+    						end
+    					end
+    				end
+    				--lightning in the air
+    				if rand(0,10) > 9 then
+    					for j = 1, StStr do
+    						s = VecAdd(origin,VecScale(RVec(),rand(-5,5)))
+    						local e = VecAdd(RedTrack,VecScale(RVec(),rand(-5,5)))
+    						local last = s
+    						for i=1, 4 do
+    							local tt = i/4
+    							local p = VecLerp(s, e, tt)
+    							p = VecAdd(p, VecScale(VecNormalize(RVec()),(0.5*tt)))
+    							DrawLine(last, p, 1, 1, 1)
+    							last = p
+    						end
+    					end
+    				end
+
+    			end
+    			if (pshart == true and DomainToggle == false) then
+    				if NMove == false then
+    					SetPostProcessingProperty("brightness",1.2)
+    					SetPostProcessingProperty("saturation",0.8)
+    					SetEnvironmentProperty("fogColor",0,0,0)
+    					--SetEnvironmentProperty("fogParams",20,120,0.9,2)
+    					SetEnvironmentProperty("skyboxbrightness", bright-0.8)
+    					--SetEnvironmentProperty("skyboxtint",tintr-0.95,tintg-0.95,tintb-0.95)
+    					SetEnvironmentProperty("sunBrightness",0)
+    				end
+    				if GetString("game.player.tool") == "INFINITY" then
+    					if (InputReleased("grab") or InputReleased("usetool")) or (((InputReleased(GetString("savegame.mod.inf.time")) or (NMove and InputDown(GetString("savegame.mod.inf.time")) == false)) and honored == true) or (pshart and honored == false)) then
+    						SetPostProcessingProperty("brightness",bright)
+    						SetPostProcessingProperty("saturation",sat)
+    						SetEnvironmentProperty("fogColor",fogr,fogg,fogb)
+    						--SetEnvironmentProperty("fogParams",fogp1,fogp2,fogp3,fogp4)
+    						SetEnvironmentProperty("skyboxbrightness", skybright)
+    						--SetEnvironmentProperty("skyboxtint",tintr,tintg,tintb)
+    						SetEnvironmentProperty("sunBrightness",sun)
+    					end
+    					if (InputReleased("grab") or InputReleased("usetool")) or (InputReleased(GetString("savegame.mod.inf.time")) and honored == true) then
+    						pshart = false
+    						PNuke = false
+    						if (honored == true and InputReleased(GetString("savegame.mod.inf.time"))) and NMove == false then
+    							PlaySound(pShot,RedTrack,1,false,10)
+    							for i = -0.1, 100,0.05 do
+    								RedTrackD = VecAdd(RedTrack,VecScale(dir,i))
+    								if StStr > 0.5 then
+    									Destroy(RedTrackD,StStr*0.1,false,0,0,StStr*0.15)
+    								else
+    									Destroy(RedTrackD,StStr*0.1,false,0,0,0.5*0.15)
+    								end
+    								if performance == true then
+    									for i = 1,2,1 do
+    										local gdis = VecScale(VecNormalize(RVec()),StStr/6)
+    										local gspawn = VecAdd(RedTrackD,gdis)
+    										ParticleType("plain")
+    										ParticleTile(2)
+    										ParticleColor(1,0.8,1,1,0,1)
+    										ParticleRadius(StStr/70)
+    										ParticleAlpha(1,0)
+    										ParticleGravity(0)
+    										ParticleDrag(0.5)
+    										ParticleEmissive(5)
+    										ParticleRotation(rand(-10,10))
+    										ParticleCollide(0)
+    										local look = Transform(RedTrackD,QuatLookAt(RedTrackD,gspawn))
+    										local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
+    										SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(dir,4),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-StStr/3)),0.5)
+    									end
+    								end
+    							end
+    							PointLight(RedTrack,0.6,0.2,1,StStr*1000)
+    							PointLight(RedTrack,0.6,0.2,1,StStr*1000)
+    						end
+    						honored = false
+    						NMove = false
+    					end
+    				end
+    			end
+    			--funky ass movement options
+    			if GetString("game.player.tool") == "INFINITY" then
+    				if InputDown(GetString("savegame.mod.inf.grab")) then
+    					RVel = Vec(0,0,0)
+    				end
+    				if InputReleased(GetString("savegame.mod.inf.grab")) then
+    					--RVel = VecScale(dir,(scrollPos/3)/Str)
+    					if Str < 1 then
+    						--Str = 1
+    					end
+    					RVel = VecScale(dir,0.5+(15/(Str*1)))
+    					NRelease = false
+    					PointLight(RedTrackD,0.8,0.4,1,Str*2000)
+    					PointLight(RedTrackD,0.8,0.4,1,Str*2000)
+    					DrawSprite(star, Transform(RedTrackD,cam.rot), rand(Str/1.2,Str/0.8), rand(Str/1.2,Str/0.8), 1, 1, 1, 1,true,true)
+    					if pshart and honored then
+    						NMove = true
+    						--Str = StStr
+    						--StStr = 0
+    						RVel = VecScale(dir,8)
+    					end
+    					PlaySound(pShot,RedTrack,1,false,6)
+    					PlaySound(Water,RedTrack,5,false,6)
+    				end
+    				if pshart and NMove then
+    					--PointLight(RedTrackD,0.1,0.2,1,Str*2000)
+    					--PointLight(RedTrackD,1,0.2,0.2,Str*2000)
+    					PointLight(RedTrackD,0.6,0.2,1,Str*500)
+    					PointLight(RedTrackD,0.6,0.2,1,Str*500)
+    					if honored then
+
+    							if VecLength(VecSub(RedTrack,origin)) > ((StStr-Str)/2+Str)/5 then
+    								Str = (StStr-Str)/4+Str
+    							end
+    							if Str > StStr - 0.1 then
+    								Str = StStr
+    							end
+    						--DebugPrint(Str)
+    					end
+    				end
+    				if (InputReleased("grab") or InputReleased("usetool")) then
+    					if NRelease == true then
+    						NukeTime = 1
+    						Burnout = 20
+    						PlaySound(Explode,RedTrack,Str,false,1)
+    						PlaySound(Water,RedTrack,Str,false,2)
+    					else
+    						PNuke = false
+    						Burnout = 20
+    						RedTrack = origin
+    					end
+    					for i = 1, #dcirc, 1 do
+    						dcirc[i] = nil
+    						ctime[i] = nil
+    					end
+    				end
+    			end
+    			--velocity movement
+    			if VecLength(RVel)/RTime > 5 then	
+    			if pshart == false then
+    				RVel = VecScale(VecNormalize(RVel),(5))
+    			end
+    			--DebugPrint((VecLength(RVel)))
+    			end
+    			if honored == false or InputDown(GetString("savegame.mod.inf.time")) == false then
+    				RedTrack = VecAdd(RedTrack,VecScale(RVel,RTime))
+    			else
+    				RedTrack = VecAdd(RedTrack,VecScale(RVel,0.025))
+    			end
+    		end
+
+    --NukeSplosion all over the place
+    		if NukeTime ~= 0 then
+    			NukeS = (Str/3)/NukeTime
+    			--/NukeTime
+    			PointLight(RedTrack,0.1,0.2,1,NukeS*200)
+    			PointLight(RedTrack,1,0.1,0.1,NukeS*150)
+    			if performance == false or time<1 then
+    				local l1,l2,l3 = GetQuatEuler(cam.rot)
+    				DrawSprite(circle, Transform(RedTrack,QuatEuler(l1,l2,l3)), NukeS, NukeS, 1, 0.6, 1, 1,true,true)
+    				DrawSprite(circle, Transform(RedTrack,QuatEuler(l1,l2,l3)), NukeS/1.2, NukeS/1.2, 1, 1, 1, 1,true, true)
+    				for i = 0, 200, 1 do
+    					DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), NukeS, NukeS, 0.2, 0, 1.0, 0.65,true,true)
+    					DrawSprite(ripple, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), NukeS, NukeS, 0, 0, 1, 1,true,true)
+    					DrawSprite(circle, Transform(RedTrack,QuatLookAt(Vec(0,0,0),RVec())), NukeS/2, NukeS/2, 1, 1, 1, 1,true,true)
+    				end
+    				QuatLookAt(Vec(0,0,0),RVec())
+    			end
+    			--RVel = Vec(0,0,0)
+
+    			for i = 1, 10 do
+    				s = VecAdd(RedTrack,VecScale(RVec(),rand(-NukeS/6,NukeS/6)))
+    				local e = VecAdd(RedTrack,VecScale(RVec(),rand(Str/2,NukeS*2)))
+    				local last = s
+    				for i=1, 10 do
+    					local tt = i/10
+    					local p = VecLerp(s, e, tt)
+    					p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
+    					DrawLine(last, p, 1, 1, 1)
+    					last = p
+    				end
+    			end
+    			--local PPlayerD = VecLength(VecSub(RedTrack,origin))
+    			--if VecLength(VecSub(RedTrack,origin)) < NukeS then
+    				--DebugPrint(GetPlayerHealth(playerId)-(NukeS/PPlayerD)/10)
+    				--SetPlayerHealth(playerId, ((GetPlayerHealth(playerId)-(NukeS/PPlayerD)/100))*time)
+    			--end
+    		end
+    	end
+    	if GetString("game.player.tool") == "INFINITY" then
+    		if InputPressed(GetString("savegame.mod.inf.flykey")) then
+    			if FlyToggle then
+    				FlyToggle = false
+    			else
+    				FlyToggle = true
+    			end
+    		end
+    	end
+    	if GetString("game.player.tool") == "INFINITY" then
+    		if InputReleased(GetString("savegame.mod.inf.time")) and (pshart == true and honored == true) then
+    			pshart = false
+    			PNuke = false
+    			honored = false
+    		end
+    	end
+    	if EntireAssFuckingCutsceneTypeAnimationTimer > 0 and honored == true then
+    		if performance == true then
+    			EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1*RTime/0.01
+    		else
+    			EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1
+    		end
+    		bich = EntireAssFuckingCutsceneTypeAnimationTimer
+    		Str = 2
+    		SetString("game.player.tool","INFINITY", true)
+    		SBlue = false
+    		--local middle = honoredpos
+    		local middle = Vec(0,1000,0)
+
+    		SetTimeScale(0.01)
+    		time = 0.01
+    		--middle = Vec(0,10000,0)
+    		BVel = Vec(0,0,0)
+    		RVel = Vec(0,0,0)
+    		ubich = bich
+    		--adderall = Vec(math.cos(60/(ubich/10))*(bich/120),0,math.sin(60/(ubich/10))*(bich/120))
+    		adderall = VecScale(honoredrotata,math.sin((bich-100)/33)/1.5)
+    		BlueTrack = VecAdd(middle,VecScale(adderall,-1))
+    		RedTrack = VecAdd(middle,adderall)
+    		rotata = VecNormalize(VecSub(RedTrack,BlueTrack))
+    		--cadir = TransformToParentVec(cam.rot, Vec(1,0,0))
+    		local campos = VecAdd(middle,VecScale(dir,-1))
+    		local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,middle))
+    		local ccam = Transform(VecAdd(campos,Vec(0,0.2,0)),Feet.rot)
+    		SetCameraTransform(ccam)
+    			SetPostProcessingProperty("brightness",1.2)
+    			SetPostProcessingProperty("saturation",1)
+    			SetEnvironmentProperty("fogColor",0,0,0)
+    			--SetEnvironmentProperty("fogParams",20,120,0.9,2)
+    			SetEnvironmentProperty("skyboxbrightness", bright-0.8)
+    			--SetEnvironmentProperty("skyboxtint",tintr-0.95,tintg-0.95,tintb-0.95)
+    			SetEnvironmentProperty("sunBrightness",0)
+    		if bich < 92 and bich > 90 then
+    			PlaySound(Water,middle,100,false,20)
+    		end
+
+    		if bich < 100 then
+    			for i = 0, 1, 0.005 do
+
+    				DrawSprite(ripple, Transform(middle,QuatLookAt(Vec(0,0,rand(-0.01,0.01)),honoredrotata)), (bich-100)*(i), (bich-100)*(i), 0.6, 0.2, 0.2, 0.1,true,true)
+    				DrawSprite(ripple, Transform(middle,QuatLookAt(Vec(0,0,rand(-0.01,0.01)),honoredrotata)), (bich-100)*(i+0.0025), (bich-100)*(i+0.0025), 0.0, 0.0, 1.0, 0.1,true,true)
+    			end
+    		end
+
+    		--DebugPrint(bich)
+    		for i = 10, 100, 1 do
+    			if bich > 100 then
+    				DrawSprite(ripple, Transform(VecAdd(middle,adderall),QuatLookAt(Vec(0,0,0),RVec())), 0.2, 0.2, 1, 0, 0, 1,true,true)
+    				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1)),QuatLookAt(Vec(0,0,0),RVec())), 0.2, 0.2, 0, 0, 1, 1,true,true)
+    			else
+    				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,1/2)),QuatLookAt(Vec(0,0,0),RVec())), 0.1, 0.1, 1, 0, 0, 1,true,true)
+    				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1/2)),QuatLookAt(Vec(0,0,0),RVec())), 0.1, 0.1, 0, 0, 1, 1,true,true)
+    				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,1/3)),QuatLookAt(Vec(0,0,0),RVec())), 0.05, 0.05, 1, 0, 0, 1,true,true)
+    				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1/3)),QuatLookAt(Vec(0,0,0),RVec())), 0.05, 0.05, 0, 0, 1, 1,true,true)
+    				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,1/12)),QuatLookAt(Vec(0,0,0),RVec())), 0.15, 0.15, 1, 0, 0, 1,true,true)
+    				DrawSprite(ripple, Transform(VecAdd(middle,VecScale(adderall,-1/12)),QuatLookAt(Vec(0,0,0),RVec())), 0.15, 0.15, 0, 0, 1, 1,true,true)
+    			end
+    		end
+    		if bich < 20 then
+    			PointLight(middle,1,1,1,5/(bich/10))
+    			PointLight(middle,0.1,0.2,1,5/(bich/10))
+    			PointLight(middle,1,0.2,0.2,5/(bich/10))
+    			DrawSprite(star, Transform(middle,cam.rot), rand(0.02/(bich/10),0.03/(bich/10)), rand(0.02/(bich/10),0.03/(bich/10)), 1, 1, 1, 1,true,true)
+    		end
+    		if bich <= 1 then
+    			pshart = true
+    			PNuke = true
+    			RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4))
+    			PointLight(RedTrack,1,1,1,10/(bich/100))
+    			PointLight(RedTrack,0.1,0.2,1,10/(bich/100))
+    			PointLight(RedTrack,1,0.2,0.2,10/(bich/100))
+    			RVel = Vec(0,0,0)
+    			if VecLength(VecSub(origin,RedTrack)) <= 2 then
+    				RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),dir)
+    			end
+    			--SetPostProcessingProperty("colorbalance", cb1, cb2, cb3)
+    			EntireAssFuckingCutsceneTypeAnimationTimer = 0
+    			StStr = 3
+    		end
+    	end
+    	if EntireAssFuckingCutsceneTypeAnimationTimer > 0 and honored == false then
+    		if performance == false then
+    			--EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1
+    		end
+
+    		bich = EntireAssFuckingCutsceneTypeAnimationTimer
+    		SetString("game.player.tool","INFINITY", true)
+    		SBlue = false
+    		SetPostProcessingProperty("brightness",1.2)
+    		SetPostProcessingProperty("saturation",1)
+    		SetEnvironmentProperty("fogColor",0,0,0)
+    		--SetEnvironmentProperty("fogParams",20,120,0.9,2)
+    		SetEnvironmentProperty("skyboxbrightness", bright-0.8)
+    		--SetEnvironmentProperty("skyboxtint",tintr-0.95,tintg-0.95,tintb-0.95)
+    		SetEnvironmentProperty("sunBrightness",0)
+    		--local middle = honoredpos
+    		honoredrotata = TransformToParentVec(cam, Vec(-1,0,0))
+    		local middle = Vec(0,1000,0)
+    		--local middle = VecAdd(origin,dir)
+    		BVel = Vec(0,0,0)
+    		RVel = Vec(0,0,0)
+    		local borigin = VecAdd(origin,Vec(0,-0.5,0))
+    		local mid2 = VecAdd(borigin,VecScale(Vec(dir[1],0,dir[3]),-3))
+    		adderall = VecScale(honoredrotata,2)
+    		if bich > 350 then
+    			Str = 0
+    			local campos = VecAdd(borigin,VecScale(dir,3))
+    			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,borigin))
+    			local ccam = Transform(VecAdd(campos,Vec(0,0.2,0)),QuatEuler(c1,c2,c3))
+    			SetCameraTransform(ccam)
+    			if bich <= 450 then
+    				if bich < 450 and bich > 440 then
+    					PointLight(VecAdd(mid2,VecScale(adderall,-1)),0.1,0.2,1,10000)
+    				end
+    				if bich < 400 and bich > 390 then
+    					PointLight(VecAdd(mid2,VecScale(adderall,1)),1,0.2,0.2,10000)
+    				end
+    				for i = 1,100,1 do
+    					--DrawSprite(ripple, Transform(VecAdd(mid2,VecScale(adderall,-1)),QuatLookAt(Vec(0,0,0),RVec())), 1, 1, 0, 0, 1, 1,false,false)
+    				end
+    				for i = 1,360 do
+    					DrawSprite(earth, Transform(VecAdd(mid2,VecScale(adderall,-1)),QuatEuler(0,i,0)), 2, 2, 0, 0, 1, 1,true,false)
+    				end
+    				if bich <= 400 then
+    					for i = 1, 100, 1 do
+    						--DrawSprite(ripple, Transform(VecAdd(mid2,adderall),QuatLookAt(Vec(0,0,0),RVec())), 1, 1, 1, 0, 0, 1,false,false)
+    					end
+    					for i = 1,360 do
+    						DrawSprite(earth, Transform(VecAdd(mid2,VecScale(adderall,1)),QuatEuler(0,i,0)), 2, 2, 1, 0, 0, 1,true,false)
+    					end
+    				--	DrawSprite(earth, Transform(VecAdd(mid2,VecScale(adderall,1)),QuatEuler(0,0,i)), 2, 2, 1, 0, 0, 1,true,false)
+    				end
+
+    			end
+    		end
+    		if bich <= 350 and bich > 200 then
+    			--EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 0.5*(RTime/0.01)
+    			--SetTimeScale(0.01)
+    			Str = 0
+    			local campos = VecAdd(middle,VecScale(Vec(0,-1,0),-2))
+    			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,middle))
+    			local ccam = Transform(VecAdd(campos,Vec(0,0,0)),QuatEuler(c1,c2,c3))
+    			SetCameraTransform(ccam)
+    			local add2 = VecScale(Vec(-1,0,0),bich/1000)
+
+    			--for i = 1, 20, 1 do
+    				DrawSprite(earth, Transform(VecAdd(middle,VecScale(add2,-1)),QuatEuler(c1,c2,c3)), 1, 1, 0, 0, 1, 1,true,true)
+    				DrawSprite(earth, Transform(VecAdd(middle,add2),QuatEuler(c1,c2,c3)), 1, 1, 1, 0, 0, 1,true,true)
+    				--DrawSprite(circle,Transform(middle,QuatLookAt(Vec(0,0,0),RVec())),0.4,0.4,0,0,0,0.5,false,false)
+    			--end
+
+    				DrawSprite(circle,Transform(VecAdd(middle,VecSub(middle,campos)),QuatEuler(c1,c2,c3)), 20, 20, 0, 0, 0, 1,true,false)
+    				--DrawSprite(ripple,Transform(middle,QuatLookAt(Vec(0,0,0),RVec())), 0.8/(bich/150), 0.8/(bich/150), 0.8, 0.2, 1, 1,true,true)
+    			--end
+    			--PointLight(VecAdd(middle,VecScale(add2,-1)),0.1,0.2,1,100)
+    			--PointLight(VecAdd(middle,VecScale(add2,1)),1,0.2,0.2,100)
+    		end
+    		if bich <= 200 and bich > 100 then
+    			--if performance == true then
+    			--	EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 0.3*(RTime/0.01)
+    			--end
+    			--SetTimeScale(0.01)
+    			RedTrack = middle
+    			local rotarted = QuatLookAt(Vec(0,0,0),TransformToParentVec(cam, Vec(0,0,-1)))
+    			local campos = VecAdd(middle,Vec(0,5*math.sin((bich+42)/30)+8,0))
+    			local c1,c2,c3 = GetQuatEuler(QuatLookAt(campos,middle))
+    			local ccam = Transform(VecAdd(campos,Vec(0,0.2,0)),QuatEuler(-90,0,0))
+    			SetCameraTransform(ccam)
+    			DrawSprite(circle,Transform(VecAdd(middle,VecScale(Vec(0,-3,0),1)),QuatEuler(-90,-180,0)), 100, 100, 0, 0, 0, 1,true,false)
+    			--DrawSprite(ripple2,Transform(VecAdd(middle,Vec(0,10-bich/200,0)),QuatEuler(-90,-180,0)), 5, 5, 0.6, 0, 1, 1,false,false)
+    			PointLight(campos,1,1,1,5)
+    			if bich < 200 and bich > 190 then
+    				for i = 1, 10 do
+    					s = VecAdd(middle,VecScale(RVec(),rand(-Str/6,Str/6)))
+    					local e = VecAdd(campos,VecScale(RVec(),rand(Str/2,Str)))
+    					local last = s
+    					for i=1, 10 do
+    						local tt = i/10
+    						local p = VecLerp(s, e, tt)
+    						p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
+    						DrawLine(last, p, 1, 1, 1)
+    						last = p
+    					end
+    				end
+    				for i = 0, 1000, 1 do
+    					if #dcirc < 1000 then
+    						dcirc[#dcirc+1] = QuatEuler(rand(-180,180),rand(-180,180),rand(-180,180))
+    						ctime[#ctime+1] = rand(-160,200)
+    					end
+    				end
+    				--if bich < 200 and bich > 190 then
+
+    				--end
+    				--DrawSprite(circle,Transform(VecAdd(campos,Vec(0,-4,0)),QuatEuler(c1,c2,c3)),10,10,0,0,0,1,true,false)
+    			end
+
+    			PNuke = false
+    			Str = 16
+    			if bich <= 150 then
+    				RVel = Vec(0,0,0)
+    				for i = 1, #dcirc, 1 do
+    					ctime[i] = ctime[i] - 0.1*(RTime)
+    					c = ctime[i]
+    					cspace = VecScale(QuatRotateVec(dcirc[i],Vec(math.cos(160/(c/10))*(c/120),0,math.sin(160/(c/10))*(c/120))),Str/10)
+    					DrawSprite(circle, Transform(VecAdd(RedTrack,cspace),rotarted), (0.1),(0.1), math.abs(ctime[i])/60+0.6, 0.6, math.abs(ctime[i])/60+0.6, 1,true,true)
+    					if ctime[i]<= -160 then
+    						ctime[i] = 200
+    					end
+    				end
+    			end
+    		end
+    		QueryRequire("static")
+    		local h,d,n = QueryRaycast(VecAdd(VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4)),VecScale(Vec(0,1,0),Str/12)),Vec(0,-1,0),Str/3)
+    		if bich <= 100 then
+    			--EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer + 0.5*RTime
+    			--h = true
+    			if h then
+    				--RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4))
+    				--RedTrack = VecAdd(VecAdd(VecAdd(VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4)),VecScale(Vec(0,1,0),Str/12)),VecScale(Vec(0,-VecSub(RedTrack,Feet.pos)[2]-1,0),1)),VecScale(Vec(0,1,0),Str/20))
+    				RedTrack = VecAdd(VecSub(origin,Vec(0,0.2-Str/20,0)),VecScale(Vec(dir[1],0,dir[3]),Str/4))
+    				RVel = VecScale(pvel,0.018)
+    			else
+    			RedTrack = VecAdd(VecSub(origin,Vec(0,0.2,0)),VecScale(dir,Str/4))
+    			RVel = Vec(0,0,0)
+    			end
+    			PNuke = true
+    			if bich < 100 and bich > 95 then
+    				Str = 0
+
+    			end
+    			if bich < 100 then
+    				if performance == true then
+    					Str = Str+0.4*(bich/100)*RTime
+    				else
+    					Str = Str+0.4*(bich/100)
+    				end
+    				if InputDown(GetString("savegame.mod.inf.sadd")) then
+    					Str = Str + 1
+    				end
+    				if InputDown(GetString("savegame.mod.inf.ssub")) then
+    					Str = Str - 1
+    				end
+    			end
+    		end
+    		--DebugPrint(bich)
+    		if bich <= 5 then
+    			PointLight(RedTrackD,0.8,0.4,1,Str*2000)
+    			PointLight(RedTrackD,0.8,0.4,1,Str*2000)
+    			DrawSprite(star, Transform(RedTrackD,cam.rot), rand(Str/1.2,Str/0.8), rand(Str/1.2,Str/0.8), 1, 1, 1, 1,false,false)
+    		end
+    		if bich <= 1 then
+    			if h then
+    				RVel = VecScale(Vec(dir[1],0,dir[3]),1)
+    			else
+    				RVel = VecScale(dir,1)
+    			end
+    			--DebugPrint("done")
+    			pshart = true
+    			PNuke = true
+    			--bich = 0
+    			EntireAssFuckingCutsceneTypeAnimationTimer = 0
+    			PlaySound(pShot,RedTrack,1,false,10)
+    		end
+    	end
+end
+
+function client.update(dt)
+    if GetString("game.player.tool") == "INFINITY" then
+    	--Gravity stuffs at the red and blue (purple too)
+    	BROTIME = BROTIME + 1
+    	if BROTIME >= 360 then
+    		BROTIME = 0
+    	end
+    	--Red
+    	if SRed and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
+    		if Burnout == 0 then
+    			if PNuke == false then
+    				if InputDown("grab") then
+    					RedStr = RedStr + 0.1
+    				end
+    			end
+    		end
+    	end
+    	if SBlue and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
+    		if Burnout == 0 then
+    			if PNuke == false then
+    				if InputDown("usetool") then
+    					BluStr = BluStr + 0.1
+    				end
+    			end
+    		end
+    	end
+    end
+    	if SRed and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
+    		if Burnout == 0 then
+    			if PNuke == false then
+    				RSP = VecLength(VecScale(RVel,1))
+    				for i = 0, RSP,0.1 do
+    					RedTrackD = VecAdd(RedTrack,VecScale(RVel,i))
+    					if RedStr > 0.5 then
+    						--Shoot(RedTrackD,VecNormalize(RVel),"shotgun",RedStr/4,0.1)
+    						--if telek == true then
+    						--	Shoot(RedTrackD,VecNormalize(RVel),"shotgun",RedStr/4,0.1)
+    						--end
+    					else
+
+    						--GDrag(RedTrackD,VecScale(RVel,1/0.018),1)
+    					end
+    				end
+    				if not telek then
+    					Gravity(RedTrackD,-RedStr,RedStr/2)
+    				end
+    				if performance == true then
+    					if SBlue == true then
+    						for i = 1,100,1 do
+    							local gdis = VecScale(VecNormalize(RVec()),rand(RedStr/20,RedStr/9.5))
+    							local gspawn = VecAdd(RedTrack,gdis)
+    							ParticleType("plain")
+    							ParticleTile(4)
+    							ParticleColor(1,1,1,1,0,0)
+    							ParticleRadius(RedStr/90)
+    							ParticleAlpha(0.9,0)
+    							ParticleGravity(0)
+    							ParticleDrag(0)
+    							ParticleEmissive(10)
+    							ParticleRotation(rand(-10,10))
+    							ParticleCollide(0)
+    							local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    							local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    							local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
+    							SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-RedStr/3)),0.1)
+    						end
+    						for i = 1,500,1 do
+    							local gdis = VecScale(VecNormalize(RVec()),rand(RedStr/8,RedStr/9))
+    							local gspawn = VecAdd(RedTrack,gdis)
+    							ParticleType("plain")
+    							ParticleTile(5)
+    							ParticleColor(1,0.3,0.3,1,0,0)
+    							ParticleRadius(RedStr/80)
+    							ParticleAlpha(0,0.9)
+    							ParticleGravity(0)
+    							ParticleDrag(0)
+    							ParticleEmissive(1)
+    							ParticleRotation(rand(-10,10))
+    							ParticleCollide(0)
+    							local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    							local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
+    							SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-RedStr/3)),0.1)
+    						end
+    						if telek == false and (RedStr < 80 and performance) then
+    							for i = 0, 1, 1 do
+    								local gspawn = RedTrack
+    								ParticleType("plain")
+    								ParticleTile(4)
+    								ParticleColor(1,0.5,0.5,1,0,0)
+    								ParticleRadius(RedStr/7)
+    								ParticleAlpha(0.3,0)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(1)
+    								ParticleRotation(100)
+    								ParticleCollide(0)
+    								SpawnParticle(gspawn,VecScale(RVel,1/0.01),0.15)
+    							end
+    						end
+    					else
+    						for i = 1,100,1 do
+    							local gdis = VecScale(VecNormalize(RVec()),rand(1/20,1/6.5))
+    							local gspawn = VecAdd(RedTrack,gdis)
+    							ParticleType("plain")
+    							ParticleTile(4)
+    							ParticleColor(1,1,1,1,0,0)
+    							ParticleRadius(1/90)
+    							ParticleAlpha(0.9,0)
+    							ParticleGravity(0)
+    							ParticleDrag(0)
+    							ParticleEmissive(10)
+    							ParticleRotation(rand(-10,10))
+    							ParticleCollide(0)
+    							local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    							local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    							local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
+    							SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-1/3)),0.1)
+    						end
+    						for i = 1,500,1 do
+    							local gdis = VecScale(VecNormalize(RVec()),rand(1/8,1/6))
+    							local gspawn = VecAdd(RedTrack,gdis)
+    							ParticleType("plain")
+    							ParticleTile(5)
+    							ParticleColor(1,0,0,1,0,0)
+    							ParticleRadius(1/80)
+    							ParticleAlpha(0,0.9)
+    							ParticleGravity(0)
+    							ParticleDrag(0)
+    							ParticleEmissive(1)
+    							ParticleRotation(rand(-10,10))
+    							ParticleCollide(0)
+    							local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    							local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
+    							SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-1/3)),0.1)
+    						end
+    						--[[
+    						for i = 1,60,1 do
+    							local gdis = VecScale(VecNormalize(RVec()),rand(1/8,1/6))
+    							local gspawn = VecAdd(RedTrack,gdis)
+    							ParticleType("plain")
+    							ParticleTile(5)
+    							ParticleColor(1,0.3,0.3,1,0,0)
+    							ParticleRadius(1/80)
+    							ParticleAlpha(0,0.9)
+    							ParticleGravity(0)
+    							ParticleDrag(0)
+    							ParticleEmissive(1)
+    							ParticleRotation(rand(-10,10))
+    							ParticleCollide(0)
+    							local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    							local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(0,0,-2))))
+    							SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-1/3)),0.1)
+    						end
+    						]]
+    						if (RedStr < 80 and performance) then
+    							for i = 0, 1, 1 do
+    								local gspawn = RedTrack
+    								ParticleType("plain")
+    								ParticleTile(4)
+    								ParticleColor(1,0.5,0.5,1,0,0)
+    								ParticleRadius(1/7)
+    								ParticleAlpha(0.3,0)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(RedStr)
+    								ParticleRotation(100)
+    								ParticleCollide(0)
+    								SpawnParticle(gspawn,VecScale(RVel,1/0.01),0.15)
+    							end
+    						end
+    					end
+    				end
+    			end
+    		end
+    	end
+    	if SBlue == true and EntireAssFuckingCutsceneTypeAnimationTimer == 0 then
+    		if Burnout == 0 then
+    			if PNuke == false then
+    				if performance == true then
+    					if BluStr < 80 and not telek then
+    						if SRed == false then
+    							for i = 1,100,1 do
+    								local gdis = VecScale(VecNormalize(RVec()),rand(0.01,BluStr/15))
+    								local gspawn = VecAdd(BlueTrack,gdis)
+    								ParticleType("plain")
+    								ParticleTile(4)
+    								ParticleColor(1,1,1,0,0,1)
+    								ParticleRadius(BluStr/400)
+    								ParticleAlpha(0.9,0)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(10)
+    								ParticleRotation(rand(-10,10))
+    								ParticleCollide(0)
+    								local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    								local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
+    								local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0.5)))
+    								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-BluStr/3)),0.2)
+    							end
+    							for i = 1,100,1 do
+    								local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/8,BluStr/5))
+    								local gspawn = VecAdd(BlueTrack,gdis)
+    								ParticleType("plain")
+    								ParticleTile(5)
+    								ParticleColor(0.2,1,0.8,0,0,1)
+    								ParticleRadius(BluStr/50)
+    								ParticleAlpha(0,0.5)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(1)
+    								ParticleRotation(rand(-10,10))
+    								ParticleCollide(0)
+    								local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
+    								local spidir = TransformToParentVec(look, Vec(-1,-1,0))
+    								--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.018),VecScale(gdis,-3)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.25)
+    								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,-3)),VecScale(VecScale(spidir,BluStr/10/VecLength(gdis)),BluStr/2)),0.2)
+    							end
+    							for i = 1,100,1 do
+    								local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/8,BluStr/5))
+    								local gspawn = VecAdd(BlueTrack,gdis)
+    								ParticleType("plain")
+    								ParticleTile(5)
+    								ParticleColor(0.2,1,0.8,0,0,1)
+    								ParticleRadius(BluStr/50)
+    								ParticleAlpha(0,0.5)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(1)
+    								ParticleRotation(rand(-10,10))
+    								ParticleCollide(0)
+    								local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
+    								local spidir = TransformToParentVec(look, Vec(1,1,0))
+    								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,-3)),VecScale(VecScale(spidir,BluStr/10/VecLength(gdis)),BluStr/2)),0.2)
+    							end
+    						else
+    							for i = 1,100,1 do
+    								local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/20,BluStr/9))
+    								local gspawn = VecAdd(BlueTrack,gdis)
+    								ParticleType("plain")
+    								ParticleTile(4)
+    								ParticleColor(1,1,1,0,0,1)
+    								ParticleRadius(BluStr/90)
+    								ParticleAlpha(0.9,0)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(10)
+    								ParticleRotation(rand(-10,10))
+    								ParticleCollide(0)
+    								local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    								local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
+    								local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
+    								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-BluStr/3)),0.1)
+    							end
+    							for i = 1,500,1 do
+    								local gdis = VecScale(VecNormalize(RVec()),rand(BluStr/8,BluStr/9))
+    								local gspawn = VecAdd(BlueTrack,gdis)
+    								ParticleType("plain")
+    								ParticleTile(5)
+    								ParticleColor(0.3,0.8,1,0,0,1)
+    								ParticleRadius(BluStr/80)
+    								ParticleAlpha(0,0.9)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(1)
+    								ParticleRotation(rand(-10,10))
+    								ParticleCollide(0)
+    								local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
+    								local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
+    								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-BluStr/3)),0.1)
+    							end
+    						end
+    						for i = 1,50,1 do
+    							local gdis = VecScale(VecNormalize(RVec()),rand(BluStr,BluStr*5))
+    							local gspawn = VecAdd(BlueTrack,gdis)
+    							ParticleType("plain")
+    							ParticleTile(5)
+    							ParticleColor(1,1,1)
+    							ParticleRadius(BluStr/80)
+    							ParticleAlpha(0,1)
+    							ParticleGravity(0)
+    							ParticleDrag(0)
+    							ParticleEmissive(0)
+    							ParticleRotation(rand(-10,10))
+    							local look = Transform(BlueTrack,QuatLookAt(BlueTrack,gspawn))
+    							local spidir = TransformToParentVec(look, Vec(-1,1,0))
+    							SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(BVel,1/0.01),VecScale(gdis,-3)),VecScale(VecScale(spidir,BluStr/11/VecLength(gdis)),BluStr/3)),0.2)
+    						end
+    						if telek == false and (BluStr < 80 and performance) then
+    							for i = 0, 1, 1 do
+    								local gspawn = BlueTrack
+    								ParticleType("plain")
+    								ParticleTile(4)
+    								ParticleColor(0.5,1,1,0,0,1)
+    								ParticleRadius(BluStr/7)
+    								ParticleAlpha(0.3,0)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(1)
+    								ParticleRotation(100)
+    								ParticleCollide(0)
+    								SpawnParticle(gspawn,VecScale(BVel,1/0.01),0.15)
+    							end
+    						end
+    					end
+    					if telek or BluesMerge then
+    						for j = 1, #smbt do
+    							for i = 0,30,1 do
+    								local gdis = VecScale(VecNormalize(RVec()),rand(5/20,5/9))
+    								local gspawn = VecAdd(smbt[j],gdis)
+    								ParticleType("plain")
+    								ParticleTile(4)
+    								ParticleColor(1,1,1,0,0,1)
+    								ParticleRadius(5/90)
+    								ParticleAlpha(0.9,0)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(10)
+    								ParticleRotation(rand(-10,10))
+    								ParticleCollide(0)
+    								local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    								local look = Transform(smbt[j],QuatLookAt(smbt[j],gspawn))
+    								local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),-0.5)))
+    								SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(smbv[j],1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,2),-5/3)),0.1)
+    							end
+    							for i = 0, 1, 1 do
+    								local gspawn = smbt[j]
+    								ParticleType("plain")
+    								ParticleTile(4)
+    								ParticleColor(0.3,0.8,1,0,0,1)
+    								ParticleRadius(5/6)
+    								ParticleAlpha(0.9,0)
+    								ParticleGravity(0)
+    								ParticleDrag(0)
+    								ParticleEmissive(1)
+    								ParticleRotation(100)
+    								ParticleCollide(0)
+    								SpawnParticle(gspawn,VecScale(smbv[j],1/0.01),0.15)
+    							end
+    						end
+    					end
+    				end
+    				--if InputDown("q") == false then
+    				if telek == false then
+    					QueryRequire("dynamic")
+    					local shit = QueryClosestPoint(BlueTrack,BluStr)
+    					if BluStr > 8 then
+    						Shoot(BlueTrack,Vec(0,0,0),"shotgun",BluStr/2,0.005)
+    					else
+    						GDrag(BlueTrack,VecScale(BVel,1/0.015),0.001)
+    					end
+    					if shit == false then
+    						for i = 0,VecLength(BVel),0.1 do
+    							local BTS = VecAdd(BlueTrack,VecScale(BVel,i))
+    							if BluStr > 8 then
+    								MakeHole(BTS,BluStr/5,BluStr/5,BluStr/5)
+    							end
+    						end
+    					end
+    					Gravity(BlueTrack,BluStr,BluStr)
+    				end
+    				if telek or BluesMerge then
+    					if not InputDown(GetString("savegame.mod.inf.grab")) and ShotBlueTime ~= 0 then
+    						ShotBlueTime = ShotBlueTime - 1
+    					end
+    					for j = 1, #smbt do
+    						for i = 0,VecLength(smbv[j]),0.2 do
+    							local BTS = VecAdd(smbt[j],VecScale(smbv[j],i))
+    							local shit = QueryClosestPoint(BTS,0.9)
+    							if shit then
+    								Shoot(BTS,Vec(0,0,0),"shotgun",5/2,0.005)
+    								MakeHole(BTS,0.8,0.8,0.8)
+    							end
+    						end
+    						Gravity(smbt[j],2,2)
+    					end
+    				end
+    				--end
+    			end
+    		end
+    	end
+    	if (SRed and SBlue) then
+    		if VecLength(VecSub(RedTrack,BlueTrack)) < Str/5 then
+    			if performance == true then
+    				Blight = VecAdd(VecScale(VecSub(BlueTrack,RedTrack),0.5),RedTrack)
+    				for i = 1,50,1 do
+    					local gdis = VecScale(VecNormalize(RVec()),Str/3)
+    					local gspawn = VecAdd(Blight,gdis)
+    					ParticleType("plain")
+    					ParticleTile(5)
+    					ParticleColor(1,0,0)
+    					ParticleRadius(Str/80)
+    					ParticleAlpha(0,1)
+    					ParticleGravity(0)
+    					ParticleDrag(0)
+    					ParticleEmissive(1)
+    					ParticleRotation(rand(-10,10))
+    					local look = Transform(Blight,QuatLookAt(Blight,gspawn))
+    					local spidir = TransformToParentVec(look, Vec(0,0,-1))
+    					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),1/0.01),VecScale(gdis,5)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.5)
+    				end
+    				for i = 1,50,1 do
+    					local gdis = VecScale(VecNormalize(RVec()),Str/3)
+    					local gspawn = VecAdd(Blight,gdis)
+    					ParticleType("plain")
+    					ParticleTile(5)
+    					ParticleColor(0,0.4,1)
+    					ParticleRadius(Str/80)
+    					ParticleAlpha(0,1)
+    					ParticleGravity(0)
+    					ParticleDrag(0)
+    					ParticleEmissive(1)
+    					ParticleRotation(rand(-10,10))
+    					local look = Transform(Blight,QuatLookAt(Blight,gspawn))
+    					local spidir = TransformToParentVec(look, Vec(0,0,-1))
+    					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),1/0.01),VecScale(gdis,5)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.5)
+    				end
+    			end
+    		end
+    	end
+    	if PNuke == true and (InputDown(GetString("savegame.mod.inf.time")) == false or honored == false) then
+    		if NukeTime == 0 then
+    			--DebugPrint((VecLength(RVel)/time))
+    			local bzzt = QueryAabbShapes(VecAdd(RedTrack,Vec(-Str,-Str,-Str)),VecAdd(RedTrack,Vec(Str,Str,Str)))
+    			for i=1,#bzzt do
+    				if rand(0,10) > 9.9 then
+    					local hit, e = GetShapeClosestPoint(bzzt[i],RedTrack)
+    					--e = GetShapeWorldTransform(bzzt[i]).pos
+    					s = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/6,Str/6)))
+    					--Draw laser line in ten segments with random offset, stolen from teardown lazer gun built-in-mod
+    					local last = s
+    					for i=1, 15 do
+    						local tt = i/15
+    						local p = VecLerp(s, e, tt)
+    						p = VecAdd(p, VecScale(VecNormalize(RVec()),(1.2*tt)))
+    						DrawLine(last, p, 1, 1, 1)
+    						last = p
+    					end
+    				end
+    			end
+    			if rand(0,10) > 9.9 then
+    				for i = 1, 2 do
+    					s = VecAdd(RedTrack,VecScale(RVec(),rand(-Str/6,Str/6)))
+    					local e = VecAdd(RedTrack,VecScale(RVec(),rand(Str/2,Str)))
+    					local last = s
+    					for i=1, 10 do
+    						local tt = i/10
+    						local p = VecLerp(s, e, tt)
+    						p = VecAdd(p, VecScale(VecNormalize(RVec()),(1*tt)))
+    						DrawLine(last, p, 1, 1, 1)
+    						last = p
+    					end
+    				end
+    			end
+    			if Str > 8 then
+    				if honored == false and InputDown(GetString("savegame.mod.inf.time")) == false then
+    					Gravity(RedTrack,Str*4,Str*0.3,_)
+    				end
+    				if performance == true then
+    					for i = 1,50,1 do
+    						local gdis = VecScale(VecNormalize(RVec()),rand(Str/7,Str*3))
+    						local gspawn = VecAdd(RedTrack,gdis)
+    						ParticleType("plain")
+    						ParticleTile(5)
+    						ParticleColor(1,1,1)
+    						ParticleRadius(Str/40)
+    						ParticleAlpha(0,1)
+    						ParticleGravity(0)
+    						ParticleDrag(0)
+    						ParticleEmissive(1)
+    						ParticleRotation(rand(-10,10))
+    						local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    						local spidir = TransformToParentVec(look, Vec(0,0,-1))
+    						SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,-3)),VecScale(VecScale(spidir,Str/11/VecLength(gdis)),Str/3)),0.25)
+    					end
+    				end
+    			end
+    			if performance == true then
+    				for i = 1,100,1 do
+    					local gdis = VecScale(VecNormalize(RVec()),rand(Str/20,Str/8))
+    					local gspawn = VecAdd(RedTrack,gdis)
+    					ParticleType("plain")
+    					ParticleTile(4)
+    					ParticleColor(1,1,1,0.5,0,1)
+    					ParticleRadius(Str/90)
+    					ParticleAlpha(0.9,0)
+    					ParticleGravity(0)
+    					ParticleDrag(0)
+    					ParticleEmissive(1000)
+    					ParticleRotation(rand(-10,10))
+    					ParticleCollide(0)
+    					local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    					local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    					local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),-0.5)))
+    					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-Str/3)),0.2)
+    				end
+    				for i = 1,500,1 do
+    					local gdis = VecScale(VecNormalize(RVec()),rand(Str/8,Str/7))
+    					local gspawn = VecAdd(RedTrack,gdis)
+    					ParticleType("plain")
+    					ParticleTile(5)
+    					ParticleColor(1,0.8,1,0.8,0,1)
+    					ParticleRadius(Str/80)
+    					ParticleAlpha(0,0.9)
+    					ParticleGravity(0)
+    					ParticleDrag(0)
+    					ParticleEmissive(1)
+    					ParticleRotation(rand(-10,10))
+    					ParticleCollide(0)
+    					local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    					local spidir = QuatRotateVec(QuatEuler(0,0,0),TransformToParentVec(look, VecNormalize(Vec(-1,rand(-1,1),0))))
+    					SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.01),VecScale(gdis,0)),VecScale(VecScale(spidir,1),-Str/3)),0.2)
+    				end
+    				--if (Str < 80 and performance) then
+    					for i = 0, 1, 1 do
+    						local gspawn = RedTrack
+    						ParticleType("plain")
+    						ParticleTile(4)
+    						ParticleColor(1,0.8,1,0.8,0,1)
+    						ParticleRadius(Str/7)
+    						ParticleAlpha(0.3,0)
+    						ParticleGravity(0)
+    						ParticleDrag(0)
+    						ParticleEmissive(10)
+    						ParticleRotation(100)
+    						ParticleCollide(0)
+    						SpawnParticle(gspawn,VecScale(RVel,1/0.01),0.15)
+    					end
+    				--end
+    			end
+    		end
+    		if NukeTime ~= 0 then
+    			NukeS = (Str/3)/NukeTime
+
+    			Gravity(RedTrack,-NukeS*60,NukeS,"dynamic")
+    			Destroy(RedTrack,NukeS*0.5,true,0,0,NukeS*0.5)
+    			Destroy(RedTrack,NukeS*0.5,true,0,0,NukeS*0.5)
+    			if performance == true then
+    				for i = 1,500,1 do
+    					local gdis = VecScale(VecNormalize(RVec()),NukeS/1.5)
+    					local gspawn = VecAdd(RedTrack,gdis)
+    					ParticleType("plain")
+    					ParticleTile(4)
+    					ParticleColor(1,1,1,0.4,0,1)
+    					ParticleRadius(NukeS/30)
+    					ParticleAlpha(1,0)
+    					ParticleGravity(0)
+    					ParticleDrag(1)
+    					ParticleEmissive(1)
+    					ParticleRotation(rand(-10,10))
+    					ParticleCollide(0)
+    					local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    					local spidir = TransformToParentVec(look, Vec(-1,0,0))
+    					SpawnParticle(gspawn,VecAdd(VecAdd(Vec(0,0,0),VecScale(gdis,5)),VecScale(VecScale(spidir,1),-Str/3)),0.1)
+    				end
+    				if NukeTime < 0.15 then
+    					for i = 1,1000,1 do
+    						local gdis = VecScale(VecNormalize(RVec()),NukeS/1.5)
+    						local gspawn = VecAdd(RedTrack,gdis)
+    						ParticleType("plain")
+    						ParticleTile(5)
+    						ParticleColor(1,1,1,0.4,0,1)
+    						ParticleRadius(NukeS/40)
+    						ParticleAlpha(1,0)
+    						ParticleGravity(0)
+    						ParticleDrag(0)
+    						ParticleEmissive(1)
+    						ParticleRotation(rand(-10,10))
+    						ParticleCollide(0)
+    						local look = Transform(RedTrack,QuatLookAt(RedTrack,gspawn))
+    						local spidir = TransformToParentVec(look, Vec(-1,0,0))
+    						SpawnParticle(gspawn,VecAdd(Vec(0,0,0),VecScale(VecScale(spidir,1),-Str/3)),1)
+    					end
+    				end
+    			end
+
+    			NukeTime = NukeTime -0.05
+    			if NukeTime < 0.1 then
+    				PNuke = false
+    				NRelease = false
+    				NukeTime = 0
+    			end
+    		end
+    	end
+    if DomActivate > 1 then
+    		DomActivate = DomActivate - 1
+    		--DebugPrint(DomActivate)
+    		--local hit, dis, gp = QueryRaycast(origin,dir,10)
+    --balls
+    		for i = -1,1,0.3 do
+    			for j = -1,1,0.3 do
+
+    				local GDir = QuatRotateVec(DPR,VecNormalize(Vec(i,j,0)))
+    				--local GDir = Vec(i,j,k)
+    				--local hit, dis, gp = QueryRaycast(origin,GDir,10)
+    				local what = ((DomActivate)/10/math.pi)
+    				--DebugPrint(math.sin(what))
+    				local gspawn = VecAdd(VecAdd(DPP,VecScale(DPD,(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
+    				--local gspawn = VecAdd(VecAdd(Feet.pos,VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
+    				ParticleType("plain")
+    				ParticleTile(3)
+    				ParticleColor(1,1,1)
+    				ParticleRadius(3)
+    				ParticleAlpha(1)
+    				ParticleGravity(0)
+    				ParticleDrag(0)
+    				ParticleEmissive(1)
+    				ParticleRotation(0)
+    				ParticleCollide(0)
+    				SpawnParticle(gspawn,Vec(0,0,0),3)
+    				PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
+    			end
+    		end
+
+    		for i = -1,1,0.3 do
+    			for j = -1,1,0.3 do
+
+    				local GDir = VecNormalize(Vec(i,j,0))
+    				--local GDir = Vec(i,j,k)
+    				--local hit, dis, gp = QueryRaycast(origin,GDir,10)
+    				local what = ((DomActivate)/10/math.pi)
+    				--DebugPrint(math.sin(what))
+    				--local gspawn = VecAdd(VecAdd(origin,VecScale(dir,(50-DomActivate)/10)),VecScale(GDir,20*math.sin(what)))
+    				local gspawn = VecAdd(VecAdd(VecAdd(DPP,Vec(0,10000,0)),VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
+    				ParticleType("plain")
+    				ParticleTile(3)
+    				ParticleColor(1,1,1)
+    				ParticleRadius(3)
+    				ParticleAlpha(1)
+    				ParticleGravity(0)
+    				ParticleDrag(0)
+    				ParticleEmissive(1)
+    				ParticleRotation(0)
+    				ParticleCollide(0)
+    				SpawnParticle(gspawn,Vec(0,0,0),1.5)
+    				PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
+    			end
+    		end
+    	end
+    if DomainToggle == true then
+    	--SetShapeBody(ovoid,GetWorldBody(),Transform(VecAdd(DPP,Vec(-10,0,10)),QuatEuler(-90,0,0)))
+    	SetBodyTransform(voidb,Transform(VecAdd(DomainPos,Vec(0,-1,0)),QuatEuler(0,0,0)))
+    	SetBodyVelocity(voidb,Vec(0,0,0))
+    	SetBodyAngularVelocity(voidb,Vec(0,0,0))
+    	--DebugTransform(GetBodyTransform(voidb))
+    	DrawBodyHighlight(voidb,1)
+
+    	SetBodyTransform(ovoidb,Transform(VecAdd(DPP,Vec(0,-1,0)),QuatEuler(0,0,0)))
+    	SetBodyVelocity(ovoidb,Vec(0,0,0))
+    	SetBodyAngularVelocity(ovoidb,Vec(0,0,0))
+    	DrawBodyHighlight(ovoidb,1)
+    	--DebugCross(GetBodyTransform(ovoidb).pos)
+    	SetPostProcessingProperty("brightness",2)
+    	if GetPlayerHealth(playerId) > HP then
+    		HP = GetPlayerHealth(playerId)
+    	end
+    	SetPlayerHealth(playerId, HP)
+    	SetPlayerParam("GodMode",true)
+    	QueryRejectBody(voidb)
+    	local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-20,-50)),VecAdd(DomainPos,Vec(50,50,50)))
+    	for i = 1, #dbodies do
+    		local dbody = dbodies[i]
+    		if IsBodyDynamic(dbody) then
+    			jbodies = GetJointedBodies(dbody)
+    			for j = 1,#jbodies do
+    				local jbody = jbodies[j]
+    				local add = true
+    				for k = 1, #dbodies do
+    					if jbody == dbodies[k] then
+    						add = false
+    					end
+    				end
+    				if add then
+    					dbodies[#dbodies+1] = jbody
+    				end
+    			end
+    		end
+    	end
+    	--makes everything in the domain stop thinking (only works with teardown robots as of now)
+    	for i = 1, #dbodies do
+    		local dbody = dbodies[i]
+    		if not HasTag(dbody, "sleeping") then
+    			SetTag(dbody, "sleeping")
+    		end
+    	end
+    	-- my feeble attempts to temporarily lobotomize the AUTUMNATIC zombies, mostly just code ripped straight from that mod
+
+    	if DsTimer >= 1 then 
+    		DsTimer = DsTimer + 1
+    		for i = 1,5, 1 do
+    			local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,rand(-200,200))),VecScale(VecNormalize(Vec(rand(-1,1),rand(-1,1),0)),40))
+    			ParticleType("plain")
+    			ParticleTile(1)
+    			ParticleColor(1,1,1)
+    			ParticleRadius(5)
+    			ParticleAlpha(0,1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(1)
+    			ParticleRotation(0)
+    			--SpawnParticle(gspawn,VecScale(Vec(0,0,1),-20),2)
+    		end
+    	end
+    	--when the wackass lines end
+    	if DsTimer > 200 then
+    		DsTimer = 0
+    		--white shit on the screen
+    		for i = 1,20,1 do
+    			local gspawn = VecAdd(DomainPos,VecScale(VecNormalize(RVec()),rand(20,40)))
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			ParticleColor(1,1,1)
+    			ParticleRadius(7)
+    			ParticleAlpha(1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(1)
+    			ParticleRotation(0)
+
+    			--SpawnParticle(gspawn,Vec(0,0,0),100)
+    		end
+    		fogtimer = 600
+    	end
+    	if DsTimer == 0 then
+    		--local dbodies = QueryAabbBodies(VecAdd(DomainPos,Vec(-50,-20,-50)),VecAdd(DomainPos,Vec(50,50,50)))
+    		--for i = 1, #dbodies do
+    		--	local dbody = dbodies[i]
+    		--	if IsBodyDynamic(dbody) then
+    				--SetTag(dbody, "inactive")
+    				--dtran = GetBodyTransform(dbody)
+    				--Shoot(dtran.pos,Vec(0,1,0),"shotgun",-1,0.01)
+    				--DebugPrint(ListTags(dbody))
+    		--	end
+    		--end
+    		local BHoleD = VecNormalize(VecSub(BHolePos,DomainPos))
+    		local BHoleDP = VecAdd(BHolePos,VecScale(BHoleD,9))
+    		--VisChain(BHoleDP,100,1,1,1,1,0.7,0.4,60,60,false,1,Vec(0,0,0),cam,false)
+    		--VisChain(BHoleDP,100,1,1,1,1,1,1,60,60,false,1,Vec(-1,0,0),cam,false)
+    		--PointLight(VecAdd(BHolePos,),1,1,1,1000)
+
+    		--complex ass fog (not really)
+    		for i = 1,40,1 do
+    			local gdis = VecScale(VecNormalize(Vec(rand(0,1),0,rand(-1,1))),130)
+    			local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,10,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			ParticleColor(rand(0.75,0.8),rand(0.85,0.9),1)
+    			ParticleRadius(5,rand(10,30))
+    			ParticleAlpha(1,0)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(0.5,0)
+    			ParticleCollide(1)
+    			ParticleRotation(0)
+    			local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(-2,rand(-5,5),0))
+    			--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),0.1)
+    			SpawnParticle(gspawn,VecScale(spidir,2),2)
+    		end
+    		for i = 1,40,1 do
+    			local gdis = VecScale(VecNormalize(Vec(rand(0,-1),0,rand(-1,1))),130)
+    			local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,10,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			ParticleColor(rand(0.75,0.8),rand(0.85,0.9),1)
+    			ParticleRadius(5,rand(10,30))
+    			ParticleAlpha(1,0)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(0.5,0)
+    			ParticleCollide(1)
+    			ParticleRotation(0)
+    			local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(2,rand(-5,5),0))
+    			--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),0.1)
+    			SpawnParticle(gspawn,VecScale(spidir,2),2)
+    		end
+    		for i = 1,5,1 do
+    			local gdis = VecScale(VecNormalize(Vec(rand(0,-1),rand(-1,1),0)),15)
+    			local gspawn = VecAdd(VecAdd(BHolePos,Vec(0,0,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			ParticleColor(1,1,1)
+    			ParticleRadius(4)
+    			ParticleAlpha(0,1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(1)
+    			ParticleCollide(0)
+    			ParticleRotation(0)
+    			local look = Transform(BHolePos,QuatLookAt(BHolePos,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(0,2,0))
+    			--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
+    			SpawnParticle(gspawn,VecScale(spidir,1),1)
+    		end
+    		for i = 1,5,1 do
+    			local gdis = VecScale(VecNormalize(Vec(rand(0,1),rand(-1,1),0)),15)
+    			local gspawn = VecAdd(VecAdd(BHolePos,Vec(0,0,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			ParticleColor(1,1,1)
+    			ParticleRadius(4)
+    			ParticleAlpha(0,1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(1)
+    			ParticleCollide(0)
+    			ParticleRotation(0)
+    			local look = Transform(BHolePos,QuatLookAt(BHolePos,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(0,-2,0))
+    			--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
+    			SpawnParticle(gspawn,VecScale(spidir,1),1)
+    		end
+    		for i = 1,100,1 do
+    			local gdis = VecScale(VecNormalize(Vec(rand(-1,1),rand(-1,1),0)),40)
+    			local gspawn = VecAdd(VecAdd(BHolePos,Vec(0,0,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(4)
+    			ParticleColor(1,1,0.5,0.5,1,0.5)
+    			ParticleRadius(1,0)
+    			ParticleAlpha(1,1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(rand(0.5,1),0.1)
+    			ParticleCollide(0)
+    			ParticleRotation(0)
+    			local look = Transform(BHolePos,QuatLookAt(BHolePos,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(0,0,4))
+    			--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
+    			SpawnParticle(gspawn,VecScale(spidir,1),1)
+    		end
+    		for i = 1,50,1 do
+    			local gdis = VecScale(VecNormalize(RVec()),200)
+    			local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			ParticleColor(0.4,rand(0.5,0.9),1)
+    			ParticleRadius(rand(10,50),rand(1,50))
+    			ParticleAlpha(0,0.1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(rand(0,8),0)
+    			ParticleCollide(0)
+    			ParticleRotation(0)
+    			local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(0,0,3))
+    			--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
+    			SpawnParticle(gspawn,VecScale(spidir,1),4)
+    		end
+    		for i = 1,20,1 do
+    			local gdis = VecScale(VecNormalize(RVec()),160)
+    			local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			ParticleColor(0.1,0.1,0.1)
+    			ParticleRadius(rand(1,50),rand(1,50))
+    			ParticleAlpha(1,1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(0)
+    			ParticleCollide(0)
+    			ParticleRotation(0)
+    			local look = Transform(DomainPos,QuatLookAt(DomainPos,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(0,0,-0))
+    			--SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(RVel,1/0.018),VecScale(gdis,0)),VecScale(VecScale(spidir,Str/8/VecLength(gdis)),Str/3)),1)
+    			SpawnParticle(gspawn,VecScale(spidir,1),4)
+    		end
+    		for i = 1, 2,1 do
+    			local gdis = VecScale(Vec(rand(-80,80),rand(-80,80),rand(-80,80)),1)
+    			local gspawn = VecAdd(VecAdd(DomainPos,Vec(0,0,0)),gdis)
+    			ParticleType("plain")
+    			ParticleTile(1)
+    			ParticleColor(1,1,1)
+    			ParticleRadius(2)
+    			ParticleAlpha(0,1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(1)
+    			ParticleCollide(0)
+    			SpawnParticle(gspawn,VecScale(Vec(0,1,0),rand(0.1,1)),5)
+    		end
+    	end
+    	--Back in the regular world
+    	if false then --remove if wanted
+    		for i = -1,1,0.3 do
+    			for j = -1,1,0.3 do
+
+    				local GDir = QuatRotateVec(DPR,VecNormalize(Vec(i,j,0)))
+    				--local GDir = Vec(i,j,k)
+    				--local hit, dis, gp = QueryRaycast(origin,GDir,10)
+    				local what = ((rand(0,100))/10/math.pi)
+    				--DebugPrint(math.sin(what))
+    				local gspawn = VecAdd(VecAdd(DPP,VecScale(DPD,(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
+    				--local gspawn = VecAdd(VecAdd(Feet.pos,VecScale(Vec(0,0,-1),(10*math.cos(what)))),VecScale(GDir,10*math.sin(what)))
+    				ParticleType("plain")
+    				ParticleTile(3)
+    				ParticleColor(1,1,1)
+    				ParticleRadius(3)
+    				ParticleAlpha(1)
+    				ParticleGravity(0)
+    				ParticleDrag(0)
+    				ParticleEmissive(1)
+    				ParticleRotation(0)
+    				ParticleCollide(0)
+    				SpawnParticle(gspawn,Vec(0,0,0),0.8)
+    				--PlaySound(Brown,gspawn,rand(0,0.5),false,rand(1,10))
+    			end
+    		end
+    	end
+    end
+    if EntireAssFuckingCutsceneTypeAnimationTimer > 0 and honored == false then
+    	--if performance == true then
+    		EntireAssFuckingCutsceneTypeAnimationTimer = EntireAssFuckingCutsceneTypeAnimationTimer - 1
+    	--end
+    	local middle = Vec(0,1000,0)
+    	local borigin = VecAdd(origin,Vec(0,-0.5,0))
+    	local mid2 = VecAdd(borigin,VecScale(Vec(dir[1],0,dir[3]),-3))
+    	if bich > 350 then
+    		if bich < 490 and bich > 470 then
+
+    			for i = 1,5,1 do
+    				local gdis = VecScale(VecNormalize(RVec()),rand(1,1.2))
+    				local gspawn = VecAdd(VecAdd(VecAdd(mid2,VecScale(adderall,-1))),gdis)
+    				ParticleType("plain")
+    				ParticleTile(2)
+    				ParticleColor(1,1,1,0.8,0.8,1)
+    				ParticleRadius(0.1,0.2)
+    				ParticleAlpha(0,1)
+    				ParticleGravity(0)
+    				ParticleDrag(0)
+    				ParticleEmissive(10)
+    				ParticleRotation(rand(-10,10))
+    				ParticleCollide(0)
+    				local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    				local look = Transform(VecAdd(VecAdd(mid2,VecScale(adderall,-1))),QuatLookAt(VecAdd(VecAdd(mid2,VecScale(adderall,-1))),gspawn))
+    				local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),1)))
+    				SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),0),VecScale(gdis,0)),VecScale(VecScale(spidir,2),1)),0.6)
+    			end
+    		end
+    		if bich < 450 and bich > 420 then
+    			for i = 1,5,1 do
+    				local gdis = VecScale(VecNormalize(RVec()),rand(1,1.2))
+    				local gspawn = VecAdd(VecAdd(VecAdd(mid2,VecScale(adderall,1))),gdis)
+    				ParticleType("plain")
+    				ParticleTile(2)
+    				ParticleColor(1,1,1,1,0.8,0.8)
+    				ParticleRadius(0.1,0.2)
+    				ParticleAlpha(0,1)
+    				ParticleGravity(0)
+    				ParticleDrag(0)
+    				ParticleEmissive(10)
+    				ParticleRotation(rand(-10,10))
+    				ParticleCollide(0)
+    				local rotata = TransformToParentVec(cam, Vec(1,0,0))
+    				local look = Transform(VecAdd(VecAdd(mid2,VecScale(adderall,1))),QuatLookAt(VecAdd(VecAdd(mid2,VecScale(adderall,1))),gspawn))
+    				local spidir = TransformToParentVec(look, VecNormalize(Vec(-1,rand(-2,2),1)))
+    				SpawnParticle(gspawn,VecAdd(VecAdd(VecScale(Vec(0,0,0),0),VecScale(gdis,0)),VecScale(VecScale(spidir,2),1)),0.6)
+    			end
+    		end
+    		if bich > 400 then
+    			if bich <= 400 then
+    				for i = 1, 0 do
+    					local gdis = VecScale(RVec(),1.2)
+    					local gspawn = VecAdd(VecAdd(mid2,VecScale(adderall,1)),gdis)
+    					ParticleType("plain")
+    					ParticleTile(5)
+    					ParticleColor(1,0.5,0.5)
+    					ParticleRadius(0.3)
+    					ParticleAlpha(0.2,0.5)
+    					ParticleGravity(0)
+    					ParticleDrag(0)
+    					ParticleEmissive(1)
+    					ParticleCollide(1)
+
+    					SpawnParticle(gspawn,VecScale(adderall,1),1)
+    				end
+    			end
+    		end
+    	end
+    	if bich <= 350 and bich > 200 then
+    		local add2 = VecScale(Vec(-1,0,0),bich/1000)
+    		for i = 1,30,1 do
+    			local gdis = VecScale(VecNormalize(RVec()),rand(0.05,1))
+    			local gspawn = VecAdd(middle,gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			local b = VecLength(VecSub(gdis,VecAdd(add2,VecNormalize(add2))))
+    			local r = VecLength(VecSub(gdis,VecAdd(VecScale(add2,-1),VecNormalize(VecScale(add2,-1)))))
+    			--DebugPrint(b)
+    			ParticleColor(0,0,1)
+    			ParticleRadius(0.1)
+    			ParticleAlpha(1,0.2)
+    			ParticleGravity(0)
+    			ParticleDrag(0.2)
+    			ParticleEmissive(1)
+    			ParticleRotation(0)
+    			ParticleCollide(0)
+    			local look = Transform(middle,QuatLookAt(middle,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(1,0,0))
+    			if VecLength(VecSub(gspawn,VecAdd(add2,middle))) < 0.5 and VecLength(VecSub(gspawn,VecAdd(VecScale(add2,-1),middle))) < 0.5 then
+    				SpawnParticle(gspawn,VecAdd(VecScale(gdis,0),VecScale(VecScale(spidir,1/10/VecLength(gdis)),3/3)),0.5)
+    			else
+    				i = i - 1
+    			end
+    		end
+    		for i = 1,30,1 do
+    			local gdis = VecScale(VecNormalize(RVec()),rand(0.05,1))
+    			local gspawn = VecAdd(middle,gdis)
+    			ParticleType("plain")
+    			ParticleTile(5)
+    			local b = VecLength(VecSub(gdis,VecAdd(add2,VecNormalize(add2))))
+    			local r = VecLength(VecSub(gdis,VecAdd(VecScale(add2,-1),VecNormalize(VecScale(add2,-1)))))
+    			--DebugPrint(b)
+    			ParticleColor(1,0,0)
+    			ParticleRadius(0.1)
+    			ParticleAlpha(1,0.2)
+    			ParticleGravity(0)
+    			ParticleDrag(0.2)
+    			ParticleEmissive(1)
+    			ParticleRotation(0)
+    			ParticleCollide(0)
+    			local look = Transform(middle,QuatLookAt(middle,gspawn))
+    			local spidir = TransformToParentVec(look, Vec(1,0,0))
+    			if VecLength(VecSub(gspawn,VecAdd(add2,middle))) < 0.5 and VecLength(VecSub(gspawn,VecAdd(VecScale(add2,-1),middle))) < 0.5 then
+    				SpawnParticle(gspawn,VecAdd(VecScale(gdis,0),VecScale(VecScale(spidir,1/10/VecLength(gdis)),3/3)),0.5)
+    			else
+    				i = i-1
+    			end
+    		end
+    	end
+    	if bich < 200 and bich > 190 then
+    		for i = 1,6,1 do
+    			local gdis = VecScale(VecNormalize(RVec()),1)
+    			local gspawn = VecAdd(middle,Vec(0,1,0))
+    			ParticleType("plain")
+    			ParticleTile(2)
+    			ParticleColor(0.6,0.2,1)
+    			ParticleRadius(2)
+    			ParticleAlpha(1)
+    			ParticleGravity(0)
+    			ParticleDrag(0)
+    			ParticleEmissive(2)
+    			ParticleRotation(0)
+    			ParticleCollide(0)
+    			SpawnParticle(gspawn,VecScale(VecNormalize(VecAdd(RVec(),Vec(0,1,0))),10),5)
+    			if bich == 199 then
+    				SpawnParticle(gspawn,VecScale(VecNormalize(VecAdd(Vec(0,0,0),Vec(0,1,0))),10),5)
+    			end
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    if GetString("game.player.tool") == "INFINITY" then
+    	UiPush()
+    		UiAlign("left")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 15)
+    		UiTranslate(1700, 900)
+    		if LockToggle then
+    			UiColor(1,1,1)
+    			UiText("Lock is: on")
+    		else
+    			UiColor(0,0,0)
+    			UiText("Lock is: off")
+    		end
+    		UiColor(1,1,1)
+    		UiTranslate(0, 20)
+    			if wheelless then
+    				UiText("Scrollwheelless: " .. tostring(math.floor(scrollPos)) .. "\n"
+    				)
+    			else
+    				UiText("Scrollwheel: " .. tostring(math.floor(scrollPos)) .. "\n"
+    				)
+    			end
+    		UiTranslate(0, 20)
+    		if InfToggle then
+    			UiColor(1,1,1)
+    			UiText("Infinity is: on")
+    		else
+    			UiColor(0,0,0)
+    			UiText("Infinity is: off")
+    		end
+    		UiTranslate(0, 20)
+    		if FlyToggle then
+    			UiColor(1,1,1)
+    			UiText("Flight is: on")
+    		else
+    			UiColor(0,0,0)
+    			UiText("Flight is: off")
+    		end
+    		UiTranslate(0, 20)
+    		if telek then
+    			UiColor(1,1,1)
+    			UiText("Alt use is: on")
+    		else
+    			UiColor(0,0,0)
+    			UiText("Alt use is: off")
+    		end
+    		UiTranslate(0, 20)
+    		UiColor(0.2,0.6,1)
+    		if SBlue then
+    			UiText("Blue: " .. tostring(math.floor(BluStr)) .. "\n"
+    			)
+    		else
+    			UiText("Blue: no")
+    		end
+    		UiTranslate(1, 20)
+    		UiColor(1,0.2,0.2)
+    		if SRed then
+    			UiText("Red: " .. tostring(math.floor(RedStr)) .. "\n"
+    			)
+    		else
+    			UiText("Red: no")
+    		end
+    		UiTranslate(0, 20)
+    		UiColor(1,0.4,1)
+    		if PNuke then
+    			UiText("Purple: " .. tostring(math.floor(Str)) .. "\n"
+    			)
+    		else
+    			UiText("Purple: no")
+    		end
+
+    		UiTranslate(0, 20)
+    		local bitchasscolorrainbowheadassthingamabob = Vec(math.sin(Frames/10)+0.5,math.cos(Frames/10)+0.5,math.tan(Frames/10)+0.5) --worst fucking color generator ever
+    		UiColor(bitchasscolorrainbowheadassthingamabob[1],bitchasscolorrainbowheadassthingamabob[2],bitchasscolorrainbowheadassthingamabob[3])
+    		if DomainToggle then
+    			UiText("DOMAIN EXPANSION: INFINITE VOID")
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
@@ -1,500 +1,501 @@
---Limitless mod options/keybinds and whatever
-
-function init()
-	
-	circle = LoadSprite("circle.png")
-	ripple = LoadSprite("ripple.png")
-	star = LoadSprite("star.png")
-	earth = LoadSprite("earth.png")
-	ripple3 = LoadSprite("ripple3copyright.png") --not actually copyrighted, despite the name, idk why i called it that
-	cleave = LoadSound("Cleave.ogg")
-	--all i know is setbool and getbool with this saving stuff
-	if not HasKey("savegame.mod.inf.wheelless") then
-		SetBool("savegame.mod.inf.wheelless", false)
-	end
-	if not HasKey("savegame.mod.inf.performancemode") then --remember, performance stat is the one WITH particles, i switched it in ONLY THE OPTIONS THING DO NOT MESS THIS UP AGAIN
-		SetBool("savegame.mod.inf.performancemode", true)
-	end
-	--keybinds, making sure there are some
-	if not HasKey("savegame.mod.inf.infkey") then
-		SetString("savegame.mod.inf.infkey","e")
-	end
-	if not HasKey("savegame.mod.inf.sadd") then
-		SetString("savegame.mod.inf.sadd","z")
-	end
-	if not HasKey("savegame.mod.inf.ssub") then
-		SetString("savegame.mod.inf.ssub","x")
-	end
-	if not HasKey("savegame.mod.inf.time") then
-		SetString("savegame.mod.inf.time","r")
-	end
-	if not HasKey("savegame.mod.inf.warp") then
-		SetString("savegame.mod.inf.warp","t")
-	end
-	if not HasKey("savegame.mod.inf.cutsc") then
-		SetString("savegame.mod.inf.cutsc","v")
-	end
-	if not HasKey("savegame.mod.inf.tel") then
-		SetString("savegame.mod.inf.tel","b")
-	end
-	if not HasKey("savegame.mod.inf.dom") then
-		SetString("savegame.mod.inf.dom","m")
-	end
-	if not HasKey("savegame.mod.inf.ptrack") then
-		SetString("savegame.mod.inf.ptrack","n")
-	end
-	if not HasKey("savegame.mod.inf.flykey") then
-		SetString("savegame.mod.inf.flykey","alt")
-	end
-	if not HasKey("savegame.mod.inf.lock") then
-		SetString("savegame.mod.inf.lock","shift")
-	end
-	if not HasKey("savegame.mod.inf.grab") then
-		SetString("savegame.mod.inf.grab","q")
-	end
-	--GetString("savegame.mod.inf.")
-	popup = false
-	order = ""
-	serve = "0"
-end
-
-function draw()
-	local mx, my = UiGetMousePos()
-	--UiButtonHoverColor()
-	--UiButtonPressColor()
---earf
-	UiPush()
-		UiAlign("left")
-		UiWordWrap(500000000)
-		UiFont("arial.ttf", 10)
-		
-		UiTranslate(1000,100)
-		UiColor(1,1,1)
-		if UiImageButton("earth.png") then
-			UiSound("Cleave.ogg",2,rand(0.5,1))
-		end
-	UiPop()
---excuses
-	UiPush()
-		UiAlign("left")
-		UiWordWrap(500000000)
-		UiFont("arial.ttf", 15)
-		
-		UiTranslate(30,30)
-		UiColor(1,1,1)
-		UiText("-Excuse the slightly less terrible UI")
-	UiPop()
---CONTROLLER? OR NAW
-	
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 150)
-		UiColor(1,1,1)
-		UiText("Controller controls (DOES NOT WORK FULLY YET): ")
-		UiAlign("left")
-		UiTranslate(30)
-		--UiButtonHoverColor(0,0,10)
-		UiButtonPressColor(0,0,10)
-		if GetBool("savegame.mod.inf.controller") == true then
-			UiColor(0,1,0.2)
-		else
-			UiColor(1,0,0.2)
-		end
-		if UiTextButton("O",2,2) then
-			if GetBool("savegame.mod.inf.controller") == true then
-				SetBool("savegame.mod.inf.controller", false)
-
-				SetString("savegame.mod.inf.infkey","e")
-				SetString("savegame.mod.inf.sadd","z")
-				SetString("savegame.mod.inf.ssub","x")
-				SetString("savegame.mod.inf.time","r")
-				SetString("savegame.mod.inf.warp","t")
-				SetString("savegame.mod.inf.cutsc","v")
-				SetString("savegame.mod.inf.tel","b")
-				SetString("savegame.mod.inf.dom","m")
-				SetString("savegame.mod.inf.ptrack","n")
-				SetString("savegame.mod.inf.flykey","alt")
-				SetString("savegame.mod.inf.lock","shift")
-				SetString("savegame.mod.inf.grab","q")
-			else
-				SetBool("savegame.mod.inf.controller", true)
-			end
-		end
-		UiTranslate(-30,50)
-		UiColor(1,1,1)
-		UiAlign("right")
-		UiText("(you can turn off controller mode and turn back on to reset keybinds)")
-		--DebugPrint(Vec(mx,my))
-	UiPop()
-	
---toolless toggle NOW WHEELLESS
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 300)
-		UiColor(1,1,1)
-		UiText("Scrollwheelless: flight/teleport, blue/red grab: ")
-		UiAlign("left")
-		UiTranslate(30)
-		--UiButtonHoverColor(0,0,10)
-		UiButtonPressColor(0,0,10)
-		if GetBool("savegame.mod.inf.wheelless") == true then
-			UiColor(0,1,0.2)
-		else
-			UiColor(1,0,0.2)
-		end
-		if UiTextButton("O",2,2) then
-			if GetBool("savegame.mod.inf.wheelless") == true then
-				SetBool("savegame.mod.inf.wheelless", false)
-			else
-				SetBool("savegame.mod.inf.wheelless", true)
-			end
-		end
-		--DebugPrint(Vec(mx,my))
-	UiPop()
-	
---Performance toggle
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 250)
-		UiColor(1,1,1)
-		UiText("Performance (sprites): ")
-		UiAlign("left")
-		UiTranslate(30)
-		--UiButtonHoverColor(0,0,10)
-		UiButtonPressColor(0,0,10)
-		if GetBool("savegame.mod.inf.performancemode") == false then
-			UiColor(0,1,0.2)
-		else
-			UiColor(1,0,0.2)
-		end
-		if UiTextButton("O",2,2) then
-			if GetBool("savegame.mod.inf.performancemode") == true then
-				SetBool("savegame.mod.inf.performancemode", false)
-			else
-				SetBool("savegame.mod.inf.performancemode", true)
-			end
-		end
-		--DebugPrint(Vec(mx,my))
-	UiPop()
---keybinds
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(730, 350)
-		UiColor(1,1,1)
-		UiText("Keybinds:")
-	UiPop()
-
-	
-	--infinity (default e)
-	if order == "e" and serve ~= "0" then
-		SetString("savegame.mod.inf.infkey",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 400)
-		UiColor(1,1,1)
-		UiText("Infinity (Default E): ")
-
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.infkey"),2,2) then
-			popup = true
-			order = "e"
-		end
-		--DebugPrint(Vec(mx,my))
-	UiPop()
-
-	--tool lock (default shift)
-	if order == "shift" and serve ~= "0" then
-		SetString("savegame.mod.inf.lock",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 450)
-		UiColor(1,1,1)
-		UiText("Tool lock (Default SHIFT): ")
-		UiAlign("left")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		if UiTextButton(GetString("savegame.mod.inf.lock"),2,2) then
-			popup = true
-			order = "shift"
-		end
-		--DebugPrint(Vec(mx,my))
-	UiPop()
-
-	--fly key
-	if order == "alt" and serve ~= "0" then
-		SetString("savegame.mod.inf.flykey",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 500)
-		UiColor(1,1,1)
-		UiText("Flight key (Default ALT): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.flykey"),2,2) then
-			popup = true
-			order = "alt"
-		end
-		--DebugPrint(Vec(mx,my))
-	UiPop()
-	
-	--Grab key
-	if order == "q" and serve ~= "0" then
-		SetString("savegame.mod.inf.grab",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 550)
-		UiColor(1,1,1)
-		UiText("Grab key (Default Q): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.grab"),2,2) then
-			popup = true
-			order = "q"
-		end
-	UiPop()
-
-	--time key
-	if order == "r" and serve ~= "0" then
-		SetString("savegame.mod.inf.time",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 600)
-		UiColor(1,1,1)
-		UiText("Time key (Default R): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.time"),2,2) then
-			popup = true
-			order = "r"
-		end
-	UiPop()
-
-	--output increase
-	if order == "z" and serve ~= "0" then
-		SetString("savegame.mod.inf.sadd",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 650)
-		UiColor(1,1,1)
-		UiText("Output Increase (Default Z): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.sadd"),2,2) then
-			popup = true
-			order = "z"
-		end
-	UiPop()
-	-- decrease
-	if order == "x" and serve ~= "0" then
-		SetString("savegame.mod.inf.ssub",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 700)
-		UiColor(1,1,1)
-		UiText("Output Decrease (Default X): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.ssub"),2,2) then
-			popup = true
-			order = "x"
-		end
-	UiPop()
-
-	--blue splode enabler
-	if order == "b" and serve ~= "0" then
-		SetString("savegame.mod.inf.tel",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 750)
-		UiColor(1,1,1)
-		UiText("Alt use toggle (Default B): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.tel"),2,2) then
-			popup = true
-			order = "b"
-		end
-	UiPop()
-
-	--warp
-	if order == "t" and serve ~= "0" then
-		SetString("savegame.mod.inf.warp",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 800)
-		UiColor(1,1,1)
-		UiText("Teleport/warp (Default T): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.warp"),2,2) then
-			popup = true
-			order = "t"
-		end
-	UiPop()
-
-	--domain
-	if order == "m" and serve ~= "0" then
-		SetString("savegame.mod.inf.dom",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 850)
-		UiColor(1,1,1)
-		UiText("Domain Expansion (Default M): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.dom"),2,2) then
-			popup = true
-			order = "m"
-		end
-	UiPop()
-	
-	--ptrack
-	if order == "n" and serve ~= "0" then
-		SetString("savegame.mod.inf.ptrack",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 900)
-		UiColor(1,1,1)
-		UiText("(Maybe I should just change this one to begin with) Purple track toggle (Default N): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.ptrack"),2,2) then
-			popup = true
-			order = "n"
-		end
-	UiPop()
-
-	--cutscene
-	if order == "v" and serve ~= "0" then
-		SetString("savegame.mod.inf.cutsc",serve)
-		popup = false
-		serve = "0"
-	end
-	UiPush()
-		UiAlign("right")
-		UiWordWrap(5000000000000000) --5 million bajilion
-		UiFont("arial.ttf", 20)
-		UiTranslate(700, 950)
-		UiColor(1,1,1)
-		UiText("Cutscene purple (Default V): ")
-		UiTranslate(20)
-		UiColor(0.1,1,1)
-		UiButtonHoverColor(10,1,0)
-		UiAlign("left")
-		if UiTextButton(GetString("savegame.mod.inf.cutsc"),2,2) then
-			popup = true
-			order = "v"
-		end
-	UiPop()
-	--ENTER KEY POPUP!!
-	
-	if popup == true then
-		UiPush()
-			UiAlign("left")
-			UiWordWrap(5000000000000000) --5 million bajilion
-			UiFont("arial.ttf", 20)
-			UiTranslate(700, 40)
-			UiColor(0.2,0.2,0.2)
-			UiRect(2000,1000)
-
-			UiAlign("left")
-			UiWordWrap(5000000000000000) --5 million bajilion
-			UiFont("arial.ttf", 50)
-			UiTranslate(600, 400)
-			UiColor(1,1,1)
-			UiText("ENTER NEW KEYBIND, SIGMA")
-		UiPop()
-		if InputDown("any") and not (InputDown("lmb") or InputDown("rmb")) then
-			serve = InputLastPressedKey()
-		end
-	end
-end
-
+#version 2
 function rand(min,max)
 	return math.random(0,1000)/1000*(max-min)+min
-end+end
+
+function server.init()
+    circle = LoadSprite("circle.png")
+    ripple = LoadSprite("ripple.png")
+    star = LoadSprite("star.png")
+    earth = LoadSprite("earth.png")
+    ripple3 = LoadSprite("ripple3copyright.png") --not actually copyrighted, despite the name, idk why i called it that
+    --all i know is setbool and getbool with this saving stuff
+    if not HasKey("savegame.mod.inf.wheelless") then
+    	SetBool("savegame.mod.inf.wheelless", false, true)
+    end
+    if not HasKey("savegame.mod.inf.performancemode") then --remember, performance stat is the one WITH particles, i switched it in ONLY THE OPTIONS THING DO NOT MESS THIS UP AGAIN
+    	SetBool("savegame.mod.inf.performancemode", true, true)
+    end
+    --keybinds, making sure there are some
+    if not HasKey("savegame.mod.inf.infkey") then
+    	SetString("savegame.mod.inf.infkey","e", true)
+    end
+    if not HasKey("savegame.mod.inf.sadd") then
+    	SetString("savegame.mod.inf.sadd","z", true)
+    end
+    if not HasKey("savegame.mod.inf.ssub") then
+    	SetString("savegame.mod.inf.ssub","x", true)
+    end
+    if not HasKey("savegame.mod.inf.time") then
+    	SetString("savegame.mod.inf.time","r", true)
+    end
+    if not HasKey("savegame.mod.inf.warp") then
+    	SetString("savegame.mod.inf.warp","t", true)
+    end
+    if not HasKey("savegame.mod.inf.cutsc") then
+    	SetString("savegame.mod.inf.cutsc","v", true)
+    end
+    if not HasKey("savegame.mod.inf.tel") then
+    	SetString("savegame.mod.inf.tel","b", true)
+    end
+    if not HasKey("savegame.mod.inf.dom") then
+    	SetString("savegame.mod.inf.dom","m", true)
+    end
+    if not HasKey("savegame.mod.inf.ptrack") then
+    	SetString("savegame.mod.inf.ptrack","n", true)
+    end
+    if not HasKey("savegame.mod.inf.flykey") then
+    	SetString("savegame.mod.inf.flykey","alt", true)
+    end
+    if not HasKey("savegame.mod.inf.lock") then
+    	SetString("savegame.mod.inf.lock","shift", true)
+    end
+    if not HasKey("savegame.mod.inf.grab") then
+    	SetString("savegame.mod.inf.grab","q", true)
+    end
+    --GetString("savegame.mod.inf.")
+    popup = false
+    order = ""
+    serve = "0"
+end
+
+function client.init()
+    cleave = LoadSound("Cleave.ogg")
+end
+
+function client.draw()
+    	local mx, my = UiGetMousePos()
+    	--UiButtonHoverColor()
+    	--UiButtonPressColor()
+    --earf
+    	UiPush()
+    		UiAlign("left")
+    		UiWordWrap(500000000)
+    		UiFont("arial.ttf", 10)
+
+    		UiTranslate(1000,100)
+    		UiColor(1,1,1)
+    		if UiImageButton("earth.png") then
+    			UiSound("Cleave.ogg",2,rand(0.5,1))
+    		end
+    	UiPop()
+    --excuses
+    	UiPush()
+    		UiAlign("left")
+    		UiWordWrap(500000000)
+    		UiFont("arial.ttf", 15)
+
+    		UiTranslate(30,30)
+    		UiColor(1,1,1)
+    		UiText("-Excuse the slightly less terrible UI")
+    	UiPop()
+    --CONTROLLER? OR NAW
+
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 150)
+    		UiColor(1,1,1)
+    		UiText("Controller controls (DOES NOT WORK FULLY YET): ")
+    		UiAlign("left")
+    		UiTranslate(30)
+    		--UiButtonHoverColor(0,0,10)
+    		UiButtonPressColor(0,0,10)
+    		if GetBool("savegame.mod.inf.controller") == true then
+    			UiColor(0,1,0.2)
+    		else
+    			UiColor(1,0,0.2)
+    		end
+    		if UiTextButton("O",2,2) then
+    			if GetBool("savegame.mod.inf.controller") == true then
+    				SetBool("savegame.mod.inf.controller", false, true)
+
+    				SetString("savegame.mod.inf.infkey","e", true)
+    				SetString("savegame.mod.inf.sadd","z", true)
+    				SetString("savegame.mod.inf.ssub","x", true)
+    				SetString("savegame.mod.inf.time","r", true)
+    				SetString("savegame.mod.inf.warp","t", true)
+    				SetString("savegame.mod.inf.cutsc","v", true)
+    				SetString("savegame.mod.inf.tel","b", true)
+    				SetString("savegame.mod.inf.dom","m", true)
+    				SetString("savegame.mod.inf.ptrack","n", true)
+    				SetString("savegame.mod.inf.flykey","alt", true)
+    				SetString("savegame.mod.inf.lock","shift", true)
+    				SetString("savegame.mod.inf.grab","q", true)
+    			else
+    				SetBool("savegame.mod.inf.controller", true, true)
+    			end
+    		end
+    		UiTranslate(-30,50)
+    		UiColor(1,1,1)
+    		UiAlign("right")
+    		UiText("(you can turn off controller mode and turn back on to reset keybinds)")
+    		--DebugPrint(Vec(mx,my))
+    	UiPop()
+
+    --toolless toggle NOW WHEELLESS
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 300)
+    		UiColor(1,1,1)
+    		UiText("Scrollwheelless: flight/teleport, blue/red grab: ")
+    		UiAlign("left")
+    		UiTranslate(30)
+    		--UiButtonHoverColor(0,0,10)
+    		UiButtonPressColor(0,0,10)
+    		if GetBool("savegame.mod.inf.wheelless") == true then
+    			UiColor(0,1,0.2)
+    		else
+    			UiColor(1,0,0.2)
+    		end
+    		if UiTextButton("O",2,2) then
+    			if GetBool("savegame.mod.inf.wheelless") == true then
+    				SetBool("savegame.mod.inf.wheelless", false, true)
+    			else
+    				SetBool("savegame.mod.inf.wheelless", true, true)
+    			end
+    		end
+    		--DebugPrint(Vec(mx,my))
+    	UiPop()
+
+    --Performance toggle
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 250)
+    		UiColor(1,1,1)
+    		UiText("Performance (sprites): ")
+    		UiAlign("left")
+    		UiTranslate(30)
+    		--UiButtonHoverColor(0,0,10)
+    		UiButtonPressColor(0,0,10)
+    		if GetBool("savegame.mod.inf.performancemode") == false then
+    			UiColor(0,1,0.2)
+    		else
+    			UiColor(1,0,0.2)
+    		end
+    		if UiTextButton("O",2,2) then
+    			if GetBool("savegame.mod.inf.performancemode") == true then
+    				SetBool("savegame.mod.inf.performancemode", false, true)
+    			else
+    				SetBool("savegame.mod.inf.performancemode", true, true)
+    			end
+    		end
+    		--DebugPrint(Vec(mx,my))
+    	UiPop()
+    --keybinds
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(730, 350)
+    		UiColor(1,1,1)
+    		UiText("Keybinds:")
+    	UiPop()
+
+    	--infinity (default e)
+    	if order == "e" and serve ~= "0" then
+    		SetString("savegame.mod.inf.infkey",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 400)
+    		UiColor(1,1,1)
+    		UiText("Infinity (Default E): ")
+
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.infkey"),2,2) then
+    			popup = true
+    			order = "e"
+    		end
+    		--DebugPrint(Vec(mx,my))
+    	UiPop()
+
+    	--tool lock (default shift)
+    	if order == "shift" and serve ~= "0" then
+    		SetString("savegame.mod.inf.lock",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 450)
+    		UiColor(1,1,1)
+    		UiText("Tool lock (Default SHIFT): ")
+    		UiAlign("left")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		if UiTextButton(GetString("savegame.mod.inf.lock"),2,2) then
+    			popup = true
+    			order = "shift"
+    		end
+    		--DebugPrint(Vec(mx,my))
+    	UiPop()
+
+    	--fly key
+    	if order == "alt" and serve ~= "0" then
+    		SetString("savegame.mod.inf.flykey",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 500)
+    		UiColor(1,1,1)
+    		UiText("Flight key (Default ALT): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.flykey"),2,2) then
+    			popup = true
+    			order = "alt"
+    		end
+    		--DebugPrint(Vec(mx,my))
+    	UiPop()
+
+    	--Grab key
+    	if order == "q" and serve ~= "0" then
+    		SetString("savegame.mod.inf.grab",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 550)
+    		UiColor(1,1,1)
+    		UiText("Grab key (Default Q): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.grab"),2,2) then
+    			popup = true
+    			order = "q"
+    		end
+    	UiPop()
+
+    	--time key
+    	if order == "r" and serve ~= "0" then
+    		SetString("savegame.mod.inf.time",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 600)
+    		UiColor(1,1,1)
+    		UiText("Time key (Default R): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.time"),2,2) then
+    			popup = true
+    			order = "r"
+    		end
+    	UiPop()
+
+    	--output increase
+    	if order == "z" and serve ~= "0" then
+    		SetString("savegame.mod.inf.sadd",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 650)
+    		UiColor(1,1,1)
+    		UiText("Output Increase (Default Z): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.sadd"),2,2) then
+    			popup = true
+    			order = "z"
+    		end
+    	UiPop()
+    	-- decrease
+    	if order == "x" and serve ~= "0" then
+    		SetString("savegame.mod.inf.ssub",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 700)
+    		UiColor(1,1,1)
+    		UiText("Output Decrease (Default X): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.ssub"),2,2) then
+    			popup = true
+    			order = "x"
+    		end
+    	UiPop()
+
+    	--blue splode enabler
+    	if order == "b" and serve ~= "0" then
+    		SetString("savegame.mod.inf.tel",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 750)
+    		UiColor(1,1,1)
+    		UiText("Alt use toggle (Default B): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.tel"),2,2) then
+    			popup = true
+    			order = "b"
+    		end
+    	UiPop()
+
+    	--warp
+    	if order == "t" and serve ~= "0" then
+    		SetString("savegame.mod.inf.warp",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 800)
+    		UiColor(1,1,1)
+    		UiText("Teleport/warp (Default T): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.warp"),2,2) then
+    			popup = true
+    			order = "t"
+    		end
+    	UiPop()
+
+    	--domain
+    	if order == "m" and serve ~= "0" then
+    		SetString("savegame.mod.inf.dom",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 850)
+    		UiColor(1,1,1)
+    		UiText("Domain Expansion (Default M): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.dom"),2,2) then
+    			popup = true
+    			order = "m"
+    		end
+    	UiPop()
+
+    	--ptrack
+    	if order == "n" and serve ~= "0" then
+    		SetString("savegame.mod.inf.ptrack",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 900)
+    		UiColor(1,1,1)
+    		UiText("(Maybe I should just change this one to begin with) Purple track toggle (Default N): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.ptrack"),2,2) then
+    			popup = true
+    			order = "n"
+    		end
+    	UiPop()
+
+    	--cutscene
+    	if order == "v" and serve ~= "0" then
+    		SetString("savegame.mod.inf.cutsc",serve, true)
+    		popup = false
+    		serve = "0"
+    	end
+    	UiPush()
+    		UiAlign("right")
+    		UiWordWrap(5000000000000000) --5 million bajilion
+    		UiFont("arial.ttf", 20)
+    		UiTranslate(700, 950)
+    		UiColor(1,1,1)
+    		UiText("Cutscene purple (Default V): ")
+    		UiTranslate(20)
+    		UiColor(0.1,1,1)
+    		UiButtonHoverColor(10,1,0)
+    		UiAlign("left")
+    		if UiTextButton(GetString("savegame.mod.inf.cutsc"),2,2) then
+    			popup = true
+    			order = "v"
+    		end
+    	UiPop()
+    	--ENTER KEY POPUP!!
+
+    	if popup == true then
+    		UiPush()
+    			UiAlign("left")
+    			UiWordWrap(5000000000000000) --5 million bajilion
+    			UiFont("arial.ttf", 20)
+    			UiTranslate(700, 40)
+    			UiColor(0.2,0.2,0.2)
+    			UiRect(2000,1000)
+
+    			UiAlign("left")
+    			UiWordWrap(5000000000000000) --5 million bajilion
+    			UiFont("arial.ttf", 50)
+    			UiTranslate(600, 400)
+    			UiColor(1,1,1)
+    			UiText("ENTER NEW KEYBIND, SIGMA")
+    		UiPop()
+    		if InputDown("any") and not (InputDown("lmb") or InputDown("rmb")) then
+    			serve = InputLastPressedKey()
+    		end
+    	end
+end
+

```
