from samples import *
from collections import defaultdict

from btagging_sys import btag_sys

name = "TestZH"

background = {
    "ZH": ["ZH"],
}


data = {}


signal = {}

import ROOT

# Color palette

fillcolor = {
    f"Z+{flavour}": ROOT.kGreen + i
    for i, flavour in zip([3, -2, -6, -9], flavourSplitting)
}
fillcolor.update(
    {
        f"VV{flavour}": ROOT.kOrange + i
        for i, flavour in zip([-1, 0], flavourVVSplitting)
    }
)
fillcolor.update(
    {
        "TT": ROOT.kBlue - 4,
        "ST": ROOT.kBlue + 2,
        "ZH": ROOT.kRed + 2,
        "ggZH": ROOT.kRed - 3,
    }
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

from rebinning import *

systematicsToPlot = btag_sys
systematicsToPlot += ["lumi", "BR_Hbb", "XSecAndNorm", "JERDown", "JERUp"]
systematicsForDC = systematicsToPlot

from systematicGrouping import *

systematicDetail = systematicGrouping(background, signal, [], "2018")

rescaleSample = {}
