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

    DY = [
        "DYZpt-0To50",
        "DYZpt-50To100",
        "DYZpt-100To250",
        "DYZpt-250To400",
        "DYZpt-400To650",
        "DYZpt-650ToInf",
    ]
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
    WW = ["WWTo2L2Nu"]
    WZ = ["WZTo2Q2L", "WZTo3LNu"]
    ZZ = ["ZZTo2L2Nu", "ZZTo2Q2L", "ZZTo4L"]
    Hbb = ["ZH", "ggZH"]


    systematicDetail = {
        "XSecAndNorm"
        + year: {
            "type": "lnN",
            #               "decorrelate": { "Hmm": HmmNoVBF, "EWK":EWK,"DY":DY, "TT":TT ,"ST":ST, "WJets":WJets, "ZZ":ZZ, "WZ":WZ, "WW":WW},
            # "decorrelate": { "Hmm": HmmNoVBF, "EWK":EWK,"DY01J":DY01J,"DY2J":DY2J , "TT":TT ,"ST":ST, "WJets":WJets, "ZZ":ZZ, "WZ":WZ, "WW":WW},
            #                "groupValues":  {"Hmm":1.01, "EWK":1.01, "DY":1.010 ,"ZZ":1.01,"WZ":1.01,"WW":1.01,"WJets":1.01,"TT":1.005,"ST":1.005},
            "groupValues": {"ZZ": 1.01, "WZ": 1.01, "WW": 1.01, "TT":1.005,"ST":1.005, "Hbb":1.},
        },
    }

    return systematicDetail
