"""Diagnostic code injection for Teardown mod runtime testing.

Injects API wrappers and tick counters into a mod's main.lua,
reporting via DebugWatch (visual) and savegame registry (programmatic).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

DIAG_PREFIX = "__diag"
BACKUP_SUFFIX = ".testbackup"

# API wrappers injected at the top of the file (after #version/#include lines)
_API_WRAPPERS = '''
-- === DIAGNOSTIC INJECTION START (auto-generated, do not edit) ===
local __diag = {
    shootCount = 0, queryShotCount = 0, damageCount = 0,
    explosionCount = 0, makeHoleCount = 0,
    soundCount = 0, particleCount = 0, lightCount = 0,
    toolRegistered = false, toolIds = {},
    serverTicks = 0, clientTicks = 0, drawCalls = 0,
    errors = 0,
}

local __origShoot = Shoot
function Shoot(...) __diag.shootCount = __diag.shootCount + 1; return __origShoot(...) end

local __origQueryShot = QueryShot
function QueryShot(...) __diag.queryShotCount = __diag.queryShotCount + 1; return __origQueryShot(...) end

local __origApplyPlayerDamage = ApplyPlayerDamage
function ApplyPlayerDamage(...) __diag.damageCount = __diag.damageCount + 1; return __origApplyPlayerDamage(...) end

local __origExplosion = Explosion
function Explosion(...) __diag.explosionCount = __diag.explosionCount + 1; return __origExplosion(...) end

local __origMakeHole = MakeHole
function MakeHole(...) __diag.makeHoleCount = __diag.makeHoleCount + 1; return __origMakeHole(...) end

local __origPlaySound = PlaySound
function PlaySound(...) __diag.soundCount = __diag.soundCount + 1; return __origPlaySound(...) end

local __origSpawnParticle = SpawnParticle
function SpawnParticle(...) __diag.particleCount = __diag.particleCount + 1; return __origSpawnParticle(...) end

local __origPointLight = PointLight
function PointLight(...) __diag.lightCount = __diag.lightCount + 1; return __origPointLight(...) end

local __origRegisterTool = RegisterTool
function RegisterTool(id, ...)
    __diag.toolRegistered = true
    table.insert(__diag.toolIds, id)
    return __origRegisterTool(id, ...)
end
-- === DIAGNOSTIC INJECTION END ===
'''

# Counter increment prepended into function bodies
_SERVER_TICK_PREPEND = '    __diag.serverTicks = __diag.serverTicks + 1\n'
_CLIENT_TICK_PREPEND = '    __diag.clientTicks = __diag.clientTicks + 1\n'
_CLIENT_DRAW_PREPEND = '    __diag.drawCalls = __diag.drawCalls + 1\n'

# Reporting appended before the end of tick functions
_REPORTING_CODE = '''
    -- DIAG: DebugWatch (visual)
    DebugWatch("DIAG:Ticks", "S:" .. __diag.serverTicks .. " C:" .. __diag.clientTicks)
    DebugWatch("DIAG:Combat", "Shoot:" .. __diag.shootCount .. " QShot:" .. __diag.queryShotCount .. " Dmg:" .. __diag.damageCount)
    DebugWatch("DIAG:Effects", "Snd:" .. __diag.soundCount .. " Part:" .. __diag.particleCount .. " Light:" .. __diag.lightCount)
    DebugWatch("DIAG:Tools", table.concat(__diag.toolIds, ","))
    -- DIAG: Savegame registry (programmatic)
    SetString("savegame.mod.diag.ticks", __diag.serverTicks .. "," .. __diag.clientTicks)
    SetString("savegame.mod.diag.combat", __diag.shootCount .. "," .. __diag.queryShotCount .. "," .. __diag.damageCount .. "," .. __diag.explosionCount)
    SetString("savegame.mod.diag.effects", __diag.soundCount .. "," .. __diag.particleCount .. "," .. __diag.lightCount)
    SetString("savegame.mod.diag.tools", table.concat(__diag.toolIds, ","))
    SetString("savegame.mod.diag.errors", tostring(__diag.errors))
'''

# Regex patterns for finding function definitions
_HEADER_LINE_RE = re.compile(r'^#(version|include)\b')
_FUNC_DEF_RE = re.compile(r'^(\s*function\s+(?:server|client)\.(?:tick|draw)\s*\([^)]*\))')


def inject_diagnostics(mod_dir: Path) -> None:
    """Inject diagnostic instrumentation into a mod's main.lua.

    1. Backs up main.lua to main.lua.testbackup
    2. Inserts API wrappers after header lines
    3. Prepends tick counters into server.tick, client.tick, client.draw
    4. Appends reporting code into server.tick and client.tick
    """
    main_lua = mod_dir / "main.lua"
    backup = mod_dir / f"main.lua{BACKUP_SUFFIX}"

    if not main_lua.exists():
        return

    # Create backup
    shutil.copy2(main_lua, backup)

    source = main_lua.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)

    # Find where header lines end (after #version and #include)
    header_end = 0
    for i, line in enumerate(lines):
        if _HEADER_LINE_RE.match(line.strip()):
            header_end = i + 1
        elif line.strip() and not _HEADER_LINE_RE.match(line.strip()):
            # Allow blank lines between headers
            if not line.strip():
                continue
            break

    # Build output: header lines + wrappers + rest of source
    output_lines = lines[:header_end]
    output_lines.append(_API_WRAPPERS + '\n')

    # Process remaining lines — inject into function bodies
    i = header_end
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # Check for function definitions we want to instrument
        if re.match(r'\s*function\s+server\.tick\s*\(', stripped):
            output_lines.append(line)
            output_lines.append(_SERVER_TICK_PREPEND)
            # Scan forward to find the closing 'end' and insert reporting before it
            i += 1
            depth = 1
            func_body_lines = []
            while i < len(lines) and depth > 0:
                fline = lines[i]
                fstripped = fline.strip()
                for kw in ['function', 'if', 'for', 'while', 'repeat']:
                    if re.search(rf'\b{kw}\b', fstripped):
                        depth += 1
                        break
                if re.search(r'\bend\b', fstripped):
                    depth -= 1
                if depth <= 0:
                    # Insert reporting before the closing end
                    output_lines.extend(func_body_lines)
                    output_lines.append(_REPORTING_CODE)
                    output_lines.append(fline)  # the 'end' line
                else:
                    func_body_lines.append(fline)
                i += 1
            continue

        elif re.match(r'\s*function\s+client\.tick\s*\(', stripped):
            output_lines.append(line)
            output_lines.append(_CLIENT_TICK_PREPEND)
            i += 1
            depth = 1
            func_body_lines = []
            while i < len(lines) and depth > 0:
                fline = lines[i]
                fstripped = fline.strip()
                for kw in ['function', 'if', 'for', 'while', 'repeat']:
                    if re.search(rf'\b{kw}\b', fstripped):
                        depth += 1
                        break
                if re.search(r'\bend\b', fstripped):
                    depth -= 1
                if depth <= 0:
                    output_lines.extend(func_body_lines)
                    output_lines.append(_REPORTING_CODE)
                    output_lines.append(fline)
                else:
                    func_body_lines.append(fline)
                i += 1
            continue

        elif re.match(r'\s*function\s+client\.draw\s*\(', stripped):
            output_lines.append(line)
            output_lines.append(_CLIENT_DRAW_PREPEND)
            i += 1
            continue

        else:
            output_lines.append(line)
            i += 1

    main_lua.write_text(''.join(output_lines), encoding="utf-8")


def restore_from_backup(mod_dir: Path) -> None:
    """Restore main.lua from backup if it exists."""
    main_lua = mod_dir / "main.lua"
    backup = mod_dir / f"main.lua{BACKUP_SUFFIX}"

    if backup.exists():
        shutil.copy2(backup, main_lua)
        backup.unlink()
