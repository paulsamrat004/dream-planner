from financial.recommendations import build_recommendations

def recommendation_plan_tool(plan: dict) -> dict:
    return build_recommendations(plan)
