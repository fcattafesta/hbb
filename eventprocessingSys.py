from nail.nail import *
import correctionlib

from btagging_sys import unc_btag
correctionlib.register_pyroot_binding()


sf_btag = {
    "Central": ["central"],
    "Up": ["up_" + x for x in unc_btag],
    "Down": ["down_" + x for x in unc_btag],
}


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
        """
        #include <cstring>

        // Calculate b-tagging scale factors for a given set of inputs
        template <typename str, typename VecI, typename Vec>
        auto sf_btag(const str & name, const VecI & hadronFlavour, const Vec & eta, const Vec & pt, const Vec & btag) {
            // Create a vector to store the scale factors
            ROOT::VecOps::RVec<float> weights(hadronFlavour.size());

            int flav[3];
            if (strstr(name, "central") != nullptr) {
                flav[0] = 0; flav[1] = 5; flav[2] = 4;
            } else if (strstr(name, "hf") != nullptr || strstr(name, "lf") != nullptr) {
                flav[0] = 0; flav[1] = 5; flav[2] = -1;
            } else {
                flav[0] = 4; flav[1] = -1; flav[2] = -1;
            }

            // Loop over each input and calculate the scale factor
            for(size_t i=0;i<hadronFlavour.size(); i++) {
                bool correct_flav = false;
                // Loop over each flavor and check if it matches the input flavor
                for (long unsigned int j = 0; j < sizeof(flav) / sizeof(flav[0]); j++) {
                    if (hadronFlavour[i] == flav[j]) {
                        // Calculate the scale factor using the btag_shape_corr object
                        weights[i]=btag_shape_corr->evaluate({name, hadronFlavour[i], abs(eta[i]), pt[i], btag[i]});
                        correct_flav = true;
                        break;
                    }
                }
                // If no matching flavor is found, set the scale factor to 1
                if (!correct_flav) {
                    weights[i]=1.;
                }
            }
            // Return the vector of scale factors
            return weights;
        }
    """
    )
    for suffix, names in sf_btag.items():
        for i, name in enumerate(names):
            flow.Define(
                "SelectedJet_btagWeight_%s%s" % (suffix, i),
                'sf_btag("%s", SelectedJet_hadronFlavour, SelectedJet_eta, SelectedJet_pt, SelectedJet_btagDeepFlavB)'
                % (name),
            )
            if suffix == "Central":
                flow.Define(
                    "btagWeight%s" % (suffix),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight_%s%s)" % (suffix, i),
                )
                flow.CentralWeight("btagWeightCentral", ["twoJets"])
            else:
                flow.Define(
                    "btagWeight_%s%s" % (unc_btag[i], suffix),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight_%s%s)" % (suffix, i),
                )
                flow.VariationWeight(
                    "btagWeight_%s%s" % (unc_btag[i], suffix), "btagWeightCentral"
                )

    return flow
