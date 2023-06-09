from labelDict import *
import re
from array import array
from math import *
import ROOT
import sys
import os
import importlib
import time

# import postfitPlot
import argparse
import copy
import ctypes

from args_plot import args

outdir = args.workspace

model = importlib.import_module(args.model)
samples = model.samples
year = "+".join(list(model.data.keys()))
lumi = "%2.1f fb^{-1}"
ROOT.gROOT.ProcessLine(".x setTDRStyle.C")

ROOT.gROOT.SetBatch(True)

totev = {}
totevCount = {}
totevSkim = {}
hnForSys = {}
systematicsSetToUse = []


def makeLegend(xDown, xUp, yDown, yUp, name=""):
    myLegend = ROOT.TLegend(xDown, yDown, xUp, yUp, name)
    myLegend.SetFillStyle(0)
    myLegend.SetFillColor(0)
    myLegend.SetBorderSize(0)
    myLegend.SetTextFont(42)
    myLegend.SetTextSize(0.02)
    return myLegend


def makeText(x, y, someText, font, size=0.05):
    tex = ROOT.TLatex(x, y, someText)
    tex.SetNDC()
    tex.SetTextAlign(35)
    tex.SetTextFont(font)
    tex.SetTextSize(size)
    tex.SetLineWidth(2)
    return tex


def d_value(h1, h2):
    hSignal = h1.Clone()
    hBackground = h2.Clone()
    nbins = hSignal.GetNbinsX()
    hSignal.Scale(1.0 / hSignal.Integral(0, nbins + 1))
    hBackground.Scale(1.0 / hBackground.Integral(0, nbins + 1))

    adiff = 0
    for n in range(nbins + 2):
        adiff += abs(hSignal.GetBinContent(n) - hBackground.GetBinContent(n))
    adiff = adiff / 2.0
    # return str(round(adiff, 2))
    return str(adiff)[0:4]


def setHistoStyle(h, gr, boundary=False):
    h.SetFillColor(model.fillcolor[gr])
    h.SetTitle("")
    h.SetLineColor(model.linecolor[gr])
    if boundary:
        h.SetLineColor(ROOT.kBlack)
        # h.SetLineColor(ROOT.kWhite)
    h.SetFillStyle(1001)  # NEW
    h.SetLineStyle(1)  # NEW


def makeRatioMCplot(h):
    hMC = h.Clone()
    hMC.SetLineWidth(1)
    for n in range(hMC.GetNbinsX() + 1):
        # hMC.SetBinError(n,  hMC.GetBinError(n)/hMC.GetBinContent(n) if hMC.GetBinContent(n)>0 else 0 )
        e = hMC.GetBinError(n) / hMC.GetBinContent(n) if hMC.GetBinContent(n) > 0 else 0
        hMC.SetBinError(n, e if e < 0.5 else 0.5)
        hMC.SetBinContent(n, 0.0)
    return hMC


def setStyle(h, isRatio=False):
    h.SetTitle("")
    w = 0.055 * (2.5 if isRatio else 1.0)
    h.GetYaxis().SetLabelSize(w)
    h.GetXaxis().SetLabelSize(w)
    h.GetYaxis().SetTitleSize(w)
    h.GetXaxis().SetTitleSize(w)
    if isRatio:
        h.GetYaxis().SetTitle("Data/MC - 1")
        h.GetYaxis().SetTitleOffset(0.5)
        #        h.GetXaxis().SetTitle(str(h.GetName()).split("___")[0])
        xKey = str(h.GetName()).split("___")[0]
        h.GetXaxis().SetTitle(
            labelVariable[xKey] if xKey in list(labelVariable.keys()) else xKey
        )
    else:
        binWidht = str(h.GetBinWidth(1))[:4]
        if binWidht.endswith("."):
            binWidht = binWidht[:3]
        h.GetXaxis().SetLabelSize(0)
        h.GetYaxis().SetTitle("Entries/" + binWidht)
        h.GetXaxis().SetLabelSize(0)
        h.GetXaxis().SetTitleSize(0)


def findSyst(hn, sy, f, silent=False):
    #  print hnForSys.keys()
    if hn in hnForSys and sy in hnForSys[hn]:
        #       print hn,sy,hnForSys[hn]
        return hnForSys[hn][sy]
    if hn not in hnForSys:
        hnForSys[hn] = {}
    allh = list([x.GetName() for x in f.GetListOfKeys()])
    h1 = hn + "__syst__" + sy
    h2 = re.sub("___", "__syst__" + sy + "___", hn)
    h3 = re.sub("___", "__syst__" + sy + "___", hn) + "__syst__" + sy
    #    print "Syst options",h1,h2,h3
    if h1 in allh:
        hnForSys[hn][sy] = h1
        return h1
    if h2 in allh:
        hnForSys[hn][sy] = h2
        return h2
    if h3 in allh:
        hnForSys[hn][sy] = h3
        return h3
    if not silent:
        print("none matching", hn, sy, f)
    return ""


def writeYields(ftxt, gr, integral, error, dataEvents):
    if dataEvents != 0:
        line = "%s,%s,%s,%s " % (
            gr,
            round(integral[gr]["nom"], 5),
            round(error[gr], 5),
            round(integral[gr]["nom"] / dataEvents, 5),
        )
    else:
        line = "%s,%s,%s,%s " % (
            gr,
            round(integral[gr]["nom"], 5),
            round(error[gr], 5),
            0,
        )
    # line = "%s\t%s +- %s\t%s "%(gr,round(integral[gr]["nom"],5), round(error[gr],5),round(integral[gr]["nom"]/dataEvents,5))
    for sy in sorted(integral[gr].keys()):
        if sy != "nom":
            line += ",%s " % (round(integral[gr][sy], 5))
    ftxt.write(line + "\n")


def powerHisto(histo1, power):
    #        print histo1.GetName()
    for i in range(len(histo1) + 2):
        val = histo1.GetBinContent(i)
        if val != 0:
            histo1.SetBinContent(i, (pow(val, power) if val > 0 else -pow(-val, power)))
        else:
            histo1.SetBinContent(i, 0.0)
        histo1.SetBinError(i, 0.0)
    #                print histo1.GetBinContent(i)
    return histo1


