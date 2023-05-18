import torch
import os


def train_one_epoch(
    epoch_index,
    tb_writer,
    model,
    training_loader,
    loss_fn,
    optimizer,
    batch_prints,
    num_batches,
):
    running_loss = 0.0
    tot_loss = 0.0

    running_correct = 0
    tot_correct = 0

    running_num = 0
    tot_num = 0

    # Loop over the training data
    for i, data in enumerate(training_loader):
        inputs, labels = data
        optimizer.zero_grad()

        outputs = model(inputs)

        # Compute the accuracy
        y_pred = torch.round(torch.sigmoid(outputs))
        correct = (y_pred == labels).sum().item()
        batch_size = labels.size(0)

        # Compute the loss and its gradients
        loss = loss_fn(outputs, labels)
        loss.backward()

        # Adjust learning weights
        optimizer.step()

        # Gather data for reporting
        running_loss += loss.item()
        tot_loss += loss.item()

        running_correct += correct
        tot_correct += correct

        running_num += batch_size
        tot_num += batch_size

        if i % batch_prints == 0 and i > 0:
            last_loss = running_loss / batch_prints  # loss per batch
            last_accuracy = running_correct / running_num  # accuracy per batch
            print(
                "EPOCH # %d  Training batch %.2f %%         accuracy: %.4f      //      loss: %.4f"
                % (epoch_index, (i + 1) / num_batches, last_accuracy, last_loss)
            )

            tb_x = epoch_index * len(training_loader) + i + 1
            tb_writer.add_scalar("Accuracy/train", last_accuracy, tb_x)
            tb_writer.add_scalar("Loss/train", last_loss, tb_x)

            running_loss = 0.0
            running_correct = 0
            running_num = 0

    avg_loss = tot_loss / (i + 1)  # loss per epoch
    avg_accuracy = tot_correct / tot_num  # accuracy per epoch

    return avg_loss, avg_accuracy


def eval_one_epoch(
    epoch_index,
    tb_writer,
    model,
    val_loader,
    loss_fn,
    timestamp,
    best_loss,
    best_accuracy,
    best_epoch,
    batch_prints,
    num_batches,
):
    running_loss = 0.0
    tot_loss = 0.0

    running_correct = 0
    tot_correct = 0

    running_num = 0
    tot_num = 0

    for i, data in enumerate(val_loader):
        inputs, labels = data
        outputs = model(inputs)

        # Compute the accuracy
        y_pred = torch.round(torch.sigmoid(outputs))
        correct = (y_pred == labels).sum().item()
        batch_size = labels.size(0)

        loss = loss_fn(outputs, labels)

        # Gather data for reporting
        running_loss += loss.item()
        tot_loss += loss.item()

        running_correct += correct
        tot_correct += correct

        running_num += batch_size
        tot_num += batch_size

        if i % batch_prints == 0 and i > 0:
            last_loss = running_loss / batch_prints  # loss per batch
            last_accuracy = running_correct / running_num  # accuracy per batch

            print(
                "EPOCH # %d  Validation batch %.2f %%         accuracy: %.4f      //      loss: %.4f"
                % (epoch_index, (i + 1) / num_batches, last_accuracy, last_loss)
            )

            tb_x = epoch_index * len(val_loader) + i + 1
            tb_writer.add_scalar("Accuracy/val", last_accuracy, tb_x)
            tb_writer.add_scalar("Loss/val", last_loss, tb_x)

            running_loss = 0.0
            running_correct = 0
            running_num = 0

    avg_loss = tot_loss / (i + 1)
    avg_accuracy = tot_correct / tot_num

    # Track best performance, and save the model's state
    if avg_loss < best_loss:
        best_loss = avg_loss
        best_accuracy = avg_accuracy
        best_epoch = epoch_index

        if not os.path.exists("models"):
            os.makedirs("models")
        model_path = "models/model_{}_{}".format(timestamp, epoch_index)
        torch.save(model.state_dict(), model_path)

    return avg_loss, avg_accuracy, best_loss, best_accuracy, best_epoch
