from collections import defaultdict

from samples import *
from plot_common_style import *

name = "VV_overlay"


VV_background_list = [
    "WWTo2L2Nu",
    "WZTo2Q2L",
    "WZTo3LNu",
    "ZZTo2L2Nu",
    "ZZTo2Q2L",
    "ZZTo4L",
]

background = defaultdict(list)
for split, flavours in flavourVVSplitting.items():
    for flav in flavours:
        background[f"VV{split}"] += [f"{bkg}_{flav}" for bkg in VV_background_list]


data = {}


signal = {}

(
    fillcolor,
    linecolor,
    linecolorOverlaid,
    markercolor,
    backgroundSortedForLegend,
    backgroundSorted,
    histosOverlaid_list,
    signalSortedForLegend,
    signalSorted,
    systematicsToPlot,
    systematicsForDC,
    systematicDetail,
) = plot_common_style(signal, background, overlay=True)


rescaleSample = {}
