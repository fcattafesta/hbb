main_dir = "/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/"
suffix = "_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"
suffix2 = "_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"
suffix3 = (
    "_TuneCP5_13TeV_powheg_pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"
)
suffix4 = "_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"
suffix5 = "_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"
main_dir1 = "/gpfs/ddn/srm/cms/store/data/Run2018"
suffix6 = "/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v"
suffix7 = "/EGamma/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v"
suffix8 = "_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"
suffix9 = "_TuneCP5_13TeV-powheg-madspin-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"
suffix10 = "_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v"

flavourSplitting = {
    #"b": "OneB",
    "bb": "TwoB",
    #"c": "OneC",
    #"udsg": "Light",
}

samples = {
    "DYM50": {
        "folder": main_dir + "DYJetsToLL_M-50" + suffix + "2/",
        "xsec": 5765.40,
        "subsamples": flavourSplitting,
    },
    "DYZpt-0To50": {
        "folder": main_dir
        + "DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20"
        + suffix
        + "1/",
        "xsec": 1341.42,
        "subsamples": flavourSplitting,
    },
    "DYZpt-50To100": {
        "folder": main_dir
        + "DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20"
        + suffix
        + "1/",
        "xsec": 359.52,
        "subsamples": flavourSplitting,
    },
    "DYZpt-100To250": {
        "folder": main_dir
        + "DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20"
        + suffix
        + "1/",
        "xsec": 88.36,
        "subsamples": flavourSplitting,
    },
    "DYZpt-250To400": {
        "folder": main_dir
        + "DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20"
        + suffix
        + "1/",
        "xsec": 3.52,
        "subsamples": flavourSplitting,
    },
    "DYZpt-400To650": {
        "folder": main_dir
        + "DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20"
        + suffix
        + "1/",
        "xsec": 0.49,
        "subsamples": flavourSplitting,
    },
    "DYZpt-650ToInf": {
        "folder": main_dir
        + "DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20"
        + suffix
        + "1/",
        "xsec": 0.05,
        "subsamples": flavourSplitting,
    },
}
# samples.update(
#     {
#         "DYHT-70To100": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-70to100" + suffix2 + "1/",
#             "xsec": 196.20,
#         },
#         "DYHT-100To200": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-100to200" + suffix2 + "1/",
#             "xsec": 190.13,
#         },
#         "DYHT-200To400": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-200to400" + suffix2 + "1/",
#             "xsec": 43.45,
#         },
#         "DYHT-400To600": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-400to600" + suffix2 + "1/",
#             "xsec": 5.45,
#         },
#         "DYHT-600To800": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-600to800" + suffix2 + "1/",
#             "xsec": 1.11,
#         },
#         "DYHT-800To1200": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-800to1200" + suffix2 + "1/",
#             "xsec": 0.47,
#         },
#         "DYHT-1200To2500": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-1200to2500" + suffix2 + "1/",
#             "xsec": 0.12,
#         },
#         "DYHT-2500ToInf": {
#             "folder": main_dir + "DYJetsToLL_M-50_HT-2500toInf" + suffix2 + "1/",
#             "xsec": 0.0,
#         },
#     }
# )

samples.update(
    {
        "ST_tW_antitop_5f_NFHD": {
            "folder": main_dir
            + "ST_tW_antitop_5f_NoFullyHadronicDecays"
            + suffix8
            + "1/",
            "xsec": 19.56,
        },
        "ST_tW_antitop_5f_ID": {
            "folder": main_dir + "ST_tW_antitop_5f_inclusiveDecays" + suffix8 + "2/",
            "xsec": 35.85,
        },
        "ST_tW_top_5f_NFHD": {
            "folder": main_dir + "ST_tW_top_5f_NoFullyHadronicDecays" + suffix8 + "1/",
            "xsec": 19.56,
        },
        "ST_tW_top_5f_ID": {
            "folder": main_dir + "ST_tW_top_5f_inclusiveDecays" + suffix8 + "2/",
            "xsec": 35.85,
        },
        "ST_t-channel_antitop_4f_ID": {
            "folder": main_dir
            + "ST_t-channel_antitop_4f_InclusiveDecays"
            + suffix9
            + "1/",
            "xsec": 80.95,
        },
        "ST_t-channel_top_4f_ID": {
            "folder": main_dir + "ST_t-channel_top_4f_InclusiveDecays" + suffix9 + "1/",
            "xsec": 136.02,
        },
        "ST_t-channel_antitop_5f_ID": {
            "folder": main_dir
            + "ST_t-channel_antitop_5f_InclusiveDecays"
            + suffix8
            + "1/",
            "xsec": 80.95,
        },
        "ST_s-channel_4f_LD": {
            "folder": main_dir + "ST_s-channel_4f_leptonDecays" + suffix10 + "1/",
            "xsec": 3.36,
        },
        "TTTo2L2Nu": {
            "folder": main_dir + "TTTo2L2Nu" + suffix8 + "1/",
            "xsec": 85.65,
        },  # 88.29
        "TTToSemiLeptonic": {
            "folder": main_dir + "TTToSemiLeptonic" + suffix8 + "1/",
            "xsec": 356.19,
        },  # 365.34
        "TTToHadronic": {
            "folder": main_dir + "TTToHadronic" + suffix8 + "1/",
            "xsec": 366.20,
        },  # 377.96
    }
)

