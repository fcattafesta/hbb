import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse
import mplhep as hep
import os
import math

parser = argparse.ArgumentParser()
parser.add_argument(
    "--sf",
    default=False,
    action="store_true",
    help="use scale factors",
)
parser.add_argument(
    "--frac-el",
    default="btag_files/fractions_el.csv",
    help="file name with fractions in el channel",
)
parser.add_argument(
    "--frac-mu",
    default="btag_files/fractions_mu.csv",
    help="file name with fractions in mu channel",
)
parser.add_argument("--out-dir", default="btag_files")
parser.add_argument("--show", action="store_true")
args = parser.parse_args()

if args.sf:
    sf="_sf"
else:
    sf=""

sig_el_file = f"btag_files/atanhDNN_Score___SR_ee_deepcsv_SignificanceSum_list{sf}.csv"
sig_mu_file = f"btag_files/atanhDNN_Score___SR_mm_deepcsv_SignificanceSum_list{sf}.csv"

def load_data_csv(file):
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

    # print(btag_rescale_list)
    # print(sig_sum_list)
    # print(btag_rescale)
    # print(sig_sum)
    # print(fractions_max)
    # print(fractions_min)
    #print("sig_list", sig_list)

    return (
        btag_rescale_list,
        sig_sum_list,
        btag_rescale,
        sig_sum,
        fractions_max,
        fractions_min,
        sig_list,
    )


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

_, _, _, _, fractions_max_el, fractions_min_el, _ = load_data_csv(args.frac_el)
_, _, _, _, _, _, sig_list_el = load_data_csv(sig_el_file)
_, _, _, _, fractions_max_mu, fractions_min_mu, _ = load_data_csv(args.frac_mu)
_, _, _, _, _, _, sig_list_mu = load_data_csv(sig_mu_file)

fractions_max=[]
fractions_min=[]
for i in range(len(fractions_max_el)):
    frac_max=[(x+y)/2 for x, y in zip(fractions_max_el[i], fractions_max_mu[i])]
    fractions_max.append(frac_max)
    frac_min=[(x+y)/2 for x, y in zip(fractions_min_el[i], fractions_min_mu[i])]
    fractions_min.append(frac_min)


sig_list = [math.sqrt(x**2+y**2) for x, y in zip(sig_list_el, sig_list_mu)]
sig_list=[(x+y)/2 for x, y in zip(sig_list_el, sig_list_mu)]

print("sig_list", sig_list)

print("fractions_max", fractions_max)
print("fractions_min", fractions_min)

# # sum of fractions
# fractions_max = [sum(lst) for lst in zip(*fractions_max)]
# fractions_min = [sum(lst) for lst in zip(*fractions_min)]

# fractions_max = [x / sum(fractions_max) for x in fractions_max]
# fractions_min = [x / sum(fractions_min) for x in fractions_min]

# fractions_average = [(x + y ) / 2 for x, y in zip(fractions_max, fractions_min)]

# print("fractions_max", fractions_max)
# print("fractions_min", fractions_min)
# print("fractions_average", fractions_average)

# wp L, M, T, UT
eff_csv_list_wp = [0.9127, 0.7903, 0.6014, 0.5309]
eff_df_list_wp = [0.9405, 0.8440, 0.6883, 0.6295]
btag_df_list_wp = [1 + (x - y) / y for x, y in zip(eff_df_list_wp, eff_csv_list_wp)]

print("btag_df_list_wp", btag_df_list_wp)

rescale_list=[]
for frac in [fractions_max, fractions_min]:
    rescale=0
    for bin in range(len(frac)):
        eff_sum = 0
        for wp in range(len(frac[bin])):
            print("eff_sum", frac[bin][wp] * btag_df_list_wp[wp])
            eff_sum += frac[bin][wp] * btag_df_list_wp[wp]
        print("rescale", eff_sum * sig_list[bin])
        rescale += eff_sum * sig_list[bin]

    rescale /= sum(sig_list)
    rescale_list.append(rescale)

print("rescale_list", rescale_list)
rescale_fin=np.average(rescale_list)
rescale_err=np.std(rescale_list, ddof=0)
print("rescale_fin", rescale_fin)
print("rescale_err", rescale_err)

#rescale_fin = 1 + (eff_df_list_wp[-1]-eff_csv_list_wp[-1])/eff_csv_list_wp[-1]




# btag_df_list = [1 + (x - y) / y for x, y in zip(eff_df_list, eff_csv_list)]
# btag_df_average = np.average(btag_df_list)
# btag_df_std_dev = np.std(btag_df_list, ddof=0)

btag_df_list = [
    (1 + (x - y) / y)  # * z
    for x, y in zip(eff_df_list_wp, eff_csv_list_wp)  # , fractions_average)
]

#print("btag_df_list", btag_df_list)
btag_df_average = np.sum(btag_df_list)
#print("btag_df_average", btag_df_average)
btag_df_std_dev = np.std(btag_df_list, ddof=0)


# mu, el
sig_df_list = [1.85, 1.63] if args.sf else [1.99, 1.78]
sig_df_average = np.average(sig_df_list)
sig_df_std_dev = np.std(sig_df_list, ddof=0)

sig_df_sum = np.sum(np.array(sig_df_list)**2, axis=None)
sig_df_sum = np.sqrt(sig_df_sum)


# x, y, xerr, yerr
df_point = [rescale_fin, sig_df_average, rescale_err, sig_df_std_dev]
#print(df_point)

btag_df_wp = {
    wp: [b, sig_df_average, 0, sig_df_std_dev]
    for wp, b in zip(
        ["Loose WP", "Medium WP", "Tight WP", "UltraTight WP"], btag_df_list_wp
    )
}
#print("btag_df_wp", btag_df_wp)

wp_color = {
    "Loose WP": "darkblue",
    "Medium WP": "cornflowerblue",
    "Tight WP": "blue",
    "UltraTight WP": "cyan",
}


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

    #print(sig_sum_list_average)
    #print(sig_sum_list_std_dev)
    csv_sig_av = sig_sum_list_average[0]

    sig_sum_list_sum = np.array(sig_sum_list_mu)**2 + np.array(sig_sum_list_el)**2
    sig_sum_list_sum = np.sqrt(sig_sum_list_sum)
    csv_sig_sum = sig_sum_list_sum[0]

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
    plt.errorbar(
        df_point[0],
        df_point[1] / csv_sig_av,
        xerr=df_point[2],
        yerr=df_point[3] / csv_sig_av,
        fmt="o",
        label="DeepFlav",
        color="blue",
    )

    # for wp, point in btag_df_wp.items():
    #     if False:
    #         plt.errorbar(
    #             point[0],
    #             point[1] / csv_sig_sum,
    #             xerr=point[2],
    #             yerr=point[3] / csv_sig_sum,
    #             fmt="o",
    #             label=f"DeepFlav {wp}",
    #             color=wp_color[wp],
    #         )

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
        btag_rescale_mu,
        sig_sum_mu,
        *_,
    ) = load_data_csv(sig_mu_file)
    (
        btag_rescale_list_el,
        sig_sum_list_el,
        btag_rescale_el,
        sig_sum_el,
        *_,
    ) = load_data_csv(sig_el_file)
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
