import matplotlib.pyplot as plt
import argparse
import numpy as np


def plot_sig_bkg_distributions(score_lbl_tensor):
    # plot the signal and background distributions for the test dataset using the best model as a function of the DNN output
    sig = score_lbl_tensor[score_lbl_tensor[:, 1] == 1]
    bkg = score_lbl_tensor[score_lbl_tensor[:, 1] == 0]
    print("sig.shape", sig.shape, sig)
    print("bkg.shape", bkg.shape, bkg)

    sig_score = sig[:, 0]
    bkg_score = bkg[:, 0]

    print("sig_score.shape", sig_score.shape, sig_score)
    print("bkg_score.shape", bkg_score.shape, bkg_score)

    plt.figure(figsize=(10, 10))
    plt.hist(
        sig_score,
        bins=500,
        range=(0, 1),
        histtype="step",
        label="Signal",
        density=True,
        color="blue",
    )
    plt.hist(
        bkg_score,
        bins=500,
        range=(0, 1),
        histtype="step",
        label="Background",
        density=True,
        color="red",
    )
    plt.xlabel("DNN output")
    plt.ylabel("Normalized counts")
    plt.legend()
    #plt.show()

    plt.savefig(f"{args.input}/sig_bkg_distributions.png")


if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", default="score_lbls", help="Input directory", type=str
    )
    parser.print_help()
    args = parser.parse_args()


    input_file = f"{args.input}/score_lbl_array.npy"

    # load the labels and scores from the test dataset
    score_lbl_tensor = np.load(input_file)

    # plot the signal and background distributions
    plot_sig_bkg_distributions(score_lbl_tensor)