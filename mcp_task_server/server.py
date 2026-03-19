"""MCP Task Coordination Server for Teardown MP Patches.

Connects 3 Claude Code terminals via stdio transport.
Each terminal calls tools to get tasks, report progress, and coordinate.
"""

import subprocess
import sys
from pathlib import Path

from mcp.server import FastMCP

# Add project root to path so we can import tools
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mcp_task_server import task_store

mcp = FastMCP(
    name="task-coordinator",
    instructions=(
        "Task coordination server for Teardown MP Patches. "
        "Manages a shared task queue across 3 terminals: "
        "API Surgeon, Mod Converter, and QA Lead."
    ),
)


@mcp.tool(description="Get the next open task for a role. Marks it IN_PROGRESS and broadcasts to all terminals that you're starting it. Returns null if no tasks available.")
def get_task(role: str) -> dict | str:
    """Get next task for role and broadcast that you're starting it."""
    valid_roles = {"api_surgeon", "mod_converter", "qa_lead", "docs_keeper"}
    if role not in valid_roles:
        return f"Invalid role '{role}'. Must be one of: {', '.join(sorted(valid_roles))}"
    task = task_store.get_next_task(role)
    if task is None:
        return f"No open tasks for {role}"
    # Auto-broadcast start to all other terminals
    mods_str = ", ".join(task.get("mods", [])[:5]) or "general"
    msg = f"STARTING: [{task['id']}] {task['title']} — mods: {mods_str}"
    broadcast(role, "info", "low", msg)
    return task


@mcp.tool(description="Mark a task as DONE with a completion summary. Auto-broadcasts completion to all terminals.")
def complete_task(task_id: str, summary: str) -> dict:
    """Complete a task and broadcast that you're done."""
    # Find the task to get role info before completing
    all_tasks = task_store.get_all_tasks()
    role = None
    title = None
    for t in all_tasks.get("tasks", []):
        if t["id"] == task_id:
            role = t.get("assigned_to") or t.get("role")
            title = t.get("title", "")
            break
    success = task_store.complete_task(task_id, summary)
    if success:
        # Auto-broadcast completion to all other terminals
        if role:
            msg = f"FINISHED: [{task_id}] {title}\n{summary}"
            broadcast(role, "info", "low", msg)
        return {"success": True, "task_id": task_id, "message": "Task completed and team notified."}
    return {"success": False, "message": f"Task '{task_id}' not found"}


@mcp.tool(description="Create a new task in the queue. Any terminal can call this.")
def create_task(title: str, role: str, priority: str, description: str, mods: list[str] | None = None) -> dict:
    """Create a new task. Priority: critical, high, medium, low."""
    valid_roles = {"api_surgeon", "mod_converter", "qa_lead", "docs_keeper"}
    valid_priorities = {"critical", "high", "medium", "low"}
    if role not in valid_roles:
        return {"success": False, "message": f"Invalid role. Must be one of: {', '.join(sorted(valid_roles))}"}
    if priority not in valid_priorities:
        return {"success": False, "message": f"Invalid priority. Must be one of: {', '.join(sorted(valid_priorities))}"}
    task_id = task_store.create_task(title, role, priority, description, mods)
    return {"success": True, "task_id": task_id}


@mcp.tool(description="QA review of a completed task. If not approved, reopens it with notes for the assignee.")
def review_task(task_id: str, approved: bool, notes: str) -> dict:
    """Review a completed task. Set approved=false to reopen with notes."""
    success = task_store.review_task(task_id, approved, notes)
    if success:
        status = "approved" if approved else "rejected and reopened"
        return {"success": True, "task_id": task_id, "status": status}
    return {"success": False, "message": f"Task '{task_id}' not found"}


@mcp.tool(description="Get full queue status: counts per role, active tasks, recently completed, pending reviews.")
def get_status() -> dict:
    """Returns complete task queue status."""
    return task_store.get_all_tasks()


