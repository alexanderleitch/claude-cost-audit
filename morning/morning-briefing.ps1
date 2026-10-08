# Run the read-only morning briefing in a repo and save it to $env:BRIEFING_DIR\yyyy-MM-dd.md.
# Env: BRIEFING_DIR, BRIEFING_MODEL, BRIEFING_EXTRA_TOOLS, CLAUDE_BIN
param([string]$RepoPath = (Get-Location).Path)
$ErrorActionPreference = 'Stop'
$outDir = if ($env:BRIEFING_DIR) { $env:BRIEFING_DIR } else { Join-Path $HOME 'claude-briefings' }
$model = if ($env:BRIEFING_MODEL) { $env:BRIEFING_MODEL } else { 'sonnet' }
$claude = if ($env:CLAUDE_BIN) { $env:CLAUDE_BIN } else { 'claude' }
# Exact commands only: a `:*` wildcard would let text planted in a commit or PR add flags such as
# `git log --output=<file>` or `git fetch --upload-pack=<cmd>`. Keep in sync with briefing-prompt.md.
$tools = 'Bash(git log --remotes --since=24.hours --oneline),Bash(gh pr list --search review-requested:@me),Bash(gh pr list --author @me),Bash(gh run list --limit 5),Bash(gh issue list --assignee @me)'
if ($env:BRIEFING_EXTRA_TOOLS) { $tools += ",$env:BRIEFING_EXTRA_TOOLS" }
New-Item -ItemType Directory -Force $outDir | Out-Null
# Prompt goes in on stdin: Windows PowerShell 5.1 mangles embedded quotes in native arguments
$prompt = Get-Content -Raw (Join-Path $PSScriptRoot 'briefing-prompt.md')
Set-Location $RepoPath
& git fetch --quiet
$prompt | & $claude -p --model $model --allowedTools $tools |
  Out-File -Encoding utf8 (Join-Path $outDir ((Get-Date -Format 'yyyy-MM-dd') + '.md'))
