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


sig_list = [(x**2 + y**2) / 1 for x, y in zip(sig_list_el, sig_list_mu)]

print("sig_list", sig_list)

print("fractions_max", fractions_max)
print("fractions_min", fractions_min)


def read_txt_file(filename, name):
    tpr_list = []
    with open(filename, "r") as f:
        current_network = None
        for line in f:
            if line.startswith("network:"):
                current_network = line.split(":")[1].strip()
            elif line.startswith("tpr:"):
                tpr_value = float(line.split(":")[1])
                if name in current_network:
                    tpr_list.append(tpr_value)
    return tpr_list

roc_file = "sb_discriminator/roc_curve/roc_data.txt"
roc_m100_file= "sb_discriminator/roc_curve/roc_data_m100.txt"

eff_csv_list_wp = read_txt_file(roc_file, "DeepCSV")
eff_df_list_wp = read_txt_file(roc_file, "DeepFlav")
# eff_dfCMSSW_list_wp = read_txt_file(roc_m100_file, "DeepFlavCMSSW")
# pn_list_wp = read_txt_file(roc_m100_file, "PN")
# pe_list_wp = read_txt_file(roc_m100_file, "PE")

print("eff_df_list_wp", eff_df_list_wp)
print("eff_csv_list_wp", eff_csv_list_wp)

#NOTE create correct fractions for all btag bins

# wp L, M, T, UT

# eff_csv_list_wp = [0.9127, 0.7903, 0.6014, 0.5309]
# eff_df_list_wp = [0.9405, 0.8440, 0.6883, 0.6295]

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
    rescale_fin = np.average(rescale_list, weights=[1, 1])
    rescale_err = np.std(rescale_list, ddof=0)
    print("rescale_fin", rescale_fin)
    print("rescale_err", rescale_err)

    return rescale_fin, rescale_err


print("deepFlav")
rescale_fin_df, rescale_err_df = rescale(btag_df_list_wp)
print("particleNet")
rescale_fin_pn, rescale_err_pn = rescale(btag_pn_list_wp)
print("particleEdge")
rescale_fin_pe, rescale_err_pe = rescale(btag_pe_list_wp)

# rescale_fin_pn = (btag_pn_list_wp[-1] + btag_pn_list_wp[-2]) / 2
# rescale_fin_pe = (btag_pe_list_wp[-1] + btag_pe_list_wp[-2]) / 2


# mu, el
sig_df_list = [1.85, 1.63] if args.sf else [1.99, 1.78]
sig_df_average = np.average(sig_df_list)
sig_df_std_dev = np.std(sig_df_list, ddof=0)

