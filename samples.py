# This file contains the samples used in the analysis.
import glob

from flavourSplitting import *



# NOTE: xsec in pt bins are obtained using the xsec.py file in the preliminar_lhe directory
# in which the xsec is computed using the ratio between the sum of weights of the events in the bin
# and the sum of weights of all the events in the sample.
samples = {
    "DYM50": {
        "xsec": 5765.40,
    },
    "DYZpt-0To50": {
        "xsec": 1341.42,
    },
    "DYZpt-50To100": {
        "xsec": 359.52,
    },
    "DYZpt-100To250": {
        "xsec": 88.36,
    },
    "DYZpt-250To400": {
        "xsec": 3.52,
    },
    "DYZpt-400To650": {
        "xsec": 0.49,
    },
    "DYZpt-650ToInf": {
        "xsec": 0.05,
    },
}

samples.update(
    {
        "ST_tW_antitop_5f_NFHD": {
            "xsec": 19.56,
        },
        "ST_tW_antitop_5f_ID": {
            "xsec": 35.85,
        },
        "ST_tW_top_5f_NFHD": {
            "xsec": 19.56,
        },
        "ST_tW_top_5f_ID": {
            "xsec": 35.85,
        },
        "ST_t-channel_antitop_4f_ID": {
            "xsec": 80.95,
        },
        "ST_t-channel_top_4f_ID": {
            "xsec": 136.02,
        },
        "ST_t-channel_antitop_5f_ID": {
            "xsec": 80.95,
        },
        "ST_s-channel_4f_LD": {
            "xsec": 3.36,
        },
        "TTTo2L2Nu": {
            "xsec": 85.65,
        },  # 88.29
        "TTToSemiLeptonic": {
            "xsec": 356.19,
        },  # 365.34
        "TTToHadronic": {
            "xsec": 366.20,
        },  # 377.96
    }
)

samples.update(
    {
        "WZTo2Q2L": {
            "xsec": 47.13 * 6.729 * 67.41 / 10000,
        },
        "WZTo3LNu": {
            "xsec": 47.13 * 21.34 * 10.099 / 10000.0,
        },
        "WWTo2L2Nu": {
            "xsec": 118.7 * 21.34 * 21.34 / 10000.0,
        },
        "ZZTo2L2Nu": {
            "xsec": 16.523 * 20.000 * 10.099 / 10000.0,
        },
        "ZZTo2Q2L": {
            "xsec": 16.523 * 2.0 * 10.099 * 69.91 / 10000.0,
        },
        "ZZTo4L": {
            "xsec": 16.523 * 10.099 * 10.099 / 10000.0,
        },
    }
)

for sample in samples:
    if "subsamples" not in samples[sample].keys():
        samples[sample]["subsamples"] = flavourSplitting

samples.update(
    {
        "ZH": {
            "xsec": 0.880 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
        },  # 0.04718 (AN)
        "ggZH": {
            "xsec": 0.123 * 58.09 * (3.3632 + 3.3662 + 3.3696) / 10000.0,
        },  # 0.01437 (AN)
    }
)
samples.update(
    {
        "SingleMuon_2018": {
            "lumi": 59970,
        },
        "EGamma_2018": {
            "lumi": 59970,  # NOTE this is the same as for muons but it is an approximation
        },
    }
)

for sample in samples:
    if "snapshot" not in samples[sample].keys():
        samples[sample]["snapshot"] = True

addSubSamples = {}
# get the files from the directory named as the sample name with the suffix /scratchnvme/malucchi/hbb_samples/
for sample in samples:
    if "subsamples" in samples[sample].keys():
        for ss in samples[sample]["subsamples"]:
            addSubSamples["%s_%s" % (sample, ss)] = {"xsec": samples[sample]["xsec"]}
    samples[sample]["files"] = [
        x
        for x in glob.glob(
            "/scratchnvme/malucchi/hbb_samples/%s/**/*.root" % sample, recursive=True
        )
    ]
samples.update(addSubSamples)

# for x in samples:
#     print(x, samples[x])
