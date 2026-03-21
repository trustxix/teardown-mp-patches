# Universal UI Standards — All Tools & Mods

Every tool and mod must follow these layout and styling rules for consistency.
All UI elements use dynamic table-based stacking to prevent overlapping.

---

## Core Principle: Table-Based Dynamic Stacking

Every group of UI elements uses a table and renders in a defined direction.
This prevents overlapping because:
1. Each element knows its exact height/spacing
2. Zones grow in ONE direction only (up or down)
3. Zone anchors are placed so they can never collide

```lua
-- Pattern: render a list of elements growing in a direction
local items = { "Line 1", "Line 2", "Line 3" }
local lineH = 18  -- consistent line height

UiPush()
UiAlign("left bottom")
UiTranslate(anchor_x, anchor_y)
for i = #items, 1, -1 do          -- reverse = grow UPWARD
    UiText(items[i])
    UiTranslate(0, -lineH)
end
UiPop()
```

---

## HUD Layout Zones

```
┌─────────────────────────────────────────────────────────┐
│ [ZONE A: TOP LEFT]                   [ZONE B: TOP RIGHT]│
│ Anchor: (20, 80)                     Reserved/future    │
│ Grows: DOWNWARD                                         │
│ Max height: 40% screen                                  │
│                                                         │
│                                                         │
│                    [ZONE C: CENTER]                      │
│                    Anchor: (W/2, H*0.6)                  │
│                    Grows: DOWNWARD                       │
│                    Temporary prompts only                │
│                                                         │
│                                                         │
│ [ZONE D: BOTTOM LEFT]       [ZONE E: BOTTOM CENTER]    │
│ Anchor: (10, H-30)          Anchor: (W/2, H-75)        │
│ Grows: UPWARD               Grows: UPWARD               │
│ Max: left 40% width         Max: center 40% width       │
└─────────────────────────────────────────────────────────┘
```

---

## Zone Definitions

### Zone A — Top Left: Mod Status HUD
- **Anchor:** `UiTranslate(20, 80)` with `UiAlign("left top")`
- **Direction:** Grows DOWNWARD
- **Line height:** 18px
- **Content:** Persistent mod state (Fly: ON, Godmode: OFF, hotkeys)
- **Max:** Don't exceed 40% of screen height
```lua
local status = { "Fly: ON  [F5]", "Godmode: OFF" }
UiPush()
UiAlign("left top")
UiFont("regular.ttf", 14)
UiTextOutline(0, 0, 0, 1, 0.5, 0.5)
UiTranslate(20, 80)
for i = 1, #status do
    UiText(status[i])
    UiTranslate(0, 18)
end
UiPop()
```

### Zone C — Center: Temporary Action Prompts
- **Anchor:** `UiTranslate(UiWidth() / 2, UiHeight() * 0.6)` with `UiAlign("center middle")`
- **Direction:** Grows DOWNWARD
- **Line height:** 22px
- **Content:** Action prompts ONLY — disappear after action completes
- **Never persistent info, never ammo, never keybinds**
```lua
local prompts = { "TARGET ACQUIRED", "LMB: CONFIRM", "R: ABORT" }
UiPush()
UiAlign("center middle")
UiFont("bold.ttf", 16)
UiTextOutline(0, 0, 0, 1, 0.1)
UiColor(1, 1, 1, 1)
UiTranslate(UiWidth() / 2, UiHeight() * 0.6)
for i = 1, #prompts do
    UiText(prompts[i])
    UiTranslate(0, 22)
end
UiPop()
```

### Zone D — Bottom Left: Keybind Hints
- **Anchor:** `UiTranslate(10, UiHeight() - 30)` with `UiAlign("left bottom")`
- **Direction:** Grows UPWARD (reverse loop)
- **Line height:** 18px
- **Content:** Tool-specific keybinds for currently held tool
- **Max width:** 40% of screen (stays clear of center zone)
```lua
local hints = { "R - Reload", "MMB - Fire Mode", "RMB - Aim" }
UiPush()
UiAlign("left bottom")
UiFont("bold.ttf", 16)
UiTextOutline(0, 0, 0, 1, 0.1)
UiColor(1, 1, 1, 0.6)
UiTranslate(10, UiHeight() - 30)
for i = #hints, 1, -1 do
    UiText(hints[i])
    UiTranslate(0, -20)
end
UiPop()
```

