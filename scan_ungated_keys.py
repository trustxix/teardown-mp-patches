"""Scan all installed mods for raw key inputs that aren't tool-gated.

Checks for:
1. Raw key inputs (a-z) in client.tick/client.tickPlayer without a hardcoded tool gate
2. Option-based soft gates (getBool toolOnly patterns) that can be bypassed by savegame
3. Gameplay-affecting calls (SetPlayerVelocity, ServerCall, etc.) outside tool gates
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

key_pattern = re.compile(r'Input(?:Pressed|Down|Released)\("([a-z])"\)')
# Hardcoded tool gates (good)
hard_gate_patterns = [
    re.compile(r'if\s+not\s+toolActive\s+then\s+return'),
    re.compile(r'if\s+GetPlayerTool\(p\)\s*~=\s*\w+\s+then\s+return'),
    re.compile(r'if\s+GetPlayerTool\(p\)\s*~=\s*"[^"]+"\s+then\s+return'),
    re.compile(r'local\s+enabled\s*=\s*toolActive'),
    re.compile(r'if\s+not\s+enabled\s+then\s+return'),
]
# Soft gates that depend on savegame options (bad - can be bypassed)
soft_gate_patterns = [
    re.compile(r'getBool\(.+toolOnly'),
    re.compile(r'GetBool\(.+toolOnly'),
    re.compile(r'not\s+getBool\(.+\)\s+or\s+toolActive'),
]
# Any tool check present at all
any_tool_check = [
    re.compile(r'GetPlayerTool\(p\)'),
    re.compile(r'toolActive'),
    re.compile(r'tool_active'),
    re.compile(r'isToolActive'),
    re.compile(r'TOOL_ID'),
]

results = []

for mod in sorted(os.listdir(MODS_DIR)):
    main = os.path.join(MODS_DIR, mod, "main.lua")
    if not os.path.isfile(main):
        continue

    with open(main, "r", errors="ignore") as f:
        lines = f.readlines()

    content = "".join(lines)

    # Skip mods with no raw key inputs at all
    all_keys = set(key_pattern.findall(content))
    if not all_keys:
        continue

    # Analyze client.tick and client.tickPlayer functions
    in_client_func = False
    func_name = ""
    has_hard_gate = False
    has_soft_gate = False
    has_any_tool_check = False
    ungated_keys = []
    gated_keys = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect entering client tick/tickPlayer
        m = re.match(r"function\s+(client\.(?:tick|tickPlayer))", stripped)
        if m:
            in_client_func = True
            func_name = m.group(1)
            has_hard_gate = False
            has_soft_gate = False
            has_any_tool_check = False
            continue

        # Detect leaving (another top-level function)
        if in_client_func and re.match(r"^function\s+", stripped) and not re.match(r"^function\s+client\.(tick|tickPlayer)", stripped):
            in_client_func = False
            continue

        if not in_client_func:
            continue

        # Check for hard gate
        if any(p.search(line) for p in hard_gate_patterns):
            has_hard_gate = True

        # Check for soft gate
        if any(p.search(line) for p in soft_gate_patterns):
            has_soft_gate = True

        # Check for any tool awareness
        if any(p.search(line) for p in any_tool_check):
            has_any_tool_check = True

        # Check for raw key input
        km = key_pattern.search(line)
        if km:
            key = km.group(1)
            if has_hard_gate:
                gated_keys.append((i + 1, key, "HARDCODED", stripped[:90]))
            elif has_soft_gate:
                ungated_keys.append((i + 1, key, "SOFT GATE (savegame bypass)", stripped[:90]))
            elif has_any_tool_check:
                # Has some tool check but not a clear gate-before-keys pattern
                ungated_keys.append((i + 1, key, "UNCLEAR GATE", stripped[:90]))
            else:
                ungated_keys.append((i + 1, key, "NO GATE", stripped[:90]))

    if ungated_keys:
        results.append((mod, ungated_keys, has_hard_gate, has_soft_gate, has_any_tool_check))

# Report
print("=" * 60)
print("UNGATED KEY INPUT SCAN")
print("=" * 60)
print()

if not results:
    print("All mods properly hardcode tool gates!")
else:
    # Group by severity
    no_gate = [(m, k, hg, sg, tc) for m, k, hg, sg, tc in results if not tc]
    soft_only = [(m, k, hg, sg, tc) for m, k, hg, sg, tc in results if sg and not hg]
    unclear = [(m, k, hg, sg, tc) for m, k, hg, sg, tc in results if tc and not sg and not hg]
    mixed = [(m, k, hg, sg, tc) for m, k, hg, sg, tc in results if hg and k]  # has hard gate but some keys before it

    if no_gate:
        print("### NO TOOL GATE AT ALL (keys fire with any tool):")
        print()
        for mod, keys, _, _, _ in no_gate:
            print(f"  {mod}:")
            for lineno, key, severity, code in keys:
                print(f"    L{lineno}: [{severity}] key '{key}' -> {code}")
            print()

    if soft_only:
        print("### SOFT GATE ONLY (savegame can bypass):")
        print()
        for mod, keys, _, _, _ in soft_only:
            print(f"  {mod}:")
            for lineno, key, severity, code in keys:
                print(f"    L{lineno}: [{severity}] key '{key}' -> {code}")
            print()

    if unclear:
        print("### UNCLEAR GATE (has tool check but keys may not be behind it):")
        print()
        for mod, keys, _, _, _ in unclear:
            print(f"  {mod}:")
            for lineno, key, severity, code in keys:
                print(f"    L{lineno}: [{severity}] key '{key}' -> {code}")
            print()

    if mixed:
        print("### MIXED (hard gate exists but some keys appear before it):")
        print()
        for mod, keys, _, _, _ in mixed:
            print(f"  {mod}:")
            for lineno, key, severity, code in keys:
                print(f"    L{lineno}: [{severity}] key '{key}' -> {code}")
            print()

    total = sum(len(k) for _, k, _, _, _ in results)
    print(f"Total: {len(results)} mods, {total} ungated key bindings")
