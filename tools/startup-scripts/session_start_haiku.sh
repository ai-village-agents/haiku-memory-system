#!/bin/bash
# Claude Haiku 4.5 session start guardrail: quick verification before editing.
set -euo pipefail
# 1) Verify local clock to avoid date confusion.
echo "=== Claude Haiku 4.5 | Session Start ==="
date +"Local time: %A, %Y-%m-%d %H:%M:%S %Z"
# 2) Navigate to repo root and pull latest.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"
echo "[pull] Refreshing repo at $REPO_ROOT"
git pull --quiet origin main
# 3) Read the current goal from consolidated memory.
GOAL_FILE="$REPO_ROOT/README_COMPREHENSIVE.md"
GOAL_LINE="$(rg --no-heading --max-count 1 '\*\*Goal\*\*: *.*' "$GOAL_FILE" | sed 's/.*Goal\*\*: *//')"
[[ -z "$GOAL_LINE" ]] && GOAL_LINE="(goal not found; open README_COMPREHENSIVE.md)"
echo "[goal] $GOAL_LINE"
# 4) List 2-3 immediate next steps from Phase 3 roadmap.
echo "[next] Immediate next steps (Phase 3)"
NEXT_STEPS="$(rg '^\\- \\[.\\] ' "$REPO_ROOT/PHASE_3_ROADMAP.md" | head -n 3)"
if [[ -n "$NEXT_STEPS" ]]; then
  echo "$NEXT_STEPS"
else
  echo "No next steps found; check PHASE_3_ROADMAP.md"
fi
# 5) External memory pointers for quick navigation.
printf "%s\n" "[pointers]" "- Repo URL: https://github.com/ai-village-agents/haiku-memory-system" "- Tiered guide: README_COMPREHENSIVE.md" "- Access patterns: patterns/memory_access_guide.md" "- Phase plan: PHASE_3_ROADMAP.md"
# 6) Verify working tree cleanliness.
STATUS_OUTPUT="$(git status --short)"
if [[ -n "$STATUS_OUTPUT" ]]; then
  echo "[status] Uncommitted changes detected:"
  echo "$STATUS_OUTPUT"
else
  echo "[status] Working tree clean."
fi
# 7) Ready signal with timestamp for logs.
echo "READY: $(date +'[%Y-%m-%d %H:%M:%S %Z]')"
