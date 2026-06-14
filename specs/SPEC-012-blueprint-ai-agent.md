# SPEC-012 — Blueprint: AI Agent

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-007, ADR-009 |
| Projetos referência | `agent_erp/`, `fut_gpt/` |

## Objetivo

Fornecer blueprint canônico para agentes de IA conversacionais com
tools, memória, e orquestração via LLM.

## Estrutura

```
projeto/
├── agent.py               # definição do agente (classe / executor)
├── tools/
│   ├── __init__.py
│   ├── search_tool.py     # tool de busca
│   └── api_tool.py        # tool de API
├── memory.py              # configuração de memória
├── prompts/
│   ├── system.md          # system prompt
│   └── few_shot.md        # exemplos few-shot
├── app/
│   ├── api.py             # FastAPI (opcional)
│   └── streamlit_app.py   # UI (opcional)
├── tests/
│   ├── test_agent.py      # teste do agente
│   └── test_tools.py      # teste das tools
├── docker-compose.yml
├── .env.example
├── Makefile
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

## Tech Stack

| Componente | Recomendado | Alternativa |
|---|---|---|
| Framework | LangChain | CrewAI, OpenAI Agents SDK |
| LLM | OpenAI GPT-4o | Anthropic, OpenRouter |
| Memória | ConversationBufferMemory | Redis, SQLite |
| Tools | @tool decorator | Tool() class |
| API | FastAPI | — |
| UI | Streamlit | Chainlit, Gradio |

## Qualidade

- Definição do agente em `agent.py` com executor configurado
- Tools definidas com `@tool` e documentadas
- Memória configurada para contexto entre turnos
- Testes do agente e das tools
- System prompt versionado em `prompts/system.md`

## Checks Ativados

`AgentDefinition`, `AgentToolDefinition`, `AgentMemory`, `AgentTestExists`

## Referências

- Blueprint: `blueprints/blueprint-ai-agent.yaml`
- Projetos referência: `agent_erp/`, `fut_gpt/`
