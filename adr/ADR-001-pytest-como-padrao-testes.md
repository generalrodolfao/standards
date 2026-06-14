# ADR-001 — Adotar pytest como framework de testes Python

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | testes |

## Contexto

80% dos projetos na pasta `projetos/` não têm testes automatizados.
Projetos que têm testes usam pytest (`lgnd`, `case_kaggle`, `ext_domi`).
Projetos sem testes quebraram silenciosamente ou foram abandonados.

A ausência de testes é a **maior fragilidade** do portfolio: sem rede de
segurança, refatorar é arriscado, onboarding é lento, e agentes de AI
não conseguem validar que suas mudanças funcionam.

## Decisão

**Todo projeto Python novo ou existente deve usar pytest como framework
de testes oficial.** Nenhuma alternativa (unittest, nose, doctest) será
usada em projetos novos.

Regras:
- Testes em `tests/` no raiz do projeto
- Arquivos nomeados `test_*.py`
- Usar `pytest-cov` para cobertura
- Usar `pytest-asyncio` para testes assíncronos
- Usar `pytest-xdist` para paralelização quando aplicável

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| pytest | Ecossistema rico, plugins, amplamente usado, suporte asyncio | — | ✅ |
| unittest (stdlib) | Zero dependências | Verborrágico, sem fixtures, sem plugins | ❌ |
| unittest + pytest (runner) | Usa stdlib + runner pytest | Pior dos dois mundos | ❌ |

## Consequências

- Projetos existentes sem testes precisam ser auditados e receber testes
- `pyproject.toml` deve incluir `[tool.pytest.ini_options]` e `[tool.coverage]`
- O CI (ADR-003) deve rodar `pytest --cov --cov-fail-under=80`

## Projetos Afetados

Críticos (precisam de testes urgentemente): `agent_erp`, `gera_netao`,
`lang_chat`, `marmisystem`, `grupo_primo`, `park_flow`, `plux_park`

## Referências

- SPEC-001: detalhes de implementação do pipeline de testes
- ADR-010: cobertura mínima de 80%
- Templates: `templates/pyproject.toml`, `templates/Makefile`
- Projetos referência: `lgnd/`, `case_kaggle/`, `ext_domi/`
