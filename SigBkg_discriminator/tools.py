import torch
import os


def train_one_epoch(
    epoch_index,
    tb_writer,
    model,
    loader,
    loss_fn,
    timestamp,
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
    for i, data in enumerate(loader):
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

            # write info to file txt
            os.makedirs(f"models/{timestamp}", exist_ok=True)
            with open(f"models/{timestamp}/log.txt", "a") as f:
                f.write(
                    "EPOCH # %d  Training batch %.1f %%         accuracy: %.4f      //      loss: %.4f\n"
                    % (
                        epoch_index,
                        (i + 1) / num_batches * 100,
                        last_accuracy,
                        last_loss,
                    )
                )

            tb_x = epoch_index * len(loader) + i + 1
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
    loader,
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

    for i, data in enumerate(loader):
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

            # write info to file txt
            with open(f"models/{timestamp}/log.txt", "a") as f:
                f.write(
                    "EPOCH # %d  Validation batch %.1f %%         accuracy: %.4f      //      loss: %.4f\n"
                    % (
                        epoch_index,
                        (i + 1) / num_batches * 100,
                        last_accuracy,
                        last_loss,
                    )
                )

            tb_x = epoch_index * len(loader) + i + 1
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

        os.makedirs(f"models/{timestamp}/", exist_ok=True)
        model_name = "models/{}/model_{}.pt".format(timestamp, epoch_index)
        torch.save(model.state_dict(), model_name)
        best_model_name = model_name

    return avg_loss, avg_accuracy, best_loss, best_accuracy, best_epoch, best_model_name


def eval_model(model, loader, batch_prints, num_batches, type):
    # Test the model by running it on the test set
    running_loss = 0.0
    tot_loss = 0.0

    running_correct = 0
    tot_correct = 0

    running_num = 0
    tot_num = 0

    for i, data in enumerate(loader):
        inputs, labels = data
        outputs = model(inputs)
        y_score = torch.sigmoid(outputs)
        y_pred = torch.round(y_score)
        correct = (y_pred == labels).sum().item()
        batch_size = labels.size(0)
        running_correct += correct
        running_num += batch_size

        if (i + 1) % batch_prints == 0:
            last_accuracy = running_correct / running_num
            print(
                "Evaluating (%s) batch %.1f %%         accuracy: %.4f"
                % (type, (i + 1) / num_batches * 100, last_accuracy)
            )
            running_correct = 0
            running_num = 0

        # Create array of scores and labels
        if i == 0:
            all_scores = y_score
            all_labels = labels
        else:
            all_scores = torch.cat((all_scores, y_score))
            all_labels = torch.cat((all_labels, labels))

    print("All scores: ", all_scores, all_scores.size())
    print("All labels: ", all_labels, all_labels.size())
    # concatenate all scores and labels
    all_scores = all_scores.view(-1, 1)
    all_labels = all_labels.view(-1, 1)
    print("All scores: ", all_scores, all_scores.size())
    print("All labels: ", all_labels, all_labels.size())

    score_lbl_tensor = torch.cat((all_scores, all_labels), 1)
    print("scoreiction and label tensor: ", score_lbl_tensor, score_lbl_tensor.size())

    # detach the tensor from the graph and convert to numpy array
    score_lbl_array = score_lbl_tensor.detach().numpy()

    return score_lbl_array