from samples import *
from plot_common_style import *

name = "OSSingleEvent"


background = {
    "Oversampling": ["DYZpt-100To250-0b"],
    "FlashSim": ["DYZpt-100To250-1b"],
}

data = {}

signal = {}

fillcolor = {key: ROOT.kWhite for key in background.keys()}
linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
markercolor = fillcolor

histosOverlayed_list = ["Oversampling", "FlashSim"]
linecolorOverlayed = {"Oversampling": ROOT.kAzure + 1, "FlashSim": ROOT.kOrange + 8}
linestyleOverlayed = {"Oversampling": 1, "FlashSim": 1}

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
