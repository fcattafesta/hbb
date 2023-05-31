labelRegion_ = {
    "SR_ee": "Signal Region Electrons",
    "CR_Zee_bjets": "Z+bjets Region Electrons",
    "CR_Zee_lightjets": "Z+lightjets Region Electrons",
    "CR_ee_ttbar": "t#bar{t} Region Electrons",
    "SR_mm": "Signal Region Muons",
    "CR_Zmm_bjets": "Z+bjets Region Muons",
    "CR_Zmm_lightjets": "Z+lightjets Region Muons",
    "CR_mm_ttbar": "t#bar{t} Region Muons",
}

labelRegionDeepFlav = {}
for key in labelRegion_.keys():
    labelRegionDeepFlav[key] = labelRegion_[key] + " DeepFlav"

labelRegionDeepCSV = {}
for key in labelRegion_.keys():
    labelRegionDeepCSV[key] = labelRegion_[key] + " DeepCSV"


labelVariable = {
    "Zee_mass": "m_{ee}",
    "Zmm_mass": "m_{#mu#mu}",
    "Z_mass": "m_{ll}",
    "Zee_pt": "p_{T}(ee)",
    "Zmm_pt": "p_{T}(#mu#mu)",
    "Z_pt": "p_{T}(ll)",
    "Dijets_mass": "m_{jj}",
    "Dijets_pt": "p_{T}(jj)",
    "MET_pt": "p_{T}^{miss}",
    "ZH_dphi": "#Delta#phi(Z,jj)",
    "ZH_deta": "#Delta#eta(Z,jj)",
    "ZH_dr": "#DeltaR(Z,jj)",
    "HZ_ptRatio": "p_{T}(jj)/p_{T}(Z)",
    "btag_max": "btag_{max}",
    "btag_min": "btag_{min}",
    "jj_dphi": "#Delta#phi(jj)",
    "jj_deta": "#Delta#eta(jj)",
    "jj_dr": "#DeltaR(jj)",
    "JetBtagMax_pt": "p_{T}^{max}",
    "JetBtagMin_pt": "p_{T}^{min}",
    "SoftActivityJetNjets5": "N_{jets}^{soft} (p_{T} > 5 GeV)",
}

labelLegend = {
    "ZH": "ZH(b#bar{b})",
    "ggZH": "ggZH(b#bar{b})",
    "TT": "t#bar{t}",
    "ST": "Single top",
    "Z+udsg": "Z+udsg",
    "Z+b": "Z+b",
    "Z+bb": "Z+b#bar{b}",
    "Z+c": "Z+c",
    "VVHF": "VVHF",
    "VVLF": "VVLF",
}
