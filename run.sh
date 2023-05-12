#!/bin/bash

set -x

echo "args: $@"

CMD="python analysis.py"

if [ "$1" == "mu" ]; then
    model="modelsMuon"
elif [ "$1" == "el" ]; then
    model="modelsElectron"


histodir="/gpfs/ddn/cms/user/malucchi/hbb_out"

# set a comment via `COMMENT`
suffix=$2

$CMD \
    --histfolder ${histodir}/${suffix}/ \
    --model ${model} \
    "${@:2}"
