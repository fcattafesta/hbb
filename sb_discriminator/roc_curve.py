import uproot
import os
import numpy as np
import argparse
import sklearn.metrics as _m
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import mplhep as hep
import glob


# plt.rcParams["text.usetex"] = True

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dirs",
    nargs="+",
    default=[
        "/scratchnvme/malucchi/hbb_samples/TTToHadronic/"
        # "/m100_scratch/userexternal/mmalucch/hbb_DNN_input/nano_roc_inputs/",
    ],
)

parser.add_argument("--out-dir", default="roc_curve")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()


wp_lists = (
    list(np.linspace(0.0001, 0.0009, 9)) + list(np.linspace(0.001, 0.009, 9)) + list(np.linspace(0.01, 0.1, 10))
)
print(len(wp_lists))
print(wp_lists)


TT_list = ["TTToHadronic"]
#NOTE: CleanJet_jetId > 0 && CleanJet_puId > 0
var_list = [
    "Jet_btagDeepB",
    "Jet_btagDeepFlavB",
    "Jet_hadronFlavour",
    "Jet_pt",
    "Jet_eta",
]

tag_dict = {
    "b vs udsg": [[5], [0], "solid"],
    "b vs c": [[5], [4], "dashed"],
}


def load_data(dirs, variables_list):
    # list of all the files
    files = []
    for x in dirs:
        for i, file in enumerate(glob.glob("%s/**/*.root" % x, recursive=True)):
            if i < 1:
                files.append(file)
    print(f"Loading files: {files}")

    networks_dict = {
        "DeepCSV": [np.array([]), np.array([]), "r"],
        "DeepFlavour": [np.array([]), np.array([]), "b"],
    }

    # open each file and get the Events tree using uproot
    for file in files:
        print(f"Loading file {file}")
        file = uproot.open(f"{file}:Events")
        variables = np.array(
            [
                np.concatenate(file[input].array(library="np"))
                for input in variables_list
            ]
        )

        print("variables", variables, len(variables))
        # exclude the events with -1 in the DeepCSV column
        mask = (
            np.array(variables[0, :] != -1)
            * np.array(variables[3, :] > 30) #>20
            * np.array(variables[3, :] < 200)
            * np.array(variables[4, :] < 1.4) #<2.5
            * np.array(variables[4, :] > -1.4) # >2.5
        )
        print("mask", mask)
        variables = variables[:, mask]
        print("variables_mask", variables, len(variables))

        for j, btag in enumerate(networks_dict.keys()):
            # get the score columns
            score = variables[j]

            # ge the hadronFlavour columns
            hadronFlavour = variables[2]

            networks_dict[btag][0] = np.concatenate(
                (networks_dict[btag][0], score), axis=0
            )
            networks_dict[btag][1] = np.concatenate(
                (networks_dict[btag][1], hadronFlavour), axis=0
            )

            print(
                btag,
                networks_dict[btag][0].shape,
                networks_dict[btag][0],
                networks_dict[btag][1].shape,
                networks_dict[btag][1],
            )

    return networks_dict


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
    return fpr, tpr, roc_auc, threshold


def plt_fts(out_dir, name, fig_handle, show):
    """Plot features
    :param    out_dir : string with the output directory
    :param    name : string with the name of the plot
    :param    fig_handle : figure handle
    """

    plt.xlabel("b-jet efficiency", fontsize=20, loc="right")
    plt.ylabel("mis-id rate", fontsize=20, loc="top")
    plt.xlim([0.5, 1.0005])
    plt.ylim([0.0005, 1.005])
    plt.text(
        0.05,
        0.6,
        r"$t\bar{t} (\mathrm{AK4jets})$"
        + "\n"
        + r"$p_T \in (30, 200) \mathrm{GeV} , |\eta| < 1.4$",
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


def printer(f, rates, i):
    f.write("threshold: %.4f \n" % rates[5][i])
    f.write("fpr: %.4f \n" % rates[0][i])
    f.write("tpr: %.4f \n" % rates[1][i])


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

    networks_dict = load_data(args.dirs, var_list)

    rates_dict = {}
    for net, data in networks_dict.items():
        for tag_type, labels in tag_dict.items():
            if "udsg" in tag_type:
                # compute roc curve and auc
                fpr, tpr, roc_auc, threshold = get_rates(
                    data[1], data[0], labels[0], labels[1]
                )
                rates_dict[f"{net}"] = [
                    fpr,
                    tpr,
                    roc_auc,
                    data[2],
                    labels[2],
                    threshold,
                ]

    plotting_function(args.out_dir, rates_dict)

    # save the fpr, tpr and threshold for each network to a file
    with open(f"{args.out_dir}/roc_data.txt", "w") as f:
        for net, rates in rates_dict.items():
            if True: #"udsg" in net:
                f.write("network: %s\n" % net)
                print_dict = {x: True for x in wp_lists}

                for i in range(len(rates[0])):
                    for key, value in print_dict.items():
                        if rates[0][i] >= key and value:
                            printer(f, rates, i)
                            print_dict[key] = False
                f.write("\n############################################\n")
