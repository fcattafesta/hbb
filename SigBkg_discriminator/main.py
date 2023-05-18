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
import time

start_time = time.time()

model = DNN(X_fts.size(1)).to(device)
print(model)


loss_fn = torch.nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(model.parameters())


# Initializing in a separate cell so we can easily add more epochs to the same run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
writer = SummaryWriter("runs/DNN_trainer_{}".format(timestamp))

best_vloss = 1_000_000.0
best_vaccuracy = 0.0
best_epoch = -1

for epoch in range(args.epochs):
    print("EPOCH # %d" %epoch)

    # Turn on gradients for training
    train_batch_prints=train_size // batch_size // args.num_prints
    model.train(True)
    avg_loss, avg_accuracy = train_one_epoch(epoch, writer, model, training_loader, loss_fn, optimizer, train_batch_prints)

    # Turn off gradients for validation
    model.train(False)
    val_batch_prints=val_size // batch_size // args.num_prints
    avg_vloss, avg_vaccuracy, best_vloss, best_vaccuracy, best_epoch = eval_one_epoch(epoch, writer, model, val_loader, loss_fn, timestamp, best_vloss, best_vaccuracy, best_epoch, val_batch_prints)

    print("EPOCH # %d: loss train %.4f,  val %.4f" %(epoch, avg_loss, avg_vloss))
    print("EPOCH # %d: acc train %.4f,  val %.4f" %(epoch, avg_accuracy, avg_vaccuracy))
    print("\n\n\n")

    # Log the running loss averaged per batch
    # for both training and validation
    writer.add_scalars(
        "Training vs. Validation Loss",
        {"Training": avg_loss, "Validation": avg_vloss},
        epoch,
    )
    writer.add_scalars(
        "Training vs. Validation Accuracy",
        {"Training": avg_accuracy, "Validation": avg_vaccuracy},
        epoch,
    )

    writer.flush()
    epoch += 1

print("Best epoch: %d" %best_epoch)
print("Best val loss: %.4f" %best_vloss)
print("Best val accuracy: %.4f" %best_vaccuracy)

print("Total time: %.1f" %(time.time() - start_time))
