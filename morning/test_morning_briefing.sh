#!/usr/bin/env bash
# Runs morning-briefing.sh against a fake `claude` and checks prompt, flags and output file.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/claude" <<'FAKE'
#!/usr/bin/env bash
echo "ARGS: $*"
echo "PWD: $PWD"
echo "STDIN: $(head -1)"
FAKE
chmod +x "$tmp/claude"
mkdir "$tmp/repo"
CLAUDE_BIN="$tmp/claude" BRIEFING_DIR="$tmp/out" BRIEFING_EXTRA_TOOLS="mcp__x" "$here/morning-briefing.sh" "$tmp/repo"
out="$tmp/out/$(date +%F).md"
grep -q -- "-p --model sonnet --allowedTools Bash(git log --remotes" "$out"
# wildcard rules (`:*`) would let injected text add flags like --output or --upload-pack
! grep -q -- ":\*" "$out"
# every command the prompt tells Claude to run must be allowed verbatim
grep -o '`[^`]*`' "$here/briefing-prompt.md" | tr -d '`' | grep -E '^(git|gh) ' | while read -r cmd; do
  grep -qF "Bash($cmd)" "$out" || { echo "not allowed: $cmd"; exit 1; }
done
grep -q -- ",mcp__x" "$out"
grep -q "PWD: $tmp/repo" "$out" || grep -q "PWD: $(cd "$tmp/repo" && pwd -P)" "$out"
grep -q "STDIN: # Morning briefing" "$out"
echo ok
