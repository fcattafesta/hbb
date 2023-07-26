import ROOT
import os
import argparse
import array

from samples import *

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--variable", default="atanhDNN_Score", help="Variable to plot"
)
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")
parser.add_argument("-s", "--suffix", default="", help="Suffix for output file")
args = parser.parse_args()


histodir = f"/gpfs/ddn/cms/user/malucchi/hbb_out/{args.lep}/{args.suffix}/"

variable = args.variable
if args.lep == "mu":
    SR = "SR_mm"
elif args.lep == "el":
    SR = "SR_ee"


files_to_open = [
    x
    for x in os.listdir(histodir)
    if x.split("Histos")[0].endswith(flavourSplitting.keys())
]
print(files_to_open)

s = 0
b = 0
for file in files_to_open:
    name = file.split("Histos")[0]
    for ss in flavourSplitting.keys():
        if name.endswith(ss):
            name.replace(ss, "")
    if name in ["ZH", "ggZH"]:
        fSignal = ROOT.TFile.Open(f"{histodir}/{file}")
        h = fSignal.Get(variable + f"___{SR}").Clone()
        h.Scale(samples[name]["xsec"] * samples[data]["lumi"])

        if s == 0:
            hSignal = h
        else:
            hSignal.Add(h)
        s += 1
    else:
        fBackgroud = ROOT.TFile.Open(f"{histodir}/{file}")
        h = fBackgroud.Get(variable + f"___{SR}").Clone()
        h.Scale(samples[name]["xsec"] * samples[data]["lumi"])

        if b == 0:
            hBackground = h
        else:
            hBackground.Add(h)
        b += 1


def figure_of_merit(hs, hb):
    significance_list = []
    for i in range(1, hs.GetNbinsX() + 1):
        s = hs.GetBinContent(i)
        b = hb.GetBinContent(i)
        significance = s / ROOT.TMath.Sqrt(b + 0.01 * b**2 + 0.5)
        significance_list.append(significance)

    # sum in quadrature of the significances
    return ROOT.TMath.Sqrt(sum([x**2 for x in significance_list]))

desired_events_per_bin=1
desired_bins=10


def rebin_histogram(hs, hb, figure_of_merit, desired_events_per_bin, desired_bins):
    # Compute the current figure of merit
    current_figure_of_merit = figure_of_merit(hs, hb)
    print("current_figure_of_merit", current_figure_of_merit)

    # Loop over the bins in the histogram
    while hs.GetNbinsX() > desired_bins:
        max_figure_of_merit = -1
        max_bin = -1

        # Find the pair of adjacent bins that maximizes the figure of merit
        for i in range(1, hs.GetNbinsX()):
            # Combine the pair of adjacent bins
            combined_bin = hs.GetBinContent(i) + hs.GetBinContent(i + 1)

            # Compute the figure of merit for the combined bin
            combined_figure_of_merit = figure_of_merit(combined_bin)

            # Check if the combined figure of merit is greater than the current maximum
            if combined_figure_of_merit > max_figure_of_merit:
                max_figure_of_merit = combined_figure_of_merit
                max_bin = i

        # Combine the pair of adjacent bins that maximizes the figure of merit
        hs.SetBinContent(
            max_bin,
            hs.GetBinContent(max_bin) + hs.GetBinContent(max_bin + 1),
        )
        hs.SetBinError(
            max_bin,
            ROOT.TMath.Sqrt(
                hs.GetBinError(max_bin) ** 2
                + hs.GetBinError(max_bin + 1) ** 2
            ),
        )
        hs.SetBinContent(max_bin + 1, 0)
        hs.SetBinError(max_bin + 1, 0)

        # Check if the number of events in the new bin is less than the desired number of events per bin
        if hs.GetBinContent(max_bin) < desired_events_per_bin:
            continue

        # Check if the number of bins in the histogram is less than or equal to the desired number of bins
        if hs.GetNbinsX() <= desired_bins:
            break

        # Compute the new figure of merit
        new_figure_of_merit = figure_of_merit(hs)

        # Check if the new figure of merit is greater than the current figure of merit
        if new_figure_of_merit > current_figure_of_merit:
            current_figure_of_merit = new_figure_of_merit
        else:
            # Undo the last bin combination
            hs.SetBinContent(max_bin + 1, hs.GetBinContent(max_bin))
            hs.SetBinError(
                max_bin + 1,
                ROOT.TMath.Sqrt(
                    hs.GetBinError(max_bin) ** 2
                    + hs.GetBinError(max_bin + 1) ** 2
                ),
            )
            hs.SetBinContent(max_bin, 0)
            hs.SetBinError(max_bin, 0)

    return hs


histo=rebin_histogram(hSignal, hBackground, figure_of_merit, desired_events_per_bin, desired_bins)