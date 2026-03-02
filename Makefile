PYTHON ?= python3
TMPDIR ?= /tmp
PRE_COMMIT_HOME ?= $(PWD)/.pc-home

.PHONY: verify test fmt lint

verify:
	@echo "Running pre-commit checks..."
	@TMPDIR=$(TMPDIR) PRE_COMMIT_HOME=$(PRE_COMMIT_HOME) $(PYTHON) -m pre_commit run --all-files
	@echo "Running tests..."
	@$(MAKE) test

test:
	@TMPDIR=$(TMPDIR) PYTHONPATH=apps/cli:$$PYTHONPATH $(PYTHON) -m pytest -q

fmt:
	@$(PYTHON) -m ruff format .

lint:
	@$(PYTHON) -m ruff check .
