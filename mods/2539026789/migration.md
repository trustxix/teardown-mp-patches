# Migration Report: cfg\weapon.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/cfg\weapon.lua
+++ patched/cfg\weapon.lua
@@ -0,0 +1 @@
+#version 2

```

---

# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,115 +1,4 @@
-#include "umf/umf_core.lua"
-
---[[
-
-
-	Thermite cannon pack
-
-
-	created by: elboydo
-
-
-
-]]
-
-
---[[
-
-
-	debug shit
-
-
-]]
-
-debugMode = false
-
-IS_EXPERIMENTAL_POST_API_2_0 = nil
-
-debugStuff = {
-	crosses = {},
-	redCrosses = {}
-
-}
-
-
-className = "elboydo"
---[[
-	global values for behaviors and stuff
-
-]]
-globalConfig = {
-	aimAhead = 400,
-	minAimAhead = 10,
-	penCheck = 0.01,
-	penIteration = 0.1,
-	HEATRange = 3,
-	gravity = Vec(0,-15,0),
-	MaxSpall = 8,
-	spallQuantity = 16,
-	spallFactor = {
-			kinetic = 0.75,
-			AP 		= 0.3,
-			APHE    = 0.3,
-			HESH 	= 1.8,
-			HEI 	= 1,
-	},
-
-	materials = {
-		rock  = 13,
-		dirt  = 0.2,
-		plaster = 0.1,
-		plastic = 0.05,
-		masonry = 0.27,
-		glass = 0.01,
-		foliage = 0.025,
-		wood  = 0.2,
-		metal  = 0.42,
-		hardmetal = 0.73,
-		heavymetal  = 13,
-		hardmasonry = 0.6,
-
-
-	},	
-	incendiaryMaterials = {
-		rock  = 13,
-		dirt  = 0.2,
-		plaster = 0.1,
-		plastic = 0.05,
-		masonry = 0.299,
-		glass = 0.01,
-		foliage = 0.025,
-		wood  = 0.2,
-		metal  = 0.27,
-		hardmetal = 0.73,
-		heavymetal  = 13,
-		hardmasonry = 0.6,
-
-
-	},
-	testNumber = 0,
-}
-
---- values for setvalues
-FOV=GetInt("options.gfx.fov")
-zoomLevel = 0
-viewQuat = QuatEuler()
-viewVec = Vec()
-push=0.5
-recoilVal = 0
-recoilCoef = 0.4
-vx,vy,vz = 0,0,0
-pqx, pqy, pqz=0,0,0
-pvx, pvy, pvz=0,0,0
-
-qx, qy, qz = 0,0,0
-vzr = 0
-qxr, qyr=0,0
-
-
-
-vox=.05
-
-
+#version 2
 local weaponBase = {
 	id 						= nil, 
 	name 					= "default",
@@ -141,7 +30,6 @@
 	inaccuracy 				= 2,
 	inaccuracyRampTime 		= 4,	
 	baseInaccuracy 				= 0.5,
-
 
 	canZoom					= false,
 	zoomMultiplier = 0.8,
@@ -223,7 +111,29 @@
 		}
 	},
 }
-
+local defaultProjectile = {
+			name = "custom ball round",
+			caliber 				= 7.62,
+			velocity				= 350,
+			timeToLive 				= 7,
+			hit 					=2,
+			maxPenDepth 			= 0.1,
+			payload					= "AP",
+			shellWidth				= 0.1,
+			shellHeight				= 0.3,
+			r						= 0.8,
+			g						= 0.8, 
+			b						= 0.5, 
+			tracer 					= 5,
+			tracerL					= 6,
+			tracerW					= 2,
+			tracerR					= 1.8,
+			tracerG					= 1.0, 
+			tracerB					= 1.0, 
+			shellSpriteName			= "MOD/gfx/shell2.png",
+			shellSpriteRearName		= "MOD/gfx/shellRear.png",
+	}
+local thermiteCannon = weaponBase:new()
 
 function weaponBase:init(cfg)
 	
@@ -265,7 +175,6 @@
 
 end
 
-
 function weaponBase:loadReloadSounds()
 	self.snd.reloadEject ={}
 	self.snd.reloadLoad ={}
@@ -283,7 +192,6 @@
 		self.snd.reloadCockWeapon[i] = LoadSound("MOD/snd/"..self.reloadSnd.dir..self.reloadSnd.files.cockWeapon.name..i..".ogg") 
 	end 
 end
-
 
 function weaponBase:loadImpactSounds()
 	self.snd.impactSnds = {}
@@ -301,23 +209,21 @@
 			end
 		end
 
-
-
 	end
 end
 
 function weaponBase:tick(dt) 
 	if not self.reloading then
 		if(SafeGetToolValue(self.id)>math.floor(SafeGetToolValue(self.id))and SafeGetToolValue(self.id)<math.ceil(SafeGetToolValue(self.id)))then
-			SetString(self.ammoID..".display", string.format("%.2f",self.loadedMagazine).." | "..string.format("%.2f",SafeGetToolValue(self.id)-self.magazineCapacity+(self.magazineCapacity - self.loadedMagazine)))
+			SetString(self.ammoID..".display", string.format("%.2f",self.loadedMagazine).." | "..string.format("%.2f",SafeGetToolValue(self.id)-self.magazineCapacity+(self.magazineCapacity - self.loadedMagazine)), true)
 			
 		else
-			SetString(self.ammoID..".display", self.loadedMagazine.." | "..SafeGetToolValue(self.id)-self.magazineCapacity+(self.magazineCapacity - self.loadedMagazine))
+			SetString(self.ammoID..".display", self.loadedMagazine.." | "..SafeGetToolValue(self.id)-self.magazineCapacity+(self.magazineCapacity - self.loadedMagazine), true)
 		
 		end
 		self:fire(dt)
 	elseif(self.reloading) then 
-		SetString(self.ammoID..".display", "Reloading")
+		SetString(self.ammoID..".display", "Reloading", true)
 
 		self:reloadWeapon(dt)
 	end		
@@ -330,9 +236,9 @@
 function weaponBase:fire(dt) 
 		--Check if tool is firing
 		if toolFiring(self) then
-			SetBool("game.input.locktool",true)
+			SetBool("game.input.locktool",true, true)
 			if(self.timeToFire<0)then 
-				local t =  GetPlayerCameraTransform()
+				local t =  GetPlayerCameraTransform(playerId)
 				-- local b = GetBodyTransform(GetToolBody())
 				local fwd = TransformToParentPoint(t, Vec(0, 0, -1))
 				local c = TransformToParentPoint(t, Vec(0, 0, -400))
@@ -378,9 +284,8 @@
 		end
 end
 
-
 function weaponBase:getFirePos()
-			local t =  GetPlayerCameraTransform()
+			local t =  GetPlayerCameraTransform(playerId)
 			local fwd = TransformToParentPoint(t, Vec(0, 0, -1))
 			local c = TransformToParentPoint(t, Vec(0, 0, -globalConfig.aimAhead))
 			local s = self:getBarrelPos()
@@ -390,7 +295,7 @@
 end
 
 function weaponBase:getAimPos()
-			local t =  GetPlayerCameraTransform()
+			local t =  GetPlayerCameraTransform(playerId)
 			local fwd = TransformToParentPoint(t, Vec(0, 0, -1))
 			local c = TransformToParentPoint(t, Vec(0, 0, -globalConfig.aimAhead))
 			local dir =VecNormalize(VecSub(fwd,t.pos))
@@ -421,13 +326,13 @@
 end
 
 function weaponBase:zoomAim(b)
-	if(InputDown("grab") and not IsHandleValid(GetPlayerGrabBody())) then
+	if(InputDown("grab") and not IsHandleValid(GetPlayerGrabBody(playerId))) then
 		if(zoomLevel==0) then  
 			SetValue("zoomLevel", 1, "linear", 0.5)
 		end
 
 		
-	elseif((InputReleased("grab") and not IsHandleValid(GetPlayerGrabBody())) ) then --(zoomlevel~=0) then 
+	elseif((InputReleased("grab") and not IsHandleValid(GetPlayerGrabBody(playerId))) ) then --(zoomlevel~=0) then 
 		SetValue("zoomLevel", 0, "linear", 0.25)
 	end
 	if(zoomLevel~=0) then
@@ -436,13 +341,10 @@
 	end
 end
 
-
 function weaponBase:onKill(hitPos)
 	MakeHole(hitPos,self.ammo.bulletdamage[1],self.ammo.bulletdamage[2], self.ammo.bulletdamage[3])
 
-
-end
-
+end
 
 function weaponBase:reloadWeapon(dt) 
 	if(self.reloadTimer == self.maxReload) then 
@@ -475,9 +377,7 @@
 	
 end
 
-
 function weaponBase:animateReload()
-
 
 end
 
@@ -487,15 +387,6 @@
 		self.loadedMagazine = self.loadedMagazine - 1
 	end
 end
-
-
---[[
-
-	many thanks to please pick a name for their amazing guidance in making recoil animations smooth
-
-
-
-]]
 
 function 	weaponBase:animateRecoil()
 	local b = GetToolBody()
@@ -514,8 +405,6 @@
 
 end
 
-
---[[ gun holding in front of chest pose ]]
 function safeMove()
 	SetValue("vx",pvx-1*vox,"cosine",.1)
 	SetValue("vy",pvy-2*vox,"cosine",.1)
@@ -525,7 +414,6 @@
 	SetValue("qz",pqz-5,"cosine",.1)
 end
 
---[[ gun holding pose ]]
 function pose0()
 	SetValue("vx",pvx,"cosine",.1)
 	SetValue("vy",pvy,"cosine",.1)
@@ -534,8 +422,6 @@
 	SetValue("qy",pqy,"cosine",.1)
 	SetValue("qz",pqz,"cosine",.1)
 end
-
-
 
 function ViewDefault()
 	viewVec=Vec()
@@ -622,7 +508,6 @@
 
 end
 
-
 function weaponBase:specialBehaviors(dt)
 	self:zoomAim()
 end
@@ -640,7 +525,7 @@
 function weaponBase:establishBaseStates()
 	
 	local b = GetToolBody()
-	if b > 0 then
+	if b ~= 0 then
 	local shapes = GetBodyShapes(b)
 		if b ~= self.body then
 			self.body = b
@@ -654,7 +539,6 @@
 	end
 
 end
-
 
 function weaponBase:draw(dt)
 	local aimDotWidth = self.aimDotSizeX or self.aimDotSize
@@ -679,133 +563,12 @@
 	return o
 end
 
-local defaultProjectile = {
-			name = "custom ball round",
-			caliber 				= 7.62,
-			velocity				= 350,
-			timeToLive 				= 7,
-			hit 					=2,
-			maxPenDepth 			= 0.1,
-			payload					= "AP",
-			shellWidth				= 0.1,
-			shellHeight				= 0.3,
-			r						= 0.8,
-			g						= 0.8, 
-			b						= 0.5, 
-			tracer 					= 5,
-			tracerL					= 6,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shell2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear.png",
-	}
-
 function defaultProjectile:new (o)
 	o = o or {}
 	setmetatable(o, self)
 	self.__index = self
 	return o
 end
-
-
-
-
---[[
-
----------------------------------
-			s_Thermite
-
-			Thermite
----------------------------------
-
-]]
-
-local thermiteCannon = weaponBase:new()
-
-thermiteCannon.cfg = {
-				name 	= "Thermite Cannon",
-				controller = "Thermite_Cannon",
-				vox 					= "Thermite_Cannon",
-				ammunitionType 			= "Incendiary",
-				drag 					= 1,--0.2,
-				fireRate 				= 780,
-				weaponType 				= "spray",
-				inaccuracy 				= 0.5,
-				baseInaccuracy 			= 1.5,
-				maxAmmo 				= 395,
-				maxReload				= 2.5,
-				magazineCapacity 		= 45,
-				loadedMagazine 			= 45,
-				burnPower 				=	5,
-				recoil 					= 0.25,
-
-
-				aimDot 					= "gfx/aimDot_lower.png",
-				aimDotSizeX 				= 70,
-				ammo = defaultProjectile:new{
-							name = "custom ball round",
-							caliber 				= 5,
-							velocity 				= 40,
-							drag 					= 0.3,
-							hit 					=2,
-							launcher				= "mgun",
-					},
-				barrels				= 
-											{
-												[1] = {x=0.25,y=1.7,z=0.40},
-											},
-				multiBarrel 			= 1,
-				barrelEffectPos				= Vec(0.25,2.1,0.33),
-				canZoom					= false,
-				reloadAnimation = {
-					[1] = {
-						pos = Vec(0.3,0.3,-0.3),
-						rot = QuatEuler(15,30,0)--Vec(-2,-1,0),
-					},
-					[2] = {
-						pos = Vec(-1.5,-.1,1.2),
-						rot = QuatEuler(45,45,0),
-					},
-				},
-				reloadKeyFrames = {
-					[1] = 0.2,
-					[2]	= 0.8,
-					[3] = 0.5,
-
-				},
-				snd 					= {
-					dir = "flamethrower/",
-					files	= {
-						fireLoop = {
-							sounds = 1,
-							loop 	= true,
-							name = "FlameThrower_FireLoop02",
-
-						},
-						impactLoop = {
-							sounds = 1,
-							loop 	= true,
-							name = "FlameThrower_ImpactSmoulderLoop01",
-						},
-
-						fire = {
-							sounds = 4,
-							name   = "FlameThrower_Fire0",
-						},
-						fireStop = {
-							sounds = 2,
-							name = "FlameThrower_FireStop0",
-						},
-						
-
-
-					}
-				},
-}
-
-
 
 function thermiteCannon:loadSounds()
 	self:loadShootSounds()
@@ -817,10 +580,6 @@
 	self.snd.fireLoop =LoadLoop("MOD/snd/"..self.snd.dir..self.snd.files.fireLoop.name..".ogg")
 	self.snd.impactLoop =LoadLoop("MOD/snd/"..self.snd.dir..self.snd.files.impactLoop.name..".ogg")
 end
-
-
-thermiteCannon:init(thermiteCannon.cfg)
-
 
 function thermiteCannon:fire(dt)
 	
@@ -846,7 +605,7 @@
 				local s = VecAdd(VecAdd(t.pos, Vec(0, -0.5, 0)),VecScale(fwd, 1.5))
 				local e = VecAdd(t.pos, VecScale(fwd, dist))
 
-				local t =  GetPlayerCameraTransform()
+				local t =  GetPlayerCameraTransform(playerId)
 				-- local b = GetBodyTransform(GetToolBody())
 				local fwd = TransformToParentVec(t, Vec(0, 0, -1))
 				local c = TransformToParentPoint(t, Vec(0, 0, -400))
@@ -879,7 +638,7 @@
 		end
 	
 		local b = GetToolBody()
-		if b > 0 then
+		if b ~= 0 then
 			local shapes = GetBodyShapes(b)
 
 			--Control emissiveness
@@ -888,15 +647,13 @@
 			end
 	
 			--Add some light
-			if ready > 0 then
+			if ready ~= 0 then
 				local p = TransformToParentPoint(GetBodyTransform(body), Vec(0, 0, -2))
 				PointLight(p, 1, 0.5, 0.7, ready * math.random(10, 15) / 10)
 			end
 			
 			self:barrelEffect()
 		end
-
-
 
 end
 
@@ -906,7 +663,6 @@
 	
 	end	
 end
-
 
 function thermiteCannon:animateReload()
 		-- if not(self.magOrigin) then 
@@ -973,7 +729,6 @@
 		end		
 end
 
-
 function thermiteCannon:barrelEffect()
 	local b = GetToolBody()
 	local shapes = GetBodyShapes(b)
@@ -1030,32 +785,16 @@
 	
 end
 
-
-
-
 function thermiteCannon:onKill(hitPos)
 	SpawnFire(hitPos)
 
 end
-
-
---[[
------------------------------------------------------
-
-
-	projectile operation handlers
-
-
------------------------------------------------------
-]]
-
-
 
 function pushProjectile(cannonLoc,weaponClass)
 		local fwdPos = TransformToParentPoint(cannonLoc, Vec(0,0,-1))
 		local direction = VecSub(fwdPos, cannonLoc.pos)
 		local point1 = cannonLoc.pos
-		local predictedBulletVelocity =VecScale(direction,weaponClass.ammo.velocity)--VecAdd(GetPlayerVelocity(),VecScale(direction,weaponClass.ammo.velocity))
+		local predictedBulletVelocity =VecScale(direction,weaponClass.ammo.velocity)--VecAdd(GetPlayerVelocity(playerId),VecScale(direction,weaponClass.ammo.velocity))
 		local innacuracyModifier = 0
 		if(weaponClass.fireTime>0)then 
 			innacuracyModifier = weaponClass.inaccuracy* math.min(1, easeInCubic(weaponClass.fireTime)/easeInCubic(weaponClass.inaccuracyRampTime))
@@ -1083,7 +822,6 @@
 	return Vec(v[1]*s,v[2]*s,v[3]*s)
 end
 
-
 function rectifyBarrelCoords(cannonLoc)
 
 	-- utils.printStr	(gun.multiBarrel)--.." | "..#gun.barrels	)
@@ -1096,7 +834,6 @@
 	cannonLoc.pos = VecAdd(cannonLoc.pos, direction)
 	return cannonLoc
 end
-
 
 function impactEffect(projectile,hitPos)
 	
@@ -1133,8 +870,6 @@
 	end
 end
 
---- stuff happens here when it hits stuff
-
 function popProjectile(projectile,hitPos,hitTarget)
 	if(projectile.weaponClass.ammo.stickyObject) then 
 		projectile.stuckOnTarget = true
@@ -1154,7 +889,6 @@
 
 		-- playImpactSound(projectile,hitPos,hitTarget)
 
-
 		-- apply effects to impact pos
 		if(projectile.weaponClass.ammunitionType =="cartridge" or projectile.weaponClass.ammunitionType =="Incendiary") then 
 			impactEffect(projectile,hitPos)
@@ -1208,9 +942,6 @@
 			end
 			projectile = deepcopy(projectileHandler.defaultShell)
 end
-
-
---- this is what runs when it's in flight
 
 function projectileOperations(projectile,dt )
 		if(not projectile.stuckOnTarget)then 
@@ -1265,19 +996,6 @@
 		end
 end
 
-
-
-
---[[
-		s_Pen
-
-		penetration handling
-
-
-
-]]
-
- -- check left right, if number then explode, if 0 then fly on.
 function getProjectilePenetration(shell,hitTarget)
 	local penetrationTable = globalConfig.materials
 	if(shell.weaponClass.ammunitionType =="Incendiary") then
@@ -1353,28 +1071,18 @@
 	return penetration,passThrough,test,penDepth,dist1,spallValue,returnDir
 end
 
-
 function rectifyPenetrationVal(t_cannonLoc)
 		-- utils.printStr("fixingpen")
 	local y = 0
 	local x = 0 
 	local z = 0.1
 
-
 	local fwdPos = TransformToParentPoint(t_cannonLoc, Vec(x, z,y))
 
 	local direction = VecSub(fwdPos, t_cannonLoc.pos)
 	t_cannonLoc.pos = VecAdd(t_cannonLoc.pos, direction)
 	return t_cannonLoc
 end
-
-
---[[
-
-	callbacks
-
-]]
-
 
 function callbackTick(dt)
 	local activecallbacks = 0
@@ -1394,7 +1102,6 @@
 
 		end
 end
-
 
 function pushcallback(timeToFire,targetFunc,callingFunction,arr)
 		callbackHandler.callbacks[callbackHandler.index] = deepcopy(callbackHandler.defaultCallback)
@@ -1412,72 +1119,9 @@
 	-- 			smokeFactor 			= .5,
 	-- 			smokeMulti				= 1,
 
-
-
 	callbackHandler.index = (callbackHandler.index%#callbackHandler.callbacks) +1
 end
 
-
-
---[[
-
-
-	s_setup
-
-putting it together
-
-
-]]
-
-weapons = {
-	[1] = thermiteCannon,
-}
-
-
---[[
-	projectile and spalling handlers
-
-
-]]
-
-projectileHandler = 
-	{
-		shellNum = 1,
-		shells = {
-
-		},
-	defaultShell = {active=false, velocity=nil, direction =nil, currentPos=nil, timeLaunched=nil},
-	gravity = 0.4,
-	shellWidth = 0.1,
-	shellHeight = .8
-	}
-
-callbackHandler = 
-	{
-	index = 1,
-	callbacks = {
-
-		},
-	defaultCallback = {active=false},
-	}
-
-
---[[
-	few static variables
-
-]]
-
--- static of hoqw much gravity is applied
-gravity = globalConfig.gravity
-maxActiveShells = 500
-
-
---Laser Gun example mod
-equippedWeapon = nil
-equipDelay = 0.3
-equipTimer = 0.3
-
--- Returns true if v1 >= v2
 function VersionAtLeast(v1, v2)
     local function split(ver)
         local t = {}
@@ -1497,8 +1141,7 @@
     return true  -- equal
 end
 
--- Safely get a tool’s ammo/count value
-function SafeGetToolValue(tool)
+nction SafeGetToolValue(tool)
     if IS_EXPERIMENTAL_API_2_0 then
         -- Experimental API 2.0+
         return GetToolAmmo(tool)
@@ -1511,21 +1154,22 @@
     end
 end
 
--- Safely set a tool’s ammo/count value
-function SafeSetToolValue(tool, value)
+tion SafeSetToolValue(tool, value)
     if IS_EXPERIMENTAL_API_2_0 then
         -- Experimental API 2.0+
         SetToolAmmo(tool, value)
     elseif VersionAtLeast(GetVersion(), "1.7.0") then
         -- Stable API 1.7+
-        SetFloat(tool, value)
+        SetFloat(tool, value, true)
     else
         -- Older legacy versions: no-op or log
         DebugPrint("Legacy version, cannot set tool value")
     end
 end
 
-function init()
+fu
+
+tion init()
 	local v = GetVersion()
 	if VersionAtLeast(v, "2.0.0") then
 -- 		-- Experimental API is available
@@ -1540,7 +1184,6 @@
 	end
 	IS_EXPERIMENTAL_POST_API_2_0 = VersionAtLeast(GetVersion(), "2.0.0")
 
-
 	
 
 	thermiteCannon:init(thermiteCannon.cfg)
@@ -1548,11 +1191,11 @@
 	for i = 1,#weapons do
 		local weaponClass = weapons[i]
 		RegisterTool(weaponClass.id, weaponClass.name, "MOD/vox/"..weaponClass.vox..".vox")
-		SetBool("game.tool."..weaponClass.id..".enabled", true)
+		SetBool("game.tool."..weaponClass.id..".enabled", true, true)
 		--If played in sandbox mode, the sandbox script will make it infinite automatically
 		SafeSetToolValue(weaponClass.id, weaponClass.maxAmmo)
-		-- SetInt(weaponClass.ammoID..".max",  weaponClass.maxAmmo)	
-		SetString(weaponClass.ammoID..".display", weaponClass.loadedMagazine.." | "..SafeGetToolValue(weaponClass.id)-weaponClass.magazineCapacity+(weaponClass.magazineCapacity - weaponClass.loadedMagazine))
+		-- SetInt(weaponClass.ammoID..".max",  weaponClass.maxAmmo, true)	
+		SetString(weaponClass.ammoID..".display", weaponClass.loadedMagazine.." | "..SafeGetToolValue(weaponClass.id)-weaponClass.magazineCapacity+(weaponClass.magazineCapacity - weaponClass.loadedMagazine), true)
 		
 	end
 	ready = 0
@@ -1571,22 +1214,25 @@
 
 	equippedWeapon =  GetString("game.player.tool")
 
-
 	unlimitedammo = (GetBool("level.unlimitedammo"))
 end
 
---Return a random vector of desired length
-function rndVec(length)
+--
+
+tion rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
 
-function rnd(mi, ma)
+fu
+
+tion rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
 
-
-function tick(dt)
+f
+
+tion tick(dt)
 	projectileTick(dt)
 	callbackTick(dt)
 	playerTick(dt)
@@ -1606,8 +1252,9 @@
 	end
 end
 
-
-function playerTick(dt)
+f
+
+tion playerTick(dt)
 	if(GetString("game.player.tool")~= equippedWeapon) then
 		equipTimer = equipDelay
 		equippedWeapon = GetString("game.player.tool")
@@ -1626,10 +1273,12 @@
 		end
 	end
 end
-function draw()
+fun
+
+tion draw()
 	for i = 1,#weapons do 
 		if GetString("game.player.tool") == weapons[i].id and GetBool("game.player.canusetool") then
-			SetBool("hud.aimdot",false) 
+			SetBool("hud.aimdot",false, true) 
 			if(equipTimer<=0) then
 				weapons[i]:draw(dt)
 			end
@@ -1637,22 +1286,15 @@
 	end
 end
 
---[[
-	some tool helper functions
-
-
-]]
-function toolFiring(weaponClass)
+--
+
+tion toolFiring(weaponClass)
 	return (GetBool("game.player.canusetool") and (InputPressed("usetool")  or InputDown("usetool")) and SafeGetToolValue(weaponClass.id) > 0)
 end
 
---[[
-
-	common functins
-
-
-]]
-function deepcopy(orig)
+--
+
+tion deepcopy(orig)
     local orig_type = type(orig)
     local copy
     if orig_type == 'table' then
@@ -1667,26 +1309,17 @@
     return copy
 end
 
-
-function easeInCubic(t)	
+f
+
+tion easeInCubic(t)	
 	return t*t*t
 end
 
-
---[[
-
-
-	debugging
-
-]]
-
-
-function debugInfo(weaponClass)
+-
+
+tion debugInfo(weaponClass)
 
 	DebugWatch("ammo left",weaponClass.loadedMagazine)
 
 end
 
-
-
-UpdateQuickloadPatch() 
```

