# Feature-name warning fix

Fixed:

`UserWarning: X has feature names, but LinearRegression was fitted without feature names`

Cause: an older saved model was fitted with an array without column names.

Fix:
1. Training uses pandas DataFrames with named columns.
2. The same exact named columns are used during prediction.
3. The saved model is a bundle containing the trained pipeline.
4. The predictor supports the new bundle and a bare pipeline for compatibility.
5. Age is included consistently in training and prediction.

After installing dependencies, retrain the model:

```powershell
python scripts\train_salary_model.py
```

Then run the UI:

```powershell
python -m uvicorn api.main:app --reload
```

Open:

`http://127.0.0.1:8000/`
