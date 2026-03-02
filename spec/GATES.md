# Gates (v0)

## Gate categories
- Repo hygiene (required files present)
- Forbidden root paths (build artifacts, generated folders, secrets files)
- Basic secret scan (high-confidence token/pem patterns)

## Implemented baseline gates

### VG001 — Required Files
Ensures required files exist at repository root (`README.md`, `SECURITY.md`, `ARCHITECTURE.md`, `AGENTS.md`, `ISSUE_ORDER.md`).

### VG002 — Forbidden Directories / Files
Checks for forbidden paths at repository root.

Default forbidden paths:
- `node_modules/`
- `dist/`
- `build/`
- `.next/`
- `.venv/`
- `__pycache__/`
- `.env`
- `secrets/`

Config:
- `forbidden: list[str]` paths relative to repo root
- `allow: list[str]` explicit exceptions

### VG003 — Basic Secret Scan
Scans scoped text files using high-confidence patterns:
- AWS access key IDs (`AKIA[0-9A-Z]{16}`)
- GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`, `github_pat_`)
- Slack tokens (`xoxb-`, `xoxp-`, `xoxa-`)
- `BEGIN PRIVATE KEY` blocks

Config:
- `allow_paths: list[str]` glob paths skipped during scan
- `allow_patterns: list[str]` regex patterns to suppress matched token text

Findings are `high` severity and include path + pattern name, never the secret value.

## Scope filters
Policy supports global scope filters and per-gate overrides:
- `include_paths: list[str]` optional glob allowlist
- `exclude_paths: list[str]` optional glob denylist

Per-gate `include_paths` / `exclude_paths` override global values for that gate.

## Fail-closed rules
- Policy cannot be loaded → error → overall fail
- Unknown gate id in policy → finding → overall fail
