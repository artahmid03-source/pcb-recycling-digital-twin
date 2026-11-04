(* =========================================================================
   FILE: plc/pcb_safety_interlocks.st
   TARGET: OpenPLC Runtime v3 (Modbus TCP Server Port 502)
   STANDARD: IEC 61131-3 Structured Text / Ladder Equivalent
   PROJECT: 5-Stage Waste-PCB Recycling Digital Twin Safety Shield
   ========================================================================= *)

PROGRAM PCB_Safety_Supervisor
VAR
    (* Physical Digital Inputs & Outputs Mapped to Modbus Coils *)
    ENCLOSURE_CLOSED_IX0_1  AT %IX0.1 : BOOL := TRUE;   (* Safety door limit switch *)
    SHRED_FWD_RUN_QX0_0     AT %QX0.0 : BOOL := TRUE;   (* Coil 00001: Shredder forward contactor *)
    SHRED_REV_UNJAM_QX0_1   AT %QX0.1 : BOOL := FALSE;  (* Coil 00002: 3.0 s auto-reverse contactor *)
    HV_CORONA_ENABLE_QX0_3  AT %QX0.3 : BOOL := FALSE;  (* Coil 00004: 28 kV HV supply enable *)

    (* Analog Input Registers (30001 - 30004) *)
    BLADE_HI_SCALED_IW0     AT %IW0   : UINT := 1000;   (* Input Reg 30001: HI_blade x 1000 *)
    MEAN_PSD_MICRONS_IW1    AT %IW1   : UINT := 380;    (* Input Reg 30002: Mean d_p in um *)
    SHRED_CURRENT_DA_IW2    AT %IW2   : UINT := 95;     (* Shredder motor current in 0.1 A (125 = 12.5 A) *)
    ACTUAL_ROLL_RPM_IW3     AT %IW3   : UINT := 58;     (* Measured grounded drum speed in RPM *)

    (* Holding Registers Written by Shielded MO-PPO Agent (40001 - 40004) *)
    SET_HM_RPM_QW0          AT %QW0   : UINT := 2400;   (* Holding Reg 40001: Hammer Mill RPM [1800-3000] *)
    SET_AIRFLOW_CMH_QW1     AT %QW1   : UINT := 162;    (* Holding Reg 40002: Cyclone Blower [100-240 m3/h] *)
    SET_CORONA_KV10_QW2     AT %QW2   : UINT := 235;    (* Holding Reg 40003: Corona Voltage [180-280 (0.1 kV)] *)
    SET_ROLL_RPM_QW3        AT %QW3   : UINT := 58;     (* Holding Reg 40004: Grounded Drum [40-95 RPM] *)

    (* IEC 61131-3 Standard Timer Function Block for 3.0-Second Auto-Reverse *)
    TON_REV : TON;
    OVERCURRENT_LATCH : BOOL := FALSE;
END_VAR

(* -------------------------------------------------------------------------
   RUNG 1: Shredder Over-Torque Auto-Reverse (I_shred > 12.5 A triggers 3.0 s reverse)
   ------------------------------------------------------------------------- *)
IF SHRED_CURRENT_DA_IW2 > 125 THEN
    OVERCURRENT_LATCH := TRUE;
END_IF;

TON_REV(IN := OVERCURRENT_LATCH, PT := T#3000ms);

IF OVERCURRENT_LATCH AND NOT TON_REV.Q THEN
    SHRED_FWD_RUN_QX0_0   := FALSE;
    SHRED_REV_UNJAM_QX0_1 := TRUE;
ELSIF TON_REV.Q THEN
    OVERCURRENT_LATCH     := FALSE;
    SHRED_REV_UNJAM_QX0_1 := FALSE;
    SHRED_FWD_RUN_QX0_0   := TRUE;
ELSE
    SHRED_FWD_RUN_QX0_0   := TRUE;
    SHRED_REV_UNJAM_QX0_1 := FALSE;
END_IF;

(* -------------------------------------------------------------------------
   RUNG 2: High-Voltage Corona Interlock (Enclosure Closed AND Roll > 30 RPM)
   ------------------------------------------------------------------------- *)
IF ENCLOSURE_CLOSED_IX0_1 AND (ACTUAL_ROLL_RPM_IW3 > 30) THEN
    HV_CORONA_ENABLE_QX0_3 := TRUE;
ELSE
    HV_CORONA_ENABLE_QX0_3 := FALSE;
    SET_CORONA_KV10_QW2    := 0;
END_IF;

END_PROGRAM

CONFIGURATION Config0
    RESOURCE Res0 ON PLC
        TASK MainTask(INTERVAL := T#50ms, PRIORITY := 0);
        PROGRAM Inst0 WITH MainTask : PCB_Safety_Supervisor;
    END_RESOURCE
END_CONFIGURATION
