import ROOT
import array
from plot import makeText, makeLegend
from rebinning import rebin
from labelDict import labelVariable

ROOT.gROOT.ProcessLine(".x setTDRStyle.C")

# normalize = False
normalize = True

samples = {
    "DYZpt-0To50": {
        "xsec": 1341.42,
    },
    "DYZpt-50To100": {
        "xsec": 359.52,
    },
    "DYZpt-100To250": {
        "xsec": 88.36,
    },
    "DYZpt-250To400": {
        "xsec": 3.52,
    },
    "DYZpt-400To650": {
        "xsec": 0.49,
    },
    "DYZpt-650ToInf": {
        "xsec": 0.05,
    },
    "ZH": {
        "xsec": 0.880 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
    },
    "ggZH": {
        "xsec": 0.123 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
    },
}

model = {
    "DY": [
        "DYZpt-0To50",
        "DYZpt-50To100",
        "DYZpt-100To250",
        "DYZpt-250To400",
        "DYZpt-400To650",
        "DYZpt-650ToInf",
    ],
    "ZH": ["ZH", "ggZH"],
}

lumi = 59970

# Drell-Yan Histogram
for sample in model["DY"]:
    # f = ROOT.TFile.Open(
    #     f"/home/filippo/Downloads/FlashSimFinal_deepflav_NOsnap_eval/{sample}Full_Histos.root"
    # )
    f = ROOT.TFile.Open(
        f"/home/filippo/Downloads/MuonFlashNoOppositeSign_deepflav_NOsnap_eval//{sample}Full_Histos.root"
    )
    tmp_full_dy = f.Get("atanhDNN_Score___SR_mm")
    tmp_full_dy.AddDirectory(ROOT.kFALSE)
    bins = array.array("d", rebin["atanhDNN_Score"])
    tmp_full_dy = tmp_full_dy.Rebin(len(bins) - 1, "full_dy", bins)
    tmp_full_dy.Scale(lumi * samples[sample]["xsec"])
    if sample == "DYZpt-0To50":
        full_dy = tmp_full_dy.Clone()
    else:
        full_dy.Add(tmp_full_dy)

    # f_flash = ROOT.TFile.Open(
    #     f"/home/filippo/Downloads/FlashSimFinal_deepflav_NOsnap_eval/{sample}_Histos.root"
    # )
    f_flash = ROOT.TFile.Open(
        f"/home/filippo/Downloads/MuonFlashNoOppositeSign_deepflav_NOsnap_eval//{sample}_Histos.root"
    )
    tmp_flash_dy = f_flash.Get("atanhDNN_Score___SR_mm")
    tmp_flash_dy.AddDirectory(ROOT.kFALSE)
    tmp_flash_dy = tmp_flash_dy.Rebin(len(bins) - 1, "flash_dy", bins)
    tmp_flash_dy.Scale(lumi * samples[sample]["xsec"])
    if sample == "DYZpt-0To50":
        flash_dy = tmp_flash_dy.Clone()
    else:
        flash_dy.Add(tmp_flash_dy)


# ZH Histogram
for sample in model["ZH"]:
    # f = ROOT.TFile.Open(
    #     f"/home/filippo/Downloads/FlashSignal_deepflav_NOsnap_eval/{sample}Full_Histos.root"
    # )
    f = ROOT.TFile.Open(
        f"/home/filippo/Downloads/MuonFlashSignalNoOppositeSign_deepflav_NOsnap_eval/{sample}Full_Histos.root"
    )
    tmp_full_zh = f.Get("atanhDNN_Score___SR_mm")
    tmp_full_zh.AddDirectory(ROOT.kFALSE)
    bins = array.array("d", rebin["atanhDNN_Score"])
    tmp_full_zh = tmp_full_zh.Rebin(len(bins) - 1, "full_zh", bins)
    tmp_full_zh.Scale(lumi * samples[sample]["xsec"])
    if sample == "ZH":
        full_zh = tmp_full_zh.Clone()
    else:
        full_zh.Add(tmp_full_zh)

    # f_flash = ROOT.TFile.Open(
    #     f"/home/filippo/Downloads/FlashSignal_deepflav_NOsnap_eval/{sample}_Histos.root"
    # )
    f_flash = ROOT.TFile.Open(
        f"/home/filippo/Downloads/MuonFlashSignalNoOppositeSign_deepflav_NOsnap_eval/{sample}_Histos.root"
    )
    tmp_flash_zh = f_flash.Get("atanhDNN_Score___SR_mm")
    tmp_flash_zh.AddDirectory(ROOT.kFALSE)
    tmp_flash_zh = tmp_flash_zh.Rebin(len(bins) - 1, "flash_zh", bins)
    tmp_flash_zh.Scale(lumi * samples[sample]["xsec"])
    if sample == "ZH":
        flash_zh = tmp_flash_zh.Clone()
    else:
        flash_zh.Add(tmp_flash_zh)


