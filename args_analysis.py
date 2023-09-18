import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f", "--histfolder", default="out/", help="Histograms folder for plots"
)
parser.add_argument("-m", "--model", default="", help="Model to use")
parser.add_argument(
    "-r",
    "--range",
    default=[-1, -1],
    help="Number of events to process",
    type=list,
)
parser.add_argument(
    "-n",
    "--nthreads",
    default=10,
    help="Number of threads",
    type=int,
)
parser.add_argument(
    "-p", "--num_processes", default=4, help="Number of processes", type=int
)  # 27 samples
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")
parser.add_argument(
    "-b", "--btag", default="deepflav", help="Btagging algorithm (deepflav or deepcsv)"
)
parser.add_argument(
    "-s", "--snapshot", default=False, action="store_true", help="Save snapshot"
)
parser.add_argument(
    "-e",
    "--eval-model",
    default="",
    help="Evaluate model",
    type=str,
)
parser.add_argument(
    "--sf",
    default=False,
    action="store_true",
    help="Apply scale factors and systematics",
)
parser.add_argument(
    "--oversampling",
    default=False,
    action="store_true",
    help="Apply oversampling",
)
parser.print_help()
args = parser.parse_args()
print(args)
