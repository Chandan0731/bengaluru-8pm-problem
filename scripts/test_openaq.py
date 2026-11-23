import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAQ_API_KEY")
headers = {"X-API-Key": API_KEY}

url = "https://api.openaq.org/v3/locations"
params = {
    "coordinates": "12.9716,77.5946",
    "radius": 25000,
    "limit": 50
}

response = requests.get(url, headers=headers, params=params)
locations = response.json().get("results", [])

active_sensors = []
print("=== ACTIVE 2026 BENGALURU STATIONS & TARGET SENSORS ===")

for loc in locations:
    # Safely handle stations where datetimeLast is None
    last_dt = (loc.get("datetimeLast") or {}).get("local", "")
    if last_dt and last_dt.startswith("2026"):
        print(f"\nStation ID: {loc['id']} | {loc['name']} | Last: {last_dt}")
        for s in loc.get("sensors", []):
            p_name = s["parameter"]["name"]
            if p_name in ["pm25", "pm10", "no2", "co"]:
                print(f"   -> Sensor ID: {s['id']} | Parameter: {p_name} ({s['parameter']['units']})")
                active_sensors.append((loc["id"], loc["name"], s["id"], p_name))

print(f"\nTotal active target sensors found: {len(active_sensors)}")

# Test pulling 48 hours of hourly data from the first active pm25 sensor
pm25_sensors = [s for s in active_sensors if s[3] == "pm25"]
if pm25_sensors:
    st_id, st_name, sensor_id, param = pm25_sensors[0]
    print(f"\nTesting hourly endpoint for {st_name} (Sensor {sensor_id} - {param})...")
    hours_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"
    h_params = {
        "datetime_from": "2026-10-01T00:00:00Z",
        "datetime_to": "2026-10-03T00:00:00Z",
        "limit": 100
    }
    h_res = requests.get(hours_url, headers=headers, params=h_params)
    print("Hourly Endpoint Status:", h_res.status_code)
    if h_res.status_code == 200:
        results = h_res.json().get("results", [])
        print(f"Sample rows returned: {len(results)}")
        if results:
            print("Sample row:", results[0])
    else:
        print("Error:", h_res.text)