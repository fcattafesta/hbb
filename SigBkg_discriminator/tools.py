import torch
import os
import matplotlib.pyplot as plt


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

        if (i + 1) % batch_prints == 0:
            last_loss = running_loss / batch_prints  # loss per batch
            last_accuracy = running_correct / running_num  # accuracy per batch
            print(
                "EPOCH # %d  Training batch %.1f %%         accuracy: %.4f      //      loss: %.4f"
                % (epoch_index, (i + 1) / num_batches * 100, last_accuracy, last_loss)
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
    best_model_name,
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

        if (i + 1) % batch_prints == 0:
            last_loss = running_loss / batch_prints  # loss per batch
            last_accuracy = running_correct / running_num  # accuracy per batch

            print(
                "EPOCH # %d  Validation batch %.1f %%         accuracy: %.4f      //      loss: %.4f"
                % (epoch_index, (i + 1) / num_batches * 100, last_accuracy, last_loss)
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
            os.makedirs(f"models/{timestamp}/")
        model_name = "models/{}/model_{}.pt".format(timestamp, epoch_index)
        torch.save(model.state_dict(), model_name)
        best_model_name = model_name

    return avg_loss, avg_accuracy, best_loss, best_accuracy, best_epoch, best_model_name


def test_model(model, test_loader, test_batch_prints, num_test_batches):
    # Test the model by running it on the test set
    running_loss = 0.0
    tot_loss = 0.0

    running_correct = 0
    tot_correct = 0

    running_num = 0
    tot_num = 0

    for i, data in enumerate(test_loader):
        inputs, labels = data
        outputs = model(inputs)
        y_pred = torch.round(torch.sigmoid(outputs))
        correct = (y_pred == labels).sum().item()
        batch_size = labels.size(0)
        running_correct += correct
        running_num += batch_size

        if (i + 1) % test_batch_prints == 0:
            last_accuracy = running_correct / running_num
            print(
                "Testing batch %.1f %%         accuracy: %.4f"
                % ((i + 1) / num_test_batches * 100, last_accuracy)
            )
            running_correct = 0
            running_num = 0

        # Create array of predictions and labels
        if i == 0:
            all_preds = y_pred
            all_labels = labels
        else:
            all_preds = torch.cat((all_preds, y_pred))
            all_labels = torch.cat((all_labels, labels))

    # concatenate all predictions and labels
    all_preds = all_preds.view(-1, 1)
    all_labels = all_labels.view(-1, 1)

    pred_lbl_tensor = torch.cat((all_preds, all_labels), 1)

    return pred_lbl_tensor


def plot_sig_bkg_distributions(pred_lbl_tensor):
    # plot the signal and background distributions for the test dataset using the best model as a function of the DNN output
    sig = pred_lbl_tensor[pred_lbl_tensor[:, 1] == 1]
    bkg = pred_lbl_tensor[pred_lbl_tensor[:, 1] == 0]

    sig_pred = sig[:, 0]
    bkg_pred = bkg[:, 0]

    plt.figure()
    plt.hist(
        sig_pred,
        bins=50,
        range=(0, 1),
        histtype="step",
        label="Signal",
        density=True,
        color="blue",
    )
    plt.hist(
        bkg_pred,
        bins=50,
        range=(0, 1),
        histtype="step",
        label="Background",
        density=True,
        color="red",
    )
    plt.xlabel("DNN output")
    plt.ylabel("Normalized counts")
    plt.legend()
    plt.show()

    plt.savefig("sig_bkg_distributions.png")
