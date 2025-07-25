import cv2
import numpy as np
from pathlib import Path

class FisheyeRectCropper:
    def __init__(self, output_size=None):
        """
        output_size: (width, height) tuple for resizing the output (optional).
        If None, keeps the cropped size.
        """
        self.output_size = output_size

    def crop_center_rect(self, img):
        h, w = img.shape[:2]
        # Crop 90% of the largest centered square
        side = int(min(h, w) * 0.85)
        x1 = (w - side) // 2
        y1 = (h - side) // 2
        x2 = x1 + side
        y2 = y1 + side
        cropped = img[y1:y2, x1:x2]
        if self.output_size:
            cropped = cv2.resize(cropped, self.output_size, interpolation=cv2.INTER_AREA)
        return cropped

    def crop_folder(self, src_folder, dst_folder, ext="jpg"):
        src_folder = Path(src_folder)
        dst_folder = Path(dst_folder)
        dst_folder.mkdir(parents=True, exist_ok=True)
        for img_path in src_folder.glob(f"*.{ext}"):
            img = cv2.imread(str(img_path))
            if img is not None:
                cropped = self.crop_center_rect(img)
                out_path = dst_folder / img_path.name
                cv2.imwrite(str(out_path), cropped)