# sig_df_sum = np.sum(np.array(sig_df_list) ** 2, axis=None)
# sig_df_sum = np.sqrt(sig_df_sum)


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

    csv_sig_average = sig_sum_list_average[0]

    csv_sig_mu = sig_sum_list_mu[0]
    csv_sig_el = sig_sum_list_el[0]
    print("csv_sig_mu", csv_sig_mu)
    print("csv_sig_el", csv_sig_el)

    sig_sum_list_av = [
        np.average([x / csv_sig_mu, y / csv_sig_el])
        for x, y in zip(sig_sum_list_mu, sig_sum_list_el)
    ]

    sig_sum_list_std = [
        np.std([x / csv_sig_mu, y / csv_sig_el], ddof=0)
        for x, y in zip(sig_sum_list_mu, sig_sum_list_el)
    ]

    # csv_spline = splrep(btag_rescale_list, sig_sum_list_average, s=0)
    csv_spline_av = splrep(btag_rescale_list, sig_sum_list_av, s=0)
    csv_spline_std = splrep(btag_rescale_list, sig_sum_list_std, s=0)

    # # plot the average
    # plt.plot(
    #     btag_rescale_list,
    #     sig_sum_list_average / csv_sig_average,
    #     label="DeepCSV rescaled",
    #     color="red",
    #     linewidth=2,
    #     linestyle="--",
    # )
    # # fill between the average and the two lines
    # plt.fill_between(
    #     btag_rescale_list,
    #     np.subtract(sig_sum_list_average, sig_sum_list_std_dev) / csv_sig_average,
    #     np.add(sig_sum_list_average, sig_sum_list_std_dev) / csv_sig_average,
    #     color="salmon",
    #     alpha=0.5,
    #     # label=r"$1 \sigma$",
    # )

    # plt.plot(
    #     btag_rescale_list,
    #     np.array(sig_sum_list_mu) / csv_sig_mu,
    #     #color="lime",
    #     alpha=0.5,
    #     label=r"$\mu$",
    # )

    # plt.plot(
    #     btag_rescale_list,
    #     np.array(sig_sum_list_el) / csv_sig_el,
    #     #color="lime",
    #     alpha=0.5,
    #     label=r"$el$",
    # )

    plt.plot(
        btag_rescale_list,
        np.array(sig_sum_list_av),
        color="red",
        label=r"DeepCSV rescaled",
        linewidth=2,
        linestyle="--",
    )
    plt.fill_between(
        btag_rescale_list,
        np.subtract(sig_sum_list_av, sig_sum_list_std),
        np.add(sig_sum_list_av, sig_sum_list_std),
        color="salmon",
        alpha=0.5,
        # label=r"$1 \sigma$",
    )

    plt.plot(
        1,  # btag_rescale_list[0],
        1,  # sig_sum_list_average[0] / csv_sig_average,
        "o",
        label="DeepCSV",
        color="red",
    )

    # plt.errorbar(
    #     df_point[0],
    #     df_point[1] / csv_sig_average,
    #     xerr=df_point[2],
    #     yerr=df_point[3] / csv_sig_average,
    #     fmt="o",
    #     label="DeepFlav",
    #     color="purple",
    # )

    sig_ratio = [sig_df_list[0] / csv_sig_mu, sig_df_list[1] / csv_sig_el]
    sig_ratio_av = np.average(sig_ratio)
    sig_ratio_std_dev = np.std(sig_ratio, ddof=0)

    plt.errorbar(
        df_point[0],
        sig_ratio_av,
        xerr=df_point[2],
        yerr=sig_ratio_std_dev,
        fmt="o",
        label="DeepFlav",
        color="blue",
    )

    plt.vlines(
        x=rescale_fin_pn,
        ymin=1,
        ymax=1.3,  # BSpline(*csv_spline_av)(rescale_fin_pn),
        # label="ParticleNet",
        color="black",
        linestyle="--",
    )

    plt.vlines(
        x=rescale_fin_pe,
        ymin=1,
        ymax=1.3,  # BSpline(*csv_spline_av)(rescale_fin_pe),
        # label="ParticleEdge",
        color="green",
        linestyle="--",
    )

    plt.plot(
        rescale_fin_pn,
        BSpline(*csv_spline_av)(rescale_fin_pn),
        "o",
        label="ParticleNet",
        color="black",
    )

    plt.plot(
        rescale_fin_pe,
        BSpline(*csv_spline_av)(rescale_fin_pe),
        "o",
        label="ParticleEdge",
        color="green",
    )
    print(BSpline(*csv_spline_av)(rescale_fin_pe))

    # plt.errorbar(
    #     rescale_fin_pn,
    #     BSpline(*csv_spline_av)(rescale_fin_pn),
    #     xerr=rescale_err_pn,
    #     yerr=BSpline(*csv_spline_std)(rescale_fin_pn),
    #     fmt="o",
    #     label="ParticleNet",
    #     color="black",

    # )

    # plt.errorbar(
    #     rescale_fin_pe,
    #     BSpline(*csv_spline_av)(rescale_fin_pe),
    #     xerr=rescale_err_pe,
    #     yerr=BSpline(*csv_spline_std)(rescale_fin_pe),
    #     fmt="o",
    #     label="ParticleEdge",
    #     color="green",
    # )

    # plt.plot(
    #     1.16,
    #     BSpline(*csv_spline_av)(1.16)+BSpline(*csv_spline_std)(1.16),
    #     marker=".",
    #     label="el",
    #     color="cyan",
    # )

    # plt.plot(
    #     1.16,
    #     BSpline(*csv_spline_av)(1.16)-BSpline(*csv_spline_std)(1.16),
    #     marker=".",
    #     label="$\mu$",
    #     color="gold",
    # )

    plt.xlabel(r"$\varepsilon$", fontsize=20, loc="right")
    plt.ylabel("Sig / Sig DeepCSV", fontsize=20, loc="top")
    plt.grid(which="both")
    hep.style.use("CMS")
    hep.cms.label("Preliminary")
    hep.cms.label(year="UL18")
    plt.legend()  # loc="upper left", fontsize=20)
    plt.savefig(
        f"{args.out_dir}/plot_btag_vs_significance.png", bbox_inches="tight", dpi=300
    )
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
