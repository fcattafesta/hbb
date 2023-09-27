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
        sel="GenJet_pt > 15. && abs(GenJet_eta) < 2.5",
    )

    #TODO: GenJet_pt > 25

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
