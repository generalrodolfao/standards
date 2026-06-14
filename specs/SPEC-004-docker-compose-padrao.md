# SPEC-004 — Docker Compose Padrão

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-004 |
| Projetos referência | `lgnd/`, `case_kaggle/`, `infra_dados/` |

## Objetivo

Padronizar o uso de Docker Compose para garantir ambiente reproduzível
em todos os projetos.

## Contrato

### Entrada

Projeto com serviços (web, banco, cache, fila).

### Saída

- `docker-compose.yml` no raiz
- `Dockerfile` por serviço
- `.dockerignore`
- Serviços essenciais configurados

## Implementação

### 1. Estrutura

```
projeto/
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
└── docker/
    ├── Dockerfile.dev
    └── wait-for-it.sh
```

### 2. docker-compose.yml padrão

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      target: dev
    ports:
      - "${PORT:-8000}:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    ports:
      - "${DB_PORT:-5432}:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis-data:/data

volumes:
  pgdata:
  redis-data:
```

### 3. Dockerfile multi-stage

```dockerfile
# Dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM base AS dev
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS prod
RUN adduser --disabled-password appuser
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. .dockerignore

```
__pycache__/
.venv/
venv/
.env
.git
.gitignore
*.md
tests/
.DS_Store
```

## Critério de Aceite

- [ ] `docker-compose.yml` no raiz com serviços essenciais
- [ ] `Dockerfile` com multi-stage (dev + prod)
- [ ] `.dockerignore` configurado
- [ ] `docker compose up` funciona sem configuração manual
- [ ] Volumes nomeados para dados persistentes
- [ ] Healthchecks nos serviços críticos

## Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Portas conflitantes | Usar `${VARIABLE:-default}` para portas customizáveis |
| Build lento | Camadas Docker otimizadas (requirements.txt antes do código) |
| Dependências de serviços (db antes da app) | `depends_on` com `condition: service_healthy` + `wait-for-it.sh` |

## Projetos que Precisam Adequação

Projetos que ainda não têm Docker: `linkedin_opt`, `rag_corporativo`,
`lang_chat`, `agent_erp` (já tem), `marmisystem`, `ebook`.

## Referências

- ADR-004: decisão sobre Docker Compose
- Templates: `templates/docker-compose.yml`, `templates/Dockerfile`
- Projetos referência: `lgnd/docker-compose.yml`, `case_kaggle/docker-compose.yml`
