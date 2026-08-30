def investment_category_for_horizon(years: int) -> str:
    if years <= 3:
        return "Short-term / lower-volatility / capital-preservation-oriented category"
    if years <= 7:
        return "Medium-term / diversified balanced category"
    return "Long-term / diversified growth-oriented category"


def build_recommendations(plan: dict) -> dict:
    recs = {}
    for key, goal in plan["goals"].items():
        recs[key] = {
            "goal": goal["goal"],
            "timeline_years": goal["years"],
            "broad_category": investment_category_for_horizon(goal["years"]),
            "note": "Educational category guidance only; no individual security or guaranteed return is recommended.",
        }

    if plan["shortfall"] > 0:
        recs["gap_actions"] = [
            "Increase the saving percentage if affordable.",
            "Increase the goal timeline to reduce the monthly requirement.",
            "Adjust the goal amount or scope if appropriate.",
        ]
    else:
        recs["gap_actions"] = [
            "Keep the selected saving percentage consistent.",
            "Review the plan periodically as income and goal costs change.",
        ]
    return recs
