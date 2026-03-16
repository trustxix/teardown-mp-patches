"""Phase 3b: AI-assisted v1→v2 Lua rewriter using Claude API.

This module sends v1 Teardown mod scripts to Claude with comprehensive
v2 architecture reference material, producing properly restructured
multiplayer-compatible code with per-player state management.
"""

import hashlib
import json
import time
from pathlib import Path

import anthropic

SYSTEM_PROMPT = r"""You are an expert Teardown modding assistant. Your job is to rewrite Teardown v1 (single-player) Lua scripts into v2 multiplayer-compatible format.

## V2 ARCHITECTURE RULES

### File Header
- Start with `#version 2`
- Add `#include "script/include/player.lua"` (provides Players(), PlayersAdded(), PlayersRemoved() iterators)

### Per-Player State (CRITICAL)
V1 mods use global variables. V2 mods MUST use per-player state tables:

```lua
players = {}

function createPlayerData()
    return {
        -- Move ALL per-player state here (timers, flags, physics refs, etc.)
        state = 0,
        coolDown = 0,
        angle = 0,
        body = nil,
        -- etc.
    }
end
```

### server.init() - Tool Registration
```lua
function server.init()
    RegisterTool("toolid", "Tool Name", "MOD/vox/tool.vox")
    -- Optional: load server-side sounds
end
```

### server.tick(dt) - MANDATORY Three-Phase Pattern
```lua
function server.tick(dt)
    -- PHASE 1: Initialize new players
    for p in PlayersAdded() do
        players[p] = createPlayerData()
        SetToolEnabled("toolid", true, p)
    end

    -- PHASE 2: Clean up disconnected players
    for p in PlayersRemoved() do
        players[p] = nil
    end

    -- PHASE 3: Process each active player
    for p in Players() do
        server.tickPlayer(p, dt)
    end
end
```

### server.tickPlayer(p, dt) - Authoritative Game Logic
Server handles: damage, ammo, shooting, scoring, physics mutations.
```lua
function server.tickPlayer(p, dt)
    if GetPlayerTool(p) ~= "toolid" then return end
    local data = players[p]

    if InputDown("usetool", p) and GetPlayerVehicle(p) == 0 then
        -- Authoritative logic: shooting, damage, ammo
        Shoot(pos, dir, "bullet", damage, force, p, "toolid")
        SetToolAmmo("toolid", ammo - 1, p)
    end
end
```

### client.init() - Load Audio/Visual Resources
```lua
function client.init()
    snd = LoadSound("MOD/snd/sound.ogg")
    loopSnd = LoadLoop("MOD/snd/loop.ogg")
end
```

### client.tick(dt) - MANDATORY Three-Phase Pattern (mirrors server)
```lua
function client.tick(dt)
    for p in PlayersAdded() do
        players[p] = createPlayerData()
    end
    for p in PlayersRemoved() do
        players[p] = nil
    end
    for p in Players() do
        client.tickPlayer(p, dt)
    end
end
```

### client.tickPlayer(p, dt) - Visual/Audio Effects
Client handles: sounds, particles, animations, tool transforms, barrel rotation.
Client REPLICATES server state calculations locally for smooth visuals.
```lua
function client.tickPlayer(p, dt)
    if GetPlayerTool(p) ~= "toolid" then return end
    local pt = GetPlayerTransform(p)
    local data = players[p]

    if InputDown("usetool", p) and GetPlayerVehicle(p) == 0 then
        -- Visual effects: sound, particles, light
        PlaySound(snd, pt.pos)
        PointLight(pos, 1, 0.7, 0.5, 3)
        SpawnParticle(pos, vel, lifetime)
    end

    -- Tool body animation
    local b = GetToolBody(p)
    -- Barrel rotation, shape animation, etc.
end
```

### client.draw() or draw() - UI Overlay
```lua
function draw()
    -- Note: draw() works in v2, no need for client.draw()
    -- Ui* functions ONLY go here
    UiPush()
    UiText("info")
    UiPop()
end
```

## API CHANGES FROM V1 TO V2

### Input
- `InputDown("lmb")` → `InputDown("usetool", p)` (with player ID)
- `InputDown("rmb")` → `InputDown("alttool", p)`
- `InputPressed("lmb")` → `InputPressed("usetool", p)`
- `InputReleased("lmb")` → `InputReleased("usetool", p)`
- Other keys like "ctrl", "shift", "space" keep their names but add player ID: `InputDown("ctrl", p)`

### Player Functions (ALL require player ID now)
- `GetPlayerTransform()` → `GetPlayerTransform(p)`
- `GetPlayerVelocity()` → `GetPlayerVelocity(p)`
- `SetPlayerVelocity(vel)` → `SetPlayerVelocity(vel, p)` (NOTE: vel first, then p)
- `GetPlayerVehicle()` → `GetPlayerVehicle(p)`
- `GetPlayerHealth()` → `GetPlayerHealth(p)`
- `SetPlayerHealth(h)` → `SetPlayerHealth(p, h)` (NOTE: p first)
- `GetCameraTransform()` → `GetPlayerCameraTransform(p)` or `GetPlayerEyeTransform(p)`

### Tool Functions (ALL require player ID)
- `GetToolBody()` → `GetToolBody(p)`
- `SetToolTransform(t)` → `SetToolTransform(t, 1.0, p)`
- `GetString("game.player.tool")` → `GetPlayerTool(p)`

### Tool Registration
- `SetBool("game.tool.X.enabled", true)` → `SetToolEnabled("X", true, p)` in server.tick PlayersAdded loop
- `SetFloat("game.tool.X.ammo", n)` → `SetToolAmmo("X", n, p)` in server.tick PlayersAdded loop

### Deprecated
- `GetPlayerRigTransform()` → `GetPlayerRigWorldTransform(p)`
- `handle > 0` → `handle ~= 0` (negative handles exist in v2)

## CRITICAL RULES
1. ALL per-player state MUST be in the players[p] table, NOT global variables
2. Server.tick and client.tick MUST have the PlayersAdded/PlayersRemoved/Players three-phase loop
3. Server handles authoritative logic (shooting, damage, ammo, scoring)
4. Client handles visual feedback (sound, particles, light, animations)
5. Client should REPLICATE server calculations locally for smooth visual prediction
6. Helper functions (deepcopy, utility math, etc.) stay as global functions - they're fine
7. The `options.lua` file should NOT be modified (it uses a special draw() callback for the options menu)
8. If the mod uses custom projectile systems (raycasts, MakeHole, etc.), keep that on the server side
9. Use `IsPlayerLocal(p)` to guard local-only effects (haptics, camera shake)

## OUTPUT FORMAT
Return ONLY the rewritten Lua code. No explanations, no markdown fences, no comments about what you changed.
If the file is `options.lua`, return it UNCHANGED (just add #version 2 at top).
"""


