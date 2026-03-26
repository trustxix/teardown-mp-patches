# Teardown Modding Ecosystem

All Teardown-related tools, scripts, and locations across the system. The MP patcher project is the hub — everything else feeds into it.

---

## Directory Map

| Location | Purpose |
|----------|---------|
| `C:/Users/trust/teardown-mp-patches/` | **Main project.** Patcher, linter, tools, docs. All mod editing happens here. |
| `C:/Program Files (x86)/Steam/steamapps/common/Teardown/mods/` | **Main game install.** Live mods. ALL edits go here. |
| `C:/Steam2/steamapps/common/Teardown/mods/` | **Sandboxed game install.** Second player for local MP testing. |
| `C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630/` | Workshop originals. Read-only reference. |
| `C:/Users/trust/Documents/Teardown/` | Local SP mods, backups, utilities. NOT visible in MP. |
| `C:/Users/trust/Teardown-ModSync/` | Mod sync/publish toolchain — zips, uploads, distributes to friends. |
| `C:/Users/trust/Dropbox/teardown-mod-pack/` | Distribution folder. 103 mod zips served to friends via Dropbox. |
| `C:/Users/trust/Desktop/Teardown Team/` | Agent team launchers (Claude Code orchestration). |
| `C:/Users/trust/Desktop/Teardown Workshop/` | Workshop publishing and install sync scripts. |
| `C:/Users/trust/Desktop/Teardown-ModSync/` | Compiled sync executables + logs. |
| `C:/Users/trust/trust-realism/` | Trust Realism framework standalone repo (GitHub: trustxix/trust-realism). Keep in sync with `lib/ballistics.lua`. |
| `C:/Users/trust/AppData/Local/Teardown/` | Game config, crash logs, GUID. |
| `C:/Users/trust/SandboxieSteamProject/` | Sandboxie dual-Steam setup (see `docs/TESTING_SETUP.md`). |

---

## Mod Distribution Pipeline

```
Edit mod in game install dir
        |
        v
tools.lint + tools.test --static (validate)
        |
        v
sync_installs.py (copy to Steam2 for local MP test)
        |
        v
Test in-game with dual Steam instances
        |
        v
td_mod_publisher.py (zip, hash, upload to GitHub + Dropbox)
        |
        v
manifest.json updated (friends' sync clients pull from this)
        |
        v
Publish_Teardown_Mods.py (push to Steam Workshop via SteamCMD)
```

---

## Tools Outside the Main Project

### Mod Sync & Distribution (`~/Teardown-ModSync/`)

| File | What It Does |
|------|-------------|
| `td_mod_sync.py` | Master sync tool. Syncs packaged mods to Teardown install, cleans non-synced mods from Documents, removes non-vanilla from install. Used by friends to receive mod packs. |
| `td_mod_publisher.py` | Zips changed mods, uploads to GitHub (`trustxix/teardown-mod-pack`) + Dropbox, updates `manifest.json` with SHA256 hashes and download URLs. |
| `dev_sync_host.py` | Watches game install mods folder, serves changes to dev clients via HTTP on port 9876 over Tailscale (100.87.49.91). |
| `dev_sync_client.py` | Polls host every 10s for mod changes, downloads updates. Used for real-time dev sync during testing sessions. |
| `manifest.json` | Distribution manifest — version, timestamp, game build ID, per-mod SHA256 + GitHub URLs. Last updated 2026-03-22. |
| `dist/` | Compiled exes: `Dev_Sync_CLIENT.exe`, `Dev_Sync_HOST.exe`, `Teardown-ModPublisher.exe`. |

### Workshop Publishing (`~/Desktop/Teardown Workshop/`)

| File | What It Does |
|------|-------------|
| `Publish_Teardown_Mods.py` | Pushes mods to Steam Workshop via SteamCMD. Modes: `--list` (dry run), `--mod "X"` (single), `--login` (auth), default (all). Requires `STEAM_USER`/`STEAM_PASS` env vars. |
| `sync_installs.py` | Syncs mods between main install and Steam2 (sandbox) using robocopy `/MIR`. Modes: `--list`, `--mods`, `--workshop`, `--mod "X"`, `--check` (verify match). |
| `Publish_Teardown_Mods.bat` | Wrapper for the publish script. |
| `sync.bat` | Wrapper for sync_installs.py. |
| `Delete_Workshop_Duplicates.bat` | Cleans duplicate Workshop items. |
| `Delete_Workshop_Web.py` / `.bat` | Removes Workshop items via web API. |

### Team Launchers (`~/Desktop/Teardown Team/`)

| File | What It Does |
|------|-------------|
| `launch_team.bat` | Launches 4-terminal Claude agent team (QA Lead, API Surgeon, Mod Converter, Docs Keeper) against the patcher project. |
| `launch_team_maintenance.bat` | Lightweight 2-agent variant (QA Lead + combined Maintainer). |
| `activate_all_mods.bat` | Runs `teardown-mp-patches/activate_all_local_mods.py` to enable all local mods. |

