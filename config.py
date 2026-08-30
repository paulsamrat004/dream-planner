from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
RAG_DIR = BASE_DIR / "rag"
DOCS_DIR = RAG_DIR / "documents"

CITY_COST_FILE = DATA_DIR / "city_goal_costs.csv"
SALARY_DATA_FILE = DATA_DIR / "salary_data.csv"
SALARY_MODEL_FILE = MODEL_DIR / "salary_model.joblib"
RAG_INDEX_FILE = RAG_DIR / "rag_index.joblib"

INFLATION_RATE = 0.06
EXPECTED_ANNUAL_RETURN = 0.10  # documented project assumption
MIN_SAVING_PERCENT = 0.0
MAX_SAVING_PERCENT = 100.0
MAX_GOAL_YEARS = 50
