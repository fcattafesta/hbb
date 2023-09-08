import numpy as np


def main():
    data = np.genfromtxt(
        "xsec.csv",
        delimiter=",",
        skip_header=1,
        names=[
            "sample",
            "xsec",
            "sumW",
            "fN",
            "nEvents",
            "effLumi",
        ],
        dtype=None,
        encoding="latin1",
    )

    data["sample"] = np.char.replace(data["sample"], "_", "\_")
    data["xsec"] = np.around(data["xsec"], 3)
    data["sumW"] = np.around(data["sumW"], 2)
    data["fN"] = np.around(data["fN"], 2)
    data["effLumi"] = np.around(data["effLumi"], 2)

    # Format data in latex table and save it to file and add two empty columns after the sample name
    with open("xsec.tex", "w") as f:
        f.write(
            "\\begin{tabular}{l|c|c|c|c|c|c}\n"
            + "Sample & & & Cross section  & Negative Fraction & Dataset Events & Effective luminosity \\\\\n"
            + "\\hline\n"
        )
        for i in range(len(data)):
            f.write(
                f"{data['sample'][i]} & & & \\num{{{data['xsec'][i]}}} & \\num{{{data['fN'][i]}}} & \\num{{{data['nEvents'][i]}}} & \\num{{{data['effLumi'][i]:e}}} \\\\\n"
            )
