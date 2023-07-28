# [0.0, 0.8099999999999999, 1.6199999999999999, 1.905, 2.13, 2.34, 2.5349999999999997, 2.715, 2.94, 3.3, 10]
# new_histo_content [0.8485512535380314, 4.383495129583348, 2.747284548676875, 2.405946694539244, 2.3386751692457755, 2.3030540730695988, 2.1161810676834087, 2.4635075345617445, 3.0687765287028705, 5.856188600518083]
# sig_sum 9.91484272553397

import ROOT
import os
import argparse
import array
import math

from samples import *

ROOT.gErrorIgnoreLevel = ROOT.kError

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
    data = "SingleMuon_2018"
elif args.lep == "el":
    SR = "SR_ee"
    data = "EGamma_2018"

# print("file in directory:", os.listdir(histodir))
files_to_open = [
    x
    for x in os.listdir(histodir)
    if not x.split("_Histos")[0].endswith(tuple(flavourSplitting.keys()))
    and x.endswith("Histos.root")
    and data not in x
]
# print(files_to_open)

signalSample = "ZH"
fSignal = ROOT.TFile.Open(f"{histodir}/{signalSample}_Histos.root")
hs = fSignal.Get(variable + f"___{SR}").Clone()
hs.Scale(samples[signalSample]["xsec"] * samples[data]["lumi"])
hSignal = hs.Clone()

bkgSample = "DYZpt-400To650"
fBackground = ROOT.TFile.Open(f"{histodir}/{bkgSample}_Histos.root")
hb = fBackground.Get(variable + f"___{SR}").Clone()
hb.Scale(samples[bkgSample]["xsec"] * samples[data]["lumi"])
hBackground = hb.Clone()

files_to_open.remove(f"{signalSample}_Histos.root")
files_to_open.remove(f"{bkgSample}_Histos.root")

for file in files_to_open:
    name = file.split("_Histos")[0]
    print(name)
    for ss in flavourSplitting.keys():
        if name.endswith(ss):
            name.replace(ss, "")
    if name in ["ggZH"]:
        fSignal1 = ROOT.TFile.Open(f"{histodir}/{file}")
        h = fSignal1.Get(variable + f"___{SR}").Clone()
        h.Scale(samples[name]["xsec"] * samples[data]["lumi"])
        hSignal.Add(h)
        fSignal1.Close()

    else:
        fBackground1 = ROOT.TFile.Open(f"{histodir}/{file}")
        h = fBackground1.Get(variable + f"___{SR}").Clone()
        h.Scale(samples[name]["xsec"] * samples[data]["lumi"])

        hBackground.Add(h)
        fBackground1.Close()

# def figure_of_merit(hs, hb):
#     significance_list = []
#     for i in range(1, hs.GetNbinsX() + 1):
#         s = hs.GetBinContent(i)
#         b = hb.GetBinContent(i)
#         significance = s / ROOT.TMath.Sqrt(b + 0.01 * b**2 + 0.5)
#         significance_list.append(significance)

#     # sum in quadrature of the significances
#     return ROOT.TMath.Sqrt(sum([x**2 for x in significance_list]))


def significance_sum(significance_list):
    # sum in quadrature of the bins

    # significance_list = []
    # for i in range(1, hs.GetNbinsX() + 1):
    #     s = hs.GetBinContent(i)
    #     significance_list.append(s)

    significance = math.sqrt(sum([x**2 for x in significance_list]))
    return significance


# hSignal.Rebin(50)
# hBackground.Rebin(50)

# if bBackground.GetBinContent(i) < 0.1 merge with the previous bin
i = 1
while i in range(1, hBackground.GetNbinsX() + 1):
    if hBackground.GetBinContent(i) < 0.0001 or hSignal.GetBinContent(i) < 0.0001:
        # print("merging bin", i)
        new_bin_edges = [
            hBackground.GetBinLowEdge(j)
            for j in range(1, hBackground.GetNbinsX() + 1)
            if hBackground.GetBinLowEdge(j) != hBackground.GetBinLowEdge(i)
        ]
        #print(new_bin_edges)

        hBackground = hBackground.Rebin(
            len(new_bin_edges) - 1, "hBackground", array.array("d", new_bin_edges)
        )
        hSignal = hSignal.Rebin(
            len(new_bin_edges) - 1, "hSignal", array.array("d", new_bin_edges)
        )
        bkg_list=[hBackground.GetBinContent(j) for j in range(1, hBackground.GetNbinsX() + 1)]
        sig_list=[hSignal.GetBinContent(j) for j in range(1, hSignal.GetNbinsX() + 1)]
        # print   (bkg_list, sum(bkg_list))
        # print   (hBackground.GetNbinsX())
        # print   (sig_list, sum(sig_list))
        # print   (hSignal.GetNbinsX())
        # hBackground.SetBinContent(i - 1, hBackground.GetBinContent(i) + hBackground.GetBinContent(i - 1))
        # hBackground.SetBinContent(i, 0)

        # hSignal.SetBinContent(i - 1, hSignal.GetBinContent(i) + hSignal.GetBinContent(i - 1))
        # hSignal.SetBinContent(i, 0)
        i -= 1
    else:
        i += 1


