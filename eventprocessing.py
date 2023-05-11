from nail.nail import *
import ROOT
import sys
import copy


def getFlow():
    # Start flow definition
    flow = SampleProcessing(
        "Analysis", "/scratchnvme/malucchi/1574B1FB-8C40-A24E-B059-59A80F397A0F.root"
    )

    ### Muons ###

    # Muon selection ID
    flow.Define("Muon_iso", "(Muon_pfRelIso04_all)")
    # NOTE: Multiple Muon Id (loose, tight) for differnet purposes, isolation 0.06
    flow.SubCollection(
        "SelectedMuon",
        "Muon",
        sel="Muon_iso < 0.06 && Muon_mediumId && Muon_pt > 20. && abs(Muon_eta) < 2.4 && Muon_dxy < 0.5 && Muon_dz < 0.1",
    )

    # Muon pair selection
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

    # Z boson from muons TODO: Maybe define Zmm only
    flow.Define("Zmm", "Mu0_p4+Mu1_p4", requires=["PtSelMu"])
    flow.Define("Zmm_pt", "Zmm.Pt()", requires=["PtSelMu"])
    flow.Define("Zmm_mass", "Zmm.M()", requires=["PtSelMu"])

    ### Electrons ###

    # Electron selection ID
    flow.Define("Electron_iso", "(Electron_pfRelIso03_all)")
    flow.SubCollection(
        "SelectedElectron",
        "Electron",
        sel="Electron_iso < 0.06 && Electron_mvaFall17V2Iso_WP90 && abs(Electron_eta) < 2.4 && Electron_dxy < 0.05 && Electron_dz < 0.2",
    )

    # Electron pair selection
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

    # Z boson from electrons TODO: Maybe define Zee only
    flow.Define("Zee", "El0_p4+El1_p4", requires=["PtSelEl"])
    flow.Define("Zee_pt", "Zee.Pt()", requires=["PtSelEl"])
    flow.Define("Zee_mass", "Zee.M()", requires=["PtSelEl"])

    ### Jets ###

    # Jet selection
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

    # Jet pair selection for dijet
    flow.Selection("twoJets", "nSelectedJet >= 2")
    flow.Define("SelectedJet_p4", "@p4v(SelectedJet)")
    flow.Define("Dijets", "SelectedJet_p4[0]+SelectedJet_p4[1]", requires=["twoJets"])
    flow.Define("Dijets_mass", "Dijets.M()")
    flow.Define("Dijets_pt", "Dijets.Pt()")

    # jet variables
    flow.Define(
        "btag_max",
        "int((SelectedJet_btagDeepB[0] > 0.7527)) + int((SelectedJet_btagDeepB[0] > 0.4184)) + int((SelectedJet_btagDeepB[0] > 0.1241))",
    )
    flow.Define(
        "btag_min",
        "int((SelectedJet_btagDeepB[1] > 0.1241)) + int((SelectedJet_btagDeepB[1] > 0.4184)) + int((SelectedJet_btagDeepB[1] > 0.7527))",
    )
    flow.Define("jj_deta", "abs(SelectedJet_eta[0] - SelectedJet_eta[1])")
    flow.Define(
        "jj_dphi",
        "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(SelectedJet_p4[0], SelectedJet_p4[1]))",
    )
    flow.Define("jj_dr", "TMath::Sqrt(jj_deta*jj_deta + jj_dphi*jj_dphi)")

    flow.Define("LeadingJet_pt", "SelectedJet_pt[0]")
    flow.Define("SubLeadingJet_pt", "SelectedJet_pt[1]")

    # DeltaPhi between Z and dijet
    flow.Define(
        "ZH_ee_dphi", "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(Zee, Dijets))"
    )
    flow.Define(
        "ZH_mm_dphi", "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(Zmm, Dijets))"
    )

    # Common pre-selection for signal and control regions
    flow.Selection("CommonSelEle", "Zee_pt > 75 && Dijets_mass > 50")
    flow.Selection("CommonSelMu", "Zmm_pt > 75 && Dijets_mass > 50")

    ### Signal regions ###
    # Electrons
    flow.Selection(
        "SR_ee",
        "Zee_mass >= 75 && Zee_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && LeadingJetMedium && SubLeadingJetLoose",
        requires=["CommonSelEle"],
    )
    # Muons
    flow.Selection(
        "SR_mm",
        "Zmm_mass >= 75 && Zmm_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && LeadingJetMedium && SubLeadingJetLoose",
        requires=["CommonSelMu"],
    )

    ### Control regions ###
    ## Z+bjets  ##
    # Electrons
    flow.Selection(
        "CR_Zee_bjets",
        "Zee_mass >= 85 && Zee_mass <= 97 && (Dijets_mass < 90 || Dijets_mass > 150) && MET_pt < 60 && LeadingJetMedium && SubLeadingJetLoose && ZH_ee_dphi > 2.5",
        requires=["CommonSelEle"],
    )

    # Muons
    flow.Selection(
        "CR_Zmm_bjets",
        "Zmm_mass >= 85 && Zmm_mass <= 97 && (Dijets_mass < 90 || Dijets_mass > 150) && MET_pt < 60 && LeadingJetMedium && SubLeadingJetLoose && ZH_mm_dphi > 2.5",
        requires=["CommonSelMu"],
    )

    ## Z+light jets ##
    # Electrons
    flow.Selection(
        "CR_Zee_lightjets",
        "Zee_mass >= 75 && Zee_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && !LeadingJetLoose && !SubLeadingJetLoose && ZH_ee_dphi > 2.5",
        requires=["CommonSelEle"],
    )
    # Muons
    flow.Selection(
        "CR_Zmm_lightjets",
        "Zmm_mass >= 75 && Zmm_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && !LeadingJetLoose && !SubLeadingJetLoose && ZH_mm_dphi > 2.5",
        requires=["CommonSelMu"],
    )

    ## ttbar ##
    # Electrons
    flow.Selection(
        "CR_ee_ttbar",
        "((Zee_mass >= 10 && Zee_mass <= 75)  || Zee_mass > 120) && LeadingJetTight && SubLeadingJetLoose",
        requires=["CommonSelEle"],
    )
    # Muons
    flow.Selection(
        "CR_mm_ttbar",
        "((Zmm_mass >= 10 && Zmm_mass <= 75)  || Zmm_mass > 120) && LeadingJetTight && SubLeadingJetLoose",
        requires=["CommonSelMu"],
    )


    ### All leptons collection ###

    flow.MergeCollections("Lepton", ["SelectedElectron", "SelectedMuon"])

    flow.Selection("twoLeptons", "nLepton>=2")
    flow.Distinct("LPair", "Lepton")
    flow.Define(
        "isOSSF",
        "LPair0_charge != LPair1_charge && LPair0_pdgId == LPair1_pdgId",
        requires=["twoLeptons"],
    )
    flow.Selection("hasOSSF", "Sum(isOSSF) > 0")
    # NOTE: Closest to Z (?)
    flow.TakePair(
        "ZLep",
        "Lepton",
        "LPair",
        "Argmax(-abs(MemberMap((LPair0_p4 + LPair1_p4), M()) - 91.2) * isOSSF)",
        requires=["hasOSSF"],
    )
    flow.Define("Z", "ZLep0_p4+ZLep1_p4")
    flow.Define("Z_pt", "Z.Pt()")
    flow.Define("Z_mass", "Z.M()")

    flow.Define("ZH_dphi", "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(Z, Dijets))")
    flow.Define("ZH_deta", "TMath::Abs(Z.Eta() - Dijets.Eta())")
    flow.Define("ZH_dr", "TMath::Sqrt(ZH_dphi*ZH_dphi + ZH_deta*ZH_deta)")
    flow.Define("HZ_ptRatio", "Dijets_pt/Z_pt")

    # Common pre-selection for signal and control regions
    flow.Selection("CommonSel", "Z_pt > 75 && Dijets_mass > 50")

    ## Signal regions ##

    flow.Selection(
        "SR",
        "Z_mass >= 75 && Z_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && Z_pt > 75 && LeadingJetMedium && SubLeadingJetLoose",
        requires=["CommonSel"],
    )

    ## Control regions ##
    # Z+bjets
    flow.Selection(
        "CR_Z_bjets",
        "Z_mass >= 85 && Z_mass <= 97 && (Dijets_mass < 90 || Dijets_mass > 150) && MET_pt < 60 && LeadingJetMedium && SubLeadingJetLoose && ZH_dphi > 2.5",
        requires=["CommonSel"],
    )
    # Z+light jets
    flow.Selection(
        "CR_Z_lightjets",
        "Z_mass >= 75 && Z_mass <= 105 && Dijets_mass >= 90 && Dijets_mass <= 150 && !LeadingJetLoose && !SubLeadingJetLoose && ZH_dphi > 2.5",
        requires=["CommonSel"],
    )
    # ttbar
    flow.Selection(
        "CR_ttbar",
        "((Z_mass >= 10 && Z_mass <= 75)  || Z_mass > 120) && LeadingJetTight && SubLeadingJetLoose",
        requires=["CommonSel"],
    )

    # Interesting variables (input for DNN)

    flowData = copy.deepcopy(flow)

    ## MonteCarlo-only definitions ##

    flow.CentralWeight("genWeight")  # add a central weight

    # Cleaning of GenJet collection from GenLeptons
    flow.SubCollection(
        "GenLepton",
        "GenPart",
        sel="abs(GenPart_pdgId) == 11 || abs(GenPart_pdgId) == 13 || abs(GenPart_pdgId) == 15",
    )
    flow.MatchDeltaR("GenLepton", "GenJet")
    flow.SubCollection(
        "CleanGenJet",
        "GenJet",
        sel="GenJet_GenLeptonDr > 0.3 || GenJet_GenLeptonIdx==-1",
    )

    # Defining subsamples based on flavour of the leading and subleading GenJets
    flow.Define(
        "OneB",
        "(nCleanGenJet >= 1  && ((CleanGenJet_hadronFlavour[0] == 5 && CleanGenJet_hadronFlavour[1] != 5) || (CleanGenJet_hadronFlavour[0] != 5 && CleanGenJet_hadronFlavour[1] == 5))) ",
    )
    flow.Define(
        "TwoB",
        "nCleanGenJet >= 2 && CleanGenJet_hadronFlavour[0] == 5 && CleanGenJet_hadronFlavour[1] == 5",
    )
    flow.Define(
        "OneC",
        "nCleanGenJet >= 1 && ((CleanGenJet_hadronFlavour[0] == 4 && CleanGenJet_hadronFlavour[1] != 5) || (CleanGenJet_hadronFlavour[0] != 5 && CleanGenJet_hadronFlavour[1] == 4))",
    )
    flow.Define(
        "Light",
        "!TwoB && !OneB && !OneC ",
    )

    # Flavour splitting for Diboson processes
    flow.Define(
        "HF",
        "OneB || TwoB || OneC",
    )
    flow.Define("LF", "!HF")

    return flow, flowData
