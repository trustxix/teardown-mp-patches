from tools.audit import detect_features, generate_report, check_duplicate_tool_ids


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


def test_detect_register_tool():
    src = 'RegisterTool("ak47", "AK-47", "MOD/vox/ak47.xml", 6)\n'
    assert detect_features(src)["has_register_tool"] is True


def test_detect_no_register_tool():
    src = 'function server.init()\nend\n'
    assert detect_features(src)["has_register_tool"] is False


def test_detect_nothing():
    src = 'function server.init()\nend\n'
    f = detect_features(src)
    assert f["has_shoot"] is False
    assert f["has_aim_info"] is False
    assert f["is_gun_mod"] is False
    assert f["has_register_tool"] is False


def test_generate_report():
    results = [
        {
            "name": "AK-47",
            "features": {
                "has_shoot": True,
                "has_aim_info": False,
                "has_ammo_pickup": False,
                "has_register_tool": True,
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
                "has_register_tool": True,
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
    assert "Y" in report


def test_detect_options_guard_early_return():
    src = 'if data.optionsOpen then return end\nif InputPressed("usetool") then\nend\n'
    assert detect_features(src)["has_options_guard"] is True


def test_detect_options_guard_missing():
    src = 'if InputPressed("usetool") then\nend\n'
    assert detect_features(src)["has_options_guard"] is False


def test_detect_keybind_hints():
    src = 'UiText("Press LMB to fire")\n'
    assert detect_features(src)["has_keybind_hints"] is True


def test_detect_keybind_hints_missing():
    src = 'UiText("Hello world")\n'
    assert detect_features(src)["has_keybind_hints"] is False


def test_detect_audit_suppression():
    src = '-- @audit-ok AimInfo\nShoot(pos, dir, "bullet", 1, 100, p, "gun")\n'
    f = detect_features(src)
    assert "aiminfo" in f["suppressions"]
    assert f["has_shoot"] is True


# ── Tool ID extraction & duplicate detection ─────────────────────────────────

def test_detect_tool_ids():
    src = 'RegisterTool("mygun", "My Gun", "MOD/gun.xml", 3)\n'
    f = detect_features(src)
    assert "mygun" in f["tool_ids"]


def test_detect_multiple_tool_ids():
    src = (
        'RegisterTool("primary", "Primary", "MOD/a.xml", 1)\n'
        'RegisterTool("secondary", "Secondary", "MOD/b.xml", 2)\n'
    )
    f = detect_features(src)
    assert f["tool_ids"] == {"primary", "secondary"}


def test_detect_tool_ids_in_comment_ignored():
    src = '-- RegisterTool("old", "Old", "MOD/old.xml")\n'
    f = detect_features(src)
    assert len(f["tool_ids"]) == 0


def test_no_duplicate_tool_ids():
    results = [
        {"name": "ModA", "features": {"tool_ids": {"gun_a"}}},
        {"name": "ModB", "features": {"tool_ids": {"gun_b"}}},
    ]
    assert check_duplicate_tool_ids(results) == []


def test_duplicate_tool_ids_detected():
    results = [
        {"name": "ModA", "features": {"tool_ids": {"mygun"}}},
        {"name": "ModB", "features": {"tool_ids": {"mygun"}}},
    ]
    warnings = check_duplicate_tool_ids(results)
    assert len(warnings) == 1
    assert "mygun" in warnings[0]
    assert "ModA" in warnings[0]
    assert "ModB" in warnings[0]


def test_duplicate_tool_ids_multiple_conflicts():
    results = [
        {"name": "ModA", "features": {"tool_ids": {"gun1", "gun2"}}},
        {"name": "ModB", "features": {"tool_ids": {"gun1"}}},
        {"name": "ModC", "features": {"tool_ids": {"gun2", "gun3"}}},
    ]
    warnings = check_duplicate_tool_ids(results)
    assert len(warnings) == 2  # gun1 and gun2 are duplicated
