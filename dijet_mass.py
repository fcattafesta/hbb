import ROOT
import numpy as np
from array import array

# Define a dictionary to store the ROOT files
root_files = {
    "Jet_pt":["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH/ZH_Histos.root", "Dijets_mass___SR_mm"],
    "Jet_pt_Nom":["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_sf/ZH_Histos.root", "Dijets_mass___SR_mm"],
    "Jet_pt_jerUp"  :["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_sf/ZH_Histos.root", "Dijets_mass__syst__JERUp___SR_mm__syst__JERUp"],
    "Jet_pt_jerDown":["/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_sf/ZH_Histos.root", "Dijets_mass__syst__JERDown___SR_mm__syst__JERDown"],
}

histos={}
histos_pt={}

pts=["GenJet_pt___SR_mm", "Jet_pt___SR_mm", "Jet_pt_Nom___SR_mm", "Jet_pt_jerUp___SR_mm", "Jet_pt_jerDown___SR_mm"]
rebinning=list(np.linspace(50, 200, 100))
files={}
# Loop over the file names and add them to the dictionary
for type, names in root_files.items():
    files[type] = ROOT.TFile.Open(names[0])
    histos[type] = files[type].Get(names[1]).Rebin(len(rebinning)-1, "hnew"+type, array("d", rebinning))
    if type=="Jet_pt_Nom":
        for pt in pts:
            histos_pt[pt] = files[type].Get(pt)#.Rebin(len(rebinning)-1, "hnew"+pt, array("d", rebinning))

print(histos_pt)
colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange]

c=ROOT.TCanvas()
legend=ROOT.TLegend()
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
c.SaveAs("dijet_mass.root")

c1=ROOT.TCanvas()
legend1=ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
for i, pt in enumerate(histos_pt):
    h=histos_pt[pt]
    h.SetLineColor(colors[i])
    legend1.AddEntry(h, pt, "l")
    if i==0:
        h.SetMaximum(max([h.GetMaximum() for h in histos_pt.values()])*1.1)
        h.Draw("hist")
    else:
        h.Draw("hist same")
legend1.Draw()
c1.Draw()
c1.SaveAs("jet_pt.png")
c1.SaveAs("jet_pt.root")
