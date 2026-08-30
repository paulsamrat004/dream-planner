# Entered Salary Is Primary

The financial plan now uses the user's entered `monthly_salary` as the primary income value.

It controls:
- available monthly investment capacity
- total required monthly investment comparison
- surplus/shortfall
- feasibility classification
- all financial goal calculations

The ML salary prediction endpoint remains available for optional comparison, but its prediction is NOT used in `/plan`.

## Run

```powershell
cd "C:\Users\SAMRAT PAUL\Desktop\finish"
.\.venv\Scripts\Activate.ps1
python -m uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/`.

No model retraining is required for this change.
