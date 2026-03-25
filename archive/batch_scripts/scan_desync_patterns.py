"""Scan all mods for the 5 desync/performance patterns found in Bunker Buster.

Categories:
  SAFE    - Can be auto-fixed without affecting functionality
  REVIEW  - Fix could affect gameplay/visuals, needs manual inspection
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

results = {}

def add(mod, pattern_id, severity, detail, file="main.lua"):
    if mod not in results:
        results[mod] = []
    results[mod].append((pattern_id, severity, detail, file))

for mod in sorted(os.listdir(MODS_DIR)):
    mod_dir = os.path.join(MODS_DIR, mod)
    if not os.path.isdir(mod_dir):
        continue

    for root, dirs, files in os.walk(mod_dir):
        for fname in files:
            if not fname.endswith(".lua"):
                continue
            filepath = os.path.join(root, fname)
            relpath = os.path.relpath(filepath, MODS_DIR)

            with open(filepath, "r", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")

            # ── Pattern 1: shared table that grows unbounded ──
            # Look for table.insert or [#t+1] on shared.* without any cleanup
            shared_appends = re.findall(
                r'shared\.(\w+)\[#shared\.\w+\s*\+\s*1\]|table\.insert\(shared\.(\w+)',
                content
            )
            if shared_appends:
                # Check if there's any cleanup (table.remove, = nil, = {})
                tables = set(t[0] or t[1] for t in shared_appends)
                for tbl in tables:
                    has_cleanup = bool(re.search(
                        rf'table\.remove\(shared\.{tbl}|shared\.{tbl}\s*=\s*\{{|shared\.{tbl}\[\w+\]\s*=\s*nil',
                        content
                    ))
                    if not has_cleanup:
                        add(mod, "P1-SHARED-BLOAT", "SAFE",
                            f"shared.{tbl} appended to but never cleaned up", relpath)

            # Also check for shared[key] = value patterns that accumulate (dict-style)
            shared_dict_writes = re.findall(
                r'shared\.(\w+)\[(\w+)\]\s*=\s*\{', content
            )
            if shared_dict_writes:
                for tbl, key in shared_dict_writes:
                    # Skip if it's a fixed key (not dynamic)
                    if key in ('true', 'false', '1', '2', '3'):
                        continue
                    has_cleanup = bool(re.search(
                        rf'shared\.{tbl}\[\w+\]\s*=\s*nil', content
                    ))
                    if not has_cleanup:
                        add(mod, "P1-SHARED-BLOAT", "REVIEW",
                            f"shared.{tbl}[{key}] written dynamically, no cleanup found", relpath)

            # ── Pattern 2: Raycast in client.update but input in client.tick ──
            in_update = False
            in_tick = False
            has_raycast_in_update = False
            has_input_in_tick = False
            update_raycast_line = 0

            for i, line in enumerate(lines):
                if re.match(r"function\s+client\.update", line):
                    in_update = True
                    in_tick = False
                elif re.match(r"function\s+client\.tick", line):
                    in_tick = True
                    in_update = False
                elif re.match(r"function\s+\w", line) and not re.match(r"function\s+client\.(update|tick)", line):
                    in_update = False
                    in_tick = False

                if in_update and re.search(r"QueryRaycast", line):
                    has_raycast_in_update = True
                    update_raycast_line = i + 1
                if in_tick and re.search(r'InputPressed\("usetool"', line):
                    has_input_in_tick = True

            if has_raycast_in_update and has_input_in_tick:
                add(mod, "P2-STALE-AIM", "REVIEW",
                    f"QueryRaycast in client.update (L{update_raycast_line}) but InputPressed(usetool) in client.tick — aim may be 1 frame stale at >60fps",
                    relpath)

            # ── Pattern 3: Multiple GetString("game.player.tool") calls ──
            tool_calls = [
                (i+1, line.strip()) for i, line in enumerate(lines)
                if re.search(r'GetString\("game\.player\.tool"\)', line)
            ]
            if len(tool_calls) >= 3:
                # Check if it's in one function or spread across many
                add(mod, "P3-REDUNDANT-TOOL-CHECK", "SAFE",
                    f'{len(tool_calls)} calls to GetString("game.player.tool") — cache in local variable',
                    relpath)

            # ── Pattern 4: v1 fallback loop (for id = 1, N) ──
            v1_loops = re.findall(r'for\s+\w+\s*=\s*1\s*,\s*(\d+)\s+do', content)
            for limit in v1_loops:
                if int(limit) >= 16:  # 16+ suggests player iteration
                    line_num = 0
                    for i, line in enumerate(lines):
                        if re.search(rf'for\s+\w+\s*=\s*1\s*,\s*{limit}\s+do', line):
                            line_num = i + 1
                            break
                    # Verify it's actually iterating players (has GetPlayerTool or similar nearby)
                    context = content[max(0, content.find(f"= 1, {limit}") - 200):
                                      content.find(f"= 1, {limit}") + 500]
                    if re.search(r'GetPlayerTool|GetPlayerTransform|IsPlayerLocal|GetPlayerPos', context):
                        add(mod, "P4-V1-FALLBACK", "SAFE",
                            f"for id = 1, {limit} player iteration loop (L{line_num}) — use Players() iterator instead",
                            relpath)

            # Also check for type(Players) == "function" guard
            if 'type(Players) == "function"' in content or "type(Players)==" in content:
                add(mod, "P4-V1-FALLBACK", "SAFE",
                    'type(Players) == "function" guard — unnecessary in v2, Players() always exists',
                    relpath)

            # ── Pattern 5: Per-tick ServerCall/ClientCall (continuous state) ──
            # Already tracked by lint (PER-TICK-RPC), but check for specific patterns
            # that are clearly continuous (inside a for p in Players() loop in tick/update)
            in_players_loop = False
            in_tick_or_update = False

            for i, line in enumerate(lines):
                stripped = line.strip()
                if re.match(r"function\s+client\.(tick|update|tickPlayer)|function\s+server\.(tick|update|tickPlayer)", stripped):
                    in_tick_or_update = True
                elif re.match(r"function\s+", stripped):
                    in_tick_or_update = False
                    in_players_loop = False

                if in_tick_or_update and re.search(r'for\s+\w+\s+in\s+Players\(\)', stripped):
                    in_players_loop = True

                if in_tick_or_update and in_players_loop:
                    # ServerCall/ClientCall inside Players() loop in tick = per-tick RPC
                    if re.search(r'ServerCall\(|ClientCall\(', stripped):
                        # Skip if it's already annotated as ok
                        if '@lint-ok PER-TICK-RPC' not in line:
                            add(mod, "P5-PER-TICK-RPC", "REVIEW",
                                f"RPC inside Players() loop in tick/update (L{i+1}): {stripped[:80]}",
                                relpath)

# ── Report ──
print("=" * 70)
print("DESYNC PATTERN SCAN — All 125 Mods")
print("=" * 70)
print()

safe_fixes = {}
review_fixes = {}
for mod, findings in sorted(results.items()):
    for pid, sev, detail, fp in findings:
        if sev == "SAFE":
            safe_fixes.setdefault(pid, []).append((mod, detail, fp))
        else:
            review_fixes.setdefault(pid, []).append((mod, detail, fp))

print("### SAFE TO AUTO-FIX (won't affect functionality):\n")
for pid in sorted(safe_fixes.keys()):
    items = safe_fixes[pid]
    desc = {
        "P1-SHARED-BLOAT": "shared table grows unbounded — add cleanup",
        "P3-REDUNDANT-TOOL-CHECK": "multiple GetString tool checks — cache in variable",
        "P4-V1-FALLBACK": "v1 player iteration fallback — use Players()",
    }
    print(f"  {pid}: {desc.get(pid, pid)}")
    for mod, detail, fp in items:
        print(f"    {mod} ({fp}): {detail}")
    print()

print()
print("### NEEDS MANUAL REVIEW (fix could affect behavior):\n")
for pid in sorted(review_fixes.keys()):
    items = review_fixes[pid]
    desc = {
        "P1-SHARED-BLOAT": "shared table may grow — verify cleanup exists elsewhere",
        "P2-STALE-AIM": "aim raycast in update (60Hz) + input in tick — may cause aim drift",
        "P5-PER-TICK-RPC": "RPC called every tick — should use registry sync instead",
    }
    print(f"  {pid}: {desc.get(pid, pid)}")
    for mod, detail, fp in items:
        print(f"    {mod} ({fp}): {detail}")
    print()

# Summary
total_safe = sum(len(v) for v in safe_fixes.values())
total_review = sum(len(v) for v in review_fixes.values())
mods_affected = len(results)
print(f"\nSummary: {mods_affected} mods affected, {total_safe} safe fixes, {total_review} need review")
