# SPEC-008 — Blueprint: Fullstack Web

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-007 |
| Projetos referência | `lgnd/`, `park_flow/`, `apm/` |

## Objetivo

Fornecer blueprint canônico para aplicações web fullstack:
FastAPI + PostgreSQL + React/Vite + Docker.

## Estrutura do Blueprint

```
projeto/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint
│   │   ├── routers/          # Rotas da API
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Lógica de negócio
│   │   └── core/             # Config, DB, auth
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_routers/
│   │   └── test_services/
│   ├── migrations/           # Alembic
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/         # API client
│   │   └── types/
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── Makefile
├── .env.example
├── .gitignore
├── CLAUDE.md
└── README.md
```

## Stack

| Componente | Tecnologia | Justificativa |
|---|---|---|
| Backend | FastAPI + SQLAlchemy async + Alembic | Já domina, tem no `lgnd` |
| Schemas | Pydantic v2 | Type safety, validação automática |
| Frontend | React + Vite + Tailwind + shadcn/ui | Já usa, moderno |
| Estado | Zustand | Simples, já usa no dashboard |
| Testes | pytest (backend) + vitest (frontend) | Padrão |
| Lint | ruff + mypy (backend) / biome (frontend) | ADR-002 |
| Banco | PostgreSQL 16 | Padrão |
| Cache | Redis | Sessão, rate limiting |
| Infra | Docker Compose | ADR-004 |

## Makefile

```makefile
.PHONY: setup dev test lint format migrate

setup:
	cd backend && python -m venv .venv && .venv/bin/pip install -r requirements.txt
	cd frontend && npm install
	cp .env.example .env

dev:
	docker compose up -d db redis
	cd backend && uvicorn app.main:app --reload &
	cd frontend && npm run dev

test:
	cd backend && pytest --cov --cov-fail-under=80
	cd frontend && npm test

lint:
	cd backend && ruff check . && mypy app/
	cd frontend && biome check .

format:
	cd backend && ruff format .
	cd frontend && biome format --write .

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python scripts/seed.py
```

## Rate limiting (inspirado no `lgnd`)

```python
# backend/app/core/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

## Referências

- ADR-007: decisão sobre blueprints reutilizáveis
- Projetos referência: `lgnd/` (implementação completa), `park_flow/`
- Templates: `templates/Makefile`, `templates/docker-compose.yml`
