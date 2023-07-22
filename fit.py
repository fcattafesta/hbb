import os
import argparse

parser = argparse.ArgumentParser()

# Plot
parser.add_argument("-d", "--dir", help="Directory", type=str)
args = parser.parse_args()

workdir = f"{args.dir}/workspace/"

datacard = os.path.splitext(
    [f for f in os.listdir(workdir) if f.startswith("datacard")][0]
)[0]

name = datacard.split("2018")[1]

os.system(f"text2workspace.py {datacard}.txt -m 125")

os.system(
    f"combineTool.py -M Impacts -d {datacard}.root -m 125 --doInitialFit --robustFit 1 -t -1"
)
os.system(
    f"combineTool.py -M Impacts -d {datacard}.root -m 125 --robustFit 1 --doFits --parallel 30 -t -1"
)
os.system(f"combineTool.py -M Impacts -d {datacard}.root -m 125 -o impacts_{name}.json -t -1")
os.system(f"plotImpacts.py -i impacts_{name}.json -o impacts_{name}")

os.system(f"mv impacts_{name}.* {workdir}/")


os.system(f"combine -M Significance {datacard}.txt -t -1 --expectSignal=1")