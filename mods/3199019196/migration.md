# Migration Report: scripts\ava.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ava.lua
+++ patched/scripts\ava.lua
@@ -1,27 +1,6 @@
-#include "config.lua"
-#include "vehicle.lua"
-#include "plane.lua"
-#include "helicopter.lua"
-#include "lighting.lua"
-#include "landing.lua"
-#include "ui.lua"
-#include "surfaces.lua"
-#include "cockpit.lua"
-#include "panels.lua"
-#include "weapons.lua"
-#include "ramp.lua"
-#include "vtol.lua"
-#include "hook.lua"
-#include "utility.lua"
-#include "particles.lua"
-
-folder = GetStringParam("name", "")
-debug_mode = GetBoolParam("debug", false)
-initialised = false
-
-function init()
+#version 2
+function server.init()
     param = aircraft_config[folder]
-
     if not initialised then
         config_init()
         vehicle_init()
@@ -44,56 +23,58 @@
     end
 end
 
-function tick(dt)
-    delta = dt
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        delta = dt
+        update_variables()
+        vehicle_tick()
+        lighting_tick()
+        interact_tick()
+        cockpit_tick()
+        landing_tick()
+        if hasHook then hook_tick() end
+        if hasRamp then ramp_tick() end    
+        if hasVTOL then vtol_tick() end
+        if hasFlaps then surfaces_tick() end    
+        if param.loadout ~= nil or param.weapons ~= nil then weapons_tick() end
 
-    update_variables()
-    vehicle_tick()
-    lighting_tick()
-    interact_tick()
-    cockpit_tick()
-    landing_tick()
+        if not aircraft.crashed then
+            if (param.type == "helicopter") then
+                if not hasVTOL then
+                    helicopter_flight_tick(1)
+                else                    
+                    helicopter_flight_tick(1 - vtolDone)
+                    plane_flight_tick(vtolDone)
+                end
+            end
 
-    if hasHook then hook_tick() end
-    if hasRamp then ramp_tick() end    
-    if hasVTOL then vtol_tick() end
-    if hasFlaps then surfaces_tick() end    
-    if param.loadout ~= nil or param.weapons ~= nil then weapons_tick() end
-
-    if not aircraft.crashed then
-        if (param.type == "helicopter") then
-            if not hasVTOL then
-                helicopter_flight_tick(1)
-            else                    
-                helicopter_flight_tick(1 - vtolDone)
-                plane_flight_tick(vtolDone)
-            end
-        end
-
-        if (param.type == "plane") then
-            if not hasVTOL then
-                plane_flight_tick(1)
-            else
-                plane_flight_tick(1 - vtolDone)
-                helicopter_flight_tick(vtolDone)
+            if (param.type == "plane") then
+                if not hasVTOL then
+                    plane_flight_tick(1)
+                else
+                    plane_flight_tick(1 - vtolDone)
+                    helicopter_flight_tick(vtolDone)
+                end
             end
         end
     end
 end
 
-function update()    
-    if not HasTag(aircraft.vehicle, "spawning") then
-        if not isProp then
-            SetBodyAngularVelocity(aircraft.body, aircraft.angular)
-            SetBodyVelocity(aircraft.body, aircraft.velocity)
-        else
-            SetBodyAngularVelocity(aircraft.body, Vec(0, 0, 0))
-            SetBodyVelocity(aircraft.body, Vec(0, 0.18, 0))
-        end 
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not HasTag(aircraft.vehicle, "spawning") then
+            if not isProp then
+                SetBodyAngularVelocity(aircraft.body, aircraft.angular)
+                SetBodyVelocity(aircraft.body, aircraft.velocity)
+            else
+                SetBodyAngularVelocity(aircraft.body, Vec(0, 0, 0))
+                SetBodyVelocity(aircraft.body, Vec(0, 0.18, 0))
+            end 
+        end
     end
 end
 
-function draw()
+function client.draw()
     UiPush()
         if debug_mode then
            debugging_ui()
@@ -109,12 +90,12 @@
                     info[1] = {string.upper(start_key), "Start Engine"}
                 end
             end
-            
+
             if GetBool("savegame.mod.ava.keys.ui_controls") then
                 controls_ui()
             end
         end
-        
+
         if GetBool("savegame.mod.ava.keys.ui_flight_display") then
             instruments_ui()
         end
@@ -124,7 +105,5 @@
             weapon_reticle_ui()
         end
     UiPop()
-end   
+end
 
-
-

```

---

# Migration Report: scripts\cockpit.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\cockpit.lua
+++ patched/scripts\cockpit.lua
@@ -1,3 +1,4 @@
+#version 2
 function cockpit_init()
     jointsCockpit = FindJoints("cockpit")
 
@@ -149,4 +150,5 @@
 
         ConstrainOrientation(stick, 0, transCyclic.rot, QuatRotateQuat(q, QuatEuler(rot_query.x, rot_query.y, rot_query.z)), 5)
     end
-end+end
+

```

---

