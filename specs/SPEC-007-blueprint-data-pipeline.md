# SPEC-007 — Blueprint: Data Pipeline

| Campo | Valor |
|---|---|
| Status | Em implementação |
| Data | 2026-06-14 |
| ADRs aplicáveis | ADR-007 |
| Projetos referência | `case_kaggle/`, `tirolez_queries/`, `airflow_aula/` |

## Objetivo

Fornecer o blueprint canônico para projetos de pipeline de dados:
ingestão (producer), processamento (consumer/dbt), orquestração
(Airflow), serving (API), e visualização (frontend).

## Estrutura do Blueprint

```
projeto/
├── producer/              # Ingestão de dados (Kafka producer)
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
├── consumer/              # Processamento (Kafka consumer)
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
├── dbt/                   # Transformações (dbt)
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   ├── tests/
│   └── dbt_project.yml
├── airflow/               # Orquestração
│   ├── dags/
│   ├── Dockerfile
│   └── requirements.txt
├── api/                   # Serving (FastAPI)
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
├── ml/                    # ML inference (opcional)
│   ├── models/
│   ├── features/
│   ├── tests/
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/              # Dashboard (React/Vite)
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
├── infra/                 # Infra as code
│   └── docker-compose.yml
├── scripts/               # Scripts auxiliares
│   ├── seed.py
│   └── setup.sh
├── specs/                 # Especificações
│   ├── 01-producer.md
│   ├── 02-consumer.md
│   └── 03-dbt.md
├── data/                  # Dados de amostra (pequenos)
│   ├── sample/
│   └── .gitkeep
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

## Stack

| Componente | Tecnologia | Alternativa |
|---|---|---|
| Stream | Redpanda (Kafka-compatível) | Confluent Kafka |
| Storage | MinIO (S3-compatível) | AWS S3 |
| Transform | dbt-core + DuckDB | dbt + Spark |
| Orquestração | Airflow | Prefect, Dagster |
| API | FastAPI | — |
| Frontend | React + Vite + Tailwind | — |
| ML | scikit-learn + MLflow | — |
| Infra | Docker Compose | Kubernetes |

## Tecnologias vs seus projetos atuais

| Tecnologia | Onde você já usou bem | Referência |
|---|---|---|
| Kafka/Redpanda | `case_kaggle` | Melhor exemplo do portfolio |
| dbt | `case_kaggle`, `tirolez_queries` | Domínio consolidado |
| Airflow | `airflow_aula`, `gera_netao` | Já tem experiência |
| MinIO | `case_kaggle`, `infra_dados` | Já usa |
| FastAPI | `lgnd`, `park_flow` | Padrão consolidado |

## Makefile

```makefile
.PHONY: up down test lint demo

up:
	docker compose up -d

down:
	docker compose down

test:
	cd producer && pytest --cov --cov-fail-under=80
	cd consumer && pytest --cov --cov-fail-under=80
	cd api && pytest --cov --cov-fail-under=80
	cd ml && pytest --cov --cov-fail-under=80

lint:
	cd producer && ruff check .
	cd consumer && ruff check .
	cd api && ruff check .

demo: up
	@echo "=== Running demo pipeline ==="
	python scripts/seed.py
	@echo "Demo complete. Access:"
	@echo "  API: http://localhost:8000/docs"
	@echo "  Frontend: http://localhost:5173"
```

## Referências

- ADR-007: decisão sobre blueprints reutilizáveis
- Projetos referência: `case_kaggle/` (implementação completa)
- Makefile template: `templates/Makefile`
- Docker Compose template: `templates/docker-compose.yml`
