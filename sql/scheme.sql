CREATE DATABASE IF NOT EXISTS bengaluru_8pm_db;
USE bengaluru_8pm_db;

-- Drop in reverse dependency order for clean reruns
DROP TABLE IF EXISTS readings;
DROP TABLE IF EXISTS weather_hourly;
DROP TABLE IF EXISTS calendar;
DROP TABLE IF EXISTS stations;

-- 1. Dimension Table: Air Quality Monitoring Stations
CREATE TABLE stations (
    station_id INT PRIMARY KEY,
    station_name VARCHAR(150) NOT NULL,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    provider VARCHAR(100),
    timezone VARCHAR(50)
);

-- 2. Dimension Table: Bengaluru Holiday & Exodus Calendar
CREATE TABLE calendar (
    cal_date DATE PRIMARY KEY,
    day_of_week VARCHAR(15) NOT NULL,
    weekday_num TINYINT NOT NULL,
    is_weekend TINYINT(1) NOT NULL,
    is_public_holiday TINYINT(1) NOT NULL,
    festival_name VARCHAR(100),
    is_long_weekend TINYINT(1) NOT NULL,
    is_exodus_evening TINYINT(1) NOT NULL
);

-- 3. Time-Series Fact Table: Hourly Weather (Open-Meteo)
CREATE TABLE weather_hourly (
    weather_ts DATETIME PRIMARY KEY,
    cal_date DATE NOT NULL,
    temperature_2m DECIMAL(5, 2),
    relative_humidity_2m DECIMAL(5, 2),
    precipitation DECIMAL(6, 2),
    rain DECIMAL(6, 2),
    wind_speed_10m DECIMAL(6, 2),
    CONSTRAINT fk_weather_cal FOREIGN KEY (cal_date) REFERENCES calendar(cal_date)
);

-- 4. High-Frequency Fact Table: Hourly Air Quality Sensor Readings (OpenAQ)
CREATE TABLE readings (
    reading_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    sensor_id INT NOT NULL,
    parameter VARCHAR(20) NOT NULL,
    units VARCHAR(20),
    datetime_utc DATETIME,
    weather_ts DATETIME NOT NULL,
    value DOUBLE,
    percent_coverage DECIMAL(5, 2),
    INDEX idx_station_param (station_id, parameter),
    INDEX idx_weather_ts (weather_ts),
    CONSTRAINT fk_readings_station FOREIGN KEY (station_id) REFERENCES stations(station_id),
    CONSTRAINT fk_readings_weather FOREIGN KEY (weather_ts) REFERENCES weather_hourly(weather_ts)
);