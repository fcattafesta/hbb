import ROOT
from plot import makeText, makeLegend
import array

ROOT.gROOT.ProcessLine(".x setTDRStyle.C")


# Get the DNN score histograms
f1 = ROOT.TFile.Open(
    "/gpfs/ddn/cms/user/cattafe/hbb_out/el/deepflav_sys_eval_rescalebtag/DYZpt-100To250_Histos.root"
)
full = f1.Get("atanhDNN_Score___SR_ee")
f2 = ROOT.TFile.Open(
    "/gpfs/ddn/cms/user/cattafe/hbb_out/el/DNN_deepflav_NOsnap_eval//DYZpt-100To250_Histos.root"
)
flash = f2.Get("atanhDNN_Score___SR_ee")
f3 = ROOT.TFile.Open(
    "/gpfs/ddn/cms/user/cattafe/hbb_out/el/OversamplingFinal_deepflav_NOsnap_eval/DYZpt-100To250_Histos.root"
)
overflash = f3.Get("atanhDNN_Score___SR_ee")

# Make 3 random filled histograms
# full = ROOT.TH1F("full", "full", 10, -1, 1)
# flash = ROOT.TH1F("flash", "flash", 10, -1, 1)
# overflash = ROOT.TH1F("overflash", "overflash", 10, -1, 1)

# full.FillRandom("gaus", 10000)
# flash.FillRandom("gaus", 10000)
# overflash.FillRandom("gaus", 10000)

lumi = 59970
xsec = 88.36

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
c.GetPad(3).SetTopMargin(0.1)
c.GetPad(3).SetBottomMargin(0.42)

c.GetPad(1).SetFillStyle(4000)
c.GetPad(2).SetFillStyle(4000)
c.GetPad(3).SetFillStyle(4000)

c.GetPad(1).Draw()
c.GetPad(2).Draw()
c.GetPad(3).Draw()

# Draw the histograms in the upper pad

c.GetPad(1).cd()
c.GetPad(1).SetLogy()
legend = makeLegend(0.7, 0.9, 0.85, 0.95)

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
ratio1.Draw("E1 hist")

ratio2 = overflash.Clone("ratio2")
ratio2.Divide(full)
ratio2.SetMarkerStyle(20)
ratio2.SetMarkerColor(ROOT.kAzure + 1)
ratio2.Draw("E1 hist same")

ratio1.GetXaxis().SetTitle("")
ratio1.GetXaxis().SetTitleSize(0)
ratio1.GetXaxis().SetLabelSize(0)

ratio1.GetYaxis().SetTitle("Ratio")
ratio1.GetYaxis().SetTitleSize(0.15)
ratio1.GetYaxis().SetTitleOffset(0.3)
ratio1.GetYaxis().SetLabelSize(0.12)
ratio1.GetYaxis().SetRangeUser(0.5, 1.5)
ratio1.GetYaxis().SetNdivisions(5)

# Draw the error for each bin for each histogram
c.GetPad(3).cd()
c.GetPad(3).SetGridy()
error1 = full.Clone("error1")
error2 = full.Clone("error2")
error3 = full.Clone("error3")

for i in range(1, error1.GetNbinsX() + 1):
    error1.SetBinContent(i, full.GetBinError(i) / full.GetBinContent(i))
    error2.SetBinContent(i, flash.GetBinError(i) / flash.GetBinContent(i))
    error3.SetBinContent(i, overflash.GetBinError(i) / overflash.GetBinContent(i))

error1.SetMarkerStyle(20)
error1.SetMarkerColor(ROOT.kBlack)
error1.SetLineColor(ROOT.kBlack)
error1.SetLineWidth(2)
error1.SetLineStyle(2)
error1.Draw("P hist same")

error2.SetMarkerStyle(21)
error2.SetMarkerColor(ROOT.kOrange + 8)
error2.SetLineColor(ROOT.kOrange + 8)
error2.SetLineWidth(2)
error2.SetLineStyle(1)
error2.Draw("P hist same")

error3.SetMarkerStyle(22)
error3.SetMarkerColor(ROOT.kAzure + 1)
error3.SetLineColor(ROOT.kAzure + 1)
error3.SetLineWidth(2)
error3.SetLineStyle(1)
error3.Draw("P hist same")

error1.GetYaxis().SetTitle("Rel. Unc.")
error1.GetYaxis().SetTitleSize(0.075)
error1.GetYaxis().SetTitleOffset(0.6)
error1.GetYaxis().SetLabelSize(0.07)
error1.GetYaxis().SetMaxDigits(2)
# error1.GetYaxis().SetRangeUser(0, 0.04)
error1.GetYaxis().SetNdivisions(5)

c.cd()
error1.GetXaxis().SetTitle("atanh(DNN Score)")
error1.GetXaxis().SetTitleSize(0.1)
error1.GetXaxis().SetTitleOffset(1.1)
error1.GetXaxis().SetLabelSize(0.07)


# Text
t0 = makeText(
    0.2,
    0.92,
    "Signal Region",
    42,
    size=0.04,
)
t1 = makeText(0.18, 0.97, "CMS", 61)
t2 = makeText(
    0.2,
    0.87,
    "Electrons",
    42,
    size=0.04,
)
t3 = makeText(0.7, 0.97, "(13 TeV)", 42)
t4 = makeText(0.38, 0.97, "2018", 42)


# Draw the text
c.cd()
t0.Draw()
t1.Draw()
t2.Draw()
t3.Draw()
t4.Draw()

legend.Draw()


c.SaveAs("dnn_score_comparison.pdf")
