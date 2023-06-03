import uproot
import logging
import os
import sys
import numpy as np
import argparse
import sklearn.metrics as _m
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import mplhep as hep

sys.path.append("../")
from logger import setup_logger



parser = argparse.ArgumentParser()
parser.add_argument("--csv-dirs", nargs="+", required=True)
parser.add_argument("--flav-dirs", nargs="+", required=True)
parser.add_argument("--out-dir", default="roc_curve")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()



TT_list = ["TTTo2L2Nu", "TTToSemiLeptonic", "TTToHadronic"]
varibles_list = [
    "btag_max",
    "btag_min",
    "btag_max_hadronFlavour",
    "btag_min_hadronFlavour",
]


def load_data(dirs):
    # list of all the csv files
    files = []
    for x in dirs:
        files = os.listdir(x)
        for file in files:
            for background in TT_list:
                if background in file:
                    files.append(x + file)
                    print(f"Loading file {file}")
    print("Loading files: {files}")

    # open each file and get the Events tree using uproot
    for i, file in enumerate(files):
        print(f"Loading file {file}")
        file = uproot.open(f"{file}:Events")
        variables_array = np.array(
            [file[input].array(library="np") for input in varibles_list]
        )
        print(variables_array.shape, variables_array)
        # concatenate the first two columns of the variables array
        score_csv = np.concatenate(
            (
                variables_array[0].reshape(-1, 1),
                variables_array[1].reshape(-1, 1),
            ),
            axis=1,
        )
        # concatenate the third and fourth columns of the variables array
        hadronFlavour_csv = np.concatenate(
            (
                variables_array[2].reshape(-1, 1),
                variables_array[3].reshape(-1, 1),
            ),
            axis=1,
        )

        if i == 0:
            score_total = score_csv
            hadronFlavour_total = hadronFlavour_csv
        else:
            score_total = np.concatenate((score_total, score_csv), axis=0)
            hadronFlavour_total = np.concatenate(
                (hadronFlavour_total, hadronFlavour_csv), axis=0
            )
        print(score_total.shape, score_csv)
        print(hadronFlavour_total.shape, hadronFlavour_csv)

    print(score_total.shape, score_csv)
    print(hadronFlavour_total.shape, hadronFlavour_csv)

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
    y_true_s = np.logical_or.reduce([y_true == label for label in labels_s])
    y_true_b = np.logical_or.reduce([y_true == label for label in labels_b])
    # consider only the events that are signal or background
    y_true_idx = np.logical_or(y_true_s, y_true_b)
    y_true_tot = y_true_s[y_true_idx].astype(int)

    # get the score for the signal and background by summing the scores
    y_score_s = sum([y_score[:, label] for label in labels_s]) * y_true_s
    y_score_b = sum([y_score[:, label] for label in labels_s]) * y_true_b
    y_score_tot = y_score_s + y_score_b
    # consider only the events that are signal or background
    y_score_tot = y_score_tot[y_true_idx]

    return y_true_tot, y_score_tot


def get_rates(y_t, y_s, l_s, l_b, weights=None):
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

    if l_s is None and l_b is None:
        fpr, tpr, roc_auc = y_s, y_t, np.nan
    else:
        y_true, y_score = get_labels(y_t, y_s, l_s, l_b, weights)
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
    plt.xlim([0.5, 1.0005])
    plt.ylim([0.0001, 1.005])
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
        plt.plot(rates[1], rates[0], label=f"{network} (AUC=%0.4f)" % rates[2])

    plt_fts(out_dir, f"ROC_DeepCSV_DeepFlavour", fig_handle)


if "__main__" == __name__:
    os.makedirs(args.out_dir, exist_ok=True)

    logger = setup_logger(f"{args.out_dir}/logger.log")
    logger.info("args:\n - %s", "\n - ".join(str(it) for it in args.__dict__.items()))

    networks_dict = {}
    networks_dict["csv"] = load_data(args.csv_dirs)
    networks_dict["flav"] = load_data(args.flav_dirs)

    rates_dict = {}
    for net, data in networks_dict.items():
        # compute roc curve and auc
        fpr, tpr, roc_auc = get_rates(data[1], data[0], [5], [1, 2, 3, 21])
        rates_dict[net] = [fpr, tpr, roc_auc]


    plotting_function(args.out_dir, rates_dict)
