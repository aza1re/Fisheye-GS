import os
from pathlib import Path
import numpy as np
import cv2
from scene.reader import MetaCamEduReader
import open3d as o3d
import csv
from tqdm import tqdm
import traceback
from scene.undistort import Undistorter
from scene.mask import BorderMasker
from scene.cameratxt import CameraTxtWriter
from scene.crop import FisheyeRectCropper

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

src_root = Path("/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10")
dst_scene = src_root
left_dst = dst_scene / "images" / "left"
right_dst = dst_scene / "images" / "right"
imu_dst = dst_scene / "imu"
lidar_dst = dst_scene / "lidar"
left_dst.mkdir(parents=True, exist_ok=True)
right_dst.mkdir(parents=True, exist_ok=True)
imu_dst.mkdir(parents=True, exist_ok=True)
lidar_dst.mkdir(parents=True, exist_ok=True)

cropped_left_dst = dst_scene / "cropped" / "left"
cropped_right_dst = dst_scene / "cropped" / "right"
cropped_left_dst.mkdir(parents=True, exist_ok=True)
cropped_right_dst.mkdir(parents=True, exist_ok=True)

cropper = FisheyeRectCropper(output_size=(760, 760))  # <-- Add this line

try:
    with MetaCamEduReader(src_root) as reader:
        # Count total messages for tqdm
        total_msgs = sum(1 for _ in reader.synced_msgs())
    # Re-open the reader for actual extraction
    with MetaCamEduReader(src_root) as reader:
        imu_file = open(imu_dst / "imu.csv", "w", newline="")
        imu_writer = csv.writer(imu_file)
        imu_writer.writerow(["timestamp", "ax", "ay", "az", "gx", "gy", "gz"])
        for idx, (timestamp, synced) in enumerate(tqdm(reader.synced_msgs(), total=total_msgs, desc="Extracting")):
            # Left camera
            if synced.camera_left is not None:
                img_bytes = synced.camera_left.data
                img_array = np.frombuffer(img_bytes, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if img is not None:
                    out_path = left_dst / f"left_{idx:06d}.jpg"
                    cv2.imwrite(str(out_path), img)  # Save original size
                    cropped_img = cropper.crop_center_rect(img)
                    cropped_out_path = cropped_left_dst / f"left_{idx:06d}.jpg"
                    cv2.imwrite(str(cropped_out_path), cropped_img)
            # Right camera
            if synced.camera_right is not None:
                img_bytes = synced.camera_right.data
                img_array = np.frombuffer(img_bytes, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                if img is not None:
                    out_path = right_dst / f"right_{idx:06d}.jpg"
                    cv2.imwrite(str(out_path), img)  # Save original size
                    cropped_img = cropper.crop_center_rect(img)
                    cropped_out_path = cropped_right_dst / f"right_{idx:06d}.jpg"
                    cv2.imwrite(str(cropped_out_path), cropped_img)
            # IMU
            if hasattr(synced, "imu") and synced.imu is not None:
                imu = synced.imu
                imu_writer.writerow([
                    timestamp,
                    imu.linear_acceleration.x,
                    imu.linear_acceleration.y,
                    imu.linear_acceleration.z,
                    imu.angular_velocity.x,
                    imu.angular_velocity.y,
                    imu.angular_velocity.z,
                ])
            # Lidar
            if hasattr(synced, "lidar") and synced.lidar is not None:
                try:
                    pcd = synced.pcd()
                    if pcd is not None and len(pcd.points) > 0:
                        o3d.io.write_point_cloud(str(lidar_dst / f"lidar_{idx:06d}.pcd"), pcd)
                except Exception as e:
                    print(f"Failed to save lidar at idx {idx}: {e}")
        imu_file.close()
except Exception as e:
    print(f"Failed to extract from {src_root}: {e}")
    traceback.print_exc()

print("Extraction and reformatting complete.")

calib_path = "/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10/info/calibration.json"
out_path = "/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10/colmap/cameras.txt"

downscale = 4  # 3040/760 or 4032/1008

cameratxtwriter = CameraTxtWriter(calib_path, out_path, downscale=downscale)
cameratxtwriter.write_cameras_txt()

# Undistort images
undistorter = Undistorter(out_path)
undistorter.undistort_images(
    1,
    src_root / "images" / "left",
    src_root / "undistorted" / "left"
)
undistorter.undistort_images(
    2,
    src_root / "images" / "right",
    src_root / "undistorted" / "right"
)