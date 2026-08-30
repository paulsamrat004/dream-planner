# Fixed UI/API version

The UI and FastAPI schema now use the same request fields.

The `/plan` endpoint requires:

- name
- age
- city
- education
- job_role
- monthly_salary (optional)
- marriage_years
- car_years
- home_years
- saving_percent
- area_type (optional)

The JavaScript sends those exact fields.

## Run

```powershell
cd "C:\Users\SAMRAT PAUL\Desktop\pro"
.\.venv\Scripts\Activate.ps1
python -m uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Retrain ML

```powershell
python scripts\train_salary_model.py
```
