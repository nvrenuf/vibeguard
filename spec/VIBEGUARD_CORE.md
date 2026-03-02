# VibeGuard Core (Product Spec)

## Objective
Create a repeatable, team-friendly flow that turns “vibe-coded output” into **reviewable, auditable, policy-compliant** changes.

## In scope (v0)
- A local-first **CLI** that runs policy gates on a repo checkout.
- Versioned policy bundles (YAML) and a schema.
- Audit pack exporter that writes an evidence folder.
- Minimal integration hooks for CI (GitHub Actions).

## Out of scope (v0)
- IDE plugins / UI (tracked for v1+)
- Running untrusted code in sandboxes
- Complex approvals workflow integrated with GitHub (start with files/artifacts)

## Core user stories
1) As a team lead, I can define guardrails (policy bundle) and enforce them in CI.
2) As an engineer using Codex, I can run `vibeguard check` before opening a PR.
3) As a security/compliance reviewer, I can download an audit pack to verify what was checked and what passed/failed.

## Definitions
- **Gate:** a deterministic check that produces findings.
- **Policy bundle:** configuration that enables/disables gates and sets thresholds.
- **Audit pack:** the exported evidence bundle for a run.

## Primary flow (v0)
1) select policy bundle
2) run gates
3) review findings
4) generate audit pack
