# Security Policy

VibeGuard is a security-adjacent tool. Treat correctness and trust boundaries as product-critical.

## Reporting vulnerabilities
If you believe you found a security issue:
- Prefer private disclosure (security email/ticket) over public issues.
- Include reproduction steps and impact.

## Security posture (v0)
- Local-first CLI; **no network access required** for baseline gates.
- Fail-closed behavior for policy load failures and gate execution errors.
- Audit pack output is stored locally by default.

## Hard requirements
- Never log secrets or sensitive repo contents.
- Policies are treated as untrusted input (validate schema, safe YAML parsing).
- Any feature that introduces network calls, remote execution, or credential usage
  requires:
  - an explicit spec
  - threat model update
  - security review
