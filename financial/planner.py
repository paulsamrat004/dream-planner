from config import INFLATION_RATE, EXPECTED_ANNUAL_RETURN
from financial.data_loader import get_city_costs
from financial.calculations import available_monthly_capacity, validate_saving_percent
from tools.future_cost_tool import future_cost_tool
from tools.investment_tool import investment_calculator_tool
from tools.feasibility_tool import feasibility_checker_tool
from financial.calculations import goal_status

GOALS = ("marriage", "car", "home")
LABELS = {"marriage": "Marriage", "car": "Car", "home": "Home"}


def build_plan(city, monthly_salary, marriage_years, car_years, home_years,
               saving_percent, area_type=None, predicted_salary=None):
    if monthly_salary <= 0:
        raise ValueError("Monthly salary must be greater than zero.")
    saving_percent = validate_saving_percent(saving_percent)

    # Validate city/area once before invoking goal tools.
    costs = get_city_costs(city, area_type)
    timelines = {
        "marriage": marriage_years,
        "car": car_years,
        "home": home_years,
    }

    goals = {}
    total_required = 0.0

    for goal in GOALS:
        future_result = future_cost_tool(city, goal, timelines[goal], area_type)
        investment_result = investment_calculator_tool(
            future_result["future_cost"], timelines[goal]
        )
        monthly = investment_result["monthly_investment_required"]
        total_required += monthly

        goals[goal] = {
            "goal": LABELS[goal],
            "years": int(timelines[goal]),
            "current_cost": future_result["current_cost"],
            "future_cost": future_result["future_cost"],
            "monthly_investment": monthly,
            "status": goal_status(float(monthly_salary) * saving_percent / 100.0, monthly),
        }

    feasibility = feasibility_checker_tool(
        float(monthly_salary), saving_percent, total_required
    )

    return {
        "city": costs["city"],
        "area_type": costs["area_type"],
        "monthly_salary": round(float(monthly_salary), 2),
        "predicted_salary": round(predicted_salary, 2) if predicted_salary is not None else None,
        "saving_percent": saving_percent,
        "available_monthly_investment": feasibility["available_monthly"],
        "total_required_monthly_investment": round(total_required, 2),
        "surplus": feasibility["surplus"],
        "shortfall": feasibility["shortfall"],
        "feasibility": feasibility["status"],
        "assumptions": {
            "inflation_rate": INFLATION_RATE,
            "expected_annual_return": EXPECTED_ANNUAL_RETURN,
        },
        "goals": goals,
    }
