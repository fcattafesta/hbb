import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
import mplhep as hep
import os
import math
from scipy.interpolate import splrep, BSpline

parser = argparse.ArgumentParser()
parser.add_argument(
    "--sf",
    default=False,
    action="store_true",
    help="use scale factors",
)
parser.add_argument(
    "--frac-el",
    default="btag_files/fractions_el_flav.csv",
    help="file name with fractions in el channel",
)
parser.add_argument(
    "--frac-mu",
    default="btag_files/fractions_mu_flav.csv",
    help="file name with fractions in mu channel",
)
parser.add_argument("--out-dir", default="btag_files")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()


def load_data(file):
    sig_list = []
    btag_rescale_list = []
    sig_sum_list = []
    btag_rescale = 0
    sig_sum = 0
    fractions_max = []
    fractions_min = []
    with open(file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
        for elem in data:
            if "Significance_list" in elem:
                sig_list = elem[1].replace("^M", "").replace("[", "").replace("]", "")
                sig_list = [float(x) for x in sig_list.split(",")]
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
            elif "fractions_max" in elem:
                fractions_max_string = (
                    elem[1].replace("^M", "").replace("[[", "[").replace("]]", "]")
                )
                fractions_max = []
                for x in fractions_max_string.split("], "):
                    fractions_max.append([])
                    for y in x.split(", "):
                        fractions_max[-1].append(
                            float(y.replace("[", "").replace("]", ""))
                        )
            elif "fractions_min" in elem:
                fractions_min_string = (
                    elem[1].replace("^M", "").replace("[[", "[").replace("]]", "]")
                )
                fractions_min = []
                for x in fractions_min_string.split("], "):
                    fractions_min.append([])
                    for y in x.split(", "):
                        fractions_min[-1].append(
                            float(y.replace("[", "").replace("]", ""))
                        )

    return (
        btag_rescale_list,
        sig_sum_list,
        btag_rescale,
        sig_sum,
        fractions_max,
        fractions_min,
        sig_list,
    )


def rescale(btag_list):
    rescale_list = []
    for frac in [fractions_max, fractions_min]:
        rescale = 0
        for bin in range(len(frac)):
            eff_sum = 0
            for wp in range(len(frac[bin])):
                eff_sum += frac[bin][wp] * btag_list[wp]
            rescale += eff_sum * sig_list[bin]

        rescale /= sum(sig_list)
        rescale_list.append(rescale)

    print("rescale_list", rescale_list)
    rescale_fin = np.average(rescale_list)
    rescale_err = np.std(rescale_list, ddof=0)
    print("rescale_fin", rescale_fin)
    print("rescale_err", rescale_err)

    return rescale_fin, rescale_err


if args.sf:
    sf = "_sf"
else:
    sf = ""

sig_csv_el_file = (
    f"btag_files/atanhDNN_Score___SR_ee_deepcsv_SignificanceSum_list{sf}.csv"
)
sig_csv_mu_file = (
    f"btag_files/atanhDNN_Score___SR_mm_deepcsv_SignificanceSum_list{sf}.csv"
)
sig_flav_el_file = (
    f"btag_files/atanhDNN_Score___SR_ee_deepflav_SignificanceSum_list{sf}.csv"
)
sig_flav_mu_file = (
    f"btag_files/atanhDNN_Score___SR_mm_deepflav_SignificanceSum_list{sf}.csv"
)

_, _, _, _, fractions_max_el, fractions_min_el, _ = load_data(args.frac_el)
_, _, _, _, _, _, sig_list_el = load_data(sig_flav_el_file)
_, _, _, _, fractions_max_mu, fractions_min_mu, _ = load_data(args.frac_mu)
_, _, _, _, _, _, sig_list_mu = load_data(sig_flav_mu_file)

fractions_max = []
fractions_min = []
for i in range(len(fractions_max_el)):
    frac_max = [(x + y) / 2 for x, y in zip(fractions_max_el[i], fractions_max_mu[i])]
    fractions_max.append(frac_max)
    frac_min = [(x + y) / 2 for x, y in zip(fractions_min_el[i], fractions_min_mu[i])]
    fractions_min.append(frac_min)


sig_list = [(x + y) / 2 for x, y in zip(sig_list_el, sig_list_mu)]

print("sig_list", sig_list)

print("fractions_max", fractions_max)
print("fractions_min", fractions_min)


# wp L, M, T, UT
eff_csv_list_wp = [0.9127, 0.7903, 0.6014, 0.5309]
eff_df_list_wp = [0.9405, 0.8440, 0.6883, 0.6295]

eff_dfCMSSW_list_wp = [0.9340, 0.8213, 0.6547, 0.5966]
pn_list_wp = [0.9463, 0.8504, 0.7146, 0.6656]
pe_list_wp = [0.9519, 0.8673, 0.7458, 0.7069]

eff_pn_list_wp = [
    y * z / x for x, y, z in zip(eff_dfCMSSW_list_wp, pn_list_wp, eff_df_list_wp)
]
print("eff_pn_list_wp", eff_pn_list_wp)
eff_pe_list_wp = [
    y * z / x for x, y, z in zip(eff_dfCMSSW_list_wp, pe_list_wp, eff_df_list_wp)
]
print("eff_pe_list_wp", eff_pe_list_wp)

btag_df_list_wp = [x / y for x, y in zip(eff_df_list_wp, eff_csv_list_wp)]
btag_pn_list_wp = [x / y for x, y in zip(eff_pn_list_wp, eff_csv_list_wp)]
btag_pe_list_wp = [x / y for x, y in zip(eff_pe_list_wp, eff_csv_list_wp)]

print("btag_df_list_wp", btag_df_list_wp)
print("btag_pn_list_wp", btag_pn_list_wp)
print("btag_pe_list_wp", btag_pe_list_wp)


rescale_fin_df, rescale_err_df = rescale(btag_df_list_wp)
rescale_fin_pn, rescale_err_pn = rescale(btag_pn_list_wp)
rescale_fin_pe, rescale_err_pe = rescale(btag_pe_list_wp)


# mu, el
sig_df_list = [1.85, 1.63] if args.sf else [1.99, 1.78]
sig_df_average = np.average(sig_df_list)
sig_df_std_dev = np.std(sig_df_list, ddof=0)

sig_df_sum = np.sum(np.array(sig_df_list) ** 2, axis=None)
sig_df_sum = np.sqrt(sig_df_sum)


# x, y, xerr, yerr
df_point = [rescale_fin_df, sig_df_average, rescale_err_df, sig_df_std_dev]
print("df_point", df_point)


def plot_data(
    btag_rescale_list,
    sig_sum_list_mu,
    sig_sum_list_el,
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

    csv_sig_av = sig_sum_list_average[0]

    csv_spline = splrep(btag_rescale_list, sig_sum_list_average, s=0)

    # plot the average
    plt.plot(
        btag_rescale_list,
        sig_sum_list_average / csv_sig_av,
        label="DeepCSV rescaled",
        color="red",
        linewidth=2,
        linestyle="--",
    )
    # fill between the average and the two lines
    plt.fill_between(
        btag_rescale_list,
        np.subtract(sig_sum_list_average, sig_sum_list_std_dev) / csv_sig_av,
        np.add(sig_sum_list_average, sig_sum_list_std_dev) / csv_sig_av,
        color="salmon",
        alpha=0.5,
        # label=r"$1 \sigma$",
    )

    plt.plot(
        btag_rescale_list[0],
        sig_sum_list_average[0] / csv_sig_av,
        "o",
        label="DeepCSV",
        color="red",
    )
    plt.errorbar(
        df_point[0],
        df_point[1] / csv_sig_av,
        xerr=df_point[2],
        yerr=df_point[3] / csv_sig_av,
        fmt="o",
        label="DeepFlav",
        color="blue",
    )
    plt.errorbar(
        rescale_fin_pn,
        BSpline(*csv_spline)(rescale_fin_pn) / csv_sig_av,
        xerr=rescale_err_pn,
        yerr=0,
        fmt="o",
        label="ParticleNet",
        color="black",
    )

    plt.errorbar(
        rescale_fin_pe,
        BSpline(*csv_spline)(rescale_fin_pe) / csv_sig_av,
        xerr=rescale_err_pe,
        yerr=0,
        fmt="o",
        label="ParticleEdge",
        color="green",
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

    (
        btag_rescale_list_mu,
        sig_sum_list_mu,
        *_,
    ) = load_data(sig_csv_mu_file)
    (
        btag_rescale_list_el,
        sig_sum_list_el,
        *_,
    ) = load_data(sig_csv_el_file)
    plot_data(
        btag_rescale_list_mu,
        sig_sum_list_mu,
        sig_sum_list_el,
    )

    # NOTE : instead of using the average of the two channels, we can also use the sum in quadrature ?
