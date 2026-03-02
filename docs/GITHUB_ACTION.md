# Reusable GitHub Action

VibeGuard ships an in-repo reusable composite action at:

- `.github/actions/vibeguard/action.yml`

Use it from another repository with:

```yaml
name: vibeguard

on:
  pull_request:
  push:
    branches: [main]

jobs:
  vibeguard-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run VibeGuard
        uses: nvrenuf/vibeguard/.github/actions/vibeguard@<tag-or-sha>
        with:
          policy_path: policies/bundles/baseline/policy.yaml
          fail_on: high
          format: json
```

## Inputs

- `policy_path` (default: `policies/bundles/baseline/policy.yaml`)
- `fail_on` (default: `high`)
- `format` (default: `json`)