# Migration Report: scripts\config.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\config.lua
+++ patched/scripts\config.lua
@@ -1,410 +1,4 @@
-
-param = nil
-heli_list = {"mh53", "ah64", "mi24", "ka52", "uh60", "v22", "uh1", "ch47", "mi8", "mh6", "mi26", "ka50", "206"}
-plane_list = {"172", "f4", "lancaster", "f16", "su27", "su25"}
-aircraft_order = {}
-
-for i=1, #heli_list do
-    table.insert(aircraft_order, heli_list[i])
-end
-for i=1, #plane_list do
-    table.insert(aircraft_order, plane_list[i])
-end
-
-projectile_list = {
-    ["agm65"] = {title = "AGM-65 Maverick", type = "missile"},
-    ["agm114"] = {title = "AGM-114 Hellfire", type = "missile"},
-    ["agm65"] = {title = "AGM-65 Maverick", type = "missile"},
-    ["s8"] = {title = "S-8", type = "rocket"},
-    ["hydra"] = {title = "Hydra-70", type = "rocket"},
-    ["at6"] = {title = "9K114 Shturm", type = "missile"},
-    ["vikhr"] = {title = "9K121 Vikhr", type = "missile"},
-    ["igla"] = {title = "9K38 Igla", type = "missile"},
-    ["aim9"] = {title = "AIM-9 Sidewinder", type = "missile"},
-    ["aim7"] = {title = "AIM-7 Sparrow", type = "missile"},
-    ["r73"] = {title = "Vympel R-73", type = "missile"},
-    ["r27"] = {title = "Vympel R-27", type = "missile"},
-    ["b500"] = {title = "500LB Bomb", type = "bomb"},
-    ["mk82"] = {title = "MK82 500LB Bomb", type = "bomb"},
-}
-
-aircraft_config = {
-    ["172"] = {
-        info = {maker = "Cessna", title = "172 Skyhawk", length = 8.28, year = 1955, wip = false},
-        flight = {terminal_velocity = 200, acceleration = 0.07, stabilisation = 0.001},
-        controls = {roll = 0.02, pitch = 0.007, yaw = 0.02, ground_yaw = 0.1},
-        exhaust = {type = "piston", init = 0.1, final = 0, force = 1},
-        path = "MOD/planes/172/",
-        type = "plane",
-    }, 
-    ["f4"] = {
-        info = {maker = "McDonnell Douglas", title = "F-4 Phantom II", length = 17.7, year = 1958, wip = false},
-        flight = {terminal_velocity = 300, acceleration = 0.1, stabilisation = 0.005},
-        controls = {roll = 0.06, pitch = 0.03, yaw = 0.04, ground_yaw = 0.2},
-        landing_order_index = {1, 2},
-        exhaust = {type = "jet", init = 0.5, final = 0.1},
-        path = "MOD/planes/f4/",
-        type = "plane",
-        loadout = {
-            {"mk82_3_0"}, 
-            {"aim9_2_0"}, 
-            {"mk82_3_0"}, 
-            {"aim7_1_0"},
-            {"aim7_1_0"},
-            {"mk82_3_0"}, 
-            {"aim9_2_0"},
-            {"mk82_3_0"}
-        },
-    },
-    ["lancaster"] = {
-        info = {maker = "Avro", title = "Lancaster", length = 21.1, year = 1941, wip = false},
-        flight = {terminal_velocity = 200, acceleration = 0.015, stabilisation = 0.001},
-        controls = {roll = 0.005, pitch = 0.003, yaw = 0.004, ground_yaw = 0.2},
-        landing_order_index = {1, 2},
-        engine_startup_sequence = {2, 1, 3, 4},
-        landing_speed = 0.8,
-        exhaust = {type = "piston", init = 0.1, final = 0.1, force = 1},
-        path = "MOD/planes/lancaster/",
-        type = "plane",
-        static_loadout = true,
-        loadout = {
-            {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}, {"b500_1_0"}
-        },
-        weapons = {
-            ["turret1"] = {title = "Forward Turret", delay = 0.1, idle = {-15, 0, 0}, active = 0, sound = "gun0", ammo = 500},
-            ["turret2"] = {title = "Mid Turret", delay = 0.1, idle = {-15, 0, 0}, active = 180, sound = "gun0", ammo = 500},
-            ["turret3"] = {title = "Rear Turret", delay = 0.1, idle = {0, 0, 0}, active = 90, sound = "gun0", ammo = 500}
-        },
-    },
-    ["f16"] = {
-        info = {maker = "General Dynamics", title = "F-16 Fighting Falcon", length = 14.80, year = 1974, wip = false},
-        flight = {terminal_velocity = 300, acceleration = 0.1, stabilisation = 0.005},
-        controls = {roll = 0.06, pitch = 0.03, yaw = 0.04, ground_yaw = 0.45},
-        landing_order_index = {1, 2},
-        exhaust = {type = "jet", init = 0.5, final = 0.1, force = 1},
-        path = "MOD/planes/f16/",
-        type = "plane",
-        weapons = {
-            ["cannon1"] = {title = "M61 Vulcan Cannon", delay = 0.02, sound = "cannon4", ammo = 500}
-        },
-        loadout = {
-            {"aim9_1_0"}, 
-            {"aim9_1_0"}, 
-            {"aim9_1_0"}, 
-            {"aim9_1_0"}, 
-            {"aim9_1_0"}, 
-            {"aim9_1_0"}, 
-            {"aim9_1_0"}, 
-            {"aim9_1_0"}
-        },
-    },
-
-    ["su27"] = {
-        info = {maker = "Sukhoi", title = "Su-27 'Flanker'", length = 21.9, year = 1985, wip = false},
-        flight = {terminal_velocity = 300, acceleration = 0.1, stabilisation = 0.005},
-        controls = {roll = 0.06, pitch = 0.03, yaw = 0.04, ground_yaw = 0.1},
-        landing_order_index = {1, 2, 3, 4},
-        exhaust = {type = "jet", init = 0.5, final = 0.1, force = 1},
-        path = "MOD/planes/su27/",
-        type = "plane",
-        weapons = {
-            ["cannon1"] = {title = "GSh-30-1 autocannon", delay = 0.02, sound = "cannon4", ammo = 500}
-        },
-        loadout = {
-            {"r73_1_0"}, 
-            {"r73_1_0"}, 
-            {"r73_1_0"}, 
-            {"r73_1_0"}, 
-            {"r73_1_0"}, 
-            {"r73_1_0"}, 
-            {"r73_1_0"}, 
-            {"r73_1_0"}
-        },
-    },
-    ["su25"] = {
-        info = {maker = "Sukhoi", title = "Su-25 'Frogfoot'", length = 15.5, year = 1981, wip = false},
-        controls = {roll = 0.04, pitch = 0.03, yaw = 0.015, ground_yaw = 0.1, lift = 0.15},
-        flight = {terminal_velocity = 300, acceleration = 0.1, stabilisation = 0.005},
-        exhaust = {type = "turbofan", init = 0.15, final = 0.1, force = 20},
-        landing_order_index = {1, 2, 1, 3, 4},
-        landing_order_bool = {true, true, false, true, true},
-        path = "MOD/planes/su25/",
-        type = "plane",
-        loadout = {
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}
-        },
-        weapons = {
-            ["cannon1"] = {title = "GSh-30-2 autocannon", delay = 0.02, sound = "cannon4", ammo = 250}
-        },
-    },
-    ["su57"] = {
-        info = {maker = "Sukhoi", title = "Su-57 'Felon'", length = 19.8, year = 2020, wip = true},
-        flight = {terminal_velocity = 300, acceleration = 0.1, stabilisation = 0.005},
-        controls = {roll = 0.06, pitch = 0.03, yaw = 0.04, ground_yaw = 0.1},
-        exhaust = {type = "jet", init = 0.7, final = 0.1},
-        landing_order_index = {1, 2, 3, 2, 4, 1},
-        landing_order_bool = {true, true, true, true, true, false},
-        type = "plane",
-        path = "MOD/planes/su57/",
-    },
-    -- ["mig15"] = {
-    --     info = {maker = "Mikoyan-Gurevich", title = "MiG-15 'Fagot'", length = 10, price = 11000000, wip = true},
-    --     controls = {roll = 0.04, pitch = 0.03, yaw = 0.015, lift = 0.15},
-    --     flight = {terminal_velocity = 300, acceleration = 0.1, stabilisation = 0.005},
-    --     exhaust = {type = "turbofan", init = 0.15, final = 0.1},
-    --     landing_order_index = {1, 2},
-    --     landing_order_bool = {true, true},
-    --     path = "MOD/planes/mig15/",
-    --     type = "plane",
-    -- },
-    ["spitfire"] = {
-        info = {maker = "Supermarine", title = "172 Skyhawk", length = 9.12, year = 1955, wip = false},
-        flight = {terminal_velocity = 200, acceleration = 0.05, stabilisation = 0.001},
-        controls = {roll = 0.02, pitch = 0.007, yaw = 0.02, ground_yaw = 0.1},
-        exhaust = {type = "piston", init = 0.1, final = 0, force = 1},
-        path = "MOD/planes/spitfire/",
-        type = "plane",
-    }, 
-    ["b17"] = {
-        info = {maker = "Boeing", title = "B-17 Flying Fortress", length = 21.1, year = 1941, wip = false},
-        flight = {terminal_velocity = 200, acceleration = 0.015, stabilisation = 0.001},
-        controls = {roll = 0.005, pitch = 0.003, yaw = 0.004, ground_yaw = 0.2},
-        landing_order_index = {1, 2},
-        engine_startup_sequence = {2, 1, 3, 4},
-        landing_speed = 0.8,
-        exhaust = {type = "piston", init = 0.1, final = 0.1, force = 1},
-        path = "MOD/planes/b17/",
-        type = "plane",
-        weapons = {
-            ["turret1"] = {title = "Forward Turret", delay = 0.1, idle = {-15, 0, 0}, active = 0, sound = "gun0", ammo = 500},
-            ["turret2"] = {title = "Mid Turret", delay = 0.1, idle = {-15, 0, 0}, active = 180, sound = "gun0", ammo = 500},
-            ["turret3"] = {title = "Rear Turret", delay = 0.1, idle = {0, 0, 0}, active = 90, sound = "gun0", ammo = 500}
-        },
-    },
-
-    ["f35"] = {
-        info = {maker = "Lockheed Martin", title = "F-35B Lightning II", length = 14.80, year = 1974, wip = true},
-        flight = {terminal_velocity = 250, acceleration = 0.3, stabilisation = 0.005},
-        controls = {roll = 0.06, pitch = 0.03, yaw = 0.02, ground_yaw = 0.1},
-        exhaust = {type = "jet", init = 0.5, final = 0.1, force = 5},
-        landing_order_index = {1, 2, 3, 1},
-        landing_order_bool = {true, true, true, false},
-        vtol_speed_change = 1,
-        vtol_terminal_velocity = 200,
-        vtol_controls = {roll = 0.005, pitch = 0.003, yaw = 0.004},
-        vtol_acceleration = 0.11,
-        path = "MOD/planes/f35/",
-        type = "plane",
-    },
-
-    ["mh53"] = {
-        info = {maker = "Sikorsky", title = "MH-53 Pave Low", length = 21, year = 1967, wip = false},
-        controls = {roll = 0.005, pitch = 0.003, yaw = 0.005},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.3, final = 0.1, force = 20},
-        landing_order_index = {1},
-        path = "MOD/helicopters/mh53/",
-        type = "helicopter",
-    },
-    ["ah64"] = {
-        info = {maker = "Boeing", title = "AH-64 Apache", length = 14.7, year = 1975, wip = false},
-        controls = {roll = 0.005, pitch = 0.003, yaw = 0.006},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        max_roll_angle = 1,
-        exhaust = {type = "turbine", init = 0.15, final = 0.1, force = 20},
-        loadout = {
-            {"hydra_12_0", "agm114_4_0"}, 
-            {"hydra_12_0", "agm114_4_0"}, 
-            {"hydra_12_0", "agm114_4_0"}, 
-            {"hydra_12_0", "agm114_4_0"}
-        },
-        weapons = {
-            ["turret1"] = {title = "M230 Chain Gun", delay = 0.1, idle = {0, -90, -8}, active = -90, sound = "cannon1", ammo = 1200}
-        },
-        path = "MOD/helicopters/ah64/",
-        type = "helicopter",
-    },
-    ["mi24"] = {
-        info = {maker = "Mil", title = "Mi-24 'Hind'", length = 17.3, year = 1973, wip = false},
-        controls = {roll = 0.0035, pitch = 0.003, yaw = 0.005},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.3, final = 0.1, force = 20},
-        max_roll_angle = 1,
-        counter_rotation = -0.0005,
-        landing_order_index = {1, 2, 1, 3},
-        landing_order_bool = {true, true, false, true},
-        loadout = {
-            {"at6_2_0"}, 
-            {"at6_2_0", "s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"at6_2_0", "s8_12_0"}, 
-            {"at6_2_0"}
-        },
-        weapons = {
-            ["cannon1"] = {title = "GSh-30-2 autocannon", delay = 0.02, sound = "cannon4", ammo = 250}
-        },
-        path = "MOD/helicopters/mi24/",
-        type = "helicopter",
-    },
-    ["ka52"] = {
-        info = {maker = "Kamov", title = "Ka-52 'Hokum B'", length = 13.5, year = 1997, wip = false},
-        controls = {roll = 0.006, pitch = 0.003, yaw = 0.007},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.3, final = 0.1, force = 20},
-        max_roll_angle = 1,
-        landing_order_index = {1, 2, 1, 3},
-        landing_order_bool = {true, true, false, true},
-        loadout = {
-            {"igla_3_0"}, 
-            {"s8_12_0", "igla_3_0", "vikhr_6_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0", "igla_3_0", "vikhr_6_0"}, 
-            {"igla_3_0"}
-        },
-        weapons = {
-            ["cannon1"] = {title = "2A42 autocannon", delay = 0.1, sound = "cannon5", ammo = 460}
-        },
-        path = "MOD/helicopters/ka52/",
-        type = "helicopter",
-    },
-
-    ["uh60"] = {
-        info = {maker = "Sikorsky", title = "UH-60 Black Hawk", length = 15.26, year = 1974, wip = false},
-        controls = {roll = 0.005, pitch = 0.003, yaw = 0.005},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.3, final = 0.1, force = 20},
-        path = "MOD/helicopters/uh60/",
-        type = "helicopter",
-        loadout = {
-            {"hydra_12_0", "agm114_4_0"}, 
-            {"hydra_12_0", "agm114_4_0"}, 
-            {"hydra_12_0", "agm114_4_0"}, 
-            {"hydra_12_0", "agm114_4_0"}
-        },
-    },
-    ["v22"] = {
-        info = {maker = "Bell Boeing", title = "V-22 Osprey", length = 17.48, year = 1989, wip = false},
-        controls = {roll = 0.005, pitch = 0.0015, yaw = 0.005},
-        flight = {terminal_velocity = 200, stabilisation = 0.001, acceleration = 0.11},
-        landing_order_index = {1, 2, 3, 1},
-        landing_order_bool = {true, true, true, false},
-        exhaust = {type = "turbine", init = 0.4, final = 0.3, force = 20},
-        vtol_speed_change = 0.23,
-        vtol_terminal_velocity = 250,
-        vtol_controls = {roll = 0.02, pitch = 0.007, yaw = 0.02},
-        vtol_acceleration = 0.2,
-        path = "MOD/helicopters/v22/",
-        type = "helicopter",
-    },
-    ["uh1"] = {
-        info = {maker = "Bell", title = "UH-1 Iroquois", length = 12.8, year = 1956, wip = false},
-        controls = {roll = 0.005, pitch = 0.003, yaw = 0.005},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.2, final = 0.1, force = 20},
-        path = "MOD/helicopters/uh1/",
-        type = "helicopter",
-    },
-    ["ch47"] = {
-        startup_time = 10,
-        stop_time = 20,
-        info = {maker = "Boeing", title = "CH-47 Chinook", length = 15.9, year = 1961, wip = false},
-        controls = {roll = 0.005, pitch = 0.0015, yaw = 0.005},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.3, final = 0.1, force = 20},
-        path = "MOD/helicopters/ch47/",
-        type = "helicopter",
-    },
-    ["mi8"] = {
-        info = {maker = "Mil", title = "Mi-8 'Hip'", length = 18, year = 1967, wip = false},
-        controls = {roll = 0.0025, pitch = 0.0015, yaw = 0.005},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.3, final = 0.1, force = 20},
-        counter_rotation = 0.0001,
-        max_roll_angle = 1,
-        path = "MOD/helicopters/mi8/",
-        type = "helicopter",
-        loadout = {
-            {"s8_12_0"},
-            {"s8_12_0"},
-            {"s8_12_0"},
-            {"s8_12_0"},
-            {"s8_12_0"},
-            {"s8_12_0"},
-        },
-    },
-    ["mh6"] = {
-        info = {maker = "Boeing", title = "MH-6 Little Bird", length = 7.5, year = 1963, wip = false},
-        controls = {roll = 0.006, pitch = 0.003, yaw = 0.0074},
-        flight = {terminal_velocity = 200, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.2, final = 0, force = 20},
-        counter_rotation = 0.002,
-        loadout = {
-            {"hydra_5_0", "agm114_2_0"}, 
-            {"hydra_5_0", "agm114_2_0"}
-        },
-        path = "MOD/helicopters/mh6/",
-        type = "helicopter",
-    },
-    ["mi26"] = {
-        startup_time = 10,
-        stop_time = 20,
-        info = {maker = "Mil", title = "Mi-26 'Halo'", length = 30, year = 1977, wip = false},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        controls = {roll = 0.004, pitch = 0.0015, yaw = 0.0025},
-        exhaust = {type = "turbine", init = 1, final = 0.1, force = 20},
-        path = "MOD/helicopters/mi26/",
-        type = "helicopter",
-    },
-    ["ka50"] = {
-        info = {maker = "Kamov", title = "Ka-50 'Hokum A'", length = 13.5, year = 1990, wip = false},
-        controls = {roll = 0.006, pitch = 0.003, yaw = 0.007},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.3, final = 0.1, force = 20},
-        max_roll_angle = 1,
-        landing_order_index = {1, 2, 1, 3},
-        landing_order_bool = {true, true, false, true},
-        loadout = {
-            {"s8_12_0", "vikhr_6_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0"}, 
-            {"s8_12_0", "vikhr_6_0"}
-        },
-        weapons = {
-            ["cannon1"] = {title = "2A42 autocannon", delay = 0.1, sound = "cannon5", ammo = 460}
-        },
-        path = "MOD/helicopters/ka50/",
-        type = "helicopter",
-    },
-    ["206"] = {
-        info = {maker = "Bell", title = "206 JetRanger", length = 10.15, year = 1967, wip = false},
-        controls = {roll = 0.005, pitch = 0.003, yaw = 0.005},
-        flight = {terminal_velocity = 150, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.15, final = 0.1, force = 4},
-        path = "MOD/helicopters/206/",
-        type = "helicopter",
-    },
-      ["s64"] = {
-        startup_time = 10,
-        stop_time = 20,
-        info = {maker = "Sikorsky", title = "S-64 Skycrane", length = 21.5, year = 1967, wip = true},
-        controls = {roll = 0.001, pitch = 0.0015, yaw = 0.0025},
-        flight = {terminal_velocity = 250, acceleration = 0.11},
-        exhaust = {type = "turbine", init = 0.4, final = 0.2, force = 10},
-        max_roll_angle = 1,
-        path = "MOD/helicopters/s64/",
-        type = "helicopter",
-    },
-}
-
+#version 2
 function config_init()    
     if (param.startup_time == nil) then
         param.startup_time = 4