def makeAlternativeShape(
    hn, sy, f, nominalSample, alternativeSamples, alphaUp=+1, alphaDown=-1
):
    (altSampleUp, altSampleDown) = alternativeSamples
    if not altSampleUp in f:
        f[altSampleUp] = ROOT.TFile.Open(folder + "/%sHistos.root" % altSampleUp)
    if not altSampleDown in f:
        f[altSampleDown] = ROOT.TFile.Open(folder + "/%sHistos.root" % altSampleDown)
    histoNameNom = hn + "rebin"
    histoNameUp = hn + "rebinAltSampleUp"
    histoNameDown = hn + "rebinAltSampleDown"
    histoNom = f[nominalSample].Get(hn).Clone(histoNameNom)
    histoUp = f[altSampleUp].Get(hn).Clone(histoNameUp)
    histoDown = f[altSampleDown].Get(hn).Clone(histoNameDown)
    if hn.split("___")[0] in list(model.rebin.keys()):
        histoNom = histoNom.Rebin(
            len(model.rebin[hn.split("___")[0]]) - 1,
            "hnew" + sy,
            array("d", model.rebin[hn.split("___")[0]]),
        )
        histoUp = histoUp.Rebin(
            len(model.rebin[hn.split("___")[0]]) - 1,
            "hnew" + sy,
            array("d", model.rebin[hn.split("___")[0]]),
        )
        histoDown = histoDown.Rebin(
            len(model.rebin[hn.split("___")[0]]) - 1,
            "hnew" + sy,
            array("d", model.rebin[hn.split("___")[0]]),
        )
    histoUp.Scale(samples[altSampleUp]["xsec"])
    histoDown.Scale(samples[altSampleDown]["xsec"])
    ratio = histoUp.Clone(histoNameUp.replace("altSampleUp", "altSampleRatio"))
    ratio.Divide(histoDown)
    ## up   = ratio^alpha_up   * nom
    histoNameSyst = hn.replace("___", "__syst__%s___" % sy) + "__syst__%s" % sy
    histoSyst = histoNom.Clone(histoNameSyst)

    alpha = None
    if "Up" in sy:
        alpha = alphaUp
    ## down = ratio^alpha_down * nom
    elif "Down" in sy:
        alpha = alphaDown
    else:
        print("No alternative sample for %s" % d)
    if alpha:
        histoSyst.Multiply(powerHisto(ratio, alpha))
    #    print "Making %s using %s %s %s %s %s %f"%(sy, nominalSample, alternativeSamples, str(alpha), hn, histoNameSyst, histoSyst.GetMean()/histoNom.GetMean())
    return copy.copy(histoSyst)


def makeEnvelopeShape(hn, sy, f, d, model):
    sy_base = sy.replace("Up", "").replace("Down", "")
    envelope = model.systematicDetail[sy_base]["envelope"]
    envelopeFunction = model.systematicDetail[sy_base]["envelopeFunction"]
    envelopeFunctionParameter = model.systematicDetail[sy_base][
        "envelopeFunctionParameter"
    ]
    envelopeFunctionParameterValues = model.systematicDetail[sy_base][
        "envelopeFunctionParameterValues"
    ]
    envelopeFunctionRange = model.systematicDetail[sy_base]["envelopeFunctionRange"]
    if not "envelopeBinning" in model.systematicDetail[sy_base]:
        model.systematicDetail[sy_base]["envelopeBinning"] = {}
    # uncomment if you want to use the standard binning (ie. ignore "envelopeNBins")
    if hn.split("___")[0] in list(model.rebin.keys()):
        model.systematicDetail[sy_base]["envelopeBinning"][(hn, d)] = model.rebin[
            hn.split("___")[0]
        ]

    nomHistoRebinned = f[d].Get(hn).Clone("nomHistoRebinned")
    if (hn, d) in model.systematicDetail[sy_base]["envelopeBinning"]:
        envelopeBinning = model.systematicDetail[sy_base]["envelopeBinning"][(hn, d)]
        nomHistoRebinned = nomHistoRebinned.Rebin(
            len(envelopeBinning) - 1,
            nomHistoRebinned.GetName(),
            array("d", envelopeBinning),
        )
    else:
        envelopeBinning = None

    pdfReplica = "LHEPdfReplica"
    pdfHessian = "LHEPdfHessian"
    if f[d].Get(findSyst(hn, pdfHessian + "0", f[d], silent=True)):
        pdf = pdfHessian
    elif f[d].Get(findSyst(hn, pdfReplica + "0", f[d], silent=True)):
        pdf = pdfReplica
    else:
        print(
            "makeEnvelopeShape - Warning: neither LHEPdfHessian nor LHEPdfReplica found for %s %s"
            % (d, hn)
        )
        return

    try:
        LHApdf_min = f[d].Get("LHApdf_down").GetVal()
        LHApdf_max = f[d].Get("LHApdf_up").GetVal()
    except:
        print("WARNING makeEnvelopeShape: LHApdf_down not found", hn, sy, f, d, model)
        print("I will consider ", pdf)
        LHApdf_min = -1
        LHApdf_max = -1

    ratio = nomHistoRebinned.Clone("ratio")
    ratio.Reset()

    funct = ROOT.TF1(
        "funct",
        envelopeFunction,
        nomHistoRebinned.GetXaxis().GetXmin(),
        nomHistoRebinned.GetXaxis().GetXmax(),
    )
    #    funct = ROOT.TF1("funct",envelopeFunction,envelopeFunctionRange[0],envelopeFunctionRange[1])
    funct.SetParameters(*envelopeFunctionParameterValues)
    par2 = 0
    i = 0
    hs = f[d].Get(findSyst(hn, pdf + str(i), f[d]))
    badFit = 0
    hs0 = None
    while hs and hs.GetMaximum() > 0:
        if envelopeBinning:
            hs = hs.Rebin(
                len(envelopeBinning) - 1,
                nomHistoRebinned.GetName(),
                array("d", envelopeBinning),
            ).Clone(hs.GetName())
        if i == 0:
            if LHApdf_min == 91400:
                hs0 = hs.Clone("hs0")
                i += 1
                badFit += 1
                hs = f[d].Get(findSyst(hn, pdf + str(i), f[d]))
                continue
            else:
                hs0 = nomHistoRebinned

        ratio.Divide(hs, hs0)
        ratio.Fit(funct, "QN0R")
        if abs(funct.GetParameter(0) - 1) < 0.2:
            par2 += (
                funct.GetParameter(envelopeFunctionParameter)
                - envelopeFunctionParameterValues[envelopeFunctionParameter]
            ) ** 2
        else:
            badFit += 1
            print(
                "BAD Fit",
                hn,
                sy,
                f,
                d,
                model,
                funct.GetParameter(0),
                funct.GetParameter(1),
                end=" ",
            )
        i = i + 1
        hs = f[d].Get(findSyst(hn, pdf + str(i), f[d]))

    # if not hessian
    if (
        not (
            (LHApdf_min < 0 and pdf == pdfHessian)
            or LHApdf_min
            in [
                303000,
                303200,
                304200,
                304400,
                304600,
                304800,
                305800,
                306000,
                306200,
                306400,
                91400,
            ]
        )
        and (i - badFit) > 0
    ):
        print("REPLICAS, not HESSIAN for", hn, sy, f, d, model)
        par2 = par2 / (i - badFit)

    funct.SetParameters(*envelopeFunctionParameterValues)
    if "Up" in sy:
        funct.SetParameter(
            envelopeFunctionParameter,
            envelopeFunctionParameterValues[envelopeFunctionParameter] + par2**0.5,
        )
    elif "Down" in sy:
        funct.SetParameter(
            envelopeFunctionParameter,
            envelopeFunctionParameterValues[envelopeFunctionParameter] - par2**0.5,
        )
    else:
        raise Exception("Error in makeEnvelopeShape")

    nhisto = nomHistoRebinned.Clone(hn + sy)
    nhisto.Multiply(funct)
    print(
        "Creating %s using %s" % (nhisto.GetName(), pdf),
        nhisto.Integral(),
        funct.GetParameters()[0],
        funct.GetParameters()[1],
    )
    return copy.copy(nhisto)


