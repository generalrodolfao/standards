# CHECKLIST: Novo Projeto

Use este checklist ao iniciar um projeto novo.

## Antes de escrever código

- [ ] Defini o tipo do projeto: [data-pipeline | fullstack-web | agent-system | script]
- [ ] Consultei o blueprint correspondente em `standards/blueprints/`
- [ ] Criei o repositório no GitHub
- [ ] Clonei e entrei no diretório

## Setup inicial

- [ ] Copiei `.gitignore` do `standards/templates/`
- [ ] Copiei `pyproject.toml` e ajuste (Python) ou `package.json` (JS/TS)
- [ ] Copiei `Makefile` e ajustei
- [ ] Copiei `.env.example`
- [ ] Copiei `.pre-commit-config.yaml`
- [ ] Copiei `docker-compose.yml` e ajustei
- [ ] Copiei `Dockerfile` e ajustei
- [ ] Criei `CLAUDE.md` (baseado no template)
- [ ] Criei `README.md` com descrição, setup, pipeline
- [ ] Rodei `make setup` (instala dependências + pre-commit hooks)
- [ ] Rodei `pre-commit run --all-files` para verificar
- [ ] Commit inicial com `chore: initial project setup`

## Quality gates (antes do primeiro deploy)

- [ ] `make test` passa (pelo menos 1 teste placeholder)
- [ ] `make lint` passa
- [ ] `make format-check` passa
- [ ] `make typecheck` passa (se aplicável)
- [ ] `make check` passa (lint + format + type + test)
- [ ] `.github/workflows/ci.yml` configurado
- [ ] ADR-001 criado se houver decisão arquitetural relevante
