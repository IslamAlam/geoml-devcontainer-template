.PHONY: install
install: ## Create the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync --all-groups
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: running mypy"
	@uv run mypy

.PHONY: test
test: ## Run the tests with coverage
	@echo "🚀 Testing code: running pytest"
	@uv run python -m pytest --cov --cov-report=term-missing --cov-report=xml

.PHONY: env
env: ## Show what the container provides (Python, GDAL, GPU)
	@uv run python examples/check_environment.py

.PHONY: build
build: clean-build ## Build the wheel and sdist
	@echo "🚀 Creating wheel file"
	@uv build

.PHONY: clean-build
clean-build: ## Remove build artifacts
	@rm -rf dist

.PHONY: docs-test
docs-test: ## Check that the documentation builds without warnings
	@uv run --group docs mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run --group docs mkdocs serve

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
