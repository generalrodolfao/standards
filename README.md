<div align="center">
  <h1>Aurum ✦ Padrão Ouro</h1>
  <p><em>Validador inteligente de qualidade de projetos</em></p>

  <!-- TODO: add badges once CI is set up
  ![CI](https://img.shields.io/github/actions/workflow/status/rodolfo/aurum/ci.yml)
  ![Python](https://img.shields.io/badge/python-3.12%2B-blue)
  -->
  <img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</div>

Aurum (latim para **ouro**) audita seus projetos contra um conjunto de
padrões de qualidade — testes, lint, docker, CI, documentação — e aponta
exatamente o que precisa ser corrigido. Auto-detecção inteligente de
tipo de projeto: sabe se é um RAG, um SaaS, uma landing page ou um
pipeline de dados.

```bash
aurum check /caminho/do/projeto
# → landing-page: ✔ 4 passed  ✘ 10 failed  ⊘ 32 skipped
# → Score: 29%  (tipo: landing-page)

aurum check . --fix
# → Corrige automaticamente .gitignore, .env.example, Makefile, etc.

aurum check . --json > report.json
# → Saída estruturada para CI
```

---

## ✦ Por que Aurum?

| Problema | Como Aurum resolve |
|---|---|
| "Não sei o que meu projeto precisa ter" | Detecta automaticamente o tipo e audita os padrões corretos |
| "80% dos meus projetos não têm teste" | `PY-TEST-001` a `003`: pytest, coverage, test files |
| "Sempre esqueço .gitignore, .env.example" | `--fix` cria o que falta a partir de templates |
| "Landing page não precisa de Docker" | Auto-detection pula checks irrelevantes (⊘ skipped) |
| "Meu RAG não tem teste de retrieval" | `RAG-TEST-001`: valida se test_rag.py existe |

---

## ✦ Quick Start

```bash
pip install aurum

# Auditar projeto (auto-detecção de tipo)
aurum check .

# Auditar com tipo forçado e auto-fix
aurum check . --type rag-system --fix

# Iniciar novo projeto com blueprint
aurum init meu-projeto --blueprint rag-system

# Listar blueprints disponíveis
aurum blueprints

# Saída JSON para pipeline de CI
aurum check . --json > report.json
```

---

## ✦ Auto-detecção de Tipo

Não precisa configurar nada. Aurum identifica o tipo do projeto pelos
arquivos presentes:

| Tipo detectado | Quando |
|---|---|
| `rag-system` | chroma_db/ ou import langchain |
| `ai-agent` | agent.py ou agents/ |
| `landing-page` | Só arquivos .html (sem Python/JS framework) |
| `data-pipeline` | dbt/, airflow/, producer/ |
| `agent-system` | squad.yaml ou pipeline.yaml |
| `fullstack-web` | backend/ ou frontend/ |
| `python-tool` | pyproject.toml + main.py CLI |
| `generic` | Nenhum padrão específico identificado |

Use `--type` para forçar: `aurum check . --type python-tool`

---

## ✦ Checks por Tipo de Projeto

### Universais (todo projeto)

| ID | Check | Severidade |
|---|---|---|
| GIT-IGNORE-001 | .gitignore existe | error |
| GIT-IGNORE-005 | .gitignore inclui .env | error |
| GIT-README-001 | README.md existe | warning |
| GIT-ENV-001 | .env.example existe | warning |
| DOC-CLAUDE-001 | CLAUDE.md existe (contexto AI) | info |
| DOC-ADR-001 | docs/adr/ ou adr/ existe | info |

### Python (fullstack, data, rag, agent, tool)

| ID | Check | Severidade |
|---|---|---|
| PY-CONFIG-001 | pyproject.toml | error |
| PY-TEST-001 | pytest configurado | error |
| PY-TEST-002 | coverage fail_under >= 80 | error |
| PY-TEST-003 | testes em tests/ | warning |
| PY-LINT-001 | ruff configurado | error |
| PY-TYPE-001 | mypy configurado | warning |
| PY-MAKE-001 | Makefile com comandos | warning |

### RAG System

| ID | Check | Severidade |
|---|---|---|
| RAG-INFRA-001 | Vector store configurado | warning |
| RAG-MODEL-001 | Modelo de embedding definido | warning |
| RAG-PROMPT-001 | PromptTemplate para controle | info |
| RAG-TEST-001 | test_rag.py com retrieval | warning |

### AI Agent

| ID | Check | Severidade |
|---|---|---|
| AGENT-CONFIG-001 | Definição do agente | warning |
| AGENT-TOOL-001 | Tools com @tool decorator | info |
| AGENT-MEMORY-001 | Memória configurada | info |
| AGENT-TEST-001 | test_agent.py | warning |

### Landing Page

| ID | Check | Severidade |
|---|---|---|
| LP-HTML-001 | <!DOCTYPE html> presente | warning |
| LP-HTML-002 | <meta name="viewport"> | warning |
| LP-DIRT-001 | Sem .venv em projeto estático | warning |
| LP-DIRT-002 | Sem __pycache__ | warning |

### Python Tool

| ID | Check | Severidade |
|---|---|---|
| TOOL-CLI-001 | Entry point CLI (main()) | warning |
| TOOL-TEST-001 | Testes da ferramenta | warning |
| TOOL-DOC-001 | README com exemplos de uso | info |

### Fullstack Web

| ID | Check | Severidade |
|---|---|---|
| FW-BACKEND-001 | backend/ existe | warning |
| FW-FRONTEND-001 | frontend/ existe | info |

### Data Pipeline

| ID | Check | Severidade |
|---|---|---|
| DP-STRUCT-001 | producer/consumer/dbt/airflow | info |
| DP-DBT-001 | dbt_project.yml | info |

### Agent System (Opensquad)

| ID | Check | Severidade |
|---|---|---|
| AS-SQUAD-001 | squad.yaml | error |
| AS-PIPELINE-001 | pipeline.yaml | error |
| AS-SKILLS-001 | skills/ com SKILL.md | warning |

---

## ✦ Arquitetura

```
aurum/
├── adr/               # Decisões arquiteturais (porquê)
├── specs/             # Especificações detalhadas (como)
├── blueprints/        # Templates de projeto
├── templates/         # Arquivos para copiar (pyproject.toml, Makefile, etc.)
├── checklists/        # Listas verificáveis para auditoria manual
├── aurum/             # CLI tool
│   ├── app.py         # Comandos: check, init, blueprints
│   ├── engine.py      # Orquestrador de checks
│   ├── checks.py      # 39 checks organizados por tipo
│   ├── reporter.py    # Output terminal, JSON, Markdown
│   ├── fixer.py       # Auto-fix via templates
│   └── models.py      # CheckResult, Report, BlueprintType
└── tests/
```

Cada padrão tem:
- **ADR** (o *porquê* da decisão) → `adr/ADR-NNN-title.md`
- **SPEC** (o *como* implementar) → `specs/SPEC-NNN-title.md`
- **Template** (arquivo pronto) → `templates/`
- **Check** (verificação automatizada) → `aurum/checks.py`

---

## ✦ Projetos de Referência

Estes projetos seus serviram de base para definir os padrões:

| Projeto | Ensina |
|---|---|
| `lgnd/` | Testes, CI, Makefile, Docker, Pydantic + mypy |
| `case_kaggle/` | Pipeline dados, coverage >80%, demo end-to-end |
| `agents_monit/pixel-agents/` | Open-source readiness, CI workflows |
| `open_qix/` | Arquitetura poliglota, monorepo |
| `tirolez_queries/` | Taxonomia documentação, ADRs, auditoria |
| `galerati/` | Documentação de produto, QA checklist |

---

## ✦ Desenvolvimento

```bash
git clone https://github.com/rodolfo/aurum
cd aurum
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make check     # lint + typecheck + test
make test      # pytest com coverage
make lint      # ruff
make format    # ruff format
```

---

Licença MIT.
