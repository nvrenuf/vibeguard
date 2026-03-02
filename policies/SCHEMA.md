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
