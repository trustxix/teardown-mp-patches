# Infinity Technique — V2 Conversion Plan

**Status:** PLAN ONLY — no code written yet
**Source:** Workshop 3549181010, author DiggolBick
**Size:** 3505 lines main.lua + 499 lines options.lua = 4004 total (2 files)
**Difficulty:** Very High — 12 abilities, 12 remappable keybinds, environment manipulation

## Overview

Anime-inspired ability mod (Jujutsu Kaisen — Satoru Gojo's Limitless technique). Provides gravity manipulation, defensive barriers, domain expansion, telekinesis, and environmental effects.

## Abilities Identified (from v1 source analysis)

| # | Ability | Key (default) | Server-Side | Client-Side | Complexity |
|---|---------|---------------|-------------|-------------|------------|
| 1 | Blue (attraction) | LMB/usetool | Gravity(), ApplyBodyImpulse, PlayerGravity | SpawnParticle, DrawSprite, PlayLoop | High |
| 2 | Red (repulsion) | RMB/grab | Gravity(), ApplyBodyImpulse | SpawnParticle, DrawSprite, PlayLoop | High |
| 3 | Purple (merge) | V (cutsc) | MakeHole, Explosion, Destroy() | SpawnParticle, DrawSprite, camera effects | Very High |
| 4 | Infinity (barrier) | E (infkey) | Body velocity deflection | DrawSprite (ripple effect), PlayLoop | Medium |
| 5 | Domain Expansion | M (dom) | Environment properties, MakeHole, voxel spawn | Skybox/fog changes, DrawSprite, PointLight | Very High |
| 6 | Fly toggle | Alt (flykey) | SetPlayerVelocity | Camera FX | Low |
| 7 | Teleport | B (tel) | SetPlayerTransform | Camera FX | Low |
| 8 | Telekinesis (grab) | Q (grab) | SetBodyVelocity, ApplyBodyImpulse | DrawLine, PointLight | Medium |
| 9 | Lock bodies | Shift (lock) | SetBodyDynamic(false) | none | Low |
| 10 | Strength adjust | Z/X (sadd/ssub) | Modify Str/BluStr/RedStr | HUD update | Low |
| 11 | Time control | R (time) | SetTimeScale | HUD display | Low |
| 12 | Performance mode | 8 | none (local toggle) | Particle vs sprite mode | Low |

## Key Technical Challenges

### 1. Massive Monolithic Tick Function (1749 lines)
The v1 `tick(dt)` function is 1749 lines of deeply nested conditionals. Must be decomposed into per-ability functions for the server/client split.

### 2. Raw Key Inputs (12 remappable keybinds)
All abilities use `InputPressed(GetString("savegame.mod.inf.*"))` — raw keys read from savegame. In v2:
- Client reads keybinds locally (raw keys can't take player param)
- Client sends actions via ServerCall: `ServerCall("server.onBlue", p, aimPos)`, etc.
- Each ability gets its own ServerCall handler

### 3. Environment Manipulation (Domain Expansion)
Domain Expansion modifies `SetEnvironmentProperty()` and `SetPostProcessingProperty()` — these are GLOBAL state changes. In MP:
- Server must own the decision to activate/deactivate domain
- Environment changes affect ALL players (they're global)
- Need to save/restore original values when domain ends
- Only one player should be able to activate domain at a time

### 4. Per-Player State vs Global State
Many abilities use global variables (BlueTrack, RedTrack, etc.). In v2:
- Per-player state via `players[p]` table
- Each player has independent Blue/Red/Purple tracking
- Domain Expansion may remain single-instance (server decides who gets it)

### 5. 224 Server/Client API Calls to Split
Counted from v1: MakeHole, Explosion, PlaySound, SpawnParticle, DrawSprite, DrawLine, PointLight, QueryRaycast, SetBodyVelocity, ApplyBodyImpulse — all currently in the single-context v1 code.

## Proposed Architecture

```
server.init()
  RegisterTool, SetToolAmmo, keybind defaults

server.tick(dt)
  PlayersAdded/Removed — createPlayerData/cleanup
  Per-player: read ability inputs (via ServerCall handlers)
  Per-player: execute ability logic (physics, damage, destruction)
  Global: domain expansion state machine

server.onBlue(p, aimX, aimY, aimZ)      — Blue ability
server.onRed(p, aimX, aimY, aimZ)       — Red ability
server.onPurple(p, aimX, aimY, aimZ)    — Purple merge
server.onInfinity(p)                     — Toggle Infinity barrier
server.onDomain(p)                       — Domain Expansion
server.onTeleport(p, posX, posY, posZ)  — Teleport
server.onGrab(p, aimX, aimY, aimZ)      — Telekinesis
server.onLock(p)                         — Lock bodies
server.onFly(p)                          — Toggle fly
server.onStrength(p, delta)             — Adjust strength

client.init()
  Load sounds, sprites

client.tick(dt)
  PlayersAdded/Removed
  Per-player: read local input, fire ServerCalls
  Per-player: visual effects (particles, sprites, sounds)

client.draw()
  HUD: ability state, strength meter, keybind hints
  Options menu with UiMakeInteractive
```

## Conversion Strategy

### Phase 1: Scaffold (est. 200 lines)
- `#version 2` header, player.lua include
- `players = {}`, `createPlayerData()` with all per-player state
- `server.init()` with RegisterTool, ammo, keybind defaults
- `server.tick()` skeleton with Players/Added/Removed loops
- `client.init()` with sound/sprite loading
- `client.tick()` skeleton
- `client.draw()` with basic HUD + keybind hints
- info.txt with `version = 2`

### Phase 2: Low-complexity abilities (est. 150 lines)
- Fly toggle, teleport, lock, strength adjust, time control
- These are straightforward input→action patterns

### Phase 3: Medium-complexity abilities (est. 300 lines)
- Infinity barrier (body deflection on server, ripple sprites on client)
- Telekinesis (server body manipulation, client DrawLine/PointLight)

### Phase 4: High-complexity abilities (est. 400 lines)
- Blue technique (gravity well, body attraction, player gravity)
- Red technique (repulsion force, directional blast)
- Purple merge (requires both Blue+Red active, then merge sequence)

### Phase 5: Domain Expansion (est. 200 lines)
- Most complex: global environment changes, voxel spawning, area damage
- Server-authoritative state machine
- Single-instance (first to activate wins)
- Save/restore environment properties

### Phase 6: Options Menu (est. 100 lines from existing options.lua)
- Port 499-line options.lua to v2 client.draw() options pattern
- UiMakeInteractive, keybind remapping UI
- Savegame persistence

## Risks

1. **Domain Expansion global state** — may cause desyncs if multiple players try to activate simultaneously
2. **Purple merge physics** — heavy destruction (MakeHole spam) may cause lag in MP with multiple players
3. **Telekinesis per-player** — each player grabbing bodies independently may conflict
4. **Options.lua port** — 499 lines of custom UI, complex keybind remapping system
5. **Performance** — the v1 mod already has performance concerns (author notes); MP amplifies this

## Estimated Output
- ~1350 lines main.lua (down from 3505 — removing blank lines, crude comments, dead code, duplicate logic)
- ~200 lines options section in client.draw
- Total: ~1550 lines v2 (62% reduction from 4004)

## Decision Needed
This is the single most complex conversion remaining. Recommend:
- **Dedicated session** with no other tasks
- **Incremental testing** per phase (lint after each)
- **Consider dropping Domain Expansion** if too complex — it's the most impressive but least MP-compatible feature
