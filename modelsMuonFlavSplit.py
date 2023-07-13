import numpy as np
from samples import *
from collections import defaultdict

from btagging_sys import btag_sys

name = "HBB_mm_flavSplit"


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
        background[f"bkg_{num_b}"] += [f"{bkg}_{flav}" for bkg in background_list]

data = {
    "2018": ["SingleMuon_2018"],
}


signal = {
    "ZH": ["ZH"],
    "ggZH": ["ggZH"],
}

import ROOT

# Color palette

fillcolor = {bkg: ROOT.kAzure + i for bkg, i in zip(background, [7, 0, 3])}
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

systematicsToPlot = btag_sys
systematicsToPlot += ["lumi", "BR_Hbb", "XSecAndNorm", "JERDown", "JERUp"]
systematicsForDC = systematicsToPlot

from systematicGrouping import *
systematicDetail = systematicGrouping(background, signal,[],"2018")


rescaleArray = np.linspace(1.0, 1.4, 10)
rescaleSample = {
    "bkg_0b": [1.0, np.ones(10)],
    "bkg_1b": [1.16, rescaleArray],
    "bkg_2b": [1.16**2, rescaleArray**2],
    "ZH": [1.16**2, rescaleArray**2],
    "ggZH": [1.16**2, rescaleArray**2],
}
