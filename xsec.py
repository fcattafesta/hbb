import ROOT
import argparse
import glob

filters=[
    'LHE_Vpt > 0 && LHE_Vpt < 50',
    'LHE_Vpt > 50 && LHE_Vpt < 100',
    'LHE_Vpt > 100 && LHE_Vpt < 250',
    'LHE_Vpt > 250 && LHE_Vpt < 400',
    'LHE_Vpt > 400 && LHE_Vpt < 650',
    'LHE_Vpt > 650 ',
    'LHE_HT > 70 && LHE_HT < 100',
    'LHE_HT > 100 && LHE_HT < 200',
    'LHE_HT > 200 && LHE_HT < 400',
    'LHE_HT > 400 && LHE_HT < 600',
    'LHE_HT > 600 && LHE_HT < 800',
    'LHE_HT > 800 && LHE_HT < 1200',
    'LHE_HT > 1200 && LHE_HT < 2500',
    'LHE_HT > 2500',
]

xsec_tot=5765.4

ROOT.ROOT.EnableImplicitMT(200)
thread_size = ROOT.ROOT.GetThreadPoolSize()
print(">>> Thread pool size for parallel processing: %s", thread_size)

#files=[x for x in glob.glob('/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/**/*.root', recursive=True)]
files= "../1574B1FB-8C40-A24E-B059-59A80F397A0F.root"
rdf = ROOT.RDataFrame("Events", files)

rdf=rdf.Define("weight", "TMath::Sign(1, genWeight)")
num_tot=rdf.Histo1D("LHE_Vpt").GetSumOfWeights()
print("num_tot",  " = ", num_tot)
num_tot_w=rdf.Sum("weight").GetValue() #rdf.Histo1D("LHE_Vpt", "weight").GetSumOfWeights()
print("tot_weight",  " = ", num_tot_w, "\n")

print(rdf.Sum("weight").GetValue())

for filter in filters:
    rdf_cut=rdf.Filter(filter)
    num_cut=rdf_cut.Histo1D("LHE_Vpt").GetSumOfWeights()
    print("num_cut ", filter,  " = ", num_cut)
    num_cut_w=rdf_cut.Sum("weight").GetValue()# rdf_cut.Histo1D("LHE_Vpt", "weight").GetSumOfWeights()
    print("cut_weight ", filter, " = ", num_cut_w)
    print("xsec %s = %.2f \n" %(filter,  num_cut_w/num_tot_w*xsec_tot))


# 1063268.0