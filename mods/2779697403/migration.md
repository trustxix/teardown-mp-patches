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

# Migration Report: avf\prefabs\cromwell\cromwell_V.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\cromwell\cromwell_V.lua
+++ patched/avf\prefabs\cromwell\cromwell_V.lua
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
-											x = -0.03,
-											y = 0.01
-											},
-									},
-			zoomSight 				= "MOD/gfx/cromwell_sight.png",
-			soundFile				= "MOD/sounds/tank/tank_fire_09",
-			reloadSound				= "MOD/sounds/tank/reload_short_01",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 400,
-
-			elevationSpeed			= 0.5,
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
-						magazineCapacity = 1,
-						ammoCount = 0,
-						magazineCount = 100,
-						caliber 				= 75,
-						velocity				= 200,
-						maxPenDepth 			= 	1.09,
-						shellWidth				= 0.25,
-						shellHeight				= .75,
-						r						= 0.4,
-						g						= 1.4, 
-						b						= 0.4,
-						payload					= "AP",
-					},
-						[2] = {name="HE M46",
-						magazineCapacity = 1,
-						ammoCount = 0,
-						magazineCount = 50,
-						caliber 				= 75,
-						velocity				= 190,
-						explosionSize			= 0.8,
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
-					zoomSight 				= "MOD/gfx/cromwell_sight.png",
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

# Migration Report: avf\prefabs\cromwell\cromwell_V_blufor_ai.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\cromwell\cromwell_V_blufor_ai.lua
+++ patched/avf\prefabs\cromwell\cromwell_V_blufor_ai.lua
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
-	ai_elements = {
-		side = 1,
-
-
-	},
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
-											x = -0.03,
-											y = 0.01
-											},
-									},
-			zoomSight 				= "MOD/gfx/cromwell_sight.png",
-			soundFile				= "MOD/sounds/tank/tank_fire_09",
-			reloadSound				= "MOD/sounds/tank/reload_short_01",
-			reloadPlayOnce			= true,
-										-- aimForwards = true,
-			zero_range 				= 400,
-
-			elevationSpeed			= 0.5,
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
-						magazineCapacity = 1,
-						ammoCount = 0,
-						magazineCount = 100,
-						caliber 				= 75,
-						velocity				= 200,
-						maxPenDepth 			= 	1.09,
-						shellWidth				= 0.25,
-						shellHeight				= .75,
-						r						= 0.4,
-						g						= 1.4, 
-						b						= 0.4,
-						payload					= "AP",
-					},
-						[2] = {name="HE M46",
-						magazineCapacity = 1,
-						ammoCount = 0,
-						magazineCount = 50,
-						caliber 				= 75,
-						velocity				= 190,
-						explosionSize			= 0.8,
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
-					zoomSight 				= "MOD/gfx/cromwell_sight.png",
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

# Migration Report: avf\prefabs\t72\t72A.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\t72\t72A.lua
+++ patched/avf\prefabs\t72\t72A.lua
@@ -1,38 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46M"
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
@@ -1,38 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46M1"
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
@@ -1,37 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46"
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
@@ -1,38 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46M"
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
@@ -1,38 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46M1"
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
@@ -1,37 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46"
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
@@ -1,38 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46M"
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
@@ -1,38 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46M1"
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
@@ -1,37 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					template = "2A46"
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

# Migration Report: avf\prefabs\technicals\Offroad_armed.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\Offroad_armed.lua
+++ patched/avf\prefabs\technicals\Offroad_armed.lua
@@ -1,118 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-		["NSV"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "NSV"
-				},	
-		["GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
-				},	
-		["main_GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG_02"
-				},	
-		["main_MILAN"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simple_cannon",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "MILAN_02"
-				},	
-		["GMG_01"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG"
-				},	
-		["GMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG_02"
-				},
-		["mainCannon"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "KSP_88"
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

# Migration Report: avf\prefabs\technicals\Offroad_WMIK.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\Offroad_WMIK.lua
+++ patched/avf\prefabs\technicals\Offroad_WMIK.lua
@@ -1,94 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-		["GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
-				},	
-		["main_GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
-				},	
-		["main_MILAN"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simple_cannon",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "MILAN_02"
-				},	
-		["GMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG"
-				},	
-		["mainCannon"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "L1A1_2"
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

# Migration Report: avf\prefabs\technicals\ZSU-23-2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\ZSU-23-2.lua
+++ patched/avf\prefabs\technicals\ZSU-23-2.lua
@@ -1,125 +1 @@
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
-					name = "23 mm 2A13 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= {
-											[1] = {
-													name = "B_23mm_AA",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .55,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "HE",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-																									
-												},
-											[2] = {
-													name = "B_23mm_AA_AP",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,			
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .6,
-													maxPenDepth 			= 0.5,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "AP",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=0.2,y=.1,z=-1.2},
-									[2] = {x=0.6,y=.1,z=-1.2},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 1.2,
-												y = 1.3,
-												z = 0.3,
-												},
-
-
-												},
-					canZoom					= false,
-					highVelocityShells		= true,
-					RPM 					= 350,
-					reload 					= 4,
-					cannonBlast				= 0.1,
-					recoil 					= 0.05,
-					weapon_recoil 			= 2400,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .5,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/autocannons/zsu_23_2_single",
-					mouseDownSoundFile 			=	"MOD/sounds/autocannons/zsu_23_2_sub_burst_02",
-
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

# Migration Report: avf\prefabs\technicals\ZSU-23-4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals\ZSU-23-4.lua
+++ patched/avf\prefabs\technicals\ZSU-23-4.lua
@@ -1,125 +1 @@
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
-					name = "23 mm 2A13 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= {
-											[1] = {
-													name = "B_23mm_AA",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .6,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "HE",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-																									
-												},
-											[2] = {
-													name = "B_23mm_AA_AP",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,			
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .6,
-													maxPenDepth 			= 0.5,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "AP",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=0.2,y=.1,z=-1.2},
-									[2] = {x=0.6,y=.1,z=-1.2},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 1.2,
-												y = 1.3,
-												z = 0.3,
-												},
-
-
-												},
-					canZoom					= false,
-					highVelocityShells		= true,
-					RPM 					= 350,
-					reload 					= 4,
-					recoil 					= 1,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .5,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/zsuSingle",
-					mouseDownSoundFile 		=	"MOD/sounds/zsuMulti1",
-					loopSoundFile 			=	"MOD/sounds/zsuFiring_long-2.ogg",
-					tailOffSound	 		=	"MOD/sounds/zsuSingle",
-
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

