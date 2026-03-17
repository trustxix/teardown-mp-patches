from tools.status import build_status_report


def test_status_report_has_header(tmp_path):
    (tmp_path / "TestMod").mkdir()
    (tmp_path / "TestMod" / "info.txt").write_text("name = Test\nversion = 2\n")
    (tmp_path / "TestMod" / "main.lua").write_text("#version 2\nfunction server.init()\nend\n")

    report = build_status_report(mods_dir=tmp_path, skip_git=True, skip_log=True)
    assert "TEARDOWN MP PATCHER" in report
    assert "Status" in report


def test_status_report_mod_count(tmp_path):
    for name in ["Mod1", "Mod2", "Mod3"]:
        (tmp_path / name).mkdir()
        (tmp_path / name / "info.txt").write_text(f"name = {name}\n")
        (tmp_path / name / "main.lua").write_text("#version 2\n")

    report = build_status_report(mods_dir=tmp_path, skip_git=True, skip_log=True)
    assert "3" in report


def test_status_report_no_mods(tmp_path):
    report = build_status_report(mods_dir=tmp_path, skip_git=True, skip_log=True)
    assert "0" in report


def test_status_report_lint_clean(tmp_path):
    (tmp_path / "Clean").mkdir()
    (tmp_path / "Clean" / "info.txt").write_text("name = Clean\n")
    (tmp_path / "Clean" / "main.lua").write_text("#version 2\nfunction server.init()\nend\n")

    report = build_status_report(mods_dir=tmp_path, skip_git=True, skip_log=True)
    assert "0 hard errors" in report


def test_status_report_lint_errors(tmp_path):
    (tmp_path / "Bad").mkdir()
    (tmp_path / "Bad" / "info.txt").write_text("name = Bad\n")
    (tmp_path / "Bad" / "main.lua").write_text('#version 2\nfor _, p in ipairs(Players()) do\nend\n')

    report = build_status_report(mods_dir=tmp_path, skip_git=True, skip_log=True)
    assert "hard error" in report
