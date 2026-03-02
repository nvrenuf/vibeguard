# Repository Contract — AI-Assisted Development (Production)

This repository uses AI tools (Codex / Claude Code) to accelerate implementation.
**AI is not allowed to define requirements or architecture**. AI output is treated as untrusted until verified.

## Mandatory reading (always)
Before generating or modifying code, the AI tool MUST read (or be provided) the following files:

- `REPO_CONTRACT.md`
- `AI_CODING_RULES.md`
- `ARCHITECTURE.md`
- `ACCEPTANCE_CRITERIA.md`
- The relevant spec in `SPECS/` (e.g., `SPECS/ISSUE-123-*.md`)

If any of these are missing from context, the AI must stop and request them.

## Required output format: Plan → Patch → Verify
All AI-driven work must follow this structure.

### 1) PLAN
- Identify the spec and restate intended outcome.
- List files to be changed (and why).
- Explain approach (high-level).
- Identify risks (security, data handling, tenancy, backwards compatibility).
- Identify tests to add/update.
- Confirm dependency impact (none / list new + justification).

### 2) PATCH
- Implement code and tests.
- Keep changes scoped to the spec.
- Update docs when required by acceptance criteria.

### 3) VERIFY
- Run (or instruct to run) verification commands:
  - `make verify`
  - plus any project-specific test commands (document in `DEVELOPMENT.md`)
- Summarize results and fix failures.
- Confirm:
  - no secrets added
  - no insecure defaults introduced
  - logging is present where required
  - any new endpoints/actions have authz + audit

## Non-negotiable rules
- **No architectural changes** unless explicitly authorized in the spec and updated in `ARCHITECTURE.md`.
- **No copy/paste from external repositories** (patterns may be studied; code must be rewritten).
- **No hardcoded secrets**. Use env vars + secret management.
- **No disabling CI/lint/security checks**.
- **No “temporary” TODO placeholders** in production paths.
- **Least privilege** for permissions, tokens, APIs, and actions.
- **Fail closed**: defaults should deny rather than allow.

## Review and merge policy (minimum)
- No direct pushes to `main`.
- CI must pass.
- A reviewer must approve (use CODEOWNERS for sensitive paths).
- If the change touches security-critical areas, security review is required (see `SECURITY.md` and CODEOWNERS rules).
