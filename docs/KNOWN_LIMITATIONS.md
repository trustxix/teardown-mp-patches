# Known Limitations & Gotchas

Technical limitations discovered through testing that aren't obvious from docs or code. Each cost real debugging time.

---

## Engine Limits

### Active Mod Ceiling

The engine crashes when too many mods are active. Root cause: shadow volume integer overflow (values hit ~7.9 billion GB).

| Mod Count | Result |
|-----------|--------|
| ~125 | Safe. Audio budget ~650MB. |
| ~150 | Warning zone. Performance degrades. |
| 178 | Crash (strncpy buffer overflow during mod enumeration). |

Audio-heavy mods (vehicle/weapon packs with custom sounds) consume disproportionate memory. Deprioritize these when near the limit.

**Not fixable from mod code.** Only solution is reducing active mod count.

### Audio Budget

With 178 mods: ~760MB audio. With 125 mods: ~650MB. Vehicle and weapon packs with many .ogg files are the biggest consumers. Monitor total when adding mods.

---

## V2 Preprocessor Quirks

### `local` at File Scope is Invisible Across Contexts

The v2 preprocessor splits scripts into separate server/client chunks. A `local` variable at file scope only exists in ONE chunk — the other chunk gets nil.

```lua
-- BAD: projectiles table invisible in server functions
local projectiles = {}

function server.tick(dt)
    -- projectiles is nil here!
end
```

```lua
-- GOOD: module-level without local
projectiles = {}

function server.tick(dt)
    -- projectiles works
end
```

This is why CLAUDE.md rule #17 says "NEVER use `local` at file scope".

### Nested Callback Definitions Silently Break

`function server.*()` / `function client.*()` definitions are extracted by the preprocessor regardless of nesting. If defined inside another function, closures break silently — the callback runs but captured variables are nil.

```lua
-- BAD: server.fire() extracted out of the closure, myVar is nil
function setup()
    local myVar = 10
    function server.fire(p)
        print(myVar) -- nil!
    end
end
```

### Lint Annotations Can Break Syntax

Placing lint annotations between a function name and its arguments causes Lua compile errors:

```lua
-- BAD: breaks compilation
ClientCall -- @lint-ok PER-TICK-RPC
(id, "client.onHit", x, y, z)

-- GOOD: annotation at end of line
ClientCall(id, "client.onHit", x, y, z) -- @lint-ok PER-TICK-RPC
```

---

## Tool Limitations

### Deepcheck Does Not Catch Lua Syntax Errors

`tools.test --static` (deepcheck) checks SEMANTIC correctness — firing chains, effect chains, asset refs, ID consistency. It does NOT check syntactic correctness (Lua compilation).

A mod can pass all deepcheck checks but fail to compile in-game. Known failure cases:
- Orphaned `end` statements from incomplete block deletion
- Misplaced comments inside expressions
- Unclosed blocks

**Mods that failed this way:** ARM_M4A4, ARM_NOVA, Hurricanes_and_Blizzards.

**Mitigation:** When the game log shows compile errors, don't dismiss them because deepcheck passed. Read the actual code. Consider `luac -p` as an additional check.

### `tools.lint` vs In-Game Behavior

Tools passing does NOT mean the mod works. Only in-game testing is final. The lint tool catches 45 known patterns but cannot simulate the v2 runtime environment.

---

## Camera Input

### `mousedx`/`mousedy` vs `camerax`/`cameray`

Which input to use depends on whether the mod controls the camera:

| Mod Camera Type | Use | Why |
|----------------|-----|-----|
| `SetCameraTransform()` (custom camera) | `mousedx` / `mousedy` | `camerax`/`cameray` return 0 when camera is script-controlled |
| Normal gameplay camera | `camerax` / `cameray` | Respects player sensitivity, returns degrees |

### Camera Sensitivity Formula (Reusable)

For any mod with a custom camera (`SetCameraTransform`):

```lua
local mx, my = InputValue("mousedx"), InputValue("mousedy")
local sens = (GetInt("options.input.sensitivity") / 1000) * (zoomlevel / 6)
CameraRot = QuatRotateQuat(CameraRot, QuatEuler(-my * sens, -mx * sens, 0))
```

- `options.input.sensitivity`: player's setting (e.g. 25)
- Divide by 1000 (not 100) to match on-foot feel — raw mousedx values are larger than engine internal values
- `zoomlevel / defaultZoom`: slower camera when zoomed in, faster when zoomed out
- `SetCameraTransform(transform, zoomlevel * 10)`: FOV param, higher = wider

---

## V1 to V2 Conversion

### Template Approach Does NOT Work

Simply renaming callbacks (`init()` -> `server.init()`) and moving code blocks produces scripts that pass syntax checks but DO NOT work in-game. Full logic restructuring is required.

### V1 -> V2 API Translation

| V1 | V2 | Notes |
|----|-----|-------|
| `init()` | `server.init()` + `client.init()` | Split logic by context |
| `tick(dt)` | `server.tick(dt)` + `client.tick(dt)` | + PlayersAdded/Removed/Players loops |
| `draw()` | `client.draw()` | Use `GetLocalPlayer()`, NOT `Players()` |
| `InputDown("lmb")` | `InputDown("usetool", p)` | Tool-specific input |
| `InputDown("rmb")` | `InputDown("rmb")` + ServerCall | Raw keys: NO player param |
| `GetCameraTransform()` | `GetPlayerEyeTransform(p)` | Per-player |
| `GetString("game.player.tool")` | `GetPlayerTool(p)` | |
| `GetToolBody()` | `GetToolBody(p)` | |
| `SetToolTransform(t)` | `SetToolTransform(t, 1.0, p)` | Weight param added |
| `SetBool("game.tool.X.enabled", true)` | `SetToolEnabled("X", true, p)` | In PlayersAdded |
| `GetPlayerVelocity()` | `GetPlayerVelocity(p)` | |
| `SetPlayerVelocity(vel)` | `SetPlayerVelocity(vel, p)` | |
| `SetPlayerTransform()` | `SetPlayerTransform(t, p)` | **SERVER-ONLY in v2** |
| `InputValue("mousedx")` | `InputValue("camerax") * 180 / math.pi` | Normal camera only |

