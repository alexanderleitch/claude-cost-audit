import json
import tempfile
from pathlib import Path

from claude_cost_audit import claude_dir, disable_plugins, frontmatter_desc, pick, plugin_cost


def test_frontmatter_desc_handles_multiline_and_missing():
    assert frontmatter_desc("---\nname: x\ndescription: one\n  two\n---\nbody") == "one\n  two"
    assert frontmatter_desc("no frontmatter") == ""


def test_plugin_cost_counts_skills_servers_and_hooks():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "skills" / "a").mkdir(parents=True)
        (root / "skills" / "a" / "SKILL.md").write_text("---\ndescription: abcd\n---\n")
        (root / ".mcp.json").write_text(json.dumps({"mcpServers": {"srv": {}}}))
        (root / "hooks").mkdir()
        (root / "hooks" / "hooks.json").write_text(json.dumps({"hooks": {"SessionStart": [], "Stop": []}}))
        assert plugin_cost(root) == (44, 1, ["srv"], ["SessionStart"])


def test_claude_dir_honours_env():
    import os
    os.environ["CLAUDE_CONFIG_DIR"] = "/tmp/x"
    try:
        assert claude_dir() == Path("/tmp/x")
    finally:
        del os.environ["CLAUDE_CONFIG_DIR"]
    assert claude_dir() == Path.home() / ".claude"


def test_disable_plugins_runs_cli_and_skips_unknown():
    calls = []

    def runner(cmd):
        calls.append(cmd)
        return 0

    failed = disable_plugins(["a@m", "nope@m"], enabled=["a@m", "b@m"], claude_bin="claude", run=runner)
    assert calls == [["claude", "plugin", "disable", "a@m"]]
    assert failed == ["nope@m"]


def test_pick_stops_on_quit():
    rows = [(900, "a@m", 3, [], []), (500, "b@m", 1, [], []), (100, "c@m", 1, [], [])]
    answers = iter(["y", "n", "q"])
    assert pick(rows, ask=lambda _prompt: next(answers)) == ["a@m"]


if __name__ == "__main__":
    test_frontmatter_desc_handles_multiline_and_missing()
    test_plugin_cost_counts_skills_servers_and_hooks()
    test_claude_dir_honours_env()
    test_disable_plugins_runs_cli_and_skips_unknown()
    test_pick_stops_on_quit()
    print("ok")
