#!/bin/bash

set -x

echo "args: $@"

CMD="python analysis.py"

lep=$1
suffix=$2

if [[ "$lep" == "mu" ]]; then
    model="modelsMuon"
elif [[ "$lep" == "el" ]]; then
    model="modelsElectron"
fi

if [[ $flavsplit == true ]]; then
    model="${model}FlavSplit"
fi

btag=""
if [[ $suffix == *deepcsv* ]]; then
    btag="deepcsv"
elif [[ $suffix == *deepflav* ]]; then
    btag="deepflav"
fi

sys=""
if [[ $suffix == *_sys* ]]; then
    sys="--sys"
fi

sf_only=""
if [[ $suffix == *_sf* ]]; then
    sf_only="--sf-only"
fi

snap="--snapshot"
if [[ $suffix == *_NOsnap* ]]; then
    snap=""
fi

eval=""
if [[ $suffix == *_eval* ]]; then
    eval="--eval model_"${btag}".onnx"
fi

fit=""
if [[ $suffix == *_fit* ]]; then
    fit="--fit"
fi

bit=""
if [[ $suffix == *_bit* ]]; then
    bit="--btag-bit"
    eval="--eval model_${btag}_bit.onnx"
fi

train=""
if [[ $suffix == *_train* ]]; then
    train="--train"
fi

btag="--btag ${btag}"

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out/${lep}/${suffix}/"

$CMD \
    --model ${model} \
    --histfolder ${histodir}/ \
    --lep ${lep} \
    ${eval} \
    ${snap} \
    ${btag} \
    ${sys} \
    ${sf_only} \
    ${fit} \
    ${bit} \
    ${train} \
    "${@:3}"
