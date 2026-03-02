# Audit Pack (v0)

An audit pack is an **exported evidence folder** intended for:
- internal review
- customer trust (security questionnaires)
- compliance programs (SOC 2 evidence)

## Required contents
- `manifest.json` (run metadata + hashes)
- `policy_bundle/` (copied policy YAML + computed hash)
- `reports/findings.json` (machine-readable output)
- `reports/summary.md` (human summary)
- `attestations/` (optional approvals / signoffs)
- `tooling/` (versions, environment, command line)

## Non-goals
- Storing secrets or raw sensitive data
- Uploading anywhere by default (local-first)
