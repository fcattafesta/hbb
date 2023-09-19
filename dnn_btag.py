import uproot
import os
import numpy as np
import argparse
import sklearn.metrics as _m
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import mplhep as hep
import glob
import matplotlib as mpl
import csv
from samples import samples


# plt.rcParams["text.usetex"] = True

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dir",
    default="deepflav_eval_newSR",
)
parser.add_argument(
    "-b", "--btag", default="DeepFlavour", help="Btagging algorithm (DeepFlavour or DeepCSV)"
)
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")

parser.add_argument("--out-dir", default="btag_files")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()


def read_txt_file(filename, name):
    threshold_list = []
    with open(filename, "r") as f:
        current_network = None
        for line in f:
            if line.startswith("network:"):
                current_network = line.split(":")[1].strip()
            elif line.startswith("threshold:"):
                threshold_value = float(line.split(":")[1])
                if name in current_network:
                    threshold_list.append(threshold_value)
    threshold_list.reverse()
    return threshold_list


# main_dir = f"/gpfs/ddn/cms/user/malucchi/hbb_out/{args.lep}/{args.dir}/Snapshots/"
main_dir_mu = f"/gpfs/ddn/cms/user/malucchi/hbb_out/mu/{args.dir}/Snapshots/"
main_dir_el = f"/gpfs/ddn/cms/user/malucchi/hbb_out/el/{args.dir}/Snapshots/"

var_list = [
    "btag_max",
    "btag_min",
    "atanhDNN_Score",
]

# wp L, M, T, UT
thresholds = (
    [0.0420, 0.2551, 0.6855, 0.7988]
    if args.btag == "DeepFlavour"
    else [0.1047, 0.3787, 0.7563, 0.8486]
)

# thresholds = read_txt_file("sb_discriminator/roc_curve/roc_data.txt", args.btag)
print(thresholds)

bins = [
    [0.0] + thresholds + [1.0],  # np.linspace(0, 1, 50),
    # [
    #     0,
    #     0.029,
    #     0.379,
    #     0.729,
    #     1.079,
    #     1.429,
    #     1.779,
    #     2.129,
    #     2.479,
    #     2.829,
    #     10.0,
    # ],
    # [
    #     0.0,
    #     # 0.0015,
    #     1.425,
    #     1.7085,
    #     1.9155,
    #     2.1195,
    #     2.3265,
    #     2.568,
    #     2.7315,
    #     3.024,
    #     10,
    # ],
    [  # smooth rebin 10
        0.0,
        0.015,
        1.53,
        1.815,
        2.04,
        2.265,
        2.475,
        2.685,
        2.94,
        3.315,
        10,
    ],
]


def load_data(dir_mu, dir_el, variables_list):
    # list of all the files
    files = []
    print(dir_mu)
    print(variables_list)

    for i, file in enumerate(glob.glob("%s/**/*_SR_*.root" % dir_mu, recursive=True)):
        if i < 10000 and "SingleMuon" not in file and "EGamma" not in file:
            files.append(file)
    for i, file in enumerate(glob.glob("%s/**/*_SR_*.root" % dir_el, recursive=True)):
        if i < 10000 and "SingleMuon" not in file and "EGamma" not in file:
            files.append(file)
    # print(f"Loading files: {files}")

    var_tot = np.array([[], [], [], []])
    # open each file and get the Events tree using uproot
    for file in files:
        try:
            print(f"Loading file {file}")
            sample_name = file.split("/")[-1].split("_SR")[0].split("_CR")[0]
            print(f"Sample name: {sample_name}")
            file = uproot.open(f"{file}:Events")
            variables = np.array(
                [file[input].array(library="np") for input in variables_list]
            )
            variables = np.concatenate(
                (
                    variables,
                    samples[sample_name]["xsec"] * np.ones((1, variables.shape[1])),
                ),
                axis=0,
            )
            print(variables, variables.shape)

            # mask = np.array(variables[2, :]>2.829)
            # variables = variables[:, mask]
            var_tot = np.concatenate((var_tot, variables), axis=1)
        except uproot.exceptions.KeyInFileError:
            print(f"File {file} empty")
            continue

    print("var_tot", var_tot, var_tot.shape)

    return var_tot


def plt_fts(out_dir, name, fig_handle, show, type):
    """Plot features
    :param    out_dir : string with the output directory
    :param    name : string with the name of the plot
    :param    fig_handle : figure handle
    """

    plt.xlabel("$btag_{" + type + "}$ " + args.btag, fontsize=20, loc="right")
    plt.ylabel("atanh(DNN score)", fontsize=20, loc="top")

    minorLocator = MultipleLocator(0.05)
    ax = plt.gca()
    ax.xaxis.set_minor_locator(minorLocator)

    # plt.tick_params(axis="x", labelsize=16)
    # plt.tick_params(axis="y", labelsize=16)

    plt.grid(which="both")
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")

    plt.savefig(f"{out_dir}/{name}.png", dpi=200, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()


def plotting_function(out_dir, variables, type):
    fig_handle = plt.figure(figsize=(13, 13))

    # plot scatter plot
    plt.hist2d(
        variables[0],
        variables[1],
        bins=bins,  # [50, 50],
        cmap=plt.cm.jet,
        density=True,
        range=[[0, 1], [0, 10]],
        norm=mpl.colors.LogNorm(),
        weights=variables[2],
    )
    ax = plt.gca()
    cmap = mpl.cm.jet
    norm = mpl.colors.LogNorm(vmin=0.00001, vmax=1.0)
    plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax).set_label(
        "Log Normalized counts", loc="center", fontsize=20
    )

    plt_fts(
        out_dir,
        f"btag_VS_DNN_{args.btag}_{type}",
        fig_handle,
        args.show,
        type,
    )


def fractions(out_dir, variables, type):
    # find the fraction of events with btag score > threshold for each atanhDNN score bin

    fractions = [[] for _ in range(len(bins[1]) - 1)]
    for i in range(len(bins[1]) - 1):
        mask = np.array(
            (variables[1] > bins[1][i]) & (variables[1] < bins[1][i + 1]), dtype=bool
        )
        print(mask)
        print(variables[0][mask])
        print(variables[1][mask])
        print(variables[2][mask])

        for j in range(len(thresholds)):
            if j + 1 < len(thresholds):
                fractions[i].append(
                    np.sum(
                        np.logical_and(
                            variables[0][mask] > thresholds[j],
                            variables[0][mask] < thresholds[j + 1],
                        )
                        * variables[2][mask]
                    )
                    / np.sum(variables[2][mask])
                )
            else:
                fractions[i].append(
                    np.sum((variables[0][mask] > thresholds[j]) * variables[2][mask])
                    / np.sum(variables[2][mask])
                )
    print(fractions)

    return fractions


if "__main__" == __name__:
    os.makedirs(args.out_dir, exist_ok=True)

    variables = load_data(main_dir_mu, main_dir_el, var_list)

    variables_max = np.array([variables[0], variables[2], variables[3]])
    variables_min = np.array([variables[1], variables[2], variables[3]])

    for v, s in zip([variables_min, variables_max], ["min", "max"]):
        plotting_function(args.out_dir, v, s)

    fractions_max = fractions(args.out_dir, variables_max, "max")
    fractions_min = fractions(args.out_dir, variables_min, "min")

    # write fractions to file
    with open(f"{args.out_dir}/fractions_{args.btag}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["fractions_max", fractions_max])
        writer.writerow(["fractions_min", fractions_min])
