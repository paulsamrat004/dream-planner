from pathlib import Path
import joblib
import pandas as pd
from config import SALARY_MODEL_FILE

class SalaryPredictor:
    DEFAULT_FEATURES = ["age", "city", "education", "job_role"]

    def __init__(self, model_path=SALARY_MODEL_FILE):
        if not Path(model_path).exists():
            raise FileNotFoundError(
                f"Salary model not found at {model_path}. Run: python scripts/train_salary_model.py"
            )
        loaded = joblib.load(model_path)
        if isinstance(loaded, dict):
            self.model = loaded.get("model")
            self.features = loaded.get("features") or self.DEFAULT_FEATURES
        else:
            self.model = loaded
            self.features = self._features_from_pipeline()
        if self.model is None:
            raise ValueError("Saved salary model does not contain a valid model.")

    def _features_from_pipeline(self):
        try:
            preprocessor = self.model.named_steps["preprocessor"]
            features = []
            for _, _, cols in preprocessor.transformers:
                if isinstance(cols, (list, tuple)):
                    features.extend(cols)
            if features:
                return list(features)
        except Exception:
            pass
        return list(self.DEFAULT_FEATURES)

    def predict(self, age, city, education, job_role):
        values = {
            "age": int(age), "city": str(city), "education": str(education),
            "job_role": str(job_role),
            "Age": int(age), "City": str(city), "Education": str(education),
            "Job_Role": str(job_role),
        }
        normalized = {
            "age": int(age), "city": str(city), "education": str(education),
            "jobrole": str(job_role),
        }
        row_values = {}
        for feature in self.features:
            if feature in values:
                row_values[feature] = values[feature]
                continue
            key = feature.strip().lower().replace("_", "")
            if key in normalized:
                row_values[feature] = normalized[key]
            else:
                raise ValueError(f"Saved salary model requires unsupported feature: {feature}")
        row = pd.DataFrame([row_values], columns=self.features)
        return float(self.model.predict(row)[0])
