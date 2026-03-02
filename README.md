# VibeGuard

VibeGuard is a **guardrailed vibe-coding** control plane for teams.

It sits between “AI wrote some code” and “we shipped it” and enforces:
- **Scope + data boundaries** (what the agent is allowed to touch)
- **Policy gates** (security / compliance / quality checks)
- **Approval workflow** (human sign-off for risky changes)
- **Audit pack export** (evidence bundle for SOC 2 / internal audit / customers)

## End-to-end flow

1) **Idea**
2) **VibeGuard Wizard** (define scope, data, criteria)
3) **Code Agent** (Codex / Claude / Cursor writes code)
4) **VibeGuard Gates** run (policy checks + proofs)
5) **Approval**
6) **Deploy**
7) **Export Audit Pack**

This repo is the **single source of truth** for the VibeGuard product: specs, policies, gates engine, and audit pack format.

---

## Repository map

- `spec/` — product-level specs (stable, curated)
- `SPECS/` — issue-level specs (generated / per-change)
- `policies/` — policy bundles (YAML) that gates evaluate
- `audit-pack/` — audit pack schema + templates
- `apps/cli/` — `vibeguard` CLI (v0 interface)
- `packages/` — core library modules (gates, reporting, connectors)
- `docs/` — repo/bootstrap docs

## Quickstart (local)

Prereqs: Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e apps/cli
pre-commit install
make verify
```

Run the CLI (skeleton):
```bash
vibeguard --help
```

---

## How work gets done here (Codex-friendly)

Mandatory reading for any AI coding run:
- `REPO_CONTRACT.md`
- `AI_CODING_RULES.md`
- `ARCHITECTURE.md`
- `ACCEPTANCE_CRITERIA.md`
- `spec/VIBEGUARD_CORE.md`
- the relevant spec in `SPECS/`

Use `tools/ai/ai-brief.sh <issue_number>` to print a standardized prompt bundle for Codex/Claude Code.

---

## Roadmap (v0 → v1)

See `spec/ROADMAP.md`.
