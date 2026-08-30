# AI Financial Dream & Goal Planner — Final Project

An educational, local financial-planning application for fresher-focused goal planning. It combines a FastAPI API, HTML/CSS/JavaScript UI, deterministic financial tools, salary ML, an Agent, and local RAG.

## Final project decisions

- **Inflation: 6% per year** (`INFLATION_RATE = 0.06`).
- **Random Forest: NOT USED**. The salary model comparison uses Linear Regression, Decision Tree and Gradient Boosting.
- **Entered salary is authoritative** for the `/plan` financial calculation. ML salary prediction is a separate reference/tool result and is never substituted for an entered salary.
- Experience is excluded because the project treats users as freshers.
- Expected annual investment return is a documented 10% project assumption.
- Recommendations are broad educational categories only; no individual securities or guaranteed returns are given.

## Run locally on Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts\train_salary_model.py
python -m uvicorn api.main:app --reload
```

Open:

`http://127.0.0.1:8000/`

FastAPI serves the HTML/CSS/JS frontend through its static-file mounting.

## Optional semantic RAG packages

The project runs with the local TF-IDF vector retrieval backend in the base requirements. If a machine supports the optional semantic stack, install:

```powershell
python -m pip install -r requirements-rag-optional.txt
```

## Training

```powershell
python scripts\train_salary_model.py
```

The script compares:

1. Linear Regression
2. Decision Tree
3. Gradient Boosting

and saves the selected model to `models/salary_model.joblib`.

## Tests

```powershell
pytest -q
```

The final project contains 24 automated tests covering inflation, timelines, savings limits, salary-primary behavior, feasibility, datasets, model comparison, RAG grounding, unknown RAG questions, prompt injection and other required behavior.

## Project structure

- `api/` — FastAPI application and request schemas
- `financial/` — deterministic planner/calculation logic
- `tools/` — future-cost, investment, feasibility, recommendation and salary tools
- `agent/` — natural-language Agent/parser
- `rag/` — local documents and retrieval index
- `data/` — salary and city/goal datasets
- `models/` — trained salary model and comparison artifacts
- `frontend/static/` — HTML/CSS/JavaScript UI
- `scripts/` — salary model training
- `tests/` — automated tests
- `docs/` — report, DFD, criteria checklist and test evidence

## Important

This is an educational simulation, not professional financial advice. Returns are not guaranteed.
