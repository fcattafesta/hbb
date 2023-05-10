#!/bin/bash

set -x

echo "args: $@"

CMD="python plot.py"
model="models"

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out/"
plotdir="/gpfs/ddn/cms/user/malucchi/hbb_plots/"

# set a comment via `COMMENT`
suffix=$1

$CMD \
    ${model} \
    --histfolder ${histodir}${suffix}/ \
    --outfolder ${plotdir}${suffix}/ \
    "${@:2}"
