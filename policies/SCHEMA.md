# Policy Bundle Schema (v0)

Policy bundles are JSON-formatted files stored under `policies/bundles/*`.

## Required keys
- `id` (string)
- `version` (string)
- `description` (string)
- `gates` (non-empty list)

## Optional global scope
- `include_paths: list[str]` glob patterns to include
- `exclude_paths: list[str]` glob patterns to exclude

## Gate entry schema
Each gate entry supports:
- `id` (string)
- `enabled` (bool, default `true`)
- `config` (object)
- `include_paths: list[str]` (optional, overrides global for this gate)
- `exclude_paths: list[str]` (optional, overrides global for this gate)

See: `policies/bundles/baseline/policy.yaml`.

## Baseline gate config keys (v0.1)
- `VG001`: no gate-specific config keys.
- `VG002`:
  - `forbidden: list[str]`
  - `allow: list[str]`
- `VG003`:
  - `allow_paths: list[str]`
  - `allow_patterns: list[str]`
- `VG004`:
  - `require_license: bool` (default `true`)
  - `require_third_party_notices: bool` (default `false`)
  - `license_paths: list[str]` (default `['LICENSE', 'LICENSE.md', 'LICENSE.txt']`)
  - `notices_paths: list[str]` (default `['THIRD_PARTY_NOTICES.md', 'THIRD_PARTY_NOTICES.txt']`)
- `VG005`:
  - `required_workflows: list[str]` (default `['.github/workflows/verify.yml']`)
- `VG006`:
  - `threat_model_path: str` (default `'THREAT_MODEL.md'`)
  - `required_sections: list[str]` (default `['Assets', 'Actors', 'Trust boundaries', 'Key threats and mitigations']`)
