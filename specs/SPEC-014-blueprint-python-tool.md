# SPEC-014 — Blueprint: Python Tool

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-007 |
| Projetos referência | `ext_domi/`, `nb_pagnussati/`, `yt_down/` |

## Objetivo

Fornecer blueprint canônico para ferramentas Python de linha de comando
(CLI) e scripts utilitários. Projetos pequenos mas que merecem qualidade
profissional.

## Estrutura

```
projeto/
├── main.py                # entry point CLI
├── src/
│   ├── core.py            # lógica principal
│   └── utils.py           # utilitários
├── tests/
│   ├── test_tool.py       # testes
│   └── conftest.py
├── scripts/
│   └── setup.sh           # (opcional)
├── pyproject.toml         # entry_points para pip install
├── Makefile
├── .env.example
├── .gitignore
└── README.md
```

## Stack

| Componente | Recomendado |
|---|---|
| CLI | `argparse` (stdlib) ou `typer` |
| Testing | pytest + pytest-cov (> 80%) |
| Lint | ruff + mypy strict |
| Packaging | `pyproject.toml` com `[project.scripts]` |
| Python | 3.12+ |

## Qualidade

- Entry point CLI (`main()` + `if __name__ == '__main__'`)
- Testes em `tests/` com cobertura > 80%
- README com exemplos de uso (comandos `$ ...`)
- Empacotado via `pyproject.toml` (`pip install -e .`)
- Ruff + mypy configurados

## Checks Ativados

`ToolEntryPoint`, `ToolHasTests`, `ToolHasReadme`

## Referências

- Blueprint: `blueprints/blueprint-python-tool.yaml`
- Projetos referência: `ext_domi/`, `nb_pagnussati/`, `yt_down/`
