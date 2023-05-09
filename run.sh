#!/bin/bash

set -x

echo "args: $@"

CMD="python analysis.py"
model="models"

histodir="/scratchnvme/malucchi/hbb_out/"

# set a comment via `COMMENT`
suffix=$1

$CMD \
    --histfolder ${histodir}${suffix}/ \
    --model ${model} \
    "${@:2}"