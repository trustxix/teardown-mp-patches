# Lint Rules Reference

All 45 rules from `tools/lint.py`. Each rule was derived from a real bug discovered during MP testing. Rule IDs match `@lint-ok` suppression annotations.

---

## Tier 1 — Hard Errors (14 rules)

These cause silent failures, crashes, or mods being disabled in MP.

| # | Rule ID | What It Catches | Why It Breaks |
|---|---------|-----------------|---------------|
| 1 | IPAIRS-ITERATOR | `ipairs(Players())` / `ipairs(PlayersAdded())` | These return iterators, not tables. `ipairs()` crashes or returns nothing. Use `for p in Players() do`. |
| 2 | RAW-KEY-PLAYER | `InputPressed("rmb", p)` with raw key + player param | Raw keys silently fail with player param. Use `InputPressed("rmb")` client-side + ServerCall. |
| 3 | TOOL-ENABLED-ORDER | `SetToolEnabled(p, "id", true)` with swapped args | Correct order: `SetToolEnabled("toolid", true, p)` — string, bool, player. |
| 4 | ALTTOOL | `"alttool"` key name | Use `"rmb"` instead. |
| 5 | GOTO-LABEL | `goto` or `::label::` syntax | Teardown uses Lua 5.1. No goto support. Use if/end. |
| 6 | MOUSEDX | `"mousedx"` / `"mousedy"` | Use `"camerax"` / `"cameray"` for normal camera. Exception: valid with `SetCameraTransform` mods. |
| 7 | SPT-CLIENT | `SetPlayerTransform()` in `client.*` | Server-only API. Silently fails on client. |
| 8 | DRAW-NOT-CLIENT | `function draw()` without client prefix | Must be `function client.draw()` in v2. Bare `draw()` is silently ignored. |
| 9 | HEALTH-ARG-ORDER | `SetPlayerHealth(p, 1)` with swapped args | Correct: `SetPlayerHealth(health, player)` — health first, player second. |
| 10 | MISSING-VERSION2 | v2 patterns without `#version 2` header | Script silently disabled in MP without the header. |
| 11 | QUERYSHOT-PLAYER-GUARD | `if player then` after QueryShot | QueryShot returns `player=0` for non-player hits. Lua `0` is truthy. Must use `player ~= 0`. |
| 12 | FILE-SCOPE-LOCAL | `local x = ...` at file scope in v2 | Preprocessor splits server/client chunks. File-scope locals invisible across boundary. |
| 13 | SHARED-TABLE-BOMB | Large `shared.*` table init (>50 elements) | Syncs every frame. Causes extreme lag with large tables. |
| 14 | PLAYERS-NO-INCLUDE | `PlayersAdded()` without `#include "script/include/player.lua"` | Function undefined without include. Use `GetAddedPlayers()` (engine built-in) as alternative. |
| 15 | INFO-MISSING-VERSION2 | Lua has `#version 2` but info.txt lacks `version = 2` | Mod won't be recognized as MP-compatible. |

---

## Tier 2 — Warnings (30 rules)

These cause desync, missing features, or degraded MP experience.

### Missing Features

| # | Rule ID | What It Catches | Fix |
|---|---------|-----------------|-----|
| 16 | MISSING-AMMO-DISPLAY | RegisterTool but no `SetString("game.tool.ID.ammo.display", "")` | Engine renders wrong ammo counter without this. |
| 17 | MISSING-TOOL-AMMO | SetToolEnabled but no SetToolAmmo | Players see 0 ammo, tool may not appear in toolbar. |
| 18 | MISSING-AMMO-PICKUP | RegisterTool but no SetToolAmmoPickupAmount | Ammo crates won't refill this tool. |
| 19 | MISSING-OPTIONS-GUARD | `InputPressed("usetool")` without `optionsOpen` check | Tool fires while options menu is open. |
| 20 | MISSING-OPTIONS-SYNC | `optionsOpen` used but no `server.setOptionsOpen` | Options state won't sync in MP. |
| 21 | MISSING-INTERACTIVE | UiTextButton without UiMakeInteractive | Buttons render but can't be clicked. |
| 22 | MISSING-KEYBIND-HINTS | 2+ raw key inputs but no hint UiText | Players won't know the keybinds. |
| 23 | MISSING-PLAYERS-REMOVED | PlayersAdded without PlayersRemoved | Per-player state leaks (memory grows forever). |
| 24 | MISSING-MOD-PREFIX | Asset path without `MOD/` prefix | `LoadSound("snd/fire.ogg")` fails in v2. Must be `LoadSound("MOD/snd/fire.ogg")`. |

### Desync Patterns

