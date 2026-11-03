\# Multi-Physics Digital Twin and Deep Reinforcement Learning Control of a Compact Mechanical-Electrostatic Waste PCB Recycling Line



\*\*Author:\*\* Arifur Rahman Tahmid  

\*\*Affiliation:\*\* Department of Mechanical and Production Engineering (MPE), Islamic University of Technology (IUT)  

\*\*Contact:\*\* artahmid03@gmail.com  



> \*\*PUBLICATION HOLD NOTICE:\*\* Figure 3 and nine benchmark entries in Table 1 below contain blueprint placeholders alongside baseline Python simulation measurements. Do not submit this manuscript as final until all `\[PLACEHOLDER — REPLACE BEFORE FINAL PUBLICATION]` items are replaced with locked experimental/validated campaign values.



\## 1. Abstract \& Research Novelty

Dry mechanical-physical separation recovers high-purity copper (Cu) from Waste Printed Circuit Boards (WPCBs: 28% Cu, $\\rho\_{Cu}=8,960\\text{ kg/m}^3$; 72% FR-4 fiberglass, $\\rho\_{FR4}=1,850\\text{ kg/m}^3$) without acid smelting or cyanide leaching (Cui \& Forssberg, 2003). In a compact $880 \\times 450 \\times 580\\text{ mm}$ five-stage line, progressive cutter wear shifts crushed particle size distribution (PSD) above the $0.65\\text{ mm}$ copper delamination threshold, clogging the feeder and reducing copper recovery by over 18%. We present a closed-loop Multi-Physics Digital Twin coupling Bond comminution ($W\_i = 16.4\\text{ kWh/t}$; Bond, 1952), Gamma blade degradation (van Noortwijk, 2009), Lapple cyclone classification ($B\_c = 45\\text{ mm}$; Lapple, 1951), and Pauthenier-ballistic corona electrostatic separation ($R\_{roll} = 90\\text{ mm}$, $L\_{gap} = 50\\text{ mm}$; Pauthenier \& Moreau-Hanot, 1932; Lu et al., 2008) under an IEC 61131-3 safety-shielded Multi-Objective PPO supervisor (Schulman et al., 2017; Raffin et al., 2021).



\## 2. Cyber-Physical Safety Shield \& Control Formulation

The OpenPLC safety layer enforces two deterministic hardware interlocks:

1\. \*\*Shredder Over-Torque Auto-Reverse (`%QX0.1`):\*\* Triggers a 3.0-second reverse unjamming cycle (`TON\_REV`) whenever shredder motor current exceeds $12.5\\text{ A}$.

2\. \*\*High-Voltage Corona Gate (`%QX0.3`):\*\* Energizes the $18\\text{--}28\\text{ kV}$ electrode only when enclosure interlock `%IX0.1 == TRUE` and grounded roll speed exceeds $30\\text{ RPM}$.



At each 5-kg batch step $k$, the MO-PPO agent observes $s\_k = \[HI\_{blade}, \\bar{d}\_p, L\_{sieve}, w\_1, w\_2, w\_3]^T$ with weights $\[0.45, 0.40, 0.15]$ and adjusts $a\_k = (\\Omega\_{hm}, Q\_{air}, U\_{kV}, \\omega\_{roll})$.



\## 3. 500-kg Campaign Evaluation \& Flagged Placeholders



\- \*\*Figure 3 Trajectory Data (`results/telemetry\_stream.csv`):\*\* `\[PLACEHOLDER — REPLACE BEFORE FINAL PUBLICATION]` Plot copper recovery across $0\\text{ kg}$ ($HI=1.00$), $125\\text{ kg}$ ($HI=0.84$), $250\\text{ kg}$ ($HI=0.68$), $375\\text{ kg}$ ($HI=0.51$), and $500\\text{ kg}$ ($HI=0.35$) from `results/telemetry\_stream.csv`.



| Control Policy (500-kg Campaign) | Mean PSD (mm) | Cu Grade (%) | Cu Recovery (%) | Specific Energy (kWh/kg) | Feeder Jams / Arcs |

| :--- | :--- | :--- | :--- | :--- | :--- |

| 1. Static Open-Loop Setpoints | 0.58 mm `\[PLACEHOLDER]` (Sim: 0.518 mm) | 89.4% `\[PLACEHOLDER]` (Sim: 94.61%) | 82.1% `\[PLACEHOLDER]` (Sim: 81.94%) | 0.34 kWh/kg (Sim: 0.342) | 4 Jams / 1 Arc |

| 2. RSM Box-Behnken + PID | 0.49 mm `\[PLACEHOLDER]` (Sim: 0.459 mm) | 93.1% `\[PLACEHOLDER]` (Sim: 95.34%) | 87.4% `\[PLACEHOLDER]` (Sim: 88.35%) | 0.38 kWh/kg (Sim: 0.369) | 1 Jam / 0 Arcs |

| 3. Shielded MO-PPO (Proposed) | 0.39 mm `\[PLACEHOLDER]` (Sim: 0.395 mm) | 96.8% `\[PLACEHOLDER]` (Sim: 96.65%) | 94.8% `\[PLACEHOLDER]` (Sim: 94.71%) | 0.36 kWh/kg (Sim: 0.388) | 0 Jams / 0 Arcs |



\## 4. References

1\. Bond, F. C. (1952). The third theory of comminution. \*Transactions of AIME\*, 193, 484–494.

2\. Cui, J., \& Forssberg, E. (2003). Mechanical recycling of waste electric and electronic equipment: A review. \*Journal of Hazardous Materials\*, 99(3), 243–263.

3\. Lapple, C. E. (1951). Processes use many collector types. \*Chemical Engineering\*, 58(5), 144–151.

4\. Lu, H., Li, J., Guo, J., \& Xu, Z. (2008). Movement behavior of particles in a roll-type corona-electrostatic separator for recycling waste printed circuit boards. \*Journal of Materials Processing Technology\*, 197(1-3), 101–108.

5\. Pauthenier, M. M., \& Moreau-Hanot, M. (1932). La charge des particules sphériques dans un champ ionisé. \*Journal de Physique et le Radium\*, 3(12), 590–613.

6\. Raffin, A., et al. (2021). Stable-Baselines3: Reliable reinforcement learning implementations. \*Journal of Machine Learning Research\*, 22(268), 1–8.

7\. Schulman, J., et al. (2017). Proximal policy optimization algorithms. \*arXiv preprint arXiv:1707.06347\*.

8\. van Noortwijk, J. M. (2009). A survey of the application of gamma processes in maintenance. \*Reliability Engineering \& System Safety\*, 94(1), 2–21.

