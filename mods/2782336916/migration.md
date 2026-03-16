# Migration Report: avf\prefabs\bmp2\avf_custom.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\bmp2\avf_custom.lua
+++ patched/avf\prefabs\bmp2\avf_custom.lua
@@ -1,30 +1,4 @@
-#include "check_avf.lua"
-
-
-
-function init()
-	local sceneVehicle = FindVehicle("cfg")
-		local value = GetTagValue(sceneVehicle, "cfg")
-		if(value == "vehicle") then
-			vehicle.id = sceneVehicle
-
-			local status,retVal = pcall(initVehicle)
-			if status then 
-				-- utils.printStr("no errors")
-			else
-				DebugPrint(retVal)
-			end
-			-- initVehicle()
-		end
-
-		SetTag(sceneVehicle,"AVF_Custom","unset")
-
-		check_AVF:init(sceneVehicle)
-
-
-end
-
-
+#version 2
 function initVehicle()
 	if unexpected_condition then error() end
 	vehicle.body = GetVehicleBody(vehicle.id)
@@ -105,7 +79,7 @@
 	local val3 = GetTagValue(gun, "component")
 	return val3
 end
--- @magazine1_tracer
+
 function addItems(shape,values)
 	for key,val in pairs(values) do 
 			if(type(val)== 'table') then
@@ -136,23 +110,27 @@
 	end
 end
 
--- function tick(dt)
--- 	check_AVF:tick()
+function server.init()
+    local sceneVehicle = FindVehicle("cfg")
+    	local value = GetTagValue(sceneVehicle, "cfg")
+    	if(value == "vehicle") then
+    		vehicle.id = sceneVehicle
 
--- end
-
-
-function draw(dt)
-	if(check_AVF.enabled) then 
-		check_AVF:draw()
-	end
-
+    		local status,retVal = pcall(initVehicle)
+    		if status then 
+    			-- utils.printStr("no errors")
+    		else
+    			DebugPrint(retVal)
+    		end
+    		-- initVehicle()
+    	end
+    	SetTag(sceneVehicle,"AVF_Custom","unset")
+    	check_AVF:init(sceneVehicle)
 end
 
--- end
-utils = {
-	contains = function(set,key)
-		return set[key] ~= nil
-		-- body
-	end,
-	}+function client.draw()
+    if(check_AVF.enabled) then 
+    	check_AVF:draw()
+    end
+end
+

```

---

# Migration Report: avf\prefabs\bmp2\avf_tank.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\bmp2\avf_tank.lua
+++ patched/avf\prefabs\bmp2\avf_tank.lua
@@ -1,59 +1 @@
-#include "avf_custom.lua"
-
-
-
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-
-	},
-	guns = {
-		["yourTankCannonName"] = {	
-			name="tank shooty",
-			magazines = {},
-			
-			sight					= {
-										[1] = {
-										x=1.1,
-										y=1.0,
-										z=2.0,
-											},
-										},
-										-- aimForwards = true,
-			barrels		= {
-							[1] = {
-								x = 0.2,
-								y = 0.1,
-								z = -1.5,
-								}
-
-							},
-			},
-	},
-	}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\bmp2\check_avf.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\bmp2\check_avf.lua
+++ patched/avf\prefabs\bmp2\check_avf.lua
@@ -1,22 +1,10 @@
-
-
---[[
-
-
-A simple method that will check if AVF is running and inform the user if they are in an AVF vehicle without AVF active. 
-
-
-]]
-check_AVF = {}
-
-
+#version 2
 function check_AVF:init(vehicle)
 	self.maxTime = 1
 	self.timer = 0
 	self.vehicle = vehicle
 	self.enabled = true
 	self.hideKey = {[0]="ctrl",[1]="c"}
-
 
 end
 
@@ -28,7 +16,7 @@
 end
 
 function check_AVF:draw()
-	if(self.enabled and GetPlayerVehicle() == self.vehicle and  not GetBool("level.avf.enabled")) then
+	if(self.enabled and GetPlayerVehicle(playerId) == self.vehicle and  not GetBool("level.avf.enabled")) then
 		self:drawMessage()
 		if((InputPressed(self.hideKey[0])or InputDown(self.hideKey[0])) and
 			(InputPressed(self.hideKey[1])or InputDown(self.hideKey[1]))) then 
@@ -50,7 +38,6 @@
 				[5] = "and enabled in the mod manager",
 				[6] = "Otherwise this tank won't shoot",
 				[7] = "press ctrl+c to hide",
-
 
 		}
 		header = "Armed Vehicle Framework (AVF)"
@@ -78,4 +65,5 @@
 		UiWordWrap(w)
 		UiText(message2)
 		UiPop()
-end+end
+

```

---

# Migration Report: avf\prefabs\Captured tanks\M4A2 Sherman.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\Captured tanks\M4A2 Sherman.lua
+++ patched/avf\prefabs\Captured tanks\M4A2 Sherman.lua
@@ -1,172 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="75mm M3 cannon",
-			RPM=9.0,
-			sight					= {
-										[1] = {
-										x=0.6,
-										y=1.45,
-										z=-0.35,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.04,
-											y = -0.04
-											},
-									},
-			zoomSight 				= "MOD/gfx/Sherman_sights.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.5,
-								y = 0.1,
-								z = -1.9,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="M61 shot (APCBC)",
-						caliber 				= 75,
-						velocity				= 200,
-						explosionSize			= 0.5,
-						maxPenDepth = 1.0,
-						payload					= "AP",
-						magazineCount             = 24,
-					},
-						[2] = {name="M48 Shell (HE)",
-						caliber 				= 75,
-						velocity				= 200,
-						explosionSize			= 0.6,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.3, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 24, 
-					},
-						[3] = {name="72 shot (AP)",
-						caliber 				= 75,
-						velocity				= 200,
-						maxPenDepth 			= 0.9,
-						r						= 0.3,
-						g						= 0.3, 
-						b						= 0.3, 
-						payload = "AP",
-						magazineCount             = 23, 
-					},
-					[4] = {name="T45 shot (APCR)",
-						caliber 				= 75,
-						velocity				= 200,
-						maxPenDepth 			= 1.4,
-						r						= 0.3,
-						g						= 0.3, 
-						b						= 0.3, 
-						payload = "AP",
-						magazineCount             = 23, 
-					},
-				},
-				coax = 	{
-					name="7.62mm M1919A4",
-					caliber 				= 7.62,
-					sight					= {
-												[1] = {
-												x=0.6,
-												y=1.4,
-												z=-0.35,
-													},
-												},
-					scope_offset 			= {
-										[1] = {
-											x = 0.04,
-											y = -0.04
-											},
-									},	
-					barrels		= {
-										[1] = {
-											x = 0.85,
-											y = 0.15,
-											z = -0.9,
-											}
-										},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/Sherman_sights.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.62mm",
-								r						= 1.9,
-								g						= 0.3, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			caliber 				= 7.62,
-			name="7.62mm M1919A4",
-			sight					= {
-										[1] = {
-										x=0.0,
-										y=1.3,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.62mm",
-						r						= 1.9,
-						g						= 0.3, 
-						b						= 0.3, 
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\Cars,Trucks,Guns\Door.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\Cars,Trucks,Guns\Door.lua
+++ patched/avf\prefabs\Cars,Trucks,Guns\Door.lua
@@ -1,16 +1,17 @@
-Vehicle = FindVehicle("Door")
-doors = FindJoints("door")
+#version 2
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if GetPlayerVehicle(playerId) == Vehicle then
+        	for i=1, #doors do
+        		door = doors[i]
+        		SetJointMotorTarget(door, 0, 3)
+        	end
+        else
+        	for i=1, #doors do
+        		door = doors[i]
+        		SetJointMotorTarget(door, 90, 0, 0)
+        	end
+        end
+    end
+end
 
-function tick()
-	if GetPlayerVehicle() == Vehicle then
-		for i=1, #doors do
-			door = doors[i]
-			SetJointMotorTarget(door, 0, 3)
-		end
-	else
-		for i=1, #doors do
-			door = doors[i]
-			SetJointMotorTarget(door, 90, 0, 0)
-		end
-	end
-end
```

---

# Migration Report: avf\prefabs\Cars,Trucks,Guns\KubelWagon with MG42.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\Cars,Trucks,Guns\KubelWagon with MG42.lua
+++ patched/avf\prefabs\Cars,Trucks,Guns\KubelWagon with MG42.lua
@@ -1,92 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "MG42",
-					caliber 				= 7.92,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "7.92×57mm Mauser",
-													magazineCapacity = 250,
-													ammoCount = 0,
-													magazineCount = 9,
-													caliber 				= 7.92,
-													velocity				= 180,
-													hit 					=3,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													gravityCoef 			= 1.3,
-													shellWidth				= 0.1,
-													shellHeight				= 0.1,
-													r						= 0.3,
-													g						= 3.6, 
-													b						= 0.3, 
-													tracer 					= 2,
-													tracerL					= 7,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											},
-										},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 2.,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 2500,
-				reload 					= 7,
-				magazineCapacity 		= 100,
-				recoil 					= 0.08,
-				weapon_recoil 			= 23,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,			
-				},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\Cars,Trucks,Guns\Sd.Kfz.251.22.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\Cars,Trucks,Guns\Sd.Kfz.251.22.lua
+++ patched/avf\prefabs\Cars,Trucks,Guns\Sd.Kfz.251.22.lua
@@ -1,105 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="7.5 cm PaK40/3 L46 Cannon",
-			RPM=8.0,
-			sight					= {
-										[1] = {
-										x=0.65,
-										y=0.415,
-										z=0.50,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-			zoomSight 				= "MOD/gfx/TZF5.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.1,
-								y = 0.15,
-								z = -2.8,
-								}
-
-							},
-			magazines = {
-						[1] = {name="PzGr 39 (APCBC)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.2,
-						maxPenDepth = 1.37,
-						payload					= "AP",
-						magazineCount             = 6,
-					},
-						[2] = {name="Sprgr. 34 (HE)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 6, 
-					},
-						[3] = {name="PzGr 40 (AP)",
-						caliber 				= 75,
-						velocity				= 300,
-						maxPenDepth 			= 1.6,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "AP",
-						magazineCount             = 6,
-					},
-						[4] = {name="HL.Gr (HEAT)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 0.4,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HEAT",
-						magazineCount             = 6, 
-					},
-				}, 
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\Cars,Trucks,Guns\Sd.Kfz.251.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\Cars,Trucks,Guns\Sd.Kfz.251.lua
+++ patched/avf\prefabs\Cars,Trucks,Guns\Sd.Kfz.251.lua
@@ -1,92 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "MG42",
-					caliber 				= 7.92,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "7.92×57mm Mauser",
-													magazineCapacity = 250,
-													ammoCount = 0,
-													magazineCount = 11,
-													caliber 				= 7.92,
-													velocity				= 180,
-													hit 					=3,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													gravityCoef 			= 1.3,
-													shellWidth				= 0.1,
-													shellHeight				= 0.1,
-													r						= 0.3,
-													g						= 3.6, 
-													b						= 0.3, 
-													tracer 					= 2,
-													tracerL					= 7,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											},
-										},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 2.,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 2500,
-				reload 					= 7,
-				magazineCapacity 		= 100,
-				recoil 					= 0.08,
-				weapon_recoil 			= 150,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,			
-				},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\cromwell\cromwell_V.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\cromwell\cromwell_V.lua
+++ patched/avf\prefabs\cromwell\cromwell_V.lua
@@ -1,144 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="Ordnance QF 75 mm",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = 0.01
-											},
-									},
-			zoomSight 				= "MOD/gfx/TZF12.png",
-			soundFile				= "MOD/sounds/tank/tank_fire_09",
-			reloadSound				= "MOD/sounds/tank/reload_short_01",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 400,
-
-			elevationSpeed			= 1,
-			barrels		= {
-							[1] = {
-								x = 0.9,
-								y = 0.1,
-								z = -0.1,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="APC M61",
-						caliber 				= 75,
-						velocity				= 200,
-						maxPenDepth 			= 	1,
-						shellWidth				= 0.25,
-						shellHeight				= .75,
-						r						= 0.4,
-						g						= 1.4, 
-						b						= 0.4,
-						payload					= "AP",
-					},
-						[2] = {name="HE M46",
-						caliber 				= 75,
-						velocity				= 190,
-						explosionSize			= 1.0,
-						maxPenDepth 			= 0.3,
-						shellWidth				= 0.25,
-						shellHeight				= .75,
-						r						= 1.0,
-						g						= 0.4, 
-						b						= 0.4, 
-						payload = "HE",
-					},
-				},
-				coax = 	{
-					name="7.92mm Besa  Coax",
-					sight					= {
-												[1] = {
-												x=2.12,
-												y=1.7,
-												z=-0.05,
-													},
-												},
-					barrels		= {
-									[1] = {
-										x = 0.2,
-										y = 0.1,
-										z = 2.5,
-										}
-									},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/tzf9b.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.2,
-								y = 0.1,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\Equipment\MG34.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\Equipment\MG34.lua
+++ patched/avf\prefabs\Equipment\MG34.lua
@@ -1,92 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "MG34",
-					caliber 				= 7.92,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "7.92×57mm Mauser",
-													magazineCapacity = 300,
-													ammoCount = 0,
-													magazineCount = 5,
-													caliber 				= 7.92,
-													velocity				= 180,
-													hit 					=3,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													gravityCoef 			= 1.3,
-													shellWidth				= 0.1,
-													shellHeight				= 0.1,
-													r						= 0.3,
-													g						= 3.6, 
-													b						= 0.3, 
-													tracer 					= 2,
-													tracerL					= 7,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											},
-										},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 2.,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 900,
-				reload 					= 7,
-				magazineCapacity 		= 300,
-				recoil 					= 0.08,
-				weapon_recoil 			= 23,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,			
-				},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\Equipment\MG42.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\Equipment\MG42.lua
+++ patched/avf\prefabs\Equipment\MG42.lua
@@ -1,92 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "MG42",
-					caliber 				= 7.92,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "7.92×57mm Mauser",
-													magazineCapacity = 250,
-													ammoCount = 0,
-													magazineCount = 5,
-													caliber 				= 7.92,
-													velocity				= 180,
-													hit 					=3,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													gravityCoef 			= 1.3,
-													shellWidth				= 0.1,
-													shellHeight				= 0.1,
-													r						= 0.3,
-													g						= 3.6, 
-													b						= 0.3, 
-													tracer 					= 2,
-													tracerL					= 7,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											},
-										},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 2.,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 2500,
-				reload 					= 7,
-				magazineCapacity 		= 250,
-				recoil 					= 0.08,
-				weapon_recoil 			= 23,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,			
-				},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\ferdinand\Ferdinand.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\ferdinand\Ferdinand.lua
+++ patched/avf\prefabs\ferdinand\Ferdinand.lua
@@ -1,105 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="8.8 cm PaK43/2 Cannon",
-			RPM=6.5,
-			sight					= {
-										[1] = {
-										x=2.15,
-										y=2.6,
-										z=3.8,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.05
-											},
-									},
-			zoomSight 				= "MOD/gfx/tzf9b.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.3,
-								y = 0.3,
-								z = -4.2,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="PzGr 39/43 (APCBC)",
-						caliber 				= 88,
-						velocity				= 330,
-						explosionSize			= 0.5,
-						maxPenDepth = 2.37,
-						payload					= "AP",
-						magazineCount             = 13,
-					},
-						[2] = {name="PzGr 40/43 (AP)",
-						caliber 				= 88,
-						velocity				= 330,
-						explosionSize			= 0.5,
-						maxPenDepth = 2.8,
-						payload					= "AP",
-						magazineCount             = 13,
-					},
-						[3] = {name="Sprgr.43 (HE)",
-						caliber 				= 88,
-						velocity				= 330,
-						explosionSize			= 0.5,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 12, 
-					},
-						[4] = {name="HL.Gr 39 (HEAT)",
-						caliber 				= 88,
-						velocity				= 330,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 0.4,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HEAT",
-						magazineCount             = 12, 
-					},
-				},
-			
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\katyusha\katyusha.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\katyusha\katyusha.lua
+++ patched/avf\prefabs\katyusha\katyusha.lua
@@ -1,101 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "BM-13",
-					weaponType 				= "rocket",
-					caliber 				= 132,
-					magazines 					= {
-											[1] = {
-									name = "132mm rocket HE",
-									caliber 				= 132,
-									velocity				= 87,
-									explosionSize			= 2,
-									maxPenDepth 			= 0.1,
-									gravityCoef 			= 2,
-									timeToLive 				= 12,
-									launcher				= "rocket",
-									payload					= "HE",
-									shellWidth				= 1,
-									shellHeight				= 3,
-									r						= 0.7,
-									g						= 1.2, 
-									b						= 0.7, 
-									shellSpriteName			= "MOD/gfx/rocketModel2.png",
-									shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-									magazineCapacity = 14,
-									ammoCount = 0,
-									magazineCount = 150,
-
-
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.5,z=-0.6},
-												
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=3.0,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 2.3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 150,
-					reload 					= 5,
-					recoil 					= 0.3,
-					weapon_recoil 			= 75,
-					cannonBlast 			= 0.2,
-					dispersion 				= 5,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/rockets/rocket_launcher_05",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\panther\Panther A.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\panther\Panther A.lua
+++ patched/avf\prefabs\panther\Panther A.lua
@@ -1,160 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="7.5 cm KwK.42 L/70 Cannon",
-			RPM=6.5,
-			sight					= {
-										[1] = {
-										x=1.9,
-										y=1.5,
-										z=-0.35,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.03
-											},
-									},
-			zoomSight 				= "MOD/gfx/TZF12.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.9,
-								y = 0.1,
-								z = -3.8,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="PzGr 39/42 (APCBC)",
-						caliber 				= 75,
-						velocity				= 330,
-						explosionSize			= 0.2,
-						maxPenDepth = 1.9,
-						payload					= "AP",
-						magazineCount             = 20,
-					},
-						[2] = {name="Sprgr. 42 (HE)",
-						caliber 				= 75,
-						velocity				= 330,
-						explosionSize			= 0.5,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 19, 
-					},
-						[3] = {name="PzGr 40/42 (AP)",
-						caliber 				= 75,
-						velocity				= 330,
-						maxPenDepth 			= 2.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "AP",
-						magazineCount             = 19, 
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=2.12,
-												y=1.7,
-												z=-0.05,
-													},
-												},
-					scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.03
-											},
-									},	
-					barrels		= {
-									[1] = {
-										x = 0.2,
-										y = 0.3,
-										z = -0.5,
-										}
-									},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/TZF12.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-								r						= 0.3,
-								g						= 3.6, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\panther\Panther D.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\panther\Panther D.lua
+++ patched/avf\prefabs\panther\Panther D.lua
@@ -1,150 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="7.5 cm KwK.42 L/70 Cannon",
-			RPM=6.5,
-			sight					= {
-										[1] = {
-										x=1.9,
-										y=1.5,
-										z=-0.35,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.03
-											},
-									},
-			zoomSight 				= "MOD/gfx/TZF12.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.9,
-								y = 0.1,
-								z = -3.8,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="PzGr 39/42 (APCBC)",
-						caliber 				= 75,
-						velocity				= 330,
-						explosionSize			= 0.2,
-						maxPenDepth = 1.9,
-						payload					= "AP",
-						magazineCount             = 39,
-					},
-						[2] = {name="Sprgr. 42 (HE)",
-						caliber 				= 75,
-						velocity				= 330,
-						explosionSize			= 0.5,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 38, 
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=2.12,
-												y=1.7,
-												z=-0.05,
-													},
-												},
-					scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.03
-											},
-									},	
-					barrels		= {
-									[1] = {
-										x = 0.2,
-										y = 0.3,
-										z = -0.5,
-										}
-									},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/TZF12.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-								r						= 0.3,
-								g						= 3.6, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.2,
-								y = 0.1,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\panzer_IV\Panzer_IV F1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\panzer_IV\Panzer_IV F1.lua
+++ patched/avf\prefabs\panzer_IV\Panzer_IV F1.lua
@@ -1,167 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="7.5cm KwK37 Cannon",
-			RPM=14.0,
-			sight					= {
-										[1] = {
-										x=1.5,
-										y=1.45,
-										z=-0.35,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-			zoomSight 				= "MOD/gfx/TZF5.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.50,
-								y = 0.15,
-								z = -0.8,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="K.Gr.rot Pz. (APCBC)",
-						caliber 				= 75,
-						velocity				= 180,
-						explosionSize			= 0.2,
-						maxPenDepth = 0.52,
-						payload					= "AP",
-						magazineCount             = 27,
-					},
-						[2] = {name="Sprgr. 34 (HE)",
-						caliber 				= 75,
-						velocity				= 180,
-						explosionSize			= 0.68,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 27, 
-					},
-						[3] = {name="Hl.Gr 38C (HEAT)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 1.0,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HEAT",
-						magazineCount             = 26, 
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=1.5,
-												y=1.45,
-												z=-0.35,
-													},
-												},
-					barrels		= {
-									[1] = {
-										x = 0.15,
-										y = 0.25,
-										z = 0.0,
-										}
-									},
-					scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/TZF5.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-								r						= 0.3,
-								g						= 3.6, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=1.5,
-										y=1.45,
-										z=-0.35,
-											},
-										},
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\panzer_IV\Panzer_IV G.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\panzer_IV\Panzer_IV G.lua
+++ patched/avf\prefabs\panzer_IV\Panzer_IV G.lua
@@ -1,177 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="7.5cm KwK.40 L/43 Cannon",
-			RPM=8.0,
-			sight					= {
-										[1] = {
-										x=1.5,
-										y=1.45,
-										z=-0.35,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-			zoomSight 				= "MOD/gfx/TZF5.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.5,
-								y = 0.15,
-								z = -0.8,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="PzGr 39 (APCBC)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.2,
-						maxPenDepth = 1.37,
-						payload					= "AP",
-						magazineCount             = 21,
-					},
-						[2] = {name="Sprgr. 34 (HE)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.68,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 21, 
-					},
-						[3] = {name="PzGr 40 (AP)",
-						caliber 				= 75,
-						velocity				= 300,
-						maxPenDepth 			= 1.6,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "AP",
-						magazineCount             = 21,
-					},
-						[4] = {name="HL.Gr (HEAT)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 0.4,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HEAT",
-						magazineCount             = 20, 
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=1.5,
-												y=1.45,
-												z=-0.35,
-													},
-												},
-					barrels		= {
-									[1] = {
-										x = 0.15,
-										y = 0.25,
-										z = 1.9,
-										}
-									},
-					scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/TZF5.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-								r						= 0.3,
-								g						= 3.6, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=1.5,
-										y=1.45,
-										z=-0.35,
-											},
-										},
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\panzer_IV\Panzer_IV H & J.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\panzer_IV\Panzer_IV H & J.lua
+++ patched/avf\prefabs\panzer_IV\Panzer_IV H & J.lua
@@ -1,177 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="7.5cm KwK.40 L/48 Cannon",
-			RPM=8.0,
-			sight					= {
-										[1] = {
-										x=1.5,
-										y=1.45,
-										z=-0.35,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-			zoomSight 				= "MOD/gfx/TZF5.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.5,
-								y = 0.15,
-								z = -0.8,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="PzGr 39 (APCBC)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.2,
-						maxPenDepth = 1.37,
-						payload					= "AP",
-						magazineCount             = 21,
-					},
-						[2] = {name="Sprgr. 34 (HE)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.68,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 21, 
-					},
-						[3] = {name="PzGr 40 (AP)",
-						caliber 				= 75,
-						velocity				= 300,
-						maxPenDepth 			= 1.6,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "AP",
-						magazineCount             = 21,
-					},
-						[4] = {name="HL.Gr (HEAT)",
-						caliber 				= 75,
-						velocity				= 300,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 0.4,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HEAT",
-						magazineCount             = 20, 
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=1.5,
-												y=1.45,
-												z=-0.35,
-													},
-												},
-					scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-					barrels		= {
-									[1] = {
-										x = 0.15,
-										y = 0.25,
-										z = 1.9,
-										}
-									},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/TZF5.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-								r						= 0.3,
-								g						= 3.6, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=1.5,
-										y=1.45,
-										z=-0.35,
-											},
-										},
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.04
-											},
-									},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\sturmtiger\SturmTiger.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\sturmtiger\SturmTiger.lua
+++ patched/avf\prefabs\sturmtiger\SturmTiger.lua
@@ -1,173 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="38cm RW61 auf SturmMörser",
-			cannonBlast 			= 100,
-			RPM=1.0,
-			smokeFactor 			= 5,
-			smokeMulti				= 50,
-			sight					= {
-										[1] = {
-										x=1.9,
-										y=1.5,
-										z=-0.35,
-											},
-										},
-
-			zoomSight 				= "MOD/gfx/spg9-sight.png",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			barrels		= {
-							[1] = {
-								x = 0.6,
-								y = 0.1,
-								z = -1.0,
-								}
-
-							},
-			
-			magazines = {
-				                
-						[1] = {name="Raketen Hohlladungsgranate 4592",
-						caliber 				= 380,
-						velocity				= 100,
-						explosionSize			= 5.5,
-						maxPenDepth = 1.5,
-						launcher                = "rocket",
-						payload					= "APHE",
-						shellWidth				= 2,
-						shellHeight				= 2,
-						tracer 					= 5,
-						tracerL					= 6,
-						tracerW					= 2,
-						tracerR					= 1.8,
-						tracerG					= 1.0, 
-						tracerB					= 1.0, 
-						magazineCount             = 6,
-						shellSpriteName			= "MOD/gfx/rocketModel2.png",
-						shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-						flightLoop				= "MOD/sounds/rocketFlightLoop0",
-					},
-						[2] = {name="Raketen Sprenggranate 4581",
-						caliber 				= 380,
-						velocity				= 100,
-						explosionSize			= 5.5,
-						maxPenDepth = 1.0,
-						launcher                = "rocket",
-						payload					= "HE",
-						shellWidth				= 2,
-						shellHeight				= 2,
-						magazineCount             = 6,
-						shellSpriteName			= "MOD/gfx/rocketModel2.png",
-						shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-						flightLoop				= "MOD/sounds/rocketFlightLoop0",
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=2.12,
-												y=1.7,
-												z=-0.05,
-													},
-												},
-					barrels		= {
-									[1] = {
-										x = 0.2,
-										y = 0.2,
-										z = 2.5,
-										}
-									},
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-							},
-				},
-			},
-		["commander_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 1.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-							},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72\t72A.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72\t72A.lua
+++ patched/avf\prefabs\t72\t72A.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46M 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.0,
-								maxPenDepth 			= 1.8,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 250,
-								explosionSize			= 0.4,
-								maxPenDepth 			= 1.0,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 180,
-								explosionSize			= 1.35,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 26,
-					reload 					= 2,
-					recoil 					= 1.8,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72\t72b.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72\t72b.lua
+++ patched/avf\prefabs\t72\t72b.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46M-1 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 220,
-								explosionSize			= 1.2,
-								maxPenDepth 			= 2.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 270,
-								explosionSize			= 0.5,
-								maxPenDepth 			= 1.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.5,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72\t90.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72\t90.lua
+++ patched/avf\prefabs\t72\t90.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 220,
-								explosionSize			= 1.2,
-								maxPenDepth 			= 2.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 270,
-								explosionSize			= 0.5,
-								maxPenDepth 			= 1.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.5,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72\tos_1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72\tos_1.lua
+++ patched/avf\prefabs\t72\tos_1.lua
@@ -1,101 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "BM-13",
-					weaponType 				= "rocket",
-					caliber 				= 132,
-					magazines 					= {
-											[1] = {
-									name = "220m MO.1.01.04",
-									caliber 				= 220,
-									velocity				= 90,
-									explosionSize			= 3.5,
-									maxPenDepth 			= 0.1,
-									gravityCoef 			= 2,
-									timeToLive 				= 12,
-									launcher				= "rocket",
-									payload					= "HE",
-									shellWidth				= 1.5,
-									shellHeight				= 5,
-									r						= 0.7,
-									g						= 1.2, 
-									b						= 0.7, 
-									shellSpriteName			= "MOD/gfx/rocketModel2.png",
-									shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-									magazineCapacity = 14,
-									ammoCount = 0,
-									magazineCount = 150,
-
-
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.5,z=-0.6},
-												
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=3.0,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 2.3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 150,
-					reload 					= 5,
-					recoil 					= 0.3,
-					weapon_recoil 			= 75,
-					cannonBlast 			= 0.2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/rockets/rocket_launcher_06",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_desert\t72A.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_desert\t72A.lua
+++ patched/avf\prefabs\t72_desert\t72A.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46M 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.0,
-								maxPenDepth 			= 1.8,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 250,
-								explosionSize			= 0.4,
-								maxPenDepth 			= 1.0,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 180,
-								explosionSize			= 1.35,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 26,
-					reload 					= 2,
-					recoil 					= 1.8,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_desert\t72b.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_desert\t72b.lua
+++ patched/avf\prefabs\t72_desert\t72b.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46M-1 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 220,
-								explosionSize			= 1.2,
-								maxPenDepth 			= 2.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 270,
-								explosionSize			= 0.5,
-								maxPenDepth 			= 1.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.5,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_desert\t90.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_desert\t90.lua
+++ patched/avf\prefabs\t72_desert\t90.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 220,
-								explosionSize			= 1.2,
-								maxPenDepth 			= 2.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 270,
-								explosionSize			= 0.5,
-								maxPenDepth 			= 1.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.5,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_desert\tos_1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_desert\tos_1.lua
+++ patched/avf\prefabs\t72_desert\tos_1.lua
@@ -1,101 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "BM-13",
-					weaponType 				= "rocket",
-					caliber 				= 132,
-					magazines 					= {
-											[1] = {
-									name = "220m MO.1.01.04",
-									caliber 				= 220,
-									velocity				= 90,
-									explosionSize			= 3.5,
-									maxPenDepth 			= 0.1,
-									gravityCoef 			= 2,
-									timeToLive 				= 12,
-									launcher				= "rocket",
-									payload					= "HE",
-									shellWidth				= 1.5,
-									shellHeight				= 5,
-									r						= 0.7,
-									g						= 1.2, 
-									b						= 0.7, 
-									shellSpriteName			= "MOD/gfx/rocketModel2.png",
-									shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-									magazineCapacity = 14,
-									ammoCount = 0,
-									magazineCount = 150,
-
-
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.5,z=-0.6},
-												
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=3.0,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 2.3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 150,
-					reload 					= 5,
-					recoil 					= 0.3,
-					weapon_recoil 			= 75,
-					cannonBlast 			= 0.2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/rockets/rocket_launcher_06",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_woodland\t72A.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_woodland\t72A.lua
+++ patched/avf\prefabs\t72_woodland\t72A.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46M 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.0,
-								maxPenDepth 			= 1.8,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 250,
-								explosionSize			= 0.4,
-								maxPenDepth 			= 1.0,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 180,
-								explosionSize			= 1.35,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 26,
-					reload 					= 2,
-					recoil 					= 1.8,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_woodland\t72b.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_woodland\t72b.lua
+++ patched/avf\prefabs\t72_woodland\t72b.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46M-1 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 220,
-								explosionSize			= 1.2,
-								maxPenDepth 			= 2.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 270,
-								explosionSize			= 0.5,
-								maxPenDepth 			= 1.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.5,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_woodland\t90.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_woodland\t90.lua
+++ patched/avf\prefabs\t72_woodland\t90.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 220,
-								explosionSize			= 1.2,
-								maxPenDepth 			= 2.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 270,
-								explosionSize			= 0.5,
-								maxPenDepth 			= 1.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.5,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t72_woodland\tos_1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72_woodland\tos_1.lua
+++ patched/avf\prefabs\t72_woodland\tos_1.lua
@@ -1,101 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "BM-13",
-					weaponType 				= "rocket",
-					caliber 				= 132,
-					magazines 					= {
-											[1] = {
-									name = "220m MO.1.01.04",
-									caliber 				= 220,
-									velocity				= 90,
-									explosionSize			= 3.5,
-									maxPenDepth 			= 0.1,
-									gravityCoef 			= 2,
-									timeToLive 				= 12,
-									launcher				= "rocket",
-									payload					= "HE",
-									shellWidth				= 1.5,
-									shellHeight				= 5,
-									r						= 0.7,
-									g						= 1.2, 
-									b						= 0.7, 
-									shellSpriteName			= "MOD/gfx/rocketModel2.png",
-									shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-									magazineCapacity = 14,
-									ammoCount = 0,
-									magazineCount = 150,
-
-
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.5,z=-0.6},
-												
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=3.0,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 2.3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 150,
-					reload 					= 5,
-					recoil 					= 0.3,
-					weapon_recoil 			= 75,
-					cannonBlast 			= 0.2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/rockets/rocket_launcher_06",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t90\t90.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t90\t90.lua
+++ patched/avf\prefabs\t90\t90.lua
@@ -1,141 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "2A46 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-						[1] = {
-								name = "125mm HEAT",
-								caliber 				= 125,
-								velocity				= 220,
-								explosionSize			= 1.2,
-								maxPenDepth 			= 2.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,--0.3,
-								launcher				= "cannon",
-								payload					= "HEAT",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.3,
-								g						= 0.6, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-
-							},
-						[2] = {
-								name = "125mm APFSDS",
-								caliber 				= 125,
-								velocity				= 270,
-								explosionSize			= 0.5,
-								maxPenDepth 			= 1.2,
-								timeToLive 				= 7,
-								gravityCoef 			= 0.9,
-								launcher				= "cannon",
-								payload					= "kinetic",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 1.7,
-								g						= 1.7, 
-								b						= 1.7, 
-								shellSpriteName			= "MOD/gfx/sabot.png",
-								shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							},
-						[3] = {
-								name = "125mm HE",
-								caliber 				= 125,
-								velocity				= 200,
-								explosionSize			= 1.5,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								gravityCoef 			= 1,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.5,
-								shellHeight				= 1.5,
-								r						= 0.8,
-								g						= 0.3, 
-								b						= 0.3, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								magazineCapacity = 1,
-								ammoCount = 0,
-								magazineCount = 500,
-							}, 
-						},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = -0.02
-													},
-											},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\t90\t90_test_config.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t90\t90_test_config.lua
+++ patched/avf\prefabs\t90\t90_test_config.lua
@@ -1,110 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-				name="2A46 125 mm gun",
-			magazines = {
-						[1] = {
-				name = "125mm APHE",
-				caliber 				= 125,
-				velocity				= 240,
-				explosionSize			= 1.2,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				gravityCoef 			= 0.3,
-				launcher				= "cannon",
-				payload					= "APHE",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.1,
-				g						= 0.5, 
-				b						= 0.2, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-				magazineCount = 999999,
-			},
-		},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 5,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-	
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.2,
-								y = 0.1,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\technicals\technical_bm_14.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\technical_bm_14.lua
+++ patched/avf\prefabs\technicals\technical_bm_14.lua
@@ -1,142 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "BM-14",
-					weaponType 				= "rocket",
-					caliber 				= 122,
-					magazines 					= {
-											[1] = {
-									name = "122mm  rocket HE Mid",
-									caliber 				= 122,
-									velocity				= 70,
-									explosionSize			= 2,
-									maxPenDepth 			= 0.2,
-									timeToLive 				= 12,
-									launcher				= "rocket",
-									payload					= "HE",
-									shellWidth				= 1,
-									shellHeight				= 3,
-									r						= 0.7,
-									g						= 1.0, 
-									b						= 0.7, 
-									shellSpriteName			= "MOD/gfx/rocketModel2.png",
-									shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-									magazineCapacity = 14,
-									ammoCount = 0,
-									magazineCount = 150,
-
-												},
-											[2] = {
-									name = "122mm rocket HE Close",
-									caliber 				= 122,
-									velocity				= 60,
-									explosionSize			= 2,
-									maxPenDepth 			= 0.2,
-									timeToLive 				= 12,
-									launcher				= "rocket",
-									payload					= "HE",
-									shellWidth				= 1,
-									shellHeight				= 3,
-									r						= 0.7,
-									g						= 1.2, 
-									b						= 0.7, 
-									shellSpriteName			= "MOD/gfx/rocketModel2.png",
-									shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-									magazineCapacity = 14,
-									ammoCount = 0,
-									magazineCount = 150,
-
-												},
-											[3] = {
-									name = "122mm  rocket HE Far",
-									caliber 				= 122,
-									velocity				= 80,
-									explosionSize			= 2,
-									maxPenDepth 			= 0.2,
-									timeToLive 				= 12,
-									launcher				= "rocket",
-									payload					= "HE",
-									shellWidth				= 1,
-									shellHeight				= 3,
-									r						= 0.7,
-									g						= 1.2, 
-									b						= 0.7, 
-									shellSpriteName			= "MOD/gfx/rocketModel2.png",
-									shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-									magazineCapacity = 14,
-									ammoCount = 0,
-									magazineCount = 150,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.5,z=-0.6},
-												
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=3.0,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 2.3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 70,
-					reload 					= 5,
-					recoil 					= 0.8,
-					weapon_recoil 			= 150,
-					dispersion 				= 5,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/mlrs",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\technicals\technical_dshk.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\technical_dshk.lua
+++ patched/avf\prefabs\technicals\technical_dshk.lua
@@ -1,98 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "DSHK",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_127x107_Ball",
-													magazineCapacity = 50,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 240,
-													hit 					=3,
-													maxPenDepth 			= 0.33,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.3,
-													shellWidth				= 0.1,
-													shellHeight				= 0.3,
-													r						= 0.8,
-													g						= 0.8, 
-													b						= 0.5, 
-													tracer 					= 2,
-													tracerL					= 7,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											},
-										},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 2.,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 360,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.05,
-				weapon_recoil 			= 200,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/HeavySingleShot",
-				mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"MOD/sounds/HeavyAutoFire",			
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\technicals\technical_spg9.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\technical_spg9.lua
+++ patched/avf\prefabs\technicals\technical_spg9.lua
@@ -1,116 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= "SPG-9",
-					weaponType 				= "rocket",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-													name = "PG9_AT",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 100,
-													caliber 				= 73,
-													velocity				= 430,
-													explosionSize			= 1,
-													gravityCoef 			= 1.25,
-													maxPenDepth 			= .6,
-													timeToLive 				= 12,
-													launcher				= "rocket",
-													payload					= "HEAT",
-													shellWidth				= 0.8,
-													shellHeight				= 1.5,
-													r						= 0.3,
-													g						= 0.8, 
-													b						= 0.3, 
-													shellSpriteName			= "MOD/gfx/rocketModel.png",
-													shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-
-												},
-											[2] = {
-													name = "OG9_HE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 100,
-													velocity				= 400,
-													explosionSize			= 1.2,
-													maxPenDepth 			= 0.1,
-
-													gravityCoef 			= 1.5,
-													timeToLive 				= 12,
-													launcher				= "rocket",
-													payload					= "HE",
-													shellWidth				= 0.8,
-													shellHeight				= 1.5,
-													r						= 0.3,
-													g						= 0.8, 
-													b						= 0.3, 
-													shellSpriteName			= "MOD/gfx/rocketModel.png",
-													shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-													},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0.6,
-												y = 1.8,
-												z = 0.2,
-													},
-
-
-												},
-					backBlast				= 
-												{
-													[1] = {z=4.3,force=5},
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/spg9-sight.png",
-					highVelocityShells		= true,
-					RPM 					= 20,
-					reload 					= 2,
-					recoil 					= 0.1,
-					weapon_recoil 			= 333,
-					cannonBlast 			= 2.5,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 1,
-					smokeMulti				= 5,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-				},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\technicals\technical_type_63.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\technical_type_63.lua
+++ patched/avf\prefabs\technicals\technical_type_63.lua
@@ -1,140 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "Type 63",
-					weaponType 				= "rocket",
-					caliber 				= 106.7,
-					magazines 					= {
-											[1] = {
-							magazineCapacity = 14,
-							ammoCount = 0,
-							magazineCount = 150,
-							name = "107mm Type 63 rocket HE Mid",
-							caliber 				= 106.7,
-							velocity				= 50,
-							explosionSize			= 1.5,
-							maxPenDepth 			= 0.1,
-							timeToLive 				= 20,
-							launcher				= "rocket",
-							payload					= "HE",
-							shellWidth				= 1,
-							shellHeight				= 3,
-							r						= 0.1,
-							g						= .3, 
-							b						= 0.1, 
-							shellSpriteName			= "MOD/gfx/rocketModel2.png",
-							shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											[2] = {
-							magazineCapacity = 14,
-							ammoCount = 0,
-							magazineCount = 150,
-							name = "107mm Type 63 rocket HE Far",
-							caliber 				= 106.7,
-							velocity				= 60,
-							explosionSize			= 1.5,
-							maxPenDepth 			= 0.1,
-							timeToLive 				= 20,
-							launcher				= "rocket",
-							payload					= "HE",
-							shellWidth				= 1,
-							shellHeight				= 3,
-							r						= 0.1,
-							g						= .5, 
-							b						= 0.1, 
-							shellSpriteName			= "MOD/gfx/rocketModel2.png",
-							shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-												},
-											[3] = {
-							magazineCapacity = 14,
-							ammoCount = 0,
-							magazineCount = 150,
-							name = "122mm rocket HE Close",
-							caliber 				= 122,
-							velocity				= 45,
-							explosionSize			= 1.8,
-							maxPenDepth 			= 0.1,
-							timeToLive 				= 12,
-							launcher				= "rocket",
-							payload					= "HE",
-							shellWidth				= 1,
-							shellHeight				= 3,
-							r						= 0.1,
-							g						= .8, 
-							b						= 0.1, 
-							shellSpriteName			= "MOD/gfx/rocketModel2.png",
-							shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=10},
-												},
-					sight					= {
-												[1] = {
-												x = 2.2,
-												y = 1.3,
-												z = 0.3,
-											},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 90,
-					reload 					= 5,
-					recoil 					= 0.3,
-					weapon_recoil 			= 100,
-					cannonBlast 			= 0,
-					dispersion 				= 10,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/rockets/rocket_launcher_01",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\technicals\technical_UB16.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\technical_UB16.lua
+++ patched/avf\prefabs\technicals\technical_UB16.lua
@@ -1,97 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "UB-16-57",
-					weaponType 				= "rocket",
-					caliber 				= 55,
-					magazines 					= {
-											[1] = {
-													name = "S-5M",
-													magazineCapacity = 16,
-													ammoCount = 0,
-													magazineCount = 100,
-													caliber 				= 55,
-													velocity				= 200,
-													explosionSize			= 1.25,
-													maxPenDepth 			= 0.2,
-													timeToLive 				= 12,
-													launcher				= "rocket",
-													payload					= "HE",
-													shellWidth				= 0.5,
-													shellHeight				= 1.2,
-													r						= 0.25,
-													g						= 0.3, 
-													b						= 0.3, 
-														shellSpriteName			= "MOD/gfx/rocketModel2.png",
-													shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.1,z=-0.5},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 0 ,
-												y = 0,
-												z = -0.6,
-											},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/chopperScope9.png",
-					highVelocityShells		= true,
-					RPM 					= 300,
-					reload 					= 5,
-					recoil 					= 0.5,
-					weapon_recoil 			= 50,
-					cannonBlast 			= 1.5,
-					dispersion 				= 150,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 1,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\tiger_1\Tiger1.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\tiger_1\Tiger1.lua
+++ patched/avf\prefabs\tiger_1\Tiger1.lua
@@ -1,155 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="8.8 cm KwK36 Cannon",
-			RPM=6.5,
-			sight					= {
-										[1] = {
-										x=1.9,
-										y=1.5,
-										z=-0.35,
-											},
-										},
-
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.05
-											},
-									},
-			zoomSight 				= "MOD/gfx/tzf9b.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 100,
-			barrels		= {
-							[1] = {
-								x = 0.9,
-								y = 0.1,
-								z = -0.1,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="PzGr 39 (APCBC)",
-						caliber 				= 88,
-						velocity				= 300,
-						explosionSize			= 0.5,
-						maxPenDepth = 1.6,
-						payload					= "AP",
-						magazineCount             = 31,
-					},
-						[2] = {name="Sprgr. L/45 (HE)",
-						caliber 				= 88,
-						velocity				= 300,
-						explosionSize			= 0.5,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 31, 
-					},
-						[3] = {name="HL.Gr (HEAT)",
-						caliber 				= 88,
-						velocity				= 300,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 0.4,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HEAT",
-						magazineCount             = 30, 
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=2.12,
-												y=1.7,
-												z=-0.05,
-													},
-												},
-					barrels		= {
-									[1] = {
-										x = 0.2,
-										y = 0.1,
-										z = 2.5,
-										}
-									},
-
-					elevationSpeed			= .5,
-					zoomSight 				= "MOD/gfx/tzf9b.png",
-					canZoom					= true,
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-								r						= 0.3,
-								g						= 3.6, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-					},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}+#version 2

```

---

# Migration Report: avf\prefabs\tiger_E\Tiger 1 (E).lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\tiger_E\Tiger 1 (E).lua
+++ patched/avf\prefabs\tiger_E\Tiger 1 (E).lua
@@ -1,187 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="8.8 cm KwK36 Cannon",
-			RPM=6.5,
-			sight					= {
-										[1] = {
-										x=1.9,
-										y=1.5,
-										z=-0.35,
-											},
-										},
-			scope_offset 			= {
-										[1] = {
-											x = 0.0,
-											y = -0.05
-											},
-									},
-			zoomSight 				= "MOD/gfx/tzf9b.png",
-			soundFile				= "MOD/sounds/Relic700KwK37",
-			reloadSound				= "MOD/sounds/Relic700KwKReload",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			barrels		= {
-							[1] = {
-								x = 0.9,
-								y = 0.1,
-								z = -0.1,
-								}
-
-							},
-			
-			magazines = {
-						[1] = {name="PzGr 39 (APCBC)",
-						caliber 				= 88,
-						velocity				= 300,
-						explosionSize			= 0.5,
-						maxPenDepth = 1.6,
-						payload					= "AP",
-						magazineCount             = 23,
-					},
-						[2] = {name="Sprgr. L/45 (HE)",
-						caliber 				= 88,
-						velocity				= 300,
-						explosionSize			= 0.5,
-						maxPenDepth 			= 0.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
-						magazineCount             = 23,
-					},
-						[3] = {name="PzGr 40 (AP)",
-						caliber 				= 88,
-						velocity				= 300,
-						maxPenDepth 			= 2.1,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "AP",
-						magazineCount             = 23,  
-					},
-						[4] = {name="HL.Gr (HEAT)",
-						caliber 				= 88,
-						velocity				= 300,
-						explosionSize			= 0.4,
-						maxPenDepth 			= 0.4,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HEAT",
-						magazineCount             = 23, 
-					},
-				},
-				coax = 	{
-					name="MG34 Coax",
-					sight					= {
-												[1] = {
-												x=2.12,
-												y=1.7,
-												z=-0.05,
-													},
-												},
-					barrels		= {
-									[1] = {
-										x = 0.2,
-										y = 0.2,
-										z = 2.5,
-										}
-									},
-
-					-- 				},
-					
-					magazines = {
-								[1] = {name="7.92×57mm Mauser",
-								r						= 0.3,
-								g						= 3.6, 
-								b						= 0.3, 
-							},
-						},
-				},
-			
-		},
-		["hull_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[1] = {
-								x = 0.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[1] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-							},
-				},
-			},
-		["commander_mg"] = 	{
-			name="MG34 Coax",
-			sight					= {
-										[1] = {
-										x=2.12,
-										y=1.7,
-										z=-0.05,
-											},
-										},
-			barrels		= {
-							[2] = {
-								x = 1.05,
-								y = 0.15,
-								z = -0.5,
-								}
-							},
-
-			-- 				},
-			
-			magazines = {
-						[2] = {name="7.92×57mm Mauser",
-						r						= 0.3,
-						g						= 3.6, 
-						b						= 0.3, 
-							},
-				},
-			},
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\prefabs\ZSU_23_4\ZSU-23-4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\ZSU_23_4\ZSU-23-4.lua
+++ patched/avf\prefabs\ZSU_23_4\ZSU-23-4.lua
@@ -1,131 +1 @@
-#include "../../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					
-					name = "23 mm 2A7 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= 
-					{
-						[1] = {
-								name= "B_23mm_AA",
-								magazineCapacity = 200,
-								ammoCount = 0,
-								magazineCount = 30,
-								caliber 				= 23,
-								velocity				= 220,
-								explosionSize 			= .6,
-								maxPenDepth 			= 0.1,
-								timeToLive 				= 7,
-								launcher				= "cannon",
-								payload					= "HE",
-								shellWidth				= 0.1,
-								shellHeight				= 0.7,
-								r						= 0.5,
-								g						= 0.5, 
-								b						= 0.5, 
-								tracer 					= 1,
-								tracerL					= 5,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-							},
-						[2] = {
-								name= "B_23mm_AA_AP",
-								magazineCapacity = 200,
-								ammoCount = 0,
-								magazineCount = 30,
-								caliber 				= 23,
-								velocity				= 220,
-								explosionSize 			= .6,
-								maxPenDepth 			= 0.5,
-								timeToLive 				= 7,
-								launcher				= "cannon",
-								payload					= "AP",
-								shellWidth				= 0.1,
-								shellHeight				= 0.7,
-								r						= 0.5,
-								g						= 0.5, 
-								b						= 0.5, 
-								tracer 					= 1,
-								tracerL					= 5,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-							},
-
-					},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=.6,y=.6,z=-1.0},
-									[2] = {x=0.2,y=.1,z=-1.0},
-									[3] = {x=.2,y=.6,z=-1.0},
-									[4] = {x=0.6,y=.1,z=-1.0},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-											},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/zsuDUBLAR2.png",
-					highVelocityShells		= true,
-					RPM 					= 700,
-					reload 					= 4,
-					recoil 					= 0.2,
-					dispersion 				= 10,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .3,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/zsuSingle",
-					mouseDownSoundFile 		=	"MOD/sounds/zsuMulti0",
-					loopSoundFile 			=	"MOD/sounds/zsuFiring_long-2.ogg",
-					tailOffSound	 		=	"MOD/sounds/zsuSingle",
-
-
-		},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\scripts\avf_custom.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\avf_custom.lua
+++ patched/avf\scripts\avf_custom.lua
@@ -1,68 +1,4 @@
-#include "check_avf.lua"
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's  custom tank setup script for AVF tanks
-*
-* FILENAME :        avf_custom.lua             
-*
-* DESCRIPTION :
-
-			A utility script that does most of the tank creation work for you 
-
-			just create a seperate tank config for your vehicle, weapons, 
-			and other utilities, then this will do the magic for you!
-
-
-**********************************************************************
-]]
-
-custom_locations = {
-	[1] = "emitter",
-	[2] = "coax_emitter",
-	[3] = "sight",
-	[4] = "backblast",
-	[5] = "shell_ejector",
-	[6] = "shell_ejector_dir"
-
-}
-
-DEBUG = false
-DEBUG_EJECTORS  =false
-
-function init()
-	-- DebugPrint("starting")
-	for key,val in pairs(vehicleParts.guns) do 
-		if(val.template ~= nil) then 
-			-- DebugPrint("tasdss")
-			vehicleParts.guns[key]= deepcopy(templates[val.template])
-		end
-
-	end
-
-	local sceneVehicle = FindVehicle("cfg")
-		local value = GetTagValue(sceneVehicle, "cfg")
-		if(value == "vehicle") then
-			vehicle.id = sceneVehicle
-
-			local status,retVal = pcall(initVehicle)
-			if status then 
-				-- utils.printStr("no errors")
-			else
-				DebugPrint(retVal)
-			end
-			-- initVehicle()
-		end
-
-		SetTag(sceneVehicle,"AVF_Custom","unset")
-		-- DebugPrint("vehicle configured!!")
-		check_AVF:init(sceneVehicle)
-
-
-end
-
-
+#version 2
 function initVehicle()
 	if unexpected_condition then error() end
 	vehicle.body = GetVehicleBody(vehicle.id)
@@ -169,7 +105,7 @@
 	local val3 = GetTagValue(gun, "component")
 	return val3
 end
--- @magazine1_tracer
+
 function addItems(shape,values)
 	for key,val in pairs(values) do 
 			if(key=="coax") then 
@@ -251,15 +187,6 @@
 	end
 end
 
---[[
-
-	[1] = "emitter",
-	[2] = "coax_emitter",
-	[3] = "sight",
-	[4] = "backblast",
-
-
-]]
 function add_emitters(gun,gun_key,gun_val,turret_mounted)
 	local gun_transform = GetShapeWorldTransform(gun)
 	if(gun ~= nil and 
@@ -351,7 +278,6 @@
 	end
 end
 
-
 function add_emitter_group(gun,gun_transform,gun_key,emitter_group,emitters,emitter_type,turret_mounted) 
 	for i =1,#emitters do
 		local emitter_transform = GetLocationTransform(emitters[i]) 
@@ -416,24 +342,6 @@
 	end
 
 end
-
-
-
-
--- function tick(dt)
--- 	check_AVF:tick()
-
--- end
-
-
-function draw(dt)
-	if(check_AVF.enabled) then 
-		check_AVF:draw()
-	end
-
-end
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -450,11 +358,35 @@
     return copy
 end
 
-
--- end
-utils = {
-	contains = function(set,key)
-		return set[key] ~= nil
-		-- body
-	end,
-	}+function server.init()
+    for key,val in pairs(vehicleParts.guns) do 
+    	if(val.template ~= nil) then 
+    		-- DebugPrint("tasdss")
+    		vehicleParts.guns[key]= deepcopy(templates[val.template])
+    	end
+
+    end
+    local sceneVehicle = FindVehicle("cfg")
+    	local value = GetTagValue(sceneVehicle, "cfg")
+    	if(value == "vehicle") then
+    		vehicle.id = sceneVehicle
+
+    		local status,retVal = pcall(initVehicle)
+    		if status then 
+    			-- utils.printStr("no errors")
+    		else
+    			DebugPrint(retVal)
+    		end
+    		-- initVehicle()
+    	end
+    	SetTag(sceneVehicle,"AVF_Custom","unset")
+    	-- DebugPrint("vehicle configured!!")
+    	check_AVF:init(sceneVehicle)
+end
+
+function client.draw()
+    if(check_AVF.enabled) then 
+    	check_AVF:draw()
+    end
+end
+

```

---

# Migration Report: avf\scripts\AVF_REFERENCE.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\AVF_REFERENCE.lua
+++ patched/avf\scripts\AVF_REFERENCE.lua
@@ -1,98 +1 @@
-
-sampleGun = {
-	["sample"]  = {
-					name 	= "sample Name",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					magazines 					= {
-											[1] = {
-													name = "125mm_HEAT",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[2] = {
-													name = "125mm_APFSDS",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											[3] = {
-													name = "125mm_HE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-												}, 
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=3,
-												y=1.3,
-												z=0.3,
-													},
-												},
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-												},
-					canZoom					= true,
-					zoomSight 				= "LEVEL/YOURTANK/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 5,
-					soundFile				= "LEVEL/YOURTANK/sounds/tankshot0",
-					reloadSound				= "LEVEL/YOURTANK/sounds/AltTankReload",
-					mouseDownSoundFile 		= "LEVEL/YOURTANK/sounds/bmpAutoFire",
-					loopSoundFile 			= "LEVEL/YOURTANK/sounds/autoFirealt",
-					tailOffSound	 		= "LEVEL/YOURTANK/sounds/altTailOff",
-					reloadSound				= "LEVEL/YOURTANK/sounds/AltTankReload",
-
-				},
-
-
-}
-
-
-SampleShell = {
-	["125mm_HEAT"] = {
-				name = "125mm HEAT",
-				caliber 				= 125,
-				velocity				= 220,
-				explosionSize			= 1.2,
-				maxPenDepth 			= 1.2,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "explosive",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.3,
-				g						= 0.6, 
-				b						= 0.3,
-				tracer 					= 1,
-				tracerL					= 3,
-				tracerW					= 2,
-				tracerR					= 1.8,
-				tracerG					= 1.0, 
-				tracerB					= 1.0,  
-				shellSpriteName			= "LEVEL/YOURTANK/gfx/shellModel2.png",
-				shellSpriteRearName		= "LEVEL/YOURTANK/gfx/shellRear2.png",
-					
-			},
-
-	
-}+#version 2

```

---

# Migration Report: avf\scripts\check_avf.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\check_avf.lua
+++ patched/avf\scripts\check_avf.lua
@@ -1,22 +1,10 @@
-
-
---[[
-
-
-A simple method that will check if AVF is running and inform the user if they are in an AVF vehicle without AVF active. 
-
-
-]]
-check_AVF = {}
-
-
+#version 2
 function check_AVF:init(vehicle)
 	self.maxTime = 1
 	self.timer = 0
 	self.vehicle = vehicle
 	self.enabled = true
 	self.hideKey = {[0]="ctrl",[1]="c"}
-
 
 end
 
@@ -28,7 +16,7 @@
 end
 
 function check_AVF:draw()
-	if(self.enabled and GetPlayerVehicle() == self.vehicle and  not GetBool("level.avf.enabled")) then
+	if(self.enabled and GetPlayerVehicle(playerId) == self.vehicle and  not GetBool("level.avf.enabled")) then
 		self:drawMessage()
 		if((InputPressed(self.hideKey[0])or InputDown(self.hideKey[0])) and
 			(InputPressed(self.hideKey[1])or InputDown(self.hideKey[1]))) then 
@@ -50,7 +38,6 @@
 				[5] = "and enabled in the mod manager",
 				[6] = "Otherwise this tank won't shoot",
 				[7] = "press ctrl+c to hide",
-
 
 		}
 		header = "Armed Vehicle Framework (AVF)"
@@ -78,4 +65,5 @@
 		UiWordWrap(w)
 		UiText(message2)
 		UiPop()
-end+end
+

```

---

# Migration Report: avf\scripts\Immersive_Tank.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\Immersive_Tank.lua
+++ patched/avf\scripts\Immersive_Tank.lua
@@ -1,206 +1,4 @@
-#include "script/common.lua"
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's  Immersive Tanks Script for AVF tanks
-*
-* FILENAME :        immersive_Tank.lua             
-*
-* DESCRIPTION :
-
-		Adds functionality for ammo cookoff, engine failure, fuel burn, and lots of fun
-
-		simple to implement and provides high impact effects
-
-**********************************************************************
-]]
-
-
-DEBUG =false
-
-tank_found = true
-tank = {}
-
-cook_off_intensity = 1
-cook_off_value = 0
-cook_off_pulse = 0
-cook_off_blast_min_strength = 120
-cook_off_blast_max_strength =750
-
-
-min_tank_health = 0.8
-normal_kill_intensity = 40
-
-min_cook_off = 0.5
-
-max_cook_off = 30
-
-min_burn_off = 5
-
-max_burn_off = 35
-
-burn_off_value = 1
-
-upward_force = 40
-hatch_size = 0.4
-
-
-explosive_force = 1
-
-cook_off_sounds = {}
-tank_explode_sounds = {}
-
-tank_explode_sound_vol = 60
-
-cook_off_sound_vol = 40
-burn_off_sound_vol =5
-
-
-function init()
-
-	local scene_tank 	= FindVehicle("cfg")
-
-	if(IsHandleValid(scene_tank)) then 
-		tank_found = true
-		tank.id = scene_tank
-		local base_vehicle = FindVehicle("base_vehicle")
-
-		if(IsHandleValid(base_vehicle)) then 
-			tank.base_vehicle = base_vehicle
-		end
-		hole_force = math.random(5,50)/10
-
-
-		tank.ammo_racks = FindShapes("ammo_rack")
-
-		tank.ammo_rack_state = {}
-		-- if(tank.ammo_racks) then
-			for i=1,#tank.ammo_racks do
-				tank.ammo_rack_state[i] = true
-			end
-		-- end
-
-		tank.fuel_tanks = FindShapes("fuel_tank")
-
-		tank.fuel_tanks_states = {}
-		tank.fuel_tanks_volume = {}
-		tank.fuel_leak_rate = math.random(10,200)/10
-		if(tank.fuel_tanks) then 
-			for i = 1,#tank.fuel_tanks do 
-				tank.fuel_tanks_states[i] = false 
-				local x, y, z = GetShapeSize(tank.fuel_tanks[i])
-				tank.fuel_tanks_volume[i]  = x*y*z
-				-- DebugPrint("fuel tank: "..i.." volume: "..tank.fuel_tanks_volume[i])
-			end
-		end
-		tank.damaged_fuel_tanks = 0
-		tank.fuel_tanks_okay = true
-
-		tank.engines = FindShapes("engine")
-		tank.engine_states = {}
-		if(tank.engines) then 
-			for i = 1,#tank.engines do 
-				tank.engine_states[i] = false 
-			end
-		end
-		tank.damaged_engines = 0
-		tank.engine_okay = true
-
-
-		tank.tracks = FindShapes("tracks")
-
-
-		local cook_off_loc = FindLocation("cook_off")
-
-	--	DebugPrint(cook_off_loc)
-	--	DebugPrint("scene tank: "..scene_tank)
-		if(IsHandleValid(cook_off_loc)) then
-			tank.cook_off_loc = cook_off_loc 
-
-			tank.cook_off_origin =TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(cook_off_loc))
-			if(HasTag(cook_off_loc,"max_force") and (GetTagValue(cook_off_loc,"max_force"))) then
-				cook_off_blast_max_strength = (GetTagValue(cook_off_loc,"max_force"))
-			end
-			if(HasTag(cook_off_loc,"min_force") and (GetTagValue(cook_off_loc,"min_force"))) then
-				cook_off_blast_min_strength = (GetTagValue(cook_off_loc,"min_force"))
-				
-			end		
-			if(HasTag(cook_off_loc,"max_cook_off") and (GetTagValue(cook_off_loc,"max_cook_off"))) then
-				max_cook_off = (GetTagValue(cook_off_loc,"max_cook_off"))
-			end
-			if(HasTag(cook_off_loc,"min_cook_off") and (GetTagValue(cook_off_loc,"min_cook_off"))) then
-				min_cook_off = (GetTagValue(cook_off_loc,"min_cook_off"))
-				
-			end		
-			if(HasTag(cook_off_loc,"upward_force") and (GetTagValue(cook_off_loc,"upward_force"))) then
-				upward_force = (GetTagValue(cook_off_loc,"upward_force"))
-			end
-			if(HasTag(cook_off_loc,"explosive_force") and (GetTagValue(cook_off_loc,"explosive_force"))) then
-				explosive_force = (GetTagValue(cook_off_loc,"explosive_force"))
-			end
-				
-						
-		end
-
-
-		breakable_joints = FindJoints("break_joint")
-
-
-		local blow_out_locs = FindLocations("blow_out")
-		tank.blow_out_locs = {}
-		tank.blow_out_origins = {}
-		for i=1,#blow_out_locs do
-		local blow_out_loc = blow_out_locs[i] 
-			if(IsHandleValid(blow_out_loc )) then
-				local j = #tank.blow_out_locs+1 
-
-				tank.blow_out_locs[j] = blow_out_loc 
-				tank.blow_out_origins[j] =TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(blow_out_loc))
-			
-				-- DebugPrint("blow out #"..i.." at pos: "..VecStr(tank.blow_out_origins[j].pos))
-				-- DebugPrint("blow out world location"..VecStr(GetLocationTransform(blow_out_loc).pos).." from: "..VecStr(GetLocationTransform(blow_out_locs[i] ).pos).."target:"..VecStr(TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(blow_out_loc)).pos)) 
-			end
-		end
-		local burn_off_locs = FindLocations("burn_off")
-		tank.burn_off_locs = {}
-		tank.burn_off_origins = {}
-		for i=1,#burn_off_locs do
-		local burn_off_loc = burn_off_locs[i] 
-			if(IsHandleValid(burn_off_loc )) then
-				tank.burn_off_locs[i] = burn_off_loc 
-				tank.burn_off_origins[i] =TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(burn_off_loc))
-			end
-		end
-
-
-		tank.hatches_blown = 0
-
-		fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-
-		for i=1, 7 do
-			cook_off_sounds[i] = LoadSound("MOD/avf/snd/cook_off_0"..i..".ogg")
-			tank_explode_sounds[i] = LoadSound("MOD/avf/snd/tank_explode_0"..i..".ogg")
-		end
-
-		cook_off_loop = LoadLoop("MOD/avf/snd/cook_off_loop.ogg")
-
-	end
-
-
-
-end
-
-
-
-function tick()
-
-	local status,retVal = pcall(tick_behaviors)
-	if(not status) then 
-		DebugWatch("[ERROR] ",retVal)
-	end
-end
+#version 2
 function tick_behaviors( )
 	if unexpected_condition then error() end
 
@@ -247,7 +45,6 @@
 	end
 end
 
-
 function kill_tank(max_intensity)
 	min_intensity = 5
 	max_intensity = max_intensity or 100
@@ -267,7 +64,6 @@
 	-- end
 
 end
-
 
 function check_engine_state()
 	-- if(#tank.engines>0) then 
@@ -302,7 +98,6 @@
 		simulate_engine_disabled()--DriveVehicle(tank.id,0,0,true)
 	end
 end
-
 
 function simulate_engine_disabled()
 	DriveVehicle(tank.id,0,0,true)
@@ -327,8 +122,6 @@
 		SpawnParticle(engine_pos.pos, v, life)
 	end
 end
-
-
 
 function check_fuel_tank_state()
 	for i = 1,#tank.fuel_tanks do 
@@ -369,7 +162,6 @@
 	end
 end
 
-
 function animated_fuel_leak(engine_pos,count, vel)
 	for i=1, count do
 		local v = VecAdd(Vec(0, vel, 0 ), rndVec(rnd(vel*0.5, vel*1.5)))
@@ -427,7 +219,6 @@
 					tank.cooking_off = true
 					break_all_breakable_joints()
 
-
 				--	DebugPrint("ammo rack destroyed! cooking off")
 					cook_off_intensity = math.random(1,10)
 					if(cook_off_intensity<=2 and min_cook_off<4) then 
@@ -473,8 +264,6 @@
 	-- 	cook_off()
 	end
 end
-
-
 
 function break_all_breakable_joints()
 	for i=1,#breakable_joints do 
@@ -542,10 +331,6 @@
 				
 			end
 
-
-
-
-
 			if(tank.hatches_blown<3 and  cook_off_value>0.2) then 
 				apply_impulse(transform)
 				
@@ -558,8 +343,6 @@
 			end
 
 			
-
-
 
 		elseif(cook_off_pulse>=1) then
 			cook_off_pulse=0
@@ -591,7 +374,6 @@
 
 end
 
-
 function tank_ignition(transform)
 	local hitLocations = {nil,nil,nil}
 	for i=1,3 do 
@@ -611,7 +393,6 @@
 	end
 	spawn_cookoff_debris(transform.pos)
 end
-
 
 function burn_off()
 
@@ -651,7 +432,6 @@
 			end
 			spawn_cookoff_debris(pos)
 
-
 	elseif(cook_off_pulse>=1) then
 		cook_off_pulse=0
 	end
@@ -673,7 +453,6 @@
 		end
 
 	end
-
 
 	local strength = math.random(cook_off_blast_min_strength,cook_off_blast_max_strength)	--Strength of blower
 	local small_strength = strength*.25
@@ -692,7 +471,6 @@
 	for i=1,#bodies do
 		local b = bodies[i]
 
-
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
 		local bc = VecLerp(bmi, bma, 0.5)
@@ -728,7 +506,6 @@
 	for i=1,#bodies do
 		local b = bodies[i]
 
-
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
 		local bc = VecLerp(bmi, bma, 0.5)
@@ -757,8 +534,7 @@
 		end
 	end
 
-
-end 
+end
 
 function kill_tracks()
 	for i=1,#tank.tracks do 
@@ -768,7 +544,6 @@
 
 	end
 end
-
 
 function EmitFire(strength, t, amount,force)
 	local p = TransformToParentPoint(t, Vec(0, 0,0))
@@ -791,7 +566,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			
@@ -804,11 +579,11 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 5.0, 0.0, 1.0)
 		-- DebugWatch("dist scale",distScale)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			-- DebugWatch("toplayer ",toPlayer)
 
@@ -818,7 +593,7 @@
 				
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.015 * strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.015 * strength * amount * distScale)
 				end
 			end	
 		end
@@ -839,12 +614,10 @@
 	spawn_entity(pos,xml,vel)
 end
 
-
 function spawn_entity(pos,xml,vel,burn)
 	local entities = Spawn(xml, Transform(pos))
 
 	--Set velocity on spawned bodies (only one in this case)
-
 
 	for i=1, #entities do
 		if GetEntityType(entities[i]) == "body" then
@@ -861,9 +634,7 @@
 	end
 end
 
-
 function apply_impulse(transform )
-
 
 	local strength = math.random(10,250)	--Strength of blower
 	local maxMass = 500	--The maximum mass for a body to be affected
@@ -881,7 +652,6 @@
 	for i=1,#bodies do
 		local b = bodies[i]
 
-
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
 		local bc = VecLerp(bmi, bma, 0.5)
@@ -911,15 +681,9 @@
 	end
 end
 
-
-
 function burn_down()
 
-
-
-end
-
-
+end
 
 function rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
@@ -928,10 +692,6 @@
 function rndVec(t)
 	return Vec(rnd(-t, t), rnd(-t, t), rnd(-t, t))
 end
-
-explosionPos = Vec()
-
-trails = {}
 
 function trailsAdd(pos, vel, life, size, damp, gravity)
 	t = {}
@@ -977,14 +737,6 @@
 	end
 end
 
-smoke = {}
-smoke.age = 0
-smoke.size = 0
-smoke.life = 0
-smoke.next = 0
-smoke.vel = 0
-smoke.gravity = 0
-smoke.amount = 0
 function smokeUpdate(pos, dt)
 	smoke.age = smoke.age + dt
 	if smoke.age < smoke.life then
@@ -1007,11 +759,6 @@
 	end
 end
 
-
-fire = {}
-fire.age = 0
-fire.life = 0
-fire.size = 0
 function fireUpdate(pos, dt)
 	fire.age = fire.age + dt
 	if fire.age < fire.life then
@@ -1035,11 +782,6 @@
 	end
 end
 
-
-flash = {}
-flash.age = 0
-flash.life = 0
-flash.intensity = 0
 function flashTick(pos, dt)
 	flash.age = flash.age + dt
 	if flash.age < flash.life then
@@ -1048,11 +790,6 @@
 	end
 end
 
-
-light = {}
-light.age = 0
-light.life = 0
-light.intensity = 0
 function lightTick(pos, dt)
 	light.age = light.age + dt
 	if light.age < light.life then
@@ -1129,7 +866,6 @@
 	smoke.amount = 2
 end
 
-
 function explosionMedium(pos)
 	explosionPos = pos
 	explosionSparks(30, 3)
@@ -1159,7 +895,6 @@
 	smoke.gravity = 2
 	smoke.amount = 2
 end
-
 
 function explosionLarge(pos)
 	explosionPos = pos
@@ -1205,11 +940,145 @@
 	end
 end
 
-
-function update(dt)
-	trailsUpdate(dt)
-	fireUpdate(explosionPos, dt)
-	smokeUpdate(explosionPos, dt)
-end
-
-
+function server.init()
+    local scene_tank 	= FindVehicle("cfg")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local status,retVal = pcall(tick_behaviors)
+        if(not status) then 
+        	DebugWatch("[ERROR] ",retVal)
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        trailsUpdate(dt)
+        fireUpdate(explosionPos, dt)
+        smokeUpdate(explosionPos, dt)
+    end
+end
+
+function client.init()
+    if(IsHandleValid(scene_tank)) then 
+    	tank_found = true
+    	tank.id = scene_tank
+    	local base_vehicle = FindVehicle("base_vehicle")
+
+    	if(IsHandleValid(base_vehicle)) then 
+    		tank.base_vehicle = base_vehicle
+    	end
+    	hole_force = math.random(5,50)/10
+
+    	tank.ammo_racks = FindShapes("ammo_rack")
+
+    	tank.ammo_rack_state = {}
+    	-- if(tank.ammo_racks) then
+    		for i=1,#tank.ammo_racks do
+    			tank.ammo_rack_state[i] = true
+    		end
+    	-- end
+
+    	tank.fuel_tanks = FindShapes("fuel_tank")
+
+    	tank.fuel_tanks_states = {}
+    	tank.fuel_tanks_volume = {}
+    	tank.fuel_leak_rate = math.random(10,200)/10
+    	if(tank.fuel_tanks) then 
+    		for i = 1,#tank.fuel_tanks do 
+    			tank.fuel_tanks_states[i] = false 
+    			local x, y, z = GetShapeSize(tank.fuel_tanks[i])
+    			tank.fuel_tanks_volume[i]  = x*y*z
+    			-- DebugPrint("fuel tank: "..i.." volume: "..tank.fuel_tanks_volume[i])
+    		end
+    	end
+    	tank.damaged_fuel_tanks = 0
+    	tank.fuel_tanks_okay = true
+
+    	tank.engines = FindShapes("engine")
+    	tank.engine_states = {}
+    	if(tank.engines) then 
+    		for i = 1,#tank.engines do 
+    			tank.engine_states[i] = false 
+    		end
+    	end
+    	tank.damaged_engines = 0
+    	tank.engine_okay = true
+
+    	tank.tracks = FindShapes("tracks")
+
+    	local cook_off_loc = FindLocation("cook_off")
+
+    --	DebugPrint(cook_off_loc)
+    --	DebugPrint("scene tank: "..scene_tank)
+    	if(IsHandleValid(cook_off_loc)) then
+    		tank.cook_off_loc = cook_off_loc 
+
+    		tank.cook_off_origin =TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(cook_off_loc))
+    		if(HasTag(cook_off_loc,"max_force") and (GetTagValue(cook_off_loc,"max_force"))) then
+    			cook_off_blast_max_strength = (GetTagValue(cook_off_loc,"max_force"))
+    		end
+    		if(HasTag(cook_off_loc,"min_force") and (GetTagValue(cook_off_loc,"min_force"))) then
+    			cook_off_blast_min_strength = (GetTagValue(cook_off_loc,"min_force"))
+
+    		end		
+    		if(HasTag(cook_off_loc,"max_cook_off") and (GetTagValue(cook_off_loc,"max_cook_off"))) then
+    			max_cook_off = (GetTagValue(cook_off_loc,"max_cook_off"))
+    		end
+    		if(HasTag(cook_off_loc,"min_cook_off") and (GetTagValue(cook_off_loc,"min_cook_off"))) then
+    			min_cook_off = (GetTagValue(cook_off_loc,"min_cook_off"))
+
+    		end		
+    		if(HasTag(cook_off_loc,"upward_force") and (GetTagValue(cook_off_loc,"upward_force"))) then
+    			upward_force = (GetTagValue(cook_off_loc,"upward_force"))
+    		end
+    		if(HasTag(cook_off_loc,"explosive_force") and (GetTagValue(cook_off_loc,"explosive_force"))) then
+    			explosive_force = (GetTagValue(cook_off_loc,"explosive_force"))
+    		end
+
+    	end
+
+    	breakable_joints = FindJoints("break_joint")
+
+    	local blow_out_locs = FindLocations("blow_out")
+    	tank.blow_out_locs = {}
+    	tank.blow_out_origins = {}
+    	for i=1,#blow_out_locs do
+    	local blow_out_loc = blow_out_locs[i] 
+    		if(IsHandleValid(blow_out_loc )) then
+    			local j = #tank.blow_out_locs+1 
+
+    			tank.blow_out_locs[j] = blow_out_loc 
+    			tank.blow_out_origins[j] =TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(blow_out_loc))
+
+    			-- DebugPrint("blow out #"..i.." at pos: "..VecStr(tank.blow_out_origins[j].pos))
+    			-- DebugPrint("blow out world location"..VecStr(GetLocationTransform(blow_out_loc).pos).." from: "..VecStr(GetLocationTransform(blow_out_locs[i] ).pos).."target:"..VecStr(TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(blow_out_loc)).pos)) 
+    		end
+    	end
+    	local burn_off_locs = FindLocations("burn_off")
+    	tank.burn_off_locs = {}
+    	tank.burn_off_origins = {}
+    	for i=1,#burn_off_locs do
+    	local burn_off_loc = burn_off_locs[i] 
+    		if(IsHandleValid(burn_off_loc )) then
+    			tank.burn_off_locs[i] = burn_off_loc 
+    			tank.burn_off_origins[i] =TransformToLocalTransform(GetVehicleTransform(scene_tank), GetLocationTransform(burn_off_loc))
+    		end
+    	end
+
+    	tank.hatches_blown = 0
+
+    	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+
+    	for i=1, 7 do
+    		cook_off_sounds[i] = LoadSound("MOD/avf/snd/cook_off_0"..i..".ogg")
+    		tank_explode_sounds[i] = LoadSound("MOD/avf/snd/tank_explode_0"..i..".ogg")
+    	end
+
+    	cook_off_loop = LoadLoop("MOD/avf/snd/cook_off_loop.ogg")
+
+    end
+end
+

```

---

# Migration Report: avf\scripts\shell_casing_lifespan.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\shell_casing_lifespan.lua
+++ patched/avf\scripts\shell_casing_lifespan.lua
@@ -1,34 +1,31 @@
-
-
-
-function init()
-	script_active = true
-
-	DebugWatch("test",true)
-	shape = FindShape("")
-	min_dist = 30
-	life_timer = 0 
-	max_life = math.random(10,45)
-
+#version 2
+function server.init()
+    script_active = true
+    DebugWatch("test",true)
+    shape = FindShape("")
+    min_dist = 30
+    life_timer = 0 
+    max_life = math.random(10,45)
 end
 
-function tick(dt) 
-	DebugWatch("shell life",life_timer)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        DebugWatch("shell life",life_timer)
+        if(script_active) then 
+        	if(IsHandleValid(shape)) then 
+        		local shape_pos = GetShapeWorldTransform(shape).pos
+        		local player_pos = GetPlayerPos(playerId)
+        		if(life_timer > max_life and  VecLength(VecSub(player_pos,shape_pos))>min_dist) then 
+        			Delete(shape)
+        			script_active = false
+        		else
+        			life_timer = life_timer + dt
+        		end
 
-	if(script_active) then 
-		if(IsHandleValid(shape)) then 
-			local shape_pos = GetShapeWorldTransform(shape).pos
-			local player_pos = GetPlayerPos()
-			if(life_timer > max_life and  VecLength(VecSub(player_pos,shape_pos))>min_dist) then 
-				Delete(shape)
-				script_active = false
-			else
-				life_timer = life_timer + dt
-			end
+        	else 
+        		script_active = false
+        	end
+        end
+    end
+end
 
-		else 
-			script_active = false
-		end
-	end
-
-end
```

---

# Migration Report: avf\scripts\simple_avf_tank.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\simple_avf_tank.lua
+++ patched/avf\scripts\simple_avf_tank.lua
@@ -1,38 +1 @@
-#include "avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			exists = 1,
-			
-			
-		},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: avf\scripts\yourTankNameHere.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\yourTankNameHere.lua
+++ patched/avf\scripts\yourTankNameHere.lua
@@ -1,87 +1 @@
-#include "avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-			name="8.8 cm KwK Cannon",
-			magazines = {
-						[1] = {name="APCBC",
-						caliber 				= 88,
-						velocity				= 230,
-						maxPenDepth = 0.85,
-						payload					= "AP",
-					},
-						[2] = {name="HESH",
-						caliber 				= 77,
-						velocity				= 220,
-						explosionSize			= 1.2,
-						maxPenDepth 			= 1.2,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HESH",
-					},
-			},
-			-- coax = {
-			-- 			[1] = {name="APCBC",
-			-- 			caliber 				= 88,
-			-- 			velocity				= 230,
-			-- 			maxPenDepth = 0.85,
-			-- 			payload					= "AP",
-			-- 		},
-			-- 			[2] = {name="HESH",
-			-- 			caliber 				= 77,
-			-- 			velocity				= 220,
-			-- 			explosionSize			= 1.2,
-			-- 			maxPenDepth 			= 1.2,
-			-- 			r						= 0.3,
-			-- 			g						= 0.6, 
-			-- 			b						= 0.3, 
-			-- 			payload = "HESH",
-			-- 		},
-			-- },
-			sight					= {
-										[1] = {
-										x=2.1,
-										y=2.8,
-										z=2.0,
-											},
-										},
-										-- aimForwards = true,
-			barrels		= {
-							[1] = {
-								x = 50.9,
-								y = 0.25,
-								z = -7.8,
-								}
-
-							},
-			},
-	},
-	}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: main\Cessna 172\scripts\engineprops.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172\scripts\engineprops.lua
+++ patched/main\Cessna 172\scripts\engineprops.lua
@@ -1,14 +1,13 @@
-function init()
+#version 2
+function server.init()
+    blades = FindJoints("engine", true)
+    if GetPlayerVehicle(playerId) ~= 0 then
 
-	blades = FindJoints("engine", true)
+    	for i = 1, #blades do
+    		local blade = blades[i]
+    		SetJointMotor(blade, 30)
+    	end
 
-	if GetPlayerVehicle() ~= 0 then
+    end
+end
 
-		for i = 1, #blades do
-			local blade = blades[i]
-			SetJointMotor(blade, 30)
-		end
-
-	end
-
-end
```

---

# Migration Report: main\Cessna 172\scripts\lights.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172\scripts\lights.lua
+++ patched/main\Cessna 172\scripts\lights.lua
@@ -1,87 +1,83 @@
-function init()
-	btn_navlight = FindShape("nl", true)
-	btn_cabinlight = FindShape("cl", true)
-	btn_instrumentlight = FindShape("ilb", true)
-	
-	light_instrument = FindLight("instrument", true)
-	light_beacon = FindLight("beacon", true)
-	light_cabin = FindLights("cabin", true)
-	light_nav = FindLights("navlight", true)
-	
-	SetTag(btn_navlight, "interact", "Navigation lights")
-	SetTag(btn_cabinlight, "interact", "Cabin lights")
-	SetTag(btn_instrumentlight, "interact", "Instrument light")
-	
-	for i=1,#light_cabin do
-		SetLightEnabled(light_cabin[i], false)
-	end
-	
-	for i=1,#light_nav do
-		SetLightEnabled(light_nav[i], false)
-	end
-	
-	SetLightEnabled(light_instrument, false)
-	SetLightEnabled(light_beacon, false)
-	
-	beacon = false
-	timer = 0
+#version 2
+function server.init()
+    btn_navlight = FindShape("nl", true)
+    btn_cabinlight = FindShape("cl", true)
+    btn_instrumentlight = FindShape("ilb", true)
+    light_instrument = FindLight("instrument", true)
+    light_beacon = FindLight("beacon", true)
+    light_cabin = FindLights("cabin", true)
+    light_nav = FindLights("navlight", true)
+    SetTag(btn_navlight, "interact", "Navigation lights")
+    SetTag(btn_cabinlight, "interact", "Cabin lights")
+    SetTag(btn_instrumentlight, "interact", "Instrument light")
+    for i=1,#light_cabin do
+    	SetLightEnabled(light_cabin[i], false)
+    end
+    for i=1,#light_nav do
+    	SetLightEnabled(light_nav[i], false)
+    end
+    SetLightEnabled(light_instrument, false)
+    SetLightEnabled(light_beacon, false)
+    beacon = false
+    timer = 0
 end
 
-function update(dt)
-	
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if beacon then
+        timer = timer + 1
+        	if timer == 80 then
+        		timer = timer * 0 + 1
+        	end
+        	if timer > 0 and timer < 10 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 10 and timer < 20 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        	if timer >= 20 and timer < 30 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 30 and timer < 80 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        end
+    end
+end
 
-	
-	if GetPlayerInteractShape() == btn_cabinlight and InputPressed("interact") then
-		for i=1,#light_cabin do
-			if IsLightActive(light_cabin[i]) == false then
-				SetLightEnabled(light_cabin[i], true)
-			else
-				SetLightEnabled(light_cabin[i], false)
-			end
-		end
-	end
-	
-	if GetPlayerInteractShape() == btn_navlight and InputPressed("interact") then
-		if not beacon then
-			beacon = true
-		else
-			beacon = false
-		end
-		
-		for i=1,#light_nav do
-			if IsLightActive(light_nav[i]) == false then
-				SetLightEnabled(light_nav[i], true)
-			else
-				SetLightEnabled(light_nav[i], false)
-			end
-		end
-		
-	end
-	
-	if GetPlayerInteractShape() == btn_instrumentlight and InputPressed("interact") then
-		if IsLightActive(light_instrument) == false then
-			SetLightEnabled(light_instrument, true)
-		else
-			SetLightEnabled(light_instrument, false)
-		end
-	end
-	
-	if beacon then
-	timer = timer + 1
-		if timer == 80 then
-			timer = timer * 0 + 1
-		end
-		if timer > 0 and timer < 10 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 10 and timer < 20 then
-			SetLightEnabled(light_beacon, false)
-		end
-		if timer >= 20 and timer < 30 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 30 and timer < 80 then
-			SetLightEnabled(light_beacon, false)
-		end
-	end
-end+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == btn_cabinlight and InputPressed("interact") then
+    	for i=1,#light_cabin do
+    		if IsLightActive(light_cabin[i]) == false then
+    			SetLightEnabled(light_cabin[i], true)
+    		else
+    			SetLightEnabled(light_cabin[i], false)
+    		end
+    	end
+    end
+    if GetPlayerInteractShape(playerId) == btn_navlight and InputPressed("interact") then
+    	if not beacon then
+    		beacon = true
+    	else
+    		beacon = false
+    	end
+
+    	for i=1,#light_nav do
+    		if IsLightActive(light_nav[i]) == false then
+    			SetLightEnabled(light_nav[i], true)
+    		else
+    			SetLightEnabled(light_nav[i], false)
+    		end
+    	end
+
+    end
+    if GetPlayerInteractShape(playerId) == btn_instrumentlight and InputPressed("interact") then
+    	if IsLightActive(light_instrument) == false then
+    		SetLightEnabled(light_instrument, true)
+    	else
+    		SetLightEnabled(light_instrument, false)
+    	end
+    end
+end
+

```

---

# Migration Report: main\Cessna 172 FUEL\scripts\engineprops.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172 FUEL\scripts\engineprops.lua
+++ patched/main\Cessna 172 FUEL\scripts\engineprops.lua
@@ -1,14 +1,13 @@
-function init()
+#version 2
+function server.init()
+    blades = FindJoints("engine", true)
+    if GetPlayerVehicle(playerId) ~= 0 then
 
-	blades = FindJoints("engine", true)
+    	for i = 1, #blades do
+    		local blade = blades[i]
+    		SetJointMotor(blade, 30)
+    	end
 
-	if GetPlayerVehicle() ~= 0 then
+    end
+end
 
-		for i = 1, #blades do
-			local blade = blades[i]
-			SetJointMotor(blade, 30)
-		end
-
-	end
-
-end
```

---

# Migration Report: main\Cessna 172 FUEL\scripts\fuel.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172 FUEL\scripts\fuel.lua
+++ patched/main\Cessna 172 FUEL\scripts\fuel.lua
@@ -1,308 +1,275 @@
--- fuel.lua
--- @date 2022-02-20
--- @author MrRare
--- @brief Fuel logic, detects fuel cells based on shape tags, detect health of fuel cells, make fuel cells go boom, spawns particles, creates debris and spawns more particles
-
-#include "light_spawner/lightspawner.lua"
-#include "particle.lua"
-#include "generic.lua"
-
-Fuel_Cells = {} -- Stores all the found fuel cells
-Fuel_FireSpawnTimeout = 30 -- how long fires/smoke can spawn (and spawn new fires)
-Fuel_FireAmount = 5 -- How many random locations close to the tank should catch and spawn fires
-Fuel_ExplosionAmount = 3 -- How many explosion tanks generate
-Fuel_ExplosionSize = 2 -- How many explosion tanks generate
-Fuel_ExplosionDelay = 0-- Delay between fuel tanks damaged and explosion.
-Fuel_ExplosionFireAmount = 200  -- fuel explosion sudden fire spawn
-Fuel_DebrisAmount = 3 -- AMount of shapes that can be assinged as "debris"
-Fuel_Timer = 0	-- Counts every second
-Fuel_AccurateTimer = 0 -- Counts every frame time
-Fuel_RateTimer = 0 -- Counts every frame time
-Fuel_Rate = (0.9 / 60) * 2 -- You can set the rate to for example (1/60) * 2 = 30 fps spawn and update rate, will improve performance but limit smoke and fire generation by a lot
-Fuel_BigExplosionSound = {} -- List of sounds for explosions
-Fuel_EmitLight = true -- Use pointlights to enhance visuals (slow as hell)
-Fuel_ToggleLightKey = 'L' -- Toggle lights, to give ya a choice
-Fuel_ToggleLightModeKey = 'N' -- Switch between legacy and new method
-Fuel_LightRandomness = 0.3 -- This determines the flickering of the lights  (simulating fire)
-
--- If lights are enabled
-Fuel_ExplosionBrightness = 500  -- Brightness of explosion
-Fuel_BigFireBrightness = 100  -- Brightness of big fires
-Fuel_SmallFireBrightness = 50 -- Brightness of smaller fires
-
-Fuel_OldVersion = false -- Used for switching between old and new light methods
-
-function init()
-	-- Generic_ClearDebugPrinter()
-	-- Load explosion sounds
-	for i=0,3 do
-		Fuel_BigExplosionSound[i] = LoadSound("MOD/main/CRJ-200 FUEL/snd/fail_big/"..i)
-	end
-
-	-- Detect all fuel shapes
-    local fuel_cell_shapes = FindShapes("fuel")
-
-	-- Store them once, determine center, and how many voxels it consists of
-    for i=1, #fuel_cell_shapes do
-        local fuel_cell = fuel_cell_shapes[i]
-		local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell)
-		local center = GetShapeWorldTransform(fuel_cell_shape).pos
-        Fuel_Cells[fuel_cell] = {voxcount=fuel_cell_voxels, damaged=false, exploded=false, spawntime=0, center=center, fire_locations={}, debris=false, debris_count=0, explosion_count=0, strength=tonumber(GetTagValue(fuel_cell, "strength")), light=nil}
+#version 2
+function server.init()
+    -- Detect all fuel shapes
+       local fuel_cell_shapes = FindShapes("fuel")
+    -- Store them once, determine center, and how many voxels it consists of
+       for i=1, #fuel_cell_shapes do
+           local fuel_cell = fuel_cell_shapes[i]
+    	local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell)
+    	local center = GetShapeWorldTransform(fuel_cell_shape).pos
+           Fuel_Cells[fuel_cell] = {voxcount=fuel_cell_voxels, damaged=false, exploded=false, spawntime=0, center=center, fire_locations={}, debris=false, debris_count=0, explosion_count=0, strength=tonumber(GetTagValue(fuel_cell, "strength")), light=nil}
+       end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local last_pressed = InputLastPressedKey()
+        if last_pressed == Fuel_ToggleLightKey then
+        	if Fuel_EmitLight then
+        		Fuel_EmitLight = false
+        		LightSpawner_DeleteAll()
+        		-- DebugWatch("Disabled light during fire/explosions on plane (YOUR PC IS GRATEFULL)")
+        	else
+        		Fuel_EmitLight = true
+        		if Fuel_OldVersion == false then
+        			LightSpawner_DeleteAll()
+        		end
+        		-- DebugWatch("Enabled light during fire/explosions on plane(FPS KILLER)")
+        	end
+        end
+        if last_pressed == Fuel_ToggleLightModeKey then
+        	if Fuel_OldVersion == false then
+        		Fuel_OldVersion = true
+        		LightSpawner_DeleteAll()
+        	else
+        		Fuel_OldVersion = false
+        	end
+        end
+        -- Accurate timer, counts in frame time
+           Fuel_AccurateTimer = Fuel_AccurateTimer + dt
+        -- Second timer, counts in seconds (to prevent rounding errors)
+           if Fuel_AccurateTimer >= 1 then
+               Fuel_Timer = Fuel_Timer + 1
+               Fuel_AccurateTimer = 0
+           end
     end
 end
 
-function tick(dt)
-	local last_pressed = InputLastPressedKey()
-	if last_pressed == Fuel_ToggleLightKey then
-		if Fuel_EmitLight then
-			Fuel_EmitLight = false
-			LightSpawner_DeleteAll()
-			-- DebugWatch("Disabled light during fire/explosions on plane (YOUR PC IS GRATEFULL)")
-		else
-			Fuel_EmitLight = true
-			if Fuel_OldVersion == false then
-				LightSpawner_DeleteAll()
-			end
-			-- DebugWatch("Enabled light during fire/explosions on plane(FPS KILLER)")
-		end
-	end
-
-	if last_pressed == Fuel_ToggleLightModeKey then
-		if Fuel_OldVersion == false then
-			Fuel_OldVersion = true
-			LightSpawner_DeleteAll()
-		else
-			Fuel_OldVersion = false
-		end
-	end
-
-	-- Accurate timer, counts in frame time
-    Fuel_AccurateTimer = Fuel_AccurateTimer + dt
-
-	-- Second timer, counts in seconds (to prevent rounding errors)
-    if Fuel_AccurateTimer >= 1 then
-        Fuel_Timer = Fuel_Timer + 1
-        Fuel_AccurateTimer = 0
+function client.init()
+    for i=0,3 do
+    	Fuel_BigExplosionSound[i] = LoadSound("MOD/main/CRJ-200 FUEL/snd/fail_big/"..i)
     end
-
-	if Fuel_RateTimer > Fuel_Rate then
-		-- For each existing fuel cell
-		for key, value in pairs(Fuel_Cells) do
-			-- Get voxel count and recalculate center every frame.
-			local fuel_cell = value
-			local fuel_cell_shape = key
-			local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell_shape)
-			local center = GetShapeWorldTransform(fuel_cell_shape).pos
-
-		-- Debris (See later) can have issues witht center location, if anything is close to center ignore it.
-			-- Apply newly found center to fuel cell
-			if fuel_cell_voxels > 0 then
-				fuel_cell["center"] = center
-			end
-			-- If fuel cell is not damaged, calculate health of fuel cell
-			if fuel_cell["damaged"] == false then
-				local fuel_cell_health = (fuel_cell_voxels /  fuel_cell["voxcount"]) * 100
-
-				-- DebugWatch("Fuel cell " .. GetTagValue(fuel_cell_shape, "fuel") .. " health (explodes on: " .. GetTagValue(fuel_cell_shape, "strength") .. ") Expl: " .. fuel_cell["explosion_count"], fuel_cell_health)
-
-				if fuel_cell_health > 0 and fuel_cell_health < fuel_cell["strength"] then
-					fuel_cell["damaged"] = true
-					fuel_cell["spawntime"] = Generic_deepCopy(Fuel_Timer)
-				end
-
-			elseif Fuel_Timer - fuel_cell["spawntime"] >= Fuel_FireSpawnTimeout then
-				for x=1, #fuel_cell["fire_locations"] do
-					local fire_location = fuel_cell["fire_locations"][x]
-					LightSpawner_DeleteLight(fire_location[3])
-				end
-				if fuel_cell["light"] ~= nil then
-					LightSpawner_DeleteLight(fuel_cell["light"])
-				end
-				Fuel_Cells[fuel_cell_shape] = nil
-			-- If fuel cell is damaged, and within the timeout range (set when it is detected that it is damaged), spawn fire and such
-			elseif fuel_cell["damaged"] and Fuel_Timer - fuel_cell["spawntime"] < Fuel_FireSpawnTimeout then
-				-- If fuel cell has exploded, detect debris and assign them as "fuel cells that has exploded and thus spawn fire/smoke"
-				if fuel_cell["exploded"] == true then
-					LightSpawner_DeleteTagged("explosion_light")
-
-					-- Only original fuel cells can spawn ALOT of fire/smoke
-					if fuel_cell["debris"] == false then
-						-- DebugCross(center, 0,1,0,1)
-
-						-- Detect debris caused by explosion (most likely) (they will be set on fire as well)
-						if fuel_cell["debris_count"] < Fuel_DebrisAmount  then
-							local outerpoints = Generic_CreateBox(fuel_cell["center"], 8, nil, {1, 0, 0}, false)
-							local shapes = QueryAabbShapes(outerpoints[1], outerpoints[7])
-							-- DebugPrint("Tank " .. GetTagValue(fuel_cell_shape, "fuel") .. "exploded, found " .. #shapes .. " shapes")
-							for s=1, #shapes do
-								local debris = shapes[s]
-								if Fuel_Cells[debris] == nil then
-									-- Make sure not every tiny voxel is counted as debris ;P
-									local debris_center = GetShapeWorldTransform(debris).pos
-									local debris_vox = GetShapeVoxelCount(debris)
-
-									if debris_vox > 1 and debris_vox < 100 then
-										SetTag(debris, "fuel", "debris_" .. GetTagValue(fuel_cell_shape, "fuel"))
-										SpawnFire(debris_center)
-										local light = nil
-										if Fuel_EmitLight then
-											local l = Generic_SpawnLight(debris_center,  Particle_Fire, Generic_rnd((Fuel_BigFireBrightness * Fuel_LightRandomness) / 2 ,Fuel_BigFireBrightness  / 2))
-											light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
-										end
-										Fuel_Cells[debris] = {voxcount=0, damaged=true, exploded=true, spawntime=Generic_deepCopy(Fuel_Timer), center=debris_center, debris=true, debris_count=0, explosion_count=0, strength=nil, fire_locations={}, light=light}
-										if fuel_cell["debris_count"] > Fuel_DebrisAmount then
-											break
-										end
-										fuel_cell["debris_count"] = fuel_cell["debris_count"] + 1
-									end
-
-								end
-							end
-						end
-
-						-- Give the game  100 chances to use raycast to find locations to spawn fire at
-						for x = 0, 100 do
-							if #fuel_cell["fire_locations"] < Fuel_FireAmount then
-								local direction = Vec(Generic_rnd(-1,1),Generic_rnd(-1,1),Generic_rnd(-1,1))
-								local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
-								if hit then
-									local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
-									local hit, point, normal, shape = QueryClosestPoint(newpoint, 1)
-									if hit then
-										local l = Generic_SpawnLight(point,  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-										local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
-										fuel_cell["fire_locations"][#fuel_cell["fire_locations"] + 1] = {point, shape, light}
-										SpawnFire(point)
-									end
-								end
-							else
-								break
-							end
-						end
-
-						-- Then spawn per fire location particles, and doe a closest p oint query to set thhe nearest object on fire
-						for x=1, #fuel_cell["fire_locations"] do
-							local fire_location = fuel_cell["fire_locations"][x]
-							local shape_mat = GetShapeMaterialAtPosition(fire_location[2], fire_location[1])
-							if shape_mat == "" then
-								local hit, point, normal, shape = QueryClosestPoint(fire_location[1], 3)
-								if hit then
-									SpawnFire(point)
-									local random = Generic_rndInt(50,90)
-									Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, point)
-									if Fuel_EmitLight then
-										if Fuel_OldVersion then
-											PointLight(VecAdd(point, Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-										else
-											LightSpawner_SetNewLightLocation(fire_location[3], point)
-										end
-									end
-									fuel_cell["fire_locations"][x][1] = point
-									fuel_cell["fire_locations"][x][2] = shape
-								else
-
-									LightSpawner_DeleteLight(fire_location[3])
-								end
-							else
-								local random = Generic_rndInt(50,90)
-								Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, fire_location[1])
-								if Fuel_EmitLight then
-									if Fuel_OldVersion then
-										PointLight(VecAdd(fire_location[1], Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-									else
-										if LightSpawner_UpdateLightIntensity(fire_location[3], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness)) == nil then
-											LightSpawner_DeleteLight(fire_location[3])
-											local l = Generic_SpawnLight(fire_location[1],  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-											local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], false)
-											fuel_cell["fire_locations"][x][3] = light
-										end
-									end
-								end
-							end
-						end
-
-						-- Give the game  100 chances to use raycast to find locations to cause remainder explosions
-						for x = 0, 100 do
-							if fuel_cell["explosion_count"] < Fuel_ExplosionAmount then
-								local direction = Generic_rndVec(1)
-								local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
-								if hit then
-									local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
-									local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
-									Explosion(newpoint, explsize)
-
-									if Fuel_EmitLight then
-										if Fuel_OldVersion == false then
-											local l = Generic_SpawnLight(newpoint,  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
-											LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
-										end
-									end
-									PlaySound(Fuel_BigExplosionSound[math.random(1,3)],newpoint, explsize * 100)
-									for a=0, Fuel_ExplosionFireAmount do
-										Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, newpoint)
-									end
-									-- For visual effect, spawn bright intensive light (Performance heavy!)
-									fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
-									break
-								end
-							else
-								break
-							end
-						end
-					-- For debris in specific we want to just generate fire/smoke particles at the center of debris, but it can spawn actual when it is close to something
-					elseif  fuel_cell_voxels > 0 then
-						-- DebugCross(center, 1,0,0,1)
-						local hit, point, normal, shape = QueryClosestPoint(fuel_cell["center"], 6)
-						if hit then
-							fuel_cell["center"] = point
-							SpawnFire(point)
-							LightSpawner_SetNewLightLocation(fuel_cell["light"], point)
-							LightSpawner_UpdateLightIntensity(fuel_cell["light"], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness))
-							local random = Generic_rndInt(50,80)
-							Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random+10, fuel_cell["center"])
-						end
-					-- If somehow we end up here, debris no longer exist so might as well forget it
-					else
-						for x=1, #fuel_cell["fire_locations"] do
-							local fire_location = fuel_cell["fire_locations"][x]
-							LightSpawner_DeleteLight(fire_location[3])
-						end
-						if fuel_cell["light"] ~= nil then
-							LightSpawner_DeleteLight(fuel_cell["light"])
-						end
-						Fuel_Cells[fuel_cell_shape] = nil
-					end
-				-- If fuel cell after being damaged hits the explosion delay, create the explosion
-				elseif (Fuel_Timer - fuel_cell["spawntime"] >= Fuel_ExplosionDelay) then
-					-- DebugPrint("Explosion count for " .. GetTagValue(fuel_cell_shape, "fuel") .. " is " .. fuel_cell["explosion_count"] )
-					local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
-					Explosion(fuel_cell["center"], explsize)
-
-					if Fuel_EmitLight then
-						if Fuel_OldVersion == false then
-							local l = Generic_SpawnLight(fuel_cell["center"],  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
-							LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
-						end
-					end
-					PlaySound(Fuel_BigExplosionSound[math.random(1,3)],fuel_cell["center"], explsize * 100)
-					for a=0, Fuel_ExplosionFireAmount do
-						Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, fuel_cell["center"])
-					end
-					-- For visual effect, spawn bright intensive light (Performance heavy!)
-					fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
-
-					fuel_cell["exploded"] = true
-				-- Initial damage will cause a smaller fire, then after some time it will explode
-				else
-					local random = Generic_rndInt(30,60)
-					Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, random, random + 10, fuel_cell["center"])
-				end
-			end
-		end
-		Fuel_RateTimer = 0
-	else
-		Fuel_RateTimer = Fuel_RateTimer + dt
-	end
-
-end
-
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if Fuel_RateTimer > Fuel_Rate then
+    	-- For each existing fuel cell
+    	for key, value in pairs(Fuel_Cells) do
+    		-- Get voxel count and recalculate center every frame.
+    		local fuel_cell = value
+    		local fuel_cell_shape = key
+    		local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell_shape)
+    		local center = GetShapeWorldTransform(fuel_cell_shape).pos
+
+    	-- Debris (See later) can have issues witht center location, if anything is close to center ignore it.
+    		-- Apply newly found center to fuel cell
+    		if fuel_cell_voxels ~= 0 then
+    			fuel_cell["center"] = center
+    		end
+    		-- If fuel cell is not damaged, calculate health of fuel cell
+    		if fuel_cell["damaged"] == false then
+    			local fuel_cell_health = (fuel_cell_voxels /  fuel_cell["voxcount"]) * 100
+
+    			-- DebugWatch("Fuel cell " .. GetTagValue(fuel_cell_shape, "fuel") .. " health (explodes on: " .. GetTagValue(fuel_cell_shape, "strength") .. ") Expl: " .. fuel_cell["explosion_count"], fuel_cell_health)
+
+    			if fuel_cell_health > 0 and fuel_cell_health < fuel_cell["strength"] then
+    				fuel_cell["damaged"] = true
+    				fuel_cell["spawntime"] = Generic_deepCopy(Fuel_Timer)
+    			end
+
+    		elseif Fuel_Timer - fuel_cell["spawntime"] >= Fuel_FireSpawnTimeout then
+    			for x=1, #fuel_cell["fire_locations"] do
+    				local fire_location = fuel_cell["fire_locations"][x]
+    				LightSpawner_DeleteLight(fire_location[3])
+    			end
+    			if fuel_cell["light"] ~= nil then
+    				LightSpawner_DeleteLight(fuel_cell["light"])
+    			end
+    			Fuel_Cells[fuel_cell_shape] = nil
+    		-- If fuel cell is damaged, and within the timeout range (set when it is detected that it is damaged), spawn fire and such
+    		elseif fuel_cell["damaged"] and Fuel_Timer - fuel_cell["spawntime"] < Fuel_FireSpawnTimeout then
+    			-- If fuel cell has exploded, detect debris and assign them as "fuel cells that has exploded and thus spawn fire/smoke"
+    			if fuel_cell["exploded"] == true then
+    				LightSpawner_DeleteTagged("explosion_light")
+
+    				-- Only original fuel cells can spawn ALOT of fire/smoke
+    				if fuel_cell["debris"] == false then
+    					-- DebugCross(center, 0,1,0,1)
+
+    					-- Detect debris caused by explosion (most likely) (they will be set on fire as well)
+    					if fuel_cell["debris_count"] < Fuel_DebrisAmount  then
+    						local outerpoints = Generic_CreateBox(fuel_cell["center"], 8, nil, {1, 0, 0}, false)
+    						local shapes = QueryAabbShapes(outerpoints[1], outerpoints[7])
+    						-- DebugPrint("Tank " .. GetTagValue(fuel_cell_shape, "fuel") .. "exploded, found " .. #shapes .. " shapes")
+    						for s=1, #shapes do
+    							local debris = shapes[s]
+    							if Fuel_Cells[debris] == nil then
+    								-- Make sure not every tiny voxel is counted as debris ;P
+    								local debris_center = GetShapeWorldTransform(debris).pos
+    								local debris_vox = GetShapeVoxelCount(debris)
+
+    								if debris_vox > 1 and debris_vox < 100 then
+    									SetTag(debris, "fuel", "debris_" .. GetTagValue(fuel_cell_shape, "fuel"))
+    									SpawnFire(debris_center)
+    									local light = nil
+    									if Fuel_EmitLight then
+    										local l = Generic_SpawnLight(debris_center,  Particle_Fire, Generic_rnd((Fuel_BigFireBrightness * Fuel_LightRandomness) / 2 ,Fuel_BigFireBrightness  / 2))
+    										light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
+    									end
+    									Fuel_Cells[debris] = {voxcount=0, damaged=true, exploded=true, spawntime=Generic_deepCopy(Fuel_Timer), center=debris_center, debris=true, debris_count=0, explosion_count=0, strength=nil, fire_locations={}, light=light}
+    									if fuel_cell["debris_count"] > Fuel_DebrisAmount then
+    										break
+    									end
+    									fuel_cell["debris_count"] = fuel_cell["debris_count"] + 1
+    								end
+
+    							end
+    						end
+    					end
+
+    					-- Give the game  100 chances to use raycast to find locations to spawn fire at
+    					for x = 0, 100 do
+    						if #fuel_cell["fire_locations"] < Fuel_FireAmount then
+    							local direction = Vec(Generic_rnd(-1,1),Generic_rnd(-1,1),Generic_rnd(-1,1))
+    							local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
+    							if hit then
+    								local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
+    								local hit, point, normal, shape = QueryClosestPoint(newpoint, 1)
+    								if hit then
+    									local l = Generic_SpawnLight(point,  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    									local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
+    									fuel_cell["fire_locations"][#fuel_cell["fire_locations"] + 1] = {point, shape, light}
+    									SpawnFire(point)
+    								end
+    							end
+    						else
+    							break
+    						end
+    					end
+
+    					-- Then spawn per fire location particles, and doe a closest p oint query to set thhe nearest object on fire
+    					for x=1, #fuel_cell["fire_locations"] do
+    						local fire_location = fuel_cell["fire_locations"][x]
+    						local shape_mat = GetShapeMaterialAtPosition(fire_location[2], fire_location[1])
+    						if shape_mat == "" then
+    							local hit, point, normal, shape = QueryClosestPoint(fire_location[1], 3)
+    							if hit then
+    								SpawnFire(point)
+    								local random = Generic_rndInt(50,90)
+    								Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, point)
+    								if Fuel_EmitLight then
+    									if Fuel_OldVersion then
+    										PointLight(VecAdd(point, Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    									else
+    										LightSpawner_SetNewLightLocation(fire_location[3], point)
+    									end
+    								end
+    								fuel_cell["fire_locations"][x][1] = point
+    								fuel_cell["fire_locations"][x][2] = shape
+    							else
+
+    								LightSpawner_DeleteLight(fire_location[3])
+    							end
+    						else
+    							local random = Generic_rndInt(50,90)
+    							Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, fire_location[1])
+    							if Fuel_EmitLight then
+    								if Fuel_OldVersion then
+    									PointLight(VecAdd(fire_location[1], Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    								else
+    									if LightSpawner_UpdateLightIntensity(fire_location[3], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness)) == nil then
+    										LightSpawner_DeleteLight(fire_location[3])
+    										local l = Generic_SpawnLight(fire_location[1],  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    										local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], false)
+    										fuel_cell["fire_locations"][x][3] = light
+    									end
+    								end
+    							end
+    						end
+    					end
+
+    					-- Give the game  100 chances to use raycast to find locations to cause remainder explosions
+    					for x = 0, 100 do
+    						if fuel_cell["explosion_count"] < Fuel_ExplosionAmount then
+    							local direction = Generic_rndVec(1)
+    							local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
+    							if hit then
+    								local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
+    								local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
+    								Explosion(newpoint, explsize)
+
+    								if Fuel_EmitLight then
+    									if Fuel_OldVersion == false then
+    										local l = Generic_SpawnLight(newpoint,  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
+    										LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
+    									end
+    								end
+    								PlaySound(Fuel_BigExplosionSound[math.random(1,3)],newpoint, explsize * 100)
+    								for a=0, Fuel_ExplosionFireAmount do
+    									Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, newpoint)
+    								end
+    								-- For visual effect, spawn bright intensive light (Performance heavy!)
+    								fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
+    								break
+    							end
+    						else
+    							break
+    						end
+    					end
+    				-- For debris in specific we want to just generate fire/smoke particles at the center of debris, but it can spawn actual when it is close to something
+    				elseif  fuel_cell_voxels ~= 0 then
+    					-- DebugCross(center, 1,0,0,1)
+    					local hit, point, normal, shape = QueryClosestPoint(fuel_cell["center"], 6)
+    					if hit then
+    						fuel_cell["center"] = point
+    						SpawnFire(point)
+    						LightSpawner_SetNewLightLocation(fuel_cell["light"], point)
+    						LightSpawner_UpdateLightIntensity(fuel_cell["light"], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness))
+    						local random = Generic_rndInt(50,80)
+    						Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random+10, fuel_cell["center"])
+    					end
+    				-- If somehow we end up here, debris no longer exist so might as well forget it
+    				else
+    					for x=1, #fuel_cell["fire_locations"] do
+    						local fire_location = fuel_cell["fire_locations"][x]
+    						LightSpawner_DeleteLight(fire_location[3])
+    					end
+    					if fuel_cell["light"] ~= nil then
+    						LightSpawner_DeleteLight(fuel_cell["light"])
+    					end
+    					Fuel_Cells[fuel_cell_shape] = nil
+    				end
+    			-- If fuel cell after being damaged hits the explosion delay, create the explosion
+    			elseif (Fuel_Timer - fuel_cell["spawntime"] >= Fuel_ExplosionDelay) then
+    				-- DebugPrint("Explosion count for " .. GetTagValue(fuel_cell_shape, "fuel") .. " is " .. fuel_cell["explosion_count"] )
+    				local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
+    				Explosion(fuel_cell["center"], explsize)
+
+    				if Fuel_EmitLight then
+    					if Fuel_OldVersion == false then
+    						local l = Generic_SpawnLight(fuel_cell["center"],  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
+    						LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
+    					end
+    				end
+    				PlaySound(Fuel_BigExplosionSound[math.random(1,3)],fuel_cell["center"], explsize * 100)
+    				for a=0, Fuel_ExplosionFireAmount do
+    					Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, fuel_cell["center"])
+    				end
+    				-- For visual effect, spawn bright intensive light (Performance heavy!)
+    				fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
+
+    				fuel_cell["exploded"] = true
+    			-- Initial damage will cause a smaller fire, then after some time it will explode
+    			else
+    				local random = Generic_rndInt(30,60)
+    				Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, random, random + 10, fuel_cell["center"])
+    			end
+    		end
+    	end
+    	Fuel_RateTimer = 0
+    else
+    	Fuel_RateTimer = Fuel_RateTimer + dt
+    end
+end
+

```

---

# Migration Report: main\Cessna 172 FUEL\scripts\generic.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172 FUEL\scripts\generic.lua
+++ patched/main\Cessna 172 FUEL\scripts\generic.lua
@@ -1,15 +1,11 @@
--- generic.lua
--- @date 2021-09-06
--- @author Teardown devs
--- @brief Helper functions originaly part of SmokeGun mode by Teardown
-
---Helper to return a random vector of particular length
+#version 2
+local floor = math.floor
+
 function Generic_rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)
 end
 
---Helper to return a random number in range mi to ma
 function Generic_rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
@@ -18,7 +14,6 @@
 	return math.random(mi, ma)
 end
 
--- Deep copy helper
 function Generic_deepCopy(o, seen)
 	seen = seen or {}
 	if o == nil then return nil end
@@ -38,8 +33,6 @@
 	end
 	return no
 end
-
---- A moving average calculator
 
 function Generic_sma(period)
 	local t = {}
@@ -125,7 +118,6 @@
 	return {255 / r, 255 / g, 255 / b}
 end
 
-local floor = math.floor
 function Generic_xor(a, b)
   local r = 0
   for i = 0, 31 do
@@ -148,35 +140,18 @@
     return xored_p1_2wp3
 end
 
-
----Draw a point if visualize fire detection is turned on
----@param point Vec (array of 3 values) containing the position to draw the point
----@param r float intensity of the color red
----@param g float intensity of the color green
----@param b float intensity of the color blue
 function Generic_DrawPoint(point, r, g, b, draw)
     if draw then
         DebugCross(point,  r, g, b)
     end
 end
 
-
----Draw a line between two points if visualize fire detection is turned on
----@param vec1 Vec (array of 3 values) containing the position to draw the point
----@param vec2 Vec (array of 3 values) containing the position to draw the point
----@param r float intensity of the color red
----@param g float intensity of the color green
----@param b float intensity of the color blue
 function Generic_DrawLine(vec1, vec2, r, g, b, draw)
     if draw then
         DebugLine(vec1, vec2, r, g, b)
     end
 end
 
----Calculate distance between two 3D vectors
----@param vec1 Vec (array of 3 values) containing the position
----@param vec2 Vec (array of 3 values) containing the position
----@return number value of the distance
 function Generic_VecDistance(vec1, vec2)
     return VecLength(VecSub(vec1, vec2))
 end
@@ -202,13 +177,11 @@
         Generic_DrawLine(p3, p4, color[1], color[2], color[3], draw)
         Generic_DrawLine(p4, p1, color[1], color[2], color[3], draw)
 
-
         Generic_DrawLine(p5, p6, color[1], color[2], color[3], draw)
         Generic_DrawLine(p6, p7, color[1], color[2], color[3], draw)
         Generic_DrawLine(p7, p8, color[1], color[2], color[3], draw)
         Generic_DrawLine(p8, p5, color[1], color[2], color[3], draw)
 
-
         Generic_DrawLine(p1, p5, color[1], color[2], color[3], draw)
         Generic_DrawLine(p2, p6, color[1], color[2], color[3], draw)
         Generic_DrawLine(p3, p7, color[1], color[2], color[3], draw)
@@ -235,7 +208,6 @@
         local w2 = VecDot(w, p8)
 
         if  (ud > u2 and ud < u1) and (vd > v2 and vd < v1) and (wd > w2 and wd < w1) then
-
 
             Generic_DrawPoint(point2, 1,0,0, draw)
             return true
@@ -278,4 +250,5 @@
     local color = Vec(material["color"]["r"], material["color"]["g"], material["color"]["b"])
     intensity = intensity
     return {point, intensity, intensity, color, true}
-end+end
+

```

---

# Migration Report: main\Cessna 172 FUEL\scripts\light_spawner\lightspawner.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172 FUEL\scripts\light_spawner\lightspawner.lua
+++ patched/main\Cessna 172 FUEL\scripts\light_spawner\lightspawner.lua
@@ -1,17 +1,4 @@
--- lightspwaner.lua
--- @date 2022-02-26
--- @author Eldin Zenderink
--- @brief Spawn FPS friendly lights using spawning of light points (instead of spotlight), side effect it looks a bit worse than spotlights (affects global illumination less), but faster and better than none ;P.
-
-
--- List to keep track of light instance
-LightSpawner_Lights = {}
-LightSpawner_Entities = {}
-
----Deep copy function to create a unreferenced copy of a value (e.g. if you don't want the value you get to upate a existing referenced value in a table)
----@param o any
----@param seen any
----@return any
+#version 2
 function LightSpawner_deepCopy(o, seen)
 	seen = seen or {}
 	if o == nil then return nil end
@@ -31,29 +18,14 @@
 	return no
 end
 
----Helper function to compare two vectors
----@param vec1 Vec
----@param vec2 Vec
----@return boolean (true == the same)
 function LightSpawner_VecCompare(vec1, vec2)
     return ((vec1[1] == vec2[1]) and (vec1[2] == vec2[2]) and (vec1[3] == vec2[3]))
 end
 
----Convert RGB (0-255) to Teardown RGB values (0-1)
----@param r number Red color in values from 0-255
----@param g number Green color in values from 0-255
----@param b number Blue color in values from 0-255
----@return Vec Vector containing teardown compatible colors
 function LightSpawner_RGBConv(r, g, b)
 	return Vec(255 / r, 255 / g, 255 / b)
 end
 
-
-
----XOR helper
----@param a any value to xor
----@param b any value to xor with
----@return integer xored value
 function LightSpawner_xor(a, b)
   local r = 0
   for i = 0, 31 do
@@ -67,9 +39,6 @@
   return r
 end
 
----Generates a unique hash for a vectore
----@param Vec vec
----@return integer
 function LightSpawner_HashVec(vec)
     local p1 = 73856093
     local p2 = 19349663
@@ -79,21 +48,11 @@
     return xored_p1_2wp3
 end
 
----Generate random vector with max lenght
----@param length number
----@return Vec
 function LightSpawner_rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)
 end
 
----Spawns a new light point.
----@param location Vec location of the light point
----@param size number size of the light
----@param intensity number intensity of the light
----@param color Vec color of the light (can be RGB 0-255 values!)
----@param enabled boolean if the light should emit or not (can be toggled)
----@return number id reference compatible with Teardown functions such as SetLightColor, SetLightIntensity, SetLightEnabled, also used as reference for LightSpawner, remember them!
 function LightSpawner_Spawn(location, size, intensity, color, enabled, tag)
     if tag == nil then
         tag = ""
@@ -146,9 +105,6 @@
     DebugWatch("Lights Spawned", count)
 end
 
----Spawns a new light point.
----@param id number light reference returned from LightSpawner_Spawn function
----@return number id reference compatible with Teardown functions such as SetLightColor, SetLightIntensity, SetLightEnabled, also used as reference for LightSpawner, remember them!
 function LightSpawner_ReplaceSpawn(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_deepCopy(LightSpawner_Lights[id])
@@ -179,16 +135,12 @@
     return nil
 end
 
---- Delete all lights spawned
---- @note Make sure if you store light handles locally to remove those as well!
 function LightSpawner_DeleteAll()
     for id, instance in pairs(LightSpawner_Lights) do
         LightSpawner_DeleteLight(id)
     end
 end
 
---- Delete all tagged lights spawned
---- @note Make sure if you store light handles locally to remove those as well!
 function LightSpawner_DeleteTagged(tag)
     local lights = FindLights(tag, true)
     for l=1, #lights do
@@ -197,9 +149,6 @@
     end
 end
 
---- Delete a specific light (disables and removes light, then removes spawned entity)
----@param id number light reference returned from LightSpawner_Spawn function
----@return boolean -- Succeed or failed  (true or false) (failure could mean that the light reference has already been deleted once!)
 function LightSpawner_DeleteLight(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -214,10 +163,6 @@
     end
 end
 
---- Update light color.
----@param light number light reference returned from LightSpawner_Spawn function
----@param color Vec color of the light (can be RGB 0-255 values!)
----@return number The original light reference upon success, or nil on failure (light reference unknown)
 function LightSpawner_UpdateLightColor(id, color)
     if color[1] > 1 or color[2] > 1 or color[3] > 1 then
         color = LightSpawner_RGBConv(color[1], color[2], color[3])
@@ -231,10 +176,6 @@
     return nil
 end
 
---- Update light inensity
----@param id number light reference returned from LightSpawner_Spawn function
----@param intensity number Intensity value (normally between 0 and 1)
----@return number The original light reference upon success, or nil on failure (light reference unknown)
 function LightSpawner_UpdateLightIntensity(id, intensity)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -245,10 +186,6 @@
     return nil
 end
 
---- Enable/Disable light
----@param id number light reference returned from LightSpawner_Spawn function
----@param enable boolean Enable or disable light
----@return number The original light reference upon success, or nil on failure (light reference unknown)
 function LightSpawner_UpdateLightEnabled(id, enable)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -259,11 +196,6 @@
     return nil
 end
 
-
---- Update light location
----@param id number light reference returned from LightSpawner_Spawn function
----@param location Vec Location of the light source.
----@return number The original light reference if no update has happend, updated light reference if changed or nil on failure (light reference unknown)
 function LightSpawner_SetNewLightLocation(id, location)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -276,10 +208,6 @@
     return nil
 end
 
---- Update light size
----@param id number light reference returned from LightSpawner_Spawn function
----@param size number size of the light source.
----@return number The original light reference if no update has happend, updated light reference if changed or nil on failure (light reference unknown)
 function LightSpawner_SetNewLightSize(id, size)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -292,9 +220,6 @@
     return nil
 end
 
----Get light location by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return Vec location = unreferenced vec or nil upon failure (light might not exist)
 function LightSpawner_GetLightLocation(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -303,9 +228,6 @@
     return nil
 end
 
----Get light intensity by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return number intensity = unreferenced number or nil upon failure (light might not exist)
 function LightSpawner_GetLightIntensity(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -314,9 +236,6 @@
     return nil
 end
 
----Get light size by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return number size unreferenced number or nil upon failure (light might not exist)
 function LightSpawner_GetLightSize(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -325,9 +244,6 @@
     return nil
 end
 
----Get light color by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return Vec color  unreferenced vec or nil upon failure (light might not exist)
 function LightSpawner_GetLightColor(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -336,13 +252,11 @@
     return nil
 end
 
----Get light entity compatible with teadown functions
----@param id number light reference returned from LightSpawner_Spawn function
----@return light number unreferenced number or nil upon failure (light might not exist)
 function LightSpawner_GetTeardownLightEntity(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
         return LightSpawner_deepCopy(light_instance["light"])
     end
     return nil
-end+end
+

```

---

# Migration Report: main\Cessna 172 FUEL\scripts\lights.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172 FUEL\scripts\lights.lua
+++ patched/main\Cessna 172 FUEL\scripts\lights.lua
@@ -1,87 +1,83 @@
-function init()
-	btn_navlight = FindShape("nl", true)
-	btn_cabinlight = FindShape("cl", true)
-	btn_instrumentlight = FindShape("ilb", true)
-	
-	light_instrument = FindLight("instrument", true)
-	light_beacon = FindLight("beacon", true)
-	light_cabin = FindLights("cabin", true)
-	light_nav = FindLights("navlight", true)
-	
-	SetTag(btn_navlight, "interact", "Navigation lights")
-	SetTag(btn_cabinlight, "interact", "Cabin lights")
-	SetTag(btn_instrumentlight, "interact", "Instrument light")
-	
-	for i=1,#light_cabin do
-		SetLightEnabled(light_cabin[i], false)
-	end
-	
-	for i=1,#light_nav do
-		SetLightEnabled(light_nav[i], false)
-	end
-	
-	SetLightEnabled(light_instrument, false)
-	SetLightEnabled(light_beacon, false)
-	
-	beacon = false
-	timer = 0
+#version 2
+function server.init()
+    btn_navlight = FindShape("nl", true)
+    btn_cabinlight = FindShape("cl", true)
+    btn_instrumentlight = FindShape("ilb", true)
+    light_instrument = FindLight("instrument", true)
+    light_beacon = FindLight("beacon", true)
+    light_cabin = FindLights("cabin", true)
+    light_nav = FindLights("navlight", true)
+    SetTag(btn_navlight, "interact", "Navigation lights")
+    SetTag(btn_cabinlight, "interact", "Cabin lights")
+    SetTag(btn_instrumentlight, "interact", "Instrument light")
+    for i=1,#light_cabin do
+    	SetLightEnabled(light_cabin[i], false)
+    end
+    for i=1,#light_nav do
+    	SetLightEnabled(light_nav[i], false)
+    end
+    SetLightEnabled(light_instrument, false)
+    SetLightEnabled(light_beacon, false)
+    beacon = false
+    timer = 0
 end
 
-function update(dt)
-	
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if beacon then
+        timer = timer + 1
+        	if timer == 80 then
+        		timer = timer * 0 + 1
+        	end
+        	if timer > 0 and timer < 10 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 10 and timer < 20 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        	if timer >= 20 and timer < 30 then
+        		SetLightEnabled(light_beacon, true)
+        	end
+        	if timer >= 30 and timer < 80 then
+        		SetLightEnabled(light_beacon, false)
+        	end
+        end
+    end
+end
 
-	
-	if GetPlayerInteractShape() == btn_cabinlight and InputPressed("interact") then
-		for i=1,#light_cabin do
-			if IsLightActive(light_cabin[i]) == false then
-				SetLightEnabled(light_cabin[i], true)
-			else
-				SetLightEnabled(light_cabin[i], false)
-			end
-		end
-	end
-	
-	if GetPlayerInteractShape() == btn_navlight and InputPressed("interact") then
-		if not beacon then
-			beacon = true
-		else
-			beacon = false
-		end
-		
-		for i=1,#light_nav do
-			if IsLightActive(light_nav[i]) == false then
-				SetLightEnabled(light_nav[i], true)
-			else
-				SetLightEnabled(light_nav[i], false)
-			end
-		end
-		
-	end
-	
-	if GetPlayerInteractShape() == btn_instrumentlight and InputPressed("interact") then
-		if IsLightActive(light_instrument) == false then
-			SetLightEnabled(light_instrument, true)
-		else
-			SetLightEnabled(light_instrument, false)
-		end
-	end
-	
-	if beacon then
-	timer = timer + 1
-		if timer == 80 then
-			timer = timer * 0 + 1
-		end
-		if timer > 0 and timer < 10 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 10 and timer < 20 then
-			SetLightEnabled(light_beacon, false)
-		end
-		if timer >= 20 and timer < 30 then
-			SetLightEnabled(light_beacon, true)
-		end
-		if timer >= 30 and timer < 80 then
-			SetLightEnabled(light_beacon, false)
-		end
-	end
-end+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if GetPlayerInteractShape(playerId) == btn_cabinlight and InputPressed("interact") then
+    	for i=1,#light_cabin do
+    		if IsLightActive(light_cabin[i]) == false then
+    			SetLightEnabled(light_cabin[i], true)
+    		else
+    			SetLightEnabled(light_cabin[i], false)
+    		end
+    	end
+    end
+    if GetPlayerInteractShape(playerId) == btn_navlight and InputPressed("interact") then
+    	if not beacon then
+    		beacon = true
+    	else
+    		beacon = false
+    	end
+
+    	for i=1,#light_nav do
+    		if IsLightActive(light_nav[i]) == false then
+    			SetLightEnabled(light_nav[i], true)
+    		else
+    			SetLightEnabled(light_nav[i], false)
+    		end
+    	end
+
+    end
+    if GetPlayerInteractShape(playerId) == btn_instrumentlight and InputPressed("interact") then
+    	if IsLightActive(light_instrument) == false then
+    		SetLightEnabled(light_instrument, true)
+    	else
+    		SetLightEnabled(light_instrument, false)
+    	end
+    end
+end
+

```

---

# Migration Report: main\Cessna 172 FUEL\scripts\particle.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Cessna 172 FUEL\scripts\particle.lua
+++ patched/main\Cessna 172 FUEL\scripts\particle.lua
@@ -1,77 +1,4 @@
--- particle.lua
--- @date 2022-02-20
--- @author MrRare
--- @brief Enhanced fire and smoke particle spawner, based on ThiccSmoke & ThiccFire (I am the author of that mod :P).
-
-Particle_Randomness =  0.8
-Particle_TypeFire = {3, 5, 5, 13, 14, 8}
-Particle_TypeSmoke = {3, 5, 3, 5, 3, 5}
-Particle_Duplicator = 1
-Particle_SmokeFadeIn = 0
-Particle_SmokeFadeOut = 5
-Particle_FireFadeIn = 1
-Particle_FireFadeOut = 1
-Particle_FireEmissive = 6
-Particle_Embers = "OFF"
-
-Particle_Fire = {
-    color={r=0.93,g=0.25,b=0.10,a=1},
-    lifetime=5,
-    size=1,
-    gravity=6,
-    speed=1,
-    drag=0.5,
-    variation=0.1,
-	location_random=0.5,
-    custom_direction=nil
-}
-
-Particle_Smoke = {
-    color={r=0.08,g=0.08,b=0.08,a=1},
-    lifetime=8,
-    size=1,
-    gravity=8,
-    speed=2,
-    drag=0.3,
-    variation=0.3,
-	location_random=3,
-    custom_direction=nil
-}
-
-Particle_Fire_Expl = {
-    color={r=0.93,g=0.25,b=0.10,a=1},
-    lifetime=4,
-    size=1,
-    gravity=8,
-    speed=8,
-    drag=0.8,
-    variation=0.3,
-	location_random=4,
-    custom_direction=nil
-}
-
-Particle_Smoke_Expl = {
-    color={r=0,g=0,b=0,a=1},
-    lifetime=8,
-    size=1,
-    gravity=8,
-    speed=10,
-    drag=1,
-    variation=0.1,
-	location_random=4,
-    custom_direction=nil
-}
-
-Particle_FireGradient = {
-    {-0.2, -0.3, -0.3},
-    {0, -0.2, -0.2},
-    {-0.2, -0.1, -0.1},
-    {-0.3, 0, 0},
-    {-0.3, 0.1, 0.2}
-}
-
-
-Particle_SpawningFire = true
+#version 2
 function Particle_FireSmoke(fire_emitter, smoke_emitter,fire_intensity, smoke_intensity, location)
 	if Particle_SpawningFire then
 		Particle_EmitParticle(fire_emitter, location, "fire", fire_intensity)
@@ -133,7 +60,6 @@
 			life = 0.5
 		end
 
-
 		ParticleColor (s_red, s_green, s_blue, red, green, blue)
 		ParticleStretch(0, Generic_rnd(1, Particle_Randomness * 2))
 		ParticleAlpha(alpha, 0, "smooth",  life * (Particle_FireFadeIn / 100),  life * (Particle_FireFadeOut / 100))	-- Ramp up fast, ramp down after 50%
@@ -178,3 +104,4 @@
 		SpawnParticle(VecAdd(location, Generic_rndVec(location_random)), v, life)
 	end
 end
+

```

---

# Migration Report: main\CRJ-200\script\engineprops.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\CRJ-200\script\engineprops.lua
+++ patched/main\CRJ-200\script\engineprops.lua
@@ -1,14 +1,13 @@
-function init()
+#version 2
+function server.init()
+    blades = FindJoints("engine", true)
+    if GetPlayerVehicle(playerId) ~= 0 then
 
-	blades = FindJoints("engine", true)
+    	for i = 1, #blades do
+    		local blade = blades[i]
+    		SetJointMotor(blade, 30)
+    	end
 
-	if GetPlayerVehicle() ~= 0 then
+    end
+end
 
-		for i = 1, #blades do
-			local blade = blades[i]
-			SetJointMotor(blade, 30)
-		end
-
-	end
-
-end
```

---

# Migration Report: main\CRJ-200 FUEL\script\engineprops.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\CRJ-200 FUEL\script\engineprops.lua
+++ patched/main\CRJ-200 FUEL\script\engineprops.lua
@@ -1,49 +1,4 @@
-#include "particle.lua"
-#include "generic.lua"
-
-function init()
-
-	blades = FindJoints("engine", true)
-
-	hull = FindShape("engine_hull")
-	SetShapeCollisionFilter(hull, 2, 255-2)
-	outerblades = FindShapes("outerblade")
-	for b=1, #outerblades do
-		local outerblade = outerblades[b]
-		SetShapeCollisionFilter(outerblade, 2, 255-2)
-	end
-
-	if GetPlayerVehicle() ~= 0 then
-		for i = 1, #blades do
-			local blade = blades[i]
-			SetJointMotor(blade, 30)
-		end
-	end
-
-	engineLoop = LoadLoop("MOD/main/CRJ-200 FUEL/snd/engine.ogg")
-	engine_body = FindBody("engine")
-end
-
-function tick(dt)
-	if engine_body ~= nil then
-		if IsBodyBroken(engine_body) == false then
-			local engine_pos = GetBodyTransform(engine_body).pos
-			pTrans = GetPlayerTransform()
-			if VecLength(VecMult(VecSub(pTrans.pos,engine_pos),Vec(1,1,0.4))) < 5 then
-				SetPlayerVelocity(VecAdd(GetPlayerVelocity(),Vec(0,0,1)))
-				if VecLength(VecSub(pTrans.pos,engine_pos))<2.5 then
-					SetPlayerHealth(0)
-					SetPlayerVelocity(Vec(0,0,5))
-					pTrans.pos[3]= pTrans.pos[3]+3
-					SetPlayerTransform(pTrans)
-				end
-			end
-			PlayLoop(engineLoop,engine_pos,2/VecLength(VecSub(pTrans.pos,engine_pos)))
-		end
-	end
-end
-
-
+#version 2
 function GetBodyVoxelCount(body)
 	local broken = 0
 	local voxels = 0
@@ -60,3 +15,43 @@
 function VecMult(a,b)
 	return Vec(a[1]*b[1],a[2]*b[2],a[3]*b[3])
 end
+
+function server.init()
+    blades = FindJoints("engine", true)
+    hull = FindShape("engine_hull")
+    SetShapeCollisionFilter(hull, 2, 255-2)
+    outerblades = FindShapes("outerblade")
+    for b=1, #outerblades do
+    	local outerblade = outerblades[b]
+    	SetShapeCollisionFilter(outerblade, 2, 255-2)
+    end
+    if GetPlayerVehicle(playerId) ~= 0 then
+    	for i = 1, #blades do
+    		local blade = blades[i]
+    		SetJointMotor(blade, 30)
+    	end
+    end
+    engineLoop = LoadLoop("MOD/main/CRJ-200 FUEL/snd/engine.ogg")
+    engine_body = FindBody("engine")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if engine_body ~= nil then
+    	if IsBodyBroken(engine_body) == false then
+    		local engine_pos = GetBodyTransform(engine_body).pos
+    		pTrans = GetPlayerTransform(playerId)
+    		if VecLength(VecMult(VecSub(pTrans.pos,engine_pos),Vec(1,1,0.4))) < 5 then
+    			SetPlayerVelocity(playerId, VecAdd(GetPlayerVelocity(playerId),Vec(0,0,1)))
+    			if VecLength(VecSub(pTrans.pos,engine_pos))<2.5 then
+    				SetPlayerHealth(playerId, 0)
+    				SetPlayerVelocity(playerId, Vec(0,0,5))
+    				pTrans.pos[3]= pTrans.pos[3]+3
+    				SetPlayerTransform(playerId, pTrans)
+    			end
+    		end
+    		PlayLoop(engineLoop,engine_pos,2/VecLength(VecSub(pTrans.pos,engine_pos)))
+    	end
+    end
+end
+

```

---

# Migration Report: main\CRJ-200 FUEL\script\fuel.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\CRJ-200 FUEL\script\fuel.lua
+++ patched/main\CRJ-200 FUEL\script\fuel.lua
@@ -1,308 +1,275 @@
--- fuel.lua
--- @date 2022-02-20
--- @author MrRare
--- @brief Fuel logic, detects fuel cells based on shape tags, detect health of fuel cells, make fuel cells go boom, spawns particles, creates debris and spawns more particles
-
-#include "light_spawner/lightspawner.lua"
-#include "particle.lua"
-#include "generic.lua"
-
-Fuel_Cells = {} -- Stores all the found fuel cells
-Fuel_FireSpawnTimeout = 30 -- how long fires/smoke can spawn (and spawn new fires)
-Fuel_FireAmount = 5 -- How many random locations close to the tank should catch and spawn fires
-Fuel_ExplosionAmount = 3 -- How many explosion tanks generate
-Fuel_ExplosionSize = 2 -- How many explosion tanks generate
-Fuel_ExplosionDelay = 0-- Delay between fuel tanks damaged and explosion.
-Fuel_ExplosionFireAmount = 200  -- fuel explosion sudden fire spawn
-Fuel_DebrisAmount = 3 -- AMount of shapes that can be assinged as "debris"
-Fuel_Timer = 0	-- Counts every second
-Fuel_AccurateTimer = 0 -- Counts every frame time
-Fuel_RateTimer = 0 -- Counts every frame time
-Fuel_Rate = (0.9 / 60) * 2 -- You can set the rate to for example (1/60) * 2 = 30 fps spawn and update rate, will improve performance but limit smoke and fire generation by a lot
-Fuel_BigExplosionSound = {} -- List of sounds for explosions
-Fuel_EmitLight = true -- Use pointlights to enhance visuals (slow as hell)
-Fuel_ToggleLightKey = 'L' -- Toggle lights, to give ya a choice
-Fuel_ToggleLightModeKey = 'N' -- Switch between legacy and new method
-Fuel_LightRandomness = 0.3 -- This determines the flickering of the lights  (simulating fire)
-
--- If lights are enabled
-Fuel_ExplosionBrightness = 500  -- Brightness of explosion
-Fuel_BigFireBrightness = 100  -- Brightness of big fires
-Fuel_SmallFireBrightness = 50 -- Brightness of smaller fires
-
-Fuel_OldVersion = false -- Used for switching between old and new light methods
-
-function init()
-	-- Generic_ClearDebugPrinter()
-	-- Load explosion sounds
-	for i=0,3 do
-		Fuel_BigExplosionSound[i] = LoadSound("MOD/main/CRJ-200 FUEL/snd/fail_big/"..i)
-	end
-
-	-- Detect all fuel shapes
-    local fuel_cell_shapes = FindShapes("fuel")
-
-	-- Store them once, determine center, and how many voxels it consists of
-    for i=1, #fuel_cell_shapes do
-        local fuel_cell = fuel_cell_shapes[i]
-		local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell)
-		local center = GetShapeWorldTransform(fuel_cell_shape).pos
-        Fuel_Cells[fuel_cell] = {voxcount=fuel_cell_voxels, damaged=false, exploded=false, spawntime=0, center=center, fire_locations={}, debris=false, debris_count=0, explosion_count=0, strength=tonumber(GetTagValue(fuel_cell, "strength")), light=nil}
+#version 2
+function server.init()
+    -- Detect all fuel shapes
+       local fuel_cell_shapes = FindShapes("fuel")
+    -- Store them once, determine center, and how many voxels it consists of
+       for i=1, #fuel_cell_shapes do
+           local fuel_cell = fuel_cell_shapes[i]
+    	local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell)
+    	local center = GetShapeWorldTransform(fuel_cell_shape).pos
+           Fuel_Cells[fuel_cell] = {voxcount=fuel_cell_voxels, damaged=false, exploded=false, spawntime=0, center=center, fire_locations={}, debris=false, debris_count=0, explosion_count=0, strength=tonumber(GetTagValue(fuel_cell, "strength")), light=nil}
+       end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local last_pressed = InputLastPressedKey()
+        if last_pressed == Fuel_ToggleLightKey then
+        	if Fuel_EmitLight then
+        		Fuel_EmitLight = false
+        		LightSpawner_DeleteAll()
+        		-- DebugWatch("Disabled light during fire/explosions on plane (YOUR PC IS GRATEFULL)")
+        	else
+        		Fuel_EmitLight = true
+        		if Fuel_OldVersion == false then
+        			LightSpawner_DeleteAll()
+        		end
+        		-- DebugWatch("Enabled light during fire/explosions on plane(FPS KILLER)")
+        	end
+        end
+        if last_pressed == Fuel_ToggleLightModeKey then
+        	if Fuel_OldVersion == false then
+        		Fuel_OldVersion = true
+        		LightSpawner_DeleteAll()
+        	else
+        		Fuel_OldVersion = false
+        	end
+        end
+        -- Accurate timer, counts in frame time
+           Fuel_AccurateTimer = Fuel_AccurateTimer + dt
+        -- Second timer, counts in seconds (to prevent rounding errors)
+           if Fuel_AccurateTimer >= 1 then
+               Fuel_Timer = Fuel_Timer + 1
+               Fuel_AccurateTimer = 0
+           end
     end
 end
 
-function tick(dt)
-	local last_pressed = InputLastPressedKey()
-	if last_pressed == Fuel_ToggleLightKey then
-		if Fuel_EmitLight then
-			Fuel_EmitLight = false
-			LightSpawner_DeleteAll()
-			-- DebugWatch("Disabled light during fire/explosions on plane (YOUR PC IS GRATEFULL)")
-		else
-			Fuel_EmitLight = true
-			if Fuel_OldVersion == false then
-				LightSpawner_DeleteAll()
-			end
-			-- DebugWatch("Enabled light during fire/explosions on plane(FPS KILLER)")
-		end
-	end
-
-	if last_pressed == Fuel_ToggleLightModeKey then
-		if Fuel_OldVersion == false then
-			Fuel_OldVersion = true
-			LightSpawner_DeleteAll()
-		else
-			Fuel_OldVersion = false
-		end
-	end
-
-	-- Accurate timer, counts in frame time
-    Fuel_AccurateTimer = Fuel_AccurateTimer + dt
-
-	-- Second timer, counts in seconds (to prevent rounding errors)
-    if Fuel_AccurateTimer >= 1 then
-        Fuel_Timer = Fuel_Timer + 1
-        Fuel_AccurateTimer = 0
+function client.init()
+    for i=0,3 do
+    	Fuel_BigExplosionSound[i] = LoadSound("MOD/main/CRJ-200 FUEL/snd/fail_big/"..i)
     end
-
-	if Fuel_RateTimer > Fuel_Rate then
-		-- For each existing fuel cell
-		for key, value in pairs(Fuel_Cells) do
-			-- Get voxel count and recalculate center every frame.
-			local fuel_cell = value
-			local fuel_cell_shape = key
-			local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell_shape)
-			local center = GetShapeWorldTransform(fuel_cell_shape).pos
-
-		-- Debris (See later) can have issues witht center location, if anything is close to center ignore it.
-			-- Apply newly found center to fuel cell
-			if fuel_cell_voxels > 0 then
-				fuel_cell["center"] = center
-			end
-			-- If fuel cell is not damaged, calculate health of fuel cell
-			if fuel_cell["damaged"] == false then
-				local fuel_cell_health = (fuel_cell_voxels /  fuel_cell["voxcount"]) * 100
-
-				-- DebugWatch("Fuel cell " .. GetTagValue(fuel_cell_shape, "fuel") .. " health (explodes on: " .. GetTagValue(fuel_cell_shape, "strength") .. ") Expl: " .. fuel_cell["explosion_count"], fuel_cell_health)
-
-				if fuel_cell_health > 0 and fuel_cell_health < fuel_cell["strength"] then
-					fuel_cell["damaged"] = true
-					fuel_cell["spawntime"] = Generic_deepCopy(Fuel_Timer)
-				end
-
-			elseif Fuel_Timer - fuel_cell["spawntime"] >= Fuel_FireSpawnTimeout then
-				for x=1, #fuel_cell["fire_locations"] do
-					local fire_location = fuel_cell["fire_locations"][x]
-					LightSpawner_DeleteLight(fire_location[3])
-				end
-				if fuel_cell["light"] ~= nil then
-					LightSpawner_DeleteLight(fuel_cell["light"])
-				end
-				Fuel_Cells[fuel_cell_shape] = nil
-			-- If fuel cell is damaged, and within the timeout range (set when it is detected that it is damaged), spawn fire and such
-			elseif fuel_cell["damaged"] and Fuel_Timer - fuel_cell["spawntime"] < Fuel_FireSpawnTimeout then
-				-- If fuel cell has exploded, detect debris and assign them as "fuel cells that has exploded and thus spawn fire/smoke"
-				if fuel_cell["exploded"] == true then
-					LightSpawner_DeleteTagged("explosion_light")
-
-					-- Only original fuel cells can spawn ALOT of fire/smoke
-					if fuel_cell["debris"] == false then
-						-- DebugCross(center, 0,1,0,1)
-
-						-- Detect debris caused by explosion (most likely) (they will be set on fire as well)
-						if fuel_cell["debris_count"] < Fuel_DebrisAmount  then
-							local outerpoints = Generic_CreateBox(fuel_cell["center"], 8, nil, {1, 0, 0}, false)
-							local shapes = QueryAabbShapes(outerpoints[1], outerpoints[7])
-							-- DebugPrint("Tank " .. GetTagValue(fuel_cell_shape, "fuel") .. "exploded, found " .. #shapes .. " shapes")
-							for s=1, #shapes do
-								local debris = shapes[s]
-								if Fuel_Cells[debris] == nil then
-									-- Make sure not every tiny voxel is counted as debris ;P
-									local debris_center = GetShapeWorldTransform(debris).pos
-									local debris_vox = GetShapeVoxelCount(debris)
-
-									if debris_vox > 1 and debris_vox < 100 then
-										SetTag(debris, "fuel", "debris_" .. GetTagValue(fuel_cell_shape, "fuel"))
-										SpawnFire(debris_center)
-										local light = nil
-										if Fuel_EmitLight then
-											local l = Generic_SpawnLight(debris_center,  Particle_Fire, Generic_rnd((Fuel_BigFireBrightness * Fuel_LightRandomness) / 2 ,Fuel_BigFireBrightness  / 2))
-											light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
-										end
-										Fuel_Cells[debris] = {voxcount=0, damaged=true, exploded=true, spawntime=Generic_deepCopy(Fuel_Timer), center=debris_center, debris=true, debris_count=0, explosion_count=0, strength=nil, fire_locations={}, light=light}
-										if fuel_cell["debris_count"] > Fuel_DebrisAmount then
-											break
-										end
-										fuel_cell["debris_count"] = fuel_cell["debris_count"] + 1
-									end
-
-								end
-							end
-						end
-
-						-- Give the game  100 chances to use raycast to find locations to spawn fire at
-						for x = 0, 100 do
-							if #fuel_cell["fire_locations"] < Fuel_FireAmount then
-								local direction = Vec(Generic_rnd(-1,1),Generic_rnd(-1,1),Generic_rnd(-1,1))
-								local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
-								if hit then
-									local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
-									local hit, point, normal, shape = QueryClosestPoint(newpoint, 1)
-									if hit then
-										local l = Generic_SpawnLight(point,  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-										local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
-										fuel_cell["fire_locations"][#fuel_cell["fire_locations"] + 1] = {point, shape, light}
-										SpawnFire(point)
-									end
-								end
-							else
-								break
-							end
-						end
-
-						-- Then spawn per fire location particles, and doe a closest p oint query to set thhe nearest object on fire
-						for x=1, #fuel_cell["fire_locations"] do
-							local fire_location = fuel_cell["fire_locations"][x]
-							local shape_mat = GetShapeMaterialAtPosition(fire_location[2], fire_location[1])
-							if shape_mat == "" then
-								local hit, point, normal, shape = QueryClosestPoint(fire_location[1], 3)
-								if hit then
-									SpawnFire(point)
-									local random = Generic_rndInt(50,90)
-									Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, point)
-									if Fuel_EmitLight then
-										if Fuel_OldVersion then
-											PointLight(VecAdd(point, Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-										else
-											LightSpawner_SetNewLightLocation(fire_location[3], point)
-										end
-									end
-									fuel_cell["fire_locations"][x][1] = point
-									fuel_cell["fire_locations"][x][2] = shape
-								else
-
-									LightSpawner_DeleteLight(fire_location[3])
-								end
-							else
-								local random = Generic_rndInt(50,90)
-								Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, fire_location[1])
-								if Fuel_EmitLight then
-									if Fuel_OldVersion then
-										PointLight(VecAdd(fire_location[1], Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-									else
-										if LightSpawner_UpdateLightIntensity(fire_location[3], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness)) == nil then
-											LightSpawner_DeleteLight(fire_location[3])
-											local l = Generic_SpawnLight(fire_location[1],  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
-											local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], false)
-											fuel_cell["fire_locations"][x][3] = light
-										end
-									end
-								end
-							end
-						end
-
-						-- Give the game  100 chances to use raycast to find locations to cause remainder explosions
-						for x = 0, 100 do
-							if fuel_cell["explosion_count"] < Fuel_ExplosionAmount then
-								local direction = Generic_rndVec(1)
-								local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
-								if hit then
-									local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
-									local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
-									Explosion(newpoint, explsize)
-
-									if Fuel_EmitLight then
-										if Fuel_OldVersion == false then
-											local l = Generic_SpawnLight(newpoint,  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
-											LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
-										end
-									end
-									PlaySound(Fuel_BigExplosionSound[math.random(1,3)],newpoint, explsize * 100)
-									for a=0, Fuel_ExplosionFireAmount do
-										Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, newpoint)
-									end
-									-- For visual effect, spawn bright intensive light (Performance heavy!)
-									fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
-									break
-								end
-							else
-								break
-							end
-						end
-					-- For debris in specific we want to just generate fire/smoke particles at the center of debris, but it can spawn actual when it is close to something
-					elseif  fuel_cell_voxels > 0 then
-						-- DebugCross(center, 1,0,0,1)
-						local hit, point, normal, shape = QueryClosestPoint(fuel_cell["center"], 6)
-						if hit then
-							fuel_cell["center"] = point
-							SpawnFire(point)
-							LightSpawner_SetNewLightLocation(fuel_cell["light"], point)
-							LightSpawner_UpdateLightIntensity(fuel_cell["light"], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness))
-							local random = Generic_rndInt(50,80)
-							Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random+10, fuel_cell["center"])
-						end
-					-- If somehow we end up here, debris no longer exist so might as well forget it
-					else
-						for x=1, #fuel_cell["fire_locations"] do
-							local fire_location = fuel_cell["fire_locations"][x]
-							LightSpawner_DeleteLight(fire_location[3])
-						end
-						if fuel_cell["light"] ~= nil then
-							LightSpawner_DeleteLight(fuel_cell["light"])
-						end
-						Fuel_Cells[fuel_cell_shape] = nil
-					end
-				-- If fuel cell after being damaged hits the explosion delay, create the explosion
-				elseif (Fuel_Timer - fuel_cell["spawntime"] >= Fuel_ExplosionDelay) then
-					-- DebugPrint("Explosion count for " .. GetTagValue(fuel_cell_shape, "fuel") .. " is " .. fuel_cell["explosion_count"] )
-					local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
-					Explosion(fuel_cell["center"], explsize)
-
-					if Fuel_EmitLight then
-						if Fuel_OldVersion == false then
-							local l = Generic_SpawnLight(fuel_cell["center"],  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
-							LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
-						end
-					end
-					PlaySound(Fuel_BigExplosionSound[math.random(1,3)],fuel_cell["center"], explsize * 100)
-					for a=0, Fuel_ExplosionFireAmount do
-						Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, fuel_cell["center"])
-					end
-					-- For visual effect, spawn bright intensive light (Performance heavy!)
-					fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
-
-					fuel_cell["exploded"] = true
-				-- Initial damage will cause a smaller fire, then after some time it will explode
-				else
-					local random = Generic_rndInt(30,60)
-					Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, random, random + 10, fuel_cell["center"])
-				end
-			end
-		end
-		Fuel_RateTimer = 0
-	else
-		Fuel_RateTimer = Fuel_RateTimer + dt
-	end
-
-end
-
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if Fuel_RateTimer > Fuel_Rate then
+    	-- For each existing fuel cell
+    	for key, value in pairs(Fuel_Cells) do
+    		-- Get voxel count and recalculate center every frame.
+    		local fuel_cell = value
+    		local fuel_cell_shape = key
+    		local fuel_cell_voxels = GetShapeVoxelCount(fuel_cell_shape)
+    		local center = GetShapeWorldTransform(fuel_cell_shape).pos
+
+    	-- Debris (See later) can have issues witht center location, if anything is close to center ignore it.
+    		-- Apply newly found center to fuel cell
+    		if fuel_cell_voxels ~= 0 then
+    			fuel_cell["center"] = center
+    		end
+    		-- If fuel cell is not damaged, calculate health of fuel cell
+    		if fuel_cell["damaged"] == false then
+    			local fuel_cell_health = (fuel_cell_voxels /  fuel_cell["voxcount"]) * 100
+
+    			-- DebugWatch("Fuel cell " .. GetTagValue(fuel_cell_shape, "fuel") .. " health (explodes on: " .. GetTagValue(fuel_cell_shape, "strength") .. ") Expl: " .. fuel_cell["explosion_count"], fuel_cell_health)
+
+    			if fuel_cell_health > 0 and fuel_cell_health < fuel_cell["strength"] then
+    				fuel_cell["damaged"] = true
+    				fuel_cell["spawntime"] = Generic_deepCopy(Fuel_Timer)
+    			end
+
+    		elseif Fuel_Timer - fuel_cell["spawntime"] >= Fuel_FireSpawnTimeout then
+    			for x=1, #fuel_cell["fire_locations"] do
+    				local fire_location = fuel_cell["fire_locations"][x]
+    				LightSpawner_DeleteLight(fire_location[3])
+    			end
+    			if fuel_cell["light"] ~= nil then
+    				LightSpawner_DeleteLight(fuel_cell["light"])
+    			end
+    			Fuel_Cells[fuel_cell_shape] = nil
+    		-- If fuel cell is damaged, and within the timeout range (set when it is detected that it is damaged), spawn fire and such
+    		elseif fuel_cell["damaged"] and Fuel_Timer - fuel_cell["spawntime"] < Fuel_FireSpawnTimeout then
+    			-- If fuel cell has exploded, detect debris and assign them as "fuel cells that has exploded and thus spawn fire/smoke"
+    			if fuel_cell["exploded"] == true then
+    				LightSpawner_DeleteTagged("explosion_light")
+
+    				-- Only original fuel cells can spawn ALOT of fire/smoke
+    				if fuel_cell["debris"] == false then
+    					-- DebugCross(center, 0,1,0,1)
+
+    					-- Detect debris caused by explosion (most likely) (they will be set on fire as well)
+    					if fuel_cell["debris_count"] < Fuel_DebrisAmount  then
+    						local outerpoints = Generic_CreateBox(fuel_cell["center"], 8, nil, {1, 0, 0}, false)
+    						local shapes = QueryAabbShapes(outerpoints[1], outerpoints[7])
+    						-- DebugPrint("Tank " .. GetTagValue(fuel_cell_shape, "fuel") .. "exploded, found " .. #shapes .. " shapes")
+    						for s=1, #shapes do
+    							local debris = shapes[s]
+    							if Fuel_Cells[debris] == nil then
+    								-- Make sure not every tiny voxel is counted as debris ;P
+    								local debris_center = GetShapeWorldTransform(debris).pos
+    								local debris_vox = GetShapeVoxelCount(debris)
+
+    								if debris_vox > 1 and debris_vox < 100 then
+    									SetTag(debris, "fuel", "debris_" .. GetTagValue(fuel_cell_shape, "fuel"))
+    									SpawnFire(debris_center)
+    									local light = nil
+    									if Fuel_EmitLight then
+    										local l = Generic_SpawnLight(debris_center,  Particle_Fire, Generic_rnd((Fuel_BigFireBrightness * Fuel_LightRandomness) / 2 ,Fuel_BigFireBrightness  / 2))
+    										light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
+    									end
+    									Fuel_Cells[debris] = {voxcount=0, damaged=true, exploded=true, spawntime=Generic_deepCopy(Fuel_Timer), center=debris_center, debris=true, debris_count=0, explosion_count=0, strength=nil, fire_locations={}, light=light}
+    									if fuel_cell["debris_count"] > Fuel_DebrisAmount then
+    										break
+    									end
+    									fuel_cell["debris_count"] = fuel_cell["debris_count"] + 1
+    								end
+
+    							end
+    						end
+    					end
+
+    					-- Give the game  100 chances to use raycast to find locations to spawn fire at
+    					for x = 0, 100 do
+    						if #fuel_cell["fire_locations"] < Fuel_FireAmount then
+    							local direction = Vec(Generic_rnd(-1,1),Generic_rnd(-1,1),Generic_rnd(-1,1))
+    							local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
+    							if hit then
+    								local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
+    								local hit, point, normal, shape = QueryClosestPoint(newpoint, 1)
+    								if hit then
+    									local l = Generic_SpawnLight(point,  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    									local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], true)
+    									fuel_cell["fire_locations"][#fuel_cell["fire_locations"] + 1] = {point, shape, light}
+    									SpawnFire(point)
+    								end
+    							end
+    						else
+    							break
+    						end
+    					end
+
+    					-- Then spawn per fire location particles, and doe a closest p oint query to set thhe nearest object on fire
+    					for x=1, #fuel_cell["fire_locations"] do
+    						local fire_location = fuel_cell["fire_locations"][x]
+    						local shape_mat = GetShapeMaterialAtPosition(fire_location[2], fire_location[1])
+    						if shape_mat == "" then
+    							local hit, point, normal, shape = QueryClosestPoint(fire_location[1], 3)
+    							if hit then
+    								SpawnFire(point)
+    								local random = Generic_rndInt(50,90)
+    								Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, point)
+    								if Fuel_EmitLight then
+    									if Fuel_OldVersion then
+    										PointLight(VecAdd(point, Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    									else
+    										LightSpawner_SetNewLightLocation(fire_location[3], point)
+    									end
+    								end
+    								fuel_cell["fire_locations"][x][1] = point
+    								fuel_cell["fire_locations"][x][2] = shape
+    							else
+
+    								LightSpawner_DeleteLight(fire_location[3])
+    							end
+    						else
+    							local random = Generic_rndInt(50,90)
+    							Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random + 10, fire_location[1])
+    							if Fuel_EmitLight then
+    								if Fuel_OldVersion then
+    									PointLight(VecAdd(fire_location[1], Generic_rndVec(0.01)), Particle_Fire["color"]["r"] /  1, Particle_Fire["color"]["g"] /  1.75, Particle_Fire["color"]["b"] / 4,  Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    								else
+    									if LightSpawner_UpdateLightIntensity(fire_location[3], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness)) == nil then
+    										LightSpawner_DeleteLight(fire_location[3])
+    										local l = Generic_SpawnLight(fire_location[1],  Particle_Fire, Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness ,Fuel_BigFireBrightness))
+    										local light = LightSpawner_Spawn(l[1], l[2], l[3], l[4], false)
+    										fuel_cell["fire_locations"][x][3] = light
+    									end
+    								end
+    							end
+    						end
+    					end
+
+    					-- Give the game  100 chances to use raycast to find locations to cause remainder explosions
+    					for x = 0, 100 do
+    						if fuel_cell["explosion_count"] < Fuel_ExplosionAmount then
+    							local direction = Generic_rndVec(1)
+    							local hit, dist,n,s = QueryRaycast(fuel_cell["center"], direction, 10)
+    							if hit then
+    								local newpoint = VecAdd(fuel_cell["center"], VecScale(direction, dist))
+    								local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
+    								Explosion(newpoint, explsize)
+
+    								if Fuel_EmitLight then
+    									if Fuel_OldVersion == false then
+    										local l = Generic_SpawnLight(newpoint,  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
+    										LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
+    									end
+    								end
+    								PlaySound(Fuel_BigExplosionSound[math.random(1,3)],newpoint, explsize * 100)
+    								for a=0, Fuel_ExplosionFireAmount do
+    									Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, newpoint)
+    								end
+    								-- For visual effect, spawn bright intensive light (Performance heavy!)
+    								fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
+    								break
+    							end
+    						else
+    							break
+    						end
+    					end
+    				-- For debris in specific we want to just generate fire/smoke particles at the center of debris, but it can spawn actual when it is close to something
+    				elseif  fuel_cell_voxels ~= 0 then
+    					-- DebugCross(center, 1,0,0,1)
+    					local hit, point, normal, shape = QueryClosestPoint(fuel_cell["center"], 6)
+    					if hit then
+    						fuel_cell["center"] = point
+    						SpawnFire(point)
+    						LightSpawner_SetNewLightLocation(fuel_cell["light"], point)
+    						LightSpawner_UpdateLightIntensity(fuel_cell["light"], Generic_rnd(Fuel_BigFireBrightness * Fuel_LightRandomness,Fuel_BigFireBrightness))
+    						local random = Generic_rndInt(50,80)
+    						Particle_FireSmoke(Particle_Fire, Particle_Smoke, random, random+10, fuel_cell["center"])
+    					end
+    				-- If somehow we end up here, debris no longer exist so might as well forget it
+    				else
+    					for x=1, #fuel_cell["fire_locations"] do
+    						local fire_location = fuel_cell["fire_locations"][x]
+    						LightSpawner_DeleteLight(fire_location[3])
+    					end
+    					if fuel_cell["light"] ~= nil then
+    						LightSpawner_DeleteLight(fuel_cell["light"])
+    					end
+    					Fuel_Cells[fuel_cell_shape] = nil
+    				end
+    			-- If fuel cell after being damaged hits the explosion delay, create the explosion
+    			elseif (Fuel_Timer - fuel_cell["spawntime"] >= Fuel_ExplosionDelay) then
+    				-- DebugPrint("Explosion count for " .. GetTagValue(fuel_cell_shape, "fuel") .. " is " .. fuel_cell["explosion_count"] )
+    				local explsize = Generic_rnd(Fuel_ExplosionSize / 2, Fuel_ExplosionSize)
+    				Explosion(fuel_cell["center"], explsize)
+
+    				if Fuel_EmitLight then
+    					if Fuel_OldVersion == false then
+    						local l = Generic_SpawnLight(fuel_cell["center"],  Particle_Fire, Generic_rnd(Fuel_ExplosionBrightness * explsize ,Fuel_ExplosionBrightness * explsize * 2))
+    						LightSpawner_Spawn(l[1], l[2], l[3], l[4], true, "explosion_light")
+    					end
+    				end
+    				PlaySound(Fuel_BigExplosionSound[math.random(1,3)],fuel_cell["center"], explsize * 100)
+    				for a=0, Fuel_ExplosionFireAmount do
+    					Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, 100, 100, fuel_cell["center"])
+    				end
+    				-- For visual effect, spawn bright intensive light (Performance heavy!)
+    				fuel_cell["explosion_count"] = fuel_cell["explosion_count"]  + 1
+
+    				fuel_cell["exploded"] = true
+    			-- Initial damage will cause a smaller fire, then after some time it will explode
+    			else
+    				local random = Generic_rndInt(30,60)
+    				Particle_FireSmoke(Particle_Fire_Expl, Particle_Smoke_Expl, random, random + 10, fuel_cell["center"])
+    			end
+    		end
+    	end
+    	Fuel_RateTimer = 0
+    else
+    	Fuel_RateTimer = Fuel_RateTimer + dt
+    end
+end
+

```

---

# Migration Report: main\CRJ-200 FUEL\script\generic.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\CRJ-200 FUEL\script\generic.lua
+++ patched/main\CRJ-200 FUEL\script\generic.lua
@@ -1,15 +1,11 @@
--- generic.lua
--- @date 2021-09-06
--- @author Teardown devs
--- @brief Helper functions originaly part of SmokeGun mode by Teardown
-
---Helper to return a random vector of particular length
+#version 2
+local floor = math.floor
+
 function Generic_rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)
 end
 
---Helper to return a random number in range mi to ma
 function Generic_rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
@@ -18,7 +14,6 @@
 	return math.random(mi, ma)
 end
 
--- Deep copy helper
 function Generic_deepCopy(o, seen)
 	seen = seen or {}
 	if o == nil then return nil end
@@ -38,8 +33,6 @@
 	end
 	return no
 end
-
---- A moving average calculator
 
 function Generic_sma(period)
 	local t = {}
@@ -125,7 +118,6 @@
 	return {255 / r, 255 / g, 255 / b}
 end
 
-local floor = math.floor
 function Generic_xor(a, b)
   local r = 0
   for i = 0, 31 do
@@ -148,35 +140,18 @@
     return xored_p1_2wp3
 end
 
-
----Draw a point if visualize fire detection is turned on
----@param point Vec (array of 3 values) containing the position to draw the point
----@param r float intensity of the color red
----@param g float intensity of the color green
----@param b float intensity of the color blue
 function Generic_DrawPoint(point, r, g, b, draw)
     if draw then
         DebugCross(point,  r, g, b)
     end
 end
 
-
----Draw a line between two points if visualize fire detection is turned on
----@param vec1 Vec (array of 3 values) containing the position to draw the point
----@param vec2 Vec (array of 3 values) containing the position to draw the point
----@param r float intensity of the color red
----@param g float intensity of the color green
----@param b float intensity of the color blue
 function Generic_DrawLine(vec1, vec2, r, g, b, draw)
     if draw then
         DebugLine(vec1, vec2, r, g, b)
     end
 end
 
----Calculate distance between two 3D vectors
----@param vec1 Vec (array of 3 values) containing the position
----@param vec2 Vec (array of 3 values) containing the position
----@return number value of the distance
 function Generic_VecDistance(vec1, vec2)
     return VecLength(VecSub(vec1, vec2))
 end
@@ -202,13 +177,11 @@
         Generic_DrawLine(p3, p4, color[1], color[2], color[3], draw)
         Generic_DrawLine(p4, p1, color[1], color[2], color[3], draw)
 
-
         Generic_DrawLine(p5, p6, color[1], color[2], color[3], draw)
         Generic_DrawLine(p6, p7, color[1], color[2], color[3], draw)
         Generic_DrawLine(p7, p8, color[1], color[2], color[3], draw)
         Generic_DrawLine(p8, p5, color[1], color[2], color[3], draw)
 
-
         Generic_DrawLine(p1, p5, color[1], color[2], color[3], draw)
         Generic_DrawLine(p2, p6, color[1], color[2], color[3], draw)
         Generic_DrawLine(p3, p7, color[1], color[2], color[3], draw)
@@ -235,7 +208,6 @@
         local w2 = VecDot(w, p8)
 
         if  (ud > u2 and ud < u1) and (vd > v2 and vd < v1) and (wd > w2 and wd < w1) then
-
 
             Generic_DrawPoint(point2, 1,0,0, draw)
             return true
@@ -278,4 +250,5 @@
     local color = Vec(material["color"]["r"], material["color"]["g"], material["color"]["b"])
     intensity = intensity
     return {point, intensity, intensity, color, true}
-end+end
+

```

---

# Migration Report: main\CRJ-200 FUEL\script\light_spawner\lightspawner.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\CRJ-200 FUEL\script\light_spawner\lightspawner.lua
+++ patched/main\CRJ-200 FUEL\script\light_spawner\lightspawner.lua
@@ -1,17 +1,4 @@
--- lightspwaner.lua
--- @date 2022-02-26
--- @author Eldin Zenderink
--- @brief Spawn FPS friendly lights using spawning of light points (instead of spotlight), side effect it looks a bit worse than spotlights (affects global illumination less), but faster and better than none ;P.
-
-
--- List to keep track of light instance
-LightSpawner_Lights = {}
-LightSpawner_Entities = {}
-
----Deep copy function to create a unreferenced copy of a value (e.g. if you don't want the value you get to upate a existing referenced value in a table)
----@param o any
----@param seen any
----@return any
+#version 2
 function LightSpawner_deepCopy(o, seen)
 	seen = seen or {}
 	if o == nil then return nil end
@@ -31,29 +18,14 @@
 	return no
 end
 
----Helper function to compare two vectors
----@param vec1 Vec
----@param vec2 Vec
----@return boolean (true == the same)
 function LightSpawner_VecCompare(vec1, vec2)
     return ((vec1[1] == vec2[1]) and (vec1[2] == vec2[2]) and (vec1[3] == vec2[3]))
 end
 
----Convert RGB (0-255) to Teardown RGB values (0-1)
----@param r number Red color in values from 0-255
----@param g number Green color in values from 0-255
----@param b number Blue color in values from 0-255
----@return Vec Vector containing teardown compatible colors
 function LightSpawner_RGBConv(r, g, b)
 	return Vec(255 / r, 255 / g, 255 / b)
 end
 
-
-
----XOR helper
----@param a any value to xor
----@param b any value to xor with
----@return integer xored value
 function LightSpawner_xor(a, b)
   local r = 0
   for i = 0, 31 do
@@ -67,9 +39,6 @@
   return r
 end
 
----Generates a unique hash for a vectore
----@param Vec vec
----@return integer
 function LightSpawner_HashVec(vec)
     local p1 = 73856093
     local p2 = 19349663
@@ -79,21 +48,11 @@
     return xored_p1_2wp3
 end
 
----Generate random vector with max lenght
----@param length number
----@return Vec
 function LightSpawner_rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)
 end
 
----Spawns a new light point.
----@param location Vec location of the light point
----@param size number size of the light
----@param intensity number intensity of the light
----@param color Vec color of the light (can be RGB 0-255 values!)
----@param enabled boolean if the light should emit or not (can be toggled)
----@return number id reference compatible with Teardown functions such as SetLightColor, SetLightIntensity, SetLightEnabled, also used as reference for LightSpawner, remember them!
 function LightSpawner_Spawn(location, size, intensity, color, enabled, tag)
     if tag == nil then
         tag = ""
@@ -146,9 +105,6 @@
     DebugWatch("Lights Spawned", count)
 end
 
----Spawns a new light point.
----@param id number light reference returned from LightSpawner_Spawn function
----@return number id reference compatible with Teardown functions such as SetLightColor, SetLightIntensity, SetLightEnabled, also used as reference for LightSpawner, remember them!
 function LightSpawner_ReplaceSpawn(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_deepCopy(LightSpawner_Lights[id])
@@ -179,16 +135,12 @@
     return nil
 end
 
---- Delete all lights spawned
---- @note Make sure if you store light handles locally to remove those as well!
 function LightSpawner_DeleteAll()
     for id, instance in pairs(LightSpawner_Lights) do
         LightSpawner_DeleteLight(id)
     end
 end
 
---- Delete all tagged lights spawned
---- @note Make sure if you store light handles locally to remove those as well!
 function LightSpawner_DeleteTagged(tag)
     local lights = FindLights(tag, true)
     for l=1, #lights do
@@ -197,9 +149,6 @@
     end
 end
 
---- Delete a specific light (disables and removes light, then removes spawned entity)
----@param id number light reference returned from LightSpawner_Spawn function
----@return boolean -- Succeed or failed  (true or false) (failure could mean that the light reference has already been deleted once!)
 function LightSpawner_DeleteLight(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -214,10 +163,6 @@
     end
 end
 
---- Update light color.
----@param light number light reference returned from LightSpawner_Spawn function
----@param color Vec color of the light (can be RGB 0-255 values!)
----@return number The original light reference upon success, or nil on failure (light reference unknown)
 function LightSpawner_UpdateLightColor(id, color)
     if color[1] > 1 or color[2] > 1 or color[3] > 1 then
         color = LightSpawner_RGBConv(color[1], color[2], color[3])
@@ -231,10 +176,6 @@
     return nil
 end
 
---- Update light inensity
----@param id number light reference returned from LightSpawner_Spawn function
----@param intensity number Intensity value (normally between 0 and 1)
----@return number The original light reference upon success, or nil on failure (light reference unknown)
 function LightSpawner_UpdateLightIntensity(id, intensity)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -245,10 +186,6 @@
     return nil
 end
 
---- Enable/Disable light
----@param id number light reference returned from LightSpawner_Spawn function
----@param enable boolean Enable or disable light
----@return number The original light reference upon success, or nil on failure (light reference unknown)
 function LightSpawner_UpdateLightEnabled(id, enable)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -259,11 +196,6 @@
     return nil
 end
 
-
---- Update light location
----@param id number light reference returned from LightSpawner_Spawn function
----@param location Vec Location of the light source.
----@return number The original light reference if no update has happend, updated light reference if changed or nil on failure (light reference unknown)
 function LightSpawner_SetNewLightLocation(id, location)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -276,10 +208,6 @@
     return nil
 end
 
---- Update light size
----@param id number light reference returned from LightSpawner_Spawn function
----@param size number size of the light source.
----@return number The original light reference if no update has happend, updated light reference if changed or nil on failure (light reference unknown)
 function LightSpawner_SetNewLightSize(id, size)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -292,9 +220,6 @@
     return nil
 end
 
----Get light location by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return Vec location = unreferenced vec or nil upon failure (light might not exist)
 function LightSpawner_GetLightLocation(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -303,9 +228,6 @@
     return nil
 end
 
----Get light intensity by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return number intensity = unreferenced number or nil upon failure (light might not exist)
 function LightSpawner_GetLightIntensity(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -314,9 +236,6 @@
     return nil
 end
 
----Get light size by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return number size unreferenced number or nil upon failure (light might not exist)
 function LightSpawner_GetLightSize(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -325,9 +244,6 @@
     return nil
 end
 
----Get light color by light reference
----@param id number light reference returned from LightSpawner_Spawn function
----@return Vec color  unreferenced vec or nil upon failure (light might not exist)
 function LightSpawner_GetLightColor(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
@@ -336,13 +252,11 @@
     return nil
 end
 
----Get light entity compatible with teadown functions
----@param id number light reference returned from LightSpawner_Spawn function
----@return light number unreferenced number or nil upon failure (light might not exist)
 function LightSpawner_GetTeardownLightEntity(id)
     if LightSpawner_Lights[id] ~= nil then
         local light_instance = LightSpawner_Lights[id]
         return LightSpawner_deepCopy(light_instance["light"])
     end
     return nil
-end+end
+

```

---

# Migration Report: main\CRJ-200 FUEL\script\particle.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\CRJ-200 FUEL\script\particle.lua
+++ patched/main\CRJ-200 FUEL\script\particle.lua
@@ -1,77 +1,4 @@
--- particle.lua
--- @date 2022-02-20
--- @author MrRare
--- @brief Enhanced fire and smoke particle spawner, based on ThiccSmoke & ThiccFire (I am the author of that mod :P).
-
-Particle_Randomness =  0.8
-Particle_TypeFire = {3, 5, 5, 13, 14, 8}
-Particle_TypeSmoke = {3, 5, 3, 5, 3, 5}
-Particle_Duplicator = 1
-Particle_SmokeFadeIn = 0
-Particle_SmokeFadeOut = 5
-Particle_FireFadeIn = 1
-Particle_FireFadeOut = 1
-Particle_FireEmissive = 6
-Particle_Embers = "OFF"
-
-Particle_Fire = {
-    color={r=0.93,g=0.25,b=0.10,a=1},
-    lifetime=5,
-    size=1,
-    gravity=6,
-    speed=1,
-    drag=0.5,
-    variation=0.1,
-	location_random=0.5,
-    custom_direction=nil
-}
-
-Particle_Smoke = {
-    color={r=0.08,g=0.08,b=0.08,a=1},
-    lifetime=8,
-    size=1,
-    gravity=8,
-    speed=2,
-    drag=0.3,
-    variation=0.3,
-	location_random=3,
-    custom_direction=nil
-}
-
-Particle_Fire_Expl = {
-    color={r=0.93,g=0.25,b=0.10,a=1},
-    lifetime=4,
-    size=1,
-    gravity=8,
-    speed=8,
-    drag=0.8,
-    variation=0.3,
-	location_random=4,
-    custom_direction=nil
-}
-
-Particle_Smoke_Expl = {
-    color={r=0,g=0,b=0,a=1},
-    lifetime=8,
-    size=1,
-    gravity=8,
-    speed=10,
-    drag=1,
-    variation=0.1,
-	location_random=4,
-    custom_direction=nil
-}
-
-Particle_FireGradient = {
-    {-0.2, -0.3, -0.3},
-    {0, -0.2, -0.2},
-    {-0.2, -0.1, -0.1},
-    {-0.3, 0, 0},
-    {-0.3, 0.1, 0.2}
-}
-
-
-Particle_SpawningFire = true
+#version 2
 function Particle_FireSmoke(fire_emitter, smoke_emitter,fire_intensity, smoke_intensity, location)
 	if Particle_SpawningFire then
 		Particle_EmitParticle(fire_emitter, location, "fire", fire_intensity)
@@ -133,7 +60,6 @@
 			life = 0.5
 		end
 
-
 		ParticleColor (s_red, s_green, s_blue, red, green, blue)
 		ParticleStretch(0, Generic_rnd(1, Particle_Randomness * 2))
 		ParticleAlpha(alpha, 0, "smooth",  life * (Particle_FireFadeIn / 100),  life * (Particle_FireFadeOut / 100))	-- Ramp up fast, ramp down after 50%
@@ -178,3 +104,4 @@
 		SpawnParticle(VecAdd(location, Generic_rndVec(location_random)), v, life)
 	end
 end
+

```

---

# Migration Report: main\flight.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\flight.lua
+++ patched/main\flight.lua
@@ -1,71 +1,4 @@
-#include "ui.lua"
-
-freeze = true -- plane is frozen on spawn (allows player to setup its viewpoint)
-
-plane_settings = {
-    boeing={
-        strength=5,
-        max_speed=40,
-        horizontal_decent_modifier = 0.0005,
-        vertical_decent_modifier = 0.0001,
-        can_loop=true
-    },
-    crj200={
-        strength=5,
-        max_speed=35,
-        horizontal_decent_modifier = 0.001,
-        vertical_decent_modifier = 0.0005,
-        can_loop=true
-    },
-    cesna172={
-        strength=1,
-        max_speed=50,
-        horizontal_decent_modifier = 0.001,
-        vertical_decent_modifier = 0.0005,
-        can_loop=true
-    },
-    unknown={
-        strength=1,
-        max_speed=50,
-        horizontal_decent_modifier = 0.0025,
-        vertical_decent_modifier = 0.001,
-        can_loop=true
-    }
-}
-
-
-strength = 10 -- strenght of hte plane (100 - value ) =  percentage of plane that needs to be destroyed until it no longer flies.
-max_speed = 25 -- Speed of plane
-horizontal_decent_modifier = 0.0005
-vertical_decent_modifier = 0.001
-vertical_acceleration_modifier = 0.1
-absolute = false
-startvoxelCount = 0
-spawned = false
-body_start_pos = nil
-body_start_transform = nil
-body_start_angle = nil
-body_angular_dive = 0
-ui = true
-onfloor = false
-plane_type = "unknown"
-loop = false
-dive = 0
-dive_applied = 0
-keep_momentum = true
-
-keybind_pause_unpause = "p"
-keybind_toggle_momentum = "x"
-keybind_speed_up = "m"
-keybind_speed_down = "n"
-keybind_strength_up = "b"
-keybind_strength_down = "v"
-keybind_toggle_loop = "l"
-keybind_dive_angle_up = "h"
-keybind_dive_angle_down = "g"
-keybind_acceleration_up = "r"
-keybind_acceleration_down = "t"
-
+#version 2
 function Generic_rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
@@ -74,8 +7,8 @@
 	return math.random(mi, ma)
 end
 
-function init()
-    a = GetPlayerCameraTransform()
+function server.init()
+    a = GetPlayerCameraTransform(playerId)
     plane = FindBody("plane")
     plane_type = GetTagValue(plane, "plane")
     if plane_type ~= nil and plane_type ~= "" then
@@ -86,7 +19,6 @@
     else
         plane_type = "unknown"
     end
-
     speed = 1
     vert_speed = 0
     horz_speed_fall = 0
@@ -96,17 +28,101 @@
     b = FindShape("bby")
     startmass = GetBodyMass(plane)
     wings = FindShapes("wings")
-
     for i=1,#wings do
         wing = wings[i]
         startvoxelCount = startvoxelCount + GetShapeVoxelCount(wing)
     end
-
     ui = true
     dive = -(body_angular_dive * math.pi / 180)
 end
 
-function tick(dt)
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        currentvoxelCount = 0
+        wings = FindShapes("wings")
+        for i=1,#wings do
+            wing = wings[i]
+            currentvoxelCount = currentvoxelCount + GetShapeVoxelCount(wing)
+        end
+        if currentvoxelCount < startvoxelCount - (startvoxelCount / 100 * strength) then
+            absolute = true
+        end
+        if currentvoxelCount < startvoxelCount - (startvoxelCount / 100 * (strength * 4)) then
+            no_momentum = true
+        end
+        currentmass = GetBodyMass(plane)
+        -- These need to be updated each tick for their new values/positions.
+        local planet = GetBodyTransform(plane)
+        local trVec = Vec(0, vert_speed, -speed)
+        local trVel = TransformToParentPoint(planet, trVec)
+        local velSub = VecSub(trVel, planet.pos)
+        local bias = Vec(0, 0, 0)
+        if freeze then
+            velSub = Vec(0,0,0)
+            if spawned then
+                SetBodyVelocity(plane, velSub)
+                SetBodyTransform(plane, body_start_pos)
+                -- SetBodyAngularVelocity(plane, body_start_angle)
+            end
+        else
+            if not absolute then
+                -- if (planet.pos[2] < maxheight) then
+                --     -- bias[2] = speed
+                --     speed = speed
+                -- end
+                local cur_vel = GetBodyVelocity(plane)
+
+                SetBodyVelocity(plane, velSub)
+                if loop == false then
+
+                    if dive_applied < 60 then
+                        body_start_angle[1] = dive
+                        local trRotVel = TransformToParentPoint(planet, body_start_angle)
+                        body_start_angle = VecSub(trRotVel, planet.pos)
+                    end
+                    SetBodyAngularVelocity(plane, body_start_angle)
+
+                    if dive_applied >= 60 then
+                        body_start_angle[1] = 0
+                    end
+                    dive_applied = dive_applied + 1
+                else
+                    body_start_angle[1] = dive * -1
+                    local trRotVel = TransformToParentPoint(planet, body_start_angle)
+                    body_start_angle = VecSub(trRotVel, planet.pos)
+                    SetBodyAngularVelocity(plane, body_start_angle)
+                end
+                speed = speed + vertical_acceleration_modifier
+                if speed > max_speed then
+                    speed = max_speed
+                end
+            elseif keep_momentum and no_momentum == false then
+                if speed > 3 then
+                    if (planet.pos[2] < 1) then
+                        vert_speed = 0
+                        if onfloor == false then
+                            onfloor = true
+                            horizontal_decent_modifier = horizontal_decent_modifier * 8
+                        end
+                    else
+                        if vert_speed <= -max_speed then
+                            vert_speed = -max_speed
+                        else
+                            vert_speed = vert_speed - (vertical_decent_modifier * ((max_speed - speed + 1)/2)^2)
+                        end
+                    end
+                    SetBodyVelocity(plane, velSub)
+
+                    speed = speed - (horizontal_decent_modifier * (-speed/2)^2)
+                end
+            end
+
+        end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if ui then
         if InputPressed("esc") or InputPressed("return") or InputPressed("lmb") then
             ui = false
@@ -136,7 +152,6 @@
         if InputPressed(keybind_speed_down) then
             max_speed = max_speed - (1 / 3.6 / 4.8) * 10
         end
-
 
         if max_speed < 1 then
             max_speed = 1
@@ -165,286 +180,191 @@
             strength = 1
         end
     end
-
-
     if InputPressed("lmb") and spawned == false then
         body_start_pos = GetBodyTransform(plane)
         body_start_angle = GetBodyAngularVelocity(plane)
         spawned = true
     end
-
     if InputPressed(keybind_pause_unpause) and spawned then
         freeze = false
     end
-
-    currentvoxelCount = 0
-    wings = FindShapes("wings")
-
-    for i=1,#wings do
-        wing = wings[i]
-        currentvoxelCount = currentvoxelCount + GetShapeVoxelCount(wing)
-    end
-
-    if currentvoxelCount < startvoxelCount - (startvoxelCount / 100 * strength) then
-        absolute = true
-    end
-
-    if currentvoxelCount < startvoxelCount - (startvoxelCount / 100 * (strength * 4)) then
-        no_momentum = true
-    end
-    currentmass = GetBodyMass(plane)
-    -- These need to be updated each tick for their new values/positions.
-    local planet = GetBodyTransform(plane)
-    local trVec = Vec(0, vert_speed, -speed)
-    local trVel = TransformToParentPoint(planet, trVec)
-    local velSub = VecSub(trVel, planet.pos)
-    local bias = Vec(0, 0, 0)
-    if freeze then
-        velSub = Vec(0,0,0)
-        if spawned then
-            SetBodyVelocity(plane, velSub)
-            SetBodyTransform(plane, body_start_pos)
-            -- SetBodyAngularVelocity(plane, body_start_angle)
-        end
-    else
-        if not absolute then
-            -- if (planet.pos[2] < maxheight) then
-            --     -- bias[2] = speed
-            --     speed = speed
-            -- end
-            local cur_vel = GetBodyVelocity(plane)
-
-            SetBodyVelocity(plane, velSub)
-            if loop == false then
-
-                if dive_applied < 60 then
-                    body_start_angle[1] = dive
-                    local trRotVel = TransformToParentPoint(planet, body_start_angle)
-                    body_start_angle = VecSub(trRotVel, planet.pos)
-                end
-                SetBodyAngularVelocity(plane, body_start_angle)
-
-                if dive_applied >= 60 then
-                    body_start_angle[1] = 0
-                end
-                dive_applied = dive_applied + 1
-            else
-                body_start_angle[1] = dive * -1
-                local trRotVel = TransformToParentPoint(planet, body_start_angle)
-                body_start_angle = VecSub(trRotVel, planet.pos)
-                SetBodyAngularVelocity(plane, body_start_angle)
-            end
-            speed = speed + vertical_acceleration_modifier
-            if speed > max_speed then
-                speed = max_speed
-            end
-        elseif keep_momentum and no_momentum == false then
-            if speed > 3 then
-                if (planet.pos[2] < 1) then
-                    vert_speed = 0
-                    if onfloor == false then
-                        onfloor = true
-                        horizontal_decent_modifier = horizontal_decent_modifier * 8
-                    end
-                else
-                    if vert_speed <= -max_speed then
-                        vert_speed = -max_speed
-                    else
-                        vert_speed = vert_speed - (vertical_decent_modifier * ((max_speed - speed + 1)/2)^2)
-                    end
-                end
-                SetBodyVelocity(plane, velSub)
-
-                speed = speed - (horizontal_decent_modifier * (-speed/2)^2)
-            end
-        end
-
-    end
-
-end
-
-function draw()
-
-
-    local w = 540
-    local h = 540
-	if ui then
-		-- UiMakeInteractive()
-		-- SetBool("game.disablepause", true)
-        UiTranslate( 30 + w / 2, 30)
-        UiAlign("center")
-		UiColor(0,0,0,0.7)
-		UiImageBox("ui/common/box-solid-10.png", w, h, 10, 10)
-		UiWindow(w, h)
-
-		UiPush()
-			UiTranslate(UiCenter(), 40)
-			UiColor(1,1,1)
-			UiFont("bold.ttf", 32)
-			UiText("Plane Options For: " .. plane_type)
-		UiPop()
-
-		UiTranslate(0, 90)
-
-		UiPush()
-			UiFont("regular.ttf", 20)
-			UiTranslate(30, 0)
-			UiAlign("left")
-			UiColor(0.9, 0.9, 0.9)
-			UiWordWrap(UiWidth()-60)
-			UiText("READ: Configure the plane to be spawned. Press ENTER/ESC or Left Click to place Plane to apply/close menu. Configuration only applies to the current plane and cannot be changed after! See keybinds before each option to change them.")
-		UiPop()
-
-
-		UiTranslate(0, 120)
-
-		UiPush()
-			UiTranslate(UiCenter() + 75, 0)
-			UiFont("regular.ttf", 14)
-			UiColor(1,1,1)
-			UiAlign("right")
-			UiText("Plane Max Speed (Up: " .. keybind_speed_up .. ") (Down: " .. keybind_speed_down .. "):")
-			UiTranslate(10, 0)
-			UiAlign("left")
-			UiColor(1, 1, 0.5)
-			UiText(tostring(max_speed * 3.6 * 4.8) .. " km/h")
-		UiPop()
-
-		UiTranslate(0, 48)
-
-		UiPush()
-			UiTranslate(UiCenter() + 75, 0)
-			UiFont("regular.ttf", 14)
-			UiColor(1,1,1)
-			UiAlign("right")
-            UiText("Plane accelration to max speed: (Up: " .. keybind_acceleration_up .. ") (Down: " .. keybind_acceleration_down .. "):")
-			UiTranslate(10, 0)
-			UiAlign("left")
-			UiColor(1, 1, 0.5)
-			UiText(tostring(vertical_acceleration_modifier * 3.6 * 4.8) .. " km/h per frame")
-		UiPop()
-
-
-        UiTranslate(0, 48)
-
-		UiPush()
-			UiTranslate(UiCenter() + 75, 0)
-			UiFont("regular.ttf", 14)
-			UiColor(1,1,1)
-			UiAlign("right")
-			UiText("Plane Strength (Up: " .. keybind_strength_up .. ") (Down: " .. keybind_strength_down .. "):")
-			UiTranslate(10, 0)
-			UiAlign("left")
-			UiColor(1, 1, 0.5)
-			UiText(tostring(strength) .. " %")
-		UiPop()
-
-
-		UiTranslate(0, 48)
-
-		UiPush()
-			UiTranslate(UiCenter() + 75, 0)
-			UiFont("regular.ttf", 14)
-			UiColor(1,1,1)
-			UiAlign("right")
-            UiText("Plane attempts dive: (Up: " .. keybind_dive_angle_up .. ") (Down: " .. keybind_dive_angle_down .. "):")
-			UiTranslate(10, 0)
-			UiAlign("left")
-			UiColor(1, 1, 0.5)
-			UiText(tostring(body_angular_dive) .. " degrees.")
-		UiPop()
-
-        if plane_settings[plane_type]["can_loop"] ~= nil then
-            UiTranslate(0, 48)
-            UiPush()
-                UiTranslate(UiCenter() + 75, 0)
-                UiFont("regular.ttf", 14)
-                UiColor(1,1,1)
-                UiAlign("right")
-                UiText("Plane attempts barrelrolls: (Toggle: " .. keybind_toggle_loop .. "):")
-                UiTranslate(10, 0)
-                UiAlign("left")
-                UiColor(1, 1, 0.5)
-                if loop then
-                    UiText("true")
-                else
-                    UiText("false")
-                end
-            UiPop()
-        end
-
-
-        UiTranslate(0, 48)
-        UiPush()
-            UiTranslate(UiCenter() + 75, 0)
-            UiFont("regular.ttf", 14)
-            UiColor(1,1,1)
-            UiAlign("right")
-            UiText("Note, applies force after hitting ground")
-            UiTranslate(0, 24)
-            UiText("Note, turn this off for original (previous version) behavior.")
-            UiTranslate(0, 24)
-            UiText("Plane keeps realisitic momentum when damaged: (Toggle: " .. keybind_toggle_momentum .. "):")
-            UiTranslate(10, 0)
-            UiAlign("left")
-            UiColor(1, 1, 0.5)
-            if keep_momentum then
-                UiText("true")
-            else
-                UiText("false")
-            end
-        UiPop()
-		-- UiTranslate(0, 48)
-
-
-		-- UiPush()
-        --     UiFont("bold.ttf", 20)
-        --     UiTranslate(UiCenter() - w / 2 + 40, 0)
-        --     UiAlign("left")
-        --     UiColor(0.9, 0.9, 0.9)
-        --     UiWordWrap(UiWidth()-60)
-        --     UiText("The following configuration is applied if plane is damaged beyond " .. tostring(strength) .. "%.")
-        -- UiPop()
-
-		-- UiTranslate(0, 48)
-
-		-- UiPush()
-        --     UiTranslate(UiCenter() + 75, 0)
-        --     UiFont("regular.ttf", 20)
-        --     UiColor(1,1,1)
-        --     UiAlign("right")
-        --     UiText("Vertical Deacceleration(Up: " .. keybind_ver_dec_mf_up .. ") (Down: " .. keybind_ver_dec_mf_down .. "):")
-        --     UiTranslate(10, 0)
-        --     UiAlign("left")
-        --     UiColor(1, 1, 0.5)
-        --     UiText(tostring(vertical_decent_modifier))
-        -- UiPop()
-
-
-		-- UiTranslate(0, 48)
-
-		-- UiPush()
-        --     UiTranslate(UiCenter() + 75, 0)
-        --     UiFont("regular.ttf", 20)
-        --     UiColor(1,1,1)
-        --     UiAlign("right")
-        --     UiText("Horizontal Deacceleration (Up: " .. keybind_hor_dec_mf_up .. ") (Down: " .. keybind_hor_dec_mf_down .. "):")
-        --     UiTranslate(10, 0)
-        --     UiAlign("left")
-        --     UiColor(1, 1, 0.5)
-        --     UiText(tostring(horizontal_decent_modifier))
-        -- UiPop()
-    else
-        if freeze then
-            UiColor(1, 1, 1)
-            UiTranslate(30, 30)
-            UiRect(10, 60)
-            UiTranslate(40, 0)
-            UiRect(10, 60)
-            UiColor(1, 0, 0)
-            UiTranslate(-40, 90)
-            UiFont("regular.ttf", 20)
-            UiText("Press '" .. keybind_pause_unpause .."' to start flight!")
-        end
-    end
-end+end
+
+function client.draw()
+       local w = 540
+       local h = 540
+    if ui then
+    	-- UiMakeInteractive()
+    	-- SetBool("game.disablepause", true, true)
+           UiTranslate( 30 + w / 2, 30)
+           UiAlign("center")
+    	UiColor(0,0,0,0.7)
+    	UiImageBox("ui/common/box-solid-10.png", w, h, 10, 10)
+    	UiWindow(w, h)
+
+    	UiPush()
+    		UiTranslate(UiCenter(), 40)
+    		UiColor(1,1,1)
+    		UiFont("bold.ttf", 32)
+    		UiText("Plane Options For: " .. plane_type)
+    	UiPop()
+
+    	UiTranslate(0, 90)
+
+    	UiPush()
+    		UiFont("regular.ttf", 20)
+    		UiTranslate(30, 0)
+    		UiAlign("left")
+    		UiColor(0.9, 0.9, 0.9)
+    		UiWordWrap(UiWidth()-60)
+    		UiText("READ: Configure the plane to be spawned. Press ENTER/ESC or Left Click to place Plane to apply/close menu. Configuration only applies to the current plane and cannot be changed after! See keybinds before each option to change them.")
+    	UiPop()
+
+    	UiTranslate(0, 120)
+
+    	UiPush()
+    		UiTranslate(UiCenter() + 75, 0)
+    		UiFont("regular.ttf", 14)
+    		UiColor(1,1,1)
+    		UiAlign("right")
+    		UiText("Plane Max Speed (Up: " .. keybind_speed_up .. ") (Down: " .. keybind_speed_down .. "):")
+    		UiTranslate(10, 0)
+    		UiAlign("left")
+    		UiColor(1, 1, 0.5)
+    		UiText(tostring(max_speed * 3.6 * 4.8) .. " km/h")
+    	UiPop()
+
+    	UiTranslate(0, 48)
+
+    	UiPush()
+    		UiTranslate(UiCenter() + 75, 0)
+    		UiFont("regular.ttf", 14)
+    		UiColor(1,1,1)
+    		UiAlign("right")
+               UiText("Plane accelration to max speed: (Up: " .. keybind_acceleration_up .. ") (Down: " .. keybind_acceleration_down .. "):")
+    		UiTranslate(10, 0)
+    		UiAlign("left")
+    		UiColor(1, 1, 0.5)
+    		UiText(tostring(vertical_acceleration_modifier * 3.6 * 4.8) .. " km/h per frame")
+    	UiPop()
+
+           UiTranslate(0, 48)
+
+    	UiPush()
+    		UiTranslate(UiCenter() + 75, 0)
+    		UiFont("regular.ttf", 14)
+    		UiColor(1,1,1)
+    		UiAlign("right")
+    		UiText("Plane Strength (Up: " .. keybind_strength_up .. ") (Down: " .. keybind_strength_down .. "):")
+    		UiTranslate(10, 0)
+    		UiAlign("left")
+    		UiColor(1, 1, 0.5)
+    		UiText(tostring(strength) .. " %")
+    	UiPop()
+
+    	UiTranslate(0, 48)
+
+    	UiPush()
+    		UiTranslate(UiCenter() + 75, 0)
+    		UiFont("regular.ttf", 14)
+    		UiColor(1,1,1)
+    		UiAlign("right")
+               UiText("Plane attempts dive: (Up: " .. keybind_dive_angle_up .. ") (Down: " .. keybind_dive_angle_down .. "):")
+    		UiTranslate(10, 0)
+    		UiAlign("left")
+    		UiColor(1, 1, 0.5)
+    		UiText(tostring(body_angular_dive) .. " degrees.")
+    	UiPop()
+
+           if plane_settings[plane_type]["can_loop"] ~= nil then
+               UiTranslate(0, 48)
+               UiPush()
+                   UiTranslate(UiCenter() + 75, 0)
+                   UiFont("regular.ttf", 14)
+                   UiColor(1,1,1)
+                   UiAlign("right")
+                   UiText("Plane attempts barrelrolls: (Toggle: " .. keybind_toggle_loop .. "):")
+                   UiTranslate(10, 0)
+                   UiAlign("left")
+                   UiColor(1, 1, 0.5)
+                   if loop then
+                       UiText("true")
+                   else
+                       UiText("false")
+                   end
+               UiPop()
+           end
+
+           UiTranslate(0, 48)
+           UiPush()
+               UiTranslate(UiCenter() + 75, 0)
+               UiFont("regular.ttf", 14)
+               UiColor(1,1,1)
+               UiAlign("right")
+               UiText("Note, applies force after hitting ground")
+               UiTranslate(0, 24)
+               UiText("Note, turn this off for original (previous version) behavior.")
+               UiTranslate(0, 24)
+               UiText("Plane keeps realisitic momentum when damaged: (Toggle: " .. keybind_toggle_momentum .. "):")
+               UiTranslate(10, 0)
+               UiAlign("left")
+               UiColor(1, 1, 0.5)
+               if keep_momentum then
+                   UiText("true")
+               else
+                   UiText("false")
+               end
+           UiPop()
+    	-- UiTranslate(0, 48)
+
+    	-- UiPush()
+           --     UiFont("bold.ttf", 20)
+           --     UiTranslate(UiCenter() - w / 2 + 40, 0)
+           --     UiAlign("left")
+           --     UiColor(0.9, 0.9, 0.9)
+           --     UiWordWrap(UiWidth()-60)
+           --     UiText("The following configuration is applied if plane is damaged beyond " .. tostring(strength) .. "%.")
+           -- UiPop()
+
+    	-- UiTranslate(0, 48)
+
+    	-- UiPush()
+           --     UiTranslate(UiCenter() + 75, 0)
+           --     UiFont("regular.ttf", 20)
+           --     UiColor(1,1,1)
+           --     UiAlign("right")
+           --     UiText("Vertical Deacceleration(Up: " .. keybind_ver_dec_mf_up .. ") (Down: " .. keybind_ver_dec_mf_down .. "):")
+           --     UiTranslate(10, 0)
+           --     UiAlign("left")
+           --     UiColor(1, 1, 0.5)
+           --     UiText(tostring(vertical_decent_modifier))
+           -- UiPop()
+
+    	-- UiTranslate(0, 48)
+
+    	-- UiPush()
+           --     UiTranslate(UiCenter() + 75, 0)
+           --     UiFont("regular.ttf", 20)
+           --     UiColor(1,1,1)
+           --     UiAlign("right")
+           --     UiText("Horizontal Deacceleration (Up: " .. keybind_hor_dec_mf_up .. ") (Down: " .. keybind_hor_dec_mf_down .. "):")
+           --     UiTranslate(10, 0)
+           --     UiAlign("left")
+           --     UiColor(1, 1, 0.5)
+           --     UiText(tostring(horizontal_decent_modifier))
+           -- UiPop()
+       else
+           if freeze then
+               UiColor(1, 1, 1)
+               UiTranslate(30, 30)
+               UiRect(10, 60)
+               UiTranslate(40, 0)
+               UiRect(10, 60)
+               UiColor(1, 0, 0)
+               UiTranslate(-40, 90)
+               UiFont("regular.ttf", 20)
+               UiText("Press '" .. keybind_pause_unpause .."' to start flight!")
+           end
+       end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\img\ID.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\img\ID.lua
+++ patched/main\Gore Ragdolls 2\img\ID.lua
@@ -1,5 +1,7 @@
-function draw()
-  UiPush()
-	UiImageBox('MOD/main/Gore Ragdolls 2/img/ID.png',UiWidth(),UiHeight())
-  UiPop()
-end+#version 2
+function client.draw()
+     UiPush()
+    UiImageBox('MOD/main/Gore Ragdolls 2/img/ID.png',UiWidth(),UiHeight())
+     UiPop()
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\img\ID2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\img\ID2.lua
+++ patched/main\Gore Ragdolls 2\img\ID2.lua
@@ -1,5 +1,7 @@
-function draw()
-  UiPush()
-	UiImageBox('MOD/main/Gore Ragdolls 2/img/ID2.png',UiWidth(),UiHeight())
-  UiPop()
-end+#version 2
+function client.draw()
+     UiPush()
+    UiImageBox('MOD/main/Gore Ragdolls 2/img/ID2.png',UiWidth(),UiHeight())
+     UiPop()
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\fakegore.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\fakegore.lua
+++ patched/main\Gore Ragdolls 2\scripts\fakegore.lua
@@ -1,27 +1,32 @@
-function init()
-	TORSO = FindShape("TORSO")
+#version 2
+function server.init()
+    TORSO = FindShape("TORSO")
 end
-function tick()
-	if not done then
-	bodyparts = FindShapes("bodypart")
 
-		for i=1,#bodyparts do
-			if IsShapeBroken(bodyparts[i]) then
-			deleteandspawn = true
-			cooltrans = GetShapeWorldTransform(TORSO)
-			end
-		end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not done then
+        bodyparts = FindShapes("bodypart")
 
-		if deleteandspawn then
-		shapes = FindShapes("")
-		ragdollname = GetTagValue(TORSO, "ragdollname")
-			for i=1,#shapes do
-				Delete(shapes[i])
-			end
-			--DebugPrint("Ragdoll name: ".. ragdollname)
-			Spawn("MOD/main/Gore Ragdolls 2/Sitters/" .. ragdollname .. ".xml", Transform(cooltrans.pos, cooltrans.rot))
-			done = true
-			--DebugPrint("MOD/main/Gore Ragdolls 2/Sitters/" .. ragdollname .. ".xml")
-		end
-	end
-end	
+        	for i=1,#bodyparts do
+        		if IsShapeBroken(bodyparts[i]) then
+        		deleteandspawn = true
+        		cooltrans = GetShapeWorldTransform(TORSO)
+        		end
+        	end
+
+        	if deleteandspawn then
+        	shapes = FindShapes("")
+        	ragdollname = GetTagValue(TORSO, "ragdollname")
+        		for i=1,#shapes do
+        			Delete(shapes[i])
+        		end
+        		--DebugPrint("Ragdoll name: ".. ragdollname)
+        		Spawn("MOD/main/Gore Ragdolls 2/Sitters/" .. ragdollname .. ".xml", Transform(cooltrans.pos, cooltrans.rot))
+        		done = true
+        		--DebugPrint("MOD/main/Gore Ragdolls 2/Sitters/" .. ragdollname .. ".xml")
+        	end
+        end
+    end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\GoreAi.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\GoreAi.lua
+++ patched/main\Gore Ragdolls 2\scripts\GoreAi.lua
@@ -1,257 +1,6 @@
-ak47projectileHandler = {
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
-
-
-function init()
-	ShoulderJoints = FindJoints("shoulder")
-	ArmJoints = FindJoints("hand1")
-	Eyes = FindBody("Head")
-	Torso = FindBody("Torso")
-	RRARM = FindBody("LLARM")
-	HipJoints = FindJoints("hip")
-	KneeJoints = FindJoints("knee")
-	walktim = 0
-	speed = 0.07
-
-	shootTimer = 0
-	shotDelay = 0.09
-	damage = 0.15
-	gravity = Vec(0, -40, 0)
-	velocity = 300 --tonumber(GetTagValue(barrel, "bulletspeed"))
-	maxMomentum = 6
-	ShootTimMax = 0.5
-	--GetTagValue(barrel,"gun")
-	--shoot = LoadSound("MOD/snd/".."makarov"..".ogg")
-	shoot = LoadSound("MOD/snd/"..GetTagValue(barrel, "gun")..".ogg")
-	BulletsShot = 0
-	oldbulletsshot = 0
-	bulletsshot = 1
-	reloading = false
-	reloadtim = 0
-	maxreloadtim = 3
-	barrel = FindShape("barrel")
-	MagSize = tonumber(GetTagValue(barrel, "magsize"))
-	maxrange = tonumber(GetTagValue(barrel, "range"))/2
-	damage = tonumber(GetTagValue(barrel, "damage"))
-	firerate = tonumber(GetTagValue(barrel, "firerate"))
-	ShootTimer = math.random(1,firerate*100)/100
-	Fucked = false
-	Torso = FindBody("Torso")
-	Head = FindBody("Head")
-	canSeePlayer = false
-	if GetTagValue(barrel, "team") == "friend" then
-		SetTag(Torso, "friend")
-		SetTag(Head, "friendhead")
-		team = 1
-	end
-	if GetTagValue(barrel, "team") == "enemy"then
-		SetTag(Torso, "enemy")
-		SetTag(Head, "enemyhead")
-		SetTag(Torso, "shooting_target")
-		team = 2
-	end
-	for i=1, 150 do
-		ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
-	end
-	if HasTag(barrel, "rpg") then
-		rpg = true
-		gravity = Vec(0, -2, 0)
-		velocity = 70
-	end
-	if HasTag(barrel, "stationary") then
-		nowalk = true
-	end
-	DrawTeam = true
-end
-
-function update(dt)
-	if InputPressed("J") then
-		canSeePlayer = true
-	end
-	Radios = FindShapes("Spawn",true)
-	--DebugPrint("Radios: "..#Radios)
-	for i=1,#Radios do
-		Radio = Radios[i]
-		DistToRadio = VecLength(VecSub(GetShapeWorldTransform(Radio).pos, GetBodyTransform(Torso).pos))
-		if DistToRadio < 5 then
-			canSeePlayer = true
-		end
-	end
-
-	if InputPressed("L") then
-		optimizedead()
-	end
-	if InputPressed("M") then
-		optimize()
-	end
-	if Fucked then
-		RemoveTag(Torso, "friend")
-		RemoveTag(Torso, "enemy")
-		RemoveTag(Head, "friendhead")
-		RemoveTag(Head, "enemyhead")
-		RemoveTag(Torso, "shooting_target")
-	end
-	if InputPressed("H") then
-		DrawTeam = false
-	end
-	if DrawTeam then
-	if GetTagValue(barrel, "team") == "friend" and not Fucked then
-		TT = GetBodyTransform(Torso)
-		DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 1,0,0)
-	end
-	if GetTagValue(barrel, "team") == "enemy" and not Fucked then
-		TT = GetBodyTransform(Torso)
-		DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 0,0,1)
-	end
-	if Fucked then
-		TT = GetBodyTransform(Torso)
-		--DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 2, TT.pos[3]), 0.5,0.5,0.5)
-	end
-	end
-
-	if HasTag(Torso, "dead") or HasTag(Torso, "panicked") then
-		Fucked = true
-	end
-	-- LOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOOOLOLOLOLOLOL
-	if team == 1 then
-		enemies = FindBodies("enemy",true)
-		enemieshead = FindBodies("enemyhead",true)
-	end
-	if team == 2 then
-		enemies = FindBodies("friend",true)
-		enemieshead = FindBodies("friendhead",true)
-	end
-
-	for k=1,#enemies do
-		E = enemies[k]
-		H = enemieshead[k]
-		disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, GetBodyTransform(E).pos))
-		if disttoenemy < 155 then
-			enemyhead = GetBodyTransform(H)
-			enemy = GetBodyTransform(E)
-			for i=1,#enemies do
-				Secondaryenemytrans = GetBodyTransform(enemies[i])
-				disttosecondary = VecLength(VecSub(Secondaryenemytrans.pos, GetBodyTransform(Torso).pos))
-				disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, enemy.pos))
-				Player = GetPlayerTransform()
-				disttoplayerz = VecLength(VecSub(GetBodyTransform(Torso).pos, Player.pos))
-				if disttosecondary < disttoenemy then
-					enemy = Secondaryenemytrans
-					--DebugCross(enemy)
-				end
-				if disttoplayerz < disttosecondary and team == 1 then
-					Player.pos[2] = Player.pos[2] + 1
-					enemy = Player
-					--DebugCross(enemy)
-				end
-				if disttoplayerz < disttoenemy and team == 1 then
-					Player.pos[2] = Player.pos[2] + 1
-					enemy = Player
-					--DebugCross(enemy)
-				end
-			end
-		end
-	end
-	if #enemies == 0 and team == 1 then
-		Player = GetPlayerTransform()
-		disttoplayerz = VecLength(VecSub(GetBodyTransform(Torso).pos, Player.pos))
-		if disttoplayerz < 155 then
-			Player.pos[2] = Player.pos[2] + 1
-			enemy = Player
-
-		end
-	end
-	--DebugPrint(canSeePlayer())
-	if #enemies > 0 or DoPlayer then
-	gunTrans = GetBodyTransform(Eyes)
-	gunPos = gunTrans.pos
-	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
-	shootPos = VecAdd(gunPos, VecScale(direction,0.2))
-	disttoplayer = VecLength(VecSub(enemy.pos, gunTrans.pos))
-	if reloading then
-		--DebugPrint(reloadtim)
-		reloadtim = reloadtim + dt
-		if reloadtim > maxreloadtim then
-			reloading = false
-			reloadtim = 0
-			BulletsShot = 0
-			bulletsshot = 0
-		end
-	end
-	end
-
-	ShootTimer = ShootTimer + dt
-
-	Player = GetPlayerTransform()
-	disttoplayerz = VecLength(VecSub(GetBodyTransform(Torso).pos, Player.pos))
-	if disttoplayerz < 155 and team == 1 and #enemies < 1 then
-		DoPlayer = true
-	else
-		DoPlayer = false
-	end
-	if #enemies > 0 or DoPlayer then
-	if not Fucked then
-	faceplayer()
-	end
-	end
-
-	if #enemies > 0 or DoPlayer then
-	if canSeePlayer and not Fucked then
-		agro = true
-		aimweapon()
-		runtoenemy()
-		if disttoplayer > maxrange then
-		run = true
-	else
-		run = false
-		agro = false
-	end
-	end
-	end
-
-	if #enemies > 0 or DoPlayer then
-	if canSeePlayer and ShootTimer > firerate and not reloading and not Fucked then
-		if not run then
-		Shoot()
-		BulletsShot = BulletsShot + 1
-		bulletsshot = bulletsshot + 1
-		if BulletsShot == MagSize or bulletsshot > MagSize then
-			reloading = true
-		end
-		ShootTimer = 0
-	end
-end
-	end
-end
-
-function tick()
-	for key, shell in ipairs(ak47projectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-    end
-
+#version 2
 function canSeePlayer()
-    local camTrans = GetPlayerCameraTransform()
+    local camTrans = GetPlayerCameraTransform(playerId)
 	local playerPos = camTrans.pos
 
 	--Direction to player
@@ -259,7 +8,7 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	rejectragdoll()
 	bodypartz = FindBodies("bodypart",true)
 	for i=1,#bodypartz do
@@ -317,7 +66,7 @@
 		armvel = -0.9
 		local bmi, bma = GetBodyBounds(RRARM)
       	local bc = VecLerp(bmi, bma, 0.5)
-      	local ppos = VecSub(GetPlayerCameraTransform().pos, Vec(0,1,0))
+      	local ppos = VecSub(GetPlayerCameraTransform(playerId).pos, Vec(0,1,0))
       	local dir = VecSub(bc, ppos)
       	local dist = VecLength(dir)
       	dir = VecScale(dir, 1.0 / dist)
@@ -392,7 +141,6 @@
 	--recoilTimer = shotDelay
 	--lightTimer = shotDelay/2
 
-
 	--if spentcasingsoption then
 	--	SpentCasing()
 	--end
@@ -405,18 +153,18 @@
 	local hit, dist, normal, shape = QueryRaycast(projectile.pos, dir, VecLength(VecSub(point2, projectile.pos)))
 	
 
-	local P = VecSub(VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0)), projectile.pos)
+	local P = VecSub(VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0)), projectile.pos)
 	local T = VecSub(point2, projectile.pos)
 	local N = VecScale(VecNormalize(T), VecDot(VecNormalize(T), P))
 	local R = VecSub(P, N)
 
 	if VecLength(R) < 0.7 and projectile.momentum ~= 0 then
-		SetPlayerHealth(GetPlayerHealth()-damage)
+		SetPlayerHealth(playerId, GetPlayerHealth(playerId)-damage)
 		projectile.momentum = 0
 	end
 
 	if disttoplayer > 4 and bulletsshot > oldbulletsshot then
-	PlaySound(LoadSound("MOD/snd/"..GetTagValue(barrel, "gun").."dist.ogg"), GetPlayerTransform().pos, disttoplayer/10)
+	PlaySound(LoadSound("MOD/snd/"..GetTagValue(barrel, "gun").."dist.ogg"), GetPlayerTransform(playerId).pos, disttoplayer/10)
 	oldbulletsshot = bulletsshot
 	end
 	if rpg then
@@ -566,17 +314,251 @@
 	end
 end
 
-function draw()
-	if not canSeePlayer then
-	 UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("J = begin ragdoll agression")
-      UiTranslate(0, 50)
-      UiText("All ragdolls near a radio")
-      UiTranslate(0, 50)
-      UiText("will become agressive by themselves")
-    UiPop()
-end
-end+function server.init()
+    ShoulderJoints = FindJoints("shoulder")
+    ArmJoints = FindJoints("hand1")
+    Eyes = FindBody("Head")
+    Torso = FindBody("Torso")
+    RRARM = FindBody("LLARM")
+    HipJoints = FindJoints("hip")
+    KneeJoints = FindJoints("knee")
+    walktim = 0
+    speed = 0.07
+    shootTimer = 0
+    shotDelay = 0.09
+    damage = 0.15
+    gravity = Vec(0, -40, 0)
+    velocity = 300 --tonumber(GetTagValue(barrel, "bulletspeed"))
+    maxMomentum = 6
+    ShootTimMax = 0.5
+    --GetTagValue(barrel,"gun")
+    --shoot = LoadSound("MOD/snd/".."makarov"..".ogg")
+    BulletsShot = 0
+    oldbulletsshot = 0
+    bulletsshot = 1
+    reloading = false
+    reloadtim = 0
+    maxreloadtim = 3
+    barrel = FindShape("barrel")
+    MagSize = tonumber(GetTagValue(barrel, "magsize"))
+    maxrange = tonumber(GetTagValue(barrel, "range"))/2
+    damage = tonumber(GetTagValue(barrel, "damage"))
+    firerate = tonumber(GetTagValue(barrel, "firerate"))
+    ShootTimer = math.random(1,firerate*100)/100
+    Fucked = false
+    Torso = FindBody("Torso")
+    Head = FindBody("Head")
+    canSeePlayer = false
+    if GetTagValue(barrel, "team") == "friend" then
+    	SetTag(Torso, "friend")
+    	SetTag(Head, "friendhead")
+    	team = 1
+    end
+    if GetTagValue(barrel, "team") == "enemy"then
+    	SetTag(Torso, "enemy")
+    	SetTag(Head, "enemyhead")
+    	SetTag(Torso, "shooting_target")
+    	team = 2
+    end
+    for i=1, 150 do
+    	ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    end
+    if HasTag(barrel, "rpg") then
+    	rpg = true
+    	gravity = Vec(0, -2, 0)
+    	velocity = 70
+    end
+    if HasTag(barrel, "stationary") then
+    	nowalk = true
+    end
+    DrawTeam = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(ak47projectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        	Radios = FindShapes("Spawn",true)
+        	--DebugPrint("Radios: "..#Radios)
+        	for i=1,#Radios do
+        		Radio = Radios[i]
+        		DistToRadio = VecLength(VecSub(GetShapeWorldTransform(Radio).pos, GetBodyTransform(Torso).pos))
+        		if DistToRadio < 5 then
+        			canSeePlayer = true
+        		end
+        	end
+        	if Fucked then
+        		RemoveTag(Torso, "friend")
+        		RemoveTag(Torso, "enemy")
+        		RemoveTag(Head, "friendhead")
+        		RemoveTag(Head, "enemyhead")
+        		RemoveTag(Torso, "shooting_target")
+        	end
+        	if DrawTeam then
+        	if GetTagValue(barrel, "team") == "friend" and not Fucked then
+        		TT = GetBodyTransform(Torso)
+        		DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 1,0,0)
+        	end
+        	if GetTagValue(barrel, "team") == "enemy" and not Fucked then
+        		TT = GetBodyTransform(Torso)
+        		DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 0,0,1)
+        	end
+        	if Fucked then
+        		TT = GetBodyTransform(Torso)
+        		--DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 2, TT.pos[3]), 0.5,0.5,0.5)
+        	end
+        	end
+        	if HasTag(Torso, "dead") or HasTag(Torso, "panicked") then
+        		Fucked = true
+        	end
+        	-- LOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOOOLOLOLOLOLOL
+        	if team == 1 then
+        		enemies = FindBodies("enemy",true)
+        		enemieshead = FindBodies("enemyhead",true)
+        	end
+        	if team == 2 then
+        		enemies = FindBodies("friend",true)
+        		enemieshead = FindBodies("friendhead",true)
+        	end
+        	for k=1,#enemies do
+        		E = enemies[k]
+        		H = enemieshead[k]
+        		disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, GetBodyTransform(E).pos))
+        		if disttoenemy < 155 then
+        			enemyhead = GetBodyTransform(H)
+        			enemy = GetBodyTransform(E)
+        			for i=1,#enemies do
+        				Secondaryenemytrans = GetBodyTransform(enemies[i])
+        				disttosecondary = VecLength(VecSub(Secondaryenemytrans.pos, GetBodyTransform(Torso).pos))
+        				disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, enemy.pos))
+        				Player = GetPlayerTransform(playerId)
+        				disttoplayerz = VecLength(VecSub(GetBodyTransform(Torso).pos, Player.pos))
+        				if disttosecondary < disttoenemy then
+        					enemy = Secondaryenemytrans
+        					--DebugCross(enemy)
+        				end
+        				if disttoplayerz < disttosecondary and team == 1 then
+        					Player.pos[2] = Player.pos[2] + 1
+        					enemy = Player
+        					--DebugCross(enemy)
+        				end
+        				if disttoplayerz < disttoenemy and team == 1 then
+        					Player.pos[2] = Player.pos[2] + 1
+        					enemy = Player
+        					--DebugCross(enemy)
+        				end
+        			end
+        		end
+        	end
+        	if #enemies == 0 and team == 1 then
+        		Player = GetPlayerTransform(playerId)
+        		disttoplayerz = VecLength(VecSub(GetBodyTransform(Torso).pos, Player.pos))
+        		if disttoplayerz < 155 then
+        			Player.pos[2] = Player.pos[2] + 1
+        			enemy = Player
+
+        		end
+        	end
+        	--DebugPrint(canSeePlayer())
+        	if #enemies > 0 or DoPlayer then
+        	gunTrans = GetBodyTransform(Eyes)
+        	gunPos = gunTrans.pos
+        	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
+        	shootPos = VecAdd(gunPos, VecScale(direction,0.2))
+        	disttoplayer = VecLength(VecSub(enemy.pos, gunTrans.pos))
+        	if reloading then
+        		--DebugPrint(reloadtim)
+        		reloadtim = reloadtim + dt
+        		if reloadtim > maxreloadtim then
+        			reloading = false
+        			reloadtim = 0
+        			BulletsShot = 0
+        			bulletsshot = 0
+        		end
+        	end
+        	end
+        	ShootTimer = ShootTimer + dt
+        	Player = GetPlayerTransform(playerId)
+        	disttoplayerz = VecLength(VecSub(GetBodyTransform(Torso).pos, Player.pos))
+        	if disttoplayerz < 155 and team == 1 and #enemies < 1 then
+        		DoPlayer = true
+        	else
+        		DoPlayer = false
+        	end
+        	if #enemies > 0 or DoPlayer then
+        	if not Fucked then
+        	faceplayer()
+        	end
+        	end
+        	if #enemies > 0 or DoPlayer then
+        	if canSeePlayer and not Fucked then
+        		agro = true
+        		aimweapon()
+        		runtoenemy()
+        		if disttoplayer > maxrange then
+        		run = true
+        	else
+        		run = false
+        		agro = false
+        	end
+        	end
+        	end
+        	if #enemies > 0 or DoPlayer then
+        	if canSeePlayer and ShootTimer > firerate and not reloading and not Fucked then
+        		if not run then
+        		Shoot()
+        		BulletsShot = BulletsShot + 1
+        		bulletsshot = bulletsshot + 1
+        		if BulletsShot == MagSize or bulletsshot > MagSize then
+        			reloading = true
+        		end
+        		ShootTimer = 0
+        	end
+        end
+        	end
+    end
+end
+
+function client.init()
+    shoot = LoadSound("MOD/snd/"..GetTagValue(barrel, "gun")..".ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("J") then
+    	canSeePlayer = true
+    end
+    if InputPressed("L") then
+    	optimizedead()
+    end
+    if InputPressed("M") then
+    	optimize()
+    end
+    if InputPressed("H") then
+    	DrawTeam = false
+    end
+end
+
+function client.draw()
+    	if not canSeePlayer then
+    	 UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("J = begin ragdoll agression")
+          UiTranslate(0, 50)
+          UiText("All ragdolls near a radio")
+          UiTranslate(0, 50)
+          UiText("will become agressive by themselves")
+        UiPop()
+    end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\GoreAiSpawnables.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\GoreAiSpawnables.lua
+++ patched/main\Gore Ragdolls 2\scripts\GoreAiSpawnables.lua
@@ -1,208 +1,6 @@
-ak47projectileHandler = {
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
-
-
-function init()
-	ShoulderJoints = FindJoints("shoulder")
-	ArmJoints = FindJoints("hand1")
-	Eyes = FindBody("Head")
-	Torso = FindBody("Torso")
-	RRARM = FindBody("LLARM")
-	HipJoints = FindJoints("hip")
-	KneeJoints = FindJoints("knee")
-	walktim = 0
-	speed = 0.07
-
-	ShootTimer = 0
-	shootTimer = 0
-	shotDelay = 0.09
-	damage = 0.15
-	gravity = Vec(0, -40, 0)
-	velocity = 300 --tonumber(GetTagValue(barrel, "bulletspeed"))
-	maxMomentum = 6
-	ShootTimMax = 0.5
-	--GetTagValue(barrel,"gun")
-	--shoot = LoadSound("MOD/snd/".."makarov"..".ogg")
-	shoot = LoadSound("MOD/snd/"..GetTagValue(barrel, "gun")..".ogg")
-	BulletsShot = 0
-	oldbulletsshot = 0
-	bulletsshot = 1
-	reloading = false
-	reloadtim = 0
-	maxreloadtim = 3
-	barrel = FindShape("barrel")
-	MagSize = tonumber(GetTagValue(barrel, "magsize"))
-	maxrange = tonumber(GetTagValue(barrel, "range"))/15
-	damage = tonumber(GetTagValue(barrel, "damage"))
-	firerate = tonumber(GetTagValue(barrel, "firerate"))
-	Fucked = false
-	Torso = FindBody("Torso")
-	Head = FindBody("Head")
-	canSeePlayer = false
-	if GetTagValue(barrel, "team") == "friend" then
-		SetTag(Torso, "friend")
-		SetTag(Head, "friendhead")
-		team = 1
-	end
-	if GetTagValue(barrel, "team") == "enemy"then
-		SetTag(Torso, "enemy")
-		SetTag(Head, "enemyhead")
-		SetTag(Torso, "shooting_target")
-		team = 2
-	end
-	for i=1, 150 do
-		ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
-	end
-	if HasTag(barrel, "rpg") then
-		rpg = true
-		gravity = Vec(0, -2, 0)
-		velocity = 70
-	end
-	if HasTag(barrel, "stationary") then
-		nowalk = true
-	end
-	DrawTeam = true
-end
-function update(dt)
-	if InputPressed("J") then
-		canSeePlayer = true
-	end
-	if InputPressed("L") then
-		optimizedead()
-	end
-	if InputPressed("M") then
-		optimize()
-	end
-	if Fucked then
-		RemoveTag(Torso, "friend")
-		RemoveTag(Torso, "enemy")
-		RemoveTag(Head, "friendhead")
-		RemoveTag(Head, "enemyhead")
-		RemoveTag(Torso, "shooting_target")
-	end
-	if InputPressed("H") then
-		DrawTeam = false
-	end
-	if DrawTeam then
-	if GetTagValue(barrel, "team") == "friend" and not Fucked then
-		TT = GetBodyTransform(Torso)
-		DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 1,0,0)
-	end
-	if GetTagValue(barrel, "team") == "enemy" and not Fucked then
-		TT = GetBodyTransform(Torso)
-		DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 0,0,1)
-	end
-	if Fucked then
-		TT = GetBodyTransform(Torso)
-		--DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 2, TT.pos[3]), 0.5,0.5,0.5)
-	end
-	end
-
-	if HasTag(Torso, "dead") or HasTag(Torso, "panicked") then
-		Fucked = true
-	end
-	-- LOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOOOLOLOLOLOLOL
-	if team == 1 then
-		enemies = FindBodies("enemy",true)
-		enemieshead = FindBodies("enemyhead",true)
-	end
-	if team == 2 then
-		enemies = FindBodies("friend",true)
-		enemieshead = FindBodies("friendhead",true)
-	end
-
-	for k=1,#enemies do
-		E = enemies[k]
-		H = enemieshead[k]
-		disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, GetBodyTransform(E).pos))
-		if disttoenemy < 155 then
-			enemyhead = GetBodyTransform(H)
-			enemy = GetBodyTransform(E)
-			for i=1,#enemies do
-				Secondaryenemytrans = GetBodyTransform(enemies[i])
-				disttosecondary = VecLength(VecSub(Secondaryenemytrans.pos, GetBodyTransform(Torso).pos))
-				disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, enemy.pos))
-				if disttosecondary < disttoenemy then
-					enemy = Secondaryenemytrans
-					--DebugCross(enemy)
-				end
-			end
-		end
-	end
-	--DebugPrint(canSeePlayer())
-	if #enemies > 0 then
-	gunTrans = GetBodyTransform(Eyes)
-	gunPos = gunTrans.pos
-	direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
-	shootPos = VecAdd(gunPos, VecScale(direction,0.2))
-	disttoplayer = VecLength(VecSub(enemy.pos, gunTrans.pos))
-	if reloading then
-		reloadtim = reloadtim + dt
-		if reloadtim > maxreloadtim then
-			reloading = false
-			reloadtim = 0
-			BulletsShot = 0
-		end
-	end
-	end
-
-	ShootTimer = ShootTimer + dt
-	if not Fucked and #enemies > 0 then
-	faceplayer()
-	end
-	if canSeePlayer and ShootTimer > firerate and not reloading and not Fucked and #enemies > 0 then
-		if not run then
-		Shoot()
-		BulletsShot = BulletsShot + 1
-		bulletsshot = bulletsshot + 1
-		if BulletsShot == MagSize then
-			reloading = true
-		end
-		ShootTimer = 0
-	end
-	end
-
-	if canSeePlayer and not Fucked and #enemies > 0 then
-		agro = true
-		aimweapon()
-		runtoenemy()
-		if disttoplayer > maxrange then
-		run = true
-	else
-		run = false
-		agro = false
-	end
-	end
-end
-
-function tick()
-	for key, shell in ipairs(ak47projectileHandler.shells) do
-		if shell.active then
-			ProjectileOperations(shell)
-		end
-	end
-    end
-
+#version 2
 function canSeePlayer()
-    local camTrans = GetPlayerCameraTransform()
+    local camTrans = GetPlayerCameraTransform(playerId)
 	local playerPos = camTrans.pos
 
 	--Direction to player
@@ -210,7 +8,7 @@
 	local dist = VecLength(dir)
 	dir = VecNormalize(dir)
 
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	rejectragdoll()
 	bodypartz = FindBodies("bodypart",true)
 	for i=1,#bodypartz do
@@ -268,7 +66,7 @@
 		armvel = -0.9
 		local bmi, bma = GetBodyBounds(RRARM)
       	local bc = VecLerp(bmi, bma, 0.5)
-      	local ppos = VecSub(GetPlayerCameraTransform().pos, Vec(0,1,0))
+      	local ppos = VecSub(GetPlayerCameraTransform(playerId).pos, Vec(0,1,0))
       	local dir = VecSub(bc, ppos)
       	local dist = VecLength(dir)
       	dir = VecScale(dir, 1.0 / dist)
@@ -343,7 +141,6 @@
 	--recoilTimer = shotDelay
 	--lightTimer = shotDelay/2
 
-
 	--if spentcasingsoption then
 	--	SpentCasing()
 	--end
@@ -356,18 +153,18 @@
 	local hit, dist, normal, shape = QueryRaycast(projectile.pos, dir, VecLength(VecSub(point2, projectile.pos)))
 	
 
-	local P = VecSub(VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0)), projectile.pos)
+	local P = VecSub(VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0)), projectile.pos)
 	local T = VecSub(point2, projectile.pos)
 	local N = VecScale(VecNormalize(T), VecDot(VecNormalize(T), P))
 	local R = VecSub(P, N)
 
 	if VecLength(R) < 0.7 and projectile.momentum ~= 0 then
-		SetPlayerHealth(GetPlayerHealth()-damage)
+		SetPlayerHealth(playerId, GetPlayerHealth(playerId)-damage)
 		projectile.momentum = 0
 	end
 
 	if disttoplayer > 4 and bulletsshot > oldbulletsshot then
-	PlaySound(LoadSound("MOD/snd/"..GetTagValue(barrel, "gun").."dist.ogg"), GetPlayerTransform().pos, disttoplayer/10)
+	PlaySound(LoadSound("MOD/snd/"..GetTagValue(barrel, "gun").."dist.ogg"), GetPlayerTransform(playerId).pos, disttoplayer/10)
 	oldbulletsshot = bulletsshot
 	end
 	if rpg then
@@ -509,17 +306,206 @@
 	end
 end
 
-function draw()
-	if not canSeePlayer then
-	 UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("J = begin ragdoll agression")
-      UiTranslate(0, 50)
-      UiText("All ragdolls near a radio")
-      UiTranslate(0, 50)
-      UiText("will become agressive by themselves")
-    UiPop()
-end
-end+function server.init()
+    ShoulderJoints = FindJoints("shoulder")
+    ArmJoints = FindJoints("hand1")
+    Eyes = FindBody("Head")
+    Torso = FindBody("Torso")
+    RRARM = FindBody("LLARM")
+    HipJoints = FindJoints("hip")
+    KneeJoints = FindJoints("knee")
+    walktim = 0
+    speed = 0.07
+    ShootTimer = 0
+    shootTimer = 0
+    shotDelay = 0.09
+    damage = 0.15
+    gravity = Vec(0, -40, 0)
+    velocity = 300 --tonumber(GetTagValue(barrel, "bulletspeed"))
+    maxMomentum = 6
+    ShootTimMax = 0.5
+    --GetTagValue(barrel,"gun")
+    --shoot = LoadSound("MOD/snd/".."makarov"..".ogg")
+    BulletsShot = 0
+    oldbulletsshot = 0
+    bulletsshot = 1
+    reloading = false
+    reloadtim = 0
+    maxreloadtim = 3
+    barrel = FindShape("barrel")
+    MagSize = tonumber(GetTagValue(barrel, "magsize"))
+    maxrange = tonumber(GetTagValue(barrel, "range"))/15
+    damage = tonumber(GetTagValue(barrel, "damage"))
+    firerate = tonumber(GetTagValue(barrel, "firerate"))
+    Fucked = false
+    Torso = FindBody("Torso")
+    Head = FindBody("Head")
+    canSeePlayer = false
+    if GetTagValue(barrel, "team") == "friend" then
+    	SetTag(Torso, "friend")
+    	SetTag(Head, "friendhead")
+    	team = 1
+    end
+    if GetTagValue(barrel, "team") == "enemy"then
+    	SetTag(Torso, "enemy")
+    	SetTag(Head, "enemyhead")
+    	SetTag(Torso, "shooting_target")
+    	team = 2
+    end
+    for i=1, 150 do
+    	ak47projectileHandler.shells[i] = deepcopy(ak47projectileHandler.defaultShell)
+    end
+    if HasTag(barrel, "rpg") then
+    	rpg = true
+    	gravity = Vec(0, -2, 0)
+    	velocity = 70
+    end
+    if HasTag(barrel, "stationary") then
+    	nowalk = true
+    end
+    DrawTeam = true
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for key, shell in ipairs(ak47projectileHandler.shells) do
+        	if shell.active then
+        		ProjectileOperations(shell)
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if Fucked then
+        	RemoveTag(Torso, "friend")
+        	RemoveTag(Torso, "enemy")
+        	RemoveTag(Head, "friendhead")
+        	RemoveTag(Head, "enemyhead")
+        	RemoveTag(Torso, "shooting_target")
+        end
+        if DrawTeam then
+        if GetTagValue(barrel, "team") == "friend" and not Fucked then
+        	TT = GetBodyTransform(Torso)
+        	DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 1,0,0)
+        end
+        if GetTagValue(barrel, "team") == "enemy" and not Fucked then
+        	TT = GetBodyTransform(Torso)
+        	DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 3, TT.pos[3]), 0,0,1)
+        end
+        if Fucked then
+        	TT = GetBodyTransform(Torso)
+        	--DrawLine(Vec(TT.pos[1], TT.pos[2] + 2.9, TT.pos[3]), Vec(TT.pos[1], TT.pos[2] + 2, TT.pos[3]), 0.5,0.5,0.5)
+        end
+        end
+        if HasTag(Torso, "dead") or HasTag(Torso, "panicked") then
+        	Fucked = true
+        end
+        -- LOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOOOLOLOLOLOLOL
+        if team == 1 then
+        	enemies = FindBodies("enemy",true)
+        	enemieshead = FindBodies("enemyhead",true)
+        end
+        if team == 2 then
+        	enemies = FindBodies("friend",true)
+        	enemieshead = FindBodies("friendhead",true)
+        end
+        for k=1,#enemies do
+        	E = enemies[k]
+        	H = enemieshead[k]
+        	disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, GetBodyTransform(E).pos))
+        	if disttoenemy < 155 then
+        		enemyhead = GetBodyTransform(H)
+        		enemy = GetBodyTransform(E)
+        		for i=1,#enemies do
+        			Secondaryenemytrans = GetBodyTransform(enemies[i])
+        			disttosecondary = VecLength(VecSub(Secondaryenemytrans.pos, GetBodyTransform(Torso).pos))
+        			disttoenemy = VecLength(VecSub(GetBodyTransform(Torso).pos, enemy.pos))
+        			if disttosecondary < disttoenemy then
+        				enemy = Secondaryenemytrans
+        				--DebugCross(enemy)
+        			end
+        		end
+        	end
+        end
+        --DebugPrint(canSeePlayer())
+        if #enemies ~= 0 then
+        gunTrans = GetBodyTransform(Eyes)
+        gunPos = gunTrans.pos
+        direction = TransformToParentVec(gunTrans, Vec(0, -1, 0))
+        shootPos = VecAdd(gunPos, VecScale(direction,0.2))
+        disttoplayer = VecLength(VecSub(enemy.pos, gunTrans.pos))
+        if reloading then
+        	reloadtim = reloadtim + dt
+        	if reloadtim > maxreloadtim then
+        		reloading = false
+        		reloadtim = 0
+        		BulletsShot = 0
+        	end
+        end
+        end
+        ShootTimer = ShootTimer + dt
+        if not Fucked and #enemies ~= 0 then
+        faceplayer()
+        end
+        if canSeePlayer and ShootTimer > firerate and not reloading and not Fucked and #enemies ~= 0 then
+        	if not run then
+        	Shoot()
+        	BulletsShot = BulletsShot + 1
+        	bulletsshot = bulletsshot + 1
+        	if BulletsShot == MagSize then
+        		reloading = true
+        	end
+        	ShootTimer = 0
+        end
+        end
+        if canSeePlayer and not Fucked and #enemies ~= 0 then
+        	agro = true
+        	aimweapon()
+        	runtoenemy()
+        	if disttoplayer > maxrange then
+        	run = true
+        else
+        	run = false
+        	agro = false
+        end
+        end
+    end
+end
+
+function client.init()
+    shoot = LoadSound("MOD/snd/"..GetTagValue(barrel, "gun")..".ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("J") then
+    	canSeePlayer = true
+    end
+    if InputPressed("L") then
+    	optimizedead()
+    end
+    if InputPressed("M") then
+    	optimize()
+    end
+    if InputPressed("H") then
+    	DrawTeam = false
+    end
+end
+
+function client.draw()
+    	if not canSeePlayer then
+    	 UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("J = begin ragdoll agression")
+          UiTranslate(0, 50)
+          UiText("All ragdolls near a radio")
+          UiTranslate(0, 50)
+          UiText("will become agressive by themselves")
+        UiPop()
+    end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\gorefunctions.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\gorefunctions.lua
+++ patched/main\Gore Ragdolls 2\scripts\gorefunctions.lua
@@ -1,407 +1,4 @@
-#include "UiHealthOverlay.lua"
-
-function init()	
-	MyHealthUiIsActive = false
-	RagdollBody = {}
-
-	sbloodval = {};
-	bloodval = {};
-	currentbloodvalue = {};
-	Puddles = {};
-	
-	Torso = FindBody("Torso")
-	
-	bodyparts = FindBodies("bodypart")
-	starttotalbloodvalue = 0
-	for i=1,#bodyparts do		
-			bodypart = bodyparts[i]
-			bodypartshapes = GetBodyShapes(bodypart)
-			--DebugPrint(#bodypartshapes)
-			for h=1,#bodypartshapes do
-			SetTag(bodypartshapes[h], "fxbreak","l3red")
-			--DebugPrint("Set")
-			end
-
-		RagdollBody[bodypart] = 1
-		bodypartstartmass = GetBodyMass(bodypart)
-		table.insert(sbloodval, bodypartstartmass)
-		table.insert(bloodval, bodypartstartmass)
-		table.insert(currentbloodvalue, bodypartstartmass)
-		--table.insert(puddles, {pos={x,y,z}, amount=3.0})
-		starttotalbloodvalue = starttotalbloodvalue + GetBodyMass(bodypart)
-	end
-	bleed = 0
-	puddleregtim = 0
-	repuddle = 0.5
-	mergepuddledistance = 1
-	puddleneutspeed = 0.2
-	GrowSpeed = 0.003
-	Puddlemaxsize = 1
-	upspeed = 50
-	headvel = Vec(0,GetBodyMass(FindBody("RRLEG"))/upspeed,0)
-	--DebugPrint("HeadMass: "..headvel)
-	legvel = Vec(0,-GetBodyMass(FindBody("LLLEG"))/20,0)
-	recoverfromtrip = 3
-	triptim = 0
-	tripped = false
-	restartjoints = false
-	trippingspeed = 10
-	jointstrength = 10	
-	sretractjoint = 12
-	retractjoint = sretractjoint
-	retractjoint1 = sretractjoint
-	retractjoint2 = sretractjoint
-	retractjoint3 = sretractjoint
-	retractjoint4 = sretractjoint
-	retractjoint5 = sretractjoint
-	panictim = 0
-	actualpanictim = 0
-	criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
-	goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
-	headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
-	drowntim = 0
-	inpostim = 0
-	deadtim = 0
-	
-	SetHeadHealth(RED)
-	AddHeadHealthEffect("argh",RED)
-	UI = FindLocations("UIISADDED", true)
-	--if UI == nil then
-		Spawn("MOD/prefab/UISPAWN.xml", Vec(0,0,0))
-		Spawn("MOD/prefab/GoreFX.xml", Vec(0,0,0))
-	--end
-	manualdietim = 0
-	gorelevel = GetInt("savegame.mod.gore")
-	bleedbool = GetBool("savegame.mod.bleed")
-	if gorelevel == 4 then
-		multiplier = 2
-	else
-		multiplier = 1
-	end
-	--DebugPrint(gorelevel)
-	keytokill = GetString("savegame.mod.gore_kill")
-end
-
-function tick()
-	CheckHealthUi()
-end
-
-function draw(dt)
-	DrawUiHealthOverlay(dt)
-	if warn then
-	UiPush()
-      UiAlign("center middle")
-      --UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiColor(1,0,0)
-      UiText("PRESS"..keytokill.." AGAIN TO KILL ALL RAGDOLLS: "..10 - manualdietim)
-     UiPop()
- end
-end
-
-function update(dt)
-	if manualdietim < 10 then
-		if InputPressed(keytokill) and warn then
-		entirelystop = true
-		warn = false
-		manualdietim = 0
-		end
-	else
-		warn = false
-		manualdietim = 0
-	end
-	if InputPressed(keytokill) and not warn and not entirelystop then
-		warn = true
-	end
-	if warn then
-		manualdietim = manualdietim + dt
-	end
-if not entirelystop then
-	if not tripped and not sitting then
-		knees = FindJoints("knee")
-		for i=1,#knees do
-			panick()
-			--if not IsJointBroken(hips[i]) then
-				SetJointMotor(knees[i], -retractjoint3/4,jointstrength)
-			--end
-		end
-	end
-
-	jaw = FindShape("jaw")
-	if not dead then
-		jaw = FindShape("jaw")
-		evtelse = FindShapes("")
-		SetShapeCollisionFilter(jaw, 2, 255-2)
-		torsos = GetBodyShapes(FindBody("Torso"))
-		for i=1,#torsos do
-		SetShapeCollisionFilter(torsos[i], 2, 255-2)
-		end
-		jawjoints = GetShapeJoints(jaw)
-		for i=1,#jawjoints do
-			SetJointMotor(jawjoints[i], 0.5)
-		end
-	else
-		jawjoints = GetShapeJoints(jaw)
-		for i=1,#jawjoints do
-			SetJointMotor(jawjoints[i], 0, 0)
-		end
-	end
-	if panic then
-		SetTag(Torso, "panicked")
-		panictim = panictim + dt
-		actualpanictim = actualpanictim + dt
-	end
-	bodyparts = FindBodies("bodypart")
-	totalbloodvalue = 0
-	if tripped then
-		cower()
-		triptim = triptim + dt
-		if triptim > recoverfromtrip and VecLength(GetBodyVelocity(FindBody("Torso"))) < trippingspeed then
-			tripped = false
-			triptim = 0
-		end
-	end
-	for i=1,#bodyparts do
-		bodypart = bodyparts[i]
-		SetTag(bodypart, "nocull")
-		bodypartcurrentmass = GetBodyMass(bodypart)
-		bloodval[i] = bodypartcurrentmass
-		bodyparttransform = GetBodyTransform(bodypart)
-		--DebugPrint(bloodval[i])
-		bleedintensity = ((bloodval[i]/sbloodval[i]) - 1) * -10
-		--DebugPrint(currentbloodvalue[i])
-		currentbloodvalue[i] = currentbloodvalue[i] - bleedintensity/75
-		totalbloodvalue = totalbloodvalue + currentbloodvalue[i]
-		if HasTag(bodypart, "Torso") then
-			torsovelocity = VecLength(GetBodyVelocity(bodypart))
-			if torsovelocity > trippingspeed then
-				tripped = true
-			end
-		end
-
-		if sitting then
-			sit()
-		end
-
-		if HasTag(bodypart,"Torso") then
-			if HasTag(bodypart, "sit") then
-				sitting = true
-			end
-				bodypartpos = GetBodyTransform(bodypart)
-				disttobodypart = VecLength(VecSub(GetAimPossit(), bodypartpos.pos))
-				cycled = true
-				if InputPressed("P") and cycled and not sitting then
-				if disttobodypart < 3 then
-					sitting = true
-					cycled = false
-				end
-				end
-
-				if InputPressed("P") and cycled and sitting then
-				if disttobodypart < 3 then
-					sitting = false
-					cycled = false
-					restartjointsfunc()
-					inposition = false
-				end
-				end
-		end
-
-		if HasTag(bodypart, "Head") then
-			if IsPointInWater(bodyparttransform.pos) then
-				tripped = true
-				drowntim = drowntim + dt
-			end
-		end
-
-		if drowntim > 5 then
-			dead = true
-		end
-
-		if not tripped and HasTag(bodypart, "Head") and not dead and not sitting then
-				--Paint(GetAimPos(), (bleedintensity/sbloodval[i])*1.3, "explosion")
-				currentvel = GetBodyVelocity(bodypart)
-				SetBodyVelocity(bodypart, VecAdd(currentvel, headvel))
-				--DebugPrint(VecAdd(currentvel, headvel)[2])
-				if IsBodyBroken(bodypart) then
-					bodyState.head = BROKEN_BODY_PART	
-					bodyState.overall = "dead"					
-					dead = true
-					if bloodval[i] < sbloodval[i] - sbloodval[i] / 4 then
-					bods = GetBodyShapes(bodypart)
-					for i = 1,#bods do
-						j = GetShapeJoints(bods[i])
-						for z = 1,#j do
-							Delete(j[i])
-						end
-					end
-				end
-				end
-		end
-
-		if not tripped and HasTag(bodypart, "RRLEG") or HasTag(bodypart, "LLLEG") then
-			if not dead and not sitting and not tripped then
-				--Paint(GetAimPos(), (bleedintensity/sbloodval[i])*1.3, "explosion")
-				currentvel = GetBodyVelocity(bodypart)
-				SetBodyVelocity(bodypart, VecAdd(currentvel, legvel))
-			end
-		end
-
-		if IsBodyBroken(bodypart) then
-
-			if HasTag(bodypart, "Head") then
-				dead = true
-			end
-
-			if bloodval[i] < sbloodval[i] - sbloodval[i]/10 then
-				panic = true
-				tripped = true
-			end
-		end
-
-		if IsBodyBroken(bodypart) and currentbloodvalue[i] > 0 then
-			if bodyState.overall == "healthy" then bodyState.overall = "injured" end
-			
-			if HasTag(bodypart, "LLLEG") or HasTag(bodypart, "LLEG") then
-				bodyState.leftLeg = BROKEN_BODY_PART			
-				if not diddit1 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
-					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
-					diddit1 = true
-				end
-			elseif HasTag(bodypart, "RRLEG") or HasTag(bodypart, "RLEG") then
-				bodyState.rightLeg = BROKEN_BODY_PART					
-				if not diddit2 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
-					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
-					diddit2 = true
-				end
-			elseif HasTag(bodypart, "RRARM") or HasTag(bodypart, "RARM") then
-				bodyState.rightArm = BROKEN_BODY_PART	
-				if not diddit3 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
-					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
-					diddit3 = true
-				end				
-			elseif HasTag(bodypart, "LLARM") or HasTag(bodypart, "LARM") then
-				bodyState.leftArm = BROKEN_BODY_PART	
-				if not diddit4 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
-					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
-					diddit4 = true
-				end							
-			end
-		
-		
-			--Paint(GetAimPos(), bleedintensity/sbloodval[i], "explosion")
-
-			puddleregtim = puddleregtim + dt
-
-			PuddleHandleing()
-			if puddleregtim > repuddle then
-			--for i=1,bleedintensity/10 do
-			--DebugPrint(bleedintensity)
-			InsertPuddleToTable()
-			bleedparticles()
-			if bleedbool then
-			--Paint(GetAimPos(), bleedintensity/sbloodval[i], "explosion")
-			end
-			--end
-			puddleregtim = 0
-			end
-			bleedparticles()
-
-			if bloodval[i] < 0.5 then ---------------------------------------------------------------
-			bleedintensity = 1000
-				for i=1,12 do
-					InsertPuddleToTable()
-				end
-				currentbloodvalue[i] = 0
-			end
-
-			if HasTag(bodypart, "Torso") and bloodval[i] < sbloodval[i]/1.2 then			
-				--DebugPrint("SUPPOSED TO BE LOL GUTTED XD")
-				if not entrailed then
-					bodyState.body = BROKEN_BODY_PART
-					bodyState.overall = "dead"
-					dead = true
-					entrailed = true
-					for i=1,4 do
-						InsertPuddleToTable()
-					end
-
-					PlaySound(goresplat, GetBodyTransform(Torso).pos, 1)
-
-					if gorelevel ~= 1 then
-					Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", bodyparttransform)
-					Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", bodyparttransform)
-					Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", bodyparttransform)
-					if gorelevel ~= 2 then
-					for i=1,2 do
-					Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", bodyparttransform)
-					end
-					for i=1,30 * multiplier do
-						Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", bodyparttransform)
-					end
-					end
-					end
-					--DebugPrint("LOL GUTTED XD")
-				end
-			end
-
-			if HasTag(bodypart, "Head") then
-				bodyState.head = BROKEN_BODY_PART	
-				bodyState.overall = "dead"	
-				eyej = FindJoints("eye")
-				if bloodval[i] < sbloodval[i] - sbloodval[i]/4 then
-				for i=1,#eyej do
-					Delete(eyej[i])
-				end
-				end
-				if bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
-				if not fragged then
-					fragged = true
-					PlaySound(headsplat, GetBodyTransform(Torso).pos, 1)
-					if gorelevel ~= 1 then
-					for i=1,4 do
-						InsertPuddleToTable()
-					end
-					Spawn("MOD/main/Gore Ragdolls 2/internals/Skull_Jaw.xml.xml", bodyparttransform)
-					for i=1,2 * multiplier do
-					Spawn("MOD/main/Gore Ragdolls 2/internals/Skull_Eye_Socket.xml", bodyparttransform)
-					Spawn("MOD/main/Gore Ragdolls 2/internals/Skull_Fragment.xml", bodyparttransform)
-					end
-					if gorelevel ~= 2 then
-					for i=1,10 * multiplier do
-						Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", bodyparttransform)
-					end
-				end
-					end
-					--DebugPrint("LOL GUTTED XD")
-				end
-				end
-			end
-		end
-	end
-	if IsJointBroken(FindJoint("neck")) or totalbloodvalue < starttotalbloodvalue - starttotalbloodvalue/1.5 then
-		bodyState.head = BROKEN_NECK						
-		bodyState.overall = "dead"	
-		dead = true
-	end
-	
-
-	if restartjoints and not tripped then
-		restartjointsfunc()
-	end
-
-	if dead then
-		SetTag(Torso, "dead")
-		restartjointsfunc()
-		deadtim = deadtim + dt
-		if deadtim > 10 then
-			entirelystop = true
-		end
-	end
-end
-
-end
-
+#version 2
 function GetAimPos()
      ct = bodyparttransform
     ctrot1, ctrot2, ctrot3 = GetQuatEuler(ct.rot)
@@ -592,8 +189,8 @@
 	end
 	end
 
-	function GetAimPossit()
-   local ct = GetPlayerCameraTransform()
+function GetAimPossit()
+   local ct = GetPlayerCameraTransform(playerId)
    local forwardPos = TransformToParentPoint(ct, Vec(0, 0, -200))
    local direction = VecSub(forwardPos, ct.pos)
    local distance = VecLength(direction)
@@ -652,12 +249,12 @@
 	if InputPressed("h") then 			
 		if lookingAtMe and not MyHealthUiIsActive then
 			MyHealthUiIsActive = true
-			SetInt("health.ui.active.body", Torso)
-			SetBool("health.ui.shown", true)
+			SetInt("health.ui.active.body", Torso, true)
+			SetBool("health.ui.shown", true, true)
 		else
 			MyHealthUiIsActive = false			
 			if GetInt("health.ui.active.body") == Torso then
-				SetBool("health.ui.shown", false)
+				SetBool("health.ui.shown", false, true)
 			end
 		end							
 	end	
@@ -671,7 +268,7 @@
 	end
 	
 	if MyHealthUiIsActive then
-		SetInt("health.ui.active.body", Torso)		
+		SetInt("health.ui.active.body", Torso, true)		
 		ShowUiHealthOverlay()	
 	else
 		HideUiHealthOverlay()	
@@ -680,4 +277,411 @@
 	if InputPressed("x") and MyHealthUiIsActive then
 		ToggleUiHealthDetailsOverlay()
 	end		
-end+end
+
+function server.init()
+    MyHealthUiIsActive = false
+    RagdollBody = {}
+    sbloodval = {};
+    bloodval = {};
+    currentbloodvalue = {};
+    Puddles = {};
+    Torso = FindBody("Torso")
+    bodyparts = FindBodies("bodypart")
+    starttotalbloodvalue = 0
+    for i=1,#bodyparts do		
+    		bodypart = bodyparts[i]
+    		bodypartshapes = GetBodyShapes(bodypart)
+    		--DebugPrint(#bodypartshapes)
+    		for h=1,#bodypartshapes do
+    		SetTag(bodypartshapes[h], "fxbreak","l3red")
+    		--DebugPrint("Set")
+    		end
+
+    	RagdollBody[bodypart] = 1
+    	bodypartstartmass = GetBodyMass(bodypart)
+    	table.insert(sbloodval, bodypartstartmass)
+    	table.insert(bloodval, bodypartstartmass)
+    	table.insert(currentbloodvalue, bodypartstartmass)
+    	--table.insert(puddles, {pos={x,y,z}, amount=3.0})
+    	starttotalbloodvalue = starttotalbloodvalue + GetBodyMass(bodypart)
+    end
+    bleed = 0
+    puddleregtim = 0
+    repuddle = 0.5
+    mergepuddledistance = 1
+    puddleneutspeed = 0.2
+    GrowSpeed = 0.003
+    Puddlemaxsize = 1
+    upspeed = 50
+    headvel = Vec(0,GetBodyMass(FindBody("RRLEG"))/upspeed,0)
+    --DebugPrint("HeadMass: "..headvel)
+    legvel = Vec(0,-GetBodyMass(FindBody("LLLEG"))/20,0)
+    recoverfromtrip = 3
+    triptim = 0
+    tripped = false
+    restartjoints = false
+    trippingspeed = 10
+    jointstrength = 10	
+    sretractjoint = 12
+    retractjoint = sretractjoint
+    retractjoint1 = sretractjoint
+    retractjoint2 = sretractjoint
+    retractjoint3 = sretractjoint
+    retractjoint4 = sretractjoint
+    retractjoint5 = sretractjoint
+    panictim = 0
+    actualpanictim = 0
+    criticalcough = LoadLoop("MOD/main/Gore Ragdolls 2/snd/criticalcondition.ogg")
+    drowntim = 0
+    inpostim = 0
+    deadtim = 0
+    SetHeadHealth(RED)
+    AddHeadHealthEffect("argh",RED)
+    UI = FindLocations("UIISADDED", true)
+    --if UI == nil then
+    	Spawn("MOD/prefab/UISPAWN.xml", Vec(0,0,0))
+    	Spawn("MOD/prefab/GoreFX.xml", Vec(0,0,0))
+    --end
+    manualdietim = 0
+    gorelevel = GetInt("savegame.mod.gore")
+    bleedbool = GetBool("savegame.mod.bleed")
+    if gorelevel == 4 then
+    	multiplier = 2
+    else
+    	multiplier = 1
+    end
+    --DebugPrint(gorelevel)
+    keytokill = GetString("savegame.mod.gore_kill")
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        CheckHealthUi()
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if warn then
+        	manualdietim = manualdietim + dt
+        end
+    end
+end
+
+function client.init()
+    goresplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/goresplat.ogg")
+    headsplat = LoadSound("MOD/main/Gore Ragdolls 2/snd/headsplat.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    	if manualdietim < 10 then
+    		if InputPressed(keytokill) and warn then
+    		entirelystop = true
+    		warn = false
+    		manualdietim = 0
+    		end
+    	else
+    		warn = false
+    		manualdietim = 0
+    	end
+    	if InputPressed(keytokill) and not warn and not entirelystop then
+    		warn = true
+    	end
+    if not entirelystop then
+    	if not tripped and not sitting then
+    		knees = FindJoints("knee")
+    		for i=1,#knees do
+    			panick()
+    			--if not IsJointBroken(hips[i]) then
+    				SetJointMotor(knees[i], -retractjoint3/4,jointstrength)
+    			--end
+    		end
+    	end
+
+    	jaw = FindShape("jaw")
+    	if not dead then
+    		jaw = FindShape("jaw")
+    		evtelse = FindShapes("")
+    		SetShapeCollisionFilter(jaw, 2, 255-2)
+    		torsos = GetBodyShapes(FindBody("Torso"))
+    		for i=1,#torsos do
+    		SetShapeCollisionFilter(torsos[i], 2, 255-2)
+    		end
+    		jawjoints = GetShapeJoints(jaw)
+    		for i=1,#jawjoints do
+    			SetJointMotor(jawjoints[i], 0.5)
+    		end
+    	else
+    		jawjoints = GetShapeJoints(jaw)
+    		for i=1,#jawjoints do
+    			SetJointMotor(jawjoints[i], 0, 0)
+    		end
+    	end
+    	if panic then
+    		SetTag(Torso, "panicked")
+    		panictim = panictim + dt
+    		actualpanictim = actualpanictim + dt
+    	end
+    	bodyparts = FindBodies("bodypart")
+    	totalbloodvalue = 0
+    	if tripped then
+    		cower()
+    		triptim = triptim + dt
+    		if triptim > recoverfromtrip and VecLength(GetBodyVelocity(FindBody("Torso"))) < trippingspeed then
+    			tripped = false
+    			triptim = 0
+    		end
+    	end
+    	for i=1,#bodyparts do
+    		bodypart = bodyparts[i]
+    		SetTag(bodypart, "nocull")
+    		bodypartcurrentmass = GetBodyMass(bodypart)
+    		bloodval[i] = bodypartcurrentmass
+    		bodyparttransform = GetBodyTransform(bodypart)
+    		--DebugPrint(bloodval[i])
+    		bleedintensity = ((bloodval[i]/sbloodval[i]) - 1) * -10
+    		--DebugPrint(currentbloodvalue[i])
+    		currentbloodvalue[i] = currentbloodvalue[i] - bleedintensity/75
+    		totalbloodvalue = totalbloodvalue + currentbloodvalue[i]
+    		if HasTag(bodypart, "Torso") then
+    			torsovelocity = VecLength(GetBodyVelocity(bodypart))
+    			if torsovelocity > trippingspeed then
+    				tripped = true
+    			end
+    		end
+
+    		if sitting then
+    			sit()
+    		end
+
+    		if HasTag(bodypart,"Torso") then
+    			if HasTag(bodypart, "sit") then
+    				sitting = true
+    			end
+    				bodypartpos = GetBodyTransform(bodypart)
+    				disttobodypart = VecLength(VecSub(GetAimPossit(), bodypartpos.pos))
+    				cycled = true
+    				if InputPressed("P") and cycled and not sitting then
+    				if disttobodypart < 3 then
+    					sitting = true
+    					cycled = false
+    				end
+    				end
+
+    				if InputPressed("P") and cycled and sitting then
+    				if disttobodypart < 3 then
+    					sitting = false
+    					cycled = false
+    					restartjointsfunc()
+    					inposition = false
+    				end
+    				end
+    		end
+
+    		if HasTag(bodypart, "Head") then
+    			if IsPointInWater(bodyparttransform.pos) then
+    				tripped = true
+    				drowntim = drowntim + dt
+    			end
+    		end
+
+    		if drowntim > 5 then
+    			dead = true
+    		end
+
+    		if not tripped and HasTag(bodypart, "Head") and not dead and not sitting then
+    				--Paint(GetAimPos(), (bleedintensity/sbloodval[i])*1.3, "explosion")
+    				currentvel = GetBodyVelocity(bodypart)
+    				SetBodyVelocity(bodypart, VecAdd(currentvel, headvel))
+    				--DebugPrint(VecAdd(currentvel, headvel)[2])
+    				if IsBodyBroken(bodypart) then
+    					bodyState.head = BROKEN_BODY_PART	
+    					bodyState.overall = "dead"					
+    					dead = true
+    					if bloodval[i] < sbloodval[i] - sbloodval[i] / 4 then
+    					bods = GetBodyShapes(bodypart)
+    					for i = 1,#bods do
+    						j = GetShapeJoints(bods[i])
+    						for z = 1,#j do
+    							Delete(j[i])
+    						end
+    					end
+    				end
+    				end
+    		end
+
+    		if not tripped and HasTag(bodypart, "RRLEG") or HasTag(bodypart, "LLLEG") then
+    			if not dead and not sitting and not tripped then
+    				--Paint(GetAimPos(), (bleedintensity/sbloodval[i])*1.3, "explosion")
+    				currentvel = GetBodyVelocity(bodypart)
+    				SetBodyVelocity(bodypart, VecAdd(currentvel, legvel))
+    			end
+    		end
+
+    		if IsBodyBroken(bodypart) then
+
+    			if HasTag(bodypart, "Head") then
+    				dead = true
+    			end
+
+    			if bloodval[i] < sbloodval[i] - sbloodval[i]/10 then
+    				panic = true
+    				tripped = true
+    			end
+    		end
+
+    		if IsBodyBroken(bodypart) and currentbloodvalue[i] > 0 then
+    			if bodyState.overall == "healthy" then bodyState.overall = "injured" end
+
+    			if HasTag(bodypart, "LLLEG") or HasTag(bodypart, "LLEG") then
+    				bodyState.leftLeg = BROKEN_BODY_PART			
+    				if not diddit1 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
+    					diddit1 = true
+    				end
+    			elseif HasTag(bodypart, "RRLEG") or HasTag(bodypart, "RLEG") then
+    				bodyState.rightLeg = BROKEN_BODY_PART					
+    				if not diddit2 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
+    					diddit2 = true
+    				end
+    			elseif HasTag(bodypart, "RRARM") or HasTag(bodypart, "RARM") then
+    				bodyState.rightArm = BROKEN_BODY_PART	
+    				if not diddit3 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
+    					diddit3 = true
+    				end				
+    			elseif HasTag(bodypart, "LLARM") or HasTag(bodypart, "LARM") then
+    				bodyState.leftArm = BROKEN_BODY_PART	
+    				if not diddit4 and bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/boner.xml", bodyparttransform)
+    					diddit4 = true
+    				end							
+    			end
+
+    			--Paint(GetAimPos(), bleedintensity/sbloodval[i], "explosion")
+
+    			puddleregtim = puddleregtim + dt
+
+    			PuddleHandleing()
+    			if puddleregtim > repuddle then
+    			--for i=1,bleedintensity/10 do
+    			--DebugPrint(bleedintensity)
+    			InsertPuddleToTable()
+    			bleedparticles()
+    			if bleedbool then
+    			--Paint(GetAimPos(), bleedintensity/sbloodval[i], "explosion")
+    			end
+    			--end
+    			puddleregtim = 0
+    			end
+    			bleedparticles()
+
+    			if bloodval[i] < 0.5 then ---------------------------------------------------------------
+    			bleedintensity = 1000
+    				for i=1,12 do
+    					InsertPuddleToTable()
+    				end
+    				currentbloodvalue[i] = 0
+    			end
+
+    			if HasTag(bodypart, "Torso") and bloodval[i] < sbloodval[i]/1.2 then			
+    				--DebugPrint("SUPPOSED TO BE LOL GUTTED XD")
+    				if not entrailed then
+    					bodyState.body = BROKEN_BODY_PART
+    					bodyState.overall = "dead"
+    					dead = true
+    					entrailed = true
+    					for i=1,4 do
+    						InsertPuddleToTable()
+    					end
+
+    					PlaySound(goresplat, GetBodyTransform(Torso).pos, 1)
+
+    					if gorelevel ~= 1 then
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/entrails.xml", bodyparttransform)
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/Heart.xml", bodyparttransform)
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/Spine.xml", bodyparttransform)
+    					if gorelevel ~= 2 then
+    					for i=1,2 do
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/Lung.xml", bodyparttransform)
+    					end
+    					for i=1,30 * multiplier do
+    						Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", bodyparttransform)
+    					end
+    					end
+    					end
+    					--DebugPrint("LOL GUTTED XD")
+    				end
+    			end
+
+    			if HasTag(bodypart, "Head") then
+    				bodyState.head = BROKEN_BODY_PART	
+    				bodyState.overall = "dead"	
+    				eyej = FindJoints("eye")
+    				if bloodval[i] < sbloodval[i] - sbloodval[i]/4 then
+    				for i=1,#eyej do
+    					Delete(eyej[i])
+    				end
+    				end
+    				if bloodval[i] < sbloodval[i] - sbloodval[i]/3 then
+    				if not fragged then
+    					fragged = true
+    					PlaySound(headsplat, GetBodyTransform(Torso).pos, 1)
+    					if gorelevel ~= 1 then
+    					for i=1,4 do
+    						InsertPuddleToTable()
+    					end
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/Skull_Jaw.xml.xml", bodyparttransform)
+    					for i=1,2 * multiplier do
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/Skull_Eye_Socket.xml", bodyparttransform)
+    					Spawn("MOD/main/Gore Ragdolls 2/internals/Skull_Fragment.xml", bodyparttransform)
+    					end
+    					if gorelevel ~= 2 then
+    					for i=1,10 * multiplier do
+    						Spawn("MOD/main/Gore Ragdolls 2/internals/BrainMatter.xml", bodyparttransform)
+    					end
+    				end
+    					end
+    					--DebugPrint("LOL GUTTED XD")
+    				end
+    				end
+    			end
+    		end
+    	end
+    	if IsJointBroken(FindJoint("neck")) or totalbloodvalue < starttotalbloodvalue - starttotalbloodvalue/1.5 then
+    		bodyState.head = BROKEN_NECK						
+    		bodyState.overall = "dead"	
+    		dead = true
+    	end
+
+    	if restartjoints and not tripped then
+    		restartjointsfunc()
+    	end
+
+    	if dead then
+    		SetTag(Torso, "dead")
+    		restartjointsfunc()
+    		deadtim = deadtim + dt
+    		if deadtim > 10 then
+    			entirelystop = true
+    		end
+    	end
+    end
+end
+
+function client.draw()
+    DrawUiHealthOverlay(dt)
+    if warn then
+    UiPush()
+         UiAlign("center middle")
+         --UiTranslate(400, 200)
+         UiFont("bold.ttf", 30)
+         UiColor(1,0,0)
+         UiText("PRESS"..keytokill.." AGAIN TO KILL ALL RAGDOLLS: "..10 - manualdietim)
+        UiPop()
+    end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\gorefx.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\gorefx.lua
+++ patched/main\Gore Ragdolls 2\scripts\gorefx.lua
@@ -1,86 +1,7 @@
-#include "script/common.lua"
-
+#version 2
 function rnd(mi, ma) return math.random()*(ma-mi) + mi end
+
 function rndVec(t) return Vec(rnd(-t, t), rnd(-t, t), rnd(-t, t)) end
-
-breakables = {}
-smokes = {}
-flickers = {}
-
-function init()
-	local turnoff = FindShapes("fxturnoff", true)
-	for i=1, #turnoff do
-		SetShapeEmissiveScale(turnoff[i], 0.0)
-	end
-
-	local shapes = FindShapes("fxbreak", true)
-	for i=1, #shapes do
-		local v = GetTagValue(shapes[i], "fxbreak")
-		local b = {}
-		b.shape = shapes[i]
-		b.broken = false
-		b.voxelCount = GetShapeVoxelCount(b.shape)
-		b.point = Vec()
-		b.normal = Vec()
-		b.age = 0
-		b.radius = 0
-		b.lifeTime = tonumber(string.sub(v, 2, 2))
-		b.color = string.sub(v, 3, string.len(v))
-		b.type = string.sub(v, 1, 1)
-		if b.lifeTime and b.lifeTime > 0 then
-			breakables[#breakables+1] = b		
-		end
-	end
-	snd = {}
-	snd["l"] = { LoadSound("liquid-s0.ogg"), LoadSound("liquid-m0.ogg"), LoadSound("liquid-m0.ogg")}
-	snd["g"] = { LoadSound("gas-s0.ogg"), LoadSound("gas-m0.ogg"), LoadSound("gas-l0.ogg")}
-
-	local locations = FindLocations("fxsmoke", true)
-	for i=1, #locations do
-		local l = locations[i]
-		local v = GetTagValue(l, "fxsmoke")
-		local s = {}
-		local t = GetLocationTransform(l)
-		local hit,point,normal,shape = QueryClosestPoint(t.pos, 0.5)
-		if hit then
-			s.shape = shape
-			s.enabled = true
-			local st = GetShapeWorldTransform(shape)
-			s.point = TransformToLocalPoint(st, t.pos)
-			s.normal = TransformToLocalVec(st, TransformToParentVec(t, Vec(0,0,-1)))
-			s.spawn = 0
-			s.color = string.sub(v, 3, string.len(v))
-			s.type = string.sub(v, 1, 1)
-			s.scale = tonumber(string.sub(v, 2, 2))
-			s.timeOffset = rnd(0, 10)
-			if not s.scale then
-				s.scale = 1
-			end
-			smokes[#smokes+1] = s
-		end
-	end
-	
-	local lights = FindLights("fxflicker", true)
-	for i=1, #lights do
-		local l = lights[i]
-		local shape = GetLightShape(l)
-		if IsLightActive(l) then
-			local v = GetTagValue(l, "fxflicker")
-			local f = {}
-			f.enabled = true
-			f.light = l
-			f.shape = shape
-			f.timer = 0
-			f.scale = 1
-			f.period = tonumber(string.sub(v, 1, 1))
-			if not f.period then
-				f.period = 1
-			end
-			flickers[#flickers+1] = f
-		end
-	end
-end
-
 
 function cancelAllBreakables()
 	for i=1, #breakables do
@@ -90,7 +11,6 @@
 		end
 	end
 end
-
 
 function disableJointed(shape)
 	local body = GetShapeBody(shape)
@@ -106,99 +26,6 @@
 		end
 	end
 end
-
-
-function tick(dt)
-	local hasBreakage = GetBool("game.break")
-	local breakPoint = Vec(GetFloat("game.break.x"), GetFloat("game.break.y"), GetFloat("game.break.z"))
-	for i=1, #breakables do
-		local b = breakables[i]
-		if not b.broken then
-			if IsShapeBroken(b.shape) then
-				b.age = b.lifeTime
-				b.broken = true
-				if HasTag(b.shape, "fxbreak") and hasBreakage then
-					disableJointed(b.shape)
-					cancelAllBreakables()
-					local t = GetShapeWorldTransform(b.shape)
-					local h,cp,cn = GetShapeClosestPoint(b.shape, breakPoint)
-					if h and VecLength(VecSub(cp, breakPoint)) < 1.0 then
-						local mi, ma = GetShapeBounds(b.shape)
-						if b.type == "l" then
-							local center = VecLerp(mi, ma, 0.5)
-							center[2] = math.max(breakPoint[2], center[2])
-							b.normal = TransformToLocalVec(t, VecNormalize(VecSub(breakPoint, center)))
-						else
-							b.normal = TransformToLocalVec(t, VecNormalize(VecSub(breakPoint, cp)))
-						end
-						b.point = TransformToLocalPoint(t, VecAdd(cp, VecScale(cn, 0.2)))
-						b.radius = clamp(VecLength(VecSub(breakPoint, cp))*0.8-0.1, 0.1, 0.25)
-						b.age = 0
-						if snd[b.type] then
-							if b.lifeTime < 1.5 then
-								PlaySound(snd[b.type][1], breakPoint)
-							elseif b.lifeTime < 2.5 then
-								PlaySound(snd[b.type][2], breakPoint)
-							else
-								PlaySound(snd[b.type][3], breakPoint)
-							end
-						end
-					end
-				end
-			end
-		end
-	end
-	
-	for i=1, #smokes do
-		local s = smokes[i]
-		if s.enabled then
-			if IsShapeBroken(s.shape) then
-				s.enabled = false
-			end
-		end
-	end
-	
-	for i=1, #flickers do
-		local f = flickers[i]
-		if f.enabled then
-			if IsShapeBroken(f.shape) then
-				f.enabled = false
-			else
-				f.timer = f.timer - dt
-				if f.timer < 0 then
-					if f.scale == 1 then
-						f.scale = rnd(0.2, 0.5)
-						SetShapeEmissiveScale(f.shape, f.scale)
-						f.timer = rnd(0.0, f.period*0.3)
-					else
-						f.scale = 1
-						SetShapeEmissiveScale(f.shape, f.scale)
-						f.timer = rnd(0.0, f.period)
-					end
-				end
-			end
-		end
-	end
-end
-
-
-function update(dt)
-	for i=1, #breakables do
-		local b = breakables[i]
-		if b.broken and b.age < b.lifeTime then
-			b.age = math.min(b.age + dt, b.lifeTime)
-			effect(b)
-		end
-	end
-
-	for i=1, #smokes do
-		local s = smokes[i]
-		if s.enabled then
-			emitSmoke(s)
-		end
-	end
-end
-
 
 function effect(b)
 	local q = 1.0 - b.age/b.lifeTime
@@ -277,7 +104,6 @@
 	end
 end
 
-
 function emitSmoke(s)
 	local t = GetShapeWorldTransform(s.shape)
 	local p = TransformToParentPoint(t, s.point)
@@ -314,3 +140,172 @@
 	end
 end
 
+function server.init()
+    local turnoff = FindShapes("fxturnoff", true)
+    for i=1, #turnoff do
+    	SetShapeEmissiveScale(turnoff[i], 0.0)
+    end
+    local shapes = FindShapes("fxbreak", true)
+    for i=1, #shapes do
+    	local v = GetTagValue(shapes[i], "fxbreak")
+    	local b = {}
+    	b.shape = shapes[i]
+    	b.broken = false
+    	b.voxelCount = GetShapeVoxelCount(b.shape)
+    	b.point = Vec()
+    	b.normal = Vec()
+    	b.age = 0
+    	b.radius = 0
+    	b.lifeTime = tonumber(string.sub(v, 2, 2))
+    	b.color = string.sub(v, 3, string.len(v))
+    	b.type = string.sub(v, 1, 1)
+    	if b.lifeTime and b.lifeTime ~= 0 then
+    		breakables[#breakables+1] = b		
+    	end
+    end
+    snd = {}
+    local locations = FindLocations("fxsmoke", true)
+    for i=1, #locations do
+    	local l = locations[i]
+    	local v = GetTagValue(l, "fxsmoke")
+    	local s = {}
+    	local t = GetLocationTransform(l)
+    	local hit,point,normal,shape = QueryClosestPoint(t.pos, 0.5)
+    	if hit then
+    		s.shape = shape
+    		s.enabled = true
+    		local st = GetShapeWorldTransform(shape)
+    		s.point = TransformToLocalPoint(st, t.pos)
+    		s.normal = TransformToLocalVec(st, TransformToParentVec(t, Vec(0,0,-1)))
+    		s.spawn = 0
+    		s.color = string.sub(v, 3, string.len(v))
+    		s.type = string.sub(v, 1, 1)
+    		s.scale = tonumber(string.sub(v, 2, 2))
+    		s.timeOffset = rnd(0, 10)
+    		if not s.scale then
+    			s.scale = 1
+    		end
+    		smokes[#smokes+1] = s
+    	end
+    end
+    local lights = FindLights("fxflicker", true)
+    for i=1, #lights do
+    	local l = lights[i]
+    	local shape = GetLightShape(l)
+    	if IsLightActive(l) then
+    		local v = GetTagValue(l, "fxflicker")
+    		local f = {}
+    		f.enabled = true
+    		f.light = l
+    		f.shape = shape
+    		f.timer = 0
+    		f.scale = 1
+    		f.period = tonumber(string.sub(v, 1, 1))
+    		if not f.period then
+    			f.period = 1
+    		end
+    		flickers[#flickers+1] = f
+    	end
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        local hasBreakage = GetBool("game.break")
+        local breakPoint = Vec(GetFloat("game.break.x"), GetFloat("game.break.y"), GetFloat("game.break.z"))
+        for i=1, #smokes do
+        	local s = smokes[i]
+        	if s.enabled then
+        		if IsShapeBroken(s.shape) then
+        			s.enabled = false
+        		end
+        	end
+        end
+        for i=1, #flickers do
+        	local f = flickers[i]
+        	if f.enabled then
+        		if IsShapeBroken(f.shape) then
+        			f.enabled = false
+        		else
+        			f.timer = f.timer - dt
+        			if f.timer < 0 then
+        				if f.scale == 1 then
+        					f.scale = rnd(0.2, 0.5)
+        					SetShapeEmissiveScale(f.shape, f.scale)
+        					f.timer = rnd(0.0, f.period*0.3)
+        				else
+        					f.scale = 1
+        					SetShapeEmissiveScale(f.shape, f.scale)
+        					f.timer = rnd(0.0, f.period)
+        				end
+        			end
+        		end
+        	end
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        for i=1, #breakables do
+        	local b = breakables[i]
+        	if b.broken and b.age < b.lifeTime then
+        		b.age = math.min(b.age + dt, b.lifeTime)
+        		effect(b)
+        	end
+        end
+        for i=1, #smokes do
+        	local s = smokes[i]
+        	if s.enabled then
+        		emitSmoke(s)
+        	end
+        end
+    end
+end
+
+function client.init()
+    snd["l"] = { LoadSound("liquid-s0.ogg"), LoadSound("liquid-m0.ogg"), LoadSound("liquid-m0.ogg")}
+    snd["g"] = { LoadSound("gas-s0.ogg"), LoadSound("gas-m0.ogg"), LoadSound("gas-l0.ogg")}
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    for i=1, #breakables do
+    	local b = breakables[i]
+    	if not b.broken then
+    		if IsShapeBroken(b.shape) then
+    			b.age = b.lifeTime
+    			b.broken = true
+    			if HasTag(b.shape, "fxbreak") and hasBreakage then
+    				disableJointed(b.shape)
+    				cancelAllBreakables()
+    				local t = GetShapeWorldTransform(b.shape)
+    				local h,cp,cn = GetShapeClosestPoint(b.shape, breakPoint)
+    				if h and VecLength(VecSub(cp, breakPoint)) < 1.0 then
+    					local mi, ma = GetShapeBounds(b.shape)
+    					if b.type == "l" then
+    						local center = VecLerp(mi, ma, 0.5)
+    						center[2] = math.max(breakPoint[2], center[2])
+    						b.normal = TransformToLocalVec(t, VecNormalize(VecSub(breakPoint, center)))
+    					else
+    						b.normal = TransformToLocalVec(t, VecNormalize(VecSub(breakPoint, cp)))
+    					end
+    					b.point = TransformToLocalPoint(t, VecAdd(cp, VecScale(cn, 0.2)))
+    					b.radius = clamp(VecLength(VecSub(breakPoint, cp))*0.8-0.1, 0.1, 0.25)
+    					b.age = 0
+    					if snd[b.type] then
+    						if b.lifeTime < 1.5 then
+    							PlaySound(snd[b.type][1], breakPoint)
+    						elseif b.lifeTime < 2.5 then
+    							PlaySound(snd[b.type][2], breakPoint)
+    						else
+    							PlaySound(snd[b.type][3], breakPoint)
+    						end
+    					end
+    				end
+    			end
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\gorelaunch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\gorelaunch.lua
+++ patched/main\Gore Ragdolls 2\scripts\gorelaunch.lua
@@ -1,29 +1,4 @@
-function init()
-	yeeeeeeeeted = false
-	force = 5
-	tim = 0
-end
-
-function tick()
-	body = FindBody("gore")
-	if not yeeeeeeeeted then
-		local pos = Vec(0,0,0)
-		imp = Vec(math.random(-force,force),math.random(force/3,force),math.random(-force,force))
-		SetBodyVelocity(body, imp)
-		imp = Vec(math.random(-force,force),math.random(force/3,force),math.random(-force,force))
-		SetBodyAngularVelocity(body, imp)
-		yeeeeeeeeted = true
-	end
-	tim = tim + 1
-	if tim < 75 then
-	Paint(GetAimPos(), 0.11, "explosion")
-	end
-	if InputPressed("L") then
-		body = FindBody("gore")
-		Delete(body)
-	end
-end
-
+#version 2
 function GetAimPos()
      ct = GetBodyTransform(body)
     ctrot1, ctrot2, ctrot3 = GetQuatEuler(ct.rot)
@@ -42,4 +17,37 @@
         distance = hitDistance
     end
     return forwardPos, hit, distance
-end+end
+
+function server.init()
+    yeeeeeeeeted = false
+    force = 5
+    tim = 0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        body = FindBody("gore")
+        if not yeeeeeeeeted then
+        	local pos = Vec(0,0,0)
+        	imp = Vec(math.random(-force,force),math.random(force/3,force),math.random(-force,force))
+        	SetBodyVelocity(body, imp)
+        	imp = Vec(math.random(-force,force),math.random(force/3,force),math.random(-force,force))
+        	SetBodyAngularVelocity(body, imp)
+        	yeeeeeeeeted = true
+        end
+        tim = tim + 1
+        if tim < 75 then
+        Paint(GetAimPos(), 0.11, "explosion")
+        end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("L") then
+    	body = FindBody("gore")
+    	Delete(body)
+    end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\Oscillograph.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\Oscillograph.lua
+++ patched/main\Gore Ragdolls 2\scripts\Oscillograph.lua
@@ -1,6 +1,4 @@
-oscillographicShift = 0
-heartbeatMask = "MOD/imgs/heartbeatGradient.png"		
-
+#version 2
 function draw2(dt)
 	UiTranslate(400,400)
 	UiDrawOxygenOscillograph(dt,200,20,5,30,300)
@@ -77,12 +75,11 @@
 	UiPop()
 end
 
---- HELPER FUNCTIONS ---
-
 function drawRect(x,y,w,h,r,g,b,a)
 	UiPush()
 		UiColor(r,g,b,a)
 		UiTranslate(x,y)
 		UiRect(w,h)
 	UiPop()
-end+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\RndRagdoll.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\RndRagdoll.lua
+++ patched/main\Gore Ragdolls 2\scripts\RndRagdoll.lua
@@ -1,4 +1 @@
-function init()
-end
-function tick()
-end+#version 2

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\SpawnPad.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\SpawnPad.lua
+++ patched/main\Gore Ragdolls 2\scripts\SpawnPad.lua
@@ -1,91 +1,100 @@
-function init()
-	Location = FindShape("Spawn")
-	if GetTagValue(Location, "Spawn") == "Friendly" then
-		type = "Friend"
-	end
-	if GetTagValue(Location, "Spawn") == "Enemy" then
-		type = "Enemy"
-	end
-	RagdollType = GetTagValue(Location, "Type")
-	Diffragdolls = tonumber(GetTagValue(Location, "DiffRag"))
-	timetonextspawn = 8
-	maxragdollsatspawn = 5
-	range = 2
-	timer = 0
-	chancefor1 = 10
-	chancefor2 = 80
-	chancefor3 = 95
-	chancefor4 = 100
-end
-function tick(dt)
-	if IsShapeBroken(Location) then
-		Absolute = true
-		start = true
-		body = GetShapeBody(Location)
-		RemoveTag(body, "enemy")
-		RemoveTag(body, "friend")
-	end
-	if not Absolute then
-	draw()
-	LT = GetShapeWorldTransform(Location)
-	if not start then
-		LT2 = LT
-		LT2.pos[2] = LT2.pos[2] + 1
-		body = GetShapeBody(Location)
-		if type == "Enemy" then
-			SetTag(body, "enemy")
-		DrawShapeOutline(Location, 0, 0, 1, 1)
-		else
-			SetTag(body, "friend")
-		DrawShapeOutline(Location, 1, 0, 0, 1)
-		end
-	end
-	if start then
-	timer = timer + dt
-	--DebugPrint(timer)
-	if timer > timetonextspawn then
-		--RandSpawn = Vec(LT[1] + math.random(-range,range), LT[2], LT[3] + math.random(-range, range))
-		timer = 0
-		rndragdoll = math.random(1, Diffragdolls)
-		--if rndragdoll > 0 and rndragdoll < 50 then
-		--	rndragdoll = 1
-		--end
-		--if rndragdoll > 50 and rndragdoll < 65 then
-		--	rndragdoll = 2
-		--end
-		--if rndragdoll > 65 and rndragdoll < 83 then
-		--	rndragdoll = 3
-		--end
-		--if rndragdoll > 83 then
-		--	rndragdoll = 4
-		--end
-		Spawn("MOD/main/Gore Ragdolls 2/Agro pack/"..RagdollType..type..rndragdoll..".xml", Transform(LT.pos))
-		--DebugPrint(type.." Spawned")
-	end
-end
-end
-cycled = false
-	if InputPressed("j") and not start and not cycled then
-		start = true
-		cycled = true
-	end
-	if InputPressed("j") and start and not cycled then
-		start = false
-		cycled = true
-	end
+#version 2
+function server.init()
+    Location = FindShape("Spawn")
+    if GetTagValue(Location, "Spawn") == "Friendly" then
+    	type = "Friend"
+    end
+    if GetTagValue(Location, "Spawn") == "Enemy" then
+    	type = "Enemy"
+    end
+    RagdollType = GetTagValue(Location, "Type")
+    Diffragdolls = tonumber(GetTagValue(Location, "DiffRag"))
+    timetonextspawn = 8
+    maxragdollsatspawn = 5
+    range = 2
+    timer = 0
+    chancefor1 = 10
+    chancefor2 = 80
+    chancefor3 = 95
+    chancefor4 = 100
 end
 
-function draw()
-	if not start then
-	 UiPush()
-      UiAlign("center middle")
-      UiTranslate(400, 200)
-      UiFont("bold.ttf", 30)
-      UiText("J = Start/Disable spawning")
-      UiTranslate(0, 50)
-      UiText("L = Delete dead")
-      UiTranslate(0, 50)
-      UiText("M = Delete everyone")
-    UiPop()
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        	if IsShapeBroken(Location) then
+        		Absolute = true
+        		start = true
+        		body = GetShapeBody(Location)
+        		RemoveTag(body, "enemy")
+        		RemoveTag(body, "friend")
+        	end
+        	if not Absolute then
+        	draw()
+        	LT = GetShapeWorldTransform(Location)
+        	if not start then
+        		LT2 = LT
+        		LT2.pos[2] = LT2.pos[2] + 1
+        		body = GetShapeBody(Location)
+        		if type == "Enemy" then
+        			SetTag(body, "enemy")
+        		DrawShapeOutline(Location, 0, 0, 1, 1)
+        		else
+        			SetTag(body, "friend")
+        		DrawShapeOutline(Location, 1, 0, 0, 1)
+        		end
+        	end
+        	if start then
+        	timer = timer + dt
+        	--DebugPrint(timer)
+        	if timer > timetonextspawn then
+        		--RandSpawn = Vec(LT[1] + math.random(-range,range), LT[2], LT[3] + math.random(-range, range))
+        		timer = 0
+        		rndragdoll = math.random(1, Diffragdolls)
+        		--if rndragdoll > 0 and rndragdoll < 50 then
+        		--	rndragdoll = 1
+        		--end
+        		--if rndragdoll > 50 and rndragdoll < 65 then
+        		--	rndragdoll = 2
+        		--end
+        		--if rndragdoll > 65 and rndragdoll < 83 then
+        		--	rndragdoll = 3
+        		--end
+        		--if rndragdoll > 83 then
+        		--	rndragdoll = 4
+        		--end
+        		Spawn("MOD/main/Gore Ragdolls 2/Agro pack/"..RagdollType..type..rndragdoll..".xml", Transform(LT.pos))
+        		--DebugPrint(type.." Spawned")
+        	end
+        end
+        end
+        cycled = false
+    end
 end
-end+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("j") and not start and not cycled then
+    	start = true
+    	cycled = true
+    end
+    if InputPressed("j") and start and not cycled then
+    	start = false
+    	cycled = true
+    end
+end
+
+function client.draw()
+    	if not start then
+    	 UiPush()
+          UiAlign("center middle")
+          UiTranslate(400, 200)
+          UiFont("bold.ttf", 30)
+          UiText("J = Start/Disable spawning")
+          UiTranslate(0, 50)
+          UiText("L = Delete dead")
+          UiTranslate(0, 50)
+          UiText("M = Delete everyone")
+        UiPop()
+    end
+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\UIBodyState.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\UIBodyState.lua
+++ patched/main\Gore Ragdolls 2\scripts\UIBodyState.lua
@@ -1,18 +1,4 @@
-RED = {r=1,g=0,b=0,a=1}
-GREEN = {r=0,g=1,b=0,a=1}
-YELLOW = {r=1,g=1,b=0,a=1}
-
-HEAD_SIZE = 30
-BODY_WIDTH = 38
-BODY_HEIGHT= 60
-ARM_WIDTH = 18
-
-COLORS = {red=RED,green=GREEN,yellow=YELLOW}
-
-HEALTHY = "healthy"
-INJURED = "injured"
-DEAD = "dead"
-
+#version 2
 function Effect(title, color)
 	return {text=title, color=color}
 end
@@ -26,20 +12,6 @@
 	if effects == nil then effects = {} end
 	return {color=color, effects=effects}
 end
-
-BROKEN_BODY_PART = BodyPart(RED, {Effect("broken", RED)}) 
-BROKEN_NECK = BodyPart(RED, {Effect("broken neck", RED)}) 
-
-HEALTHY_BODY_STATE = BodyState(
-		HEALTHY,
-		BodyPart(GREEN, {}),
-		BodyPart(GREEN, {}),	
-		BodyPart(GREEN, {}),
-		BodyPart(GREEN, {}),
-		BodyPart(GREEN, {}),
-		BodyPart(GREEN, {}),
-		{}
-	)
 
 function UiDrawBodyState(state)	
 	UiTranslate(ARM_WIDTH+2+(BODY_WIDTH-HEAD_SIZE)/2,0)
@@ -70,4 +42,5 @@
 
 function UiDrawArm(color)
 	drawRect(0,0,ARM_WIDTH,BODY_HEIGHT,color.r,color.g,color.b,color.a)
-end+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\UiHealthOverlay.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\UiHealthOverlay.lua
+++ patched/main\Gore Ragdolls 2\scripts\UiHealthOverlay.lua
@@ -1,18 +1,4 @@
-#include "Oscillograph.lua"
-#include "UIBodyState.lua"
-
-HEALTH_UI_BACKGROUND_WIDTH = 300
-HEALTH_UI_BACKGROUND_HEIGHT= 110
-HEALTH_UI_DETAIL_BACKGROUND_WIDTH = 150
-HEALTH_UI_DETAIL_BACKGROUND_HEIGHT= 230
-HEALTH_UI_INFO_BACKGROUND_HEIGHT= 24
-
-showHealthMenu = false
-showHealthDetails = false
-
-bodyState = HEALTHY_BODY_STATE
-
-
+#version 2
 function indexOf(tabl, el)	
 	for k,v in pairs(tab) do
 		if v.text == el then
@@ -24,114 +10,105 @@
 
 function deleteElement(tab, el) 
 	local i = indexOf(tab, el)
-	if i > 0 then
+	if i ~= 0 then
 		table.remove(tab, i)
 	end
 end
-
--- SetHealthy() - Sets the whole status of the body to healty, which causes the healthy text to appear on the ui and the oscillograph look normal
--- SetInjured() - Sets the whole status of the body to injured, which causes the injured text to appear on the ui and the oscillograph will be running faster 
--- SetDead() - Sets the whole status of the body to dead, which causes the dead text to appear on the ui and the oscillograph will flatline
--- None of the above methods will change colors on body parts!
--- AddHealthEffect(effectText, color) - This will add a general effect with the given text and color to the detail view (pressing X). Possible colors are RED, YELLOW, GREEN.
--- RemoveHealthEffect(effectText) - This will remove the given general effect by its text if the effect was added earlier
---
--- SetHeadHealth(color) - This sets the color of the head to the given color. Possible colors are RED, YELLOW, GREEN
--- AddHeadHealthEffect(effectText, color) - his will add an effect to the head with the given text and color to the detail view (pressing X). Possible colors are RED, YELLOW, GREEN.
--- RemoveHeadHealthEffect(effectText) - This will remove the given effect from the head by its text if the effect was added earlier
---
--- SetTorsoHealth(color) - This sets the color of the torso to the given color. Possible colors are RED, YELLOW, GREEN
--- AddTorsoHealthEffect(effectText, color) - his will add an effect to the torso with the given text and color to the detail view (pressing X). Possible colors are RED, YELLOW, GREEN.
--- RemoveTorsoHealthEffect(effectText) - This will remove the given effect from the torso by its text if the effect was added earlier
---
--- SetLeftArmHealth(color) - This sets the color of the left arm to the given color. Possible colors are RED, YELLOW, GREEN
--- AddLeftArmHealthEffect(effectText, color) - his will add an effect to the left arm with the given text and color to the detail view (pressing X). Possible colors are RED, YELLOW, GREEN.
--- RemoveLeftArmHealthEffect(effectText) - This will remove the given effect from the left arm by its text if the effect was added earlier
---
--- SetRightArmHealth(color) - This sets the color of the right arm to the given color. Possible colors are RED, YELLOW, GREEN
--- AddRightArmHealthEffect(effectText, color) - his will add an effect to the right arm with the given text and color to the detail view (pressing X). Possible colors are RED, YELLOW, GREEN.
--- RemoveRightArmHealthEffect(effectText) - This will remove the given effect from the right arm by its text if the effect was added earlier
---
--- SetLeftLegHealth(color) - This sets the color of the left leg to the given color. Possible colors are RED, YELLOW, GREEN
--- AddLeftLegHealthEffect(effectText, color) - his will add an effect to the left leg with the given text and color to the detail view (pressing X). Possible colors are RED, YELLOW, GREEN.
--- RemoveLeftLegHealthEffect(effectText) - This will remove the given effect from the left leg by its text if the effect was added earlier
---
--- SetRightLegHealth(color) - This sets the color of the right leg to the given color. Possible colors are RED, YELLOW, GREEN
--- AddRightLegHealthEffect(effectText, color) - his will add an effect to the right leg with the given text and color to the detail view (pressing X). Possible colors are RED, YELLOW, GREEN.
--- RemovRightLegHealthEffect(effectText) - This will remove the given effect from the right leg by its text if the effect was added earlier
 
 function SetHealthy()
 	bodyState.overall = HEALTHY
 end
+
 function SetInjured()
 	bodyState.overall = INJURED
 end
+
 function SetDead()
 	bodyState.overall = DEAD
 end
+
 function AddHealthEffect(effect, color)
 	table.insert(bodyState.effects, Effect(effect, color))
 end
+
 function RemoveHealthEffect(effect)
 	deleteElement(bodyState.effects, effect)
 end
+
 function SetHeadHealth(color)
 	bodyState.head.color = color	
 end
+
 function AddHeadHealthEffect(effect, color)
 	table.insert(bodyState.head.effects, Effect(effect, color))
 end
+
 function RemoveHeadHealthEffect(effect)
 	deleteElement(bodyState.head.effects, effect)
 end
+
 function SetTorsoHealth(color)
 	bodyState.body.color = color	
 end
+
 function AddTorsoHealthEffect(effect, color)
 	table.insert(bodyState.body.effects, Effect(effect, color))
 end
+
 function RemoveTorsoHealthEffect(effect)
 	deleteElement(bodyState.body.effects, effect)
 end
+
 function SetLeftArmHealth(color)
 	bodyState.leftArm.color = color	
 end
+
 function AddLeftArmHealthEffect(effect, color)
 	table.insert(bodyState.leftArm.effects, Effect(effect, color))
 end
+
 function RemoveLeftArmHealthEffect(effect)
 	deleteElement(bodyState.leftArm.effects, effect)
 end
+
 function SetRightArmHealth(color)
 	bodyState.rightArm.color = color	
 end
+
 function AddRightArmHealthEffect(effect, color)
 	table.insert(bodyState.rightArm.effects, Effect(effect, color))
 end
+
 function RemoveRightArmHealthEffect(effect)
 	deleteElement(bodyState.rightArm.effects, effect)
 end
+
 function SetRightLegHealth(color)
 	bodyState.rightLeg.color = color	
 end
+
 function AddRightLegHealthEffect(effect, color)
 	table.insert(bodyState.rightLeg.effects, Effect(effect, color))
 end
+
 function RemoveRightLegHealthEffect(effect)
 	deleteElement(bodyState.rightLeg.effects, effect)
 end
+
 function SetLeftLegHealth(color)
 	bodyState.leftLeg.color = color	
 end
+
 function AddLeftLegHealthEffect(effect, color)
 	table.insert(bodyState.leftLeg.effects, Effect(effect, color))
 end
+
 function RemoveLeftLegHealthEffect(effect)
 	deleteElement(bodyState.leftLeg.effects, effect)
 end
 
 function WriteDetailStatus(name, effects,y)
-	if #effects > 0 then
+	if #effects ~= 0 then
 		for i,effect in ipairs(effects) do				
 			writeText(name .. effect.text,18,10,y, false,effect.color)
 			y=y+20
@@ -253,4 +230,5 @@
 function HideUiHealthOverlay()
 	showHealthMenu = false
 	showHealthDetails = false
-end+end
+

```

---

# Migration Report: main\Gore Ragdolls 2\scripts\UiHealthOverlayManager.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\Gore Ragdolls 2\scripts\UiHealthOverlayManager.lua
+++ patched/main\Gore Ragdolls 2\scripts\UiHealthOverlayManager.lua
@@ -1,11 +1,15 @@
-function tick()
-	SetInt("health.ui.target.body",GetShapeBody(GetPlayerLookingShape()))	
-end
-
+#version 2
 function GetPlayerLookingShape()
-	local hit, dist, normal, shape = QueryRaycast(GetPlayerCameraTransform().pos, TransformToParentVec(GetPlayerCameraTransform(), Vec(0,0,-1)), 1000)
+	local hit, dist, normal, shape = QueryRaycast(GetPlayerCameraTransform(playerId).pos, TransformToParentVec(GetPlayerCameraTransform(playerId), Vec(0,0,-1)), 1000)
 	if hit then
 		return shape
 	end
 	return nil
-end+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        SetInt("health.ui.target.body",GetShapeBody(GetPlayerLookingShape()), true)	
+    end
+end
+

```

---

# Migration Report: main\ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\ui.lua
+++ patched/main\ui.lua
@@ -1,10 +1,4 @@
--- ui.lua
--- @date 2021-09-06
--- @author Eldin Zenderink
--- @brief All the ui helper functions reside here
-#include "util.lua"
-
-_UI_Toggle_Buttons = {}
+#version 2
 function Generic_TableContains(t1,contains)
     for i=1,#t1 do
         if t1[i] == contains then
@@ -13,7 +7,7 @@
     end
     return false
 end
--- @note original from smokegun mod from teardown!
+
 function Ui_StringProperty(x, y, current, name, notes, list)
     local value = nil
     if current == "" then
@@ -54,7 +48,6 @@
 	local awaiting_key_press = GetBool("savegame.mod.planespawner.ui.keyselector." .. id .. ".awaiting_key_press")
 	local last_pressed = InputLastPressedKey():lower()
 
-
 	local ignore_inputs = {
 		" ",
 		",",
@@ -83,12 +76,11 @@
 		last_pressed = current_key
 	end
 
-
 	local  color = {0.5,0.5,0.5,1}
 	local text_color = {1,1,1,1}
 
 	if awaiting_key_press and last_pressed ~= current_key then
-		SetBool("savegame.mod.planespawner.ui.keyselector." .. id .. ".awaiting_key_press", false)
+		SetBool("savegame.mod.planespawner.ui.keyselector." .. id .. ".awaiting_key_press", false, true)
 		value = last_pressed
 	end
     UiPush()
@@ -110,7 +102,7 @@
 		end
         if UiTextedButton(value, "center middle", 100, (font_size / 2 * 3), color, text_color) then
 			if not awaiting_key_press then
-				SetBool("savegame.mod.planespawner.ui.keyselector." .. id .. ".awaiting_key_press", true)
+				SetBool("savegame.mod.planespawner.ui.keyselector." .. id .. ".awaiting_key_press", true, true)
 			end
 			value = last_pressed
         end
@@ -162,7 +154,6 @@
 		color = {0.5,0.5,0.5,1}
 	end
 
-
 	if clicked then
 		color = {0.2,0.8,0.2,1}
 	end

```

---

# Migration Report: main\umf\umf_meta.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\umf\umf_meta.lua
+++ patched/main\umf\umf_meta.lua
@@ -1,24 +1,3 @@
-local __RUNLATER = {} UMF_RUNLATER = function(code) __RUNLATER[#__RUNLATER + 1] = code end
-(function() if hook then return end local hook_table = {} local hook_compiled = {} local function recompile( event ) local hooks = {} for k, v in pairs( hook_table[event] ) do hooks[#hooks + 1] = v end hook_compiled[event] = hooks end hook = { table = hook_table } function hook.add( event, identifier, func ) assert( type( event ) == "string", "Event must be a string" ) if func then assert( identifier ~= nil, "Identifier must not be nil" ) assert( type( func ) == "function", "Callback must be a function" ) else assert( type( identifier ) == "function", "Callback must be a function" ) end hook_table[event] = hook_table[event] or {} hook_table[event][identifier] = func or identifier recompile( event ) return identifier end function hook.remove( event, identifier ) assert( type( event ) == "string", "Event must be a string" ) assert( identifier ~= nil, "Identifier must not be nil" ) if hook_table[event] then hook_table[event][identifier] = nil if next( hook_table[event] ) == nil then hook_table[event] = nil hook_compiled[event] = nil else recompile( event ) end end end function hook.run( event, ... ) local hooks = hook_compiled[event] if not hooks then return end for i = 1, #hooks do local a, b, c, d, e = hooks[i]( ... ) if a ~= nil then return a, b, c, d, e end end end function hook.saferun( event, ... ) local hooks = hook_compiled[event] if not hooks then return end for i = 1, #hooks do local s, a, b, c, d, e = softassert( pcall( hooks[i], ... ) ) if s and a ~= nil then return a, b, c, d, e end end end function hook.used( event ) return hook_table[event] end end)();
-(function() local original = {} local function call_original( name, ... ) local fn = original[name] if fn then return fn( ... ) end end local detoured = {} function DETOUR( name, generator ) original[name] = _G[name] detoured[name] = generator( function( ... ) return call_original( name, ... ) end ) rawset( _G, name, nil ) end setmetatable( _G, { __index = detoured, __newindex = function( self, k, v ) if detoured[k] then original[k] = v else rawset( self, k, v ) end end, } ) end)();
-(function() UMF_RUNLATER "UpdateQuickloadPatch()" local hook = hook local function checkoriginal( b, ... ) if not b then printerror( ... ) return end return ... end local function simple_detour( name ) local event = "base." .. name DETOUR( name, function( original ) return function( ... ) hook.saferun( event, ... ) return checkoriginal( pcall( original, ... ) ) end end ) end local detours = { "init", "tick", "update", } for i = 1, #detours do simple_detour( detours[i] ) end function shoulddraw( kind ) return hook.saferun( "api.shoulddraw", kind ) ~= false end DETOUR( "draw", function( original ) return function( dt ) if shoulddraw( "all" ) then hook.saferun( "base.predraw", dt ) if shoulddraw( "original" ) then checkoriginal( pcall( original, dt ) ) end hook.saferun( "base.draw", dt ) end end end ) DETOUR( "Command", function( original ) return function( cmd, ... ) hook.saferun( "base.precmd", cmd, { ... } ) local a, b, c, d, e, f = original( cmd, ... ) hook.saferun( "base.postcmd", cmd, { ... }, { a, b, c, d, e, f } ) end end ) local saved = {} local function hasfunction( t, bck ) if bck[t] then return end bck[t] = true for k, v in pairs( t ) do if type( v ) == "function" then return true end if type( v ) == "table" and hasfunction( v, bck ) then return true end end end function UpdateQuickloadPatch() for k, v in pairs( _G ) do if k ~= "_G" and type( v ) == "table" and hasfunction( v, {} ) then saved[k] = v end end end local quickloadfix = function() for k, v in pairs( saved ) do _G[k] = v end end DETOUR( "handleCommand", function( original ) return function( command, ... ) if command == "quickload" then quickloadfix() end hook.saferun( "base.command." .. command, ... ) return original( command, ... ) end end ) hook.add( "base.tick", "api.firsttick", function() hook.remove( "base.tick", "api.firsttick" ) hook.saferun( "api.firsttick" ) if type( firsttick ) == "function" then firsttick() end end ) end)();
-(function() function IsPlayerInVehicle() return GetBool( "game.player.usevehicle" ) end local tool = GetString( "game.player.tool" ) local invehicle = IsPlayerInVehicle() local keyboardkeys = { "esc", "up", "down", "left", "right", "space", "interact", "return" } for i = 97, 97 + 25 do keyboardkeys[#keyboardkeys + 1] = string.char( i ) end local function checkkeys( func, mousehook, keyhook ) if hook.used( keyhook ) and func( "any" ) then for i = 1, #keyboardkeys do if func( keyboardkeys[i] ) then hook.saferun( keyhook, keyboardkeys[i] ) end end end if hook.used( mousehook ) then if func( "lmb" ) then hook.saferun( mousehook, "lmb" ) end if func( "rmb" ) then hook.saferun( mousehook, "rmb" ) end end end local mousekeys = { "lmb", "rmb", "mmb" } local heldkeys = {} hook.add( "base.tick", "api.default_hooks", function() if InputLastPressedKey then for i = 1, #mousekeys do local k = mousekeys[i] if InputPressed( k ) then hook.saferun( "api.mouse.pressed", k ) elseif InputReleased( k ) then hook.saferun( "api.mouse.released", k ) end end local lastkey = InputLastPressedKey() if lastkey ~= "" then heldkeys[lastkey] = true hook.saferun( "api.key.pressed", lastkey ) end for key in pairs( heldkeys ) do if not InputDown( key ) then heldkeys[key] = nil hook.saferun( "api.key.released", key ) break end end local wheel = InputValue( "mousewheel" ) if wheel ~= 0 then hook.saferun( "api.mouse.wheel", wheel ) end local mousedx = InputValue( "mousedx" ) local mousedy = InputValue( "mousedy" ) if mousedx ~= 0 or mousedy ~= 0 then hook.saferun( "api.mouse.move", mousedx, mousedy ) end elseif InputPressed then checkkeys( InputPressed, "api.mouse.pressed", "api.key.pressed" ) checkkeys( InputReleased, "api.mouse.released", "api.key.released" ) local wheel = InputValue( "mousewheel" ) if wheel ~= 0 then hook.saferun( "api.mouse.wheel", wheel ) end local mousedx = InputValue( "mousedx" ) local mousedy = InputValue( "mousedy" ) if mousedx ~= 0 or mousedy ~= 0 then hook.saferun( "api.mouse.move", mousedx, mousedy ) end end local n_invehicle = IsPlayerInVehicle() if invehicle ~= n_invehicle then hook.saferun( n_invehicle and "api.player.enter_vehicle" or "api.player.exit_vehicle", n_invehicle and GetPlayerVehicle() ) invehicle = n_invehicle end local n_tool = GetString( "game.player.tool" ) if tool ~= n_tool then hook.saferun( "api.player.switch_tool", n_tool, tool ) tool = n_tool end end ) end)();
-(function() util = util or {} do local serialize_any, serialize_table serialize_table = function( val, bck ) if bck[val] then return "nil" end bck[val] = true local entries = {} for k, v in pairs( val ) do entries[#entries + 1] = string.format( "[%s] = %s", serialize_any( k, bck ), serialize_any( v, bck ) ) end return string.format( "{%s}", table.concat( entries, "," ) ) end serialize_any = function( val, bck ) local vtype = type( val ) if vtype == "table" then return serialize_table( val, bck ) elseif vtype == "string" then return string.format( "%q", val ) elseif vtype == "function" or vtype == "userdata" then return string.format( "nil ", tostring( val ) ) else return tostring( val ) end end function util.serialize( ... ) local result = {} for i = 1, select( "#", ... ) do result[i] = serialize_any( select( i, ... ), {} ) end return table.concat( result, "," ) end end function util.unserialize( dt ) local fn = loadstring( "return " .. dt ) if fn then setfenv( fn, {} ) return fn() end end do local function serialize_any( val, bck ) local vtype = type( val ) if vtype == "table" then if bck[val] then return "{}" end bck[val] = true local len = 0 for k, v in pairs( val ) do len = len + 1 end local rt = {} if len == #val then for i = 1, #val do rt[i] = serialize_any( val[i], bck ) end return string.format( "[%s]", table.concat( rt, "," ) ) else for k, v in pairs( val ) do if type( k ) == "string" or type( k ) == "number" then rt[#rt + 1] = string.format( "%s: %s", serialize_any( k, bck ), serialize_any( v, bck ) ) end end return string.format( "{%s}", table.concat( rt, "," ) ) end elseif vtype == "string" then return string.format( "%q", val ) elseif vtype == "function" or vtype == "userdata" or vtype == "nil" then return "null" else return tostring( val ) end end function util.serializeJSON( val ) return serialize_any( val, {} ) end end function util.shared_buffer( name, max ) max = max or 64 return { _pos_name = name .. ".position", _list_name = name .. ".list.", push = function( self, text ) local cpos = GetInt( self._pos_name ) SetString( self._list_name .. (cpos % max), text ) SetInt( self._pos_name, cpos + 1 ) end, len = function( self ) return math.min( GetInt( self._pos_name ), max ) end, pos = function( self ) return GetInt( self._pos_name ) end, get = function( self, index ) local pos = GetInt( self._pos_name ) local len = math.min( pos, max ) if index >= len then return end return GetString( self._list_name .. (pos + index - len) % max ) end, get_g = function( self, index ) return GetString( self._list_name .. (index % max) ) end, clear = function( self ) SetInt( self._pos_name, 0 ) ClearKey( self._list_name:sub( 1, -2 ) ) end, } end function util.shared_channel( name, max, local_realm ) max = max or 64 local channel = { _buffer = util.shared_buffer( name, max ), _offset = 0, _hooks = {}, _ready_count = 0, _ready = {}, broadcast = function( self, ... ) return self:send( "", ... ) end, send = function( self, realm, ... ) self._buffer:push( string.format( ",%s,;%s", (type( realm ) == "table" and table.concat( realm, "," ) or tostring( realm )), util.serialize( ... ) ) ) end, listen = function( self, callback ) if self._ready[callback] ~= nil then return end self._hooks[#self._hooks + 1] = callback self:ready( callback ) return callback end, unlisten = function( self, callback ) self:unready( callback ) self._ready[callback] = nil for i = 1, #self._hooks do if self._hooks[i] == callback then table.remove( self._hooks, i ) return true end end end, ready = function( self, callback ) if not self._ready[callback] then self._ready_count = self._ready_count + 1 self._ready[callback] = true end end, unready = function( self, callback ) if self._ready[callback] then self._ready_count = self._ready_count - 1 self._ready[callback] = false end end, } local_realm = "," .. (local_realm or "unknown") .. "," local function receive( ... ) for i = 1, #channel._hooks do local f = channel._hooks[i] if channel._ready[f] then f( channel, ... ) end end end hook.add( "base.tick", name, function( dt ) if channel._ready_count > 0 then local last_pos = channel._buffer:pos() if last_pos > channel._offset then for i = math.max( channel._offset, last_pos - max ), last_pos - 1 do local message = channel._buffer:get_g( i ) local start = message:find( ";", 1, true ) local realms = message:sub( 1, start - 1 ) if realms == ",," or realms:find( local_realm, 1, true ) then receive( util.unserialize( message:sub( start + 1 ) ) ) if channel._ready_count <= 0 then channel._offset = i + 1 return end end end channel._offset = last_pos end end end ) return channel end function util.async_channel( channel ) local listener = { _channel = channel, _waiter = nil, read = function( self ) self._waiter = coroutine.running() if not self._waiter then error( "async_channel:read() can only be used in a coroutine" ) end self._channel:ready( self._handler ) return coroutine.yield() end, close = function( self ) if self._handler then self._channel:unlisten( self._handler ) end end, } listener._handler = listener._channel:listen( function( _, ... ) if listener._waiter then local co = listener._waiter listener._waiter = nil listener._channel:unready( listener._handler ) return coroutine.resume( co, ... ) end end ) listener._channel:unready( listener._handler ) return listener end do local gets, sets = {}, {} function util.register_unserializer( type, callback ) gets[type] = function( key ) return callback( GetString( key ) ) end end hook.add( "api.newmeta", "api.createunserializer", function( name, meta ) gets[name] = function( key ) return setmetatable( {}, meta ):__unserialize( GetString( key ) ) end sets[name] = function( key, value ) return SetString( key, meta.__serialize( value ) ) end end ) function util.shared_table( name, base ) return setmetatable( base or {}, { __index = function( self, k ) local key = tostring( k ) local vtype = GetString( string.format( "%s.%s.type", name, key ) ) if vtype == "" then return end return gets[vtype]( string.format( "%s.%s.val", name, key ) ) end, __newindex = function( self, k, v ) local vtype = type( v ) local handler = sets[vtype] if not handler then return end local key = tostring( k ) if vtype == "table" then local meta = getmetatable( v ) if meta and meta.__serialize and meta.__type then vtype = meta.__type v = meta.__serialize( v ) handler = sets.string end end SetString( string.format( "%s.%s.type", name, key ), vtype ) handler( string.format( "%s.%s.val", name, key ), v ) end, } ) end function util.structured_table( name, base ) local function generate( base ) local root = {} local keys = {} for k, v in pairs( base ) do local key = name .. "." .. tostring( k ) if type( v ) == "table" then root[k] = util.structured_table( key, v ) elseif type( v ) == "string" then keys[k] = { type = v, key = key } else root[k] = v end end return setmetatable( root, { __index = function( self, k ) local entry = keys[k] if entry and gets[entry.type] then return gets[entry.type]( entry.key ) end end, __newindex = function( self, k, v ) local entry = keys[k] if entry and sets[entry.type] then return sets[entry.type]( entry.key, v ) end end, } ) end if type( base ) == "table" then return generate( base ) end return generate end gets.number = GetFloat gets.integer = GetInt gets.boolean = GetBool gets.string = GetString gets.table = util.shared_table sets.number = SetFloat sets.integer = SetInt sets.boolean = SetBool sets.string = SetString sets.table = function( key, val ) local tab = util.shared_table( key ) for k, v in pairs( val ) do tab[k] = v end end end end)();
-(function() util = util or {} function util.current_line( level ) level = (level or 0) + 3 local _, line = pcall( error, "-", level ) if line == "-" then _, line = pcall( error, "-", level + 1 ) if line == "-" then return end line = "[C]:?" else line = line:sub( 1, -4 ) end return line end function util.stacktrace( start ) start = (start or 0) + 3 local stack, last = {}, nil for i = start, 32 do local _, line = pcall( error, "-", i ) if line == "-" then if last == "-" then break end else if last == "-" then stack[#stack + 1] = "[C]:?" end stack[#stack + 1] = line:sub( 1, -4 ) end last = line end return stack end end)();
-(function() local console_buffer = util.shared_buffer( "game.console", 128 ) local function maketext( ... ) local text = "" local len = select( "#", ... ) for i = 1, len do local s = tostring( select( i, ... ) ) if i < len then s = s .. string.rep( " ", 8 - #s % 8 ) end text = text .. s end return text end _OLDPRINT = _OLDPRINT or print function printcolor( r, g, b, ... ) local text = maketext( ... ) console_buffer:push( string.format( "%f;%f;%f;%s", r, g, b, text ) ) if PRINTTOSCREEN then DebugPrint( text ) end return _OLDPRINT( ... ) end function print( ... ) printcolor( 1, 1, 1, ... ) end function printinfo( ... ) printcolor( 0, .6, 1, ... ) end function warning( msg ) printcolor( 1, .7, 0, "[WARNING] " .. tostring( msg ) .. "\n " .. table.concat( util.stacktrace( 1 ), "\n " ) ) end printwarning = warning function printerror( ... ) printcolor( 1, .2, 0, ... ) end function clearconsole() console_buffer:clear() end function softassert( b, ... ) if not b then printerror( ... ) end return b, ... end function assert( b, msg, ... ) if not b then local m = msg or "Assertion failed" warning( m ) return error( m, ... ) end return b, msg, ... end end)();
-(function() GLOBAL_CHANNEL = util.shared_channel( "game.umf_global_channel", 128 ) end)();
-(function() local registered_meta = {} local reverse_meta = {} function global_metatable( name, parent ) local meta = registered_meta[name] if meta then if not parent then return meta end else meta = {} meta.__index = meta meta.__type = name registered_meta[name] = meta reverse_meta[meta] = name hook.saferun( "api.newmeta", name, meta ) end if parent then setmetatable( meta, global_metatable( parent ) ) end return meta end function find_global_metatable( name ) if not name then return end if type( name ) == "table" then return reverse_meta[name] end return registered_meta[name] end local function findmeta( src, found ) if found[src] then return end found[src] = true local res for k, v in pairs( src ) do if type( v ) == "table" then local dt local m = getmetatable( v ) if m then local name = reverse_meta[m] if name then dt = {} dt[1] = name end end local sub = findmeta( v, found ) if sub then dt = dt or {} dt[2] = sub end if dt then res = res or {} res[k] = dt end end end return res end local previous = -2 hook.add( "base.tick", "api.metatables.save", function( ... ) if GetTime() - previous > 2 then previous = GetTime() _G.GLOBAL_META_SAVE = findmeta( _G, {} ) end end ) local function restoremeta( dst, src ) for k, v in pairs( src ) do local dv = dst[k] if type( dv ) == "table" then if v[1] then setmetatable( dv, global_metatable( v[1] ) ) end if v[2] then restoremeta( dv, v[2] ) end end end end hook.add( "base.command.quickload", "api.metatables.restore", function( ... ) if GLOBAL_META_SAVE then restoremeta( _G, GLOBAL_META_SAVE ) end end ) end)();
-(function() local vector_meta = global_metatable( "vector" ) local quat_meta = global_metatable( "quaternion" ) function IsQuaternion( q ) return type( q ) == "table" and type( q[1] ) == "number" and type( q[2] ) == "number" and type( q[3] ) == "number" and type( q[4] ) == "number" end function MakeQuaternion( q ) return setmetatable( q, quat_meta ) end function Quaternion( i, j, k, r ) if IsQuaternion( i ) then i, j, k, r = i[1], i[2], i[3], i[4] end return MakeQuaternion { i or 0, j or 0, k or 0, r or 1 } end function quat_meta:__unserialize( data ) local i, j, k, r = data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*)" ) self[1] = tonumber( i ) self[2] = tonumber( j ) self[3] = tonumber( k ) self[4] = tonumber( r ) return self end function quat_meta:__serialize() return table.concat( self, ";" ) end QUAT_ZERO = Quaternion() function quat_meta:Clone() return MakeQuaternion { self[1], self[2], self[3], self[4] } end local QuatStr = QuatStr function quat_meta:__tostring() return QuatStr( self ) end function quat_meta:__unm() return MakeQuaternion { -self[1], -self[2], -self[3], -self[4] } end function quat_meta:Conjugate() return MakeQuaternion { -self[1], -self[2], -self[3], self[4] } end function quat_meta:Add( o ) if IsQuaternion( o ) then self[1] = self[1] + o[1] self[2] = self[2] + o[2] self[3] = self[3] + o[3] self[4] = self[4] + o[4] else self[1] = self[1] + o self[2] = self[2] + o self[3] = self[3] + o self[4] = self[4] + o end return self end function quat_meta.__add( a, b ) if not IsQuaternion( a ) then a, b = b, a end return quat_meta.Add( quat_meta.Clone( a ), b ) end function quat_meta:Sub( o ) if IsQuaternion( o ) then self[1] = self[1] - o[1] self[2] = self[2] - o[2] self[3] = self[3] - o[3] self[4] = self[4] - o[4] else self[1] = self[1] - o self[2] = self[2] - o self[3] = self[3] - o self[4] = self[4] - o end return self end function quat_meta.__sub( a, b ) if not IsQuaternion( a ) then a, b = b, a end return quat_meta.Sub( quat_meta.Clone( a ), b ) end function quat_meta:Mul( o ) local i1, j1, k1, r1 = self[1], self[2], self[3], self[4] local i2, j2, k2, r2 = o[1], o[2], o[3], o[4] self[1] = j1 * k2 - k1 * j2 + r1 * i2 + i1 * r2 self[2] = k1 * i2 - i1 * k2 + r1 * j2 + j1 * r2 self[3] = i1 * j2 - j1 * i2 + r1 * k2 + k1 * r2 self[4] = r1 * r2 - i1 * i2 - j1 * j2 - k1 * k2 return self end function quat_meta.__mul( a, b ) if not IsQuaternion( a ) then a, b = b, a end if type( b ) == "number" then return Quaternion( a[1] * b, a[2] * b, a[3] * b, a[4] * b ) end if IsVector( b ) then return vector_meta.__mul( b, a ) end if IsTransformation( b ) then return Transformation( vector_meta.Mul( vector_meta.Clone( b.pos ), a ), QuatRotateQuat( b.rot, a ) ) end return MakeQuaternion( QuatRotateQuat( a, b ) ) end function quat_meta:Div( o ) self[1] = self[1] / o self[2] = self[2] / o self[3] = self[3] / o self[4] = self[4] / o return self end function quat_meta.__div( a, b ) return quat_meta.Div( quat_meta.Clone( a ), b ) end function quat_meta.__eq( a, b ) return a[1] == b[1] and a[2] == b[2] and a[3] == b[3] and a[4] == b[4] end function quat_meta:LengthSquare() return self[1] ^ 2 + self[2] ^ 2 + self[3] ^ 2 + self[4] ^ 2 end function quat_meta:Length() return math.sqrt( quat_meta.LengthSquare( self ) ) end local QuatSlerp = QuatSlerp function quat_meta:Slerp( o, n ) return MakeQuaternion( QuatSlerp( self, o, n ) ) end function quat_meta:Left() local x, y, z, s = self[1], self[2], self[3], self[4] return Vector( 1 - (y ^ 2 + z ^ 2) * 2, (z * s + x * y) * 2, (x * z - y * s) * 2 ) end function quat_meta:Up() local x, y, z, s = self[1], self[2], self[3], self[4] return Vector( (y * x - z * s) * 2, 1 - (z ^ 2 + x ^ 2) * 2, (x * s + y * z) * 2 ) end function quat_meta:Forward() local x, y, z, s = self[1], self[2], self[3], self[4] return Vector( (y * s + z * x) * 2, (z * y - x * s) * 2, 1 - (x ^ 2 + y ^ 2) * 2 ) end function quat_meta:ToEuler() if GetQuatEuler then return GetQuatEuler( self ) end local x, y, z, w = self[1], self[2], self[3], self[4] local bank, heading, attitude local s = 2 * x * y + 2 * z * w if s >= 1 then heading = 2 * math.atan2( x, w ) bank = 0 attitude = math.pi / 2 elseif s <= -1 then heading = -2 * math.atan2( x, w ) bank = 0 attitude = math.pi / -2 else bank = math.atan2( 2 * x * w - 2 * y * z, 1 - 2 * x ^ 2 - 2 * z ^ 2 ) heading = math.atan2( 2 * y * w - 2 * x * z, 1 - 2 * y ^ 2 - 2 * z ^ 2 ) attitude = math.asin( s ) end return math.deg( bank ), math.deg( heading ), math.deg( attitude ) end function quat_meta:Approach( dest, rate ) local dot = self[1] * dest[1] + self[2] * dest[2] + self[3] * dest[3] + self[4] * dest[4] if dot >= 1 then return self end local corr_rate = rate / math.acos( 2 * dot ^ 2 - 1 ) if corr_rate >= 1 then return MakeQuaternion( dest ) end return MakeQuaternion( QuatSlerp( self, dest, corr_rate ) ) end end)();
-(function() local vector_meta = global_metatable( "vector" ) local quat_meta = global_metatable( "quaternion" ) local transform_meta = global_metatable( "transformation" ) function IsTransformation( t ) return type( t ) == "table" and t.pos and t.rot end function MakeTransformation( t ) setmetatable( t.pos, vector_meta ) setmetatable( t.rot, quat_meta ) return setmetatable( t, transform_meta ) end function Transformation( pos, rot ) return MakeTransformation { pos = pos, rot = rot } end function transform_meta:__unserialize( data ) local x, y, z, i, j, k, r = data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*);([-0-9.]*)" ) self.pos = Vector( tonumber( x ), tonumber( y ), tonumber( z ) ) self.rot = Quaternion( tonumber( i ), tonumber( j ), tonumber( k ), tonumber( r ) ) return self end function transform_meta:__serialize() return table.concat( self.pos, ";" ) .. ";" .. table.concat( self.rot, ";" ) end function transform_meta:Clone() return MakeTransformation { pos = vector_meta.Clone( self.pos ), rot = quat_meta.Clone( self.rot ) } end local TransformStr = TransformStr function transform_meta:__tostring() return TransformStr( self ) end local TransformToLocalPoint = TransformToLocalPoint local TransformToLocalTransform = TransformToLocalTransform local TransformToLocalVec = TransformToLocalVec local TransformToParentPoint = TransformToParentPoint local TransformToParentTransform = TransformToParentTransform local TransformToParentVec = TransformToParentVec function transform_meta.__add( a, b ) if not IsTransformation( b ) then if IsVector( b ) then b = Transformation( b, QUAT_ZERO ) elseif IsQuaternion( b ) then b = Transformation( VEC_ZERO, b ) end end return MakeTransformation( TransformToParentTransform( a, b ) ) end function transform_meta:ToLocal( o ) if IsTransformation( o ) then return MakeTransformation( TransformToLocalTransform( self, o ) ) elseif IsQuaternion( o ) then return MakeQuaternion( TransformToLocalTransform( self, Transform( {}, o ) ).rot ) else return MakeVector( TransformToLocalPoint( self, o ) ) end end function transform_meta:ToLocalDir( o ) return MakeVector( TransformToLocalVec( self, o ) ) end function transform_meta:ToGlobal( o ) if IsTransformation( o ) then return MakeTransformation( TransformToParentTransform( self, o ) ) elseif IsQuaternion( o ) then return MakeQuaternion( TransformToParentTransform( self, Transform( {}, o ) ).rot ) else return MakeVector( TransformToParentPoint( self, o ) ) end end function transform_meta:ToGlobalDir( o ) return MakeVector( TransformToParentVec( self, o ) ) end function transform_meta:Raycast( dist, mul, radius, rejectTransparent ) local dir = TransformToParentVec( self, VEC_FORWARD ) if mul then vector_meta.Mul( dir, mul ) end local hit, dist2, normal, shape = QueryRaycast( self.pos, dir, dist, radius, rejectTransparent ) return { hit = hit, dist = dist2, normal = hit and MakeVector( normal ), shape = hit and Shape and Shape( shape ) or shape, hitpos = vector_meta.__add( self.pos, vector_meta.Mul( dir, hit and dist2 or dist ) ), } end end)();
-(function() local vector_meta = global_metatable( "vector" ) local quat_meta = global_metatable( "quaternion" ) function IsVector( v ) return type( v ) == "table" and type( v[1] ) == "number" and type( v[2] ) == "number" and type( v[3] ) == "number" and not v[4] end function MakeVector( v ) return setmetatable( v, vector_meta ) end function Vector( x, y, z ) if IsVector( x ) then x, y, z = x[1], x[2], x[3] end return MakeVector { x or 0, y or 0, z or 0 } end function vector_meta:__unserialize( data ) local x, y, z = data:match( "([-0-9.]*);([-0-9.]*);([-0-9.]*)" ) self[1] = tonumber( x ) self[2] = tonumber( y ) self[3] = tonumber( z ) return self end function vector_meta:__serialize() return table.concat( self, ";" ) end VEC_ZERO = Vector() VEC_FORWARD = Vector( 0, 0, 1 ) VEC_UP = Vector( 0, 1, 0 ) VEC_LEFT = Vector( 1, 0, 0 ) function vector_meta:Clone() return MakeVector { self[1], self[2], self[3] } end local VecStr = VecStr function vector_meta:__tostring() return VecStr( self ) end function vector_meta:__unm() return MakeVector { -self[1], -self[2], -self[3] } end function vector_meta:Add( o ) if IsVector( o ) then self[1] = self[1] + o[1] self[2] = self[2] + o[2] self[3] = self[3] + o[3] else self[1] = self[1] + o self[2] = self[2] + o self[3] = self[3] + o end return self end function vector_meta.__add( a, b ) if not IsVector( a ) then a, b = b, a end if IsTransformation( b ) then return Transformation( vector_meta.Add( vector_meta.Clone( a ), b.pos ), quat_meta.Clone( b.rot ) ) end return vector_meta.Add( vector_meta.Clone( a ), b ) end function vector_meta:Sub( o ) if IsVector( o ) then self[1] = self[1] - o[1] self[2] = self[2] - o[2] self[3] = self[3] - o[3] else self[1] = self[1] - o self[2] = self[2] - o self[3] = self[3] - o end return self end function vector_meta.__sub( a, b ) if not IsVector( a ) then a, b = b, a end return vector_meta.Sub( vector_meta.Clone( a ), b ) end function vector_meta:Mul( o ) if IsVector( o ) then self[1] = self[1] * o[1] self[2] = self[2] * o[2] self[3] = self[3] * o[3] elseif IsQuaternion( o ) then local x1, y1, z1 = self[1], self[2], self[3] local x2, y2, z2, s = o[1], o[2], o[3], o[4] local x3 = y2 * z1 - z2 * y1 local y3 = z2 * x1 - x2 * z1 local z3 = x2 * y1 - y2 * x1 self[1] = x1 + (x3 * s + y2 * z3 - z2 * y3) * 2 self[2] = y1 + (y3 * s + z2 * x3 - x2 * z3) * 2 self[3] = z1 + (z3 * s + x2 * y3 - y2 * x3) * 2 else self[1] = self[1] * o self[2] = self[2] * o self[3] = self[3] * o end return self end function vector_meta.__mul( a, b ) if not IsVector( a ) then a, b = b, a end return vector_meta.Mul( vector_meta.Clone( a ), b ) end function vector_meta:Div( o ) self[1] = self[1] / o self[2] = self[2] / o self[3] = self[3] / o return self end function vector_meta.__div( a, b ) return vector_meta.Div( vector_meta.Clone( a ), b ) end function vector_meta:Mod( o ) self[1] = self[1] % o self[2] = self[2] % o self[3] = self[3] % o return self end function vector_meta.__mod( a, b ) return vector_meta.Mod( vector_meta.Clone( a ), b ) end function vector_meta:Pow( o ) self[1] = self[1] ^ o self[2] = self[2] ^ o self[3] = self[3] ^ o return self end function vector_meta.__pow( a, b ) return vector_meta.Pow( vector_meta.Clone( a ), b ) end function vector_meta.__eq( a, b ) return a[1] == b[1] and a[2] == b[2] and a[3] == b[3] end function vector_meta.__lt( a, b ) return a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and (a[3] < b[3])))) end function vector_meta.__le( a, b ) return a[1] < b[1] or (a[1] == b[1] and (a[2] < b[2] or (a[2] == b[2] and (a[3] <= b[3])))) end local VecDot = VecDot function vector_meta:Dot( b ) return VecDot( self, b ) end local VecCross = VecCross function vector_meta:Cross( b ) return MakeVector( VecCross( self, b ) ) end local VecLength = VecLength function vector_meta:Length() return VecLength( self ) end function vector_meta:Volume() return math.abs( self[1] * self[2] * self[3] ) end local VecLerp = VecLerp function vector_meta:Lerp( o, n ) return MakeVector( VecLerp( self, o, n ) ) end local VecNormalize = VecNormalize function vector_meta:Normalized() return MakeVector( VecNormalize( self ) ) end function vector_meta:Normalize() return vector_meta.Div( self, vector_meta.Length( self ) ) end function vector_meta:DistSquare( o ) return (self[1] - o[1]) ^ 2 + (self[2] - o[2]) ^ 2 + (self[3] - o[3]) ^ 2 end function vector_meta:Distance( o ) return math.sqrt( vector_meta.DistSquare( self, o ) ) end function vector_meta:LookAt( o ) return MakeQuaternion( QuatLookAt( self, o ) ) end function vector_meta:Approach( dest, rate ) local dist = vector_meta.Distance( self, dest ) if dist < rate then return dest end return vector_meta.Lerp( self, dest, rate / dist ) end end)();
-(function() local entity_meta = global_metatable( "entity" ) function GetEntityHandle( e ) if IsEntity( e ) then return e.handle end return e end function IsValid( e ) if type( e ) == "table" and e.IsValid then return e:IsValid() end return false end function IsEntity( e ) return type( e ) == "table" and type( e.handle ) == "number" end function Entity( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "unknown" }, entity_meta ) end end function entity_meta:__unserialize( data ) self.handle = tonumber( data ) return self end function entity_meta:__serialize() return tostring( self.handle ) end function entity_meta:__tostring() return string.format( "Entity[%d]", self.handle ) end function entity_meta:GetType() return self.type or "unknown" end local IsHandleValid = IsHandleValid function entity_meta:IsValid() return IsHandleValid( self.handle ) end local SetTag = SetTag function entity_meta:SetTag( tag, value ) assert( self:IsValid() ) return SetTag( self.handle, tag, value ) end local SetDescription = SetDescription function entity_meta:SetDescription( description ) assert( self:IsValid() ) return SetDescription( self.handle, description ) end local RemoveTag = RemoveTag function entity_meta:RemoveTag( tag ) assert( self:IsValid() ) return RemoveTag( self.handle, tag ) end local HasTag = HasTag function entity_meta:HasTag( tag ) assert( self:IsValid() ) return HasTag( self.handle, tag ) end local GetTagValue = GetTagValue function entity_meta:GetTagValue( tag ) assert( self:IsValid() ) return GetTagValue( self.handle, tag ) end local GetDescription = GetDescription function entity_meta:GetDescription() assert( self:IsValid() ) return GetDescription( self.handle ) end local Delete = Delete function entity_meta:Delete() return Delete( self.handle ) end end)();
-(function() local body_meta = global_metatable( "body", "entity" ) function IsBody( e ) return IsEntity( e ) and e.type == "body" end function Body( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "body" }, body_meta ) end end function FindBodyByTag( tag, global ) return Body( FindBody( tag, global ) ) end function FindBodiesByTag( tag, global ) local t = FindBodies( tag, global ) for i = 1, #t do t[i] = Body( t[i] ) end return t end function body_meta:__tostring() return string.format( "Body[%d]", self.handle ) end function body_meta:ApplyImpulse( pos, vel ) assert( self:IsValid() ) return ApplyBodyImpulse( self.handle, pos, vel ) end function body_meta:ApplyLocalImpulse( pos, vel ) local transform = self:GetTransform() return self:ApplyImpulse( transform:ToGlobal( pos ), transform:ToGlobalDir( vel ) ) end function body_meta:DrawOutline( r, ... ) assert( self:IsValid() ) return DrawBodyOutline( self.handle, r, ... ) end function body_meta:DrawHighlight( amount ) assert( self:IsValid() ) return DrawBodyHighlight( self.handle, amount ) end function body_meta:SetTransform( tr ) assert( self:IsValid() ) return SetBodyTransform( self.handle, tr ) end function body_meta:SetDynamic( bool ) assert( self:IsValid() ) return SetBodyDynamic( self.handle, bool ) end function body_meta:SetVelocity( vel ) assert( self:IsValid() ) return SetBodyVelocity( self.handle, vel ) end function body_meta:SetAngularVelocity( avel ) assert( self:IsValid() ) return SetBodyAngularVelocity( self.handle, avel ) end function body_meta:GetTransform() assert( self:IsValid() ) return MakeTransformation( GetBodyTransform( self.handle ) ) end function body_meta:GetMass() assert( self:IsValid() ) return GetBodyMass( self.handle ) end function body_meta:GetVelocity() assert( self:IsValid() ) return MakeVector( GetBodyVelocity( self.handle ) ) end function body_meta:GetVelocityAtPos( pos ) assert( self:IsValid() ) return MakeVector( GetBodyVelocityAtPos( self.handle, pos ) ) end function body_meta:GetAngularVelocity() assert( self:IsValid() ) return MakeVector( GetBodyAngularVelocity( self.handle ) ) end function body_meta:GetShapes() assert( self:IsValid() ) local shapes = GetBodyShapes( self.handle ) for i = 1, #shapes do shapes[i] = Shape( shapes[i] ) end return shapes end function body_meta:GetVehicle() assert( self:IsValid() ) return Vehicle( GetBodyVehicle( self.handle ) ) end function body_meta:GetWorldBounds() assert( self:IsValid() ) local min, max = GetBodyBounds( self.handle ) return MakeVector( min ), MakeVector( max ) end function body_meta:GetLocalCenterOfMass() assert( self:IsValid() ) return MakeVector( GetBodyCenterOfMass( self.handle ) ) end function body_meta:GetWorldCenterOfMass() return self:GetTransform():ToGlobal( self:GetLocalCenterOfMass() ) end function body_meta:IsActive() assert( self:IsValid() ) return IsBodyActive( self.handle ) end function body_meta:IsDynamic() assert( self:IsValid() ) return IsBodyDynamic( self.handle ) end function body_meta:IsVisible( maxdist ) assert( self:IsValid() ) return IsBodyVisible( self.handle, maxdist ) end function body_meta:IsBroken() return not self:IsValid() or IsBodyBroken( self.handle ) end function body_meta:IsJointedToStatic() assert( self:IsValid() ) return IsBodyJointedToStatic( self.handle ) end end)();
-(function() local joint_meta = global_metatable( "joint", "entity" ) function IsJoint( e ) return IsEntity( e ) and e.type == "joint" end function Joint( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "joint" }, joint_meta ) end end function FindJointByTag( tag, global ) return Joint( FindJoint( tag, global ) ) end function FindJointsByTag( tag, global ) local t = FindJoints( tag, global ) for i = 1, #t do t[i] = Joint( t[i] ) end return t end function joint_meta:__tostring() return string.format( "Joint[%d]", self.handle ) end function joint_meta:SetMotor( velocity, strength ) assert( self:IsValid() ) return SetJointMotor( self.handle, velocity, strength ) end function joint_meta:SetMotorTarget( target, maxVel, strength ) assert( self:IsValid() ) return SetJointMotorTarget( self.handle, target, maxVel, strength ) end function joint_meta:GetJointType() assert( self:IsValid() ) return GetJointType( self.handle ) end function joint_meta:GetOtherShape( shape ) assert( self:IsValid() ) return Shape( GetJointOtherShape( self.handle, GetEntityHandle( shape ) ) ) end function joint_meta:GetLimits() assert( self:IsValid() ) return GetJointLimits( self.handle ) end function joint_meta:GetMovement() assert( self:IsValid() ) return GetJointMovement( self.handle ) end function joint_meta:IsBroken() return not self:IsValid() or IsJointBroken( self.handle ) end end)();
-(function() local light_meta = global_metatable( "light", "entity" ) function IsLight( e ) return IsEntity( e ) and e.type == "light" end function Light( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "light" }, light_meta ) end end function FindLightByTag( tag, global ) return Light( FindLight( tag, global ) ) end function FindLightsByTag( tag, global ) local t = FindLights( tag, global ) for i = 1, #t do t[i] = Light( t[i] ) end return t end function light_meta:__tostring() return string.format( "Light[%d]", self.handle ) end function light_meta:SetEnabled( enabled ) assert( self:IsValid() ) return SetLightEnabled( self.handle, enabled ) end function light_meta:SetColor( r, g, b ) assert( self:IsValid() ) return SetLightColor( self.handle, r, g, b ) end function light_meta:SetIntensity( intensity ) assert( self:IsValid() ) return SetLightIntensity( self.handle, intensity ) end function light_meta:GetTransform() assert( self:IsValid() ) return MakeTransformation( GetLightTransform( self.handle ) ) end function light_meta:GetShape() assert( self:IsValid() ) return Shape( GetLightShape( self.handle ) ) end function light_meta:IsActive() assert( self:IsValid() ) return IsLightActive( self.handle ) end function light_meta:IsPointAffectedByLight( point ) assert( self:IsValid() ) return IsPointAffectedByLight( self.handle, point ) end end)();
-(function() local location_meta = global_metatable( "location", "entity" ) function IsLocation( e ) return IsEntity( e ) and e.type == "location" end function Location( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "location" }, location_meta ) end end function FindLocationByTag( tag, global ) return Location( FindLocation( tag, global ) ) end function FindLocationsByTag( tag, global ) local t = FindLocations( tag, global ) for i = 1, #t do t[i] = Location( t[i] ) end return t end function location_meta:__tostring() return string.format( "Location[%d]", self.handle ) end function location_meta:GetTransform() assert( self:IsValid() ) return MakeTransformation( GetLocationTransform( self.handle ) ) end end)();
-(function() local player_meta = global_metatable( "player" ) PLAYER = setmetatable( {}, player_meta ) function player_meta:__unserialize( data ) return self end function player_meta:__serialize() return "" end function player_meta:__tostring() return string.format( "Player" ) end function player_meta:GetType() return "player" end function player_meta:Respawn() return RespawnPlayer() end function player_meta:SetTransform( transform ) return SetPlayerTransform( transform ) end function player_meta:SetCamera( transform ) return SetCameraTransform( transform ) end function player_meta:SetSpawnTransform( transform ) return SetPlayerSpawnTransform( transform ) end function player_meta:SetVehicle( handle ) return SetPlayerVehicle( GetEntityHandle( handle ) ) end function player_meta:SetVelocity( velocity ) return SetPlayerVelocity( velocity ) end function player_meta:SetScreen( handle ) return SetPlayerScreen( GetEntityHandle( handle ) ) end function player_meta:SetHealth( health ) return SetPlayerHealth( health ) end function player_meta:GetTransform() return MakeTransformation( GetPlayerTransform() ) end function player_meta:GetPlayerCamera() return MakeTransformation( GetPlayerCameraTransform() ) end function player_meta:GetCamera() return MakeTransformation( GetCameraTransform() ) end function player_meta:GetVelocity() return MakeVector( GetPlayerVelocity() ) end function player_meta:GetVehicle() return Vehicle( GetPlayerVehicle() ) end function player_meta:GetGrabShape() return Shape( GetPlayerGrabShape() ) end function player_meta:GetGrabBody() return Body( GetPlayerGrabBody() ) end function player_meta:GetPickShape() return Shape( GetPlayerPickShape() ) end function player_meta:GetPickBody() return Body( GetPlayerPickBody() ) end function player_meta:GetInteractShape() return Shape( GetPlayerInteractShape() ) end function player_meta:GetInteractBody() return Body( GetPlayerInteractBody() ) end function player_meta:GetScreen() return Screen( GetPlayerScreen() ) end function player_meta:GetHealth() return GetPlayerHealth() end end)();
-(function() local screen_meta = global_metatable( "screen", "entity" ) function IsScreen( e ) return IsEntity( e ) and e.type == "screen" end function Screen( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "screen" }, screen_meta ) end end function FindScreenByTag( tag, global ) return Screen( FindScreen( tag, global ) ) end function FindScreensByTag( tag, global ) local t = FindScreens( tag, global ) for i = 1, #t do t[i] = Screen( t[i] ) end return t end function screen_meta:__tostring() return string.format( "Screen[%d]", self.handle ) end function screen_meta:SetEnabled( enabled ) assert( self:IsValid() ) return SetScreenEnabled( self.handle, enabled ) end function screen_meta:GetShape() assert( self:IsValid() ) return Shape( GetScreenShape( self.handle ) ) end function screen_meta:IsEnabled() assert( self:IsValid() ) return IsScreenEnabled( self.handle ) end end)();
-(function() local shape_meta = global_metatable( "shape", "entity" ) function IsShape( e ) return IsEntity( e ) and e.type == "shape" end function Shape( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "shape" }, shape_meta ) end end function FindShapeByTag( tag, global ) return Shape( FindShape( tag, global ) ) end function FindShapesByTag( tag, global ) local t = FindShapes( tag, global ) for i = 1, #t do t[i] = Shape( t[i] ) end return t end function shape_meta:__tostring() return string.format( "Shape[%d]", self.handle ) end function shape_meta:DrawOutline( r, ... ) assert( self:IsValid() ) return DrawShapeOutline( self.handle, r, ... ) end function shape_meta:DrawHighlight( amount ) assert( self:IsValid() ) return DrawShapeHighlight( self.handle, amount ) end function shape_meta:SetLocalTransform( transform ) assert( self:IsValid() ) return SetShapeLocalTransform( self.handle, transform ) end function shape_meta:SetEmissiveScale( scale ) assert( self:IsValid() ) return SetShapeEmissiveScale( self.handle, scale ) end function shape_meta:GetLocalTransform() assert( self:IsValid() ) return MakeTransformation( GetShapeLocalTransform( self.handle ) ) end function shape_meta:GetWorldTransform() assert( self:IsValid() ) return MakeTransformation( GetShapeWorldTransform( self.handle ) ) end function shape_meta:GetBody() assert( self:IsValid() ) return Body( GetShapeBody( self.handle ) ) end function shape_meta:GetJoints() assert( self:IsValid() ) local joints = GetShapeJoints( self.handle ) for i = 1, #joints do joints[i] = Joint( joints[i] ) end return joints end function shape_meta:GetLights() assert( self:IsValid() ) local lights = GetShapeLights( self.handle ) for i = 1, #lights do lights[i] = Light( lights[i] ) end return lights end function shape_meta:GetWorldBounds() assert( self:IsValid() ) local min, max = GetShapeBounds( self.handle ) return MakeVector( min ), MakeVector( max ) end function shape_meta:GetMaterialAtPos( pos ) assert( self:IsValid() ) return GetShapeMaterialAtPosition( self.handle, pos ) end function shape_meta:GetSize() assert( self:IsValid() ) return GetShapeSize( self.handle ) end function shape_meta:GetVoxelCount() assert( self:IsValid() ) return GetShapeVoxelCount( self.handle ) end function shape_meta:IsVisible( maxDist, rejectTransparent ) assert( self:IsValid() ) return IsShapeVisible( self.handle, maxDist, rejectTransparent ) end function shape_meta:IsBroken() return not self:IsValid() or IsShapeBroken( self.handle ) end end)();
-(function() local trigger_meta = global_metatable( "trigger", "entity" ) function IsTrigger( e ) return IsEntity( e ) and e.type == "trigger" end function Trigger( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "trigger" }, trigger_meta ) end end function FindTriggerByTag( tag, global ) return Trigger( FindTrigger( tag, global ) ) end function FindTriggersByTag( tag, global ) local t = FindTriggers( tag, global ) for i = 1, #t do t[i] = Trigger( t[i] ) end return t end function trigger_meta:__tostring() return string.format( "Trigger[%d]", self.handle ) end function trigger_meta:SetTransform( transform ) assert( self:IsValid() ) return SetTriggerTransform( self.handle, transform ) end function trigger_meta:GetTransform() assert( self:IsValid() ) return MakeTransformation( GetTriggerTransform( self.handle ) ) end function trigger_meta:GetWorldBounds() assert( self:IsValid() ) local min, max = GetTriggerBounds( self.handle ) return MakeVector( min ), MakeVector( max ) end function trigger_meta:IsBodyInTrigger( handle ) assert( self:IsValid() ) return IsBodyInTrigger( self.handle, GetEntityHandle( handle ) ) end function trigger_meta:IsVehicleInTrigger( handle ) assert( self:IsValid() ) return IsVehicleInTrigger( self.handle, GetEntityHandle( handle ) ) end function trigger_meta:IsShapeInTrigger( handle ) assert( self:IsValid() ) return IsShapeInTrigger( self.handle, GetEntityHandle( handle ) ) end function trigger_meta:IsPointInTrigger( point ) assert( self:IsValid() ) return IsPointInTrigger( self.handle, point ) end function trigger_meta:IsEmpty( demolision ) assert( self:IsValid() ) local empty, highpoint = IsTriggerEmpty( self.handle, demolision ) return empty, highpoint and MakeVector( highpoint ) end end)();
-(function() local vehicle_meta = global_metatable( "vehicle", "entity" ) function IsVehicle( e ) return IsEntity( e ) and e.type == "vehicle" end function Vehicle( handle ) if handle > 0 then return setmetatable( { handle = handle, type = "vehicle" }, vehicle_meta ) end end function FindVehicleByTag( tag, global ) return Vehicle( FindVehicle( tag, global ) ) end function FindVehiclesByTag( tag, global ) local t = FindVehicles( tag, global ) for i = 1, #t do t[i] = Vehicle( t[i] ) end return t end function vehicle_meta:__tostring() return string.format( "Vehicle[%d]", self.handle ) end function vehicle_meta:Drive( drive, steering, handbrake ) assert( self:IsValid() ) return DriveVehicle( self.handle, drive, steering, handbrake ) end function vehicle_meta:GetTransform() assert( self:IsValid() ) return MakeTransformation( GetVehicleTransform( self.handle ) ) end function vehicle_meta:GetBody() assert( self:IsValid() ) return Body( GetVehicleBody( self.handle ) ) end function vehicle_meta:GetHealth() assert( self:IsValid() ) return GetVehicleHealth( self.handle ) end function vehicle_meta:GetDriverPos() assert( self:IsValid() ) return MakeVector( GetVehicleDriverPos( self.handle ) ) end function vehicle_meta:GetGlobalDriverPos() return self:GetTransform():ToGlobal( self:GetDriverPos() ) end end)();
-for i = 1, #__RUNLATER do local f = loadstring(__RUNLATER[i]) if f then pcall(f) end end
+#version 2
+local __RUNLATER = {}
+

```

---

# Migration Report: main\umf\umf_utils.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\umf\umf_utils.lua
+++ patched/main\umf\umf_utils.lua
@@ -1,14 +1,3 @@
-local __RUNLATER = {} UMF_RUNLATER = function(code) __RUNLATER[#__RUNLATER + 1] = code end
-(function() util = util or {} function util.current_line( level ) level = (level or 0) + 3 local _, line = pcall( error, "-", level ) if line == "-" then _, line = pcall( error, "-", level + 1 ) if line == "-" then return end line = "[C]:?" else line = line:sub( 1, -4 ) end return line end function util.stacktrace( start ) start = (start or 0) + 3 local stack, last = {}, nil for i = start, 32 do local _, line = pcall( error, "-", i ) if line == "-" then if last == "-" then break end else if last == "-" then stack[#stack + 1] = "[C]:?" end stack[#stack + 1] = line:sub( 1, -4 ) end last = line end return stack end end)();
-(function() local original = {} local function call_original( name, ... ) local fn = original[name] if fn then return fn( ... ) end end local detoured = {} function DETOUR( name, generator ) original[name] = _G[name] detoured[name] = generator( function( ... ) return call_original( name, ... ) end ) rawset( _G, name, nil ) end setmetatable( _G, { __index = detoured, __newindex = function( self, k, v ) if detoured[k] then original[k] = v else rawset( self, k, v ) end end, } ) end)();
-(function() if hook then return end local hook_table = {} local hook_compiled = {} local function recompile( event ) local hooks = {} for k, v in pairs( hook_table[event] ) do hooks[#hooks + 1] = v end hook_compiled[event] = hooks end hook = { table = hook_table } function hook.add( event, identifier, func ) assert( type( event ) == "string", "Event must be a string" ) if func then assert( identifier ~= nil, "Identifier must not be nil" ) assert( type( func ) == "function", "Callback must be a function" ) else assert( type( identifier ) == "function", "Callback must be a function" ) end hook_table[event] = hook_table[event] or {} hook_table[event][identifier] = func or identifier recompile( event ) return identifier end function hook.remove( event, identifier ) assert( type( event ) == "string", "Event must be a string" ) assert( identifier ~= nil, "Identifier must not be nil" ) if hook_table[event] then hook_table[event][identifier] = nil if next( hook_table[event] ) == nil then hook_table[event] = nil hook_compiled[event] = nil else recompile( event ) end end end function hook.run( event, ... ) local hooks = hook_compiled[event] if not hooks then return end for i = 1, #hooks do local a, b, c, d, e = hooks[i]( ... ) if a ~= nil then return a, b, c, d, e end end end function hook.saferun( event, ... ) local hooks = hook_compiled[event] if not hooks then return end for i = 1, #hooks do local s, a, b, c, d, e = softassert( pcall( hooks[i], ... ) ) if s and a ~= nil then return a, b, c, d, e end end end function hook.used( event ) return hook_table[event] end end)();
-(function() UMF_RUNLATER "UpdateQuickloadPatch()" local hook = hook local function checkoriginal( b, ... ) if not b then printerror( ... ) return end return ... end local function simple_detour( name ) local event = "base." .. name DETOUR( name, function( original ) return function( ... ) hook.saferun( event, ... ) return checkoriginal( pcall( original, ... ) ) end end ) end local detours = { "init", "tick", "update", } for i = 1, #detours do simple_detour( detours[i] ) end function shoulddraw( kind ) return hook.saferun( "api.shoulddraw", kind ) ~= false end DETOUR( "draw", function( original ) return function( dt ) if shoulddraw( "all" ) then hook.saferun( "base.predraw", dt ) if shoulddraw( "original" ) then checkoriginal( pcall( original, dt ) ) end hook.saferun( "base.draw", dt ) end end end ) DETOUR( "Command", function( original ) return function( cmd, ... ) hook.saferun( "base.precmd", cmd, { ... } ) local a, b, c, d, e, f = original( cmd, ... ) hook.saferun( "base.postcmd", cmd, { ... }, { a, b, c, d, e, f } ) end end ) local saved = {} local function hasfunction( t, bck ) if bck[t] then return end bck[t] = true for k, v in pairs( t ) do if type( v ) == "function" then return true end if type( v ) == "table" and hasfunction( v, bck ) then return true end end end function UpdateQuickloadPatch() for k, v in pairs( _G ) do if k ~= "_G" and type( v ) == "table" and hasfunction( v, {} ) then saved[k] = v end end end local quickloadfix = function() for k, v in pairs( saved ) do _G[k] = v end end DETOUR( "handleCommand", function( original ) return function( command, ... ) if command == "quickload" then quickloadfix() end hook.saferun( "base.command." .. command, ... ) return original( command, ... ) end end ) hook.add( "base.tick", "api.firsttick", function() hook.remove( "base.tick", "api.firsttick" ) hook.saferun( "api.firsttick" ) if type( firsttick ) == "function" then firsttick() end end ) end)();
-(function() function IsPlayerInVehicle() return GetBool( "game.player.usevehicle" ) end local tool = GetString( "game.player.tool" ) local invehicle = IsPlayerInVehicle() local keyboardkeys = { "esc", "up", "down", "left", "right", "space", "interact", "return" } for i = 97, 97 + 25 do keyboardkeys[#keyboardkeys + 1] = string.char( i ) end local function checkkeys( func, mousehook, keyhook ) if hook.used( keyhook ) and func( "any" ) then for i = 1, #keyboardkeys do if func( keyboardkeys[i] ) then hook.saferun( keyhook, keyboardkeys[i] ) end end end if hook.used( mousehook ) then if func( "lmb" ) then hook.saferun( mousehook, "lmb" ) end if func( "rmb" ) then hook.saferun( mousehook, "rmb" ) end end end local mousekeys = { "lmb", "rmb", "mmb" } local heldkeys = {} hook.add( "base.tick", "api.default_hooks", function() if InputLastPressedKey then for i = 1, #mousekeys do local k = mousekeys[i] if InputPressed( k ) then hook.saferun( "api.mouse.pressed", k ) elseif InputReleased( k ) then hook.saferun( "api.mouse.released", k ) end end local lastkey = InputLastPressedKey() if lastkey ~= "" then heldkeys[lastkey] = true hook.saferun( "api.key.pressed", lastkey ) end for key in pairs( heldkeys ) do if not InputDown( key ) then heldkeys[key] = nil hook.saferun( "api.key.released", key ) break end end local wheel = InputValue( "mousewheel" ) if wheel ~= 0 then hook.saferun( "api.mouse.wheel", wheel ) end local mousedx = InputValue( "mousedx" ) local mousedy = InputValue( "mousedy" ) if mousedx ~= 0 or mousedy ~= 0 then hook.saferun( "api.mouse.move", mousedx, mousedy ) end elseif InputPressed then checkkeys( InputPressed, "api.mouse.pressed", "api.key.pressed" ) checkkeys( InputReleased, "api.mouse.released", "api.key.released" ) local wheel = InputValue( "mousewheel" ) if wheel ~= 0 then hook.saferun( "api.mouse.wheel", wheel ) end local mousedx = InputValue( "mousedx" ) local mousedy = InputValue( "mousedy" ) if mousedx ~= 0 or mousedy ~= 0 then hook.saferun( "api.mouse.move", mousedx, mousedy ) end end local n_invehicle = IsPlayerInVehicle() if invehicle ~= n_invehicle then hook.saferun( n_invehicle and "api.player.enter_vehicle" or "api.player.exit_vehicle", n_invehicle and GetPlayerVehicle() ) invehicle = n_invehicle end local n_tool = GetString( "game.player.tool" ) if tool ~= n_tool then hook.saferun( "api.player.switch_tool", n_tool, tool ) tool = n_tool end end ) end)();
-(function() util = util or {} do local serialize_any, serialize_table serialize_table = function( val, bck ) if bck[val] then return "nil" end bck[val] = true local entries = {} for k, v in pairs( val ) do entries[#entries + 1] = string.format( "[%s] = %s", serialize_any( k, bck ), serialize_any( v, bck ) ) end return string.format( "{%s}", table.concat( entries, "," ) ) end serialize_any = function( val, bck ) local vtype = type( val ) if vtype == "table" then return serialize_table( val, bck ) elseif vtype == "string" then return string.format( "%q", val ) elseif vtype == "function" or vtype == "userdata" then return string.format( "nil ", tostring( val ) ) else return tostring( val ) end end function util.serialize( ... ) local result = {} for i = 1, select( "#", ... ) do result[i] = serialize_any( select( i, ... ), {} ) end return table.concat( result, "," ) end end function util.unserialize( dt ) local fn = loadstring( "return " .. dt ) if fn then setfenv( fn, {} ) return fn() end end do local function serialize_any( val, bck ) local vtype = type( val ) if vtype == "table" then if bck[val] then return "{}" end bck[val] = true local len = 0 for k, v in pairs( val ) do len = len + 1 end local rt = {} if len == #val then for i = 1, #val do rt[i] = serialize_any( val[i], bck ) end return string.format( "[%s]", table.concat( rt, "," ) ) else for k, v in pairs( val ) do if type( k ) == "string" or type( k ) == "number" then rt[#rt + 1] = string.format( "%s: %s", serialize_any( k, bck ), serialize_any( v, bck ) ) end end return string.format( "{%s}", table.concat( rt, "," ) ) end elseif vtype == "string" then return string.format( "%q", val ) elseif vtype == "function" or vtype == "userdata" or vtype == "nil" then return "null" else return tostring( val ) end end function util.serializeJSON( val ) return serialize_any( val, {} ) end end function util.shared_buffer( name, max ) max = max or 64 return { _pos_name = name .. ".position", _list_name = name .. ".list.", push = function( self, text ) local cpos = GetInt( self._pos_name ) SetString( self._list_name .. (cpos % max), text ) SetInt( self._pos_name, cpos + 1 ) end, len = function( self ) return math.min( GetInt( self._pos_name ), max ) end, pos = function( self ) return GetInt( self._pos_name ) end, get = function( self, index ) local pos = GetInt( self._pos_name ) local len = math.min( pos, max ) if index >= len then return end return GetString( self._list_name .. (pos + index - len) % max ) end, get_g = function( self, index ) return GetString( self._list_name .. (index % max) ) end, clear = function( self ) SetInt( self._pos_name, 0 ) ClearKey( self._list_name:sub( 1, -2 ) ) end, } end function util.shared_channel( name, max, local_realm ) max = max or 64 local channel = { _buffer = util.shared_buffer( name, max ), _offset = 0, _hooks = {}, _ready_count = 0, _ready = {}, broadcast = function( self, ... ) return self:send( "", ... ) end, send = function( self, realm, ... ) self._buffer:push( string.format( ",%s,;%s", (type( realm ) == "table" and table.concat( realm, "," ) or tostring( realm )), util.serialize( ... ) ) ) end, listen = function( self, callback ) if self._ready[callback] ~= nil then return end self._hooks[#self._hooks + 1] = callback self:ready( callback ) return callback end, unlisten = function( self, callback ) self:unready( callback ) self._ready[callback] = nil for i = 1, #self._hooks do if self._hooks[i] == callback then table.remove( self._hooks, i ) return true end end end, ready = function( self, callback ) if not self._ready[callback] then self._ready_count = self._ready_count + 1 self._ready[callback] = true end end, unready = function( self, callback ) if self._ready[callback] then self._ready_count = self._ready_count - 1 self._ready[callback] = false end end, } local_realm = "," .. (local_realm or "unknown") .. "," local function receive( ... ) for i = 1, #channel._hooks do local f = channel._hooks[i] if channel._ready[f] then f( channel, ... ) end end end hook.add( "base.tick", name, function( dt ) if channel._ready_count > 0 then local last_pos = channel._buffer:pos() if last_pos > channel._offset then for i = math.max( channel._offset, last_pos - max ), last_pos - 1 do local message = channel._buffer:get_g( i ) local start = message:find( ";", 1, true ) local realms = message:sub( 1, start - 1 ) if realms == ",," or realms:find( local_realm, 1, true ) then receive( util.unserialize( message:sub( start + 1 ) ) ) if channel._ready_count <= 0 then channel._offset = i + 1 return end end end channel._offset = last_pos end end end ) return channel end function util.async_channel( channel ) local listener = { _channel = channel, _waiter = nil, read = function( self ) self._waiter = coroutine.running() if not self._waiter then error( "async_channel:read() can only be used in a coroutine" ) end self._channel:ready( self._handler ) return coroutine.yield() end, close = function( self ) if self._handler then self._channel:unlisten( self._handler ) end end, } listener._handler = listener._channel:listen( function( _, ... ) if listener._waiter then local co = listener._waiter listener._waiter = nil listener._channel:unready( listener._handler ) return coroutine.resume( co, ... ) end end ) listener._channel:unready( listener._handler ) return listener end do local gets, sets = {}, {} function util.register_unserializer( type, callback ) gets[type] = function( key ) return callback( GetString( key ) ) end end hook.add( "api.newmeta", "api.createunserializer", function( name, meta ) gets[name] = function( key ) return setmetatable( {}, meta ):__unserialize( GetString( key ) ) end sets[name] = function( key, value ) return SetString( key, meta.__serialize( value ) ) end end ) function util.shared_table( name, base ) return setmetatable( base or {}, { __index = function( self, k ) local key = tostring( k ) local vtype = GetString( string.format( "%s.%s.type", name, key ) ) if vtype == "" then return end return gets[vtype]( string.format( "%s.%s.val", name, key ) ) end, __newindex = function( self, k, v ) local vtype = type( v ) local handler = sets[vtype] if not handler then return end local key = tostring( k ) if vtype == "table" then local meta = getmetatable( v ) if meta and meta.__serialize and meta.__type then vtype = meta.__type v = meta.__serialize( v ) handler = sets.string end end SetString( string.format( "%s.%s.type", name, key ), vtype ) handler( string.format( "%s.%s.val", name, key ), v ) end, } ) end function util.structured_table( name, base ) local function generate( base ) local root = {} local keys = {} for k, v in pairs( base ) do local key = name .. "." .. tostring( k ) if type( v ) == "table" then root[k] = util.structured_table( key, v ) elseif type( v ) == "string" then keys[k] = { type = v, key = key } else root[k] = v end end return setmetatable( root, { __index = function( self, k ) local entry = keys[k] if entry and gets[entry.type] then return gets[entry.type]( entry.key ) end end, __newindex = function( self, k, v ) local entry = keys[k] if entry and sets[entry.type] then return sets[entry.type]( entry.key, v ) end end, } ) end if type( base ) == "table" then return generate( base ) end return generate end gets.number = GetFloat gets.integer = GetInt gets.boolean = GetBool gets.string = GetString gets.table = util.shared_table sets.number = SetFloat sets.integer = SetInt sets.boolean = SetBool sets.string = SetString sets.table = function( key, val ) local tab = util.shared_table( key ) for k, v in pairs( val ) do tab[k] = v end end end end)();
-(function() local console_buffer = util.shared_buffer( "game.console", 128 ) local function maketext( ... ) local text = "" local len = select( "#", ... ) for i = 1, len do local s = tostring( select( i, ... ) ) if i < len then s = s .. string.rep( " ", 8 - #s % 8 ) end text = text .. s end return text end _OLDPRINT = _OLDPRINT or print function printcolor( r, g, b, ... ) local text = maketext( ... ) console_buffer:push( string.format( "%f;%f;%f;%s", r, g, b, text ) ) if PRINTTOSCREEN then DebugPrint( text ) end return _OLDPRINT( ... ) end function print( ... ) printcolor( 1, 1, 1, ... ) end function printinfo( ... ) printcolor( 0, .6, 1, ... ) end function warning( msg ) printcolor( 1, .7, 0, "[WARNING] " .. tostring( msg ) .. "\n " .. table.concat( util.stacktrace( 1 ), "\n " ) ) end printwarning = warning function printerror( ... ) printcolor( 1, .2, 0, ... ) end function clearconsole() console_buffer:clear() end function softassert( b, ... ) if not b then printerror( ... ) end return b, ... end function assert( b, msg, ... ) if not b then local m = msg or "Assertion failed" warning( m ) return error( m, ... ) end return b, msg, ... end end)();
-(function() GLOBAL_CHANNEL = util.shared_channel( "game.umf_global_channel", 128 ) end)();
-(function() local registered_meta = {} local reverse_meta = {} function global_metatable( name, parent ) local meta = registered_meta[name] if meta then if not parent then return meta end else meta = {} meta.__index = meta meta.__type = name registered_meta[name] = meta reverse_meta[meta] = name hook.saferun( "api.newmeta", name, meta ) end if parent then setmetatable( meta, global_metatable( parent ) ) end return meta end function find_global_metatable( name ) if not name then return end if type( name ) == "table" then return reverse_meta[name] end return registered_meta[name] end local function findmeta( src, found ) if found[src] then return end found[src] = true local res for k, v in pairs( src ) do if type( v ) == "table" then local dt local m = getmetatable( v ) if m then local name = reverse_meta[m] if name then dt = {} dt[1] = name end end local sub = findmeta( v, found ) if sub then dt = dt or {} dt[2] = sub end if dt then res = res or {} res[k] = dt end end end return res end local previous = -2 hook.add( "base.tick", "api.metatables.save", function( ... ) if GetTime() - previous > 2 then previous = GetTime() _G.GLOBAL_META_SAVE = findmeta( _G, {} ) end end ) local function restoremeta( dst, src ) for k, v in pairs( src ) do local dv = dst[k] if type( dv ) == "table" then if v[1] then setmetatable( dv, global_metatable( v[1] ) ) end if v[2] then restoremeta( dv, v[2] ) end end end end hook.add( "base.command.quickload", "api.metatables.restore", function( ... ) if GLOBAL_META_SAVE then restoremeta( _G, GLOBAL_META_SAVE ) end end ) end)();
-(function() timer = {} timer._backlog = {} local backlog = timer._backlog local function sortedinsert( tab, val ) for i = #tab, 1, -1 do if val.time < tab[i].time then tab[i + 1] = val return end tab[i + 1] = tab[i] end tab[1] = val end local diff = GetTime() function timer.simple( time, callback ) sortedinsert( backlog, { time = GetTime() + time - diff, callback = callback } ) end function timer.create( id, interval, iterations, callback ) sortedinsert( backlog, { id = id, time = GetTime() + interval - diff, interval = interval, callback = callback, runsleft = iterations - 1, } ) end function timer.wait( time ) local co = coroutine.running() if not co then error( "timer.wait() can only be used in a coroutine" ) end timer.simple( time, function() coroutine.resume( co ) end ) return coroutine.yield() end local function find( id ) for i = 1, #backlog do if backlog[i].id == id then return i, backlog[i] end end end function timer.time_left( id ) local index, entry = find( id ) if entry then return entry.time - GetTime() end end function timer.iterations_left( id ) local index, entry = find( id ) if entry then return entry.runsleft + 1 end end function timer.remove( id ) local index, entry = find( id ) if index then table.remove( backlog, index ) end end hook.add( "base.tick", "framework.timer", function( dt ) diff = 0 local now = GetTime() while #backlog > 0 do local first = backlog[#backlog] if first.time > now then break end backlog[#backlog] = nil first.callback() if first.runsleft and first.runsleft > 0 then first.runsleft = first.runsleft - 1 first.time = first.time + first.interval sortedinsert( backlog, first ) end end end ) end)();
-(function() visual = {} degreeToRadian = math.pi / 180 COLOR_WHITE = { r = 255 / 255, g = 255 / 255, b = 255 / 255, a = 255 / 255 } COLOR_BLACK = { r = 0, g = 0, b = 0, a = 255 / 255 } COLOR_RED = { r = 255 / 255, g = 0, b = 0, a = 255 / 255 } COLOR_ORANGE = { r = 255 / 255, g = 128 / 255, b = 0, a = 255 / 255 } COLOR_YELLOW = { r = 255 / 255, g = 255 / 255, b = 0, a = 255 / 255 } COLOR_GREEN = { r = 0, g = 255 / 255, b = 0, a = 255 / 255 } COLOR_CYAN = { r = 0, g = 255 / 255, b = 128 / 255, a = 255 / 255 } COLOR_AQUA = { r = 0, g = 255 / 255, b = 255 / 255, a = 255 / 255 } COLOR_BLUE = { r = 0, g = 0, b = 255 / 255, a = 255 / 255 } COLOR_VIOLET = { r = 128 / 255, g = 0, b = 255 / 255, a = 255 / 255 } COLOR_PINK = { r = 255 / 255, g = 0, b = 255 / 255, a = 255 / 255 } if DrawSprite then function visual.huergb( p, q, t ) if t < 0 then t = t + 1 end if t > 1 then t = t - 1 end if t < 1 / 6 then return p + (q - p) * 6 * t end if t < 1 / 2 then return q end if t < 2 / 3 then return p + (q - p) * (2 / 3 - t) * 6 end return p end function visual.hslrgb( h, s, l ) local r, g, b if s == 0 then r = l g = l b = l else local huergb = visual.huergb local q = l < .5 and l * (1 + s) or l + s - l * s local p = 2 * l - q r = huergb( p, q, h + 1 / 3 ) g = huergb( p, q, h ) b = huergb( p, q, h - 1 / 3 ) end return Vec( r, g, b ) end function visual.drawsprite( sprite, source, radius, info ) local r, g, b, a local writeZ, additive = true, false local target = GetCameraTransform().pos local DrawFunction = DrawSprite radius = radius or 1 if info then r = info.r and info.r or 1 g = info.g and info.g or 1 b = info.b and info.b or 1 a = info.a and info.a or 1 target = info.target or target if info.writeZ ~= nil then writeZ = info.writeZ end if info.additive ~= nil then additive = info.additive end DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or DrawFunction end DrawFunction( sprite, Transform( source, QuatLookAt( source, target ) ), radius, radius, r, g, b, a, writeZ, additive ) end function visual.drawsprites( sprites, sources, radius, info ) sprites = type( sprites ) ~= "table" and { sprites } or sprites for i = 1, #sprites do for j = 1, #sources do visual.drawsprite( sprites[i], sources[j], radius, info ) end end end function visual.drawline( sprite, source, destination, info ) local r, g, b, a local writeZ, additive = true, false local target = GetCameraTransform().pos local DrawFunction = DrawLine local width = 0.03 if info then r = info.r and info.r or 1 g = info.g and info.g or 1 b = info.b and info.b or 1 a = info.a and info.a or 1 width = info.width or width target = info.target or target if info.writeZ ~= nil then writeZ = info.writeZ end if info.additive ~= nil then additive = info.additive end DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine) end if sprite then local middle = VecScale( VecAdd( source, destination ), .5 ) local len = VecLength( VecSub( source, destination ) ) local transform = Transform( middle, QuatRotateQuat( QuatLookAt( source, destination ), QuatEuler( -90, 0, 0 ) ) ) local target_local = TransformToLocalPoint( transform, target ) target_local[2] = 0 local transform_fixed = TransformToParentTransform( transform, Transform( nil, QuatLookAt( target_local, nil ) ) ) DrawSprite( sprite, transform_fixed, width, len, r, g, b, a, writeZ, additive ) else DrawFunction( source, destination, r, g, b, a ); end end function visual.drawlines( sprites, sources, connect, info ) sprites = type( sprites ) ~= "table" and { sprites } or sprites for i = 1, #sprites do local sourceCount = #sources for j = 1, sourceCount - 1 do visual.drawline( sprites[i], sources[j], sources[j + 1], info ) end if connect then visual.drawline( sprites[i], sources[1], sources[sourceCount], info ) end end end function visual.drawaxis( transform, quat, radius, writeZ ) local DrawFunction = writeZ and DrawLine or DebugLine if not transform.pos then transform = Transform( transform, quat or QUAT_ZERO ) end radius = radius or 1 DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( radius, 0, 0 ) ), 1, 0, 0 ) DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, radius, 0 ) ), 0, 1, 0 ) DrawFunction( transform.pos, TransformToParentPoint( transform, Vec( 0, 0, radius ) ), 0, 0, 1 ) end function visual.drawpolygon( transform, radius, rotation, sides, info ) local points = {} local iteration = 1 local pow, sqrt, sin, cos = math.pow, math.sqrt, math.sin, math.cos local r, g, b, a local DrawFunction = DrawLine radius = sqrt( 2 * pow( radius, 2 ) ) or sqrt( 2 ) rotation = rotation or 0 sides = sides or 4 if info then r = info.r and info.r or 1 g = info.g and info.g or 1 b = info.b and info.b or 1 a = info.a and info.a or 1 DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine) end for v = 0, 360, 360 / sides do points[iteration] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius, 0, cos( (v + rotation) * degreeToRadian ) * radius ) ) points[iteration + 1] = TransformToParentPoint( transform, Vec( sin( ((v + 360 / sides) + rotation) * degreeToRadian ) * radius, 0, cos( ((v + 360 / sides) + rotation) * degreeToRadian ) * radius ) ) if iteration > 2 then DrawFunction( points[iteration], points[iteration + 1], r, g, b, a ) end iteration = iteration + 2 end return points end function visual.drawbox( transform, min, max, info ) local r, g, b, a local DrawFunction = DrawLine local points = { TransformToParentPoint( transform, Vec( min[1], min[2], min[3] ) ), TransformToParentPoint( transform, Vec( max[1], min[2], min[3] ) ), TransformToParentPoint( transform, Vec( min[1], max[2], min[3] ) ), TransformToParentPoint( transform, Vec( max[1], max[2], min[3] ) ), TransformToParentPoint( transform, Vec( min[1], min[2], max[3] ) ), TransformToParentPoint( transform, Vec( max[1], min[2], max[3] ) ), TransformToParentPoint( transform, Vec( min[1], max[2], max[3] ) ), TransformToParentPoint( transform, Vec( max[1], max[2], max[3] ) ), } if info then r = info.r and info.r or 1 g = info.g and info.g or 1 b = info.b and info.b or 1 a = info.a and info.a or 1 DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine) end DrawFunction( points[1], points[2], r, g, b, a ) DrawFunction( points[1], points[3], r, g, b, a ) DrawFunction( points[1], points[5], r, g, b, a ) DrawFunction( points[4], points[3], r, g, b, a ) DrawFunction( points[4], points[2], r, g, b, a ) DrawFunction( points[4], points[8], r, g, b, a ) DrawFunction( points[6], points[5], r, g, b, a ) DrawFunction( points[6], points[8], r, g, b, a ) DrawFunction( points[6], points[2], r, g, b, a ) DrawFunction( points[7], points[8], r, g, b, a ) DrawFunction( points[7], points[5], r, g, b, a ) DrawFunction( points[7], points[3], r, g, b, a ) return points end function visual.drawprism( transform, radius, depth, rotation, sides, info ) local points = {} local iteration = 1 local pow, sqrt, sin, cos = math.pow, math.sqrt, math.sin, math.cos local r, g, b, a local DrawFunction = DrawLine radius = sqrt( 2 * pow( radius, 2 ) ) or sqrt( 2 ) depth = depth or 1 rotation = rotation or 0 sides = sides or 4 if info then r = info.r and info.r or 1 g = info.g and info.g or 1 b = info.b and info.b or 1 a = info.a and info.a or 1 DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine) end for v = 0, 360, 360 / sides do points[iteration] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius, depth, cos( (v + rotation) * degreeToRadian ) * radius ) ) points[iteration + 1] = TransformToParentPoint( transform, Vec( sin( (v + rotation) * degreeToRadian ) * radius, -depth, cos( (v + rotation) * degreeToRadian ) * radius ) ) if iteration > 2 then DrawFunction( points[iteration], points[iteration + 1], r, g, b, a ) DrawFunction( points[iteration - 2], points[iteration], r, g, b, a ) DrawFunction( points[iteration - 1], points[iteration + 1], r, g, b, a ) end iteration = iteration + 2 end return points end function visual.drawsphere( transform, radius, rotation, samples, info ) local points = {} local sqrt, sin, cos = math.sqrt, math.sin, math.cos local r, g, b, a local DrawFunction = DrawLine radius = radius or 1 rotation = rotation or 0 samples = samples or 100 if info then r = info.r and info.r or 1 g = info.g and info.g or 1 b = info.b and info.b or 1 a = info.a and info.a or 1 DrawFunction = info.DrawFunction ~= nil and info.DrawFunction or (info.writeZ == false and DebugLine or DrawLine) end local points = {} for i = 0, samples do local y = 1 - (i / (samples - 1)) * 2 local rad = sqrt( 1 - y * y ) local theta = 2.399963229728653 * i local x = cos( theta ) * rad local z = sin( theta ) * rad local point = TransformToParentPoint( Transform( transform.pos, QuatRotateQuat( transform.rot, QuatEuler( 0, rotation, 0 ) ) ), Vec( x * radius, y * radius, z * radius ) ) DrawFunction( point, VecAdd( point, Vec( 0, .01, 0 ) ), r, g, b, a ) points[i + 1] = point end return points end end end)();
-(function() local xmlnode = { Render = function( self ) local attr = "" if self.attributes then for name, val in pairs( self.attributes ) do attr = string.format( "%s %s=%q", attr, name, val ) end end local children = {} if self.children then for i = 1, #self.children do children[i] = self.children[i]:Render() end end return string.format( "<%s%s>%s</%s>", self.type, attr, table.concat( children, "" ), self.type ) end, } local meta = { __call = function( self, children ) self.children = children return self end, __index = xmlnode, } XMLTag = function( type ) return function( attributes ) return setmetatable( { type = type, attributes = attributes }, meta ) end end ParseXML = function( xml ) local pos = 1 local function skipw() local next = xml:find( "[^ \t\n]", pos ) if not next then return false end pos = next return true end local function expect( pattern, noskip ) if not noskip then if not skipw() then return false end end local s, e = xml:find( pattern, pos ) if not s then return false end local pre = pos pos = e + 1 return xml:match( pattern, pre ) end local readtag, readattribute, readstring local rt = { n = "\n", t = "\t", r = "\r", ["0"] = "\0", ["\\"] = "\\", ["\""] = "\"" } readstring = function() if not expect( "^\"" ) then return false end local start = pos while true do local s = assert( xml:find( "[\\\"]", pos ), "Invalid string" ) if xml:sub( s, s ) == "\\" then pos = s + 2 else pos = s + 1 break end end return xml:sub( start, pos - 2 ):gsub( "\\(.)", rt ) end readattribute = function() local name = expect( "^([%d%w_]+)" ) if not name then return false end if expect( "^=" ) then return name, assert( readstring() ) else return name, "1" end end readtag = function() local save = pos if not expect( "^<" ) then return false end local type = expect( "^([%d%w_]+)" ) if not type then pos = save return false end skipw() local attributes = {} repeat local attr, val = readattribute() if attr then attributes[attr] = val end until not attr local children = {} if not expect( "^/>" ) then assert( expect( "^>" ) ) repeat local child = readtag() if child then children[#children + 1] = child end until not child assert( expect( "^</" ) and expect( "^" .. type ) and expect( "^>" ) ) end return XMLTag( type )( attributes )( children ) end return readtag() end end)();
-for i = 1, #__RUNLATER do local f = loadstring(__RUNLATER[i]) if f then pcall(f) end end
+#version 2
+local __RUNLATER = {}
+

```

---

# Migration Report: main\util.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main\util.lua
+++ patched/main\util.lua
@@ -1,11 +1,8 @@
-#include "umf/umf_meta.lua"
-#include "umf/umf_utils.lua"
-
+#version 2
 local VEC_MIN = Vec(-math.huge, -math.huge, -math.huge)
 local VEC_MAX = Vec(math.huge, math.huge, math.huge)
 
--- UI functions
-	function UiDrawLine(dx, dy, r, g, b, a)
+function UiDrawLine(dx, dy, r, g, b, a)
 		UiPush()
 			UiColor(r, g, b, a)
 			UiRotate(math.atan2(-dy, dx) * 180 / math.pi)
@@ -13,7 +10,7 @@
 		UiPop()
 	end
 
-	function UiEmptyButton(w, h, backColor)
+function UiEmptyButton(w, h, backColor)
 		UiAlign("left")
 
 		local info = {UiIsMouseInRect(w, h), InputPressed("lmb"), InputDown("lmb")}
@@ -28,7 +25,7 @@
 		return info
 	end
 
-	function UiTextedButton(text, align, w, h, backColor, textColor)
+function UiTextedButton(text, align, w, h, backColor, textColor)
 		local info = UiEmptyButton(w, h, backColor)
 		local colorOffset = (info[1] and info[3]) and .1 or 0
 
@@ -43,7 +40,7 @@
 		return info[1] and info[2], info[1] and info[3]
 	end
 
-	function UiColoredSlider(value, pos, rangeMin, rangeMax, w, h, backColor, sliderColor)
+function UiColoredSlider(value, pos, rangeMin, rangeMax, w, h, backColor, sliderColor)
 		local info = {UiIsMouseInRect(w, h), InputPressed("lmb"), InputDown("lmb")}
 
 		UiPush()
@@ -79,7 +76,7 @@
 		return widthValue * x
 	end
 
-	function UiColorPicker(lastColor, scale)
+function UiColorPicker(lastColor, scale)
 		local size = (480 * scale)
 		local mouseX, mouseY = UiGetMousePos()
 		local positions = (UiIsMouseInRect(size, size) and InputDown("lmb")) and {1 / size * math.min(math.max(mouseX, 0), size), 1, 1 / size * math.min(math.max(mouseY, 0), size)} or lastColor
@@ -102,7 +99,7 @@
 		return positions
 	end
 
-	function UiInformationCounter(x, y, scale, data, options)
+function UiInformationCounter(x, y, scale, data, options)
 		UiPush()
 			local color = visual.hslrgb(options.counter.textColor[1][1], options.counter.textColor[1][2], options.counter.textColor[1][3])
 			local xAlignments = {"left", "center", "right"}
@@ -149,35 +146,36 @@
 		UiPop()
 	end
 
--- Global functions
-	function Clone(object)
+function Clone(object)
 		return util.unserialize(util.serialize(object))
 	end
 
-	function GetBodies(min, max, require)
+function GetBodies(min, max, require)
 		QueryRequire(require and require or "")
 		return QueryAabbBodies(min and min or VEC_MIN, max and max or VEC_MAX)
 	end
-	function GetBodyCount(min, max, require)
+
+function GetBodyCount(min, max, require)
 		QueryRequire(require and require or "")
 		return #QueryAabbBodies(min and min or VEC_MIN, max and max or VEC_MAX)
 	end
 
-	function GetShapes(min, max, require)
+function GetShapes(min, max, require)
 		return QueryAabbShapes(min and min or VEC_MIN, max and max or VEC_MAX)
 	end
-	function GetShapeCount(min, max, require)
+
+function GetShapeCount(min, max, require)
 		return #QueryAabbShapes(min and min or VEC_MIN, max and max or VEC_MAX)
 	end
 
--- Mathematical functions
-	function Round(value, decimals, overflow)
+function Round(value, decimals, overflow)
 		decimals = decimals or 0
 		overflow = overflow or .5
 		return math.floor((value + overflow) * 10 ^ decimals) / 10 ^ decimals
 	end
 
-	function CalculateFrameAccuracy(framesPerSecond, options)
+function CalculateFrameAccuracy(framesPerSecond, options)
 		local accuracy = math.pow(10, framesPerSecond >= 100 and math.max(options.counter.accuracy - 1, 0) or options.counter.accuracy)
 		return math.floor(framesPerSecond * accuracy) / accuracy
-	end+	end
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
@@ -1,105 +1,105 @@
-
-function init()
-	bleed = GetBool("savegame.mod.bleed")
-	gore = GetInt("savegame.mod.gore")
-	gore_kill = GetString("savegame.mod.gore_kill")
-	if gore_kill == "" then
-		SetString("savegame.mod.gore_kill", "O")
-	end
-	--DebugPrint(gore_kill)
-	if gore == nil or gore == 0 then
-		gore = 1
-	end
-	changing_mode = 0
+#version 2
+function server.init()
+    bleed = GetBool("savegame.mod.bleed")
+    gore = GetInt("savegame.mod.gore")
+    gore_kill = GetString("savegame.mod.gore_kill")
+    if gore_kill == "" then
+    	SetString("savegame.mod.gore_kill", "O", true)
+    end
+    --DebugPrint(gore_kill)
+    if gore == nil or gore == 0 then
+    	gore = 1
+    end
+    changing_mode = 0
 end
 
-function draw()
-	UiAlign("center middle")
-	UiTranslate(UiCenter(), 350)
-	UiFont("bold.ttf", 48)
-	UiText("[SW's GORE MOD 2]")
-	UiFont("regular.ttf", 24)
-	UiTranslate(0, 70)
-	UiPush()
-		UiTranslate(75, 0)
-		last_input = InputLastPressedKey()
-		if last_input ~= "" then
-			if changing_mode == 1 then gore_kill = last_input end
-			SetString("savegame.mod.gore_kill", last_input)
-			changing_mode = 0
-		end
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-	    if UiTextButton(gore_kill, 50, 30) and changing_mode == 0 then --Explode Input
-		    gore_kill = "..."
-			changing_mode = 1
-		end
-		UiTranslate(-135, 0)
-		UiText("Kill all ragdolls:", 150, 30)
-	UiPop()
-	UiTranslate(0, 90)
-	UiPush()
-	UiAlign("center")
-		UiText("Gore Effects Detail")
-		UiTranslate(0, 34)
-		UiAlign("center")
-		UiColor(0.5, 0.8, 1)
-		if gore == 1 then
-			UiAlign("center middle")
-		    --UiTranslate(-35, 0)
-			if UiTextButton("No gore", 20, 20) then
-				gore = 2
-				SetInt("savegame.mod.gore", gore)
-			end
-		else if gore == 2 then
-			--UiTranslate(-28, 0)
-			if UiTextButton("Some gore", 20, 20) then
-				gore = 3
-				SetInt("savegame.mod.gore", gore)
-			end
-		else if gore == 3 then
-			--UiTranslate(-21, 0)
-			if UiTextButton("Advanced gore", 20, 20) then
-				gore = 4
-				SetInt("savegame.mod.gore", gore)
-			end
-			else if gore == 4 then
-			--UiTranslate(-14, 0)
-			if UiTextButton("Experimental gore (Very likely laggy)", 20, 20) then
-				gore = 1
-				SetInt("savegame.mod.gore", gore)
-			end
-		end
-		end
-		end
-		end
-	UiPop()
-	UiTranslate(0, 60)
-	UiColor(1, 1, 1)
-	UiPush()
-		UiText("Ragdolls leave blood puddles, Currently: "..tostring(bleed))
-		UiTranslate(0, 30)
-		UiAlign("center")
-		UiColor(0.5, 0.8, 1)
-		if bleed then 
-			UiTranslate(0, 0)
-			if UiTextButton("Yes", 20, 20) then
-				bleed = false
-				SetBool("savegame.mod.bleed", bleed)
-			end
-		else
-			UiTranslate(0, 0)
-			if UiTextButton("No", 20, 20) then
-				bleed = true
-				SetBool("savegame.mod.bleed", bleed)
-			end
-		end
-	UiPop()
-	
-	
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+function client.draw()
+    UiAlign("center middle")
+    UiTranslate(UiCenter(), 350)
+    UiFont("bold.ttf", 48)
+    UiText("[SW's GORE MOD 2]")
+    UiFont("regular.ttf", 24)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiTranslate(75, 0)
+    	last_input = InputLastPressedKey()
+    	if last_input ~= "" then
+    		if changing_mode == 1 then gore_kill = last_input end
+    		SetString("savegame.mod.gore_kill", last_input, true)
+    		changing_mode = 0
+    	end
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+        if UiTextButton(gore_kill, 50, 30) and changing_mode == 0 then --Explode Input
+    	    gore_kill = "..."
+    		changing_mode = 1
+    	end
+    	UiTranslate(-135, 0)
+    	UiText("Kill all ragdolls:", 150, 30)
+    UiPop()
+    UiTranslate(0, 90)
+    UiPush()
+    UiAlign("center")
+    	UiText("Gore Effects Detail")
+    	UiTranslate(0, 34)
+    	UiAlign("center")
+    	UiColor(0.5, 0.8, 1)
+    	if gore == 1 then
+    		UiAlign("center middle")
+    	    --UiTranslate(-35, 0)
+    		if UiTextButton("No gore", 20, 20) then
+    			gore = 2
+    			SetInt("savegame.mod.gore", gore, true)
+    		end
+    	else if gore == 2 then
+    		--UiTranslate(-28, 0)
+    		if UiTextButton("Some gore", 20, 20) then
+    			gore = 3
+    			SetInt("savegame.mod.gore", gore, true)
+    		end
+    	else if gore == 3 then
+    		--UiTranslate(-21, 0)
+    		if UiTextButton("Advanced gore", 20, 20) then
+    			gore = 4
+    			SetInt("savegame.mod.gore", gore, true)
+    		end
+    		else if gore == 4 then
+    		--UiTranslate(-14, 0)
+    		if UiTextButton("Experimental gore (Very likely laggy)", 20, 20) then
+    			gore = 1
+    			SetInt("savegame.mod.gore", gore, true)
+    		end
+    	end
+    	end
+    	end
+    	end
+    UiPop()
+    UiTranslate(0, 60)
+    UiColor(1, 1, 1)
+    UiPush()
+    	UiText("Ragdolls leave blood puddles, Currently: "..tostring(bleed))
+    	UiTranslate(0, 30)
+    	UiAlign("center")
+    	UiColor(0.5, 0.8, 1)
+    	if bleed then 
+    		UiTranslate(0, 0)
+    		if UiTextButton("Yes", 20, 20) then
+    			bleed = false
+    			SetBool("savegame.mod.bleed", bleed, true)
+    		end
+    	else
+    		UiTranslate(0, 0)
+    		if UiTextButton("No", 20, 20) then
+    			bleed = true
+    			SetBool("savegame.mod.bleed", bleed, true)
+    		end
+    	end
+    UiPop()
 
-	UiTranslate(0, 120)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
-end+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 120)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
+end
+

```

---

# Migration Report: US military vehicle pack\humveeCROWS.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/US military vehicle pack\humveeCROWS.lua
+++ patched/US military vehicle pack\humveeCROWS.lua
@@ -1,98 +1 @@
-#include "../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {	
-					name 	= ".50-cal Browning",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = ".50-cal",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 50,
-													velocity				= 240,
-													hit 					=3,
-													maxPenDepth 			= 0.33,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.3,
-													shellWidth				= 0.1,
-													shellHeight				= 0.3,
-													r						= 0.8,
-													g						= 0.8, 
-													b						= 0.5, 
-													tracer 					= 2,
-													tracerL					= 7,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											},
-										},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 2.,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 360,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.05,
-				weapon_recoil 			= 200,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/HeavySingleShot",
-				mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"MOD/sounds/HeavyAutoFire",			
-				},
-
-	},
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```

---

# Migration Report: US military vehicle pack\humveerocket.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/US military vehicle pack\humveerocket.lua
+++ patched/US military vehicle pack\humveerocket.lua
@@ -1,140 +1 @@
-#include "../scripts/avf_custom.lua"
-
-
---[[
-
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-vehicleParts = {
-	chassis = {
-		
-	},
-	turrets = {
-
-	},
-	guns = {
-		["mainCannon"] = {
-					name 	= "Rocket Launcher",
-					weaponType 				= "rocket",
-					caliber 				= 106.7,
-					magazines 					= {
-											[1] = {
-							magazineCapacity = 14,
-							ammoCount = 0,
-							magazineCount = 150,
-							name = "107mm rocket HE Mid",
-							caliber 				= 106.7,
-							velocity				= 50,
-							explosionSize			= 1.5,
-							maxPenDepth 			= 0.1,
-							timeToLive 				= 20,
-							launcher				= "rocket",
-							payload					= "HE",
-							shellWidth				= 1,
-							shellHeight				= 3,
-							r						= 0.1,
-							g						= .3, 
-							b						= 0.1, 
-							shellSpriteName			= "MOD/gfx/rocketModel2.png",
-							shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											[2] = {
-							magazineCapacity = 14,
-							ammoCount = 0,
-							magazineCount = 150,
-							name = "107mm rocket HE Far",
-							caliber 				= 106.7,
-							velocity				= 60,
-							explosionSize			= 1.5,
-							maxPenDepth 			= 0.1,
-							timeToLive 				= 20,
-							launcher				= "rocket",
-							payload					= "HE",
-							shellWidth				= 1,
-							shellHeight				= 3,
-							r						= 0.1,
-							g						= .5, 
-							b						= 0.1, 
-							shellSpriteName			= "MOD/gfx/rocketModel2.png",
-							shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-												},
-											[3] = {
-							magazineCapacity = 14,
-							ammoCount = 0,
-							magazineCount = 150,
-							name = "122mm rocket HE Close",
-							caliber 				= 122,
-							velocity				= 45,
-							explosionSize			= 1.8,
-							maxPenDepth 			= 0.1,
-							timeToLive 				= 12,
-							launcher				= "rocket",
-							payload					= "HE",
-							shellWidth				= 1,
-							shellHeight				= 3,
-							r						= 0.1,
-							g						= .8, 
-							b						= 0.1, 
-							shellSpriteName			= "MOD/gfx/rocketModel2.png",
-							shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-									flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=10},
-												},
-					sight					= {
-												[1] = {
-												x = 2.2,
-												y = 1.3,
-												z = 0.3,
-											},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 90,
-					reload 					= 5,
-					recoil 					= 0.3,
-					weapon_recoil 			= 25,
-					cannonBlast 			= 0,
-					dispersion 				= 10,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/rockets/rocket_launcher_01",
-
-				},		
-			},
-	
-	
-}
-	
-
-	---- magazine num _ val
-	---- barrels num value
-
-vehicle = {
-
-}
-
+#version 2

```
