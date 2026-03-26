# Local MP Testing Setup — Dual Steam via Sandboxie Plus

How to test Teardown multiplayer locally with two game instances on one PC.

**Tested on:** Windows 11 Pro 25H2 (Build 26200), Sandboxie Plus 1.17.2, Steam March 2026.

---

## Overview

Two Steam accounts, two Teardown installs, one machine. Main Steam runs normally, second Steam runs inside a Sandboxie Plus App Compartment with IPC renaming so the two instances don't detect each other.

| Instance | Steam Path | Teardown Mods Path |
|----------|-----------|-------------------|
| **Main** | `C:\Program Files (x86)\Steam` | `C:\Program Files (x86)\Steam\steamapps\common\Teardown\mods\` |
| **Sandboxed** | `C:\Steam2` | `C:\Steam2\steamapps\common\Teardown\mods\` |

## Prerequisites

### 1. Disable Windows MIDI Service

Windows 11 25H2's `midisrv` interferes with IPC inside Sandboxie. Admin prompt:

```
sc.exe config midisrv start= disabled
sc.exe stop midisrv
```

No effect on game audio. Only matters for physical MIDI keyboards.

### 2. Second Steam Copy

Full copy of `C:\Program Files (x86)\Steam` to `C:\Steam2`.

Clear `C:\Steam2\config\loginusers.vdf`:
```
"users"
{
}
```

Install Teardown on the second account so it lives under `C:\Steam2\steamapps\common\Teardown\`.

### 3. Sandboxie Plus Config

Create sandbox named `SteamTest`. Edit ini to:

```ini
[SteamTest]
Enabled=y
ConfigLevel=10
NoSecurityIsolation=y
UseAlternateIpcNaming=y
BlockNetParam=n
UseFileDeleteV2=y
UseRegDeleteV2=y
ClosedFilePath=|*\wdmaud2.drv
ClosedIpcPath=*\SC_AutoStartComplete
OpenIpcPath=\Sessions\*\BaseNamedObjects\SteamChrome_*
OpenIpcPath=\RPC Control\*
OpenFilePath=C:\Steam2\*
```

**Key settings:**
- `NoSecurityIsolation=y` — App Compartment mode (Steam needs direct GPU/window access)
- `UseAlternateIpcNaming=y` — Renames IPC objects per sandbox so dual-instance detection is bypassed
- **Do NOT add `NoSecurityFiltering=y`** — disables the IPC renaming and breaks everything

## Launching

1. Open main Steam, log into first account
2. Launch sandboxed Steam:
   ```
   "C:\Program Files\Sandboxie-Plus\Start.exe" /box:SteamTest "C:\Steam2\steam.exe"
   ```
   Or: Sandboxie Plus GUI > right-click SteamTest > Run > Run Program > browse to `C:\Steam2\steam.exe`
3. On first launch: steamwebhelper "not responding" dialog appears. Select **"Restart Steam with Browser Sandboxing disabled"** and click OK. Saved in sandbox registry — only needed once.
4. Log in with second account. Launch Teardown on both.

## Testing Workflow

### Syncing Mods Between Instances

Both Teardown installs need **byte-identical mod files** for MP. After patching mods on the main install:

Use the dedicated sync script (robocopy-based, more reliable than rsync on Windows):

```bash
# Single mod
python "C:/Users/trust/Desktop/Teardown Workshop/sync_installs.py" --mod "ModName"

# All mods (mirror)
python "C:/Users/trust/Desktop/Teardown Workshop/sync_installs.py" --mods

# Verify both installs match
python "C:/Users/trust/Desktop/Teardown Workshop/sync_installs.py" --check

# Workshop content too
python "C:/Users/trust/Desktop/Teardown Workshop/sync_installs.py" --workshop
```

### Test Procedure

1. Patch mod on main install, run lint:
   ```
   python -m tools.lint --mod "ModName"
   ```
2. Copy patched mod to `C:\Steam2\steamapps\common\Teardown\mods\ModName\`
3. Launch Teardown on both instances
4. Host creates lobby on one instance, other joins
5. Test the mod in MP
6. After testing, parse logs:
   ```
   python -m tools.logparse
   ```

### Saved Modlists

Teardown supports saved mod configurations at `C:\Users\trust\AppData\Local\Teardown\modlists\`:

| File | Name | Contents |
|------|------|----------|
| `1.xml` | Default | Empty (all mods active) |
| `2.xml` | Host | 33 mods — curated MP hosting set |

Use modlists to quickly switch between full mod set (solo testing) and curated MP set (hosting friends).

### Log Locations

| Instance | Log Path |
|----------|----------|
| Main | `C:\Users\trust\AppData\Local\Teardown\log.txt` |
| Sandboxed | Check sandbox file system — may be in sandboxed AppData |

### Crash Logs

Crash dumps are at `C:\Users\trust\AppData\Local\Teardown\crash\` with timestamped directories containing `teardown.exe` and `.pdb` files. Recent crashes (Mar 19-22) were caused by shadow volume overflow with too many active mods — resolved by reducing from 178 to 125.

## Troubleshooting

**Sandboxed Steam flashes "checking for updates" and disappears:**
`UseAlternateIpcNaming=y` isn't active. Verify `NoSecurityFiltering=y` is NOT in the config.

**steamwebhelper dialog every launch:**
Sandbox content was deleted. The preference is in the sandboxed registry. Leave sandbox content intact.

**Zombie processes after closing:**
```
taskkill /IM steamerrorreporter64.exe /F
```

**Broke after Steam update:**
Delete sandbox content (right-click > Delete Content), relaunch, click through dialog again. Login is remembered.

**Mods work on host but not on joiner:**
Files aren't identical. Re-copy the mod folder. Check that `info.txt` has `version = 2`.

## What Does NOT Work

Documented so nobody wastes time retrying:

- `ClosedIpcPath` to block `Valve_SteamIPC_Class` — not enforced in App Compartment mode
- Standard Sandbox — Steam UI won't render
- `-no-cef-sandbox` / `-cef-disable-sandbox` flags — don't prevent webhelper crash
- `NoSecurityFiltering=y` — disables IPC renaming, breaks dual instance
- Clearing `SteamPID` registry key — race condition, unreliable
- `-master_ipc_name_override` — broke in early 2025

## Related

- Full Sandboxie guide: `C:\Users\trust\SandboxieSteamProject\GUIDE.md`
- Desktop launcher: `C:\Users\trust\Desktop\SteamTestLauncher.exe`
- Launcher source: `C:\Users\trust\SteamTestLauncher.cs`
