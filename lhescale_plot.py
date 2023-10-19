import ROOT
import array
from plot import makeText, makeLegend
from rebinning import rebin
from labelDict import labelVariable

ROOT.gROOT.ProcessLine(".x setTDRStyle.C")

histo_list = ["HZ_ptRatio", "Dijets_pt", "jj_deta"]

lumi = 59970
xsec = 88.36

for histo in histo_list:
    # f1 = ROOT.TFile.Open("/home/filippo/Downloads/FullDY_nom.root")
    # full_nom = f1.Get(histo + "___SR_ee")
    # f2 = ROOT.TFile.Open("/home/filippo/Downloads/FullDY_7.root")
    # full_up = f2.Get(histo + "___SR_ee")
    # f3 = ROOT.TFile.Open("/home/filippo/Downloads/FullDY_1.root")
    # full_down = f3.Get(histo + "___SR_ee")

    f1 = ROOT.TFile.Open("/home/filippo/Downloads/FlashOverDY_nom.root")
    full_nom = f1.Get(histo + "___SR_ee")
    f2 = ROOT.TFile.Open("/home/filippo/Downloads/FlashOverDY_7.root")
    full_up = f2.Get(histo + "___SR_ee")
    f3 = ROOT.TFile.Open("/home/filippo/Downloads/FlashOverDY_1.root")
    full_down = f3.Get(histo + "___SR_ee")

    # Rebin the histograms
    if histo in rebin.keys():
        bins = array.array("d", rebin[histo])
        full_nom = full_nom.Rebin(len(bins) - 1, "full_nom", bins)
        full_up = full_up.Rebin(len(bins) - 1, "full_up", bins)
        full_down = full_down.Rebin(len(bins) - 1, "full_down", bins)

    # Normalize the histograms
    full_nom.Scale(1 / full_nom.Integral())
    full_up.Scale(1 / full_up.Integral())
    full_down.Scale(1 / full_down.Integral())

    # Set histogram styles
    full_nom.SetTitle("")
    full_nom.SetLineColor(ROOT.kBlack)
    full_nom.SetLineWidth(2)
    full_nom.SetLineStyle(1)

    full_up.SetTitle("")
    full_up.SetLineColor(ROOT.kRed + 1)
    full_up.SetLineWidth(2)
    full_up.SetLineStyle(1)

    full_down.SetTitle("")
    full_down.SetLineColor(ROOT.kBlue + 1)
    full_down.SetLineWidth(2)
    full_down.SetLineStyle(1)

    # Make the plot + ratio plot
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c", "c", 800, 800)
    c.Divide(1, 2)
    c.GetPad(1).SetPad(0, 0.3, 1, 1)
    c.GetPad(2).SetPad(0, 0.0, 1, 0.3)

    # Set the margins
    c.GetPad(1).SetTopMargin(0.065)
    c.GetPad(1).SetBottomMargin(0.01)
    c.GetPad(2).SetTopMargin(0.08)
    c.GetPad(2).SetBottomMargin(0.35)

    c.GetPad(1).cd()
    c.GetPad(2).cd()

    c.GetPad(1).cd()
    legend = makeLegend(0.7, 0.95, 0.78, 0.92)
    legend.SetTextSize(0.023)

    full_nom.Draw("hist")
    full_up.Draw("hist same")
    full_down.Draw("hist same")

    full_nom.GetYaxis().SetTitle("Normalized Events")
    full_nom.GetYaxis().SetTitleSize(0.05)
    full_nom.GetYaxis().SetTitleOffset(1.1)
    full_nom.GetYaxis().SetLabelSize(0.04)
    full_nom.GetYaxis().SetRangeUser(0.7e-3, 1)

    legend.AddEntry(full_nom, "Reference", "f")
    legend.AddEntry(full_up, "Up variation", "f")
    legend.AddEntry(full_down, "Down variation", "f")

    # Make the ratio plot
    c.GetPad(2).cd()
    ratio_up = full_up.Clone()
    ratio_up.Divide(full_nom)
    ratio_up.SetTitle("")

    ratio_down = full_down.Clone()
    ratio_down.Divide(full_nom)
    ratio_down.SetTitle("")

    ratio_up.Draw("hist")
    ratio_down.Draw("hist same")

    ratio_up.GetYaxis().SetTitle("Ratio")
    ratio_up.GetYaxis().SetTitleSize(0.1)
    ratio_up.GetYaxis().SetTitleOffset(0.6)
    ratio_up.GetYaxis().SetLabelSize(0.09)

    ratio_up.GetXaxis().SetTitleSize(0.1)
    ratio_up.GetXaxis().SetLabelSize(0.09)
    ratio_up.GetXaxis().SetTitle(labelVariable[histo])
    ratio_up.GetYaxis().SetRangeUser(0.91, 1.1)
    ratio_up.GetYaxis().SetNdivisions(8)

    if histo == "jj_deta":
        ratio_up.GetXaxis().SetRangeUser(0, 3)
        full_nom.GetXaxis().SetRangeUser(0, 3)

    # Text
    t0 = makeText(
        0.2,
        0.91,
        "Signal Region",
        42,
        size=0.03,
    )
    t1 = makeText(0.18, 0.96, "CMS", 61)
    tl = makeText(0.3, 0.96, "Private Work", 52)
    t2 = makeText(
        0.2,
        0.88,
        "Electrons DY 100 < p^{  Z}_{  T} < 250 GeV",
        42,
        size=0.03,
    )
    t3 = makeText(0.8, 0.96, "(13 TeV)", 42)
    t4 = makeText(0.65, 0.96, "2018", 42)
    t5 = makeText(0.2, 0.85, "LHEScaleWeight", 42, size=0.03)
    # t6 = makeText(0.2, 0.82, "FullSim", 42, size=0.03)
    t6 = makeText(0.2, 0.82, "FlashSim ( #times 5)", 42, size=0.03)

    # Draw the text
    c.cd()
    t0.Draw()
    t1.Draw()
    t2.Draw()
    t3.Draw()
    t4.Draw()
    t5.Draw()
    tl.Draw()
    t6.Draw()

    legend.Draw()
    c.GetPad(1).SetLogy()
    c.GetPad(2).SetGridy()
    c.Update()
    c.SaveAs(f"LHEScale/{histo}_over.pdf")
    c.SaveAs(f"LHEScale/{histo}_over.png")
    # c.SaveAs(f"LHEScale/{histo}.pdf")
    # c.SaveAs(f"LHEScale/{histo}.png")