### Zone E — Bottom Center: Ammo & Status
- **Anchor:** `UiTranslate(UiWidth() / 2, UiHeight() - 75)` with `UiAlign("center")`
- **Direction:** Grows UPWARD (reverse loop)
- **Line height:** 20px
- **Content:** Ammo count, fire mode, reload status, mode indicator
```lua
local lines = {}
if reloading then
    lines[#lines+1] = {text = "RELOADING...", color = {1, 0.8, 0, 0.9}}
else
    lines[#lines+1] = {text = mag.."/"..ammo.."  "..fireMode, color = {1, 1, 1, 0.9}}
end
lines[#lines+1] = {text = "MODE: Bunker Buster (R)", color = {1, 1, 1, 0.9}}

UiPush()
UiAlign("center")
UiFont("bold.ttf", 16)
UiTextOutline(0, 0, 0, 1, 0.1)
UiTranslate(UiWidth() / 2, UiHeight() - 75)
for i = #lines, 1, -1 do
    UiColor(unpack(lines[i].color))
    UiText(lines[i].text)
    UiTranslate(0, -20)
end
UiPop()
```

---

## Font Standards

| Element | Font | Size | Color | Opacity |
|---------|------|------|-------|---------|
| Ammo count / mode | bold.ttf | 16 | White | 0.9 |
| Keybind hints | bold.ttf | 16 | White | 0.6 |
| Status indicators (ON/OFF) | regular.ttf | 14 | Green(ON)/Gray(OFF) | 0.9/0.7 |
| Action prompts (center) | bold.ttf | 16 | White | 1.0 |
| Sub-prompts (LMB: CONFIRM) | bold.ttf | 14 | White | 0.9 |
| Options panel title | bold.ttf | 20 | White | 1.0 |
| Options panel buttons | bold.ttf | 13 | White | 1.0 |
| Options panel labels | regular.ttf | 13 | Light gray | 0.8 |

### Line Heights (consistent spacing)
| Zone | Line height |
|------|-------------|
| Zone A (top-left status) | 18px |
| Zone C (center prompts) | 22px |
| Zone D (bottom-left keybinds) | 18px |
| Zone E (bottom-center ammo) | 20px |

### Text Outline
Always use `UiTextOutline(0, 0, 0, 1, 0.1)` for in-game HUD text.
Not needed for menu panels with dark backgrounds.

---

## Menu Standards

### Options / Settings Access
- **Always via `PauseMenuButton()` in `tick()` or `client.tick()`** — never raw keybinds
- **Never in `draw()` / `client.draw()`** — PauseMenuButton doesn't work there
- **One button per mod** — use a panel for multiple controls
- **Non-tool mods** (weather, utilities): PauseMenuButton only, no global keybinds

### Panel Design
- **Background:** `UiColor(0.1, 0.1, 0.1, 0.94)` dark overlay
- **Buttons:** Full rectangle clickable via helper:
```lua
function PanelButton(label, bw, bh)
    local pressed = false
    UiPush()
        UiAlign("left top")
        pressed = UiBlankButton(bw, bh)
    UiPop()
    UiPush()
        UiAlign("left top")
        UiTranslate(bw / 2, bh / 2)
        UiAlign("center middle")
        UiText(label)
    UiPop()
    return pressed
end
```
- **Active state:** Green `(0.2, 0.65, 0.2)` for enabled, Dark gray `(0.3, 0.3, 0.3)` for disabled
- **Close button:** Red `(0.55, 0.12, 0.12)` at bottom — ALWAYS include one
- **ESC closes any menu:** ALL custom menus/panels MUST close when ESC is pressed. Add `if InputPressed("esc") then menuOpen = false end` to every menu. This prevents users from getting trapped in menus.
- **Always call `UiMakeInteractive()` before rendering interactive panels**
- **Panel elements use tables too** — button lists rendered from tables, same stacking pattern

### Tool Gating
- **ALL keybinds gated behind tool check** — `if GetPlayerTool(p) ~= TOOL_ID then return end`
- **Hardcoded gates only** — never rely on savegame options for gating
- **Gate must be ABOVE all input handling** — never after

---

## What NOT To Do

- No overlapping text — always use table-based stacking with consistent line heights
- No hardcoded Y positions for lists — always computed from table length
- No ammo bars or persistent info in center (only temporary prompts)
- No keybind hints in center (always bottom-left, stacked)
- No `UiTextButton` for panel buttons (use `UiBlankButton` + text)
- No `InputPressed("o")` or other raw keys for options (use PauseMenuButton)
- No font sizes above 16 for in-game HUD
- No font sizes above 20 for panel titles
- No single-line keybind dumps (always stacked, one per line)
- No custom crosshairs/reticles — use the engine's default crosshair only
