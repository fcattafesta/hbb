### List of histograms to be plotted ###
histos = [
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
    "JetBtagMax_pt",
    "JetBtagMin_pt",
    "SoftActivityJetNjets5",
    "DNN_Score"
]

### List of selections for muons and electrons ###
selsMu = ["SR_mm", "CR_Zmm_bjets", "CR_Zmm_lightjets", "CR_mm_ttbar"]
selsEle = ["SR_ee", "CR_Zee_bjets", "CR_Zee_lightjets", "CR_ee_ttbar"]

### Dictionary of histograms per selection ###
histosPerSelectionMuon = {sel: histos for sel in selsMu}
histosPerSelectionElectron = {sel: histos for sel in selsEle}
