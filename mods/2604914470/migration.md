# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,377 +1,379 @@
-function init()
-    tool_name = "explosivepackgs"
-    RegisterTool(tool_name, "Explosive Pack", "MOD/vox/C4.vox", 4)
-	SetBool("game.tool." .. tool_name ..".enabled", true)
-	SetFloat("game.tool." .. tool_name .. ".ammo", 101)
-	safe = GetInt("savegame.mod.safe")
-	no_limit = GetBool("savegame.mod.no_limit")
-	claymore_mode = GetBool("savegame.mod.claymore_mode")
-	input_ex = GetString("savegame.mod.input_ex")
-	if input_ex == "" then input_ex = "K" end
-	input_change = GetString("savegame.mod.input_change")
-	if input_change == "" then input_change = "C" end
-	old_system = GetBool("savegame.mod.oldsystem")
-	
-	triger = 0
-	C4s = {{}, {}, {}, {}, {}, {}}
-	safety_n = 0
-	safety_timer = 0
-	explosive_type = 0
-	exploding = 0
-	has_pressed = false
-	safety_t = 0
-	
-	C4sp = LoadSprite("MOD/img/C4.png")
-	EMPsp = LoadSprite("MOD/img/EMP.png")
-	CMFsp = LoadSprite("MOD/img/ClayMoreF.png")
-	CMBsp = LoadSprite("MOD/img/ClayMoreB.png")
-	LMsp = LoadSprite("MOD/img/LandMine.png")
-	INsp = LoadSprite("MOD/img/Incendary.png")
-	DBsp = LoadSprite("MOD/img/DoorBreaching.png")
+#version 2
+function server.init()
+       tool_name = "explosivepackgs"
+       RegisterTool(tool_name, "Explosive Pack", "MOD/vox/C4.vox", 4)
+    SetBool("game.tool." .. tool_name ..".enabled", true, true)
+    SetFloat("game.tool." .. tool_name .. ".ammo", 101, true)
+    safe = GetInt("savegame.mod.safe")
+    no_limit = GetBool("savegame.mod.no_limit")
+    claymore_mode = GetBool("savegame.mod.claymore_mode")
+    input_ex = GetString("savegame.mod.input_ex")
+    if input_ex == "" then input_ex = "K" end
+    input_change = GetString("savegame.mod.input_change")
+    if input_change == "" then input_change = "C" end
+    old_system = GetBool("savegame.mod.oldsystem")
+
+    triger = 0
+    C4s = {{}, {}, {}, {}, {}, {}}
+    safety_n = 0
+    safety_timer = 0
+    explosive_type = 0
+    exploding = 0
+    has_pressed = false
+    safety_t = 0
+
+    C4sp = LoadSprite("MOD/img/C4.png")
+    EMPsp = LoadSprite("MOD/img/EMP.png")
+    CMFsp = LoadSprite("MOD/img/ClayMoreF.png")
+    CMBsp = LoadSprite("MOD/img/ClayMoreB.png")
+    LMsp = LoadSprite("MOD/img/LandMine.png")
+    INsp = LoadSprite("MOD/img/Incendary.png")
+    DBsp = LoadSprite("MOD/img/DoorBreaching.png")
 end
 
-
-function tick(dt)
-    if GetString("game.player.tool") == tool_name and GetPlayerVehicle() == 0 then
-	    for i = 1, 60 do
-	        SetShapeLocalTransform(GetBodyShapes(GetToolBody())[2+i], Transform(Vec(0, 0, 999999)))
-	    end
-	    if InputDown("rmb") and grabing then
-		    grabing = 1
-		else
-		    grabing = GetPlayerGrabShape()
-		end
-		if grabing > 0 then grabing = true else grabing = false end
-	    local Detonator_Shapes = GetBodyShapes(GetToolBody())
-		local Triger_Shape = Detonator_Shapes[2]
-		SetShapeLocalTransform(Triger_Shape, Transform(Vec(0.55, -0.65+triger*0.09, -0.9+triger*0.22), QuatEuler(-90+triger*-30, 0, 0)))
-		if InputDown("rmb") and not grabing then
-			triger = math.max(triger - dt * 10, 0)
-        else
-		    triger = math.min(triger + dt * 5, 1)
+function client.tick(dt)
+    local playerId = GetLocalPlayer()
+       if GetString("game.player.tool") == tool_name and GetPlayerVehicle(playerId) == 0 then
+        for i = 1, 60 do
+            SetShapeLocalTransform(GetBodyShapes(GetToolBody())[2+i], Transform(Vec(0, 0, 999999)))
         end
