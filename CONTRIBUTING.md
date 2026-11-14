# Contributing to PayBridge

Thank you for your interest in contributing to **PayBridge â€” AI-Powered Payment Operations & FinOps Intelligence Platform**!

## Repository Architecture

The repository is organized into a clean, modern modular structure:

```
â”œâ”€â”€ .github/workflows/       # Automated CI/CD pipelines (lint, test, build)
â”œâ”€â”€ backend/                 # FastAPI REST API, database models, payment services, ingestion
â”‚   â”œâ”€â”€ app/                 # Core backend application modules
â”‚   â”‚   â”œâ”€â”€ api/             # FastAPI routes & endpoints (v1)
â”‚   â”‚   â”œâ”€â”€ core/            # Config, security, JWT auth
â”‚   â”‚   â”œâ”€â”€ db/              # SQLAlchemy session & PostgreSQL/SQLite engine
â”‚   â”‚   â”œâ”€â”€ models/          # Declarative ORM models (transactions, webhooks, audit)
â”‚   â”‚   â”œâ”€â”€ rag/             # Vector store, hybrid retriever, grounding engine
â”‚   â”‚   â”œâ”€â”€ schemas/         # Pydantic schemas (canonical payment, requests, responses)
â”‚   â”‚   â””â”€â”€ services/        # Webhook processor, CSV mapper, URL fetcher, FinOps
â”‚   â”œâ”€â”€ alembic/             # Database migrations
â”‚   â”œâ”€â”€ config/              # YAML configs & customer profiles
â”‚   â”œâ”€â”€ data/                # Sample datasets, raw uploads, lineage archives
â”‚   â”œâ”€â”€ scripts/             # Data bootstrapping & evaluation runners
â”‚   â”œâ”€â”€ main.py              # Backend entrypoint (`uvicorn backend:app`)
â”‚   â””â”€â”€ rag_agent.py         # Standalone RAG CLI query agent
â”œâ”€â”€ docs/                    # Technical architecture, API specs, governance docs
â”œâ”€â”€ frontend/                # Streamlit Operations & Intelligence Dashboard
â”‚   â”œâ”€â”€ views/               # Portal views (Overview, Transactions, Anomalies, FinOps)
â”‚   â”œâ”€â”€ dashboard.py         # Main Streamlit application entrypoint
â”‚   â”œâ”€â”€ components.py        # Reusable UI widgets & API client
â”‚   â”œâ”€â”€ styles.py            # Custom CSS & design system
â”‚   â””â”€â”€ Dockerfile           # Frontend container definition
â”œâ”€â”€ ml/                      # Machine Learning anomaly detection models
â”‚   â”œâ”€â”€ anomaly.py           # Isolation Forest + DBSCAN anomaly detector
â”‚   â””â”€â”€ __init__.py          # ML package exports
â”œâ”€â”€ screenshots/             # Product screenshots, architectural GIFs, and media
â””â”€â”€ tests/                   # Automated test suite (Unit & Integration tests)
```

---

## Local Development Setup

### 1. Prerequisites
- Python 3.11+
- Git
- Docker & Docker Compose (optional for containerized deployment)
- Ollama (optional for local LLM inference)

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/naveenkotnana/Deploy-PayBridge-PAYTM-inspired-AI-FinOps-Platform.git
cd Deploy-PayBridge-PAYTM-inspired-AI-FinOps-Platform

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Bootstrap Database & Sample Data
```bash
python backend/scripts/setup_all.py
```

### 4. Running the Services

- **Backend API**:
  ```bash
  uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
  ```
  Interactive Swagger UI documentation is available at `http://localhost:8000/docs`.

- **Frontend Dashboard**:
  ```bash
  streamlit run frontend/dashboard.py
  ```
  The dashboard will open automatically at `http://localhost:8501`.

---

## Code Quality & Testing

Before submitting a Pull Request, ensure all checks pass:

```bash
# 1. Lint and format checks
ruff check backend frontend ml tests

# 2. Run unit and integration tests
pytest tests/ -v

# 3. RAG Grounding & Evaluation
python backend/scripts/run_rag_eval.py

# 4. Agent Governance & Guardrails Evaluation
python backend/scripts/run_agent_eval.py
```

---

## Submitting Pull Requests

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Write clean, self-documenting code with type annotations and docstrings.
3. Add corresponding unit or integration tests under `tests/`.
4. Ensure all 117+ tests pass without errors or warnings.
5. Submit your PR with a clear description of changes and test results.
