import matplotlib.pyplot as plt
import argparse
import numpy as np
import mplhep as hep

def handle_arrays(score_lbl_tensor):
    sig = score_lbl_tensor[score_lbl_tensor[:, 1] == 1]
    bkg = score_lbl_tensor[score_lbl_tensor[:, 1] == 0]
    print("sig.shape", sig.shape, sig)
    print("bkg.shape", bkg.shape, bkg)

    # get the scores for signal and background
    # and make them the same length (which is the minimum of the two)

    # if sig.shape[0] < bkg.shape[0]:
    #     bkg = bkg[: sig.shape[0]]
    # else:
    #     sig = sig[: bkg.shape[0]]

    sig_score = sig[:, 0]
    bkg_score = bkg[:, 0]

    print("sig_score.shape", sig_score.shape, sig_score)
    print("bkg_score.shape", bkg_score.shape, bkg_score)

    return sig_score, bkg_score


def plot_sig_bkg_distributions(score_lbl_tensor_train, score_lbl_tensor_test):
    # plot the signal and background distributions for the test dataset using the best model as a function of the DNN output
    sig_score_train, bkg_score_train = handle_arrays(score_lbl_tensor_train)
    sig_score_test, bkg_score_test = handle_arrays(score_lbl_tensor_test)

    plt.figure(figsize=(13, 10))
    plt.hist(
        sig_score_train,
        bins=30,
        range=(0, 1),
        histtype="step",
        label="Signal (training)",
        density=True,
        edgecolor="blue",
        facecolor="dodgerblue",
        fill=True,
        alpha=0.5,
    )
    plt.hist(
        bkg_score_train,
        bins=30,
        range=(0, 1),
        histtype="step",
        label="Background (training)",
        density=True,
        color="red",
        fill=False,
        hatch="\\\\",
    )

    # Create the histogram with dots on top using plt.scatter
    counts, bins, _ = plt.hist(sig_score_test, bins=30, alpha=0      ,  label="Signal (test)"
)  # alpha=0 hides the bars

    # Calculate the x-position of the dots as the center of each bin
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    # Plot the dots on top of the histogram
    plt.scatter(bin_centers, counts, c='blue', s=10)

    # Create the histogram with dots on top using plt.scatter
    counts, bins, _ = plt.hist(bkg_score_test, bins=30, alpha=0,         label="Background (test)")  # alpha=0 hides the bars

    # Calculate the x-position of the dots as the center of each bin
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    # Plot the dots on top of the histogram
    plt.scatter(bin_centers, counts, c='red', s=10)

    # plt.hist(
    #     sig_score_test,
    #     bins=30,
    #     range=(0, 1),
    #     histtype="step",
    #     label="Signal (test)",
    #     density=True,
    #     edgecolor="blue",
    #     facecolor="dodgerblue",
    #     fill=True,
    #     alpha=0.5,
    # )

    # plt.hist(
    #     bkg_score_test,
    #     bins=30,
    #     range=(0, 1),
    #     histtype="step",
    #     label="Background (test)",
    #     density=True,
    #     color="red",
    #     fill=False,
    #     hatch="\\\\",
    # )


    plt.xlabel("DNN output", fontsize=20, loc="right")
    plt.ylabel("Normalized counts", fontsize=20, loc="top")
    plt.legend(loc="upper center", fontsize=20)
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")
    plt.savefig(f"{args.input}/sig_bkg_distributions.png")
    if args.show:
        plt.show()


if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", default="score_lbls", help="Input directory", type=str
    )
    parser.add_argument(
        "-s", "--show", default=False, help="Show plots", action="store_true"
    )
    parser.print_help()
    args = parser.parse_args()

    input_file = f"{args.input}/score_lbl_array.npy"

    # load the labels and scores from the train and test datasets from a .npz file
    score_lbl_tensor_train = np.load(input_file, allow_pickle=True)["score_lbl_array_train"]
    score_lbl_tensor_test = np.load(input_file, allow_pickle=True)["score_lbl_array_test"]

    # plot the signal and background distributions
    plot_sig_bkg_distributions(score_lbl_tensor_train, score_lbl_tensor_test)
