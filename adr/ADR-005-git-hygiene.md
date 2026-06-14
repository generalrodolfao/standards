# ADR-005 — Git Hygiene: .gitignore, sem lixo, commits semânticos

| Campo | Valor |
|---|---|
| Status | Aceito |
| Data | 2026-06-14 |
| Decisores | @rodolfo |
| Tema | git / github |

## Contexto

Múltiplos projetos têm lixo commitado:
- `arvore_copa`: `__pycache__/` e `.venv/`
- `gere_video`: `venv_video/` e `venv_tts/` (virtualenvs inteiras!)
- `.DS_Store` espalhado em dezenas de projetos
- `lang_chat`: `demo.db` commitado
- `gera_netao`: `api_debug.log`, `api.log`
- `lp_rerun`: JSON e CSV brutos

Isso polui o repositório, aumenta o clone, e pode expor dados sensíveis.

## Decisão

**Regras obrigatórias para todo projeto:**

1. `.gitignore` padronizado com categorias: Python, Node, OS, IDE, logs, env, output
2. **Nunca commitar**: `__pycache__/`, `.venv/`, `node_modules/`, `.DS_Store`, `*.log`, `.env`
3. Commits semânticos (opcional mas recomendado): `tipo(escopo): mensagem`
4. Branch protection para projetos compartilhados

## Alternativas Consideradas

| Alternativa | Prós | Contras | Voto |
|---|---|---|---|
| .gitignore padronizado + revisão | Simples, eficaz | Requer disciplina inicial | ✅ |
| git-secrets + hooks | Detecta antes do commit | Complexidade extra | ❌ |
| Nenhuma regra (status quo) | Zero esforço | Lixo acumulado em 78 projetos | ❌ |

## Consequências

- Template `.gitignore` disponível em `templates/.gitignore`
- Projetos existentes precisam de mutirão de limpeza (`.git filter-branch` se necessário)
- Adicionar `gitleaks` no CI (como `agents_monit`) para detectar secrets

## Projetos Afetados

Críticos (precisam de limpeza urgente):
- `arvore_copa` — remover `__pycache__/`, `.venv/`, `.DS_Store`
- `gere_video` — remover `venv_video/`, `venv_tts/`
- `gera_netao` — remover `*.log`, adicionar ao .gitignore
- `lang_chat` — remover `demo.db`
- `lp_rerun` — limpar dados brutos

## Referências

- SPEC-005: boas práticas de git e GitHub
- Templates: `templates/.gitignore`
