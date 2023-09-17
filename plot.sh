#!/bin/bash

set -x

echo "args: $@"

CMD="python plot.py"

lep=$1
suffix=$2

if [ "$lep" == "mu" ]; then
    model="modelsMuon"
    region="mm"
elif [ "$lep" == "el" ]; then
    model="modelsElectron"
    region="ee"
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
if [[ $suffix == *_sf* || $suffix == *_sys* ]]; then
    sf="--sf"
fi

bit=""
if [[ $suffix == *_bit* ]]; then
    bit="--bit"
fi

if [[ $suffix == *_fit*  ||  $fit == true  || "${@:3}" == *" -v "* ]]; then
    model="${model}Fit"
fi

fit_vars=""
if [[ $fit == true ]]; then
    fit_vars="-v atanhDNN_Score___SR_${region} jj_dr___CR_Z${region}_bjets jj_dr___CR_Z${region}_lightjets jj_dr___CR_${region}_ttbar"
fi

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out/${lep}/${suffix}/"
plotdir="/gpfs/ddn/cms/user/malucchi/hbb_plots/${lep}/${suffix}${fs}/"

$CMD \
    --model ${model} \
    --histfolder ${histodir} \
    --outfolder ${plotdir} \
    --workspace ${plotdir}/ \
    ${btag} \
    ${sf} \
    ${bit} \
    ${fit_vars} \
    "${@:3}"
