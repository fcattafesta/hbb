from samplesDY import *

name = "FlashFullDY"

background = {
    "FlashSim": [
        "DYZpt-0To50",
        "DYZpt-50To100",
        "DYZpt-100To250",
        "DYZpt-250To400",
        "DYZpt-400To650",
        "DYZpt-650ToInf",
    ],
    "FullSim": [
        "DYZpt-0To50Full",
        "DYZpt-50To100Full",
        "DYZpt-100To250Full",
        "DYZpt-250To400Full",
        "DYZpt-400To650Full",
        "DYZpt-650ToInfFull",
    ],
}


data = {}


signal = {}

import ROOT

# Color palette

fillcolor = {key: ROOT.kWhite for key in background.keys()}
linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
markercolor = fillcolor

histosOverlayed_list = ["FullSim", "FlashSim"]
linecolorOverlayed = {"FullSim": ROOT.kBlack, "FlashSim": ROOT.kOrange + 8}
linestyleOverlayed = {"FullSim": 2, "FlashSim": 1}

# legend sorting
backgroundSortedForLegend = []
backgroundSortedForLegend += [
    x for x in background if x not in backgroundSortedForLegend
]
backgroundSorted = backgroundSortedForLegend

signalSortedForLegend = []
signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = []
systematicDetail = {}
systematicsForDC = []
