import ROOT
import sys
import argparse

from samples import samples

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--variable", default="DNN_Score", help="Variable to plot")
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")
parser.add_argument("-s", "--suffix", default="", help="Suffix for output file")
args = parser.parse_args()


def FindBinDown(
    hBackground, hSignal, binLimitUp, minNumberOfEventPerBin, MinNumberOfBin_inBinning
):
    binLimitDown = 0.0
    for n in range(binLimitUp - MinNumberOfBin_inBinning - 1, 0, -1):
        error_B = ROOT.Double(0)
        error_S = ROOT.Double(0)
        integral_B = hBackground.IntegralAndError(n + 1, binLimitUp, error_B)
        integral_S = hSignal.IntegralAndError(n + 1, binLimitUp, error_S)

        integral = integral_S + integral_B
        error2 = error_B * error_B + error_S * error_S

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

fSignal = ROOT.TFile.Open(f"{histodir}/{signalSample}Histos.root")
fBackground = ROOT.TFile.Open(f"{histodir}/{signalSample}Histos.root")


hSignal = fSignal.Get(variable + f"___{SR}").Clone()
hBackground = fBackground.Get(variable + f"___{SR}").Clone()


xMax = 5.0
binMinWidth = 0.01
Nbins_binning = hSignal.GetNbinsX()
MinNumberOfBin_inBinning = int(binMinWidth / xMax * Nbins_binning)
binLimitDown = Nbins_binning

minNumberOfEventPerBin = 0.3
hSignal.Scale(samples[signalSample]["xsec"] * samples[data]["lumi"])
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
        hBackground,
        hSignal,
        binLimitUp,
        minNumberOfEventPerBin,
        MinNumberOfBin_inBinning,
    )
    minNumberOfEventPerBin += delta

print("    '" + variable + "' : [0")
for n in range(len(binning_DNN) - 1, 0, -1):
    print(",", binning_DNN[n])

print("]")
print(len(binning_DNN))
