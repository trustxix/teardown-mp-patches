from pathlib import Path
from tools.common import (
    LIVE_MODS_DIR, LOG_PATH, RAW_KEYS, PLAYER_INPUTS, discover_mods, read_lua_files,
    TEARDOWN_DATA_DIR, SAVEGAME_PATH, OPTIONS_PATH, TEARDOWN_EXE_PATHS,
    TEST_LOCK_PATH, TEST_CONFIG_PATH, TEST_RESULTS_DIR, TEST_HARNESS_DIR,
)


def test_live_mods_dir_is_documents():
    assert "Documents" in str(LIVE_MODS_DIR)
    assert "Teardown" in str(LIVE_MODS_DIR)


def test_log_path():
    assert "Teardown" in str(LOG_PATH)
    assert str(LOG_PATH).endswith("log.txt")


def test_raw_keys_contains_known():
    assert "rmb" in RAW_KEYS
    assert "lmb" in RAW_KEYS
    assert "mousedx" in RAW_KEYS
    assert "r" in RAW_KEYS


def test_player_inputs_contains_known():
    assert "usetool" in PLAYER_INPUTS
    assert "interact" in PLAYER_INPUTS


def test_raw_keys_and_player_inputs_disjoint():
    assert RAW_KEYS.isdisjoint(PLAYER_INPUTS)


def test_discover_mods(tmp_path):
    (tmp_path / "AK-47").mkdir()
    (tmp_path / "AK-47" / "info.txt").write_text("name = AK-47\n")
    (tmp_path / "AK-47" / "main.lua").write_text("#version 2\n")
    (tmp_path / "Bee_Gun").mkdir()
    (tmp_path / "Bee_Gun" / "info.txt").write_text("name = Bee Gun\n")
    (tmp_path / "Bee_Gun" / "main.lua").write_text("#version 2\n")
    (tmp_path / "random_dir").mkdir()  # no info.txt

    mods = discover_mods(tmp_path)
    assert len(mods) == 2
    names = [m.name for m in mods]
    assert "AK-47" in names
    assert "Bee_Gun" in names


def test_discover_mods_single(tmp_path):
    (tmp_path / "AK-47").mkdir()
    (tmp_path / "AK-47" / "info.txt").write_text("name = AK-47\n")
    (tmp_path / "Bee_Gun").mkdir()
    (tmp_path / "Bee_Gun" / "info.txt").write_text("name = Bee Gun\n")

    mods = discover_mods(tmp_path, mod_name="AK-47")
    assert len(mods) == 1
    assert mods[0].name == "AK-47"


def test_discover_mods_empty(tmp_path):
    mods = discover_mods(tmp_path / "nonexistent")
    assert mods == []


def test_teardown_data_dir():
    assert TEARDOWN_DATA_DIR.name == "Teardown"
    assert "AppData" in str(TEARDOWN_DATA_DIR)


def test_savegame_path():
    assert SAVEGAME_PATH.name == "savegame.xml"
    assert SAVEGAME_PATH.parent == TEARDOWN_DATA_DIR


def test_options_path():
    assert OPTIONS_PATH.name == "options.xml"
    assert OPTIONS_PATH.parent == TEARDOWN_DATA_DIR


def test_teardown_exe_paths_is_list():
    assert isinstance(TEARDOWN_EXE_PATHS, list)
    assert len(TEARDOWN_EXE_PATHS) > 0
    assert all(str(p).endswith("teardown.exe") for p in TEARDOWN_EXE_PATHS)


def test_test_infrastructure_paths():
    assert TEST_LOCK_PATH.name == ".test_lock"
    assert TEST_CONFIG_PATH.name == "test_config.json"
    assert TEST_RESULTS_DIR.name == "test_results"
    assert TEST_HARNESS_DIR.name == "__test_harness"


def test_read_lua_files(tmp_path):
    (tmp_path / "main.lua").write_text("#version 2\nfunction server.init()\nend\n")
    (tmp_path / "options.lua").write_text("function init()\nend\n")

    files = read_lua_files(tmp_path)
    assert len(files) == 2
    paths = [f[0] for f in files]
    assert "main.lua" in paths
    assert "options.lua" in paths
