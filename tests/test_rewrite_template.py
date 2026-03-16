from pathlib import Path
from tools.rewrite_template import (
    rewrite_script,
    apply_fixups,
    update_info_txt,
    split_callback_body,
    wrap_player_calls_for_mp,
)
from tools.analyze import analyze_script


def test_apply_fixups_version_header():
    source = "function init()\nend"
    result = apply_fixups(source)
    assert result.startswith("#version 2\n")


def test_apply_fixups_handle_check():
    source = "if handle > 0 then\nend"
    result = apply_fixups(source)
    assert "handle ~= 0" in result
    assert "handle > 0" not in result


def test_apply_fixups_deprecated():
    source = "local t = GetPlayerRigTransform()"
    result = apply_fixups(source)
    assert "GetPlayerRigWorldTransform" in result
    assert "GetPlayerRigTransform" not in result


def test_apply_fixups_registry_sync():
    source = 'SetInt("score", 10)'
    result = apply_fixups(source)
    assert "true)" in result


def test_wrap_player_calls():
    source = "local h = GetPlayerHealth()"
    result = wrap_player_calls_for_mp(source)
    assert "GetPlayerHealth(playerId)" in result


def test_update_info_txt(simple_tool_dir, tmp_path):
    import shutil
    dest = tmp_path / "info.txt"
    shutil.copy(simple_tool_dir / "info.txt", dest)
    update_info_txt(dest)
    content = dest.read_text()
    assert "version = 2" in content


def test_split_callback_body_simple():
    """tick() with input calls should split: input->client, rest->server."""
    body_lines = [
        'if InputPressed("lmb") then',
        '    toolActive = true',
        'end',
        'SetPlayerHealth(100)',
    ]
    client_lines, server_lines = split_callback_body(body_lines, "tick")
    client_text = "\n".join(client_lines)
    server_text = "\n".join(server_lines)
    assert "InputPressed" in client_text
    assert "SetPlayerHealth" in server_text


def test_split_callback_body_keeps_blocks_intact():
    """An if block containing InputPressed should stay together in client."""
    body_lines = [
        'if InputPressed("lmb") then',
        '    toolActive = true',
        '    charge = 0',
        'end',
    ]
    client_lines, server_lines = split_callback_body(body_lines, "tick")
    # Entire block should be in client (InputPressed is client-domain)
    assert len(client_lines) == 4
    assert "end" in client_lines[-1]


def test_rewrite_script_simple_tool(simple_tool_dir):
    source = (simple_tool_dir / "main.lua").read_text()
    analysis = analyze_script(source, "main.lua")
    result = rewrite_script(source, analysis, mod_type="tool")
    assert result.startswith("#version 2")
    assert "function server.init()" in result
    assert "function client.draw()" in result
    # No bare v1 callbacks
    lines = result.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("function ") and "." not in stripped:
            # Allow helper functions but not v1 callbacks
            func_name = stripped.split("(")[0].replace("function ", "").strip()
            assert func_name not in ("init", "tick", "update", "draw"), f"Found v1 callback: {stripped}"
    # UI calls should be present
    assert "UiText" in result


def test_rewrite_script_vehicle(simple_vehicle_dir):
    source = (simple_vehicle_dir / "main.lua").read_text()
    analysis = analyze_script(source, "main.lua")
    result = rewrite_script(source, analysis, mod_type="vehicle")
    assert result.startswith("#version 2")
    assert "function server" in result or "function client" in result
    # Vehicle template should have player loop or local player
    assert "GetAllPlayers" in result or "GetLocalPlayer" in result
