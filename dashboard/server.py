"""Team Dashboard Server — visual overview of all terminals, tasks, and project health.

Run: python dashboard/server.py
Opens: http://localhost:8420
"""

import json
import glob
import os
import subprocess
import sys
import time
import webbrowser
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse

PROJECT = Path(__file__).parent.parent
MODS_DIR = Path("C:/Users/trust/Documents/Teardown/mods")
COMMS = PROJECT / ".comms"
TASKS_FILE = PROJECT / "mcp_task_server" / "tasks.json"
ARCHIVE_FILE = PROJECT / "mcp_task_server" / "tasks_archive.json"
CHANGES_FILE = PROJECT / "mcp_change_tracker" / "changes.json"

# Cache lint results (expensive to run)
_lint_cache = {"data": None, "time": 0}
LINT_CACHE_SECONDS = 30


def get_inboxes():
    roles = ["qa_lead", "api_surgeon", "mod_converter", "docs_keeper"]
    # Also detect dynamic roles
    if COMMS.exists():
        for d in COMMS.iterdir():
            if d.is_dir() and (d / "inbox").is_dir() and d.name not in roles and d.name != "__pycache__":
                roles.append(d.name)
    result = {}
    for role in roles:
        inbox = COMMS / role / "inbox"
        outbox = COMMS / role / "outbox"
        msgs = list(inbox.glob("*.md")) if inbox.exists() else []
        sent = list(outbox.glob("*.md")) if outbox.exists() else []
        urgent = 0
        for m in msgs:
            try:
                h = m.read_text(encoding="utf-8", errors="replace")[:300]
                if "priority: critical" in h or "priority: high" in h:
                    urgent += 1
            except:
                pass
        result[role] = {"inbox": len(msgs), "outbox": len(sent), "urgent": urgent}
    return result


def get_tasks():
    if not TASKS_FILE.exists():
        return {"active": [], "open": [], "counts": {}, "by_role": {}}
    data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    tasks = data.get("tasks", [])

    open_t = [t for t in tasks if t["status"] == "open"]
    progress = [t for t in tasks if t["status"] == "in_progress"]
    done = [t for t in tasks if t["status"] == "done"]
    pending_review = [t for t in tasks if t.get("review_status") == "pending"]

    by_role = {}
    for t in tasks:
        r = t["role"]
        by_role.setdefault(r, {"open": 0, "in_progress": 0, "done": 0})
        by_role[r][t["status"]] = by_role[r].get(t["status"], 0) + 1

    # Count archived too
    archived_count = 0
    if ARCHIVE_FILE.exists():
        try:
            arch = json.loads(ARCHIVE_FILE.read_text(encoding="utf-8"))
            archived_count = len(arch.get("archived", []))
        except:
            pass

    return {
        "open": [{"id": t["id"], "title": t["title"], "role": t["role"], "priority": t.get("priority", "medium")} for t in open_t],
        "in_progress": [{"id": t["id"], "title": t["title"], "role": t.get("assigned_to", t["role"]), "started": t.get("started_at", "")} for t in progress],
        "done_count": len(done) + archived_count,
        "pending_review": len(pending_review),
        "total": len(tasks) + archived_count,
        "by_role": by_role,
    }


def get_lint():
    now = time.time()
    if _lint_cache["data"] and (now - _lint_cache["time"]) < LINT_CACHE_SECONDS:
        return _lint_cache["data"]

    try:
        result = subprocess.run(
            [sys.executable, "-m", "tools.lint"],
            capture_output=True, text=True,
            cwd=str(PROJECT), timeout=30,
        )
        output = result.stdout + result.stderr
        fail = output.count("[FAIL]")
        warn = output.count("[WARN]")
        info = output.count("[INFO]")

        # Get summary line
        summary = ""
        for line in output.strip().split("\n"):
            if "mods scanned" in line:
                summary = line.strip()

        data = {"FAIL": fail, "WARN": warn, "INFO": info, "summary": summary}
        _lint_cache["data"] = data
        _lint_cache["time"] = now
        return data
    except:
        return {"FAIL": "?", "WARN": "?", "INFO": "?", "summary": "lint unavailable"}


