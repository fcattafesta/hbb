from samples import *

name = "DY_test"

background = {
    "DYZpt": [
        "DYZpt-0To50",
        "DYZpt-50To100",
        "DYZpt-100To250",
        "DYZpt-250To400",
        "DYZpt-400To650",
        "DYZpt-650ToInf",
    ],
    "DYHT": [
        "DYHT-70to100",
        "DYHT-100to200",
        "DYHT-200to400",
        "DYHT-400to600",
        "DYHT-600to800",
        "DYHT-800to1200",
        "DYHT-1200to2500",
        "DYHT-2500toInf",
    ],
}
# DY_background=['DYZpt-0To50', 'DYZpt-50To100', 'DYZpt-100To250', 'DYZpt-250To400', 'DYZpt-400To650', 'DYZpt-650ToInf' ]
# background={x: [x] for x in DY_background}

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

background=    {
        "VV": [
       #     "WWTo2L2Nu",
       #     "WZTo2Q2L",
#	    "WZTo3LNu",
#	    "ZZTo2L2Nu",
	    "ZZTo2Q2L",
#	    "ZZTo4L"
	]}


data = {}

signal = {"ZHJet": ["ZZTo2Q2L"]}

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
