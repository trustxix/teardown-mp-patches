import json
from pathlib import Path
from unittest.mock import MagicMock, patch
from tools.rewrite_ai import build_prompt, rewrite_script_ai, SYSTEM_PROMPT


def test_build_prompt(simple_tool_dir):
    source = (simple_tool_dir / "main.lua").read_text()
    analysis = {"file": "main.lua", "complexity": "complex", "api_calls": []}
    prompt = build_prompt(source, analysis)
    assert "main.lua" in prompt
    assert "v2" in prompt.lower()
    assert "rewrite" in prompt.lower()


def test_system_prompt_contains_rules():
    assert "server.init" in SYSTEM_PROMPT
    assert "client" in SYSTEM_PROMPT
    assert "Players()" in SYSTEM_PROMPT
    assert "per-player" in SYSTEM_PROMPT.lower() or "players[p]" in SYSTEM_PROMPT


@patch("tools.rewrite_ai._call_claude")
def test_rewrite_script_ai(mock_call, simple_tool_dir):
    expected_output = '#version 2\n\nfunction server.init()\nend\n\nfunction client.draw()\n    UiText("test")\nend'
    mock_call.return_value = expected_output
    source = (simple_tool_dir / "main.lua").read_text()
    analysis = {"file": "main.lua", "complexity": "complex", "api_calls": []}
    result = rewrite_script_ai(source, analysis)
    assert result.startswith("#version 2")
    assert mock_call.called


@patch("tools.rewrite_ai._call_claude")
def test_rewrite_caches_result(mock_call, simple_tool_dir, tmp_path):
    expected_output = '#version 2\n\nfunction server.init()\nend'
    mock_call.return_value = expected_output
    source = (simple_tool_dir / "main.lua").read_text()
    analysis = {"file": "main.lua", "complexity": "complex", "api_calls": []}
    result1 = rewrite_script_ai(source, analysis, cache_dir=tmp_path)
    result2 = rewrite_script_ai(source, analysis, cache_dir=tmp_path)
    assert mock_call.call_count == 1
    assert result1 == result2


@patch("tools.rewrite_ai._call_claude")
def test_rewrite_strips_markdown_fences(mock_call):
    mock_call.return_value = '```lua\n#version 2\n\nfunction server.init()\nend\n```'
    result = rewrite_script_ai("function init()\nend", {"file": "test.lua", "api_calls": []})
    assert not result.startswith("```")
    assert result.startswith("#version 2")
