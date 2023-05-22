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
parser.add_argument(
    "-n", "--nthreads", default=50, help="Number of threads", type=int,
)
parser.add_argument(
    "-l", "--lep", default="mu", help="Lepton channel"
)
parser.add_argument(
    "-s", "--snapshot", default=False, action="store_true", help="Save snapshot"
)
# TODO: add option to evaluate model
parser.add_argument(
    "-e", "--eval-model", default=False, action="store_true", help="Evaluate model"
)
parser.print_help()
args = parser.parse_args()
