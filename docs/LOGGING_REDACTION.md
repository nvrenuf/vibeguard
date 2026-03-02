# Logging and Redaction Policy (v0.1)

This policy defines safe output behavior for CLI logs, findings, and audit-pack artifacts.

## Goals
- Prevent secret/token leakage in CLI output and generated artifacts.
- Keep findings actionable without exposing sensitive values.

## Rules
- Never include raw secret values in finding `title`, `message`, or `id`.
- Secret findings may include:
  - gate id
  - file path
  - line number
  - pattern class (`AWS Access Key ID`, `GitHub Token`, etc.)
- Secret findings must not include:
  - matched token strings
  - private key contents
  - file content excerpts
- CLI should avoid debug dumps of file contents.
- Audit-pack summaries should reference findings metadata only; no secret payload copies.

## Enforcement
- `VG003` secret scan emits generic remediation text and pattern class only.
- Tests assert that known test secrets are absent from serialized findings payloads.
- New logging/telemetry features must include redaction tests before merge.
