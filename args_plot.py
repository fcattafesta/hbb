import argparse

parser = argparse.ArgumentParser()

# Plot
parser.add_argument("model", help="Model to plot")
parser.add_argument("-p", "--postfit", help="plot postfit plot", action="store_true")
parser.add_argument("-v", "--variablesToFit", nargs="*")
parser.add_argument(
    "-f", "--histfolder", default="out/", help="Histograms folder for plots"
)
parser.add_argument("-o", "--outfolder", default="figures/", help="Plot output folder")
parser.add_argument(
    "-w", "--workspace", default="workspace/", help="Workspace output folder"
)
parser.add_argument(
    "-fsub", "--foldersuffix", default="", help="Folder suffix for annotations"
)
parser.add_argument("--blind", help="Blind data in plots", action="store_true")
parser.add_argument(
    "-b", "--btag", default="deepflav", help="Btagging algorithm (deepflav or deepcsv)"
)

parser.print_help()
args = parser.parse_args()
print(args)
