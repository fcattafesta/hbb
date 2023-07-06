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
    flow.AddCppCode('#include <TRandom.h>\n')
    flow.AddCppCode('#include <cstring>\n')
    #flow.AddCppCode('#include "correctionlib_sys.h"\n')

    # btag systematics
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
                    sf[i]=1.;
                }
            }
            // Return the vector of scale factors
            return sf;
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

    # JER systematics
    flow.AddCppCode(
        'auto jer_corr = correction::CorrectionSet::from_file("jet_jerc.json.gz");\n'
    )
    flow.AddCppCode(
        'auto jer_sf_corr = jer_corr->at("%s");\n'
        % "Summer19UL18_JRV2_MC_ScaleFactor_AK4PFchs"
    )

    flow.AddCppCode(
        """
        // Calculate jer scale factors for a given set of inputs
        template <typename Vec, typename str>
        auto sf_jer(const Vec & eta, const str & name) {
            // Create a vector to store the scale factors
            ROOT::VecOps::RVec<float> sf(eta.size());

            // Loop over each input and calculate the scale factor
            for(size_t i=0;i<eta.size(); i++) {
                // Calculate the scale factor using the jer_sf_corr object
                sf[i]=jer_sf_corr->evaluate({eta[i], name});
            }
            // Return the vector of scale factors
            return sf;
        }
    """
    )

    flow.Define("Jet_genPt", "TakeDef(GenJet_pt,Jet_genJetIdx,Jet_pt)")
    for name in ["Nom", "Up", "Down"]:
        flow.Define(
            "Jet_jer%sSF" % (name),
            'sf_jer(Jet_eta, "%s")' % (name.lower()),
        )
    flow.Define("Jet_pt_jerNom", "Jet_genPt+(Jet_pt-Jet_genPt)*Jet_jerNomSF")
    flow.Define("Jet_pt_jerDown", "Jet_genPt+(Jet_pt-Jet_genPt)*Jet_jerDownSF")
    flow.Define(
        "Jet_pt_jerUp",
        "Jet_genPt+(Jet_pt-Jet_genPt)*Jet_jerUpSF+(Jet_genPt==Jet_pt)*Map(Jet_pt, [](float sigma) {return float(TRandom->Gaus(0,0.15*sigma));} )",
    )
    flow.Systematic("JERDown","Jet_pt_jerNom","Jet_pt_jerDown")
    flow.Systematic("JERUp","Jet_pt_jerNom","Jet_pt_jerUp")

    # nom? pt_touse per fare massa dell higgs
    # jet
    # quando reco non matcha con gen fai lo smearing up

    return flow
