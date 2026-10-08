import json
import tempfile
from pathlib import Path

from claude_cost_audit import claude_dir, frontmatter_desc, plugin_cost


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


if __name__ == "__main__":
    test_frontmatter_desc_handles_multiline_and_missing()
    test_plugin_cost_counts_skills_servers_and_hooks()
    test_claude_dir_honours_env()
    print("ok")
