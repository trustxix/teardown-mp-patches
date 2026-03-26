# Keybind Standards

Standardized keybind assignments for all custom mods. Prevents conflicts with engine controls and player movement.

---

## Reserved Keys — NEVER Use in Mods

### Engine Hardcoded (cannot be changed)

| Action | Key |
|--------|-----|
| Map | TAB |
| Pause | ESC |
| Change tool | MOUSE WHEEL or 1-6 |
| Use tool | LMB |
| Grab | HOLD RMB |
| Grab distance | HOLD RMB + MOUSE WHEEL |
| Throw | HOLD RMB + LMB |

### Player Movement (user-configurable, avoid conflicts)

| Action | Key |
|--------|-----|
| Move forward | W |
| Move backward | S |
| Move left | A |
| Move right | D |
| Jump | SPACE |
| Crouch | CTRL |
| Interact | F |
| Flashlight | T |
| Camera view | Y |

---

## Standardized Mod Keybinds

Every mod action MUST use these assignments. No exceptions.

### Firearms

| Action | Key | Notes |
|--------|-----|-------|
| Fire | LMB | Uses "usetool" — engine standard |
| Aim / ADS | RMB | Conflicts with grab — use `SetBool("game.input.locktool", true)` while aiming |
| Reload | R | Universal reload key for all firearms |
| Fire mode toggle | B | Semi/auto/burst switching |

### Value Adjustment (sliders, power, zoom)

| Action | Key | Notes |
|--------|-----|-------|
| Adjust value | HOLD G + SCROLL WHEEL | Standard for any slider-like control (power, range, size, etc.) |

Example: Thruster Tool uses Hold G + Scroll to adjust thrust power. All mods with adjustable values must follow this pattern.

### Tool Modes / Special Actions

| Action | Key | Notes |
|--------|-----|-------|
| Cycle mode | B | Switch between tool modes |
| Toggle special | V | Toggle on/off features (fly, noclip, laser, etc.) |
| Deploy / Place | LMB | Standard "use tool" action |
| Detonate / Trigger | MMB | Secondary trigger (C4 detonate, remote trigger) |
| Options menu | G | Open mod settings panel |

### Camera / Vehicle Mods

| Action | Key | Notes |
|--------|-----|-------|
| Enter/exit vehicle or camera | LMB | "usetool" to activate |
| Camera zoom | SCROLL WHEEL | Must use `SetBool("game.input.locktool", true)` to prevent tool switch |
| Camera look | MOUSE | Uses mousedx/mousedy with SetCameraTransform |

### Key Priority (when conflicts arise)

If two mods need the same key, resolve by this priority:
1. Engine hardcoded keys — NEVER override
2. Player movement keys (WASD, SPACE, CTRL, F, T, Y) — avoid unless tool is active and gated
3. Standardized mod keys above — follow the standard
4. Unique mod keys — use uncommon keys (X, C, V, B, N, M, Q, E)

### Available Keys for Custom Actions

Keys NOT used by engine or movement — safe for mod-specific bindings:

| Key | Suggested Use |
|-----|--------------|
| R | Reload (firearms only) |
| G | Options menu / hold for value adjust |
| B | Mode cycle / fire mode toggle |
| V | Toggle special feature |
| X | Secondary action |
| C | Tertiary action |
| N | Info display toggle |
| M | Map/minimap toggle |
| Q | Quick action |
| E | Alternate interact |
| MMB | Secondary trigger |
| SHIFT | Sprint modifier (hold) |

---

## Implementation Rules

1. ALL keybinds must be gated behind tool check: `if GetPlayerTool(p) == TOOL_ID then`
2. ALL keybinds must be displayed on-screen (MISSING-KEYBIND-HINTS lint rule)
3. RMB usage requires `SetBool("game.input.locktool", true)` to prevent grab
4. SCROLL WHEEL usage requires `SetBool("game.input.locktool", true)` to prevent tool switch
5. Raw keys need `IsPlayerLocal(p)` check + ServerCall for server actions
