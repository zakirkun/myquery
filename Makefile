# Makefile for MyQuery
# Simplified commands untuk development dan release

.PHONY: help install dev test lint format clean build release docker

# Default target
.DEFAULT_GOAL := help

help: ## Tampilkan help message
	@echo "MyQuery - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Install in development mode
	pip install -e .
	pip install pytest pytest-asyncio black ruff mypy

test: ## Run tests
	pytest tests/ -v --cov

lint: ## Run linters
	black --check .
	ruff check .

format: ## Format code
	black .
	ruff check --fix .

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '.coverage' -delete
	rm -rf .pytest_cache

build: clean ## Build binary for current platform
	python scripts/build_binary.py

build-all: ## Build binaries untuk semua platform (requires GitHub Actions)
	@echo "Building for all platforms requires GitHub Actions"
	@echo "Push a tag to trigger: git tag v0.1.0 && git push --tags"

docker-build: ## Build Docker image
	docker build -t myquery:dev .

docker-run: ## Run Docker container
	docker run -it --rm myquery:dev

docker-push: ## Push Docker image (requires auth)
	docker tag myquery:dev ghcr.io/myquery/myquery:latest
	docker push ghcr.io/myquery/myquery:latest

release-patch: ## Prepare patch release (0.0.X)
	bash scripts/prepare-release.sh patch

release-minor: ## Prepare minor release (0.X.0)
	bash scripts/prepare-release.sh minor

release-major: ## Prepare major release (X.0.0)
	bash scripts/prepare-release.sh major

install-hooks: ## Install git hooks
	@echo "Installing git hooks..."
	@echo "#!/bin/bash" > .git/hooks/pre-commit
	@echo "make lint" >> .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "✅ Git hooks installed"

docs: ## Build documentation (future)
	@echo "Documentation building not yet implemented"

serve-docs: ## Serve documentation locally (future)
	@echo "Documentation serving not yet implemented"

# Development helpers
run-chat: ## Run interactive chat
	python -m cli.main chat start

run-web: ## Run web UI
	python -m cli.main web start

run-server: ## Run MCP server
	python -m cli.main server start

# CI/CD helpers
ci-test: ## Run CI tests locally
	act -j test

ci-lint: ## Run CI linters locally
	act -j lint

ci-release: ## Simulate release build locally
	act -j build --secret-file .secrets

# Setup
setup: ## Initial setup untuk development
	@echo "🚀 Setting up MyQuery development environment..."
	python -m venv venv
	@echo "✅ Virtual environment created"
	@echo ""
	@echo "Activate it with:"
	@echo "  source venv/bin/activate  # Linux/macOS"
	@echo "  venv\\Scripts\\activate     # Windows"
	@echo ""
	@echo "Then run: make install dev"

# Version info
version: ## Show current version
	@grep -Po '(?<=version = ")[^"]*' pyproject.toml

# Security
security-check: ## Run security checks
	pip install safety bandit
	safety check
	bandit -r cli/ core/ tools/ mcp/

# Coverage
coverage: ## Generate coverage report
	pytest tests/ --cov --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