def makeEnvelopeShapeOld(hn, sy, f, d, model):
    sy_base = sy.replace("Up", "").replace("Down", "")
    envelope = model.systematicDetail[sy_base]["envelope"]
    envelopeFunction = model.systematicDetail[sy_base]["envelopeFunction"]
    envelopeNBins = model.systematicDetail[sy_base]["envelopeNBins"]
    if not "envelopeBinning" in model.systematicDetail[sy_base]:
        model.systematicDetail[sy_base]["envelopeBinning"] = {}
    # uncomment if you want to use the standard binning (ie. ignore "envelopeNBins")
    #    if hn.split("___")[0] in model.rebin.keys():
    #        model.systematicDetail[sy_base]["envelopeBinning"][(hn, d)] = model.rebin[hn.split("___")[0]]
    if not (hn, d) in model.systematicDetail[sy_base]["envelopeBinning"]:
        binning = [0]
        nomHisto = f[d].Get(hn).Clone()
        binWeight = nomHisto.Integral() / envelopeNBins
        tmp = 0
        for i in range(len(nomHisto)):
            tmp += nomHisto.GetBinContent(i)
            if tmp > binWeight:
                tmp = 0
                binning.append(nomHisto.GetBinLowEdge(i))
        binning.append(nomHisto.GetBinLowEdge(i))
        model.systematicDetail[sy_base]["envelopeBinning"][(hn, d)] = binning

    envelopeBinning = model.systematicDetail[sy_base]["envelopeBinning"][(hn, d)]
    nomHistoRebinned = f[d].Get(hn).Clone("nomHistoRebinned")
    nomHistoRebinned = nomHistoRebinned.Rebin(
        len(envelopeBinning) - 1,
        nomHistoRebinned.GetName(),
        array("d", envelopeBinning),
    )

    pdfReplica = "LHEPdfReplica"
    pdfHessian = "LHEPdfHessian"
    if f[d].Get(findSyst(hn, pdfHessian + "0", f[d], silent=True)):
        pdf = pdfHessian
    elif f[d].Get(findSyst(hn, pdfReplica + "0", f[d], silent=True)):
        pdf = pdfReplica
    else:
        print(
            "makeEnvelopeShape - Warning: neither LHEPdfHessian nor LHEPdfReplica found for %s %s"
            % (d, hn)
        )
        return

    try:
        LHApdf_min = f[d].Get("LHApdf_down").GetVal()
        LHApdf_max = f[d].Get("LHApdf_up").GetVal()
    except:
        print("WARNING makeEnvelopeShape: LHApdf_down not found", hn, sy, f, d, model)
        print("I will consider ", pdf)
        LHApdf_min = -1
        LHApdf_max = -1

    ratio = nomHistoRebinned.Clone("ratio")
    ratio.Reset()
    sums = [0] * len(ratio)
    sumSquares = [0] * len(ratio)
    i = 0  # nominal is the first entry.
    hs = f[d].Get(findSyst(hn, pdf + str(i), f[d], silent=True))
    hs = hs.Rebin(len(envelopeBinning) - 1, hs.GetName(), array("d", envelopeBinning))
    #        Calculate ratio wrt to PDF0:
    hs0 = hs
    while hs and hs.GetMaximum() > 0:
        hs = hs.Rebin(
            len(envelopeBinning) - 1, hs.GetName(), array("d", envelopeBinning)
        )
        for bin_ in range(1, len(ratio)):
            rat = (
                hs.GetBinContent(bin_) / hs0.GetBinContent(bin_)
                if hs0.GetBinContent(bin_) > 0
                else 0.0
            )
            sums[bin_] += rat
            sumSquares[bin_] += rat**2
        i = i + 1
        hs = f[d].Get(findSyst(hn, pdf + str(i), f[d], silent=True))
    meanrms = 0.0
    ngood = 0
    for bin_ in range(len(ratio) - 1):
        if sumSquares[bin_] > 0:
            rms = (sumSquares[bin_] / i - (sums[bin_] / i) ** 2) ** 0.5
            # If hessian (numbers from checkLHAPdf.py and https://lhapdf.hepforge.org/pdfsets)
            # if not hessian
            if not (
                (LHApdf_min < 0 and pdf == pdfHessian)
                or LHApdf_min
                in [
                    303000,
                    303200,
                    304200,
                    304400,
                    304600,
                    304800,
                    305800,
                    306000,
                    306200,
                    306400,
                    91400,
                ]
            ):
                rms = rms * (i**0.5)
            meanrms += rms
            ngood += 1
        else:
            rms = 10.0  # large error if no MC stat
        ratio.SetBinContent(bin_, 0.0)
        ratio.SetBinError(bin_, rms)

    meanrms /= ngood if ngood != 0 else 1
    funct = ROOT.TF1(
        "funct",
        envelopeFunction.format(
            up=(1.0 if "Up" in sy else -1.0),
            rms=meanrms,
            xmin=nomHistoRebinned.GetXaxis().GetXmin(),
            xmax=nomHistoRebinned.GetXaxis().GetXmax(),
        ),
        nomHistoRebinned.GetXaxis().GetXmin(),
        nomHistoRebinned.GetXaxis().GetXmax(),
    )
    nhisto = f[d].Get(hn).Clone(hn + sy)
    if hn.split("___")[0] in list(model.rebin.keys()):
        nhisto = (
            nhisto.Rebin(
                len(model.rebin[hn.split("___")[0]]) - 1,
                "hnew" + sy,
                array("d", model.rebin[hn.split("___")[0]]),
            )
        ).Clone(hn + "rebinned")
    copyhisto = nhisto.Clone("copya")
    for bin_ in range(len(nhisto) - 1):
        x = nhisto.GetBinCenter(bin_)
        rms = ratio.GetBinError(ratio.FindBin(x))
        f = funct.Eval(x)
        nhisto.SetBinContent(bin_, copyhisto.GetBinContent(bin_) * (1.0 + f * rms))
        nhisto.SetBinError(bin_, 0)
    # DEBUG: Save ratio plots
    #    testFile = ROOT.TFile("debug/%s_%s_%s.root"%(hn,sy, d),"recreate")
    #    funct.Write()
    #    ratio.Write()
    #    testFile.Close()
    return copy.copy(nhisto)


