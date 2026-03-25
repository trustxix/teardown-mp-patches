"""Classify all mods by type, version, and MP status.

Usage:
    python -m tools.classify              # Full table
    python -m tools.classify --json       # JSON output
    python -m tools.classify --summary    # Counts only
"""
import os
import re
import json
import sys
from pathlib import Path
from tools.common import LIVE_MODS_DIR

WORKSHOP_DIR = Path("C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630")

# Built-in game mods to skip
BUILTIN_MODS = {
    "assetpack", "bananabomb", "basic", "castle", "contentgamemodeexample",
    "cratertown", "cullington", "debuginfo", "drivetosurvive", "editorshowcase",
    "evertidesmall", "frustrum", "heistexample", "hollowrockisland",
    "islaestocastica", "jetpack", "lasergun", "leechemicals", "merlin",
    "minigun", "motorpark", "mpclassics", "muratoribeach", "proppack",
    "quilezsecurity", "robotshowcase", "screenrecorder", "scriptingshowcase",
    "simplehouse", "slowmotion", "smokegun", "speedometer", "splitfieldestate",
    "tillaggaryd", "uishowcase", "vehiclebooster", "vehicleikshowcase",
    "vehiclepack", "villagordon", "westpointmarina",
}


def classify_mod(mod_dir: Path) -> dict:
    """Classify a single mod."""
    name = mod_dir.name
    result = {"name": name, "version": "v1", "type": "unknown", "mp_status": "unknown", "has_id": False}

    # Check id.txt (our custom mods have this)
    id_path = mod_dir / "id.txt"
    result["has_id"] = id_path.exists()
    if id_path.exists():
        result["workshop_id"] = id_path.read_text(errors="ignore").strip().split("\n")[0]

    # Check info.txt
    info_path = mod_dir / "info.txt"
    if info_path.exists():
        info = info_path.read_text(errors="ignore")
        if re.search(r"version\s*=\s*2", info):
            result["info_v2"] = True
        tags = re.search(r"tags\s*=\s*(.*)", info, re.IGNORECASE)
        if tags:
            tag_str = tags.group(1).lower()
            if "tool" in tag_str:
                result["type"] = "tool"
            elif "map" in tag_str:
                result["type"] = "map"
            elif "vehicle" in tag_str:
                result["type"] = "vehicle"
            elif "gameplay" in tag_str:
                result["type"] = "gameplay"

    # Check main.lua
    main_path = mod_dir / "main.lua"
    if not main_path.exists():
        result["type"] = result["type"] if result["type"] != "unknown" else "map"
        result["mp_status"] = "content"
        return result

    try:
        source = main_path.read_text(errors="ignore")
    except Exception:
        result["mp_status"] = "error"
        return result

    # Check if it's actually XML (scene file named main.lua)
    if source.strip().startswith("<"):
        result["type"] = result["type"] if result["type"] != "unknown" else "map"
        result["mp_status"] = "content"
        return result

    # Version check
    if "#version 2" in source:
        result["version"] = "v2"
    else:
        result["mp_status"] = "disabled"
        return result

    # Check for actual game logic (not just empty stubs)
    has_server_logic = bool(re.search(r"function server\.\w+\(", source))
    has_client_logic = bool(re.search(r"function client\.\w+\(", source))
    line_count = len(source.splitlines())

    if line_count < 30:
        result["mp_status"] = "content"
        return result

    # Determine type from code patterns
    if result["type"] == "unknown":
        if "RegisterTool" in source:
            result["type"] = "tool"
        elif "level.sandbox" in source or "level.spawn" in source:
            result["type"] = "gameplay"
        elif has_server_logic and has_client_logic:
            result["type"] = "tool"
        else:
            result["type"] = "content"

    # Check for known desync patterns
    issues = []
    if re.search(r'\blocal\s+\w+\s*=', source) and "#version 2" in source:
        # Quick file-scope local check
        depth = 0
        for line in source.splitlines():
            s = line.strip()
            if s.startswith("#") or s.startswith("--") or not s:
                continue
            if depth == 0 and re.match(r"^local\s+\w+\s*=", s):
                issues.append("file-scope-local")
                break
            depth += s.count("function ") + s.count("if ") + s.count("for ") - s.count("end")
            if depth < 0:
                depth = 0

    if re.search(r'InputPressed\s*\(\s*"(lmb|rmb|r|c|v|g|f1|space|shift)".*,', source):
        issues.append("raw-key-player")
    if re.search(r'shared\.\w+.*for\s+\w+\s*=\s*1\s*,\s*\d{3}', source, re.DOTALL):
        issues.append("shared-bomb")
    if "mousedx" not in source and "SetCameraTransform" in source and "camerax" in source:
        issues.append("camerax-setcamera")

    if issues:
        result["mp_status"] = "issues"
        result["issues"] = issues
    else:
        result["mp_status"] = "ok"

    return result


def main():
    as_json = "--json" in sys.argv
    summary_only = "--summary" in sys.argv

    mods = []
    for d in sorted(LIVE_MODS_DIR.iterdir()):
        if not d.is_dir():
            continue
        if d.name.lower() in BUILTIN_MODS:
            continue
        if d.name.startswith("__"):
            continue
        mods.append(classify_mod(d))

    if as_json:
        print(json.dumps(mods, indent=2))
        return

    # Count by category
    counts = {"v2_ok": 0, "v2_issues": 0, "v1_disabled": 0, "content": 0, "error": 0}
    for m in mods:
        if m["mp_status"] == "ok":
            counts["v2_ok"] += 1
        elif m["mp_status"] == "issues":
            counts["v2_issues"] += 1
        elif m["mp_status"] == "disabled":
            counts["v1_disabled"] += 1
        elif m["mp_status"] == "content":
            counts["content"] += 1
        else:
            counts["error"] += 1

    if summary_only:
        print(f"Total: {len(mods)}")
        print(f"  v2 OK:      {counts['v2_ok']}")
        print(f"  v2 Issues:  {counts['v2_issues']}")
        print(f"  v1 Disabled:{counts['v1_disabled']}")
        print(f"  Content:    {counts['content']}")
        return

    # Full table
    print(f"{'Mod':<40} {'Ver':<4} {'Type':<10} {'MP Status':<12} {'Issues'}")
    print("-" * 95)
    for m in mods:
        issues_str = ", ".join(m.get("issues", []))
        print(f"{m['name']:<40} {m['version']:<4} {m['type']:<10} {m['mp_status']:<12} {issues_str}")
    print("-" * 95)
    print(f"Total: {len(mods)} | OK: {counts['v2_ok']} | Issues: {counts['v2_issues']} | Disabled: {counts['v1_disabled']} | Content: {counts['content']}")


if __name__ == "__main__":
    main()
