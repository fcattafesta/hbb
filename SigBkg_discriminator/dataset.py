import ROOT
import numpy as np
import torch
import sys

from args_dnn import args

batch_size = args.batch_size

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

background_list = [
    "DYZpt-0To50",
    "DYZpt-50To100",
    "DYZpt-100To250",
    "DYZpt-250To400",
    "DYZpt-400To650",
    "DYZpt-650ToInf",
    "ST_tW_antitop_5f_NFHD",
    "ST_tW_antitop_5f_ID",
    "ST_tW_top_5f_NFHD",
    "ST_tW_top_5f_ID",
    "ST_t-channel_antitop_4f_ID",
    "ST_t-channel_top_4f_ID",
    "ST_t-channel_antitop_5f_ID",
    "ST_s-channel_4f_LD",
    "TTTo2L2Nu",
    "TTToSemiLeptonic",
    "TTToHadronic",
    "WZTo2Q2L",
    "WZTo3LNu",
    "WWTo2L2Nu",
    "ZZTo2L2Nu",
    "ZZTo2Q2L",
    "ZZTo4L",
]
signal_list = ["ZH", "ggZH"]

main_dir = "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/snap/Snapshots/"

# list of signal files
sig_files = [main_dir + x + "_Snapshot.root" for x in signal_list]

# list of background files
bkg_files = [main_dir + x + "_Snapshot.root" for x in background_list]


# get input data from a ROOT file and convert it to a torch tensor
sig_train = ROOT.RDataFrame("Events", sig_files)

variables_sig = np.array([sig_train.AsNumpy()[x] for x in input_list])
variables_sig = torch.tensor(variables_sig, device=device, dtype=torch.float32)
ones_array = np.ones_like(sig_train.AsNumpy()["event"], dtype=np.float32)
ones_array = torch.tensor(ones_array, device=device, dtype=torch.float32).unsqueeze(0)

X_sig = (variables_sig, ones_array)

#######################################################
bkg_train = ROOT.RDataFrame(
    "Events",
    bkg_files,
)
variables_bkg = np.array([bkg_train.AsNumpy()[x] for x in input_list])
variables_bkg = torch.tensor(variables_bkg, device=device, dtype=torch.float32)
zeros_array = np.zeros_like(bkg_train.AsNumpy()["event"], dtype=np.float32)
zeros_array = torch.tensor(zeros_array, device=device, dtype=torch.float32).unsqueeze(0)

X_bkg = (variables_bkg, zeros_array)

#######################################################
X_fts = torch.cat((X_sig[0], X_bkg[0]), dim=1).transpose(1, 0)
X_lbl = torch.cat((X_sig[1], X_bkg[1]), dim=1).transpose(1, 0)
X = torch.utils.data.TensorDataset(X_fts, X_lbl)

# split the dataset into training and val sets
train_size = int(0.8 * len(X)) if args.train_size is -1 else args.train_size
val_size = len(X) - train_size if args.val_size is -1 else args.val_size

train_dataset, val_dataset = torch.utils.data.random_split(X, [train_size, val_size])

training_loader = torch.utils.data.DataLoader(train_dataset.dataset, batch_size=batch_size, shuffle=True)

val_loader = torch.utils.data.DataLoader(val_dataset.dataset, batch_size=batch_size, shuffle=True)