samples.update(
    {
        "WZTo2Q2L": {
            "folder": main_dir + "WZTo2Q2L" + suffix5 + "1/",
            "xsec": 47.13 * 6.729 * 67.41 / 10000,
            "subsamples": flavourSplitting,
        },
        "WZTo3LNu": {
            "folder": main_dir + "WZTo3LNu" + suffix4 + "2/",
            "xsec": 47.13 * 21.34 * 10.099 / 10000.0,
            "subsamples": flavourSplitting,
        },
        "WWTo2L2Nu": {
            "folder": main_dir + "WWTo2L2Nu" + suffix8 + "2/",
            "xsec": 118.7 * 21.34 * 21.34 / 10000.0,
            "subsamples": flavourSplitting,
        },
        "ZZTo2L2Nu": {
            "folder": main_dir + "ZZTo2L2Nu" + suffix3 + "1/",
            "xsec": 16.523 * 20.000 * 10.099 / 10000.0,
        },
        "ZZTo2Q2L": {
            "folder": main_dir + "ZZTo2Q2L" + suffix5 + "1/",
            "xsec": 16.523 * 2.0 * 10.099 * 69.91 / 10000.0,
            "subsamples": flavourSplitting,
        },
        "ZZTo4L": {
            "folder": main_dir + "ZZTo4L" + suffix3 + "2/",
            "xsec": 16.523 * 10.099 * 10.099 / 10000.0,
        },
    }
)
samples.update(
    {
        "ZH": {
            "folder": main_dir + "ZH_HToBB_ZToLL_M-125" + suffix8 + "1/",
            "xsec": 0.880 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
        },  # 0.04718 (AN)
        "ggZH": {
            "folder": main_dir + "ggZH_HToBB_ZToLL_M-125" + suffix8 + "1/",
            "xsec": 0.123 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
        },  # 0.01437 (AN)
    }
)
samples.update(
    {
        "SingleMuon": {
            "folders": [
                main_dir1 + "A" + suffix6+"2/",
                main_dir1 + "B" + suffix6+"2/",
                main_dir1 + "C" + suffix6+"2/",
                main_dir1 + "D" + suffix6+"1/",
            ],
            "lumi": 59970,
        },
    }
)
samples.update(
    {
        "EGamma": {
            "folders": [
                main_dir1 + "A" + suffix7+"1/",
                main_dir1 + "B" + suffix7+"1/",
                main_dir1 + "C" + suffix7+"1/",
                main_dir1 + "D" + suffix7+"3/",
            ],
            "lumi": 0,
        },
    }
)


import os, glob
addSubSamples = {}
# get the files from the directory named as the sample name with the suffix /scratchnvme/malucchi/hbb_samples/
for sample in samples:
    if "subsamples" in samples[sample].keys():
        for ss in samples[sample]["subsamples"]:
            addSubSamples["%s_%s" % (sample, ss)] = {"xsec": samples[sample]["xsec"]}
    samples[sample]["files"] = [
        x for x in glob.glob("/scratchnvme/malucchi/hbb_samples/%s/**/*.root" % sample, recursive=True)
    ]
samples.update(addSubSamples)

if __name__ == "__main__":
    # copy all the files inside the "folder" in the directory called as the sample name with the prefix "/scratchnvme/malucchi/hbb_samples/"
    for sample in samples:
        if "folder" in samples[sample].keys():
            os.system("mkdir -p /scratchnvme/malucchi/hbb_samples/%s" % sample)
            os.system(
                "cp -r %s /scratchnvme/malucchi/hbb_samples/%s/"
                % (samples[sample]["folder"], sample)
            )
        elif "folders" in samples[sample].keys():
            os.system("mkdir -p /scratchnvme/malucchi/hbb_samples/%s" % sample)
            for folder in samples[sample]["folders"]:
                os.system("cp -r %s /scratchnvme/malucchi/hbb_samples/%s/" % (folder, sample))

# for sample in samples:
#     if "folder" in samples[sample].keys():
#         print(samples[sample]["folder"])
#     elif "folders" in samples[sample].keys():
#         for folder in samples[sample]["folders"]:
#             print(folder)

# addSubSamples = {}
# for sample in samples:
#     if "subsamples" in samples[sample].keys():
#         for ss in samples[sample]["subsamples"]:
#             addSubSamples["%s_%s" % (sample, ss)] = {"xsec": samples[sample]["xsec"]}
#     if "folder" in samples[sample].keys():
#         samples[sample]["files"] = [
#             x
#             for x in glob.glob(samples[sample]["folder"] + "/**/*.root", recursive=True)
#         ]
#     if "folders" in samples[sample].keys():
#         samples[sample]["files"] = []
#         for folder in samples[sample]["folders"]:
#             samples[sample]["files"].extend(
#                 [x for x in glob.glob(folder + "/**/*.root", recursive=True)]
#             )
# samples.update(addSubSamples)