---

# Migration Report: umf\core\added_hooks.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\added_hooks.lua
+++ patched/umf\core\added_hooks.lua
@@ -1,14 +1,14 @@
+#version 2
+local tool = GetString( "game.player.tool" )
+local invehicle = IsPlayerInVehicle()
+local keyboardkeys = { "esc", "up", "down", "left", "right", "space", "interact", "return" }
+local mousekeys = { "lmb", "rmb", "mmb" }
+local heldkeys = {}
+
 function IsPlayerInVehicle()
 	return GetBool( "game.player.usevehicle" )
 end
 
-local tool = GetString( "game.player.tool" )
-local invehicle = IsPlayerInVehicle()
-
-local keyboardkeys = { "esc", "up", "down", "left", "right", "space", "interact", "return" }
-for i = 97, 97 + 25 do
-	keyboardkeys[#keyboardkeys + 1] = string.char( i )
-end
 local function checkkeys( func, mousehook, keyhook )
 	if hook.used( keyhook ) and func( "any" ) then
 		for i = 1, #keyboardkeys do
@@ -27,64 +27,3 @@
 	end
 end
 
-local mousekeys = { "lmb", "rmb", "mmb" }
-local heldkeys = {}
-
-hook.add( "base.tick", "api.default_hooks", function()
-	if InputLastPressedKey then
-		for i = 1, #mousekeys do
-			local k = mousekeys[i]
-			if InputPressed( k ) then
-				hook.saferun( "api.mouse.pressed", k )
-			elseif InputReleased( k ) then
-				hook.saferun( "api.mouse.released", k )
-			end
-		end
-		local lastkey = InputLastPressedKey()
-		if lastkey ~= "" then
-			heldkeys[lastkey] = true
-			hook.saferun( "api.key.pressed", lastkey )
-		end
-		for key in pairs( heldkeys ) do
-			if not InputDown( key ) then
-				heldkeys[key] = nil
-				hook.saferun( "api.key.released", key )
-				break
-			end
-		end
-		local wheel = InputValue( "mousewheel" )
-		if wheel ~= 0 then
-			hook.saferun( "api.mouse.wheel", wheel )
-		end
-		local mousedx = InputValue( "mousedx" )
-		local mousedy = InputValue( "mousedy" )
-		if mousedx ~= 0 or mousedy ~= 0 then
-			hook.saferun( "api.mouse.move", mousedx, mousedy )
-		end
-	elseif InputPressed then
-		checkkeys( InputPressed, "api.mouse.pressed", "api.key.pressed" )
-		checkkeys( InputReleased, "api.mouse.released", "api.key.released" )
-		local wheel = InputValue( "mousewheel" )
-		if wheel ~= 0 then
-			hook.saferun( "api.mouse.wheel", wheel )
-		end
-		local mousedx = InputValue( "mousedx" )
-		local mousedy = InputValue( "mousedy" )
-		if mousedx ~= 0 or mousedy ~= 0 then
-			hook.saferun( "api.mouse.move", mousedx, mousedy )
-		end
-	end
-
-	local n_invehicle = IsPlayerInVehicle()
-	if invehicle ~= n_invehicle then
-		hook.saferun( n_invehicle and "api.player.enter_vehicle" or "api.player.exit_vehicle",
-		              n_invehicle and GetPlayerVehicle() )
-		invehicle = n_invehicle
-	end
-
-	local n_tool = GetString( "game.player.tool" )
-	if tool ~= n_tool then
-		hook.saferun( "api.player.switch_tool", n_tool, tool )
-		tool = n_tool
-	end
-end )

```

---

# Migration Report: umf\core\console_backend.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\console_backend.lua
+++ patched/umf\core\console_backend.lua
@@ -1,6 +1,5 @@
+#version 2
 local console_buffer = util.shared_buffer( "savegame.mod.console", 128 )
-
--- Console backend --
 
 local function maketext( ... )
 	local text = ""
@@ -15,7 +14,6 @@
 	return text
 end
 
-_OLDPRINT = _OLDPRINT or print
 function printcolor( r, g, b, ... )
 	local text = string.format( "%f;%f;%f;%s", r, g, b, maketext( ... ) )
 	console_buffer:push( text )
@@ -33,8 +31,6 @@
 function warning( msg )
 	printcolor( 1, .7, 0, "[WARNING] " .. tostring( msg ) .. "\n  " .. table.concat( util.stacktrace( 1 ), "\n  " ) )
 end
-
-printwarning = warning
 
 function printerror( ... )
 	printcolor( 1, .2, 0, ... )

```

---

# Migration Report: umf\core\default_hooks.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\default_hooks.lua
+++ patched/umf\core\default_hooks.lua
@@ -1,4 +1,16 @@
+#version 2
 local hook = hook
+local detours = {
+	"init", -- "base.init" (runs before init())
+	"tick", -- "base.tick" (runs before tick())
+	"update", -- "base.update" (runs before update())
+}
+local saved = {}
+local quickloadfix = function()
+	for k, v in pairs( saved ) do
+		_G[k] = v
+	end
+end
 
 local function checkoriginal( b, ... )
 	if not b then
@@ -19,46 +31,9 @@
 	end )
 end
 
