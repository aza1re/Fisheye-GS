import os
import numpy as np
import cv2
from tqdm import tqdm
from pathlib import Path
from argparse import ArgumentParser
import json


def read_intrinsics_json(json_path, camera_name="left"):
    with open(json_path, "r") as f:
        calib = json.load(f)
    for cam in calib["cameras"]:
        if cam["name"] == camera_name:
            width = cam["width"]
            height = cam["height"]
            fx = cam["intrinsic"]["fl_x"]
            fy = cam["intrinsic"]["fl_y"]
            cx = cam["intrinsic"]["cx"]
            cy = cam["intrinsic"]["cy"]
            kk = [
                cam["distortion"]["params"]["k1"],
                cam["distortion"]["params"]["k2"],
                cam["distortion"]["params"]["k3"],
                cam["distortion"]["params"]["k4"],
            ]
            return width, height, fx, fy, cx, cy, kk
    raise ValueError(f"Camera '{camera_name}' not found in calibration file.")


def colmap_main(args):
    root_dir = args.path
    json_path = Path(root_dir) / args.calib_json
    input_image_dir = Path(root_dir) / args.src
    out_image_dir = Path(root_dir) / args.dst

    width, height, fx, fy, cx, cy, kk = read_intrinsics_json(json_path, args.camera_name)
    print(f"Camera: {args.camera_name}, fx={fx}, fy={fy}, cx={cx}, cy={cy}, distortion={kk}")

    mapx = np.zeros((height, width), dtype=np.float32)
    mapy = np.zeros((height, width), dtype=np.float32)

    for i in tqdm(range(height), desc="calculate_maps"):
        for j in range(width):
            x = float(j)
            y = float(i)
            x1 = (x - cx) / fx
            y1 = (y - cy) / fy
            theta = np.sqrt(x1**2 + y1**2)
            r = (1.0 + kk[0] * theta**2 + kk[1] * theta**4 + kk[2] * theta**6 + kk[3] * theta**8)
            x2 = fx * x1 * r + cx
            y2 = fy * y1 * r + cy
            mapx[i, j] = x2
            mapy[i, j] = y2

    frames = os.listdir(input_image_dir)

    for frame in tqdm(frames, desc="frame"):
        image_path = Path(input_image_dir) / frame
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"Warning: Could not read {image_path}")
            continue
        undistorted_image = cv2.remap(
            image,
            mapx,
            mapy,
            interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT_101,
        )
        out_image_path = Path(out_image_dir) / frame
        out_image_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out_image_path), undistorted_image)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--path', type=str, default="data")
    parser.add_argument('--src', type=str, default="camera")
    parser.add_argument('--dst', type=str, default="processed")
    parser.add_argument('--calib_json', type=str, default="calibration.json")
    parser.add_argument('--camera_name', type=str, default="left")
    args = parser.parse_args()
    colmap_main(args)

