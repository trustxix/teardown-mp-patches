"""Phase 6: GitHub Release automation using gh CLI."""

import json
import subprocess
from pathlib import Path


def build_release_tag(meta: dict) -> str:
    return f"mod-{meta['workshop_id']}-v{meta.get('patch_version', '1.0')}"


def build_release_body(meta: dict) -> str:
    wid = meta["workshop_id"]
    workshop_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={wid}"
    return f"""## {meta['name']} - Multiplayer Patch

**Original Author:** {meta.get('author', 'Unknown')}
**Workshop:** [{meta['name']}]({workshop_url})
**Patch Version:** {meta.get('patch_version', '1.0')}

> This is an **unofficial multiplayer compatibility patch**. Please subscribe to the [original mod on Steam Workshop]({workshop_url}) to support the original author.

### Description
{meta.get('description', 'N/A')}

### Installation
1. Download the zip file below
2. Extract to your `Documents/Teardown/mods/` folder
3. Enable the mod in-game
"""


def release_mod(mod_dir: Path) -> dict:
    """Create a GitHub Release for a packaged mod."""
    meta = json.loads((mod_dir / "metadata.json").read_text())
    tag = build_release_tag(meta)
    title = f"{meta['name']} MP Patch v{meta.get('patch_version', '1.0')}"
    body = build_release_body(meta)

    zip_files = list(mod_dir.glob("*.zip"))
    if not zip_files:
        return {"error": "No zip file found. Run package first."}

    zip_path = zip_files[0]

    cmd = [
        "gh", "release", "create", tag,
        str(zip_path),
        "--title", title,
        "--notes", body,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}

    meta["status"] = "released"
    (mod_dir / "metadata.json").write_text(json.dumps(meta, indent=2))

    return {"tag": tag, "url": result.stdout.strip()}


def release_all(mods_dir: Path) -> list[dict]:
    """Create releases for all packaged mods."""
    results = []
    for mod_dir in sorted(mods_dir.iterdir()):
        meta_path = mod_dir / "metadata.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        if meta.get("status") == "packaged":
            result = release_mod(mod_dir)
            results.append({"workshop_id": meta["workshop_id"], **result})
    return results
