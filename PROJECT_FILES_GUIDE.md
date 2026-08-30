# Project File Guide

## ML
- `scripts/train_salary_model.py` — Linear Regression + Decision Tree + Gradient Boosting training/comparison. Random Forest is intentionally not used.
- `data/salary_data.csv` — put your salary dataset here.
- `models/salary_model.joblib` — generated trained model.
- `models/salary_predictor.py` — prediction wrapper using the exact feature names stored in the model.

## Backend
- `api/main.py` — FastAPI backend and frontend serving.
- `financial/` — financial calculations.
- `tools/` — deterministic tools.
- `agent/` — Agent.
- `rag/` — retrieval.

## Run

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\train_salary_model.py
python -m uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/`.
