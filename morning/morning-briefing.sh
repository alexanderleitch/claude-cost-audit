#!/usr/bin/env bash
# Run the read-only morning briefing in a repo and save it to $BRIEFING_DIR/YYYY-MM-DD.md.
# Usage: morning-briefing.sh [repo-path]   Env: BRIEFING_DIR, BRIEFING_MODEL, BRIEFING_EXTRA_TOOLS, CLAUDE_BIN
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
out_dir=${BRIEFING_DIR:-$HOME/claude-briefings}
# Exact commands only: a `:*` wildcard would let text planted in a commit or PR add flags such as
# `git log --output=<file>` or `git fetch --upload-pack=<cmd>`. Keep in sync with briefing-prompt.md.
tools='Bash(git log --remotes --since=24.hours --oneline),Bash(gh pr list --search review-requested:@me),Bash(gh pr list --author @me),Bash(gh run list --limit 5),Bash(gh issue list --assignee @me)'
[ -n "${BRIEFING_EXTRA_TOOLS:-}" ] && tools="$tools,$BRIEFING_EXTRA_TOOLS"
mkdir -p "$out_dir"
cd "${1:-$PWD}"
git fetch --quiet 2>/dev/null || true
"${CLAUDE_BIN:-claude}" -p --model "${BRIEFING_MODEL:-sonnet}" --allowedTools "$tools" \
  < "$here/briefing-prompt.md" > "$out_dir/$(date +%F).md"
