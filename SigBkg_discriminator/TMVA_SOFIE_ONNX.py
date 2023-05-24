import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--model", help="Path to the model", type=str
)
args = parser.parse_args()


# Make the header known to the interpreter
ROOT.gInterpreter.ProcessLine('#include "TMVA_SOFIE_ONNX.h"')

ROOT.TMVA_SOFIE_ONNX(args.model)