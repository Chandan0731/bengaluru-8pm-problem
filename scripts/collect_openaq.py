import os
import time
import json
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAQ_API_KEY")
HEADERS = {"X-API-Key": API_KEY}

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# 1. Fetch active Bengaluru stations and save stations_metadata.csv
print("Step 1: Fetching Bengaluru station metadata...")
loc_url = "https://api.openaq.org/v3/locations"
loc_params = {"coordinates": "12.9716,77.5946", "radius": 25000, "limit": 50}
loc_res = requests.get(loc_url, headers=HEADERS, params=loc_params)
loc_res.raise_for_status()
locations = loc_res.json().get("results", [])

# Focus on the 10 major CPCB/KSPCB stations active in 2026
target_station_ids = {5548, 5574, 5607, 5644, 6973, 6974, 6975, 6983, 6984, 3409388}
stations_rows = []
sensors_to_pull = []

for loc in locations:
    if loc["id"] in target_station_ids:
        coords = loc.get("coordinates") or {}
        stations_rows.append({
            "station_id": loc["id"],
            "station_name": loc["name"],
            "latitude": coords.get("latitude"),
            "longitude": coords.get("longitude"),
            "provider": (loc.get("provider") or {}).get("name"),
            "timezone": loc.get("timezone")
        })
        for s in loc.get("sensors", []):
            p_name = s["parameter"]["name"]
            p_units = s["parameter"]["units"]
            if p_name in ["pm25", "pm10", "no2", "co"]:
                sensors_to_pull.append({
                    "station_id": loc["id"],
                    "station_name": loc["name"],
                    "sensor_id": s["id"],
                    "parameter": p_name,
                    "units": p_units
                })

df_stations = pd.DataFrame(stations_rows)
df_stations.to_csv("data/processed/stations_metadata.csv", index=False)
print(f"-> Saved stations_metadata.csv ({len(df_stations)} stations)")
print(f"-> Found {len(sensors_to_pull)} target sensors to download.\n")

# 2. Pull hourly readings from Nov 1, 2025 to Nov 15, 2026
all_readings = []
saved_sample_json = False

for idx, s in enumerate(sensors_to_pull, start=1):
    sensor_id = s["sensor_id"]
    print(f"[{idx}/{len(sensors_to_pull)}] Pulling {s['station_name']} | {s['parameter']} ({s['units']}) [Sensor {sensor_id}]...")
    page = 1
    sensor_count = 0

    while True:
        hours_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"
        params = {
            "datetime_from": "2025-11-01T00:00:00Z",
            "datetime_to": "2026-11-16T00:00:00Z",
            "limit": 1000,
            "page": page
        }
        res = requests.get(hours_url, headers=HEADERS, params=params)

        if res.status_code == 429:
            print("   Rate limit hit (429). Sleeping 10 seconds...")
            time.sleep(10)
            continue
        elif res.status_code != 200:
            print(f"   Warning: Status {res.status_code} on page {page}. Skipping.")
            break

        payload = res.json()
        if not saved_sample_json and payload.get("results"):
            with open("data/raw/openaq_sample_raw.json", "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            saved_sample_json = True

        results = payload.get("results", [])
        if not results:
            break

        for row in results:
            period = row.get("period") or {}
            dt_from = period.get("datetimeFrom") or {}
            cov = row.get("coverage") or {}
            all_readings.append({
                "station_id": s["station_id"],
                "sensor_id": sensor_id,
                "parameter": s["parameter"],
                "units": s["units"],
                "datetime_utc": dt_from.get("utc"),
                "datetime_local": dt_from.get("local"),
                "value": row.get("value"),
                "percent_coverage": cov.get("percentCoverage")
            })

        sensor_count += len(results)
        if len(results) < 1000:
            break
        page += 1
        time.sleep(0.5)

    print(f"   -> Collected {sensor_count} hourly rows.")
    time.sleep(0.5)

df_readings = pd.DataFrame(all_readings)
output_csv = "data/raw/openaq_bengaluru_hourly_raw.csv"
df_readings.to_csv(output_csv, index=False)
file_mb = os.path.getsize(output_csv) / (1024 * 1024)

print("\n==========================================")
print(f"DONE! Total rows collected: {len(df_readings):,}")
print(f"Saved to: {output_csv} ({file_mb:.2f} MB)")
print("==========================================")