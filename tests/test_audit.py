from tools.audit import detect_features, generate_report


def test_detect_shoot():
    src = 'Shoot(pos, dir, "bullet", 1, 100, p, "ak47")\n'
    assert detect_features(src)["has_shoot"] is True


def test_detect_aim_info():
    src = 'local _, sp, ep, d = GetPlayerAimInfo(muzzle, 100, p)\n'
    assert detect_features(src)["has_aim_info"] is True


def test_detect_ammo_pickup():
    src = 'SetToolAmmoPickupAmount("ak47", 10)\n'
    assert detect_features(src)["has_ammo_pickup"] is True


def test_detect_options_menu():
    src = 'data.optionsOpen = false\nUiMakeInteractive()\n'
    assert detect_features(src)["has_options_menu"] is True


def test_detect_options_menu_partial():
    src = 'data.optionsOpen = false\n'  # no UiMakeInteractive
    assert detect_features(src)["has_options_menu"] is False


def test_detect_keybind_remap():
    src = 'local key = GetString("savegame.mod.keys.fire")\n'
    assert detect_features(src)["has_keybind_remap"] is True


def test_detect_ammo_display():
    src = 'SetString("game.tool.ak47.ammo.display", "")\n'
    assert detect_features(src)["has_ammo_display_hidden"] is True


def test_detect_gun_mod_shoot():
    src = 'Shoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
    assert detect_features(src)["is_gun_mod"] is True


def test_detect_gun_mod_makehole():
    src = 'MakeHole(pos, 0.5, 0.5, 0.5)\nlocal ammo = 30\n'
    assert detect_features(src)["is_gun_mod"] is True


def test_detect_nothing():
    src = 'function server.init()\nend\n'
    f = detect_features(src)
    assert f["has_shoot"] is False
    assert f["has_aim_info"] is False
    assert f["is_gun_mod"] is False


def test_generate_report():
    results = [
        {
            "name": "AK-47",
            "features": {
                "has_shoot": True,
                "has_aim_info": False,
                "has_ammo_pickup": False,
                "has_options_menu": False,
                "has_options_guard": False,
                "has_keybind_hints": False,
                "has_keybind_remap": False,
                "has_ammo_display_hidden": True,
                "is_gun_mod": True,
            },
        },
        {
            "name": "Black_Hole",
            "features": {
                "has_shoot": False,
                "has_aim_info": False,
                "has_ammo_pickup": True,
                "has_options_menu": True,
                "has_options_guard": True,
                "has_keybind_hints": True,
                "has_keybind_remap": True,
                "has_ammo_display_hidden": True,
                "is_gun_mod": False,
            },
        },
    ]
    report = generate_report(results)
    assert "AK-47" in report
    assert "Black_Hole" in report
    assert "✓" in report
