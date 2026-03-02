# Bootstrap Checklist (Do this immediately after creating a repo from the template)

## Repository settings (GitHub)
1) Enable Actions (if your org requires manual enablement).
2) Protect `main` branch:
   - Require PRs
   - Require approvals
   - Require status checks:
     - `verify (pre-commit)`
     - `secret scan (gitleaks)`
     - `actionlint`
3) Configure CODEOWNERS enforcement (if available).
4) Add required labels (at minimum):
   - `needs-spec`
   - `ai:ok-to-implement`
   - `security-review`
   - `breaking-change`
   - `schema-change`

## Secrets (only if needed)
If you use advanced automations that require elevated permissions, configure:
- Org/repo secrets for GitHub App tokens (optional)

This template’s spec-generation workflow uses `GITHUB_TOKEN` and should work in most orgs.

## Local dev
- `pip install -r requirements-dev.txt`
- `pre-commit install`
- `make verify`
