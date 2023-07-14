from samplesDY import *

name = "MCUncertDY"

background = {
    "DY0To50": ["DYZpt-0To50Full"],
    "DY50To100": ["DYZpt-50To100Full"],
    "DY100To250": ["DYZpt-100To250Full"],
    "DY250To400": ["DYZpt-250To400Full"],
    "DY400To650": ["DYZpt-400To650Full"],
    "DY650ToInf": ["DYZpt-650ToInfFull"],
}


data = {}


signal = {}

import ROOT

# Color palette

fillcolor = {key: ROOT.kWhite for key in background.keys()}
linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
markercolor = fillcolor

histosOverlayed_list = [
    "DY0To50",
    "DY50To100",
    "DY100To250",
    "DY250To400",
    "DY400To650",
    "DY650ToInf",
]
linecolorOverlayed = {
    key: color
    for key, color in zip(
        background.keys(),
        [ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta, ROOT.kCyan],
    )
}
linestyleOverlayed = {}

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
rescaleSample = {}