f = {}
folder = args.histfolder
for group in model.signal:
    for s in model.signal[group]:
        f[s] = ROOT.TFile.Open(folder + "%sHistos.root" % s)
#        f[s]=ROOT.TFile.Open("out/%sHistos.root"%s)
for group in model.background:
    for b in model.background[group]:
        #        f[b]=ROOT.TFile.Open("out/%sHistos.root"%b)
        f[b] = ROOT.TFile.Open(folder + "/%sHistos.root" % b)
for group in model.data:
    for d in model.data[group]:
        #       f[d]=ROOT.TFile.Open("out/%sHistos.root"%d)
        f[d] = ROOT.TFile.Open(folder + "/%sHistos.root" % d)

histoNames = list(
    set([x.GetName() for y in list(f.keys()) for x in f[y].GetListOfKeys()])
)

canvas = {}
datastack = {}
datasum = {}
histos = {}
histosum = {}
histosSig = {}
histoSigsum = {}

datasumSyst = {}
histosumSyst = {}
histoSigsumSyst = {}
histosSignal = {}
all_histo_all_syst = {}

integral = {}
error = {}

histoSingleSyst = {}

# i=1
ROOT.gStyle.SetOptStat(0)


def addHistoInTStack(hs, stackSys, all_histo_all_syst, gr, hn, sy, d, makeWorkspace):
    #    print "Adding %s with integral %f"%(hs.GetName(), hs.Integral())
    if sy not in list(stackSys[hn].keys()):
        stackSys[hn][sy] = hs.Clone()
    else:
        stackSys[hn][sy].Add(hs)

    if sy not in list(integral[gr].keys()):
        integral[gr][sy] = hs.Integral(0, hs.GetNbinsX() + 1)
    else:
        integral[gr][sy] += hs.Integral(0, hs.GetNbinsX() + 1)

    if makeWorkspace:
        all_histo_all_syst[hn][d][sy] = hs.Clone()


def getYear(sample):
    if "201" in sample:
        return "201" + sample.split("201")[1][:1]
    else:
        raise Exception("ERROR in getYear ( sample = %s ) " % sample)
        return


