
# new_bin_num [0, 1, 207, 249, 286, 320, 348, 379, 441, 535] 10
# new_bin_edges [0.0, 0.0075, 1.5525, 1.8675, 2.145, 2.4, 2.6174999999999997, 2.85, 3.3225, 4.3275, 10] 11
# new_histo_s [0.007215708254781813, 50.019729538779764, 16.57155753818742, 11.967472432695121, 8.982256093157455, 6.144879546477957, 4.949213263746416, 5.847191019914706, 3.977848449593
# 3033, 0.7257194612268202] 10
# new_histo_b [387.66449914771994, 12117.897760268326, 457.00630807090727, 214.33770205797617, 110.67978661051367, 53.570534976578905, 31.45989695826863, 28.97375439069168, 13.2015794595
# 91919, 0.14554047541830972] 10
# significance_list [0.0001640682985797849, 0.04109140975340342, 0.32522914373102024, 0.4523438181833145, 0.5695703658283888, 0.6420846377716076, 0.7140740344137804, 0.8841989183775651,
# 0.9111388834293984, 0.8230209464416844, 0.0]
# sig_sum 1.9616338948462193




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

def figure_of_merit(hs, hb, print_stuff=False):
    significance_list = []
    for i in range(1, len(hs)):
        significance = hs[i] / (ROOT.TMath.Sqrt(hb[i] + 0.01 * hb[i]**2) + 0.5)
        significance_list.append(significance)
    if print_stuff:
        print("significance_list", significance_list)

    # sum in quadrature of the significances
    return ROOT.TMath.Sqrt(sum([x**2 for x in significance_list]))


def significance_sum(significance_list):
    # sum in quadrature of the bins

    # significance_list = []
    # for i in range(1, hs.GetNbinsX() + 1):
    #     s = hs.GetBinContent(i)
    #     significance_list.append(s)

    significance = math.sqrt(sum([x**2 for x in significance_list]))
    return significance


# hSignal.Rebin(5)
# hBackground.Rebin(5)

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
        # print(new_bin_edges)

        hBackground = hBackground.Rebin(
            len(new_bin_edges) - 1, "hBackground", array.array("d", new_bin_edges)
        )
        hSignal = hSignal.Rebin(
            len(new_bin_edges) - 1, "hSignal", array.array("d", new_bin_edges)
        )
        bkg_list = [
            hBackground.GetBinContent(j) for j in range(1, hBackground.GetNbinsX() + 1)
        ]
        sig_list = [hSignal.GetBinContent(j) for j in range(1, hSignal.GetNbinsX() + 1)]
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


desired_events_per_bin = 1
desired_bins = 10


# def rebin_histogram(
#     hs, figure_of_merit, desired_events_per_bin, desired_bins, max_num_bins=20
# ):
#     # Compute the current figure of merit
#     current_figure_of_merit = figure_of_merit(
#         [hs.GetBinContent(i) for i in range(1, hs.GetNbinsX() + 1)]
#     )
#     print("current_figure_of_merit", current_figure_of_merit)
#     j = 0
#     bin_edges = [hs.GetBinLowEdge(i) for i in range(hs.GetNbinsX(), 0, -1)]
#     # Loop over the bins in the histogram
#     n = 100
#     while hs.GetNbinsX() > desired_bins:
#         max_figure_of_merit = -1
#         max_bin = -1
#         # get the list of bin edges
#         # Find the pair of adjacent bins that maximizes the figure of merit
#         for i in range(hs.GetNbinsX(), 0, -n):
#             # Combine the the 10 adjacent bins
#             combined_figure_of_merit = sum(
#                 [hs.GetBinContent(i) for i in range(i, i - n - 1, -1)]
#             )
#             print("combined_figure_of_merit", combined_figure_of_merit)

#             # Compute the figure of merit for the combined bin
#             # combined_figure_of_merit = figure_of_merit([combined_bin])

#             # Check if the combined figure of merit is greater than the current maximum
#             if combined_figure_of_merit >= max_figure_of_merit:
#                 max_figure_of_merit = combined_figure_of_merit
#                 max_bin = i
#                 # if max_bin<1220:
#                 #     print("max_figure_of_merit", max_figure_of_merit)
#                 #     print("max_bin", max_bin)

#         # Combine the pair of adjacent bins that maximizes the figure of merit
#         hs.SetBinContent(
#             max_bin,
#             max_figure_of_merit,
#         )
#         for i in range(max_bin - 1, max_bin - n - 1, -1):
#             hs.SetBinContent(i, 0)