-local detours = {
-	"init", -- "base.init" (runs before init())
-	"tick", -- "base.tick" (runs before tick())
-	"update", -- "base.update" (runs before update())
-}
-for i = 1, #detours do
-	simple_detour( detours[i] )
-end
-
 function shoulddraw( kind )
 	return hook.saferun( "api.shoulddraw", kind ) ~= false
 end
-
-DETOUR( "draw", function( original )
-	return function()
-		if shoulddraw( "all" ) then
-			hook.saferun( "base.predraw" )
-			if shoulddraw( "original" ) then
-				checkoriginal( pcall( original ) )
-			end
-			hook.saferun( "base.draw" )
-		end
-	end
-
-end )
-
-DETOUR( "Command", function( original )
-	return function( cmd, ... )
-		hook.saferun( "base.precmd", cmd, { ... } )
-		local a, b, c, d, e, f = original( cmd, ... )
-		hook.saferun( "base.postcmd", cmd, { ... }, { a, b, c, d, e, f } )
-	end
-
-end )
-
------- QUICKSAVE WORKAROUND -----
--- Quicksaving stores a copy of the global table without functions, so libraries get corrupted on quickload
--- This code prevents this by overriding them back
-
-local saved = {}
 
 local function hasfunction( t, bck )
 	if bck[t] then
