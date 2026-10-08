# claude-cost-audit

Find out what Claude Code loads into **every turn** of every session, so you can disable what you
don't use and stretch your plan's usage further.

Output-shortening plugins only trim Claude's replies. Most usage is *input*: the system prompt,
plugin skill listings, MCP tool schemas, hook output and instruction files are re-sent on every
turn. This script ranks those so the big, unused ones are obvious.

Read-only. No dependencies. Python 3.8+ on macOS, Linux and Windows.

## Run it (no git needed)

macOS / Linux:

    curl -fsSL https://raw.githubusercontent.com/alexanderleitch/claude-cost-audit/main/claude_cost_audit.py | python3 -

Windows (PowerShell):

    irm https://raw.githubusercontent.com/alexanderleitch/claude-cost-audit/main/claude_cost_audit.py | python -

(Use `py -` instead of `python -` if that is how Python is installed.)

Or download `claude_cost_audit.py` and run `python3 claude_cost_audit.py`.
If you use `CLAUDE_CONFIG_DIR`, the script honours it.

## What it reports

- Enabled plugins ranked by estimated tokens of their skill/command/agent listings, with the MCP
  servers they bring `[...]` and any `{SessionStart, UserPromptSubmit}` hooks that inject text.
- User-scope MCP servers from `~/.claude.json`.
- Instruction files: `CLAUDE.md`, `rules/*.md`, and each project's `MEMORY.md`.

Token figures are rough (chars / 4) and exclude MCP tool schemas and hook output. Confirm real
numbers with `/context` inside Claude Code.

## Then cut

Let the script do it:

    python3 claude_cost_audit.py --pick                  # asks y/N/q per plugin, biggest first
    python3 claude_cost_audit.py --disable a@mkt b@mkt   # disable named plugins
    python3 claude_cost_audit.py --pick --dry-run        # print the commands, change nothing

Piped runs take the same flags, e.g. `irm <url> | python - --pick`.
It calls `claude plugin disable <plugin>`; undo any time with `claude plugin enable <plugin>`.
Restart Claude Code afterwards.

Other levers: `/clear` between unrelated tasks, `/compact` in long sessions, `/model sonnet` for
routine work, fewer subagents, and shorter CLAUDE.md / memory files.

## Morning briefing (shift your 5-hour window)

Usage limits run in 5-hour windows that start at your first message. A scheduled run at, say,
05:00 opens a window that resets at 10:00, so you get a fresh window mid-morning instead of one
from 09:00 to 14:00. It does not add usage, and it counts toward your weekly cap.

`morning/` makes that run useful: a **read-only** briefing of overnight commits, PRs awaiting your
review, failing CI, assigned issues and (if connected) today's meetings and email, saved to
`~/claude-briefings/YYYY-MM-DD.md`. Edit `morning/briefing-prompt.md` to change what it covers.

Pick the time as: when you start work + an hour or two - 5 hours.

Windows (wakes the PC from sleep, not from shutdown):

    powershell -ExecutionPolicy Bypass -File morning\install-morning-briefing.ps1 -RepoPath C:\code\myrepo -At 5am
    Start-ScheduledTask ClaudeMorningBriefing      # test it now

macOS / Linux (cron does not wake a sleeping machine):

    crontab -e
    0 5 * * * /path/to/claude-cost-audit/morning/morning-briefing.sh /path/to/myrepo

Settings, as environment variables:

- `BRIEFING_MODEL` (default `sonnet`; `haiku` is cheaper)
- `BRIEFING_DIR` (default `~/claude-briefings`)
- `BRIEFING_EXTRA_TOOLS`: comma-separated extra tools to allow, such as calendar and mail read
  tools. Find their names with `/mcp`. Allowing a whole server (`mcp__<server>`) also allows its
  write tools, so name individual read tools when the connector can send email or edit files.

Only the tools listed in the runner are allowed (read files, `git fetch/log/branch`,
`gh pr/run/issue list`); everything else is denied, so the run cannot change anything.

## Test

    python3 test_claude_cost_audit.py
    morning/test_morning_briefing.sh

## License

MIT
