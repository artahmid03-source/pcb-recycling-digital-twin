# File: src/cad_mass_properties.py
"""
Analytical CAD Mass Properties & Inertia Extraction Module
Computes structural mass, center of gravity, rotor moments of inertia,
and natural frequencies for the 880 x 450 x 580 mm Tabletop PCB Recycling Line.
"""

import math

def compute_analytical_assembly_properties():
    # 1. Structural Frame Envelope (Mild Steel Structural Tubing 25x25x2 mm)
    L, W, H = 0.88, 0.45, 0.58  # meters
    steel_density = 7850.0       # kg/m^3
    tube_od, tube_t = 0.025, 0.002
    cross_section_area = 4.0 * tube_t * (tube_od - tube_t)
    total_frame_length = 4.0 * (L + W + H)
    frame_mass = total_frame_length * cross_section_area * steel_density

    # 2. Subassembly Mass Breakdown
    shredder_mass = 14.5   # Dual-shaft shear shredder module (kg)
    hammer_mill_mass = 12.0 # High-speed hammer mill & sieve (kg)
    cyclone_mass = 6.2     # Lapple air cyclone classifier (kg)
    electrostatic_mass = 9.8 # Corona roll separator & electrodes (kg)
    enclosure_bins_mass = 8.5 # Bins, ducting, and safety shielding (kg)

    total_assembly_mass = (
        frame_mass + shredder_mass + hammer_mill_mass + 
        cyclone_mass + electrostatic_mass + enclosure_bins_mass
    )

    # 3. Rotor Axial Mass Moment of Inertia (J_rotor) for Hammer Mill (Solid Steel Cylinder approximation)
    r_rotor = 0.075  # radius 75 mm
    l_rotor = 0.350  # length 350 mm
    m_rotor = 7.8    # rotor mass kg
    j_rotor = 0.5 * m_rotor * (r_rotor ** 2)

    # 4. First-Mode Natural Frequency Estimation (Cantilevered Frame Beam approximation)
    # Equivalent stiffness k_frame derived from mild-steel structural members
    young_modulus = 200e9  # Pa (Steel)
    moment_inertia_beam = (math.pi / 4.0) * ((tube_od/2)**4 - ((tube_od/2)-tube_t)**4)
    k_equivalent = (3.0 * young_modulus * moment_inertia_beam) / ((L / 2.0) ** 3) * 4.0
    natural_freq_hz = (1.0 / (2.0 * math.pi)) * math.sqrt(k_equivalent / total_assembly_mass)

    print("=== ANALYTICAL CAD & MASS PROPERTIES REPORT ===")
    print(f"Structural Envelope Dimensions : {L*1000:.0f} x {W*1000:.0f} x {H*1000:.0f} mm")
    print(f"Welded Steel Frame Mass      : {frame_mass:.2f} kg")
    print(f"Total Assembly Dry Mass      : {total_assembly_mass:.2f} kg")
    print(f"Hammer-Mill Rotor Inertia J  : {j_rotor:.5f} kg*m^2")
    print(f"Estimated 1st Natural Freq   : {natural_freq_hz:.2f} Hz")
    print("================================================")

if __name__ == "__main__":
    compute_analytical_assembly_properties()