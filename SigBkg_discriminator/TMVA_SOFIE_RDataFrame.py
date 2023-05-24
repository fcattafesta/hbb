import ROOT
from os.path import exists

ROOT.TMVA.PyMethodBase.PyInitialize()


# check if the input file exists
modelFile = "model_0.onnx"

# parse the input Keras model into RModel object
model = ROOT.TMVA.Experimental.SOFIE.PyKeras.Parse(modelFile)

# generating inference code
model.Generate()
model.OutputGenerated("model_torch_0.hxx")
model.PrintGenerated()

# compile using ROOT JIT trained model
print("compiling SOFIE model and functor....")
ROOT.gInterpreter.Declare('#include "model_torch_0.hxx"')
modelName = "model_torch_0"
ROOT.gInterpreter.Declare('auto sofie_functor = TMVA::Experimental::SofieFunctor<7,TMVA_SOFIE_'+modelName+'::Session>(0);')

# # run inference over input data
# inputFile = "http://root.cern/files/Higgs_data.root"
# df1 = ROOT.RDataFrame("sig_tree", inputFile)
# h1 = df1.Define("DNN_Value", "sofie_functor(rdfslot_,m_jj, m_jjj, m_lv, m_jlv, m_bb, m_wbb, m_wwbb)").Histo1D(("h_sig", "", 100, 0, 1),"DNN_Value")

# df2 = ROOT.RDataFrame("bkg_tree", inputFile)
# h2 = df2.Define("DNN_Value", "sofie_functor(rdfslot_,m_jj, m_jjj, m_lv, m_jlv, m_bb, m_wbb, m_wwbb)").Histo1D(("h_bkg", "", 100, 0, 1),"DNN_Value")

# # run over the input data once, combining both RDataFrame graphs.
# ROOT.RDF.RunGraphs([h1, h2]);

# print("Number of signal entries",h1.GetEntries())
# print("Number of background entries",h2.GetEntries())

# h1.SetLineColor(ROOT.kRed)
# h2.SetLineColor(ROOT.kBlue)

# c1 = ROOT.TCanvas()
# ROOT.gStyle.SetOptStat(0)

# h2.DrawClone()
# h1.DrawClone("SAME")