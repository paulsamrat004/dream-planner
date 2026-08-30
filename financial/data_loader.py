import pandas as pd
from config import CITY_COST_FILE

def load_city_costs(path=CITY_COST_FILE) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "City", "Area_Type",
        "Marriage_Cost_Current", "Car_Cost_Current", "Home_Cost_Current"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"city_goal_costs.csv missing columns: {sorted(missing)}")
    df["City"] = df["City"].astype(str).str.strip()
    df["Area_Type"] = df["Area_Type"].astype(str).str.strip()
    return df

def available_cities(path=CITY_COST_FILE):
    return sorted(load_city_costs(path)["City"].unique().tolist())

def get_city_costs(city: str, area_type: str | None = None, path=CITY_COST_FILE) -> dict:
    df = load_city_costs(path)
    city_norm = city.strip().casefold()
    rows = df[df["City"].str.casefold() == city_norm]
    if rows.empty:
        raise ValueError(f"Unknown city: {city}. Available cities: {available_cities(path)}")
    if area_type:
        rows2 = rows[rows["Area_Type"].str.casefold() == area_type.strip().casefold()]
        if rows2.empty:
            raise ValueError(f"Unknown area type '{area_type}' for {city}.")
        row = rows2.iloc[0]
    else:
        # Use the first row consistently when no area is supplied.
        row = rows.iloc[0]
    return {
        "city": str(row["City"]),
        "area_type": str(row["Area_Type"]),
        "marriage": float(row["Marriage_Cost_Current"]),
        "car": float(row["Car_Cost_Current"]),
        "home": float(row["Home_Cost_Current"]),
    }
