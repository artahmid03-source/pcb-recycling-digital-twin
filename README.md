\# Multi-Physics Digital Twin \& Shielded MO-PPO Control of a Waste-PCB Recycling Line



A plant-wide cyber-physical digital twin for a compact tabletop mechanical-electrostatic Waste Printed Circuit Board (WPCB) recycling line ($880 \\times 450 \\times 580\\text{ mm}$ envelope). This repository couples upstream Bond-Rosin-Rammler comminution cutter wear to downstream Lapple cyclone classification and Pauthenier corona-electrostatic ballistics, governed by an IEC 61131-3 safety-shielded Multi-Objective Proximal Policy Optimization (MO-PPO) controller.



\## Physical \& Process Parameters



\- \*\*Feed Composition:\*\* 28% Copper ($\\rho\_{Cu} = 8,960\\text{ kg/m}^3$), 72% FR-4 Epoxy-Fiberglass ($\\rho\_{FR4} = 1,850\\text{ kg/m}^3$)

\- \*\*Liberation Threshold ($d\_{lib}$):\*\* $0.65\\text{ mm}$ (composite middling density $\\rho\_{mid} \\approx 3,600\\text{ kg/m}^3$)

\- \*\*Composite Bond Work Index ($W\_i$):\*\* $16.4\\text{ kWh/t}$

\- \*\*Stage 3 Cyclone Geometry:\*\* Inlet width $B\_c = 45\\text{ mm}$, height $H\_c = 90\\text{ mm}$, effective vortex turns $N\_e = 5.0$

\- \*\*Stage 4 Electrostatic Separator:\*\* Grounded roll radius $R\_{roll} = 90\\text{ mm}$, corona gap $L\_{gap} = 50\\text{ mm}$, splitter drop $H\_{bin} = 220\\text{ mm}$

\- \*\*OpenPLC Safety Interlocks:\*\*

&#x20; 1. \*\*Shredder Over-Torque Auto-Reverse (`%QX0.1`):\*\* 3.0-second reverse unjamming cycle whenever motor current exceeds $12.5\\text{ A}$.

&#x20; 2. \*\*High-Voltage Corona Gate (`%QX0.3`):\*\* Permits $18\\text{--}28\\text{ kV}$ supply only when enclosure interlock `%IX0.1 == TRUE` and roll speed $> 30\\text{ RPM}$.



\## Quickstart (Windows PowerShell)



&#x20;   python -m venv .venv

&#x20;   .\\.venv\\Scripts\\Activate.ps1

&#x20;   pip install -r requirements.txt

&#x20;   python src\\run\_pcb\_digital\_twin.py

&#x20;   pytest -v



\## InfluxDB 3 Core \& Grafana Flight SQL Schema



The simulation exports batch telemetry to results/telemetry\_stream.csv matching the three InfluxDB 3 Core tables (separation\_kpis, comminution\_state, electrostatic\_state):



\- Panel 1 (separation\_kpis): SELECT time, cu\_grade\_pct, cu\_recovery\_pct FROM separation\_kpis WHERE time >= now() - 1h ORDER BY time

\- Panel 2 (comminution\_state): SELECT time, blade\_hi, mean\_dp\_mm, hm\_rpm FROM comminution\_state WHERE time >= now() - 1h

\- Panel 3 (electrostatic\_state): SELECT time, voltage\_kv, roll\_rpm, spec\_kwh\_per\_kg FROM electrostatic\_state WHERE time >= now() - 1h

