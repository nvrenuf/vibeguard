# Specs

Specs are the source-of-truth for shipped changes.

## Workflow (low friction)
1) Create an Issue using the Feature/Bug template.
2) Apply label `needs-spec`.
3) The GitHub Action generates a spec PR into this folder:
   - `SPECS/ISSUE-###-<slug>.md`

Implementation PRs must reference the spec file.

## Templates
- `SPECS/TEMPLATE.md` — used for issue templates and spec generation
