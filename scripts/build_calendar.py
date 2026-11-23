import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

# Generate all dates from Nov 1, 2025 to Nov 15, 2026
dates = pd.date_range(start="2025-11-01", end="2026-11-15", freq="D")
df = pd.DataFrame({"cal_date": dates})
df["day_of_week"] = df["cal_date"].dt.day_name()
df["weekday_num"] = df["cal_date"].dt.weekday  # 0=Mon, 6=Sun
df["is_weekend"] = df["weekday_num"].isin([5, 6]).astype(int)

# Official Karnataka Government Public Holidays (Nov 2025 - Nov 2026)
holidays = {
    "2025-11-01": "Kannada Rajyotsava",
    "2025-12-25": "Christmas",
    "2026-01-15": "Makara Sankranti",
    "2026-01-26": "Republic Day",
    "2026-03-19": "Ugadi",
    "2026-03-21": "Khutub-E-Ramzan",
    "2026-03-31": "Mahaveera Jayanthi",
    "2026-04-03": "Good Friday",
    "2026-04-14": "Dr. B.R. Ambedkar Jayanti",
    "2026-04-20": "Basava Jayanthi / Akshaya Tritiya",
    "2026-05-01": "May Day",
    "2026-05-28": "Bakrid",
    "2026-06-26": "Last Day of Muharram",
    "2026-08-15": "Independence Day",
    "2026-08-26": "Eid-Milad",
    "2026-09-14": "Ganesh Chaturthi",
    "2026-10-02": "Gandhi Jayanti",
    "2026-10-20": "Mahanavami / Ayudha Puja",
    "2026-10-21": "Vijayadashami (Dasara)",
    "2026-11-08": "Naraka Chaturdashi (Deepavali)",
    "2026-11-10": "Balipadyami (Deepavali)",
}

df["date_str"] = df["cal_date"].dt.strftime("%Y-%m-%d")
df["festival_name"] = df["date_str"].map(holidays).fillna("None")
df["is_public_holiday"] = (df["festival_name"] != "None").astype(int)
df["is_off_day"] = ((df["is_weekend"] == 1) | (df["is_public_holiday"] == 1)).astype(int)

# Identify contiguous blocks of 3+ off days (Long Weekends / Festival Breaks)
block_id = (df["is_off_day"] != df["is_off_day"].shift()).cumsum()
block_sizes = df.groupby(block_id)["is_off_day"].transform("sum")
df["is_long_weekend"] = ((df["is_off_day"] == 1) & (block_sizes >= 3)).astype(int)

# Exodus Evening: Working day immediately before a Long Weekend OR before a major festival
next_day_long_wknd = df["is_long_weekend"].shift(-1).fillna(0) == 1
next_day_holiday = df["is_public_holiday"].shift(-1).fillna(0) == 1
df["is_exodus_evening"] = ((df["is_off_day"] == 0) & (next_day_long_wknd | next_day_holiday)).astype(int)

# Clean final columns
final_cols = [
    "date_str", "day_of_week", "weekday_num", "is_weekend",
    "is_public_holiday", "festival_name", "is_long_weekend", "is_exodus_evening"
]
df_out = df[final_cols].rename(columns={"date_str": "cal_date"})

output_path = "data/processed/bengaluru_calendar.csv"
df_out.to_csv(output_path, index=False)

print(f"Saved {len(df_out)} calendar days to {output_path}")
print("\n=== IDENTIFIED EXODUS EVENINGS (Pre-Holiday / Pre-Long-Weekend Rush) ===")
print(df_out[df_out["is_exodus_evening"] == 1][["cal_date", "day_of_week", "is_exodus_evening"]])