| # | Rule ID | What It Catches | Fix |
|---|---------|-----------------|-----|
| 25 | CLIENT-SERVER-FUNC | Server-only functions in `client.*` | Shoot, MakeHole, Explosion, SetPlayerVelocity, SetPlayerHealth in client = silent fail. |
| 26 | SERVER-EFFECT | SpawnParticle/PointLight/SetShapeEmissiveScale in `server.*` | Client-only rendering APIs. No visual on server. PlaySound on server IS ok. |
| 27 | PER-TICK-RPC | ServerCall/ClientCall in tick/update without guards | Floods reliable channel at 60 RPC/sec. Use registry broadcast or `shared.*`. |
| 28 | DOUBLE-PROCESS-TIMER | Same field modified in both `server.*` and `client.*` | Host runs both contexts on shared data = 2x speed. Use separate fields. |
| 29 | CLIENTCALL-SOUND | ClientCall wrapping PlaySound | Server PlaySound auto-syncs. No ClientCall needed. |
| 30 | TOOLANIM-LOCAL-ONLY | tickToolAnimator gated behind IsPlayerLocal | Must call for ALL players. Remote players see static tool otherwise. |
| 31 | CAMERAX-WITH-SETCAMERA | camerax/cameray in SetCameraTransform mod | Returns 0 when camera is script-controlled. Use mousedx/mousedy. |
| 32 | HOST-ONLY-HARDCODE | `GetLocalPlayer()==1` restriction | Restricts to host only. Remove `==1` to allow all players. |
| 33 | VARIABLE-KEY-PLAYER | `InputPressed(variable, p)` with non-literal first arg | If variable holds raw key, silently fails with player param. |

### Code Quality

| # | Rule ID | What It Catches | Fix |
|---|---------|-----------------|-----|
| 34 | HANDLE-GT-ZERO | `handle > 0` comparison | V2 client handles can be negative. Use `~= 0`. |
| 35 | MANUAL-AIM | QueryRaycast without GetPlayerAimInfo in weapon | Manual aim can desync. Use GetPlayerAimInfo for crosshair accuracy. |
| 36 | MAKEHOLE-DAMAGE | MakeHole without player damage | MakeHole can't damage players. Use Shoot() instead. |
| 37 | SHOOT-NO-ATTRIB | Shoot() with <7 args | Missing playerId/toolId for kill feed attribution. |
| 38 | EXPLOSION-NO-DAMAGE | Explosion without ApplyPlayerDamage | Explosion() does NOT damage players. Must add explicit ApplyPlayerDamage. |
| 39 | SETPLAYER-ARG-ORDER | SetPlayer* with player as first arg | Player is LAST: `SetPlayerVelocity(vel, p)`, not `SetPlayerVelocity(p, vel)`. |
| 40 | DAMAGE-NO-ATTACKER | ApplyPlayerDamage with <4 args | Missing attacker ID for kill attribution. |
| 41 | USE-SHOOT | QueryShot + ApplyPlayerDamage + MakeHole chain | Old pattern. Use Shoot() — handles terrain, players, kill feed, bullet trace, MP sync. |
| 42 | PER-TICK-SPATIAL | FindShapes/FindBodies/QueryAabb in tick | Expensive. Throttle to 4Hz or cache results. |
| 43 | V1-ENTITY-SCRIPT | Entity script with v1 callbacks, no `#version 2` | Silently disabled in MP. |
| 44 | V2-DEAD-CALLBACK | v2 script with bare v1 callbacks (init/tick/draw) | Silently ignored in MP. Only server.*/client.* callbacks run. |

---

## Deepcheck Semantic Validators (6 checks)

These trace multi-function chains — what lint can't catch with single-line regex.

| Validator | What It Checks | FAIL | WARN |
|-----------|----------------|------|------|
| **ASSET** | All `MOD/` asset paths point to existing files | File not found (checks .tde variants too) | — |
| **ID-XREF** | Tool IDs consistent across RegisterTool, SetToolEnabled, SetToolAmmo, GetPlayerTool | Case mismatch between registrations | Missing SetToolEnabled/SetToolAmmo |
| **FIRING-CHAIN** | usetool input -> ServerCall -> server damage complete | Shoot() in client, missing ServerCall, target doesn't exist | Indirect damage via helpers |
| **EFFECT-CHAIN** | Server damage broadcasts to clients for visuals | SpawnParticle in server damage function | No ClientCall after QueryShot damage |
| **HUD** | Tool mod has client.draw() with GetPlayerTool guard | — | No client.draw(), no tool guard |
| **SERVERCALL-PARAMS** | ServerCall arg count matches target function params | Target doesn't exist, arg count mismatch | — |

Suppress with `@deepcheck-ok CATEGORY` in info.txt (mod-level) or first 5 lines (file-level).

---

## API Database (`tools/api_database.json`)

53KB classification of every Teardown v2 API function. Each entry has:

```json
{
  "FunctionName": {
    "domain": "server" | "client" | "both",
    "needs_player_id": true | false,
    "restricted_to": null | "server" | "client",
    "notes": "..."
  }
}
```

**Key classifications:**
- **Server-only mutators:** SetPlayerHealth, SetPlayerTransform, SetPlayerVelocity, ApplyPlayerDamage, Shoot, MakeHole, Explosion
- **Client-only rendering:** SpawnParticle, PointLight, DrawLine, DrawSprite, SetShapeEmissiveScale, LoadLoop
- **Auto-synced from server:** PlaySound (no ClientCall needed)
- **Both contexts (read-only):** GetAllPlayers, GetLocalPlayer, GetPlayerCount, GetAddedPlayers, GetRemovedPlayers
- **Player param added in v2:** All player-state functions gained a player ID parameter

This database powers lint rules CLIENT-SERVER-FUNC and SERVER-EFFECT.