-		if triger == 0 and safe == 2 then
-		    safety_t = math.min(safety_t+dt/0.6, 1.5)
-		else
-		    safety_t = math.max(safety_t-dt*3.5, 0)
-		end
-		if triger == 1 then
-		    has_exploded = false
-		end
-		if InputPressed(input_change) then
-		    explosive_type = explosive_type + 1
-			if explosive_type == 6 then explosive_type = 0 end
-		end
-		if InputPressed("R") then
-		    for u = 1, 6 do
-		        for i = 1, #C4s[u] do
-					if C4s[u][i][5] ~= nil then if not old_system then Delete(C4s[u][i][5]) end end
-			    end
-			end
-		    C4s = {{}, {}, {}, {}, {}, {}}
-		end
-		if InputPressed("lmb") and not grabing and triger == 1 and GetBool("game.player.canusetool") then
-		    QueryRejectBody(GetToolBody())
-			if not(old_system) then
-			    for u = 1, 6 do
-		            for i = 1, #C4s[u] do
-					    if C4s[u][i][5] ~= nil then QueryRejectBody(C4s[u][i][5]) end
-					end
-				end
-			end
-		    local hit, dis, normal, shape = QueryRaycast(GetPlayerCameraTransform().pos, TransformToParentVec(GetPlayerCameraTransform(), Vec(0, 0, -1)), 4)
-			if hit and (#C4s[explosive_type+1] < 10 or (no_limit or not old_system)) then
-			    local hitpos = VecAdd(GetPlayerCameraTransform().pos, VecScale(TransformToParentVec(GetPlayerCameraTransform(), Vec(0, 0, -1)), dis))
-			    local tr = TransformToLocalPoint(GetShapeWorldTransform(shape), hitpos)
-                local qu 
-				--normal = Vec(normal[3], normal[2], normal[1])
-				if explosive_type == 2 then
-				    local x, y, z = GetQuatEuler(GetPlayerTransform().rot)
-					rot = Transform(Vec(0, 0, 0), QuatEuler(0, y, 0))
-					qu = TransformToLocalTransform(GetShapeWorldTransform(shape), rot).rot
-				else
-				    local x, y , z = GetQuatEuler(GetShapeWorldTransform(shape).rot)
-				    qu = QuatRotateQuat(QuatLookAt(VecAdd(hitpos, TransformToLocalVec(GetShapeWorldTransform(shape), normal)), hitpos), QuatEuler(0, 0, 90))
-				end
-				local tra = Transform(tr, qu)
-				--tra.pos = VecAdd(tra.pos, TransformToLocalVec(Transform(Vec(0, 0, 0), QuatRotateQuat(GetShapeWorldTransform(shape).rot, tra.rot)), Vec(-0.175, -0.3, 0)))
-				if explosive_type == 3 then table.insert(C4s[explosive_type+1], {tra, shape, 1, 2}) else table.insert(C4s[explosive_type+1], {tra, shape, 0, 0}) end
-			end
-		end
-		if triger == 0 and exploding == 0 and ((safe == 1 and safety_n == 4) or (safe == 2 and safety_t == 1.5) or safe == 0) then
-		    exploding = 2
-		end
-		if safety_timer > 0 then
-		    safety_timer = safety_timer - dt
-			if safety_timer <= 0 then
-			    safety_n = 0
-			end
-		end
-		if triger == 0 and exploding == 0 and safe == 1 and not has_pressed then
-		    safety_n = safety_n + 1
-			if safety_n == 1 then
-			    safety_timer = 2
-			end
-			has_pressed = true
-	    end
-		if triger >= 0.1 and has_pressed then
-		    has_pressed = false
-		end
-		if #C4s[1] ~= 0 or #C4s[2] ~= 0 or #C4s[3] ~= 0 then
-		    SetToolTransform(Transform(Vec(), QuatEuler()), 0)
-		end
-		if old_system then
-		for u = 1, 6 do
-		    local ve 
-			if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
-		    for i = 1, #C4s[u] do
-			    if i <= 10 then
-	                local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(ve[1], ve[2], ve[3]), QuatEuler(0, 0, 0)))
-				    tr.pos = VecSub(tr.pos, VecScale(GetPlayerVelocity(), dt))
-			        --if grabing then tr = TransformToParentTransform(tr, Transform(TransformToLocalVec(tr, Vec(0, 1, 0)), QuatEuler(0, 0, 0))) end
-		            SetShapeLocalTransform(GetBodyShapes(GetToolBody())[2+i+(u-1)*10], TransformToLocalTransform(GetBodyTransform(GetToolBody()), tr))
-				else
-				    local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(0, 0, 0.01), QuatEuler(0, 0, 0)))
-				    if u == 1 then
-				        DrawSprite(C4sp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				    end
-				    if u == 2 then
-				        DrawSprite(EMPsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				    end
-				    if u == 3 then
-				        DrawSprite(CMFsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0), QuatEuler(0, 180, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-					    DrawSprite(CMBsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0.001), QuatEuler(0, 0, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				    end
-				    if u == 4 then
-				        DrawSprite(LMsp, tr, 15*0.05, 15*0.05, 0.3, 0.3, 0.3, 1, true)
-				    end
-				    if u == 5 then
-				        DrawSprite(INsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				    end
-					if u == 6 then
-				        DrawSprite(DBsp, tr, 3*0.05, 4*0.05, 0.3, 0.3, 0.3, 1, true)
-				    end
-				end
-	        end
-		end
-		end
-	elseif old_system then
-	    for u = 1, 6 do
-		    for i = 1, #C4s[u] do
-	            local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(0, 0, 0.01), QuatEuler(0, 0, 0)))
-				if u == 1 then
-				    DrawSprite(C4sp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				end
-				if u == 2 then
-				    DrawSprite(EMPsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				end
-				if u == 3 then
-				    DrawSprite(CMFsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0), QuatEuler(0, 180, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-					DrawSprite(CMBsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0.001), QuatEuler(0, 0, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				end
-				if u == 4 then
-				    DrawSprite(LMsp, tr, 15*0.05, 15*0.05, 0.3, 0.3, 0.3, 1, true)
-				end
-				if u == 5 then
-				    DrawSprite(INsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
-				end
-				if u == 6 then
-				    DrawSprite(DBsp, tr, 3*0.05, 4*0.05, 0.3, 0.3, 0.3, 1, true)
-				end
-	        end
-		end
-	end
-	if not old_system then
-	    for u = 1, 6 do
-		    local ve 
-			if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
-		    for i = 1, #C4s[u] do
-				    if C4s[u][i][5] == nil then
-					    if u == 1 then obj = Spawn("MOD/spn/C4.xml") elseif u == 2 then obj = Spawn("MOD/spn/EMP.xml") elseif u == 3 then obj = Spawn("MOD/spn/Claymore.xml") 
-						elseif u == 4 then obj = Spawn("MOD/spn/ATMine.xml") elseif u == 5 then obj = Spawn("MOD/spn/Incendiary.xml") elseif u == 6 then obj = Spawn("MOD/spn/DoorBreach.xml") end
-						
-						if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
-						local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(ve[1], ve[2], ve[3]), QuatEuler(0, 0, 0)))
-						SetBodyDynamic(obj[1], false)
-						SetTag(obj[1], "unbreakable")
-						SetBodyTransform(obj[1], tr)
-						C4s[u][i][5] = obj[1]
-						SetBodyActive(C4s[u][i][5], false)
-					else
-					    if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
-						local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(ve[1], ve[2], ve[3]), QuatEuler(0, 0, 0)))
-						SetBodyTransform(C4s[u][i][5], TransformToParentTransform(tr, Transform(Vec(0.3, 0, 0), QuatEuler(90, 0, 0))))
-						SetBodyActive(C4s[u][i][5], false)
-					end
-	        end
-	end
-	end
-	if InputPressed(input_ex) and exploding == 0 then
-		exploding = 2
-	end
-	local mine_number = #C4s[4]
-	for i = 1, #C4s[4] do
-	    local tr = TransformToParentTransform(GetShapeWorldTransform(C4s[4][mine_number+1-i][2]), C4s[4][mine_number+1-i][1])
-		QueryRejectShape(C4s[4][mine_number+1-i][2])
-		if not(old_system) then
-			for o = 1, 6 do
-		        for l = 1, #C4s[o] do
-					if C4s[o][l][5] ~= nil then QueryRejectBody(C4s[o][l][5]) end
-				end
-			end
-		end
-	    if C4s[4][mine_number+1-i][3] > 0 then 
-		    C4s[4][mine_number+1-i][3] = math.max(C4s[4][mine_number+1-i][3] - dt/2, 0) 
-			if C4s[4][mine_number+1-i][3] == 0 then
-			    if not old_system then QueryRejectBody(C4s[4][mine_number+1-i][5]) end
-			    local hit, dis = QueryRaycast(tr.pos, TransformToParentVec(tr, Vec(0, 0, 1)), 2)
-				if hit then 
-				    C4s[4][mine_number+1-i][4] = dis
-				end
-			end
-		else
-		    PointLight(tr.pos, 0.5, 0, 0)
-			if not old_system then QueryRejectBody(C4s[4][mine_number+1-i][5]) end
-		    local hit, dis = QueryRaycast(tr.pos, TransformToParentVec(tr, Vec(0, 0, 1)), 2)
-		    if hit or (math.abs(C4s[4][mine_number+1-i][4]) ~= 2 and not hit) then 
-				if C4s[4][mine_number+1-i][4] == 2 or math.abs(C4s[4][mine_number+1-i][4]-dis) > 0.1 then
-				    Explosion(tr.pos, 4)
-					if not old_system then Delete(C4s[4][mine_number+1-i][5]) end
-					table.remove(C4s[4], mine_number+1-i)
-				end
-		    end
-		end
-	end
-	if exploding ~= 0 then
-		    if  #C4s[exploding] == 0 then
-			    if exploding == 2 then
-				    exploding = 1 
-				elseif exploding == 1 then
-				    exploding = 3
-				elseif exploding == 3 then
-				    exploding = 4
-				elseif exploding == 4 then
-				    exploding = 5
-				elseif exploding == 5 then
-				    exploding = 6
-				else
-				    exploding = 0
-				end
-			else
-			    local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[exploding][1][2]), C4s[exploding][1][1]), Transform(Vec(-0.3, -0.175, 0), QuatEuler(0, 0, 0)))
-				if exploding == 6 then
-				    ApplyBodyImpulse(GetShapeBody(C4s[exploding][1][2]), tr.pos, TransformToParentVec(tr, Vec(0, 0, -800)))
-				    local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[exploding][1][2]), C4s[exploding][1][1]), Transform(Vec(-0.075, -0.1, 0.55), QuatEuler(0, 0, 0)))
-		            Explosion(tr.pos, 0.5)
-		        end
-				if not old_system then Delete(C4s[exploding][1][5]) end
-			    table.remove(C4s[exploding], 1) 
-				if exploding == 1 then
-		            Explosion(tr.pos,2)
-		        end
-			    if exploding == 2 then
-			        local pos = tr.pos
-				    local lights = FindLights("", true)
-				    for i = 1, #lights do
-				        if VecLength(VecSub(GetLightTransform(lights[i]).pos, pos)) < 50 then
-					        MakeHole(GetLightTransform(lights[i]).pos, 0.1)
-					    end
-				    end
-		            MakeHole(tr.pos, 1, 1, 1)
-					local bots = FindShapes("", true)
-					for i = 1, #bots do
-					    if VecLength(VecSub(GetShapeWorldTransform(bots[i]).pos, pos)) < 50 then
-						    --bot damage system
-			                if HasTag(bots[i], "gsgunsystemhitcount") then
-			                    local damage = tonumber(GetTagValue(bots[i], "gsgunsystemhitcount"))+50
-				                SetTag(bots[i], "gsgunsystemhitcount", tostring(damage))
-			                else
-			                    SetTag(bots[i], "gsgunsystemhitcount", "50")
-			                end
-						end
-					end
-		        end
-				if exploding == 4 then
-				    Explosion(tr.pos,2)
-				end
-				if exploding == 5 then
-				    SpawnFire(tr.pos)
-					MakeHole(tr.pos, 0.2, 0.1, 0)
-				    for i = 1, 200 do SpawnFire(VecAdd(tr.pos, Vec((math.random()-0.5)*4, (math.random()-0.5)*4, (math.random()-0.5)*4))) end
-				end
-				if exploding == 3 and claymore_mode then
-				    local laser_tr = TransformToParentTransform(tr, Transform(Vec(0.275, 0.25, 0) , QuatEuler(0, 0, 0)))
-					laser_tr.pos = VecAdd(TransformToParentVec(laser_tr, Vec(0, 0, -0.25)), laser_tr.pos)
-				    for i = 1, 500 do
-						local dir = VecNormalize(TransformToParentVec(laser_tr, Vec((math.random()-0.5), math.random()*0.3, -1)))
-						local hit, dis, normal, shape = QueryRaycast(laser_tr.pos, dir, 40)
-						if hit then 
-						    local hitpos = VecAdd(laser_tr.pos, VecScale(dir, dis))
-						    MakeHole(hitpos, 0.2, 0.15, 0.1) 
-							--Explosion(hitpos, 0.01)
-							ParticleRadius(0.5)
-							SpawnParticle(hitpos, VecSub(Vec(0, 0, 0), VecScale(hitpos, 0.2)), 0.5)
-							
-							--bot damage system
-			                if HasTag(shape, "gsgunsystemhitcount") then
-			                    local damage = tonumber(GetTagValue(shape, "gsgunsystemhitcount"))+0.3
-				                SetTag(shape, "gsgunsystemhitcount", tostring(damage))
-			                else
-			                    SetTag(shape, "gsgunsystemhitcount", "0.3")
-			                end
-						end
-				    end
-		            Explosion(tr.pos, 1)
-					local vec = VecNormalize(TransformToLocalPoint(tr, GetPlayerCameraTransform().pos))
-					QueryRejectBody(GetToolBody())
-					tr = TransformToParentTransform(tr, Transform(Vec(0, 0.2, 0), QuatEuler(0, 0, 0)))
-					local hit = QueryRaycast(tr.pos, VecNormalize(VecSub(GetPlayerCameraTransform().pos, tr.pos)), VecLength(VecSub(tr.pos,  GetPlayerCameraTransform().pos)))
-					if vec[3] < 0 and math.abs(vec[1]) < 0.35 and vec[2] < 0.5 and vec[2] > 0 and VecLength(VecSub(tr.pos,  GetPlayerCameraTransform().pos)) < 40 and not hit then
-					    SetPlayerHealth(GetPlayerHealth()-0.8)
-					end
-		        end
-				if exploding == 3 and not claymore_mode then
-				    local laser_tr = TransformToParentTransform(tr, Transform(Vec(0.275, 0.25, 0) , QuatEuler(0, 0, 0)))
-					laser_tr.pos = VecAdd(TransformToParentVec(laser_tr, Vec(0, 0, -0.25)), laser_tr.pos)
-				    for i = 1, 50 do
-						local dir = VecNormalize(TransformToParentVec(laser_tr, Vec((math.random()-0.5), math.random()*0.3, -1)))
-						local hit, dis, normal, shape = QueryRaycast(laser_tr.pos, dir, 50)
-						if hit then 
-						    local hitpos = VecAdd(laser_tr.pos, VecScale(dir, dis))
-						    MakeHole(hitpos, 1, 0.8, 0.7) 
-							--Explosion(hitpos, 0.01)
-							ParticleRadius(0.5)
-							SpawnParticle(hitpos, VecSub(Vec(0, 0, 0), VecScale(hitpos, 0.2)), 0.5)
-							
-							--bot damage system
-			                if HasTag(shape, "gsgunsystemhitcount") then
-			                    local damage = tonumber(GetTagValue(shape, "gsgunsystemhitcount"))+6
-				                SetTag(shape, "gsgunsystemhitcount", tostring(damage))
-			                else
-			                    SetTag(shape, "gsgunsystemhitcount", "6")
-			                end
-						end
-				    end
-		            Explosion(tr.pos, 1)
-		        end
-			end
-		end
+        if InputDown("rmb") and grabing then
+    	    grabing = 1
+    	else
+    	    grabing = GetPlayerGrabShape(playerId)
+    	end
+    	if grabing ~= 0 then grabing = true else grabing = false end
+        local Detonator_Shapes = GetBodyShapes(GetToolBody())
+    	local Triger_Shape = Detonator_Shapes[2]
+    	SetShapeLocalTransform(Triger_Shape, Transform(Vec(0.55, -0.65+triger*0.09, -0.9+triger*0.22), QuatEuler(-90+triger*-30, 0, 0)))
+    	if InputDown("rmb") and not grabing then
+    		triger = math.max(triger - dt * 10, 0)
+           else
+    	    triger = math.min(triger + dt * 5, 1)
+           end
+    	if triger == 0 and safe == 2 then
+    	    safety_t = math.min(safety_t+dt/0.6, 1.5)
+    	else
+    	    safety_t = math.max(safety_t-dt*3.5, 0)
+    	end
+    	if triger == 1 then
+    	    has_exploded = false
+    	end
+    	if InputPressed(input_change) then
+    	    explosive_type = explosive_type + 1
+    		if explosive_type == 6 then explosive_type = 0 end
+    	end
+    	if InputPressed("R") then
+    	    for u = 1, 6 do
+    	        for i = 1, #C4s[u] do
+    				if C4s[u][i][5] ~= nil then if not old_system then Delete(C4s[u][i][5]) end end
+    		    end
+    		end
+    	    C4s = {{}, {}, {}, {}, {}, {}}
+    	end
+    	if InputPressed("lmb") and not grabing and triger == 1 and GetBool("game.player.canusetool") then
+    	    QueryRejectBody(GetToolBody())
+    		if not(old_system) then
+    		    for u = 1, 6 do
+    	            for i = 1, #C4s[u] do
+    				    if C4s[u][i][5] ~= nil then QueryRejectBody(C4s[u][i][5]) end
+    				end
+    			end
+    		end
+    	    local hit, dis, normal, shape = QueryRaycast(GetPlayerCameraTransform(playerId).pos, TransformToParentVec(GetPlayerCameraTransform(playerId), Vec(0, 0, -1)), 4)
+    		if hit and (#C4s[explosive_type+1] < 10 or (no_limit or not old_system)) then
+    		    local hitpos = VecAdd(GetPlayerCameraTransform(playerId).pos, VecScale(TransformToParentVec(GetPlayerCameraTransform(playerId), Vec(0, 0, -1)), dis))
+    		    local tr = TransformToLocalPoint(GetShapeWorldTransform(shape), hitpos)
+                   local qu 
+    			--normal = Vec(normal[3], normal[2], normal[1])
+    			if explosive_type == 2 then
+    			    local x, y, z = GetQuatEuler(GetPlayerTransform(playerId).rot)
+    				rot = Transform(Vec(0, 0, 0), QuatEuler(0, y, 0))
+    				qu = TransformToLocalTransform(GetShapeWorldTransform(shape), rot).rot
+    			else
+    			    local x, y , z = GetQuatEuler(GetShapeWorldTransform(shape).rot)
+    			    qu = QuatRotateQuat(QuatLookAt(VecAdd(hitpos, TransformToLocalVec(GetShapeWorldTransform(shape), normal)), hitpos), QuatEuler(0, 0, 90))
+    			end
+    			local tra = Transform(tr, qu)
+    			--tra.pos = VecAdd(tra.pos, TransformToLocalVec(Transform(Vec(0, 0, 0), QuatRotateQuat(GetShapeWorldTransform(shape).rot, tra.rot)), Vec(-0.175, -0.3, 0)))
+    			if explosive_type == 3 then table.insert(C4s[explosive_type+1], {tra, shape, 1, 2}) else table.insert(C4s[explosive_type+1], {tra, shape, 0, 0}) end
+    		end
+    	end
+    	if triger == 0 and exploding == 0 and ((safe == 1 and safety_n == 4) or (safe == 2 and safety_t == 1.5) or safe == 0) then
+    	    exploding = 2
+    	end
+    	if safety_timer ~= 0 then
+    	    safety_timer = safety_timer - dt
+    		if safety_timer <= 0 then
+    		    safety_n = 0
+    		end
+    	end
+    	if triger == 0 and exploding == 0 and safe == 1 and not has_pressed then
+    	    safety_n = safety_n + 1
+    		if safety_n == 1 then
+    		    safety_timer = 2
+    		end
+    		has_pressed = true
+        end
+    	if triger >= 0.1 and has_pressed then
+    	    has_pressed = false
+    	end
+    	if #C4s[1] ~= 0 or #C4s[2] ~= 0 or #C4s[3] ~= 0 then
+    	    SetToolTransform(Transform(Vec(), QuatEuler()), 0)
+    	end
+    	if old_system then
+    	for u = 1, 6 do
+    	    local ve 
+    		if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
+    	    for i = 1, #C4s[u] do
+    		    if i <= 10 then
+                    local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(ve[1], ve[2], ve[3]), QuatEuler(0, 0, 0)))
+    			    tr.pos = VecSub(tr.pos, VecScale(GetPlayerVelocity(playerId), dt))
+    		        --if grabing then tr = TransformToParentTransform(tr, Transform(TransformToLocalVec(tr, Vec(0, 1, 0)), QuatEuler(0, 0, 0))) end
+    	            SetShapeLocalTransform(GetBodyShapes(GetToolBody())[2+i+(u-1)*10], TransformToLocalTransform(GetBodyTransform(GetToolBody()), tr))
+    			else
+    			    local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(0, 0, 0.01), QuatEuler(0, 0, 0)))
+    			    if u == 1 then
+    			        DrawSprite(C4sp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			    end
+    			    if u == 2 then
+    			        DrawSprite(EMPsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			    end
+    			    if u == 3 then
+    			        DrawSprite(CMFsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0), QuatEuler(0, 180, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    				    DrawSprite(CMBsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0.001), QuatEuler(0, 0, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			    end
+    			    if u == 4 then
+    			        DrawSprite(LMsp, tr, 15*0.05, 15*0.05, 0.3, 0.3, 0.3, 1, true)
+    			    end
+    			    if u == 5 then
+    			        DrawSprite(INsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			    end
+    				if u == 6 then
+    			        DrawSprite(DBsp, tr, 3*0.05, 4*0.05, 0.3, 0.3, 0.3, 1, true)
+    			    end
+    			end
+            end
+    	end
+    	end
+    elseif old_system then
+        for u = 1, 6 do
+    	    for i = 1, #C4s[u] do
+                local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(0, 0, 0.01), QuatEuler(0, 0, 0)))
+    			if u == 1 then
+    			    DrawSprite(C4sp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			end
+    			if u == 2 then
+    			    DrawSprite(EMPsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			end
+    			if u == 3 then
+    			    DrawSprite(CMFsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0), QuatEuler(0, 180, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    				DrawSprite(CMBsp, TransformToParentTransform(tr, Transform(Vec(0, 0.175, 0.001), QuatEuler(0, 0, 0))), 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			end
+    			if u == 4 then
+    			    DrawSprite(LMsp, tr, 15*0.05, 15*0.05, 0.3, 0.3, 0.3, 1, true)
+    			end
+    			if u == 5 then
+    			    DrawSprite(INsp, tr, 13*0.05, 7*0.05, 0.3, 0.3, 0.3, 1, true)
+    			end
+    			if u == 6 then
+    			    DrawSprite(DBsp, tr, 3*0.05, 4*0.05, 0.3, 0.3, 0.3, 1, true)
+    			end
+            end
+    	end
+    end
+    if not old_system then
+        for u = 1, 6 do
+    	    local ve 
+    		if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
+    	    for i = 1, #C4s[u] do
+    			    if C4s[u][i][5] == nil then
+    				    if u == 1 then obj = Spawn("MOD/spn/C4.xml") elseif u == 2 then obj = Spawn("MOD/spn/EMP.xml") elseif u == 3 then obj = Spawn("MOD/spn/Claymore.xml") 
+    					elseif u == 4 then obj = Spawn("MOD/spn/ATMine.xml") elseif u == 5 then obj = Spawn("MOD/spn/Incendiary.xml") elseif u == 6 then obj = Spawn("MOD/spn/DoorBreach.xml") end
+
+    					if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
+    					local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(ve[1], ve[2], ve[3]), QuatEuler(0, 0, 0)))
+    					SetBodyDynamic(obj[1], false)
+    					SetTag(obj[1], "unbreakable")
+    					SetBodyTransform(obj[1], tr)
+    					C4s[u][i][5] = obj[1]
+    					SetBodyActive(C4s[u][i][5], false)
+    				else
+    				    if u == 3 then ve = {-0.3, 0, 0} elseif u == 4 then ve = {-0.375, -0.375, 0} elseif u == 6 then ve = {-0.075, -0.1, 0} else ve = {-0.3, -0.175, 0} end
+    					local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[u][i][2]), C4s[u][i][1]), Transform(Vec(ve[1], ve[2], ve[3]), QuatEuler(0, 0, 0)))
+    					SetBodyTransform(C4s[u][i][5], TransformToParentTransform(tr, Transform(Vec(0.3, 0, 0), QuatEuler(90, 0, 0))))
+    					SetBodyActive(C4s[u][i][5], false)
+    				end
+            end
+    end
+    end
+    if InputPressed(input_ex) and exploding == 0 then
+    	exploding = 2
+    end
+    local mine_number = #C4s[4]
+    for i = 1, #C4s[4] do
+        local tr = TransformToParentTransform(GetShapeWorldTransform(C4s[4][mine_number+1-i][2]), C4s[4][mine_number+1-i][1])
+    	QueryRejectShape(C4s[4][mine_number+1-i][2])
+    	if not(old_system) then
+    		for o = 1, 6 do
+    	        for l = 1, #C4s[o] do
+    				if C4s[o][l][5] ~= nil then QueryRejectBody(C4s[o][l][5]) end
+    			end
+    		end
+    	end
+        if C4s[4][mine_number+1-i][3] > 0 then 
+    	    C4s[4][mine_number+1-i][3] = math.max(C4s[4][mine_number+1-i][3] - dt/2, 0) 
+    		if C4s[4][mine_number+1-i][3] == 0 then
+    		    if not old_system then QueryRejectBody(C4s[4][mine_number+1-i][5]) end
+    		    local hit, dis = QueryRaycast(tr.pos, TransformToParentVec(tr, Vec(0, 0, 1)), 2)
+    			if hit then 
+    			    C4s[4][mine_number+1-i][4] = dis
+    			end
+    		end
+    	else
+    	    PointLight(tr.pos, 0.5, 0, 0)
+    		if not old_system then QueryRejectBody(C4s[4][mine_number+1-i][5]) end
+    	    local hit, dis = QueryRaycast(tr.pos, TransformToParentVec(tr, Vec(0, 0, 1)), 2)
+    	    if hit or (math.abs(C4s[4][mine_number+1-i][4]) ~= 2 and not hit) then 
+    			if C4s[4][mine_number+1-i][4] == 2 or math.abs(C4s[4][mine_number+1-i][4]-dis) > 0.1 then
+    			    Explosion(tr.pos, 4)
+    				if not old_system then Delete(C4s[4][mine_number+1-i][5]) end
+    				table.remove(C4s[4], mine_number+1-i)
+    			end
+    	    end
+    	end
+    end
+    if exploding ~= 0 then
+    	    if  #C4s[exploding] == 0 then
+    		    if exploding == 2 then
+    			    exploding = 1 
+    			elseif exploding == 1 then
+    			    exploding = 3
+    			elseif exploding == 3 then
+    			    exploding = 4
+    			elseif exploding == 4 then
+    			    exploding = 5
+    			elseif exploding == 5 then
+    			    exploding = 6
+    			else
+    			    exploding = 0
+    			end
+    		else
+    		    local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[exploding][1][2]), C4s[exploding][1][1]), Transform(Vec(-0.3, -0.175, 0), QuatEuler(0, 0, 0)))
+    			if exploding == 6 then
+    			    ApplyBodyImpulse(GetShapeBody(C4s[exploding][1][2]), tr.pos, TransformToParentVec(tr, Vec(0, 0, -800)))
+    			    local tr = TransformToParentTransform(TransformToParentTransform(GetShapeWorldTransform(C4s[exploding][1][2]), C4s[exploding][1][1]), Transform(Vec(-0.075, -0.1, 0.55), QuatEuler(0, 0, 0)))
+    	            Explosion(tr.pos, 0.5)
+    	        end
+    			if not old_system then Delete(C4s[exploding][1][5]) end
+    		    table.remove(C4s[exploding], 1) 
+    			if exploding == 1 then
+    	            Explosion(tr.pos,2)
+    	        end
+    		    if exploding == 2 then
+    		        local pos = tr.pos
+    			    local lights = FindLights("", true)
+    			    for i = 1, #lights do
+    			        if VecLength(VecSub(GetLightTransform(lights[i]).pos, pos)) < 50 then
+    				        MakeHole(GetLightTransform(lights[i]).pos, 0.1)
+    				    end
+    			    end
+    	            MakeHole(tr.pos, 1, 1, 1)
+    				local bots = FindShapes("", true)
+    				for i = 1, #bots do
+    				    if VecLength(VecSub(GetShapeWorldTransform(bots[i]).pos, pos)) < 50 then
+    					    --bot damage system
+    		                if HasTag(bots[i], "gsgunsystemhitcount") then
+    		                    local damage = tonumber(GetTagValue(bots[i], "gsgunsystemhitcount"))+50
+    			                SetTag(bots[i], "gsgunsystemhitcount", tostring(damage))
+    		                else
+    		                    SetTag(bots[i], "gsgunsystemhitcount", "50")
+    		                end
+    					end
+    				end
+    	        end
+    			if exploding == 4 then
+    			    Explosion(tr.pos,2)
+    			end
+    			if exploding == 5 then
+    			    SpawnFire(tr.pos)
+    				MakeHole(tr.pos, 0.2, 0.1, 0)
+    			    for i = 1, 200 do SpawnFire(VecAdd(tr.pos, Vec((math.random()-0.5)*4, (math.random()-0.5)*4, (math.random()-0.5)*4))) end
+    			end
+    			if exploding == 3 and claymore_mode then
+    			    local laser_tr = TransformToParentTransform(tr, Transform(Vec(0.275, 0.25, 0) , QuatEuler(0, 0, 0)))
+    				laser_tr.pos = VecAdd(TransformToParentVec(laser_tr, Vec(0, 0, -0.25)), laser_tr.pos)
+    			    for i = 1, 500 do
+    					local dir = VecNormalize(TransformToParentVec(laser_tr, Vec((math.random()-0.5), math.random()*0.3, -1)))
+    					local hit, dis, normal, shape = QueryRaycast(laser_tr.pos, dir, 40)
+    					if hit then 
+    					    local hitpos = VecAdd(laser_tr.pos, VecScale(dir, dis))
+    					    MakeHole(hitpos, 0.2, 0.15, 0.1) 
+    						--Explosion(hitpos, 0.01)
+    						ParticleRadius(0.5)
+    						SpawnParticle(hitpos, VecSub(Vec(0, 0, 0), VecScale(hitpos, 0.2)), 0.5)
+
+    						--bot damage system
+    		                if HasTag(shape, "gsgunsystemhitcount") then
+    		                    local damage = tonumber(GetTagValue(shape, "gsgunsystemhitcount"))+0.3
+    			                SetTag(shape, "gsgunsystemhitcount", tostring(damage))
+    		                else
+    		                    SetTag(shape, "gsgunsystemhitcount", "0.3")
+    		                end
+    					end
+    			    end
+    	            Explosion(tr.pos, 1)
+    				local vec = VecNormalize(TransformToLocalPoint(tr, GetPlayerCameraTransform(playerId).pos))
+    				QueryRejectBody(GetToolBody())
+    				tr = TransformToParentTransform(tr, Transform(Vec(0, 0.2, 0), QuatEuler(0, 0, 0)))
+    				local hit = QueryRaycast(tr.pos, VecNormalize(VecSub(GetPlayerCameraTransform(playerId).pos, tr.pos)), VecLength(VecSub(tr.pos,  GetPlayerCameraTransform(playerId).pos)))
+    				if vec[3] < 0 and math.abs(vec[1]) < 0.35 and vec[2] < 0.5 and vec[2] > 0 and VecLength(VecSub(tr.pos,  GetPlayerCameraTransform(playerId).pos)) < 40 and not hit then
+    				    SetPlayerHealth(playerId, GetPlayerHealth(playerId)-0.8)
+    				end
+    	        end
+    			if exploding == 3 and not claymore_mode then
+    			    local laser_tr = TransformToParentTransform(tr, Transform(Vec(0.275, 0.25, 0) , QuatEuler(0, 0, 0)))
+    				laser_tr.pos = VecAdd(TransformToParentVec(laser_tr, Vec(0, 0, -0.25)), laser_tr.pos)
+    			    for i = 1, 50 do
+    					local dir = VecNormalize(TransformToParentVec(laser_tr, Vec((math.random()-0.5), math.random()*0.3, -1)))
+    					local hit, dis, normal, shape = QueryRaycast(laser_tr.pos, dir, 50)
+    					if hit then 
+    					    local hitpos = VecAdd(laser_tr.pos, VecScale(dir, dis))
+    					    MakeHole(hitpos, 1, 0.8, 0.7) 
+    						--Explosion(hitpos, 0.01)
+    						ParticleRadius(0.5)
+    						SpawnParticle(hitpos, VecSub(Vec(0, 0, 0), VecScale(hitpos, 0.2)), 0.5)
+
+    						--bot damage system
+    		                if HasTag(shape, "gsgunsystemhitcount") then
+    		                    local damage = tonumber(GetTagValue(shape, "gsgunsystemhitcount"))+6
+    			                SetTag(shape, "gsgunsystemhitcount", tostring(damage))
+    		                else
+    		                    SetTag(shape, "gsgunsystemhitcount", "6")
+    		                end
+    					end
+    			    end
+    	            Explosion(tr.pos, 1)
+    	        end
+    		end
+    	end
 end
 
