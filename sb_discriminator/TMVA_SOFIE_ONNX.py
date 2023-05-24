import ROOT
import argparse
import os

input_list = [
    "Z_mass",
    "Z_pt",
    "Dijets_mass",
    "Dijets_pt",
    "MET_pt",
    "ZH_dphi",
    "ZH_deta",
    "ZH_dr",
    "HZ_ptRatio",
    "btag_max",
    "btag_min",
    "jj_dphi",
    "jj_deta",
    "jj_dr",
    "JetBtagMax_pt",
    "JetBtagMin_pt",
    "SoftActivityJetNjets5",
]

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--model", help="Path to the model", type=str
)
args = parser.parse_args()


# Make the header known to the interpreter
ROOT.gInterpreter.ProcessLine('#include "TMVA_SOFIE_ONNX.h"')

ROOT.TMVA_SOFIE_ONNX(ROOT.std.string(args.model))

# compile using ROOT JIT trained model
print("compiling SOFIE model and functor....")
ROOT.gInterpreter.Declare(f'#include "{args.model.replace(".onnx", ".hxx")}"')
modelName = os.path.basename(args.model).replace(".onnx", "")
ROOT.gInterpreter.Declare(f'auto sofie_functor = TMVA::Experimental::SofieFunctor<{len(input_list)},TMVA_SOFIE_'+modelName+'::Session>(0);')

rdf = ROOT.RDataFrame('Events', '~/el/Snapshots/ggZH_Snapshot.root')
# print branches
print("branches in the tree:")
for i in rdf.GetColumnNames():
    print(i)


# loop over input list and put the in the string
eval_string='sofie_functor(rdfslot_,'
for i in input_list:
    eval_string += i+', '
eval_string = eval_string[:-2]+')'
print(eval_string)
h1 = rdf.Define("DNN_Value", eval_string).Histo1D(("h_sig", "", 100, 0, 1),"DNN_Value")

c1 = ROOT.TCanvas()
h1.Draw()
c1.SaveAs("test.png")
c1.close()
