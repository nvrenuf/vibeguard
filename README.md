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

Flow contract for v0.1:
- Wizard definition constrains allowed repo/data change scope.
- Code Agent produces code/doc changes under that contract.
- Gates run deterministically and emit machine-readable findings.
- Approval is a human checkpoint for merge/deploy.
- Audit Pack captures evidence (findings + manifest + policy snapshot).

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

Run the CLI:
```bash
PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main --help
```

## CLI commands (v0.1)

Version information:
- `vibeguard --version` is not currently implemented as a CLI flag in v0.1.
- Source-of-truth version is in `apps/cli/pyproject.toml` (`version = "0.1.0"`).

```bash
rg '^version\\s*=\\s*\"' apps/cli/pyproject.toml
```

`check` command:

```bash
PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main check . \
  --policy policies/bundles/baseline/policy.yaml \
  --fail-on high
```

Supported flags:
- `--policy <path>` policy bundle path (default baseline policy)
- `--out <path>` write output to file (default stdout)
- `--fail-on low|medium|high|critical` severity threshold for non-zero exit
- `--format json|sarif` output format

SARIF example:

```bash
PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main check . \
  --policy policies/bundles/baseline/policy.yaml \
  --format sarif \
  --out out/findings.sarif
```

`audit-pack` command:

```bash
PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main audit-pack . \
  --policy policies/bundles/baseline/policy.yaml \
  --out-dir out/audit-pack
```

Supported flags:
- `--policy <path>`
- `--out-dir <path>`
- `--force-pack` always exit 0 after writing pack, even when findings fail

`init` command:

```bash
PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main init .
```

Supported flags:
- scaffolds baseline policy and recommended output folders
- `--force` overwrites generated policy file when present

`wizard compile` command:

```bash
PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main wizard compile \
  --in wizard/template.yaml \
  --out policies/bundles/generated/policy.yaml
```

## Baseline gates (v0.1)

Current baseline bundle (`policies/bundles/baseline/policy.yaml`) includes:
- `VG001`: required files at repo root
- `VG002`: forbidden root paths (for example build artifacts/secrets dirs)
- `VG003`: high-confidence secret pattern scan
- `VG004`: license / notices requirements
- `VG005`: required CI workflow presence

Scope and allowlist notes:
- Global `include_paths` / `exclude_paths` are supported by policy.
- Per-gate `include_paths` / `exclude_paths` overrides are supported.
- `VG003` supports:
  - `allow_paths` glob exclusions
  - `allow_patterns` regex suppressions for matched token text classes

## Audit pack output

`audit-pack` writes a run directory under `out/audit-pack/<run-id>/` with:
- `manifest.json`
- `reports/findings.json`
- `reports/summary.md`
- `policy_bundle/policy.yaml`
- `evidence/` directory

Manifest/hashing overview:
- Each file (except `manifest.json`) is hashed with SHA-256.
- Manifest includes run metadata (`run_id`, `created_at_utc`, `git_commit`, `policy_path`).
- Manifest records file `path`, `sha256`, and `size_bytes`.

## CI behavior

PR CI is defined in `.github/workflows/verify.yml` and currently runs:
- Python 3.11 setup
- dependency install (`requirements-dev.txt` + editable CLI install)
- `make verify` (pre-commit + tests)

## Gate extension guide

To add a new gate:
1. Implement gate class in `packages/gates/registry.py` (subclass `Gate`, define `id`, implement `run`).
2. Register the gate in `GATE_REGISTRY`.
3. Add baseline policy entry in `policies/bundles/baseline/policy.yaml` if it should run by default.
4. Document config keys in:
   - `policies/SCHEMA.md`
   - `spec/GATES.md`
5. Add tests under `apps/cli/tests/` for pass/fail/determinism and regression expectations.

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
