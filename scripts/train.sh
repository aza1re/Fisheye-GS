#!/bin/bash
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/python3.10/site-packages/torch/lib:$LD_LIBRARY_PATH"

python train.py \
    -m output/4ba22fa7e4 \
    -s /home/user/Fisheye-GS/data/ScanNet++/data/4ba22fa7e4/dslr \
    --iterations 30000 \
    --save_iterations 10000 20000 30000\
    --test_iterations 10000 20000 30000 \
    --bs 3 \
    -r 1 \
    --sh_degree 3 \
    --camera_model FISHEYE \
    --train_random_background 