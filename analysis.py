from multiprocessing import Pool
import psutil
from samples import samples 
import copy
import sys
from nail.nail import *
import ROOT
import traceback
nthreads = 50
nprocesses = 7


#flow = ...  # get the processing flow somewhere
#histosPerSelection = ....  # get the list of histograms to produce for each selection
#flow.binningRules = ....  # set binning rules


flow = SampleProcessing(
    "Analysis", "/scratchnvme/cicco/QCD1/01CD88A2-878C-6446-9D9C-70BFF7D9E19C.root")

flow.Define("isBB", "true")
flow.Define("FatJet_p4", "@p4v(FatJet)")
flow.Define("FatJet_tag", "FatJet_deepTagMD_HbbvsQCD")
flow.SubCollection("SelectedFatJet", "FatJet","FatJet_pt > 300 && abs(FatJet_eta) < 2.4")
flow.Define("FatJetOrder","ROOT::VecOps::Take(ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(SelectedFatJet_tag)),2)")
flow.Selection("twoFatJets","nSelectedFatJet>=2")
flow.ObjectAt("LeadingFJ","SelectedFatJet","FatJetOrder[0]",requires=["twoFatJets"])
flow.ObjectAt("SubLeadingFJ","SelectedFatJet","FatJetOrder[1]",requires=["twoFatJets"])
flow.Selection("PreSelection40","LeadingFJ_msoftdrop > 40 && SubLeadingFJ_msoftdrop > 40 ")
flow.Selection("PreSelection","LeadingFJ_msoftdrop > 50 && SubLeadingFJ_msoftdrop > 50 ")
flow.Selection("PreSelection050","LeadingFJ_msoftdrop > 50 && SubLeadingFJ_msoftdrop > 50 && LeadingFJ_tag > 0.5")
flow.Selection("PreSelection070","LeadingFJ_msoftdrop > 50 && SubLeadingFJ_msoftdrop > 50 && LeadingFJ_tag > 0.7")
flow.Selection("PreSelection080","LeadingFJ_msoftdrop > 50 && SubLeadingFJ_msoftdrop > 50 && LeadingFJ_tag > 0.8")
flow.Selection("PreSelection090","LeadingFJ_msoftdrop > 50 && SubLeadingFJ_msoftdrop > 50 && LeadingFJ_tag > 0.9")

histosPerSelection = {
    "": [ #"LHE_HT",
    "FatJet_pt"
     ],
        "PreSelection": ["LeadingFJ_pt","SubLeadingFJ_pt","SelectedFatJet_pt","LeadingFJ_msoftdrop","LeadingFJ_deepTagMD_HbbvsQCD","SubLeadingFJ_deepTagMD_HbbvsQCD"], #,"LeadingFJ_particleNet_HbbvsQCD","SubLeadingFJ_particleNet_HbbvsQCD"],
        "PreSelection40": ["LeadingFJ_deepTagMD_HbbvsQCD"],
        "PreSelection050": ["LeadingFJ_msoftdrop"],
        "PreSelection070": ["LeadingFJ_msoftdrop"],
        "PreSelection080": ["LeadingFJ_msoftdrop"],
        "PreSelection090": ["LeadingFJ_msoftdrop"],
}

flow.binningRules = [
    (".*_pt", "50,0,1000"),
    (".*_HT", "100,0,3000"),
    (".*drop", "25,0,500"),
    (".*QCD", "25,0,1"),

    ]



flow.CentralWeight("genWeight")  # add a central weight
nthreads=20


proc=flow.CreateProcessor("eventProcessor",["isBB"],histosPerSelection,[],"",nthreads)


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
    subs={}
    if rdf:
        try:
            #add customizations here 
            #rdf = rdf.Define("year", year)
            #rdf = rdf.Define("TriggerSel", trigger)
            if "lumi" in samples[s].keys():
                rdf = rdf.Define("isMC", "false")
                out = procData(rdf)
            else:
                if "subsamples" in samples[s].keys():
                    subs=samples[s]["subsamples"]
                rdf = rdf.Define("isMC", "true")
                out = proc(rdf,subs)
            
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

            for subname in subs :
              outFile = ROOT.TFile.Open("out/%s_%sHistos.root" % (s,subname), "recreate")
              for h in out.histosOutSplit[subname]:
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
toproc = [(s, samples[s]["files"]) for s in sams if "files" in samples[s].keys() and os.path.exists(samples[s]["files"][0])]

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
