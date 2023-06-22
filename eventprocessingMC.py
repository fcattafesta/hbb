from nail.nail import *
import correctionlib

correctionlib.register_pyroot_binding()


def getFlowMC(flow, btag, no_sf):
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

    if not no_sf:
        flow.AddCppCode('#include "correction.h"\n')
        flow.AddCppCode(
            'auto btag_corr = correction::CorrectionSet::from_file("btagging.json.gz");\n'
        )
        flow.AddCppCode(
            'auto btag_shape_corr = btag_corr->at("%s");\n'
            % ("deepJet_shape" if btag == "deepflav" else "deepCSV_shape")
        )
        flow.AddCppCode(
            """template <typename VecI, typename Vec>
                auto sf_btag(const VecI & hadronFlavour, const Vec & eta, const Vec & pt, const Vec & btag) {
                float weight=1.;
                for(size_t i=0;i<hadronFlavour.size(); i++) weight=weight*btag_shape_corr->evaluate({"central", hadronFlavour[i], abs(eta[i]), pt[i], btag[i]});
                return weight;
                }"""
        )
        flow.Define(
            "SelectedJet_btagWeight",
            "sf_btag(SelectedJet_hadronFlavour, SelectedJet_eta, SelectedJet_pt, %s)"
            % (
                "SelectedJet_btagDeepFlavB"
                if btag == "deepflav"
                else "SelectedJet_btagDeepB"
            ),
        )
        flow.CentralWeight("SelectedJet_btagWeight", ["twoJets"])
    return flow
