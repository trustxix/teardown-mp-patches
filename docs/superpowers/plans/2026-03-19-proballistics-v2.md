# ProBallistics Framework — V2 Conversion Plan

**Status:** ANALYSIS ONLY — conversion NOT recommended at this time
**Source:** Workshop 3600192776 + expansion packs (3611419174, 3619318834)
**Author:** [PB] / Phalanx
**Size:** 17,447 lines across 54 lua files (3.5x larger than previously estimated "5000+")
**Difficulty:** EXTREME — full game engine framework

## Overview

ProBallistics is not a simple weapon mod — it's a complete ballistics simulation framework with its own SDK, weapon registration system, ammo types, vision modes, vehicle systems, and defense platforms. Converting it to v2 is equivalent to porting a game engine.

## Architecture (54 files)

### Core Systems
| File | Lines | Purpose |
|------|-------|---------|
| `src/main.lua` | 469 | Entry point, initMod(), tick/draw routing |
| `src/common.lua` | 667 | Shared utilities, math helpers, framework state |
| `src/ballistics.lua` | 996 | Projectile physics simulation engine |
| `src/particles.lua` | 1404 | Custom particle effects system |
| `src/sounds.lua` | 436 | Sound management system |
| `src/materials.lua` | 351 | Material/surface interaction system |

### Weapon Systems
| File | Lines | Purpose |
|------|-------|---------|
| `src/weapons.lua` | 388 | Weapon base class, registration |
| `src/weapons/hand-held.lua` | 911 | Hand-held weapon logic (firing, recoil, etc.) |
| `src/weapons/hand-held-rotary.lua` | ~200 | Rotary weapons (minigun-style) |
| `src/weapons/fx.lua` | ~150 | Muzzle flash, tracer effects |
| `src/weapons/casings.lua` | ~100 | Shell casing ejection |

### Ammo Types (8 categories!)
| File | Lines | Purpose |
|------|-------|---------|
| `src/ammo/base.lua` | ~200 | Ammo base class |
| `src/ammo/small-caliber.lua` | ~200 | Bullets |
| `src/ammo/hand-held.lua` | 660 | Grenades, RPG |
| `src/ammo/artillery.lua` | 554 | Howitzer shells |
| `src/ammo/rocketry.lua` | 831 | Rockets |
| `src/ammo/rocketry-advanced.lua` | 1043 | Guided missiles, ATGM |
| `src/ammo/rockets-incendiary.lua` | ~200 | Incendiary rockets |
| `src/ammo/bombs.lua` | 354 | Air-dropped bombs |
| `src/ammo/debris-shrapnel.lua` | 405 | Shrapnel simulation |

### Defense Systems
| File | Lines | Purpose |
|------|-------|---------|
| `src/phalanxPro.lua` | 698 | Phalanx CIWS defense system |
| `src/ironDome.lua` | 475 | Iron Dome missile defense |
| `src/antiAir.lua` | ~200 | Anti-air systems |

### Vision & HUD
| File | Lines | Purpose |
|------|-------|---------|
| `src/vision.lua` | ~200 | Vision mode framework |
| `src/milvision.lua` | ~200 | Military vision modes |
| `src/crosshair.lua` | ~200 | Dynamic crosshair system |
| `src/ui.lua` | ~200 | HUD framework |

### Vehicle & Navigation
| File | Lines | Purpose |
|------|-------|---------|
| `src/plane.lua` | 385 | Aircraft physics & control |
| `src/autopilot.lua` | ~200 | Autopilot system |
| `src/tracker.lua` | 507 | Target tracking system |
| `src/autoaim.lua` | ~200 | Auto-aim assistance |
| `src/spotter.lua` | ~200 | Spotter camera system |
| `src/obstacle-avoid.lua` | ~200 | Obstacle avoidance |

### SDK & API
| File | Lines | Purpose |
|------|-------|---------|
| `src/sdk/base.lua` | ~200 | SDK base framework |
| `src/sdk/weapons.lua` | ~200 | Weapon registration SDK |
| `src/sdk/commands.lua` | ~200 | Command system |
| `src/api/pb.weapons.lua` | ~200 | Public weapon API |
| `src/api/pb.commands.lua` | ~200 | Public command API |

### Configuration
| File | Lines | Purpose |
|------|-------|---------|
| `options.lua` | 474 | Options menu with keybind remapping |
| `src/mod_options.lua` | ~200 | ModOptions class |
| `src/randomizer.lua` | ~200 | RNG system |

## Key Technical Challenges

### 1. Ballistics Engine (996 lines)
The ballistics system simulates projectile physics (gravity, drag, wind) and detects impacts via raycasting. In v2:
- Projectile simulation MUST run on server (authoritative)
- Visual tracers run on client
- Each projectile's position must be synced or predicted
- With multiple players firing simultaneously, this could be 100+ active projectiles

### 2. Per-Player Weapon State
The framework maintains weapon state (magazine, fire mode, reload timer, recoil) in global variables. In v2:
- ALL weapon state must be per-player in `players[p]`
- 50+ state variables per weapon per player
- The SDK pattern means external mods depend on this API

### 3. Defense Systems (Phalanx, Iron Dome)
These are autonomous entities that detect and intercept projectiles. In v2:
- Server must track all projectiles AND defense system projectiles
- Client renders the interception effects
- Heavy CPU load from detection algorithms

### 4. Vision Modes
Night vision, thermal, LIDAR affect post-processing and rendering. In v2:
- These are per-player client effects (fine)
- But some vision modes highlight enemy positions which needs server data

### 5. Aircraft System
Commander plane tool with autopilot, bombing runs. In v2:
- Vehicle control → server
- Camera/HUD → client
- Bomb drops → server (physics + damage)

### 6. Extension/SDK System
Other mods can register weapons via the SDK. In v2:
- SDK API must work across server/client boundary
- Registration must happen in server.init
- External mods would also need v2 conversion

## Conversion Estimate

| Phase | Scope | Est. Lines | Effort |
|-------|-------|-----------|--------|
| 1 | Core framework + server/client split | 1500 | Very High |
| 2 | Ballistics engine (server) + tracers (client) | 800 | Very High |
| 3 | Hand-held weapons (fire, reload, recoil) | 600 | High |
| 4 | Ammo types (8 categories) | 1200 | Very High |
| 5 | Defense systems (Phalanx, Iron Dome) | 500 | High |
| 6 | Vision modes + HUD | 400 | Medium |
| 7 | Aircraft + autopilot | 400 | High |
| 8 | SDK/API layer | 300 | Medium |
| 9 | Options menu + keybinds | 200 | Low |
| **Total** | | **~5900** | **EXTREME** |

## Recommendation

**DO NOT convert this mod at this time.** Reasons:
1. **17,447 lines is 4x our largest conversion** (Infinity Technique was 4004 → 1143)
2. **SDK dependency** — other mods may depend on this framework's API
3. **Defense systems** (Phalanx, Iron Dome) have no clear v2 pattern for autonomous entities
4. **Risk** — the ballistics engine is physics-critical; bugs cause desync
5. **ROI** — one extremely complex mod vs 16 UMF mods that could be batch-converted

### If Converting Eventually
- Dedicate 3-4 full sessions minimum
- Start with Phase 1 (core) and Phase 3 (hand-held weapons only)
- Defer defense systems and aircraft until core works
- Test extensively with 2+ players after each phase
- Consider whether the author would do a v2 port themselves (check their Discord)
