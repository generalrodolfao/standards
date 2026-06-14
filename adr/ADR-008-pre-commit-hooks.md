# ADR-008 — Pre-commit hooks obrigatórios

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | automação / qualidade |

## Contexto

A qualidade do código depende de disciplina manual. Sem automação local:
- Código não formatado entra no repositório
- `__pycache__/`, `.DS_Store`, `.env` são commitados acidentalmente
- Lint só roda no CI (descobre tarde)
- O ciclo `commit → CI falha → corrige → commit` é ineficiente

## Decisão

**Todo projeto deve usar pre-commit hooks** com pelo menos:

1. `ruff check` — lint Python
2. `ruff format` — formatação Python
3. `mypy` — type checking (para projetos com types)
4. `check-added-large-files` — evita commits de >500KB
5. `check-merge-conflict` — evita conflitos de merge
6. `detect-private-key` — evita secrets
7. `trailing-whitespace` + `end-of-file-fixer` — higiene básica
8. `check-yaml` + `check-json` + `check-toml` — validade de configs

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| pre-commit (Python) | Ecossistema rico, 3000+ hooks, amplamente usado | — | ✅ |
| Lefthook | Já usado no `aicerts`, rápido (Go) | Menos hooks disponíveis | ❌ |
| Husky (JS) | Padrão Node.js | Só para JS/TS | ❌ |
| Nenhum (status quo) | Zero configuração | Qualidade depende de lembrança | ❌ |

## Consequências

- Arquivo `.pre-commit-config.yaml` no raiz de cada projeto
- `Makefile` com `make setup` que instala os hooks (`pre-commit install`)
- CI deve também rodar os mesmos hooks

## Projetos Afetados

Todos os projetos ativos.

## Referências

- SPEC-010: configuração detalhada de pre-commit hooks
- Templates: `templates/.pre-commit-config.yaml`
- Projetos referência: `aicerts/` (lefthook), `agents_monit/` (husky)
