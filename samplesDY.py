# Description: Samples for the DY analysis
import glob

flavourSplitting = {
    "b": "OneB",
    "bb": "TwoB",
    "c": "OneC",
    "udsg": "Light",
}

samples = {
    "DYM50": {
        "xsec": 5765.40,
        "subsamples": flavourSplitting,
        "training": True,
    },
    # "DYZpt-0To50": {
    #     "xsec": 1341.42,
    #     "subsamples": flavourSplitting,
    #     "training": True,
    # },
    # "DYZpt-50To100": {
    #     "xsec": 359.52,
    #     "subsamples": flavourSplitting,
    #     "training": True,
    # },
    # "DYZpt-100To250": {
    #     "xsec": 88.36,
    #     "subsamples": flavourSplitting,
    #     "training": True,
    # },
    # "DYZpt-250To400": {
    #     "xsec": 3.52,
    #     "subsamples": flavourSplitting,
    #     "training": True,
    # },
    # "DYZpt-400To650": {
    #     "xsec": 0.49,
    #     "subsamples": flavourSplitting,
    #     "training": True,
    # },
    # "DYZpt-650ToInf": {
    #     "xsec": 0.05,
    #     "subsamples": flavourSplitting,
    #     "training": True,
    # },
}

addSubSamples = {}
# get the files from the directory named as the sample name with the suffix /scratchnvme/malucchi/hbb_samples/
for sample in samples:
    if "subsamples" in samples[sample].keys():
        for ss in samples[sample]["subsamples"]:
            addSubSamples["%s_%s" % (sample, ss)] = {"xsec": samples[sample]["xsec"]}
    samples[sample]["files"] = [
        x
        for x in glob.glob(
            "/gpfs/ddn/cms/user/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/230000/*.root",
            recursive=True,
        )
    ]
samples.update(addSubSamples)
