from hbb_samples import *

name="DY_test"

background={'DY':['DYZpt-0To50', 'DYZpt-50To100', 'DYZpt-100To250', 'DYZpt-250To400', 'DYZpt-400To650' ]}

data={}

signal={"DY_":['DYZpt-650ToInf']
}

import ROOT
fillcolor={
"DY": ROOT.kBlue,
'DY_': ROOT.kBlue,
}
linecolor=fillcolor
markercolor=fillcolor


#legend sorting
backgroundSortedForLegend=[]
backgroundSortedForLegend+=[x for x in background if x not in backgroundSortedForLegend]
backgroundSorted=backgroundSortedForLegend
signalSortedForLegend=[]
signalSorted=signalSortedForLegend

from rebinning import *
systematicsToPlot=[]
systematicDetail={}
systematicsForDC=[]