@@ -83,28 +58,3 @@
 	end
 end
 
-local quickloadfix = function()
-	for k, v in pairs( saved ) do
-		_G[k] = v
-	end
-end
-
-DETOUR( "handleCommand", function( original )
-	return function( command, ... )
-		if command == "quickload" then
-			quickloadfix()
-		end
-		hook.saferun( "base.command." .. command, ... )
-		return original( command, ... )
-	end
-end )
-
---------------------------------
-
-hook.add( "base.tick", "api.firsttick", function()
-	hook.remove( "base.tick", "api.firsttick" )
-	hook.saferun( "api.firsttick" )
-	if type( firsttick ) == "function" then
-		firsttick()
-	end
-end )

```

---

# Migration Report: umf\core\detouring.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\detouring.lua
+++ patched/umf\core\detouring.lua
@@ -1,4 +1,7 @@
+#version 2
 local original = {}
+local detoured = {}
+
 local function call_original( name, ... )
 	local fn = original[name]
 	if fn then
@@ -6,7 +9,6 @@
 	end
 end
 
-local detoured = {}
 function DETOUR( name, generator )
 	original[name] = _G[name]
 	detoured[name] = generator( function( ... )
@@ -15,13 +17,3 @@
 	rawset( _G, name, nil )
 end
 
-setmetatable( _G, {
-	__index = detoured,
-	__newindex = function( self, k, v )
-		if detoured[k] then
-			original[k] = v
-		else
-			rawset( self, k, v )
-		end
-	end,
-} )

```

---

# Migration Report: umf\core\hook.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\hook.lua
+++ patched/umf\core\hook.lua
@@ -1,7 +1,4 @@
-if hook then
-	return
-end
-
+#version 2
 local hook_table = {}
 local hook_compiled = {}
 
@@ -12,8 +9,6 @@
 	end
 	hook_compiled[event] = hooks
 end
-
-hook = { table = hook_table }
 
 function hook.add( event, identifier, func )
 	assert( type( event ) == "string", "Event must be a string" )

```

---

# Migration Report: umf\core\meta.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\meta.lua
+++ patched/umf\core\meta.lua
@@ -1,5 +1,7 @@
+#version 2
 local registered_meta = {}
 local reverse_meta = {}
+local previous = -2
 
 function global_metatable( name, parent )
 	local meta = registered_meta[name]
@@ -62,15 +64,6 @@
 	return res
 end
 
--- I hate this but without a pre-quicksave handler I see no other choice.
-local previous = -2
-hook.add( "base.tick", "api.metatables.save", function( ... )
-	if GetTime() - previous > 2 then
-		previous = GetTime()
-		_G.GLOBAL_META_SAVE = findmeta( _G, {} )
-	end
-end )
-
 local function restoremeta( dst, src )
 	for k, v in pairs( src ) do
 		local dv = dst[k]
@@ -85,8 +78,3 @@
 	end
 end
 
-hook.add( "base.command.quickload", "api.metatables.restore", function( ... )
-	if GLOBAL_META_SAVE then
-		restoremeta( _G, GLOBAL_META_SAVE )
-	end
-end )

```

---

# Migration Report: umf\core\timer.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\timer.lua
+++ patched/umf\core\timer.lua
@@ -1,12 +1,6 @@
-----------------------------------------
---              WARNING               --
---   Timers are reset on quickload!   --
--- Keep this in mind if you use them. --
-----------------------------------------
-timer = {}
-timer._backlog = {}
-
+#version 2
 local backlog = timer._backlog
+local diff = GetTime()
 
 local function sortedinsert( tab, val )
 	for i = #tab, 1, -1 do
@@ -18,8 +12,6 @@
 	end
 	tab[1] = val
 end
-
-local diff = GetTime() -- In certain realms, GetTime() is not 0 right away
 
 function timer.simple( time, callback )
 	sortedinsert( backlog, { time = GetTime() + time - diff, callback = callback } )
@@ -75,20 +67,3 @@
 	end
 end
 
