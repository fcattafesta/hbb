from args_analysis import args
from btagging_sys import *
from regions import regionsMu, regionsEl

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
    "number_of_events",
]

if args.train:
    histosMC = histosData

    ### Dictionary of histograms per selection ###
    histosPerSelectionMuonMC = {"SR_mm": histosMC}
    histosPerSelectionElectronMC = {"SR_ee": histosMC}

    histosPerSelectionMuonData = {"SR_mm": histosData}
    histosPerSelectionElectronData = {"SR_ee": histosData}

else:
    histosData += [
        "Jet_pt",
        "Jet_pt_jerNom",
    ]

    if args.eval_model:
        histosData.append("DNN_Score")
        histosData.append("atanhDNN_Score")

    histosMC = histosData + [
        #"GenJet_pt",
        "hadronFlavour_btag_max",
        "hadronFlavour_btag_min",
        #"LHE_Nb",
        #"genWeight",
        "SelectedJet_hadronFlavour",
        "SelectedJet_btagDeepFlavB" if args.btag=="deepflav" else "SelectedJet_btagDeepB",
    ]

    #if args.sf_only:
         #histosMC += ["btagWeightCentral"]
         #histosMC += btag_sys
         #histosMC += jet_btag_sys + ["SelectedJet_btagWeight_central"]
    #     histosMC += [
    #         "Jet_pt_jerUp",
    #         "Jet_pt_jerDown",
    #         "Jet_jerNomSF",
    #         "Jet_jerUpSF",
    #         "Jet_jerDownSF",
    #     ]

    ### Dictionary of histograms per selection ###
    histosPerSelectionMuonMC = {sel: histosMC for sel in regionsMu}
    histosPerSelectionElectronMC = {sel: histosMC for sel in regionsEl}

    histosPerSelectionMuonData = {sel: histosData for sel in regionsMu}
    histosPerSelectionElectronData = {sel: histosData for sel in regionsEl}
