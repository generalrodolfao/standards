# SPEC-005 — Git e GitHub Boas Práticas

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-005 |
| Projetos referência | `agents_monit/pixel-agents/` (SECURITY.md, CONTRIBUTING.md) |

## Objetivo

Padronizar a higiene de repositórios: .gitignore, estrutura de
branches, commits, e arquivos obrigatórios.

## Implementação

### 1. .gitignore obrigatório

Copiar `templates/.gitignore` para todo projeto novo. Categorias:
- Python: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.pytest_cache/`
- Node: `node_modules/`, `.next/`, `dist/`, `build/`
- OS: `.DS_Store`, `Thumbs.db`
- IDE: `.idea/`, `.vscode/`, `*.swp`
- Logs: `*.log`
- Dados: `.env` (manter `.env.example`)
- Output: `output/`, `temp/`, `docker-data/`

### 2. Commits semânticos (recomendado)

```
tipo(escopo): descrição no imperativo

tipos: feat, fix, refactor, test, docs, chore, style, perf, ci
escopo: modulo afetado (opcional)
```

Exemplos:
```
feat(api): adiciona endpoint de busca de produtos
fix(worker): corrige timeout em processamento de imagens
test(models): adiciona testes para validação de CPF
docs(readme): atualiza pipeline de setup
```

### 3. Arquivos obrigatórios no raiz

| Arquivo | Obrigatório? | Para quê |
|---|---|---|
| `README.md` | Sim | Descrição, setup, pipeline |
| `CLAUDE.md` | Sim (projetos AI) | Contexto para agentes |
| `.gitignore` | Sim | Evitar lixo |
| `LICENSE` | Recomendado (público) | Licenciamento |
| `.env.example` | Sim | Documentar variáveis |
| `CONTRIBUTING.md` | Opcional | Guia de contribuição |
| `CHANGELOG.md` | Opcional | Histórico de versões |

### 4. Mutirão de limpeza (projetos existentes)

```bash
# 1. Adicionar .gitignore padronizado

# 2. Remover lixo do git (exemplo: __pycache__)
git rm -r --cached __pycache__/
git rm -r --cached .venv/
git rm --cached .DS_Store

# 3. Se o histórico estiver muito poluído, considerar git filter-branch
# (apenas para projetos que realmente importam)

# 4. Adicionar gitleaks para detectar secrets
# brew install gitleaks  (macOS)
# gitleaks detect --verbose
```

## Critério de Aceite

- [ ] `.gitignore` padronizado presente
- [ ] Nenhum `__pycache__/`, `.venv/`, `.DS_Store` no repo
- [ ] `.env.example` presente (`.env` no .gitignore)
- [ ] `README.md` com instruções mínimas
- [ ] `CLAUDE.md` presente (projetos com AI)
- [ ] Últimos 10 commits seguem padrão semântico

## Projetos que Precisam Adequação

- `arvore_copa`: remover `__pycache__/`, `.venv/`, `.DS_Store`
- `gere_video`: remover `venv_video/`, `venv_tts/`
- `gera_netao`: adicionar `*.log` ao .gitignore, remover logs commitados
- `lang_chat`: adicionar `*.db` ao .gitignore, remover `demo.db`
- Quase todos: adicionar `.DS_Store` ao .gitignore

## Referências

- ADR-005: decisão sobre git hygiene
- Template: `templates/.gitignore`
- Projetos referência: `agents_monit/pixel-agents/.gitignore`