#         j += 1
#         # print("max_content", hs.GetBinContent(max_bin))
#         # print("max_bin", max_bin)
#         # Check if the number of events in the new bin is less than the desired number of events per bin
#         if hs.GetBinContent(max_bin) < desired_events_per_bin:
#             print("j", j)
#             continue

#         # Check if the number of bins in the histogram is less than or equal to the desired number of bins
#         if hs.GetNbinsX() <= desired_bins:
#             print("num_bins", hs.GetNbinsX())
#             break

#         # Compute the new figure of merit
#         new_figure_of_merit = figure_of_merit(
#             [hs.GetBinContent(i) for i in range(1, hs.GetNbinsX() + 1)]
#         )
#         # Check if the new figure of merit is greater than the current figure of merit
#         if new_figure_of_merit > current_figure_of_merit:
#             current_figure_of_merit = new_figure_of_merit
#             for i in range(max_bin - 1, max_bin - n - 1, -1):
#                 bin_edges.pop(i)
#             # bin_edges.pop(max_bin - 1)
#             hs = hs.Rebin(
#                 len(bin_edges) - 1,
#                 f"{hs.GetName().split('_rebin_')[0]}_rebin_{j}",
#                 array.array("d", list(reversed(bin_edges))),
#             )
#             if j % 50 == 0:
#                 print("max_bin", max_bin)
#                 print("new_figure_of_merit", new_figure_of_merit)
#                 print("bin_edges", len(bin_edges))
#                 print("new number of bins", hs.GetNbinsX())
#             # break
#         elif new_figure_of_merit == current_figure_of_merit:
#             if hs.GetNbinsX() > max_num_bins:
#                 print("num bins", hs.GetNbinsX())
#                 n += 5
#             else:
#                 break
#         # else:
#         #     n+=-5
#         #     print("n", n)
#         #     print("max_bin", max_bin)
#         #     if n==0:
#         #         break
#         # Undo the last bin combination
#         # hs.SetBinContent(max_bin - 1, hs.GetBinContent(max_bin))
#         # hs.SetBinContent(max_bin, 0)

#     return hs


def optimal_rebinning(histo_s, histo_b, target_bins):
    n_bins = len(histo_s)

    # Base case: If the number of target bins is equal to the number of bins in the histo_s,
    # return the histo_s as it is.
    if target_bins == n_bins:
        return histo_s, histo_b

    # Initialize an array to store the maximum figure of merit for each combination of bins.
    max_merits = [[float("-inf")] * (n_bins + 1) for _ in range(target_bins + 1)]

    # print("max_merits 0", max_merits)
    # Initialize an array to store the split indices corresponding to each combination of bins.
    split_indices = [[0] * (n_bins + 1) for _ in range(target_bins + 1)]

    # print("split_indices", split_indices)
    # Calculate the figure of merit for single bins (base case of the dynamic programming).
    for i in range(1, n_bins + 1):
        max_merits[1][i] = figure_of_merit([histo_s[i - 1]], [histo_b[i - 1]])
    # print("max_merits 1", max_merits[1])
    # Calculate the maximum figure of merit for all combinations of target_bins and number of bins.
    for bins in range(2, target_bins + 1):
        for i in range(1, n_bins + 1):
            for j in range(i):
                current_merit = max_merits[bins - 1][j] + figure_of_merit(
                    histo_s[j:i], histo_b[j:i]
                )
                if current_merit > max_merits[bins][i]:
                    # print("current_merit ",bins, i, j,  current_merit)
                    max_merits[bins][i] = current_merit
                    split_indices[bins][i] = j
    # print("max_merits", max_merits)
    # Backtrack to find the optimal rebinning.
    result_bins_s = []
    result_bins_b = []

    i = n_bins
    for bins in range(target_bins, 0, -1):
        j = split_indices[bins][i]
        result_bins_s.insert(0, histo_s[j:i])
        result_bins_b.insert(0, histo_b[j:i])
        i = j

    return result_bins_s, result_bins_b


# histo = rebin_histogram(
#     hSignificance,
#     significance_sum,
#     desired_events_per_bin,
#     desired_bins
#     # hSignificance, desired_events_per_bin, desired_bins
# )

