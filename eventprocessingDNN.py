import ROOT
import argparse
import os
import sys

sys.path.append("../")
from sb_discriminator.DNN_input_lists import DNN_input_variables
from args_analysis import args

if "DNN_weight" in DNN_input_variables:
    DNN_input_variables.remove("DNN_weight")


def getFlowDNN(flow, model, sample_type="data", define=True):

    if flow:
        nthreads = args.nthreads if args.range == -1 else 0
        if model.endswith(".onnx"):
            flow.AddCppCode('\n#include "TMVA_SOFIE_ONNX.h"\n')
        ROOT.TMVA_SOFIE_ONNX(model)

        modelName = os.path.splitext(model)[0]
        nl = "\n"
        if define:
            pass
        print("compiling SOFIE model and functor....")
        # compile using ROOT JIT trained model
        flow.AddCppCode(f'{nl}#include "{modelName}.hxx"{nl}')
        flow.AddCppCode('\n#include <TMVA/SOFIEHelpers.hxx>\n')

        flow.AddCppCode(
            f"{nl}auto sofie_functor_{sample_type} = TMVA::Experimental::SofieFunctor<{len(DNN_input_variables)},TMVA_SOFIE_"
            + os.path.basename(modelName)
            + f"::Session>({nthreads});{nl}"
        )

        eval_string = f"sofie_functor_{sample_type}(__slot,"
        for i in DNN_input_variables:
            eval_string += i + ", "
        eval_string = eval_string[:-2] + ")"

        flow.Define("DNN_Score", eval_string)
        flow.Define("atanhDNN_Score", "atanh(DNN_Score)")

    else:
        ROOT.gInterpreter.Declare('\n#include "TMVA_SOFIE_ONNX.h"\n')
        ROOT.TMVA_SOFIE_ONNX(model)
        modelName = os.path.splitext(model)[0]
        ROOT.gInterpreter.Declare(f'#include "{modelName}.hxx"')
        ROOT.gInterpreter.Declare(
            f"auto sofie_functor = TMVA::Experimental::SofieFunctor<{len(DNN_input_variables)},TMVA_SOFIE_"
            + os.path.basename(modelName)
            + "::Session>(0);"
        )
        # test on a RDataFrame
        eval_string = "sofie_functor(rdfslot_,"
        for i in DNN_input_variables:
            eval_string += i + ", "
        eval_string = eval_string[:-2] + ")"

        rdf = ROOT.RDataFrame("Events", "~/ggZH_Snapshot.root").Range(100)
        print("branches in the tree:")
        for i in rdf.GetColumnNames():
            print(i)
        rdf=rdf.Define("DNN_Score", eval_string)
        rdf=rdf.Define("atanhDNN_Score", "atanh(DNN_Score)")
        h1 = rdf.Histo1D(
            ("h_sig", "", 50, 0, 1), "DNN_Score"
        )
        h2 = rdf.Histo1D(
            ("h_sig", "", 50, 0, 5), "atanhDNN_Score"
        )
        c1 = ROOT.TCanvas()
        h1.Draw()
        c1.SaveAs("test.png")
        c2 = ROOT.TCanvas()
        h2.Draw()
        c2.SaveAs("test2.png")

    return flow


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to the model", type=str)
    args_ = parser.parse_args()

    _ = getFlowDNN(None, args_.model)
