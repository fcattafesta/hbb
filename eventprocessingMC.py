from nail.nail import *
import correctionlib

correctionlib.register_pyroot_binding()


def getFlowMC(flow, btag, sf):
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

    if sf:
        flow.AddCppCode('#include "correction.h"\n')
        flow.AddCppCode(
            'auto btag_corr = correction::CorrectionSet::from_file("btagging.json.gz");\n'
        )
        flow.AddCppCode(
            'auto btag_shape_corr = btag_corr->at("%s");\n'
            % ("deepJet_shape" if btag == "deepflav" else "deepCSV_shape")
        )
        flow.AddCppCode(
            """ template <typename str, typename VecI, typename Vec>
                auto sf_btag(const str & name, const VecI & hadronFlavour, const Vec & eta, const Vec & pt, const Vec & btag) {
                ROOT::VecOps::RVec<float> weights(hadronFlavour.size());
                for(size_t i=0;i<hadronFlavour.size(); i++) weights[i]=btag_shape_corr->evaluate({name, hadronFlavour[i], abs(eta[i]), pt[i], btag[i]});
                return weights;
                }"""
        )
        flow.Define(
            "SelectedJet_btagWeight",
            'sf_btag("central", SelectedJet_hadronFlavour, SelectedJet_eta, SelectedJet_pt, %s)'
            % (
                "SelectedJet_btagDeepFlavB"
                if btag == "deepflav"
                else "SelectedJet_btagDeepB"
            ),
        )
        flow.Define("btagWeight", "ROOT::VecOps::Product(SelectedJet_btagWeight)")
        flow.CentralWeight("btagWeight", ["twoJets"])
    return flow
