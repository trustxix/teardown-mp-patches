"""End-to-end integration test: ingest -> analyze -> rewrite -> validate -> package."""

import json
import shutil
from pathlib import Path

from tools.ingest import ingest_mod
from tools.analyze import analyze_mod
from tools.rewrite_template import rewrite_script, update_info_txt
from tools.validate import validate_mod
from tools.package import package_mod


def test_full_pipeline_simple_tool(simple_tool_dir, tmp_output):
    """Full pipeline for a simple tool mod."""
    # Ingest
    meta = ingest_mod(simple_tool_dir, tmp_output, "test_tool")
    assert meta is not None
    assert meta["status"] == "pending"

    # Analyze
    original_dir = tmp_output / "test_tool" / "original"
    analysis = analyze_mod(original_dir)
    assert analysis["mod_type"] == "tool"
    assert analysis["complexity"] == "simple"
    (tmp_output / "test_tool" / "analysis.json").write_text(json.dumps(analysis, indent=2))

    # Rewrite
    patched_dir = tmp_output / "test_tool" / "patched"
    shutil.copytree(original_dir, patched_dir)
    for script in analysis["scripts"]:
        lua_path = patched_dir / script["file"]
        source = lua_path.read_text()
        rewritten = rewrite_script(source, script, mod_type="tool")
        lua_path.write_text(rewritten)
    update_info_txt(patched_dir / "info.txt")

    # Validate
    val = validate_mod(patched_dir, original_dir=original_dir)
    # Print any failing checks for diagnostics
    for fe in val["files"]:
        for check in fe["checks"]:
            if not check["passed"]:
                print(f"FAIL: {check['check']} in {fe['file']} - {check.get('detail', '')}")
    if val["info_check"] and not val["info_check"]["passed"]:
        print(f"FAIL: {val['info_check']['check']} - {val['info_check'].get('detail', '')}")
    assert val["all_passed"], "Validation failed; see FAIL lines above"

    # Package
    pkg = package_mod(tmp_output / "test_tool")
    assert pkg["zip_path"].exists()


def test_full_pipeline_simple_vehicle(simple_vehicle_dir, tmp_output):
    """Full pipeline for a vehicle mod."""
    meta = ingest_mod(simple_vehicle_dir, tmp_output, "test_vehicle")
    assert meta is not None

    original_dir = tmp_output / "test_vehicle" / "original"
    analysis = analyze_mod(original_dir)
    assert analysis["mod_type"] == "vehicle"

    patched_dir = tmp_output / "test_vehicle" / "patched"
    shutil.copytree(original_dir, patched_dir)
    for script in analysis["scripts"]:
        lua_path = patched_dir / script["file"]
        source = lua_path.read_text()
        rewritten = rewrite_script(source, script, mod_type="vehicle")
        lua_path.write_text(rewritten)
    update_info_txt(patched_dir / "info.txt")

    val = validate_mod(patched_dir, original_dir=original_dir)
    # Print any failing checks for diagnostics
    for fe in val["files"]:
        for check in fe["checks"]:
            if not check["passed"]:
                print(f"FAIL: {check['check']} in {fe['file']} - {check.get('detail', '')}")
    if val["info_check"] and not val["info_check"]["passed"]:
        print(f"FAIL: {val['info_check']['check']} - {val['info_check'].get('detail', '')}")
    assert val["all_passed"], "Validation failed; see FAIL lines above"


def test_v2_mod_skipped(already_v2_dir, tmp_output):
    """Already v2 mods should be skipped during ingest."""
    result = ingest_mod(already_v2_dir, tmp_output, "skip_me")
    assert result is None
