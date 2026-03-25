"""Build a mod pack zip for sharing with friends.

Creates a zip containing all patched mods (mods that differ from workshop).
Friends extract this to their game install mods dir for identical files.
Solves the "mod files differ from host" file integrity check.

Usage:
    python -m tools.pack                          # Pack all modified mods
    python -m tools.pack --output my_mods.zip     # Custom output name
    python -m tools.pack --include-all            # Pack ALL custom mods (not just modified)
"""
import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime
from tools.common import LIVE_MODS_DIR
from tools.classify import BUILTIN_MODS
from tools.diff import find_workshop_original

WORKSHOP_DIR = Path("C:/Program Files (x86)/Steam/steamapps/workshop/content/1167630")
SKIP_EXTENSIONS = {".jpg", ".jpeg", ".png"}  # No preview images


def is_modified(mod_dir: Path) -> bool:
    """Check if a mod differs from its workshop original."""
    ws_dir = find_workshop_original(mod_dir)
    if ws_dir is None:
        return True  # No workshop original = always include

    main_lua = mod_dir / "main.lua"
    ws_main = ws_dir / "main.lua"

    if main_lua.exists() and ws_main.exists():
        return main_lua.read_bytes() != ws_main.read_bytes()

    return False


def build_pack(output_path: str, include_all: bool = False):
    mods_to_pack = []

    for d in sorted(LIVE_MODS_DIR.iterdir()):
        if not d.is_dir():
            continue
        if d.name.lower() in BUILTIN_MODS:
            continue
        if d.name.startswith("__"):
            continue
        if not (d / "id.txt").exists():
            continue  # Not our mod

        if include_all or is_modified(d):
            mods_to_pack.append(d)

    if not mods_to_pack:
        print("No modified mods to pack.")
        return

    print(f"Packing {len(mods_to_pack)} mods...")

    file_count = 0
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for mod_dir in mods_to_pack:
            mod_name = mod_dir.name
            for root, dirs, files in os.walk(mod_dir):
                for fname in files:
                    fpath = Path(root) / fname
                    if fpath.suffix.lower() in SKIP_EXTENSIONS:
                        continue
                    arcname = f"mods/{mod_name}/{fpath.relative_to(mod_dir)}"
                    zf.write(fpath, arcname)
                    file_count += 1
            print(f"  + {mod_name}")

        # Add a README
        readme = (
            "Teardown MP Mod Pack\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Mods: {len(mods_to_pack)}\n\n"
            "Installation:\n"
            "1. Close Teardown\n"
            "2. Extract this zip so the 'mods' folder merges with:\n"
            "   C:\\Program Files (x86)\\Steam\\steamapps\\common\\Teardown\\mods\\\n"
            "3. Launch Teardown\n\n"
            "All players must have identical mod files for MP to work.\n"
        )
        zf.writestr("README.txt", readme)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nPacked {len(mods_to_pack)} mods ({file_count} files) -> {output_path} ({size_mb:.1f} MB)")


def main():
    include_all = "--include-all" in sys.argv

    output = f"teardown_modpack_{datetime.now().strftime('%Y%m%d')}.zip"
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output = sys.argv[idx + 1]

    build_pack(output, include_all=include_all)


if __name__ == "__main__":
    main()
