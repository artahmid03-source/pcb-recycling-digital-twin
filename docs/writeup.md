\# Multi-Physics Digital Twin and Deep Reinforcement Learning Control of a Compact Mechanical-Electrostatic Waste PCB Recycling Line



\*\*Author:\*\* Arifur Rahman Tahmid  

\*\*Affiliation:\*\* Department of Mechanical and Production Engineering (MPE), Islamic University of Technology (IUT)  

\*\*Contact:\*\* artahmid03@gmail.com  

\*\*Target Venues:\*\* \*Resources, Conservation and Recycling\*, \*Waste Management\*, \*Journal of Cleaner Production\*



\---



\## 1. Executive Overview and Research Novelty

Dry mechanical-physical separation is the cleanest industrial pathway for recovering high-purity copper (Cu) and precious metals from Waste Printed Circuit Boards (WPCBs: 28% Cu with $\\rho\_{Cu}=8,960\\text{ kg/m}^3$; 72% FR-4 epoxy-fiberglass with $\\rho\_{FR4}=1,850\\text{ kg/m}^3$) without cyanide leaching or acid smelting (Cui \& Forssberg, 2003). Existing recycling models optimize unit operations in isolation (Lu et al., 2008). In a compact $880 \\times 450 \\times 580\\text{ mm}$ recycling unit, progressive wear on the shredder and hammer-mill cutters shifts the crushed particle size distribution (PSD) above the $0.65\\text{ mm}$ copper delamination threshold, clogging the feeder and causing copper recovery to drop by more than 18%.



This study presents a closed-loop Multi-Physics Digital Twin that couples upstream Bond-Rosin-Rammler comminution mechanics to downstream Lapple cyclone classification and Maxwell-Pauthenier corona electrostatic ballistics, regulated by an IEC 61131-3 safety-shielded Multi-Objective Proximal Policy Optimization (MO-PPO) controller (Schulman et al., 2017; Raffin et al., 2021).



\---



\## 2. System Architecture and Five-Stage Process Flow



!\[Figure 1: End-to-End Physical Material Flow and Cyber-Physical Control Architecture](fig1\_architecture.svg)

\*Figure 1: End-to-end physical material flow and cyber-physical control architecture of the 5-stage waste PCB recovery Digital Twin ($880 \\times 450 \\times 580\\text{ mm}$ envelope), linking multi-physics comminution/ballistics, OpenPLC safety interlocks, Shielded MO-PPO setpoint control, and InfluxDB 3 Core / Grafana observability.\*



\### Closed-Loop Cyber-Physical Control \& Safety Shield Flowchart



```mermaid

flowchart TD

&#x20;   A\[5-kg WPCB Batch Feed: 28% Cu, 72% FR-4] --> B\[Stage 1: Dual-Shaft Shredder]

&#x20;   B -->|Motor Current I\_shred > 12.5 A?| C{OpenPLC Rung 1}

&#x20;   C -->|YES: Jam Detected| D\[Trigger %QX0.1: 3.0 s Auto-Reverse TON\_REV]

&#x20;   C -->|NO: Normal Shear| E\[Stage 2: Hammer Mill \& Vibrating Sieve]

&#x20;   D --> E

&#x20;   E -->|Gamma Blade Wear HI\_blade \& Rosin-Rammler PSD d\_bar| F\[Stage 3: Lapple Cyclone Classifier B\_c = 45 mm]

&#x20;   F -->|Strip FR-4 Dust via Airflow Q\_air| G{OpenPLC Rung 2: Door Closed \& Roll > 30 RPM?}

&#x20;   G -->|NO: Unsafe State| H\[De-energize %QX0.3: HV Supply = 0 kV]

&#x20;   G -->|YES: Interlock Passed| I\[Stage 4: Corona Roll R = 90 mm, Gap = 50 mm, U\_kV = 18-28 kV]

&#x20;   I --> J\[Product Bins: Bin 1 FR-4, Bin 2 Middlings, Bin 3 Cu Concentrate]

&#x20;   J --> K\[Shielded MO-PPO Agent: Observes HI\_blade, d\_bar, Sieve\_Load, w]

&#x20;   K -->|Updates Holding Registers 40001-40004: Ohm, Q\_air, U\_kV, w\_roll| E

```



\### Table 1: Five-Stage Subsystem Governing Laws and State Variables



| Stage | Subsystem | Governing Physical Law | Control Input ($u\_t$) | Twin State / Output ($x\_t, y\_t$) |

| :--- | :--- | :--- | :--- | :--- |

| \*\*Stage 1\*\* | Double-Shaft Primary Shredder | Bond Work Index (Bond, 1952) \& Gamma Blade Wear | Shaft Speed $\\Omega\_{shred}$, Feed $\\dot{m}\_{in}$ | Coarse size $d\_{80}$, Torque $\\tau\_{shred}$, Health $HI\_{blade}$ |

| \*\*Stage 2\*\* | Vibrating Sieve \& Hammer Mill | Rosin-Rammler PSD \& Liberation $L(d\_p)$ | Hammer Speed $\\Omega\_{hm}$ (1,900–2,900 RPM) | Mean size $\\bar{d}\_p$ (mm), Liberation fraction $L\_{Cu}$ |

