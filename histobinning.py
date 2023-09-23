binningRules = [
    (".*_pt", "30 , 0, 300"),
    ("Dijets_mass", "3000, 50, 200"),
    ("Z.*_mass", "3000, 10, 150"),
    (".*_dphi", "30, 0, 3.2"),
    (".*_deta", "30, 0, 5"),
    (".*_dr", "30, 0, 10"),
    (".*_ptRatio", "30, 0, 2"),
    ("btag.*", "30, 0, 1"),
    ("SoftActivityJetNjets5", "12, -0.5, 11.5"),
    ("DNN_Score", "10000, 0, 1"),
    ("atanhDNN_Score", "10000, 0, 15"),
    ("hadronFlavour_btag.*", "6, -0.5, 5.5"),
    ("LHE_Nb", "6, -0.5, 5.5"),
    (".*btagWeight.*", "100, 0, 10"),
    ("number_of_events", "1, 0.5, 1.5"),
    ("SelectedJet_btagDeep.*B", "100, 0,1"),
    (".*_eta", "30, -3, 3"),
    (".*_phi", "30, -3.2, 3.2"),
    (".*_iso", "30, 0, 0.3"),
    (".*_dxy", "30, 0, 0.6"),
    (".*_dz", "30, 0, 0.6"),
]
binningRules += [(".*_pt_.*", "30, 0, 300")]
binningRules += [
    (jer, "100, 0, 5")
    for jer in [
        "Jet_jerNomSF",
        "Jet_jerUpSF",
        "Jet_jerDownSF",
    ]
]
