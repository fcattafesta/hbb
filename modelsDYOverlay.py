from samples import *
from plot_common_style import *

name = "DY_overlay"

# TODO: add the inclusive DY sample
background = {
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
