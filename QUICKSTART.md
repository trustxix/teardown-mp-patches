# Teardown MP Patcher — Quick Start

Automated v1→v2 multiplayer mod conversion for Teardown Workshop mods.

## First Thing

```
python -m tools.status
```

This gives you: mod count, last commit, game log errors, lint failures, missing features.

## Key Paths

| What | Where |
|------|-------|
| **Live mods (edit here)** | `C:/Users/trust/Documents/Teardown/mods/` |
| **Game log** | `C:/Users/trust/AppData/Local/Teardown/log.txt` |
| **Project repo** | `C:/Users/trust/teardown-mp-patches/` |
| **Reference mods** | `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/` |
| **Issues log** | `ISSUES_AND_FIXES.md` |
| **API reference** | `C:/Users/trust/Documents/Teardown/TEARDOWN_V2_API_REFERENCE.md` |
| **Backup** | `C:/Users/trust/Documents/Teardown/mods_BACKUP/` |

## Top 10 Rules

1. `#version 2` + `#include "script/include/player.lua"` header
2. Per-player state: `players = {}` with `createPlayerData()`
3. Three-phase loop: `PlayersAdded()` → `PlayersRemoved()` → `Players()`
4. NEVER `ipairs()` on Players/PlayersAdded/PlayersRemoved — they're iterators
5. NEVER raw keys with player param — use ServerCall pattern
6. `SetToolEnabled("id", true, p)` — string, bool, player order
7. Server: damage/physics/state. Client: audio/visual/UI.
8. `options.lua` stays UNCHANGED — special menu callbacks
9. Always check `log.txt` after testing (`python -m tools.logparse`)
10. All edits in `Documents/Teardown/mods/` — never the patches repo

## Developer Tools

| Command | When |
|---------|------|
| `python -m tools.status` | Start of every session |
| `python -m tools.lint --mod "X"` | After writing mod code |
| `python -m tools.fix --dry-run` | Check for auto-fixable issues |
| `python -m tools.logparse` | After user tests a mod |
| `python -m tools.audit` | To see what features mods are missing |

## Detailed Docs

- `CLAUDE.md` — full rewrite rules + developer tool commands
- `docs/RESEARCH.md` — 34 API findings from official sources
- `ISSUES_AND_FIXES.md` — 32 resolved bugs with rules
- `docs/V2_SYNC_PATTERNS.md` — network sync patterns for custom entities
- `docs/AUDIT_REPORT.md` — generated feature matrix (run `python -m tools.audit`)
