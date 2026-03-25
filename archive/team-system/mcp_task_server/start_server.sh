#!/usr/bin/env bash
# Launch the MCP Task Coordination Server (stdio transport)
# Claude Code connects to this automatically via MCP config.
# Manual launch is only needed for testing.

cd "$(dirname "$0")/.." || exit 1
python -m mcp_task_server.server
