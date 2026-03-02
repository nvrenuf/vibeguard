.PHONY: verify test

verify:
	@echo "Running pre-commit checks..."
	@python -m pre_commit run --all-files
	@$(MAKE) test

test:
	@echo "Running tests..."
	@pytest -q
