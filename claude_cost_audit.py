#!/usr/bin/env python3
"""Rank what Claude Code loads into every turn, so unused plugins can be disabled.

Read-only. Token figures are estimates (chars / 4). Run: python3 claude_cost_audit.py
"""
import json
import re
from pathlib import Path

HOME = Path.home()
CLAUDE = HOME / ".claude"
EVERY_TURN_HOOKS = ("SessionStart", "UserPromptSubmit")


def tokens(chars):
    return chars // 4


def frontmatter_desc(text):
    """Return the `description:` value from a markdown file's YAML frontmatter."""
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    d = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", m.group(1), re.M)
    return d.group(1).strip() if d else ""


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def plugin_cost(root):
    """Listing chars for skills/commands/agents, MCP server names, every-turn hook events."""
    chars, skills = 0, 0
    for pattern in ("skills/*/SKILL.md", "commands/*.md", "agents/*.md"):
        for f in root.glob(pattern):
            chars += len(frontmatter_desc(f.read_text(encoding="utf-8", errors="ignore"))) + 40
            skills += 1
    mcp = load_json(root / ".mcp.json")
    servers = list(mcp.get("mcpServers", mcp).keys())
    hooks = load_json(root / "hooks" / "hooks.json").get("hooks", {})
    return chars, skills, servers, [h for h in EVERY_TURN_HOOKS if h in hooks]


def main():
    enabled = [k for k, v in load_json(CLAUDE / "settings.json").get("enabledPlugins", {}).items() if v]
    installed = load_json(CLAUDE / "plugins" / "installed_plugins.json").get("plugins", {})
    rows = []
    for name in enabled:
        paths = [Path(e["installPath"]) for e in installed.get(name, []) if e.get("scope") == "user"]
        if not paths or not paths[0].exists():
            continue
        chars, n, servers, hooks = plugin_cost(paths[0])
        rows.append((tokens(chars), name, n, servers, hooks))
    rows.sort(reverse=True)

    print(f"{'~tok':>6}  {'items':>5}  plugin  [MCP servers] {{every-turn hooks}}")
    for tok, name, n, servers, hooks in rows:
        extra = (f"  [{', '.join(servers)}]" if servers else "") + (f"  {{{', '.join(hooks)}}}" if hooks else "")
        print(f"{tok:>6}  {n:>5}  {name}{extra}")
    print(f"{sum(r[0] for r in rows):>6}  total skill/command/agent listing (+ MCP tool schemas, not counted)")

    user_mcp = list(load_json(HOME / ".claude.json").get("mcpServers", {}).keys())
    print(f"\nUser-scope MCP servers: {', '.join(user_mcp) or 'none'}")

    print("\nInstruction files loaded every session:")
    files = [CLAUDE / "CLAUDE.md", *sorted((CLAUDE / "rules").glob("*.md")),
             *sorted((CLAUDE / "projects").glob("*/memory/MEMORY.md"))]
    for f in files:
        if f.exists():
            print(f"{tokens(len(f.read_text(encoding='utf-8', errors='ignore'))):>6}  {f.relative_to(HOME)}")

    print("\nDisable with:  claude plugin disable <plugin>   (re-enable: claude plugin enable <plugin>)")
    print("Plugins with {hooks} inject text at start / on every prompt; check real size with /context.")


if __name__ == "__main__":
    main()
