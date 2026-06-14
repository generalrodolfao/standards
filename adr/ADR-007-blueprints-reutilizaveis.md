# ADR-007 — Blueprints de projeto reutilizáveis

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | templates / organização |

## Contexto

Você repete os mesmos 4 tipos de projeto:
- **Data Pipeline**: Kafka + dbt + Airflow + MinIO + API
- **Fullstack Web**: FastAPI + React/Vite + PostgreSQL
- **Agent System**: Opensquad (squads + agentes + skills)
- **Python Script**: Script único que vira mini-ferramenta

Cada vez você começa do zero ou copia manualmente de um projeto anterior.
Não há um template padronizado para cada tipo. Isso gera inconsistência
e retrabalho.

## Decisão

**Criar 4 blueprints oficiais**, um para cada tipo de projeto, contendo:
- Estrutura de diretórios
- `Makefile` com comandos padronizados
- `docker-compose.yml` específico do tipo
- `pyproject.toml` / `package.json` com dependências típicas
- Checklist de qualidade para o tipo específico
- Referência ao(s) projeto(s) exemplo(s)

Cada blueprint é um arquivo YAML descritivo + diretório de template.

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| Blueprints YAML + templates | Leve, versionado, fácil de consultar | — | ✅ |
| Cookiecutter | Geração automática de projeto | Mais complexo, menos transparente | ❌ |
| Opensquad agents geram projeto | Automático, AI-powered | Imaturo, sem garantia de qualidade | ❌ |

## Consequências

- Blueprints em `standards/blueprints/`
- Cada blueprint documenta estrutura, tech stack, padrões e checklists
- Projetos novos seguem o blueprint antes de começar

## Projetos Afetados

Projetos futuros. Projetos existentes servem de referência para os blueprints.

## Referências

- SPEC-007: blueprint data pipeline
- SPEC-008: blueprint fullstack web
- SPEC-009: blueprint agent system
- SPEC-010: blueprint python script
- Templates em `standards/templates/`