### Utilities (`~/Documents/Teardown/`)

| File | What It Does |
|------|-------------|
| `keybind_remapper.pyw` | System-level keyboard/mouse hook remapper (WH_KEYBOARD_LL/WH_MOUSE_LL). tkinter GUI. Remaps keys when Teardown is focused. Sub-millisecond latency. |
| `TEARDOWN_V2_API_REFERENCE.md` | V2 scripting API reference. **OUTDATED** — predates the MP release. Do not rely on for MP-specific APIs. |
| `mods_BACKUP/` | 100+ mod folder backups (AC130, Armored Vehicles, Russian Town, Boeing 737, GTAV Map, etc.). |
| `mods.7z` / `mods_BACKUP.7z` | Compressed mod archives (953MB + 319MB). |

### Crash Logs (`~/AppData/Local/Teardown/`)

| Path | What It Contains |
|------|-----------------|
| `crash/` | Crash dumps from 2026-03-19, 2026-03-20, 2026-03-22 (teardown.exe + .pdb). |
| `config_backup_20260322/` | Saved modlists and config snapshots. |
| `log.txt` | Current game log. Parse with `python -m tools.logparse`. |

### Design Docs (`~/docs/superpowers/`)

| File | What It Contains |
|------|-----------------|
| `plans/2026-03-16-teardown-mp-patcher.md` | Original project plan. |
| `specs/2026-03-16-teardown-mp-mod-patcher-design.md` | Original design spec. |

---

## Key Hardcoded Paths

Scripts across the ecosystem reference these paths. If any change, update all scripts.

| Path | Used By |
|------|---------|
| `C:\Program Files (x86)\Steam\steamapps\common\Teardown\mods` | td_mod_sync, td_mod_publisher, dev_sync_host, Publish_Teardown_Mods, sync_installs |
| `C:\Steam2\steamapps\common\Teardown\mods` | sync_installs |
| `C:\Program Files (x86)\Steam\steamapps\workshop\content\1167630` | Publish_Teardown_Mods, sync_installs |
| `C:\Users\trust\Teardown-ModSync\manifest.json` | td_mod_publisher |
| `C:\Users\trust\Dropbox\teardown-mod-pack` | td_mod_publisher |
| `C:\steamcmd\steamcmd.exe` | Publish_Teardown_Mods |
| `C:\Users\trust\teardown-mp-patches\workshop_ids` | Publish_Teardown_Mods |

---

## Sync Between Installs

For local MP testing, mods must be byte-identical on both installs. Use:

```bash
# Quick: single mod
python "C:/Users/trust/Desktop/Teardown Workshop/sync_installs.py" --mod "ModName"

# Full mirror
python "C:/Users/trust/Desktop/Teardown Workshop/sync_installs.py" --mods

# Verify they match
python "C:/Users/trust/Desktop/Teardown Workshop/sync_installs.py" --check
```

See `docs/TESTING_SETUP.md` for full dual-Steam setup.

---

## Trust Realism Framework

Standalone repo at `C:/Users/trust/trust-realism/` (GitHub: `trustxix/trust-realism`).

| Path | Contents |
|------|----------|
| `src/ballistics.lua` | Core library (1504 lines) |
| `docs/BALLISTICS.md` | Full API reference |
| `examples/hook_shotgun_profile.lua` | Example weapon profile |
| `README.md` | Overview, quick start, firing pipeline, roadmap (v1.0-v6.0) |

**Sync requirement:** The patcher's `lib/realistic_ballistics.lua` (1517 lines) and the standalone `src/ballistics.lua` (1504 lines) must be kept identical. They are currently **out of sync**. When updating one, update both.

**Roadmap:** v1.0 Ballistics (current) → v2.0 Effects → v3.0 Audio → v4.0 Ammo → v5.0 Physics → v6.0 Non-weapon tools.

---

## Project History (82 commits)

The project evolved through distinct phases visible in git history:

1. **Initial rewrite** — v2 rewrites for 10 tool mods, AI rewriter with proper v2 reference
2. **Subagent bug fixes** — Critical bugs in subagent-written mods (led to no-subagents rule)
3. **Tool development** — Lint (45 rules), deepcheck, audit, logparse, status, batch auto-fixer
4. **Team infrastructure** — 4-terminal autonomous team system with 5 MCP servers, dashboards, watchdog
5. **Deepcheck era** — 0 FAIL across 112+ mods, entity script conversions, workshop sync
6. **Trust Realism** — Realistic ballistics framework, Hook_Shotgun overhaul, USE-SHOOT resolution
7. **DEF framework** — Desync Exterminator Framework v1.2, project cleanup
8. **Ecosystem docs** — Testing setup, ecosystem map, known limitations (current session)
