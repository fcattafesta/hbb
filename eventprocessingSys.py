from nail.nail import *
import correctionlib

correctionlib.register_pyroot_binding()


def getFlowSys(flow, btag):
    ## Systematics definitions ##

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

    for name in ["Central", "Up", "Down"]:
        flow.Define(
            "SelectedJet_btagWeight%s" % name,
            "sf_btag(%s, SelectedJet_hadronFlavour, SelectedJet_eta, SelectedJet_pt, %s)"
            % (
                name.lower(),
                "SelectedJet_btagDeepFlavB"
                if btag == "deepflav"
                else "SelectedJet_btagDeepB",
            ),
        )
        flow.Define(
            "btagWeight%s" % name,
            "ROOT::VecOps::Product(SelectedJet_btagWeight%s)" % name,
        )


    flow.CentralWeight("btagWeightCentral", ["twoJets"])
    flow.VariationWeight("btagWeightUp", "btagWeightCentral")
    flow.VariationWeight("btagWeightDown", "btagWeightCentral")

    return flow
