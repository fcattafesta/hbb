import uproot
import argparse
import numpy as np

from DNN_input_lists import signal_list, background_list


def load_data(dirs):
    # list of signal files
    sig_files = []
    for x in dirs:
        sig_files += [x + y + "_Snapshot.root" for y in signal_list]

    # open each file and get the Events tree using uproot
    # the array of variables is stored in a numpy array
    # concatenate all the variables into a single numpy array
    for i, file in enumerate(sig_files):
        sig_file = uproot.open(f"{file}:Events")
        score_sig =  sig_file["DNN_score"].array(library="np")

        if i == 0:
            scores_sig = score_sig
        else:
            scores_sig = np.concatenate((scores_sig, score_sig))

    # do the same for the background
    bkg_files = []
    for x in dirs:
        bkg_files += [x + y + "_Snapshot.root" for y in background_list]

    for i, file in enumerate(bkg_files):
        bkg_file = uproot.open(f"{file}:Events")
        score_bkg = bkg_file["DNN_score"].array(library="np")

        if i == 0:
            scores_bkg = score_bkg
        else:
            scores_bkg = np.concatenate((scores_bkg, score_bkg))

    return scores_sig, scores_bkg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--data-dirs",
        nargs="+",
        default=[
            "~/el/Snapshots/",
            "~/mu/Snapshots/",
        ],
        help="Directory for data",
    )

    args = parser.parse_args()

    scores_sig, scores_bkg = load_data(args.data_dirs)
