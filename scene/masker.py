import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm

class BorderMasker:
    def __init__(self, mask_ratio=0.95):
        """
        mask_ratio: Ratio of mask radius to image (0.0-1.0, default 0.95)
        """
        self.mask_ratio = mask_ratio

    def apply_circular_mask(self, image):
        h, w = image.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        center = (w // 2, h // 2)
        radius = int(self.mask_ratio * min(center))
        cv2.circle(mask, center, radius, 255, -1)
        if image.shape[2] == 3:
            masked = cv2.bitwise_and(image, image, mask=mask)
        else:
            # For images with alpha channel
            for c in range(image.shape[2]):
                image[..., c] = cv2.bitwise_and(image[..., c], mask)
            masked = image
        return masked

    def process_folder(self, src_dir, dst_dir):
        src_dir = Path(src_dir)
        dst_dir = Path(dst_dir)
        dst_dir.mkdir(parents=True, exist_ok=True)
        images = sorted(list(src_dir.glob("*.jpg")) + list(src_dir.glob("*.png")))
        for img_path in tqdm(images, desc=f"Masking {src_dir.name}"):
            img = cv2.imread(str(img_path))
            if img is None:
                continue
            masked = self.apply_circular_mask(img)
            out_path = dst_dir / img_path.name
            cv2.imwrite(str(out_path), masked)