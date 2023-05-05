from nail.nail import *
import ROOT
import sys


def getFlow():
    # Start flow definition
    flow = SampleProcessing(
        "Analysis", "/scratchnvme/malucchi/1574B1FB-8C40-A24E-B059-59A80F397A0F.root"
    )
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

    # GenJet selection: leading and subleading (pt ordered)
    flow.Selection("AtLeastTwoGenJets", "nCleanGenJet >= 2")
    flow.ObjectAt("LeadingGenJet", "CleanGenJet", "0", requires=["AtLeastTwoGenJets"])
    flow.ObjectAt(
        "SubLeadingGenJet", "CleanGenJet", "1", requires=["AtLeastTwoGenJets"]
    )

    # Defining subsamples based on flavour of the leading and subleading GenJets
    # NOTE: Defined collections are mutually exclusive, are they ok?
    flow.Define(
        "OneB",
        "(LeadingGenJet_hadronFlavour == 5 && SubLeadingGenJet_hadronFlavour != 5) || (LeadingGenJet_hadronFlavour != 5 && SubLeadingGenJet_hadronFlavour == 5)",
    )
    flow.Define(
        "TwoB",
        "LeadingGenJet_hadronFlavour == 5 && SubLeadingGenJet_hadronFlavour == 5",
    )
    flow.Define(
        "OneC",
        "(LeadingGenJet_hadronFlavour == 4 && SubLeadingGenJet_hadronFlavour != 5) || (LeadingGenJet_hadronFlavour != 5 && SubLeadingGenJet_hadronFlavour == 4)",
    )
    flow.Define(
        "Light",
        "LeadingGenJet_hadronFlavour == 0 && SubLeadingGenJet_hadronFlavour == 0",
    )

    # Muon selection ID
    flow.Define("Muon_iso", "(Muon_pfRelIso04_all)")
    # NOTE: Multiple Muon Id (loose, tight), isolation (0.4 or 0.06)
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

    # reco Z from RECO particles
    flow.Define("Zmm", "Mu0_p4+Mu1_p4", requires=["PtSelMu"])
    flow.Define("Zmm_pt", "Zmm.Pt()", requires=["PtSelMu"])
    flow.Define("Zmm_mass", "Zmm.M()", requires=["PtSelMu"])

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

    # reco Z from RECO particles
    flow.Define("Zee", "El0_p4+El1_p4", requires=["PtSelEl"])
    flow.Define("Zee_pt", "Zee.Pt()", requires=["PtSelEl"])
    flow.Define("Zee_mass", "Zee.M()", requires=["PtSelEl"])

    # reco Z form GENParticles
    flow.SubCollection(
        "GenMuon",
        "GenPart",
        sel="abs(GenPart_pdgId) == 13 && GenPart_status == 1 && GenPart_pt > 20. && abs(GenPart_eta) < 2.4",
    )
    flow.Selection("twoGenMuons", "nGenMuon==2")
    flow.Define("GenMuon_p4", "@p4v(GenMuon)")
    flow.Define("GenMuon_charge", "-GenMuon_pdgId/abs(GenMuon_pdgId)")
    flow.Distinct("GenMuMu", "GenMuon")
    flow.Define(
        "OppositeSignGenMuMu",
        "Nonzero(GenMuMu0_charge != GenMuMu1_charge)",
        requires=["twoGenMuons"],
    )
    flow.Selection("twoOppositeSignGenMuons", "OppositeSignGenMuMu.size() > 0")
    flow.TakePair(
        "GenMu",
        "GenMuon",
        "GenMuMu",
        "At(OppositeSignGenMuMu,0,-200)",
        requires=["twoOppositeSignGenMuons"],
    )
    flow.Define("GenZ", "GenMu0_p4+GenMu1_p4")
    flow.Define("Gen_Zpt", "GenZ.Pt()")
    flow.Define("Gen_ZMass", "GenZ.M()")
    flow.Selection("lowMass", "Gen_ZMass < 50 && twoOppositeSignGenMuons")

    # signal region
    flow.Selection("SR", "Reco_ZMass > 75 && Reco_ZMass < 105")

    return flow
