from nail.nail import *


def getFlowCommon(flow, btag):
    ### Common preselections for leptons ###
    ## Muons ##
    flow.Define("Muon_iso", "(Muon_pfRelIso04_all)")
    # NOTE: Multiple Muon Id (loose, tight) for differnet purposes, isolation 0.06
    flow.SubCollection(
        "SelectedMuon",
        "Muon",
        sel="Muon_iso < 0.06 && Muon_looseId && Muon_pt > 20. && abs(Muon_eta) < 2.4 && Muon_dxy < 0.5 && Muon_dz < 0.1",
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
    # NOTE: FSR, JET_pt=30
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
        sel="CleanJet_pt_Nom > 30. && abs(CleanJet_eta) < 2.5 && CleanJet_jetId > 0 && CleanJet_puId > 0",
    )

    flow.Define("event_unsigned_long", "(unsigned long)event)")
    flow.Selection("twoJets", "nSelectedJet >= 2 && event_unsigned_long == 80119208")

    # Define LeadingJet and SubLeadingJet
    flow.Define("SelectedJetPtOrderIndices", "Argsort(-SelectedJet_pt_Nom)")
    flow.ObjectAt(
        "LeadingJet",
        "SelectedJet",
        "At(SelectedJetPtOrderIndices,0)",
        requires=["twoJets"],
    )

    flow.ObjectAt(
        "SubLeadingJet",
        "SelectedJet",
        "At(SelectedJetPtOrderIndices,1)",
        requires=["twoJets"],
    )

    # Define p4
    flow.Define(
        "SelectedJet_p4",
        "vector_map_t<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> >        >(SelectedJet_pt_Nom , SelectedJet_eta, SelectedJet_phi, SelectedJet_mass)",
    )
    # flow.Define("SelectedJet_p4", "@p4v(SelectedJet)")

    btag_score = "btagDeepFlavB" if btag == "deepflav" else "btagDeepB"

    # Order by btag score
    flow.Define("SelectedJetBTagOrderIndices", "Argsort(-SelectedJet_%s)" % btag_score)
    flow.ObjectAt(
        "JetBtagMax",
        "SelectedJet",
        "At(SelectedJetBTagOrderIndices,0)",
        requires=["twoJets"],
    )
    flow.ObjectAt(
        "JetBtagMin",
        "SelectedJet",
        "At(SelectedJetBTagOrderIndices,1)",
        requires=["twoJets"],
    )

    ### Dijet ###
    ## Jet pair selection ##
    flow.Define("Dijets", "JetBtagMax_p4+JetBtagMin_p4")
    flow.Define("Dijets_mass", "Dijets.M()")
    flow.Define("Dijets_pt", "Dijets.Pt()")

    # Relative topological properties of the two jets
    flow.Define("jj_deta", "abs(JetBtagMax_eta - JetBtagMin_eta)")
    flow.Define(
        "jj_dphi",
        "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(JetBtagMax_p4, JetBtagMin_p4))",
    )
    flow.Define("jj_dr", "TMath::Sqrt(jj_deta*jj_deta + jj_dphi*jj_dphi)")

    btag_wp = (
        [0.0490, 0.2783, 0.7100] if btag == "deepflav" else [0.1208, 0.4168, 0.7665]
    )

    # B-tagging working points
    flow.Selection("JetBtagMaxLoose", "JetBtagMax_%s > %f" % (btag_score, btag_wp[0]))
    flow.Selection("JetBtagMaxMedium", "JetBtagMax_%s > %f" % (btag_score, btag_wp[1]))
    flow.Selection("JetBtagMaxTight", "JetBtagMax_%s > %f" % (btag_score, btag_wp[2]))
    flow.Selection("JetBtagMinLoose", "JetBtagMin_%s > %f" % (btag_score, btag_wp[0]))

    # B-tagging distributions for JetBtagMax and JetBtagMin
    flow.Define(
        "btag_max",
        "JetBtagMax_%s" % btag_score,
    )
    flow.Define(
        "btag_min",
        "JetBtagMin_%s" % btag_score,
    )

    return flow
