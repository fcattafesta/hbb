import ROOT
import argparse
import os
import sys

sys.path.append("../")
from sb_discriminator.DNN_input_lists import DNN_input_variables
from args_analysis import args


def getFlowDNN(model, flow=None):
    if model.endswith(".onnx"):
        if flow is not None:
            flow.AddCppCode('\n#include "TMVA_SOFIE_ONNX.h"\n')
        else:
            ROOT.gInterpreter.Declare('\n#include "TMVA_SOFIE_ONNX.h"\n')
        ROOT.TMVA_SOFIE_ONNX(model)

    modelName = os.path.splitext(model)[0]

    # compile using ROOT JIT trained model
    print("compiling SOFIE model and functor....")
    nl = "\n"
    if flow is not None:
        flow.AddCppCode(f'{nl}#include "{modelName}.hxx"{nl}')
        flow.AddCppCode("\n#include <TMVA/SOFIEHelpers.hxx>\n")
        flow.AddCppCode(
            f"{nl}auto sofie_functor = TMVA::Experimental::SofieFunctor<{len(DNN_input_variables)},TMVA_SOFIE_"
            + os.path.basename(modelName)
            + f"::Session>({args.nthreads});{nl}"
        )
    else:
        ROOT.gInterpreter.Declare(f'#include "{modelName}.hxx"')
        ROOT.gInterpreter.Declare(
            f"auto sofie_functor = TMVA::Experimental::SofieFunctor<{len(DNN_input_variables)},TMVA_SOFIE_"
            + os.path.basename(modelName)
            + "::Session>(0);"
        )

    eval_string = "sofie_functor(__slot,"
    for i in (
        DNN_input_variables.remove("DNN_Score")
        if "DNN_Score" in DNN_input_variables
        else DNN_input_variables
    ):
        eval_string += i + ", "
    eval_string = eval_string[:-2] + ")"

    if flow is not None:
        flow.Define("DNN_Score", eval_string)
    else:
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
