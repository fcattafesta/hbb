import argparse

parser_a = argparse.ArgumentParser()

parser_a.add_argument(
    "-f", "--histfolder", default="out/", help="Histograms folder for plots"
)
parser_a.add_argument("-m", "--model", default="", help="Model to use")
parser_a.add_argument(
    "-r",
    "--range",
    default=-1,
    help="Number of events to process",
    type=int,
)
parser_a.add_argument(
    "-n",
    "--nthreads",
    default=10,
    help="Number of threads",
    type=int,
)
parser_a.add_argument(
    "-p", "--num-processes", default=4, help="Number of processes", type=int
)  # 27 samples
parser_a.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")
parser_a.add_argument(
    "-b", "--btag", default="deepflav", help="Btagging algorithm (deepflav or deepcsv)"
)
parser_a.add_argument(
    "-s", "--snapshot", default=False, action="store_true", help="Save snapshot"
)
parser_a.add_argument(
    "-e",
    "--eval-model",
    default="",
    help="Evaluate model",
    type=str,
)
parser_a.add_argument(
    "--sf",
    default=False,
    action="store_true",
    help="Apply btagging scale factors",
)
parser_a.print_help()
args_a = parser_a.parse_args()
print(args_a)
