# Teardown MP Patches

Multiplayer compatibility patches for Teardown Steam Workshop mods. Converts v1 single-player mod scripts to v2 multiplayer-compatible code following official Teardown MP patterns.

> **Note:** These are community patches. Subscribe to the original mods on the Steam Workshop to support the original authors.

## Current Status

| Metric | Value |
|--------|-------|
| **Mods installed** | 112 |
| **Lint clean (tier 1)** | 112/112 |
| **Issues documented** | 73 (with rules derived from each) |
| **Lint rules** | 39 (covering 48 V2 rewrite rules) |
| **Deferred mods** | 13 (framework dependencies, too complex) |

## How It Works

Patches are applied directly to `C:/Users/trust/Documents/Teardown/mods/` — the game's local mod directory. Local mods override workshop versions when both exist.

**Key conversions:**
- Add `#version 2` header + v2 callbacks (`server.init`, `client.tick`, etc.)
- Split server/client logic (server owns game state, client owns visuals)
- Fix raw key input (`InputPressed("rmb", p)` fails silently in MP)
- Add per-player state via `PlayersAdded()`/`PlayersRemoved()` loops
- Convert `ipairs()` on iterators to bare `for p in Players() do`
- Add `SetToolAmmoPickupAmount` for mplib loot crate integration

## Project Structure

| Path | Purpose |
|------|---------|
| `docs/` | Research, patterns, guides, audit reports |
| `tools/` | Lint (39 rules), deepcheck, audit, auto-fix, log parser |
| `mods/` | Patches repo metadata (game does NOT read from here) |
| `.comms/` | Inter-terminal coordination (4-terminal team system) |
| `CLAUDE.md` | Project rules — 48 V2 rewrite rules, batch workflow, tool usage |
| `MASTER_MOD_LIST.md` | Complete mod inventory with batch history and workshop IDs |
| `ISSUES_AND_FIXES.md` | 73 documented bugs with root causes, fixes, and derived rules |

## Key References

- **`docs/BASE_GAME_MP_PATTERNS.md`** — How official Teardown tools sync in MP (12 patterns)
- **`docs/OFFICIAL_DEVELOPER_DOCS.md`** — Complete API from teardowngame.com (ground truth)
- **`docs/WHAT_WORKS.md`** — Proven fixes and patterns
- **`docs/WHAT_DOESNT_WORK.md`** — Failed approaches to avoid

## Developer Tools

```
python -m tools.status          # Session overview
python -m tools.lint             # 39-rule scanner (all mods)
python -m tools.lint --mod "X"   # Single mod
python -m tools.test --mod "X" --static  # Deep semantic analysis
python -m tools.audit            # Feature matrix
python -m tools.fix --dry-run    # Preview auto-fixes
python -m tools.logparse         # Parse game log for errors
```

## Batch History

See `MASTER_MOD_LIST.md` for the full inventory. Summary: 13 batches across 4 sessions converted 177 mods from v1 to v2, with 66+ later removed by user (engine stability at ~178 mods). Current set: 112 active, 13 deferred.
