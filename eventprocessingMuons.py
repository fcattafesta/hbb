from nail.nail import *
import ROOT
import sys
import copy


def getFlowMuons(flow):
    ### Analysis for muons ###

    ## Muon pair selection ##
    flow.Selection("twoMuons", "nSelectedMuon==2")
    flow.Define("SelectedMuon_p4", "@p4v(SelectedMuon)")
    flow.Distinct("MuMu", "SelectedMuon")
    flow.Define(
        "OppositeSignMuMu",
        "Nonzero(MuMu0_charge != MuMu1_charge)",
        requires=["twoMuons"],
    )
    flow.Selection("twoOppositeSignMuons", "OppositeSignMuMu.size() > 0")
    flow.TakePair(
        "Mu",
        "SelectedMuon",
        "MuMu",
        "At(OppositeSignMuMu,0,-200)",
        requires=["twoOppositeSignMuons"],
    )
    flow.Selection("PtSelMu", "Mu0_pt > 25 && Mu1_pt > 15")

    ### Z boson from muons ###
    flow.Define("Z", "Mu0_p4+Mu1_p4", requires=["PtSelMu"])
    flow.Define("Z_pt", "Z.Pt()", requires=["PtSelMu"])
    flow.Define("Z_mass", "Z.M()", requires=["PtSelMu"])

    # Relative kinematic and topological properties bewtween Z and Dijet
    flow.Define("ZH_dphi", "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(Z, Dijets))")
    flow.Define("ZH_deta", "TMath::Abs(Z.Eta() - Dijets.Eta())")
    flow.Define("ZH_dr", "TMath::Sqrt(ZH_dphi*ZH_dphi + ZH_deta*ZH_deta)")
    flow.Define("HZ_ptRatio", "Dijets_pt/Z_pt")

    # Common pre-selection for signal and control regions
    flow.Selection("CommonSelMu", "Z_pt > 75 && Dijets_mass > 50")

    ### Signal regions ###
    flow.Selection(
        "SR_mm",
        "Z_mass >= 75 && Z_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && JetBtagMaxMedium && JetBtagMaxLoose",
        requires=["CommonSelMu"],
    )

    ### Control regions ###
    ## Z+bjets ##
    flow.Selection(
        "CR_Zmm_bjets",
        "Z_mass >= 85 && Z_mass <= 97 && (Dijets_mass < 90 || Dijets_mass > 150) && MET_pt < 60 && JetBtagMaxMedium && JetBtagMinLoose && ZH_dphi > 2.5",
        requires=["CommonSelMu"],
    )
    ## Z+light jets ##
    # Muons
    flow.Selection(
        "CR_Zmm_lightjets",
        "Z_mass >= 75 && Z_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && !JetBtagMaxLoose && !JetBtagMinLoose && ZH_dphi > 2.5",
        requires=["CommonSelMu"],
    )
    ## ttbar ##
    # Muons
    flow.Selection(
        "CR_mm_ttbar",
        "((Z_mass >= 10 && Z_mass <= 75)  || Z_mass > 120) && JetBtagMaxTight && JetBtagMinLoose",
        requires=["CommonSelMu"],
    )

    return flow
