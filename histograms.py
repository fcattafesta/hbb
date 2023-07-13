from args_analysis import args
from btagging_sys import *
from selections import selsMu, selsEle

### List of histograms to be plotted ###
histosData = [
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
]
histosData += [
    "GenJet_pt",
    "Jet_pt",
    "Jet_pt_Nom",
]

if args.eval_model:
    histosData.append("DNN_Score")
    histosData.append("atanhDNN_Score")

histosMC = histosData + ["hadronFlavour_btag_max", "hadronFlavour_btag_min", "LHE_Nb", "genWeight", "Jet_hadronFlavour"]
if args.sf:
    histosMC += ["btagWeightCentral"]
    histosMC += btag_sys
    histosMC += jet_btag_sys + ["Jet_btagWeight_central"]
    histosMC += [
        "Jet_pt_jerUp",
        "Jet_pt_jerDown",
        "Jet_jerNomSF",
        "Jet_jerUpSF",
        "Jet_jerDownSF",
    ]


### Dictionary of histograms per selection ###
histosPerSelectionMuonMC = {sel: histosMC for sel in selsMu}
histosPerSelectionElectronMC = {sel: histosMC for sel in selsEle}

histosPerSelectionElectronData = {sel: histosData for sel in selsEle}
histosPerSelectionMuonData = {sel: histosData for sel in selsMu}
