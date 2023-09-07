import ROOT

ROOT.EnableImplicitMT()

files = [
    "/scratchnvme/malucchi/hbb_samples/ST_s-channel_4f_LD/106X_upgrade2018_realistic_v16_L1v1-v1/120000/6F471BFE-BFD5-0847-8C5A-626A7C865EF0.root",
    "/scratchnvme/malucchi/hbb_samples/ggZH/106X_upgrade2018_realistic_v16_L1v1-v1/2520000/1412A75E-6CBA-5142-914D-2FE8356F680C.root",
    "/scratchnvme/malucchi/hbb_samples/ST_t-channel_antitop_4f_ID/106X_upgrade2018_realistic_v16_L1v1-v1/2540000/8288F355-084C-0541-B8CD-EA2DE15FA214.root",
    "/scratchnvme/malucchi/hbb_samples/ST_t-channel_antitop_5f_ID/106X_upgrade2018_realistic_v16_L1v1-v1/2430000/4DEC0180-DAA7-AE42-84C2-9A5C74823674.root",
    "/scratchnvme/malucchi/hbb_samples/ST_t-channel_top_4f_ID/106X_upgrade2018_realistic_v16_L1v1-v1/2540000/0D659B3B-F2D9-8341-9EB1-1EFCD1807617.root",
    "/scratchnvme/malucchi/hbb_samples/ST_tW_antitop_5f_ID/106X_upgrade2018_realistic_v16_L1v1-v2/230000/6371B801-DE75-5B4B-A781-98523A058E30.root",
    "/scratchnvme/malucchi/hbb_samples/ST_tW_antitop_5f_NFHD/106X_upgrade2018_realistic_v16_L1v1-v1/120000/2F285346-84D3-E347-82E9-26F8D04103BF.root",
    "/scratchnvme/malucchi/hbb_samples/ST_tW_top_5f_ID/106X_upgrade2018_realistic_v16_L1v1-v2/100000/60FB6FDE-25EA-6C4E-80E5-96ED7EF8C294.root",
    "/scratchnvme/malucchi/hbb_samples/ST_tW_top_5f_NFHD/106X_upgrade2018_realistic_v16_L1v1-v1/120000/2C21C6AB-549E-B84D-96DC-F6BB8D3F3DD5.root",
    "/scratchnvme/malucchi/hbb_samples/TTTo2L2Nu/106X_upgrade2018_realistic_v16_L1v1-v1/70000/1F39E43A-2869-4540-8A95-B46F63B7D7B0.root",
    "/scratchnvme/malucchi/hbb_samples/TTToHadronic/106X_upgrade2018_realistic_v16_L1v1-v1/70000/195480E4-5D1B-9542-B8C4-CFAAF97C624E.root",
    "/scratchnvme/malucchi/hbb_samples/TTToSemiLeptonic/106X_upgrade2018_realistic_v16_L1v1-v1/70000/67FF016B-0F26-BF44-AD35-080622EB52EE.root",
    "/scratchnvme/malucchi/hbb_samples/WWTo2L2Nu/106X_upgrade2018_realistic_v16_L1v1-v2/100000/DDE0E00A-D9CE-004B-B973-9F4BE582BE78.root",
    "/scratchnvme/malucchi/hbb_samples/WZTo2Q2L/106X_upgrade2018_realistic_v16_L1v1-v1/80000/5203227E-C1DE-B54F-B206-B77EF0735D91.root",
    "/scratchnvme/malucchi/hbb_samples/WZTo3LNu/106X_upgrade2018_realistic_v16_L1v1-v2/40000/405F159E-56A2-5449-9C99-D0B78DBDEA87.root",
    "/scratchnvme/malucchi/hbb_samples/ZH/106X_upgrade2018_realistic_v16_L1v1-v1/40000/7848EBE7-31CC-FA45-9D9E-14F8FC15AE13.root",
    "/scratchnvme/malucchi/hbb_samples/ZZTo2L2Nu/106X_upgrade2018_realistic_v16_L1v1-v1/70000/691B674F-83CA-0140-9754-14863CD3B950.root",
    "/scratchnvme/malucchi/hbb_samples/ZZTo2Q2L/106X_upgrade2018_realistic_v16_L1v1-v1/80000/8041015B-1FB7-F14B-8B4A-33AFD5EA88EA.root",
    "/scratchnvme/malucchi/hbb_samples/ZZTo4L/106X_upgrade2018_realistic_v16_L1v1-v2/70000/B291AA40-0B34-484D-9523-AB8E31F8B9D9.root",
]

names = [
    "ST_s-channel_4f_LD",
    "ggZH",
    "ST_t-channel_antitop_4f_ID",
    "ST_t-channel_antitop_5f_ID",
    "ST_t-channel_top_4f_ID",
    "ST_tW_antitop_5f_ID",
    "ST_tW_antitop_5f_NFHD",
    "ST_tW_top_5f_ID",
    "ST_tW_top_5f_NFHD",
    "TTTo2L2Nu",
    "TTToHadronic",
    "TTToSemiLeptonic",
    "WWTo2L2Nu",
    "WZTo2Q2L",
    "WZTo3LNu",
    "ZH",
    "ZZTo2L2Nu",
    "ZZTo2Q2L",
    "ZZTo4L",
]

xsecs = [
    3.36,
    0.0072158061930000005,
    80.95,
    80.95,
    136.02,
    35.85,
    19.56,
    35.85,
    19.56,
    85.65,
    366.20,
    356.19,
    5.405545772,
    2.1378257075700002,
    1.01571116658,
    0.05162528008,
    0.333731554,
    2.333117294014,
    0.16851774819230003,
]
n_samples = [
    19365999,
    4891000,
    95627000,
    98934000,
    178336000,
    7749000,
    10949620,
    7956000,
    11270430,
    145020000,
    334206000,
    476408000,
    9994000,
    28576996,
    9821283,
    4885835,
    56886000,
    29357938,
    98488000,
]

eff_lumi = []
frac_neg_w = []
sum_of_weights = []

for i in range(len(files)):
    rdf = ROOT.RDataFrame("Events", files[i])
    # Fraction of negative weights
    num_neg_w = rdf.Filter("genWeight < 0").Count().GetValue()
    num_tot = rdf.Count().GetValue()
    frac_neg_w.append(num_neg_w / num_tot)
    # Effective luminosity
    eff_lumi.append((n_samples[i] / xsecs[i]) * (1 - 2 * frac_neg_w[i]) ** 2)
    # Sum of weights
    sum_of_weights.append(rdf.Sum("genWeight").GetValue())

# write the table
with open("xsec.csv", "w") as f:
    f.write(
        "#Sample, Cross section, Sum of weights, Negative Fraction, Dataset Events, Effective luminosity\n"
    )
    for i in range(len(files)):
        f.write(
            f"{names[i]},{xsecs[i]},{sum_of_weights[i]},{frac_neg_w[i]},{n_samples[i]},{eff_lumi[i]}\n"
        )
