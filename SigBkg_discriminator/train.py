import torch

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

        # accuracy
        correct = (y_pred == labels).float().sum()
        accuracy = correct / batch_size
        print(f"Accuracy: {accuracy}")

        # Compute the loss and its gradients
        loss = loss_fn(outputs, labels)
        loss.backward()

        # Adjust learning weights
        optimizer.step()

        # Gather data and report
        running_loss += loss.item()
        #if i % 1000 == 999:
        last_loss = running_loss / 1000 # loss per batch
        print('  batch {} loss: {}'.format(i + 1, last_loss))
        tb_x = epoch_index * len(training_loader) + i + 1
        tb_writer.add_scalar('Loss/train', last_loss, tb_x)
        running_loss = 0.

    return last_loss