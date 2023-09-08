import numpy as np
from latex_table import main

names = [
    "DY_0To50",
    "DY_50To100",
    "DY_100To250",
    "DY_250To400",
    "DY_400To650",
    "DY_650ToInf",
]

names = np.char.replace(names, "_", "\_")

nEvents = [196207761, 122967660, 79527324, 24195330, 3936102, 3994997]

fN = [
    0.245855253245936,
    0.293318126844675,
    0.299897094134366,
    0.290967741935484,
    0.289340101522843,
    0.1,
]

xsec = [1341.42, 359.52, 88.36, 3.52, 0.49, 0.05]

lumieff = np.around(np.array(nEvents) / np.array(xsec) * (1 - 2 * np.array(fN)) ** 2, 2)
fN = np.around(np.array(fN), 2)

main()

# fromat data in latex table and save it to xsec.tex without overwriting and add two empty columns after the sample name
with open("xsec.tex", "a") as f:
    for i in range(len(names)):
        f.write(
            f"{names[i]} & & & \\num{{{xsec[i]}}} & \\num{{{fN[i]}}} & \\num{{{nEvents[i]}}} & \\num{{{lumieff[i]:e}}} \\\\\n"
        )
    f.write("\\end{tabular}")
