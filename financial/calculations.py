from config import INFLATION_RATE, EXPECTED_ANNUAL_RETURN

def validate_years(years: int) -> int:
    if isinstance(years, bool) or not isinstance(years, int):
        raise ValueError("Goal years must be an integer.")
    if years < 1 or years > 50:
        raise ValueError("Goal years must be between 1 and 50.")
    return years

def validate_saving_percent(percent: float) -> float:
    try:
        value = float(percent)
    except (TypeError, ValueError):
        raise ValueError("Saving percentage must be numeric.")
    if not 0 <= value <= 100:
        raise ValueError("Saving percentage must be between 0 and 100.")
    return value

def future_cost(current_cost: float, years: int, inflation_rate: float = INFLATION_RATE) -> float:
    validate_years(years)
    if current_cost < 0:
        raise ValueError("Current cost cannot be negative.")
    return current_cost * ((1 + inflation_rate) ** years)

def monthly_investment_for_goal(
    future_value: float,
    years: int,
    annual_return: float = EXPECTED_ANNUAL_RETURN
) -> float:
    validate_years(years)
    if future_value < 0:
        raise ValueError("Future value cannot be negative.")
    if annual_return < 0:
        raise ValueError("Expected annual return cannot be negative.")
    n = years * 12
    monthly_rate = (1 + annual_return) ** (1 / 12) - 1
    if monthly_rate == 0:
        return future_value / n
    return future_value * monthly_rate / (((1 + monthly_rate) ** n) - 1)

def available_monthly_capacity(monthly_salary: float, saving_percent: float) -> float:
    if monthly_salary <= 0:
        raise ValueError("Monthly salary must be greater than zero.")
    percent = validate_saving_percent(saving_percent)
    return monthly_salary * percent / 100

def classify_feasibility(available: float, required: float) -> str:
    if required <= available:
        return "Achievable"
    ratio = required / max(available, 1e-9)
    if ratio <= 1.5:
        return "Challenging"
    return "Highly Challenging"

def goal_status(available: float, required: float) -> str:
    return classify_feasibility(available, required)