@mcp.tool(description="Run the project linter and return summary of findings (FAIL/WARN/INFO counts). Use to discover new work.")
def get_lint_summary() -> dict:
    """Runs python -m tools.lint and returns the summary."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.lint"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=180,
        )
        output = result.stdout + result.stderr
        # Parse counts from output
        lines = output.strip().split("\n")
        counts = {"FAIL": 0, "WARN": 0, "INFO": 0}
        findings = []
        for line in lines:
            for level in counts:
                if f"[{level}]" in line:
                    counts[level] += 1
                    findings.append(line.strip())
        return {
            "success": result.returncode == 0,
            "counts": counts,
            "total_findings": sum(counts.values()),
            "findings": findings[:50],  # Cap at 50 to avoid huge responses
            "raw_summary": "\n".join(lines[-20:]),  # Last 20 lines as summary
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Lint timed out after 180s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(description="Run the project audit and return the feature matrix. Use to identify gaps in mod coverage.")
def get_audit_summary() -> dict:
    """Runs python -m tools.audit and returns the feature matrix."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.audit"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=180,
        )
        output = result.stdout + result.stderr
        return {
            "success": result.returncode == 0,
            "report": output.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Audit timed out after 180s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


##############################################################################
# INBOX / MESSAGING TOOLS
##############################################################################

COMMS_DIR = PROJECT_ROOT / ".comms"
ROLES_MAP = {"api_surgeon": "api_surgeon", "mod_converter": "mod_converter", "qa_lead": "qa_lead", "docs_keeper": "docs_keeper"}


def _timestamp() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


@mcp.tool(description="Quick check: do you have unread messages? Call this frequently between tool calls. Cheap and fast.")
def has_mail(role: str) -> dict:
    """Returns whether you have messages waiting and how many."""
    if role not in ROLES_MAP:
        return {"error": f"Invalid role. Must be one of: {', '.join(sorted(ROLES_MAP))}"}
    inbox = COMMS_DIR / role / "inbox"
    if not inbox.exists():
        return {"has_mail": False, "count": 0}
    messages = list(inbox.glob("*.md"))
    critical = sum(1 for m in messages if "critical" in m.read_text(encoding="utf-8", errors="replace").lower()[:200])
    return {"has_mail": len(messages) > 0, "count": len(messages), "critical": critical}


@mcp.tool(description="Read the current team focus area. All terminals should work on this area.")
def get_focus() -> str:
    """Returns the current team focus from .comms/FOCUS.md."""
    focus_path = COMMS_DIR / "FOCUS.md"
    if focus_path.exists():
        return focus_path.read_text(encoding="utf-8", errors="replace")
    return "No focus set. QA Lead should set one."


@mcp.tool(description="Check your inbox for new messages from other terminals. Returns list of messages sorted oldest-first.")
def check_inbox(role: str) -> list[dict] | str:
    """Read all messages in your inbox. Role: 'api_surgeon', 'mod_converter', 'qa_lead'."""
    if role not in ROLES_MAP:
        return f"Invalid role. Must be one of: {', '.join(sorted(ROLES_MAP))}"
    inbox = COMMS_DIR / role / "inbox"
    if not inbox.exists():
        return []
    messages = []
    for f in sorted(inbox.glob("*.md")):
        content = f.read_text(encoding="utf-8", errors="replace")
        messages.append({"filename": f.name, "content": content})
    return messages if messages else "Inbox empty"


@mcp.tool(description="Send a message to another terminal's inbox. Also logs to your outbox.")
def send_message(from_role: str, to_role: str, msg_type: str, priority: str, content: str, re: str | None = None) -> dict:
    """Send a message. type: task|question|review|info|result. priority: critical|high|medium|low."""
    if from_role not in ROLES_MAP or to_role not in ROLES_MAP:
        return {"success": False, "message": f"Invalid role. Must be one of: {', '.join(sorted(ROLES_MAP))}"}
    valid_types = {"task", "question", "review", "info", "result"}
    if msg_type not in valid_types:
        return {"success": False, "message": f"Invalid type. Must be one of: {', '.join(sorted(valid_types))}"}

    ts = _timestamp()
    filename = f"{ts}_{from_role}_{msg_type}.md"
    header = f"---\nfrom: {from_role}\nto: {to_role}\ntype: {msg_type}\npriority: {priority}\n"
    if re:
        header += f"re: {re}\n"
    header += "---\n\n"
    full = header + content

    # Write to recipient's inbox
    inbox_path = COMMS_DIR / to_role / "inbox" / filename
    inbox_path.write_text(full, encoding="utf-8")

    # Log to sender's outbox
    outbox_path = COMMS_DIR / from_role / "outbox" / filename
    outbox_path.write_text(full, encoding="utf-8")

    return {"success": True, "filename": filename, "delivered_to": f"{to_role}/inbox"}


@mcp.tool(description="Broadcast a message to all other terminals' inboxes.")
def broadcast(from_role: str, msg_type: str, priority: str, content: str) -> dict:
    """Send a message to all terminals except yourself."""
    results = []
    for role in ROLES_MAP:
        if role != from_role:
            r = send_message(from_role, role, msg_type, priority, content)
            results.append(r)
    return {"success": True, "delivered_to": [r.get("delivered_to") for r in results if isinstance(r, dict)]}


@mcp.tool(description="Delete a processed message from your inbox.")
def clear_message(role: str, filename: str) -> dict:
    """Remove a message from your inbox after processing it."""
    if role not in ROLES_MAP:
        return {"success": False, "message": "Invalid role"}
    path = COMMS_DIR / role / "inbox" / filename
    if path.exists():
        path.unlink()
        return {"success": True, "deleted": filename}
    return {"success": False, "message": f"File not found: {filename}"}


##############################################################################
# TEAM DASHBOARD
##############################################################################


@mcp.tool(description="One-command team overview: all terminals' inbox counts, active tasks, task queue health, lint summary, and killswitch status. The user's 'what's going on' button.")
def team_dashboard() -> dict:
    """Full team status in one call."""
    import glob

    dashboard = {}

    # Inbox counts per terminal
    inboxes = {}
    for role in ROLES_MAP:
        inbox_dir = COMMS_DIR / role / "inbox"
        if inbox_dir.exists():
            msgs = list(inbox_dir.glob("*.md"))
            inboxes[role] = {"count": len(msgs), "urgent": sum(1 for m in msgs if "critical" in m.read_text(encoding="utf-8", errors="replace")[:200].lower())}
        else:
            inboxes[role] = {"count": 0, "urgent": 0}
    dashboard["inboxes"] = inboxes

    # Task queue summary
    all_tasks = task_store.get_all_tasks()
    dashboard["tasks"] = {
        "open": all_tasks["counts"].get("open", 0),
        "in_progress": all_tasks["counts"].get("in_progress", 0),
        "done": all_tasks["counts"].get("done", 0),
        "pending_review": len(all_tasks.get("pending_review", [])),
        "active": [{"id": t["id"], "title": t["title"], "role": t.get("assigned_to", t["role"])} for t in all_tasks.get("active", [])],
    }

    # Per-role task counts
    dashboard["by_role"] = all_tasks.get("by_role", {})

    # Killswitch status
    dashboard["killswitch"] = KILLSWITCH_FILE.exists()

    # Focus area
    focus_path = COMMS_DIR / "FOCUS.md"
    if focus_path.exists():
        lines = focus_path.read_text(encoding="utf-8").split("\n")
        for line in lines:
            if line.startswith("## Focus:"):
                dashboard["focus"] = line.replace("## Focus:", "").strip()
                break
        else:
            dashboard["focus"] = "Set in .comms/FOCUS.md"
    else:
        dashboard["focus"] = "Not set"

    # Quick lint health (just counts, not full run)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.lint"],
            capture_output=True, text=True,
            cwd=str(PROJECT_ROOT), timeout=30,
        )
        output = result.stdout + result.stderr
        fail = output.count("[FAIL]")
        warn = output.count("[WARN]")
        info = output.count("[INFO]")
        dashboard["lint"] = {"FAIL": fail, "WARN": warn, "INFO": info}
    except Exception:
        dashboard["lint"] = "unavailable"

    return dashboard


