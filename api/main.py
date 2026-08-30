from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.schemas import PlanRequest, AgentRequest, RAGQuestion
from financial.planner import build_plan
from financial.recommendations import build_recommendations
from tools.salary_tool import predict_salary_tool
from agent.agent import FinancialAgent
from rag.retriever import retrieve


app = FastAPI(
    title="AI Financial Dream & Goal Planner",
    version="1.0.0",
    description="Educational local financial-planning simulation using ML, deterministic tools, RAG and an Agent.",
)

# ---------------- Frontend ----------------
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "static"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    def frontend():
        return FileResponse(FRONTEND_DIR / "index.html")


# ---------------- Health ----------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- Data ----------------
@app.get("/cities")
def cities():
    from financial.data_loader import available_cities
    return {"cities": available_cities()}


# ---------------- Salary ML ----------------
@app.post("/salary/predict")
def salary_predict(age: int, city: str, education: str, job_role: str):
    try:
        return predict_salary_tool(age, city, education, job_role)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------- Financial Plan ----------------
@app.post("/plan")
def plan(request: PlanRequest):
    try:
        # The user's entered salary is the PRIMARY source of income
        # for every financial calculation. ML salary prediction is
        # intentionally not used to calculate the plan.
        salary_used = request.monthly_salary

        result = build_plan(
            city=request.city,
            monthly_salary=salary_used,
            marriage_years=request.marriage_years,
            car_years=request.car_years,
            home_years=request.home_years,
            saving_percent=request.saving_percent,
            area_type=request.area_type,
            predicted_salary=None,
        )

        # Optional ML estimate for comparison only. It does NOT affect
        # available capacity, goal investments, or feasibility.
        try:
            salary_result = predict_salary_tool(
                request.age,
                request.city,
                request.education,
                request.job_role,
            )
        except Exception:
            salary_result = None

        result["salary_source"] = "user_entered"
        result["entered_monthly_salary"] = round(salary_used, 2)
        result["salary_prediction"] = salary_result
        result["recommendations"] = build_recommendations(result)

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------- Agent ----------------
@app.post("/agent/plan")
def agent_plan(request: AgentRequest):
    try:
        return FinancialAgent().plan_from_message(request.message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------- RAG ----------------
@app.post("/rag/query")
def rag_query(request: RAGQuestion):
    results = retrieve(request.question, k=3)

    if not results:
        return {
            "answer": "This information is unavailable in the project knowledge base.",
            "sources": [],
        }

    return {
        "answer": "\n\n".join(r["text"] for r in results),
        "sources": [
            {
                "source": r["source"],
                "score": round(r["score"], 4),
            }
            for r in results
        ],
    }
