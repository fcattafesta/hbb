import os
import torch
import numpy as np
from datetime import datetime
import time

# PyTorch TensorBoard support
from torch.utils.tensorboard import SummaryWriter

from dataset import *
from tools import *
from DNN_model import *
from args_dnn import args

if args.histos:
    from sig_bkg_histos import *
if args.history:
    from plot_history import *


if __name__ == "__main__":
    start_time = time.time()

    input_size=X_fts.size(1)
    model = DNN(input_size).to(device)
    print(model)

    loss_fn = torch.nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(model.parameters())
    if args.load_model:
        checkpoint = torch.load(args.load_model)
        model.load_state_dict(checkpoint["state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        loaded_epoch = checkpoint["epoch"]

    # Initializing in a separate cell so we can easily add more epochs to the same run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_dir = f"out/{timestamp}"
    os.makedirs(main_dir, exist_ok=True)
    writer = SummaryWriter(f"runs/DNN_trainer_{timestamp}")

    best_vloss = 1_000_000.0
    best_vaccuracy = 0.0
    best_epoch = -1
    best_model_name = ""

    train_accuracy, train_loss, val_accuracy, val_loss = [], [], [], []

    train_batch_prints = train_size // batch_size // args.num_prints
    num_train_batches = train_size // batch_size

    if not args.eval_model:
        val_batch_prints = val_size // batch_size // args.num_prints
        num_val_batches = val_size // batch_size
        for epoch in range(args.epochs):
            if args.load_model and epoch < loaded_epoch:
                continue
            time_epoch = time.time()
            # Turn on gradients for training
            print("\nTraining \n")
            model.train(True)

            avg_loss, avg_accuracy, train_accuracy, train_loss = train_one_epoch(
                main_dir,
                epoch,
                writer,
                model,
                training_loader,
                loss_fn,
                optimizer,
                train_batch_prints,
                num_train_batches,
                train_accuracy,
                train_loss,
            )

            print("time elapsed: {:.2f}s".format(time.time() - time_epoch))

            print("\nValidation \n")
            # Turn off gradients for validation
            model.train(False)

            (
                avg_vloss,
                avg_vaccuracy,
                best_vloss,
                best_vaccuracy,
                best_epoch,
                best_model_name,
                val_accuracy,
                val_loss,
            ) = val_one_epoch(
                main_dir,
                epoch,
                writer,
                model,
                val_loader,
                loss_fn,
                best_vloss,
                best_vaccuracy,
                best_epoch,
                val_batch_prints,
                num_val_batches,
                best_model_name,
                val_accuracy,
                val_loss,
                optimizer,
            )

            print(
                "EPOCH # %d: loss train %.4f,  val %.4f" % (epoch, avg_loss, avg_vloss)
            )
            print(
                "EPOCH # %d: acc train %.4f,  val %.4f"
                % (epoch, avg_accuracy, avg_vaccuracy)
            )

            print("\n\n\n")
            print(
                "Best epoch: %d, best val loss: %.4f, best val accuracy: %.4f"
                % (best_epoch, best_vloss, best_vaccuracy)
            )

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
            print("time elapsed: {:.2f}s".format(time.time() - time_epoch))

        if args.history:
            # plot the training and validation loss and accuracy
            print("\n\n\n")
            print("Plotting training and validation loss and accuracy")
            plot_history(
                train_accuracy,
                train_loss,
                val_accuracy,
                val_loss,
                main_dir,
                False,
            )
        if args.onnx:
            # export the model to ONNX
            print("\n\n\n")
            print("Exporting model to ONNX")
            model.train(False)
            export_onnx(model, best_model_name, batch_size, input_size, input_list, ["sigmoid"], device)

    if args.eval or args.eval_model:
        # evaluate model on test_dataset loadining the best model
        print("\n\n\n")
        print("Evaluating best model on test and train dataset")
        print("================================")

        test_batch_prints = test_size // batch_size // args.num_prints
        num_test_batches = test_size // batch_size

        # load best model
        model.load_state_dict(
            torch.load(best_model_name if not args.eval_model else args.eval_model)[
                "state_dict"
            ]
        )
        model.train(False)

        print("Training dataset\n")
        score_lbl_array_train = eval_model(
            model, training_loader, train_batch_prints, num_train_batches, "training"
        )
        print("\nTest dataset")
        score_lbl_array_test = eval_model(
            model, test_loader, test_batch_prints, num_test_batches, "test"
        )

        # plot the signal and background distributions
        if args.histos:
            print("\n\n\n")
            print("Plotting signal and background distributions")
            plot_sig_bkg_distributions(
                score_lbl_array_train, score_lbl_array_test, main_dir, False
            )

        # create the directory for labels with time stamp
        # save array with labels and score for train and test in the same file .npz
        np.savez(
            f"{main_dir}/score_lbl_array.npz",
            score_lbl_array_train=score_lbl_array_train,
            score_lbl_array_test=score_lbl_array_test,
        )

        print("Saved score_lbl_array.npy in %s" % main_dir)

    print("Total time: %.1f" % (time.time() - start_time))
