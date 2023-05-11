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
    flow.Define("Mjj", "Dijets.M()")

    # DeltaPhi between Z and dijet
    flow.Define(
        "ZH_ee_dphi", "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(Zee, Dijets))"
    )
    flow.Define(
        "ZH_mm_dphi", "TMath::Abs(ROOT::Math::VectorUtil::DeltaPhi(Zmm, Dijets))"
    )

    ### Signal regions ###
    # Electrons
    flow.Selection(
        "SR_ee",
        "Zee_mass >= 75 && Zee_mass <= 105 && Mjj >= 90 && Mjj <= 150 && Zee_pt > 75 && LeadingJetMedium && SubLeadingJetLoose",
    )
    # Muons
    flow.Selection(
        "SR_mm",
        "Zmm_mass >= 75 && Zmm_mass <= 105 && Mjj >= 90 && Mjj <= 150 && Zmm_pt > 75 && LeadingJetMedium && SubLeadingJetLoose",
    )

    ### Control regions ###
    ## Z+bjets  ##
    # Electrons
    flow.Selection(
        "CR_Zee_bjets",
        "Zee_mass >= 85 && Zee_mass <= 97 && (Mjj < 90 || Mjj > 150) && MET_pt < 60 && LeadingJetMedium && SubLeadingJetLoose && ZH_ee_dphi > 2.5",
    )
    # Muons
    flow.Selection(
        "CR_Zmm_bjets",
        "Zmm_mass >= 85 && Zmm_mass <= 97 && (Mjj < 90 || Mjj > 150) && MET_pt < 60 && LeadingJetMedium && SubLeadingJetLoose && ZH_mm_dphi > 2.5",
    )

    ## Z+light jets ##
    # Electrons
    flow.Selection(
        "CR_Zee_lightjets",
        "Zee_mass >= 75 && Zee_mass <= 105 && Mjj >= 90 && Mjj <= 150 && !LeadingJetLoose && !SubLeadingJetLoose && ZH_ee_dphi > 2.5",
    )
    # Muons
    flow.Selection(
        "CR_Zmm_lightjets",
        "Zmm_mass >= 75 && Zmm_mass <= 105 && Mjj >= 90 && Mjj <= 150 && !LeadingJetLoose && !SubLeadingJetLoose && ZH_mm_dphi > 2.5",
    )

    ## ttbar ##
    # Electrons
    flow.Selection(
        "CR_ee_ttbar",
        "((Zee_mass >= 10 && Zee_mass <= 75)  || Zee_mass > 120) && LeadingJetTight && SubLeadingJetLoose",
    )
    # Muons
    flow.Selection(
        "CR_mm_ttbar",
        "((Zmm_mass >= 10 && Zmm_mass <= 75)  || Zmm_mass > 120) && LeadingJetTight && SubLeadingJetLoose",
    )

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
