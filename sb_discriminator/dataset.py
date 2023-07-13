import uproot
import numpy as np
import torch
import math
import logging
import os

from DNN_input_lists import (
    DNN_input_variables,
    signal_list,
    background_list,
    background_list_noVV,
)

logger = logging.getLogger(__name__)


def load_data(args):
    batch_size = args.batch_size
    logger.info(f"Batch size: {batch_size}")

    dirs = args.data_dirs

    dimension = (args.train_size + args.val_size + args.test_size) / 2
    logger.info("Variables: %s", DNN_input_variables)

    # list of signal and background files
    sig_files = []
    bkg_files = []
    for x in dirs:
        files = os.listdir(x)
        for file in files:
            for signal in signal_list:
                if signal in file and "SR" in file:
                    sig_files.append(x + file)
            for background in background_list_noVV if args.noVV else background_list:
                if background in file and "SR" in file:
                    bkg_files.append(x + file)

    # open each file and get the Events tree using uproot
    for i, file in enumerate(sig_files):
        logger.info(f"Loading file {file}")
        sig_file = uproot.open(f"{file}:Events")
        variables_sig_array = np.array(
            [sig_file[input].array(library="np") for input in DNN_input_variables]
        )
        # concatenate all the variables into a single torch tensor
        if i == 0:
            variables_sig = torch.tensor(variables_sig_array, dtype=torch.float32)[
                :, : math.ceil(dimension)
            ]
        else:
            variables_sig = torch.cat(
                (
                    variables_sig,
                    torch.tensor(variables_sig_array, dtype=torch.float32),
                ),
                dim=1,
            )[:, : math.ceil(dimension)]

    logger.info(f"number of signal events: {variables_sig.shape[1]}")

    # sum of weights
    sumw_sig = variables_sig[-1].sum()
    logger.info(f"sum of weights sig: {sumw_sig}")

    # multiply the weights by the weight factor
    variables_sig[-1] = variables_sig[-1] * args.weights[0]

    sumw_sig = variables_sig[-1].sum()
    logger.info(f"sum of weights sig: {sumw_sig}")

    ones_tensor = torch.ones_like(variables_sig[0], dtype=torch.float32).unsqueeze(0)

    X_sig = (variables_sig, ones_tensor)

    #######################################################
    for i, file in enumerate(bkg_files):
        logger.info(f"Loading file {file}")
        bkg_file = uproot.open(f"{file}:Events")
        variables_bkg_array = np.array(
            [bkg_file[input].array(library="np") for input in DNN_input_variables]
        )
        if i == 0:
            variables_bkg = torch.tensor(variables_bkg_array, dtype=torch.float32)[
                :, : math.floor(dimension)
            ]
        else:
            variables_bkg = torch.cat(
                (
                    variables_bkg,
                    torch.tensor(variables_bkg_array, dtype=torch.float32),
                ),
                dim=1,
            )[:, : math.floor(dimension)]

    logger.info(f"number of background events: {variables_bkg.shape[1]}")

    # sum of weights
    sumw_bkg = variables_bkg[-1].sum()
    logger.info(f"sum of weights bkg: {sumw_bkg}")

    # multiply the weights by the weight factor
    variables_bkg[-1] = variables_bkg[-1] * args.weights[1]

    sumw_bkg = variables_bkg[-1].sum()
    logger.info(f"sum of weights bkg: {sumw_bkg}")

    zeros_tensor = torch.zeros_like(variables_bkg[0], dtype=torch.float32).unsqueeze(0)

    X_bkg = (variables_bkg, zeros_tensor)

    #######################################################
    X_fts = torch.cat((X_sig[0], X_bkg[0]), dim=1).transpose(1, 0)
    X_lbl = torch.cat((X_sig[1], X_bkg[1]), dim=1).transpose(1, 0)

    # split the dataset into training and val sets
    if args.train_size != -1 and args.val_size != -1 and args.test_size != -1:
        X_fts = X_fts[: args.train_size + args.val_size + args.test_size, :]
        X_lbl = X_lbl[: args.train_size + args.val_size + args.test_size, :]

    X = torch.utils.data.TensorDataset(X_fts, X_lbl)

    train_size = int(0.8 * len(X)) if args.train_size == -1 else args.train_size
    val_size = math.ceil((len(X) - train_size) / 2)
    test_size = math.floor((len(X) - train_size) / 2)

    logger.info(f"Total size: {len(X)}")
    logger.info(f"Training size: {train_size}")
    logger.info(f"Validation size: {val_size}")
    logger.info(f"Test size: {test_size}")

    gen = torch.Generator()
    gen.manual_seed(0)
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        X, [train_size, val_size, test_size], generator=gen
    )

    # check size of the dataset
    print("Training dataset size:", len(train_dataset))
    print("Validation dataset size:", len(val_dataset))
    print("Test dataset size:", len(test_dataset))

    training_loader = None
    val_loader = None
    test_loader = None

    training_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        drop_last=True,
        pin_memory=args.pin_memory,
    )
    logger.info("Training loader size: %d", len(training_loader))

    if not args.eval_model:
        val_loader = torch.utils.data.DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            drop_last=True,
            pin_memory=args.pin_memory,
        )
        logger.info("Validation loader size: %d", len(val_loader))

    if args.eval or args.eval_model:
        test_loader = torch.utils.data.DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            drop_last=True,
            pin_memory=args.pin_memory,
        )
        logger.info("Test loader size: %d", len(test_loader))

    return (
        training_loader,
        val_loader,
        test_loader,
        train_size,
        val_size,
        test_size,
        X_fts,
        X_lbl,
        batch_size,
    )
