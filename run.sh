#!/bin/bash

set -x

echo "args: $@"

CMD="python analysis.py"
model="models"

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out/"

# set a comment via `COMMENT`
suffix=$1

$CMD \
    --histfolder ${histodir}${suffix}/ \
    --model ${model} \
    "${@:2}"
