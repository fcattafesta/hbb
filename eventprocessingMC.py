from nail.nail import *


def getFlowMC(flow):
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

    flow.Define(
        "btag_max_hadronFlavour",
        "JetBtagMax_hadronFlavour",
    )
    flow.Define(
        "btag_min_hadronFlavour",
        "JetBtagMin_hadronFlavour",
    )

    return flow
