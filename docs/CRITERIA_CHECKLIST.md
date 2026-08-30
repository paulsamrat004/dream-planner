# Final Capstone Criteria Checklist

This project is aligned to the supplied Advanced Final Capstone Assessment while preserving the explicit project decisions:
- inflation = **6% per year** (`0.06`)
- **Random Forest is not used**
- user-entered monthly salary is authoritative for the financial plan

| Requirement | Implementation | Status |
|---|---|---|
| Salary dataset | `data/salary_data.csv` | PASS |
| Categorical preprocessing | One-hot encoding for city, education, job role | PASS |
| 3 regression models | Linear Regression, Decision Tree, Gradient Boosting | PASS |
| Random Forest | Explicitly excluded by project requirement | PASS (intentional exclusion) |
| MAE + R² | `models/model_comparison.csv` | PASS |
| Best model selection | Lowest MAE, R² tie-break | PASS |
| Saved selected model | `models/salary_model.joblib` | PASS |
| Experience excluded | Not a feature | PASS |
| Marriage/Car/Home | Separate goal calculations | PASS |
| Inflation | Fixed 6% annually | PASS |
| Monthly investment | Future-value annuity calculation, 10% annual return assumption | PASS |
| Combined requirement | Sum of goal requirements | PASS |
| Feasibility | Surplus/shortfall + three statuses | PASS |
| Gap actions | Timeline, savings %, goal amount suggestions | PASS |
| Timeline/savings recalculation | Form submits current values to `/plan` | PASS |
| Investment categories | Short/medium/long documented broad categories | PASS |
| No individual securities | Educational category language only | PASS |
| Agent | Natural-language extraction + tool selection | PASS |
| Deterministic calculations | Financial formulas remain in Python tools | PASS |
| RAG | 3 local documents + local vector retrieval + grounded fallback | PASS |
| Unknown RAG question | Returns unavailable message | PASS |
| Prompt injection test | Automated test included | PASS |
| FastAPI | Local `/plan`, `/salary/predict`, `/agent/plan`, `/rag/query`, `/cities`, `/health` | PASS |
| Local/no paid API | Ollama optional; application runs without paid API | PASS |
| 15+ tests | 24 automated tests | PASS |
| Architecture/DFD | `docs/architecture.svg`, `docs/ARCHITECTURE.md` | PASS |
| Project report | `docs/PROJECT_REPORT.md` and PDF | PASS |
| Demo checklist | `docs/DEMO_CHECKLIST.md` | PASS |
| Demo video/viva | Must be recorded/presented by the student | EXTERNAL |

## Inflation wording note

The supplied PDF text contains `0.06%` in its inflation line, while the project requirement requested by the student is **6% per year**. This implementation intentionally uses `0.06` as the Python rate, i.e. **6% per year**, and all tests/documentation use that project decision.
