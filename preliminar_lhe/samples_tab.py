import ROOT

ROOT.EnableImplicitMT()


file = "/scratchnvme/malucchi/hbb_samples/ST_s-channel_4f_LD/106X_upgrade2018_realistic_v16_L1v1-v1/120000/6F471BFE-BFD5-0847-8C5A-626A7C865EF0.root"
xsec = 0.0072158061930000005
n_samples = 4891000

rdf = ROOT.RDataFrame("Events", file)

# Fraction of negative weights
num_neg_w = rdf.Filter("genWeight < 0").Count().GetValue()
num_tot = rdf.Count().GetValue()
frac_neg_w = num_neg_w / num_tot

# Effective luminosity
eff_lumi = (n_samples / xsec) * (1 - 2 * frac_neg_w) ** 2

# Sum of weights
sumOfWeights = rdf.Sum("genWeight").GetValue()

with open("xsec.csv", "a+") as f:
    if f.tell() == 0:
        f.write("# file sumOfWeights xsec n_samples frac_neg_w eff_lumi \n")
    f.write(f"{file},{sumOfWeights},{xsec},{n_samples},{frac_neg_w},{eff_lumi}\n")
