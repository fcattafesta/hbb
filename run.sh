#!/bin/bash

set -x

echo "args: $@"

CMD="python analysis.py"

if [ "$1" == "mu" ]; then
    model="modelsMuon"
elif [ "$1" == "el" ]; then
    model="modelsElectron"
echo $model

histodir="/gpfs/ddn/cms/user/malucchi/hbb_out"
lep=$1
echo $lep
# set a comment via `COMMENT`
suffix=$2
echo $suffix

$CMD \
    --histfolder ${histodir}/${lep}/${suffix}/ \
    --model ${model} \
    --lep ${lep} \
    "${@:3}"