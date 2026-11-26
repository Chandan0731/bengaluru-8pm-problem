import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Bengaluru 8 PM Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, high-contrast institutional styling (zero emojis)
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .alert-red {
        background-color: #FEF2F2; border-left: 6px solid #DC2626;
        padding: 1rem 1.25rem; border-radius: 6px; color: #7F1D1D;
        font-weight: 600; margin-bottom: 1rem;
    }
    .alert-amber {
        background-color: #FFFBEB; border-left: 6px solid #D97706;
        padding: 1rem 1.25rem; border-radius: 6px; color: #78350F;
        font-weight: 600; margin-bottom: 1rem;
    }
    .alert-green {
        background-color: #ECFDF5; border-left: 6px solid #059669;
        padding: 1rem 1.25rem; border-radius: 6px; color: #064E3B;
        font-weight: 600; margin-bottom: 1rem;
    }
    .decision-box {
        background-color: #F8FAFC; border: 1px solid #CBD5E1;
        padding: 1rem 1.25rem; border-radius: 6px; color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/dashboard_summary.csv")

df = load_data()

# --- SIDEBAR: OPERATIONAL SCENARIO CONTROLS ---
st.sidebar.header("Operational Scenario Controls")
st.sidebar.caption("Select corridor, weather, and calendar conditions to simulate 8 PM exposure and recommended deployment.")

stations = ["All Bengaluru Corridors (Citywide)"] + sorted(df["short_station"].unique().tolist())
selected_station = st.sidebar.selectbox("1. Target Corridor / Junction", stations, index=0)

weather_choice = st.sidebar.radio(
    "2. Evening Weather Condition",
    ["All Evenings", "Dry Evening (0 mm)", "Rainy Evening (> 0 mm)"],
    index=1
)

calendar_choice = st.sidebar.radio(
    "3. Calendar / Travel Regime",
    ["All Days", "Regular Day", "Pre-Holiday / Exodus"],
    index=0
)

day_choice = st.sidebar.selectbox(
    "4. Work-Week Schedule",
    ["All Days (7-Day View)", "Core Office (Tue-Thu)", "Hybrid Edge (Mon & Fri)", "Weekend (Sat-Sun)"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Foundation:** 226,171 validated hourly CPCB/KSPCB & Open-Meteo records (Nov 2025 – Nov 2026).")

# --- FILTER DATA ---
filtered = df.copy()
if selected_station != "All Bengaluru Corridors (Citywide)":
    filtered = filtered[filtered["short_station"] == selected_station]
if weather_choice != "All Evenings":
    filtered = filtered[filtered["weather_regime"] == weather_choice]
if calendar_choice != "All Days":
    filtered = filtered[filtered["calendar_regime"] == calendar_choice]
if day_choice != "All Days (7-Day View)":
    filtered = filtered[filtered["day_regime"] == day_choice]

def weighted_avg(sub_df):
    if sub_df.empty or sub_df["sample_count"].sum() == 0:
        return np.nan
    return np.average(sub_df["mean_pm25"], weights=sub_df["sample_count"])

aft_val = weighted_avg(filtered[filtered["hour_ist"].between(12, 15)])
peak_val = weighted_avg(filtered[filtered["hour_ist"].between(19, 21)])
delta_val = peak_val - aft_val if pd.notnull(peak_val) and pd.notnull(aft_val) else 0.0
pct_change = (delta_val / aft_val * 100) if pd.notnull(aft_val) and aft_val > 0 else 0.0

# --- HEADER & COMMAND STATUS BANNER ---
st.title("Bengaluru 8 PM Air Quality ")
st.markdown("**Prepared for:** Office of the Commissioner & Urban Services Cell | **Focus Window:** 19:00 – 21:00 IST")

if pd.notnull(peak_val):
    if peak_val >= 38.0:
        st.markdown(
            f'<div class="alert-red">COMMAND STATUS: HIGH EXPOSURE ALERT ({peak_val:.1f} µg/m³ at 8 PM) — '
            f'Activate adaptive signal green-waves, traffic marshals, and BBMP road-misting immediately.</div>',
            unsafe_allow_html=True
        )
    elif peak_val >= 28.0:
        st.markdown(
            f'<div class="alert-amber">COMMAND STATUS: ELEVATED EVENING SURGE ({peak_val:.1f} µg/m³ at 8 PM) — '
            f'Maintain standard 18:00–21:30 IST bottleneck decongestion and BMTC bus-lane priority.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="alert-green">COMMAND STATUS: LOW PARTICULATE EXPOSURE ({peak_val:.1f} µg/m³ at 8 PM) — '
            f'Wet scavenging / dispersion active; shift field units from dust control to waterlogging & traffic flow.</div>',
            unsafe_allow_html=True
        )

# --- TOP KPI METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Afternoon Baseline (12–15h)", f"{aft_val:.1f} µg/m³" if pd.notnull(aft_val) else "N/A")
c2.metric("8 PM Peak Window (19–21h)", f"{peak_val:.1f} µg/m³" if pd.notnull(peak_val) else "N/A",
          delta=f"{delta_val:+.1f} µg/m³ ({pct_change:+.1f}%)", delta_color="inverse")
c3.metric("Top Priority Bottlenecks", "Hebbal & Silk Board", delta="+9.4 & +9.0 µg/m³ surge", delta_color="off")
c4.metric("Rain Washout Effect (8 PM)", "-51.2% PM2.5", delta="19.5 vs 39.9 µg/m³ dry", delta_color="off")

st.markdown("---")

# --- MAIN ANALYTICAL TABS ---
tab1, tab2, tab3 = st.tabs([
    "1. Hourly Exposure Trajectory",
    "2. Corridor Deployment Triage",
    "3. Actionable Policy Matrix"
])

with tab1:
    col_chart, col_takeaway = st.columns([2.2, 1])
    with col_chart:
        hourly = (
            filtered.groupby("hour_ist")
            .apply(lambda g: np.average(g["mean_pm25"], weights=g["sample_count"]))
            .reset_index(name="pm25")
        )
        fig, ax = plt.subplots(figsize=(9, 4.2))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(True, linestyle="--", alpha=0.25)

        ax.plot(hourly["hour_ist"], hourly["pm25"], color="#1B365D", linewidth=2.6, marker="o", markersize=5)
        ax.axvspan(19, 21, color="#DC2626", alpha=0.12, label="8 PM Peak Window (19:00–21:00 IST)")
        ax.axvline(20, color="#DC2626", linestyle=":", linewidth=1.3)

        ax.set_title(f"24-Hour PM2.5 Profile: {selected_station}", fontsize=11.5, fontweight="bold", loc="left", pad=10)
        ax.set_xlabel("Hour of Day (IST)", fontweight="bold")
        ax.set_ylabel("Mean PM2.5 (µg/m³)", fontweight="bold")
        ax.set_xticks(range(0, 24, 2))
        ax.set_xlim(0, 23)
        ax.legend(loc="lower left", frameon=True, facecolor="white")
        plt.tight_layout()
        st.pyplot(fig)

    with col_takeaway:
        st.subheader("Key Briefing Takeaways")
        st.markdown("""
        * **Why 8 PM Matters:** Evening traffic gridlock coincides with nocturnal boundary-layer cooling, trapping exhaust at breathing height.
        * **7-Day Persistence:** Weekend 8 PM pollution (**32.5 µg/m³**) matches Tue–Thu office nights—enforcement cannot pause on weekends.
        * **The Rain Paradox:** Rain slows traffic, but washes out **51.2%** of particulates. **Dry, calm evenings** pose the highest health risk.
        """)

with tab2:
    st.subheader("Where to Deploy Field Resources: Evening Surge by Station (18–22h vs. 12–15h)")
    st_base = df.copy()
    if weather_choice != "All Evenings":
        st_base = st_base[st_base["weather_regime"] == weather_choice]
    if calendar_choice != "All Days":
        st_base = st_base[st_base["calendar_regime"] == calendar_choice]

    aft_s = st_base[st_base["hour_ist"].between(12, 15)].groupby("short_station").apply(
        lambda g: np.average(g["mean_pm25"], weights=g["sample_count"])
    )
    eve_s = st_base[st_base["hour_ist"].between(18, 22)].groupby("short_station").apply(
        lambda g: np.average(g["mean_pm25"], weights=g["sample_count"])
    )
    comp = pd.DataFrame({"Afternoon (12-15h)": aft_s, "Evening (18-22h)": eve_s}).dropna()
    comp["Evening Surge Delta"] = comp["Evening (18-22h)"] - comp["Afternoon (12-15h)"]
    comp = comp.sort_values("Evening Surge Delta", ascending=True)

    fig2, ax2 = plt.subplots(figsize=(9.5, 4.4))
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(True, linestyle="--", alpha=0.25)

    y_pos = np.arange(len(comp))
    for idx, (_, row) in enumerate(comp.iterrows()):
        c = "#DC2626" if row["Evening Surge Delta"] > 7 else ("#2563EB" if row["Evening Surge Delta"] > 0 else "#64748B")
        ax2.plot([row["Afternoon (12-15h)"], row["Evening (18-22h)"]], [idx, idx], color=c, linewidth=2.8)
        sign = "+" if row["Evening Surge Delta"] >= 0 else ""
        ax2.text(max(row["Afternoon (12-15h)"], row["Evening (18-22h)"]) + 0.6, idx,
                 f"{sign}{row['Evening Surge Delta']:.2f} µg/m³", va="center", fontsize=9, fontweight="bold", color=c)

    ax2.scatter(comp["Afternoon (12-15h)"], y_pos, color="#64748B", s=70, label="Afternoon (12–15h)", zorder=3)
    ax2.scatter(comp["Evening (18-22h)"], y_pos, color="#1B365D", s=80, label="Evening Rush (18–22h)", zorder=4)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(comp.index, fontweight="bold")
    ax2.set_xlim(15, max(56, comp["Evening (18-22h)"].max() + 8))
    ax2.set_xlabel("Mean PM2.5 Concentration (µg/m³)", fontweight="bold")
    ax2.set_title("Corridor Triage: Commuter Hubs Surge While Industrial Peenya Drops", fontsize=11.5, fontweight="bold", loc="left")
    ax2.legend(loc="lower right", frameon=True, facecolor="white")
    plt.tight_layout()
    st.pyplot(fig2)

with tab3:
    st.subheader("Recommended Operational Decisions for Bengaluru Urban Services Cell")
    decision_table = pd.DataFrame([
        {
            "Operational Trigger": "Daily Evening Window (18:00 – 21:30 IST, All 7 Days)",
            "Priority Corridors": "Hebbal Flyover (+9.39 µg/m³), Silk Board (+8.99 µg/m³), Jayanagar 5th Block (+8.76 µg/m³)",
            "Recommended Action": "Deploy adaptive traffic signal green-waves and strict BMTC bus-lane enforcement across all 7 days; reallocate evening pollution patrols away from Peenya (-0.67 µg/m³)."
        },
        {
            "Operational Trigger": "Dry & Stagnant Evening (Rain = 0 mm & Wind < 8 km/h)",
            "Priority Corridors": "Outer Ring Road, Bellary Road (NH-44), Hosur Road (NH-48)",
            "Recommended Action": "Issue automated Dry-Calm Evening health advisories for traffic personnel and activate BBMP mechanical road sweeping/misting (rainy evenings self-clean by -51.2%)."
        },
        {
            "Operational Trigger": "Pre-Long-Weekend / Festival Exodus Evening (16:00 – 22:00 IST)",
            "Priority Corridors": "Hebbal Exit (NH-44), Silk Board / Electronic City Toll Corridor (NH-48)",
            "Recommended Action": "Pre-activate staggered heavy-freight restrictions 24 hours before long weekends and add Metro/BMTC feeder frequency to curb the +25.8% (+7.90 µg/m³) exodus spike."
        }
    ])
    st.table(decision_table)