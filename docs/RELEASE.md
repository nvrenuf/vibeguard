# Release Checklist

Use this checklist for every production release.

## 1) Preconditions

- Confirm clean working tree:
  - `git status --short` should be empty.
- Confirm you are up to date on main:
  - `git checkout main`
  - `git pull --ff-only origin main`
- Confirm no open release-blocker PRs:
  - `gh pr list --repo nvrenuf/vibeguard --state open --limit 50`
- Confirm CI is green on main (latest verify workflow run):
  - `gh run list --repo nvrenuf/vibeguard --branch main --workflow verify --limit 5`

## 2) Version Bump (Single Source of Truth)

Canonical release version file:
- `apps/cli/pyproject.toml` (`project.version`)

Procedure:
- Update `version = "X.Y.Z"` in `apps/cli/pyproject.toml`.
- If policy contract changes in the same release, also update policy bundle version in:
  - `policies/bundles/baseline/policy.yaml` (`version`)
- Commit with message like:
  - `chore(release): bump version to vX.Y.Z`

## 3) Run Gates Before Tagging

- `pre-commit run --all-files`
- `make verify`
- Baseline gate check:
  - `PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main check . --policy policies/bundles/baseline/policy.yaml`

If local cache folders (for example `.venv`, `.pc-home`) cause local-only failures, run baseline check in a clean worktree:
- `tmpdir=$(mktemp -d /tmp/vgcheck-release-XXXXXX)`
- `git worktree add --detach "$tmpdir" HEAD`
- `(cd "$tmpdir" && PYTHONPATH=apps/cli:$PYTHONPATH /Users/leecuevas/Projects/vibeguard/.venv/bin/python -m vibeguard_cli.main check . --policy policies/bundles/baseline/policy.yaml)`
- `git worktree remove "$tmpdir" --force`

## 4) Changelog and Release Notes

Use GitHub auto-generated release notes:
- Docs: <https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes>
- CLI path:
  - `gh release create vX.Y.Z --generate-notes --title "vX.Y.Z"`

Before publishing, review generated notes and add:
- migration/breaking-change notes (if any)
- security-impact notes (if any)
- operator actions required after upgrade

## 5) Tag and Publish

- Create annotated tag:
  - `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- Push tag:
  - `git push origin vX.Y.Z`
- Create GitHub release (if not already created from CLI):
  - `gh release create vX.Y.Z --generate-notes --title "vX.Y.Z"`

## 6) Post-Release Verification

- Confirm release page exists and notes render correctly:
  - `gh release view vX.Y.Z --repo nvrenuf/vibeguard`
- Smoke test CLI from current repo checkout:
  - `PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main --help`
  - `PYTHONPATH=apps/cli:$PYTHONPATH .venv/bin/python -m vibeguard_cli.main check . --policy policies/bundles/baseline/policy.yaml`

## 7) Rollback Guidance

If a release must be rolled back:
- Document reason in a follow-up issue.
- Revert offending commit(s) on a hotfix branch and merge via PR.
- Publish a follow-up patch release (`vX.Y.Z+1`) rather than deleting release history.
- If a tag was pushed in error and absolutely must be removed:
  - `git push --delete origin vX.Y.Z`
  - recreate corrected tag and release with explicit notes.

## 8) Security Notes

- Never include secrets in logs, release notes, or audit-pack artifacts.
- Confirm redaction expectations in `docs/LOGGING_REDACTION.md`.
- Review workflow actions for supply-chain hygiene (prefer pinned versions/SHAs where practical).
- Do not attach raw sensitive evidence files to public release artifacts.
