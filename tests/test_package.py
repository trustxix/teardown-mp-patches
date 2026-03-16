import json
import zipfile
from pathlib import Path
from tools.package import package_mod, generate_migration_md


def test_generate_migration_md():
    original = "function init()\n    RegisterTool('test', 'Test', 'MOD/vox/t.vox')\nend"
    patched = '#version 2\n\nfunction server.init()\n    RegisterTool("test", "Test", "MOD/vox/t.vox")\nend'
    md = generate_migration_md(original, patched, "main.lua")
    assert "main.lua" in md
    assert "server.init" in md or "version 2" in md


def test_package_mod(tmp_path):
    mod_dir = tmp_path / "mods" / "123456"
    patched = mod_dir / "patched"
    patched.mkdir(parents=True)
    (patched / "info.txt").write_text("name = Test\nauthor = A\nversion = 2")
    (patched / "main.lua").write_text('#version 2\n\nfunction server.init()\nend')
    (mod_dir / "metadata.json").write_text(json.dumps({
        "workshop_id": "123456",
        "name": "Test",
        "author": "A",
        "status": "patched",
        "patch_version": "1.0",
    }))

    original = mod_dir / "original"
    original.mkdir()
    (original / "main.lua").write_text("function init()\nend")
    (original / "info.txt").write_text("name = Test\nauthor = A")

    result = package_mod(mod_dir)
    assert result["zip_path"].exists()
    assert result["migration_md"].exists()

    with zipfile.ZipFile(result["zip_path"]) as zf:
        names = zf.namelist()
        assert any("main.lua" in n for n in names)
        assert any("info.txt" in n for n in names)
