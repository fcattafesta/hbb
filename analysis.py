from multiprocessing import Pool
import psutil
import copy
import sys
from nail.nail import *
import ROOT
import traceback
import time
import os

from logger import setup_logger

from histobinning import binningRules
from args_analysis import args

from eventprocessingMC import getFlowMC
from eventprocessingDNN import getFlowDNN
from histograms import histosData, histosMC

from samples import *

if args.btag not in ["deepcsv", "deepflav"]:
    print("Btagging algo must be 'deepflav' or 'deepcsv'")
    sys.exit(1)

from eventprocessingCommon import getFlowCommon
from eventprocessingSysBtag import getFlowSysBtag
from eventprocessingSysJER import getFlowSysJER

if args.lep == "mu":
    from eventprocessingMuons import getFlowMuons as getFlow
    from histograms import histosPerSelectionMuonMC as histosPerSelectionMC
    from histograms import histosPerSelectionMuonData as histosPerSelectionData
    from histograms import selsMu as sels
elif args.lep == "el":
    from eventprocessingElectrons import getFlowElectrons as getFlow
    from histograms import histosPerSelectionElectronMC as histosPerSelectionMC
    from histograms import histosPerSelectionElectronData as histosPerSelectionData
    from histograms import selsEle as sels
else:
    print("Lepton channel must be 'mu' or 'el'")
    sys.exit(1)

nthreads = args.nthreads if args.range == -1 else 0
nprocesses = args.num_processes
start = time.time()

os.makedirs(args.histfolder, exist_ok=True)
# remove the log file if already exists
if os.path.exists(f"{args.histfolder}/logger.log"):
    os.remove(f"{args.histfolder}/logger.log")

logger = setup_logger(f"{args.histfolder}/logger.log")


logger.info("args:\n - %s", "\n - ".join(str(it) for it in args.__dict__.items()))

# Create the flow
flowMC = SampleProcessing(
    "Analysis", "/scratchnvme/malucchi/1574B1FB-8C40-A24E-B059-59A80F397A0F.root"
)

# Add binning rules
flowMC.binningRules = binningRules

flowData = copy.deepcopy(flowMC)

# Flow for data
flowData = getFlowSysJER(flowData, sys=False)
flowData = getFlowCommon(flowData, args.btag)
flowData = getFlow(flowData)
if args.eval_model:
    flowData = getFlowDNN(args.eval_model, flowData)

# Flow for MC
if args.sf:
    flowMC = getFlowSysJER(flowMC, sys=True)
else:
    flowMC = getFlowSysJER(flowMC, sys=False)
flowMC = getFlowCommon(flowMC, args.btag)
if args.sf:
    flowMC = getFlowSysBtag(flowMC, args.btag)
flowMC = getFlow(flowMC)
if args.eval_model:
    flowMC = getFlowDNN(args.eval_model, flowMC)
flowMC = getFlowMC(flowMC)

# systematics
systematics = flowMC.variations
logger.info("Systematics for all plots: %s" % systematics)
histosWithSystematicsMC = flowMC.createSystematicBranches(
    systematics, histosPerSelectionMC
)
logger.info("Histograms with systematics: %s" % histosWithSystematicsMC)

procMC = flowMC.CreateProcessor(
    "eventProcessorMC",
    [flavourSplitting[x] for x in flavourSplitting],
    histosWithSystematicsMC,
    [],
    "",
    nthreads,
)
procData = flowData.CreateProcessor(
    "eventProcessorData",
    [],
    histosPerSelectionData,
    [],
    "",
    nthreads,
)


def sumwsents(files):
    sumws = 1e-9
    nevents = 0
    LHEPdfSumw = []
    for fn in files:
        f = ROOT.TFile.Open(fn)
        run = f.Get("Runs")
        hasUnderscore = "genEventSumw_" in [
            x.GetName() for x in run.GetListOfBranches()
        ]
        if run:
            hw = ROOT.TH1F("hw", "", 5, 0, 5)
            if hasUnderscore:
                run.Project("hw", "1", "genEventSumw_")
            else:
                run.Project("hw", "1", "genEventSumw")
                sumws += hw.GetSumOfWeights()

            hn = ROOT.TH1I("hn", "", 5, 0, 5)
            run.Project("hn", "1", "genEventCount")
            nevents += int(hn.GetSumOfWeights())

    if sumws < 1:
        sumws = 1
    if nevents < 1:
        nevents = 1

    return sumws, LHEPdfSumw, nevents


