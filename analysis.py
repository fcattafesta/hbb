from multiprocessing import Pool
import psutil
from samples import samples, flavourSplitting, flavourVVSplitting
import copy
import sys
from nail.nail import *
import ROOT
import traceback
import time
import os

from histobinning import binningRules
from args_analysis import args

from eventprocessingCommon import getFlowCommon
from eventprocessingMC import getFlowMC
from histograms import histos

if args.lep == "mu":
    from eventprocessingMuons import getFlowMuons as getFlow
    from histograms import histosPerSelectionMuon as histosPerSelection
elif args.lep == "el":
    from eventprocessingElectrons import getFlowElectrons as getFlow
    from histograms import histosPerSelectionElectron as histosPerSelection
else:
    print("Lepton channel must be 'mu' or 'el'")
    sys.exit(1)

nthreads = args.nthreads
nprocesses = 7
start = time.time()

if not os.path.exists(args.histfolder):
    os.makedirs(args.histfolder)

# Create the flow
flow = SampleProcessing(
    "Analysis", "/scratchnvme/malucchi/1574B1FB-8C40-A24E-B059-59A80F397A0F.root"
)
# Flow for data
flowData = getFlowCommon(flow)
flowData = getFlow(flowData)
# Final flow for MC
flow = copy.deepcopy(flowData)
flow = getFlowMC(flow)

# Add binning rules
flow.binningRules = binningRules
flowData.binningRules = binningRules

proc = flow.CreateProcessor(
    "eventProcessor",
    ["OneB", "TwoB", "OneC", "Light", "HF", "LF"],
    histosPerSelection,
    [],
    "",
    nthreads,
)
procData = flowData.CreateProcessor(
    "eventProcessorData",
    [],
    histosPerSelection,
    [],
    "",
    nthreads,
)


def sumwsents(files):
    sumws = 1e-9
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
    if sumws < 1:
        sumws = 1
    return sumws, LHEPdfSumw


# import samples


def runSample(ar):
    # f,s,i=ar
    p = psutil.Process()
    #    print("Affinity", p.cpu_affinity())
    p.cpu_affinity(list(range(psutil.cpu_count())))
    if args.range == -1:
        ROOT.gROOT.ProcessLine(
            """
        ROOT::EnableImplicitMT(%s);
        """
            % nthreads
        )
    s, files = ar
    #    print(files)
    if not "lumi" in samples[s].keys():  # is MC
        sumws, LHEPdfSumw = sumwsents(files)
    else:  # is data
        sumws, LHEPdfSumw = 1.0, []
    #    import jsonreader
    rdf = ROOT.RDataFrame("Events", files)
    if args.range != -1:
        rdf = rdf.Range(int(args.range))
    subs = {}
    if rdf:
        try:
            # add customizations here
            # rdf = rdf.Define("year", year)
            # rdf = rdf.Define("TriggerSel", trigger)
            if "lumi" in samples[s].keys():
                rdf = rdf.Define("isMC", "false")
                out = procData(rdf)
            else:
                if "subsamples" in samples[s].keys():
                    subs = samples[s]["subsamples"]
                rdf = rdf.Define("isMC", "true")
                out = proc(rdf, subs)

            snaplist = ["run", "event"] + histos
            branchList = ROOT.vector("string")()
            map(lambda x: branchList.push_back(x), snaplist)
            if args.snapshot and "training" in samples[s].keys() and samples[s]["training"]:
                sig_region = "SR_ee" if args.lep == "el" else "SR_mm"
                out.rdf[sig_region].Snapshot(
                    "Events", f"{args.histfolder}/Snapshots/{s}Snapshot.root", branchList
                )

            outFile = ROOT.TFile.Open(f"{args.histfolder}/{s}Histos.root", "recreate")
            if args.range == -1:
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
                    f"{args.histfolder}/{s}_{subname}Histos.root", "recreate"
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
            print(e)
            traceback.print_exc()
            print("FAIL", s)
            return 1
    else:
        print("Null file", s)


# from multiprocessing.pool import ThreadPool as Pool
runpool = Pool(nprocesses)

print(samples.keys())
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
print("To process", [x[0] for x in toproc])

if not os.path.exists(args.histfolder):
    os.makedirs(args.histfolder)


if args.model == "fix":
    toproc = []
    sss = sams
    if len(sys.argv[3:]):
        sss = [s for s in sams if s in sys.argv[3:]]
        print("fixing", sss)
    for s in sss:
        if os.path.exists(samples[s]["files"][0]):
            try:
                ff = ROOT.TFile.Open(f"{args.histfolder}/{s}Histos.root")
                if ff.IsZombie() or len(ff.GetListOfKeys()) == 0:
                    print("zombie or zero keys", s)
                    toproc.append((s, samples[s]["files"]))

            except:
                print("failed", s)
                toproc.append((s, samples[s]["files"]))
elif args.model[:5] == "model":
    import importlib

    model = importlib.import_module(args.model)
    # 	samples=model.samples

    allmc = []
    for x in model.background:
        for y in model.background[x]:
            if x.endswith(
                tuple(flavourSplitting.keys()) + tuple(flavourVVSplitting.keys())
            ):
                allmc.append(y.rsplit("_", 1)[0])
            else:
                allmc.append(y)

    allmc += [y for x in model.signal for y in model.signal[x]]
    alldata = [y for x in model.data for y in model.data[x]]
    for x in allmc:
        print(x, "\t", samples[x]["xsec"])
    for x in alldata:
        print(x, "\t", samples[x]["lumi"])

    toproc = [
        (s, samples[s]["files"]) for s in sams if s in allmc + alldata  # + sys.argv[3:]
    ]
elif args.model != "":
    toproc = [(s, samples[s]["files"]) for s in sams if s in args.model.split(",")]

print("Will process", [x[0] for x in toproc])

if nprocesses > 1:
    results = zip(runpool.map(runSample, toproc), [x[0] for x in toproc])
else:
    results = zip([runSample(x) for x in toproc], [x[0] for x in toproc])

print("Results", results)
print("To resubmit", [x[1] for x in results if x[0]])

print("time:  ", time.time() - start)