hSignificance = hSignal.Clone()
for i in range(1, hSignificance.GetNbinsX() + 1):
    # if hBackground.GetBinContent(i) <= 0:
    #     # print("bin", i, "has {} background events".format(hBackground.GetBinContent(i)))
    #     hBackground.SetBinContent(i, 0)

    print(
        "bin",
        i,
        "has {} background events and {} signal events".format(
            hBackground.GetBinContent(i), hSignal.GetBinContent(i)
        ),
    )

    hSignificance.SetBinContent(
        i,
        hSignificance.GetBinContent(i)
        / (
            math.sqrt(
                hBackground.GetBinContent(i) + (0.1 * hBackground.GetBinContent(i)) ** 2
            )
            + 0.5
        ),
    )

desired_events_per_bin = 1
desired_bins = 10


def rebin_histogram(
    hs, figure_of_merit, desired_events_per_bin, desired_bins, max_num_bins=20
):
    # Compute the current figure of merit
    current_figure_of_merit = figure_of_merit(
        [hs.GetBinContent(i) for i in range(1, hs.GetNbinsX() + 1)]
    )
    print("current_figure_of_merit", current_figure_of_merit)
    j = 0
    bin_edges = [hs.GetBinLowEdge(i) for i in range(hs.GetNbinsX(), 0, -1)]
    # Loop over the bins in the histogram
    n = 100
    while hs.GetNbinsX() > desired_bins:
        max_figure_of_merit = -1
        max_bin = -1
        # get the list of bin edges
        # Find the pair of adjacent bins that maximizes the figure of merit
        for i in range(hs.GetNbinsX(), 0, -n):
            # Combine the the 10 adjacent bins
            combined_figure_of_merit = sum(
                [hs.GetBinContent(i) for i in range(i, i - n - 1, -1)]
            )
            print("combined_figure_of_merit", combined_figure_of_merit)

            # Compute the figure of merit for the combined bin
            # combined_figure_of_merit = figure_of_merit([combined_bin])

            # Check if the combined figure of merit is greater than the current maximum
            if combined_figure_of_merit >= max_figure_of_merit:
                max_figure_of_merit = combined_figure_of_merit
                max_bin = i
                # if max_bin<1220:
                #     print("max_figure_of_merit", max_figure_of_merit)
                #     print("max_bin", max_bin)

        # Combine the pair of adjacent bins that maximizes the figure of merit
        hs.SetBinContent(
            max_bin,
            max_figure_of_merit,
        )
        for i in range(max_bin - 1, max_bin - n - 1, -1):
            hs.SetBinContent(i, 0)

        j += 1
        # print("max_content", hs.GetBinContent(max_bin))
        # print("max_bin", max_bin)
        # Check if the number of events in the new bin is less than the desired number of events per bin
        if hs.GetBinContent(max_bin) < desired_events_per_bin:
            print("j", j)
            continue

        # Check if the number of bins in the histogram is less than or equal to the desired number of bins
        if hs.GetNbinsX() <= desired_bins:
            print("num_bins", hs.GetNbinsX())
            break

        # Compute the new figure of merit
        new_figure_of_merit = figure_of_merit(
            [hs.GetBinContent(i) for i in range(1, hs.GetNbinsX() + 1)]
        )
        # Check if the new figure of merit is greater than the current figure of merit
        if new_figure_of_merit > current_figure_of_merit:
            current_figure_of_merit = new_figure_of_merit
            for i in range(max_bin - 1, max_bin - n - 1, -1):
                bin_edges.pop(i)
            # bin_edges.pop(max_bin - 1)
            hs = hs.Rebin(
                len(bin_edges) - 1,
                f"{hs.GetName().split('_rebin_')[0]}_rebin_{j}",
                array.array("d", list(reversed(bin_edges))),
            )
            if j % 50 == 0:
                print("max_bin", max_bin)
                print("new_figure_of_merit", new_figure_of_merit)
                print("bin_edges", len(bin_edges))
                print("new number of bins", hs.GetNbinsX())
            # break
        elif new_figure_of_merit == current_figure_of_merit:
            if hs.GetNbinsX() > max_num_bins:
                print("num bins", hs.GetNbinsX())
                n += 5
            else:
                break
        # else:
        #     n+=-5
        #     print("n", n)
        #     print("max_bin", max_bin)
        #     if n==0:
        #         break
        # Undo the last bin combination
        # hs.SetBinContent(max_bin - 1, hs.GetBinContent(max_bin))
        # hs.SetBinContent(max_bin, 0)

    return hs


