import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
import mplhep as hep
import os

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
parser.add_argument("--out-dir", default="btag_plots")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()


# sampling
eff_csv_list = [
    0.6014,
    0.6658,
    0.7005,
    0.7227,
    0.7399,
    0.7536,
    0.7647,
    0.7745,
    0.7831,
    0.7903,
]
eff_df_list = [
    0.6883,
    0.7423,
    0.7715,
    0.7896,
    0.8035,
    0.8151,
    0.8242,
    0.8317,
    0.8381,
    0.8440,
]

# wp
eff_csv_list_wp = [0.3594, 0.6014, 0.7903, 0.9127]
eff_df_list_wp = [0.4931, 0.6883, 0.8440, 0.9405]
btag_df_list_wp = [1 + (x - y) / y for x, y in zip(eff_df_list_wp, eff_csv_list_wp)]


# get the difference between the two lists
btag_df_list = [1 + (x - y) / y for x, y in zip(eff_df_list, eff_csv_list)]

btag_df_average = np.average(btag_df_list)
btag_df_std_dev = np.std(btag_df_list, ddof=0)

# mu, el
sig_df_list = [1.99, 1.78]
sig_df_average = np.average(sig_df_list)
sig_df_std_dev = np.std(sig_df_list, ddof=0)

# x, y, xerr, yerr
df_point = [btag_df_average, sig_df_average, btag_df_std_dev, sig_df_std_dev]
print(df_point)

btag_df_wp = {
    wp: [b, sig_df_average, 0, sig_df_std_dev]
    for wp, b in zip(["1e-4", "Tight WP", "1e-2", "1e-1"], btag_df_list_wp)
}
print("btag_df_wp", btag_df_wp)

wp_color = {
    "1e-4": "cyan",
    "Tight WP": "blue",
    "1e-2": "cornflowerblue",
    "1e-1": "darkblue",
}


def load_data_csv(file):
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

    # compute the average of the two channels and plot it
    sig_sum_list_average = [
        np.average([x, y]) for x, y in zip(sig_sum_list_mu, sig_sum_list_el)
    ]
    # compute the standard deviation of the two channels
    sig_sum_list_std_dev = [
        np.std([x, y], ddof=0) for x, y in zip(sig_sum_list_mu, sig_sum_list_el)
    ]

    print(sig_sum_list_average)
    print(sig_sum_list_std_dev)
    csv_sig_av = sig_sum_list_average[0]

    # plt.plot(
    #     btag_rescale_list_mu,
    #     sig_sum_list_mu / csv_sig_av,
    #     label="DeepCSV muon",
    #     color="darkred",
    # )
    # plt.plot(
    #     btag_rescale_list_el,
    #     sig_sum_list_el / csv_sig_av,
    #     label="DeepCSV electron",
    #     color="orange",
    # )

    # plot the average
    plt.plot(
        btag_rescale_list_mu,
        sig_sum_list_average / csv_sig_av,
        label="DeepCSV rescaled",
        color="red",
        linewidth=2,
        linestyle="--",
    )
    # fill between the average and the two lines
    plt.fill_between(
        btag_rescale_list_mu,
        np.subtract(sig_sum_list_average, sig_sum_list_std_dev) / csv_sig_av,
        np.add(sig_sum_list_average, sig_sum_list_std_dev) / csv_sig_av,
        color="salmon",
        alpha=0.5,
        # label=r"$1 \sigma$",
    )

    # plt.plot(btag_rescale_mu, sig_sum_mu, "o", label="muon channel")
    # plt.plot(btag_rescale_el, sig_sum_el, "o", label="electron channel")

    plt.plot(
        btag_rescale_list_mu[0],
        sig_sum_list_average[0] / csv_sig_av,
        "o",
        label="DeepCSV",
        color="red",
    )
    # plt.errorbar(
    #     df_point[0],
    #     df_point[1] / csv_sig_av,
    #     xerr=df_point[2],
    #     yerr=df_point[3] / csv_sig_av,
    #     fmt="o",
    #     label="DeepFlav",
    #     color="blue",
    # )

    for wp, point in btag_df_wp.items():
        if wp == "Tight WP":
            plt.errorbar(
                point[0],
                point[1] / csv_sig_av,
                xerr=point[2],
                yerr=point[3] / csv_sig_av,
                fmt="o",
                label=f"DeepFlav {wp}",
                color=wp_color[wp],
            )

    plt.xlabel("btag TPR / btag TPR DeepCSV", fontsize=20, loc="right")
    plt.ylabel("Sig / Sig DeepCSV", fontsize=20, loc="top")
    plt.grid(which="both")
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")
    plt.legend()  # loc="upper left", fontsize=20)
    plt.savefig(f"{args.out_dir}/plot_btag_vs_significance.png")
    if args.show:
        plt.show()


if __name__ == "__main__":
    os.makedirs(args.out_dir, exist_ok=True)
    btag_rescale_list_mu, sig_sum_list_mu, btag_rescale_mu, sig_sum_mu = load_data_csv(
        args.mu
    )
    btag_rescale_list_el, sig_sum_list_el, btag_rescale_el, sig_sum_el = load_data_csv(
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
