from pathlib import Path
from tools.analyze import (
    analyze_script,
    analyze_mod,
    classify_complexity,
    extract_callbacks,
    extract_api_calls,
)


def test_extract_callbacks_v1(simple_tool_dir):
    source = (simple_tool_dir / "main.lua").read_text()
    callbacks = extract_callbacks(source)
    assert set(callbacks) == {"init", "tick", "update", "draw"}


def test_extract_callbacks_v2(already_v2_dir):
    source = (already_v2_dir / "main.lua").read_text()
    callbacks = extract_callbacks(source)
    assert "server.init" in callbacks
    assert "client.draw" in callbacks


def test_extract_api_calls(simple_tool_dir):
    source = (simple_tool_dir / "main.lua").read_text()
    calls = extract_api_calls(source)
    fn_names = [c["function"] for c in calls]
    assert "RegisterTool" in fn_names
    assert "InputPressed" in fn_names
    assert "GetPlayerTransform" in fn_names
    assert "UiText" in fn_names
    assert "MakeHole" in fn_names
    assert "PlaySound" in fn_names


def test_analyze_script_simple(simple_tool_dir):
    source = (simple_tool_dir / "main.lua").read_text()
    result = analyze_script(source, "main.lua")
    assert result["file"] == "main.lua"
    assert result["server_calls"] > 0
    assert result["client_calls"] > 0
    assert len(result["callbacks_found"]) == 4
    assert any(c["needs_player_id"] for c in result["api_calls"])


def test_analyze_script_detects_deprecated():
    source = "function tick(dt)\n    local t = GetPlayerRigTransform()\nend"
    result = analyze_script(source, "test.lua")
    assert len(result["deprecated_calls"]) > 0


def test_analyze_script_detects_handle_issues():
    source = "function tick(dt)\n    local h = FindBody('test')\n    if h > 0 then\n    end\nend"
    result = analyze_script(source, "test.lua")
    assert len(result["entity_handle_checks"]) > 0


def test_analyze_mod(simple_tool_dir):
    result = analyze_mod(simple_tool_dir)
    assert result["mod_name"] == "Laser Cutter"
    assert result["current_version"] == 1
    assert len(result["scripts"]) == 1
    assert result["complexity"] in ("simple", "medium", "complex")


def test_classify_complexity_simple():
    scripts = [{"lines": 50, "api_calls": [], "callbacks_found": ["init", "tick"]}]
    assert classify_complexity(scripts) == "simple"


def test_classify_complexity_complex():
    scripts = [
        {"lines": 600, "api_calls": [{"function": "x"}] * 50, "callbacks_found": ["init", "tick", "update", "draw"]},
        {"lines": 100, "api_calls": [], "callbacks_found": []},
    ]
    assert classify_complexity(scripts) == "complex"


def test_analyze_mod_detects_vehicle(simple_vehicle_dir):
    result = analyze_mod(simple_vehicle_dir)
    assert result["mod_type"] == "vehicle"


def test_analyze_mod_detects_tool(simple_tool_dir):
    result = analyze_mod(simple_tool_dir)
    assert result["mod_type"] == "tool"