def optimal_rebinning(histogram, target_bins):
    n_bins = len(histogram)

    # Base case: If the number of target bins is equal to the number of bins in the histogram,
    # return the histogram as it is.
    if target_bins == n_bins:
        return histogram

    # Initialize an array to store the maximum figure of merit for each combination of bins.
    max_merits = [[float("-inf")] * (n_bins + 1) for _ in range(target_bins + 1)]

    # print("max_merits 0", max_merits)
    # Initialize an array to store the split indices corresponding to each combination of bins.
    split_indices = [[0] * (n_bins + 1) for _ in range(target_bins + 1)]

    # print("split_indices", split_indices)
    # Calculate the figure of merit for single bins (base case of the dynamic programming).
    for i in range(1, n_bins + 1):
        max_merits[1][i] = significance_sum([histogram[i - 1]])
    # print("max_merits 1", max_merits[1])
    # Calculate the maximum figure of merit for all combinations of target_bins and number of bins.
    for bins in range(2, target_bins + 1):
        for i in range(1, n_bins + 1):
            for j in range(i):
                current_merit = max_merits[bins - 1][j] + significance_sum(
                    histogram[j:i]
                )
                if current_merit > max_merits[bins][i]:
                    # print("current_merit ",bins, i, j,  current_merit)
                    max_merits[bins][i] = current_merit
                    split_indices[bins][i] = j
    # print("max_merits", max_merits)
    # Backtrack to find the optimal rebinning.
    result_bins = []
    i = n_bins
    for bins in range(target_bins, 0, -1):
        j = split_indices[bins][i]
        result_bins.insert(0, histogram[j:i])
        i = j

    return result_bins


# histo = rebin_histogram(
#     hSignificance,
#     significance_sum,
#     desired_events_per_bin,
#     desired_bins
#     # hSignificance, desired_events_per_bin, desired_bins
# )

# merge adjacent bins so that the number of bins is 1/100 of the number it is now
# hSignificance.Rebin(100)
histo = [
    hSignificance.GetBinContent(i) for i in range(1, hSignificance.GetNbinsX() + 1)
]
bin_edges = [
    hSignificance.GetBinLowEdge(i) for i in range(1, hSignificance.GetNbinsX() + 1)
]
print("histo", histo, len(histo))
print("bin_edges", bin_edges, len(bin_edges))

histo = optimal_rebinning(
    histo,
    desired_bins
    # hSignificance, desired_events_per_bin, desired_bins
)
print("histo", histo)
print("len histo", len(histo))

# compute the new bin-edges
new_bin_num = [0]
for i, new_bin in enumerate(histo[:-1]):
    j = len(new_bin)
    if i == 0:
        to_add = j #+ 1
    else:
        to_add = j + new_bin_num[-1]
    new_bin_num.append(to_add)

#new_bin_num =[0, 529, 1021, 1208, 1374, 1533, 1668, 1774, 2056, 2405]
print("new_bin_num", new_bin_num, len(new_bin_num))
#new_bin_num [0, 529, 1021, 1208, 1374, 1533, 1668, 1774, 2056, 2406]

new_bin_edges = [bin_edges[i] for i in new_bin_num] + [10]
print("new_bin_edges", new_bin_edges, len(new_bin_edges))

new_histo_content = [sum(new_bin) for new_bin in histo]
print("new_histo_content", new_histo_content, len(new_histo_content))


new_histo = ROOT.TH1F(
    "new_histo", "new_histo", len(new_bin_edges) - 1, array.array("d", new_bin_edges)
)
for i, new_bin in enumerate(histo):
    new_histo.SetBinContent(i + 1, sum(new_bin))

sig_sum = significance_sum(new_histo_content)
print("sig_sum", sig_sum)


# if a bin has 0 content merge it with the previous bin and create a unique bin
# for i in range(1, histo.GetNbinsX() + 1):
#     if histo.GetBinContent(i) == 0:
#         histo.SetBinContent(i - 1, histo.GetBinContent(i - 1) + histo.GetBinContent(i))
#         histo.SetBinContent(i, 0)

# new_histo = ROOT.TH1F()
# for i in range(1, histo.GetNbinsX() + 1):
#     print("bin", i, "has {} events".format(histo.GetBinContent(i)))
#     new_histo.SetBinContent(i, histo.GetBinContent(i))


# for i in range(1, histo.GetNbinsX() + 1):
#     if histo.GetBinContent(i) != 0:
#         print(
#             "bin",
#             i,
#             "with edge {} has {} events".format(
#                 histo.GetBinLowEdge(i), histo.GetBinContent(i)
#             ),
#         )


# print("number of bins", histo.GetNbinsX())

canvas = ROOT.TCanvas("canvas", "canvas", 800, 800)
new_histo.Draw()
# canvas.Draw()
# wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
# ROOT.gApplication.Run()
canvas.SaveAs("rebinning_sig.png")

print("saving histogram")

fSignal.Close()
fBackground.Close()