-hook.add( "base.tick", "framework.timer", function( dt )
-	diff = 0
-	local now = GetTime()
-	while #backlog > 0 do
-		local first = backlog[#backlog]
-		if first.time > now then
-			break
-		end
-		backlog[#backlog] = nil
-		first.callback()
-		if first.runsleft and first.runsleft > 0 then
-			first.runsleft = first.runsleft - 1
-			first.time = first.time + first.interval
-			sortedinsert( backlog, first )
-		end
-	end
-end )

```

---

# Migration Report: umf\core\util.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\util.lua
+++ patched/umf\core\util.lua
@@ -1,87 +1,9 @@
-util = {}
-
-do
-	local serialize_any, serialize_table
-
-	serialize_table = function( val, bck )
-		if bck[val] then
-			return "nil"
-		end
-		bck[val] = true
-		local entries = {}
-		for k, v in pairs( val ) do
-			entries[#entries + 1] = string.format( "[%s] = %s", serialize_any( k, bck ), serialize_any( v, bck ) )
-		end
-		return string.format( "{%s}", table.concat( entries, "," ) )
-	end
-
-	serialize_any = function( val, bck )
-		local vtype = type( val )
-		if vtype == "table" then
-			return serialize_table( val, bck )
-		elseif vtype == "string" then
-			return string.format( "%q", val )
-		elseif vtype == "function" or vtype == "userdata" then
-			return string.format( "nil --[[%s]]", tostring( val ) )
-		else
-			return tostring( val )
-		end
-	end
-
-	function util.serialize( ... )
-		local result = {}
-		for i = 1, select( "#", ... ) do
-			result[i] = serialize_any( select( i, ... ), {} )
-		end
-		return table.concat( result, "," )
-	end
-end
-
+#version 2
 function util.unserialize( dt )
 	local fn = loadstring( "return " .. dt )
 	if fn then
 		setfenv( fn, {} )
 		return fn()
-	end
-end
-
-do
-	local function serialize_any( val, bck )
-		local vtype = type( val )
-		if vtype == "table" then
-			if bck[val] then
-				return "{}"
-			end
-			bck[val] = true
-			local len = 0
-			for k, v in pairs( val ) do
-				len = len + 1
-			end
-			local rt = {}
-			if len == #val then
-				for i = 1, #val do
-					rt[i] = serialize_any( val[i], bck )
-				end
-				return string.format( "[%s]", table.concat( rt, "," ) )
-			else
-				for k, v in pairs( val ) do
-					if type( k ) == "string" or type( k ) == "number" then
-						rt[#rt + 1] = string.format( "%s: %s", serialize_any( k, bck ), serialize_any( v, bck ) )
-					end
-				end
-				return string.format( "{%s}", table.concat( rt, "," ) )
-			end
-		elseif vtype == "string" then
-			return string.format( "%q", val )
-		elseif vtype == "function" or vtype == "userdata" or vtype == "nil" then
-			return "null"
-		else
-			return tostring( val )
-		end
-	end
-
-	function util.serializeJSON( val )
-		return serialize_any( val, {} )
 	end
 end
 
@@ -92,8 +14,8 @@
 		_list_name = name .. ".list.",
 		push = function( self, text )
 			local cpos = GetInt( self._pos_name )
-			SetString( self._list_name .. (cpos % max), text )
-			SetInt( self._pos_name, cpos + 1 )
+			SetString( self._list_name .. (cpos % max), text , true)
+			SetInt( self._pos_name, cpos + 1 , true)
 		end,
 		len = function( self )
 			return math.min( GetInt( self._pos_name ), max )
@@ -113,7 +35,7 @@
 			return GetString( self._list_name .. (index % max) )
 		end,
 		clear = function( self )
-			SetInt( self._pos_name, 0 )
+			SetInt( self._pos_name, 0 , true)
 			ClearKey( self._list_name:sub( 1, -2 ) )
 		end,
 	}
@@ -176,7 +98,7 @@
 		end
 	end
 	hook.add( "base.tick", name, function( dt )
-		if channel._ready_count > 0 then
+		if channel._ready_count ~= 0 then
 			local last_pos = channel._buffer:pos()
 			if last_pos > channel._offset then
 				for i = math.max( channel._offset, last_pos - max ), last_pos - 1 do
@@ -228,110 +150,6 @@
 	return listener
 end
 
-do
-
-	local gets, sets = {}, {}
-
-	function util.register_unserializer( type, callback )
-		gets[type] = function( key )
-			return callback( GetString( key ) )
-		end
-	end
-
-	hook.add( "api.newmeta", "api.createunserializer", function( name, meta )
-		gets[name] = function( key )
-			return setmetatable( {}, meta ):__unserialize( GetString( key ) )
-		end
-		sets[name] = function( key, value )
-			return SetString( key, meta.__serialize( value ) )
-		end
-	end )
-
-	function util.shared_table( name, base )
-		return setmetatable( base or {}, {
-			__index = function( self, k )
-				local key = tostring( k )
-				local vtype = GetString( string.format( "%s.%s.type", name, key ) )
-				if vtype == "" then
-					return
-				end
-				return gets[vtype]( string.format( "%s.%s.val", name, key ) )
-			end,
-			__newindex = function( self, k, v )
-				local vtype = type( v )
-				local handler = sets[vtype]
-				if not handler then
-					return
-				end
-				local key = tostring( k )
-				if vtype == "table" then
-					local meta = getmetatable( v )
-					if meta and meta.__serialize and meta.__type then
-						vtype = meta.__type
-						v = meta.__serialize( v )
-						handler = sets.string
-					end
-				end
-				SetString( string.format( "%s.%s.type", name, key ), vtype )
-				handler( string.format( "%s.%s.val", name, key ), v )
-			end,
-		} )
-	end
-
-	function util.structured_table( name, base )
-		local function generate( base )
-			local root = {}
-			local keys = {}
-			for k, v in pairs( base ) do
-				local key = name .. "." .. tostring( k )
-				if type( v ) == "table" then
-					root[k] = util.structured_table( key, v )
-				elseif type( v ) == "string" then
-					keys[k] = { type = v, key = key }
-				else
-					root[k] = v
-				end
-			end
-			return setmetatable( root, {
-				__index = function( self, k )
-					local entry = keys[k]
-					if entry and gets[entry.type] then
-						return gets[entry.type]( entry.key )
-					end
-				end,
-				__newindex = function( self, k, v )
-					local entry = keys[k]
-					if entry and sets[entry.type] then
-						return sets[entry.type]( entry.key, v )
-					end
-				end,
-			} )
-		end
-		if type( base ) == "table" then
-			return generate( base )
-		end
-		return generate
-	end
-
-	gets.number = GetFloat
-	gets.integer = GetInt
-	gets.boolean = GetBool
-	gets.string = GetString
-	gets.table = util.shared_table
-
-	sets.number = SetFloat
-	sets.integer = SetInt
-	sets.boolean = SetBool
-	sets.string = SetString
-	sets.table = function( key, val )
-		local tab = util.shared_table( key )
-		for k, v in pairs( val ) do
-			tab[k] = v
-		end
-	end
-
-end
-
 function util.current_line( level )
 	level = (level or 0) + 3
 	local _, line = pcall( error, "-", level )
@@ -366,3 +184,4 @@
 	end
 	return stack
 end
+

```

---

# Migration Report: umf\core\xml.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\core\xml.lua
+++ patched/umf\core\xml.lua
@@ -1,3 +1,4 @@
+#version 2
 local meta = {
 	__call = function( self, children )
 		self.children = children
@@ -22,104 +23,3 @@
 	},
 }
 
-XMLTag = function( type )
-	return function( attributes )
-		return setmetatable( { type = type, attributes = attributes }, meta )
-	end
-end
-
-ParseXML = function( xml )
-	local pos = 1
-	local function skipw()
-		local next = xml:find( "[^ \t\n]", pos )
-		if not next then
-			return false
-		end
-		pos = next
-		return true
-	end
-	local function expect( pattern, noskip )
-		if not noskip then
-			if not skipw() then
-				return false
-			end
-		end
-		local s, e = xml:find( pattern, pos )
-		if not s then
-			return false
-		end
-		local pre = pos
-		pos = e + 1
-		return xml:match( pattern, pre )
-	end
-
-	local readtag, readattribute, readstring
-
-	local rt = { n = "\n", t = "\t", r = "\r", ["0"] = "\0", ["\\"] = "\\", ["\""] = "\"" }
-	readstring = function()
-		if not expect( "^\"" ) then
-			return false
-		end
-		local start = pos
-		while true do
-			local s = assert( xml:find( "[\\\"]", pos ), "Invalid string" )
-			if xml:sub( s, s ) == "\\" then
-				pos = s + 2
-			else
-				pos = s + 1
-				break
-			end
-		end
-		return xml:sub( start, pos - 2 ):gsub( "\\(.)", rt )
-	end
-
-	readattribute = function()
-		local name = expect( "^([%d%w_]+)" )
-		if not name then
-			return false
-		end
-		if expect( "^=" ) then
-			return name, assert( readstring() )
-		else
-			return name, "1"
-		end
-	end
-
-	readtag = function()
-		local save = pos
-		if not expect( "^<" ) then
-			return false
-		end
-
-		local type = expect( "^([%d%w_]+)" )
-		if not type then
-			pos = save
-			return false
-		end
-		skipw()
-
-		local attributes = {}
-		repeat
-			local attr, val = readattribute()
-			if attr then
-				attributes[attr] = val
-			end
-		until not attr
-
-		local children = {}
-		if not expect( "^/>" ) then
-			assert( expect( "^>" ) )
-			repeat
-				local child = readtag()
-				if child then
-					children[#children + 1] = child
-				end
-			until not child
-			assert( expect( "^</" ) and expect( "^" .. type ) and expect( "^>" ) )
-		end
-
-		return XMLTag( type )( attributes )( children )
-	end
-
-	return readtag()
-end

```

---

# Migration Report: umf\extension\meta\armature.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\armature.lua
+++ patched/umf\extension\meta\armature.lua
@@ -1,84 +1,5 @@
+#version 2
 local armature_meta = global_metatable( "armature" )
-
---[[
-
-Armature {
-    shapes = {
-        "core_2",
-        "core_1",
-        "core_0",
-        "arm_21",
-        "arm_11",
-        "arm_01",
-        "arm_20",
-        "arm_10",
-        "arm_00",
-        "body"
-    },
-
-    bones = {
-        name = "root",
-        shapes = {
-            body = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-        },
-        {
-            name = "core_0",
-            shapes = {
-                core_0 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "core_1",
-            shapes = {
-                core_1 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "core_2",
-            shapes = {
-                core_2 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-        },
-        {
-            name = "arm_00",
-            shapes = {
-                arm_00 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_01",
-                shapes = {
-                    arm_01 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-        {
-            name = "arm_10",
-            shapes = {
-                arm_10 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_11",
-                shapes = {
-                    arm_11 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-        {
-            name = "arm_20",
-            shapes = {
-                arm_20 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-            },
-            {
-                name = "arm_21",
-                shapes = {
-                    arm_21 = Transformation(Vec(0,0,0), QuatEuler(0,0,0)),
-                },
-            },
-        },
-    }
-}
-
-]]
 
 function Armature( definition )
 	local ids = {}
@@ -189,7 +110,7 @@
 		return
 	end
 	self.dirty = true
-	if jiggle > 0 then
+	if jiggle ~= 0 then
 		self.jiggle = true
 	end
 	b.jiggle = math.atan( jiggle ) / math.pi * 2
@@ -327,83 +248,4 @@
 	arm:ComputeBones()
 	return arm, dt
 end
---[=[
---[[---------------------------------------------------
-    LoadArmatureFromXML is capable of taking the XML of a prefab and turning it into a useable armature object for tools and such.
-    Two things are required: the XML of the prefab itself, and a list of all the objects inside the vox for position correction.
-    The list of objects should be as it appears in MagicaVoxel, with every slot corresponding to an object in the vox file.
-    One notable limitation is that there can only be one vox file used and that all the objects inside it can only be used once.
---]]---------------------------------------------------
-
--- Loading the armature from the prefab and the objects list
-local armature = LoadArmatureFromXML([[
-<prefab version="0.7.0">
-    <group id_="1196432640" open_="true" name="instance=MOD/physgun.xml" pos="-3.4 0.7 0.0" rot="0.0 0.0 0.0">
-        <vox id_="1866644736" pos="-0.125 -0.125 0.125" file="MOD/physgun.vox" object="body" scale="0.5"/>
-        <group id_="279659168" open_="true" name="core0" pos="0.0 0.0 -0.075" rot="0.0 0.0 0.0">
-            <vox id_="496006720" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_0" scale="0.5"/>
-        </group>
-        <group id_="961930560" open_="true" name="core1" pos="0.0 0.0 -0.175" rot="0.0 0.0 0.0">
-            <vox id_="1109395584" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_1" scale="0.5"/>
-        </group>
-        <group id_="806535232" open_="true" name="core2" pos="0.0 0.0 -0.275" rot="0.0 0.0 0.0">
-            <vox id_="378362432" pos="-0.025 -0.125 0.0" rot="0.0 0.0 0.0" file="MOD/physgun.vox" object="core_2" scale="0.5"/>
-        </group>
-        <group id_="1255943040" open_="true" name="arms_rot" pos="0.0 0.0 -0.375" rot="0.0 0.0 0.0">
-            <group id_="439970016" open_="true" name="arm0_base" pos="0.0 0.1 0.0" rot="0.0 0.0 0.0">
-                <vox id_="1925106432" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_00" scale="0.5"/>
-                <group id_="2122316288" open_="true" name="arm0_tip" pos="0.0 0.2 -0.0" rot="0.0 0.0 0.0">
-                    <vox id_="572557440" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_01" scale="0.5"/>
-                </group>
-            </group>
-            <group id_="516324128" open_="true" name="arm1_base" pos="0.087 -0.05 0.0" rot="180.0 180.0 -60.0">
-                <vox id_="28575440" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_10" scale="0.5"/>
-                <group id_="962454912" open_="true" name="arm1_tip" pos="0.0 0.2 0.0" rot="0.0 0.0 0.0">
-                    <vox id_="1966724352" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_11" scale="0.5"/>
-                </group>
-            </group>
-            <group id_="634361664" open_="true" name="arm2_base" pos="-0.087 -0.05 0.0" rot="180.0 180.0 60.0">
-                <vox id_="1049360960" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_20" scale="0.5"/>
-                <group id_="1428116608" open_="true" name="arm2_tip" pos="0.0 0.2 0.0" rot="0.0 0.0 0.0">
-                    <vox id_="1388661504" pos="-0.025 0.0 0.025" file="MOD/physgun.vox" object="arm_21" scale="0.5"/>
-                </group>
-            </group>
-        </group>
-        <group id_="1569551872" open_="true" name="nozzle" pos="0.0 0.0 -0.475">
-            <vox id_="506099872" pos="-0.025 -0.125 0.1" file="MOD/physgun.vox" object="cannon" scale="0.5"/>
-        </group>
-    </group>
-</prefab>
-]], {
-    -- The list of objects as it appears in MagicaVoxel. Each entry has the name of the object followed by the size as seen in MagicaVoxel.
-    -- Please note that the order MUST be the same as in MagicaVoxel and that there can be no gaps.
-    {"cannon", Vec(5, 3, 5)},
-    {"core_2", Vec(5, 2, 5)},
-    {"core_1", Vec(5, 2, 5)},
-    {"core_0", Vec(5, 2, 5)},
-    {"arm_21", Vec(1, 1, 2)},
-    {"arm_11", Vec(1, 1, 2)},
-    {"arm_01", Vec(1, 1, 2)},
-    {"arm_20", Vec(1, 1, 4)},
-    {"arm_10", Vec(1, 1, 4)},
-    {"arm_00", Vec(1, 1, 4)},
-    {"body", Vec(9, 6, 5)}
-})
------------------------------------------------------
-
--- Every frame you can animate the armature by setting the local transform of bones and then applying the changes to the shapes of the object.
-armature:SetBoneTransform("core0", Transform(Vec(), QuatEuler(0, 0, GetTime()*73)))
-armature:SetBoneTransform("core1", Transform(Vec(), QuatEuler(0, 0, -GetTime()*45)))
-armature:SetBoneTransform("core2", Transform(Vec(), QuatEuler(0, 0, GetTime()*83)))
-armature:SetBoneTransform("arms_rot", Transform(Vec(), QuatEuler(0, 0, GetTime()*20)))
-local tr = Transform(Vec(0,0,0), QuatEuler(-40 + 5 * math.sin(GetTime()), 0, 0))
-armature:SetBoneTransform("arm0_base", tr)
-armature:SetBoneTransform("arm0_tip", tr)
-armature:SetBoneTransform("arm1_base", tr)
-armature:SetBoneTransform("arm1_tip", tr)
-armature:SetBoneTransform("arm2_base", tr)
-armature:SetBoneTransform("arm2_tip", tr)
--- shapes is the list of all the shapes of the vox, it can be obtained with GetBodyShapes()
-armature:Apply(shapes)
-
---]=]
+

```

---

# Migration Report: umf\extension\meta\body.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\body.lua
+++ patched/umf\extension\meta\body.lua
@@ -1,3 +1,4 @@
+#version 2
 local body_meta = global_metatable( "body", "entity" )
 
 function IsBody( e )
@@ -5,7 +6,7 @@
 end
 
 function Body( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "body" }, body_meta )
 	end
 end
@@ -124,3 +125,4 @@
 	assert( self:IsValid() )
 	return IsBodyJointedToStatic( self.handle )
 end
+

```

---

# Migration Report: umf\extension\meta\entity.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\entity.lua
+++ patched/umf\extension\meta\entity.lua
@@ -1,4 +1,12 @@
+#version 2
 local entity_meta = global_metatable( "entity" )
+local IsHandleValid = IsHandleValid
+local SetTag = SetTag
+local RemoveTag = RemoveTag
+local HasTag = HasTag
+local GetTagValue = GetTagValue
+local GetDescription = GetDescription
+local Delete = Delete
 
 function GetEntityHandle( e )
 	if IsEntity( e ) then
@@ -19,7 +27,7 @@
 end
 
 function Entity( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "unknown" }, entity_meta )
 	end
 end
@@ -41,42 +49,36 @@
 	return self.type
 end
 
-local IsHandleValid = IsHandleValid
 function entity_meta:IsValid()
 	return IsHandleValid( self.handle )
 end
 
-local SetTag = SetTag
 function entity_meta:SetTag( tag, value )
 	assert( self:IsValid() )
 	return SetTag( self.handle, tag, value )
 end
 
-local RemoveTag = RemoveTag
 function entity_meta:RemoveTag( tag )
 	assert( self:IsValid() )
 	return RemoveTag( self.handle, tag )
 end
 
-local HasTag = HasTag
 function entity_meta:HasTag( tag )
 	assert( self:IsValid() )
 	return HasTag( self.handle, tag )
 end
 
-local GetTagValue = GetTagValue
 function entity_meta:GetTagValue( tag )
 	assert( self:IsValid() )
 	return GetTagValue( self.handle, tag )
 end
 
-local GetDescription = GetDescription
 function entity_meta:GetDescription()
 	assert( self:IsValid() )
 	return GetDescription( self.handle )
 end
 
-local Delete = Delete
 function entity_meta:Delete()
 	return Delete( self.handle )
 end
+

```

---

# Migration Report: umf\extension\meta\joint.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\joint.lua
+++ patched/umf\extension\meta\joint.lua
@@ -1,3 +1,4 @@
+#version 2
 local joint_meta = global_metatable( "joint", "entity" )
 
 function IsJoint( e )
@@ -5,7 +6,7 @@
 end
 
 function Joint( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "joint" }, joint_meta )
 	end
 end

