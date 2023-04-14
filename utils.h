#ifndef UTILS_H
#define UTILS_H

auto InvMass(ROOT::VecOps::RVec<float> pt, ROOT::VecOps::RVec<float> eta,
             ROOT::VecOps::RVec<float> phi, ROOT::VecOps::RVec<float> mass) {
  TLorentzVector v1, v2;
  v1.SetPtEtaPhiM(pt[0], eta[0], phi[0], mass[0]);
  v2.SetPtEtaPhiM(pt[1], eta[1], phi[1], mass[1]);
  return (v1 + v2).M();
}

#endif