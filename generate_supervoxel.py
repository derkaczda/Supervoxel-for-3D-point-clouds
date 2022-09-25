import argparse
import os
import glob
import os.path as osp
import shutil

def main(args):
    xyz_files = glob.glob(osp.join(args.dir, "*.xyz"))

    for xyz in xyz_files:
        filename = xyz.split('/')[-1][:-len(".xyz")]
        print(filename)
        os.system(f"./build/supervoxel {osp.abspath(xyz)}")
        shutil.move("out.xyz", osp.join(args.dest, f"{filename}_out.xyz"))
        shutil.move("out_vccs.xyz", osp.join(args.dest, f"{filename}_out_vccs.xyz"))
        shutil.move("out_vccs_knn.xyz", osp.join(args.dest, f"{filename}_out_vccs_knn.xyz"))
        shutil.move("out_labels.txt", osp.join(args.dest, f"{filename}_out_labels.txt"))
        shutil.move("out_supervoxel.txt", osp.join(args.dest, f"{filename}_out_supervoxel.txt"))
        shutil.move("out_vccs_labels.txt", osp.join(args.dest, f"{filename}_out_vccs_labels.txt"))
        shutil.move("out_vccs_knn_labels.txt", osp.join(args.dest, f"{filename}_out_vccs_knn_labels.txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir")
    parser.add_argument("--dest")
    args = parser.parse_args()

    os.makedirs(args.dest, exist_ok=True)
    main(args)