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

    claude plugin disable <plugin>     # re-enable any time with: claude plugin enable <plugin>

Other levers: `/clear` between unrelated tasks, `/compact` in long sessions, `/model sonnet` for
routine work, fewer subagents, and shorter CLAUDE.md / memory files.

## Test

    python3 test_claude_cost_audit.py

## License

MIT
