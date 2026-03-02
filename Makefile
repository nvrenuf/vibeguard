.PHONY: verify
verify:
	@echo "Running pre-commit checks..."
	@python -m pre_commit run --all-files

# Add stack-specific targets as your repo evolves:
# .PHONY: test
# test:
# 	pytest -q
