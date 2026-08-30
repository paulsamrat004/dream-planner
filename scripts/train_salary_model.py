from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "salary_data.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    # Remove unwanted Excel/index columns.
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]

    # Normalize names: Job_Role -> job_role, Monthly_Salary -> monthly_salary
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # Dataset target is Monthly_Salary.
    if "monthly_salary" in df.columns:
        df = df.rename(columns={"monthly_salary": "salary"})

    required = ["age", "city", "education", "job_role", "salary"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {missing}. "
            f"Available columns: {list(df.columns)}"
        )

    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

    df = df.dropna(subset=required).copy()

    if len(df) < 10:
        raise ValueError("At least 10 valid salary records are recommended.")

    return df


def build_preprocessor():
    numeric = ["age"]
    categorical = ["city", "education", "job_role"]

    return ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median"))
        ]), numeric),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical),
    ])


def train_and_compare(df):
    features = ["age", "city", "education", "job_role"]
    X = df[features]
    y = df["salary"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    # Three regression models are compared. Random Forest is intentionally NOT used.
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(
            random_state=42,
            max_depth=6,
            min_samples_leaf=2
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            random_state=42,
            n_estimators=100,
            learning_rate=0.05,
            max_depth=3,
            loss="squared_error"
        ),
    }

    results = []
    trained = {}

    for name, estimator in models.items():
        pipeline = Pipeline([
            ("preprocessor", build_preprocessor()),
            ("model", estimator)
        ])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        results.append({
            "model": name,
            "MAE": float(mean_absolute_error(y_test, predictions)),
            "R2": float(r2_score(y_test, predictions)),
        })
        trained[name] = pipeline

    comparison = pd.DataFrame(results)

    # Lower MAE is better; R2 breaks ties.
    best_name = comparison.sort_values(
        ["MAE", "R2"], ascending=[True, False]
    ).iloc[0]["model"]

    return comparison, trained, best_name


def save_artifacts(comparison, trained, best_name, df):
    model_path = MODEL_DIR / "salary_model.joblib"
    comparison_path = MODEL_DIR / "model_comparison.csv"
    metadata_path = MODEL_DIR / "model_metadata.json"

    joblib.dump({"model": trained[best_name], "features": ["age", "city", "education", "job_role"]}, model_path)
    comparison.to_csv(comparison_path, index=False)

    metadata = {
        "selected_model": best_name,
        "available_models": ["Linear Regression", "Decision Tree", "Gradient Boosting"],
        "random_forest": False,
        "target": "salary",
        "features": ["age", "city", "education", "job_role"],
        "training_rows": int(len(df)),
        "selection_metric": "MAE"
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main():
    print("=" * 70)
    print("AI FINANCIAL DREAM PLANNER - SALARY MODEL TRAINING")
    print("=" * 70)

    df = load_data()
    print(f"Dataset: {DATA_FILE}")
    print(f"Valid records: {len(df)}")
    print("Features: age, city, education, job_role")
    print("Target: monthly salary")

    comparison, trained, best_name = train_and_compare(df)

    print("\nModel comparison:")
    print(comparison.to_string(index=False))

    save_artifacts(comparison, trained, best_name, df)

    print(f"\nSelected model: {best_name}")
    print("Training completed successfully.")


if __name__ == "__main__":
    main()