def get_focus():
    fp = COMMS / "FOCUS.md"
    if fp.exists():
        content = fp.read_text(encoding="utf-8", errors="replace")
        for line in content.split("\n"):
            if line.startswith("## Focus:"):
                return line.replace("## Focus:", "").strip()
    return "Not set"


def get_mod_stats():
    if not MODS_DIR.exists():
        return {"total": 0, "with_options": 0, "with_hints": 0}

    total = 0
    with_options = 0
    with_hints = 0

    for mod_dir in MODS_DIR.iterdir():
        main = mod_dir / "main.lua"
        if not main.exists():
            continue
        total += 1
        try:
            src = main.read_text(encoding="utf-8", errors="replace")
            if "optionsOpen" in src or "optionsopen" in src or "settingsOpen" in src:
                with_options += 1
            if "UiText(" in src and ("Fire" in src or "Reload" in src or "Options" in src):
                with_hints += 1
        except:
            pass

    return {"total": total, "with_options": with_options, "with_hints": with_hints}


def get_killswitch():
    return (COMMS / "STOP").exists()


def get_changes():
    if not CHANGES_FILE.exists():
        return {"total": 0, "undocumented": 0, "recent": []}
    try:
        data = json.loads(CHANGES_FILE.read_text(encoding="utf-8"))
        changes = data.get("changes", [])
        undoc = [c for c in changes if not c.get("documented", False)]
        recent = sorted(changes, key=lambda c: c.get("timestamp", ""), reverse=True)[:5]
        return {"total": len(changes), "undocumented": len(undoc), "recent": recent}
    except:
        return {"total": 0, "undocumented": 0, "recent": []}


def get_servers():
    mcp_json = PROJECT / ".mcp.json"
    if not mcp_json.exists():
        return []
    try:
        data = json.loads(mcp_json.read_text(encoding="utf-8"))
        servers = []
        for name, config in data.get("mcpServers", {}).items():
            script = config.get("args", [""])[0] if config.get("args") else ""
            exists = Path(script).exists() if script else False
            servers.append({"name": name, "script": os.path.basename(script), "exists": exists})
        return servers
    except:
        return []


