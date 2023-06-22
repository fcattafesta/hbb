from nail.nail import *
import correctionlib

correctionlib.register_pyroot_binding()


def getFlowMC(flow, btag, sf=False):
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

    if sf:
        flow.AddCppCode('#include "correction.h"\n')
        flow.AddCppCode(
            'auto btag_corr = correction::CorrectionSet::from_file("btagging.json.gz");\n'
        )
        if btag == "deepflav":
            flow.AddCppCode('auto btag_shape_corr = btag_corr->at("deepJet_shape");\n')
            flow.Define(
                "SelectedJet_btagWeight",
                'vector_map(btag_shape_corr->evaluate, ROOT::VecOps::RVec<char>(nSelectedJet,"central"), SelectedJet_hadronFlavour, abs(SelectedJet_eta), SelectedJet_pt, JetBtagMax_btagDeepFlavB})',
                #'btag_shape_corr->evaluate({"central", SelectedJet_hadronFlavour, abs(SelectedJet_eta), SelectedJet_pt, JetBtagMax_btagDeepFlavB})',
            )
        elif btag == "deepcsv":
            flow.AddCppCode('auto btag_shape_corr = btag_corr->at("deepCSV_shape");\n')
            flow.Define(
                "SelectedJet_btagWeight",
                'vector_map(btag_shape_corr->evaluate, ROOT::VecOps::RVec<char>(nSelectedJet,"central"), SelectedJet_hadronFlavour, abs(SelectedJet_eta), SelectedJet_pt, SelectedJet_btagDeepB})',
                #'btag_shape_corr->evaluate({"central", SelectedJet_hadronFlavour, abs(SelectedJet_eta), SelectedJet_pt, SelectedJet_btagDeepB})',
            )
        flow.CentralWeight("SelectedJet_btagWeight", ["twoJets"])
    return flow
