#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate fgs310

python render.py \
    -m output/4ba22fa7e4 \
    -s /home/user/Fisheye-GS/data/ScanNet++/data/4ba22fa7e4/dslr \
    --iteration 30000 \
    --camera_model FISHEYE \
    -r 1