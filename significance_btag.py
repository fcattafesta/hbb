import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    "--fileCSV-mu",
    default="input.csv",
)
parser.add_argument(
    "--fileCSV-el",
    default="input.csv",
)
parser.add_argument("--show", action="store_true")
args = parser.parse_args()


def load_data(file):
    with open(file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
        for elem in data:
            if "btag_rescale" in elem:
                btag_rescale_list = (
                    elem[1].replace("^M", "").replace("[", "").replace("]", "")
                )
                btag_rescale_list = [float(x) for x in btag_rescale_list.split(",")]
            elif "SignificanceSum" in elem:
                sig_sum_list = (
                    elem[1].replace("^M", "").replace("[", "").replace("]", "")
                )
                sig_sum_list = [float(x) for x in sig_sum_list.split(",")]
            elif "RescaleFactors" in elem:
                btag_rescale = (
                    float(elem[1].replace("^M", "").replace("[", "").replace("]", ""))
                )
                sig_sum = float(elem[2].replace("^M", "").replace("[", "").replace("]", ""))

    print(btag_rescale_list)
    print(sig_sum_list)
    return btag_rescale_list, sig_sum_list, btag_rescale, sig_sum


def plot_data(
    btag_rescale_list_mu,
    sig_sum_list_mu,
    btag_rescale_mu,
    sig_sum_mu,
    btag_rescale_list_el,
    sig_sum_list_el,
    btag_rescale_el,
    sig_sum_el,
):
    plt.plot(btag_rescale_list_mu, sig_sum_list_mu, label="muon channel")
    plt.plot(btag_rescale_list_el, sig_sum_list_el, label="electron channel")

    plt.plot(btag_rescale_mu, sig_sum_mu, "o", label="muon channel")
    plt.plot(btag_rescale_el, sig_sum_el, "o", label="electron channel")

    plt.xlabel("btag rescale")
    plt.ylabel("significance sum")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    btag_rescale_list_mu, sig_sum_list_mu, btag_rescale_mu, sig_sum_mu = load_data(
        args.fileCSV_mu
    )
    btag_rescale_list_el, sig_sum_list_el, btag_rescale_el, sig_sum_el = load_data(
        args.fileCSV_el
    )
    plot_data(
        btag_rescale_list_mu,
        sig_sum_list_mu,
        btag_rescale_mu,
        sig_sum_mu,
        btag_rescale_list_el,
        sig_sum_list_el,
        btag_rescale_el,
        sig_sum_el,
    )
    #TODO: the point to plot is not the one I put
    # but is the significance of the deepflav point

    # add deepflav files with significance for mu and el and btag gain of the 2 wp

    # draw error band?
