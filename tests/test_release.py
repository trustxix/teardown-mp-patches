import json
from unittest.mock import patch, MagicMock
from pathlib import Path
from tools.release import build_release_body, build_release_tag, release_mod


def test_build_release_tag():
    meta = {"workshop_id": "123456", "patch_version": "1.0"}
    assert build_release_tag(meta) == "mod-123456-v1.0"


def test_build_release_body():
    meta = {
        "workshop_id": "123456",
        "name": "Test Mod",
        "author": "TestAuthor",
        "description": "A test mod",
        "patch_version": "1.0",
    }
    body = build_release_body(meta)
    assert "Test Mod" in body
    assert "TestAuthor" in body
    assert "123456" in body
    assert "Unofficial" in body or "unofficial" in body


@patch("tools.release.subprocess.run")
def test_release_mod(mock_run, tmp_path):
    mod_dir = tmp_path / "123456"
    mod_dir.mkdir()
    (mod_dir / "metadata.json").write_text(json.dumps({
        "workshop_id": "123456", "name": "Test", "author": "A",
        "description": "Desc", "status": "packaged", "patch_version": "1.0",
    }))
    (mod_dir / "Test-mp-patch-v1.0.zip").write_bytes(b"fake zip")

    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="https://github.com/user/repo/releases/tag/mod-123456-v1.0\n",
        stderr=""
    )
    result = release_mod(mod_dir)
    assert result["tag"] == "mod-123456-v1.0"
    assert "error" not in result
    call_args = mock_run.call_args[0][0]
    assert "gh" in call_args
    assert "release" in call_args
    assert "create" in call_args
    meta = json.loads((mod_dir / "metadata.json").read_text())
    assert meta["status"] == "released"
