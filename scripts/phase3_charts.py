import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Clean, modern publication style (no emojis, high contrast)
plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--"
})

os.makedirs("outputs", exist_ok=True)
df = pd.read_csv("data/processed/bengaluru_8pm_clean.csv")
pm25 = df[df["parameter"] == "pm25"].copy()

pm25["day_regime"] = np.where(
    pm25["is_weekend"] == 1, "Weekend (Sat-Sun)",
    np.where(pm25["weekday_num"].isin([1, 2, 3]), "Core Office (Tue-Thu)", "Hybrid Edge (Mon & Fri)")
)

# ==============================================================================
# FIGURE 1: 24-Hour Diurnal Curve by Work-Week Regime
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
palette_f1 = {
    "Core Office (Tue-Thu)": "#1B365D",
    "Hybrid Edge (Mon & Fri)": "#D95F02",
    "Weekend (Sat-Sun)": "#4A90E2"
}

diurnal = pm25.groupby(["day_regime", "hour_ist"])["value"].agg(["mean", "sem"]).reset_index()
for regime in ["Core Office (Tue-Thu)", "Hybrid Edge (Mon & Fri)", "Weekend (Sat-Sun)"]:
    sub = diurnal[diurnal["day_regime"] == regime]
    ax.plot(sub["hour_ist"], sub["mean"], marker="o", markersize=4.5, linewidth=2.2,
            label=regime, color=palette_f1[regime])
    ax.fill_between(sub["hour_ist"], sub["mean"] - 1.96 * sub["sem"], sub["mean"] + 1.96 * sub["sem"],
                    color=palette_f1[regime], alpha=0.12)

ax.axvspan(19, 21, color="#E63946", alpha=0.10, label="8 PM Peak Window (19:00-21:00 IST)")
ax.axvline(20, color="#E63946", linestyle=":", linewidth=1.3)
ax.set_ylim(18, 48)

ax.annotate("8 PM Nocturnal Surge\n(All 7 days converge; p = 0.386)",
            xy=(20, 39.2), xytext=(10.2, 42.5),
            arrowprops=dict(arrowstyle="->", color="#1B365D", lw=1.3, connectionstyle="arc3,rad=-0.12"),
            fontsize=9.5, fontweight="bold", color="#1B365D",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#F8F9FA", edgecolor="#CBD5E1"))

ax.set_title("Bengaluru 24-Hour PM2.5 Profile: The 8 PM Surge Persists Across All Day Regimes",
             fontsize=12.5, fontweight="bold", pad=16, loc="left")
ax.set_xlabel("Hour of Day (IST)", fontsize=10.5, fontweight="bold")
ax.set_ylabel("Mean PM2.5 Concentration (µg/m³)", fontsize=10.5, fontweight="bold")
ax.set_xticks(range(0, 24, 2))
ax.set_xlim(0, 23)
ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9, loc="lower left")
plt.tight_layout()
plt.savefig("outputs/fig1_diurnal_hybrid_curve.png")
plt.close()

# ==============================================================================
# FIGURE 2: Corridor Hotspot Dumbbell Chart (Afternoon vs Evening Peak)
# ==============================================================================
st_aft = pm25[pm25["hour_ist"].between(12, 15)].groupby("station_name")["value"].mean()
st_eve = pm25[pm25["hour_ist"].between(18, 22)].groupby("station_name")["value"].mean()
st_df = pd.DataFrame({"Afternoon (12-15h)": st_aft, "Evening (18-22h)": st_eve}).dropna()
st_df["Delta"] = st_df["Evening (18-22h)"] - st_df["Afternoon (12-15h)"]
st_df = st_df.sort_values("Delta", ascending=True)
st_df["Short_Name"] = st_df.index.str.replace(", Bengaluru - CPCB", "", regex=False).str.replace(", Bengaluru - KSPCB", "", regex=False)

fig, ax = plt.subplots(figsize=(10, 5.2))
y_pos = np.arange(len(st_df))

for idx, (_, row) in enumerate(st_df.iterrows()):
    line_color = "#E63946" if row["Delta"] > 7 else ("#457B9D" if row["Delta"] > 0 else "#6C757D")
    ax.plot([row["Afternoon (12-15h)"], row["Evening (18-22h)"]], [idx, idx],
            color=line_color, linewidth=2.8, zorder=2)
    sign = "+" if row["Delta"] >= 0 else ""
    ax.text(max(row["Afternoon (12-15h)"], row["Evening (18-22h)"]) + 0.7, idx,
            f"{sign}{row['Delta']:.2f} µg/m³", va="center", fontsize=9,
            fontweight="bold" if row["Delta"] > 7 else "normal", color=line_color)

ax.scatter(st_df["Afternoon (12-15h)"], y_pos, color="#64748B", s=75, label="Afternoon Baseline (12:00-15:00)", zorder=3)
ax.scatter(st_df["Evening (18-22h)"], y_pos, color="#1B365D", s=85, label="Evening Rush Peak (18:00-22:00)", zorder=4)

