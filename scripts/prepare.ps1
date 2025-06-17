# Extract frames from MP4 video using FFmpeg
Write-Host "Extracting frames from MP4 video..."
ffmpeg -i input_video.mp4 -vf fps=30 output_frames/frame_%04d.png

# Run the preprocessing script
Write-Host "Running preprocessing..."
python prepare_scannetpp.py `
    --path /nas/shared/pjlab_lingjun_landmarks/liaozimu/data/scannet/0a5c013435/dslr `
    --src images `
    --dst image_undistorted_fisheye