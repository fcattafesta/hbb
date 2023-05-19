# plot the history for the training and validation losses and accuracies

import argparse
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep

# import a tensorboard log file
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

# read the tensorboard log file
def read_tensorboard_log_file(log_file):
    event_acc = EventAccumulator(log_file)
    event_acc.Reload()
    # Show all tags in the log file
    print(event_acc.Tags())
    # E. g. get wall clock, number of steps and value for a scalar 'Accuracy'

    infos = [event_acc.Scalars('Accuracy/train'), event_acc.Scalars('Accuracy/val'), event_acc.Scalars('Loss/train'), event_acc.Scalars('Loss/val')]
    w_times = [zip(*info)[0] for info in infos]
    step_nums = [zip(*info)[1] for info in infos]
    vals = [zip(*info)[2] for info in infos]


    return w_times, step_nums, vals

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_file", type=str, help="path to tensorboard log file")
    args = parser.parse_args()

    w_times, step_nums, vals = read_tensorboard_log_file(args.log_file)

    # plot the history for the training and validation losses and accuracies
    plt.figure(figsize=(13, 10))
    plt.plot(step_nums[0], vals[0], label="Training Accuracy", color="blue")
    plt.plot(step_nums[1], vals[1], label="Validation Accuracy", color="red")
    plt.plot(step_nums[2], vals[2], label="Training Loss", color="blue", linestyle="--")
    plt.plot(step_nums[3], vals[3], label="Validation Loss", color="red", linestyle="--")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy/Loss")
    plt.legend()
    plt.savefig("history.png")
    plt.show()