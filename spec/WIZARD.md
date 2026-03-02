# VibeGuard Wizard (Spec Generator)

The wizard creates structured constraints **before** an agent writes code.

## Inputs
- Problem statement / desired outcome
- Repo paths/modules allowed to change
- Data/system access boundaries (if any)
- Risk level (low/med/high)
- Required approvers
- Additional acceptance criteria

## Outputs
- Issue-level spec file in `SPECS/ISSUE-###-*.md` (or a standalone spec when not tied to GitHub issues)
- A machine-readable constraints file (future): `spec/instances/<id>.json`

## v0 approach
- Use GitHub issue template + spec file as the wizard output.
- Add a structured “Scope + Data + Risk” block to the spec template.
