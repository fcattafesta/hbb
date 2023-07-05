import argparse

parser_t = argparse.ArgumentParser()

parser_t.add_argument(
    "-b",
    "--batch-size",
    default=32,
    help="Batch size",
    type=int,
)
parser_t.add_argument(
    "-e",
    "--epochs",
    default=10,
    help="Number of epochs",
    type=int,
)
parser_t.add_argument(
    "-t",
    "--train-size",
    default=-1,
    help="Number of events to process during training",
    type=int,
)
parser_t.add_argument(
    "-v",
    "--val-size",
    default=-1,
    help="Number of events to process during validation",
    type=int,
)
parser_t.add_argument(
    "-te",
    "--test-size",
    default=-1,
    help="Number of events to process during testing",
    type=int,
)
parser_t.add_argument(
    "-p",
    "--num-prints",
    default=50,
    help="Number of prints for each epoch",
    type=int,
)
parser_t.add_argument(
    "-n",
    "--num-workers",
    default=4,
    help="Number of workers for data loading",
    type=int,
)
parser_t.add_argument(
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
parser_t.add_argument(
    "--eval",
    action="store_true",
    help="Evaluate the model",
    default=False,
)
parser_t.add_argument(
    "-g", "--gpus", default="", help="GPU numbers separated by a comma", type=str
)
parser_t.add_argument(
    "--histos", default=False, help="Make histograms", action="store_true"
)
parser_t.add_argument(
    "--history", default=False, help="Plot history", action="store_true"
)
parser_t.add_argument(
    "--eval-model",
    default="",
    help="Path to model to evaluate",
    type=str,
)
parser_t.add_argument(
    "-l",
    "--load-model",
    default="",
    help="Path to model to load and continue training",
    type=str,
)
parser_t.add_argument(
    "-o",
    "--onnx",
    default=False,
    help="Save model in ONNX format",
    action="store_true",
)
parser_t.add_argument(
    "--pin-memory",
    default=False,
    help="Pin memory for data loading",
    action="store_true",
)
parser_t.add_argument(
    "--weights",
    nargs="+",
    default=[50, 0.014],  # [50, 0.01] for csv, [50, 0.014] for flav
    help="Weights for the loss function (signal, background)",
    type=float,
)
parser_t.add_argument(
    "--name",
    default="",
    help="Name for the directory",
    type=str,
)
parser_t.add_argument(
    "--noVV",
    default=False,
    help="Remove VV from the background",
    action="store_true",
)

parser_t.print_help()
args_t = parser_t.parse_args()