def fill_datasum(
    f,
    gr,
    samplesToPlot,
    SumTH1,
    stack,
    stackSys,
    hn,
    myLegend,
    ftxt,
    lumis=[],
    data=False,
):
    integral[gr] = {}
    integral[gr]["nom"] = 0
    error[gr] = 0
    lumi = 59000
    # for d in samplesToPlot[gr]:
    for n in range(len(samplesToPlot[gr])):
        d = samplesToPlot[gr][n]
        if lumis:
            # yr = getYear(d)
            yr = "2018"
            lumi = lumis[yr]
        if makeWorkspace:
            all_histo_all_syst[hn][d] = {}
        if f[d]:
            h = f[d].Get(hn)
            histoSingleSyst[hn][d] = {}
            if h:
                if hn.split("___")[0] in list(model.rebin.keys()):
                    # print "Rebin",hn
                    h = h.Rebin(
                        len(model.rebin[hn.split("___")[0]]) - 1,
                        "hnew",
                        array("d", model.rebin[hn.split("___")[0]]),
                    )
                h = h.Clone(hn + "rebinned")
                if data:
                    h.SetMarkerStyle(20)
                    h.SetMarkerColor(ROOT.kBlack)
                    h.SetLineColor(ROOT.kBlack)
                else:
                    # if postfit : addFitVariation( h, fitVariation(model, f, d, hn, h, histoSingleSyst))
                    print(
                        h.GetSumOfWeights(),
                        h.GetEntries(),
                        lumi * samples[d]["xsec"],
                        d,
                    )
                    h.Scale(samples[d]["xsec"] * lumi)
                    error_b = ctypes.c_double(0)
                    integral[gr]["nom"] += h.IntegralAndError(
                        0, h.GetNbinsX() + 1, error_b
                    )
                    error[gr] = sqrt(
                        error[gr] * error[gr] + error_b.value * error_b.value
                    )
                    # non funziona: d==samplesToPlot[gr][-1])
                    setHistoStyle(h, gr)
                if hn not in SumTH1:
                    SumTH1[hn] = h.Clone()
                    stackSys[hn] = {}
                    for sy in systematicsSetToUse:
                        sy_base = sy.replace("Up", "").replace("Down", "")
                        if not data:
                            if (
                                sy_base in model.systematicDetail
                                and "alternativeSamples"
                                in model.systematicDetail[sy_base]
                            ):
                                if (
                                    d
                                    in model.systematicDetail[sy_base][
                                        "alternativeSamples"
                                    ]
                                ):
                                    hs = makeAlternativeShape(
                                        hn,
                                        sy,
                                        f,
                                        d,
                                        model.systematicDetail[sy_base][
                                            "alternativeSamples"
                                        ][d],
                                        model.systematicDetail[sy_base]["powerUp"],
                                        model.systematicDetail[sy_base]["powerDown"],
                                    )
                                else:
                                    hs = f[d].Get(hn).Clone(hn + sy)
                                    if hs and hn.split("___")[0] in list(
                                        model.rebin.keys()
                                    ):
                                        hs = (
                                            hs.Rebin(
                                                len(model.rebin[hn.split("___")[0]])
                                                - 1,
                                                "hnew" + sy,
                                                array(
                                                    "d", model.rebin[hn.split("___")[0]]
                                                ),
                                            )
                                        ).Clone(hs.GetName() + "rebinned")
                            elif (
                                sy_base in model.systematicDetail
                                and "envelope" in model.systematicDetail[sy_base]
                            ):
                                hs = makeEnvelopeShape(hn, sy, f, d, model)
                            else:
                                hs = f[d].Get(findSyst(hn, sy, f[d]))
                                if hs and hn.split("___")[0] in list(
                                    model.rebin.keys()
                                ):
                                    hs = (
                                        hs.Rebin(
                                            len(model.rebin[hn.split("___")[0]]) - 1,
                                            "hnew" + sy,
                                            array("d", model.rebin[hn.split("___")[0]]),
                                        )
                                    ).Clone(hs.GetName() + "rebinned")
                            # if postfit :
                            # hs=f[d].Get(hn).Clone()
                            if hs:
                                # if postfit : addFitVariation( hs, fitVariation(model, f, d, hn, h, histoSingleSyst, sy))
                                if (
                                    sy_base in list(model.systematicDetail.keys())
                                    and "normalizationType"
                                    in list(model.systematicDetail[sy_base].keys())
                                    and model.systematicDetail[sy_base][
                                        "normalizationType"
                                    ]
                                    == "shapeOnly"
                                    and hs.Integral(0, hs.GetNbinsX() + 1) > 0
                                ):
                                    hs.Scale(
                                        h.Integral(0, h.GetNbinsX() + 1)
                                        / hs.Integral(0, hs.GetNbinsX() + 1)
                                    )
                                else:
                                    hs.Scale(samples[d]["xsec"] * lumi)
                                addHistoInTStack(
                                    hs,
                                    stackSys,
                                    all_histo_all_syst,
                                    gr,
                                    hn,
                                    sy,
                                    d,
                                    makeWorkspace,
                                )
                            else:
                                print("missing", sy, "for", hn, gr, d)
                                addHistoInTStack(
                                    h,
                                    stackSys,
                                    all_histo_all_syst,
                                    gr,
                                    hn,
                                    sy,
                                    d,
                                    makeWorkspace,
                                )
                        else:
                            addHistoInTStack(
                                h,
                                stackSys,
                                all_histo_all_syst,
                                gr,
                                hn,
                                sy,
                                d,
                                makeWorkspace,
                            )
                else:
                    SumTH1[hn].Add(h)
                    for sy in systematicsSetToUse:
                        sy_base = sy.replace("Up", "").replace("Down", "")
                        if (
                            sy_base in model.systematicDetail
                            and "alternativeSamples" in model.systematicDetail[sy_base]
                        ):
                            if (
                                d
                                in model.systematicDetail[sy_base]["alternativeSamples"]
                            ):
                                hs = makeAlternativeShape(
                                    hn,
                                    sy,
                                    f,
                                    d,
                                    model.systematicDetail[sy_base][
                                        "alternativeSamples"
                                    ][d],
                                    model.systematicDetail[sy_base]["powerUp"],
                                    model.systematicDetail[sy_base]["powerDown"],
                                )
                            else:
                                hs = f[d].Get(hn).Clone(hn + sy)
                                if hs and hn.split("___")[0] in list(
                                    model.rebin.keys()
                                ):
                                    hs = (
                                        hs.Rebin(
                                            len(model.rebin[hn.split("___")[0]]) - 1,
                                            "hnew" + sy,
                                            array("d", model.rebin[hn.split("___")[0]]),
                                        )
                                    ).Clone(hs.GetName() + "rebinned")
                        elif (
                            sy_base in model.systematicDetail
                            and "envelope" in model.systematicDetail[sy_base]
                        ):
                            hs = makeEnvelopeShape(hn, sy, f, d, model)
                        else:
                            hs = f[d].Get(findSyst(hn, sy, f[d]))
                            if hs and hn.split("___")[0] in list(model.rebin.keys()):
                                hs = (
                                    hs.Rebin(
                                        len(model.rebin[hn.split("___")[0]]) - 1,
                                        "hnew" + sy,
                                        array("d", model.rebin[hn.split("___")[0]]),
                                    )
                                ).Clone(hs.GetName() + "rebinned")
                        # if postfit :
                        # hs=f[d].Get(hn).Clone()
                        if hs:
                            # if postfit : addFitVariation( hs, fitVariation(model, f, d, hn, h, histoSingleSyst, sy))
                            if not data:
                                if (
                                    sy_base in list(model.systematicDetail.keys())
                                    and "normalizationType"
                                    in list(model.systematicDetail[sy_base].keys())
                                    and model.systematicDetail[sy_base][
                                        "normalizationType"
                                    ]
                                    == "shapeOnly"
                                    and hs.Integral(0, hs.GetNbinsX() + 1) > 0
                                ):
                                    hs.Scale(
                                        h.Integral(0, h.GetNbinsX() + 1)
                                        / hs.Integral(0, hs.GetNbinsX() + 1)
                                    )
                                else:
                                    hs.Scale(samples[d]["xsec"] * lumi)
                            addHistoInTStack(
                                hs,
                                stackSys,
                                all_histo_all_syst,
                                gr,
                                hn,
                                sy,
                                d,
                                makeWorkspace,
                            )
                        else:
                            print("missing", sy, "for", hn, gr, d)
                            addHistoInTStack(
                                h,
                                stackSys,
                                all_histo_all_syst,
                                gr,
                                hn,
                                sy,
                                d,
                                makeWorkspace,
                            )
                stack[hn].Add(h)
                # if n==0 : stack[hn].Add(h)
                # else :
                # stack[hn].GetHists()[-1].Add(h)
                # stack[hn].GetStack().Last().Add(h)
                if makeWorkspace:
                    all_histo_all_syst[hn][d]["nom"] = h.Clone()
            else:
                print("Cannot open", d, hn)
                exit(1)
            if gr in model.signal:
                if gr not in list(histosSignal[hn].keys()):
                    histosSignal[hn][gr] = h.Clone()
                else:
                    histosSignal[hn][gr].Add(h)
    if not data:
        writeYields(
            ftxt,
            gr,
            integral,
            error,
            SumTH1[hn].Integral(0, SumTH1[hn].GetNbinsX() + 1),
        )
    # if not data :
    # ftxt.write("%s\t%s +- %s\t%s \n"%(gr,integral[gr]["nom"], error[gr],integral[gr]["nom"]/datasum[hn].Integral(0,datasum[hn].GetNbinsX()+1)))
    # for sy in integral[gr].keys() : ftxt.write("%s\t%s +- %s\t%s \n"%(gr,integral[gr]["nom"], error[gr],integral[gr]["nom"]/datasum[hn].Integral(0,datasum[hn].GetNbinsX()+1)))
    # if (data) : myLegend.AddEntry(h,"data","P")
    # else : myLegend.AddEntry(h,gr,"f")
    return h


