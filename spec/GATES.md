# Gates (v0)

## Gate categories
- Repo hygiene (required files present, formatting)
- Secrets scan (baseline)
- Dependency policy (licenses, ecosystem, allow/deny)
- Scope enforcement (changed files are within allowed paths)
- CI configuration (required workflows present)

## Output contract
Every gate returns:
- `id`, `name`, `status` (pass/fail/warn/error)
- `findings[]` with `severity`, `message`, `evidence` (paths/lines when applicable)

## Fail-closed rules
- Policy cannot be loaded → error → overall fail
- Gate errors executing → error → overall fail
