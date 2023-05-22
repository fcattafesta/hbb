import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-b",
    "--batch-size",
    default=32,
    help="Batch size",
    type=int,
)
parser.add_argument(
    "-e",
    "--epochs",
    default=10,
    help="Number of epochs",
    type=int,
)
parser.add_argument(
    "-t",
    "--train-size",
    default=-1,
    help="Number of events to process during training",
    type=int,
)
parser.add_argument(
    "-v",
    "--val-size",
    default=-1,
    help="Number of events to process during validation",
    type=int,
)
parser.add_argument(
    "-te",
    "--test-size",
    default=-1,
    help="Number of events to process during testing",
    type=int,
)
parser.add_argument(
    "-p",
    "--num-prints",
    default=50,
    help="Number of prints for each epoch",
    type=int,
)
parser.add_argument(
    "-n",
    "--num-workers",
    default=4,
    help="Number of workers for data loading",
    type=int,
)
parser.add_argument(
    "-d",
    "--data-dirs",
    nargs="+",
    default=[
        # "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/snap/Snapshots/",
        # "/gpfs/ddn/cms/user/malucchi/hbb_out/el/snap/Snapshots/",
        "~/el/Snapshots/",
        "~/mu/Snapshots/",
    ],
    help="Directory for data",
)
parser.add_argument(
    "--eval",
    action="store_true",
    help="Evaluate the model",
    default=False,
)
# TODO: add option to use multiple gpus
parser.add_argument(
    "-g", "--gpu", default=False, help="GPU number", action="store_true"
)
parser.add_argument(
    "--histos", default=False, help="Make histograms", action="store_true"
)
parser.add_argument(
    "--history", default=False, help="Plot history", action="store_true"
)
parser.add_argument(
    "--eval-model",
    default="",
    help="Path to model to evaluate",
    type=str,
)
parser.add_argument(
    "-l",
    "--load-model",
    default="",
    help="Path to model to load and continue training",
    type=str,
)
parser.print_help()
args = parser.parse_args()
