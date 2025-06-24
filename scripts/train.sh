#!/bin/bash
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/python3.10/site-packages/torch/lib:$LD_LIBRARY_PATH"

python train.py \
    -m output/0a5c013435 \
    -s /home/user/Fisheye-GS/data/ScanNet++/data/0b031f3119/dslr \
    --iterations 15000 \
    --save_iterations 10000 \
    --test_iterations 10000 \
    --bs 6 \
    -r 1 \
    --sh_degree 3 \
    --camera_model FISHEYE \
    --train_random_background 