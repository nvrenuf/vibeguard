# Observability Standards (VibeGuard)

## Logging
- Prefer structured logs (JSON) for gate execution (v1+).
- Never log secrets or raw sensitive payloads.
- Include run ID, gate ID, and policy bundle ID in every record.

## Reports
v0 uses a JSON findings report as the primary “observable” output:
- machine-readable `findings.json`
- human-readable `summary.md`

## Metrics (future)
- gate runtime by gate ID
- finding counts by severity
- pass/fail rate by policy bundle
