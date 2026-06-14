.PHONY: setup dev test lint format typecheck coverage clean check ci

package = aurum

setup:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"
	pre-commit install
	cp -n .env.example .env 2>/dev/null || true

dev:
	standards check .

test:
	pytest --cov=$(package) --cov-report=term-missing

coverage:
	pytest --cov=$(package) --cov-report=html
	@echo "Open htmlcov/index.html"

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

typecheck:
	mypy $(package)

check: lint format-check typecheck test

hooks:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage *.egg-info dist build 2>/dev/null || true
