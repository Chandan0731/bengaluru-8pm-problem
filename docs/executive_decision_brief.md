# Executive Decision Brief: Mitigating Bengaluru's 8 PM Air Quality & Commuter Exposure Surge

**Prepared for:** Bengaluru Urban Services & Mobility Cell  
**Analysis Window:** November 2025 – November 2026 ($N = 226,171$ validated hourly air-quality records across 10 CPCB/KSPCB monitoring stations merged with Open-Meteo hourly weather and Karnataka holiday/exodus calendars)  
**By:** Chandan K S ,Sumith S Shet

---

## 1. Executive Summary

Between **19:00 and 21:00 IST ("The 8 PM Problem")**, Bengaluru experiences a statistically significant citywide surge in fine particulate matter ($\text{PM}_{2.5}$), rising from an afternoon baseline median of **26.10 µg/m³** (12:00–15:00 IST) to **32.30 µg/m³** ($p = 6.40 \times 10^{-66}$). Even after controlling for station location, wind speed, relative humidity, rainfall, and day-of-week regimes in multivariable OLS regression ($R^2 = 0.224, N = 50,435$), the 8 PM window adds **+3.82 µg/m³** ($p = 7.05 \times 10^{-44}$).

Crucially, empirical evidence challenges three common policy assumptions:
1. **The surge is corridor-specific, not uniform:** Commuter arterial bottlenecks at **Hebbal (+9.39 µg/m³)** and **Silk Board (+8.99 µg/m³)** drive the evening spike, whereas industrial **Peenya (-0.67 µg/m³)** shows no evening increase.
2. **The Rain Washout Paradox:** While evening rainfall triggers traffic congestion headlines, wet scavenging cuts 8 PM $\text{PM}_{2.5}$ by **51.2%** (**19.50 µg/m³** during light rain vs. **39.92 µg/m³** on dry evenings; $p = 3.78 \times 10^{-193}$). **Dry, low-wind evenings** represent the acute public health exposure hazard.
3. **7-Day Persistence & Exodus Amplification:** Evening $\text{PM}_{2.5}$ remains elevated across Core Office Days (Tue–Thu: **32.50 µg/m³**), Hybrid Edge Days (Mon/Fri: **31.60 µg/m³**), and Weekends (**32.50 µg/m³**; $p = 0.386$), but spikes by **+25.8%** (**38.50 vs. 30.60 µg/m³**, $p = 4.18 \times 10^{-12}$) on **Pre-Long-Weekend and Festival Exodus Evenings**.

---

## 2. Key Empirical Findings

| Hypothesis / Dimension | Metric & Comparison | Quantitative Result | Statistical Significance |
| :--- | :--- | :--- | :--- |
| **8 PM Diurnal Surge** | Evening Peak (19–21h) vs. Afternoon (12–15h) | Median **32.30** vs. **26.10 µg/m³** (+23.8%) | Mann-Whitney $p = 6.40 \times 10^{-66}$ |
| **Corridor Bottlenecks** | Evening (18–22h) minus Afternoon (12–15h) | **Hebbal +9.39**, **Silk Board +8.99**, **Jayanagar +8.76** vs. **Peenya -0.67 µg/m³** | Corridor divergence |
| **Rain Washout Paradox** | 8 PM (20:00 IST) Dry vs. Light Rain (0.1–2.5 mm) | Mean **39.92** vs. **19.50 µg/m³** (-51.2%) | Mann-Whitney $p = 3.78 \times 10^{-193}$ |
| **Hybrid Work Schedule** | 8 PM Median: Tue–Thu vs. Mon/Fri vs. Weekend | **32.50** / **31.60** / **32.50 µg/m³** | Kruskal-Wallis $H = 1.91, p = 0.386$ |
| **Festival / Exodus Surge** | Pre-Long-Weekend/Festival vs. Regular Weekday Eve | Median **38.50** vs. **30.60 µg/m³** (+25.8%) | Mann-Whitney $p = 4.18 \times 10^{-12}$ |

---

## 3. Actionable Policy & Operational Recommendations

1. **Deploy Dynamic Signal Prioritization & BMTC Bus-Lane Enforcement (18:00–21:30 IST, 7 Days a Week):**
   * Concentrate traffic-decongestion patrols and adaptive signal green-waves at **Hebbal Flyover**, **Central Silk Board**, and **Jayanagar 5th Block** across **all seven days of the week** (not just Tue–Thu), as evening boundary-layer trapping and retail/leisure trips keep weekend 8 PM exposure identical to core workdays.
2. **Trigger "Dry-Calm Evening" Public Health & Dust-Suppression Alerts:**
   * Replace rain-only traffic advisories with automated KSPCB/BBMP **Dry-Stagnant Evening Alerts** whenever evening precipitation is `0 mm` and wind speed drops below `8 km/h` (each `+1 km/h` of wind disperses `-0.74 µg/m³` of $\text{PM}_{2.5}$). Prioritize mechanical road sweeping and misting along Outer Ring Road and Bellary Road on dry evenings.
3. **Pre-Activate Exodus Corridor Protocols 24 Hours Before Long Weekends & Major Festivals:**
   * Because pre-holiday exodus evenings elevate $\text{PM}_{2.5}$ by **+7.90 µg/m³** (median), initiate staggered freight bans, extra BMTC/Namma Metro feeder frequency, and highway toll-plaza fast-tracking at **Hebbal (NH-44)** and **Silk Board / Electronic City (NH-48)** starting at 16:00 IST on exodus days.

---

## 4. Visual Evidence Index
* **Figure 1 (`outputs/fig1_diurnal_hybrid_curve.png`):** 24-hour $\text{PM}_{2.5}$ diurnal trajectory across Core Office, Hybrid Edge, and Weekend regimes.
* **Figure 2 (`outputs/fig2_corridor_surge_dumbbell.png`):** Station-level afternoon-to-evening surge comparison highlighting Hebbal and Silk Board.
* **Figure 3 (`outputs/fig3_rain_washout_paradox.png`):** Evening wet-scavenging drop comparing dry hours against light and moderate/heavy rain.
* **Figure 4 (`outputs/fig4_exodus_evening_impact.png`):** Distribution shift on pre-holiday/long-weekend exodus evenings vs. regular weekdays.