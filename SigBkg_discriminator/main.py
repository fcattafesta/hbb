from dataset import *
from train import *
from DNN_model import *

import os
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import ROOT
import numpy as np

# PyTorch TensorBoard support
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime




batch_size = 8



model = DNN(X_fts.size(1)).to(device)
print(model)



# Initializing in a separate cell so we can easily add more epochs to the same run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
writer = SummaryWriter("runs/DNN_trainer_{}".format(timestamp))
epoch_number = 0

EPOCHS = 5

best_vloss = 1_000_000.0

for epoch in range(EPOCHS):
    print("EPOCH {}:".format(epoch_number + 1))

    # Make sure gradient tracking is on, and do a pass over the data
    model.train(True)
    avg_loss = train_one_epoch(epoch_number, writer)

    # We don't need gradients on to do reporting
    model.train(False)

    running_vloss = 0.0
    for i, vdata in enumerate(validation_loader):
        vinputs, vlabels = vdata
        voutputs = model(vinputs)
        vloss = loss_fn(voutputs, vlabels)
        running_vloss += vloss

        # validation accuracy
        vpreds = torch.round(torch.sigmoid(voutputs))
        vcorrect = (vpreds == vlabels).sum().item()
        vtotal = vlabels.size(0)
        vaccuracy = vcorrect / vtotal
        print("Validation batch {} accuracy: {}".format(i + 1, vaccuracy))

    avg_vloss = running_vloss / (i + 1)
    print("LOSS train {} valid {}".format(avg_loss, avg_vloss))

    # Log the running loss averaged per batch
    # for both training and validation
    writer.add_scalars(
        "Training vs. Validation Loss",
        {"Training": avg_loss, "Validation": avg_vloss},
        epoch_number + 1,
    )
    writer.flush()

    # Track best performance, and save the model's state
    if avg_vloss < best_vloss:
        best_vloss = avg_vloss
        model_path = "models/model_{}_{}".format(timestamp, epoch_number)
        torch.save(model.state_dict(), model_path)

    epoch_number += 1
