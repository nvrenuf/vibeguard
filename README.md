# Production Repository Template — AI-Assisted Development (Codex / Claude Code)

This repository is a **production-grade scaffold** designed to eliminate “slop” when using AI coding tools.
It enforces: **persistent requirements**, **repeatable verification**, **security defaults**, and **CI gates**.

## How to use

### 1) Create a new repo from this template
- Click **Use this template** in GitHub (or create via your internal repo provisioning).
- Immediately set branch protection (see `docs/BOOTSTRAP_CHECKLIST.md`).

### 2) Create work using Issues (source of truth)
- Use the **Feature** or **Bug** issue templates.
- Add label `needs-spec` (or your workflow can auto-add it).

### 3) Spec is generated automatically
- A GitHub Action converts the issue into `SPECS/ISSUE-###-<slug>.md` via a PR.

### 4) Implement via AI with low friction
- Run `tools/ai/ai-brief.sh 123` to generate the standard “context bundle” prompt to feed Codex/Claude.
- Or implement manually, but you must follow `REPO_CONTRACT.md`.

## Standard verification
- `make verify` runs repo-wide quality checks (pre-commit hooks).
- Language-specific tests should be added as the project grows (document in `DEVELOPMENT.md`).

## Key files
- `REPO_CONTRACT.md` — rules for AI-assisted development
- `AI_CODING_RULES.md` — coding + security standards
- `ACCEPTANCE_CRITERIA.md` — definition of done
- `SPECS/` — generated specs per issue (source of truth for features)
- `.github/workflows/` — CI, spec generation, and policy checks
