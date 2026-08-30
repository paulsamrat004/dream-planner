# AI Financial Dream & Goal Planner — Final Project Report

## 1. Problem
The system helps fresher users estimate the affordability of Marriage, Car and Home goals using current city costs, a user-entered monthly salary, a saving percentage and goal timelines.

## 2. Input design
Inputs include name, age, city, education, job role, monthly salary, saving percentage, goal timelines and optional area type. Experience is intentionally excluded because users are treated as freshers.

## 3. Dataset and preprocessing
The salary dataset uses Age, City, Education, Job_Role and Monthly_Salary. Unwanted index columns are removed, numeric fields are coerced, and invalid required rows are removed. City, education and job role are one-hot encoded with unknown-category handling.

## 4. Machine learning
Three regression models are compared:
1. Linear Regression
2. Decision Tree Regressor
3. Gradient Boosting Regressor

Random Forest is intentionally not used. Models are evaluated with MAE and R². The selected model minimizes MAE, with R² as the tie-breaker. The selected pipeline is saved as `models/salary_model.joblib`.

## 5. Salary rule
If the user enters a monthly salary, that exact number is the primary salary for all financial calculations. The ML prediction is shown only as a separate reference. It cannot replace the entered salary in `/plan`.

## 6. Financial calculations
For every goal:

- Future Cost = Current Cost × `(1 + 0.06)^Years`
- Monthly investment uses the future-value annuity formula with a 10% expected annual return assumption.
- Available monthly investment capacity = Monthly Salary × Saving % / 100.
- Total required monthly investment = Marriage + Car + Home monthly requirements.
- Surplus/shortfall = Available capacity − Total requirement.

## 7. Feasibility
- Achievable: required <= available
- Challenging: required/available <= 1.5
- Highly Challenging: otherwise

Each goal is also classified with the same deterministic rule and displayed in the UI.

## 8. Gap-reduction guidance
When a shortfall exists, the system suggests increasing the saving percentage, increasing the timeline, or adjusting the goal amount/scope.

## 9. Investment categories
- Up to 3 years: short-term / lower-volatility / capital-preservation-oriented category.
- 4–7 years: medium-term / diversified balanced category.
- More than 7 years: long-term / diversified growth-oriented category.

These are broad educational categories only.

## 10. Agent
The local Agent extracts user information, decides which tools are needed, and delegates deterministic calculations to Python tools. It can optionally use Ollama for extraction, but the application does not require a paid API.

## 11. RAG
Three local documents are included under `rag/documents/`. The retriever chunks local documents and searches a local vector representation. If sufficiently relevant content is unavailable, it returns an unavailable response instead of inventing information.

## 12. API and UI
FastAPI exposes `/plan`, `/salary/predict`, `/agent/plan`, `/rag/query`, `/cities` and `/health`. The HTML/CSS/JavaScript interface is served by FastAPI.

## 13. Testing
The project contains 24 automated tests covering valid inputs, invalid timelines, saving boundaries, unknown cities/areas, salary-primary behavior, model comparison, RAG grounding, unknown knowledge questions, prompt injection and project assumptions.

## 14. Project assumptions
- Inflation: **6% per year**.
- Expected annual return: **10%**.
- No Random Forest.
- No experience feature.
- Educational simulation only; returns are not guaranteed.
