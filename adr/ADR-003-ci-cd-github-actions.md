# ADR-003 — CI/CD obrigatório via GitHub Actions

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | infra / automação |

## Contexto

Dos 78 projetos, **apenas 1** (`agents_monit/pixel-agents`) tem GitHub
Actions configurado. O resto depende de deploy manual ou não tem deploy.

Sem CI/CD:
- Testes não são executados automaticamente
- Lint não é verificado em PRs
- Deploys são manuais e propensos a erro
- Agentes de AI não têm feedback automatizado

## Decisão

**Todo projeto deve ter um workflow mínimo de CI via GitHub Actions**
que execute:

1. **Lint** — ruff (Python) / biome (JS/TS)
2. **Test** — pytest com coverage (Python) / vitest (JS/TS)
3. **Build** — verificação de que o projeto compila/empacota

Projetos com deploy devem ter CD configurado (Vercel, Railway, Docker Hub).

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| GitHub Actions | Gratuito, integrado, ecossistema rico, matrix builds | — | ✅ |
| GitLab CI | Bom se já usa GitLab | Seus projetos estão no GitHub | ❌ |
| CircleCI | Rápido | Custo, vendor lock-in | ❌ |
| Nenhum (status quo) | Zero esforço | 78 projetos sem rede de segurança | ❌ |

## Consequências

- Template de workflow em `.github/workflows/ci.yml`
- Badge de CI no README de cada projeto
- `dependabot` para dependências (seguindo `agents_monit`)
- `gitleaks` para secrets (seguindo `agents_monit`)

## Projetos Afetados

Todos os projetos ativos com deploy: `lgnd`, `case_kaggle`, `linkedin_opt`,
`plux_park`, `park_flow`, `marmisystem`, `aicerts`, `agent_erp`, `ebook`

## Referências

- SPEC-003: configuração detalhada do workflow de CI
- ADR-008: pre-commit hooks (complemento local do CI)
- Templates: `.github/workflows/ci.yml`
- Projetos referência: `agents_monit/pixel-agents/` (4 workflows)
