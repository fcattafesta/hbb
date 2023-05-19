# plot the history for the training and validation losses and accuracies

import argparse
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep

from torch.utils.tensorboard import SummaryReader

# read the tensorboard log file
def read_tensorboard_log_file(log_file):
    reader = SummaryReader(log_file)

    # Initialize a dictionary to store scalar values
    scalar_data = {}

    # Extract scalar values from the log file
    for scalar in reader.scalars():
        scalar_name = scalar.tag
        if scalar_name not in scalar_data:
            scalar_data[scalar_name] = {'steps': [], 'values': []}
        scalar_data[scalar_name]['steps'].append(scalar.step)
        scalar_data[scalar_name]['values'].append(scalar.value)

    # Plot each scalar value separately
    for scalar_name, data in scalar_data.items():
        steps = data['steps']
        values = data['values']
        plt.plot(steps, values, label=scalar_name)
    return scalar_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-file", type=str, help="path to tensorboard log file"
    )
    args = parser.parse_args()

    scalar_data = read_tensorboard_log_file(args.input_file)

    # Plot each scalar value separately
    for scalar_name, data in scalar_data.items():
        steps = data['steps']
        values = data['values']
        plt.plot(steps, values, label=scalar_name)

    plt.xlabel("Epoch")
    plt.ylabel("Accuracy/Loss")
    plt.legend()
    plt.savefig("history.png")
    plt.show()