@@ -457,4 +51,5 @@
     if param.vtol_terminal_velocity ~= nil then
         param.vtol_terminal_velocity = (param.vtol_terminal_velocity / 3.6)
     end
-end+end
+

```

---

# Migration Report: scripts\helicopter.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\helicopter.lua
+++ patched/scripts\helicopter.lua
@@ -1,4 +1,4 @@
-#include "utility.lua"
+#version 2
 local up_delta = {val = 0, max = 0.8}
 local down_delta = {val = 0, max = 0.8}
 
@@ -59,7 +59,7 @@
                 up_delta.val = up_delta.max
             end
         else
-            if up_delta.val > 0 then
+            if up_delta.val ~= 0 then
                 up_delta.val = up_delta.val - delta
             else
                 up_delta.val = 0
@@ -73,7 +73,7 @@
                 down_delta.val = down_delta.max
             end
         else
-            if down_delta.val > 0 then
+            if down_delta.val ~= 0 then
                 down_delta.val = down_delta.val - delta
             else
                 down_delta.val = 0
@@ -141,6 +141,7 @@
         end
     end
 end
+
 function verticalThrust()
     if not hasVTOL or (hasVTOL and not vtolMode and #propeller_list > 0) then
         local count = 0
@@ -280,7 +281,7 @@
         end
         roll.strength = 0.0002
     else
-        if rollAdd1 > 0 then
+        if rollAdd1 ~= 0 then
             rollAdd1 = rollAdd1 - rollDecreaseMultiplier
         else
             rollAdd1 = 0
@@ -295,7 +296,7 @@
         end
         roll.strength = 0.0002
     else
-        if rollAdd2 > 0 then
+        if rollAdd2 ~= 0 then
             rollAdd2 = rollAdd2 - rollDecreaseMultiplier
         else
             rollAdd2 = 0
@@ -371,4 +372,5 @@
             passiveBrake()
         end
     end
-end+end
+

```

