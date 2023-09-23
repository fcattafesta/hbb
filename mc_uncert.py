import ROOT
from rebinning import rebin
from plot import makeText, makeLegend
from labelDict import labelLegend
import array

ROOT.gROOT.ProcessLine(".x setTDRStyle.C")
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetHistTopMargin(0)

samples = [
    "DYZpt-0To50",
    "DYZpt-50To100",
    "DYZpt-100To250",
    "DYZpt-250To400",
    "DYZpt-400To650",
    "DYZpt-650ToInf",
]

files = [
    f"/home/filippo/Downloads/MCUncert/{sample}Full_Histos.root"
    if sample != "DYZpt-100To250"
    else "/home/filippo/Downloads/overflash_20.root"
    for sample in samples
]

colors = [
    ROOT.kMagenta + 1,
    ROOT.kBlue + 1,
    ROOT.kAzure + 1,
    ROOT.kGreen + 2,
    ROOT.kOrange + 1,
    ROOT.kRed + 1,
]


histos = {}
uncert_list = []


uncert = ROOT.THStack("uncert", "")
rel_uncert = ROOT.THStack("rel_uncert", "")

lumi = 59970
xsec = [1341.42, 359.52, 88.36, 3.52, 0.49, 0.05]

c1 = ROOT.TCanvas("c1", "", 800, 800)

legend = makeLegend(0.62, 0.9, 0.68, 0.9)
legend.SetTextSize(0.025)

legend_2 = makeLegend(0.62, 0.9, 0.68, 0.9)
legend_2.SetTextSize(0.025)

max = -1

for i in range(len(samples)):
    print(samples[i])
    f = ROOT.TFile.Open(files[i])
    histos[samples[i]] = f.Get("atanhDNN_Score___SR_ee")
    histos[samples[i]].AddDirectory(ROOT.kFALSE)
    new_bins = array.array("d", rebin["atanhDNN_Score"])
    histos[samples[i]] = histos[samples[i]].Rebin(
        len(rebin["atanhDNN_Score"]) - 1,
        f"{samples[i]}_rebin",
        new_bins,
    )
    histos[samples[i]].Scale(lumi * xsec[i])
    bins = histos[samples[i]].GetNbinsX()
    new_histo = ROOT.TH1F(f"{samples[i]}_new", "", bins, 0.5, bins + 0.5)
    for j in range(1, bins + 1):
        new_histo.SetBinContent(j, histos[samples[i]].GetBinContent(j))
        new_histo.SetBinError(j, histos[samples[i]].GetBinError(j))
    uncert_histo = new_histo.Clone()
    if i == 0:
        sum_histo = new_histo.Clone()
    else:
        sum_histo.Add(new_histo)
    for j in range(1, bins + 1):
        uncert_histo.SetBinContent(j, histos[samples[i]].GetBinError(j) ** 2)
        uncert_histo.SetBinError(j, 0)
    uncert_histo.SetFillColor(colors[i])
    uncert_histo.SetLineColor(ROOT.kBlack)
    uncert_histo.SetLineWidth(1)
    uncert.Add(uncert_histo)
    legend_2.AddEntry(uncert_histo, labelLegend[samples[i]], "f")
    uncert_list.append(uncert_histo)
    histos[samples[i]] = new_histo.Clone()
    histos[samples[i]].SetTitle("")
    histos[samples[i]].SetLineWidth(2)
    histos[samples[i]].SetLineStyle(1)
    histos[samples[i]].SetFillStyle(4000)
    legend.AddEntry(histos[samples[i]], labelLegend[samples[i]], "f")
    histos[samples[i]].SetLineColor(colors[i])
    if i == 0:
        histos[samples[i]].Draw("hist")
    else:
        histos[samples[i]].Draw("hist same")
    if histos[samples[i]].GetMaximum() > max:
        max = histos[samples[i]].GetMaximum()

# for i in range(len(uncert_list)):
#     sum_histo.Multiply(sum_histo)
#     uncert_list[i].Divide(sum_histo)
#     rel_uncert.Add(uncert_list[i])

