from models.salary_predictor import SalaryPredictor

_predictor = None

def predict_salary_tool(age: int, city: str, education: str, job_role: str) -> dict:
    global _predictor
    if _predictor is None:
        _predictor = SalaryPredictor()
    salary = _predictor.predict(age=age, city=city, education=education, job_role=job_role)
    return {
        "age": int(age), "city": city, "education": education, "job_role": job_role,
        "predicted_monthly_salary": round(float(salary), 2),
    }
