import ROOT


rdf = ROOT.ROOT.RDataFrame("Events", "/home/filippo/Downloads/WJetsToLNu.root")

n_neg = rdf.Filter("genWeight < 0").Count().GetValue()

f = n_neg / rdf.Count().GetValue()

n_sample = 470266804
xsec = 763.7
lumi_eff = (n_sample / xsec) * (1 - 2 * f) ** 2

print(lumi_eff, f)
