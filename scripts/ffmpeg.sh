#!/bin/bash
# Extract frames from MP4 video using FFmpeg
echo "Extracting frames from MP4 video..."
ffmpeg -i input_video.mp4 -vf fps=30 data/output_frames/frame_%04d.png