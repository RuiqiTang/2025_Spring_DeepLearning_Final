import os
import json
import argparse
import numpy as np
import pycolmap
import random


def qvec2rotmat(qvec):
    """Convert quaternion to rotation matrix."""
    q0, q1, q2, q3 = qvec
    return np.array([
        [1 - 2*q2**2 - 2*q3**2,     2*q1*q2 - 2*q0*q3,     2*q1*q3 + 2*q0*q2],
        [2*q1*q2 + 2*q0*q3,         1 - 2*q1**2 - 2*q3**2, 2*q2*q3 - 2*q0*q1],
        [2*q1*q3 - 2*q0*q2,         2*q2*q3 + 2*q0*q1,     1 - 2*q1**2 - 2*q2**2]
    ])


def convert_colmap_to_nerf(sparse_dir, image_dir, out_path, seed=42):
    recon = pycolmap.Reconstruction(sparse_dir)

    all_frames = []
    up = []
    positions = []

    for image_id, image in recon.images.items():
        name = image.name
        qvec = image.qvec
        tvec = image.tvec
        R = qvec2rotmat(qvec)
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, 3] = tvec
        T = np.linalg.inv(T)  # camera-to-world

        positions.append(T[:3, 3])
        up.append(T[:3, 1])

        frame = {
            "file_path": os.path.join(image_dir, name),
            "transform_matrix": T.tolist(),
        }
        all_frames.append(frame)

    # normalize scene
    positions = np.array(positions)
    center = positions.mean(axis=0)
    scale = np.linalg.norm(positions - center, axis=1).max()
    for f in all_frames:
        M = np.array(f["transform_matrix"])
        M[:3, 3] -= center
        M[:3, 3] /= scale
        f["transform_matrix"] = M.tolist()

    # shuffle & split
    random.seed(seed)
    random.shuffle(all_frames)
    N = len(all_frames)
    train_frames = all_frames[:int(0.8*N)]
    val_frames = all_frames[int(0.8*N):int(0.9*N)]
    test_frames = all_frames[int(0.9*N):]

    cam = recon.cameras[1]
    fx = cam.params[0]
    w = cam.width
    cx = cam.params[1]
    camera_angle_x = 2 * np.arctan(w / (2 * fx))

    def write_split(name, frames):
        out = {
            "camera_angle_x": float(camera_angle_x),
            "frames": frames
        }
        out_file = os.path.join(out_path, f"transforms_{name}.json")
        with open(out_file, "w") as f:
            json.dump(out, f, indent=4)
        print(f"✅ transforms_{name}.json saved to {out_file}")

    write_split("train", train_frames)
    write_split("val", val_frames)
    write_split("test", test_frames)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", type=str, default="colmap/sparse/0", help="Path to sparse/0")
    parser.add_argument("--images", type=str, default="nerf_data/images", help="Image folder")
    parser.add_argument("--out", type=str, default="nerf_data", help="Output folder")
    args = parser.parse_args()

    convert_colmap_to_nerf(args.bin, args.images, args.out)
