# SPEC-013 — Blueprint: Landing Page

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-007 |
| Projetos referência | `bloco26/`, `secreta/`, `dviz_pag/` |

## Objetivo

Fornecer blueprint canônico para landing pages estáticas (HTML/CSS/JS
puro, sem framework). Ideal para projetos simples que não precisam de
Python, Docker, ou backend.

## Estrutura

```
projeto/
├── index.html             # página principal
├── obrigado.html          # página de confirmação (opcional)
├── css/
│   └── style.css
├── js/
│   └── main.js            # (opcional)
├── assets/
│   ├── images/
│   └── fonts/
├── CNAME                  # domínio customizado (GitHub Pages)
├── .gitignore
└── README.md
```

## Stack

| Componente | Recomendado |
|---|---|
| Markup | HTML5 com semântica (`<header>`, `<section>`, `<footer>`) |
| Style | CSS3 Grid/Flexbox ou Tailwind CDN |
| JS | Vanilla JS (mínimo necessário) |
| Deploy | GitHub Pages, Vercel, Netlify |
| Analytics | Google Analytics ou Plausible |

## Qualidade

- `<!DOCTYPE html>` presente em todos os HTMLs
- `<meta name="viewport">` para responsividade
- Design responsivo (testar em mobile)
- **Sem** `__pycache__/`, `.venv/`, ou outros artefatos Python
- Deploy configurado

## Checks Ativados

`LandingHtml5Doctype`, `LandingMetaViewport`,
`LandingNoVenv`, `LandingNoPycache`

## Referências

- Blueprint: `blueprints/blueprint-landing-page.yaml`
- Projetos referência: `bloco26/`, `secreta/`, `dviz_pag/`
