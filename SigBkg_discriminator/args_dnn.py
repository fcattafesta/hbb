import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-b", "--batch-size", default=512, help="Batch size", type=int,
)
parser.add_argument(
    "-e", "--epochs", default=10, help="Number of epochs", type=int,
)
parser.add_argument(
    "-t", "--train-size", default=-1, help="Number of events to process during training", type=int,
)
parser.add_argument(
    "-v", "--val-size", default=-1, help="Number of events to process during validation", type=int,
)
parser.add_argument(
    "-p", "--num-prints", default=50, help="Number of batches to process before printing", type=int,
)

parser.print_help()
args = parser.parse_args()
