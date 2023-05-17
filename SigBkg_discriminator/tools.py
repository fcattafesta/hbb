import torch
import os

def train_one_epoch(epoch_index, tb_writer, model, training_loader, loss_fn, optimizer, batch_size):
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
        #print(f"out: {outputs}", outputs.size())
        #outputs = nn.Sigmoid(dim=1)(outputs)
        y_pred =torch.round(torch.sigmoid(outputs))
        #print(f"Predicted class: {y_pred}", y_pred.size())


        # Compute the loss and its gradients
        loss = loss_fn(outputs, labels)
        loss.backward()

        # Adjust learning weights
        optimizer.step()

        # Gather data and report
        running_loss += loss.item()
        if i % 10 == 0:
            # accuracy
            correct = (y_pred == labels).float().sum()
            accuracy = correct / batch_size
            print(f"Accuracy: {accuracy}")

            last_loss = running_loss / 10 # loss per batch
            print('  batch {} loss: {}'.format(i + 1, last_loss))
            tb_x = epoch_index * len(training_loader) + i + 1
            tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.

    return last_loss


def eval_one_epoch(epoch_index, tb_writer, model, val_loader, loss_fn, timestamp, best_vloss):
    running_vloss = 0.0
    for i, vdata in enumerate(val_loader):
        vinputs, vlabels = vdata
        voutputs = model(vinputs)
        vloss = loss_fn(voutputs, vlabels)
        running_vloss += vloss

    # validation accuracy
    vpreds = torch.round(torch.sigmoid(voutputs))
    vcorrect = (vpreds == vlabels).sum().item()
    vtotal = vlabels.size(0)
    vaccuracy = vcorrect / vtotal

    avg_vloss = running_vloss / (i + 1)

    # Track best performance, and save the model's state
    if avg_vloss < best_vloss:
        best_vloss = avg_vloss
        if not os.path.exists("models"):
            os.makedirs("models")
        model_path = "models/model_{}_{}".format(timestamp, epoch_number)
        torch.save(model.state_dict(), model_path)

    epoch_number += 1

    if i % 10 == 0:
        print("Validation batch {} accuracy: {}".format(i + 1, vaccuracy))

        last_vloss = running_vloss / 10 # loss per batch
        print('  batch {} val loss: {}'.format(i + 1, last_vloss))
        tb_x = epoch_index * len(val_loader) + i + 1
        tb_writer.add_scalar('Loss/val', last_vloss, tb_x)
        running_vloss = 0.

    return avg_vloss