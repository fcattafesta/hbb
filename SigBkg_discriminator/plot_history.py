# plot the history for the training and validation losses and accuracies

import argparse
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep


def read_from_txt(file):
    # read form a txt with the info written like this:
    # EPOCH # 14  Validation batch 97.9 %         accuracy: 0.8080      //      loss: 0.4195

    # get accuracy and loss and separate them between training and validation
    with open(file, 'r') as f:
        lines = f.readlines()
        train_accuracy = []
        train_loss = []
        val_accuracy = []
        val_loss = []
        for line in lines:
            if 'Training' in line:
                train_accuracy.append(float(line.split('accuracy: ')[1].split(' ')[0]))
                train_loss.append(float(line.split()[2]))
            if 'Validation' in line:
                val_accuracy.append(float(line.split('accuracy: ')[1].split(' ')[0]))
                val_loss.append(float(line.split()[2]))

    return train_accuracy, train_loss, val_accuracy, val_loss


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-file", type=str, help="path to tensorboard log file"
    )
    args = parser.parse_args()

    train_accuracy, train_loss, val_accuracy, val_loss = read_from_txt(args.input_file)

    for info in ["accuracy", "loss"]:
        plt.figure(figsize=(10, 10))
        plt.plot(
            range(len(train_accuracy)),
            train_accuracy,
            label="Training " + info,
            color="blue",
        )
        plt.plot(
            range(len(val_accuracy)),
            val_accuracy,
            label="Validation " + info,
            color="orange",
        )
        plt.title("Training and validation " + info)

        plt.xlabel("Epoch")
        plt.ylabel(info.capitalize())
        plt.legend()
        plt.savefig(info + ".png")
        plt.show()
