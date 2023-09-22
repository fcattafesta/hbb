import ROOT

from samples import *
from btagging_sys import btag_sys
from rebinning import *
from systematicGrouping import *


# Color palette
def plot_common_style(signal, background, overlay=False, bkg_list=None):
    fillcolor = {
        f"Z+{flavour}": ROOT.kGreen + i
        for i, flavour in zip([3, -2, -6, -9], flavourSplitting)
    }
    fillcolor.update(
        {
            f"VV{flavour}": ROOT.kOrange + i
            for i, flavour in zip([-1, 0], flavourVVSplitting)
        },
    )
    fillcolor.update(
        {
            "VV": ROOT.kOrange + 1,
            "TT": ROOT.kBlue - 4,
            "ST": ROOT.kBlue + 2,
            "ZH": ROOT.kRed + 2,
            "ggZH": ROOT.kRed - 3,
        }
    )
    fillcolor.update(
        {f"bkg_{num_b}": ROOT.kAzure + i for i, num_b in zip([7, 0, 3], number_of_b)}
    )
    if bkg_list:
        fillcolor.update(
            {bkg: ROOT.kBlack + i for i, bkg in enumerate(bkg_list)}
        )
    linecolorOverlaid = {}

    if overlay:
        linecolorOverlaid=fillcolor.copy()
        for key in fillcolor.keys():
            fillcolor[key] = ROOT.kWhite


    linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
    markercolor = fillcolor


    # legend sorting
    backgroundSortedForLegend = []
    backgroundSortedForLegend += [
        x for x in background if x not in backgroundSortedForLegend
    ]
    backgroundSorted = backgroundSortedForLegend

    histosOverlaid_list = []
    if overlay:
        histosOverlaid_list=list(signal.keys())+list(background.keys())

    signalSortedForLegend = []
    signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
    signalSorted = signalSortedForLegend

    systematicsToPlot = btag_sys
    systematicsToPlot += ["lumi", "BR_Hbb", "XSecAndNorm", "JERDown", "JERUp"]
    systematicsForDC = systematicsToPlot

    systematicDetail = systematicGrouping(background, signal, [], "2018")

    # return all the variables
    return (
        fillcolor,
        linecolor,
        linecolorOverlaid,
        markercolor,
        backgroundSortedForLegend,
        backgroundSorted,
        histosOverlaid_list,
        signalSortedForLegend,
        signalSorted,
        systematicsToPlot,
        systematicsForDC,
        systematicDetail,
    )
