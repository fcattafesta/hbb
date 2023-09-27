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
    default="deepflav_sys_eval_rescalebtag",
)
parser.add_argument(
    "-b", "--btag", default="DeepFlavour", help="Btagging algorithm (DeepFlavour or DeepCSV)"
)
parser.add_argument("-l", "--lep", default="mu", help="Lepton channel (mu or el)")

parser.add_argument("--out-dir", default="btag_files")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()


# main_dir = f"/gpfs/ddn/cms/user/malucchi/hbb_out/{args.lep}/{args.dir}/Snapshots/"
main_dir_mu = f"/scratchnvme/malucchi/hbb_out/mu/{args.dir}/Snapshots/"
main_dir_el = f"/scratchnvme/malucchi/hbb_out/el/{args.dir}/Snapshots/"

var_list = [
    "Dijets_mass",
    "atanhDNN_Score",
]


bins = [
    np.linspace(80,160, 60),
    [  # smooth rebin 10
        0.0,
        # 0.015,
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

    var_tot = np.array([[], [], []])
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
            # print(variables, variables.shape)

            # mask = np.array(variables[2, :]>2.829)
            # variables = variables[:, mask]
            var_tot = np.concatenate((var_tot, variables), axis=1)
        except uproot.exceptions.KeyInFileError:
            print(f"File {file} empty")
            continue

    # print("var_tot", var_tot, var_tot.shape)

    return var_tot


def plt_fts(out_dir, name, fig_handle, show, type):
    """Plot features
    :param    out_dir : string with the output directory
    :param    name : string with the name of the plot
    :param    fig_handle : figure handle
    """

    plt.xlabel("m_jj", fontsize=20, loc="right")
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
        f"mjj_VS_DNN_{args.btag}_{type}",
        fig_handle,
        args.show,
        type,
    )


if "__main__" == __name__:
    os.makedirs(args.out_dir, exist_ok=True)

    variables = load_data(main_dir_mu, main_dir_el, var_list)

    plotting_function(args.out_dir, variables, "fin")
