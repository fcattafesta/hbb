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
    default="deepflav_eval_newFlavSplit",
)
parser.add_argument(
    "-b", "--btag", default="deepflav", help="Btagging algorithm (deepflav or deepcsv)"
)
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")

parser.add_argument("--out-dir", default="btag_plots")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()

main_dir = f"/gpfs/ddn/cms/user/malucchi/hbb_out/{args.lep}/" + args.dir + "/Snapshots/"

var_list_max = [
    "btag_max",
    "atanhDNN_Score",
]
var_list_min = [
    "btag_min",
    "atanhDNN_Score",
]

def load_data(dir, variables_list):
    # list of all the files
    files = []
    print(dir)
    print(variables_list)

    for i, file in enumerate(glob.glob("%s/**/*.root" % dir, recursive=True)):
        if i < 10000:
            files.append(file)

    var_tot = np.array([])
    # open each file and get the Events tree using uproot
    for file in files:
        try:
            print(f"Loading file {file}")
            file = uproot.open(f"{file}:Events")
            variables = np.array(
                [
                    file[input].array(library="np")
                    for input in variables_list
                ]
            )
            var_tot = np.concatenate((var_tot, variables), axis=1)
        except uproot.exceptions.KeyInFileError:
            print(f"File {file} empty")
            continue

    print("var_tot", var_tot, len(var_tot))


    return var_tot

def plt_fts(out_dir, name, fig_handle, show):
    """Plot features
    :param    out_dir : string with the output directory
    :param    name : string with the name of the plot
    :param    fig_handle : figure handle
    """

    plt.xlabel("True positive rate", fontsize=20, loc="right")
    plt.ylabel("False positive rate ", fontsize=20, loc="top")

    minorLocator = MultipleLocator(0.05)
    ax = plt.gca()
    ax.xaxis.set_minor_locator(minorLocator)

    plt.grid(which="both")
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")

    plt.legend(loc="upper left", fontsize=20)

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
        bins=[100, 100],
        cmap=plt.cm.jet,
        density=True,
        range=[[0, 1], [0, 10]],
    )
    ax = plt.gca()
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=0, vmax=1.0)
    plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax
    ).set_label("Normalized counts", loc="center", fontsize=20)

    plt_fts(out_dir, f"btag_VS_DNN_{args.lep}_{args.btag}_ {type}", fig_handle, args.show)


if "__main__" == __name__:
    os.makedirs(args.out_dir, exist_ok=True)

    variables_max = load_data(main_dir, var_list_max)
    plotting_function(args.out_dir, variables_max, "max")

    variables_min = load_data(main_dir, var_list_min)
    plotting_function(args.out_dir, variables_min, "min")