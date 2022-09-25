import open3d as o3d
import argparse
import os.path as osp
import os
import glob
import numpy as np
import shutil

def main(args):
    os.makedirs(args.dest, exist_ok=True)
    pointcloud_files = glob.glob(osp.join(args.dir, "samples", "LIDAR_TOP", "*.bin"))
    for i, file in enumerate(pointcloud_files):
        filename = file.split('/')[-1][:-len(".pcd.bin")]
        points = np.fromfile(
            file,
            dtype=np.float32,
        ).reshape([-1, 5])[:,:3]
        colors = np.zeros((points.shape[0], 3))
        pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
        pc.colors = o3d.utility.Vector3dVector(colors)
        o3d.io.write_point_cloud(osp.join(args.dest, f"{filename}.xyzrgb"), pc)

    xyzrgbfiles = glob.glob(osp.join(args.dest, "*.xyzrgb"))
    for xyzrgbfile in xyzrgbfiles:
        without_extension = xyzrgbfile[:-len("xyzrgb")]
        shutil.move(xyzrgbfile, f"{without_extension}.xyz")

    # pcd = o3d.io.read_point_cloud(osp.join(args.dir, "out.ply"))
    # o3d.io.write_point_cloud(osp.join(args.dir, "out_test.xyzrgb"), pcd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir')
    parser.add_argument('--dest')
    args = parser.parse_args()
    main(args)