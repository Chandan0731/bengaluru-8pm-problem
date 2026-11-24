import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)

conn = mysql.connector.connect(
    host="localhost",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database="bengaluru_8pm_db"
)
cursor = conn.cursor()

# 1. Load stations
df_stations = pd.read_csv("data/processed/stations_metadata.csv")
station_sql = """
INSERT INTO stations (station_id, station_name, latitude, longitude, provider, timezone)
VALUES (%s, %s, %s, %s, %s, %s)
"""
cursor.executemany(station_sql, df_stations.where(pd.notnull(df_stations), None).values.tolist())
conn.commit()
print(f"Loaded {cursor.rowcount} rows into stations.")

# 2. Load calendar
df_cal = pd.read_csv("data/processed/bengaluru_calendar.csv")
cal_sql = """
INSERT INTO calendar (cal_date, day_of_week, weekday_num, is_weekend, is_public_holiday, festival_name, is_long_weekend, is_exodus_evening)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(cal_sql, df_cal.values.tolist())
conn.commit()
print(f"Loaded {cursor.rowcount} rows into calendar.")

# 3. Load weather_hourly
df_w = pd.read_csv("data/raw/weather_hourly_raw.csv")
df_w["weather_ts"] = pd.to_datetime(df_w["time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
df_w["cal_date"] = pd.to_datetime(df_w["time"]).dt.strftime("%Y-%m-%d")
w_cols = ["weather_ts", "cal_date", "temperature_2m", "relative_humidity_2m", "precipitation", "rain", "wind_speed_10m"]
w_sql = """
INSERT INTO weather_hourly (weather_ts, cal_date, temperature_2m, relative_humidity_2m, precipitation, rain, wind_speed_10m)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(w_sql, df_w[w_cols].where(pd.notnull(df_w[w_cols]), None).values.tolist())
conn.commit()
print(f"Loaded {cursor.rowcount} rows into weather_hourly.")

# 4. Load readings in chunks of 10,000 rows
df_r = pd.read_csv("data/raw/openaq_bengaluru_hourly_raw.csv")
df_r["datetime_utc_clean"] = pd.to_datetime(df_r["datetime_utc"]).dt.tz_localize(None).dt.strftime("%Y-%m-%d %H:%M:%S")
df_r["weather_ts"] = pd.to_datetime(df_r["datetime_local"]).dt.tz_localize(None).dt.floor("h").dt.strftime("%Y-%m-%d %H:%M:%S")

valid_ts = set(df_w["weather_ts"])
df_r = df_r[df_r["weather_ts"].isin(valid_ts)].copy()

r_cols = ["station_id", "sensor_id", "parameter", "units", "datetime_utc_clean", "weather_ts", "value", "percent_coverage"]
r_sql = """
INSERT INTO readings (station_id, sensor_id, parameter, units, datetime_utc, weather_ts, value, percent_coverage)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

records = df_r[r_cols].where(pd.notnull(df_r[r_cols]), None).values.tolist()
batch_size = 10000
total_inserted = 0
for i in range(0, len(records), batch_size):
    cursor.executemany(r_sql, records[i:i+batch_size])
    conn.commit()
    total_inserted += len(records[i:i+batch_size])
    print(f"   Inserted {total_inserted:,} / {len(records):,} readings...")

cursor.close()
conn.close()
print("All 4 tables loaded into MySQL successfully!")