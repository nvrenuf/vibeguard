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

### VG004 — License / Third-Party Notices
Checks for repository licensing and optional third-party notices files.

Defaults:
- License required
- Third-party notices optional

Config:
- `require_license: bool` (default `true`)
- `require_third_party_notices: bool` (default `false`)
- `license_paths: list[str]` (default `['LICENSE', 'LICENSE.md', 'LICENSE.txt']`)
- `notices_paths: list[str]` (default `['THIRD_PARTY_NOTICES.md', 'THIRD_PARTY_NOTICES.txt']`)

Example:
```json
{
  "id": "VG004",
  "enabled": true,
  "config": {
    "require_license": true,
    "require_third_party_notices": false,
    "license_paths": ["LICENSE", "LICENSE.md", "LICENSE.txt"],
    "notices_paths": ["THIRD_PARTY_NOTICES.md", "THIRD_PARTY_NOTICES.txt"]
  }
}
```

### VG005 — CI Workflow Presence
Checks that required CI workflow files are present.

Config:
- `required_workflows: list[str]` (default `['.github/workflows/verify.yml']`)

Example:
```json
{
  "id": "VG005",
  "enabled": true,
  "config": {
    "required_workflows": [".github/workflows/verify.yml"]
  }
}
```

### VG006 — Threat Model Structure
Checks that the threat model document exists and includes required section headings.

Config:
- `threat_model_path: str` (default `'THREAT_MODEL.md'`)
- `required_sections: list[str]`
  default: `['Assets', 'Actors', 'Trust boundaries', 'Key threats and mitigations']`

Example:
```json
{
  "id": "VG006",
  "enabled": true,
  "config": {
    "threat_model_path": "THREAT_MODEL.md",
    "required_sections": [
      "Assets",
      "Actors",
      "Trust boundaries",
      "Key threats and mitigations"
    ]
  }
}
```

## Scope filters
Policy supports global scope filters and per-gate overrides:
- `include_paths: list[str]` optional glob allowlist
- `exclude_paths: list[str]` optional glob denylist

Per-gate `include_paths` / `exclude_paths` override global values for that gate.

## Fail-closed rules
- Policy cannot be loaded → error → overall fail
- Unknown gate id in policy → finding → overall fail
