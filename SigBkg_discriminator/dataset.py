import uproot
import numpy as np
import torch
import math
import sys

from args_dnn import args

batch_size = args.batch_size

if args.gpu:
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
#device = 0 if torch.cuda.is_available() else "cpu"
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

signal_list = ["ZH", "ggZH"]
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

if args.data_dirs:
    dirs = args.data_dirs


# list of signal files
sig_files = []
for x in dirs:
    sig_files += [x + y + "_Snapshot.root" for y in signal_list]


# open each file and get the Events tree using uproot
for i, file in enumerate(sig_files):
    sig_train = uproot.open(f"{file}:Events")
    variables_sig_array = np.array(
        [sig_train[input].array(library="np") for input in input_list]
    )
    # concatenate all the variables into a single torch tensor
    if i == 0:
        variables_sig = torch.tensor(
            variables_sig_array, device=device, dtype=torch.float32
        )[:, : math.ceil((args.train_size + args.val_size + args.test_size) / 2)]
    else:
        variables_sig = torch.cat(
            (
                variables_sig,
                torch.tensor(variables_sig_array, device=device, dtype=torch.float32),
            ), dim=1
        )[:, : math.ceil((args.train_size + args.val_size + args.test_size) / 2)]

ones_tensor = torch.ones_like(
    variables_sig[0], device=device, dtype=torch.float32
).unsqueeze(0)

X_sig = (variables_sig, ones_tensor)


#######################################################
bkg_files = []
for x in dirs:
    bkg_files += [x + y + "_Snapshot.root" for y in background_list]


for i, file in enumerate(bkg_files):
    bkg_train = uproot.open(f"{file}:Events")
    variables_bkg_array = np.array(
        [bkg_train[input].array(library="np") for input in input_list]
    )
    if i == 0:
        variables_bkg = torch.tensor(
            variables_bkg_array, device=device, dtype=torch.float32
        )[:, : math.floor((args.train_size + args.val_size + args.test_size) / 2)]
    else:
        variables_bkg = torch.cat(
            (
                variables_bkg,
                torch.tensor(variables_bkg_array, device=device, dtype=torch.float32),
            ), dim=1
        )[:, : math.floor((args.train_size + args.val_size + args.test_size) / 2)]

zeros_tensor = torch.zeros_like(
    variables_bkg[0], device=device, dtype=torch.float32
).unsqueeze(0)

X_bkg = (variables_bkg, zeros_tensor)

#######################################################
X_fts = torch.cat((X_sig[0], X_bkg[0]), dim=1).transpose(1, 0)
X_lbl = torch.cat((X_sig[1], X_bkg[1]), dim=1).transpose(1, 0)

# split the dataset into training and val sets
if args.train_size != -1 and args.val_size != -1 and args.test_size != -1:
    X_fts = X_fts[: args.train_size + args.val_size + args.test_size, :]
    X_lbl = X_lbl[: args.train_size + args.val_size + args.test_size, :]


X = torch.utils.data.TensorDataset(X_fts, X_lbl)


train_size = int(0.8 * len(X)) if args.train_size == -1 else args.train_size
val_size = math.ceil((len(X) - train_size) / 2)
test_size = math.floor((len(X) - train_size) / 2)

print(f"Total size: {len(X)}")
print(f"Training size: {train_size}")
print(f"Validation size: {val_size}")
print(f"Test size: {test_size}")

gen = torch.Generator()
gen.manual_seed(0)
train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
    X, [train_size, val_size, test_size], generator=gen
)

# check size of the dataset
print("Training dataset size:", len(train_dataset))
print("Validation dataset size:", len(val_dataset))
print("Test dataset size:", len(test_dataset))

training_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=args.num_workers,
    drop_last=True,
)

val_loader = torch.utils.data.DataLoader(
    val_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=args.num_workers,
    drop_last=True,
)

test_loader = torch.utils.data.DataLoader(
    test_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=args.num_workers,
    drop_last=True,
)


# check size of the loader
print("Training loader size:", len(training_loader))
print("Validation loader size:", len(val_loader))
print("Test loader size:", len(test_loader))
