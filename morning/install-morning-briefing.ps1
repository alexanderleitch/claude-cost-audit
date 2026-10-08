# Register a daily Windows scheduled task that runs morning-briefing.ps1, waking the PC if asleep.
# Usage: powershell -ExecutionPolicy Bypass -File install-morning-briefing.ps1 -RepoPath C:\code\myrepo [-At 5am]
param(
  [Parameter(Mandatory)][string]$RepoPath,
  [string]$At = '5am',
  [string]$TaskName = 'ClaudeMorningBriefing'
)
$ErrorActionPreference = 'Stop'
$runner = Join-Path $PSScriptRoot 'morning-briefing.ps1'
$repo = (Resolve-Path $RepoPath).Path
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$runner`" -RepoPath `"$repo`""
$trigger = New-ScheduledTaskTrigger -Daily -At $At
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null
"Registered '$TaskName' daily at $At for $repo."
"Test now:  Start-ScheduledTask $TaskName   then look in $HOME\claude-briefings"
"Remove:    Unregister-ScheduledTask $TaskName"
