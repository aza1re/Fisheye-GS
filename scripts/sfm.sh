#!/bin/bash
set -e

export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/python3.10/site-packages/torch/lib:$LD_LIBRARY_PATH"

DATASET=/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10
ALLIMAGES=$DATASET/cropped/all
SPARSE=$DATASET/sparse

LEFT_PARAMS="297.62475464773746,297.58619235461475,386.30385160022036,495.98419710399907,-0.011234801674675991,0.0017341540312918334,-0.003972944462135868,0.0006499045739833588"
RIGHT_PARAMS="298.6921796532508,298.72130690115836,387.4307420419426,506.5863603006935,-0.010445840343537294,-0.0016941509960656255,-0.0013831771880681383,4.5532568167260544e-05"

rm -f "$DATASET/database.db"

echo "Step 2: COLMAP feature extraction for all images..."
colmap feature_extractor \
    --database_path "$DATASET/database.db" \
    --image_path "$DATASET/cropped/left" \
    --ImageReader.camera_model OPENCV_FISHEYE \
    --ImageReader.single_camera 0

colmap feature_extractor \
    --database_path "$DATASET/database.db" \
    --image_path "$DATASET/cropped/right" \
    --ImageReader.camera_model OPENCV_FISHEYE \
    --ImageReader.single_camera 0

mkdir -p "$ALLIMAGES"
cp $DATASET/cropped/left/* $ALLIMAGES/
cp $DATASET/cropped/right/* $ALLIMAGES/

colmap exhaustive_matcher \
    --database_path "$DATASET/database.db"

mkdir -p "$SPARSE"
colmap mapper \
    --database_path "$DATASET/database.db" \
    --image_path "$ALLIMAGES" \
    --output_path "$SPARSE"

colmap model_converter \
    --input_path "$SPARSE/0" \
    --output_path "$SPARSE/0" \
    --output_type TXT