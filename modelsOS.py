from samples import *
from plot_common_style import *


name = "OS"

background = {
    "DYZpt-100To250": [
        # "DYZpt-100To250-0",
        # "DYZpt-100To250-1",
        # "DYZpt-100To250-2",
        # "DYZpt-100To250-3",
        "DYZpt-100To250-4",
        "DYZpt-100To250-5",
        "DYZpt-100To250-6",
        "DYZpt-100To250-7",
        "DYZpt-100To250-8",
        "DYZpt-100To250-9",
    ],
}

data = {}

signal = {}

fillcolor = {"DYZpt-100To250": ROOT.kAzure + 1}
linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
markercolor = fillcolor

histosOverlayed_list = []
linecolorOverlayed = {}
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
