"""
Issue #68 minimal entity script v2 converter.
Applies the established conversion pattern to entity scripts:
  1. Add #version 2 at top
  2. init() → server.init()
  3. tick(dt) → server.tick(dt)  (also tick() without dt)
  4. update(dt) → server.update(dt)
  5. draw() → client.draw()
  6. mousedx → camerax, mousedy → cameray
  7. Add client.init() end at bottom

Usage: python tools/entity_v2_convert.py <file1> [file2] ...
       python tools/entity_v2_convert.py --dry-run <file1> ...
"""
import sys
import re
import os

DRY_RUN = "--dry-run" in sys.argv
FILE_LIST = None
for arg in sys.argv[1:]:
    if arg.startswith("--file-list="):
        FILE_LIST = arg.split("=", 1)[1]

if FILE_LIST:
    with open(FILE_LIST, 'r') as f:
        files = [line.strip() for line in f if line.strip()]
else:
    files = [f for f in sys.argv[1:] if not f.startswith("--")]

if not files:
    print("Usage: python tools/entity_v2_convert.py [--dry-run] [--file-list=file.txt] <file1> [file2] ...")
    sys.exit(1)

# Patterns to replace (only exact v1 callback signatures)
REPLACEMENTS = [
    (re.compile(r'^(function\s+)init\s*\(\s*\)', re.MULTILINE), r'\1server.init()'),
    (re.compile(r'^(function\s+)tick\s*\(\s*dt\s*\)', re.MULTILINE), r'\1server.tick(dt)'),
    (re.compile(r'^(function\s+)tick\s*\(\s*\)', re.MULTILINE), r'\1server.tick()'),
    (re.compile(r'^(function\s+)update\s*\(\s*dt\s*\)', re.MULTILINE), r'\1server.update(dt)'),
    (re.compile(r'^(function\s+)draw\s*\(\s*\)', re.MULTILINE), r'\1client.draw()'),
    (re.compile(r'^(function\s+)draw\s*\(\s*dt\s*\)', re.MULTILINE), r'\1client.draw(dt)'),
    # mousedx/mousedy → camerax/cameray (in string literals)
    (re.compile(r'"mousedx"'), '"camerax"'),
    (re.compile(r'"mousedy"'), '"cameray"'),
]

converted = 0
skipped = 0
errors = 0

for filepath in files:
    if not os.path.isfile(filepath):
        print(f"  SKIP (not found): {filepath}")
        skipped += 1
        continue

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Skip if already has #version 2
    if '#version 2' in content:
        print(f"  SKIP (already v2): {filepath}")
        skipped += 1
        continue

    original = content
    changes = []

    # Apply replacements
    for pattern, replacement in REPLACEMENTS:
        new_content = pattern.sub(replacement, content)
        if new_content != content:
            # Find what changed
            matches = pattern.findall(content)
            changes.append(f"{pattern.pattern.strip()} -> {replacement}")
            content = new_content

    # Add #version 2 at top
    content = "#version 2\n" + content
    changes.append("Added #version 2")

    # Add client.init() at bottom if not already present
    if 'client.init' not in content:
        content = content.rstrip() + "\n\nfunction client.init() end\n"
        changes.append("Added client.init()")

    if content == original:
        print(f"  SKIP (no changes): {filepath}")
        skipped += 1
        continue

    if DRY_RUN:
        print(f"  DRY-RUN: {filepath}")
        for c in changes:
            print(f"    - {c}")
        converted += 1
    else:
        try:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            print(f"  CONVERTED: {filepath}")
            for c in changes:
                print(f"    - {c}")
            converted += 1
        except Exception as e:
            print(f"  ERROR: {filepath}: {e}")
            errors += 1

print(f"\nSummary: {converted} converted, {skipped} skipped, {errors} errors")
