import re
from financial.data_loader import available_cities

def _find_city(text):
    for city in available_cities():
        if re.search(rf"\b{re.escape(city)}\b", text, re.I):
            return city
    return None

def _find_first(patterns, text, cast=float):
    for pattern in patterns:
        m = re.search(pattern, text, re.I)
        if m:
            try:
                return cast(m.group(1))
            except ValueError:
                return None
    return None

def parse_user_message(text: str) -> dict:
    # This parser is deterministic and exists as a local fallback to an LLM.
    data = {}
    data["city"] = _find_city(text)

    data["age"] = _find_first([
        r"\b(?:age|aged)\s*(?:is|:)?\s*(\d{1,3})\b",
        r"\b(?:i\s*am|i\'m)\s*(\d{1,3})\s*(?:years?\s*old)?\b"
    ], text, int)
    data["saving_percent"] = _find_first([
        r"(?:save|saving|invest)\s*(?:about\s*)?(\d+(?:\.\d+)?)\s*%",
        r"(\d+(?:\.\d+)?)\s*%\s*(?:of\s+my\s+salary\s+)?(?:to\s+save|saving)"
    ], text, float)

    data["marriage_years"] = _find_first([
        r"marri\w*.*?(?:after|in)\s+(\d+)\s+years?",
        r"marry.*?(\d+)\s+years?"
    ], text, int)
    data["car_years"] = _find_first([
        r"(?:buy|purchase).*?car.*?(?:after|in)\s+(\d+)\s+years?",
        r"car.*?(?:after|in)\s+(\d+)\s+years?"
    ], text, int)
    data["home_years"] = _find_first([
        r"(?:buy|purchase).*?home.*?(?:after|in)\s+(\d+)\s+years?",
        r"home.*?(?:after|in)\s+(\d+)\s+years?"
    ], text, int)

    # Education and role are matched against the dataset vocabularies.
    educations = ["B.E.", "B.Sc", "B.Tech", "BCA", "M.Sc", "M.Tech", "MBA", "MCA"]
    roles = [
        "Business Analyst", "Data Analyst", "Data Scientist", "DevOps Engineer",
        "Project Coordinator", "QA Engineer", "Software Engineer",
        "Technical Support Engineer", "UI UX Designer", "Web Developer"
    ]
    for value in educations:
        if re.search(re.escape(value), text, re.I):
            data["education"] = value
            break
    for value in roles:
        if re.search(re.escape(value), text, re.I):
            data["job_role"] = value
            break

    salary = _find_first([
        r"(?:earn|salary|income|make)\s*(?:is|of|:)?\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",
        r"(?:₹|rs\.?|inr)\s*([\d,]+)\s*(?:per\s+month|monthly)?"
    ], text, float)
    if salary is not None:
        data["monthly_salary"] = salary

    return data