---

# Migration Report: scripts\hook.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\hook.lua
+++ patched/scripts\hook.lua
@@ -1,3 +1,4 @@
+#version 2
 local hook_handles = {}
 local max_hook_detect_dist = 15
 local pp = Vec()
@@ -99,7 +100,6 @@
         local hit, dist, normal, shape = QueryRaycast(middle_hook_pos, Vec(0, -1, 0), max_hook_detect_dist)
         local pos = VecAdd(middle_hook_pos, VecScale(Vec(0, -1, 0), dist))
         local body = GetShapeBody(shape)
-
 
         if hit then
             local vehi = GetBodyVehicle(body)
@@ -204,7 +204,7 @@
                 end
             end
         else
-            if #hook_handles > 0 then
+            if #hook_handles ~= 0 then
                 for i=1, #hook_handles do
                     local handle = hook_handles[i]
                     Delete(handle)
@@ -213,4 +213,5 @@
             end
         end
     end
-end+end
+

```

---

# Migration Report: scripts\landing.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\landing.lua
+++ patched/scripts\landing.lua
@@ -1,3 +1,4 @@
+#version 2
 function landing_init()
     local landingBodies = FindBodies("landing")
     gearSound = LoadLoop("MOD/sounds/heavy_motor.ogg")
@@ -151,4 +152,5 @@
             end
         end
     end
-end+end
+

```

---

# Migration Report: scripts\level.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\level.lua
+++ patched/scripts\level.lua
@@ -1,18 +1,4 @@
-#include "utility.lua"
-#include "config.lua"
-
-active = GetBoolParam("enable", true)
-
-function init()
-	spawn_location = FindLocation("spawn", true)
-
-	-- SetString("savegame.mod.ava.start", "w=day,s=ground,p=MOD/helicopter/f4/,t=2#2#2#2#2#2#2#2#,")
-	
-	if active then
-		spawn_aircraft()
-	end
-end
-
+#version 2
 function spawn_aircraft()
 	local spawn_location_transform = GetLocationTransform(spawn_location)
 	local handles = Spawn(aircraft_config[string_parameter_extract("a")].path .. "aircraft.xml", spawn_location_transform, true, true)
@@ -24,5 +10,14 @@
 			vehicle = h
 		end
 	end
-	SetPlayerVehicle(vehicle)
-end+	SetPlayerVehicle(playerId, vehicle)
+end
+
+function server.init()
+    spawn_location = FindLocation("spawn", true)
+    -- SetString("savegame.mod.ava.start", "w=day,s=ground,p=MOD/helicopter/f4/,t=2#2#2#2#2#2#2#2#,")
+    if active then
+    	spawn_aircraft()
+    end
+end
+

```

---

# Migration Report: scripts\lighting.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\lighting.lua
+++ patched/scripts\lighting.lua
@@ -1,3 +1,4 @@
+#version 2
 function lighting_init()
     lightsFound = FindBodies("light")
     soundToggle = LoadSound("MOD/sounds/torch.ogg")
@@ -236,3 +237,4 @@
         end
     end
 end
+

```

---

# Migration Report: scripts\menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\menu.lua
+++ patched/scripts\menu.lua
@@ -1,6 +1,4 @@
-#include "config.lua"
-#include "utility.lua"
-
+#version 2
 local helicopter_controls = {
 	{title = "Altitude Up", reset = "lmb", code = "altitude_up", type = "bind"},
 	{title = "Altitude Down", reset = "rmb", code = "altitude_down", type = "bind"},
@@ -11,7 +9,6 @@
 	{title = "Yaw Right", reset = "c", code = "yaw_right_h", type = "bind"},
 	{title = "Yaw Left", reset = "z", code = "yaw_left_h", type = "bind"},
 }
-
 local plane_controls = {
 	{title = "Throttle Up", reset = "lmb", code = "throttle_up", type = "bind"},
 	{title = "Throttle Down", reset = "rmb", code = "throttle_down", type = "bind"},
@@ -23,7 +20,6 @@
 	{title = "Yaw Right", reset = "c", code = "yaw_right_p", type = "bind"},
 	{title = "Yaw Left", reset = "z", code = "yaw_left_p", type = "bind"},
 }
-
 local function_controls = {
 	{title = "Start Engines", reset = "lmb", code = "start", type = "bind"},
 	{title = "Navigation Lights", reset = "n", code = "navigation", type = "bind"},
@@ -41,7 +37,6 @@
 	{title = "Switch Firing Mode", reset = "2", code = "switch_fwp", type = "bind"},
 	{title = "Infinite Ammo", reset = false, code = "infinite_ammo", type = "toggle"},
 }
-
 local misc_controls = {
 	{title = "UI Controls", reset = true, code = "ui_controls", type = "toggle"},
 	{title = "UI Flight Display", reset = true, code = "ui_flight_display", type = "toggle"},
@@ -54,9 +49,7 @@
 	{title = "Weapons", data = weapon_controls},
 	{title = "UI", data = misc_controls},
 }
-
 local slide = {time = 0, interval = 7, transition = 3, index = 0, max = 6}
-
 local statistics_dictionary = {
 	["level"] = {stat = "level", val = ""},
 	["heli"] = {stat = "favourite helicopter", val = ""},
@@ -68,19 +61,16 @@
 	-- ["destroyed"] = {stat = "vehicles destroyed", val = 0},
 }
 local statistics_order = {"heli", "plane", "owned", "time"}
-
 local performance_list = {
 	"speed",
 	"acceleration",
 	"maneuverability",
 }
-
 local filter_list = {
 	"all",
 	"helicopters",
 	"planes",
 }
-
 local mission_list = {
 	{title = "Tutorial", id = "tutorial", diff = "easy"},
 	{title = "Time Trial", id = "time0", diff = "easy"},
@@ -89,22 +79,18 @@
 	{title = "Convoy Elemination", id = "convoy0", diff = "easy"},
 	{title = "Airbase Attack", id = "airbase0", diff = "easy"},
 }
-
 local maps_list = {
 	["sandbox"] = {title = "Sandbox Map", description = ""}
 }
 local maps_order = {"sandbox"}
-
 local footer_constructor = {
 	{keys = {"wasd", "lmb"}, title = "navigation", offset = 45},
 }
-
 local aircraft_performance = {
 	speed = {val = 100, max = 0},
 	acceleration = {val = 100, max = 0},
 	maneuverability = {val = 100, max = 0},
 }
-
 local sandbox = {
 	weather = {"day", "night", "rainy", "snowy"},
 	starts = {"ground", "air"},
@@ -119,28 +105,24 @@
 	aircraft_loadout = {},
 	choose_loadout = {},
 }