histos[samples[0]].GetYaxis().SetTitle("Entries")
histos[samples[0]].GetYaxis().SetTitleSize(0.05)
histos[samples[0]].GetYaxis().SetTitleOffset(1.4)
histos[samples[0]].GetYaxis().SetLabelSize(0.04)

histos[samples[0]].GetXaxis().SetTitleSize(0.05)
histos[samples[0]].GetXaxis().SetLabelSize(0.04)
histos[samples[0]].GetXaxis().SetTitle("DNN Score Bin")


t0 = makeText(
    0.2,
    0.89,
    "Signal Region",
    42,
    size=0.03,
)
t1 = makeText(0.18, 0.95, "CMS", 61)
t2 = makeText(
    0.2,
    0.85,
    "Electrons Drell-Yan p_{  T}^{  Z} Binned",
    42,
    size=0.03,
)
t3 = makeText(0.7, 0.95, "(13 TeV)", 42)
t4 = makeText(0.38, 0.95, "2018", 42)

t0.Draw()
t1.Draw()
t2.Draw()
t3.Draw()
t4.Draw()

legend.Draw()

# Linear
histos[samples[0]].GetYaxis().SetRangeUser(0, max * 1.2)
c1.SaveAs("figures/dy_zpt_flash_binned.pdf")

# Log
c1.SetLogy()
histos[samples[0]].SetMaximum(1e6)
histos[samples[0]].SetMinimum(1e-1)
c1.SaveAs("figures/dy_zpt_flash_binned_log.pdf")

c2 = ROOT.TCanvas("c2", "", 800, 800)

uncert.Draw("hist")
uncert.GetYaxis().SetTitle("(MC Stat. Unc.)^{ 2}")
uncert.GetYaxis().SetTitleSize(0.05)
uncert.GetYaxis().SetTitleOffset(1.4)
uncert.GetYaxis().SetLabelSize(0.04)
uncert.GetXaxis().SetTitleSize(0.05)
uncert.GetXaxis().SetLabelSize(0.04)
uncert.GetXaxis().SetTitle("DNN Score Bin")

t0.Draw()
t1.Draw()
t2.Draw()
t3.Draw()
t4.Draw()

legend_2.Draw()

# Linear
uncert.SetMaximum(3500)
c2.SaveAs("figures/dy_zpt_flash_binned_uncert.pdf")

# Log
c2.SetLogy()
uncert.SetMaximum(1e4)
uncert.SetMinimum(3.3e-1)
c2.SaveAs("figures/dy_zpt_flash_binned_uncert_log.pdf")

for i in range(len(uncert_list)):
    sum2 = sum_histo.Clone()
    sum2.Multiply(sum_histo, sum_histo)
    uncert_list[i].Divide(sum_histo)
    rel_uncert.Add(uncert_list[i])

c3 = ROOT.TCanvas("c3", "", 800, 800)

sum2.Draw("hist")
rel_uncert.Draw("hist")
rel_uncert.GetYaxis().SetTitle("#sum(#sigma_{i}^{2}) / #left(#sum N_{i} #right)^{2}")
rel_uncert.GetYaxis().SetTitleSize(0.03)
rel_uncert.GetYaxis().SetTitleOffset(1.7)
rel_uncert.GetYaxis().SetLabelSize(0.04)
rel_uncert.GetXaxis().SetTitleSize(0.05)
rel_uncert.GetXaxis().SetLabelSize(0.04)
rel_uncert.GetXaxis().SetTitle("DNN Score Bin")

t0.Draw()
t1.Draw()
t2.Draw()
t3.Draw()
t4.Draw()

legend_2.Draw()

# Linear
rel_uncert.SetMaximum(1.15)
c3.SaveAs("figures/dy_zpt_flash_binned_rel_uncert.pdf")

# Log
c3.SetLogy()
rel_uncert.SetMaximum(2e1)
rel_uncert.SetMinimum(1e-3)
c3.SaveAs("figures/dy_zpt_flash_binned_rel_uncert_log.pdf")
