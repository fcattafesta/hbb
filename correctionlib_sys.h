#ifndef CORRECTIONLIB_H
#define CORRECTIONLIB_H

#include "correction.h"
#include <cstring>


// Calculate b-tagging scale factors for a given set of inputs
template <typename str, typename VecI, typename Vec>
auto sf_btag(const str & name, const VecI & hadronFlavour, const Vec & eta, const Vec & pt, const Vec & btag) {
    // Create a vector to store the scale factors
    ROOT::VecOps::RVec<float> weights(hadronFlavour.size());

    int flav[3];
    if (strstr(name, "central") != nullptr) {
        flav[0] = 0; flav[1] = 5; flav[2] = 4;
    } else if (strstr(name, "hf") != nullptr || strstr(name, "lf") != nullptr) {
        flav[0] = 0; flav[1] = 5; flav[2] = -1;
    } else {
        flav[0] = 4; flav[1] = -1; flav[2] = -1;
    }

    // Loop over each input and calculate the scale factor
    for(size_t i=0;i<hadronFlavour.size(); i++) {
        bool correct_flav = false;
        // Loop over each flavor and check if it matches the input flavor
        for (long unsigned int j = 0; j < sizeof(flav) / sizeof(flav[0]); j++) {
            if (hadronFlavour[i] == flav[j]) {
                // Calculate the scale factor using the btag_shape_corr object
                weights[i]=btag_shape_corr->evaluate({name, hadronFlavour[i], abs(eta[i]), pt[i], btag[i]});
                correct_flav = true;
                break;
            }
        }
        // If no matching flavor is found, set the scale factor to 1
        if (!correct_flav) {
            weights[i]=1.;
        }
    }
    // Return the vector of scale factors
    return weights;
}

// Calculate jer scale factors for a given set of inputs
template <typename str, typename Vec>
auto sf_jer(const str & name, const Vec & eta) {
    // Create a vector to store the scale factors
    ROOT::VecOps::RVec<float> weights(eta.size());

    // Loop over each input and calculate the scale factor
    for(size_t i=0;i<eta.size(); i++) {
        // Calculate the scale factor using the jer_sf_corr object
        weights[i]=jer_sf_corr->evaluate({eta[i], name});
    }
    // Return the vector of scale factors
    return weights;
}