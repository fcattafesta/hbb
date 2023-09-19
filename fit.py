import os
import argparse
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--datacard", help="Datacard name", type=str, default="datacard.txt")
parser.add_argument("-c", "--combine", help="Combine datacards", action="store_true", default=False)
parser.add_argument("-u", "--unblind", help="Unlind analysis", action="store_true", default=False)
parser.add_argument("-t", "--threads", help="Number of threads", type=int, default=30)
parser.add_argument("-r", "--rename", help="Rename POI file", type=str, default="../../rename_fit.json")
args = parser.parse_args()

if args.combine:
    datacards = ""
    # find the datacard file recursevely
    for root, dirs, files in os.walk("."):
        for file in files:
            if "datacard" in file and ".txt" in file:
                datacards+=os.path.join(root, file) + " "

    print("Found datacards: ", datacards)
    print("Combining datacards...")
    subprocess.run(f"combineCards.py {datacards} > {args.datacard}", shell=True)

workdir = os.path.dirname(args.datacard)
workdir = workdir + "/" if workdir else ""

if args.unblind:
    asimov=""
else:
    asimov="-t -1"

datacard = os.path.splitext(args.datacard)[0]

print("workdir: ", workdir)
print("datacard: ", datacard)

name = os.path.basename(datacard.replace("datacard_", "").replace("datacard", ""))

# Define the file name for the output log
log_file = 'output.log'
# If the file already exists, delete it
if os.path.exists(log_file):
    os.remove(log_file)

cmd_list = [
    f"combine -M Significance {datacard}.txt {asimov} --expectSignal=1",
    f"text2workspace.py {datacard}.txt -m 125",
    f"combineTool.py -M Impacts -d {datacard}.root -m 125 --doInitialFit --robustFit 1 {asimov} --expectSignal=1",
    f"combineTool.py -M Impacts -d {datacard}.root -m 125 --robustFit 1 --doFits --parallel {args.threads} {asimov} --expectSignal=1",
    f"combineTool.py -M Impacts -d {datacard}.root -m 125 -o {workdir}impacts_{name}.json {asimov} --expectSignal=1",
    f"plotImpacts.py -i {workdir}impacts_{name}.json -o {workdir}impacts_{name} -t {args.rename} --units 1",
]

# Open the log file for writing
with open(log_file, 'w') as f:
    for cmd in cmd_list:
        # Run the command and capture the output
        output = subprocess.check_output(cmd, shell=True, text=True)
        # Print the output to the console and write it to the log file
        print(output)
        print("\n\n")
        f.write(output)
        f.write('\n\n')


# combineCards.py datacard1.txt datacard2.txt > datacard_combined.txt
