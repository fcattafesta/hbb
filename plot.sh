#!/bin/bash

set -x

echo "args: $@"

CMD="python plot.py"
model="models"

histodir="/scratchnvme/malucchi/hbb_out/"
plotdir="/scratchnvme/malucchi/hbb_plots/"

# set a comment via `COMMENT`
suffix=$1

$CMD \
    ${model} \
    --histfolder ${histodir}${suffix}/ \
    --outfolder ${plotdir}${suffix}/ \
    "${@:2}"
