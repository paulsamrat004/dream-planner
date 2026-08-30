# Salary ML Training

Models:
- Linear Regression
- Decision Tree Regressor
- Gradient Boosting Regressor

Random Forest is intentionally not used.

Features:
- age
- city
- education
- job_role

Target:
- monthly salary

Evaluation:
- MAE
- R²

Selection:
- lowest MAE, with R² as tie-breaker

Run from the project root:

```powershell
python scripts\train_salary_model.py
```
