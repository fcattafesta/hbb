import ROOT
import sys
import argparse
import array

from samples import samples

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--variable", default="atanhDNN_Score", help="Variable to plot")
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")
parser.add_argument("-s", "--suffix", default="", help="Suffix for output file")
args = parser.parse_args()


def FindBinDown(
    hSignal, binLimitUp, minNumberOfEventPerBin, MinNumberOfBin_inBinning
):
    binLimitDown = 0.0
    for n in range(binLimitUp - MinNumberOfBin_inBinning - 1, 0, -1):

        integral_S = hSignal.Integral(n + 1, binLimitUp)

        if integral_S >= minNumberOfEventPerBin:
            binLimitDown = n
            break

    return binLimitDown


histodir = f"/gpfs/ddn/cms/user/malucchi/hbb_out/{args.lep}/{args.suffix}/"
variable = args.variable
if args.lep == "mu":
    SR = "SR_mm"
    data = "SingleMuon_2018"
elif args.lep == "el":
    SR = "SR_ee"
    data = "EGamma_2018"

signalSample = "ZH"
fSignal = ROOT.TFile.Open(f"{histodir}/{signalSample}_Histos.root")
hSignal=fSignal.Get(variable + f"___{SR}").Clone()
print(hSignal)
hSignal.Scale(samples[signalSample]["xsec"] * samples[data]["lumi"])
print(hSignal)

signalSample = "ggZH"
fSignal1 = ROOT.TFile.Open(f"{histodir}/{signalSample}_Histos.root")
hSignal.Add(fSignal1.Get(variable + f"___{SR}").Clone(), samples[signalSample]["xsec"] * samples[data]["lumi"])


xMax = 10. if variable == "atanhDNN_Score" else 1.
binMinWidth = 0.15 if variable == "atanhDNN_Score" else 0.03
Nbins_binning = hSignal.GetNbinsX()
MinNumberOfBin_inBinning = int(binMinWidth / xMax * Nbins_binning)
binLimitDown = Nbins_binning

minNumberOfEventPerBin = 1
tot = hSignal.Integral(0, Nbins_binning + 1)
N = tot * 2
print("Total number of events:  ", tot)
delta = 2.0 * (tot - minNumberOfEventPerBin * N) / N**2
print("min size", minNumberOfEventPerBin, "step", delta, "N", N, "tot", tot)


# delta=0
# minNumberOfEventPerBin=0.6

binning_DNN = [xMax]


while binLimitDown > 0:
    binning_DNN.append((1.0 * binLimitDown * xMax) / Nbins_binning)
    binLimitUp = binLimitDown
    binLimitDown = FindBinDown(
        hSignal,
        binLimitUp,
        minNumberOfEventPerBin,
        MinNumberOfBin_inBinning,
    )
    minNumberOfEventPerBin += delta

print("'" + variable + "' :")
#invert the list
binning_DNN += [0]
binning_DNN.reverse()

print("[")
for i in range(len(binning_DNN)):
    print(binning_DNN[i], end=", ")

print("\n],")
print(len(binning_DNN))

# binning_DNN=[0, 0.125, 0.276, 0.427, 0.578, 0.729, 0.88, 1.031, 1.182, 1.333, 1.484, 1.635, 1.786, 1.937, 2.088, 2.239, 2.39, 2.545, 2.779, 3.0, 3.3, 3.6, 4.0, 10.0, ]
binning_DNN=[0, 0.88, 1.4, 1.937, 2.545,   3.0, 3.3, 3.6, 4.0, 10.0]
print("len", len(binning_DNN))
h_rebin=hSignal.Rebin(len(binning_DNN) - 1, "hSignal_rebinned", array.array("d", binning_DNN))
c=ROOT.TCanvas("c","c",800,800)
h_rebin.Draw()

# c.Draw()
# # wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
# ROOT.gApplication.Run()

c.SaveAs("rebinning.png")


fSignal.Close()
fSignal1.Close()
