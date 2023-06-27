# TODO: separate systematics as
# shape only (remove normalization effects)
# per group
# per sample

# default is correlated among all samples
# and correlated nuisance for norm+shape


def systematicGrouping(background, signal, jesList, year):
    legendGrouping = {}
    legendGrouping.update(background)
    legendGrouping.update(signal)

    DY_bb = [
        "DYZpt-0To50_bb",
        "DYZpt-50To100_bb",
        "DYZpt-100To250_bb",
        "DYZpt-250To400_bb",
        "DYZpt-400To650_bb",
        "DYZpt-650ToInf_bb",
    ]
    DY_b = [
        "DYZpt-0To50_b",
        "DYZpt-50To100_b",
        "DYZpt-100To250_b",
        "DYZpt-250To400_b",
        "DYZpt-400To650_b",
        "DYZpt-650ToInf_b",
    ]
    DY_c = [
        "DYZpt-0To50_c",
        "DYZpt-50To100_c",
        "DYZpt-100To250_c",
        "DYZpt-250To400_c",
        "DYZpt-400To650_c",
        "DYZpt-650ToInf_c",
    ]
    DY_udsg = [
        "DYZpt-0To50_udsg",
        "DYZpt-50To100_udsg",
        "DYZpt-100To250_udsg",
        "DYZpt-250To400_udsg",
        "DYZpt-400To650_udsg",
        "DYZpt-650ToInf_udsg",
    ]

    DY = ["Z+bb", "Z+b", "Z+c", "Z+udsg"]

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
    WW_HF = ["WWTo2L2Nu_HF"]
    WW_LF = ["WWTo2L2Nu_LF"]
    WZ_HF = ["WZTo2Q2L_HF", "WZTo3LNu_HF"]
    WZ_LF = ["WZTo2Q2L_LF", "WZTo3LNu_LF"]
    ZZ_HF = ["ZZTo2L2Nu_HF", "ZZTo2Q2L_HF", "ZZTo4L_HF"]
    ZZ_LF = ["ZZTo2L2Nu_LF", "ZZTo2Q2L_LF", "ZZTo4L_LF"]
    Hbb = ["ZH", "ggZH"]

    systematicDetail = {
        "XSecAndNorm": {
            "type": "lnN",
            #               "decorrelate": { "Hmm": HmmNoVBF, "EWK":EWK,"DY":DY, "TT":TT ,"ST":ST, "WJets":WJets, "ZZ":ZZ, "WZ":WZ, "WW":WW},
            "additionalNormalizations": [],
            "decorrelate": {
                "VVHF": ["VVHF"],
                "VVLF": ["VVLF"],
                "TT": ["TT"],
                "ST": ["ST"],
                "Z+bb": ["Z+bb"],
                "Z+b": ["Z+b"],
                "Z+c": ["Z+c"],
                "Z+udsg": ["Z+udsg"],
                "ZH": ["ZH"],
                "ggZH": ["ggZH"],
            },
            #                "groupValues":  {"Hmm":1.01, "EWK":1.01, "DY":1.010 ,"ZZ":1.01,"WZ":1.01,"WW":1.01,"WJets":1.01,"TT":1.005,"ST":1.005},
            "groupValues": {
                "VVHF": 1.01,
                "VVLF": 1.01,
                "TT": 1.005,
                "ST": 1.005,
                "Z+bb": 1.010,
                "Z+b": 1.010,
                "Z+c": 1.010,
                "Z+udsg": 1.010,
                "ZH": 1.010,
                "ggZH": 1.010,
            },
        },
    }

    return systematicDetail
