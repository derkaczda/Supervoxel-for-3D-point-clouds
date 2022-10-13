import open3d as o3d
import argparse
import os.path as osp
import numpy as np
import os

def get_supervoxel_mapping(path):
    return np.loadtxt(path).astype(int)


def main(args):
    pcd = o3d.io.read_point_cloud(osp.join(args.xyz_dir, f"{args.filename}.xyz"), format="xyzrgb")
    mapping = get_supervoxel_mapping(osp.join(args.supervox_dir, f"{args.filename}_out_labels.txt"))
    supervoxel_ids = np.unique(mapping)

    colors = np.empty((mapping.shape[0], 3))
    for supervox_id in supervoxel_ids:
        mask = mapping == supervox_id
        colors[mask] = np.random.random(3)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.io.write_point_cloud(osp.join(args.dest, f"{args.filename}.ply"), pcd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--xyz_dir')
    parser.add_argument('--supervox_dir')
    parser.add_argument('--dest')
    parser.add_argument('--filename', help='without extension')
    args = parser.parse_args()
    os.makedirs(args.dest, exist_ok=True)
    main(args)