| \*\*Stage 3\*\* | Cyclone Air Density Classifier | Lapple Centrifugal Cut-Size $d\_{p50}$ (Lapple, 1951) | Blower Airflow $Q\_{air}$ ($\\text{m}^3/\\text{s}$) | Fiberglass dust removal $\\eta\_{air}$, Underflow $\\dot{m}\_u$ |

| \*\*Stage 4\*\* | Roll-Type Corona Electrostatic | Pauthenier Charge (Pauthenier, 1932) \& Ballistic ODE | Voltage $U\_{kV}$ (kV), Roll $\\omega\_{roll}$ (RPM) | Landing coordinate $x\_{land}$, Cu Grade \& Recovery |

| \*\*Stage 5\*\* | OpenPLC \& MO-PPO Supervisor | Multi-Objective MDP + IEC 61131-3 Interlocks | Setpoints $(\\Omega\_{hm}, Q\_{air}, U\_{kV}, \\omega\_{roll})$ | Net Reward $R\_k$, Specific Energy ($\\text{kWh/kg}$) |



\---



\## 3. Multi-Physics Mathematical Formulation



\### 3.1 Stage 1 \& 2: Comminution Energy, Blade Degradation, and Copper Liberation

By Bond (1952), specific comminution energy $E\_{comm}$ ($\\text{kWh/t}$) with composite work index $W\_i \\approx 16.4\\text{ kWh/t}$ and cutter health index $HI\_{blade} \\in \[0, 1]$ is:



$$E\_{comm} = 10 \\cdot W\_i \\cdot \\left(\\frac{1}{\\sqrt{d\_{80}}} - \\frac{1}{\\sqrt{D\_{80}}}\\right) \\cdot \\left\[1 + 0.45 \\cdot (1 - HI\_{blade})\\right]$$



Irreversible cutter wear $\\Delta D\_{blade}$ over batch duration $\\Delta t$ follows a non-homogeneous Gamma process (van Noortwijk, 2009), shifting the Rosin-Rammler characteristic particle size $\\bar{d}(\\Omega\_{hm}, HI\_{blade})$:



$$\\bar{d}(\\Omega\_{hm}, HI\_{blade}) = d\_0 \\cdot \\left(\\frac{\\Omega\_{nom}}{\\Omega\_{hm}}\\right)^{0.65} \\cdot \\left\[1 + \\lambda\_w (1 - HI\_{blade})\\right]$$



Copper delaminates cleanly from FR-4 when $d\_p \\le d\_{lib} \\approx 0.65\\text{ mm}$ (Cui \& Forssberg, 2003); coarser fragments ($d\_p > 0.65\\text{ mm}$) remain locked as composite middlings ($\\rho\_{mid} \\approx 3,600\\text{ kg/m}^3$).



\### 3.2 Stage 3: Cyclone Air Density Classifier

Using Lapple (1951) centrifugal cut-size theory with air viscosity $\\mu\_{air} = 1.81 \\times 10^{-5}\\text{ Pa}\\cdot\\text{s}$, inlet width $B\_c = 0.045\\text{ m}$, height $H\_c = 0.090\\text{ m}$, and $N\_e = 5.0$ vortex turns:



$$d\_{p50} = \\sqrt{\\frac{g \\cdot \\mu\_{air} \\cdot B\_c^2}{2 \\cdot \\pi \\cdot N\_e \\cdot v\_{in} \\cdot (\\rho\_p - \\rho\_{air})}}, \\quad P\_{underflow}(d\_p) = \\frac{1}{1 + (d\_{p50} / d\_p)^{2.2}}$$



\### 3.3 Stage 4: Roll-Type Corona Electrostatic Ballistics

Across corona gap $L\_{gap} = 0.050\\text{ m}$ on a grounded roll of radius $R\_{roll} = 0.090\\text{ m}$, a particle of radius $r\_p = d\_p / 2$ acquires Pauthenier saturation charge (Pauthenier \& Moreau-Hanot, 1932):



$$q\_{max} = 4 \\cdot \\pi \\cdot \\varepsilon\_0 \\cdot \\left(\\frac{3\\varepsilon\_r}{\\varepsilon\_r + 2}\\right) \\cdot r\_p^2 \\cdot E\_{corona}, \\quad E\_{corona} \\approx \\frac{U\_{kV}}{L\_{gap}}$$



!\[Figure 2: Cross-Sectional Mechanics of Stage 4 Roll-Type Corona Electrostatic Separator](fig2\_corona\_separator.svg)

\*Figure 2: Cross-sectional mechanics of Stage 4 (Roll-Type Corona Electrostatic Separator) showing why uncompensated upstream blade wear ($d\_p > 0.65\\text{ mm}$) causes unliberated composite particles to drop into the Middlings bin (Lu et al., 2008).\*



\---



\## 4. OpenPLC Modbus TCP Register Map \& Safety Shield



| Modbus Address | IEC 61131-3 Tag | Variable Name | Data Type / Unit | Interlock / Control Role |

