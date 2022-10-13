import argparse
import os
import glob
import os.path as osp
import shutil
import sys

os.umask(0000)

from multiprocessing import Pool, cpu_count
from functools import partial

def generate_supervoxel(xyz_file, dest):
    filename = xyz_file.split('/')[-1].split('.')[0]
    print(f"Processing file {filename}")
    if osp.exists(osp.join(dest, f"{filename}_out.xyz")):
        print("File exists, skipping ...")
        return
    sys.stdout.flush()
    os.system(f"./build/supervoxel {osp.abspath(xyz_file)}")
    shutil.move(f"{filename}_out.xyz", osp.join(dest, f"{filename}_out.xyz"))
    shutil.move(f"{filename}_out_vccs.xyz", osp.join(dest, f"{filename}_out_vccs.xyz"))
    shutil.move(f"{filename}_out_vccs_knn.xyz", osp.join(dest, f"{filename}_out_vccs_knn.xyz"))
    shutil.move(f"{filename}_out_labels.txt", osp.join(dest, f"{filename}_out_labels.txt"))
    shutil.move(f"{filename}_out_supervoxel.txt", osp.join(dest, f"{filename}_out_supervoxel.txt"))
    shutil.move(f"{filename}_out_vccs_labels.txt", osp.join(dest, f"{filename}_out_vccs_labels.txt"))
    shutil.move(f"{filename}_out_vccs_knn_labels.txt", osp.join(dest, f"{filename}_out_vccs_knn_labels.txt"))

def main(args):
    xyz_files = glob.glob(osp.join(args.dir, "*.xyz"))
    with Pool(args.n_proc) as pool:
        pool.map(
            partial(generate_supervoxel, dest=args.dest),
            xyz_files
        )



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir")
    parser.add_argument("--dest")
    parser.add_argument("--n_proc", default=cpu_count(), type=int)
    args = parser.parse_args()

    os.makedirs(args.dest, exist_ok=True)
    main(args)