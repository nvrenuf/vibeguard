# Roadmap

## v0.1 scope (current milestone)
- Canonical Core flow and terminology are documented and aligned across:
  - `README.md`
  - `ARCHITECTURE.md`
  - `spec/VIBEGUARD_CORE.md`
- CLI ships and is documented with these commands:
  - `vibeguard check` with `--policy`, `--out`, `--fail-on`, and `--format json|sarif`
  - `vibeguard audit-pack` with `--policy`, `--out-dir`, and `--force-pack`
  - `vibeguard init` with `--force`
- Baseline policy bundle and gate runner are active for repo hygiene, path controls, and secret detection.
- Audit-pack generation is deterministic and includes findings, summary, policy snapshot, and manifest with hashes.
- CI runs verification on PRs using `.github/workflows/verify.yml` and `make verify`.
- Versioning source-of-truth is policy/report metadata (`policy_version`) for v0.1 outputs.

## Not in v0.1
- Full Wizard interactive UX/application.
- Wizard spec-to-policy compiler.
- GitHub PR inline findings comments and review workflow automation.
- Policy signing/provenance attestation (SLSA-style).
- Multi-repo/org policy management and exception lifecycles.
- IDE integrations and agent-runner orchestration hooks.

## v1 candidates
- Wizard compile path (`wizard.yaml` -> policy bundle) with schema validation.
- PR-native findings publication and approval gates.
- Versioning model expansion beyond policy/report metadata (release/tag automation hardening).

## v2+ candidates
- Rich Wizard UI and templates.
- Multi-repo policy operations.
- Extended agent integrations.
