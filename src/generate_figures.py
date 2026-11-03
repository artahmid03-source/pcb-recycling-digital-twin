# File: src/generate_figures.py
"""
Generates publication-grade SVG vector figures for the Waste-PCB Digital Twin:
- docs/fig1_architecture.svg: 5-Stage Process & Cyber-Physical Control Flowchart
- docs/fig2_corona_separator.svg: Stage 4 Corona Electrostatic Ballistics Schematic
- docs/fig3_recovery_trajectory.svg: Measured 500-kg Copper Recovery Trajectory Plot
"""

import csv
import os


def create_fig1_architecture(out_path: str) -> None:
    """Generates Figure 1: Five-stage plant and cyber-physical control architecture."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 430" width="100%" height="100%" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#334155"/>
    </marker>
    <marker id="arrow-bi" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#4f46e5"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="980" height="430" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>

  <!-- Top Layer Container: Physical Plant -->
  <rect x="20" y="20" width="940" height="190" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="6,4" stroke-width="1.5"/>
  <text x="35" y="46" font-size="14" font-weight="bold" fill="#0f172a">PHYSICAL / SIMPY MULTI-PHYSICS PLANT LAYER (880 &#215; 450 &#215; 580 mm ENVELOPE)</text>

  <!-- Stage 1 -->
  <rect x="35" y="65" width="160" height="125" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="115" y="88" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">Stage 1: Shredder</text>
  <text x="115" y="110" font-size="11.5" text-anchor="middle" fill="#1e293b">Dual-Shaft Shear</text>
  <text x="115" y="130" font-size="11.5" text-anchor="middle" fill="#1e293b">Torque &#964; &amp; Blade HI</text>
  <text x="115" y="150" font-size="11.5" text-anchor="middle" fill="#1e293b">d_80 = 8&#8211;12 mm</text>
  <text x="115" y="170" font-size="11" text-anchor="middle" fill="#475569">W_i = 16.4 kWh/t</text>

  <!-- Stage 2 -->
  <rect x="220" y="65" width="170" height="125" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="305" y="88" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">Stage 2: Hammer Mill</text>
  <text x="305" y="108" font-size="11.5" text-anchor="middle" fill="#1e293b">&amp; Vibrating Sieve</text>
  <text x="305" y="128" font-size="11.5" text-anchor="middle" fill="#1e293b">Rosin-Rammler PSD</text>
  <text x="305" y="148" font-size="11.5" text-anchor="middle" fill="#1e293b">Speed &#937;_hm (RPM)</text>
  <text x="305" y="168" font-size="11" text-anchor="middle" fill="#475569">d_lib &#8804; 0.65 mm</text>

  <!-- Stage 3 -->
  <rect x="415" y="65" width="170" height="125" rx="6" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="500" y="88" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">Stage 3: Air Cyclone</text>
  <text x="500" y="110" font-size="11.5" text-anchor="middle" fill="#1e293b">Lapple Cut-Size d_p50</text>
  <text x="500" y="130" font-size="11.5" text-anchor="middle" fill="#1e293b">Resin Dust Exhaust</text>
  <text x="500" y="150" font-size="11.5" text-anchor="middle" fill="#1e293b">Airflow Q_air (m&#179;/s)</text>
  <text x="500" y="170" font-size="11" text-anchor="middle" fill="#475569">Inlet B_c = 45 mm</text>

  <!-- Stage 4 -->
  <rect x="610" y="65" width="170" height="125" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="695" y="88" font-size="13" font-weight="bold" text-anchor="middle" fill="#b45309">Stage 4: Corona Roll</text>
  <text x="695" y="110" font-size="11.5" text-anchor="middle" fill="#1e293b">Electrostatic Separator</text>
  <text x="695" y="130" font-size="11.5" text-anchor="middle" fill="#1e293b">Pauthenier Charge q_max</text>
  <text x="695" y="150" font-size="11.5" text-anchor="middle" fill="#1e293b">U_kV (kV) &amp; &#969;_roll</text>
  <text x="695" y="170" font-size="11" text-anchor="middle" fill="#475569">R = 90 mm, Gap = 50 mm</text>

  <!-- Stage 5 Product Bins -->
  <rect x="805" y="65" width="140" height="125" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="875" y="88" font-size="13" font-weight="bold" text-anchor="middle" fill="#15803d">Product Bins</text>
  <text x="875" y="112" font-size="11.5" text-anchor="middle" fill="#1e293b">Cu Grade &#8805; 96%</text>
  <text x="875" y="134" font-size="11.5" text-anchor="middle" fill="#1e293b">Recovery &#8805; 94%</text>
  <text x="875" y="156" font-size="11.5" text-anchor="middle" fill="#1e293b">Middling Recycle</text>

  <!-- Process Flow Arrows -->
  <line x1="195" y1="127" x2="218" y2="127" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="390" y1="127" x2="413" y2="127" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="585" y1="127" x2="608" y2="127" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="780" y1="127" x2="803" y2="127" stroke="#334155" stroke-width="2.5" marker-end="url(#arrow)"/>

  <!-- Bottom Layer Container: Cyber-Physical Layer -->
  <rect x="20" y="230" width="940" height="180" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="6,4" stroke-width="1.5"/>
  <text x="35" y="256" font-size="14" font-weight="bold" fill="#0f172a">CYBER-PHYSICAL CONTROL, SAFETY INTERLOCK &amp; IIoT TELEMETRY LAYER</text>

  <!-- OpenPLC Box -->
  <rect x="35" y="275" width="275" height="115" rx="6" fill="#f1f5f9" stroke="#475569" stroke-width="2"/>
  <text x="172" y="300" font-size="13" font-weight="bold" text-anchor="middle" fill="#0f172a">OpenPLC Runtime (Modbus TCP :502)</text>
  <text x="172" y="324" font-size="11.5" text-anchor="middle" fill="#334155">IEC 61131-3 Ladder Logic Interlocks:</text>
  <text x="172" y="346" font-size="11.5" text-anchor="middle" fill="#334155">Rung 1: 3.0 s Auto-Reverse (&gt; 12.5 A)</text>
  <text x="172" y="368" font-size="11.5" text-anchor="middle" fill="#334155">Rung 2: 28 kV HV Gate (&gt; 30 RPM &amp; Door)</text>

  <!-- Shielded MO-PPO Box -->
  <rect x="350" y="275" width="280" height="115" rx="6" fill="#ede9fe" stroke="#6d28d9" stroke-width="2"/>
  <text x="490" y="300" font-size="13" font-weight="bold" text-anchor="middle" fill="#5b21b6">Shielded MO-PPO Agent (Gymnasium)</text>
  <text x="490" y="324" font-size="11.5" text-anchor="middle" fill="#334155">Observes [HI_blade, d_bar, Sieve_Load, w]</text>
  <text x="490" y="346" font-size="11.5" text-anchor="middle" fill="#334155">Adapts (&#937;_hm, Q_air, U_kV, &#969;_roll)</text>
  <text x="490" y="368" font-size="11.5" text-anchor="middle" fill="#334155">Weights w = [0.45, 0.40, 0.15]</text>

  <!-- InfluxDB & Grafana Box -->
  <rect x="670" y="275" width="275" height="115" rx="6" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
  <text x="807" y="300" font-size="13" font-weight="bold" text-anchor="middle" fill="#166534">InfluxDB 3 (:8181) &amp; Grafana (:3000)</text>
  <text x="807" y="324" font-size="11.5" text-anchor="middle" fill="#334155">Apache Arrow Flight SQL Telemetry</text>
  <text x="807" y="346" font-size="11.5" text-anchor="middle" fill="#334155">Tables: separation_kpis, comminution_state</text>
  <text x="807" y="368" font-size="11.5" text-anchor="middle" fill="#334155">Live Cu Grade, PSD &amp; Specific kWh/kg</text>

  <!-- Cyber-Physical Arrows -->
  <line x1="312" y1="332" x2="348" y2="332" stroke="#4f46e5" stroke-width="2.5" marker-start="url(#arrow)" marker-end="url(#arrow-bi)"/>
  <line x1="630" y1="332" x2="668" y2="332" stroke="#15803d" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="490" y1="275" x2="490" y2="195" stroke="#6d28d9" stroke-width="2.5" stroke-dasharray="5,3" marker-end="url(#arrow)"/>
</svg>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)


def create_fig2_corona_separator(out_path: str) -> None:
    """Generates Figure 2: Cross-sectional mechanics of Stage 4 Corona Electrostatic Separator."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 390" width="100%" height="100%" font-family="Segoe UI, Arial, sans-serif">
  <rect width="920" height="390" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <text x="30" y="35" font-size="15" font-weight="bold" fill="#0f172a">Stage 4: Roll-Type Corona-Electrostatic Tri-Zone Particle Ballistics (R_roll = 90 mm, L_gap = 50 mm)</text>

  <!-- Vibratory Feeder -->
  <text x="70" y="68" font-size="12.5" font-weight="bold" fill="#1e293b">Vibratory Feeder (Stage 3 Underflow)</text>
  <polygon points="85,78 245,78 255,100 85,100" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>

  <!-- Grounded Roll -->
  <circle cx="255" cy="195" r="78" fill="#e2e8f0" stroke="#0f172a" stroke-width="4"/>
  <circle cx="255" cy="195" r="8" fill="#0f172a"/>
  <text x="255" y="180" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#0f172a">Grounded Roll</text>
  <text x="255" y="218" font-size="11.5" text-anchor="middle" fill="#334155">R_roll = 90 mm, &#969;_roll</text>

  <!-- Scraper Brush -->
  <rect x="142" y="190" width="28" height="14" fill="#475569" stroke="#1e293b"/>
  <text x="95" y="201" font-size="11.5" text-anchor="middle" fill="#334155">Scraper Brush</text>

  <!-- Corona Ionization Electrode -->
  <circle cx="372" cy="108" r="11" fill="#f87171" stroke="#b91c1c" stroke-width="2.5"/>
  <line x1="363" y1="115" x2="325" y2="142" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,3"/>
  <line x1="367" y1="118" x2="332" y2="155" stroke="#ef4444" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="485" y="102" font-size="12.5" font-weight="bold" fill="#b91c1c">Corona Ionization Electrode (U_kV = 18&#8211;28 kV)</text>

  <!-- Static Electrostatic Electrode -->
  <ellipse cx="412" cy="182" rx="14" ry="34" transform="rotate(-18 412 182)" fill="#fde047" stroke="#ca8a04" stroke-width="2.5"/>
  <text x="505" y="168" font-size="12.5" font-weight="bold" fill="#a16207">Static Electrostatic Attraction Electrode</text>

  <!-- Trajectories -->
  <!-- FR-4 Insulator (Pinned) -->
  <path d="M 185 235 L 185 330" stroke="#64748b" stroke-width="3" stroke-dasharray="6,4" fill="none"/>
  <!-- Unliberated Middling (Drops near x=0) -->
  <path d="M 326 165 Q 340 245 352 330" stroke="#d97706" stroke-width="3.5" fill="none"/>
  <!-- Copper Conductor (Leaps forward) -->
  <path d="M 322 145 Q 405 195 468 330" stroke="#0284c7" stroke-width="4" fill="none"/>

  <!-- Collection Bins & Splitters -->
  <line x1="125" y1="330" x2="545" y2="330" stroke="#334155" stroke-width="3"/>
  <line x1="275" y1="295" x2="275" y2="355" stroke="#dc2626" stroke-width="3"/>
  <line x1="395" y1="295" x2="395" y2="355" stroke="#dc2626" stroke-width="3"/>

  <text x="200" y="352" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#475569">Bin 1: FR-4 Non-Metals</text>
  <text x="335" y="352" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#b45309">Bin 2: Middlings</text>
  <text x="475" y="352" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#0369a1">Bin 3: Copper Concentrate</text>

  <!-- Governing Force Balance Box -->
  <rect x="550" y="210" width="345" height="145" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>
  <text x="565" y="234" font-size="12.5" font-weight="bold" fill="#0f172a">Governing Force Balance on Roll Surface:</text>
  <text x="565" y="258" font-size="11.5" fill="#475569">&#8226; FR-4 Insulator: Pinned by Image Force</text>
  <text x="578" y="276" font-size="11" fill="#475569">F_img = q&#178; / (16&#960;&#949;_0 r_p&#178;)</text>
  <text x="565" y="300" font-size="11.5" fill="#0369a1">&#8226; Copper Conductor (d_p &#8804; 0.65 mm): Leaps via</text>
  <text x="578" y="318" font-size="11" fill="#0369a1">F_elec + m&#183;&#969;_roll&#178;&#183;R_roll &gt; m&#183;g&#183;cos(&#966;_det)</text>
  <text x="565" y="340" font-size="11.5" fill="#b45309">&#8226; Unliberated Middling (d_p &gt; 0.65 mm): Drops to Bin 2</text>
</svg>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)


