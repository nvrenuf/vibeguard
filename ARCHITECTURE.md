# Architecture (Living Document)

This document describes the architecture of **VibeGuard** and must remain accurate.

## What VibeGuard is

VibeGuard is a **policy gate and audit layer** for AI-assisted development.
It does **not** replace Codex/Claude/Cursor. It wraps them with:
- a structured “wizard” spec,
- deterministic checks (“gates”),
- an approval boundary,
- and an exportable audit pack.

## Core components

### 1) Wizard (spec + constraints)
Artifacts produced by the wizard are the **contract** for implementation:
- scope: what paths / modules / services may be modified
- data: what datasets/systems may be accessed (if any)
- criteria: acceptance criteria beyond repo defaults
- risk classification: low/med/high
- required approvers

Stored as:
- product-level spec: `spec/WIZARD.md`
- issue-level instances: `SPECS/ISSUE-###-*.md`

### 2) Gate runner
A deterministic engine that:
- loads a policy bundle (`policies/bundles/...`)
- evaluates the target workspace (repo checkout)
- produces a machine-readable findings report
- can enforce **fail-closed** behavior on disallowed actions

Runtime surfaces (v0):
- `vibeguard` CLI: `apps/cli/`

Core flow wiring in v0.1:
1) Wizard constraints are defined in spec artifacts.
2) Code Agent changes are produced in-repo.
3) Gate runner executes policy bundle checks (`vibeguard check`).
4) Human approval happens at PR review/merge boundary.
5) Audit evidence is exported (`vibeguard audit-pack`).

### 3) Policy bundles
Versioned policy definitions (YAML) for:
- dependency allow/deny (licenses, ecosystems)
- secrets scanning requirements
- repo hygiene (required files, required CI)
- change scope enforcement (paths touched)
- optional framework mappings (SOC 2, PCI, etc.)

Location: `policies/`

### 4) Audit pack exporter
Produces an evidence bundle containing:
- policy bundle version + hashes
- findings report
- PR/commit metadata (when integrated)
- verification outputs
- attestation / approvals

Schema + templates: `audit-pack/`

## Trust boundaries

- **Untrusted input:** repository contents being checked; PR diffs; user-supplied policy bundles.
- **Trusted computing base:** VibeGuard gate runner + policies shipped in this repo.
- **Principle:** *Fail closed* when policy cannot be loaded or a gate cannot execute reliably.

## Security invariants (non-negotiable)

- Gates must be deterministic and reproducible.
- No gate may exfiltrate repo contents. Default: **no network**.
- No secrets are logged. Logs are structured and redact sensitive content.
- Policies are versioned and cryptographically hashed into the audit pack.
- Approvals are required for high-risk changes (as defined by wizard output).

## Observability

- Gate runs emit a structured JSON report (and optional human summary).
- Every gate run has a run ID, timestamp, policy bundle identifier, and git revision.
- SARIF output is available from CLI for ecosystem tooling.
- Report metadata includes policy versioning fields to support v0.1 traceability.

## Change control

Architectural changes require:
1) updating this file
2) updating `spec/ROADMAP.md` if scope changes
3) a spec in `SPECS/` for the change
