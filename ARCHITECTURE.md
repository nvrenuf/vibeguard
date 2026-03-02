# Architecture (Living Document)

This document describes the current architecture and must remain accurate.
Update this file when adding modules, changing boundaries, or changing runtime flows.

## Current state (template)
- **Domain modules:** (define here)
- **APIs:** (define endpoints, auth model, major flows)
- **Data stores:** (define schemas/ownership)
- **Integrations:** (define external dependencies)

## Trust boundaries
List where untrusted data enters and how it is validated.

## Security invariants (examples)
- All external inputs validated.
- Authz required for state-changing operations.
- Audit logs for privileged actions.

## Observability
- Structured logging required.
- Correlation IDs for request-level tracing.

## Change control
Architectural changes require:
1) A spec that explicitly authorizes the change
2) An update to this file
3) Appropriate tests and threat model review
