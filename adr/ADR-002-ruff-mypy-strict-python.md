# ADR-002 — Adotar ruff + mypy strict para Python

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | linting / tipos |

## Contexto

Apenas ~20% dos projetos têm lint configurado. Desses, alguns usam ruff
(`case_kaggle`, `lgnd`, `open_qix`), outros não têm nada.

Projetos sem type hints sofrem com:
- Bugs de tipo que poderiam ser detectados estaticamente
- Agentes de AI que produzem código inconsistente
- Dificuldade de refatoração
- Falta de auto-complete e documentação embutida

## Decisão

**Todo projeto Python novo deve usar ruff para linting + formatação e
mypy em strict mode para type checking.** Projetos existentes devem
migrar progressivamente.

### Ruff

- **All rules** (`select = ["ALL"]`) com exclusões seletivas
- `ruff format` como formatador (substitui black)
- Rodar em CI e pre-commit

### Mypy

- `--strict` habilitado
- `disallow_untyped_defs = true`
- `disallow_any_unimported = false` (relaxado para libs sem types)
- Arquivos `py.typed` para pacotes publicáveis

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| ruff + mypy strict | Mais moderno, 100x mais rápido que flake8, substitui black/isort/flake8 | Mypy pode ser exigente no começo | ✅ |
| flake8 + black + isort | Maduro, bem conhecido | Lento, várias ferramentas, sem type checking | ❌ |
| pylint + mypy | Análise profunda | Lento, falso-positivos frequentes | ❌ |
| Apenas ruff (sem mypy) | Mais simples | Sem type safety | ❌ |

## Consequências

- `pyproject.toml` unificado com `[tool.ruff]` e `[tool.mypy]`
- Projetos legado sem types: adicionar mypy gradualmente com `follow_imports = skip`
- Formatação automática via `ruff format` em pre-commit e CI

## Projetos Afetados

Todos os projetos Python. Prioridade para os ativos: `agent_erp`, `gera_netao`,
`lang_chat`, `grupo_primo`, `rag_corporativo`, `nb_pagnussati`

## Referências

- SPEC-002: configuração detalhada de ruff + mypy
- ADR-008: pre-commit hooks
- Templates: `templates/pyproject.toml`
- Projetos referência: `case_kaggle/`, `open_qix/`, `lgnd/`
