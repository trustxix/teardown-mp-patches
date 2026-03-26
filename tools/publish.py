"""Mass-publish mods to Steam Workshop via SteamCMD.

Creates VDF item configs and uploads each mod sequentially.
Requires one-time Steam login (will prompt for credentials + Steam Guard).

Usage:
    python -m tools.publish                    # Publish all unpublished mods
    python -m tools.publish --mod "AC130"      # Publish one mod
    python -m tools.publish --login            # Just login to Steam (do this first)
    python -m tools.publish --list             # Show what would be published
"""
import os
import sys
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

STEAMCMD = Path("C:/steamcmd/steamcmd.exe")
MODS_DIR = Path("D:/The Vault/Modding/Games/Teardown")
VDF_DIR = Path("C:/Users/trust/teardown-mp-patches/workshop_vdf")
PUBLISHED_LOG = Path("C:/Users/trust/teardown-mp-patches/workshop_published.json")
TEARDOWN_APP_ID = "1167630"


def get_mod_info(mod_dir: Path) -> dict:
    """Read mod metadata from info.txt."""
    info = {"name": mod_dir.name, "author": "", "description": "", "tags": ""}
    info_path = mod_dir / "info.txt"
    if info_path.exists():
        content = info_path.read_text(errors="ignore")
        for key in ("name", "en_name", "author", "description", "en_description", "tags"):
            m = re.search(rf"^{key}\s*=\s*(.*)", content, re.MULTILINE)
            if m:
                val = m.group(1).strip()
                if key == "en_name":
                    info["name"] = val
                elif key == "en_description":
                    info["description"] = val
                elif key in info:
                    info[key] = val
    return info


def create_vdf(mod_dir: Path, workshop_id: str = "") -> Path:
    """Create a VDF file for steamcmd workshop_build_item."""
    os.makedirs(VDF_DIR, exist_ok=True)

    info = get_mod_info(mod_dir)

    # Find preview image
    preview = ""
    for img_name in ("preview.jpg", "preview.png", "preview.jpeg"):
        img_path = mod_dir / img_name
        if img_path.exists():
            preview = str(img_path).replace("/", "\\")
            break

    vdf_name = f"{mod_dir.name}.vdf"
    vdf_path = VDF_DIR / vdf_name

    lines = [
        '"workshopitem"',
        '{',
        f'    "appid" "{TEARDOWN_APP_ID}"',
    ]

    if workshop_id:
        lines.append(f'    "publishedfileid" "{workshop_id}"')

    content_path = str(mod_dir).replace("/", "\\")
    lines.append(f'    "contentfolder" "{content_path}"')

    if preview:
        lines.append(f'    "previewfile" "{preview}"')

    lines.append(f'    "visibility" "0"')  # 0=public, 1=friends, 2=private
    lines.append(f'    "title" "{info["name"]}"')
    lines.append(f'    "description" "{info["description"]}"')

    # Tags
    if info["tags"]:
        tag_list = [t.strip().strip("#") for t in info["tags"].split(",")]
        for i, tag in enumerate(tag_list):
            lines.append(f'    "tag{i}" "{tag}"')

    lines.append('}')

    vdf_path.write_text("\n".join(lines), encoding="utf-8")
    return vdf_path


def load_published() -> dict:
    """Load record of already-published mods."""
    if PUBLISHED_LOG.exists():
        return json.loads(PUBLISHED_LOG.read_text())
    return {}


def save_published(data: dict):
    PUBLISHED_LOG.write_text(json.dumps(data, indent=2))


def steam_login():
    """Interactive Steam login."""
    print("Logging into Steam...")
    print("You'll need your username, password, and Steam Guard code.")
    print()
    username = input("Steam username: ").strip()
    result = subprocess.run(
        [str(STEAMCMD), "+login", username, "+quit"],
        timeout=120,
    )
    return result.returncode == 0


def publish_mod(mod_dir: Path, published: dict) -> str | None:
    """Publish a single mod. Returns workshop ID or None on failure."""
    mod_name = mod_dir.name
    workshop_id = published.get(mod_name, {}).get("id", "")

    vdf_path = create_vdf(mod_dir, workshop_id)

    print(f"  Publishing {mod_name}...")

    result = subprocess.run(
        [str(STEAMCMD), "+login", "anonymous_or_cached", "+workshop_build_item",
         str(vdf_path), "+quit"],
        capture_output=True, text=True, timeout=120,
    )

    output = result.stdout + result.stderr

    # Parse workshop ID from output
    id_match = re.search(r"PublishFileID\s*=\s*(\d+)", output)
    if id_match:
        new_id = id_match.group(1)
        published[mod_name] = {
            "id": new_id,
            "name": get_mod_info(mod_dir)["name"],
            "published": datetime.now().isoformat(),
        }
        save_published(published)
        print(f"    OK: Workshop ID {new_id}")
        return new_id

    # Check for common errors
    if "Login" in output and "Fail" in output:
        print(f"    FAIL: Steam login required. Run: python -m tools.publish --login")
        return None
    elif "Error" in output or "FAIL" in output:
        error_match = re.search(r"(Error|FAIL).*", output)
        print(f"    FAIL: {error_match.group(0) if error_match else 'Unknown error'}")
        return None
    else:
        print(f"    FAIL: No workshop ID in output")
        # Save output for debugging
        (VDF_DIR / f"{mod_name}_output.txt").write_text(output)
        return None


def main():
    if "--login" in sys.argv:
        steam_login()
        return

    mod_filter = None
    if "--mod" in sys.argv:
        idx = sys.argv.index("--mod")
        if idx + 1 < len(sys.argv):
            mod_filter = sys.argv[idx + 1]

    list_only = "--list" in sys.argv

    if not STEAMCMD.exists():
        print(f"SteamCMD not found at {STEAMCMD}")
        print("Install: mkdir C:\\steamcmd && download steamcmd.zip from Valve")
        sys.exit(1)

    # Find mods to publish
    mods = []
    for d in sorted(MODS_DIR.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith("__"):
            continue
        info_path = d / "info.txt"
        if not info_path.exists():
            continue
        if mod_filter and mod_filter.lower() not in d.name.lower():
            continue
        mods.append(d)

    published = load_published()

    if list_only:
        print(f"Mods to publish ({len(mods)}):")
        for m in mods:
            info = get_mod_info(m)
            status = "UPDATE" if m.name in published else "NEW"
            print(f"  [{status}] {info['name']}")
        return

    print(f"Publishing {len(mods)} mods to Steam Workshop...")
    print()

    success = 0
    failed = 0
    for mod_dir in mods:
        result = publish_mod(mod_dir, published)
        if result:
            success += 1
        else:
            failed += 1

    print()
    print(f"Done: {success} published, {failed} failed")
    if failed > 0:
        print("Run with --login first if you got login errors")


if __name__ == "__main__":
    main()
