#!/bin/bash

set -x

echo "args: $@"

CMD="python plot.py"

if [ "$1" == "mu" ]; then
    model="modelsMuon"
elif [ "$1" == "el" ]; then
    model="modelsElectron"

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out"
plotdir="/gpfs/ddn/cms/user/malucchi/hbb_plots"

# set a comment via `COMMENT`
suffix=$2

$CMD \
    ${model} \
    --histfolder ${histodir}/${suffix}/ \
    --outfolder ${plotdir}/${suffix}/ \
    "${@:2}"
