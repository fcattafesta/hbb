from nail.nail import *


def getFlowElectrons(flow):
    ### Analysis for electrons ###

    ## Electron pair selection ##
    flow.Selection("twoElectrons", "nSelectedElectron==2")
    flow.Define("SelectedElectron_p4", "@p4v(SelectedElectron)")
    flow.Distinct("ElEl", "SelectedElectron")
    flow.Define(
        "OppositeSignElEl",
        "Nonzero(ElEl0_charge != ElEl1_charge)",
        requires=["twoElectrons"],
    )
    flow.Selection("twoOppositeSignElectrons", "OppositeSignElEl.size() > 0")
    flow.TakePair(
        "El",
        "SelectedElectron",
        "ElEl",
        "At(OppositeSignElEl,0,-200)",
        requires=["twoOppositeSignElectrons"],
    )
    flow.Selection("PtSelEl", "El0_pt > 25 && El1_pt > 17")

    ### Z boson from electrons ###
    flow.Define("Z", "El0_p4+El1_p4", requires=["PtSelEl"])
    flow.Define("Z_pt", "Z.Pt()", requires=["PtSelEl"])
    flow.Define("Z_mass", "Z.M()", requires=["PtSelEl"])

    # Relative kinematic and topological properties bewtween Z and Dijet
    flow.Define("ZH_dphi", "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(Z, Dijets))")
    flow.Define("ZH_deta", "TMath::Abs(Z.Eta() - Dijets.Eta())")
    flow.Define("ZH_dr", "TMath::Sqrt(ZH_dphi*ZH_dphi + ZH_deta*ZH_deta)")
    flow.Define("HZ_ptRatio", "Dijets_pt/Z_pt")

    # Common pre-selection for signal and control regions
    flow.Selection("CommonSelEle", "Z_pt > 75 && Dijets_mass > 50")

    ### Signal regions ###
    flow.Selection(
        "SR_ee",
        "Z_mass >= 75 && Z_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && JetBtagMaxMedium && JetBtagMinLoose",
        requires=["CommonSelEle"],
    )

    ### Control regions ###
    ## Z+bjets  ##
    flow.Selection(
        "CR_Zee_bjets",
        "Z_mass >= 85 && Z_mass <= 97 && (Dijets_mass < 90 || Dijets_mass > 150) && MET_pt < 60 && JetBtagMaxMedium && JetBtagMinLoose && ZH_dphi > 2.5",
        requires=["CommonSelEle"],
    )

    ## Z+light jets ##
    flow.Selection(
        "CR_Zee_lightjets",
        "Z_mass >= 75 && Z_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && !JetBtagMaxLoose && !JetBtagMinLoose && ZH_dphi > 2.5",
        requires=["CommonSelEle"],
    )

    ## ttbar ##
    flow.Selection(
        "CR_ee_ttbar",
        "((Z_mass >= 10 && Z_mass <= 75)  || Z_mass > 120) && JetBtagMaxTight && JetBtagMinLoose",
        requires=["CommonSelEle"],
    )

    return flow
