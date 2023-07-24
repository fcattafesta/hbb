import os
import argparse
import subprocess

parser = argparse.ArgumentParser()

# Plot
parser.add_argument("-d", "--dir", help="Directory", type=str, default=".")
args = parser.parse_args()

workdir = args.dir + "/"

datacard = os.path.splitext(
    [f for f in os.listdir(workdir) if f.startswith("datacard")][0]
)[0]

name = datacard.split("2018")[1] if "2018" in datacard else datacard

# Define the file name for the output log
log_file = 'output.log'
# If the file already exists, delete it
if os.path.exists(log_file):
    os.remove(log_file)

cmd_list = [
    f"combine -M Significance {workdir}{datacard}.txt -t -1 --expectSignal=1",
    f"text2workspace.py {workdir}{datacard}.txt -m 125",
    f"combineTool.py -M Impacts -d {workdir}{datacard}.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal=1",
    f"combineTool.py -M Impacts -d {workdir}{datacard}.root -m 125 --robustFit 1 --doFits --parallel 30 -t -1 --expectSignal=1",
    f"combineTool.py -M Impacts -d {workdir}{datacard}.root -m 125 -o {workdir}impacts_{name}.json -t -1 --expectSignal=1",
    f"plotImpacts.py -i {workdir}impacts_{name}.json -o {workdir}impacts_{name}",
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
