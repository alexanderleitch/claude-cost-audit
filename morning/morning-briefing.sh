#!/usr/bin/env bash
# Run the read-only morning briefing in a repo and save it to $BRIEFING_DIR/YYYY-MM-DD.md.
# Usage: morning-briefing.sh [repo-path]   Env: BRIEFING_DIR, BRIEFING_MODEL, BRIEFING_EXTRA_TOOLS, CLAUDE_BIN
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
out_dir=${BRIEFING_DIR:-$HOME/claude-briefings}
tools="Read,Grep,Glob,Bash(git fetch:*),Bash(git log:*),Bash(git branch:*),Bash(gh pr list:*),Bash(gh run list:*),Bash(gh issue list:*)"
[ -n "${BRIEFING_EXTRA_TOOLS:-}" ] && tools="$tools,$BRIEFING_EXTRA_TOOLS"
mkdir -p "$out_dir"
cd "${1:-$PWD}"
"${CLAUDE_BIN:-claude}" -p --model "${BRIEFING_MODEL:-sonnet}" --allowedTools "$tools" \
  < "$here/briefing-prompt.md" > "$out_dir/$(date +%F).md"