# merge adjacent bins so that the number of bins is 1/100 of the number it is now
# hSignificance.Rebin(100)
histo_s = [hSignal.GetBinContent(i) for i in range(1, hSignal.GetNbinsX() + 1)]
histo_b = [
    hBackground.GetBinContent(i) for i in range(1, hBackground.GetNbinsX() + 1)
]
bin_edges = [hSignal.GetBinLowEdge(i) for i in range(1, hSignal.GetNbinsX() + 1)]
print("histo_s", histo_s, len(histo_s))
print("histo_b", histo_b, len(histo_b))
print("bin_edges", bin_edges, len(bin_edges))

new_histo_s, new_histo_b = optimal_rebinning(
    histo_s,
    histo_b,
    desired_bins
    # hSignificance, desired_events_per_bin, desired_bins
)
print("new_histo_s", new_histo_s, len(new_histo_s))
print("new_histo_b", new_histo_b, len(new_histo_b))


# compute the new bin-edges
new_bin_num = [0]
for i, new_bin in enumerate(new_histo_s[:-1]):
    j = len(new_bin)
    if i == 0:
        to_add = j  # + 1
    else:
        to_add = j + new_bin_num[-1]
    new_bin_num.append(to_add)

# new_bin_num =[0, 529, 1021, 1208, 1374, 1533, 1668, 1774, 2056, 2405]
print("new_bin_num", new_bin_num, len(new_bin_num))
# new_bin_num [0, 529, 1021, 1208, 1374, 1533, 1668, 1774, 2056, 2406]

new_bin_edges = [bin_edges[i] for i in new_bin_num] + [10]
print("new_bin_edges", new_bin_edges, len(new_bin_edges))

new_histo_s = [sum(new_bin) for new_bin in new_histo_s]
new_histo_b = [sum(new_bin) for new_bin in new_histo_b]
print("new_histo_s", new_histo_s, len(new_histo_s))
print("new_histo_b", new_histo_b, len(new_histo_b))

histo_rebin_s = ROOT.TH1F(
    "histo_rebin_s", "histo_rebin_s", len(new_bin_edges) - 1, array.array("d", new_bin_edges)
)
for i, new_bin in enumerate(new_histo_s):
    histo_rebin_s.SetBinContent(i + 1, new_bin)

histo_rebin_b = ROOT.TH1F(
    "histo_rebin_b", "histo_rebin_b", len(new_bin_edges) - 1, array.array("d", new_bin_edges)
)
for i, new_bin in enumerate(new_histo_b):
    histo_rebin_b.SetBinContent(i + 1, new_bin)

sig_sum = figure_of_merit(histo_rebin_s,   histo_rebin_b, True)
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



hSignificance = histo_rebin_s.Clone()
for i in range(1, hSignificance.GetNbinsX() + 1):
    # if hBackground.GetBinContent(i) <= 0:
    #     # print("bin", i, "has {} background events".format(hBackground.GetBinContent(i)))
    #     hBackground.SetBinContent(i, 0)

    print(
        "bin",
        i,
        "has {} background events and {} signal events".format(
            histo_rebin_b.GetBinContent(i), histo_rebin_s.GetBinContent(i)
        ),
    )

    hSignificance.SetBinContent(
        i,
        hSignificance.GetBinContent(i)
        / (
            math.sqrt(
                histo_rebin_b.GetBinContent(i) + (0.1 * histo_rebin_b.GetBinContent(i)) ** 2
            )
            + 0.5
        ),
    )
    print("bin", i, "has {} significance".format(hSignificance.GetBinContent(i)))

significance_content=[hSignificance.GetBinContent(i) for i in range(1, hSignificance.GetNbinsX() + 1)]
print("hSignificance", significance_content, len(significance_content))
print("significance sum", significance_sum(significance_content))

canvas = ROOT.TCanvas("canvas", "canvas", 800, 800)
hSignificance.Draw()
# canvas.Draw()
# wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
# ROOT.gApplication.Run()
canvas.SaveAs("rebinning_sig.png")

c_sig = ROOT.TCanvas("c_sig", "c_sig", 800, 800)
c_sig.cd()
# log scale
c_sig.SetLogy()
histo_rebin_s.Draw()
c_sig.SaveAs("rebinning_sig_s.png")

c_bkg = ROOT.TCanvas("c_bkg", "c_bkg", 800, 800)
c_bkg.cd()
# log scale
c_bkg.SetLogy()
histo_rebin_b.Draw()
c_bkg.SaveAs("rebinning_sig_b.png")


fSignal.Close()
fBackground.Close()
