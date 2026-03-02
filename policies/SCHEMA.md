# Policy Bundle Schema (v0)

This repo uses simple YAML policy bundles in `policies/bundles/*`.

## Required keys
- `bundle_id` (string)
- `version` (string)
- `gates` (map of gate_id -> config)
- `thresholds` (optional)

## Gate config (common)
- `enabled` (bool)
- `severity_fail` (list of severities that fail the run: [high, critical] etc)

See: `policies/bundles/baseline/policy.yaml`.
