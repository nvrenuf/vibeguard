# AI Coding Rules (Codex / Claude Code)

These rules exist to keep AI-assisted output production-grade.

## Repository structure discipline
- Do not add new top-level directories without approval.
- Keep changes within existing module boundaries described in `ARCHITECTURE.md`.
- Prefer small, reviewable PRs; one issue → one PR whenever possible.

## Secure-by-default requirements
- Validate all external inputs (HTTP, CLI, message queues, webhooks).
- Use allowlists where possible; sanitize and normalize inputs.
- Use timeouts and retries for outbound calls; never infinite waits.
- Avoid logging secrets, tokens, credentials, or sensitive payloads.
- Use least privilege for any credentials or permissions.

## Dependencies
- Prefer standard library over new packages.
- New dependencies must be:
  - pinned (exact or narrow range)
  - justified in the PR and referenced in the spec
  - vetted for maintenance/security history
- Do not introduce “toolchain sprawl” (multiple linters/test frameworks without justification).

## Error handling
- Fail closed on security checks.
- Use typed/structured errors where appropriate.
- Do not swallow exceptions silently.
- Include actionable error messages (but never secret material).

## Testing
- Any behavior change requires tests.
- Bug fixes require regression tests.
- Security controls require tests where feasible (authz checks, input validation).

## Documentation
- If a change affects how to run, configure, deploy, or secure the system:
  - update `DEVELOPMENT.md`, `DEPLOYMENT.md`, `SECURITY.md`, and/or `OBSERVABILITY.md` accordingly.

## No slop rules (explicit)
- No commented-out code in final output.
- No placeholder implementations returning “mock” values.
- No “MVP shortcuts” in production paths.
- No unexplained magic numbers.
- Prefer clarity over cleverness.