-
 local fade = {
 	t = 0, 
 	max = 0.5, 
 	done = 1,
 	rate = 0.2
 }
-
 local options = {
 	index_p = 1, 
 	selected_code = "", 
 	waiting_for_key = false,
 	alpha = 1
 }
-
 local spawn_details = {
 	spawned = false, 
 	handles = {}, 
 	camera_focus_point, 
 	config = {}
 }
-
 local selection = {
 	offset = 0,
 	selected_index = 1,
@@ -153,17 +135,14 @@
 	selected_filter = "all",
 	info_lerp = 0
 }
-
 local owned = {}
 local lerp = {from = 0, to = 0}
 local camera = {x = 60, y = 20}
-
 local mouse_in = ""
 local all_aircraft_list = {}
 local sub_aircraft_list = {}
 local owned_aircraft_list = {}
 local footer_updated = false
-
 local page = "main"
 local sub_page = ""
 
@@ -174,15 +153,15 @@
 		local row = list.data[k]
 			
 		if row.type == "bind" then
-			SetString("savegame.mod.ava.keys." .. row.code, row.reset)
+			SetString("savegame.mod.ava.keys." .. row.code, row.reset, true)
 		end
 
 		if row.type == "toggle" then
-			SetBool("savegame.mod.ava.keys." .. row.code, row.reset)
+			SetBool("savegame.mod.ava.keys." .. row.code, row.reset, true)
 		end
 
 		if row.type == "multi" then
-			SetString("savegame.mod.ava.keys." .. row.code, row.choises[row.reset])
+			SetString("savegame.mod.ava.keys." .. row.code, row.choises[row.reset], true)
 		end
 	end
 end
@@ -289,7 +268,7 @@
 local function spawn_aircraft(name)
 	local found = false
 		
-	if #spawn_details.handles > 0 then
+	if #spawn_details.handles ~= 0 then
 		for i=1, #spawn_details.handles do
 			local h = spawn_details.handles[i]
 			Delete(h)
@@ -368,7 +347,6 @@
 			UiColor(1, 0, 0)
 			UiRoundedRect(val * w, h, 5)
 		UiPop()
-
 
 		UiPush()
 			UiColor(1, 1, 1)
@@ -772,7 +750,6 @@
 			-- 						selection.ordering = not selection.ordering
 			-- 					end
 
-
 			-- 					if fil == "filter" then
 			-- 						selection.filtering = not selection.filtering
 			-- 					end
@@ -984,7 +961,6 @@
 						UiPop()
 
 						UiTranslate(0, 30)
-
 
 						if (order == "map") then
 							if #maps_order > 3 then
@@ -1304,7 +1280,7 @@
 						end
 
 						local str = string.format("w=%s,m=%s,s=%s,a=%s,", sandbox.selected.weather, sandbox.selected.map, sandbox.selected.start, sandbox.selected.aircraft)
-						SetString("savegame.mod.ava.start", str)
+						SetString("savegame.mod.ava.start", str, true)
 						StartLevel("", string.format("MOD/%s.xml", path))
 					end
 				end
@@ -1516,7 +1492,7 @@
 		
 							if row.type == "toggle" then
 								local b = GetBool("savegame.mod.ava.keys." .. row.code)
-								SetBool("savegame.mod.ava.keys." .. row.code, not b)
+								SetBool("savegame.mod.ava.keys." .. row.code, not b, true)
 							end
 		
 							if row.type == "multi" then
@@ -1525,7 +1501,7 @@
 								else
 									row.index = 1
 								end	
-								SetString("savegame.mod.ava.keys." .. row.code, row.choises[row.index])
+								SetString("savegame.mod.ava.keys." .. row.code, row.choises[row.index], true)
 							end
 
 							PlaySound(click_sound)
@@ -1539,24 +1515,24 @@
 						local pressed_key = string.lower(InputLastPressedKey())
 						
 						if (string.len(pressed_key) > 0) then
-							SetString("savegame.mod.ava.keys." .. options.selected_code, pressed_key)
+							SetString("savegame.mod.ava.keys." .. options.selected_code, pressed_key, true)
 							options.waiting_for_key = false
 							options.selected_code = ""
 						else
 							if InputPressed("lmb") then
-								SetString("savegame.mod.ava.keys." .. options.selected_code, "lmb")
+								SetString("savegame.mod.ava.keys." .. options.selected_code, "lmb", true)
 								options.waiting_for_key = false
 								options.selected_code = ""
 							end
 
 							if InputPressed("mmb") then
-								SetString("savegame.mod.ava.keys." .. options.selected_code, "mmb")
+								SetString("savegame.mod.ava.keys." .. options.selected_code, "mmb", true)
 								options.waiting_for_key = false
 								options.selected_code = ""
 							end
 
 							if InputPressed("rmb") then
-								SetString("savegame.mod.ava.keys." .. options.selected_code, "rmb")
+								SetString("savegame.mod.ava.keys." .. options.selected_code, "rmb", true)
 								options.waiting_for_key = false
 								options.selected_code = ""
 							end
@@ -1704,83 +1680,19 @@
 
 			if (not HasKey("savegame.mod.ava.keys." .. row.code)) then
 				if row.type == "bind" then
-					SetString("savegame.mod.ava.keys." .. row.code, row.reset)
+					SetString("savegame.mod.ava.keys." .. row.code, row.reset, true)
 				end
 
 				if row.type == "toggle" then
-					SetBool("savegame.mod.ava.keys." .. row.code, row.reset)
+					SetBool("savegame.mod.ava.keys." .. row.code, row.reset, true)
 				end
 
 				if row.type == "multi" then
-					SetString("savegame.mod.ava.keys." .. row.code, row.choises[row.reset])
+					SetString("savegame.mod.ava.keys." .. row.code, row.choises[row.reset], true)
 				end
 			end
 		end
 	end
