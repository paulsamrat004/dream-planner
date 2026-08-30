# AI Financial Dream Planner — Runtime

## Windows setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the UI

The HTML/CSS/JavaScript UI is served by FastAPI.

```powershell
python -m uvicorn api.main:app --reload
```

Open:

`http://127.0.0.1:8000/`

## Optional model retraining

The repository includes `models/salary_model.joblib`. Retraining is optional:

```powershell
python scripts\train_salary_model.py
```

## Important salary rule

The monthly salary entered by the user is the authoritative salary for all financial calculations. ML prediction is a separate reference estimate.

## Project assumptions

- Inflation: 6% per year
- Expected annual return: 10%
- Random Forest: not used
