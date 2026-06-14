# Aurum — Padrão Ouro

Validador inteligente de qualidade de projetos. Audita, detecta tipo,
corrige automaticamente.

## CLI

```bash
aurum check .            # auditar projeto (auto-detecta tipo)
aurum check . --fix      # auditar + corrigir
aurum check . --json     # saída JSON para CI
aurum init nome --blueprint rag-system  # criar projeto novo
aurum blueprints         # listar blueprints
```

## Tipos de Projeto

fullstack-web, data-pipeline, agent-system, rag-system, ai-agent, landing-page, python-tool, generic

Detectados automaticamente por arquivos presentes.

## Estrutura

```
aurum/      ← CLI tool (Python, typer + rich)
adr/        ← decisões arquiteturais
specs/      ← especificações
blueprints/ ← templates de projeto
templates/  ← arquivos para copiar (pyproject.toml, Makefile, etc)
checklists/ ← listas para auditoria manual
```

## Comandos úteis (Makefile)

```bash
make test      # pytest com coverage
make lint      # ruff check
make format    # ruff format
make typecheck # mypy
make check     # lint + typecheck + test
make setup     # instala dependências
```

## Checks

39 checks em `aurum/checks.py`. Cada check tem `id`, `severity`, `fixable`.
Checks específicos por tipo de projeto: `relevant_for = [BlueprintType.xxx]`.
