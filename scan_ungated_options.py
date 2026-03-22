"""Find all mods where pressing O opens an options menu without checking the active tool."""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

# Patterns that indicate a tool gate exists before the O key check
gate_patterns = [
    # Direct tool checks
    r'GetPlayerTool\(p?\)\s*[=~!]=',
    r'GetPlayerTool\(\w+\)\s*[=~!]=',
    r'toolActive',
    r'tool_active',
    r'hasTool',
    r'currentTool\s*==',
    r'currentTool\s*~=',
    # Early return if wrong tool
    r'if\s+not\s+toolActive\s+then\s+return',
    r'if\s+GetPlayerTool.*~=.*then\s+return',
    r'if\s+GetPlayerTool.*~=.*then\n\s*return',
]

results = []

for mod in sorted(os.listdir(MODS_DIR)):
    mod_dir = os.path.join(MODS_DIR, mod)
    if not os.path.isdir(mod_dir):
        continue

    # Check all lua files in the mod
    for root, dirs, files in os.walk(mod_dir):
        for fname in files:
            if not fname.endswith(".lua"):
                continue
            filepath = os.path.join(root, fname)
            relpath = os.path.relpath(filepath, MODS_DIR)

            with open(filepath, "r", errors="ignore") as f:
                lines = f.readlines()

            content = "".join(lines)

            # Find InputPressed("o") occurrences
            o_lines = []
            for i, line in enumerate(lines):
                if re.search(r'InputPressed\("o"\)', line):
                    o_lines.append((i + 1, line.strip()))

            if not o_lines:
                continue

            # For each O key press, check if it's gated
            for lineno, code in o_lines:
                # Look backwards from this line to find the enclosing function
                gated = False
                func_name = "unknown"

                for j in range(lineno - 2, max(0, lineno - 80), -1):
                    check_line = lines[j] if j < len(lines) else ""

                    # Find function declaration
                    fm = re.match(r"function\s+(\S+)", check_line.strip())
                    if fm:
                        func_name = fm.group(1)

                    # Check for gate patterns between function start and O key
                    for pat in gate_patterns:
                        if re.search(pat, check_line):
                            gated = True
                            break
                    if gated:
                        break

                    # Also check for wrapping if blocks with tool checks
                    if re.search(r'if.*GetPlayerTool.*==.*then', check_line):
                        gated = True
                        break
                    if re.search(r'if.*GetPlayerTool.*~=.*then', check_line):
                        # Check if it returns (gate) or just does something
                        # Look at next few lines for return
                        for k in range(j + 1, min(j + 4, len(lines))):
                            if "return" in lines[k]:
                                gated = True
                                break
                        if gated:
                            break

                if not gated:
                    results.append((mod, relpath, lineno, func_name, code))

print("=" * 70)
print("UNGATED OPTIONS MENU (O KEY) SCAN")
print("=" * 70)
print()

if not results:
    print("All O key handlers are properly tool-gated!")
else:
    print(f"Found {len(results)} ungated O key handlers:\n")
    for mod, relpath, lineno, func_name, code in results:
        print(f"  {mod}")
        print(f"    File: {relpath}:{lineno}")
        print(f"    In:   {func_name}")
        print(f"    Code: {code[:90]}")
        print()
