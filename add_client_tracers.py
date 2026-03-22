"""Add client-side tracer rendering to all gun mods missing it.

Pattern:
1. Add clientTracers={} to createPlayerData
2. In client.tickPlayer shooting block, create tracer after muzzle flash
3. Add tracer update+DrawLine before SetToolTransform
"""
import os
import re

MODS_DIR = r"C:\Users\trust\Documents\Teardown\mods"

# Mod configs: (name, muzzle_offset, velocity, is_semi_auto)
MODS = {
    "AK-47":          {"muzzle": "Vec(0.275, -0.6, -2.6)", "vel": "1.5"},
    "AWP":            {"muzzle": "Vec(0.2, -0.7, -3.2)",   "vel": "2.0"},
    "Desert_Eagle":   {"muzzle": "Vec(0.2, -0.5, -1.5)",   "vel": "1.5"},
    "Dual_Berettas":  {"muzzle": "Vec(0, 0, -2)",          "vel": "1.5"},
    "Dual_Miniguns":  {"muzzle": "Vec(0, -0.7, -2)",       "vel": "1.5"},
    "M1_Garand":      {"muzzle": "Vec(0.35, -0.6, -2.6)",  "vel": "1.7"},
    "M249":           {"muzzle": "Vec(0.275, -0.6, -2.6)", "vel": "1.5"},
    "M4A1":           {"muzzle": "Vec(0.275, -0.6, -2.6)", "vel": "1.5"},
    "Minigun":        {"muzzle": "Vec(0.15, -0.7, -2.6)",  "vel": "1.5"},
    "Nova_Shotgun":   {"muzzle": "Vec(0.2, -0.5, -2)",     "vel": "1.5"},
    "SCAR-20":        {"muzzle": "Vec(0.2, -0.6, -2.6)",   "vel": "2.0"},
    "Hook_Shotgun":   {"muzzle": "Vec(0.35, -0.6, -2.1)",  "vel": "1.5"},
    "Attack_Drone":   {"muzzle": "Vec(0, -0.3, -1.5)",     "vel": "1.5"},
}

fixed = 0

