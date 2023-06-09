from samples import *

name = "DY_overlay"

# TODO: add the inclusive DY sample
background = {
    f"Z+{flavour}": [
        f"DYZpt-50To100_{flavour}",
    ]
    for flavour in flavourSplitting.keys()
}

data = {}

signal = {}

import ROOT

# Color palette

fillcolor = {f"Z+{flavour}": ROOT.kWhite for flavour in flavourSplitting}

linecolor = fillcolor
linecolorNotStacked = {
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

histosNotStacked_list = [f"Z+{flavour}" for flavour in flavourSplitting.keys()]

signalSortedForLegend = []
signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = []
systematicDetail = {}
systematicsForDC = []
