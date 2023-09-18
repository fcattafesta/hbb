import ROOT
import awkward as ak
import numpy as np
import mplhep as hep

rdf = ROOT.RDataFrame("btag", "btag.root")

awk = ak.from_rdataframe(
    rdf,
    columns=[
        "MatchedJet_btagDeepFlavB",
        "MatchedGenJet_hadronFlavour",
        "MatchedJet_FullSim_btagDeepFlavB",
        "MatchedGenJet_FullSim_hadronFlavour",
        "FullSim_Jet_btagDeepFlavB",
        "FullSim_Jet_hadronFlavour",
    ],
)

flash_truth = np.array(ak.flatten(awk["MatchedGenJet_hadronFlavour"]))
flash_score = np.array(ak.flatten(awk["MatchedJet_btagDeepFlavB"]))

flash_b_vs_udsg_mask = flash_truth != 4
flash_truth = flash_truth[flash_b_vs_udsg_mask]
flash_truth = np.where(flash_truth == 5, 1, 0)
flash_score = flash_score[flash_b_vs_udsg_mask]

full_truth = np.array(ak.flatten(awk["MatchedGenJet_FullSim_hadronFlavour"]))
full_score = np.array(ak.flatten(awk["MatchedJet_FullSim_btagDeepFlavB"]))
full_b_vs_udsg_mask = full_truth != 4

full_truth = full_truth[full_b_vs_udsg_mask]
full_truth = np.where(full_truth == 5, 1, 0)
full_score = full_score[full_b_vs_udsg_mask]

original_full_truth = np.array(ak.flatten(awk["FullSim_Jet_hadronFlavour"]))
original_full_score = np.array(ak.flatten(awk["FullSim_Jet_btagDeepFlavB"]))
original_full_b_vs_udsg_mask = original_full_truth != 4

original_full_truth = original_full_truth[original_full_b_vs_udsg_mask]
original_full_truth = np.where(original_full_truth == 5, 1, 0)
original_full_score = original_full_score[original_full_b_vs_udsg_mask]


from sklearn.metrics import roc_curve, auc

flash_fpr, flash_tpr, flash_thresholds = roc_curve(
    flash_truth, flash_score, pos_label=1
)
flash_roc_auc = auc(flash_fpr, flash_tpr)

full_fpr, full_tpr, full_thresholds = roc_curve(full_truth, full_score, pos_label=1)
full_roc_auc = auc(full_fpr, full_tpr)

original_full_fpr, original_full_tpr, original_full_thresholds = roc_curve(
    original_full_truth, original_full_score, pos_label=1
)

import matplotlib.pyplot as plt

plt.style.use(hep.style.CMS)
plt.figure()
plt.plot(
    flash_tpr,
    flash_fpr,
    color="orange",
    lw=2,
    label="FlashSim (area = %0.2f)" % flash_roc_auc,
)
plt.plot(
    full_tpr,
    full_fpr,
    color="black",
    lw=2,
    ls="--",
    label="FullSim (area = %0.2f)" % full_roc_auc,
)
plt.plot(
    original_full_tpr,
    original_full_fpr,
    color="blue",
    lw=2,
    ls=":",
    label="FullSim (original) (area = %0.2f)" % full_roc_auc,
)
# plt.plot([1, 1], [0, 0], color="navy", lw=2, linestyle="--")
plt.xlim([0.4, 1.0])
plt.xlabel("b-jet efficiency")
plt.ylabel("Misidentification probability")
plt.yscale("log")
plt.grid(which="both")
plt.ylim([1e-4, 1.2])
# plt.title("ROC curve")
plt.legend(loc="upper left")
plt.savefig("roc.png")
