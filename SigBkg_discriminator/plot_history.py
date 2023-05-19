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

    # save the step and the value for the scalar in infos
    infos = [
        event_acc.Scalars("Accuracy/train"),
        event_acc.Scalars("Accuracy/val"),
        event_acc.Scalars("Loss/train"),
        event_acc.Scalars("Loss/val"),
    ]
    vals = ()
    step_nums = ()
    for info in infos:
        step_nums.append(event_acc.Scalars(info).step)
        vals.append(event_acc.Scalars(info).value)

    print("step_nums", step_nums)
    print("vals", vals)

    return step_nums, vals


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-file", type=str, help="path to tensorboard log file"
    )
    args = parser.parse_args()

    step_nums, vals = read_tensorboard_log_file(args.input_file)

    # plot the history for the training and validation losses and accuracies
    plt.figure(figsize=(13, 10))
    plt.plot(step_nums[0], vals[0], label="Training Accuracy", color="blue")
    plt.plot(step_nums[1], vals[1], label="Validation Accuracy", color="red")
    plt.plot(step_nums[2], vals[2], label="Training Loss", color="blue", linestyle="--")
    plt.plot(
        step_nums[3], vals[3], label="Validation Loss", color="red", linestyle="--"
    )
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy/Loss")
    plt.legend()
    plt.savefig("history.png")
    plt.show()
