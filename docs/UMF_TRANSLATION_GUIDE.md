# UMF → V2 Translation Guide

> **Purpose:** Practical translation rules for converting Geneosis-style UMF mods to standalone v2.
> These mods share a common framework: `registry.lua`, `umf.lua`, `ui.lua`, `tool.lua`, `utility.lua`.
>
> **Analyzed mods:** Omni Gun (2994616319), Blight Gun (3004952393), BHL-X42 (2721596235), Magnets (2783125614)
>
> **Created:** 2026-03-19 by API Surgeon
>
> **Results:** 14 UMF mods converted via bypass strategy (#162-#177). 5 UMF mods deferred (too complex). Guide proved viable for all attempted conversions.

---

## Registry Layer (registry.lua)

The UMF registry is a thin wrapper around `savegame.mod.*` keys. Drop-in replacement:

| UMF Function | V2 Equivalent |
|---|---|
| `regGetFloat(path)` | `GetFloat("savegame.mod." .. path)` |
| `regSetFloat(path, value)` | `SetFloat("savegame.mod." .. path, value)` |
| `regGetInt(path)` | `GetInt("savegame.mod." .. path)` |
| `regSetInt(path, value)` | `SetInt("savegame.mod." .. path, value)` |
| `regGetBool(path)` | `GetBool("savegame.mod." .. path)` |
| `regSetBool(path, value)` | `SetBool("savegame.mod." .. path, value)` |
| `regGetString(path)` | `GetString("savegame.mod." .. path)` |
| `regSetString(path, value)` | `SetString("savegame.mod." .. path, value)` |
| `regListKeys(path)` | `ListKeys("savegame.mod." .. path)` |
| `regClearKey(path)` | `ClearKey("savegame.mod." .. path)` |
| `regHasKey(path)` | `HasKey("savegame.mod." .. path)` |

**Soft reset pattern:** `regInitKey(path, key)` sets a default only if key doesn't exist:
```lua
-- UMF
regInitKey('key.shoot', "lmb")

-- V2
local REG = "savegame.mod."
if not HasKey(REG .. "key.shoot") then
    SetString(REG .. "key.shoot", "lmb")
end
```

**Version check + reset:** `checkRegInitialized()` compares saved version → resets on major version change. In v2, use `getOptions()` pattern or `server.init()` one-time setup.

---

## Tool Layer (tool.lua)

| UMF Pattern | V2 Equivalent |
|---|---|
| `RegisterTool(name, title, voxPath)` | `RegisterTool(name, title, voxPath, group)` — add group number |
| `SetBool('game.tool.'..name..'.enabled', true)` | `SetToolEnabled(name, true, p)` — per-player, server only |
| `GetString('game.player.tool') == name` | `GetPlayerTool(p) == name` — per-player |
| `GetPlayerVehicle() == 0` | `GetPlayerVehicle(p) == 0` — add player param |
| `GetToolBody()` | `GetToolBody(p)` — add player param |
| `SetToolTransform(offset)` | `SetToolTransform(offset, 1.0, p)` — add sway + player |
| `SetToolOffset(vec)` | `SetToolOffset(vec, p)` — add player param |
| `SetToolHandPoseLocalTransform(right, nil)` | `SetToolHandPoseLocalTransform(right, left, p)` — add player |
| `GetCameraTransform()` | `GetPlayerCameraTransform(p)` or `GetPlayerEyeTransform(p)` |
| `GetPlayerTransform()` | `GetPlayerTransform(p)` — add player param |

**Tool activation:** In v2, do `SetToolEnabled` + `SetToolAmmo` in `PlayersAdded` loop:
```lua
-- UMF (server.init, one-time)
RegisterTool(name, title, voxPath)
SetBool('game.tool.'..name..'.enabled', true)

-- V2 (server.init + server.tick)
function server.init()
    RegisterTool(TOOL_ID, "Tool Name", "MOD/vox/tool.vox", 1)
    SetToolAmmoPickupAmount(TOOL_ID, 0)
    SetString("game.tool." .. TOOL_ID .. ".ammo.display", "")
end

function server.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled(TOOL_ID, true, p)
        SetToolAmmo(TOOL_ID, 101, p)
    end
    for p in PlayersRemoved() do
        players[p] = nil
    end
end
```

---

## Input Layer

| UMF Pattern | V2 Equivalent |
|---|---|
| `InputDown(regGetString('key.shoot'))` | Client-local only: `if IsPlayerLocal(p) and InputDown(regGetString("savegame.mod.key.shoot")) then ServerCall("server.onShoot", p, ...) end` |
| `InputPressed(regGetString('key.options'))` | Same local-only pattern: `if IsPlayerLocal(p) and InputPressed(GetString("savegame.mod.key.options")) then` |
| `InputDown("usetool")` | Works with player param: `InputDown("usetool", p)` — no change needed for action names |

**Critical rule:** Raw key names (`"lmb"`, `"rmb"`, `"r"`, `"o"`, etc.) do NOT work with player param. Always use the `IsPlayerLocal(p)` + `ServerCall` pattern for raw keys in MP.

---

## UI Layer (ui.lua)

### Options Menu

UMF uses a custom UI framework with `ui.container`, `ui.padding`, `ui.slider`, `ui.checkBox`, `ui.keyBinding`. In v2, replace with standard Teardown UI:

```lua
-- UMF options pattern
function draw()
    if UI_GAME then
        UiMakeInteractive()
        uiDrawOptions()  -- custom framework
    end
end

-- V2 options pattern
function client.draw()
    local p = GetLocalPlayer()
    if not p then return end
    local data = clientData[p]
    if not data then return end
    if GetPlayerTool(p) ~= TOOL_ID then return end

    if data.optionsOpen then
        UiMakeInteractive()
        UiPush()
            -- Standard v2 options layout
            UiTranslate(60, UiHeight() / 2 - 200)
            UiAlign("left top")
            UiColor(0, 0, 0, 0.85)
            UiImageBox("ui/common/box-solid-shadow-50.png", 380, 400, 6, 6)
            UiTranslate(20, 20)
            UiFont("bold.ttf", 28)
            UiColor(1, 1, 1)
            UiText("Options")
            -- ... sliders, toggles, close button ...
        UiPop()
        return
    end
end
```

### UI Widget Translation

| UMF Widget | V2 Equivalent |
|---|---|
| `ui.slider.create(title, regPath, unit, min, max)` | `UiSlider(...)` + `GetFloat/SetFloat("savegame.mod." .. path)` |
| `ui.checkBox.create(title, regPath)` | `UiTextButton("Toggle: " .. title)` + `GetBool/SetBool` toggle |
| `ui.keyBinding.create(title, regPath)` | Custom keybind widget using `InputLastPressedKey()` + `SetString` |
| `ui.colorPicker.create(title, regPath)` | Three sliders (R/G/B) or simplified color picker |
| `ui.lineEdit.create(title, regPath)` | Custom text input (rare, can simplify or remove) |
| `ui.container.create(w, h, color, alpha)` | `UiColor(r, g, b, a); UiRect(w, h)` |
| `ui.padding.create(w, h)` | `UiTranslate(w, h)` |

### Keybind Hints

```lua
-- UMF
function uiDrawKeyHint()
    UiText('[' .. string.upper(regGetString('key.shoot')) .. ']: Shoot')
end

-- V2
UiPush()
    UiTranslate(10, UiHeight() - 80)
    UiAlign("left bottom")
    UiColor(1, 1, 1, 0.8)
    UiFont("bold.ttf", 20)
    UiTextOutline(0, 0, 0, 1, 0.1)
    local shoot = string.upper(GetString("savegame.mod.key.shoot"))
    UiText("[" .. shoot .. "] Shoot\n[O] Options")
UiPop()
```

---

## UMF Framework (umf.lua) — What to Drop

| UMF Feature | V2 Status |
|---|---|
| `UpdateQuickloadPatch()` | **DROP** — v2 engine handles quickload |
| `IsPlayerInVehicle()` | Replace with `GetPlayerVehicle(p) ~= 0` |
| OOP entity wrappers (`Body()`, `Shape()`, etc.) | **DROP** — use raw Teardown API handles |
| `Quaternion()`, `Vector()`, `Transformation()` classes | **DROP** — use `Quat()`, `Vec()`, `Transform()` |
| `constraint.*` physics solver | **DROP** unless mod needs custom constraints (rare) |
| `Armature()` animation system | **DROP** unless mod uses skeletal animation |
| `RegisterToolUMF()` | Replace with `RegisterTool()` in `server.init()` |
| `OptionsMenu.*` components | Replace with standard v2 UI (see UI section) |
| `hook.add/run/remove` event system | Replace with direct function calls in v2 callbacks |
| `timer.*` system | Replace with `data.timer = data.timer - dt` pattern |
| `util.shared_buffer()` | Replace with per-player `data.*` table |

---

## Server/Client Split

UMF mods use plain `init()`, `tick()`, `draw()`. In v2 MP, split into server/client:

| UMF Callback | V2 Server | V2 Client |
|---|---|---|
| `init()` | `server.init()` — RegisterTool, options defaults | `client.init()` — load sounds/sprites |
| `tick()` | `server.tick(dt)` — game logic, damage, spawning | `client.tick(dt)` — visuals, input, animations |
| `draw()` | *(none)* | `client.draw()` — HUD, options menu, keybind hints |

**Key principle:** Physics, damage, spawning, deletion → `server.*`. Visuals, sounds, UI, input reading → `client.*`. The host runs both.

---

## Conversion Checklist

1. [ ] Add `#version 2` + `#include "script/include/player.lua"`
2. [ ] Replace all `reg*()` calls with direct `savegame.mod.*` registry calls
3. [ ] Split `init/tick/draw` into `server.*/client.*` callbacks
4. [ ] Add `players = {}` + `createPlayerData()` + `PlayersAdded/Removed` loops
5. [ ] Add player param to all Get/Set functions (`GetToolBody(p)`, etc.)
6. [ ] Replace `GetCameraTransform()` with `GetPlayerEyeTransform(p)`
7. [ ] Gate raw key input with `IsPlayerLocal(p)` + `ServerCall`
8. [ ] Replace `RegisterTool` with `RegisterTool(id, name, path, group)`
9. [ ] Add `SetToolEnabled`, `SetToolAmmo` in `PlayersAdded`
10. [ ] Add `SetToolAmmoPickupAmount` in `server.init()`
11. [ ] Replace custom UI framework with standard v2 options menu
12. [ ] Add keybind hints in `client.draw()`
13. [ ] Drop all UMF includes (`scripts/umf.lua`, etc.)
14. [ ] Run `python -m tools.lint --mod "ModName"` — must be 0 findings
15. [ ] Verify: `info.txt` has `version = 2`

---

## Complexity Estimate by Mod

| Mod | Unique Lines | UMF Deps | Difficulty | Notes |
|---|---|---|---|---|
| **Magnets** | ~200 | registry, tool, ui, sound | LOW | Magnet placement + physics pull. Simple tool. |
| **Omni Gun** | ~520 | registry, tool, ui, utility | MEDIUM | Physics projectile spawner. Shape copying. |
| **Blight Gun** | ~500+ | registry, tool, ui, utility, shape_utils, json, blob | MEDIUM-HIGH | Blight blob system, shape manipulation. |
| **BHL-X42** | ~400+ | registry, tool, ui, utility, projectiles, timers, sound, black_hole | HIGH | Black hole physics, projectile system, timers. |

**Recommendation:** Start with Magnets (lowest complexity), then Omni Gun.
