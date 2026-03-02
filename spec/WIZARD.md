# VibeGuard Wizard (Spec + Policy Compile)

The wizard defines structured constraints **before** an agent writes code, and can compile
those constraints into a policy bundle.

## Inputs
- Problem statement / desired outcome
- Repo paths/modules allowed to change
- Data/system access boundaries (if any)
- Risk level (low/med/high)
- Required approvers
- Additional acceptance criteria
- Gate selection (`gate_ids`) for compiled policy output

## Outputs
- Issue-level spec file in `SPECS/ISSUE-###-*.md` (or standalone spec)
- Wizard YAML input (`wizard/template.yaml`)
- Compiled policy YAML/JSON at a chosen path (for gate runner use)

## CLI compile flow (v0.1)
Compile wizard template to a policy bundle:

```bash
vibeguard wizard compile --in wizard/template.yaml --out policies/bundles/generated/policy.yaml
```

Compile behavior:
- fail closed on invalid wizard schema
- emit deterministic policy output ordering
- validate generated policy with the existing policy loader/schema

Required wizard fields:
- `policy_id` (string)
- `policy_version` (string)
- `description` (string)
- `gate_ids` (non-empty list of strings)
- optional: `include_paths`, `exclude_paths` (list of strings)
