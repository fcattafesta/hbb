from samples import *
from plot_common_style import *

name = "TestTT"

background = {
    "TT": ["TTToHadronic"],
}


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
) = plot_common_style(signal, background)

rescaleSample = {}
