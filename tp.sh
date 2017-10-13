#!/bin/bash

OPTIONS=""
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -a|--algo)
    ALGO="$2"
    shift
    ;;
    -e|--ex_path)
    EX_PATH1="$2"
    EX_PATH2="$3"
    shift 2
    ;;
    -p|--print|-t|--time)
    OPTIONS="${OPTIONS}${1} "
    ;;
    *)
        echo "Argument inconnu2: ${1}"
        exit
    ;;
esac
shift
done

#EX_PATH="${EX_PATH1} ${EX_PATH2}"
python3 ./source/teststrassen.py $ALGO $EX_PATH1 $EX_PATH2 $OPTIONS