```

---

# Migration Report: umf\extension\meta\light.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\light.lua
+++ patched/umf\extension\meta\light.lua
@@ -1,3 +1,4 @@
+#version 2
 local light_meta = global_metatable( "light", "entity" )
 
 function IsLight( e )
@@ -5,7 +6,7 @@
 end
 
 function Light( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "light" }, light_meta )
 	end
 end
@@ -55,3 +56,4 @@
 	assert( self:IsValid() )
 	return IsPointAffectedByLight( self.handle, point )
 end
+

```

---

# Migration Report: umf\extension\meta\location.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\location.lua
+++ patched/umf\extension\meta\location.lua
@@ -1,3 +1,4 @@
+#version 2
 local location_meta = global_metatable( "location", "entity" )
 
 function IsLocation( e )
@@ -5,7 +6,7 @@
 end
 
 function Location( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "location" }, location_meta )
 	end
 end
@@ -30,3 +31,4 @@
 	assert( self:IsValid() )
 	return MakeTransformation( GetLocationTransform( self.handle ) )
 end
+

```

---

# Migration Report: umf\extension\meta\player.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\player.lua
+++ patched/umf\extension\meta\player.lua
@@ -1,6 +1,5 @@
+#version 2
 local player_meta = global_metatable( "player" )
-
-PLAYER = setmetatable( {}, player_meta )
 
 function player_meta:__unserialize( data )
 	return self
@@ -19,11 +18,11 @@
 end
 
 function player_meta:Respawn()
-	return RespawnPlayer()
+	return RespawnPlayer(playerId)
 end
 
 function player_meta:SetTransform( transform )
-	return SetPlayerTransform( transform )
+	return SetPlayerTransform(playerId,  transform )
 end
 
 function player_meta:SetCamera( transform )
@@ -35,11 +34,11 @@
 end
 
 function player_meta:SetVehicle( handle )
-	return SetPlayerVehicle( GetEntityHandle( handle ) )
+	return SetPlayerVehicle(playerId,  GetEntityHandle( handle ) )
 end
 
 function player_meta:SetVelocity( velocity )
-	return SetPlayerVelocity( velocity )
+	return SetPlayerVelocity(playerId,  velocity )
 end
 
 function player_meta:SetScreen( handle )
@@ -47,11 +46,11 @@
 end
 
 function player_meta:SetHealth( health )
-	return SetPlayerHealth( health )
+	return SetPlayerHealth(playerId,  health )
 end
 
 function player_meta:GetTransform()
-	return MakeTransformation( GetPlayerTransform() )
+	return MakeTransformation( GetPlayerTransform(playerId) )
 end
 
 function player_meta:GetCamera()
@@ -59,35 +58,35 @@
 end
 
 function player_meta:GetVelocity()
-	return MakeVector( GetPlayerVelocity() )
+	return MakeVector( GetPlayerVelocity(playerId) )
 end
 
 function player_meta:GetVehicle()
-	return Vehicle( GetPlayerVehicle() )
+	return Vehicle( GetPlayerVehicle(playerId) )
 end
 
 function player_meta:GetGrabShape()
-	return Shape( GetPlayerGrabShape() )
+	return Shape( GetPlayerGrabShape(playerId) )
 end
 
 function player_meta:GetGrabBody()
-	return Body( GetPlayerGrabBody() )
+	return Body( GetPlayerGrabBody(playerId) )
 end
 
 function player_meta:GetPickShape()
-	return Shape( GetPlayerPickShape() )
+	return Shape( GetPlayerPickShape(playerId) )
 end
 
 function player_meta:GetPickBody()
-	return Body( GetPlayerPickBody() )
+	return Body( GetPlayerPickBody(playerId) )
 end
 
 function player_meta:GetInteractShape()
-	return Shape( GetPlayerInteractShape() )
+	return Shape( GetPlayerInteractShape(playerId) )
 end
 
 function player_meta:GetInteractBody()
-	return Body( GetPlayerInteractBody() )
+	return Body( GetPlayerInteractBody(playerId) )
 end
 
 function player_meta:GetScreen()
@@ -95,5 +94,6 @@
 end
 
 function player_meta:GetHealth()
-	return GetPlayerHealth()
+	return GetPlayerHealth(playerId)
 end
+

```

---

# Migration Report: umf\extension\meta\quat.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\quat.lua
+++ patched/umf\extension\meta\quat.lua
@@ -1,5 +1,8 @@
+#version 2
 local vector_meta = global_metatable( "vector" )
 local quat_meta = global_metatable( "quaternion" )
+local QuatStr = QuatStr
+local QuatSlerp = QuatSlerp
 
 function IsQuaternion( q )
 	return type( q ) == "table" and type( q[1] ) == "number" and type( q[2] ) == "number" and type( q[3] ) == "number" and
@@ -30,13 +33,10 @@
 	return table.concat( self, ";" )
 end
 
-QUAT_ZERO = Quaternion()
-
 function quat_meta:Clone()
 	return MakeQuaternion { self[1], self[2], self[3], self[4] }
 end
 
-local QuatStr = QuatStr
 function quat_meta:__tostring()
 	return QuatStr( self )
 end
@@ -125,7 +125,6 @@
 	return math.sqrt( quat_meta.LengthSquare( self ) )
 end
 
-local QuatSlerp = QuatSlerp
 function quat_meta:Slerp( o, n )
 	return MakeQuaternion( QuatSlerp( self, o, n ) )
 end
@@ -173,3 +172,4 @@
 
 	return math.deg( bank ), math.deg( heading ), math.deg( attitude )
 end
+

```

---

# Migration Report: umf\extension\meta\screen.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\screen.lua
+++ patched/umf\extension\meta\screen.lua
@@ -1,3 +1,4 @@
+#version 2
 local screen_meta = global_metatable( "screen", "entity" )
 
 function IsScreen( e )
@@ -5,7 +6,7 @@
 end
 
 function Screen( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "screen" }, screen_meta )
 	end
 end
@@ -40,3 +41,4 @@
 	assert( self:IsValid() )
 	return IsScreenEnabled( self.handle )
 end
+

```

---

# Migration Report: umf\extension\meta\shape.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\shape.lua
+++ patched/umf\extension\meta\shape.lua
@@ -1,3 +1,4 @@
+#version 2
 local shape_meta = global_metatable( "shape", "entity" )
 
 function IsShape( e )
@@ -5,7 +6,7 @@
 end
 
 function Shape( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "shape" }, shape_meta )
 	end
 end
@@ -93,3 +94,4 @@
 function shape_meta:IsBroken()
 	return not self:IsValid() or IsShapeBroken( self.handle )
 end
+

