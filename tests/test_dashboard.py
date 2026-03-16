import json
from pathlib import Path
from tools.dashboard import generate_dashboard


def test_generate_dashboard(tmp_path):
    mod1 = tmp_path / "mods" / "111"
    mod1.mkdir(parents=True)
    (mod1 / "metadata.json").write_text(json.dumps({
        "workshop_id": "111", "name": "Laser Tool", "author": "Alice",
        "tags": "Tool", "status": "released", "patch_version": "1.0",
    }))
    (mod1 / "analysis.json").write_text(json.dumps({
        "complexity": "simple", "mod_type": "tool",
    }))

    mod2 = tmp_path / "mods" / "222"
    mod2.mkdir(parents=True)
    (mod2 / "metadata.json").write_text(json.dumps({
        "workshop_id": "222", "name": "Monster Truck", "author": "Bob",
        "tags": "Vehicle", "status": "patched", "patch_version": "1.0",
    }))
    (mod2 / "analysis.json").write_text(json.dumps({
        "complexity": "medium", "mod_type": "vehicle",
    }))

    readme = generate_dashboard(tmp_path / "mods")
    assert "Laser Tool" in readme
    assert "Monster Truck" in readme
    assert "Alice" in readme
    assert "| Tool |" in readme or "| tool |" in readme
