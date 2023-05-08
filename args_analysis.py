import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f", "--histfolder", default="out/", help="Histograms folder for plots"
)
parser.add_argument(
    "-m", "--model", default="", help="Model to use"
)
parser.add_argument(
    "-r", "--range", default=-1, help="Number of events to process", type=int,
)
parser.print_help()
args = parser.parse_args()
