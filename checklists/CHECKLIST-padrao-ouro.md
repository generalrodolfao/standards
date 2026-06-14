# CHECKLIST: Padrão Ouro

Use este checklist para auditar se um projeto atinge o padrão ouro.
Cada item linka para o ADR/SPEC correspondente.

## 1. Testes

- [ ] `pytest` configurado no `pyproject.toml` (ADR-001)
- [ ] `tests/` existe com ao menos um teste (SPEC-001)
- [ ] Cobertura ≥ 80% com `--cov-fail-under=80` (ADR-010)
- [ ] `make test` executa pytest com cobertura
- [ ] Testes de integração separados (`@pytest.mark.integration`)
- [ ] CI roda testes (SPEC-003)

## 2. Linting & Type Safety

- [ ] `ruff check .` passa sem erros (ADR-002)
- [ ] `ruff format --check .` passa (SPEC-002)
- [ ] `mypy --strict` passa (Python) / `tsc --strict` passa (TS)
- [ ] Configuração em `pyproject.toml` (Python) / `tsconfig.json` (TS)
- [ ] CI roda lint + type check (SPEC-003)

## 3. CI/CD

- [ ] `.github/workflows/ci.yml` com lint → test → build (ADR-003)
- [ ] `.github/dependabot.yml` configurado (SPEC-003)
- [ ] Badge de CI no README
- [ ] Pipeline passa em todos os checks

## 4. Docker

- [ ] `docker-compose.yml` no raiz (ADR-004)
- [ ] `Dockerfile` multi-stage (dev + prod) (SPEC-004)
- [ ] `.dockerignore` presente
- [ ] `docker compose up` funciona

## 5. Git Hygiene

- [ ] `.gitignore` padronizado (ADR-005)
- [ ] Sem `__pycache__/`, `.venv/`, `.DS_Store` no repo
- [ ] `.env.example` presente (`.env` no .gitignore)
- [ ] `README.md` com descrição + setup + pipeline

## 6. Documentação

- [ ] `docs/` segue taxonomia ADR/SPEC/STD/RUNBOOK (ADR-006)
- [ ] ADRs para decisões arquiteturais significativas
- [ ] `CLAUDE.md` presente (projetos com AI)
- [ ] Documentos têm header table (ID, Status, Data, Owners)

## 7. Automação

- [ ] `.pre-commit-config.yaml` presente (ADR-008)
- [ ] `pre-commit install` executado
- [ ] `Makefile` com `setup`, `test`, `lint`, `format` (SPEC-010)
- [ ] `make test` + `make lint` + `make format` passam

## 8. Arquitetura

- [ ] Segue blueprint apropriado (ADR-007)
- [ ] Separação clara de camadas (models/schemas/services/routers)
- [ ] Type hints em todo código Python
- [ ] Pydantic schemas para validação de entrada/saída

## Pontuação

| Itens | Nível |
|---|---|
| 30-32 | 🥇 Padrão Ouro |
| 25-29 | 🥈 Quase lá |
| 20-24 | 🥉 Precisa de atenção |
| < 20 | 🔴 Começar do zero |