date_time = time.strftime("%m%d-%H%M%S")


def makeplot(hn, saveintegrals=True):
    if "__syst__" not in hn:
        dictLegendBackground = dict()
        dictLegendSignal = dict()

        myLegend_1 = makeLegend(0.58, 0.68, 0.75, 0.92)
        myLegend_2 = makeLegend(0.68, 0.78, 0.75, 0.92)

        myLegend_sy = makeLegend(0.85, 1, 0.1, 0.15 + 0.015 * len(systematicsSetToUse))
        outpath = (
            f"{args.outfolder}/{year}/{model.name}_{args.foldersuffix}_{date_time}"
        )
        os.system("mkdir -p " + outpath)
        os.system("cp " + args.histfolder + "/description.txt " + outpath)
        #        os.system("git rev-parse HEAD > "+outpath+"/git_commit.txt")
        #        os.system("git diff HEAD > "+outpath+"/git_diff.txt")
        #        os.system("git status HEAD > "+outpath+"/git_status.txt")
        YieldFileName = outpath + "/" + hn + ".csv"
        if postfit:
            YieldFileName = outpath + "/" + hn + "_postFit.txt"
        ftxt = open(YieldFileName, "w")
        # print "Making histo",hn
        histos[hn] = ROOT.THStack(hn, "")
        histosSig[hn] = ROOT.THStack(hn, "")
        datastack[hn] = ROOT.THStack(hn, "")

        # canvas[hn]=ROOT.TCanvas("canvas_"+hn,"",900,750)
        # canvas[hn].SetLeftMargin(0.2)

        if makeWorkspace:
            all_histo_all_syst[hn] = {}

        lumitot = 0
        lumis = {}
        print(("model.data=", model.data))
        for gr in model.data:
            for d in model.data[gr]:
                lumitot += samples[d]["lumi"]
                print("lumitot=%f" % lumitot)
                # yr = getYear(d)
                yr = "2018"
                if yr in lumis:
                    lumis[yr] += samples[d]["lumi"]
                else:
                    lumis[yr] = samples[d]["lumi"]

        print(("lumis=", lumis))

        histoSingleSyst[hn] = {}
        histosSignal[hn] = {}
        for gr in model.data:
            h = fill_datasum(
                f,
                gr,
                model.data,
                SumTH1=datasum,
                stack=datastack,
                stackSys=datasumSyst,
                hn=hn,
                myLegend=myLegend_1,
                ftxt=ftxt,
                data=True,
            )
            myLegend_1.AddEntry(h, "Data", "PL")

        DataYieldLine = "sample,yield,uncert,fraction"
        for sy in systematicsSetToUse:
            DataYieldLine = DataYieldLine + "," + sy + ""
        ftxt.write(DataYieldLine + "\n")
        # if saveintegrals:
        if hn in datasum.keys():
            ftxt.write(
                "DATA,%s \n" % (datasum[hn].Integral(0, datasum[hn].GetNbinsX() + 1))
            )

        for gr in model.backgroundSorted:
            h = fill_datasum(
                f,
                gr,
                model.background,
                SumTH1=histosum,
                stack=histos,
                stackSys=histosumSyst,
                hn=hn,
                myLegend=myLegend_1,
                ftxt=ftxt,
                lumis=lumis,
            )
            dictLegendBackground[gr] = h

        for gr in model.signal:
            h = fill_datasum(
                f,
                gr,
                model.signal,
                SumTH1=histoSigsum,
                stack=histosSig,
                stackSys=histoSigsumSyst,
                hn=hn,
                myLegend=myLegend_1,
                ftxt=ftxt,
                lumis=lumis,
            )
            dictLegendSignal[gr] = h

        # myLegend.AddEntry(None, "", "")
        for gr in model.backgroundSortedForLegend:
            myLegend_2.AddEntry(dictLegendBackground[gr], labelLegend[gr], "FL")
        # myLegend.AddEntry(None, "", "")
        for gr in model.signalSortedForLegend:
            myLegend_1.AddEntry(dictLegendSignal[gr], labelLegend[gr], "FL")
        # myLegend.AddEntry(None, "", "")
        # superImposedPlot (histos[hn], histosSig[hn], outpath)
        # if makeWorkspace : return

        # histosum[hn].Add(histoSigsum[hn])
        # ftxt.write("d_value = "+d_value(histosum[hn], histoSigsum[hn]))

        if model.signal:
            S = histoSigsum[hn].Clone()
            B = histosum[hn].Clone()
            B.Add(S)
            R = S.Divide(B)
            fR = ROOT.TFile.Open(outpath + "/%s_SBratio.root" % hn, "recreate")
            S.Write()
            fR.Close()

        # for gr in model.signalSortedForLegend:
        #     h = histosSignal[hn][gr]
        #     histos[hn].Add(h.Clone())
        #     h.SetLineColor(model.linecolor[gr])
        #     h.SetFillStyle(0)
        #     h.SetLineWidth(3)
        #     h.SetLineStyle(2)
        #     h.Scale(5000.0)
        #     myLegend_1.AddEntry(h, gr + " x5k", "l")
        firstBlind = 100000
        lastBlind = -1

        if model.signal:
            for i in range(histosSig[hn].GetStack().Last().GetNbinsX() + 1):
                if (
                    histosSig[hn].GetStack().Last().GetBinContent(i)
                    > 0.1 * sqrt(abs(histos[hn].GetStack().Last().GetBinContent(i)))
                    and histosSig[hn].GetStack().Last().GetBinContent(i)
                    / (0.001 + abs(histos[hn].GetStack().Last().GetBinContent(i)))
                    > 0.05
                ):
                    # print "to blind",hn,i,abs(histos[hn].GetStack().Last().GetBinContent(i)), histosSig[hn].GetStack().Last().GetBinContent(i)
                    if i < firstBlind:
                        firstBlind = i
                    lastBlind = i
            if False:  # blind!
                for i in range(firstBlind, lastBlind + 1):
                    datastack[hn].GetStack().Last().SetBinContent(i, 0)
                    datasum[hn].SetBinContent(i, 0)
                    # print "blinded",i,hn

        myLegend_2.AddEntry(histosum[hn], "MC uncert. (stat.)", "FL")

        canvas[hn] = ROOT.TCanvas("canvas_" + hn, "", 1200, 1000)
        # canvas[hn].SetRightMargin(.0);
        canvas_log = ROOT.TCanvas("canvas_log_" + hn, "", 1200, 1000)
        # canvas[hn].SetRightMargin(.0);
        canvas_tuple = (canvas_log, canvas[hn])

        for i, c in enumerate(canvas_tuple):
            c.Divide(1, 2)
            c.GetPad(2).SetPad(0.0, 0.0, 0.90, 0.25)
            c.GetPad(1).SetPad(0.0, 0.20, 0.90, 1.0)

            ROOT.gStyle.SetPadLeftMargin(0.2)
            c.GetPad(2).SetBottomMargin(0.35)
            c.GetPad(2).SetTopMargin(0.0)

            c.cd()

            myLegend_1.Draw()  # NEW
            myLegend_2.Draw()  # NEW

            c.cd(1)

            histos[hn].SetTitle("")
            if hn in datasum.keys():
                datasum[hn].SetMinimum(
                    max(0.1 * datasum[hn].GetMinimum(), 0.1)
                )  # zoom out y axis
                if i == 0:
                    datasum[hn].SetMaximum(
                        max(2 * datasum[hn].GetMaximum(), 2 * histosum[hn].GetMaximum())
                    )  # zoom out y axis
                else:
                    datasum[hn].SetMaximum(
                        max(
                            (datasum[hn].GetMaximum()) ** 2,
                            (histosum[hn].GetMaximum()) ** 2,
                        )
                    )  # zoom out y axis

                datasum[hn].Draw("E P")
                # datastack[hn].GetXaxis().SetTitle(hn)
                setStyle(datasum[hn])
                datasum[hn].Draw("E P")
                histos[hn].Draw("hist same")
            else:
                histos[hn].SetMinimum(
                    max(0.1 * histos[hn].GetMinimum(), 0.1)
                )  # zoom out y axis
                if i == 0:
                    histos[hn].SetMaximum(
                        max(2 * datasum[hn].GetMaximum(), 2 * histosum[hn].GetMaximum())
                    )
                else:
                    histos[hn].SetMaximum(
                        max(
                            (datasum[hn].GetMaximum()) ** 2,
                            (histosum[hn].GetMaximum()) ** 2,
                        )
                    )
                histos[hn].Draw("hist")

            #  histos[hn].Draw("hist")
            histosum[hn].SetLineWidth(0)
            histosum[hn].SetFillColor(ROOT.kBlack)
            histosum[hn].SetFillStyle(3004)
            setStyle(histos[hn].GetStack().Last())
            c.Update()
            histosum[hn].Draw("same E2")

            if hn in datasum.keys():
                datasum[hn].Draw("E P sameaxis")
                datasum[hn].Draw("E P same")
            for gr in model.signal:
                histosSignal[hn][gr].Draw("hist same")

            t0 = makeText(
                0.4,
                0.8,
                labelRegion[hn.split("___")[1]]
                if hn.split("___")[1] in list(labelRegion.keys())
                else hn.split("___")[1],
                42,
                size=0.04,
            )
            t1 = makeText(0.25, 0.95, "CMS", 61)
            t2 = makeText(0.45, 0.95, str(year), 42)
            t3 = makeText(0.95, 0.95, lumi % (lumitot / 1000.0) + "  (13 TeV)", 42)
            # td = makeText(
            #     0.85, 0.78, "d = " + d_value(histosum[hn], histoSigsum[hn]), 42, 0.04
            # )
            t0.Draw()
            t1.Draw()
            t2.Draw()
            t3.Draw()
            # td.Draw()
            if hn in datasum.keys():
                datasum[hn].SetMarkerStyle(20)
                datasum[hn].SetMarkerColor(ROOT.kBlack)
                datasum[hn].SetLineColor(ROOT.kBlack)
                c.Update()
                ratio = datasum[hn].Clone()
                ratio.Add(histosum[hn], -1.0)
                ratio.Divide(histosum[hn])
                for n in range(datasum[hn].GetNbinsX() + 2):
                    if datasum[hn].GetBinContent(n) > 0:
                        ratio.SetBinError(
                            n,
                            datasum[hn].GetBinError(n)
                            / (
                                histosum[hn].GetBinContent(n)
                                if histosum[hn].GetBinContent(n) > 0
                                else datasum[hn].GetBinContent(n)
                            ),
                        )
                ratio.SetMarkerStyle(20)
                ratio.SetMarkerColor(ROOT.kBlack)
                ratio.SetLineColor(ROOT.kBlack)

                c.cd(2)
                setStyle(ratio, isRatio=True)

                ratio.Draw("E1 P")
                ratioError = makeRatioMCplot(histosum[hn])
                ratioError.Draw("same E2")

                ratio.SetAxisRange(-0.5, 0.5, "Y")
                ratio.GetYaxis().SetNdivisions(5)
                ratiosy = []
                for j, sy in enumerate(systematicsSetToUse):
                    ratiosy.append(histosumSyst[hn][sy].Clone())
                    ratiosy[-1].Add(histosum[hn], -1.0)
                    ratiosy[-1].Divide(histosum[hn])
                    ratiosy[-1].SetLineColor(1 + j)
                    # ratiosy[-1].SetLineStyle(j)
                    ratiosy[-1].SetFillStyle(0)
                    myLegend_sy.AddEntry(ratiosy[-1], sy, "LE")
                    ratiosy[-1].Draw("same hist")
                    # print "Heu",hn,sy,histosumSyst[hn][sy].Integral(),histosum[hn].Integral(),lumitot,ratiosy[-1]
                c.cd()
                # myLegend_sy.Draw()

                tchi2 = makeText(
                    0.25,
                    0.26,
                    "#chi^{2}="
                    + str(round(datasum[hn].Chi2Test(histosum[hn], "UWCHI2/NDF"), 2)),
                    42,
                    0.025,
                )
                tKS = makeText(
                    0.35,
                    0.26,
                    "KS=" + str(round(datasum[hn].KolmogorovTest(histosum[hn]), 2)),
                    42,
                    0.025,
                )
                tchi2.Draw()
                tKS.Draw()

            c.GetPad(2).SetGridy()
            if i == 0:
                if postfit:
                    c.SaveAs(outpath + "/%s_postFit.png" % hn)
                else:
                    c.SaveAs(outpath + "/%s.png" % hn)
                    c.SaveAs(outpath + "/%s.root" % hn)
            # c.SaveAs("%s.root"%hn)
            else:
                c.GetPad(1).SetLogy(True)
                if postfit:
                    c.SaveAs(outpath + "/%s_log_postFit.png" % hn)
                else:
                    c.SaveAs(outpath + "/%s_log.png" % hn)
                    c.SaveAs(outpath + "/%s_log.root" % hn)
            del c


