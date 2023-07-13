# TODO: separate systematics as
# shape only (remove normalization effects)
# per group
# per sample

# default is correlated among all samples
# and correlated nuisance for norm+shape

from btagging_sys import btag_sys


def systematicGrouping(background, signal, jesList, year):
    legendGrouping = {}
    legendGrouping.update(background)
    legendGrouping.update(signal)

    DY_ = [
        "DYZpt-0To50",
        "DYZpt-50To100",
        "DYZpt-100To250",
        "DYZpt-250To400",
        "DYZpt-400To650",
        "DYZpt-650ToInf",
    ]

    DY = [x + y for x in DY_ for y in ["_bb", "_b", "_c", "_udsg"]]

    VV_ = [
        "WWTo2L2Nu",
        "WZTo2Q2L",
        "WZTo3LNu",
        "ZZTo2L2Nu",
        "ZZTo2Q2L",
        "ZZTo4L",
    ]
    VV = [x + y for x in VV_ for y in ["_bb", "_b", "_c", "_udsg"]]

    TT = ["TTTo2L2Nu", "TTToHadronic", "TTToSemiLeptonic"]
    ST = [
        "ST_tW_antitop_5f_NFHD",
        "ST_tW_top_5f_NFHD",
        "ST_tW_antitop_5f_ID",
        "ST_tW_top_5f_ID",
        "ST_t-channel_antitop_4f_ID",
        "ST_t-channel_top_4f_ID",
        "ST_t-channel_antitop_5f_ID",
        "ST_s-channel_4f_LD",
    ]

    Hbb = ["ZH", "ggZH"]

    systematicDetail = {
        "lumi": {"type": "lnN", "value": 1.025},
        "BR_Hbb": {
            "type": "lnN",
            "decorrelate": {"Hbb": Hbb},
            "additionalNormalizations": [],
            "groupValues": {"Hbb": 1.005},
        },
        "XSecAndNorm": {
            "type": "lnN",
            "additionalNormalizations": [],
            "decorrelate": {
                "ZH": ["ZH"],
                "ggZH": ["ggZH"],
                "DY": DY,
                "VV": VV,
                "TT": TT,
                "ST": ST,
            },
            "groupValues": {
                "ZH": 1.006, #1.010,
                "ggZH": 1.25, #1.010,
                "DY": 1.15, #1.010, #NOTE?
                "VV": 1.15,  # 1.010,
                "TT": 1.15, #1.005, #NOTE?
                "ST": 1.15,  # 1.005,
            },
        },
    }

    btag = {
        x.replace("Down", ""): {
            # x: {
            "type": "shape",
            "value": 1.0,
            "decorrelate": {"": Hbb + DY + VV + TT + ST},  # NOTE: ok?
        }
        for x in btag_sys
        if "Down" in x  # NOTE: ?
    }
    systematicDetail.update(btag)

    jer = {
        f"JER": {
        # f"JER{type}": {
            "type": "shape",
            "value": 1.0,
            "decorrelate": {"": Hbb + DY + VV + TT + ST},  # NOTE: ok?
        }
        # for type in ["Up", "Down"]
    }
    systematicDetail.update(jer)

    return systematicDetail
