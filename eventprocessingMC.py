from nail.nail import *
import correctionlib

correctionlib.register_pyroot_binding()


def getFlowMC(flow):
    ## MonteCarlo-only definitions ##

    flow.Define(
        "hadronFlavour_btag_max",
        "JetBtagMax_hadronFlavour",
    )
    flow.Define(
        "hadronFlavour_btag_min",
        "JetBtagMin_hadronFlavour",
    )

    flow.CentralWeight("genWeight")  # add a central weight

    flow.SubCollection(
        "SelectedGenJet",
        "GenJet",
        sel="GenJet_pt > 25. && abs(GenJet_eta) < 2.5",
    )

    flow.SubCollection(
        "GenLepton",
        "GenPart",
        sel="abs(GenPart_pdgId) == 11 || abs(GenPart_pdgId) == 13",
    )
    flow.MatchDeltaR("SelectedGenJet", "GenLepton")

    flow.SubCollection(
        "CleanedGenJet",
        "SelectedGenJet",
        sel="SelectedGenJet_GenLeptonDr > 0.4 || SelectedGenJet_GenLeptonIdx==-1",
    )
    flow.Define("CleanedGenJet_ptOrderIdx", "Argsort(-CleanedGenJet_pt)")
    flow.Selection("twoGenJets", "nCleanedGenJet >= 2")
    flow.ObjectAt(
        "LeadingGenJet",
        "CleanedGenJet",
        "At(CleanedGenJet_ptOrderIdx,0)",
        requires=["twoGenJets"],
    )
    flow.ObjectAt(
        "SubLeadingGenJet",
        "CleanedGenJet",
        "At(CleanedGenJet_ptOrderIdx,1)",
        requires=["twoGenJets"],
    )

    ## Defining subsamples
    flow.Define(
        "TwoB",
        "Sum(SelectedGenJet_hadronFlavour == 5) >= 2",
    )
    flow.Define(
        "OneB",
        "Sum(SelectedGenJet_hadronFlavour == 5) == 1",
    )
    flow.Define(
        "C",
        "Sum(SelectedGenJet_hadronFlavour == 4) >= 1 && Sum(SelectedGenJet_hadronFlavour == 5) == 0",
    )
    flow.Define(
        "Light",
        "!TwoB && !OneB && !C ",
    )

    return flow
