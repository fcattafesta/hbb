from samples import *

name = "Test"

# TODO: add the inclusive DY sample
background = {
    f"Z+bb": [
        f"DYZpt-50To100_bb",
    ]
}

data = {}

signal = {}

import ROOT

# Color palette

fillcolor = {f"Z+{flavour}": ROOT.kWhite for flavour in flavourSplitting}

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

histosOverlayed_list = [f"Z+bb"]

signalSortedForLegend = []
signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = []
systematicDetail = {}
systematicsForDC = []

rescale_sample = {}