variablesToFit = []
makeWorkspace = False
systematicsSetToUse = model.systematicsToPlot
if args.variablesToFit != None:
    variablesToFit = args.variablesToFit
    makeWorkspace = True
    systematicsSetToUse = model.systematicsForDC
systematicsSetToUse.sort()
postfit = False
postfit = args.postfit

print("makeWorkspace", makeWorkspace)
print("variablesToFit", variablesToFit)


his = [x for x in histoNames if "__syst__" not in x and "sumWeight" not in x]
print(his[0])
# do once for caching normalizations and to dump integrals
makeplot(variablesToFit[0] if makeWorkspace else his[0], True)

if not makeWorkspace:
    print("Preload")
    for ff in f:
        for h in histoNames:
            f[ff].Get(h)
    print("Preload-done")

if makeWorkspace:
    for hn in variablesToFit[1:]:
        makeplot(hn, True)
    # Merge data in one plot for workspace, if is not already there
    for hn in variablesToFit:
        if not "data" + year in all_histo_all_syst[hn]:
            all_histo_all_syst[hn]["data" + year] = {}
            for group in model.data:
                for d in model.data[group]:
                    for syst in list(all_histo_all_syst[hn][d].keys()):
                        if not syst in all_histo_all_syst[hn]["data" + year]:
                            all_histo_all_syst[hn]["data" + year][
                                syst
                            ] = all_histo_all_syst[hn][d][syst].Clone()
                        else:
                            all_histo_all_syst[hn]["data" + year][syst].Add(
                                all_histo_all_syst[hn][d][syst]
                            )
    #    print("DEBUG", model, all_histo_all_syst, year)
    import WorkSpace

    WorkSpace.createWorkSpace(model, all_histo_all_syst, year, outdir)
else:
    from multiprocessing import Pool

    runpool = Pool(20)
    # toproc=[(x,y,i) for y in sams for i,x in enumerate(samples[y]["files"])]
    runpool.map(makeplot, his[1:])


tot = 0
for s in totevCount:
    tot += totevSkim[s]

print(tot, "input events")
