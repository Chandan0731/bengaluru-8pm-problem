import requests
import pandas as pd

# Test 1: Open-Meteo Historical Weather API (JSON) for Bengaluru
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "start_date": "2025-11-01",
    "end_date": "2026-11-15",
    "hourly": "temperature_2m,precipitation,rain,wind_speed_10m",
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params)
print("Open-Meteo Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    df_weather = pd.DataFrame(data["hourly"])
    print("Rows fetched:", len(df_weather))
    print(df_weather.head(3))
    print(df_weather.tail(3))
else:
    print("Error:", response.text)