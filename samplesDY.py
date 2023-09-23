# Description: Samples for the DY analysis
import glob

print("Loading samplesDY.py")

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
    # "DYM50": {
    #     "xsec": 5765.40,
    #     "subsamples": flavourSplitting,
    #     "training": True,
    # },
    "DYZpt-0To50": {
        "xsec": 1341.42,
        "subsamples": flavourSplitting,
        "training": True,
    },
    "DYZpt-50To100": {
        "xsec": 359.52,
        "subsamples": flavourSplitting,
        "training": True,
    },
    "DYZpt-100To250": {
        "xsec": 88.36,
        "subsamples": flavourSplitting,
        "training": True,
    },
    "DYZpt-250To400": {
        "xsec": 3.52,
        "subsamples": flavourSplitting,
        "training": True,
    },
    "DYZpt-400To650": {
        "xsec": 0.49,
        "subsamples": flavourSplitting,
        "training": True,
    },
    "DYZpt-650ToInf": {
        "xsec": 0.05,
        "subsamples": flavourSplitting,
        "training": True,
    },
}

samples.update(
    {
        # "DYM50Full": {
        #     "xsec": 5765.40,
        #     "subsamples": flavourSplitting,
        #     "training": True,
        # },
        "DYZpt-0To50Full": {
            "xsec": 1341.42,
            "subsamples": flavourSplitting,
            "training": True,
        },
        "DYZpt-50To100Full": {
            "xsec": 359.52,
            "subsamples": flavourSplitting,
            "training": True,
        },
        "DYZpt-100To250Full": {
            "xsec": 88.36,
            "subsamples": flavourSplitting,
            "training": True,
        },
        "DYZpt-250To400Full": {
            "xsec": 3.52,
            "subsamples": flavourSplitting,
            "training": True,
        },
        "DYZpt-400To650Full": {
            "xsec": 0.49,
            "subsamples": flavourSplitting,
            "training": True,
        },
        "DYZpt-650ToInfFull": {
            "xsec": 0.05,
            "subsamples": flavourSplitting,
            "training": True,
        },
    }
)

samples.update(
    {
        "ST_tW_antitop_5f_NFHD": {
            "xsec": 19.56,
            "training": True,
        },
        "ST_tW_antitop_5f_ID": {
            "xsec": 35.85,
            "training": True,
        },
        "ST_tW_top_5f_NFHD": {
            "xsec": 19.56,
            "training": True,
        },
        "ST_tW_top_5f_ID": {
            "xsec": 35.85,
            "training": True,
        },
        "ST_t-channel_antitop_4f_ID": {
            "xsec": 80.95,
            "training": True,
        },
        "ST_t-channel_top_4f_ID": {
            "xsec": 136.02,
            "training": True,
        },
        "ST_t-channel_antitop_5f_ID": {
            "xsec": 80.95,
            "training": True,
        },
        "ST_s-channel_4f_LD": {
            "xsec": 3.36,
            "training": True,
        },
        "TTTo2L2Nu": {
            "xsec": 85.65,
            "training": True,
        },  # 88.29
        "TTToSemiLeptonic": {
            "xsec": 356.19,
            "training": True,
        },  # 365.34
        "TTToHadronic": {
            "xsec": 366.20,
            "training": True,
        },  # 377.96
    }
)

samples.update(
    {
        "WZTo2Q2L": {
            "xsec": 47.13 * 6.729 * 67.41 / 10000,
            "subsamples": flavourVVSplitting,
            "training": True,
        },
        "WZTo3LNu": {
            "xsec": 47.13 * 21.34 * 10.099 / 10000.0,
            "subsamples": flavourVVSplitting,
            "training": True,
        },
        "WWTo2L2Nu": {
            "xsec": 118.7 * 21.34 * 21.34 / 10000.0,
            "subsamples": flavourVVSplitting,
            "training": True,
        },
        "ZZTo2L2Nu": {
            "xsec": 16.523 * 20.000 * 10.099 / 10000.0,
            "subsamples": flavourVVSplitting,
            "training": True,
        },
        "ZZTo2Q2L": {
            "xsec": 16.523 * 2.0 * 10.099 * 69.91 / 10000.0,
            "subsamples": flavourVVSplitting,
            "training": True,
        },
        "ZZTo4L": {
            "xsec": 16.523 * 10.099 * 10.099 / 10000.0,
            "subsamples": flavourVVSplitting,
            "training": True,
        },
    }
)
samples.update(
    {
        "ZHFull": {
            "xsec": 0.880 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
            "training": True,
        },  # 0.04718 (AN)
        "ggZHFull": {
            "xsec": 0.123 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
            "training": True,
        },  # 0.01437 (AN)
    }
)

