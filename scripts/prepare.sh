#!/bin/bash
# Run the preprocessing script
echo "Running preprocessing..."
python preparesnpp.py \
    --path /home/user/Fisheye-GS/data/ScanNet++/data/4ba22fa7e4/dslr \
    --src resized_images \
    --dst image_undistorted_fisheye