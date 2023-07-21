import ROOT
import numpy as np
from array import array
from plot import makeText, makeLegend

ROOT.gROOT.ProcessLine(".x setTDRStyle.C")
ROOT.gStyle.SetOptStat(0)

#/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH/
#/gpfs/ddn/cms/user/malucchi/hbb_out/mu/deepflav_testZH_sf/
root_files = {
    "Jet_pt":["ZH_Histos.root", "Dijets_mass___SR_mm"],
    "Jet_pt_jerNom":["ZH_Histos_sf_2.root", "Dijets_mass___SR_mm"],
    "Jet_pt_jerUp"  :["ZH_Histos_sf_2.root", "Dijets_mass__syst__JERUp___SR_mm__syst__JERUp"],
    "Jet_pt_jerDown":["ZH_Histos_sf_2.root", "Dijets_mass__syst__JERDown___SR_mm__syst__JERDown"],
}

t0 = makeText(0.2, 0.95, "CMS", 61)
t1 = makeText(0.8, 0.95,"(13 TeV)", 42)

histos={}
histos_pt={}

pts=["GenJet_pt___SR_mm", "Jet_pt___SR_mm", "Jet_pt_jerNom___SR_mm", "Jet_pt_jerUp___SR_mm", "Jet_pt_jerDown___SR_mm"]
rebinning=list(np.linspace(50, 200, 40))
files={}
sumws={}
# Loop over the file names and add them to the dictionary
for type, names in root_files.items():
    files[type] = ROOT.TFile.Open(names[0])
    h=files[type].Get(names[1]).Rebin(len(rebinning)-1, "hnew"+type, array("d", rebinning))
    sumws[type]=files[type].Get("sumWeights")
    histos[type] = h
    if type=="Jet_pt_jerNom":
        for pt in pts:
            histos_pt[pt] = files[type].Get(pt)#.Rebin(len(rebinning)-1, "hnew"+pt, array("d", rebinning))

print(histos_pt)
colors=[ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange]

gen_weight=histos["Jet_pt"].GetSumOfWeights()/histos["Jet_pt"].GetEntries()

c=ROOT.TCanvas()
legend= makeLegend(0.75, 0.85, 0.7, 0.92, size=1.5)
for i, type in enumerate(histos):
    h=histos[type]
    h.SetTitle("")
    h.SetLineColor(colors[i])
    h.SetLineWidth(1)
    legend.AddEntry(h, type, "l")
    # print number of entries
    print(type, "GetSumOfWeights 1", h.GetSumOfWeights() )
    print(type, h.GetEntries())
    h.Scale(1/h.Integral())
    print(type, "sumws", sumws[type].GetVal() )
    acceptance=gen_weight*h.GetEntries()/sumws[type].GetVal()
    print("\n\n")
    if i==0:
        h.SetMaximum(max([h.GetMaximum() for h in histos.values()])*1.1)
        h.GetXaxis().SetTitle("m_{jj} [GeV]")
        binWidht = str(h.GetBinWidth(1))[:4]
        if binWidht.endswith("."):
            binWidht = binWidht[:3]
        h.GetYaxis().SetTitle(f"Norm Events / {binWidht}")
        h.SetFillColor(ROOT.kBlack)
        h.SetFillStyle(3003)
        h.Draw("hist")
    else:
        h.Draw("hist same")

legend.Draw()
t0.Draw()
t1.Draw()
c.Draw()
c.SaveAs("dijet_mass.png")
c.SaveAs("dijet_mass.root")


# c1=ROOT.TCanvas()
# legend1=makeLegend(0.58, 0.68, 0.75, 0.92)
# for i, pt in enumerate(histos_pt):
#     h=histos_pt[pt]
#     h.SetLineColor(colors[i])
#     print(type, h.GetEntries())
#     legend1.AddEntry(h, pt, "l")
#     if i==0:
#         h.SetMaximum(max([h.GetMaximum() for h in histos_pt.values()])*1.1)
#         h.Draw("hist")
#     else:
#         h.Draw("hist same")
# legend1.Draw()
# c1.Draw()
# c1.SaveAs("jet_pt.png")
# c1.SaveAs("jet_pt.root")
