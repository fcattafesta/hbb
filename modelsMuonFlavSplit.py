from samples import *
from collections import defaultdict

name = "HBB_mm_flavSplit"

number_of_b = {
    2: ["bb"],
    1: ["b"],
    0: ["udsg", "c"],
}

# TODO: add the inclusive DY sample
background_list = [
    "WWTo2L2Nu",
    "WZTo2Q2L",
    "WZTo3LNu",
    "ZZTo2L2Nu",
    "ZZTo2Q2L",
    "ZZTo4L",
    "DYZpt-0To50",
    "DYZpt-50To100",
    "DYZpt-100To250",
    "DYZpt-250To400",
    "DYZpt-400To650",
    "DYZpt-650ToInf",
    "ST_tW_antitop_5f_NFHD",
    "ST_tW_top_5f_NFHD",
    "ST_tW_antitop_5f_ID",
    "ST_tW_top_5f_ID",
    "ST_t-channel_antitop_4f_ID",
    "ST_t-channel_top_4f_ID",
    "ST_t-channel_antitop_5f_ID",
    "ST_s-channel_4f_LD",
    "TTTo2L2Nu",
    "TTToHadronic",
    "TTToSemiLeptonic",
]

# divide all backgrounds into b, bb, c+udsg
background = defaultdict(list)
for num_b, flavours in number_of_b.items():
    for flav in flavours:
        background[f"bkg_{num_b}b"] += [f"{bkg}_{flav}" for bkg in background_list]

data = {
    "2018": ["SingleMuon_2018"],
}


signal = {
    "ZH": ["ZH"],
    "ggZH": ["ggZH"],
}

import ROOT

# Color palette

fillcolor = {bkg: ROOT.kAzure + i for bkg, i in zip(background, [3, 0, 7])}
fillcolor.update(
    {
        "ZH": ROOT.kRed + 2,
        "ggZH": ROOT.kRed - 3,
    }
)
linecolor = fillcolor
linecolorOverlayed = {}
markercolor = fillcolor


# legend sorting
backgroundSortedForLegend = []
backgroundSortedForLegend += [
    x for x in background if x not in backgroundSortedForLegend
]
backgroundSorted = backgroundSortedForLegend

histosOverlayed_list = []

signalSortedForLegend = []
signalSortedForLegend = [z for z in signal if z not in signalSortedForLegend]
signalSorted = signalSortedForLegend

from rebinning import *

systematicsToPlot = []
systematicDetail = {}
systematicsForDC = []
