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
