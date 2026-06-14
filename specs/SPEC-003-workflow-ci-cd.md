# SPEC-003 — Workflow CI/CD

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-003 |
| Projetos referência | `agents_monit/pixel-agents/` (4 workflows), `case_kaggle/` |

## Objetivo

Implementar CI/CD via GitHub Actions em todo projeto ativo,
com pipeline mínimo de lint → test → build.

## Contrato

### Entrada

Projeto com GitHub repo e dependências gerenciadas.

### Saída

- `.github/workflows/ci.yml` — pipeline principal
- Badge de CI no README
- Dependabot configurado para atualizações automáticas

## Implementação

### 1. Workflow CI padrão (Python)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  quality:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff mypy pytest pytest-cov

      - name: Lint
        run: ruff check .

      - name: Format check
        run: ruff format --check .

      - name: Type check
        run: mypy --strict src/ app/

      - name: Test with coverage
        run: pytest --cov --cov-report=term-missing --cov-fail-under=80

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.python-version }}
          path: htmlcov/
```

### 2. Workflow CI padrão (Node/TS)

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: latest

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - name: Install
        run: pnpm install

      - name: Lint
        run: pnpm lint

      - name: Type check
        run: pnpm typecheck

      - name: Test
        run: pnpm test

      - name: Build
        run: pnpm build
```

### 3. Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 4. Badges no README

```markdown
![CI](https://github.com/usuario/projeto/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)
```

## Critério de Aceite

- [ ] `.github/workflows/ci.yml` configurado
- [ ] `.github/dependabot.yml` configurado
- [ ] Badge de CI no README
- [ ] Pipeline passa (lint → test → build → coverage)
- [ ] Projetos com deploy têm CD configurado

## Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| CI lento (projetos grandes) | Cache de dependências (`actions/cache` ou `setup-python --cache`) |
| Matrix build consome muitos minutos | Limitar a Python 3.12, Node 20 |
| CI falha por razões externas | `continue-on-error` para jobs não críticos |

## Projetos que Precisam Adequação

Todos os projetos ativos. Prioridade: `lgnd` (já tem Makefile, falta CI),
`case_kaggle` (já tem Makefile, falta CI), `linkedin_opt`, `plux_park`,
`park_flow`, `marmisystem`, `aicerts`.

## Referências

- ADR-003: decisão sobre CI/CD obrigatório
- Templates: `.github/`
- Projetos referência: `agents_monit/pixel-agents/.github/workflows/`
