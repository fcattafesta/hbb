import ROOT
import numpy as np
from array import array

# Define a dictionary to store the ROOT files
root_files = {
    "Jet_pt":["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_NOsnap/ZH_Histos.root", "Dijets_mass___SR_mm"],
    "Jet_ptNom":["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_sf_NOsnap/ZH_Histos.root", "Dijets_mass___SR_mm"],
    "Jet_pt_jerUp"  :["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_sf_NOsnap/ZH_Histos.root", "Dijets_mass__syst__JERUp___SR_mm__syst__JERUp"],
    "Jet_pt_jerDown":["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_sf_NOsnap/ZH_Histos.root", "Dijets_mass__syst__JERDown___SR_mm__syst__JERDown"],
}

histos={}

rebinning=list(np.linspace(90, 150, 100))
files={}
# Loop over the file names and add them to the dictionary
for type, names in root_files.items():
    files[type] = ROOT.TFile.Open(names[0])
    histos[type] = files[type].Get(names[1]).Rebin(len(rebinning)-1, "hnew"+type, array("d", rebinning))
    #f.Close()

print(histos)

c=ROOT.TCanvas()
legend=ROOT.TLegend()
colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen]
for i, type in enumerate(histos):
    h=histos[type]
    h.SetLineColor(colors[i])
    legend.AddEntry(h, type, "l")
    if i==0:
        h.Draw("hist")
    else:
        h.Draw("hist same")
legend.Draw()
c.Draw()
c.SaveAs("dijet_mass.png")