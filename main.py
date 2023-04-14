import os 
import njets

root = "/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/"
sample = "DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8"
aod = "/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/"

path = root + sample + aod

files = [
    os.path.join(d, f)
    for d in os.listdir(path)
    for f in os.listdir(os.path.join(path, d))
]

files_paths = [os.path.join(path, f) for f in files]

print(files_paths[0])

njets.njet(path=files_paths[0], njets=0, var="LHE_NpNLO", outpath="DY_0J_LHE_NpNLO.png")