def runSample(ar):
    # f,s,i=ar
    p = psutil.Process()
    #    print("Affinity", p.cpu_affinity())
    p.cpu_affinity(list(range(psutil.cpu_count())))
    if nthreads != 0:
        ROOT.gROOT.ProcessLine(
            """
        ROOT::EnableImplicitMT(%s);
        """
            % nthreads
        )
    s, files = ar
    #    print(files)
    if not "lumi" in samples[s].keys():  # is MC
        sumws, LHEPdfSumw, nevents = sumwsents(files)
        logger.info("Start sample %s: sumws %s, nevents %s" % (s, sumws, nevents))
    else:  # is data
        sumws, LHEPdfSumw, nevents = 1.0, [], 0
        logger.info("Start sample %s: nevents %s" % (s, nevents))
    #    import jsonreader
    rdf = ROOT.RDataFrame("Events", files)
    if args.range != -1:
        rdf = rdf.Range(args.range)
    subs = {}
    if rdf:
        try:
            # add customizations here
            # rdf = rdf.Define("year", year)
            # rdf = rdf.Define("TriggerSel", trigger)
            snaplist = ["run", "event"]

            if "lumi" in samples[s].keys():
                rdf = rdf.Define("isMC", "false")
                out = procData(rdf)
                snaplist += histosData
            else:
                if "subsamples" in samples[s].keys():
                    subs = samples[s]["subsamples"]
                rdf = rdf.Define("isMC", "true")
                out = procMC(rdf, subs)
                snaplist += histosMC + ["DNN_weight"]

            if (
                args.snapshot
                and "snapshot" in samples[s].keys()
                and samples[s]["snapshot"]
            ):
                for region in sels:
                    # create snapshot directory
                    os.makedirs(f"{args.histfolder}/Snapshots", exist_ok=True)
                    processed_rdf = out.rdf.find(region).second
                    if "xsec" in samples[s].keys():  # is MC
                        processed_rdf = processed_rdf.Define(
                            "DNN_weight",
                            f"genWeight/{sumws}*{samples[s]['xsec']}*{nevents}",
                        )
                    processed_rdf.Snapshot(
                        "Events",
                        f"{args.histfolder}/Snapshots/{s}_{region}_Snapshot.root",
                        snaplist,
                    )
                    if "xsec" in samples[s].keys():
                        output_file = ROOT.TFile(
                            f"{args.histfolder}/Snapshots/{s}_{region}_Snapshot.root",
                            "UPDATE",
                        )
                        tree = ROOT.TTree("Runs", "Runs")
                        x = ROOT.std.vector("double")()
                        tree.Branch("genEventSumw", x)
                        x.push_back(sumws)
                        tree.Fill()
                        output_file.Write()
                        output_file.Close()

            outFile = ROOT.TFile.Open(f"{args.histfolder}/{s}_Histos.root", "recreate")
            if nthreads != 0:
                ROOT.gROOT.ProcessLine("ROOT::EnableImplicitMT(%s);" % nthreads)
            normalization = 1.0

            for h in out.histos:
                hname = h.GetName()
                h.GetValue()
                outFile.cd()
                h.Scale(1.0 / normalization / sumws)
                h.Write()
            sumWeights = getattr(ROOT, "TParameter<double>")("sumWeights", sumws)
            sumWeights.Write()
            outFile.Write()
            outFile.Close()

            for subname in subs:
                outFile = ROOT.TFile.Open(
                    f"{args.histfolder}/{s}_{subname}_Histos.root", "recreate"
                )
                for h in out.histosOutSplit[subname]:
                    hname = h.GetName()
                    h.GetValue()
                    outFile.cd()
                    h.Scale(1.0 / normalization / sumws)
                    h.Write()
                sumWeights = getattr(ROOT, "TParameter<double>")("sumWeights", sumws)
                sumWeights.Write()
                outFile.Write()
                outFile.Close()

            return 0
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            logger.error("FAIL", s)
            return 1
    else:
        logger.info("Null file %s" % s)

    logger.info("Finish sample %s: nevents %s" % (s, nevents))


# from multiprocessing.pool import ThreadPool as Pool
runpool = Pool(nprocesses)

logger.info(samples.keys())
sams = samples.keys()

# check that at least the first file exists
toproc = [
    (s, samples[s]["files"])
    for s in sams
    if "files" in samples[s].keys() and os.path.exists(samples[s]["files"][0])
]

# sort by sample size, start heaviest first
toproc = sorted(
    toproc,
    key=lambda x: sum(
        map(lambda x: (os.path.getsize(x) if os.path.exists(x) else 0), x[1])
    ),
    reverse=True,
)
logger.info("To process %s" % [x[0] for x in toproc])

if args.model == "fix":
    toproc = []
    sss = sams
    if len(sys.argv[3:]):
        sss = [s for s in sams if s in sys.argv[3:]]
        logger.info("fixing %s" % sss)
    for s in sss:
        if os.path.exists(samples[s]["files"][0]):
            try:
                ff = ROOT.TFile.Open(f"{args.histfolder}/{s}_Histos.root")
                if ff.IsZombie() or len(ff.GetListOfKeys()) == 0:
                    logger.info("zombie or zero keys %s" % s)
                    toproc.append((s, samples[s]["files"]))

            except:
                logger.error("failed", s)
                toproc.append((s, samples[s]["files"]))
elif "model" in args.model[:5]:
    import importlib

    model = importlib.import_module(args.model.replace(".py", ""))
    # 	samples=model.samples

    allmc = []
    for x in model.background:
        for y in model.background[x]:
            if x.endswith(
                tuple(flavourSplitting.keys())
                + tuple(flavourVVSplitting.keys())
                + tuple(number_of_b.keys())
            ):
                if y.rsplit("_", 1)[0] not in allmc:
                    allmc.append(y.rsplit("_", 1)[0])
            else:
                if y not in allmc:
                    allmc.append(y)

    allmc += [y for x in model.signal for y in model.signal[x]]
    alldata = [y for x in model.data for y in model.data[x]]
    for x in allmc:
        logger.info("%s\t%s" % (x, samples[x]["xsec"]))
    for x in alldata:
        logger.info("%s\t%s" % (x, samples[x]["lumi"]))

    toproc = [
        (s, samples[s]["files"]) for s in sams if s in allmc + alldata  # + sys.argv[3:]
    ]
elif args.model != "":
    toproc = [(s, samples[s]["files"]) for s in sams if s in args.model.split(",")]

logger.info("Will process %s" % [x[0] for x in toproc])

if nprocesses > 1:
    results = zip(runpool.map(runSample, toproc), [x[0] for x in toproc])
else:
    results = zip([runSample(x) for x in toproc], [x[0] for x in toproc])

logger.info("Results %s" % results)
logger.info("To resubmit %s" % [x[1] for x in results if x[0] == 1])

logger.info("histo folder %s" % args.histfolder)
logger.info("time:   %s" % (time.time() - start))
