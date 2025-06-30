import os
import numpy as np
import cv2
from tqdm import tqdm
from pathlib import Path

class Undistorter:
    def undistort_images(self, cam_id, src_dir, dst_dir):
        model, width, height, params = self.cams[cam_id]
        fx = params[0]
        fy = params[1]
        cx = params[2]
        cy = params[3]
        distortion_params = params[4:]
        kk = distortion_params

        # Prepare undistortion maps
        mapx = np.zeros((width, height), dtype=np.float32)
        mapy = np.zeros((width, height), dtype=np.float32)
        for i in tqdm(range(0, width), desc=f"calc_maps_{src_dir.name}"):
            for j in range(0, height):
                x = float(i)
                y = float(j)
                x1 = (x - cx) / fx
                y1 = (y - cy) / fy
                theta = np.sqrt(x1**2 + y1**2)
                r = (1.0 + kk[0] * theta**2 + kk[1] * theta**4 + kk[2] * theta**6 + kk[3] * theta**8)
                x2 = fx * x1 * r + width // 2
                y2 = fy * y1 * r + height // 2
                mapx[i, j] = x2
                mapy[i, j] = y2

        frames = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.png'))])
        dst_dir = Path(dst_dir)
        dst_dir.mkdir(parents=True, exist_ok=True)
        for frame in tqdm(frames, desc=f"undistort_{src_dir.name}"):
            image_path = Path(src_dir) / frame
            image = cv2.imread(str(image_path))
            if image is None:
                continue
            undistorted_image = cv2.remap(
                image,
                mapx.T,
                mapy.T,
                interpolation=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REFLECT_101,
            )
            out_image_path = dst_dir / frame
            cv2.imwrite(str(out_image_path), undistorted_image)