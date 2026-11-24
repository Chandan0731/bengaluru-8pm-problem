USE bengaluru_8pm_db;

-- Query 1: Hourly Diurnal Curve (Hybrid Core Tue-Thu vs Mon/Fri vs Weekends) for PM2.5 and NO2
SELECT 
    CASE 
        WHEN c.is_weekend = 1 THEN 'Weekend (Sat-Sun)'
        WHEN c.weekday_num IN (1, 2, 3) THEN 'Core Office Days (Tue-Thu)'
        ELSE 'Hybrid Edge Days (Mon & Fri)'
    END AS day_category,
    HOUR(r.weather_ts) AS hour_of_day,
    r.parameter,
    COUNT(*) AS sample_count,
    ROUND(AVG(r.value), 2) AS avg_concentration,
    ROUND(STDDEV(r.value), 2) AS std_concentration
FROM readings r
JOIN calendar c ON DATE(r.weather_ts) = c.cal_date
WHERE r.parameter IN ('pm25', 'no2')
  AND r.value IS NOT NULL AND r.value > 0
GROUP BY day_category, hour_of_day, r.parameter
ORDER BY r.parameter, day_category, hour_of_day;

-- Query 2: Evening Rush Window (17:00 - 23:00) Surge by Station (Corridor Hotspots)
SELECT 
    s.station_id,
    s.station_name,
    ROUND(AVG(CASE WHEN HOUR(r.weather_ts) BETWEEN 12 AND 15 THEN r.value END), 2) AS afternoon_baseline_pm25,
    ROUND(AVG(CASE WHEN HOUR(r.weather_ts) BETWEEN 18 AND 22 THEN r.value END), 2) AS evening_peak_pm25,
    ROUND(
        AVG(CASE WHEN HOUR(r.weather_ts) BETWEEN 18 AND 22 THEN r.value END) -
        AVG(CASE WHEN HOUR(r.weather_ts) BETWEEN 12 AND 15 THEN r.value END), 
    2) AS evening_surge_delta
FROM readings r
JOIN stations s ON r.station_id = s.station_id
WHERE r.parameter = 'pm25'
  AND r.value IS NOT NULL AND r.value > 0
GROUP BY s.station_id, s.station_name
ORDER BY evening_surge_delta DESC;

-- Query 3: Rain Washout Effect on the 6 PM - 11 PM Pollution Curve
SELECT 
    CASE 
        WHEN w.rain = 0 THEN 'Dry Hour (0 mm)'
        WHEN w.rain > 0 AND w.rain <= 2.5 THEN 'Light Rain (0.1 - 2.5 mm)'
        ELSE 'Moderate/Heavy Rain (> 2.5 mm)'
    END AS rain_intensity,
    HOUR(r.weather_ts) AS hour_of_day,
    COUNT(*) AS observations,
    ROUND(AVG(r.value), 2) AS avg_pm25,
    ROUND(AVG(w.wind_speed_10m), 2) AS avg_wind_kmh
FROM readings r
JOIN weather_hourly w ON r.weather_ts = w.weather_ts
WHERE r.parameter = 'pm25'
  AND HOUR(r.weather_ts) BETWEEN 17 AND 23
  AND r.value IS NOT NULL AND r.value > 0
GROUP BY rain_intensity, hour_of_day
ORDER BY hour_of_day, rain_intensity;

-- Query 4: Pre-Long-Weekend & Festival Exodus Evening Amplification (17:00 - 23:00)
SELECT 
    CASE 
        WHEN c.is_exodus_evening = 1 THEN 'Exodus Evening (Pre-Long-Weekend/Festival)'
        WHEN c.is_public_holiday = 1 THEN 'Public Holiday / Festival Day'
        WHEN c.is_weekend = 1 THEN 'Regular Weekend'
        ELSE 'Regular Working Weekday'
    END AS calendar_regime,
    r.parameter,
    COUNT(DISTINCT c.cal_date) AS num_days,
    ROUND(AVG(r.value), 2) AS evening_avg_concentration,
    ROUND(MAX(r.value), 2) AS peak_hourly_reading
FROM readings r
JOIN calendar c ON DATE(r.weather_ts) = c.cal_date
WHERE r.parameter IN ('pm25', 'pm10', 'no2', 'co')
  AND HOUR(r.weather_ts) BETWEEN 17 AND 23
  AND r.value IS NOT NULL AND r.value > 0
GROUP BY calendar_regime, r.parameter
ORDER BY r.parameter, evening_avg_concentration DESC;

-- Query 5: Top 10 Worst 8 PM (20:00 IST) Citywide Pollution Episodes with Weather & Festival Context
SELECT 
    r.weather_ts AS timestamp_ist,
    c.day_of_week,
    COALESCE(NULLIF(c.festival_name, ''), 'None') AS festival,
    c.is_exodus_evening,
    ROUND(AVG(r.value), 2) AS citywide_avg_pm25,
    MAX(w.rain) AS rain_mm,
    MAX(w.wind_speed_10m) AS wind_speed_kmh,
    MAX(w.relative_humidity_2m) AS humidity_pct
FROM readings r
JOIN weather_hourly w ON r.weather_ts = w.weather_ts
JOIN calendar c ON w.cal_date = c.cal_date
WHERE r.parameter = 'pm25'
  AND HOUR(r.weather_ts) = 20
  AND r.value IS NOT NULL AND r.value > 0
GROUP BY r.weather_ts, c.day_of_week, festival, c.is_exodus_evening
ORDER BY citywide_avg_pm25 DESC
LIMIT 10;