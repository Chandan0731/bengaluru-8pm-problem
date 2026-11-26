from fpdf import FPDF

class MemoPDF(FPDF):
    def footer(self):
        self.set_y(-11)
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(100, 116, 139)
        self.cell(
            0, 6,
            "Bengaluru Urban Services & Mobility Cell  |  Data Window: Nov 2025 - Nov 2026 (N = 226,171 Validated Records)  |  Page 1 of 1",
            align="C"
        )

pdf = MemoPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=False)
pdf.add_page()

# --- TOP NAVY HEADER BANNER ---
pdf.set_fill_color(27, 54, 93)
pdf.rect(12, 10, 186, 18, style="F")
pdf.set_xy(16, 12.5)
pdf.set_font("Helvetica", "B", 13.5)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 6, "OPERATIONAL DECISION BRIEF: THE 8 PM AIR QUALITY SURGE", ln=True)
pdf.set_x(16)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(226, 232, 240)
pdf.cell(0, 5, "Actionable Corridor Triage, Weather Triggers & Holiday Exodus Protocols for Bengaluru", ln=True)

# --- METADATA BLOCK ---
pdf.set_fill_color(241, 245, 249)
pdf.set_draw_color(203, 213, 225)
pdf.rect(12, 30, 186, 12, style="DF")
pdf.set_font("Helvetica", "B", 8.5)
pdf.set_text_color(27, 54, 93)
pdf.set_xy(15, 31.5)
pdf.cell(14, 4.5, "TO:")
pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(30, 41, 59)
pdf.cell(82, 4.5, "Office of the Commissioner & Urban Services Cell")
pdf.set_font("Helvetica", "B", 8.5)
pdf.set_text_color(27, 54, 93)
pdf.cell(16, 4.5, "DATE:")
pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(30, 41, 59)
pdf.cell(0, 4.5, "November 26, 2026", ln=True)

pdf.set_x(15)
pdf.set_font("Helvetica", "B", 8.5)
pdf.set_text_color(27, 54, 93)
pdf.cell(14, 4.5, "FROM:")
pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(30, 41, 59)
pdf.cell(82, 4.5, "Chandan K S, Data Analytics")
pdf.set_font("Helvetica", "B", 8.5)
pdf.set_text_color(27, 54, 93)
pdf.cell(16, 4.5, "WINDOW:")
pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(30, 41, 59)
pdf.cell(0, 4.5, "19:00 - 21:00 IST (Daily Peak Window)", ln=True)

# --- SECTION 1: EXECUTIVE SITUATION ASSESSMENT ---
pdf.set_xy(12, 46)
pdf.set_font("Helvetica", "B", 10.5)
pdf.set_text_color(27, 54, 93)
pdf.cell(0, 6, "1. Executive Situation Assessment", ln=True)
pdf.set_draw_color(27, 54, 93)
pdf.line(12, 52, 198, 52)

pdf.set_xy(12, 54)
pdf.set_font("Helvetica", "", 8.5)
pdf.set_text_color(30, 41, 59)
pdf.multi_cell(
    186, 4.2,
    "Between 19:00 and 21:00 IST ('The 8 PM Problem'), Bengaluru experiences a consistent citywide spike in fine particulate matter (PM2.5), rising +23.8% over afternoon levels (32.30 vs. 26.10 ug/m3). Cross-referencing 10 CPCB/KSPCB stations with hourly meteorology and Karnataka holiday calendars identifies three operational realities that overturn conventional deployment assumptions:"
)

bullets = [
    ("Corridor-Specific Bottlenecks: ", "Evening pollution surges at commuter hubs - Hebbal (+9.39 ug/m3) and Silk Board (+8.99 ug/m3) - whereas industrial Peenya (-0.67 ug/m3) drops in the evening."),
    ("The Rain Washout Paradox: ", "Rain causes traffic delays, yet cuts 8 PM PM2.5 in half (19.50 vs. 39.92 ug/m3 on dry nights; -51.2%). Dry, low-wind evenings (< 8 km/h) are the true respiratory hazard."),
    ("7-Day Persistence & Exodus Spikes: ", "Weekend 8 PM pollution (32.50 ug/m3) equals Tue-Thu office nights, while Pre-Long-Weekend / Festival Exodus Evenings spike an additional +25.8% (38.50 vs. 30.60 ug/m3).")
]
y_b = pdf.get_y() + 1.5
for bold_lead, body_txt in bullets:
    pdf.set_xy(15, y_b)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(27, 54, 93)
    pdf.write(4.1, "- " + bold_lead)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.write(4.1, body_txt)
    y_b = pdf.get_y() + 5.2

