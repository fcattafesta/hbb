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

sf=""
if [[ $suffix == *_sf* ]]; then
    sf="--sf"
fi

snap="--snapshot"
if [[ $suffix == *_NOsnap* ]]; then
    snap=""
fi

eval=""
if [[ $suffix == *_eval* ]]; then
    eval="--eval model_"${btag}".onnx"
fi

btag="--btag "${btag}

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out"
totaldir="${histodir}/${lep}/${suffix}/"

$CMD \
    --model ${model} \
    --histfolder ${totaldir}/ \
    --lep ${lep} \
    --workspace ${totaldir}/workspace/ \
    ${eval} \
    ${snap} \
    ${btag} \
    ${sf} \
    "${@:3}"
