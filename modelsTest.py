from samples import *

from btagging_sys import btag_sys

name = "Test"

background = {
    # f"Z+bb": [
    #     f"DYZpt-0To50_bb",
    # ]
}
signal = {"Hbb": ["ZH"]}

data = {}


import ROOT

# Color palette

fillcolor = {f"Z+{flavour}": ROOT.kGreen for flavour in flavourSplitting}
fillcolor.update(
    {
        "Hbb": ROOT.kRed,
    }
)
linecolor = fillcolor
linecolorOverlayed = {
    f"Z+{flavour}": ROOT.kGreen + i
    for i, flavour in zip([3, -2, -6, -9], flavourSplitting)
}
markercolor = fillcolor


# legend sorting
backgroundSortedForLegend = []
backgroundSortedForLegend += [
    x for x in background if x not in backgroundSortedForLegend
]
backgroundSorted = backgroundSortedForLegend

histosOverlayed_list = []#f"Z+bb"]

signalSortedForLegend = []
signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = btag_sys
systematicsToPlot += ["XSecAndNorm"]

from systematicGrouping import *
systematicDetail = systematicGrouping(background, signal,[],"2018")

systematicsForDC = []

rescaleSample = {}
