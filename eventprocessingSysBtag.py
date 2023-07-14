from nail.nail import *
import correctionlib

from btagging_sys import unc_btag

correctionlib.register_pyroot_binding()


sf_btag = {
    "Central": ["central"],
    "Up": ["up_" + x for x in unc_btag],
    "Down": ["down_" + x for x in unc_btag],
}


def getFlowSysBtag(flow, btag):
    # Btag systematics
    flow.AddCppCode(
        'auto btag_corr = correction::CorrectionSet::from_file("btagging.json.gz");\n'
    )
    flow.AddCppCode(
        'auto btag_shape_corr = btag_corr->at("%s");\n'
        % ("deepJet_shape" if btag == "deepflav" else "deepCSV_shape")
    )

    # NOTE: cut on eta for the jet
    flow.AddCppCode(
        """
        // Calculate b-tagging scale factors for a given set of inputs
        template <typename str, typename VecI, typename Vec>
        auto sf_btag(const str & name, const VecI & hadronFlavour, const Vec & eta, const Vec & pt, const Vec & btag) {
            // Create a vector to store the scale factors
            ROOT::VecOps::RVec<float> sf(hadronFlavour.size());

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
                        sf[i]=btag_shape_corr->evaluate({name, hadronFlavour[i], abs(eta[i]), pt[i], btag[i]});
                        correct_flav = true;
                        break;
                    }
                }
                // If no matching flavor is found, set the scale factor to 1
                if (!correct_flav) {
                    sf[i]=btag_shape_corr->evaluate({"central", hadronFlavour[i], abs(eta[i]), pt[i], btag[i]});
                }
            }
            // Return the vector of scale factors
            return sf;
        }
    """
    )

    # FIXME: btag weights to all jets or to only selected jets? i think to only selected jets
    for suffix, names in sf_btag.items():
        for name in names:
            unc = name.replace("up_", "").replace("down_", "")

            # NOTE: which score? C or B?

            flow.Define(
                "SelectedJet_btagWeight_%s" % name,
                'sf_btag("%s", SelectedJet_hadronFlavour, SelectedJet_eta, SelectedJet_pt, %s)'
                % (
                    name,
                    "SelectedJet_btagDeepFlavB" if btag == "deepflav" else "SelectedJet_btagDeepB",
                ),
            )
            if suffix == "Central":
                flow.Define(
                    "btagWeight%s" % (suffix),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight_%s)" % name,
                )
                flow.CentralWeight("btagWeightCentral", ["twoJets"]) #HERE
            else:
                flow.Define(
                    "btagWeight_%s%s" % (unc, suffix),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight_%s)" % name,
                )
                flow.VariationWeight(
                    "btagWeight_%s%s" % (unc, suffix), "btagWeightCentral"
                )

    return flow
