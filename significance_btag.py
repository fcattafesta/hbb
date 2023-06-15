import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
import mplhep as hep


parser = argparse.ArgumentParser()
parser.add_argument(
    "--mu",
    default="atanhDNN_Score___SR_mm_deepcsv_SignificanceSum_list.csv",
    help="file name for CSV in mu channel",
)
parser.add_argument(
    "--el",
    default="atanhDNN_Score___SR_ee_deepcsv_SignificanceSum_list.csv",
    help="file name for CSV in el channel",
)
parser.add_argument("--show", action="store_true")
args = parser.parse_args()

# tight, medium
btag_df_list = [1.144, 1.068]
btag_df_average = np.average(btag_df_list)
btag_df_std_dev = np.std(btag_df_list, ddof=0)

# el, mu
sig_df_list = [1.78, 1.86]
sig_df_average = np.average(sig_df_list)
sig_df_std_dev = np.std(sig_df_list, ddof=0)

# x, y, xerr, yerr
df_point = [btag_df_average, sig_df_average, btag_df_std_dev, sig_df_std_dev]
print(df_point)


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
                btag_rescale = float(
                    elem[1].replace("^M", "").replace("[", "").replace("]", "")
                )
                sig_sum = float(
                    elem[2].replace("^M", "").replace("[", "").replace("]", "")
                )

    print(btag_rescale_list)
    print(sig_sum_list)
    print(btag_rescale)
    print(sig_sum)

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
    fig_handle = plt.figure(figsize=(13, 10))
    plt.plot(btag_rescale_list_mu, sig_sum_list_mu, label="muon", color="blue")
    plt.plot(
        btag_rescale_list_el, sig_sum_list_el, label="electron", color="dodgerblue"
    )

    # fill between the two lines
    plt.fill_between(
        btag_rescale_list_mu,
        sig_sum_list_mu,
        sig_sum_list_el,
        color="lightblue",
        alpha=0.5,
        # label="difference",
    )

    # compute the average of the two channels and plot it
    sig_sum_list_average = [
        np.average([x, y]) for x, y in zip(sig_sum_list_mu, sig_sum_list_el)
    ]
    # compute the standard deviation of the two channels
    sig_sum_list_std_dev = [
        np.std([x, y], ddof=0) for x, y in zip(sig_sum_list_mu, sig_sum_list_el)
    ]
    # plot the average
    plt.plot(
        btag_rescale_list_mu,
        sig_sum_list_average,
        label="average",
        color="black",
        linewidth=2,
        linestyle="--",
    )
    # fill between the average and the two lines
    plt.fill_between(
        btag_rescale_list_mu,
        sig_sum_list_average-sig_sum_list_std_dev,
        sig_sum_list_average+sig_sum_list_std_dev,
        color="yellow",
        alpha=0.5,
        label="one sigma",
    )


    # plt.plot(btag_rescale_mu, sig_sum_mu, "o", label="muon channel")
    # plt.plot(btag_rescale_el, sig_sum_el, "o", label="electron channel")

    plt.plot(
        btag_rescale_list_mu[0],
        sig_sum_list_mu[0],
        "o",
        label="DeepCSV muon",
        color="blue",
    )
    plt.plot(
        btag_rescale_list_el[0],
        sig_sum_list_el[0],
        "o",
        label="DeepCSV electron",
        color="dodgerblue",
    )

    plt.errorbar(
        df_point[0],
        df_point[1],
        xerr=df_point[2],
        yerr=df_point[3],
        fmt="o",
        label="DeepFlav",
        color="red",
    )

    plt.xlabel("btag efficiency gain", fontsize=20, loc="right")
    plt.ylabel("significance", fontsize=20, loc="top")
    plt.grid(which="both")
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")
    plt.legend()  # loc="upper left", fontsize=20)
    plt.savefig("btag_rescale_vs_significance_sum.png")
    if args.show:
        plt.show()


if __name__ == "__main__":
    btag_rescale_list_mu, sig_sum_list_mu, btag_rescale_mu, sig_sum_mu = load_data(
        args.mu
    )
    btag_rescale_list_el, sig_sum_list_el, btag_rescale_el, sig_sum_el = load_data(
        args.el
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

    # NOTE : instead of using the average of the two channels, we can also use the sum in quadrature ?
