import open3d as o3d
import argparse
import os.path as osp
import numpy as np
import os
import glob

def get_supervoxel_mapping(path):
    return np.loadtxt(path).astype(int)


def main(args):
    pointcloud_files = sorted(glob.glob(osp.join(args.data_root, args.trial, args.phase, 'pointclouds', '*_pointcloud.ply')))
    superpoint_files = sorted(glob.glob(osp.join(args.data_root, args.trial, args.phase, 'superpoints', '*_pointcloud.superpoint')))
    files = list(zip(pointcloud_files, superpoint_files))

    for pcd_file, sup_file in files:
        filename = pcd_file.split('/')[-1].split('.')[0]
        pcd = o3d.io.read_point_cloud(pcd_file)
        superpoints = np.loadtxt(sup_file)
        superpoint_ids = np.unique(superpoints)
        colormap = np.random.random((superpoint_ids.shape[0], 3))
        colors = np.empty((superpoints.shape[0], 3))
        for idx, superpoint_id in enumerate(superpoint_ids):
            point_ids = superpoints == superpoint_id
            colors[point_ids] = colormap[idx]

        pcd.colors = o3d.utility.Vector3dVector(colors)
        o3d.io.write_point_cloud(
            osp.join(args.dest, f"{filename}.ply"),
            pcd
        )


    # pcd = o3d.io.read_point_cloud(osp.join(args.xyz_dir, f"{args.filename}.ply"))
    # mapping = get_supervoxel_mapping(osp.join(args.supervox_dir, f"{args.filename}_out_labels.txt"))
    # supervoxel_ids = np.unique(mapping)

    # colors = np.empty((mapping.shape[0], 3))
    # for supervox_id in supervoxel_ids:
    #     mask = mapping == supervox_id
    #     colors[mask] = np.random.random(3)
    # pcd.colors = o3d.utility.Vector3dVector(colors)
    # o3d.io.write_point_cloud(osp.join(args.dest, f"{args.filename}.ply"), pcd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root')
    parser.add_argument('--trial')
    parser.add_argument('--phase')
    parser.add_argument('--dest')
    args = parser.parse_args()
    os.makedirs(args.dest, exist_ok=True)
    main(args)