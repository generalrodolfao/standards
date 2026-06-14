# ADR-010 — Cobertura de Testes Mínima de 80%

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | testes / qualidade |

## Contexto

Cobertura de testes abaixo de 80% significa que partes significativas
do código nunca são executadas em teste. O `case_kaggle` já usa
`--cov-fail-under=80` e se beneficia disso.

Projetos sem métrica de cobertura:
- Não sabem o que não está testado
- Tendem a acumular dívida técnica
- Agentes de AI não conseguem validar se cobriram o suficiente

## Decisão

**Todo projeto com `pytest` deve ter cobertura mínima de 80%** com falha
automática no CI se abaixo disso.

```
# pyproject.toml
[tool.coverage.run]
source = ["src", "app"]
branch = true

[tool.coverage.report]
fail_under = 80
```

Exceções:
- Scripts de entrada (CLI, `__main__.py`) — não precisam de cobertura
- Código gerado automaticamente — pode ser excluído
- Projetos legado: meta progressiva (ex: começar com 40%, subir 10% a cada mês)

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| 80% fixo com fail_under | Simples, enforcement automático | Pode incentivar testes rasos | ✅ |
| 80% com code review | Mais flexível | Depende de disciplina humana | ❌ |
| Sem métrica (status quo) | Zero pressão | 80% dos projetos sem teste | ❌ |

## Consequências

- `pyproject.toml` deve incluir config de coverage
- CI deve rodar `pytest --cov --cov-report=term-missing --cov-fail-under=80`
- Relatório de cobertura deve ser gerado em HTML para inspeção
- Branches não devem ser mergeados abaixo de 80%

## Projetos Afetados

`lgnd` (já tem), `case_kaggle` (já tem). Os demais projetos Python
precisam ser auditados e receber testes até atingir 80%.

## Referências

- ADR-001: pytest como framework padrão
- SPEC-001: pipeline de testes (inclui config de coverage)
- Templates: `templates/pyproject.toml`
- Projetos referência: `case_kaggle/` (coverage >80%), `lgnd/`
