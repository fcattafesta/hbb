histos = (
    [
        "Z_mass",
        "Z_pt",
        "Dijets_mass",
        "Dijets_pt",
        "MET_pt",
        "ZH_dphi",
        "ZH_deta",
        "ZH_dr",
        "HZ_ptRatio",
        "btag_max",
        "btag_min",
        "jj_dphi",
        "jj_deta",
        "jj_dr",
        "LeadingJet_pt",
        "SubLeadingJet_pt",
        "SoftActivityJetNjets5",
    ],
)
sels = ["SR", "CR_Z_bjets", "CR_Z_lightjets", "CR_ttbar"]

histosPerSelection = {sel: histos for sel in sels}


# histosPerSelection = {
#     # Electrons
#     # "SR_ee": ["Zee_mass", "Dijets_mass"],
#     # "CR_Zee_bjets": ["Zee_mass", "Dijets_mass", "Zee_pt"],
#     # "CR_Zee_lightjets": ["Zee_mass", "Dijets_mass", "Zee_pt"],
#     # "CR_ee_ttbar": ["Zee_mass", "Dijets_mass", "Zee_pt"],
#     # Muons
#     # "CR_Zmm_bjets": ["Zmm_mass", "Dijets_mass", "Zmm_pt"],
#     # "SR_mm": ["Zmm_mass", "Dijets_mass", "Zmm_pt"],
#     # "CR_Zmm_lightjets": ["Zmm_mass", "Dijets_mass", "Zmm_pt"],
#     # "CR_mm_ttbar": ["Zmm_mass", "Dijets_mass", "Zmm_pt"],
#     # Combined
#     "SR": ["Z_mass", "Z_pt", "Dijets_mass", "Dijets_pt"],
#     "CR_Z_bjets": ["Z_mass", "Z_pt", "Dijets_mass", "Dijets_pt"],
#     "CR_Z_lightjets": ["Z_mass", "Z_pt", "Dijets_mass", "Dijets_pt"],
#     "CR_ttbar": ["Z_mass", "Z_pt", "Dijets_mass", "Dijets_pt"],
# }
