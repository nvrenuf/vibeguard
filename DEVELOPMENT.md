# Development Guide

## Prerequisites
- Git
- Python 3.11+

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e apps/cli
pre-commit install
```

## Standard commands
- `make verify` — pre-commit + tests
- `pytest -q` — tests only
- `vibeguard --help` — CLI help

## Adding a new gate (v0 rules)
1) Create a spec in `SPECS/` first.
2) Implement deterministic logic in `packages/gates/`.
3) Add unit tests.
4) Update baseline policy bundle if the gate is enabled by default.
5) Update `spec/GATES.md` if the output contract changes.
