from samples import *
from plot_common_style import *


name = "OS"

background = {
    "DYZpt-100To250": [
        "DYZpt-100To250-0",
        "DYZpt-100To250-1",
        "DYZpt-100To250-2",
        "DYZpt-100To250-3",
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

(
    fillcolor,
    linecolor,
    linecolorOverlayed,
    linestyleOverlayed,
    markercolor,
    backgroundSortedForLegend,
    backgroundSorted,
    histosOverlayed_list,
    signalSortedForLegend,
    signalSorted,
    systematicsToPlot,
    systematicsForDC,
    systematicDetail,
) = plot_common_style(signal, background)

fillcolor = {"DYZpt-100To250": ROOT.KOrange + 8}
