# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,52 +1,13 @@
+#version 2
 local math_random = math.random
 local math_min = math.min
 local math_max = math.max
-
 local projectiles = {}
 local proj_counter = 1
 local gravity = Vec(0, -4.0, 0)
 local ready = 0
 
-function init()
-	RegisterTool("M2A1_flamethrower", "M2A1 Flamethrower", "MOD/flm.xml")
-	SetBool("game.tool.M2A1_flamethrower.enabled", true)
-	SetFloat("game.tool.M2A1_flamethrower.ammo", 60)
-
-	torch_sound = LoadLoop("tools/blowtorch-loop.ogg")
-	spray_sound = LoadLoop("tools/spray-loop.ogg")
-end
-
-function tick(dt)
-	update_napalm_physics(dt)
-	render_realistic_fx()
-
-	if GetString("game.player.tool") == "M2A1_flamethrower" then
-		local b = GetToolBody()
-		if b == 0 then return end
-
-		local ammo = GetFloat("game.tool.M2A1_flamethrower.ammo")
-		local firing = GetBool("game.player.canusetool") and InputDown("usetool") and ammo > 0
-
-		if firing then
-			if ready < 1.0 then PlayLoop(spray_sound) end
-			ready = math_min(1.0, ready + dt * 4)
-			if ready == 1.0 then
-				PlayLoop(torch_sound)
-				ammo = math_max(0, ammo - dt)
-				SetFloat("game.tool.M2A1_flamethrower.ammo", ammo)
-				spawn_napalm_stream(b)
-			end
-		else
-			ready = math_max(0.0, ready - dt * 4)
-		end
-		
-		SetToolTransform(Transform(Vec(0.35, -0.35, -0.90), QuatEuler(0, 0, 0)))
-	end
-end
-
--- Вспомогательная функция для создания капли
-function create_p(pos, vel, life)
-	local p = {
+al p = {
 		pos = pos,
 		vel = vel,
 		maxLife = life,
@@ -59,7 +20,9 @@
 end
 
 function spawn_napalm_stream(body)
-	local ct = GetCameraTransform()
+	local ct = GetCa
+
+raTransform()
 	local forwardDir = TransformToParentVec(ct, Vec(0, 0, -1.2))
 	local bodyTrans = GetBodyTransform(body)
 	local localOffset = Vec(0.05, 0.1, -0.4) 
@@ -70,7 +33,9 @@
 end
 
 function update_napalm_physics(dt)
-	for k, p in pairs(projectiles) do
+	for k, p in pair
+
+projectiles) do
 		if p.stuck then
 			p.stuckTime = p.stuckTime + dt
 			p.pos = VecAdd(p.pos, Vec(0, -0.003, 0)) -- Медленное стекание
@@ -118,7 +83,7 @@
 	ParticleType("smoke")
 	ParticleColor(1, 0.5, 0.1, 0.8, 0.2, 0)
 	ParticleGravity(2)
-	ParticleEmissive(6, 0)
+	ParticleEmissive(6, 
 
 	for _, p in pairs(projectiles) do
 		local lifeRatio = math_max(0.1, p.life / p.maxLife)
@@ -155,4 +120,43 @@
 			PointLight(p.pos, 0.8 * intensity, 0.3 * intensity, 0.1 * intensity, 0.5)
 		end
 	end
-end+end
+
+function server.init()
+    RegisterTool("M2A1_flamethrower", "M2A1 Flamethrower", "MOD/flm.xml")
+    SetBool("game.tool.M2A1_flamethrower.enabled", true, true)
+    SetFloat("game.tool.M2A1_flamethrower.ammo", 60, true)
+    torch_sound = LoadLoop("tools/blowtorch-loop.ogg")
+    spray_sound = LoadLoop("tools/spray-loop.ogg")
+end
+
+function server.tick(dt)
+    update_napalm_physics(dt)
+    render_realistic_fx()
+end
+
+function client.tick(dt)
+    if GetString("game.player.tool") == "M2A1_flamethrower" then
+    	local b = GetToolBody()
+    	if b == 0 then return end
+
+    	local ammo = GetFloat("game.tool.M2A1_flamethrower.ammo")
+    	local firing = GetBool("game.player.canusetool") and InputDown("usetool") and ammo > 0
+
+    	if firing then
+    		if ready < 1.0 then PlayLoop(spray_sound) end
+    		ready = math_min(1.0, ready + dt * 4)
+    		if ready == 1.0 then
+    			PlayLoop(torch_sound)
+    			ammo = math_max(0, ammo - dt)
+    			SetFloat("game.tool.M2A1_flamethrower.ammo", ammo, true)
+    			spawn_napalm_stream(b)
+    		end
+    	else
+    		ready = math_max(0.0, ready - dt * 4)
+    	end
+
+    	SetToolTransform(Transform(Vec(0.35, -0.35, -0.90), QuatEuler(0, 0, 0)))
+    end
+end
+

```
