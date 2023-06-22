import ROOT
import correctionlib

correctionlib.register_pyroot_binding()

f = ROOT.TFile.Open("../410F079F-36E5-3945-AA96-8DA05256A477.root")
df = ROOT.ROOT.RDataFrame(f.Get("Events"))

ROOT.gInterpreter.Declare(
    'auto csetEl = correction::CorrectionSet::from_file("btagging.json.gz");'
)
ROOT.gInterpreter.Declare('auto csetEl_2016preID = csetEl->at("deepJet_shape");')
df = df.Filter("nJet >= 1 && Jet_pt[0] > 10. && abs(Jet_eta[0])<1.4").Define(
    "weight",
    'csetEl_2016preID->evaluate({"central", Jet_hadronFlavour[0], abs(Jet_eta[0]), Jet_pt[0], Jet_btagDeepFlavB[0]})',
)

c=ROOT.TCanvas()
h = df.Histo1D("weight")
h.Draw()
c.SaveAs("scale_factor.png")
