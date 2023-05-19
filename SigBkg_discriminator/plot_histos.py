import matplotlib.pyplot as plt
import argparse
import torch


def plot_sig_bkg_distributions(pred_lbl_tensor):
    # plot the signal and background distributions for the test dataset using the best model as a function of the DNN output
    sig = pred_lbl_tensor[pred_lbl_tensor[:, 1] == 1]
    bkg = pred_lbl_tensor[pred_lbl_tensor[:, 1] == 0]

    sig_pred = sig[:, 0]
    bkg_pred = bkg[:, 0]

    plt.figure()
    plt.hist(
        sig_pred,
        bins=50,
        range=(0, 1),
        histtype="step",
        label="Signal",
        density=True,
        color="blue",
    )
    plt.hist(
        bkg_pred,
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
    #plt.show()

    plt.savefig(f"{args.input}/sig_bkg_distributions.png")


if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", default="pred_lbls", help="Input directory", type=str
    )
    parser.print_help()
    args = parser.parse_args()

    input_file = f"{args.input}/pred_lbl_tensor.pt"

    # load the predicted labels
    pred_lbl_tensor = torch.load(input_file)

    # plot the signal and background distributions
    plot_sig_bkg_distributions(pred_lbl_tensor)