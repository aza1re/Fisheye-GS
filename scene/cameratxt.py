import json
from pathlib import Path

class CameraTxtWriter:
    def __init__(self, calib_path, out_path):
        self.calib_path = Path(calib_path)
        self.out_path = Path(out_path)
        self.calib = None

    def load_calibration(self):
        with open(self.calib_path) as f:
            self.calib = json.load(f)

    def write_cameras_txt(self):
        if self.calib is None:
            self.load_calibration()
        lines = [
            "# Camera list with one line of data per camera:",
            "#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]",
            f"# Number of cameras: {len(self.calib['cameras'])}"
        ]
        for idx, cam in enumerate(self.calib["cameras"], 1):
            model = cam["distortion"]["camera_model"]
            width = cam["width"]
            height = cam["height"]
            fx = cam["intrinsic"]["fl_x"]
            fy = cam["intrinsic"]["fl_y"]
            cx = cam["intrinsic"]["cx"]
            cy = cam["intrinsic"]["cy"]
            k1 = cam["distortion"]["params"]["k1"]
            k2 = cam["distortion"]["params"]["k2"]
            k3 = cam["distortion"]["params"]["k3"]
            k4 = cam["distortion"]["params"]["k4"]
            lines.append(
                f"{idx} {model} {width} {height} {fx} {fy} {cx} {cy} {k1} {k2} {k3} {k4}"
            )
        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.out_path, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Wrote {self.out_path}")