| :--- | :--- | :--- | :--- | :--- |

| \*\*Coil 00001\*\* | `%QX0.0` | `SHRED\_FWD\_RUN` | `BOOL (0/1)` | Primary shredder forward contactor |

| \*\*Coil 00002\*\* | `%QX0.1` | `SHRED\_REV\_UNJAM` | `BOOL (0/1)` | 3.0 s auto-reverse unjamming cycle ($I > 12.5\\text{ A}$) |

| \*\*Coil 00004\*\* | `%QX0.3` | `HV\_CORONA\_ENABLE` | `BOOL (0/1)` | Hardware-interlocked ($\\omega\_{roll} > 30\\text{ RPM}$ \& door closed) |

| \*\*Input Reg 30001\*\* | `%IW0` | `BLADE\_HI\_SCALED` | `UINT16 (0–1000)` | Cutter Health Index ($HI\_{blade} \\times 1000$) |

| \*\*Input Reg 30002\*\* | `%IW1` | `MEAN\_PSD\_MICRONS` | `UINT16 (um)` | Soft-sensor mean particle diameter $\\bar{d}\_p$ |

| \*\*Holding Reg 40001\*\* | `%QW0` | `SET\_HM\_RPM` | `UINT16 (RPM)` | MO-PPO setpoint: Hammer Mill (1,900–2,900 RPM) |

| \*\*Holding Reg 40002\*\* | `%QW1` | `SET\_AIRFLOW\_CMH` | `UINT16 (m3/h)` | MO-PPO setpoint: Cyclone Blower (118–205 $\\text{m}^3/\\text{h}$) |

| \*\*Holding Reg 40003\*\* | `%QW2` | `SET\_CORONA\_KV10` | `UINT16 (0.1 kV)` | MO-PPO setpoint: Electrode Voltage (190–280) |

| \*\*Holding Reg 40004\*\* | `%QW3` | `SET\_ROLL\_RPM` | `UINT16 (RPM)` | MO-PPO setpoint: Grounded Drum (44–80 RPM) |



\---



\## 5. 500-kg Campaign Evaluation Results (100 Batches of 5.0 kg)



!\[Figure 3: Measured Copper Recovery Trajectory Across 500-kg WPCB Campaign](fig3\_recovery\_trajectory.svg)

\*Figure 3: Measured copper recovery retention across a 500-kg WPCB campaign (100 batches of 5.0 kg) as hammer-mill cutter health degrades from $HI\_{blade} = 1.00$ to $0.35$.\*



\### Table 2: Measured Digital Twin Benchmark Comparison (500-kg Campaign)



| Control Policy (500-kg Campaign) | Mean PSD $\\bar{d}\_p$ (mm) | Cu Grade $G\_{Cu}$ (%) | Cu Recovery $R\_{Cu}$ (%) | Specific Energy (kWh/kg) | Feeder Jams / Arcs |

| :--- | :--- | :--- | :--- | :--- | :--- |

| \*\*1. Static Open-Loop Setpoints\*\* | 0.518 mm | 94.61% | 81.94% | 0.342 kWh/kg | 12 Jams / 0 Arcs |

| \*\*2. RSM Box-Behnken + PID\*\* | 0.459 mm | 95.34% | 88.35% | 0.369 kWh/kg | 0 Jams / 0 Arcs |

| \*\*3. Shielded MO-PPO (Proposed)\*\* | \*\*0.395 mm\*\* | \*\*96.65%\*\* | \*\*94.71%\*\* | \*\*0.388 kWh/kg\*\* | \*\*0 Jams / 0 Arcs\*\* |



\---



\## 6. References

1\. Bond, F. C. (1952). The third theory of comminution. \*Transactions of AIME\*, 193, 484–494.

2\. Cui, J., \& Forssberg, E. (2003). Mechanical recycling of waste electric and electronic equipment: A review. \*Journal of Hazardous Materials\*, 99(3), 243–263.

3\. Lapple, C. E. (1951). Processes use many collector types. \*Chemical Engineering\*, 58(5), 144–151.

4\. Lu, H., Li, J., Guo, J., \& Xu, Z. (2008). Movement behavior of particles in a roll-type corona-electrostatic separator for recycling waste printed circuit boards. \*Journal of Materials Processing Technology\*, 197(1-3), 101–108.

5\. Pauthenier, M. M., \& Moreau-Hanot, M. (1932). La charge des particules sphériques dans un champ ionisé. \*Journal de Physique et le Radium\*, 3(12), 590–613.

6\. Raffin, A., Hill, A., Gleave, A., Kanervisto, A., Ernestus, M., \& Dormann, N. (2021). Stable-Baselines3: Reliable reinforcement learning implementations. \*Journal of Machine Learning Research\*, 22(268), 1–8.

7\. Schulman, J., Wolski, F., Dhariwal, P., Radford, A., \& Klimov, O. (2017). Proximal policy optimization algorithms. \*arXiv preprint arXiv:1707.06347\*.

8\. van Noortwijk, J. M. (2009). A survey of the application of gamma processes in maintenance. \*Reliability Engineering \& System Safety\*, 94(1), 2–21.