```

---

# Migration Report: umf\extension\meta\transform.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\transform.lua
+++ patched/umf\extension\meta\transform.lua
@@ -1,6 +1,14 @@
+#version 2
 local vector_meta = global_metatable( "vector" )
 local quat_meta = global_metatable( "quaternion" )
 local transform_meta = global_metatable( "transformation" )
+local TransformStr = TransformStr
+local TransformToLocalPoint = TransformToLocalPoint
+local TransformToLocalTransform = TransformToLocalTransform
+local TransformToLocalVec = TransformToLocalVec
+local TransformToParentPoint = TransformToParentPoint
+local TransformToParentTransform = TransformToParentTransform
+local TransformToParentVec = TransformToParentVec
 
 function IsTransformation( v )
 	return type( v ) == "table" and v.pos and v.rot
@@ -32,17 +40,9 @@
 	return MakeTransformation { pos = vector_meta.Clone( self.pos ), rot = quat_meta.Clone( self.rot ) }
 end
 
-local TransformStr = TransformStr
 function transform_meta:__tostring()
 	return TransformStr( self )
 end
-
-local TransformToLocalPoint = TransformToLocalPoint
-local TransformToLocalTransform = TransformToLocalTransform
-local TransformToLocalVec = TransformToLocalVec
-local TransformToParentPoint = TransformToParentPoint
-local TransformToParentTransform = TransformToParentTransform
-local TransformToParentVec = TransformToParentVec
 
 function transform_meta.__add( a, b )
 	if not IsTransformation( b ) then
@@ -93,3 +93,4 @@
 		hitpos = vector_meta.__add( self.pos, vector_meta.Mul( dir, hit and dist2 or dist ) ),
 	}
 end
+

```

---

# Migration Report: umf\extension\meta\trigger.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\trigger.lua
+++ patched/umf\extension\meta\trigger.lua
@@ -1,3 +1,4 @@
+#version 2
 local trigger_meta = global_metatable( "trigger", "entity" )
 
 function IsTrigger( e )
@@ -5,7 +6,7 @@
 end
 
 function Trigger( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "trigger" }, trigger_meta )
 	end
 end
@@ -60,3 +61,4 @@
 	assert( self:IsValid() )
 	return IsTriggerEmpty( self.handle, demolision )
 end
+

```

---

# Migration Report: umf\extension\meta\vector.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\vector.lua
+++ patched/umf\extension\meta\vector.lua
@@ -1,5 +1,12 @@
+#version 2
 local vector_meta = global_metatable( "vector" )
 local quat_meta = global_metatable( "quaternion" )
+local VecStr = VecStr
+local VecDot = VecDot
+local VecCross = VecCross
+local VecLength = VecLength
+local VecLerp = VecLerp
+local VecNormalize = VecNormalize
 
 function IsVector( v )
 	return type( v ) == "table" and type( v[1] ) == "number" and type( v[2] ) == "number" and type( v[3] ) == "number" and
@@ -29,16 +36,10 @@
 	return table.concat( self, ";" )
 end
 
-VEC_ZERO = Vector()
-VEC_FORWARD = Vector( 0, 0, 1 )
-VEC_UP = Vector( 0, 1, 0 )
-VEC_LEFT = Vector( 1, 0, 0 )
-
 function vector_meta:Clone()
 	return MakeVector { self[1], self[2], self[3] }
 end
 
-local VecStr = VecStr
 function vector_meta:__tostring()
 	return VecStr( self )
 end
@@ -170,17 +171,14 @@
 	return a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and (a[3] <= b[3]))))
 end
 
-local VecDot = VecDot
 function vector_meta:Dot( b )
 	return MakeVector( VecDot( self, b ) )
 end
 
-local VecCross = VecCross
 function vector_meta:Cross( b )
 	return MakeVector( VecCross( self, b ) )
 end
 
-local VecLength = VecLength
 function vector_meta:Length()
 	return VecLength( self )
 end
@@ -189,12 +187,10 @@
 	return math.abs( self[1] * self[2] * self[3] )
 end
 
-local VecLerp = VecLerp
 function vector_meta:Lerp( o, n )
 	return MakeVector( VecLerp( self, o, n ) )
 end
 
-local VecNormalize = VecNormalize
 function vector_meta:Normalized()
 	return MakeVector( VecNormalize( self ) )
 end
@@ -214,3 +210,4 @@
 function vector_meta:LookAt( o )
 	return MakeQuaternion( QuatLookAt( self, o ) )
 end
+

```

---

# Migration Report: umf\extension\meta\vehicle.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\meta\vehicle.lua
+++ patched/umf\extension\meta\vehicle.lua
@@ -1,3 +1,4 @@
+#version 2
 local vehicle_meta = global_metatable( "vehicle", "entity" )
 
 function IsVehicle( e )
@@ -5,7 +6,7 @@
 end
 
 function Vehicle( handle )
-	if handle > 0 then
+	if handle ~= 0 then
 		return setmetatable( { handle = handle, type = "vehicle" }, vehicle_meta )
 	end
 end
@@ -44,3 +45,4 @@
 function vehicle_meta:GetGlobalDriverPos()
 	return self:GetTransform():ToGlobal( self:GetDriverPos() )
 end
+

```

---

# Migration Report: umf\extension\tool_loader.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\tool_loader.lua
+++ patched/umf\extension\tool_loader.lua
@@ -1,3 +1,4 @@
+#version 2
 local tool_meta = {
 	__index = {
 		DrawInWorld = function( self, transform )
@@ -37,8 +38,9 @@
 		end,
 	},
 }
+local extra_tools = {}
+local prev
 
-local extra_tools = {}
 function RegisterToolUMF( id, data )
 	if LoadArmatureFromXML and type( data.model ) == "table" then
 		local arm, xml = LoadArmatureFromXML( data.model.prefab, data.model.objects, data.model.scale )
@@ -62,113 +64,10 @@
 	data.id = id
 	extra_tools[id] = data
 	RegisterTool( id, data.printname or id, data.model or "" )
-	SetBool( "game.tool." .. id .. ".enabled", true )
+	SetBool( "game.tool." .. id .. ".enabled", true , true)
 end
 
 local function istoolactive()
 	return GetBool( "game.player.canusetool" )
 end
 
-local prev
-hook.add( "api.mouse.wheel", "api.tool_loader", function( ds )
-	if not istoolactive() then
-		return
-	end
-	local tool = prev and extra_tools[prev]
-	if tool and tool.MouseWheel then
-		tool:MouseWheel( ds )
-	end
-end )
-
-hook.add( "base.tick", "api.tool_loader", function( dt )
-	local cur = GetString( "game.player.tool" )
-
-	local prevtool = prev and extra_tools[prev]
-	if prevtool then
-		if prevtool.ShouldLockMouseWheel then
-			local s, b = softassert( pcall( prevtool.ShouldLockMouseWheel, prevtool ) )
-			if s then
-				SetBool( "game.input.locktool", not not b )
-			end
-			if b then
-				SetString( "game.player.tool", prev )
-				cur = prev
-			end
-		end
-		if prev ~= cur and prevtool.Holster then
-			softassert( pcall( prevtool.Holster, prevtool ) )
-		end
-	end
-
-	local tool = extra_tools[cur]
-	if tool then
-		if prev ~= cur then
-			if tool.Deploy then
-				softassert( pcall( tool.Deploy, tool ) )
-			end
-			if tool._ARMATURE then
-				tool._ARMATURE:ResetJiggle()
-			end
-		end
-		local body = GetToolBody()
-		if not tool._BODY or tool._BODY.handle ~= body then
-			tool._BODY = Body( body )
-			tool._SHAPES = tool._BODY and tool._BODY:GetShapes()
-		end
-		if tool._BODY then
-			tool._TRANSFORM = tool._BODY:GetTransform()
-			tool._TRANSFORM_DIFF = tool._TRANSFORM_OLD and tool._TRANSFORM:ToLocal( tool._TRANSFORM_OLD ) or
-			                       Transformation( Vec(), Quat() )
-			local reverse_diff = tool._TRANSFORM_OLD and tool._TRANSFORM_OLD:ToLocal( tool._TRANSFORM ) or
-			                     Transformation( Vec(), Quat() )
-			-- reverse_diff.pos = VecScale(reverse_diff.pos, 60 * dt)
-			tool._TRANSFORM_FIX = tool._TRANSFORM:ToGlobal( reverse_diff )
-			if tool.Animate then
-				softassert( pcall( tool.Animate, tool, tool._BODY, tool._SHAPES ) )
-			end
-			if tool._ARMATURE then
-				tool._ARMATURE:UpdatePhysics( tool:GetTransformDelta(), GetTimeStep(),
-				                              TransformToLocalVec( tool:GetTransform(), Vec( 0, -10, 0 ) ) )
-				tool._ARMATURE:Apply( tool._SHAPES )
-			end
-		end
-		if tool.Tick then
-			softassert( pcall( tool.Tick, tool, dt ) )
-		end
-		if tool._TRANSFORM then
-			tool._TRANSFORM_OLD = tool._TRANSFORM
-		end
-	end
-	prev = cur
-end )
-
-hook.add( "api.firsttick", "api.tool_loader", function()
-	for id, tool in pairs( extra_tools ) do
-		if tool.Initialize then
-			softassert( pcall( tool.Initialize, tool ) )
-		end
-	end
-end )
-
-hook.add( "base.draw", "api.tool_loader", function()
-	local tool = extra_tools[GetString( "game.player.tool" )]
-	if tool and tool.Draw then
-		softassert( pcall( tool.Draw, tool ) )
-	end
-end )
-
-hook.add( "api.mouse.pressed", "api.tool_loader", function( button )
-	local tool = extra_tools[GetString( "game.player.tool" )]
-	local event = button == "lmb" and "LeftClick" or "RightClick"
-	if tool and tool[event] and istoolactive() then
-		softassert( pcall( tool[event], tool ) )
-	end
-end )
-
-hook.add( "api.mouse.released", "api.tool_loader", function( button )
-	local tool = extra_tools[GetString( "game.player.tool" )]
-	local event = button == "lmb" and "LeftClickReleased" or "RightClickReleased"
-	if tool and tool[event] and istoolactive() then
-		softassert( pcall( tool[event], tool ) )
-	end
-end )

```

---

