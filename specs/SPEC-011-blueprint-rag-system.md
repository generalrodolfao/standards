# SPEC-011 — Blueprint: RAG System

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-007 |
| Projetos referência | `rag_corporativo/`, `rag_pdf/`, `lang_chat/` |

## Objetivo

Fornecer blueprint canônico para sistemas RAG (Retrieval-Augmented
Generation): ingestão de documentos, chunking, embedding, vector store,
recuperação e geração com LLM.

## Estrutura

```
projeto/
├── app/
│   ├── rag_engine.py       # retrieval + generation
│   ├── embeddings.py       # modelo de embedding
│   ├── prompt_templates.py # templates de prompt
│   └── vector_store.py     # interface com vector db
├── chroma_db/              # vector store local (gitignorado)
├── data/
│   ├── raw/                # documentos fonte (PDF, DOCX, TXT)
│   └── processed/          # chunked + embedded
├── tests/
│   └── test_rag.py         # teste de retrieval + QA
├── scripts/
│   ├── ingest.py           # pipeline de ingestão
│   └── query.py            # query interativa
├── docker-compose.yml
├── .env.example
├── Makefile
├── pyproject.toml
└── README.md
```

## Tech Stack

| Componente | Recomendado | Alternativa |
|---|---|---|
| Vector Store | ChromaDB | Qdrant, Pinecone, Weaviate |
| Embeddings | OpenAI text-embedding-3-small | Ollama, HuggingFace, Voyage |
| LLM | OpenAI / Anthropic | Ollama, OpenRouter |
| Framework | LangChain | LlamaIndex, custom |
| API | FastAPI | — |
| UI | Streamlit | Chainlit, React |

## Qualidade

- Vector store configurado e populado
- Modelo de embedding definido (não default)
- Template de prompt para controle de qualidade
- Testes de retrieval (recupera documentos relevantes)
- RAG checks ativados: `RagVectorStore`, `RagEmbeddingModel`, etc.

## Referências

- Blueprint: `blueprints/blueprint-rag-system.yaml`
- Projetos referência: `rag_corporativo/`, `rag_pdf/`, `lang_chat/`