ax.set_yticks(y_pos)
ax.set_yticklabels(st_df["Short_Name"], fontsize=10, fontweight="bold")
ax.set_xlim(18, 55)
ax.set_xlabel("Mean PM2.5 Concentration (µg/m³)", fontsize=10.5, fontweight="bold")
ax.set_title("Corridor Hotspots: Hebbal (+9.39) & Silk Board (+8.99) Drive Evening Surge",
             fontsize=12.5, fontweight="bold", pad=12, loc="left")
ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9.5, loc="lower right")
plt.tight_layout()
plt.savefig("outputs/fig2_corridor_surge_dumbbell.png")
plt.close()

# ==============================================================================
# FIGURE 3: Rain Washout Paradox (17:00 - 23:00 IST)
# ==============================================================================
eve = pm25[pm25["hour_ist"].between(17, 23)].copy()
eve["rain_tier"] = np.where(
    eve["rain"] == 0, "Dry Evening (0 mm)",
    np.where(eve["rain"] <= 2.5, "Light Rain (0.1 - 2.5 mm)", "Moderate/Heavy Rain (> 2.5 mm)")
)
rain_grp = eve.groupby(["rain_tier", "hour_ist"]).agg(
    mean_pm25=("value", "mean"),
    sem_pm25=("value", "sem"),
    n=("value", "count")
).reset_index()
rain_grp = rain_grp[rain_grp["n"] >= 15]  # Show well-sampled hours only

fig, ax = plt.subplots(figsize=(9.5, 5))
palette_f3 = {
    "Dry Evening (0 mm)": "#D62828",
    "Light Rain (0.1 - 2.5 mm)": "#2A9D8F",
    "Moderate/Heavy Rain (> 2.5 mm)": "#1D3557"
}

for tier in ["Dry Evening (0 mm)", "Light Rain (0.1 - 2.5 mm)", "Moderate/Heavy Rain (> 2.5 mm)"]:
    sub = rain_grp[rain_grp["rain_tier"] == tier]
    ax.plot(sub["hour_ist"], sub["mean_pm25"], marker="s", markersize=5.5, linewidth=2.4,
            label=tier, color=palette_f3[tier])
    ax.fill_between(sub["hour_ist"], sub["mean_pm25"] - 1.96 * sub["sem_pm25"],
                    sub["mean_pm25"] + 1.96 * sub["sem_pm25"], color=palette_f3[tier], alpha=0.12)

ax.annotate("8 PM Washout Drop: -51.2%\n(39.92 vs. 19.50 µg/m³; p = 3.8e-193)",
            xy=(20, 19.5), xytext=(20.3, 28.5),
            arrowprops=dict(arrowstyle="->", color="#2A9D8F", lw=1.4),
            fontsize=9.5, fontweight="bold", color="#1D3557",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#F8F9FA", edgecolor="#CBD5E1"))

ax.set_title("The Rain Washout Paradox: Wet Scavenging Cuts 8 PM PM2.5 in Half",
             fontsize=12.5, fontweight="bold", pad=12, loc="left")
ax.set_xlabel("Evening Hour (IST)", fontsize=10.5, fontweight="bold")
ax.set_ylabel("Mean PM2.5 Concentration (µg/m³)", fontsize=10.5, fontweight="bold")
ax.set_xticks(range(17, 24))
ax.set_xticklabels([f"{h}:00" for h in range(17, 24)])
ax.set_ylim(10, 45)
ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9.5, loc="upper left")
plt.tight_layout()
plt.savefig("outputs/fig3_rain_washout_paradox.png")
plt.close()

# ==============================================================================
# FIGURE 4: Exodus Evening vs Regular Weekday Evening (18:00 - 22:00 IST)
# ==============================================================================
wd_eve = pm25[(pm25["hour_ist"].between(18, 22)) & (pm25["is_weekend"] == 0)].copy()
wd_eve["Regime"] = np.where(
    wd_eve["is_exodus_evening"] == 1,
    "Pre-Holiday / Long-Weekend\nExodus Evening",
    "Regular Working\nWeekday Evening"
)

fig, ax = plt.subplots(figsize=(8.5, 5))
sns.boxplot(
    data=wd_eve, x="Regime", y="value",
    order=["Regular Working\nWeekday Evening", "Pre-Holiday / Long-Weekend\nExodus Evening"],
    palette=["#457B9D", "#E76F51"], width=0.42, showfliers=False, ax=ax
)

medians = wd_eve.groupby("Regime")["value"].median()
for idx, label in enumerate(["Regular Working\nWeekday Evening", "Pre-Holiday / Long-Weekend\nExodus Evening"]):
    med_val = medians[label]
    ax.text(idx, med_val + 1.5, f"Median: {med_val:.2f} µg/m³",
            ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#CBD5E1", alpha=0.9))

ax.set_title("Festival & Long-Weekend Exodus Evenings Amplify PM2.5 by +25.8% (p = 4.2e-12)",
             fontsize=11.5, fontweight="bold", pad=12, loc="left")
ax.set_xlabel("")
ax.set_ylabel("Evening PM2.5 Concentration (18:00-22:00 IST, µg/m³)", fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/fig4_exodus_evening_impact.png")
plt.close()

print("All 4 publication-grade charts saved successfully inside outputs/!")