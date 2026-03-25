"""Remove recoil SetToolTransform overrides that cause tools to float.

The recoil block (modifying offset.pos with recoilTimer Z push + calling SetToolTransform
a second time) causes the tool body to clip into the player and float away.

Fix: remove the second SetToolTransform call inside the recoilTimer block.
Keep the first (base position) SetToolTransform call.
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

fixed = 0

for mod in sorted(os.listdir(MODS_DIR)):
    main = os.path.join(MODS_DIR, mod, "main.lua")
    if not os.path.isfile(main):
        continue
    with open(main, "r", errors="ignore") as f:
        content = f.read()

    if "recoilTimer" not in content or "SetToolTransform" not in content:
        continue
    if content.count("SetToolTransform") < 2:
        continue

    original = content
    lines = content.split("\n")
    new_lines = []
    skip_block = False
    brace_depth = 0
    in_recoil_block = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Detect start of recoil block
        if re.match(r'\s*if\s+data\.recoilTimer\s*[~>!=]+\s*0\s+then', stripped):
            # Look ahead: does this block contain SetToolTransform?
            block_lines = []
            j = i
            depth = 1
            while j + 1 < len(lines) and depth > 0:
                j += 1
                s = lines[j].strip()
                block_lines.append(lines[j])
                if s.startswith("if ") and s.endswith("then"):
                    depth += 1
                if s == "end":
                    depth -= 1

            block_text = "\n".join(block_lines)
            has_stt = "SetToolTransform" in block_text

            if has_stt:
                # Skip this entire block (recoil SetToolTransform override)
                # But keep the recoilTimer decrement
                new_lines.append(line.replace(stripped, "-- Recoil visual removed (prevents tool floating)"))
                # Find and keep only the timer decrement line
                for bl in block_lines:
                    bs = bl.strip()
                    if "recoilTimer" in bs and "-" in bs and "dt" in bs:
                        # Keep timer decrement but clamp to 0
                        indent = bl[:len(bl) - len(bl.lstrip())]
                        new_lines.append(bl)
                        new_lines.append(indent + "if data.recoilTimer < 0 then data.recoilTimer = 0 end")
                    elif bs == "end":
                        pass  # skip the closing end
                    # Skip everything else in the block
                i = j + 1  # Skip past the block
                continue
            else:
                # Recoil block without SetToolTransform — keep it
                new_lines.append(line)
                i += 1
                continue
        else:
            new_lines.append(line)
            i += 1

    content = "\n".join(new_lines)

    if content != original:
        with open(main, "w") as f:
            f.write(content)
        fixed += 1
        print(f"  FIXED {mod}")

print(f"\nFixed: {fixed}")
