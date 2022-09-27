import open3d as o3d
import argparse
import os.path as osp

import os
os.umask(0000)

def main(args):
    pcd = o3d.io.read_point_cloud(osp.join(args.dir, "out.xyz"), format="xyzrgb")
    o3d.io.write_point_cloud(osp.join(args.dir, "out.ply"), pcd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir')
    args = parser.parse_args()
    main(args)