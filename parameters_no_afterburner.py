#!/usr/bin/env python3
"""iEBE-MUSIC config for IP-Glasma + MUSIC without decays or UrQMD."""

control_dict = {}
ipglasma_dict = {}
kompost_dict = {}
mcglauber_dict = {}
music_dict = {}
iss_dict = {}
hadronic_afterburner_toolkit_dict = {}

control_dict.update({
    "initial_state_type": "IPGlasma",
    "afterburner_type": "decay",
    "save_ipglasma_results": False,
    "save_kompost_results": False,
    "save_hydro_surfaces": False,
    "save_UrQMD_files": False,
    "compute_photon_emission": False,
    "compute_polarization": False,
})

ipglasma_dict.update({
    "type": "self",
    "QsmuRatio": 0.8,
    "maxtime": 0.4,
})

music_dict.update({
    "Initial_time_tau_0": 0.4,
    "use_eps_for_freeze_out": 0,
    "N_freeze_out": 1,
    "T_freeze": 0.150,
    "Include_Rhob_Yes_1_No_0": 0,
    "turn_on_baryon_diffusion": 0,
    "Viscosity_Flag_Yes_1_No_0": 1,
    "Include_Shear_Visc_Yes_1_No_0": 1,
    "T_dependent_Shear_to_S_ratio": 3,
    "shear_viscosity_3_eta_over_s_T_kink_in_GeV": 0.180,
    "shear_viscosity_3_eta_over_s_low_T_slope_in_GeV": -0.50,
    "shear_viscosity_3_eta_over_s_high_T_slope_in_GeV": 0.50,
    "shear_viscosity_3_eta_over_s_at_kink": 0.10,
    "Include_Bulk_Visc_Yes_1_No_0": 1,
    "T_dependent_zeta_over_s": 10,
    "bulk_viscosity_10_max": 0.050,
    "bulk_viscosity_10_width_low": 0.015,
    "bulk_viscosity_10_width_high": 0.100,
    "bulk_viscosity_10_T_peak": 0.170,
})
