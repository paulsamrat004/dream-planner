# Simple HTML/CSS/JavaScript UI

This version replaces the Streamlit UI with a beginner-friendly web interface.

## Run

PowerShell:

```powershell
cd "C:\Users\SAMRAT PAUL\Desktop\Finance\AI_Financial_Dream_Planner"
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

API docs remain available at:

```text
http://127.0.0.1:8000/docs
```

## Files

- `frontend/static/index.html` — page structure
- `frontend/static/style.css` — simple responsive styling
- `frontend/static/app.js` — sends form data to the FastAPI `/plan` endpoint and displays results
- `api/main.py` — serves the frontend and keeps the API

No React, Node.js, npm, or JavaScript framework is required.
