# Threat Model (Template)

This is a living document. Update when new trust boundaries, integrations, or privileged actions are introduced.

## Assets
- Credentials (API keys, tokens)
- Sensitive data (PII, financial, internal)
- Operational integrity (availability, correctness)
- Audit trail integrity

## Trust boundaries
- External requests (HTTP/CLI/webhooks)
- Inbound data streams (queues/events)
- Third-party integrations
- Admin/privileged operations

## Common threat classes
- Injection (command, SQL, template, prompt/tool)
- Auth bypass / privilege escalation
- Data exfiltration via logs or misconfig
- Supply chain compromise (dependencies, build pipeline)
- Tenant boundary violations (if multi-tenant)

## AI-specific risks (if applicable)
- Prompt injection and indirect prompt injection
- Tool misuse (unsafe tool invocation)
- Retrieval poisoning (RAG)
- Sensitive context leakage
- Non-human identity sprawl (agents acting with broad permissions)

## Baseline mitigations (examples)
- Input validation + allowlists
- Least privilege + scoped tokens
- Structured audit logs
- CI security scanning + dependency policy
- Secure config defaults + explicit opt-in for risky features
