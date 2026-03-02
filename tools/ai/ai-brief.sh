#!/usr/bin/env bash
set -euo pipefail

# ai-brief.sh <issue_number> [spec_path]
# Prints a standardized prompt bundle for Codex/Claude Code.

ISSUE="${1:-}"
SPEC_PATH="${2:-}"

if [[ -z "$ISSUE" ]]; then
  echo "Usage: tools/ai/ai-brief.sh <issue_number> [spec_path]" >&2
  exit 1
fi

if [[ -z "$SPEC_PATH" ]]; then
  # try to find a matching spec
  SPEC_PATH="$(ls -1 SPECS/ISSUE-${ISSUE}-*.md 2>/dev/null | head -n 1 || true)"
fi

if [[ -z "$SPEC_PATH" ]]; then
  echo "ERROR: Could not find spec for ISSUE-${ISSUE}. Create/merge the spec PR first." >&2
  exit 2
fi

echo "### AI IMPLEMENTATION BRIEF (Issue #${ISSUE})"
echo
echo "You are implementing Issue #${ISSUE} according to the repository contract."
echo
echo "MANDATORY: Read and follow these files:"
echo "- REPO_CONTRACT.md"
echo "- AI_CODING_RULES.md"
echo "- ARCHITECTURE.md"
echo "- ACCEPTANCE_CRITERIA.md"
echo "- spec/VIBEGUARD_CORE.md"
echo "- ${SPEC_PATH}"
echo
echo "Output format REQUIRED:"
echo "1) PLAN"
echo "2) PATCH"
echo "3) VERIFY"
echo
echo "Verification REQUIRED:"
echo "- Run: make verify"
echo "- Add/Run any project-specific tests documented in DEVELOPMENT.md"
echo
echo "Open a PR with a summary and include verification output in the PR template."
