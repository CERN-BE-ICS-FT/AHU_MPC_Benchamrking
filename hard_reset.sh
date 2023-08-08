#!/bin/bash

# Directories
OUT_DIR="out"
ERR_DIR="err"
RESULT_DIR="results"

# Remove .out files if out directory exists
if [[ -d "$OUT_DIR" ]]; then
    rm -f "${OUT_DIR}"/*.out
    echo "All .out files in ${OUT_DIR} have been deleted."
else
    echo "Directory ${OUT_DIR} does not exist."
fi

# Remove .err files if err directory exists
if [[ -d "$ERR_DIR" ]]; then
    rm -f "${ERR_DIR}"/*.err
    echo "All .err files in ${ERR_DIR} have been deleted."
else
    echo "Directory ${ERR_DIR} does not exist."
fi

# Remove .csv files if results directory exists
if [[ -d "$RESULT_DIR" ]]; then
    rm -f "${RESULT_DIR}"/*.csv
    echo "All .csv files in ${RESULT_DIR} have been deleted."
else
    echo "Directory ${RESULT_DIR} does not exist."
fi

