import os
import numpy as np
import cv2
from tqdm import tqdm
from pathlib import Path

class Undistorter:
    def __init__(self, cameras_txt):
        self.cams = self.read_intrinsics_text(cameras_txt)

    def read_intrinsics_text(self, path):
        cams = {}
        with open(path, "r") as fid:
            for line in fid:
                line = line.strip()
                if len(line) > 0 and line[0] != "#":
                    elems = line.split()
                    camera_id = int(elems[0])
                    model = elems[1]
                    width = int(elems[2])
                    height = int(elems[3])
                    params = np.array(tuple(map(float, elems[4:])))
                    cams[camera_id] = (model, width, height, params)
        return cams

    def undistort_images(self, cam_id, src_dir, dst_dir, exclude_k1=False):
        model, width, height, params = self.cams[cam_id]
        fx = params[0]
        fy = params[1]
        cx = params[2]
        cy = params[3]
        distortion_params = params[4:]
        kk = distortion_params.copy()
        if exclude_k1 and len(kk) > 0:
            kk[0] = 0.0  # Exclude k1

        # Prepare undistortion maps (height, width)
        mapx = np.zeros((height, width), dtype=np.float32)
        mapy = np.zeros((height, width), dtype=np.float32)
        for j in tqdm(range(height), desc=f"calc_maps_{Path(src_dir).name}"):
            for i in range(width):
                x = float(i)
                y = float(j)
                x1 = (x - cx) / fx
                y1 = (y - cy) / fy
                theta = np.sqrt(x1**2 + y1**2)
                # Only use as many coefficients as available
                r = 1.0
                for idx, k in enumerate(kk):
                    r += k * theta ** (2 * (idx + 1))
                x2 = fx * x1 * r + cx
                y2 = fy * y1 * r + cy
                mapx[j, i] = x2
                mapy[j, i] = y2

        frames = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.png'))])
        dst_dir = Path(dst_dir)
        dst_dir.mkdir(parents=True, exist_ok=True)
        for frame in tqdm(frames, desc=f"undistort_{Path(src_dir).name}"):
            image_path = Path(src_dir) / frame
            image = cv2.imread(str(image_path))
            if image is None:
                continue
            undistorted_image = cv2.remap(
                image,
                mapx,
                mapy,
                interpolation=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REFLECT_101,
            )
            out_image_path = dst_dir / frame
            cv2.imwrite(str(out_image_path), undistorted_image)