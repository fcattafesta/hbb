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

fs=""
if [[ "$suffix" == *"flavsplit"* ]]; then
    model="${model}FlavSplit"
    fs="--flav-split"
fi

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out"

$CMD \
    --histfolder ${histodir}/${lep}/${suffix}/ \
    --model ${model} \
    --lep ${lep} \
    --snapshot \
    ${fs} \
    "${@:3}"
