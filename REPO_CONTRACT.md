# Repository Contract — AI-Assisted Development (VibeGuard)

This repository uses AI tools (Codex / Claude Code) to accelerate implementation.
**AI is not allowed to define requirements or architecture**. AI output is treated as untrusted until verified.

## Mandatory reading (always)
Before generating or modifying code, the AI tool MUST read (or be provided) the following files:

- `REPO_CONTRACT.md`
- `AI_CODING_RULES.md`
- `ARCHITECTURE.md`
- `ACCEPTANCE_CRITERIA.md`
- `spec/VIBEGUARD_CORE.md`
- The relevant spec in `SPECS/` (e.g., `SPECS/ISSUE-123-*.md`)

If any of these are missing from context, the AI must stop and request them.

## Required output format: Plan → Patch → Verify
All AI-driven work must follow this structure.

### 1) PLAN
- Identify the spec and restate intended outcome.
- List files to be changed.
- Identify risks and how they will be mitigated.
- State how you will verify.

### 2) PATCH
- Provide the minimal code changes to implement the spec.
- Keep changes tight and avoid unrelated refactors.

### 3) VERIFY
- Run `make verify` and relevant tests.
- Include output or describe what was run and the result.

## Change management rules
- Any new gate must include unit tests and a documented output contract.
- Any policy schema change must include:
  - schema update
  - migration notes (if needed)
  - baseline policy bundle update
- Any audit pack change must include:
  - updated `audit-pack/` templates
  - backward compatibility notes (if breaking)

## No silent scope creep
If the spec is unclear or incomplete, the AI must:
- propose edits to the spec
- stop implementation until the spec is updated
