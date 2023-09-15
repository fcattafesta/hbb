from samples import *
from plot_common_style import *


name = "OS"

background = {
    "DYZpt-100To250": ["DYZpt-100To250"],
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
