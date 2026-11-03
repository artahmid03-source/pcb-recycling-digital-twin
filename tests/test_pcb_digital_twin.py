# File: tests/test_pcb_digital_twin.py
"""Automated unit and integration tests for the Waste-PCB Recycling Digital Twin."""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from run_pcb_digital_twin import (
    OpenPLCSafetyShield,
    PCBRecyclingEnv,
    PlantConfig,
    run_benchmark_campaign,
)


def test_plant_physical_constants():
    """Verifies report geometry and material parameters."""
    cfg = PlantConfig()
    assert cfg.envelope_mm == (880, 450, 580)
    assert cfg.feed_cu_mass_frac == 0.28
    assert cfg.feed_fr4_mass_frac == 0.72
    assert cfg.d_lib_mm == 0.65
    assert cfg.bond_work_index_kwh_t == 16.4
    assert cfg.cyclone_inlet_b_m == 0.045
    assert cfg.roll_radius_m == 0.090
    assert cfg.corona_gap_m == 0.050


def test_openplc_safety_interlocks():
    """Verifies 3-second shredder reverse above 12.5 A and HV gate interlocks."""
    shield = OpenPLCSafetyShield()

    # Over-current jam (> 12.5 A) must trigger 3.0 s auto-reverse
    res_jam = shield.evaluate_interlocks(
        shredder_current_a=13.2,
        enclosure_closed=True,
        hm_rpm=2400.0,
        air_flow_m3s=0.045,
        voltage_kv=24.0,
        roll_rpm=60.0,
        blade_hi=0.80,
        mean_dp_mm=0.55,
    )
    assert res_jam["jam_triggered"] is True
    assert res_jam["reverse_timer_s"] == 3.0
    assert shield.coils["00002_SHRED_REV_UNJAM"] is True

    # Roll speed <= 30 RPM or open enclosure must cut HV corona voltage to 0 kV
    res_low_rpm = shield.evaluate_interlocks(
        shredder_current_a=9.5,
        enclosure_closed=True,
        hm_rpm=2400.0,
        air_flow_m3s=0.045,
        voltage_kv=25.0,
        roll_rpm=28.0,
        blade_hi=0.90,
        mean_dp_mm=0.38,
    )
    assert res_low_rpm["hv_enabled"] is False
    assert res_low_rpm["effective_voltage_kv"] == 0.0


def test_gymnasium_environment_step_and_wear():
    """Verifies 6D state space, 4D action space, and monotonic cutter degradation."""
    env = PCBRecyclingEnv(seed=42)
    obs, _ = env.reset(seed=42)
    assert obs.shape == (6,)
    assert np.isclose(obs[0], 1.00)

    next_obs, reward, terminated, truncated, info = env.step(np.array([0.0, 0.0, 0.0, 0.0]))
    assert next_obs.shape == (6,)
    assert isinstance(reward, float)
    assert terminated is False
    assert truncated is False
    assert info["blade_hi"] < 1.00


def test_benchmark_campaign_ordering(tmp_path):
    """Verifies that Shielded MO-PPO outperforms RSM+PID and Static Open-Loop over 100 batches."""
    summary = run_benchmark_campaign(output_dir=str(tmp_path))
    by_policy = {row["policy_mode"]: row for row in summary}

    static_rec = by_policy["Static_Open_Loop"]["cu_recovery_pct"]
    rsm_rec = by_policy["RSM_PID"]["cu_recovery_pct"]
    moppo_rec = by_policy["Shielded_MO_PPO"]["cu_recovery_pct"]

    assert moppo_rec > rsm_rec > static_rec
    assert by_policy["Shielded_MO_PPO"]["jams"] == 0
    assert by_policy["Shielded_MO_PPO"]["arcs"] == 0