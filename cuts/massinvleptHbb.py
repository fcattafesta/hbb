import os
from nail import *
import ROOT
import sys


flow = SampleProcessing(
    "Inv_Mass", "/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/250000/A87275E3-6D57-6A46-8EB2-17F616321665.root")

flow.SubCollection("LHELept", "LHEPart", "abs(LHEPart_pdgId)==13 || abs(LHEPart_pdgId)==11")
flow.Define("LHELept_p4", "@p4v(LHELept)")
flow.Distinct("LHELeptLHELept", "LHELept")
flow.Define("Lept_invMass", "MemberMap(LHELeptLHELept0_p4+LHELeptLHELept1_p4,M())")

nthreads = 10
histos = {}
targets = ["Lept_invMass"]

processor = flow.CreateProcessor(
    "eventProcessor", targets, histos, [], "", nthreads)
rdf = ROOT.RDataFrame(
    "Events", "/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/250000/A87275E3-6D57-6A46-8EB2-17F616321665.root")

result = processor(rdf)

processed_rdf = result.rdf.find("").second
processed_rdf.Snapshot("Events", "out.root", targets)