samples.update(
    {
        "ZH": {
            "xsec": 0.880 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
            "training": True,
        },  # 0.04718 (AN)
        "ggZH": {
            "xsec": 0.123 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
            "training": True,
        },  # 0.01437 (AN)
    }
)

samples.update(
    {
        "SingleMuon_2018": {
            "lumi": 59970,
            "training": True,
        },
    }
)
samples.update(
    {
        "EGamma_2018": {
            "lumi": 59970,  # NOTE this is the same as for muons but it is an approximation
            "training": True,
        },
    }
)

addSubSamples = {}
# get the files from the directory named as the sample name with the suffix /scratchnvme/malucchi/hbb_samples/
for sample in samples:
    if "subsamples" in samples[sample].keys():
        for ss in samples[sample]["subsamples"]:
            addSubSamples["%s_%s" % (sample, ss)] = {"xsec": samples[sample]["xsec"]}
    if sample.startswith("DYZpt") and sample.endswith("Full"):
        files = [
            x
            for x in glob.glob(
                "/scratchnvme/malucchi/hbb_samples/%s/**/*.root"
                % sample.replace("Full", ""),
                recursive=True,
            )
        ]
        if sample == "DYZpt-0To50Full":
            files.remove(
                "/scratchnvme/malucchi/hbb_samples/DYZpt-0To50/106X_upgrade2018_realistic_v16_L1v1-v1/40000/C69E7CE2-4C90-AD40-BCF7-CBD024956640.root"
            )
        elif sample == "DYZpt-50To100Full":
            files.remove(
                "/scratchnvme/malucchi/hbb_samples/DYZpt-50To100/106X_upgrade2018_realistic_v16_L1v1-v1/40000/51C14FFE-9AFF-374E-8A53-61AF6E4E1B77.root"
            )
        samples[sample]["files"] = files
    elif sample.startswith("DYZpt") and not sample.endswith("Full"):
        files = [
            x
            for x in glob.glob(
                f"/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-{sample.replace('DYZpt-', '', 1)}_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/**/*.root",
                recursive=True,
            )
        ]
        if sample == "DYZpt-0To50":
            files.remove(
                "/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/40000/C69E7CE2-4C90-AD40-BCF7-CBD024956640.root"
            )
        elif sample == "DYZpt-50To100":
            files.remove(
                "/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/40000/51C14FFE-9AFF-374E-8A53-61AF6E4E1B77.root"
            )
        samples[sample]["files"] = files
    elif sample == "ZH":
        files = [
            x
            for x in glob.glob(
                "/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/ZH_HToBB_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/**/*.root",
                recursive=True,
            )
        ]
        samples[sample]["files"] = files
    elif sample == "ggZH":
        files = [
            x
            for x in glob.glob(
                "/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/ggZH_HToBB_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/**/*.root",
                recursive=True,
            )
        ]
        samples[sample]["files"] = files

    elif sample == "ZHFull":
        samples[sample]["files"] = [
            x
            for x in glob.glob(
                "/scratchnvme/malucchi/hbb_samples/ZH/106X_upgrade2018_realistic_v16_L1v1-v1/**/*.root",
                recursive=True,
            )
        ]
    elif sample == "ggZHFull":
        samples[sample]["files"] = [
            x
            for x in glob.glob(
                "/scratchnvme/malucchi/hbb_samples/ggZH/106X_upgrade2018_realistic_v16_L1v1-v1/**/*.root",
                recursive=True,
            )
        ]
    else:
        samples[sample]["files"] = [
            x
            for x in glob.glob(
                "/scratchnvme/malucchi/hbb_samples/%s/**/*.root" % sample,
                recursive=True,
            )
        ]
samples.update(addSubSamples)
