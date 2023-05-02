from hbb_samples import *

name = 'DY_test'

background = {
    'DY': [
        'DYZpt-0To50',
        'DYZpt-50To100',
        'DYZpt-100To250',
        'DYZpt-250To400',
        'DYZpt-400To650',
    ]
}
# DY_background=['DYZpt-0To50', 'DYZpt-50To100', 'DYZpt-100To250', 'DYZpt-250To400', 'DYZpt-400To650', 'DYZpt-650ToInf' ]
# background={x: [x] for x in DY_background}
background.update(
    {
        'TOP': [
            'ST_tW_antitop_5f_NoFullyHadronicDecays',
            'ST_tW_top_5f_NoFullyHadronicDecays',
            'ST_tW_antitop_5f_inclusiveDecays',
            'ST_tW_top_5f_inclusiveDecays',
            'ST_t-channel_antitop_4f_InclusiveDecays',
            'ST_t-channel_top_4f_InclusiveDecays',
            'ST_t-channel_antitop_5f_InclusiveDecays',
            'ST_s-channel_4f_leptonDecays',
            'TTTo2L2Nu',
            'TTToHadronic',
            'TTToSemiLeptonic',
        ]
    }
)

background.update(
    {'VV': ['WWTo2L2Nu', 'WZTo2Q2L', 'WZTo3LNu', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'ZZTo4L']}
)

data = {}

signal = {'ZHJet': ['ZHJet']}

import ROOT

fillcolor = {
    'DY': ROOT.kBlue,
    'TOP': ROOT.kRed,
    'VV': ROOT.kGreen,
    'ZHJet': ROOT.kOrange
}
#fillcolor.update({x: ROOT.kBlue + i - 3 for i, x in enumerate(background)})
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
