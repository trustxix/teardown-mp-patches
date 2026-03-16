import json
from pathlib import Path
from tools.ingest import parse_info_txt, ingest_mod, ingest_batch, is_already_v2


def test_parse_info_txt(simple_tool_dir):
    info = parse_info_txt(simple_tool_dir / "info.txt")
    assert info["name"] == "Laser Cutter"
    assert info["author"] == "TestAuthor"
    assert info["description"] == "A simple laser cutting tool"
    assert info["tags"] == "Tool"
    assert info.get("version") is None


def test_parse_info_txt_v2(already_v2_dir):
    info = parse_info_txt(already_v2_dir / "info.txt")
    assert info["version"] == "2"


def test_is_already_v2_false(simple_tool_dir):
    assert is_already_v2(simple_tool_dir) is False


def test_is_already_v2_true(already_v2_dir):
    assert is_already_v2(already_v2_dir) is True


def test_ingest_mod(simple_tool_dir, tmp_output):
    result = ingest_mod(simple_tool_dir, tmp_output, workshop_id="123456")
    assert result["workshop_id"] == "123456"
    assert result["name"] == "Laser Cutter"
    assert result["status"] == "pending"
    assert (tmp_output / "123456" / "original" / "main.lua").exists()
    assert (tmp_output / "123456" / "original" / "info.txt").exists()
    assert (tmp_output / "123456" / "metadata.json").exists()
    meta = json.loads((tmp_output / "123456" / "metadata.json").read_text())
    assert "sha256" in meta
    assert meta["status"] == "pending"


def test_ingest_mod_skips_v2(already_v2_dir, tmp_output):
    result = ingest_mod(already_v2_dir, tmp_output, workshop_id="999999")
    assert result is None


def test_ingest_batch(fixtures_dir, tmp_output):
    results = ingest_batch(fixtures_dir, tmp_output)
    names = [r["name"] for r in results if r is not None]
    assert "Laser Cutter" in names
    assert "Monster Truck" in names
    assert "Battle Royale Lite" in names
    assert len([r for r in results if r is not None]) == 3
