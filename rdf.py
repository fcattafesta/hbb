import ROOT
import argparse

parser = argparse.ArgumentParser( description = "Analysis Tool" )
parser.add_argument("-f", "--file",   default="", type=str,
                            help="file name" )
args = parser.parse_args()

ROOT.ROOT.EnableImplicitMT(100)
thread_size = ROOT.ROOT.GetThreadPoolSize()
print(">>> Thread pool size for parallel processing: %s", thread_size)

file_name = f"/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/{args.file}"
rdf = ROOT.RDataFrame("Events", file_name)

ROOT.gInterpreter.Declare("""
#include "ROOT/RVec.hxx"
using namespace ROOT::VecOps;

using VecF = const RVec<float>&;

/*
 * Reconstruct the fourvector of the leptons.
*/
RVec<TLorentzVector> lepFourVec(VecF lep_pt, VecF lep_eta, VecF lep_phi, VecF lep_mass){
    RVec<TLorentzVector> lep_fourvecs(lep_pt.size());
    for (size_t i = 0; i < lep_pt.size(); i++) {
        TLorentzVector p;
        p.SetPtEtaPhiM(lep_pt[i], lep_eta[i], lep_phi[i], lep_mass[i]);
        lep_fourvecs[i] = p ;
    }
    return lep_fourvecs;
};
""")


'''rdf = (
    rdf.Define("muon_mask", "abs(LHEPart_pdgId) == 13")
    .Define("muon_pt", "LHEPart_pt[muon_mask]")
    .Define("muon_eta", "LHEPart_eta[muon_mask]")
    .Define("muon_phi", "LHEPart_phi[muon_mask]")
    .Define("muon_mass", "LHEPart_mass[muon_mask]")
    .Define("Muon_fourvec","lepFourVec(muon_pt, muon_eta, muon_phi, muon_mass)")
    .Define("muon_inv_mass", "(Muon_fourvec[0]+Muon_fourvec[1]).M()")
    .Define("electron_mask", "abs(LHEPart_pdgId) == 11")
    .Define("electron_pt", "LHEPart_pt[electron_mask]")
    .Define("electron_eta", "LHEPart_eta[electron_mask]")
    .Define("electron_phi", "LHEPart_phi[electron_mask]")
    .Define("electron_mass", "LHEPart_mass[electron_mask]")
    .Define("Electron_fourvec", "lepFourVec(electron_pt, electron_eta, electron_phi, electron_mass)")
    .Define("electron_inv_mass", "(Electron_fourvec[0]+Electron_fourvec[1]).M()")
    .Define("tau_mask", "abs(LHEPart_pdgId) == 15")
    .Define("tau_pt", "LHEPart_pt[tau_mask]")
    .Define("tau_eta", "LHEPart_eta[tau_mask]")
    .Define("tau_phi", "LHEPart_phi[tau_mask]")
    .Define("tau_mass", "LHEPart_mass[tau_mask]")
    .Define("Tau_fourvec", "lepFourVec(tau_pt, tau_eta, tau_phi, tau_mass)")
    .Define("tau_inv_mass", "(Tau_fourvec[0]+Tau_fourvec[1]).M()")
)'''

rdf= (
    rdf.Define("lepton_mask", "abs(LHEPart_pdgId) >= 11 &&  abs(LHEPart_pdgId) <= 15")
    .Define("lepton_pt", "LHEPart_pt[lepton_mask]")
    .Define("lepton_eta", "LHEPart_eta[lepton_mask]")
    .Define("lepton_phi", "LHEPart_phi[lepton_mask]")
    .Define("lepton_mass", "LHEPart_mass[lepton_mask]")
    .Define("Lepton_fourvec", "lepFourVec(lepton_pt, lepton_eta, lepton_phi, lepton_mass)")
    .Define("lepton_inv_mass", "(Lepton_fourvec[0]+Lepton_fourvec[1]).M()")
)

rdf_empty = rdf.Filter(" LHE_Vpt<50 || LHE_Vpt > 100 || lepton_inv_mass <50")
empty_histos = rdf_empty.Histo1D(("lepton_inv_mass_empty", "lepton_inv_mass_empty", 200, -10, 200),"lepton_inv_mass")
c=ROOT.TCanvas()
empty_histos.Draw()
c.SaveAs("empty.png")
# print elemts of rdf_empty
for val in rdf_empty.AsNumpy()["lepton_inv_mass"]:
    print(val)

histo_lep=rdf.Histo1D(("lepton_inv_mass", "lepton_inv_mass", 200, 0., 200),"lepton_inv_mass")
c2=ROOT.TCanvas()
histo_lep.Draw()
c2.SaveAs("inv_mass.png")


'''histo_mu=rdf.Histo1D(("muon_inv_mass", "muon_inv_mass", 200, 0., 200),"muon_inv_mass")
histo_el=rdf.Histo1D(("electron_inv_mass", "electron_inv_mass", 200, 0., 200),"electron_inv_mass")
histo_tau=rdf.Histo1D(("tau_inv_mass", "tau_inv_mass", 200, 0., 200),"tau_inv_mass")
print(type(histo_mu))
#histo_sum=ROOT.TH1.Add(histo_mu, histo_el)
c=ROOT.TCanvas()
histo_el.Draw()
histo_mu.Draw("same")
histo_tau.Draw("same")
c.SaveAs("inv_mass.png")


histo_ht=rdf.Histo1D(("HT", "HT", 400, 300, 700),"LHE_HT")
c1=ROOT.TCanvas()
histo_ht.Draw()
c1.SaveAs("HT.png")
'''

histo_z=rdf.Histo1D(("LHE_Vpt", "LHE_Vpt", 400, -10, 110),"LHE_Vpt")
c1=ROOT.TCanvas()
histo_z.Draw()
c1.SaveAs("z.png")
