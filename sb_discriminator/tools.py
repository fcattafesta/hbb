import torch
import os
import time
import logging

logger = logging.getLogger(__name__)

def get_model_parameters_number(model):
    params_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return params_num

def train_val_one_epoch(
    train,
    epoch_index,
    #tb_writer,
    model,
    loader,
    loss_fn,
    optimizer,
    num_prints,
    device,
    time_epoch,
    main_dir=None,
    best_loss=None,
    best_accuracy=None,
    best_epoch=None,
    best_model_name=None,
):
    logger.info("Training" if train else "Validation")
    model.train(train)

    running_loss = 0.0
    tot_loss = 0.0

    running_correct = 0
    tot_correct = 0

    running_num = 0
    tot_num = 0

    num_batches = len(loader)
    count = 1

    # Loop over the training data
    for i, data in enumerate(loader):
        inputs, labels = data
        inputs = inputs.to(device)
        weights = inputs[:, -1]
        inputs = inputs[:, :-1]
        labels = labels.to(device)
        if train:
            optimizer.zero_grad()

        outputs = model(inputs)

        # Compute the accuracy
        y_pred = torch.round(outputs)
        correct = (y_pred == labels).sum().item()
        batch_size = labels.size(0)

        # Compute the loss and its gradients
        loss = loss_fn(outputs, labels)

        # reshape the loss
        loss = loss.view(1, -1).squeeze()

        # weight the loss
        loss = loss * weights
        # average the loss
        loss = loss.mean()

        if train:
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

        if i + 1 >= num_batches / num_prints * count:
            count += 1

            last_loss = running_loss * num_prints / num_batches  # loss per batch
            last_accuracy = running_correct / running_num  # accuracy per batch
            tb_x = epoch_index * num_batches + i + 1

            logger.info(
                "EPOCH # %d, time %.1f,  %s batch %.1f %% , step %d        accuracy: %.4f      //      loss: %.4f"
                % (
                    epoch_index,
                    time.time() - time_epoch,
                    "Training" if train else "Validation",
                    (i + 1) / num_batches * 100,
                    tb_x,
                    last_accuracy,
                    last_loss,
                )
            )

            type = "train" if train else "val"
            #tb_writer.add_scalar(f"Accuracy/{type}", last_accuracy, tb_x)
            #tb_writer.add_scalar(f"Loss/{type}", last_loss, tb_x)

            running_loss = 0.0
            running_correct = 0
            running_num = 0

    avg_loss = tot_loss / (i + 1)
    avg_accuracy = tot_correct / tot_num

    # Track best performance, and save the model state
    if not train and avg_loss < best_loss:
        best_loss = avg_loss
        best_accuracy = avg_accuracy
        best_epoch = epoch_index

        model_dir = f"{main_dir}/models"
        os.makedirs(model_dir, exist_ok=True)
        model_name = f"{model_dir}/model_{epoch_index}.pt"
        checkpoint = {
            "epoch": epoch_index,
            "state_dict": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        }
        torch.save(checkpoint, model_name)
        best_model_name = model_name

    return (
        avg_loss,
        avg_accuracy,
        best_loss,
        best_accuracy,
        best_epoch,
        best_model_name,
    )


def eval_model(model, loader, loss_fn, num_prints, type, device, best_epoch):
    # Test the model by running it on the test set
    running_loss = 0.0
    tot_loss = 0.0

    running_correct = 0
    tot_correct = 0

    running_num = 0
    tot_num = 0

    num_batches = len(loader)
    count = 1

    for i, data in enumerate(loader):
        inputs, labels = data
        inputs = inputs.to(device)
        weights = inputs[:, -1]
        inputs = inputs[:, :-1]
        labels = labels.to(device)

        outputs = model(inputs)

        y_pred = torch.round(outputs)
        correct = (y_pred == labels).sum().item()
        batch_size = labels.size(0)

        loss = loss_fn(outputs, labels)

        loss = loss.view(1, -1).squeeze()

        # weight the loss
        loss = loss * weights
        # average the loss
        loss = loss.mean()

        # Gather data for reporting
        running_loss += loss.item()
        tot_loss += loss.item()

        running_correct += correct
        tot_correct += correct

        running_num += batch_size
        tot_num += batch_size

        if i + 1 >= num_batches / num_prints * count:
            count += 1

            last_loss = running_loss * num_batches / num_prints  # loss per batch
            last_accuracy = running_correct / running_num  # accuracy per batch

            logger.info(
                "Evaluating epoch # %d (%s) batch %.1f %%         accuracy: %.4f      //      loss: %.4f"
                % (
                    best_epoch,
                    type,
                    (i + 1) / num_batches * 100,
                    last_accuracy,
                    last_loss,
                )
            )

            running_loss = 0.0
            running_correct = 0
            running_num = 0

        # Create array of scores and labels
        if i == 0:
            all_scores = outputs
            all_labels = labels
        else:
            all_scores = torch.cat((all_scores, outputs))
            all_labels = torch.cat((all_labels, labels))

    avg_loss = tot_loss / (i + 1)
    avg_accuracy = tot_correct / tot_num

    # concatenate all scores and labels
    all_scores = all_scores.view(-1, 1)
    all_labels = all_labels.view(-1, 1)

    score_lbl_tensor = torch.cat((all_scores, all_labels), 1)

    # detach the tensor from the graph and convert to numpy array
    score_lbl_array = score_lbl_tensor.cpu().detach().numpy()

    return score_lbl_array, avg_loss, avg_accuracy


def export_onnx(model, model_name, batch_size, input_size, device):
    # Export the model to ONNX format
    dummy_input = torch.zeros(batch_size, input_size, device=device)
    torch.onnx.export(
        model,
        dummy_input,
        model_name.replace(".pt", ".onnx"),
        verbose=True,
        export_params=True,
        opset_version=13,
        input_names=["InputVariables"],  # the model's input names
        output_names=["Sigmoid"],  # the model's output names
        dynamic_axes={
            "InputVariables": {0: "batch_size"},  # variable length axes
            "Sigmoid": {0: "batch_size"},
        },

    )
