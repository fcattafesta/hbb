
import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import ROOT
import numpy as np

# PyTorch TensorBoard support
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

batch_size = 8

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
print("len input_list: ", len(input_list))


class DNN(nn.Module):
    def __init__(self, dim_in):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(dim_in, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )

    def forward(self, x):
        # x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

def train_one_epoch(epoch_index, tb_writer):
    running_loss = 0.
    last_loss = 0.

    # Here, we use enumerate(training_loader) instead of
    # iter(training_loader) so that we can track the batch
    # index and do some intra-epoch reporting
    for i, data in enumerate(training_loader):
        # Every data instance is an input + label pair
        inputs, labels = data

        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch
        outputs = model(inputs)
        pred_probab = nn.Softmax(dim=1)(outputs)
        y_pred = pred_probab  # .argmax(1)
        print(f"Predicted class: {y_pred}", y_pred.size())

        # Compute the loss and its gradients
        loss = loss_fn(outputs, labels)
        loss.backward()

        # Adjust learning weights
        optimizer.step()

        # Gather data and report
        running_loss += loss.item()
        if i % 1000 == 999:
            last_loss = running_loss / 1000 # loss per batch
            print('  batch {} loss: {}'.format(i + 1, last_loss))
            tb_x = epoch_index * len(training_loader) + i + 1
            tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.

    return last_loss


# get input data from a ROOT file and convert it to a torch tensor
sig_input_data = ROOT.RDataFrame(
    "Events", "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/test/Snapshots/ggZH_Snapshot.root"
)


variables_sig = np.array([sig_input_data.AsNumpy()[x] for x in input_list])
variables_sig = torch.tensor(variables_sig, device=device, dtype=torch.float32)
ones_array=np.ones_like(sig_input_data.AsNumpy()["event"], dtype=np.float32)
ones_array = torch.tensor(ones_array, device=device, dtype=torch.float32).unsqueeze(0)

X_sig = (variables_sig,ones_array)


print("tensor shape: ", X_sig, X_sig[0].size(), X_sig[1].size())

#######################################################
bkg_input_data = ROOT.RDataFrame(
    "Events",
    "/gpfs/ddn/cms/user/malucchi/hbb_out/mu/test/Snapshots/ZZTo2Q2L_Snapshot.root",
)
variables_bkg = np.array([bkg_input_data.AsNumpy()[x] for x in input_list])
variables_bkg = torch.tensor(variables_bkg, device=device, dtype=torch.float32)
zeros_array=np.zeros_like(bkg_input_data.AsNumpy()["event"], dtype=np.float32)
zeros_array = torch.tensor(zeros_array, device=device, dtype=torch.float32).unsqueeze(0)

X_bkg = (variables_bkg,zeros_array)

print("tensor shape: ", X_bkg, X_bkg[0].size(), X_bkg[1].size())

X=(torch.cat((X_sig[0],X_bkg[0]),dim=1).transpose(1,0), torch.cat((X_sig[1],X_bkg[1]),dim=1).transpose(1,0))
print("X: ", X, X[0].size(), X[1].size())

training_loader = torch.utils.data.DataLoader(X, batch_size=batch_size, shuffle=True)
print("training_loader: ", training_loader)

loss_fn = torch.nn.BCEWithLogitsLoss()

model = DNN(X[0].size(1)).to(device)
print(model)

optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)


# Initializing in a separate cell so we can easily add more epochs to the same run
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
writer = SummaryWriter('runs/fashion_trainer_{}'.format(timestamp))
epoch_number = 0

EPOCHS = 5

best_vloss = 1_000_000.

for epoch in range(EPOCHS):
    print('EPOCH {}:'.format(epoch_number + 1))

    # Make sure gradient tracking is on, and do a pass over the data
    model.train(True)
    avg_loss = train_one_epoch(epoch_number, writer)

    # We don't need gradients on to do reporting
    model.train(False)

    running_vloss = 0.0
    # for i, vdata in enumerate(validation_loader):
    #     vinputs, vlabels = vdata
    #     voutputs = model(vinputs)
    #     vloss = loss_fn(voutputs, vlabels)
    #     running_vloss += vloss

    avg_vloss = running_vloss / (i + 1)
    print('LOSS train {} valid {}'.format(avg_loss, avg_vloss))

    # Log the running loss averaged per batch
    # for both training and validation
    writer.add_scalars('Training vs. Validation Loss',
                    { 'Training' : avg_loss, 'Validation' : avg_vloss },
                    epoch_number + 1)
    writer.flush()

    # Track best performance, and save the model's state
    if avg_vloss < best_vloss:
        best_vloss = avg_vloss
        model_path = 'model_{}_{}'.format(timestamp, epoch_number)
        torch.save(model.state_dict(), model_path)

    epoch_number += 1

#logits = model(X)
# pred_probab = nn.Softmax(dim=1)(logits)
# y_pred = pred_probab  # .argmax(1)
# print(f"Predicted class: {y_pred}", y_pred.size())
