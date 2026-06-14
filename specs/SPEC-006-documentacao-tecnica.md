# SPEC-006 — Documentação Técnica

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-006 |
| Projetos referência | `tirolez_queries/docs/` (taxonomia completa), `galerati/` (8 documentos) |

## Objetivo

Padronizar a documentação técnica de projetos seguindo a taxonomia
ADR/SPEC/STD/RUNBOOK, estabelecida no `tirolez_queries`.

## Contrato

### Entrada

Projeto que precisa de documentação técnica duradoura.

### Saída

Estrutura `docs/` com subdiretórios conforme a taxonomia.

## Implementação

### 1. Estrutura docs/

```
docs/
├── README.md             # Índice central, links para todos os documentos
├── adr/                  # Decision Records (ADR-NNN-title.md)
├── spec/                 # Especificações (SPEC-NNN-title.md)
├── std/                  # Standards reutilizáveis (STD-NNN.md)
├── harness/              # Qualidade e reconciliação (HARNESS-NNN.md)
├── runbook/              # Procedimentos operacionais (RUNBOOK-NNN.md)
└── reviews/              # Revisões pós-implementação (*-review.md)
```

### 2. Quando usar cada tipo

| Tipo | Quando criar | Exemplo |
|---|---|---|
| ADR | Decisão arquitetural significativa | "Usar Kafka vs RabbitMQ", "SQL vs NoSQL" |
| SPEC | Especificação de implementação | "Como funciona o pipeline de dados" |
| STD | Padrão reutilizável entre projetos | "Template de notebook", "Convenções de SQL" |
| HARNESS | Qualidade de dados | "Reconciliação entre bronze e silver" |
| RUNBOOK | Procedimento operacional | "Como dar deploy", "Como debugar" |
| Review | Pós-implementação | "Design review", "Code review", "Security review" |

### 3. Templates de documentos

Usar os templates em `standards/templates/`:

```bash
cp ../../standards/templates/ADR_TEMPLATE.md docs/adr/ADR-001-meu-titulo.md
cp ../../standards/templates/SPEC_TEMPLATE.md docs/spec/SPEC-001-meu-titulo.md
```

### 4. Índice central (docs/README.md)

```markdown
# Documentação do Projeto

## ADRs — Decisões Arquiteturais
| ID | Título | Status |
|---|---|---|
| ADR-001 | Decisão X | Aceito |

## SPECs — Especificações
| ID | Título | ADRs Relacionados |
|---|---|---|
| SPEC-001 | Implementação Y | ADR-001 |

## RUNBOOKs — Procedimentos
| ID | Título |
|---|---|
| RUNBOOK-001 | Deploy |

## Reviews
| Documento | Data |
|---|---|
| design-review.md | 2026-06 |
```

## Critério de Aceite

- [ ] `docs/README.md` com índice central
- [ ] ADRs para decisões arquiteturais significativas
- [ ] SPECs para implementações relevantes
- [ ] Documentos seguem templates padronizados (header table + seções)
- [ ] Documentos se referenciam por ID (ADR-NNN, SPEC-NNN)
- [ ] Projetos pequenos (scripts) isentos — apenas README.md

## Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Documentos ficam desatualizados | Incluir data e status; revisar em code review |
| Muito overhead para projetos pequenos | Scripts únicos: apenas README.md |
| Documentos não são lidos | ADRs e SPECs curtos; linkar no README principal |

## Projetos que Precisam Adequação

`lgnd` (já tem docs parciais), `airflow_aula` (já tem specs), `gera_netao`,
`galerati` (já tem docs excelentes). Projetos maiores que ainda não têm docs.

## Referências

- ADR-006: decisão sobre taxonomia de documentação
- Templates: `templates/ADR_TEMPLATE.md`, `templates/SPEC_TEMPLATE.md`
- Projetos referência: `tirolez_queries/docs/` (modelo), `galerati/` (8 documentos de produto)
