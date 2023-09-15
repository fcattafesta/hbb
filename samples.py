# This file contains the samples used in the analysis.
import glob

# NOTE: change order of flavsplit?
flavourSplitting = {
    # "bb": "TwoB",
    # "b": "OneB",
    # "c": "C",
    # "udsg": "Light",
}

flavourVVSplitting = {
    "HF": ["bb", "b", "c"],
    "LF": ["udsg"],
}


number_of_b = {
    "0b": ["udsg", "c"],
    "1b": ["b"],
    "2b": ["bb"],
}

samples = {
    "DYM50": {
        "xsec": 5765.40,
        "subsamples": flavourSplitting,
        "snapshot": True,
    },
    "DYZpt-0To50": {
        "xsec": 1341.42,
        "subsamples": flavourSplitting,
        "snapshot": True,
    },
    "DYZpt-50To100": {
        "xsec": 359.52,
        "subsamples": flavourSplitting,
        "snapshot": True,
    },
    "DYZpt-100To250": {
        "xsec": 88.36,
        "subsamples": flavourSplitting,
        "snapshot": True,
    },
    "DYZpt-250To400": {
        "xsec": 3.52,
        "subsamples": flavourSplitting,
        "snapshot": True,
    },
    "DYZpt-400To650": {
        "xsec": 0.49,
        "subsamples": flavourSplitting,
        "snapshot": True,
    },
    "DYZpt-650ToInf": {
        "xsec": 0.05,
        "subsamples": flavourSplitting,
        "snapshot": True,
    },
}

samples.update(
    {
        "DYZpt-100To250-0": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-1": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-2": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-3": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-4": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-5": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-6": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-7": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-8": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "DYZpt-100To250-9": {
            "xsec": 88.36 / 10.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
    }
)

samples.update(
    {
        "ST_tW_antitop_5f_NFHD": {
            "xsec": 19.56,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ST_tW_antitop_5f_ID": {
            "xsec": 35.85,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ST_tW_top_5f_NFHD": {
            "xsec": 19.56,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ST_tW_top_5f_ID": {
            "xsec": 35.85,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ST_t-channel_antitop_4f_ID": {
            "xsec": 80.95,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ST_t-channel_top_4f_ID": {
            "xsec": 136.02,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ST_t-channel_antitop_5f_ID": {
            "xsec": 80.95,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ST_s-channel_4f_LD": {
            "xsec": 3.36,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "TTTo2L2Nu": {
            "xsec": 85.65,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },  # 88.29
        "TTToSemiLeptonic": {
            "xsec": 356.19,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },  # 365.34
        "TTToHadronic": {
            "xsec": 366.20,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },  # 377.96
    }
)


samples.update(
    {
        "WZTo2Q2L": {
            "xsec": 47.13 * 6.729 * 67.41 / 10000,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "WZTo3LNu": {
            "xsec": 47.13 * 21.34 * 10.099 / 10000.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "WWTo2L2Nu": {
            "xsec": 118.7 * 21.34 * 21.34 / 10000.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ZZTo2L2Nu": {
            "xsec": 16.523 * 20.000 * 10.099 / 10000.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ZZTo2Q2L": {
            "xsec": 16.523 * 2.0 * 10.099 * 69.91 / 10000.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
        "ZZTo4L": {
            "xsec": 16.523 * 10.099 * 10.099 / 10000.0,
            "subsamples": flavourSplitting,
            "snapshot": True,
        },
    }
)
samples.update(
    {
        "ZH": {
            "xsec": 0.880 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
            "snapshot": True,
        },  # 0.04718 (AN)
        "ggZH": {
            "xsec": 0.123 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
            "snapshot": True,
        },  # 0.01437 (AN)
    }
)
samples.update(
    {
        "SingleMuon_2018": {
            "lumi": 59970,
            "snapshot": True,
        },
    }
)
samples.update(
    {
        "EGamma_2018": {
            "lumi": 59970,  # NOTE this is the same as for muons but it is an approximation
            "snapshot": True,
        },
    }
)
i = 0
addSubSamples = {}
# get the files from the directory named as the sample name with the suffix /scratchnvme/malucchi/hbb_samples/
for sample in samples:
    if "subsamples" in samples[sample].keys():
        for ss in samples[sample]["subsamples"]:
            addSubSamples["%s_%s" % (sample, ss)] = {"xsec": samples[sample]["xsec"]}
    if not "files" in samples[sample].keys():
        if sample.startswith("DYZpt-100To250"):
            samples[sample]["files"] = [
                x
                for x in glob.glob(
                    "/scratchnvme/cattafe/FlashSim-Oversampled/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/**/*.root"
                )
            ][:1]
            # samples[sample]["files"] = [
            #     "/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2530000/B24D7292-7CA2-804F-9082-BCFDC95CFDC5.root"
            # ]
            print(samples[sample]["files"])
            # [10 * (i) :: 10 * (i + 1)]
            # i += 1
        else:
            samples[sample]["files"] = [
                x
                for x in glob.glob(
                    "/scratchnvme/malucchi/hbb_samples/%s/**/*.root" % sample,
                    recursive=True,
                )
            ]
samples.update(addSubSamples)

# for x in samples:
#     print(x, samples[x])
