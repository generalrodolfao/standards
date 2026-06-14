# SPEC-010 — Automação com Pre-commit

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-008 |
| Projetos referência | `aicerts/` (lefthook), `agents_monit/` (husky) |

## Objetivo

Automatizar a qualidade do código antes do commit usando pre-commit hooks.
Impedir que código mal formatado, com erros de lint, ou com secrets chegue
ao repositório.

## Contrato

### Entrada

Projeto com Python (ruff, mypy) e/ou JS/TS (biome).

### Saída

- `.pre-commit-config.yaml` no raiz
- `make setup` instala os hooks
- Hooks rodam automaticamente em `git commit`

## Implementação

### 1. .pre-commit-config.yaml

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files
        args: ["--maxkb=500"]
      - id: check-merge-conflict
      - id: detect-private-key
      - id: check-case-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.15.0
    hooks:
      - id: mypy
        args: [--strict, --ignore-missing-imports]
        language: system
        types: [python]

  - repo: https://github.com/rhysd/actionlint
    rev: v1.7.7
    hooks:
      - id: actionlint
        files: .github/workflows/
```

### 2. Instalação

```bash
# No setup do projeto
pip install pre-commit
pre-commit install

# Via Makefile
make setup  # inclui pre-commit install
```

### 3. Makefile

```makefile
.PHONY: setup hooks

setup:
	python -m pip install -r requirements.txt
	pip install pre-commit
	pre-commit install

hooks:
	pre-commit run --all-files

hooks-quick:
	pre-commit run
```

### 4. Comandos úteis

```bash
# Rodar hooks em todos os arquivos (útil no CI)
pre-commit run --all-files

# Rodar hook específico
pre-commit run ruff --all-files

# Pular hooks (emergência)
git commit --no-verify

# Atualizar hooks para versões recentes
pre-commit autoupdate
```

## Integração com CI

O CI (SPEC-003) deve rodar `pre-commit run --all-files` como primeiro passo,
garantindo que o que passa localmente também passa no CI.

```yaml
- name: Pre-commit checks
  run: |
    pip install pre-commit
    pre-commit run --all-files
```

## Critério de Aceite

- [ ] `.pre-commit-config.yaml` configurado
- [ ] `pre-commit install` executado
- [ ] `pre-commit run --all-files` passa sem erros
- [ ] CI roda pre-commit hooks
- [ ] Hook de ruff, ruff-format, trailing-whitespace, end-of-file-fixer presentes

## Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Hooks lentos (especialmente mypy) | mypy usa cache; configurar `language: system` para usar venv |
| Hooks bloqueiam commits triviais | `git commit --no-verify` em emergência |
| Manter hooks atualizados | `pre-commit autoupdate` periódico; dependabot pode automatizar |

## Projetos que Precisam Adequação

Todos os projetos ativos. Prioridade: projetos com mais colaboração/agentes AI.

## Referências

- ADR-008: decisão sobre pre-commit hooks
- Templates: `templates/.pre-commit-config.yaml`
- Projetos referência: `aicerts/` (lefthook), `agents_monit/` (husky + eslint)
