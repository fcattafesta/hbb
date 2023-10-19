import ROOT
import array
from plot import makeText, makeLegend
from rebinning import rebin
from labelDict import labelVariable

ROOT.gROOT.ProcessLine(".x setTDRStyle.C")
ROOT.gStyle.SetOptStat(0)

histo_list = [
    "atanhDNN_Score",
    "Z_mass",
    "Z_pt",
    "Dijets_mass",
    "Dijets_pt",
    "JetBtagMax_pt",
    "JetBtagMin_pt",
    "HZ_ptRatio",
]
lumi = 1  # 59970
xsec = 1  # 88.36

for histo in histo_list:
    f1 = ROOT.TFile.Open("/home/filippo/Downloads/oversampling485723929_single.root")
    oversampled = f1.Get(histo + "___SR_ee")
    f2 = ROOT.TFile.Open("/home/filippo/Downloads/full485723929_single.root")
    full = f2.Get(histo + "___SR_ee")

    # Rebin the histograms
    if histo in rebin.keys():
        bins = array.array("d", rebin[histo])
        full = full.Rebin(len(bins) - 1, "full", bins)
        oversampled = oversampled.Rebin(len(bins) - 1, "oversampled", bins)

    for i in range(1, full.GetNbinsX() + 1):
        scale = full.GetBinContent(i)
        if scale != 0:
            lumi = 1 / scale

    # Normalize the histograms
    full.Scale(lumi * xsec)
    oversampled.Scale(lumi * xsec)

    # full.Scale(1 / full.Integral())
    # oversampled.Scale(1 / oversampled.Integral())

    # Set histogram styles
    full.SetTitle("")
    full.SetLineColor(ROOT.kBlack)
    full.SetLineWidth(2)
    full.SetLineStyle(2)

    oversampled.SetTitle("")
    oversampled.SetLineColor(ROOT.kAzure + 1)
    oversampled.SetLineWidth(2)
    oversampled.SetLineStyle(1)

    full.GetYaxis().SetTitle("Entries")
    full.GetYaxis().SetTitleSize(0.04)
    full.GetYaxis().SetTitleOffset(1.1)
    full.GetYaxis().SetLabelSize(0.03)

    # Make the plot
    c = ROOT.TCanvas("c", "c", 800, 800)
    c.SetLogy()

    full.Draw("hist")
    oversampled.Draw("hist same")

    full.SetMaximum(20)
    full.SetMinimum(1e-5)

    full.GetXaxis().SetTitle(labelVariable[histo])
    full.GetXaxis().SetTitleSize(0.04)
    full.GetXaxis().SetTitleOffset(1.1)
    full.GetXaxis().SetLabelSize(0.03)

    # Make the legend
    leg = makeLegend(0.68, 0.93, 0.75, 0.9)
    leg.AddEntry(full, "FullSim", "f")
    leg.AddEntry(oversampled, "FlashSim (#times 10000)", "f")

    t0 = makeText(
        0.2,
        0.88,
        "Signal Region (1 Event)",
        42,
        size=0.03,
    )
    t1 = makeText(0.18, 0.95, "CMS", 61)
    t2 = makeText(
        0.2,
        0.83,
        "Electrons DY 100 < p^{  Z}_{  T} < 250 GeV",
        42,
        size=0.03,
    )
    t3 = makeText(0.7, 0.95, "(13 TeV)", 42)
    t4 = makeText(0.38, 0.95, "2018", 42)

    # Draw the text
    c.cd()
    t0.Draw()
    t1.Draw()
    t2.Draw()
    t3.Draw()
    t4.Draw()

    leg.Draw()

    c.SaveAs(f"figures_os/single_event/{histo}.pdf")