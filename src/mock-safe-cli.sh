#!/bin/bash


[ -f data/.mockerr ] && { exit 1; }

[ -f data/.mockover ] && {
    SEC=$(date "+%s")
    cat data/safe-cli-output.txt | sed -e "s/938422/$SEC/g"
    exit 0
}

{ cat data/safe-cli-output.txt; exit 0; }

