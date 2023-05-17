import ROOT
import numpy as np
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

input_list = [
    "Z_mass",
    "Z_pt",
    "Dijets_mass",
    "Dijets_pt",
    "MET_pt",
    "ZH_dphi",
    "ZH_deta",
    "ZH_dr",
    "HZ_ptRatio",
    "btag_max",
    "btag_min",
    "jj_dphi",
    "jj_deta",
    "jj_dr",
    "JetBtagMax_pt",
    "JetBtagMin_pt",
    "SoftActivityJetNjets5",
]


# get input data from a ROOT file and convert it to a torch tensor
sig_train = ROOT.RDataFrame(
    "Events", "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/test/Snapshots/ZH_Snapshot.root"
)

variables_sig = np.array([sig_train.AsNumpy()[x] for x in input_list])
variables_sig = torch.tensor(variables_sig, device=device, dtype=torch.float32)
ones_array=np.ones_like(sig_train.AsNumpy()["event"], dtype=np.float32)
ones_array = torch.tensor(ones_array, device=device, dtype=torch.float32).unsqueeze(0)

X_sig = (variables_sig,ones_array)
print("train sig: ", X_sig, X_sig[0].size(), X_sig[1].size())

#######################################################
bkg_train = ROOT.RDataFrame(
    "Events",
    "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/test/Snapshots/ZZTo2Q2L_Snapshot.root",
)
variables_bkg = np.array([bkg_train.AsNumpy()[x] for x in input_list])
variables_bkg = torch.tensor(variables_bkg, device=device, dtype=torch.float32)
zeros_array=np.zeros_like(bkg_train.AsNumpy()["event"], dtype=np.float32)
zeros_array = torch.tensor(zeros_array, device=device, dtype=torch.float32).unsqueeze(0)

X_bkg = (variables_bkg,zeros_array)
print("train bkg: ", X_bkg, X_bkg[0].size(), X_bkg[1].size())

#######################################################
X_fts = torch.cat((X_sig[0],X_bkg[0]),dim=1).transpose(1,0)
X_lbl = torch.cat((X_sig[1],X_bkg[1]),dim=1).transpose(1,0)
X = torch.utils.data.TensorDataset(X_fts, X_lbl)
print("X train: ", X, X[0], X[1])

training_loader = torch.utils.data.DataLoader(X, batch_size=batch_size, shuffle=True)
print("training_loader: ", training_loader)

#######################################################
# do the same for validation data
sig_val = ROOT.RDataFrame(
    "Events", "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/test/Snapshots/ggZH_Snapshot.root"
)
variables_sig = np.array([sig_val.AsNumpy()[x] for x in input_list])
variables_sig = torch.tensor(variables_sig, device=device, dtype=torch.float32)
ones_array=np.ones_like(sig_val.AsNumpy()["event"], dtype=np.float32)
ones_array = torch.tensor(ones_array, device=device, dtype=torch.float32).unsqueeze(0)

X_sig = (variables_sig,ones_array)

print("val sig: ", X_sig, X_sig[0].size(), X_sig[1].size())

bkg_val = ROOT.RDataFrame(
    "Events", "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/test/Snapshots/WZTo2Q2L_Snapshot.root"
)
variables_bkg = np.array([bkg_val.AsNumpy()[x] for x in input_list])
variables_bkg = torch.tensor(variables_bkg, device=device, dtype=torch.float32)
zeros_array=np.zeros_like(bkg_val.AsNumpy()["event"], dtype=np.float32)
zeros_array = torch.tensor(zeros_array, device=device, dtype=torch.float32).unsqueeze(0)

X_bkg = (variables_bkg,zeros_array)
print("val bkg: ", X_bkg, X_bkg[0].size(), X_bkg[1].size())


X_fts = torch.cat((X_sig[0],X_bkg[0]),dim=1).transpose(1,0)
X_lbl = torch.cat((X_sig[1],X_bkg[1]),dim=1).transpose(1,0)
X = torch.utils.data.TensorDataset(X_fts, X_lbl)
print("X val: ", X, X[0], X[1])

validation_loader = torch.utils.data.DataLoader(X, batch_size=batch_size, shuffle=False)
print("val_loader: ", validation_loader)
