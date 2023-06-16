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


# plt.rcParams["text.usetex"] = True

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dir",
    default="deepcsv_eval_newSR",
)
parser.add_argument(
    "-b", "--btag", default="deepcsv", help="Btagging algorithm (deepflav or deepcsv)"
)
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")

parser.add_argument("--out-dir", default="btag_plots")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()

main_dir = f"/gpfs/ddn/cms/user/malucchi/hbb_out/{args.lep}/" + args.dir + "/Snapshots/"

var_list = [
    "btag_max",
    "btag_min",
    "atanhDNN_Score",
]

bins = [
    [
        0,
        0.029,
        0.379,
        0.729,
        1.079,
        1.429,
        1.779,
        2.129,
        2.479,
        2.829,
        10.0,
    ],
    np.linspace(0, 1, 10),
]


def load_data(dir, variables_list):
    # list of all the files
    files = []
    print(dir)
    print(variables_list)

    for i, file in enumerate(glob.glob("%s/**/*_SR_*.root" % dir, recursive=True)):
        if i < 10000:
            files.append(file)

    var_tot = np.array([[], [], []])
    # open each file and get the Events tree using uproot
    for file in files:
        try:
            print(f"Loading file {file}")
            file = uproot.open(f"{file}:Events")
            variables = np.array(
                [file[input].array(library="np") for input in variables_list]
            )
            print(variables.shape)
            #mask = np.array(variables[2, :]>2.829)
            #variables = variables[:, mask]
            var_tot = np.concatenate((var_tot, variables), axis=1)
        except uproot.exceptions.KeyInFileError:
            print(f"File {file} empty")
            continue

    print("var_tot", var_tot, var_tot.shape)

    return var_tot


def plt_fts(out_dir, name, fig_handle, show):
    """Plot features
    :param    out_dir : string with the output directory
    :param    name : string with the name of the plot
    :param    fig_handle : figure handle
    """

    plt.xlabel(f"btag score {args.btag}", fontsize=20, loc="right")
    plt.ylabel("atanh(DNN score)", fontsize=20, loc="top")

    minorLocator = MultipleLocator(0.05)
    ax = plt.gca()
    ax.xaxis.set_minor_locator(minorLocator)

    plt.grid(which="both")
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")

    plt.savefig(f"{out_dir}/{name}.png", dpi=200, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()


def plotting_function(out_dir, variables, type):
    fig_handle = plt.figure(figsize=(13, 10))

    # plot scatter plot
    plt.hist2d(
        variables[0],
        variables[1],
        bins=[50, 50],#bins,
        cmap=plt.cm.jet,
        density=True,
        range=[[0, 1], [0, 10]],
        norm=mpl.colors.LogNorm(),
    )
    ax = plt.gca()
    cmap = mpl.cm.jet
    norm = mpl.colors.LogNorm()#vmin=0.00001, vmax=1.0)
    plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax).set_label(
        "Log Normalized counts", loc="center", fontsize=20
    )

    plt_fts(
        out_dir, f"btag_VS_DNN_{args.lep}_{args.btag}_{type}", fig_handle, args.show
    )


if "__main__" == __name__:
    os.makedirs(args.out_dir, exist_ok=True)

    variables = load_data(main_dir, var_list)

    variables_max = np.array([variables[0], variables[2]])
    variables_min = np.array([variables[1], variables[2]])

    plotting_function(args.out_dir, variables_max, "max")
    plotting_function(args.out_dir, variables_min, "min")