# --- SECTION 2: VISUAL EVIDENCE ---
pdf.set_xy(12, y_b + 1)
pdf.set_font("Helvetica", "B", 10.5)
pdf.set_text_color(27, 54, 93)
pdf.cell(0, 6, "2. Visual Evidence: Corridor Hotspots & Rain Scavenging", ln=True)
pdf.line(12, y_b + 7, 198, y_b + 7)

img_y = y_b + 9
pdf.image("outputs/fig2_corridor_surge_dumbbell.png", x=12, y=img_y, w=91)
pdf.image("outputs/fig3_rain_washout_paradox.png", x=107, y=img_y, w=91)

# --- SECTION 3: RECOMMENDED COMMAND DECISIONS ---
sec3_y = img_y + 51
pdf.set_xy(12, sec3_y)
pdf.set_font("Helvetica", "B", 10.5)
pdf.set_text_color(27, 54, 93)
pdf.cell(0, 6, "3. Recommended Command Decisions & Deployment Matrix", ln=True)
pdf.line(12, sec3_y + 6, 198, sec3_y + 6)

# Table Header
t_y = sec3_y + 8
pdf.set_fill_color(27, 54, 93)
pdf.set_text_color(255, 255, 255)
pdf.set_font("Helvetica", "B", 8)
pdf.set_xy(12, t_y)
pdf.cell(48, 6.5, " Operational Trigger", border=1, fill=True)
pdf.cell(48, 6.5, " Target Corridors", border=1, fill=True)
pdf.cell(90, 6.5, " Immediate Field Action", border=1, fill=True, ln=True)

rows = [
    (
        "1. Daily 8 PM Window\n(18:00-21:30 IST, All 7 Days)",
        "Hebbal Flyover (+9.39),\nSilk Board (+8.99),\nJayanagar (+8.76)",
        "Deploy adaptive traffic signal green-waves and strict BMTC bus-lane enforcement across all 7 days; reallocate evening patrols away from Peenya."
    ),
    (
        "2. Dry & Calm Evenings\n(Rain = 0 mm, Wind < 8 km/h)",
        "Outer Ring Road,\nBellary Rd (NH-44),\nHosur Rd (NH-48)",
        "Issue automated health advisories for outdoor traffic personnel and trigger BBMP mechanical road misting (rainy evenings self-clean by -51.2%)."
    ),
    (
        "3. Pre-Holiday Exodus\n(16:00-22:00 IST pre-holiday)",
        "Hebbal Exit (NH-44),\nSilk Board / Electronic\nCity Toll (NH-48)",
        "Pre-activate staggered heavy-freight bans 24 hours ahead and increase Metro/BMTC feeder frequency to curb the +25.8% exodus surge."
    )
]

curr_y = t_y + 6.5
for idx, (col1, col2, col3) in enumerate(rows):
    row_h = 16.5
    if idx % 2 == 1:
        pdf.set_fill_color(248, 250, 252)
    else:
        pdf.set_fill_color(255, 255, 255)
    pdf.rect(12, curr_y, 186, row_h, style="DF")
    pdf.line(60, curr_y, 60, curr_y + row_h)
    pdf.line(108, curr_y, 108, curr_y + row_h)

    pdf.set_font("Helvetica", "B", 7.8)
    pdf.set_text_color(27, 54, 93)
    pdf.set_xy(13, curr_y + 1.5)
    pdf.multi_cell(46, 3.8, col1)

    pdf.set_font("Helvetica", "", 7.8)
    pdf.set_text_color(30, 41, 59)
    pdf.set_xy(61, curr_y + 1.5)
    pdf.multi_cell(46, 3.8, col2)

    pdf.set_xy(109, curr_y + 1.5)
    pdf.multi_cell(88, 3.8, col3)
    curr_y += row_h

pdf.output("docs/commissioner_decision_memo.pdf")
print("Generated docs/commissioner_decision_memo.pdf successfully!")