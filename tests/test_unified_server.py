"""Tests for unified server tools that don't go through MCP transport."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta


def test_handoff_save_and_load(tmp_path):
    """save_handoff writes file, check_handoff reads and deletes it."""
    from mcp_unified_server import server
    old_comms = server.COMMS_DIR
    server.COMMS_DIR = tmp_path
    try:
        (tmp_path / "qa_lead" / "inbox").mkdir(parents=True)
        result = server.save_handoff("qa_lead", "T42", "Working on AWP lint fixes")
        assert result["success"] is True
        assert (tmp_path / "qa_lead" / "handoff.md").exists()

        loaded = server.check_handoff("qa_lead")
        assert loaded["found"] is True
        assert "T42" in loaded["content"]
        assert not (tmp_path / "qa_lead" / "handoff.md").exists()  # deleted after read
    finally:
        server.COMMS_DIR = old_comms


def test_check_handoff_no_file(tmp_path):
    """check_handoff returns string when no handoff exists."""
    from mcp_unified_server import server
    old_comms = server.COMMS_DIR
    server.COMMS_DIR = tmp_path
    try:
        (tmp_path / "qa_lead" / "inbox").mkdir(parents=True)
        result = server.check_handoff("qa_lead")
        assert isinstance(result, str)
        assert "no handoff" in result.lower()
    finally:
        server.COMMS_DIR = old_comms


def test_message_archival_preserves_critical(tmp_path):
    """check_inbox auto-archives old messages but keeps critical ones."""
    from mcp_unified_server import server
    old_comms = server.COMMS_DIR
    server.COMMS_DIR = tmp_path
    try:
        inbox = tmp_path / "qa_lead" / "inbox"
        inbox.mkdir(parents=True)
        # Old non-critical message (2 hours old timestamp in filename)
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=2)).strftime("%Y%m%d_%H%M%S")
        (inbox / f"{old_ts}_api_surgeon_info.md").write_text(
            "---\npriority: low\n---\nOld message", encoding="utf-8"
        )
        # Old critical message (same age)
        (inbox / f"{old_ts}_qa_lead_stop.md").write_text(
            "---\npriority: critical\n---\nSTOP ORDER", encoding="utf-8"
        )
        # Recent message
        now_ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        (inbox / f"{now_ts}_mod_converter_info.md").write_text(
            "---\npriority: low\n---\nRecent message", encoding="utf-8"
        )

        msgs = server.check_inbox("qa_lead")
        # Should return 2: the critical (preserved despite age) + the recent one
        assert isinstance(msgs, list)
        assert len(msgs) == 2
        # Old non-critical should be archived
        archive = tmp_path / "qa_lead" / "archive"
        assert archive.exists()
        assert len(list(archive.glob("*.md"))) == 1
    finally:
        server.COMMS_DIR = old_comms
