import uproot
import os
import numpy as np
import argparse
import sklearn.metrics as _m
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import mplhep as hep

#plt.rcParams["text.usetex"] = True

parser = argparse.ArgumentParser()
parser.add_argument(
    "--csv-dirs",
    nargs="+",
    default=[
        "/m100_scratch/userexternal/mmalucch/hbb_DNN_input/roc_inputs_csv_el/",
        "/m100_scratch/userexternal/mmalucch/hbb_DNN_input/roc_inputs_csv_mu/",
    ],
)
parser.add_argument(
    "--flav-dirs",
    nargs="+",
    default=[
        "/m100_scratch/userexternal/mmalucch/hbb_DNN_input/roc_inputs_flav_el/",
        "/m100_scratch/userexternal/mmalucch/hbb_DNN_input/roc_inputs_flav_mu/",
    ],
)
parser.add_argument("--out-dir", default="roc_curve")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()


TT_list = ["TTTo2L2Nu", "TTToSemiLeptonic", "TTToHadronic"]
variables_list = [
    "btag_max",
    "btag_min",
    "btag_max_hadronFlavour",
    "btag_min_hadronFlavour",
]
tag_dict = {
    "b vs udsg": [[5], [0], "solid"],
    "b vs c": [[5], [4], "dashed"],
}


def load_data(dirs):
    # list of all the files
    files = []
    for x in dirs:
        for file in os.listdir(x):
            for background in TT_list:
                if background in file:
                    files.append(x + file)
    print(f"Loading files: {files}")

    # open each file and get the Events tree using uproot
    for i, file in enumerate(files):
        print(f"Loading file {file}")
        file = uproot.open(f"{file}:Events")
        variables_array = np.array(
            [file[input].array(library="np") for input in variables_list]
        )
        # get the score columns
        score = np.concatenate(
            (
                variables_array[0],
                variables_array[1],
            ),
            axis=0,
        )

        # ge the hadronFlavour columns
        hadronFlavour = np.concatenate(
            (
                variables_array[2],
                variables_array[3],
            ),
            axis=0,
        )

        if i == 0:
            score_total = score
            hadronFlavour_total = hadronFlavour
        else:
            score_total = np.concatenate((score_total, score), axis=0)
            hadronFlavour_total = np.concatenate(
                (hadronFlavour_total, hadronFlavour), axis=0
            )

    return [score_total, hadronFlavour_total]


def get_labels(y_true, y_score, labels_s, labels_b):
    """Get the labels for the ROC curves
    :param    y_true : array with the true labels
    :param    y_score : array with the scores
    :param    labels_s : list with the labels for the signal
    :param    labels_b : list with the labels for the background
    :return   y_true_tot : array with the true labels for the ROC curves
    :return   y_score_tot : array with the scores for the ROC curves
    """
    # get the true label for signal and background
    y_true_s = np.ones_like(y_true[np.isin(y_true, labels_s)])
    y_true_b = np.zeros_like(y_true[np.isin(y_true, labels_b)])

    # get the score for signal and background
    y_score_s = y_score[np.isin(y_true, labels_s)]
    y_score_b = y_score[np.isin(y_true, labels_b)]

    # concatenate the signal and background
    y_true_tot = np.concatenate((y_true_s, y_true_b), axis=0)
    y_score_tot = np.concatenate((y_score_s, y_score_b), axis=0)

    print("y_tot: ", y_true_tot.shape)
    print("y_tot_signal: ", y_true_s.shape)
    print("y_tot_background: ", y_true_b.shape)

    return y_true_tot, y_score_tot


def get_rates(y_t, y_s, l_s, l_b):
    """Compute the ROC curve and the AUC
    :param    y_t : array with the true labels
    :param    y_s : array with the scores
    :param    l_s : list with the labels for the signal
    :param    l_b : list with the labels for the background
    :param    weights : weights for the different classes
    :return   fpr : array with the false positive rate
    :return   tpr : array with the true positive rate
    :return   roc_auc : float with the AUC
    """

    y_true, y_score = get_labels(y_t, y_s, l_s, l_b)
    fpr, tpr, threshold = _m.roc_curve(y_true, y_score)
    roc_auc = _m.roc_auc_score(y_true, y_score)
    return fpr, tpr, roc_auc


def plt_fts(out_dir, name, fig_handle, show):
    """Plot features
    :param    out_dir : string with the output directory
    :param    name : string with the name of the plot
    :param    fig_handle : figure handle
    """

    plt.xlabel("True positive rate", fontsize=20, loc="right")
    plt.ylabel("False positive rate ", fontsize=20, loc="top")
    plt.xlim([0.23, 1.0005])
    plt.ylim([0.0008, 1.005])
    plt.text(
        0.7,
        0.1,
        "$t\\bar{t}$\n$ \\mathrm{AK4jets}$ $(p_T > 20 \\mathrm{GeV})$",
        fontsize=20,
        horizontalalignment="left",
        verticalalignment="bottom",
        transform=plt.gca().transAxes,
    )
    minorLocator = MultipleLocator(0.05)
    ax = plt.gca()
    ax.xaxis.set_minor_locator(minorLocator)
    plt.yscale("log")

    plt.grid(which="both")
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")

    plt.legend(loc="upper left", fontsize=20)

    plt.savefig(f"{out_dir}/{name}.png", dpi=200, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()


def plotting_function(out_dir, networks):
    """Plot the roc curves for a epoch and a roc type for each network
    :param    out_dir : string with the name of the output directory
    :param    networks :  networks to plot
    """

    fig_handle = plt.figure(figsize=(13, 10))
    for network, rates in networks.items():
        plt.plot(
            rates[1],
            rates[0],
            label=f"{network} (AUC=%.4f)" % rates[2],
            color=rates[3],
            linestyle=rates[4],
        )

    plt_fts(out_dir, f"ROC_DeepCSV_DeepFlavour", fig_handle, args.show)


if "__main__" == __name__:
    os.makedirs(args.out_dir, exist_ok=True)

    networks_dict = {}
    networks_dict["DeepCSV"] = load_data(args.csv_dirs) + ["r"]
    networks_dict["DeepFlavour"] = load_data(args.flav_dirs) + ["b"]

    rates_dict = {}
    for net, data in networks_dict.items():
        for tag_type, labels in tag_dict.items():
            # compute roc curve and auc
            fpr, tpr, roc_auc = get_rates(data[1], data[0], labels[0], labels[1])
            rates_dict[f"{net} {tag_type}"] = [fpr, tpr, roc_auc, data[2], labels[2]]

    plotting_function(args.out_dir, rates_dict)