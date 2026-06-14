# SPEC-001 — Pipeline de Testes Python

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-001, ADR-010 |
| Projetos referência | `lgnd/`, `case_kaggle/`, `ext_domi/` |

## Objetivo

Implementar pytest com cobertura mínima de 80% em todo projeto Python.
Fechar a maior lacuna do portfolio: 80% dos projetos sem testes.

## Contrato

### Entrada

Projeto Python com no mínimo:
- `pyproject.toml` (ou `setup.cfg`)
- `requirements.txt` ou dependências gerenciadas

### Saída

- `tests/` com pelo menos 1 teste
- Cobertura ≥ 80%
- CI rodando `pytest --cov --cov-fail-under=80` (SPEC-003)
- `make test` disponível

## Implementação

### 1. Estrutura de diretórios

```
projeto/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # fixtures compartilhadas
│   ├── test_*.py            # testes organizados por módulo
│   └── test_*.py
├── pyproject.toml            # config pytest + coverage
└── Makefile                  # comando make test
```

### 2. Configuração pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
asyncio_mode = "auto"

[tool.coverage.run]
source = ["app", "src"]
branch = true
omit = ["*/tests/*", "*/__main__.py", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
    "raise AssertionError",
]
```

### 3. Comandos

```bash
# Rodar testes
pytest

# Rodar com cobertura
pytest --cov --cov-report=term-missing

# Gerar relatório HTML
pytest --cov --cov-report=html
open htmlcov/index.html
```

### 4. Plugins essenciais

```
pytest
pytest-cov
pytest-asyncio       # código assíncrono
pytest-xdist         # paralelização: pytest -n auto
pytest-mock          # mocking via mocker fixture
pytest-timeout       # timeout em testes lentos
```

### 5. Organização de testes

```
tests/
├── conftest.py           # fixtures globais
├── unit/                 # testes unitários (rápidos, sem IO)
│   ├── test_models.py
│   └── test_services.py
├── integration/          # testes de integração (com banco/API)
│   ├── test_api.py
│   └── test_database.py
└── e2e/                  # testes end-to-end (fluxo completo)
    └── test_pipeline.py
```

## Critério de Aceite

- [ ] `pytest` instalado e configurado no `pyproject.toml`
- [ ] `tests/` existe com ao menos `test_placeholder.py` para projetos novos
- [ ] `make test` executa `pytest --cov --cov-report=term-missing`
- [ ] Cobertura ≥ 80% (ou meta progressiva documentada)
- [ ] CI falha se cobertura < 80%
- [ ] Plugins `pytest-cov`, `pytest-asyncio` no requirements

## Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Projetos legado sem testes têm base grande | Meta progressiva: começar com 40%, subir 10%/mês |
| Testes que tocam banco/API são lentos | Separar unit (sem IO) de integration; usar `@pytest.mark.integration` |
| Fixtures complexas | Usar `conftest.py` hierárquico; pytest fixtures no lugar de setup/teardown manuais |

## Projetos que Precisam Adequação

Críticos: `agent_erp`, `gera_netao`, `lang_chat`, `marmisystem`, `grupo_primo`, `park_flow`, `plux_park`

## Referências

- ADR-001: pytest como framework padrão
- ADR-010: cobertura mínima de 80%
- Template: `templates/pyproject.toml`
- Projetos referência: `lgnd/` (examine `pytest.ini`, testes com asyncio), `case_kaggle/` (coverage config)
