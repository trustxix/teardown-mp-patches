from pathlib import Path
from tools.validate import (
    check_v2_header,
    check_v2_info,
    check_no_v1_callbacks,
    check_ui_in_draw,
    check_handle_safe,
    check_no_deprecated,
    check_player_id,
    check_server_auth,
    check_client_input,
    check_registry_sync,
    check_no_globals,
    check_file_complete,
    validate_script,
    validate_mod,
)


GOOD_V2_SCRIPT = """#version 2

local score = 0

function server.init()
    RegisterTool("test", "Test", "MOD/vox/test.vox")
end

function server.update(dt)
    for _, pid in ipairs(GetAllPlayers()) do
        SetPlayerHealth(pid, 100)
    end
end

function client.tick(dt)
    if InputPressed("lmb") then
        ServerCall("onFire")
    end
end

function client.draw()
    UiPush()
    UiText("Score: " .. score)
    UiPop()
end
"""

BAD_SCRIPT_NO_HEADER = """function server.init()
end
"""

BAD_SCRIPT_V1_CALLBACKS = """#version 2

function init()
end

function tick(dt)
end
"""

BAD_SCRIPT_UI_OUTSIDE_DRAW = """#version 2

function client.tick(dt)
    UiText("wrong place")
end

function client.draw()
    UiText("right place")
end
"""

BAD_SCRIPT_HANDLE = """#version 2

function client.tick(dt)
    local h = FindBody("test")
    if h > 0 then
    end
end
"""


def test_check_v2_header_pass():
    assert check_v2_header(GOOD_V2_SCRIPT)["passed"]


def test_check_v2_header_fail():
    assert not check_v2_header(BAD_SCRIPT_NO_HEADER)["passed"]


def test_check_no_v1_callbacks_pass():
    assert check_no_v1_callbacks(GOOD_V2_SCRIPT)["passed"]


def test_check_no_v1_callbacks_fail():
    assert not check_no_v1_callbacks(BAD_SCRIPT_V1_CALLBACKS)["passed"]


def test_check_ui_in_draw_pass():
    assert check_ui_in_draw(GOOD_V2_SCRIPT)["passed"]


def test_check_ui_in_draw_fail():
    assert not check_ui_in_draw(BAD_SCRIPT_UI_OUTSIDE_DRAW)["passed"]


def test_check_handle_safe_pass():
    assert check_handle_safe(GOOD_V2_SCRIPT)["passed"]


def test_check_handle_safe_fail():
    assert not check_handle_safe(BAD_SCRIPT_HANDLE)["passed"]


def test_check_registry_sync_pass():
    source = '#version 2\nfunction server.init()\n    SetInt("score", 10, true)\nend'
    assert check_registry_sync(source)["passed"]


def test_check_registry_sync_fail():
    source = '#version 2\nfunction server.init()\n    SetInt("score", 10)\nend'
    assert not check_registry_sync(source)["passed"]


def test_check_file_complete_pass(tmp_path):
    orig = tmp_path / "orig"
    orig.mkdir()
    (orig / "main.lua").write_text("test")
    patch = tmp_path / "patch"
    patch.mkdir()
    (patch / "main.lua").write_text("test2")
    assert check_file_complete(orig, patch)["passed"]


def test_check_file_complete_fail(tmp_path):
    orig = tmp_path / "orig"
    orig.mkdir()
    (orig / "main.lua").write_text("test")
    (orig / "extra.lua").write_text("test")
    patch = tmp_path / "patch"
    patch.mkdir()
    (patch / "main.lua").write_text("test2")
    assert not check_file_complete(orig, patch)["passed"]


def test_check_no_globals_no_warning():
    source = '#version 2\nlocal x = 1\nfunction server.init()\n    x = 2\nend'
    result = check_no_globals(source)
    assert result["passed"]  # Always passes (warnings only)


def test_check_server_auth_pass():
    source = '#version 2\nfunction server.update(dt)\n    SetPlayerHealth(pid, 100)\nend'
    assert check_server_auth(source)["passed"]


def test_check_server_auth_fail():
    source = '#version 2\nfunction client.tick(dt)\n    SetPlayerHealth(pid, 100)\nend'
    assert not check_server_auth(source)["passed"]


def test_check_client_input_pass():
    source = '#version 2\nfunction client.tick(dt)\n    InputPressed("lmb")\nend'
    assert check_client_input(source)["passed"]


def test_check_client_input_fail():
    source = '#version 2\nfunction server.tick(dt)\n    InputPressed("lmb")\nend'
    assert not check_client_input(source)["passed"]


def test_validate_script_good():
    results = validate_script(GOOD_V2_SCRIPT, "main.lua")
    # All checks should pass (NO-GLOBALS always passes as warnings-only)
    for r in results:
        assert r["passed"], f"Check {r['check']} failed: {r.get('detail', '')}"


def test_validate_script_bad():
    results = validate_script(BAD_SCRIPT_V1_CALLBACKS, "main.lua")
    failed = [r for r in results if not r["passed"]]
    assert len(failed) > 0


def test_validate_mod_pass(already_v2_dir):
    result = validate_mod(already_v2_dir)
    assert result["all_passed"]


def test_validate_mod_fail(simple_tool_dir):
    result = validate_mod(simple_tool_dir)
    assert not result["all_passed"]