def build_prompt(source: str, analysis: dict, mod_info: dict | None = None) -> str:
    """Build the user prompt for Claude with full context."""
    mod_name = ""
    tool_id = ""
    if mod_info:
        mod_name = mod_info.get("name", "")
        tool_id = mod_info.get("tool_id", "")

    # Try to detect tool ID from RegisterTool call
    if not tool_id:
        import re
        match = re.search(r'RegisterTool\s*\(\s*"([^"]+)"', source)
        if match:
            tool_id = match.group(1)

    filename = analysis.get("file", "main.lua")

    prompt = f"""Rewrite this Teardown v1 mod script to v2 multiplayer format.

Mod: {mod_name}
File: {filename}
Tool ID: {tool_id or "(detect from RegisterTool call)"}

IMPORTANT: This is a COMPLETE rewrite following the v2 architecture in your system prompt.
- Convert ALL global state to per-player tables
- Add the PlayersAdded/PlayersRemoved/Players three-phase loops
- Split logic between server (authoritative) and client (visual)
- Update ALL API calls to v2 signatures with player IDs

Original v1 source:
```lua
{source}
```

Return ONLY the complete rewritten v2 Lua code."""

    return prompt


def _call_claude(system: str, prompt: str, max_tokens: int = 16384) -> str:
    """Call Claude API with retry logic."""
    client = anthropic.Anthropic()
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                temperature=0,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except anthropic.RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise
        except anthropic.APIError:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise


def _cache_key(source: str, analysis: dict) -> str:
    """Generate cache key from source + analysis."""
    h = hashlib.sha256()
    h.update(source.encode())
    h.update(json.dumps(analysis, sort_keys=True).encode())
    # Include a version tag so cache invalidates when we change the prompt
    h.update(b"v2-rewrite-2026-03-16")
    return h.hexdigest()


def rewrite_script_ai(
    source: str,
    analysis: dict,
    cache_dir: Path | None = None,
    mod_info: dict | None = None,
) -> str:
    """Rewrite a script using Claude AI with full v2 architecture reference."""
    # Check cache
    if cache_dir:
        key = _cache_key(source, analysis)
        cache_file = cache_dir / f"{key}.lua"
        if cache_file.exists():
            return cache_file.read_text(encoding="utf-8")

    # Handle options.lua specially - just add version header
    filename = analysis.get("file", "")
    if filename.endswith("options.lua"):
        result = "#version 2\n\n" + source
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_file = cache_dir / f"{_cache_key(source, analysis)}.lua"
            cache_file.write_text(result, encoding="utf-8")
        return result

    prompt = build_prompt(source, analysis, mod_info)

    # Scale max_tokens based on source length
    source_lines = len(source.splitlines())
    max_tokens = min(32000, max(8192, source_lines * 30))

    result = _call_claude(SYSTEM_PROMPT, prompt, max_tokens=max_tokens)

    # Strip markdown fences if present
    if result.startswith("```"):
        lines = result.splitlines()
        if lines[-1].strip() == "```":
            result = "\n".join(lines[1:-1])
        else:
            result = "\n".join(lines[1:])

    # Ensure #version 2 header
    if not result.strip().startswith("#version 2"):
        result = "#version 2\n\n" + result

    # Save to cache
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f"{_cache_key(source, analysis)}.lua"
        cache_file.write_text(result, encoding="utf-8")

    return result