# Migration Report: avf\prefabs\technicals_woodland\Offroad_armed.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\Offroad_armed.lua
+++ patched/avf\prefabs\technicals_woodland\Offroad_armed.lua
@@ -1,158 +1,4 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../weapon_templates/weapon_sights_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-		["NSV"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "NSV"
-				},	
-		["GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
-				},	
-		["main_GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG_02"
-				},	
-		["main_MILAN"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simple_cannon",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "MILAN_02"
-				},	
-		["GMG_01"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG"
-				},	
-		["GMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG_02"
-				},
-		["mainCannon"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "KSP_88"
-				},	
-		["CROWS"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "KSP_88_CROWS",
-					custom_sight_script = true,
-					custom_sight_template = "CROWS_MG",
-				},
-		["CROWS_JAV"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "javelin",
-					custom_sight_script = true,
-					custom_sight_template = "JAVELIN"
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
-
-				-- special_custom_sounds = 
-				-- 						{
-				-- 							reload_sounds			= {
-				-- 								reload_type 	= "loop_and_sound",
-				-- 								reloaded_sound = "MOD/avf/snd/nsv/nsv_reload_loop",
-				-- 								reload_loop = "MOD/avf/snd/nsv/nsv_reloaded",
-
+#version 2
 function load_vehice_specific_sounds()
 	local special_sound_set =""
 	for key,gun in pairs(vehicleParts.guns) do
@@ -192,14 +38,7 @@
 		end
 	end
 end
-	
---[[
-
-SetTag(source, "PlaySound", sound_type)
-SetTag(source, "PlayLoop", sound_type)
-SetTag(source, "reloading", reload_percentage)
-PlaySound(self.snd.shootSnd[math.random(1,#self.snd.shootSnd)])
-]]
+
 function custom_avf_sounds()
 	local gun_sound = nil
 	local sound_type 
@@ -273,7 +112,7 @@
 
 	-- DebugWatch("custom_avf_ .weapon_group",GetString("level.avf.weapon_group"))
 
-	SetInt("level.avf.focus_weapon",testgunobj )
+	SetInt("level.avf.focus_weapon",testgunobj , true)
 	if(GetBool("level.avf.sniper_mode")) then
 		local focus_gun = FindShape("avf_primary_weapon_group_"..GetString("level.avf.weapon_group"))
 		-- DebugWatch("found shape",IsHandleValid(focus_gun))
@@ -343,7 +182,7 @@
 				-- 			local height = UiHeight() 
 				-- 			local w = UiWidth()
 				-- 			UiPush()
-				-- 				if dist > 0 then
+				-- 				if dist ~= 0 then
 				-- 					UiFont("bold.ttf", 12)
 				-- 					-- DebugWatch("dist ",dist)
 				-- 					-- DebugWatch("xy ",x)
@@ -368,7 +207,9 @@
 
 end
 
-function draw_custom_sight(gun,gun_key,gun_values)
+function draw_custom_
+
+ght(gun,gun_key,gun_values)
 	local sight_template = gun_values['custom_sight_template'] 
 	if(gun_key=="igla") then 
 		igla_scope()

```

---

# Migration Report: avf\prefabs\technicals_woodland\Offroad_WMIK.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\Offroad_WMIK.lua
+++ patched/avf\prefabs\technicals_woodland\Offroad_WMIK.lua
@@ -1,94 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-		["GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
-				},	
-		["main_GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
-				},	
-		["main_MILAN"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simple_cannon",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "MILAN_02"
-				},	
-		["GMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG"
-				},	
-		["mainCannon"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "L1A1_2"
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

# Migration Report: avf\prefabs\technicals_woodland\technical_armed.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\technical_armed.lua
+++ patched/avf\prefabs\technicals_woodland\technical_armed.lua
@@ -1,169 +1,11 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../weapon_templates/weapon_sights_templates.lua"
-
-#include "../../scripts/avf_custom.lua"
-]]
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
-		["NSV"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "NSV"
-				},	
-		["GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="2",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
-				},	
-		["main_GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG_02"
-				},	
-		["secondary_GPMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG_02"
-				},
-		["main_MILAN"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simple_cannon",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "MILAN_02"
-				},	
-		["GMG_01"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG"
-				},	
-		["GMG"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG_02"
-				},
-		["mainCannon"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "KSP_88_2",
-					custom_sight_script = true,
-
-				},	
-		["mainCannon2"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "KSP_88_2"
-				},	
-		["igla"] = {	
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customcannon",
-						group="1",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true,
-					},
-					template = "igla",
-					custom_sight_script = true,
-
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
 function custom_avf_ui() 
 	-- test_import()
 	-- DebugWatch("custom_avf_ui",""..string.byte("script 1 running"))
 
 	-- DebugWatch("custom_avf_ .weapon_group",GetString("level.avf.weapon_group"))
 
-	SetInt("level.avf.focus_weapon",testgunobj )
+	SetInt("level.avf.focus_weapon",testgunobj , true)
 	if(GetBool("level.avf.sniper_mode")) then
 		local focus_gun = FindShape("avf_primary_weapon_group_"..GetString("level.avf.weapon_group"))
 		-- DebugWatch("found shape",IsHandleValid(focus_gun))
@@ -221,7 +63,7 @@
 						local height = UiHeight() 
 						local w = UiWidth()
 						UiPush()
-							if dist > 0 then
+							if dist ~= 0 then
 								UiFont("bold.ttf", 12)
 								-- DebugWatch("dist ",dist)
 								-- DebugWatch("xy ",x)
@@ -253,8 +95,11 @@
 
 end
 
-function draw_custom_sight(gun,gun_key,gun_values)
+function draw_custom_
+
+ght(gun,gun_key,gun_values)
 	if(gun_key=="igla") then 
 		igla_scope()
 	end
-end+end
+

```

---

# Migration Report: avf\prefabs\technicals_woodland\technical_bm_14.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\technical_bm_14.lua
+++ patched/avf\prefabs\technicals_woodland\technical_bm_14.lua
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

# Migration Report: avf\prefabs\technicals_woodland\technical_dshk.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\technical_dshk.lua
+++ patched/avf\prefabs\technicals_woodland\technical_dshk.lua
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

# Migration Report: avf\prefabs\technicals_woodland\technical_spg9.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\technical_spg9.lua
+++ patched/avf\prefabs\technicals_woodland\technical_spg9.lua
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

# Migration Report: avf\prefabs\technicals_woodland\technical_type_63.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\technical_type_63.lua
+++ patched/avf\prefabs\technicals_woodland\technical_type_63.lua
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

# Migration Report: avf\prefabs\technicals_woodland\technical_UB16.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\technical_UB16.lua
+++ patched/avf\prefabs\technicals_woodland\technical_UB16.lua
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

# Migration Report: avf\prefabs\technicals_woodland\ZSU-23-2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\ZSU-23-2.lua
+++ patched/avf\prefabs\technicals_woodland\ZSU-23-2.lua
@@ -1,125 +1 @@
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
-					name = "23 mm 2A13 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= {
-											[1] = {
-													name = "B_23mm_AA",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .55,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "HE",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-																									
-												},
-											[2] = {
-													name = "B_23mm_AA_AP",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,			
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .6,
-													maxPenDepth 			= 0.5,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "AP",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=0.2,y=.1,z=-1.2},
-									[2] = {x=0.6,y=.1,z=-1.2},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 1.2,
-												y = 1.3,
-												z = 0.3,
-												},
-
-
-												},
-					canZoom					= false,
-					highVelocityShells		= true,
-					RPM 					= 350,
-					reload 					= 4,
-					cannonBlast				= 0.1,
-					recoil 					= 0.05,
-					weapon_recoil 			= 2400,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .5,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/autocannons/zsu_23_2_single",
-					mouseDownSoundFile 			=	"MOD/sounds/autocannons/zsu_23_2_sub_burst_02",
-
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

# Migration Report: avf\prefabs\technicals_woodland\ZSU-23-4.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\technicals_woodland\ZSU-23-4.lua
+++ patched/avf\prefabs\technicals_woodland\ZSU-23-4.lua
@@ -1,125 +1 @@
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
-					name = "23 mm 2A13 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= {
-											[1] = {
-													name = "B_23mm_AA",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .6,
-													maxPenDepth 			= 0.1,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "HE",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-																									
-												},
-											[2] = {
-													name = "B_23mm_AA_AP",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,			
-													caliber 				= 23,
-													velocity				= 220,
-													explosionSize 			= .6,
-													maxPenDepth 			= 0.5,
-													timeToLive 				= 7,
-													launcher				= "cannon",
-													payload					= "AP",
-													shellWidth				= 0.1,
-													shellHeight				= 0.7,
-													r						= 0.5,
-													g						= 0.5, 
-													b						= 0.5, 
-													tracer 					= 1,
-													tracerL					= 5,
-													tracerW					= 2,
-													tracerR					= 1.8,
-													tracerG					= 1.0, 
-													tracerB					= 1.0, 
-													shellSpriteName			= "MOD/gfx/shellModel2.png",
-													shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=0.2,y=.1,z=-1.2},
-									[2] = {x=0.6,y=.1,z=-1.2},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 1.2,
-												y = 1.3,
-												z = 0.3,
-												},
-
-
-												},
-					canZoom					= false,
-					highVelocityShells		= true,
-					RPM 					= 350,
-					reload 					= 4,
-					recoil 					= 1,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .5,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/zsuSingle",
-					mouseDownSoundFile 		=	"MOD/sounds/zsuMulti1",
-					loopSoundFile 			=	"MOD/sounds/zsuFiring_long-2.ogg",
-					tailOffSound	 		=	"MOD/sounds/zsuSingle",
-
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

# Migration Report: avf\prefabs\turrets\D-30.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\D-30.lua
+++ patched/avf\prefabs\turrets\D-30.lua
@@ -1,46 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customcannon",
-						group="primary",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "D-30"
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

# Migration Report: avf\prefabs\turrets\GMG.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\GMG.lua
+++ patched/avf\prefabs\turrets\GMG.lua
@@ -1,46 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="primary",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GMG"
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

# Migration Report: avf\prefabs\turrets\GPMG_LMG.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\GPMG_LMG.lua
+++ patched/avf\prefabs\turrets\GPMG_LMG.lua
@@ -1,46 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customMG",
-						group="primary",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "GPMG"
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

# Migration Report: avf\prefabs\turrets\L1A1_HMG.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\L1A1_HMG.lua
+++ patched/avf\prefabs\turrets\L1A1_HMG.lua
@@ -1,46 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simpleMG",
-						group="primary",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "L1A1"
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

# Migration Report: avf\prefabs\turrets\MILAN_ATGM.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\MILAN_ATGM.lua
+++ patched/avf\prefabs\turrets\MILAN_ATGM.lua
@@ -1,46 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simpleMG",
-						group="primary",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "MILAN"
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

# Migration Report: avf\prefabs\turrets\SPG-9.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\SPG-9.lua
+++ patched/avf\prefabs\turrets\SPG-9.lua
@@ -1,46 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					cfgWeapon = {
-						component="gun", 
-						weaponType="simpleMG",
-						group="primary",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "SPG9"
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

# Migration Report: avf\prefabs\turrets\weapon_templates.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\weapon_templates.lua
+++ patched/avf\prefabs\turrets\weapon_templates.lua
@@ -1,169 +1 @@
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
-templates = {
-
-	["2A13"] = {
-		name = "23 mm 2A13 autocannons",
-		weaponType 				= "cannon",
-		caliber 				= 23,
-		default = "B_23mm_AA",
-		magazines 					= {
-								[1] = {
-										name = "B_23mm_AA",
-										magazineCapacity = 100,
-										ammoCount = 0,
-										magazineCount = 50,
-										caliber 				= 23,
-										velocity				= 220,
-										explosionSize 			= .55,
-										maxPenDepth 			= 0.1,
-										timeToLive 				= 7,
-										launcher				= "cannon",
-										payload					= "HE",
-										shellWidth				= 0.1,
-										shellHeight				= 0.7,
-										r						= 0.5,
-										g						= 0.5, 
-										b						= 0.5, 
-										tracer 					= 1,
-										tracerL					= 5,
-										tracerW					= 2,
-										tracerR					= 1.8,
-										tracerG					= 1.0, 
-										tracerB					= 1.0, 
-										shellSpriteName			= "MOD/gfx/shellModel2.png",
-										shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-																						
-									},
-								[2] = {
-										name = "B_23mm_AA_AP",
-										magazineCapacity = 200,
-										ammoCount = 0,
-										magazineCount = 10,			
-										caliber 				= 23,
-										velocity				= 220,
-										explosionSize 			= .6,
-										maxPenDepth 			= 0.5,
-										timeToLive 				= 7,
-										launcher				= "cannon",
-										payload					= "AP",
-										shellWidth				= 0.1,
-										shellHeight				= 0.7,
-										r						= 0.5,
-										g						= 0.5, 
-										b						= 0.5, 
-										tracer 					= 1,
-										tracerL					= 5,
-										tracerW					= 2,
-										tracerR					= 1.8,
-										tracerG					= 1.0, 
-										tracerB					= 1.0, 
-										shellSpriteName			= "MOD/gfx/shellModel2.png",
-										shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-
-									},
-								},
-		loadedMagazine 			= 1,
-		barrels = 
-					{
-						[1] = {x=0.2,y=.1,z=-1.2},
-						[2] = {x=0.6,y=.1,z=-1.2},
-					},
-		multiBarrel 			= 1,
-		sight					= {
-									[1] = {
-									x = 1.2,
-									y = 1.3,
-									z = 0.3,
-									},
-
-
-									},
-		canZoom					= false,
-		highVelocityShells		= true,
-		RPM 					= 350,
-		reload 					= 4,
-		cannonBlast				= 0.1,
-		recoil 					= 0.05,
-		weapon_recoil 			= 2400,
-		dispersion 				= 20,
-		gunRange				= 500,
-		gunBias 				= -1,
-		smokeFactor 			= .5,
-		smokeMulti				= 1,
-		soundFile   = "MOD/sounds/autocannons/zsu_23_2_single",
-		mouseDownSoundFile 			=	"MOD/sounds/autocannons/zsu_23_2_sub_burst_02",
-	},
-
-	["D-30"] = {
-		name = "D-30 Artillary",
-		weaponType 				= "cannon",
-		caliber 				= 152,
-		default = "152mm_HE",
-		magazines 					= {
-								[1] = {
-										name = "152mm_HE",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 300,
-										caliber 				= 152,
-										velocity				= 200,
-										gravityCoef				= 3,
-										explosionSize			= 3.5,
-										maxPenDepth 			= 0.25,
-										timeToLive 				= 7,
-										launcher				= "cannon",
-										payload					= "HE",
-										shellWidth				= 1.5,
-										shellHeight				= 3,
-										r						= 0.8,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/shellModel2.png",
-										shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								},
-							},
-		loadedMagazine 			= 1,
-		barrels 				= 
-									{
-										[1] = {x=0.2,y=0.2,z=-0.3},
-									},
-		multiBarrel 			= 1,
-		sight					= {
-									[1] = {
-									x = 3,
-									y = 1.3,
-									z = 0.3,
-										},
-
-									},
-		canZoom					= true,
-		highVelocityShells		= true,
-		cannonBlast 			= 10,
-		RPM 					= 10,
-		reload 					= 2,
-		recoil 					= 2.5,
-		dispersion 				= 20,
-		gunRange				= 500,
-		gunBias 				= -1,
-		elevationSpeed			= .5,
-		smokeFactor 			= 3,
-		smokeMulti				= 20,
-		soundFile				= "MOD/sounds/Relic_700_KV2Fire",
-	},
-
-}
-	
-
-
+#version 2

```

---

# Migration Report: avf\prefabs\turrets\ZSU-23-2.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\turrets\ZSU-23-2.lua
+++ patched/avf\prefabs\turrets\ZSU-23-2.lua
@@ -1,46 +1 @@
---[[
-#include "../weapon_templates/weapon_templates.lua"
-#include "../../scripts/avf_custom.lua"
-]]
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
-					cfgWeapon = {
-						component="gun", 
-						weaponType="customcannon",
-						group="primary",
-						interact="mountedGun",
-						commander = true,
-						avf_barrel_coords_true = true
-
-					},
-					template = "2A13"
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

# Migration Report: avf\prefabs\weapon_templates\weapon_sights_templates.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\weapon_templates\weapon_sights_templates.lua
+++ patched/avf\prefabs\weapon_templates\weapon_sights_templates.lua
@@ -1,21 +1,16 @@
-
-
+#version 2
 function test_sight() 
 	DebugWatch("calling test site function")
 
 end
 
-
-
 function test_import() 
 	DebugWatch("calling test sight function")
 
 end
 
-
 function igla_scope(gun,gun_details) 
 	-- DebugWatch("calling IGLA sight function")
-
 
 end
 
@@ -71,7 +66,7 @@
 	local height = UiHeight() 
 	local w = UiWidth()
 	UiPush()
-		if dist > 0 then
+		if dist ~= 0 then
 			-- DebugWatch("dist ",dist)
 			-- DebugWatch("xy ",x)
 			-- DebugWatch("w",w)
@@ -89,7 +84,6 @@
 end
 
 function CROWS_MG(focus_gun,val)
-
 
 	-- DebugWatch("loaded magazine",GetTagValue(focus_gun,"avf.databus.loaded_magazine"))
 	local loaded_magazine =tonumber(GetTagValue(focus_gun,"avf.databus.loaded_magazine"))		 	
@@ -146,7 +140,7 @@
 		local height = UiHeight() 
 		local w = UiWidth()
 		UiPush()
-			if dist > 0 then
+			if dist ~= 0 then
 				UiFont("bold.ttf", 12)
 				-- DebugWatch("dist ",dist)
 				-- DebugWatch("xy ",x)
@@ -177,9 +171,9 @@
 	UiPop()
 end
 
-
-
-function JAVELIN_SIGHT(weapon,weapon_payload)
+function
+
+ELIN_SIGHT(weapon,weapon_payload)
 	-- SetTag(gun.id,"avf.databus.TRACKING_TARGET",gun.missile_guidance_tracking_target)
 	-- SetTag(gun.id,"avf.databus.CURRENT_TRACK",gun.missile_guidance_current_track)
 	-- SetTag(gun.id,"avf.databus.TARGET_LOCKED", gun.missile_guidance_current_track>MISSILE_TRACK_TIME_MIN)
@@ -240,7 +234,7 @@
 		local height = UiHeight() 
 		local w = UiWidth()
 		UiPush()
-			if dist > 0 then
+			if dist ~= 0 then
 				-- DebugWatch("dist ",dist)
 				-- DebugWatch("xy ",x)
 				-- DebugWatch("w",w)
@@ -257,3 +251,4 @@
 	UiPop()
 						
 end
+

```

---

# Migration Report: avf\prefabs\weapon_templates\weapon_templates.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\weapon_templates\weapon_templates.lua
+++ patched/avf\prefabs\weapon_templates\weapon_templates.lua
@@ -1,2410 +1 @@
-
---[[
-	use this file to config the parameters for your tank
-
-	Feel free to rename this to the name of your tank
-
-
-
-]]
-
-templates = {
-
-
---[[
-
-
-	Tank Cannons
-
-
-]]
-
-		["2A46"] = {
-
-
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
-								RHAe 					= 550,
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
-								RHAe 					= 454,
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
-								RHAe 					= 42,
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
-					RPM 					= 12,
-					reload 					= 6,
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
-
-
-		["2A46M"] = {
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
-								RHAe 					= 550,
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
-								RHAe 					= 454,
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
-								RHAe 					= 42,
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
-					RPM 					= 8,
-					reload 					= 8,
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
-
-				},
-
-
-		["2A46M1"] = {
-
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
-								RHAe 					= 550,
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
-								RHAe 					= 454,
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
-								RHAe 					= 42,
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
-					RPM 					= 15,
-					reload 					= 4.5,
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
---[[
-
-	#############################################################################
-
-
-							AUTOCANNONS
-		
-
-	#############################################################################
-
-
-
-]]
-
-
-
-
-	["2A13"] = {
-		name = "23 mm 2A13 autocannons",
-		weaponType 				= "cannon",
-		caliber 				= 23,
-		default = "B_23mm_AA",
-		magazines 					= {
-								[1] = {
-										name = "B_23mm_AA",
-										magazineCapacity = 100,
-										ammoCount = 0,
-										magazineCount = 50,
-										caliber 				= 23,
-										velocity				= 220,
-										explosionSize 			= .55,
-										RHAe 					= 2,
-										timeToLive 				= 7,
-										launcher				= "cannon",
-										payload					= "HE",
-										shellWidth				= 0.1,
-										shellHeight				= 0.7,
-										r						= 0.5,
-										g						= 0.5, 
-										b						= 0.5, 
-										tracer 					= 1,
-										tracerL					= 5,
-										tracerW					= 2,
-										tracerR					= 1.8,
-										tracerG					= 1.0, 
-										tracerB					= 1.0, 
-										shellSpriteName			= "MOD/gfx/shellModel2.png",
-										shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-																						
-									},
-								[2] = {
-										name = "B_23mm_AA_AP",
-										magazineCapacity = 200,
-										ammoCount = 0,
-										magazineCount = 10,			
-										caliber 				= 23,
-										velocity				= 220,
-										explosionSize 			= .6,
-										RHAe 					= 48,
-										timeToLive 				= 7,
-										launcher				= "cannon",
-										payload					= "AP",
-										shellWidth				= 0.1,
-										shellHeight				= 0.7,
-										r						= 0.5,
-										g						= 0.5, 
-										b						= 0.5, 
-										tracer 					= 1,
-										tracerL					= 5,
-										tracerW					= 2,
-										tracerR					= 1.8,
-										tracerG					= 1.0, 
-										tracerB					= 1.0, 
-										shellSpriteName			= "MOD/gfx/shellModel2.png",
-										shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-
-									},
-								},
-		loadedMagazine 			= 1,
-		barrels = 
-					{
-						[1] = {x=0.2,y=.1,z=-1.2},
-						[2] = {x=0.6,y=.1,z=-1.2},
-					},
-		multiBarrel 			= 1,
-		sight					= {
-									[1] = {
-									x = 1.2,
-									y = 1.3,
-									z = 0.3,
-									},
-
-
-									},
-		canZoom					= false,
-		highVelocityShells		= true,
-		RPM 					= 350,
-		reload 					= 4,
-		cannonBlast				= 0.1,
-		recoil 					= 0.05,
-		weapon_recoil 			= 2400,
-		dispersion 				= 20,
-		gunRange				= 500,
-		gunBias 				= -1,
-		smokeFactor 			= .5,
-		smokeMulti				= 1,
-		soundFile   = "MOD/sounds/autocannons/zsu_23_2_single",
-		mouseDownSoundFile 			=	"MOD/sounds/autocannons/zsu_23_2_sub_burst_02",
-	},
-
-
---[[
-
-	#############################################################################
-
-
-							ARTILLERY
-		
-
-	#############################################################################
-
-
-
-]]
-
-
-
-	["D-30"] = {
-		name = "D-30 Artillary",
-		weaponType 				= "cannon",
-		caliber 				= 152,
-		default = "152mm_HE",
-		magazines 					= {
-								[1] = {
-										name = "152mm_HE",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 300,
-										caliber 				= 152,
-										velocity				= 200,
-										gravityCoef				= 12,
-										explosionSize			= 3.5,
-										RHAe 					= 12,
-										timeToLive 				= 7,
-										launcher				= "cannon",
-										payload					= "HE",
-										shellWidth				= .5,
-										shellHeight				= 1,
-										r						= 0.8,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/shellModel2.png",
-										shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-								},
-								[2] =  {
-										name = "BK-6M HEAT",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 50,
-										caliber 				= 152,
-										velocity				= 150,
-										explosionSize			= 1.2,
-										RHAe 					= 510,
-										timeToLive 				= 7,
-										gravityCoef 			= 14,--0.3,
-										launcher				= "cannon",
-										payload					= "HEAT",
-										shellWidth				= .5,
-										shellHeight				= 1,
-										r						= 0.3,
-										g						= 0.8, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/shellModel2.png",
-										shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											
-			},
-							},
-		loadedMagazine 			= 1,
-		barrels 				= 
-									{
-										[1] = {x=0.2,y=0.2,z=-0.3},
-									},
-		multiBarrel 			= 1,
-		sight					= {
-									[1] = {
-									x = 3,
-									y = 1.3,
-									z = 0.3,
-										},
-
-									},
-		canZoom					= true,
-		highVelocityShells		= true,
-		cannonBlast 			= 1,
-		RPM 					= 10,
-		reload 					= 2,
-		recoil 					= 0.05,
-		weapon_recoil 			= 750,
-		dispersion 				= 15,
-		gunRange				= 500,
-		gunBias 				= -1,
-		elevationSpeed			= .3,
-		smokeFactor 			= 3,
-		smokeMulti				= 20,
-		soundFile				= "MOD/sounds/Relic_700_KV2Fire",
-	},
-
-
-
-
-
---[[
-
-	#############################################################################
-
-
-							Anti Tank rockets and ATGMS
-		
-
-	#############################################################################
-
-
-
-]]
-		["SPG9"] = {
-			name 	= "SPG-9",
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
-													RHAe 					= 400,
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
-													RHAe 					= 5,
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
-
-
-		["9M133"]  = {
-					name 	= "9M133 Kornet",
-					weaponType 				= "atgm",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-										name = "9M133M-2",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 152,
-										velocity				= 20,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.2,
-										RHAe 					= 1100,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										payload					= "HEAT",
-										shellWidth				= 0.8,
-										shellHeight				= 1.5,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.3,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0.6,
-												y = 1.2,
-												z = -.7,
-													},
-
-
-												},
-					backBlast				= 
-												{
-													[1] = {z=1.3,force=5},
-												},
-					canZoom					= true,
-					aimForwards				= true,
-					zoomSight 				= "MOD/gfx/KORNETsight.png",
-					highVelocityShells		= true,
-					RPM 					= 20,
-					reload 					= 2,
-					recoil 					= 0,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.4,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/atgm00",
-				},
-
-		["MILAN"]  = {
-					name 	= "MILAN ",
-					weaponType 				= "atgm",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-										name = "MILAN-2 ",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 125,
-										velocity				= 40,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.45,
-										maxPenDepth 			= 1.8,
-										RHAe 					= 1000,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										payload					= "HEAT",
-										chargeType					= "tandem",
-										shellWidth				= 0.5,
-										shellHeight				= 1.25,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.3,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0.6,
-												y = 1.2,
-												z = -.7,
-													},
-					scope_offset 			= {
-												[1] = {
-													x = 0.00,
-													y = 0.01
-													},
-											},
-
-
-												},
-					backBlast				= 
-												{
-													[1] = {z=1.3,force=5},
-												},
-					canZoom					= true,
-					aimForwards				= true,
-					zoomSight 				= "MOD/gfx/KORNETsight.png",
-					highVelocityShells		= true,
-					RPM 					= 20,
-					reload 					= 2,
-					cannonBlast				= 0.1,
-					recoil 					= 0,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.2,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/atgm00",
-				},
-
-		["MILAN_02"]  = {
-					name 	= "MILAN ",
-					weaponType 				= "atgm",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-										name = "MILAN-2 ",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 125,
-										velocity				= 60,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.45,
-										maxPenDepth 			= 1.8,
-										RHAe 					= 1000,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										payload					= "HEAT",
-										shellWidth				= 0.5,
-										shellHeight				= 1.25,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.3,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0.6,
-												y = 1.2,
-												z = -.7,
-													},
-					scope_offset 			= {
-												[1] = {
-													x = 0.00,
-													y = 0.00
-													},
-											},
-
-
-												},
-					backBlast				= 
-												{
-													[1] = {z=1.3,force=5},
-												},
-					canZoom					= true,
-					aimForwards				= true,
-					zoomSight 				= "MOD/gfx/KORNETsight.png",
-					highVelocityShells		= true,
-					RPM 					= 20,
-					reload 					= 2,
-					cannonBlast				= 0.1,
-					recoil 					= 0,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.2,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/atgm00",
-				},
-
-
-
-
-
-		["igla"]  = {
-					name 	= "9K38 Igla",
-					weaponType 				= "atgm",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-										name = "9M39 TOP DOWN",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 72,
-										velocity				= 60,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.0,
-										RHAe		 			= 760,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										guidance 				= "homing",
-										attack_pattern 				= "top_down",
-										missile_ramp_speed = 0.85,
-										guidance_peak_dist = 50,
-										guidance_height_ratio = 0.8,
-										payload					= "HEAT",
-										chargeType=				'tandem',
-										shellWidth				= 0.8,
-										shellHeight				= 1.5,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											[2] = {
-										name = "9M39 DIRECT",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 72,
-										velocity				= 60,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.0,
-										RHAe		 			= 760,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										guidance 				= "homing",
-										attack_pattern 				= "direct",
-										missile_ramp_speed = 0.85,
-										guidance_peak_dist = 50,
-										guidance_height_ratio = 0.8,
-										payload					= "HEAT",
-										chargeType=				'tandem',
-										shellWidth				= 0.8,
-										shellHeight				= 1.5,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											[3] = {
-										name = "9M39 TOP DOWN_close",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 72,
-										velocity				= 60,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.0,
-										RHAe		 			= 760,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										guidance 				= "homing",
-										attack_pattern 				= "top_down",
-										missile_ramp_speed = 0.85,
-										guidance_peak_dist = 25,
-										guidance_height_ratio = 1.8,
-										payload					= "HEAT",
-										chargeType=				'tandem',
-										shellWidth				= 0.8,
-										shellHeight				= 1.5,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-										[4] = {
-												name = "PG9_AT",
-												magazineCapacity = 1,
-												ammoCount = 0,
-												magazineCount = 100,
-												caliber 				= 73,
-												velocity				= 430,
-												explosionSize			= 1,
-												gravityCoef 			= 1.25,
-												RHAe 					= 400,
-												timeToLive 				= 12,
-												launcher				= "rocket",
-												payload					= "HEAT",
-												shellWidth				= 0.8,
-												shellHeight				= 1.5,
-												r						= 0.3,
-												g						= 0.8, 
-												b						= 0.3, 
-												shellSpriteName			= "MOD/gfx/rocketModel.png",
-												shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-
-											},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.3,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0.6,
-												y = 1.2,
-												z = -.7,
-													},
-
-
-												},
-
-					backBlast				= 
-												{
-													[1] = {z=1.3,force=5},
-												},
-					canZoom					= true,
-					aimForwards				= true,
-					zoomSight 				= "MOD/gfx/KORNETsight.png",
-					highVelocityShells		= true,
-					RPM 					= 20,
-					reload 					= 2,
-					recoil 					= 0,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.4,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/atgm00",
-				},
-
-
-
-
-
-
-
-		["javelin"]  = {
-					name 	= "FGM-148 Javelin",
-					weaponType 				= "atgm",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-										name = "TOP DOWN",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 72,
-										velocity				= 60,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.0,
-										RHAe		 			= 760,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										guidance 				= "homing",
-										attack_pattern 				= "top_down",
-										missile_ramp_speed = 0.85,
-										guidance_peak_dist = 50,
-										guidance_height_ratio = 0.8,
-										payload					= "HEAT",
-										chargeType=				'tandem',
-										shellWidth				= 0.8,
-										shellHeight				= 1.5,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											[2] = {
-										name = "DIRECT",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 72,
-										velocity				= 60,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.0,
-										RHAe		 			= 760,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										guidance 				= "homing",
-										attack_pattern 				= "direct",
-										missile_ramp_speed = 0.85,
-										guidance_peak_dist = 50,
-										guidance_height_ratio = 0.8,
-										payload					= "HEAT",
-										chargeType=				'tandem',
-										shellWidth				= 0.8,
-										shellHeight				= 1.5,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											[3] = {
-										name = "TOP DOWN_close",
-										magazineCapacity = 1,
-										ammoCount = 0,
-										magazineCount = 60,
-										caliber 				= 72,
-										velocity				= 60,
-										gravityCoef 			= 0,
-										dispersionCoef 			= 0,
-										explosionSize			= 1.0,
-										RHAe		 			= 760,
-										timeToLive 				= 12,
-										launcher				= "guided",
-										guidance 				= "homing",
-										attack_pattern 				= "top_down",
-										missile_ramp_speed = 0.85,
-										guidance_peak_dist = 25,
-										guidance_height_ratio = 1.8,
-										payload					= "HEAT",
-										chargeType=				'tandem',
-										shellWidth				= 0.8,
-										shellHeight				= 1.5,
-										r						= 0.9,
-										g						= 0.3, 
-										b						= 0.3, 
-										shellSpriteName			= "MOD/gfx/rocketModel.png",
-										shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-										flightLoop				= "MOD/sounds/rocketFlightLoop0",
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.3,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0.6,
-												y = 1.2,
-												z = -.7,
-													},
-
-
-												},
-
-					backBlast				= 
-												{
-													[1] = {z=1.3,force=5},
-												},
-					canZoom					= true,
-					aimForwards				= true,
-					zoomSight 				= "MOD/gfx/KORNETsight.png",
-					highVelocityShells		= true,
-					RPM 					= 20,
-					reload 					= 2,
-					recoil 					= 0,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.4,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/atgm00",
-				},
-
---[[
-
-	#############################################################################
-
-
-							MACHINE GUNS / Grenade Machine Guns
-		
-
-	#############################################################################
-
-
-
-]]
-
-
-	["GMG"] = {
-					name 	= "L134A1",
-					caliber 				= 30,
-					weaponType 				= "GMGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-									name = "40 mm grenade",
-									magazineCapacity = 60,
-									ammoCount = 0,
-									magazineCount = 50,
-									caliber 				= 40,
-									velocity				= 180,
-									gravityCoef 			= 1.7,
-									explosionSize			= .7,
-									maxPenDepth 			= 0.17,
-									RHAe 					= 50,
-									timeToLive 				= 20,
-									launcher				= "cannon",
-									payload					= "HE",
-									shellWidth				= 0.3,
-									shellHeight				= .55,
-									r						= 0.6,
-									g						= 0.3, 
-									b						= 0.3, 
-									shellSpriteName			= "MOD/gfx/shellModel2.png",
-									shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0.65,y=0.3,z=-0.1},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = 0.15,
-											y = 0.9,
-											z = 1.68,
-												},
-
-
-											},
-				canZoom					= false,
-				aimForwards				= true,
-				RPM 					= 340 ,
-				cannonBlast				= 0.1,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.1,
-
-				weapon_recoil 					= 0.0005,
-				dispersion 				= 10,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/grenade_mg/single_shot_01",
-				mouseDownSoundFile 		=	"MOD/sounds/grenade_mg/auto_01",
-				loopSoundFile			= 	"MOD/sounds/grenade_mg/auto_01",
-				tailOffSound	 		=	"MOD/sounds/grenade_mg/auto_tail_off_01",				
-				},
-	["GMG_02"] = {
-					name 	= "40 KRKK 2005",
-					caliber 				= 30,
-					weaponType 				= "GMGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-									name = "40 mm grenade",
-									magazineCapacity = 60,
-									ammoCount = 0,
-									magazineCount = 50,
-									caliber 				= 40,
-									velocity				= 180,
-									gravityCoef 			= 1.7,
-									explosionSize			= .7,
-									maxPenDepth 			= 0.17,
-									RHAe 					= 50,
-									timeToLive 				= 20,
-									launcher				= "cannon",
-									payload					= "HE",
-									shellWidth				= 0.3,
-									shellHeight				= .55,
-									r						= 0.6,
-									g						= 0.3, 
-									b						= 0.3, 
-									shellSpriteName			= "MOD/gfx/shellModel2.png",
-									shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0.65,y=0.3,z=-0.1},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = 0.15,
-											y = 0.9,
-											z = 1.68,
-												},
-
-
-											},
-				canZoom					= false,
-				aimForwards				= true,
-				RPM 					= 340 ,
-				cannonBlast				= 0.1,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.1,
-
-				weapon_recoil 					= 0.0005,
-				dispersion 				= 10,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/grenade_mg/single_shot_01",
-				mouseDownSoundFile 		=	"MOD/sounds/grenade_mg/auto_01",
-				loopSoundFile			= 	"MOD/sounds/grenade_mg/auto_01",
-				tailOffSound	 		=	"MOD/sounds/grenade_mg/auto_tail_off_01",				
-				},
-
-		["PKT"]		= {
-					name 	= "PKT",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_762x54_Ball",
-													magazineCapacity = 250,
-													RHAe 					= 12,
-													ammoCount = 0,
-													magazineCount = 20,
-												},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-				sight					= {
-												[1] = {
-											x = 3,
-											y = 1.3,
-											z = 0.3,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 750,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.02,
-				dispersion 				= 3,
-				gunRange				= 1000,
-				elevationSpeed			= 3,
-				smokeFactor 			= .25,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/lmgSingle0",
-				mouseDownSoundFile 		=	"MOD/sounds/lmgBurst0",
-
-				},
-
-
-	["DSHK"]	= {	
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
-													RHAe 					= 27.5,
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
-
-	["NSV"]	= {	
-					name 	= "NSV",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "12.7×108mm",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 240,
-													hit 					=3,
-													maxPenDepth 			= 0.36,
-													RHAe 					= 27.5,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.2,
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
-				RPM 					= 370,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.05,
-				weapon_recoil 			= 50,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .9,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/HeavySingleShot",
-				mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"MOD/sounds/HeavyAutoFire",			
-				},
-
-	["PKT"]		= {
-					name 	= "PKT",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-								name = "B_762x54_Ball",
-								magazineCapacity = 250,
-								ammoCount = 0,
-								magazineCount = 20,
-								caliber 				= 7.62,
-								velocity				= 350,
-								maxPenDepth 			= 0.15,
-								RHAe 					= 12,
-								timeToLive 				= 7,
-								launcher				= "mgun",
-								payload					= "AP",
-								shellWidth				= 0.1,
-								shellHeight				= 0.3,
-								r						= 0.8,
-								g						= 0.8, 
-								b						= 0.5, 
-								tracer 					= 5,
-								tracerL					= 6,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-				sight					= {
-												[1] = {
-											x = 3,
-											y = 1.3,
-											z = 0.3,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 750,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.02,
-				dispersion 				= 3,
-				gunRange				= 1000,
-				elevationSpeed			= 3,
-				smokeFactor 			= .25,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/lmgSingle0",
-				mouseDownSoundFile 		=	"MOD/sounds/lmgBurst0",
-
-				},
-
-
-
-	["L1A1"]	= {	
-					name 	= "L111A1 HMG",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = ".50 BMG",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 250,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.5,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.6,
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
-				weapon_recoil 			= 5,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/m2_single_01",
-				mouseDownSoundFile 		=	"MOD/sounds/machine_gun/m2_burst_01",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/m2_loop_03",		
-				},
-
-
-
-	["L1A1_2"]	= {	
-					name 	= "L111A1 HMG",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = ".50 BMG",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 250,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.5,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.6,
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
-				weapon_recoil 			= 50,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/m2_single_01",
-				mouseDownSoundFile 		=	"MOD/sounds/machine_gun/m2_burst_01",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/m2_loop_03",		
-				},
-
-
-
-
-
-
-	["M2"]	= {	
-					name 	= "M2 HMG",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = ".50 BMG",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 250,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.7,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.6,
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
-				weapon_recoil 			= 25,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .8,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/m2_single_01",
-				mouseDownSoundFile 		=	"MOD/sounds/machine_gun/m2_burst_01",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/m2_loop_03",		
-				},
-
-
-
-
-	["Tksp"]	= {	
-					name 	= "Tksp 12,7 mm",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "12.7×99mm NATO",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 250,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.7,
-													RHAe 					= 25,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.6,
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
-				weapon_recoil 			= 25,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .8,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/m2_single_01",
-				mouseDownSoundFile 		=	"MOD/sounds/machine_gun/m2_burst_01",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/m2_loop_03",		
-				},
-
-
-
-	["KSP_88"]	= {	
-					name 	= "Ksp 88",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "12.7×99mm NATO",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 250,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.8,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1.6,
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
-				weapon_recoil 			= 25,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .8,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/m2_single_01",
-				mouseDownSoundFile 		=	"MOD/sounds/machine_gun/m2_burst_01",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/m2_loop_03",		
-				},
-
-
-	["KSP_88_2"]	= {	
-					name 	= "KSP_88_2",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "12.7×99mm NATO 50m",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 50,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.8,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1,
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
-											[2] = {
-													name = "12.7×99mm NATO 100m",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 100,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.8,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1,
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
-											[3] = {
-													name = "12.7×99mm NATO 200m",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 200,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.8,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1,
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
-				weapon_recoil 			= 25,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .8,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/m2_single_01",
-				mouseDownSoundFile 		=	"MOD/sounds/machine_gun/m2_burst_01",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/m2_loop_03",		
-				},
-
-
-
-	["KSP_88_CROWS"]	= {	
-					name 	= "KSP_88_CROWS",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-						[1] = {
-													name = "12.7×99mm NATO 50m",
-													magazineCapacity = 150,
-													ammoCount = 0,
-													magazineCount = 50,
-													caliber 				= 12.7,
-													velocity				= 350,
-													hit 					=3,
-													maxPenDepth 			= 0.31,
-													RHAe 					= 27.8,
-													timeToLive 				= 7,
-													launcher				= "mgun",
-													payload					= "AP",
-													gravityCoef 			= 1,
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
-											-- [1] = {
-											-- 		name = "12.7×99mm NATO 50m",
-											-- 		magazineCapacity = 10,
-											-- 		ammoCount = 0,
-											-- 		magazineCount = 50,
-											-- 		caliber 				= 12.7,
-											-- 		velocity				= 50,
-											-- 		hit 					=3,
-											-- 		maxPenDepth 			= 0.31,
-											-- 		RHAe 					= 27.8,
-											-- 		timeToLive 				= 7,
-											-- 		launcher				= "mgun",
-											-- 		payload					= "AP",
-											-- 		gravityCoef 			= 1,
-											-- 		shellWidth				= 0.1,
-											-- 		shellHeight				= 0.3,
-											-- 		r						= 0.8,
-											-- 		g						= 0.8, 
-											-- 		b						= 0.5, 
-											-- 		tracer 					= 2,
-											-- 		tracerL					= 7,
-											-- 		tracerW					= 2,
-											-- 		tracerR					= 1.8,
-											-- 		tracerG					= 1.0, 
-											-- 		tracerB					= 1.0, 
-											-- 		shellSpriteName			= "MOD/gfx/shellModel2.png",
-											-- 		shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											-- },
-											-- [2] = {
-											-- 		name = "12.7×99mm NATO 100m",
-											-- 		magazineCapacity = 100,
-											-- 		ammoCount = 0,
-											-- 		magazineCount = 50,
-											-- 		caliber 				= 12.7,
-											-- 		velocity				= 100,
-											-- 		hit 					=3,
-											-- 		maxPenDepth 			= 0.31,
-											-- 		RHAe 					= 27.8,
-											-- 		timeToLive 				= 7,
-											-- 		launcher				= "mgun",
-											-- 		payload					= "AP",
-											-- 		gravityCoef 			= 1,
-											-- 		shellWidth				= 0.1,
-											-- 		shellHeight				= 0.3,
-											-- 		r						= 0.8,
-											-- 		g						= 0.8, 
-											-- 		b						= 0.5, 
-											-- 		tracer 					= 2,
-											-- 		tracerL					= 7,
-											-- 		tracerW					= 2,
-											-- 		tracerR					= 1.8,
-											-- 		tracerG					= 1.0, 
-											-- 		tracerB					= 1.0, 
-											-- 		shellSpriteName			= "MOD/gfx/shellModel2.png",
-											-- 		shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											-- },
-											-- [3] = {
-											-- 		name = "12.7×99mm NATO 200m",
-											-- 		magazineCapacity = 100,
-											-- 		ammoCount = 0,
-											-- 		magazineCount = 50,
-											-- 		caliber 				= 12.7,
-											-- 		velocity				= 200,
-											-- 		hit 					=3,
-											-- 		maxPenDepth 			= 0.31,
-											-- 		RHAe 					= 27.8,
-											-- 		timeToLive 				= 7,
-											-- 		launcher				= "mgun",
-											-- 		payload					= "AP",
-											-- 		gravityCoef 			= 1,
-											-- 		shellWidth				= 0.1,
-											-- 		shellHeight				= 0.3,
-											-- 		r						= 0.8,
-											-- 		g						= 0.8, 
-											-- 		b						= 0.5, 
-											-- 		tracer 					= 2,
-											-- 		tracerL					= 7,
-											-- 		tracerW					= 2,
-											-- 		tracerR					= 1.8,
-											-- 		tracerG					= 1.0, 
-											-- 		tracerB					= 1.0, 
-											-- 		shellSpriteName			= "MOD/gfx/shellModel2.png",
-											-- 		shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-											-- },
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
-				zeroing 				= 100,
-				reload 					= 4,
-				magazineCapacity 		= 10,
-				weapon_recoil 			= 25,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				elevationSpeed			= .8,
-				smokeFactor 			= .1,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/m2_single_01",
-				mouseDownSoundFile 		=	"MOD/sounds/machine_gun/m2_burst_01",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/m2_loop_03",
-				custom_fire_sound		= {
-										num_sounds = 6,
-										file_name = "MOD/avf/snd/nsv/nsv_shot_"
-											},
-				custom_mouse_down		= true,
-				custom_loop_sound_file	= {
-										num_sounds = 1,
-										file_name = "MOD/avf/snd/nsv/nsv_loop_"
-											},
-				custom_tail_off			= true,
-				custom_reload			= true,
-				special_custom_sounds = 
-										{
-											reload_sounds			= {
-												reload_type 	= "loop_and_sound",
-												reload_loop = "MOD/avf/snd/nsv/nsv_reload_loop",
-												reloaded_sound = "MOD/avf/snd/nsv/nsv_reloaded",
-											},
-										}
-
-				},
-
-
-	["GPMG"]		= {
-					name 	= "L7A2 GPMG",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-								name = "B_762x54_Ball",
-								magazineCapacity = 200,
-								ammoCount = 0,
-								magazineCount = 20,
-								caliber 				= 7.62,
-								velocity				= 350,
-								maxPenDepth 			= 0.05,
-								RHAe 					= 13,
-								timeToLive 				= 7,
-								launcher				= "mgun",
-								payload					= "AP",
-								gravityCoef 			= 2,
-								shellWidth				= 0.1,
-								shellHeight				= 0.3,
-								r						= 0.8,
-								g						= 0.8, 
-								b						= 0.5, 
-								tracer 					= 5,
-								tracerL					= 6,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-				sight					= {
-												[1] = {
-											x = 3,
-											y = 1.3,
-											z = 0.3,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 750,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				weapon_recoil 			= 5,
-				dispersion 				= 3,
-				gunRange				= 1000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .05,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/gpmg_single_02",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/gpmg_loop_02",
-
-				},
-
-
-
-	["GPMG_02"]		= {
-					name 	= "KSP 58",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-								name = "7.62x51 NATO",
-								magazineCapacity = 200,
-								ammoCount = 0,
-								magazineCount = 20,
-								caliber 				= 7.62,
-								velocity				= 350,
-								maxPenDepth 			= 0.05,
-								RHAe 					= 13,
-								timeToLive 				= 7,
-								launcher				= "mgun",
-								payload					= "AP",
-								gravityCoef 			= 2,
-								shellWidth				= 0.1,
-								shellHeight				= 0.3,
-								r						= 0.8,
-								g						= 0.8, 
-								b						= 0.5, 
-								tracer 					= 5,
-								tracerL					= 6,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-				sight					= {
-												[1] = {
-											x = 3,
-											y = 1.3,
-											z = 0.3,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 750,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				weapon_recoil 			= 5,
-				dispersion 				= 3,
-				gunRange				= 1000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .05,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/gpmg_single_02",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/gpmg_loop_02",
-
-				},
-
-
-
-	["GPMG_custom_sound"]		= {
-					name 	= "KSP 58",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-								name = "7.62x51 NATO",
-								magazineCapacity = 200,
-								ammoCount = 0,
-								magazineCount = 20,
-								caliber 				= 7.62,
-								velocity				= 350,
-								maxPenDepth 			= 0.05,
-								RHAe 					= 13,
-								timeToLive 				= 7,
-								launcher				= "mgun",
-								payload					= "AP",
-								gravityCoef 			= 2,
-								shellWidth				= 0.1,
-								shellHeight				= 0.3,
-								r						= 0.8,
-								g						= 0.8, 
-								b						= 0.5, 
-								tracer 					= 5,
-								tracerL					= 6,
-								tracerW					= 2,
-								tracerR					= 1.8,
-								tracerG					= 1.0, 
-								tracerB					= 1.0, 
-								shellSpriteName			= "MOD/gfx/shellModel2.png",
-								shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-
-
-	},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0,y=0.2,z=-0.6},
-											},
-				multiBarrel 			= 1,
-				sight					= {
-												[1] = {
-											x = 3,
-											y = 1.3,
-											z = 0.3,
-												},
-
-
-											},
-				canZoom					= false,
-				RPM 					= 750,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				weapon_recoil 			= 5,
-				dispersion 				= 3,
-				gunRange				= 1000,
-				elevationSpeed			= .5,
-				smokeFactor 			= .05,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/machine_gun/gpmg_single_02",
-				loopSoundFile 		=	"MOD/sounds/machine_gun/gpmg_loop_02",
-				custom_fire_sound		= {
-										num_sounds = 6,
-										file_name = "MOD/avf/snd/nsv/nsv_shot_"
-											},
-				custom_mouse_down		= true,
-				custom_loop_sound_file	= true,
-				custom_tail_off			= true,
-				custom_reload			= true,
-
-				},
-}
-	
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
@@ -1,139 +1,4 @@
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
-custom_sound_types = {
-	[1] = "custom_fire_sound",
-	[2] = "custom_mouse_down",
-	[3] = "custom_loop_sound_file",
-	[4] = "custom_reload",
-
-}
-
-
-ai_locations = {
-	[1] = "ai_commander",
-
-}
-
-DEBUG = false
-DEBUG_EJECTORS  =false
-
-collision_items_index = 1
-collision_mask_index = 1
-collision_items = {
-
-
-}
-
-custom_weapon_sounds = {
-	primary_weapons = {},
-	coax_weapons = {
-
-	}
-
-
-}
-
-filters = {
-	[1] = 2,
-	[2] = 4,
-	[3] = 8,
-	[4] = 16,
-	[5] = 32 ,
-	[6] = 64,
-	[7] = 128,
-}
-
-
-
-vehicle_alive = true
-
-hull_filter = 0
-turret_filter = 0
-gun_filter = 0
-
-filter_max = 255
--- SetShapeCollisionFilter(a, 2, 255-2)
-
-function init()
-	hull_filter = filters[math.random(1,3)] --1+ math.floor((filter_max/2*math.random())-1)
-	turret_filter = filters[math.random(4,5)]
-	gun_filter = filters[math.random(6,7)] --(filter_max/2)+ math.floor((filter_max/2*math.random())-1)
-	local custom_sight_script = false
-	-- DebugPrint("starting")
-	for key,val in pairs(vehicleParts.guns) do 
-		custom_sight_script = false
-		if(val.custom_sight_script) then 
-			custom_sight_script = true
-		end
-		custom_sight_template = nil
-		if(val.custom_sight_template) then 
-			custom_sight_template = val.custom_sight_template
-		end
-		if(val.cfgWeapon ~= nil) then 
-			cfg_weapon(key,val.cfgWeapon)
-		end
-
-		if(val.template ~= nil) then 
-			-- DebugPrint("tasdss")
-			vehicleParts.guns[key]= deepcopy(templates[val.template])
-			vehicleParts.guns[key].custom_sight_script = custom_sight_script
-			vehicleParts.guns[key].custom_sight_template = custom_sight_template
-		end
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
-		SetTag(sceneVehicle,"SPAWNED_AVF_VEHICLE")
-
-		SetBool("level.avf.vehicle_spawned", true)
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
@@ -141,7 +6,6 @@
 	vehicle.shapes = GetBodyShapes(vehicle.body)
 
 	init_ai_elements()
-
 
 	local totalShapes = ""
 	for i=1,#vehicle.shapes do
@@ -189,11 +53,6 @@
 	end
 end
 
-
---[[
-
-	loads  custom weapon sounds and adds to custom_weapon_sounds dict
-]]
 function init_custom_sounds(key,gun)
 	local sound_type = ""
 	for i =1,#custom_sound_types do 
@@ -208,8 +67,8 @@
 
 	end 
 
-
-end
+end
+
 function init_gun_sounds(key,gun,sound_type,weapon_class) 
 	loaded_sounds = {}
 	local index_num = ""
@@ -261,7 +120,6 @@
 		end
 	end
 
-
 end
 
 function traverseTurret(turretJoint,attatchedShape)
@@ -335,7 +193,7 @@
 	local val3 = GetTagValue(gun, "component")
 	return val3
 end
--- @magazine1_tracer
+
 function addItems(shape,values)
 	for key,val in pairs(values) do 
 			if(key=="coax") then 
@@ -419,15 +277,6 @@
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
@@ -519,7 +368,6 @@
 	end
 end
 
-
 function add_emitter_group(gun,gun_transform,gun_key,emitter_group,emitters,emitter_type,turret_mounted) 
 	for i =1,#emitters do
 		local emitter_transform = GetLocationTransform(emitters[i]) 
@@ -585,17 +433,6 @@
 
 end
 
-
---[[
-
-
-mainCannon component=gun weaponType=customcannon commander avf_barrel_coords_true
-
-				 group=primary interact=mountedGun
-
-]]
-
-
 function cfg_weapon(gun_id,cfgWeapon)
 	local gun = FindShape(gun_id)
 
@@ -604,19 +441,6 @@
 	end	
 end
 
-
-
---[[
-
-
-	ai location handling
-
-	ai_locations = {
-	[1] = "ai_commander",
-
-	}
-
-]]
 function add_ai_locations()
 	
 	for i=1,#ai_locations do 
@@ -634,7 +458,6 @@
 	end
 end
 
-
 function add_ai_location_group(emitter_group,emitters,emitter_type) 
 	for i =1,#emitters do
 		local emitter_transform = GetLocationTransform(emitters[i]) 
@@ -652,7 +475,6 @@
 
 end
 
-
 function append_to_collision_filter(item1,item2,index)
 	if(not collision_items[index]) then 
 		collision_items[index] = {}
@@ -664,52 +486,6 @@
 	}
 
 end
-
-
-function tick(dt)
-	if(vehicle_alive) then
-		if(custom_avf_sounds) then 
-			custom_avf_sounds()
-		end 
-		if(HasTag(vehicle.id, "vehicle_disabled")) then 
-			vehicle_alive= false
-
-		end
-	end
-end
-
--- function update(dt)
--- 	maintain_collision_filters()
--- end
-
-
-
-function draw(dt)
-	if(check_AVF.enabled) then 
-		check_AVF:draw()
-	end
-
-	if(vehicle_alive) then 
-		if(player_in_vehicle())then
-
-
-			-- if( GetBool("level.avf.sniper_mode") )then 
-			-- 	DebugWatch("avf sniper mode","active")
-			-- else
-
-			-- 	DebugWatch("avf sniper mode","inactive")
-			-- end
-			if(custom_avf_ui) then 
-				custom_avf_ui()
-			end
-		end
-	end
-
-end
-
-
-
-
 
 function retrieve_first_barrel_coord(gun,gun_id)
 	local barrel = nil
@@ -736,7 +512,6 @@
 	
 	return cannonLoc
 end
-
 
 function add_vehicle_vel(pos,vehicle_id)
 	return VecAdd(
@@ -753,7 +528,7 @@
 end
 
 function player_in_vehicle()
-	local playerVehicle = GetPlayerVehicle()
+	local playerVehicle = GetPlayerVehicle(playerId)
 
 	if(vehicle.id == playerVehicle) then 
 		return true
@@ -776,11 +551,84 @@
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
+    hull_filter = filters[math.random(1,3)] --1+ math.floor((filter_max/2*math.random())-1)
+    turret_filter = filters[math.random(4,5)]
+    gun_filter = filters[math.random(6,7)] --(filter_max/2)+ math.floor((filter_max/2*math.random())-1)
+    local custom_sight_script = false
+    -- DebugPrint("starting")
+    for key,val in pairs(vehicleParts.guns) do 
+    	custom_sight_script = false
+    	if(val.custom_sight_script) then 
+    		custom_sight_script = true
+    	end
+    	custom_sight_template = nil
+    	if(val.custom_sight_template) then 
+    		custom_sight_template = val.custom_sight_template
+    	end
+    	if(val.cfgWeapon ~= nil) then 
+    		cfg_weapon(key,val.cfgWeapon)
+    	end
+
+    	if(val.template ~= nil) then 
+    		-- DebugPrint("tasdss")
+    		vehicleParts.guns[key]= deepcopy(templates[val.template])
+    		vehicleParts.guns[key].custom_sight_script = custom_sight_script
+    		vehicleParts.guns[key].custom_sight_template = custom_sight_template
+    	end
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
+    	SetTag(sceneVehicle,"SPAWNED_AVF_VEHICLE")
+    	SetBool("level.avf.vehicle_spawned", true, true)
+    	SetTag(sceneVehicle,"AVF_Custom","unset")
+    	-- DebugPrint("vehicle configured!!")
+    	check_AVF:init(sceneVehicle)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(vehicle_alive) then
+        	if(custom_avf_sounds) then 
+        		custom_avf_sounds()
+        	end 
+        	if(HasTag(vehicle.id, "vehicle_disabled")) then 
+        		vehicle_alive= false
+
+        	end
+        end
+    end
+end
+
+function client.draw()
+    if(check_AVF.enabled) then 
+    	check_AVF:draw()
+    end
+
+    if(vehicle_alive) then 
+    	if(player_in_vehicle())then
+
+    		-- if( GetBool("level.avf.sniper_mode") )then 
+    		-- 	DebugWatch("avf sniper mode","active")
+    		-- else
+
+    		-- 	DebugWatch("avf sniper mode","inactive")
+    		-- end
+    		if(custom_avf_ui) then 
+    			custom_avf_ui()
+    		end
+    	end
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
 		UiMakeInteractive()
 		self:drawMessage()
 		if((InputPressed(self.hideKey[0])or InputDown(self.hideKey[0])) and
@@ -51,7 +39,6 @@
 				[5] = "and enabled in the mod manager",
 				[6] = "Otherwise this tank won't shoot",
 				[7] = "press ctrl+c to hide",
-
 
 		}
 		header = "Armed Vehicle Framework (AVF)"
@@ -79,4 +66,5 @@
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
@@ -1,220 +1,4 @@
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
-min_tank_health = 0.6
-
-fuel_health_reduction = 0.25
-
-
-engine_damage_reduction = 0.15
-
-normal_kill_intensity = 40
-health_kill_intensity = 40
-unarmed_kill_intensity = 25
-unarmed = false
-
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
-		if(#tank.ammo_racks==0) then 
-			unarmed = true
-		end
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
-		else
-			tank.cook_off_origin =Transform(VecAdd(GetBodyCenterOfMass(GetVehicleBody(tank.id)),Vec(0,0.5,0)))
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
 	if(tank.id~= nil and IsHandleValid(tank.id)) then 
@@ -235,7 +19,6 @@
 			
 			check_generic_survival_conditions()
 		elseif(tank.burning_off and not tank.burned_off) then 
-
 
 			burn_off()
 			simulate_engine_disabled()
@@ -268,7 +51,6 @@
 		-- DebugWatch("cooking off",cook_off_value)
 	end
 end
-
 
 function kill_tank(max_intensity)
 	min_intensity = 5
@@ -290,7 +72,6 @@
 	-- end
 
 end
-
 
 function check_engine_state()
 	-- if(#tank.engines>0) then 
@@ -327,7 +108,6 @@
 	end
 end
 
-
 function simulate_engine_disabled()
 	-- DriveVehicle(tank.id,0,0,true)
 	-- if(IsHandleValid(base_vehicle)) then 
@@ -351,8 +131,6 @@
 		SpawnParticle(engine_pos.pos, v, life)
 	end
 end
-
-
 
 function check_fuel_tank_state()
 	for i = 1,#tank.fuel_tanks do 
@@ -393,7 +171,6 @@
 		end
 	end
 end
-
 
 function animated_fuel_leak(engine_pos,count, vel)
 	for i=1, count do
@@ -452,7 +229,6 @@
 					tank.cooking_off = true
 					break_all_breakable_joints()
 
-
 				--	DebugPrint("ammo rack destroyed! cooking off")
 					cook_off_intensity = math.random(1,10)
 					if(cook_off_intensity<=2 and min_cook_off<4) then 
@@ -503,8 +279,6 @@
 	end
 end
 
-
-
 function break_all_breakable_joints()
 	for i=1,#breakable_joints do 
 		-- DebugPrint("i"..i)
@@ -575,10 +349,6 @@
 				
 			end
 
-
-
-
-
 			if(tank.hatches_blown<3 and  cook_off_value>0.2) then 
 				apply_impulse(transform)
 				
@@ -591,8 +361,6 @@
 			end
 
 			
-
-
 
 		elseif(cook_off_pulse>=1) then
 			cook_off_pulse=0
@@ -627,7 +395,6 @@
 
 end
 
-
 function tank_ignition(transform)
 	local hitLocations = {nil,nil,nil}
 	for i=1,3 do 
@@ -647,7 +414,6 @@
 	end
 	spawn_cookoff_debris(transform.pos)
 end
-
 
 function burn_off()
 
@@ -687,7 +453,6 @@
 			end
 			spawn_cookoff_debris(pos)
 
-
 	elseif(cook_off_pulse>=1) then
 		cook_off_pulse=0
 	end
@@ -709,7 +474,6 @@
 		end
 
 	end
-
 
 	local strength = math.random(cook_off_blast_min_strength,cook_off_blast_max_strength)	--Strength of blower
 	local small_strength = strength*.25
@@ -727,7 +491,6 @@
 	--Loop through bodies and push them
 	for i=1,#bodies do
 		local b = bodies[i]
-
 
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
@@ -764,7 +527,6 @@
 	for i=1,#bodies do
 		local b = bodies[i]
 
-
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
 		local bc = VecLerp(bmi, bma, 0.5)
@@ -793,8 +555,7 @@
 		end
 	end
 
-
-end 
+end
 
 function kill_tracks()
 	for i=1,#tank.tracks do 
@@ -804,7 +565,6 @@
 
 	end
 end
-
 
 function kill_lights()
 	local lights = FindLights()
@@ -837,7 +597,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			
@@ -850,11 +610,11 @@
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
 
@@ -864,7 +624,7 @@
 				
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.015 * strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.015 * strength * amount * distScale)
 				end
 			end	
 		end
@@ -885,12 +645,10 @@
 	spawn_entity(pos,xml,vel)
 end
 
-
 function spawn_entity(pos,xml,vel,burn)
 	local entities = Spawn(xml, Transform(pos))
 
 	--Set velocity on spawned bodies (only one in this case)
-
 
 	for i=1, #entities do
 		if GetEntityType(entities[i]) == "body" then
@@ -907,9 +665,7 @@
 	end
 end
 
-
 function apply_impulse(transform )
-
 
 	local strength = math.random(10,250)	--Strength of blower
 	local maxMass = 500	--The maximum mass for a body to be affected
@@ -926,7 +682,6 @@
 	--Loop through bodies and push them
 	for i=1,#bodies do
 		local b = bodies[i]
-
 
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
@@ -957,15 +712,9 @@
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
@@ -974,10 +723,6 @@
 function rndVec(t)
 	return Vec(rnd(-t, t), rnd(-t, t), rnd(-t, t))
 end
-
-explosionPos = Vec()
-
-trails = {}
 
 function trailsAdd(pos, vel, life, size, damp, gravity)
 	t = {}
@@ -1023,14 +768,6 @@
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
@@ -1053,11 +790,6 @@
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
@@ -1081,11 +813,6 @@
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
@@ -1094,11 +821,6 @@
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
@@ -1175,7 +897,6 @@
 	smoke.amount = 2
 end
 
-
 function explosionMedium(pos)
 	explosionPos = pos
 	explosionSparks(30, 3)
@@ -1205,7 +926,6 @@
 	smoke.gravity = 2
 	smoke.amount = 2
 end
-
 
 function explosionLarge(pos)
 	explosionPos = pos
@@ -1251,11 +971,150 @@
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
+    	if(#tank.ammo_racks==0) then 
+    		unarmed = true
+    	end
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
+    	else
+    		tank.cook_off_origin =Transform(VecAdd(GetBodyCenterOfMass(GetVehicleBody(tank.id)),Vec(0,0.5,0)))
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

# Migration Report: target_tracks\moving_range_target.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/target_tracks\moving_range_target.lua
+++ patched/target_tracks\moving_range_target.lua
@@ -1,45 +1,35 @@
-
-
-track_distance = 2
-
-function init() 
-	track_driver = FindJoint("track_driver")
-	turn_dial = FindJoint("turn_dial")
-
-	track_driver_min, track_driver_max = GetJointLimits(track_driver)
-
-	turn_dial_min, turn_dial_max = GetJointLimits(turn_dial)
-	track_speed = math.random(4,8)
-
-	change_dist = 0.92
-	max_dist = 0.96
-	side = "max"
-
-
-	shift_time = 1
+#version 2
+function server.init()
+    track_driver = FindJoint("track_driver")
+    turn_dial = FindJoint("turn_dial")
+    track_driver_min, track_driver_max = GetJointLimits(track_driver)
+    turn_dial_min, turn_dial_max = GetJointLimits(turn_dial)
+    track_speed = math.random(4,8)
+    change_dist = 0.92
+    max_dist = 0.96
+    side = "max"
+    shift_time = 1
 end
 
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(GetJointMovement(track_driver)<(track_driver_min+track_driver_max*(1-change_dist)) and side =="max") then 
+        	SetJointMotorTarget(turn_dial,turn_dial_min+turn_dial_max*(1-change_dist),track_speed)
+        	SetValue("track_distance",2,"linear",shift_time)
+        	side = "min"
+        elseif(GetJointMovement(track_driver)>(track_driver_max*change_dist) and side =="min") then 
+        	SetJointMotorTarget(turn_dial,turn_dial_max*change_dist,track_speed)
+        	SetValue("track_distance",0,"linear",shift_time)
+        	side = "max"
+        end
+        if(track_distance == 0) then 
+        	SetJointMotorTarget(track_driver,track_driver_min+track_driver_max*(1-max_dist),track_speed)
+        	track_distance=1
+        elseif(track_distance ==2) then 
 
-function tick()
-	-- DebugWatch("track movement",GetJointMovement(track_driver))
-	-- DebugWatch("track dist ",track_distance)
-	-- DebugWatch("side  ",side)
-	if(GetJointMovement(track_driver)<(track_driver_min+track_driver_max*(1-change_dist)) and side =="max") then 
-		SetJointMotorTarget(turn_dial,turn_dial_min+turn_dial_max*(1-change_dist),track_speed)
-		SetValue("track_distance",2,"linear",shift_time)
-		side = "min"
-	elseif(GetJointMovement(track_driver)>(track_driver_max*change_dist) and side =="min") then 
-		SetJointMotorTarget(turn_dial,turn_dial_max*change_dist,track_speed)
-		SetValue("track_distance",0,"linear",shift_time)
-		side = "max"
-	end
+        	SetJointMotorTarget(track_driver,track_driver_max*max_dist,track_speed)
+        	track_distance=1
+        end
+    end
+end
 
-	if(track_distance == 0) then 
-		SetJointMotorTarget(track_driver,track_driver_min+track_driver_max*(1-max_dist),track_speed)
-		track_distance=1
-	elseif(track_distance ==2) then 
-
-		SetJointMotorTarget(track_driver,track_driver_max*max_dist,track_speed)
-		track_distance=1
-	end
-end
```

---

# Migration Report: voxscript\ground.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/voxscript\ground.lua
+++ patched/voxscript\ground.lua
@@ -1,37 +1,29 @@
-file = GetString("file", "testground.png", "script png")
-heightScale = GetInt("scale", 64)
-tileSize = GetInt("tilesize", 128)
-hollow = GetInt("hollow", 0)
+#version 2
+function server.init()
+    matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
+    matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
+    matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
+    matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
+    matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
+    matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
+    matTarmacLine = CreateMaterial("dirt", 0.66, 0.57, 0.42, 1, 0, 0.1)
+    LoadImage(file)
+    w,h = GetImageSize()
+    local maxSize = tileSize
+    local y0 = 0
+    while y0 < h-1 do
+    	local y1 = y0 + maxSize
+    	if y1 > h-1 then y1 = h-1 end
 
-function init()
-	matRock = CreateMaterial("rock", 0.3, 0.3, 0.3)
-	matDirt = CreateMaterial("dirt", 0.26, 0.23, 0.20, 1, 0, 0.1)
-	matGrass1 = CreateMaterial("unphysical", 0.17, 0.21, 0.15, 1, 0, 0.2)
-	matGrass2 = CreateMaterial("unphysical", 0.19, 0.24, 0.17, 1, 0, 0.2)
-	matTarmac = CreateMaterial("masonry", 0.35, 0.35, 0.35, 1, 0, 0.4)
-	matTarmacTrack = CreateMaterial("masonry", 0.2, 0.2, 0.2, 1, 0, 0.3)
-	matTarmacLine = CreateMaterial("dirt", 0.66, 0.57, 0.42, 1, 0, 0.1)
-	
-	LoadImage(file)
-	
-	w,h = GetImageSize()
-
-	local maxSize = tileSize
-	
-	local y0 = 0
-	while y0 < h-1 do
-		local y1 = y0 + maxSize
-		if y1 > h-1 then y1 = h-1 end
-
-		local x0 = 0
-		while x0 < w-1 do
-			local x1 = x0 + maxSize
-			if x1 > w-1 then x1 = w-1 end
-			Vox(x0, 0, y0)
-			Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
-			x0 = x1
-		end
-		y0 = y1
-	end
+    	local x0 = 0
+    	while x0 < w-1 do
+    		local x1 = x0 + maxSize
+    		if x1 > w-1 then x1 = w-1 end
+    		Vox(x0, 0, y0)
+    		Heightmap(x0, y0, x1, y1, heightScale, hollow==0)
+    		x0 = x1
+    	end
+    	y0 = y1
+    end
 end
 

```