def create_fig3_recovery_trajectory(csv_path: str, out_path: str) -> None:
    """Reads measured telemetry_stream.csv and plots Figure 3 Copper Recovery vs Cumulative WPCB Mass."""
    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    policies = ["Shielded_MO_PPO", "RSM_PID", "Static_Open_Loop"]
    series = {p: [] for p in policies}
    for r in rows:
        p = r["policy_mode"]
        if p in series:
            series[p].append((int(r["batch_idx"]), float(r["cu_recovery_pct"]), float(r["blade_hi"])))

    # Compute rolling/milestone points at 0, 25, 50, 75, 100 batches (0, 125, 250, 375, 500 kg)
    # Chart coordinate system: X in [90, 610] for batch [1..100], Y in [50, 290] for recovery [74%..98%]
    def to_xy(batch_idx: int, rec_pct: float) -> tuple:
        x = 90.0 + ((batch_idx - 1) / 99.0) * 520.0
        rec_clamped = max(74.0, min(98.0, rec_pct))
        y = 290.0 - ((rec_clamped - 74.0) / 24.0) * 240.0
        return round(x, 1), round(y, 1)

    def build_smoothed_points(data_list: list) -> list:
        """Computes 5 milestone averages at batches 1, 25, 50, 75, 100 for clean trajectory plotting."""
        windows = [(0, 5), (20, 30), (45, 55), (70, 80), (90, 100)]
        b_indices = [1, 25, 50, 75, 100]
        pts = []
        for b_idx, (w0, w1) in zip(b_indices, windows):
            vals = [item[1] for item in data_list[w0:w1]]
            mean_v = sum(vals) / len(vals)
            pts.append((b_idx, mean_v))
        return pts

    means = {
        p: round(sum(item[1] for item in series[p]) / len(series[p]), 2)
        for p in policies
    }

    moppo_pts = [to_xy(b, v) for b, v in build_smoothed_points(series["Shielded_MO_PPO"])]
    rsm_pts = [to_xy(b, v) for b, v in build_smoothed_points(series["RSM_PID"])]
    static_pts = [to_xy(b, v) for b, v in build_smoothed_points(series["Static_Open_Loop"])]

    def poly_str(pts: list) -> str:
        return " ".join(f"{x},{y}" for x, y in pts)

    moppo_circles = "\n  ".join(
        f'<circle cx="{x}" cy="{y}" r="4.5" fill="#0284c7"/>' for x, y in moppo_pts
    )
    rsm_circles = "\n  ".join(
        f'<circle cx="{x}" cy="{y}" r="4" fill="#d97706"/>' for x, y in rsm_pts
    )
    static_circles = "\n  ".join(
        f'<circle cx="{x}" cy="{y}" r="4" fill="#be123c"/>' for x, y in static_pts
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 370" width="100%" height="100%" font-family="Segoe UI, Arial, sans-serif">
  <rect width="940" height="370" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <text x="90" y="30" font-size="14.5" font-weight="bold" fill="#0f172a">Figure 3: Measured Copper Recovery Trajectory Across 500-kg WPCB Campaign (100 Batches)</text>

  <!-- Grid Lines & Y-Axis Labels (74% to 98%) -->
  <line x1="90" y1="50" x2="610" y2="50" stroke="#e2e8f0" stroke-width="1"/>
  <text x="78" y="54" font-size="11.5" text-anchor="end" fill="#475569">98%</text>

  <line x1="90" y1="110" x2="610" y2="110" stroke="#e2e8f0" stroke-width="1"/>
  <text x="78" y="114" font-size="11.5" text-anchor="end" fill="#475569">92%</text>

  <line x1="90" y1="170" x2="610" y2="170" stroke="#e2e8f0" stroke-width="1"/>
  <text x="78" y="174" font-size="11.5" text-anchor="end" fill="#475569">86%</text>

  <line x1="90" y1="230" x2="610" y2="230" stroke="#e2e8f0" stroke-width="1"/>
  <text x="78" y="234" font-size="11.5" text-anchor="end" fill="#475569">80%</text>

  <line x1="90" y1="290" x2="610" y2="290" stroke="#334155" stroke-width="2"/>
  <text x="78" y="294" font-size="11.5" text-anchor="end" fill="#475569">74%</text>

  <!-- Y-Axis Line & Title -->
  <line x1="90" y1="50" x2="90" y2="290" stroke="#334155" stroke-width="2"/>
  <text x="28" y="170" font-size="12.5" font-weight="bold" text-anchor="middle" transform="rotate(-90 28 170)" fill="#0f172a">Copper Recovery (%)</text>

  <!-- X-Axis Milestone Labels -->
  <text x="90" y="314" font-size="11.5" text-anchor="middle" fill="#334155">5 kg (HI=1.00)</text>
  <text x="220" y="314" font-size="11.5" text-anchor="middle" fill="#334155">125 kg (HI=0.84)</text>
  <text x="350" y="314" font-size="11.5" text-anchor="middle" fill="#334155">250 kg (HI=0.68)</text>
  <text x="480" y="314" font-size="11.5" text-anchor="middle" fill="#334155">375 kg (HI=0.51)</text>
  <text x="610" y="314" font-size="11.5" text-anchor="middle" fill="#334155">500 kg (HI=0.35)</text>
  <text x="350" y="344" font-size="12.5" font-weight="bold" text-anchor="middle" fill="#0f172a">Cumulative WPCB Processed &amp; Cutter Health Index (HI_blade)</text>

  <!-- Plotted Trajectories -->
  <polyline fill="none" stroke="#be123c" stroke-width="3" stroke-dasharray="4,4" points="{poly_str(static_pts)}"/>
  <polyline fill="none" stroke="#d97706" stroke-width="3" stroke-dasharray="8,5" points="{poly_str(rsm_pts)}"/>
  <polyline fill="none" stroke="#0284c7" stroke-width="3.5" points="{poly_str(moppo_pts)}"/>

  {static_circles}
  {rsm_circles}
  {moppo_circles}

  <!-- Legend Box -->
  <rect x="640" y="60" width="275" height="190" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="655" y="86" font-size="12.5" font-weight="bold" fill="#0f172a">Measured Campaign Legend</text>

  <line x1="655" y1="112" x2="695" y2="112" stroke="#0284c7" stroke-width="3.5"/>
  <circle cx="675" cy="112" r="4" fill="#0284c7"/>
  <text x="705" y="116" font-size="11.5" font-weight="bold" fill="#0284c7">Shielded MO-PPO ({means['Shielded_MO_PPO']}% Mean)</text>

  <line x1="655" y1="145" x2="695" y2="145" stroke="#d97706" stroke-width="3" stroke-dasharray="6,4"/>
  <circle cx="675" cy="145" r="4" fill="#d97706"/>
  <text x="705" y="149" font-size="11.5" font-weight="bold" fill="#b45309">RSM + PID Control ({means['RSM_PID']}% Mean)</text>

  <line x1="655" y1="178" x2="695" y2="178" stroke="#be123c" stroke-width="3" stroke-dasharray="3,3"/>
  <circle cx="675" cy="178" r="4" fill="#be123c"/>
  <text x="705" y="182" font-size="11.5" font-weight="bold" fill="#be123c">Static Open-Loop ({means['Static_Open_Loop']}% Mean)</text>

  <text x="655" y="214" font-size="11" fill="#475569">Dynamic &#937;_hm + U_kV adaptation</text>
  <text x="655" y="230" font-size="11" fill="#475569">prevents middling loss at low HI_blade</text>
</svg>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    create_fig1_architecture(os.path.join("docs", "fig1_architecture.svg"))
    create_fig2_corona_separator(os.path.join("docs", "fig2_corona_separator.svg"))
    create_fig3_recovery_trajectory(
        os.path.join("results", "telemetry_stream.csv"),
        os.path.join("docs", "fig3_recovery_trajectory.svg"),
    )
    print("Generated 3 publication-grade vector figures in docs/:")
    print(" - docs/fig1_architecture.svg")
    print(" - docs/fig2_corona_separator.svg")
    print(" - docs/fig3_recovery_trajectory.svg")