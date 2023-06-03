from samples import *
from collections import defaultdict

name = "VV"


flavourVVSplitting = {
    "HF": ["bb", "b", "c"],
    "LF": ["udsg"],
}

VV_background_list = [
    "WWTo2L2Nu",
    "WZTo2Q2L",
    "WZTo3LNu",
    "ZZTo2L2Nu",
    "ZZTo2Q2L",
    "ZZTo4L",
]

background = defaultdict(list)
for name, flavours in flavourVVSplitting.items():
    for flav in flavours:
        background[f"VV{name}"] += [f"{bkg}_{flav}" for bkg in VV_background_list]


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
