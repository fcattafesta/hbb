import ROOT
import argparse
import os

from input_lists import *

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--model", help="Path to the model", type=str
)
parser.add_argument(
    "-c", "--convert", help="Convert model", action="store_true", default=False
)
args = parser.parse_args()

if args.convert:
    ROOT.gInterpreter.ProcessLine('#include "TMVA_SOFIE_ONNX.h"')
    ROOT.TMVA_SOFIE_ONNX(ROOT.std.string(args.model))


modelName = os.path.splitext(os.path.basename(args.model))[0]

# compile using ROOT JIT trained model
print("compiling SOFIE model and functor....")
ROOT.gInterpreter.Declare(f'#include "{modelName}.hxx"')

ROOT.gInterpreter.Declare(f'auto sofie_functor = TMVA::Experimental::SofieFunctor<{len(DNN_input_variables)},TMVA_SOFIE_'+modelName+'::Session>(0);')

rdf = ROOT.RDataFrame('Events', '~/el/Snapshots/ggZH_Snapshot.root').Range(1000)
# print branches
print("branches in the tree:")
for i in rdf.GetColumnNames():
    print(i)


# loop over input list and put the in the string
eval_string='sofie_functor(rdfslot_,'
for i in DNN_input_variables:
    eval_string += i+', '
eval_string = eval_string[:-2]+')'
print(eval_string)

h1 = rdf.Define("DNN_Value", eval_string).Histo1D(("h_sig", "", 100, 0, 1),"DNN_Value")

c1 = ROOT.TCanvas()
h1.Draw()
c1.SaveAs("test.png")