# Migration Report: umf\extension\visual.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\extension\visual.lua
+++ patched/umf\extension\visual.lua
@@ -1,260 +1 @@
-visual = {}
-degreeToRadian = math.pi / 180
-COLOR_WHITE = { r = 255 / 255, g = 255 / 255, b = 255 / 255, a = 255 / 255 }
-COLOR_BLACK = { r = 0, g = 0, b = 0, a = 255 / 255 }
-COLOR_RED = { r = 255 / 255, g = 0, b = 0, a = 255 / 255 }
-COLOR_ORANGE = { r = 255 / 255, g = 128 / 255, b = 0, a = 255 / 255 }
-COLOR_YELLOW = { r = 255 / 255, g = 255 / 255, b = 0, a = 255 / 255 }
-COLOR_GREEN = { r = 0, g = 255 / 255, b = 0, a = 255 / 255 }
-COLOR_CYAN = { r = 0, g = 255 / 255, b = 128 / 255, a = 255 / 255 }
-COLOR_AQUA = { r = 0, g = 255 / 255, b = 255 / 255, a = 255 / 255 }
-COLOR_BLUE = { r = 0, g = 0, b = 255 / 255, a = 255 / 255 }
-COLOR_VIOLET = { r = 128 / 255, g = 0, b = 255 / 255, a = 255 / 255 }
-COLOR_PINK = { r = 255 / 255, g = 0, b = 255 / 255, a = 255 / 255 }
-
-if DrawSprite then
-	function visual.drawsprite( sprite, source, radius, info )
-		local r, g, b, a
-		local writeZ, additive = true, false
-		local target = GetCameraTransform().pos
-		local DrawFunction = DrawSprite
-
-		radius = radius or 1
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			target = info.target or target
-			if info.writeZ ~= nil then
-				writeZ = info.writeZ
-			end
-			if info.additive ~= nil then
-				additive = info.additive
-			end
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or DrawFunction
-		end
-
-		DrawFunction( sprite, Transform( source, QuatLookAt( source, target ) ), radius, radius, r, g, b, a, writeZ, additive )
-	end
-
-	function visual.drawsprites( sprites, sources, radius, info )
-		sprites = type( sprites ) ~= "table" and { sprites } or sprites
-
-		for i = 1, #sprites do
-			for j = 1, #sources do
-				visual.drawsprite( sprites[i], sources[j], radius, info )
-			end
-		end
-	end
-
-	function visual.drawline( sprite, source, destination, info )
-		local r, g, b, a
-		local writeZ, additive = true, false
-		local target = GetCameraTransform().pos
-		local DrawFunction = DrawLine
-		local width = 0.03
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			width = info.width or width
-			target = info.target or target
-			if info.writeZ ~= nil then
-				writeZ = info.writeZ
-			end
-			if info.additive ~= nil then
-				additive = info.additive
-			end
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		if sprite then
-			local middle = VecScale( VecAdd( source, destination ), .5 )
-			local len = VecLength( VecSub( source, destination ) )
-			local transform = Transform( middle, QuatRotateQuat( QuatLookAt( source, destination ), QuatEuler( -90, 0, 0 ) ) )
-			local target_local = TransformToLocalPoint( transform, target )
-			target_local[2] = 0
-			local transform_fixed = TransformToParentTransform( transform, Transform( nil, QuatLookAt( target_local, nil ) ) )
-
-			DrawSprite( sprite, transform_fixed, width, len, r, g, b, a, writeZ, additive )
-		else
-			DrawFunction( source, destination, r, g, b, a );
-		end
-	end
-
-	function visual.drawlines( sprites, sources, connect, info )
-		sprites = type( sprites ) ~= "table" and { sprites } or sprites
-
-		for i = 1, #sprites do
-			local sourceCount = #sources
-
-			for j = 1, sourceCount - 1 do
-				visual.drawline( sprites[i], sources[j], sources[j + 1], info )
-			end
-
-			if connect then
-				visual.drawline( sprites[i], sources[1], sources[sourceCount], info )
-			end
-		end
-	end
-
-	function visual.drawaxis( transform, quat, radius, writeZ )
-		local DrawFunction = writeZ and DrawLine or DebugLine
-
-		if not transform.pos then
-			transform = Transform( transform, quat or QUAT_ZERO )
-		end
-		radius = radius or 1
-
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( radius, 0, 0 ) ), 1, 0, 0 )
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, radius, 0 ) ), 0, 1, 0 )
-		DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, 0, radius ) ), 0, 0, 1 )
-	end
-
-	function visual.drawpolygon( transform, radius, rotation, sides, info )
-		local points = {}
-		local iteration = 1
-		local pow, sqrt, sin, cos = math.pow, math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-		
-		radius = sqrt(2 * pow(radius, 2)) or sqrt(2)
-		rotation = rotation or 0
-		sides = sides or 4
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		for v = 0, 360, 360 / sides do
-			points[iteration] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius, 0,
-			                                                            cos( (v + rotation) * degreeToRadian ) * radius ) )
-			points[iteration + 1] = TransformToParentPoint( transform,
-			                                                Vec( sin( ((v + 360 / sides) + rotation) * degreeToRadian ) * radius,
-			                                                     0,
-			                                                     cos( ((v + 360 / sides) + rotation) * degreeToRadian ) * radius ) )
-			if iteration > 2 then
-				DrawFunction( points[iteration], points[iteration + 1], r, g, b, a )
-			end
-			iteration = iteration + 2
-		end
-
-		return points
-	end
-
-	function visual.drawbox(transform, min, max, info)
-		local r, g, b, a
-		local DrawFunction = DrawLine
-		local points = {
-			TransformToParentPoint(transform, Vec(min[1], min[2], min[3])),
-			TransformToParentPoint(transform, Vec(max[1], min[2], min[3])),
-			TransformToParentPoint(transform, Vec(min[1], max[2], min[3])),
-			TransformToParentPoint(transform, Vec(max[1], max[2], min[3])),
-			TransformToParentPoint(transform, Vec(min[1], min[2], max[3])),
-			TransformToParentPoint(transform, Vec(max[1], min[2], max[3])),
-			TransformToParentPoint(transform, Vec(min[1], max[2], max[3])),
-			TransformToParentPoint(transform, Vec(max[1], max[2], max[3]))
-		}
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		DrawFunction(points[1], points[2], r, g, b, a)
-		DrawFunction(points[1], points[3], r, g, b, a)
-		DrawFunction(points[1], points[5], r, g, b, a)
-		DrawFunction(points[4], points[3], r, g, b, a)
-		DrawFunction(points[4], points[2], r, g, b, a)
-		DrawFunction(points[4], points[8], r, g, b, a)
-		DrawFunction(points[6], points[5], r, g, b, a)
-		DrawFunction(points[6], points[8], r, g, b, a)
-		DrawFunction(points[6], points[2], r, g, b, a)
-		DrawFunction(points[7], points[8], r, g, b, a)
-		DrawFunction(points[7], points[5], r, g, b, a)
-		DrawFunction(points[7], points[3], r, g, b, a)
-
-		return points
-	end
-	function visual.drawprism(transform, radius, depth, rotation, sides, info)
-		local points = {}
-		local iteration = 1
-		local pow, sqrt, sin, cos = math.pow, math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-
-		radius = sqrt(2 * pow(radius, 2)) or sqrt(2)
-		depth = depth or 1
-		rotation = rotation or 0
-		sides = sides or 4
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		for v = 0, 360, 360 / sides do
-			points[iteration] = TransformToParentPoint(transform, Vec(sin((v + rotation) * degreeToRadian) * radius, depth, cos((v + rotation) * degreeToRadian) * radius))
-			points[iteration + 1] = TransformToParentPoint(transform, Vec(sin((v + rotation) * degreeToRadian) * radius, -depth, cos((v + rotation) * degreeToRadian) * radius))
-			if iteration > 2 then
-				DrawFunction( points[iteration], points[iteration + 1], r, g, b, a )
-				DrawFunction( points[iteration - 2], points[iteration], r, g, b, a )
-				DrawFunction( points[iteration - 1], points[iteration + 1], r, g, b, a )
-			end
-			iteration = iteration + 2
-		end
-
-		return points
-	end
-
-	function visual.drawsphere( transform, radius, rotation, samples, info )
-		local points = {}
-		local sqrt, sin, cos = math.sqrt, math.sin, math.cos
-		local r, g, b, a
-		local DrawFunction = DrawLine
-
-		radius = radius or 1
-		rotation = rotation or 0
-		samples = samples or 100
-
-		if info then
-			r = info.r and info.r or 1
-			g = info.g and info.g or 1
-			b = info.b and info.b or 1
-			a = info.a and info.a or 1
-			DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine)
-		end
-
-		-- Converted from python to lua, see original code https://stackoverflow.com/a/26127012/5459461
-		local points = {}
-		for i = 0, samples do
-			local y = 1 - (i / (samples - 1)) * 2
-			local rad = sqrt(1 - y * y)
-			local theta = 2.399963229728653 * i
-
-			local x = cos(theta) * rad
-			local z = sin(theta) * rad
-			local point = TransformToParentPoint(Transform(transform.pos, QuatRotateQuat(transform.rot, QuatEuler(0, rotation, 0))), Vec(x * radius, y * radius, z * radius))
-
-			DrawFunction( point, VecAdd( point, Vec( 0, .01, 0 ) ), r, g, b, a )
-			points[i + 1] = point
-		end
-
-		return points
-	end
-
-end
+#version 2

```

---

# Migration Report: umf\umf_3d.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\umf_3d.lua
+++ patched/umf\umf_3d.lua
@@ -1,4 +1 @@
-#include "umf_core.lua"
-#include "extension/visual.lua"
-
-UpdateQuickloadPatch()
+#version 2

```

---

# Migration Report: umf\umf_core.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\umf_core.lua
+++ patched/umf\umf_core.lua
@@ -1,12 +1 @@
-#include "core/detouring.lua"
-#include "core/hook.lua"
-#include "core/util.lua"
-#include "core/console_backend.lua"
-#include "core/meta.lua"
-#include "core/timer.lua"
-#include "core/default_hooks.lua"
-#include "core/added_hooks.lua"
-#include "core/xml.lua"
-
-GLOBAL_CHANNEL = util.shared_channel( "game.umf_global_channel", 128 )
-UpdateQuickloadPatch()
+#version 2

```

---

# Migration Report: umf\umf_full.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\umf_full.lua
+++ patched/umf\umf_full.lua
@@ -1,6 +1 @@
-#include "umf_core.lua"
-#include "umf_meta.lua"
-#include "umf_tool.lua"
-#include "umf_3d.lua"
-
-UpdateQuickloadPatch()
+#version 2

```

---

# Migration Report: umf\umf_meta.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\umf_meta.lua
+++ patched/umf\umf_meta.lua
@@ -1,17 +1 @@
-#include "umf_core.lua"
-#include "extension/meta/vector.lua"
-#include "extension/meta/quat.lua"
-#include "extension/meta/transform.lua"
-#include "extension/meta/entity.lua"
-#include "extension/meta/body.lua"
-#include "extension/meta/shape.lua"
-#include "extension/meta/location.lua"
-#include "extension/meta/joint.lua"
-#include "extension/meta/light.lua"
-#include "extension/meta/trigger.lua"
-#include "extension/meta/screen.lua"
-#include "extension/meta/vehicle.lua"
-#include "extension/meta/player.lua"
-#include "extension/meta/armature.lua"
-
-UpdateQuickloadPatch()
+#version 2

```

---

# Migration Report: umf\umf_tool.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/umf\umf_tool.lua
+++ patched/umf\umf_tool.lua
@@ -1,4 +1 @@
-#include "umf_core.lua"
-#include "extension/tool_loader.lua"
-
-UpdateQuickloadPatch()
+#version 2

```
