from samples import *

name = "VV"

background = {
    f"VV{flavour}": [
        f"WWTo2L2Nu_{flavour}",
        f"WZTo2Q2L_{flavour}",
        f"WZTo3LNu_{flavour}",
        f"ZZTo2L2Nu_{flavour}",
        f"ZZTo2Q2L_{flavour}",
        f"ZZTo4L_{flavour}",
    ]
    for flavour in flavourVVSplitting.keys()
}

data = {}


signal = {}

import ROOT

# Color palette

fillcolor = {f"VV{flavour}": ROOT.kWhite for flavour in flavourVVSplitting}

linecolor = fillcolor
linecolorNotStacked = {
    f"VV{flavour}": ROOT.kOrange + i for i, flavour in zip([0, -1], flavourVVSplitting)
}
markercolor = fillcolor


# legend sorting
backgroundSortedForLegend = []
backgroundSortedForLegend += [
    x for x in background if x not in backgroundSortedForLegend
]
backgroundSorted = backgroundSortedForLegend

histosNotStacked_list = [f"VV{flavour}" for flavour in flavourVVSplitting.keys()]

signalSortedForLegend = []
signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = []
systematicDetail = {}
systematicsForDC = []
