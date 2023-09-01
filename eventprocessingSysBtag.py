from nail.nail import *
import correctionlib

from btagging_sys import unc_btag
from args_analysis import args

correctionlib.register_pyroot_binding()


sf_btag = (
    {
        "Central": ["central"],
        # "Up": ["up_cferr1", "up_hf", "up_lfstats1", "up_lf"],
        # "Down": ["down_cferr1", "down_hf", "down_lfstats1", "down_lf"],
    }
    if args.sf_only
    else {
        "Central": ["central"],
        "Up": ["up_" + x for x in unc_btag],
        "Down": ["down_" + x for x in unc_btag],
    }
)


def getFlowSysBtag(flow, btag):
    flow.AddCppCode('#include "correction.h"\n')
    # Btag systematics
    flow.AddCppCode(
        'auto btag_corr = correction::CorrectionSet::from_file("btagging.json.gz");\n'
    )
    flow.AddCppCode(
        'auto btag_shape_corr = btag_corr->at("%s");\n'
        % ("deepJet_shape" if btag == "deepflav" else "deepCSV_shape")
    )
    flow.AddCppCode(
        """
        #include <json.hpp>
        std::ifstream f("rescale_btag.json");
        json btag_rescale_avg = json::parse(f);
        """
    )
    flow.AddCppCode(
        """
        // Calculate b-tagging scale factors for a given set of inputs
        template <typename str, typename VecI, typename Vec>
        auto sf_btag(const str & name, const VecI & hadronFlavour, const Vec & eta, const Vec & pt, const Vec & btag, const str & btag_name) {
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
                // check if the flav matches the input flavor
                int *match_flav = std::find(std::begin(flav), std::end(flav), hadronFlavour[i]);
                if (match_flav != std::end(flav)) {
                    std::string h_f=std::to_string(hadronFlavour[i]);
                    // Calculate the scale factor using the btag_shape_corr object
                    sf[i]=btag_shape_corr->evaluate({name, hadronFlavour[i], abs(eta[i]), pt[i], btag[i]})/btag_shape_corr[btag_name][h_f][name];
                    correct_flav = true;
                }
                // If no matching flavor is found, set the scale factor to the central value
                if (!correct_flav) {
                    sf[i]=btag_shape_corr->evaluate({"central", hadronFlavour[i], abs(eta[i]), pt[i], btag[i]})/btag_shape_corr[btag_name][hadronFlavour[i]][name];
                }
            }
            // Return the vector of scale factors
            return sf;
        }
    """
    )

    # NOTE: btag weights to all jets or to only selected jets? i think to only selected jets
    for suffix, names in sf_btag.items():
        for name in names:
            unc = name.replace("up_", "").replace("down_", "")

            flow.Define(
                "SelectedJet_btagWeight_%s" % name,
                'sf_btag("%s", SelectedJet_hadronFlavour, SelectedJet_eta, SelectedJet_pt, %s, "%s")'
                % (
                    name,
                    "SelectedJet_btagDeepFlavB"
                    if btag == "deepflav"
                    else "SelectedJet_btagDeepB",
                    btag,
                ),
            )
            if suffix == "Central":
                flow.Define(
                    "btagWeight%s" % (suffix),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight_%s)" % name,
                )
                flow.CentralWeight("btagWeightCentral", ["twoJets"])
            else:
                flow.Define(
                    "btagWeight_%s%s" % (unc, suffix),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight_%s)" % name,
                )
                flow.VariationWeight(
                    "btagWeight_%s%s" % (unc, suffix), "btagWeightCentral"
                )

    return flow
