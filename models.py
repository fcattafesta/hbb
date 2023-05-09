from samples import *

name = "HBB"

# Drell-Yan

background = {
    "DYZpt": [
        "DYZpt-0To50",
        "DYZpt-50To100",
        "DYZpt-100To250",
        "DYZpt-250To400",
        "DYZpt-400To650",
        "DYZpt-650ToInf",
    ]
}

# TOP

background.update(
    {
        "TOP": [
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
    }
)

# Diboson

background.update(
    {"VV": ["WWTo2L2Nu", "WZTo2Q2L", "WZTo3LNu", "ZZTo2L2Nu", "ZZTo2Q2L", "ZZTo4L"]}
)

# To be added

data = {
    # "SingleMuon": ["SingleMuon"],
}


signal = {
    "ZH": ["ZH"],
    "ggZH": ["ggZH"],
}

import ROOT

# Color palette

fillcolor = {
    "DY": ROOT.kBlue,
    "TOP": ROOT.kRed,
    "VV": ROOT.kGreen,
    "ZH": ROOT.kOrange,
    "ggZH": ROOT.kOrange - 3,
}
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
