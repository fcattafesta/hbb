#ifndef TEST_H
#define TEST_H

#include <TMVA/SOFIEHelpers.hxx>
#include "model_DNN.hxx"

auto sofie_functor = TMVA::Experimental::SofieFunctor<17, TMVA_SOFIE_model_DNN::Session>(0);

#endif
