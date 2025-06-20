#!/bin/bash
# Run the preprocessing script
echo "Running preprocessing..."
python preparesnpp.py \
    --path /home/user/Fisheye-GS/data/ScanNet++/data/0b031f3119/dslr \
    --src resized_undistorted_images \
    --dst image_undistorted_fisheye