from PIL import Image
import sys

if len(sys.argv) != 2:
    print("Usage: python get_image_resolution.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
with Image.open(image_path) as img:
    width, height = img.size
    print(f"Resolution: {width} x {height}")