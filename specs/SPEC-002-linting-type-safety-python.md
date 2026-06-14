# SPEC-002 — Linting e Type Safety Python

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-002 |
| Projetos referência | `case_kaggle/`, `lgnd/`, `open_qix/` |

## Objetivo

Garantir que todo projeto Python tenha linting (ruff) e type checking
(mypy strict). Prevenir bugs de tipo, garantir consistência de estilo,
e permitir que agentes de AI gerem código que passa na verificação.

## Contrato

### Entrada

Projeto Python com `pyproject.toml`.

### Saída

- `ruff check` passa sem erros (preferência: all rules)
- `ruff format` aplicado (diferença zero)
- `mypy --strict` passa sem erros

## Implementação

### 1. Configuração ruff

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D203",    # conflito com D211 (one-blank-line-before-class)
    "D213",    # conflito com D212 (multi-line-summary-first-line)
    "D407",    # conflito com numpy-style docstrings
    "D416",    # conflito com numpy-style docstrings
    "ANN101",  # self type annotation
    "ANN102",  # cls type annotation
    "CPY001",  # copy-right (não aplicável)
    "TD002",   # missing author in TODO
    "TD003",   # missing issue link in TODO
    "ERA001",  # commented-out code (útil em dev)
    "FBT001",  # boolean trap (muito agressivo)
    "FBT002",  # boolean default trap
    "PLR0913", # too many arguments (usar com critério)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"

[tool.ruff.lint.per-file-ignores]
"tests/*.py" = [
    "S101",    # assert (permitido em testes)
    "ANN201",  # missing return type (test fixtures)
    "D100",    # missing docstring
    "D101",    # missing docstring
    "D102",    # missing docstring
    "PLR2004", # magic values (testes têm valores mágicos)
]
```

### 2. Configuração mypy

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_ignores = true
warn_redundant_casts = true
warn_unused_configs = true
ignore_missing_imports = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
check_untyped_defs = false

[[tool.mypy.overrides]]
module = [
    "tests/*",
]
ignore_errors = true
```

### 3. Comandos

```bash
# Lint
ruff check .
ruff check --fix .   # auto-fix

# Formatação
ruff format .
ruff format --check .   # CI mode

# Type check
mypy src/
mypy app/

# Tudo (via Makefile)
make lint
make format
make typecheck
```

## Critério de Aceite

- [ ] `ruff check .` passa sem erros
- [ ] `ruff format --check .` passa (diferença zero)
- [ ] `mypy` passa sem erros
- [ ] Configuração no `pyproject.toml`
- [ ] CI roda lint e type check (SPEC-003)
- [ ] Pre-commit hooks configurados (SPEC-010)

## Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Mypy strict muito agressivo para projetos legado | Usar `follow_imports = skip` para módulos não migrados; criar `mypy.ini` com exclusões |
| Ruff "ALL" rules pode ser barulhento | Usar `ignore` para regras conflitantes (ver config acima) |
| Ruff + mypy lentos em projetos grandes | `ruff check` é rápido; mypy usa cache (`--cache-dir`) |

## Projetos que Precisam Adequação

Todos os projetos Python. Prioridade: `agent_erp`, `gera_netao`, `lang_chat`, `rag_corporativo`

## Referências

- ADR-002: decisão sobre ruff + mypy strict
- Template: `templates/pyproject.toml`
- Projetos referência: `case_kaggle/pyproject.toml`, `open_qix/services/*/pyproject.toml`
