import ROOT

from samples import *
from btagging_sys import btag_sys
from rebinning import *
from systematicGrouping import *


# Color palette
def plot_common_style(signal, background):
    fillcolor = {
        f"Z+{flavour}": ROOT.kGreen + i
        for i, flavour in zip([3, -2, -6, -9], flavourSplitting)
    }
    fillcolor.update(
        {
            f"VV{flavour}": ROOT.kOrange + i
            for i, flavour in zip([-1, 0], flavourVVSplitting)
        },
        {
            "VV": ROOT.kOrange + 1,
        },
    )
    fillcolor.update(
        {
            "TT": ROOT.kBlue - 4,
            "ST": ROOT.kBlue + 2,
            "ZH": ROOT.kRed + 2,
            "ggZH": ROOT.kRed - 3,
        }
    )
    fillcolor.update(
        {f"bkg_{num_b}": ROOT.kAzure + i for i, num_b in zip([7, 0, 3], number_of_b)}
    )
    linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
    linecolorOverlayed = {}
    markercolor = fillcolor

    # legend sorting
    backgroundSortedForLegend = []
    backgroundSortedForLegend += [
        x for x in background if x not in backgroundSortedForLegend
    ]
    backgroundSorted = backgroundSortedForLegend

    histosOverlayed_list = []

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
        linecolorOverlayed,
        markercolor,
        backgroundSortedForLegend,
        backgroundSorted,
        histosOverlayed_list,
        signalSortedForLegend,
        signalSorted,
        systematicsToPlot,
        systematicsForDC,
        systematicDetail,
    )
