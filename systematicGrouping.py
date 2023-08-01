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

    DY_bb = [x + "_bb" for x in DY_]
    DY_b = [x + "_b" for x in DY_]
    DY_c = [x + "_c" for x in DY_]
    DY_udsg = [x + "_udsg" for x in DY_]

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
                "DY_bb": DY_bb,
                "DY_b": DY_b,
                "DY_c": DY_c,
                "DY_udsg": DY_udsg,
                "VV": VV_,
                "TT": TT,
                "ST": ST,
            },
            "groupValues": {
                "ZH": 1.006,  # 1.010,
                "ggZH": 1.25,  # 1.010,
                "DY_bb": 1.15,  # 1.010, #NOTE?
                "DY_b": 1.15,  # 1.010, #NOTE?
                "DY_c": 1.15,  # 1.010, #NOTE?
                "DY_udsg": 1.15,  # 1.010, #NOTE?
                "VV": 1.15,  # 1.010,
                "TT": 1.15,  # 1.005, #NOTE?
                "ST": 1.15,  # 1.005,
            },
        },
    }

    btag = {
        x.replace("Down", ""): {
            # x: {
            "type": "shape",
            "value": 1.0,
            "decorrelate": {"": Hbb + DY_bb + DY_b + DY_c + DY_udsg + VV_ + TT + ST},  # NOTE: ok?
        }
        for x in btag_sys
        if "Down" in x  # NOTE: ?
    }
    systematicDetail.update(btag)

    jer = {
        f"JER": {
            # f"JER{type}": {
            "type": "shape",
            "value": 1.0, #0.5,
            "decorrelate": {"": Hbb + DY_bb + DY_b + DY_c + DY_udsg + VV_ + TT + ST},  # NOTE: ok?
        }
        # for type in ["Up", "Down"]
    }
    systematicDetail.update(jer)

    return systematicDetail
