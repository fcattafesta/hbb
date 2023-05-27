import ROOT
import argparse
import os
import sys

sys.path.append("../")
from sb_discriminator.DNN_input_lists import DNN_input_variables
from args_analysis import args

if "DNN_weight" in DNN_input_variables:
    DNN_input_variables.remove("DNN_weight")


def getFlowDNN(model, flow=None):
    #ROOT.gSystem.Load("test_dnn.so")
    ROOT.gInterpreter.Declare('\n#include "test_dnn.h"\n')
    #ROOT.TMVA_SOFIE_ONNX(model)
    eval_string = "sofie_functor(rdfslot_, "#__slot,"
    for i in DNN_input_variables:
        eval_string += i + ", "
    eval_string = eval_string[:-2] + ")"

    #ROOT.gInterpreter.Declare(f'#include "model_DNN.hxx"')

    # test on a RDataFrame
    rdf = ROOT.RDataFrame("Events", "~/el/Snapshots/ggZH_Snapshot.root").Range(100)
    print("branches in the tree:")
    for i in rdf.GetColumnNames():
        print(i)
    h1 = rdf.Define("DNN_Score", eval_string).Histo1D(
        ("h_sig", "", 100, 0, 1), "DNN_Score"
    )
    c1 = ROOT.TCanvas()
    h1.Draw()
    c1.SaveAs("test.png")

    return flow


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to the model", type=str)
    args = parser.parse_args()

    _ = getFlowDNN(args.model)
