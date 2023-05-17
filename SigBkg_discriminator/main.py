from dataset import *
from tools import *
from DNN_model import *
from args_dnn import args

import os
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import ROOT
import numpy as np

# PyTorch TensorBoard support
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime







model = DNN(X_fts.size(1)).to(device)
print(model)


loss_fn = torch.nn.BCEWithLogitsLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)


# Initializing in a separate cell so we can easily add more epochs to the same run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
writer = SummaryWriter("runs/DNN_trainer_{}".format(timestamp))
epoch_number = 0

EPOCHS = args.epochs

best_vloss = 1_000_000.0

for epoch in range(EPOCHS):
    print("EPOCH {}:".format(epoch_number + 1))

    # Make sure gradient tracking is on, and do a pass over the data
    model.train(True)
    avg_loss = train_one_epoch(epoch_number, writer, model, training_loader, loss_fn, optimizer, batch_size, args.num_prints)

    # We don't need gradients on to do reporting
    model.train(False)

    avg_vloss = eval_one_epoch(epoch_number, writer, model, val_loader, loss_fn, timestamp, best_vloss, args.num_prints)


    print("LOSS train {} valid {}".format(avg_loss, avg_vloss))

    # Log the running loss averaged per batch
    # for both training and validation
    writer.add_scalars(
        "Training vs. Validation Loss",
        {"Training": avg_loss, "Validation": avg_vloss},
        epoch_number + 1,
    )
    writer.flush()
