import open3d as o3d
import argparse
import os.path as osp
import numpy as np

def get_supervoxel_mapping(path):
    return np.loadtxt(path).astype(int)


def main(args):
    pcd = o3d.io.read_point_cloud(osp.join(args.dir, "out.xyz"), format="xyzrgb")
    mapping = get_supervoxel_mapping(osp.join(args.dir, "out_labels.txt"))
    supervoxel_ids = np.unique(mapping)

    colors = np.empty((mapping.shape[0], 3))
    for supervox_id in supervoxel_ids:
        mask = mapping == supervox_id
        colors[mask] = np.random.random(3)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.io.write_point_cloud(osp.join(args.dir, "out.ply"), pcd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir')
    args = parser.parse_args()
    main(args)