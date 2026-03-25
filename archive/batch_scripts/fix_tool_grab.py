"""Add ReleasePlayerGrab(p) to all tool mods."""
import os

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

fixed = 0
skipped = 0

for mod in sorted(os.listdir(MODS_DIR)):
    main = os.path.join(MODS_DIR, mod, "main.lua")
    if not os.path.isfile(main):
        continue
    with open(main, "r", errors="ignore") as f:
        lines = f.readlines()

    content = "".join(lines)
    if "ReleasePlayerGrab" in content:
        continue
    if "SetToolTransform" not in content:
        continue
    if "RegisterTool" not in content:
        continue

    # Find server.tickPlayer gate: look for the return-end after tool check
    inserted = False
    new_lines = []
    in_tickPlayer = False
    found_gate_return = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        stripped = line.strip()

        if "function server.tickPlayer(p" in stripped:
            in_tickPlayer = True
            found_gate_return = False
            continue

        if in_tickPlayer and not found_gate_return:
            # Look for "return" followed by "end" (the gate block)
            if stripped == "return":
                # Check if next non-empty line is "end"
                for j in range(i + 1, min(i + 3, len(lines))):
                    if lines[j].strip() == "end":
                        # Found the gate. Insert after the "end" line
                        # We'll insert when we process that "end" line
                        found_gate_return = True
                        break
            # Single-line gate: if ... then return end
            elif "then return end" in stripped and "GetPlayerTool" in stripped:
                new_lines.append("\tReleasePlayerGrab(p)\n")
                inserted = True
                in_tickPlayer = False

        if in_tickPlayer and found_gate_return and stripped == "end":
            new_lines.append("\n\tReleasePlayerGrab(p)\n")
            inserted = True
            in_tickPlayer = False

    if inserted:
        with open(main, "w") as f:
            f.writelines(new_lines)
        fixed += 1
        print(f"  FIXED {mod}")
    else:
        skipped += 1
        print(f"  SKIP {mod}")

print(f"\nFixed: {fixed}, Skipped: {skipped}")