def build_api_response():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "killswitch": get_killswitch(),
        "focus": get_focus(),
        "inboxes": get_inboxes(),
        "tasks": get_tasks(),
        "lint": get_lint(),
        "mods": get_mod_stats(),
        "changes": get_changes(),
        "servers": get_servers(),
    }


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Teardown MP — Team Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', -apple-system, sans-serif;
    padding: 20px;
    min-height: 100vh;
}
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #21262d;
}
.header h1 {
    font-size: 24px;
    color: #58a6ff;
    font-weight: 600;
}
.header .status {
    display: flex;
    gap: 16px;
    align-items: center;
}
.killswitch {
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.killswitch.active { background: #da3633; color: #fff; }
.killswitch.inactive { background: #238636; color: #fff; }
.focus-bar {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.focus-bar .label { color: #8b949e; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }
.focus-bar .value { color: #f0883e; font-size: 16px; font-weight: 600; }
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    transition: border-color 0.2s;
}
.card:hover { border-color: #58a6ff; }
.card h3 {
    font-size: 14px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}
.card .big-number {
    font-size: 42px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 8px;
}
.card .subtitle { color: #8b949e; font-size: 13px; }
.green { color: #3fb950; }
.yellow { color: #d29922; }
.red { color: #f85149; }
.blue { color: #58a6ff; }
.orange { color: #f0883e; }
.purple { color: #bc8cff; }

/* Terminal cards */
.terminals { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-bottom: 20px; }
.terminal-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 16px;
    position: relative;
    overflow: hidden;
}
.terminal-card .role-name {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.terminal-card .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}
.dot.active { background: #3fb950; box-shadow: 0 0 6px #3fb950; }
.dot.idle { background: #484f58; }
.dot.urgent { background: #f85149; box-shadow: 0 0 6px #f85149; animation: pulse 1s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.terminal-card .stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    font-size: 13px;
}
.terminal-card .stat-label { color: #8b949e; }
.terminal-card .stat-value { font-weight: 600; text-align: right; }

/* Progress bars */
.progress-section { margin-bottom: 20px; }
.progress-section h2 { font-size: 16px; color: #c9d1d9; margin-bottom: 12px; }
.progress-bar-container {
    background: #21262d;
    border-radius: 8px;
    height: 28px;
    overflow: hidden;
    margin-bottom: 8px;
    position: relative;
}
.progress-bar {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
    display: flex;
    align-items: center;
    padding-left: 12px;
    font-size: 12px;
    font-weight: 600;
    color: #fff;
}
.progress-bar.green-bar { background: linear-gradient(90deg, #238636, #2ea043); }
.progress-bar.blue-bar { background: linear-gradient(90deg, #1f6feb, #388bfd); }
.progress-bar.orange-bar { background: linear-gradient(90deg, #9e6a03, #d29922); }
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: #8b949e;
    margin-bottom: 4px;
}

/* Task list */
.task-list { margin-bottom: 20px; }
.task-list h2 { font-size: 16px; color: #c9d1d9; margin-bottom: 12px; }
.task-item {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.task-item .task-title { font-size: 14px; }
.task-item .task-meta { display: flex; gap: 8px; align-items: center; }
.badge {
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
}
.badge.high { background: #da363322; color: #f85149; border: 1px solid #f8514933; }
.badge.medium { background: #d2992222; color: #d29922; border: 1px solid #d2992233; }
.badge.low { background: #23863622; color: #3fb950; border: 1px solid #3fb95033; }
.badge.role { background: #1f6feb22; color: #58a6ff; border: 1px solid #58a6ff33; }

/* Servers */
.servers { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.server-pill {
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
}
.server-pill.online { background: #23863622; color: #3fb950; border: 1px solid #3fb95033; }
.server-pill.offline { background: #da363322; color: #f85149; border: 1px solid #f8514933; }

.timestamp {
    text-align: center;
    color: #484f58;
    font-size: 12px;
    margin-top: 20px;
}
</style>
</head>
<body>

<div class="header">
    <h1>Teardown MP — Team Dashboard</h1>
    <div class="status">
        <div id="killswitch" class="killswitch inactive">RUNNING</div>
        <div style="color: #484f58; font-size: 13px;" id="update-time">updating...</div>
    </div>
</div>

<div class="focus-bar">
    <span class="label">FOCUS</span>
    <span class="value" id="focus">Loading...</span>
</div>

<!-- Terminals -->
<div class="terminals" id="terminals"></div>

<!-- Progress Bars -->
<div class="progress-section">
    <h2>Project Progress</h2>
    <div>
        <div class="progress-label"><span>Tasks Completed</span><span id="task-pct">0%</span></div>
        <div class="progress-bar-container">
            <div class="progress-bar green-bar" id="task-bar" style="width: 0%"></div>
        </div>
    </div>
    <div style="margin-top: 12px;">
        <div class="progress-label"><span>Options Menus</span><span id="options-pct">0%</span></div>
        <div class="progress-bar-container">
            <div class="progress-bar blue-bar" id="options-bar" style="width: 0%"></div>
        </div>
    </div>
    <div style="margin-top: 12px;">
        <div class="progress-label"><span>Keybind Hints</span><span id="hints-pct">0%</span></div>
        <div class="progress-bar-container">
            <div class="progress-bar orange-bar" id="hints-bar" style="width: 0%"></div>
        </div>
    </div>
</div>

<!-- Stats Cards -->
<div class="grid">
    <div class="card">
        <h3>Mods</h3>
        <div class="big-number blue" id="mod-count">0</div>
        <div class="subtitle">installed & patched</div>
    </div>
    <div class="card">
        <h3>Lint Health</h3>
        <div class="big-number" id="lint-number">0</div>
        <div class="subtitle" id="lint-detail">loading...</div>
    </div>
    <div class="card">
        <h3>Changes Tracked</h3>
        <div class="big-number purple" id="changes-count">0</div>
        <div class="subtitle" id="changes-detail">loading...</div>
    </div>
    <div class="card">
        <h3>MCP Servers</h3>
        <div class="servers" id="servers"></div>
    </div>
</div>

<!-- Active Tasks -->
<div class="task-list">
    <h2>Active & Open Tasks</h2>
    <div id="task-items"></div>
</div>

<div class="timestamp" id="footer-time"></div>

<script>
const ROLE_DISPLAY = {
    qa_lead: {name: "QA Lead", icon: "\\u{1F451}"},
    api_surgeon: {name: "API Surgeon", icon: "\\u{1FA78}"},
    mod_converter: {name: "Mod Converter", icon: "\\u{1F527}"},
    docs_keeper: {name: "Docs Keeper", icon: "\\u{1F4DA}"},
};

function updateDashboard(data) {
    // Killswitch
    const ks = document.getElementById("killswitch");
    if (data.killswitch) {
        ks.className = "killswitch active";
        ks.textContent = "STOPPED";
    } else {
        ks.className = "killswitch inactive";
        ks.textContent = "RUNNING";
    }

    // Focus
    document.getElementById("focus").textContent = data.focus || "Not set";

    // Terminals
    const terminalsEl = document.getElementById("terminals");
    terminalsEl.innerHTML = "";
    for (const [role, info] of Object.entries(data.inboxes)) {
        const display = ROLE_DISPLAY[role] || {name: role, icon: "\\u{1F4BB}"};
        const roleTaskInfo = data.tasks.by_role?.[role] || {};
        const isActive = (roleTaskInfo.in_progress || 0) > 0;
        const isUrgent = info.urgent > 0;
        const dotClass = isUrgent ? "urgent" : isActive ? "active" : "idle";

        const activeTask = data.tasks.in_progress?.find(t => t.role === role);
        const taskText = activeTask ? activeTask.title : "Idle";

        terminalsEl.innerHTML += \`
        <div class="terminal-card">
            <div class="role-name"><span class="dot \${dotClass}"></span>\${display.icon} \${display.name}</div>
            <div style="font-size: 12px; color: #8b949e; margin-bottom: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="\${taskText}">\${taskText}</div>
            <div class="stats">
                <span class="stat-label">Inbox</span><span class="stat-value \${info.inbox > 0 ? (info.urgent > 0 ? 'red' : 'yellow') : 'green'}">\${info.inbox}</span>
                <span class="stat-label">Sent</span><span class="stat-value">\${info.outbox}</span>
                <span class="stat-label">Open</span><span class="stat-value">\${roleTaskInfo.open || 0}</span>
                <span class="stat-label">Done</span><span class="stat-value green">\${roleTaskInfo.done || 0}</span>
            </div>
        </div>\`;
    }

    // Progress bars
    const tasks = data.tasks;
    const totalTasks = Math.max(tasks.total || 1, 1);
    const doneCount = tasks.done_count || 0;
    const taskPct = Math.round((doneCount / totalTasks) * 100);
    document.getElementById("task-bar").style.width = taskPct + "%";
    document.getElementById("task-bar").textContent = doneCount + " / " + totalTasks;
    document.getElementById("task-pct").textContent = taskPct + "%";

    const mods = data.mods;
    const modTotal = Math.max(mods.total || 1, 1);
    const optPct = Math.round((mods.with_options / modTotal) * 100);
    document.getElementById("options-bar").style.width = optPct + "%";
    document.getElementById("options-bar").textContent = mods.with_options + " / " + modTotal;
    document.getElementById("options-pct").textContent = optPct + "%";

    const hintPct = Math.round((mods.with_hints / modTotal) * 100);
    document.getElementById("hints-bar").style.width = hintPct + "%";
    document.getElementById("hints-bar").textContent = mods.with_hints + " / " + modTotal;
    document.getElementById("hints-pct").textContent = hintPct + "%";

    // Mod count
    document.getElementById("mod-count").textContent = mods.total;

    // Lint
    const lint = data.lint;
    const lintEl = document.getElementById("lint-number");
    const lintDetail = document.getElementById("lint-detail");
    if (lint.FAIL > 0) {
        lintEl.textContent = lint.FAIL;
        lintEl.className = "big-number red";
        lintDetail.textContent = lint.FAIL + " errors, " + lint.WARN + " warnings";
    } else if (lint.WARN > 0) {
        lintEl.textContent = lint.WARN;
        lintEl.className = "big-number yellow";
        lintDetail.textContent = lint.WARN + " warnings, " + lint.INFO + " info";
    } else {
        lintEl.textContent = "\\u2713";
        lintEl.className = "big-number green";
        lintDetail.textContent = lint.INFO + " info notes (clean)";
    }

    // Changes
    document.getElementById("changes-count").textContent = data.changes.total;
    document.getElementById("changes-detail").textContent = data.changes.undocumented + " undocumented";

    // Servers
    const serversEl = document.getElementById("servers");
    serversEl.innerHTML = "";
    for (const s of data.servers) {
        const cls = s.exists ? "online" : "offline";
        const dot = s.exists ? "\\u25CF" : "\\u25CB";
        serversEl.innerHTML += \`<div class="server-pill \${cls}">\${dot} \${s.name}</div>\`;
    }

    // Tasks
    const taskItems = document.getElementById("task-items");
    taskItems.innerHTML = "";
    const allTasks = [...(tasks.in_progress || []).map(t => ({...t, status: "in_progress"})), ...(tasks.open || []).map(t => ({...t, status: "open"}))];
    if (allTasks.length === 0) {
        taskItems.innerHTML = '<div style="color: #484f58; padding: 12px; text-align: center;">No active or open tasks</div>';
    }
    for (const t of allTasks) {
        const priorityCls = t.priority || "medium";
        const statusBadge = t.status === "in_progress" ? '<span class="badge" style="background:#1f6feb22;color:#58a6ff;border:1px solid #58a6ff33;">IN PROGRESS</span>' : '';
        const display = ROLE_DISPLAY[t.role] || {name: t.role};
        taskItems.innerHTML += \`
        <div class="task-item">
            <span class="task-title">\${t.id} — \${t.title}</span>
            <div class="task-meta">
                <span class="badge role">\${display.name}</span>
                <span class="badge \${priorityCls}">\${priorityCls}</span>
                \${statusBadge}
            </div>
        </div>\`;
    }

    // Timestamps
    const now = new Date();
    document.getElementById("update-time").textContent = "Updated " + now.toLocaleTimeString();
    document.getElementById("footer-time").textContent = "Auto-refreshes every 5 seconds";
}

async function fetchData() {
    try {
        const res = await fetch("/api/status");
        const data = await res.json();
        updateDashboard(data);
    } catch (e) {
        document.getElementById("update-time").textContent = "Error: " + e.message;
    }
}

fetchData();
setInterval(fetchData, 5000);
</script>
</body>
</html>"""


class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            data = build_api_response()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress request logging


def main():
    port = 8420
    server = HTTPServer(("localhost", port), DashboardHandler)
    print(f"Dashboard running at http://localhost:{port}")
    print("Press Ctrl+C to stop")

    # Open in browser
    def open_browser():
        time.sleep(1)
        webbrowser.open(f"http://localhost:{port}")

    Thread(target=open_browser, daemon=True).start()
    server.serve_forever()


if __name__ == "__main__":
    main()
