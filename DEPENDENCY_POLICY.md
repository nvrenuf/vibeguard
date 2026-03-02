# Dependency Policy

## Principles
- Minimize dependencies.
- Prefer standard library and well-maintained core frameworks.
- Pin versions for reproducibility.

## New dependency requirements
Any new dependency must:
- be explicitly justified (why the standard library is insufficient)
- be pinned (exact or narrow range)
- have an active maintenance history
- not duplicate existing tooling

## Prohibited patterns
- Unpinned dependencies in production.
- Multiple overlapping frameworks without rationale.
- Auto-upgrade dependencies without review in production repos.
