# Migration Report: main.lua

## Changes Applied
- Added `#version 2` header
- Split callbacks into `server.*` / `client.*` domains
- Applied automatic fixups (handle checks, deprecated functions, playerId)

## Diff

```diff
--- original/main.lua
+++ patched/main.lua
@@ -1,3 +1,4 @@
+#version 2
 local menu_key = 'q'
 local favorite_tools_reg = 'savegame.mod.favorites'
 local activate_key_reg = 'savegame.mod.activate_key'
@@ -24,20 +25,6 @@
     'explosive'
 }
 
-function init()
-    menu_open = false
-    menu_opened_before = false
-    all_tools = {}
-    tool_instance = {}
-
-    recent_menu_height = 100
-    scroll_pos = 0
-    
-    if HasKey(activate_key_reg) then
-        menu_key = GetString(activate_key_reg)
-    end
-end
-
 function get_tool_key(tool_id, k)
     local result = string.format('game.tool.%s.%s', tool_id, k)
     return GetString(result)
@@ -103,7 +90,7 @@
 
     -- save to perst.
     local fav_string = table.concat(favorite_ids, ",")
-    SetString(favorite_tools_reg, fav_string)
+    SetString(favorite_tools_reg, fav_string, true)
 end
 
 function load_favorite_tools()
@@ -117,84 +104,6 @@
         if table_contains(tool_ids, tool.id) then
 			all_tools[i].favorite = true
 		end
-    end
-end
-
-function tick(dt)
-
-    -- scrolling
-    if menu_open then
-
-        local new_scroll_pos = scroll_pos + InputValue("mousewheel") * scroll_sensitivity
-        local diff_height = recent_menu_height - UiHeight() + menu_padding * 2
-
-        -- prevent scrolling up
-        if new_scroll_pos > 0 then
-            new_scroll_pos = 0
-        end
-
-        -- prevent scrolling if menu to small
-        if diff_height < 0 then
-            new_scroll_pos = 0
-
-        -- prevent scrolling past the end
-        elseif new_scroll_pos < -diff_height then
-            new_scroll_pos = -diff_height
-        end
-
-        -- update scroll variable
-        scroll_pos = new_scroll_pos
-    end
-
-    -- toggle menu
-    if InputPressed(menu_key) then
-
-        -- when the menu is opened for the first time
-        if not menu_opened_before then
-            generate_all_tools()
-            load_favorite_tools()
-            menu_opened_before = true
-        end
-
-        -- on menu open
-        if not menu_open then
-            generate_tool_instance()
-            update_tool_data()
-            scroll_pos = 0
-        end
-
-        -- on menu close
-        if menu_open then
-            save_favorite_tools()
-        end
-
-        -- toggle menu open
-        menu_open = not menu_open
-    end
-end
-
-function draw()
-    if menu_open then
-
-        -- allow clicking on menu
-        UiMakeInteractive()
-
-        -- blurred underlay
-        UiPush()
-            UiColor(0, 0, 0, 0.2)
-            UiBlur(0.5)
-            UiRect(UiWidth(), UiHeight())
-        UiPop()
-        
-        -- safe margins
-        local x0, y0, x1, y1 = UiSafeMargins()
-        UiTranslate(x0, y0)
-        UiWindow(x1-x0, y1-y0, true)
-
-        -- scrolling
-        UiTranslate(0, scroll_pos)
-
-        draw_tool_menu()
     end
 end
 
@@ -337,7 +246,7 @@
 end
 
 function set_tool_enabled(tool, state)
-    SetBool(string.format('game.tool.%s.enabled', tool.id), state)
+    SetBool(string.format('game.tool.%s.enabled', tool.id), state, true)
     tool.enabled = state
 end
 
@@ -380,7 +289,7 @@
             UiAlign("center middle")
             UiTranslate(UiWidth() / 2, UiHeight() / 2)
             if UiTextButton(tool.name) then
-                SetString("game.player.tool", tool.id)
+                SetString("game.player.tool", tool.id, true)
                 menu_open = false
                 set_tool_enabled(tool, true)
                 save_favorite_tools()
@@ -401,3 +310,94 @@
         end
     UiPop()
 end
+
+function server.init()
+    menu_open = false
+    menu_opened_before = false
+    all_tools = {}
+    tool_instance = {}
+    recent_menu_height = 100
+    scroll_pos = 0
+    if HasKey(activate_key_reg) then
+        menu_key = GetString(activate_key_reg)
+    end
+end
+
+function server.tick(dt)
+    -- toggle menu
+end
+
+function client.tick(dt)
+    if menu_open then
+
+        local new_scroll_pos = scroll_pos + InputValue("mousewheel") * scroll_sensitivity
+        local diff_height = recent_menu_height - UiHeight() + menu_padding * 2
+
+        -- prevent scrolling up
+        if new_scroll_pos ~= 0 then
+            new_scroll_pos = 0
+        end
+
+        -- prevent scrolling if menu to small
+        if diff_height < 0 then
+            new_scroll_pos = 0
+
+        -- prevent scrolling past the end
+        elseif new_scroll_pos < -diff_height then
+            new_scroll_pos = -diff_height
+        end
+
+        -- update scroll variable
+        scroll_pos = new_scroll_pos
+    end
+    if InputPressed(menu_key) then
+
+        -- when the menu is opened for the first time
+        if not menu_opened_before then
+            generate_all_tools()
+            load_favorite_tools()
+            menu_opened_before = true
+        end
+
+        -- on menu open
+        if not menu_open then
+            generate_tool_instance()
+            update_tool_data()
+            scroll_pos = 0
+        end
+
+        -- on menu close
+        if menu_open then
+            save_favorite_tools()
+        end
+
+        -- toggle menu open
+        menu_open = not menu_open
+    end
+end
+
+function client.draw()
+    if menu_open then
+
+        -- allow clicking on menu
+        UiMakeInteractive()
+
+        -- blurred underlay
+        UiPush()
+            UiColor(0, 0, 0, 0.2)
+            UiBlur(0.5)
+            UiRect(UiWidth(), UiHeight())
+        UiPop()
+
+        -- safe margins
+        local x0, y0, x1, y1 = UiSafeMargins()
+        UiTranslate(x0, y0)
+        UiWindow(x1-x0, y1-y0, true)
+
+        -- scrolling
+        UiTranslate(0, scroll_pos)
+
+        draw_tool_menu()
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
@@ -1,54 +1,56 @@
+#version 2
 local activate_key_reg = 'savegame.mod.activate_key'
 
-function draw()
-	UiTranslate(UiCenter(), 250)
-	UiAlign("center middle")
+function client.draw()
+    UiTranslate(UiCenter(), 250)
+    UiAlign("center middle")
 
-	--Title
-	UiFont("bold.ttf", 48)
-	UiText("Tool menu")
+    --Title
+    UiFont("bold.ttf", 48)
+    UiText("Tool menu")
 
-	--Keyboard instructions
-	UiFont("regular.ttf", 26)
-	UiTranslate(0, 70)
-	UiPush()
-		UiText("Keyboard Layout")
-		UiTranslate(0, 20)
-		UiFont("regular.ttf", 20)
-		UiText("Defines which key is used to make the menu appearing.")
-		UiTranslate(0, 20)
-		UiText("QWERTY will set the key to 'q'. AZERTY will set the key to 'a'.")
-	UiPop()
+    --Keyboard instructions
+    UiFont("regular.ttf", 26)
+    UiTranslate(0, 70)
+    UiPush()
+    	UiText("Keyboard Layout")
+    	UiTranslate(0, 20)
+    	UiFont("regular.ttf", 20)
+    	UiText("Defines which key is used to make the menu appearing.")
+    	UiTranslate(0, 20)
+    	UiText("QWERTY will set the key to 'q'. AZERTY will set the key to 'a'.")
+    UiPop()
 
-    --Buttons
-	UiTranslate(0, 80)
-	UiFont("regular.ttf", 26)
-	UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
-	UiPush()
-		UiTranslate(-110, 0)
-		if GetString(activate_key_reg) == "q" then
-			UiPush()
-				UiColor(0.5, 1, 0.5, 0.2)
-				UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
-			UiPop()
-		end
-		if UiTextButton("QWERTY Keyboard", 200, 40) then
-			SetString(activate_key_reg, "q")
-		end
-		UiTranslate(220, 0)
-		if GetString(activate_key_reg) == "a" then
-			UiPush()
-				UiColor(0.5, 1, 0.5, 0.2)
-				UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
-			UiPop()
-		end
-		if UiTextButton("AZERTY Keyboard", 200, 40) then
-			SetString(activate_key_reg, "a")
-		end
-	UiPop()
-	
-	UiTranslate(0, 100)
-	if UiTextButton("Close", 200, 40) then
-		Menu()
-	end
-end+       --Buttons
+    UiTranslate(0, 80)
+    UiFont("regular.ttf", 26)
+    UiButtonImageBox("ui/common/box-outline-6.png", 6, 6)
+    UiPush()
+    	UiTranslate(-110, 0)
+    	if GetString(activate_key_reg) == "q" then
+    		UiPush()
+    			UiColor(0.5, 1, 0.5, 0.2)
+    			UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
+    		UiPop()
+    	end
+    	if UiTextButton("QWERTY Keyboard", 200, 40) then
+    		SetString(activate_key_reg, "q", true)
+    	end
+    	UiTranslate(220, 0)
+    	if GetString(activate_key_reg) == "a" then
+    		UiPush()
+    			UiColor(0.5, 1, 0.5, 0.2)
+    			UiImageBox("ui/common/box-solid-6.png", 200, 40, 6, 6)
+    		UiPop()
+    	end
+    	if UiTextButton("AZERTY Keyboard", 200, 40) then
+    		SetString(activate_key_reg, "a", true)
+    	end
+    UiPop()
+
+    UiTranslate(0, 100)
+    if UiTextButton("Close", 200, 40) then
+    	Menu()
+    end
+end
+

```
