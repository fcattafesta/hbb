import matplotlib.pyplot as plt
import argparse
import numpy as np


def plot_sig_bkg_distributions(score_lbl_tensor):
    # plot the signal and background distributions for the test dataset using the best model as a function of the DNN output
    sig = score_lbl_tensor[score_lbl_tensor[:, 1] == 1]
    bkg = score_lbl_tensor[score_lbl_tensor[:, 1] == 0]
    print("sig.shape", sig.shape, sig)
    print("bkg.shape", bkg.shape, bkg)

    # get the scores for signal and background
    # and make them the same length (which is the minimum of the two)
    if sig.shape[0] < bkg.shape[0]:
        bkg = bkg[: sig.shape[0]]
    else:
        sig = sig[: bkg.shape[0]]

    sig_score = sig[:, 0]
    bkg_score = bkg[:, 0]

    print("sig_score.shape", sig_score.shape, sig_score)
    print("bkg_score.shape", bkg_score.shape, bkg_score)

    plt.figure()
    plt.hist(
        sig_score,
        bins=50,
        range=(0, 1),
        histtype="step",
        label="Signal",
        density=True,
        color="blue",
    )
    plt.hist(
        bkg_score,
        bins=50,
        range=(0, 1),
        histtype="step",
        label="Background",
        density=True,
        color="red",
    )
    plt.xlabel("DNN output")
    plt.ylabel("Normalized counts")
    plt.legend()
    plt.show()

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