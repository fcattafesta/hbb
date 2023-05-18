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

optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)


# Initializing in a separate cell so we can easily add more epochs to the same run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
writer = SummaryWriter("runs/DNN_trainer_{}".format(timestamp))

best_vloss = 1_000_000.0
best_vaccuracy = 0.0
best_epoch = -1

for epoch in range(args.epochs):
    print("EPOCH {}:".format(epoch))

    # Turn on gradients for training
    model.train(True)
    avg_loss, avg_accuracy = train_one_epoch(epoch, writer, model, training_loader, loss_fn, optimizer, batch_size, args.num_prints)

    # Turn off gradients for validation
    model.train(False)
    avg_vloss, avg_vaccuracy, best_vloss, best_vaccuracy, best_epoch = eval_one_epoch(epoch, writer, model, val_loader, loss_fn, timestamp, best_vloss, best_vaccuracy, best_epoch, args.num_prints)

    print("EPOCH # {}: loss train {},  val {}".format(epoch, avg_loss, avg_vloss))
    print("EPOCH # {}: acc train {},  val {}".format(epoch, avg_accuracy, avg_vaccuracy))

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

print("Best val loss: {}".format(best_vloss))
print("Best val accuracy: {}".format(best_vaccuracy))

print("Total time: {}".format(time.time() - start_time))