##############################################################################
# AUTO-TASK GENERATION FROM LINT
##############################################################################


@mcp.tool(description="Generate tasks from current lint findings. Groups warnings by mod, creates one task per mod. QA Lead runs this to fill the queue.")
def generate_tasks_from_lint(role: str = "api_surgeon", priority: str = "medium") -> dict:
    """Run lint, parse findings, create tasks for each mod with warnings. Skips mods that already have open tasks."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.lint", "--json-output"],
            capture_output=True, text=True,
            cwd=str(PROJECT_ROOT), timeout=180,
        )
        all_results = __import__("json").loads(result.stdout)
    except Exception as e:
        return {"success": False, "error": str(e)}

    # Get existing open tasks to avoid duplicates
    existing = task_store.get_all_tasks()
    existing_mods = set()
    for t in existing.get("tasks", []):
        if t.get("status") in ("open", "in_progress"):
            for m in t.get("mods", []):
                existing_mods.add(m)

    created = []
    skipped = []
    for mod_name, findings in all_results.items():
        warns = [f for f in findings if f.get("severity") in ("error", "warn")]
        if not warns:
            continue
        if mod_name in existing_mods:
            skipped.append(mod_name)
            continue

        # Group by check type
        by_check = {}
        for f in warns:
            check = f.get("check", "UNKNOWN")
            by_check.setdefault(check, []).append(f)

        check_summary = ", ".join(f"{c}: {len(fs)}" for c, fs in by_check.items())
        desc = f"Fix {len(warns)} lint warning(s) in {mod_name}: {check_summary}. Run `python -m tools.lint --mod \"{mod_name}\"` for details."

        # Add fix guide reference for PER-TICK-RPC
        if "PER-TICK-RPC" in by_check:
            desc += " Read docs/PER_TICK_RPC_FIX_GUIDE.md for fix patterns."

        task_id = task_store.create_task(
            title=f"LINT-FIX: {mod_name} ({len(warns)} warnings)",
            role=role,
            priority=priority,
            description=desc,
            mods=[mod_name],
        )
        created.append({"task_id": task_id, "mod": mod_name, "warnings": len(warns)})

    return {
        "success": True,
        "created": len(created),
        "skipped": len(skipped),
        "tasks": created,
        "skipped_mods": skipped,
        "message": f"Created {len(created)} tasks, skipped {len(skipped)} (already have open tasks)."
    }


##############################################################################
# TERMINAL HEARTBEAT
##############################################################################

_heartbeats: dict[str, str] = {}


@mcp.tool(description="Report that you are alive and working. Call this every few minutes so the dashboard can track terminal health.")
def heartbeat(role: str, status: str = "working") -> dict:
    """Record a heartbeat. Status: 'working', 'idle', 'blocked'."""
    from datetime import datetime, timezone
    if role not in ROLES_MAP:
        return {"error": f"Invalid role. Must be one of: {', '.join(sorted(ROLES_MAP))}"}
    ts = datetime.now(timezone.utc).isoformat()
    _heartbeats[role] = ts
    # Write to file so dashboard can read it
    hb_file = COMMS_DIR / "heartbeats.json"
    try:
        import json
        data = {}
        if hb_file.exists():
            data = json.loads(hb_file.read_text(encoding="utf-8"))
        data[role] = {"timestamp": ts, "status": status}
        hb_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass
    return {"recorded": True, "role": role, "timestamp": ts}


@mcp.tool(description="Get heartbeat status for all terminals. Shows when each was last seen.")
def get_heartbeats() -> dict:
    """Returns last-seen timestamps for all terminals."""
    import json
    hb_file = COMMS_DIR / "heartbeats.json"
    if not hb_file.exists():
        return {r: {"status": "unknown", "last_seen": "never"} for r in ROLES_MAP}
    try:
        return json.loads(hb_file.read_text(encoding="utf-8"))
    except Exception:
        return {r: {"status": "unknown", "last_seen": "never"} for r in ROLES_MAP}


##############################################################################
# KILLSWITCH
##############################################################################

KILLSWITCH_FILE = COMMS_DIR / "STOP"


@mcp.tool(description="Activate the killswitch. Broadcasts STOP to all terminals and creates the STOP file. All terminals will finish their current task and halt.")
def killswitch() -> dict:
    """QA Lead activates this when the user says 'stop'. Broadcasts to all terminals."""
    KILLSWITCH_FILE.write_text("STOP — Finish your current task, then halt. Wait for further instructions.", encoding="utf-8")
    # Broadcast to all inboxes
    for role in ROLES_MAP:
        msg = "---\nfrom: qa_lead\nto: " + role + "\ntype: info\npriority: critical\n---\n\nSTOP ORDER: Finish your current task, then HALT. Do not pick up new tasks. Do not check the queue. Wait for further instructions from the user."
        inbox = COMMS_DIR / role / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        ts = _timestamp()
        (inbox / f"{ts}_qa_lead_stop.md").write_text(msg, encoding="utf-8")
    return {"success": True, "message": "Killswitch activated. STOP broadcast sent to all terminals."}


@mcp.tool(description="Check if the killswitch is active. ALL terminals must call this at the start of every loop iteration.")
def check_killswitch() -> dict:
    """Returns whether the STOP file exists. If true, terminal must halt after current task."""
    active = KILLSWITCH_FILE.exists()
    return {"active": active}


@mcp.tool(description="Deactivate the killswitch so terminals can resume work.")
def clear_killswitch() -> dict:
    """Removes the STOP file and broadcasts RESUME to all terminals."""
    if KILLSWITCH_FILE.exists():
        KILLSWITCH_FILE.unlink()
    for role in ROLES_MAP:
        msg = "---\nfrom: qa_lead\nto: " + role + "\ntype: info\npriority: critical\n---\n\nRESUME ORDER: Killswitch cleared. Resume your autonomous work loop."
        inbox = COMMS_DIR / role / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        ts = _timestamp()
        (inbox / f"{ts}_qa_lead_resume.md").write_text(msg, encoding="utf-8")
    return {"success": True, "message": "Killswitch cleared. RESUME broadcast sent to all terminals."}


##############################################################################
# TEAM MEMBER SPAWNING
##############################################################################

DESKTOP = Path("C:/Users/trust/Desktop")
PWSH = "C:\\Program Files\\PowerShell\\7\\pwsh.exe"


@mcp.tool(description="Create a new team member: writes role file, creates inbox, adds to valid roles, creates desktop launcher, and updates launch_team.bat. QA Lead only.")
def spawn_terminal(role_name: str, display_name: str, role_description: str, role_file_content: str) -> dict:
    """Create a new team member terminal with full integration.

    role_name: lowercase_underscore identifier (e.g., 'test_runner')
    display_name: human-readable name (e.g., 'Test Runner')
    role_description: one-line description for broadcasts
    role_file_content: full markdown content for ROLE_{NAME}.md
    """
    try:
        role_file = f"ROLE_{role_name.upper()}.md"
        role_path = PROJECT_ROOT / role_file

        # 1. Write role file
        role_path.write_text(role_file_content, encoding="utf-8")

        # 2. Create inbox/outbox
        (COMMS_DIR / role_name / "inbox").mkdir(parents=True, exist_ok=True)
        (COMMS_DIR / role_name / "outbox").mkdir(parents=True, exist_ok=True)

        # 3. Add to valid roles (in-memory for this session)
        ROLES_MAP[role_name] = role_name

        # 4. Create individual desktop launcher
        launcher = DESKTOP / f"launch_{role_name}.bat"
        prompt = f"Read {role_file} and start your autonomous work loop. You are {role_name}. Run tools.status first, then get_focus, check_inbox, and get_task to find work. Keep working forever."
        bat = f'@echo off\nstart "{display_name}" "{PWSH}" -NoExit -Command "cd C:\\Users\\trust\\teardown-mp-patches; claude --dangerously-skip-permissions \'{prompt}\'"\n'
        launcher.write_text(bat, encoding="utf-8")

        # 5. Update launch_team.bat to include new member
        team_bat = DESKTOP / "launch_team.bat"
        if team_bat.exists():
            content = team_bat.read_text(encoding="utf-8")
            # Find the last "timeout" line and insert after it
            insert_block = f'\ntimeout /t 5 >nul\n\necho [+] {display_name}...\nstart "{display_name}" "{PWSH}" -NoExit -Command "cd C:\\Users\\trust\\teardown-mp-patches; claude --dangerously-skip-permissions \'{prompt}\'"\n'
            # Insert before the final echo/timeout block
            if "All" in content and "launched" in content:
                parts = content.rsplit("echo.", 1)
                if len(parts) == 2:
                    content = parts[0] + insert_block + "\necho." + parts[1]
                    # Update the terminal count in the title
                    import re
                    content = re.sub(r'(\d+)-Terminal', lambda m: f'{int(m.group(1))+1}-Terminal', content, count=1)
                    content = re.sub(r'(\d+) terminals', lambda m: f'{int(m.group(1))+1} terminals', content, count=1, flags=re.IGNORECASE)
                    team_bat.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "role_name": role_name,
            "role_file": role_file,
            "launcher": str(launcher),
            "inbox": f".comms/{role_name}/inbox/",
            "message": f"Terminal '{display_name}' created. Launch via desktop shortcut or launch_team.bat."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
