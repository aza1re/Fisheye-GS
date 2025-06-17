# Run the preprocessing script
Write-Host "Running preprocessing..."
python prepare_scannetpp.py `
    --path output_frames `
    --src images `
    --dst image_undistorted_fisheye