#!/bin/bash
set -e

export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/python3.10/site-packages/torch/lib:$LD_LIBRARY_PATH"

DATASET=/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10
LEFTIMAGES=$DATASET/images/left
RIGHTIMAGES=$DATASET/images/right
SPARSE=$DATASET/sparse
COLMAP_INTRINSICS=$DATASET/colmap/cameras.txt

LEFT_PARAMS="1190.4990185909498,1190.344769418459,1545.2154064008814,1983.9367884159963,-0.011234801674675991,0.0017341540312918334,-0.003972944462135868,0.0006499045739833588"
RIGHT_PARAMS="1194.768718613003,1194.8852276046334,1549.7229681677704,2026.345441202774,-0.010445840343537294,-0.0016941509960656255,-0.0013831771880681383,4.5532568167260544e-05"

rm -f "$DATASET/database.db"

echo "Step 2a: COLMAP feature extraction for LEFT camera..."
colmap feature_extractor \
    --database_path "$DATASET/database.db" \
    --image_path "$LEFTIMAGES" \
    --ImageReader.single_camera 1 \
    --ImageReader.camera_model OPENCV_FISHEYE \
    --ImageReader.camera_params "$LEFT_PARAMS"

echo "Step 2b: COLMAP feature extraction for RIGHT camera..."
colmap feature_extractor \
    --database_path "$DATASET/database.db" \
    --image_path "$RIGHTIMAGES" \
    --ImageReader.single_camera 1 \
    --ImageReader.camera_model OPENCV_FISHEYE \
    --ImageReader.camera_params "$RIGHT_PARAMS"

colmap exhaustive_matcher \
    --database_path "$DATASET/database.db"

mkdir -p "$SPARSE"
colmap mapper \
    --database_path "$DATASET/database.db" \
    --image_path "$DATASET/images" \
    --output_path "$SPARSE"

colmap model_converter \
    --input_path "$SPARSE/0" \
    --output_path "$SPARSE/0" \
    --output_type TXT