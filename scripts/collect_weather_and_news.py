import os
import json
import requests
import pandas as pd
import xml.etree.ElementTree as ET

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# 1. Fetch & Save Open-Meteo Historical Hourly Weather (JSON -> CSV)
print("Fetching Open-Meteo hourly weather (Nov 1, 2025 - Nov 15, 2026)...")
weather_url = "https://archive-api.open-meteo.com/v1/archive"
weather_params = {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "start_date": "2025-11-01",
    "end_date": "2026-11-15",
    "hourly": "temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m",
    "timezone": "Asia/Kolkata"
}

w_res = requests.get(weather_url, params=weather_params)
w_res.raise_for_status()
w_json = w_res.json()

# Save raw JSON (proof of raw API collection)
with open("data/raw/open_meteo_bengaluru_raw.json", "w", encoding="utf-8") as f:
    json.dump(w_json, f, indent=2)

# Flatten JSON 'hourly' object into a tabular DataFrame
df_weather = pd.DataFrame(w_json["hourly"])
df_weather.to_csv("data/raw/weather_hourly_raw.csv", index=False)
print(f"-> Saved weather_hourly_raw.csv ({len(df_weather)} rows, {df_weather.shape[1]} columns)")

# 2. Fetch & Flatten Google News RSS Feeds (Unstructured Text Source)
print("\nFetching Google News RSS feeds for Bengaluru traffic, rain, metro & KSRTC...")
queries = [
    "Bengaluru traffic rain",
    "Bengaluru KSRTC long weekend rush",
    "Namma Metro rush hour parking",
    "Bengaluru air pollution PM2.5"
]

articles = []
for q in queries:
    rss_url = f"https://news.google.com/rss/search?q={requests.utils.quote(q)}&hl=en-IN&gl=IN&ceid=IN:en"
    r = requests.get(rss_url)
    if r.status_code == 200:
        root = ET.fromstring(r.content)
        for item in root.findall(".//item"):
            articles.append({
                "search_topic": q,
                "title": item.findtext("title"),
                "pub_date": item.findtext("pubDate"),
                "source": item.findtext("source"),
                "link": item.findtext("link")
            })

df_news = pd.DataFrame(articles).drop_duplicates(subset=["title"])
df_news.to_csv("data/processed/bengaluru_commute_news.csv", index=False)
print(f"-> Saved bengaluru_commute_news.csv ({len(df_news)} unique articles)")