if normalize:
    full_dy.Scale(1.0 / full_dy.Integral())
    flash_dy.Scale(1.0 / flash_dy.Integral())
    full_zh.Scale(1.0 / full_zh.Integral())
    flash_zh.Scale(1.0 / flash_zh.Integral())
    full_dy.GetYaxis().SetRangeUser(1e-3, 1e3)
else:
    full_dy.GetYaxis().SetRangeUser(1e-1, 1e6)

nbins = full_dy.GetNbinsX()
full_dy_rebin = ROOT.TH1F("full_dy_rebin", "", nbins, 0.5, nbins + 0.5)
flash_dy_rebin = full_dy_rebin.Clone()
full_zh_rebin = full_dy_rebin.Clone()
flash_zh_rebin = full_dy_rebin.Clone()

for i in range(1, nbins + 1):
    full_dy_rebin.SetBinContent(i, full_dy.GetBinContent(i))
    full_dy_rebin.SetBinError(i, full_dy.GetBinError(i))
    flash_dy_rebin.SetBinContent(i, flash_dy.GetBinContent(i))
    flash_dy_rebin.SetBinError(i, flash_dy.GetBinError(i))
    full_zh_rebin.SetBinContent(i, full_zh.GetBinContent(i))
    full_zh_rebin.SetBinError(i, full_zh.GetBinError(i))
    flash_zh_rebin.SetBinContent(i, flash_zh.GetBinContent(i))
    flash_zh_rebin.SetBinError(i, flash_zh.GetBinError(i))


ROOT.gStyle.SetOptStat(0)
c = ROOT.TCanvas("c", "c", 800, 800)
legend = makeLegend(0.62, 0.9, 0.68, 0.9)

full_dy_rebin.SetTitle("")
full_dy_rebin.SetLineColor(ROOT.kGreen + 3)
full_dy_rebin.SetLineWidth(2)
full_dy_rebin.SetLineStyle(2)

flash_dy_rebin.SetTitle("")
flash_dy_rebin.SetLineColor(ROOT.kGreen - 4)
flash_dy_rebin.SetLineWidth(2)
flash_dy_rebin.SetLineStyle(1)

full_zh_rebin.SetTitle("")
full_zh_rebin.SetLineColor(ROOT.kRed + 3)
full_zh_rebin.SetLineWidth(2)
full_zh_rebin.SetLineStyle(2)

flash_zh_rebin.SetTitle("")
flash_zh_rebin.SetLineColor(ROOT.kRed - 4)
flash_zh_rebin.SetLineWidth(2)
flash_zh_rebin.SetLineStyle(1)

legend.AddEntry(full_dy_rebin, "DY FullSim", "f")
legend.AddEntry(flash_dy_rebin, "DY FlashSim", "f")
legend.AddEntry(full_zh_rebin, "ZH(bb) FullSim", "f")
legend.AddEntry(flash_zh_rebin, "ZH(bb) FlashSim", "f")

full_dy_rebin.Draw("hist")
flash_dy_rebin.Draw("hist same")
full_zh_rebin.Draw("hist same")
flash_zh_rebin.Draw("hist same")

legend.SetTextSize(0.025)
legend.Draw()

full_dy_rebin.GetYaxis().SetTitle("Normalized Entries")
full_dy_rebin.GetYaxis().SetTitleOffset(1.4)
full_dy_rebin.GetYaxis().SetTitleSize(0.05)
full_dy_rebin.GetYaxis().SetLabelSize(0.04)
full_dy_rebin.GetXaxis().SetTitle("DNN Score Bin")
full_dy_rebin.GetXaxis().SetTitleSize(0.05)
full_dy_rebin.GetXaxis().SetLabelSize(0.04)
full_dy_rebin.GetXaxis().SetTitleOffset(1.1)
full_dy_rebin.GetYaxis().SetRangeUser(1e-3, 1e1)
t0 = makeText(
    0.2,
    0.89,
    "Signal Region",
    42,
    size=0.04,
)
t1 = makeText(0.26, 0.95, "CMS", 61)
t2 = makeText(
    0.2,
    0.85,
    "Muons",
    42,
    size=0.04,
)
t3 = makeText(0.7, 0.95, "(13 TeV)", 42)
t4 = makeText(0.38, 0.95, "2018", 42)

t0.Draw()
t1.Draw()
t2.Draw()
t3.Draw()
t4.Draw()

c.SetLogy()
c.SaveAs("DNN_plot_mm.pdf")
