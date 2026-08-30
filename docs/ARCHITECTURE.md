# Architecture / DFD

```text
[User]
   |
   v
[HTML/CSS/JS UI]
   |
   v
[FastAPI API]
   |---------------------> [Salary ML Tool]
   |                              |
   |                              v
   |                       [Saved ML Pipeline]
   |
   +---------------------> [Financial Planner]
   |                              |
   |                              +--> [Future Cost Tool]
   |                              +--> [Investment Tool]
   |                              +--> [Feasibility Tool]
   |                              +--> [Recommendation Tool]
   |
   +---------------------> [Agent]
   |                              |
   |                              +--> deterministic tools
   |                              +--> [Local RAG Retriever]
   |
   v
[Financial Plan JSON]
   |
   v
[UI Results]

Data stores:
  data/salary_data.csv       -> ML training
  data/city_goal_costs.csv   -> goal costs
  models/salary_model.joblib -> runtime salary model
  rag/documents/*.txt        -> local knowledge
  rag/rag_index.joblib       -> local vector/retrieval index
```

The Agent orchestrates tools but does not perform the financial formulas itself. The user's entered salary is authoritative for financial calculations.
