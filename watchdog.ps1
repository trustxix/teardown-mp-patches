# watchdog.ps1 — Terminal health monitor for Teardown MP Patcher team
# Started by launch_team.bat. Monitors heartbeats, restarts dead terminals.
#
# Usage: pwsh -File watchdog.ps1 -ConfigFile watchdog_config.json

param(
    [string]$ConfigFile = "watchdog_config.json",
    [int]$CheckIntervalSeconds = 30,
    [int]$StaleMinutes = 5,
    [int]$MaxRestarts = 3
)

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$HeartbeatFile = Join-Path $ProjectRoot ".comms\heartbeats.json"
$StopFile = Join-Path $ProjectRoot ".comms\STOP"
$LogFile = Join-Path $ProjectRoot "logs\watchdog.log"
$PidFile = Join-Path $ProjectRoot "logs\watchdog.pid"
$ConfigPath = Join-Path $ProjectRoot $ConfigFile

# Write PID
$PID | Out-File -FilePath $PidFile -NoNewline

# Track restarts per terminal
$restartCounts = @{}

function Write-Log {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$ts] $Message"
    Add-Content -Path $LogFile -Value $entry
    Write-Host $entry
}

function Get-Config {
    if (-not (Test-Path $ConfigPath)) {
        Write-Log "ERROR: Config file not found: $ConfigPath"
        return $null
    }
    return Get-Content $ConfigPath -Raw | ConvertFrom-Json
}

function Get-Heartbeats {
    if (-not (Test-Path $HeartbeatFile)) { return $null }
    try {
        return Get-Content $HeartbeatFile -Raw | ConvertFrom-Json
    } catch {
        return $null
    }
}

function Restart-Terminal {
    param([string]$Role, [string]$Command, [string]$Title)

    if (-not $restartCounts.ContainsKey($Role)) {
        $restartCounts[$Role] = 0
    }

    if ($restartCounts[$Role] -ge $MaxRestarts) {
        Write-Log "RESTART_LIMIT_REACHED: $Role has been restarted $MaxRestarts times. Skipping."
        return
    }

    Write-Log "RESTARTING: $Role (restart #$($restartCounts[$Role] + 1)/$MaxRestarts)"
    $restartCounts[$Role]++

    try {
        Start-Process -FilePath "C:\Program Files\PowerShell\7\pwsh.exe" `
            -ArgumentList "-NoExit", "-Command", $Command `
            -WindowStyle Normal
        Write-Log "RESTARTED: $Role successfully"
    } catch {
        Write-Log "RESTART_FAILED: $Role — $_"
    }
}

# Main loop
Write-Log "Watchdog started. Check interval: ${CheckIntervalSeconds}s, Stale threshold: ${StaleMinutes}m, Max restarts: $MaxRestarts"

while ($true) {
    Start-Sleep -Seconds $CheckIntervalSeconds

    # Respect killswitch
    if (Test-Path $StopFile) {
        Write-Log "Killswitch active — skipping health check"
        continue
    }

    $config = Get-Config
    if ($null -eq $config) { continue }

    $heartbeats = Get-Heartbeats
    $now = [DateTimeOffset]::UtcNow

    foreach ($terminal in $config.terminals) {
        $role = $terminal.role
        $hb = $null
        if ($null -ne $heartbeats) {
            $hb = $heartbeats.$role
        }

        if ($null -eq $hb -or $null -eq $hb.timestamp) {
            # Never seen — might still be starting up. Skip for first 2 minutes.
            continue
        }

        try {
            $lastSeen = [DateTimeOffset]::Parse($hb.timestamp)
            $elapsed = ($now - $lastSeen).TotalMinutes

            if ($elapsed -gt $StaleMinutes) {
                Write-Log "STALE: $role — last seen ${elapsed:F1}m ago"
                Restart-Terminal -Role $role -Command $terminal.command -Title $terminal.title
            }
        } catch {
            Write-Log "PARSE_ERROR: $role heartbeat timestamp: $_"
        }
    }
}
