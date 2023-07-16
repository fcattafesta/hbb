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

sf=""
if [[ $suffix == *_sf* ]]; then
    sf="--sf"
fi


histodir="/gpfs/ddn/cms/user/malucchi/hbb_out/"${lep}"/"${suffix}"/"
plotdir="/gpfs/ddn/cms/user/malucchi/hbb_plots/"${lep}"/"${suffix}${fs}"/"

$CMD \
    --model ${model} \
    --histfolder ${histodir} \
    --outfolder ${plotdir} \
    --workspace ${plotdir}/ \
    --blind \
    ${btag} \
    ${sf} \
    "${@:3}"
