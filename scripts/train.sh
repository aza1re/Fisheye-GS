#!/bin/bash
python train.py \
    -m output/0b031f3119 \
    -s /home/user/Fisheye-GS/data/ScanNet++/data/0b031f3119/dslr \
    --iterations 30000 \
    --save_iterations 10000 20000 30000 \
    --test_iterations 10000 20000 30000 \
    --bs 3 \
    -r 1 \
    --sh_degree 3 \
    --camera_model FISHEYE \
    --train_random_background