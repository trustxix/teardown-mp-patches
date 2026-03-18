@echo off
title Teardown MP Patcher — Team Launcher
echo.
echo ============================================
echo  Teardown MP Patcher — 3-Terminal Team
echo ============================================
echo.
echo This will open 3 Claude Code terminals.
echo Each will start in the project directory
echo with the MCP server and its role loaded.
echo.
echo Press any key to launch all 3...
pause >nul

echo.
echo [1/3] Launching API Surgeon...
start "API Surgeon" cmd /k "cd /d C:\Users\trust\teardown-mp-patches && claude "Read ROLE_API_SURGEON.md and start your autonomous work loop. You are api_surgeon. Run tools.status first, approve the MCP server when prompted, then use check_inbox and get_task to find work. Keep working forever.""

timeout /t 5 >nul

echo [2/3] Launching Mod Converter...
start "Mod Converter" cmd /k "cd /d C:\Users\trust\teardown-mp-patches && claude "Read ROLE_MOD_CONVERTER.md and start your autonomous work loop. You are mod_converter. Run tools.status first, approve the MCP server when prompted, then use check_inbox and get_task to find work. Keep working forever.""

timeout /t 5 >nul

echo [3/3] Launching QA Lead...
start "QA Lead" cmd /k "cd /d C:\Users\trust\teardown-mp-patches && claude "Read ROLE_QA_LEAD.md and start your autonomous work loop. You are qa_lead. Run tools.status first, approve the MCP server when prompted, then use check_inbox and get_task to find work. Keep working forever.""

echo.
echo ============================================
echo  All 3 terminals launched!
echo.
echo  NOTE: Each terminal will ask you to
echo  approve the task-coordinator MCP server
echo  on first run. Press Y to approve.
echo.
echo  After that, they work autonomously.
echo  Close this window anytime.
echo ============================================
echo.
pause