for mod, cfg in sorted(MODS.items()):
    main = os.path.join(MODS_DIR, mod, "main.lua")
    if not os.path.isfile(main):
        print(f"  SKIP {mod}: not found")
        continue
    with open(main, "r", errors="ignore") as f:
        content = f.read()

    if "clientTracers" in content:
        print(f"  SKIP {mod}: already has tracers")
        continue

    original = content

    # 1. Add clientTracers to createPlayerData
    # Find optionsOpen = false in createPlayerData and add after it
    content = content.replace(
        "optionsOpen = false,\n",
        "optionsOpen = false,\n\t\tclientTracers = {},\n",
        1
    )

    # 2. Add tracer creation in client.tickPlayer shooting block
    # Find the SpawnParticle("fire"...) line in client.tickPlayer and add tracer after the end of that if block
    # Look for the pattern: SpawnParticle("fire", toolPos, ...) followed by end
    lines = content.split("\n")
    new_lines = []
    in_client_tick = False
    added_tracer_create = False
    added_tracer_render = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if "function client.tickPlayer" in stripped:
            in_client_tick = True

        if in_client_tick and not added_tracer_create:
            # Find SpawnParticle("fire" in shooting block and add tracer after the if b ~= 0 block
            if 'SpawnParticle("fire"' in stripped and "toolPos" in stripped:
                # Found the muzzle flash line. Look for the closing "end" of the if b ~= 0 block
                new_lines.append(line)
                i += 1
                # Keep going until we find the "end" that closes the if b ~= 0 block
                while i < len(lines):
                    new_lines.append(lines[i])
                    if lines[i].strip() == "end":
                        # Add tracer creation after this end
                        indent = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
                        # Go back up to find if we're at the right level
                        # Actually, add it right after this end, before ammo decrement
                        tracer_code = f"""
{indent}-- Create client tracer (local player only)
{indent}if isLocal and b ~= 0 then
{indent}\tlocal toolTrans = GetBodyTransform(b)
{indent}\tlocal muzzlePos = TransformToParentPoint(toolTrans, {cfg['muzzle']})
{indent}\tlocal aimpos, distance = GetAimPos(p)
{indent}\tif distance and distance > 0 then
{indent}\t\tlocal dir = VecSub(aimpos, muzzlePos)
{indent}\t\tlocal spread = math.min(data.spreadTimer or 0, 4) * distance / 100
{indent}\t\tdir[1] = dir[1] + (math.random() - 0.5) * 2 * spread
{indent}\t\tdir[2] = dir[2] + (math.random() - 0.5) * 2 * spread
{indent}\t\tdir[3] = dir[3] + (math.random() - 0.5) * 2 * spread
{indent}\t\tdata.clientTracers[#data.clientTracers + 1] = {{
{indent}\t\t\tpos = VecCopy(muzzlePos),
{indent}\t\t\tvel = VecScale(dir, {cfg['vel']} * (100 / distance)),
{indent}\t\t\tlife = 0.3,
{indent}\t\t}}
{indent}\tend
{indent}end"""
                        new_lines.append(tracer_code)
                        added_tracer_create = True
                        i += 1
                        break
                    i += 1
                continue

        if in_client_tick and not added_tracer_render:
            # Find SetToolTransform and add tracer rendering before it
            if "SetToolTransform" in stripped and "Transform" in stripped:
                indent = line[:len(line) - len(line.lstrip())]
                # Go back to find "local b = GetToolBody(p)" — add tracer rendering before that block
                # Actually, insert tracer rendering right before this line's parent block
                tracer_render = f"""
{indent}-- Client tracers (local player only)
{indent}if isLocal then
{indent}\tfor ti = #data.clientTracers, 1, -1 do
{indent}\t\tlocal tr = data.clientTracers[ti]
{indent}\t\tlocal prevPos = VecCopy(tr.pos)
{indent}\t\ttr.vel = VecAdd(tr.vel, VecScale(Vec(0, -1, 0), dt))
{indent}\t\ttr.pos = VecAdd(tr.pos, VecScale(tr.vel, dt))
{indent}\t\ttr.life = tr.life - dt
{indent}\t\tlocal tdir = VecNormalize(VecSub(tr.pos, prevPos))
{indent}\t\tlocal tdist = VecLength(VecSub(tr.pos, prevPos))
{indent}\t\tlocal thit = QueryRaycast(prevPos, tdir, tdist)
{indent}\t\tif thit or tr.life <= 0 then
{indent}\t\t\ttable.remove(data.clientTracers, ti)
{indent}\t\telse
{indent}\t\t\tDrawLine(prevPos, tr.pos)
{indent}\t\tend
{indent}\tend
{indent}end
"""
                # Find the "local b = GetToolBody" line before SetToolTransform
                # Insert tracer rendering before it
                for j in range(len(new_lines) - 1, max(0, len(new_lines) - 5), -1):
                    if "GetToolBody" in new_lines[j]:
                        new_lines.insert(j, tracer_render)
                        added_tracer_render = True
                        break

                if not added_tracer_render:
                    # Fallback: insert before current line
                    new_lines.append(tracer_render)
                    added_tracer_render = True

        new_lines.append(line)
        i += 1

    content = "\n".join(new_lines)

    if content != original and added_tracer_create and added_tracer_render:
        with open(main, "w") as f:
            f.write(content)
        fixed += 1
        print(f"  FIXED {mod}")
    elif content != original:
        with open(main, "w") as f:
            f.write(content)
        status = f"create={'Y' if added_tracer_create else 'N'} render={'Y' if added_tracer_render else 'N'}"
        print(f"  PARTIAL {mod}: {status}")
        fixed += 1
    else:
        print(f"  NO CHANGE {mod}")

print(f"\nFixed: {fixed}/{len(MODS)}")
