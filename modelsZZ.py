from samples import *

name = "Z_test"


background = {
    # "VV": [
    #     #     "WWTo2L2Nu",
    #     "WZTo2Q2L",
    #     # 	    "WZTo3LNu",
    #     # 	    "ZZTo2L2Nu",
    #     "ZZTo2Q2L",
    #     # 	    "ZZTo4L"
    # ],
    "DY": ["DYM50"],
}


data = {}

signal = {}

import ROOT

fillcolor = {
    "DY": ROOT.kBlue,
    "TOP": ROOT.kRed,
    "VV": ROOT.kGreen,
    "ZHJet": 0,
}
# fillcolor.update({x: ROOT.kBlue + i - 3 for i, x in enumerate(background)})
linecolor = fillcolor
markercolor = fillcolor


# legend sorting
backgroundSortedForLegend = []
backgroundSortedForLegend += [
    x for x in background if x not in backgroundSortedForLegend
]
backgroundSorted = backgroundSortedForLegend
signalSortedForLegend = []
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = []
systematicDetail = {}
systematicsForDC = []
