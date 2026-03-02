# Threat Model (VibeGuard)

This is a living document. Update it when new trust boundaries, integrations, or privileged actions are introduced.

## Assets
- Policy bundles (integrity matters)
- Findings reports (integrity matters)
- Audit packs (integrity + confidentiality)
- Local developer environment where VibeGuard executes

## Actors
- Well-meaning developers
- Malicious contributor submitting a PR (supply chain)
- Malicious policy bundle author
- Insider attempting to bypass gates

## Trust boundaries
- Repo being checked is **untrusted input**
- Policy YAML is **untrusted input**
- VibeGuard binary/runtime is the trusted computing base

## Key threats and mitigations

### 1) Policy tampering / downgrade
**Threat:** attacker modifies policy to disable gates.
**Mitigations:**
- Policy bundle hash recorded in audit pack manifest.
- CI pins to an approved policy bundle path/ref (v1+).
- Fail closed if policy missing or invalid.

### 2) Gate bypass via execution failure
**Threat:** gate errors out and run still passes.
**Mitigations:**
- Fail closed on gate execution errors.

### 3) Exfiltration of repo contents
**Threat:** a gate uploads code/data to external service.
**Mitigations:**
- v0: no network by default; disallow network in CI runners (org policy).
- Future network-enabled gates must be explicitly policy-enabled and documented.

### 4) Sensitive data leakage in logs / audit pack
**Threat:** secrets or PII end up in reports.
**Mitigations:**
- Redaction rules for findings evidence.
- Avoid embedding raw file contents; prefer pointers (path + line range).

### 5) Malicious YAML payloads
**Threat:** unsafe YAML parsing leading to code execution.
**Mitigations:**
- Use safe YAML loaders only.
- Validate schema strictly.

## Out of scope (v0)
- Running untrusted code in sandboxes
- Remote policy signing / provenance (tracked for v1+)
