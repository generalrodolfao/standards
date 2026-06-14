# ============================================================
# Makefile — Project template
# standards/templates/Makefile
# ============================================================
.PHONY: setup dev test lint format typecheck coverage clean hooks

# ---- Setup ----

setup:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install ruff mypy pytest pytest-cov pytest-asyncio pre-commit
	pre-commit install
	cp -n .env.example .env 2>/dev/null || true

# ---- Development ----

dev:
	@echo "Starting dev server..."
	# python -m app.main

# ---- Testing ----

test:
	pytest --cov --cov-report=term-missing

coverage:
	pytest --cov --cov-report=html
	@echo "Open htmlcov/index.html"

test-fast:
	pytest -x --no-header -q

test-parallel:
	pytest -n auto --cov

# ---- Linting ----

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

typecheck:
	mypy app/ src/

check: lint format-check typecheck test

# ---- Pre-commit ----

hooks:
	pre-commit run --all-files

hooks-install:
	pre-commit install

hooks-update:
	pre-commit autoupdate

# ---- Docker ----

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-build:
	docker compose build

docker-logs:
	docker compose logs -f

# ---- Cleanup ----

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage *.egg-info dist build 2>/dev/null || true
