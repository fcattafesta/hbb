from nail.nail import *
import correctionlib

correctionlib.register_pyroot_binding()

unc_list = [
    "hf",
    "lf",
    "hfstats1",
    "hfstats2",
    "lfstats1",
    "lfstats2",
    "cferr1",
    "cferr2",
]
sf = {
    "Central": ["central"],
    "Up": ["up_" + x for x in unc_list],
    "Down": ["down_" + x for x in unc_list],
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
        // Calculate b-tagging scale factors for a given set of inputs
        template <typename str, typename VecI, typename Vec, typename T>
        auto sf_btag(const str & name, const VecI & hadronFlavour, const Vec & eta, const Vec & pt, const Vec & btag, std::vector<T> flav) {
            // Create a vector to store the scale factors
            ROOT::VecOps::RVec<float> weights(hadronFlavour.size());

            // Loop over each input and calculate the scale factor
            for(size_t i=0;i<hadronFlavour.size(); i++) {
                bool correct_flav = false;
                // Loop over each flavor and check if it matches the input flavor
                for (int i = 0; i < flav.size(); i++) {
                    if (hadronFlavour[i] == flav[i]) {
                        // Calculate the scale factor using the btag_shape_corr object
                        weights[i]=btag_shape_corr->evaluate({name, hadronFlavour[i], abs(eta[i]), pt[i], btag[i]});
                        correct_flav = true;
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
    flow.AddCppCode("#include <vector>\n")
    flow.AddCppCode("std::vector<int> flav;\n")
    for suffix, names in sf.items():
        for i, name in enumerate(names):
            if "lf" or "hf" in name:
                flow.AddCppCode("flav = {0,5};\n")
            elif "central" in name:
                flow.AddCppCode("flav = {0,4,5};\n")
            else:
                flow.AddCppCode("flav = {4};\n")
            flow.Define(
                "SelectedJet_btagWeight%s_%s" % (suffix, i),
                'sf_btag("%s", SelectedJet_hadronFlavour, SelectedJet_eta, SelectedJet_pt, SelectedJet_btagDeepFlavB, flav)'
                % (name),
            )
            if suffix == "Central":
                flow.Define(
                    "btagWeight%s" % (suffix),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight%s_%s)" % (suffix, i),
                )
                flow.CentralWeight("btagWeightCentral", ["twoJets"])
            else:
                flow.Define(
                    "btagWeight%s_%s" % (suffix, unc_list[i]),
                    "ROOT::VecOps::Product(SelectedJet_btagWeight%s_%s)" % (suffix, i),
                )
                flow.VariationWeight(
                    "btagWeight%s_%s" % (suffix, unc_list[i]), "btagWeightCentral"
                )

        # # multiply all the weights together
        # multiply_string = ""
        # for i in range(len(names)):
        #     multiply_string += "btagWeight%s%s*" % (suffix, i)
        # multiply_string = multiply_string[:-1]
        # flow.Define(
        #     "btagWeight%s" % suffix,
        #     multiply_string,
        # )

    return flow
