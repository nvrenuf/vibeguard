# AI Coding Rules (Codex / Claude Code)

These rules exist to keep AI-assisted output production-grade **and** aligned with VibeGuard’s guardrailing mission.

## Repository structure discipline
- Do not add new top-level directories without approval.
- Keep changes within module boundaries described in `ARCHITECTURE.md`.
- Prefer small, reviewable PRs; one issue → one PR whenever possible.
- Update `ARCHITECTURE.md` and relevant `spec/*` docs when changing boundaries or runtime flows.

## Determinism and safety (VibeGuard-specific)
- Gates must be **deterministic** (same inputs → same outputs).
- Default: **no network access** from gates. If a future gate needs network, it must be explicitly policy-enabled and documented as a trust boundary.
- Fail closed: if a gate cannot run reliably, the overall result is failure.
- Findings must include actionable evidence (file paths, lines, or command output references) without leaking secrets.

## Secure-by-default requirements
- Validate all external inputs (CLI args, file paths, YAML/JSON policy files).
- Use allowlists where possible; sanitize and normalize inputs.
- Use timeouts and retries for outbound calls; never infinite waits.
- Avoid logging secrets, tokens, credentials, or sensitive payloads.
- Use least privilege for any credentials or permissions.

## Dependencies
- Prefer standard library over new packages.
- New dependencies must be justified in the spec and documented in `DEPENDENCY_POLICY.md`.
- Never add dependencies that expand attack surface unnecessarily (e.g., unmaintained parsing libs) without security review.

## Output requirements for AI-generated work
All AI-driven work must follow: **Plan → Patch → Verify** (see `REPO_CONTRACT.md`).

Verification minimum:
- `make verify`
- relevant unit tests (pytest) for new logic
