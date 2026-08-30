from financial.calculations import available_monthly_capacity, classify_feasibility

def feasibility_checker_tool(monthly_salary: float, saving_percent: float, required_monthly: float) -> dict:
    available = available_monthly_capacity(monthly_salary, saving_percent)
    difference = available - required_monthly
    return {
        "available_monthly": round(available, 2),
        "required_monthly": round(required_monthly, 2),
        "surplus": round(max(difference, 0), 2),
        "shortfall": round(max(-difference, 0), 2),
        "status": classify_feasibility(available, required_monthly),
    }
