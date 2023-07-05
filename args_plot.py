import argparse

parser_p = argparse.ArgumentParser()

# Plot
parser_p.add_argument("-m", "--model", help="Model to plot", type=str)
parser_p.add_argument("-p", "--postfit", help="plot postfit plot", action="store_true")
parser_p.add_argument("-v", "--variablesToFit", nargs="*")
parser_p.add_argument(
    "-f", "--histfolder", default="out/", help="Histograms folder for plots"
)
parser_p.add_argument("-o", "--outfolder", default="figures/", help="Plot output folder")
parser_p.add_argument(
    "-w", "--workspace", default="workspace/", help="Workspace output folder"
)
parser_p.add_argument(
    "-fsub", "--foldersuffix", default="", help="Folder suffix for annotations"
)
parser_p.add_argument("--blind", help="Blind data in plots", action="store_true")
parser_p.add_argument("--sf", default=False, help="Scale Factor", action="store_true")
parser_p.add_argument(
    "-b", "--btag", default="deepflav", help="Btagging algorithm (deepflav or deepcsv)"
)

parser_p.print_help()
args_p = parser_p.parse_args()
print(args_p)
