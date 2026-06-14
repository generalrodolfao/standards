# ADR-006 — Taxonomia de Documentação ADR/SPEC/STD/RUNBOOK

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | docs |

## Contexto

Você já usa documentação técnica em 14 padrões diferentes — SPEC numeradas,
ADRs, SDDs, prompts, YAML de squad, READMEs, etc. O problema é que **cada
projeto inventa o próprio formato**, não há reuso entre projetos, e não
há um template canônico.

O projeto `tirolez_queries/docs/` é o mais maduro, com taxonomia
ADR + SPEC + STD + HARNESS + RUNBOOK. Precisamos padronizar e
tornar esta taxonomia reutilizável.

## Decisão

**Adotar a taxonomia do `tirolez_queries` como padrão oficial:**

| Diretório | Finalidade | Template |
|---|---|---|
| `docs/adr/` | Decisões arquiteturais (o *porquê*) | `templates/ADR_TEMPLATE.md` |
| `docs/spec/` | Especificações de implementação (o *como*) | `templates/SPEC_TEMPLATE.md` |
| `docs/std/` | Standards e normas (padrões reutilizáveis) | — |
| `docs/harness/` | Qualidade e reconciliação de dados | — |
| `docs/runbook/` | Procedimentos operacionais | — |
| `docs/reviews/` | Revisões pós-implementação | — |

Projetos pequenos (scripts únicos) podem usar README.md apenas, desde
que sigam o template mínimo. Projetos médios/grandes DEVEM usar a
taxonomia completa.

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| Taxonomia ADR/SPEC/STD/RUNBOOK | Já testada no `tirolez_queries`, funciona | Exige disciplina | ✅ |
| Docstring-only (README + docstrings) | Leve | Não escala, sem rastreabilidade | ❌ |
| Notion / Wiki externo | Rico em recursos | Fora do git, sem versionamento | ❌ |

## Consequências

- `standards/` segue esta taxonomia e serve de referência
- Projetos ativos devem ser migrados gradualmente
- ADRs e SPECs devem referenciar IDs entre si (como `tirolez_queries` faz)

## Projetos Afetados

`lgnd` (já tem docs), `tirolez_queries` (já segue), `airflow_aula` (parcial).
Novos projetos devem começar com a taxonomia desde o dia 1.

## Referências

- SPEC-006: guia detalhado de documentação técnica
- Templates: `templates/ADR_TEMPLATE.md`, `templates/SPEC_TEMPLATE.md`
- Projetos referência: `tirolez_queries/docs/`
