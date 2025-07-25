#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fgs310

python render.py \
    -m output/2025-06-18_16-57-10 \
    -s /home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10 \
    --iteration 30000 \
    --camera_model FISHEYE \
    -r 1