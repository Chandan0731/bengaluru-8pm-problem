import os
import numpy as np
import pandas as pd

df = pd.read_csv("data/processed/bengaluru_8pm_clean.csv")
pm25 = df[df["parameter"] == "pm25"].copy()

pm25["short_station"] = (
    pm25["station_name"]
    .str.replace(", Bengaluru - CPCB", "", regex=False)
    .str.replace(", Bengaluru - KSPCB", "", regex=False)
)

pm25["day_regime"] = np.where(
    pm25["is_weekend"] == 1, "Weekend (Sat-Sun)",
    np.where(pm25["weekday_num"].isin([1, 2, 3]), "Core Office (Tue-Thu)", "Hybrid Edge (Mon & Fri)")
)

pm25["weather_regime"] = np.where(pm25["rain"] == 0, "Dry Evening (0 mm)", "Rainy Evening (> 0 mm)")
pm25["calendar_regime"] = np.where(pm25["is_exodus_evening"] == 1, "Pre-Holiday / Exodus", "Regular Day")

summary = (
    pm25.groupby(["short_station", "hour_ist", "day_regime", "weather_regime", "calendar_regime"], as_index=False)
    .agg(
        mean_pm25=("value", "mean"),
        median_pm25=("value", "median"),
        mean_wind=("wind_speed_10m", "mean"),
        sample_count=("value", "count")
    )
)

os.makedirs("data/processed", exist_ok=True)
summary.to_csv("data/processed/dashboard_summary.csv", index=False)
print(f"Saved data/processed/dashboard_summary.csv ({len(summary):,} rows, {os.path.getsize('data/processed/dashboard_summary.csv')/1024:.1f} KB)")