import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f", "--histfolder", default="out/", help="Histograms folder for plots"
)

parser.print_help()
args = parser.parse_args()
