from nail.nail import *


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

    ## Defining subsamples

    # TwoB if there are at least two b jets, not necessarily the first two
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


    # # Cleaning of GenJet collection from GenLeptons
    # flow.SubCollection(
    #     "GenLepton",
    #     "GenPart",
    #     sel="abs(GenPart_pdgId) == 11 || abs(GenPart_pdgId) == 13 || abs(GenPart_pdgId) == 15",
    # )
    # flow.MatchDeltaR("GenLepton", "GenJet")
    # flow.SubCollection(
    #     "CleanGenJet",
    #     "GenJet",
    #     sel="GenJet_GenLeptonDr > 0.3 || GenJet_GenLeptonIdx==-1",
    # )

    # # Defining subsamples based on flavour of the leading and subleading GenJets
    # flow.Define(
    #     "TwoB",
    #     "nCleanGenJet >= 2 && CleanGenJet_hadronFlavour[0] == 5 && CleanGenJet_hadronFlavour[1] == 5",
    # )
    # flow.Define(
    #     "OneB",
    #     "(nCleanGenJet >= 1  && ((CleanGenJet_hadronFlavour[0] == 5 && CleanGenJet_hadronFlavour[1] != 5) || (CleanGenJet_hadronFlavour[0] != 5 && CleanGenJet_hadronFlavour[1] == 5))) ",
    # )
    # flow.Define(
    #     "C",
    #     "nCleanGenJet >= 1 && ((CleanGenJet_hadronFlavour[0] == 4 && CleanGenJet_hadronFlavour[1] != 5) || (CleanGenJet_hadronFlavour[0] != 5 && CleanGenJet_hadronFlavour[1] == 4))",
    # )
    # flow.Define(
    #     "Light",
    #     "!TwoB && !OneB && !C ",
    # )

    return flow
