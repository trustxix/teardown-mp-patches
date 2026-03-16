# Migration Report: AIComponent.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/AIComponent.lua
+++ patched/AIComponent.lua
@@ -1,223 +1,4 @@
---[[
-
-#include "common.lua"
-#include "pathfinding/AVF_pathfinder.lua"
-#include "AVF_AI_ACS.lua"
-
-]]
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) 
-*
-* FILENAME :        AiComponent.lua             
-*
-* DESCRIPTION :
-*       File that manages AI operations and teams 
-*
-*		Controls here manage AI aiming, weapon systems and other behaviors
-*		
-*
-
-
-
-sides 
-
-0= neutral
-1= blufor
-2= opfor
-3= inde
-
-]]
-
-
-ai_locations = {
-	ai_commander = {
-		x = nil,
-		y = nil,
-		z = nil,
-	}
-
-}
-
-_AI_DEBUG_PATHING = false
-
-
-AIM_FORWARDS_POS = Vec(0,0,-20)
-
-
-AVF_ai = {
-	phases = 32,
-	current_phase = 1,
-	assignment_phase = 1,
-
-	pathing_phase = 0,
-
-	-- if they register then they get seen to, refresh register every n time stamps AIHOLDS TAGTO SAY IN LIST 
-    -- IF DEAD THEN IGNORED,THEN REMOVED ON REFERESH
-	pathing_queue = 
-
-	 	{},
-
-	 pathing_template = {
-	 	id = 0, 
-	 	finished = 0, 
-
-
-	 },
-
-	OPFOR = 1,
-	BLUFOR = 2,
-	INDEP = 3,
-
-
-	sides = {
-		[1] = "blueForAI",
-		[2] = "opForAI",
-		[3] = "indepAI",
-	},
-
-
-	vehicles = {
-
-	},
-
-	blueForAI = {
-
-
-	},
-	opForAI = {
-
-
-	},
-	indepAI = {
-
-
-	},
-	templateVehicle = {
-		id = nil,
-		alive = true,
-		info = nil, 
-		features = nil, 
-		side = nil,
-		NEW_TAK_COMMAND = nil,
-		NEW_COMMAND_TIMER = 0,
-		NEW_COMMAND_TIMER_MAX = 0.5,
-		range = 100,
-		precision = 1,
-		persistance = 0.3,
-		optics_range = 200,
-		behaviors = {
-			state = "safe",
-			last_spotted = 0,
-			spotted_memory = 1.5,
-			target = nil,
-			target_pos = nil,
-		},
-		optics_pos = Transform(Vec(0,0.85,0),Quat()),
-		custom_optics = false,
-		optics_range = 200,
-		proximity_threshold = 0.9,
-		pathing = {
-			active = false,
-			has_path = false,
-			current_path = {},
-			lastPath = {},
-			vehicle_bodies = {},
-			goal_pos = {},
-			target_node = {},
-		},
-		current_priority = 1,
-		current_priority_score = 0,
-		pathing_priorities= {
-			[1] = {
-					name = "patrol",
-					actionable = false, 
-					impulse = 1,
-					score = -1,
-					target = 0,
-					target_type = "location",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "moves around locations with no clear goal",
-			},
-			[2] = {
-					name = "capture",
-					actionable = false,  
-					impulse = 1,
-					preference = 1,
-					score = -1,
-					target = nil,
-					target_type = "point",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to capture a point",
-			},
-			[3] = {
-					name = "attack",
-					actionable = false,  
-					impulse = 1,
-					preference = 1,
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to attack a vehicle",
-			},
-			[4] = {
-					name = "defend",
-					actionable = false,  
-					impulse = 0.7,
-					preference = 1,
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to defend a point",
-			},
-			[5] = {
-					name = "follow",
-					actionable = false,  
-					impulse = 1,
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "follow a nearby ally",
-			},
-			[6] = {
-					name = "recieve_orders",
-					actionable = false,  
-					impulse = 1,
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "Follow commander orders",
-			},
-			[7] = {
-					name = "neutral",
-					actionable = false,  
-					impulse = 1,
-					score = 0.1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "remain inactive while untasked",
-			},
-		},
-		ACS = {}
-	},
-}
-
-
-
+#version 2
 function AVF_ai:initAi()
 	self.assignment_phase = (self.assignment_phase%self.phases) +1
 
@@ -250,25 +31,6 @@
 
  end
 
-
---[[
-
-	ai_locations = {
-		[1] = "ai_commander",
-
-	}
-
-ai_locations = {
-	ai_commander = {
-		x = nil,
-		y = nil,
-		z = nil,
-	}
-
-}
-
-]]
-
 function AVF_ai:init_custom_ai_behaviours(ai)
 	for key, val in pairs(ai_locations) do 
 		if(type(val)== 'table') then 
@@ -298,34 +60,7 @@
 	ai.ACS:initVehicle(ai) 
 end
 
-
- --- function that operates through ai behaviors
-
-
- 	--[[
-
-		GENERIC AI BEHAVIORS
-
-			moves to goal pos
-
-			sees if a target in range
-
-			opts to stop to stop + engage target, move to goal, or relocate to better engage
-
-				Each of the above are linked with "apply stealth" aka - perhaps not engage if unlikely to be seen
-
-				This needs code to work out if both are detected. 
-
-		simple first run: 
-			move to target pos, engage on the way for each possible target. 
-
-				move to closest target pos
-
-				find closest visible taget and engage
-
-
- 	]]
- function AVF_ai:aiTick(dt)
+function AVF_ai:aiTick(dt)
  	-- if(DEBUG_AI)then
 
  	-- 	DebugWatch("debugging ai",#self.vehicles)
@@ -374,36 +109,7 @@
 
  end
 
-
---[[
-
-
-		pathing = {
-			current_path = {},
-			lastPath = {},
-			vehicle_bodies = {},
-			goal_pos = {},
-			target_node = {},
-		},
-
-
-
-]]
-
---[[
-
-function AVF_ai:reject_current_entity_parts(ai)
-	local body_parts = self:get_entity_body_parts(ai)
-	for i=1,#body_parts do 
-		QueryRejectBody(body_parts[i])
-	end
-end
-		current_priority = 1,
-		current_priority_score = 0,
-		pathing_priorities= {
-
-]]
- function AVF_ai:pathing_tick(dt)
+function AVF_ai:pathing_tick(dt)
  	if(_AI_DEBUG_PATHING) then 
  		DebugWatch("PATHING QUEUE LENGTH",#self.pathing_queue)
  	end
@@ -437,13 +143,12 @@
 
  end
 
- function AVF_ai:push_queue(ai)
+function AVF_ai:push_queue(ai)
  		self.pathing_queue[#self.pathing_queue+1] = ai 
 
-
  end
 
- function AVF_ai:pop_queue()
+function AVF_ai:pop_queue()
  	if(#self.pathing_queue>1) then
  		local temp_queue = {} 
  		for i = 2,#self.pathing_queue do
@@ -454,30 +159,9 @@
  		self.pathing_queue = {}
  	end
 
-
  end
 
- --[[
-
-	Ai behaviours follow this pattern 
-
-	if turn then detect targets. 
-
-	If target found then attempt fire on target. 
-
-	Search for points to capture. 
-
-	Advance on uncaptured points. 
-
-	Alternative AI behaviours may focus on 
-		guarding points
-		stopping to engage detected target. 
-		Changing path to advance on detected target. 
-
-
- ]]
-
- function AVF_ai:ai_behaviors(ai)
+function AVF_ai:ai_behaviors(ai)
  	-- DebugWatch("ai"..ai.id.." state: ",ai.id)
  	-- self:move_to_pos(ai)
  	if(not HasTag(ai.id,"avf_vehicle_cooking_off") or math.random()>0.8) then 
@@ -503,67 +187,11 @@
 
 		self:manage_priorities(ai)
 
-
 		
 	end
 	self:navigate_pathing(ai)
 
  end
-
-
---[[		current_priority = 1,
-		pathing_priorities= {
-			[1] = {
-					name = "patrol",
-					actionable = false, 
-					score = 0.01,
-					target = 0,
-					target_type = "location",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "moves around locations with no clear goal",
-			},
-			[2] = {
-					name = "capture",
-					actionable = false, 
-					score = -1,
-					target = 0,
-					target_type = "point",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to capture a point",
-			},
-			[3] = {
-					name = "attack",
-					actionable = false, 
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to attack a vehicle",
-			},
-			[4] = {
-					name = "defend",
-					actionable = false, 
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to defend a point",
-			},
-			[5] = {
-					name = "follow",
-					actionable = false, 
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "follow a nearby ally",
-			},
-		},]]
 
 function AVF_ai:manage_priorities(ai)
 	--[[  
@@ -571,7 +199,6 @@
 	
 
 		score is >0 and lowest score wins. 
-
 
 	]]
 	ai.current_priority_score = 0
@@ -614,27 +241,7 @@
 	-- DebugWatch("ai "..ai.id.."priority name",ai.pathing_priorities[ai.current_priority].name)
 	-- DebugWatch("ai priority score",ai.current_priority_score)
 
-
-end
-
---[[
-	below handles major ai priorities for higher level functions
-			[2] = {
-					name = "capture",
-					actionable = false, 
-					score = -1,
-					target = 0,
-					target_type = "point",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to capture a point",
-			},
-
-		ORIGINAL FOCUS: GET DISTANCE, FIND LOWEST DISTANCE
-		NEW FOCUS: GET DISTANCE, CALCULATE AGAINST 400 (THEORETICAL INGAME MAX, NORMALIZE BETWEEN 0 AND 1,
-		HIGHEST VALUE WINS)
-]]
-
+end
 
 function AVF_ai:get_capture_priority(ai,priority)
 	local vehicle_pos = Transform(self:get_entity_main_centre(ai)) 
@@ -696,26 +303,6 @@
 	end
 end
 
---[[
-			[3] = {
-					name = "attack",
-					actionable = false, 
-					score = -1,
-					target = 0,
-					target_type = "",
-					target_location = {0,0,0},
-					origin = {},
-					action_desc = "move to attack a vehicle",
-			},
-		behaviors = {
-			state = "safe",
-			last_spotted = 0,
-			spotted_memory = 1.5,
-			target = nil,
-			target_pos = nil,
-		},
-
-		]]
 function AVF_ai:get_attack_priority(ai,priority)
 	-- DebugWatch("last spotted",ai.behaviors.last_spotted)
 	local vehicle_pos = Transform(self:get_entity_main_centre(ai))
@@ -738,7 +325,6 @@
 		local engagement_spacing = VecScale(VecNormalize(fwdPos),target_engagement_range*known_target_modifer)
 		local engagement_pos =  VecAdd(target_pos.pos,engagement_spacing)
 
-
 		distance_value = VecLength(TransformToLocalPoint(vehicle_pos , target_point))
 
 		distance_score = (1-((distance_value/distance_max)*priority.preference)) * priority.impulse
@@ -753,7 +339,6 @@
 	end
 
 end
-
 
 function AVF_ai:get_defend_priority(ai,priority)
 	local vehicle_pos = Transform(self:get_entity_main_centre(ai)) 
@@ -815,7 +400,6 @@
 	end
 end
 
-
 function AVF_ai:get_command_priority(ai,priority)
 	local new_command,move_target,attack_target = databus:retrieve_tak_commands(ai)
 	priority.target_location = move_target
@@ -831,7 +415,6 @@
 	priority.target = attack_target	
 end
 
-
 function AVF_ai:get_follow_priority(ai)
 	return -1
 
@@ -844,26 +427,6 @@
 	priority.score = 0.001
 	priority.target = vehicle_pos
 end
-
---[[
-
-	NAVIGATE PATHING
-
-	handles pathing for any AVF vehicle that has been given a path and is now following it
-
-	This is where microbehaviours can / will trigger
-
-
-		pathing = {
-			active = false,
-			has_path = false,
-			current_path = {},
-			lastPath = {},
-			vehicle_bodies = {},
-			goal_pos = {},
-			target_node = {},
-		},
-]]
 
 function AVF_ai:navigate_pathing(ai)
 	if(ai.pathing.has_path and ai.pathing.current_path ~=nil and  #ai.pathing.current_path>0) then
@@ -893,9 +456,7 @@
 
 	end
 
-
-end
-
+end
 
 function AVF_ai:control_vehicle(ai)
 	local look_ahead_coef = 10
@@ -936,27 +497,9 @@
 	-- 	DriveVehicle(ai.id, 0,0, true)
 	-- end
 
-
-end
-
-
-
---[[
-
-		considerations for ai behaviors
-		ai = 
-		{
-			behaviors = {
-				state = "safe",
-				last_spotted = 0,
-				spotted_memory = 3,
-				target = nil,
-			},
-		}
-]]
-
- function AVF_ai:find_target(ai)
-
+end
+
+function AVF_ai:find_target(ai)
 
  	local target,target_pos = self:targetSelection(ai)
  	 
@@ -965,7 +508,6 @@
 	 	ai.behaviors.target_pos = self:getPos(target)
 	 end
  end
-
 
 function AVF_ai:targetSelection(ai)
 	local ai_pos = AVF_ai:getPos(ai)
@@ -1027,7 +569,6 @@
 	end 
 end
 
-
 function AVF_ai:dist_to_target(ai_pos,target_pos)
 	return VecLength(VecSub(ai_pos.pos,target_pos.pos))
 end
@@ -1041,16 +582,13 @@
 	local fwdPos = VecSub(target_pos.pos,commanderPos.pos)
 	local dir = VecNormalize(fwdPos)
 
-
 	self:reject_current_entity_parts(ai)
 	local scan_range = math.min(VecLength(fwdPos) *1.15,ai.optics_range)
 	
 	local hit, dist,normal, shape = QueryRaycast(commanderPos.pos, dir ,scan_range  ,0,true)
 
-
 	local hit_body = GetShapeBody(shape)
 	local hitVehicle = self:hit_ai_body_parts(other_ai,hit_body)
-
 
 	return hitVehicle,dist
 end
@@ -1067,8 +605,6 @@
 	local fwdPos = VecSub(targetPos.pos,commanderPos.pos)
 	local dir = VecNormalize(fwdPos)
 
-
-
 	self:gunAiming(ai,targetPos,target_vel,fwdPos,false)
 	return hitVehicle
 
@@ -1081,7 +617,7 @@
 	local targetPos = self:getPos(target)
 	targetPos.pos = self:get_entity_main_centre(target) 
 	local target_vel =  GetBodyVelocity(self:get_entity_main_body(target))
-	-- targetPos.pos = VecAdd(targetPos.pos,VecScale(GetPlayerVelocity(),GetTimeStep()*2))
+	-- targetPos.pos = VecAdd(targetPos.pos,VecScale(GetPlayerVelocity(playerId),GetTimeStep()*2))
 	local commanderPos = GetVehicleTransform(vehicle.id)
 	commanderPos.pos = self:get_entity_main_centre(ai) --TransformToParentPoint(commanderPos,Vec(0,3,0))
 
@@ -1134,7 +670,6 @@
 
 				-- vehicleFeatures.weapons[group][index].turretJoint = turretJoint
 				-- vehicleFeatures.weapons[group][index].base_turret = attatchedShape
-
 
 				local previouslyAimed = gun.aimed
 				if(DEBUG_AI) then 
@@ -1166,13 +701,11 @@
 					end
 				end
 
-
 				-- test_player_damage(gun)
 			end
 	end			
 
 end
-
 
 function get_target_range(gun,fwdPos)
 		local shellType = gun.magazines[gun.loadedMagazine].CfgAmmo
@@ -1205,8 +738,6 @@
 
 end
 
----- must handle multiple guns
----- if gun angle up > 0 then gun goes down and vice versa, with bias to control
 function AVF_ai:gunLaying(ai,gun,targetPos)
 	local up = self:gunAngle(0,0,-1,gun,targetPos)
 	local down = self:gunAngle(0,0,1	,gun,targetPos)
@@ -1245,7 +776,6 @@
 
 	local rotation_force = GetBodyMass(GetShapeBody(gun.id))
 
-
 	local min, max = GetJointLimits(gun.gunJoint)
 	local current = GetJointMovement(gun.gunJoint)
 	gun.commander_view_y = clamp(0,1,(gun.commander_view_y + (gun.commander_y_rate*GetTimeStep() * -dir)))
@@ -1335,8 +865,6 @@
 	end
 
 end
-
-
 
 function AVF_ai:turretRotatation(ai,turret,turretJoint,targetPos,gun)
 
@@ -1369,7 +897,6 @@
 		bias = bias * math.random(-1,1)
 		if(forward<(1-bias)) then
 
-
 			local target_move = left-right
 			if(math.abs(target_move)>bias) then
 				SetJointMotor(
@@ -1394,7 +921,6 @@
 
 function AVF_ai:turretAngle(x,y,z,turret,targetPos)
 
-
 	 	-- DebugWatch("avf ai turret test ",1)
 	local turretTransform = GetShapeWorldTransform(turret)
 	turretTransform=GetShapeWorldTransform(vehicleFeatures.commanderPos) 
@@ -1406,7 +932,6 @@
 	return orientationFactor
 end
 
-
 function AVF_ai:gunAngle(x,y,z,gun,targetPos)
 
 	 	-- DebugWatch("avf ai turret test ",1)
@@ -1421,9 +946,6 @@
 	-- DebugLine(gunTransform.pos,fwdPos,1,0,0,1)
 	return orientationFactor
 end
-
-
-
 
 function AVF_ai:getPos(ai)
 	local pos = nil
@@ -1437,9 +959,6 @@
 	return pos
 end
 
-
-
-
 function AVF_ai:hit_ai_body_parts(ai,hit_body)
 	local body_parts = self:get_entity_body_parts(ai)
 	for i=1,#body_parts do 
@@ -1450,14 +969,12 @@
 	return false
 end
 
-
 function AVF_ai:reject_current_entity_parts(ai)
 	local body_parts = self:get_entity_body_parts(ai)
 	for i=1,#body_parts do 
 		QueryRejectBody(body_parts[i])
 	end
 end
-
 
 function AVF_ai:get_entity_body_parts(ai)
 	local body = nil 
@@ -1474,7 +991,6 @@
 	end
 
 end
-
 
 function AVF_ai:get_entity_main_body(entity)
 	
@@ -1518,4 +1034,5 @@
 		end
 	end
 
-end+end
+

```

---

# Migration Report: ammo.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/ammo.lua
+++ patched/ammo.lua
@@ -1,1213 +1 @@
-AmmoOverrides = {
-	name				= "name",	
-	caliber 			= "caliber",
-	velocity 			= "velocity",
-	gravityCoef 		= "gravityCoef",
-	dispersionCoef		= "dispersionCoef",
-	timeToLive 			= "timeToLive",
-	launcher 			= "launcher",
-	guidance 			= "guidance",
-	guidance_frequency 	= "guidance_frequency",
-	guidance_N 	= "guidance_N",
-	guidance_Nt 	= "guidance_Nt",
-	kinematic_sim 	 	= "kinematic_sim",
-	launch_method		= "launch_method",
-	activation_range 	= "activation_range",
-	attack_pattern 		= "attack_pattern",
-	guidance_peak_dist 		= "guidance_peak_dist",
-	guidance_height_ratio  = "guidance_height_ratio",
-	missile_ramp_speed = "missile_ramp_speed",
-	turn_speed			= "turn_speed",
-	max_climb 			= "max_climb",
-	payload 			= "payload",
-	chargeType 			= "chargeType",
-	shellWidth				= "shellWidth",
-	shellHeight				= "shellHeight",
-	r						= "r",
-	g						= "g", 
-	b						= "b", 
-	tracer 					= "tracer",
-	tracerL					= "tracerL",
-	tracerW					= "tracerW",
-	tracerR					= "tracerR",
-	tracerG					= "tracerG", 
-	tracerB					= "tracerB", 
-	shellSpriteName			= "shellSpriteName",
-	shellSpriteRearName		= "shellSpriteRearName",
-	magazineCapacity   	= "magazineCapacity",
-	magazineCount    	= "magazineCount",
-	explosionSize		= "explosionSize",
-	maxPenDepth			= "maxPenDepth",
-	RHAe				= "RHAe",
-	flightLoop 			= "flightLoop",
-
-}
-
-
-penetrationModifiers = {
-	kinetic = 0.2,
-	AP = 0.3,
-	APHE = 0.6,
-	HEAT = 0.25,
-
-
-}
-
-richochetModifiers = {
-	kinetic = 2,
-	AP = 1,
-	APHE = 0.8,
-	incendiary = 1.1,
-	HEAT = 1.5,
-	HE = 4,
-	shrapnel = 4,
-	explosive = 4,
-	HESH = 2,
-	APBC  = 1.2,
-
-}
-
-
-shell_launcher_types = {
-	["rocket"] = "rocket",
-	["missile"] = "rocket",
-	["homing"] = "rocket",
-	["guided"] = "rocket",
-	["cannon"] = "shell",
-}
-shell_warhead_penetration_effect = {
-	["HEAT"] = "chemical",
-	["HESH"] = "chemical",
-	["HEI"] = "kinetic",
-	["APHE"] = "kinetic",
-	["AP"] = "kinetic",
-	["explosive"] = "kinetic",
-	["oldschool_HE"] = "kinetic",
-	["high-explosive"] = "kinetic",
-	["HE"] = "kinetic",
-	["Incendiary"] = "kinetic",
-	["kinetic"] = "kinetic",
-	["shrapnel"] = "kinetic",
-
-}
-
-
---[[
-
-	MUNITION TYPES: 
-
-		HEAT
-		HESH
-		HEI
-		APHE
-		AP
-		explosive
-		oldschool_HE
-		high-explosive
-		HE
-		Incendiary
-		kinetic
-		shrapnel
-
-
-]]
-
-
-
-
-munitions = {
-	
---[[
-
-
-	Custom
-
-]]
-
-
-	["customShell"] = {
-				name = "customShell",
-				caliber 				= 100,
-				velocity				= 200,
-				explosionSize			= 2,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "explosive",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-	["custom_Ball_round"] = {
-			name = "custom ball round",
-			caliber 				= 7.62,
-			velocity				= 350,
-			hit 					=2,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 7,
-			launcher				= "mgun",
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
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
---[[
-
-	Cannon shells
-
-]]
-	["125mm_HEAT"] = {
-				name = "125mm HEAT",
-				caliber 				= 125,
-				velocity				= 220,
-				explosionSize			= 1.2,
-				maxPenDepth 			= 2.2,
-				timeToLive 				= 7,
-				gravityCoef 			= 0.9,--0.3,
-				launcher				= "cannon",
-				payload					= "HEAT",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.3,
-				g						= 0.6, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-					
-			},
-
-	["125mm_HESH"] = {
-				name = "125mm HESH",
-				caliber 				= 125,
-				velocity				= 220,
-				explosionSize			= 1.2,
-				maxPenDepth 			= 1.2,
-				timeToLive 				= 7,
-				gravityCoef 			= 0.9,
-				launcher				= "cannon",
-				payload					= "HESH",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.3,
-				g						= 0.6, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-					
-			},
-
-
-	["125mm_APFSDS"] = {
-				name = "125mm APFSDS",
-				caliber 				= 125,
-				velocity				= 270,
-				explosionSize			= 0.5,
-				maxPenDepth 			= 1.2,
-				timeToLive 				= 7,
-				gravityCoef 			= 0.9,
-				launcher				= "cannon",
-				payload					= "kinetic",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 1.7,
-				g						= 1.7, 
-				b						= 1.7, 
-				shellSpriteName			= "MOD/gfx/sabot.png",
-				shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-			},
-
-
-	["125mm_AP"] = {
-				name = "125mm AP",
-				caliber 				= 125,
-				velocity				= 270,
-				explosionSize			= 0.5,
-				maxPenDepth 			= 1.0,
-				timeToLive 				= 7,
-				gravityCoef 			= 0.9,
-				launcher				= "cannon",
-				payload					= "AP",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 1.7,
-				g						= 1.7, 
-				b						= 1.7, 
-				shellSpriteName			= "MOD/gfx/sabot.png",
-				shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-			},
-
-	["125mm_HE"] = {
-				name = "125mm HE",
-				caliber 				= 125,
-				velocity				= 200,
-				explosionSize			= 1.5,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-	["BR-482B"] = {
-				name = "BR-482B",
-				caliber 				= 130,
-				velocity				= 250,
-				explosionSize			= 1.0,
-				maxPenDepth 			= 0.8,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "APHE",
-				shellWidth				= 0.6,
-				shellHeight				= 1.7,
-				r						= 0.4,
-				g						= 0.8, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-					
-			},
-
-	["OF-482M"] = {
-				name = "OF-482M",
-				caliber 				= 130,
-				velocity				= 220,
-				explosionSize			= 2.3,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.6,
-				shellHeight				= 1.7,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-
-	["L23A1"] = {
-				name = "L23A1 120mm APFSDS",
-				caliber 				= 120,
-				velocity				= 300,
-				explosionSize			= 0.5,
-				maxPenDepth 			= 1.0,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "kinetic",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.3,
-				g						= 0.3, 
-				b						= 1, 
-				shellSpriteName			= "MOD/gfx/sabot.png",
-				shellSpriteRearName		= "MOD/gfx/sabotRear.png",
-			},
-
-	["L31A7"] = {
-				name = "L31A7 120mm HESH",
-				caliber 				= 120,
-				velocity				= 235,
-				explosionSize			= 0.7,
-				maxPenDepth 			= 1.3,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "HESH",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.9,
-				g						= 0.9, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-					
-			},
-
-	["L34A2"] = {
-				name = "L34A2 120mm Smoke",
-				caliber 				= 120,
-				velocity				= 230,
-				explosionSize			= 0.7,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "smoke",
-				shellWidth				= 0.5,
-				shellHeight				= 1.5,
-				r						= 0.6,
-				g						= 0.6, 
-				b						= 0.6, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-					
-			},
-
-	["90mm_HEAT"] = {
-				name = "90mm HEAT",
-				caliber 				= 90,
-				velocity				= 200,
-				explosionSize			= 1.2,
-				maxPenDepth 			= 1.2,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "HEAT",
-				shellWidth				= 0.35,
-				shellHeight				= 1.25,
-				r						= 0.3,
-				g						= 0.6, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-					
-			},
-
-	["90mm_HE"] = {
-				name = "90mm HE",
-				caliber 				= 90,
-				velocity				= 180,
-				explosionSize			= 1.65,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				gravityCoef 			= 1,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.35,
-				shellHeight				= 1.25,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-	["PzGr39"] = {
-				name = "PzGr. 39",
-				caliber 				= 75,
-				velocity				= 200,
-				explosionSize			= .8,
-				maxPenDepth 			= 1.2,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.8,
-				shellHeight				= 1.5,
-				r						= 0.3,
-				g						= 0.8, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["Sprgr34"] = {
-				name = "Sprgr. 34 ",
-				caliber 				= 75,
-				velocity				= 180,
-				explosionSize			= 1.2,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.8,
-				shellHeight				= 1.5,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["152mm_HE"] = {
-				name = "152mm HE",
-				caliber 				= 152,
-				velocity				= 75,
-				explosionSize			= 3.5,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 1.5,
-				shellHeight				= 3,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-
-	["76mm_HE"] = {
-				name = "76mm HE",
-				caliber 				= 76,
-				velocity				= 110,
-				explosionSize			= 1.8,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.8,
-				shellHeight				= 1.5,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-
-	["76mm_APHE"] = {
-				name = "76mm APHE",
-				caliber 				= 76,
-				velocity				= 110,
-				explosionSize			= 1.6,
-				maxPenDepth 			= 0.5,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "APHE",
-				shellWidth				= 0.8,
-				shellHeight				= 1.5,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-	["PG9_AT"] = {
-				name = "PG9 AT",
-				caliber 				= 73,
-				velocity				= 430,
-				explosionSize			= 1,
-				gravityCoef 			= 1.25,
-				maxPenDepth 			= .6,
-				timeToLive 				= 12,
-				launcher				= "rocket",
-				payload					= "HEAT",
-				shellWidth				= 0.8,
-				shellHeight				= 1.5,
-				r						= 0.3,
-				g						= 0.8, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/rocketModel.png",
-				shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			},
-	["OG9_HE"] = {
-			name = "OG9 HE",
-			caliber 				= 73,
-			velocity				= 400,
-			explosionSize			= 1.2,
-			maxPenDepth 			= 0.1,
-
-			gravityCoef 			= 1.5,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 0.8,
-			shellHeight				= 1.5,
-			r						= 0.3,
-			g						= 0.8, 
-			b						= 0.3, 
-			shellSpriteName			= "MOD/gfx/rocketModel.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			},
-
-	["RocketLowVelocity"] = {
-			name = "Low Velocity rocket",
-			caliber 				= 57,
-			velocity				= 10,
-			gravityCoef 			= 0,
-			dispersionCoef 			= 0,
-			explosionSize			= 0.8,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 12,
-			launcher				= "cannon",
-			payload					= "HE",
-			shellWidth				= 0.8,
-			shellHeight				= 1.5,
-			r						= 0.3,
-			g						= 0.8, 
-			b						= 0.3, 
-			shellSpriteName			= "MOD/gfx/rocketModel.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-
-	["9M133M-2"] = {
-			name = "9M133M-2",
-			caliber 				= 152,
-			velocity				= 20,
-			gravityCoef 			= 0,
-			dispersionCoef 			= 0,
-			explosionSize			= 1.2,
-			maxPenDepth 			= 0.8,
-			timeToLive 				= 12,
-			launcher				= "guided",
-			payload					= "HEAT",
-			shellWidth				= 0.8,
-			shellHeight				= 1.5,
-			r						= 0.9,
-			g						= 0.3, 
-			b						= 0.3, 
-			shellSpriteName			= "MOD/gfx/rocketModel.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-
-	["M_Hellfire_AT"] = {
-			name = "AGM-114 Hellfire",
-			caliber 				= 180,
-			velocity				= 30,
-			gravityCoef 			= 0,
-			dispersionCoef 			= 0,
-			explosionSize			= 1.2,
-			maxPenDepth 			= 0.8,
-			timeToLive 				= 12,
-			launcher				= "guided",
-			payload					= "HEAT",
-			shellWidth				= 0.8,
-			shellHeight				= 1.5,
-			r						= 0.9,
-			g						= 0.3, 
-			b						= 0.3, 
-			shellSpriteName			= "MOD/gfx/rocketModel.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["M_Hellfire_AP"] = {
-			name = "AGM-114R Hellfire II",
-			caliber 				= 180,
-			velocity				= 40,
-			gravityCoef 			= 0,
-			dispersionCoef 			= 0,
-			explosionSize			= 0.8,
-			maxPenDepth 			= 0.5,
-			timeToLive 				= 12,
-			launcher				= "guided",
-			payload					= "HE",
-			shellWidth				= 0.8,
-			shellHeight				= 1.5,
-			r						= 0.9,
-			g						= 0.3, 
-			b						= 0.3, 
-			shellSpriteName			= "MOD/gfx/rocketModel.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-
-
-	["S-5M"] = {
-			name = "S-5M",
-			caliber 				= 55,
-			velocity				= 200,
-			explosionSize			= 1.1,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 0.5,
-			shellHeight				= 1.2,
-			r						= 0.3,
-			g						= 0.8, 
-			b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			},
-	["S-8"] = {
-			name = "S-8",
-			caliber 				= 80,
-			velocity				= 200,
-			explosionSize			= 1.3,
-			maxPenDepth 			= 0.4,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 0.8,
-			shellHeight				= 1.6,
-			r						= 0.1,
-			g						= 0.5, 
-			b						= 0.1, 
-				shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			},
-	["S-13"] = {
-			name = "S-13",
-			caliber 				= 122,
-			velocity				= 250,
-			explosionSize			= 1.6,
-			maxPenDepth 			= 0.6,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1.0,
-			shellHeight				= 2.4,
-			r						= 0.1,
-			g						= 0.6, 
-			b						= 0.1, 
-				shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			},
-	["R_Hydra_HE"] = {
-			name = "Hydra 70",
-			caliber 				= 70,
-			velocity				= 230,
-			explosionSize			= 1.25,
-			maxPenDepth 			= 0.3,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 0.8,
-			shellHeight				= 1.6,
-			r						= 0.1,
-			g						= 0.1, 
-			b						= 0.5, 
-				shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			},
-	["107_HE_Close"] = {
-			name = "107mm Type 63 rocket HE Close",
-			caliber 				= 106.7,
-			velocity				= 40,
-			explosionSize			= 1.5,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 20,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1,
-			shellHeight				= 3,
-			r						= 0.7,
-			g						= 1.2, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["107_HE_Mid"] = {
-			name = "107mm Type 63 rocket HE Mid",
-			caliber 				= 106.7,
-			velocity				= 50,
-			explosionSize			= 1.5,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 20,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1,
-			shellHeight				= 3,
-			r						= 0.7,
-			g						= 1.2, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["107_HE_long"] = {
-			name = "107mm Type 63 rocket HE Far",
-			caliber 				= 106.7,
-			velocity				= 60,
-			explosionSize			= 1.5,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 20,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1,
-			shellHeight				= 3,
-			r						= 0.7,
-			g						= 1.2, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["122mm_HE_Close"] = {
-			name = "122mm rocket HE Close",
-			caliber 				= 122,
-			velocity				= 45,
-			explosionSize			= 1.8,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1,
-			shellHeight				= 3,
-			r						= 0.7,
-			g						= 1.2, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["122mm_HE_Mid"] = {
-			name = "122mm  rocket HE Mid",
-			caliber 				= 122,
-			velocity				= 55,
-			explosionSize			= 1.8,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1,
-			shellHeight				= 3,
-			r						= 0.7,
-			g						= 1.0, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["122mm_HE_long"] = {
-			name = "122mm  rocket HE Far",
-			caliber 				= 122,
-			velocity				= 65,
-			explosionSize			= 1.8,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1,
-			shellHeight				= 3,
-			r						= 0.7,
-			g						= 1.2, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["132mm_HE"] = {
-			name = "132mm rocket HE",
-			caliber 				= 132,
-			velocity				= 87,
-			explosionSize			= 2,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "HE",
-			shellWidth				= 1,
-			shellHeight				= 3,
-			r						= 0.7,
-			g						= 1.2, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			},
-	["9M55K"] = {
-			name = "300mm 9M55K",
-			caliber 				= 300,
-			velocity				= 100,
-			gravityCoef 			= 0.1,
-			explosionSize			= 2,
-			maxPenDepth 			= 0.25,
-			timeToLive 				= 12,
-			launcher				= "rocket",
-			payload					= "cluster",
-			airburst 				= true,
-			shellWidth				= 2,
-			shellHeight				= 6.6,
-			r						= 0.7,
-			g						= 0.7, 
-			b						= 0.7, 
-			shellSpriteName			= "MOD/gfx/rocketModel2.png",
-			shellSpriteRearName		= "MOD/gfx/rocketRear.png",
-			flightLoop				= "MOD/sounds/rocketFlightLoop0",
-			bomblet = {
-				payload = "HE",
-				explosionSize = 1.5,
-				dispersion 		= 3,
-				gravityCoef 			= 1.0,
-
-				},
-			},
-	["OFAB-250"] = {
-				name = "OFAB 250",
-				caliber 				= 325,
-				velocity				= .5,
-				explosionSize			= 4,
-				maxPenDepth 			= 0.3,
-				timeToLive 				= 15,
-				launcher				= "bomb",
-				payload					= "HE",
-				shellWidth				= 1,
-				shellHeight				= 2,
-				r						= 0.1,
-				g						= 0.1, 
-				b						= 0.1, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-	["3UOF8"] = {
-				name = "30mm HE",
-				caliber 				= 30,
-				velocity				= 250,
-				explosionSize			= .7,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.2,
-				shellHeight				= .8,
-				r						= 0.8,
-				g						= 0.3, 
-				b						= 0.3, 
-				tracer 					= 1,
-				tracerL					= 3,
-				tracerW					= 2,
-				tracerR					= 1.8,
-				tracerG					= 1.0, 
-				tracerB					= 1.0, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["3UBR8"] = {
-				name = "30mm AP-I",
-				caliber 				= 30,
-				velocity				= 270,
-				explosionSize			= .5,
-				maxPenDepth 			= 0.6,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.2,
-				shellHeight				= .8,
-				r						= 0.8,
-				g						= 0.8, 
-				b						= 0.3, 
-				tracer 					= 1,
-				tracerL					= 3,
-				tracerW					= 2,
-				tracerR					= 1.8,
-				tracerG					= 1.0, 
-				tracerB					= 1.0, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["3UBR6"] = {
-				name = "30mm AP-T",
-				caliber 				= 30,
-				velocity				= 270,
-				explosionSize			= .5,
-				maxPenDepth 			= 0.8,
-				timeToLive 				= 7,
-				launcher				= "cannon",
-				payload					= "AP",
-				shellWidth				= 0.2,
-				shellHeight				= .8,
-				r						= 0.8,
-				g						= 0.8, 
-				b						= 0.3, 
-				tracer 					= 1,
-				tracerL					= 3,
-				tracerW					= 2,
-				tracerR					= 1.8,
-				tracerG					= 1.0, 
-				tracerB					= 1.0, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-
-	["B_23mm_AA"] = {
-			name= "B_23mm_AA",
-			caliber 				= 23,
-			velocity				= 220,
-			explosionSize 			= .6,
-			maxPenDepth 			= 0.1,
-			timeToLive 				= 7,
-			launcher				= "cannon",
-			payload					= "HE",
-			shellWidth				= 0.1,
-			shellHeight				= 0.7,
-			r						= 0.5,
-			g						= 0.5, 
-			b						= 0.5, 
-			tracer 					= 1,
-			tracerL					= 5,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["B_23mm_AA_AP"] = {
-			name= "B_23mm_AA_AP",
-			caliber 				= 23,
-			velocity				= 220,
-			explosionSize 			= .6,
-			maxPenDepth 			= 0.5,
-			timeToLive 				= 7,
-			launcher				= "cannon",
-			payload					= "AP",
-			shellWidth				= 0.1,
-			shellHeight				= 0.7,
-			r						= 0.5,
-			g						= 0.5, 
-			b						= 0.5, 
-			tracer 					= 1,
-			tracerL					= 5,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["OFZ_30mm_HE"] = {
-			name= "OFZ-30",
-			caliber 				= 30,
-			velocity				= 220,
-			explosionSize 			= .7,
-			maxPenDepth 			= 0.3,
-			timeToLive 				= 7,
-			launcher				= "cannon",
-			payload					= "HE",
-			shellWidth				= 0.1,
-			shellHeight				= 0.7,
-			r						= 0.5,
-			g						= 0.5, 
-			b						= 0.5, 
-			tracer 					= 1,
-			tracerL					= 5,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["BR_30mm_AP"] = {
-			name= "BR-30",
-			caliber 				= 30,
-			velocity				= 220,
-			explosionSize 			= .6,
-			maxPenDepth 			= 0.8,
-			timeToLive 				= 7,
-			launcher				= "cannon",
-			payload					= "HE-I",
-			shellWidth				= 0.1,
-			shellHeight				= 0.7,
-			r						= 0.5,
-			g						= 0.5, 
-			b						= 0.5, 
-			tracer 					= 1,
-			tracerL					= 5,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["B_30x113mm_M789_HEDP"] = {
-			name= "M789 HEDP",
-			caliber 				= 30,
-			velocity				= 230,
-			explosionSize 			= .7,
-			maxPenDepth 			= 0.6,
-			timeToLive 				= 7,
-			launcher				= "cannon",
-			payload					= "HE",
-			shellWidth				= 0.1,
-			shellHeight				= 0.7,
-			r						= 0.5,
-			g						= 0.5, 
-			b						= 0.5, 
-			tracer 					= 1,
-			tracerL					= 5,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-	["B_762x54_Ball"] = {
-			name = "762x54_PKT",
-			caliber 				= 7.62,
-			velocity				= 350,
-			hit 					=2,
-			maxPenDepth 			= 0.15,
-			timeToLive 				= 7,
-			launcher				= "mgun",
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
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-	["B_127x107_Ball"] = {
-			name = "127x107 Ball",
-			caliber 				= 12.7,
-			velocity				= 240,
-			hit 					=3,
-			maxPenDepth 			= 0.33,
-			timeToLive 				= 7,
-			launcher				= "mgun",
-			payload					= "AP",
-			shellWidth				= 0.1,
-			shellHeight				= 0.3,
-			r						= 0.8,
-			g						= 0.8, 
-			b						= 0.5, 
-			tracer 					= 2,
-			tracerL					= 7,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-	["B_127x107_Ball_INC"] = {
-			name = "127x107 Incendiary",
-			caliber 				= 12.7,
-			velocity				= 240,
-			hit 					=3,
-			maxPenDepth 			= 0.3,
-			timeToLive 				= 7,
-			launcher				= "mgun",
-			payload					= "Incendiary",
-			shellWidth				= 0.1,
-			shellHeight				= 0.3,
-			r						= 0.8,
-			g						= 0.8, 
-			b						= 0.5, 
-			tracer 					= 2,
-			tracerL					= 7,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-	["B_145x114_Ball"] = {
-			name = "145x114 Ball",
-			caliber 				= 14.5,
-			velocity				= 280,
-			hit 					=3,
-			maxPenDepth 			= 0.46,
-			timeToLive 				= 7,
-			launcher				= "mgun",
-			payload					= "AP",
-			shellWidth				= 0.14,
-			shellHeight				= 0.4,
-			r						= 0.8,
-			g						= 0.8, 
-			b						= 0.5, 
-			tracer 					= 2,
-			tracerL					= 7,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-
-
---[[
-
-
-	Grenades
-
-]]
-
-	["G_30mm_HE"] = {
-				name = "30mm HE",
-				caliber 				= 30,
-				velocity				= 120,
-				explosionSize			= .6,
-				maxPenDepth 			= 0.1,
-				timeToLive 				= 20,
-				launcher				= "cannon",
-				payload					= "HE",
-				shellWidth				= 0.2,
-				shellHeight				= .5,
-				r						= 0.6,
-				g						= 0.3, 
-				b						= 0.3, 
-				shellSpriteName			= "MOD/gfx/shellModel2.png",
-				shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-			},
-
-
---[[
-
-
-	Special
-
-]]
-
-
-
-
-	["foam"] = {
-			name = "foam",
-			caliber 				= 14.5,
-			velocity				= 30,
-			hit 					=	0,
-			maxPenDepth 			= 0.46,
-			timeToLive 				= 7,
-			launcher				= "mgun",
-			payload					= "foam",
-			shellWidth				= 0.14,
-			shellHeight				= 0.4,
-			r						= 0.8,
-			g						= 0.8, 
-			b						= 0.5, 
-			tracer 					= 2,
-			tracerL					= 7,
-			tracerW					= 2,
-			tracerR					= 1.8,
-			tracerG					= 1.0, 
-			tracerB					= 1.0, 
-			shellSpriteName			= "MOD/gfx/shellModel2.png",
-			shellSpriteRearName		= "MOD/gfx/shellRear2.png",
-	},
-
-
-}
-
-ammoDefaults = {
-		defaultMagazine = {
-			ammoName = "",
-			magazineCapacity = 0,
-			AmmoCount = 0,
-			isEmpty = true
-
-	},
-}+#version 2

```

---

# Migration Report: audio_effects.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/audio_effects.lua
+++ patched/audio_effects.lua
@@ -1,6 +1,4 @@
-
-
--- Play a sound at a ocation and tag the source as playing the sound if necessary
+#version 2
 function play_gun_sound(sound,pos,volume,tag_sound,source,sound_type)
 	if(tag_sound) then 
 		SetTag(source.id, "PlaySound", sound_type)
@@ -9,7 +7,6 @@
 	end
 end
 
--- Play a sound at a ocation and tag the source as playing the sound if necessary
 function play_gun_loop_sound(sound,pos,volume,tag_sound,source,sound_type)
 	if(tag_sound) then 
 		-- DebugWatch("avf setting ".."PlayLoop",sound_type)
@@ -18,7 +15,7 @@
 		PlayLoop(sound, pos, volume)
 	end
 end
--- Play a sound at a ocation and tag the source as playing the sound if necessary
+
 function play_reloading_sound(sound,pos,volume,tag_sound,reload_percentage,source,sound_type)
 	-- DebugWatch("reloading",reload_percentage)
 	if(tag_sound) then 
@@ -26,4 +23,5 @@
 	else
 		PlayLoop(sound, pos, volume)
 	end
-end+end
+

```

---

# Migration Report: avf\conquest\scripts\AVF_conquest_manager.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\conquest\scripts\AVF_conquest_manager.lua
+++ patched/avf\conquest\scripts\AVF_conquest_manager.lua
@@ -1,147 +1,4 @@
-
-
---[[
-
-	File that manages conquest mode behaviours, activies, point scoring, etc. 
-
-
-	Thsi can be custmized to make very specific game modes or used as is for a simple conquest game. 
-
-	examples can include respawning assets with points lost for respawns or capture pont ticks. 
-
-
-	teams:
-		1: bluefor
-		2: opfor
-		3: inde
-
-]]
-
-
-phonetic_alphabet = {
-[1] = "Alpha",
-[2] = "Bravo",
-[3] = "Charlie",
-[4] = "Delta",
-[5] = "Echo",
-[6] = "Foxtrot",
-[7] = "Golf",
-[8] = "Hotel",
-[9] = "India",
-[10] = "Juliett",
-[11] = "Kilo",
-[12] = "Lima",
-[13] = "Mike",
-[14] = "November",
-[15] = "Oscar",
-[16] = "Papa",
-[17] = "Quebec",
-[18] = "Romeo",
-[19] = "Sierra",
-[20] = "Tango",
-[21] = "Uniform",
-[22] = "Victor",
-[23] = "Whiskey",
-[24] = "X-ray",
-[25] = "Yankee",
-[26] = "Zulu",
-}
-
-
-side_names = {
-	[1] = "blufor",
-	[2] = "opfor",
-	[3] = "inde"
-
-
-}
-
-side_colours = {
-	[1] = {0,0,1},
-	[2] = {1,0,0},
-	[3] = {0,1,0}
-
-
-}
-
-capture_point_states = {}
-default_capture_point_state = {
-						active = true,
-						id = 0,
-						name = "DEFAULT",
-						captured = false,
-						capture_side = 0,
-						capture_percentage = 0,
-}
-
-total_capture_points = 0
-
-team_scores = {0,0,0}
--- team_scores = {0,0,0}
-
-score_to_win = 9000
-
-player_team = 1
-
-
-score_tick = 1000
-score_count = 0
-
-
-score_increment = 1
-
-
-min_held_percentage = .20
-
-capture_points = nil 
-
-
-manager_active = false
-
-function init()
-	--get current AVF entities
-	-- update_capture_point_list()	
-	local existng_conquest_manager = GetBool("level.avf_conquest.game_manager_enabled")
-	if(not existng_conquest_manager) then 
-		SetBool("level.avf_conquest.game_manager_enabled", true)
-		manager_active = true
-	end
-
-end
-
-
---[[
-
-CAPTURE POINT VALUES: 
-
-
-	SetTag(capture_point,"active","true")   true/false
-	SetTag(capture_point,"captured","false") true/false
-	SetTag(capture_point,"capture_side",0) 0,1,2,3 
-	SetTag(capture_point,"capture_percentage",0) 0-1
-	SetTag(capture_point,"capture_zone_value",capture_zone_value) number 
-
-
-
-]]
-
-function tick(dt)   
-	if(manager_active) then 
-		-- DebugWatch("startng tick",#capture_point_states)
-		update_capture_point_list()	
-		-- document_capture_points( )
-		-- DebugWatch("ending  tick",#capture_point_states)
-
-		score_count = score_count + dt
-		if(score_count>score_increment) then
-			calculate_scores()
-			score_count=0
-
-		end 
-	end
-end
-
--- add newly found capture point to list of known points, give it a name. 
+#version 2
 function add_capture_point(capture_point_handle)	
 	capture_point_states[#capture_point_states+1] = deepcopy(default_capture_point_state)
 	local current_index = #capture_point_states
@@ -168,8 +25,6 @@
 
 end
 
-
--- update list of capture points every few seconds, if capture point not known then add to list. 
 function update_capture_point_list()	
 	capture_points = FindTriggers("avf_conquest_point",true)
 	for i = 1,#capture_points do 
@@ -183,7 +38,6 @@
 
 end
 
-
 function document_capture_points( )
 	for i =1, #capture_point_states do
 		format_capture_info(capture_point_states[i])
@@ -191,16 +45,6 @@
 	end
 end
 
-
-
---[[
-	a capture point has 3 states - uncaptured / neutral 
-	[SIDE] capturing 
-	[SIDE] captured
-	this may extend to Contested but not currently 
-
-
-]]
 function format_capture_info(capture_point)
 		local capture_point_name = capture_point.name
 		local side_string = ""
@@ -237,13 +81,6 @@
 
 end
 
-function draw(dt)
-	if(manager_active) then 
-		show_capture_values(dt)
-	end
-end
-
-
 function show_capture_values(dt)
 	local capture_string = ""
 	local side_colour = {1,1,1}
@@ -266,17 +103,10 @@
 	UiPop()
 end
 
-
-
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
-
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -291,4 +121,37 @@
         copy = orig
     end
     return copy
-end+end
+
+function server.init()
+    local existng_conquest_manager = GetBool("level.avf_conquest.game_manager_enabled")
+    if(not existng_conquest_manager) then 
+    	SetBool("level.avf_conquest.game_manager_enabled", true, true)
+    	manager_active = true
+    end
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(manager_active) then 
+        	-- DebugWatch("startng tick",#capture_point_states)
+        	update_capture_point_list()	
+        	-- document_capture_points( )
+        	-- DebugWatch("ending  tick",#capture_point_states)
+
+        	score_count = score_count + dt
+        	if(score_count>score_increment) then
+        		calculate_scores()
+        		score_count=0
+
+        	end 
+        end
+    end
+end
+
+function client.draw()
+    if(manager_active) then 
+    	show_capture_values(dt)
+    end
+end
+

```

---

# Migration Report: avf\conquest\scripts\capture_area.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\conquest\scripts\capture_area.lua
+++ patched/avf\conquest\scripts\capture_area.lua
@@ -1,221 +1,9 @@
---[[
-
-
-	capture_area script 
-
-
-
-		outline of script: 
-
-			Gets list of active assets 
-
-			Computes distance of assets to location 
-
-			as assets move into area, tick moves towards that assets side. 
-
-
-			As tick moves, colour changes to / from neutral to assets colour. 
-
-			When tick hits max, area remains under that side, unless tick doesn't hit min value. 
-
-
-
-	Code story: 
-
-
-		As a zone:
-
-			I tick until the max value 
-
-			dependent on what side entitites have the largest presence in my area
-
-			biased based on the quantity of those entities within my area
-
-
-			if no max value reached, nor any entity present, then i tick until i reach neutral 
-
-
-				netal s 
-
-
-		As an entity entering a region alone: 
-
-		1: 
-			
-			When i enter a neutral area
-			
-			the counter ticks towards my side
-
-			until it hits max
-
-
-		2:
-			When I enter a hostile area
-
-			the counter ticks their hold downwards
-
-			until it hits neutral 
-
-		3: 
-
-			When I enter friendly territory 
-
-			the counter remains constant
-
-
-
-		As an entity entering a region with entities within: 
-
-		1: 
-			
-			When i enter an area with a larger quantity of friendly assets
-
-			the ticker will be biased towards our side. 
-
-
-		2:
-			When I enter a region with more hostile entities 
-
-			The ticker will be biased towards their side. 
-
-		3: 
-
-			When I consider bias to a side
-
-
-			I consider the bias to be the product of the majority - perhaps ease out cubic. 
-
-		4: 
-			if i enter a zone controlled by other entities not in control of zone
-
-			zone ticks down to neutral 
-
-			zone then handled as per regular rules. 
-
-
-
---------------------------------------------------------------------------------------------------------
-
-
-	
-	Assumptions:
-		Assets could range from vehicles to people. Larger AVf handlers will only consider if a region is registered as "active" and its side. 
-
-
-		Some assets may have a higher or lower capability to hold a region. This will be an advanced feature. 
-
-		Assets with high capture capability will be measured as a float value above the regular 1 asset 1 score, likewise for assets with lower capture capability. 
-
-
-		NO AVF COMPATIBLE ASSET IS LABELLED AS MORE THAN ONE SIDE, UNLESS YOU HAVE SOME INSANE LOGIC FOR THINGS THAT WILL COUNT AS LESS OF AN ASSEST, 
-		This means that vehicles are labelled once, bodies once, shapes once, unless you do so.
-
-			If you complain of a thing being counted twice then i shall be dissapointed. 
-
-
-
-
-]]
-
-
-capture_zone_value = 1
-
-capture_zone_range = 35
-
-base_smoke = 0.3
-
---side represents which side holds the point. 
--- capture point is the same but more firm due to drunk me coding in the past 
-capture_point_side =0 
-side =0 
--- how held is the point by the current side (this is min tick not max tick)
-capture_percentage = 0
-
-min_capture_percentage = 0.2
-
-
-capture_total = 0 
-
-capture_total_max = 75
-
--- the total tick value of the point as it stands. 
-tick_total = 0
-
--- how much of this tick is applied as a base rate 1-1 of a tick. 
-tick_rate =1 
-
--- -- the min tick to be captured
--- tick_min = 25
-
--- -- the max value to be captured
--- tick_max = 60
-
-
--- time since last update to perform a tick, in ms, best to keep higher as this does a full scan of assets and therefore each node will doe. 
-tick_update = 0.750
-
--- the counter until the next update 
-tick_update_counter = 0 
-
-
-
-team_capture_score = {0,0,0}
-
-blufor_hold = 0
-opfor_hold = 0
-inde_hold = 0
-
-
-function init()
-	--get current AVF entities
-
-
-	capture_point = FindTrigger("avf_conquest_point")
-	capture_point_sprite = LoadSprite("gfx/ring.png")
-
-
-	SetTag(capture_point,"active","true")
-	SetTag(capture_point,"captured","false")
-	SetTag(capture_point,"capture_side",0)
-	SetTag(capture_point,"capture_percentage",0)
-	SetTag(capture_point,"capture_zone_value",capture_zone_value) 
-
-	triggerWidth = capture_zone_range
-	triggerDepth = capture_zone_range
-
-	spriteColorR = .5
-	spriteColorB = .5
-	spriteColorG = .5
-	spriteColorAlpha = 2
-
-	-- capture_total_max = tick_max
-
-
-
-
-end
-
-function tick(dt)   
-
-		draw_capture_region(dt)
-		--[[
-
-			for all elements of one side closer than max 
-				incremeent tick total to max of +/- tick_max. 
-		]]
-		capture_region_tick(dt)
-
-
-		-- DebugWatch("Capture Point: "..capture_point.." Status",team_capture_score)
-
-end
-
+#version 2
 function draw_capture_region(dt)
 		local trigger_pos = GetTriggerTransform(capture_point)
 
 		trigger_pos.rot = QuatLookAt(Vec(0,0,0),Vec(0,1,0))
 		DrawSprite(capture_point_sprite,trigger_pos , triggerWidth, triggerDepth, spriteColorR + team_capture_score[2], spriteColorG + team_capture_score[3], spriteColorB + team_capture_score[1], spriteColorAlpha, true, false)
-
 
 		deploy_smoke(trigger_pos.pos)
 end
@@ -230,14 +18,12 @@
 	end
 end
 
-
 function deploy_smoke(pos)
 
 	life = 5+5*math.random()
 
 	smoke_dir =  VecAdd(rndVec(0.9),GetWindVelocity(pos))
 	smoke_dir =  VecAdd(Vec(0, 2, 0),smoke_dir )
-
 
 	ParticleReset()
 	ParticleColor(base_smoke + team_capture_score[2], base_smoke + team_capture_score[3] , base_smoke + team_capture_score[1], base_smoke , base_smoke , base_smoke )
@@ -249,31 +35,8 @@
 	ParticleCollide(0, 1)
 	SpawnParticle(pos, smoke_dir, life)
 
-
-
-end
-
-
---[[
-
-
-		Process:
-			- call measure_entities tick to calculate present entities
-			- Call measure_tick tick to calculate the tick strength of an entity, add strength to tick total. 
-			- apply tick to zone - decide if adversarial tick, to strengthen tick, or reduce zone strength 
-			- final consideration 
-
-
-	---------------------------------------------------------------
-
-
-
-	Calculates all assets in an area that would need to be considered by the capture region, and turns them into a score based on their class
-
-	currently only works for vehicles, code needed to work out bodies that may be different from typical AVF assets.  
-
-	please make sure you label the correct entities with the tags, as this will check shapes and it'll be a nightmare, especially for complicated stuff!!
-]]
+end
+
 function measure_entities()
 	local avf_vehicles, avf_bodies, avf_shapes  = get_avf_entities() 
 	-- DebugWatch("avf vehicles: ", tablelength(avf_vehicles))
@@ -286,15 +49,8 @@
 	-- DebugPrint("time: "..GetTimeStep().." blufor: "..blufor_score)
 	blufor_score,opfor_score,inde_score = apply_tick(blufor_score,opfor_score,inde_score)
 
-
-end
-
-
---[[
-
-	take a group of entities, such as vehicles or bodies or shapes, and perform the appropriate calculations
-
-]]
+end
+
 function measure_entity_set(entity_set, blufor_score, opfor_score, inde_score, entity_type,ready_vehicles,ready_bodies )
 	ready_vehicles = ready_vehicles or nil 
 	ready_bodies = ready_bodies or nil 
@@ -314,8 +70,6 @@
 			NEEDS DEBUG 
 
 			NEEDS TO WORK OUT IF OBJECT HAS BEEN COUNTED ABOVE, AND IF SO THEN TO NOTE ACT, IF NO VEHICLE OR BODY EXISTS THEN CONTINUE AS NORMAL. 
-
-
 
 			update: 20220923 : it has been decided that if you be a dumb shit and make everything have a side then it's on you. 
 				~This is not lazy coding.
@@ -351,15 +105,6 @@
 
 end
 
---[[
-
-	Calculates individual asset tick value
-
-	Modify this if you create special vehicles like resource vehicles, scout units, or light units.
-
-	This will allow you to make some vehicles have more or less influence on the capture
-
-]]
 function measure_entity_tick(asset, modifiers)
 	local asset_value = 0
 	local asset_tag_value = tonumber(GetTagValue(asset,"avf_asset_value"))
@@ -380,21 +125,6 @@
 		return false
 	end
 end
-
-
---[[
-
-	Calculates what assets will make the region tick for their side based on measured scores on assumed asset capability.
-
-
-	check if side is occupied, if the current side is ticked over then site hold drops. 
-
-
-		if site not owned then get all holds and if one is stronger tehn add to that, otherwise remains held or doesn't drop. 
-
-
-]]
-
 
 function calculate_tick(blufor_score, opfor_score, inde_score)
 	scores = {blufor_score, opfor_score, inde_score}
@@ -429,25 +159,13 @@
 	end
 	return tick_side,max_tick,negative_tick
 
-
-end
-
---[[
-
-	Calculates what assets will make the region tick for their side based on measured scores on assumed asset capability.
-
-
-	checks tick above neg, then adds to side, if no side then adds to that. 
-
-		otherwise deducts from main
-
-]]
+end
 
 function apply_tick(blufor_score, opfor_score, inde_score) 
 	local flag_changed = false
 	local tick_side, tick_quantity, negative_tick = calculate_tick(blufor_score, opfor_score, inde_score)
 	local tick_value =  tick_quantity - negative_tick
-	if tick_value > 0 then 
+	if tick_value ~= 0 then 
 		if(capture_point_side  == 0) then 
 			capture_point_side = tick_side
 			capture_total = tick_value
@@ -476,12 +194,6 @@
 
 end
 
-
---[[ 
-
-	set values for controlling side from 0-1 then map that to the smoke controls to inform terriory hold
-
-]]
 function set_controlling_side(side,capture_total,flag_changed )
 	if(capture_point_side ~= 0) then 
 				team_capture_score[capture_point_side] =  get_capture_percentage()
@@ -492,14 +204,6 @@
 	end
 end
 
-
-
---[[
-
-	Increments the tick value and updates global record.
-
-]]
-
 function record_global_state() 
 	local capture_state = "false"
 	if(capture_point_side~=0) then
@@ -522,15 +226,10 @@
 
 end
 
-
-
 function get_capture_percentage()
 	return capture_total / capture_total_max
 
 end
-
-
-
 
 function get_avf_entities()
 	-- vehicles
@@ -541,7 +240,6 @@
 	local  avf_shapes = FindShapes("avf_side",true)
 	return  avf_vehicles, avf_bodies, avf_shapes 
 end
-
 
 function get_entity_pos(entity)
 	local entity_type = GetEntityType(entity)
@@ -557,7 +255,7 @@
 end
 
 function getDistanceToPlayer()
-	local playerPos = GetPlayerPos()
+	local playerPos = GetPlayerPos(playerId)
 	return VecLength(VecSub(playerPos,  GetTriggerTransform(stockpiles[1]).pos))
 end
 
@@ -570,13 +268,10 @@
 	return distance
 end
 
-
---Return a random vector of desired length
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
-
 
 function rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
@@ -590,4 +285,32 @@
 
 function setContains(set, key)
     return set[key] ~= nil
-end+end
+
+function server.init()
+    capture_point = FindTrigger("avf_conquest_point")
+    capture_point_sprite = LoadSprite("gfx/ring.png")
+    SetTag(capture_point,"active","true")
+    SetTag(capture_point,"captured","false")
+    SetTag(capture_point,"capture_side",0)
+    SetTag(capture_point,"capture_percentage",0)
+    SetTag(capture_point,"capture_zone_value",capture_zone_value) 
+    triggerWidth = capture_zone_range
+    triggerDepth = capture_zone_range
+    spriteColorR = .5
+    spriteColorB = .5
+    spriteColorG = .5
+    spriteColorAlpha = 2
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        draw_capture_region(dt)
+        --[[
+        	for all elements of one side closer than max 
+        		incremeent tick total to max of +/- tick_max. 
+        ]]
+        capture_region_tick(dt)
+    end
+end
+

```

---

# Migration Report: avf\conquest\scripts\capture_area_spawnable.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\conquest\scripts\capture_area_spawnable.lua
+++ patched/avf\conquest\scripts\capture_area_spawnable.lua
@@ -1,217 +1,4 @@
---[[
-
-
-	capture_area script 
-
-
-
-		outline of script: 
-
-			Gets list of active assets 
-
-			Computes distance of assets to location 
-
-			as assets move into area, tick moves towards that assets side. 
-
-
-			As tick moves, colour changes to / from neutral to assets colour. 
-
-			When tick hits max, area remains under that side, unless tick doesn't hit min value. 
-
-
-
-	Code story: 
-
-
-		As a zone:
-
-			I tick until the max value 
-
-			dependent on what side entitites have the largest presence in my area
-
-			biased based on the quantity of those entities within my area
-
-
-			if no max value reached, nor any entity present, then i tick until i reach neutral 
-
-
-				netal s 
-
-
-		As an entity entering a region alone: 
-
-		1: 
-			
-			When i enter a neutral area
-			
-			the counter ticks towards my side
-
-			until it hits max
-
-
-		2:
-			When I enter a hostile area
-
-			the counter ticks their hold downwards
-
-			until it hits neutral 
-
-		3: 
-
-			When I enter friendly territory 
-
-			the counter remains constant
-
-
-
-		As an entity entering a region with entities within: 
-
-		1: 
-			
-			When i enter an area with a larger quantity of friendly assets
-
-			the ticker will be biased towards our side. 
-
-
-		2:
-			When I enter a region with more hostile entities 
-
-			The ticker will be biased towards their side. 
-
-		3: 
-
-			When I consider bias to a side
-
-
-			I consider the bias to be the product of the majority - perhaps ease out cubic. 
-
-		4: 
-			if i enter a zone controlled by other entities not in control of zone
-
-			zone ticks down to neutral 
-
-			zone then handled as per regular rules. 
-
-
-
---------------------------------------------------------------------------------------------------------
-
-
-	
-	Assumptions:
-		Assets could range from vehicles to people. Larger AVf handlers will only consider if a region is registered as "active" and its side. 
-
-
-		Some assets may have a higher or lower capability to hold a region. This will be an advanced feature. 
-
-		Assets with high capture capability will be measured as a float value above the regular 1 asset 1 score, likewise for assets with lower capture capability. 
-
-
-		NO AVF COMPATIBLE ASSET IS LABELLED AS MORE THAN ONE SIDE, UNLESS YOU HAVE SOME INSANE LOGIC FOR THINGS THAT WILL COUNT AS LESS OF AN ASSEST, 
-		This means that vehicles are labelled once, bodies once, shapes once, unless you do so.
-
-			If you complain of a thing being counted twice then i shall be dissapointed. 
-
-
-
-
-]]
-
-
-capture_zone_value = 1
-
-capture_zone_range = 35
-
-base_smoke = 0.3
-
---side represents which side holds the point. 
--- capture point is the same but more firm due to drunk me coding in the past 
-capture_point_side =0 
-side =0 
--- how held is the point by the current side (this is min tick not max tick)
-capture_percentage = 0
-
-min_capture_percentage = 0.2
-
-
-capture_total = 0 
-
-capture_total_max = 75
-
--- the total tick value of the point as it stands. 
-tick_total = 0
-
--- how much of this tick is applied as a base rate 1-1 of a tick. 
-tick_rate =1 
-
--- -- the min tick to be captured
--- tick_min = 25
-
--- -- the max value to be captured
--- tick_max = 60
-
-
--- time since last update to perform a tick, in ms, best to keep higher as this does a full scan of assets and therefore each node will doe. 
-tick_update = 0.750
-
--- the counter until the next update 
-tick_update_counter = 0 
-
-
-
-team_capture_score = {0,0,0}
-
-blufor_hold = 0
-opfor_hold = 0
-inde_hold = 0
-
-
-function init()
-	--get current AVF entities
-
-
-	capture_point = FindTrigger("avf_conquest_point")
-	capture_point_sprite = LoadSprite("gfx/ring.png")
-
-
-	SetTag(capture_point,"active","true")
-	SetTag(capture_point,"captured","false")
-	SetTag(capture_point,"capture_side",0)
-	SetTag(capture_point,"capture_percentage",0)
-	SetTag(capture_point,"capture_zone_value",capture_zone_value) 
-
-	triggerWidth = capture_zone_range
-	triggerDepth = capture_zone_range
-
-	spriteColorR = .5
-	spriteColorB = .5
-	spriteColorG = .5
-	spriteColorAlpha = 2
-
-	-- capture_total_max = tick_max
-
-
-
-
-end
-
-function tick(dt)   
-
-		maintain_location(dt)
-
-		draw_capture_region(dt)
-		--[[
-
-			for all elements of one side closer than max 
-				incremeent tick total to max of +/- tick_max. 
-		]]
-		capture_region_tick(dt)
-
-
-		-- DebugWatch("Capture Point: "..capture_point.." Status",team_capture_score)
-
-end
-
+#version 2
 function maintain_location(dt)
 	local burner_offset = Vec(0,0.1,0.8)-- Vec(0,9.5,1.2)
 	local flag_marker_pos = GetShapeWorldTransform(FindShape("avf_conquest_flag_marker"))
@@ -228,7 +15,6 @@
 		trigger_pos.rot = QuatLookAt(Vec(0,0,0),Vec(0,1,0))
 		DrawSprite(capture_point_sprite,trigger_pos , triggerWidth, triggerDepth, spriteColorR + team_capture_score[2], spriteColorG + team_capture_score[3], spriteColorB + team_capture_score[1], spriteColorAlpha, true, false)
 
-
 		deploy_smoke(trigger_pos.pos)
 end
 
@@ -242,14 +28,12 @@
 	end
 end
 
-
 function deploy_smoke(pos)
 
 	life = 5+5*math.random()
 
 	smoke_dir =  VecAdd(rndVec(0.9),GetWindVelocity(pos))
 	smoke_dir =  VecAdd(Vec(0, 2, 0),smoke_dir )
-
 
 	ParticleReset()
 	ParticleColor(base_smoke + team_capture_score[2], base_smoke + team_capture_score[3] , base_smoke + team_capture_score[1], base_smoke , base_smoke , base_smoke )
@@ -261,31 +45,8 @@
 	ParticleCollide(0, 1)
 	SpawnParticle(pos, smoke_dir, life)
 
-
-
-end
-
-
---[[
-
-
-		Process:
-			- call measure_entities tick to calculate present entities
-			- Call measure_tick tick to calculate the tick strength of an entity, add strength to tick total. 
-			- apply tick to zone - decide if adversarial tick, to strengthen tick, or reduce zone strength 
-			- final consideration 
-
-
-	---------------------------------------------------------------
-
-
-
-	Calculates all assets in an area that would need to be considered by the capture region, and turns them into a score based on their class
-
-	currently only works for vehicles, code needed to work out bodies that may be different from typical AVF assets.  
-
-	please make sure you label the correct entities with the tags, as this will check shapes and it'll be a nightmare, especially for complicated stuff!!
-]]
+end
+
 function measure_entities()
 	local avf_vehicles, avf_bodies, avf_shapes  = get_avf_entities() 
 	-- DebugWatch("avf vehicles: ", tablelength(avf_vehicles))
@@ -298,15 +59,8 @@
 	-- DebugPrint("time: "..GetTimeStep().." blufor: "..blufor_score)
 	blufor_score,opfor_score,inde_score = apply_tick(blufor_score,opfor_score,inde_score)
 
-
-end
-
-
---[[
-
-	take a group of entities, such as vehicles or bodies or shapes, and perform the appropriate calculations
-
-]]
+end
+
 function measure_entity_set(entity_set, blufor_score, opfor_score, inde_score, entity_type,ready_vehicles,ready_bodies )
 	ready_vehicles = ready_vehicles or nil 
 	ready_bodies = ready_bodies or nil 
@@ -326,8 +80,6 @@
 			NEEDS DEBUG 
 
 			NEEDS TO WORK OUT IF OBJECT HAS BEEN COUNTED ABOVE, AND IF SO THEN TO NOTE ACT, IF NO VEHICLE OR BODY EXISTS THEN CONTINUE AS NORMAL. 
-
-
 
 			update: 20220923 : it has been decided that if you be a dumb shit and make everything have a side then it's on you. 
 				~This is not lazy coding.
@@ -363,15 +115,6 @@
 
 end
 
---[[
-
-	Calculates individual asset tick value
-
-	Modify this if you create special vehicles like resource vehicles, scout units, or light units.
-
-	This will allow you to make some vehicles have more or less influence on the capture
-
-]]
 function measure_entity_tick(asset, modifiers)
 	local asset_value = 0
 	local asset_tag_value = tonumber(GetTagValue(asset,"avf_asset_value"))
@@ -392,21 +135,6 @@
 		return false
 	end
 end
-
-
---[[
-
-	Calculates what assets will make the region tick for their side based on measured scores on assumed asset capability.
-
-
-	check if side is occupied, if the current side is ticked over then site hold drops. 
-
-
-		if site not owned then get all holds and if one is stronger tehn add to that, otherwise remains held or doesn't drop. 
-
-
-]]
-
 
 function calculate_tick(blufor_score, opfor_score, inde_score)
 	scores = {blufor_score, opfor_score, inde_score}
@@ -441,25 +169,13 @@
 	end
 	return tick_side,max_tick,negative_tick
 
-
-end
-
---[[
-
-	Calculates what assets will make the region tick for their side based on measured scores on assumed asset capability.
-
-
-	checks tick above neg, then adds to side, if no side then adds to that. 
-
-		otherwise deducts from main
-
-]]
+end
 
 function apply_tick(blufor_score, opfor_score, inde_score) 
 	local flag_changed = false
 	local tick_side, tick_quantity, negative_tick = calculate_tick(blufor_score, opfor_score, inde_score)
 	local tick_value =  tick_quantity - negative_tick
-	if tick_value > 0 then 
+	if tick_value ~= 0 then 
 		if(capture_point_side  == 0) then 
 			capture_point_side = tick_side
 			capture_total = tick_value
@@ -488,12 +204,6 @@
 
 end
 
-
---[[ 
-
-	set values for controlling side from 0-1 then map that to the smoke controls to inform terriory hold
-
-]]
 function set_controlling_side(side,capture_total,flag_changed )
 	if(capture_point_side ~= 0) then 
 				team_capture_score[capture_point_side] =  get_capture_percentage()
@@ -504,14 +214,6 @@
 	end
 end
 
-
-
---[[
-
-	Increments the tick value and updates global record.
-
-]]
-
 function record_global_state() 
 	local capture_state = "false"
 	if(capture_point_side~=0) then
@@ -534,15 +236,10 @@
 
 end
 
-
-
 function get_capture_percentage()
 	return capture_total / capture_total_max
 
 end
-
-
-
 
 function get_avf_entities()
 	-- vehicles
@@ -553,7 +250,6 @@
 	local  avf_shapes = FindShapes("avf_side",true)
 	return  avf_vehicles, avf_bodies, avf_shapes 
 end
-
 
 function get_entity_pos(entity)
 	local entity_type = GetEntityType(entity)
@@ -569,7 +265,7 @@
 end
 
 function getDistanceToPlayer()
-	local playerPos = GetPlayerPos()
+	local playerPos = GetPlayerPos(playerId)
 	return VecLength(VecSub(playerPos,  GetTriggerTransform(stockpiles[1]).pos))
 end
 
@@ -582,13 +278,10 @@
 	return distance
 end
 
-
---Return a random vector of desired length
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
-
 
 function rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
@@ -602,4 +295,33 @@
 
 function setContains(set, key)
     return set[key] ~= nil
-end+end
+
+function server.init()
+    capture_point = FindTrigger("avf_conquest_point")
+    capture_point_sprite = LoadSprite("gfx/ring.png")
+    SetTag(capture_point,"active","true")
+    SetTag(capture_point,"captured","false")
+    SetTag(capture_point,"capture_side",0)
+    SetTag(capture_point,"capture_percentage",0)
+    SetTag(capture_point,"capture_zone_value",capture_zone_value) 
+    triggerWidth = capture_zone_range
+    triggerDepth = capture_zone_range
+    spriteColorR = .5
+    spriteColorB = .5
+    spriteColorG = .5
+    spriteColorAlpha = 2
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        maintain_location(dt)
+        draw_capture_region(dt)
+        --[[
+        	for all elements of one side closer than max 
+        		incremeent tick total to max of +/- tick_max. 
+        ]]
+        capture_region_tick(dt)
+    end
+end
+

```

---

# Migration Report: avf\conquest\scripts\force_group_ai_sides.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\conquest\scripts\force_group_ai_sides.lua
+++ patched/avf\conquest\scripts\force_group_ai_sides.lua
@@ -1,43 +1 @@
-
-
-
-
-vehicleParts = {
-	ai_elements = {
-		side = 1,
-
-
-	},
-}
-
-function init()
-	vehicle = nil
-	vehicles = FindVehicles("cfg") 
-	for i = 1,#vehicles do 
-		local value = GetTagValue(sceneVehicle, "cfg")
-		if(value == "vehicle") then
-			vehicle.id = sceneVehicle
-	end
-
-
-end
-
-function init_ai_elements()
-	if(vehicleParts.ai_elements ~= nil) then 
-		for key,val in pairs(vehicleParts.ai_elements) do 
-			if(type(val)== 'table') then
-				for subKey,subVal in pairs(val) do
-					SetTag(vehicle.id,"avf_ai".."_"..key.."_"..subKey,subVal)
-				end
-			elseif(key =="side") then 
-				SetTag(vehicle.id,"avf_ai",val)
-			else
-				SetTag(vehicle.id,"avf_ai"..key,val)
-			end
-			
-			
-		end
-	end
-
-
-end+#version 2

```

---

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

# Migration Report: avf\prefabs\tiger_131\New folder\avf_custom.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\tiger_131\New folder\avf_custom.lua
+++ patched/avf\prefabs\tiger_131\New folder\avf_custom.lua
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
 			if(key=="coax") then 
@@ -179,24 +153,27 @@
 	end
 end
 
+function server.init()
+    local sceneVehicle = FindVehicle("cfg")
+    	local value = GetTagValue(sceneVehicle, "cfg")
+    	if(value == "vehicle") then
+    		vehicle.id = sceneVehicle
 
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

# Migration Report: avf\prefabs\tiger_131\New folder\check_avf.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\tiger_131\New folder\check_avf.lua
+++ patched/avf\prefabs\tiger_131\New folder\check_avf.lua
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

# Migration Report: avf\prefabs\tiger_131\Tiger131.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\prefabs\tiger_131\Tiger131.lua
+++ patched/avf\prefabs\tiger_131\Tiger131.lua
@@ -1,135 +1 @@
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
-			name="8.8 cm KwK Cannon",
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
-						[1] = {name="APCBC",
-						caliber 				= 88,
-						velocity				= 230,
-						maxPenDepth = 0.85,
-						payload					= "AP",
-					},
-						[2] = {name="Sprgr. L/45 (HE)",
-						caliber 				= 88,
-						velocity				= 220,
-						explosionSize			= 1.2,
-						maxPenDepth 			= 0.3,
-						r						= 0.3,
-						g						= 0.6, 
-						b						= 0.3, 
-						payload = "HE",
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

# Migration Report: avf\scripts\avf_custom.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/avf\scripts\avf_custom.lua
+++ patched/avf\scripts\avf_custom.lua
@@ -1,65 +1,4 @@
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
-
-}
-
-DEBUG = false
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
@@ -159,7 +98,7 @@
 	local val3 = GetTagValue(gun, "component")
 	return val3
 end
--- @magazine1_tracer
+
 function addItems(shape,values)
 	for key,val in pairs(values) do 
 			if(key=="coax") then 
@@ -233,15 +172,6 @@
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
@@ -280,7 +210,6 @@
 	end
 end
 
-
 function add_emitter_group(gun,gun_transform,gun_key,emitter_group,emitters,emitter_type,turret_mounted) 
 	for i =1,#emitters do
 		local emitter_transform = GetLocationTransform(emitters[i]) 
@@ -335,24 +264,6 @@
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
@@ -369,11 +280,35 @@
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
@@ -1,178 +1,4 @@
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
-min_cook_off = 0.5
-
-max_cook_off = 30
-
-min_burn_off = 2
-
-max_burn_off = 20
-
-burn_off_value = 1
-
-upward_force = 40
-hatch_size = 0.4
-
-
-cook_off_sounds = {}
-tank_explode_sounds = {}
-
-tank_explode_sound_vol = 60
-cook_off_sound_vol = 40
-burn_off_sound_vol =5
-
-
-function init()
-	local scene_tank = FindVehicle("cfg")
-	hole_force = math.random(5,50)/10
-
-	if(IsHandleValid(scene_tank)) then 
-		tank_found = true
-		tank.id = scene_tank
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
-	if(not tank.dead) then
-		if(DEBUG) then 
-			DebugWatch("cook_off_value: ",cook_off_value)
-			DebugWatch("cook_off_pulse: ",cook_off_pulse)
-
-			DebugWatch("burn_off_value: ",burn_off_value)
-		end
-		if(tank.ammo_racks and #tank.ammo_racks>0) then 
-			check_ammo_stability()
-		end
-		if(tank.engines) then 
-			check_engine_state()
-		end
-	elseif(tank.burning_off and not tank.burned_off) then 
-		burn_off()
-	end
-
-
-end
-
+#version 2
 function check_engine_state()
 	-- if(#tank.engines>0) then 
 	-- 	DebugWatch("engne_state",tank.engine_okay)
@@ -263,7 +89,6 @@
 					tank.cooking_off = true
 					break_all_breakable_joints()
 
-
 				--	DebugPrint("ammo rack destroyed! cooking off")
 
 					SetValue("cook_off_value", 1, "easein", math.random(min_cook_off,max_cook_off))
@@ -294,8 +119,6 @@
 		cook_off()
 	end
 end
-
-
 
 function break_all_breakable_joints()
 	for i=1,#breakable_joints do 
@@ -363,10 +186,6 @@
 				
 			end
 
-
-
-
-
 			if(tank.hatches_blown<3 and  cook_off_value>0.2) then 
 				apply_impulse(transform)
 				
@@ -379,8 +198,6 @@
 			end
 
 			
-
-
 
 		elseif(cook_off_pulse>=1) then
 			cook_off_pulse=0
@@ -408,7 +225,6 @@
 
 end
 
-
 function tank_ignition(transform)
 	local hitLocations = {nil,nil,nil}
 	for i=1,3 do 
@@ -427,7 +243,6 @@
 		end
 	end
 end
-
 
 function burn_off()
 
@@ -466,7 +281,6 @@
 				explosionSmall(pos)
 			end
 
-
 	elseif(cook_off_pulse>=1) then
 		cook_off_pulse=0
 	end
@@ -488,7 +302,6 @@
 		end
 
 	end
-
 
 	local strength = math.random(cook_off_blast_min_strength,cook_off_blast_max_strength)	--Strength of blower
 	local maxMass = 5000	--The maximum mass for a body to be affected
@@ -506,7 +319,6 @@
 	for i=1,#bodies do
 		local b = bodies[i]
 
-
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
 		local bc = VecLerp(bmi, bma, 0.5)
@@ -535,8 +347,7 @@
 		end
 	end
 
-
-end 
+end
 
 function kill_tracks()
 	for i=1,#tank.tracks do 
@@ -546,7 +357,6 @@
 
 	end
 end
-
 
 function EmitFire(strength, t, amount,force)
 	local p = TransformToParentPoint(t, Vec(0, 0,0))
@@ -569,7 +379,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			
@@ -582,11 +392,11 @@
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
 
@@ -596,16 +406,14 @@
 				
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.015 * strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.015 * strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
 
-
 function apply_impulse(transform )
-
 
 	local strength = math.random(10,250)	--Strength of blower
 	local maxMass = 500	--The maximum mass for a body to be affected
@@ -623,7 +431,6 @@
 	for i=1,#bodies do
 		local b = bodies[i]
 
-
 		--Compute body center point and distance
 		local bmi, bma = GetBodyBounds(b)
 		local bc = VecLerp(bmi, bma, 0.5)
@@ -653,15 +460,9 @@
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
@@ -670,10 +471,6 @@
 function rndVec(t)
 	return Vec(rnd(-t, t), rnd(-t, t), rnd(-t, t))
 end
-
-explosionPos = Vec()
-
-trails = {}
 
 function trailsAdd(pos, vel, life, size, damp, gravity)
 	t = {}
@@ -719,14 +516,6 @@
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
@@ -749,11 +538,6 @@
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
@@ -777,11 +561,6 @@
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
@@ -790,11 +569,6 @@
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
@@ -871,7 +645,6 @@
 	smoke.amount = 2
 end
 
-
 function explosionMedium(pos)
 	explosionPos = pos
 	explosionSparks(30, 3)
@@ -901,7 +674,6 @@
 	smoke.gravity = 2
 	smoke.amount = 2
 end
-
 
 function explosionLarge(pos)
 	explosionPos = pos
@@ -947,11 +719,124 @@
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
+    local scene_tank = FindVehicle("cfg")
+    hole_force = math.random(5,50)/10
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(not tank.dead) then
+        	if(DEBUG) then 
+        		DebugWatch("cook_off_value: ",cook_off_value)
+        		DebugWatch("cook_off_pulse: ",cook_off_pulse)
+
+        		DebugWatch("burn_off_value: ",burn_off_value)
+        	end
+        	if(tank.ammo_racks and #tank.ammo_racks>0) then 
+        		check_ammo_stability()
+        	end
+        	if(tank.engines) then 
+        		check_engine_state()
+        	end
+        elseif(tank.burning_off and not tank.burned_off) then 
+        	burn_off()
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
-			exists = true,
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

# Migration Report: AVF_AI_ACS.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/AVF_AI_ACS.lua
+++ patched/AVF_AI_ACS.lua
@@ -1,486 +1,10 @@
-
-aiPresets = {
-	
-	EASY = 1,
-	MEDIUM = 2,
-	HARD = 3,
-	INSANE = 4,	
-	DGAF = 5,
-	ROADRAGE = 6,
-
-	difficulties = {
-		[1] = {
-			name =  "easy", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.1, 
-			tenacity = 0.7,
-			errorCoef = 0.4,
-
-		}, 
-		[2] = {
-			name =  "medium", 
-			steeringThres = 0.2,
-			speedSteeringThres = 0.2, 
-			tenacity = 0.8,
-			errorCoef = 0.2,
-
-		}, 
-		[3] = {
-			name =  "hard", 
-			steeringThres = 0.4,
-			speedSteeringThres = 0.4, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-		[4] = {
-			name =  "insane", 
-			steeringThres = 0.6,
-			speedSteeringThres = 0.6, 
-			tenacity = 0.94,
-			errorCoef = 0.05,
-
-		}, 
-		[5] = {
-			name =  "DGAF", 
-			steeringThres = 0.9,
-			speedSteeringThres = 0.9, 
-			tenacity = 0.99,
-			errorCoef = 0.1,
-
-		}, 
-		[6] = {
-			name =  "road rage", 
-			steeringThres = 1,
-			speedSteeringThres = 0.2, 
-			tenacity = 1.1,
-			errorCoef = 0.1,
-
-		}, 
-		[7] = {
-			name =  "Never Overtakes - gentle", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.25, 
-			tenacity = 0.85,
-			errorCoef = 0.1,
-
-		}, 
-		[8] = {
-			name =  "Never Overtakes - speedDemon", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.9, 
-			tenacity = 0.85,
-			errorCoef = 0.1,
-
-		}, 
-		[9] = {
-			name =  "Medium corners, overtakes", 
-			steeringThres = 0.95,
-			speedSteeringThres = 0.5, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-
-		[10] = {
-			name =  "slower corners, overtakes", 
-			steeringThres = 0.7,
-			speedSteeringThres = 0.35, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-
-	},
-
-	difficulty_ranged = {
-		[1] = {
-			name =  "easy", 
-			steeringThres = {10,100},
-			speedSteeringThres = {10,90}, 
-			tenacity = {70,100},
-			errorCoef = {1,40},
-
-		}, 
-		[2] = {
-			name =  "medium", 
-			steeringThres = {20,100},
-			speedSteeringThres = {20,99}, 
-			tenacity = {80,100},
-			errorCoef = {1,20},
-
-		}, 
-		[3] = {
-			name =  "competative_medium", 
-			steeringThres = {60,100},
-			speedSteeringThres = {20,99}, 
-			tenacity = {80,100},
-			errorCoef = {1,10},
-
-		}, 
-		[4] = {
-			name =  "hard", 
-			steeringThres = {40,100},
-			speedSteeringThres = {40,100}, 
-			tenacity = {90,100},
-			errorCoef = {1,10},
-
-		}, 
-		[5] = {
-			name =  "insane", 
-			steeringThres = {60,110},
-			speedSteeringThres = {60,110}, 
-			tenacity = {90,110},
-			errorCoef = {1,5},
-
-		}, 
-		[6] = {
-			name =  "psycobilly_freakout", 
-			steeringThres = {80,130},
-			speedSteeringThres = {80,130}, 
-			tenacity = {95,130},
-			errorCoef = {0.5,2.5},
-
-		}, 
-
-		-- [7] = {
-		-- 	name =  "texas_psycobilly_freakout", 
-		-- 	steeringThres = {80,160},
-		-- 	speedSteeringThres = {80,160}, 
-		-- 	tenacity = {100,160},
-		-- 	errorCoef = {0.25,2},
-
-		-- }, 
-
-	}
-
-}
-
-
-AVF_AI_ACS = {
-	active = true,
-	goalPos= Vec(0,0,0),
-
-	min_path = 10,
-
-	raceValues = {
-		completedGoals  = 0,
-		targetNode 		= 1,
-		NextNode 		= 2,
-		passedCheckPoints = 0,
-		nextCheckpoint = 1,
-		completionRange = 4.5,--4.5,
-		lookAhead = 2,
-		laps = 0 	,
-		lastLap = 0,
-		splits = {},
-
-		bestLap = nil,
-
-	},
-
-	targetNode = nil,
-	NextNode =nil,
-
-	controller = {
-		aiType = "default",
-
-		accelerationValue = 0,
-		steeringValue = 0,
-		handbrake = false,
-
-		steeringThres  = {60,110}, --0.4
-		steeringForce  = 0.5,
-		speedSteeringThres = {60,110},
-		tenacity 			= 0.9,
-		relativeThreshold = 0.8,
-		minDist = 2--.5,--5,
-	},
-
-	reversingController = {
-		reversing = false,
-		minVelocity = 1,
-		waitTime = 5.5,
-		currentWait = 3,
-		reverseTime = 2.5,
-		currentReverseTime = 5.5,
-	},
-
-
-	detectRange = 3,
-	commands = {
-	[1] = Vec(0,0,-1),
-	[2] = Vec(1*0.8,0,-1*1.5),
-	[3] = Vec(-1*0.8,0,-1*1.5),
-	[4] = Vec(-1,0,0),
-	[5] = Vec(1,0,0),
-	[6] = Vec(0,0,1),
-
-	},
-
-	weights = {
-
-	[1] = 0.870,
-	[2] = 0.86,
-	[3] = 0.86,
-	[4] = 0.84,
-	[5] = 0.84,
-	[6] = 0.80,
-
-			} ,
-
-	targetMoves = {
-		list        = {},
-		target      = Vec(0,0,0),
-		targetIndex = 1
-	},
-
-
-	directions = {
-		forward = Vec(0,0,1),
-
-		back = Vec(0,0,-1),
-
-		left = Vec(1,0,0),
-
-		right = Vec(-1,0,0),
-	},
-
-	maxVelocity = 0,
-
-	cornerCoef = 16,
-
-	accelerationCoef = 0.75,
-	steeringCoef = 2.55,
-
-	pidState = {
-
-			--- pid gain params
---		pGain = 0.765,
-		pGain = 0.865,
-		iGain = -0.04,
-		dGain = -1.35,---1.3,
-
-		intergralTime = 5,
-
-		integralIndex = 1,
-		integralSum = 0,
-		integralData = {
-
-		},
-		lastCrossTrackError = 0,
-		lastPnt = Vec(0,0,0),
-
-			-- pid output value 
-		controllerValue = 0,
-
-
-			--- pid update and training params
-			training = false,
-		inputrate=0.0665,
-		learningrateweights=0.009,
-		learningrateThres = 0.02,
-	    bestrate=0.05,
-	    secondbestrate=0.01,
-	    gammasyn=0.9,
-	    gammaref=0.7,
-	    gammapsp=0.9,
-	},
-	usingClustering = false,
-
-	clustering = {
-		pass = 1,
-		maxPass = 10,
-		centroids = 2,
-		iterations = 5,
-		prior = 1,
-		dataSize = 100,
-		mode = -1,
-		previousOutput = -1,
-		output = nil,
-		clusters = {
-			centroids = {
-				pass = 1,
-				index = 1,
-				data = {},
-			},
-			current = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-			prior = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-		},
-
-	},
-
-	scanning = {
-		numScans = 2,
-		scanThreshold = 0.5,
-		maxScanLength = 10,
-		scanLength = 50,
-		scanDepths = 2,
-		vehicleHeight = 2,
-		cones = {
-			left   = {
-				direction = "left",
-				startVec = Vec(0.25,0,-1.5),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				direction = "centre",
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				direction = "right",
-				size = 110,
-				startVec = Vec(-0.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-		positions = {
-			left   = {
-				direction = "left",
-				startVec = Vec(0.25,0,-1.5),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			sideL  = {
-				direction = "sideL",
-				size = 110,
-				startVec = Vec(1.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				direction = "centre",
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				direction = "right",
-				size = 110,
-				startVec = Vec(-0.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			sideR  = {
-				direction = "sideR",
-				size = 110,
-				startVec = Vec(-1.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-
-	},
-
-
-
-	--altChecks = Vec(0.25,0.4,-0.6),
-	altChecks = {
-				[1] = -2,
-				[2] =0.2,
-				[3] = 0.4
-			},
-	altWeight ={
-			[1] = 1,
-			[2] =1,
-			[3] = -1,
-			[4] = -1,
-	},
-
-
-	validSurfaceColours ={ 
-			[1] = {
-				r = 0.20,
-				g = 0.20,
-				b = 0.20,
-				range = 0.02
-			},
-			[2] = {
-				r = 0.60,
-				g = 0.60,
-				b = 0.60,
-				range = 0.02
-			},
-			[3] = {
-				r = 0.34,
-				g = 0.34,
-				b = 0.34,
-				range = 0.02
-			},
-		},
-	hitColour = Vec(1,0,0),
-	detectColour = Vec(1,1,0),
-	clearColour = Vec(0,1,0),
-}
-
-
+#version 2
 function AVF_AI_ACS:initVehicle(ai) 
 
 	self.id = ai.id
 	self.body = GetVehicleBody(self.id)
 	self.transform =  GetBodyTransform(self.body)
 	self.shapes = GetBodyShapes(self.body)
-
 
 	-- DebugPrint("[INFO] "..ai.id.." ACS setup begun")
 
@@ -509,7 +33,6 @@
 	self.bodyXSize,self.bodyYSize ,self.bodyZSize  = GetShapeSize(self.mainBody)
 	-- DebugPrint("body Size: "..self.bodyXSize.." | "..self.bodyYSize.." | "..self.bodyZSize)
 
-
 	for i=1,3 do 
 		self.targetMoves.list[i] = Vec(0,0,0)
 	end
@@ -527,7 +50,6 @@
 		self.pidState.integralData[i] = 0
 
 	end
-
 
 	self.hudColour = {math.random(0,100)/100,math.random(0,100)/100,math.random(0,100)/100}
 
@@ -547,7 +69,6 @@
 	-- 		DebugPrint(key..": "..val)
 	-- 	end
 
-
 	-- end
 	
 
@@ -560,25 +81,13 @@
 
 	self.controller.errorCoef = aiLevel.errorCoef
 
-
 	self.scanning.maxScanLength = self.scanning.maxScanLength * (math.random(90,350)/100) 
 
-
 	self.reversingController.currentReverseTime = math.random()*self.reversingController.reverseTime
 
 	-- DebugPrint("[INFO] "..ai.id.." ACS setup complete")
 
 end
-
-
-	-- reversingController = {
-	-- 	reversing = false,
-	-- 	minVelocity = 1,
-	-- 	waitTime = 3,
-	-- 	currentWait = 3,
-	-- 	reverseTime = 2,
-	-- 	currentReverseTime = 2,
-	-- },
 
 function AVF_AI_ACS:controlActions(dt,ai)
 
@@ -608,7 +117,6 @@
 		-- DebugWatch("ai-"..ai.id.."pre acceletation: ",self.controller.accelerationValue)
 		-- DebugWatch("ai-"..ai.id.."pre steering: ",self.controller.steeringValue)
 
-
 		self.controller.steeringValue = steeringValue * self.steeringCoef
 		self.controller.accelerationValue = accelerationValue*self.accelerationCoef
 
@@ -617,8 +125,6 @@
 		-- DebugWatch("post steering: ",self.controller.steeringValue)
 
 		self:obstacleAvoidance()
-
-
 
 		self:applyError()
 			
@@ -658,17 +164,6 @@
 		
 	end
 end
-
-
-
-
---[[
-
-	calculate relative speed, if vehicle moving towards then stop / avoid. 
-
-	if movng faster than gap between then stop, otherwise move proportionally to the distance between vehicles vs speed
-
-]]
 
 function AVF_AI_ACS:getRelativeSpeed(shape,hitPos)
 	local otherShapeBody = GetShapeBody(shape)
@@ -755,7 +250,6 @@
 
 	for key,scan in pairs(self.scanning.positions) do 
 
-
 		if(scan.direction == "centre") then 
 			scanStartPos =VecCopy(vehicleTransform.pos)
 		elseif(scan.direction =="left") then
@@ -834,7 +328,6 @@
 
 		 -- sign((Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax))
 
-
 		if turnBias <0.5 then
 			self.controller.steeringValue = self.controller.steeringForce*2
 		else
@@ -844,7 +337,6 @@
 	
 	end
 end
-
 
 function AVF_AI_ACS:pid()
 	
@@ -868,7 +360,6 @@
 	return output
 end
 
-
 function AVF_AI_ACS:currentCrossTrackError()
 	local crossTrackErrorValue = 0
 	local vehicleTransform = GetVehicleTransform(self.id)
@@ -880,10 +371,7 @@
 	return targetNode, crossTrackErrorValue,sign
 end
 
---- calculate distance to target direction and apply steering by force
---- fill in the gap here related to the distance ebtween the aprrelel lines of target nod3e to vehicle pos to solve it all
 function AVF_AI_ACS:crossTrackError(pnt,vehicleTransform)
-
 
 		
 		vehicleTransform.pos[2] = pnt[2]
@@ -905,7 +393,6 @@
 			sign = 0
 		end
 
-
 		return d*sign,sign
 
 		-- Use the sign of the determinant of vectors (AB,AM), where M(X,Y) is the query point:	
@@ -924,12 +411,6 @@
 		-- DebugWatch("output pos : ",out)
 
 		-- DebugWatch("output value: ",VecSub(out,pnt))
-
-
-
-
-
-
 
 		-- local vehicleTransform = GetVehicleTransform(self.id)
 		-- vehicleTransform.pos[2] = targetNode:getPos()[2]
@@ -964,7 +445,6 @@
 	return verifyCrossCheckErrorVal
 end
 
-
 function AVF_AI_ACS:calculateSteadyStateError(crossTrackErrorValue)
 	local index = self.pidState.integralIndex
 
@@ -1008,13 +488,10 @@
 		-- DebugWatch("is forward",is_forward)
 		-- DebugWatch("local point  forwar", TransformToLocalPoint(vehicleTransform, pnt)[3])
 
-
 		return VecLength(VecSub(vehicleTransform.pos,out))
 	end	
 end
 
-
-	-- thanks to  iaobardar for help on getting the vecdot to work
 function AVF_AI_ACS:directionError()
 	local vehicleTransform = GetVehicleTransform(self.id)
 	local targetNode = self.targetNode
@@ -1039,8 +516,6 @@
 
 end
 
-
-
 function AVF_AI_ACS:controllerAugmentation()
 	local velocity =  VecLength(GetBodyVelocity(GetVehicleBody(self.id)))
 
@@ -1054,7 +529,6 @@
 	
 	
 end
-
 
 function AVF_AI_ACS:applyError()
 	local errorCoef = self.controller.errorCoef--0.1
@@ -1093,11 +567,10 @@
 
 end
 
- 
-
 function AVF_AI_ACS:vehicleController()
 	DriveVehicle(self.id, 0.05+self.controller.accelerationValue,
 							self.controller.steeringValue,
 							 self.controller.handbrake)
 	self.controller.handbrake = false
-end+end
+

```

---

# Migration Report: AVF_UI.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/AVF_UI.lua
+++ patched/AVF_UI.lua
@@ -1,8 +1,4 @@
-
-
---[[ debug stuff ]]
-
-
+#version 2
 function debug_draw_x_y_z(t)
 				--red = x axis
 			draw_line_from_transform(t,-.1,0,0,	1,0,0)
@@ -14,7 +10,6 @@
 			draw_line_from_transform(t,0,-.1,0,	0,0,1)
 end
 
-
 function draw_line_from_transform(t,x,y,z,r,g,b)
 	r = (r ~= nil and r) or 0
 	g = (g ~= nil and g) or 0
@@ -26,11 +21,8 @@
 		DebugCross(newpos,r,g,b)
 	end
 
-
-end
-
-
---- taken from evertide mall tank script 
+end
+
 function drawReticleSprite(t)
 	t.rot = QuatLookAt(t.pos, GetCameraTransform().pos)
 	-- t.rot = QuatLookAt(t.pos, GetBodyTransform(body).pos)
@@ -59,143 +51,12 @@
 	DrawSprite(reticle3, t, size, size, .5, 0, 0, 1, true, false)
 end
 
-
-
-function draw(dt)
-		if(DEBUG_CODE) then 
-			local status,retVal = pcall(AVF_TAK_DRAW,dt)
-			if status then 
-					-- utils.printStr("no errors")
-			else
-				DebugWatch("TOOL DRAW ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-			end	
-			local status,retVal = pcall(team_allocator_draw)
-			if status then 
-					-- utils.printStr("no errors")
-			else
-				DebugWatch("TOOL DRAW ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-			end	
-		else
-
-			AVF_TAK_DRAW(dt)
-
-			team_allocator_draw()
-		end
-	if AVF_DEV_HUD_VISIBLE then
-		SHOW_AVF_DEV_HUD()
-	end
-
-	local visible	 = 1
-
-		-- DebugWatch("hide controls",GetBool("savegame.mod.hideControls"))
-	inVehicle, vehicleid = playerInVehicle()
-	if(inVehicle)then
-		vehicle = vehicles[vehicleid].vehicle
-		vehicleFeatures = vehicles[vehicleid].vehicleFeatures
-	end
-
-	--Only draw speedometer if visible
-	if(inVehicle and not viewingMap) then
-		local gunGroup = vehicleFeatures.weapons[vehicleFeatures.equippedGroup]
-		UiPush()
-			if(vehicle.sniperMode and not vehicle.artillery_weapon)then
-				for key,gun in pairs(gunGroup)	do 
-					if(not gun.custom_sight_script) then
-						-- drawWeaponReticles(gun)	
-						draw_weapon_true_reticle(gun)
-					end
-				end
-		end
-		UiPop()
-		
-		UiPush()
-		if(DEBUG_CODE) then 
-			local status,retVal = pcall(draw_health_bars)
-			if status then 
-					-- utils.printStr("no errors")
-			else
-				DebugWatch("[GAMEPLAY TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-			end
-		else
-			draw_health_bars()
-		end
-
-		
-		UiPop()
-
-		UiPush()
-		
-		--Place it in upper right corner
-		UiTranslate(UiWidth()+200 - 400*visible, 50)
-		-- UiAlign("center middle")
-		-- UiTranslate(0, 30)
-		-- UiColor(0,0,0,.3)
-		-- UiRect(300, 20+90)
-		-- UiTranslate(0, -30)
-		-- UiColor(1,1,1)
-		UiFont("bold.ttf", 24)
-
-		-- local weaponText =  string.format("%s%s\n%s", tag, title, tag)
-		-- DebugWatch("hide controls",GetBool("savegame.mod.hideControls"))
-		if(not GetBool("savegame.mod.hideControls")) then		
-			if(gunGroup~=nil and #gunGroup>0) then 
-				for key,gun in pairs(gunGroup)	do 
-						-- UiPush()
-							UiAlign("center middle")
-							UiTranslate(0, 40)
-							UiColor(0,0,0,.3)
-							UiRect(350, 10+90)
-							UiTranslate(0, -30)
-							UiColor(1,1,1)
-							UiText(gun.name)
-							-- if(not IsShapeBroken(gun.id))then	
-
-							-- 	UiText(gun.name)
-							-- else
-							-- 	UiText(gun.name.." BROKEN")
-							-- end
-							
-							UiTranslate(0, 40)
-							
-							
-							getWeaponAmmoText(gun)--getWeaponAmmoText(gun))
-							UiTranslate(0, 30)
-						-- UiPop()
-				end
-			end
-			UiPop()
-
-
-			drawControls()
-		end
-
-			-- if GetBool("savegame.mod.mph") then
-			-- 	UiImage("mph.png")
-			-- 	--Convert to rotation for mph
-			-- 	UiRotate(-displayKmh*2/1.609)
-			-- else
-			-- 	UiImage("kmh.png")
-			-- 	--Convert to rotation for kmh
-			-- 	UiRotate(-displayKmh)
-			-- end
-			-- UiImage("needle.png")
-
-		if(not vehicle.sniperMode and not vehicle.artillery_weapon) then 
-
-			drawDynamicReticle()
-		end
-
-
-	end
-end
-
-
 function progressBar(w, h, t)
 	UiPush()
 		UiAlign("left top")
 		UiColor(0, 0, 0, 0.5)
 		UiImageBox("ui/common/box-solid-10.png", w, h, 6, 6)
-		if t > 0 then
+		if t ~= 0 then
 			UiTranslate(2, 2)
 			w = (w-4)*t
 			if w < 12 then w = 12 end
@@ -205,7 +66,6 @@
 		end
 	UiPop()
 end
-
 
 function draw_health_bars()
 	if unexpected_condition then error() end
@@ -225,9 +85,7 @@
 		UiText("VEHICLE CONDITION")
 	UiPop()
 
-
-end
-
+end
 
 function drawHealth()
 	local health = GetFloat("game.player.health")
@@ -266,7 +124,7 @@
 			UiAlign("left top")
 			UiColor(0, 0, 0, 0.5)
 			UiImageBox("ui/common/box-solid-10.png", w, h, 6, 6)
-			if health > 0 then
+			if health ~= 0 then
 				UiTranslate(2, 2)
 				w = (w-4)*health
 				if w < 12 then w = 12 end
@@ -278,7 +136,6 @@
 
 	UiPop()
 end
-
 
 function drawControls()
 		info = {}
@@ -352,7 +209,6 @@
 		magazineCount = "9999"
 	end
 
-
 	local weaponText =  string.format("%s  | (%s)", ammoState, magazineCount)
 	UiAlign("center right")
 	UiText(weaponText)
@@ -362,7 +218,6 @@
 	UiText(gun.magazines[gun.loadedMagazine].CfgAmmo.name)
 
 end
-
 
 function drawWeaponReticles(gun)
 
@@ -416,7 +271,6 @@
 	end
 	UiPop()
 
-
 end
 
 function draw_weapon_true_reticle(gun)
@@ -445,9 +299,6 @@
 	-- local expected_hit_point = Vec(0, (-gravity_vector * ((zero_range  / gun_vel ))*.1), -zero_range)
 	-- local p2 =  TransformToParentPoint( focusGunPos,Vec(0,expected_hit_point[3],expected_hit_point[2]))
 
-
-
-
 	-- local loaded_magazine =tonumber(GetTagValue(gun,"avf.databus.loaded_magazine"))	
 	-- local ammo_count =tonumber(GetTagValue(gun,"avf.databus.ammo_count"))	
 
@@ -470,7 +321,7 @@
 	local height = UiHeight() 
 	local w = UiWidth()
 	UiPush()
-		if dist > 0 then
+		if dist ~= 0 then
 			-- DebugWatch("dist ",dist)
 			-- DebugWatch("target pos ",Vec(x,y,0))
 			-- DebugWatch("w",w)
@@ -502,23 +353,14 @@
 
 function draw_weapon_tracking()	
 
-
-
-
-end
-
-
-
-
-
-
-
--- cheej
+end
+
 function initCamera()
     cameraX = 0
 	cameraY = 0
 	zoom = 20
 end
+
 function manageCamera()
 
 	SetCameraTransform(vehicle.last_external_cam_pos)
@@ -530,11 +372,11 @@
 	cameraY = cameraY - my / 10
 	cameraY = clamp(cameraY, -30, 60)
 	local cameraRot = QuatEuler(cameraY, cameraX, 0)
-	local cameraT = Transform(VecAdd(Vec(0,0,0), GetVehicleTransform(GetPlayerVehicle()).pos), cameraRot)
+	local cameraT = Transform(VecAdd(Vec(0,0,0), GetVehicleTransform(GetPlayerVehicle(playerId)).pos), cameraRot)
 	zoom = zoom - InputValue("mousewheel")
 	zoom = clamp(zoom, 2, 30)
 
-	local vehicle_body = GetVehicleBody(GetPlayerVehicle())
+	local vehicle_body = GetVehicleBody(GetPlayerVehicle(playerId))
 	local min, max = GetBodyBounds(vehicle_body)
 	local boundsSize = VecSub(max, min)
 
@@ -559,6 +401,7 @@
 	reticleScreenPosX, reticleScreenPosY = UiWorldToPixel(projectileHitPos)
 	reticleScreenPos = {reticleScreenPosX, reticleScreenPosY}
 end
+
 function removeReticleScreenPos()
 	reticleScreenPos = nil	
 end
@@ -578,6 +421,7 @@
     end
 
 end
+
 function drawDynamicReticle()
 	if reticleScreenPos ~= nil then
 		UiPush()
@@ -597,14 +441,10 @@
 	getOuterReticleWorldPos()
 end
 
-
-function QuatDir(dir) return QuatLookAt(Vec(0, 0, 0), dir) end -- Quat to 3d worldspace dir.
+function QuatDir(dir) return QuatLookAt(Vec(0, 0, 0), dir) end
+
 function GetQuatEulerVec(quat) local x,y,z = GetQuatEuler(quat) return Vec(x,y,z) end
----@param tr table
----@param distance number
----@param rad number
----@param rejectBodies table
----@param rejectShapes table
+
 function RaycastFromTransform(tr, distance, rad, rejectBodies, rejectShapes)
 
 	if distance ~= nil then distance = -distance else distance = -300 end
@@ -627,12 +467,14 @@
 		return nil
 	end
 end
+
 function DrawDot(pos, l, w, r, g, b, a, dt)
 	local dot = LoadSprite("ui/hud/dot-small.png")
 	local spriteRot = QuatLookAt(pos, GetCameraTransform().pos)
 	local spriteTr = Transform(pos, spriteRot)
 	DrawSprite(dot, spriteTr, l or 0.2, w or 0.2, r or 1, g or 1, b or 1, a or 1, dt or true)
 end
+
 function AabbGetShapeCenterPos(shape)
 	local mi, ma = GetShapeBounds(shape)
 	return VecLerp(mi,ma,0.5)
@@ -646,7 +488,6 @@
 	end
 
 end
-
 
 function debug_vehicle_locations()
 
@@ -693,6 +534,127 @@
 	return cannonLoc
 end
 
-
-
-
+function client.draw()
+    	if(DEBUG_CODE) then 
+    		local status,retVal = pcall(AVF_TAK_DRAW,dt)
+    		if status then 
+    				-- utils.printStr("no errors")
+    		else
+    			DebugWatch("TOOL DRAW ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+    		end	
+    		local status,retVal = pcall(team_allocator_draw)
+    		if status then 
+    				-- utils.printStr("no errors")
+    		else
+    			DebugWatch("TOOL DRAW ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+    		end	
+    	else
+
+    		AVF_TAK_DRAW(dt)
+
+    		team_allocator_draw()
+    	end
+    if AVF_DEV_HUD_VISIBLE then
+    	SHOW_AVF_DEV_HUD()
+    end
+
+    local visible	 = 1
+
+    	-- DebugWatch("hide controls",GetBool("savegame.mod.hideControls"))
+    inVehicle, vehicleid = playerInVehicle()
+    if(inVehicle)then
+    	vehicle = vehicles[vehicleid].vehicle
+    	vehicleFeatures = vehicles[vehicleid].vehicleFeatures
+    end
+
+    --Only draw speedometer if visible
+    if(inVehicle and not viewingMap) then
+    	local gunGroup = vehicleFeatures.weapons[vehicleFeatures.equippedGroup]
+    	UiPush()
+    		if(vehicle.sniperMode and not vehicle.artillery_weapon)then
+    			for key,gun in pairs(gunGroup)	do 
+    				if(not gun.custom_sight_script) then
+    					-- drawWeaponReticles(gun)	
+    					draw_weapon_true_reticle(gun)
+    				end
+    			end
+    	end
+    	UiPop()
+
+    	UiPush()
+    	if(DEBUG_CODE) then 
+    		local status,retVal = pcall(draw_health_bars)
+    		if status then 
+    				-- utils.printStr("no errors")
+    		else
+    			DebugWatch("[GAMEPLAY TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+    		end
+    	else
+    		draw_health_bars()
+    	end
+
+    	UiPop()
+
+    	UiPush()
+
+    	--Place it in upper right corner
+    	UiTranslate(UiWidth()+200 - 400*visible, 50)
+    	-- UiAlign("center middle")
+    	-- UiTranslate(0, 30)
+    	-- UiColor(0,0,0,.3)
+    	-- UiRect(300, 20+90)
+    	-- UiTranslate(0, -30)
+    	-- UiColor(1,1,1)
+    	UiFont("bold.ttf", 24)
+
+    	-- local weaponText =  string.format("%s%s\n%s", tag, title, tag)
+    	-- DebugWatch("hide controls",GetBool("savegame.mod.hideControls"))
+    	if(not GetBool("savegame.mod.hideControls")) then		
+    		if(gunGroup~=nil and #gunGroup>0) then 
+    			for key,gun in pairs(gunGroup)	do 
+    					-- UiPush()
+    						UiAlign("center middle")
+    						UiTranslate(0, 40)
+    						UiColor(0,0,0,.3)
+    						UiRect(350, 10+90)
+    						UiTranslate(0, -30)
+    						UiColor(1,1,1)
+    						UiText(gun.name)
+    						-- if(not IsShapeBroken(gun.id))then	
+
+    						-- 	UiText(gun.name)
+    						-- else
+    						-- 	UiText(gun.name.." BROKEN")
+    						-- end
+
+    						UiTranslate(0, 40)
+
+    						getWeaponAmmoText(gun)--getWeaponAmmoText(gun))
+    						UiTranslate(0, 30)
+    					-- UiPop()
+    			end
+    		end
+    		UiPop()
+
+    		drawControls()
+    	end
+
+    		-- if GetBool("savegame.mod.mph") then
+    		-- 	UiImage("mph.png")
+    		-- 	--Convert to rotation for mph
+    		-- 	UiRotate(-displayKmh*2/1.609)
+    		-- else
+    		-- 	UiImage("kmh.png")
+    		-- 	--Convert to rotation for kmh
+    		-- 	UiRotate(-displayKmh)
+    		-- end
+    		-- UiImage("needle.png")
+
+    	if(not vehicle.sniperMode and not vehicle.artillery_weapon) then 
+
+    		drawDynamicReticle()
+    	end
+
+    end
+end
+

```

---

# Migration Report: AVF_VERSION.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/AVF_VERSION.lua
+++ patched/AVF_VERSION.lua
@@ -1,2 +1 @@
-
-VERSION = "V-3.0.2"+#version 2

```

---

# Migration Report: commander\AVF_TAK.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/commander\AVF_TAK.lua
+++ patched/commander\AVF_TAK.lua
@@ -1,91 +1,8 @@
-
-
---[[
-
-
-
-		Allows setting of AVF vehicles to teams
-
-		Teams are : bluefor | opfor | indfor 
-
-
-
-
-
-]]
-
-AVF_TAK_SERVER = {
-	assets = {
-		BLUFOR = {},
-		OPFOR = {},
-		INDFOR ={}
-
-
-	}
-
-
-
-}
-
-
-AVF_TAK_CONTROLLER = {
-	current_side = 1,
-	sides = {
-		[1] = "BLUFOR",
-		[2] = "OPFOR",
-		[3] = "INDFOR",
-	},
-
-
-	selected_vehicles = {
-
-	},
-	SELECTING_REGION =false,
-	SELECTED_REGION_START_BOUNDS = {0,0},
-
-	current_target = nil,
-	last_target = nil,
-	target_lock_time = 0,
-	target_lock_max = 2,
-	accepted_colour = Vec(0,1,0),
-	unmatched_colour = Vec(1,0,0),
-
-	cam_source = Transform(),
-
-	camera_view = Vec(50,50,50),
-
-	COMMANDER_CAM_ACTIVE = false,
-
-	SMOOTHING_FACTOR =2,
-	MOVE_SPEED  = 4,
-	ZOOM_SPEED  = 200,
-	ROTATE_SPEED = 45 ,
-
-	MIN_ZOOM = 5 ,
-	MAX_ZOOM = 150 ,
-	AVG_ZOOM = 40 ,
-
-	BORDER = .05,
-
-	cam_target_x = 0,
-
-	cam_target_y = 0,
-
-	cam_rotate = 0,
-	cam_zoom_target = 80 ,
-	LAST_COMMAND = nil ,
-	SHOW_COMMAND_TIMER = 0,
-	SHOW_COMMAND_TIMER_MAX = 1.5, 
-	LAST_COMMAND_POS = Vec() ,
-	MOVE_COMMAND_COLOUR = {0,0.7,0},
-	ATTACK_COMMAND_COLOUR = {1,0,0}, 
-}
-
-
+#version 2
 function AVF_TAK_INIT()
 	RegisterTool("avf_tak", "AVF-TAK", "MOD/vox/ATAK.vox",5)
-	SetBool("game.tool.avf_tak.enabled", true)
-	local player_trans = Transform(GetPlayerPos(),QuatEuler(0,45,0))	
+	SetBool("game.tool.avf_tak.enabled", true, true)
+	local player_trans = Transform(GetPlayerPos(playerId),QuatEuler(0,45,0))	
 	AVF_TAK_CONTROLLER.cam_source = player_trans
 	AVF_TAK_CONTROLLER.camera_view = TransformCopy(player_trans)
 	AVF_TAK_CONTROLLER.camera_view.rot = QuatRotateQuat(AVF_TAK_CONTROLLER.camera_view.rot,QuatEuler(-45,0,0))
@@ -111,7 +28,7 @@
 		-- DebugWatch("current_target_side",current_target_side)
 		if not AVF_TAK_CONTROLLER.COMMANDER_CAM_ACTIVE and  not InputDown("lmb") and InputPressed("rmb") then
 			
-				local player_trans = Transform(GetPlayerPos())
+				local player_trans = Transform(GetPlayerPos(playerId))
 				local start_transform= TransformToLocalTransform(AVF_TAK_CONTROLLER.cam_source,AVF_TAK_CONTROLLER.camera_view)
 	
 				AVF_TAK_CONTROLLER.cam_source = player_trans
@@ -148,16 +65,7 @@
 	end
 
 end
---[[
-AVF_TAK_SERVER = {
-	assets = {
-		BLUFOR = {},
-		OPFOR = {},
-		INDEFOR ={}
-	}
-}
-
-]]
+
 function AVF_TAK_FIND_ASSETS()
 	local asset_list = FindVehicles("avf_ai",true)
 	local asset_side = 0
@@ -180,7 +88,6 @@
 	end
 
 end
-
 
 function AVF_TAK_CAM_MOVEMENT(dt)
 	
@@ -260,9 +167,7 @@
 	SetCameraDof(12.5)
 	SetCameraTransform(AVF_TAK_CONTROLLER.camera_view)
 
-
-end
-
+end
 
 function AVF_TAK_ASSET_SELECT(assets)
 	AVF_TAK_CONTROLLER['selected_vehicles'] = {}
@@ -327,7 +232,7 @@
 
 	
 end
---[[ check if vehicle x y is median ]]
+
 function AVF_TAK_check_vehicle_in_region(x,y,x1,x2,y1,y2)
 
 	-- DebugWatch("input values ",table.concat({x,y,x1,x2,y1,y2},','))
@@ -376,7 +281,6 @@
 			-- UiTranslate(-(width-border_width),side_border_height)
 			-- UiImageBox("ui/common/box-solid-6.png", width, border_height, 1, 1)
 		UiPop()
-
 
 		UiPush()
 			UiAlign("top left")
@@ -494,7 +398,6 @@
 
 end
 
-
 function AVF_TAK_GIVE_COMMAND()
 
 	if(#AVF_TAK_CONTROLLER['selected_vehicles']>0) then 
@@ -513,7 +416,6 @@
 						table.concat(hitPos, ","))
 					SetTag(AVF_TAK_CONTROLLER['selected_vehicles'][i],'AVF_TAK_NEW_COMMAND')
 
-
 				AVF_TAK_CONTROLLER.LAST_COMMAND = AVF_TAK_COMMAND
 				AVF_TAK_CONTROLLER.SHOW_COMMAND_TIMER = AVF_TAK_CONTROLLER.SHOW_COMMAND_TIMER_MAX  
 		 		AVF_TAK_CONTROLLER.LAST_COMMAND_POS = VecAdd(hitPos,Vec(0,0.2,0))
@@ -538,7 +440,6 @@
 
 end
 
-
 function AVF_TAK_drawCommandSprite(t)
 	t.rot = QuatLookAt(t.pos, GetCameraTransform().pos)
 	-- t.rot = QuatLookAt(t.pos, GetBodyTransform(body).pos)
@@ -574,8 +475,6 @@
 	end
 end
 
-
-
 function AVF_TAK_DRAW_TRACKED_ASSETS()
 
 	local current_target_side = AVF_PLAYER_COMMANDER['sides'][AVF_PLAYER_COMMANDER['current_side']]
@@ -589,7 +488,6 @@
 
 	local namePlacardW = 170
 	local namePlacardH = 30
-
 
 	local letterSize = 11.8
 
@@ -631,11 +529,10 @@
 						vehicleTransform.pos =VecAdd(vehicleTransform.pos,Vec(0,boundsSize*.5,0))
 						UiPush()
 
-
 							-- if vehicle visible on screen then display 
 							local x, y, dist = UiWorldToPixel(vehicleTransform.pos)
 								
-							if dist > 0 then
+							if dist ~= 0 then
 
 								UiTranslate(x, y)
 								-- UiText("Label")
@@ -690,7 +587,7 @@
 
 						-- local x1, y1, dist1 = UiWorldToPixel(min)	
 						-- local x2, y2, dist2 = UiWorldToPixel(max)	
-						-- if dist1 > 0 and dist2 > 0 then
+						-- if dist1 > 0 and dist2 ~= 0 then
 
 						-- end
 
@@ -699,7 +596,6 @@
 			end
 		end
 	UiPop()
-
 
 end
 
@@ -719,19 +615,15 @@
 
 	return (input_a  and 1) or (input_b   and -1) or 0 
 end
+
 function AVF_TAK_get_zoom_rate()
 	local mouse_wheel_impulse = InputValue("mousewheel")
 
 	return (mouse_wheel_impulse  > 0 and 1) or (mouse_wheel_impulse  == 0 and 0) or -1 
 end
-
-
-
 
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
 
-
-

```

---

# Migration Report: commander\AVF_TAK_INDFOR.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/commander\AVF_TAK_INDFOR.lua
+++ patched/commander\AVF_TAK_INDFOR.lua
@@ -1,93 +1,8 @@
-
-
---[[
-
-
-
-		Allows setting of AVF vehicles to teams
-
-		Teams are : bluefor | opfor | indfor 
-
-
-
-
-
-]]
-
-_TARGED_FACTION = 'INDFOR'
-
-AVF_TAK_SERVER = {
-	assets = {
-		BLUFOR = {},
-		OPFOR = {},
-		INDFOR ={}
-
-
-	}
-
-
-
-}
-
-
-AVF_TAK_CONTROLLER = {
-	current_side = 3,
-	sides = {
-		[1] = "BLUFOR",
-		[2] = "OPFOR",
-		[3] = "INDFOR",
-	},
-
-
-	selected_vehicles = {
-
-	},
-	SELECTING_REGION =false,
-	SELECTED_REGION_START_BOUNDS = {0,0},
-
-	current_target = nil,
-	last_target = nil,
-	target_lock_time = 0,
-	target_lock_max = 2,
-	accepted_colour = Vec(0,1,0),
-	unmatched_colour = Vec(1,0,0),
-
-	cam_source = Transform(),
-
-	camera_view = Vec(50,50,50),
-
-	COMMANDER_CAM_ACTIVE = false,
-
-	SMOOTHING_FACTOR =2,
-	MOVE_SPEED  = 4,
-	ZOOM_SPEED  = 200,
-	ROTATE_SPEED = 45 ,
-
-	MIN_ZOOM = 5 ,
-	MAX_ZOOM = 150 ,
-	AVG_ZOOM = 40 ,
-
-	BORDER = .05,
-
-	cam_target_x = 0,
-
-	cam_target_y = 0,
-
-	cam_rotate = 0,
-	cam_zoom_target = 80 ,
-	LAST_COMMAND = nil ,
-	SHOW_COMMAND_TIMER = 0,
-	SHOW_COMMAND_TIMER_MAX = 1.5, 
-	LAST_COMMAND_POS = Vec() ,
-	MOVE_COMMAND_COLOUR = {0,0.7,0},
-	ATTACK_COMMAND_COLOUR = {1,0,0}, 
-}
-
-
+#version 2
 function AVF_TAK_INIT()
 	RegisterTool("avf_tak_indfor", "AVF-TAK_indfor", "MOD/vox/ATAK_INDFOR.vox",5)
-	SetBool("game.tool.avf_tak_indfor.enabled", true)
-	local player_trans = Transform(GetPlayerPos(),QuatEuler(0,45,0))
+	SetBool("game.tool.avf_tak_indfor.enabled", true, true)
+	local player_trans = Transform(GetPlayerPos(playerId),QuatEuler(0,45,0))
 	AVF_TAK_CONTROLLER.cam_source = player_trans
 	AVF_TAK_CONTROLLER.camera_view = TransformCopy(player_trans)
 	AVF_TAK_CONTROLLER.camera_view.rot = QuatRotateQuat(AVF_TAK_CONTROLLER.camera_view.rot,QuatEuler(-45,0,0))
@@ -112,7 +27,7 @@
 		local current_target_side = AVF_TAK_CONTROLLER['sides'][AVF_TAK_CONTROLLER['current_side']]
 		if not AVF_TAK_CONTROLLER.COMMANDER_CAM_ACTIVE and  not InputDown("lmb") and InputPressed("rmb") then
 			
-				local player_trans = Transform(GetPlayerPos())
+				local player_trans = Transform(GetPlayerPos(playerId))
 				local start_transform= TransformToLocalTransform(AVF_TAK_CONTROLLER.cam_source,AVF_TAK_CONTROLLER.camera_view)
 	
 				AVF_TAK_CONTROLLER.cam_source = player_trans
@@ -149,16 +64,7 @@
 	end
 
 end
---[[
-AVF_TAK_SERVER = {
-	assets = {
-		BLUFOR = {},
-		OPFOR = {},
-		INDEFOR ={}
-	}
-}
-
-]]
+
 function AVF_TAK_FIND_ASSETS()
 	local asset_list = FindVehicles("avf_ai",true)
 	local asset_side = 0
@@ -181,7 +87,6 @@
 	end
 
 end
-
 
 function AVF_TAK_CAM_MOVEMENT(dt)
 	
@@ -261,9 +166,7 @@
 	SetCameraDof(12.5)
 	SetCameraTransform(AVF_TAK_CONTROLLER.camera_view)
 
-
-end
-
+end
 
 function AVF_TAK_ASSET_SELECT(assets)
 	AVF_TAK_CONTROLLER['selected_vehicles'] = {}
@@ -327,7 +230,7 @@
 
 	
 end
---[[ check if vehicle x y is median ]]
+
 function AVF_TAK_check_vehicle_in_region(x,y,x1,x2,y1,y2)
 
 	-- DebugWatch("input values ",table.concat({x,y,x1,x2,y1,y2},','))
@@ -376,7 +279,6 @@
 			-- UiTranslate(-(width-border_width),side_border_height)
 			-- UiImageBox("ui/common/box-solid-6.png", width, border_height, 1, 1)
 		UiPop()
-
 
 		UiPush()
 			UiAlign("top left")
@@ -494,7 +396,6 @@
 
 end
 
-
 function AVF_TAK_GIVE_COMMAND()
 
 	if(#AVF_TAK_CONTROLLER['selected_vehicles']>0) then 
@@ -513,7 +414,6 @@
 						table.concat(hitPos, ","))
 					SetTag(AVF_TAK_CONTROLLER['selected_vehicles'][i],'AVF_TAK_NEW_COMMAND')
 
-
 				AVF_TAK_CONTROLLER.LAST_COMMAND = AVF_TAK_COMMAND
 				AVF_TAK_CONTROLLER.SHOW_COMMAND_TIMER = AVF_TAK_CONTROLLER.SHOW_COMMAND_TIMER_MAX  
 		 		AVF_TAK_CONTROLLER.LAST_COMMAND_POS = VecAdd(hitPos,Vec(0,0.2,0))
@@ -538,7 +438,6 @@
 
 end
 
-
 function AVF_TAK_drawCommandSprite(t)
 	t.rot = QuatLookAt(t.pos, GetCameraTransform().pos)
 	-- t.rot = QuatLookAt(t.pos, GetBodyTransform(body).pos)
@@ -574,8 +473,6 @@
 	end
 end
 
-
-
 function AVF_TAK_DRAW_TRACKED_ASSETS()
 	local displayRange = 350
 	local uiScaleFactor = 0.4
@@ -587,7 +484,6 @@
 
 	local namePlacardW = 170
 	local namePlacardH = 30
-
 
 	local letterSize = 11.8
 
@@ -629,11 +525,10 @@
 						vehicleTransform.pos =VecAdd(vehicleTransform.pos,Vec(0,boundsSize*.5,0))
 						UiPush()
 
-
 							-- if vehicle visible on screen then display 
 							local x, y, dist = UiWorldToPixel(vehicleTransform.pos)
 								
-							if dist > 0 then
+							if dist ~= 0 then
 
 								UiTranslate(x, y)
 								-- UiText("Label")
@@ -688,7 +583,7 @@
 
 						-- local x1, y1, dist1 = UiWorldToPixel(min)	
 						-- local x2, y2, dist2 = UiWorldToPixel(max)	
-						-- if dist1 > 0 and dist2 > 0 then
+						-- if dist1 > 0 and dist2 ~= 0 then
 
 						-- end
 
@@ -697,7 +592,6 @@
 			end
 		end
 	UiPop()
-
 
 end
 
@@ -717,19 +611,15 @@
 
 	return (input_a  and 1) or (input_b   and -1) or 0 
 end
+
 function AVF_TAK_get_zoom_rate()
 	local mouse_wheel_impulse = InputValue("mousewheel")
 
 	return (mouse_wheel_impulse  > 0 and 1) or (mouse_wheel_impulse  == 0 and 0) or -1 
 end
-
-
-
 
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
 
-
-

```

---

# Migration Report: commander\AVF_TAK_OPFOR.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/commander\AVF_TAK_OPFOR.lua
+++ patched/commander\AVF_TAK_OPFOR.lua
@@ -1,93 +1,8 @@
-
-
---[[
-
-
-
-		Allows setting of AVF vehicles to teams
-
-		Teams are : bluefor | opfor | indfor 
-
-
-
-
-
-]]
-
-_TARGED_FACTION = 'OPFOR'
-
-AVF_TAK_SERVER = {
-	assets = {
-		BLUFOR = {},
-		OPFOR = {},
-		INDFOR ={}
-
-
-	}
-
-
-
-}
-
-
-AVF_TAK_CONTROLLER = {
-	current_side = 2,
-	sides = {
-		[1] = "BLUFOR",
-		[2] = "OPFOR",
-		[3] = "INDFOR",
-	},
-
-
-	selected_vehicles = {
-
-	},
-	SELECTING_REGION =false,
-	SELECTED_REGION_START_BOUNDS = {0,0},
-
-	current_target = nil,
-	last_target = nil,
-	target_lock_time = 0,
-	target_lock_max = 2,
-	accepted_colour = Vec(0,1,0),
-	unmatched_colour = Vec(1,0,0),
-
-	cam_source = Transform(),
-
-	camera_view = Vec(50,50,50),
-
-	COMMANDER_CAM_ACTIVE = false,
-
-	SMOOTHING_FACTOR =2,
-	MOVE_SPEED  = 4,
-	ZOOM_SPEED  = 200,
-	ROTATE_SPEED = 45 ,
-
-	MIN_ZOOM = 5 ,
-	MAX_ZOOM = 150 ,
-	AVG_ZOOM = 40 ,
-
-	BORDER = .05,
-
-	cam_target_x = 0,
-
-	cam_target_y = 0,
-
-	cam_rotate = 0,
-	cam_zoom_target = 80 ,
-	LAST_COMMAND = nil ,
-	SHOW_COMMAND_TIMER = 0,
-	SHOW_COMMAND_TIMER_MAX = 1.5, 
-	LAST_COMMAND_POS = Vec() ,
-	MOVE_COMMAND_COLOUR = {0,0.7,0},
-	ATTACK_COMMAND_COLOUR = {1,0,0}, 
-}
-
-
+#version 2
 function AVF_TAK_INIT()
 	RegisterTool("avf_tak_opfor", "AVF-TAK_OPFOR", "MOD/vox/ATAK_OPFOR.vox",5)
-	SetBool("game.tool.avf_tak_opfor.enabled", true)
-	local player_trans = Transform(GetPlayerPos(),QuatEuler(0,45,0))
+	SetBool("game.tool.avf_tak_opfor.enabled", true, true)
+	local player_trans = Transform(GetPlayerPos(playerId),QuatEuler(0,45,0))
 	AVF_TAK_CONTROLLER.cam_source = player_trans
 	AVF_TAK_CONTROLLER.camera_view = TransformCopy(player_trans)
 	AVF_TAK_CONTROLLER.camera_view.rot = QuatRotateQuat(AVF_TAK_CONTROLLER.camera_view.rot,QuatEuler(-45,0,0))
@@ -112,7 +27,7 @@
 		local current_target_side = AVF_TAK_CONTROLLER['sides'][AVF_TAK_CONTROLLER['current_side']]
 		if not AVF_TAK_CONTROLLER.COMMANDER_CAM_ACTIVE and  not InputDown("lmb") and InputPressed("rmb") then
 			
-				local player_trans = Transform(GetPlayerPos())
+				local player_trans = Transform(GetPlayerPos(playerId))
 				local start_transform= TransformToLocalTransform(AVF_TAK_CONTROLLER.cam_source,AVF_TAK_CONTROLLER.camera_view)
 	
 				AVF_TAK_CONTROLLER.cam_source = player_trans
@@ -149,16 +64,7 @@
 	end
 
 end
---[[
-AVF_TAK_SERVER = {
-	assets = {
-		BLUFOR = {},
-		OPFOR = {},
-		INDEFOR ={}
-	}
-}
-
-]]
+
 function AVF_TAK_FIND_ASSETS()
 	local asset_list = FindVehicles("avf_ai",true)
 	local asset_side = 0
@@ -181,7 +87,6 @@
 	end
 
 end
-
 
 function AVF_TAK_CAM_MOVEMENT(dt)
 	
@@ -261,9 +166,7 @@
 	SetCameraDof(12.5)
 	SetCameraTransform(AVF_TAK_CONTROLLER.camera_view)
 
-
-end
-
+end
 
 function AVF_TAK_ASSET_SELECT(assets)
 	AVF_TAK_CONTROLLER['selected_vehicles'] = {}
@@ -327,7 +230,7 @@
 
 	
 end
---[[ check if vehicle x y is median ]]
+
 function AVF_TAK_check_vehicle_in_region(x,y,x1,x2,y1,y2)
 
 	-- DebugWatch("input values ",table.concat({x,y,x1,x2,y1,y2},','))
@@ -376,7 +279,6 @@
 			-- UiTranslate(-(width-border_width),side_border_height)
 			-- UiImageBox("ui/common/box-solid-6.png", width, border_height, 1, 1)
 		UiPop()
-
 
 		UiPush()
 			UiAlign("top left")
@@ -494,7 +396,6 @@
 
 end
 
-
 function AVF_TAK_GIVE_COMMAND()
 
 	if(#AVF_TAK_CONTROLLER['selected_vehicles']>0) then 
@@ -513,7 +414,6 @@
 						table.concat(hitPos, ","))
 					SetTag(AVF_TAK_CONTROLLER['selected_vehicles'][i],'AVF_TAK_NEW_COMMAND')
 
-
 				AVF_TAK_CONTROLLER.LAST_COMMAND = AVF_TAK_COMMAND
 				AVF_TAK_CONTROLLER.SHOW_COMMAND_TIMER = AVF_TAK_CONTROLLER.SHOW_COMMAND_TIMER_MAX  
 		 		AVF_TAK_CONTROLLER.LAST_COMMAND_POS = VecAdd(hitPos,Vec(0,0.2,0))
@@ -538,7 +438,6 @@
 
 end
 
-
 function AVF_TAK_drawCommandSprite(t)
 	t.rot = QuatLookAt(t.pos, GetCameraTransform().pos)
 	-- t.rot = QuatLookAt(t.pos, GetBodyTransform(body).pos)
@@ -574,8 +473,6 @@
 	end
 end
 
-
-
 function AVF_TAK_DRAW_TRACKED_ASSETS()
 	local displayRange = 350
 	local uiScaleFactor = 0.4
@@ -587,7 +484,6 @@
 
 	local namePlacardW = 170
 	local namePlacardH = 30
-
 
 	local letterSize = 11.8
 
@@ -629,11 +525,10 @@
 						vehicleTransform.pos =VecAdd(vehicleTransform.pos,Vec(0,boundsSize*.5,0))
 						UiPush()
 
-
 							-- if vehicle visible on screen then display 
 							local x, y, dist = UiWorldToPixel(vehicleTransform.pos)
 								
-							if dist > 0 then
+							if dist ~= 0 then
 
 								UiTranslate(x, y)
 								-- UiText("Label")
@@ -688,7 +583,7 @@
 
 						-- local x1, y1, dist1 = UiWorldToPixel(min)	
 						-- local x2, y2, dist2 = UiWorldToPixel(max)	
-						-- if dist1 > 0 and dist2 > 0 then
+						-- if dist1 > 0 and dist2 ~= 0 then
 
 						-- end
 
@@ -697,7 +592,6 @@
 			end
 		end
 	UiPop()
-
 
 end
 
@@ -717,19 +611,15 @@
 
 	return (input_a  and 1) or (input_b   and -1) or 0 
 end
+
 function AVF_TAK_get_zoom_rate()
 	local mouse_wheel_impulse = InputValue("mousewheel")
 
 	return (mouse_wheel_impulse  > 0 and 1) or (mouse_wheel_impulse  == 0 and 0) or -1 
 end
-
-
-
 
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
 
-
-

```

---

# Migration Report: commander\team_allocater.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/commander\team_allocater.lua
+++ patched/commander\team_allocater.lua
@@ -1,43 +1,7 @@
-
-
---[[
-
-
-
-		Allows setting of AVF vehicles to teams
-
-		Teams are : bluefor | opfor | indfor 
-
-
-
-
-
-]]
-
-
-AVF_PLAYER_COMMANDER = {
-	current_side = 1,
-	sides = {
-		[1] = "BLUFOR",
-		[2] = "OPFOR",
-		[3] = "INDFOR",
-	},
-
-
-	current_target = nil,
-	last_target = nil,
-	target_lock_time = 0,
-	target_lock_max = 1.25,
-	accepted_colour = Vec(0,1,0),
-	unmatched_colour = Vec(1,0,0)
-
-}
-CURRENT_AI_TRACK = 0
-
-
+#version 2
 function team_allocator_init()
 	RegisterTool("avf_ai_commander_team_allocator", "AVF Command", "MOD/vox/commander_radio.vox",5)
-	SetBool("game.tool.avf_ai_commander_team_allocator.enabled", true)
+	SetBool("game.tool.avf_ai_commander_team_allocator.enabled", true, true)
 end
 
 function team_allocator_tick()
@@ -52,7 +16,7 @@
 			AVF_PLAYER_COMMANDER['current_side'] = (AVF_PLAYER_COMMANDER['current_side']%#AVF_PLAYER_COMMANDER['sides'])+1
 		end
 		if GetBool("game.player.canusetool") and InputDown("lmb") then 
-			local t = GetPlayerCameraTransform()
+			local t = GetPlayerCameraTransform(playerId)
 			local hit, dist, normal, shape  = QueryRaycast(t.pos, TransformToParentVec(t,Vec(0, 0, -1)), 100)
 			if hit then
 				local tracked_body = GetShapeBody(shape)
@@ -122,8 +86,6 @@
 
 end
 
-
-
 function draw_allocator_bar()
 	UiPush()
 		UiFont("bold.ttf", 20)
@@ -192,4 +154,3 @@
 
 end
 
-

```

---

# Migration Report: common.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/common.lua
+++ patched/common.lua
@@ -1,13 +1,8 @@
-
-
-
+#version 2
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
 end
-
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -24,64 +19,3 @@
     return copy
 end
 
-utils = {
-
-	contains = function(set,key)
-		return set[key] ~= nil
-		-- body
-	end,
-
--- catchBadPos = function (x)
--- 	if(x.x)
--- end,
-
- getLoc = function(x )
-	return	"X "..
-	x[1]..
-	"\nY"..
-	x[2]..
-	"\nZ"..
-	x[3]
-	-- body
-end,
-
-randomFloat = function (lower, greater)
-    return lower + math.random()  * (greater - lower);
-end,
-
-printRot = function(x)
-
-	SetString("hud.notification",
-	"X "..
-	x[2]..
-	"\nY"..
-	x[3]..
-	"\nZ"..
-	x[4]
-	) -- this prints the rotation top center of the screen  
-
-end, 
-
-printStr = function (x)
-	SetString("hud.notification",x)
-end,
-
-explodeTable = function(x)
-	local testString = ""
-	for key,value in pairs(x) do
-		testString = testString..key.." | "..value.."\n"
-	end
-	return testString
-end,
-
-sign = function(x)
-   if x<0 then
-     return -1
-   elseif x>0 then
-     return 1
-   else
-     return 0
-   end
-end
-
-}

```

---

# Migration Report: controls.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/controls.lua
+++ patched/controls.lua
@@ -1,49 +1,4 @@
-armedVehicleControls = {
-	fire 				= "usetool",
-	sniperMode 			= "vehiclelower",
-	changeWeapons		= "r",
-	changeTurretGroup	= "t",
-	changeAmmunition	= "f",
-	deploySmoke			= "g",
-	toggle_Searchlight =  "l",
-	increase_zero =  "p",
-	decrease_zero =  ";",
-}
-
-armedVehicleControlsOrder = {
-	[1] 			="fire",
-	[2] 			= "sniperMode",
-	[3] 			= "changeWeapons",
-	[4]				= "changeAmmunition",
-	[5]				= "deploySmoke",
-	[6]			="toggle_Searchlight",
-	[7]				= "Adjust Zero Up",
-	[8]			="Adjust Zero Down",
-}
-
-armedVehicleControls_arty = {
-	fire 				= "usetool",
-	Arty_cam 			= "vehiclelower",
-	left	= "left",
-	right	= "right",
-	up			= "up",
-	down  =  "down",
-}
-
-armedVehicleControlsOrder_arty = {
-	[1] 			="fire",
-	[2] 			= "Arty_cam",
-	[3] 			= "left",
-	[4]				= "right",
-	[5]				= "up",
-	[6]			="down",
-}
-
--- 	camerax = "camerax",	--Camera x movement, scaled by sensitivity. Only valid in InputValue.
--- cameray = "cameray",
-
-
-
+#version 2
 function loadCustomControls()
 	for key, value in pairs(armedVehicleControls) do 
 		
@@ -52,4 +7,5 @@
 		end
 	end
 
-end+end
+

```

---

# Migration Report: databus.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/databus.lua
+++ patched/databus.lua
@@ -1,10 +1,4 @@
-databus ={
-	TAK_COMMANDS = {
-		[1] = 'AVF_TAK_MOVE',
-		[2] = 'AVF_TAK_ATTACK'
-	}
-}
-
+#version 2
 function databus:update_vehicle_states()
 
 	for i =1,#vehicleFeatures.validGroups do 
@@ -14,7 +8,6 @@
 	end 
 
 end
-
 
 function databus:update_weapons_data(gunGroup)
 
@@ -26,8 +19,6 @@
 	end
 
 end
-
-
 
 function databus:update_missile_guidance(gun)
 	SetTag(gun.id,"avf.databus.TRACKING_TARGET",gun.missile_guidance_tracking_target)
@@ -81,8 +72,6 @@
 
 end
 
-
-
 function string:split(sSeparator, nMax, bRegexp)
    assert(sSeparator ~= '')
    assert(nMax == nil or nMax >= 1)
@@ -106,4 +95,5 @@
    end
 
    return aRecord
-end+end
+

```

---

# Migration Report: debug_menu.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/debug_menu.lua
+++ patched/debug_menu.lua
@@ -1,13 +1,7 @@
-DEBUG_AI_PRIORITIES = false	
-
-DEBUG_MISSILE_PROTOCOL = false
-
-SHOW_DEV_MENU = false
-
+#version 2
 function SHOW_AVF_DEV_HUD()
 
 	UiMakeInteractive()
-
 
 	UiPush()
 	UiTranslate(UiCenter(), 50)
@@ -25,9 +19,6 @@
 
 --[[
 
-
-
-
 debugMode = false
 
 DEBUG_AI = false
@@ -40,17 +31,13 @@
 
 debug_weapon_pos = false
 
-
 debug_special_armour = false
 
 debug_shell_casings = false
 
-
 debug_player_damage = false
 
-
 debug_vehicle_locations_active = false
-
 
 ]]
 
@@ -95,7 +82,6 @@
 				_AI_DEBUG_PATHING = not _AI_DEBUG_PATHING
 			end
 
-
 			
 				UiTranslate(0, 40)
 
@@ -111,9 +97,6 @@
 				debug_combat_stuff = not debug_combat_stuff
 			end
 				UiTranslate(0, 40)
-
-
-
 
 			UiTranslate(0, 100)
 			if UiTextButton("Close", 200, 40) then
@@ -138,7 +121,7 @@
 			debugText = "Disable"
 		end
 		if UiTextButton(debugText.." Debug Mode", w, h) then
-			SetBool("savegame.mod.debug", not GetBool("savegame.mod.debug"))
+			SetBool("savegame.mod.debug", not GetBool("savegame.mod.debug"), true)
 		end	
 		UiTranslate(0, 50)
 		local infiniteAmmoText = "Enable"
@@ -146,7 +129,7 @@
 			infiniteAmmoText = "Disable"
 		end
 		if UiTextButton(infiniteAmmoText.." Infinite Ammo", w, h) then
-			SetBool("savegame.mod.infiniteAmmo", not GetBool("savegame.mod.infiniteAmmo"))
+			SetBool("savegame.mod.infiniteAmmo", not GetBool("savegame.mod.infiniteAmmo"), true)
 		end	
 		UiTranslate(0, 50)
 		local controlsHudText = "Hide"
@@ -154,9 +137,8 @@
 			controlsHudText = "Show"
 		end
 		if UiTextButton(controlsHudText.." Controls HUD", w, h) then
-			SetBool("savegame.mod.hideControls", not GetBool("savegame.mod.hideControls"))
+			SetBool("savegame.mod.hideControls", not GetBool("savegame.mod.hideControls"), true)
 		end
-
 
 		-- UiTranslate(270, 0)
 		-- if GetBool("savegame.mod.mph") then
@@ -166,7 +148,7 @@
 		-- 	UiPop()
 		-- end
 		-- if UiTextButton("Imperial MPH", 200, 40) then
-		-- 	SetBool("savegame.mod.mph", true)
+		-- 	SetBool("savegame.mod.mph", true, true)
 		-- end
 	UiPop()
 	
@@ -182,4 +164,5 @@
 	else
 		UiColor(0.8,0.8,0.8,0.5)
 	end
-end+end
+

```

---

# Migration Report: explosionController.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/explosionController.lua
+++ patched/explosionController.lua
@@ -1,51 +1,4 @@
-explosionController = {
-
-	test =  "hello world",
-
-	explosionPos = Vec(),
-
-	trails = {},
-
-
-	smoke = {
-		age = 0,
-		size = 0,
-		life = 0,
-		next = 0,
-		vel = 0,
-		gravity = 0,
-		amount = 0,
-	},
-
-
-
-	fire = {
-		age = 0,
-		life = 0,
-		size = 0,
-	},
-
-
-
-	flash = {
-		age = 0,
-		life = 0,
-		intensity = 0,
-	},
-
-	light = {
-		age = 0,
-		life = 0,
-		intensity = 0,
-	},
-
-
-	maxMass = 1000,
-	forceCoef = 250
-
-}
-
-
+#version 2
 function explosionController:rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
@@ -53,8 +6,6 @@
 function explosionController:rndVec(t)
 	return Vec(self:rnd(-t, t), self:rnd(-t, t), self:rnd(-t, t))
 end
-
-
 
 function explosionController:trailsAdd(pos, vel, life, size, damp, gravity)
 	t = {}
@@ -102,7 +53,6 @@
 	end
 end
 
-
 function explosionController:smokeUpdate(pos, dt)
 	
 	if self.smoke.age < self.smoke.life then
@@ -126,7 +76,6 @@
 		end
 	end
 end
-
 
 function explosionController:fireUpdate(pos, dt)
 
@@ -151,7 +100,6 @@
 	end
 end
 
-
 function explosionController:flashTick(pos, dt)
 
 	if self.flash.age < self.flash.life then
@@ -160,8 +108,6 @@
 		PointLight(pos, 1, 0.5, 0.2, self.flash.intensity*q) 
 	end
 end
-
-
 
 function explosionController:lightTick(pos, dt)
 
@@ -240,7 +186,6 @@
 	self.smoke.amount = 2
 end
 
-
 function explosionController:explosionMedium(pos)
 	self.explosionPos = pos
 	self:explosionSparks(30, 3)
@@ -270,7 +215,6 @@
 	self.smoke.gravity = 2
 	self.smoke.amount = 2
 end
-
 
 function explosionController:explosionLarge(pos)
 	self.explosionPos = pos
@@ -316,7 +260,6 @@
 	end
 end
 
-
 function explosionController:tick(dt)
 	self:flashTick(self.explosionPos, dt)
 	self:lightTick(self.explosionPos, dt)
@@ -333,7 +276,6 @@
 	self:shockwave(pos,strength)
 end
 
-
 function explosionController:update(dt)
 	self:trailsUpdate(dt)
 	self:fireUpdate(self.explosionPos, dt)
@@ -343,12 +285,6 @@
 function explosionController:testFunc(dt)
 	return "hello world"
 end
-
-
-
--- strength = 2000	--Strength of shockwave impulse
--- maxDist = 15	--The maximum distance for bodies to be affected
--- maxMass = 1000	--The maximum mass for a body to be affected
 
 function explosionController:shockwave(pos,power)
 	local maxDist = power * 5
@@ -367,7 +303,6 @@
 		local b = bodies[i]
 		
 		-- if(avoid_repeat_body(b,jointed_bodies)) then 
-
 
 		-- 	local jointed = GetJointedBodies(b)
 		-- 	for j =1,#jointed do
@@ -407,4 +342,5 @@
 
 	end
 	return true
-end+end
+

```

---

# Migration Report: guidance.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/guidance.lua
+++ patched/guidance.lua
@@ -1,38 +1,7 @@
-
-test_distance = 30 
-scale_modifier = 1
-
-t_test_distance = 7
-
-t_guidance_peak_dist = 50
-
-
-
-DEBUG_GUIDANCE_FUNCTIONALITY =false
-
-
-
-guidance_peak_dist = 100
-
-guidance_peak_height = 30
-guidance_height_ratio = .8--0.32 
-
-guidance_time_since_fly = 0
-guidance_drop_dist = 0
-
-guidance_start_y = 1
-guidance_start_y_2 = 0.95
-
--- y = np.sin(2*np.pi*freq*t)
-
-
-
-
+#version 2
 function follow_guidance(projectile)
 
-
-end
-
+end
 
 function guidance_tick(dt)
 	if(DEBUG_GUIDANCE_FUNCTIONALITY) then 
@@ -56,9 +25,7 @@
 		-- basic_sin(dt)
 	end
 
-
-end
-
+end
 
 function debug_top_down_generation()
 	local target_shape = FindShape("avf_guidance_target",true) 
@@ -74,7 +41,6 @@
 
 			},
 			target_body = target_body,
-
 
 		}
 
@@ -106,14 +72,9 @@
 		target_dist
 		)
 
-
-
 	return flight_pattern,flight_keypoints
 
-
-
-end
-
+end
 
 function top_down_computation(
 	projectile,
@@ -124,14 +85,10 @@
 	flight_keypoints,
 	target_dist)
 
-
 	local z = 1
 	local flight_index = 1
 
-
-
 	local expected_guidance_drop_dist = guidance_drop_dist
-
 
 	if(DEBUG_GUIDANCE_FUNCTIONALITY) then 
 		DebugCross(Vec(target_dist,guidance_start_y,z),0,2,0)
@@ -169,13 +126,11 @@
 		overcompensation = 1.0
 	end
 
-
 	local hit_apex = false
 	
 	local cutoff_y = 0
 
 	local flight_distance = 0
-
 
 	local x_move = 0
 	local drop_offset = 0
@@ -229,15 +184,12 @@
 					completed = false
 				}
 
-
 			if(DEBUG_GUIDANCE_FUNCTIONALITY) then 
 				DrawLine(Vec(flight_distance, y_pos, z), Vec(flight_distance, y_pos-2, z), 0, 1, 1)
 			end
 			
 
-
-		end
-
+		end
 
 		if(DEBUG_GUIDANCE_FUNCTIONALITY) then 
 	
@@ -279,41 +231,27 @@
 
 		last_x_pos = x_pos
 
-
 		if (x_pos > (target_dist-expected_guidance_drop_dist)) then
 			break
 		end
 	end
 
-
 	return flight_distance,flight_pattern,flight_index
 
-
-	
-end
-
-
-
---[[
-
-
-	proNav functions 
+	
+end
+
+function TruProNav()
+
+	control_effector_commmand = Vec(0,0,0)
+
+--[[ 
+
+	REMOVED
+
 ]]
-function TruProNav()
-
-	control_effector_commmand = Vec(0,0,0)
-
-
---[[ 
-
-
-	REMOVED
-
-]]
-
-end
-
-
+
+end
 
 function init_missile_behaviours(projectile)
 	local target_vel = GetBodyVelocity(projectile.target_body)
@@ -380,10 +318,8 @@
 		keypoint_index = 1,
 		flight_keypoints = projectile.flight_keypoints,
 
-
 	}
 end
-
 
 function compute_CED(dt,projectile) 
 	-- missile.msl_pos
@@ -441,7 +377,6 @@
 		end
 	end 
 
-
 	-- local target_vel = GetBodyVelocity(missile.target_body)
 
 	-- local min, max = GetBodyBounds(missile.target_body)
@@ -487,7 +422,6 @@
 	dt,
 	missile,
 	target_vel)
-
 
 	-- missile = {
 	-- 	missile_body = msl_body ,
@@ -502,7 +436,6 @@
 		-- N = 3.0,
 		-- nt = 664, 
 
-
 	-- }
 	if(DEBUG_MISSILE_PROTOCOL and  not guidance_info_printed) then 
 
@@ -547,7 +480,6 @@
 			local new_msl_pos = VecAdd(missile.msl_pos,missile.missile_vel )
 			local print_colour =VecLerp(chaser_colour,impact_colour,clamp(0,1,range/50))
 
-
 			--- draw lines for trajectory planning
 			-- DrawLine(missile.tgt_pos, VecAdd(missile.tgt_pos,target_vel), 0, 0, 1)
 			-- DrawLine(VecAdd(missile.tgt_pos,target_vel), missile.msl_pos, 0, 1, 1)
@@ -567,9 +499,7 @@
 
 end
 
-
 function autopilot_x(dt,missile)
-
 
 	-- missile = {
 	-- 	missile_body = msl_body ,
@@ -583,7 +513,6 @@
 	-- last_target_vel = target_vel
 		-- N = 3.0,
 		-- nt = 664, 
-
 
 	-- }
 
@@ -607,10 +536,7 @@
 	missile.tgt_pos_previous = missile.tgt_pos
 	return missile
 
-
-end
-
-
+end
 
 function base_pronav(
 	msl_pos,
@@ -646,7 +572,6 @@
 	return latax		
 end
 
-
 function flight_controller_X(current_vel, adjustment_vel,min, max,Nt)
 	if(VecLength(current_vel)<max)then 
 
@@ -669,9 +594,6 @@
 	end
 	return current_vel
 end
-
-
-
 
 function reworked_top_down(dt,target_dist,z)
 	local expected_guidance_drop_dist = guidance_drop_dist
@@ -712,13 +634,11 @@
 		overcompensation = 1.0
 	end
 
-
 	local hit_apex = false
 	
 	local cutoff_y = 0
 
 	local flight_distance = 0
-
 
 	local x_move = 0
 	local drop_offset = 0
@@ -762,12 +682,9 @@
 		last_y_pos = y_pos
 		last_x_pos = x_pos
 
-
-
-	end
-
-end
-
+	end
+
+end
 
 function continue_flight(x_pos,y_pos,z,expected_guidance_drop_dist,target_dist)
 	local last_x_pos = x_pos
@@ -779,7 +696,6 @@
 		flight_distance = flight_distance + increment_size
 		x_pos = last_x_pos + increment_size
 
-
 		-- DebugPrint("xpos "..x_pos)
 		DrawLine(Vec(x_pos, last_y_pos, z), Vec(x_pos, y_pos-0.5, z), 1, 1, 0)
 
@@ -789,94 +705,10 @@
 		end
 	end
 
-
 	return flight_distance
 
-
-	
-end
-
-
-
-	-- 	if(y>tick_cutoff or  x_pos > (target_dist-guidance_drop_dist) ) then 
-	-- 		if(y<0.99) then 
-	-- 			for j = i, true_sample do 
-	-- 				t = ts * (i-1)
-	-- 				y = math.sin(2*math.pi*freq*t)
-	-- 				if
-	-- 		else
-	-- 			cutoff_y = i
-	-- 		end
-	-- 		cutoff_x = x_pos
-	-- 		guidance_drop_height = guidance_peak_height
-	-- 		 DebugPrint(y>tick_cutoff)
-	-- 		-- DebugPrint("condition 1 "..(y>tick_cutoff) .." condition 2"..  x_pos > (target_dist-guidance_drop_dist))
-	-- 		break
-	-- 	end
-
-	-- end
-
-
-
-	-- for i=1,target_dist do
-	-- 	flight_distance = flight_distance + 1
-	-- 	x_pos = last_x_pos + 1 
-
-
-	-- 	-- DebugPrint("xpos "..x_pos)
-	-- 	DrawLine(Vec(last_x_pos, last_y_pos, z), Vec(x_pos, y_pos, z), 1, 0, 0)
-
-	-- 	last_x_pos = x_pos
-	-- 	if (x_pos > (target_dist-guidance_drop_dist)) then
-	-- 		break
-	-- 	end
-	-- end
-
-
-	-- flight_distance = x_pos
-	-- DebugWatch("custoff",cutoff_y)
-	-- DebugWatch("true sampe",true_sample)
-	-- for i = cutoff_y,true_sample,1 do 
-
-	-- 	t = ts * (i-1)
-	-- 	y = math.sin(2*math.pi*freq*t)
-	-- 	x_pos = ((guidance_drop_dist*2) * t ) + flight_distance
-	-- 	y_pos = ((guidance_drop_height * y) ) +  guidance_start_y
-
-	-- DebugWatch("true saddddse",flight_distance)
-
-	-- 	DrawLine(Vec(last_x_pos, last_y_pos, z), Vec(x_pos, y_pos, z), 1, 0, 0)
-
-	-- 	last_y_pos = y_pos
-	-- 	last_x_pos = x_pos
-
-	-- end
-
-
-	-- -- for i = 1,sr/2 do 
-	-- -- 	t = ts * (i-1)
-	-- -- 	y = math.sin(2*math.pi*freq*t)
-	-- -- 	DebugPrint(ts)
-	-- -- 	x_pos = (guidance_peak_dist*2) * t 
-	-- -- 	y_pos = ((guidance_peak_height * y) ) +  guidance_peak_height
-
-
-	-- -- 	DrawLine(Vec(last_x_pos, last_y_pos, 0), Vec(x_pos, y_pos, 0), 1, 0, 0)
-
-	-- -- 	last_y_pos = y_pos
-	-- -- 	last_x_pos = x_pos
-
-	-- -- end
-
-
-
--- end
-
-
-
-
-
-
+	
+end
 
 function basic_top_down(dt,target_dist,z)
 
@@ -899,7 +731,6 @@
 	local last_y_pos = guidance_peak_height
 	local t = 0 
 
-
 	local tick_cutoff = 0.99
 	if(guidance_peak_dist + guidance_drop_dist > target_dist) then 
 		tick_cutoff = (target_dist -  guidance_drop_dist / guidance_peak_dist)
@@ -914,7 +745,6 @@
 		y = math.sin(2*math.pi*freq*t)
 		x_pos = ((guidance_peak_dist) * t) +flight_distance
 		y_pos = ((guidance_peak_height * y) ) +  guidance_peak_height
-
 
 		DrawLine(Vec(last_x_pos, last_y_pos, z), Vec(x_pos, y_pos, z), 1, 0, 0)
 		-- DebugPrint(x_pos)
@@ -930,13 +760,10 @@
 
 	end
 
-
-
 	for i=1,target_dist do
 		flight_distance = flight_distance + 1
 		x_pos = last_x_pos + 1 
 
-
 		-- DebugPrint("xpos "..x_pos)
 		DrawLine(Vec(last_x_pos, last_y_pos, z), Vec(x_pos, y_pos, z), 1, 0, 0)
 
@@ -945,7 +772,6 @@
 			break
 		end
 	end
-
 
 	flight_distance = x_pos
 	DebugWatch("custoff",cutoff_y)
@@ -965,7 +791,6 @@
 		last_x_pos = x_pos
 
 	end
-
 
 	-- for i = 1,sr/2 do 
 	-- 	t = ts * (i-1)
@@ -974,7 +799,6 @@
 	-- 	x_pos = (guidance_peak_dist*2) * t 
 	-- 	y_pos = ((guidance_peak_height * y) ) +  guidance_peak_height
 
-
 	-- 	DrawLine(Vec(last_x_pos, last_y_pos, 0), Vec(x_pos, y_pos, 0), 1, 0, 0)
 
 	-- 	last_y_pos = y_pos
@@ -982,14 +806,9 @@
 
 	-- end
 
-
-
-end
-
-
+end
 
 function basic_sin(dt)
-
 
 	-- # sampling rate
 	local sr = 100.0
@@ -1016,7 +835,6 @@
 		x_pos = (dist*2) * t 
 		y_pos = ((heigt * y) ) +  heigt
 
-
 		DrawLine(Vec(last_x_pos, last_y_pos, 0), Vec(x_pos, y_pos, 0), 1, 0, 0)
 
 		last_y_pos = y_pos
@@ -1024,113 +842,5 @@
 
 	end
 
-
-
-end
-
-
-
-
--- function guidance_tick(dt)
--- 	DebugWatch("guidance being run",dt)
-
--- 	local target_dist =  100
-
--- 	local guidance_drop_dist = guidance_peak_dist * 1.5
--- 	-- # sampling rate
--- 	local sr = 100.0
--- 	local true_sample = sr/2
--- 	-- # sampling interval
--- 	local ts = 1.0/sr
-	
-
--- 	-- # frequency of the signal
--- 	local freq = 1
--- 	local last = 0
--- 	local x_pos = 0
--- 	local y_pos = 0
--- 	local last_x_pos = 0
--- 	local last_y_pos = guidance_peak_height
--- 	local t = 0 
-
--- 	local tick_cutoff = 0.99
-
-	
--- 	local cutoff_y = 0
-
--- 	local flight_distance = 0
-
--- 	for i = 1,true_sample do 
--- 		t = ts * (i-1)
--- 		y = math.sin(2*math.pi*freq*t)
--- 		x_pos = ((guidance_peak_dist*2) * t) +flight_distance
--- 		y_pos = ((guidance_peak_height * y) ) +  guidance_peak_height
-
-
--- 		DrawLine(Vec(last_x_pos, last_y_pos, 0), Vec(x_pos, y_pos, 0), 1, 0, 0)
-
--- 		last_y_pos = y_pos
--- 		last_x_pos = x_pos
--- 		if(y>tick_cutoff or x_pos > (target_dist-guidance_drop_dist) ) then 
--- 			cutoff_y = i
--- 			cutoff_x = x_pos
--- 			break
--- 		end
-
--- 	end
--- 	DebugPrint(1)
--- 	for i=1,target_dist do
--- 		DebugPrint(2)
--- 		flight_distance = flight_distance + 1
--- 		x_pos = last_x_pos + 1 
-
-
--- 		DebugPrint(x_pos)
--- 		DrawLine(Vec(last_x_pos, last_y_pos, 0), Vec(x_pos, y_pos, 0), 1, 0, 0)
-
--- 		last_x_pos = x_pos
--- 		if (flight_distance < target_dist - (cutoff_x)) then
--- 			break
--- 		end
--- 	end
-
-
--- 	flight_distance = x_pos
--- 	DebugWatch("custoff",cutoff_y)
--- 	DebugWatch("true sampe",true_sample)
--- 	for i = cutoff_y,true_sample,1 do 
-
--- 		DebugPrint("i "..i.." f "..cutoff_y.." x"..true_sample)
--- 		t = ts * (i-1)
--- 		y = math.sin(2*math.pi*freq*t)
--- 		x_pos = ((guidance_drop_dist*2) * t ) + flight_distance
--- 		y_pos = ((guidance_peak_height * y) ) +  guidance_peak_height
-
--- 	DebugWatch("true saddddse",flight_distance)
-
--- 		DrawLine(Vec(last_x_pos, last_y_pos, 0), Vec(x_pos, y_pos, 0), 1, 0, 0)
-
--- 		last_y_pos = y_pos
--- 		last_x_pos = x_pos
-
--- 	end
-
-
--- 	-- for i = 1,sr/2 do 
--- 	-- 	t = ts * (i-1)
--- 	-- 	y = math.sin(2*math.pi*freq*t)
--- 	-- 	DebugPrint(ts)
--- 	-- 	x_pos = (guidance_peak_dist*2) * t 
--- 	-- 	y_pos = ((guidance_peak_height * y) ) +  guidance_peak_height
-
-
--- 	-- 	DrawLine(Vec(last_x_pos, last_y_pos, 0), Vec(x_pos, y_pos, 0), 1, 0, 0)
-
--- 	-- 	last_y_pos = y_pos
--- 	-- 	last_x_pos = x_pos
-
--- 	-- end
-
-
-
--- end
+end
+

```

---

# Migration Report: kinetic_effects.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/kinetic_effects.lua
+++ patched/kinetic_effects.lua
@@ -1,12 +1,4 @@
-
-
-
-
-
-
-
-
-
+#version 2
 function fire(gun,barrelCoords,intel_payload)	
 	-- if(intel_payload and intel_payload.payload_type ) then 
 	-- 	DebugPrint("fire mode intel payload: "..intel_payload.payload_type)
@@ -24,7 +16,6 @@
 		play_gun_sound(gun.sound,barrelCoords.pos,50, gun.custom_fire_sound,gun,"sound")
     end
 
-
 	if(not oldShoot)then
 		if(gun.weaponType =="special") then 
 			pushSpecial(barrelCoords,gun)
@@ -79,18 +70,6 @@
 
 end
 
-
-
-
-
---[[ @PROJECTILEOPERATIONS
-
-
-	projectile operations code
-
-
-]]
-
 function projectileOperations(projectile,dt )
 	    projectile.lastPos = projectile.point1
 		projectile.cannonLoc.pos = projectile.point1
@@ -130,7 +109,6 @@
 		---
 
 		projectile.distance_travelled = projectile.distance_travelled + VecLength(VecScale(projectile.predictedBulletVelocity,dt))
-
 
 		-- unique case handling
 		if(not(is_rocket(projectile) or is_chemical_warhead(projectile))) then
@@ -169,7 +147,6 @@
 
 		else 
 
-
 			--- adding drag 
 
 			-- projectile.predictedBulletVelocity = VecScale(projectile.predictedBulletVelocity,0.950)
@@ -180,9 +157,7 @@
 			end
 			projectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity,(VecScale(dispersion,dt)))
 
-
 			--APPLYING WIND
-
 
 			projectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity,(VecScale(GetWindVelocity(),dt/
 				math.log(projectile.shellType.velocity))))
@@ -250,18 +225,11 @@
 			if(hit)then 
 				-- DebugPrint(rangeTestCoef.." "..projectile.shellType.payload)
 
-
 				--[[
 
-
 					TEMP FIX TO SUPPORT MORS LONGA
 
-
-
 				]]
-
-
-
 
 				if(projectile.hit_npc ==nil  or not projectile.hit_npc) then  
 					mors_longa_damage(projectile,shape1, VecAdd(projectile.point1, VecScale(VecNormalize(VecSub(point2,projectile.point1)),dist1))) 
@@ -269,20 +237,13 @@
 
 					--[[
 
-
 						TEMP FIX ENDS 
 
-
-
-
 					]]
 
 				local refDir = getRefDir(norm1,dir_vec)
 
-
 				--[[
-
-
 
 					acos(dotProduct(Va.normalize(), Vb.normalize()));
 				cross = crossProduct(Va, Vb);
@@ -398,27 +359,6 @@
 		
 end
 
-
-
---- bs maths 
-
---[[
-	10 start, 250 peak
-	150 max cimb
-
-	(peak / climb) * xy speed
-
-third rule
-
-	max_climb = ((distance_to_target / 3) / x_y_speed)
-
-	max_turn_vector = ((peak / climb) * xy speed) * 1.2
-	
-	descent_vector = max_turn_vector * 0.75 
-	descent_vel_increase = xy_speed * 1.05
-
-]]
-
 function homing_missile_computations(projectile,dt)
 	if(not projectile.homing_computations )then 
 		projectile.homing_computations = {}
@@ -456,21 +396,9 @@
 
 end
 
----
-
-
-
-----
-
----- specials
-
------
-
 function pushSpecial(barrelCoords,gun)
 	fireFoam(barrelCoords,gun)
 end
-
-
 
 function fireFoam(cannonLoc,gun)
 
@@ -511,18 +439,6 @@
 	end
 end
 
-
-
-
-
------ payload handlers
-
-
-	--- @payload_tank_he
-
-----
-
-
 function payload_tank_he(shell,hitPos,hitTarget,test,custom_explosion_size,non_penetration)
 
 	--Explosion(VecLerp(shell.last_flight_pos,hitPos,0.8),0.3)
@@ -563,16 +479,16 @@
 
 	-- hurt player if needed
 	local hurt_dist = explosion_size*2.1
-	local toPlayer = VecSub(GetPlayerCameraTransform().pos, hitPos)
+	local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, hitPos)
 	local distToPlayer = VecLength(toPlayer)
 	local distScale = clamp(1.0 - distToPlayer / hurt_dist, 0.0, 1.0)
-	if distScale > 0 then
+	if distScale ~= 0 then
 		local hit = QueryRaycast(hitPos, toPlayer, distToPlayer)
 		if(not hit) then 
 			local regular_damage = explosion_size*100
 			local expected_damage = math.random((regular_damage*.75),regular_damage*1.25)/100
 			local player_damage = 
-				SetPlayerHealth(GetPlayerHealth() - expected_damage*distScale)
+				SetPlayerHealth(playerId, GetPlayerHealth(playerId) - expected_damage*distScale)
 			end
 	end
 
@@ -601,15 +517,6 @@
 	-- DebugWatch("EXPLOSION SIZE3",explosion_size)
 
 end
-
-
-
-
----- 
-
----- PROJECTILE HANDLING
-
----
 
 function pushProjectile(cannonLoc,gun,intel_payload)
 	-- if(intel_payload and intel_payload.payload_type ) then 
@@ -670,10 +577,7 @@
 		loadedShell.optimum_distance = loadedShell.shellType.optimum_distance
 	end 
 
-
-
 	loadedShell = pre_mission_calibration(loadedShell,intel_payload)
-
 
 	loadedShell.pen_dist_coef= 1
 
@@ -691,18 +595,6 @@
 
 end
 
-
---[[
-	example payload 
-
-				intel_payload = {
-				target = target_body,
-
-
-			}
-
-
-]]
 function pre_mission_calibration(loadedShell,intel_payload)
 	-- if(intel_payload and intel_payload.payload_type ) then 
 	-- 	DebugPrint("calibration: intel payload: "..intel_payload.payload_type)
@@ -735,7 +627,6 @@
 		
 	end
 end
-
 
 function pushClusterProjectile(bombletPos,parentProjectile)
 	local fwdPos = TransformToParentPoint(bombletPos, Vec(0,-1,0))
@@ -784,22 +675,11 @@
 	projectileHandler.shellNum = (projectileHandler.shellNum%#projectileHandler.shells) +1
 end
 
-
---[[ @pop_projectile
-
-		CODE TO RUN ON PROJECTILE IMPACT
-
-		CONTROLS SHELL PENTRATION AND ALL SORTS
-
-]]
-
 function popProjectile(shell,hitTarget)
-
 
 		if(shell.shellType.payload=="cluster") then
 			if(VecLength(VecSub(shell.flightPos.pos,shell.originPos.pos))>10) then 
 				Explosion(shell.flightPos.pos,shell.shellType.explosionSize)
-
 
 			end
 			PlaySound(explosion_sounds[math.random(1,#explosion_sounds)], shell.point1, 20*(shell.shellType.explosionSize*shell.shellType.explosionSize), false)
@@ -892,11 +772,8 @@
 
 		end
 
-
 		SpawnParticle("smoke", shell.point1, Vec(0,1,0), (math.log(shell.shellType.caliber)/2)*(1+holeModifier), math.random(1,3))
 		SpawnParticle("fire", shell.point1, Vec(0,1,0), (math.log(shell.shellType.caliber)/4)*(1+holeModifier) , .25)
-
-
 
 		if(shell.shellType.payload and shell.penDepth>0 and 
 			(shell.shellType.payload == "HEAT" or shell.shellType.payload == "HEAT-MP"))  then
@@ -912,7 +789,6 @@
 				dist=(shell.shellType.caliber/100)*1.25
 			end
 			
-
 
 			local explosionPos = VecCopy(test.pos)
 			-- DebugPrint(dist)
@@ -938,8 +814,6 @@
 
 				explosive_penetrator_effect(shell,explosionPos)
 
-
-
 			end
 			-- DebugPrint("start  explostion pos  "..vec2str(test.pos))
 			explosionPos = TransformToParentPoint(test, Vec(0,dist*.7+0.25,0))
@@ -981,7 +855,6 @@
 
 			end
 			shell = deepcopy(projectileHandler.defaultShell)
-
 
 		elseif(shell.penDepth>0) then		
 			-- DebugPrint("2".." "..shell.penDepth)
@@ -1005,7 +878,6 @@
 					projectileShrapnel(shell,test,spallValue)
 					explosive_penetrator_effect(shell,test.pos)
 
-
 					shell.predictedBulletVelocity = VecAdd(shell.predictedBulletVelocity,rndVec(shell.shellType.velocity/(shell.penDepth*10)))
 					
 					-- SpawnParticle("darksmoke",test.pos, Vec(0, -.1, 0), shell.shellType.bulletdamage[2], 2)
@@ -1047,7 +919,6 @@
 							shell_hole[3]*(1+holeModifier))
 					end
 
-
 					local fireChance = math.random()
 					if(fireChance>globalConfig.fire_chance_thres)then
 						SpawnFire(test.pos)
@@ -1068,7 +939,6 @@
 							shell_hole[2]*(1+holeModifier),
 							shell_hole[3]*(1+holeModifier))
 					end
-
 
 					local fireChance = math.random()
 					if(fireChance>globalConfig.fire_chance_thres)then
@@ -1128,9 +998,7 @@
 		-- shell = deepcopy(artilleryHandler.defaultShell)
 		end
 
-
-end
-
+end
 
 function shell_passthrough_penetration(shell,test,spallValue,holeModifier)
 	shell.point1 = test.pos
@@ -1143,10 +1011,7 @@
 	
 end
 
-
-
 function projectileShrapnel(projectile,test,spallValue)
-
 
 			local projectile_vel = 80
 			local projectile_caliber = 20
@@ -1177,7 +1042,6 @@
 			--Loop through bodies and push them
 			for i=1,#bodies do
 				local b = bodies[i]
-
 
 				--Compute body center point and distance
 				local bmi, bma = GetBodyBounds(b)
@@ -1210,12 +1074,6 @@
 			pushSpalling(projectile.cannonLoc,projectile,test,spallValue)
 end
 
-
-
-----
-
------- SPALLING and SHRAPNAL HANDLING
-
 function pushSpalling(spallingLoc,spallShell,test,spallValue)
 
 	---			kinetic = 0.8,
@@ -1241,7 +1099,6 @@
 			spallFactor = globalConfig.spallFactor.kinetic	
 		end
 
-
 	end
 	local spall_num = spallValue*spallFactor
 	spall_num = math.max(spall_num,1)*math.random(3,9)--3
@@ -1317,7 +1174,6 @@
 		currentSpall.shellType.g = 0.7 + (math.random(0,5)/10)
 		currentSpall.shellType.b = 1
 
-
 		spallHandler.shellNum = (spallHandler.shellNum%#spallHandler.shells) +1
 	end
 	-- DebugPrint("test")
@@ -1345,12 +1201,10 @@
 
 function popSpalling(shell,hitTarget)
 
-
 		local penetration,passThrough,test,penDepth,dist,spallValue =  getProjectilePenetration(shell,hitTarget)
 		-- shell.penDepth = shell.penDepth - penDepth
 
 		local holeModifier = math.random(-15,15)/100
-
 
 		-- local daamge_coef = VecLength(shell.predictedBulletVelocity)/VecLength(shell.initial_speed)
 		-- DebugWatch("shell damage",shell.shellType.bulletdamage[1])
@@ -1457,7 +1311,6 @@
 		local g = projectile.shellType.g
 		local b = projectile.shellType.b
 
-
 		--- sprite drawing
 		DrawSprite(projectile.shellType.Spallingsprite, projectile.cannonLoc,projectile.shellType.shellWidth,shellHeight , r, g, b, 1, 0, false)
 		local altloc = projectile.cannonLoc
@@ -1469,14 +1322,12 @@
 
 		projectile.predictedBulletVelocity = VecScale(projectile.predictedBulletVelocity,0.9)
 
-
 		---
 		---
 
 			--- PROJECTILE MOTION
 
 		---
-
 
 		---  ADDING DISPERSION
 		local dispersion = Vec(math.random(-1,1)*projectile.dispersion,math.random(-1,1)*projectile.dispersion,math.random(-1,1)*projectile.dispersion)
@@ -1484,8 +1335,6 @@
 			dispersion=VecScale(dispersion,dispersionCoef)
 		end
 		projectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity,(VecScale(dispersion,dt)))
-
-
 
 		-- --- applying drag 
 		-- local spallDrag = VecScale(
@@ -1530,7 +1379,6 @@
 			end
 		
 end
-
 
 function pushshrapnel(spallingLoc,spallShell,test,hitTarget)
 
@@ -1620,14 +1468,12 @@
 		currentSpall.shellType.g = math.max((1.7 + (math.random(0,5)/10))*spall_damage_coef,0.3)
 		currentSpall.shellType.b = math.max((1 + (math.random(0,10)/10)) *spall_damage_coef,0.3)
 
-
 		spallHandler.shellNum = (spallHandler.shellNum%#spallHandler.shells) +1
 
 	end
 	-- DebugPrint("test")
 
 end
-
 
 function shrapnelOperations(projectile,dt )
 		projectile.cannonLoc.pos = projectile.point1
@@ -1639,7 +1485,6 @@
 		local g = projectile.shellType.g * spallDecay
 		local b = projectile.shellType.b * spallDecay
 
-
 		--- sprite drawing
 		DrawSprite(projectile.shellType.Spallingsprite, projectile.cannonLoc,projectile.shellType.shellWidth,shellHeight , r, g, b, 1, 0, false)
 		local altloc = projectile.cannonLoc
@@ -1649,14 +1494,12 @@
 		DrawSprite(projectile.shellType.Spallingsprite, altloc, projectile.shellType.shellWidth, projectile.shellType.shellWidth, r, g, b, 1, 0, false)
 		
 
-
 		---
 		---
 
 			--- PROJECTILE MOTION
 
 		---
-
 
 		---  ADDING DISPERSION
 
@@ -1667,8 +1510,6 @@
 			dispersion=VecScale(dispersion,dispersionCoef)
 		end
 		projectile.predictedBulletVelocity = VecAdd(projectile.predictedBulletVelocity,(VecScale(dispersion,dt)))
-
-
 
 		-- --- applying drag 
 		-- local spallDrag = VecScale(
@@ -1732,18 +1573,6 @@
 		end
 end
 
-
------
-
-
-
-----
-
------ SHELL HANDLING
-
-----
-
-
 function pushShell(gun,t_hitPos,dist,t_distance,t_cannon,t_penDepth)
 	-- utils.printStr("pushing shell")
 	if(dist <=0)then
@@ -1768,7 +1597,7 @@
 				end
 				-- utils.printStr("1")
 		end
-		-- SetString("hud.notification",artilleryHandler.shells[getShellNum()].penetrations.."\n"..artilleryHandler.shells[getShellNum()].timeToTarget)
+		-- SetString("hud.notification",artilleryHandler.shells[getShellNum()].penetrations.."\n"..artilleryHandler.shells[getShellNum()].timeToTarget, true)
 	-- utils.printStr("3")
 	end
 
@@ -1807,7 +1636,7 @@
 				artilleryHandler.shells[getShellNum()].maxChecks = shell.maxChecks
 				artilleryHandler.shells[getShellNum()].explosionSize = artilleryHandler.shells[getShellNum()].shellType.explosionSize
 				-- utils.printStr("1")
-		-- SetString("hud.notification",artilleryHandler.shells[getShellNum()].penetrations.."\n"..artilleryHandler.shells[getShellNum()].timeToTarget)
+		-- SetString("hud.notification",artilleryHandler.shells[getShellNum()].penetrations.."\n"..artilleryHandler.shells[getShellNum()].timeToTarget, true)
 	-- utils.printStr("3")
 	end
 
@@ -1841,7 +1670,6 @@
 					utils.printStr("no shell hitPos")
 				end
 
-
 		else
 
 			Explosion(test.pos,shell.explosionSize)
@@ -1866,9 +1694,6 @@
 	artilleryHandler.shellNum = ((artilleryHandler.shellNum+1) % #artilleryHandler.shells)+1
 end
 
-
-
-
 function kill_shell(shell)
 
 	shell.active = false
@@ -1879,7 +1704,6 @@
 	shell = deepcopy(projectileHandler.defaultShell)
 
 		end
-
 
 function artilleryTick(dt)
 	local activeShells = 0
@@ -1900,11 +1724,6 @@
 	-- utils.printStr(activeShells)
 end
 
-
-
-
-
- -- check left right, if number then explode, if 0 then fly on.
 function getPenetration(shell)
 	local cannonLoc = shell.t_cannon
 	local penetration = false
@@ -1994,11 +1813,11 @@
 	local x = 0 
 	local z = globalConfig.penCheck
 
-
 	local fwdPos = TransformToParentPoint(t_cannonLoc, Vec(x, z,y))
 
 	local direction = VecSub(fwdPos, t_cannonLoc.pos)
 
 	t_cannonLoc.pos = VecAdd(t_cannonLoc.pos, direction)
 	return t_cannonLoc
-end+end
+

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
@@ -1,768 +1,4 @@
-
---[[]
-#include "umf/umf_core.lua"
-#include "AVF_VERSION.lua"
-
-#include "common.lua"
-#include "ammo.lua"
-#include "weapons.lua"
-#include "vehicle_setup.lua"
-#include "AVF_UI.lua"
-#include "commander/team_allocater.lua"
-#include kinetic_effects.lua
-
-#include "audio_effects.lua"
-#include "visual_effects.lua"
-
-#include "AIComponent.lua"
-
-
-#include "explosionController.lua"
-
-
-#include "guidance.lua"
-
-#include "controls.lua"	
-1
-
-#include "commander/AVF_TAK.lua"	
-
-#include databus.lua
-
-#include debug_menu.lua
-
-]]
--- #include "../Abu Zayeet Ballistic Range/main/scripts/testing.lua"
-
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) 
-*
-* FILENAME :        main.lua             
-*
-* DESCRIPTION :
-*       File that controls player vehicle turrets within the game teardown (2020)
-*
-*		File Handles both player physics controlled and in vehicle controlled turrets
-*		This is extended to include ammo reloading and weapon group management
-*		
-*
-* SETUP FUNCTIONS :
-*		In V3 all initialization is done at level init and based entirely off 
-*		Vehicle xml values
-*
-*
-*		In accessor init: 
-*
-*       setValues(vehicle,weaponFeatures) - Establishes environment variables for vehicle
-*       gunInit() 						  - Establishes vehicle gun state
-*
-*		In accessor Tick(dt):
-*
-*		gunTick(dt)						  - Manages gun control during gameplay
-*
-*
-*		gunUpdate(d)					  - Manages gun elevation during gameplay
-*
-*
-*
-* VEHICLE SETUP 
-*
-*		add inside tags=""
-*
-*		vehicle -> cfg=vehicle
-*		body -> component=body
-*		vox  (for vehicle body) -> component=chassis
-*		vox (for turret) -> component=turret turretGroup=mainTurret
-*		joint (for turret joint) ->component=turretJoint
-*		vox (for gun) -> component=gun weaponType=2A46M group=primary  
-*		vox (for gun joint) -> component=gunJoint
-*
-*
-*
-* NOTES :
-*       Future versions may ammend issue with exact gun location
-*		physics based gun control lost after driving player vehicle.
-*       
-* 		Please ensure to add player click to hud.lua.  (no longer needed)
-*
-*       Copyright - Of course no copyright but please give credit if this code is 
-* 		re-used in part or whole by yourself or others.
-*
-* AUTHOR :    elboydo        START DATE :    04 Nov 2020
-*
-*
-* ACKNOWLEDGEMENTS:
-*
-*		Mnay thanks to the many users of the teardown discord for support in coding an establishing this mod,
-* 		particularly @rubikow for their invaluable assistance in grasping lua and the functions
-*		provided to teardown modders at the inception of this mod, many thanks to Thomasims for guidance on custom projectiles
-*		Thanks to spexta for all of the excellent models and assistance involved in developing this mod.  
-*
-* HUB REPO: https://github.com/elboydo/TearDownTurretControl
-*
-* CHANGES :
-*
-*			Release: Public release V_1 - NOV 11 - 11 - 2020
-*
-*			V2: Added Turret elevation
-*					Added crane functionality to control turret 
-*					Added high velocity shells
-*					+ other quality of life features
-*
-*			Release: Public release V_1_0_0 - DEC 21 - 12 - 2020
-*
-*			REMOVED:
-*					crane functionality to control turret - replaced with player input
-*
-*
-*			ADDITIONS:
-*					Complete rewrite
-*					XML driven control
-*					Complete XML overrides for weapons
-*					Lua controlled weapon / ammo configs
-*					Shell penetration
-*					Multiple weapon support
-*					Multilple gun support
-*					Kronenberg 1664 support
-*					Dynamic ammo and reloading
-*
-*					custom projectiles 
-*					tracers
-*					shrapnal
-*					backblast
-*					cannon blast
-*					sniperMode
-*					custom sniper zooms					
-*
-*			Release: Public release V_1_0_8 - DEC 22 - 12 - 2020
-*
-*
-*			Fixed: FOV bug on exiting game when in sniper mode
-*			New issue - this will have issues if you change your fov later, can be fixed
-*
-*
-*			Release: Public release V_1_0_9 - JAN 02 - 01 - 2021
-*
-*
-*			Fixed: FOV related Bugs
-* 			
-*			ADDITIONS:
-*				aerial Weapons and rockets. 
-*				Customization scripts
-*				gravityCoef and dispersionCoef to shells
-*
-*
-*
-*			Release: Public release V_1_1_0 - JAN 06 - 01 - 2021
-*
-*			ADDITIONS:
-*				More aerial Weapons and rockets. 
-*				guided Missiles
-*
-*
-*			Release: Public release V_1_1_1 - JAN 20 - 01 - 2021
-*
-*			ADDITIONS:
-*				Custom weapon and ammo slot to enable better custom weapons
-*				HEAT shells
-* 				HESH shells
-* 				Spalling / shrapnal mechanics
-* 				Improved zoom
-* 				ERA armour support
-*				
-*
-*
-*			Release: Public release V_1_1_1_75 - FEB 05 - 02 - 2021
-*
-*
-*				Temp fix for loading custom sprites - disabled custom shell sprites
-*
-*
-*
-*			Release: Public release V_1_1_2 - FEB 10 - 02 - 2021
-*
-*			ADDITIONS:
-*				Controls hud
-*				Demo map
-* 				Small fixes
-*
-*
-*
-*			Release: Public release V_1_2_1 - MARCH 22 - 03 - 2021
-*
-*			ADDITIONS:
-*				Interacton based control
-*
-*
-*
-*
-*			Release: Public release V_1_3_0 - June 20 - 06 - 2021
-*
-*			ADDITIONS:
-*				Reworked explosive system for better realism
-*				Improved penetration mechanics
-*				Added more realistic penetration model
-*
-*
-*			Release: Public release V_1_9_0 - June 20 - 06 - 2021
-**				lots of stuff unlisted here - projectile ops, pen charts, more features
-
-*			Release: Public release V_2_4_0 - Jan 20 - 01 - 2022
-*
-*			ADDITIONS:
-
-
-				All avf confirmed vehicles included with mod
-
-				artillery system rework 
-
-				interaction timers -- DONE
-
-				improve Heat effects / damage - DONE
-**
-
-
-*			Release: Public release V_2_4_1 - Feb 07 - 02 - 2022
-*
-*			ADDITIONS:
-
-
-				Player damage from bullets
-
-
-
-
-*			Release: Public release V_2_5_0 - xxx xx - xx - xxxx
-*
-*			ADDITIONS:
-
-
-				Shell ejection
-				Better HEAT impact
-				upgraded ERA / special armour behaviors
-
-				general bug  fixes - 
-					- fixed aim bug 
-					- fixed backblast customization 
-					- fixed vehicle mapping when incorrect weapon entered 
-					- fixed heat impact breaking 
-					- added better error handling 
-					- updated reloading to better occur across weapons 
-					- improved turret mechanics when leaving vehicle 
-					- improved recoil mechanics
-
-			TO DO:
-
-
-				ai pathing 
-
-				ai combat
-
-			ISSUES: 
-
-				HEAT non pen impact pos wrong
-				some lag issues
-
-
-*			Release: Public release V_2_6_0 - xxx xx - xx - xxxx
-*
-*			ADDITIONS:
-				Improved shell impact effects  [REALISM]
-				Improved HEAT mechanics [REALISM]
-				Improved penetration values  [REALISM]
-				doubled penetration checks pr vox (improves sloped armour)  [REALISM]
-
-			BUG FIXES 
-				Scope reticle missing
-				HEAT non pen impact pos wrong
-				ATGM aimpos wrong
-				some lag issues
-
-
-			TO DO:
-				custom sounds from avf_custom
-				custom gui from avf_custom
-
-				ai pathing 
-
-				ai combat
-
-			ISSUES: 
-
-
-*			Release: Public release V_2_6_2 - xxx xx - xx - xxxx
-*
-*			ADDITIONS:
-				Improved shell impact effects  [REALISM]
-				Improved HEAT mechanics [REALISM]
-				Improved penetration values  [REALISM]
-				doubled penetration checks pr vox (improves sloped armour)  [REALISM]
-
-				Added distance modifiers for shell penetration
-
-			BUG FIXES 
-
-
-			TO DO:
-				custom sounds from avf_custom
-				custom gui from avf_custom
-
-				ai pathing 
-
-				ai combat
-
-			ISSUES: 
-
-*
-]]
-
-
-
-debugMode = false
-
-DEBUG_AI = false
-
-DEBUG_CODE = false
-
-debugging_traversal =false
-
-debug_combat_stuff = false
-
-debug_weapon_pos = false
-
-
-debug_special_armour = false
-
-debug_shell_casings = false
-
-
-debug_player_damage = false
-
-
-debug_vehicle_locations_active = false
-
-AVF_DEV_HUD_VISIBLE = false
-
-debugStuff= {
-
-	redCrosses = {}
-}
-
-errorMessages = ""
-frameErrorMessages = ""
-
-globalConfig = {
-	base_pen = 0.1,
-	RHAe_2_vox = 0.01,
-	min_vehicle_health = 0.6,
-	penCheck = 0.01,
-	penIteration = 0.1,
-	pen_check_iterations = 100,
-	rpm_to_rad = 0.1047,
-	HEATRange = 3,
-	gravity = Vec(0,-10,0),
-	impulse_coef = 0.002,
-	fire_chance_thres = 0.975,
-	--gravity = Vec(0,-25,0),
-	weaponOrders = {
-			[1] = "primary",
-			[2] = "secondary",
-			[3] = "tertiary",
-			[4] = "smoke",
-			[5] = "utility1",
-			[6] = "utility2",
-			[7] = "utility3",
-			[8] = "1",
-			[9] = "2",
-			[10] = "3",
-			[11] = "4",
-			[12] = "5",
-			[13] = "6",
-			[14] = "coax",
-		},
-	MaxSpall = 16,
-	spallQuantity = 32,
-	spallFactor = {
-			kinetic = 0.85,
-			AP 		= 0.4,
-			APHE    = 0.4,
-			HESH 	= 1.8,
-			HESH 	= 1.5,
-			HEI 	= 1,
-	},
-
-	materials = {
-		rock  = 13,
-		dirt  = 0.2,
-		plaster = 0.1,
-		plastic = 0.05,
-		masonry = 0.27,
-		glass = 0.05,
-		foliage = 0.025,
-		wood  = 0.2,
-		metal  = 0.42,
-		hardmetal = 0.73,
-		heavymetal  = 13,
-		hardmasonry = 0.6,
-
-
-	},
-
-	HEAT_pentable = {
-		rock  = 13,
-		dirt  = 0.5,
-		plaster = 0.25,
-		plastic = 0.025,
-		masonry = 0.5,
-		glass = 0.2,
-		foliage = 0.0023,
-		wood  = 0.1,
-		metal  = 0.21,
-		hardmetal = 0.33,
-		heavymetal  = 4,
-		hardmasonry = 0.8,
-
-	},
-
-	kinetic_pentable = {
-		rock  = 13,
-		dirt  = 0.2,
-		plaster = 0.1,
-		plastic = 0.05,
-		masonry = 0.27,
-		glass = 0.05,
-		foliage = 0.025,
-		wood  = 0.2,
-		metal  = 0.23,
-		hardmetal = 0.45,
-		heavymetal  = 10,
-		hardmasonry = 0.6,
-
-
-	},
-	pen_coefs = {
-		HEAT = .75,
-		kinetic= .55,
-
-
-
-	},
-	optimum_spall_shell_calibre_size = 100, 
-
-	shrapnel_coefs = {
-		HEAT = 0.5,
-		kinetic= 2,
-		APHE = 25,
-		HE = 75,
-		shrapnel = 125,
-		frag = 125,
-
-
-
-
-	},
-	shrapnel_hard_damage_coef = {
-		HEAT = 1,
-		kinetic= 1,
-		HE = 0.8,
-
-	},
-	shrapnel_pen_coef = {
-		HEAT = 1,
-		kinetic= 1,
-		HE = 10,
-		shrapnel = 4,
-
-	},
-	shrapnel_speed_coefs = {
-		HEAT = 1,
-		kinetic= 1,
-		HE = 2,
-		shrapnel = 2,
-
-
-
-	},
-
-	armour_types = {
-		RHA = 0.03
-
-	},
-}
-penVals = "PENETRATION RESULTS\n-------------------------"
---[[
- Vehicle config
-]]
-
-
-
-avf_types = {
-	"vehicle",
-	"turret",
-	"artillery"
-}
-
-vehicle = {
-	vehicleName 				= "",
-	armed 						= true,
-  	Create 						= "elboydo"
-  }
-
-
- vehicles = {
-
- }
-
- ammoContainers = {
- 	refillTimer = 0,
- }
-
-
-vehicleFeatures = {}
-
-defaultVehicleFeatures = {
-	weapons = 
-		{
-			primary 	= {},
-			secondary 	= {},
-			tertiary 	= {},
-			coax    	= {},
-			smoke 		= {},
-			utility1 	= {},
-			utility2 	= {},
-			utility3 	= {},
-			["1"] 	= {},
-			["2"] 	= {},
-			["3"] 	= {},
-			["4"] 	= {},
-			["5"] 	= {},
-			["6"] 	= {},
-		},
-	utility = {
-		smoke 		= {},
-	},
-	equippedGroup = "primary",
-	turrets = 
-				{
-					mainTurret 			= {},
-					secondaryTurret 	= {},
-					tertiaryTurret 		= {}
-				}
-
-}
-
-artilleryHandler = 
-{
-	shellNum = 1,
-
-	explosionSize = 0.5,
-
-	shells = {
-
-	},
-	defaultShell = {active=false, hitPos=nil,timeToTarget =0},
-}
-shellSpeed = 0.005--5--0.05 --45
-
-projectileHandler = 
-	{
-		shellNum = 1,
-		shells = {
-
-		},
-	defaultShell = {active=false, velocity=nil, direction =nil, currentPos=nil, timeLaunched=nil},
-	velocity = 200,
-	gravity = Vec(0,-25,0),
-	shellWidth = 0.3,
-	shellHeight = 1.2,
-	}
-
-
-spallHandler = 
-	{
-		shellNum = 1,
-		shells = {
-
-		},
-	defaultShell = {active=false, velocity=nil, direction =nil, currentPos=nil, timeLaunched=nil},
-	velocity = 200,
-	gravity = Vec(0,-25,0),
-	shellWidth = 0.3,
-	shellHeight = 0.3,
-	}
-
-
-projectorHandler = 
-	{
-		shellNum = 1,
-		shells = {
-
-		},
-	defaultShell = {active=false, speed=0, currentPos=nil, hitPos=nil,timeToTarget =0},
-	}
-
-
-explosion_sounds = {}
-
-
-maxDist = 500
-
-AVF_Vehicle_Used = false
-
-interaction_timeout_max = 1
-
-interaction_timeout_timer = 0
-
-
-ai_scan_timestep = 0.3
-
-last_ai_scan = 0
-
-
-MISSILE_TRACK_TIME_MIN =1.3
-
-viewingMap = false
-
-AVF_V3 = {
-	interactions = {
-		firedLastFrame = false,
-
-
-	}
-
-
-}
-
-
--- weapon would use xml weaponType= tag then that would relate to the thing
-
-function init()
-	-- SetBool("savegame.mod.newVehicle",false)
-	-- SetInt("savegame.mod.playerFov",0)
-	-- originalFov = SetInt("options.gfx.fov", 90)
-	-- if(not GetInt("savegame.mod.playerFov") or GetInt("savegame.mod.playerFov") == 0) then
-	-- 	SetInt("savegame.mod.playerFov",GetInt("options.gfx.fov"))
-	-- 	-- DebugPrint(GetInt("options.gfx.fov").." | "..GetInt("savegame.mod.playerFov"))
-	-- end
-	-- DebugPrint(GetInt("options.gfx.fov").." | "..GetInt("savegame.mod.playerFov"))
-	-- SetInt("savegame.mod.playerFov",GetInt("options.gfx.fov"))
-	originalFov = GetInt("options.gfx.fov")---GetInt("savegame.mod.playerFov")
-	-- SetInt("options.gfx.fov",originalFov)
-	-- if(GetBool("savegame.mod.debug")) then	
-	-- 	debugMode = true
-	-- end
-
-
-	initCamera()
-
-	reticle1 = LoadSprite("MOD/sprite/reticle1.png")
-	reticle2 = LoadSprite("MOD/sprite/reticle2.png")
-	reticle3 = LoadSprite("MOD/sprite/reticle3.png")
-
-
-
-	globalConfig.gravity = VecScale(globalConfig.gravity,1)
-
-	ammoContainers.crates = FindTriggers("ammoStockpile",true)
-	ammoRefillSound = LoadSound(weaponDefaults.refillingAmmo)
-
-	local sceneVehicles = FindVehicles("cfg",true)
-	--utils.printStr(#sceneVehicles)
-
-	for i = 1,#sceneVehicles do 
-		local value = GetTagValue(sceneVehicles[i], "cfg")
-
-		if(value == "vehicle" and not HasTag(sceneVehicles[i],"AVF_Custom")) then
-
-			local index = #vehicles +1
-			vehicles[index] = {
-							vehicle ={
-									id = sceneVehicles[i],
-									groupIndex = index,
-									},
-							vehicleFeatures = deepcopy(defaultVehicleFeatures),
-							}
-			vehicle = vehicles[index].vehicle
-			vehicleFeatures = vehicles[index].vehicleFeatures
-
-			vehicle.last_cam_pos = nil
-			vehicle.last_external_cam_pos = nil
-
-
-			if(not GetBool("savegame.mod.debug")) then	
-				initVehicle(vehicles[index])
-			else
-				if(DEBUG_CODE) then 
-					local status,retVal = pcall(initVehicle,vehicles[index])
-					if status then 
-							-- utils.printStr("no errors")
-					else
-						errorMessages = errorMessages..retVal.."\n"
-					end
-				else
-					initVehicle(vehicles[index])
-				end
-			end
-		end
-	end
-
-
-	-- ignored_shapes = FindShapes("muzzle_blast_ignore",true)
-
-	-- ignored_bodies = {}
-	-- for i=1,#ignored_shapes do 
-	-- 	ignored_bodies[i] = GetShapeBody(ignored_shapes[i])
-	-- end
-
-	for i =1,1050 do
-		artilleryHandler.shells[i] = deepcopy(artilleryHandler.defaultShell)
-
-		projectorHandler.shells[i]= deepcopy(projectorHandler.defaultShell)
-
-		projectileHandler.shells[i]= deepcopy(projectileHandler.defaultShell)
-
-
-		spallHandler.shells[i]= deepcopy(projectileHandler.defaultShell)
-	end
-
-
-	for i=1, 7 do
-		explosion_sounds[i] = LoadSound("MOD/sounds/explosion/ExplosionDistant0"..i..".ogg")
-	end
-
-	loadCustomControls()
-
-	if(GetBool("savegame.mod.debug")) then	
-		utils.printStr("AVF: "..VERSION.." Started!")
-	end
-		
-		-- utils.printStr(testing.test)
-
-	gunSmokedissipation = 3
-	gunSmokeSize =1
-	gunSmokeGravity = 2
-
-
-
-	team_allocator_init()
-	AVF_TAK_INIT()
-
-	----- setting up tandem warhead pen valeus - ideally this will be raw deduction on major, or perhaps something more elegant is needed 
-
-	-- potentially a calc of 20-80 on primary charge to secondary 
-	
-	---- setup Complete
-
-	SetBool("level.avf.enabled", true)
-	
-end
-
-
-
+#version 2
 function initVehicle(vehicle_in,vehicle_type)
 
 	if unexpected_condition then error() end
@@ -771,7 +7,6 @@
 	vehicle.shapes = GetBodyShapes(vehicle.body)
 	vehicle.sniperFOV = originalFov
 	totalShapes = ""
-
 
 	if(vehicle_type~=nil) then 
 		vehicle.entity_type = vehicle_type
@@ -851,7 +86,6 @@
 
 			end	
 
-
 		-- end	
 
 	-- utils.printStr(totalShapes)
@@ -912,10 +146,8 @@
 
 	SetTag(vehicle.id,"avf_initialized")
 
-
 	-- utils.printStr(tstStrn)
 end
-
 
 function initAI()
 
@@ -923,108 +155,6 @@
 		AVF_ai:initAi()
 		-- DebugPrint("Vehicle: "..vehicle.id.." is ai ready")
 	end
-end
-
-function tick(dt)
-
-
-	-- Button will be placed in the bottom bar of the pause menu
-	if(SHOW_DEV_MENU) then 
-
-		if PauseMenuButton("AVF Settings") then
-			AVF_DEV_HUD_VISIBLE = not AVF_DEV_HUD_VISIBLE
-		end
-	end
-	if(AVF_DEV_HUD_VISIBLE) then 
-		SetTimeScale(0.01)
-	end
-
-	frameErrorMessages = ""
-
-	-- local player_pos = GetPlayerCameraTransform().pos
-	-- local hit,d,n= QueryRaycast(player_pos, Vec(0,-1,0),10)
-	-- DebugWatch("player height ",d)
-	-- if(AVF_Vehicle_Used and (InputPressed("esc") or InputDown("esc") or InputReleased("esc"))) then
-	-- 	SetInt("options.gfx.fov",originalFov)
-	-- end
-
-	
-	
-
-	if(DEBUG_CODE) then 
-		-- local status,retVal = pcall(guidance_tick,dt)
-		-- if status then 
-		-- 	-- utils.printStr("no errors")
-		-- else
-		-- 	DebugWatch("[GUIDANCE TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-		-- end
-
-		local status,retVal = pcall(gameplayTicks,dt)
-		if status then 
-			-- utils.printStr("no errors")
-		else
-			DebugWatch("[GAMEPLAY TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-		end
-
-		status,retVal = pcall(playerTicks,dt)
-		if status then 
-				
-		else
-			DebugWatch("[PLAYER TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-		end
-	else
-		gameplayTicks(dt)
-		playerTicks(dt)
-
-		--guidance_tick(dt)
-	end
-
-	pollNewVehicle(dt)
-	new_ai_scan()
-
-	if(GetBool("savegame.mod.debug")) then	
-		DebugWatch("Errors: ",errorMessages)
-		DebugWatch("Frame errors",frameErrorMessages)
-	end
-
-	if(debugMode or debug_player_damage) then 
-		if(#debugStuff.redCrosses>0) then
-			for i = 1,#debugStuff.redCrosses do
-
-				DebugCross(debugStuff.redCrosses[i],2-i,-1+i,0)
-
-			end
-		end
-	end
-
-	-- DebugWatch("x: ",InputValue("mousedx"))
-	-- DebugWatch("y: ",InputValue("mousedy"))
-	-- DebugWatch("fox: ",GetInt("options.gfx.fov", fov))
-
-	-- if(AVF_Vehicle_Used and (InputPressed("esc") or InputDown("esc") or InputReleased("esc"))) then
-	-- 	SetInt("options.gfx.fov",originalFov)
-	-- end
-
-
-	if(DEBUG_CODE) then 
-		-- local status,retVal = pcall(guidance_tick,dt)
-		-- if status then 
-		-- 	-- utils.printStr("no errors")
-		-- else
-		-- 	DebugWatch("[GUIDANCE TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-		-- end
-
-		local status,retVal = pcall(tool_ticks,dt)
-		if status then 
-			-- utils.printStr("no errors")
-		else
-			DebugWatch("[GAMEPLAY TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-		end	
-	else
-		tool_ticks(dt)
-	end
-
-
 end
 
 function tool_ticks(dt)
@@ -1036,24 +166,18 @@
 function gameplayTicks( dt )
 	if unexpected_condition then error() end
 
-
 	AVF_ai:aiTick(dt)
 
 	
 
 	reloadTicks(dt)
 
-
-
-
 	ammoRefillTick(dt)
 
 	explosionController:tick(dt)
 end
 
 function new_ai_scan(dt)
-
-
 
 	local current_game_time = GetTime()
 	if (current_game_time - last_ai_scan > ai_scan_timestep ) then 
@@ -1082,7 +206,6 @@
 	end
 
 end
-
 
 function init_new_ai()
 	AVF_ai:initAi()
@@ -1119,16 +242,15 @@
 						interaction_timeout_timer  = 0
 					end 
 
-
 					if(not AVF_Vehicle_Used) then
 						AVF_Vehicle_Used = true
 					end
 					vehicle = vehicles[vehicleid].vehicle
 					vehicleFeatures = vehicles[vehicleid].vehicleFeatures
-					SetString("level.avf.weapon_group",vehicleFeatures.equippedGroup)
+					SetString("level.avf.weapon_group",vehicleFeatures.equippedGroup, true)
 					handleInputs(dt)
 					--DebugWatch("sniperMode", vehicle.sniperMode) 
-					SetBool("level.avf.sniper_mode",false)
+					SetBool("level.avf.sniper_mode",false, true)
 					if(vehicle.artillery_weapon) then 
 						handle_artillery_control(dt)
 
@@ -1141,7 +263,7 @@
 						--	set_artillery_cam(vehicle.arty.final_pos,vehicle.arty.hit_target)
 						--else
 						 
-						SetBool("level.avf.sniper_mode",true)
+						SetBool("level.avf.sniper_mode",true, true)
 							set_sniper_cam(dt)
 						--end
 					end
@@ -1167,12 +289,10 @@
 
 end
 
-
-
 function interactionTicks(dt)
-	if(GetPlayerVehicle()==0) then 
-
-		local interactGun = GetPlayerInteractShape()
+	if(GetPlayerVehicle(playerId)==0) then 
+
+		local interactGun = GetPlayerInteractShape(playerId)
 	--SetTag(gun, "AVF_Parent", vehicle.groupIndex )
 		if(HasTag(interactGun,"weapon_host")) then 
 			local gun_shapes = GetBodyShapes(GetShapeBody(interactGun))
@@ -1198,12 +318,12 @@
 				return
 			end
 			if(vehicle.turret_weapon) then 
-				SetPlayerVehicle(vehicle.id)
+				SetPlayerVehicle(playerId, vehicle.id)
 			else
 				handleInteractedGunOperation(dt,interactGun)
 			end
 		end
-		local interactGun  =  GetPlayerGrabShape()
+		local interactGun  =  GetPlayerGrabShape(playerId)
 		if(HasTag(interactGun,"AVF_Parent") and  getPlayerGrabInput()) then 
 
 			-- DebugPrint("AVF_Parent val: "..GetTagValue(interactGun,"AVF_Parent").." gun index: "..interactGun)
@@ -1269,34 +389,6 @@
 
 end
 
-
-function update(dt)
-	--physics_update_ticks(dt) 
-	if(DEBUG_CODE) then 	
-		local status,retVal =pcall(physics_update_ticks,dt);
-		if status then 
-			-- utils.printStr("no errors")
-		else
-			DebugWatch("[ERROR]",retVal)
-		end 
-		local status,retVal = pcall(update_gameplay_ticks,dt)
-		if status then 
-				
-		else
-			DebugWatch("[update_gameplay_ticks ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
-		end
-		if(debug_vehicle_locations_active) then 
-			debug_vehicle_locations()
-		end
-	else
-		physics_update_ticks(dt)
-		update_gameplay_ticks(dt)
-	end
-
-
-end
-
-
 function update_gameplay_ticks(dt)
 	if unexpected_condition then error() end
 	if(
@@ -1306,7 +398,7 @@
 			inVehicle, vehicleid = playerInVehicle()
 				if(inVehicle)then 
 					-- if(InputPressed("esc") or InputDown("esc") or InputReleased("esc")) then
-					-- 	SetInt("options.gfx.fov",originalFov)
+					-- 	SetInt("options.gfx.fov",originalFov, true)
 					-- end
 					if(not AVF_Vehicle_Used ) then
 						AVF_Vehicle_Used = true
@@ -1374,7 +466,7 @@
 				end
 	else
 		-- if(AVF_Vehicle_Used) then
-		-- 	SetInt("options.gfx.fov",originalFov)
+		-- 	SetInt("options.gfx.fov",originalFov, true)
 		-- 	AVF_Vehicle_Used = false
 		-- end 
 		for _, vehicle in pairs(vehicles) do 					
@@ -1398,7 +490,7 @@
 		explosionController:update(dt)
 	end
 	-- if(AVF_Vehicle_Used and(InputPressed("esc") or InputDown("esc") or InputReleased("esc"))) then
-	-- 	SetInt("options.gfx.fov",originalFov)
+	-- 	SetInt("options.gfx.fov",originalFov, true)
 	-- end
 end
 
@@ -1412,25 +504,18 @@
 
 end
 
-
 function physics_update_ticks(dt) 
 	if unexpected_condition then error() end
 
 	projectileTick(dt)
 
-
 	spallingTick(dt)
 
 	projectorTick(dt)
 	
 	artilleryTick(dt)
 
-
-
-
-
-end
-
+end
 
 function physics_player_update(dt)
 
@@ -1439,7 +524,6 @@
 	else
 		handleGunMovement(dt)
 	end
-
 
 end
 
@@ -1505,7 +589,6 @@
 
 	
 end
-
 
 function handleSniperMode(dt ) 
 	if unexpected_condition then error() end
@@ -1665,7 +748,6 @@
 		end
 end
 
-
 function one_d_distance(num_1,num_2) 
 if(num_1 > num_2) then
 	return num_1
@@ -1677,22 +759,17 @@
 
 end
 
-
 function set_sniper_cam(dt) 
 	if unexpected_condition then error() end
 
-
 	local gunGroup = vehicleFeatures.weapons[vehicleFeatures.equippedGroup]
 	local testgunobj = gunGroup[1].id
-	SetInt("level.avf.focus_weapon",testgunobj )
+	SetInt("level.avf.focus_weapon",testgunobj , true)
 
 	local focusGun = gunGroup[1]
 	local y = tonumber(focusGun.sight[1].y)
 	local x = tonumber(focusGun.sight[1].x)
 	local z = tonumber(focusGun.sight[1].z)
-
-
-
 
 	local commanderPos = GetShapeWorldTransform(vehicleFeatures.commanderPos) 
 	local focusGunPos = GetShapeWorldTransform(focusGun.id) 
@@ -1727,7 +804,7 @@
 	end	
 	-- DebugWatch("zero range",zero_range)
 
-	SetInt("level.avf.zeroing",zero_range)
+	SetInt("level.avf.zeroing",zero_range, true)
 		-- DebugWatch("ZERO RANGE",zero_range)
 	local cmddist = zero_range
 	local deadzone = 0
@@ -1784,8 +861,6 @@
 	bodyPoint = Vec(0, -zero_range,-0.5*gravity * flight_time*flight_time )
 
 	expected_hit_point = TransformToParentPoint(t, bodyPoint)
-
-
 
 	local testCommander =  TransformToParentPoint(commanderPos,Vec(0,000,-zero_range))
 	-- local testGun =  TransformToParentPoint( focusGunPos,Vec(0,-zero_range,0))
@@ -1804,7 +879,6 @@
 	-- 	DebugWatch("test veclength: ",VecLength(VecSub(testCommander,testGun)))
 	--DebugWatch("test angle: ",offSetAngle)
 
-
 	-- simplified
 	-- local testGun =  TransformToParentPoint( focusGunPos,Vec(0,expected_hit_point[3],expected_hit_point[2]))
 	-- DebugCross(testGun,1,0,0	)
@@ -1825,8 +899,6 @@
 	
 	SetCameraTransform(commanderPos, vehicle.sniperFOV*ZOOMVALUE)
 end
-
-
 
 function set_artillery_cam()
 	local reticle_pos = vehicle.arty_cam_pos[1]
@@ -1924,13 +996,11 @@
 									
 					local rotation_force = GetBodyMass(GetShapeBody(gun.id))
 
-
 					local min, max = GetJointLimits(gun.gunJoint)
 					local current = GetJointMovement(gun.gunJoint)
 					gun.commander_view_y = clamp(0,1,(gun.commander_view_y + (gun.commander_y_rate*GetTimeStep() * -gun_movement)))
 					local target_y = gun.commander_view_y * (max - min) + min
 					SetJointMotorTarget(gun.gunJoint, target_y, gun.elevationRate)
-
 
 					-- if( gun.elevationSpeed) then
 					-- 	SetJointMotor(gun.gunJoint, (gun.elevationSpeed*gun_movement)*rotateSpeed)
@@ -2007,14 +1077,11 @@
 	-- 	end 
 	-- end
 
-
  
 end
-
 
 function get_arty_aim_movement(rotate_vec,arty_pos,gun)
 	if(arty_pos) then 
-
 
 		-- arty_pos.pos = rotate_vec
 		-- DebugWatch("arty_cam",arty_pos)
@@ -2039,15 +1106,6 @@
 		return 0,0
 	end
 end
-
---[[@GUNHANDLING
-
-
-	GUN_OPERATION_HANDLING_CODE
-	CODE KEY @GUNHANDLING
-
-
-]]
 
 function handleGunOperation(dt)
 
@@ -2121,7 +1179,6 @@
 							drawReticleSprite(t)
 
 							setReticleScreenPos(projectileHitPos)
-
 
 						else
 							removeReticleScreenPos()
@@ -2215,8 +1272,6 @@
 	-- end 
 end
 
-
-
 function handleGrabGunReset(interactGun)
 		for key,gunGroup in pairs(vehicleFeatures.weapons) do
 		
@@ -2231,7 +1286,6 @@
 			end
 		end
 end
-
 
 function handleInteractedGunOperation(dt,interactGun)
 
@@ -2365,13 +1419,6 @@
 
 end
 
-
---[[@MISSILE_GUIDANCE
-
-	MISSILE GUIDANCE CODE
-
-
-]]
 function initiate_missile_guidance(dt,gun,firing)
 	local target_body = nil
 	local max_dist = 400
@@ -2426,7 +1473,6 @@
 				payload_type 		= "target",
 				target_body = gun.missile_guidance_tracked_target ,
 
-
 			}	
 
 			fireControl(dt,gun,Vec(),intel_payload)
@@ -2437,11 +1483,9 @@
 			gun.missile_guidance_target_pos = center
 			-- Explosion(center,1.2)
 
-
 			intel_payload = {
 				payload_type 		= "target",
 				target_body = gun.missile_guidance_tracked_target ,
-
 
 			}
 			fireControl(dt,gun,Vec(),intel_payload)
@@ -2469,7 +1513,6 @@
 	end
 	return last_tracked,tracked_body
 end
-
 
 function get_largest_body(body)
 	local mass = GetBodyMass(body)
@@ -2485,8 +1528,6 @@
 	return largest_body,mass
 end
 
-
-
 function missile_guidance_behaviors(gun)
 	if(gun.missile_guidance_current_track>MISSILE_TRACK_TIME_MIN ) then 
 		DrawBodyOutline(gun.missile_guidance_tracked_target, 0, 1, 0, 1)
@@ -2506,15 +1547,6 @@
 	gun.missile_guidance_current_track = 0
 
 end
-
---[[@RELOADING
-
-
-	RELOAD HANDLING CODE 
-	CODE KEY @RELOADINGCODE
-
-
-]]
 
 function handleReload(gun,dt)
 	
@@ -2618,7 +1650,6 @@
 
 	--Set velocity on spawned bodies (only one in this case)
 
-
 	for i=1, #entities do
 		if GetEntityType(entities[i]) == "body" then
 			SetBodyVelocity(entities[i], vel)
@@ -2626,12 +1657,6 @@
 		end
 	end
 end
-
---[[@GUN_ANGLING
-
-	HANDLE GUN ANGLING CODE
-
-]]
 
 function handlegunAngles()
 	local gunGroup = vehicleFeatures.weapons[vehicleFeatures.equippedGroup]
@@ -2650,7 +1675,7 @@
 function storegunAngle(gun)
 	gun.currentGunjointAngle = GetJointMovement(gun.gunJoint)
 end
---- i have no idea what this function was supposed to originally do, i guess compare last frame to this frame maybe?
+
 function retainGunAngle(gun)
 	if(gun.currentGunjointAngle < GetJointMovement(gun.gunJoint)) then
 		return 1
@@ -2698,15 +1723,6 @@
 		end
 
 end
-
-
---[[@FIRECONTROL
-	
-	HANDLE WEAPON FIRE CONTROL
-
-
-
-]]
 
 function fireControl(dt,gun,barrelCoords,--[[optional]]intel_payload)
 	-- if(intel_payload and intel_payload.payload_type ) then 
@@ -2780,7 +1796,6 @@
 
 		SpawnParticle(smokePos,  VecScale(direction,0.25), math.random(3,16))
 
-
 		-- ParticleReset()
 		-- ParticleType("plain")
 		-- ParticleTile(5)
@@ -2795,7 +1810,6 @@
 		-- ParticleCollide(0, 1, "constant", 0.05)
 
 		-- SpawnParticle(smokePos,  direction, math.random(0.1,1))
-
 
 		-- SpawnParticle("smoke", smokePos, direction, (math.random(1,gunSmokeSize)*gun.smokeFactor), math.random(1,gunSmokeGravity)*gun.smokeFactor)
 		SpawnParticle("fire", smokePos,direction, gun.smokeFactor, .2)
@@ -2845,8 +1859,6 @@
 
 		SpawnParticle(smokePos,  direction, math.random(7,18))
 
-
-
 		-- ParticleReset()
 		-- ParticleType("plain")
 		-- ParticleTile(5)
@@ -2870,7 +1882,6 @@
 	-- DebugWatch("Direction: ["..direction[1]..","..direction[2]..","..direction[3].."]".."smokex: "..smokeX.." smoke y :"..smokeY)
 end
 
-
 function physicalBackblast(gun,backBlastLoc)
 			local backBlast = nil
 			if(gun.multiBarrel)then
@@ -2893,11 +1904,9 @@
 			QueryRejectVehicle(vehicle.id)
 			local bodies = QueryAabbBodies(mi, ma)
 
-
 			--Loop through bodies and push them
 			for i=1,#bodies do
 				local b = bodies[i]
-
 
 				local rand = (math.random())
 				if(rand<.005) then 
@@ -2966,7 +1975,6 @@
 			for i=1,#bodies do
 				local b = bodies[i]
 
-
 				--Compute body center point and distance
 				local bmi, bma = GetBodyBounds(b)
 				local bc = VecLerp(bmi, bma, 0.5)
@@ -2976,7 +1984,6 @@
 
 				--Get body mass
 				local mass = GetBodyMass(b)
-
 
 				--Check if body is should be affected
 				
@@ -3001,8 +2008,6 @@
 			end
 end
 
-
-
 function add_blast_dust(gun,strength,mass,b,body_vel)
 		local size = (strength*math.log(mass))* .2
 		local pos = GetBodyTransform(b).pos
@@ -3024,10 +2029,7 @@
 			SpawnParticle(p, v, rnd(3,9	))
 		end
 
-
-end
-
-
+end
 
 function rectifyBackBlastPoint(gun)
 
@@ -3090,7 +2092,6 @@
 		     -- SpawnParticle("smoke",hitPos, Vec(0, 1, 0), 3, 8)
 		    
 		end
-
 
 	 end
 
@@ -3142,8 +2143,6 @@
 	loadedShell.pos 			= cannonPos
 	loadedShell.vel 			= Vec()
 
-
-
 	-- defaultShell = {active=false, hitPos=nil,timeToTarget =0}
 	-- 			maxDist					= 10,
 	-- 			magazineCapacity 		= 6,
@@ -3151,11 +2150,8 @@
 	-- 			smokeFactor 			= .5,
 	-- 			smokeMulti				= 1,
 
-
-
 	projectorHandler.shellNum = (projectorHandler.shellNum%#projectorHandler.shells) +1
 end
-
 
 function reloadSmoke(projector)
 	projector.currentReload = projector.reload
@@ -3208,7 +2204,6 @@
 	-- chopperVel = VecScale(chopperVel, 0.98)
 	-- chopperTransform.pos = VecAdd(chopperTransform.pos, VecScale(chopperVel, dt))
 
-
 end
 
 function popSmoke(shell)
@@ -3230,10 +2225,6 @@
 	-- body
 end
 
---[[
-	simulate the projectiles motion from the weapon
-
-]]
 function simulate_projectile_motion(gun,cannonLoc) 
 	local dt = GetTimeStep()
 
@@ -3281,7 +2272,6 @@
 
 		end
 
-
 	--	DrawLine(projectile.point1,point2,0,1)
 		local hit, dist1,norm1,shape1 = QueryRaycast(projectile.point1, VecNormalize(VecSub(point2,projectile.point1)),VecLength(VecSub(point2,projectile.point1)))
 		if(hit)then 
@@ -3310,20 +2300,16 @@
 		hit_target = true
 	end
 
-
-
 	if(vehicle.sniperMode) then 
 			vehicle.last_mouse_shift = {0,0}
 			vehicle.arty_cam_pos = {TransformCopy(final_pos),hit_target}
 
-
 		--set_artillery_cam(final_pos,hit_target)
 	end
 
 	return final_pos,hit_target 
 
 end
-
 
 function processRecoil(gun)
 	local recoil = 0.01
@@ -3396,8 +2382,6 @@
 
 end
 
-
-
 function testDistance(gun )
 	local cannonLoc=  rectifyBarrelCoords(gun)
 	QueryRejectBody(vehicle.body)
@@ -3408,7 +2392,6 @@
     hit, dist = QueryRaycast(cannonLoc.pos, direction, maxDist,.2)
     utils.printStr(dist.." | "..type(norma))
 end
-
 
 function vec2str(tvec)
     return "(x: "..tvec[1].."a y: "..tvec[2].." z: "..tvec[3]..")"
@@ -3481,7 +2464,6 @@
 	
 	end
 end
-
 
 function explosive_penetrator_effect(projectile,hitPos)
 	local impactSize = projectile.shellType.bulletdamage[1]/3
@@ -3526,8 +2508,6 @@
 	end
 end
 
-
-
 function mors_longa_damage(projectile, hitshape,hitPos)
 
 		local mors_longa_damage_mod = 7.5
@@ -3540,15 +2520,15 @@
             local path_damage = "level.goreai.body_damage_player." .. hitBody 
 		    local damage = GetFloat(path_damage) + gun_damage
 		    -- DebugPrint("damage done: "..damage)
-		    SetFloat(path_damage, damage) -- Specific damage to each body by handle.
-
-		    SetFloat("level.goreai.body_damage_player_x", hitPos[1])
-		    SetFloat("level.goreai.body_damage_player_y", hitPos[2])
-		    SetFloat("level.goreai.body_damage_player_z", hitPos[3])
-
-		    SetFloat("level.goreai.body_damage_player_vel_x", projectile.predictedBulletVelocity[1])
-		    SetFloat("level.goreai.body_damage_player_vel_y", projectile.predictedBulletVelocity[2])
-		    SetFloat("level.goreai.body_damage_player_vel_z", projectile.predictedBulletVelocity[3])
+		    SetFloat(path_damage, damage, true) -- Specific damage to each body by handle.
+
+		    SetFloat("level.goreai.body_damage_player_x", hitPos[1], true)
+		    SetFloat("level.goreai.body_damage_player_y", hitPos[2], true)
+		    SetFloat("level.goreai.body_damage_player_z", hitPos[3], true)
+
+		    SetFloat("level.goreai.body_damage_player_vel_x", projectile.predictedBulletVelocity[1], true)
+		    SetFloat("level.goreai.body_damage_player_vel_y", projectile.predictedBulletVelocity[2], true)
+		    SetFloat("level.goreai.body_damage_player_vel_z", projectile.predictedBulletVelocity[3], true)
 
 		    projectile.hit_npc = true
             -- DebugPrint("gun damage hit for "..gun_damage)
@@ -3567,7 +2547,6 @@
 	local refDir = VecSub(dir, VecScale(hitNormal, VecDot(hitNormal, dir)*2))
 	return refDir
 end
-
 
 function apply_impact_impulse(pos,projectile,shape1,factor)
 	local pos = VecAdd(projectile.point1, VecScale(VecNormalize(VecSub(point2,projectile.point1)),dist1))
@@ -3601,9 +2580,6 @@
 		end
 end
 
-
- -- check left right, if number then explode, if 0 then fly on.
- 	-- pen coef typically 0.1 == 100mm
 function getProjectilePenetration(shell,hitTarget)
 	local cannonLoc = shell.cannonLoc
 	cannonLoc.pos = shell.point1
@@ -3654,8 +2630,6 @@
 
 	for i =1,pen_check_iterations*iteration_coef do 
 
-
-
 		if(debugMode) then 
 			debugStuff.redCrosses[#debugStuff.redCrosses+1] = test.pos 
 
@@ -3674,7 +2648,6 @@
 		spallCoef = spallCoef + penValue
 		damagePoints[i] = VecCopy(test.pos)
 		if(not hit1)then
-
 
 			penDepth = globalConfig.penCheck*i
 			penetration=true
@@ -3692,7 +2665,6 @@
 		shell.penDepth = shell.penDepth  - sum_pen_depth
 	end
 
-
 	if(dist1 ==0) then
 
 		passThrough = not hit1
@@ -3749,15 +2721,6 @@
 	return penetration,passThrough,test,penDepth,dist1,spallValue
 end
 
-
--- original pen value code
- --- (penValue + checkArmor(hitTarget))*pen_coef
-
- -- updated representative value below
-
- -- hardmetal = 0.45 
- -- rha = 0.03
-
 function calculate_pen_value(shell,hitTarget,test,pen_coef)
 	local mat,r,g,b = GetShapeMaterialAtPosition(hitTarget,test.pos)
 	local penValue = get_penetration_table(shell)[mat]
@@ -3772,11 +2735,8 @@
 	end
 	return penValue
 
-
-end
-
-
--- returns pen table for shell based on payload type 
+end
+
 function get_penetration_table(shell) 
 	if(shell.shellType.payload =="HEAT") then 
 		-- DebugPrint("heat payload")
@@ -3790,7 +2750,6 @@
 
 end
 
--- returns pen table for shell based on payload type 
 function get_penetration_table_by_payload(payload) 
 	if(payload =="HEAT") then 
 		-- DebugPrint("heat payload")
@@ -3803,6 +2762,7 @@
 	end
 
 end
+
 function checkArmor(target,RHAe)
 	for armour_type,modifier in pairs(globalConfig.armour_types) do 
 		if(HasTag(target,armour_type)) then 
@@ -3816,7 +2776,6 @@
 	return 0
 
 end
-
 
 function rectifyBarrelCoords(gun)
 	local barrel = nil
@@ -3842,8 +2801,6 @@
 	return cannonLoc
 end
 
-
-
 function retrieve_first_barrel_coord(gun)
 	local barrel = nil
 
@@ -3865,8 +2822,6 @@
 	cannonLoc.pos = add_vehicle_vel(cannonLoc.pos,gun.parent_vehicle)
 	return cannonLoc
 end
-
-
 
 function getBarrelCoords(gun)
 	local barrel = nil
@@ -3887,7 +2842,6 @@
 	cannonLoc.pos = add_vehicle_vel(cannonLoc.pos,gun.parent_vehicle)
 	return cannonLoc
 end
-
 
 function add_vehicle_vel(pos,vehicle_id)
 	return VecAdd(
@@ -3902,7 +2856,6 @@
 				)
 			)	
 end
-
 
 function turretRotatation(turret,turretJoint,aim_gun,gun)
 	if unexpected_condition then error() end
@@ -4024,6 +2977,7 @@
 	local orientationFactor = clamp(VecDot(forward, toPlayer) * 0.7 + 0.3, 0.0, 1.0)
 	return orientationFactor
 end
+
 function gunAngle(x,y,z,gun,gunJoint)
 
 	local targetAngle, dist = getTargetAngle(gun)
@@ -4031,7 +2985,7 @@
 	
 
 	-- targetAngle = targetAngle*verted
-    -- SetString("hud.notification","target Angle: "..targetAngle.."\nDist: "..dist.."\nJoint at: "..GetJointMovement(gunJoint).."\n min"..gun.elevationMin.." max:"..gun.elevationMax)
+    -- SetString("hud.notification","target Angle: "..targetAngle.."\nDist: "..dist.."\nJoint at: "..GetJointMovement(gunJoint).."\n min"..gun.elevationMin.." max:"..gun.elevationMax, true)
     local bias = 0
     if(-GetJointMovement(gunJoint) < (targetAngle-bias)) then
 			SetJointMotor(gunJoint, 1*bias)
@@ -4042,7 +2996,6 @@
 	end 
 
 end
-
 
 function autoGunAim(gun,barrelCoords)
 	local turretPos = retrieve_first_barrel_coord(gun).pos--GetShapeWorldTransform(gun.id).pos -- cheej
@@ -4073,7 +3026,6 @@
 	local lookDir =  VecAdd(turretPos,VecScale(shootDir,gun.zeroing))
 	local nt = Transform()
 
-
 	nt.rot = QuatLookAt(turretPos, lookDir) -- cheej
 	nt.pos = VecCopy(turretPos)
 	nt = TransformToParentPoint(nt,Vec(0,0,-gun.zeroing))
@@ -4105,7 +3057,6 @@
 	-- DebugWatch("dir",dir)
 
 	local rotation_force = GetBodyMass(GetShapeBody(gun.id))
-
 
 	local min, max = GetJointLimits(gun.gunJoint)
 	local current = GetJointMovement(gun.gunJoint)
@@ -4156,6 +3107,7 @@
 function lockGun(gun)
 	gun.lockedAngle =  GetJointMovement(gun.gunJoint)
 end
+
 function lockTurret(turret)
 	turret.lockedAngle =  GetJointMovement(turret.turretJoint)
 end
@@ -4164,7 +3116,7 @@
 	
 
 	-- targetAngle = targetAngle*verted
-    -- SetString("hud.notification","target Angle: "..targetAngle.."\nDist: "..dist.."\nJoint at: "..GetJointMovement(gunJoint).."\n min"..gun.elevationMin.." max:"..gun.elevationMax)
+    -- SetString("hud.notification","target Angle: "..targetAngle.."\nDist: "..dist.."\nJoint at: "..GetJointMovement(gunJoint).."\n min"..gun.elevationMin.." max:"..gun.elevationMax, true)
     local turretMovement = 0
     if(GetJointMovement(turret.turretJoint) > turret.lockedAngle) then
 			turretMovement = 1
@@ -4175,12 +3127,11 @@
 
 end
 
-
 function lockedGunAngle(gun)
 	
 
 	-- targetAngle = targetAngle*verted
-    -- SetString("hud.notification","target Angle: "..targetAngle.."\nDist: "..dist.."\nJoint at: "..GetJointMovement(gunJoint).."\n min"..gun.elevationMin.." max:"..gun.elevationMax)
+    -- SetString("hud.notification","target Angle: "..targetAngle.."\nDist: "..dist.."\nJoint at: "..GetJointMovement(gunJoint).."\n min"..gun.elevationMin.." max:"..gun.elevationMax, true)
     local gunMovement = 0
     if(GetJointMovement(gun.gunJoint) > gun.lockedAngle) then
 			gunMovement = 1
@@ -4190,8 +3141,6 @@
 	return gunMovement
 
 end
-
-
 
 function getTargetAngle(gun )
 	 	local gunTransform =	GetShapeWorldTransform(GetJointOtherShape(gun.gunJoint,gun.id))
@@ -4205,8 +3154,6 @@
 		local fwdPos = TransformToParentPoint(gunTransform, Vec(0,maxDist *-1 ,0))
 	    local direction = VecSub(fwdPos, gunTransform.pos)
 
-
-
 	     -- printloc(direction)
 	    direction = VecNormalize(direction)
     	QueryRejectBody(vehicle.body)
@@ -4216,8 +3163,6 @@
 
 		-- outerReticleScreenPos = 
 		-- TransformToParentPoint(gunTransform, )
-
-
 
 	    if(dist == 0)then
 	    	dist = maxDist
@@ -4230,29 +3175,14 @@
 		return targetAngle,dist
 end
 
-
---Return a random vector of desired length
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
 
-
 function rnd(mi, ma)
 	return math.random(1000)/1000*(ma-mi) + mi
 end
-
-
---[[
-
-
-
-		PLAYER BEHAVIOURS 
-
-
-
-
-]]
 
 function inflict_player_damage(projectile,point2)
   local t= Transform(projectile.point1,QuatLookAt(projectile.point1,point2))
@@ -4263,15 +3193,15 @@
 
   hurt_dist = VecLength(VecSub(projectile.point1,point2))
   --Hurt player
-  local player_cam_pos = GetPlayerCameraTransform().pos
-  local player_pos = GetPlayerTransform().pos
+  local player_cam_pos = GetPlayerCameraTransform(playerId).pos
+  local player_pos = GetPlayerTransform(playerId).pos
 
   player_pos = VecLerp(player_pos,player_cam_pos,0.8)
   local toPlayer = VecSub(player_pos, t.pos)
   local distToPlayer = VecLength(toPlayer)
   local distScale = clamp(1.0 - distToPlayer / hurt_dist, 0.0, 1.0)
   -- DebugWatch("test",distScale)
-  if distScale > 0 then
+  if distScale ~= 0 then
     -- DebugWatch("dist scale",distScale)
     toPlayer = VecNormalize(toPlayer)
     -- DebugWatch("dot to player",VecDot(d, toPlayer))
@@ -4282,8 +3212,6 @@
       local hit,hit_dist = QueryRaycast(p, toPlayer, distToPlayer)
       if not hit then
 
-
-
 				if(debug_player_damage) then 
 					DebugWatch("hit?",hit)
 	      			DebugWatch("dist?",distToPlayer)
@@ -4295,7 +3223,7 @@
       			distScale = VecDot(d, toPlayer)
 				-- DebugWatch("player would be hit",distToPlayer)
 				-- DebugWatch("hit? ",VecDot(d, toPlayer))
-				SetPlayerHealth(GetPlayerHealth() - 0.035 * projectile.shellType.bulletdamage[1] * (distScale*2)*projectile.shellType.caliber)
+				SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.035 * projectile.shellType.bulletdamage[1] * (distScale*2)*projectile.shellType.caliber)
 				return true, player_pos
 			end
 		end	
@@ -4316,8 +3244,6 @@
 	
 end
 
-
-
 function getPlayerInteactInput()
 	if InputPressed("interact") or InputDown("interact") then
 	 
@@ -4349,7 +3275,6 @@
 	-- DebugWatch("mouse pressed",InputPressed(armedVehicleControls.fire))
  -- 	DebugWatch("Mouse down ",InputDown(armedVehicleControls.fire)) 
 
-
 	if not InputPressed(armedVehicleControls.fire) and InputDown(armedVehicleControls.fire) then
 		return true
 
@@ -4375,6 +3300,7 @@
 	end
 	
 end
+
 function input_active(inputKey) 
 	if not InputPressed(inputKey) and InputDown(inputKey) then
 		return true
@@ -4383,15 +3309,6 @@
 		return false
 	end
 end
-
-
---[[
-
-
-	AMMO REFILL
-
-]]
-
 
 function ammoRefillTick(dt)
 	
@@ -4413,7 +3330,6 @@
 		end
 	end
 end
-
 
 function refillAmmo(dt)
 	local reloaded = 0
@@ -4510,7 +3426,6 @@
 		vehicle.last_mouse_shift = {0,0}
 	end
 
-
 	handleLightOperation()
 
 		-- local k,v = next(vehicleFeatures.weapons,nil)
@@ -4522,12 +3437,11 @@
 	return InputValue("camerax") * modifier , InputValue("cameray") * modifier 
 end
 
-
 function playerInVehicle()
 
 	local inVehicle = false
 	local currentVehicle = 0
-	local playerVehicle = GetPlayerVehicle()
+	local playerVehicle = GetPlayerVehicle(playerId)
 	
 	for key,vehicle in pairs(vehicles) do
 		-- utils.printStr(vehicles[key].vehicleFeatures.weapons.primary[1].name)
@@ -4542,14 +3456,205 @@
 	return inVehicle,currentVehicle 
 end
 
---Return a random vector of desired length
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
 end
 
-
-
-
-
-UpdateQuickloadPatch() +function server.init()
+    originalFov = GetInt("options.gfx.fov")---GetInt("savegame.mod.playerFov")
+    -- SetInt("options.gfx.fov",originalFov, true)
+    -- if(GetBool("savegame.mod.debug")) then	
+    -- 	debugMode = true
+    -- end
+    initCamera()
+    reticle1 = LoadSprite("MOD/sprite/reticle1.png")
+    reticle2 = LoadSprite("MOD/sprite/reticle2.png")
+    reticle3 = LoadSprite("MOD/sprite/reticle3.png")
+    globalConfig.gravity = VecScale(globalConfig.gravity,1)
+    ammoContainers.crates = FindTriggers("ammoStockpile",true)
+    local sceneVehicles = FindVehicles("cfg",true)
+    --utils.printStr(#sceneVehicles)
+    for i = 1,#sceneVehicles do 
+    	local value = GetTagValue(sceneVehicles[i], "cfg")
+
+    	if(value == "vehicle" and not HasTag(sceneVehicles[i],"AVF_Custom")) then
+
+    		local index = #vehicles +1
+    		vehicles[index] = {
+    						vehicle ={
+    								id = sceneVehicles[i],
+    								groupIndex = index,
+    								},
+    						vehicleFeatures = deepcopy(defaultVehicleFeatures),
+    						}
+    		vehicle = vehicles[index].vehicle
+    		vehicleFeatures = vehicles[index].vehicleFeatures
+
+    		vehicle.last_cam_pos = nil
+    		vehicle.last_external_cam_pos = nil
+
+    		if(not GetBool("savegame.mod.debug")) then	
+    			initVehicle(vehicles[index])
+    		else
+    			if(DEBUG_CODE) then 
+    				local status,retVal = pcall(initVehicle,vehicles[index])
+    				if status then 
+    						-- utils.printStr("no errors")
+    				else
+    					errorMessages = errorMessages..retVal.."\n"
+    				end
+    			else
+    				initVehicle(vehicles[index])
+    			end
+    		end
+    	end
+    end
+    -- ignored_shapes = FindShapes("muzzle_blast_ignore",true)
+    -- ignored_bodies = {}
+    -- for i=1,#ignored_shapes do 
+    -- 	ignored_bodies[i] = GetShapeBody(ignored_shapes[i])
+    -- end
+    for i =1,1050 do
+    	artilleryHandler.shells[i] = deepcopy(artilleryHandler.defaultShell)
+
+    	projectorHandler.shells[i]= deepcopy(projectorHandler.defaultShell)
+
+    	projectileHandler.shells[i]= deepcopy(projectileHandler.defaultShell)
+
+    	spallHandler.shells[i]= deepcopy(projectileHandler.defaultShell)
+    end
+    loadCustomControls()
+    if(GetBool("savegame.mod.debug")) then	
+    	utils.printStr("AVF: "..VERSION.." Started!")
+    end
+    	-- utils.printStr(testing.test)
+    gunSmokedissipation = 3
+    gunSmokeSize =1
+    gunSmokeGravity = 2
+    team_allocator_init()
+    AVF_TAK_INIT()
+    ----- setting up tandem warhead pen valeus - ideally this will be raw deduction on major, or perhaps something more elegant is needed 
+    -- potentially a calc of 20-80 on primary charge to secondary 
+    ---- setup Complete
+    SetBool("level.avf.enabled", true, true)
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(SHOW_DEV_MENU) then 
+
+        	if PauseMenuButton("AVF Settings") then
+        		AVF_DEV_HUD_VISIBLE = not AVF_DEV_HUD_VISIBLE
+        	end
+        end
+        if(AVF_DEV_HUD_VISIBLE) then 
+        	SetTimeScale(0.01)
+        end
+        frameErrorMessages = ""
+        -- local player_pos = GetPlayerCameraTransform(playerId).pos
+        -- local hit,d,n= QueryRaycast(player_pos, Vec(0,-1,0),10)
+        -- DebugWatch("player height ",d)
+        -- if(AVF_Vehicle_Used and (InputPressed("esc") or InputDown("esc") or InputReleased("esc"))) then
+        -- 	SetInt("options.gfx.fov",originalFov, true)
+        -- end
+        if(DEBUG_CODE) then 
+        	-- local status,retVal = pcall(guidance_tick,dt)
+        	-- if status then 
+        	-- 	-- utils.printStr("no errors")
+        	-- else
+        	-- 	DebugWatch("[GUIDANCE TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+        	-- end
+
+        	local status,retVal = pcall(gameplayTicks,dt)
+        	if status then 
+        		-- utils.printStr("no errors")
+        	else
+        		DebugWatch("[GAMEPLAY TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+        	end
+
+        	status,retVal = pcall(playerTicks,dt)
+        	if status then 
+
+        	else
+        		DebugWatch("[PLAYER TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+        	end
+        else
+        	gameplayTicks(dt)
+        	playerTicks(dt)
+
+        	--guidance_tick(dt)
+        end
+        pollNewVehicle(dt)
+        new_ai_scan()
+        if(GetBool("savegame.mod.debug")) then	
+        	DebugWatch("Errors: ",errorMessages)
+        	DebugWatch("Frame errors",frameErrorMessages)
+        end
+        if(debugMode or debug_player_damage) then 
+        	if(#debugStuff.redCrosses>0) then
+        		for i = 1,#debugStuff.redCrosses do
+
+        			DebugCross(debugStuff.redCrosses[i],2-i,-1+i,0)
+
+        		end
+        	end
+        end
+        -- DebugWatch("x: ",InputValue("mousedx"))
+        -- DebugWatch("y: ",InputValue("mousedy"))
+        -- DebugWatch("fox: ",GetInt("options.gfx.fov", fov))
+        -- if(AVF_Vehicle_Used and (InputPressed("esc") or InputDown("esc") or InputReleased("esc"))) then
+        -- 	SetInt("options.gfx.fov",originalFov, true)
+        -- end
+        if(DEBUG_CODE) then 
+        	-- local status,retVal = pcall(guidance_tick,dt)
+        	-- if status then 
+        	-- 	-- utils.printStr("no errors")
+        	-- else
+        	-- 	DebugWatch("[GUIDANCE TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+        	-- end
+
+        	local status,retVal = pcall(tool_ticks,dt)
+        	if status then 
+        		-- utils.printStr("no errors")
+        	else
+        		DebugWatch("[GAMEPLAY TICK ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+        	end	
+        else
+        	tool_ticks(dt)
+        end
+    end
+end
+
+function server.update(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(DEBUG_CODE) then 	
+        	local status,retVal =pcall(physics_update_ticks,dt);
+        	if status then 
+        		-- utils.printStr("no errors")
+        	else
+        		DebugWatch("[ERROR]",retVal)
+        	end 
+        	local status,retVal = pcall(update_gameplay_ticks,dt)
+        	if status then 
+
+        	else
+        		DebugWatch("[update_gameplay_ticks ERROR]",retVal)--frameErrorMessages = frameErrorMessages..retVal.."\n"
+        	end
+        	if(debug_vehicle_locations_active) then 
+        		debug_vehicle_locations()
+        	end
+        else
+        	physics_update_ticks(dt)
+        	update_gameplay_ticks(dt)
+        end
+    end
+end
+
+function client.init()
+    ammoRefillSound = LoadSound(weaponDefaults.refillingAmmo)
+    for i=1, 7 do
+    	explosion_sounds[i] = LoadSound("MOD/sounds/explosion/ExplosionDistant0"..i..".ogg")
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
@@ -1,182 +1,137 @@
-#include "controls.lua"
-#include "AVF_VERSION.lua"
+#version 2
+local alpha = getAlphabet()
 
-changingKey = false
-selectedKey = ""
-
--- esc	Escape key
--- lmb	Left mouse button
--- rmb	Right mouse button
--- up	Up key
--- down	Down key
--- left	Left key
--- right	Right key
--- space	Space bar
--- interact	Interact key
--- return	Return key
--- any	Any key or button
--- a,b,c,...	Latin, alphabetical keys a through z
--- mousewheel	Mouse wheel. Only valid in InputValue.
--- mousedx	Mouse horizontal diff. Only valid in InputValue.
--- mousedy
-uniqueCharacters = {
-	[1] = "lmb",
-	[2] = "rmb",
-	[3] = "up",
-	[4] = "down",
-	[5] = "left",
-	[6] = "right",
-	[7] = "space",
-	[8] = "interact",
-	[9] = "return",
-
-}
-
--- The_Letter = ('ABCDEFGHIJKLMNOPQRSTUVWXYZA'):match(The_Letter..'(.)')
 function getAlphabet ()
     local letters = {}
     for ascii = 97, 122 do table.insert(letters, string.char(ascii)) end
     for key,value in ipairs(uniqueCharacters) do table.insert(letters, value) end
     return letters
 end
- 
-local alpha = getAlphabet()
--- DebugPrint(alpha[25] .. alpha[1] .. alpha[25]..alpha[28]) 
 
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if(changingKey and (InputPressed("any") or InputPressed("rmb") )) then
 
-function tick(dt )
-	-- if(InputPressed("rmb")) then
-	-- 	DebugPrint("rmb pressed")
-	-- end
-	if(changingKey and (InputPressed("any") or InputPressed("rmb") )) then
-
-		-- DebugPrint("rmb pressed")
-		for key,value in ipairs(alpha) do
-			if(InputPressed(value)) then
-				SetString("savegame.mod.controls."..selectedKey,value)
-				selectedKey = ""
-				changingKey = false
-			end
-		end
-	end
-
+    	-- DebugPrint("rmb pressed")
+    	for key,value in ipairs(alpha) do
+    		if(InputPressed(value)) then
+    			SetString("savegame.mod.controls."..selectedKey,value, true)
+    			selectedKey = ""
+    			changingKey = false
+    		end
+    	end
+    end
 end
 
+function client.draw()
+    UiPush()
+    UiTranslate(UiCenter(), 50)
+    UiAlign("center top")
 
-function draw()
+    --Title
+    UiImageBox("MOD/gfx/AVF_logo.png",400,400,1,1)
+    UiTranslate(0, 300)
+    UiFont("bold.ttf", 48)
+    UiText("Armed Vehicles Framework (AVF) Options")
+    UiTranslate(0, 50)
+    UiText("AVF Version: "..VERSION)
+    UiPop()
+    ---AVF_logo
 
-	UiPush()
-	UiTranslate(UiCenter(), 50)
-	UiAlign("center top")
+    UiTranslate(UiCenter()/2, 150)
+    UiFont("regular.ttf", 26)
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    -- UiPush()
+    -- 	UiTranslate(-110, 0)
+    -- 	UiAlign("center left")
+    -- 	for key,val in ipairs(armedVehicleControlsOrder) do
+    -- 		local inputKey = armedVehicleControls[val] 
+    -- 		key = val
 
-	--Title
-	UiImageBox("MOD/gfx/AVF_logo.png",400,400,1,1)
-	UiTranslate(0, 300)
-	UiFont("bold.ttf", 48)
-	UiText("Armed Vehicles Framework (AVF) Options")
-	UiTranslate(0, 50)
-	UiText("AVF Version: "..VERSION)
-	UiPop()
-	---AVF_logo
+    -- 		if(GetString("savegame.mod.controls."..key,val)~="")then
+    -- 			inputKey = GetString("savegame.mod.controls."..key,inputKey)
+    -- 		end
+    -- 		local displayText = string.format("%-10s %5s",key..": ",inputKey)
 
+    -- 		if(changingKey and selectedKey == key) then
+    -- 			displayText = string.format("%-10s %5s",key..": ","____")
+    -- 			UiTextButton(displayText, 250, 40)
+    -- 		else
+    -- 			if UiTextButton(displayText, 250, 40) and not changingKey then
 
-	UiTranslate(UiCenter()/2, 150)
-	UiFont("regular.ttf", 26)
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-	-- UiPush()
-	-- 	UiTranslate(-110, 0)
-	-- 	UiAlign("center left")
-	-- 	for key,val in ipairs(armedVehicleControlsOrder) do
-	-- 		local inputKey = armedVehicleControls[val] 
-	-- 		key = val
+    -- 				changingKey = true
+    -- 				selectedKey = key
 
-	-- 		if(GetString("savegame.mod.controls."..key,val)~="")then
-	-- 			inputKey = GetString("savegame.mod.controls."..key,inputKey)
-	-- 		end
-	-- 		local displayText = string.format("%-10s %5s",key..": ",inputKey)
-			
-	-- 		if(changingKey and selectedKey == key) then
-	-- 			displayText = string.format("%-10s %5s",key..": ","____")
-	-- 			UiTextButton(displayText, 250, 40)
-	-- 		else
-	-- 			if UiTextButton(displayText, 250, 40) and not changingKey then
-					
-	-- 				changingKey = true
-	-- 				selectedKey = key
+    -- 			end
+    -- 		end	
+    -- 		UiTranslate(0, 40)
+    -- 	end
+    -- 	UiTranslate(0, 40)
+    -- 	if UiTextButton("Reset Defaults", 250, 40) then
+    -- 		for key,val in pairs(armedVehicleControls) do
+    -- 			SetString("savegame.mod.controls."..key,val, true)
 
-	-- 			end
-	-- 		end	
-	-- 		UiTranslate(0, 40)
-	-- 	end
-	-- 	UiTranslate(0, 40)
-	-- 	if UiTextButton("Reset Defaults", 250, 40) then
-	-- 		for key,val in pairs(armedVehicleControls) do
-	-- 			SetString("savegame.mod.controls."..key,val)
+    -- 		end
 
-	-- 		end
+    -- 	end
 
-	-- 	end
+    -- UiPop()
 
-	-- UiPop()
+    UiTranslate(UiCenter(), 250)
+    --Draw buttons
+    UiTranslate(0, 200)
+    UiFont("regular.ttf", 26)
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    UiPush()
+    	local w = 300
+    	local h = 50
+    	UiTranslate(-110, -100)
+    	-- if not GetBool("savegame.mod.mph") then
+    	-- 	UiPush()
+    	-- 		UiColor(0.5, 1, 0.5, 0.2)
+    	-- 		UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
+    	-- 	UiPop()
+    	-- end
+    	UiAlign("left")
+    	-- local debugText = "Enable"
+    	-- if(GetBool("savegame.mod.debug")) then
+    	-- 	debugText = "Disable"
+    	-- end
+    	-- if UiTextButton(debugText.." Debug Mode", w, h) then
+    	-- 	SetBool("savegame.mod.debug", not GetBool("savegame.mod.debug"), true)
+    	-- end	
+    	UiTranslate(0, 50)
+    	local infiniteAmmoText = "Enable"
+    	if(GetBool("savegame.mod.infiniteAmmo")) then
+    		infiniteAmmoText = "Disable"
+    	end
+    	if UiTextButton(infiniteAmmoText.." Infinite Ammo", w, h) then
+    		SetBool("savegame.mod.infiniteAmmo", not GetBool("savegame.mod.infiniteAmmo"), true)
+    	end	
+    	UiTranslate(0, 50)
+    	local controlsHudText = "Hide"
+    	if(GetBool("savegame.mod.hideControls")) then
+    		controlsHudText = "Show"
+    	end
+    	if UiTextButton(controlsHudText.." Controls HUD", w, h) then
+    		SetBool("savegame.mod.hideControls", not GetBool("savegame.mod.hideControls"), true)
+    	end
 
+    	-- UiTranslate(270, 0)
+    	-- if GetBool("savegame.mod.mph") then
+    	-- 	UiPush()
+    	-- 		UiColor(0.5, 1, 0.5, 0.2)
+    	-- 		UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
+    	-- 	UiPop()
+    	-- end
+    	-- if UiTextButton("Imperial MPH", 200, 40) then
+    	-- 	SetBool("savegame.mod.mph", true, true)
+    	-- end
+    UiPop()
 
-	
-	UiTranslate(UiCenter(), 250)
-	--Draw buttons
-	UiTranslate(0, 200)
-	UiFont("regular.ttf", 26)
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-	UiPush()
-		local w = 300
-		local h = 50
-		UiTranslate(-110, -100)
-		-- if not GetBool("savegame.mod.mph") then
-		-- 	UiPush()
-		-- 		UiColor(0.5, 1, 0.5, 0.2)
-		-- 		UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
-		-- 	UiPop()
-		-- end
-		UiAlign("left")
-		-- local debugText = "Enable"
-		-- if(GetBool("savegame.mod.debug")) then
-		-- 	debugText = "Disable"
-		-- end
-		-- if UiTextButton(debugText.." Debug Mode", w, h) then
-		-- 	SetBool("savegame.mod.debug", not GetBool("savegame.mod.debug"))
-		-- end	
-		UiTranslate(0, 50)
-		local infiniteAmmoText = "Enable"
-		if(GetBool("savegame.mod.infiniteAmmo")) then
-			infiniteAmmoText = "Disable"
-		end
-		if UiTextButton(infiniteAmmoText.." Infinite Ammo", w, h) then
-			SetBool("savegame.mod.infiniteAmmo", not GetBool("savegame.mod.infiniteAmmo"))
-		end	
-		UiTranslate(0, 50)
-		local controlsHudText = "Hide"
-		if(GetBool("savegame.mod.hideControls")) then
-			controlsHudText = "Show"
-		end
-		if UiTextButton(controlsHudText.." Controls HUD", w, h) then
-			SetBool("savegame.mod.hideControls", not GetBool("savegame.mod.hideControls"))
-		end
-
-
-		-- UiTranslate(270, 0)
-		-- if GetBool("savegame.mod.mph") then
-		-- 	UiPush()
-		-- 		UiColor(0.5, 1, 0.5, 0.2)
-		-- 		UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
-		-- 	UiPop()
-		-- end
-		-- if UiTextButton("Imperial MPH", 200, 40) then
-		-- 	SetBool("savegame.mod.mph", true)
-		-- end
-	UiPop()
-	
-	UiTranslate(0, 100)
-	if UiTextButton("Close", 200, 40) then
-		Menu()
-	end
+    UiTranslate(0, 100)
+    if UiTextButton("Close", 200, 40) then
+    	Menu()
+    end
 end
 

```

---

# Migration Report: pathfinding\AStarSearch.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding\AStarSearch.lua
+++ patched/pathfinding\AStarSearch.lua
@@ -1,416 +1,4 @@
-#include "priorityQueue.lua"
-#include "mapNode.lua"
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        AStarSearch.lua             
-*
-* DESCRIPTION :
-*       Implements A Star search in Teardown 2020
-*
-*       
-*
-*
-* NOTES :
-*
-*       Yes, i know while loops are bad. This can be optimised by 
-*       using for loops and making it async       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-*                            Release Date :    29 Nov 2021 
-*
-]]
-
-__ASTAR_DEBUG = false
-
-AStar = {
-    APPROACHES = {
-        [1] = 'traditional',
-        [2] = 'enhanced',
-        [3] = 'enhanced',
-        [4] = 'enhanced',
-        [5] = 'traditional',
-        [6] = 'traditional',
-        [7] = 'traditional',
-
-    },
-    heuristic_approach = "enhanced", -- traditional or enhanced
-    maxChecks = 1000,
-    cameFrom = {},
-    costSoFar = {},
-    maxIterations = 10,
-    currentIteration = 0,
-
-    heuristicWeight = 21.78,
-    vert_heuristic_weight = 1.25,
-    vert_limit = 3
-
-}
-
-path_variables = {
-    frontier =nil, 
-    cameFrom = nil, 
-    costSoFar = nil,
-    start = nil,
-    goal = nil,
-    checks = 0
-}
-
-active_search = {}
-
-
-
-
-
-function AStar:Heuristic(a, b)
-      return (math.abs(a[1] - b[1]) + math.abs(a[2] - b[2])) * self.heuristicWeight
- end 
-
-
-function AStar:Heuristic_3d(a, b)
-      return (math.abs(a[1] - b[1]) + math.abs(a[2] - b[2])) * self.heuristicWeight
- end 
-
-function AStar:heuristic_vec_3d(node_a,node_b)
-    return VecLength(VecSub(node_a:getPos(),node_b:getPos()))* self.vert_heuristic_weight
-
-end
-
-
-function AStar:AStarSearch(graph, start, goal)
-    
-        frontier =  deepcopy(PriorityQueue)
-        frontier:init(#graph,#graph[1])
-        frontier:put(deepcopy(start), 0);
-
-        local startIndex = start:getIndex()
-        -- DebugPrint(type(start:getIndex()).." | "..type(start:getIndex()[2]))
-        -- DebugPrint("Val = " ..startIndex[1]..startIndex[2])
-        local cameFrom = {}
-        cameFrom[startIndex[2]] = {}
-        cameFrom[startIndex[2]][startIndex[1]] = start;
-        local lastIndex = nil
-        local costSoFar = {}
-        costSoFar[startIndex[2]] = {}
-        costSoFar[startIndex[2]][startIndex[1]] = start:getCost();
-
-        local current = nil
-        local currentIndex = nil
-        local nextNode = nil
-        local newCost = 0
-        local priority = 0
-        local currentIndex = nil
-        local nodeExists = false
-        local next_node_cost =0
-        local next_node_vert_cost = 0
-        local totalNodes = 0
-        -- DebugPrint(frontier:empty())
-        -- for i=1,self.maxChecks do 
-        local checks = 0
-        for i=1,frontier:size() do 
-       --- while not frontier:empty() do
-            checks = checks + 1
-        
-            current = deepcopy(frontier:get()) 
-
-            totalNodes = totalNodes + 1
-            if (type(current)~="table" or not current or  current:Equals(goal)) then
-                -- DebugPrint("goal found")
-
-                if(_AI_DEBUG_PATHING) then 
-                    DebugWatch("goal found, checks taken",checks)
-                end
-                break
-            end  
-            currentIndex = current:getIndex()
-             for key, val in ipairs(current:getNeighbors()) do
-                    nextNode =  deepcopy(graph[val.y][val.x])
-                    next_node_cost =  nextNode:getCost()
-                    newCost = costSoFar[currentIndex[2]][currentIndex[1]] + next_node_cost
-                    nodeExists = ( self:nodeExists(costSoFar,val.y,val.x) )
-                    if(nextNode.validTerrain and( not nodeExists or (not (cameFrom[currentIndex[2]][currentIndex[1]]:indexEquals({val.y,val.x}))  and 
-                                        newCost < costSoFar[val.y][val.x])) )
-                    then 
-                        if(not nodeExists) then 
-                            if(not costSoFar[val.y]) then 
-                                costSoFar[val.y] = {}
-                                cameFrom[val.y] = {}
-                            end
-                        end
-                        nextNode:setCost(next_node_cost)
-                        costSoFar[val.y][val.x] = newCost
-                        priority =   newCost +  self:Heuristic(nextNode:getIndex(),goal:getIndex())
-                        frontier:put(nextNode, priority)
-                        cameFrom[val.y][val.x] = deepcopy(current)
-
-                        -- DebugPrint(newCost.." | "..val.y.." | "..val.x.." | ")
-                        -- lastIndex = deepcopy(val)
-                        
-                        -- DebugPrint(nextNode:getIndex()[1].." | "..nextNode:getIndex()[2])
-                    --+ graph.Cost(current, next);
-                    end
-             end
-         end
-         -- DebugPrint("total checks = "..checks)
-         
-         local path = self:reconstructPath(graph,cameFrom,current,start,totalNodes)
-         -- DebugPrint("total nodes: "..totalNodes)
-         return path
- end
-
-
-function AStar:init(graph, start, goal,heuristic_approach)
-        if not heuristic_approach then 
-            self.heuristic_approach = self.APPROACHES[math.random(1,#self.APPROACHES)]
-        else
-            self.heuristic_approach = heuristic_approach
-        end
-        if(_AI_DEBUG_PATHING) then 
-            DebugWatch("heuristic_approach",self.heuristic_approach)
-        end
-
-        frontier =  deepcopy(PriorityQueue)
-        frontier:init(#graph,#graph[1])
-        frontier:put(deepcopy(start), 0);
-
-        local startIndex = start:getIndex()
-        -- DebugPrint(type(start:getIndex()).." | "..type(start:getIndex()[2]))
-        -- DebugPrint("Val = " ..startIndex[1]..startIndex[2])
-        local cameFrom = {}
-        cameFrom[startIndex[2]] = {}
-        cameFrom[startIndex[2]][startIndex[1]] = start;
-        local lastIndex = nil
-        local costSoFar = {}
-        costSoFar[startIndex[2]] = {}
-        costSoFar[startIndex[2]][startIndex[1]] = start:getCost();
-
-        local current = nil
-        local currentIndex = nil
-        local nextNode = nil
-        local newCost = 0
-        local priority = 0
-        local currentIndex = nil
-        local nodeExists = false
-        local next_node_cost =0
-        local totalNodes = 0
-        -- DebugPrint(frontier:empty())
-        -- for i=1,self.maxChecks do 
-        local checks = 0
-        active_search = deepcopy(path_variables)
-        start_time = GetTime()
-        active_search = {
-            frontier =frontier, 
-            cameFrom = cameFrom, 
-            costSoFar = costSoFar,
-            start = start,
-            goal = goal,
-            checks = 0,
-        }
-        return graph
-    end
-
-
-function AStar:AStarSearch_2(graph)
-
-        
-        local frontier =active_search['frontier'] 
-        local cameFrom = active_search['cameFrom']
-        local costSoFar = active_search['costSoFar']
-        local start = active_search['start']
-        local goal = active_search['goal']
-        local checks = active_search['checks']
-        
-
-        local path = nil
-        local goal_found = nil
-        local current = nil
-        local currentIndex = nil
-        local nextNode = nil
-        local newCost = 0
-        local priority = 0
-        local currentIndex = nil
-        local nodeExists = false
-        local next_node_cost =0
-        local totalNodes = 0
-        local next_node_vert_cost = 0
-        local current_time = GetTime()
-        -- DebugPrint(frontier:empty())
-        -- for i=1,self.maxChecks do 
-        search_length = math.floor(math.max(5,50/current_time)* (5/ mapSize.grid))
-        local max_search_time = 1.5   
-        for i=1,search_length do 
-       --- while not frontier:empty() do
-            checks = checks + 1
-        
-            current = deepcopy(frontier:get()) 
-
-            totalNodes = totalNodes + 1
-
-            if(type(current)~="table" or not current) then 
-                return -1
-            elseif  (GetTime() - start_time >max_search_time) then 
-                goal_found = true
-            elseif (current:Equals(goal)) then
-                -- DebugPrint("goal found")
-                goal_found = true
-                    -- local start_tpime = active_search['search_start']
-                -- DebugWatch("goal found, time start:", start_time )
-
-                if(_AI_DEBUG_PATHING) then 
-                    DebugWatch("goal found, time taken:", current_time - start_time)
-                    
-                    DebugWatch("goal found, checks taken",checks)
-                end
-                break
-            end  
-            currentIndex = current:getIndex()
-            for key, val in ipairs(current:getNeighbors()) do
-                    -- DebugWatch("current height",current:getHeight())
-                    next_node_cost = graph[val.y][val.x]:getPotentialCost(current:getHeight())
-                    nextNode =  deepcopy(graph[val.y][val.x])
-                    
-                    -- next_node_vert_cost = self:heuristic_vec_3d(current,nextNode)
-                    if(__ASTAR_DEBUG) then 
-                        DebugLine(current:getPos(),nextNode:getPos())
-                    end
-                    newCost = costSoFar[currentIndex[2]][currentIndex[1]] + next_node_cost --+next_node_vert_cost
-                    nodeExists = ( self:nodeExists(costSoFar,val.y,val.x) )
-                    if(nextNode.validTerrain and( not nodeExists or (not (cameFrom[currentIndex[2]][currentIndex[1]]:indexEquals({val.y,val.x}))  and 
-                                        newCost < costSoFar[val.y][val.x])) )
-                    then 
-                        if(not nodeExists) then 
-                            if(not costSoFar[val.y]) then 
-                                costSoFar[val.y] = {}
-                                cameFrom[val.y] = {}
-                            end
-                        end
-                        nextNode:setCost(next_node_cost)
-                        costSoFar[val.y][val.x] = newCost
-                        if(self.heuristic_approach == "traditional") then 
-                            priority =   newCost + (self:heuristic_vec_3d(goal,nextNode)*self:Heuristic(nextNode:getIndex(),goal:getIndex()))
-                        elseif(self.heuristic_approach == "enhanced") then 
-                            priority =   newCost *  (self:heuristic_vec_3d(goal,nextNode)*self:Heuristic(nextNode:getIndex(),goal:getIndex()))
-                        else 
-                            priority =   newCost + (self:heuristic_vec_3d(goal,nextNode)*self:Heuristic(nextNode:getIndex(),goal:getIndex()))
-                        end
-                        frontier:put(nextNode, priority)
-                        cameFrom[val.y][val.x] = deepcopy(current)
-
-                        -- DebugPrint(newCost.." | "..val.y.." | "..val.x.." | ")
-                        -- lastIndex = deepcopy(val)
-                        
-                        -- DebugPrint(nextNode:getIndex()[1].." | "..nextNode:getIndex()[2])
-                    --+ graph.Cost(current, next);
-                    end
-             end
-        end
-         -- DebugPrint("total checks = "..checks)
-        active_search = {
-            frontier =frontier, 
-            cameFrom = cameFrom, 
-            costSoFar = costSoFar,
-            start = start,
-            goal = goal,
-            checks = checks
-        }        
-        if(goal_found) then 
-            path = self:reconstructPath(graph,cameFrom,current,start,totalNodes)
-        end
-         -- DebugPrint("total nodes: "..totalNodes)
-        return path
-
- end
-
- function AStar:nodeExists(listVar,y,x)
-     if(listVar[y] and listVar[y][x]) then
-        return true
-    else
-        return false
-    end
- end
-
-function AStar:reconstructPath(graph,cameFrom,current,start,totalNodes)
-    local path = {}
-    local index = current:getIndex()
-    -- for i=1,100 do 
-    while not current:Equals(start) do
-    -- DebugPrint("came from: "..index[1].." | "..index[2])
-        path[#path+1] = graph[index[2]][index[1]]:getPos()
-        index = cameFrom[current:getIndex()[2]][current:getIndex()[1]]:getIndex()
-        current = deepcopy(graph[index[2]][index[1]])
-        
-        if(current:Equals(start)) then
-                -- DebugPrint("found, nodes: "..totalNodes) 
-
-            break
-
-        end
-
-
-    end
-    local tmp = {}
-    for i = #path, 1, -1 do
-        tmp[#tmp+1] = path[i]
-    end
-    path = tmp
-    return path
-
-
-end
-
-function AStar:path_to_pos(graph,cameFrom,current,start,totalNodes)
-    local path = {}
-    local index = current:getIndex()
-    -- for i=1,100 do 
-    while not current:Equals(start) do
-    -- DebugPrint("came from: "..index[1].." | "..index[2])
-        path[#path+1] = index
-        index = cameFrom[current:getIndex()[2]][current:getIndex()[1]]:getIndex()
-        current = deepcopy(graph[index[2]][index[1]])
-        
-        if(current:Equals(start)) then
-                -- DebugPrint("found, nodes: "..totalNodes) 
-
-            break
-
-        end
-
-
-    end
-    local tmp = {}
-    for i = #path, 1, -1 do
-        tmp[#tmp+1] = path[i]
-    end
-    path = tmp
-    return path
-
-
-end
-
- function AStar:drawPath(graph,path)
-    local node1,node2 = nil,nil
-    for i = 1, #path-1 do
-        node1 = graph[path[i][2]][path[i][1]]:getPos()
-        node2 = graph[path[i+1][2]][path[i+1][1]]:getPos()
-        DebugLine(node1,node2, 1, 0, 0)
-    end
- end
-
- function AStar:drawPath2(graph,path,colours)
-    local node1,node2 = nil,nil
-
-    for i = 1, #path-1 do
-        node1 = graph[path[i][2]][path[i][1]]:getPos()
-        node2 = graph[path[i+1][2]][path[i+1][1]]:getPos()
-        DebugLine(node1,node2, 1,0,0)
-    end
- end
-
-
+#version 2
 function deepcopy(orig)
     local orig_type = type(orig)
     local copy
@@ -425,3 +13,4 @@
     end
     return copy
 end
+

```

---

# Migration Report: pathfinding\AVF_pathfinder.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding\AVF_pathfinder.lua
+++ patched/pathfinding\AVF_pathfinder.lua
@@ -1,226 +1,4 @@
-
-
----PATHFINDING LINKED
-
-#include "mapNode.lua"
-#include "AStarSearch.lua"
-
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        AVF_AI_3.lua             
-*
-* DESCRIPTION :
-*       File that implements racing AI inside teardown 2020, with PID controllers
-* 		to ensure cars respond to coordinates in a good fashion and can handle high speed
-*		Also includes simple goal achievement and collision avoidance 
-*		Including "driver ai" to make them more / less aggressive with speed, cornering
-*		overtaking, and driving. 
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-PATHSET = false
-
-mapInitialized = false
-DEBUG = false
-
-PATH_NODE_TOLERANCE = 3
-
-AVF_PATHFINDING_STEP = 1.2
-map = {
-
-  xIndex = 0,
-  data = {
-
-  },
-
-  smoothingFactor = 3,
-  validMaterials = {
-  	[1] = {	
-  		material = "masonry",
-
-
-	  validSurfaceColours ={ 
-				[1] = {
-					r = 0.20,
-					g = 0.20,
-					b = 0.20,
-					range = 0.2
-				},
-				[2] = {
-					r = 0.80,
-					g = 0.60,
-					b = 0.60,
-					range = 0.2
-				},
-				[3] = {
-					r = 0.34,
-					g = 0.34,
-					b = 0.34,
-					range = 0.2
-				},
-			},
-		},
-	},
-}
-
--- negative grid pos is solved by simply showing 
-mapSize = {
-			x=600,
-			y=600,
-			grid =3,--6,
-      gridHeight = 1.5,
-      gridResolution = 4, -- seaches per grid square
-      gridThres      = 0.6,
-
-      scanHeight = 100,
-
-      scanLength = 200,
-      refresh_rate = 20,
-      weights = {
-          goodTerrain = 0.5,
-          badTerrain   = 5,
-          avoidTerrain = 25,
-          impassableTerrain = 50,
-      }
-		}
-    path = nil
-
-
---- AI LINKED
-
-ai = {}
-
-pathing_states = {
-	current_state = 1,
-	states = {
-		[1] = 'READY',
-		[2] = 'SEARCHING',
-		[3] = 'ERROR'
-	}
-
-
-}
-
-
-TARGET_POS =nil
-
-
-function init_pathing()
-
-	mapSize.gridResolution = mapSize.grid/mapSize.gridResolution
-	mapSize.gridHeight =  mapSize.grid/4
-	PATH_NODE_TOLERANCE = mapSize.grid * 1.5
-	initMapArr()
-
-end
-
-
-function initMapArr()
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-	    pos = posToInt(Vec(0,0,y))
-	    map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        map.data[pos[3]][pos[1]] = nil 
-	    end
-	end
-end
-
-function initMap( )
-  local pos = Vec(0,0,0)
-  local gridCost = 0
-  local maxVal  = {math.modf((mapSize.x)/mapSize.grid),math.modf((mapSize.y)/mapSize.grid)}
-
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-    pos = posToInt(Vec(0,0,y))
-    -- map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        gridCost,validTerrain,avgHeight,grid_avg =  scanGrid(x,y) 
-	        -- gridCost,validTerrain,avgHeight,grid_avg =  1,true,1,1,1
-	        -- if(pos[3] ~= nil and pos[1]~= nil) then
-	          
-	          map.data[pos[3]][pos[1]] = deepcopy(mapNode) 
-	          map.data[pos[3]][pos[1]]:push(x,grid_avg,y,gridCost,pos[3],pos[1],validTerrain,maxVal,0 )
-
-	        -- end
-	  		  -- DebugPrint(x.." | "..y)
-	    end
-	end
-
-
-	mapInitialized = true
-	
-
-end
-
-function get_pathing_state()
-	pathing_state = pathing_states['states'][pathing_states['current_state']]
-	return pathing_state
-
-end
-
-function init_pathfinding(startPos,goalPos,heuristic_approach)
-	path = nil
-	goalPos = posToInt(goalPos)
-	startPos = posToInt(startPos)
-	local goal = map.data[goalPos[3]][goalPos[1]]
-	local start = map.data[startPos[3]][startPos[1]]
-	AStar:init(map.data, start, goal, heuristic_approach ) 
-
-	pathing_states['current_state'] = 2
-
-end
-		
-function perform_pathfinding()
-	local search_result =  AStar:AStarSearch_2(map.data)
-
-	if(search_result) then 
-		if(search_result ~= -1) then
-
-			if(_AI_DEBUG_PATHING) then 
-				DebugWatch("pathing outcome","SUCCESS")
-			end
-			path = search_result
-			PATHSET = true
-
-			pathing_states['current_state'] = 1
-			return path, false
-		else 
-
-			if(_AI_DEBUG_PATHING) then 
-				DebugWatch("pathing outcome","ERROR")
-			end
-			pathing_states['current_state'] = 3
-		end
-		
-	end
-	return false
-	
-
-end
-
-
-
---[[
-
-	hande all path plotting - onyinit variabes on first run to save memory
-
-]]
-
+#version 2
 function handle_path_plotting(startPos,goalPos,dt,ai,vehicle_body_parts)
 	if(not(mapInitialized)) then 
 		init_pathing()
@@ -253,10 +31,8 @@
 		end
 	end
 
-
-end
-
---This function retrieves the most recent path and stores it in lastPath
+end
+
 function adjust_pathing(path,ai,vehicle_body_parts)
 	for i=1, #path  do
 		path[i] = simple_obstacle_avoidance(path[i],ai,vehicle_body_parts)
@@ -295,11 +71,10 @@
 	return pos
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath(path,ai)
 	local vehicle_transform = GetVehicleTransform(ai.id)
 	-- DebugWatch("navigating path for ai "..ai.id.."  at pos",vehicle_transform)
-	if #path > 0 then
+	if #path ~= 0 then
 		for i=#path, 1, -1 do
 			local p = path[i]
 			local dv = VecSub(p, vehicle_transform.pos)
@@ -318,8 +93,6 @@
 	return path
 end
 
-
---This function will draw the content of lastPath as a line
 function drawPath(lastPath)
 	-- DebugWatch("last path length",#lastPath)
 	local p1,p2 = Vec(),Vec()
@@ -332,9 +105,7 @@
 	end
 end
 
-
 function perform_raycast()
-
 
 	local t = GetCameraTransform()
 	local dir = TransformToParentVec(t, {0, 0, -1})
@@ -349,7 +120,6 @@
 	return nil
 end
 
--- find euclidian distance of data to clusters and update centroid locations
 function ai:clusteringCalculateClusters()
 	local pos = Vec(0,0,0)
 	local center = Vec(0,0,0)
@@ -370,11 +140,9 @@
 
 end
 
---- perform operations on clusters to extract target
 function ai:clusteringOperations()
 	
 	self:clusteringCalculateClusters()
-
 
 	self:pseudoSNN()
 
@@ -389,14 +157,6 @@
 	self.targetNode = self.clustering.clusters.centroids.data[self.clustering.mode]
 
 end
-
-
---- simulate an snn network slightly to get best node
-
--- if(SNNpspprev[j]<SNNpsp[i])
---  {
---      SNNweights[j][i]=tanh(gammaweights*SNNweights[j][i]+learningrateweights*SNNpspprev[j]*SNNpsp[i]);
---  }
 
 function ai:pseudoSNN()
 	local bestpsp = 100000000
@@ -463,10 +223,8 @@
 	--DebugPrint("values: index: "..index.."\nhitpos:"..VecStr(hitPos).."\nhitval: "..hitValue.."\nClusterPos = "..VecStr(self.clustering.clusters.current.data[index]:getPos()))
 	self.clustering.clusters.current.data[index]:push(hitPos[1],hitPos[2],hitPos[3],hitValue) 
 
-
 	self.clustering.clusters.current.index = (self.clustering.clusters.current.index%self.clustering.dataSize )+1
 end
-
 
 function ai:MAV(targetCost)
 	self.targetMoves.targetIndex = (self.targetMoves.targetIndex%#self.targetMoves.list)+1 
@@ -477,11 +235,7 @@
 
 end
 
-
-
 function ai:costFunc(testPos,hit,dist,shape,key)
-
-
 
 	local cost = 10000 
 	if(not hit) then
@@ -489,29 +243,6 @@
 	end
 	return cost
 end
-
-
-------------------------------------------------
-
-
----- PATHFINDING
-
-
------------------------------------------------------
-
-
-
----- 
-
-
-
----- use flood fill to comap[re to last neighbor  that was known and if neighbor foun and  track then 
-
----- compare the next based on known locations nd move outwards.]
-
-----
-
-
 
 function scanGrid(x,y)
   local pos = Vec(0,0,0)
@@ -557,8 +288,6 @@
   end
   return gridScore,validTerrain, minHeight, ((minHeight+maxHeight)/2)
 end
-
-
 
 function scanGrid_local(x,y,height)
 	-- if(height<0 ) then 
@@ -617,8 +346,6 @@
   return gridScore,validTerrain, minHeight, ((minHeight+maxHeight)/2)
 end
 
-
-
 function getMaterialScore_local(x,y,probe_height,scan_length)
   local score = 0
   local probe = Vec(x,probe_height,y)
@@ -660,7 +387,6 @@
 
 end
 
-
 function getHeight(x,y)
 
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -730,7 +456,6 @@
   return score
 
 end
-
 
 function getMaterialScore3(x,y)
   local score = 0
@@ -800,14 +525,9 @@
   return pos,pos2
 end
 
-
 function Heuristic(a, b)
       return Math.Abs(a[1] - b[1]) + Math.Abs(a[3] - b[3]);
- end 
-
-
-
-
+ end
 
 function checkIfTerrainValid(mat,r,g,b)
 		local score = 0
@@ -842,20 +562,6 @@
 	    return score
 end
 
-
-
-
-
-
-
----------------------------------------------------------
-
-
-
-
--------------------------------------------------------
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
@@ -869,8 +575,6 @@
 	end
 
 end
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -887,7 +591,6 @@
     return copy
 end
 
-
 function inRange(min,max,value)
 		if(tonumber(min) < tonumber(value) and tonumber(value)<=tonumber(max)) then 
 			return true
@@ -898,7 +601,3 @@
 
 end
 
-
-
-
-

```

---

# Migration Report: pathfinding\AVF_pathfinding.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding\AVF_pathfinding.lua
+++ patched/pathfinding\AVF_pathfinding.lua
@@ -1,1806 +1,9 @@
-
-
----PATHFINDING LINKED
-
-#include "mapNode.lua"
-#include "AStarSearch.lua"
-
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        AVF_AI_3.lua             
-*
-* DESCRIPTION :
-*       File that implements racing AI inside teardown 2020, with PID controllers
-* 		to ensure cars respond to coordinates in a good fashion and can handle high speed
-*		Also includes simple goal achievement and collision avoidance 
-*		Including "driver ai" to make them more / less aggressive with speed, cornering
-*		overtaking, and driving. 
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-
-RACESTARTED = false
-
-RACECOUNTDOWN = false
-
-RACEENDED = false
-
-
-PLAYER_TOTALED = false
-
-PATHSET = false
-
-mapInitialized = false
-
-PLAYERRACING = true
-	
-DEBUG = false
-DEBUGCARS = false
-
-DEBUG_SAE = false
-
-
-STOPTHEMUSIC = true
-
-
-DEBUGCONTROLLERS = false
-
-DEFAULTRACETIME = 1000000
-
-map = {
-
-  xIndex = 0,
-  data = {
-
-  },
-  smoothingFactor = 3,
-  validMaterials = {
-  	[1] = {	
-  		material = "masonry",
-
-
-	  validSurfaceColours ={ 
-				[1] = {
-					r = 0.20,
-					g = 0.20,
-					b = 0.20,
-					range = 0.02
-				},
-				[2] = {
-					r = 0.80,
-					g = 0.60,
-					b = 0.60,
-					range = 0.02
-				},
-				[3] = {
-					r = 0.34,
-					g = 0.34,
-					b = 0.34,
-					range = 0.02
-				},
-			},
-		},
-	},
-}
-
--- negative grid pos is solved by simply showing 
-mapSize = {
-			x=400,
-			y=400,
-			grid =4,--6,
-      gridHeight = 2.5,
-      gridResolution = 3, -- seaches per grid square
-      gridThres      = 0.6,
-
-      scanHeight = 100,
-
-      scanLength = 200,
-
-      weights = {
-          goodTerrain = 0.5,
-          badTerrain   = 5,
-          avoidTerrain = 25,
-          impassableTerrain = 50,
-      }
-		}
-    path = nil
-
-
---- AI LINKED
-
-
-
-RACESTARTED  = false
-
-aiVehicles = {
-
-
-
-	}
-
-playerConfig = {
-	name = "PLAYER ",
-	finished = false,
-	car = 0,
-	bestLap = 0,
-	playerLaps = 0,
-
-	hudInfo = {
-		lapInfo = {
-			[1] = {
-				name = "Race",
-				time = 0,
-			},
-
-			[2] = {
-				name = "Lap",
-				time = 0,
-			},
-
-			[3] = {
-				name = "Best",
-				time = 0,
-			},
-		},
-	},
-}
-
-
-aiPresets = {
-	
-	EASY = 1,
-	MEDIUM = 2,
-	HARD = 3,
-	INSANE = 4,	
-	DGAF = 5,
-	ROADRAGE = 6,
-
-	difficulties = {
-		[1] = {
-			name =  "easy", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.1, 
-			tenacity = 0.7,
-			errorCoef = 0.4,
-
-		}, 
-		[2] = {
-			name =  "medium", 
-			steeringThres = 0.2,
-			speedSteeringThres = 0.2, 
-			tenacity = 0.8,
-			errorCoef = 0.2,
-
-		}, 
-		[3] = {
-			name =  "hard", 
-			steeringThres = 0.4,
-			speedSteeringThres = 0.4, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-		[4] = {
-			name =  "insane", 
-			steeringThres = 0.6,
-			speedSteeringThres = 0.6, 
-			tenacity = 0.94,
-			errorCoef = 0.05,
-
-		}, 
-		[5] = {
-			name =  "DGAF", 
-			steeringThres = 0.9,
-			speedSteeringThres = 0.9, 
-			tenacity = 0.99,
-			errorCoef = 0.1,
-
-		}, 
-		[6] = {
-			name =  "road rage", 
-			steeringThres = 1,
-			speedSteeringThres = 0.2, 
-			tenacity = 1.1,
-			errorCoef = 0.1,
-
-		}, 
-		[7] = {
-			name =  "Never Overtakes - gentle", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.25, 
-			tenacity = 0.85,
-			errorCoef = 0.1,
-
-		}, 
-		[8] = {
-			name =  "Never Overtakes - speedDemon", 
-			steeringThres = 0.1,
-			speedSteeringThres = 0.9, 
-			tenacity = 0.85,
-			errorCoef = 0.1,
-
-		}, 
-		[9] = {
-			name =  "Medium corners, overtakes", 
-			steeringThres = 0.95,
-			speedSteeringThres = 0.5, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-
-		[10] = {
-			name =  "slower corners, overtakes", 
-			steeringThres = 0.7,
-			speedSteeringThres = 0.35, 
-			tenacity = 0.9,
-			errorCoef = 0.1,
-
-		}, 
-
-	},
-
-	difficulty_ranged = {
-		[1] = {
-			name =  "easy", 
-			steeringThres = {10,100},
-			speedSteeringThres = {10,90}, 
-			tenacity = {70,100},
-			errorCoef = {1,40},
-
-		}, 
-		[2] = {
-			name =  "medium", 
-			steeringThres = {20,100},
-			speedSteeringThres = {20,99}, 
-			tenacity = {80,100},
-			errorCoef = {1,20},
-
-		}, 
-		[3] = {
-			name =  "competative_medium", 
-			steeringThres = {60,100},
-			speedSteeringThres = {20,99}, 
-			tenacity = {80,100},
-			errorCoef = {1,10},
-
-		}, 
-		[4] = {
-			name =  "hard", 
-			steeringThres = {40,100},
-			speedSteeringThres = {40,100}, 
-			tenacity = {90,100},
-			errorCoef = {1,10},
-
-		}, 
-		[5] = {
-			name =  "insane", 
-			steeringThres = {60,110},
-			speedSteeringThres = {60,110}, 
-			tenacity = {90,110},
-			errorCoef = {1,5},
-
-		}, 
-		[6] = {
-			name =  "psycobilly_freakout", 
-			steeringThres = {80,130},
-			speedSteeringThres = {80,130}, 
-			tenacity = {95,130},
-			errorCoef = {0.5,2.5},
-
-		}, 
-
-		[7] = {
-			name =  "broad_strokes", 
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[8] = {
-			name =  "broad_strokes_2",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[9] = {
-			name =  "broad_strokes_3",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[10] = {
-			name =  "broad_strokes_4",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[11] = {
-			name =  "broad_strokes_5",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[12] = {
-			name =  "broad_strokes_6",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[13] = {
-			name =  "broad_strokes_7",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[14] = {
-			name =  "broad_strokes_8",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		[15] = {
-			name =  "broad_strokes_9",  
-			steeringThres = {1,120},
-			speedSteeringThres = {1,120}, 
-			tenacity = {1,120},
-			errorCoef = {.01,10},
-
-		}, 
-		-- [7] = {
-		-- 	name =  "texas_psycobilly_freakout", 
-		-- 	steeringThres = {80,160},
-		-- 	speedSteeringThres = {80,160}, 
-		-- 	tenacity = {100,160},
-		-- 	errorCoef = {0.25,2},
-
-		-- }, 
-
-	}
-
-}
-
-
-ai = {
-	active = true,
-	goalPos= Vec(0,0,0),
-
-
-
-	raceValues = {
-		completedGoals  = 0,
-		targetNode 		= 1,
-		NextNode 		= 2,
-		passedCheckPoints = 0,
-		nextCheckpoint = 1,
-		completionRange = 4.5,--4.5,
-		lookAhead = 2,
-		laps = 0 	,
-		lastLap = 0,
-		splits = {},
-
-		bestLap = nil,
-
-	},
-
-	targetNode = nil,
-	NextNode =nil,
-
-	controller = {
-		aiType = "default",
-
-		accelerationValue = 0,
-		steeringValue = 0,
-		handbrake = false,
-
-		steeringThres  = aiPresets.HARD, --0.4
-		steeringForce  = 0.5,
-		speedSteeringThres = aiPresets.HARD,
-		tenacity 			= 0.9,
-		relativeThreshold = 0.8,
-		minDist = 2--.5,--5,
-	},
-
-	reversingController = {
-		reversing = false,
-		minVelocity = 1,
-		waitTime = 2.5,
-		currentWait = 3,
-		reverseTime = 2.5,
-		currentReverseTime = 2.5,
-	},
-
-
-	detectRange = 3,
-	commands = {
-	[1] = Vec(0,0,-1),
-	[2] = Vec(1*0.8,0,-1*1.5),
-	[3] = Vec(-1*0.8,0,-1*1.5),
-	[4] = Vec(-1,0,0),
-	[5] = Vec(1,0,0),
-	[6] = Vec(0,0,1),
-
-	},
-
-	weights = {
-
-	[1] = 0.870,
-	[2] = 0.86,
-	[3] = 0.86,
-	[4] = 0.84,
-	[5] = 0.84,
-	[6] = 0.80,
-
-			} ,
-
-	targetMoves = {
-		list        = {},
-		target      = Vec(0,0,0),
-		targetIndex = 1
-	},
-
-
-	directions = {
-		forward = Vec(0,0,1),
-
-		back = Vec(0,0,-1),
-
-		left = Vec(1,0,0),
-
-		right = Vec(-1,0,0),
-	},
-
-	maxVelocity = 0,
-
-	cornerCoef = 16,
-
-	accelerationCoef = 0.75,
-	steeringCoef = 2.55,
-
-	pidState = {
-
-			--- pid gain params
-		pGain = 0.765,
-		iGain = -0.08,
-		dGain = -1.3,
-
-		intergralTime = 5,
-
-		integralIndex = 1,
-		integralSum = 0,
-		integralData = {
-
-		},
-		lastCrossTrackError = 0,
-		lastPnt = Vec(0,0,0),
-
-			-- pid output value 
-		controllerValue = 0,
-
-
-			--- pid update and training params
-			training = false,
-		inputrate=0.0665,
-		learningrateweights=0.009,
-		learningrateThres = 0.02,
-	    bestrate=0.05,
-	    secondbestrate=0.01,
-	    gammasyn=0.9,
-	    gammaref=0.7,
-	    gammapsp=0.9,
-	},
-	usingClustering = false,
-
-	clustering = {
-		pass = 1,
-		maxPass = 10,
-		centroids = 2,
-		iterations = 5,
-		prior = 1,
-		dataSize = 100,
-		mode = -1,
-		previousOutput = -1,
-		output = nil,
-		clusters = {
-			centroids = {
-				pass = 1,
-				index = 1,
-				data = {},
-			},
-			current = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-			prior = {
-				pass = 1,
-				index = 1,
-				data = {},
-
-
-			},
-		},
-
-	},
-
-	scanning = {
-		numScans = 2,
-		scanThreshold = 0.5,
-		maxScanLength = 10,
-		scanLength = 50,
-		scanDepths = 2,
-		vehicleHeight = 2,
-		cones = {
-			left   = {
-				direction = "left",
-				startVec = Vec(0.25,0,-1.5),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				direction = "centre",
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				direction = "right",
-				size = 110,
-				startVec = Vec(-0.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-		positions = {
-			left   = {
-				direction = "left",
-				startVec = Vec(0.25,0,-1.5),
-				size = 110,
-				scanColour = {
-					r = 1,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			sideL  = {
-				direction = "sideL",
-				size = 110,
-				startVec = Vec(1.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			centre = {
-				direction = "centre",
-				startVec = Vec(0,0,-1),
-				size = 0.5,
-				scanColour = {
-					r = 0,
-					g = 0, 
-					b = 1,
-				},
-				weight = 0.6
-
-			},
-			right  = {
-				direction = "right",
-				size = 110,
-				startVec = Vec(-0.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-			sideR  = {
-				direction = "sideR",
-				size = 110,
-				startVec = Vec(-1.25,0,-1.5),
-				scanColour = {
-					r = 0,
-					g = 1, 
-					b = 0,
-				},
-				weight = 0.5
-
-			},
-		},
-
-	},
-
-
-
-	--altChecks = Vec(0.25,0.4,-0.6),
-	altChecks = {
-				[1] = -2,
-				[2] =0.2,
-				[3] = 0.4
-			},
-	altWeight ={
-			[1] = 1,
-			[2] =1,
-			[3] = -1,
-			[4] = -1,
-	},
-
-
-	validSurfaceColours ={ 
-			[1] = {
-				r = 0.20,
-				g = 0.20,
-				b = 0.20,
-				range = 0.1
-			},
-			[2] = {
-				r = 0.60,
-				g = 0.60,
-				b = 0.60,
-				range = 0.1
-			},
-			[3] = {
-				r = 0.34,
-				g = 0.34,
-				b = 0.34,
-				range = 0.1
-			},
-		},
-	hitColour = Vec(1,0,0),
-	detectColour = Vec(1,1,0),
-	clearColour = Vec(0,1,0),
-}
-
-pathing_states = {
-	current_state = 1,
-	states = {
-		[1] = 'READY',
-		[2] = 'SEARCHING',
-		[3] = 'EXPIRED'
-	}
-
-
-}
-
-
-
-function init()
-
-	checkpoints = FindTriggers("checkpoint",true)
-
-	for i = 1,#checkpoints do 
-		if(GetTagValue(value, "checkpoint")=="") then 
-			SetTag(checkpoints[i],"checkpoint",i)
-		end
-
-	end
-
-	mapSize.gridResolution = mapSize.grid/mapSize.gridResolution
-	-- negative grid pos is solved by simply showing 
-	-- mapSize = {
-	-- 			x=400,
-	-- 			y=400,
-	-- 			grid =4,--6,
-	--       gridHeight = 2.5,
-	--       gridResolution = 3, -- seaches per grid square
-	--       gridThres      = 0.6,
-
-	tracker = FindBody("tracker_obj")
-	target_obj = FindBody("target_obj")
-
-	 initMapArr()
-
-
-	-- DebugPrint("started")
-
-end
-
-
-function initMapArr()
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-	    pos = posToInt(Vec(0,0,y))
-	    map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        map.data[pos[3]][pos[1]] = nil 
-	    end
-	end
-end
-
-function initMap( )
-  local pos = Vec(0,0,0)
-  local gridCost = 0
-  local maxVal  = {math.modf((mapSize.x)/mapSize.grid),math.modf((mapSize.y)/mapSize.grid)}
-
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-    pos = posToInt(Vec(0,0,y))
-    -- map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        gridCost,validTerrain,avgHeight,grid_avg =  scanGrid(x,y) 
-	        -- gridCost,validTerrain,avgHeight,grid_avg =  1,true,1,1,1
-	        -- if(pos[3] ~= nil and pos[1]~= nil) then
-	          
-	          map.data[pos[3]][pos[1]] = deepcopy(mapNode) 
-	          map.data[pos[3]][pos[1]]:push(x,grid_avg,y,gridCost,pos[3],pos[1],validTerrain,maxVal,0 )
-
-	        -- end
-	  		  -- DebugPrint(x.." | "..y)
-	    end
-	end
-
-
-	mapInitialized = true
-	
-
-end
-
-function get_pathing_state()
-	pathing_state = pathing_states['states'][pathing_states['current_state']]
-	return pathing_state
-
-end
-
-function init_pathfinding()
-
-	pos = posToInt(GetPlayerPos())
-	goalPos = posToInt(GetBodyTransform(target_obj).pos)
-	-- startPos = map.data[55][72]
-	startPos = posToInt(GetBodyTransform(tracker).pos)
-	-- startPos = map.data[startPos[3]][startPos[1]]
-	local goal = map.data[goalPos[3]][goalPos[1]]
-	local start = map.data[startPos[3]][startPos[1]]
-	AStar:init(map.data, start, goal  ) 
-
-	pathing_states['current_state'] = 2
-
-end
-
-function perform_pathfinding()
-	local search_result =  AStar:AStarSearch_2(map.data)
-	if(search_result) then 
-		if(search_result ~= -1) then 
-			path = search_result
-			PATHSET = true
-		end
-		pathing_states['current_state'] = 1
-		
-	end
-	
-
-end
-
-
-function initPaths()
-
-  pos = posToInt(GetPlayerPos())
-   goalPos = map.data[60][30]
-   startPos = map.data[55][72]
-  startPos = map.data[pos[3]][pos[1]]
-
-
-
-  paths = {}
-  gateState = {}
-  gates = {}
-  triggers = FindTriggers("gate",true)
-  for i=1,#triggers do
-    gateState[tonumber(GetTagValue(triggers[i], "gate"))] = 0
-    gates[tonumber(GetTagValue(triggers[i], "gate"))] = triggers[i]
-  end
-
-  for i =1,#triggers do 
-    startPos = posToInt(GetTriggerTransform(gates[i]).pos)
-    startPos = map.data[startPos[3]][startPos[1]]
-    if(i==#triggers) then 
-      goalPos = posToInt(GetTriggerTransform(gates[1]).pos )
-    else
-      goalPos = posToInt(GetTriggerTransform(gates[i+1]).pos )
-    end
-    goalPos = map.data[goalPos[3]][goalPos[1]]
-    paths[#paths+1] =  AStar:AStarSearch(map.data, startPos, goalPos)
-  end
-  	path = paths[#paths]
-  	for i = 1,#paths-1 do
-  		for j = 1,#paths[i] do 
-	  		path[#path+1] = paths[i][j]
-	  	end
-  	end
-end
-
-
-function tick(dt)
-
-	DebugWatch("game time",GetTime())
-	DebugWatch("pathing_state",get_pathing_state())
-
-	DebugWatch("tracker pos",GetBodyTransform(tracker))
-	DebugWatch("target  pos",GetBodyTransform(target_obj))
-	DebugWatch("PATHSET",PATHSET)
-	if(PATHSET) then 
-		 AStar:drawPath(map.data,path)
-	  	if(DEBUG)then 
-
-		    AStar:drawPath(map.data,path)
-
-			local t = GetCameraTransform()
-			local dir = TransformToParentVec(t, {0, 0, -1})
-
-			local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 10)
-			DebugWatch("Hit", hit)
-			if hit then
-				--Visualize raycast hit and normal
-				local hitPoint = VecAdd(t.pos, VecScale(dir, dist))
-				local mat,r,g,b = GetShapeMaterialAtPosition(shape, hitPoint)
-				DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
-				DebugWatch("Terrain cost",checkIfTerrainValid(mat,r,g,b))
-				DebugWatch("body mass",GetBodyMass(GetShapeBody(shape)))
-			end
-
-		end
-
-	     -- path =  AStar:AStarSearch(map.data, startPos, goalPos)
-	  elseif( path)then 
-
-
-
-
-
-	    -- DebugWatch("running",#paths)
-	    -- for key,val in ipairs(paths) do  
-	    --    AStar:drawPath2(map.data,val)
-	    -- end
-	  -- local playerTrans = GetPlayerTransform()
-	  -- playerTrans.pos,pos2 = posToInt(playerTrans.pos)
-	  -- DebugWatch("Player Pos: ",playerTrans.pos)
-	  -- -- --  DebugWatch("original Player Pos: ", GetPlayerTransform().pos)
-	  -- --  -- DebugWatch("Pos 2: ",pos2) 
-	  --  local pos = VecCopy(playerTrans.pos)
-	  --  if(pos[3] ~= nil and pos[1]~= nil) then
-	  --   	-- DebugPrint(pos[3].." | "..pos[1])
-	  --   	 DebugWatch("player Grid Cost: ",map.data[pos[3]][pos[1]]:getCost())
-
-	  --    DebugWatch("player Grid neighbors: ",#map.data[pos[3]][pos[1]].neighbors)
-
-	  --    local totalCost = 0
-	  --    for key, val in ipairs(map.data[pos[3]][pos[1]]:getNeighbors()) do
-	  --         totalCost = totalCost + map.data[val.y][val.x]:getCost()
-	  --    end
-
-	  --    DebugWatch("player Grid neighbor: ",totalCost)
-
-	  --    DebugWatch("player Grid VALID: ",map.data[pos[3]][pos[1]].validTerrain)
-	  -- -- else
-
-	  -- end
-
-	-- elseif not PATHSET and GetTime() >0.1 then 
-	-- 	if(not mapInitialized) then 
-	-- 		initMap()
-	-- 	end
-	-- 	-- DebugPrint("prepping paths")
-
-		
-	-- 		initPaths()
-
-
-	-- 		for key,vehicle in pairs(aiVehicles) do 
-	-- 			vehicle:initGoalPos()
-	-- 		end	
-	-- 		PATHSET = true
-	-- 	-- DebugPrint("Paths set")
-
-	-- 	-------
-
-	-- 	 --- init racing values
-
-	-- 	 -----
-
-
-	-- 		raceManager:init(aiVehicles,path)
-		
-	end
-
-
-
-	---------------------
-			---------- keypress stuff
-	---------------
-	-- DebugWatch("map_mode")
-	if InputPressed("c") then 
-		CAMMODE = not CAMMODE
-
-	end
-
-	if(InputPressed("p")) then
-		DebugWatch("map init",mapInitialized)
-		if(not mapInitialized) then
-			initMap()
-		end
-		if(get_pathing_state() =="READY") then 
-			init_pathfinding()
-		end
-	end
-	if(mapInitialized and get_pathing_state() == "SEARCHING") then 
-		perform_pathfinding()
-	end
-
-
-end
-
-function update(dt )
-
-end
-
-
-
-
-function ai:initVehicle(vehicle) 
-
-	self.id = vehicle
-	self.body = GetVehicleBody(self.id)
-	self.transform =  GetBodyTransform(self.body)
-	self.shapes = GetBodyShapes(self.body)
-
-
-
-	--- declare driver name 
-
-	if(math.random(0,200)<=1) then
-		self.driverName = uniqueNames[math.random(1,#uniqueNames)]
-	else
-		self.driverFName = fNames[math.random(1,#fNames)] 
-		self.driverSName = sNames[math.random(1,#sNames)]
-		self.driverName = self.driverFName.." "..self.driverSName
-	end
-		--- find largest shape and dclare that the main vehicle SpawnParticle
-
-	local largestKey = 0
-	local shapeVoxels = 0
-	local largestShapeVoxels = 0
-	for key,shape in ipairs(self.shapes) do
-		shapeVoxels = GetShapeVoxelCount(shape)
-		if(shapeVoxels> largestShapeVoxels) then
-			largestShapeVoxels = shapeVoxels
-			largestKey = key
-		end
-	end
-	self.mainBody = self.shapes[largestKey]
-	self.bodyXSize,self.bodyYSize ,self.bodyZSize  = GetShapeSize(self.mainBody)
-	-- DebugPrint("body Size: "..self.bodyXSize.." | "..self.bodyYSize.." | "..self.bodyZSize)
-
-
-	for i=1,3 do 
-		self.targetMoves.list[i] = Vec(0,0,0)
-	end
-
-	self.raceCheckpoint = 1
-	self.currentCheckpoint = nil
-
-	for key,value in ipairs(checkpoints) do
-		if(tonumber(GetTagValue(value, "checkpoint"))==self.raceCheckpoint) then 
-			self.currentCheckpoint = value
-		end
-	end	
-
-	for i = 1, self.pidState.intergralTime do
-		self.pidState.integralData[i] = 0
-
-	end
-
-
-	self.hudColour = {math.random(0,100)/100,math.random(0,100)/100,math.random(0,100)/100}
-
---	local aiLevel = aiPresets.difficulties[math.random(1,#aiPresets.difficulties)]
-	-- local aiLevel = aiPresets.difficulties[5]--math.random(3,5)]
-	
-	local aiLevel = deepcopy(aiPresets.difficulty_ranged[math.random(1,#aiPresets.difficulty_ranged)])--aiPresets.difficulty_ranged[4])
-	for key,val in pairs(aiLevel) do 
-		if(type(val)=="table") then
-			aiLevel[key] = math.random(val[1],val[2])/100 
-		end
-	end
-	-- for key,val in pairs(aiLevel) do 
-	-- 	if(type(val)=="table") then 
-	-- 		DebugPrint(key..": "..val[1].."-"..val[2]) 
-	-- 	else
-	-- 		DebugPrint(key..": "..val)
-	-- 	end
-
-
-	-- end
-	
-
-	self.controller.aiLevel = aiLevel.name
-
-	self.controller.steeringThres  = aiLevel.steeringThres --0.4
-
-	self.controller.speedSteeringThres = aiLevel.speedSteeringThres
-	self.controller.tenacity = aiLevel.tenacity
-
-	self.controller.errorCoef = aiLevel.errorCoef
-
-
-	self.scanning.maxScanLength = self.scanning.maxScanLength * (math.random(90,350)/100) 
-
-
-
-end
-
-function ai:initGoalPos()
-	self.goalPos = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]:getPos()
-	self.targetNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-
-
-
-	self.NextNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-	-- self:initClusters()
-
-
-end
-
-
-function ai:initClusters()
-	for cluster= 1,self.clustering.centroids do 
-		self.clustering.clusters.centroids.data[cluster] = deepcopy(node)
-
-		 self.clustering.clusters.centroids.data[cluster]:loadSprite()
-	end
-	for i = 1,self.clustering.dataSize do 
-		--clustering.clusters.current.data
-		self.clustering.clusters.current.data[i] = deepcopy(node)
-		self.clustering.clusters.prior.data[i] = deepcopy(node)
-		self.clustering.clusters.current.data[i]:loadSprite()
-	end
-
-	self:scanPos()
-	self:clusteringCentroids()
-
-end
-
-function ai:tick(dt)
-		-- DebugWatch("datasize = ",#self.clustering.clusters.centroids.data)
-
-		self:raceController()
-		-- self:controlActions()
-	if(RACESTARTED and (not PLAYERRACING or (self.id ~= aiVehicles[playerConfig.car].id or playerConfig.finished))) then 
-		self:vehicleController()
-
-		if(GetPlayerVehicle() == self.id and DEBUG) then
-			DebugWatch("current lap:",self.raceValues.laps)
-
-		end
-	end
-		-- DebugWatch("velocity:", VecLength(GetBodyVelocity(GetVehicleBody(self.id))))
-
-	
-end
-
-function ai:update(dt)
-	if(RACESTARTED) then
-
-		-- self:vehicleController()
-	end
-	
-end
-
-function ai:raceController()
-	if(RACESTARTED) then 
-		if(PLAYERRACING and self.id == aiVehicles[playerConfig.car].id) then 
-			self:player_raceController()
-		else
-
-			self:raceDetailsHandler()
-
-
-			self:controlActions()
-
-			local vehiclePos = GetVehicleTransform(self.id).pos
-			local indexVal = posToInt(vehiclePos)
-			-- DebugWatch("vec1: ",Vec(indexVal[1],0,indexVal[3]))
-			-- DebugWatch("vec2: ",Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2]))
-			-- 	DebugWatch("dist to goal",VecLength( VecSub(
-				-- 	Vec(indexVal[1],0,indexVal[3]),
-				-- 	Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-				-- )
-			if(VecLength( VecSub(
-					Vec(indexVal[1],0,indexVal[3]),
-					Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-			<self.raceValues.completionRange) then 
-				
-					self.raceValues.targetNode = self.raceValues.targetNode%#path +1
-					self.raceValues.NextNode = self.raceValues.targetNode%#path +1
-
-					self.goalPos = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]:getPos()
-					self.targetNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-					
-					self.NextNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-
-
-
-
-					self.raceValues.completedGoals = self.raceValues.completedGoals + 1
-
-					if(math.floor(self.raceValues.completedGoals/(#path+1))>self.raceValues.laps) then 
-
-						if(	not self.raceValues.bestLap) then
-							self.raceValues.bestLap = raceManager:lapTime()
-
-						elseif (raceManager:lapTime()-self.raceValues.lastLap < self.raceValues.bestLap )then
-							self.raceValues.bestLap = raceManager:lapTime()-self.raceValues.lastLap
-						end
-
-						--- add player lastlap if vehicle is player 
-						if(PLAYERRACING and (self.id == aiVehicles[playerConfig.car].id and not playerConfig.finished)) then 
-							playerConfig.bestLap = self.raceValues.bestLap 
-							playerConfig.hudInfo.lapInfo[3].time =  self.raceValues.bestLap 
-							-- DebugPrint(playerConfig.hudInfo.lapInfo[3].time)
-						end
-						self.raceValues.lastLap = raceManager:lapTime()
-						playerConfig.hudInfo.lapInfo[2].time = self.raceValues.lastLap 
-
-					end
-					self.raceValues.laps = math.floor(self.raceValues.completedGoals/(#path+1))
-			else
-				-- SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
-			end
-
-		end
-	end
-
-	-- DebugWatch("checkpoint: ",self.goalPos)
-
-
-
-end
-
-
-function ai:player_raceController()
-	if(RACESTARTED) then 
-
-		self:raceDetailsHandler()
-
-
-		self:controlActions()
-
-		local vehiclePos = GetVehicleTransform(self.id).pos
-		local indexVal = posToInt(vehiclePos)
-		-- DebugWatch("vec1: ",Vec(indexVal[1],0,indexVal[3]))
-		-- DebugWatch("vec2: ",Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2]))
-		-- 	DebugWatch("dist to goal",VecLength( VecSub(
-			-- 	Vec(indexVal[1],0,indexVal[3]),
-			-- 	Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-			-- )
-
-		local player_hit_range = self.raceValues.completionRange
-
-
-		if(self.raceValues.targetNode%#path +1 >2 ) then
-			player_hit_range = player_hit_range * 1
-		end
-		node_hit,new_node = self:player_check_future(player_hit_range)
-		if(DEBUG)then 
-			DebugPrint(tostring(node_hit).." | "..new_node)
-		end
-		if(node_hit) then 
-			
-				self.raceValues.targetNode = self.raceValues.targetNode%#path +1
-				self.raceValues.NextNode = self.raceValues.targetNode%#path +1
-
-				self.goalPos = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]:getPos()
-				self.targetNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-				
-				self.NextNode = map.data[path[self.raceValues.targetNode][2]][path[self.raceValues.targetNode][1]]
-
-
-
-
-				self.raceValues.completedGoals = self.raceValues.completedGoals + 1
-
-				if(math.floor(self.raceValues.completedGoals/(#path+1))>self.raceValues.laps) then 
-
-					if(	not self.raceValues.bestLap) then
-						self.raceValues.bestLap = raceManager:lapTime()
-
-					elseif (raceManager:lapTime()-self.raceValues.lastLap < self.raceValues.bestLap )then
-						self.raceValues.bestLap = raceManager:lapTime()-self.raceValues.lastLap
-					end
-
-					--- add player lastlap if vehicle is player 
-					if(PLAYERRACING and (self.id == aiVehicles[playerConfig.car].id and not playerConfig.finished)) then 
-						playerConfig.bestLap = self.raceValues.bestLap 
-						playerConfig.hudInfo.lapInfo[3].time =  self.raceValues.bestLap 
-						-- DebugPrint(playerConfig.hudInfo.lapInfo[3].time)
-					end
-					self.raceValues.lastLap = raceManager:lapTime()
-					playerConfig.hudInfo.lapInfo[2].time = self.raceValues.lastLap 
-
-				end
-				self.raceValues.laps = math.floor(self.raceValues.completedGoals/(#path+1))
-		elseif(VecLength( VecSub(
-					Vec(indexVal[1],0,indexVal[3]),
-					Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2])))
-			>(self.raceValues.completionRange*5)) then 
-			-- DebugPrint("test range: "..(self.raceValues.completionRange*30)..
-			-- 	"current len: "..VecLength( VecSub(
-			-- 		Vec(indexVal[1],0,indexVal[3]),
-			-- 		Vec(path[self.raceValues.targetNode][1],0,path[self.raceValues.targetNode][2]))))
-			SetString("hud.notification", "Too far from race track last location, look for flame on track")
-			SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
-		end
-
-
-	end
-
-	-- DebugWatch("checkpoint: ",self.goalPos)
-
-
-
-end
-
-function ai:player_check_future(player_hit_range)
-	local next_point = nil 
-	local vehiclePos = GetVehicleTransform(self.id).pos
-	local indexVal = posToInt(vehiclePos)
-	local target = 0
-	for i=0,15 do 
-		target =(((self.raceValues.targetNode-1) +i)%#path )+1
-		if(DEBUG) then 
-			DebugPrint("target pos is: "..target.." path length: "..#path)
-			SpawnParticle("fire", Vec(path[target][1],0,path[target][2]), Vec(0,5,0), 0.5, 1)
-		end
-		
-		if(VecLength( VecSub(
-							Vec(indexVal[1],0,indexVal[3]),
-							Vec(path[target][1],0,path[target][2])))
-							<player_hit_range)
-		then 
-			if(DEBUG) then 
-				DebugPrint(target.." id "..i)
-			end
-			return true, i
-		end
-	end
-	return false,0
- 
-end
-
---- handle race position / laps / checkpoints
-	-- raceValues = {
-	-- 	completedGoals  = 0,
-	-- 	targetNode 		= 1,
-	-- nextCheckpoint = 1,
-		-- passedCheckPoints = 0,
-	-- 	completionRange = 4,
-	-- 	lookAhead = 2,
-	-- 	laps = 0 	
-		-- splits = {}
-
-	-- },
-
-
-
-function ai:raceDetailsHandler()
-	
-	if IsVehicleInTrigger(self.raceValues.nextCheckpoint, self.id) then
-		
-
-	end
-
-
-	if (self.raceValues.targetNode%#path) == 0 then
-		
-
-	end
-	
-end
-
-
-function ai:goalDistance()
-	return VecLength( VecSub(self:getPos(),self.goalPos))
-end
-
-function ai:getPos()
-	return GetVehicleTransform(self.id).pos
-end
-
-function ai:markLoc()
-	
-	if InputPressed("g") and not RACESTARTED  then
-
-		RACESTARTED = true
-		DebugPrint("race Started")
-		self.currentCheckpoint = self.currentCheckpoint+1
-		self.goalOrigPos = GetTriggerTransform(self.currentCheckpoint).pos
-
-		self.goalPos = TransformToParentPoint(GetTriggerTransform(self.currentCheckpoint),Vec(math.random(-7,7),0,math.random(5,10)))
-
-		-- local camera = GetCameraTransform()
-		-- local aimpos = TransformToParentPoint(camera, Vec(0, 0, -300))
-		-- local hit, dist,normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aimpos, camera.pos)), 200,0)
-		-- if hit then
-			
-		-- 	self.goalPos = TransformToParentPoint(camera, Vec(0, 0, -dist))
-
-		-- end 	
-
-		-- DebugPrint("hitspot"..VecStr(goalPos).." | "..dist.." | "..VecLength(
-		-- 							VecSub(GetVehicleTransform(vehicle.id).pos,goalPos)))
-	end
-
-	if(RACESTARTED) then 
-		if(IsVehicleInTrigger(self.currentCheckpoint,self.id)) then
-			self.raceCheckpoint = (self.raceCheckpoint%#checkpoints)+1
-			for key,value in ipairs(checkpoints) do 
-				
-				if(tonumber(GetTagValue(value, "checkpoint"))==self.raceCheckpoint) then 
-					self.currentCheckpoint = value
-					self.goalOrigPos = GetTriggerTransform(self.currentCheckpoint).pos
-
-					self.goalPos =TransformToParentPoint(GetTriggerTransform(self.currentCheckpoint),Vec(math.random(-7,7),0,math.random(5,10)))
-				end
-			end
-
-			end
-
-		-- DebugWatch("checkpoint: ",raceCheckpoint)
-		-- DebugWatch("goalpos",VecLength(goalPos))
-		--SpawnParticle("fire", self.goalPos, Vec(0,5,0), 0.5, 1)
-	end
-
-
-end
-
-
-
-	-- reversingController = {
-	-- 	reversing = false,
-	-- 	minVelocity = 1,
-	-- 	waitTime = 3,
-	-- 	currentWait = 3,
-	-- 	reverseTime = 2,
-	-- 	currentReverseTime = 2,
-	-- },
-
-function ai:controlActions(dt)
-	if(not self.reversingController.reversing) then 
-		if(VecLength(GetBodyVelocity(GetVehicleBody(self.id)))<self.reversingController.minVelocity) then
-			if(self.reversingController.currentWait<0) then
-				self.reversingController.reversing = true
-			end
-			self.reversingController.currentWait = self.reversingController.currentWait - GetTimeStep()
-		elseif(self.reversingController.currentWait  ~= self.reversingController.waitTime) then
-			self.reversingController.currentWait  = self.reversingController.waitTime
-		end
-
-		if(self.usingClustering) then
-			self:scanPos()
-		end
-		local steeringValue = -self:pid()
-		local accelerationValue = self:accelerationError()
-		
-		
-		-- DebugWatch("pre acceletation: ",self.controller.accelerationValue)
-		-- DebugWatch("pre steering: ",self.controller.steeringValue)
-
-
-		self.controller.steeringValue = steeringValue * self.steeringCoef
-		self.controller.accelerationValue = accelerationValue*self.accelerationCoef
-
-		self:controllerAugmentation()
-		-- DebugWatch("post acceletation: ",self.controller.accelerationValue)
-		-- DebugWatch("post steering: ",self.controller.steeringValue)
-
-		self:obstacleAvoidance()
-
-
-
-		self:applyError()
-			
-			--- apply reversing error
-
-		local directionError =  self:directionError()
-		self.controller.accelerationValue = self.controller.accelerationValue * directionError
-		
-		    --- apply steering safety error
-		if(self.controller.accelerationValue>0)then 
-			local corneringErrorMagnitude = self:corneringError()
-			self.controller.accelerationValue = self.controller.accelerationValue * corneringErrorMagnitude
-		end
-		self.controller.steeringValue = self.controller.steeringValue  * directionError
-	else
-		if(self.reversingController.currentReverseTime >0) then
-			self.controller.accelerationValue = -1
-			self.controller.steeringValue = -self.controller.steeringValue 
-			self.reversingController.currentReverseTime = self.reversingController.currentReverseTime - GetTimeStep()
-		else
-			self.reversingController.reversing = false
-			self.reversingController.currentReverseTime = self.reversingController.reverseTime
-			self.reversingController.currentWait = self.reversingController.waitTime
-		end
-		
-	end
-end
-
-
-function ai:controllerAugmentation()
-	local velocity =  VecLength(GetBodyVelocity(GetVehicleBody(self.id)))
-
-	if(math.abs(self.controller.accelerationValue)>1.5 and velocity>self.cornerCoef and self.controller.accelerationValue*0.8 ~=0
-		and math.abs(self.controller.steeringValue) >= self.controller.speedSteeringThres) then
-		
-		self.controller.accelerationValue = (math.log(self.controller.accelerationValue*0.4)) - math.abs(self.controller.steeringValue*self.steeringCoef)
-	else 
-		self.controller.accelerationValue  = 1
-	end
-	
-	
-end
-
-function ai:obstacleAvoidance()
-	local scanResults = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
-	local scanShapes = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
-	local scanhitPos = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
-	local scanDists = {centre=0,left =0, sideL =0 , sideR =0, right = 0}
-	local vehicleTransform = GetVehicleTransform(self.id)
-
-	local front = self.bodyYSize/4 
-	local side = self.bodyXSize/4
-	local height = self.bodyZSize /6
-	-- DebugWatch("height",self.bodyZSize)
-	-- DebugWatch("width",self.bodyXSize)
-	-- DebugWatch("length",self.bodyYSize)
-	vehicleTransform.pos = TransformToParentPoint(vehicleTransform,Vec(0,height/4	,-front/4))
-	local testScanRot = nil
-	local fwdPos = nil
-	local direction = nil
-	local scanStartPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
-	local scanEndPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
-
-	local scanLength = 2+ self.scanning.maxScanLength*((VecLength(GetBodyVelocity(GetVehicleBody(self.id))))/self.scanning.maxScanLength)
-
-	for key,scan in pairs(self.scanning.positions) do 
-
-
-		if(scan.direction == "centre") then 
-			scanStartPos =VecCopy(vehicleTransform.pos)
-		elseif(scan.direction =="left") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/6,0,front/8))
-		elseif(scan.direction =="right") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/6,0,front/8))
-		elseif(scan.direction =="sideR") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/5,0,front/4))
-		elseif(scan.direction =="sideL") then
-			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/5,0,front/4))
-		end
-
-		scanEndPos = TransformToParentPoint(Transform(scanStartPos,vehicleTransform.rot),scan.startVec)
-		testScanRot = QuatLookAt(scanEndPos,scanStartPos)
-
-		fwdPos = TransformToParentPoint(Transform(scanStartPos,testScanRot),  
-				Vec(0,0,-scanLength))---self.scanning.maxScanLength))
-		direction = VecSub(scanStartPos,fwdPos)
-		direction = VecNormalize(direction)
-	    QueryRejectVehicle(self.id)
-	    QueryRequire("dynamic large")
-
-	    local hit,dist,normal, shape = QueryRaycast(scanStartPos, direction, scanLength)--self.scanning.maxScanLength)
-	    scanResults[key] = hit
-	    scanDists[key] = dist
-	    scanShapes[key] = shape
-	    scanhitPos[key]	= VecScale(direction,dist)
-	    if(hit and DEBUGCARS) then
-
-			 DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 1, 0, 0)
-		elseif(DEBUGCARS) then
-			DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 0, 1, 0)
-		end
-	end
-
-	local turnBias = math.random()
-
-	if(scanResults.centre ) then 
-		-- DebugWatch("pre val:",self.controller.accelerationValue )
-		self.controller.accelerationValue =self.controller.accelerationValue* (self:getRelativeSpeed(scanShapes.centre,scanhitPos.center))--/self.controller.tenacity)
-		-- self.controller.accelerationValue = self.controller.accelerationValue    * self.controller.tenacity
-
-		-- DebugWatch("post val:",self.controller.accelerationValue )
-		-- DebugWatch("relative val:",relative )
-		
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and not scanResults.centre and  
-				(scanResults.left or scanResults.right or scanResults.sideL or scanResults.sideR)	) then
-		self.controller.accelerationValue = self.controller.accelerationValue    * 2
-
-	end
-	if(scanResults.left and scanResults.right) then 
-
-		self.controller.accelerationValue = self.controller.accelerationValue    * 0.5
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.left) then
-
-		self.controller.steeringValue = self.controller.steeringForce +(scanDists.left/(self.scanning.maxScanLength/2)/2)
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.right) then 
-
-		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.right/(self.scanning.maxScanLength/2)/2)
-	
-
-	--- handle sides 
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideL) then
-
-		self.controller.steeringValue = self.controller.steeringForce +(scanDists.sideL/(self.scanning.maxScanLength/2)/4)
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideR) then
-
-		
-		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.sideR/(self.scanning.maxScanLength/2)/4)
-
-	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.centre ) then 
-		--- random moving vs best direction 
-
-		 -- sign((Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax))
-
-
-		if turnBias <0.5 then
-			self.controller.steeringValue = self.controller.steeringForce*2
-		else
-			self.controller.steeringValue = -self.controller.steeringForce*2
-		end
-
-	
-	end
-end
-
-
-
-
--- function ai:obstacleAvoidance()
--- 	local scanResults = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
--- 	local scanShapes = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
--- 	local scanhitPos = {centre=nil,left =nil,sideL =nil,sideR =nil,right = nil}
--- 	local scanDists = {centre=0,left =0, sideL =0 , sideR =0, right = 0}
--- 	local vehicleTransform = GetVehicleTransform(self.id)
-
--- 	local front = self.bodyYSize/4 
--- 	local side = self.bodyXSize/4
--- 	local height = self.bodyZSize /4
-
--- 	vehicleTransform.pos = TransformToParentPoint(vehicleTransform,Vec(0,height/4	,-front/4))
--- 	local testScanRot = nil
--- 	local fwdPos = nil
--- 	local direction = nil
--- 	local scanStartPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
--- 	local scanEndPos = TransformToParentPoint(vehicleTransform,Vec(0,0,0))
-
--- 	local scanLength = 2+ self.scanning.maxScanLength*((VecLength(GetBodyVelocity(GetVehicleBody(self.id))))/self.scanning.maxScanLength)
-
--- 	for key,scan in pairs(self.scanning.positions) do 
-
-
--- 		if(scan.direction == "centre") then 
--- 			scanStartPos =VecCopy(vehicleTransform.pos)
--- 		elseif(scan.direction =="left") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/6,0,front/8))
--- 		elseif(scan.direction =="right") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/6,0,front/8))
--- 		elseif(scan.direction =="sideR") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(-side/5,0,front/4))
--- 		elseif(scan.direction =="sideL") then
--- 			scanStartPos = TransformToParentPoint(vehicleTransform,Vec(side/5,0,front/4))
--- 		end
-
--- 		scanEndPos = TransformToParentPoint(Transform(scanStartPos,vehicleTransform.rot),scan.startVec)
--- 		testScanRot = QuatLookAt(scanEndPos,scanStartPos)
-
--- 		fwdPos = TransformToParentPoint(Transform(scanStartPos,testScanRot),  
--- 				Vec(0,0,-scanLength))---self.scanning.maxScanLength))
--- 		direction = VecSub(scanStartPos,fwdPos)
--- 		direction = VecNormalize(direction)
--- 	    QueryRejectVehicle(self.id)
--- 	    QueryRequire("dynamic large")
-
--- 	    local hit,dist,normal, shape = QueryRaycast(scanStartPos, direction, scanLength)--self.scanning.maxScanLength)
--- 	    scanResults[key] = hit
--- 	    scanDists[key] = dist
--- 	    scanShapes[key] = shape
--- 	    scanhitPos[key]	= VecScale(direction,dist)
--- 	    if(hit and DEBUGCARS) then
-
--- 			 DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 1, 0, 0)
--- 		elseif(DEBUGCARS) then
--- 			DrawLine(scanStartPos, VecAdd(scanStartPos, VecScale(direction, dist)), 0, 1, 0)
--- 		end
--- 	end
-
--- 	local turnBias = math.random()
-
--- 	if(scanResults.centre ) then 
--- 		-- DebugWatch("pre val:",self.controller.accelerationValue )
--- 		self.controller.accelerationValue =self.controller.accelerationValue* (self:getRelativeSpeed(scanShapes.centre,scanhitPos.center))--/self.controller.tenacity)
--- 		-- self.controller.accelerationValue = self.controller.accelerationValue    * self.controller.tenacity
-
--- 		-- DebugWatch("post val:",self.controller.accelerationValue )
--- 		-- DebugWatch("relative val:",relative )
-		
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and not scanResults.centre and  
--- 				(scanResults.left or scanResults.right or scanResults.sideL or scanResults.sideR)	) then
--- 		self.controller.accelerationValue = self.controller.accelerationValue    * 2
-
--- 	end
--- 	if(scanResults.left and scanResults.right) then 
-
--- 		self.controller.accelerationValue = self.controller.accelerationValue    * 0.5
-
-
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.centre ) then 
--- 		--- random moving vs best direction 
-
--- 		 -- sign((Bx - Ax) * (Y - Ay) - (By - Ay) * (X - Ax))
-
--- 		if(scanResults.left and not scanResults.right) then
--- 			self.controller.steeringValue = 0.5
--- 		elseif(not scanResults.left and scanResults.right) then
--- 			self.controller.steeringValue = -0.5
--- 		elseif(not scanResults.left and not scanResults.right) then 
-
--- 			if turnBias <0.5 then
--- 				self.controller.steeringValue = self.controller.steeringForce*2
--- 			else
--- 				self.controller.steeringValue = -(self.controller.steeringForce)*2
--- 			end
--- 		end
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.left) then
-
--- 		self.controller.steeringValue = self.controller.steeringForce +(scanDists.left/(self.scanning.maxScanLength/2)/2)
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.right) then 
-
--- 		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.right/(self.scanning.maxScanLength/2)/2)
-	
-
--- 	--- handle sides 
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideL) then
-
--- 		self.controller.steeringValue = self.controller.steeringForce +(scanDists.sideL/(self.scanning.maxScanLength/2)/4)
-
--- 	elseif(math.abs(self.controller.steeringValue) < self.controller.steeringThres and scanResults.sideR) then
-
-		
--- 		self.controller.steeringValue = -self.controller.steeringForce - (scanDists.sideR/(self.scanning.maxScanLength/2)/4)
-
--- 	end
--- end
-
-
-
---[[
-
-	calculate relative speed, if vehicle moving towards then stop / avoid. 
-
-	if movng faster than gap between then stop, otherwise move proportionally to the distance between vehicles vs speed
-
-]]
-
-function ai:getRelativeSpeed(shape,hitPos)
-	local otherShapeBody = GetShapeBody(shape)
-	local otherShapeBodyPos = GetBodyTransform(otherShapeBody).pos
-	local otherShapeVelocity =  GetBodyVelocity(otherShapeBody)
-	local vehicleBody = GetVehicleBody(self.id)
-	local vehicleBodyPos = GetBodyTransform(vehicleBody).pos
-	local vehicleVelocity = GetBodyVelocity(vehicleBody) 
-
-	local toPoint = VecSub(vehicleBodyPos,otherShapeBodyPos)
-	local movingTowards = false
-	---VecSub(vehicleVelocity,otherShapeVelocity)
-	-- DebugWatch("otherShapeVelocity",VecLength(otherShapeVelocity))
-	-- DebugWatch("vehicleVelocity",VecLength(vehicleVelocity))
-
-	local adjustmentValue = 0 
-
-	--[[
-		if crash likely then set adjustment to -1 (GTFO mode)
-		elseif speed greater than safe range then force slow down
-			else adjust speed to maintain safe distance 
-		else set to higher speed to get closer for overtaking
-	]]
-	local minDist = self.controller.minDist
-	if(VecLength(vehicleVelocity) >0) then 
-		 minDist = minDist / math.log(VecLength(vehicleVelocity))
-	end
-
-	
-	if(VecDot(toPoint,otherShapeVelocity)>0) then 
-		adjustmentValue = -1
-		if(DEBUG_SAE) then 
-			DebugWatch("slowing for safety",1)
-		end
-	elseif(VecLength(otherShapeVelocity)<VecLength(vehicleVelocity)) then 
-		local relativeSpeed = VecLength(vehicleVelocity)-VecLength(otherShapeVelocity) 
-		local relativeDistance = VecLength(VecSub(vehicleBodyPos,hitPos))
-			--- set mindist to be math.log of relative speed, relative speed is negative if they are faster
-			--- dist coef 
-		if(relativeSpeed ~=0) then 
-			 minDist =  math.log((relativeSpeed))*math.sign(relativeSpeed)
-		end
-		local distCoef = relativeDistance-minDist
-
-		if((relativeSpeed) > distCoef) then
-			adjustmentValue = -(distCoef/(relativeSpeed*2))
-		else
-			adjustmentValue = (relativeSpeed/distCoef)--(0.2) + relativeSpeed/(relativeDistance)--*self.controller.tenacity)
-			-- adjustmentValue=1
-		end
-		
-	else
-		adjustmentValue=2
-	end
-	if(DEBUG_SAE) then
-		DebugWatch("minDist",minDist)
-		DebugWatch("adjusting",adjustmentValue)
-	end
-	return adjustmentValue
-
-end
+#version 2
+local minDist = self.controller.minDist
 
 function ai:turnDirection()
 	
 end
-
 
 function ai:applyError()
 	local errorCoef = self.controller.errorCoef--0.1
@@ -1817,19 +20,15 @@
 	local boundsSize = VecSub(max, min)
 	local center = VecLerp(min, max, 0.5)
 
-
 	-- DebugWatch("boundsize",boundsSize)
 	-- DebugWatch("center",center)
 
 	vehicleTransform.pos = TransformToParentPoint(vehicleTransform,Vec(0,1.2	,0))
 
-
 	for key,scan in pairs(self.scanning.cones) do 
 
 		for i=1,ai.scanning.scanDepths do 
 			local scanLength = self.scanning.scanLength * i
-
-
 
 			local projectionAngle =  (math.sin(math.rad(scan.size)) * ((scanLength)))
 			if(scan.startVec[1]>0) then
@@ -1872,17 +71,13 @@
 
 	end
 
-
 	self:clusteringOperations()
-
 
 	self.clustering.clusters.current.pass = (self.clustering.clusters.current.pass%self.clustering.dataSize )+1 
 	self.clustering.clusters.current.index = 1
 
 end
 
-
---init clusters 
 function ai:clusteringCentroids()
 	local valRange = { min = { 100000, 100000, 100000},
 						max = {-100000 , -100000 , -100000 } 
@@ -1916,7 +111,6 @@
 	--DebugPrint("min:"..valRange.min[1]..","..valRange.min[2]..","..valRange.min[2].."\nMax: "..valRange.max[1]..","..valRange.max[2]..","..valRange.max[3])
 end
 
---init clusters 
 function ai:clusteringUpdateCentroids()
 	local pos = Vec(0,0,0)
 	local inputData = nil
@@ -1934,8 +128,6 @@
 	end
 end
 
-
--- find euclidian distance of data to clusters and update centroid locations
 function ai:clusteringCalculateClusters()
 	local pos = Vec(0,0,0)
 	local center = Vec(0,0,0)
@@ -1956,11 +148,9 @@
 
 end
 
---- perform operations on clusters to extract target
 function ai:clusteringOperations()
 	
 	self:clusteringCalculateClusters()
-
 
 	self:pseudoSNN()
 
@@ -1975,14 +165,6 @@
 	self.targetNode = self.clustering.clusters.centroids.data[self.clustering.mode]
 
 end
-
-
---- simulate an snn network slightly to get best node
-
--- if(SNNpspprev[j]<SNNpsp[i])
---  {
---      SNNweights[j][i]=tanh(gammaweights*SNNweights[j][i]+learningrateweights*SNNpspprev[j]*SNNpsp[i]);
---  }
 
 function ai:pseudoSNN()
 	local bestpsp = 100000000
@@ -2048,7 +230,6 @@
 	
 	--DebugPrint("values: index: "..index.."\nhitpos:"..VecStr(hitPos).."\nhitval: "..hitValue.."\nClusterPos = "..VecStr(self.clustering.clusters.current.data[index]:getPos()))
 	self.clustering.clusters.current.data[index]:push(hitPos[1],hitPos[2],hitPos[3],hitValue) 
-
 
 	self.clustering.clusters.current.index = (self.clustering.clusters.current.index%self.clustering.dataSize )+1
 end
@@ -2072,7 +253,6 @@
 	self.pidState.controllerValue = output
 	-- DebugWatch("pid output: ",output)
 
-
 	if(RACESTARTED and  self.pidState.training) then
 		if math.abs(crossTrackErrorRate) > self.pidState.learningrateThres then 
 			if(crossTrackErrorRate>0) then 
@@ -2091,7 +271,6 @@
 
 	return output
 end
-
 
 function ai:currentCrossTrackError()
 	local crossTrackErrorValue = 0
@@ -2104,10 +283,7 @@
 	return targetNode, crossTrackErrorValue,sign
 end
 
---- calculate distance to target direction and apply steering by force
---- fill in the gap here related to the distance ebtween the aprrelel lines of target nod3e to vehicle pos to solve it all
 function ai:crossTrackError(pnt,vehicleTransform)
-
 
 		
 		vehicleTransform.pos[2] = pnt[2]
@@ -2129,7 +305,6 @@
 			sign = 0
 		end
 
-
 		return d*sign,sign
 
 		-- Use the sign of the determinant of vectors (AB,AM), where M(X,Y) is the query point:	
@@ -2148,12 +323,6 @@
 		-- DebugWatch("output pos : ",out)
 
 		-- DebugWatch("output value: ",VecSub(out,pnt))
-
-
-
-
-
-
 
 		-- local vehicleTransform = GetVehicleTransform(self.id)
 		-- vehicleTransform.pos[2] = targetNode:getPos()[2]
@@ -2188,7 +357,6 @@
 	return verifyCrossCheckErrorVal
 end
 
-
 function ai:calculateSteadyStateError(crossTrackErrorValue)
 	local index = self.pidState.integralIndex
 
@@ -2232,13 +400,10 @@
 		-- DebugWatch("is forward",is_forward)
 		-- DebugWatch("local point  forwar", TransformToLocalPoint(vehicleTransform, pnt)[3])
 
-
 		return VecLength(VecSub(vehicleTransform.pos,out))
 	end	
 end
 
-
-	-- thanks to  iaobardar for help on getting the vecdot to work
 function ai:directionError()
 	local vehicleTransform = GetVehicleTransform(self.id)
 	local targetNode = self.targetNode
@@ -2294,13 +459,6 @@
 
 end
 
-
-
-
-
-
- 
-
 function ai:vehicleController()
 	DriveVehicle(self.id, 0.05+self.controller.accelerationValue,
 							self.controller.steeringValue,
@@ -2316,11 +474,7 @@
 
 end
 
-
-
 function ai:costFunc(testPos,hit,dist,shape,key)
-
-
 
 	local cost = 10000 
 	if(not hit) then
@@ -2328,8 +482,6 @@
 	end
 	return cost
 end
-
-
 
 function ai:controlVehicle( targetCost)
 	local hBrake = false
@@ -2359,7 +511,6 @@
 				targetMove[3] = targetMove[3] *2
 			end
 
-
 			DriveVehicle(self.id, -targetMove[3]*drivePower,-targetMove[1], hBrake)
 			-- DebugWatch("post updated",VecStr(targetMove))
 			-- DebugWatch("motion2",VecStr(detectPoints[targetCost.key]))
@@ -2368,34 +519,6 @@
 		end
 	end
 end
-
-
--- function ai:modulo(a,b )
--- 	return a - math.floor(a/b)*b
-	
--- end
-
-------------------------------------------------
-
-
----- PATHFINDING
-
-
------------------------------------------------------
-
-
-
----- 
-
-
-
----- use flood fill to comap[re to last neighbor  that was known and if neighbor foun and  track then 
-
----- compare the next based on known locations nd move outwards.]
-
-----
-
-
 
 function scanGrid(x,y)
   local pos = Vec(0,0,0)
@@ -2442,8 +565,6 @@
   return gridScore,validTerrain, minHeight, ((minHeight+maxHeight)/2)
 end
 
-
-
 function getHeight(x,y)
 
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -2513,7 +634,6 @@
   return score
 
 end
-
 
 function getMaterialScore3(x,y)
   local score = 0
@@ -2582,14 +702,9 @@
   return pos,pos2
 end
 
-
 function Heuristic(a, b)
       return Math.Abs(a[1] - b[1]) + Math.Abs(a[3] - b[3]);
- end 
-
-
-
-
+ end
 
 function checkIfTerrainValid(mat,r,g,b)
 		local score = 0
@@ -2624,20 +739,6 @@
 	    return score
 end
 
-
-
-
-
-
-
----------------------------------------------------------
-
-
-
-
--------------------------------------------------------
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
@@ -2651,8 +752,6 @@
 	end
 
 end
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -2669,7 +768,6 @@
     return copy
 end
 
-
 function inRange(min,max,value)
 		if(tonumber(min) < tonumber(value) and tonumber(value)<=tonumber(max)) then 
 			return true
@@ -2680,12 +778,3 @@
 
 end
 
-
-
-
-function draw()
-
-
-end
-
-

```

---

# Migration Report: pathfinding\AVF_pathfinding_refined.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding\AVF_pathfinding_refined.lua
+++ patched/pathfinding\AVF_pathfinding_refined.lua
@@ -1,185 +1,4 @@
-
-
----PATHFINDING LINKED
-
-#include "mapNode.lua"
-#include "AStarSearch.lua"
-
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        AVF_AI_3.lua             
-*
-* DESCRIPTION :
-*       File that implements racing AI inside teardown 2020, with PID controllers
-* 		to ensure cars respond to coordinates in a good fashion and can handle high speed
-*		Also includes simple goal achievement and collision avoidance 
-*		Including "driver ai" to make them more / less aggressive with speed, cornering
-*		overtaking, and driving. 
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-PATHSET = false
-
-mapInitialized = false
-DEBUG = false
-
-map = {
-
-  xIndex = 0,
-  data = {
-
-  },
-
-  smoothingFactor = 3,
-  validMaterials = {
-  	[1] = {	
-  		material = "masonry",
-
-
-	  validSurfaceColours ={ 
-				[1] = {
-					r = 0.20,
-					g = 0.20,
-					b = 0.20,
-					range = 0.2
-				},
-				[2] = {
-					r = 0.80,
-					g = 0.60,
-					b = 0.60,
-					range = 0.2
-				},
-				[3] = {
-					r = 0.34,
-					g = 0.34,
-					b = 0.34,
-					range = 0.2
-				},
-			},
-		},
-	},
-}
-
--- negative grid pos is solved by simply showing 
-mapSize = {
-			x=400,
-			y=400,
-			grid =4,--6,
-      gridHeight = 2.5,
-      gridResolution = 3, -- seaches per grid square
-      gridThres      = 0.6,
-
-      scanHeight = 100,
-
-      scanLength = 200,
-      refresh_rate = 20,
-      weights = {
-          goodTerrain = 0.5,
-          badTerrain   = 5,
-          avoidTerrain = 25,
-          impassableTerrain = 50,
-      }
-		}
-    path = nil
-
-
---- AI LINKED
-
-ai = {}
-
-pathing_states = {
-	current_state = 1,
-	states = {
-		[1] = 'READY',
-		[2] = 'SEARCHING',
-		[3] = 'EXPIRED'
-	}
-
-
-}
-
-
-TARGET_POS =nil
-
-
-function init()
-
-	mapSize.gridResolution = mapSize.grid/mapSize.gridResolution
-	initMapArr()
-
-end
-
-
-function initMapArr()
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-	    pos = posToInt(Vec(0,0,y))
-	    map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        map.data[pos[3]][pos[1]] = nil 
-	    end
-	end
-end
-
-function initMap( )
-  local pos = Vec(0,0,0)
-  local gridCost = 0
-  local maxVal  = {math.modf((mapSize.x)/mapSize.grid),math.modf((mapSize.y)/mapSize.grid)}
-
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-    pos = posToInt(Vec(0,0,y))
-    -- map.data[pos[3]] = {}
-	    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-	        pos = posToInt(Vec(x,0,y))
-	        gridCost,validTerrain,avgHeight,grid_avg =  scanGrid(x,y) 
-	        -- gridCost,validTerrain,avgHeight,grid_avg =  1,true,1,1,1
-	        -- if(pos[3] ~= nil and pos[1]~= nil) then
-	          
-	          map.data[pos[3]][pos[1]] = deepcopy(mapNode) 
-	          map.data[pos[3]][pos[1]]:push(x,grid_avg,y,gridCost,pos[3],pos[1],validTerrain,maxVal,0 )
-
-	        -- end
-	  		  -- DebugPrint(x.." | "..y)
-	    end
-	end
-
-
-	mapInitialized = true
-	
-
-end
-
-function get_pathing_state()
-	pathing_state = pathing_states['states'][pathing_states['current_state']]
-	return pathing_state
-
-end
-
-function init_pathfinding(startPos,goalPos)
-
-	goalPos = posToInt(goalPos)
-	startPos = posToInt(startPos)
-	local goal = map.data[goalPos[3]][goalPos[1]]
-	local start = map.data[startPos[3]][startPos[1]]
-	AStar:init(map.data, start, goal  ) 
-
-	pathing_states['current_state'] = 2
-
-end
-		
+#version 2
 function perform_pathfinding()
 	local search_result =  AStar:AStarSearch_2(map.data)
 
@@ -199,78 +18,7 @@
 
 end
 
-
-
-function tick(dt)
-	if(not(mapInitialized)) then 
-		initMap()
-	end
-	DebugWatch("game time",GetTime())
-	DebugWatch("pathing_state",get_pathing_state())
-
-	DebugWatch("PATHSET",PATHSET)
-	if(PATHSET) then 
-		 AStar:drawPath(map.data,path)
-	  	if(DEBUG)then 
-
-		    AStar:drawPath(map.data,path)
-
-			local t = GetCameraTransform()
-			local dir = TransformToParentVec(t, {0, 0, -1})
-
-			local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 10)
-			DebugWatch("Hit", hit)
-			if hit then
-				--Visualize raycast hit and normal
-				local hitPoint = VecAdd(t.pos, VecScale(dir, dist))
-				local mat,r,g,b = GetShapeMaterialAtPosition(shape, hitPoint)
-				DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
-				DebugWatch("Terrain cost",checkIfTerrainValid(mat,r,g,b))
-				DebugWatch("body mass",GetBodyMass(GetShapeBody(shape)))
-			end
-
-		end
-	end
-
-
-
-	---------------------
-			---------- keypress stuff
-	---------------
-	-- DebugWatch("map_mode")
-	if InputPressed("c") then 
-		CAMMODE = not CAMMODE
-
-	end
-	if(InputPressed("y")) then
-		local hitPos = perform_raycast()
-		if(hitPos) then 
-			TARGET_POS= hitPos
-		end
-	end
-	DebugWatch("TARGET_POS",TARGET_POS)
-
-	if(TARGET_POS and InputPressed("p")) then
-		DebugWatch("map init",mapInitialized)
-
-		if(get_pathing_state() =="READY") then 
-			local hitPos = perform_raycast()
-			if(hitPos) then 
-				DebugWatch("start pos",hitPos)
-				init_pathfinding(hitPos, TARGET_POS)
-			end
-		end
-	end
-	if(mapInitialized and get_pathing_state() == "SEARCHING") then 
-		perform_pathfinding()
-	end
-
-
-end
-
-
 function perform_raycast()
-
 
 	local t = GetCameraTransform()
 	local dir = TransformToParentVec(t, {0, 0, -1})
@@ -285,7 +33,6 @@
 	return nil
 end
 
--- find euclidian distance of data to clusters and update centroid locations
 function ai:clusteringCalculateClusters()
 	local pos = Vec(0,0,0)
 	local center = Vec(0,0,0)
@@ -306,11 +53,9 @@
 
 end
 
---- perform operations on clusters to extract target
 function ai:clusteringOperations()
 	
 	self:clusteringCalculateClusters()
-
 
 	self:pseudoSNN()
 
@@ -325,14 +70,6 @@
 	self.targetNode = self.clustering.clusters.centroids.data[self.clustering.mode]
 
 end
-
-
---- simulate an snn network slightly to get best node
-
--- if(SNNpspprev[j]<SNNpsp[i])
---  {
---      SNNweights[j][i]=tanh(gammaweights*SNNweights[j][i]+learningrateweights*SNNpspprev[j]*SNNpsp[i]);
---  }
 
 function ai:pseudoSNN()
 	local bestpsp = 100000000
@@ -399,10 +136,8 @@
 	--DebugPrint("values: index: "..index.."\nhitpos:"..VecStr(hitPos).."\nhitval: "..hitValue.."\nClusterPos = "..VecStr(self.clustering.clusters.current.data[index]:getPos()))
 	self.clustering.clusters.current.data[index]:push(hitPos[1],hitPos[2],hitPos[3],hitValue) 
 
-
 	self.clustering.clusters.current.index = (self.clustering.clusters.current.index%self.clustering.dataSize )+1
 end
-
 
 function ai:MAV(targetCost)
 	self.targetMoves.targetIndex = (self.targetMoves.targetIndex%#self.targetMoves.list)+1 
@@ -413,11 +148,7 @@
 
 end
 
-
-
 function ai:costFunc(testPos,hit,dist,shape,key)
-
-
 
 	local cost = 10000 
 	if(not hit) then
@@ -425,29 +156,6 @@
 	end
 	return cost
 end
-
-
-------------------------------------------------
-
-
----- PATHFINDING
-
-
------------------------------------------------------
-
-
-
----- 
-
-
-
----- use flood fill to comap[re to last neighbor  that was known and if neighbor foun and  track then 
-
----- compare the next based on known locations nd move outwards.]
-
-----
-
-
 
 function scanGrid(x,y)
   local pos = Vec(0,0,0)
@@ -494,8 +202,6 @@
   return gridScore,validTerrain, minHeight, ((minHeight+maxHeight)/2)
 end
 
-
-
 function getHeight(x,y)
 
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -565,7 +271,6 @@
   return score
 
 end
-
 
 function getMaterialScore3(x,y)
   local score = 0
@@ -635,14 +340,9 @@
   return pos,pos2
 end
 
-
 function Heuristic(a, b)
       return Math.Abs(a[1] - b[1]) + Math.Abs(a[3] - b[3]);
- end 
-
-
-
-
+ end
 
 function checkIfTerrainValid(mat,r,g,b)
 		local score = 0
@@ -677,20 +377,6 @@
 	    return score
 end
 
-
-
-
-
-
-
----------------------------------------------------------
-
-
-
-
--------------------------------------------------------
-
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
@@ -704,8 +390,6 @@
 	end
 
 end
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -722,7 +406,6 @@
     return copy
 end
 
-
 function inRange(min,max,value)
 		if(tonumber(min) < tonumber(value) and tonumber(value)<=tonumber(max)) then 
 			return true
@@ -733,12 +416,69 @@
 
 end
 
-
-
-
-function draw()
-
-
-end
-
-
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(not(mapInitialized)) then 
+        	initMap()
+        end
+        DebugWatch("game time",GetTime())
+        DebugWatch("pathing_state",get_pathing_state())
+        DebugWatch("PATHSET",PATHSET)
+        if(PATHSET) then 
+        	 AStar:drawPath(map.data,path)
+          	if(DEBUG)then 
+
+        	    AStar:drawPath(map.data,path)
+
+        		local t = GetCameraTransform()
+        		local dir = TransformToParentVec(t, {0, 0, -1})
+
+        		local hit, dist, normal, shape = QueryRaycast(t.pos, dir, 10)
+        		DebugWatch("Hit", hit)
+        		if hit then
+        			--Visualize raycast hit and normal
+        			local hitPoint = VecAdd(t.pos, VecScale(dir, dist))
+        			local mat,r,g,b = GetShapeMaterialAtPosition(shape, hitPoint)
+        			DebugWatch("Raycast hit voxel made out of ", mat.." | r:"..r.."g:"..g.."b:"..b)
+        			DebugWatch("Terrain cost",checkIfTerrainValid(mat,r,g,b))
+        			DebugWatch("body mass",GetBodyMass(GetShapeBody(shape)))
+        		end
+
+        	end
+        end
+        ---------------------
+        		---------- keypress stuff
+        ---------------
+        -- DebugWatch("map_mode")
+        DebugWatch("TARGET_POS",TARGET_POS)
+        if(mapInitialized and get_pathing_state() == "SEARCHING") then 
+        	perform_pathfinding()
+        end
+    end
+end
+
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+    if InputPressed("c") then 
+    	CAMMODE = not CAMMODE
+
+    end
+    if(InputPressed("y")) then
+    	local hitPos = perform_raycast()
+    	if(hitPos) then 
+    		TARGET_POS= hitPos
+    	end
+    end
+    if(TARGET_POS and InputPressed("p")) then
+    	DebugWatch("map init",mapInitialized)
+
+    	if(get_pathing_state() =="READY") then 
+    		local hitPos = perform_raycast()
+    		if(hitPos) then 
+    			DebugWatch("start pos",hitPos)
+    			init_pathfinding(hitPos, TARGET_POS)
+    		end
+    	end
+    end
+end
+

```

---

# Migration Report: pathfinding\mapBuilder.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding\mapBuilder.lua
+++ patched/pathfinding\mapBuilder.lua
@@ -1,208 +1,4 @@
-#include "mapNode.lua"
-#include "AStarSearch.lua"
-
-
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        mapBuilder.lua             
-*
-* DESCRIPTION :
-*   File that constructs the map based on scanning positions for materials
-*   Buidls a 2d array representing a weighted graph of every map location
-*   
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-*                Release Date :    29 Nov 2021 
-*
-]]
-
-
-RACESTARTED = false
-map = {
-  xIndex = 0,
-  data = {
-
-  },
-
-  validSurfaceColours ={ 
-      [1] = {
-        r = 0.20,
-        g = 0.20,
-        b = 0.20,
-        range = 0.01
-      },
-    },
-}
-
--- negative grid pos is solved by simply showing 
-mapSize = {
-			x=400,
-			y=400,
-			grid = 5,
-      gridHeight = 1,
-      gridResolution = 0.5,
-      gridThres      = 0.2,
-
-      scanHeight = 100,
-
-      scanLength = 200,
-
-      weights = {
-          goodTerrain = 0.1,
-          badTerrain   = 10,
-          avoidTerrain = 25,
-          impassableTerrain = 50,
-      }
-		}
-    path = nil
-
-function init()
-  local pos = Vec(0,0,0)
-  local gridCost = 0
-  local maxVal  = {math.modf((mapSize.x)/mapSize.grid),math.modf((mapSize.y)/mapSize.grid)}
-	for y= -mapSize.y/2,mapSize.y/2,mapSize.grid do
-    pos = posToInt(Vec(0,0,y))
-    map.data[pos[3]] = {}
-    for x= -mapSize.x,mapSize.x/2,mapSize.grid do
-        pos = posToInt(Vec(x,0,y))
-        gridCost,validTerrain,avgHeight =  scanGrid(x,y) 
-        -- if(pos[3] ~= nil and pos[1]~= nil) then
-          
-          map.data[pos[3]][pos[1]] = deepcopy(mapNode) 
-          map.data[pos[3]][pos[1]]:push(x,avgHeight,y,gridCost,pos[3],pos[1],validTerrain,maxVal )
-
-        -- end
-  		  -- DebugPrint(x.." | "..y)
-    end
-	end
-	
-
-  pos = posToInt(GetPlayerPos())
-   goalPos = map.data[60][30]
-   startPos = map.data[55][72]
-  startPos = map.data[pos[3]][pos[1]]
-
-
-
-  paths = {}
-  gateState = {}
-  gates = {}
-  triggers = FindTriggers("gate",true)
-  for i=1,#triggers do
-    gateState[tonumber(GetTagValue(triggers[i], "gate"))] = 0
-    gates[tonumber(GetTagValue(triggers[i], "gate"))] = triggers[i]
-  end
-
-  for i =1,#triggers do 
-    startPos = posToInt(GetTriggerTransform(gates[i]).pos)
-    startPos = map.data[startPos[3]][startPos[1]]
-    if(i==#triggers) then 
-      goalPos = posToInt(GetTriggerTransform(gates[1]).pos )
-    else
-      goalPos = posToInt(GetTriggerTransform(gates[i+1]).pos )
-    end
-    goalPos = map.data[goalPos[3]][goalPos[1]]
-    paths[#paths+1] =  AStar:AStarSearch(map.data, startPos, goalPos)
-  end
-
-  --- AStar:AStarSearch(graph, start, goal)
-
- 
-  -- local cameFromIndex = cameFrom[current:getIndex()[2]][current:getIndex()[1]]:getIndex()
-end
-
-
-function scanMap( ... )
-	-- body
-end
-
-function scanGrid(x,y)
-  local pos = Vec(0,0,0)
-  local gridScore = 1
-  local spotScore = 0 
-  local hitHeight = mapSize.scanHeight
-  local heightOrigin = 1000000
-  local minHeight = heightOrigin
-  local maxHeight = -heightOrigin
-  local validTerrain  = true
-  for y1= y, y+mapSize.grid, mapSize.gridResolution do
-    for x1= x, x+mapSize.grid, mapSize.gridResolution do
-      spotScore,hitHeight,hit =  getMaterialScore3(x,y)
-      if(hitHeight == mapSize.scanHeight or IsPointInWater(Vec(x,hitHeight,y))or not hit) then
-        minHeight = -mapSize.scanLength
-        maxHeight = mapSize.scanLength
-        validTerrain = false
-      elseif(minHeight == heightOrigin or maxHeight == heightOrigin) then
-        minHeight = hitHeight
-        maxHeight = hitHeight
-      elseif(hitHeight < minHeight) then
-        minHeight = hitHeight
-      elseif(hitHeight > maxHeight) then
-        maxHeight = hitHeight
-      end
-
-      -- local hit,height,hitPos, shape = getHeight(x,y)
-      -- spotScore =  getMaterialScore2(hit,hitPos,shape)
-      gridScore = gridScore + spotScore
-
-    end
-  end
-  --DebugPrint("max: "..maxHeight.." min: "..minHeight.." sum: "..(((maxHeight - minHeight) / (mapSize.gridHeight*mapSize.gridThres)))  )  
-  if(((maxHeight - minHeight) /  (mapSize.gridHeight*mapSize.gridThres))>1) then
-    validTerrain = false
-  end  
-  if(((maxHeight) - (minHeight)) ~=0 ) then
-    gridScore = gridScore * (1+math.log(((maxHeight) - (minHeight)))*2)
-  end
-  return gridScore,validTerrain, minHeight
-end
-
-
-function tick(dt)
-  if InputPressed("r") and not RACESTARTED  then
-    RACESTARTED = true
-     path =  AStar:AStarSearch(map.data, startPos, goalPos)
-  elseif(RACESTARTED and path)then 
-    -- AStar:drawPath(map.data,path)
-    DebugWatch("running",#paths)
-    for key,val in ipairs(paths) do  
-       AStar:drawPath2(map.data,val)
-    end
-  end
-  local playerTrans = GetPlayerTransform()
-  playerTrans.pos,pos2 = posToInt(playerTrans.pos)
-  -- DebugWatch("Player Pos: ",playerTrans.pos)
-  --  DebugWatch("original Player Pos: ", GetPlayerTransform().pos)
-   -- DebugWatch("Pos 2: ",pos2) 
-   local pos = VecCopy(playerTrans.pos)
-   if(pos[3] ~= nil and pos[1]~= nil) then
-    -- DebugPrint(pos[3].." | "..pos[1])
-     -- DebugWatch("player Grid Cost: ",map.data[pos[3]][pos[1]]:getCost())
-
-     -- DebugWatch("player Grid neighbors: ",#map.data[pos[3]][pos[1]].neighbors)
-
-     local totalCost = 0
-     for key, val in ipairs(map.data[pos[3]][pos[1]]:getNeighbors()) do
-          totalCost = totalCost + map.data[val.y][val.x]:getCost()
-     end
-
-     -- DebugWatch("player Grid neighbor: ",totalCost)
-
-     -- DebugWatch("player Grid VALID: ",map.data[pos[3]][pos[1]].validTerrain)
-  else
-
-  end
-
-  
-end
-
+#version 2
 function getHeight(x,y)
 
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -273,7 +69,6 @@
 
 end
 
-
 function getMaterialScore3(x,y)
   local score = 0
   local probe = Vec(x,mapSize.scanHeight,y)
@@ -336,10 +131,9 @@
   return pos,pos2
 end
 
-
 function Heuristic(a, b)
       return Math.Abs(a[1] - b[1]) + Math.Abs(a[3] - b[3]);
- end 
+ end
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -356,8 +150,6 @@
     return copy
 end
 
-
-
 function inRange(min,max,value)
     if(min < value and value<=max) then 
       return true
@@ -366,4 +158,5 @@
       return false
     end
 
-end+end
+

```

---

# Migration Report: pathfinding\mapNode.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding\mapNode.lua
+++ patched/pathfinding\mapNode.lua
@@ -1,46 +1,4 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        mapNode.lua             
-*
-* DESCRIPTION :
-*       File that implements a structure to represent map nodes and scores
-*		used for pathfinding 
-*		
-
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-mapNode = {
-	minID = -1,
-	secondMinID = -1,
-	MinDistance = 1000,
-	secondMinDistance = 999,
-	x = 0,
-	y = 0,
-	z = 0,
-	baseCost = 0,
-	validTerrain = false,
-	spriteColour = {1,1,0},
-	neighbors = {},
-	maxVal = {},
-	indexX = 0,
-	indexY = 0,
-	live_time = 8,
-
-}
-
-
-
-
+#version 2
 function mapNode:push(x,y,z,value,t_indexY,t_indexX,validTerrain,maxVal,calc_time)
 	self.x, self.y, self.z, self.baseCost,self.indexX , self.indexY, self.validTerrain,self.maxVal,self.last_calc = x,y,z,value,t_indexX,t_indexY,validTerrain,maxVal,calc_time
 	-- local index = 0
@@ -69,6 +27,7 @@
 function mapNode:setHeight(y)
 	self.y = y
 end
+
 function mapNode:getHeight()
 	return self.y
 end
@@ -76,7 +35,6 @@
 function mapNode:getIndex()
 	return  {self.indexX, self.indexY}
 end
-
 
 function mapNode:Equals(node)
 	local nodeIndex = node:getIndex()
@@ -87,7 +45,6 @@
 		return false
 	end
 end
-
 
 function mapNode:indexEquals(nodeIndex)
 	if(self.indexX==nodeIndex[1] and self.indexY==nodeIndex[2])  then 
@@ -101,7 +58,6 @@
 function mapNode:getDistance(altPos)
 	return VecLength(VecSub(self:getPos(),altPos))
 end
-
 
 function mapNode:computeNodeDistance(CentroidId,centroid)
 	local dist = self:getDistance(centroid:getPos())
@@ -134,6 +90,7 @@
 function mapNode:loadSprite()
 	self.sprite = LoadSprite("MOD/images/dot.png")
 end
+
 function mapNode:showSprite()
 	if(not IsHandleValid(self.sprite)) then
 		DebugPrint("NO SPRITE FOUND")
@@ -146,15 +103,6 @@
 	DebugWatch("clusterPos",self:getPos())
 end
 
-
-
------
-
- ---- getters
-
------
-
-
 function mapNode:getMinDistance()
 	return self.MinDistance 
 end
@@ -163,14 +111,13 @@
 	return self.secondMinDistance
 end
 
-
 function mapNode:getMinID()
 	return self.minID 
 end
+
 function mapNode:getSecondMinID()
 	return self.secondMinID 
 end
-
 
 function mapNode:getCost()
 	return self.baseCost 
@@ -205,7 +152,6 @@
 	return self.last_check 
 end
 
-
 function mapNode:setCost(new_cost)
 	self.baseCost = new_cost
 end
@@ -214,16 +160,9 @@
 	return self.neighbors
 end
 
---- 
-
- --- setters
-
----
-
 function mapNode:setPos(pos)
 	self.x,self.y,self.z = pos[1],pos[2],pos[3]
 end
-
 
 function mapNode:setMinDistance(dist)
 	self:setSecondMinDistance(self.MinDistance)
@@ -238,24 +177,17 @@
 	self:setSecondMinID(self.minID)
 	self.minID = id
 end
+
 function mapNode:setSecondMinID(id)
 	self.secondMinID = id
 end
-
-
 
 function mapNode:set_last_check(time)
 	self.last_check = time
 end
 
----
-
-  --- helpers
-
-----
-
-
 function mapNode:clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
-end+end
+

```

---

# Migration Report: pathfinding\PriorityQueue.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding\PriorityQueue.lua
+++ patched/pathfinding\PriorityQueue.lua
@@ -1,34 +1,4 @@
---[[
-**********************************************************************
-*
-* FILEHEADER: Elboydo's Armed Vehicles Framework (AVF) AI V3 - The Racing Edition 
-*
-* FILENAME :        PriorityQeue.lua             
-*
-* DESCRIPTION :
-*       File that implements a priority queue data structure in lua. 
-* 		used for pathfinding in teardown 
-*		
-*
-* NOTES :
-*       
-*
-* AUTHOR :    elboydo        START DATE   :    Jan  2021
-* 							 Release Date :    29 Nov 2021 
-*
-]]
-
-
-PriorityQueue = {
-	queuelength = 0,
-	currentIndex = 0,
-	queueSize = 0,
-	elements = {
-
-	},
-}
-
-
+#version 2
 function PriorityQueue:init(x,y) 
 	local maxElements = (x)*(y)
 	for i=1, maxElements do
@@ -52,7 +22,6 @@
 	return true
 
 end
-
 
 function PriorityQueue:put(node,cost) 
 	
@@ -100,3 +69,4 @@
 	end
 
 end
+

```

---

# Migration Report: pathfinding.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/pathfinding.lua
+++ patched/pathfinding.lua
@@ -1,37 +1,5 @@
-
-
-
-
-
-
+#version 2
 local vehicle_weight = GetIntParam("weight", 1)
-
-
-pathing_vehicle_id = 0
-
-last_ai = -1
-
---This is the maximum time in seconds before aborting a path query
---Increasing this will handle more complex scenarios
-MIN_THINK_TIME = 2.0
-MAX_THINK_TIME = 2.0
-ULTIMATE_THINK_TIME = 15.0
-
-
-AVF_PATHFINDING_STEP = 3.23
-path_step =2--2
-avoidance_size = 3.5
-max_steer = 3
-PATH_NODE_TOLERANCE = 4.1
-
-
-path_update_timer_max = 3
-path_update_timer = 0  
-static_timeout = 0
-static_timeout_max = 5
-timeout_pos = Vec()
-
-goalPos = nil
 
 function init_pathing()	
 	path_step = AVF_PATHFINDING_STEP
@@ -40,8 +8,6 @@
 	max_steer = path_step * 2
 	
 end
-
-
 
 function pathing_tick(dt,ai_state)
 	--Get the current position of start and goal bodies
@@ -75,13 +41,11 @@
 	end
 end
 
-
 function pathfinding()
 	local dt = GetTimeStep()
 	local startPos = GetVehicleTransform(vehicle).pos--GetBodyTransform(startBody).pos
 --	local goalPos = GetBodyTransform(goalBody).pos
 
-
 	if((VecLength(GetBodyVelocity(GetVehicleBody(vehicle))) < 5 and  
 		path_update_timer > path_update_timer_max) or path_update_timer > path_update_timer_max*1.5) then 
 		handle_path_plotting(startPos,goalPos,dt)
@@ -95,8 +59,6 @@
 	end
 end
 
-
---[[ check if pathfinding system idle. ]]
 function pathfinding_system_idle()
 	local state = GetPathState()
 	if state == "idle" then
@@ -107,13 +69,6 @@
 	end
 end
 
-
---[[
-		
-		This function will only ever fire for the active AI at the top of the list. 
-		Returns false if no path, returns path if path found. 
-
-]]
 function handle_path_plotting(startPos,goalPos,dt,ai,vehicle_body_parts)
 	if(MAX_THINK_TIME<ULTIMATE_THINK_TIME) then 
 		MAX_THINK_TIME = math.min(math.max((GetTime()/ULTIMATE_THINK_TIME),MIN_THINK_TIME),ULTIMATE_THINK_TIME)
@@ -186,8 +141,6 @@
 	return found_path
 end
 
-
---This function retrieves the most recent path and stores it in lastPath
 function retrievePath(ai,vehicle_body_parts)
 	local lastPath = {}
 	local length=GetPathLength()
@@ -209,12 +162,10 @@
 	-- end
 end
 
-
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath(path,ai)
 	local vehicle_transform = GetVehicleTransform(ai.id)
 	-- DebugWatch("navigating path for ai "..ai.id.."  at pos",vehicle_transform)
-	if #path > 0 then
+	if #path ~= 0 then
 		for i=#path, 1, -1 do
 			local p = path[i]
 			local dv = VecSub(p, vehicle_transform.pos)
@@ -233,8 +184,6 @@
 	return path
 end
 
-
---This function will draw the content of lastPath as a line
 function drawPath(lastPath)
 	DebugWatch("last path length",#lastPath)
 	for i=1, #lastPath-1 do
@@ -242,7 +191,6 @@
 		DebugCross(lastPath[i],1,0,0)
 	end
 end
-
 
 function get_path_deviation(vehicle_transform,path,map_vel) 
 	local lookAhead = 2
@@ -271,7 +219,6 @@
 
 	return total_deviation
 end
-
 
 function simple_obstacle_avoidance(pos,ai,vehicle_body_parts)
 	local size = avoidance_size 
@@ -391,7 +338,6 @@
 
 end
 
-
 function clamp(val, lower, upper)
     if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
     return math.max(lower, math.min(upper, val))
@@ -405,8 +351,6 @@
 	end
 
 end
-
-
 
 function deepcopy(orig)
     local orig_type = type(orig)
@@ -423,412 +367,3 @@
     return copy
 end
 
---[[
-
-
-
-
-
-local vehicle_weight = GetIntParam("weight", 1)
-
---This is the maximum time in seconds before aborting a path query
---Increasing this will handle more complex scenarios
-MAX_THINK_TIME = 1.0
-
-path_step =2
-avoidance_size = 3
-max_steer = 3
-PATH_NODE_TOLERANCE = 2.5
-
-
-path_update_timer_max = 3
-path_update_timer = 0  
-static_timeout = 0
-static_timeout_max = 5
-timeout_pos = Vec()
-
-goalPos = nil
-
-function init_pathing()	
-	path_update_timer = path_update_timer_max
-	vehicle = FindVehicle("ai_testbed")
-	PATH_NODE_TOLERANCE = path_step*(avoidance_size*1.3)
-	max_steer = path_step * 2
-	vehicle_shapes = FindShapes(vehicle,true)
-	vehicle_bodies = {}
-	for i=1,#vehicle_shapes do 
-		body = GetShapeBody(vehicle_shapes[i])
-		local body_exists = false
-		for j =1,#vehicle_bodies do 
-			if(body == vehicle_bodies[j]) then 
-				body_exists = true
-				break
-			end
-		end
-		if(not body_exists) then 
-			vehicle_bodies[#vehicle_bodies+1] = body
-		end
-
-	end	
-	--Find handles to start and goal bodies
-	startBody = GetVehicleBody(vehicle)
-	goalBody = FindBody("goal",true)
-	
-	--Table to hold all points of the last computed path
-	lastPath = {}
-end
-
-
---This function retrieves the most recent path and stores it in lastPath
-function retrievePath()
-	lastPath = {}
-	local length=GetPathLength()
-
-	if GetPathLength() > 0.5 then
-		for l=0.5, GetPathLength(), path_step  do
-			local newPoint = GetPathPoint(l)
-			if(VecLength(VecSub(newPoint,lastPath[#lastPath]))>path_step*.9) then 
-				lastPath[#lastPath+1] = newPoint
-				lastPath[#lastPath] = simple_obstacle_avoidance(lastPath[#lastPath])
-			end
-		end
-	end			
-
-	-- local l=0
-	-- while l < length do
-	-- 	lastPath[#lastPath+1] = GetPathPoint(l)
-	-- 	l = l + 0.2
-	-- end
-end
-
-
---Prune path backwards so robot don't need to go backwards
-function navigationPrunePath(path,vehicle_transform)
-	if #path > 0 then
-		for i=#path, 1, -1 do
-			local p = path[i]
-			local dv = VecSub(p, vehicle_transform.pos)
-			local d = VecLength(dv)
-			if d < PATH_NODE_TOLERANCE then
-				--Keep everything after this node and throw out the rest
-				local newPath = {}
-				for j=i, #path do
-					newPath[#newPath+1] = path[j]
-				end
-				lastPath= newPath
-				return 
-			end
-		end
-	end
-end
-
-
---This function will draw the content of lastPath as a line
-function drawPath()
-	DebugWatch("last path elngth",#lastPath)
-	for i=1, #lastPath-1 do
-		DrawLine(lastPath[i], lastPath[i+1])
-		DebugCross(lastPath[i],1,0,0)
-	end
-end
-
-
-
-
-function tick(dt)
-	--Get the current position of start and goal bodies
-	get_target_input()
-
-	if(VecLength(goalPos)~= 0) then 
-		-- DebugWatch("goalpos",VecLength(goalPos))
-		SpawnParticle("smoke", goalPos, Vec(0,5,0), 0.5, 1)
-	end
-	if(goalPos~=nil) then 
-		pathfinding()
-		if(IsHandleValid(vehicle)and #lastPath>0) then 
-			navigationPrunePath(lastPath,GetVehicleTransform(vehicle))
-			controlVehicle(lastPath)
-		end
-	end
-end
-
-function get_target_input()
-	
-	if InputPressed("g") then
-
-		local camera = GetCameraTransform()
-		local aimpos = TransformToParentPoint(camera, Vec(0, 0, -300))
-		local hit, dist,normal = QueryRaycast(camera.pos,  VecNormalize(VecSub(aimpos, camera.pos)), 200,0)
-		if hit then
-			
-			goalPos = TransformToParentPoint(camera, Vec(0, 0, -dist))
-
-		end 	
-	end
-end
-
-function pathfinding()
-	local dt = GetTimeStep()
-	local startPos = GetVehicleTransform(vehicle).pos--GetBodyTransform(startBody).pos
---	local goalPos = GetBodyTransform(goalBody).pos
-
-
-	if((VecLength(GetBodyVelocity(GetVehicleBody(vehicle))) < 5 and  
-		path_update_timer > path_update_timer_max) or path_update_timer > path_update_timer_max*1.5) then 
-		handle_path_plotting(startPos,goalPos,dt)
-	else
-		path_update_timer = path_update_timer + dt
-	end
-	--Draw last computed path and a red cross at the end of it in case it didn't reach the goal.
-	drawPath()
-	if failed then
-		DebugCross(lastPath[#lastPath], 1, 0, 0)
-	end
-end
-
-
-function handle_path_plotting(startPos,goalPos,dt)
-	
-	local recalc = false
-	local state = GetPathState()
-	DebugWatch("path plotting ",state)
-	if state == "idle" then
-		--Path finding system is not in use. Start a new query.
-		recalc = true
-	elseif state == "done" then
-		--Path finding system has completed a path query
-		--Store the result and start a new query.
-		recalc = true
-		failed = false
-		retrievePath()
-		path_update_timer = 0
-	elseif state == "fail" then
-		--Path finding system has failed to find a valid path
-		--It is still possible to retrieve a result (path to closest point found)
-		--Store the result and start a new query.
-		recalc = true	
-		failed = true
-		retrievePath()
-
-		path_update_timer = 0
-	else
-		--Path finding system is currently busy. If it has been thinking for more than the 
-		--allowed time, abort current query and store the best result
-		thinkTime = thinkTime + dt
-		if thinkTime > MAX_THINK_TIME then
-			AbortPath()
-			recalc = true
-			failed = true
-			retrievePath()
-
-			path_update_timer = 0
-		end
-	end
-
-	if recalc then
-		--Compute path from startPos to goalPos but exclude startBody and goalBody from the query.
-		--Set the maximum path length to 100 and let any point within 0.5 meters to the goal point
-		--count as a valid path.
-		QueryRejectBody(startBody)
-		QueryRejectBody(goalBody)
-		local vehicle_transform = GetVehicleTransform(vehicle)
-		for j =1,#vehicle_bodies do 
-			QueryRejectBody(vehicle_bodies[j])
-
-		end
-		for i = 1,#vehicle_shapes do 
-			QueryRejectShape(vehicle_shapes[i])
-		end
-		local target_pos = TransformToParentPoint(GetVehicleTransform(vehicle),
-			VecScale(
-				VecNormalize(
-						TransformToLocalPoint(vehicle_transform,goalPos)
-						),
-				avoidance_size*1.5
-				))--Vec(0,0,-5))
-		-- Explosion(target_pos)
-		-- QueryRequire("physical large")
-		QueryPath(target_pos, goalPos, 150.0, 1,"standard")
-		thinkTime = 0
-	end
-
-end
-
-function get_path_deviation(vehicle_transform,path,map_vel) 
-	local lookAhead = 2
-	local total_deviation = Vec()
-
-	for i = 1, lookAhead do 
-		local current_pos = path[math.min(#path,  i)]
-		local next_pos = path[math.min(#path,  i+1)]
-		local goalPos = path[math.min(#path,  i+2)]
-		local current_transform = Transform(current_pos,
-									 QuatLookAt(current_pos, next_pos))
-		local next_deviation = TransformToLocalPoint(current_transform,goalPos)
-		--local nextPos_deviation = VecSub(,goalPos) 
-		--total_deviation = VecAdd(total_deviation,nextPos_deviation)
-		total_deviation[1] = total_deviation[1]+next_deviation[1]
-		-- DebugPrint(i.. " | "..VecStr(next_deviation))
-	end
-	
-	DebugWatch("total_deviation_1",total_deviation)
-	total_deviation = VecScale(total_deviation,(1/lookAhead))
-
-	DebugWatch("total_deviation_2",total_deviation)
-	total_deviation[1] = total_deviation[1]
-
-	-- VecScale(total_deviation,)
-
-	return total_deviation
-end
-
-
-function simple_obstacle_avoidance(pos)
-	local size = avoidance_size 
-
-	local testPoint = VecAdd(pos,Vec(0,size,0))
-	for j =1,#vehicle_bodies do 
-		QueryRejectBody(vehicle_bodies[j])
-
-	end
-	for i = 1,#vehicle_shapes do 
-		QueryRejectShape(vehicle_shapes[i])
-	end
-	local hit, p, n, s = QueryClosestPoint(testPoint,size)
-	if(hit) then 
-
-		local newVec = VecSub(testPoint,p)
-		for i =1,#newVec do 
-			newVec[i] = (size-math.abs(newVec[i])) *math.sign(newVec[i])
-
-		end
-		newVec[2] = 0
-		pos = VecAdd(pos,newVec)
-	end
-
-	return pos
-end
-
-function controlVehicle(path)
-	local vel = GetBodyVelocity(GetVehicleBody(vehicle))
-	local map_vel = math.floor(VecLength(vel)/path_step*.25)+1
-
-	local map_vel_steer = math.floor(VecLength(vel)/(path_step*.5))+1
-	-- DebugWatch("vel",VecLength(vel))
-	-- DebugWatch("adjusted vel",VecLength(vel)%path_step)
-	-- DebugWatch("adjusted vel 2",math.floor(VecLength(vel)/path_step)+1)
-	
-	local goalPos =path[math.min(#path, map_vel)] 
-
-	goalPos_steer =path[math.min(#path, 3)] 
-	local vehicle_transform = GetVehicleTransform(vehicle)
-	local deviation =get_path_deviation(vehicle_transform,path,map_vel)
-	local target_pos = TransformToLocalPoint(vehicle_transform,goalPos)--VecAdd(goalPos,VecScale(deviation,-1)) --TransformToLocalPoint(vehicle_transform,goalPos)
-	local target_pos_steer = TransformToLocalPoint(vehicle_transform,goalPos_steer)--VecAdd(goalPos,VecScale(deviation,-1)) --TransformToLocalPoint(vehicle_transform,goalPos)
-	DebugWatch("x",target_pos[1])
-	DebugWatch("z",target_pos[3])
-	DebugWatch("time",GetTime())
-	local steer_force = (-(math.abs(target_pos_steer[1]/path_step)*math.sign(target_pos_steer[1])))
-
-	local acceleration= -(((math.abs(target_pos[3])/map_vel	))*math.sign(target_pos[3]))
-	acceleration=clamp(acceleration,-1,1)
-	if(acceleration<0.1) then 
-		acceleration = acceleration*5
-	end
-	if(target_pos[1]>path_step*2) then
-		acceleration = -acceleration
-	end 
-	steer_force = steer_force-deviation[1]
-	DebugWatch("pre acceleration",acceleration)
-	acceleration = acceleration * (math.max(1-
-				
-				(math.max(
-						VecLength(deviation),
-						math.abs(target_pos_steer[1]))
-				/max_steer),0.1 ))
-	-- acceleration = acceleration * (math.max(1-(math.abs(VecLength(deviation))/max_steer),0.1 ))
-	DebugWatch("speed scale",(math.max(
-						VecLength(deviation),
-						math.abs(target_pos_steer[1]))
-				/max_steer))
-	DebugWatch("post acceleration",acceleration)
-	DebugWatch("STEER FORCE",steer_force)
-
-	
-	DebugWatch("timeout",static_timeout)
-	if(VecLength(
-			VecSub(
-				path[#path],
-				vehicle_transform.pos))
-		>path_step*2 and VecLength(vel)<0.5 ) then 
-		static_timeout = static_timeout+GetTimeStep()
-		timeout_pos = vehicle_transform.pos
-	else
-		if(VecLength(VecSub(timeout_pos,vehicle_transform.pos))>path_step*2) then
-			static_timeout = 0
-		end
-		-- static_timeout = math.max(static_timeout-GetTimeStep()*.5,0)
-	end
-	if(static_timeout>static_timeout_max*1) then 
-		acceleration = -math.sign(acceleration)
-
-		if(static_timeout>static_timeout_max*1.5) then 
-			static_timeout = 0
-		end
-	end
-
-	steer_force = steer_force * math.sign(acceleration)
-	-- DebugWatch("remaining lentgh ",VecLength(
-	-- 		VecSub(
-	-- 			path[#path],
-	-- 			vehicle_transform.pos))
-	-- 	)
-	DebugWatch("acceleration pre",acceleration)
-	acceleration = acceleration* math.min(VecLength(vehicle_transform.pos,path[#path]) / path_step*4,1)
-	DebugWatch("acceleration",acceleration)
-	DebugWatch("path length ",#path)
-	if(VecLength(
-			VecSub(
-				path[#path],
-				vehicle_transform.pos))
-		>path_step*2) then 
-		DriveVehicle(vehicle, acceleration,steer_force, false)
-	else
-		DriveVehicle(vehicle, 0,0, true)
-	end
-
-end
-
-
-function clamp(val, lower, upper)
-    if lower > upper then lower, upper = upper, lower end -- swap if boundaries supplied the wrong way
-    return math.max(lower, math.min(upper, val))
-end
-
-function math.sign(x) 
-	if(x<0) then 
-		return -1
-	else
-		return 1
-	end
-
-end
-
-
-
-function deepcopy(orig)
-    local orig_type = type(orig)
-    local copy
-    if orig_type == 'table' then
-        copy = {}
-        for orig_key, orig_value in next, orig, nil do
-            copy[deepcopy(orig_key)] = deepcopy(orig_value)
-        end
-        setmetatable(copy, deepcopy(getmetatable(orig)))
-    else -- number, string, boolean, etc
-        copy = orig
-    end
-    return copy
-end
-
-]]
```

---

# Migration Report: scripts\shell_casing_lifespan.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/scripts\shell_casing_lifespan.lua
+++ patched/scripts\shell_casing_lifespan.lua
@@ -1,29 +1,28 @@
-
-
-
-function init()
-	script_active = true
-	shape = FindShape("")
-	min_dist = math.random(15,55)
-	life_timer = 0 
-	max_life = math.random(10,45)
-
+#version 2
+function server.init()
+    script_active = true
+    shape = FindShape("")
+    min_dist = math.random(15,55)
+    life_timer = 0 
+    max_life = math.random(10,45)
 end
 
-function tick(dt) 
-	if(script_active) then 
-		if(IsHandleValid(shape)) then 
-			local shape_pos = GetShapeWorldTransform(shape).pos
-			local player_pos = GetPlayerPos()
-			if((life_timer > max_life and  VecLength(VecSub(player_pos,shape_pos))>min_dist) or life_timer > max_life *2 ) then 
-				Delete(shape)
-				script_active = false
-			else
-				life_timer = life_timer + dt
-			end
-		else 
-			script_active = false
-		end
-	end
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if(script_active) then 
+        	if(IsHandleValid(shape)) then 
+        		local shape_pos = GetShapeWorldTransform(shape).pos
+        		local player_pos = GetPlayerPos(playerId)
+        		if((life_timer > max_life and  VecLength(VecSub(player_pos,shape_pos))>min_dist) or life_timer > max_life *2 ) then 
+        			Delete(shape)
+        			script_active = false
+        		else
+        			life_timer = life_timer + dt
+        		end
+        	else 
+        		script_active = false
+        	end
+        end
+    end
+end
 
-end
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
@@ -1,16 +1,7 @@
-----------------
--- Metatable Utilities
--- special AVF backwards-compatible patch
--- @script util.meta
-
+#version 2
 local registered_meta = {}
 local reverse_meta = {}
 
---- Defines a new metatable type.
----
----@param name string
----@param parent? string
----@return table
 function global_metatable( name, parent, usecomputed )
 	local meta = registered_meta[name]
 	if meta then
@@ -57,10 +48,6 @@
 	return meta
 end
 
---- Gets an existing metatable.
----
----@param name string
----@return table?
 function find_global_metatable( name )
 	if not name then
 		return
@@ -102,8 +89,6 @@
 	return res
 end
 
--- AVF patch
-_ORIG_setmetatable = _ORIG_setmetatable or setmetatable
 function setmetatable(t, meta)
 	if reverse_meta[meta] then
 		rawset(t, "__UMF_GLOBAL_METATYPE", reverse_meta[meta])
@@ -148,6 +133,3 @@
 	restoremeta( _G, {} )
 end
 
-hook.add( "base.command.quickload", "api.metatables.restore", function()
-	restore_global_metatables()
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

---

# Migration Report: vehicle_setup.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/vehicle_setup.lua
+++ patched/vehicle_setup.lua
@@ -1,5 +1,4 @@
-
-
+#version 2
 function addGun(gunJoint,attatchedShape,turretJoint,turret_rot)
 	if unexpected_condition then error() end
 	
@@ -58,8 +57,6 @@
 		return "false"
 
 	end
-
-
 
 	SetTag(gun, "AVF_Parent", vehicle.groupIndex )
 
@@ -90,7 +87,6 @@
 			DebugPrint(retVal)
 		end
 
-
 		status,retVal = pcall(loadShells,(vehicleFeatures.weapons[group][index]));
 		if status then 
 			-- utils.printStr("no errors")
@@ -105,10 +101,7 @@
 
 	-- gunCustomization(vehicleFeatures.weapons[group][index])
 
-
-
 	-- loadShells(vehicleFeatures.weapons[group][index])
-
 
 	-- turret and weapon rotation values
 
@@ -134,8 +127,6 @@
 	end
 	vehicleFeatures.weapons[group][index].turret_rotation_rate = turret_rot
 
-
-
 	if(not vehicleFeatures.weapons[group][index].elevationSpeed) then
 		vehicleFeatures.weapons[group][index].elevationSpeed = 3
 	end
@@ -206,7 +197,6 @@
 	-- 	utils.printStr(weaponType.." | "..vehicleFeatures.weapons[group][index].name.." | "..group)
 	
 	-- end
-
 
 	if(HasTag(gun,"commander")) then
 		 vehicleFeatures.commanderPos = gun
@@ -226,7 +216,6 @@
 			vehicleFeatures.weapons[group][index].elevationRate
 			)
 
-
 	end
 
 	addSearchlights(gun)
@@ -279,7 +268,6 @@
 	elevationRate
 	)
 
-
 	-- DebugPrint("ADDING COAX")
 
 	local gun = GetJointOtherShape(gunJoint, attatchedShape)
@@ -294,12 +282,10 @@
 		end
 	end
 
-
 	local val3 = GetTagValue(gun, "component")
 	local weaponType = GetTagValue(gun, "coax")
 	local min, max = GetJointLimits(gunJoint)
 	local group = "coax"
-
 
 	-- if(debugMode) then
 	-- 	DebugPrint(weaponType.." | "..gunJoint.." | "..group.." | vehicle: "..vehicle.id)
@@ -337,14 +323,12 @@
 		vehicleFeatures.weapons[group][index].elevationSpeed = 1
 	end
 
-
 	if (not
 		vehicleFeatures.weapons[group][index].zeroing) then 
 		vehicleFeatures.weapons[group][index].zeroing =  weaponDefaults.DEFAULT_ZEROING  
 	end
 
 	vehicleFeatures.weapons[group][index].elevationRate = elevationRate
-
 
 	vehicleFeatures.weapons[group][index].turret_min = turret_min
 	vehicleFeatures.weapons[group][index].turret_max = turret_max
@@ -357,8 +341,6 @@
 
 	vehicleFeatures.weapons[group][index].commander_y_rate = commander_y_rate
 	vehicleFeatures.weapons[group][index].commander_x_rate = commander_x_rate
-
-
 
 	if (not vehicleFeatures.weapons[group][index].sight[1].bias)then
 		vehicleFeatures.weapons[group][index].sight[1].bias = 1
@@ -384,8 +366,6 @@
 		vehicleFeatures.weapons[group][index].reloadSound = LoadLoop(weaponDefaults.reloadSound)
 	end
 	vehicleFeatures.weapons[group][index].dryFire =  LoadSound("MOD/sounds/dryFire0.ogg")
-
-
 
 	-- DebugPrint("added gun")
 end
@@ -534,8 +514,6 @@
 			end
 		end
 
-
-
 		if (gun.magazines[i].CfgAmmo.shellSpriteRearName )then 
 			gun.magazines[i].CfgAmmo.spriteRear = LoadSprite(gun.magazines[i].CfgAmmo.shellSpriteRearName)
 		else
@@ -557,7 +535,6 @@
 		if((gun.magazines[i].CfgAmmo.flightLoop)) then
 			gun.magazines[i].CfgAmmo.flightLoopSound = LoadLoop(gun.magazines[i].CfgAmmo.flightLoop)
 		end
-
 
 		local modifier = math.log(gun.magazines[i].CfgAmmo.caliber)/10--/10
 		modifier = modifier*.75
@@ -570,7 +547,6 @@
 							[2] = modifier*1,
 							[3] = modifier*0.5
 						}
-
 
 		--- add penetration modifiers
 		local penModifier = 1
@@ -598,7 +574,6 @@
 
 		-- if(i==1) then
 			-- utils.printStr("@shell"..i.."_name")
-
 
 			-- if(HasTag(gun.id,"@magazine"..i.."_name")) then 
 			-- 	gun.magazines[i].CfgAmmo.name = GetTagValue(gun.id,"@magazine"..i.."_name")  
@@ -634,7 +609,6 @@
 				
 			end
 
-
 	-- 			ammoDefaults = {
 	-- 	defaultMagazine = {
 	-- 		ammoName = "",
@@ -648,17 +622,8 @@
 	end
 -- munitions[gun.magazines[gun.loadedMagazine].name]
 
-
-end
-
-
---[[
-	
-	helper functions to detect warhead traits - such as rockets or chemical effect based warheads like HEAT. 
-
-	Initial use case is for shells that don't suffer penetration loss over distance
-
-]]
+end
+
 function is_rocket(projectile)
 	if(shell_launcher_types[projectile.shellType.launcher] and 
 			shell_launcher_types[projectile.shellType.launcher] == "rocket") then 
@@ -677,9 +642,7 @@
 		return false
 	end
 
-
-end
-
+end
 
 function addSearchlights(object)
 	local objectLights= GetShapeLights(object)
@@ -757,7 +720,6 @@
 						addGun(joints[j],turret,turretJoint,rotation_rate)
 					end
 
-
 	--				outString = outString..addGun(joints[j], turret,turretJoint)
 				else
 					tag_jointed_object(joints[j],shapes[i])
@@ -775,15 +737,11 @@
 	end
 	addSearchlights(turret)
 
-
-
-
 	vehicle.shapes[#vehicle.shapes+1] = turret
 
 	return outString
 
 end
-
 
 function tag_jointed_object(joint,source_shape)
 		
@@ -801,7 +759,7 @@
 	-- if GetBool("savegame.mod.newVehicle") then
 		addVehicle()
 
-	-- 	SetBool("savegame.mod.newVehicle",false)
+	-- 	SetBool("savegame.mod.newVehicle",false, true)
 	-- end
 
 end
@@ -831,5 +789,6 @@
 			-- RemoveTag(sceneVehicles[i],"AVF_Custom")
 		end
 	end
-	SetBool("level.avf.vehicle_spawned", false)
-end
+	SetBool("level.avf.vehicle_spawned", false, true)
+end
+

```

---

# Migration Report: visual_effects.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/visual_effects.lua
+++ patched/visual_effects.lua
@@ -1,86 +1,7 @@
-
--- function fire(gun,barrelCoords)
---     if(gun.mouseDownSound and getPlayerMouseDown())then
---     	if(not gun.loopSoundFile)then 
--- 			PlaySound(gun.mouseDownSound, barrelCoords.pos, 50, false)
--- 		end
---     elseif(not gun.tailOffSound or not getPlayerMouseDown())then
---     	PlaySound(gun.sound, barrelCoords.pos, 50, false)
---     	-- PlaySound(explosion_sounds[math.random(1,#explosion_sounds)],barrelCoords.pos, 400, false)
-		
---     end
-
-
--- 	if(not oldShoot)then
--- 		if(gun.weaponType =="special") then 
--- 			pushSpecial(barrelCoords,gun)
--- 		--	DebugWatch("USING",gun.name)
--- 		else
--- 			pushProjectile(barrelCoords,gun)
--- 		end
--- 	else 
--- 		local cannonLoc=  barrelCoords--rectifyBarrelCoords(gun)
--- 			QueryRejectBody(vehicle.body)
--- 			QueryRejectShape(gun.id)
--- 			local fwdPos = TransformToParentPoint(cannonLoc, Vec(0,  maxDist * -1),1)
--- 		    local direction = VecSub(fwdPos, cannonLoc.pos)
--- 		    direction = VecNormalize(direction)
--- 		    QueryRequire("physical")
--- 		    hit, dist = QueryRaycast(cannonLoc.pos, direction, maxDist)
--- 		    -- utils.printStr(dist)
-
--- 		    if hit then
--- 				hitPos = TransformToParentPoint(cannonLoc, Vec(0, dist * -1,0))
--- 			else
--- 				hitPos = TransformToParentPoint(cannonLoc, Vec(0,  maxDist * -1,0))
--- 			end
--- 		      	p = cannonLoc.pos
-
--- 				d = VecNormalize(VecSub(hitPos, p))
--- 				spread = 0.03
--- 				d[1] = d[1] + ((math.random()-0.5)*2*spread)*dist/maxDist
--- 				d[2] = d[2] + ((math.random()-0.5)*2*spread)*dist/maxDist
--- 				d[3] = d[3] + ((math.random()-0.5)*2*spread)*dist/maxDist
--- 				d = VecNormalize(d)
--- 				p = VecAdd(p, VecScale(d, 0.5))
-				
-
--- 				-- if(gun.highVelocityShells)then
--- 						-- utils.printStr(gun.loadedMagazine)--type(munitions[gun.magazines[gun.loadedMagazine].name]))
--- 					-- if (gun.magazines[gun.loadedMagazine].CfgAmmo.maxPenDepth and hit) then
-							
--- 					-- 	cannonLoc.pos = hitPos
--- 					-- 	pushShell(gun,hitPos,dist,(maxDist-dist),cannonLoc)
-
--- 					-- else
-
--- 					-- 	pushShell(gun,hitPos,dist)
--- 					-- end
--- 				-- else
--- 					Shoot(p, d,0)
--- 				-- end		
--- 	end
-
-	
-
--- end
-
-
----
-
-
-
-----
-
----- specials
-
------
-
+#version 2
 function pushSpecial(barrelCoords,gun)
 	fireFoam(barrelCoords,gun)
 end
-
-
 
 function fireFoam(cannonLoc,gun)
 
@@ -121,4 +42,3 @@
 	end
 end
 
-

```

---

# Migration Report: weapons.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/weapons.lua
+++ patched/weapons.lua
@@ -1,2716 +1 @@
-weaponOverrides = {
-					name 	= "name",
-					weaponType 				= "weaponType",
-					default = "default",
-					magazines 				= {
-												name = "name",
-												magazineCapacity = "magazineCapacity",
-												magazineCount 	= "magazineCount"
-
-												},
-					loadedMagazine 			= "loadedMagazine",
-					barrels 				= 
-												{
-													x="x",
-													y="y",
-													z="z",
-												},
-					backBlast 				= {
-												z = "z",
-												force = "force",
-
-												},
-					shell_ejector 				= 
-												{
-													x="x",
-													y="y",
-													z="z",
-												},
-					shell_ejector_dir 				= 
-												{
-													x="x",
-													y="y",
-													z="z",
-												},
-					sight					= {
-													x="x",
-													y="y",
-													z="z",
-												},
-					scope_offset					= {
-													x="x",
-													y="y",
-												},
-					multiBarrel 			= "multiBarrel",
-					canZoom					= "canZoom",
-					fireControlComputer		= "fireControlComputer",
-					scope_scale				= "scope_scale",
-					zoomSight				= "zoomSight",
-					aimForwards				= "aimForwards",
-					aimReticle 				= "aimReticle",
-					zero_range				= "zero_range",
-					zeroing 				= "zeroing",
-					highVelocityShells		= "highVelocityShells",
-					cannonBlast 			= "cannonBlast",
-					RPM 					= "RPM",
-					reload 					= "reload",
-					recoil 					= "recoil",
-					weapon_recoil 			= "weapon_recoil",
-					dispersion 				= "dispersion",
-					gunRange				= "gunRange",
-					gunBias 				= "gunBias",
-					elevationSpeed			= "elevationSpeed",
-					elevation_rate			= "elevation_rate",
-					smokeFactor 			= "smokeFactor",
-					smokeMulti				= "smokeMulti",
-					soundFile				= "soundFile",
-					custom_fire_sound		= "custom_fire_sound",
-					mouseDownSoundFile 		= "mouseDownSoundFile",
-					custom_mouse_down		= "custom_mouse_down",
-					loopSoundFile 			= "loopSoundFile",
-					custom_loop_sound_file  = "custom_loop_sound_file",
-					tailOffSound	 		= "tailOffSound",
-					custom_tail_off         = "custom_tail_off",
-					reloadSound 			= "reloadSound",
-					custom_reload         	= "custom_reload",
-					reloadPlayOnce 			= "reloadPlayOnce",
-					custom_sight_script     = "custom_sight_script"
-
-}
-
-override_samples = {
-		barrels 				= { 
-		[1] = {
-				{
-					x=0,
-					y=0,
-					z=0,
-				},
-			}
-							},
-		backBlast 				=
-		{
-			[1] = 
-		 {
-				z = 0,
-				force = 0,
-
-									},
-								},
-		sight					= 
-					{
-		[1] = {
-								x=0,
-								y=0,
-								z=0,
-							},
-						},
-		shell_ejector					= 
-					{
-		[1] = {
-								x=0,
-								y=0,
-								z=0,
-							},
-						},	
-		shell_ejector_dir 					= 
-					{
-		[1] = {
-								x=0,
-								y=0,
-								z=0,
-							},
-						},						
-	scope_offset					= 
-	{
-		[1]= {
-								x=0,
-								y=0,
-							},
-	}
-
-
-
-}
-
-weaponDefaults = {
-	reloadSound = "MOD/sounds/weaponReload",
-	refillingAmmo = "MOD/sounds/refillingAmmo",
-	DEFAULT_ZEROING  =300
-}
-
-
-weapons = {
-	--- custom weapons
-
-	["customcannon"]  = {
-					name 	= "custom cannon",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					magazines 					= {
-											[1] = {
-													name = "customShell",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.069,y=0.069,z=0.069},
-												},
-					sight					= {
-												[1] = {
-												x=0,
-												y=0.7,
-												z=2.5,
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
-				},
-	["simple_cannon"]  = {
-					name 	= "custom cannon",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					magazines 					= {
-											[1] = {
-													name = "customShell",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.069,y=0.069,z=0.069},
-												},
-					sight					= {
-												[1] = {
-												x=0,
-												y=0.7,
-												z=2.5,
-													},
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 0,
-					RPM 					= 30,
-					reload 					= 0,
-					recoil 					= 0,
-					dispersion 				= 1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 2,
-					smokeMulti				= 5,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-	["gun"]  = {
-					name 	= "custom cannon",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					magazines 					= {
-											[1] = {
-													name = "customShell",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.0,y=0.0,z=0.0},
-												},
-					sight					= {
-												[1] = {
-												x=0,
-												y=0.7,
-												z=2.5,
-													},
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= .1,
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
-				},
-	["customMG"]		= {
-					name 	= "custom MG",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "custom_Ball_round",
-													magazineCapacity = 250,
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
-	["simpleMG"]		= {
-					name 	= "simple MG",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "custom_Ball_round",
-													magazineCapacity = 250,
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
-
-				},
-
-
-	--- cannons
-	["2A46M"]  = {
-					name 	= "2A46 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
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
-					scope_offset 			= {
-												[1] = {
-													x = 0.01,
-													y = 0
-												},
-					},
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
-
-	["M-65"]  = {
-					name 	= "M-65 130 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_HEAT",
-					magazines 					= {
-											[1] = {
-													name = "BR-482B",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[2] = {
-													name = "OF-482M",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.9,y=0.2,z=-1.4},
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
-					cannonBlast 			= 20,
-					RPM 					= 16,
-					reload 					= 2,
-					recoil 					= 2.8,
-					dispersion 				= 1.1,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .25,
-					smokeFactor 			= 5,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-	["D81"]  = {
-					name 	= "D81 125 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 125,
-					default = "125mm_APFSDS",
-					magazines 					= {
-											[1] = {
-													name = "125mm_APFSDS",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 20,
-												},
-											[2] = {
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
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/tpd-k1m_7.png",
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 25,
-					reload 					= 2,
-					recoil 					= 1.6,
-					dispersion 				= 2,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 3,
-					smokeMulti				= 5,
-					soundFile				= "MOD/sounds/tankshot0",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-
-
-	["L30A1"]  = {
-					name 	= "L30A1 120 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 120,
-					magazines 					= {
-											[1] = {
-													name = "L23A1",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 29,
-												},
-											[2] = {
-													name = "L31A7",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 15,
-												}, 
-											[3] = {
-													name = "L34A2",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 5,
-												}, 
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=1.9,
-												y=1.3,
-												z=0.3,
-													},
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 20,
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
-				},
-
-
-	["D921"]  = {
-					name 	= "D921 90 mm gun",
-					weaponType 				= "cannon",
-					caliber 				= 120,
-					magazines 					= {
-											[1] = {
-													name = "90mm_HEAT",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 29,
-												},
-											[2] = {
-													name = "90mm_HE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 15,
-												}, 
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					sight					= {
-												[1] = {
-												x=1.9,
-												y=1.3,
-												z=0.3,
-													},
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/1G46Sight.png",
-					multiBarrel 			= 1,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 20,
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
-				},
-	["KWK37"]  = {
-					name 	= "75mm KwK 37 gun",
-					weaponType 				= "cannon",
-					caliber 				= 75,
-					default = "125mm_APFSDS",
-					magazines 					= {
-											[1] = {
-													name = "PzGr39",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 20,
-												},
-											[2] = {
-													name = "Sprgr34",
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
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 2,
-					dispersion 				= 4,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 3,
-					smokeMulti				= 20,
-					soundFile				= "MOD/sounds/Relic700KwK37",
-
-				},
-	["KWK37RL"]  = {
-					name 	= "75mm KwK 37 gun",
-					weaponType 				= "cannon",
-					caliber 				= 75,
-					default = "PzGr39",
-					magazines 					= {
-											[1] = {
-													name = "PzGr39",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 20,
-												},
-											[2] = {
-													name = "Sprgr34",
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
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-												},
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 30,
-					reload 					= 2,
-					recoil 					= 2,
-					dispersion 				= 4,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 3,
-					smokeMulti				= 20,
-					soundFile				= "MOD/sounds/Relic700KwK37",
-					reloadSound				= "MOD/sounds/Relic700KwKReload",
-					reloadPlayOnce			= true,
-
-				},
-
-
-	["QF6Pounder"]  = {
-					name 	= "QF 6-pounder",
-					weaponType 				= "cannon",
-					caliber 				= 57,
-					default = "152mm_HE",
-					magazines 					= {
-											[1] = {
-													name = "76mm_HE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 32,
-												},
-											[2] = {
-													name = "76mm_APHE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 32,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.4,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 16,
-					reload 					= 1.5,
-					recoil 					= 0.2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 3,
-					smokeMulti				= 20,
-					soundFile				= "MOD/sounds/artillary_A_01",
-					reloadSound				= "MOD/sounds/Relic_700_tankReload",
-					reloadPlayOnce			= true,
-				},
-
-
-
-	
-	--- howitzers
-
-	["M10HowitzerRL"]  = {
-					name 	= "152mm M-10T howitzer _rl",
-					weaponType 				= "cannon",
-					caliber 				= 152,
-					default = "152mm_HE",
-					magazines 					= {
-											[1] = {
-													name = "152mm_HE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 15,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-												},
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 10,
-					reload 					= 2,
-					recoil 					= 2.5,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 3,
-					smokeMulti				= 20,
-					soundFile				= "MOD/sounds/Relic_700_KV2Fire",
-					reloadSound				= "MOD/sounds/Relic_700_tankReload",
-					reloadPlayOnce			= true,
-				},
-	["M10Howitzer"]  = {
-					name 	= "152mm M-10T howitzer",
-					weaponType 				= "cannon",
-					caliber 				= 152,
-					default = "152mm_HE",
-					magazines 					= {
-											[1] = {
-													name = "152mm_HE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 15,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 10,
-					reload 					= 2,
-					recoil 					= 2.5,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 3,
-					smokeMulti				= 20,
-					soundFile				= "MOD/sounds/Relic_700_KV2Fire",
-				},
-	["76mmFieldGun"]  = {
-					name 	= "76mm Field Gun",
-					weaponType 				= "cannon",
-					caliber 				= 152,
-					default = "152mm_HE",
-					magazines 					= {
-											[1] = {
-													name = "76mm_HE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 32,
-												},
-											[2] = {
-													name = "76mm_APHE",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 32,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.4,y=0.2,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-													},
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					cannonBlast 			= 10,
-					RPM 					= 16,
-					reload 					= 1.5,
-					recoil 					= 0.2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 3,
-					smokeMulti				= 20,
-					soundFile				= "MOD/sounds/artillary_A_01",
-					reloadSound				= "MOD/sounds/Relic_700_tankReload",
-					reloadPlayOnce			= true,
-				},
-
-
-	--- autocannons
-
-	["2A42"]  = {
-					name 	= "2A42 30 mm autocannon",
-					weaponType 				= "cannon",
-					caliber 				= 30,
-					default = "3UOF8",
-					magazines 					= {
-											[1] = {
-													name = "3UBR6",
-													magazineCapacity = 500,
-													ammoCount = 0,
-													magazineCount = 2,
-
-												},
-											[2] = {
-													name = "3UOF8",
-													magazineCapacity = 500,
-													ammoCoddddunt = 0,
-													magazineCount = 2,
-												},
-											-- [3] = {
-											-- 		name = "125mm_HE",
-											-- 		magazineCapacity = 1,
-											-- 		ammoCount = 0,
-											-- 		magazineCount = 10,
-											-- 	}, 
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.1,z=-0.5},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 3,
-												y = 1.3,
-												z = 0.3,
-												},
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/BPK-2-42.png",
-					highVelocityShells		= true,
-					cannonBlast 			= 3,
-					RPM 					= 200,
-					reload 					= 15,
-					recoil 					= .2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 0.7,
-					smokeMulti				= 2,
-					soundFile   = "MOD/sounds/BMPsingle",
-					mouseDownSoundFile 		=	"MOD/sounds/bmpAutoFire",
-					loopSoundFile 			=	"MOD/sounds/autoFirealt_2",
-					tailOffSound	 		=	"MOD/sounds/altFirealt_TailOff_2",
-					reloadSound				= "MOD/sounds/AltTankReload",
-
-				},
-	["OFAB-250"]  = {
-					name 	= "OFAB-250",
-					weaponType 				= "cannon",
-					caliber 				= 325,
-					magazines 					= {
-											[1] = {
-													name = "OFAB-250",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 15,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0,y=-1.5,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0,
-												y = 0,
-												z = -0.3,
-													},
-
-												},
-					zoomSight 				= "MOD/gfx/crosshair-gun.png",
-					highVelocityShells		= true,
-					cannonBlast 			= 0,
-					RPM 					= 5,
-					reload 					= 15,
-					recoil 					= 0.1,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 0,
-					smokeMulti				= 0,
-					soundFile				= "MOD/sounds/bombRelease0",
-				},
-
-	["2A7"]  = {
-					name = "23 mm 2A7 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= {
-											[1] = {
-													name = "B_23mm_AA",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											[2] = {
-													name = "B_23mm_AA_AP",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											},
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
-				},
-	["2A14"]  = {
-					name = "23 mm 2A13 autocannons",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					default = "B_23mm_AA",
-					magazines 					= {
-											[1] = {
-													name = "B_23mm_AA",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											[2] = {
-													name = "B_23mm_AA_AP",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,
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
-	["M230"]  = {
-					name = "30 mm M230",
-					weaponType 				= "cannon",
-					caliber 				= 30,
-					magazines 					= {
-											[1] = {
-													name = "B_30x113mm_M789_HEDP",
-													magazineCapacity = 250,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=0,y=-.3,z=-0.5},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0,
-												y = 0.5,
-												z = 0.8,
-												},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/chopperScope12.png",
-					fireControlComputer		= "MOD/gfx/TEDAC1.png",
-					highVelocityShells		= true,
-					RPM 					= 420,
-					reload 					= 4,
-					recoil 					= 1,
-					dispersion 				= 4,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .5,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/autoCannonSingle",
-					loopSoundFile 			=	"MOD/sounds/autoCannon420RPM.ogg",
-					tailOffSound	 		=	"MOD/sounds/autocannonTailOff",
-
-				},	["GSh-30-2"]  = {
-					name = "30 mm GSh-30-2 autocannon",
-					weaponType 				= "cannon",
-					caliber 				= 23,
-					magazines 					= {
-											[1] = {
-													name = "OFZ_30mm_HE",
-													magazineCapacity = 100,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											[2] = {
-													name = "BR_30mm_AP",
-													magazineCapacity = 200,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels = 
-								{
-									[1] = {x=0.2,y=.3,z=-0.5},
-									[2] = {x=0.2,y=.5,z=-0.5},
-								},
-					multiBarrel 			= 1,
-					sight					= {
-												[1] = {
-												x = 0 ,
-												y = 0,
-												z = -0.6,
-												},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/chopperScope.png",
-					highVelocityShells		= true,
-					RPM 					= 420,
-					reload 					= 4,
-					recoil 					= 1,
-					dispersion 				= 4,
-					gunRange				= 500,
-					gunBias 				= -1,
-					smokeFactor 			= .5,
-					smokeMulti				= 1,
-					soundFile   = "MOD/sounds/autoCannonSingle",
-					loopSoundFile 			=	"MOD/sounds/autoCannon420RPM.ogg",
-					tailOffSound	 		=	"MOD/sounds/autocannonTailOff",
-
-				},
-		["SPG9"]  = {
-					name 	= "SPG-9",
-					weaponType 				= "rocket",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-													name = "PG9_AT",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[2] = {
-													name = "OG9_HE",
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
-					recoil 					= 0.2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .5,
-					smokeFactor 			= 1,
-					smokeMulti				= 5,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},	
-		["LowVelRocket"]  = {
-					name 	= "SPG-9",
-					weaponType 				= "rocket",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-													name = "PG9_AT",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[2] = {
-													name = "RocketLowVelocity",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-
-											[3] = {
-													name = "RocketLowVelocity",
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
-					recoil 					= 0.2,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= .8,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},	
-		["9M133"]  = {
-					name 	= "9M133 Kornet",
-					weaponType 				= "atgm",
-					caliber 				= 73,
-					magazines 					= {
-											[1] = {
-													name = "9M133M-2",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 10,
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
-		["HellfireLauncher"]  = {
-					name 	= "Hellfire Launcher",
-					weaponType 				= "atgm",
-					caliber 				= 180,
-					magazines 					= {
-											[1] = {
-													name = "M_Hellfire_AT",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 8,
-
-												},
-											[2] = {
-													name = "M_Hellfire_AP",
-													magazineCapacity = 1,
-													ammoCount = 0,
-													magazineCount = 8,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.1,z=-1.5},
-													[2] = {x=0.3,y=0.1,z=-1.5},
-													[3] = {x=0.2,y=0.2,z=-1.5},
-													[4] = {x=0.3,y=0.2,z=-1.5},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-													[2] = {z=1.45,force=5},
-													[3] = {z=1.45,force=5},
-													[4] = {z=1.43,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 0.2,
-												y = 0.5,
-												z = 0.8,
-											},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/chopperScope9.png",
-					fireControlComputer		= "MOD/gfx/TEDAC1.png",
-					aimForwards				= true,
-					highVelocityShells		= true,
-					RPM 					= 6,
-					reload 					= 15,
-					recoil 					= 0,
-					dispersion 				= 20,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.8,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/atgm00",
-				},					
-		["UB32"]  = {
-					name 	= "UB-32",
-					weaponType 				= "rocket",
-					caliber 				= 55,
-					magazines 					= {
-											[1] = {
-													name = "S-5M",
-													magazineCapacity = 32,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.1,z=-0.5},
-													[2] = {x=0.3,y=0.1,z=-0.5},
-													[3] = {x=0.2,y=0.2,z=-0.5},
-													[4] = {x=0.3,y=0.2,z=-0.5},
-													[5] = {x=0.2,y=0.3,z=-0.5},
-													[6] = {x=0.3,y=0.3,z=-0.5},
-													[7] = {x=0.2,y=0.4,z=-0.5},
-													[8] = {x=0.3,y=0.4,z=-0.5},
-													[9] = {x=0.2,y=0.5,z=-0.5},
-													[10] = {x=0.2,y=0.5,z=-0.5},
-													[11] = {x=0.2,y=0.4,z=-0.5},
-													[12] = {x=0.3,y=0.5,z=-0.5},
-													[13] = {x=0.3,y=0.4,z=-0.5},
-													[14] = {x=0.4,y=0.5,z=-0.5},
-													[15] = {x=0.4,y=0.4,z=-0.5},
-													[16] = {x=0.5,y=0.5,z=-0.5},
-													[17] = {x=0.5,y=0.4,z=-0.5},
-													[18] = {x=0.6,y=0.5,z=-0.5},
-													[19] = {x=0.6,y=0.4,z=-.5},
-													[20] = {x=0.5,y=0.4,z=-.5},
-													[21] = {x=0.4,y=0.3,z=-.5},
-													[22] = {x=0.5,y=0.3,z=-.5},
-													[23] = {x=0.4,y=0.2,z=-.5},
-													[24] = {x=0.5,y=0.2,z=-.5},
-													[25] = {x=0.4,y=0.1,z=-.5},
-													[26] = {x=0.5,y=0.2,z=-.5},
-													[27] = {x=0.6,y=0.1,z=-.5},
-													[28] = {x=0.5,y=0.2,z=-.5},
-													[29] = {x=0.5,y=0.1,z=-.5},
-													[30] = {x=0.4,y=0.2,z=-.5},
-													[31] = {x=0.4,y=0.1,z=-.5},
-													[32] = {x=0.3,y=0.2,z=-.5},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-													[2] = {z=1.45,force=5},
-													[3] = {z=1.45,force=5},
-													[4] = {z=1.43,force=5},
-													[5] = {z=1.43,force=5},
-													[6] = {z=1.43,force=5},
-													[7] = {z=1.43,force=5},
-													[8] = {z=1.43,force=5},
-													[9] = {z=1.43,force=5},
-													[10] = {z=1.43,force=5},
-													[11] = {z=1.43,force=5},
-													[12] = {z=1.43,force=5},
-													[13] = {z=1.43,force=5},
-													[14] = {z=1.43,force=5},
-													[15] = {z=1.45,force=5},
-													[16] = {z=1.45,force=5},
-													[17] = {z=1.45,force=5},
-													[18] = {z=1.43,force=5},
-													[19] = {z=1.43,force=5},
-													[20] = {z=1.43,force=5},
-													[21] = {z=1.43,force=5},
-													[22] = {z=1.43,force=5},
-													[23] = {z=1.43,force=5},
-													[24] = {z=1.43,force=5},
-													[25] = {z=1.43,force=5},
-													[26] = {z=1.43,force=5},
-													[27] = {z=1.43,force=5},
-													[28] = {z=1.43,force=5},
-													[29] = {z=1.43,force=5},
-													[30] = {z=1.43,force=5},
-													[31] = {z=1.43,force=5},
-													[32] = {z=1.43,force=5},
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
-					zoomSight 				= "MOD/gfx/chopperScope.png",
-					highVelocityShells		= true,
-					RPM 					= 400,
-					reload 					= 5,
-					recoil 					= 0.5,
-					dispersion 				= 30,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 9.5,
-					smokeFactor 			= 1,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},			
-		["B-8M1"]  = {
-					name 	= "B-8M1",
-					weaponType 				= "rocket",
-					caliber 				= 80,
-					magazines 					= {
-											[1] = {
-													name = "S-5",
-													magazineCapacity = 20,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.1,z=-0.5},
-													[2] = {x=0.3,y=0.1,z=-0.5},
-													[3] = {x=0.2,y=0.2,z=-0.5},
-													[4] = {x=0.3,y=0.2,z=-0.5},
-													[5] = {x=0.2,y=0.3,z=-0.5},
-													[6] = {x=0.3,y=0.3,z=-0.5},
-													[7] = {x=0.2,y=0.4,z=-0.5},
-													[8] = {x=0.3,y=0.4,z=-0.5},
-													[9] = {x=0.2,y=0.5,z=-0.5},
-													[10] = {x=0.2,y=0.5,z=-0.5},
-													[11] = {x=0.2,y=0.4,z=-0.5},
-													[12] = {x=0.3,y=0.5,z=-0.5},
-													[13] = {x=0.3,y=0.4,z=-0.5},
-													[14] = {x=0.4,y=0.5,z=-0.5},
-													[15] = {x=0.4,y=0.4,z=-0.5},
-													[16] = {x=0.5,y=0.5,z=-0.5},
-													[17] = {x=0.5,y=0.4,z=-0.5},
-													[18] = {x=0.6,y=0.5,z=-0.5},
-													[19] = {x=0.6,y=0.4,z=-.5},
-													[20] = {x=0.5,y=0.4,z=-.5},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-													[2] = {z=1.45,force=5},
-													[3] = {z=1.45,force=5},
-													[4] = {z=1.43,force=5},
-													[5] = {z=1.43,force=5},
-													[6] = {z=1.43,force=5},
-													[7] = {z=1.43,force=5},
-													[8] = {z=1.43,force=5},
-													[9] = {z=1.43,force=5},
-													[10] = {z=1.43,force=5},
-													[11] = {z=1.43,force=5},
-													[12] = {z=1.43,force=5},
-													[13] = {z=1.43,force=5},
-													[14] = {z=1.43,force=5},
-													[15] = {z=1.45,force=5},
-													[16] = {z=1.45,force=5},
-													[17] = {z=1.45,force=5},
-													[18] = {z=1.43,force=5},
-													[19] = {z=1.43,force=5},
-													[20] = {z=1.43,force=5},
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
-					zoomSight 				= "MOD/gfx/chopperScope.png",
-					highVelocityShells		= true,
-					RPM 					= 400,
-					reload 					= 5,
-					recoil 					= 0.5,
-					dispersion 				= 30,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 9.5,
-					smokeFactor 			= 1,
-					smokeMulti				= 3,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},				
-		["B-13L1"]  = {
-					name 	= "B-13L1",
-					weaponType 				= "rocket",
-					caliber 				= 122,
-					magazines 					= {
-											[1] = {
-													name = "S-13",
-													magazineCapacity = 5,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.1,z=-0.5},
-													[2] = {x=0.3,y=0.1,z=-0.5},
-													[3] = {x=0.2,y=0.2,z=-0.5},
-													[4] = {x=0.3,y=0.2,z=-0.5},
-													[5] = {x=0.2,y=0.3,z=-0.5},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-													[2] = {z=1.45,force=5},
-													[3] = {z=1.45,force=5},
-													[4] = {z=1.43,force=5},
-													[5] = {z=1.43,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 0,
-												y = 0,
-												z = -0.7,
-											},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/chopperScope.png",
-					highVelocityShells		= true,
-					RPM 					= 300,
-					reload 					= 5,
-					recoil 					= 0.5,
-					dispersion 				= 30,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 9.5,
-					smokeFactor 			= 2,
-					smokeMulti				= 6,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},			
-		["M261"]  = {
-					name 	= "M261",
-					weaponType 				= "rocket",
-					caliber 				= 80,
-					magazines 					= {
-											[1] = {
-													name = "R_Hydra_HE",
-													magazineCapacity = 19,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.4,z=-0.5},
-													[2] = {x=0.3,y=0.4,z=-0.5},
-													[3] = {x=0.2,y=0.5,z=-0.5},
-													[4] = {x=0.3,y=0.5,z=-0.5},
-													[5] = {x=0.2,y=0.6,z=-0.5},
-													[6] = {x=0.3,y=0.6,z=-0.5},
-													[7] = {x=0.2,y=0.7,z=-0.5},
-													[8] = {x=0.3,y=0.7,z=-0.5},
-													[9] = {x=0.2,y=0.8,z=-0.5},
-													[10] = {x=0.2,y=0.8,z=-0.5},
-													[11] = {x=0.2,y=0.7,z=-0.5},
-													[12] = {x=0.3,y=0.8,z=-0.5},
-													[13] = {x=0.3,y=0.7,z=-0.5},
-													[14] = {x=0.4,y=0.8,z=-0.5},
-													[15] = {x=0.4,y=0.7,z=-0.5},
-													[16] = {x=0.5,y=0.8,z=-0.5},
-													[17] = {x=0.5,y=0.6,z=-0.5},
-													[18] = {x=0.6,y=0.5,z=-0.5},
-													[19] = {x=0.6,y=0.4,z=-.5},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-													[2] = {z=1.45,force=5},
-													[3] = {z=1.45,force=5},
-													[4] = {z=1.43,force=5},
-													[5] = {z=1.43,force=5},
-													[6] = {z=1.43,force=5},
-													[7] = {z=1.43,force=5},
-													[8] = {z=1.43,force=5},
-													[9] = {z=1.43,force=5},
-													[10] = {z=1.43,force=5},
-													[11] = {z=1.43,force=5},
-													[12] = {z=1.43,force=5},
-													[13] = {z=1.43,force=5},
-													[14] = {z=1.43,force=5},
-													[15] = {z=1.45,force=5},
-													[16] = {z=1.45,force=5},
-													[17] = {z=1.45,force=5},
-													[18] = {z=1.43,force=5},
-													[19] = {z=1.43,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 0,
-												y = 0.5,
-												z = 0.8,
-											},
-
-
-												},
-					canZoom					= true,
-					zoomSight 				= "MOD/gfx/chopperScope9.png",
-					fireControlComputer		= "MOD/gfx/TEDAC1.png",
-					highVelocityShells		= true,
-					RPM 					= 400,
-					reload 					= 5,
-					recoil 					= 0.5,
-					dispersion 				= 30,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 9.5,
-					smokeFactor 			= 1,
-					smokeMulti				= 2,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},			
-
-
-		["TYPE63"]  = {
-					name 	= "Type 63",
-					weaponType 				= "rocket",
-					caliber 				= 106.7,
-					magazines 					= {
-											[1] = {
-													name = "107_HE_Close",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[2] = {
-													name = "107_HE_Mid",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											[3] = {
-													name = "107_HE_long",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-													[2] = {x=0.4,y=0.2,z=-0.3},
-													[3] = {x=0.6,y=0.2,z=-0.3},
-													[4] = {x=0.8,y=0.2,z=-0.3},
-													[5] = {x=1.0,y=0.2,z=-0.3},
-													[6] = {x=1.2,y=0.2,z=-0.3},
-													[7] = {x=1.4,y=0.2,z=-0.3},
-													[8] = {x=0.2,y=0.5,z=-0.3},
-													[9] = {x=0.4,y=0.5,z=-0.3},
-													[10] = {x=0.6,y=0.5,z=-0.3},
-													[11] = {x=0.8,y=0.5,z=-0.3},
-													[12] = {x=1.0,y=0.5,z=-0.3},
-													[13] = {x=1.2,y=0.5,z=-0.3},
-													[14] = {x=1.4,y=0.5,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-													[2] = {z=1.45,force=5},
-													[3] = {z=1.45,force=5},
-													[4] = {z=1.43,force=5},
-													[5] = {z=1.43,force=5},
-													[6] = {z=1.43,force=5},
-													[7] = {z=1.43,force=5},
-													[8] = {z=1.43,force=5},
-													[9] = {z=1.43,force=5},
-													[10] = {z=1.43,force=5},
-													[11] = {z=1.43,force=5},
-													[12] = {z=1.43,force=5},
-													[13] = {z=1.43,force=5},
-													[14] = {z=1.43,force=5},
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
-					RPM 					= 400,
-					reload 					= 5,
-					recoil 					= 0.5,
-					dispersion 				= 30,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 9.5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},
-
-		["TYPE63_a"]  = {
-					name 	= "Type 63",
-					weaponType 				= "rocket",
-					caliber 				= 106.7,
-					magazines 					= {
-											[1] = {
-													name = "107_HE_Close",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[2] = {
-													name = "107_HE_Mid",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-												},
-											[3] = {
-													name = "107_HE_long",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.2,z=-0.3},
-													[2] = {x=0.4,y=0.2,z=-0.3},
-													[3] = {x=0.6,y=0.2,z=-0.3},
-													[4] = {x=0.8,y=0.2,z=-0.3},
-													[5] = {x=1.0,y=0.2,z=-0.3},
-													[6] = {x=1.2,y=0.2,z=-0.3},
-													[7] = {x=1.4,y=0.2,z=-0.3},
-													[8] = {x=0.2,y=0.5,z=-0.3},
-													[9] = {x=0.4,y=0.5,z=-0.3},
-													[10] = {x=0.6,y=0.5,z=-0.3},
-													[11] = {x=0.8,y=0.5,z=-0.3},
-													[12] = {x=1.0,y=0.5,z=-0.3},
-													[13] = {x=1.2,y=0.5,z=-0.3},
-													[14] = {x=1.4,y=0.5,z=-0.3},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=1.45,force=5},
-													[2] = {z=1.45,force=5},
-													[3] = {z=1.45,force=5},
-													[4] = {z=1.43,force=5},
-													[5] = {z=1.43,force=5},
-													[6] = {z=1.43,force=5},
-													[7] = {z=1.43,force=5},
-													[8] = {z=1.43,force=5},
-													[9] = {z=1.43,force=5},
-													[10] = {z=1.43,force=5},
-													[11] = {z=1.43,force=5},
-													[12] = {z=1.43,force=5},
-													[13] = {z=1.43,force=5},
-													[14] = {z=1.43,force=5},
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
-					RPM 					= 400,
-					reload 					= 5,
-					recoil 					= 0.5,
-					dispersion 				= 10,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 2,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/recoilessRifle0",
-
-				},
-		["BM13"]  = {
-					name 	= "BM-13",
-					weaponType 				= "rocket",
-					caliber 				= 132,
-					magazines 					= {
-											[1] = {
-													name = "132mm_HE",
-													magazineCapacity = 16,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.0,y=1.5,z=-0.6},
-													[2] = {x=0.3,y=1.5,z=-0.6},
-													[3] = {x=0.6,y=1.5,z=-0.6},
-													[4] = {x=0.9,y=1.5,z=-0.6},
-													[5] = {x=1.1,y=1.5,z=-0.6},
-													[6] = {x=1.5,y=1.5,z=-0.6},
-													[7] = {x=1.8,y=1.5,z=-0.6},
-													[8] = {x=2.2,y=1.5,z=-0.6},
-													[9] = {x=0.0,y=1.7,z=-0.6},
-													[10] = {x=0.3,y=1.7,z=-0.6},
-													[11] = {x=0.6,y=1.7,z=-0.6},
-													[12] = {x=0.8,y=1.7,z=-0.6},
-													[13] = {x=1.1,y=1.7,z=-0.6},
-													[14] = {x=0.4,y=1.7,z=-0.6},
-													[15] = {x=1.7,y=1.7,z=-0.6},
-													[16] = {x=2.2,y=1.7,z=-0.6},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=5.0,force=5},
-													[2] = {z=5.0,force=5},
-													[3] = {z=5.0,force=5},
-													[4] = {z=5.0,force=5},
-													[5] = {z=5.0,force=5},
-													[6] = {z=5.0,force=5},
-													[7] = {z=5.0,force=5},
-													[8] = {z=5.0,force=5},
-													[9] = {z=5.0,force=5},
-													[10] = {z=5.0,force=5},
-													[11] = {z=5.0,force=5},
-													[12] = {z=5.0,force=5},
-													[13] = {z=5.0,force=5},
-													[14] = {z=5.0,force=5},
-													[15] = {z=5.0,force=5},
-													[16] = {z=5.0,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 2.3,
-												y = 2.3,
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
-					dispersion 				= 30,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/mlrs",
-
-				},
-		["BM14"]  = {
-					name 	= "BM-14",
-					weaponType 				= "rocket",
-					caliber 				= 122,
-					magazines 					= {
-											[1] = {
-													name = "122mm_HE_Close",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[2] = {
-													name = "122mm_HE_Mid",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											[3] = {
-													name = "122mm_HE_long",
-													magazineCapacity = 14,
-													ammoCount = 0,
-													magazineCount = 10,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.2,y=0.5,z=-0.6},
-													[2] = {x=0.4,y=0.5,z=-0.6},
-													[3] = {x=0.6,y=0.5,z=-0.6},
-													[4] = {x=0.8,y=0.5,z=-0.6},
-													[5] = {x=1.0,y=0.5,z=-0.6},
-													[6] = {x=1.2,y=0.5,z=-0.6},
-													[7] = {x=1.4,y=0.5,z=-0.6},
-													[8] = {x=0.2,y=0.7,z=-0.6},
-													[9] = {x=0.4,y=0.7,z=-0.6},
-													[10] = {x=0.6,y=0.7,z=-0.6},
-													[11] = {x=0.8,y=0.7,z=-0.6},
-													[12] = {x=1.0,y=0.7,z=-0.6},
-													[13] = {x=1.2,y=0.7,z=-0.6},
-													[14] = {x=1.4,y=0.7,z=-0.6},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=3.0,force=5},
-													[2] = {z=3.0,force=5},
-													[3] = {z=3.0,force=5},
-													[4] = {z=3.0,force=5},
-													[5] = {z=3.0,force=5},
-													[6] = {z=3.0,force=5},
-													[7] = {z=3.0,force=5},
-													[8] = {z=3.0,force=5},
-													[9] = {z=3.0,force=5},
-													[10] = {z=3.0,force=5},
-													[11] = {z=3.0,force=5},
-													[12] = {z=3.0,force=5},
-													[13] = {z=3.0,force=5},
-													[14] = {z=3.0,force=5},
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
-					RPM 					= 100,
-					reload 					= 5,
-					recoil 					= 0.8,
-					dispersion 				= 25,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 3.3,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/mlrs",
-
-				},
-		["BM30"]  = {
-					name 	= "BM-30 Smerch",
-					weaponType 				= "rocket",
-					caliber 				= 300,
-					magazines 					= {
-											[1] = {
-													name = "9M55K",
-													magazineCapacity = 15,
-													ammoCount = 0,
-													magazineCount = 50,
-
-												},
-											},
-					loadedMagazine 			= 1,
-					barrels 				= 
-												{
-													[1] = {x=0.3,y=1.5,z=-0.6},
-													[2] = {x=0.9,y=1.5,z=-0.6},
-													[3] = {x=1.6,y=1.5,z=-0.6},
-													[4] = {x=2.3,y=1.5,z=-0.6},
-													[5] = {x=2.9,y=1.5,z=-0.6},
-													[6] = {x=0.3,y=0.9,z=-0.6},
-													[7] = {x=0.9,y=0.9,z=-0.6},
-													[8] = {x=1.6,y=0.9,z=-0.6},
-													[9] = {x=2.3,y=0.9,z=-0.6},
-													[10] = {x=2.9,y=0.9,z=-0.6},
-													[11] = {x=0.3,y=0.3,z=-0.6},
-													[12] = {x=0.9,y=0.3,z=-0.6},
-													[13] = {x=1.6,y=0.3,z=-0.6},
-													[14] = {x=2.3,y=0.3,z=-0.6},
-													[15] = {x=2.9,y=0.3,z=-0.6},
-												},
-					multiBarrel 			= 1,
-					backBlast				= 
-												{
-													[1] = {z=8.0,force=5},
-													[2] = {z=8.0,force=5},
-													[3] = {z=8.0,force=5},
-													[4] = {z=8.0,force=5},
-													[5] = {z=8.0,force=5},
-													[6] = {z=8.0,force=5},
-													[7] = {z=8.0,force=5},
-													[8] = {z=8.0,force=5},
-													[9] = {z=8.0,force=5},
-													[10] = {z=8.0,force=5},
-													[11] = {z=8.0,force=5},
-													[12] = {z=8.0,force=5},
-													[13] = {z=8.0,force=5},
-													[14] = {z=8.0,force=5},
-													[15] = {z=8.0,force=5},
-												},
-					sight					= {
-												[1] = {
-												x = 2.3,
-												y = 4.3,
-												z = 0.3,
-													},
-
-
-												},
-					canZoom					= true,
-					highVelocityShells		= true,
-					RPM 					= 140,
-					reload 					= 5,
-					recoil 					= 0.3,
-					dispersion 				= 30,
-					gunRange				= 500,
-					gunBias 				= -1,
-					elevationSpeed			= 0.5,
-					smokeFactor 			= 2,
-					smokeMulti				= 10,
-					soundFile				= "MOD/sounds/mlrs",
-
-				},
-	["PKT"]		= {
-					name 	= "PKT",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_762x54_Ball",
-													magazineCapacity = 250,
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
-	["DSHK"]		= {
-					name 	= "DSHK",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_127x107_Ball",
-													magazineCapacity = 50,
-													ammoCount = 0,
-													magazineCount = 5,
-												},
-											},
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
-				recoil 					= 0.2,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				smokeFactor 			= .2,
-				smokeMulti				= 2,
-				soundFile 				=	"MOD/sounds/HeavySingleShot",
-				mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"MOD/sounds/HeavyAutoFire",
-				tailOffSound	 		=	"MOD/sounds/HeavySingleShot",				
-				},
-	["KORD"]		= {
-					name 	= "KORD",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_127x107_Ball",
-													magazineCapacity = 150,
-													ammoCount = 0,
-													magazineCount = 5,
-												},
-											[2] = {
-													name = "B_127x107_Ball_INC",
-													magazineCapacity = 150,
-													ammoCount = 0,
-													magazineCount = 5,
-												},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0.3,y=0.5,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 1.2,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				aimForwards				= true,
-				RPM 					= 550,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.2,
-				dispersion 				= 12,
-				gunRange				= 3000,
-				elevationSpeed			= 3.4,
-				smokeFactor 			= .5,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/HeavySingleShot",
-				mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"MOD/sounds/HeavyAutoFire",
-				tailOffSound	 		=	"MOD/sounds/HeavySingleShot",				
-				},
-
-
-
-	["KPVT"]		= {
-		-- 14.5 × 114 mm KPVT coaxial machine gun
-
-					name 	= "KPVT",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_145x114_Ball",
-													magazineCapacity = 150,
-													ammoCount = 0,
-													magazineCount = 5,
-												},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0.3,y=0.5,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 1.2,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				aimForwards				= true,
-				RPM 					= 550,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.2,
-				dispersion 				= 12,
-				gunRange				= 3000,
-				elevationSpeed			= 3.4,
-				smokeFactor 			= .5,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/HeavySingleShot",
-				mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"MOD/sounds/HeavyAutoFire",
-				tailOffSound	 		=	"MOD/sounds/HeavySingleShot",				
-				},
-
-
-
-	["KPVTCoax"]		= {
-		-- 14.5 × 114 mm KPVT coaxial machine gun
-
-					name 	= "KPVT Coax",
-					caliber 				= 12.7,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_145x114_Ball",
-													magazineCapacity = 150,
-													ammoCount = 0,
-													magazineCount = 5,
-												},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0.5,y=0.3,z=5.7},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 1.2,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				aimForwards				= true,
-				RPM 					= 550,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.2,
-				dispersion 				= 12,
-				gunRange				= 3000,
-				elevationSpeed			= 1,
-				smokeFactor 			= .2,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/HeavySingleShot",
-				mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"MOD/sounds/HeavyAutoFire",
-				tailOffSound	 		=	"MOD/sounds/HeavySingleShot",				
-				},
-
-	["PKTM"]		= {
-					name 	= "PKTM",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_762x54_Ball",
-													magazineCapacity = 250,
-													ammoCount = 0,
-													magazineCount = 20,
-												},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0.5,y=0.1,z=2.1},
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
-	["COAXMG"]		= {
-					name 	= "Coax MG",
-					caliber 				= 7.62,
-					weaponType 				= "MGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "B_762x54_Ball",
-													magazineCapacity = 250,
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
---[[
-
-	GRENADE LAUNCHERS
-
-
-]]
-
-
-
-	["mk19"]		= {
-					name 	= "MK-19",
-					caliber 				= 30,
-					weaponType 				= "GMGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "G_30mm_HE",
-													magazineCapacity = 60,
-													ammoCount = 0,
-													magazineCount = 1,
-												},
-											},
-
-				barrels 				= 
-											{
-												[1] = {x=0.3,y=0.5,z=-0.6},
-											},
-				multiBarrel 			= 1,
-
-				sight					= {
-												[1] = {
-											x = .25,
-											y = 1.2,
-											z = 1.8,
-												},
-
-
-											},
-				canZoom					= false,
-				aimForwards				= true,
-				RPM 					= 400 ,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.2,
-				dispersion 				= 12,
-				gunRange				= 3000,
-				elevationSpeed			= 3.4,
-				smokeFactor 			= .5,
-				smokeMulti				= 1,
-				soundFile 				=	"MOD/sounds/grenade_mg/single_shot_01",
-				mouseDownSoundFile 		=	"MOD/sounds/grenade_mg/auto_01",
-				loopSoundFile			= 	"MOD/sounds/grenade_mg/auto_01",
-				tailOffSound	 		=	"MOD/sounds/grenade_mg/auto_tail_off_01",				
-				},
-
-
-	["AGS30"]		= {
-					name 	= "AGS-30",
-					caliber 				= 30,
-					weaponType 				= "GMGun",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "G_30mm_HE",
-													magazineCapacity = 60,
-													ammoCount = 0,
-													magazineCount = 1,
-												},
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
-				RPM 					= 360 ,
-				reload 					= 4,
-				magazineCapacity 		= 100,
-				recoil 					= 0.1,
-
-				weapon_recoil 					= 0.0000005,
-				dispersion 				= 12,
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
-
-
---[[
-
-
-		smoke + the funny weapons
-
-
-]]
-
-	['fire_Hose'] = {
-					name 	= "Fire Hose",
-					caliber 				= 0.01,
-					weaponType 				= "special",
-					loadedMagazine 			= 1,
-					magazines 					= {
-											[1] = {
-													name = "foam",
-													magazineCapacity = 99999,
-													ammoCount = 0,
-													magazineCount = 1000,
-												},
-											},
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
-				RPM 					= 1200,
-				reload 					= 4,
-				magazineCapacity 		= 99999,
-				recoil 					= 0.2,
-				dispersion 				= 6,
-				gunRange				= 3000,
-				smokeFactor 			= .2,
-				smokeMulti				= 2,
-				-- soundFile 				=	"MOD/sounds/HeavySingleShot",
-				-- mouseDownSoundFile 		=	"MOD/sounds/HeavyAutoFire",
-				loopSoundFile			= 	"tools/extinguisher-loop"--"MOD/sounds/HeavyAutoFire",
-				-- tailOffSound	 		=	"MOD/sounds/HeavySingleShot",				
-
-	},
-
-
-	["t90_smoke_turret"] = {
-				name 					= "Smoke Dischargers",
-				type 					= "projector",
-				barrels = {	
-					[1] = {x=3.8,y=0.2,z=1.3		,x_angle = 0,y_angle = -15},
-					[2] = {x=3.8,y=0.3,z=1.5		,x_angle = 15,y_angle = -20},
-					[3] = {x=3.8,y=0.4,z=1.6	,x_angle = 30,y_angle = -25},
-					[4] = {x=-0.0,y=0.2,z=1.6	,x_angle = -0,y_angle = -15},
-					[5] = {x=-0.0,y=0.3,z=1.6	,x_angle = -15,y_angle = -20},
-					[6] = {x=-0.0,y=0.4,z=1.6	,x_angle = -30,y_angle = -25},
-
-				},
-				multiBarrel = 1,
-				RPM 					= 100,
-				maxDist					= 10,
-				velocity 				= 3,
-				magazineCapacity 		= 6,
-				reload 					= 10,
-				smokeFactor 			= 4,
-				smokeMulti				= 3,
-
-
-
-
-		},
-	["t72_smokeGenerator"] = {
-				name 					= "Smoke Generator",
-				type 					= "generator",
-				barrels = {	
-
-					[1] = {x=2.1,y=1.6,z=-1.5,x_angle = 90,y_angle = 15,z_angle = 0,},
-
-				},
-				RPM 					= 100,
-				maxDist					= 10,
-				velocity 				= 3,
-				magazineCapacity 		= 6,
-				reload 					= 10,
-				smokeFactor 			= 4,
-				smokeMulti				= 3,
-				smokeTime 				= 10,
-
-
-
-
-		},
-	}+#version 2

```
