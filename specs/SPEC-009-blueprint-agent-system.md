# SPEC-009 — Blueprint: Agent System (Opensquad)

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-007, ADR-009 |
| Projetos referência | `content_ag/`, `gera_netao/` |

## Objetivo

Fornecer blueprint canônico para sistemas multi-agente usando Opensquad.
Padronizar a estrutura de squad.yaml, pipeline.yaml, agentes, e skills.

## Estrutura do Blueprint

```
projeto/
├── squad.yaml              # Definição do squad
├── pipeline.yaml           # Fluxo de execução
├── agents/                 # Definições individuais
│   ├── arquiteto.agent.yaml
│   ├── escritor.agent.yaml
│   └── revisor.agent.yaml
├── skills/                 # Skills dos agentes
│   ├── pesquisa/
│   │   └── SKILL.md
│   ├── escrita/
│   │   └── SKILL.md
│   └── revisao/
│       └── SKILL.md
├── output/                 # Artefatos gerados
│   └── .gitkeep
├── state.json              # Estado da execução (gerado)
├── _opensquad/             # Framework
├── .claude/
│   ├── agents/             # Agentes Claude Code
│   └── skills/             # Skills Claude Code
├── CLAUDE.md               # Contexto do projeto
├── .env.example
├── .gitignore
└── README.md
```

## squad.yaml padrão

```yaml
name: nome-do-squad
version: 1.0.0
description: >
  Missão do squad em uma frase.

agents:
  - id: agente-arquiteto
    name: Arquiteto
    role: architect
    definition: agents/arquiteto.agent.yaml
    skills:
      - pesquisa
      - escrita

  - id: agente-escritor
    name: Escritor
    role: writer
    definition: agents/escritor.agent.yaml
    skills:
      - escrita

  - id: agente-revisor
    name: Revisor
    role: reviewer
    definition: agents/revisor.agent.yaml
    skills:
      - revisao

skills:
  - id: pesquisa
    type: prompt-only
    source: skills/pesquisa/SKILL.md

  - id: escrita
    type: prompt-only
    source: skills/escrita/SKILL.md

  - id: revisao
    type: prompt-only
    source: skills/revisao/SKILL.md

handoff_protocol:
  format: briefing
  checkpoint_approval: sequential
```

## pipeline.yaml padrão

```yaml
name: workflow-padrao
version: 1.0.0

steps:
  - id: pesquisa
    name: "Pesquisa e planejamento"
    agents: [agente-arquiteto]
    parallel: false
    checkpoint: true
    actions:
      agente-arquiteto:
        prompt: >
          Seu briefing aqui.
        output: plano
    conditions:
      green_signal: "Plano aprovado"
      red_signal: "Revisar briefing"
    output: plano

  - id: producao
    name: "Produção de conteúdo"
    agents: [agente-escritor]
    parallel: false
    checkpoint: true
    actions:
      agente-escritor:
        prompt: >
          Seu briefing aqui. Use o plano: {{outputs.pesquisa.plano}}
        output: rascunho
    output: rascunho

  - id: revisao
    name: "Revisão e qualidade"
    agents: [agente-revisor]
    parallel: false
    checkpoint: true
    actions:
      agente-revisor:
        prompt: >
          Revise: {{outputs.producao.rascunho}}
        output: revisado
    output: final
```

## CLAUDE.md (projetos AI)

```markdown
# Nome do Projeto

Este projeto usa Opensquad para orquestrar um squad de agentes AI.

## Estrutura

- `squad.yaml` — definição do squad e agentes
- `pipeline.yaml` — fluxo de execução (passos, checkpoints, handoffs)
- `agents/` — definições individuais dos agentes
- `skills/` — instruções detalhadas para cada skill

## Pipeline

1. `make setup` — configura o projeto
2. `make run` — executa o pipeline
3. `make review` — revisa o output

## Output

Resultados em `output/`. Estado em `state.json`.
```

## Referências

- ADR-009: decisão sobre arquitetura de agentes Opensquad
- Projetos referência: `content_ag/`, `gera_netao/`
- Template: `templates/CLAUDE.md`
