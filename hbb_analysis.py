from multiprocessing import Pool
import psutil
from hbb_samples import samples
import copy
import sys
from nail.nail import *
import ROOT
import traceback
import time

nthreads = 50
nprocesses = 7
start=time.time()

flow = SampleProcessing( "DYJetsToLL", "/scratchnvme/malucchi/1574B1FB-8C40-A24E-B059-59A80F397A0F.root")
flow.CentralWeight("genWeight")  # add a central weight

flow.binningRules = [
    (".*_pt", "500,0,1000"),
    ]

flow.Define("LHE_Zpt", "LHE_Vpt")
flow.SubCollection("SelectedMuon","Muon",sel="Muon_iso < 0.25 && Muon_mediumId && Muon_pt > 20. && abs(Muon_eta) < 2.4")
flow.Selection("twoMuons","nSelectedMuon==2")
flow.Define("SelectedMuon_p4","@p4v(SelectedMuon)")

flow.Distinct("MuMu","SelectedMuon")
flow.Define("OppositeSignMuMu","Nonzero(MuMu0_charge != MuMu1_charge)",requires=["twoMuons"])
flow.Selection("twoOppositeSignMuons","OppositeSignMuMu.size() > 0")
flow.TakePair("Mu","SelectedMuon","MuMu","At(OppositeSignMuMu,0,-200)",requires=["twoOppositeSignMuons"])
flow.Define("Z","Mu0_p4+Mu1_p4")
flow.Define("Z_pt","Z.Pt()")
#flow.Selection("NotZeroZ_pt","Z_pt > 0")

histosPerSelection = {
    "": [ "LHE_Zpt" ],
    "twoOppositeSignMuons": [ "LHE_Zpt" , 'Z_pt'],
}

proc=flow.CreateProcessor("eventProcessor",[],histosPerSelection,[],"",nthreads)

def sumwsents(files):
   sumws=1e-9
   LHEPdfSumw=[]
   for fn in files:
      f=ROOT.TFile.Open(fn)
      run=f.Get("Runs")
      hasUnderscore = ("genEventSumw_" in [x.GetName() for x in run.GetListOfBranches()])
      if run :
         hw=ROOT.TH1F("hw","", 5,0,5)
         if hasUnderscore: run.Project("hw","1","genEventSumw_")
         else :
                 run.Project("hw","1","genEventSumw")
                 sumws+=hw.GetSumOfWeights()
   if sumws < 1: sumws = 1
   return sumws, LHEPdfSumw

#import samples

def runSample(ar):
    # f,s,i=ar
    p = psutil.Process()
#    print("Affinity", p.cpu_affinity())
    p.cpu_affinity(list(range(psutil.cpu_count())))
    ROOT.gROOT.ProcessLine('''
     ROOT::EnableImplicitMT(%s);
     ''' % nthreads)
    s, files = ar
#    print(files)
    if not "lumi" in samples[s].keys(): #is MC
        sumws, LHEPdfSumw = sumwsents(files)
    else: #is data
        sumws, LHEPdfSumw = 1., []
#    import jsonreader
    rdf = ROOT.RDataFrame("Events", files)  # .Range(10000)
    if rdf:
        try:
            #add customizations here
            #rdf = rdf.Define("year", year)
            #rdf = rdf.Define("TriggerSel", trigger)
            if "lumi" in samples[s].keys():
                rdf = rdf.Define("isMC", "false")
                out = procData(rdf)
            else:
                rdf = rdf.Define("isMC", "true")
                out = proc(rdf)

            snaplist = ["run", "event"]
            branchList = ROOT.vector('string')()
            map(lambda x: branchList.push_back(x), snaplist)
            if "training" in samples[s].keys() and samples[s]["training"]:
                out.rdf["PreSel"].Snapshot("Events", "out/%sSnapshot.root" % (s), branchList)

            outFile = ROOT.TFile.Open("out/%sHistos.root" % (s), "recreate")
            ROOT.gROOT.ProcessLine("ROOT::EnableImplicitMT(%s);" % nthreads)
            normalization = 1.
            for h in out.histos:
                hname = h.GetName()
                h.GetValue()
                outFile.cd()
                h.Scale(1./normalization/sumws)
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


#from multiprocessing.pool import ThreadPool as Pool
runpool = Pool(nprocesses)

print(samples.keys())
sams = samples.keys()

#check that at least the first file exists
toproc = [(s, samples[s]["files"]) for s in sams if os.path.exists(samples[s]["files"][0])]

#sort by sample size, start heaviest first
toproc = sorted(toproc, key=lambda x: sum(map(lambda x: (
    os.path.getsize(x) if os.path.exists(x) else 0), x[1])), reverse=True)
print ("To process", [x[0] for x in toproc])

if len(sys.argv[2:]):
    if sys.argv[2] == "fix":
        toproc = []
        sss = sams
        if(len(sys.argv[3:])):
            sss = [s for s in sams if s in sys.argv[3:]]
            print("fixing", sss)
        for s in sss:
            if os.path.exists(samples[s]["files"][0]):
                try:
                    ff = ROOT.TFile.Open("out/%sHistos.root" % s)
                    if ff.IsZombie() or len(ff.GetListOfKeys()) == 0:
                        print( "zombie or zero keys", s)
                        toproc.append((s, samples[s]["files"]))

                except:
                    print( "failed", s)
                    toproc.append((s, samples[s]["files"]))
    else:
        if sys.argv[2][:5] == "model":
            import importlib
            model = importlib.import_module(sys.argv[2])
#	samples=model.samples
            allmc = [y for x in model.background for y in model.background[x]
                     ]+[y for x in model.signal for y in model.signal[x]]
            alldata = [y for x in model.data for y in model.data[x]]
            for x in allmc:
                print (x, "\t", samples[x]["xsec"])
            for x in alldata:
                print( x, "\t", samples[x]["lumi"])

            toproc = [(s, samples[s]["files"])
                      for s in sams if s in allmc+alldata+sys.argv[3:]]

        else:
            toproc = [(s, samples[s]["files"])
                      for s in sams if s in sys.argv[2:]]

print ("Will process", [x[0] for x in toproc])

if nprocesses > 1:
    results = zip(runpool.map(runSample, toproc), [x[0] for x in toproc])
else:
    results = zip([runSample(x) for x in toproc], [x[0] for x in toproc])

print ("Results", results)
print ("To resubmit", [x[1] for x in results if x[0]])

print("time:  ", time.time()-start)