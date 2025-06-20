#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fgs310

python render.py \
    -m output/0b031f3119 \
    -s /home/user/Fisheye-GS/data/ScanNet++/data/0b031f3119/dslr \
    --iteration 30000 \
    --camera_model FISHEYE \
    -r 1