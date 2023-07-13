unc_btag = [
    "hf",
    "lf",
    "hfstats1",
    "hfstats2",
    "lfstats1",
    "lfstats2",
    "cferr1",
    "cferr2",
]

btag_sys = ["btagWeight_" + x + y for x in unc_btag for y in ["Up", "Down"]]
jet_btag_sys = ["Jet_btagWeight_" + y + x for x in unc_btag for y in ["up_", "down_"]]