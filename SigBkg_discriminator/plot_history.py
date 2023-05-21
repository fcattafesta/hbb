# plot the history for the training and validation losses and accuracies

import argparse
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
from scipy.ndimage import uniform_filter1d


def read_from_txt(file):
    # read form a txt with the info written like this:

    # get accuracy and loss and separate them between training and validation
    with open(file, "r") as f:
        lines = f.readlines()
        train_accuracy = []
        train_loss = []
        val_accuracy = []
        val_loss = []
        for line in lines:
            if "Training" in line:
                train_accuracy.append(float(line.split("accuracy: ")[1].split(" ")[0]))
                train_loss.append(float(line.split("loss: ")[1].split("\n")[0]))
            if "Validation" in line:
                val_accuracy.append(float(line.split("accuracy: ")[1].split(" ")[0]))
                val_loss.append(float(line.split("loss: ")[1].split("\n")[0]))

    return train_accuracy, train_loss, val_accuracy, val_loss


def plot_history(train_accuracy, train_loss, val_accuracy, val_loss, dir, show, uniform_filter=10):
    infos_dict = {
        "accuracy": {"train": train_accuracy, "val": val_accuracy},
        "loss": {"train": train_loss, "val": val_loss},
    }

    for type, info in infos_dict.items():
        plt.figure(figsize=(10, 10))
        plt.plot(
            range(len(info["train"])),
            uniform_filter1d(info["train"], size=uniform_filter),
            label=f"Training {type}",
            color="blue",
        )
        plt.plot(
            range(len(info["val"])),
            uniform_filter1d(info["val"], size=uniform_filter),
            label=f"Validation {type}",
            color="orange",
        )

        plt.xlabel("Epoch")
        plt.ylabel(type.capitalize())
        plt.legend()
        hep.style.use("CMS")
        hep.cms.label("Preliminary")
        hep.cms.label(year="UL18")
        plt.savefig(f"{dir}/{type}.png")
        if show:
            plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-dir", type=str, help="path to tensorboard log file"
    )
    parser.add_argument(
        "-u",
        "--uniform-filter",
        default=10,
        type=int,
        help="size of the uniform filter",
    )
    parser.add_argument(
        "-s",
        "--show",
        default=False,
        action="store_true",
        help="show plots",
    )
    args = parser.parse_args()

    train_accuracy, train_loss, val_accuracy, val_loss = read_from_txt(
        f"{args.input_dir}/log.txt"
    )

    plot_history(train_accuracy, train_loss, val_accuracy, val_loss, args.input_dir, args.show, args.uniform_filter)
