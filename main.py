import os
import njets
import zpt
import mass

root = "/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9"
sample = "/DYBJetsToLL_M-50_Zpt-100to200_TuneCP5_13TeV-madgraphMLM-pythia8"
aod = "/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/"

path = root + sample + aod

files = [
    os.path.join(d, f)
    for d in os.listdir(path)
    for f in os.listdir(os.path.join(path, d))
]

files_paths = [os.path.join(path, f) for f in files]

print(files_paths[0])

# njets.njet(path=files_paths[0], njets=2, var="LHE_NpNLO", outpath="DY_2J_LHE_NpNLO.png")

zpt.zpt(path=files_paths[0], zpt=200, outpath="DYB_Zpt_200.png")

# mass.mass(path=files_paths[0], outpath="DY_M-50_incl.png")
