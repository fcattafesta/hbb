from collections import defaultdict

from samples import *
from plot_common_style import *

name = "signal"


background = {
    "Signal": ["ZH", "ggZH"],
}

signal = {}

data = {}

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

rescaleSample = {}
