# ADR-004 — Docker Compose para todo projeto

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | infra |

## Contexto

Apenas ~12 dos 78 projetos têm Docker configurado. Projetos sem Docker:
- Dependem de ambiente local configurado manualmente
- São difíceis de reproduzir em outra máquina
- Não podem ser deployados em container facilmente
- Agentes de AI não conseguem testar em ambiente padronizado

## Decisão

**Todo projeto deve ter `docker-compose.yml` no raiz.** O compose deve
incluir todos os serviços necessários para rodar o projeto em dev:
banco de dados, cache, fila, aplicação.

Estrutura:
- `docker-compose.yml` — dev (com bind mounts para hot-reload)
- `docker-compose.prod.yml` — prod (opcional, sem bind mounts)
- `Dockerfile` — um por serviço (multi-stage quando aplicável)
- `.dockerignore` — evitar enviar lixo para o build

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| Docker Compose | Padrão de facto, simplicidade, ecossistema | — | ✅ |
| Podman Compose | Open source puro | Menos ecossistema, menos tutorial | ❌ |
| Apenas Dockerfile | Mais simples | Sem orquestração multi-serviço | ❌ |
| Nenhum (status quo) | Zero esforço | Ambiente não reproduzível | ❌ |

## Consequências

- Projetos com banco (PostgreSQL, Redis) devem ter serviço no compose
- Dados persistentes em volumes nomeados (não bind mounts)
- Variáveis de ambiente via `.env` (não hardcoded no compose)

## Projetos Afetados

Projetos que precisam de Docker: `lgnd` (já tem), `park_flow` (já tem),
`agent_erp` (já tem). Novos projetos devem começar com Docker.

## Referências

- SPEC-004: configuração detalhada do Docker Compose
- Templates: `templates/docker-compose.yml`, `templates/Dockerfile`
- Projetos referência: `lgnd/`, `case_kaggle/` (melhores exemplos)