-function draw()
-    if GetString("game.player.tool") == tool_name and GetPlayerVehicle() == 0 then
-	    UiTranslate(UiCenter(), UiHeight()-80)
-        UiAlign("center middle")
-        UiColor(1, 1, 1)
-        UiFont("bold.ttf", 32)
-        UiTextOutline(0,0,0,1,0.1)
-		local bomb_type_text
-		local bomb_number = #C4s[explosive_type+1]
-		if explosive_type == 0 then bomb_type_text = "C4" elseif explosive_type == 1 then bomb_type_text = "EMP" elseif explosive_type == 2 then bomb_type_text = "Claymore" elseif explosive_type == 3 then bomb_type_text = "LandMine" elseif explosive_type == 4 then bomb_type_text = "Incendiary" elseif explosive_type == 5 then bomb_type_text = "Door Breaching" end
-		if no_limit or not old_system then UiText(bomb_type_text .. " - " .. bomb_number) else UiText(bomb_type_text .. " - " .. bomb_number .. "/10") end
-		UiTranslate(0, -80)
-		UiColor(1, 0.5, 0.5)
-		if safe == 1 then if safety_n == 0 then UiText("") elseif safety_n == 1 then UiText("[O - -]") elseif safety_n == 2 then UiText("[O O -]") elseif safety_n == 3 then UiText("[O O O]") else UiText("[DETONATION]") end end
-		if safe == 2 then if safety_t == 0 then UiText("") elseif safety_t == 1.5 then UiText("[DETONATION]") elseif safety_t > 1.2 then UiText("[ ||||| ]") elseif safety_t > 0.9 then UiText("[ ||||- ]") elseif safety_t > 0.6 then UiText("[ |||-- ]") elseif safety_t > 0.3 then UiText("[ ||--- ]") else UiText("[ |---- ]") end end
-	end
-end+function client.draw()
+       if GetString("game.player.tool") == tool_name and GetPlayerVehicle(playerId) == 0 then
+        UiTranslate(UiCenter(), UiHeight()-80)
+           UiAlign("center middle")
+           UiColor(1, 1, 1)
+           UiFont("bold.ttf", 32)
+           UiTextOutline(0,0,0,1,0.1)
+    	local bomb_type_text
+    	local bomb_number = #C4s[explosive_type+1]
+    	if explosive_type == 0 then bomb_type_text = "C4" elseif explosive_type == 1 then bomb_type_text = "EMP" elseif explosive_type == 2 then bomb_type_text = "Claymore" elseif explosive_type == 3 then bomb_type_text = "LandMine" elseif explosive_type == 4 then bomb_type_text = "Incendiary" elseif explosive_type == 5 then bomb_type_text = "Door Breaching" end
+    	if no_limit or not old_system then UiText(bomb_type_text .. " - " .. bomb_number) else UiText(bomb_type_text .. " - " .. bomb_number .. "/10") end
+    	UiTranslate(0, -80)
+    	UiColor(1, 0.5, 0.5)
+    	if safe == 1 then if safety_n == 0 then UiText("") elseif safety_n == 1 then UiText("[O - -]") elseif safety_n == 2 then UiText("[O O -]") elseif safety_n == 3 then UiText("[O O O]") else UiText("[DETONATION]") end end
+    	if safe == 2 then if safety_t == 0 then UiText("") elseif safety_t == 1.5 then UiText("[DETONATION]") elseif safety_t > 1.2 then UiText("[ ||||| ]") elseif safety_t > 0.9 then UiText("[ ||||- ]") elseif safety_t > 0.6 then UiText("[ |||-- ]") elseif safety_t > 0.3 then UiText("[ ||--- ]") else UiText("[ |---- ]") end end
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
@@ -1,148 +1,149 @@
-function init()
-	safe = GetInt("savegame.mod.safe")
-	no_limit = GetBool("savegame.mod.no_limit")
-	claymore_mode = GetBool("savegame.mod.claymore_mode")
-	input_ex = GetString("savegame.mod.input_ex")
-	if input_ex == "" then input_ex = "K" end
-	input_change = GetString("savegame.mod.input_change")
-	if input_change == "" then input_change = "C" end
-	oldsystem = GetBool("savegame.mod.oldsystem")
-	changing_mode = 0
+#version 2
+function server.init()
+    safe = GetInt("savegame.mod.safe")
+    no_limit = GetBool("savegame.mod.no_limit")
+    claymore_mode = GetBool("savegame.mod.claymore_mode")
+    input_ex = GetString("savegame.mod.input_ex")
+    if input_ex == "" then input_ex = "K" end
+    input_change = GetString("savegame.mod.input_change")
+    if input_change == "" then input_change = "C" end
+    oldsystem = GetBool("savegame.mod.oldsystem")
+    changing_mode = 0
 end
 
