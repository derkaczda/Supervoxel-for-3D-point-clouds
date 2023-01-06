import argparse
import os
import glob
import os.path as osp
import shutil
import sys
import open3d as o3d
import tempfile
import shutil

os.umask(0000)

from multiprocessing import Pool, cpu_count
from functools import partial

def convert_ply_to_xyz(ply_file):
    filename = ply_file.split('/')[-1].split('.')[0]
    phase = ply_file.split('/')[-3]
    trial = ply_file.split('/')[-4]
    print(phase, trial)
    pcd = o3d.io.read_point_cloud(ply_file)
    save_path_tmp = osp.join(tempfile.gettempdir(), f"{filename}_{phase}_{trial}.xyzrgb")
    save_path = osp.join(tempfile.gettempdir(), f"{filename}_{phase}_{trial}.xyz")
    o3d.io.write_point_cloud(save_path_tmp, pcd)
    shutil.move(save_path_tmp, save_path)
    return save_path


def generate_supervoxel(ply_file, resolution):
    filename_ply = ply_file.split('/')[-1].split('.')[0]
    xyz_file = convert_ply_to_xyz(ply_file=ply_file)
    filename_xyz = xyz_file.split('/')[-1].split('.')[0]
    dest = osp.join('/', *ply_file.split('/')[0:-2], "superpoints")
    print(dest)
    os.makedirs(dest, exist_ok=True)
    print(f"Processing file {filename_xyz}")
    sys.stdout.flush()
    os.system(f"./build/supervoxel {osp.abspath(xyz_file)} {resolution}")
    shutil.move(f"{filename_xyz}_out_labels.txt", osp.join(dest, f"{filename_ply}.superpoint"))
    os.remove(f"{filename_xyz}_out.xyz")
    os.remove(f"{filename_xyz}_out_vccs.xyz")
    os.remove(f"{filename_xyz}_out_vccs_knn.xyz")
    os.remove(f"{filename_xyz}_out_supervoxel.txt")
    os.remove(f"{filename_xyz}_out_vccs_labels.txt")
    os.remove(f"{filename_xyz}_out_vccs_knn_labels.txt")
    os.remove(xyz_file)

def main(args):
    ply_files = glob.glob(osp.join(args.data_root,"*", "*", "pointclouds", "*_pointcloud.ply"))
    with Pool(args.n_proc) as pool:
        pool.map(
            partial(generate_supervoxel, resolution=args.resolution),
            ply_files
        )



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_root")
    parser.add_argument("--n_proc", default=cpu_count(), type=int)
    parser.add_argument("--resolution", type=float)
    args = parser.parse_args()

    main(args)
