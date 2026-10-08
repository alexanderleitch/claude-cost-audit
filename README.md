# claude-cost-audit

Read-only report of what Claude Code loads into every turn: enabled plugins ranked by estimated
skill/command/agent listing size, their MCP servers and every-turn hooks, user-scope MCP servers,
and the instruction files (CLAUDE.md, rules, MEMORY.md) loaded each session.

    python3 claude_cost_audit.py
    python3 test_claude_cost_audit.py   # self-check

Token figures are chars/4 estimates and exclude MCP tool schemas and hook output; confirm with
`/context` inside Claude Code. Disable unused plugins with `claude plugin disable <plugin>`.
