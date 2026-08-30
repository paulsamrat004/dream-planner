from financial.data_loader import get_city_costs
from financial.calculations import future_cost

def future_cost_tool(city: str, goal: str, years: int, area_type=None) -> dict:
    goal = goal.lower().strip()
    if goal not in {"marriage", "car", "home"}:
        raise ValueError("Goal must be marriage, car, or home.")
    costs = get_city_costs(city, area_type)
    current = costs[goal]
    future = future_cost(current, years)
    return {
        "city": costs["city"],
        "area_type": costs["area_type"],
        "goal": goal,
        "years": years,
        "current_cost": round(current, 2),
        "future_cost": round(future, 2),
    }
