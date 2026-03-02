# Acceptance Criteria (Definition of Done) — Production Standard

A change may be merged only when all applicable criteria are met.

## Required for every PR
- [ ] Linked to an Issue and a spec (`SPECS/ISSUE-###-*.md`)
- [ ] `make verify` passes locally or in CI
- [ ] All CI checks pass
- [ ] No secrets added (CI secrets scanning passes)
- [ ] No unauthorized dependencies added (or justified + approved)
- [ ] Code is readable, typed where applicable, and consistent with repo standards

## Security requirements (when applicable)
- [ ] Inputs validated and sanitized
- [ ] Authn/Authz enforced for any new endpoints/actions
- [ ] Audit logging added for security-relevant operations
- [ ] Sensitive data is not logged
- [ ] Threat model impact considered (see `THREAT_MODEL.md`)

## Testing requirements (when applicable)
- [ ] Unit tests updated/added for behavior changes
- [ ] Integration tests updated/added when interfaces change
- [ ] Regression tests for bug fixes
- [ ] Negative tests for authz/input validation where feasible

## Documentation requirements (when applicable)
- [ ] `README.md` updated if the public surface changes
- [ ] `DEVELOPMENT.md` updated if local workflow changes
- [ ] `DEPLOYMENT.md` updated if deploy/runtime changes
- [ ] `SECURITY.md` updated if security posture changes
- [ ] `OBSERVABILITY.md` updated if logging/metrics/tracing changes
