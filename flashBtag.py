import ROOT

ROOT.EnableImplicitMT()
# file = ROOT.TFile.Open(
#     "/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/230000/068B0797-DEF5-9341-BBBE-EDBE50EBC6A1.root"
# )
file = ROOT.TFile.Open("~/DYIncl_btag.root")
events = file.Get("Events")

fullsim = file.Get("FullSim")
events.AddFriend(fullsim)

rdf = ROOT.RDataFrame(events)

cpp_code = """

ROOT::VecOps::RVec<int> GenJet_JetIdx_func(ROOT::VecOps::RVec<float> GenJet_eta, ROOT::VecOps::RVec<float> GenJet_phi, ROOT::VecOps::RVec<float> Jet_eta, ROOT::VecOps::RVec<float> Jet_phi) {
    ROOT::VecOps::RVec<int> result;
    for (unsigned int i = 0; i < GenJet_eta.size(); i++) {
        float min_delta_r = 0.4;
        int min_delta_r_idx = -1;
        for (unsigned int j = 0; j < Jet_eta.size(); j++) {
            float delta_r = ROOT::VecOps::DeltaR(GenJet_eta[i], Jet_eta[j], GenJet_phi[i], Jet_phi[j]);
            if (delta_r < min_delta_r) {
                min_delta_r = delta_r;
                min_delta_r_idx = j;
            }
        }
        result.push_back(min_delta_r_idx);
    }
    return result;  
}

"""

ROOT.gInterpreter.Declare(cpp_code)

rdf = (
    rdf.Define("Jet_preselection", "Jet_pt > 30 && abs(Jet_eta) < 1.4")
    .Define("SelectedJet_eta", "Jet_eta[Jet_preselection]")
    .Define("SelectedJet_phi", "Jet_phi[Jet_preselection]")
    .Define("SelectedJet_btagDeepFlavB", "Jet_btagDeepFlavB[Jet_preselection]")
    .Define(
        "GenJet_JetIdx",
        "GenJet_JetIdx_func(GenJet_eta, GenJet_phi, SelectedJet_eta, SelectedJet_phi)",
    )
    .Define(
        "MatchedGenJet",
        "GenJet_JetIdx != -1",
    )
    .Define("MatchedGenJet_hadronFlavour", "GenJet_hadronFlavour[MatchedGenJet]")
    .Define(
        "MatchedJet_btagDeepFlavB",
        "Take(SelectedJet_btagDeepFlavB, GenJet_JetIdx[MatchedGenJet])",
    )
    .Define(
        "FullSimJet_preselection", "FullSim.Jet_pt > 30 && abs(FullSim.Jet_eta) < 1.4"
    )
    .Define("FullSimJet_eta", "FullSim.Jet_eta[FullSimJet_preselection]")
    .Define("FullSimJet_phi", "FullSim.Jet_phi[FullSimJet_preselection]")
    .Define(
        "FullSimJet_btagDeepFlavB", "FullSim.Jet_btagDeepFlavB[FullSimJet_preselection]"
    )
    .Define(
        "GenJet_FullSimJetIdx",
        "GenJet_JetIdx_func(GenJet_eta, GenJet_phi, FullSimJet_eta, FullSimJet_phi)",
    )
    .Define(
        "MatchedGenJet_FullSim",
        "GenJet_FullSimJetIdx != -1",
    )
    .Define(
        "MatchedGenJet_FullSim_hadronFlavour",
        "GenJet_hadronFlavour[MatchedGenJet_FullSim]",
    )
    .Define(
        "MatchedJet_FullSim_btagDeepFlavB",
        "Take(FullSimJet_btagDeepFlavB, GenJet_FullSimJetIdx[MatchedGenJet_FullSim])",
    )
)

rdf.Snapshot(
    "btag",
    "btag.root",
    [
        "MatchedJet_btagDeepFlavB",
        "MatchedGenJet_hadronFlavour",
        "MatchedJet_FullSim_btagDeepFlavB",
        "MatchedGenJet_FullSim_hadronFlavour",
        "FullSimJet_btagDeepFlavB",
        "FullSim.Jet_hadronFlavour",
        "FullSim.Jet_btagDeepFlavB",
    ],
)
