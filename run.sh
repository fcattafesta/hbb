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

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out"

$CMD \
    --histfolder ${histodir}/${lep}/${suffix}/ \
    --model ${model} \
    --lep ${lep} \
    "${@:3}"
