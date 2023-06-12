from samplesDY import *

name = "HBB"

# background = {
#     f"Z+{flavour}": [
#         f"DYM50_{flavour}",
#     ]
#     for flavour in flavourSplitting.keys()
# }

background = {
    "FlashSim": [
        "DYM50",
    ],
    "FullSim": [
        "DYM50_full",
    ],
}

# background.update(
#     {
#         f"VV{flavour}": [
#             f"WWTo2L2Nu_{flavour}",
#             f"WZTo2Q2L_{flavour}",
#             f"WZTo3LNu_{flavour}",
#             f"ZZTo2L2Nu_{flavour}",
#             f"ZZTo2Q2L_{flavour}",
#             f"ZZTo4L_{flavour}",
#         ]
#         for flavour in flavourVVSplitting.keys()
#     }
# )

# background.update(
#     {
#         "ST": [
#             "ST_tW_antitop_5f_NFHD",
#             "ST_tW_top_5f_NFHD",
#             "ST_tW_antitop_5f_ID",
#             "ST_tW_top_5f_ID",
#             "ST_t-channel_antitop_4f_ID",
#             "ST_t-channel_top_4f_ID",
#             "ST_t-channel_antitop_5f_ID",
#             "ST_s-channel_4f_LD",
#         ],
#         "TT": ["TTTo2L2Nu", "TTToHadronic", "TTToSemiLeptonic"],
#     }
# )

# To be added

data = {
    # "2018": ["EGamma_2018"],
}


signal = {
    # "ZH": ["ZH"],
    # "ggZH": ["ggZH"],
}

import ROOT

# Color palette

fillcolor = {key: ROOT.kWhite for key in background.keys()}
linecolor = fillcolor  # {key: ROOT.kBlack for key in fillcolor.keys()}
markercolor = fillcolor

histosOverlayed_list = ["FullSim", "FlashSim"]
linecolorOverlayed = {"FullSim": ROOT.kBlack, "FlashSim": ROOT.kOrange}
linestyleOverlayed = {"FullSim": 2, "FlashSim": 1}

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