-end
-
-function init()
-	spawn_location = FindLocation("spawn", true)
-	spawn_transform = GetLocationTransform(spawn_location)
-	click_sound = LoadSound("MOD/sounds/click.ogg")
-
-	selection.selected_index = 1
-	spawn_details.spawned = false
-	apply_filter_list(aircraft_order)
-	calculate_flight_time()
-	check_null_keybinds()
-	read_owned_aircraft()
-	
-	local list = ListKeys("savegame.mod.ava.loadout")
-
-	-- SetString("savegame.mod.ava.new", "aircraft")
-	
-	for i=1, #owned_aircraft_list do
-		local air = owned_aircraft_list[i]
-		local loadout = aircraft_config[air].loadout
-
-		if loadout ~= nil and not inList(list, air)then
-			local lst = {}
-			for k=1, #loadout do
-				table.insert(lst, 1)
-			end
-
-			write_aircraft_loadout(air, lst)
-		end
-	end
-
-	sandbox.slider["aircraft"].max = (#owned_aircraft_list - 3) * 280
-
-	if #owned_aircraft_list > 0 then
-		if HasKey("savegame.mod.ava.start") then
-			sandbox.selected.aircraft = string_parameter_extract("a")
-			sandbox.selected.map = string_parameter_extract("m")
-
-			local found = false
-			for k=1, #maps_order do
-				local map = maps_order[k]
-				if (map == sandbox.selected.map) then
-					found = true
-				end
-			end	
-			if not found then
-				sandbox.selected.map = maps_order[1]
-			end
-		
-			sandbox.selected.weather = string_parameter_extract("w")
-			sandbox.selected.start = string_parameter_extract("s")
-		else
-			sandbox.selected.aircraft = owned_aircraft_list[1]
-			sandbox.selected.map = maps_order[1]
-			sandbox.selected.weather = sandbox.weather[1]
-			sandbox.selected.start = sandbox.starts[1]
-		end
-
-		statistics_dictionary["crashed"].val = GetInt("savegame.mod.ava.stats.crashed")
-
-		sandbox.aircraft_loadout = aircraft_config[sandbox.selected.aircraft].loadout
-		sandbox.choose_loadout = read_aircraft_loadout(sandbox.selected.aircraft)
-	end	
 end
 
 function main_ui(dt)
@@ -1853,68 +1765,130 @@
 	UiPop()
 end
 
-function draw(dt)	
-	if page == "main" then
-		main_ui(dt)
-	end
-
-	mouse_in = ""
-		
-	header_ui()
-	footer_ui()
-
-	fade.done = (fade.t / fade.max)
-
-	if (sub_page ~= "" and page == "main") then
-		fade.t = lerp_animate(fade.t, fade.max, fade.rate)
-	else	
-		fade.t = lerp_animate(fade.t, 0, fade.rate)
-	end
-
-	if fade.done > 0.99 then
-		fade.done = 1
-	end
-	if fade.done < 0.01 then
-		fade.done = 0
-	end
-
-	if page == "shop" then
-		shop_ui()
-	end
-
-	if (sub_page == "options") then
-		option_ui()
-	end
-
-	if (sub_page == "sandbox") then
-		sandbox_ui()
-	end
-
-	if (sub_page == "missions") then
-		mission_ui()
-	end
-
-	if InputPressed("backspace") then
-		footer_updated = false
-			
-		if sub_page ~= "" then
-			sub_page = ""
-			page = "main"
-			camera = {x = 60, y = 20}
-		end
-	end
-
-	if not footer_updated then
-		footer_constructor = {}
-		if page == "main" and sub_page == "" then
-			table.insert(footer_constructor, {keys = {"wasd", "lmb"}, title = "navigation", offset = 45})
-		end
-		if page == "shop" then
-			table.insert(footer_constructor, {keys = {"leftarrow", "right", "lmb"}, title = "navigation", offset = 45})
-		end
-		if sub_page == "sandbox" then
-			table.insert(footer_constructor, {keys = {"lmb"}, title = "navigation", offset = 45})
-		end
-		footer_updated = true
-	end
-end
+function server.init()
+    spawn_location = FindLocation("spawn", true)
+    spawn_transform = GetLocationTransform(spawn_location)
+    selection.selected_index = 1
+    spawn_details.spawned = false
+    apply_filter_list(aircraft_order)
+    calculate_flight_time()
+    check_null_keybinds()
+    read_owned_aircraft()
+    local list = ListKeys("savegame.mod.ava.loadout")
+    -- SetString("savegame.mod.ava.new", "aircraft", true)
+    for i=1, #owned_aircraft_list do
+    	local air = owned_aircraft_list[i]
+    	local loadout = aircraft_config[air].loadout
+
+    	if loadout ~= nil and not inList(list, air)then
+    		local lst = {}
+    		for k=1, #loadout do
+    			table.insert(lst, 1)
+    		end
+
+    		write_aircraft_loadout(air, lst)
+    	end
+    end
+    sandbox.slider["aircraft"].max = (#owned_aircraft_list - 3) * 280
+    if #owned_aircraft_list ~= 0 then
+    	if HasKey("savegame.mod.ava.start") then
+    		sandbox.selected.aircraft = string_parameter_extract("a")
+    		sandbox.selected.map = string_parameter_extract("m")
+
+    		local found = false
+    		for k=1, #maps_order do
+    			local map = maps_order[k]
+    			if (map == sandbox.selected.map) then
+    				found = true
+    			end
+    		end	
+    		if not found then
+    			sandbox.selected.map = maps_order[1]
+    		end
+
+    		sandbox.selected.weather = string_parameter_extract("w")
+    		sandbox.selected.start = string_parameter_extract("s")
+    	else
+    		sandbox.selected.aircraft = owned_aircraft_list[1]
+    		sandbox.selected.map = maps_order[1]
+    		sandbox.selected.weather = sandbox.weather[1]
+    		sandbox.selected.start = sandbox.starts[1]
+    	end
+
+    	statistics_dictionary["crashed"].val = GetInt("savegame.mod.ava.stats.crashed")
+
+    	sandbox.aircraft_loadout = aircraft_config[sandbox.selected.aircraft].loadout
+    	sandbox.choose_loadout = read_aircraft_loadout(sandbox.selected.aircraft)
+    end	
+end
+
+function client.init()
+    click_sound = LoadSound("MOD/sounds/click.ogg")
+end
+
+function client.draw()
+    if page == "main" then
+    	main_ui(dt)
+    end
+
+    mouse_in = ""
+
+    header_ui()
+    footer_ui()
+
+    fade.done = (fade.t / fade.max)
+
+    if (sub_page ~= "" and page == "main") then
+    	fade.t = lerp_animate(fade.t, fade.max, fade.rate)
+    else	
+    	fade.t = lerp_animate(fade.t, 0, fade.rate)
+    end
+
+    if fade.done > 0.99 then
+    	fade.done = 1
+    end
+    if fade.done < 0.01 then
+    	fade.done = 0
+    end
+
+    if page == "shop" then
+    	shop_ui()
+    end
+
+    if (sub_page == "options") then
+    	option_ui()
+    end
+
+    if (sub_page == "sandbox") then
+    	sandbox_ui()
+    end
+
+    if (sub_page == "missions") then
+    	mission_ui()
+    end
+
+    if InputPressed("backspace") then
+    	footer_updated = false
+
+    	if sub_page ~= "" then
+    		sub_page = ""
+    		page = "main"
+    		camera = {x = 60, y = 20}
+    	end
+    end
+
+    if not footer_updated then
+    	footer_constructor = {}
+    	if page == "main" and sub_page == "" then
+    		table.insert(footer_constructor, {keys = {"wasd", "lmb"}, title = "navigation", offset = 45})
+    	end
+    	if page == "shop" then
+    		table.insert(footer_constructor, {keys = {"leftarrow", "right", "lmb"}, title = "navigation", offset = 45})
+    	end
+    	if sub_page == "sandbox" then
+    		table.insert(footer_constructor, {keys = {"lmb"}, title = "navigation", offset = 45})
+    	end
+    	footer_updated = true
+    end
+end
+

```

---

# Migration Report: scripts\panels.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\panels.lua
+++ patched/scripts\panels.lua
@@ -1,3 +1,4 @@
+#version 2
 function interact_init()
     findPanels = FindBodies("panel")
     openableFound = FindBodies("openable")
@@ -121,7 +122,7 @@
         local group = openableGroupArray[i]
         local panels = group.openables
 
-        if InputPressed("interact") and GetPlayerInteractShape() == group.trigger then
+        if InputPressed("interact") and GetPlayerInteractShape(playerId) == group.trigger then
             group.active = not group.active
         end
 
@@ -165,7 +166,7 @@
 
         for k=1, #shapes do
             local s = shapes[k]
-            if InputPressed("interact") and GetPlayerInteractShape() == s then
+            if InputPressed("interact") and GetPlayerInteractShape(playerId) == s then
                 panel.active = not panel.active
             end
         end
@@ -191,7 +192,7 @@
 end
 
 function panelsFUNC()
-    if InputPressed("interact") and GetPlayerInteractShape() == inspectShape then
+    if InputPressed("interact") and GetPlayerInteractShape(playerId) == inspectShape then
         inspect = not inspect
         for i=1, #nonOpenableArray do
             local panel = nonOpenableArray[i]
@@ -292,4 +293,5 @@
             end
         end
     end
-end+end
+

```

---

# Migration Report: scripts\particles.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\particles.lua
+++ patched/scripts\particles.lua
@@ -1,15 +1,5 @@
+#version 2
 local exhaust_duration = 0.15
-
-function init()
-    particle = FindLocation("particle_test", true)
-    trans = GetLocationTransform(particle)
-end
-
-function tick()
-    if InputDown("o") then
-        bomb_water_hit_particle(trans)
-    end
-end
 
 function bomb_water_hit_particle(trans)
     local angle = 20
@@ -56,7 +46,7 @@
         SetLightIntensity(exhaust, engine.working)      
         ParticleReset()
 
-        if engine.working > 0 then
+        if engine.working ~= 0 then
             ParticleTile(1)
             ParticleRadius(param.exhaust.init, 0 + math.random(1) * 0.5)
             ParticleColor(1, 1, 1)
@@ -120,4 +110,17 @@
     ParticleCollide(0)
     
     SpawnParticle(trans.pos, VecScale(TransformToParentVec(trans, Vec(0, 0, 1)),  (param.exhaust.force * engine.working)), exhaust_duration)
-end+end
+
+function server.init()
+    particle = FindLocation("particle_test", true)
+    trans = GetLocationTransform(particle)
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputDown("o") then
+        bomb_water_hit_particle(trans)
+    end
+end
+

```

---

# Migration Report: scripts\plane.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\plane.lua
+++ patched/scripts\plane.lua
@@ -1,3 +1,4 @@
+#version 2
 function plane_flight_init()
     local wings = FindShapes("surface")
     local wingOrder = {"left", "right", "vertical", "horizontal"}
@@ -333,7 +334,7 @@
             end
         end
         if InputDown(throttledown_key) then
-            if accelerationDelta > 0 then
+            if accelerationDelta ~= 0 then
                 accelerationDelta = accelerationDelta - (delta / 8) * vtolTransitionPlane
             else
                 accelerationDelta = 0
@@ -347,7 +348,7 @@
             aircraft.velocity = VecAdd(aircraft.velocity, TransformToParentVec(GetBodyTransform(prop.body), Vec(0, param.vtol_acceleration * prop.engine.working * accelerationDelta, 0)))
         end
     else
-        if #propeller_list > 0 then
+        if #propeller_list ~= 0 then
             for i=1, #propeller_list do
                 local prop = propeller_list[i]
 
@@ -402,7 +403,8 @@
     wing_tick()
     wind_tip_effect()
 
-    if #exhaust_nozzle > 0 then
+    if #exhaust_nozzle ~= 0 then
         nozzle_vectoring()
     end 
-end+end
+

```

---

# Migration Report: scripts\ramp.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ramp.lua
+++ patched/scripts\ramp.lua
@@ -1,3 +1,4 @@
+#version 2
 function ramp_init()
     ramps = FindJoints("ramp")
     ramp_list = {}
@@ -70,7 +71,7 @@
         local trigger = ramp.trigger
         local joints = ramp.joints
 
-        if (InputPressed("interact") and GetPlayerInteractShape() == trigger) or (aircraft.startup and aircraft.inside and InputPressed(ramp_key)) then
+        if (InputPressed("interact") and GetPlayerInteractShape(playerId) == trigger) or (aircraft.startup and aircraft.inside and InputPressed(ramp_key)) then
             ramp.active = not ramp.active
         end
         
@@ -140,3 +141,4 @@
         end
     end
 end
+

```

---

# Migration Report: scripts\spawn.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\spawn.lua
+++ patched/scripts\spawn.lua
@@ -1,14 +1,4 @@
-#include "vehicle.lua"
-#include "utility.lua"
-
-spawned = false
-
-function init()
-    vehicle = FindVehicle()
-    wheel_shapes = FindShapes("wheel")
-    SetTag(vehicle, "spawning")
-end
-
+#version 2
 function ground_detect()
     local count = 0
     for i=1, #wheel_shapes do
@@ -28,7 +18,14 @@
     return count > 0
 end
 
-function tick()
+function server.init()
+    vehicle = FindVehicle()
+    wheel_shapes = FindShapes("wheel")
+    SetTag(vehicle, "spawning")
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
     if not spawned then
         if InputPressed("lmb") then
             if ground_detect() then
@@ -36,10 +33,11 @@
             else
                 SetTag(vehicle, "spawn", "air")
             end
-            
+
             SetTag(vehicle, "weapon")
             RemoveTag(vehicle, "spawning")
             spawned = true
         end
     end
-end+end
+

```

---

# Migration Report: scripts\surfaces.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\surfaces.lua
+++ patched/scripts\surfaces.lua
@@ -1,3 +1,4 @@
+#version 2
 function surfaces_init()
     surface_joint_handles = FindJoints("surface")
     surfaceArray = {}
@@ -284,4 +285,5 @@
     elevatorData.health = (elevatorHealth / elevatorData.count)
     spoilerData.health = (spoilerHealth / spoilerData.count)
     flapData.health = (flapHealth / flapData.count)
-end+end
+

```

---

# Migration Report: scripts\ui.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\ui.lua
+++ patched/scripts\ui.lua
@@ -1,15 +1,10 @@
-#include "menu.lua"
-
+#version 2
 local compass_right = {"N", "NE", "E", "SE", "S", "SO"}
 local compass_left = {"N", "NO", "O", "SO", "S", "SE"}
 local instrument_lerp = 0
 local lerp_finish = 0
 local blink_t = 0
 
-emergency_states = {}
-
-metric = GetString("savegame.mod.ava.keys.ui_flight_unit") == "metric"
-
 function create_controls_ui_list()
 	list = {}
 
@@ -52,7 +47,7 @@
 		table.insert(list, {string.upper(hover_key), "Hover Mode"})
 	end
 	if hasWeapons then
-		if #weapons_order > 0 then
+		if #weapons_order ~= 0 then
 			table.insert(list, {string.upper(switch_weapon_key), "Switch Weapon"})
 		end
 		table.insert(list, {string.upper(fire_key), "Fire Weapon"})
@@ -311,7 +306,7 @@
 		emergency_handler()
 
 	UiPop()
-end		
+end
 
 function emergency_handler()
 	local w = 150
@@ -385,7 +380,7 @@
 		end	
 	UiPop()
 
-	-- if #emergency_states > 0 then
+	-- if #emergency_states ~= 0 then
 	-- 	PlayLoop(emergency_loop, aircraft.transform.pos, 3 * lerp_finish)
 	-- end
 
@@ -473,7 +468,6 @@
     end
     table.insert(info_list, {title = "Engines", info = info_engines, colour = {1, 0, 0}, main = string.format("hp: %0.2f, wk : %0.2f", aircraft.engines.health, aircraft.engines.working), highlight = engine_shapes})
 
-
     -- fuel
     local info_fuel = {}
     local fuel_shapes = {}
@@ -511,7 +505,7 @@
     end
   
     -- propellers 
-    if #propeller_list > 0 then
+    if #propeller_list ~= 0 then
         local info_prop = {}
         local prop_shapes = {}
 
@@ -637,4 +631,5 @@
     
     DebugLine(aircraft.transform.pos, VecAdd(aircraft.transform.pos, VecScale(local_front_dir, 10)), 1, 0, 0)
     DebugLine(aircraft.transform.pos, VecAdd(aircraft.transform.pos, VecScale(global_front_dir, 10)), 0, 0, 1)
-end +end
+

```

---

# Migration Report: scripts\utility.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\utility.lua
+++ patched/scripts\utility.lua
@@ -1,3 +1,4 @@
+#version 2
 function inList(list, element)
     local found = false
     for i=1, #list do
@@ -84,9 +85,10 @@
         local c = list[i]
         str = str .. c .. "#"
     end
-    SetString(string.format("savegame.mod.ava.loadout.%s", aircraft), str)
+    SetString(string.format("savegame.mod.ava.loadout.%s", aircraft), str, true)
 end
 
 function vec_distance(vec1, vec2)
     return VecLength(VecSub(vec1, vec2))
-end+end
+

```

---

# Migration Report: scripts\vehicle.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\vehicle.lua
+++ patched/scripts\vehicle.lua
@@ -1,7 +1,4 @@
-
-
-
-
+#version 2
 local function fuel_function_init()
     local fuel_handles = FindShapes("fuel")
     for i=1, #fuel_handles do
@@ -181,7 +178,7 @@
 
         if aircraft.inside and not crash_set then
             local g = GetInt("savegame.mod.ava.stats.crashed") 
-            SetInt("savegame.mod.ava.stats.crashed", g + 1)
+            SetInt("savegame.mod.ava.stats.crashed", g + 1, true)
             crash_set = true
         end
     end
@@ -251,7 +248,7 @@
                     engine.engineStartupDelta = param.startup_time
                 end
             else
-                if engine.engineStartupDelta > 0 then
+                if engine.engineStartupDelta ~= 0 then
                     engine.engineStartupDelta = engine.engineStartupDelta - delta / (param.stop_time / param.startup_time) * aircraft.fuel
                 else
                     engine.engineStartupDelta = 0
@@ -259,7 +256,6 @@
             end
             
             engine.working = (engine.engineStartupDelta / param.startup_time)
-
 
             local sum = 0
             for k=1, #shapes do
@@ -267,7 +263,6 @@
                 sum = sum + GetShapeVoxelCount(sh)
             end
             engine.health = sum / engine.count
-
 
             if engine.link ~= nil then
                 for k=1, #wing_list do
@@ -301,7 +296,7 @@
         for k=1, #exhausts do
             local exhaust = exhausts[k]
 
-            if engine.working > 0 then
+            if engine.working ~= 0 then
                 local trans = GetLightTransform(exhaust)
                 local colour = 0.5
                 local duration = 0.15
@@ -350,7 +345,7 @@
             end
 
             if tank.health < 1 then
-                if tank.amount > 0 then
+                if tank.amount ~= 0 then
                     tank.amount = tank.amount - delta * leak_rate * (1 - tank.health)
                 else
                     tank.amount = 0
@@ -472,7 +467,7 @@
     local sum = 0
     local healthSum = 0
     
-    if GetPlayerVehicle() == aircraft.vehicle then
+    if GetPlayerVehicle(playerId) == aircraft.vehicle then
         aircraft.inside = true
 
         if (InputPressed(start_key)) then
@@ -489,7 +484,7 @@
             weaponIndex = 0
         end
 
-        SetBool("game.vehicle.interactive", false)
+        SetBool("game.vehicle.interactive", false, true)
     else
         if not auto_pilot_mode then
             aircraft.startup = false
@@ -532,12 +527,12 @@
 
     if not aircraft.crashed then 
         if not (seat == 0) then
-            if not (GetPlayerVehicle() == aircraft.vehicle) then
+            if not (GetPlayerVehicle(playerId) == aircraft.vehicle) then
                 SetTag(aircraft.vehicle, "nodrive") 
             end
-            if InputPressed("interact") and GetPlayerInteractShape() == seat then
+            if InputPressed("interact") and GetPlayerInteractShape(playerId) == seat then
                 RemoveTag(aircraft.vehicle, "nodrive") 
-                SetPlayerVehicle(aircraft.vehicle)
+                SetPlayerVehicle(playerId, aircraft.vehicle)
             end
         end
     else
@@ -558,9 +553,9 @@
         else
             if HasKey(string.format("savegame.mod.ava.stats.flight_time.%s", folder)) then
                 local g = GetFloat(string.format("savegame.mod.ava.stats.flight_time.%s", folder)) 
-                SetFloat(string.format("savegame.mod.ava.stats.flight_time.%s", folder), g + flight_time) 
+                SetFloat(string.format("savegame.mod.ava.stats.flight_time.%s", folder), g + flight_time, true) 
             else
-                SetFloat(string.format("savegame.mod.ava.stats.flight_time.%s", folder), flight_time) 
+                SetFloat(string.format("savegame.mod.ava.stats.flight_time.%s", folder), flight_time, true) 
             end
             save_time = 0
             flight_time = 0
@@ -719,7 +714,7 @@
     end
 
     if debug_mode then
-        SetPlayerVehicle(aircraft.vehicle)
+        SetPlayerVehicle(playerId, aircraft.vehicle)
     end 
 
     update_variables()
@@ -813,4 +808,5 @@
     for i=1, #wheel_shapes do
         SetShapeCollisionFilter(wheel_shapes[i], 4, 4)
     end
-end+end
+

```

---

# Migration Report: scripts\vtol.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\vtol.lua
+++ patched/scripts\vtol.lua
@@ -1,16 +1,9 @@
-vtolMode = false
-vtolMoving = false
-vtol_request = false
-vtol_move_reverse = false
-
+#version 2
 local vtolSequence = {}
 local vtolSequenceInvert = {}
 local vtolPanelArray = {}
 local vtolSequenceGroups = {}
-
 local sequenceIndex = 1
-vtolFinished = false
-vtolDone = 0
 local vtolMaxFinished = 0
 
 function vtol_init()
@@ -87,7 +80,7 @@
         local group = vtolSequenceGroups[i]
         vtolMaxFinished = vtolMaxFinished + group.max_joint
     end 
-end 
+end
 
 function vtol_particles()
     if vtolDone > 0.7 then
@@ -237,4 +230,5 @@
             vtolMoving = false
         end
     end
-end+end
+

```

---

# Migration Report: scripts\weapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\weapons.lua
+++ patched/scripts\weapons.lua
@@ -1,39 +1,6 @@
-switch_sound = LoadSound("MOD/sounds/click.ogg")
+#version 2
 local launch_sound = LoadSound('MOD/sounds/projectile/launcher0.ogg')
-
-pylons_list = {}
-turret_list = {}
-cannon_list = {}
-
-projectile_doors = {}
-bullet_casing_list = {}
-bullet_projectile_list = {}
-
-weapons_order = {}
-weapons_data = {}
-active_projectiles = {}
-weapon_selected = ""
-weapon_type = ""
-weapon_reticle_positions = Vec(0, 0, 0)
-
-firing_modes = {"sequential", "salvo", "burst"}
-firing_mode_selected = "salvo"
-firing_mode_index = 1
-turret_mouse_control = false
-weapon_index = 1
-shoot_time = 0
-
-infinite_ammo = GetBool("savegame.mod.ava.keys.infinite_ammo")
-
 local burst = {bursting = false, time = 0, delay = 0.1, val = 1, max = 4}
-
-hasTurret = false
-hasCannon = false
-hasWeapons = false
-hasPylons = false
-
-weapons_spawned = false
-
 local lockon_cords = {0, 0}
 local lock_time = 0
 local vehicle_lockon = nil
@@ -160,7 +127,7 @@
                     end
                 end
         
-                if #trigger_handles > 0 then
+                if #trigger_handles ~= 0 then
                     for j=1, #shape_handles do
                         local shape = shape_handles[j]
                         
@@ -184,7 +151,7 @@
                             if HasTag(shape, "projectile") and IsShapeInTrigger(trigger, shape) then
                                 local lights = GetShapeLights(shape)
         
-                                if light == nil and #lights > 0 then
+                                if light == nil and #lights ~= 0 then
                                     light = lights[1]
                                 end
                                 table.insert(shapes, shape)
@@ -202,7 +169,7 @@
                         if HasTag(shape, "projectile") then
                             local lights = GetShapeLights(shape)
         
-                            if light == nil and #lights > 0 then
+                            if light == nil and #lights ~= 0 then
                                 light = lights[1]
                             end
     
@@ -274,7 +241,7 @@
         for j=1, #shapes do
             local s = shapes[j]
             local joints = GetShapeJoints(s)
-            if #joints > 0 then
+            if #joints ~= 0 then
                 table.insert(d.joints, joints[1])
             end
         end 
@@ -384,7 +351,7 @@
             end
         end
 
-        if weapon_selected == pylon.name and not pylon.destroyed and #pylon.projectiles > 0 then
+        if weapon_selected == pylon.name and not pylon.destroyed and #pylon.projectiles ~= 0 then
             if fire_wait then
                 if (firing_mode_selected == "salvo") then
                     weapon_reticle_positions = return_aim_pos(pylon)
@@ -639,7 +606,7 @@
             local joints = GetShapeJoints(s)
             local lights = GetShapeLights(s)
 
-            if #lights > 0 then
+            if #lights ~= 0 then
                 for p=1, #lights do
                     local l = lights[p] 
                     if HasTag(l, "barrel") then
@@ -656,7 +623,7 @@
                 end
             end
             
-            if #joints > 0 then
+            if #joints ~= 0 then
                 local j = GetJointShapes(joints[1])
 
                 if (j[1] == s) then
@@ -729,7 +696,7 @@
             end
 
             if InputDown(fire_key) then
-                if turret.ammo > 0 then
+                if turret.ammo ~= 0 then
                     if shoot_time < turret.delay then
                         shoot_time = shoot_time + delta
                     else
@@ -800,7 +767,7 @@
             if (tag == GetTagValue(s, "cannon")) then
                 local lights = GetShapeLights(s)
 
-                if #lights > 0 then
+                if #lights ~= 0 then
                     local l = lights[1]
 
                     if not HasTag(l, "ejection") then
@@ -846,7 +813,7 @@
                 end
                 
                 if InputDown(fire_key) then
-                    if cannon.ammo > 0 then
+                    if cannon.ammo ~= 0 then
                         if shoot_time < cannon.delay then
                             shoot_time = shoot_time + delta
                         else
@@ -913,7 +880,7 @@
             table.insert(bullet_casing_list, {body = bod, time = 0})
         end
     end
-end 
+end
 
 function weapon_reticle_ui()
     local x, y, dist = UiWorldToPixel(weapon_reticle_positions)
@@ -972,7 +939,7 @@
             end
         end 
 
-        if #potential_locks > 0 then
+        if #potential_locks ~= 0 then
             vehicle_lockon = potential_locks[1]
 
             for i=1, #potential_locks do
@@ -1202,4 +1169,5 @@
         bullet_handler()
         weapon_cycle()
     end
-end+end
+

```
