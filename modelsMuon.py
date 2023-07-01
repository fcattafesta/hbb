from samples import *
from collections import defaultdict

from btagging_sys import btag_sys

name = "HBB_mm"


VV_background_list = [
    "WWTo2L2Nu",
    "WZTo2Q2L",
    "WZTo3LNu",
    "ZZTo2L2Nu",
    "ZZTo2Q2L",
    "ZZTo4L",
]

background = defaultdict(list)
for fs, flavours in flavourVVSplitting.items():
    for flav in flavours:
        background[f"VV{fs}"] += [f"{bkg}_{flav}" for bkg in VV_background_list]

# TODO: add the inclusive DY sample
background.update(
    {
        f"Z+{flavour}": [
            f"DYZpt-0To50_{flavour}",
            f"DYZpt-50To100_{flavour}",
            f"DYZpt-100To250_{flavour}",
            f"DYZpt-250To400_{flavour}",
            f"DYZpt-400To650_{flavour}",
            f"DYZpt-650ToInf_{flavour}",
        ]
        for flavour in flavourSplitting.keys()
    }
)

background.update(
    {
        "ST": [
            "ST_tW_antitop_5f_NFHD",
            "ST_tW_top_5f_NFHD",
            "ST_tW_antitop_5f_ID",
            "ST_tW_top_5f_ID",
            "ST_t-channel_antitop_4f_ID",
            "ST_t-channel_top_4f_ID",
            "ST_t-channel_antitop_5f_ID",
            "ST_s-channel_4f_LD",
        ],
        "TT": ["TTTo2L2Nu", "TTToHadronic", "TTToSemiLeptonic"],
    }
)
data = {"2018": ["SingleMuon_2018"]}


signal = {
    "ZH": ["ZH"],
    "ggZH": ["ggZH"],
}

import ROOT

# Color palette

fillcolor = {
    f"Z+{flavour}": ROOT.kGreen + i
    for i, flavour in zip([3, -2, -6, -9], flavourSplitting)
}
fillcolor.update(
    {
        f"VV{flavour}": ROOT.kOrange + i
        for i, flavour in zip([-1, 0], flavourVVSplitting)
    }
)
fillcolor.update(
    {
        "TT": ROOT.kBlue - 4,
        "ST": ROOT.kBlue + 2,
        "ZH": ROOT.kRed + 2,
        "ggZH": ROOT.kRed - 3,
    }
)
linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
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

systematicsToPlot = btag_sys + ["XSecAndNorm"]
systematicsForDC = systematicsToPlot

from systematicGrouping import *
systematicDetail = systematicGrouping(background, signal,[],"2018")

rescaleSample = {}