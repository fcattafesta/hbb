from nail.nail import *
import correctionlib

from args_analysis import args

correctionlib.register_pyroot_binding()


def getFlowSysJER(flow, sys):
    if sys:
        # JER systematics
        flow.AddCppCode('#include "correction.h"\n')
        flow.AddCppCode("#include <TRandom3.h>\n")
        flow.AddCppCode("#include <cstring>\n")

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
        for name in ["Nom", "Down", "Up"]:
            flow.Define(
                "Jet_jer%sSF" % (name),
                'sf_jer(Jet_eta, "%s")' % (name.lower()),
            )
            flow.Define(
                "Jet_pt_jer%s" % (name),
                "Jet_genPt+(Jet_pt-Jet_genPt)*Jet_jer%sSF" % (name),
            )
            if name != "Nom":
                flow.Systematic(
                    "JER%s" % (name), "Jet_pt_jerNom", "Jet_pt_jer%s" % (name)
                )
        # +(Jet_genPt==Jet_pt)*Map(Jet_pt, [](float sigma) {TRandom3 r; return float(r.Gaus(0,0.15*sigma));} )",

    else:
        flow.Define("Jet_pt_jerNom", "Jet_pt")

    return flow
