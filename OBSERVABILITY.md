# Observability Standards

## Logging
- Use structured logging (JSON preferred).
- Do not log secrets or sensitive payloads.
- Include correlation IDs for request flows.

## Metrics
- Define key SLOs (latency, error rate, throughput).
- Emit metrics for critical operations.

## Tracing (optional)
- Use distributed tracing where appropriate.
- Ensure traces do not include sensitive data.

## Audit logs
Any privileged or security-relevant action must produce an audit log event:
- who/what performed the action
- what was changed
- when
- result (success/failure)
