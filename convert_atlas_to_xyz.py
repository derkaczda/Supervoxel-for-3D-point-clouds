import open3d as o3d
import argparse
import os.path as osp
import os
import glob
import numpy as np
import shutil

NUM_CAMS = 4

def merge_convert(args, dest_path):
    file_ids = glob.glob(osp.join(args.dir, args.phase, "cn01", "*.ply"))
    file_ids = [file_id.split('/')[-1][:-len("_pointcloud.ply")] for file_id in file_ids]
    for file_id in file_ids:
        pointcloud, colors = [], []
        for cam_id in range(1, NUM_CAMS+1):
            pointcloud_path = osp.join(args.dir, args.phase, f"cn0{cam_id}", f"{file_id}_pointcloud.ply")
            data = o3d.io.read_point_cloud(pointcloud_path)
            pointcloud.append(
                np.asarray(data.points)
            )
            colors.append(
                np.asarray(data.colors)
            )

        pointcloud = np.concatenate(pointcloud, axis=0)
        colors = np.concatenate(colors, axis=0)
        pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pointcloud))
        pc.colors = o3d.utility.Vector3dVector(colors)
        o3d.io.write_point_cloud(osp.join(dest_path, f"{file_id}.xyzrgb"), pc)
        print("saved")
        shutil.move(
            osp.join(dest_path, f"{file_id}.xyzrgb"),
            osp.join(dest_path, f"{file_id}.xyz")
        )

def convert(args, dest_path):
    for cam_id in range(1, NUM_CAMS + 1):
        files = glob.glob(osp.join(args.dir, args.phase, f"cn0{cam_id}", "*.ply"))
        for file in files:
            file_id = file.split('/')[-1][:-len("_pointcloud.ply")]
            pc = o3d.io.read_point_cloud(file)
            o3d.io.write_point_cloud(osp.join(dest_path, f"{file_id}_cn0{cam_id}.xyzrgb"), pc)
            shutil.move(
                osp.join(dest_path, f"{file_id}_cn0{cam_id}.xyzrgb"),
                osp.join(dest_path, f"{file_id}_cn0{cam_id}.xyz")
            )


def main(args):
    dest_path = osp.join(args.dir, args.phase, 'xyz_data')
    os.makedirs(dest_path, exist_ok=True)
    if args.merge:
        merge_convert(args, dest_path)
    else:
        convert(args, dest_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir')
    parser.add_argument('--phase')
    parser.add_argument('--merge', action='store_true', default=False)
    args = parser.parse_args()
    main(args)