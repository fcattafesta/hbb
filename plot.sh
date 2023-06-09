#!/bin/bash

set -x

echo "args: $@"

CMD="python plot.py"

lep=$1
suffix=$2

if [ "$lep" == "mu" ]; then
    model="modelsMuon"
elif [ "$lep" == "el" ]; then
    model="modelsElectron"
fi

fs=""
if [[ $flavsplit == true ]]; then
    model="${model}FlavSplit"
    fs="_flavsplit"
fi

btag=""
if [[ $suffix == *deepcsv* ]]; then
    btag="--btag deepcsv"
elif [[ $suffix == *deepflav* ]]; then
    btag="--btag deepflav"
fi


histodir="/gpfs/ddn/cms/user/malucchi/hbb_out"
plotdir="/gpfs/ddn/cms/user/malucchi/hbb_plots"

$CMD \
    --model ${model} \
    --histfolder ${histodir}/${lep}/${suffix}/ \
    --outfolder ${plotdir}/${lep}/${suffix}${fs}/ \
    --blind \
    ${btag} \
    "${@:3}"
