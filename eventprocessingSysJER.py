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
        for name in ["Nom", "Up", "Down"]:
            flow.Define(
                "Jet_jer%sSF" % (name),
                'sf_jer(Jet_eta, "%s")' % (name.lower()),
            )
        flow.Define("Jet_pt_Nom", "Jet_genPt+(Jet_pt-Jet_genPt)*Jet_jerNomSF")
        flow.Define("Jet_pt_jerDown", "Jet_genPt+(Jet_pt-Jet_genPt)*Jet_jerDownSF")
        flow.Define(
            "Jet_pt_jerUp",
            "Jet_genPt+(Jet_pt-Jet_genPt)*Jet_jerUpSF",  # +(Jet_genPt==Jet_pt)*Map(Jet_pt, [](float sigma) {TRandom3 r; return float(r.Gaus(0,0.15*sigma));} )",
        )
        flow.Systematic("JERDown", "Jet_pt_Nom", "Jet_pt_jerDown")
        flow.Systematic("JERUp", "Jet_pt_Nom", "Jet_pt_jerUp")

    else:
        flow.Define("Jet_pt_Nom", "Jet_pt")

    return flow
