from tools.logparse import parse_log


SAMPLE_LOG = '''Teardown 2.0.0 (20260315)
Some loading stuff
Loading mod "Bee_Gun" from C:/Users/trust/Documents/Teardown/mods/Bee_Gun
[string "C:/Users/trust/Documents/Teardown/mods/Bee_Gun/main.lua"]:45: attempt to call nil value 'GetPlayerAimInfo'
Loading mod "AK-47" from C:/Users/trust/Documents/Teardown/mods/AK-47
Loading mod "Hook_Shotgun" from C:/Users/trust/Documents/Teardown/mods/Hook_Shotgun
Error compiling: C:/Users/trust/Documents/Teardown/mods/Hook_Shotgun/main.lua
[string "C:/Users/trust/Documents/Teardown/mods/Bee_Gun/main.lua"]:89: SetPlayerTransform is not available in client script
'''


def test_parse_log_version():
    result = parse_log(SAMPLE_LOG)
    assert result["version"] == "2.0.0"


def test_parse_log_runtime_error():
    result = parse_log(SAMPLE_LOG)
    assert "Bee_Gun" in result["mods"]
    errors = result["mods"]["Bee_Gun"]
    assert len(errors) == 2
    assert errors[0]["line"] == 45
    assert errors[0]["type"] == "runtime"
    assert "GetPlayerAimInfo" in errors[0]["message"]


def test_parse_log_compile_error():
    result = parse_log(SAMPLE_LOG)
    assert "Hook_Shotgun" in result["mods"]
    errors = result["mods"]["Hook_Shotgun"]
    assert len(errors) == 1
    assert errors[0]["type"] == "compile"


def test_parse_log_clean_mod():
    result = parse_log(SAMPLE_LOG)
    assert "AK-47" not in result["mods"]


def test_parse_log_empty():
    result = parse_log("")
    assert result["version"] == "unknown"
    assert result["mods"] == {}


def test_parse_log_no_errors():
    result = parse_log("Teardown 2.0.0 (20260315)\nLoading stuff\n")
    assert result["version"] == "2.0.0"
    assert result["mods"] == {}


def test_parse_log_backslash_paths():
    log = r'[string "C:\Users\trust\Documents\Teardown\mods\AK-47\main.lua"]:10: some error'
    result = parse_log(log)
    assert "AK-47" in result["mods"]
    assert result["mods"]["AK-47"][0]["line"] == 10
