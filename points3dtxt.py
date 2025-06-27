import open3d as o3d
from pathlib import Path
import numpy as np

def load_all_pcd_points(lidar_dir):
    points = []
    for pcd_file in sorted(Path(lidar_dir).glob("*.pcd")):
        pcd = o3d.io.read_point_cloud(str(pcd_file))
        if len(pcd.points) > 0:
            pts = np.asarray(pcd.points)
            points.append(pts)
    if points:
        return np.vstack(points)
    else:
        return np.zeros((0, 3))

def write_colmap_points3d(points, out_path):
    with open(out_path, "w") as f:
        f.write("# 3D point list with one line of data per point:\n")
        f.write("#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)\n")
        f.write(f"# Number of points: {len(points)}, mean track length: 0\n")
        for idx, pt in enumerate(points, 1):
            x, y, z = pt
            r, g, b = 128, 128, 128
            error = 1.0
            f.write(f"{idx} {x} {y} {z} {r} {g} {b} {error}\n")

if __name__ == "__main__":
    lidar_dir = "/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10/lidar"
    out_path = "/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10/colmap/points3D.txt"
    points = load_all_pcd_points(lidar_dir)
    print(f"Loaded {points.shape[0]} points from {lidar_dir}")
    write_colmap_points3d(points, out_path)
    print(f"Wrote COLMAP points3D.txt to {out_path}")