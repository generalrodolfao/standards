# ADR-009 — Arquitetura de Agentes Opensquad Padronizada

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | agentes / opensquad |

## Contexto

Você tem 11 projetos usando Opensquad, mas cada um tem uma estrutura
ligeiramente diferente de `squad.yaml`, `pipeline.yaml`, e agentes.
Não há um blueprint canônico de como estruturar um squad de agentes.

Além disso, agentes de AI (Claude Code, etc.) não têm um contexto
padronizado sobre como o projeto funciona — cada `CLAUDE.md` é único.

## Decisão

**Padronizar a arquitetura de agentes Opensquad:**

### Estrutura de diretórios

```
projeto/
├── squad.yaml           # definição do squad (agentes + skills)
├── pipeline.yaml        # fluxo de execução (passos + checkpoints)
├── agents/              # definições individuais dos agentes
│   ├── agent-01.agent.yaml
│   └── agent-02.agent.yaml
├── skills/              # skills referenciadas pelos agentes
│   └── minha-skill/
│       └── SKILL.md
├── state.json           # estado da execução (gerado)
├── output/              # artefatos gerados
├── CLAUDE.md            # contexto do projeto para AI
└── .claude/             # config do Claude Code
    ├── agents/          # agentes especializados do Claude
    └── skills/          # skills do Claude
```

### Padrões de nomenclatura

- `squad.yaml`: `name`, `version`, `description`, `agents[]`, `skills[]`, `handoff_protocol`
- `pipeline.yaml`: `name`, `steps[]`, cada step com `id`, `name`, `agents`, `actions`, `checkpoint`
- Agentes: `id` kebab-case, `name` legível, `role` do sistema, `skills` referenciadas

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| Opensquad padronizado | Já usado em 11 projetos, testado | — | ✅ |
| CrewAI | Framework consolidado | Fora do ecossistema, mais pesado | ❌ |
| LangGraph | Flexível | Muito baixo nível, verboso | ❌ |
| Ad-hoc (cada projeto diferente) | Liberdade total | 11 projetos inconsistentes | ❌ |

## Consequências

- Blueprint específico para Opensquad em `blueprints/blueprint-agent-system.yaml`
- Projetos Opensquad existentes devem ser revisados contra o padrão
- `CLAUDE.md` padronizado com seções obrigatórias

## Projetos Afetados

`content_ag/`, `api_tirole/`, `gera_netao/`, `data_game/`, `dash_concer/`,
`dissec_xls/`, `gere_video/`, `landing_quarta/`, `assitencia/`, `ag/`

## Referências

- SPEC-009: blueprint detalhado de agent system
- Templates: `templates/CLAUDE.md`
- Projetos referência: `content_ag/`, `gera_netao/`
