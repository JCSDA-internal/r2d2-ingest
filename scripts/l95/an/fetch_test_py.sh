#!/bin/bash

R2D2_PATH=/Users/eric/JCSDA_PROJECTS/R2D2/r2d2/src/r2d2/bin/r2d2
PYTHON_FILE=fetch.py

date +"%Y-%m-%d_%H-%M-%S"

eval ${R2D2_PATH} ${PYTHON_FILE}

date +"%Y-%m-%d_%H-%M-%S"