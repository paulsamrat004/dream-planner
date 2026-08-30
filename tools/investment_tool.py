from financial.calculations import monthly_investment_for_goal

def investment_calculator_tool(future_value: float, years: int) -> dict:
    monthly = monthly_investment_for_goal(future_value, years)
    return {
        "future_value": round(future_value, 2),
        "years": years,
        "monthly_investment_required": round(monthly, 2),
    }
