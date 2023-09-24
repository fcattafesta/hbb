import argparse

parser = argparse.ArgumentParser()

# Plot
parser.add_argument("-m", "--model", help="Model to plot", type=str)
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
    "-suf", "--foldersuffix", default="", help="Folder suffix for annotations"
)
parser.add_argument("--unblind", help="Unblind data in plots", action="store_true", default=False)
parser.add_argument("--sf", default=False, help="Scale Factor", action="store_true")
parser.add_argument("--bit", default=False, help="Btag bit", action="store_true")
parser.add_argument(
    "-b", "--btag", default="deepflav", help="Btagging algorithm (deepflav or deepcsv)"
)
parser.add_argument(
    "-s", "--sys", default=False, help="Show systematics", action="store_true"
)

parser.print_help()
args = parser.parse_args()
print(args)
