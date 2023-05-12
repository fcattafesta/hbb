from nail.nail import *


def getFlowCommon(flow):
    ### Common preselections for leptons ###
    ## Muons ##
    flow.Define("Muon_iso", "(Muon_pfRelIso04_all)")
    # NOTE: Multiple Muon Id (loose, tight) for differnet purposes, isolation 0.06
    flow.SubCollection(
        "SelectedMuon",
        "Muon",
        sel="Muon_iso < 0.06 && Muon_mediumId && Muon_pt > 20. && abs(Muon_eta) < 2.4 && Muon_dxy < 0.5 && Muon_dz < 0.1",
    )

    ## Electrons ##
    flow.Define("Electron_iso", "(Electron_pfRelIso03_all)")
    flow.SubCollection(
        "SelectedElectron",
        "Electron",
        sel="Electron_iso < 0.06 && Electron_mvaFall17V2Iso_WP90 && abs(Electron_eta) < 2.4 && Electron_dxy < 0.05 && Electron_dz < 0.2",
    )

    ### Preselction for Jets ###
    # NOTE: JEC?
    # NOTE: FSR, PUId=0, JET_pt=30
    flow.MatchDeltaR("SelectedElectron", "Jet")
    flow.MatchDeltaR("SelectedMuon", "Jet")
    flow.SubCollection(
        "CleanJet",
        "Jet",
        sel="(Jet_SelectedElectronDr > 0.4 || Jet_SelectedElectronIdx==-1) && (Jet_SelectedMuonDr > 0.4 || Jet_SelectedMuonIdx==-1)",
    )
    flow.SubCollection(
        "SelectedJet",
        "CleanJet",
        sel="CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5",
    )

    # B-tagging working points
    flow.Selection(
        "LeadingJetLoose", "SelectedJet_btagDeepB[0] > 0.1241", requires=["twoJets"]
    )
    flow.Selection(
        "LeadingJetMedium", "SelectedJet_btagDeepB[0] > 0.4184", requires=["twoJets"]
    )
    flow.Selection(
        "LeadingJetTight", "SelectedJet_btagDeepB[0] > 0.7527", requires=["twoJets"]
    )
    flow.Selection(
        "SubLeadingJetLoose", "SelectedJet_btagDeepB[1] > 0.1241", requires=["twoJets"]
    )

    # B-tagging distributions for LeadingJet and SubLeadingJet
    flow.Define(
        "btag_max",
        "int((SelectedJet_btagDeepB[0] > 0.7527)) + int((SelectedJet_btagDeepB[0] > 0.4184)) + int((SelectedJet_btagDeepB[0] > 0.1241))",
    )
    flow.Define(
        "btag_min",
        "int((SelectedJet_btagDeepB[1] > 0.1241)) + int((SelectedJet_btagDeepB[1] > 0.4184)) + int((SelectedJet_btagDeepB[1] > 0.7527))",
    )
    # Pt distributions for LeadingJet and SubLeadingJet
    flow.Define("LeadingJet_pt", "SelectedJet_pt[0]")
    flow.Define("SubLeadingJet_pt", "SelectedJet_pt[1]")

    ### Dijet ###
    ## Jet pair selection ##
    flow.Selection("twoJets", "nSelectedJet >= 2")
    flow.Define("SelectedJet_p4", "@p4v(SelectedJet)")
    flow.Define("Dijets", "SelectedJet_p4[0]+SelectedJet_p4[1]", requires=["twoJets"])
    flow.Define("Dijets_mass", "Dijets.M()")
    flow.Define("Dijets_pt", "Dijets.Pt()")

    # Relative topological properties of the two jets
    flow.Define("jj_deta", "abs(SelectedJet_eta[0] - SelectedJet_eta[1])")
    flow.Define(
        "jj_dphi",
        "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(SelectedJet_p4[0], SelectedJet_p4[1]))",
    )
    flow.Define("jj_dr", "TMath::Sqrt(jj_deta*jj_deta + jj_dphi*jj_dphi)")

    return flow