### options.lua

Leave special Teardown options callbacks (`init()` + `draw()`) intact. options.lua needs `#version 2` and its own v2 callbacks but does NOT use `server.init()`/`client.init()` — it uses the Teardown options menu system.

---

## UMF Mods

UMF (Universal Mod Framework) mods share ~10K lines of framework code (umf.lua, entities.lua, registry.lua, json.lua, color.lua, constraint.lua, math.lua). Line counts are misleading.

**Example:** Shards Summoner was estimated at 456 unique lines but actually had 2,677 lines of real logic in tool.lua/ui.lua.

When estimating UMF mod complexity, read the actual tool.lua/ui.lua/utility.lua files. Count real unique logic, not total minus known framework files.

---

## Batch Workflow

Never change more than 3 mods at once. A previous session changed 30+ mods simultaneously — when the game crashed, isolating the culprit across 30 mods with binary search took hours and was never precisely identified.

**Rule:** 2-3 mods per batch, test between batches, commit after each batch for rollback points.

---

## Pending Work

### ~75 New Workshop Subscriptions (as of 2026-03-19)

- ~35 maps/content (copy, no patching)
- ~15 vehicle packs (copy, minimal patching)
- ~15 tool mods (need v2 conversion)
- ~6 deferred (Shards Summoner, GLARE, Lockonauts Toolbox, Ascended Sword Master, ProBallistics, Thermite Cannon)
- ~5 gameplay/asset mods

Run `python -m tools.sync` to check current state.

### Missing Doc: V2_SYNC_PATTERNS.md

Memory references `docs/V2_SYNC_PATTERNS.md` as a sync patterns guide, but this file was never created. The knowledge exists spread across `docs/BASE_GAME_MP_PATTERNS.md` (5 sync mechanisms, 12 patterns from official scripts) and `docs/WHAT_WORKS.md` (per-issue sync fixes). A consolidated sync reference would be valuable.

### AIO Integration

All_In_One_Utilities needs refactoring to use Trust Realism's dynamic tool discovery instead of its hardcoded tool list. Phases:

1. Replace hardcoded tool options panel with `DrawMasterPanel()`
2. Keep fly/godmode/noclip/speed as standalone AIO features
3. Include `lib/ballistics.lua` and use framework's options system
4. Consider moving utilities into ToolProfile system
5. AIO becomes thin wrapper — ESC menu button + delegation to framework

Separate project from current patcher work. Requires careful testing.

---

## Engine Quirks (from WHAT_DOESNT_WORK.md)

These are engine-level limitations with no mod-side fix:

### Custom Characters Don't Work in MP

Only 6 built-in Lagom family characters work. `characters.txt` modding is SP-only — the MP character picker ignores it. Engine limitation, waiting on Tuxedo Labs.

### XML Prefab Tools Can't Be Switched Programmatically

`SetPlayerTool()` and `SetString("game.player.tool")` can't load XML-prefab-registered tools. Tool body is invisible. Affected: ARM M4A4, ARM AK-47, ARM Glock, Light Saber [GP]. Workaround: filter from Tool Menu, use toolbar keys (1-6).

### No API to Disable Grab

`SetBool("game.player.cangrab", false)` has no effect. `ReleasePlayerGrab(p)` per-tick causes hand flash. RMB grab conflicts with ADS on gun mods. No fix exists.

### PauseMenuButton Must Be in tick(), Not draw()

`PauseMenuButton()` registers buttons during the tick phase. Calling it in `draw()` / `client.draw()` does nothing.

### ListKeys Returns Different Case Than RegisterTool

`ListKeys('game.tool')` may return IDs in different case. Always use case-insensitive comparison (`tool_id:lower():find()`).

---

## Weapon Float Bug (RESOLVED, Critical Knowledge)

After firing, weapon models floated out of hands in zero gravity. Affected 21+ mods. Root cause: timer-based position offsets in `SetToolTransform` and `SetShapeLocalTransform` caused physics collisions in v2's split server/client physics. Fix: remove ALL timer-based position offsets, use static positions only. The `~= 0` check (vs v1's `> 0`) let timers go negative, pushing tools behind the player indefinitely.

What didn't work: ReleasePlayerGrab, SetBool cangrab, merging SetToolTransform calls, changing smooth parameter, removing server GetToolBody, emptying server.tickPlayer.

---

## Trust Realism Sync Status

The patcher's `lib/realistic_ballistics.lua` is the source of truth (battle-tested in MP). The standalone repo (`~/trust-realism/src/ballistics.lua`) must be kept identical. When updating one, update both. See `docs/ECOSYSTEM.md` for repo locations.

---

## First MP Playtest Results (2026-03-22, Historical)

The first real MP session revealed that 100% static analysis pass rate meant nothing:
- Near-universal tool desync across modded tools
- AC-130 caused extreme lag (per-tick computation)
- Documents/ mods invisible to host in MP lobby
- "102 mods patched, 0 FAIL" was misleading — tools measure code patterns, not actual MP behavior

This led to the fundamental rule: **tools passing is necessary but NOT sufficient. Only in-game MP testing is final.**