-function draw()
-	UiTranslate(UiCenter(), 350)
-	UiAlign("center middle")
+function client.draw()
+    UiTranslate(UiCenter(), 350)
+    UiAlign("center middle")
 
-	UiFont("bold.ttf", 48)
-	UiText("Explosive Pack by gs_115")
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-	    UiTranslate(75, 0)
-		last_input = InputLastPressedKey()
-		if last_input ~= "" then
-		    if changing_mode == 1 then input_ex = last_input end
-			if changing_mode == 2 then input_change = last_input end
-			SetString("savegame.mod.input_ex", input_ex)
-			SetString("savegame.mod.input_change", input_change)
-		    changing_mode = 0
-		end
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-	    if UiTextButton(input_ex, 50, 30) and changing_mode == 0 then --Explode Input
-		    input_ex = "..."
-			changing_mode = 1
-		end
-		UiTranslate(-90, 0)
-		UiText("Explode All:", 150, 30)
-		
-		UiTranslate(110, 10)
-		UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-	    if UiTextButton(input_change, 50, 30) and changing_mode == 0 then --Explode Input
-		    input_change = "..."
-			changing_mode = 2
-		end
-		UiTranslate(-110, 0)
-		UiText("Change Explosif:", 150, 30)
-	UiPop()
-	UiTranslate(0, 90)
-	UiPush()
-		UiText("Claymore Mode")
-		UiTranslate(90, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if claymore_mode then
-		    UiTranslate(-35, 0)
-			if UiTextButton("\"Realistic\"", 20, 20) then
-				claymore_mode = false
-				SetBool("savegame.mod.claymore_mode", claymore_mode)
-			end
-		else
-			if UiTextButton("High Performance", 20, 20) then
-				claymore_mode = true
-				SetBool("savegame.mod.claymore_mode", claymore_mode)
-			end
-		end
-	UiPop()
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Safety")
-		UiTranslate(15, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if safe == 0 then
-		    UiTranslate(12, 0)
-			if UiTextButton("None", 20, 20) then
-				safe = 1
-				SetInt("savegame.mod.safe", safe)
-			end
-		elseif safe == 1 then
-		    UiTranslate(42, 0)
-			if UiTextButton("Triple Press", 20, 20) then
-				safe = 2
-				SetInt("savegame.mod.safe", safe)
-			end
-		else
-		    UiTranslate(38, 0)
-			if UiTextButton("Long Press", 20, 20) then
-				safe = 0
-				SetInt("savegame.mod.safe", safe)
-			end
-		end
-	UiPop()
-	UiTranslate(0, 70)
-	UiPush()
-	    UiTranslate(2, 0)
-		UiText("Use old display system")
-		UiTranslate(13, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if oldsystem then
-			if UiTextButton("Yes", 20, 20) then
-				oldsystem = false
-				no_limit = true
-				SetBool("savegame.mod.oldsystem", oldsystem)
-				SetBool("savegame.mod.no_limit", no_limit)
-			end
-		else
-			if UiTextButton("No", 20, 20) then
-				oldsystem = true
-				no_limit = true
-				SetBool("savegame.mod.oldsystem", oldsystem)
-				SetBool("savegame.mod.no_limit", no_limit)
-			end
-		end
-	UiPop()
-	UiTranslate(0, 70)
-	if oldsystem then
-	UiPush()
-	    UiTranslate(2, 0)
-		UiText("Infinite number of explosive")
-		UiTranslate(13, 40)
-		UiAlign("right")
-		UiColor(0.5, 0.8, 1)
-		if no_limit then
-			if UiTextButton("Yes", 20, 20) then
-				no_limit = false
-				SetBool("savegame.mod.no_limit", no_limit)
-			end
-		else
-		    UiTranslate(60, 0)
-			if UiTextButton("No (limit to 10)", 20, 20) then
-				no_limit = true
-				SetBool("savegame.mod.no_limit", no_limit)
-			end
-		end
-	UiPop()
-    else
-        UiTranslate(0, -70)
-	end
+    UiFont("bold.ttf", 48)
+    UiText("Explosive Pack by gs_115")
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+        UiTranslate(75, 0)
+    	last_input = InputLastPressedKey()
+    	if last_input ~= "" then
+    	    if changing_mode == 1 then input_ex = last_input end
+    		if changing_mode == 2 then input_change = last_input end
+    		SetString("savegame.mod.input_ex", input_ex, true)
+    		SetString("savegame.mod.input_change", input_change, true)
+    	    changing_mode = 0
+    	end
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+        if UiTextButton(input_ex, 50, 30) and changing_mode == 0 then --Explode Input
+    	    input_ex = "..."
+    		changing_mode = 1
+    	end
+    	UiTranslate(-90, 0)
+    	UiText("Explode All:", 150, 30)
 
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    	UiTranslate(110, 10)
+    	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+        if UiTextButton(input_change, 50, 30) and changing_mode == 0 then --Explode Input
+    	    input_change = "..."
+    		changing_mode = 2
+    	end
+    	UiTranslate(-110, 0)
+    	UiText("Change Explosif:", 150, 30)
+    UiPop()
+    UiTranslate(0, 90)
+    UiPush()
+    	UiText("Claymore Mode")
+    	UiTranslate(90, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if claymore_mode then
+    	    UiTranslate(-35, 0)
+    		if UiTextButton("\"Realistic\"", 20, 20) then
+    			claymore_mode = false
+    			SetBool("savegame.mod.claymore_mode", claymore_mode, true)
+    		end
+    	else
+    		if UiTextButton("High Performance", 20, 20) then
+    			claymore_mode = true
+    			SetBool("savegame.mod.claymore_mode", claymore_mode, true)
+    		end
+    	end
+    UiPop()
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Safety")
+    	UiTranslate(15, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if safe == 0 then
+    	    UiTranslate(12, 0)
+    		if UiTextButton("None", 20, 20) then
+    			safe = 1
+    			SetInt("savegame.mod.safe", safe, true)
+    		end
+    	elseif safe == 1 then
+    	    UiTranslate(42, 0)
+    		if UiTextButton("Triple Press", 20, 20) then
+    			safe = 2
+    			SetInt("savegame.mod.safe", safe, true)
+    		end
+    	else
+    	    UiTranslate(38, 0)
+    		if UiTextButton("Long Press", 20, 20) then
+    			safe = 0
+    			SetInt("savegame.mod.safe", safe, true)
+    		end
+    	end
+    UiPop()
+    UiTranslate(0, 70)
+    UiPush()
+        UiTranslate(2, 0)
+    	UiText("Use old display system")
+    	UiTranslate(13, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if oldsystem then
+    		if UiTextButton("Yes", 20, 20) then
+    			oldsystem = false
+    			no_limit = true
+    			SetBool("savegame.mod.oldsystem", oldsystem, true)
+    			SetBool("savegame.mod.no_limit", no_limit, true)
+    		end
+    	else
+    		if UiTextButton("No", 20, 20) then
+    			oldsystem = true
+    			no_limit = true
+    			SetBool("savegame.mod.oldsystem", oldsystem, true)
+    			SetBool("savegame.mod.no_limit", no_limit, true)
+    		end
+    	end
+    UiPop()
+    UiTranslate(0, 70)
+    if oldsystem then
+    UiPush()
+        UiTranslate(2, 0)
+    	UiText("Infinite number of explosive")
+    	UiTranslate(13, 40)
+    	UiAlign("right")
+    	UiColor(0.5, 0.8, 1)
+    	if no_limit then
+    		if UiTextButton("Yes", 20, 20) then
+    			no_limit = false
+    			SetBool("savegame.mod.no_limit", no_limit, true)
+    		end
+    	else
+    	    UiTranslate(60, 0)
+    		if UiTextButton("No (limit to 10)", 20, 20) then
+    			no_limit = true
+    			SetBool("savegame.mod.no_limit", no_limit, true)
+    		end
+    	end
+    UiPop()
+       else
+           UiTranslate(0, -70)
+    end
 
-	UiTranslate(0, 90)
-	if UiTextButton("Close", 80, 40) then
-		Menu()
-	end
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+
+    UiTranslate(0, 90)
+    if UiTextButton("Close", 80, 40) then
+    	Menu()
+    end
 end
 

```

---

# Migration Report: robotMod\robot.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/robotMod\robot.lua
+++ patched/robotMod\robot.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,35 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 3.5)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 25
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 100.0
-config.aggressive = false
-config.stepSound = "m"
-config.practice = false
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -180,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -197,40 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -238,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 	robot.body = FindBody("body")
@@ -258,28 +115,24 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -298,7 +151,7 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	local vel = GetBodyVelocity(robot.body)
@@ -310,7 +163,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -340,7 +193,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -355,35 +208,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -403,9 +244,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -413,10 +253,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -435,7 +271,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -452,7 +287,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -465,7 +299,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -481,8 +314,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -545,7 +376,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -554,7 +385,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -565,15 +396,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -590,11 +412,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -603,12 +425,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -641,7 +457,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -669,9 +484,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -716,7 +530,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -758,13 +572,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -805,13 +612,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -838,7 +643,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -847,9 +651,8 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -870,7 +673,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -883,22 +686,21 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 6.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
 				rejectAllBodies(robot.allBodies)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -922,7 +724,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -987,15 +789,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1005,7 +799,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1030,22 +823,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1084,32 +865,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1133,7 +894,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1180,8 +941,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1210,26 +971,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(0, -100, 0)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1265,35 +1017,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1385,7 +1118,7 @@
 		end
 
 		local targetRadius = 1.0
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 4.0
 		end
 	
@@ -1416,9 +1149,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1428,7 +1160,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1491,12 +1223,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1545,7 +1271,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1554,8 +1280,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1571,7 +1295,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1586,7 +1309,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1594,7 +1316,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1605,7 +1326,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1624,439 +1344,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
-	turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("robot/alert.ogg", 9.0)
-	huntSound = LoadSound("robot/hunt.ogg", 9.0)
-	idleSound = LoadSound("robot/idle.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	local damage_gs = 0
-	local total_health_gs = 0
-	for i=1, #robot.allShapes do
-		if HasTag(robot.allShapes[i], "gsgunsystemhitcount") then
-            damage_gs = damage_gs + tonumber(GetTagValue(robot.allShapes[i], "gsgunsystemhitcount")) * GetShapeVoxelCount(robot.allShapes[i])
-			total_health_gs = total_health_gs + GetShapeVoxelCount(robot.allShapes[i]) * 5.8
-        end
-	end
-	if IsPointInWater(robot.bodyCenter) or damage_gs > total_health_gs then
-		PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 6.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			PlaySound(alertSound, robot.bodyCenter, 1.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 1.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2065,64 +1352,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2146,14 +1375,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2169,19 +1397,15 @@
 	end
 end
 
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2199,8 +1423,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2227,3 +1449,470 @@
 	end
 end
 
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
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
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        local damage_gs = 0
+        local total_health_gs = 0
+        for i=1, #robot.allShapes do
+        	if HasTag(robot.allShapes[i], "gsgunsystemhitcount") then
+                   damage_gs = damage_gs + tonumber(GetTagValue(robot.allShapes[i], "gsgunsystemhitcount")) * GetShapeVoxelCount(robot.allShapes[i])
+        		total_health_gs = total_health_gs + GetShapeVoxelCount(robot.allShapes[i]) * 5.8
+               end
+        end
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 6.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
+    turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("robot/alert.ogg", 9.0)
+    huntSound = LoadSound("robot/hunt.ogg", 9.0)
+    idleSound = LoadSound("robot/idle.ogg", 9.0)
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if IsPointInWater(robot.bodyCenter) or damage_gs > total_health_gs then
+    	PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+    	for i=1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "huntlost" then
+    	if not state.timer then
+    		state.timer = 6
+    		state.turnTimer = 1
+    	end
+    	state.timer = state.timer - dt
+    	head.dir = VecCopy(robot.dir)
+    	if state.timer < 0 then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	else
+    		state.turnTimer = state.turnTimer - dt
+    		if state.turnTimer < 0 then
+    			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+    			state.turnTimer = rnd(0.5, 1.5)
+    		end
+    	end
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		PlaySound(alertSound, robot.bodyCenter, 1.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 1.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```

---

# Migration Report: robotMod\robotOriginal.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/robotMod\robotOriginal.lua
+++ patched/robotMod\robotOriginal.lua
@@ -1,84 +1,7 @@
-#include "script/common.lua"
-
-------------------------------------------------------------------------------------
--- ROBOT SCRIPT
-------------------------------------------------------------------------------------
---[[
-
-The robot script should be parent of all bodies that make up the robot. 
-Configure the robot with the type parameter that can be combinations of the following words:
-investigate: investigate sounds in the environment
-chase: chase player when seen, this is the most common configuration
-nooutline: no outline when close and hidden
-alarm: trigger alarm when player is seen and lit by light for 2.0 seconds 
-stun: electrocute player when close or grabbed
-avoid: avoid player (should not be combined chase, requires patrol locations)
-aggressive: always know where player is (even through walls)
-
-The following robot parts are supported:
-
-body (type body: required)
-This is the main part of the robot and should be the hevaiest part
-
-head (type body: required)
-The head should be jointed to the body (hinge joint with or without limits). 
-heardist=<value> - Maximum hearing distance in meters, default 100
-
-eye (type light: required)
-Represents robot vision. The direction of light source determines what the robot can see. Can be placed on head or body
-viewdist=<value> - View distance in meters. Default 25.
-viewfov=<value> - View field of view in degrees. Default 150.
-
-aim (type body: optional)
-This part will be directed towards the player when seen and is usually equipped with weapons. Should be jointed to body or head with ball joint. There can be multiple aims.
-
-wheel (type body: optional, should be static with no collisions)
-If present wheels will rotate along with the motion of the robot. There can be multiple wheels.
-
-leg (type body: optional)
-Legs should be jointed between body and feet. All legs will have collisions disabled when walking and enabled in rag doll mode. There can be multiple legs.
-
-foot (type body: optional)
-Foot bodies are animated with respect to the body when walking. They only collide with the environment in rag doll mode.
-tag force - Movement force scale, default is 1. Can also be two values to separate linear and angular, for example: 2,0.5
-
-weapon (type location: optional)
-Usually placed on aim head or body. There are several types of weapons:
-weapon=fire - Emit fire when player is close and seen
-weapon=gun - Regular shot
-weapon=rocket - Fire rockets
-strength=<value> - The scaling factor which controls how much damage it makes (default is 1.0)
-The following tags are used to control the weapon behavior (only affect gun and rocket):
-idle=<seconds> - Idle time in between rounds
-charge=<seconds> - Charge time before firing
-cooldown=<seconds> - Cooldown between each shot in a round
-count=<number> - Number of shots in a round
-spread=<fraction> - How much each shot may deviates from optimal direction (for instance: 0.05 to deviate up to 5%)
-maxdist=<meters> - How far away target can be to trigger shot. Default is 100
-
-patrol (type location: optional)
-If present the robot will patrol these locations. Make sure to place near walkable ground. Targets are visited in the same order they appear in scene explorer. Avoid type robots MUST have patrol targets.
-
-roam (type trigger: optional)
-If there are no patrol locations, the robot will roam randomly within this trigger.
-
-limit (type trigger: optional)
-If present the robot will try stay within this trigger volume. If robot ends up outside trigger, it will automatically navigate back inside.
-
-investigate (type trigger: optional)
-If present and the robot has type investigate it will only react to sounds within this trigger.
-
-activate (type trigger: optional)
-If present, robot will start inactive and become activated when player enters trigger
-]]
-------------------------------------------------------------------------------------
-
-
-
+#version 2
 function VecDist(a, b)
 	return VecLength(VecSub(a, b))
 end
-
 
 function getTagParameter(entity, name, default)
 	local v = tonumber(GetTagValue(entity, name))
@@ -110,35 +33,6 @@
 		return default, default
 	end
 end
-
-pType = GetStringParam("type", "")
-pSpeed = GetFloatParam("speed", 3.5)
-pTurnSpeed = GetFloatParam("turnspeed", pSpeed)
-
-config = {}
-config.hasVision = false
-config.viewDistance = 25
-config.viewFov = 150
-config.canHearPlayer = false
-config.canSeePlayer = false
-config.patrol = false
-config.sensorDist = 5.0
-config.speed = pSpeed
-config.turnSpeed = pTurnSpeed
-config.huntPlayer = false
-config.huntSpeedScale = 1.6
-config.avoidPlayer = false
-config.triggerAlarmWhenSeen = false
-config.visibilityTimer = 0.3 --Time player must be seen to be identified as enemy (ideal condition)
-config.lostVisibilityTimer = 5.0 --Time player is seen after losing visibility
-config.outline = 13
-config.aimTime = 5.0
-config.maxSoundDist = 100.0
-config.aggressive = false
-config.stepSound = "m"
-config.practice = false
-
-PATH_NODE_TOLERANCE = 0.8
 
 function configInit()
 	local eye = FindLight("eye")
@@ -180,8 +74,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
 function rndVec(length)
 	local v = VecNormalize(Vec(math.random(-100,100), math.random(-100,100), math.random(-100,100)))
 	return VecScale(v, length)	
@@ -197,40 +89,6 @@
 		QueryRejectBody(bodies[i])
 	end
 end
-
-------------------------------------------------------------------------
-
-
-robot = {}
-robot.body = 0
-robot.transform = Transform()
-robot.axes = {}
-robot.bodyCenter = Vec()
-robot.navigationCenter = Vec()
-robot.dir = Vec(0, 0, -1)
-robot.speed = 0
-robot.blocked = 0
-robot.mass = 0
-robot.allBodies = {}
-robot.allShapes = {}
-robot.allJoints = {}
-robot.initialBodyTransforms = {}
-robot.enabled = true
-robot.deleted = false
-robot.speedScale = 1
-robot.breakAll = false
-robot.breakAllTimer = 0
-robot.distToPlayer = 100
-robot.dirToPlayer = 0
-robot.roamTrigger = 0
-robot.limitTrigger = 0
-robot.investigateTrigger = 0
-robot.activateTrigger = 0
-robot.stunned = 0
-robot.outlineAlpha = 0
-robot.canSensePlayer = false
-robot.playerPos = Vec()
-
 
 function robotSetAxes()
 	robot.transform = GetBodyTransform(robot.body)
@@ -238,7 +96,6 @@
 	robot.axes[2] = TransformToParentVec(robot.transform, Vec(0, 1, 0))
 	robot.axes[3] = TransformToParentVec(robot.transform, Vec(0, 0, 1))
 end
-
 
 function robotInit()
 	robot.body = FindBody("body")
@@ -258,28 +115,24 @@
 	robotSetAxes()
 end
 
-
 function robotTurnTowards(pos)
 	robot.dir = VecNormalize(VecSub(pos, robot.transform.pos))
 end
-
 
 function robotSetDirAngle(angle)
 	robot.dir[1] = math.cos(angle)
 	robot.dir[3] = math.sin(angle)
 end
 
-
 function robotGetDirAngle()
 	return math.atan2(robot.dir[3], robot.dir[1])
 end
 
-
 function robotUpdate(dt)
 	robotSetAxes()
 
 	if config.practice then
-		local pp = GetPlayerCameraTransform().pos
+		local pp = GetPlayerCameraTransform(playerId).pos
 		local pt = FindTrigger("practicearea")
 		if pt ~= 0 and IsPointInTrigger(pt, pp) then
 			robot.playerPos = VecCopy(pp)
@@ -298,7 +151,7 @@
 			end
 		end
 	else
-		robot.playerPos = GetPlayerCameraTransform().pos
+		robot.playerPos = GetPlayerCameraTransform(playerId).pos
 	end
 	
 	local vel = GetBodyVelocity(robot.body)
@@ -310,7 +163,7 @@
 	robot.blocked = robot.blocked * 0.95 + blocked * 0.05
 
 	--Always blocked if fall is detected
-	if sensor.detectFall > 0 then
+	if sensor.detectFall ~= 0 then
 		robot.blocked = 1.0
 	end
 
@@ -340,7 +193,7 @@
 	end
 	
 	--Distance and direction to player
-	local pp = VecAdd(GetPlayerTransform().pos, Vec(0, 1, 0))
+	local pp = VecAdd(GetPlayerTransform(playerId).pos, Vec(0, 1, 0))
 	local d = VecSub(pp, robot.bodyCenter)
 	robot.distToPlayer = VecLength(d)
 	robot.dirToPlayer = VecScale(d, 1.0/robot.distToPlayer)
@@ -355,35 +208,23 @@
 	end
 
 	--Robot body sounds
-	if robot.enabled and hover.contact > 0 then
+	if robot.enabled and hover.contact ~= 0 then
 		local vol
 		vol = clamp(VecLength(GetBodyVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			PlayLoop(walkLoop, robot.transform.pos, vol)
 		end
 
 		vol = clamp(VecLength(GetBodyAngularVelocity(robot.body)) * 0.4, 0.0, 1.0)
-		if vol > 0 then
+		if vol ~= 0 then
 			PlayLoop(turnLoop, robot.transform.pos, vol)
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-hover = {}
-hover.hitBody = 0
-hover.contact = 0.0
-hover.distTarget = 1.1
-hover.distPadding = 0.3
-hover.timeSinceContact = 0.0
-
 
 function hoverInit()
 	local f = FindBodies("foot")
-	if #f > 0 then
+	if #f ~= 0 then
 		hover.distTarget = 0
 		for i=1, #f do
 			local ft = GetBodyTransform(f[i])
@@ -403,9 +244,8 @@
 	end
 end
 
-
 function hoverFloat()
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local d = clamp(hover.distTarget - hover.currentDist, -0.2, 0.2)
 		local v = d * 10
 		local f = hover.contact * math.max(0, d*robot.mass*5.0) + robot.mass*0.2
@@ -413,10 +253,6 @@
 	end
 end
 
-
-UPRIGHT_STRENGTH = 1.0	-- Spring strength
-UPRIGHT_MAX = 0.5		-- Max spring force
-UPRIGHT_BASE = 0.1		-- Fraction of max spring force to always apply (less springy)
 function hoverUpright()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -435,7 +271,6 @@
 	end
 end
 
-
 function hoverGetUp()
 	local up = VecCross(robot.axes[2], VecAdd(Vec(0,1,0)))
 	axes = {}
@@ -452,7 +287,6 @@
 	end
 end
 
-
 function hoverTurn()
 	local fwd = VecScale(robot.axes[3], -1)
 	local c = VecCross(fwd, robot.dir)
@@ -465,7 +299,6 @@
 	local f = robot.mass*0.5 * hover.contact
 	ConstrainAngularVelocity(robot.body, hover.hitBody, robot.axes[2], angVel, -f , f)
 end
-
 
 function hoverMove()
 	local desiredSpeed = robot.speed * robot.speedScale
@@ -481,8 +314,6 @@
 	ConstrainVelocity(robot.body, hover.hitBody, robot.bodyCenter, robot.axes[1], 0, -f , f)
 end
 
-
-BALANCE_RADIUS = 0.4
 function hoverUpdate(dt)
 	local dir = VecScale(robot.axes[2], -1)
 
@@ -545,7 +376,7 @@
 	end
 	
 	--Limit body angular velocity magnitude to 10 rad/s at max contact
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		local maxAngVel = 10.0 / hover.contact
 		local angVel = GetBodyAngularVelocity(robot.body)
 		local angVelLength = VecLength(angVel)
@@ -554,7 +385,7 @@
 		end
 	end
 	
-	if hover.contact > 0 then
+	if hover.contact ~= 0 then
 		hover.timeSinceContact = 0
 	else
 		hover.timeSinceContact = hover.timeSinceContact + dt
@@ -565,15 +396,6 @@
 	hoverTurn()
 	hoverMove()
 end
-
-
-------------------------------------------------------------------------
-
-
-wheels = {}
-wheels.bodies = {}
-wheels.transforms = {}
-wheels.radius = {}
 
 function wheelsInit()
 	wheels.bodies = FindBodies("wheel")
@@ -590,11 +412,11 @@
 	for i=1, #wheels.bodies do
 		local v = GetBodyVelocityAtPos(robot.body, TransformToParentPoint(robot.transform, wheels.transforms[i].pos))
 		local lv = VecDot(robot.axes[3], v)
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			local shapes = GetBodyShapes(wheels.bodies[i])
-			if #shapes > 0 then
+			if #shapes ~= 0 then
 				local joints = GetShapeJoints(shapes[1])
-				if #joints > 0 then
+				if #joints ~= 0 then
 					local angVel = lv / wheels.radius[i]
 					SetJointMotor(joints[1], angVel, 100)
 				end
@@ -603,12 +425,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-feet = {}
 
 function feetInit()
 	local f = FindBodies("foot")
@@ -641,7 +457,6 @@
 	end
 end
 
-
 function feetCollideLegs(enabled)
 	local mask = 0
 	if enabled then
@@ -669,9 +484,8 @@
 	end
 end
 
-
 function feetUpdate(dt)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		feetCollideLegs(true)
 		return
 	else
@@ -716,7 +530,7 @@
 		end
 
 		--Animate foot
-		if hover.contact > 0 then
+		if hover.contact ~= 0 then
 			if foot.stepAge < foot.stepLifeTime then
 				foot.stepAge = math.min(foot.stepAge + dt, foot.stepLifeTime)
 				local q = foot.stepAge / foot.stepLifeTime
@@ -758,13 +572,6 @@
 		end
 	end
 end
-
-
-------------------------------------------------------------------------
-
-
-
-weapons = {}
 
 function weaponsInit()
 	local locs = FindLocations("weapon")
@@ -805,13 +612,11 @@
 	end
 end
 
-
 function getPerpendicular(dir)
 	local perp = VecNormalize(Vec(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)))
 	perp = VecNormalize(VecSub(perp, VecScale(dir, VecDot(dir, perp))))
 	return perp
 end
-
 
 function weaponFire(weapon, pos, dir)
 	local perp = getPerpendicular(dir)
@@ -838,7 +643,6 @@
 	end
 end
 
-
 function weaponsReset()
 	for i=1, #weapons do
 		weapons[i].state = "idle"
@@ -847,9 +651,8 @@
 	end
 end
 
-
 function weaponEmitFire(weapon, t, amount)
-	if robot.stunned > 0 then
+	if robot.stunned ~= 0 then
 		return
 	end
 	local p = TransformToParentPoint(t, Vec(0, 0, -0.1))
@@ -870,7 +673,7 @@
 		if not spawnFireTimer then
 			spawnFireTimer = 0
 		end
-		if spawnFireTimer > 0 then
+		if spawnFireTimer ~= 0 then
 			spawnFireTimer = math.max(spawnFireTimer-0.01667, 0)
 		else
 			rejectAllBodies(robot.allBodies)
@@ -883,22 +686,21 @@
 		end
 		
 		--Hurt player
-		local toPlayer = VecSub(GetPlayerCameraTransform().pos, t.pos)
+		local toPlayer = VecSub(GetPlayerCameraTransform(playerId).pos, t.pos)
 		local distToPlayer = VecLength(toPlayer)
 		local distScale = clamp(1.0 - distToPlayer / 6.0, 0.0, 1.0)
-		if distScale > 0 then
+		if distScale ~= 0 then
 			toPlayer = VecNormalize(toPlayer)
 			if VecDot(d, toPlayer) > 0.8 or distToPlayer < 0.5 then
 				rejectAllBodies(robot.allBodies)
 				local hit = QueryRaycast(p, toPlayer, distToPlayer)
 				if not hit or distToPlayer < 0.5 then
-					SetPlayerHealth(GetPlayerHealth() - 0.02 * weapon.strength * amount * distScale)
+					SetPlayerHealth(playerId, GetPlayerHealth(playerId) - 0.02 * weapon.strength * amount * distScale)
 				end
 			end	
 		end
 	end
 end
-
 
 function weaponsUpdate(dt)
 	for i=1, #weapons do
@@ -922,7 +724,7 @@
 			else
 				weapon.fire = math.max(weapon.fire - dt*0.5, 0.0)
 			end
-			if weapon.fire > 0 then
+			if weapon.fire ~= 0 then
 				weaponEmitFire(weapon, t, weapon.fire)
 			else
 				weaponEmitFire(weapon, t, math.max(weapon.fire, 0.1))
@@ -987,15 +789,7 @@
 			end
 		end
 	end
-end	
-
-
-
-------------------------------------------------------------------------
-
-
-
-aims = {}
+end
 
 function aimsInit()
 	local bodies = FindBodies("aim")
@@ -1005,7 +799,6 @@
 		aims[i] = aim
 	end
 end
-
 
 function aimsUpdate(dt)
 	for i=1, #aims do
@@ -1030,22 +823,10 @@
 			ConstrainOrientation(robot.body, aim.body, GetBodyTransform(robot.body).rot, GetBodyTransform(aim.body).rot, v, f)
 		end
 	end
-end	
-	
-
-------------------------------------------------------------------------
-
-
-sensor = {}
-sensor.blocked = 0
-sensor.blockedLeft = 0
-sensor.blockedRight = 0
-sensor.detectFall = 0
-
+end
 
 function sensorInit()
 end
-
 
 function sensorGetBlocked(dir, maxDist)
 	dir = VecNormalize(VecAdd(dir, rndVec(0.3)))
@@ -1084,32 +865,12 @@
 	sensor.blockedRight = sensor.blockedRight * 0.9 + blockedRight * 0.1
 end
 
-
-------------------------------------------------------------------------
-
-
-head = {}
-head.body = 0
-head.eye = 0
-head.dir = Vec(0,0,-1)
-head.lookOffset = 0
-head.lookOffsetTimer = 0
-head.canSeePlayer = false
-head.lastSeenPos = Vec(0,0,0)
-head.timeSinceLastSeen = 999
-head.seenTimer = 0
-head.alarmTimer = 0
-head.alarmTime = 2.0
-head.aim = 0	-- 1.0 = perfect aim, 0.0 = will always miss player. This increases when robot sees player based on config.aimTime
-
-
 function headInit()
 	head.body = FindBody("head")
 	head.eye = FindLight("eye")
 	head.joint = FindJoint("head")
 	head.alarmTime = getTagParameter(head.eye, "alarm", 2.0)
 end
-
 
 function headTurnTowards(pos)
 	head.dir = VecNormalize(VecSub(pos, GetBodyTransform(head.body).pos))
@@ -1133,7 +894,7 @@
 			local limit = math.cos(config.viewFov * 0.5 * math.pi / 180)
 			if VecDot(toPlayer, fwd) > limit then --In view frustum
 				rejectAllBodies(robot.allBodies)
-				QueryRejectVehicle(GetPlayerVehicle())
+				QueryRejectVehicle(GetPlayerVehicle(playerId))
 				if not QueryRaycast(et.pos, toPlayer, distToPlayer, 0, true) then --Not blocked
 					playerVisible = true
 				end
@@ -1180,8 +941,8 @@
 				head.alarmTimer = head.alarmTimer + dt
 				PlayLoop(chargeLoop, robot.transform.pos)
 				if head.alarmTimer > head.alarmTime and playerVisible then
-					SetString("hud.notification", "Detected by robot. Alarm triggered.")
-					SetBool("level.alarm", true)
+					SetString("hud.notification", "Detected by robot. Alarm triggered.", true)
+					SetBool("level.alarm", true, true)
 				end
 			else
 				head.alarmTimer = math.max(0.0, head.alarmTimer - dt)
@@ -1210,26 +971,17 @@
 	if ang < mi+1 and angVel < 0 then
 		angVel = 0
 	end
-	if ang > ma-1 and angVel > 0 then
+	if ang > ma-1 and angVel ~= 0 then
 		angVel = 0
 	end
 
 	ConstrainAngularVelocity(head.body, robot.body, robot.axes[2], angVel, -f , f)
 
 	local vol = clamp(math.abs(angVel)*0.3, 0.0, 1.0)
-	if vol > 0 then
+	if vol ~= 0 then
 		PlayLoop(headLoop, robot.transform.pos, vol)
 	end
 end
-
-
-------------------------------------------------------------------------
-
-hearing = {}
-hearing.lastSoundPos = Vec(0, -100, 0)
-hearing.lastSoundVolume = 0
-hearing.timeSinceLastSound = 0
-hearing.hasNewSound = false
 
 function hearingInit()
 end
@@ -1265,35 +1017,16 @@
 	hearing.hasNewSound = false
 end
 
-------------------------------------------------------------------------
-
-navigation = {}
-navigation.state = "done"
-navigation.path = {}
-navigation.target = Vec()
-navigation.hasNewTarget = false
-navigation.resultRetrieved = true
-navigation.deviation = 0		-- Distance to path
-navigation.blocked = 0
-navigation.unblockTimer = 0		-- Timer that ticks up when blocked. If reaching limit, unblock kicks in and timer resets
-navigation.unblock = 0			-- If more than zero, navigation is in unblock mode (reverse direction)
-navigation.vertical = 0
-navigation.thinkTime = 0
-navigation.timeout = 1
-navigation.lastQueryTime = 0
-navigation.timeSinceProgress = 0
-
 function navigationInit()
-	if #wheels.bodies > 0 then
+	if #wheels.bodies ~= 0 then
 		navigation.pathType = "low"
 	else
 		navigation.pathType = "standard"
 	end
 end
 
---Prune path backwards so robot don't need to go backwards
 function navigationPrunePath()
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		for i=#navigation.path, 1, -1 do
 			local p = navigation.path[i]
 			local dv = VecSub(p, robot.transform.pos)
@@ -1385,7 +1118,7 @@
 		end
 
 		local targetRadius = 1.0
-		if GetPlayerVehicle()~=0 then
+		if GetPlayerVehicle(playerId)~=0 then
 			targetRadius = 4.0
 		end
 	
@@ -1416,9 +1149,8 @@
 	end
 end
 
-
 function navigationMove(dt)
-	if #navigation.path > 0 then
+	if #navigation.path ~= 0 then
 		if navigation.resultRetrieved then
 			--If we have a finished path and didn't progress along it for five seconds, recompute
 			--Should probably only do this for a limited time until giving up
@@ -1428,7 +1160,7 @@
 				navigation.path = {}
 			end
 		end
-		if navigation.unblock > 0 then
+		if navigation.unblock ~= 0 then
 			robot.speed = -2
 			navigation.unblock = navigation.unblock - dt
 		else
@@ -1491,12 +1223,6 @@
 	end
 end
 
-------------------------------------------------------------------------
-
-
-stack = {}
-stack.list = {}
-
 function stackTop()
 	return stack.list[#stack.list]
 end
@@ -1545,7 +1271,7 @@
 end
 
 function stackUpdate(dt)
-	if #stack.list > 0 then
+	if #stack.list ~= 0 then
 		for i=1, #stack.list do
 			stack.list[i].totalTime = stack.list[i].totalTime + dt
 		end
@@ -1554,8 +1280,6 @@
 		stack.list[#stack.list].activeTime = stack.list[#stack.list].activeTime + dt
 	end
 end
-
-
 
 function getClosestPatrolIndex()
 	local bestIndex = 1
@@ -1571,7 +1295,6 @@
 	return bestIndex
 end
 
-
 function getDistantPatrolIndex(currentPos)
 	local bestIndex = 1
 	local bestDistance = 0
@@ -1586,7 +1309,6 @@
 	return bestIndex
 end
 
-
 function getNextPatrolIndex(current)
 	local i = current + 1
 	if i > #patrolLocations then
@@ -1594,7 +1316,6 @@
 	end
 	return i
 end
-
 
 function markPatrolLocationAsActive(index)
 	for i=1, #patrolLocations do
@@ -1605,7 +1326,6 @@
 		end
 	end
 end
-
 
 function debugState()
 	local state = stackTop()
@@ -1624,431 +1344,6 @@
 	DebugWatch("GetPathState()", GetPathState())
 end
 
-
-function init()
-	configInit()
-	robotInit()
-	hoverInit()
-	headInit()
-	sensorInit()
-	wheelsInit()
-	feetInit()
-	aimsInit()
-	weaponsInit()
-	navigationInit()
-	hearingInit()
-	stackInit()
-
-	patrolLocations = FindLocations("patrol")
-	shootSound = LoadSound("tools/gun0.ogg", 8.0)
-	rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
-	local nomDist = 7.0
-	if config.stepSound == "s" then nomDist = 5.0 end
-	if config.stepSound == "l" then nomDist = 9.0 end
-	stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
-	headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
-	turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
-	walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
-	rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
-	chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
-	alertSound = LoadSound("robot/alert.ogg", 9.0)
-	huntSound = LoadSound("robot/hunt.ogg", 9.0)
-	idleSound = LoadSound("robot/idle.ogg", 9.0)
-	fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
-	disableSound = LoadSound("robot/disable0.ogg")
-end
-
-
-function update(dt)
-	if robot.deleted then 
-		return
-	else 
-		if not IsHandleValid(robot.body) then
-			for i=1, #robot.allBodies do
-				Delete(robot.allBodies[i])
-			end
-			for i=1, #robot.allJoints do
-				Delete(robot.allJoints[i])
-			end
-			robot.deleted = true
-		end
-	end
-
-	if robot.activateTrigger ~= 0 then 
-		if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform().pos) then
-			RemoveTag(robot.body, "inactive")
-			robot.activateTrigger = 0
-		end
-	end
-	
-	if HasTag(robot.body, "inactive") then
-		robot.inactive = true
-		return
-	else
-		if robot.inactive then
-			robot.inactive = false
-			--Reset robot pose
-			local sleep = HasTag(robot.body, "sleeping")
-			for i=1, #robot.allBodies do
-				SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
-				SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
-				SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
-				if sleep then
-					--If robot is sleeping make sure to not wake it up
-					SetBodyActive(robot.allBodies[i], false)
-				end
-			end
-		end
-	end
-
-	if HasTag(robot.body, "sleeping") then
-		if IsBodyActive(robot.body) then
-			wakeUp = true
-		end
-		local vol, pos = GetLastSound()
-		if vol > 0.2 then
-			if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
-				wakeUp = true
-			end
-		end	
-		if wakeUp then
-			RemoveTag(robot.body, "sleeping")
-		end
-		return
-	end
-
-	robotUpdate(dt)
-	wheelsUpdate(dt)
-
-	if not robot.enabled then
-		return
-	end
-
-	feetUpdate(dt)
-	
-	if IsPointInWater(robot.bodyCenter) then
-		PlaySound(disableSound, robot.bodyCenter, 1.0, false)
-		for i=1, #robot.allShapes do
-			SetShapeEmissiveScale(robot.allShapes[i], 0)
-		end
-		SetTag(robot.body, "disabled")
-		robot.enabled = false
-	end
-	
-	robot.stunned = clamp(robot.stunned - dt, 0.0, 6.0)
-	if robot.stunned > 0 then
-		head.seenTimer = 0
-		weaponsReset()
-		return
-	end
-	
-	hoverUpdate(dt)
-	headUpdate(dt)
-	sensorUpdate(dt)
-	aimsUpdate(dt)
-	weaponsUpdate(dt)
-	hearingUpdate(dt)
-	stackUpdate(dt)
-	robot.speedScale = 1
-	robot.speed = 0
-	local state = stackTop()
-	
-	if state.id == "none" then
-		if config.patrol then
-			stackPush("patrol")
-		else
-			stackPush("roam")
-		end
-	end
-
-	if state.id == "roam" then
-		if not state.nextAction then
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			local randomPos
-			if robot.roamTrigger ~= 0 then
-				randomPos = getRandomPosInTrigger(robot.roamTrigger)
-				randomPos = truncateToGround(randomPos)
-			else
-				local rndAng = rnd(0, 2*math.pi)
-				randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
-			end
-			local s = stackPush("navigate")
-			s.timeout = 1
-			s.pos = randomPos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "patrol" then
-		if not state.nextAction then
-			state.index = getClosestPatrolIndex()
-			state.nextAction = "move"
-		elseif state.nextAction == "move" then
-			markPatrolLocationAsActive(state.index)
-			local nav = stackPush("navigate")
-			nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.index = getNextPatrolIndex(state.index)
-			state.nextAction = "move"
-		end
-	end
-
-	
-	if state.id == "search" then
-		if state.activeTime > 2.5 then
-			if not state.turn then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turn = true
-			end
-			if state.activeTime > 6.0 then
-				stackPop()
-			end
-		end
-		if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
-			head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
-		else
-			head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
-		end
-	end
-
-	
-	if state.id == "investigate" then
-		if not state.nextAction then
-			local pos = state.pos
-			robotTurnTowards(state.pos)
-			headTurnTowards(state.pos)
-			local nav = stackPush("navigate")
-			nav.pos = state.pos
-			nav.timeout = 5.0
-			state.nextAction = "search"
-		elseif state.nextAction == "search" then
-			stackPush("search")
-			state.nextAction = "done"
-		elseif state.nextAction == "done" then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		end	
-	end
-	
-	if state.id == "move" then
-		robotTurnTowards(state.pos)
-		robot.speed = config.speed
-		head.dir = VecCopy(robot.dir)
-		local d = VecLength(VecSub(state.pos, robot.transform.pos))
-		if d < 2 then
-			robot.speed = 0
-			stackPop()
-		else
-			if robot.blocked > 0.5 then
-				stackPush("unblock")
-			end
-		end
-	end
-	
-	if state.id == "unblock" then
-		if not state.dir then
-			if math.random(0, 10) < 5 then
-				state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
-			else
-				state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
-			end
-			state.dir = VecNormalize(state.dir)
-		else
-			robot.dir = state.dir
-			robot.speed = -math.min(config.speed, 2.0)
-			if state.activeTime > 1 then
-				stackPop()
-			end
-		end
-	end
-
-	--Hunt player
-	if state.id == "hunt" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		if robot.distToPlayer < 4.0 then
-			robot.dir = VecCopy(robot.dirToPlayer)
-			head.dir = VecCopy(robot.dirToPlayer)
-			robot.speed = 0
-			navigationClear()
-		else
-			navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
-			robot.speedScale = config.huntSpeedScale
-			navigationUpdate(dt)
-			if head.canSeePlayer then
-				head.dir = VecCopy(robot.dirToPlayer)
-				state.headAngle = 0
-				state.headAngleTimer = 0
-			else
-				state.headAngleTimer = state.headAngleTimer + dt
-				if state.headAngleTimer > 1.0 then
-					if state.headAngle > 0.0 then
-						state.headAngle = rnd(-1.0, -0.5)
-					elseif state.headAngle < 0 then
-						state.headAngle = rnd(0.5, 1.0)
-					else
-						state.headAngle = rnd(-1.0, 1.0)
-					end
-					state.headAngleTimer = 0
-				end
-				head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-			end
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
-			--Turn towards player if not moving
-			robot.dir = VecCopy(robot.dirToPlayer)
-		end
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
-			if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
-				stackClear()
-				local s = stackPush("investigate")
-				s.pos = VecCopy(head.lastSeenPos)		
-			else
-				stackClear()
-				stackPush("huntlost")
-			end
-		end
-	end
-
-	if state.id == "huntlost" then
-		if not state.timer then
-			state.timer = 6
-			state.turnTimer = 1
-		end
-		state.timer = state.timer - dt
-		head.dir = VecCopy(robot.dir)
-		if state.timer < 0 then
-			PlaySound(idleSound, robot.bodyCenter, 1.0, false)
-			stackPop()
-		else
-			state.turnTimer = state.turnTimer - dt
-			if state.turnTimer < 0 then
-				robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
-				state.turnTimer = rnd(0.5, 1.5)
-			end
-		end
-	end
-	
-	--Avoid player
-	if state.id == "avoid" then
-		if not state.init then
-			navigationClear()
-			state.init = true
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		end
-		
-		local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform().pos)
-		local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
-		navigationSetTarget(avoidTarget, 1.0)
-		robot.speedScale = config.huntSpeedScale
-		navigationUpdate(dt)
-		if head.canSeePlayer then
-			head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
-			state.headAngle = 0
-			state.headAngleTimer = 0
-		else
-			state.headAngleTimer = state.headAngleTimer + dt
-			if state.headAngleTimer > 1.0 then
-				if state.headAngle > 0.0 then
-					state.headAngle = rnd(-1.0, -0.5)
-				elseif state.headAngle < 0 then
-					state.headAngle = rnd(0.5, 1.0)
-				else
-					state.headAngle = rnd(-1.0, 1.0)
-				end
-				state.headAngleTimer = 0
-			end
-			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
-		end
-		
-		if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
-			stackClear()
-		end
-	end
-	
-	--Get up player
-	if state.id == "getup" then
-		if not state.time then 
-			state.time = 0 
-		end
-		state.time = state.time + dt
-		hover.timeSinceContact = 0
-		if state.time > 2.0 then
-			stackPop()
-		else
-			hoverGetUp()
-		end
-	end
-
-	if state.id == "navigate" then
-		if not state.initialized then
-			if not state.timeout then state.timeout = 30 end
-			navigationClear()
-			navigationSetTarget(state.pos, state.timeout)
-			state.initialized = true
-		else
-			head.dir = VecCopy(robot.dir)
-			navigationUpdate(dt)
-			if navigation.state == "done" or navigation.state == "fail" then
-				stackPop()
-			end
-		end
-	end
-
-	--React to sound
-	if not stackHas("hunt") then
-		if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
-			stackClear()
-			PlaySound(alertSound, robot.bodyCenter, 1.0, false)
-			local s = stackPush("investigate")
-			s.pos = hearing.lastSoundPos	
-			hearingConsumeSound()
-		end
-	end
-	
-	--Seen player
-	if config.huntPlayer and not stackHas("hunt") then
-		if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
-			stackClear()
-			PlaySound(huntSound, robot.bodyCenter, 1.0, false)
-			stackPush("hunt")
-		end
-	end
-	
-	--Seen player
-	if config.avoidPlayer and not stackHas("avoid") then
-		if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
-			stackClear()
-			stackPush("avoid")
-		end
-	end
-	
-	--Get up
-	if hover.timeSinceContact > 3.0 and not stackHas("getup") then
-		stackPush("getup")
-	end
-	
-	if IsShapeBroken(GetLightShape(head.eye)) then
-		config.hasVision = false
-		config.canSeePlayer = false
-	end
-	
-	--debugState()
-end
-
-
 function canBeSeenByPlayer()
 	for i=1, #robot.allShapes do
 		if IsShapeVisible(robot.allShapes[i], config.outline, true) then
@@ -2057,64 +1352,6 @@
 	end
 	return false
 end
-
-
-function tick(dt)
-	if not robot.enabled then
-		return
-	end
-	
-	if HasTag(robot.body, "turnhostile") then
-		RemoveTag(robot.body, "turnhostile")
-		config.canHearPlayer = true
-		config.canSeePlayer = true
-		config.huntPlayer = true
-		config.aggressive = true
-		config.practice = false
-	end
-	
-	--Outline
-	local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform().pos)
-	if dist < config.outline then
-		local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
-		if canBeSeenByPlayer() then
-			a = 0
-		end
-		robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
-		for i=1, #robot.allBodies do
-			DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
-		end
-	end
-	
-	--Remove planks and wires after some time
-	local tags = {"plank", "wire"}
-	local removeTimeOut = 10
-	for i=1, #robot.allShapes do
-		local shape = robot.allShapes[i]
-		local joints = GetShapeJoints(shape)
-		for j=1, #joints do
-			local joint = joints[j]
-			for t=1, #tags do
-				local tag = tags[t]
-				if HasTag(joint, tag) then
-					local t = tonumber(GetTagValue(joint, tag)) or 0
-					t = t + dt
-					if t > removeTimeOut then
-						if GetJointType(joint) == "rope" then
-							DetachJointFromShape(joint, shape)
-						else
-							Delete(joint)
-						end
-						break
-					else
-						SetTag(joint, tag, t)
-					end
-				end
-			end
-		end
-	end
-end
-
 
 function hitByExplosion(strength, pos)
 	--Explosions smaller than 1.0 are ignored (with a bit of room for rounding errors)
@@ -2138,14 +1375,13 @@
 			local v = GetBodyVelocity(b)
 			local scale = clamp(1.0-VecLength(v)/maxVel, 0.0, 1.0)
 			local velAdd = math.min(maxVel, f*scale*strength)
-			if velAdd > 0 then
+			if velAdd ~= 0 then
 				v = VecAdd(v, VecScale(dir, velAdd))
 				SetBodyVelocity(b, v)
 			end
 		end
 	end
 end
-
 
 function hitByShot(strength, pos, dir)
 	if VecDist(pos, robot.bodyCenter) < 3 then
@@ -2161,19 +1397,15 @@
 	end
 end
 
----------------------------------------------------------------------------------
-
-
 function truncateToGround(pos)
 	rejectAllBodies(robot.allBodies)
-	QueryRejectVehicle(GetPlayerVehicle())
+	QueryRejectVehicle(GetPlayerVehicle(playerId))
 	hit, dist = QueryRaycast(pos, Vec(0, -1, 0), 5, 0.2)
 	if hit then
 		pos = VecAdd(pos, Vec(0, -dist, 0))
 	end
 	return pos
 end
-
 
 function getRandomPosInTrigger(trigger)
 	local mi, ma = GetTriggerBounds(trigger)
@@ -2191,8 +1423,6 @@
 	end
 	return VecLerp(mi, ma, 0.5)
 end
-
-
 
 function handleCommand(cmd)
 	words = splitString(cmd, " ")
@@ -2219,3 +1449,462 @@
 	end
 end
 
+function server.init()
+    configInit()
+    robotInit()
+    hoverInit()
+    headInit()
+    sensorInit()
+    wheelsInit()
+    feetInit()
+    aimsInit()
+    weaponsInit()
+    navigationInit()
+    hearingInit()
+    stackInit()
+    patrolLocations = FindLocations("patrol")
+    local nomDist = 7.0
+end
+
+function server.tick(dt)
+    for _, playerId in ipairs(GetAllPlayers()) do
+        if not robot.enabled then
+        	return
+        end
+        if HasTag(robot.body, "turnhostile") then
+        	RemoveTag(robot.body, "turnhostile")
+        	config.canHearPlayer = true
+        	config.canSeePlayer = true
+        	config.huntPlayer = true
+        	config.aggressive = true
+        	config.practice = false
+        end
+        --Outline
+        local dist = VecDist(robot.bodyCenter, GetPlayerCameraTransform(playerId).pos)
+        if dist < config.outline then
+        	local a = clamp((config.outline - dist) / 5.0, 0.0, 1.0)
+        	if canBeSeenByPlayer() then
+        		a = 0
+        	end
+        	robot.outlineAlpha = robot.outlineAlpha + clamp(a - robot.outlineAlpha, -0.1, 0.1)
+        	for i=1, #robot.allBodies do
+        		DrawBodyOutline(robot.allBodies[i], 1, 1, 1, robot.outlineAlpha*0.5)
+        	end
+        end
+        --Remove planks and wires after some time
+        local tags = {"plank", "wire"}
+        local removeTimeOut = 10
+        for i=1, #robot.allShapes do
+        	local shape = robot.allShapes[i]
+        	local joints = GetShapeJoints(shape)
+        	for j=1, #joints do
+        		local joint = joints[j]
+        		for t=1, #tags do
+        			local tag = tags[t]
+        			if HasTag(joint, tag) then
+        				local t = tonumber(GetTagValue(joint, tag)) or 0
+        				t = t + dt
+        				if t > removeTimeOut then
+        					if GetJointType(joint) == "rope" then
+        						DetachJointFromShape(joint, shape)
+        					else
+        						Delete(joint)
+        					end
+        					break
+        				else
+        					SetTag(joint, tag, t)
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
+        if robot.deleted then 
+        	return
+        else 
+        	if not IsHandleValid(robot.body) then
+        		for i=1, #robot.allBodies do
+        			Delete(robot.allBodies[i])
+        		end
+        		for i=1, #robot.allJoints do
+        			Delete(robot.allJoints[i])
+        		end
+        		robot.deleted = true
+        	end
+        end
+        if robot.activateTrigger ~= 0 then 
+        	if IsPointInTrigger(robot.activateTrigger, GetPlayerCameraTransform(playerId).pos) then
+        		RemoveTag(robot.body, "inactive")
+        		robot.activateTrigger = 0
+        	end
+        end
+        if HasTag(robot.body, "inactive") then
+        	robot.inactive = true
+        	return
+        else
+        	if robot.inactive then
+        		robot.inactive = false
+        		--Reset robot pose
+        		local sleep = HasTag(robot.body, "sleeping")
+        		for i=1, #robot.allBodies do
+        			SetBodyTransform(robot.allBodies[i], robot.initialBodyTransforms[i])
+        			SetBodyVelocity(robot.allBodies[i], Vec(0,0,0))
+        			SetBodyAngularVelocity(robot.allBodies[i], Vec(0,0,0))
+        			if sleep then
+        				--If robot is sleeping make sure to not wake it up
+        				SetBodyActive(robot.allBodies[i], false)
+        			end
+        		end
+        	end
+        end
+        if HasTag(robot.body, "sleeping") then
+        	if IsBodyActive(robot.body) then
+        		wakeUp = true
+        	end
+        	local vol, pos = GetLastSound()
+        	if vol > 0.2 then
+        		if robot.investigateTrigger == 0 or IsPointInTrigger(robot.investigateTrigger, pos) then
+        			wakeUp = true
+        		end
+        	end	
+        	if wakeUp then
+        		RemoveTag(robot.body, "sleeping")
+        	end
+        	return
+        end
+        robotUpdate(dt)
+        wheelsUpdate(dt)
+        if not robot.enabled then
+        	return
+        end
+        feetUpdate(dt)
+        robot.stunned = clamp(robot.stunned - dt, 0.0, 6.0)
+        if robot.stunned ~= 0 then
+        	head.seenTimer = 0
+        	weaponsReset()
+        	return
+        end
+        hoverUpdate(dt)
+        headUpdate(dt)
+        sensorUpdate(dt)
+        aimsUpdate(dt)
+        weaponsUpdate(dt)
+        hearingUpdate(dt)
+        stackUpdate(dt)
+        robot.speedScale = 1
+        robot.speed = 0
+        local state = stackTop()
+        if state.id == "none" then
+        	if config.patrol then
+        		stackPush("patrol")
+        	else
+        		stackPush("roam")
+        	end
+        end
+        if state.id == "roam" then
+        	if not state.nextAction then
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		local randomPos
+        		if robot.roamTrigger ~= 0 then
+        			randomPos = getRandomPosInTrigger(robot.roamTrigger)
+        			randomPos = truncateToGround(randomPos)
+        		else
+        			local rndAng = rnd(0, 2*math.pi)
+        			randomPos = VecAdd(robot.transform.pos, Vec(math.cos(rndAng)*6.0, 0, math.sin(rndAng)*6.0))
+        		end
+        		local s = stackPush("navigate")
+        		s.timeout = 1
+        		s.pos = randomPos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "patrol" then
+        	if not state.nextAction then
+        		state.index = getClosestPatrolIndex()
+        		state.nextAction = "move"
+        	elseif state.nextAction == "move" then
+        		markPatrolLocationAsActive(state.index)
+        		local nav = stackPush("navigate")
+        		nav.pos = GetLocationTransform(patrolLocations[state.index]).pos
+        		state.nextAction = "search"
+        	elseif state.nextAction == "search" then
+        		stackPush("search")
+        		state.index = getNextPatrolIndex(state.index)
+        		state.nextAction = "move"
+        	end
+        end
+        if state.id == "search" then
+        	if state.activeTime > 2.5 then
+        		if not state.turn then
+        			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+        			state.turn = true
+        		end
+        		if state.activeTime > 6.0 then
+        			stackPop()
+        		end
+        	end
+        	if state.activeTime < 1.5 or state.activeTime > 3 and state.activeTime < 4.5 then
+        		head.dir = TransformToParentVec(robot.transform, Vec(-5, 0, -1))
+        	else
+        		head.dir = TransformToParentVec(robot.transform, Vec(5, 0, -1))
+        	end
+        end
+        if state.id == "move" then
+        	robotTurnTowards(state.pos)
+        	robot.speed = config.speed
+        	head.dir = VecCopy(robot.dir)
+        	local d = VecLength(VecSub(state.pos, robot.transform.pos))
+        	if d < 2 then
+        		robot.speed = 0
+        		stackPop()
+        	else
+        		if robot.blocked > 0.5 then
+        			stackPush("unblock")
+        		end
+        	end
+        end
+        if state.id == "unblock" then
+        	if not state.dir then
+        		if math.random(0, 10) < 5 then
+        			state.dir = TransformToParentVec(robot.transform, Vec(-1, 0, -1))
+        		else
+        			state.dir = TransformToParentVec(robot.transform, Vec(1, 0, -1))
+        		end
+        		state.dir = VecNormalize(state.dir)
+        	else
+        		robot.dir = state.dir
+        		robot.speed = -math.min(config.speed, 2.0)
+        		if state.activeTime > 1 then
+        			stackPop()
+        		end
+        	end
+        end
+        --Hunt player
+        if state.id == "hunt" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+        	if robot.distToPlayer < 4.0 then
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        		head.dir = VecCopy(robot.dirToPlayer)
+        		robot.speed = 0
+        		navigationClear()
+        	else
+        		navigationSetTarget(head.lastSeenPos, 1.0 + clamp(head.timeSinceLastSeen, 0.0, 4.0))
+        		robot.speedScale = config.huntSpeedScale
+        		navigationUpdate(dt)
+        		if head.canSeePlayer then
+        			head.dir = VecCopy(robot.dirToPlayer)
+        			state.headAngle = 0
+        			state.headAngleTimer = 0
+        		else
+        			state.headAngleTimer = state.headAngleTimer + dt
+        			if state.headAngleTimer > 1.0 then
+        				if state.headAngle > 0.0 then
+        					state.headAngle = rnd(-1.0, -0.5)
+        				elseif state.headAngle < 0 then
+        					state.headAngle = rnd(0.5, 1.0)
+        				else
+        					state.headAngle = rnd(-1.0, 1.0)
+        				end
+        				state.headAngleTimer = 0
+        			end
+        			head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        		end
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen < 2 then
+        		--Turn towards player if not moving
+        		robot.dir = VecCopy(robot.dirToPlayer)
+        	end
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 and VecLength(GetBodyVelocity(robot.body)) < 1 then
+        		if VecDist(head.lastSeenPos, robot.bodyCenter) > 3.0 then
+        			stackClear()
+        			local s = stackPush("investigate")
+        			s.pos = VecCopy(head.lastSeenPos)		
+        		else
+        			stackClear()
+        			stackPush("huntlost")
+        		end
+        	end
+        end
+        --Avoid player
+        if state.id == "avoid" then
+        	if not state.init then
+        		navigationClear()
+        		state.init = true
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	end
+
+        	local distantPatrolIndex = getDistantPatrolIndex(GetPlayerTransform(playerId).pos)
+        	local avoidTarget = GetLocationTransform(patrolLocations[distantPatrolIndex]).pos
+        	navigationSetTarget(avoidTarget, 1.0)
+        	robot.speedScale = config.huntSpeedScale
+        	navigationUpdate(dt)
+        	if head.canSeePlayer then
+        		head.dir = VecNormalize(VecSub(head.lastSeenPos, robot.transform.pos))
+        		state.headAngle = 0
+        		state.headAngleTimer = 0
+        	else
+        		state.headAngleTimer = state.headAngleTimer + dt
+        		if state.headAngleTimer > 1.0 then
+        			if state.headAngle > 0.0 then
+        				state.headAngle = rnd(-1.0, -0.5)
+        			elseif state.headAngle < 0 then
+        				state.headAngle = rnd(0.5, 1.0)
+        			else
+        				state.headAngle = rnd(-1.0, 1.0)
+        			end
+        			state.headAngleTimer = 0
+        		end
+        		head.dir = QuatRotateVec(QuatEuler(0, state.headAngle, 0), robot.dir)
+        	end
+
+        	if navigation.state ~= "move" and head.timeSinceLastSeen > 2 and state.activeTime > 3.0 then
+        		stackClear()
+        	end
+        end
+        --Get up player
+        if state.id == "getup" then
+        	if not state.time then 
+        		state.time = 0 
+        	end
+        	state.time = state.time + dt
+        	hover.timeSinceContact = 0
+        	if state.time > 2.0 then
+        		stackPop()
+        	else
+        		hoverGetUp()
+        	end
+        end
+    end
+end
+
+function client.init()
+    shootSound = LoadSound("tools/gun0.ogg", 8.0)
+    rocketSound = LoadSound("tools/launcher0.ogg", 7.0)
+    if config.stepSound == "s" then nomDist = 5.0 end
+    if config.stepSound == "l" then nomDist = 9.0 end
+    stepSound = LoadSound("robot/step-" .. config.stepSound .. "0.ogg", nomDist)
+    headLoop = LoadLoop("robot/head-loop.ogg", 7.0)
+    turnLoop = LoadLoop("robot/turn-loop.ogg", 7.0)
+    walkLoop = LoadLoop("robot/walk-loop.ogg", 7.0)
+    rollLoop = LoadLoop("robot/roll-loop.ogg", 7.0)
+    chargeLoop = LoadLoop("robot/charge-loop.ogg", 8.0)
+    alertSound = LoadSound("robot/alert.ogg", 9.0)
+    huntSound = LoadSound("robot/hunt.ogg", 9.0)
+    idleSound = LoadSound("robot/idle.ogg", 9.0)
+    fireLoop = LoadLoop("tools/blowtorch-loop.ogg")
+    disableSound = LoadSound("robot/disable0.ogg")
+end
+
+function client.update(dt)
+    local playerId = GetLocalPlayer()
+    if IsPointInWater(robot.bodyCenter) then
+    	PlaySound(disableSound, robot.bodyCenter, 1.0, false)
+    	for i=1, #robot.allShapes do
+    		SetShapeEmissiveScale(robot.allShapes[i], 0)
+    	end
+    	SetTag(robot.body, "disabled")
+    	robot.enabled = false
+    end
+    if state.id == "investigate" then
+    	if not state.nextAction then
+    		local pos = state.pos
+    		robotTurnTowards(state.pos)
+    		headTurnTowards(state.pos)
+    		local nav = stackPush("navigate")
+    		nav.pos = state.pos
+    		nav.timeout = 5.0
+    		state.nextAction = "search"
+    	elseif state.nextAction == "search" then
+    		stackPush("search")
+    		state.nextAction = "done"
+    	elseif state.nextAction == "done" then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	end	
+    end
+    if state.id == "huntlost" then
+    	if not state.timer then
+    		state.timer = 6
+    		state.turnTimer = 1
+    	end
+    	state.timer = state.timer - dt
+    	head.dir = VecCopy(robot.dir)
+    	if state.timer < 0 then
+    		PlaySound(idleSound, robot.bodyCenter, 1.0, false)
+    		stackPop()
+    	else
+    		state.turnTimer = state.turnTimer - dt
+    		if state.turnTimer < 0 then
+    			robotSetDirAngle(robotGetDirAngle() + math.random(2, 4))
+    			state.turnTimer = rnd(0.5, 1.5)
+    		end
+    	end
+    end
+    if state.id == "navigate" then
+    	if not state.initialized then
+    		if not state.timeout then state.timeout = 30 end
+    		navigationClear()
+    		navigationSetTarget(state.pos, state.timeout)
+    		state.initialized = true
+    	else
+    		head.dir = VecCopy(robot.dir)
+    		navigationUpdate(dt)
+    		if navigation.state == "done" or navigation.state == "fail" then
+    			stackPop()
+    		end
+    	end
+    end
+
+    --React to sound
+    if not stackHas("hunt") then
+    	if hearing.hasNewSound and hearing.timeSinceLastSound < 1.0 then
+    		stackClear()
+    		PlaySound(alertSound, robot.bodyCenter, 1.0, false)
+    		local s = stackPush("investigate")
+    		s.pos = hearing.lastSoundPos	
+    		hearingConsumeSound()
+    	end
+    end
+
+    --Seen player
+    if config.huntPlayer and not stackHas("hunt") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.canSensePlayer then
+    		stackClear()
+    		PlaySound(huntSound, robot.bodyCenter, 1.0, false)
+    		stackPush("hunt")
+    	end
+    end
+
+    --Seen player
+    if config.avoidPlayer and not stackHas("avoid") then
+    	if config.canSeePlayer and head.canSeePlayer or robot.distToPlayer < 2.0 then
+    		stackClear()
+    		stackPush("avoid")
+    	end
+    end
+
+    --Get up
+    if hover.timeSinceContact > 3.0 and not stackHas("getup") then
+    	stackPush("getup")
+    end
+
+    if IsShapeBroken(GetLightShape(head.eye)) then
+    	config.hasVision = false
+    	config.canSeePlayer = false
+    end
+end
+

```
