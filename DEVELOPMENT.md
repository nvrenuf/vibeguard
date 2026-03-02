# Development Guide

## Prerequisites
- Git
- Python 3.11+ (for `pre-commit` tooling used by `make verify`)
- Optional: Node / Go / etc. depending on your project stack

## Standard commands
- `make verify` — required repo-wide quality checks (format/lint/security hooks)
- Add project-specific commands here (tests, typecheck, etc.)

## Local setup
1) Create a virtualenv (recommended):
   - `python -m venv .venv`
   - `source .venv/bin/activate`
2) Install tooling:
   - `pip install -r requirements-dev.txt`
3) Install hooks:
   - `pre-commit install`

## Adding language-specific checks
As the project is implemented, update:
- `Makefile` targets (`test`, `typecheck`, etc.)
- `.pre-commit-config.yaml` hooks as needed
