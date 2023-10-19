import ROOT
import array
from plot import makeText, makeLegend
from rebinning import rebin
from labelDict import labelVariable, labelStatUncRange

ROOT.gROOT.ProcessLine(".x setTDRStyle.C")


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


lumi = 59970
xsec = 88.36

for histo in histo_list:
    f1 = ROOT.TFile.Open("/home/filippo/Downloads/full_nosf20.root")
    full = f1.Get(histo + "___SR_ee")
    f2 = ROOT.TFile.Open("/home/filippo/Downloads/flash_20.root")
    flash = f2.Get(histo + "___SR_ee")
    f3 = ROOT.TFile.Open("/home/filippo/Downloads/overflash_20.root")
    overflash = f3.Get(histo + "___SR_ee")

    # Rebin the histograms
    if histo in rebin.keys():
        bins = array.array("d", rebin[histo])
        full = full.Rebin(len(bins) - 1, "full", bins)
        flash = flash.Rebin(len(bins) - 1, "flash", bins)
        overflash = overflash.Rebin(len(bins) - 1, "overflash", bins)

    # Normalize the histograms
    full.Scale(lumi * xsec)
    flash.Scale(lumi * xsec)
    overflash.Scale(lumi * xsec)

    # Set histogram styles
    full.SetTitle("")
    full.SetLineColor(ROOT.kBlack)
    full.SetLineWidth(2)
    full.SetLineStyle(2)

    flash.SetTitle("")
    flash.SetLineColor(ROOT.kOrange + 8)
    flash.SetLineWidth(2)
    flash.SetLineStyle(1)

    overflash.SetTitle("")
    overflash.SetLineColor(ROOT.kAzure + 1)
    overflash.SetLineWidth(2)
    overflash.SetLineStyle(1)

    full.GetYaxis().SetTitle("Entries")
    full.GetYaxis().SetTitleSize(0.05)
    full.GetYaxis().SetTitleOffset(1.1)
    full.GetYaxis().SetLabelSize(0.04)

    full.GetXaxis().SetTitleSize(0)
    full.GetXaxis().SetLabelSize(0)

    # Create a canvas with 3 pads
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c", "c", 800, 1200)
    c.Divide(1, 3)
    c.GetPad(1).SetPad(0, 0.45, 1, 1)
    c.GetPad(2).SetPad(0, 0.3, 1, 0.45)
    c.GetPad(3).SetPad(0, 0.0, 1, 0.3)

    # Set the margins
    c.GetPad(1).SetTopMargin(0.065)
    c.GetPad(1).SetBottomMargin(0.0)
    c.GetPad(2).SetTopMargin(0.06)
    c.GetPad(2).SetBottomMargin(0.0)
    c.GetPad(3).SetTopMargin(0.03)
    c.GetPad(3).SetBottomMargin(0.5)

    c.GetPad(1).SetFillStyle(4000)
    c.GetPad(2).SetFillStyle(4000)
    c.GetPad(3).SetFillStyle(4000)

    c.GetPad(1).Draw()
    c.GetPad(2).Draw()
    c.GetPad(3).Draw()

    # Draw the histograms in the upper pad

    c.GetPad(1).cd()
    legend = makeLegend(0.65, 0.9, 0.8, 0.95)

    full.Draw("hist")
    flash.Draw("hist same")
    overflash.Draw("hist same")

    legend.AddEntry(full, "FullSim", "f")
    legend.AddEntry(flash, "FlashSim", "f")
    legend.AddEntry(overflash, "FlashSim (#times 5)", "f")

    # Draw the ratio histograms in the middle pad
    c.GetPad(2).cd()
    c.GetPad(2).SetGridy()
    ratio1 = flash.Clone("ratio1")
    ratio1.SetMarkerStyle(20)
    ratio1.SetMarkerColor(ROOT.kOrange + 8)
    ratio1.Divide(full)
    ratio1.Draw("E1 ")

    ratio2 = overflash.Clone("ratio2")
    ratio2.Divide(full)
    ratio2.SetMarkerStyle(20)
    ratio2.SetMarkerColor(ROOT.kAzure + 1)
    ratio2.Draw("E1 same")

    # draw a black dotted line at 1
    line = ROOT.TLine(ratio1.GetXaxis().GetXmin(), 1, ratio1.GetXaxis().GetXmax(), 1)
    line.SetLineColor(ROOT.kBlack)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw("same")

    ratio1.GetXaxis().SetTitle("")
    ratio1.GetXaxis().SetTitleSize(0)
    ratio1.GetXaxis().SetLabelSize(0)

    ratio1.GetYaxis().SetTitle("Ratio")
    ratio1.GetYaxis().SetTitleSize(0.17)
    ratio1.GetYaxis().SetTitleOffset(0.3)
    ratio1.GetYaxis().SetLabelSize(0.15)
    ratio1.GetYaxis().SetRangeUser(0.5, 1.5)
    ratio1.GetYaxis().SetNdivisions(5)

    # Draw the error for each bin for each histogram
    c.GetPad(3).cd()
    c.GetPad(3).SetGridy()
    error1 = full.Clone("error1")
    error2 = error1.Clone("error2")
    error3 = error2.Clone("error3")

    for i in range(1, error1.GetNbinsX() + 1):
        if full.GetBinContent(i) == 0:
            error1.SetBinContent(i, -5)
        else:
            error1.SetBinContent(i, full.GetBinError(i) / full.GetBinContent(i))
        if flash.GetBinContent(i) == 0:
            error2.SetBinContent(i, -5)
        else:
            error2.SetBinContent(i, flash.GetBinError(i) / flash.GetBinContent(i))
        if overflash.GetBinContent(i) == 0:
            error3.SetBinContent(i, -5)
        else:
            error3.SetBinContent(
                i, overflash.GetBinError(i) / overflash.GetBinContent(i)
            )

    error3.SetMarkerStyle(22)
    error3.SetMarkerColor(ROOT.kAzure + 1)
    error3.SetMarkerSize(1.1)
    error3.SetLineColor(ROOT.kAzure + 1)
    error3.SetLineWidth(2)
    error3.SetLineStyle(1)

    error1.SetMarkerStyle(20)
    error1.SetMarkerColor(ROOT.kBlack)
    error1.SetLineColor(ROOT.kBlack)
    error1.SetLineWidth(2)
    error1.SetLineStyle(2)

    error2.SetMarkerStyle(21)
    error2.SetMarkerColor(ROOT.kOrange + 8)
    error2.SetMarkerSize(1.1)
    error2.SetLineColor(ROOT.kOrange + 8)
    error2.SetLineWidth(2)
    error2.SetLineStyle(1)

    # error3.SetMaximum(0.3)
    # error3.SetMinimum(-0.1)

    error3.GetYaxis().SetTitle("Rel. Unc.")
    error3.GetYaxis().SetTitleSize(0.075)
    error3.GetYaxis().SetTitleOffset(0.7)
    error3.GetYaxis().SetLabelSize(0.07)
    error3.GetYaxis().SetMaxDigits(5)
    # error3.GetYaxis().SetRangeUser(0, 0.04)
    error3.GetYaxis().SetNdivisions(10)

    error3.GetXaxis().SetTitle(labelVariable[histo])
    error3.GetXaxis().SetTitleSize(0.1)
    error3.GetXaxis().SetTitleOffset(1.1)
    error3.GetXaxis().SetLabelSize(0.07)

    error3.Draw("P hist")
    error2.Draw("P hist same")
    error1.Draw("P hist same")

    error3.GetYaxis().SetRangeUser(-0.1, 0.3)
    error3.GetYaxis().UnZoom()
    error3.GetYaxis().SetRangeUser(
        *labelStatUncRange[histo] if histo in labelStatUncRange.keys() else (-0.1, 0.3)
    )

    # Text
    t0 = makeText(
        0.2,
        0.92,
        "Signal Region",
        42,
        size=0.03,
    )
    t1 = makeText(0.18, 0.97, "CMS", 61)
    tl = makeText(0.3, 0.97, "Private Work", 52)
    t2 = makeText(
        0.2,
        0.87,
        "Electrons DY 100 < p^{  Z}_{  T} < 250 GeV",
        42,
        size=0.03,
    )
    t3 = makeText(0.8, 0.97, "(13 TeV)", 42)
    t4 = makeText(0.65, 0.97, "2018", 42)

    # Draw the text
    c.cd()
    t0.Draw()
    t1.Draw()
    t2.Draw()
    t3.Draw()
    t4.Draw()
    tl.Draw()

    legend.Draw()
    c.GetPad(1).SetLogy()
    full.GetYaxis().SetRangeUser(2e-1, 5e4)
    c.Update()
    c.SaveAs(f"figures_os/{histo}.pdf")
