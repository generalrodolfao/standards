# {{project_name}}

{{one-line description}}

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy async + Pydantic v2
- **Frontend**: React + Vite + Tailwind + shadcn/ui
- **Database**: PostgreSQL 16
- **Cache**: Redis
- **Infra**: Docker Compose

## Project Structure

```
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── core/
│   └── tests/
├── frontend/         # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── tests/
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Commands

```bash
make setup     # Install dependencies
make dev       # Start dev server
make test      # Run tests with coverage
make lint      # Run ruff
make format    # Run ruff format
make typecheck # Run mypy
```

## Quality Gates

- Tests: `pytest --cov --cov-fail-under=80`
- Lint: `ruff check .`
- Format: `ruff format --check .`
- Types: `mypy --strict app/`
- Pre-commit hooks at commit time
- CI runs all gates on push/PR

## ADRs

Key architectural decisions in `docs/adr/`.

## Blueprint

This project follows the `fullstack-web` blueprint from `standards/`.
