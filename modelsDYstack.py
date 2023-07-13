from samples import *

name = "DY_stack"

# TODO: add the inclusive DY sample
background = {
    f"Z+{flavour}": [
        f"DYZpt-0To50_{flavour}",
        f"DYZpt-50To100_{flavour}",
        f"DYZpt-100To250_{flavour}",
        f"DYZpt-250To400_{flavour}",
        f"DYZpt-400To650_{flavour}",
        f"DYZpt-650ToInf_{flavour}",
    ]
    for flavour in flavourSplitting.keys()
}

data = {}

signal = {}

import ROOT

# Color palette

fillcolor = {
    f"Z+{flavour}": ROOT.kGreen + i
    for i, flavour in zip([3, -2, -6, -9], flavourSplitting)
}

linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
linecolorNotStacked = {}
markercolor = fillcolor


# legend sorting
backgroundSortedForLegend = []
backgroundSortedForLegend += [
    x for x in background if x not in backgroundSortedForLegend
]
backgroundSorted = backgroundSortedForLegend

histosNotStacked_list = []

signalSortedForLegend = []
signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = []
systematicDetail = {}
systematicsForDC = []
