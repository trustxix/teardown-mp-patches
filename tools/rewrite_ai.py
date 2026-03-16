"""Phase 3b: AI-assisted v1→v2 Lua rewriter using Claude API."""

import hashlib
import json
import time
from pathlib import Path

import anthropic

SYSTEM_PROMPT = """You are an expert Teardown modding assistant. Your job is to rewrite Teardown v1 Lua scripts to v2 multiplayer-compatible format.

RULES:
1. Add #version 2 at the top of every script
2. Split all logic into server.* and client.* callbacks:
   - server.init(), server.tick(dt), server.update(dt), server.postUpdate(), server.destroy()
   - client.init(), client.tick(dt), client.update(dt), client.postUpdate(), client.draw(), client.render(dt), client.destroy()
3. Input functions (InputPressed, InputDown, etc.) go in client.tick or client.update
4. All Ui* functions go in client.draw() ONLY (no dt parameter)
5. Player state mutations (SetPlayerHealth, ApplyPlayerDamage, RespawnPlayer) go in server.*
6. Sound/effects (PlaySound, SpawnParticle, SpawnFire) go in client.*
7. Tool registration (RegisterTool) goes in server.init()
8. Replace GetPlayerRigTransform with GetPlayerRigWorldTransform
9. Replace handle > 0 checks with handle ~= 0 (negative handles exist in v2)
10. Add playerId parameter to player functions. Use GetAllPlayers() loop for multi-player support.
11. Registry calls (SetInt, SetFloat, etc.) that store game state should use sync=true third parameter
12. Keep helper functions as-is (they can be called from either server or client context)
13. Module-level local variables stay at the top of the file

OUTPUT: Return ONLY the rewritten Lua code. No explanations, no markdown fences."""


def build_prompt(source: str, analysis: dict) -> str:
    """Build the user prompt for Claude."""
    return f"""Rewrite this Teardown v1 Lua script to v2 multiplayer format.

File: {analysis['file']}
Complexity: {analysis.get('complexity', 'unknown')}

Original source:
```lua
{source}
```

Analysis notes:
{json.dumps(analysis.get('api_calls', []), indent=2)[:2000]}

Rewrite this script following all the rules in your system prompt. Remember:
- Add #version 2 at the top
- Split logic into server.* and client.* callbacks

Return only the rewritten Lua code."""


def _call_claude(system: str, prompt: str) -> str:
    """Call Claude API with retry logic."""
    client = anthropic.Anthropic()
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
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
        except anthropic.APIError as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise


def _cache_key(source: str, analysis: dict) -> str:
    """Generate cache key from source + analysis."""
    h = hashlib.sha256()
    h.update(source.encode())
    h.update(json.dumps(analysis, sort_keys=True).encode())
    return h.hexdigest()


def rewrite_script_ai(
    source: str,
    analysis: dict,
    cache_dir: Path | None = None,
) -> str:
    """Rewrite a script using Claude AI."""
    if cache_dir:
        key = _cache_key(source, analysis)
        cache_file = cache_dir / f"{key}.lua"
        if cache_file.exists():
            return cache_file.read_text(encoding="utf-8")

    prompt = build_prompt(source, analysis)
    result = _call_claude(SYSTEM_PROMPT, prompt)

    # Strip markdown fences if present
    if result.startswith("```"):
        lines = result.splitlines()
        result = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / f"{_cache_key(source, analysis)}.lua"
        cache_file.write_text(result, encoding="utf-8")

    return result
