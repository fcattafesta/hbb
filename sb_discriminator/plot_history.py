import argparse
import matplotlib.pyplot as plt
import mplhep as hep
from scipy.ndimage import uniform_filter1d
import os
import numpy as np


def read_from_txt(file):
    # get accuracy and loss and separate them between training and validation
    with open(file, "r") as f:
        lines = f.readlines()
        train_accuracy = []
        train_loss = []
        val_accuracy = []
        val_loss = []
        i = 0
        j = 0
        for line in lines:
            if "Training batch" in line:
                train_accuracy.append(float(line.split("accuracy: ")[1].split(" ")[0]))
                train_loss.append(float(line.split("loss: ")[1].split("\n")[0]))
                i += 1
            elif "Validation batch" in line:
                val_accuracy.append(float(line.split("accuracy: ")[1].split(" ")[0]))
                val_loss.append(float(line.split("loss: ")[1].split("\n")[0]))
                j += 1
                if j > 10000:
                    print(line)

    print("len train accuracy: ", len(train_accuracy))
    print("len train loss: ", len(train_loss))
    print("len val accuracy: ", len(val_accuracy))
    print("len val loss: ", len(val_loss))

    return train_accuracy, train_loss, val_accuracy, val_loss


def plot_history(
    train_accuracy,
    train_loss,
    val_accuracy,
    val_loss,
    dir,
    show,
    uniform_filter=50,
    lenght=-1,
):
    infos_dict = {
        "accuracy": {"train": train_accuracy[:lenght], "val": val_accuracy[:lenght]},
        "loss": {"train": train_loss[:lenght], "val": val_loss[:lenght]},
    }
    line_style = {
        "accuracy": "--",
        "loss": "-",
    }

    plt.figure(figsize=(13, 13))

    for type, info in infos_dict.items():
        print("len info train: ", len(info["train"]))
        print("len info val: ", len(info["val"]))
        plt.plot(
            np.linspace(0, len(info["train"]) / 50, len(info["train"])),
            # range(len(info["train"])),
            uniform_filter1d(info["train"], size=uniform_filter),
            label=f"Training {type}",
            color="dodgerblue",
            linestyle=line_style[type],
        )
        plt.plot(
            np.linspace(
                0,
                len(info["val"]) / 50
                if len(info["val"]) / 50 == len(info["train"]) / 50
                else len(info["train"]) / 50,
                len(info["val"]),
            ),
            # range(len(info["val"])),
            uniform_filter1d(info["val"], size=uniform_filter),
            label=f"Validation {type}",
            color="r",
            linestyle=line_style[type],
        )

    plt.xlabel("Epoch", fontsize=20, loc="right")
    # plt.ylabel(type.capitalize())
    # legend = ax.legend(frameon=False)
    plt.legend(
        fontsize="15",
        frameon=False,
        loc="center right",
    )
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")
    plt.grid()
    plt.savefig(f"{dir}/history.png", bbox_inches="tight")
    if show:
        plt.show()


if __name__ == "__main__":
    # plot the history for the training and validation losses and accuracies
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-path", type=str, help="path to log file")
    parser.add_argument(
        "-u",
        "--uniform-filter",
        default=50,
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
    parser.add_argument(
        "-l",
        "--lenght",
        default=-1,
        help="max lenght of the plot",
        type=int,
    )
    args = parser.parse_args()

    train_accuracy, train_loss, val_accuracy, val_loss = read_from_txt(args.input_path)

    plot_history(
        train_accuracy,
        train_loss,
        val_accuracy,
        val_loss,
        os.path.dirname(args.input_path),
        args.show,
        args.uniform_filter,
        args.lenght,
    )
