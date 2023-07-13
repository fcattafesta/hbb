#ifndef TEST_H
#define TEST_H

#include <TMVA/SOFIEHelpers.hxx>
#include "model_102.hxx"

auto sofie_functor = TMVA::Experimental::SofieFunctor<17, TMVA_SOFIE_model_102::Session>(0);

#endif
