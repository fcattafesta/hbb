import os
import argparse

parser = argparse.ArgumentParser()

# Plot
parser.add_argument("-d", "--dir", help="Directory", type=str, default="workspace")
args = parser.parse_args()

workdir = f"{args.dir}/workspace/"

datacard = os.path.splitext(
    [f for f in os.listdir(workdir) if f.startswith("datacard")][0]
)[0]

name = datacard.split("2018")[1]

os.system(f"text2workspace.py {workdir}{datacard}.txt -m 125")

os.system(
    f"combineTool.py -M Impacts -d {workdir}{datacard}.root -m 125 --doInitialFit --robustFit 1 -t -1"
)
os.system(
    f"combineTool.py -M Impacts -d {workdir}{datacard}.root -m 125 --robustFit 1 --doFits --parallel 30 -t -1"
)
os.system(
    f"combineTool.py -M Impacts -d {workdir}{datacard}.root -m 125 -o {workdir}impacts_{name}.json -t -1"
)
os.system(f"plotImpacts.py -i {workdir}impacts_{name}.json -o {workdir}impacts_{name}")

#os.system(f"mv impacts_{name}.* {workdir}/")


os.system(f"combine -M Significance {workdir}{datacard}.txt -t -1 --expectSignal=1")
